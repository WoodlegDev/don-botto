from config import Settings
from logger import log
import requests

class MeApi:

    def __init__(self, token):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }

        self.base_url = f"{Settings.kickbase_api_url}/v4/leagues"

    def load_context(self):
        budget = self.my_budget()
        players = self.my_players()
        lineup = self.my_lineup()
        manager_context = {
            "my_budget": budget,
            "my_players": players,
            "current_lineup": lineup
        }
        return manager_context

    def my_budget(self) -> dict | None:
        res = requests.get(f"{self.base_url}/{Settings.league_id}/me/budget", headers=self.headers)
        return self._map_budget_data(res.json())

    def _map_budget_data(self, budget_data):
        mapped_data = {
            "projected_budget_after_all_actions": budget_data["pbaa"] if "pbaa" in budget_data else budget_data["b"],
            "projected_budget_after_sales": budget_data["pbas"],
            "current_budget": budget_data["b"],
            "budget_status": "positive" if budget_data["bs"] == 1 else "negative"
        }
        return mapped_data

    def my_players(self):
        res = requests.get(f"{self.base_url}/{Settings.league_id}/squad", headers=self.headers)
        return self._map_my_players(res.json())

    def _map_my_players(self, players):
        mapped_data = []
        for player in players["it"]:
            mapped_player = {
                "player_id": player["i"],
                "last_name": player["n"],
                "position": Settings.player_position_dict[str(player["pos"])],
                "market_value": player["mv"],
                "points": player["p"] if "p" in player else 0,
                "average_points": player["ap"] if "ap" in player else 0,
                "is_in_team_of_the_month": player["iotm"],
                "market_value_trend": Settings.market_value_trend[str(player["mvt"])],
                "market_value_changed_in_last_week": player["sdmvt"],
                "market_value_changed_in_last_day": player["tfhmvt"]
            }
            mapped_data.append(mapped_player)
        return mapped_data

    def my_lineup(self):
        res = requests.get(f"{self.base_url}/{Settings.league_id}/lineup", headers=self.headers)
        return self._map_my_lineup(res.json())

    def _map_my_lineup(self, players):
        mapped_data = []
        for player in players["it"]:
            mapped_player = {
                "player_id": player["i"],
                "last_name": player["n"],
                "position": Settings.player_position_dict[str(player["pos"])],
                "average_points": player["ap"] if "ap" in player else 0,
                "status": "fit" if player["st"] == 0 else "not fit",
                "lineup_status": "in current lineup" if "lo" in player else "benched"
            }
            mapped_data.append(mapped_player)
        return mapped_data

    def update_lineup(self, player_list):
        request_url = f"{self.base_url}/{Settings.league_id}/lineup"
        request_body = {
            "type": None,
            "players": [{"i": "1844", "lo": 1}]}
        res = requests.post(request_url, json=request_body, headers=self.headers)
        print(res.status_code)
        log("update_lineup", f"Updated lineup with: {player_list}")
