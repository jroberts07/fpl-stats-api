from aiounittest import futurized, AsyncTestCase
import datetime
from unittest.mock import Mock, patch

from server import app
from team_picks_handler import get_entry_picks


class TestGetEntryPicks(AsyncTestCase):
    """Async test class for testing the function that add entry picks to the league
    data.

    Args:
        obj: Async test class from the aiounittest library.
    """
    player_cookie = 'TEST'
    gameweek = 1

    async def test_update_picks(self):
        """Test picks are updated.
        """
        picks_updated = datetime.datetime.now() - datetime.timedelta(minutes=5)
        start_time = datetime.datetime.now()
        league_data = {
            "picks_updated": picks_updated,
            "start_time": start_time,
            "standings": [
                {
                    "entry_id": 1
                },
                {
                    "entry_id": 2
                },
            ]
        }
        mock_get_remote_picks_data = Mock(return_value=futurized({
            "picks": "TEST PICK"
        }))
        patch(
            'team_picks_handler.get_remote_picks_data',
            mock_get_remote_picks_data
        ).start()
        mock_put_local_league_data = Mock(return_value=futurized(None))
        patch(
            'team_picks_handler.put_local_league_data',
            mock_put_local_league_data
        ).start()
        result = await get_entry_picks(
            self.player_cookie, app, league_data, self.gameweek
        )
        mock_get_remote_picks_data.assert_called()
        mock_put_local_league_data.assert_called()
        self.assertEqual(
            result["standings"],
            [
                {
                    "entry_id": 1,
                    "picks": "TEST PICK"
                },
                {
                    "entry_id": 2,
                    "picks": "TEST PICK"
                },
            ]
        )

    async def test_update_picks_no_picks_date(self):
        """Test update if no pick update time.
        """
        start_time = datetime.datetime.now()
        league_data = {
            "start_time": start_time,
            "standings": [
                {
                    "entry_id": 1
                },
                {
                    "entry_id": 2
                },
            ]
        }
        mock_get_remote_picks_data = Mock(return_value=futurized({
            "picks": "TEST PICK"
        }))
        patch(
            'team_picks_handler.get_remote_picks_data',
            mock_get_remote_picks_data
        ).start()
        mock_put_local_league_data = Mock(return_value=futurized(None))
        patch(
            'team_picks_handler.put_local_league_data',
            mock_put_local_league_data
        ).start()
        result = await get_entry_picks(
            self.player_cookie, app, league_data, self.gameweek
        )
        mock_get_remote_picks_data.assert_called()
        mock_put_local_league_data.assert_called()
        self.assertEqual(
            result["standings"],
            [
                {
                    "entry_id": 1,
                    "picks": "TEST PICK"
                },
                {
                    "entry_id": 2,
                    "picks": "TEST PICK"
                },
            ]
        )

    async def test__update_picks_if_one_hour_since_last_update(self):
        """Test remote update if picks over one hour old.
        """
        picks_updated = datetime.datetime.now() - datetime.timedelta(hours=2)
        start_time = datetime.datetime.now() - datetime.timedelta(hours=3)
        mock_get_remote_picks_data = Mock(return_value=futurized({
            "picks": "TEST PICK"
        }))
        patch(
            'team_picks_handler.get_remote_picks_data',
            mock_get_remote_picks_data
        ).start()
        mock_put_local_league_data = Mock(return_value=futurized(None))
        patch(
            'team_picks_handler.put_local_league_data',
            mock_put_local_league_data
        ).start()
        league_data = {
            "picks_updated": picks_updated,
            "start_time": start_time,
            "standings": [
                {
                    "entry_id": 1
                },
                {
                    "entry_id": 2
                },
            ]
        }
        result = await get_entry_picks(
            self.player_cookie, app, league_data, self.gameweek
        )
        mock_get_remote_picks_data.assert_called()
        mock_put_local_league_data.assert_called()
        self.assertEqual(
            result["standings"],
            [
                {
                    "entry_id": 1,
                    "picks": "TEST PICK"
                },
                {
                    "entry_id": 2,
                    "picks": "TEST PICK"
                },
            ]
        )

    async def test_no_update_picks_less_than_5_minutes_since_update(self):
        """Test no remotes update if last update less than 5 mins ago.
        """
        picks_updated = datetime.datetime.now() - datetime.timedelta(minutes=2)
        start_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
        league_data = {
            "picks_updated": picks_updated,
            "start_time": start_time,
            "standings": [
                {
                    "entry_id": 1
                },
                {
                    "entry_id": 2
                },
            ]
        }
        result = await get_entry_picks(
            self.player_cookie, app, league_data, self.gameweek
        )
        self.assertEqual(
            result["standings"],
            [
                {
                    "entry_id": 1
                },
                {
                    "entry_id": 2
                },
            ]
        )
