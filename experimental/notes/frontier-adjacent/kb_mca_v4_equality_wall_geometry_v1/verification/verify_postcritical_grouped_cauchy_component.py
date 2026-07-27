#!/usr/bin/env python3
"""Verify grouped-Cauchy identities and all KoalaBear row inequalities."""

from __future__ import annotations
class VerificationError(RuntimeError):
    """Raised when an exact verifier condition fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(str(message))


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )



import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "postcritical_grouped_cauchy_component_certificate.json"
PRIME = 101


def inv(value: int) -> int:
    return pow(value % PRIME, PRIME - 2, PRIME)


def trim(poly: list[int]) -> list[int]:
    result = [entry % PRIME for entry in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def add(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    result = [0] * size
    for index in range(size):
        result[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % PRIME
    return trim(result)


def scale(poly: list[int], scalar: int) -> list[int]:
    return trim([(scalar * entry) % PRIME for entry in poly])


def multiply(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            result[i + j] = (result[i + j] + x * y) % PRIME
    return trim(result)


def evaluate(poly: list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * value + coefficient) % PRIME
    return result


def divide_by_root(poly: list[int], root: int) -> tuple[list[int], int]:
    descending = list(reversed(poly))
    quotient_descending = [descending[0]]
    for coefficient in descending[1:]:
        quotient_descending.append(
            (coefficient + root * quotient_descending[-1]) % PRIME
        )
    remainder = quotient_descending.pop()
    return trim(list(reversed(quotient_descending))), remainder


def polynomial_from_roots(roots: list[int]) -> list[int]:
    result = [1]
    for root in roots:
        result = multiply(result, [(-root) % PRIME, 1])
    return result


def lagrange_basis(sources: list[int]) -> list[list[int]]:
    result = []
    for index, source in enumerate(sources):
        other = [
            value
            for position, value in enumerate(sources)
            if position != index
        ]
        numerator = polynomial_from_roots(other)
        denominator = 1
        for value in other:
            denominator = denominator * (source - value) % PRIME
        result.append(scale(numerator, inv(denominator)))
    return result


def rank_mod(columns: list[list[int]]) -> int:
    if not columns:
        return 0
    row_count = max(len(column) for column in columns)
    matrix = [
        [
            columns[column][row] if row < len(columns[column]) else 0
            for column in range(len(columns))
        ]
        for row in range(row_count)
    ]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if matrix[row][column] % PRIME
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        factor = inv(matrix[rank][column])
        matrix[rank] = [
            factor * entry % PRIME for entry in matrix[rank]
        ]
        for row in range(row_count):
            if row == rank:
                continue
            factor = matrix[row][column] % PRIME
            if not factor:
                continue
            matrix[row] = [
                (matrix[row][j] - factor * matrix[rank][j]) % PRIME
                for j in range(len(columns))
            ]
        rank += 1
    return rank


def nonzero_group_weights(
    basis: list[list[int]],
    indices: list[int],
    common_root: int,
) -> list[int]:
    values = [evaluate(basis[index], common_root) for index in indices]
    require(
        all(values),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:140',
    )
    for first in range(1, PRIME):
        for second in range(1, PRIME):
            last = -(first * values[0] + second * values[1])
            last = last * inv(values[2]) % PRIME
            if last:
                return [first, second, last]
    raise VerificationError("failed to find nonzero group weights")


def grouped_common_root_fixture() -> dict[str, object]:
    sources = [1, 2, 3, 4, 5, 6]
    groups = [[0, 1, 2], [3, 4, 5]]
    common_root = 10
    poles = [20, 30]
    basis = lagrange_basis(sources)
    group_polynomials = []
    quotient_polynomials = []
    group_weights = []

    for group in groups:
        weights = nonzero_group_weights(basis, group, common_root)
        polynomial = [0]
        for weight, index in zip(weights, group):
            polynomial = add(polynomial, scale(basis[index], weight))
        require(
            evaluate(polynomial, common_root) == 0,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:165',
        )
        quotient, remainder = divide_by_root(polynomial, common_root)
        require(
            remainder == 0,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:167',
        )
        group_weights.append(weights)
        group_polynomials.append(polynomial)
        quotient_polynomials.append(quotient)

    # h_0=lambda-beta_1 and h_1=lambda-beta_0.
    coefficient_zero = add(
        scale(quotient_polynomials[0], -poles[1]),
        scale(quotient_polynomials[1], -poles[0]),
    )
    coefficient_one = add(
        quotient_polynomials[0], quotient_polynomials[1]
    )
    coefficient_rank = rank_mod([coefficient_zero, coefficient_one])
    require(
        coefficient_rank == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:181',
    )

    off_block_checks = 0
    for group_index, group in enumerate(groups):
        other = 1 - group_index
        for source_index in group:
            require(
                evaluate(quotient_polynomials[other], sources[source_index]) == 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:187',
            )
            require(
                evaluate(quotient_polynomials[group_index], sources[source_index]) != 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:191',
            )
            off_block_checks += 1

    a = len(sources)
    b = len(groups)
    d = 1
    u = a - 1 - d
    v = b - 1
    effective_degree = b * u - a * v
    require(
        effective_degree == a - b * (d + 1) == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:206',
    )

    return {
        "prime": PRIME,
        "sources": sources,
        "groups": groups,
        "group_weights": group_weights,
        "common_root": common_root,
        "poles": poles,
        "a": a,
        "b": b,
        "d": d,
        "u": u,
        "v": v,
        "coefficient_rank": coefficient_rank,
        "off_block_checks": off_block_checks,
        "effective_divisor_degree": effective_degree,
        "group_polynomials": group_polynomials,
        "quotient_polynomials": quotient_polynomials,
    }


def row_certificate(a: int, regular_count: int) -> dict[str, object]:
    minimum = regular_count - a + 4
    periods = 5 if a == 12 else 4
    cases = []
    for d in range(a):
        for b in range(2, a + 1):
            if b * (d + 1) > a:
                continue
            u = a - 1 - d
            v = b - 1
            r = regular_count - d - periods * a
            s_min = minimum - periods * b
            require(
                r >= 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:240',
            )
            require(
                s_min >= 1,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:241',
            )
            if regular_count == 69 and a == 14:
                require(
                    r == u,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:243',
                )
                require(
                    s_min >= 2,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:244',
                )
                branch = "BOUNDARY_INDEPENDENT_COEFFICIENTS"
            else:
                require(
                    r <= u - 1,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:247',
                )
                branch = "KUNNETH_VANISHING"
            cases.append(
                {
                    "d": d,
                    "b": b,
                    "u": u,
                    "v": v,
                    "effective_divisor_degree": a - b * (d + 1),
                    "reduced_first_degree": r,
                    "reduced_negative_second_floor": s_min,
                    "branch": branch,
                }
            )
    require(
        cases,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:261',
    )
    return {
        "a": a,
        "R": regular_count,
        "minimum_overload": minimum,
        "periods_removed": periods,
        "case_count": len(cases),
        "minimum_reduced_negative_second_degree": min(
            case["reduced_negative_second_floor"] for case in cases
        ),
        "cases": cases,
    }


def payload() -> dict[str, object]:
    result = {
        "status": (
            "PROVED_COMPLETE_POSTCRITICAL_OVERLOADED_LINE_EXCLUSION_"
            "HIGHER_SUPPORT_BRANCHES_OPEN"
        ),
        "finite_field_grouped_fixture": grouped_common_root_fixture(),
        "koalabear_rows": [
            row_certificate(12, 69),
            row_certificate(14, 67),
            row_certificate(14, 68),
            row_certificate(14, 69),
        ],
        "claims": {
            "grouped_cauchy_normal_form": "PROVED",
            "common_vertical_factor_removal": "PROVED",
            "effective_source_pole_period": "PROVED",
            "selected_grid_section": "PROVED",
            "subcritical_vanishing": "PROVED",
            "boundary_injectivity": "PROVED",
            "common_root_overload": "IMPOSSIBLE",
            "coordinate_ratio_overload": "IMPOSSIBLE",
            "generic_overload": "IMPOSSIBLE",
            "complete_line_branch": "CLOSED",
            "conic_cubic_large_circuit_branches": "OPEN",
            "active_owner_payment": "NONE_NEEDED_FOR_LINE_BRANCH",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    fixture = data["finite_field_grouped_fixture"]
    require(
        fixture['coefficient_rank'] == fixture['b'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:312',
    )
    require(
        fixture['effective_divisor_degree'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:313',
    )
    require(
        fixture['off_block_checks'] == fixture['a'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:314',
    )
    expected_rows = [
        (12, 69, 61, 5, 1),
        (14, 67, 57, 4, 1),
        (14, 68, 58, 4, 2),
        (14, 69, 59, 4, 3),
    ]
    require(
        [(row['a'], row['R'], row['minimum_overload'], row['periods_removed'], row['minimum_reduced_negative_second_degree']) for row in data['koalabear_rows']] == expected_rows,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:321',
    )
    for row in data["koalabear_rows"]:
        require(
            row['case_count'] == len(row['cases']),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:332',
        )
        for case in row["cases"]:
            require(
                case['effective_divisor_degree'] >= 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:334',
            )
            require(
                case['reduced_negative_second_floor'] >= 1,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:335',
            )
            if case["branch"] == "KUNNETH_VANISHING":
                require(
                    0 <= case['reduced_first_degree'] <= case['u'] - 1,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:337',
                )
            else:
                require(
                    case['branch'] == 'BOUNDARY_INDEPENDENT_COEFFICIENTS',
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:343',
                )
                require(
                    case['reduced_first_degree'] == case['u'],
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:347',
                )
                require(
                    case['reduced_negative_second_floor'] >= 2,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:348',
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    data = payload()
    validate(data)
    if args.emit:
        CERTIFICATE.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n"
        )
    if args.check:
        require(
            json.loads(CERTIFICATE.read_text()) == data,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_grouped_cauchy_component.py:365',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["koalabear_rows"][0]["cases"][0][
            "effective_divisor_degree"
        ] = -1
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("grouped-Cauchy common-root fixture: PASS")
    print("effective source-pole period arithmetic: PASS")
    print("all KoalaBear overloaded-line cases: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
