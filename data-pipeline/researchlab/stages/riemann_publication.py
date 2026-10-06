"""Manuscripts contain one PDF; artifact evidence is a separate publication."""
import copy
import hashlib
import json


def admit(history: dict, current_raw: bytes, companion_raw: bytes, pdf_raw: bytes) -> tuple[dict, dict]:
    def require(condition, message):
        if not condition:
            raise ValueError(f"Publication separation rejected: {message}")

    current, companion = json.loads(current_raw), json.loads(companion_raw)
    require(current.get("schema") == "caos-manuscript-publication-v2"
            and companion.get("schema") == "separate-zenodo-evidence-publication-v1", "record schemas")
    require(current.get("passed") is True and current.get("status") == "published"
            and current.get("manuscript_only") is True and current.get("scientific_content_changed") is False
            and current.get("external_peer_review") is False, "manuscript status and scope")
    require(companion.get("passed") is True and companion.get("status") == "published"
            and companion.get("resource_type") == "dataset" and companion.get("manuscript_pdf_included") is False,
            "separate artifact status")
    require(current["record_id"] == str(history.get("record_id", history.get("id")))
            == companion["manuscript_record"] and current["version_doi"] == history["version_doi"]
            and current["concept_doi"] == history["concept_doi"], "preserved manuscript identifiers")
    require(current["version"] == current["metadata"]["version"] == companion["version"]
            == companion["metadata"]["version"]
            and ("version" not in history or current["version"] == history["version"]), "preserved version")
    require(current["evidence_companion_doi"] == companion["doi"]
            and current["evidence_companion_record_id"] == companion["record_id"]
            and companion["record_id"] != current["record_id"], "independent linked records")
    require(current["metadata"]["resource_type"]["id"] == "publication-preprint"
            and companion["metadata"]["resource_type"]["id"] == "dataset", "publication resource types")
    require(any(x["identifier"] == companion["doi"] and x["relation_type"]["id"] == "issupplementedby"
                for x in current["metadata"]["related_identifiers"])
            and any(x["identifier"] == current["version_doi"] and x["relation_type"]["id"] == "issupplementto"
                    for x in companion["metadata"]["related_identifiers"]), "reciprocal supplement relations")

    def name(f):
        return f.get("name", f.get("filename", ""))

    historical_files = history["files"]
    old_pdf = next(f for f in historical_files if name(f).endswith(".pdf"))
    old_archives = {name(f): f for f in historical_files if name(f).endswith(".zip")}
    require(len(current.get("files", [])) == 1 and name(current["files"][0]).endswith(".pdf"), "PDF-only manuscript file set")
    pdf = current["files"][0]
    require(current["record_url"] == "https://zenodo.org/records/" + current["record_id"]
            and pdf["url"] == "https://zenodo.org/api/records/" + current["record_id"]
            + "/files/" + name(pdf) + "/content", "manuscript download location")
    require(pdf.get("live_bytes_verified") is True and name(pdf) == name(old_pdf)
            and pdf["sha256"] == current["pdf_sha256"] == old_pdf["sha256"] == hashlib.sha256(pdf_raw).hexdigest()
            and pdf["bytes"] == old_pdf["bytes"] == len(pdf_raw)
            and pdf["md5"] == old_pdf["md5"] == hashlib.md5(pdf_raw).hexdigest()
            and pdf_raw.startswith(b"%PDF-"), "original PDF bytes")
    files = companion.get("files", [])
    require(len(files) == len(old_archives) and {name(f) for f in files} == set(old_archives), "complete companion file set")
    for f in files:
        old = old_archives[name(f)]
        require(name(f).endswith(".zip") and f.get("live_bytes_verified") is True
                and all(f[k] == old[k] for k in ("sha256", "md5", "bytes")), "preserved companion archives")
        require(f["url"] == "https://zenodo.org/api/records/" + companion["record_id"]
                + "/files/" + name(f) + "/content",
                "companion download location")
    require(companion["metadata"]["creators"] == current["metadata"]["creators"], "preserved human authorship")
    return copy.deepcopy(current), copy.deepcopy(companion)
