"""Verify the KoalaBear fixed-domain rank-16 equality-wall reduction."""

from __future__ import annotations

import argparse
import copy
import math
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_equality_wall_residue_line_partition_reduction_v1 as parent

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-equality-wall-fixed-domain-rank16-normalization-v1"
)
CERT_PATH = CERT_DIR / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.schema.json"
)

ARCH = parent.ARCH
PARTITION_DIGEST = parent.PARTITION_DIGEST
R = parent.R
P = parent.FIELD_P
S = parent.SOURCE_SIZE
E = parent.E
C = parent.C
V_SIZE = parent.CARRIER_SIZE
J = parent.LOCATOR_DEGREE
M = parent.TARGET_PACKET_SIZE
PAIR_COUNT = parent.TARGET_PAIR_COUNT
K0_DIMENSION = parent.SELECTOR_KERNEL_DIMENSION

COMPLEMENT_LOCATOR_DEGREE = V_SIZE - J
TRANSVERSAL_DOMAIN_FLOOR = V_SIZE - C
NORMALIZED_DOMAIN_BASE = J + C
DELTA_MAX = V_SIZE - NORMALIZED_DOMAIN_BASE
NORMALIZED_LOCATOR_DEGREE_BASE = C
LOCATOR_COEFFICIENT_RANK_CAP = 2 * K0_DIMENSION
GRAPH_POLYNOMIAL_SPACE_DIMENSION_CAP = K0_DIMENSION + 1
STRENGTHENED_FORBIDDEN_PARAMETER_CAP = (
    parent.FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP + C + M
)
STRENGTHENED_PARAMETER_MARGIN = P - STRENGTHENED_FORBIDDEN_PARAMETER_CAP
NORMALIZED_GRAPH_DEGREE_MAX = S + DELTA_MAX
PUSHFORWARD_MAX_SPLITTING_DEGREE = NORMALIZED_GRAPH_DEGREE_MAX // E
GENERIC_KERNEL_BRANCH_CAP = (
    GRAPH_POLYNOMIAL_SPACE_DIMENSION_CAP
    * PUSHFORWARD_MAX_SPLITTING_DEGREE
)
INCIDENCE_FIRST_INFEASIBLE_DELTA = 3_911
INCIDENCE_FIRST_FEASIBLE_DELTA = 3_912

Failure = parent.Failure
need = parent.need
seal = parent.seal
dump = parent.dump
load = parent.load
file_digest = parent.file_digest

UPSTREAM_CERTIFICATES = {
    "equality_wall_residue_line_partition": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-equality-wall-residue-line-partition-reduction-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'e2f3159960425614b6cb6e3bf849b2d737a6f6525e8aeb37d266804acfb9ef17'
        ),
    }
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.md"
    ),
]


def balanced_pair_incidence(delta: int) -> dict[str, int]:
    domain_size = NORMALIZED_DOMAIN_BASE + delta
    locator_degree = NORMALIZED_LOCATOR_DEGREE_BASE + delta
    total_incidence = M * locator_degree
    quotient, remainder = divmod(total_incidence, domain_size)
    minimum = (
        (domain_size - remainder) * math.comb(quotient, 2)
        + remainder * math.comb(quotient + 1, 2)
    )
    cap = PAIR_COUNT * delta
    return {
        "delta": delta,
        "domain_size": domain_size,
        "locator_degree": locator_degree,
        "total_incidence": total_incidence,
        "balanced_quotient": quotient,
        "balanced_remainder": remainder,
        "minimum_pair_incidence": minimum,
        "pair_intersection_cap": cap,
        "cap_minus_minimum": cap - minimum,
    }


def source_bindings() -> list[dict[str, str]]:
    bindings = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        bindings.append(
            {
                "binding_id": (
                    f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}"
                ),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return bindings


def upstream_bindings() -> dict[str, dict[str, str]]:
    bindings = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        certificate = load(path)
        need(
            certificate.get("payload_sha256")
            == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        bindings[key] = {**contract, "file_sha256": file_digest(path)}
    return bindings


def exact_arithmetic() -> dict[str, Any]:
    at_3911 = balanced_pair_incidence(
        INCIDENCE_FIRST_INFEASIBLE_DELTA
    )
    at_3912 = balanced_pair_incidence(
        INCIDENCE_FIRST_FEASIBLE_DELTA
    )
    return {
        "base_field_size": P,
        "source_size": S,
        "source_pencil_degree": E,
        "minimum_active_exchange": C,
        "carrier_size": V_SIZE,
        "moving_set_size": J,
        "target_packet_size": M,
        "target_pair_count": PAIR_COUNT,
        "selector_kernel_dimension": K0_DIMENSION,
        "complement_locator_degree": COMPLEMENT_LOCATOR_DEGREE,
        "transversal_evaluation_domain_floor": TRANSVERSAL_DOMAIN_FLOOR,
        "normalized_domain_base": NORMALIZED_DOMAIN_BASE,
        "normalized_excess_upper_bound": DELTA_MAX,
        "normalized_locator_degree_base": NORMALIZED_LOCATOR_DEGREE_BASE,
        "locator_coefficient_rank_cap": LOCATOR_COEFFICIENT_RANK_CAP,
        "graph_polynomial_space_dimension_cap": (
            GRAPH_POLYNOMIAL_SPACE_DIMENSION_CAP
        ),
        "full_domain_forbidden_parameter_cap": (
            parent.FULL_DOMAIN_SOURCE_UNIT_FORBIDDEN_PARAMETER_CAP
        ),
        "strengthened_forbidden_parameter_cap": (
            STRENGTHENED_FORBIDDEN_PARAMETER_CAP
        ),
        "strengthened_parameter_margin": STRENGTHENED_PARAMETER_MARGIN,
        "normalized_graph_degree_maximum": NORMALIZED_GRAPH_DEGREE_MAX,
        "eight_times_source_pencil_degree": 8 * E,
        "pushforward_maximum_splitting_degree": (
            PUSHFORWARD_MAX_SPLITTING_DEGREE
        ),
        "generic_kernel_free_branch_cap": GENERIC_KERNEL_BRANCH_CAP,
        "incidence_delta_3911": at_3911,
        "incidence_delta_3912": at_3912,
        "first_feasible_pair_incidence_delta": (
            INCIDENCE_FIRST_FEASIBLE_DELTA
        ),
        "delta_3912_pair_incidence_margin": (
            at_3912["cap_minus_minimum"]
        ),
        "source_zero_kernel_degree_descent": E,
        "maximum_source_zero_descent_steps": DELTA_MAX // E,
        "additional_charge": 0,
        "first_open_slack": R,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": (
                "HYPOTHETICAL 69-SOURCE-MAP-CLASS PRIMITIVE TRANSVERSAL "
                "RESIDUE LINE AT THE R=134943 EQUALITY WALL"
            ),
            "active_ledger": {
                "B_remaining": parent.B_REMAINING,
                "additional_charge": 0,
                "first_open_slack": R,
            },
            "theorem": {
                "all_69_complement_locators_have_coefficient_rank_at_most_16": (
                    True
                ),
                "canonical_star_basis_has_at_most_8_records": True,
                "all_69_moving_sets_lie_in_one_9_set_union": True,
                "normalized_locators_are_monic_and_split_on_one_fixed_domain": (
                    True
                ),
                "normalized_pair_intersection_at_most_delta": True,
                "normalized_total_intersection_is_empty": True,
                "normalized_locator_span_dimension_at_most_16": True,
                "exact_fixed_domain_rs_agreement_list": True,
                "agreement_polynomials_have_affine_dimension_at_most_8": (
                    True
                ),
                "pair_incidence_forces_delta_at_least_3912": True,
                "delta_3912_pair_incidence_margin_is_458": True,
                "strengthened_source_parameter_exists": True,
                "strengthened_source_pencil_is_coprime_exact_degree_e": True,
                "graph_polynomial_space_dimension_at_most_9": True,
                "pushforward_bundle_splitting_is_exact": True,
                "generic_kernel_free_branch_has_cap_63": True,
                "hypothetical_69_packet_forces_positive_generic_kernel": True,
                "source_zero_generic_kernel_descends_by_degree_e": True,
                "source_zero_generic_kernel_recursion_is_finite": True,
                "non_source_zero_kernel_has_source_value_divisor_constraint": (
                    True
                ),
                "fixed_parameter_split_quotient_is_unique_when_delta_below_e": (
                    True
                ),
                "universal_kernel_split_quotient_status": "OPEN",
                "same_record_owner_emission_status": "OPEN_ALTERNATIVE_ROUTE",
                "line_cap_68_status": "OPEN",
                "additional_charge_status": "ZERO",
                "first_open_slack_after_packet": R,
            },
            "arithmetic": exact_arithmetic(),
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_FIXED_DOMAIN_RANK16_NORMALIZATION_DELTA3912_"
                "COPRIME_DEGREE_E_PENCIL_GENERIC_KERNEL_CAP63_"
                "SOURCE_ZERO_KERNEL_RECURSION_SOURCE_VALUE_DIVISOR_"
                "LOW_DELTA_FIXED_PARAMETER_UNIQUENESS_"
                "UNIVERSAL_KERNEL_SPLIT_QUOTIENT_OPEN_R134943_UNCHANGED"
            ),
        }
    )


def expected_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": True,
        "properties": {
            "architecture_id": {"type": "string"},
            "partition_sha256": {
                "pattern": "^[0-9a-f]{64}$",
                "type": "string",
            },
            "payload_sha256": {
                "pattern": "^[0-9a-f]{64}$",
                "type": "string",
            },
        },
        "required": [
            "architecture_id",
            "partition_sha256",
            "payload_sha256",
        ],
        "title": (
            "KoalaBear equality-wall fixed-domain rank-16 normalization"
        ),
        "type": "object",
    }


def check_note_anchors() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.md"
    ).read_text(encoding="utf-8")
    anchors = [
        "# KoalaBear equality-wall fixed-domain rank-16 normalization",
        "\\dim_F\\operatorname{span}\\{q_1,\\ldots,q_{69}\\}\\le16",
        "Y_i\\subseteq U_0",
        "\\deg\\gcd(p_i,p_j)\\le\\delta",
        "Exact fixed-domain agreement list",
        "\\boxed{\\delta\\ge3{,}912.}",
        "=131{,}009{,}087",
        "\\gcd(U,V)=1",
        "The generic-kernel branch has cap 63",
        "\\text{the generic-kernel-free branch has at most }63",
        "Exact universal-kernel remainder",
        "This source-Cauchy divisor is an exact constraint",
        "\\deg_XQ\\le\\delta-e",
        "supports at most one normalized split quotient",
        "Universal-kernel split-quotient lemma",
        "# PROVED REDUCTION / UNIVERSAL-KERNEL BRANCH OPEN",
    ]
    for anchor in anchors:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from replay")
    need(schema == expected_schema(), "schema differs from replay")
    arithmetic = cert["arithmetic"]
    theorem = cert["theorem"]
    need(
        arithmetic["locator_coefficient_rank_cap"] == 16,
        "locator rank cap",
    )
    need(
        arithmetic["graph_polynomial_space_dimension_cap"] == 9,
        "graph space dimension",
    )
    need(
        arithmetic["transversal_evaluation_domain_floor"] == 1_827_264,
        "transversal domain",
    )
    need(
        arithmetic["normalized_domain_base"] == 1_048_577,
        "normalized domain base",
    )
    need(
        arithmetic["normalized_excess_upper_bound"] == 846_159,
        "delta upper bound",
    )
    need(
        arithmetic["strengthened_forbidden_parameter_cap"] == 131_009_087,
        "strengthened forbidden count",
    )
    need(
        arithmetic["pushforward_maximum_splitting_degree"] == 7,
        "bundle splitting degree",
    )
    need(
        arithmetic["generic_kernel_free_branch_cap"] == 63,
        "generic branch cap",
    )
    need(
        arithmetic["incidence_delta_3911"]["cap_minus_minimum"]
        == -1_622,
        "delta 3911 contradiction",
    )
    need(
        arithmetic["incidence_delta_3912"]["minimum_pair_incidence"]
        == 9_177_094,
        "delta 3912 minimum",
    )
    need(
        arithmetic["incidence_delta_3912"]["pair_intersection_cap"]
        == 9_177_552,
        "delta 3912 cap",
    )
    need(
        arithmetic["delta_3912_pair_incidence_margin"] == 458,
        "delta 3912 margin",
    )
    need(
        theorem[
            "all_69_complement_locators_have_coefficient_rank_at_most_16"
        ],
        "rank-16 theorem",
    )
    need(
        theorem["generic_kernel_free_branch_has_cap_63"],
        "generic cap theorem",
    )
    need(
        theorem["hypothetical_69_packet_forces_positive_generic_kernel"],
        "universal-kernel reduction",
    )
    need(
        theorem["universal_kernel_split_quotient_status"] == "OPEN",
        "universal-kernel status",
    )
    need(theorem["line_cap_68_status"] == "OPEN", "cap 68 remains open")
    need(
        cert["active_ledger"]["additional_charge"] == 0,
        "zero charge",
    )
    need(
        cert["active_ledger"]["first_open_slack"] == R,
        "first open unchanged",
    )
    check_note_anchors()


def emit() -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    validate(cert, schema)
    mutations = [
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["active_ledger"].__setitem__("first_open_slack", R + 1),
        lambda d: d["theorem"].__setitem__(
            "all_69_complement_locators_have_coefficient_rank_at_most_16",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "all_69_moving_sets_lie_in_one_9_set_union", False
        ),
        lambda d: d["theorem"].__setitem__(
            "pair_incidence_forces_delta_at_least_3912", False
        ),
        lambda d: d["theorem"].__setitem__(
            "strengthened_source_pencil_is_coprime_exact_degree_e", False
        ),
        lambda d: d["theorem"].__setitem__(
            "generic_kernel_free_branch_has_cap_63", False
        ),
        lambda d: d["theorem"].__setitem__(
            "hypothetical_69_packet_forces_positive_generic_kernel", False
        ),
        lambda d: d["theorem"].__setitem__(
            "source_zero_generic_kernel_descends_by_degree_e", False
        ),
        lambda d: d["theorem"].__setitem__(
            "non_source_zero_kernel_has_source_value_divisor_constraint",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "fixed_parameter_split_quotient_is_unique_when_delta_below_e",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "universal_kernel_split_quotient_status", "PROVED"
        ),
        lambda d: d["theorem"].__setitem__("line_cap_68_status", "PROVED"),
        lambda d: d["arithmetic"].__setitem__(
            "locator_coefficient_rank_cap", 17
        ),
        lambda d: d["arithmetic"].__setitem__(
            "normalized_excess_upper_bound", DELTA_MAX + 1
        ),
        lambda d: d["arithmetic"].__setitem__(
            "strengthened_forbidden_parameter_cap",
            STRENGTHENED_FORBIDDEN_PARAMETER_CAP + 1,
        ),
        lambda d: d["arithmetic"].__setitem__(
            "generic_kernel_free_branch_cap", 64
        ),
        lambda d: d["arithmetic"]["incidence_delta_3911"].__setitem__(
            "cap_minus_minimum", 0
        ),
        lambda d: d["arithmetic"]["incidence_delta_3912"].__setitem__(
            "minimum_pair_incidence", 9_177_093
        ),
        lambda d: d["arithmetic"].__setitem__(
            "delta_3912_pair_incidence_margin", 459
        ),
        lambda d: d["upstream_certificates"][
            "equality_wall_residue_line_partition"
        ].__setitem__("payload_sha256", "0" * 64),
    ]
    passed = 0
    for mutate in mutations:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            validate(bad, schema)
        except Failure:
            passed += 1
        else:
            raise Failure("tamper accepted")
    need(passed == len(mutations), "tamper count")
    print(f"tamper-selftest: PASS {passed}/{len(mutations)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not (args.emit or args.check or args.tamper_selftest):
        parser.error("choose --emit, --check, or --tamper-selftest")
    try:
        if args.emit:
            emit()
        if args.check:
            validate(load(CERT_PATH), load(SCHEMA_PATH))
            cert = load(CERT_PATH)
            print(f"architecture: {cert['architecture_id']}")
            print(f"partition_sha256: {cert['partition_sha256']}")
            print(
                "locator_coefficient_rank_cap: "
                f"{cert['arithmetic']['locator_coefficient_rank_cap']}"
            )
            print(
                "first_feasible_pair_incidence_delta: "
                f"{cert['arithmetic']['first_feasible_pair_incidence_delta']}"
            )
            print(
                "generic_kernel_free_branch_cap: "
                f"{cert['arithmetic']['generic_kernel_free_branch_cap']}"
            )
            print(f"payload_sha256: {cert['payload_sha256']}")
            print("check: PASS")
        if args.tamper_selftest:
            tamper_selftest()
        return 0
    except (Failure, OSError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
