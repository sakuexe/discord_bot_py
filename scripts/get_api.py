from urllib.request import urlopen, Request
import json
from time import time


def fetch_api(url: str) -> dict:
    """Fetch data from a given API and return it"""
    user_agent = f'mediamokki-bot-{time()}'
    req = Request(url, headers={'User-Agent': user_agent})
    with urlopen(req) as response:
        data = response.read().decode('utf-8')
        return json.loads(data)


if __name__ == "__main__":
    pokemon = fetch_api('https://pokeapi.co/api/v2/pokemon/ditto')
    print(pokemon['name'])
