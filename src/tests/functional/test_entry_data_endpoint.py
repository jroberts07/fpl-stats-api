from aioresponses import aioresponses
from server import app as sanic_app


async def test_success_multiple_classics(test_cli):
    """Test entry data with an array of classic leagues.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/'
                'entry_response_multiple_classic_leagues.json'
        ) as f:
            fpl_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=fpl_data
        )
        resp = await test_cli.get(
            '/entry_data/123?player_cookie=456'
        )
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {
            "name": "TEAM A",
            "leagues": [
                {
                    "id": 1,
                    "name": "LEAGUE A",
                },
                {
                    "id": 2,
                    "name": "LEAGUE B",
                },
                {
                    "id": 3,
                    "name": "LEAGUE C",
                },
                {
                    "id": 4,
                    "name": "LEAGUE D",
                },
                {
                    "id": 5,
                    "name": "LEAGUE E",
                }
            ]
        }


async def test_success_single_classics(test_cli):
    """Test entry data with a single classic league.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/'
                'entry_response_single_classic_league.json'
        ) as f:
            fpl_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=fpl_data
        )
        resp = await test_cli.get(
            '/entry_data/123?player_cookie=456'
        )
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {
            "name": "TEAM A",
            "leagues": [
                {
                    "id": 1,
                    "name": "LEAGUE A",
                }
            ]
        }


async def test_no_leagues(test_cli):
    """Test entry data with no leagues.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/entry_response_no_leagues.json'
        ) as f:
            fpl_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=fpl_data
        )
        resp = await test_cli.get(
            '/entry_data/123?player_cookie=456'
        )
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {
            "name": "TEAM A",
            "leagues": []
        }


async def test_no_name(test_cli):
    """Test entry data with no name.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/entry_response_no_name.json'
        ) as f:
            fpl_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=fpl_data
        )
        resp = await test_cli.get(
            '/entry_data/123?player_cookie=456'
        )
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {
            "name": None,
            "leagues": [
                {
                    "id": 1,
                    "name": "LEAGUE A",
                }
            ]
        }


async def test_no_player_cookie(test_cli):
    """Test entry data with no player_cookie.

    Args:
        test_cli (obj): The test event loop.
    """
    resp = await test_cli.get(
        '/entry_data/123?player_cookie='
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
            '/entry_data/123?player_cookie=456'
        )
        assert resp.status == 500
        resp_json = await resp.json()
        assert resp_json == {
            "error": "ERROR CONNECTING TO THE FANTASY API"
        }
