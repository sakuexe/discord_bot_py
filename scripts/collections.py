from discord import Client
from discord.flags import Intents
from typing import Dict
import json
from random import randint
from .get_api import fetch_api


class Raino(Client):
    """Custom client class for Raino bot"""
    # _rocks: int

    def __init__(self, *, intents: Intents, **options) -> None:
        # initialize the client with intents and options
        super().__init__(intents=intents, **options)
        # load data of states from a file
        data = read_from_json('raino_data.json')
        if len(data) == 0:
            self._rocks = 0
        else:
            self._rocks = data['rocks']

    @property
    def rocks(self):
        """Getter for property of rocks"""
        return self._rocks

    @rocks.setter
    def rocks(self, value: int):
        """Setter for property of rocks. Writes changes to file"""
        self._rocks = value
        write_to_json('raino_data.json', {'rocks': self._rocks})

    def fetch_random_rock(self) -> Dict[str, str]:
        """Fetch a random rock from the list of rocks"""
        # then fetch the random rock
        rock_data = fetch_api(f'https://rockapi.apiworks.tech/rock/random')
        return rock_data


def read_from_json(file_url: str) -> dict:
    try:
        with open(file_url, 'r') as file:
            data = file.read()
            return json.loads(data)
    except OSError:
        print(
            f"File not found or couldn't be opened. Creating new one at {file_url}")
        write_to_json(file_url)
        return {}


def write_to_json(file_url: str, write_data: dict = {}) -> None:
    with open(file_url, 'w') as file:
        file.write(json.dumps(write_data))


if __name__ == "__main__":
    test_raino = Raino(intents=Intents.default())
    print('initial rocks:', test_raino.rocks)
    print('adding 1 rock')
    test_raino.rocks += 1
    print('rocks:', test_raino.rocks)
    print('adding 2 rocks')
    test_raino.rocks += 2
    print('rocks:', test_raino.rocks)
