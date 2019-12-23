from aioresponses import aioresponses
import datetime
from server import app as sanic_app
import json


async def test_league_table_success(test_cli):
    """Test a sorted league table is returned.

    Args:
        test_cli (obj): The test event loop.
    """
    with aioresponses(passthrough=['http://127.0.0.1:']) as m:
        with open(
                'tests/functional/data/static.json'
        ) as f:
            static_data = json.loads(f.read())
            static_data["events"][0]["deadline_time"] = (
                datetime.datetime.strftime(
                    datetime.datetime.now(), "%Y-%m-%dT%H:%M:%SZ"
                )
            )
            static_data["events"][1]["deadline_time"] = (
                datetime.datetime.strftime(
                    datetime.datetime.now() + datetime.timedelta(weeks=1),
                    "%Y-%m-%dT%H:%M:%SZ"
                )
            )
            static_data = json.dumps(static_data)
        with open(
                'tests/functional/data/league.json'
        ) as f:
            league_data = f.read()
        with open(
                'tests/functional/data/team_a_picks.json'
        ) as f:
            team_a_picks_data = f.read()
        with open(
                'tests/functional/data/team_b_picks.json'
        ) as f:
            team_b_picks_data = f.read()
        with open(
                'tests/functional/data/live.json'
        ) as f:
            live_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.STATIC_DATA,
            status=200,
            body=static_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LEAGUE_DATA.format(
                league_id=1
            ),
            status=200,
            body=league_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.PICKS_DATA.format(
                entry_id=1, gameweek=1
            ),
            status=200,
            body=team_a_picks_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.PICKS_DATA.format(
                entry_id=2, gameweek=1
            ),
            status=200,
            body=team_b_picks_data
        )
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LIVE_DATA.format(
                gameweek=1
            ),
            status=200,
            body=live_data
        )
        resp = await test_cli.get(
            '/league_table/1?player_cookie=456'
        )
        assert resp.status == 200
        resp_json = await resp.json()
        assert resp_json == {
            "league_id": "1",
            "league_name": "League A",
            "standings": [
                {
                    "entry_id": "2",
                    "player_name": "Player B",
                    "entry_name": "Team B",
                    "live_points": 110,
                    "total_points": 90,
                    "confirmed_rank": 2,
                    "live_rank": 1
                },
                {
                    "entry_id": "1",
                    "player_name": "Player A",
                    "entry_name": "Team A",
                    "live_points": 100,
                    "total_points": 100,
                    "confirmed_rank": 1,
                    "live_rank": 2
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
                'bad_response.json'
        ) as f:
            live_data = f.read()
        m.get(
            sanic_app.config.FPL_URL + sanic_app.config.LIVE_DATA.format(
                gameweek=1
            ),
            status=500,
            body=live_data
        )
        resp = await test_cli.get(
            '/league_table/1?player_cookie=456'
        )
        assert resp.status == 500
        resp_json = await resp.json()
        assert resp_json == {
            "error": "ERROR CONNECTING TO THE FANTASY API"
        }
