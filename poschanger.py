"change puzzle on arrow-key press"
from random import shuffle
from pynput.keyboard import Key

try:
    from .npuzzle import Puzzle
except ImportError:
    from npuzzle import Puzzle

namedic = dict(up="bottom", down="top", left="right", right="left")


def on_release(puz: "Puzzle", key: Key):
    """handle key release"""
    if not isinstance(key, Key):
        return
    if key in (Key.esc, Key.enter):
        return False
    if key == Key.tab:
        shuffle(puz.pos)
        if not puz.is_solvable:
            puz.swap(0, puz.c)
        print()
        puz.show()
        return
    name: str = key.name
    for i in puz.next_states():
        if namedic.get(name) == i.prev:
            puz.pos = i.pos
            print()
            puz.show()
            return
