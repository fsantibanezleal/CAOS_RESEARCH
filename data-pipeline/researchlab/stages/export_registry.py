"""Export stage: bake the program registry and the Jacobian problem data into web artifacts.

Deterministic, stdlib + PyYAML only. Sources of truth: program/portfolio.yaml (the portfolio
board) and problems/<area>/<slug>/experiments/EXP-* (hypothesis/verdict records). The Jacobian
numeric payload (family table, escape wall, census samples, collisions) is transcribed from the
exact experiment verdicts (EXP-004/007/008/011/012); every value here is traceable to an
artifact in the corresponding experiment folder.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
DERIVED = ROOT / "data" / "derived"
MANIFESTS = DERIVED / "manifests"


def _read_portfolio() -> dict:
    data = yaml.safe_load((ROOT / "program" / "portfolio.yaml").read_text(encoding="utf-8"))
    return {"updated": data.get("updated"), "areas": data.get("areas", []),
            "problems": data.get("problems", [])}


VERDICT_RE = re.compile(r"Verdict:\s*([A-Z][A-Z 0-9,\-]+?)\s*[(.]")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def _read_experiments() -> list[dict]:
    out: list[dict] = []
    for probdir in sorted((ROOT / "problems").glob("*/*")):
        exps = probdir / "experiments"
        if not exps.is_dir():
            continue
        for expdir in sorted(exps.iterdir()):
            if not expdir.is_dir() or not expdir.name.startswith("EXP-"):
                continue
            rec = {"problem": probdir.name, "area": probdir.parent.name,
                   "id": expdir.name.split("-")[1], "slug": expdir.name,
                   "title": "", "verdict": "", "date": ""}
            hyp = expdir / "hypothesis.md"
            if hyp.exists():
                first = hyp.read_text(encoding="utf-8").splitlines()[0]
                rec["title"] = first.lstrip("# ").split(" - ", 1)[-1].strip()
            ver = expdir / "verdict.md"
            if ver.exists():
                first = ver.read_text(encoding="utf-8").splitlines()[0]
                m = VERDICT_RE.search(first)
                if m:
                    rec["verdict"] = m.group(1).strip().lower()
                dm = DATE_RE.search(first)
                if dm:
                    rec["date"] = dm.group(1)
            out.append(rec)
    return out


def _jacobian_payload() -> dict:
    """The exact numeric payload for the Jacobian problem page (traceable to verdicts)."""
    return {
        "map": {
            "P": "u^3 z + y^2 u (4+3xy)", "Q": "y + 3x u^2 z + 3x y^2 (4+3xy)",
            "R": "2x - 3x^2 y - x^3 z", "u": "1 + xy", "det": -2,
            "collision_points": [[0, 0, -0.25], [1, -1.5, 6.5], [-1, 1.5, 6.5]],
            "collision_target": [-0.25, 0, 0],
        },
        "family": [
            {"seed": "2w - 3w^2 (announced)", "det": -2, "degrees": [7, 6, 4], "fiber": 3},
            {"seed": "w - 2w^3", "det": -3, "degrees": [12, 11, 4], "fiber": 4,
             "collision": {"points": [["-1/15", "18", "5130"], ["1/24", "-18", "-10368"]],
                           "target": ["-54", "-54", "1"]}},
            {"seed": "8w - 12w^2 + 4w^3 - 5w^4", "det": -350, "degrees": [17, 16, 4], "fiber": 5},
            {"seed": "w - 3w^5", "det": -20, "degrees": [22, 21, 4], "fiber": 6},
            {"seed": "2w - 3w^2, section tail v^2", "det": -2, "degrees": [8, 7, 5], "fiber": 3},
        ],
        "laws": {"det": "-k p(1)^2", "fiber_degree": "deg p + 1",
                 "degrees": "(5d-3, 5d-4, 4)"},
        "wall": {"equation": "27 A^2 C^2 - 18 A B C + 16 A + B^3 C - B^2 = 0",
                 "bracket_coeffs": {"A2C2": 27, "ABC": -18, "A": 16, "B3C": 1, "B2": -1},
                 "census": {"bracket_negative": 3, "bracket_positive": 1},
                 "escape_demo": {"target": [0, 1, 1], "surviving_point": [2, -0.5, 1.125]}},
        "fiber_cubic": {"phi": "w^2 - w^3", "equation": "4 Phi(w) - w BC + A C^2 = 0"},
        "landscape": [
            {"m": 1, "o": [-1, -1, 1], "status": "JC(2) bridge; 93 instances, all injective"},
            {"m": 2, "o": [-2, -1, 1], "status": "THE mechanism (announced map + our family)"},
            {"m": 3, "o": [-2, -2, 1], "status": "EMPTY (valuation proof)"},
            {"m": 3, "o": [-3, -1, 1], "status": "rigid in scans (60 instances)"},
            {"m": 4, "o": [-3, -2, 1], "status": "potential family EMPTY (Groebner certificate)"},
        ],
    }


def run() -> list[Path]:
    DERIVED.mkdir(parents=True, exist_ok=True)
    (DERIVED / "research").mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "portfolio": _read_portfolio(),
        "experiments": {"experiments": _read_experiments()},
        "jacobian": _jacobian_payload(),
    }
    written: list[Path] = []
    index = {"contract": "research-registry-v1", "cases": []}
    for name, payload in artifacts.items():
        art_rel = f"research/{name}.json"
        art_path = DERIVED / art_rel
        art_path.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n",
                            encoding="utf-8")
        digest = hashlib.sha256(art_path.read_bytes()).hexdigest()
        manifest = {"case_id": name, "artifact": {"path": art_rel,
                    "bytes": art_path.stat().st_size, "sha256": digest},
                    "lane": "precompute", "gate": {"lane": "precompute",
                    "reason": "baked registry export; the web replays it"}}
        man_rel = f"manifests/{name}.json"
        (DERIVED / man_rel).write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n",
                                       encoding="utf-8")
        index["cases"].append({"case_id": name, "manifest_path": man_rel})
        written += [art_path, DERIVED / man_rel]
    (MANIFESTS / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8")
    written.append(MANIFESTS / "index.json")
    return written
