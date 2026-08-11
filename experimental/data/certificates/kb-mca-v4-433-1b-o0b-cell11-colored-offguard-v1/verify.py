#!/usr/bin/env python3
"""Verify the O0b cell-11 colored off-guard certificate."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERT = HERE / "kb_mca_v4_433_1b_o0b_cell11_colored_offguard_v1.json"
PRIME = 2130706433


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def blob(root, commit, path):
    return subprocess.run(
        ["git", "-C", str(root), "show", f"{commit}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def digest(value):
    return hashlib.sha256(value).hexdigest()


def validate_source(cert, source_root):
    commit = cert["provenance"]["commit"]
    node = cert["node"]
    checked = 0
    for key, name in (
        ("node_manifest_sha256", "node.json"),
        ("verify_sha256", "verify.py"),
        ("verify_audit_sha256", "verify_audit.py"),
    ):
        path = f"{node['path']}/{name}"
        require(digest(blob(source_root, commit, path)) == node[key],
                f"digest mismatch: {path}")
        checked += 1
    manifest = json.loads(blob(
        source_root, commit, f"{node['path']}/node.json"
    ))
    require(manifest["node"]["id"] == node["id"], "node id")
    require(manifest["node"]["status"] == "PROVED", "node status")

    result = None
    for path, expected in cert["evidence_files"].items():
        raw = blob(source_root, commit, path)
        require(digest(raw) == expected, f"digest mismatch: {path}")
        checked += 1
        if path.endswith("colored_consistency_result.json"):
            result = json.loads(raw)
    require(result is not None, "result payload")
    require(result["source_tower_count"] == 8, "tower census")
    require(result["case_count"] == 16, "case census")
    require(result["status_counts"] == {"DEPLOYED_OFF_GUARD_UNIT": 16},
            "status census")
    require(result["non_guard_root_occurrences"] == 0, "non-guard roots")
    for source in result["rows"]:
        require(source["tower_valid"], "tower validity")
        require({row["missing_record"] for row in source["rows"]}
                == {"BE", "CF"}, "record cover")
        expected = (
            [(0, 5), (1, 12)] if source["bc_sign"] == -1
            else [(0, 4), (PRIME - 1, 8)]
        )
        for row in source["rows"]:
            roots = [
                (root["x"], root["multiplicity"])
                for root in row["base_field_roots"]
            ]
            require(roots == expected, "root profile")
            require(all(not root["construction_guards_nonzero"]
                        for root in row["base_field_roots"]),
                    "guard classification")
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    cert = json.loads(CERT.read_text())
    require(cert["schema"]
            == "kb-mca-v4-433-1b-o0b-cell11-colored-offguard-v1", "schema")
    require(not cert["K3_closed"] and not cert["KoalaBear_row_closed"],
            "scope flags")
    require(cert["statement"]["ledger_movement"] == 0, "ledger movement")
    require(cert["provenance"]["node_count"] == 1, "node count")
    require(len(cert["evidence_files"])
            == cert["provenance"]["evidence_file_count"] == 4,
            "evidence count")
    checked = 0
    if args.source_root is not None:
        checked = validate_source(cert, args.source_root)
    print(
        "O0B_CELL11_COLORED_OFFGUARD_CERT_PASS "
        f"blobs={checked} towers=8 cases=16 non_guard_roots=0"
    )


if __name__ == "__main__":
    main()

