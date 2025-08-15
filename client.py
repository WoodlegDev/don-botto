from datetime import datetime
from zoneinfo import ZoneInfo
from api.activities import ActivitiesApi
from api.me import MeApi
from api.market import MarketApi

from api.auth import login
from api.players import PlayerApi
from api.team import TeamApi
import json

class KickbaseClient:

    token = ""
    market_api: MarketApi
    player_api: PlayerApi
    team_api: TeamApi
    me_api: MeApi
    activities_api: ActivitiesApi

    def __init__(self):
        self.token = login()
        self.market_api = MarketApi(self.token)
        self.player_api = PlayerApi(self.token)
        self.team_api = TeamApi(self.token)
        self.me_api = MeApi(self.token)
        self.activities_api = ActivitiesApi(self.token)

    def load_context(self):


        players = self.market_api.load_context()
        self._add_details_to_players(players, self.player_api, self.team_api)

        manager_context = self.me_api.load_context()
        activities = self.activities_api.load_context()

        day_context = get_day_context_tz()

        context_object = {
            "data_from_transfermarket": players,
            "league_activities": activities
        }

        context_object.update(manager_context)
        context_object.update(day_context)

        json_string = json.dumps(context_object)
        print(json_string)
        return json_string

        #me_api.update_lineup(["1844"]) Schrott. Kein Plan wie request body aussehen muss



    def _add_details_to_players(self, players, player_api: PlayerApi, team_api: TeamApi):
        for player in players:
            player_details = player_api.load_context(player["player_id"])
            team_details = team_api.load_context(player["team_id"])
            player.update(player_details)
            player.update(team_details)
        return players

def get_day_context_tz(tz_name: str = "Europe/Berlin") -> dict:
    """
    Liefert:
      - today_date: 'YYYY-MM-DD'
      - today_weekday: 'Monday'..'Sunday'
      - days_until_friday: 0..6 (0 wenn heute Freitag)
      - is_friday: bool
    """
    now = datetime.now(ZoneInfo(tz_name))
    weekday = now.weekday()  # Monday=0 ... Sunday=6
    friday = 4
    days_until_friday = (friday - weekday) % 7
    return {
        "today_date": now.strftime("%Y-%m-%d"),
        "today_weekday": now.strftime("%A"),
        "days_until_friday": days_until_friday,
        "is_friday": days_until_friday == 0,
    }
