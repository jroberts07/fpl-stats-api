import datetime
from utils.exceptions import LocalDataNotFoundException


async def get_local_static_data(db, field):
    """Checks the local database too see if we have stored up to date static
    FPL data and returns the field requested.

    Args:
        db (obj): The DB connection client from the sanic app.
        field (string): The field to be returned.

    Returns:
        obj: The locally stored league data.

    Raises:
        LocalDataNotFound: If local data isn't found

    """
    static_data = await db.static_data.find_one(
        {}, {'_id': 0, field: 1, 'time_updated': 1}
    )
    if (
            static_data and
            static_data['time_updated'] and
            static_data['time_updated'] > (
                datetime.datetime.now() - datetime.timedelta(days=1)
            )
    ):
        del static_data['time_updated']
        return static_data
    else:
        # Is returned when data isn't found or needs updating.
        raise LocalDataNotFoundException


async def put_local_static_data(db, static_data):
    """Stores static_data in the db.

    Args:
        db (obj): The DB connection client from the sanic app.
        static_data (obj): The static data to store locally.
    """
    static_data['time_updated'] = datetime.datetime.now()
    await db.static_data.replace_one(
        {}, static_data, upsert=True
    )


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
            league_data['end_time'] and
            league_data['end_time'] > datetime.datetime.now()
    ):
        return league_data
    else:
        # Is returned when data isn't found or needs updating.
        raise LocalDataNotFoundException


async def put_local_league_data(db, league_data):
    """Stores league_data in the db.
    Args:
        db (obj): The DB connection client from the sanic app.
        league_data (obj): The league data to store locally.
    """
    await db.league_data.replace_one(
        {'league_id': league_data['league_id']}, league_data, upsert=True
    )
