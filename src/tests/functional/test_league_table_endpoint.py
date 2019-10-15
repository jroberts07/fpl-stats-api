from aioresponses import aioresponses
from server import app as sanic_app


async def test_success(test_cli):
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/'
                'league_response_multiple_entries.json'
        ) as f:
            league_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=123
            ),
            status=200,
            body=league_data
        )
        resp = await test_cli.get(
            '/league_table/123?player_cookie=456'
        )
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {
            "league_name": "League A",
            "standings": [
                {
                    "rank": 1,
                    "previous_rank": 1,
                    "entry_name": "Team A",
                    "player_name": "Player A",
                    "gameweek_points": 42,
                    "total_points": 453
                },
                {
                    "rank": 1,
                    "previous_rank": 1,
                    "entry_name": "Team B",
                    "player_name": "Player B",
                    "gameweek_points": 43,
                    "total_points": 453
                }
            ]
        }


async def test_bad_response(test_cli):
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/'
                'bad_response.json'
        ) as f:
            league_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=123
            ),
            status=200,
            body=league_data
        )
        resp = await test_cli.get(
            '/league_table/123?player_cookie=456'
        )
        assert resp.status == 500
        resp_json = await resp.json()
        assert resp_json == {
            "error": "THERE WAS A PROBLEM WITH THE DATA RETURNED FROM FPL"
        }


async def test_no_player_cookie(test_cli):
    """Test entry data with no player_cookie.

    Args:
        test_cli (obj): The test event loop.
    """
    resp = await test_cli.get(
        '/league_table/123?player_cookie='
    )
    assert resp.status == 400
    resp_json = await resp.json()
    assert resp_json == {
        "error": "PARAMETERS REQUIRED: player_cookie"
    }


async def test_fpl_error_response(test_cli):
    """Test entry data with an error response from FPL.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=500,
            body=None
        )
        resp = await test_cli.get(
            '/league_table/123?player_cookie=456'
        )
        assert resp.status == 500
        resp_json = await resp.json()
        assert resp_json == {
            "error": "ERROR CONNECTING TO THE FANTASY API"
        }
