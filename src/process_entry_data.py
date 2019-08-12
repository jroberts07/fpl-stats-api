async def get_leagues_entered(entry_data):
    """Takes raw entry data and extracts the league's id and name.

    Args:
        entry_data (obj): The raw entry data.

    Returns:
        array: An array of the ids and names of the leagues the player has
        entered.
    """
    leagues_entered = []
    if (
        entry_data['leagues']
        and 'classic' in entry_data['leagues']
        and entry_data['leagues']['classic']
    ):
        for league in entry_data['leagues']['classic']:
            leagues_entered.append(
                {
                    'id': league['id'],
                    'name': league['name']
                }
            )
    return leagues_entered


async def get_name(entry_data):
    """Takes raw entry data and extracts the player name.

    Args:
        entry_data (obj): The raw entry data.

    Returns:
        string: The player name.
    """
    if 'name' in entry_data:
        return entry_data['name']
    else:
        return None
