# Hanoi
# @File:   state.py
# @Time:   26/09/2021
# @Author: Gabriel O.

from dataclasses import dataclass
from typing import List

from pile import Pile


@dataclass
class State:
    piles: List[Pile]
    last_move: str = ""

    def __hash__(self):
        s = 0
        for pile in self.piles:
            s += pile.__hash__()
        return s

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __str__(self):
        st_str = ""
        piles_as_lists_of_strings = [str(pile).split("\n") for pile in self.piles]
        for line_number in range(len(piles_as_lists_of_strings[0])):
            st_str += "   ".join(
                [
                    piles_as_lists_of_strings[pile_number][line_number]
                    for pile_number in range(len(self.piles))
                ]
            )
            st_str += "\n"
        st_str += f"{self.last_move}   {self.__hash__()}"
        return st_str
