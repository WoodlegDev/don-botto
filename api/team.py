from config import Settings
import requests

class TeamApi:

    def __init__(self, token):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        self.base_url = f"{Settings.kickbase_api_url}/v4/leagues"

    def load_context(self, team_id: str):
       team_details = self.team_profile(team_id)
       return {"team_details": team_details}

    def team_profile(self, team_id):
        request_url = f"{self.base_url}/{Settings.league_id}/teams/{team_id}/teamprofile"
        res = requests.get(request_url, headers=self.headers)
        return self._map_team_data(res.json())

    def _map_team_data(self, team_data):
        mapped_data = {
            "team_name": team_data["tn"],
            "place_in_table": team_data["pl"],
            "team_value": team_data["tv"]
        }
        return mapped_data
