#!/usr/bin/env python3
"""Verify the saturated (1,1,2) source-line q-slice exclusions."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m2-u2-saturated-112-q-slice-exclusions-v1"
    / "kb_mca_v4_m2_u2_saturated_112_q_slice_exclusions_v1.json"
)
PARENT = {
    "commit": "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc",
    "note_path": (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_m2_u2_universal_source_facet_census_v1.md"
    ),
    "note_blob_oid": "cc315015998cf9ab0ecf2970c13f1e27f1f132d6",
    "verifier_path": (
        "experimental/scripts/"
        "verify_kb_mca_v4_m2_u2_universal_source_facet_census_v1.py"
    ),
    "verifier_blob_oid": "e810f286d5b67d19660c3c382501a690e3e76fb0",
    "certificate_path": (
        "experimental/data/certificates/"
        "kb-mca-v4-m2-u2-universal-source-facet-census-v1/"
        "kb_mca_v4_m2_u2_universal_source_facet_census_v1.json"
    ),
    "certificate_blob_oid": "844b7885620bf10fe19336f3acd7866cf1d9a204",
    "certificate_payload_sha256": (
        "8f768cfded349dc3dd40cf6214ffe980c69ff18ae2d8c209e63b4307767429d2"
    ),
    "terminal": (
        "M2_U2_SOURCE_FACET_COLOR_COORDINATE_QUOTIENT_VIETA_TRANSPOSE_"
        "DIAGONAL_MIXING_C6_QUOTIENT_C2_CAPACITY_C2_SOURCE_LINEAR_C2_202_"
        "ROW_DEFECT_C2_112_SATURATED_DEFECT_C2_112_SOURCE_QUOTIENT_C2_112_"
        "ODD_INCIDENCE_C2_112_RAMIFIED_REPAIR_C2_112_FINITE_RECONSTRUCTION_"
        "C2_112_Q_SLICE_NEGATIVE_FACTOR_AND_ALIGNED_NEGATIVE_EXCLUSION_"
        "INTERFACES"
    ),
}

HELPERS = {
    "negative_core": (
        EXPERIMENTAL
        / "scripts/kb_mca_v4_m2_u2_saturated_112_negative_qslice_core_v1.py"
    ),
    "near_negative": (
        EXPERIMENTAL
        / "scripts/kb_mca_v4_m2_u2_saturated_112_near_negative_qslice_v1.py"
    ),
    "positive_core": (
        EXPERIMENTAL
        / "scripts/kb_mca_v4_m2_u2_saturated_112_positive_qslice_core_v1.py"
    ),
    "aligned_ramified": (
        EXPERIMENTAL
        / "scripts/"
        "kb_mca_v4_m2_u2_saturated_112_aligned_positive_ramified_qslice_v1.py"
    ),
    "near_projective": (
        EXPERIMENTAL
        / "scripts/"
        "kb_mca_v4_m2_u2_saturated_112_near_positive_projective_qslice_v1.py"
    ),
}
HELPER_SHA256 = {
    "negative_core": "412ccf180a4de9b39bb33330397c72e79994f5c9f00e2e6f3df4d5e377c89a9c",
    "near_negative": "958ca2c6e53380ead0b8f90599f500417ef2e842c7ce999497d3a2da11a509a9",
    "positive_core": "242d76eb58a0af2cbffa1cedfbcfd116b6b3a7912d9db64e1ec022ff59dd4a13",
    "aligned_ramified": "2b9ea459bff2d46a8a04404e54d1d585f14a69f59237f4383b5951f5d5c3d599",
    "near_projective": "d1f36c8451a3407adc4c58436c6a67f8c25777da47752be4ea60833bb1b570a1",
}


def deep_case(helper: str, arguments: list[str], *fragments: str) -> dict[str, Any]:
    return {
        "helper": helper,
        "arguments": arguments,
        "required_output_fragments": list(fragments),
    }


DEEP_CASES = {
    "near-negative-template": deep_case(
        "near_negative",
        ["fixed-moving", "--compare-templates"],
        "NEAR_NEGATIVE_TEMPLATE_EQUIVALENCE_PASS",
        "same_z=true U_opposite=true V_equal=true G_equal=true",
    ),
    "near-negative-a": deep_case(
        "near_negative",
        [
            "fixed-moving", "--xi", "a", "--eliminate", "--fibers",
            "--modular-saturate",
        ],
        "projection=(c + 2)**4*(13*c - 14)**4",
        "fiber=-2 w_gcd_degree=2 w_gcd=w**2 + 2*w + 1",
        "fiber=14/13 w_gcd_degree=2 w_gcd=w**2 - 2*w + 1",
        "xi=a modular_forbidden_saturation_unit=True",
    ),
    "near-negative-tau-a": deep_case(
        "near_negative",
        [
            "fixed-moving", "--xi", "tau-a", "--eliminate", "--fibers",
            "--modular-saturate",
        ],
        "projection=(2*c + 1)**4*(14*c - 13)**4",
        "fiber=-1/2 w_gcd_degree=2 w_gcd=w**2 + 2*w + 1",
        "fiber=13/14 w_gcd_degree=2 w_gcd=w**2 - 2*w + 1",
        "xi=tau-a modular_forbidden_saturation_unit=True",
    ),
    "near-negative-other": deep_case(
        "near_negative",
        [
            "fixed-moving", "--xi", "other", "--eliminate", "--fibers",
            "--modular-saturate",
        ],
        "projection=d**2*(d - 1)**6*(d + 1)**6*(d + 2)**4*",
        "(d**3 - 6*d**2 + 3*d - 2)**4",
        "fiber=0 w_gcd_degree=2 w_gcd=w**2",
        "d**3 - 6*d**2 + 3*d - 2 w_gcd_degree=2 w_gcd=w**2 + 2*w + 1",
        "xi=other modular_forbidden_saturation_unit=True",
    ),
    "aligned-ramified-fixed-same": deep_case(
        "aligned_ramified", ["fixed-moving", "same"], "basis=unit",
        "digest=48e8be2962036927d72c8dbc299b449e94b6902ce22f4aa97e4c5343779bcace",
    ),
    "aligned-ramified-fixed-swap": deep_case(
        "aligned_ramified", ["fixed-moving", "swap"], "basis=unit",
        "digest=ea4a29b822314685d3eb91337372b2c19f8d7065bc8f4364f13361abb1c92341",
    ),
    "aligned-ramified-fixed-mixed": deep_case(
        "aligned_ramified", ["fixed-moving", "mixed"], "basis=unit",
        "digest=c88354fa6c3284c4ffe460eee511f8a0d6b71809f02dfac55a99ca6234a204ff",
    ),
    "aligned-ramified-moving-same": deep_case(
        "aligned_ramified", ["moving-moving", "same"], "basis=unit",
        "digest=0ab646a7f71d52ac6ad157b50635d36f6541802f207420b73713b5d23e8d402b",
    ),
    "aligned-ramified-moving-swap": deep_case(
        "aligned_ramified", ["moving-moving", "swap"], "basis=unit",
        "digest=0af2e99f4c89721fc9baeec36da3ffc8ca0ef17fe4f9bf6e542602a76b5f1e58",
    ),
    "aligned-ramified-moving-mixed": deep_case(
        "aligned_ramified", ["moving-moving", "mixed"], "basis=unit",
        "digest=06b3195101008998876f26e6468ad830b3e81bdc51981b0533ffa626fd279330",
    ),
    "near-projective-fixed-a": deep_case(
        "near_projective", ["fixed-moving", "--xi", "a"], "basis=unit",
        "digest=70f4c010cd06ee27cb03658b4d58758b556f30760f178c16e035a6145e2fc442",
    ),
    "near-projective-fixed-tau-a": deep_case(
        "near_projective", ["fixed-moving", "--xi", "tau-a"], "basis=unit",
        "digest=6b5f573cdb40bb1143ee598f4bcd7c024b7228065ab3f489b535ee67af1eaa3e",
    ),
    "near-projective-fixed-other": deep_case(
        "near_projective", ["fixed-moving", "--xi", "other"], "basis=unit",
        "digest=7409bb53fad5683912a596423d2ff8ff6ff5cc0619703610a363047fc3cc51a2",
    ),
    "near-projective-moving-a": deep_case(
        "near_projective", ["moving-moving", "--xi", "a"], "basis=unit",
        "digest=1411f536466ee16b420ff956240e8254721749e0798d75b8091c98050cdc57ba",
    ),
    "near-projective-moving-tau-a": deep_case(
        "near_projective", ["moving-moving", "--xi", "tau-a"], "basis=unit",
        "digest=fb5f5f73633bc2aa9efd82d8bfa79d076157c8ea02b29009e4eaef206a07f255",
    ),
    "near-projective-moving-other-plus": deep_case(
        "near_projective",
        ["moving-moving", "--xi", "other", "--sign", "1"],
        "basis=unit",
        "digest=2e20bddd6b75d705498f04513efea4267667f974310149a26fa61f566f68e1ef",
    ),
    "near-projective-moving-other-minus": deep_case(
        "near_projective",
        ["moving-moving", "--xi", "other", "--sign", "-1"],
        "basis=unit",
        "digest=e0817f557782249d5af979161b32d577cd04394ba351e47e2754e9f727af46d1",
    ),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def load_parent() -> dict[str, Any]:
    for path_key, blob_key in (
        ("note_path", "note_blob_oid"),
        ("verifier_path", "verifier_blob_oid"),
        ("certificate_path", "certificate_blob_oid"),
    ):
        actual = git_output("rev-parse", f"{PARENT['commit']}:{PARENT[path_key]}")
        require(actual == PARENT[blob_key], f"parent blob {PARENT[path_key]}")
    data = parse_json(
        git_output("show", f"{PARENT['commit']}:{PARENT['certificate_path']}"),
        PARENT["certificate_path"],
    )
    require(
        data.get("payload_sha256") == PARENT["certificate_payload_sha256"],
        "parent payload",
    )
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data["conclusion"]["terminal"] == PARENT["terminal"], "parent terminal")
    require(
        data["diagonal_c2_112_negative_factor"][
            "aligned_negative_q_slice_deleted"
        ],
        "parent aligned-negative deletion",
    )
    require(
        not data["diagonal_c2_112_negative_factor"][
            "near_aligned_negative_deleted"
        ],
        "parent near-negative frontier",
    )
    require(
        not data["diagonal_c2_112_negative_factor"]["positive_sign_deleted"],
        "parent positive frontier",
    )
    return data


def verify_helper_hashes() -> None:
    for name, path in HELPERS.items():
        require(path.is_file(), f"missing helper: {name}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == HELPER_SHA256[name], f"helper hash: {name}")


def expected_certificate() -> dict[str, Any]:
    data: dict[str, Any] = {
        "schema": "kb-mca-v4-m2-u2-saturated-112-q-slice-exclusions-v1",
        "workboard_item": "K3",
        "row": "KoalaBear MCA at 2^-128",
        "object": "MCA",
        "target_epsilon": "2^-128",
        "agreement": 1116048,
        "B_star": 274980728111395087,
        "deployed_base_characteristic": 2130706433,
        "parent": copy.deepcopy(PARENT),
        "helper_sha256": copy.deepcopy(HELPER_SHA256),
        "near_aligned_negative": {
            "templates_covered": ["fixed-moving", "moving-moving"],
            "relative_xi_orbits": ["2", "1/2", "b"],
            "moving_C_locus_covered_by_inversion": True,
            "forced_ramification_w_zero_included": True,
            "constant_gate": "(xi*d)^2=1",
            "plus_branch": "label collision d=tau(xi)",
            "minus_branch_projections": {
                "xi=2": "(c+2)^4*(13c-14)^4",
                "xi=1/2": "(2c+1)^4*(14c-13)^4",
                "xi=b": (
                    "d^2*(d-1)^6*(d+1)^6*(d+2)^4*"
                    "(d^3-6d^2+3d-2)^4"
                ),
            },
            "admissible_residue_fibers": 0,
            "deployed_prime_saturations": 3,
            "deleted": True,
        },
        "aligned_positive_forced_ramified": {
            "source_parameter": "w=0",
            "templates": ["fixed-moving", "moving-moving"],
            "allocations": ["same", "swap", "mixed"],
            "relative_scales": {
                "fixed-moving": "3*(2b-1)*(p-1)*(p+2t+4)",
                "moving-moving": (
                    "-3*(b-1)*(b+1)*(p-1)*(p+2t+4)*(5p+4t+5)"
                ),
            },
            "deployed_prime_unit_ideals": 6,
            "moving_trace_descent": "s=b+1/b",
            "deleted": True,
        },
        "near_aligned_positive_projective_boundary": {
            "homogeneous_q": "Y*(T-dY)",
            "oriented_endpoint": "eta=infinity",
            "source_parameter": "w=tau(eta)=0",
            "odd_vector": ["-d", "1+W", "-dW"],
            "internal_label": "(d-2)/(2-4d)",
            "projective_q_slice": "G(d,W)*coeff_T^4(G(T,W))",
            "fixed_moving_unit_ideals": 3,
            "moving_fixed_xi_trace_unit_ideals": 2,
            "moving_other_xi_sign_unit_ideals": 2,
            "deployed_prime_unit_ideals": 7,
            "deleted": True,
        },
        "synthesis": {
            "near_positive_affine_cells_banked_here": 0,
            "near_positive_affine_cells_proved_in_prize_not_imported": 18,
            "near_positive_projective_cells_deleted_here": 7,
            "near_negative_branch_deleted_here": True,
            "near_aligned_source_line_branch_deleted_here": False,
            "aligned_negative_branch_deleted_by_parent": True,
            "aligned_positive_forced_ramified_deleted_here": True,
            "aligned_forced_ramified_source_line_branch_deleted": True,
            "remaining_aligned_positive_unramified_cells": [
                "fixed-moving/same/w!=0",
                "fixed-moving/swap/w!=0",
                "fixed-moving/mixed/w!=0",
                "moving-moving/same/w!=0",
                "moving-moving/swap/w!=0",
                "moving-moving/mixed/w!=0",
            ],
        },
        "deep_replay": {
            "wall_time_cap_seconds_per_case": 60,
            "serial_execution_required": True,
            "case_count": len(DEEP_CASES),
            "cases": copy.deepcopy(DEEP_CASES),
        },
        "conclusion": {
            "near_aligned_source_line_branch_deleted_here": False,
            "aligned_forced_ramified_source_line_branch_deleted": True,
            "aligned_positive_unramified_cells_remaining": 6,
            "row_112_deleted": False,
            "order_two_type_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": (
                "M2_U2_SATURATED_112_NEAR_ALIGNED_Q_SLICE_AND_ALIGNED_"
                "FORCED_RAMIFIED_EXCLUSIONS"
            ),
        },
        "nonclaims": [
            "no sufficiency claim for the necessary q-slice identity",
            "no banking here of the separately proved 18-cell near-positive affine ledger",
            "no complete near-aligned source-line deletion from this packet alone",
            "no deletion of the six aligned positive unramified cells",
            "no deletion of the full saturated (1,1,2) orbit row",
            "no later packet, source-row, owner, or payment assembly",
            "no order-two type, K3, KoalaBear row, or Prize close",
        ],
        "provenance": {
            "prize_near_negative_commit": "08a2e4de",
            "prize_aligned_positive_ramified_commit": "e9baa0de",
            "prize_near_positive_projective_commit": "7d2d7aca",
            "upstream_parent_pr": 1132,
        },
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def normalized_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode(errors="replace")
    return value


def run_deep_case(name: str) -> None:
    require(name in DEEP_CASES, f"unknown deep case: {name}")
    verify_helper_hashes()
    case = DEEP_CASES[name]
    command = [sys.executable, str(HELPERS[case["helper"]]), *case["arguments"]]
    process = subprocess.Popen(
        command,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=60)
    except subprocess.TimeoutExpired as error:
        partial = normalized_output(error.output)
        os.killpg(process.pid, signal.SIGTERM)
        try:
            tail, _ = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            tail, _ = process.communicate()
        output = partial + normalized_output(tail)
        print(output, end="")
        raise VerificationError(f"deep case exceeded 60 seconds: {name}") from error
    print(output, end="")
    require(process.returncode == 0, f"deep case exit: {name}")
    for fragment in case["required_output_fragments"]:
        require(fragment in output, f"deep case output {name}: {fragment}")
    print(f"KB_MCA_SATURATED_112_DEEP_CASE_PASS case={name}")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["near_aligned_negative"].__setitem__("deleted", False),
        lambda x: x["near_aligned_negative"].__setitem__(
            "admissible_residue_fibers", 1
        ),
        lambda x: x["aligned_positive_forced_ramified"].__setitem__(
            "deployed_prime_unit_ideals", 5
        ),
        lambda x: x["near_aligned_positive_projective_boundary"].__setitem__(
            "homogeneous_q", "T*(T-d)"
        ),
        lambda x: x["synthesis"][
            "remaining_aligned_positive_unramified_cells"
        ].pop(),
        lambda x: x["conclusion"].__setitem__(
            "near_aligned_source_line_branch_deleted_here", True
        ),
        lambda x: x["conclusion"].__setitem__(
            "aligned_positive_unramified_cells_remaining", 0
        ),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["helper_sha256"].__setitem__("near_negative", "0" * 64),
        lambda x: x["parent"].__setitem__("certificate_payload_sha256", "0" * 64),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
    ]
    rejected = 0
    for mutation in mutations:
        hostile = copy.deepcopy(data)
        mutation(hostile)
        try:
            verify_data(hostile)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "tamper self-test")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--list-deep", action="store_true")
    parser.add_argument("--deep-case", choices=sorted(DEEP_CASES))
    parser.add_argument("--deep-all", action="store_true")
    args = parser.parse_args()

    if args.list_deep:
        print("\n".join(sorted(DEEP_CASES)))
        return

    load_parent()
    verify_helper_hashes()
    expected = expected_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    if args.check or not (args.write or args.deep_case or args.deep_all):
        require(CERTIFICATE.is_file(), "missing certificate")
        data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
        verify_data(data)
    else:
        data = expected

    if args.deep_case:
        run_deep_case(args.deep_case)
    if args.deep_all:
        for name in sorted(DEEP_CASES):
            run_deep_case(name)
    rejected = tamper_selftest(data) if args.tamper_selftest else 0
    print(
        "KB_MCA_V4_M2_U2_SATURATED_112_Q_SLICE_EXCLUSIONS_PASS "
        f"near_negative_saturations="
        f"{data['near_aligned_negative']['deployed_prime_saturations']} "
        f"aligned_ramified_unit_ideals="
        f"{data['aligned_positive_forced_ramified']['deployed_prime_unit_ideals']} "
        f"near_projective_unit_ideals="
        f"{data['near_aligned_positive_projective_boundary']['deployed_prime_unit_ideals']} "
        f"remaining_unramified="
        f"{data['conclusion']['aligned_positive_unramified_cells_remaining']} "
        f"deep_cases={data['deep_replay']['case_count']} "
        f"tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
