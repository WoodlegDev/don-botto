from config import Settings
import requests
from logger import log

class ActivitiesApi:

    def __init__(self, token):
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        self.base_url = f"{Settings.kickbase_api_url}/v4/leagues"

    def load_context(self):
        return self.activities()

    def activities(self, max_items=20, start=0):
        request_url = f"{self.base_url}/{Settings.league_id}/activitiesFeed"
        params = {"max": max_items, "start": start}
        res = requests.get(request_url, headers=self.headers, params=params)
        return self._map_activities(res.json())

    def _map_activities(self, json_data):
        mapped = []
        for activity in json_data.get("af", []):
            type_id = str(activity["t"])
            type_name = Settings.activity_type_dict.get(type_id, "unknown")

            if type_name == "bonus_payment":
                continue

            base = {
                "activity_id": activity["i"],
                "type_id": type_id,
                "type_name": type_name,
                "context_code": activity["coc"],
                "datetime": activity["dt"]
            }

            data = activity.get("data", {})

            if type_name == "transfer_action":
                transaction_type_id = str(data.get("t")) if data.get("t") is not None else None
                transaction_type_name = Settings.transaction_type_dict.get(transaction_type_id, "unknown")
                base.update({
                    "buyer": data.get("byr"),
                    "seller": data.get("slr"),
                    "player_id": data.get("pi"),
                    "player_name": data.get("pn"),
                    "team_id": data.get("tid"),
                    "transaction_type": transaction_type_name,
                    "transfer_price": data.get("trp"),
                })

            else:
                base.update({"raw_data": data})

            mapped.append(base)

        return mapped

    def send_feed_item_comment(self, activity_id, comment):
        request_url = f"{self.base_url}/{Settings.league_id}/activitiesFeed/{activity_id}/comments"
        request_body = {"comm": comment}
        requests.post(request_url, json=request_body, headers=self.headers)
        log("comment", f"Made comment to activity: {activity_id} with comment: {comment}")
