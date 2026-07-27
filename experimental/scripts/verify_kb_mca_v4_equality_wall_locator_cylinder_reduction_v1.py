#!/usr/bin/env python3
"""Verify the KoalaBear equality-wall locator-cylinder reduction."""

from __future__ import annotations

import argparse
import copy
import itertools
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_first_gap_complement_locator_linearization_v1 as linear
import verify_kb_mca_v4_next_slack_source_plane_closure_v1 as plane
import verify_kb_mca_v4_reciprocal_kernel_plane_sweep_v1 as sweep

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-equality-wall-locator-cylinder-reduction-v1"
)
CERT_PATH = CERT_DIR / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_equality_wall_locator_cylinder_reduction_v1.schema.json"
)

ARCH = sweep.ARCH
PARTITION_DIGEST = sweep.PARTITION_DIGEST
R = 134_943
T = 67_472
N = 2_097_152
K = 1_048_576
A = 1_116_048
J = N - A
SOURCE_SIZE = T + R + 1
E = R + 1
C = 2 * E - SOURCE_SIZE
X = 1
H = R + X - E
CARRIER_SIZE = N - SOURCE_SIZE
LOCATOR_DEGREE = J + X
PER_LINE_CAP = J + 1
B_REMAINING = sweep.B_REMAINING
REQUIRED_LOCATOR_CAP = B_REMAINING // PER_LINE_CAP
LOCAL_LINE_CAP = 130
LOCAL_LINE_GLOBAL_CAP = 129 * sweep.P + LOCAL_LINE_CAP

Failure = sweep.Failure
need = sweep.need
seal = sweep.seal
dump = sweep.dump
load = sweep.load
file_digest = sweep.file_digest
residue = sweep.residue

UPSTREAM_CERTIFICATES = {
    "reciprocal_kernel_sweep": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-reciprocal-kernel-plane-sweep-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'dabd61e2242b5ec6ec5b19ce8966b8375cae5624091768b6c5cbc4dabdf4984c'
        ),
    },
    "post_sweep_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-reciprocal-kernel-plane-sweep-"
            "full-histogram-replay-v1/certificate.json"
        ),
        "payload_sha256": (
            'b6970ce42a1857654c2a4659a7ad918df1d38236618a017a39c62ba2e5b3f7e7'
        ),
    },
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_reciprocal_kernel_plane_sweep_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_reciprocal_kernel_plane_sweep_"
        "full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_outlier_basis_residue_transform_v1.md"
    ),
    (
        "experimental/notes/thresholds/"
        "split_locator_star_flat_intersection.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_locator_cylinder_reduction_v1.md"
    ),
]


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


def pad(poly: list[int], length: int) -> list[int]:
    return poly + [0] * (length - len(poly))


def add_poly(left: list[int], right: list[int], prime: int) -> list[int]:
    return sweep.add_poly(left, right, prime)


def scale_poly(poly: list[int], scalar: int, prime: int) -> list[int]:
    return residue.trim([scalar * coefficient % prime for coefficient in poly])


def determinant_three(
    matrix: list[list[list[int]]], prime: int
) -> list[int]:
    result = [0]
    for permutation in itertools.permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j]
            for i in range(3)
            for j in range(i + 1, 3)
        )
        term = [1]
        for row, column in enumerate(permutation):
            term = residue.mul(term, matrix[row][column], prime)
        if inversions % 2:
            term = scale_poly(term, -1, prime)
        result = add_poly(result, term, prime)
    return residue.trim(result)


def minor_two(
    matrix: list[list[list[int]]],
    row_a: int,
    row_b: int,
    col_a: int,
    col_b: int,
    prime: int,
) -> list[int]:
    return sweep.sub_poly(
        residue.mul(
            matrix[row_a][col_a], matrix[row_b][col_b], prime
        ),
        residue.mul(
            matrix[row_a][col_b], matrix[row_b][col_a], prime
        ),
        prime,
    )


def adjugate(
    matrix: list[list[list[int]]], prime: int
) -> list[list[list[int]]]:
    result: list[list[list[int]]] = [
        [[0] for _ in range(3)] for _ in range(3)
    ]
    for row in range(3):
        for column in range(3):
            remaining_rows = [index for index in range(3) if index != column]
            remaining_columns = [index for index in range(3) if index != row]
            value = minor_two(
                matrix,
                remaining_rows[0],
                remaining_rows[1],
                remaining_columns[0],
                remaining_columns[1],
                prime,
            )
            if (row + column) % 2:
                value = scale_poly(value, -1, prime)
            result[row][column] = value
    return result


def row_times_matrix(
    row: list[list[int]],
    matrix: list[list[list[int]]],
    prime: int,
) -> list[list[int]]:
    return [
        residue.trim(
            sum_polys(
                [
                    residue.mul(row[index], matrix[index][column], prime)
                    for index in range(3)
                ],
                prime,
            )
        )
        for column in range(3)
    ]


def sum_polys(polys: list[list[int]], prime: int) -> list[int]:
    total = [0]
    for poly in polys:
        total = add_poly(total, poly, prime)
    return residue.trim(total)


def constant_row_times_matrix(
    row: list[int],
    matrix: list[list[list[int]]],
    prime: int,
) -> list[list[int]]:
    return [
        sum_polys(
            [
                scale_poly(matrix[index][column], row[index], prime)
                for index in range(3)
            ],
            prime,
        )
        for column in range(3)
    ]


def independent_indices(
    vectors: list[list[int]], prime: int
) -> list[int]:
    basis: list[list[int]] = []
    indices: list[int] = []
    for index, vector in enumerate(vectors):
        if residue.rank([*basis, vector], prime) > len(basis):
            basis.append(vector)
            indices.append(index)
    return indices


def normalize_projective(
    vector: list[int], prime: int
) -> tuple[int, ...]:
    for entry in vector:
        if entry % prime:
            inverse = pow(entry, -1, prime)
            return tuple(value * inverse % prime for value in vector)
    raise Failure("zero projective vector")


def maximum_weighted_projective_line(
    vectors: list[list[int]], prime: int
) -> int:
    weights = Counter(
        normalize_projective(vector, prime) for vector in vectors
    )
    representatives = [list(point) for point in weights]
    maximum = max(weights.values(), default=0)
    for first, second in itertools.combinations(representatives, 2):
        if residue.rank([first, second], prime) != 2:
            continue
        occupancy = sum(
            weight
            for point, weight in weights.items()
            if residue.rank([first, second, list(point)], prime) <= 2
        )
        maximum = max(maximum, occupancy)
    return maximum


def exact_arithmetic() -> dict[str, Any]:
    need(SOURCE_SIZE == 202_416, "source size")
    need(E == 134_944, "equality degree")
    need(C == 67_472, "equality c")
    need(H == 0, "extra gcd degree")
    need(E == 2 * C, "e=2c")
    need(SOURCE_SIZE == 3 * C, "s=3c")
    need(3 * E == 2 * SOURCE_SIZE, "three-minor equality")
    need(E + C == SOURCE_SIZE, "relation-product equality")
    need(CARRIER_SIZE == 1_894_736, "carrier size")
    need(LOCATOR_DEGREE == 981_105, "locator degree")
    cylinder_dimension = LOCATOR_DEGREE - SOURCE_SIZE + 3
    need(cylinder_dimension == 778_692, "cylinder dimension")
    direct_cap = (sweep.P + 1) * CARRIER_SIZE
    need(direct_cap == 4_037_126_185_931_424, "direct cap")
    need(
        B_REMAINING - direct_cap == 266_743_086_774_644_456,
        "direct margin",
    )
    need(REQUIRED_LOCATOR_CAP == 275_995_141_152, "locator cap")
    locator_product = REQUIRED_LOCATOR_CAP * PER_LINE_CAP
    need(locator_product == 270_780_212_959_932_960, "floor product")
    need(B_REMAINING - locator_product == 642_920, "floor remainder")
    need(
        (REQUIRED_LOCATOR_CAP + 1) * PER_LINE_CAP
        > B_REMAINING,
        "locator cap maximality",
    )
    need(
        LOCAL_LINE_GLOBAL_CAP == 274_861_129_987,
        "line-cap global locator count",
    )
    line_cap_locator_margin = (
        REQUIRED_LOCATOR_CAP - LOCAL_LINE_GLOBAL_CAP
    )
    need(
        line_cap_locator_margin == 1_134_011_165,
        "line-cap locator margin",
    )
    line_cap_slope_charge = LOCAL_LINE_GLOBAL_CAP * PER_LINE_CAP
    need(
        line_cap_slope_charge == 269_667_628_935_895_635,
        "line-cap slope charge",
    )
    need(
        B_REMAINING - line_cap_slope_charge
        == 1_112_584_024_680_245,
        "line-cap reserve margin",
    )
    return {
        "r": R,
        "x": X,
        "source_size": SOURCE_SIZE,
        "e": E,
        "c": C,
        "extra_gcd_degree": H,
        "carrier_size": CARRIER_SIZE,
        "locator_degree": LOCATOR_DEGREE,
        "per_line_cap": PER_LINE_CAP,
        "cylinder_projective_dimension": cylinder_dimension,
        "direct_rank_at_most_two_cap": direct_cap,
        "direct_cap_reserve_margin": B_REMAINING - direct_cap,
        "required_locator_incidence_cap": REQUIRED_LOCATOR_CAP,
        "incidence_cap_times_per_line": locator_product,
        "incidence_cap_floor_remainder": B_REMAINING - locator_product,
        "sufficient_local_projective_line_cap": LOCAL_LINE_CAP,
        "line_cap_implied_locator_count": LOCAL_LINE_GLOBAL_CAP,
        "line_cap_locator_margin": line_cap_locator_margin,
        "line_cap_implied_slope_charge": line_cap_slope_charge,
        "line_cap_reserve_margin": B_REMAINING - line_cap_slope_charge,
    }


def strict_substrata() -> dict[str, Any]:
    e_min = (SOURCE_SIZE + 1) // 2
    x_min = e_min - R
    # At fixed x, the admissible degrees are
    #   e_min, ..., R+x,
    # so the stratum counts are exactly 1, 2, ..., 2-x_min.  Moreover
    # e-2c = 2*SOURCE_SIZE-3e depends only on e.  Its unique zero is
    # e=E, which can occur only at x=1; every other stratum is strict.
    x_count = 2 - x_min
    total_count = x_count * (x_count + 1) // 2
    count = total_count - 1
    maximum_strict_e = E - 1
    minimum_margin = 2 * SOURCE_SIZE - 3 * maximum_strict_e
    equality_records = [
        {
            "x": X,
            "e": E,
            "c": C,
            "h": H,
            "margin": E - 2 * C,
        }
    ]
    need(e_min == 101_208, "minimum equality-wall degree")
    need(x_min == -33_735, "minimum scalar offset")
    need(maximum_strict_e == E - 1, "strict degree endpoint")
    need(minimum_margin == 3, "strict minimum margin")
    need(
        equality_records
        == [{"x": 1, "e": E, "c": C, "h": 0, "margin": 0}],
        "unique equality record",
    )
    return {
        "x_min": x_min,
        "degree_min": e_min,
        "total_stratum_count": total_count,
        "strict_stratum_count": count,
        "maximum_strict_degree": maximum_strict_e,
        "minimum_strict_margin": minimum_margin,
        "equality_records": equality_records,
    }


def locator_cylinder_route_cut() -> dict[str, Any]:
    prime = 19
    source = list(range(6))
    source_locator = residue.locator(source, prime)
    _, inverse = plane.evaluation_inverse(prime, len(source))
    locator_sets = [
        [6, 7, 8, 9, 10, 11, 12, 13],
        [6, 7, 8, 9, 10, 11, 14, 16],
        [6, 7, 8, 9, 10, 11, 15, 17],
        [6, 7, 8, 12, 13, 14, 16, 17],
        [6, 7, 9, 10, 13, 14, 15, 16],
    ]
    reciprocal_columns = [
        [2, 5, 8, 1],
        [15, 15, 15, 0, 1],
        [4, 0, 0, 0, 0, 1],
    ]
    locators = [residue.locator(points, prime) for points in locator_sets]
    need(all(len(locator) - 1 == 8 for locator in locators), "locator degree")
    locator_rank = residue.rank(locators, prime)
    need(locator_rank == 4, "polynomial locator span")

    locator_values = [
        plane.polynomial_values(locator, source, prime)
        for locator in locators
    ]
    locator_residues = [
        pad(residue.matrix_vector(inverse, values, prime), len(source))
        for values in locator_values
    ]
    residue_rank = residue.rank(locator_residues, prime)
    need(residue_rank == 3, "locator residue span")
    maximum_line_occupancy = maximum_weighted_projective_line(
        locator_residues, prime
    )
    need(maximum_line_occupancy == 3, "projective-line occupancy")

    reciprocal_values = [
        plane.polynomial_values(column, source, prime)
        for column in reciprocal_columns
    ]
    product_rows = [
        [
            residue.trim(
                residue.matrix_vector(
                    inverse,
                    [
                        q_value * reciprocal_value % prime
                        for q_value, reciprocal_value in zip(
                            q_values, column_values
                        )
                    ],
                    prime,
                )
            )
            for column_values in reciprocal_values
        ]
        for q_values in locator_values
    ]
    need(
        all(
            len(product) - 1 <= 4
            for row in product_rows
            for product in row
        ),
        "degree-four admission",
    )
    need(
        any(
            max(len(row[0]), len(row[1])) - 1 == 4
            and residue.gcd_poly(row[0], row[1], prime) == [1]
            for row in product_rows
        ),
        "missing coprime exact-degree row",
    )

    basis_indices = independent_indices(locator_residues, prime)[:3]
    need(len(basis_indices) == 3, "missing residue basis")
    reciprocal_dimension = plane.reciprocal_dimension(
        [locator_residues[index] for index in basis_indices],
        source,
        inverse,
        4,
        prime,
    )
    need(
        reciprocal_dimension == 3,
        "complete reciprocal space does not collapse to dimension three",
    )
    product_basis = [product_rows[index] for index in basis_indices]
    determinant = determinant_three(product_basis, prime)
    quotient, remainder = residue.divmod_poly(
        determinant,
        residue.mul(source_locator, source_locator, prime),
        prime,
    )
    need(remainder == [0], "determinant lacks double source zero")
    need(len(quotient) == 1 and quotient[0] != 0, "nonconstant determinant residue")
    kappa = quotient[0]

    adj = adjugate(product_basis, prime)
    q_matrix: list[list[list[int]]] = [
        [[0] for _ in range(3)] for _ in range(3)
    ]
    for row in range(3):
        for column in range(3):
            quotient_entry, remainder_entry = residue.divmod_poly(
                adj[row][column], source_locator, prime
            )
            need(remainder_entry == [0], "adjugate entry not source-divisible")
            need(len(quotient_entry) - 1 <= 2, "adjugate quotient degree")
            q_matrix[row][column] = quotient_entry

    constant_reconstructions = []
    for row_index, row in enumerate(product_rows):
        multiplied = row_times_matrix(row, q_matrix, prime)
        constants = []
        for coordinate in multiplied:
            quotient_coordinate, remainder_coordinate = residue.divmod_poly(
                coordinate, source_locator, prime
            )
            need(
                remainder_coordinate == [0],
                "replacement minor lacks second source factor",
            )
            need(
                len(quotient_coordinate) <= 1,
                "nonconstant adjugate reconstruction",
            )
            constants.append(
                quotient_coordinate[0] if quotient_coordinate else 0
            )
        reconstructed = constant_row_times_matrix(
            constants, product_basis, prime
        )
        need(
            reconstructed
            == [scale_poly(entry, kappa, prime) for entry in row],
            "adjugate row reconstruction",
        )
        coefficient_row = [
            constant * pow(kappa, -1, prime) % prime
            for constant in constants
        ]
        reconstructed_residue = [
            sum(
                coefficient_row[index]
                * locator_residues[basis_indices[index]][coordinate]
                for index in range(3)
            )
            % prime
            for coordinate in range(len(source))
        ]
        need(
            reconstructed_residue == locator_residues[row_index],
            "residue reconstruction",
        )
        constant_reconstructions.append(coefficient_row)

    need(
        residue.rank(constant_reconstructions, prime) == 3,
        "reconstruction coordinate rank",
    )
    return {
        "prime": prime,
        "source_size": len(source),
        "source_degree": 4,
        "carrier_size": 12,
        "locator_degree": 8,
        "admitted_locator_count": len(locators),
        "locator_polynomial_span_dimension": locator_rank,
        "locator_residue_span_dimension": residue_rank,
        "maximum_weighted_projective_line_occupancy": (
            maximum_line_occupancy
        ),
        "reciprocal_dimension_used": len(reciprocal_columns),
        "complete_reciprocal_dimension": reciprocal_dimension,
        "product_rank": 3,
        "determinant_quotient": kappa,
        "adjugate_quotient_degree": 2,
        "constant_reconstruction_count": len(constant_reconstructions),
        "basis_indices": basis_indices,
        "locator_sets": locator_sets,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": (
                "SCALAR-UNPAID FULL-OUTSIDE SELECTED FINITE SLOPES "
                "AT THE FIRST RECIPROCAL EQUALITY WALL"
            ),
            "active_ledger": {
                "U_paid": sweep.upper.plane.active.PAID,
                "B_remaining": B_REMAINING,
                "additional_charge": 0,
                "first_open_slack": R,
            },
            "theorem": {
                "strict_substrata_paid_by_upstream_sweep": True,
                "unique_equality_stratum_is_x1_e134944": True,
                "complete_reciprocal_rank_at_most_two_is_directly_paid": True,
                "rank_three_minor_is_kappa_times_source_locator_squared": True,
                "rank_three_adjugate_reconstruction_is_constant": True,
                "rank_three_forces_occupied_residue_dimension_three": True,
                "rank_three_forces_complete_reciprocal_dimension_three": True,
                "actual_locators_form_a_residue_cylinder": True,
                "residue_plane_is_not_a_polynomial_plane": True,
                "uniform_weighted_line_cap_130_implies_payment": True,
                "rank_three_cylinder_incidence_cap_status": "OPEN",
                "first_open_slack_after_packet": R,
            },
            "arithmetic": exact_arithmetic(),
            "strict_substrata": strict_substrata(),
            "regressions": {
                "locator_cylinder_route_cut": locator_cylinder_route_cut(),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_EQUALITY_WALL_RANK_REDUCTION_"
                "R134943_REMAINS_OPEN_ON_RESIDUE_PLANE_LOCATOR_INCIDENCE"
            ),
        }
    )


def expected_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": True,
        "properties": {
            "architecture_id": {"const": ARCH},
            "partition_sha256": {"const": PARTITION_DIGEST},
            "payload_sha256": {"pattern": "^[0-9a-f]{64}$", "type": "string"},
        },
        "required": ["architecture_id", "partition_sha256", "payload_sha256"],
        "title": "KoalaBear equality-wall locator-cylinder reduction",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_equality_wall_locator_cylinder_reduction_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED_REDUCTION_ROW_OPEN",
        "Equality-wall reciprocal rank dichotomy",
        "\\det\\mathcal P=\\kappa\\Lambda_\\Sigma^2",
        "\\boxed{b=3.}",
        "\\boxed{\\dim_B\\mathcal R_b=3.}",
        "d_{\\rm cyl}=J-s+3=778{,}692",
        "275{,}995{,}141{,}152",
        "residue dimension three is not polynomial dimension three",
        "M_\\ell\\le130",
        "274{,}861{,}129{,}987",
        "# PROVED REDUCTION / ROW OPEN",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["theorem"]["rank_three_cylinder_incidence_cap_status"] == "OPEN",
        "open incidence status",
    )
    need(
        cert["theorem"]["first_open_slack_after_packet"] == R,
        "first open unchanged",
    )
    need(
        cert["regressions"]["locator_cylinder_route_cut"][
            "locator_polynomial_span_dimension"
        ]
        > cert["regressions"]["locator_cylinder_route_cut"][
            "locator_residue_span_dimension"
        ],
        "route-cut inequality",
    )
    need(
        cert["regressions"]["locator_cylinder_route_cut"][
            "complete_reciprocal_dimension"
        ]
        == 3,
        "complete reciprocal dimension",
    )
    check_sources()


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
            "unique_equality_stratum_is_x1_e134944", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_three_adjugate_reconstruction_is_constant", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_three_forces_occupied_residue_dimension_three", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_three_forces_complete_reciprocal_dimension_three", False
        ),
        lambda d: d["theorem"].__setitem__(
            "rank_three_cylinder_incidence_cap_status", "PROVED"
        ),
        lambda d: d["arithmetic"].__setitem__(
            "required_locator_incidence_cap", REQUIRED_LOCATOR_CAP + 1
        ),
        lambda d: d["arithmetic"].__setitem__(
            "sufficient_local_projective_line_cap", LOCAL_LINE_CAP + 1
        ),
        lambda d: d["strict_substrata"].__setitem__(
            "maximum_strict_degree", E
        ),
        lambda d: d["regressions"]["locator_cylinder_route_cut"].__setitem__(
            "locator_polynomial_span_dimension", 3
        ),
        lambda d: d["upstream_certificates"][
            "reciprocal_kernel_sweep"
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
    try:
        if args.emit:
            emit()
        if args.check:
            cert = load(CERT_PATH)
            schema = load(SCHEMA_PATH)
            validate(cert, schema)
            arithmetic = cert["arithmetic"]
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {PARTITION_DIGEST}")
            print(f"equality_slack: {R}")
            print(
                "rank_at_most_two_cap: "
                f"{arithmetic['direct_rank_at_most_two_cap']}"
            )
            print(
                "required_locator_incidence_cap: "
                f"{arithmetic['required_locator_incidence_cap']}"
            )
            print(
                "cylinder_projective_dimension: "
                f"{arithmetic['cylinder_projective_dimension']}"
            )
            print(f"payload_sha256: {cert['payload_sha256']}")
            print("check: PASS")
        if args.tamper_selftest:
            tamper_selftest()
        if not (args.emit or args.check or args.tamper_selftest):
            parser.error("choose --emit, --check, or --tamper-selftest")
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
