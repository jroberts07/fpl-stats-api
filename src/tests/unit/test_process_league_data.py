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
                'tests/unit/data/league_response_multiple_entries.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = await process_remote_league_data(league_data)
        self.assertEqual(
            result['standings'],
            [
                {
                    "rank": 1,
                    "previous_rank": 1,
                    "entry_name": "Team A",
                    "player_name": "Player A",
                    "gameweek_points": 42,
                    "total_points": 453
                },
                {
                    "rank": 1,
                    "previous_rank": 1,
                    "entry_name": "Team B",
                    "player_name": "Player B",
                    "gameweek_points": 43,
                    "total_points": 453
                }
            ]

        )
        self.assertEqual(result['league_name'], "Caversham Gossip Girls")

    async def test_one_entry(self):
        """Test league with one entry.
        """
        with open(
                'tests/unit/data/league_response_one_entry.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = await process_remote_league_data(league_data)
        self.assertEqual(
            result['standings'],
            [
                {
                    "rank": 1,
                    "previous_rank": 1,
                    "entry_name": "Team A",
                    "player_name": "Player A",
                    "gameweek_points": 42,
                    "total_points": 453
                }
            ]

        )
        self.assertEqual(result['league_name'], "Caversham Gossip Girls")

    async def test_bad_data(self):
        """Test bad response from API.
        """
        with open(
                'tests/unit/data/bad_response.json'
        ) as json_file:
            league_data = json.load(json_file)
        with self.assertRaises(FantasyDataException):
            await process_remote_league_data(league_data)
