from dataclasses import dataclass
from .jsonutils import read_from_json, write_to_json
from typing import Tuple, Optional, Union


@dataclass
class UserScores():
    """Class to store user scores"""
    _rock_scores: dict

    def __init__(self) -> None:
        """Initialize the class"""
        data = read_from_json('scores.json')
        if 'rocks' not in data:
            data['rocks'] = {}
        self._rock_scores = data['rocks']

    def save_rocks(self, rock_scores: dict) -> None:
        """Setter for property of rocks"""
        write_to_json('scores.json', {'rocks': rock_scores})

    def get_rocks(self, user_id: Optional[str] = None) -> dict:
        """
        Getter for property of rocks
        ---
        @param user_id: the ID of the user to get the score of
        @return the score of the user with the given ID (int) 
        or all scores (dict) if no ID is given
        """
        if not user_id:
            return self._rock_scores
        try:
            return self._rock_scores[user_id]
        except KeyError as error:
            print(error)
            return {user_id: 0}

    def give_rocks(self, user_id: str, amount: int) -> None:
        """
        Setter for property of rocks. Writes changes to file
        ---
        @param user_id: the ID of the user to add rocks to
        @param amount: a tuple of the user ID and the number of rocks to add
        """
        # if user already has a score, add to it
        if user_id in self._rock_scores:
            self._rock_scores[user_id] += amount
        else:
            # otherwise, set the score to the amount given
            self._rock_scores[user_id] = amount
        # write the changes to the file
        self.save_rocks(self._rock_scores)
