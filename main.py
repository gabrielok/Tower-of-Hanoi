# Hanoi
# @File:   main.py
# @Time:   25/09/2021
# @Author: Gabriel O.

from pile import Pile
from state import State

def calc_h(state):
    """
    Here the heuristics are defined:
    0. Start with 0
    1. Let fault mean a disk placed on top of another one which is
        not its direct successor, add 'a' for each fault in all piles.
    2. Add 'b' for each disk that is not on the target pile.
    3. Add 'c' for each disk in the target pile that is not on its
        correct final place, as it would be when the game is over.
    """
    p1, p2, p3 = state.piles
    n = len(p1) + len(p2) + len(p3)
    h = 0

    for pile in (p1, p2, p3):
        h += a * count_faults(pile)

    h += b * (len(p1) + len(p2))

    h += c * count_errors(p3, n)
    return h


def count_faults(pile):
    fault_count = 0
    for i in range(len(pile) - 1):
        if pile[i + 1] - pile[i] > 1:
            fault_count += 1
    return fault_count


def count_errors(pile: Pile, n):
    pile_reversed = pile.reversed()
    error_count = 0
    for i in range(len(pile_reversed)):
        if pile_reversed[i] != n:
            error_count += 1
        n -= 1
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
                new_state = State(
                    piles=new_piles,
                    last_move=f"{new_pile_from.name}->{new_pile_to.name}",
                )
                possible_states.append(new_state)
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


def move(current_state, visited_states):
    possible_states = calc_possible_states(current_state)
    best_h = 1e10
    new_state = None
    for state in possible_states:
        if state in visited_states:
            continue
        temp_h = calc_h(state)
        if temp_h < best_h:
            new_state = state
            best_h = temp_h
    if DISPLAY:
        print("NEW STATE:")
        print(new_state)
    return new_state


def hanoi(n):
    start = Pile(_pile=[i for i in range(1, n + 1)], name="start", max_size=n)
    aux, end = Pile(name="aux", max_size=n), Pile(name="end", max_size=n)
    state = State(piles=[start, aux, end])
    if DISPLAY:
        print("INITIAL STATE:")
        print(state)
    visited_states = [state]
    moves = []
    while calc_h(state) != 0:
        new_state = move(state, visited_states)
        visited_states.append(state)
        state = new_state
        moves.append(new_state.last_move)
    return moves


if __name__ == "__main__":
    DEBUG = False
    DISPLAY = False
    errors = []
    combinations = [
        # (1, 1, 1),
        # (2, 1, 1),
        # (2, 2, 1),
        # (2, 1, 2),
        # (1, 2, 1),
        # (1, 2, 2),
        # (1, 1, 2),
        # (0.5, 1, 2),
        # (0.5, 2, 1),
        # (1, 0.5, 2),
        # (2, 0.5, 1),
        # (1, 2, 0.5),
        # (2, 1, 0.5),
        # (1, 2, 3),
        # (1, 3, 2),
        # (2, 1, 3),
        # (2, 3, 1),
        # (3, 1, 2),
        # (3, 2, 2),
        # (3, 2, 1.5),
        # (3, 2, 0),
        (3, 2, 1),
    ]
    for a, b, c in combinations:
        failures = 0
        first_n, last_n = 3, 10
        for n_disks in range(first_n, last_n + 1):
            try:
                if DEBUG:
                    print(f"==== {n_disks} DISKS ====")
                output = hanoi(n_disks)
            except AttributeError:
                if DEBUG:
                    print(f"Failed with {n_disks} disks")
                failures += 1
                continue
            expected_moves = 2 ** n_disks - 1
            err = (len(output) - expected_moves) / expected_moves
            errors.append(err)
            if DISPLAY:
                print(output)
            if DEBUG:
                print(f"Total moves: {len(output)}")
                print(f"Minimum moves: {2 ** n_disks - 1} (2^n - 1)")
                print(f"Error rate: {err * 100:.2f}%")
        print()
        print(f"Parameters: a = {a}, b = {b}, c = {c}")
        print(f"Average error: {sum(errors) / len(errors) * 100:.2f}%")
        print(f"Failure rate: {failures / (last_n - first_n + 1) * 100:.2f}%")
