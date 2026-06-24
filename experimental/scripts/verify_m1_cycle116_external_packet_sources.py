#!/usr/bin/env python3
"""Verify the PR #96 source objects behind the Cycle116 external contract.

The compact contract in
experimental/data/witnesses/m1-cycle116/external_packet_contract.json records
hashes for four files from the closed PR #96 packet.  This verifier checks those
hashes against the actual Git objects at the recorded PR #96 head commit, and
checks that the two JSON inputs are copied exactly into the compact contract.

The verifier is nonmutating but it requires the recorded commit to be present in
the local Git object database.  Fetch it with:

    git fetch origin pull/96/head:refs/remotes/origin/pr-96
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_external_packet_contract as packet_contract


SOURCE_COMMIT = packet_contract.EXPECTED_HEAD_COMMIT
FETCH_COMMAND = "git fetch origin pull/96/head:refs/remotes/origin/pr-96"

EXPECTED_GIT_OBJECTS = {
    "fixed_jet_certificate": {
        "mode": "100644",
        "blob": "02a72d9c35f496985fa76778506ab2aac174036f",
        "size": 1727,
    },
    "cycle84_anchor": {
        "mode": "100644",
        "blob": "02a74f5c2b796bd9a750791558f22060d6fa50e2",
        "size": 981,
    },
    "standalone_certificate_section": {
        "mode": "100644",
        "blob": "eb8619635547bd4dfdad8a64244fb2816a266807",
        "size": 4446,
    },
    "transfer_verifier": {
        "mode": "100755",
        "blob": "dc01f7c1ea03849a8d32ac2aa6bad09bfc392ce3",
        "size": 37461,
    },
}

STANDALONE_REQUIRED_FRAGMENTS = {
    "native_ldsw": "LD_sw(RS[F0,D0,137],143) >= 52,747,567,092",
    "smooth_ldsw": "LD_sw(C,262) >= 52,747,567,092",
    "field_ledger": "q_gen=q_code=q_line=17^32.",
    "smooth_domain": "H=<theta>=D0 disjoint_union theta D0.",
    "native_scalar": "P_T(beta)=(beta-1)3^28 Phi(T)=kappa Phi(T)",
}

TRANSFER_REQUIRED_FRAGMENTS = {
    "success_code": "CYCLE116_TRANSFER_CERTIFICATE_VERIFIED",
    "fixed_jet_missing_code": "MISSING_FIXED_JET_CERTIFICATE",
    "cycle84_anchor_missing_code": "MISSING_CYCLE84_ANCHOR",
    "smooth_domain_check": "SMOOTH_DOMAIN_DECOMPOSITION",
    "q_gen_subfield_check": "Q_GEN_SUBFIELD_TEST",
    "ldsw_output_field": "LD_sw_lower_bound",
    "density_output_field": "floor_q_line_over_2^128",
}


def run_git(args: list[str]) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=packet_contract.ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise AssertionError(
            f"git {' '.join(args)} failed: {stderr}. "
            f"Fetch the source commit with `{FETCH_COMMAND}`."
        )
    return result.stdout


def check_commit_present() -> None:
    run_git(["cat-file", "-e", f"{SOURCE_COMMIT}^{{commit}}"])


def git_object_info(path: str) -> Dict[str, Any]:
    raw = run_git(["ls-tree", "-l", SOURCE_COMMIT, "--", path])
    text = raw.decode("utf-8").strip()
    if not text:
        raise AssertionError(f"missing source path at {SOURCE_COMMIT}: {path}")
    fields = text.split(None, 4)
    if len(fields) != 5 or fields[1] != "blob":
        raise AssertionError(f"unexpected git ls-tree output: {text}")
    return {
        "mode": fields[0],
        "type": fields[1],
        "blob": fields[2],
        "size": int(fields[3]),
        "path": fields[4],
    }


def git_file_bytes(path: str) -> bytes:
    return run_git(["show", f"{SOURCE_COMMIT}:{path}"])


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_json_bytes(payload: bytes) -> Any:
    return json.loads(payload.decode("utf-8"))


def build_report() -> Dict[str, Any]:
    check_commit_present()
    contract = packet_contract.load_contract()
    source_files = contract["provenance"]["source_files"]

    source_reports = {}
    file_payloads = {}
    checks = {
        "contract_comparison_still_passes": packet_contract.build_report()["status"]
        == "PASS",
        "source_commit_matches_contract": (
            contract["provenance"]["head_commit"] == SOURCE_COMMIT
        ),
    }

    for name, recorded in source_files.items():
        if name not in EXPECTED_GIT_OBJECTS:
            raise AssertionError(f"unexpected source file in contract: {name}")
        path = recorded["path"]
        info = git_object_info(path)
        payload = git_file_bytes(path)
        digest = sha256_bytes(payload)
        expected = EXPECTED_GIT_OBJECTS[name]

        source_reports[name] = {
            "path": path,
            "mode": info["mode"],
            "blob": info["blob"],
            "size": info["size"],
            "sha256": digest,
        }
        file_payloads[name] = payload

        checks[f"{name}_git_object_matches_expected"] = (
            info["mode"] == expected["mode"]
            and info["blob"] == expected["blob"]
            and info["size"] == expected["size"]
        )
        checks[f"{name}_sha256_matches_contract"] = (
            digest == recorded["sha256"]
        )
        checks[f"{name}_payload_size_matches_git"] = len(payload) == info["size"]

    checks["source_file_set_matches_expected"] = (
        set(source_files) == set(EXPECTED_GIT_OBJECTS)
    )
    checks["fixed_jet_json_copied_exactly"] = (
        parse_json_bytes(file_payloads["fixed_jet_certificate"])
        == contract["fixed_jet_certificate"]
    )
    checks["cycle84_anchor_json_copied_exactly"] = (
        parse_json_bytes(file_payloads["cycle84_anchor"])
        == contract["cycle84_anchor"]
    )

    standalone_text = file_payloads["standalone_certificate_section"].decode("utf-8")
    transfer_text = file_payloads["transfer_verifier"].decode("utf-8")

    standalone_fragments = {
        name: fragment in standalone_text
        for name, fragment in STANDALONE_REQUIRED_FRAGMENTS.items()
    }
    transfer_fragments = {
        name: fragment in transfer_text
        for name, fragment in TRANSFER_REQUIRED_FRAGMENTS.items()
    }
    checks["standalone_certificate_fragments_present"] = all(
        standalone_fragments.values()
    )
    checks["transfer_verifier_fragments_present"] = all(transfer_fragments.values())

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / EXTERNAL-CYCLE116-SOURCE-HASHES-VERIFIED",
        "theorem_problem_id": "M1 Cycle116 external packet source hash audit",
        "source": {
            "repository": contract["provenance"]["repository"],
            "pull_request": int(contract["provenance"]["pull_request"]),
            "head_ref": contract["provenance"]["head_ref"],
            "head_commit": SOURCE_COMMIT,
            "fetch_command": FETCH_COMMAND,
            "files": source_reports,
        },
        "exact_copies": {
            "fixed_jet_certificate": True,
            "cycle84_anchor": True,
        },
        "fragment_audit": {
            "standalone_certificate_section": standalone_fragments,
            "transfer_verifier": transfer_fragments,
        },
        "checks": checks,
        "remaining_imports": [
            "external PR #96 provenance review if the packet is cited directly",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    source = report["source"]
    files = source["files"]

    print("m1_cycle116_external_packet_sources: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "source="
        f"PR #{source['pull_request']} {source['head_ref']} "
        f"commit {source['head_commit']}"
    )
    print(
        "files="
        + ", ".join(
            f"{name}:{payload['sha256'][:12]}:{payload['size']}B"
            for name, payload in sorted(files.items())
        )
    )
    print(
        "exact_json_copies="
        f"fixed_jet_certificate={report['exact_copies']['fixed_jet_certificate']}, "
        f"cycle84_anchor={report['exact_copies']['cycle84_anchor']}"
    )
    print("fetch_command=" + source["fetch_command"])
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify PR #96 source objects for the Cycle116 packet contract."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
