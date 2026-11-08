"""EXP-141: multi-modular cofactor certificate that Case 1 is empty (hypothesis.md).

Subcommands (all paths absolute; the work directory is scratch in the temp root, never in the repository):
  build   --work W [--caseL F]     build E''_e over L = Q[y]/(P) from EXP-140's caseL_Q.sing, with the exact
                                    field checks; writes W/eqs.json
  gate1   --work W                 specialised E'' at a root of P modulo EXP-140's five gate primes: unit, and
                                    the first four equations non-unit of dimension 4
  planted --work W                 gate 2: a planted system with a known certificate, through the same pipeline
  gate3                            gate 3: interpolation, CRT and reconstruction on random vectors
  run     --work W [--jobs N] [--batch B] [--max-primes K] [--max-hours H]
                                    modular lifts at the five roots of P for primes in [2^30, 2^31), support rule,
                                    interpolation, residues, CRT and reconstruction checkpoints (crt_recon)
  verify  --work W                 exact identity sum_e g_e E''_e = 1 in L[q] (python-flint)
  verify-singular --work W         the same identity in Singular over Q(y) with minpoly P

The Singular and crt_recon calls run in WSL (distribution Ubuntu-24.04); crt_recon is compiled from crt_recon.c
into the WSL home (see README in the verdict).
"""
import argparse
import json
import random
import re
import subprocess
import sys
import threading
import time
from array import array
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from math import gcd, lcm
from pathlib import Path

from flint import fmpq, fmpq_mpoly_ctx, fmpq_poly, fmpz, nmod_mat, nmod_poly

HERE = Path(__file__).resolve().parent
CASEL = HERE.parent / "EXP-140-case1-quintic-certificate" / "artifacts" / "caseL_Q.sing"
NAMES = ["q0", "q1", "q2", "q3", "q4", "q5"]
P_ASC = [26, 0, 3, 3, -1, 1]                       # P(y) = y^5 - y^4 + 3y^3 + 3y^2 + 26
A_ASC = [Fraction(-9725570295901, 12623962), Fraction(-1170753213563, 971074), Fraction(-387111042229, 12623962),
         Fraction(1578225240619, 12623962), Fraction(-469713794365, 6311981)]
GATE_PRIMES = (1021, 1031, 1033, 1049, 1061)
import os  # noqa: E402
# The WSL distribution and the compiled crt_recon (gcc -O2 crt_recon.c -lflint -lgmp inside WSL) are device
# settings, given by the environment: JCB_WSL_DISTRO and JCB_CRT_BIN (a path inside WSL).
DISTRO = os.environ.get("JCB_WSL_DISTRO", "")
CRT_BIN = os.environ.get("JCB_CRT_BIN", "")


def wsl_path(p):
    p = str(Path(p).resolve()).replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:]


def wsl(args, timeout):
    if not DISTRO:
        raise SystemExit("set JCB_WSL_DISTRO (the WSL distribution with Singular and FLINT)")
    r = subprocess.run(["wsl.exe", "-d", DISTRO, "--"] + args, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


# ---------------------------------------------------------------- field and equations

def parse_gen(gen, varnames, last):
    terms = []
    for co, rest in re.findall(r"\(([^)]*)\)((?:\*[a-z]\d?(?:\^\d+)?)*)", gen):
        mon, k = [0] * len(varnames), 0
        for name, ex in re.findall(r"\*([a-z]\d?)(?:\^(\d+))?", rest):
            if name == last:
                k = int(ex or 1)
            else:
                mon[varnames.index(name)] = int(ex or 1)
        terms.append((Fraction(co), tuple(mon), k))
    return terms


def qpoly(cs):
    return fmpq_poly([fmpq(c.numerator, c.denominator) for c in cs])


def coords(poly):
    return [Fraction(int(poly[i].p), int(poly[i].q)) for i in range(5)]


def build(work, caseL):
    text = Path(caseL).read_text(encoding="utf-8")
    gens = [g.strip() for g in text.split("ideal I=\n", 1)[1].split(";\n", 1)[0].split(",\n")]
    eqs = [parse_gen(g, NAMES, "v") for g in gens[:-1]]
    h = parse_gen(gens[-1], NAMES, "v")
    P, A = qpoly([Fraction(c) for c in P_ASC]), qpoly(A_ASC)
    fac = P.factor()
    irreducible = len(fac[1]) == 1 and fac[1][0][1] == 1 and fac[1][0][0].degree() == 5
    hA = fmpq_poly([0])
    for c, mon, k in h:
        assert not any(mon)
        hA += fmpq(c.numerator, c.denominator) * (A ** k % P)
    hA_zero = (hA % P) == 0
    print(f"P irreducible over Q: {irreducible}; h(A(y)) = 0 mod P: {hA_zero}; deg h = {max(k for *_, k in h)}")
    if not (irreducible and hA_zero):
        raise SystemExit("field checks failed")
    maxk = max(k for e in eqs for *_, k in e)
    pw = [fmpq_poly([1])]
    for _ in range(maxk):
        pw.append(pw[-1] * A % P)
    out = []
    for e in eqs:
        acc = {}
        for c, mon, k in e:
            acc[mon] = acc.get(mon, fmpq_poly([0])) + fmpq(c.numerator, c.denominator) * pw[k]
        rows = [(mon, coords(poly)) for mon, poly in sorted(acc.items())]
        den = 1
        for _, cs in rows:
            for x in cs:
                den = lcm(den, x.denominator)
        ints = [(mon, [int(x * den) for x in cs]) for mon, cs in rows]
        g = 0
        for _, cs in ints:
            for x in cs:
                g = gcd(g, x)
        out.append([[list(mon), [x // g for x in cs]] for mon, cs in ints if any(cs)])
    W = Path(work)
    W.mkdir(parents=True, exist_ok=True)
    (W / "eqs.json").write_text(json.dumps({"nvars": 6, "names": NAMES, "eqs": out}), encoding="utf-8")
    digits = [max(len(str(abs(x))) for _, cs in e for x in cs) for e in out]
    print(f"wrote {W / 'eqs.json'}: {len(out)} equations, terms {[len(e) for e in out]}, max digits {digits}")


def load_eqs(work):
    d = json.loads((Path(work) / "eqs.json").read_text(encoding="utf-8"))
    return d["names"], [[(tuple(m), cs) for m, cs in e] for e in d["eqs"]]


# ---------------------------------------------------------------- modular pieces

def is_prime(n):
    return fmpz(n).is_prime()


def roots_mod(p):
    """The roots of P mod p when P has five distinct roots, else None."""
    f = nmod_poly(P_ASC, p)
    c, fs = f.factor()
    if len(fs) != 5 or any(g.degree() != 1 or m != 1 for g, m in fs):
        return None
    return sorted((-int(g[0]) * pow(int(g[1]), -1, p)) % p for g, m in fs)


def any_root_mod(p):
    for g, m in nmod_poly(P_ASC, p).factor()[1]:
        if g.degree() == 1:
            return (-int(g[0]) * pow(int(g[1]), -1, p)) % p
    return None


def specialise(eqs, r, p):
    pw = [pow(r, j, p) for j in range(5)]
    out = []
    for e in eqs:
        d = {}
        for mon, cs in e:
            val = sum(c * pw[j] for j, c in enumerate(cs)) % p
            if val:
                d[mon] = val
        out.append(d)
    return out


def fmt_poly(d, names):
    if not d:
        return "0"
    out = []
    for mon, c in d.items():
        facs = [f"{names[i]}^{x}" if x > 1 else names[i] for i, x in enumerate(mon) if x]
        out.append(f"({c})" + ("*" + "*".join(facs) if facs else ""))
    return "+".join(out)


def lift_script(p, names, specs):
    s = [f"ring R={p},({','.join(names)}),dp;", "option(redSB);", "int i; poly g; poly chk;"]
    for k, sp in enumerate(specs, 1):
        s.append(f"ideal I{k}=\n" + ",\n".join(fmt_poly(d, names) for d in sp) + ";")
        s.append(f"matrix T{k}=lift(I{k},ideal(1));")
        s.append(f'"ROOT {k}";')
        s.append(f"chk=0; for(i=1;i<=ncols(I{k});i++){{ chk=chk+T{k}[i,1]*I{k}[i]; }}")
        s.append(f'"CHK "+string(chk);')
        s.append(f"for(i=1;i<=nrows(T{k});i++){{ g=T{k}[i,1]; while(g!=0){{ "
                 f'string(i)+" "+string(leadexp(g))+" "+string(leadcoef(g)); g=g-lead(g); }} }}')
        s.append(f"kill T{k}; kill I{k};")
    s.append("quit;")
    return "\n".join(s) + "\n"


def parse_lift(text, p, nroots):
    per, chk, cur = [dict() for _ in range(nroots)], [False] * nroots, -1
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("ROOT "):
            cur = int(line[5:]) - 1
        elif line.startswith("CHK "):
            chk[cur] = line[4:].strip() == "1"
        elif line:
            i, e, c = line.split(" ")
            per[cur][(int(i), tuple(int(x) for x in e.split(",")))] = int(c) % p
    return per, chk


def interpolate(vals, roots, p, keys):
    """vals[k][key] at root roots[k] -> residues, key-major, coordinate-minor (5 per key)."""
    V = nmod_mat(5, 5, [pow(r, j, p) for r in roots for j in range(5)], p)
    Vi = V.inv()
    n = len(keys)
    G = nmod_mat(5, n, [vals[k].get(key, 0) for k in range(5) for key in keys], p)
    C = Vi * G
    ent = [int(x) for x in C.entries()]
    out = array("I", [0]) * (5 * n)
    for j in range(5):
        row = ent[j * n:(j + 1) * n]
        out[j::5] = array("I", row)
    return out


def keyset_ok(per, ref_keys, ref_counts):
    for d in per:
        if not set(d) <= ref_keys:
            return False, "support outside the reference"
    agree = 0
    for d in per:
        cnt = {}
        for i, _ in d:
            cnt[i] = cnt.get(i, 0) + 1
        agree += cnt == ref_counts
    if agree < 3:
        return False, "term counts differ at the majority of roots"
    return True, ""


# ---------------------------------------------------------------- run

class Runner:
    def __init__(self, work, names, eqs, lo, hi):
        self.W = Path(work)
        (self.W / "res").mkdir(parents=True, exist_ok=True)
        (self.W / "sing").mkdir(parents=True, exist_ok=True)
        self.names, self.eqs, self.lo, self.hi = names, eqs, lo, hi
        self.lock = threading.Lock()
        self.ref = None
        kf = self.W / "keys.json"
        if kf.exists():
            keys = [(i, tuple(m)) for i, m in json.loads(kf.read_text())]
            self.set_ref(keys)
        self.done = set()
        log = self.W / "processed.log"
        if log.exists():
            self.done = {int(l.split()[0]) for l in log.read_text().splitlines() if l.strip()}

    def set_ref(self, keys):
        self.keys = keys
        self.ref = set(keys)
        self.ref_counts = {}
        for i, _ in keys:
            self.ref_counts[i] = self.ref_counts.get(i, 0) + 1

    def primes(self):
        p = self.hi
        while p >= self.lo:
            if p not in self.done and is_prime(p):
                rs = roots_mod(p)
                if rs:
                    yield p, rs
            p -= 2 if p % 2 else 1

    def lift(self, p, rs):
        specs = [specialise(self.eqs, r, p) for r in rs]
        f = self.W / "sing" / f"{p}.sing"
        f.write_text(lift_script(p, self.names, specs), encoding="utf-8", newline="\n")
        code, out, err = wsl(["Singular", "-q", wsl_path(f)], timeout=1800)
        f.unlink()
        if code != 0:
            return None, f"Singular exit {code}: {err.strip()[:200]}"
        per, chk = parse_lift(out, p, len(rs))
        if not all(chk):
            return None, "lift check failed"
        return per, ""

    def record(self, p, status):
        with self.lock:
            with open(self.W / "processed.log", "a", encoding="utf-8") as fh:
                fh.write(f"{p} {status}\n")
            self.done.add(p)

    def one(self, p, rs):
        try:
            return self._one(p, rs)
        except Exception as exc:                    # a failed prime is discarded, never fatal
            self.record(p, f"discard error {type(exc).__name__}: {str(exc)[:120]}")
            return False

    def _one(self, p, rs):
        per, why = self.lift(p, rs)
        if per is None:
            self.record(p, "discard " + why)
            return False
        ok, why = keyset_ok(per, self.ref, self.ref_counts)
        if not ok:
            self.record(p, "discard " + why)
            return False
        res = interpolate(per, rs, p, self.keys)
        with open(self.W / "res" / f"{p}.bin", "wb") as fh:
            res.tofile(fh)
        with self.lock:
            with open(self.W / "primes.txt", "a", encoding="utf-8") as fh:
                fh.write(f"{p}\n")
        self.record(p, "kept")
        return True

    def establish_reference(self, gen):
        for p, rs in gen:
            per, why = self.lift(p, rs)
            if per is None:
                self.record(p, "discard " + why)
                continue
            if any(set(d) != set(per[0]) for d in per):
                self.record(p, "discard roots disagree on the support (reference search)")
                continue
            keys = sorted(per[0])
            (self.W / "keys.json").write_text(json.dumps([[i, list(m)] for i, m in keys]))
            self.set_ref(keys)
            res = interpolate(per, rs, p, keys)
            with open(self.W / "res" / f"{p}.bin", "wb") as fh:
                res.tofile(fh)
            with open(self.W / "primes.txt", "a", encoding="utf-8") as fh:
                fh.write(f"{p}\n")
            self.record(p, "kept reference")
            print(f"reference prime {p}: {len(keys)} cofactor terms, {5 * len(keys)} coordinates", flush=True)
            return
        raise SystemExit("no reference prime found")

    def kept(self):
        f = self.W / "primes.txt"
        return [int(x) for x in f.read_text().split()] if f.exists() else []

    def checkpoint(self, final_out):
        k = len(self.kept()) - 3
        if k < 1:
            return False, ""
        if not CRT_BIN:
            raise SystemExit("set JCB_CRT_BIN (path of the compiled crt_recon inside WSL)")
        code, out, err = wsl([CRT_BIN, wsl_path(self.W), str(k), wsl_path(final_out)], timeout=7200)
        line = (out.strip() or err.strip()).splitlines()[-1] if (out.strip() or err.strip()) else ""
        return code == 0, line


def run(args):
    names, eqs = load_eqs(args.work)
    R = Runner(args.work, names, eqs, 2 ** 30, 2 ** 31 - 1)
    gen = R.primes()
    if R.ref is None:
        R.establish_reference(gen)
    t0 = time.time()
    out = Path(args.work) / "cert.txt"
    with ThreadPoolExecutor(args.jobs) as ex:
        while True:
            batch = []
            for p, rs in gen:
                batch.append((p, rs))
                if len(batch) == args.batch:
                    break
            if not batch:
                print("prime range exhausted", flush=True)
                return 1
            kept_now = sum(ex.map(lambda t: R.one(*t), batch))
            nk = len(R.kept())
            ok, line = R.checkpoint(out)
            hours = (time.time() - t0) / 3600
            print(f"[{hours:.2f} h] batch {len(batch)} kept {kept_now}; total kept {nk}; {line}", flush=True)
            if ok:
                print(f"CHECKPOINT PASSED with {nk - 3} primes; certificate candidate {out}", flush=True)
                return 0
            if nk >= args.max_primes or hours >= args.max_hours:
                print("BUDGET EXHAUSTED", flush=True)
                return 1


# ---------------------------------------------------------------- verification

def load_cert(work):
    W = Path(work)
    keys = [(i, tuple(m)) for i, m in json.loads((W / "keys.json").read_text())]
    vals = [Fraction(x) for x in (W / "cert.txt").read_text().split()]
    assert len(vals) == 5 * len(keys)
    cof = {}
    for n, (i, mon) in enumerate(keys):
        cof.setdefault(i - 1, {})[mon] = vals[5 * n:5 * n + 5]
    return cof


def verify(args):
    names, eqs = load_eqs(args.work)
    cof = load_cert(args.work)
    ctx = fmpq_mpoly_ctx.get(tuple(names), "degrevlex")

    def coord_poly(d, j):
        return ctx.from_dict({mon: fmpq(Fraction(cs[j]).numerator, Fraction(cs[j]).denominator)
                              for mon, cs in d.items() if cs[j]})

    t0 = time.time()
    S = [ctx.from_dict({}) for _ in range(9)]
    for e, eq in enumerate(eqs):
        if e not in cof:
            continue
        Ed = {mon: cs for mon, cs in eq}
        G = [coord_poly(cof[e], i) for i in range(5)]
        E = [coord_poly(Ed, j) for j in range(5)]
        for i in range(5):
            if G[i].is_zero():
                continue
            for j in range(5):
                if not E[j].is_zero():
                    S[i + j] += G[i] * E[j]
        print(f"  equation {e + 1}: cofactor terms {len(cof[e])}, {time.time() - t0:.1f} s", flush=True)
    for k in range(8, 4, -1):                       # y^5 = y^4 - 3 y^3 - 3 y^2 - 26
        S[k - 1] += S[k]
        S[k - 2] += -3 * S[k]
        S[k - 3] += -3 * S[k]
        S[k - 5] += -26 * S[k]
        S[k] = ctx.from_dict({})
    one = S[0].is_one() and all(S[k].is_zero() for k in range(1, 5))
    print(f"IDENTITY sum g_e E''_e = 1 in L[q]: {one} ({time.time() - t0:.1f} s; equations used {sorted(e + 1 for e in cof)})")
    return 0 if one else 1


def lpoly(cs):
    parts = []
    for j, c in enumerate(cs):
        c = Fraction(c)
        if c:
            cstr = str(c.numerator) if c.denominator == 1 else f"{c.numerator}/{c.denominator}"
            parts.append(f"({cstr})" + (f"*y^{j}" if j > 1 else ("*y" if j == 1 else "")))
    return "(" + ("+".join(parts) if parts else "0") + ")"


def verify_singular(args):
    names, eqs = load_eqs(args.work)
    cof = load_cert(args.work)
    W = Path(args.work)
    f = W / "verify.sing"

    def poly(d):
        out = []
        for mon, cs in d.items():
            facs = [f"{names[i]}^{x}" if x > 1 else names[i] for i, x in enumerate(mon) if x]
            out.append(lpoly(cs) + ("*" + "*".join(facs) if facs else ""))
        return "+".join(out) if out else "0"

    lines = [f"ring R=(0,y),({','.join(names)}),dp;", "minpoly=y^5-y^4+3*y^3+3*y^2+26;", "poly S=0;"]
    for e, eq in enumerate(eqs):
        if e not in cof:
            continue
        lines.append(f"poly E={poly({m: cs for m, cs in eq})};")
        lines.append(f"poly G={poly(cof[e])};")
        lines.append("S=S+G*E; kill E; kill G;")
    lines += ['"IDENTITY "+string(S==1);', "quit;"]
    f.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    code, out, err = wsl(["Singular", "-q", wsl_path(f)], timeout=6 * 3600)
    print(out.strip()[-500:], err.strip()[-300:])
    return 0 if "IDENTITY 1" in out else 1


# ---------------------------------------------------------------- gates

def gate1(args):
    names, eqs = load_eqs(args.work)
    ok = True
    for p in GATE_PRIMES:
        r = any_root_mod(p)
        if r is None:
            print(f"p={p}: P has no root mod p")
            ok = False
            continue
        sp = specialise(eqs, r, p)
        for label, sub, want in (("gate", sp, "UNIT"), ("control", sp[:4], "NONUNIT")):
            s = (f"ring R={p},({','.join(names)}),dp;\noption(redSB);\nideal I=\n" +
                 ",\n".join(fmt_poly(d, names) for d in sub) + ";\nideal J=std(I);\n"
                 "if(size(J)==1 && deg(J[1])==0){ \"UNIT\"; } else { \"NONUNIT DIM=\"+string(dim(J)); }\nquit;\n")
            f = Path(args.work) / f"gate1_{label}_{p}.sing"
            f.write_text(s, encoding="utf-8", newline="\n")
            code, out, err = wsl(["Singular", "-q", wsl_path(f)], timeout=600)
            f.unlink()
            res = out.strip()
            good = res == "UNIT" if want == "UNIT" else res == "NONUNIT DIM=4"
            ok &= good
            print(f"{label} p={p} root={r}: {res} {'PASS' if good else 'FAIL'}")
    print("GATE 1", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def planted(args):
    """Three polynomials over L in q0..q2 with 1 in their ideal by construction."""
    rnd = random.Random(141)
    P = qpoly([Fraction(c) for c in P_ASC])
    names = ["q0", "q1", "q2"]

    def rand_el(b):
        return fmpq_poly([fmpq(rnd.randint(-b, b), rnd.randint(1, 50)) for _ in range(5)])

    def rand_poly(deg, b):
        d = {}
        for _ in range(6):
            mon = [0, 0, 0]
            for _ in range(rnd.randint(0, deg)):
                mon[rnd.randrange(3)] += 1
            d[tuple(mon)] = d.get(tuple(mon), fmpq_poly([0])) + rand_el(b)
        return d

    def mul(a, b):
        d = {}
        for ma, ca in a.items():
            for mb, cb in b.items():
                m = tuple(x + y for x, y in zip(ma, mb))
                d[m] = (d.get(m, fmpq_poly([0])) + ca * cb) % P
        return d

    def add(a, b, s=1):
        d = dict(a)
        for m, c in b.items():
            d[m] = (d.get(m, fmpq_poly([0])) + s * c) % P
        return d

    f1, f2 = rand_poly(2, 10 ** 12), rand_poly(2, 10 ** 12)
    a1, a2 = rand_poly(1, 10 ** 6), rand_poly(1, 10 ** 6)
    f3 = add(add({(0, 0, 0): fmpq_poly([1])}, mul(a1, f1), -1), mul(a2, f2), -1)
    out = []
    for f in (f1, f2, f3):
        rows = [(m, coords(c)) for m, c in sorted(f.items()) if not c.is_zero()]
        den = 1
        for _, cs in rows:
            for x in cs:
                den = lcm(den, x.denominator)
        out.append([[list(m), [int(x * den) for x in cs]] for m, cs in rows])
    W = Path(args.work)
    W.mkdir(parents=True, exist_ok=True)
    (W / "eqs.json").write_text(json.dumps({"nvars": 3, "names": names, "eqs": out}), encoding="utf-8")
    print("planted system written; running the pipeline")
    ns = argparse.Namespace(work=args.work, jobs=8, batch=8, max_primes=400, max_hours=1.0)
    if run(ns) != 0:
        print("GATE 2 FAIL (no checkpoint)")
        return 1
    v = verify(argparse.Namespace(work=args.work))
    v2 = verify_singular(argparse.Namespace(work=args.work))
    print("GATE 2", "PASS" if v == 0 and v2 == 0 else "FAIL")
    return 0 if v == 0 and v2 == 0 else 1


def gate3(args):
    rnd = random.Random(3)
    p = 2 ** 31 - 1
    while True:
        p -= 2
        if is_prime(p) and roots_mod(p):
            break
    rs = roots_mod(p)
    keys = [(1, (k,)) for k in range(50)]
    true = {key: [rnd.randint(0, p - 1) for _ in range(5)] for key in keys}
    vals = [{key: sum(c * pow(r, j, p) for j, c in enumerate(true[key])) % p for key in keys} for r in rs]
    res = interpolate(vals, rs, p, keys)
    ok_i = all(list(res[5 * n:5 * n + 5]) == true[key] for n, key in enumerate(keys))
    print(f"interpolation on 50 random keys mod {p}: {'PASS' if ok_i else 'FAIL'}")
    print("CRT and reconstruction are exercised end to end by gate 2 (planted).")
    return 0 if ok_i else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--work")
    ap.add_argument("--caseL", default=str(CASEL))
    ap.add_argument("--jobs", type=int, default=24)
    ap.add_argument("--batch", type=int, default=96)
    ap.add_argument("--max-primes", type=int, default=6000)
    ap.add_argument("--max-hours", type=float, default=12.0)
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.work, a.caseL)
        return 0
    return {"gate1": gate1, "planted": planted, "gate3": gate3, "run": run, "verify": verify,
            "verify-singular": verify_singular}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
