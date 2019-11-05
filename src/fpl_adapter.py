from sanic.log import logger

from database_adapter import put_local_static_data
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
