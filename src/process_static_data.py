from sanic.log import logger

from utils.constants import ENTRY_DATA_ERROR_MSG
from utils.exceptions import FantasyDataException


async def determine_current_gameweek(gameweeks):
    """Determines the current gameweek.

    Args:
        gameweeks (obj): An array containing all the gameweeks data.

    Returns:
        int: The current gameweek.

    Raises:
        FantasyDataException: If there is an error processing the data returned
        by the FPL API.
    """
    try:
        for gameweek in gameweeks:
            if gameweek['is_current']:
                return gameweek['id']
        logger.error('NO GAMEWEEKS CURRENTLY ACTIVE')
        raise FantasyDataException(ENTRY_DATA_ERROR_MSG)
    except Exception as e:
        logger.exception(e)
        raise FantasyDataException(ENTRY_DATA_ERROR_MSG)
