from sanic.log import logger

from utils.client import get_session
from utils.constants import FANTASY_CONNECTION_ERROR_MSG
from utils.exceptions import FantasyConnectionException


async def get_entry_data(player_id, entry_id, config):
    """Gets the entry data from the FPL API.

    Args:
        player_id (obj): The player cookie used for authentication on
        the FPL API.
        entry_id (obj): The players entry id.
        config (obj): The config of the sanic app.

    Returns:
        obj: The entry data in a json response.

    Raises:
        FantasyConnectionException: If there is an error connecting to the
        FPL API.

    """
    cookie_header = config.LOGIN_COOKIE_HEADER
    cookie_header['Cookie'] = cookie_header['Cookie'].format(
        player_id=player_id
    )
    try:
        async with get_session() as session:
            async with session.get(
                config.FPL_URL + config.ENTRY_DATA.format(
                    entry_id=entry_id
                ),
                headers={**config.USER_AGENT_HEADER, **cookie_header}
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    raise FantasyConnectionException(
                        FANTASY_CONNECTION_ERROR_MSG
                    )
    except Exception as e:
        logger.error(e)
        raise FantasyConnectionException(FANTASY_CONNECTION_ERROR_MSG)
