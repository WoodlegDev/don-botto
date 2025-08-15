import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    open_ai_key = os.environ.get("OPEN_AI_KEY")
    league_id = os.environ.get("LEAGUE_ID")
    kickbase_api_url = "https://api.kickbase.com"
    player_position_dict = {
        "1": "Goalie",
        "2": "Defender",
        "3": "Midfielder",
        "4": "Attacker"
    }
    market_value_trend = {
        "0": "no change",
        "1": "increases",
        "2": "decreases"
    }
    activity_type_dict = {
            "3": "player_transfer_market",
            "15": "transfer_action",
            "22": "bonus_payment"
    }
    transaction_type_dict = {
            "1": "purchase",
            "2": "sale"
    }
