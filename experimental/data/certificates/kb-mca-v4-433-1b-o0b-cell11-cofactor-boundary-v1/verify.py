#!/usr/bin/env python3
"""Verify the O0b cell-11 selected-cofactor chart certificate."""

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERT = HERE / "kb_mca_v4_433_1b_o0b_cell11_cofactor_boundary_v1.json"
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
        if path.endswith("selected_cofactor_boundary_result.json"):
            result = json.loads(raw)
    require(result is not None, "result payload")
    require(result["case_count"] == len(result["rows"]) == 8,
            "tower census")
    require(result["status_counts"]
            == {"NO_DEPLOYED_FIELD_BOUNDARY_POINT": 8}, "status census")
    require(result["deployed_boundary_root_occurrences"] == 0,
            "deployed root census")
    require(result["field_boundary_point_count"] == 0,
            "field point census")
    expected_keys = set(itertools.product((-1, 1), repeat=3))
    seen = set()
    for row in result["rows"]:
        key = (row["epsilon"][0], row["epsilon"][1], row["bc_sign"])
        require(key in expected_keys and key not in seen, "tower key")
        seen.add(key)
        if row["bc_sign"] == -1:
            factors = [(2, 2), (1, 10)]
            root = (1, 10, [3, 4, 5, 6, 7, 8])
        else:
            factors = [(3, 2), (2, 4), (1, 4)]
            root = (PRIME - 1, 4, [2, 3, 4, 5])
        require([(item["degree"], item["multiplicity"])
                 for item in row["norm_numerator_factorization"]] == factors,
                "factor profile")
        require(len(row["base_field_roots"]) == 1, "root count")
        actual = row["base_field_roots"][0]
        require((actual["x"], actual["multiplicity"],
                 actual["zero_guard_indices"]) == root, "root profile")
        require(not actual["pre_cofactor_guards_nonzero"],
                "guard classification")
        require(row["off_chart_roots"] == row["base_field_roots"],
                "off-chart roots")
        require(row["deployed_boundary_roots"] == [], "deployed roots")
        require(row["boundary_points"] == [], "boundary points")
    require(seen == expected_keys, "Cartesian coverage")
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    cert = json.loads(CERT.read_text())
    require(cert["schema"]
            == "kb-mca-v4-433-1b-o0b-cell11-cofactor-boundary-v1",
            "schema")
    require(not cert["K3_closed"] and not cert["KoalaBear_row_closed"],
            "scope flags")
    require(cert["statement"]["ledger_movement"] == 0, "ledger movement")
    require(cert["provenance"]["node_count"] == 1, "node count")
    require(len(cert["evidence_files"])
            == cert["provenance"]["evidence_file_count"] == 5,
            "evidence count")
    checked = 0
    if args.source_root is not None:
        checked = validate_source(cert, args.source_root)
    print(
        "O0B_CELL11_COFACTOR_BOUNDARY_CERT_PASS "
        f"blobs={checked} towers=8 base_roots=8 deployed_roots=0"
    )


if __name__ == "__main__":
    main()
