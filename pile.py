# Hanoi
# @File:   pile.py
# @Time:   26/09/2021
# @Author: Gabriel O.

from dataclasses import dataclass, field
from typing import List


@dataclass
class Pile:
    max_size: int
    name: str
    _pile: List[int] = field(default_factory=list)
    disk_width: int = 1

    def __str__(self):
        pile_string_lines = [self.disk_to_str(disk) for disk in self._pile]
        largest_disk = (self.max_size - 1) * 2 * self.disk_width + 3
        for i in range(len(self._pile), self.max_size):
            pile_string_lines = ["|", *pile_string_lines]
        pile_string_lines = list(
            map(lambda x: x.center(largest_disk, " "), pile_string_lines)
        )
        pile_string_lines.append("|".center(largest_disk, "_"))
        pile_string_lines.append(self.name.center(largest_disk))
        return "\n".join(pile_string_lines)

    def __hash__(self):
        m = str_to_int(self.name)
        for disk in self._pile:
            m *= disk + 1
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
        middle[len(middle) // 2] = str(disk_size)
        disk_str = f"<{''.join(middle)}>"
        return disk_str


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
