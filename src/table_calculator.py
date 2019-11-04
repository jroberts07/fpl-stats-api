from sanic.log import logger

from database_adapter import get_local_entry_team_data, put_local_league_data
from fpl_adapter import get_remote_entry_team_data
from utils.exceptions import LocalDataNotFound


async def update_teams(league_table, gameweek, player_cookie, app):
    for entry in league_table:
        try:
            entry_team_data = await get_local_entry_team_data(
                app.db, entry['entry_id'], gameweek
            )
        except LocalDataNotFound:
            entry_team_data = await get_remote_entry_team_data(
                entry['entry_id'], gameweek, player_cookie, app
            )
        except Exception as e:
            logger.exception(e)
            entry_team_data = await get_remote_entry_team_data(
                entry['entry_id'], gameweek, player_cookie, app
            )
        # Clear the existing team or create a new one.
        entry['team'] = []
        for index, player in enumerate(entry_team_data['picks']):
            if index > 10:
                break
            else:
                entry['team'].append(
                    {
                        "element_id": player['element'],
                        "multiplier": player['multiplier'],
                    }
                )
    return league_table
