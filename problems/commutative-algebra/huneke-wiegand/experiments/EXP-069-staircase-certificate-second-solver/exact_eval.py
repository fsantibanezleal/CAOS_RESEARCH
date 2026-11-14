"""Exact integer evaluator of the SMT-LIB assertions of EXP-069 (no solver involved).

It reads the exported SMT-LIB 2 text with its own s-expression parser and evaluates every assertion over the
integers (Python integers, exact) under given values of the declared constants. Supported: and, or, not, =>,
=, distinct, <=, <, >=, >, +, -, *, ite, let, numerals, true, false, and exists. A bounded existential
quantifier is decided by enumerating the integers its body allows: the bounds of each bound variable are
read off the conjuncts of the body (comparisons of the variable with an evaluable term, disjunctions of such
intervals), and a conjunct that is an equation with one unassigned variable fixes that variable. A quantifier
with a variable that has no finite bound raises `Unevaluable`; nothing is guessed.
"""

from __future__ import annotations

import re
from fractions import Fraction

TOKEN = re.compile(r"\s*(;[^\n]*|\(|\)|\|[^|]*\||[^\s()]+)")


class Unevaluable(Exception):
    """The formula contains a construct this evaluator cannot decide exactly."""


class _Unassigned(Exception):
    """A bound variable without a value yet (internal; used for early pruning)."""


def parse(text: str) -> list:
    tokens = [t for t in TOKEN.findall(text) if not t.startswith(";")]
    stack: list[list] = [[]]
    for token in tokens:
        if token == "(":
            stack.append([])
        elif token == ")":
            done = stack.pop()
            stack[-1].append(done)
        else:
            stack[-1].append(token)
    if len(stack) != 1:
        raise ValueError("unbalanced s-expression")
    return stack[0]


class _Thunk:
    __slots__ = ("expr", "lex", "stamp", "value")

    def __init__(self, expr, lex) -> None:
        self.expr, self.lex, self.stamp, self.value = expr, lex, -1, None


class Evaluator:
    def __init__(self, consts: dict[str, int]) -> None:
        self.consts = consts
        self.qvars: dict[str, int] = {}
        self.stamp = 0
        self.nodes = 0

    # ---- evaluation -------------------------------------------------------------------------------------
    def ev(self, term, lex):
        if isinstance(term, str):
            return self.atom(term, lex)
        head = term[0]
        if head == "let":
            inner = dict(lex)
            for name, expr in term[1]:
                inner[name] = _Thunk(expr, lex)
            return self.ev(term[2], inner)
        if head == "and":
            for sub in term[1:]:
                if not self.ev(sub, lex):
                    return False
            return True
        if head == "or":
            pending = False
            for sub in term[1:]:
                try:
                    if self.ev(sub, lex):
                        return True
                except _Unassigned:
                    pending = True
            if pending:
                raise _Unassigned()
            return False
        if head == "not":
            return not self.ev(term[1], lex)
        if head == "=>":
            return (not self.ev(term[1], lex)) or bool(self.ev(term[2], lex))
        if head == "ite":
            return self.ev(term[2], lex) if self.ev(term[1], lex) else self.ev(term[3], lex)
        if head == "exists":
            return self.exists(term, lex)
        if head == "forall":
            raise Unevaluable("universal quantifier")
        if head == "!":
            return self.ev(term[1], lex)
        args = [self.ev(sub, lex) for sub in term[1:]]
        if head == "+":
            return sum(args)
        if head == "-":
            return -args[0] if len(args) == 1 else args[0] - sum(args[1:])
        if head == "*":
            out = 1
            for value in args:
                out *= value
            return out
        if head == "=":
            return all(args[0] == value for value in args[1:])
        if head == "distinct":
            return len(set(args)) == len(args)
        if head == "<=":
            return all(args[i] <= args[i + 1] for i in range(len(args) - 1))
        if head == "<":
            return all(args[i] < args[i + 1] for i in range(len(args) - 1))
        if head == ">=":
            return all(args[i] >= args[i + 1] for i in range(len(args) - 1))
        if head == ">":
            return all(args[i] > args[i + 1] for i in range(len(args) - 1))
        raise Unevaluable(f"unsupported operator {head}")

    def atom(self, name: str, lex):
        if name in lex:
            thunk = lex[name]
            if thunk.stamp != self.stamp:
                thunk.value = self.ev(thunk.expr, thunk.lex)
                thunk.stamp = self.stamp
            return thunk.value
        if name in self.qvars:
            return self.qvars[name]
        if name in self.consts:
            return self.consts[name]
        if name == "true":
            return True
        if name == "false":
            return False
        if re.fullmatch(r"-?\d+", name):
            return int(name)
        if name in self.bound_names:
            raise _Unassigned()
        raise Unevaluable(f"unknown symbol {name}")

    # ---- structure helpers ------------------------------------------------------------------------------
    def expand(self, term, lex):
        """Strip lets and resolve let-bound symbols down to a non-let compound term."""
        while True:
            if isinstance(term, str) and term in lex:
                thunk = lex[term]
                term, lex = thunk.expr, thunk.lex
            elif not isinstance(term, str) and term[0] == "let":
                inner = dict(lex)
                for name, expr in term[1]:
                    inner[name] = _Thunk(expr, lex)
                term, lex = term[2], inner
            elif not isinstance(term, str) and term[0] == "!":
                term = term[1]
            else:
                return term, lex

    def conjuncts(self, term, lex) -> list:
        term, lex = self.expand(term, lex)
        if not isinstance(term, str) and term[0] == "and":
            out = []
            for sub in term[1:]:
                out.extend(self.conjuncts(sub, lex))
            return out
        return [(term, lex)]

    def try_value(self, term, lex):
        try:
            return self.ev(term, lex)
        except _Unassigned:
            return None

    def linear(self, term, lex):
        """(coefficients over unassigned bound variables, constant) of an arithmetic term, or None."""
        term, lex = self.expand(term, lex)
        if isinstance(term, str):
            if term in self.bound_names and term not in self.qvars:
                return {term: 1}, 0
            return {}, self.ev(term, lex)
        head = term[0]
        if head in ("+", "-"):
            parts = [self.linear(sub, lex) for sub in term[1:]]
            if any(part is None for part in parts):
                return None
            if head == "-" and len(parts) == 1:
                return {k: -v for k, v in parts[0][0].items()}, -parts[0][1]
            coeffs: dict[str, int] = {}
            const = 0
            for position, (c, k) in enumerate(parts):
                sign = -1 if head == "-" and position > 0 else 1
                const += sign * k
                for name, value in c.items():
                    coeffs[name] = coeffs.get(name, 0) + sign * value
            return coeffs, const
        if head == "*":
            parts = [self.linear(sub, lex) for sub in term[1:]]
            if any(part is None for part in parts):
                return None
            varying = [part for part in parts if part[0]]
            if len(varying) > 1:
                return None
            scale = 1
            for c, k in parts:
                if not c:
                    scale *= k
            if not varying:
                return {}, scale
            return {k: v * scale for k, v in varying[0][0].items()}, varying[0][1] * scale
        value = self.try_value(term, lex)
        return None if value is None else ({}, value)

    # ---- bounds of a variable --------------------------------------------------------------------------
    @staticmethod
    def intersect(left, right):
        out = []
        for a, b in left:
            for c, d in right:
                lo, hi = max(a, c), min(b, d)
                if lo <= hi:
                    out.append((lo, hi))
        return sorted(out)

    def bounds(self, name: str, term, lex):
        """Finite union of intervals the variable must lie in for `term` to hold, or None when unknown."""
        term, lex = self.expand(term, lex)
        if isinstance(term, str):
            return None
        head = term[0]
        INF = Fraction(10**18)
        if head == "and":
            result = None
            for sub in term[1:]:
                got = self.bounds(name, sub, lex)
                if got is not None:
                    result = got if result is None else self.intersect(result, got)
            return result
        if head == "or":
            union = []
            for sub in term[1:]:
                got = self.bounds(name, sub, lex)
                if got is None:
                    return None
                union.extend(got)
            return sorted(union)
        if head in ("<=", "<", ">=", ">", "=") and len(term) == 3:
            left, right = self.linear(term[1], lex), self.linear(term[2], lex)
            if left is None or right is None:
                return None
            coeffs: dict[str, int] = dict(left[0])
            for key, value in right[0].items():
                coeffs[key] = coeffs.get(key, 0) - value
            const = left[1] - right[1]
            coeffs = {k: v for k, v in coeffs.items() if v}
            if set(coeffs) != {name}:
                return None
            c = coeffs[name]
            # c*x + const OP 0
            op = head
            if c < 0:
                c, const = -c, -const
                op = {"<=": ">=", "<": ">", ">=": "<=", ">": "<", "=": "="}[op]
            # c*x OP -const
            rhs = -const
            if op == "=":
                return [(rhs // c, rhs // c)] if rhs % c == 0 else []
            if op == "<=":
                return [(-int(INF), rhs // c)]
            if op == "<":
                return [(-int(INF), (rhs - 1) // c)]
            if op == ">=":
                return [(-((-rhs) // c), int(INF))]
            return [(-((-(rhs + 1)) // c), int(INF))]
        return None

    # ---- quantifier ----------------------------------------------------------------------------------------
    def exists(self, term, lex) -> bool:
        names = [binding[0] for binding in term[1]]
        body, body_lex = term[2], lex
        saved = {n: self.qvars.get(n) for n in names}
        self.bound_names |= set(names)
        for n in names:
            self.qvars.pop(n, None)
        self.stamp += 1
        conj = self.conjuncts(body, body_lex)

        def search(index: int) -> bool:
            if index == len(names):
                return all(self.ev(t, l) for t, l in conj)
            name = names[index]
            domain = None
            for t, l in conj:
                got = self.bounds(name, t, l)
                if got is not None:
                    domain = got if domain is None else self.intersect(domain, got)
            if domain is None:
                raise Unevaluable(f"unbounded quantified variable {name}")
            for lo, hi in domain:
                if hi - lo > 5 * 10**6:
                    raise Unevaluable(f"variable {name} has no finite bound")
                value = lo
                while value <= hi:
                    self.qvars[name] = value
                    self.stamp += 1
                    self.nodes += 1
                    viable = True
                    for t, l in conj:
                        try:
                            if not self.ev(t, l):
                                viable = False
                                break
                        except _Unassigned:
                            continue
                    if viable and search(index + 1):
                        return True
                    value += 1
            self.qvars.pop(name, None)
            self.stamp += 1
            return False

        try:
            return search(0)
        finally:
            for n in names:
                self.qvars.pop(n, None)
                if saved[n] is not None:
                    self.qvars[n] = saved[n]
            self.stamp += 1

    bound_names: set[str] = set()


def evaluate_assertions(text: str, consts: dict[str, int]) -> bool:
    """True iff every `assert` of the SMT-LIB text holds under the values of the declared constants."""
    evaluator = Evaluator(dict(consts))
    evaluator.bound_names = set()
    verdict = True
    for command in parse(text):
        if isinstance(command, list) and command and command[0] == "assert":
            if not evaluator.ev(command[1], {}):
                verdict = False
    return verdict
