import asyncio
from http import HTTPStatus
import motor.motor_asyncio
from sanic import Sanic
from sanic import response
from sanic_cors import CORS
from sanic.log import access_logger
from sanic.log import logger
import time
import uuid

from fpl_adapter import call_fpl_endpoint, get_remote_live_data
from league_data_handler import add_times_to_league_data, get_league_data
from process_entry_data import get_leagues_entered, get_name
from static_data_handler import get_static_data, determine_current_gameweek
from team_picks_handler import get_entry_picks
from utils.commons import validate_mandatory
from utils.exceptions import (
    FantasyConnectionException, FantasyDataException, ValidationException
)

app = Sanic(__name__)
CORS(app)
app.config.from_pyfile('/usr/src/app/config.py')


@app.listener('before_server_start')
async def setup_db(app, loop):
    """Creates a mongo_db client. Disables the sanic default logger.
    @TODO Use MongoDB for storing some static data so we don't have to keep
    querying the remote API.

    Args:
        app (obj): The sanic app object.
        loop (obj): The event loop.

    """
    access_logger.disabled = True
    client = motor.motor_asyncio.AsyncIOMotorClient(
        app.config.MONGODB_URI
    )
    app.db = client.fpl_stats


@app.middleware('request')
async def add_start_time(request):
    """Called every time the server receives a request. Is used to log the
    request.

    Args:
        request (obj): The request object.

    """
    request['start_time'] = time.time()
    request['uid'] = str(uuid.uuid4())
    if '/ping' not in request.path:
        logger.info(
            "uid: {0} | request: [{1}] {2} | body: {3}".format(
                request['uid'], request.method, request.path, request.json
            )
        )


@app.middleware('response')
async def add_spent_time(request, resp):
    """Called every time the server returns a response. Is used to calculate
    the time spent and log the response.

    Args:
        request (obj): The request object.
        resp (object): The response.

    """
    spend_time = round((time.time() - request['start_time']) * 1000)
    if '/ping' not in request.path:
        logger.info(
            "uid: {0} | response code: {1} | body:  {2}  | time: {3}ms".format(
                request['uid'], resp.status, resp.body, spend_time
            )
        )


@app.get("/entry_data/<entry_id>")
async def entry_data_endpoint(request, entry_id):
    """Entry data endpoint. Will return the leagues the requested entry
    id has entered and the team name.

    Args:
        request (obj): The request object.
        entry_id (str): The entry id.

    Returns:
       obj: The response object returned to the user.

    """
    try:
        player_cookie = [
            x[1] for x in request.query_args if x[0] == 'player_cookie'
        ]
        validate_mandatory(
            {
                'entry_id': entry_id,
                'player_cookie': player_cookie
            }
        )
        url = app.config.FPL_URL + app.config.ENTRY_DATA.format(
            entry_id=entry_id
        )
        entry_data = await call_fpl_endpoint(
            url, player_cookie, app.config
        )
        leagues, name = await asyncio.gather(
            get_leagues_entered(entry_data, player_cookie, app.config),
            get_name(entry_data)
        )
    except ValidationException as e:
        return response.json(
            e.get_message(),
            status=HTTPStatus.BAD_REQUEST
        )
    except FantasyConnectionException as e:
        return response.json(
            e.get_message(),
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    except FantasyDataException as e:
        return response.json(
            e.get_message(),
            status=HTTPStatus.INTERNAL_SERVER_ERROR
        )
    return response.json(
        {
            'name': name,
            'leagues': leagues
        }
    )


@app.get("/league_table/<league_id>")
async def league_table_endpoint(request, league_id):
    """League table endpoint. Will return the league name and live table of the
    requested ID.

    Args:
     request (obj): The request object.
     league_id (str): The league id.

    Returns:
    obj: The response object returned to the user.

    """
    try:
        player_cookie = [
            x[1] for x in request.query_args if x[0] == 'player_cookie'
        ]
        validate_mandatory(
            {
                'league_id': league_id,
                'player_cookie': player_cookie
            }
        )
        (
            gameweeks, (update_league, league_data)
        ) = await asyncio.gather(
            get_static_data(app, player_cookie, 'events'),
            get_league_data(app, player_cookie, league_id)
        )
        current_gameweek = await determine_current_gameweek(gameweeks)
        # True if league data has been fetched remotley, meaning we need to add
        # gameweek info.
        if update_league:
            league_data = await add_times_to_league_data(
                app.db, league_data, current_gameweek
            )
        league_data = await get_entry_picks(
            player_cookie, app, league_data, current_gameweek['id']
        )
        live_data = await get_remote_live_data(
            current_gameweek['id'], player_cookie, app
        )
        return response.json(
            league_data
        )
    except ValidationException as e:
        return response.json(
            e.get_message(),
            status=HTTPStatus.BAD_REQUEST
        )


@app.route("/ping")
async def ping_endpoint(request):
    """Ping endpoint. Responds to ping requests.

    Args:
        request (obj): The request object.

    Returns:
        obj: The response object returned to the user.

    """
    return response.json({"ping": "ok"})

if __name__ == '__main__':
    debug = app.config.LOG_LEVEL == 'DEBUG'
    app.run(
        host="0.0.0.0",
        port=8000,
        access_log=debug,
        workers=4,
        debug=debug,
    )
