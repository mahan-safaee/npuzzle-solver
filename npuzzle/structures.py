import sys


class Puzzle:
    def __init__(self, N: int, arr: list[int], g: int = 0, check=False):
        self.N = N
        self.c = N * N - 1
        self.pos = arr
        self.g = g
        self.prev = "nada"
        if check and not self.is_solvable:
            match input(
                "Warning! input puzzle is not solvable!"
                "\nWant to swap first and last tiles to make the puzzle solvable? (y/n)"
            ).lower():
                case "y":
                    self.swap(0, self.c)
                case _:
                    sys.exit()

    def __getitem__(self, x):
        # total time:    O(1)
        return self.pos.__getitem__(x)

    def __setitem__(self, i, j):
        # total time:    O(1)
        return self.pos.__setitem__(i, j)

    def __iter__(self):
        return iter(self.pos)

    def __hash__(self) -> int:
        # total time:    O(n^2)
        return hash(tuple(self.pos))

    def __eq__(self, __o: object) -> bool:
        # total time:    O(n^2)
        return hash(self) == hash(__o)

    def __len__(self):
        # total time:    O(1)
        return self.N**2

    def __repr__(self) -> str:
        return f"Puzzle({self.pos}, g={self.g})"

    def copy(self):
        # total time:    O(n^2)
        return Puzzle(self.N, self.pos[:], self.g)

    def swap(self, i, j):
        # total time:    O(1)
        self.g += 1
        self[i], self[j] = self[j], self[i]
        return self

    @property
    def empty_pos(self):
        # total time:    O(n^2)
        return self.pos.index(0)

    @property
    def is_solvable(self):
        # total time:    O(n^2)
        N = self.N
        res = N
        for i, x in enumerate(self):  # O(n)
            for y in self[i:]:  # O(n)
                res += y and (x > y)
        if N % 2 == 0:
            res += self.empty_pos // N
        return bool(res % 2)

    def show(self, file=None):
        N = self.N
        for i in range(N):
            print(*self[i * N : (i + 1) * N], sep="\t", file=file)
        print(file=file)

    def setprev(self, prev):
        # total time:    O(1)
        self.prev = prev
        return self

    def get_adjacents(self, ind: int):
        """Returns the adjacent tiles index"""
        # total time:    O(1)
        N = self.N
        dic = {}
        if ind - N >= 0:
            dic["bottom"] = ind - N
        if ind + N <= self.c:
            dic["top"] = ind + N
        if (ind + 1) % N:
            dic["left"] = ind + 1
        if ind % N:
            dic["right"] = ind - 1
        return dic.items()

    def next_states(self):
        # total time:    O(n^2)
        k = self.empty_pos
        return [self.copy().swap(k, j).setprev(i) for i, j in self.get_adjacents(k)]
