from aiounittest import AsyncTestCase
import json

from process_league_data import process_remote_league_data
from utils.exceptions import FantasyDataException


class TestProcessRemoteLeagueData(AsyncTestCase):
    """Async test class for testing process remote league data

    Args:
        obj: Async test class from the aiounittest library.
    """

    async def test_multiple_entries(self):
        """Test league with multiple entries.
        """
        with open(
                'tests/unit/data/league_table_response_multiple_entries.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = await process_remote_league_data(league_data)
        self.assertEqual(
            result,
            {
                'league_id': "123",
                'league_name': "League A",
                'start_time': None,
                'end_time': None,
                "standings": [
                                {
                                    'entry_id': "100",
                                    'player_name': "Player A",
                                    'entry_name': "Team A",
                                    'live_points': 0,
                                    'total_points': 390,
                                    'confirmed_rank': 1,
                                    'live_rank': 0
                                },
                                {
                                    'entry_id': "200",
                                    'player_name': "Player B",
                                    'entry_name': "Team B",
                                    'live_points': 0,
                                    'total_points': 280,
                                    'confirmed_rank': 2,
                                    'live_rank': 0
                                }
                            ]
            }
        )

    async def test_one_entry(self):
        """Test league with one entry.
        """
        with open(
                'tests/unit/data/league_table_response_one_entry.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = await process_remote_league_data(league_data)
        self.assertEqual(
            result,
            {
                'league_id': "123",
                'league_name': "League A",
                'start_time': None,
                'end_time': None,
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

    async def test_bad_data(self):
        """Test bad response from API.
        """
        with open(
                'tests/unit/data/bad_data.json'
        ) as json_file:
            league_data = json.load(json_file)
        with self.assertRaises(FantasyDataException):
            await process_remote_league_data(league_data)
