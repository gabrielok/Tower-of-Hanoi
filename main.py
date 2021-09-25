from copy import deepcopy
from dataclasses import dataclass
from typing import List


@dataclass
class Pile:
    pile: List[int]
    max_size: int
    name: str

    def __str__(self):
        pile_string_lines = [self.disk_to_str(disk) for disk in self.pile]
        for i in range(len(self.pile), self.max_size):
            pile_string_lines = ["|", *pile_string_lines]
        w = 7
        pile_string_lines = list(map(lambda x: x.center(w, " "), pile_string_lines))
        pile_string_lines.append("|".center(w, "_"))
        pile_string_lines.append(self.name.center(w))
        return "\n".join(pile_string_lines)

    def __hash__(self):
        m = str_to_int(self.name)
        for disk in self.pile:
            m *= (disk + 1)
        return m

    def disk_to_str(self, disk_size):
        w = 1
        middle = ["="] * (disk_size * w * 2 - 1)
        disk_str = f"<{''.join(middle)}>"
        return disk_str


@dataclass
class State:
    piles: List[Pile]
    move_str: str

    def h(self):
        return calc_h(self)

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
            st_str += "  ".join([piles_as_lists_of_strings[pile_number][line_number] for pile_number in range(len(self.piles))])
            st_str += "\n"
        if DEBUG:
            st_str += f"{self.move_str}   {self.h()}   {self.__hash__()}"
        return st_str


def str_to_int(string):
    s = 0
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lookup = {alphabet[i]: i for i in range(len(alphabet))}
    for letter in string:
        try:
            s += lookup[letter]
        except KeyError:
            pass
    return s


def calc_h(state):
    """
    Here the heuristics are defined:
    0. Start with 0
    1. Let fault mean a disk placed on top of another one which is
        not its direct successor, add 1 for each fault in all piles.
    2. Add 1.5 for each disk that is not on the target pile.
    3. Add 1 for each disk in the target pile that is not on its
        correct final place, as it would be when the game is over.
    """
    p1, p2, p3 = map(lambda x: x.pile, state.piles)
    n_disks = len(p1 + p2 + p3)
    h = 0

    for pile in (p1, p2, p3):
        h += faults(pile)

    h += 1.5 * len(p1 + p2)

    h += errors(p3, n_disks)
    return h


def faults(pile):
    f = 0
    for i in range(len(pile) - 1):
        if pile[i + 1] - pile[i] > 1:
            f += 1
    return f


def errors(pile, n_disks):
    # since piles are bound to objects, changing them changes the parent object
    # so we must make a copy first (not a reference)
    pile_copy = deepcopy(pile)
    pile_copy.reverse()
    e = 0
    for i in range(len(pile_copy)):
        if pile_copy[i] != n_disks:
            e += 1
        n_disks -= 1
    return e


def calc_possible_states(state):
    possible_states = []
    P1, P2, P3 = state.piles
    p1, p2, p3 = map(lambda x: x.pile, (P1, P2, P3))
    if len(p1) > 0:
        if can_move(P1, P2):
            P1_, P2_ = move_one(P1, P2)
            possible_states.append(State([P1_, P2_, P3], f"{P1_.name}->{P2_.name}"))
        if can_move(P1, P3):
            P1_, P3_ = move_one(P1, P3)
            possible_states.append(State([P1_, P2, P3_], f"{P1_.name}->{P3_.name}"))
    if len(p2) > 0:
        if can_move(P2, P1):
            P2_, P1_ = move_one(P2, P1)
            possible_states.append(State([P1_, P2_, P3], f"{P2_.name}->{P1_.name}"))
        if can_move(P2, P3):
            P2_, P3_ = move_one(P2, P3)
            possible_states.append(State([P1, P2_, P3_], f"{P2_.name}->{P3_.name}"))
    if len(p3) > 0:
        if can_move(P3, P1):
            P3_, P1_ = move_one(P3, P1)
            possible_states.append(State([P1_, P2, P3_], f"{P3_.name}->{P1_.name}"))
        if can_move(P3, P2):
            P3_, P2_ = move_one(P3, P2)
            possible_states.append(State([P1, P2_, P3_], f"{P3_.name}->{P2_.name}"))
    return possible_states


def can_move(pile1, pile2):
    """ From pile1 to pile2 """
    if len(pile1.pile) == 0:
        return False
    if len(pile2.pile) == 0:
        return True
    if pile1.pile[0] < pile2.pile[0]:
        return True


def move_one(pile1, pile2):
    """ From pile1 to pile2 """
    p1 = deepcopy(pile1)
    p2 = deepcopy(pile2)
    p2.pile = [p1.pile[0], *p2.pile]
    p1.pile = p1.pile[1:]
    return p1, p2


def move(state, visited_states):
    possible_states = calc_possible_states(state)
    best_h = 1e10
    new_state = None
    for st in possible_states:
        if st in visited_states:
            continue
        temp_h = st.h()
        if temp_h < best_h:
            new_state = st
            best_h = temp_h
    print("NEW STATE:")
    print(new_state)
    return new_state


def hanoi(n):
    start = Pile(pile=[i for i in range(1, n + 1)], name="start", max_size=n)
    aux, end = Pile(pile=[], name="aux", max_size=n), Pile(pile=[], name="end", max_size=n)
    state = State([start, aux, end], "")
    print("INITIAL STATE:")
    print(state)
    visited_states = [state]
    moves = []
    while calc_h(state) != 0:
        new_state = move(state, visited_states)
        visited_states.append(state)
        state = new_state
        moves.append(new_state.move_str)
    return moves


if __name__ == "__main__":
    DEBUG = False
    n = 3
    moves = hanoi(n)
    print(moves)
    print(f"Total moves: {len(moves)}")
    print(f"Minimum moves: {2 ** n - 1}")
