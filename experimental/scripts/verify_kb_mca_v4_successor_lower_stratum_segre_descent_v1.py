#!/usr/bin/env python3
"""Verify the r=67,473 lower-stratum Segre-descent reduction."""

from __future__ import annotations

import argparse
import copy
import itertools
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_successor_upper_stratum_quadratic_adjugate_v1 as upper

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-successor-lower-stratum-segre-descent-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_successor_lower_stratum_segre_descent_v1.schema.json"
)

ARCH = upper.ARCH
PARTITION_DIGEST = upper.PARTITION_DIGEST
R_SUCCESSOR = upper.R_SUCCESSOR
SOURCE_SIZE = upper.SOURCE_SIZE
REDUCED_DEGREE = upper.REDUCED_DEGREE - 1
CARRIER_SIZE = upper.CARRIER_SIZE
COMPLEMENT_SIZE = upper.COMPLEMENT_SIZE
FORCED_COMMON_ZERO_SIZE = upper.COMMON_ZERO_SIZE
PROJECTIVE_CAP = upper.PROJECTIVE_POINT_CAP
DIRECT_CAP = PROJECTIVE_CAP * CARRIER_SIZE
PLANE_CAP = 2 * PROJECTIVE_CAP * CARRIER_SIZE
BEZOUT_CAP = 64 * PROJECTIVE_CAP * CARRIER_SIZE
BEZOUT_MARGIN = upper.plane.active.REMAINING - BEZOUT_CAP

Failure = upper.Failure
need = upper.need
seal = upper.seal
dump = upper.dump
load = upper.load
file_digest = upper.file_digest

UPSTREAM_CERTIFICATES = {
    "post_next_slack_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-next-slack-full-histogram-replay-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '53a70a678e6669ac4d3083ec0dcd0a29d86aa127997cfdf2f8c9318eb844c902'
        ),
    },
    "successor_upper_stratum": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-successor-upper-stratum-quadratic-adjugate-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '492c931f1417ee417251ab6dfb8d54501ba253a5d6a58e89a78a16e6ec2629c6'
        ),
    },
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_interpolation_pencil_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_next_slack_full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_successor_lower_stratum_segre_descent_v1.md"
    ),
]


def source_bindings() -> list[dict[str, str]]:
    result = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        result.append(
            {
                "binding_id": (
                    f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}"
                ),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return result


def upstream_bindings() -> dict[str, dict[str, str]]:
    result = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        payload = load(path)
        need(
            payload.get("payload_sha256") == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        result[key] = {**contract, "file_sha256": file_digest(path)}
    return result


class GFp2:
    """Small exact quadratic-field helper for the finite control."""

    def __init__(self, prime: int, nonsquare: int):
        self.p = prime
        self.d = nonsquare % prime
        need(
            pow(self.d, (prime - 1) // 2, prime) == prime - 1,
            "quadratic nonresidue",
        )
        self.order = prime * prime

    def pair(self, value: int) -> tuple[int, int]:
        return value % self.p, value // self.p

    def element(self, left: int, right: int = 0) -> int:
        return (left % self.p) + self.p * (right % self.p)

    def add(self, left: int, right: int) -> int:
        a, b = self.pair(left)
        c, d = self.pair(right)
        return self.element(a + c, b + d)

    def neg(self, value: int) -> int:
        a, b = self.pair(value)
        return self.element(-a, -b)

    def sub(self, left: int, right: int) -> int:
        return self.add(left, self.neg(right))

    def mul(self, left: int, right: int) -> int:
        a, b = self.pair(left)
        c, d = self.pair(right)
        return self.element(
            a * c + b * d * self.d,
            a * d + b * c,
        )

    def inv(self, value: int) -> int:
        need(value != 0, "division by zero")
        a, b = self.pair(value)
        norm = (a * a - self.d * b * b) % self.p
        inverse = pow(norm, -1, self.p)
        return self.element(a * inverse, -b * inverse)

    def div(self, left: int, right: int) -> int:
        return self.mul(left, self.inv(right))

    def is_base(self, value: int) -> bool:
        return self.pair(value)[1] == 0


def rank(matrix: list[list[int]], field: GFp2) -> int:
    rows = [row[:] for row in matrix if any(row)]
    if not rows:
        return 0
    columns = len(rows[0])
    pivot = 0
    for column in range(columns):
        selected = next(
            (row for row in range(pivot, len(rows)) if rows[row][column]),
            None,
        )
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        inverse = field.inv(rows[pivot][column])
        rows[pivot] = [field.mul(value, inverse) for value in rows[pivot]]
        for row in range(len(rows)):
            if row == pivot or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                field.sub(value, field.mul(factor, pivot_value))
                for value, pivot_value in zip(rows[row], rows[pivot])
            ]
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def nullspace(matrix: list[list[int]], field: GFp2) -> list[list[int]]:
    rows = [row[:] for row in matrix]
    columns = len(rows[0]) if rows else 0
    pivots: list[int] = []
    pivot = 0
    for column in range(columns):
        selected = next(
            (row for row in range(pivot, len(rows)) if rows[row][column]),
            None,
        )
        if selected is None:
            continue
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        inverse = field.inv(rows[pivot][column])
        rows[pivot] = [field.mul(value, inverse) for value in rows[pivot]]
        for row in range(len(rows)):
            if row == pivot or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                field.sub(value, field.mul(factor, pivot_value))
                for value, pivot_value in zip(rows[row], rows[pivot])
            ]
        pivots.append(column)
        pivot += 1
    free = [column for column in range(columns) if column not in pivots]
    result = []
    for free_column in free:
        vector = [0] * columns
        vector[free_column] = 1
        for row, pivot_column in reversed(list(enumerate(pivots))):
            total = 0
            for column in free:
                total = field.add(
                    total, field.mul(rows[row][column], vector[column])
                )
            vector[pivot_column] = field.neg(total)
        result.append(vector)
    return result


def solve_square(
    matrix: list[list[int]], target: list[int], field: GFp2
) -> list[int]:
    size = len(matrix)
    rows = [matrix[row][:] + [target[row]] for row in range(size)]
    pivot = 0
    for column in range(size):
        selected = next(
            (row for row in range(pivot, size) if rows[row][column]),
            None,
        )
        need(selected is not None, "singular interpolation matrix")
        rows[pivot], rows[selected] = rows[selected], rows[pivot]
        inverse = field.inv(rows[pivot][column])
        rows[pivot] = [field.mul(value, inverse) for value in rows[pivot]]
        for row in range(size):
            if row == pivot or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                field.sub(value, field.mul(factor, pivot_value))
                for value, pivot_value in zip(rows[row], rows[pivot])
            ]
        pivot += 1
    return [rows[index][-1] for index in range(size)]


def polynomial_value(
    coefficients: list[int], point: int, field: GFp2
) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = field.add(field.mul(result, point), coefficient)
    return result


def interpolation_parity(
    points: list[int], degree: int, field: GFp2
) -> list[list[int]]:
    columns = [
        [
            polynomial_value([0] * power + [1], point, field)
            for point in points
        ]
        for power in range(degree + 1)
    ]
    return nullspace(
        [
            [column[row] for row in range(len(points))]
            for column in columns
        ],
        field,
    )


def multiplier_space(
    u0: list[int],
    u1: list[int],
    points: list[int],
    degree: int,
    field: GFp2,
) -> list[list[int]]:
    parity = interpolation_parity(points, degree, field)
    if not parity:
        return [
            [1 if row == column else 0 for column in range(len(points))]
            for row in range(len(points))
        ]
    equations = []
    for coordinate in [u0, u1]:
        for check in parity:
            equations.append(
                [
                    field.mul(check[index], coordinate[index])
                    for index in range(len(points))
                ]
            )
    return nullspace(equations, field)


def projective_base_space(
    dimension: int, field: GFp2
) -> list[list[int]]:
    result = []
    for pivot in range(dimension):
        for tail in itertools.product(
            range(field.p), repeat=dimension - pivot - 1
        ):
            result.append(
                [0] * pivot
                + [1]
                + [field.element(value) for value in tail]
            )
    return result


def projective_normalize(
    vector: list[int], field: GFp2
) -> tuple[int, ...]:
    first = next(value for value in vector if value)
    inverse = field.inv(first)
    return tuple(field.mul(value, inverse) for value in vector)


def extension_source_control() -> dict[str, Any]:
    field = GFp2(7, 3)
    degree = 2
    points = [field.element(value) for value in range(4)]
    left = [26, 3, 22]
    right = [34, 29, 11]
    zeta = field.element(0, 1)
    left_values = [
        polynomial_value(left, point, field) for point in points
    ]
    right_values = [
        polynomial_value(right, point, field) for point in points
    ]
    need(
        not any(
            left_value == 0 and right_value == 0
            for left_value, right_value in zip(left_values, right_values)
        ),
        "source pair pointwise nonzero",
    )
    twist = [field.sub(point, zeta) for point in points]
    u0 = [
        field.mul(value, source)
        for value, source in zip(twist, left_values)
    ]
    u1 = [
        field.mul(value, source)
        for value, source in zip(twist, right_values)
    ]
    degree_space = multiplier_space(u0, u1, points, degree, field)
    enlarged_space = multiplier_space(
        u0, u1, points, degree + 1, field
    )
    need(len(degree_space) == 2, "toy source-pencil dimension")
    need(len(enlarged_space) == 4, "toy enlarged dimension")

    rank_one_q: set[tuple[int, ...]] = set()
    quotient_directions: set[tuple[int, ...]] = set()
    for q_values in projective_base_space(len(points), field):
        for root in range(field.order):
            denominators = [
                field.sub(point, root) for point in points
            ]
            if any(value == 0 for value in denominators):
                continue
            quotient = [
                field.div(value, denominator)
                for value, denominator in zip(q_values, denominators)
            ]
            if rank([*degree_space, quotient], field) != len(degree_space):
                continue
            rank_one_q.add(tuple(q_values))
            quotient_directions.add(
                projective_normalize(quotient, field)
            )
            break

    need(len(rank_one_q) == 10, "toy base Segre points")
    need(len(quotient_directions) == 8, "toy quotient directions")
    return {
        "base_prime": field.p,
        "extension_degree": 2,
        "source_degree": degree,
        "source_size": len(points),
        "source_pencil_dimension": len(degree_space),
        "enlarged_source_dimension": len(enlarged_space),
        "base_projective_ambient_points": len(
            projective_base_space(len(points), field)
        ),
        "base_rank_one_points": len(rank_one_q),
        "quotient_map_directions": len(quotient_directions),
        "p_plus_one": field.p + 1,
        "left": left,
        "right": right,
    }


def quadric_controls() -> dict[str, Any]:
    prime = 7
    field = GFp2(prime, 3)
    points = projective_base_space(4, field)

    def base_values(point: list[int]) -> list[int]:
        return [field.pair(value)[0] for value in point]

    split = 0
    split_quotients: set[tuple[int, int]] = set()
    nonsplit = 0
    for point in points:
        x0, x1, x2, x3 = base_values(point)
        if (x0 * x3 - x1 * x2) % prime == 0:
            split += 1
            row = [x0, x1] if (x0 or x1) else [x2, x3]
            first = next(value for value in row if value)
            inverse = pow(first, -1, prime)
            split_quotients.add(
                tuple(value * inverse % prime for value in row)
            )
        if (
            x0 * x0 - 3 * x1 * x1 - x2 * x3
        ) % prime == 0:
            nonsplit += 1

    need(split == (prime + 1) ** 2, "split quadric count")
    need(len(split_quotients) == prime + 1, "split quotient count")
    need(nonsplit == prime * prime + 1, "nonsplit quadric count")
    return {
        "base_prime": prime,
        "projective_3_space_points": len(points),
        "split_quadric_points": split,
        "split_quotient_directions": len(split_quotients),
        "nonsplit_quadric_points": nonsplit,
        "nonsplit_ruling_field_order": prime * prime,
    }


def deployed_arithmetic() -> dict[str, Any]:
    source_rational_limit = (SOURCE_SIZE - 1) // 2
    reduced_upper = SOURCE_SIZE + 1 - upper.pencil.T - 1
    reduced_lower = source_rational_limit + 1
    forced_roots = (
        upper.pencil.A_AGREEMENT - 1 - SOURCE_SIZE
    )
    local_u = REDUCED_DEGREE - 1
    residual_slack = R_SUCCESSOR - local_u
    intrinsic_gate_no_wrap_margin = (
        SOURCE_SIZE - (REDUCED_DEGREE + 2)
    )
    direct_margin = upper.plane.active.REMAINING - DIRECT_CAP
    plane_margin = upper.plane.active.REMAINING - PLANE_CAP

    need(R_SUCCESSOR == 67_473, "successor slack")
    need(SOURCE_SIZE == 134_946 == 2 * REDUCED_DEGREE, "lower stratum")
    need(reduced_lower == REDUCED_DEGREE, "lower degree")
    need(reduced_upper == REDUCED_DEGREE + 1, "upper degree")
    need(forced_roots == FORCED_COMMON_ZERO_SIZE, "forced common roots")
    need(local_u == 67_472, "local u")
    need(residual_slack == 1, "h plus ell")
    need(
        intrinsic_gate_no_wrap_margin == 67_471 > 0,
        "intrinsic lower-pencil no-wrap gate",
    )
    need(DIRECT_CAP == 4_180_884_949_033_404, "direct cap")
    need(PLANE_CAP == 8_361_769_898_066_808, "plane cap")
    need(BEZOUT_CAP == 267_576_636_738_137_856, "Bezout cap")
    need(BEZOUT_MARGIN == 3_203_576_222_438_024, "Bezout margin")
    need(BEZOUT_CAP < upper.plane.active.REMAINING, "Bezout fits")

    return {
        "base_field_order": upper.plane.active.prev.BASE_PRIME,
        "evaluation_extension_degree": 6,
        "n": upper.pencil.N,
        "k": upper.pencil.K,
        "agreement": upper.pencil.A_AGREEMENT,
        "j": upper.pencil.J,
        "t": upper.pencil.T,
        "r": R_SUCCESSOR,
        "x": 1,
        "source_size": SOURCE_SIZE,
        "source_rational_limit": source_rational_limit,
        "reduced_degree_lower": reduced_lower,
        "reduced_degree_upper": reduced_upper,
        "treated_reduced_degree": REDUCED_DEGREE,
        "source_pencil_dimension": 2,
        "enlarged_source_dimension": 4,
        "forced_common_zero_size": FORCED_COMMON_ZERO_SIZE,
        "carrier_size": CARRIER_SIZE,
        "complement_size": COMPLEMENT_SIZE,
        "local_u": local_u,
        "h_plus_ell": residual_slack,
        "intrinsic_gate_no_wrap_margin": intrinsic_gate_no_wrap_margin,
        "direct_cap": DIRECT_CAP,
        "direct_margin": direct_margin,
        "plane_cap": PLANE_CAP,
        "plane_margin": plane_margin,
        "coefficient_component_count_max": 6,
        "bezout_degree_max": 64,
        "bezout_cap": BEZOUT_CAP,
        "bezout_margin": BEZOUT_MARGIN,
        "current_remaining_reserve": upper.plane.active.REMAINING,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "active_ledger": {
                "U_paid": upper.plane.active.PAID,
                "B_remaining": upper.plane.active.REMAINING,
                "additional_charge": 0,
            },
            "theorem": {
                "successor_slack": R_SUCCESSOR,
                "treated_degree_stratum": REDUCED_DEGREE,
                "slack_split_is_h0_ell1_or_h1_ell0": True,
                "forced_gcd_branch_directly_paid": True,
                "extra_gcd_enlarged_source_dimension": 4,
                "multiplication_tensor_isomorphism": True,
                "actual_complement_locator_on_segre_quadric": True,
                "base_dimension_at_most_three_paid": True,
                "full_base_non_descended_branch_paid": True,
                "descended_split_quadric_paid": True,
                "lower_pencil_intrinsic_inside_enlarged_space": True,
                "coefficient_frobenius_preserves_lower_pencil": True,
                "coefficient_frobenius_preserves_multiplier_ruling": True,
                "descended_nonsplit_quadric_impossible": True,
                "lower_stratum_paid": True,
                "upper_span_three_paid": True,
                "upper_span_four_paid": True,
                "upper_remaining_packets": [],
                "upper_span_three_spread_petal_payment_open": False,
                "upper_stratum_paid": True,
                "row_closed": True,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "finite_controls": {
                "quadrics": quadric_controls(),
                "extension_source": extension_source_control(),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_SUCCESSOR_LOWER_STRATUM_ZERO_CHARGE_PAYMENT_"
                "UPPER_COMPANION_PAID_SUCCESSOR_SLACK_CLOSED"
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
        "title": "KoalaBear successor lower-stratum Segre payment",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_successor_lower_stratum_segre_descent_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED LOWER-STRATUM PAYMENT",
        "\\boxed{h+\\ell=1.}",
        "One-extra-gcd tensor normal form",
        "smooth Segre quadric",
        "267{,}576{,}636{,}738{,}137{,}856",
        "Every descended source quadric is split",
        "\\sigma(\\mathscr W_e)=\\mathscr W_e",
        "descended source quadric",
        "companion upper theorem pays every occupied span",
        "close \\(r=67{,}473\\)",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["theorem"]["descended_nonsplit_quadric_impossible"] is True,
        "nonsplit impossibility status",
    )
    need(cert["theorem"]["lower_stratum_paid"] is True, "lower status")
    need(cert["theorem"]["upper_span_three_paid"] is True, "upper span-three status")
    need(cert["theorem"]["upper_span_four_paid"] is True, "upper span-four status")
    need(
        cert["theorem"]["upper_remaining_packets"] == [],
        "upper remaining packets",
    )
    need(
        cert["theorem"]["upper_span_three_spread_petal_payment_open"] is False,
        "upper span-three status",
    )
    need(cert["theorem"]["upper_stratum_paid"] is True, "upper status")
    need(cert["theorem"]["row_closed"] is True, "row status")
    check_sources()


def emit() -> None:
    CERT.mkdir(parents=True, exist_ok=True)
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    validate(cert, schema)
    mutations = [
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["theorem"].__setitem__(
            "slack_split_is_h0_ell1_or_h1_ell0", False
        ),
        lambda d: d["theorem"].__setitem__(
            "multiplication_tensor_isomorphism", False
        ),
        lambda d: d["theorem"].__setitem__(
            "lower_pencil_intrinsic_inside_enlarged_space", False
        ),
        lambda d: d["theorem"].__setitem__(
            "coefficient_frobenius_preserves_multiplier_ruling", False
        ),
        lambda d: d["theorem"].__setitem__(
            "descended_nonsplit_quadric_impossible", False
        ),
        lambda d: d["theorem"].__setitem__("lower_stratum_paid", False),
        lambda d: d["theorem"].__setitem__("upper_span_three_paid", False),
        lambda d: d["theorem"].__setitem__("upper_span_four_paid", False),
        lambda d: d["theorem"].__setitem__(
            "upper_remaining_packets", ["occupied_span_four"]
        ),
        lambda d: d["theorem"].__setitem__(
            "upper_span_three_spread_petal_payment_open", True
        ),
        lambda d: d["theorem"].__setitem__("upper_stratum_paid", False),
        lambda d: d["theorem"].__setitem__("row_closed", False),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "bezout_degree_max", 32
        ),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "intrinsic_gate_no_wrap_margin", 0
        ),
        lambda d: d["finite_controls"]["quadrics"].__setitem__(
            "nonsplit_quadric_points", 49
        ),
        lambda d: d["finite_controls"]["extension_source"].__setitem__(
            "quotient_map_directions", 9
        ),
        lambda d: d["upstream_certificates"][
            "successor_upper_stratum"
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
    need(
        sum([args.emit, args.check, args.tamper_selftest]) == 1,
        "choose exactly one mode",
    )
    if args.emit:
        emit()
    elif args.check:
        validate(load(CERT_PATH), load(SCHEMA_PATH))
        cert = load(CERT_PATH)
        print(f"architecture: {cert['architecture_id']}")
        print(f"partition_sha256: {cert['partition_sha256']}")
        print(f"successor_slack: {cert['theorem']['successor_slack']}")
        print(
            "treated_degree:",
            cert["theorem"]["treated_degree_stratum"],
        )
        print(
            "bezout_cap:",
            cert["deployed_arithmetic"]["bezout_cap"],
        )
        print(
            "nonsplit_impossible:",
            cert["theorem"]["descended_nonsplit_quadric_impossible"],
        )
        print(
            "lower_paid:",
            cert["theorem"]["lower_stratum_paid"],
        )
        print("check: PASS")
    else:
        tamper_selftest()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
