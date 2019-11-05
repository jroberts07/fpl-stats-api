from aiounittest import AsyncTestCase
import json


from static_data_handler import determine_current_gameweek
from utils.exceptions import FantasyDataException


class TestDetermineCurrentGameweek(AsyncTestCase):
    """Async test class for testing the function that determines  the current
    gameweek.

    Args:
        obj: Async test class from the aiounittest library.
    """

    async def test_active_gameweek(self):
        """Test with active gameweeks.
        """
        with open(
                'tests/unit/data/active_gameweeks.json'
        ) as json_file:
            gameweeks_data = json.load(json_file)
        result = await determine_current_gameweek(gameweeks_data)
        self.assertEqual(
            result,
            {
                "id": 2,
                "start_time": "2019-08-17T10:30:00Z",
                "end_time": "2019-08-23T18:00:00Z"
            }
        )

    async def test_last_active_gameweek(self):
        """Test with active gameweeks (last day of season).
        """
        with open(
                'tests/unit/data/last_active_gameweeks.json'
        ) as json_file:
            gameweeks_data = json.load(json_file)
        result = await determine_current_gameweek(gameweeks_data)
        self.assertEqual(
            result,
            {
                "id": 1,
                "start_time": "2019-08-09T18:00:00Z",
                "end_time": None
            }
        )

    async def test_no_active_gameweek(self):
        """Test with no active gameweeks.
        """
        with open(
                'tests/unit/data/no_active_gameweeks.json'
        ) as json_file:
            gameweeks_data = json.load(json_file)
        with self.assertRaises(FantasyDataException):
            await determine_current_gameweek(gameweeks_data)

    async def test_bad_data(self):
        """Test with no active gameweeks.
        """
        with open(
                'tests/unit/data/bad_data.json'
        ) as json_file:
            gameweeks_data = json.load(json_file)
        with self.assertRaises(FantasyDataException):
            await determine_current_gameweek(gameweeks_data)
