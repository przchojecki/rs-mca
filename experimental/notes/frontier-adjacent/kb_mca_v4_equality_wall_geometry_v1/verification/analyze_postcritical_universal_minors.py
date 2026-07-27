#!/usr/bin/env python3
"""Test whether a fixed postcritical monomial minor is universal."""

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



import itertools
import json
from math import comb

from search_postcritical_interpolation_counterexamples import compositions


def inverse(value: int, prime: int) -> int:
    return pow(value % prime, prime - 2, prime)


def matrix_for(
    prime: int,
    sources: tuple[int, ...],
    selected: tuple[int, ...],
) -> tuple[list[list[int]], list[tuple[int, ...]]]:
    a = len(sources)
    degree = len(selected) - a + 2
    monomials = compositions(degree, a)
    matrix = []
    for subset in itertools.combinations(selected, a - 1):
        coordinates = []
        for source in sources:
            value = 1
            for parameter in subset:
                value = value * (source - parameter) % prime
            coordinates.append(inverse(value, prime))
        scale = inverse(coordinates[-1], prime)
        coordinates = [value * scale % prime for value in coordinates]
        row = []
        for exponents in monomials:
            value = 1
            for coordinate, exponent in zip(coordinates, exponents):
                value = value * pow(coordinate, exponent, prime) % prime
            row.append(value)
        matrix.append(row)
    return matrix, monomials


def pivot_columns(matrix: list[list[int]], prime: int) -> list[int]:
    data = [[entry % prime for entry in row] for row in matrix]
    rows = len(data)
    columns = len(data[0])
    rank = 0
    pivots = []
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, rows)
                if data[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        data[rank], data[pivot] = data[pivot], data[rank]
        scale = inverse(data[rank][column], prime)
        data[rank] = [scale * value % prime for value in data[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = data[row][column]
            if factor:
                data[row] = [
                    (data[row][index] - factor * data[rank][index]) % prime
                    for index in range(columns)
                ]
        pivots.append(column)
        rank += 1
        if rank == rows:
            break
    return pivots


def rank_selected(
    matrix: list[list[int]], columns: list[int], prime: int
) -> int:
    reduced = [[row[column] for column in columns] for row in matrix]
    return len(pivot_columns(reduced, prime))


def analyze(prime: int, a: int, selected_count: int) -> dict[str, object]:
    field = tuple(range(prime))
    first_sources = tuple(field[:a])
    first_selected = tuple(field[a : a + selected_count])
    first_matrix, monomials = matrix_for(
        prime, first_sources, first_selected
    )
    basis = pivot_columns(first_matrix, prime)
    point_count = comb(selected_count, a - 1)
    require(
        len(basis) == point_count,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/analyze_postcritical_universal_minors.py:97',
    )
    monomial_index = {
        monomial: index for index, monomial in enumerate(monomials)
    }
    orbit_bases = []
    seen_bases = set()
    for permutation in itertools.permutations(range(a)):
        permuted = tuple(
            sorted(
                monomial_index[
                    tuple(monomial[index] for index in permutation)
                ]
                for monomial in (monomials[column] for column in basis)
            )
        )
        if permuted not in seen_bases:
            seen_bases.add(permuted)
            orbit_bases.append(list(permuted))

    tested = 0
    fixed_failures = 0
    orbit_failures = []
    for sources in itertools.combinations(field, a):
        available = tuple(value for value in field if value not in sources)
        for selected in itertools.combinations(available, selected_count):
            matrix, _ = matrix_for(prime, sources, selected)
            tested += 1
            fixed_rank = rank_selected(matrix, basis, prime)
            if fixed_rank != point_count:
                fixed_failures += 1
            orbit_ranks = [
                rank_selected(matrix, orbit_basis, prime)
                for orbit_basis in orbit_bases
            ]
            if max(orbit_ranks) != point_count:
                orbit_failures.append(
                    {
                        "sources": sources,
                        "selected": selected,
                        "best_rank": max(orbit_ranks),
                    }
                )
                if len(orbit_failures) == 3:
                    return {
                        "prime": prime,
                        "a": a,
                        "R": selected_count,
                        "tested": tested,
                        "point_count": point_count,
                        "basis": [monomials[index] for index in basis],
                        "orbit_size": len(orbit_bases),
                        "fixed_minor_failures": fixed_failures,
                        "status": "COORDINATE_ORBIT_FAILS",
                        "first_failures": orbit_failures,
                    }
    return {
        "prime": prime,
        "a": a,
        "R": selected_count,
        "tested": tested,
        "point_count": point_count,
        "basis": [monomials[index] for index in basis],
        "orbit_size": len(orbit_bases),
        "fixed_minor_failures": fixed_failures,
        "status": "COORDINATE_ORBIT_COVERS_FIELD",
    }


def main() -> int:
    results = [
        analyze(11, 3, 6),
        analyze(13, 4, 8),
    ]
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
