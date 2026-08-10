"""Exact bitset algorithms for symmetric numerical semigroups and rigidity."""

from __future__ import annotations

from collections import deque


def member(mask: int, frobenius: int, value: int) -> bool:
    """Return membership, using the conductor tail above the Frobenius number."""
    if value < 0:
        return False
    if value > frobenius:
        return True
    return bool(mask & (1 << value))


def root_mask(frobenius: int) -> int:
    """Return the Blanco-Rosales root C(F) for odd positive F."""
    if frobenius <= 0 or frobenius % 2 == 0:
        raise ValueError("F must be positive and odd")
    mask = 1
    for value in range((frobenius + 1) // 2, frobenius):
        mask |= 1 << value
    return mask


def multiplicity(mask: int, frobenius: int) -> int:
    return next(
        (value for value in range(1, frobenius + 1) if member(mask, frobenius, value)),
        frobenius + 1,
    )


def is_minimal_generator(mask: int, frobenius: int, value: int) -> bool:
    if value <= 0 or not member(mask, frobenius, value):
        return False
    return not any(
        member(mask, frobenius, left) and member(mask, frobenius, value - left)
        for left in range(1, value)
    )


def minimal_generators(mask: int, frobenius: int) -> tuple[int, ...]:
    """Return minimal generators, including any generator just above F when needed."""
    conductor = frobenius + 1
    upper = 2 * conductor - 1
    return tuple(
        value
        for value in range(1, upper + 1)
        if is_minimal_generator(mask, frobenius, value)
    )


def validate_symmetric_mask(mask: int, frobenius: int) -> tuple[str, ...]:
    """Return all semantic failures for a claimed symmetric semigroup mask."""
    failures: list[str] = []
    if frobenius <= 0 or frobenius % 2 == 0:
        failures.append("F must be positive and odd")
        return tuple(failures)
    if not member(mask, frobenius, 0):
        failures.append("zero is absent")
    if member(mask, frobenius, frobenius):
        failures.append("F is present")
    extra_bits = mask >> (frobenius + 1)
    if extra_bits:
        failures.append("mask has bits above F")
    symmetry_failure = next(
        (
            value
            for value in range(frobenius + 1)
            if member(mask, frobenius, value)
            == member(mask, frobenius, frobenius - value)
        ),
        None,
    )
    if symmetry_failure is not None:
        failures.append(f"symmetry fails at {symmetry_failure}")
    closure_failure = next(
        (
            (left, right)
            for left in range(frobenius + 1)
            if member(mask, frobenius, left)
            for right in range(left, frobenius + 1 - left)
            if member(mask, frobenius, right)
            and not member(mask, frobenius, left + right)
        ),
        None,
    )
    if closure_failure is not None:
        failures.append(f"closure fails at {closure_failure}")
    genus = sum(not member(mask, frobenius, value) for value in range(1, frobenius + 1))
    if genus != (frobenius + 1) // 2:
        failures.append(f"genus is {genus}, expected {(frobenius + 1) // 2}")
    return tuple(failures)


def child_masks(mask: int, frobenius: int) -> tuple[int, ...]:
    """Apply exactly the five child conditions in Blanco-Rosales Theorem 9."""
    current_multiplicity = multiplicity(mask, frobenius)
    children: list[int] = []
    for value in range(frobenius // 2 + 1, frobenius):
        if not is_minimal_generator(mask, frobenius, value):
            continue
        if member(mask, frobenius, 2 * value - frobenius):
            continue
        if 3 * value == 2 * frobenius or 4 * value == 3 * frobenius:
            continue
        reflected = frobenius - value
        if reflected >= current_multiplicity:
            continue
        child = (mask & ~(1 << value)) | (1 << reflected)
        children.append(child)
    return tuple(children)


def enumerate_symmetric_masks(frobenius: int) -> tuple[int, ...]:
    """Enumerate the complete Theorem 9 tree in deterministic breadth-first order."""
    root = root_mask(frobenius)
    queue = deque([root])
    seen = {root}
    ordered: list[int] = []
    while queue:
        current = queue.popleft()
        failures = validate_symmetric_mask(current, frobenius)
        if failures:
            raise AssertionError(f"invalid tree node: {failures}")
        ordered.append(current)
        for child in child_masks(current, frobenius):
            if child in seen:
                raise AssertionError("tree generated a duplicate child")
            seen.add(child)
            queue.append(child)

    for current in ordered:
        if current == root:
            continue
        child_multiplicity = multiplicity(current, frobenius)
        if not 2 * child_multiplicity < frobenius:
            raise AssertionError("non-root node lacks the theorem parent condition")
        parent = (current & ~(1 << child_multiplicity)) | (
            1 << (frobenius - child_multiplicity)
        )
        if parent not in seen:
            raise AssertionError("tree parent is absent")
    return tuple(ordered)


def gap_values(mask: int, frobenius: int) -> tuple[int, ...]:
    return tuple(
        value for value in range(1, frobenius + 1) if not member(mask, frobenius, value)
    )


def analyze_rigidity(mask: int, frobenius: int, shift: int) -> dict[str, object]:
    """Check D=E+E through 2F+1 and return witnesses and the proved tail."""
    if member(mask, frobenius, shift):
        raise ValueError("shift must be a gap")
    window_end = 2 * frobenius + 1

    def inverse_member(value: int) -> bool:
        return member(mask, frobenius, value) and member(mask, frobenius, value + shift)

    def square_inverse_member(value: int) -> bool:
        return (
            member(mask, frobenius, value)
            and member(mask, frobenius, value + shift)
            and member(mask, frobenius, value + 2 * shift)
        )

    inverse_bits = 0
    square_inverse_bits = 0
    for value in range(window_end + 1):
        if inverse_member(value):
            inverse_bits |= 1 << value
        if square_inverse_member(value):
            square_inverse_bits |= 1 << value

    sum_bits = 0
    for left in range(window_end + 1):
        if inverse_bits & (1 << left):
            sum_bits |= inverse_bits << left
    window_mask = (1 << (window_end + 1)) - 1
    sum_bits &= window_mask
    missing_bits = square_inverse_bits & ~sum_bits & window_mask
    reverse_bits = sum_bits & ~square_inverse_bits & window_mask
    first_missing = (missing_bits & -missing_bits).bit_length() - 1 if missing_bits else None
    first_reverse = (reverse_bits & -reverse_bits).bit_length() - 1 if reverse_bits else None
    minimum_inverse = (inverse_bits & -inverse_bits).bit_length() - 1
    return {
        "rigid": missing_bits == 0 and reverse_bits == 0,
        "first_missing_D": first_missing,
        "first_reverse_failure": first_reverse,
        "minimum_inverse": minimum_inverse,
        "window_end": window_end,
        "tail_start": minimum_inverse + frobenius + 1,
    }
