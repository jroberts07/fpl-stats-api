MONGODB_USERNAME = "fantasy"
MONGODB_PASSWORD = "password"
MONGODB_HOST = "stats-database"
MONGODB_URI = 'mongodb://{}:{}@{}'.format(
    MONGODB_USERNAME,
    MONGODB_PASSWORD,
    MONGODB_HOST
)

USER_AGENT_HEADER = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142'
                  ' Mobile Safari/537.36'
}
LOGIN_COOKIE_HEADER = {
    'Cookie': 'pl_profile="{player_id}"'
}

FPL_URL = "https://fantasy.premierleague.com/"
ENTRY_DATA = 'api/entry/{entry_id}/'

LOG_LEVEL = 'DEBUG'
