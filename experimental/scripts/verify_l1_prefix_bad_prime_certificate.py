#!/usr/bin/env python3
"""Verify the L1 prefix bad-prime certificate theorem.

The first theorem checked here is templatewise:

    finite-field prefix collision in characteristic p, with p not dividing n,
      -> characteristic-zero collision
         or p divides a cyclotomic resultant certificate.

This script is intentionally small and nonmutating.  It does not prove the
missing L1 bad-prime aggregation theorem.

It also checks split and nonsplit row-accounting identities, exact common-ideal
valuation budgets, and the finite-field row/fiber bound obtained from those
budgets after characteristic-zero pairs are separated.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from math import comb, factorial, gcd, isqrt
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


def radical_part(value: int) -> int:
    result = 1
    for prime in factorint(value):
        result *= prime
    return result


def part_away_from_order(value: int, order: int) -> int:
    result = 1
    for prime, exponent in factorint(value).items():
        if order % prime != 0:
            result *= prime ** exponent
    return result


def resultant_height_bound(order: int, complement_size: int, rank: int) -> int:
    return (2 * comb(complement_size, rank)) ** euler_phi(order)


def pad_poly(poly: Sequence[int], size: int) -> list[int]:
    if len(poly) > size:
        raise AssertionError("polynomial does not fit requested size")
    return list(poly) + [0] * (size - len(poly))


def multiplication_matrix_mod_cyclotomic(
    multiplier: Sequence[int],
    order: int,
) -> list[list[int]]:
    phi = cyclotomic_poly(order)
    dimension = degree(phi)
    columns = []
    for shift in range(dimension):
        _, remainder = poly_divmod_monic([0] * shift + list(multiplier), phi)
        columns.append(pad_poly(remainder, dimension))
    return [
        [columns[col][row] for col in range(dimension)]
        for row in range(dimension)
    ]


def common_ideal_matrix(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> list[list[int]]:
    phi = cyclotomic_poly(order)
    dimension = degree(phi)
    blocks = []
    for rank in range(1, sigma + 1):
        delta = poly_sub(
            exponent_elementary_poly(left, order, rank),
            exponent_elementary_poly(right, order, rank),
        )
        _, remainder = poly_divmod_monic(delta, phi)
        if remainder:
            blocks.append(multiplication_matrix_mod_cyclotomic(remainder, order))
    if not blocks:
        return []
    return [
        [entry for block in blocks for entry in block[row]]
        for row in range(dimension)
    ]


def swap_matrix_columns(matrix: list[list[int]], left: int, right: int) -> None:
    if left == right:
        return
    for row in matrix:
        row[left], row[right] = row[right], row[left]


def integer_diagonal_entries(matrix: Sequence[Sequence[int]]) -> list[int]:
    """Diagonalize an integer matrix by Euclidean row/column operations."""
    work = [list(row) for row in matrix]
    row_count = len(work)
    col_count = len(work[0]) if row_count else 0
    row_idx = 0
    col_idx = 0
    diagonal = []
    steps = 0
    while row_idx < row_count and col_idx < col_count:
        pivot = None
        best_abs = None
        for r_idx in range(row_idx, row_count):
            for c_idx in range(col_idx, col_count):
                value = abs(work[r_idx][c_idx])
                if value and (best_abs is None or value < best_abs):
                    pivot = (r_idx, c_idx)
                    best_abs = value
        if pivot is None:
            break

        work[row_idx], work[pivot[0]] = work[pivot[0]], work[row_idx]
        swap_matrix_columns(work, col_idx, pivot[1])

        while True:
            steps += 1
            if steps > 100_000:
                raise AssertionError("integer diagonalization did not terminate")
            pivot_value = work[row_idx][col_idx]
            if pivot_value < 0:
                work[row_idx] = [-entry for entry in work[row_idx]]
                pivot_value = -pivot_value

            changed = False
            for r_idx in range(row_count):
                if r_idx == row_idx or work[r_idx][col_idx] == 0:
                    continue
                quotient = work[r_idx][col_idx] // pivot_value
                work[r_idx] = [
                    entry - quotient * pivot_entry
                    for entry, pivot_entry in zip(work[r_idx], work[row_idx])
                ]
                if 0 < abs(work[r_idx][col_idx]) < pivot_value:
                    work[row_idx], work[r_idx] = work[r_idx], work[row_idx]
                    changed = True
                    break
            if changed:
                continue

            pivot_value = work[row_idx][col_idx]
            if pivot_value < 0:
                work[row_idx] = [-entry for entry in work[row_idx]]
                pivot_value = -pivot_value

            for c_idx in range(col_count):
                if c_idx == col_idx or work[row_idx][c_idx] == 0:
                    continue
                quotient = work[row_idx][c_idx] // pivot_value
                for r_idx in range(row_count):
                    work[r_idx][c_idx] -= quotient * work[r_idx][col_idx]
                if 0 < abs(work[row_idx][c_idx]) < pivot_value:
                    swap_matrix_columns(work, col_idx, c_idx)
                    changed = True
                    break
            if changed:
                continue

            column_clear = all(
                work[r_idx][col_idx] == 0
                for r_idx in range(row_count)
                if r_idx != row_idx
            )
            row_clear = all(
                work[row_idx][c_idx] == 0
                for c_idx in range(col_count)
                if c_idx != col_idx
            )
            if column_clear and row_clear:
                break

        if work[row_idx][col_idx] < 0:
            work[row_idx] = [-entry for entry in work[row_idx]]
        diagonal.append(abs(work[row_idx][col_idx]))
        row_idx += 1
        col_idx += 1
    return diagonal


def common_ideal_index(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> dict[str, Any]:
    matrix = common_ideal_matrix(left, right, order, sigma)
    dimension = degree(cyclotomic_poly(order))
    if not matrix:
        return {
            "char_zero_collision": True,
            "rank": 0,
            "dimension": dimension,
            "index": 0,
            "factorization": {},
            "diagonal_entries": [],
        }
    diagonal = integer_diagonal_entries(matrix)
    rank = len(diagonal)
    index = 0
    if rank == dimension:
        index = 1
        for entry in diagonal:
            index *= entry
    return {
        "char_zero_collision": False,
        "rank": rank,
        "dimension": dimension,
        "index": index,
        "factorization": factorint(index),
        "diagonal_entries": diagonal,
    }


def with_radical_incidence_index(common_ideal: dict[str, Any]) -> dict[str, Any]:
    if (
        common_ideal["char_zero_collision"]
        or common_ideal["rank"] != common_ideal["dimension"]
    ):
        return {
            **common_ideal,
            "radical_incidence_index": 0,
            "radical_incidence_factorization": {},
        }
    radical_index = 1
    for entry in common_ideal["diagonal_entries"]:
        radical_index *= radical_part(entry)
    if common_ideal["index"] % radical_index != 0:
        raise AssertionError("radical incidence index did not divide ideal index")
    return {
        **common_ideal,
        "radical_incidence_index": radical_index,
        "radical_incidence_factorization": factorint(radical_index),
    }


def common_ideal_radical_incidence_index(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> dict[str, Any]:
    return with_radical_incidence_index(
        common_ideal_index(left, right, order, sigma)
    )


def power_common_ideal_matrix(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> list[list[int]]:
    phi = cyclotomic_poly(order)
    dimension = degree(phi)
    blocks = []
    for rank in range(1, sigma + 1):
        delta = poly_sub(
            exponent_power_sum_poly(left, order, rank),
            exponent_power_sum_poly(right, order, rank),
        )
        _, remainder = poly_divmod_monic(delta, phi)
        if remainder:
            blocks.append(multiplication_matrix_mod_cyclotomic(remainder, order))
    if not blocks:
        return []
    return [
        [entry for block in blocks for entry in block[row]]
        for row in range(dimension)
    ]


def power_common_ideal_index(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> dict[str, Any]:
    matrix = power_common_ideal_matrix(left, right, order, sigma)
    dimension = degree(cyclotomic_poly(order))
    if not matrix:
        return {
            "char_zero_collision": True,
            "rank": 0,
            "dimension": dimension,
            "index": 0,
            "factorization": {},
            "diagonal_entries": [],
        }
    diagonal = integer_diagonal_entries(matrix)
    rank = len(diagonal)
    index = 0
    if rank == dimension:
        index = 1
        for entry in diagonal:
            index *= entry
    return {
        "char_zero_collision": False,
        "rank": rank,
        "dimension": dimension,
        "index": index,
        "factorization": factorint(index),
        "diagonal_entries": diagonal,
    }


def power_common_ideal_radical_incidence_index(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> dict[str, Any]:
    return with_radical_incidence_index(
        power_common_ideal_index(left, right, order, sigma)
    )


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


def prime_support_away_from_order(value: int, order: int) -> list[int]:
    return [
        prime for prime in sorted(factorint(value))
        if order % prime != 0
    ]


def split_prime_support(value: int, order: int) -> list[int]:
    return [
        prime for prime in prime_support_away_from_order(value, order)
        if prime % order == 1
    ]


def p_adic_valuation(value: int, prime: int) -> int:
    if value == 0:
        raise AssertionError("p-adic valuation is finite only for nonzero input")
    remaining = abs(value)
    exponent = 0
    while remaining % prime == 0:
        exponent += 1
        remaining //= prime
    return exponent


def max_fiber_bound_from_pair_bound(pair_bound: int) -> int:
    if pair_bound < 0:
        raise AssertionError("pair bound must be nonnegative")
    bound = (1 + isqrt(1 + 8 * pair_bound)) // 2
    while bound * (bound - 1) // 2 > pair_bound:
        bound -= 1
    while (bound + 1) * bound // 2 <= pair_bound:
        bound += 1
    return bound


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


def multiplicative_order_mod(value: int, modulus: int) -> int:
    if gcd(value, modulus) != 1:
        raise AssertionError("multiplicative order requires a unit")
    current = value % modulus
    exponent = 1
    while current != 1:
        current = current * value % modulus
        exponent += 1
        if exponent > modulus:
            raise AssertionError("multiplicative order search failed")
    return exponent


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
    common_ideal_index_counter: Counter[int] = Counter()
    common_root_degree_counter: Counter[int] = Counter()
    embedding_zero_count_counter: Counter[int] = Counter()
    split_factor_sets: Counter[tuple[int, ...]] = Counter()
    aggregate_certificate = 1
    aggregate_common_ideal_index = 1
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
        common_ideal = common_ideal_index(
            pair["left"],
            pair["right"],
            order=16,
            sigma=4,
        )
        if common_ideal["char_zero_collision"]:
            raise AssertionError("F_17 packet had zero common-ideal matrix")
        if common_ideal["index"] == 0:
            raise AssertionError("F_17 packet had zero common-ideal index")
        if certificate["certificate"] % common_ideal["index"] != 0:
            raise AssertionError("common-ideal index did not divide norm certificate")
        if common_ideal["index"] % 17 != 0:
            raise AssertionError("common-ideal index missed the actual bad prime")
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
        common_ideal_index_counter[common_ideal["index"]] += 1
        split_factor_sets[split_factors] += 1
        aggregate_certificate = lcm_int(
            aggregate_certificate,
            certificate["certificate"],
        )
        aggregate_common_ideal_index = lcm_int(
            aggregate_common_ideal_index,
            common_ideal["index"],
        )
        orbit_key = translation_orbit_key(pair["left"], pair["right"], 16)
        orbit_groups[orbit_key].append(pair)
        affine_orbits.add(affine_orbit_key(pair["left"], pair["right"], 16))

    expected = Counter({68: 16, 272: 16, 147_968: 8})
    if certificate_counter != expected:
        raise AssertionError((certificate_counter, expected))
    expected_ideal_indices = Counter({68: 16, 272: 16, 8_704: 8})
    if common_ideal_index_counter != expected_ideal_indices:
        raise AssertionError((common_ideal_index_counter, expected_ideal_indices))
    if aggregate_certificate != 147_968:
        raise AssertionError("unexpected aggregate lcm certificate")
    if aggregate_common_ideal_index != 8_704:
        raise AssertionError("unexpected aggregate common-ideal index")
    aggregate_split_factors = [
        prime for prime in sorted(factorint(aggregate_certificate))
        if prime % 16 == 1
    ]
    if aggregate_split_factors != [17]:
        raise AssertionError("unexpected aggregate split-prime support")
    aggregate_ideal_split_factors = [
        prime for prime in sorted(factorint(aggregate_common_ideal_index))
        if prime % 16 == 1
    ]
    if aggregate_ideal_split_factors != [17]:
        raise AssertionError("unexpected aggregate ideal split-prime support")

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
        "common_ideal_index_counts": dict(
            sorted(common_ideal_index_counter.items())
        ),
        "common_root_degree_counts": dict(sorted(common_root_degree_counter.items())),
        "embedding_zero_count_counts": dict(
            sorted(embedding_zero_count_counter.items())
        ),
        "aggregate_lcm_certificate": aggregate_certificate,
        "aggregate_common_ideal_lcm": aggregate_common_ideal_index,
        "aggregate_split_prime_factors": aggregate_split_factors,
        "aggregate_ideal_split_prime_factors": aggregate_ideal_split_factors,
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


def check_newton_common_ideal_bridge() -> dict[str, Any]:
    def compare_local_valuations(
        left: Sequence[int],
        right: Sequence[int],
        order: int,
        sigma: int,
    ) -> dict[str, Any]:
        elementary = common_ideal_index(left, right, order, sigma)
        power = power_common_ideal_index(left, right, order, sigma)
        if elementary["char_zero_collision"] != power["char_zero_collision"]:
            raise AssertionError("Newton bridge changed char-zero status")
        if elementary["index"] == 0:
            return {
                "elementary_index": 0,
                "power_index": 0,
                "checked_primes": [],
            }
        excluded = set(factorint(order)) | set(factorint(factorial(sigma)))
        candidate_primes = (
            set(factorint(elementary["index"]))
            | set(factorint(power["index"]))
        )
        checked_primes = []
        for prime in sorted(candidate_primes - excluded):
            elementary_valuation = p_adic_valuation(elementary["index"], prime)
            power_valuation = p_adic_valuation(power["index"], prime)
            if elementary_valuation != power_valuation:
                raise AssertionError("Newton bridge changed local valuation")
            checked_primes.append({
                "prime": prime,
                "valuation": elementary_valuation,
            })
        return {
            "elementary_index": elementary["index"],
            "power_index": power["index"],
            "excluded_primes": sorted(excluded),
            "checked_primes": checked_primes,
        }

    order = 16
    sigma = 4
    row = finite_prefix_collision_pairs(
        prime=17,
        order=order,
        complement_size=6,
        sigma=sigma,
    )
    index_pair_counts: Counter[tuple[int, int]] = Counter()
    checked_pair_count = 0
    for pair in row["pairs"]:
        comparison = compare_local_valuations(
            pair["left"],
            pair["right"],
            order,
            sigma,
        )
        index_pair_counts[(
            comparison["elementary_index"],
            comparison["power_index"],
        )] += 1
        checked_pair_count += 1
    expected_index_pair_counts = Counter({
        (68, 136): 16,
        (272, 272): 16,
        (8_704, 8_704): 8,
    })
    if index_pair_counts != expected_index_pair_counts:
        raise AssertionError("unexpected elementary/power index pairs")

    false_positive_comparison = compare_local_valuations(
        (0, 1, 2, 7, 9, 13),
        (0, 1, 2, 3, 4, 11),
        order,
        sigma,
    )
    if false_positive_comparison["elementary_index"] != 2:
        raise AssertionError("unexpected false-positive elementary index")
    if false_positive_comparison["power_index"] != 2:
        raise AssertionError("unexpected false-positive power index")

    depth_rows = []
    depth_left = (0, 1, 2, 3, 4, 14)
    depth_right = (5, 6, 7, 9, 12, 15)
    for depth_sigma in range(1, 7):
        comparison = compare_local_valuations(
            depth_left,
            depth_right,
            order,
            depth_sigma,
        )
        depth_rows.append({
            "sigma": depth_sigma,
            "elementary_index": comparison["elementary_index"],
            "power_index": comparison["power_index"],
            "checked_primes": comparison["checked_primes"],
        })

    extension_comparison = compare_local_valuations(
        (0, 1),
        (2, 5),
        8,
        1,
    )
    if extension_comparison["elementary_index"] != 36:
        raise AssertionError("bad F_9 elementary common-ideal index")
    if extension_comparison["power_index"] != 36:
        raise AssertionError("bad F_9 power common-ideal index")
    if extension_comparison["checked_primes"] != [{"prime": 3, "valuation": 2}]:
        raise AssertionError("bad F_9 local Newton valuation check")

    return {
        "status": "PASS",
        "condition": "ell does not divide n*sigma!",
        "f17_packet_pairs_checked": checked_pair_count,
        "f17_index_pair_counts": {
            f"{left}->{right}": count
            for (left, right), count in sorted(index_pair_counts.items())
        },
        "false_positive": false_positive_comparison,
        "depth_representative": {
            "left": list(depth_left),
            "right": list(depth_right),
            "rows": depth_rows,
        },
        "extension_witness": extension_comparison,
    }


def check_newton_radical_incidence_bridge() -> dict[str, Any]:
    def compare_local_radical_valuations(
        left: Sequence[int],
        right: Sequence[int],
        order: int,
        sigma: int,
    ) -> dict[str, Any]:
        elementary = common_ideal_radical_incidence_index(
            left,
            right,
            order,
            sigma,
        )
        power = power_common_ideal_radical_incidence_index(
            left,
            right,
            order,
            sigma,
        )
        if elementary["char_zero_collision"] != power["char_zero_collision"]:
            raise AssertionError("Newton radical bridge changed char-zero status")
        if elementary["radical_incidence_index"] == 0:
            return {
                "elementary_radical_index": 0,
                "power_radical_index": 0,
                "checked_primes": [],
            }
        excluded = set(factorint(order)) | set(factorint(factorial(sigma)))
        candidate_primes = (
            set(factorint(elementary["radical_incidence_index"]))
            | set(factorint(power["radical_incidence_index"]))
        )
        checked_primes = []
        for prime in sorted(candidate_primes - excluded):
            elementary_valuation = p_adic_valuation(
                elementary["radical_incidence_index"],
                prime,
            )
            power_valuation = p_adic_valuation(
                power["radical_incidence_index"],
                prime,
            )
            if elementary_valuation != power_valuation:
                raise AssertionError("Newton bridge changed radical valuation")
            checked_primes.append({
                "prime": prime,
                "valuation": elementary_valuation,
            })
        return {
            "elementary_radical_index": (
                elementary["radical_incidence_index"]
            ),
            "power_radical_index": power["radical_incidence_index"],
            "excluded_primes": sorted(excluded),
            "checked_primes": checked_primes,
        }

    order = 16
    sigma = 4
    row = finite_prefix_collision_pairs(
        prime=17,
        order=order,
        complement_size=6,
        sigma=sigma,
    )
    radical_pair_counts: Counter[tuple[int, int]] = Counter()
    for pair in row["pairs"]:
        comparison = compare_local_radical_valuations(
            pair["left"],
            pair["right"],
            order,
            sigma,
        )
        radical_pair_counts[(
            comparison["elementary_radical_index"],
            comparison["power_radical_index"],
        )] += 1
        if comparison["checked_primes"] != [{"prime": 17, "valuation": 1}]:
            raise AssertionError("bad F_17 radical Newton valuation")
    expected_radical_pair_counts = Counter({
        (68, 136): 16,
        (272, 272): 16,
        (4_352, 4_352): 8,
    })
    if radical_pair_counts != expected_radical_pair_counts:
        raise AssertionError("unexpected elementary/power radical pairs")

    false_positive = compare_local_radical_valuations(
        (0, 1, 2, 7, 9, 13),
        (0, 1, 2, 3, 4, 11),
        order,
        sigma,
    )
    if false_positive["elementary_radical_index"] != 2:
        raise AssertionError("unexpected false-positive elementary radical")
    if false_positive["power_radical_index"] != 2:
        raise AssertionError("unexpected false-positive power radical")
    if false_positive["checked_primes"]:
        raise AssertionError("false-positive had an off-denominator radical prime")

    depth_rows = []
    depth_left = (0, 1, 2, 3, 4, 14)
    depth_right = (5, 6, 7, 9, 12, 15)
    for depth_sigma in range(1, 7):
        comparison = compare_local_radical_valuations(
            depth_left,
            depth_right,
            order,
            depth_sigma,
        )
        depth_rows.append({
            "sigma": depth_sigma,
            "elementary_radical_index": (
                comparison["elementary_radical_index"]
            ),
            "power_radical_index": comparison["power_radical_index"],
            "checked_primes": comparison["checked_primes"],
        })

    extension = compare_local_radical_valuations(
        (0, 1),
        (2, 5),
        8,
        1,
    )
    if extension["elementary_radical_index"] != 36:
        raise AssertionError("bad F_9 elementary radical index")
    if extension["power_radical_index"] != 36:
        raise AssertionError("bad F_9 power radical index")
    if extension["checked_primes"] != [{"prime": 3, "valuation": 2}]:
        raise AssertionError("bad F_9 radical Newton valuation")

    return {
        "status": "PASS",
        "condition": "ell does not divide n*sigma!",
        "f17_packet_pairs_checked": row["collision_pair_count"],
        "f17_radical_pair_counts": {
            f"{left}->{right}": count
            for (left, right), count in sorted(radical_pair_counts.items())
        },
        "false_positive": false_positive,
        "depth_representative": {
            "left": list(depth_left),
            "right": list(depth_right),
            "rows": depth_rows,
        },
        "extension_witness": extension,
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
    common_ideal = common_ideal_index(left, right, order, sigma)
    if common_ideal["index"] != 36:
        raise AssertionError("unexpected F_9 common-ideal index")
    if common_ideal["index"] % characteristic != 0:
        raise AssertionError("F_9 common-ideal index missed characteristic 3")

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
        "common_ideal_index": common_ideal["index"],
        "common_ideal_factorization": common_ideal["factorization"],
        "common_factor_mod_3": common_factor,
        "common_factor_degree_mod_3": degree(common_factor),
    }


def check_extension_field_row_accounting() -> dict[str, Any]:
    characteristic = 3
    extension_degree = 2
    order = 8
    complement_size = 2
    sigma = 1
    if multiplicative_order_mod(characteristic, order) != extension_degree:
        raise AssertionError("bad nonsplit Frobenius orbit length")
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
    prime_ideal_count_distribution: Counter[int] = Counter()
    degree_weighted_sum = 0
    prime_ideal_weighted_sum = 0
    non_char_zero_pairs = 0
    non_char_zero_degree_sum = 0
    non_char_zero_prime_ideal_sum = 0
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
        if common_degree % extension_degree != 0:
            raise AssertionError("F_9 gcd degree is not a Frobenius-orbit multiple")
        prime_ideal_count = common_degree // extension_degree
        certificate = bad_prime_certificate(pair[0], pair[1], order, sigma)
        degree_distribution[common_degree] += 1
        prime_ideal_count_distribution[prime_ideal_count] += 1
        degree_weighted_sum += common_degree
        prime_ideal_weighted_sum += prime_ideal_count
        if certificate["char_zero_collision"]:
            char_zero_distribution[common_degree] += 1
        else:
            if certificate["certificate"] % characteristic != 0:
                raise AssertionError("F_9 bad-prime pair missed the certificate")
            non_char_zero_pairs += 1
            non_char_zero_degree_sum += common_degree
            non_char_zero_prime_ideal_sum += prime_ideal_count

    incidence_sum = sum(incidence_counter.values())
    expected_incidence_sum = len(primitive_roots) * 30
    if incidence_sum != expected_incidence_sum:
        raise AssertionError("bad F_9 incidence count")
    if degree_weighted_sum != incidence_sum:
        raise AssertionError("bad F_9 degree-weighted row accounting")
    if prime_ideal_weighted_sum * extension_degree != degree_weighted_sum:
        raise AssertionError("bad F_9 prime-ideal weighted row accounting")
    if dict(degree_distribution) != {2: 48, 4: 6}:
        raise AssertionError("unexpected F_9 degree distribution")
    if dict(prime_ideal_count_distribution) != {1: 48, 2: 6}:
        raise AssertionError("unexpected F_9 prime-ideal distribution")
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
        "prime_ideal_weighted_sum": prime_ideal_weighted_sum,
        "degree_distribution_on_incident_pairs": dict(
            sorted(degree_distribution.items())
        ),
        "prime_ideal_count_distribution": dict(
            sorted(prime_ideal_count_distribution.items())
        ),
        "char_zero_degree_distribution": dict(
            sorted(char_zero_distribution.items())
        ),
        "non_char_zero_pair_count": non_char_zero_pairs,
        "non_char_zero_degree_sum": non_char_zero_degree_sum,
        "non_char_zero_prime_ideal_sum": non_char_zero_prime_ideal_sum,
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
        {
            "sigma": 1,
            "certificate": 2_312,
            "ideal_index": 2_312,
            "degree": 2,
            "split_factors": [17],
        },
        {
            "sigma": 2,
            "certificate": 68,
            "ideal_index": 68,
            "degree": 1,
            "split_factors": [17],
        },
        {
            "sigma": 3,
            "certificate": 68,
            "ideal_index": 68,
            "degree": 1,
            "split_factors": [17],
        },
        {
            "sigma": 4,
            "certificate": 68,
            "ideal_index": 68,
            "degree": 1,
            "split_factors": [17],
        },
        {
            "sigma": 5,
            "certificate": 4,
            "ideal_index": 4,
            "degree": 0,
            "split_factors": [],
        },
        {
            "sigma": 6,
            "certificate": 4,
            "ideal_index": 4,
            "degree": 0,
            "split_factors": [],
        },
    ]
    template_rows = []
    previous_certificate = None
    previous_ideal_index = None
    previous_degree = None
    for expected in expected_template_rows:
        sigma = expected["sigma"]
        certificate = bad_prime_certificate(left, right, order, sigma)
        common_ideal = common_ideal_index(left, right, order, sigma)
        degree_at_prime = degree(common_root_gcd_mod(
            left,
            right,
            order,
            sigma,
            prime,
        ))
        if certificate["certificate"] != expected["certificate"]:
            raise AssertionError("unexpected depth-filtration certificate")
        if common_ideal["index"] != expected["ideal_index"]:
            raise AssertionError("unexpected depth-filtration common-ideal index")
        if certificate["certificate"] % common_ideal["index"] != 0:
            raise AssertionError("depth common-ideal index did not divide certificate")
        if degree_at_prime != expected["degree"]:
            raise AssertionError("unexpected depth-filtration gcd degree")
        if certificate["split_prime_factors"] != expected["split_factors"]:
            raise AssertionError("unexpected depth-filtration split factors")
        if (
            previous_certificate is not None
            and previous_certificate % certificate["certificate"] != 0
        ):
            raise AssertionError("certificate did not divide previous depth")
        if (
            previous_ideal_index is not None
            and previous_ideal_index % common_ideal["index"] != 0
        ):
            raise AssertionError("common-ideal index did not divide previous depth")
        if previous_degree is not None and degree_at_prime > previous_degree:
            raise AssertionError("gcd degree increased with sigma")
        previous_certificate = certificate["certificate"]
        previous_ideal_index = common_ideal["index"]
        previous_degree = degree_at_prime
        template_rows.append({
            "sigma": sigma,
            "certificate": certificate["certificate"],
            "common_ideal_index": common_ideal["index"],
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


def radical_frontier_drop(
    left: Sequence[int],
    right: Sequence[int],
    order: int,
    sigma: int,
) -> dict[str, Any]:
    current = common_ideal_radical_incidence_index(left, right, order, sigma)
    deeper = common_ideal_radical_incidence_index(left, right, order, sigma + 1)
    if current["radical_incidence_index"] == 0:
        raise AssertionError("frontier drop excludes char-zero current ideal")
    if deeper["radical_incidence_index"] == 0:
        raise AssertionError("frontier drop excludes char-zero deeper ideal")

    candidate_primes = (
        set(factorint(current["radical_incidence_index"]))
        | set(factorint(deeper["radical_incidence_index"]))
    )
    drop_part = 1
    rows = []
    for prime in sorted(candidate_primes):
        if order % prime == 0:
            continue
        current_valuation = p_adic_valuation(
            current["radical_incidence_index"],
            prime,
        )
        deeper_valuation = p_adic_valuation(
            deeper["radical_incidence_index"],
            prime,
        )
        if deeper_valuation > current_valuation:
            raise AssertionError("radical frontier valuation increased")
        current_degree = degree(common_root_gcd_mod(
            left,
            right,
            order,
            sigma,
            prime,
        ))
        deeper_degree = degree(common_root_gcd_mod(
            left,
            right,
            order,
            sigma + 1,
            prime,
        ))
        if current_degree != current_valuation:
            raise AssertionError("current radical valuation missed degree")
        if deeper_degree != deeper_valuation:
            raise AssertionError("deeper radical valuation missed degree")
        if current_degree - deeper_degree != current_valuation - deeper_valuation:
            raise AssertionError("frontier degree drop mismatched radical drop")
        valuation_drop = current_valuation - deeper_valuation
        drop_part *= prime ** valuation_drop
        rows.append({
            "prime": prime,
            "current_valuation": current_valuation,
            "deeper_valuation": deeper_valuation,
            "valuation_drop": valuation_drop,
            "current_degree": current_degree,
            "deeper_degree": deeper_degree,
            "degree_drop": current_degree - deeper_degree,
        })

    return {
        "sigma": sigma,
        "current_radical_index": current["radical_incidence_index"],
        "deeper_radical_index": deeper["radical_incidence_index"],
        "current_away_from_order": part_away_from_order(
            current["radical_incidence_index"],
            order,
        ),
        "deeper_away_from_order": part_away_from_order(
            deeper["radical_incidence_index"],
            order,
        ),
        "frontier_drop_part": drop_part,
        "frontier_drop_factorization": factorint(drop_part),
        "rows": rows,
    }


def check_prefix_radical_frontier_drop() -> dict[str, Any]:
    order = 16
    prime = 17
    left = (0, 1, 2, 3, 4, 14)
    right = (5, 6, 7, 9, 12, 15)
    expected_representative_drops = {
        1: {17: 1},
        2: {},
        3: {},
        4: {17: 1},
        5: {},
    }
    representative_rows = []
    for sigma in range(1, 6):
        drop = radical_frontier_drop(left, right, order, sigma)
        if drop["frontier_drop_factorization"] != expected_representative_drops[
            sigma
        ]:
            raise AssertionError("bad representative radical frontier drop")
        row_at_prime = next(
            (row for row in drop["rows"] if row["prime"] == prime),
            None,
        )
        if row_at_prime is not None:
            if row_at_prime["degree_drop"] != row_at_prime["valuation_drop"]:
                raise AssertionError("bad representative degree/drop row")
        representative_rows.append(drop)

    packet = finite_prefix_collision_pairs(
        prime=prime,
        order=order,
        complement_size=6,
        sigma=4,
    )
    packet_frontier_product = 1
    packet_drop_counter: Counter[int] = Counter()
    for pair in packet["pairs"]:
        drop = radical_frontier_drop(pair["left"], pair["right"], order, 4)
        if drop["frontier_drop_factorization"] != {17: 1}:
            raise AssertionError("bad F_17 packet radical frontier drop")
        packet_frontier_product *= drop["frontier_drop_part"]
        packet_drop_counter[drop["frontier_drop_part"]] += 1
    if factorint(packet_frontier_product) != {17: 40}:
        raise AssertionError("bad F_17 packet frontier product")

    extension_drop = radical_frontier_drop((0, 1), (2, 5), 8, 1)
    if extension_drop["frontier_drop_factorization"] != {3: 2}:
        raise AssertionError("bad F_9 radical frontier drop")

    return {
        "representative": {
            "left": list(left),
            "right": list(right),
            "rows": representative_rows,
        },
        "packet_sigma4_to_5": {
            "pair_count": packet["collision_pair_count"],
            "frontier_drop_counts": dict(sorted(packet_drop_counter.items())),
            "frontier_product_factorization": factorint(packet_frontier_product),
        },
        "nonsplit_witness": extension_drop,
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


def check_full_prefix_common_ideal_endpoint() -> dict[str, Any]:
    order = 16
    exhaustive_max_complement_size = 2
    pair_count = 0
    max_endpoint_index = 0
    endpoint_factorizations: Counter[tuple[tuple[int, int], ...]] = Counter()
    for complement_size in range(1, exhaustive_max_complement_size + 1):
        subsets = list(itertools.combinations(range(order), complement_size))
        for left_idx, left in enumerate(subsets):
            for right in subsets[left_idx + 1:]:
                common_ideal = common_ideal_index(
                    left,
                    right,
                    order,
                    complement_size,
                )
                if common_ideal["index"] == 0:
                    raise AssertionError("distinct full-prefix pair was char-zero")
                support = prime_support_away_from_order(
                    common_ideal["index"],
                    order,
                )
                if support:
                    raise AssertionError("full-prefix endpoint had off-order support")
                max_endpoint_index = max(max_endpoint_index, common_ideal["index"])
                endpoint_factorizations[
                    tuple(sorted(common_ideal["factorization"].items()))
                ] += 1
                pair_count += 1
    if pair_count != 7_260:
        raise AssertionError("unexpected full-prefix endpoint pair count")

    representative_left = (0, 1, 2, 3, 4, 14)
    representative_right = (5, 6, 7, 9, 12, 15)
    representative_ideal = common_ideal_index(
        representative_left,
        representative_right,
        order,
        6,
    )
    representative_support = prime_support_away_from_order(
        representative_ideal["index"],
        order,
    )
    if representative_ideal["index"] != 4 or representative_support:
        raise AssertionError("representative full-prefix endpoint had bad support")

    return {
        "order": order,
        "exhaustive_max_complement_size": exhaustive_max_complement_size,
        "pairs_checked": pair_count,
        "max_endpoint_index": max_endpoint_index,
        "endpoint_factorizations": {
            str(dict(key)): value
            for key, value in sorted(endpoint_factorizations.items())
        },
        "representative": {
            "complement_size": 6,
            "left": list(representative_left),
            "right": list(representative_right),
            "common_ideal_index": representative_ideal["index"],
            "support_away_from_order": representative_support,
        },
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
    common_ideal = common_ideal_index(left, right, order, sigma)
    if common_ideal["index"] != 2:
        raise AssertionError("unexpected p=97 false-positive common-ideal index")
    if common_ideal["index"] % prime == 0:
        raise AssertionError("common-ideal certificate did not remove p=97")
    if certificate["certificate"] % common_ideal["index"] != 0:
        raise AssertionError("common-ideal index did not divide norm certificate")
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
        "common_ideal_index": common_ideal["index"],
        "common_ideal_factorization": common_ideal["factorization"],
        "common_root_factor_mod_p": common_root_factor,
        "common_root_degree": degree(common_root_factor),
        "embedding_zero_count": len(zero_roots),
        "primitive_root_checks": profile,
        "actual_collision_for_any_embedding": any_collision,
    }


def check_finite_family_exact_aggregation() -> dict[str, Any]:
    order = 16
    sigma = 4
    packet = finite_prefix_collision_pairs(
        prime=17,
        order=order,
        complement_size=6,
        sigma=sigma,
    )
    false_positive = normalized_pair(
        (0, 1, 2, 7, 9, 13),
        (0, 1, 2, 3, 4, 11),
    )
    family = [
        normalized_pair(pair["left"], pair["right"])
        for pair in packet["pairs"]
    ]
    family.append(false_positive)

    norm_lcm = 1
    ideal_lcm = 1
    for left, right in family:
        certificate = bad_prime_certificate(left, right, order, sigma)
        common_ideal = common_ideal_index(left, right, order, sigma)
        if certificate["char_zero_collision"] or common_ideal["char_zero_collision"]:
            raise AssertionError("finite-family aggregation assumes char-zero removed")
        if certificate["certificate"] % common_ideal["index"] != 0:
            raise AssertionError("common-ideal index did not divide certificate")
        norm_lcm = lcm_int(norm_lcm, certificate["certificate"])
        ideal_lcm = lcm_int(ideal_lcm, common_ideal["index"])

    if norm_lcm != 14_352_896:
        raise AssertionError("unexpected finite-family resultant lcm")
    if ideal_lcm != 8_704:
        raise AssertionError("unexpected finite-family common-ideal lcm")
    if split_prime_support(norm_lcm, order) != [17, 97]:
        raise AssertionError("unexpected coarse split-prime support")
    if split_prime_support(ideal_lcm, order) != [17]:
        raise AssertionError("unexpected exact split-prime support")

    direct_rows = []
    for prime in split_prime_support(norm_lcm, order):
        positive_pairs = 0
        degree_sum = 0
        for left, right in family:
            common_degree = degree(common_root_gcd_mod(
                left,
                right,
                order,
                sigma,
                prime,
            ))
            if common_degree > 0:
                positive_pairs += 1
                degree_sum += common_degree
        direct_rows.append({
            "prime": prime,
            "positive_template_pairs": positive_pairs,
            "common_root_degree_sum": degree_sum,
        })
    expected_direct_rows = [
        {
            "prime": 17,
            "positive_template_pairs": 40,
            "common_root_degree_sum": 40,
        },
        {
            "prime": 97,
            "positive_template_pairs": 0,
            "common_root_degree_sum": 0,
        },
    ]
    if direct_rows != expected_direct_rows:
        raise AssertionError(f"bad direct split-prime rows: {direct_rows}")
    direct_split_support = [
        row["prime"] for row in direct_rows
        if row["common_root_degree_sum"] > 0
    ]
    if direct_split_support != split_prime_support(ideal_lcm, order):
        raise AssertionError("exact lcm support did not match direct gcd support")

    extension_order = 8
    extension_sigma = 1
    extension_left = (0, 1)
    extension_right = (2, 5)
    extension_ideal = common_ideal_index(
        extension_left,
        extension_right,
        extension_order,
        extension_sigma,
    )
    extension_support = prime_support_away_from_order(
        extension_ideal["index"],
        extension_order,
    )
    if extension_support != [3]:
        raise AssertionError("unexpected nonsplit exact support")
    if split_prime_support(extension_ideal["index"], extension_order):
        raise AssertionError("nonsplit witness appeared in split support")
    if degree(common_root_gcd_mod(
        extension_left,
        extension_right,
        extension_order,
        extension_sigma,
        3,
    )) != 2:
        raise AssertionError("nonsplit exact support missed F_9 collision")

    return {
        "split_family": {
            "order": order,
            "sigma": sigma,
            "template_pair_count": len(family),
            "resultant_lcm": norm_lcm,
            "resultant_split_support": split_prime_support(norm_lcm, order),
            "common_ideal_lcm": ideal_lcm,
            "common_ideal_split_support": split_prime_support(ideal_lcm, order),
            "direct_split_rows": direct_rows,
        },
        "nonsplit_witness": {
            "order": extension_order,
            "sigma": extension_sigma,
            "common_ideal_index": extension_ideal["index"],
            "support_away_from_order": extension_support,
            "split_support": split_prime_support(
                extension_ideal["index"],
                extension_order,
            ),
            "common_root_degree_at_3": degree(common_root_gcd_mod(
                extension_left,
                extension_right,
                extension_order,
                extension_sigma,
                3,
            )),
        },
    }


def check_valuation_incidence_budget() -> dict[str, Any]:
    order = 16
    sigma = 4
    packet = finite_prefix_collision_pairs(
        prime=17,
        order=order,
        complement_size=6,
        sigma=sigma,
    )
    family = [
        normalized_pair(pair["left"], pair["right"])
        for pair in packet["pairs"]
    ]
    family.append(normalized_pair(
        (0, 1, 2, 7, 9, 13),
        (0, 1, 2, 3, 4, 11),
    ))

    valuation_rows = []
    for prime in [17, 97]:
        degree_sum = 0
        valuation_sum = 0
        positive_pairs = 0
        for left, right in family:
            common_degree = degree(common_root_gcd_mod(
                left,
                right,
                order,
                sigma,
                prime,
            ))
            common_ideal = common_ideal_index(left, right, order, sigma)
            if common_ideal["index"] == 0:
                raise AssertionError("valuation budget excludes char-zero templates")
            valuation = p_adic_valuation(common_ideal["index"], prime)
            if common_degree > valuation:
                raise AssertionError("common-root degree exceeded valuation budget")
            degree_sum += common_degree
            valuation_sum += valuation
            if common_degree:
                positive_pairs += 1
        if degree_sum > valuation_sum:
            raise AssertionError("family degree sum exceeded valuation budget")
        valuation_rows.append({
            "prime": prime,
            "positive_template_pairs": positive_pairs,
            "common_root_degree_sum": degree_sum,
            "valuation_budget": valuation_sum,
        })

    expected_rows = [
        {
            "prime": 17,
            "positive_template_pairs": 40,
            "common_root_degree_sum": 40,
            "valuation_budget": 40,
        },
        {
            "prime": 97,
            "positive_template_pairs": 0,
            "common_root_degree_sum": 0,
            "valuation_budget": 0,
        },
    ]
    if valuation_rows != expected_rows:
        raise AssertionError(f"unexpected valuation rows: {valuation_rows}")

    extension_order = 8
    extension_sigma = 1
    extension_left = (0, 1)
    extension_right = (2, 5)
    extension_prime = 3
    extension_degree = degree(common_root_gcd_mod(
        extension_left,
        extension_right,
        extension_order,
        extension_sigma,
        extension_prime,
    ))
    extension_ideal = common_ideal_index(
        extension_left,
        extension_right,
        extension_order,
        extension_sigma,
    )
    extension_budget = p_adic_valuation(
        extension_ideal["index"],
        extension_prime,
    )
    if extension_degree != 2 or extension_budget != 2:
        raise AssertionError("unexpected nonsplit valuation budget")
    if extension_degree > extension_budget:
        raise AssertionError("nonsplit degree exceeded valuation budget")

    return {
        "split_family": {
            "order": order,
            "sigma": sigma,
            "template_pair_count": len(family),
            "rows": valuation_rows,
        },
        "nonsplit_witness": {
            "order": extension_order,
            "sigma": extension_sigma,
            "prime": extension_prime,
            "common_root_degree": extension_degree,
            "valuation_budget": extension_budget,
        },
    }


def check_radical_incidence_index() -> dict[str, Any]:
    order = 16
    sigma = 4
    packet = finite_prefix_collision_pairs(
        prime=17,
        order=order,
        complement_size=6,
        sigma=sigma,
    )
    packet_radical_counts: Counter[int] = Counter()
    packet_exact_degree_sum = 0
    packet_radical_valuation_sum = 0
    for pair in packet["pairs"]:
        left = pair["left"]
        right = pair["right"]
        radical = common_ideal_radical_incidence_index(
            left,
            right,
            order,
            sigma,
        )
        common_degree = degree(common_root_gcd_mod(
            left,
            right,
            order,
            sigma,
            17,
        ))
        radical_valuation = p_adic_valuation(
            radical["radical_incidence_index"],
            17,
        )
        if common_degree != radical_valuation:
            raise AssertionError("F_17 radical index missed common-root degree")
        if radical["index"] % radical["radical_incidence_index"] != 0:
            raise AssertionError("radical index did not divide common-ideal index")
        packet_exact_degree_sum += common_degree
        packet_radical_valuation_sum += radical_valuation
        packet_radical_counts[radical["radical_incidence_index"]] += 1
    if packet_exact_degree_sum != 40 or packet_radical_valuation_sum != 40:
        raise AssertionError("bad F_17 packet radical incidence total")

    primitive_roots = primitive_order_roots(17, order)
    dilation_family: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for root in primitive_roots:
        row = finite_prefix_collision_pairs(
            prime=17,
            order=order,
            complement_size=6,
            sigma=sigma,
            root=root,
        )
        for pair in row["pairs"]:
            dilation_family.add(normalized_pair(pair["left"], pair["right"]))
    dilation_degree_sum = 0
    dilation_radical_sum = 0
    for left, right in dilation_family:
        common_degree = degree(common_root_gcd_mod(
            left,
            right,
            order,
            sigma,
            17,
        ))
        radical = common_ideal_radical_incidence_index(
            left,
            right,
            order,
            sigma,
        )
        radical_valuation = p_adic_valuation(
            radical["radical_incidence_index"],
            17,
        )
        if common_degree != radical_valuation:
            raise AssertionError("dilation radical index missed degree")
        dilation_degree_sum += common_degree
        dilation_radical_sum += radical_valuation
    if len(dilation_family) != 320:
        raise AssertionError("unexpected radical dilation-family size")
    if dilation_degree_sum != 320 or dilation_radical_sum != 320:
        raise AssertionError("bad radical dilation-family total")

    false_positive = common_ideal_radical_incidence_index(
        (0, 1, 2, 7, 9, 13),
        (0, 1, 2, 3, 4, 11),
        order,
        sigma,
    )
    false_positive_degree = degree(common_root_gcd_mod(
        (0, 1, 2, 7, 9, 13),
        (0, 1, 2, 3, 4, 11),
        order,
        sigma,
        97,
    ))
    false_positive_valuation = p_adic_valuation(
        false_positive["radical_incidence_index"],
        97,
    )
    if false_positive_degree != 0 or false_positive_valuation != 0:
        raise AssertionError("radical index did not remove p=97 false positive")

    extension_order = 8
    extension_sigma = 1
    extension_prime = 3
    extension_roots = gf9_primitive_order_roots(extension_order)
    non_char_family: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    for root in extension_roots:
        row = finite_prefix_collision_pairs_gf9(
            order=extension_order,
            complement_size=2,
            sigma=extension_sigma,
            root=root,
        )
        for pair in row["pairs"]:
            key = normalized_pair(pair["left"], pair["right"])
            certificate = bad_prime_certificate(
                key[0],
                key[1],
                extension_order,
                extension_sigma,
            )
            if not certificate["char_zero_collision"]:
                non_char_family.add(key)
    extension_degree_sum = 0
    extension_radical_sum = 0
    extension_radical_counts: Counter[int] = Counter()
    for left, right in non_char_family:
        common_degree = degree(common_root_gcd_mod(
            left,
            right,
            extension_order,
            extension_sigma,
            extension_prime,
        ))
        radical = common_ideal_radical_incidence_index(
            left,
            right,
            extension_order,
            extension_sigma,
        )
        radical_valuation = p_adic_valuation(
            radical["radical_incidence_index"],
            extension_prime,
        )
        if common_degree != radical_valuation:
            raise AssertionError("F_9 radical index missed common-root degree")
        extension_degree_sum += common_degree
        extension_radical_sum += radical_valuation
        extension_radical_counts[radical["radical_incidence_index"]] += 1
    if len(non_char_family) != 48:
        raise AssertionError("unexpected F_9 non-char radical family size")
    if extension_degree_sum != 96 or extension_radical_sum != 96:
        raise AssertionError("bad F_9 radical incidence total")

    witness = common_ideal_radical_incidence_index(
        (0, 1),
        (2, 5),
        extension_order,
        extension_sigma,
    )
    if p_adic_valuation(witness["radical_incidence_index"], 3) != 2:
        raise AssertionError("F_9 witness radical index has wrong 3-valuation")

    return {
        "split_packet": {
            "order": order,
            "sigma": sigma,
            "prime": 17,
            "pair_count": packet["collision_pair_count"],
            "radical_incidence_counts": dict(
                sorted(packet_radical_counts.items())
            ),
            "common_root_degree_sum": packet_exact_degree_sum,
            "radical_valuation_sum": packet_radical_valuation_sum,
        },
        "split_dilation_family": {
            "order": order,
            "sigma": sigma,
            "prime": 17,
            "family_size": len(dilation_family),
            "common_root_degree_sum": dilation_degree_sum,
            "radical_valuation_sum": dilation_radical_sum,
            "row_bound": dilation_radical_sum // euler_phi(order),
        },
        "false_positive": {
            "prime": 97,
            "common_root_degree": false_positive_degree,
            "radical_valuation": false_positive_valuation,
            "radical_incidence_index": (
                false_positive["radical_incidence_index"]
            ),
        },
        "nonsplit_family": {
            "order": extension_order,
            "sigma": extension_sigma,
            "prime": extension_prime,
            "family_size": len(non_char_family),
            "radical_incidence_counts": dict(
                sorted(extension_radical_counts.items())
            ),
            "common_root_degree_sum": extension_degree_sum,
            "radical_valuation_sum": extension_radical_sum,
        },
        "nonsplit_witness": {
            "left": [0, 1],
            "right": [2, 5],
            "radical_incidence_index": witness["radical_incidence_index"],
            "radical_incidence_factorization": (
                witness["radical_incidence_factorization"]
            ),
        },
    }


def check_log_weighted_density_budget() -> dict[str, Any]:
    order = 16
    sigma = 4
    packet = finite_prefix_collision_pairs(
        prime=17,
        order=order,
        complement_size=6,
        sigma=sigma,
    )
    family = [
        normalized_pair(pair["left"], pair["right"])
        for pair in packet["pairs"]
    ]
    family.append(normalized_pair(
        (0, 1, 2, 7, 9, 13),
        (0, 1, 2, 3, 4, 11),
    ))

    index_product = 1
    radical_product = 1
    height_bound_product = 1
    resultant_lcm = 1
    for left, right in family:
        certificate = bad_prime_certificate(left, right, order, sigma)
        common_ideal = common_ideal_index(left, right, order, sigma)
        radical = common_ideal_radical_incidence_index(
            left,
            right,
            order,
            sigma,
        )
        if common_ideal["index"] == 0:
            raise AssertionError("log budget excludes char-zero templates")
        if certificate["certificate"] % common_ideal["index"] != 0:
            raise AssertionError("common-ideal index did not divide certificate")
        if common_ideal["index"] != radical["index"]:
            raise AssertionError("radical wrapper changed common-ideal index")
        if common_ideal["index"] > certificate["least_active_height_bound"]:
            raise AssertionError("common-ideal index exceeded height bound")
        index_product *= common_ideal["index"]
        radical_product *= radical["radical_incidence_index"]
        height_bound_product *= certificate["least_active_height_bound"]
        resultant_lcm = lcm_int(resultant_lcm, certificate["certificate"])

    candidate_primes = sorted(set(
        prime_support_away_from_order(index_product, order)
        + split_prime_support(resultant_lcm, order)
    ))
    rows = []
    incidence_divisor = 1
    for prime in candidate_primes:
        degree_sum = 0
        valuation_budget = p_adic_valuation(index_product, prime)
        radical_valuation = p_adic_valuation(radical_product, prime)
        for left, right in family:
            degree_sum += degree(common_root_gcd_mod(
                left,
                right,
                order,
                sigma,
                prime,
            ))
        if degree_sum > valuation_budget:
            raise AssertionError("degree sum exceeded product valuation budget")
        if degree_sum != radical_valuation:
            raise AssertionError("degree sum did not match radical product")
        incidence_divisor *= prime ** degree_sum
        rows.append({
            "prime": prime,
            "common_root_degree_sum": degree_sum,
            "radical_product_valuation": radical_valuation,
            "product_valuation_budget": valuation_budget,
        })

    if rows != [
        {
            "prime": 17,
            "common_root_degree_sum": 40,
            "radical_product_valuation": 40,
            "product_valuation_budget": 40,
        },
        {
            "prime": 97,
            "common_root_degree_sum": 0,
            "radical_product_valuation": 0,
            "product_valuation_budget": 0,
        },
    ]:
        raise AssertionError(f"unexpected log-density rows: {rows}")
    if index_product % incidence_divisor != 0:
        raise AssertionError("incidence divisor did not divide index product")
    radical_away_from_order = part_away_from_order(radical_product, order)
    if radical_away_from_order != incidence_divisor:
        raise AssertionError("radical product did not equal incidence divisor")
    if height_bound_product < index_product:
        raise AssertionError("height-bound product did not dominate index product")

    extension_order = 8
    extension_sigma = 1
    extension_left = (0, 1)
    extension_right = (2, 5)
    extension_prime = 3
    extension_ideal = common_ideal_index(
        extension_left,
        extension_right,
        extension_order,
        extension_sigma,
    )
    extension_radical = common_ideal_radical_incidence_index(
        extension_left,
        extension_right,
        extension_order,
        extension_sigma,
    )
    extension_degree = degree(common_root_gcd_mod(
        extension_left,
        extension_right,
        extension_order,
        extension_sigma,
        extension_prime,
    ))
    extension_incidence_divisor = extension_prime ** extension_degree
    if extension_ideal["index"] % extension_incidence_divisor != 0:
        raise AssertionError("nonsplit incidence divisor missed index product")
    if (
        extension_radical["radical_incidence_index"]
        % extension_incidence_divisor != 0
    ):
        raise AssertionError("nonsplit incidence divisor missed radical index")
    if p_adic_valuation(
        extension_radical["radical_incidence_index"],
        extension_prime,
    ) != extension_degree:
        raise AssertionError("nonsplit radical index did not match degree")

    return {
        "split_family": {
            "order": order,
            "sigma": sigma,
            "template_pair_count": len(family),
            "candidate_primes": candidate_primes,
            "rows": rows,
            "incidence_divisor": incidence_divisor,
            "incidence_divisor_factorization": factorint(incidence_divisor),
            "radical_product_factorization": factorint(radical_product),
            "radical_away_from_order": radical_away_from_order,
            "index_product_factorization": factorint(index_product),
            "height_bound_dominates_index_product": (
                height_bound_product >= index_product
            ),
        },
        "nonsplit_witness": {
            "order": extension_order,
            "sigma": extension_sigma,
            "prime": extension_prime,
            "common_root_degree": extension_degree,
            "incidence_divisor": extension_incidence_divisor,
            "common_ideal_index": extension_ideal["index"],
            "radical_incidence_index": (
                extension_radical["radical_incidence_index"]
            ),
        },
    }


def check_dilation_invariant_row_bound() -> dict[str, Any]:
    prime = 17
    order = 16
    sigma = 4
    complement_size = 6
    primitive_roots = primitive_order_roots(prime, order)
    family: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
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
            family.add(normalized_pair(pair["left"], pair["right"]))

    if set(row_counts_by_root.values()) != {40}:
        raise AssertionError("unexpected root row counts")
    if len(family) != 320:
        raise AssertionError("unexpected dilation-invariant incident family size")

    units = [unit for unit in range(1, order) if gcd(unit, order) == 1]
    for left, right in family:
        for unit in units:
            scaled = normalized_pair(
                scaled_subset(left, unit, order),
                scaled_subset(right, unit, order),
            )
            if scaled not in family:
                raise AssertionError("incident family is not dilation-stable")

    degree_sum = 0
    for left, right in family:
        degree_sum += degree(common_root_gcd_mod(
            left,
            right,
            order,
            sigma,
            prime,
        ))
    if degree_sum != len(primitive_roots) * 40:
        raise AssertionError("unexpected degree-weighted incidence sum")

    orbit_groups: dict[tuple[tuple[int, ...], tuple[int, ...]], set[
        tuple[tuple[int, ...], tuple[int, ...]]
    ]]
    orbit_groups = defaultdict(set)
    for left, right in family:
        orbit_groups[affine_orbit_key(left, right, order)].add((left, right))

    orbit_rows = []
    valuation_budget = 0
    radical_budget = 0
    for representative, members in orbit_groups.items():
        orbit_members = affine_orbit_members(
            representative[0],
            representative[1],
            order,
        )
        if members != orbit_members:
            raise AssertionError("incident family is not a full affine-orbit union")
        common_ideal = common_ideal_index(
            representative[0],
            representative[1],
            order,
            sigma,
        )
        radical = common_ideal_radical_incidence_index(
            representative[0],
            representative[1],
            order,
            sigma,
        )
        valuation = p_adic_valuation(common_ideal["index"], prime)
        radical_valuation = p_adic_valuation(
            radical["radical_incidence_index"],
            prime,
        )
        if valuation <= 0:
            raise AssertionError("incident orbit has zero valuation budget")
        if radical_valuation <= 0:
            raise AssertionError("incident orbit has zero radical budget")
        for member in members:
            member_ideal = common_ideal_index(
                member[0],
                member[1],
                order,
                sigma,
            )
            member_radical = common_ideal_radical_incidence_index(
                member[0],
                member[1],
                order,
                sigma,
            )
            if member_ideal["index"] != common_ideal["index"]:
                raise AssertionError("common-ideal index changed on affine orbit")
            if p_adic_valuation(member_ideal["index"], prime) != valuation:
                raise AssertionError("valuation changed on affine orbit")
            if (
                member_radical["radical_incidence_index"]
                != radical["radical_incidence_index"]
            ):
                raise AssertionError("radical index changed on affine orbit")
            if (
                p_adic_valuation(
                    member_radical["radical_incidence_index"],
                    prime,
                )
                != radical_valuation
            ):
                raise AssertionError("radical valuation changed on affine orbit")
        weighted_budget = len(members) * valuation
        weighted_radical_budget = len(members) * radical_valuation
        valuation_budget += weighted_budget
        radical_budget += weighted_radical_budget
        orbit_rows.append({
            "orbit_size": len(members),
            "representative": [list(representative[0]), list(representative[1])],
            "common_ideal_index": common_ideal["index"],
            "radical_incidence_index": radical["radical_incidence_index"],
            "valuation_at_prime": valuation,
            "radical_valuation_at_prime": radical_valuation,
            "weighted_budget": weighted_budget,
            "weighted_radical_budget": weighted_radical_budget,
        })
    orbit_rows.sort(key=lambda item: (
        item["orbit_size"],
        item["common_ideal_index"],
        item["representative"],
    ))

    if valuation_budget != degree_sum:
        raise AssertionError("valuation budget did not match degree sum")
    if radical_budget != degree_sum:
        raise AssertionError("radical budget did not match degree sum")
    row_bound = valuation_budget // euler_phi(order)
    radical_row_bound = radical_budget // euler_phi(order)
    if valuation_budget % euler_phi(order) != 0:
        raise AssertionError("valuation budget is not divisible by phi(n)")
    if radical_budget % euler_phi(order) != 0:
        raise AssertionError("radical budget is not divisible by phi(n)")
    if row_bound != 40:
        raise AssertionError("unexpected valuation row bound")
    if radical_row_bound != 40:
        raise AssertionError("unexpected radical row bound")
    if any(row_count > row_bound for row_count in row_counts_by_root.values()):
        raise AssertionError("row count exceeded valuation row bound")
    if any(
        row_count > radical_row_bound
        for row_count in row_counts_by_root.values()
    ):
        raise AssertionError("row count exceeded radical row bound")

    return {
        "prime": prime,
        "order": order,
        "sigma": sigma,
        "complement_size": complement_size,
        "primitive_root_count": len(primitive_roots),
        "family_size": len(family),
        "row_counts_by_root": {
            str(root): row_counts_by_root[root]
            for root in sorted(row_counts_by_root)
        },
        "degree_weighted_incidence_sum": degree_sum,
        "valuation_budget": valuation_budget,
        "radical_budget": radical_budget,
        "valuation_row_bound": row_bound,
        "radical_row_bound": radical_row_bound,
        "affine_orbit_count": len(orbit_rows),
        "affine_orbits": orbit_rows,
    }


def check_finite_field_row_fiber_bound() -> dict[str, Any]:
    def assert_unit_dilation_stable(
        family: set[tuple[tuple[int, ...], tuple[int, ...]]],
        order: int,
    ) -> None:
        units = [unit for unit in range(1, order) if gcd(unit, order) == 1]
        for left, right in family:
            for unit in units:
                scaled = normalized_pair(
                    scaled_subset(left, unit, order),
                    scaled_subset(right, unit, order),
                )
                if scaled not in family:
                    raise AssertionError("family is not unit-dilation-stable")

    split_prime = 17
    split_order = 16
    split_sigma = 4
    split_complement_size = 6
    split_roots = primitive_order_roots(split_prime, split_order)
    split_family: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    split_row_counts = {}
    split_max_fibers = {}
    for root in split_roots:
        row = finite_prefix_collision_pairs(
            prime=split_prime,
            order=split_order,
            complement_size=split_complement_size,
            sigma=split_sigma,
            root=root,
        )
        split_row_counts[root] = row["collision_pair_count"]
        split_max_fibers[root] = row["max_fiber"]
        for pair in row["pairs"]:
            split_family.add(normalized_pair(pair["left"], pair["right"]))
    assert_unit_dilation_stable(split_family, split_order)

    split_degree_sum = 0
    split_valuation_budget = 0
    for left, right in split_family:
        certificate = bad_prime_certificate(left, right, split_order, split_sigma)
        if certificate["char_zero_collision"]:
            raise AssertionError("split row-bound test includes char-zero pair")
        common_degree = degree(common_root_gcd_mod(
            left,
            right,
            split_order,
            split_sigma,
            split_prime,
        ))
        common_ideal = common_ideal_index(
            left,
            right,
            split_order,
            split_sigma,
        )
        valuation = p_adic_valuation(common_ideal["index"], split_prime)
        if common_degree > valuation:
            raise AssertionError("split common degree exceeded valuation")
        split_degree_sum += common_degree
        split_valuation_budget += valuation
    split_row_pair_bound = split_valuation_budget // euler_phi(split_order)
    split_max_fiber_bound = max_fiber_bound_from_pair_bound(split_row_pair_bound)
    if split_valuation_budget % euler_phi(split_order) != 0:
        raise AssertionError("split valuation budget is not phi-divisible")
    if set(split_row_counts.values()) != {40}:
        raise AssertionError("unexpected split row counts")
    if split_degree_sum != split_valuation_budget or split_degree_sum != 320:
        raise AssertionError("unexpected split field row budget")
    if split_row_pair_bound != 40 or split_max_fiber_bound != 9:
        raise AssertionError("unexpected split row/fiber bound")
    if max(split_max_fibers.values()) > split_max_fiber_bound:
        raise AssertionError("split max fiber exceeded valuation fiber bound")

    nonsplit_prime = 3
    nonsplit_order = 8
    nonsplit_sigma = 1
    nonsplit_complement_size = 2
    nonsplit_roots = gf9_primitive_order_roots(nonsplit_order)
    non_char_family: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    char_zero_family: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    nonsplit_row_counts = {}
    nonsplit_non_char_row_counts = {}
    nonsplit_char_zero_row_counts = {}
    nonsplit_max_fibers = {}
    for root in nonsplit_roots:
        row = finite_prefix_collision_pairs_gf9(
            order=nonsplit_order,
            complement_size=nonsplit_complement_size,
            sigma=nonsplit_sigma,
            root=root,
        )
        non_char_count = 0
        char_zero_count = 0
        for pair in row["pairs"]:
            key = normalized_pair(pair["left"], pair["right"])
            certificate = bad_prime_certificate(
                key[0],
                key[1],
                nonsplit_order,
                nonsplit_sigma,
            )
            if certificate["char_zero_collision"]:
                char_zero_family.add(key)
                char_zero_count += 1
            else:
                non_char_family.add(key)
                non_char_count += 1
        nonsplit_row_counts[tuple(root)] = row["collision_pair_count"]
        nonsplit_non_char_row_counts[tuple(root)] = non_char_count
        nonsplit_char_zero_row_counts[tuple(root)] = char_zero_count
        nonsplit_max_fibers[tuple(root)] = row["max_fiber"]
    assert_unit_dilation_stable(non_char_family, nonsplit_order)

    nonsplit_degree_sum = 0
    nonsplit_valuation_budget = 0
    for left, right in non_char_family:
        common_degree = degree(common_root_gcd_mod(
            left,
            right,
            nonsplit_order,
            nonsplit_sigma,
            nonsplit_prime,
        ))
        common_ideal = common_ideal_index(
            left,
            right,
            nonsplit_order,
            nonsplit_sigma,
        )
        valuation = p_adic_valuation(common_ideal["index"], nonsplit_prime)
        if common_degree > valuation:
            raise AssertionError("nonsplit common degree exceeded valuation")
        nonsplit_degree_sum += common_degree
        nonsplit_valuation_budget += valuation
    nonsplit_phi = euler_phi(nonsplit_order)
    nonsplit_row_pair_bound = nonsplit_valuation_budget // nonsplit_phi
    structural_pair_bound = max(nonsplit_char_zero_row_counts.values())
    nonsplit_total_pair_bound = structural_pair_bound + nonsplit_row_pair_bound
    nonsplit_max_fiber_bound = max_fiber_bound_from_pair_bound(
        nonsplit_total_pair_bound
    )
    if nonsplit_valuation_budget % nonsplit_phi != 0:
        raise AssertionError("nonsplit valuation budget is not phi-divisible")
    if set(nonsplit_row_counts.values()) != {30}:
        raise AssertionError("unexpected nonsplit row counts")
    if set(nonsplit_non_char_row_counts.values()) != {24}:
        raise AssertionError("unexpected nonsplit non-char-zero counts")
    if set(nonsplit_char_zero_row_counts.values()) != {6}:
        raise AssertionError("unexpected nonsplit char-zero counts")
    if len(non_char_family) != 48 or len(char_zero_family) != 6:
        raise AssertionError("unexpected nonsplit family sizes")
    if (
        nonsplit_degree_sum != nonsplit_valuation_budget
        or nonsplit_degree_sum != 96
    ):
        raise AssertionError("unexpected nonsplit valuation budget")
    if nonsplit_row_pair_bound != 24:
        raise AssertionError("unexpected nonsplit row-pair bound")
    if nonsplit_total_pair_bound != 30 or nonsplit_max_fiber_bound != 8:
        raise AssertionError("unexpected nonsplit fiber bound")
    if max(nonsplit_max_fibers.values()) > nonsplit_max_fiber_bound:
        raise AssertionError("nonsplit max fiber exceeded row/fiber bound")

    return {
        "split_case": {
            "field": "F_17",
            "prime": split_prime,
            "order": split_order,
            "sigma": split_sigma,
            "complement_size": split_complement_size,
            "primitive_root_count": len(split_roots),
            "family_size": len(split_family),
            "row_counts_by_root": {
                str(root): split_row_counts[root]
                for root in sorted(split_row_counts)
            },
            "max_fibers_by_root": {
                str(root): split_max_fibers[root]
                for root in sorted(split_max_fibers)
            },
            "degree_weighted_incidence_sum": split_degree_sum,
            "valuation_budget": split_valuation_budget,
            "row_pair_bound": split_row_pair_bound,
            "max_fiber_bound": split_max_fiber_bound,
        },
        "nonsplit_case": {
            "field": "F_9 = F_3[i]/(i^2+1)",
            "prime": nonsplit_prime,
            "order": nonsplit_order,
            "sigma": nonsplit_sigma,
            "complement_size": nonsplit_complement_size,
            "primitive_root_count": len(nonsplit_roots),
            "non_char_zero_family_size": len(non_char_family),
            "char_zero_family_size": len(char_zero_family),
            "row_counts_by_root": {
                str(root): nonsplit_row_counts[root]
                for root in sorted(nonsplit_row_counts)
            },
            "non_char_zero_counts_by_root": {
                str(root): nonsplit_non_char_row_counts[root]
                for root in sorted(nonsplit_non_char_row_counts)
            },
            "char_zero_counts_by_root": {
                str(root): nonsplit_char_zero_row_counts[root]
                for root in sorted(nonsplit_char_zero_row_counts)
            },
            "max_fibers_by_root": {
                str(root): nonsplit_max_fibers[root]
                for root in sorted(nonsplit_max_fibers)
            },
            "non_char_zero_degree_sum": nonsplit_degree_sum,
            "non_char_zero_valuation_budget": nonsplit_valuation_budget,
            "non_char_zero_row_pair_bound": nonsplit_row_pair_bound,
            "structural_pair_bound": structural_pair_bound,
            "total_pair_bound": nonsplit_total_pair_bound,
            "max_fiber_bound": nonsplit_max_fiber_bound,
        },
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
        base_common_ideal = common_ideal_index(
            template["left"],
            template["right"],
            order,
            sigma,
        )
        base_radical = common_ideal_radical_incidence_index(
            template["left"],
            template["right"],
            order,
            sigma,
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
        if base["certificate"] % base_common_ideal["index"] != 0:
            raise AssertionError("bad affine-invariance base common-ideal index")
        if base_common_ideal["index"] != base_radical["index"]:
            raise AssertionError("bad affine-invariance base radical wrapper")

        checked = 0
        for unit in units:
            for shift in range(order):
                left = affine_subset(template["left"], unit, shift, order)
                right = affine_subset(template["right"], unit, shift, order)
                transformed = bad_prime_certificate(left, right, order, sigma)
                transformed_common_ideal = common_ideal_index(
                    left,
                    right,
                    order,
                    sigma,
                )
                transformed_radical = common_ideal_radical_incidence_index(
                    left,
                    right,
                    order,
                    sigma,
                )
                transformed_degree = degree(common_root_gcd_mod(
                    left,
                    right,
                    order,
                    sigma,
                    template["prime"],
                ))
                if transformed["certificate"] != base["certificate"]:
                    raise AssertionError("certificate changed under affine action")
                if transformed_common_ideal["index"] != base_common_ideal["index"]:
                    raise AssertionError("common-ideal index changed under affine")
                if (
                    transformed_radical["radical_incidence_index"]
                    != base_radical["radical_incidence_index"]
                ):
                    raise AssertionError("radical index changed under affine")
                if transformed_degree != base_degree:
                    raise AssertionError("gcd degree changed under affine action")
                checked += 1
        rows.append({
            "name": template["name"],
            "prime": template["prime"],
            "certificate": base["certificate"],
            "common_ideal_index": base_common_ideal["index"],
            "radical_incidence_index": base_radical["radical_incidence_index"],
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
        "newton_common_ideal_bridge": check_newton_common_ideal_bridge(),
        "newton_radical_incidence_bridge": (
            check_newton_radical_incidence_bridge()
        ),
        "extension_field_bad_prime_certificate": (
            check_extension_field_bad_prime_certificate()
        ),
        "extension_field_row_accounting": check_extension_field_row_accounting(),
        "prefix_depth_filtration": check_prefix_depth_filtration(),
        "prefix_radical_frontier_drop": check_prefix_radical_frontier_drop(),
        "full_prefix_rigidity": check_full_prefix_rigidity(),
        "full_prefix_common_ideal_endpoint": (
            check_full_prefix_common_ideal_endpoint()
        ),
        "split_prime_sweep": check_split_prime_sweep(),
        "bounded_split_prime_row_scan": check_bounded_split_prime_row_scan(),
        "prime_ideal_false_positive": check_prime_ideal_false_positive(),
        "finite_family_exact_aggregation": (
            check_finite_family_exact_aggregation()
        ),
        "valuation_incidence_budget": check_valuation_incidence_budget(),
        "radical_incidence_index": check_radical_incidence_index(),
        "log_weighted_density_budget": check_log_weighted_density_budget(),
        "dilation_invariant_row_bound": check_dilation_invariant_row_bound(),
        "finite_field_row_fiber_bound": check_finite_field_row_fiber_bound(),
        "galois_invariance": check_galois_invariance(),
        "affine_invariance": check_affine_invariance(),
        "nonmutating": True,
        "remaining_open_problem": (
            "bound exact radical incidence budgets, or norm-controlled "
            "common-ideal envelopes, over robustly aperiodic templates"
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
        f"ideal_indices={packet['common_ideal_index_counts']}, "
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
    print(f"aggregate_common_ideal_lcm={packet['aggregate_common_ideal_lcm']}")
    print(f"translation_orbits={len(packet['translation_orbits'])}")
    print(f"affine_orbits={packet['affine_orbit_count']}")
    extension = report["extension_field_bad_prime_certificate"]
    print(
        "extension_field_certificate="
        f"p={extension['base_prime']}, "
        f"degree={extension['extension_degree']}, "
        f"cert={extension['certificate']}, "
        f"ideal_index={extension['common_ideal_index']}, "
        f"gcd_degree={extension['common_factor_degree_mod_3']}"
    )
    extension_accounting = report["extension_field_row_accounting"]
    print(
        "extension_row_accounting="
        f"p={extension_accounting['base_prime']}, "
        f"roots={extension_accounting['primitive_root_count']}, "
        f"fixed_pairs={extension_accounting['fixed_root_collision_pair_count']}, "
        f"incidence_sum={extension_accounting['root_template_incidence_sum']}, "
        f"gcd_degree_sum={extension_accounting['gcd_degree_weighted_sum']}, "
        f"prime_ideal_sum={extension_accounting['prime_ideal_weighted_sum']}"
    )
    bridge = report["newton_power_sum_bridge"]
    print(
        "newton_power_sum_bridge="
        f"f17_pairs={bridge['f17_packet_pairs_checked']}, "
        f"degrees={bridge['f17_degree_counts']}, "
        f"p97_degree={bridge['p97_false_positive_degree']}"
    )
    ideal_bridge = report["newton_common_ideal_bridge"]
    print(
        "newton_common_ideal_bridge="
        f"f17_pairs={ideal_bridge['f17_packet_pairs_checked']}, "
        f"index_pairs={ideal_bridge['f17_index_pair_counts']}, "
        f"condition='{ideal_bridge['condition']}'"
    )
    radical_bridge = report["newton_radical_incidence_bridge"]
    print(
        "newton_radical_incidence_bridge="
        f"f17_pairs={radical_bridge['f17_packet_pairs_checked']}, "
        f"radical_pairs={radical_bridge['f17_radical_pair_counts']}, "
        f"condition='{radical_bridge['condition']}'"
    )
    filtration = report["prefix_depth_filtration"]
    depth_pairs = {
        row["sigma"]: row["collision_pair_count"]
        for row in filtration["row_profile"]
    }
    print(f"prefix_depth_pairs={depth_pairs}")
    frontier = report["prefix_radical_frontier_drop"]
    print(
        "prefix_radical_frontier_drop="
        f"packet_drops={frontier['packet_sigma4_to_5']['frontier_drop_counts']}, "
        "packet_product="
        f"{frontier['packet_sigma4_to_5']['frontier_product_factorization']}, "
        "f9_drop="
        f"{frontier['nonsplit_witness']['frontier_drop_factorization']}"
    )
    full_prefix = report["full_prefix_rigidity"]
    print(
        "full_prefix_rigidity="
        f"primes={full_prefix['primes_checked']}, "
        f"m<={full_prefix['max_complement_size']}, "
        "collisions=0"
    )
    full_index = report["full_prefix_common_ideal_endpoint"]
    print(
        "full_prefix_common_ideal_endpoint="
        f"m<={full_index['exhaustive_max_complement_size']}, "
        f"pairs={full_index['pairs_checked']}, "
        f"max_index={full_index['max_endpoint_index']}, "
        "off_order_support=0"
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
        f"ideal_index={false_positive['common_ideal_index']}, "
        f"gcd_degree={false_positive['common_root_degree']}, "
        f"embedding_count={false_positive['embedding_zero_count']}, "
        f"actual={false_positive['actual_collision_for_any_embedding']}"
    )
    aggregation = report["finite_family_exact_aggregation"]
    split_family = aggregation["split_family"]
    print(
        "finite_family_exact_aggregation="
        f"templates={split_family['template_pair_count']}, "
        f"resultant_split_support={split_family['resultant_split_support']}, "
        f"ideal_split_support={split_family['common_ideal_split_support']}, "
        f"ideal_lcm={split_family['common_ideal_lcm']}"
    )
    valuation = report["valuation_incidence_budget"]["split_family"]
    print(
        "valuation_incidence_budget="
        f"templates={valuation['template_pair_count']}, "
        f"rows={valuation['rows']}"
    )
    radical = report["radical_incidence_index"]
    print(
        "radical_incidence_index="
        f"f17_degree={radical['split_packet']['common_root_degree_sum']}, "
        f"f17_radical={radical['split_packet']['radical_valuation_sum']}, "
        f"dilation_row_bound={radical['split_dilation_family']['row_bound']}, "
        f"f9_degree={radical['nonsplit_family']['common_root_degree_sum']}, "
        f"f9_radical={radical['nonsplit_family']['radical_valuation_sum']}"
    )
    log_budget = report["log_weighted_density_budget"]["split_family"]
    print(
        "log_weighted_density_budget="
        f"templates={log_budget['template_pair_count']}, "
        f"incidence_factors={log_budget['incidence_divisor_factorization']}, "
        f"index_product_factors={log_budget['index_product_factorization']}"
    )
    row_bound = report["dilation_invariant_row_bound"]
    print(
        "dilation_invariant_row_bound="
        f"family={row_bound['family_size']}, "
        f"valuation_budget={row_bound['valuation_budget']}, "
        f"radical_budget={row_bound['radical_budget']}, "
        f"row_bound={row_bound['valuation_row_bound']}, "
        f"radical_row_bound={row_bound['radical_row_bound']}, "
        f"affine_orbits={row_bound['affine_orbit_count']}"
    )
    fiber_bound = report["finite_field_row_fiber_bound"]
    split_bound = fiber_bound["split_case"]
    nonsplit_bound = fiber_bound["nonsplit_case"]
    print(
        "finite_field_row_fiber_bound="
        f"split_row_bound={split_bound['row_pair_bound']}, "
        f"split_fiber_bound={split_bound['max_fiber_bound']}, "
        f"nonsplit_nonchar_bound="
        f"{nonsplit_bound['non_char_zero_row_pair_bound']}, "
        f"nonsplit_fiber_bound={nonsplit_bound['max_fiber_bound']}"
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
