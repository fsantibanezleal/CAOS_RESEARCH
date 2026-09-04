"""A small CNF builder with named variables, exactly-one, and sequential-counter cardinality."""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path


class CNF:
    def __init__(self) -> None:
        self.nvars = 0
        self.names: dict[str, int] = {}
        self.clauses: list[tuple[int, ...]] = []

    def var(self, name: str) -> int:
        v = self.names.get(name)
        if v is None:
            self.nvars += 1
            v = self.nvars
            self.names[name] = v
        return v

    def fresh(self) -> int:
        self.nvars += 1
        return self.nvars

    def add(self, *lits: int) -> None:
        if not lits:
            raise ValueError("empty clause")
        if len(set(lits)) != len(lits) or any(-x in lits for x in lits):
            raise ValueError(f"degenerate clause {lits}")
        self.clauses.append(tuple(lits))

    def exactly_one(self, lits: list[int]) -> None:
        self.add(*lits)
        for a, b in itertools.combinations(lits, 2):
            self.add(-a, -b)

    def at_least_two(self, lits: list[int]) -> None:
        for i in range(len(lits)):
            self.add(*[x for j, x in enumerate(lits) if j != i])

    def at_most_two(self, lits: list[int]) -> None:
        for a, b, c in itertools.combinations(lits, 3):
            self.add(-a, -b, -c)

    def at_most_k(self, lits: list[int], k: int) -> None:
        """Sinz sequential counter: sum(lits) <= k."""
        n = len(lits)
        if k >= n:
            return
        if k == 0:
            for x in lits:
                self.add(-x)
            return
        s = [[self.fresh() for _ in range(k)] for _ in range(n)]
        self.add(-lits[0], s[0][0])
        for j in range(1, k):
            self.add(-s[0][j])
        for i in range(1, n):
            self.add(-lits[i], s[i][0])
            self.add(-s[i - 1][0], s[i][0])
            for j in range(1, k):
                self.add(-lits[i], -s[i - 1][j - 1], s[i][j])
                self.add(-s[i - 1][j], s[i][j])
            self.add(-lits[i], -s[i - 1][k - 1])

    def dimacs(self, comments: list[str] | None = None) -> str:
        out = [f"c {c}" for c in (comments or [])]
        out.append(f"p cnf {self.nvars} {len(self.clauses)}")
        out.extend(" ".join(map(str, cl)) + " 0" for cl in self.clauses)
        return "\n".join(out) + "\n"

    def write(self, path: Path, comments: list[str] | None = None) -> str:
        data = self.dimacs(comments).encode("ascii")
        Path(path).write_bytes(data)
        return hashlib.sha256(data).hexdigest()
