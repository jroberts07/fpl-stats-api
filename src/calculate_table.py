def calculate_table(league_data, live_data):
    """Calculates and sorts the live league table
    Args:
        league_data (obj): The league data.
        live_data (obj): The live data for the gameweek.
    Returns:
        obj: The league data sorted into live order.
    """
    for entry in league_data['standings']:
        calculate_points(entry, live_data)
    league_data["standings"] = sorted(
        league_data["standings"], key=lambda k: k['live_points'], reverse=True
    )
    for index, entry in enumerate(league_data['standings']):
        entry["live_rank"] = index + 1
        del entry["picks"]
    return league_data


def calculate_points(entry, live_data):
    """Calculates the live score for an entry
    Args:
        entry (obj): Entry data.
        live_data (obj): The live data for the gameweek.
    Returns:
        obj: Entry data with live score.
    """
    entry["live_points"] = entry["total_points"]
    for player in entry["picks"]:
        if player["multiplier"] > 0:
            entry["live_points"] += next(
                player_data["stats"]["total_points"]
                for player_data in live_data["elements"]
                if player_data["id"] == player["element"]
            ) * player["multiplier"]
    return entry
