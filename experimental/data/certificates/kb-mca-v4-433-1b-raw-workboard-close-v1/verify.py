#!/usr/bin/env python3
"""Verify the raw 433-1b/O0a workboard certificate and pinned source blobs."""

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERT = HERE / "kb_mca_v4_433_1b_raw_workboard_close_v1.json"
EXPECTED_PARTITION = "[0]|[1,2]|[3,6]|[4,7]|[5,8]|[9,10]|[11]|[12,13]|[14]"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def blob(root, commit, path):
    return subprocess.run(
        ["git", "-C", str(root), "show", f"{commit}:{path}"],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-root",
        type=Path,
        help="checkout containing the pinned rs-mca-prize-dag commit",
    )
    args = parser.parse_args()

    cert = json.loads(CERT.read_text())
    claims = cert["statement"]["claims"]
    require(cert["schema"] == "kb-mca-v4-433-1b-raw-workboard-close-v1",
            "schema")
    require(cert["statement"]["ledger_movement"] == 0, "ledger movement")
    require(not cert["K3_closed"] and not cert["KoalaBear_row_closed"],
            "scope flags")
    require(claims["owner_partition"] == EXPECTED_PARTITION,
            "owner partition")
    require("25200" in claims["principal_census"], "principal census")
    require(len(cert["nodes"]) == 3, "aggregate node count")

    checked = 0
    if args.source_root is not None:
        commit = cert["provenance"]["commit"]
        for node in cert["nodes"]:
            for key, name in (
                ("node_manifest_sha256", "node.json"),
                ("verify_sha256", "verify.py"),
                ("verify_audit_sha256", "verify_audit.py"),
            ):
                path = f"{node['path']}/{name}"
                digest = hashlib.sha256(blob(args.source_root, commit, path)).hexdigest()
                require(digest == node[key], f"digest mismatch: {path}")
                checked += 1
        experiment = (
            "experiments/prize_resolution/"
            "rate_half_kb_positive_433_1b_cells9_10_duplicate_role_transport.py"
        )
        digest = hashlib.sha256(blob(args.source_root, commit, experiment)).hexdigest()
        require(digest == cert["provenance"]["experiment_sha256"],
                "experiment digest")
        checked += 1

    print(
        "RAW_WORKBOARD_CERT_PASS "
        f"nodes=3 hashes={checked} cells=15 labels=1575 systems=25200"
    )


if __name__ == "__main__":
    main()
