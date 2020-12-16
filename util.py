import sys

import click
from collections import *
from collections.abc import *
from functools import *
from itertools import *
from parse import *
from copy import *
from math import *


def p(*a, **k):
    return print(*a, **k)


def read_file(input, delim="\n"):
    return [l.strip() for l in input.read().strip().split(delim)]


def count_paths(start, end, graph):
    @lru_cache(maxsize=None)
    def ways_recursive(start, end):
        c = 0
        if start == end:
            return 1
        for next_node in graph[start]:
            c += ways_recursive(next_node, end)
        return c

    return ways_recursive(start, end)


def get_paths(start, end, graph):
    @lru_cache(maxsize=None)
    def ways_recursive(start, end):
        if start == end:
            return [[end]]

        out = []
        for next_node in graph[start]:
            for way in ways_recursive(next_node, end):
                out.append([start] + way)
        return out

    return ways_recursive(start, end)


class graph_from_func:
    def __init__(self, f):
        self.f = f

    def __getitem__(self, k):
        return self.f(k)


def tree_find(start, target, tree):
    node = tree[start]
    if node["val"] == target:
        return True

    for child in node.get("next") or []:
        if tree_find(child, target, tree):
            return True


def deltas(l):
    out = []
    for i in range(1, len(l)):
        out.append(l[i] - l[i - 1])
    return out


class Grid:
    Throw = object()

    UDLR = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    DIAGS = [(-1, -1), (1, 1), (-1, 1), (1, -1)]

    def __init__(self, lines):
        self.lines = lines
        self.width = len(self.lines[0])
        self.height = len(self.lines)

    def get(self, x, y, default=Throw):
        if 0 <= x < self.width:
            if 0 <= y < self.height:
                return self.lines[y][x]
        if default is Grid.Throw:
            raise ValueError(f"Invalid position ({x}, {y})")
        else:
            return default

    def get_multi(self, xys, default=Throw):
        return [self.get(x, y, default) for (x, y) in xys]

    def set(self, x, y, val):
        self.lines[y][x] = val

    @staticmethod
    def neighbors(x, y, include_diags=False):
        deltas = Grid.UDLR
        if include_diags:
            deltas += Grid.DIAGS

        out = []
        for (dx, dy) in deltas:
            if 0 <= x + dx < self.width:
                if 0 <= y + dy < self.height:
                    out.append(x + dx, y + dy)
        return out

    def walk(self):
        # top to bottom, left to right
        for line in self.lines:
            for val in line:
                yield val

    def print(self, sep="", vsep="\n"):
        out = []
        for row in range(self.height):
            out.append(sep.join(self.lines[row]))
        print(vsep.join(out))

    def copy(self):
        return Grid(deepcopy(self.lines))

    def __eq__(self, other):
        return self.lines == other.lines


class Vector(list):
    def _broadcast(self, other):
        if isinstance(other, Iterable):
            return zip(self, other)
        else:
            return zip(self, [other] * len(self))

    def __add__(self, other):
        return [x.__add__(y) for (x, y) in self._broadcast(other)]

    def __sub__(self, other):
        return [x.__sub__(y) for (x, y) in self._broadcast(other)]

    def __mul__(self, other):
        return [x.__mul__(y) for (x, y) in self._broadcast(other)]

    def __truediv__(self, other):
        return [x.__truediv__(y) for (x, y) in self._broadcast(other)]

    def __floordiv__(self, other):
        return [x.__floordiv__(y) for (x, y) in self._broadcast(other)]


def softconv(val, converter, default=None):
    try:
        return converter(val)
    except ValueError:
        return default


def softint(s, default=None):
    return softconv(s, int, default)


def first(l, default=None):
    return next(iter(l), default)


def prod(l):
    return reduce(lambda x, y: x * y, l)


def running_sum(l):
    if not l:
        return l
    out = [l[0]]
    for x in l[1:]:
        out.append(out[-1] + x)
    return out


def lget(l, k, default=None):
    if 0 <= k < len(l):
        return l[k]
    else:
        return default
