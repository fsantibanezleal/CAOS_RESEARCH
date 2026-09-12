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
import subprocess
from fractions import Fraction
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
DERIVED = ROOT / "data" / "derived"
MANIFESTS = DERIVED / "manifests"
EXP004_DECLARATION = "e03413b2301bf45ca68ff6e945f25add9a1c3a89"


def _read_portfolio() -> dict:
    data = yaml.safe_load((ROOT / "program" / "portfolio.yaml").read_text(encoding="utf-8"))
    return {"updated": data.get("updated"), "areas": data.get("areas", []),
            "problems": data.get("problems", [])}


VERDICT_RE = re.compile(r"Verdict:\s*([A-Z][A-Z 0-9,\-]+?)\s*[(.]")
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
BODY_VERDICT_RE = re.compile(r"Verdict:\s*\*\*([a-z][a-z -]+)\*\*", re.IGNORECASE)
HEADER_VERDICT_RE = re.compile(
    r"\bverdict:\s*(confirmed|refuted|mixed|pass|inconclusive)\b", re.IGNORECASE,
)


def _tracked_problem_paths() -> set[str]:
    """Return committed problem paths so a bake cannot absorb live outputs."""
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "problems"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return {
        path.decode("utf-8").replace("\\", "/")
        for path in result.stdout.split(b"\0")
        if path
    }


def _committed_bytes(path: str) -> bytes:
    return _revision_bytes(path, "HEAD")


def _revision_bytes(path: str, revision: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=ROOT, check=True, capture_output=True,
    ).stdout


def _committed_riemann_paths() -> set[str]:
    return set(subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "--",
         "problems/number-theory/riemann-hypothesis/experiments/"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.splitlines())


def _read_experiments() -> list[dict]:
    out: list[dict] = []
    tracked = _tracked_problem_paths()
    riemann_paths = _committed_riemann_paths()
    problem_dirs = set((ROOT / "problems").glob("*/*"))
    if riemann_paths:
        problem_dirs.add(ROOT / "problems/number-theory/riemann-hypothesis")
    for probdir in sorted(problem_dirs):
        exps = probdir / "experiments"
        committed_replay = probdir.name == "riemann-hypothesis"
        if not committed_replay and not exps.is_dir():
            continue
        source_paths = tracked
        if committed_replay:
            prefix = exps.relative_to(ROOT).as_posix() + "/"
            source_paths = riemann_paths
            expdirs = {exps / p[len(prefix):].split("/")[0] for p in source_paths}
        else:
            expdirs = set(exps.iterdir())
        for expdir in sorted(expdirs):
            if (not committed_replay and not expdir.is_dir()) or not expdir.name.startswith("EXP-"):
                continue
            rec = {"problem": probdir.name, "area": probdir.parent.name,
                   "id": expdir.name.split("-")[1], "slug": expdir.name,
                   "title": "", "verdict": "", "date": "",
                   "hypothesis_md": "", "verdict_md": "", "artifacts": []}
            hyp = expdir / "hypothesis.md"
            ver = expdir / "verdict.md"
            hyp_rel = hyp.relative_to(ROOT).as_posix()
            ver_rel = ver.relative_to(ROOT).as_posix()
            if hyp_rel not in source_paths and ver_rel not in source_paths:
                continue
            has_hypothesis = hyp_rel in source_paths if committed_replay else hyp.exists()
            if has_hypothesis:
                text = (_committed_bytes(hyp_rel).decode("utf-8") if committed_replay
                        else hyp.read_text(encoding="utf-8"))
                first = text.splitlines()[0]
                rec["title"] = first.lstrip("# ").split(" - ", 1)[-1].strip()
                rec["hypothesis_md"] = text
            has_verdict = ver_rel in source_paths if committed_replay else ver.exists()
            if has_verdict:
                text = (_committed_bytes(ver_rel).decode("utf-8") if committed_replay
                        else ver.read_text(encoding="utf-8"))
                first = text.splitlines()[0]
                m = VERDICT_RE.search(first)
                if m:
                    rec["verdict"] = m.group(1).strip().lower()
                elif headline_match := HEADER_VERDICT_RE.search(first):
                    rec["verdict"] = headline_match.group(1).lower()
                elif body_match := BODY_VERDICT_RE.search(text):
                    rec["verdict"] = body_match.group(1).strip().lower()
                dm = DATE_RE.search(first) or DATE_RE.search(text[:500])
                if dm:
                    rec["date"] = dm.group(1)
                rec["verdict_md"] = text
            arts = expdir / "artifacts"
            if committed_replay:
                art_prefix = arts.relative_to(ROOT).as_posix() + "/"
                rec["artifacts"] = sorted(
                    [{"name": p[len(art_prefix):], "bytes": len(_committed_bytes(p))}
                     for p in source_paths
                     if p.startswith(art_prefix) and "/" not in p[len(art_prefix):]],
                    key=lambda r: r["name"])
            elif arts.is_dir():
                rec["artifacts"] = sorted(
                    [{"name": f.name, "bytes": f.stat().st_size}
                     for f in arts.iterdir()
                     if f.is_file() and f.relative_to(ROOT).as_posix() in tracked],
                    key=lambda r: r["name"])
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
        "cascade": [
            {"name": "Jacobian conjecture / Smale 16", "prior": "open (1939)",
             "now": "false for N >= 3; N = 2 open", "chain": "the counterexample itself"},
            {"name": "Mathieu conjecture", "prior": "open (1997)",
             "now": "false for SU(N), N >= 3; SU(2) and other groups open",
             "chain": "Mathieu(SU(N)) implies JC(N)"},
            {"name": "Dixmier conjecture", "prior": "open (1968)",
             "now": "full conjecture false (rank 2 false); rank 1 open",
             "chain": "JC(2n) equivalent to Dixmier(n)"},
            {"name": "Poisson conjecture", "prior": "open (2007)",
             "now": "full conjecture false; minimal failing dimension open",
             "chain": "JC equivalent to Dixmier equivalent to Poisson"},
            {"name": "Gaussian moments conjecture", "prior": "open (2015)",
             "now": "false at some finite dimension", "chain": "GMC implies JC"},
            {"name": "Zhao vanishing conjecture", "prior": "open (2004)",
             "now": "false", "chain": "vanishing equivalent to JC"},
            {"name": "Image conjecture", "prior": "open (2010)",
             "now": "false in some dimension", "chain": "Image implies vanishing"},
            {"name": "Symmetric / gradient JC", "prior": "open reduction (2005)",
             "now": "false in some dimension", "chain": "symmetric JC stably equivalent to JC"},
        ],
        "landscape": [
            {"m": 1, "o": [-1, -1, 1], "status": "JC(2) bridge; 93 instances, all injective"},
            {"m": 2, "o": [-2, -1, 1], "status": "THE mechanism (announced map + our family)"},
            {"m": 3, "o": [-2, -2, 1], "status": "EMPTY (valuation proof)"},
            {"m": 3, "o": [-3, -1, 1], "status": "rigid in scans (60 instances)"},
            {"m": 4, "o": [-3, -2, 1], "status": "potential family EMPTY (Groebner certificate)"},
        ],
    }


def _riemann_payload() -> dict:
    """Replay committed experiment bytes, retaining their exact bounds and provenance.

    HEAD reads deliberately reject uncommitted inputs. No optimizer, verifier, or
    mathematical calculation runs in the export or in the browser.
    """
    problem = "problems/number-theory/riemann-hypothesis"
    exp_one = "EXP-001-source-and-constant-audit"
    exp_two = "EXP-002-short-interval-stability"
    exp_three = "EXP-003-odd-frame-pressure"
    exp_four = "EXP-004-parity-density-transfer"
    specifications = [
        ("constant_audit", exp_one, f"experiments/{exp_one}/artifacts/result.json"),
        ("result", exp_two, f"experiments/{exp_two}/artifacts/result.json"),
        ("certificate", exp_two, f"experiments/{exp_two}/artifacts/triangle-certificate.json"),
        ("proof", exp_two, f"experiments/{exp_two}/mathematical-proof.md"),
        ("verdict", exp_two, f"experiments/{exp_two}/verdict.md"),
        ("source_manifest", "source-review", "context/source-manifest.json"),
        ("pressure_result", exp_three, f"experiments/{exp_three}/artifacts/result.json"),
        ("pressure_proof", exp_three, f"experiments/{exp_three}/mathematical-proof.md"),
        ("pressure_verdict", exp_three, f"experiments/{exp_three}/verdict.md"),
        ("pressure_audit", exp_three, f"experiments/{exp_three}/adversarial-audit.md"),
        ("pressure_hypothesis", exp_three, f"experiments/{exp_three}/hypothesis.md"),
        ("pressure_candidates", exp_three, f"experiments/{exp_three}/artifacts/candidates.json"),
        ("pressure_code", exp_three, "code/riemann_pressure.py"),
        ("legacy_certificate_code", exp_two, "code/riemann_certificates.py"),
        ("pressure_runner", exp_three, f"experiments/{exp_three}/run.py"),
        ("pressure_exploration", exp_three, f"experiments/{exp_three}/explore.py"),
        ("legacy_exploration", exp_two, f"experiments/{exp_two}/artifacts/exploration.json"),
        ("parity_result", exp_four, f"experiments/{exp_four}/artifacts/result.json"),
        ("parity_hypothesis", exp_four, f"experiments/{exp_four}/hypothesis.md"),
        ("parity_runner", exp_four, f"experiments/{exp_four}/run.py"),
        ("parity_proof", exp_four, f"experiments/{exp_four}/mathematical-proof.md"),
        ("parity_audit", exp_four, f"experiments/{exp_four}/adversarial-audit.md"),
        ("parity_verdict", exp_four, f"experiments/{exp_four}/verdict.md"),
        ("parity_review", exp_four, f"experiments/{exp_four}/proof-review.json"),
    ]
    payload: dict = {"schema": "riemann-replay-v3", "provenance": []}
    source_bytes: dict[str, bytes] = {}

    def read_source(role: str, experiment: str, relative: str) -> bytes:
        path = f"{problem}/{relative}"
        content = _committed_bytes(path)
        commit = subprocess.run(
            ["git", "log", "-1", "--format=%H", "HEAD", "--", path],
            cwd=ROOT, check=True, capture_output=True, text=True,
        ).stdout.strip()
        payload["provenance"].append({
            "role": role, "source_exp": experiment, "path": path,
            "source_commit": commit, "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        })
        source_bytes[role] = content
        return content

    for role, experiment, relative in specifications:
        content = read_source(role, experiment, relative)
        if role in {"constant_audit", "result", "pressure_result", "parity_result"}:
            payload[role] = json.loads(content)
        elif role == "source_manifest":
            payload["reviewed_on"] = json.loads(content)["reviewed_on"]
    if payload["constant_audit"]["status"] != "PASS":
        raise ValueError("Riemann source and constant audit has not passed")
    audit = payload["result"]["audit"]
    if not (audit["verified"] and audit["independent_sinc_taylor"]):
        raise ValueError("Riemann certificate requires both recorded arithmetic checks")
    pressure = payload["pressure_result"]
    if pressure.get("schema") != "riemann-exp003-results-v1":
        raise ValueError("Unexpected EXP-003 result schema")
    stage_a = pressure["stage_a"]
    if not (stage_a["arithmetic_status"] == "verified"
            and stage_a["replay"]["verified"] is True
            and stage_a["replay"]["independent_sinc_taylor"] is True):
        raise ValueError("Odd-frame reuse requires complete recorded replay")

    def check_provenance(record: dict, *, reused: bool) -> None:
        expected = {
            "pressure_hypothesis": record["hypothesis"]["sha256"],
            "pressure_code": record["certificate_code"]["riemann_pressure.py"],
            "legacy_certificate_code": record["certificate_code"]["riemann_certificates.py"],
            "pressure_runner": record["runner_sha256"],
        }
        if reused:
            expected["certificate"] = record["reused_certificate"]["sha256"]
        for role, recorded in expected.items():
            if hashlib.sha256(source_bytes[role]).hexdigest() != recorded:
                raise ValueError(f"EXP-003 committed input differs: {role}")

    check_provenance(stage_a["provenance"], reused=True)
    stage_b = pressure["stage_b"]
    candidates_hash = hashlib.sha256(source_bytes["pressure_candidates"]).hexdigest()
    if stage_b["candidate_list_sha256"] != candidates_hash:
        raise ValueError("EXP-003 candidate list differs from recorded source")
    candidate_record = json.loads(source_bytes["pressure_candidates"])
    for field, role in (("exploration_source_sha256", "pressure_exploration"),
                        ("prior_exploration_sha256", "legacy_exploration")):
        if candidate_record[field] != hashlib.sha256(source_bytes[role]).hexdigest():
            raise ValueError(f"Pressure exploration source differs: {role}")
    winners = [o for o in stage_b["outcomes"] if o["status"] == "arithmetic_verified"]
    if stage_b["arithmetic_status"] == "verified":
        if not winners:
            raise ValueError("Verified pressure stage has no complete certificate")
    elif stage_b["arithmetic_status"] != "not_confirmed" or winners:
        raise ValueError("Pressure stage status contradicts its outcomes")
    for winner in winners:
        candidate = winner["candidate"]
        if type(candidate) is not int or not 1 <= candidate <= 3:
            raise ValueError("Invalid pressure candidate index")
        frozen = candidate_record["candidates"]
        if candidate > len(frozen) or any(
                Fraction(frozen[candidate - 1][key]) != Fraction(winner[key])
                for key in ("pressure", "epsilon")):
            raise ValueError("Winning pressure parameters differ from the frozen candidate list")
        if Fraction(winner["strict_gain_gate"]["lower"]) <= 0:
            raise ValueError("Pressure result does not record the strict declared gain")
        content = read_source(f"pressure_certificate_{candidate}", exp_three,
            f"experiments/{exp_three}/artifacts/stage-b/candidate-{candidate}/pressure-certificate.json")
        certificate = json.loads(content)
        # This is canonical JSON identity checking, not a numerical verification.
        encoded = (json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n").encode()
        identity = hashlib.sha256(encoded).hexdigest()
        crosscheck = winner["audit"]
        if not (crosscheck["verified"] is True and crosscheck["independent_sinc_taylor"] is True
                and crosscheck["certificate_sha256"] == winner["certificate_sha256"] == identity
                and certificate["unresolved_boxes"] == 0):
            raise ValueError("Pressure certificate requires complete matching arithmetic checks")
        if any(certificate[key] != winner[key] for key in ("theta", "pressure", "epsilon", "cutoff")):
            raise ValueError("Pressure certificate parameters differ from the recorded theorem")
        check_provenance(winner["provenance"], reused=False)
        if winner["provenance"]["candidate_list_sha256"] != candidates_hash:
            raise ValueError("Winning pressure certificate cites a different candidate list")

    parity = payload["parity_result"]
    if (parity.get("schema") != "riemann-exp004-results-v1"
            or parity.get("experiment") != exp_four
            or parity.get("arithmetic_status") != "verified"):
        raise ValueError("EXP-004 requires its verified declared result")
    expected_counts = {
        ("symbolic", "residual_identities"): 2,
        ("symbolic", "multiplicity_regression_cases"): 24,
        ("census", "vectors"): 19683,
        ("census", "sigma_evaluations"): 59049,
        ("relaxation", "cases"): 42,
        ("sharpness", "cases"): 36,
    }
    if any(type(parity[section][field]) is not int or parity[section][field] != value
           for (section, field), value in expected_counts.items()):
        raise ValueError("EXP-004 recorded checks do not cover the declared scope")
    sigma_values = parity["census"]["sigma_values"]
    if sigma_values != [0, 1, 2] or any(type(value) is not int for value in sigma_values):
        raise ValueError("EXP-004 census slack values differ from the declaration")
    threshold = parity["threshold"]
    if any(threshold.get(field, "missing") is not None
           for field in ("classical_a", "kappa", "theta0_numeric", "theta1_decimal")):
        raise ValueError("EXP-004 does not certify numerical seed constants or a new decimal exponent")
    if (threshold["alpha"] != "51/100"
            or threshold["derivative_cap"] != "10000/2601"
            or threshold["c_alpha_upper"] != "-1801/20400"
            or threshold["derivative_formula_verified"] is not True
            or threshold["c_alpha_upper_negative"] is not True):
        raise ValueError("EXP-004 exact threshold comparisons differ from the declared proof")
    proof_status = parity.get("proof_status")
    if (not isinstance(proof_status, dict)
            or proof_status.get("all_height_theorem") != "Not proved by this computational runner"):
        raise ValueError("EXP-004 finite result cannot claim an all-height theorem")

    parity_sources = parity["provenance"]
    declaration = EXP004_DECLARATION
    if parity_sources["declaration_commit"] != declaration:
        raise ValueError("EXP-004 cites a different declaration")
    for role, name in (("parity_hypothesis", "hypothesis"), ("parity_runner", "runner")):
        expected_path = f"{problem}/experiments/{exp_four}/{'hypothesis.md' if name == 'hypothesis' else 'run.py'}"
        record = parity_sources[name]
        if (record["path"] != expected_path
                or record["sha256"] != hashlib.sha256(source_bytes[role]).hexdigest()):
            raise ValueError(f"EXP-004 committed input differs: {role}")
    if parity_sources["hypothesis"]["source_commit"] != declaration:
        raise ValueError("EXP-004 hypothesis is not bound to its declaration")
    if _revision_bytes(parity_sources["hypothesis"]["path"], declaration) != source_bytes["parity_hypothesis"]:
        raise ValueError("EXP-004 hypothesis differs from its declaration revision")
    premise_names = {
        "context/2026-09-12-critical-mass-and-multiplicity-route.md",
        "context/2026-09-12-parity-transfer-adversarial-audit.md",
        "context/2026-09-12-wang-transfer-audit.md",
        f"experiments/{exp_three}/mathematical-proof.md",
    }
    inputs = parity_sources["inputs"]
    if (len(inputs) != len(premise_names)
            or {record["path"] for record in inputs} != {f"{problem}/{name}" for name in premise_names}):
        raise ValueError("EXP-004 requires the complete declared premise set")
    for index, record in enumerate(inputs):
        content = read_source(f"parity_premise_{index}", exp_four, record["path"][len(problem) + 1:])
        if (record["source_commit"] != declaration
                or hashlib.sha256(content).hexdigest() != record["sha256"]):
            raise ValueError("EXP-004 declared premise differs from committed evidence")
        if _revision_bytes(record["path"], declaration) != content:
            raise ValueError("EXP-004 premise differs from its declaration revision")
    for section, filename in (("symbolic", "symbolic.json"), ("census", "census.jsonl"),
                              ("relaxation", "relaxation.json"), ("sharpness", "sharpness.json")):
        record = parity[section]
        if record["raw_artifact"] != filename:
            raise ValueError("EXP-004 raw evidence path differs from its declared role")
        content = read_source(f"parity_{section}_raw", exp_four, f"experiments/{exp_four}/artifacts/{filename}")
        if hashlib.sha256(content).hexdigest() != record["sha256"]:
            raise ValueError(f"EXP-004 raw evidence differs: {section}")

    # Mathematical adjudication is a separately reviewed record. A finite census
    # never promotes itself to an all-height zeta theorem during export.
    review = json.loads(source_bytes["parity_review"])
    if (review.get("schema") != "riemann-exp004-proof-review-v1"
            or review.get("declaration_commit") != declaration
            or review.get("scientific_verdict") != "confirmed"
            or review.get("universal_finite_proof_reviewed") is not True
            or review.get("asymptotic_transfer_reviewed") is not True
            or review.get("numerical_exponent_claimed") is not False):
        raise ValueError("EXP-004 requires separate finite-proof and asymptotic review")
    reviewed_roles = {"parity_result", "parity_hypothesis", "parity_proof", "parity_audit", "parity_verdict"}
    if set(review["source_sha256"]) != reviewed_roles:
        raise ValueError("EXP-004 proof review omits required scientific evidence")
    for role in reviewed_roles:
        if review["source_sha256"][role] != hashlib.sha256(source_bytes[role]).hexdigest():
            raise ValueError(f"EXP-004 proof review no longer matches: {role}")
    payload["parity_review"] = review
    return payload


def run() -> list[Path]:
    DERIVED.mkdir(parents=True, exist_ok=True)
    (DERIVED / "research").mkdir(parents=True, exist_ok=True)
    MANIFESTS.mkdir(parents=True, exist_ok=True)
    artifacts = {
        "portfolio": _read_portfolio(),
        "experiments": {"experiments": _read_experiments()},
        "jacobian": _jacobian_payload(),
        "riemann": _riemann_payload(),
    }
    written: list[Path] = []
    index = {"contract": "research-registry-v1", "cases": []}
    for name, payload in artifacts.items():
        art_rel = f"research/{name}.json"
        art_path = DERIVED / art_rel
        art_path.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n",
                            encoding="utf-8", newline="\n")
        digest = hashlib.sha256(art_path.read_bytes()).hexdigest()
        manifest = {"case_id": name, "artifact": {"path": art_rel,
                    "bytes": art_path.stat().st_size, "sha256": digest},
                    "lane": "precompute", "gate": {"lane": "precompute",
                    "reason": "baked registry export; the web replays it"}}
        if name == "riemann":
            manifest["sources"] = payload["provenance"]
        man_rel = f"manifests/{name}.json"
        (DERIVED / man_rel).write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n",
                                       encoding="utf-8", newline="\n")
        index["cases"].append({"case_id": name, "manifest_path": man_rel})
        written += [art_path, DERIVED / man_rel]
    (MANIFESTS / "index.json").write_text(json.dumps(index, indent=1, sort_keys=True) + "\n",
                                          encoding="utf-8", newline="\n")
    written.append(MANIFESTS / "index.json")
    return written
