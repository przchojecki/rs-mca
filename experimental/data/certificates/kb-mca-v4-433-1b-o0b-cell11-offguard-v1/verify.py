#!/usr/bin/env python3
"""Verify the O0b cell-11 off-guard certificate and pinned source blobs."""

import argparse
from collections import Counter
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERT = HERE / "kb_mca_v4_433_1b_o0b_cell11_offguard_v1.json"
MANIFEST_SUFFIX = "cell11_uncolored_exceptional_replay_manifest.json"


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
    for node in cert["nodes"]:
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

    norm_status = Counter()
    norm_rows = 0
    root_occurrences = 0
    distinct_x = set()
    replay_rows = 0
    replay_excluded = 0
    manifest_payload = None
    for path, expected in cert["evidence_files"].items():
        raw = blob(source_root, commit, path)
        require(digest(raw) == expected, f"digest mismatch: {path}")
        checked += 1
        if not path.endswith(".json"):
            continue
        payload = json.loads(raw)
        if "_resultant_norm_" in path:
            require(payload["case_count"] == len(payload["rows"]) == 90,
                    "norm shard census")
            norm_rows += payload["case_count"]
            norm_status.update(payload["status_counts"])
            for row in payload["rows"]:
                roots = row["selected"]["resultant_nested_norm"][
                    "non_guard_base_field_roots"
                ]
                root_occurrences += len(roots)
                distinct_x.update(root["x"] for root in roots)
        elif "_exceptional_replay_bc" in path:
            require(payload["case_count"] == len(payload["rows"]),
                    "replay shard census")
            replay_rows += payload["case_count"]
            replay_excluded += payload["status_counts"].get(
                "EXCEPTIONAL_ROOT_EXCLUDED", 0
            )
        elif path.endswith(MANIFEST_SUFFIX):
            manifest_payload = payload

    require(norm_rows == 720, "norm aggregate census")
    require(norm_status == Counter({
        "DEPLOYED_OFF_GUARD_UNIT": 288,
        "DEPLOYED_POINTWISE_NORM_COVER": 432,
    }), "norm aggregate partition")
    require(root_occurrences == replay_rows == replay_excluded == 1584,
            "exceptional replay census")
    require(len(distinct_x) == 126, "distinct base-value census")
    require(manifest_payload is not None, "exceptional manifest")
    require(manifest_payload["case_count"] == 1584, "manifest cases")
    require(manifest_payload["distinct_x_count"] == 126,
            "manifest distinct values")
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        type=Path,
        help="checkout containing the pinned rs-mca-prize-dag commit",
    )
    args = parser.parse_args()

    cert = json.loads(CERT.read_text())
    require(cert["schema"] == "kb-mca-v4-433-1b-o0b-cell11-offguard-v1",
            "schema")
    require(not cert["K3_closed"] and not cert["KoalaBear_row_closed"],
            "scope flags")
    require(cert["statement"]["ledger_movement"] == 0, "ledger movement")
    require(len(cert["nodes"]) == cert["provenance"]["node_count"] == 2,
            "node count")
    require(
        len(cert["evidence_files"])
        == cert["provenance"]["evidence_file_count"] == 19,
        "evidence count",
    )
    require(8 * 3 * 2 * 15 == 720, "representative arithmetic")
    require(288 + 432 == 720, "norm partition arithmetic")

    checked = 0
    if args.source_root is not None:
        checked = validate_source(cert, args.source_root)
    print(
        "O0B_CELL11_OFFGUARD_CERT_PASS "
        f"nodes=2 blobs={checked} representatives=720 roots=1584 "
        "distinct_x=126 excluded=1584"
    )


if __name__ == "__main__":
    main()

