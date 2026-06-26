#!/usr/bin/env python3
"""Arithmetic checks for the high-agreement adjacent-ledger theorem package.

This script does not verify the algebraic proofs.  It checks the finite
integer thresholds used in the F_17^32, n=512, k=256 corollaries and the
challenge-map pullback ledgers.
"""

from fractions import Fraction
from itertools import combinations, product
from math import ceil
from typing import Any


def challenge_pullback_probability(
    challenge_to_parameter: list[Any], bad_parameters: set[Any]
) -> Fraction:
    if not challenge_to_parameter:
        raise ValueError("empty challenge map")
    bad_count = sum(
        1 for parameter in challenge_to_parameter if parameter in bad_parameters
    )
    return Fraction(bad_count, len(challenge_to_parameter))


def fiber_sizes_descending(challenge_to_parameter: list[Any]) -> list[int]:
    if not challenge_to_parameter:
        raise ValueError("empty challenge map")
    fibers: dict[Any, int] = {}
    for parameter in challenge_to_parameter:
        fibers[parameter] = fibers.get(parameter, 0) + 1
    return sorted(fibers.values(), reverse=True)


def adversarial_fiber_envelope(
    challenge_to_parameter: list[Any], bad_parameter_count: int
) -> Fraction:
    if bad_parameter_count < 0:
        raise ValueError("negative bad parameter count")
    fibers = fiber_sizes_descending(challenge_to_parameter)
    return Fraction(
        sum(fibers[:bad_parameter_count]), len(challenge_to_parameter)
    )


def brute_adversarial_fiber_envelope(
    challenge_to_parameter: list[Any], bad_parameter_count: int
) -> Fraction:
    if bad_parameter_count < 0:
        raise ValueError("negative bad parameter count")
    parameters = list(set(challenge_to_parameter))
    best = Fraction(0, 1)
    for size in range(min(bad_parameter_count, len(parameters)) + 1):
        for bad_tuple in combinations(parameters, size):
            best = max(
                best,
                challenge_pullback_probability(
                    challenge_to_parameter, set(bad_tuple)
                ),
            )
    return best


def challenge_pullback_bound(
    challenge_count: int, bad_parameter_count: int, max_fiber_size: int
) -> Fraction:
    if challenge_count <= 0:
        raise ValueError("nonpositive challenge count")
    if bad_parameter_count < 0:
        raise ValueError("negative bad parameter count")
    if max_fiber_size <= 0:
        raise ValueError("nonpositive max fiber size")
    return Fraction(
        min(challenge_count, bad_parameter_count * max_fiber_size),
        challenge_count,
    )


def poly_eval_mod(coeffs: list[int], x: int, prime: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % prime
        power = (power * x) % prime
    return total


def poly_degree(coeffs: list[int]) -> int:
    for idx in range(len(coeffs) - 1, -1, -1):
        if coeffs[idx] != 0:
            return idx
    raise ValueError("zero polynomial has no degree")


def polynomial_map_values(coeffs: list[int], prime: int) -> list[int]:
    degree = poly_degree([coeff % prime for coeff in coeffs])
    if degree <= 0:
        raise ValueError("constant polynomial map")
    return [poly_eval_mod(coeffs, x, prime) for x in range(prime)]


def rational_map_values(
    numerator: list[int], denominator: list[int], prime: int
) -> list[int | str]:
    degree = max(
        poly_degree([coeff % prime for coeff in numerator]),
        poly_degree([coeff % prime for coeff in denominator]),
    )
    if degree <= 0:
        raise ValueError("constant rational map")

    values: list[int | str] = []
    for x in range(prime):
        den = poly_eval_mod(denominator, x, prime)
        if den == 0:
            values.append("inf")
        else:
            num = poly_eval_mod(numerator, x, prime)
            values.append((num * pow(den, -1, prime)) % prime)
    return values


def matrix_rank_mod(matrix: list[list[int]], prime: int) -> int:
    if not matrix:
        return 0
    width = len(matrix[0])
    rows = [[entry % prime for entry in row] for row in matrix]
    for row in rows:
        if len(row) != width:
            raise ValueError("ragged matrix")

    rank = 0
    for col in range(width):
        pivot = None
        for row_idx in range(rank, len(rows)):
            if rows[row_idx][col] != 0:
                pivot = row_idx
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, prime)
        rows[rank] = [(entry * inv) % prime for entry in rows[rank]]
        for row_idx in range(len(rows)):
            if row_idx == rank or rows[row_idx][col] == 0:
                continue
            factor = rows[row_idx][col]
            rows[row_idx] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(rows[row_idx], rows[rank])
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def linear_map_values(matrix: list[list[int]], prime: int) -> list[tuple[int, ...]]:
    if not matrix:
        raise ValueError("empty matrix")
    domain_dim = len(matrix[0])
    for row in matrix:
        if len(row) != domain_dim:
            raise ValueError("ragged matrix")

    values: list[tuple[int, ...]] = []
    for vector in product(range(prime), repeat=domain_dim):
        values.append(
            tuple(
                sum(row[col] * vector[col] for col in range(domain_dim)) % prime
                for row in matrix
            )
        )
    return values


def check_challenge_pullback_ledgers(target: int) -> None:
    identity = list(range(8))
    assert adversarial_fiber_envelope(identity, 3) == Fraction(3, 8)
    assert adversarial_fiber_envelope(identity, 3) == (
        brute_adversarial_fiber_envelope(identity, 3)
    )

    nonuniform = [0, 0, 0, 1, 1, 2, 3, 4]
    assert fiber_sizes_descending(nonuniform) == [3, 2, 1, 1, 1]
    assert adversarial_fiber_envelope(nonuniform, 2) == Fraction(5, 8)
    assert adversarial_fiber_envelope(nonuniform, 2) == (
        brute_adversarial_fiber_envelope(nonuniform, 2)
    )
    assert challenge_pullback_bound(8, 2, 3) == Fraction(3, 4)

    prime = 17
    polynomial_values = polynomial_map_values([1, 2, 0, 1], prime)
    assert max(fiber_sizes_descending(polynomial_values)) <= 3
    assert adversarial_fiber_envelope(polynomial_values, 2) <= (
        challenge_pullback_bound(prime, 2, 3)
    )

    rational_values = rational_map_values([1, 0, 1], [-3, 1], prime)
    assert max(fiber_sizes_descending(rational_values)) <= 2
    assert adversarial_fiber_envelope(rational_values, 2) <= (
        challenge_pullback_bound(prime, 2, 2)
    )

    base = 5
    rank_one = [[1, 0, 0]]
    rank_one_values = linear_map_values(rank_one, base)
    assert matrix_rank_mod(rank_one, base) == 1
    assert fiber_sizes_descending(rank_one_values) == [base**2] * base
    assert adversarial_fiber_envelope(rank_one_values, 2) == Fraction(2, base)

    rank_two = [[1, 0, 0], [0, 1, 0]]
    rank_two_values = linear_map_values(rank_two, base)
    assert matrix_rank_mod(rank_two, base) == 2
    assert fiber_sizes_descending(rank_two_values) == [base] * (base**2)
    assert adversarial_fiber_envelope(rank_two_values, 3) == Fraction(3, base**2)

    full_rank = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    full_rank_values = linear_map_values(full_rank, base)
    assert matrix_rank_mod(full_rank, base) == 3
    assert max(fiber_sizes_descending(full_rank_values)) == 1
    assert adversarial_fiber_envelope(full_rank_values, 4) == Fraction(4, base**3)

    assert 17**31 < target
    assert (17**31) // target == 0
    assert (17**32) // target == 6

def main() -> None:
    n = 512
    k = 256
    q = 17 ** 32
    target = 2 ** 128
    budget = q // target
    check_challenge_pullback_ledgers(target)

    print("Field and target")
    print(f"q = 17^32 = {q}")
    print(f"floor(q / 2^128) = {budget}")
    print(f"6*2^128 < q: {6*target < q}")
    print(f"7*2^128 > q: {7*target > q}")
    print()

    tangent_start = ceil((2*n + k) / 3)
    list_unique_start = ceil((n + k) / 2)
    print("High-agreement starts")
    print(f"affine/projective line exact start ceil((2n+k)/3) = {tangent_start}")
    print(f"interleaved unique-list start ceil((n+k)/2) = {list_unique_start}")
    print()

    print("Affine/projective line plus interleaved-list ledger")
    for a in [506, 507, 508]:
        line_num = n - a + 1
        list_num = 1 if a >= list_unique_start else None
        total = line_num + (list_num or 0)
        print(
            f"a={a}, r={n-a}: line={line_num}, list={list_num}, "
            f"total={total}, total<=budget? {total <= budget}"
        )
    print()

    print("Degree-d finite-parameter curve ledger")
    print("d | curve exact start | safe with list | safe curve alone")
    for d in range(1, 11):
        curve_start = ceil(((d + 1) * n + k) / (d + 2))

        # With list term: d*(n-a+1)+1 <= budget.
        max_m_with_list = (budget - 1) // d
        if max_m_with_list >= 1:
            a_with_list = n + 1 - max_m_with_list
            safe_with_list = f"a >= {a_with_list} (r <= {n-a_with_list})"
        else:
            safe_with_list = "none"

        # Curve term alone: d*(n-a+1) <= budget.
        max_m_curve = budget // d
        if max_m_curve >= 1:
            a_curve = n + 1 - max_m_curve
            safe_curve = f"a >= {a_curve} (r <= {n-a_curve})"
        else:
            safe_curve = "none"

        print(f"{d:2d} | {curve_start:17d} | {safe_with_list:24s} | {safe_curve}")
    print()

    print("Challenge-map rank ledger")
    print(f"full F_17-rank 32 budget: floor(17^32 / 2^128) = {(17**32)//target}")
    print(f"rank-loss to 31 budget: floor(17^31 / 2^128) = {(17**31)//target}")
    print("challenge pullback ledgers: PASS")

if __name__ == "__main__":
    main()
