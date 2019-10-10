from sanic.log import logger

from fpl_adapter import call_fpl_endpoint
from utils.constants import ENTRY_DATA_ERROR_MSG
from utils.exceptions import FantasyConnectionException, FantasyDataException


async def get_leagues_entered(entry_data, player_cookie, config):
    """Takes raw entry data and extracts the league's id and name.
    Only includes leagues with less than 50 entries in the response

    Args:
        entry_data (obj): The raw entry data.
        player_cookie (obj): The player cookie used for authentication on
        the FPL API.
        config (obj): The config of the sanic app.

    Returns:
        array: An array of the ids and names of the leagues the player has
        entered.

    Raises:
        FantasyConnectionException: If there is an error connecting to the
        FPL API.
        FantasyDataException: If there is an error processing the data returned
        by the FPL API.
    """
    leagues_entered = []
    try:
        for league in entry_data['leagues']['classic']:
            if await less_than_fifty_entries(
                    league['id'], player_cookie, config
            ):
                leagues_entered.append(
                    {
                        'id': league['id'],
                        'name': league['name']
                    }
                )
    except FantasyConnectionException:
        raise
    except Exception as e:
        logger.error(e)
        raise FantasyDataException(ENTRY_DATA_ERROR_MSG)
    return leagues_entered


async def get_name(entry_data):
    """Takes raw entry data and extracts the player name.

    Args:
        entry_data (obj): The raw entry data.

    Returns:
        string: The player name.
    """
    if 'name' in entry_data:
        return entry_data['name']
    else:
        return None


async def less_than_fifty_entries(league_id, player_cookie, config):
    """Determines whether a league contains more than 50 entries.

    Args:
        league_id (string): The ID of the league.
        player_cookie (obj): The player cookie used for authentication on
        the FPL API.
        config (obj): The config of the sanic app.

    Returns:
        bool: Whether the league contains more than 50 entries
    """
    url = config.FPL_URL + config.LEAGUE_DATA.format(
        league_id=league_id
    )
    league_data = await call_fpl_endpoint(
        url, player_cookie, config
    )
    if (
            len(league_data['standings']['results']) <= 50
            and not league_data['standings']['has_next']
    ):
        return True
    else:
        return False
