#!/usr/bin/env python3
"""Fail-closed manifest for the rank-twelve scalar/gluing route packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = "1b613fc669158a690a52b64f0eeb440f10672f1e"
RESULT = "experimental/data/certificates/kb-mca-rank12-scalar-gluing-route-v1/result.json"
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank12-scalar-gluing-route-v1/manifest.json"

PACKET_FILES = [
    "agents.md",
    "experimental/agents-log.md",
    "experimental/grande_finale.tex",
    "experimental/notes/thresholds/kb_mca_rank12_scalar_gluing_route_v1.md",
    "experimental/data/certificates/kb-mca-rank12-scalar-gluing-route-v1/README.md",
    RESULT,
    "experimental/scripts/verify_kb_mca_rank12_scalar_resource_barrier_v1.py",
    "experimental/scripts/verify_kb_mca_rank12_scalar_gluing_route_manifest_v1.py",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/00_contract.md",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/01_frontier_map.md",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/02_controls.md",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/03_idea_ledger.csv",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/04_dependency_ledger.csv",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/05_claim_registry.csv",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/06_review_registry.csv",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/07_review_status.csv",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/campaign.json",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/PR_DESCRIPTION.md",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/controls/syz25_coplanar_core_generation.sage",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/controls/gluing_rank_zero_post_near_counterexample.sage",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/proofs/scalar_resource_first_moment_barrier.md",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/proofs/actual_line_core_generation_route.md",
    "experimental/campaigns/kb-mca-rank12-multilevel-post-1174/reviews/literature_sweep.md",
]

SOURCE_LABELS = [
    "prop:mca-rank-twelve-scalar-resource-barrier",
    "rem:mca-rank-twelve-scalar-pair-barrier",
    "thm:mca-actual-line-core-gluing-defect",
    "rem:mca-rank-twelve-gluing-target",
]

DEPENDENCIES = {
    "parent_pr_1174": BASE,
    "near_repair_pr_1160": "c5f4ea7a0c78828c901ae5f3428894a8b2e2806b",
    "public_syz21_syz25": {
        "repository": "SlopDotCash/proximityprize",
        "commit": "acfa4f072d0c7fe8e706c80d8e21cb5b083f73a6",
    },
    "public_circuit_atlas": {
        "repository": "AllenGrahamHart/rs-mca-prize-dag",
        "commits": [
            "5330928af9d262b24b7fe986ed837b09b9c05816",
            "8eb59e7cb1fe4254ad44a3cb30e9c8b98f03053b",
        ],
    },
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Reject: {message}")


def build_manifest() -> dict[str, object]:
    result_bytes = (ROOT / RESULT).read_bytes()
    result = json.loads(result_bytes)
    canonical_result = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    files = []
    for relative in sorted(PACKET_FILES):
        data = (ROOT / relative).read_bytes()
        files.append(
            {"path": relative, "bytes": len(data), "sha256": sha256(data)}
        )

    source = (ROOT / "experimental/grande_finale.tex").read_bytes()
    source_text = source.decode()
    for label in SOURCE_LABELS:
        marker = f"\\label{{{label}}}"
        if source_text.count(marker) != 1:
            raise ValueError(f"source label must occur exactly once: {label}")

    return {
        "schema": "kb-mca-rank12-scalar-gluing-route-manifest-v1",
        "base": BASE,
        "dependencies": DEPENDENCIES,
        "result": RESULT,
        "result_sha256": sha256(result_bytes),
        "canonical_result_sha256": sha256(canonical_result),
        "active_source": "experimental/grande_finale.tex",
        "active_source_sha256": sha256(source),
        "source_labels": SOURCE_LABELS,
        "claims": {
            key: result[key]
            for key in (
                "scalar_resource_barrier_proved",
                "gluing_rank_zero_paid",
                "gluing_rank_one_paid",
                "gluing_rank_two_paid",
                "affine_error_rank12_paid",
                "active_v4_ledger_movement",
                "koalabear_closed",
            )
        },
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

    actual = json.loads(MANIFEST.read_text())
    require(actual == expected, "canonical manifest mismatch")
    seen: set[str] = set()
    for item in actual["files"]:
        relative = item["path"]
        require(relative not in seen, f"duplicate packet path: {relative}")
        seen.add(relative)
        data = (ROOT / relative).read_bytes()
        require(len(data) == item["bytes"], f"byte length mismatch: {relative}")
        require(sha256(data) == item["sha256"], f"hash mismatch: {relative}")
    print(
        "KB_MCA_RANK12_SCALAR_GLUING_ROUTE_MANIFEST_PASS "
        f"files={len(seen)} payload={actual['canonical_result_sha256']}"
    )


if __name__ == "__main__":
    main()
