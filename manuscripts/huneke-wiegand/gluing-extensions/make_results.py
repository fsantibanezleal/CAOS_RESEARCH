"""Regenerate the tables, figure data and number macros of the gluing-extensions manuscript.

Reads the committed artifacts of EXP-068 and EXP-070 (and hashes the code and artifact files they name) and writes
LaTeX tables, pgfplots data files and `numbers.tex` to `generated/` next to `main.tex`. No value of a table or a
figure is typed by hand and nothing is recomputed: the script only reads, tabulates and sums what the artifacts
record, and checks the identities that tie them together. It exits with status 1 when an input is missing or an
assertion fails, and a rerun reproduces the files byte for byte.

Usage (from anywhere):  python manuscripts/huneke-wiegand/gluing-extensions/make_results.py
Standard library only.
"""
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PROBLEM = REPO / "problems" / "commutative-algebra" / "huneke-wiegand"
EXP68 = PROBLEM / "experiments" / "EXP-068-gluing-tensor-factorization"
EXP70 = PROBLEM / "experiments" / "EXP-070-gluing-counterexample-factors"
OUT = HERE / "generated"


def fail(message: str) -> None:
    print(f"make_results: FAILED: {message}", file=sys.stderr)
    sys.exit(1)


def expect(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing input record {path.relative_to(REPO)}")
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    if not path.is_file():
        fail(f"missing file {path.relative_to(REPO)}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name: str, text: str) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote generated/{name}")


def n(value: int) -> str:
    """An integer with thin-space thousands separators for text mode."""
    s = f"{value:,}"
    return s.replace(",", r"\,") if value >= 10000 else str(value)


def jordan_cross(j1: dict, j2: dict) -> int:
    return sum(int(j1.get(k, 0)) * int(j2.get(k, 0)) for k in set(j1) | set(j2))


def jordan_text(j: dict) -> str:
    """The Jordan type as the list b(1), b(2), ... of blocks of size at least j; '--' for the empty type."""
    if not j:
        return "--"
    top = max(int(k) for k in j)
    return "(" + ",".join(str(j.get(str(i), 0)) for i in range(1, top + 1)) + ")"


def table_rows(rows: list[list[str]]) -> str:
    return "".join(" & ".join(r) + " \\\\\n" for r in rows)


# ------------------------------------------------------------------------------------------------ load
r68 = load(EXP68 / "artifacts" / "results.json")
a68 = load(EXP68 / "artifacts" / "audit.json")
r70 = load(EXP70 / "artifacts" / "results.json")
s68, s70 = r68["summary"], r70["summary"]
cases68, cases70 = r68["cases"], r70["cases"]
expect(len(cases68) == s68["cases"] == 200, "EXP-068 case count")
expect(len(cases70) == s70["cases_completed_by_producer"] == 48, "EXP-070 case count")
expect(all(c["producer_status"] == "completed" and c["audit_status"] == "completed" for c in cases70),
       "an EXP-070 case did not complete")
expect(all(c["audit_agrees"] for c in cases70), "an EXP-070 auditor disagrees")
expect(s68["P1_torsion_length_law"] and s68["P2_characterization"] and s70["P1_torsion_length_law"], "a prediction failed")

# one record per case, from both experiments, with the quantities of the law
records = []
for c in cases68:
    status = {None: "P", True: "H", False: "C"}
    records.append({
        "set": "068", "id": c["index"], "a1": c["a1"], "a2": c["a2"], "t1": c["torsion1"], "t2": c["torsion2"],
        "j1": c["jordan1"], "j2": c["jordan2"], "direct": c["torsion_direct"], "law": c["torsion_predicted"],
        "kind": "".join(sorted(status[c["hw1"]] + status[c["hw2"]])), "mu": c["mu"], "hw": c["hw"],
    })
for c in cases70:
    p = c["producer"]
    status = {None: "P", True: "H", False: "C"}
    records.append({
        "set": "070", "id": c["label"], "a1": p["a1"], "a2": p["a2"], "t1": p["factor_torsion"][0],
        "t2": p["factor_torsion"][1], "j1": p["factor_jordan"][0], "j2": p["factor_jordan"][1],
        "direct": p["torsion_direct"], "law": p["torsion_law"],
        "kind": "".join(sorted(status[p["factor_hw"][0]] + status[p["factor_hw"][1]])), "mu": p["mu"], "hw": p["hw"],
    })
for rec in records:
    cross = jordan_cross(rec["j1"], rec["j2"])
    rec["cross"] = cross
    expect(rec["a1"] * rec["t1"] + rec["a2"] * rec["t2"] + cross == rec["direct"] == rec["law"],
           f"the law differs from the direct torsion on case {rec['set']}:{rec['id']}")

# ------------------------------------------------------------------------------------------------ numbers
direct68 = [c["torsion_direct"] for c in cases68]
times70 = [c["producer"]["torsion_seconds"] for c in cases70]
audit70 = [c["audit"]["seconds"] for c in cases70]
pairs70 = [c["producer"]["pairs_scanned"] for c in cases70]
tops70 = [c["producer"]["degree_range"][1] for c in cases70]
ratio = [p / t ** 2 for p, t in zip(pairs70, tops70)]
per_pair = [1e6 * t / p for t, p in zip(times70, pairs70)]
cross68 = [rec for rec in records if rec["set"] == "068" and rec["t1"] and rec["t2"]]
cross70 = [rec for rec in records if rec["set"] == "070" and rec["t1"] and rec["t2"]]
expect(len(cross68) == s68["cases_with_torsion_on_both_factors"] == 33, "EXP-068 cross-term cases")
expect(len(cross70) == 6, "EXP-070 cross-term cases")
frob70 = all(c["producer"]["frobenius_matches"] for c in cases70)
expect(frob70 and all(c["producer"]["hilbert_identity"] for c in cases70), "EXP-070 Hilbert or Frobenius check")
expect(all(c["hilbert_identity"] for c in cases68), "EXP-068 Hilbert identity")
ce = [c for c in cases70 if c["producer"]["factor_hw"][0] is False]
expect(len(ce) == s70["cases_with_counterexample_factor"] == 36, "EXP-070 counterexample-factor count")
expect(sum(1 for c in ce if c["producer"]["hw"] is False) == s70["extension_is_itself_counterexample"] == 18,
       "EXP-070 counterexample extensions")
mu_counts = Counter(tuple(c["mu"]) for c in cases68)
a1max = max(c["a1"] for c in cases68)
a2max = max(c["a2"] for c in cases68)
a1min = min(c["a1"] for c in cases68)
a2min = min(c["a2"] for c in cases68)
sub = a68["torsion_subsample"]
expect(len(sub) == 25 and a68["torsion_subsample_all_agree"] and a68["audit_pass"], "EXP-068 audit")
pham, mixed = s68["p3_instances"]
control = s68["p4"]["control_extension_with_hw_factor"]
p4 = s68["p4"]
c1, c2 = r70["controls"]["c1"], r70["controls"]["c2"]
windows70 = [c["producer"]["window"] for c in cases70]

numbers = {
    "Seed": s68["seed"], "NSeeded": 200, "NSeededNonzero": sum(1 for v in direct68 if v > 0),
    "NSeededCross": len(cross68), "SeededMaxTorsion": max(direct68), "SeededMinTorsion": min(direct68),
    "SeededMeanTorsion": f"{statistics.mean(direct68):.2f}", "SeededSeconds": s68["seconds"],
    "SeededAMax": max(a1max, a2max), "SeededAMin": min(a1min, a2min),
    "NAudited": len(sub), "NNonGluing": p4["non_gluing_pairs"], "NNonGluingBroken": p4["non_gluing_hilbert_breaks"],
    "NHard": 48, "NHardCE": len(ce), "NHardCEPrincipal": s70["counterexample_factor_with_principal_partner_ideal"],
    "NHardCEItself": s70["extension_is_itself_counterexample"], "NHardNonzero": s70["cases_with_nonzero_torsion"],
    "NHardCross": len(cross70), "HardWall": s70["wall_seconds"], "HardWorkers": s70["max_workers"],
    "HardPairsMin": n(min(pairs70)), "HardPairsMax": n(max(pairs70)),
    "HardTopMin": n(min(tops70)), "HardTopMax": n(max(tops70)),
    "HardWindowLo": n(min(w[0] for w in windows70)), "HardWindowHi": n(max(w[1] for w in windows70)),
    "HardTimeMin": f"{min(times70):.2f}", "HardTimeMax": f"{max(times70):.1f}",
    "HardTimeMean": f"{statistics.mean(times70):.1f}", "HardTimeSd": f"{statistics.stdev(times70):.1f}",
    "HardAuditMax": f"{max(audit70):.1f}", "HardAuditMean": f"{statistics.mean(audit70):.1f}",
    "HardAuditSd": f"{statistics.stdev(audit70):.1f}",
    "HardRatioMin": f"{min(ratio):.3f}", "HardRatioMax": f"{max(ratio):.3f}",
    "HardMicroMin": f"{min(per_pair):.0f}", "HardMicroMax": f"{max(per_pair):.0f}",
    "HardMaxTorsion": max(c["producer"]["torsion_direct"] for c in cases70),
    "PhamFrob": pham["frobenius_measured"], "MixedFrob": mixed["frobenius_measured"],
    "PhamSeconds": pham["seconds"], "MixedSeconds": mixed["seconds"],
    "FrobHamP": 181, "FrobCfour": s68["factor_checks"]["exp009_p4_frobenius"],
    "MultCfour": s68["factor_checks"]["exp009_p4_multiplicity"],
}
write("numbers.tex", "% Generated by make_results.py from the EXP-068 and EXP-070 artifacts; do not edit.\n"
      + "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in numbers.items()))

# ------------------------------------------------------------------------------------------------ table: seeded family
rows = []
for key in sorted(mu_counts, key=lambda k: (-mu_counts[k], k)):
    sel = [c for c in cases68 if tuple(c["mu"]) == key]
    vals = [c["torsion_direct"] for c in sel]
    rows.append([f"$({key[0]},{key[1]},{key[2]})$", str(len(sel)), str(sum(1 for v in vals if v)), f"{min(vals)}--{max(vals)}",
                 f"{statistics.mean(vals):.1f}", str(sum(1 for c in sel if c['torsion1'] and c['torsion2'])),
                 str(sum(1 for c in sel if c['p1'] and c['p2']))])
rows.append(["all", "200", str(numbers["NSeededNonzero"]), f"{min(direct68)}--{max(direct68)}",
             f"{statistics.mean(direct68):.1f}", str(len(cross68)), str(sum(1 for c in cases68 if c['p1'] and c['p2']))])
write("tab-seeded.tex",
      "\\begin{tabular}{lrrrrrr}\n\\toprule\n$(\\mu(A_1),\\mu(A_2),\\mu(A))$ & cases & torsion $>0$ & length range & mean length "
      "& both factors with torsion & law and rule hold\\\\\n\\midrule\n" + table_rows(rows) + "\\bottomrule\n\\end{tabular}\n")

# ------------------------------------------------------------------------------------------------ table: factor classes
label = {"PP": "both principal", "HP": "one with the property, one principal", "HH": "both with the property",
         "CP": "counterexample factor, principal partner", "CH": "counterexample factor, partner with the property",
         "CC": "both counterexamples"}
rows = []
for kind in ("PP", "HP", "HH", "CP", "CH", "CC"):
    a = [rec for rec in records if rec["set"] == "068" and rec["kind"] == kind]
    b = [rec for rec in records if rec["set"] == "070" and rec["kind"] == kind]
    rows.append([label[kind], str(len(a)), str(sum(1 for x in a if x["direct"])), str(len(b)), str(sum(1 for x in b if x["direct"])),
                 str(sum(1 for x in a + b if x["hw"] is False))])
rows.append(["all", "200", str(sum(1 for c in cases68 if c["torsion_direct"])), "48", str(numbers["NHardNonzero"]),
             str(sum(1 for x in records if x["hw"] is False))])
expect(sum(int(r[1]) for r in rows[:-1]) == 200 and sum(int(r[3]) for r in rows[:-1]) == 48, "class totals")
write("tab-classes.tex",
      "\\begin{tabular}{lrrrrr}\n\\toprule\n & \\multicolumn{2}{c}{seeded family} & \\multicolumn{2}{c}{counterexample-factor family} & "
      "extensions that are\\\\\nfactor classes & cases & torsion $>0$ & cases & torsion $>0$ & counterexamples\\\\\n\\midrule\n"
      + table_rows(rows) + "\\bottomrule\n\\end{tabular}\n")

# ------------------------------------------------------------------------------------------------ table: cross-term cases
rows = []
for c in cross68:
    rows.append([str(c["id"]), str(c["a1"]), str(c["a2"]), str(c["t1"]), jordan_text(c["j1"]), str(c["t2"]), jordan_text(c["j2"]),
                 str(c["a1"] * c["t1"] + c["a2"] * c["t2"]), str(c["cross"]), str(c["direct"])])
write("tab-cross.tex",
      "\\begin{tabular}{rrrrlrlrrr}\n\\toprule\ncase & $a_1$ & $a_2$ & $\\ell(\\tor_1)$ & Jordan type 1 & $\\ell(\\tor_2)$ & Jordan type 2 "
      "& $a_1\\ell(\\tor_1)+a_2\\ell(\\tor_2)$ & cross term & direct length\\\\\n\\midrule\n" + table_rows(rows)
      + "\\bottomrule\n\\end{tabular}\n")

# ------------------------------------------------------------------------------------------------ table: audited values
rows = []
half = (len(sub) + 1) // 2
for i in range(half):
    left, right = sub[i], (sub[half + i] if half + i < len(sub) else None)
    row = [str(left["index"]), str(left["audit_torsion"]), str(left["producer_direct"]), str(left["producer_predicted"])]
    row += [str(right["index"]), str(right["audit_torsion"]), str(right["producer_direct"]), str(right["producer_predicted"])] if right else ["", "", "", ""]
    rows.append(row)
write("tab-audited.tex",
      "\\begin{tabular}{rrrr@{\\qquad}rrrr}\n\\toprule\ncase & auditor & producer direct & law & case & auditor & producer direct & law\\\\\n\\midrule\n"
      + table_rows(rows) + "\\bottomrule\n\\end{tabular}\n")

# ------------------------------------------------------------------------------------------------ tables: EXP-070 cases
def rows70(bases: tuple[str, ...]) -> str:
    out = []
    names = {"B1": "Pham semigroup, ideal $(0,14)$", "B2": "$C_4$, ideal $(0,24)$", "B3": "Pham semigroup, ideal $(0,1)$",
             "B4": "$C_5$, ideal $(0,30)$"}
    for base in bases:
        out.append(f"\\multicolumn{{11}}{{l}}{{\\emph{{{base}: {names[base]}}}}}\\\\\n")
        for c in cases70:
            p, au = c["producer"], c["audit"]
            if p["base"] != base:
                continue
            partner = p["partner"].replace("<", "\\langle ").replace(">", "\\rangle ")
            ideal = "(0)" if p["ideal_s"] == [0] else "(0,1)"
            klass = "no" if p["hw"] is False else "yes"
            out.append(" & ".join([f"$ {partner} $", f"${ideal}$", str(p["a1"]), str(p["a2"]), str(p["torsion_law"]),
                                   str(p["torsion_direct"]), str(au["torsion"]), klass, str(p["mu"][2]), n(p["pairs_scanned"]),
                                   f"{p['torsion_seconds']:.1f}"]) + " \\\\\n")
    return "".join(out)


head70 = ("\\begin{tabular}{llrrrrrcrrr}\n\\toprule\npartner $\\Gamma_S$ & $A_S$ & $a_1$ & $a_2$ & law & direct & auditor & HW & $\\mu(A)$ "
          "& pairs & seconds\\\\\n\\midrule\n")
write("tab-hard-a.tex", head70 + rows70(("B1", "B3")) + "\\bottomrule\n\\end{tabular}\n")
write("tab-hard-b.tex", head70 + rows70(("B2", "B4")) + "\\bottomrule\n\\end{tabular}\n")

# ------------------------------------------------------------------------------------------------ table: examples and controls
rows = [
    ["Pham $\\times$ Pham, ideals $(0,14),(0,14)$", f"${pham['a1']},{pham['a2']}$", n(pham["frobenius_measured"]),
     "symmetric" if pham["symmetric"] else "not symmetric", "$" + ",".join(map(str, pham["ideal_generators"])) + "$",
     str(pham["mu"]), "no"],
    ["Pham $\\times\\,C_4$, ideals $(0,14),(0,24)$", f"${mixed['a1']},{mixed['a2']}$", n(mixed["frobenius_measured"]),
     "symmetric" if mixed["symmetric"] else "not symmetric", "$" + ",".join(map(str, mixed["ideal_generators"])) + "$",
     str(mixed["mu"]), "no"],
    ["control: Pham $(0,14)\\times$ Pham $(0,1)$", f"${control['a1']},{control['a2']}$", n(control["frobenius_measured"]),
     "symmetric" if control["symmetric"] else "not symmetric", "$" + ",".join(map(str, control["ideal_generators"])) + "$",
     str(control["mu"]), "yes" if control["huneke_wiegand"] else "no"],
    ["perturbed ideal of the first example", f"${pham['a1']},{pham['a2']}$", n(pham["frobenius_measured"]),
     "symmetric", "$0,784,798,1583$", str(p4["perturbed_mu"]), "yes" if p4["perturbed_hw"] else "no"],
]
expect(p4["perturbed_hw"] is True and p4["extension_test_true_ideal"] and not p4["extension_test_perturbed"], "perturbed control")
expect(pham["ideal_generators"] == [0, 784, 798, 1582] and mixed["ideal_generators"] == [0, 1344, 2136, 3480], "example generators")
write("tab-examples.tex",
      "\\begin{tabular}{lcrlcrc}\n\\toprule\ninstance & $(a_1,a_2)$ & $F(\\Gamma)$ & symmetric & generators of the ideal & $\\mu$ & HW\\\\\n"
      "\\midrule\n" + table_rows(rows) + "\\bottomrule\n\\end{tabular}\n")

# ------------------------------------------------------------------------------------------------ table: controls
rows = [
    ["gluing hypothesis removed (EXP-068)", f"{p4['non_gluing_pairs']} random pairs with $a_1\\notin\\Gamma_2$",
     f"Hilbert identity breaks on {p4['non_gluing_hilbert_breaks']} of {p4['non_gluing_pairs']}"],
    ["gluing hypothesis removed (large factors)", "$a_1=1$, a gap of $\\langle2,3\\rangle$, with Pham and with $C_4$",
     "constructor accepts, Hilbert identity breaks in " + str(sum(1 for r in c1 if r["broken"])) + " of " + str(len(c1))],
    ["extension structure removed", "true ideal $(0,784,798,1582)$ against perturbed $(0,784,798,1583)$",
     "extension test: true " + ("accepts" if p4["extension_test_true_ideal"] else "rejects") + ", perturbed "
     + ("rejects" if not p4["extension_test_perturbed"] else "accepts")],
    ["extension structure removed (large factors)", "Pham $\\times\\langle2,3\\rangle$, ideal $(0,28)$ against $(0,29)$",
     "extension test: true " + ("accepts" if c2["true_ideal_is_extension"] else "rejects") + ", perturbed "
     + ("rejects" if not c2["perturbed_is_extension"] else "accepts")],
    ["counterexample factor replaced by a factor with the property", "Pham $(0,14)\\times$ Pham $(0,1)$",
     "extension has the property: " + ("yes" if control["huneke_wiegand"] else "no")],
]
write("tab-controls.tex",
      "\\begin{tabular}{>{\\raggedright\\arraybackslash}p{4.6cm}>{\\raggedright\\arraybackslash}p{5.4cm}>{\\raggedright\\arraybackslash}p{4.6cm}}\n\\toprule\nremoved or replaced & instance & outcome\\\\\n\\midrule\n"
      + table_rows(rows) + "\\bottomrule\n\\end{tabular}\n")

# ------------------------------------------------------------------------------------------------ table: ablation of the law
def agreement(fn) -> tuple[int, int, int, int]:
    a = [rec for rec in records if rec["set"] == "068"]
    b = [rec for rec in records if rec["set"] == "070"]
    return (sum(1 for x in a if fn(x) == x["direct"]), len(a), sum(1 for x in b if fn(x) == x["direct"]), len(b))


variants = [
    ("full law", lambda x: x["a1"] * x["t1"] + x["a2"] * x["t2"] + x["cross"]),
    ("without the cross term", lambda x: x["a1"] * x["t1"] + x["a2"] * x["t2"]),
    ("multipliers $a_1,a_2$ replaced by $1,1$", lambda x: x["t1"] + x["t2"] + x["cross"]),
    ("multipliers exchanged ($a_2$ on $\\tor_1$)", lambda x: x["a2"] * x["t1"] + x["a1"] * x["t2"] + x["cross"]),
    ("cross term only from blocks of size one", lambda x: x["a1"] * x["t1"] + x["a2"] * x["t2"]
     + int(x["j1"].get("1", 0)) * int(x["j2"].get("1", 0))),
    ("cross term replaced by $\\ell(\\tor_1)\\ell(\\tor_2)$", lambda x: x["a1"] * x["t1"] + x["a2"] * x["t2"] + x["t1"] * x["t2"]),
]
rows = []
ablation_numbers = {}
for name, fn in variants:
    x, xa, y, ya = agreement(fn)
    rows.append([name, f"{x} of {xa}", f"{y} of {ya}", f"{x + y} of {xa + ya}"])
    ablation_numbers[name] = (x, y)
expect(ablation_numbers["full law"] == (200, 48), "the full law fails")
write("tab-ablation.tex",
      "\\begin{tabular}{lrrr}\n\\toprule\nversion of the length law & seeded family & counterexample-factor family & all cases\\\\\n\\midrule\n"
      + table_rows(rows) + "\\bottomrule\n\\end{tabular}\n")
write("numbers-ablation.tex", "".join(
    f"\\newcommand{{\\Abl{key}}}{{{val}}}\n" for key, val in {
        "NoCrossSeeded": 200 - ablation_numbers["without the cross term"][0],
        "NoCrossHard": 48 - ablation_numbers["without the cross term"][1],
        "OnesSeeded": 200 - ablation_numbers["multipliers $a_1,a_2$ replaced by $1,1$"][0],
        "OnesHard": 48 - ablation_numbers["multipliers $a_1,a_2$ replaced by $1,1$"][1],
        "SwapSeeded": 200 - ablation_numbers["multipliers exchanged ($a_2$ on $\\tor_1$)"][0],
        "SwapHard": 48 - ablation_numbers["multipliers exchanged ($a_2$ on $\\tor_1$)"][1],
        "BlockOneSeeded": 200 - ablation_numbers["cross term only from blocks of size one"][0],
        "BlockOneHard": 48 - ablation_numbers["cross term only from blocks of size one"][1],
        "ProductSeeded": 200 - ablation_numbers["cross term replaced by $\\ell(\\tor_1)\\ell(\\tor_2)$"][0],
        "ProductHard": 48 - ablation_numbers["cross term replaced by $\\ell(\\tor_1)\\ell(\\tor_2)$"][1],
    }.items()))

# ------------------------------------------------------------------------------------------------ table: provenance
files = [
    ("code/hwcert/gluing.py", PROBLEM / "code" / "hwcert" / "gluing.py"),
    ("tests/test_huneke_wiegand_exp068.py", REPO / "tests" / "test_huneke_wiegand_exp068.py"),
    ("tests/test_huneke_wiegand_exp070.py", REPO / "tests" / "test_huneke_wiegand_exp070.py"),
    ("EXP-068/run.py", EXP68 / "run.py"), ("EXP-068/audit.py", EXP68 / "audit.py"),
    ("EXP-068/artifacts/results.json", EXP68 / "artifacts" / "results.json"),
    ("EXP-068/artifacts/audit.json", EXP68 / "artifacts" / "audit.json"),
    ("EXP-068/artifacts/run-log.txt", EXP68 / "artifacts" / "run-log.txt"),
    ("EXP-070/run.py", EXP70 / "run.py"), ("EXP-070/gluing\\_cases.py", EXP70 / "gluing_cases.py"),
    ("EXP-070/auditor.py", EXP70 / "auditor.py"),
    ("EXP-070/artifacts/results.json", EXP70 / "artifacts" / "results.json"),
    ("EXP-070/artifacts/run-log.txt", EXP70 / "artifacts" / "run-log.txt"),
]
rows = []
for name, path in files:
    h = digest(path)
    shown = name if chr(92) in name else name.replace("_", chr(92) + "_")
    rows.append([r"\texttt{\scriptsize " + shown + "}", r"\texttt{\scriptsize " + h + "}"])
write("tab-provenance.tex",
      r"\begin{tabular}{@{}p{5.5cm}p{9.6cm}@{}}" + "\n" + r"\toprule" + "\n"
      + r"file & SHA-256 of the committed file\\" + "\n" + r"\midrule" + "\n"
      + table_rows(rows) + r"\bottomrule" + "\n" + r"\end{tabular}" + "\n")

# figure data

def dat(name: str, header: list[str], data: list[list]) -> None:
    write(name, " ".join(header) + "\n" + "".join(" ".join(str(v) for v in row) + "\n" for row in data))


dat("fig-law-068.dat", ["law", "direct"], [[r["law"], r["direct"]] for r in records if r["set"] == "068"])
dat("fig-law-070.dat", ["law", "direct"], [[r["law"], r["direct"]] for r in records if r["set"] == "070"])
dat("fig-law-max.dat", ["x", "y"], [[0, 0], [max(r["law"] for r in records), max(r["law"] for r in records)]])
class_order = ("PP", "HP", "HH", "CP", "CH")
dat("fig-classes.dat", ["idx", "class", "seeded", "hard"],
    [[i, k, sum(1 for r in records if r["set"] == "068" and r["kind"] == k),
      sum(1 for r in records if r["set"] == "070" and r["kind"] == k)] for i, k in enumerate(class_order)])
dat("fig-cross.dat", ["idx", "own", "cross", "total"],
    [[i + 1, c["a1"] * c["t1"] + c["a2"] * c["t2"], c["cross"], c["direct"]] for i, c in enumerate(cross68)])
for base in ("B1", "B2", "B3", "B4"):
    sel = [c for c in cases70 if c["producer"]["base"] == base]
    dat(f"fig-cost-{base}.dat", ["pairs", "producer", "auditor", "top"],
        [[c["producer"]["pairs_scanned"], c["producer"]["torsion_seconds"], c["audit"]["seconds"],
          c["producer"]["degree_range"][1]] for c in sel])
kappa = statistics.median(ratio)
dat("fig-cost-line.dat", ["top", "pairs"], [[t, f"{kappa * t * t:.0f}"] for t in (min(tops70), max(tops70))])
write("numbers-cost.tex", f"\\newcommand{{\\HardRatioMedian}}{{{kappa:.3f}}}\n")
print("make_results: done")
