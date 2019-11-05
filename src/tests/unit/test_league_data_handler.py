from aiounittest import AsyncTestCase
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
                'start_time': "2019-08-09T18:00:00Z",
                'end_time': "2019-08-09T19:00:00Z",
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
