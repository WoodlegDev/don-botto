from config import Settings
import requests

class PlayerApi:

    def __init__(self, token):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        self.base_url = f"{Settings.kickbase_api_url}/v4/leagues"

    def load_context(self, player_id: str):
        player_details = self.player(player_id)
        return {"player_details": player_details}

    def player(self, player_id):
        request_url = f"{self.base_url}/{Settings.league_id}/players/{player_id}"
        res = requests.get(request_url, headers=self.headers)
        return self._map_player_data(res.json())

    def _map_player_data(self, player_data):
        mapped_data = {
            "team_name": player_data["tn"],
            "status": "fit" if player_data["st"] == 0 else "not fit",
            "market_value_change_in_last_day": player_data["tfhmvt"]

        }
        return mapped_data
