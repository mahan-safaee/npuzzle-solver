from pynput.keyboard import Key

try:
    from .npuzzle import Puzzle
except ImportError:
    from npuzzle import Puzzle

namedic = dict(up="bottom", down="top", left="right", right="left")


def on_release(puz: "Puzzle", key: Key):
    if not isinstance(key, Key):
        return
    if key in (Key.esc, Key.enter, Key):
        return False
    name: str = key.name
    for i in puz.next_states():
        if namedic.get(name) == i.prev:
            puz.pos = i.pos
            print()
            puz.show()
            return
