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

    def possible_states(self):
        possible_states = []
        for pile_from in self.piles:
            for pile_to in self.piles:
                if pile_to == pile_from:
                    continue
                new_piles = self.piles.copy()
                if can_move(pile_from, pile_to):
                    new_pile_from, new_pile_to = move_one(pile_from, pile_to)
                    new_piles[self.piles.index(pile_from)] = new_pile_from
                    new_piles[self.piles.index(pile_to)] = new_pile_to
                    new_state = State(
                        piles=new_piles,
                        last_move=f"{new_pile_from.name}->{new_pile_to.name}",
                    )
                    possible_states.append(new_state)
        return possible_states

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


def can_move(pile1, pile2):
    """ From pile1 to pile2 """
    if len(pile1) == 0:
        return False
    if len(pile2) == 0:
        return True
    if pile1[0] < pile2[0]:
        return True


def move_one(pile1, pile2):
    """ From pile1 to pile2 """
    p2 = Pile(_pile=[pile1[0], *pile2[:]], name=pile2.name, max_size=pile2.max_size)
    p1 = Pile(_pile=pile1[1:], name=pile1.name, max_size=pile1.max_size)
    return p1, p2
