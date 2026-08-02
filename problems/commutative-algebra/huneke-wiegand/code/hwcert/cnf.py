"""Direct DIMACS encoding of the finite Huneke-Wiegand rigidity problem."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


Literal = int | bool


@dataclass
class CNF:
    names: dict[str, int] = field(default_factory=dict)
    clauses: list[tuple[int, ...]] = field(default_factory=list)

    def variable(self, name: str) -> int:
        if name not in self.names:
            self.names[name] = len(self.names) + 1
        return self.names[name]

    def add(self, *literals: Literal) -> None:
        if any(literal is True for literal in literals):
            return
        integers = [literal for literal in literals if literal is not False]
        unique = tuple(dict.fromkeys(int(integer) for integer in integers))
        if any(-literal in unique for literal in unique):
            return
        self.clauses.append(unique)

    def equivalent_and(self, output: int, inputs: list[Literal]) -> None:
        if any(value is False for value in inputs):
            self.add(-output)
            return
        active = [int(value) for value in inputs if value is not True]
        if not active:
            self.add(output)
            return
        for value in active:
            self.add(-output, value)
        self.add(output, *(-value for value in active))

    def write(self, path: Path, comments: list[str] | None = None) -> None:
        lines = [f"c {comment}" for comment in comments or []]
        lines.append(f"p cnf {len(self.names)} {len(self.clauses)}")
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text("\n".join(lines) + "\n", encoding="ascii")
        temporary.replace(path)


def build_rigidity_cnf(frobenius: int, shift: int) -> tuple[CNF, tuple[int, ...]]:
    """Build the complete fixed-(F,s) CNF without a solver library."""
    if frobenius <= 0 or frobenius % 2 == 0:
        raise ValueError("F must be positive and odd")
    if not 1 <= shift <= frobenius:
        raise ValueError("shift must lie in [1,F]")
    cnf = CNF()
    h = tuple(cnf.variable(f"h:{value}") for value in range(frobenius + 1))

    def h_literal(value: int) -> Literal:
        if value < 0:
            return False
        if value > frobenius:
            return True
        return h[value]

    cnf.add(h[0])
    cnf.add(-h[frobenius])
    cnf.add(-h[shift])
    for value in range((frobenius + 1) // 2):
        reflected = frobenius - value
        cnf.add(h[value], h[reflected])
        cnf.add(-h[value], -h[reflected])
    for left in range(frobenius + 1):
        for right in range(left, frobenius + 1 - left):
            cnf.add(-h[left], -h[right], h[left + right])

    window_end = 2 * frobenius + 1
    inverse = tuple(cnf.variable(f"E:{value}") for value in range(window_end + 1))
    square_inverse = tuple(cnf.variable(f"D:{value}") for value in range(window_end + 1))
    for value in range(window_end + 1):
        cnf.equivalent_and(inverse[value], [h_literal(value), h_literal(value + shift)])
        cnf.equivalent_and(
            square_inverse[value],
            [h_literal(value), h_literal(value + shift), h_literal(value + 2 * shift)],
        )

    for value in range(window_end + 1):
        decompositions: list[int] = []
        for left in range(value // 2 + 1):
            right = value - left
            pair = cnf.variable(f"P:{value}:{left}:{right}")
            cnf.equivalent_and(pair, [inverse[left], inverse[right]])
            decompositions.append(pair)
        cnf.add(-square_inverse[value], *decompositions)
    return cnf, h


def mask_from_model(h_variables: tuple[int, ...], true_variables: set[int]) -> int:
    mask = 0
    for value, variable in enumerate(h_variables):
        if variable in true_variables:
            mask |= 1 << value
    return mask
