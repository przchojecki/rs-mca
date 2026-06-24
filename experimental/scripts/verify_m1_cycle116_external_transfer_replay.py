#!/usr/bin/env python3
"""Replay the hash-pinned external Cycle116 transfer verifier from PR #96.

This verifier materializes the PR #96 Cycle116 packet in a temporary directory
from Git objects, runs its fail-closed verify_transfer.py, and compares the
resulting theorem ledger to the local Cycle120 finite chain.

It is intentionally separate from the normal end-to-end chain because it runs
source code from the recorded PR #96 Git object.  Fetch the source commit with:

    git fetch origin pull/96/head:refs/remotes/origin/pr-96
"""

from __future__ import annotations

import argparse
import json
import posixpath
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Mapping


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_external_packet_contract as packet_contract
import verify_m1_cycle116_external_packet_sources as source_audit
import verify_m1_cycle120_end_to_end_chain as end_to_end


SOURCE_COMMIT = source_audit.SOURCE_COMMIT
FETCH_COMMAND = source_audit.FETCH_COMMAND


def git_payload(path: str) -> bytes:
    return source_audit.git_file_bytes(path)


def write_payload(path: Path, payload: bytes, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    if executable:
        path.chmod(0o755)


def normalized_import_path(anchor_source_path: str, import_path: str) -> str:
    return posixpath.normpath(
        posixpath.join(posixpath.dirname(anchor_source_path), import_path)
    )


def load_anchor_import_payloads(
    contract: Mapping[str, Any],
) -> tuple[dict[str, bytes], dict[str, str]]:
    anchor_source = contract["provenance"]["source_files"]["cycle84_anchor"]["path"]
    imported = contract["cycle84_anchor"]["imported_files"]
    payloads: dict[str, bytes] = {}
    paths: dict[str, str] = {}

    for name, record in imported.items():
        path = normalized_import_path(anchor_source, record["path"])
        payload = git_payload(path)
        digest = source_audit.sha256_bytes(payload)
        if digest != record["sha256"]:
            raise AssertionError(
                f"import hash mismatch for {name}: expected {record['sha256']} "
                f"got {digest}"
            )
        payloads[name] = payload
        paths[name] = path

    return payloads, paths


def materialize_external_packet(
    temp_root: Path,
    contract: Mapping[str, Any],
    import_payloads: Mapping[str, bytes],
) -> Dict[str, Path]:
    work_dir = temp_root / "cycle116_role08_verifier"
    input_dir = work_dir / "inputs"
    import_dir = work_dir / "imports"

    fixed_path = input_dir / "fixed_jet_certificate.json"
    anchor_path = input_dir / "cycle84_anchor.json"
    verifier_path = work_dir / "verify_transfer.py"

    write_payload(
        fixed_path,
        git_payload(contract["provenance"]["source_files"]["fixed_jet_certificate"]["path"]),
    )
    write_payload(
        anchor_path,
        git_payload(contract["provenance"]["source_files"]["cycle84_anchor"]["path"]),
    )
    write_payload(
        verifier_path,
        git_payload(contract["provenance"]["source_files"]["transfer_verifier"]["path"]),
        executable=True,
    )

    imported = contract["cycle84_anchor"]["imported_files"]
    for name, record in imported.items():
        target = import_dir / Path(record["path"]).name
        write_payload(target, import_payloads[name])

    return {
        "work_dir": work_dir,
        "fixed_path": fixed_path,
        "anchor_path": anchor_path,
        "verifier_path": verifier_path,
    }


def run_external_verifier(paths: Mapping[str, Path]) -> Dict[str, Any]:
    result = subprocess.run(
        [
            sys.executable,
            str(paths["verifier_path"]),
            "--anchor",
            str(paths["anchor_path"]),
            "--fixed-jet",
            str(paths["fixed_path"]),
        ],
        cwd=paths["work_dir"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            "external verify_transfer.py failed with exit "
            f"{result.returncode}: {result.stderr.strip()} {result.stdout.strip()}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"external verifier emitted non-JSON: {exc}") from exc


def build_report() -> Dict[str, Any]:
    source_audit.check_commit_present()
    contract = packet_contract.load_contract()
    import_payloads, import_paths = load_anchor_import_payloads(contract)
    chain_report = end_to_end.build_report()

    with tempfile.TemporaryDirectory(prefix="m1-cycle116-external-") as temp_dir:
        paths = materialize_external_packet(Path(temp_dir), contract, import_payloads)
        external = run_external_verifier(paths)

    chain = chain_report["chain"]
    native_chain = chain["cycle116_native"]
    smooth_chain = chain["cycle116_smooth_lift"]
    field_ledger = chain["cycle120_domain_field_ledger"]
    gate = chain["cycle120_gate_arithmetic"]

    native = external["native_row"]
    smooth = external["smooth_lift"]
    ledger = external["field_parameter_ledger"]
    imports = external["imports"]
    affine = external["one_affine_line_receipt"]

    checks = {
        "local_end_to_end_chain_passes": chain_report["status"] == "PASS",
        "external_decision_verified": (
            external["decision"] == "CYCLE116_TRANSFER_CERTIFICATE_VERIFIED"
        ),
        "external_label_is_proof": external["label"] == "PROOF",
        "native_ldsw_matches_local_chain": (
            int(native["LD_sw_lower_bound"]) == int(native_chain["bad_line_parameters"])
            and int(native["n"]) == int(native_chain["domain_size"]) == 256
            and int(native["k"]) == int(native_chain["dimension"]) == 137
            and int(native["agreement"]) == int(native_chain["agreement"]) == 143
            and native["delta"] == "113/256"
        ),
        "smooth_ldsw_matches_local_chain": (
            int(smooth["LD_sw_lower_bound"]) == int(smooth_chain["bad_line_parameters"])
            and int(smooth["n"]) == int(smooth_chain["domain_size"]) == 512
            and int(smooth["k"]) == int(smooth_chain["dimension"]) == 256
            and int(smooth["agreement"]) == int(smooth_chain["agreement"]) == 262
            and smooth["delta"] == smooth_chain["delta"] == "125/256"
        ),
        "smooth_domain_ledger_matches_local_chain": (
            int(smooth["H_order"]) == 512
            and int(smooth["theta_order"]) == 512
            and bool(smooth["H_generates_K"])
            and int(smooth["A_size"]) == int(smooth_chain["padding"]["A_size"])
            and int(smooth["R_size"]) == int(smooth_chain["padding"]["R_size"])
        ),
        "field_parameter_ledger_matches_local_chain": (
            int(ledger["q_gen"]) == int(field_ledger["q_gen"])
            and int(ledger["q_code"]) == int(field_ledger["q_code"])
            and int(ledger["q_line"]) == int(field_ledger["q_line"])
            and ledger["q_chal"] is None
            and int(ledger["bad_slope_numerator"]) == int(gate["bad_gamma_count"])
            and int(ledger["floor_q_line_over_2^128"])
            == int(gate["minimum_bad_gamma_count_for_gt_2_minus_128"]) - 1
        ),
        "density_gate_matches_local_chain": (
            bool(smooth["strictly_greater_than_2^-128"])
            and ledger["strict_integer_test"]
            == f"2^128*{gate['bad_gamma_count']} > 17^32"
        ),
        "fixed_jet_payload_matches_expected": (
            external["fixed_jet"]["slot_states_checked"] == 336
            and external["fixed_jet"]["family_locator"]
            == "P_T(X)=X^113-X^112+O(X^107)"
            and external["fixed_jet"]["product_scalar"] == "P_T(beta)=kappa*Phi(T)"
        ),
        "affine_line_receipt_has_closed_support": (
            int(affine["support_size"]) == 262
            and affine["construction"] == "f=e_J0-z0*g, g(x)=L_H(beta)/(beta-x)"
            and affine["noncontainment_clause"]
            == "251 distinct Vandermonde columns in dimension 256"
        ),
        "external_import_hashes_match_anchor": (
            imports["sha256"]
            == {
                name: record["sha256"]
                for name, record in contract["cycle84_anchor"]["imported_files"].items()
            }
        ),
        "external_scope_remains_narrow": (
            external["scope"]["ordinary_list_decoding_lower_bound"] is False
            and external["scope"]["protocol_soundness_failure"] is False
            and external["scope"]["asymptotic_theorem"] is False
            and external["scope"]["official_proximity_prize_counterpacket"] is False
            and external["scope"]["accepted_deployed_prime_field_theorem"] is False
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / EXTERNAL-CYCLE116-TRANSFER-REPLAYED",
        "theorem_problem_id": "M1 Cycle116 external transfer verifier replay",
        "source": {
            "repository": contract["provenance"]["repository"],
            "pull_request": int(contract["provenance"]["pull_request"]),
            "head_ref": contract["provenance"]["head_ref"],
            "head_commit": SOURCE_COMMIT,
            "fetch_command": FETCH_COMMAND,
        },
        "external_decision": external["decision"],
        "external_import_paths": import_paths,
        "native_row": {
            "n": int(native["n"]),
            "k": int(native["k"]),
            "agreement": int(native["agreement"]),
            "LD_sw_lower_bound": int(native["LD_sw_lower_bound"]),
        },
        "smooth_lift": {
            "n": int(smooth["n"]),
            "k": int(smooth["k"]),
            "agreement": int(smooth["agreement"]),
            "LD_sw_lower_bound": int(smooth["LD_sw_lower_bound"]),
            "strictly_greater_than_2^-128": bool(
                smooth["strictly_greater_than_2^-128"]
            ),
        },
        "field_parameter_ledger": {
            "q_gen": int(ledger["q_gen"]),
            "q_code": int(ledger["q_code"]),
            "q_line": int(ledger["q_line"]),
            "q_chal": ledger["q_chal"],
            "bad_slope_numerator": int(ledger["bad_slope_numerator"]),
            "floor_q_line_over_2^128": int(ledger["floor_q_line_over_2^128"]),
        },
        "one_affine_line_receipt": {
            "support_size": int(affine["support_size"]),
            "f_word_sha256": affine["f_word_sha256"],
            "g_word_sha256": affine["g_word_sha256"],
            "z0_sha256": affine["z0_sha256"],
        },
        "checks": checks,
        "remaining_imports": [
            "reviewer acceptance of the external verifier proof logic",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    native = report["native_row"]
    smooth = report["smooth_lift"]
    ledger = report["field_parameter_ledger"]
    source = report["source"]

    print("m1_cycle116_external_transfer_replay: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "source="
        f"PR #{source['pull_request']} {source['head_ref']} "
        f"commit {source['head_commit']}"
    )
    print(
        "native="
        f"LD_sw([n={native['n']},k={native['k']}],{native['agreement']}) "
        f">= {native['LD_sw_lower_bound']}"
    )
    print(
        "smooth="
        f"LD_sw([n={smooth['n']},k={smooth['k']}],{smooth['agreement']}) "
        f">= {smooth['LD_sw_lower_bound']}, "
        f">2^-128={smooth['strictly_greater_than_2^-128']}"
    )
    print(
        "field_ledger="
        f"q_gen=q_code=q_line={ledger['q_line']}, q_chal={ledger['q_chal']}"
    )
    print(
        "affine_line="
        f"support_size={report['one_affine_line_receipt']['support_size']}, "
        f"f={report['one_affine_line_receipt']['f_word_sha256'][:12]}, "
        f"g={report['one_affine_line_receipt']['g_word_sha256'][:12]}"
    )
    print("fetch_command=" + source["fetch_command"])
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replay the PR #96 Cycle116 external transfer verifier."
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
