from discord import Client
from copy import deepcopy
from scripts.scores import UserScores


async def pretty_listing(scores: dict, client: Client) -> str:
    """
    Give a list of scores in string format
    ---
    @param scores: the scores to give to users
    @return a string of the scores given
    """
    if not scores:
        return 'No scores yet!'
    pretty_scores = ''
    # convert the user_ids to usernames
    usernames = [await client.fetch_user(user_id) for user_id in scores.keys()]
    # get the length of the longest username
    longest = max(len(user.name) for user in usernames)
    # add a bit of padding to the longest username
    longest += 2
    # add the scores to the string
    for user_id, score in scores.items():
        user = await client.fetch_user(user_id)
        if score == 1:
            pretty_scores += f'{user.name.ljust(longest)} {score} rock\n'
        else:
            pretty_scores += f'{user.name.ljust(longest)} {score} rocks\n'

    return pretty_scores


async def clean_scoreboard(scoreboard: UserScores, client: Client):
    """
    Clean the scoreboard of users who have left the server
    ---
    @param scores: the scores to clean
    @return the cleaned scores
    """
    scores = scoreboard.get_rocks()
    for user_id in deepcopy(scores).keys():
        try:
            await client.fetch_user(user_id)
        except:
            # if user with the id doesn't exist, remove them from the scoreboard
            del scores[user_id]
    # save the changes to the scoreboard
    scoreboard.save_rocks(scores)
