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


def f25_add(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return ((left[0] + right[0]) % 5, (left[1] + right[1]) % 5)


def f25_mul(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    # F_25=F_5[a]/(a^2-2); 2 is a nonsquare modulo 5.
    return (
        (left[0] * right[0] + 2 * left[1] * right[1]) % 5,
        (left[0] * right[1] + left[1] * right[0]) % 5,
    )


def f25_pow(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = f25_mul(result, value)
        value = f25_mul(value, value)
        exponent //= 2
    return result


def f25_sum(values: list[tuple[int, int]]) -> tuple[int, int]:
    result = (0, 0)
    for value in values:
        result = f25_add(result, value)
    return result


def f25_moments(
    points: list[tuple[int, int]], indices: tuple[int, ...]
) -> tuple[tuple[int, int], ...]:
    return tuple(f25_sum([f25_pow(point, j) for point in points])
                 for j in indices)


def check_ambient_invariance() -> int:
    mu4 = [(1, 0), (2, 0), (4, 0), (3, 0)]
    scalar = (0, 1)
    scaled = [f25_mul(scalar, point) for point in mu4]
    indices = (1, 2, 3)
    cases = 0
    for mask in range(16):
        base = [mu4[index] for index in range(4) if mask >> index & 1]
        extension = [
            scaled[index] for index in range(4) if mask >> index & 1
        ]
        base_moments = f25_moments(base, indices)
        extension_moments = f25_moments(extension, indices)
        expected = tuple(
            f25_mul(f25_pow(scalar, j), value)
            for j, value in zip(indices, base_moments)
        )
        check(extension_moments == expected, "ambient moment scaling")
        cases += 1

    for left in range(16):
        for right in range(16):
            base_left = [mu4[index] for index in range(4) if left >> index & 1]
            base_right = [mu4[index] for index in range(4) if right >> index & 1]
            ext_left = [scaled[index] for index in range(4) if left >> index & 1]
            ext_right = [scaled[index] for index in range(4) if right >> index & 1]
            check(
                (f25_moments(base_left, indices) ==
                 f25_moments(base_right, indices)) ==
                (f25_moments(ext_left, indices) ==
                 f25_moments(ext_right, indices)),
                "ambient moment-fiber equality",
            )
            cases += 1
    return cases


def elementary_prefix(
    points: tuple[int, ...], depth: int, p: int
) -> tuple[int, ...]:
    coefficients = [1] + [0] * depth
    for point in points:
        for degree in range(depth, 0, -1):
            coefficients[degree] = (
                coefficients[degree] + point * coefficients[degree - 1]
            ) % p
    return tuple(coefficients[1:])


def power_prefix(
    points: tuple[int, ...], depth: int, p: int
) -> tuple[int, ...]:
    return tuple(
        sum(pow(point, degree, p) for point in points) % p
        for degree in range(1, depth + 1)
    )


def check_selector_transport(p: int, theta: int, m: int, r: int) -> None:
    check(pow(theta, 2 * m, p) == 1, "selector root order upper")
    check(pow(theta, m, p) == p - 1, "selector root antipode")
    check(p > 2 * r, "selector Newton gate")
    half = tuple(pow(theta, index, p) for index in range(m))
    domain = tuple(pow(theta, index, p) for index in range(2 * m))
    check(len(set(domain)) == 2 * m, "selector root order exact")

    cube_fibers: Counter[tuple[int, ...]] = Counter()
    selector_fibers: Counter[tuple[int, ...]] = Counter()
    selector_images: dict[tuple[int, ...], tuple[int, ...]] = {}
    for bits in itertools.product((0, 1), repeat=m):
        odd = tuple(
            sum(
                bit * pow(point, 2 * degree - 1, p)
                for bit, point in zip(bits, half)
            )
            % p
            for degree in range(1, r + 1)
        )
        selector = tuple(
            point if bit else (-point) % p
            for bit, point in zip(bits, half)
        )
        prefix = power_prefix(selector, 2 * r, p)
        expected = []
        for degree in range(1, 2 * r + 1):
            constant = sum(pow(point, degree, p) for point in half) % p
            if degree % 2:
                expected.append(
                    (2 * odd[(degree - 1) // 2] - constant) % p
                )
            else:
                expected.append(constant)
        check(prefix == tuple(expected), "selector affine prefix")
        if m & (m - 1) == 0:
            selector_set = set(selector)
            stabilizer = sum(
                {
                    pow(theta, shift, p) * point % p
                    for point in selector_set
                }
                == selector_set
                for shift in range(2 * m)
            )
            check(stabilizer == 1, "selector aperiodicity")
        cube_fibers[odd] += 1
        selector_fibers[prefix] += 1
        selector_images[odd] = prefix

    check(len(selector_images) == len(cube_fibers), "selector key injection")
    for odd, size in cube_fibers.items():
        check(
            selector_fibers[selector_images[odd]] == size,
            "selector fiber equality",
        )

    ambient: Counter[tuple[int, ...]] = Counter()
    power_to_elementary: dict[tuple[int, ...], tuple[int, ...]] = {}
    elementary_to_power: dict[tuple[int, ...], tuple[int, ...]] = {}
    for subset in itertools.combinations(domain, m):
        powers = power_prefix(subset, 2 * r, p)
        elementary = elementary_prefix(subset, 2 * r, p)
        ambient[powers] += 1
        previous = power_to_elementary.setdefault(powers, elementary)
        check(previous == elementary, "selector Newton forward")
        previous_power = elementary_to_power.setdefault(elementary, powers)
        check(previous_power == powers, "selector Newton reverse")

    ambient_maximum = max(ambient.values())
    check(max(cube_fibers.values()) <= ambient_maximum, "selector ambient cap")
    for prefix, size in selector_fibers.items():
        check(size <= ambient[prefix], "selector transversal containment")


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


def check_fixed_weight_bridge(
    p: int, m: int, rows: list[list[int]]
) -> int:
    layers = [Counter() for _ in range(m + 1)]
    full: Counter[tuple[int, ...]] = Counter()
    all_one = syndrome(rows, (1,) * m, p)
    for bits in itertools.product((0, 1), repeat=m):
        value = syndrome(rows, bits, p)
        layers[sum(bits)][value] += 1
        full[value] += 1

    mass = Fraction(sum(size * size for size in full.values()), 1 << m)
    for weight, layer in enumerate(layers):
        complement = Counter()
        for value, count in layer.items():
            shifted = tuple((a - v) % p for a, v in zip(all_one, value))
            complement[shifted] = count
        check(complement == layers[m - weight], "fixed-weight complement")

    codomain = p ** rank_mod(rows, p)
    bands = (set(range(m + 1)), set(range(2, max(2, m - 1))))
    for good in bands:
        loss = Fraction(1)
        for weight in good:
            population = math.comb(m, weight)
            maximum = max(layers[weight].values())
            loss = max(
                loss,
                Fraction(maximum * codomain, codomain + population),
            )
            check(
                maximum <= loss * (1 + Fraction(population, codomain)),
                "fixed-weight premise",
            )
        tail = sum(
            math.comb(m, weight)
            for weight in range(m + 1)
            if weight not in good
        )
        bound = (
            Fraction(3 * tail * tail, 1 << m)
            + 3 * loss * (m + 1 + Fraction(1 << m, codomain))
        )
        check(mass <= bound, "fixed-weight band bridge")
        if len(good) == m + 1:
            sharp = 2 * loss * (m + 1 + Fraction(1 << m, codomain))
            check(mass <= sharp, "fixed-weight all-weight bridge")
    return len(bands)


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

    all_types = {
        *(("plus", 1, degree) for degree in range(1, 7)),
        ("plus", 2, 2),
        ("plus", 2, 4),
        ("plus", 4, 4),
        ("minus", 2, 2),
        ("minus", 2, 4),
        ("minus", 4, 4),
    }
    plus_six_candidates = ((1, 257), (3, 7), (5, 3))
    for coefficient, divisor in plus_six_candidates:
        candidate = coefficient * (1 << 40) + 1
        check(candidate % divisor == 0, "plus e=6 compositeness")
        check(candidate**3 < 1 << 128, "plus cube-cap candidate")
    minus_six_candidates = (
        (40, 1, 3),
        (40, 3, 144899),
        (40, 5, 179),
        (41, 1, 13367),
        (41, 3, 5),
        (42, 1, 3),
    )
    for valuation, coefficient, divisor in minus_six_candidates:
        candidate = coefficient * (1 << valuation) - 1
        check(candidate % divisor == 0, "minus e=6 compositeness")
        check(candidate**3 < 1 << 128, "minus cube-cap candidate")
    check((7 * (1 << 40) + 1) ** 3 > 1 << 128, "plus cube cutoff")
    check((5 * (1 << 41) - 1) ** 3 > 1 << 128, "minus b41 cutoff")
    check((3 * (1 << 42) - 1) ** 3 > 1 << 128, "minus b42 cutoff")
    check(((1 << 43) - 1) ** 3 > 1 << 128, "minus valuation cutoff")
    check(len(all_types) == 12, "all admissible type count")
    check(
        sum(order < degree for _, order, degree in all_types) == 7,
        "non-generating type count",
    )
    non_generating = {
        row for row in all_types if row[1] < row[2]
    }
    descent = {
        row: (row[0], row[1], row[1]) for row in non_generating
    }
    check(
        set(descent.values()) == {
            ("plus", 1, 1), ("plus", 2, 2), ("minus", 2, 2)
        },
        "seven-to-three generated-field descent",
    )
    ambient_cases = check_ambient_invariance()
    selector_rows = (
        (17, 2, 4, 1),
        (13, 2, 6, 2),
        (17, 3, 8, 3),
    )
    for row in selector_rows:
        check_selector_transport(*row)

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
    bridge_cases = sum(check_fixed_weight_bridge(*case) for case in matrix_cases)
    check(
        any(unweighted != Fraction(collisions, 1 << case[1])
            for case, (collisions, unweighted, _) in zip(matrix_cases, collision_counts)),
        "weighted/unweighted mutation must be detected",
    )

    print(
        "F2_ADMISSIBLE_BRANCH_CORRECTION_PASS "
        f"checks={CHECKS} order_cases={order_cases} "
        f"orbit_cases={orbit_cases} top_cases={top_cases} "
        f"matrix_cases={len(matrix_cases)} ambient_cases={ambient_cases} "
        f"bridge_cases={bridge_cases} selector_cases={len(selector_rows)}"
    )


if __name__ == "__main__":
    main()
