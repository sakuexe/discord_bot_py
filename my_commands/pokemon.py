from scripts.get_api import fetch_api
from random import randint


def get_random_pokemon() -> dict:
    pokemon = fetch_api(f'https://pokeapi.co/api/v2/pokemon/{randint(1, 151)}')
    return pokemon['name']


if __name__ == "__main__":
    print("main")
