"""Exact dense linear algebra over a field object of fields.py (no floating point anywhere)."""


class Echelon:
    """A fully reduced row echelon basis, grown one vector at a time.

    Every stored row has a unit entry at its pivot column and zeros at the pivot columns of all other rows,
    so reducing a vector is a single pass and the coordinates of a vector of the span are its pivot entries.
    """

    def __init__(self, F, n):
        self.F = F
        self.n = n
        self.rows = {}  # pivot column -> row (list of length n)

    @property
    def pivots(self):
        return sorted(self.rows)

    def rank(self):
        return len(self.rows)

    def reduce(self, v):
        F = self.F
        v = list(v)
        for p, row in self.rows.items():
            c = v[p]
            if not F.is_zero(c):
                for j in range(self.n):
                    if not F.is_zero(row[j]):
                        v[j] = F.sub(v[j], F.mul(c, row[j]))
        return v

    def insert(self, v):
        """Add v; return True when it was independent of the current rows."""
        F = self.F
        r = self.reduce(v)
        piv = next((j for j in range(self.n) if not F.is_zero(r[j])), None)
        if piv is None:
            return False
        inv = F.inv(r[piv])
        r = [F.mul(inv, e) for e in r]
        for p, row in self.rows.items():
            c = row[piv]
            if not F.is_zero(c):
                self.rows[p] = [F.sub(row[j], F.mul(c, r[j])) for j in range(self.n)]
        self.rows[piv] = r
        return True

    def nonpivots(self):
        piv = set(self.rows)
        return [j for j in range(self.n) if j not in piv]

    def coordinates(self, v):
        """Coordinates of v modulo the span, on the non-pivot columns."""
        r = self.reduce(v)
        return [r[j] for j in self.nonpivots()]


def rank(F, vectors, n):
    e = Echelon(F, n)
    for v in vectors:
        e.insert(v)
    return e.rank()


def kernel(F, images, tdim):
    """Kernel of the linear map given by the images of the basis vectors (each a list of length tdim).

    Returns a list of vectors (length len(images)) spanning the kernel.
    """
    n = len(images)
    pivrows = {}  # pivot (in 0..tdim-1) -> augmented row
    ker = []
    for i, img in enumerate(images):
        row = list(img) + [F.one if j == i else F.zero for j in range(n)]
        for p, prow in pivrows.items():
            c = row[p]
            if not F.is_zero(c):
                row = [F.sub(row[j], F.mul(c, prow[j])) for j in range(tdim + n)]
        piv = next((j for j in range(tdim) if not F.is_zero(row[j])), None)
        if piv is None:
            ker.append(row[tdim:])
        else:
            inv = F.inv(row[piv])
            row = [F.mul(inv, e) for e in row]
            for p, prow in list(pivrows.items()):
                c = prow[piv]
                if not F.is_zero(c):
                    pivrows[p] = [F.sub(prow[j], F.mul(c, row[j])) for j in range(tdim + n)]
            pivrows[piv] = row
    return ker
