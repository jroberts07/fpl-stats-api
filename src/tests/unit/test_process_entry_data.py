from aiounittest import futurized, AsyncTestCase
import json
from unittest.mock import Mock, patch

from process_entry_data import get_leagues_entered, get_name
from utils.exceptions import FantasyDataException


class TestGetLeaguesEntered(AsyncTestCase):
    """Async test class for testing leagues entered.

    Args:
        obj: Async test class from the aiounittest library.
    """
    player_cookie = 'TEST'
    config = None

    async def test_no_classic(self):
        """Test with no classic leagues.
        """
        with open(
                'tests/unit/data/entry_response_no_leagues.json'
        ) as json_file:
            entry_data = json.load(json_file)
        result = await get_leagues_entered(
            entry_data, self.player_cookie, self.config
        )
        self.assertEqual(result, [])

    async def test_no_league_field(self):
        """Test with no leagues at all.
        """
        with open(
                'tests/unit/data/entry_response_no_league_field.json'
        ) as json_file:
            entry_data = json.load(json_file)
        with self.assertRaises(FantasyDataException):
            await get_leagues_entered(
                entry_data, self.player_cookie, self.config
            )

    async def test_multiple_leagues(self):
        """Test with multiple classic leagues.
        """
        mock_less_than_fifty_entries = Mock(return_value=futurized(True))
        patch(
            'process_entry_data.less_than_fifty_entries',
            mock_less_than_fifty_entries
        ).start()
        with open(
                'tests/unit/data/entry_response_multiple_classic_leagues.json'
        ) as json_file:
            entry_data = json.load(json_file)
        result = await get_leagues_entered(
            entry_data, self.player_cookie, self.config
        )
        mock_less_than_fifty_entries.assert_called()
        self.assertEqual(
            result, [
                {
                    "id": 1,
                    "name": "LEAGUE A",
                },
                {
                    "id": 2,
                    "name": "LEAGUE B",
                },
                {
                    "id": 3,
                    "name": "LEAGUE C",
                },
                {
                    "id": 4,
                    "name": "LEAGUE D",
                },
                {
                    "id": 5,
                    "name": "LEAGUE E",
                }
            ]
        )


class TestGetName(AsyncTestCase):
    """Async test class for testing get name.

    Args:
        obj: Async test class from the aiounittest library.
    """
    async def test_no_name(self):
        """Test with no name.
        """
        with open(
                'tests/unit/data/entry_response_no_name.json'
        ) as json_file:
            entry_data = json.load(json_file)
        result = await get_name(entry_data)
        self.assertEqual(result, None)

    async def test_name(self):
        """Test with name.
        """
        with open(
                'tests/unit/data/entry_response_multiple_classic_leagues.json'
        ) as json_file:
            entry_data = json.load(json_file)
        result = await get_name(entry_data)
        self.assertEqual(result, "TEAM A")
