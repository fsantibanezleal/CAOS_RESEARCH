"""The reproduction harness must cover every experiment that has a result to reproduce.

`code/reproduce_all.py` reruns each runner at the settings stored in its own result file
and diffs every numeric leaf. This guard keeps the map honest in the two ways it can rot:
a new experiment that nobody adds to the harness, and a verdict that stops saying how to
rerun itself. Neither needs a GPU to check, so both run in the CI lane.

Why it exists: the first attempt at reproducing EXP-004 used the runner's defaults for
`measure2` and `settle`, which are not what the recorded run used, and the correlation came
out 0.9920 instead of 0.9995. The record knew; the prose did not.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT / "problems/analysis-pde/navier-stokes"
EXPERIMENTS = PROBLEM / "experiments"
HARNESS = PROBLEM / "code/reproduce_all.py"
if str(PROBLEM / "code") not in sys.path:
    sys.path.insert(0, str(PROBLEM / "code"))


def harness_cases() -> dict:
    """Read the CASES map without importing torch, by parsing the module."""
    tree = ast.parse(HARNESS.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "CASES":
            return ast.literal_eval(
                ast.unparse(node.value).replace("EXPERIMENTS / ", ""))
    raise AssertionError("CASES not found in reproduce_all.py")


def test_the_harness_covers_every_runner_with_a_recorded_result():
    cases = harness_cases()
    covered = {c["runner"] for c in cases.values()}
    # EXP-005 has its own multi-part runner and is covered by the quoted-number gate;
    # EXP-001 and EXP-006 are Lean builds, not Python runs.
    assert covered == {"run_exp002.py", "run_exp003.py", "run_exp004.py"}
    for case in cases.values():
        record = EXPERIMENTS / case["record"]
        assert record.is_file(), f"{record} is missing"
        assert "args" in json.loads(record.read_text(encoding="utf-8")), (
            f"{record} has no args block, so its run cannot be reproduced")


def test_every_recorded_result_stores_the_settings_it_was_run_with():
    """A result without its args cannot be rerun, however well it is described."""
    missing = []
    for record in EXPERIMENTS.rglob("result*.json"):
        payload = json.loads(record.read_text(encoding="utf-8"))
        if record.name == "result-fresh-replay.json":
            continue                                    # a Lean run, not a Python one
        if not payload.get("args"):
            missing.append(record.relative_to(EXPERIMENTS).as_posix())
    assert not missing, f"results with no args block: {missing}"


def test_the_three_verdicts_say_how_to_rerun_themselves():
    for name in ("EXP-002-reduction-control", "EXP-003-threshold-sweep",
                 "EXP-004-multilayer-handoff"):
        verdict = (EXPERIMENTS / name / "verdict.md").read_text(encoding="utf-8")
        assert "reproduce_all.py" in verdict, f"{name} does not point at the harness"
        assert "Reproduction, added 2026-09-17" in verdict


def test_the_stored_reproduction_report_is_clean():
    report = json.loads(
        (EXPERIMENTS / "reproduction-2026-09-17.json").read_text(encoding="utf-8"))
    assert report["all_reproduce"] is True
    assert {r["name"] for r in report["results"]} == {"exp002", "exp003", "exp004"}
    for r in report["results"]:
        assert r["mismatches"] == [] and r["missing_from_rerun"] == []
        assert r["n_leaves_compared"] >= 13


def test_timings_are_excluded_from_the_diff_but_results_are_not():
    import reproduce_all as R

    assert R.is_timing("wall_seconds") and R.is_timing("ensemble.seconds")
    assert not R.is_timing("H1.max_rel_err_vs_corrected")
    assert not R.is_timing("background.steady_state_drift_over_200_steps")
    sample = {"args": {"n": 1}, "wall_seconds": 3.0, "a": {"seconds": 1.0, "corr": 0.5}}
    assert R.leaves(sample) == {"a.corr": 0.5}


def test_the_command_line_is_rebuilt_from_the_record():
    import reproduce_all as R

    record = {"args": {"out": "x.json", "device": "cuda", "n": 1024, "mask_frac": 0.35,
                       "mode": "frozen", "flag_on": True, "flag_off": False}}
    argv = R.argv_from_record(record)
    assert "--out" not in argv and "--device" not in argv
    assert argv[argv.index("--mask-frac") + 1] == "0.35"
    assert argv[argv.index("--n") + 1] == "1024"
    assert "--flag-on" in argv and "--flag-off" not in argv
