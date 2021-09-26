from dataclasses import dataclass, field
from typing import List


@dataclass
class Pile:
    max_size: int
    name: str
    _pile: List[int] = field(default_factory=list)
    pile_width: int = 7
    disk_width: int = 1

    def __str__(self):
        pile_string_lines = [self.disk_to_str(disk) for disk in self._pile]
        for i in range(len(self._pile), self.max_size):
            pile_string_lines = ["|", *pile_string_lines]
        w = self.pile_width
        pile_string_lines = list(map(lambda x: x.center(w, " "), pile_string_lines))
        pile_string_lines.append("|".center(w, "_"))
        pile_string_lines.append(self.name.center(w))
        return "\n".join(pile_string_lines)

    def __hash__(self):
        m = str_to_int(self.name)
        for disk in self._pile:
            m *= (disk + 1)
        return m

    def __getitem__(self, item):
        return self._pile[item]

    def __len__(self):
        return len(self._pile)

    def reversed(self):
        _pile_copy = self._pile.copy()
        _pile_copy.reverse()
        return _pile_copy

    def disk_to_str(self, disk_size):
        middle = ["="] * (disk_size * self.disk_width * 2 - 1)
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
            st_str += "  ".join(
                [piles_as_lists_of_strings[pile_number][line_number] for pile_number in range(len(self.piles))])
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
    2. Add 1.5 for each disk that is not on the target _pile.
    3. Add 1 for each disk in the target _pile that is not on its
        correct final place, as it would be when the game is over.
    """
    p1, p2, p3 = state.piles
    n_disks = len(p1) + len(p2) + len(p3)
    h = 0

    for pile in (p1, p2, p3):
        h += faults(pile)

    h += 1.5 * (len(p1) + len(p2))

    h += errors(p3, n_disks)
    return h


def faults(pile):
    fault_count = 0
    for i in range(len(pile) - 1):
        if pile[i + 1] - pile[i] > 1:
            fault_count += 1
    return fault_count


def errors(pile: Pile, n_disks):
    pile_reversed = pile.reversed()
    error_count = 0
    for i in range(len(pile_reversed)):
        if pile_reversed[i] != n_disks:
            error_count += 1
        n_disks -= 1
    return error_count


def calc_possible_states(state):
    possible_states = []
    for pile_from in state.piles:
        for pile_to in state.piles:
            if pile_to == pile_from:
                continue
            new_piles = state.piles.copy()
            if can_move(pile_from, pile_to):
                new_pile_from, new_pile_to = move_one(pile_from, pile_to)
                new_piles[state.piles.index(pile_from)] = new_pile_from
                new_piles[state.piles.index(pile_to)] = new_pile_to
                possible_states.append(State(new_piles, f"{new_pile_from.name}->{new_pile_to.name}"))
    return possible_states


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
    start = Pile(_pile=[i for i in range(1, n + 1)], name="start", max_size=n)
    aux, end = Pile(name="aux", max_size=n), Pile(name="end", max_size=n)
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
    number_of_disks = 4
    output = hanoi(number_of_disks)
    print(output)
    print(f"Total moves: {len(output)}")
    print(f"Minimum moves: {2 ** number_of_disks - 1}")
