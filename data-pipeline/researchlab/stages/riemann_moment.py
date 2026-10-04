"""Admit a reviewed analytic theorem separately from its finite controls."""
from fractions import Fraction as F
import hashlib
import json

from . import riemann_publication

PROBLEM = "problems/number-theory/riemann-hypothesis"
EXP = f"{PROBLEM}/experiments/EXP-028-chirp-separated-moment"
PAPER = "manuscripts/riemann-hypothesis/short-interval-levinson/versions/v0.02"
INPUTS = {
    "moment_hypothesis": f"{EXP}/hypothesis.md",
    "moment_mellin": f"{EXP}/mellin-proof.md",
    "moment_hankel": f"{EXP}/hankel-symbol-proof.md",
    "moment_review_text": f"{EXP}/proof-review.md",
    "moment_verdict": f"{EXP}/verdict.md",
    "moment_native": f"{EXP}/artifacts/conditional-onset.json",
    "moment_independent": f"{EXP}/artifacts/independent-conditional.json",
    "moment_adversarial": f"{EXP}/artifacts/adversarial-exponents.json",
    "moment_runner": f"{EXP}/run.py",
    "moment_independent_runner": f"{EXP}/independent_control.py",
    "moment_adversarial_runner": f"{EXP}/adversarial_control.py",
    "moment_independent_declaration": f"{EXP}/independent-control-declaration.md",
    "moment_adversarial_declaration": f"{EXP}/adversarial-declaration.md",
    "moment_detector": f"{PROBLEM}/experiments/EXP-010-levinson-parity-transfer/artifacts/canonical/result.json",
    "moment_interval_toolkit": f"{PROBLEM}/experiments/EXP-026-multiplicity-defect-retention/independent_compact.py",
    "moment_transform": f"{PROBLEM}/experiments/EXP-027-shifted-voronoi-dual/proof.md",
    "moment_gaussian": f"{PROBLEM}/experiments/EXP-024-gaussian-mellin-reduction/proof.md",
    "moment_paper": f"{PAPER}/main.pdf",
    "moment_tex": f"{PAPER}/main.tex",
    "moment_render": f"{PAPER}/render-review.json",
    "moment_archive": f"{PAPER}/source-replay.json",
    "moment_publication": f"{PAPER}/publication-receipt.json",
    "moment_review": f"{EXP}/proof-review.json",
    "moment_current_publication": f"{PAPER}/current-publication.json",
    "moment_companion": f"{PAPER}/evidence-companion.json",
}


def validate(raw: dict[str, bytes]) -> dict:
    def require(condition, message):
        if not condition:
            raise ValueError(f"Short-window moment evidence rejected: {message}")

    def record(role, schema):
        require(role in raw, f"missing source {role}")
        data = json.loads(raw[role])
        require(data.get("schema") == schema, f"schema {role}")
        return data

    def runtime_hash_matches(role, digest):
        # Frozen Windows receipts bind physical CRLF bytes. Git provenance is LF.
        # Accept only these two exact serializations of the same committed source.
        source = raw[role]
        return digest in {hashlib.sha256(source).hexdigest(),
                          hashlib.sha256(source.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest()}

    review = record("moment_review", "exp028-complete-proof-review-v1")
    separate = ("moment_current_publication", "moment_companion")
    require(all(role in raw for role in separate), "missing publication correction source")
    expected = {k: v for k, v in INPUTS.items() if k != "moment_review" and k not in separate}
    require(review.get("source_paths") == expected, "complete source path set")
    hashes = review.get("source_sha256", {})
    require(set(hashes) == set(expected), "complete source hash set")
    for role in expected:
        require(role in raw and hashlib.sha256(raw[role]).hexdigest() == hashes[role],
                f"committed source bytes {role}")
    require(review.get("scientific_verdict") == "confirmed-internal-relative-to-attributed-inputs"
            and all(review.get(k) is True for k in
                    ("analytic_moment_reviewed", "two_analytic_derivations", "compact_window_loss_charged")),
            "separate analytic review")
    require(all(review.get(k) is False for k in
                ("external_peer_review", "worldwide_priority_confirmed", "rh_solved", "effective_height")),
            "claim boundary")
    require(len(review.get("imported_inputs", [])) == 3, "attributed theorem inputs")
    theta, nu, eta = (F(review[k]) for k in ("theta", "nu", "eta"))
    require((theta, nu, eta) == (F(5339, 10000), F(349, 10000), F(1, 100000)), "fixed detector parameters")
    e1 = F(17, 20)*(1-2*(theta-eta))+F(33, 20)*nu
    e2 = 1-2*(theta-eta)+F(15, 8)*nu
    require(e1 < 0 and e2 < 0 and [str(e1), str(e2)] == review["charged_exponents"],
            "charged smoothing margin")

    native = record("moment_native", "exp028-conditional-onset-v1")
    independent = record("moment_independent", "exp028-independent-conditional-v1")
    adversarial = record("moment_adversarial", "exp028-adversarial-exponents-v1")
    require(native.get("passed_conditional_controls") is True and independent.get("passed") is True
            and adversarial.get("passed") is True, "finite arithmetic controls")
    ia, aa = independent["audit"], adversarial["audit"]
    require(native.get("analytic_moment_theorem_proved") is False
            and ia.get("analytic_moment_theorem_proved") is False
            and aa.get("analytic_moment_theorem_proved") is False, "historical arithmetic scope")
    for receipt in (native, ia):
        require(receipt["detector_receipt_sha256"] == hashes["moment_detector"], "frozen detector binding")
        require(receipt["theta"] == str(theta) and receipt["nu"] == str(nu), "arithmetic parameters")
        require([receipt["E1"], receipt["E2"]] == ["-9/200000", "-189/80000"], "un-narrowed exponents")
    require(runtime_hash_matches("moment_interval_toolkit", ia["interval_toolkit_sha256"]),
            "independent interval toolkit")
    for receipt, prefix in ((independent, "moment_independent"), (adversarial, "moment_adversarial")):
        require(runtime_hash_matches(prefix + "_runner", receipt["auditor_sha256"])
                and runtime_hash_matches(prefix + "_declaration", receipt["declaration_sha256"]),
                "auditor declarations")
    require(aa["charged_exponents"] == review["charged_exponents"] and aa["eta"] == str(eta)
            and aa["gaussian_theta"] == str(theta-eta) and aa["exact_dyadic_boxes"] == 7430
            and len(aa["negative_controls"]) == 5 and all(aa["negative_controls"].values()),
            "adversarial dyadic and loss controls")
    require(len(ia["negative_controls"]) == 3 and all(ia["negative_controls"].values()), "independent negative controls")
    detector = json.loads(raw["moment_detector"])
    kappa = str(F(next(row["kappa"]["lower"] for row in detector["detector_constants"] if F(row["nu"]) == nu)))
    require(native["certified_kappa_lower"] == kappa, "detector lower bound")
    floor = F(review["simple_density_floor"])
    require(floor == F(797046631827, 2000000000000000)
            and F(ia["conditional_parity"]["lower"]) > floor, "independent positive density")

    publication = record("moment_publication", "levinson-v002-zenodo-publication-v1")
    render = record("moment_render", "levinson-v002-render-review-v1")
    archive = record("moment_archive", "levinson-v002-source-replay-v1")
    require(publication.get("passed") is True and publication.get("status") == "published"
            and publication["version"] == "0.02" and publication["version_doi"] == "10.5281/zenodo.23132248"
            and publication["concept_doi"] == "10.5281/zenodo.22984154"
            and publication["external_peer_review"] is False, "publication status")
    require(publication["pdf_sha256"] == hashes["moment_paper"] == render["pdf_sha256"]
            and publication["tex_sha256"] == hashes["moment_tex"] == render["tex_sha256"], "published manuscript bytes")
    require(render.get("passed") is True and render["pages"] == 14 and len(render["images"]) == 14,
            "complete rendered review")
    require(publication["render_review_sha256"] == hashes["moment_render"]
            and publication["source_replay_sha256"] == hashes["moment_archive"], "publication review bindings")
    require(archive.get("passed") is True and archive["members"] == 80
            and archive["all_members_crc_size_sha256_verified"] is True
            and archive["pdf_sha256"] == hashes["moment_paper"]
            and archive["tex_sha256"] == hashes["moment_tex"], "source archive replay")
    require(set(archive["extracted_archive_auditors"]) == {"run", "independent_control", "adversarial_control"}
            and all(x.get("passed") is True for x in archive["extracted_archive_auditors"].values()),
            "extracted auditors")
    # This frozen receipt describes the original deposit, not its current file set.
    files = publication["files"]
    require(len(files) == 2 and all(x.get("live_bytes_verified") is True for x in files), "public download checks")
    require(next(x for x in files if x["name"].endswith('.pdf'))["sha256"] == hashes["moment_paper"]
            and next(x for x in files if x["name"].endswith('.zip'))["sha256"]
            == publication["source_archive_sha256"] == archive["archive_sha256"], "published file bindings")
    current, companion = riemann_publication.admit(publication, raw["moment_current_publication"],
                                                  raw["moment_companion"], raw["moment_paper"])
    current_hashes = {**hashes, **{k: hashlib.sha256(raw[k]).hexdigest() for k in separate}}
    return {"schema": "riemann-short-window-moment-v1", "accepted": True,
            "scientific_verdict": review["scientific_verdict"], "theta": str(theta), "nu": str(nu),
            "eta": str(eta), "gaussian_theta": str(theta-eta), "moment_range": review["moment_range"],
            "charged_exponents": review["charged_exponents"], "kappa_lower": kappa,
            "simple_density_floor": str(floor), "simple_density_decimal": "0.0003985233159135",
            "previous_onset": "0.534", "onset": "0.5339", "adversarial_boxes": 7430,
            "analytic_moment_reviewed": True, "arithmetic_alone_proves_theorem": False,
            "external_peer_review": False, "worldwide_priority_confirmed": False,
            "effective_height": False, "rh_solved": False,
            "publication": current, "evidence_companion": companion, "source_sha256": current_hashes,
            "imported_inputs": review["imported_inputs"], "trust_boundary": review["trust_boundary"]}
