"""Package exact runtime bytes only after complete cover and transfer audits."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

from transfer_audit import require, transfer

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
REPO = HERE.parents[4]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def package(directory, baseline, archive, scratch_root):
    result = transfer(directory)
    controls_path = directory/"actual-cover-corruption-controls.json"
    controls = json.loads(controls_path.read_bytes())
    require(controls.get("passed") is True and len(controls["cases"]) == 12 and
            all(case["rejected"] is True for case in controls["cases"]) and
            controls["actual_cover_reports_sha256"] == result["reports_sha256"] and
            controls["control_source_sha256"] == digest((HERE/"actual_cover_controls.py").read_bytes()),
            "actual complete-cover controls missing or unbound")
    binding = json.loads((directory/"run-binding.json").read_bytes())
    native = json.loads((HERE/"artifacts/native-kernel-taylor-full.json").read_bytes())
    require(native.get("all_cells_passed") is True and
            native.get("requested_range_passed") is True and
            native["completed_closed_cells"] == native["requested_cells"] == native["table_cells"] == binding["cells"] and
            native["unresolved_cell"] is None and native["budget_expired"] is False and
            native["tables_sha256"] == binding["tables"] and
            native["packet_sha256"] == binding["packet_sha256"] and
            native["source_sha256"] == digest((HERE/"native_kernel_taylor_audit.py").read_bytes()) and
            native["declaration_sha256"] == digest((HERE/"native-kernel-taylor-declaration.md").read_bytes()),
            "native full-table audit missing or unbound")
    metadata = json.loads((baseline/"tables/tables.json").read_bytes())
    require(metadata["cells"] == 60853 and
            metadata["binding"] == binding["baseline_source"], "baseline cache binding")
    for name in ["w.bin", "w-second.bin"]:
        require(digest((directory/"tables"/name).read_bytes()[:8*metadata["cells"]]) ==
                metadata["hashes"][name], "baseline prefix transport")
    payload = {}

    def add(path, name):
        require(name not in payload, "duplicate archive member")
        payload[name] = Path(path).read_bytes()

    sources = {"code/"+name.replace("\\", "/") for name in binding["baseline_source"]["code"]}
    sources.update(name.replace("\\", "/") for name in binding["code"])
    frozen = json.loads((PROBLEM/"code/rh019_vendor/source-binding.json").read_bytes())
    sources.update("code/rh019_vendor/"+name for name in frozen["files"])
    sources.update([
        "code/rh019_vendor/__init__.py", "code/window_input_audit.py",
        "experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json",
        "experiments/EXP-019-nine-point-local-replay/run.py",
        "experiments/EXP-019-nine-point-local-replay/artifacts/window-audit.json",
        "experiments/EXP-019-nine-point-local-replay/mathematical-audit.md",
        "experiments/EXP-019-nine-point-local-replay/analytic-transfer-review.md",
        "experiments/EXP-019-nine-point-local-replay/audit.py",
        "experiments/EXP-020-quadratic-local-certificate/transfer_audit.py",
        "experiments/EXP-020-quadratic-local-certificate/manuscript-gate-review.md",
        "experiments/EXP-020-quadratic-local-certificate/actual_cover_controls.py",
        "experiments/EXP-020-quadratic-local-certificate/reproducibility_archive.py",
        "experiments/EXP-020-quadratic-local-certificate/native_kernel_taylor_audit.py",
        "experiments/EXP-020-quadratic-local-certificate/native-kernel-taylor-declaration.md",
        "experiments/EXP-020-quadratic-local-certificate/completed-cover-audit-declaration.md",
        "experiments/EXP-023-repressured-local-certificate/native-kernel-taylor-declaration.md",
        "experiments/EXP-023-repressured-local-certificate/native-taylor-audit-declaration.md",
        "experiments/EXP-020-quadratic-local-certificate/artifacts/native-kernel-taylor-pilot.json",
        "experiments/EXP-020-quadratic-local-certificate/artifacts/native-kernel-taylor-full.json",
    ])
    for name in sorted(sources):
        path = PROBLEM/name
        add(path, "repository/"+path.relative_to(REPO).as_posix())
    for subdirectory in ["tables", "reports", "checkpoints"]:
        for path in sorted((directory/subdirectory).iterdir()):
            require(path.is_file() and path.suffix in {".json", ".bin"}, "unexpected output member")
            add(path, "output/exp020/"+path.relative_to(directory).as_posix())
    for name in ["run-binding.json", "pressure-audit.json", "actual-cover-corruption-controls.json"]:
        add(directory/name, "output/exp020/"+name)
    for name in ["w.bin", "w-second.bin"]:
        raw = (baseline/"tables"/name).read_bytes()
        require(digest(raw) == metadata["hashes"][name] and len(raw) == 8*metadata["cells"], "baseline table bytes")
        payload["baseline-cache/tables/"+name] = raw
    add(baseline/"tables/tables.json", "baseline-cache/tables/tables.json")
    payload["exact-transfer.json"] = (json.dumps(result, indent=2)+"\n").encode()
    instructions = """# EXP-020 exact-byte reproducibility archive

This archive contains the actual completed output and physical runtime source
bytes, rather than a Git checkout whose line endings may change source hashes.
No credentials or unrelated repository files are included.

After extraction, run with Python 3 (standard library only):

python repository/problems/number-theory/riemann-hypothesis/experiments/EXP-019-nine-point-local-replay/audit.py --experiment EXP-020 --output-dir output/exp020 --receipt independent-cover.json
python repository/problems/number-theory/riemann-hypothesis/experiments/EXP-020-quadratic-local-certificate/transfer_audit.py --output-dir output/exp020 --receipt independent-transfer.json

These validate input/source binding, domain coverage, tree accounting, and exact
transfer arithmetic. They do not independently rerun every interval operation.
The execution trust base is Python, python-flint 0.9.0, FLINT/Arb, IEEE-754
directed enclosures, and the archived verifier and cache-generation source.
Formal proof checking and external peer review are not claimed.

The bound input tables additionally passed all 61,029 closed-cell comparisons
through native hypergeometric midpoint jets and global Fourier Taylor bounds.
Its successful source-bound receipt and analytic declarations
are included. This input audit shares FLINT/Arb, and is not a separate
arithmetic library or a rerun of the eight-dimensional interval cover.
It can be repeated with native_kernel_taylor_audit.py --output-dir
output/exp020 --cells 61029 --seconds 600 --receipt native-repeat.json.
Use the stated python-flint runtime; preserve the existing receipt files.

Full interval replay requires the stated python-flint runtime and a fresh output
directory. The source binding includes Windows path separators; full-worker
replay is Windows-tested. Cross-platform execution of the full workers is not
claimed. Keep source bytes unchanged and use the archived baseline-cache with
run.py --baseline-dir baseline-cache --output-dir fresh-output
--workers 24. Auditors normalize binding paths without altering their hashes.

The mathematical consequence counts distinct points in the whole critical strip
relative to zeros counted with multiplicity. It is not a proof of RH, a simple
critical-line proportion, or an effective-height bound. Analytic dependencies
and their smoothing/limit order are stated in the archived proof reviews.
"""
    payload["README.md"] = instructions.encode()
    manifest = {"schema": "exp020-runtime-archive-manifest-v1", "members": {
        name: {"bytes": len(raw), "sha256": digest(raw)} for name, raw in sorted(payload.items())}}
    payload["manifest.json"] = (json.dumps(manifest, indent=2)+"\n").encode()
    require(not archive.exists(), "archive already exists; preserve previous evidence")
    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary_archive = archive.with_suffix(archive.suffix+".tmp")
    require(not temporary_archive.exists(), "unreviewed archive temporary exists")
    with zipfile.ZipFile(temporary_archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
        for name, raw in sorted(payload.items()):
            zipped.writestr(name, raw)
    scratch_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="exp020-archive-replay-", dir=scratch_root) as temporary:
        extracted = Path(temporary)
        with zipfile.ZipFile(temporary_archive) as zipped:
            require(zipped.testzip() is None, "archive CRC failure")
            require(set(zipped.namelist()) == set(payload), "archive member mismatch")
            for name, raw in payload.items():
                require(zipped.read(name) == raw, "archive bytes changed")
            zipped.extractall(extracted)
        experiment = extracted/"repository"/HERE.relative_to(REPO)
        checks = [(experiment.parent/"EXP-019-nine-point-local-replay/audit.py", ["--experiment", "EXP-020"]),
                  (experiment/"transfer_audit.py", [])]
        for script, extra in checks:
            completed = subprocess.run([sys.executable, str(script), *extra,
                "--output-dir", str(extracted/"output/exp020"),
                "--receipt", str(extracted/(script.name+".json"))], capture_output=True, text=True, check=False)
            require(completed.returncode == 0, f"extracted {script} failed: {completed.stderr}")
        replayed = json.loads((extracted/"transfer_audit.py.json").read_bytes())
        require(replayed == result, "extracted exact-transfer result differs")
    temporary_archive.replace(archive)
    return {"schema": "exp020-runtime-archive-receipt-v1", "passed": True,
            "archive_filename": archive.name, "archive_bytes": archive.stat().st_size,
            "archive_sha256": digest(archive.read_bytes()), "members": len(payload),
            "manifest_sha256": digest(payload["manifest.json"]),
            "builder_sha256": digest(Path(__file__).read_bytes()),
            "liminf_fraction": result["liminf_fraction"],
            "extracted_stdlib_cover_audit": True, "extracted_exact_transfer_audit": True,
            "native_full_table_audit_included_and_bound": True,
            "native_input_audit_rerun_from_archive": False,
            "full_interval_rerun_from_archive": False,
            "scope": "exact-byte transport, CRC/hash checks, and extracted metadata/transfer audits; interval-execution trust base unchanged"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--baseline-dir", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    receipt = package(args.output_dir.resolve(), args.baseline_dir.resolve(),
                      args.archive.resolve(), args.scratch_root.resolve())
    args.receipt.write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2))
