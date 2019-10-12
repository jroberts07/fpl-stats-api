import datetime

from sanic.log import logger

from utils.constants import ENTRY_DATA_ERROR_MSG
from utils.exceptions import FantasyDataException


async def process_remote_league_data(remote_league_data):
    """Takes league data from the remote API and converts it into a useful
    format.

    Args:
        remote_league_data (obj): The league data from the API.

    Returns:
        obj: The league data in a useful format

    Raises:
        FantasyDataException: If there is an error processing the data returned
        by the FPL API.
    """
    try:
        league_data = {
            'league_id': str(remote_league_data['league']['id']),
            'league_name': remote_league_data['league']['name'],
            'standings': [],
            'time_updated': datetime.datetime.now()
        }
        for entry in remote_league_data['standings']['results']:
            league_data['standings'].append(
                {
                    'rank': entry['rank'],
                    'previous_rank': entry['rank'],
                    'entry_name': entry['entry_name'],
                    'player_name': entry['player_name'],
                    'gameweek_points': entry['event_total'],
                    'total_points': entry['total']
                }
            )
    except Exception as e:
        logger.error(e)
        raise FantasyDataException(ENTRY_DATA_ERROR_MSG)
    return league_data
