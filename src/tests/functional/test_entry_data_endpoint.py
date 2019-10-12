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
            entry_data = f.read()
        with open(
                'tests/functional/data/'
                'league_response_less_than_fifty.json'
        ) as f:
            league_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=entry_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=1
            ),
            status=200,
            body=league_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=2
            ),
            status=200,
            body=league_data
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
                }
            ]
        }


async def test_success_multiple_classics_some_more_than_fifty(test_cli):
    """Test entry data with an array of classic leagues some with more than
    fifty entries.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/'
                'entry_response_multiple_classic_leagues.json'
        ) as f:
            entry_data = f.read()
        with open(
                'tests/functional/data/'
                'league_response_less_than_fifty.json'
        ) as f:
            league_data_less_than_fifty = f.read()
        with open(
                'tests/functional/data/'
                'league_response_more_than_fifty.json'
        ) as f:
            league_data_more_than_fifty = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=entry_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=1
            ),
            status=200,
            body=league_data_less_than_fifty
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=2
            ),
            status=200,
            body=league_data_more_than_fifty
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


async def test_league_api_bad_response(test_cli):
    """Test entry data with a bad response from league API.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/'
                'entry_response_single_classic_league.json'
        ) as f:
            entry_data = f.read()
        with open(
                'tests/functional/data/'
                'bad_response.json'
        ) as f:
            league_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=entry_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=1
            ),
            status=200,
            body=league_data
        )
        resp = await test_cli.get(
            '/entry_data/123?player_cookie=456'
        )
        assert resp.status == 500
        resp_json = await resp.json()
        assert resp_json == {
            "error": "THERE WAS A PROBLEM WITH THE DATA RETURNED FROM FPL"
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
            entry_data = f.read()
        with open(
                'tests/functional/data/'
                'league_response_less_than_fifty.json'
        ) as f:
            league_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=entry_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=1
            ),
            status=200,
            body=league_data
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
            entry_data = f.read()
        with open(
                'tests/functional/data/'
                'league_response_less_than_fifty.json'
        ) as f:
            league_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.ENTRY_DATA.format(
                entry_id=123
            ),
            status=200,
            body=entry_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=1
            ),
            status=200,
            body=league_data
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
