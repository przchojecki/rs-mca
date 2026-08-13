#!/usr/bin/env python3
"""Verify the exact finite walls of the corrected MCA occupancy compiler."""

from __future__ import annotations

from fractions import Fraction
from itertools import product as cartesian_product
from math import prod


def falling(value: int, length: int) -> int:
    result = 1
    for offset in range(length):
        result *= value - offset
    return result


def bound(R: int, d: int, K: int, rank: int, factor: int) -> int:
    N, m = R + K, d + K
    middle = prod(d + offset for offset in range(1, rank))
    values = []
    for zero_normals in range(K - rank + 1):
        for global_normals in range(zero_normals + 1):
            values.append(
                Fraction(
                    falling(N - zero_normals, rank + 1),
                    (m - global_normals) * middle * factor,
                )
            )
    maximum = max(values)
    return maximum.numerator // maximum.denominator


def first_factor(R: int, d: int, K: int, rank: int, budget: int) -> int:
    low = high = 1
    while bound(R, d, K, rank, high) > budget:
        high *= 2
    while low < high:
        middle = (low + high) // 2
        if bound(R, d, K, rank, middle) <= budget:
            high = middle
        else:
            low = middle + 1
    return low


def exhaustive_rank_one_toy() -> int:
    p, N, K, m = 3, 3, 1, 2
    words = list(cartesian_product(range(p), repeat=N))
    code = [(constant,) * N for constant in range(p)]
    checks = 0
    for base in words:
        for direction in words:
            e = min(
                sum(value != constant for value in direction)
                for constant in range(p)
            )
            options: list[list[int | None]] = []
            for slope in range(p):
                received = tuple(
                    (base[x] + slope * direction[x]) % p for x in range(N)
                )
                candidates: list[int | None] = [None]
                for explanation, word in enumerate(code):
                    support = tuple(
                        x for x in range(N) if received[x] == word[x]
                    )
                    if len(support) < m:
                        continue
                    pair_contained = any(
                        all(
                            base[x] == first and direction[x] == second
                            for x in support
                        )
                        for first in range(p)
                        for second in range(p)
                    )
                    if not pair_contained:
                        candidates.append(explanation)
                options.append(candidates)
            corrected = bound(N - K, m - K, K, 1, max(1, e - (N - m)))
            for choice in cartesian_product(*options):
                selected = [value for value in choice if value is not None]
                if len(selected) < 2 or len(set(selected)) < 2:
                    continue
                if len(selected) > corrected:
                    raise ValueError("rank-one toy violation")
                checks += 1
    return checks


def main() -> None:
    rows = (
        {
            "name": "KoalaBear",
            "R": 1048576,
            "d": 67472,
            "K": 14,
            "budget": 274980728111395087,
            "factors": (1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 49, 757, 11748, 182530),
            "walls": (981108, 981153, 981861, 992852),
            "top_bound": 743896698428332665,
        },
        {
            "name": "Mersenne-31",
            "R": 1048576,
            "d": 67448,
            "K": 6,
            "budget": 16777215,
            "factors": (1, 16, 235, 3651, 56748, 882143),
            "walls": (981144, 981363, 984779, 1037876),
            "top_bound": 219426634,
        },
    )
    zero_normal_cases = 0
    adjacent_checks = 0
    for row in rows:
        factors = tuple(
            first_factor(row["R"], row["d"], row["K"], rank, row["budget"])
            for rank in range(1, row["K"] + 1)
        )
        if factors != row["factors"]:
            raise ValueError(row["name"] + " factors")
        conditional = factors[len(factors) - 5:-1]
        walls = tuple(row["R"] - row["d"] + factor for factor in conditional)
        if walls != row["walls"]:
            raise ValueError(row["name"] + " walls")
        for offset, factor in enumerate(conditional, len(factors) - 4):
            paid = bound(row["R"], row["d"], row["K"], offset, factor)
            previous = bound(row["R"], row["d"], row["K"], offset, factor - 1)
            if not paid <= row["budget"] < previous:
                raise ValueError(row["name"] + " adjacent crossing")
            adjacent_checks += 1
        if bound(row["R"], row["d"], row["K"], row["K"], row["d"]) != row["top_bound"]:
            raise ValueError(row["name"] + " top-rank wall")
        if not factors[-1] > row["d"]:
            raise ValueError(row["name"] + " top-rank feasibility")
        zero_normal_cases += sum(
            (row["K"] - rank + 1) * (row["K"] - rank + 2) // 2
            for rank in range(1, row["K"] + 1)
        )

    regression = bound(99, 20, 1, 1, 1)
    if regression != 471 or not 31 <= regression:
        raise ValueError("GF(1009) regression")
    toy_checks = exhaustive_rank_one_toy()
    if toy_checks != 540:
        raise ValueError("toy census")
    print(
        "MCA_PROPER_SUBSPACE_OCCUPANCY_COMPILER_V1_PASS "
        f"zero_normal_cases={zero_normal_cases} adjacent={adjacent_checks} "
        f"regression={regression} toy_selections={toy_checks}"
    )


if __name__ == "__main__":
    main()
