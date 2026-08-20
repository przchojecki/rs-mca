#!/usr/bin/env python3
"""Manifest verifier for the rank-11 repair / rank-12 route packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-repair-rank12-route-v1/manifest.json"
RESULT = "experimental/data/certificates/kb-mca-rank11-repair-rank12-route-v1/result.json"
PARENT = "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
SUPERSEDED = "d01c546f4dca70e256c18c142873821b3bb48ab5"
NEAR_IMPORT = {
    "repository": "przchojecki/rs-mca",
    "pull_request": 1160,
    "commit": "c5f4ea7a0c78828c901ae5f3428894a8b2e2806b",
    "note": {
        "path": "experimental/notes/thresholds/kb_mca_supportwise_near_rational_two_anchor_repair_v1.md",
        "blob": "12bc4a0f06189829a9490928e4855d1aa958f940",
        "sha256": "7e75d67420f4ed37add3b4f6ea3aa45e043a782a6396f328b1e34ce659938989",
    },
    "verifier": {
        "path": "experimental/scripts/verify_kb_mca_supportwise_near_rational_two_anchor_repair_v1.py",
        "blob": "3b4533b53e947466de55262e3577108f125738c0",
        "sha256": "5d284cb0f857f2ff7c0797e911a2047009d6883d54f9d0df0a682627c09b5a35",
    },
    "manifest": {
        "path": "experimental/data/certificates/kb-mca-supportwise-near-rational-two-anchor-repair-v1/manifest.json",
        "blob": "d7442684309e51487a139979332a41c754650609",
        "sha256": "1854bc865a88d148f1a04676dcd566daf8fa7d50d1f16a5c105d9bbee69bae3c",
    },
}

PACKET_FILES = [
    "agents.md",
    "experimental/agents-log.md",
    "experimental/grande_finale.tex",
    "experimental/notes/thresholds/kb_mca_rank11_repair_rank12_route_v1.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/00_contract.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/01_frontier_map.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/02_controls.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/03_idea_ledger.csv",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/04_dependency_ledger.csv",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/05_claim_registry.csv",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/06_review_registry.csv",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/07_review_status.csv",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/PR_DESCRIPTION.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/campaign.json",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/controls/gf11_truncated_margin_counterexample.sage",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/proofs/uniform_rank_one_repair_and_rank12_route.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/reviews/certificate_review.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/reviews/final_certificate_review.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/reviews/final_math_review.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/reviews/final_publication_review.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/reviews/literature_sweep.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/reviews/mathematics_audit.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/reviews/wolfram_replay.md",
    "experimental/campaigns/kb-mca-rank11-repair-rank12-route-post-1173/source_integration_fragment.tex",
    "experimental/data/certificates/kb-mca-rank11-repair-rank12-route-v1/README.md",
    RESULT,
    "experimental/scripts/audit_kb_mca_rank11_repair_rank12_route_v1.py",
    "experimental/scripts/verify_kb_mca_rank11_repair_rank12_route_manifest_v1.py",
    "experimental/scripts/verify_kb_mca_rank11_repair_rank12_route_v1.py",
]

SOURCE_LABELS = [
    "thm:mca-raw-low-heavy-core-shortening",
    "thm:mca-uniform-rank-one-weighted-line",
    "cor:mca-rank-eleven-repaired",
    "thm:mca-dense-core-pair-type",
    "prop:mca-rank-twelve-single-threshold-wall",
    "rem:mca-rank-eleven-repair-scope",
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_manifest() -> dict[str, object]:
    result_path = ROOT / RESULT
    result_bytes = result_path.read_bytes()
    result = json.loads(result_bytes)
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    files = []
    for path in sorted(PACKET_FILES):
        data = (ROOT / path).read_bytes()
        files.append({"path": path, "bytes": len(data), "sha256": sha256(data)})
    active_source = (ROOT / "experimental/grande_finale.tex").read_bytes()
    active_source_text = active_source.decode()
    for label in SOURCE_LABELS:
        marker = f"\\label{{{label}}}"
        if active_source_text.count(marker) != 1:
            raise ValueError(f"source label must occur exactly once: {label}")
    return {
        "schema": "kb-mca-rank11-repair-rank12-route-manifest-v1",
        "parent": PARENT,
        "supersedes_unsubmitted_candidate": SUPERSEDED,
        "imported_near_rational_dependency": NEAR_IMPORT,
        "result": RESULT,
        "result_sha256": sha256(result_bytes),
        "canonical_payload_sha256": sha256(canonical),
        "active_source": "experimental/grande_finale.tex",
        "active_source_sha256": sha256(active_source),
        "source_labels": SOURCE_LABELS,
        "claims": result["claims"],
        "files": files,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    expected = build_manifest()
    if args.write:
        MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {MANIFEST}")
        return

    manifest = json.loads(MANIFEST.read_text())
    assert manifest == expected
    assert manifest["schema"] == "kb-mca-rank11-repair-rank12-route-manifest-v1"
    assert manifest["parent"] == PARENT
    assert manifest["supersedes_unsubmitted_candidate"] == SUPERSEDED
    assert manifest["imported_near_rational_dependency"] == NEAR_IMPORT

    result_path = ROOT / manifest["result"]
    result_bytes = result_path.read_bytes()
    assert sha256(result_bytes) == manifest["result_sha256"]
    result = json.loads(result_bytes)
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    assert sha256(canonical) == manifest["canonical_payload_sha256"]
    assert manifest["claims"] == result["claims"]

    seen: set[str] = set()
    for item in manifest["files"]:
        path = item["path"]
        assert path not in seen
        seen.add(path)
        data = (ROOT / path).read_bytes()
        assert len(data) == item["bytes"]
        assert sha256(data) == item["sha256"]

    print(
        "KB_MCA_RANK11_REPAIR_RANK12_ROUTE_MANIFEST_PASS "
        f"files={len(seen)} payload={manifest['canonical_payload_sha256']}"
    )


if __name__ == "__main__":
    main()
