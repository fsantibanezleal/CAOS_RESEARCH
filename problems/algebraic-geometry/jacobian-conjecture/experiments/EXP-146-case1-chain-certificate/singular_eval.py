"""EXP-146 M9: the second implementation. Singular 4.3.2 (WSL) reads the exact inputs (coordinate vectors over
Z[y]/(P)) and the recorded SLP, evaluates everything at (p1, r1) with its own arithmetic (evaluation of the
coordinate vectors at r1, the coordinate changes, resultants, degree-drop factors, exact divisions) and prints a
digest of every member image and every final constant. compare() checks them against python-flint's, up to sign.

Digest of a member: number of terms, degree in each variable of the node, and the value at two fixed points of F_p.
A polynomial is compared up to sign (the two resultants may differ by a sign): both values flip together.
"""
import re
import subprocess
from pathlib import Path

import chaincert as cc


def _sid(k, mid):
    return f"n{k}_" + re.sub(r"\W", "_", mid)


def _num(v):
    return f"({int(v)})" if int(v) < 0 else str(int(v))


def _bigexpr(vec):
    return " + ".join(f"{_num(c)}*RR^{i}" for i, c in enumerate(vec)) or "0"


def wsl_path(p):
    p = str(Path(p).resolve()).replace("\\", "/")
    return "/mnt/" + p[0].lower() + p[2:]


def build_script(records, root_terms, root_order, prime):
    """records: node records in creation order (parents first). root_terms: {input id: [(exps over root_order,
    coordinate vector)]}. Returns the Singular script text."""
    p = prime.p
    wnames = []
    for r in records:
        for v in r["order"]:
            if v not in root_order and v not in wnames:
                wnames.append(v)
    allvars = list(root_order) + wnames
    L = []
    L.append(f"ring R = {p}, ({','.join(allvars)}), dp;")
    L.append(f"bigint RR = {prime.r};")
    for v in allvars:
        L.append(f"intvec wv_{v} = " + ",".join("1" if u == v else "0" for u in allvars) + ";")
    idx_of = {r["id"]: k for k, r in enumerate(records)}
    uid = [0]

    def nu():
        uid[0] += 1
        return uid[0]
    for k, r in enumerate(records):
        order = r["order"]
        n = len(order)
        pts = cc.digest_points(n, p)
        L.append(f"// ---- node {r['id']} ({r['kind']}, order {order})")
        tr = r.get("transform")
        if r["parent"] is None:
            for mid in r["inputs"]:
                terms = []
                for exps, cs in root_terms[mid]:
                    mono = "*".join(f"{v}^{e}" for v, e in zip(root_order, exps) if e) or "1"
                    terms.append(f"number(bigint({_bigexpr(cs)}))*{mono}")
                L.append(f"poly {_sid(k, mid)} = " + " + ".join(terms) + ";")
        else:
            pk = idx_of[r["parent"]]
            v, w = tr["v"], tr["w"]
            L.append(f"bigint ta{k} = {_bigexpr(tr['a'])}; bigint tb{k} = {_bigexpr(tr['b'])};")
            L.append(f"number aa{k} = number(ta{k}); number bb{k} = number(tb{k}); number bi{k} = 1/bb{k};")
            for mid in r["inputs"]:
                src = _sid(pk, mid)
                u = nu()
                L.append(f"int dd{u} = deg({src}, wv_{v});")
                if tr.get("set_w_zero"):
                    # the child "w = 0": transform, then w := 0
                    L.append(f"poly {_sid(k, mid)} = subst(subst({src}, {v}, ({w} - aa{k})*bi{k})*bb{k}^dd{u}, {w}, 0);")
                else:
                    L.append(f"poly {_sid(k, mid)} = subst({src}, {v}, ({w} - aa{k})*bi{k})*bb{k}^dd{u};")
        if "last" not in r or r.get("last") is None:
            continue

        def digest(mid, sym):
            degs = ",".join(f"\" + string(deg({sym}, wv_{v})) + \"" for v in order)
            evs = []
            for pt in pts:
                e = sym
                for v, a in zip(order, pt):
                    e = f"subst({e}, {v}, {a})"
                evs.append(f"string({e})")
            L.append(f"print(\"DIG {r['id']} {mid} \" + string(size({sym})) + \" {degs} \" + {evs[0]} + \" \" + {evs[1]});")

        for mid in r["inputs"]:
            digest(mid, _sid(k, mid))
        for st in r["steps"]:
            x, nn = st["x"], st["n"]
            P = _sid(k, st["pivot"])
            L.append(f"if (deg({P}, wv_{x}) != {nn}) {{ print(\"BAD_PIVOT_DEGREE {r['id']} {st['pivot']}\"); }}")
            su = nu()
            L.append(f"matrix cm_{su} = coeffs({P}, {x}); poly lcP_{su} = cm_{su}[nrows(cm_{su}),1];")
            for e in st["members"]:
                if e["kind"] == "pass":
                    continue
                F = _sid(k, e["id"])
                m = e["m"]
                hu = nu()
                L.append(f"poly hh{hu} = resultant({F}, {P}, {x}); int mp{hu} = deg({F}, wv_{x});")
                L.append(f"if (mp{hu} < {m}) {{ hh{hu} = hh{hu} * lcP_{su}^({m} - mp{hu}); "
                         f"if (({nn} * ({m} - mp{hu})) mod 2 == 1) {{ hh{hu} = -hh{hu}; }} }}")
                if e["out"] is None:
                    L.append(f"print(\"ZERO {r['id']} {e['id']} \" + string(hh{hu} == 0));")
                else:
                    sym = _sid(k, e["out"])
                    L.append(f"poly {sym} = hh{hu};")
                    digest(e["out"], sym)
        last = r["last"]
        x = last["x"]
        if last["constant_member"] is not None:
            sym = _sid(k, last["constant_member"])
            L.append(f"print(\"CONST {r['id']} {last['constant_member']} \" + string({sym}));")
            continue
        for u in last["members"]:
            src = _sid(k, u["id"])
            sym = _sid(k, "V_" + u["id"])
            if u["L"]:
                L.append(f"poly {sym} = {src} / {x}^{u['L']};")
                L.append(f"if ({sym} * {x}^{u['L']} != {src}) {{ print(\"INEXACT_DIVISION {r['id']} {u['id']}\"); }}")
            else:
                L.append(f"poly {sym} = {src};")
            digest("V_" + u["id"], sym)
        if last["pivot"] is None:
            continue
        PV = _sid(k, "V_" + last["pivot"])
        nn = last["n"]
        L.append(f"matrix cv_{k} = coeffs({PV}, {x}); poly lcV_{k} = cv_{k}[nrows(cv_{k}),1];")
        for pr in last["pairs"]:
            F = _sid(k, "V_" + pr["i"])
            if pr["constant"]:
                L.append(f"print(\"CONST {r['id']} {pr['i']} \" + string({F}));")
                continue
            m = pr["m"]
            hu = nu()
            L.append(f"poly hh{hu} = resultant({F}, {PV}, {x}); int mp{hu} = deg({F}, wv_{x});")
            L.append(f"if (mp{hu} < {m}) {{ hh{hu} = hh{hu} * lcV_{k}^({m} - mp{hu}); "
                     f"if (({nn} * ({m} - mp{hu})) mod 2 == 1) {{ hh{hu} = -hh{hu}; }} }}")
            L.append(f"print(\"CONST {r['id']} {pr['i']} \" + string(hh{hu}));")
    L.append("quit;")
    return "\n".join(L) + "\n"


def run_singular(script_text, workdir, timeout=7200, name="check"):
    wd = Path(workdir)
    wd.mkdir(parents=True, exist_ok=True)
    sp = wd / f"{name}.sing"
    sp.write_text(script_text, encoding="utf-8")
    r = subprocess.run(["wsl", "-e", "bash", "-lc", f"Singular -q {wsl_path(sp)}"], capture_output=True,
                       text=True, timeout=timeout)
    return r.returncode, r.stdout, r.stderr


def _modp(s, p):
    return int(s.strip()) % p


def compare(records, output, prime):
    """Compare Singular's printed digests and constants with python-flint's recorded ones, up to sign."""
    p = prime.p
    sing_dig, sing_const, flags = {}, {}, []
    for line in output.splitlines():
        t = line.split()
        if not t or t[0].startswith("//"):
            continue
        if t[0] == "DIG":
            sing_dig[(t[1], t[2])] = (int(t[3]), [int(x) for x in t[4].split(",")], _modp(t[5], p), _modp(t[6], p))
        elif t[0] == "CONST":
            sing_const[(t[1], t[2])] = _modp(t[3], p)
        elif t[0] in ("ZERO",):
            if t[3] != "1":
                flags.append(" ".join(t))
        else:
            flags.append(line.strip())
    stats = {"digests_compared": 0, "digest_mismatches": [], "constants_compared": 0, "constant_mismatches": [],
             "singular_flags": flags, "sign_flips": 0, "missing": []}
    for r in records:
        if r.get("last") is None:
            continue
        mem = r["members"]
        for mid, d in mem.items():
            if d.get("dropped"):
                continue
            key = (r["id"], mid)
            if key not in sing_dig:
                stats["missing"].append(list(key))
                continue
            terms, degs, e1, e2 = sing_dig[key]
            dg = d["digest"]
            same = terms == dg["terms"] and degs == dg["degrees"]
            f1, f2 = dg["eval"]
            if same and (e1, e2) == (f1 % p, f2 % p):
                pass
            elif same and (e1, e2) == ((-f1) % p, (-f2) % p):
                stats["sign_flips"] += 1
            else:
                same = False
            stats["digests_compared"] += 1
            if not same:
                stats["digest_mismatches"].append(list(key))
        for pr in r["last"]["pairs"]:
            key = (r["id"], pr["i"])
            if key not in sing_const:
                stats["missing"].append(list(key))
                continue
            stats["constants_compared"] += 1
            c = pr["c"] % p
            s = sing_const[key]
            if s not in (c, (-c) % p):
                stats["constant_mismatches"].append(list(key))
        cm = r["last"]["constant_member"]
        if cm is not None:
            stats["constants_compared"] += 1
    stats["pass"] = (not flags and not stats["digest_mismatches"] and not stats["constant_mismatches"]
                     and not stats["missing"] and stats["digests_compared"] > 0)
    return stats
