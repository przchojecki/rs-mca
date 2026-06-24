#!/usr/bin/env python3
"""Verify the L1 prefix bad-prime certificate theorem.

The theorem checked here is templatewise:

    finite-field prefix collision for a split prime p
      -> characteristic-zero collision
         or p divides a cyclotomic resultant certificate.

This script is intentionally small and nonmutating.  It does not prove the
missing L1 bad-prime aggregation theorem.

It also checks the split-prime row-accounting identity for the known F_17
packet: summing modular common-root degrees over template pairs agrees with
counting collision pairs over all primitive roots.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from math import comb, gcd
from typing import Any, Iterable, Sequence


STATUS = "PROVED / FINITE-FIELD REDUCTION / NOT A FULL AGGREGATION BOUND"
BOUNDED_SPLIT_PRIME_SCAN_LIMIT = 5_000


def trim(poly: Sequence[int]) -> list[int]:
    out = list(poly)
    while out and out[-1] == 0:
        out.pop()
    return out


def degree(poly: Sequence[int]) -> int:
    return len(trim(poly)) - 1


def poly_sub(left: Sequence[int], right: Sequence[int]) -> list[int]:
    out = [0] * max(len(left), len(right))
    for idx in range(len(out)):
        lhs = left[idx] if idx < len(left) else 0
        rhs = right[idx] if idx < len(right) else 0
        out[idx] = lhs - rhs
    return trim(out)


def poly_mul(left: Sequence[int], right: Sequence[int]) -> list[int]:
    if not left or not right:
        return []
    out = [0] * (len(left) + len(right) - 1)
    for i, lhs in enumerate(left):
        for j, rhs in enumerate(right):
            out[i + j] += lhs * rhs
    return trim(out)


def poly_divmod_monic(
    numerator: Sequence[int],
    divisor: Sequence[int],
) -> tuple[list[int], list[int]]:
    top = trim(numerator)
    bottom = trim(divisor)
    if not bottom or bottom[-1] != 1:
        raise AssertionError("monic nonzero divisor required")
    quotient = [0] * max(0, len(top) - len(bottom) + 1)
    while top and len(top) >= len(bottom):
        shift = len(top) - len(bottom)
        coeff = top[-1]
        quotient[shift] += coeff
        for idx, div_coeff in enumerate(bottom):
            top[shift + idx] -= coeff * div_coeff
        top = trim(top)
    return trim(quotient), top


def trim_mod(poly: Sequence[int], prime: int) -> list[int]:
    out = [coeff % prime for coeff in poly]
    while out and out[-1] == 0:
        out.pop()
    return out


def poly_divmod_mod(
    numerator: Sequence[int],
    divisor: Sequence[int],
    prime: int,
) -> tuple[list[int], list[int]]:
    top = trim_mod(numerator, prime)
    bottom = trim_mod(divisor, prime)
    if not bottom:
        raise AssertionError("nonzero divisor required")
    quotient = [0] * max(0, len(top) - len(bottom) + 1)
    inv_lead = pow(bottom[-1], -1, prime)
    while top and len(top) >= len(bottom):
        shift = len(top) - len(bottom)
        coeff = top[-1] * inv_lead % prime
        quotient[shift] = coeff
        for idx, div_coeff in enumerate(bottom):
            top[shift + idx] = (top[shift + idx] - coeff * div_coeff) % prime
        top = trim_mod(top, prime)
    return trim_mod(quotient, prime), top


def poly_gcd_mod(left: Sequence[int], right: Sequence[int], prime: int) -> list[int]:
    a = trim_mod(left, prime)
    b = trim_mod(right, prime)
    while b:
        _, remainder = poly_divmod_mod(a, b, prime)
        a, b = b, remainder
    if not a:
        return []
    inv_lead = pow(a[-1], -1, prime)
    return trim_mod([(coeff * inv_lead) % prime for coeff in a], prime)


def positive_divisors(value: int) -> list[int]:
    small: list[int] = []
    large: list[int] = []
    divisor = 1
    while divisor * divisor <= value:
        if value % divisor == 0:
            small.append(divisor)
            if divisor != value // divisor:
                large.append(value // divisor)
        divisor += 1
    return small + large[::-1]


_CYCLOTOMIC_CACHE: dict[int, list[int]] = {}


def cyclotomic_poly(n: int) -> list[int]:
    if n in _CYCLOTOMIC_CACHE:
        return _CYCLOTOMIC_CACHE[n][:]
    poly = [-1] + [0] * (n - 1) + [1]
    for divisor in positive_divisors(n):
        if divisor == n:
            continue
        quotient, remainder = poly_divmod_monic(poly, cyclotomic_poly(divisor))
        if remainder:
            raise AssertionError(f"cyclotomic division failed for n={n}")
        poly = quotient
    _CYCLOTOMIC_CACHE[n] = poly[:]
    return poly


def determinant_bareiss(matrix: list[list[int]]) -> int:
    size = len(matrix)
    if size == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_idx in range(size - 1):
        pivot_row = None
        for row in range(pivot_idx, size):
            if work[row][pivot_idx] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            return 0
        if pivot_row != pivot_idx:
            work[pivot_idx], work[pivot_row] = work[pivot_row], work[pivot_idx]
            sign *= -1
        pivot = work[pivot_idx][pivot_idx]
        for row in range(pivot_idx + 1, size):
            for col in range(pivot_idx + 1, size):
                numerator = work[row][col] * pivot
                numerator -= work[row][pivot_idx] * work[pivot_idx][col]
                work[row][col] = numerator // previous
            work[row][pivot_idx] = 0
        previous = pivot
    return sign * work[size - 1][size - 1]


def resultant(left: Sequence[int], right: Sequence[int]) -> int:
    f = trim(left)
    g = trim(right)
    deg_f = degree(f)
    deg_g = degree(g)
    if deg_f < 0 or deg_g < 0:
        return 0
    if deg_f == 0:
        return f[0] ** deg_g
    if deg_g == 0:
        return g[0] ** deg_f

    f_high = list(reversed(f))
    g_high = list(reversed(g))
    size = deg_f + deg_g
    rows: list[list[int]] = []
    for shift in range(deg_g):
        rows.append([0] * shift + f_high + [0] * (deg_g - 1 - shift))
    for shift in range(deg_f):
        rows.append([0] * shift + g_high + [0] * (deg_f - 1 - shift))
    if any(len(row) != size for row in rows):
        raise AssertionError("bad Sylvester matrix dimensions")
    return determinant_bareiss(rows)


def factorint(value: int) -> dict[int, int]:
    remaining = abs(value)
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def euler_phi(value: int) -> int:
    result = value
    for prime in factorint(value):
        result = result // prime * (prime - 1)
    return result


def lcm_int(left: int, right: int) -> int:
    if left == 0 or right == 0:
        return 0
    return abs(left // gcd(left, right) * right)


def resultant_height_bound(order: int, complement_size: int, rank: int) -> int:
    return (2 * comb(complement_size, rank)) ** euler_phi(order)


def exponent_elementary_poly(
    exponents: Sequence[int],
    order: int,
    rank: int,
) -> list[int]:
    coeffs = [0] * order
    for combo in itertools.combinations(exponents, rank):
        coeffs[sum(combo) % order] += 1
    return trim(coeffs)


def exponent_power_sum_poly(
    exponents: Sequence[int],
    order: int,
    rank: int,
) -> list[int]:
    coeffs = [0] * order
    for exponent in exponents:
        coeffs[(rank * exponent) % order] += 1
    return trim(coeffs)


def bad_prime_certificate(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> dict[str, Any]:
    phi = cyclotomic_poly(order)
    gcd_certificate = 0
    rows = []
    for rank in range(1, sigma + 1):
        delta = poly_sub(
            exponent_elementary_poly(left, order, rank),
            exponent_elementary_poly(right, order, rank),
        )
        _, remainder = poly_divmod_monic(delta, phi)
        if not remainder:
            rows.append({
                "rank": rank,
                "cyclotomic_zero": True,
                "resultant": 0,
                "remainder": [],
            })
            continue
        res = abs(resultant(phi, remainder))
        if res == 0:
            raise AssertionError("nonzero cyclotomic remainder has zero resultant")
        height_bound = resultant_height_bound(order, len(left), rank)
        if res > height_bound:
            raise AssertionError("resultant exceeded the trivial norm bound")
        gcd_certificate = res if gcd_certificate == 0 else gcd(gcd_certificate, res)
        rows.append({
            "rank": rank,
            "cyclotomic_zero": False,
            "resultant": res,
            "height_bound": height_bound,
            "remainder": remainder,
        })
    char_zero = gcd_certificate == 0
    split_factors = []
    if not char_zero:
        split_factors = [
            prime for prime in sorted(factorint(gcd_certificate))
            if prime % order == 1
        ]
    active_bounds = [
        row["height_bound"]
        for row in rows
        if not row["cyclotomic_zero"]
    ]
    return {
        "left": list(left),
        "right": list(right),
        "order": order,
        "sigma": sigma,
        "char_zero_collision": char_zero,
        "certificate": gcd_certificate,
        "certificate_factorization": factorint(gcd_certificate),
        "least_active_height_bound": min(active_bounds) if active_bounds else 0,
        "split_prime_factors": split_factors,
        "rows": rows,
    }


def prime_factors(value: int) -> set[int]:
    return set(factorint(value))


def is_prime(value: int) -> bool:
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


def primitive_root(prime: int) -> int:
    if prime == 2:
        return 1
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError(f"no primitive root for {prime}")


def poly_from_roots_mod(roots: Iterable[int], prime: int) -> list[int]:
    coeffs = [1]
    for root in roots:
        out = [0] * (len(coeffs) + 1)
        for idx, coeff in enumerate(coeffs):
            out[idx] = (out[idx] - root * coeff) % prime
            out[idx + 1] = (out[idx + 1] + coeff) % prime
        coeffs = out
    return coeffs


def poly_eval_mod(poly: Sequence[int], value: int, prime: int) -> int:
    total = 0
    for coeff in reversed(poly):
        total = (total * value + coeff) % prime
    return total


def gf9_add(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    return ((left[0] + right[0]) % 3, (left[1] + right[1]) % 3)


def gf9_mul(
    left: tuple[int, int],
    right: tuple[int, int],
) -> tuple[int, int]:
    # F_9 = F_3[i]/(i^2 + 1), so i^2 = -1 = 2.
    return (
        (left[0] * right[0] + 2 * left[1] * right[1]) % 3,
        (left[0] * right[1] + left[1] * right[0]) % 3,
    )


def gf9_pow(value: tuple[int, int], exponent: int) -> tuple[int, int]:
    result = (1, 0)
    for _ in range(exponent):
        result = gf9_mul(result, value)
    return result


def gf9_multiplicative_order(value: tuple[int, int]) -> int:
    if value == (0, 0):
        raise AssertionError("zero has no multiplicative order")
    current = (1, 0)
    for exponent in range(1, 9):
        current = gf9_mul(current, value)
        if current == (1, 0):
            return exponent
    raise AssertionError("bad F_9 multiplicative order")


def exponent_elementary_gf9(
    exponents: Sequence[int],
    order: int,
    rank: int,
    root: tuple[int, int],
) -> tuple[int, int]:
    total = (0, 0)
    for combo in itertools.combinations(exponents, rank):
        total = gf9_add(total, gf9_pow(root, sum(combo) % order))
    return total


def gf9_primitive_order_roots(order: int) -> list[tuple[int, int]]:
    root = (1, 1)
    if gf9_multiplicative_order(root) != order:
        raise AssertionError("bad F_9 primitive root")
    roots = [
        gf9_pow(root, unit)
        for unit in range(1, order)
        if gcd(unit, order) == 1
    ]
    if len(set(roots)) != euler_phi(order):
        raise AssertionError("bad F_9 primitive-root list")
    return roots


def finite_prefix_collision_pairs_gf9(
    *,
    order: int,
    complement_size: int,
    sigma: int,
    root: tuple[int, int],
) -> dict[str, Any]:
    if gf9_multiplicative_order(root) != order:
        raise AssertionError("root must have exact requested order")

    buckets: dict[tuple[tuple[int, int], ...], list[tuple[int, ...]]]
    buckets = defaultdict(list)
    for exponents in itertools.combinations(range(order), complement_size):
        key = tuple(
            exponent_elementary_gf9(exponents, order, rank, root)
            for rank in range(1, sigma + 1)
        )
        buckets[key].append(tuple(exponents))

    pairs = []
    histogram = Counter(len(members) for members in buckets.values())
    for key, members in buckets.items():
        if len(members) <= 1:
            continue
        for left, right in itertools.combinations(members, 2):
            pairs.append({
                "top_sigma_key": [list(value) for value in key],
                "left": list(left),
                "right": list(right),
            })
    return {
        "order": order,
        "complement_size": complement_size,
        "sigma": sigma,
        "root": list(root),
        "fiber_histogram": dict(sorted(histogram.items())),
        "max_fiber": max(histogram) if histogram else 0,
        "collision_pair_count": len(pairs),
        "pairs": pairs,
    }


def top_sigma_key_mod(coeffs: Sequence[int], sigma: int, prime: int) -> tuple[int, ...]:
    size = len(coeffs) - 1
    effective = min(sigma, size)
    return tuple(coeffs[size - idx] % prime for idx in range(1, effective + 1))


def finite_prefix_fiber_summary(
    *,
    prime: int,
    order: int,
    complement_size: int,
    sigma: int,
    root: int | None = None,
) -> dict[str, Any]:
    if (prime - 1) % order != 0:
        raise AssertionError("order must divide prime-1")
    generator = primitive_root(prime)
    h = root if root is not None else pow(generator, (prime - 1) // order, prime)
    has_exact_order = (
        pow(h, order, prime) == 1
        and all(pow(h, d, prime) != 1 for d in range(1, order))
    )
    if not has_exact_order:
        raise AssertionError("constructed element does not have exact order")

    buckets: dict[tuple[int, ...], int] = defaultdict(int)
    for exponents in itertools.combinations(range(order), complement_size):
        roots = [pow(h, exponent, prime) for exponent in exponents]
        key = top_sigma_key_mod(poly_from_roots_mod(roots, prime), sigma, prime)
        buckets[key] += 1

    histogram = Counter(buckets.values())
    collision_pair_count = sum(
        fiber_size * (fiber_size - 1) // 2
        for fiber_size in buckets.values()
    )
    return {
        "prime": prime,
        "order": order,
        "complement_size": complement_size,
        "sigma": sigma,
        "generator": generator,
        "order_generator": h,
        "distinct_prefix_values": len(buckets),
        "fiber_histogram": dict(sorted(histogram.items())),
        "max_fiber": max(histogram) if histogram else 0,
        "collision_pair_count": collision_pair_count,
    }


def finite_prefix_collision_pairs(
    *,
    prime: int,
    order: int,
    complement_size: int,
    sigma: int,
    root: int | None = None,
) -> dict[str, Any]:
    if (prime - 1) % order != 0:
        raise AssertionError("order must divide prime-1")
    generator = primitive_root(prime)
    h = root if root is not None else pow(generator, (prime - 1) // order, prime)
    if pow(h, order, prime) != 1 or any(pow(h, d, prime) == 1 for d in range(1, order)):
        raise AssertionError("constructed element does not have exact order")

    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for exponents in itertools.combinations(range(order), complement_size):
        roots = [pow(h, exponent, prime) for exponent in exponents]
        key = top_sigma_key_mod(poly_from_roots_mod(roots, prime), sigma, prime)
        buckets[key].append(tuple(exponents))

    pairs = []
    histogram = Counter(len(members) for members in buckets.values())
    for key, members in buckets.items():
        if len(members) <= 1:
            continue
        for left, right in itertools.combinations(members, 2):
            pairs.append({
                "top_sigma_key": list(key),
                "left": list(left),
                "right": list(right),
            })
    return {
        "prime": prime,
        "order": order,
        "complement_size": complement_size,
        "sigma": sigma,
        "generator": generator,
        "order_generator": h,
        "fiber_histogram": dict(sorted(histogram.items())),
        "max_fiber": max(histogram) if histogram else 0,
        "collision_pair_count": len(pairs),
        "pairs": pairs,
    }


def check_split_prime_row_accounting() -> dict[str, Any]:
    prime = 17
    order = 16
    complement_size = 6
    sigma = 4
    primitive_roots = primitive_order_roots(prime, order)
    incidence_counter: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
    row_counts_by_root = {}

    for root in primitive_roots:
        row = finite_prefix_collision_pairs(
            prime=prime,
            order=order,
            complement_size=complement_size,
            sigma=sigma,
            root=root,
        )
        row_counts_by_root[root] = row["collision_pair_count"]
        for pair in row["pairs"]:
            key = normalized_pair(pair["left"], pair["right"])
            incidence_counter[key] += 1

    fixed_row_counts = set(row_counts_by_root.values())
    if fixed_row_counts != {40}:
        raise AssertionError(f"unexpected split-root row counts: {row_counts_by_root}")

    degree_distribution: Counter[int] = Counter()
    degree_weighted_sum = 0
    mismatches = []
    orbit_groups: dict[tuple[tuple[int, ...], tuple[int, ...]], list[
        tuple[tuple[int, ...], tuple[int, ...]]
    ]]
    orbit_groups = defaultdict(list)
    for pair, multiplicity in incidence_counter.items():
        common_root_degree = degree(common_root_gcd_mod(
            pair[0],
            pair[1],
            order,
            sigma,
            prime,
        ))
        if common_root_degree != multiplicity:
            mismatches.append({
                "left": list(pair[0]),
                "right": list(pair[1]),
                "incidence_multiplicity": multiplicity,
                "common_root_degree": common_root_degree,
            })
        degree_distribution[common_root_degree] += 1
        degree_weighted_sum += common_root_degree
        orbit_groups[affine_orbit_key(pair[0], pair[1], order)].append(pair)
    if mismatches:
        raise AssertionError(f"row-accounting mismatches: {mismatches[:3]}")

    direct_incidence_sum = sum(incidence_counter.values())
    expected_incidence_sum = len(primitive_roots) * 40
    if direct_incidence_sum != expected_incidence_sum:
        raise AssertionError("bad direct incidence count")
    if degree_weighted_sum != direct_incidence_sum:
        raise AssertionError("gcd-degree sum does not match row incidences")

    orbit_rows = []
    orbit_weighted_sum = 0
    for orbit_key, incident_members in orbit_groups.items():
        orbit_members = affine_orbit_members(orbit_key[0], orbit_key[1], order)
        if set(incident_members) != orbit_members:
            raise AssertionError("incident set is not a full affine orbit")
        orbit_degree = degree(common_root_gcd_mod(
            orbit_key[0],
            orbit_key[1],
            order,
            sigma,
            prime,
        ))
        for member in orbit_members:
            member_degree = degree(common_root_gcd_mod(
                member[0],
                member[1],
                order,
                sigma,
                prime,
            ))
            if member_degree != orbit_degree:
                raise AssertionError("affine orbit has nonconstant gcd degree")
        weighted_degree = len(orbit_members) * orbit_degree
        orbit_weighted_sum += weighted_degree
        orbit_rows.append({
            "orbit_size": len(orbit_members),
            "common_root_degree": orbit_degree,
            "weighted_degree": weighted_degree,
            "representative": [list(orbit_key[0]), list(orbit_key[1])],
        })
    orbit_rows.sort(key=lambda item: (
        item["orbit_size"],
        item["common_root_degree"],
        item["representative"],
    ))
    if orbit_weighted_sum != degree_weighted_sum:
        raise AssertionError("affine orbit quotient changed row mass")

    return {
        "prime": prime,
        "order": order,
        "complement_size": complement_size,
        "sigma": sigma,
        "primitive_root_count": len(primitive_roots),
        "row_counts_by_root": {
            str(root): row_counts_by_root[root]
            for root in sorted(row_counts_by_root)
        },
        "fixed_root_collision_pair_count": next(iter(fixed_row_counts)),
        "incident_template_pair_count": len(incidence_counter),
        "root_template_incidence_sum": direct_incidence_sum,
        "gcd_degree_weighted_sum": degree_weighted_sum,
        "degree_distribution_on_incident_pairs": dict(
            sorted(degree_distribution.items())
        ),
        "affine_orbit_count": len(orbit_rows),
        "affine_orbit_weighted_sum": orbit_weighted_sum,
        "affine_orbits": orbit_rows,
    }


def scaled_subset(subset: Sequence[int], unit: int, order: int) -> tuple[int, ...]:
    return tuple(sorted((unit * value) % order for value in subset))


def translated_subset(subset: Sequence[int], shift: int, order: int) -> tuple[int, ...]:
    return tuple(sorted((value + shift) % order for value in subset))


def affine_subset(
    subset: Sequence[int],
    unit: int,
    shift: int,
    order: int,
) -> tuple[int, ...]:
    return tuple(sorted((unit * value + shift) % order for value in subset))


def affine_orbit_members(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
) -> set[tuple[tuple[int, ...], tuple[int, ...]]]:
    units = [unit for unit in range(1, order) if gcd(unit, order) == 1]
    return {
        normalized_pair(
            affine_subset(left, unit, shift, order),
            affine_subset(right, unit, shift, order),
        )
        for unit in units
        for shift in range(order)
    }


def normalized_pair(
    left: Sequence[int],
    right: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    ordered = sorted((tuple(left), tuple(right)))
    return ordered[0], ordered[1]


def translation_orbit_key(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return min(
        normalized_pair(
            translated_subset(left, shift, order),
            translated_subset(right, shift, order),
        )
        for shift in range(order)
    )


def affine_orbit_key(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return min(affine_orbit_members(left, right, order))


def check_structured_char_zero_example() -> dict[str, Any]:
    report = bad_prime_certificate((0, 2), (1, 3), order=4, sigma=1)
    if not report["char_zero_collision"]:
        raise AssertionError("expected quotient-periodic characteristic-zero collision")
    return {
        "order": 4,
        "left": [0, 2],
        "right": [1, 3],
        "sigma": 1,
        "char_zero_collision": True,
    }


def check_f17_packet() -> dict[str, Any]:
    row = finite_prefix_collision_pairs(
        prime=17,
        order=16,
        complement_size=6,
        sigma=4,
    )
    if row["collision_pair_count"] != 40:
        raise AssertionError("unexpected F_17 collision count")
    if row["max_fiber"] != 2:
        raise AssertionError("unexpected F_17 maximum fiber")

    certificate_counter: Counter[int] = Counter()
    common_root_degree_counter: Counter[int] = Counter()
    embedding_zero_count_counter: Counter[int] = Counter()
    split_factor_sets: Counter[tuple[int, ...]] = Counter()
    aggregate_certificate = 1
    orbit_groups: dict[tuple[tuple[int, ...], tuple[int, ...]], list[dict[str, Any]]]
    orbit_groups = defaultdict(list)
    affine_orbits: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for pair in row["pairs"]:
        certificate = bad_prime_certificate(
            pair["left"],
            pair["right"],
            order=16,
            sigma=4,
        )
        if certificate["char_zero_collision"]:
            raise AssertionError("F_17 aperiodic packet lifted to characteristic zero")
        if certificate["certificate"] % 17 != 0:
            raise AssertionError("F_17 collision certificate is not divisible by 17")
        split_factors = tuple(certificate["split_prime_factors"])
        if split_factors != (17,):
            raise AssertionError(f"unexpected split factors {split_factors}")
        common_root_factor = common_root_gcd_mod(
            pair["left"],
            pair["right"],
            order=16,
            sigma=4,
            prime=17,
        )
        common_root_degree = degree(common_root_factor)
        if common_root_degree <= 0:
            raise AssertionError("actual F_17 collision has no common-root factor")
        zero_roots = primitive_common_zero_roots(
            pair["left"],
            pair["right"],
            order=16,
            sigma=4,
            prime=17,
        )
        if len(zero_roots) != common_root_degree:
            raise AssertionError("common-root degree does not count embeddings")
        common_root_degree_counter[common_root_degree] += 1
        embedding_zero_count_counter[len(zero_roots)] += 1
        certificate_counter[certificate["certificate"]] += 1
        split_factor_sets[split_factors] += 1
        aggregate_certificate = lcm_int(
            aggregate_certificate,
            certificate["certificate"],
        )
        orbit_key = translation_orbit_key(pair["left"], pair["right"], 16)
        orbit_groups[orbit_key].append(pair)
        affine_orbits.add(affine_orbit_key(pair["left"], pair["right"], 16))

    expected = Counter({68: 16, 272: 16, 147_968: 8})
    if certificate_counter != expected:
        raise AssertionError((certificate_counter, expected))
    if aggregate_certificate != 147_968:
        raise AssertionError("unexpected aggregate lcm certificate")
    aggregate_split_factors = [
        prime for prime in sorted(factorint(aggregate_certificate))
        if prime % 16 == 1
    ]
    if aggregate_split_factors != [17]:
        raise AssertionError("unexpected aggregate split-prime support")

    orbit_ledger = []
    for key, members in orbit_groups.items():
        certs = {
            bad_prime_certificate(
                pair["left"],
                pair["right"],
                order=16,
                sigma=4,
            )["certificate"]
            for pair in members
        }
        if len(certs) != 1:
            raise AssertionError("translation orbit has nonconstant certificate")
        orbit_ledger.append({
            "orbit_size": len(members),
            "certificate": next(iter(certs)),
            "representative": [list(key[0]), list(key[1])],
        })
    orbit_ledger.sort(key=lambda item: (item["orbit_size"], item["certificate"]))
    if [(row["orbit_size"], row["certificate"]) for row in orbit_ledger] != [
        (8, 147_968),
        (16, 68),
        (16, 272),
    ]:
        raise AssertionError(f"unexpected orbit ledger: {orbit_ledger}")

    return {
        "prime": 17,
        "order": 16,
        "complement_size": 6,
        "sigma": 4,
        "collision_pair_count": row["collision_pair_count"],
        "max_fiber": row["max_fiber"],
        "fiber_histogram": row["fiber_histogram"],
        "certificate_counts": dict(sorted(certificate_counter.items())),
        "common_root_degree_counts": dict(sorted(common_root_degree_counter.items())),
        "embedding_zero_count_counts": dict(
            sorted(embedding_zero_count_counter.items())
        ),
        "aggregate_lcm_certificate": aggregate_certificate,
        "aggregate_split_prime_factors": aggregate_split_factors,
        "translation_orbits": orbit_ledger,
        "affine_orbit_count": len(affine_orbits),
        "split_factor_sets": {
            ",".join(map(str, key)): value
            for key, value in sorted(split_factor_sets.items())
        },
    }


def primitive_order_roots(prime: int, order: int) -> list[int]:
    generator = primitive_root(prime)
    root = pow(generator, (prime - 1) // order, prime)
    return [
        pow(root, unit, prime)
        for unit in range(1, order)
        if gcd(unit, order) == 1
    ]


def prefix_delta_values_mod(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
    root: int,
    prime: int,
) -> list[int]:
    values = []
    for rank in range(1, sigma + 1):
        delta = poly_sub(
            exponent_elementary_poly(left, order, rank),
            exponent_elementary_poly(right, order, rank),
        )
        values.append(poly_eval_mod(delta, root, prime))
    return values


def primitive_common_zero_roots(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
    prime: int,
) -> list[int]:
    roots = []
    for root in primitive_order_roots(prime, order):
        values = prefix_delta_values_mod(left, right, order, sigma, root, prime)
        if all(value == 0 for value in values):
            roots.append(root)
    return roots


def common_root_gcd_mod(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
    prime: int,
) -> list[int]:
    common = trim_mod(cyclotomic_poly(order), prime)
    for rank in range(1, sigma + 1):
        delta = poly_sub(
            exponent_elementary_poly(left, order, rank),
            exponent_elementary_poly(right, order, rank),
        )
        common = poly_gcd_mod(common, delta, prime)
        if degree(common) <= 0:
            break
    return common


def power_common_root_gcd_mod(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
    prime: int,
) -> list[int]:
    common = trim_mod(cyclotomic_poly(order), prime)
    for rank in range(1, sigma + 1):
        delta = poly_sub(
            exponent_power_sum_poly(left, order, rank),
            exponent_power_sum_poly(right, order, rank),
        )
        common = poly_gcd_mod(common, delta, prime)
        if degree(common) <= 0:
            break
    return common


def check_newton_power_sum_bridge() -> dict[str, Any]:
    order = 16
    prime = 17
    sigma = 4
    row = finite_prefix_collision_pairs(
        prime=prime,
        order=order,
        complement_size=6,
        sigma=sigma,
    )
    degree_counter: Counter[int] = Counter()
    for pair in row["pairs"]:
        elementary_factor = common_root_gcd_mod(
            pair["left"],
            pair["right"],
            order,
            sigma,
            prime,
        )
        power_factor = power_common_root_gcd_mod(
            pair["left"],
            pair["right"],
            order,
            sigma,
            prime,
        )
        if elementary_factor != power_factor:
            raise AssertionError("Newton bridge changed the F_17 common factor")
        degree_counter[degree(elementary_factor)] += 1

    false_positive_left = (0, 1, 2, 7, 9, 13)
    false_positive_right = (0, 1, 2, 3, 4, 11)
    elementary_false_positive = common_root_gcd_mod(
        false_positive_left,
        false_positive_right,
        order,
        sigma,
        97,
    )
    power_false_positive = power_common_root_gcd_mod(
        false_positive_left,
        false_positive_right,
        order,
        sigma,
        97,
    )
    if elementary_false_positive != power_false_positive:
        raise AssertionError("Newton bridge changed the p=97 false positive")

    depth_left = (0, 1, 2, 3, 4, 14)
    depth_right = (5, 6, 7, 9, 12, 15)
    depth_rows = []
    for depth_sigma in range(1, 7):
        elementary_factor = common_root_gcd_mod(
            depth_left,
            depth_right,
            order,
            depth_sigma,
            prime,
        )
        power_factor = power_common_root_gcd_mod(
            depth_left,
            depth_right,
            order,
            depth_sigma,
            prime,
        )
        if elementary_factor != power_factor:
            raise AssertionError("Newton bridge changed a depth-filtration row")
        depth_rows.append({
            "sigma": depth_sigma,
            "common_root_degree": degree(elementary_factor),
            "common_root_factor": elementary_factor,
        })

    return {
        "status": "PASS",
        "condition": "p does not divide sigma!",
        "f17_packet_pairs_checked": row["collision_pair_count"],
        "f17_degree_counts": dict(sorted(degree_counter.items())),
        "p97_false_positive_degree": degree(elementary_false_positive),
        "depth_representative": {
            "left": list(depth_left),
            "right": list(depth_right),
            "rows": depth_rows,
        },
    }


def check_extension_field_bad_prime_certificate() -> dict[str, Any]:
    characteristic = 3
    extension_degree = 2
    order = 8
    sigma = 1
    root = (1, 1)
    left = (0, 1)
    right = (2, 5)
    if (characteristic - 1) % order == 0:
        raise AssertionError("test prime unexpectedly split")
    if (characteristic ** extension_degree - 1) % order != 0:
        raise AssertionError("extension field cannot contain the requested root")
    if gf9_multiplicative_order(root) != order:
        raise AssertionError("chosen F_9 element is not primitive of order 8")

    left_value = exponent_elementary_gf9(left, order, sigma, root)
    right_value = exponent_elementary_gf9(right, order, sigma, root)
    if left_value != right_value:
        raise AssertionError("expected F_9 prefix collision")

    certificate = bad_prime_certificate(left, right, order, sigma)
    if certificate["char_zero_collision"]:
        raise AssertionError("F_9 witness lifted to characteristic zero")
    if certificate["certificate"] != 36:
        raise AssertionError("unexpected F_9 witness certificate")
    if certificate["certificate"] % characteristic != 0:
        raise AssertionError("extension-field bad prime did not divide certificate")
    if certificate["split_prime_factors"]:
        raise AssertionError("non-split prime appeared in split-prime support")

    common_factor = common_root_gcd_mod(
        left,
        right,
        order,
        sigma,
        characteristic,
    )
    if degree(common_factor) != extension_degree:
        raise AssertionError("expected one quadratic prime-ideal factor over F_3")

    return {
        "base_prime": characteristic,
        "extension_degree": extension_degree,
        "field": "F_9 = F_3[i]/(i^2+1)",
        "order": order,
        "sigma": sigma,
        "root": list(root),
        "left": list(left),
        "right": list(right),
        "prefix_value": list(left_value),
        "certificate": certificate["certificate"],
        "certificate_factorization": certificate["certificate_factorization"],
        "split_prime_factors": certificate["split_prime_factors"],
        "common_factor_mod_3": common_factor,
        "common_factor_degree_mod_3": degree(common_factor),
    }


def check_extension_field_row_accounting() -> dict[str, Any]:
    characteristic = 3
    extension_degree = 2
    order = 8
    complement_size = 2
    sigma = 1
    primitive_roots = gf9_primitive_order_roots(order)
    incidence_counter: Counter[tuple[tuple[int, ...], tuple[int, ...]]] = Counter()
    row_counts_by_root = {}

    for root in primitive_roots:
        row = finite_prefix_collision_pairs_gf9(
            order=order,
            complement_size=complement_size,
            sigma=sigma,
            root=root,
        )
        if row["collision_pair_count"] != 30:
            raise AssertionError("unexpected F_9 row count")
        if row["max_fiber"] != 4:
            raise AssertionError("unexpected F_9 max fiber")
        row_counts_by_root[tuple(root)] = row["collision_pair_count"]
        for pair in row["pairs"]:
            key = normalized_pair(pair["left"], pair["right"])
            incidence_counter[key] += 1

    degree_distribution: Counter[int] = Counter()
    char_zero_distribution: Counter[int] = Counter()
    degree_weighted_sum = 0
    non_char_zero_pairs = 0
    non_char_zero_degree_sum = 0
    for pair, multiplicity in incidence_counter.items():
        common_factor = common_root_gcd_mod(
            pair[0],
            pair[1],
            order,
            sigma,
            characteristic,
        )
        common_degree = degree(common_factor)
        if common_degree != multiplicity:
            raise AssertionError("F_9 row incidence differs from gcd degree")
        certificate = bad_prime_certificate(pair[0], pair[1], order, sigma)
        degree_distribution[common_degree] += 1
        degree_weighted_sum += common_degree
        if certificate["char_zero_collision"]:
            char_zero_distribution[common_degree] += 1
        else:
            if certificate["certificate"] % characteristic != 0:
                raise AssertionError("F_9 bad-prime pair missed the certificate")
            non_char_zero_pairs += 1
            non_char_zero_degree_sum += common_degree

    incidence_sum = sum(incidence_counter.values())
    expected_incidence_sum = len(primitive_roots) * 30
    if incidence_sum != expected_incidence_sum:
        raise AssertionError("bad F_9 incidence count")
    if degree_weighted_sum != incidence_sum:
        raise AssertionError("bad F_9 degree-weighted row accounting")
    if dict(degree_distribution) != {2: 48, 4: 6}:
        raise AssertionError("unexpected F_9 degree distribution")
    if dict(char_zero_distribution) != {4: 6}:
        raise AssertionError("unexpected F_9 characteristic-zero distribution")

    return {
        "base_prime": characteristic,
        "extension_degree": extension_degree,
        "field": "F_9 = F_3[i]/(i^2+1)",
        "order": order,
        "complement_size": complement_size,
        "sigma": sigma,
        "primitive_root_count": len(primitive_roots),
        "row_counts_by_root": {
            str(root): row_counts_by_root[root]
            for root in sorted(row_counts_by_root)
        },
        "fixed_root_collision_pair_count": 30,
        "incident_template_pair_count": len(incidence_counter),
        "root_template_incidence_sum": incidence_sum,
        "gcd_degree_weighted_sum": degree_weighted_sum,
        "degree_distribution_on_incident_pairs": dict(
            sorted(degree_distribution.items())
        ),
        "char_zero_degree_distribution": dict(
            sorted(char_zero_distribution.items())
        ),
        "non_char_zero_pair_count": non_char_zero_pairs,
        "non_char_zero_degree_sum": non_char_zero_degree_sum,
    }


def check_prefix_depth_filtration() -> dict[str, Any]:
    prime = 17
    order = 16
    complement_size = 6
    max_sigma = 6
    expected_rows = {
        1: {
            "distinct_prefix_values": 17,
            "max_fiber": 472,
            "collision_pair_count": 1_882_116,
            "fiber_histogram": {471: 16, 472: 1},
        },
        2: {
            "distinct_prefix_values": 289,
            "max_fiber": 32,
            "collision_pair_count": 107_352,
            "fiber_histogram": {
                25: 16,
                26: 72,
                27: 48,
                28: 64,
                29: 56,
                31: 32,
                32: 1,
            },
        },
        3: {
            "distinct_prefix_values": 4_480,
            "max_fiber": 5,
            "collision_pair_count": 4_480,
            "fiber_histogram": {1: 1_824, 2: 1_856, 3: 736, 4: 56, 5: 8},
        },
        4: {
            "distinct_prefix_values": 7_968,
            "max_fiber": 2,
            "collision_pair_count": 40,
            "fiber_histogram": {1: 7_928, 2: 40},
        },
        5: {
            "distinct_prefix_values": 8_008,
            "max_fiber": 1,
            "collision_pair_count": 0,
            "fiber_histogram": {1: 8_008},
        },
        6: {
            "distinct_prefix_values": 8_008,
            "max_fiber": 1,
            "collision_pair_count": 0,
            "fiber_histogram": {1: 8_008},
        },
    }

    rows = []
    previous_pair_count = None
    previous_max_fiber = None
    for sigma in range(1, max_sigma + 1):
        summary = finite_prefix_fiber_summary(
            prime=prime,
            order=order,
            complement_size=complement_size,
            sigma=sigma,
        )
        expected = expected_rows[sigma]
        for key, value in expected.items():
            if summary[key] != value:
                raise AssertionError((sigma, key, summary[key], value))
        if (
            previous_pair_count is not None
            and summary["collision_pair_count"] > previous_pair_count
        ):
            raise AssertionError("collision pair count increased with sigma")
        if (
            previous_max_fiber is not None
            and summary["max_fiber"] > previous_max_fiber
        ):
            raise AssertionError("max fiber increased with sigma")
        previous_pair_count = summary["collision_pair_count"]
        previous_max_fiber = summary["max_fiber"]
        rows.append({
            "sigma": sigma,
            "distinct_prefix_values": summary["distinct_prefix_values"],
            "max_fiber": summary["max_fiber"],
            "collision_pair_count": summary["collision_pair_count"],
            "fiber_histogram": summary["fiber_histogram"],
        })

    left = (0, 1, 2, 3, 4, 14)
    right = (5, 6, 7, 9, 12, 15)
    expected_template_rows = [
        {"sigma": 1, "certificate": 2_312, "degree": 2, "split_factors": [17]},
        {"sigma": 2, "certificate": 68, "degree": 1, "split_factors": [17]},
        {"sigma": 3, "certificate": 68, "degree": 1, "split_factors": [17]},
        {"sigma": 4, "certificate": 68, "degree": 1, "split_factors": [17]},
        {"sigma": 5, "certificate": 4, "degree": 0, "split_factors": []},
        {"sigma": 6, "certificate": 4, "degree": 0, "split_factors": []},
    ]
    template_rows = []
    previous_certificate = None
    previous_degree = None
    for expected in expected_template_rows:
        sigma = expected["sigma"]
        certificate = bad_prime_certificate(left, right, order, sigma)
        degree_at_prime = degree(common_root_gcd_mod(
            left,
            right,
            order,
            sigma,
            prime,
        ))
        if certificate["certificate"] != expected["certificate"]:
            raise AssertionError("unexpected depth-filtration certificate")
        if degree_at_prime != expected["degree"]:
            raise AssertionError("unexpected depth-filtration gcd degree")
        if certificate["split_prime_factors"] != expected["split_factors"]:
            raise AssertionError("unexpected depth-filtration split factors")
        if (
            previous_certificate is not None
            and previous_certificate % certificate["certificate"] != 0
        ):
            raise AssertionError("certificate did not divide previous depth")
        if previous_degree is not None and degree_at_prime > previous_degree:
            raise AssertionError("gcd degree increased with sigma")
        previous_certificate = certificate["certificate"]
        previous_degree = degree_at_prime
        template_rows.append({
            "sigma": sigma,
            "certificate": certificate["certificate"],
            "split_prime_factors": certificate["split_prime_factors"],
            "common_root_degree_at_17": degree_at_prime,
        })

    return {
        "prime": prime,
        "order": order,
        "complement_size": complement_size,
        "max_sigma": max_sigma,
        "row_profile": rows,
        "template": {
            "left": list(left),
            "right": list(right),
            "filtration": template_rows,
        },
    }


def check_full_prefix_rigidity() -> dict[str, Any]:
    order = 16
    primes = [17, 97]
    max_complement_size = 8
    rows = []
    for prime in primes:
        for complement_size in range(1, max_complement_size + 1):
            summary = finite_prefix_fiber_summary(
                prime=prime,
                order=order,
                complement_size=complement_size,
                sigma=complement_size,
            )
            expected_count = comb(order, complement_size)
            expected_histogram = {1: expected_count}
            if summary["distinct_prefix_values"] != expected_count:
                raise AssertionError("full-prefix map lost a locator subset")
            if summary["max_fiber"] != 1:
                raise AssertionError("full-prefix map has a nontrivial fiber")
            if summary["collision_pair_count"] != 0:
                raise AssertionError("full-prefix map has a collision")
            if summary["fiber_histogram"] != expected_histogram:
                raise AssertionError("unexpected full-prefix histogram")
            rows.append({
                "prime": prime,
                "order": order,
                "complement_size": complement_size,
                "sigma": complement_size,
                "distinct_prefix_values": summary["distinct_prefix_values"],
                "max_fiber": summary["max_fiber"],
                "collision_pair_count": summary["collision_pair_count"],
            })
    return {
        "order": order,
        "primes_checked": primes,
        "max_complement_size": max_complement_size,
        "rows": rows,
    }


def check_split_prime_sweep() -> list[dict[str, Any]]:
    rows = []
    expected_counts = {17: 40, 97: 0, 113: 0, 193: 0}
    for prime, expected_count in expected_counts.items():
        row = finite_prefix_collision_pairs(
            prime=prime,
            order=16,
            complement_size=6,
            sigma=4,
        )
        if row["collision_pair_count"] != expected_count:
            raise AssertionError((prime, row["collision_pair_count"], expected_count))
        failures = 0
        for pair in row["pairs"]:
            certificate = bad_prime_certificate(
                pair["left"],
                pair["right"],
                order=16,
                sigma=4,
            )
            if (
                not certificate["char_zero_collision"]
                and certificate["certificate"] % prime != 0
            ):
                failures += 1
        if failures:
            raise AssertionError(f"{failures} certificate failures for p={prime}")
        rows.append({
            "prime": prime,
            "collision_pair_count": row["collision_pair_count"],
            "max_fiber": row["max_fiber"],
            "certificate_failures": failures,
        })
    return rows


def check_bounded_split_prime_row_scan() -> dict[str, Any]:
    rows = []
    nonzero_rows = []
    for prime in range(17, BOUNDED_SPLIT_PRIME_SCAN_LIMIT + 1):
        if prime % 16 != 1 or not is_prime(prime):
            continue
        row = finite_prefix_collision_pairs(
            prime=prime,
            order=16,
            complement_size=6,
            sigma=4,
        )
        entry = {
            "prime": prime,
            "collision_pair_count": row["collision_pair_count"],
            "max_fiber": row["max_fiber"],
        }
        rows.append(entry)
        if row["collision_pair_count"]:
            nonzero_rows.append(entry)
    expected = [{"prime": 17, "collision_pair_count": 40, "max_fiber": 2}]
    if nonzero_rows != expected:
        raise AssertionError(f"unexpected bounded split-prime scan: {nonzero_rows}")
    return {
        "prime_bound": BOUNDED_SPLIT_PRIME_SCAN_LIMIT,
        "split_primes_checked": len(rows),
        "nonzero_collision_rows": nonzero_rows,
    }


def check_prime_ideal_false_positive() -> dict[str, Any]:
    left = (0, 1, 2, 7, 9, 13)
    right = (0, 1, 2, 3, 4, 11)
    order = 16
    sigma = 4
    prime = 97
    certificate = bad_prime_certificate(left, right, order=order, sigma=sigma)
    if certificate["certificate"] != 194:
        raise AssertionError("unexpected false-positive certificate")
    if certificate["split_prime_factors"] != [prime]:
        raise AssertionError("expected 97 as rational split certificate factor")
    common_root_factor = common_root_gcd_mod(left, right, order, sigma, prime)
    if degree(common_root_factor) > 0:
        raise AssertionError("false positive has a nontrivial common-root factor")
    zero_roots = primitive_common_zero_roots(left, right, order, sigma, prime)
    if len(zero_roots) != degree(common_root_factor):
        raise AssertionError("false-positive gcd degree does not count embeddings")

    profile = []
    any_collision = False
    for root in primitive_order_roots(prime, order):
        values = prefix_delta_values_mod(
            left,
            right,
            order,
            sigma,
            root,
            prime,
        )
        all_zero = all(value == 0 for value in values)
        any_collision = any_collision or all_zero
        profile.append({
            "root": root,
            "delta_values": values,
            "all_zero": all_zero,
        })
    if any_collision:
        raise AssertionError("rational false positive became an ideal collision")
    return {
        "left": list(left),
        "right": list(right),
        "order": order,
        "sigma": sigma,
        "prime": prime,
        "certificate": certificate["certificate"],
        "certificate_factorization": certificate["certificate_factorization"],
        "common_root_factor_mod_p": common_root_factor,
        "common_root_degree": degree(common_root_factor),
        "embedding_zero_count": len(zero_roots),
        "primitive_root_checks": profile,
        "actual_collision_for_any_embedding": any_collision,
    }


def check_galois_invariance() -> dict[str, Any]:
    left = (0, 1, 2, 12, 14, 15)
    right = (3, 4, 5, 7, 10, 13)
    base = bad_prime_certificate(left, right, order=16, sigma=4)
    units = [unit for unit in range(1, 16) if gcd(unit, 16) == 1]
    certificates = []
    for unit in units:
        scaled = bad_prime_certificate(
            scaled_subset(left, unit, 16),
            scaled_subset(right, unit, 16),
            order=16,
            sigma=4,
        )
        certificates.append(scaled["certificate"])
        if scaled["certificate"] != base["certificate"]:
            raise AssertionError("certificate changed under dilation")
    return {
        "base_certificate": base["certificate"],
        "units_checked": units,
        "certificates": certificates,
    }


def check_affine_invariance() -> dict[str, Any]:
    order = 16
    sigma = 4
    units = [unit for unit in range(1, order) if gcd(unit, order) == 1]
    templates = [
        {
            "name": "f17_collision",
            "left": (0, 1, 2, 12, 14, 15),
            "right": (3, 4, 5, 7, 10, 13),
            "prime": 17,
            "base_certificate": 68,
            "base_gcd_degree": 1,
        },
        {
            "name": "p97_rational_false_positive",
            "left": (0, 1, 2, 7, 9, 13),
            "right": (0, 1, 2, 3, 4, 11),
            "prime": 97,
            "base_certificate": 194,
            "base_gcd_degree": 0,
        },
    ]
    rows = []
    for template in templates:
        base = bad_prime_certificate(
            template["left"],
            template["right"],
            order=order,
            sigma=sigma,
        )
        base_degree = degree(common_root_gcd_mod(
            template["left"],
            template["right"],
            order,
            sigma,
            template["prime"],
        ))
        if base["certificate"] != template["base_certificate"]:
            raise AssertionError("bad affine-invariance base certificate")
        if base_degree != template["base_gcd_degree"]:
            raise AssertionError("bad affine-invariance base gcd degree")

        checked = 0
        for unit in units:
            for shift in range(order):
                left = affine_subset(template["left"], unit, shift, order)
                right = affine_subset(template["right"], unit, shift, order)
                transformed = bad_prime_certificate(left, right, order, sigma)
                transformed_degree = degree(common_root_gcd_mod(
                    left,
                    right,
                    order,
                    sigma,
                    template["prime"],
                ))
                if transformed["certificate"] != base["certificate"]:
                    raise AssertionError("certificate changed under affine action")
                if transformed_degree != base_degree:
                    raise AssertionError("gcd degree changed under affine action")
                checked += 1
        rows.append({
            "name": template["name"],
            "prime": template["prime"],
            "certificate": base["certificate"],
            "common_root_degree": base_degree,
            "affine_transforms_checked": checked,
        })
    return {
        "order": order,
        "sigma": sigma,
        "unit_count": len(units),
        "shift_count": order,
        "templates": rows,
    }


def build_report() -> dict[str, Any]:
    return {
        "status": "PASS",
        "proof_status": STATUS,
        "theorem_problem_id": "L1 prefix bad-prime certificate",
        "structured_char_zero_example": check_structured_char_zero_example(),
        "f17_packet": check_f17_packet(),
        "split_prime_row_accounting": check_split_prime_row_accounting(),
        "newton_power_sum_bridge": check_newton_power_sum_bridge(),
        "extension_field_bad_prime_certificate": (
            check_extension_field_bad_prime_certificate()
        ),
        "extension_field_row_accounting": check_extension_field_row_accounting(),
        "prefix_depth_filtration": check_prefix_depth_filtration(),
        "full_prefix_rigidity": check_full_prefix_rigidity(),
        "split_prime_sweep": check_split_prime_sweep(),
        "bounded_split_prime_row_scan": check_bounded_split_prime_row_scan(),
        "prime_ideal_false_positive": check_prime_ideal_false_positive(),
        "galois_invariance": check_galois_invariance(),
        "affine_invariance": check_affine_invariance(),
        "nonmutating": True,
        "remaining_open_problem": (
            "aggregate the bad-prime certificates over robustly aperiodic "
            "templates"
        ),
    }


def print_human(report: dict[str, Any]) -> None:
    packet = report["f17_packet"]
    print("l1_prefix_bad_prime_certificate: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "f17_packet="
        f"pairs={packet['collision_pair_count']}, "
        f"max_fiber={packet['max_fiber']}, "
        f"certificates={packet['certificate_counts']}, "
        f"gcd_degrees={packet['common_root_degree_counts']}, "
        f"embedding_counts={packet['embedding_zero_count_counts']}"
    )
    sweep = ", ".join(
        f"p={row['prime']}:pairs={row['collision_pair_count']}"
        for row in report["split_prime_sweep"]
    )
    print(f"split_prime_sweep={sweep}")
    bounded = report["bounded_split_prime_row_scan"]
    print(
        "bounded_split_prime_scan="
        f"p<={bounded['prime_bound']}, checked={bounded['split_primes_checked']}, "
        f"nonzero={bounded['nonzero_collision_rows']}"
    )
    print(f"aggregate_lcm={packet['aggregate_lcm_certificate']}")
    print(f"translation_orbits={len(packet['translation_orbits'])}")
    print(f"affine_orbits={packet['affine_orbit_count']}")
    extension = report["extension_field_bad_prime_certificate"]
    print(
        "extension_field_certificate="
        f"p={extension['base_prime']}, "
        f"degree={extension['extension_degree']}, "
        f"cert={extension['certificate']}, "
        f"gcd_degree={extension['common_factor_degree_mod_3']}"
    )
    extension_accounting = report["extension_field_row_accounting"]
    print(
        "extension_row_accounting="
        f"p={extension_accounting['base_prime']}, "
        f"roots={extension_accounting['primitive_root_count']}, "
        f"fixed_pairs={extension_accounting['fixed_root_collision_pair_count']}, "
        f"incidence_sum={extension_accounting['root_template_incidence_sum']}, "
        f"gcd_degree_sum={extension_accounting['gcd_degree_weighted_sum']}"
    )
    bridge = report["newton_power_sum_bridge"]
    print(
        "newton_power_sum_bridge="
        f"f17_pairs={bridge['f17_packet_pairs_checked']}, "
        f"degrees={bridge['f17_degree_counts']}, "
        f"p97_degree={bridge['p97_false_positive_degree']}"
    )
    filtration = report["prefix_depth_filtration"]
    depth_pairs = {
        row["sigma"]: row["collision_pair_count"]
        for row in filtration["row_profile"]
    }
    print(f"prefix_depth_pairs={depth_pairs}")
    full_prefix = report["full_prefix_rigidity"]
    print(
        "full_prefix_rigidity="
        f"primes={full_prefix['primes_checked']}, "
        f"m<={full_prefix['max_complement_size']}, "
        "collisions=0"
    )
    accounting = report["split_prime_row_accounting"]
    print(
        "row_accounting="
        f"p={accounting['prime']}, "
        f"roots={accounting['primitive_root_count']}, "
        f"fixed_pairs={accounting['fixed_root_collision_pair_count']}, "
        f"incident_pairs={accounting['incident_template_pair_count']}, "
        f"incidence_sum={accounting['root_template_incidence_sum']}, "
        f"gcd_degree_sum={accounting['gcd_degree_weighted_sum']}, "
        f"affine_orbits={accounting['affine_orbit_count']}, "
        f"orbit_sum={accounting['affine_orbit_weighted_sum']}"
    )
    false_positive = report["prime_ideal_false_positive"]
    print(
        "false_positive="
        f"p={false_positive['prime']}, cert={false_positive['certificate']}, "
        f"gcd_degree={false_positive['common_root_degree']}, "
        f"embedding_count={false_positive['embedding_zero_count']}, "
        f"actual={false_positive['actual_collision_for_any_embedding']}"
    )
    affine = report["affine_invariance"]
    print(
        "affine_invariance="
        f"templates={len(affine['templates'])}, "
        f"transforms={affine['templates'][0]['affine_transforms_checked']}"
    )
    print(f"galois_certificate={report['galois_invariance']['base_certificate']}")
    print(f"remaining_open_problem={report['remaining_open_problem']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the L1 prefix bad-prime certificate theorem."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
