"main file"
import sys
from typing import Callable
from datetime import datetime
import contextlib
from pathlib import Path
from functools import partial
from pynput.keyboard import Listener


try:
    from .npuzzle import Puzzle, algorithms  # pylint: disable=import-error
except ImportError:
    from npuzzle import Puzzle, algorithms
try:
    from .poschanger import on_release
except ImportError:
    from poschanger import on_release


def get_int(prompt: str = "") -> int:
    inp = ""
    while not inp:
        inp: str = "".join(filter(str.isdecimal, input(prompt)))
    return int(inp)


encdic = dict(encoding="utf8")
inputfile = Path(__file__).with_name("input.txt")
with inputfile.open(**encdic) as fp:
    N, *pos = list(map(int, fp.read().replace(*"\n ").split()))
ReadPuzzle = Puzzle(N, pos, check=1)
print("this is input:")
ReadPuzzle.show()
print("wanna change it? press arrow keys and then `ESC` or `ENTER`")
with Listener(on_release=partial(on_release, ReadPuzzle)) as lis:
    lis.join()
with inputfile.open("w", **encdic) as fp:
    print(N, file=fp)
    ReadPuzzle.show(fp)

s: tuple[str] = (
    "",
    "1:\tA* (manhattan)",
    "2:\tA* (hamming)",
    "3:\tBFS (UCS)",
    "4:\tDLS (DFS)",
    "5:\tIDS",
    "6:\texit",
    "",
)
alg: Callable[["Puzzle"], list["Puzzle"]]
while True:
    alg = algorithms.AStar
    print(*s, sep="\n")
    with contextlib.suppress(ValueError):
        match get_int():
            case 1:
                algorithms.Distance.default = "manhattan"
            case 2:
                algorithms.Distance.default = "hamming"
            case 3:
                alg = algorithms.BFS
            case 4:
                L = get_int("enter L for depth (0 to get DFS):")
                kw: dict = {} if L == 0 else dict(L=L)
                alg = partial(algorithms.DFS, **kw)
            case 5:
                alg = algorithms.IDS
            case 6:
                sys.exit(0)
            case _:
                continue
        break
print("starting timer")
t = datetime.now()
steps = alg(ReadPuzzle)
t = datetime.now() - t
tt = f"{t.total_seconds():.5f}"
print(len(steps))
now = ReadPuzzle
with inputfile.with_stem("output").open("w", **encdic) as fp:
    for i, step in enumerate(steps, 1):
        print(i, "-", sep=" ", end="\t")
        print(now[step.empty_pos], "to the", step.prev)
        step.show(fp)
        now = step
print("finished in", tt, "seconds")
