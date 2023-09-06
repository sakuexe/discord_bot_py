from dotenv import load_dotenv
from os import getenv
import sys
from typing import Tuple

def get_init_values() -> Tuple[str, str]:
    load_dotenv()
    SECRET_TOKEN: str = getenv("TOKEN") or ""
    GUILD_ID: str = getenv("GUILD") or ""

    # checks if the dev flag is passed
    if len(sys.argv) > 1 and sys.argv[1] == "--dev":
        SECRET_TOKEN: str = getenv("DEV_TOKEN") or ""
        GUILD_ID: str = getenv("DEV_GUILD") or ""

    return SECRET_TOKEN, GUILD_ID

if __name__ == "__main__":
    values = get_init_values()
    print(values)
