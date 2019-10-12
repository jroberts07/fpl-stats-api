from sanic.log import logger

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
        logger.error(e)
        raise FantasyConnectionException(FANTASY_CONNECTION_ERROR_MSG)
