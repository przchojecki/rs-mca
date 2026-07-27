"""Verify the KoalaBear kernel/Kronecker/source normalization packet."""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1 as parent

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-equality-wall-kernel-kronecker-source-normalization-v1"
)
CERT_PATH = CERT_DIR / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_equality_wall_kernel_kronecker_source_normalization_v1.schema.json"
)

ARCH = parent.ARCH
PARTITION_DIGEST = parent.PARTITION_DIGEST
R = parent.R
M = parent.M
S = parent.S
E = parent.E
C = parent.C
DELTA_MIN = parent.INCIDENCE_FIRST_FEASIBLE_DELTA
DELTA_MAX = parent.DELTA_MAX
W_DIMENSION_CAP = parent.GRAPH_POLYNOMIAL_SPACE_DIMENSION_CAP
PUSHFORWARD_DEGREE_CAP = parent.PUSHFORWARD_MAX_SPLITTING_DEGREE
LOCATOR_RANK_CAP = parent.LOCATOR_COEFFICIENT_RANK_CAP
PAIR_SPACE_CAP = 17
MAX_DESCENT_DEPTH = DELTA_MAX // E

Failure = parent.Failure
need = parent.need
seal = parent.seal
dump = parent.dump
load = parent.load
file_digest = parent.file_digest

UPSTREAM_CERTIFICATES = {
    "fixed_domain_rank16_normalization": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-equality-wall-fixed-domain-rank16-normalization-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '706fc1aaef763890b3ffbfbba1f750fb926ad412f2f0c66515ead393fb3318b0'
        ),
    }
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_kernel_kronecker_source_normalization_v1.md"
    ),
]


def matrix_rank_mod(rows: list[list[int]], modulus: int) -> int:
    if not rows:
        return 0
    matrix = [[entry % modulus for entry in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                index
                for index in range(rank, row_count)
                if matrix[index][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, modulus)
        matrix[rank] = [
            entry * inverse % modulus for entry in matrix[rank]
        ]
        for index in range(row_count):
            if index == rank:
                continue
            factor = matrix[index][column] % modulus
            if not factor:
                continue
            matrix[index] = [
                (
                    matrix[index][offset]
                    - factor * matrix[rank][offset]
                )
                % modulus
                for offset in range(column_count)
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def kronecker_regression() -> dict[str, Any]:
    modulus = 101
    length = 11
    diagonal = list(range(1, length + 1))
    coordinate_indices = [0, 1]
    chain_lengths = [3, 2]
    generators = [
        [
            0 if index in coordinate_indices else 1
            for index in range(length)
        ],
        [
            (
                0
                if index in coordinate_indices
                else pow(index + 3, 4, modulus)
            )
            for index in range(length)
        ],
    ]

    rows: list[list[int]] = []
    for coordinate in coordinate_indices:
        row = [0] * length
        row[coordinate] = 1
        rows.append(row)
    for generator, chain_length in zip(
        generators, chain_lengths, strict=True
    ):
        for exponent in range(chain_length):
            rows.append(
                [
                    (
                        generator[index]
                        * pow(diagonal[index], exponent, modulus)
                    )
                    % modulus
                    for index in range(length)
                ]
            )

    translated = [
        [
            row[index] * diagonal[index] % modulus
            for index in range(length)
        ]
        for row in rows
    ]
    c_rank = matrix_rank_mod(rows, modulus)
    expansion_rank = matrix_rank_mod(rows + translated, modulus)
    predicted_rank = len(coordinate_indices) + sum(chain_lengths)
    predicted_expansion_rank = predicted_rank + len(chain_lengths)
    return {
        "field_modulus": modulus,
        "ambient_length": length,
        "coordinate_block_count": len(coordinate_indices),
        "left_singular_block_lengths": chain_lengths,
        "computed_C_rank": c_rank,
        "predicted_C_rank": predicted_rank,
        "computed_C_plus_CT_rank": expansion_rank,
        "predicted_C_plus_CT_rank": predicted_expansion_rank,
        "expansion_defect": expansion_rank - c_rank,
        "full_support": all(
            any(row[index] % modulus for row in rows)
            for index in range(length)
        ),
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


def low_excess_case(a: int) -> dict[str, int]:
    exceptional_cap = (
        PUSHFORWARD_DEGREE_CAP * (W_DIMENSION_CAP - 1) - a
    )
    regular_floor = M - exceptional_cap
    return {
        "kernel_line_degree": a,
        "exceptional_parameter_cap": exceptional_cap,
        "regular_selected_parameter_floor": regular_floor,
        "regular_floor_minus_polynomial_degree": regular_floor - a,
        "sufficient_regular_split_cap_for_total_68": 12 + a,
    }


def exact_arithmetic() -> dict[str, Any]:
    return {
        "source_size": S,
        "source_pencil_degree": E,
        "minimum_active_exchange": C,
        "target_packet_size": M,
        "normalized_excess_lower_bound": DELTA_MIN,
        "normalized_excess_upper_bound": DELTA_MAX,
        "graph_polynomial_space_dimension_cap": W_DIMENSION_CAP,
        "pushforward_maximum_splitting_degree": PUSHFORWARD_DEGREE_CAP,
        "locator_coefficient_rank_cap": LOCATOR_RANK_CAP,
        "locator_pair_space_dimension_cap": PAIR_SPACE_CAP,
        "maximum_source_zero_descent_depth": MAX_DESCENT_DEPTH,
        "low_excess_kernel_rank_cap": 1,
        "low_excess_kernel_line_degree_cap": (
            PUSHFORWARD_DEGREE_CAP * (W_DIMENSION_CAP - 1)
        ),
        "low_excess_cases": [
            low_excess_case(a) for a in (0, 1, 8, 56)
        ],
        "minimum_noncoordinate_records_after_coordinate_removal": (
            M - LOCATOR_RANK_CAP
        ),
        "maximum_single_chain_length": LOCATOR_RANK_CAP,
        "kronecker_regression": kronecker_regression(),
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
                "EQUALITY-WALL LINE AFTER FIXED-DOMAIN NORMALIZATION"
            ),
            "active_ledger": {
                "B_remaining": parent.parent.B_REMAINING,
                "additional_charge": 0,
                "first_open_slack": R,
            },
            "theorem": {
                "generic_kernel_is_a_saturated_vector_subbundle": True,
                "kernel_splits_as_nonpositive_line_bundles": True,
                "exceptional_fiber_count_at_most_q_times_m_minus_r_minus_A": (
                    True
                ),
                "source_zero_kernel_has_codimension_at_most_one": True,
                "source_zero_kernel_descends_by_exact_degree_e": True,
                "source_zero_descent_depth_at_most_six": True,
                "low_excess_positive_generic_kernel_has_rank_one": True,
                "low_excess_regular_selected_floor_is_13_plus_a": True,
                "low_excess_scroll_quotient_has_t_degree_at_most_a_minus_1": (
                    True
                ),
                "low_excess_monic_leading_coefficient_equals_source_scalar": (
                    True
                ),
                "low_excess_source_image_size_at_most_a": True,
                "small_expansion_pencil_has_no_right_singular_blocks": True,
                "regular_kronecker_part_is_coordinate_eigenlines": True,
                "remaining_kronecker_blocks_are_left_singular_chains": True,
                "kronecker_chain_count_equals_expansion_defect": True,
                "different_krylov_blocks_may_overlap_in_coordinate_support": (
                    True
                ),
                "one_chain_block_has_common_monic_normalizer": True,
                "one_chain_source_identity_is_polynomial": True,
                "one_chain_source_image_size_at_most_chain_length": True,
                "rank_one_split_scroll_counting_status": "OPEN",
                "line_cap_68_status": "OPEN",
                "additional_charge_status": "ZERO",
                "first_open_slack_after_packet": R,
            },
            "arithmetic": exact_arithmetic(),
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_SATURATED_KERNEL_EXCEPTIONAL_DIVISOR_"
                "SOURCE_ZERO_DEGREE_E_DESCENT_LOW_EXCESS_RANK_ONE_"
                "EXACT_COORDINATE_LEFT_KRONECKER_CLASSIFICATION_"
                "MONICITY_SOURCE_NORMALIZATION_"
                "RANK_ONE_SPLIT_SCROLL_COUNT_OPEN_R134943_UNCHANGED"
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
            "KoalaBear equality-wall kernel Kronecker source normalization"
        ),
        "type": "object",
    }


def check_note_anchors() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_kernel_kronecker_source_normalization_v1.md"
    ).read_text(encoding="utf-8")
    anchors = [
        "# KoalaBear equality-wall kernel, Kronecker, and source normalization",
        "\\mathcal K\\simeq",
        "|Z_{\\rm exc}|",
        "69-q(m-r)+A",
        "\\deg_XQ\\le\\delta-e",
        "\\boxed{r=1.}",
        "13+a",
        "\\lambda(t)=\\ell(t)",
        "|f(\\Sigma)|\\le a",
        "Exact Kronecker classification of locator expansion",
        "The supports of different",
        "\\operatorname{span}",
        "|f(\\Sigma)|\\le\\epsilon",
        "rank_one_split_scroll_counting_target.md",
        "# PROVED KERNEL/KRONECKER/SOURCE REDUCTION / SPLIT-SCROLL COUNT OPEN",
    ]
    for anchor in anchors:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from replay")
    need(schema == expected_schema(), "schema differs from replay")
    theorem = cert["theorem"]
    arithmetic = cert["arithmetic"]
    need(
        theorem["generic_kernel_is_a_saturated_vector_subbundle"],
        "kernel saturation",
    )
    need(
        theorem[
            "exceptional_fiber_count_at_most_q_times_m_minus_r_minus_A"
        ],
        "exceptional divisor",
    )
    need(
        theorem["source_zero_kernel_descends_by_exact_degree_e"],
        "source-zero descent",
    )
    need(
        theorem["low_excess_positive_generic_kernel_has_rank_one"],
        "low-excess rank one",
    )
    need(
        theorem[
            "low_excess_monic_leading_coefficient_equals_source_scalar"
        ],
        "monicity/source scalar",
    )
    need(
        theorem["remaining_kronecker_blocks_are_left_singular_chains"],
        "Kronecker chains",
    )
    need(
        theorem["different_krylov_blocks_may_overlap_in_coordinate_support"],
        "overlap guardrail",
    )
    need(
        theorem["rank_one_split_scroll_counting_status"] == "OPEN",
        "rank-one target remains open",
    )
    need(theorem["line_cap_68_status"] == "OPEN", "cap 68 remains open")
    need(
        arithmetic["maximum_source_zero_descent_depth"] == 6,
        "descent depth",
    )
    need(
        arithmetic["low_excess_kernel_line_degree_cap"] == 56,
        "kernel line degree",
    )
    cases = {
        row["kernel_line_degree"]: row
        for row in arithmetic["low_excess_cases"]
    }
    need(
        cases[0]["exceptional_parameter_cap"] == 56,
        "a=0 exceptional cap",
    )
    need(
        cases[0]["regular_selected_parameter_floor"] == 13,
        "a=0 regular floor",
    )
    need(
        cases[56]["exceptional_parameter_cap"] == 0,
        "a=56 exceptional cap",
    )
    need(
        cases[56]["regular_selected_parameter_floor"] == 69,
        "a=56 regular floor",
    )
    need(
        all(
            row["regular_floor_minus_polynomial_degree"] == 13
            for row in cases.values()
        ),
        "regular interpolation surplus",
    )
    regression = arithmetic["kronecker_regression"]
    need(regression["computed_C_rank"] == 7, "Kronecker C rank")
    need(
        regression["computed_C_plus_CT_rank"] == 9,
        "Kronecker expansion rank",
    )
    need(regression["expansion_defect"] == 2, "Kronecker defect")
    need(regression["full_support"], "Kronecker full support")
    need(
        arithmetic["minimum_noncoordinate_records_after_coordinate_removal"]
        == 53,
        "one-chain record floor",
    )
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
            "generic_kernel_is_a_saturated_vector_subbundle", False
        ),
        lambda d: d["theorem"].__setitem__(
            "exceptional_fiber_count_at_most_q_times_m_minus_r_minus_A",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "source_zero_kernel_descends_by_exact_degree_e", False
        ),
        lambda d: d["theorem"].__setitem__(
            "low_excess_positive_generic_kernel_has_rank_one", False
        ),
        lambda d: d["theorem"].__setitem__(
            "low_excess_regular_selected_floor_is_13_plus_a", False
        ),
        lambda d: d["theorem"].__setitem__(
            "low_excess_monic_leading_coefficient_equals_source_scalar",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "low_excess_source_image_size_at_most_a", False
        ),
        lambda d: d["theorem"].__setitem__(
            "small_expansion_pencil_has_no_right_singular_blocks", False
        ),
        lambda d: d["theorem"].__setitem__(
            "regular_kronecker_part_is_coordinate_eigenlines", False
        ),
        lambda d: d["theorem"].__setitem__(
            "remaining_kronecker_blocks_are_left_singular_chains", False
        ),
        lambda d: d["theorem"].__setitem__(
            "different_krylov_blocks_may_overlap_in_coordinate_support",
            False,
        ),
        lambda d: d["theorem"].__setitem__(
            "one_chain_source_identity_is_polynomial", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_one_split_scroll_counting_status", "PROVED"
        ),
        lambda d: d["theorem"].__setitem__("line_cap_68_status", "PROVED"),
        lambda d: d["arithmetic"].__setitem__(
            "maximum_source_zero_descent_depth", 7
        ),
        lambda d: d["arithmetic"].__setitem__(
            "low_excess_kernel_line_degree_cap", 57
        ),
        lambda d: d["arithmetic"]["low_excess_cases"][0].__setitem__(
            "regular_selected_parameter_floor", 12
        ),
        lambda d: d["arithmetic"]["kronecker_regression"].__setitem__(
            "computed_C_plus_CT_rank", 8
        ),
        lambda d: d["arithmetic"]["kronecker_regression"].__setitem__(
            "full_support", False
        ),
        lambda d: d["arithmetic"].__setitem__(
            "minimum_noncoordinate_records_after_coordinate_removal", 52
        ),
        lambda d: d["upstream_certificates"][
            "fixed_domain_rank16_normalization"
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
                "maximum_source_zero_descent_depth: "
                f"{cert['arithmetic']['maximum_source_zero_descent_depth']}"
            )
            print(
                "low_excess_kernel_line_degree_cap: "
                f"{cert['arithmetic']['low_excess_kernel_line_degree_cap']}"
            )
            print(
                "kronecker_regression_defect: "
                f"{cert['arithmetic']['kronecker_regression']['expansion_defect']}"
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
