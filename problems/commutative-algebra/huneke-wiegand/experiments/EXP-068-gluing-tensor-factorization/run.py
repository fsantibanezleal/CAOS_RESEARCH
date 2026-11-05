"""EXP-068 producer: tensor factorization of extension ideals under gluing.

Run from the repository root:  .venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-068-gluing-tensor-factorization/run.py
Writes artifacts/results.json and artifacts/run-log.txt next to this file. Exact integer arithmetic only.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
import time
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))

from hwcert.gluing import (  # noqa: E402
    Window, extension_generators, glue_generators, hilbert_identity_holds, ideal_from_generators,
    is_extension, is_huneke_wiegand, minimal_generators, predicted_length, semigroup_mask, tensor_torsion,
)

SEED = 20261030
CASES = 200
PHAM = (56, 57, 58, 63, 64, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 87, 89, 90, 93, 95, 96, 97)
ARTIFACTS = HERE / "artifacts"
LOG: list[str] = []


def log(message: str) -> None:
    line = f"{time.strftime('%H:%M:%S')} {message}"
    LOG.append(line)
    print(line, flush=True)


def exp009_member(p: int) -> tuple[tuple[int, ...], int]:
    path = HERE.parent / "EXP-009-growing-interval-family" / "audit.py"
    spec = importlib.util.spec_from_file_location("exp009_for_exp068", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    _, frobenius, generators = module.independent_mask(p)
    return tuple(generators), frobenius


def factor(gens: tuple[int, ...], ideal_gens: tuple[int, ...], y_degree: int) -> dict:
    span = max(ideal_gens)
    window = Window(-span - 4, 6 * (max(gens) * max(gens) + span) + 64)
    sg = semigroup_mask(window, gens)
    ideal = ideal_from_generators(window, sg, ideal_gens)
    mingens = minimal_generators(window, ideal, gens)
    torsion = tensor_torsion(window, sg, gens, mingens, y_degree=y_degree)
    return {"window": window, "semigroup": sg, "ideal": ideal, "gens": mingens,
            "hw": is_huneke_wiegand(window, sg, gens, mingens), "torsion": torsion}


def random_semigroup(rng: random.Random) -> tuple[int, ...]:
    while True:
        gens = tuple(sorted(rng.sample(range(3, 14), rng.randint(2, 4))))
        if gcd(*gens) != 1:
            continue
        window = Window(0, 400)
        frob = window.tail_start(semigroup_mask(window, gens)) - 1
        if frob <= 10:
            return gens


def small_case(rng: random.Random, index: int) -> dict:
    gens1, gens2 = random_semigroup(rng), random_semigroup(rng)
    w = Window(0, 200)
    sg1, sg2 = semigroup_mask(w, gens1), semigroup_mask(w, gens2)
    while True:
        a2 = rng.choice([v for v in range(2, 8) if w.contains(sg1, v)] or [8])
        a1 = rng.choice([v for v in range(2, 8) if w.contains(sg2, v)] or [8])
        if gcd(a1, a2) == 1 and w.contains(sg1, a2) and w.contains(sg2, a1):
            break
        gens1, gens2 = random_semigroup(rng), random_semigroup(rng)
        sg1, sg2 = semigroup_mask(w, gens1), semigroup_mask(w, gens2)
    ideal1 = tuple(sorted({0} | set(rng.sample(range(1, 11), rng.randint(0, 2)))))
    ideal2 = tuple(sorted({0} | set(rng.sample(range(1, 11), rng.randint(0, 2)))))
    f1, f2 = factor(gens1, ideal1, a2), factor(gens2, ideal2, a1)
    glued = glue_generators(a1, gens1, a2, gens2)
    ext = extension_generators(a1, f1["gens"], a2, f2["gens"])
    conductor_bound = a1 * max(gens1) ** 2 + a2 * max(gens2) ** 2 + a1 * a2
    window = Window(-max(ext) - 4, 4 * (conductor_bound + max(ext)) + 64)
    sg = semigroup_mask(window, glued)
    ideal = ideal_from_generators(window, sg, ext)
    mingens = minimal_generators(window, ideal, glued)
    direct = tensor_torsion(window, sg, glued, mingens)
    predicted = predicted_length(a1, a2, f1["torsion"], f2["torsion"])
    hw = is_huneke_wiegand(window, sg, glued, mingens)
    hw_pred = None if (f1["hw"] is None and f2["hw"] is None) else (f1["hw"] is True or f2["hw"] is True)
    hilbert = hilbert_identity_holds(window, sg, a1, a2, f1["ideal"], f1["window"], f2["ideal"], f2["window"],
                                     ideal, upto=min(window.hi, 3 * conductor_bound))
    return {
        "index": index, "gens1": gens1, "gens2": gens2, "a1": a1, "a2": a2,
        "ideal1": f1["gens"], "ideal2": f2["gens"], "ideal": mingens,
        "mu": [len(f1["gens"]), len(f2["gens"]), len(mingens)],
        "torsion1": f1["torsion"].length, "jordan1": f1["torsion"].jordan_at_least,
        "torsion2": f2["torsion"].length, "jordan2": f2["torsion"].jordan_at_least,
        "torsion_direct": direct.length, "torsion_predicted": predicted,
        "hw": hw, "hw1": f1["hw"], "hw2": f2["hw"], "hw_predicted": hw_pred, "hilbert_identity": hilbert,
        "p1": direct.length == predicted,
        "p2": hw == hw_pred and len(mingens) == len(f1["gens"]) * len(f2["gens"])
              and (hw is None or (direct.length > 0) == hw),
    }


def big_instance(label: str, gens1, a2, ideal1, gens2, a1, ideal2, frob1, frob2) -> dict:
    glued = glue_generators(a1, gens1, a2, gens2)
    ext = extension_generators(a1, ideal1, a2, ideal2)
    frob = a1 * frob1 + a2 * frob2 + a1 * a2
    window = Window(-max(ext) - 8, frob + 3 * max(ext) + 4 * max(glued))
    t0 = time.time()
    sg = semigroup_mask(window, glued)
    measured_frob = window.tail_start(sg) - 1
    ideal = ideal_from_generators(window, sg, ext)
    mingens = minimal_generators(window, ideal, glued)
    hw = is_huneke_wiegand(window, sg, glued, mingens)
    symmetric = all(window.contains(sg, x) != window.contains(sg, measured_frob - x) for x in range(0, measured_frob + 1))
    record = {"label": label, "a1": a1, "a2": a2, "frobenius_formula": frob, "frobenius_measured": measured_frob,
              "symmetric": symmetric, "ideal_generators": mingens, "mu": len(mingens), "huneke_wiegand": hw,
              "seconds": round(time.time() - t0, 1)}
    log(f"{label}: F={measured_frob} (formula {frob}) symmetric={symmetric} mu={len(mingens)} gens={mingens} HW={hw}")
    return record, (window, sg, glued, ideal)


def main() -> int:
    ARTIFACTS.mkdir(exist_ok=True)
    started = time.time()
    rng = random.Random(SEED)
    cases = []
    for index in range(CASES):
        case = small_case(rng, index)
        cases.append(case)
        if not (case["p1"] and case["p2"] and case["hilbert_identity"]):
            log(f"case {index} FAILED: {json.dumps(case)}")
        if index % 40 == 0:
            log(f"case {index}: torsion direct={case['torsion_direct']} predicted={case['torsion_predicted']} "
                f"hw={case['hw']} elapsed={time.time() - started:.0f}s")
    p1 = all(c["p1"] for c in cases)
    p2 = all(c["p2"] for c in cases)
    hilbert = all(c["hilbert_identity"] for c in cases)
    nontrivial_cross = sum(1 for c in cases if c["torsion1"] and c["torsion2"])
    log(f"P1 {p1}, P2 {p2}, Hilbert identity {hilbert}; cases with torsion on both factors: {nontrivial_cross}")

    gens9, frob9 = exp009_member(4)
    w9 = Window(-40, 1200)
    sg9 = semigroup_mask(w9, gens9)
    exp009_hw = is_huneke_wiegand(w9, sg9, gens9, (0, 24))
    wp = Window(-40, 900)
    sgp = semigroup_mask(wp, PHAM)
    pham_hw = is_huneke_wiegand(wp, sgp, PHAM, (0, 14))
    pham_control_hw = is_huneke_wiegand(wp, sgp, PHAM, (0, 1))
    log(f"factors: Pham (0,14) HW={pham_hw}; Pham (0,1) HW={pham_control_hw}; EXP-009 p=4 multiplicity "
        f"{min(gens9)}, F={frob9}, (0,24) HW={exp009_hw}")

    p3a, built = big_instance("Pham x Pham", PHAM, 57, (0, 14), PHAM, 56, (0, 14), 181, 181)
    p3b, _ = big_instance("Pham x EXP-009(p=4)", PHAM, 89, (0, 14), gens9, 96, (0, 24), 181, frob9)
    control_hw, _ = big_instance("control: Pham (0,14) x Pham (0,1)", PHAM, 57, (0, 14), PHAM, 56, (0, 1), 181, 181)

    window, sg, glued, _ = built
    perturbed_gens = (0, 784, 798, 1583)
    perturbed = ideal_from_generators(window, sg, perturbed_gens)
    w1 = Window(-40, window.hi // 56 + 2)
    w2 = Window(-40, window.hi // 57 + 2)
    s1, s2 = semigroup_mask(w1, PHAM), semigroup_mask(w2, PHAM)
    true_ideal = ideal_from_generators(window, sg, (0, 784, 798, 1582))
    extension_true = is_extension(window, sg, glued, true_ideal, 56, 57, s1, w1, PHAM, s2, w2, PHAM)
    extension_perturbed = is_extension(window, sg, glued, perturbed, 56, 57, s1, w1, PHAM, s2, w2, PHAM)
    perturbed_mu = len(minimal_generators(window, perturbed, glued))
    perturbed_hw = is_huneke_wiegand(window, sg, glued, perturbed_gens)
    log(f"extension test: true ideal {extension_true}, perturbed {extension_perturbed}; perturbed mu={perturbed_mu} HW={perturbed_hw}")

    non_gluing_breaks = 0
    rng2 = random.Random(SEED + 1)
    tried = 0
    while tried < 30:
        gens1, gens2 = random_semigroup(rng2), random_semigroup(rng2)
        w = Window(0, 200)
        sg1, sg2 = semigroup_mask(w, gens1), semigroup_mask(w, gens2)
        gaps2 = [v for v in range(2, 8) if not w.contains(sg2, v)]
        a2s = [v for v in range(2, 8) if w.contains(sg1, v)]
        pairs = [(a1, a2) for a1 in gaps2 for a2 in a2s if gcd(a1, a2) == 1]
        if not pairs:
            continue
        a1, a2 = rng2.choice(pairs)
        tried += 1
        glued_bad = glue_generators(a1, gens1, a2, gens2)
        bound = a1 * max(gens1) ** 2 + a2 * max(gens2) ** 2 + a1 * a2
        wb = Window(-4, 4 * bound + 64)
        sgb = semigroup_mask(wb, glued_bad)
        i1, i2 = (0,), (0,)
        f1w, f2w = Window(-4, 6 * max(gens1) ** 2 + 64), Window(-4, 6 * max(gens2) ** 2 + 64)
        m1 = ideal_from_generators(f1w, semigroup_mask(f1w, gens1), i1)
        m2 = ideal_from_generators(f2w, semigroup_mask(f2w, gens2), i2)
        if not hilbert_identity_holds(wb, sgb, a1, a2, m1, f1w, m2, f2w, sgb, upto=3 * bound):
            non_gluing_breaks += 1
    log(f"non-gluing control: Hilbert identity broken on {non_gluing_breaks} of {tried} pairs with a1 not in Gamma2")

    p3 = (p3a["mu"] == 4 and p3a["huneke_wiegand"] is False and p3a["symmetric"]
          and p3b["mu"] == 4 and p3b["huneke_wiegand"] is False and p3b["symmetric"]
          and pham_hw is False and exp009_hw is False)
    p4 = (control_hw["huneke_wiegand"] is True and pham_control_hw is True and non_gluing_breaks >= 1
          and extension_true and not extension_perturbed)
    summary = {
        "seed": SEED, "cases": CASES, "P1_torsion_length_law": p1, "P2_characterization": p2,
        "invariant_hilbert_identity": hilbert, "cases_with_torsion_on_both_factors": nontrivial_cross,
        "P3_four_generated_counterexamples": p3, "P4_controls": p4,
        "p3_instances": [p3a, p3b], "p4": {
            "control_extension_with_hw_factor": control_hw, "pham_0_1_is_hw": pham_control_hw,
            "non_gluing_pairs": tried, "non_gluing_hilbert_breaks": non_gluing_breaks,
            "extension_test_true_ideal": extension_true, "extension_test_perturbed": extension_perturbed,
            "perturbed_mu": perturbed_mu, "perturbed_hw": perturbed_hw},
        "factor_checks": {"pham_0_14_hw": pham_hw, "exp009_p4_0_24_hw": exp009_hw, "exp009_p4_frobenius": frob9,
                          "exp009_p4_multiplicity": min(gens9)},
        "seconds": round(time.time() - started, 1),
    }
    (ARTIFACTS / "results.json").write_text(json.dumps({"summary": summary, "cases": cases}, indent=1) + "\n",
                                            encoding="utf-8")
    (ARTIFACTS / "run-log.txt").write_text("\n".join(LOG) + "\n", encoding="utf-8")
    log(f"done: P1={p1} P2={p2} P3={p3} P4={p4} in {summary['seconds']}s")
    return 0 if (p1 and p2 and p3 and p4 and hilbert) else 1


if __name__ == "__main__":
    raise SystemExit(main())
