from sanic.log import logger

from database_adapter import get_local_static_data
from fpl_adapter import get_remote_static_data
from utils.constants import ENTRY_DATA_ERROR_MSG
from utils.exceptions import (FantasyDataException, LocalDataNotFoundException)


async def get_static_data(app, player_cookie, field):
    """Returns the field requested from the static data.

    Args:
        app (obj): Then sanic app.
        player_cookie (str): Cookie used for FPL api,
        field (str): The requested static data field.

    Returns:
        obj: The requested field.

    """
    try:
        local_static_data = await get_local_static_data(app.db, field)
        field_data = local_static_data[field]
    except LocalDataNotFoundException:
        static_data = await get_remote_static_data(player_cookie, app)
        field_data = static_data[field]
    except Exception as e:
        logger.exception(e)
        static_data = await get_remote_static_data(player_cookie, app)
        field_data = static_data[field]
    return field_data


async def determine_current_gameweek(gameweeks):
    """Determines the current gameweek.

    Args:
        gameweeks (obj): An array containing all the gameweeks data.

    Returns:
        obj: The current gameweek info.

    Raises:
        FantasyDataException: If there is an error processing the data returned
        by the FPL API.
    """
    try:
        for gameweek in gameweeks:
            if gameweek['is_current']:
                end_time = None
                try:
                    end_time = gameweeks[gameweek['id']]['deadline_time']
                except IndexError:
                    logger.debug('Last day of season, end_time set to None')
                relevant_gameweek_info = {
                    "id": gameweek['id'],
                    "start_time": gameweek['deadline_time'],
                    # The deadline time of the following game week
                    # (can use ID as array index starts at 0).
                    # Set to none if no next gameweek (last day of season).
                    "end_time": end_time
                }
                return relevant_gameweek_info
        logger.error('NO GAMEWEEKS CURRENTLY ACTIVE')
        raise FantasyDataException(ENTRY_DATA_ERROR_MSG)
    except Exception as e:
        logger.exception(e)
        raise FantasyDataException(ENTRY_DATA_ERROR_MSG)
