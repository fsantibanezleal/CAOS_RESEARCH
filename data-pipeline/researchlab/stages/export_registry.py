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
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
DERIVED = ROOT / "data" / "derived"
MANIFESTS = DERIVED / "manifests"
EXP004_DECLARATION = "e03413b2301bf45ca68ff6e945f25add9a1c3a89"
EXP005_DECLARATION = "6fd59fec51dda399de40e0327107dba42deb5b45"
EXP005_CANONICAL = "864fe6b7bee69c6bdac72e72fbfb88b49ac0fef2"
EXP006_DECLARATION = "b1febcf8a6d5830218e1df386af1e8a92c3037be"
EXP006_CANONICAL = "0d736fa22ce7e833200381a32e8cc89f77c660e8"


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
             "now": "false for SU(2) and for SU(N), N >= 24; SU(N) for 3 <= N <= 23 and other groups "
                    "not decided (EXP-136)",
             "chain": "Mathieu(SU(N)) implies invertibility of Keller maps x - h of C^N, h homogeneous"},
            {"name": "Dixmier conjecture", "prior": "open (1968)",
             "now": "false for rank n >= 3; ranks 1 and 2 open (EXP-136)",
             "chain": "Dixmier(n) implies JC(n); JC(2n) implies Dixmier(n)"},
            {"name": "Poisson conjecture", "prior": "open (2007)",
             "now": "false for index n >= 3; indices 1 and 2 open (EXP-136)",
             "chain": "JC(2n) implies Poisson(n) implies Dixmier(n) implies JC(n)"},
            {"name": "Gaussian moments conjecture", "prior": "open (2015)",
             "now": "false for n >= 3 (explicit); true for n = 1; n = 2 proof claimed (EXP-136)",
             "chain": "GMC implies JC"},
            {"name": "Zhao vanishing conjecture", "prior": "open (2004)",
             "now": "false; explicit witness in 48 variables (EXP-041)", "chain": "vanishing equivalent to JC"},
            {"name": "Image conjecture", "prior": "open (2010)",
             "now": "false in some dimension", "chain": "Image implies vanishing"},
            {"name": "Symmetric / gradient JC", "prior": "open reduction (2005)",
             "now": "false; explicit witness in dimension 48 (EXP-041)",
             "chain": "symmetric JC stably equivalent to JC"},
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
    exp_five = "EXP-005-local-selberg-transfer"
    exp_six = "EXP-006-hilbert-parity-compression"
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
        ("local_result", exp_five, f"experiments/{exp_five}/artifacts/canonical/result.json"),
        ("local_receipt", exp_five,
         f"experiments/{exp_five}/artifacts/canonical/execution-receipt.json"),
        ("local_hypothesis", exp_five, f"experiments/{exp_five}/hypothesis.md"),
        ("local_runner", exp_five, f"experiments/{exp_five}/run.py"),
        ("local_proof", exp_five, f"experiments/{exp_five}/mathematical-proof.md"),
        ("local_audit", exp_five, f"experiments/{exp_five}/adversarial-audit.md"),
        ("local_verdict", exp_five, f"experiments/{exp_five}/verdict.md"),
        ("local_review", exp_five, f"experiments/{exp_five}/proof-review.json"),
        ("hilbert_result", exp_six, f"experiments/{exp_six}/artifacts/canonical/result.json"),
        ("hilbert_receipt", exp_six,
         f"experiments/{exp_six}/artifacts/canonical/execution-receipt.json"),
        ("hilbert_hypothesis", exp_six, f"experiments/{exp_six}/hypothesis.md"),
        ("hilbert_runner", exp_six, f"experiments/{exp_six}/run.py"),
        ("hilbert_proof", exp_six, f"experiments/{exp_six}/mathematical-proof.md"),
        ("hilbert_audit", exp_six, f"experiments/{exp_six}/adversarial-audit.md"),
        ("hilbert_verdict", exp_six, f"experiments/{exp_six}/verdict.md"),
        ("hilbert_review", exp_six, f"experiments/{exp_six}/proof-review.json"),
    ]
    payload: dict = {"schema": "riemann-replay-v5", "provenance": []}
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
        if role in {"constant_audit", "result", "pressure_result", "parity_result",
                    "local_result", "hilbert_result"}:
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

    local = payload["local_result"]
    if (local.get("schema") != "riemann-exp005-results-v1"
            or local.get("status") != "pass" or local.get("passed") is not True):
        raise ValueError("EXP-005 requires its passing canonical result")
    expected_checks = {
        "baseline_negative", "boundary_rejected", "c3_interval_ordered",
        "curve_simple_positive", "e_interval", "fixed_u_simple_positive",
        "interval_contains_c", "interval_contains_curve", "interval_contains_fixed",
        "mollifier_below_quarter", "negative_theta_control", "source_hashes",
        "sqrt2_interval", "strict_localization_margin",
    }
    if set(local.get("checks", {})) != expected_checks or not all(local["checks"].values()):
        raise ValueError("EXP-005 canonical result omits a declared exact control")
    if (local["claim_boundary"].get("rh_solved") is not False
            or local["boundary_control"].get("accepted") is not False
            or local["boundary_control"]["margin"]["numerator"] != "0"):
        raise ValueError("EXP-005 claim or mollifier-boundary control differs from the verdict")
    parameters = local["parameters"]
    if (parameters["theta"]["numerator"] != "273"
            or parameters["theta"]["denominator"] != "500"
            or parameters["negative_control_theta"]["numerator"] != "5459"
            or parameters["negative_control_theta"]["denominator"] != "10000"
            or parameters["mollifier_exponent_u"]["numerator"] != "2299"
            or parameters["mollifier_exponent_u"]["denominator"] != "100000"):
        raise ValueError("EXP-005 threshold or fixed mollifier parameters changed")

    def certified_decimal(record: dict) -> Decimal:
        # EXP-005 keeps very large exact numerator/denominator strings. Their
        # independently checked decimal fields avoid Python's defensive
        # integer-string limit during a public-data bake.
        return Decimal(record["decimal"])

    positive = local["positive_point"]
    if (certified_decimal(positive["fixed_u_simple_lower"])
            <= certified_decimal(parameters["simple_gate"])
            or certified_decimal(positive["simple_curve_lower"]) <= 0
            or certified_decimal(positive["localization_exponent_margin"]) <= 0
            or certified_decimal(local["negative_control"]["simple_curve_upper"]) >= 0):
        raise ValueError("EXP-005 exact positive, negative, or strict-margin gate failed")
    identity = local["execution_identity"]
    if (identity.get("head") != EXP005_CANONICAL
            or identity.get("tracked_clean_at_start") is not True
            or identity.get("hypothesis_sha256")
            != hashlib.sha256(source_bytes["local_hypothesis"]).hexdigest()
            or identity.get("run_py_sha256")
            != hashlib.sha256(source_bytes["local_runner"]).hexdigest()):
        raise ValueError("EXP-005 execution identity differs from committed evidence")
    local_hypothesis_path = f"{problem}/experiments/{exp_five}/hypothesis.md"
    if _revision_bytes(local_hypothesis_path, EXP005_DECLARATION) != source_bytes["local_hypothesis"]:
        raise ValueError("EXP-005 hypothesis differs from its declaration revision")
    result_sha256 = hashlib.sha256(source_bytes["local_result"]).hexdigest()
    receipt = json.loads(source_bytes["local_receipt"])
    if (receipt.get("schema") != "riemann-exp005-execution-receipt-v1"
            or receipt.get("status") != "pass"
            or receipt.get("result_sha256") != result_sha256
            or receipt.get("git", {}).get("head") != EXP005_CANONICAL
            or receipt.get("git", {}).get("tracked_clean_at_start") is not True):
        raise ValueError("EXP-005 execution receipt does not bind the canonical result")
    local_review = json.loads(source_bytes["local_review"])
    if (local_review.get("schema") != "riemann-exp005-proof-review-v1"
            or local_review.get("declaration_commit") != EXP005_DECLARATION
            or local_review.get("canonical_commit") != EXP005_CANONICAL
            or local_review.get("scientific_verdict") != "confirmed"
            or local_review.get("analytic_localization_reviewed") is not True
            or local_review.get("exact_certificate_reviewed") is not True):
        raise ValueError("EXP-005 requires separate analytic and exact-certificate review")
    local_review_roles = {
        "hypothesis": "local_hypothesis",
        "mathematical_proof": "local_proof",
        "adversarial_audit": "local_audit",
        "result": "local_result",
        "verdict": "local_verdict",
    }
    if set(local_review.get("source_sha256", {})) != set(local_review_roles):
        raise ValueError("EXP-005 proof review omits required scientific evidence")
    for reviewed_name, role in local_review_roles.items():
        if (local_review["source_sha256"][reviewed_name]
                != hashlib.sha256(source_bytes[role]).hexdigest()):
            raise ValueError(f"EXP-005 proof review no longer matches: {role}")
    payload["local_review"] = local_review

    # EXP-006 keeps the analytic theorem separate from the finite exact
    # certificate. The exporter checks identities and byte bindings only; it
    # does not rerun or promote the mathematical proof.
    hilbert_test_path = "tests/test_riemann_hilbert_parity.py"
    hilbert_test = _committed_bytes(hilbert_test_path)
    hilbert_test_commit = subprocess.run(
        ["git", "log", "-1", "--format=%H", "HEAD", "--", hilbert_test_path],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    payload["provenance"].append({
        "role": "hilbert_test", "source_exp": exp_six, "path": hilbert_test_path,
        "source_commit": hilbert_test_commit, "bytes": len(hilbert_test),
        "sha256": hashlib.sha256(hilbert_test).hexdigest(),
    })
    source_bytes["hilbert_test"] = hilbert_test

    hilbert = payload["hilbert_result"]
    if (hilbert.get("schema") != "riemann-exp006-results-v2"
            or hilbert.get("status") != "pass" or hilbert.get("passed") is not True):
        raise ValueError("EXP-006 requires its passing strengthened canonical result")
    expected_hilbert_checks = {
        "c3_interval_ordered", "c6_interval_ordered", "e_interval",
        "finite_census", "finite_census_has_all_regimes",
        "independent_interval_contained", "old_linear_negative",
        "rank_six_sensitivity_stronger", "root_lower_negative",
        "root_monotone_conditions", "root_upper_positive",
        "scalar_headlines_allow_zero", "source_hashes", "sqrt2_interval",
        "strong_bound_improves_weak", "strong_bound_positive",
        "target_below_wang_root", "weak_bound_positive",
    }
    if (set(hilbert.get("checks", {})) != expected_hilbert_checks
            or not all(hilbert["checks"].values())):
        raise ValueError("EXP-006 canonical result omits a declared exact control")
    if hilbert["claim_boundary"].get("rh_solved") is not False:
        raise ValueError("EXP-006 claim boundary changed")
    if hilbert["finite_census"] != {
            **hilbert["finite_census"], "cases": 18479, "equality_cases": 135,
            "strict_cases": 18340, "empty_dimension_cases": 4}:
        raise ValueError("EXP-006 finite census differs from the declared scope")
    hilbert_parameters = hilbert["parameters"]
    expected_parameters = {
        "theta": ("5459", "10000"),
        "root_lower_theta": ("136471", "250000"),
        "root_upper_theta": ("109177", "200000"),
    }
    for name, (numerator, denominator) in expected_parameters.items():
        if (hilbert_parameters[name]["numerator"] != numerator
                or hilbert_parameters[name]["denominator"] != denominator):
            raise ValueError(f"EXP-006 parameter changed: {name}")
    target = hilbert["target"]
    if (certified_decimal(target["c_upper"]) >= 0
            or certified_decimal(target["old_linear_upper"]) >= 0
            or certified_decimal(target["strong_simple_lower"])
            <= certified_decimal(hilbert_parameters["simple_gate"])
            or certified_decimal(target["strong_simple_lower"])
            <= certified_decimal(target["weak_simple_upper"])
            or certified_decimal(hilbert["root_bracket"]["lower"]["root_function_upper"]) >= 0
            or certified_decimal(hilbert["root_bracket"]["upper"]["root_function_lower"]) <= 0):
        raise ValueError("EXP-006 target, improvement, or root-bracket gate failed")
    if (hilbert["scalar_headline_barrier"].get("passed") is not True
            or not all(hilbert["scalar_headline_barrier"]["checks"].values())):
        raise ValueError("EXP-006 scalar barrier witness is incomplete")
    hilbert_identity = hilbert["execution_identity"]
    if (hilbert_identity.get("head") != EXP006_CANONICAL
            or hilbert_identity.get("tracked_clean_at_start") is not True
            or hilbert_identity.get("hypothesis_sha256")
            != hashlib.sha256(source_bytes["hilbert_hypothesis"]).hexdigest()
            or hilbert_identity.get("run_py_sha256")
            != hashlib.sha256(source_bytes["hilbert_runner"]).hexdigest()):
        raise ValueError("EXP-006 execution identity differs from committed evidence")
    hilbert_result_sha256 = hashlib.sha256(source_bytes["hilbert_result"]).hexdigest()
    hilbert_receipt = json.loads(source_bytes["hilbert_receipt"])
    if (hilbert_receipt.get("schema") != "riemann-exp006-execution-receipt-v1"
            or hilbert_receipt.get("status") != "pass"
            or hilbert_receipt.get("result_sha256") != hilbert_result_sha256
            or hilbert_receipt.get("git", {}).get("head") != EXP006_CANONICAL
            or hilbert_receipt.get("git", {}).get("tracked_clean_at_start") is not True):
        raise ValueError("EXP-006 execution receipt does not bind the canonical result")
    original_hypothesis = _revision_bytes(
        f"{problem}/experiments/{exp_six}/hypothesis.md", EXP006_DECLARATION,
    )
    if b"Q(N-O)" not in original_hypothesis or b"0.5458<" not in original_hypothesis:
        raise ValueError("EXP-006 original declaration does not contain the frozen target")
    hilbert_review = json.loads(source_bytes["hilbert_review"])
    if (hilbert_review.get("schema") != "riemann-exp006-proof-review-v1"
            or hilbert_review.get("declaration_commit") != EXP006_DECLARATION
            or hilbert_review.get("canonical_commit") != EXP006_CANONICAL
            or hilbert_review.get("scientific_verdict") != "confirmed"
            or hilbert_review.get("analytic_transfer_reviewed") is not True
            or hilbert_review.get("exact_certificate_reviewed") is not True):
        raise ValueError("EXP-006 requires separate theorem and certificate review")
    hilbert_review_roles = {
        "hypothesis": "hilbert_hypothesis",
        "mathematical_proof": "hilbert_proof",
        "adversarial_audit": "hilbert_audit",
        "result": "hilbert_result",
        "verdict": "hilbert_verdict",
        "runner": "hilbert_runner",
        "focused_test": "hilbert_test",
    }
    if set(hilbert_review.get("source_sha256", {})) != set(hilbert_review_roles):
        raise ValueError("EXP-006 proof review omits required scientific evidence")
    for reviewed_name, role in hilbert_review_roles.items():
        if (hilbert_review["source_sha256"][reviewed_name]
                != hashlib.sha256(source_bytes[role]).hexdigest()):
            raise ValueError(f"EXP-006 proof review no longer matches: {role}")
    payload["hilbert_review"] = hilbert_review
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
