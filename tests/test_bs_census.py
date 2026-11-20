"""Tests for boij-soderberg-realizability EXP-001 (the realizability table of the 220 pure rays).

Pure Python: no Macaulay2 or Singular is called here. Every test writes only to pytest tmp paths.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = (ROOT / "problems" / "commutative-algebra" / "boij-soderberg-realizability" / "experiments"
       / "EXP-001-pure-ray-census")
DOSSIER = (ROOT / "problems" / "combinatorics" / "petersen-coloring" / "context" / "scouting-2026-09"
           / "2026-09-02-dossier-boij-soderberg-realizability.md")


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXP / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


C = _load("bs_census", "census.py")
R = _load("bs_run", "run.py")


# ---------------------------------------------------------------- primitive points, counts

HAND = {
    (0, 1, 3, 4): (1, 2, 2, 1),
    (0, 6, 20, 21): (1, 2, 9, 8),
    (0, 4, 9, 10): (1, 3, 8, 6),
    (0, 1, 6, 10): (6, 8, 3, 1),
    (0, 1, 2, 3): (1, 3, 3, 1),
    (0, 1, 2, 4): (3, 8, 6, 1),
    (0, 2, 3, 4): (1, 6, 8, 3),
    (0, 3, 5, 8): (1, 4, 4, 1),
    (0, 1, 4, 5): (3, 5, 5, 3),
    (0, 1, 3, 6): (5, 9, 5, 1),
    (0, 2, 3, 7): (10, 42, 35, 3),
    (0, 3, 4, 7): (1, 7, 7, 1),
    (0, 4, 9, 13): (5, 13, 13, 5),
}


@pytest.mark.parametrize("d,beta", sorted(HAND.items()))
def test_primitive_point_matches_hand_value(d, beta) -> None:
    assert C.primitive_point(d) == beta


def test_counts_of_the_census() -> None:
    rays = C.rays()
    assert len(rays) == 220
    assert rays[0] == (0, 1, 2, 3) and rays[-1] == (0, 10, 11, 12)
    cyclic = [d for d in rays if C.primitive_point(d)[0] == 1]
    assert len(cyclic) == 44
    passing = [d for d in rays if C.parity(d) == 0]
    assert len(passing) == 29


def test_parity_values_of_the_two_counterexample_rays() -> None:
    assert C.parity((0, 4, 9, 10)) == -16
    assert C.parity((0, 1, 6, 10)) == 16
    assert C.parity((0, 1, 3, 4)) == 0


def test_hilbert_functions() -> None:
    assert C.hilbert_S((0, 2, 3, 4)) == [1, 3]  # S/m^2
    assert C.hilbert_S((0, 3, 4, 5)) == [1, 3, 6]  # S/m^3
    assert C.hilbert_UH((0, 4, 9, 10)) is None  # parity fails: no finite series over U(H)
    uh = C.hilbert_UH((0, 1, 3, 4))
    assert uh is not None and all(c >= 0 for c in uh)


# ---------------------------------------------------------------- constructions and multiples

def test_construction_numbers_of_the_package_test() -> None:
    # package Test 15: pureAll{0,1,3,4} == (2,2,3)
    assert C.pure_all((0, 1, 3, 4)) == (2, 2, 3)
    assert C.pure_all((0, 1, 2, 3)) == (1, 1, 1)


def test_schur_dimension_hook_content() -> None:
    assert C.schur_dim(3, (1,)) == 3
    assert C.schur_dim(6, (1, 1, 1, 1)) == 15
    assert C.schur_dim(3, (3, 2, 0)) == 15
    assert C.schur_dim(4, (2,)) == 10


def test_pure_char_free_of_g7_ray() -> None:
    assert C.es_beta0((0, 4, 9, 13)) == 15400
    assert C.es_multiple((0, 4, 9, 13)) == 3080
    assert C.es_multiple((0, 1, 2, 3)) == 1


def test_soderberg_multiple() -> None:
    s = C.soderberg((0, 2, 3, 7))
    assert s is not None and s["multiple"] == 1 and s["s"] == 10 and s["t"] == 3
    s = C.soderberg((0, 3, 4, 8))
    assert s is not None and s["multiple"] == 2 and s["s"] == 10 and s["t"] == 6
    assert C.soderberg((0, 2, 5, 8)) is None


def test_soderberg_family_has_55_rays_and_integral_consistent_multiples() -> None:
    fam = [d for d in C.rays() if C.soderberg(d) is not None]
    assert len(fam) == 55
    for d in fam:
        s = C.soderberg(d)
        assert s["consistent"], d


# ---------------------------------------------------------------- obstructions

def ids(d, m):
    return {x.split(":")[0] for x in C.obstructions(d, m)}


def test_o1_applies_and_does_not_apply() -> None:
    assert "O1" in ids((0, 4, 9, 10), 1)
    assert "O1" not in ids((0, 1, 2, 3), 1)
    # the Rethlas ray (0,6,20,21): O1 excludes m = 1, 2 and not 3 (dossier 3.3)
    assert "O1" in ids((0, 6, 20, 21), 2) and "O1" not in ids((0, 6, 20, 21), 3)


def test_o2_codimension_and_equality_case() -> None:
    assert "O2" in ids((0, 1, 3, 4), 1)           # B1 = 2 < B0 + 2
    assert ids((0, 1, 3, 4), 2) == set()          # Buchsbaum-Rim table (2,4,4,2): realized, not excluded
    assert "O2" in ids((0, 1, 6, 10), 1)          # equality case, table is not the Buchsbaum-Rim one
    assert "O2" not in ids((0, 1, 2, 3), 1)


def test_o3_regularity() -> None:
    assert "O3" in ids((0, 1, 6, 10), 1)
    assert "O3" not in ids((0, 4, 9, 10), 2)


def test_o4_even_gorenstein_and_o5_three_generators() -> None:
    assert "O4" in ids((0, 3, 5, 8), 1)           # (1,4,4,1)
    assert "O4" not in ids((0, 3, 4, 7), 1)       # (1,7,7,1)
    assert "O4" not in ids((0, 3, 5, 8), 2)       # B0 = 2: not cyclic
    assert "O5" in ids((0, 4, 9, 10), 1)          # (1,3,8,6)
    assert "O5" not in ids((0, 4, 8, 12), 1)      # Koszul (1,3,3,1) on (0,a,2a,3a)


def test_o6_is_the_dual_of_o1_to_o5() -> None:
    assert "O6" in ids((0, 1, 6, 10), 1)          # dual (0,4,9,10) is excluded by O1 and O5
    assert "O6" in ids((0, 4, 9, 10), 1)          # dual (0,1,6,10) is excluded by O2 and O3
    assert "O6" not in ids((0, 1, 2, 3), 1)


def test_g6_statement() -> None:
    g = C.gate_g6()
    assert g["passed"], g
    assert g["details"]["(0,4,9,10)"]["beta"] == [1, 3, 8, 6]
    assert g["details"]["(0,1,6,10)"]["p_minus_1"] == 16


def test_exactly_twelve_primitive_points_excluded_at_m1() -> None:
    table = C.compute_tables()
    excluded = [d for d, r in table.items() if 1 in r["excluded"]]
    assert len(excluded) == 12, sorted(excluded)


# ---------------------------------------------------------------- closures

def test_duality_map() -> None:
    assert C.dual((0, 4, 9, 10)) == (0, 1, 6, 10)
    assert C.dual(C.dual((0, 2, 7, 11))) == (0, 2, 7, 11)
    assert C.dual_beta((1, 3, 8, 6)) == (6, 8, 3, 1)
    for d in C.rays():
        assert C.primitive_point(C.dual(d)) == C.dual_beta(C.primitive_point(d))


def test_scaling_closure_needs_a_named_source() -> None:
    base = C.compute_tables()
    assert 1 not in base[(0, 2, 6, 12)]["realized"] or base[(0, 2, 6, 12)]["realized"][1]
    hit = {"d": (0, 1, 3, 6), "m": 1, "route": "search:socle", "field": "GF(32003)", "evidence": "synthetic"}
    table = C.compute_tables(extra_realized=[hit])
    for d in [(0, 1, 3, 6), (0, 2, 6, 12), (0, 3, 6 + 0, 6)][:2]:
        assert 1 in table[d]["realized"]
    entries = table[(0, 2, 6, 12)]["realized"][1]
    assert any("(0,1,3,6)" in e["evidence"] for e in entries)
    # the dual of the hit ray is realized too, with the source named
    dd = C.dual((0, 1, 3, 6))
    assert any("(0,1,3,6)" in e["evidence"] for e in table[dd]["realized"][1])


def test_closure_without_hits_never_realizes_without_a_source() -> None:
    table = C.compute_tables()
    for d, rec in table.items():
        for m, entries in rec["realized"].items():
            assert entries, (d, m)
            for e in entries:
                assert e["route"] and e["field"] and e["evidence"], (d, m, e)


def test_direct_sum_semigroup() -> None:
    hit = {"d": (0, 1, 3, 4), "m": 3, "route": "x", "field": "char 0", "evidence": "EFW"}
    table = C.compute_tables(extra_realized=[hit])
    # (0,1,3,4): multiple 2 (Buchsbaum-Rim) plus multiple 3 give every m >= 2
    assert {m for m in table[(0, 1, 3, 4)]["realized"]} >= {2, 3, 4, 5, 6}
    assert 1 not in table[(0, 1, 3, 4)]["realized"]
    assert table[(0, 1, 3, 4)]["low"] == 2 and table[(0, 1, 3, 4)]["up"] == 2


def test_hit_on_excluded_point_is_g4_violation() -> None:
    table = C.compute_tables()
    assert C.g4_violation(table, (0, 1, 3, 4), 1)
    assert not C.g4_violation(table, (0, 1, 3, 4), 2)


def test_results_record_schema() -> None:
    table = C.compute_tables()
    rec = table[(0, 3, 4, 8)]
    for key in ("d", "beta", "parity", "hf_S", "hf_UH", "es_multiple", "efw_multiples", "soderberg_multiple",
                "classical", "excluded", "realized", "low", "up", "status_primitive", "dual", "scaled_from"):
        assert key in rec, key
    assert rec["beta"] == [5, 32, 30, 3] and rec["soderberg_multiple"] == 2
    assert rec["up"] >= 2  # the Soderberg bound is not counted before stage 1b


# ---------------------------------------------------------------- dossier appendix (G2)

def test_appendix_parse_and_compare_columns() -> None:
    rows = C.parse_appendix(DOSSIER)
    assert len(rows) == 220
    table = C.compute_tables()
    cmp = C.compare_appendix(rows, table)
    assert cmp["rows"] == 220
    assert cmp["beta_mismatch"] == [] and cmp["es_mismatch"] == [] and cmp["parity_mismatch"] == []
    for diff in cmp["status_differences"]:
        assert diff["reason"], diff


# ---------------------------------------------------------------- driver helpers

def test_wsl_path_conversion() -> None:
    assert R.wsl_path("E:/_Datos/caos-research/x") == "/mnt/e/_Datos/caos-research/x"
    assert R.wsl_path("D:\\_Repos\\a b") == "/mnt/d/_Repos/a b"


def test_ray_tag_and_cell_key() -> None:
    assert R.ray_tag((0, 3, 4, 8)) == "0-3-4-8"
    assert R.cell_key((0, 3, 4, 8), 2, "socle", 1, 32003) == "0-3-4-8|2|socle|1|32003"


def test_resumable_index_skips_finished_cells(tmp_path) -> None:
    log = tmp_path / "rays"
    log.mkdir()
    d = (0, 3, 4, 6)
    R.append_jsonl(log / f"{R.ray_tag(d)}.jsonl", {"d": list(d), "m": 1, "gen": "socle", "seed": 1, "p": 32003,
                                                  "outcome": "hit", "seconds": 0.5, "stage": "1c"})
    R.append_jsonl(log / f"{R.ray_tag(d)}.jsonl", {"d": list(d), "m": 1, "gen": "socle", "seed": 2, "p": 32003,
                                                  "outcome": "timeout", "seconds": 1200.0, "stage": "1c"})
    done = R.load_done(tmp_path)
    assert R.cell_key(d, 1, "socle", 1, 32003) in done
    assert R.cell_key(d, 1, "socle", 3, 32003) not in done
    cells = R.pending_cells(d, [1], ["socle", "module"], [1, 2, 3], 32003, done)
    assert ("socle", 1, 3) in {(c["gen"], c["m"], c["seed"]) for c in cells}
    assert ("socle", 1, 1) not in {(c["gen"], c["m"], c["seed"]) for c in cells}


def test_timeout_is_not_a_miss(tmp_path) -> None:
    d = (0, 3, 4, 6)
    R.append_jsonl(tmp_path / "rays" / f"{R.ray_tag(d)}.jsonl",
                   {"d": list(d), "m": 1, "gen": "socle", "seed": 1, "p": 32003, "outcome": "timeout",
                    "seconds": 1200.0, "stage": "1c"})
    summary = R.summarize_outcomes(R.load_cells(tmp_path))
    assert summary["timeout"] == 1 and summary["miss"] == 0 and summary["hit"] == 0


def test_search_range_rule() -> None:
    assert R.search_m_range(low=1, up=5) == [1, 2, 3, 4]
    assert R.search_m_range(low=2, up=3) == [2]
    assert R.search_m_range(low=3, up=3) == []
    assert R.search_m_range(low=1, up=1) == []
    assert R.search_m_range(low=5, up=40) == []


def test_singular_result_is_compared_with_exact_degrees() -> None:
    pure = {"d": [0, 3, 4, 6], "m": 1}
    good = "F 0 1 0 0\nF 1 8 3 3\nF 2 9 4 4\nF 3 2 6 6\n"
    assert R.singular_matches(good, (0, 3, 4, 6), (1, 8, 9, 2), pure["m"])
    bad_degrees = "F 0 1 0 0\nF 1 8 3 3\nF 2 9 5 5\nF 3 2 6 6\n"
    assert not R.singular_matches(bad_degrees, (0, 3, 4, 6), (1, 8, 9, 2), 1)
    bad_count = "F 0 1 0 0\nF 1 8 3 3\nF 2 9 4 4\nF 3 3 6 6\n"
    assert not R.singular_matches(bad_count, (0, 3, 4, 6), (1, 8, 9, 2), 1)


def test_hits_manifest_has_sha256(tmp_path) -> None:
    f = tmp_path / "a.m2"
    f.write_text("x", encoding="utf-8")
    entry = R.manifest_entry(f)
    assert entry["sha256"] == "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    json.dumps(entry)


def test_no_hard_coded_data_root_in_the_code() -> None:
    for name in ("census.py", "run.py"):
        text = (EXP / name).read_text(encoding="utf-8")
        assert "E:/" not in text and "E:\\" not in text and "/mnt/e" not in text, name
    assert "CAOS_RESEARCH_DATA" in (EXP / "run.py").read_text(encoding="utf-8")
