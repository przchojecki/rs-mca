#!/usr/bin/env python3
"""Fail-closed checks for f2_admissible_branch_correction.tex."""

from __future__ import annotations

import itertools
import math
from collections import Counter
from fractions import Fraction


CHECKS = 0


def check(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(label)


def v2(value: int) -> int:
    return (value & -value).bit_length() - 1


def dyadic_order(value: int, exponent: int) -> int:
    modulus = 1 << exponent
    current = value % modulus
    order = 1
    while current != 1:
        current = current * current % modulus
        order *= 2
        if order > 1 << (exponent - 2):
            raise AssertionError("dyadic order overflow")
    return order


def lucas_lehmer(exponent: int) -> bool:
    if exponent == 2:
        return True
    modulus = (1 << exponent) - 1
    value = 4
    for _ in range(exponent - 2):
        value = (value * value - 2) % modulus
    return value == 0


def trial_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def pocklington(
    value: int, factors: dict[int, int], witnesses: dict[int, int]
) -> None:
    product = math.prod(prime**power for prime, power in factors.items())
    check(product == value - 1, "complete p-1 factorization")
    check(product > math.isqrt(value), "Pocklington size threshold")
    for prime in factors:
        check(trial_prime(prime), "factor primality")
        witness = witnesses[prime]
        check(pow(witness, value - 1, value) == 1, "Fermat condition")
        check(
            math.gcd(pow(witness, (value - 1) // prime, value) - 1, value)
            == 1,
            "Pocklington gcd condition",
        )


def orbit_union(modulus: int, p: int, r: int) -> set[int]:
    h = dyadic_order(p, modulus.bit_length() - 1)
    roots = set()
    for j in range(1, r + 1):
        exponent = 2 * j - 1
        value = exponent
        for _ in range(h):
            roots.add(value % modulus)
            value = value * p % modulus
    check(len(roots) == h * r, "Frobenius-root collision")
    return roots


def rank_mod(rows: list[list[int]], p: int) -> int:
    work = [[entry % p for entry in row] for row in rows]
    if not work:
        return 0
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, p)
        work[rank] = [(inverse * entry) % p for entry in work[rank]]
        for index in range(len(work)):
            if index != rank and work[index][column]:
                factor = work[index][column]
                work[index] = [
                    (left - factor * right) % p
                    for left, right in zip(work[index], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def independent_rows(rows: list[list[int]], p: int) -> list[list[int]]:
    basis: list[list[int]] = []
    for row in rows:
        if rank_mod(basis + [row], p) > len(basis):
            basis.append(row)
    return basis


def syndrome(
    rows: list[list[int]], vector: tuple[int, ...], p: int
) -> tuple[int, ...]:
    return tuple(
        sum(entry * value for entry, value in zip(row, vector)) % p
        for row in rows
    )


def check_weighted_identity(
    p: int, m: int, rows: list[list[int]]
) -> tuple[int, int, int]:
    fibers: Counter[tuple[int, ...]] = Counter()
    for bits in itertools.product((0, 1), repeat=m):
        fibers[syndrome(rows, bits, p)] += 1
    collisions = sum(size * size for size in fibers.values())
    maximum = max(fibers.values())

    mass = Fraction(0)
    unweighted = 0
    for epsilon in itertools.product((-1, 0, 1), repeat=m):
        if not any(syndrome(rows, epsilon, p)):
            weight = sum(value != 0 for value in epsilon)
            mass += Fraction(1, 1 << weight)
            unweighted += 1

    rank = rank_mod(rows, p)
    check(collisions == (1 << m) * mass, "weighted collision normalization")
    check(Fraction(maximum * maximum, 1 << m) <= mass, "max-fiber lower sandwich")
    check(mass <= maximum, "max-fiber upper sandwich")
    check(mass >= 1, "diagonal floor")
    check(mass >= Fraction(1 << m, p**rank), "rank floor")

    basis = independent_rows(rows, p)
    weighted_fourier = 0.0
    wrong_fourier = 0.0
    for dual in itertools.product(range(p), repeat=rank):
        weighted_term = 1.0
        wrong_term = 1.0
        for column in range(m):
            phase = sum(
                dual[index] * basis[index][column] for index in range(rank)
            ) % p
            cosine = math.cos(2.0 * math.pi * phase / p)
            weighted_term *= 1.0 + cosine
            wrong_term *= 1.0 + 2.0 * cosine
        weighted_fourier += weighted_term
        wrong_fourier += wrong_term
    weighted_fourier /= p**rank
    wrong_fourier /= p**rank
    check(abs(weighted_fourier - float(mass)) < 1e-9, "1+cos Fourier identity")
    check(abs(wrong_fourier - unweighted) < 1e-8, "1+2cos unweighted control")
    return collisions, unweighted, maximum


def main() -> None:
    n = 1 << 41
    p = (1 << 61) - 1
    q = p * p
    check(lucas_lehmer(61), "M61 Lucas-Lehmer certificate")
    check(q.bit_length() == 122 and q < 1 << 256, "official field cap")
    check(p % n == n - 1, "M61 minus congruence")
    check(dyadic_order(p, 41) == 2, "M61 generating order")
    check(v2(p - 1) == 1, "M61 plus valuation")
    check((1 << (41 - v2(p - 1))) != 2, "old all-row formula mutation")
    check(math.gcd(n, p - 1) == 2, "prime-field root intersection")
    check(n // 2 == 1 << 40, "singleton class count")

    plus_rows = (
        (3 * (1 << 41) + 1, 1, {2: 41, 3: 1}, {2: 5, 3: 5}, 41),
        (27 * (1 << 40) + 1, 2, {2: 40, 3: 3}, {2: 5, 3: 3}, 40),
        (5 * (1 << 39) + 1, 4, {2: 39, 5: 1}, {2: 3, 5: 3}, 39),
    )
    observed_types: set[tuple[str, int, int]] = set()
    for prime, degree, factors, witnesses, valuation in plus_rows:
        pocklington(prime, factors, witnesses)
        check(prime % 4 == 1, "plus residue")
        check(v2(prime - 1) == valuation, "plus valuation")
        check(dyadic_order(prime, 41) == degree, "plus order")
        check(prime**degree < 1 << 256, "plus field cap")
        observed_types.add(("plus", valuation, degree))

    observed_types.add(("minus", 40, 2))
    minus_four = 25 * (1 << 39) - 1
    pocklington(
        minus_four,
        {2: 1, 3: 2, 131: 1, 20011: 1, 291271: 1},
        {2: 3, 3: 2, 131: 2, 20011: 2, 291271: 2},
    )
    check(minus_four % 4 == 3, "minus-four residue")
    check(v2(minus_four + 1) == 39, "minus-four valuation")
    check(dyadic_order(minus_four, 41) == 4, "minus-four order")
    check(minus_four**4 < 1 << 256, "minus-four field cap")
    observed_types.add(("minus", 39, 4))

    generated_types: set[tuple[str, int, int]] = set()
    for valuation in range(2, 48):
        plus_order = 1 << max(0, 41 - valuation)
        minus_order = 1 << max(1, 41 - valuation)
        for degree in range(1, 7):
            if plus_order == degree:
                generated_types.add(("plus", min(valuation, 41), degree))
            if minus_order == degree:
                generated_types.add(("minus", min(valuation, 40), degree))
    check(generated_types == observed_types, "five generating row types")

    order_cases = 0
    for exponent in range(3, 14):
        modulus = 1 << exponent
        for residue in range(3, modulus, 4):
            expected = 1 << max(1, exponent - v2(residue + 1))
            check(
                dyadic_order(residue, exponent) == expected,
                "minus dyadic order law",
            )
            order_cases += 1

    t_max = (n + 40) // 41
    r_max = (t_max + 1) // 2
    check(2 * r_max < 1 << 36, "official odd-root separation")

    orbit_cases = 0
    for exponent in range(8, 15):
        modulus = 1 << exponent
        for residue in range(3, modulus, 4):
            h = dyadic_order(residue, exponent)
            if h <= 4:
                r = min(7, (modulus // 8 - 1) // 2)
                if r:
                    orbit_union(modulus, residue, r)
                    orbit_cases += 1

    official_patterns = (
        (1 << 39) - 1,
        3 * (1 << 39) - 1,
        (1 << 40) - 1,
        (1 << 41) - 1,
        p,
    )
    top_cases = 0
    for residue in official_patterns:
        for exponent in (39, 40, 41):
            if dyadic_order(residue, exponent) <= 4:
                orbit_union(1 << exponent, residue, 64)
                top_cases += 1

    matrix_cases = (
        (3, 4, []),
        (3, 5, [[1, 0, 1, 2, 1], [0, 1, 1, 1, 2]]),
        (
            5,
            6,
            [
                [1, 2, 3, 4, 0, 1],
                [2, 4, 1, 3, 0, 2],
                [0, 1, 0, 1, 0, 1],
            ],
        ),
        (7, 6, [[1, 1, 1, 1, 1, 1], [0, 1, 2, 3, 4, 5]]),
    )
    collision_counts = [check_weighted_identity(*case) for case in matrix_cases]
    check(
        any(unweighted != Fraction(collisions, 1 << case[1])
            for case, (collisions, unweighted, _) in zip(matrix_cases, collision_counts)),
        "weighted/unweighted mutation must be detected",
    )

    print(
        "F2_ADMISSIBLE_BRANCH_CORRECTION_PASS "
        f"checks={CHECKS} order_cases={order_cases} "
        f"orbit_cases={orbit_cases} top_cases={top_cases} "
        f"matrix_cases={len(matrix_cases)}"
    )


if __name__ == "__main__":
    main()
