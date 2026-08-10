#!/usr/bin/env python3
"""Verify the O0b cell-11 reconstruction-boundary certificate."""

import argparse
import hashlib
import itertools
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERT = HERE / "kb_mca_v4_433_1b_o0b_cell11_reconstruction_boundary_v1.json"


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
    checked = 0
    for node in [cert["node"], *cert["dependencies"]]:
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
        if path.endswith("reconstruction_denominator_boundary_result.json"):
            result = json.loads(raw)
    require(result is not None, "result payload")
    require(result["case_count"] == len(result["rows"]) == 8,
            "tower census")
    require(result["status_counts"]
            == {"NO_GUARDED_RECONSTRUCTION_BOUNDARY_POINT": 8},
            "status census")
    require(result["chart_boundary_root_occurrences"] == 12,
            "chart root census")
    require(result["field_boundary_point_count"] == 16,
            "field point census")
    require(result["guarded_boundary_point_count"] == 0,
            "guarded point census")
    expected_keys = set(itertools.product((-1, 1), repeat=3))
    seen = set()
    for row in result["rows"]:
        key = (*row["epsilon"], row["bc_sign"])
        require(key in expected_keys and key not in seen, "tower key")
        seen.add(key)
        if row["bc_sign"] == -1:
            require(row["chart_boundary_roots"] == [], "BC- chart roots")
            require(row["boundary_points"] == [], "BC- boundary points")
        else:
            require([item["x"] for item in row["chart_boundary_roots"]]
                    == [153731577, 583634934, 1547071505],
                    "BC+ chart roots")
            require(row["field_boundary_point_count"] == 4,
                    "BC+ point census")
            require(sorted(point["x"] for point in row["boundary_points"])
                    == [583634934, 583634934, 1547071505, 1547071505],
                    "BC+ point roots")
            for point in row["boundary_points"]:
                require(point["b_equals_c"] and point["bc_matches_x"],
                        "boundary coordinates")
                require(point["common_equations_zero"], "common equations")
                require(not point["common_guard_nonzero"]
                        and not point["guarded"], "common guard")
    require(seen == expected_keys, "Cartesian coverage")
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    cert = json.loads(CERT.read_text())
    require(cert["schema"]
            == "kb-mca-v4-433-1b-o0b-cell11-reconstruction-boundary-v1",
            "schema")
    require(not cert["K3_closed"] and not cert["KoalaBear_row_closed"],
            "scope flags")
    require(cert["statement"]["ledger_movement"] == 0, "ledger movement")
    require(len(cert["dependencies"]) == 2, "dependency count")
    require(cert["provenance"]["node_count"] == 3, "node count")
    require(len(cert["evidence_files"])
            == cert["provenance"]["evidence_file_count"] == 5,
            "evidence count")
    checked = 0
    if args.source_root is not None:
        checked = validate_source(cert, args.source_root)
    print(
        "O0B_CELL11_RECONSTRUCTION_BOUNDARY_CERT_PASS "
        f"blobs={checked} towers=8 field_points=16 guarded_points=0"
    )


if __name__ == "__main__":
    main()
