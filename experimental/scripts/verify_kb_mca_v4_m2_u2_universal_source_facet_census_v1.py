#!/usr/bin/env python3
"""Verify the universal degree-two source-facet census packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from itertools import combinations, product
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
    / "data/certificates/kb-mca-v4-m2-u2-universal-source-facet-census-v1"
    / "kb_mca_v4_m2_u2_universal_source_facet_census_v1.json"
)
PARENT = {
    "commit": "c88438d7109cf7acd7caebaf006f21c776b74d74",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.md",
    "note_blob_oid": "f58c2ea9cea88dfc6be637e9f1f14e86e8862cc6",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.py",
    "verifier_blob_oid": "7cc4eb6e0560ca5c587f91623dc407892a07e2ca",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r4-order2-source-subfield-coefficient-compilers-v1/kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.json",
    "certificate_blob_oid": "033043e7a0969ea9f98207567b890b10e3077271",
    "certificate_payload_sha256": "f0b751301e56989bf6fbf19cf15e5ff8faa0d7d86e76278306950a488cdf5156",
    "terminal": "M2_R4_ORDER_TWO_SOURCE_SUBFIELD_AND_COEFFICIENT_COMPILERS",
}
SOURCE_REDUCTION_PARENT = {
    "commit": "ad109774f7d9bc320e7e0c046ba83471f39d5cd9",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.md",
    "note_blob_oid": "bd4ca8c756c22f6f475cb06c142de4c981d6b320",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.py",
    "verifier_blob_oid": "c5e7338fc03acdd245c60291aea27b0cde521645",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1/kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json",
    "certificate_blob_oid": "61afd4534740c5ccabc6196919126c80c361e4c5",
    "certificate_payload_sha256": "30a5d45895957f774ef972118e227fa54522fc27a48ee0e2a99a0d5a012a5451",
    "terminal": "DELETED_BY_COMPLETE_SOURCE_DIVISOR_PROFILE_OBSTRUCTION",
}
SOURCE_FACET_PARENT = {
    "commit": "44542e91e459364a521870ed2ebde7f6fe5055bf",
    "theorem_path": "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/proof/pole_disjoint_conic_facet_collinearity_reduction.md",
    "theorem_blob_oid": "356ff4b47d0bb429d11ea10382762a6e95b5ce24",
    "certificate_path": "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/pole_disjoint_conic_facet_collinearity_certificate.json",
    "certificate_blob_oid": "91643b5b9020f52764a77cfbc8aa6279ce2d5ef8",
    "certificate_payload_sha256": "396697687aa5baf19d8114b20858d4500b119c078f5f128b6c0e207ec8ff50bb",
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
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
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
        require(
            git_output("rev-parse", f"{PARENT['commit']}:{PARENT[path_key]}")
            == PARENT[blob_key],
            f"parent blob {PARENT[path_key]}",
        )
    data = parse_json(
        git_output("show", f"{PARENT['commit']}:{PARENT['certificate_path']}"),
        PARENT["certificate_path"],
    )
    require(data.get("payload_sha256") == PARENT["certificate_payload_sha256"],
            "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data["conclusion"]["terminal"] == PARENT["terminal"], "parent terminal")
    require(data["source_row_interpolation"]["replay"]["matrix_rows"] == 45,
            "parent source gate")
    return data


def load_source_reduction_parent() -> dict[str, Any]:
    for path_key, blob_key in (
        ("note_path", "note_blob_oid"),
        ("verifier_path", "verifier_blob_oid"),
        ("certificate_path", "certificate_blob_oid"),
    ):
        require(
            git_output(
                "rev-parse",
                f"{SOURCE_REDUCTION_PARENT['commit']}:"
                f"{SOURCE_REDUCTION_PARENT[path_key]}",
            )
            == SOURCE_REDUCTION_PARENT[blob_key],
            f"source-reduction blob {SOURCE_REDUCTION_PARENT[path_key]}",
        )
    data = parse_json(
        git_output(
            "show",
            f"{SOURCE_REDUCTION_PARENT['commit']}:"
            f"{SOURCE_REDUCTION_PARENT['certificate_path']}",
        ),
        SOURCE_REDUCTION_PARENT["certificate_path"],
    )
    require(
        data.get("payload_sha256")
        == SOURCE_REDUCTION_PARENT["certificate_payload_sha256"],
        "source-reduction payload",
    )
    require(payload_hash(data) == data.get("payload_sha256"),
            "source-reduction seal")
    require(data["conclusion"]["terminal"] == SOURCE_REDUCTION_PARENT["terminal"],
            "source-reduction terminal")
    saturation = data["complete_source_saturation"]
    require(saturation["component_source_degree"] == 2, "source degree")
    require(saturation["row_binary_degree"] == 4, "source-row degree")
    require(saturation["source_count"] == 12, "source-row count")
    require(saturation["left_total_degree"] == 48, "source-row total degree")
    require(
        saturation["product_identity"]
        == "product_i H(alpha_i,-) is proportional to B^2",
        "source product identity",
    )
    return data


def load_source_facet_parent() -> dict[str, Any]:
    require(
        git_output(
            "rev-parse",
            f"{SOURCE_FACET_PARENT['commit']}:"
            f"{SOURCE_FACET_PARENT['theorem_path']}",
        )
        == SOURCE_FACET_PARENT["theorem_blob_oid"],
        "source-facet theorem blob",
    )
    require(
        git_output(
            "rev-parse",
            f"{SOURCE_FACET_PARENT['commit']}:"
            f"{SOURCE_FACET_PARENT['certificate_path']}",
        )
        == SOURCE_FACET_PARENT["certificate_blob_oid"],
        "source-facet certificate blob",
    )
    data = parse_json(
        git_output(
            "show",
            f"{SOURCE_FACET_PARENT['commit']}:"
            f"{SOURCE_FACET_PARENT['certificate_path']}",
        ),
        SOURCE_FACET_PARENT["certificate_path"],
    )
    require(
        data.get("payload_sha256")
        == SOURCE_FACET_PARENT["certificate_payload_sha256"],
        "source-facet payload",
    )
    require(payload_hash(data) == data.get("payload_sha256"),
            "source-facet seal")
    require(
        data["theorem_status"]["q6_s6_component_edge_coloring_9_28"]
        == "PROVED",
        "component edge coloring status",
    )
    require(
        data["outgoing_conjugate_ledger"]["q6_s6_component_edge_color_multiplicity_formula"]
        == "2*u",
        "component color multiplicity",
    )
    require(
        data["outgoing_conjugate_ledger"]["q6_s6_complementary_pole_graph_left_degree"] == 2,
        "left pole-graph degree",
    )
    return data


def profile_replay() -> dict[str, Any]:
    profiles = sorted({
        tuple(sorted(4 - deficit for deficit in deficits))
        for deficits in product(range(5), repeat=6)
        if sum(deficits) == 4
    })
    expected = [
        (0, 4, 4, 4, 4, 4),
        (1, 3, 4, 4, 4, 4),
        (2, 2, 4, 4, 4, 4),
        (2, 3, 3, 4, 4, 4),
        (3, 3, 3, 3, 4, 4),
    ]
    require(profiles == expected, "five exhaustive profiles")
    require(all(sum(profile) == 20 for profile in profiles), "incidence sum")
    require(all(profile.count(0) <= 1 for profile in profiles), "one absent label")
    return {
        "category_census": {"J-J": 10, "I-I": 10, "I-J": 4},
        "J_incidence_over_K": 20,
        "J_incidence_outside_K": 4,
        "profiles": [list(profile) for profile in profiles],
        "profile_count": len(profiles),
        "maximum_absent_J_labels": 1,
        "uses_stabilizer_symmetry": False,
        "ramification_counted_by_divisor_multiplicity": True,
    }


def component_color_replay() -> dict[str, Any]:
    profiles = sorted({
        tuple(sorted(4 - deficit for deficit in deficits))
        for deficits in product(range(3), repeat=6)
        if sum(deficits) == 4
    })
    expected = [
        (2, 2, 4, 4, 4, 4),
        (2, 3, 3, 4, 4, 4),
        (3, 3, 3, 3, 4, 4),
    ]
    require(profiles == expected, "three color-surviving profiles")
    require(all(min(profile) >= 2 for profile in profiles),
            "all J labels occur over K")
    return {
        "component_source_degree": 2,
        "colored_edge_count": 4,
        "left_pole_graph_degree": 2,
        "outside_K_deficit_is_left_colored_degree": True,
        "maximum_deficit": 2,
        "surviving_profiles": [list(profile) for profile in profiles],
        "surviving_profile_count": len(profiles),
        "every_J_label_occurs_over_K": True,
        "uses_zero_migration_condition": False,
        "uses_stabilizer_symmetry": False,
    }


def colored_resultant_split_replay() -> dict[str, Any]:
    checked = 0
    for colored_tuple in combinations(range(12), 4):
        colored = set(colored_tuple)
        j_orders = [int(slot in colored) for slot in range(12)]
        i_orders = [2 - order for order in j_orders]
        require(sum(j_orders) == 4, "colored J degree")
        require(sum(i_orders) == 20, "exchange I degree")
        require(all(i_order + j_order == 2
                    for i_order, j_order in zip(i_orders, j_orders)),
                "exchange square split")
        checked += 1
    require(checked == 495, "colored divisor census")
    return {
        "colored_divisor_degree": 4,
        "colored_divisor_squarefree": True,
        "colored_divisor_divides_L_complement_pullback": True,
        "common_K_pullback_degree": 10,
        "remaining_pullback_degree": 14,
        "P_I_degree": 6,
        "P_J_degree": 6,
        "partial_resultant_degrees": {"I": 24, "J": 24},
        "J_resultant_identity": "Res_T(P_J,H) is proportional to D_K^2*C_H",
        "I_resultant_identity": "C_H*Res_T(P_I,H) is proportional to D_R^2",
        "left_deficit_recovery": "c_j=deg gcd(C_H,bZ_j)",
        "four_root_divisors_checked": checked,
        "uses_stabilizer_symmetry": False,
    }


def expected_certificate() -> dict[str, Any]:
    data = {
        "schema": "kb-mca-v4-m2-u2-universal-source-facet-census-v1",
        "parent": PARENT,
        "source_reduction_parent": SOURCE_REDUCTION_PARENT,
        "source_facet_parent": SOURCE_FACET_PARENT,
        "universal_source_facet": profile_replay(),
        "component_color_profile_cut": component_color_replay(),
        "colored_source_resultant_split": colored_resultant_split_replay(),
        "universal_source_interpolation": {
            "actual_source_bidegree": [2, 4],
            "source_count": 12,
            "row_binary_degree": 4,
            "matrix_rows": 45,
            "matrix_columns": 12,
            "kernel_condition": "full support",
            "complete_source_product": "product_i q_i is proportional to B^2",
            "stabilizer_types_r_delta": [[2, 4], [4, 2], [8, 1]],
            "uses_stabilizer_symmetry": False,
            "applies_to_trivial_stabilizer": True,
        },
        "scope": {
            "coordinate_order_two": True,
            "diagonal_order_two": True,
            "trivial_stabilizer_r8_delta1": True,
            "coordinate_pairing_transferred_to_trivial": False,
        },
        "conclusion": {
            "order_two_type_deleted": False,
            "trivial_stabilizer_type_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": "M2_U2_UNIVERSAL_SOURCE_FACET_COLOR_INTERPOLATION_AND_RESULTANT_INTERFACES",
        },
        "nonclaims": [
            "no stabilizer action or paired degree profile in the trivial branch",
            "no universal source-row kernel failure",
            "no component, type, owner, payment, K3, row, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["universal_source_facet"]["category_census"].__setitem__("I-J", 5),
        lambda x: x["universal_source_facet"].__setitem__("J_incidence_over_K", 19),
        lambda x: x["universal_source_facet"].__setitem__("profile_count", 4),
        lambda x: x["universal_source_facet"]["profiles"].pop(),
        lambda x: x["universal_source_facet"].__setitem__("uses_stabilizer_symmetry", True),
        lambda x: x["scope"].__setitem__("trivial_stabilizer_r8_delta1", False),
        lambda x: x["scope"].__setitem__("coordinate_pairing_transferred_to_trivial", True),
        lambda x: x["universal_source_interpolation"].__setitem__("matrix_rows", 44),
        lambda x: x["universal_source_interpolation"].__setitem__("actual_source_bidegree", [4, 4]),
        lambda x: x["universal_source_interpolation"].__setitem__("uses_stabilizer_symmetry", True),
        lambda x: x["universal_source_interpolation"].__setitem__("applies_to_trivial_stabilizer", False),
        lambda x: x["component_color_profile_cut"].__setitem__("colored_edge_count", 3),
        lambda x: x["component_color_profile_cut"].__setitem__("maximum_deficit", 3),
        lambda x: x["component_color_profile_cut"]["surviving_profiles"].pop(),
        lambda x: x["colored_source_resultant_split"].__setitem__("colored_divisor_degree", 5),
        lambda x: x["colored_source_resultant_split"].__setitem__("colored_divisor_squarefree", False),
        lambda x: x["colored_source_resultant_split"].__setitem__("common_K_pullback_degree", 9),
        lambda x: x["colored_source_resultant_split"].__setitem__("left_deficit_recovery", "untracked"),
        lambda x: x["conclusion"].__setitem__("trivial_stabilizer_type_deleted", True),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["parent"].__setitem__("certificate_payload_sha256", "0" * 64),
        lambda x: x["source_reduction_parent"].__setitem__("certificate_payload_sha256", "0" * 64),
        lambda x: x["source_facet_parent"].__setitem__("certificate_payload_sha256", "0" * 64),
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
    args = parser.parse_args()

    load_parent()
    load_source_reduction_parent()
    load_source_facet_parent()
    expected = expected_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    if args.check or not args.write:
        require(CERTIFICATE.is_file(), "missing certificate")
        data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
        verify_data(data)
    else:
        data = expected
    rejected = tamper_selftest(data) if args.tamper_selftest else 0
    print(
        "KB_MCA_V4_M2_U2_UNIVERSAL_SOURCE_FACET_CENSUS_PASS "
        f"raw_profiles={data['universal_source_facet']['profile_count']} "
        f"surviving_profiles={data['component_color_profile_cut']['surviving_profile_count']} "
        f"colored_divisors={data['colored_source_resultant_split']['four_root_divisors_checked']} "
        f"tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
