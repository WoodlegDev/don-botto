from config import Settings
from logger import Log
import requests

class MeApi:

    def __init__(self, token):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
            }

        self.base_url = f"{Settings.kickbase_api_url}/v4/leagues/{Settings.league_id}"

    def load_context(self) -> dict:

        budget = self.my_budget()
        print(budget)

        return {
            "budget": {
                "amount": budget["b"],
                "amountAfterAssumption": budget["pbaa"] if "pbaa" in budget else budget["b"]
            }
        }

        pass

    def my_budget(self) -> dict | None:
        res = requests.get(self.base_url + "/me/budget", headers=self.headers)

        if res.status_code != 200:
            Log("error", f"on {self.base_url}/me/budget route")
        else:
            return res.json()
