import unittest
import json

from calculate_table import calculate_points, calculate_table


class TestCalculatePoints(unittest.TestCase):
    """Async test class for testing the function that calculates an entries points

    Args:
        obj: Async test class from the aiounittest library.
    """

    def test_different_multipliers(self):
        """Test players with different multipliers.
        """
        with open(
                'tests/unit/data/live_data.json'
        ) as json_file:
            live_data = json.load(json_file)
        with open(
                'tests/unit/data/picks_with_different_multipliers.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = calculate_points(league_data, live_data)
        self.assertEqual(result["live_points"], 25)

    def test_player_with_negative_scores(self):
        """Test players with different multipliers.
        """
        with open(
                'tests/unit/data/live_data.json'
        ) as json_file:
            live_data = json.load(json_file)
        with open(
                'tests/unit/data/picks_with_negative_score.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = calculate_points(league_data, live_data)
        self.assertEqual(result["live_points"], -5)


class TestCalculateTable(unittest.TestCase):
    """Async test class for testing the function that calculates an entries points

    Args:
        obj: Async test class from the aiounittest library.
    """

    def test_different_multipliers(self):
        """Test players with different multipliers.
        """
        with open(
                'tests/unit/data/live_data.json'
        ) as json_file:
            live_data = json.load(json_file)
        with open(
                'tests/unit/data/league_table_two_teams.json'
        ) as json_file:
            league_data = json.load(json_file)
        result = calculate_table(league_data, live_data)
        self.assertEqual(
            result,
            {
                "standings": [
                    {
                        "entry_id": "2",
                        "live_points": 104,
                        "total_points": 99,
                        "confirmed_rank": 2,
                        "live_rank": 1,
                    },
                    {
                        "entry_id": "1",
                        "live_points": 95,
                        "total_points": 100,
                        "confirmed_rank": 1,
                        "live_rank": 2,
                    }
                ]
            }
        )
