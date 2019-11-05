from sanic.log import logger

from database_adapter import (put_local_league_data, get_local_league_data)
from fpl_adapter import get_remote_league_data
from utils.exceptions import LocalDataNotFoundException


async def get_league_data(app, player_cookie, league_id):
    """Returns the league table for the requested league_id.

    Args:
        app (obj): Then sanic app.
        player_cookie (str): Cookie used for FPL api.
        league_id (int): The ID of the requested league.
        current_gameweek (obj): Information about the current gameweek.

    Returns:
        obj: The requested league table.

    """
    try:
        league_data = await get_local_league_data(app.db, league_id)
        remote_data = False
    except LocalDataNotFoundException:
        league_data = await get_remote_league_data(
            league_id, player_cookie, app
        )
        remote_data = True
    except Exception as e:
        logger.exception(e)
        league_data = await get_remote_league_data(
            league_id, player_cookie, app
        )
        remote_data = True
    return remote_data, league_data


async def add_times_to_league_data(db, league_data, gameweek):
    """Adds the start and end times for the current gameweek to the league
    table and stores locally.

    Args:
        db (obj): Then database session.
        league_data (obj): The league data.
        gameweek (obj): Information about the current gameweek.

    Returns:
        obj: The league data.

    """
    league_data['start_time'] = gameweek['start_time']
    league_data['end_time'] = gameweek['end_time']
    try:
        await put_local_league_data(db, league_data)
    except Exception as e:
        # Log the error but we don't care if we cant save locally.
        logger.exception(e)
    return league_data
