from sanic.log import logger

from database_adapter import (put_local_league_data, put_local_static_data)
from process_league_data import process_remote_league_data
from utils.client import get_session
from utils.constants import FANTASY_CONNECTION_ERROR_MSG
from utils.exceptions import FantasyConnectionException
from utils.logging import fpl_log_request, fpl_log_response


async def call_fpl_endpoint(url, player_cookie, config):
    """Calls the FPL endpoint requested and returns the data.

    Args:
        url (string): The FPL URL to call
        player_cookie (obj): The player cookie used for authentication on
        the FPL API.
        config (obj): The config of the sanic app.

    Returns:
        obj: The endpoint data in a json response.

    Raises:
        FantasyConnectionException: If there is an error connecting to the
        FPL API.

    """
    cookie_header = config.LOGIN_COOKIE_HEADER
    cookie_header['Cookie'] = cookie_header['Cookie'].format(
        player_cookie=player_cookie
    )
    try:
        async with get_session() as session:
            start_time, uid = fpl_log_request(
                'GET', url,
                None
            )
            async with session.get(
                    url,
                    headers={**config.USER_AGENT_HEADER, **cookie_header}
            ) as resp:
                fpl_log_response(
                    start_time, uid, resp.status, await resp.text()
                )
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise FantasyConnectionException(
                        FANTASY_CONNECTION_ERROR_MSG
                    )
    except Exception as e:
        logger.exception(e)
        raise FantasyConnectionException(FANTASY_CONNECTION_ERROR_MSG)


async def get_remote_static_data(player_cookie, app):
    """Function responsible for gathering remote static data processing
    it and storing it locally

    Args:
        player_cookie (obj): The player cookie used for authentication on
        the FPL API.
        app (obj): The sanic app.

    Returns:
        obj: The static data in a useful format.
    """
    logger.info('Fetching remote static data')
    url = app.config.FPL_URL + app.config.STATIC_DATA
    remote_static_data = await call_fpl_endpoint(
            url, player_cookie, app.config
    )
    try:
        await put_local_static_data(app.db, remote_static_data)
    except Exception as e:
        # Log the error but we don't care if we cant save locally.
        logger.exception(e)
    return remote_static_data


async def get_remote_league_data(league_id, player_cookie, app):
    """Function responsible for gathering remote league data processing
    it and storing it locally
    Args:
        league_id (int): The ID of the league to fetch.
        player_cookie (obj): The player cookie used for authentication on
        the FPL API.
        app (obj): The sanic app.
    Returns:
        obj: The league data in a useful format.
    """
    logger.info('Fetching remote league data')
    url = app.config.FPL_URL + app.config.LEAGUE_DATA.format(
        league_id=league_id
    )
    remote_league_data = await process_remote_league_data(
        await call_fpl_endpoint(
            url, player_cookie, app.config
        )
    )
    try:
        await put_local_league_data(app.db, remote_league_data)
    except Exception as e:
        # Log the error but we don't care if we cant save locally.
        logger.exception(e)
    return remote_league_data


async def get_remote_picks_data(entry_id, gameweek, player_cookie, app):
    """Function responsible for gathering remote picks data for the entry requested
    Args:
        entry_id (int): The ID of the entry to fetch.
        gameweek (int): The gameweek to get the picks for.
        player_cookie (obj): The player cookie used for authentication on
        the FPL API.
        app (obj): The sanic app.
    Returns:
        obj: The picks for the requested entry for that gameweek.
    """
    logger.info('Fetching remote picks data')
    url = app.config.FPL_URL + app.config.PICKS_DATA.format(
        entry_id=entry_id, gameweek=gameweek
    )
    return await call_fpl_endpoint(
            url, player_cookie, app.config
    )


async def get_remote_live_data(gameweek, player_cookie, app):
    """Function responsible for gathering remote live data.
    Args:
        gameweek (int): The gameweek to get the live data for.
        player_cookie (obj): The player cookie used for authentication on
        the FPL API.
        app (obj): The sanic app.
    Returns:
        obj: The live data.
    """
    logger.info('Fetching remote live data')
    url = app.config.FPL_URL + app.config.LIVE_DATA.format(
        gameweek=gameweek
    )
    return await call_fpl_endpoint(
            url, player_cookie, app.config
    )
