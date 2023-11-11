from queue import PriorityQueue, LifoQueue, Queue
from itertools import count
from functools import partial

if 0 + 0:
    from .structures import Puzzle


def B_or_D_FS(cls: Queue | LifoQueue, puz: "Puzzle", L: int = None) -> list["Puzzle"]:
    """
    BFS and DFS are the same but with different data structures
    DLS and DFS are the same but DFS has L = inf

    BFS = partial(B_or_D_FS, Queue)
    DFS = partial(B_or_D_FS, LifoQueue)
    """
    if L is None:
        L = float("inf")
    q = cls(-1)
    q.put((puz, None))
    parent_of = {}
    while q.qsize():
        node: "Puzzle"
        parent: "Puzzle"
        node, parent = q.get()
        if node.g > L:
            continue
        if Distance.is_goal(node):
            steps = [node]
            while parent:
                steps.append(parent)
                parent = parent_of[parent]
            steps.reverse()
            steps.pop(0)
            return steps
        if node not in parent_of:
            parent_of[node] = parent
        for ns in node.next_states():
            q.put((ns, node))
    return []


BFS = partial(B_or_D_FS, Queue)
DFS = partial(B_or_D_FS, LifoQueue)


def IDS(puz: "Puzzle") -> list["Puzzle"]:
    for L in count(1):  # from 1 to inf
        if result := DFS(puz, L):  # * DLS
            return result


def AStar(puz: "Puzzle") -> list["Puzzle"]:
    c = count()
    pq = PriorityQueue(-1)
    # * priority is f(n) first and then who entered first
    pq.put((0, next(c), puz, None))
    opened = {}
    closed = {}
    while pq.qsize():
        node: "Puzzle"
        parent: "Puzzle"
        *_, node, parent = pq.get()
        if node in closed:  #! don't reopen an closed node
            continue
        if Distance.is_goal(node):  # solved
            steps = [node]
            while parent:
                steps.append(parent)
                parent = closed[parent]
            steps.reverse()
            steps.pop(0)
            return steps
        closed[node] = parent
        for ns in node.next_states():
            if ns in closed:
                continue
            if ns in opened:
                move_g, move_h = opened[ns]
                if move_g <= node.g:
                    #! same child-node but in lower depth, so don't open it later
                    continue
            else:
                move_h = Distance.compute(ns)
            opened[ns] = node.g, move_h
            pq.put((move_h + node.g, next(c), ns, node))
    return []


class Distance:
    default = "hamming manhattan".split()[0]

    @staticmethod
    def hamming(x: "Puzzle"):
        dist = 0
        l = len(x)
        for a, b in enumerate(x, 1):
            dist += b and ((a % l) != b)
        return dist

    @staticmethod
    def manhattan(x: "Puzzle"):
        N = x.N
        dist = 0
        for i, a in enumerate(x):
            if a == 0:
                continue
            x1, y1 = divmod(a - 1, N)
            x2, y2 = divmod(i, N)
            dist += abs(x1 - x2) + abs(y1 - y2)
        return dist

    @classmethod
    def compute(cls, x: "Puzzle") -> int:
        return getattr(cls, cls.default)(x)

    @classmethod
    def is_goal(cls, x: "Puzzle") -> bool:
        return cls.compute(x) == 0
