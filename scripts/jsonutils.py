import json
from os import remove


def read_from_json(file_url: str) -> dict:
    """
    read data from a JSON file in the given URL
    If the file doesn't exist, create a new one.
    ---
    @param file_url: the URL of the file to read from
    @return a dictionary of the data in the file
    """
    try:
        with open(file_url, 'r') as file:
            data = file.read()
            return json.loads(data)
    except OSError:
        print(
            f"File not found or couldn't be opened. Creating new one at {file_url}")
        write_to_json(file_url)
        return {}
    except ValueError:
        print(f'Error reading file {file_url}. Creating new one.')
        # remove old file, since it is either broken or empty
        remove(file_url)
        write_to_json(file_url)
        return {}


def write_to_json(file_url: str, write_data: dict = {}) -> None:
    """
    Write to a JSON file in the given URL
    ---
    @param file_url: the URL of the file to write to
    @param write_data: the data to write to the file
    """
    try:
        with open(file_url, 'w') as file:
            file.write(json.dumps(write_data))
    except OSError as error:
        print(f'Error writing to file: {error}')
