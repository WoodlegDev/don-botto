from config import Settings
from client import OpenAIClient
from api.auth import login

def main():
    ai = OpenAIClient()
    ai.trigger()
    ai._load_context()


if __name__ == "__main__":
    main()
