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

    def equivalent_or(self, output: int, inputs: list[Literal]) -> None:
        if any(value is True for value in inputs):
            self.add(output)
            return
        active = [int(value) for value in inputs if value is not False]
        if not active:
            self.add(-output)
            return
        for value in active:
            self.add(-value, output)
        self.add(-output, *active)

    def guarded_equivalent_and(self, guard: int, output: int, inputs: list[Literal]) -> None:
        """Add ``guard -> (output iff AND(inputs))`` without branch variables."""
        if any(value is False for value in inputs):
            self.add(-guard, -output)
            return
        active = [int(value) for value in inputs if value is not True]
        if not active:
            self.add(-guard, output)
            return
        for value in active:
            self.add(-guard, -output, value)
        self.add(-guard, output, *(-value for value in active))

    def write(self, path: Path, comments: list[str] | None = None) -> None:
        lines = [f"c {comment}" for comment in comments or []]
        lines.append(f"p cnf {len(self.names)} {len(self.clauses)}")
        lines.extend(" ".join(map(str, clause)) + " 0" for clause in self.clauses)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text("\n".join(lines) + "\n", encoding="ascii")
        temporary.replace(path)


def add_exact_cardinality(cnf: CNF, literals: tuple[int, ...], count: int, prefix: str) -> None:
    """Require exactly ``count`` literals using an exact sequential threshold circuit."""
    if not literals:
        if count != 0:
            cnf.add()
        return
    if len(set(literals)) != len(literals) or any(literal == 0 for literal in literals):
        raise ValueError("cardinality literals must be distinct and nonzero")
    if not 0 <= count <= len(literals):
        cnf.add()
        return

    # threshold[(i,j)] means at least j of the first i literals are true.
    threshold: dict[tuple[int, int], int] = {}
    for index, literal in enumerate(literals, start=1):
        for level in range(1, index + 1):
            output = cnf.variable(f"{prefix}:at-least:{index}:{level}")
            threshold[index, level] = output
            prior_same: Literal = threshold.get((index - 1, level), False)
            prior_lower: Literal = True if level == 1 else threshold[index - 1, level - 1]
            enters = cnf.variable(f"{prefix}:enters:{index}:{level}")
            cnf.equivalent_and(enters, [literal, prior_lower])
            cnf.equivalent_or(output, [prior_same, enters])

    if count == 0:
        cnf.add(-threshold[len(literals), 1])
    else:
        cnf.add(threshold[len(literals), count])
        if count < len(literals):
            cnf.add(-threshold[len(literals), count + 1])


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


def build_selector_rigidity_cnf(
    frobenius: int,
) -> tuple[CNF, tuple[int, ...], tuple[int, ...]]:
    """Build one CNF existentially selecting every possible shift for a fixed F."""
    if frobenius <= 0 or frobenius % 2 == 0:
        raise ValueError("F must be positive and odd")
    cnf = CNF()
    h = tuple(cnf.variable(f"h:{value}") for value in range(frobenius + 1))
    q = tuple(cnf.variable(f"q:{shift}") for shift in range(1, frobenius + 1))

    def h_literal(value: int) -> Literal:
        if value < 0:
            return False
        if value > frobenius:
            return True
        return h[value]

    cnf.add(h[0])
    cnf.add(-h[frobenius])
    for value in range((frobenius + 1) // 2):
        reflected = frobenius - value
        cnf.add(h[value], h[reflected])
        cnf.add(-h[value], -h[reflected])
    for left in range(frobenius + 1):
        for right in range(left, frobenius + 1 - left):
            cnf.add(-h[left], -h[right], h[left + right])

    # Exactly one shift is active, and the selected shift must be a gap.
    cnf.add(*q)
    for left in range(len(q)):
        for right in range(left + 1, len(q)):
            cnf.add(-q[left], -q[right])
    for shift, selector in enumerate(q, start=1):
        cnf.add(-selector, -h[shift])

    window_end = 2 * frobenius + 1
    inverse = tuple(cnf.variable(f"E:{value}") for value in range(window_end + 1))
    square_inverse = tuple(cnf.variable(f"D:{value}") for value in range(window_end + 1))
    for value in range(window_end + 1):
        for shift, selector in enumerate(q, start=1):
            cnf.guarded_equivalent_and(
                selector,
                inverse[value],
                [h_literal(value), h_literal(value + shift)],
            )
            cnf.guarded_equivalent_and(
                selector,
                square_inverse[value],
                [
                    h_literal(value),
                    h_literal(value + shift),
                    h_literal(value + 2 * shift),
                ],
            )

    for value in range(window_end + 1):
        decompositions: list[int] = []
        for left in range(value // 2 + 1):
            right = value - left
            pair = cnf.variable(f"P:{value}:{left}:{right}")
            cnf.equivalent_and(pair, [inverse[left], inverse[right]])
            decompositions.append(pair)
        cnf.add(-square_inverse[value], *decompositions)
    return cnf, h, q


def mask_from_model(h_variables: tuple[int, ...], true_variables: set[int]) -> int:
    mask = 0
    for value, variable in enumerate(h_variables):
        if variable in true_variables:
            mask |= 1 << value
    return mask


def shift_from_model(q_variables: tuple[int, ...], true_variables: set[int]) -> int:
    """Decode the unique one-hot shift, rejecting absent or multiple selectors."""
    selected = [shift for shift, variable in enumerate(q_variables, start=1) if variable in true_variables]
    if len(selected) != 1:
        raise ValueError(f"expected one selected shift, found {selected}")
    return selected[0]


def projected_blocking_clause(variables: tuple[int, ...], true_variables: set[int]) -> tuple[int, ...]:
    """Return the unique clause falsified by this complete projected assignment."""
    if not variables:
        raise ValueError("a projected assignment must contain at least one variable")
    if len(set(variables)) != len(variables) or any(variable <= 0 for variable in variables):
        raise ValueError("projected variables must be distinct positive integers")
    return tuple(-variable if variable in true_variables else variable for variable in variables)
