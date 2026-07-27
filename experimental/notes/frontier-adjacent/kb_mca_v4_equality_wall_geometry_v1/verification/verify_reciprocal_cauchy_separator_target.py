#!/usr/bin/env python3
"""Finite diagnostics and exact arithmetic for the RCS target."""

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
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "reciprocal_cauchy_separator_target_certificate.json"
PRIME = 1_000_003


def inverse(value: int) -> int:
    return pow(value % PRIME, PRIME - 2, PRIME)


def compositions(total: int, parts: int) -> list[tuple[int, ...]]:
    if parts == 1:
        return [(total,)]
    result = []
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            result.append((first,) + tail)
    return result


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
        for row in range(rank + 1, row_count):
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


def evaluation_row(
    coordinates: list[int], monomials: list[tuple[int, ...]]
) -> list[int]:
    row = []
    for exponents in monomials:
        value = 1
        for coordinate, exponent in zip(coordinates, exponents):
            value = value * pow(coordinate, exponent, PRIME) % PRIME
        row.append(value)
    return row


def interpolation_profile(
    a: int, selected_count: int, seed: int
) -> dict[str, int]:
    random.seed(seed)
    values = random.sample(range(1, PRIME), a + selected_count)
    source_values = values[:a]
    selected_values = values[a:]
    degree = selected_count - a + 1
    interpolation_monomials = compositions(degree, a)
    separator_monomials = compositions(degree + 1, a)
    interpolation_matrix = []
    separator_matrix = []

    for subset in itertools.combinations(selected_values, a - 1):
        coordinates = []
        for source in source_values:
            value = 1
            for selected in subset:
                value = value * (source - selected) % PRIME
            coordinates.append(inverse(value))
        projective_scale = inverse(coordinates[0])
        coordinates = [
            coordinate * projective_scale % PRIME
            for coordinate in coordinates
        ]
        interpolation_matrix.append(
            evaluation_row(coordinates, interpolation_monomials)
        )
        separator_matrix.append(
            evaluation_row(coordinates, separator_monomials)
        )

    off_rows = []
    for _ in range(5):
        coordinates = [1] + [
            random.randrange(1, PRIME) for _ in range(a - 1)
        ]
        off_rows.append(evaluation_row(coordinates, separator_monomials))

    interpolation_rank = rank_mod(interpolation_matrix)
    separator_rank = rank_mod(separator_matrix)
    augmented_rank = rank_mod(separator_matrix + off_rows)
    return {
        "a": a,
        "R": selected_count,
        "degree": degree,
        "point_count": len(interpolation_matrix),
        "interpolation_rank": interpolation_rank,
        "interpolation_defect": (
            len(interpolation_matrix) - interpolation_rank
        ),
        "separator_rank": separator_rank,
        "separator_defect": len(separator_matrix) - separator_rank,
        "off_point_count": len(off_rows),
        "off_point_rank_gain": augmented_rank - separator_rank,
    }


def koalabear_arithmetic() -> dict[str, int]:
    h_min = 118_077
    h_max = 118_599

    def minimum_rows(h: int) -> int:
        return 59 * (67_472 + h) - 10 * 981_105

    def cremona_degree(h: int) -> int:
        return 11 * h - 1_281_978

    closed_values = [
        h
        for h in range(h_min, h_max + 1)
        if minimum_rows(h) > 59 * cremona_degree(h)
    ]
    return {
        "h_min": h_min,
        "h_max": h_max,
        "conditional_closed_min": min(closed_values),
        "conditional_closed_max": max(closed_values),
        "conditional_closed_count": len(closed_values),
        "remaining_min": max(closed_values) + 1,
        "remaining_max": h_max,
        "remaining_count": h_max - max(closed_values),
        "endpoint_minimum_rows": minimum_rows(h_min),
        "endpoint_cremona_degree": cremona_degree(h_min),
        "endpoint_bezout_cap": 59 * cremona_degree(h_min),
        "endpoint_margin": (
            minimum_rows(h_min) - 59 * cremona_degree(h_min)
        ),
    }


def payload() -> dict[str, object]:
    cases = [
        interpolation_profile(3, 6, 201),
        interpolation_profile(3, 7, 101),
        interpolation_profile(4, 8, 202),
        interpolation_profile(4, 9, 102),
        interpolation_profile(5, 10, 203),
        interpolation_profile(5, 11, 103),
    ]
    result = {
        "status": "EXPERIMENTAL_RCS_OPEN_CONDITIONAL_REDUCTION_PROVED",
        "field": PRIME,
        "finite_profiles": cases,
        "koalabear_conditional_arithmetic": koalabear_arithmetic(),
        "claims": {
            "degree_d_unisolvence": "FALSE_IN_TESTED_GENERIC_CASES",
            "reciprocal_cauchy_separation": "OPEN",
            "separator_implication": "PROVED",
            "a12_R69_conditional_reduction": "PROVED",
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
    profiles = data["finite_profiles"]
    require(
        [case['interpolation_defect'] for case in profiles] == [1, 0, 2, 7, 3, 20],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:203',
    )
    require(
        all((case['separator_defect'] == 0 for case in profiles)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:206',
    )
    require(
        all((case['off_point_rank_gain'] == 5 for case in profiles)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:207',
    )
    arithmetic = data["koalabear_conditional_arithmetic"]
    require(
        arithmetic['conditional_closed_min'] == 118077,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:209',
    )
    require(
        arithmetic['conditional_closed_max'] == 118316,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:210',
    )
    require(
        arithmetic['conditional_closed_count'] == 240,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:211',
    )
    require(
        arithmetic['remaining_count'] == 283,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:212',
    )
    require(
        arithmetic['endpoint_minimum_rows'] == 1136341,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:213',
    )
    require(
        arithmetic['endpoint_cremona_degree'] == 16869,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:214',
    )
    require(
        arithmetic['endpoint_bezout_cap'] == 995271,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:215',
    )
    require(
        arithmetic['endpoint_margin'] == 141070,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:216',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_reciprocal_cauchy_separator_target.py:233',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["koalabear_conditional_arithmetic"][
            "conditional_closed_max"
        ] += 1
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("reciprocal-Cauchy separator diagnostics: PASS")
    print("KoalaBear conditional arithmetic: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
