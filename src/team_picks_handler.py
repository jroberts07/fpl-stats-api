import asyncio
import datetime

from database_adapter import put_local_league_data
from fpl_adapter import get_remote_picks_data


async def get_entry_picks(player_cookie, app, league_data, gameweek):
    """Takes a league table and adds the entries picks for that gameweek.

    Args:
        app (obj): Then sanic app.
        player_cookie (str): Cookie used for FPL api.
        league_data (obj): The league table.
        gameweek (int): The current gameweek.

    Returns:
        obj: The league table with picks added.

    """
    # Update picks every 5 minutes for 1 hour after gameweek started.
    # Then every hour.
    if (
        "picks_updated" in league_data
        and league_data["picks_updated"] + datetime.timedelta(minutes=5)
        < datetime.datetime.now()
        < league_data["start_time"] + datetime.timedelta(hours=1)
        or "picks_updated" in league_data
        and league_data["picks_updated"] + datetime.timedelta(hours=1)
        < datetime.datetime.now()
        or "picks_updated" not in league_data
    ):
        league_data['standings'] = await asyncio.gather(
            *[
                add_picks_to_entry(entry, gameweek, player_cookie, app)
                for entry in league_data['standings']
            ]
        )
        league_data["picks_updated"] = datetime.datetime.now()
        # Save the update league data locally
        await put_local_league_data(app.db, league_data)
    return league_data


async def add_picks_to_entry(entry, gameweek, player_cookie, app):
    """Takes an entry and adds the picks for this gameweek and the time updates.
    Args:
        app (obj): Then sanic app.
        player_cookie (str): Cookie used for FPL api.
        entry (obj): The entry object.
        gameweek (int): The current gameweek.

    Returns:
        obj: The league table with picks added.

    """
    pick_data = await get_remote_picks_data(
            entry['entry_id'], gameweek, player_cookie, app
    )
    entry["picks"] = pick_data["picks"]
    return entry
