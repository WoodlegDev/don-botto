import openai

from api.me import MeApi
from api.market import MarketApi

from api.auth import login

class OpenAIClient:

    token = ""

    def __init__(self):
        pass

    def trigger(self):
        self.token = login()
        print(self.token)

    def _load_context(self):
        market_api = MarketApi(self.token)
        market_api.load_context()

        me_api = MeApi(self.token)
        #me_api.load_context()
