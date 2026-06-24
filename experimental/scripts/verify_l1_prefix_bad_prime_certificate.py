#!/usr/bin/env python3
"""Verify the L1 prefix bad-prime certificate theorem.

The theorem checked here is templatewise:

    finite-field prefix collision for a split prime p
      -> characteristic-zero collision
         or p divides a cyclotomic resultant certificate.

This script is intentionally small and nonmutating.  It does not prove the
missing L1 bad-prime aggregation theorem.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from math import comb, gcd
from typing import Any, Iterable, Sequence


STATUS = "PROVED / FINITE-FIELD REDUCTION / NOT A FULL AGGREGATION BOUND"


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


def top_sigma_key_mod(coeffs: Sequence[int], sigma: int, prime: int) -> tuple[int, ...]:
    size = len(coeffs) - 1
    effective = min(sigma, size)
    return tuple(coeffs[size - idx] % prime for idx in range(1, effective + 1))


def finite_prefix_collision_pairs(
    *,
    prime: int,
    order: int,
    complement_size: int,
    sigma: int,
) -> dict[str, Any]:
    if (prime - 1) % order != 0:
        raise AssertionError("order must divide prime-1")
    generator = primitive_root(prime)
    h = pow(generator, (prime - 1) // order, prime)
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


def scaled_subset(subset: Sequence[int], unit: int, order: int) -> tuple[int, ...]:
    return tuple(sorted((unit * value) % order for value in subset))


def translated_subset(subset: Sequence[int], shift: int, order: int) -> tuple[int, ...]:
    return tuple(sorted((value + shift) % order for value in subset))


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
    split_factor_sets: Counter[tuple[int, ...]] = Counter()
    aggregate_certificate = 1
    orbit_groups: dict[tuple[tuple[int, ...], tuple[int, ...]], list[dict[str, Any]]]
    orbit_groups = defaultdict(list)
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
        certificate_counter[certificate["certificate"]] += 1
        split_factor_sets[split_factors] += 1
        aggregate_certificate = lcm_int(aggregate_certificate, certificate["certificate"])
        orbit_groups[translation_orbit_key(pair["left"], pair["right"], 16)].append(pair)

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
        "aggregate_lcm_certificate": aggregate_certificate,
        "aggregate_split_prime_factors": aggregate_split_factors,
        "translation_orbits": orbit_ledger,
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


def build_report() -> dict[str, Any]:
    return {
        "status": "PASS",
        "proof_status": STATUS,
        "theorem_problem_id": "L1 prefix bad-prime certificate",
        "structured_char_zero_example": check_structured_char_zero_example(),
        "f17_packet": check_f17_packet(),
        "split_prime_sweep": check_split_prime_sweep(),
        "prime_ideal_false_positive": check_prime_ideal_false_positive(),
        "galois_invariance": check_galois_invariance(),
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
        f"certificates={packet['certificate_counts']}"
    )
    sweep = ", ".join(
        f"p={row['prime']}:pairs={row['collision_pair_count']}"
        for row in report["split_prime_sweep"]
    )
    print(f"split_prime_sweep={sweep}")
    print(f"aggregate_lcm={packet['aggregate_lcm_certificate']}")
    print(f"translation_orbits={len(packet['translation_orbits'])}")
    false_positive = report["prime_ideal_false_positive"]
    print(
        "false_positive="
        f"p={false_positive['prime']}, cert={false_positive['certificate']}, "
        f"actual={false_positive['actual_collision_for_any_embedding']}"
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
