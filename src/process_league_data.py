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
            'start_time': None,
            'end_time': None,
            'standings': []
        }
        for entry in remote_league_data['standings']['results']:
            league_data['standings'].append(
                {
                    'entry_id': str(entry['entry']),
                    'player_name': entry['player_name'],
                    'entry_name': entry['entry_name'],
                    'live_points': 0,
                    'total_points': entry['total'] - entry['event_total'],
                    'confirmed_rank': entry['rank_sort'],
                    'live_rank': 0
                }
            )
    except Exception as e:
        logger.exception(e)
        raise FantasyDataException(ENTRY_DATA_ERROR_MSG)
    return league_data
