"""EXP-020: the chamber enumeration over the eight conditions (k = 3 closer).

Term tables are hand-coded from the dossier's MACHINE-VERIFIED closed forms.
Atoms: u, p > 0; orientation signs (h1, e12, f, gam, g1, g2) restricted to
sampled-feasible vectors (additive couplings); s-ordering atoms free except
the proven cs < cx couplings; bracket atoms Bm1 = p h1 - u g1,
Bm2 = p gam - u g2 free; sum-brackets Bs1 = u g1 + p h1, Bs2 = u g2 + p gam
forced when their height pair agrees in sign, else free.

SOUNDNESS DIRECTION: free atoms give a SUPERSET of feasible chambers, so an
EMPTY residual is a valid conclusion (no interior chamber can hold a
rank-<=2 point); a nonempty residual is a to-analyze list, not a defeat.
Interior only: the atom boundaries (h1 = 0 etc.) are explicit hypersurfaces
recorded for separate bookkeeping.
"""
import itertools, json, random, fractions
from pathlib import Path

ART = Path(__file__).resolve().parent / "artifacts"
ART.mkdir(exist_ok=True)

OR = ["h1", "e12", "f", "gam", "g1", "g2"]
SAT = ["s_r12_d1A", "s_r12_d1B", "s_r12_d2A", "s_r12_d2B",
       "s_d1A_wA", "s_d2A_wA", "s_d1B_wB", "s_d2B_wB",
       "s_d1A_cs", "s_d1A_cx", "s_d2A_cs", "s_d2A_cx",
       "s_d1B_cs", "s_d1B_cx", "s_d2B_cs", "s_d2B_cx",
       "s_d1A_d1B", "s_d2A_d2B", "s_wA_cs", "s_wA_cx", "s_cs_wB", "s_cx_wB"]
BR = ["Bm1", "Bm2", "Bs1", "Bs2"]

# entry = list of terms; term = (sign_const, [orientation atoms], [s atoms], [bracket atoms])
E = {
    ("L13", "m2"): [(-1, ["e12"], ["s_r12_d2A"], [])],
    ("L23", "m1"): [(+1, ["e12"], ["s_r12_d1A"], [])],
    ("L15", "m2"): [(-1, ["e12"], ["s_r12_d2B"], [])],
    ("L25", "m1"): [(+1, ["e12"], ["s_r12_d1B"], [])],
    ("L13", "mA"): [(-1, ["h1"], ["s_d1A_wA"], [])],
    ("L23", "mA"): [(-1, ["gam"], ["s_d2A_wA"], [])],
    ("L15", "mB"): [(-1, ["g1"], ["s_d1B_wB"], [])],
    ("L25", "mB"): [(-1, ["g2"], ["s_d2B_wB"], [])],
    ("L13", "mB"): [(+1, [], ["s_d1B_cs"], ["Bm1"]), (-1, [], ["s_d1B_cx"], ["Bs1"])],
    ("L23", "mB"): [(+1, [], ["s_d2B_cs"], ["Bm2"]), (-1, [], ["s_d2B_cx"], ["Bs2"])],
    ("L15", "mA"): [(-1, [], ["s_d1A_cs"], ["Bm1"]), (-1, [], ["s_d1A_cx"], ["Bs1"])],
    ("L25", "mA"): [(-1, [], ["s_d2A_cs"], ["Bm2"]), (-1, [], ["s_d2A_cx"], ["Bs2"])],
    ("L35", "m1"): [(+1, [], ["s_d1A_d1B"], ["Bm1"])],
    ("L35", "m2"): [(+1, [], ["s_d2A_d2B"], ["Bm2"])],
    ("L36", "m1"): [(-1, [], ["s_d1A_d1B"], ["Bs1"])],
    ("L36", "m2"): [(-1, [], ["s_d2A_d2B"], ["Bs2"])],
    ("L35", "mA"): [(-1, ["f"], ["s_wA_cx"], [])],
    ("L35", "mB"): [(-1, ["f"], ["s_cx_wB"], [])],
    ("L36", "mA"): [(-1, ["f"], ["s_wA_cs"], [])],
    ("L36", "mB"): [(+1, ["f"], ["s_cs_wB"], [])],
}
# u/p powers are strictly positive and constant-sign: omitted (never flip signs).


def mul_terms(t1, t2, sgn=+1):
    return (sgn * t1[0] * t2[0], t1[1] + t2[1], t1[2] + t2[2], t1[3] + t2[3])


def combo(*factors_and_signs):
    """product of entries (each a term list) with an overall sign per addend"""
    out = []
    for sgn, entries in factors_and_signs:
        acc = [(sgn, [], [], [])]
        for ent in entries:
            acc = [mul_terms(a, t) for a in acc for t in ent]
        out.extend(acc)
    return out


b13 = E[("L13", "m2")]; b15 = E[("L15", "m2")]
a23 = E[("L23", "m1")]; a25 = E[("L25", "m1")]
COND = {
    "C1": combo((+1, [b13, E[("L15", "mA")]]), (-1, [b15, E[("L13", "mA")]])),
    "C2": combo((+1, [b13, E[("L15", "mB")]]), (-1, [b15, E[("L13", "mB")]])),
    "C3": combo((+1, [a23, E[("L25", "mA")]]), (-1, [a25, E[("L23", "mA")]])),
    "C4": combo((+1, [a23, E[("L25", "mB")]]), (-1, [a25, E[("L23", "mB")]])),
    "C5": combo((+1, [a23, b13, E[("L35", "mA")]]),
                (-1, [b13, E[("L23", "mA")], E[("L35", "m1")]]),
                (-1, [a23, E[("L13", "mA")], E[("L35", "m2")]])),
    "C6": combo((+1, [a23, b13, E[("L35", "mB")]]),
                (-1, [b13, E[("L23", "mB")], E[("L35", "m1")]]),
                (-1, [a23, E[("L13", "mB")], E[("L35", "m2")]])),
    "C7": combo((+1, [a23, b13, E[("L36", "mA")]]),
                (-1, [b13, E[("L23", "mA")], E[("L36", "m1")]]),
                (-1, [a23, E[("L13", "mA")], E[("L36", "m2")]])),
    "C8": combo((+1, [a23, b13, E[("L36", "mB")]]),
                (-1, [b13, E[("L23", "mB")], E[("L36", "m1")]]),
                (-1, [a23, E[("L13", "mB")], E[("L36", "m2")]])),
}

# feasible orientation sign vectors by dense rational sampling
rng = random.Random(20260802)
feas = set()
for _ in range(200000):
    h1 = rng.uniform(-3, 3); e12 = rng.uniform(-3, 3); f = rng.uniform(-3, 3)
    gam = h1 - e12; g1 = h1 + f; g2 = gam + f
    vals = [h1, e12, f, gam, g1, g2]
    if any(abs(x) < 1e-6 for x in vals):
        continue
    feas.add(tuple(1 if x > 0 else -1 for x in vals))
feas = sorted(feas)

def term_sign(term, orient, satoms, bratoms):
    s = term[0]
    for a in term[1]:
        s *= orient[a]
    for a in term[2]:
        s *= satoms[a]
    for a in term[3]:
        s *= bratoms[a]
    return s

def bracket_domain(orient):
    """Bs1 forced if h1,g1 agree; Bs2 if gam,g2 agree; Bm free."""
    doms = {}
    doms["Bm1"] = (-1, +1)
    doms["Bm2"] = (-1, +1)
    doms["Bs1"] = ((orient["h1"],) if orient["h1"] == orient["g1"] else (-1, +1))
    doms["Bs2"] = ((orient["gam"],) if orient["gam"] == orient["g2"] else (-1, +1))
    return doms

# cs < cx couplings: exclude (s_x_cs, s_x_cx) = (+,-) ; exclude (s_cs_wB, s_cx_wB) = (-,+)
CS_CX_PAIRS = [("s_d1A_cs", "s_d1A_cx"), ("s_d2A_cs", "s_d2A_cx"),
               ("s_d1B_cs", "s_d1B_cx"), ("s_d2B_cs", "s_d2B_cx"),
               ("s_wA_cs", "s_wA_cx")]
WB_PAIR = ("s_cs_wB", "s_cx_wB")

def satoms_of(cond):
    out = set()
    for t in COND[cond]:
        out.update(t[2])
    return out

ALL_S = sorted(set().union(*[satoms_of(c) for c in COND]))

def atoms_of(cond):
    s, b = set(), set()
    for t in COND[cond]:
        s.update(t[2]); b.update(t[3])
    return sorted(s), sorted(b)


def nondef_table(cond, orient, bdoms):
    """All assignments over THIS condition's s/bracket atoms where it is
    NOT sign-definite (contains both signs among its terms)."""
    sa, ba = atoms_of(cond)
    rows = []
    for sv in itertools.product((-1, +1), repeat=len(sa)):
        sd = dict(zip(sa, sv))
        for bv in itertools.product(*[bdoms[b] for b in ba]):
            bd = dict(zip(ba, bv))
            signs = {term_sign(t, orient, sd, bd) for t in COND[cond]}
            if len(signs) > 1:
                rows.append({**sd, **bd})
    return rows


def compatible(a, b):
    return all(b[k] == v for k, v in a.items() if k in b)


def couplings_ok(assign):
    for x, y in CS_CX_PAIRS:
        if assign.get(x) == 1 and assign.get(y) == -1:
            return False
    if assign.get(WB_PAIR[0]) == -1 and assign.get(WB_PAIR[1]) == 1:
        return False
    return True


residual_orientations = {}
total_residual = 0
for orient_vec in feas:
    orient = dict(zip(OR, orient_vec))
    bdoms = bracket_domain(orient)
    tables = sorted((nondef_table(c, orient, bdoms) for c in COND), key=len)
    if any(len(t) == 0 for t in tables):
        continue  # some condition is ALWAYS definite here: chamber family clear
    joined = [dict(r) for r in tables[0]]
    for tbl in tables[1:]:
        nxt = []
        for a in joined:
            for r in tbl:
                if compatible(r, a):
                    m = {**a, **r}
                    if couplings_ok(m):
                        nxt.append(m)
        joined = nxt
        if not joined:
            break
        if len(joined) > 500000:
            joined = joined[:500000]  # cap, recorded
    if joined:
        residual_orientations[str(orient_vec)] = len(joined)
        total_residual += len(joined)

print(f"feasible orientation vectors: {len(feas)}")
print(f"orientation vectors WITH residual chambers: {len(residual_orientations)}")
print(f"total residual joined assignments: {total_residual}")
(ART / "residual-count.json").write_text(json.dumps(
    {"feasible_orientations": len(feas),
     "residual_orientations": residual_orientations,
     "total_residual": total_residual}, indent=2), encoding="utf-8")
