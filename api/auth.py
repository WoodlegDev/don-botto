from config import Settings
import requests

def login ():

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    data = {
        "em": Settings.username,
        "pass": Settings.password
    }

    res = requests.post(Settings.kickbase_api_url + "/v4/user/login", json=data, headers=headers)

    return res.json()["tkn"]
