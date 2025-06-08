import requests
import logging

logger = logging.getLogger(__name__)

ME_URL = "https://fantasy.premierleague.com/api/me/"
TEAM_URL_TEMPLATE = "https://fantasy.premierleague.com/api/entry/{entry_id}/event/{gw}/picks/"
BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"

class FPLClient:
    def __init__(self):
        logger.info("Initializing FPL client")
        self.session = requests.Session()
        self.entry_id = None
        self.player_map = self._get_player_id_map()
        logger.info("FPL client initialized successfully")

    def set_auth_cookie(self, cookie):
        logger.info("Setting authentication cookie")
        self.session.headers.update({
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0"
        })

        me_resp = self.session.get(ME_URL)
        if me_resp.status_code != 200:
            logger.error(f"Authentication failed with status code: {me_resp.status_code}")
            raise Exception("Failed to authenticate with provided cookie.")

        me_json = me_resp.json()
        player_info = me_json.get('player')

        if not player_info or 'entry' not in player_info:
            logger.error("No entry ID found in /api/me response")
            raise Exception("No entry ID found in /api/me response.")

        self.entry_id = player_info['entry']
        logger.info(f"Successfully authenticated with entry ID: {self.entry_id}")
        return self.entry_id

    def get_team_for_gameweek(self, gw):
        if not self.entry_id:
            logger.error("Attempted to get team without authentication")
            raise Exception("Must authenticate first.")

        logger.info(f"Fetching team data for gameweek {gw}")
        url = TEAM_URL_TEMPLATE.format(entry_id=self.entry_id, gw=gw)
        team_response = self.session.get(url)
        if team_response.status_code != 200:
            logger.error(f"Failed to fetch team data: Status code {team_response.status_code}")
            raise Exception("Failed to fetch team data")

        picks = team_response.json().get("picks", [])
        starting_11 = [p for p in picks if p['position'] <= 11]
        logger.info(f"Successfully retrieved {len(starting_11)} players for gameweek {gw}")

        return [
            {
                "id": p['element'],
                "name": self.player_map.get(p['element'], f"Player {p['element']}"),
                "is_captain": p['is_captain'],
                "is_vice_captain": p['is_vice_captain']
            }
            for p in starting_11
        ]

    def _get_player_id_map(self):
        logger.info("Fetching player ID map from bootstrap data")
        resp = requests.get(BOOTSTRAP_URL)
        if resp.status_code != 200:
            logger.error(f"Failed to fetch bootstrap data: Status code {resp.status_code}")
            raise Exception("Failed to fetch bootstrap data")
            
        data = resp.json()
        player_map = {p['id']: p['web_name'] for p in data['elements']}
        logger.info(f"Successfully created player map with {len(player_map)} players")
        return player_map