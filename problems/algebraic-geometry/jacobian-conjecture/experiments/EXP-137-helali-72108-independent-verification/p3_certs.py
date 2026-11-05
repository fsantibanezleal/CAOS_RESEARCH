"""EXP-137 P3/P4: re-evaluate Helali's serialized identities with our own exact arithmetic.

Pickles are read only through exp137_lib.restricted_loads (builtins + Fraction). Number fields are built from the
minimal polynomial stored in the certificate, checked irreducible over Q, and compared with our own field.
"""

from __future__ import annotations

import hashlib
import re
import sys
import time
from pathlib import Path

from flint import fmpq, fmpq_poly

import exp137_lib as L

sys.set_int_max_str_digits(0)

ARCH = Path("E:/_Datos/caos-research/jacobian-conjecture/sources/helali-21479814/bundle/exact_replay")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_pickle(name):
    data = (ARCH / name).read_bytes()
    return L.restricted_loads(data), {"file": name, "sha256": hashlib.sha256(data).hexdigest(),
                                      "pickle_global_opcodes": [str(x) for x in L.pickle_globals(data)]}


def field_from_coeffs(coeffs):
    return L.NF(fmpq_poly([fmpq(int(n), int(d)) for n, d in coeffs]))


def decode_k(F, ser):
    co = {int(deg): fmpq(int(n), int(d)) for deg, (n, d) in ser.items()}
    top = max(co) if co else 0
    return F.el(fmpq_poly([co.get(i, fmpq(0)) for i in range(top + 1)]))


def decode_poly(F, ser):
    return {tuple(m): decode_k(F, c) for m, c in ser.items()}


def pmul(F, a, b):
    out: dict = {}
    for m, c in a.items():
        for n, e in b.items():
            k = tuple(i + j for i, j in zip(m, n))
            out[k] = out[k] + c * e if k in out else c * e
    return out


def padd_into(acc, b):
    for m, c in b.items():
        acc[m] = acc[m] + c if m in acc else c


def residual_of_identity(F, gens, mults, target):
    """sum g_i m_i - target, as {monomial: coefficient} with zero entries removed. target: {mono: Kel}."""
    acc: dict = {}
    for g, m in zip(gens, mults):
        padd_into(acc, pmul(F, g, m))
    for m, c in target.items():
        acc[m] = acc[m] - c if m in acc else -c
    return {m: c for m, c in acc.items() if c}


def minpoly_monic_hash(F):
    p = F.m / F.m[F.m.degree()]
    return hashlib.sha256(",".join(f"{int(p[i].p)}/{int(p[i].q)}" for i in range(p.degree() + 1)).encode()).hexdigest()


def corrupt_coefficient(F, poly, which=0):
    """Add 1 to the which-th coefficient (sorted monomial order) of a polynomial dict; returns a new dict."""
    keys = sorted(poly)
    out = dict(poly)
    out[keys[which]] = out[keys[which]] + 1
    return out


def check_sum_identity(name, payload_name, expected_format, expected_branch=None, ours_hash=None, log=print):
    """Case 2 unit identity (1 = sum T_i R_i) and the h=0 unit certificates share this shape."""
    payload, meta = load_pickle(payload_name)
    res = {"certificate": meta, "status": "UNVERIFIED"}
    if payload.get("format") != expected_format:
        res["reason"] = f"unexpected format {payload.get('format')}"
        return res
    if expected_branch is not None:
        res["branch_label"] = payload.get("branch")
    F = field_from_coeffs(payload["field_minpoly_coefficients"])
    res["field_degree"] = F.deg
    res["field_minpoly_irreducible_over_Q"] = True  # NF() raised otherwise
    res["field_minpoly_monic_sha256"] = minpoly_monic_hash(F)
    if ours_hash is not None:
        res["field_equals_our_P2_field"] = bool(minpoly_monic_hash(F) == ours_hash)
    gens = [decode_poly(F, g) for g in payload["generators"]]
    mults = [decode_poly(F, m) for m in payload["multipliers"]]
    one = {(0,) * len(next(iter(gens[0]))): F.el(1)}
    t0 = time.time()
    resid = residual_of_identity(F, gens, mults, one)
    res["generators"] = len(gens)
    res["generator_terms"] = [len(g) for g in gens]
    res["multiplier_terms"] = [len(m) for m in mults]
    res["identity_residual_nonzero_terms"] = len(resid)
    res["identity_holds_sum_gT_equals_1"] = len(resid) == 0
    res["eval_seconds"] = round(time.time() - t0, 2)
    # P4 controls
    ci = max(range(len(mults)), key=lambda i: len(mults[i]))
    bad = list(mults)
    bad[ci] = corrupt_coefficient(F, mults[ci])
    r1 = residual_of_identity(F, gens, bad, one)
    gi = max(range(len(gens)), key=lambda i: len(gens[i]))
    badg = list(gens)
    badg[gi] = corrupt_coefficient(F, gens[gi])
    r2 = residual_of_identity(F, badg, mults, one)
    res["p4_corrupt_multiplier_coefficient_identity_fails"] = len(r1) > 0
    res["p4_corrupt_generator_coefficient_identity_fails"] = len(r2) > 0
    res["p4_residual_terms_after_corruption"] = [len(r1), len(r2)]
    res["status"] = "PASS" if res["identity_holds_sum_gT_equals_1"] else "FAIL"
    res["_gens"] = gens
    res["_F"] = F
    return res


# ---------------------------------------------------------------- hard identity

TERM = re.compile(r"\((-?\d+)(?:/(\d+))?\)(?:\*w(?:\^(\d+))?)?")


def parse_L_coeff(s):
    """'(a/b)+(c/d)*w+(e)*w^2...' -> list of 5 fmpq (exponents must already be < 5)."""
    co = [fmpq(0)] * 5
    for m in TERM.finditer(s):
        num, den, deg = int(m.group(1)), int(m.group(2) or 1), m.group(3)
        d = int(deg) if deg is not None else (1 if "*w" in m.group(0) else 0)
        if not 0 <= d < 5:
            raise ValueError("exponent not reduced")
        co[d] += fmpq(num, den)
    return co


def check_hard_identity(log=print):
    res = {"status": "UNVERIFIED"}
    sysobj, meta_sys = load_pickle("hne0_polred.pkl")
    res["system_pickle"] = meta_sys
    cert = ARCH / "hard" / "h_certificate_exact.txt"
    res["certificate_file"] = {"file": "hard/h_certificate_exact.txt", "bytes": cert.stat().st_size}
    t0 = time.time()
    res["certificate_sha256"] = sha256(cert)
    log(f"hard: certificate hashed in {time.time() - t0:.1f} s")
    header = []
    terms = []
    with open(cert) as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if n <= 4:
                header.append(line)
                continue
            parts = line.split("|", 5)
            assert parts[0] == "C" and len(parts) == 6
            eq, a, b, c = map(int, parts[1:5])
            terms.append(((eq, a, b, c), parse_L_coeff(parts[5])))
    res["header"] = header
    minp = header[1].split("=", 1)[1]
    assert minp == "w^5-w^4+3*w^3+3*w^2+26"
    FL = L.NF(fmpq_poly([26, 0, 3, 3, -1, 1]))  # irreducibility checked here
    res["field_minpoly"] = minp
    res["field_minpoly_irreducible_over_Q"] = True
    res["multiplier_coefficients"] = len(terms)
    supports = {s for s, _ in terms}
    res["distinct_supports"] = len(supports)
    res["max_bits_numerator"] = max(int(abs(x.p)).bit_length() for _, co in terms for x in co)
    # system E_i: list of dicts mono(3) -> {deg: (num, den)}
    E = [decode_poly(FL, e) for e in sysobj]
    res["system_equations"] = len(E)
    res["system_terms"] = [len(e) for e in E]
    used = sorted({eq for (eq, _a, _b, _c), _ in terms})
    res["equations_used"] = used
    acc: dict = {}
    for (eq, a, b, c), co in terms:
        T = FL.el(fmpq_poly(co))
        for m, sc in E[eq - 1].items():
            k = (m[0] + a, m[1] + b, m[2] + c)
            v = T * sc
            acc[k] = acc[k] + v if k in acc else v
    # h = sum T_i E_i  <=>  sum T_i E_i - h = 0
    target = (1, 0, 0)
    acc[target] = acc[target] - 1 if target in acc else FL.el(-1)
    resid = {m: c for m, c in acc.items() if c}
    res["distinct_monomials_in_identity"] = len(acc)
    res["identity_residual_nonzero_terms"] = len(resid)
    res["identity_holds_h_equals_sum_TE"] = len(resid) == 0
    res["eval_seconds"] = round(time.time() - t0, 1)
    # P4 corruptions
    def total(corrupt_cert=None, corrupt_gen=None):
        accb: dict = {}
        for idx, ((eq, a, b, c), co) in enumerate(terms):
            if corrupt_cert == idx:
                co = [co[0] + 1] + co[1:]
            T = FL.el(fmpq_poly(co))
            Eq = E[eq - 1]
            for m, sc in Eq.items():
                if corrupt_gen is not None and corrupt_gen[0] == eq and corrupt_gen[1] == m:
                    sc = sc + 1
                k = (m[0] + a, m[1] + b, m[2] + c)
                v = T * sc
                accb[k] = accb[k] + v if k in accb else v
        accb[target] = accb[target] - 1 if target in accb else FL.el(-1)
        return sum(1 for c in accb.values() if c)

    res["p4_corrupt_certificate_coefficient_residual_terms"] = total(corrupt_cert=0)
    g_eq = used[0]
    g_m = sorted(E[g_eq - 1])[0]
    res["p4_corrupt_generator_coefficient_residual_terms"] = total(corrupt_gen=(g_eq, g_m))
    res["p4_corrupt_certificate_coefficient_identity_fails"] = res["p4_corrupt_certificate_coefficient_residual_terms"] > 0
    res["p4_corrupt_generator_coefficient_identity_fails"] = res["p4_corrupt_generator_coefficient_residual_terms"] > 0
    res["status"] = "PASS" if res["identity_holds_h_equals_sum_TE"] else "FAIL"
    res["_E"] = E
    res["_FL"] = FL
    return res
