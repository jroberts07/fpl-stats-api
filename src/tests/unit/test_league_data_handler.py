from aiounittest import AsyncTestCase
from datetime import datetime
import json

from server import app

from league_data_handler import add_times_to_league_data


class TestAddDatesToLeagueData(AsyncTestCase):
    """Async test class for testing the function that adds the dates for the
    gamweek to the league data.

    Args:
        obj: Async test class from the aiounittest library.
    """

    async def test_times_added(self):
        """Test with times are added.
        """
        with open(
                'tests/unit/data/gameweek.json'
        ) as json_file:
            gameweek = json.load(json_file)
        with open(
                'tests/unit/data/league_data.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = await add_times_to_league_data(
            app.db, league_data, gameweek
        )
        self.assertEqual(
            result,
            {
                'league_id': "123",
                'league_name': "League A",
                'start_time': datetime(2019, 8, 9, 18, 0),
                'end_time': datetime(2019, 8, 9, 19, 0),
                "standings": [
                    {
                        'entry_id': "100",
                        'player_name': "Player A",
                        'entry_name': "Team A",
                        'live_points': 0,
                        'total_points': 390,
                        'confirmed_rank': 1,
                        'live_rank': 0
                    }
                ]
            }
        )
