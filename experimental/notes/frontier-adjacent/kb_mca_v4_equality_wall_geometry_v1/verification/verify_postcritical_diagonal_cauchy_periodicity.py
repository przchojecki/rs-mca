#!/usr/bin/env python3
"""Verify arithmetic and finite linear algebra for the periodicity reduction."""

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
CERTIFICATE = (
    ROOT / "postcritical_diagonal_cauchy_periodicity_certificate.json"
)
PRIME = 101


def inverse(value: int) -> int:
    return pow(value % PRIME, PRIME - 2, PRIME)


def rank_mod(matrix: list[list[int]]) -> int:
    data = [[entry % PRIME for entry in row] for row in matrix]
    row_count = len(data)
    column_count = len(data[0]) if data else 0
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if data[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        data[rank], data[pivot] = data[pivot], data[rank]
        scale = inverse(data[rank][column])
        data[rank] = [
            scale * entry % PRIME for entry in data[rank]
        ]
        for row in range(row_count):
            if row == rank:
                continue
            factor = data[row][column]
            if not factor:
                continue
            data[row] = [
                (data[row][index] - factor * data[rank][index]) % PRIME
                for index in range(column_count)
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def polynomial_from_roots(roots: list[int]) -> list[int]:
    coefficients = [1]
    for root in roots:
        result = [0] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            result[index] = (
                result[index] - root * coefficient
            ) % PRIME
            result[index + 1] = (
                result[index + 1] + coefficient
            ) % PRIME
        coefficients = result
    return coefficients


def evaluate(coefficients: list[int], value: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * value + coefficient) % PRIME
    return result


def diagonal_cauchy_coefficients() -> dict[str, object]:
    sources = [1, 2, 4, 7, 11]
    poles = [13, 17, 23, 29, 31]
    weights = [3, 5, 8, 12, 19]
    a = len(sources)
    n = a - 1
    t_cofactors = [
        polynomial_from_roots(
            [source for position, source in enumerate(sources) if position != i]
        )
        for i in range(a)
    ]
    lambda_cofactors = [
        polynomial_from_roots(
            [pole for position, pole in enumerate(poles) if position != i]
        )
        for i in range(a)
    ]

    # Column j contains the T-coefficients of N_j(T).
    coefficient_columns = [[0] * a for _ in range(a)]
    for i in range(a):
        for lambda_degree in range(a):
            scale = (
                weights[i] * lambda_cofactors[i][lambda_degree]
            ) % PRIME
            for t_degree in range(a):
                coefficient_columns[lambda_degree][t_degree] = (
                    coefficient_columns[lambda_degree][t_degree]
                    + scale * t_cofactors[i][t_degree]
                ) % PRIME

    off_diagonal_zero_count = 0
    diagonal_nonzero_count = 0
    local_transverse_count = 0
    for i, source in enumerate(sources):
        for j, pole in enumerate(poles):
            value = 0
            for index in range(a):
                value = (
                    value
                    + weights[index]
                    * evaluate(t_cofactors[index], source)
                    * evaluate(lambda_cofactors[index], pole)
                ) % PRIME
            if i == j:
                require(
                    value != 0,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:128',
                )
                diagonal_nonzero_count += 1
                continue
            require(
                value == 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:131',
            )
            off_diagonal_zero_count += 1

            t_derivative = 0
            lambda_derivative = 0
            for index in range(a):
                t_poly = t_cofactors[index]
                l_poly = lambda_cofactors[index]
                t_derivative_coefficients = [
                    degree * t_poly[degree] % PRIME
                    for degree in range(1, len(t_poly))
                ]
                l_derivative_coefficients = [
                    degree * l_poly[degree] % PRIME
                    for degree in range(1, len(l_poly))
                ]
                t_derivative = (
                    t_derivative
                    + weights[index]
                    * evaluate(t_derivative_coefficients, source)
                    * evaluate(l_poly, pole)
                ) % PRIME
                lambda_derivative = (
                    lambda_derivative
                    + weights[index]
                    * evaluate(t_poly, source)
                    * evaluate(l_derivative_coefficients, pole)
                ) % PRIME
            require(
                t_derivative != 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:159',
            )
            require(
                lambda_derivative != 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:160',
            )
            local_transverse_count += 1

    return {
        "prime": PRIME,
        "a": a,
        "n": n,
        "sources": sources,
        "poles": poles,
        "coefficient_rank": rank_mod(coefficient_columns),
        "off_diagonal_zero_count": off_diagonal_zero_count,
        "diagonal_nonzero_count": diagonal_nonzero_count,
        "local_transverse_count": local_transverse_count,
        "coefficient_columns": coefficient_columns,
    }


def convolution_rank(
    coefficient_columns: list[list[int]],
    s: int,
) -> dict[str, int]:
    n = len(coefficient_columns) - 1
    source_dimension = s + n - 1
    target_dimension = (s - 1) * (n + 1)
    matrix = [
        [0] * source_dimension for _ in range(target_dimension)
    ]
    for r in range(1, s):
        for t_degree in range(n + 1):
            row = (r - 1) * (n + 1) + t_degree
            for lambda_degree in range(n + 1):
                h = r + lambda_degree
                matrix[row][h - 1] = coefficient_columns[
                    lambda_degree
                ][t_degree]
    return {
        "s": s,
        "source_dimension": source_dimension,
        "target_dimension": target_dimension,
        "rank": rank_mod(matrix),
    }


def koalabear_rows() -> list[dict[str, object]]:
    rows = []
    for a, regular_count in [
        (12, 69),
        (14, 67),
        (14, 68),
        (14, 69),
    ]:
        n = a - 1
        minimum = regular_count - a + 4
        q = 5 if a == 12 else 4
        r = regular_count - q * a
        s_min = minimum - q * a
        s_max = regular_count - q * a
        if r <= n - 1:
            branch = "KUNNETH_VANISHING"
        else:
            require(
                r == n,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:220',
            )
            require(
                s_min >= 2,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:221',
            )
            branch = "FULL_COEFFICIENT_RANK_INJECTIVITY"
        rows.append(
            {
                "a": a,
                "n": n,
                "R": regular_count,
                "minimum_overload": minimum,
                "periods_removed": q,
                "reduced_first_degree": r,
                "reduced_second_degree_min": -s_max,
                "reduced_second_degree_max": -s_min,
                "vanishing_branch": branch,
            }
        )
    return rows


def payload() -> dict[str, object]:
    regression = diagonal_cauchy_coefficients()
    convolution = [
        convolution_rank(regression["coefficient_columns"], s)
        for s in range(2, 8)
    ]
    result = {
        "status": (
            "PROVED_GENERIC_NONCANONICAL_OVERLOAD_EXCLUSION_"
            "SEMANTIC_PRECURSOR_ADAPTERS_OPEN"
        ),
        "finite_field_regression": regression,
        "boundary_convolution_ranks": convolution,
        "koalabear_rows": koalabear_rows(),
        "claims": {
            "diagonal_cauchy_periodicity": "PROVED",
            "selected_grid_section": "PROVED",
            "subcritical_cohomology_vanishing": "PROVED",
            "full_rank_boundary_injectivity": "PROVED",
            "a12_R69_generic_overload": "IMPOSSIBLE",
            "a14_R67_R68_R69_generic_overload": "IMPOSSIBLE",
            "common_root_same_record_adapter": "OPEN",
            "coordinate_ratio_same_record_adapter": "OPEN",
            "cap_68": "OPEN",
            "active_owner_payment": "NONE",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    regression = data["finite_field_regression"]
    require(
        regression['coefficient_rank'] == regression['a'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:275',
    )
    require(
        regression['off_diagonal_zero_count'] == 20,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:276',
    )
    require(
        regression['diagonal_nonzero_count'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:277',
    )
    require(
        regression['local_transverse_count'] == 20,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:278',
    )
    for row in data["boundary_convolution_ranks"]:
        require(
            row['rank'] == row['source_dimension'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:280',
        )
        require(
            row['target_dimension'] >= row['source_dimension'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:281',
        )
    require(
        [(row['a'], row['R'], row['minimum_overload'], row['reduced_first_degree'], row['reduced_second_degree_max'], row['vanishing_branch']) for row in data['koalabear_rows']] == [(12, 69, 61, 9, -1, 'KUNNETH_VANISHING'), (14, 67, 57, 11, -1, 'KUNNETH_VANISHING'), (14, 68, 58, 12, -2, 'KUNNETH_VANISHING'), (14, 69, 59, 13, -3, 'FULL_COEFFICIENT_RANK_INJECTIVITY')],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:282',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_diagonal_cauchy_periodicity.py:321',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["koalabear_rows"][0]["reduced_first_degree"] += 1
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("diagonal-Cauchy source-pole periodicity: PASS")
    print("boundary convolution injectivity: PASS")
    print("KoalaBear generic overload exclusion: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
