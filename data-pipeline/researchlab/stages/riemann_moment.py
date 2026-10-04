"""Admit analytic review, finite controls and publication as separate evidence."""
from fractions import Fraction as F
import hashlib
import json

PROBLEM = "problems/number-theory/riemann-hypothesis"
EXP = f"{PROBLEM}/experiments/EXP-029-mellin-frequency-average"
PAPER = "manuscripts/riemann-hypothesis/short-interval-levinson/versions/v0.03"
CURRENT = {
    "hypothesis": ("hypothesis.md", "hypothesis_md"),
    "mellin": ("analytic-proof-candidate.md", "analytic_proof_candidate_md"),
    "review_text": ("proof-review.md", "proof_review_md"), "verdict": ("verdict.md", "verdict_md"),
    "frequency_runner": ("run.py", "run_py"), "runner": ("conditional_control.py", "conditional_control_py"),
    "independent_runner": ("independent_control.py", "independent_control_py"),
    "adversarial_runner": ("adversarial_control.py", "adversarial_control_py"),
    "independent_declaration": ("independent-control-declaration.md", "independent_control_declaration_md"),
    "adversarial_declaration": ("adversarial-declaration.md", "adversarial_declaration_md"),
    "frequency": ("artifacts/frequency-controls.json", "artifacts/frequency_controls_json"),
    "native": ("artifacts/conditional-native.json", "artifacts/conditional_native_json"),
    "independent": ("artifacts/conditional-rational.json", "artifacts/conditional_rational_json"),
    "adversarial": ("artifacts/adversarial-raw-cost.json", "artifacts/adversarial_raw_cost_json"),
}
PRIOR = {
    "detector": ("experiments/EXP-010-levinson-parity-transfer/artifacts/canonical/result.json", "detector"),
    "counting": ("experiments/EXP-010-levinson-parity-transfer/mathematical-proof.md", "counting"),
    "parity": ("experiments/EXP-006-hilbert-parity-compression/mathematical-proof.md", "parity"),
    "transform": ("experiments/EXP-027-shifted-voronoi-dual/proof.md", "transform"),
    "gaussian": ("experiments/EXP-024-gaussian-mellin-reduction/proof.md", "gaussian"),
    "profile": ("experiments/EXP-028-chirp-separated-moment/mellin-proof.md", "profile"),
    "prior_review": ("experiments/EXP-028-chirp-separated-moment/proof-review.json", "prior_review"),
    "interval_toolkit": ("experiments/EXP-026-multiplicity-defect-retention/independent_compact.py", "interval_toolkit"),
    "preflight": ("context/2026-10-04-mellin-frequency-preflight.md", "source_preflight"),
}
ANALYTIC_ROLES = {**{f"moment_{k}": f"current_{v[1]}" for k, v in CURRENT.items()},
                  **{f"moment_{k}": v[1] for k, v in PRIOR.items()}}
INPUTS = {**{f"moment_{k}": f"{EXP}/{v[0]}" for k, v in CURRENT.items()},
          **{f"moment_{k}": f"{PROBLEM}/{v[0]}" for k, v in PRIOR.items()},
          "moment_review": f"{EXP}/proof-review.json",
          "moment_paper": f"{PAPER}/main.pdf", "moment_tex": f"{PAPER}/main.tex",
          "moment_render": f"{PAPER}/render-review.json", "moment_archive": f"{PAPER}/source-replay.json",
          "moment_publication": f"{PAPER}/publication-receipt.json", "moment_delivery": f"{EXP}/publication-review.json"}


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
        source = raw[role]
        return digest in {hashlib.sha256(source).hexdigest(), hashlib.sha256(
            source.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")).hexdigest()}

    delivery = record("moment_delivery", "exp029-publication-delivery-review-v1")
    expected = {k: v for k, v in INPUTS.items() if k != "moment_delivery"}
    require(delivery.get("passed") is True and delivery.get("source_paths") == expected
            and delivery.get("analytic_role_map") == ANALYTIC_ROLES, "complete delivery paths")
    hashes = delivery.get("source_sha256", {})
    require(set(hashes) == set(expected), "complete source hash set")
    for role in expected:
        require(role in raw and hashlib.sha256(raw[role]).hexdigest() == hashes[role], f"committed source bytes {role}")
    review = record("moment_review", "exp029-complete-proof-review-v1")
    require(review.get("source_paths") == {v: INPUTS[k] for k, v in ANALYTIC_ROLES.items()}, "analytic source paths")
    require(set(review.get("source_sha256", {})) == set(ANALYTIC_ROLES.values())
            and set(review.get("source_lf_sha256", {})) == set(ANALYTIC_ROLES.values()), "analytic source hashes")
    for role, key in ANALYTIC_ROLES.items():
        require(review["source_lf_sha256"][key] == hashes[role]
                and runtime_hash_matches(role, review["source_sha256"][key]), "analytic source binding")
    require(review.get("scientific_verdict") == "confirmed-internal-relative-to-attributed-inputs"
            and all(review.get(k) is True for k in
                    ("analytic_moment_reviewed", "two_analytic_derivations", "compact_window_loss_charged"))
            and review.get("external_trilinear_theorem_used") is False, "separate analytic review")
    for receipt in (review, delivery):
        require(all(receipt.get(k) is False for k in
                    ("external_peer_review", "worldwide_priority_confirmed", "rh_solved", "effective_height")), "claim boundary")
    require(len(review.get("imported_inputs", [])) == 3, "attributed theorem inputs")
    theta, nu, eta = (F(review[k]) for k in ("theta", "nu", "eta"))
    require((theta, nu, eta) == (F(527, 1000), F(499, 10000), F(1, 100000)), "fixed detector parameters")
    charged = [str(1 + nu - 2*(theta-eta)), str(1 + 3*nu - F(5, 2)*(theta-eta))]
    require(all(F(e) < 0 for e in charged) and charged == review["charged_exponents"], "charged smoothing margin")

    native = record("moment_native", "exp029-conditional-native-parity-v1")
    independent = record("moment_independent", "exp029-independent-conditional-parity-v1")
    adversarial = record("moment_adversarial", "exp029-adversarial-raw-cost-v1")
    frequency = record("moment_frequency", "exp029-finite-frequency-controls-v1")
    aa = adversarial["audit"]
    require(native.get("passed_conditional_controls") is True and independent.get("passed_conditional_controls") is True
            and adversarial.get("passed") is True and frequency.get("passed") is True, "finite controls")
    for receipt in (native, independent, aa, frequency):
        require(receipt.get("analytic_moment_theorem_proved") is False, "historical arithmetic scope")
        require((receipt["theta"], receipt["nu"], receipt["eta"]) == (str(theta), str(nu), str(eta)), "arithmetic parameters")
    for receipt, role, declaration in ((native, "moment_runner", "moment_independent_declaration"),
            (independent, "moment_independent_runner", "moment_independent_declaration"),
            (adversarial, "moment_adversarial_runner", "moment_adversarial_declaration"),
            (frequency, "moment_frequency_runner", None)):
        require(runtime_hash_matches(role, receipt["runner_sha256"]), "auditor source")
        if declaration:
            require(runtime_hash_matches(declaration, receipt["declaration_sha256"]), "auditor declaration")
    for receipt in (native, independent, frequency):
        require(receipt["hypothesis_sha256"] == hashes["moment_hypothesis"]
                and [receipt["charged_E1"], receipt["charged_E2"]] == charged, "finite exponent binding")
    for receipt in (native, independent):
        require(receipt["detector_receipt_sha256"] == hashes["moment_detector"]
                and receipt.get("zero_detector_rejected") is True, "frozen detector binding")
    require(runtime_hash_matches("moment_interval_toolkit", independent["interval_toolkit_sha256"]), "interval toolkit")
    require(aa["charged_exponents"] == charged and aa["raw_cost_boxes"] == 6426
            and aa["principal_N_slopes"] == ["1/2", "1"] and aa["tail_N_slopes_before_epsilon"] == ["-7/2", "-3"]
            and aa["gcd_decay_powers"] == ["2", "4"] and aa["range_transitions"] == ["4/7", "12/13"], "raw-cost controls")
    nc = aa["negative_controls"]
    require(nc["omitted_collisions"]["true_normalized_mass"] == 36
            and nc["omitted_collisions"]["wrong_diagonal_only_mass"] == 6
            and nc["whole_line_unweighted_L2"]["analytic_divergence"] is True
            and all(nc[k] is True for k in ("oversized_window_loss_rejected", "zero_strict_margin_rejected",
                                           "uncontrolled_tail_rejected")), "adversarial negative controls")
    require((frequency["dyadic_blocks"], frequency["triples"], frequency["exponent_boxes"]) == (432, 524400, 180),
            "frequency census")
    witness = independent["spacing_N_omission_witness"]
    require(witness["N"] == 32 and F(witness["log_gap_upper"]) < F(witness["wrong_delta"])
            and F(witness["proper_delta"]) == F(1, 512), "proper spacing refutation")
    detector = json.loads(raw["moment_detector"])
    kappa = str(F(next(row["kappa"]["lower"] for row in detector["detector_constants"] if F(row["nu"]) == nu)))
    require(native["certified_kappa_lower"] == kappa, "detector lower bound")
    floor = F(review["simple_density_floor"])
    require(floor == F(5947542001, 10**13) and F(independent["conditional_density"]["lower"]) > floor,
            "independent positive density")

    publication = record("moment_publication", "levinson-v003-zenodo-publication-v1")
    render = record("moment_render", "levinson-v003-render-review-v1")
    archive = record("moment_archive", "levinson-v003-source-replay-v1")
    require(publication.get("passed") is True and publication.get("status") == "published"
            and publication["version"] == delivery["version"] == "0.03"
            and publication["version_doi"] == delivery["version_doi"] == "10.5281/zenodo.23134787"
            and publication["concept_doi"] == delivery["concept_doi"] == "10.5281/zenodo.22984154"
            and publication["external_peer_review"] is False, "publication status")
    require(publication["pdf_sha256"] == hashes["moment_paper"] == render["pdf_sha256"]
            and publication["tex_sha256"] == hashes["moment_tex"] == render["tex_sha256"], "published manuscript bytes")
    require(render.get("passed") is True and render["pages"] == delivery["rendered_pages"] == 17
            and len(render["images"]) == 17, "complete rendered review")
    require(publication["render_review_sha256"] == hashes["moment_render"]
            and publication["source_replay_sha256"] == hashes["moment_archive"], "publication review bindings")
    require(archive.get("passed") is True and archive["members"] == delivery["source_archive_members"] == 85
            and archive["all_members_crc_size_sha256_verified"] is True
            and archive["all_23_analytic_source_bindings_verified"] is True
            and archive["pdf_sha256"] == hashes["moment_paper"] and archive["tex_sha256"] == hashes["moment_tex"],
            "source archive replay")
    auditors = {"exp029-run", "exp029-conditional_control", "exp029-independent_control", "exp029-adversarial_control",
                "exp028-run", "exp028-independent_control", "exp028-adversarial_control"}
    require(set(archive["extracted_archive_auditors"]) == auditors and delivery["extracted_auditors"] == 7
            and all(x.get("passed") is True for x in archive["extracted_archive_auditors"].values()), "extracted auditors")
    files = publication["files"]
    require(len(files) == 2 and all(x.get("live_bytes_verified") is True for x in files), "public download checks")
    require(next(x for x in files if x["name"].endswith('.pdf'))["sha256"] == hashes["moment_paper"]
            and next(x for x in files if x["name"].endswith('.zip'))["sha256"]
            == publication["source_archive_sha256"] == archive["archive_sha256"], "published file bindings")
    return {"schema": "riemann-short-window-moment-v2", "accepted": True,
            "scientific_verdict": review["scientific_verdict"], "theta": str(theta), "nu": str(nu),
            "eta": str(eta), "gaussian_theta": str(theta-eta), "moment_range": review["moment_range"],
            "charged_exponents": charged, "kappa_lower": kappa,
            "simple_density_floor": str(floor), "simple_density_decimal": "0.0005947542001",
            "previous_onset": "0.5339", "onset": "0.527", "adversarial_boxes": 6426,
            "frequency_blocks": 432, "frequency_triples": 524400, "external_trilinear_theorem_used": False,
            "analytic_moment_reviewed": True, "arithmetic_alone_proves_theorem": False,
            "external_peer_review": False, "worldwide_priority_confirmed": False, "effective_height": False,
            "rh_solved": False, "publication": publication, "source_sha256": hashes,
            "imported_inputs": review["imported_inputs"], "trust_boundary": review["trust_boundary"]}
