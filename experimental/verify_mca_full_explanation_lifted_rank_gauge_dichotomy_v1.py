#!/usr/bin/env python3
"""Audit the lifted-rank gauge dichotomy and its two deployed rank-drop walls."""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import prod


def matrix_rank(rows: list[tuple[int, ...]], prime: int) -> int:
    work = [[entry % prime for entry in row] for row in rows]
    rank = 0
    width = len(work[0]) if work else 0
    for column in range(width):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(inverse * value) % prime for value in work[rank]]
        for index in range(len(work)):
            if index == rank or work[index][column] == 0:
                continue
            scale = work[index][column]
            work[index] = [
                (value - scale * basis) % prime
                for value, basis in zip(work[index], work[rank])
            ]
        rank += 1
    return rank


def dot(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % prime


def gauge_image_rank(
    lifted_basis: list[tuple[int, ...]],
    gauge: tuple[int, ...],
    prime: int,
) -> int:
    image = [
        tuple((row[index + 1] - row[0] * gauge[index]) % prime
              for index in range(len(gauge)))
        for row in lifted_basis
    ]
    return matrix_rank(image, prime)


def audit_small_field() -> tuple[int, int]:
    prime, dimension = 5, 2
    gauges = list(product(range(prime), repeat=dimension))
    standard = [
        tuple(int(index == coordinate) for index in range(dimension))
        for coordinate in range(dimension)
    ]
    gauge_checks = 0

    for functional in product(range(prime), repeat=dimension):
        if not any(functional):
            continue
        graph_basis = [
            (functional[index], *standard[index])
            for index in range(dimension)
        ]
        if matrix_rank(graph_basis, prime) != dimension:
            raise ValueError("graph lifted rank")
        histogram: dict[int, int] = {}
        for gauge in gauges:
            observed = gauge_image_rank(graph_basis, gauge, prime)
            expected = dimension - int(dot(functional, gauge, prime) == 1)
            if observed != expected:
                raise ValueError("graph gauge classification")
            histogram[observed] = histogram.get(observed, 0) + 1
            gauge_checks += 1
        expected_histogram = {
            dimension - 1: prime ** (dimension - 1),
            dimension: prime**dimension - prime ** (dimension - 1),
        }
        if histogram != expected_histogram:
            raise ValueError("graph gauge histogram")
        error_basis = [
            (row[0], *tuple(-value % prime for value in row[1:]))
            for row in graph_basis
        ]
        if matrix_rank(error_basis, prime) != dimension:
            raise ValueError("graph error rank")

    full_basis = [
        tuple(int(index == coordinate) for index in range(dimension + 1))
        for coordinate in range(dimension + 1)
    ]
    if matrix_rank(full_basis, prime) != dimension + 1:
        raise ValueError("full lifted rank")
    for gauge in gauges:
        if gauge_image_rank(full_basis, gauge, prime) != dimension:
            raise ValueError("full-lift gauge rank")
        gauge_checks += 1
    full_errors = [
        (row[0], *tuple(-value % prime for value in row[1:]))
        for row in full_basis
    ]
    if matrix_rank(full_errors, prime) != dimension + 1:
        raise ValueError("full-lift error rank")

    graph_basis = [(1, 1, 0), (0, 0, 1)]
    hostile = graph_basis + [(0, 1, 0)]
    if matrix_rank(hostile, prime) != dimension + 1:
        raise ValueError("hostile perturbation lifted rank")
    if any(
        gauge_image_rank(hostile, gauge, prime) != dimension
        for gauge in gauges
    ):
        raise ValueError("hostile perturbation gauge rank")
    return gauge_checks, 1


def word_weight(word: tuple[int, ...]) -> int:
    return sum(value != 0 for value in word)


def span_word(
    codeword: tuple[int, ...], scalar: int, direction: tuple[int, ...], prime: int
) -> tuple[int, ...]:
    return tuple((value + scalar * extra) % prime
                 for value, extra in zip(codeword, direction))


def dependent(
    left: tuple[int, ...], right: tuple[int, ...], prime: int
) -> bool:
    return any(
        all((b - scalar * a) % prime == 0 for a, b in zip(left, right))
        for scalar in range(prime)
    )


def extension_weights(
    words: frozenset[tuple[int, ...]], prime: int
) -> tuple[int, int, int]:
    nonzero = [word for word in words if any(word)]
    first = min(map(word_weight, nonzero))
    second = len(nonzero[0])
    for index, left in enumerate(nonzero):
        for right in nonzero[index + 1:]:
            if dependent(left, right, prime):
                continue
            union = sum(a != 0 or b != 0 for a, b in zip(left, right))
            second = min(second, union)
    full = sum(
        any(word[index] for word in words)
        for index in range(len(nonzero[0]))
    )
    return first, second, full


def audit_near_mds_extensions() -> tuple[int, dict[int, int]]:
    prime, length = 5, 5
    code = [
        tuple((constant + slope * x) % prime for x in range(length))
        for constant, slope in product(range(prime), repeat=2)
    ]
    code_set = frozenset(code)
    extensions: dict[frozenset[tuple[int, ...]], int] = {}
    for direction in product(range(prime), repeat=length):
        if direction in code_set:
            continue
        extension = frozenset(
            span_word(codeword, scalar, direction, prime)
            for codeword in code
            for scalar in range(prime)
        )
        distance = min(
            word_weight(tuple((a - b) % prime
                              for a, b in zip(direction, codeword)))
            for codeword in code
        )
        if extension in extensions and extensions[extension] != distance:
            raise ValueError("extension distance invariance")
        extensions[extension] = distance
    if len(extensions) != 31:
        raise ValueError("extension census")
    profile: dict[int, int] = {}
    for extension, distance in extensions.items():
        if extension_weights(extension, prime) != (distance, 4, 5):
            raise ValueError("near-MDS hierarchy")
        profile[distance] = profile.get(distance, 0) + 1
    if profile != {1: 5, 2: 25, 3: 1}:
        raise ValueError("extension profile")
    return len(extensions), profile


def falling(value: int, length: int) -> int:
    return prod(value - offset for offset in range(length))


def occupancy_bound(
    residual: int,
    distance: int,
    dimension: int,
    rank: int,
    factor: int,
) -> int:
    length, agreement = residual + dimension, distance + dimension
    middle = prod(distance + offset for offset in range(1, rank))
    candidates = []
    for zero_normals in range(dimension - rank + 1):
        for global_normals in range(zero_normals + 1):
            candidates.append(
                Fraction(
                    falling(length - zero_normals, rank + 1),
                    (agreement - global_normals) * middle * factor,
                )
            )
    maximum = max(candidates)
    return maximum.numerator // maximum.denominator


def first_factor(
    residual: int,
    distance: int,
    dimension: int,
    rank: int,
    budget: int,
) -> int:
    low = high = 1
    while occupancy_bound(residual, distance, dimension, rank, high) > budget:
        high *= 2
    while low < high:
        middle = (low + high) // 2
        if occupancy_bound(residual, distance, dimension, rank, middle) <= budget:
            high = middle
        else:
            low = middle + 1
    return low


def audit_deployed_walls() -> tuple[int, int]:
    rows = (
        {
            "name": "KoalaBear",
            "R": 1048576,
            "d": 67472,
            "K": 14,
            "budget": 274980728111395087,
            "drop_high": 992852,
            "low": 5,
            "frontier_j": 4337,
            "full_high": 1044239,
            "mds_endpoint": 743896698428332665,
            "required_top_factor": 182530,
        },
        {
            "name": "Mersenne-31",
            "R": 1048576,
            "d": 67448,
            "K": 6,
            "budget": 16777215,
            "drop_high": 1037876,
            "low": 1,
            "frontier_j": 4334,
            "full_high": 1044242,
            "mds_endpoint": 219426634,
            "required_top_factor": 882143,
        },
    )
    adjacent = ceilings = 0
    for row in rows:
        rank = row["K"] - 1
        factor = first_factor(
            row["R"], row["d"], row["K"], rank, row["budget"]
        )
        if row["R"] - row["d"] + factor != row["drop_high"]:
            raise ValueError(row["name"] + " rank-drop wall")
        if not (
            occupancy_bound(row["R"], row["d"], row["K"], rank, factor)
            <= row["budget"]
            < occupancy_bound(
                row["R"], row["d"], row["K"], rank, factor - 1
            )
        ):
            raise ValueError(row["name"] + " adjacent crossing")
        if row["R"] - row["frontier_j"] != row["full_high"]:
            raise ValueError(row["name"] + " full-lift arithmetic")
        if not row["low"] < row["drop_high"] < row["full_high"]:
            raise ValueError(row["name"] + " support ordering")
        endpoint = occupancy_bound(
            row["R"], row["d"], row["K"], row["K"], row["d"]
        )
        required = first_factor(
            row["R"], row["d"], row["K"], row["K"], row["budget"]
        )
        if endpoint != row["mds_endpoint"] or not endpoint > row["budget"]:
            raise ValueError(row["name"] + " MDS endpoint")
        if required != row["required_top_factor"] or not required > row["d"]:
            raise ValueError(row["name"] + " required top factor")
        adjacent += 1
        ceilings += 1
    return adjacent, ceilings


def main() -> None:
    gauges, hostile = audit_small_field()
    extensions, profile = audit_near_mds_extensions()
    adjacent, ceilings = audit_deployed_walls()
    profile_text = ",".join(f"{distance}:{count}"
                            for distance, count in sorted(profile.items()))
    print(
        "MCA_FULL_EXPLANATION_LIFTED_RANK_GAUGE_DICHOTOMY_V1_PASS "
        f"gauges={gauges} hostile={hostile} extensions={extensions} "
        f"profile={profile_text} adjacent={adjacent} ceilings={ceilings}"
    )


if __name__ == "__main__":
    main()
