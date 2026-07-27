#!/usr/bin/env python3
"""Exact checks for the Cremona-star reduction of PRCI."""

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
import itertools
import json
from math import comb
from pathlib import Path

from analyze_postcritical_universal_minors import analyze
from search_postcritical_interpolation_counterexamples import (
    compositions,
    rank_mod,
)


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "cremona_star_hypercohomology_certificate.json"


def polynomial_dimension(n: int, degree: int) -> int:
    if degree < 0:
        return 0
    return comb(n + degree, n)


def star_betti_number(R: int, n: int, index: int) -> int:
    return comb(R, n - index) * comb(
        R - n + index - 1, index - 1
    )


def check_star_resolution() -> dict[str, object]:
    cases = 0
    identities = 0
    maximum_betti = 0
    for n in range(1, 17):
        for d in range(n, 61):
            R = n + d
            point_count = comb(R, n)
            betti = [
                star_betti_number(R, n, index)
                for index in range(1, n + 1)
            ]
            maximum_betti = max(maximum_betti, *betti)
            for degree in range(d, d + n + 4):
                ideal_dimension = sum(
                    (-1) ** (index + 1)
                    * betti[index - 1]
                    * polynomial_dimension(
                        n, degree - (d + index)
                    )
                    for index in range(1, n + 1)
                )
                quotient_dimension = (
                    polynomial_dimension(n, degree)
                    - ideal_dimension
                )
                require(
                    quotient_dimension == point_count,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:62',
                )
                identities += 1
            cases += 1
    return {
        "parameter_pairs": cases,
        "hilbert_identities_checked": identities,
        "maximum_betti_number_checked": maximum_betti,
        "n_range": [1, 16],
        "d_range_rule": "n <= d <= 60",
        "status": "PASS",
    }


def reciprocal_points(
    prime: int,
    sources: tuple[int, ...],
    selected: tuple[int, ...],
) -> list[list[int]]:
    points: list[list[int]] = []
    for subset in itertools.combinations(selected, len(sources) - 1):
        coordinates = []
        for source in sources:
            product = 1
            for parameter in subset:
                product = product * (source - parameter) % prime
            coordinates.append(pow(product, prime - 2, prime))
        scale = pow(coordinates[0], prime - 2, prime)
        points.append(
            [coordinate * scale % prime for coordinate in coordinates]
        )
    return points


def evaluation_matrix(
    points: list[list[int]], degree: int, prime: int
) -> list[list[int]]:
    monomials = compositions(degree, len(points[0]))
    return [
        [
            product_mod(
                (
                    pow(coordinate, exponent, prime)
                    for coordinate, exponent in zip(point, monomial)
                ),
                prime,
            )
            for monomial in monomials
        ]
        for point in points
    ]


def product_mod(values, prime: int) -> int:
    result = 1
    for value in values:
        result = result * value % prime
    return result


def critical_kernel_case(
    prime: int,
    sources: tuple[int, ...],
    selected: tuple[int, ...],
) -> dict[str, object]:
    a = len(sources)
    d = len(selected) - a + 1
    points = reciprocal_points(prime, sources, selected)
    critical = evaluation_matrix(points, d, prime)
    postcritical = evaluation_matrix(points, d + 1, prime)
    point_count = len(points)

    stacked: list[list[int]] = []
    critical_columns = len(critical[0])
    for coordinate in range(a):
        for column in range(critical_columns):
            stacked.append(
                [
                    critical[row][column]
                    * points[row][coordinate]
                    % prime
                    for row in range(point_count)
                ]
            )

    critical_rank = rank_mod(critical, prime)
    postcritical_rank = rank_mod(postcritical, prime)
    stacked_rank = rank_mod(stacked, prime)
    require(
        stacked_rank == postcritical_rank,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:149',
    )
    return {
        "prime": prime,
        "a": a,
        "R": len(selected),
        "critical_degree": d,
        "point_count": point_count,
        "critical_rank": critical_rank,
        "critical_defect": point_count - critical_rank,
        "postcritical_rank": postcritical_rank,
        "postcritical_defect": point_count - postcritical_rank,
        "simultaneous_coordinate_kernel_dimension": (
            point_count - stacked_rank
        ),
        "kernel_identity": "PASS",
    }


def fixed_minor_route_cut(
    kernel_cases: list[dict[str, object]],
) -> list[dict[str, object]]:
    results = [
        analyze(11, 3, 6),
        analyze(13, 4, 8),
    ]
    summaries = []
    for row, kernel in zip(results, kernel_cases):
        require(
            row['status'] == 'COORDINATE_ORBIT_FAILS',
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:176',
        )
        require(
            row['first_failures'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:177',
        )
        require(
            (row['prime'], row['a'], row['R']) == (kernel['prime'], kernel['a'], kernel['R']),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:178',
        )
        summaries.append(
            {
                "prime": row["prime"],
                "a": row["a"],
                "R": row["R"],
                "tested_until_three_orbit_failures": row["tested"],
                "point_count": row["point_count"],
                "coordinate_minor_orbit_size": row["orbit_size"],
                "fixed_minor_failures_seen": row[
                    "fixed_minor_failures"
                ],
                "first_orbit_failure": json.loads(
                    json.dumps(row["first_failures"][0])
                ),
                "full_postcritical_rank": kernel[
                    "postcritical_rank"
                ],
                "full_postcritical_defect": kernel[
                    "postcritical_defect"
                ],
                "interpretation": (
                    "FIXED_MINOR_ORBIT_ROUTE_CUT"
                    if kernel["postcritical_defect"] == 0
                    else "GENUINE_PRCI_COUNTEREXAMPLE"
                ),
                "status": row["status"],
            }
        )
    return summaries


def payload() -> dict[str, object]:
    kernel_cases = [
        critical_kernel_case(
            11,
            (0, 1, 2),
            (3, 4, 6, 7, 9, 10),
        ),
        critical_kernel_case(
            13,
            (0, 1, 2, 5),
            (3, 4, 6, 7, 8, 9, 11, 12),
        ),
    ]
    result = {
        "status": "PROVED_REDUCTIONS_ROUTE_CUT_PRCI_OPEN",
        "star_resolution": check_star_resolution(),
        "critical_kernel_cases": kernel_cases,
        "fixed_minor_route_cut": fixed_minor_route_cut(kernel_cases),
        "claims": {
            "critical_kernel_identity": "PROVED",
            "hilbert_support_inequality": "PROVED_IN_NOTE",
            "cremona_star_hypercohomology_equivalence": (
                "PROVED_IN_NOTE"
            ),
            "single_fixed_minor_strategy": "CUT",
            "coordinate_orbit_of_one_minor": "CUT",
            "universal_postcritical_interpolation": "FALSE",
            "koalabear_postcritical_interpolation": "OPEN",
            "selected_record_semantic_or_interpolation": "OPEN",
            "known_block_line_planted_branch": "PROVED_SEPARATELY",
            "cap_68": "OPEN",
            "active_owner": "NONE",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    require(
        data['status'] == 'PROVED_REDUCTIONS_ROUTE_CUT_PRCI_OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:260',
    )
    resolution = data["star_resolution"]
    require(
        resolution['status'] == 'PASS',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:262',
    )
    require(
        resolution['parameter_pairs'] == 840,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:263',
    )
    require(
        resolution['hilbert_identities_checked'] == 10160,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:264',
    )

    kernel_cases = data["critical_kernel_cases"]
    require(
        [row['critical_defect'] for row in kernel_cases] == [1, 4],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:267',
    )
    require(
        [row['postcritical_defect'] for row in kernel_cases] == [0, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:270',
    )
    require(
        [row['simultaneous_coordinate_kernel_dimension'] for row in kernel_cases] == [0, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:273',
    )
    require(
        all((row['kernel_identity'] == 'PASS' for row in kernel_cases)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:277',
    )

    route_cut = data["fixed_minor_route_cut"]
    require(
        [row['status'] for row in route_cut] == ['COORDINATE_ORBIT_FAILS', 'COORDINATE_ORBIT_FAILS'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:280',
    )
    require(
        [row['point_count'] for row in route_cut] == [15, 56],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:283',
    )
    require(
        [row['first_orbit_failure']['best_rank'] for row in route_cut] == [14, 55],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:284',
    )
    require(
        [row['interpretation'] for row in route_cut] == ['FIXED_MINOR_ORBIT_ROUTE_CUT', 'GENUINE_PRCI_COUNTEREXAMPLE'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:287',
    )
    require(
        [row['full_postcritical_rank'] for row in route_cut] == [15, 55],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:293',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_cremona_star_hypercohomology_reduction.py:312',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["critical_kernel_cases"][0][
            "simultaneous_coordinate_kernel_dimension"
        ] = 1
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("star-resolution Hilbert identities: PASS")
    print("critical-kernel multiplication identity: PASS")
    print("fixed-minor coordinate-orbit route cut: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
