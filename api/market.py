from logger import log
from config import Settings
import requests

class MarketApi:

    def __init__(self, token):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }

        self.base_url = f"{Settings.kickbase_api_url}/v4/leagues"

    def load_context(self):
        return self.players_on_transfer()


    def players_on_transfer(self):
        request_url = f"{self.base_url}/{Settings.league_id}/market"
        res = requests.get(request_url, headers=self.headers)
        return self._map_player_on_transfer_data(res.json())

    def _map_player_on_transfer_data(self, json_data):
        mapped_data = []
        for player in json_data["it"]:
            if "u" in player:
                #indicates transfer listing is from manager
                continue
            else:
                mapped_player = {
                    "player_id": player["i"],
                    "first_name": player["fn"],
                    "last_name": player["n"],
                    "team_id": player["tid"],
                    "position": Settings.player_position_dict[str(player["pos"])],
                    "market_value": player["mv"],
                    "points": player["p"] if "p" in player else 0,
                    "average_points": player["ap"] if "ap" in player else 0,
                    "market_value_trend": Settings.market_value_trend[str(player["mvt"])],
                    "price": player["prc"],
                    "remaining_seconds_on_market": player["exs"]
                }
                mapped_data.append(mapped_player)
        return mapped_data

    def place_an_offer(self, player_id, price):
        request_url = f"{self.base_url}/{Settings.league_id}/market/{player_id}/offers"
        request_body = {"price": price}
        requests.post(request_url, json=request_body, headers=self.headers)
        log("offer", f"Placed offer for player_id: {player_id} for {price}€")


    def accept_kickbase_offer(self, player_id):
        request_url = f"{self.base_url}/{Settings.league_id}/market/{player_id}/sell"
        params = {"playerId": player_id}
        requests.post(request_url, params=params, headers=self.headers)
        log("sell", f"Sold player_id: {player_id} to kickbase")
