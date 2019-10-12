import datetime
from utils.exceptions import LocalDataNotFound


async def get_local_league_data(db, league_id):
    """Checks the local database too see if we have stored up to date data
    for this league_id.

    Args:
        db (obj): The DB connection client from the sanic app.
        league_id (string): The league_id to search the DB for.

    Returns:
        obj: The locally stored league data.

    Raises:
        LocalDataNotFound: If local data isn't found

    """
    league_data = await db.league_data.find_one({'league_id': league_id})
    if (
            league_data and
            league_data['time_updated'] > (
                datetime.datetime.now() - datetime.timedelta(hours=1)
            )
    ):
        return league_data
    else:
        # Is returned when data isn't found or needs updating.
        raise LocalDataNotFound


async def put_local_league_data(db, league_data):
    """Checks the local database too see if we have stored up to date data
    for this league_id.

    Args:
        db (obj): The DB connection client from the sanic app.
        league_data (obj): The league data to store locally.
    """
    await db.league_data.replace_one(
        {'league_id': league_data['league_id']}, league_data, upsert=True
    )
