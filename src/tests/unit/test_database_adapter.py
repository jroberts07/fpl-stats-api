from aiounittest import futurized, AsyncTestCase
import datetime
from unittest.mock import Mock, patch

from database_adapter import get_local_league_data
from utils.exceptions import LocalDataNotFound
from server import app


class TestDatabaseAdapter(AsyncTestCase):
    """Async test class for testing database adapter.

    Args:
        obj: Async test class from the aiounittest library.
    """
    async def test_local_league_data(self):
        """Test with no classic leagues.
        """
        with self.assertRaises(LocalDataNotFound):
            await get_local_league_data(app.db, 123)
