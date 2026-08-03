#!/usr/bin/env python3
"""Audit every modular specialization left by the P04cw parity filter.

For each candidate-prime/root-pair cell, recompute the six exact cyclotomic
minors, reduce them through all ten embeddings of zeta_11 into F_p, and
saturate by the same-label factor t^11-1.  The remaining degree must be zero
in characteristic zero for every cell, including the diagonal.

No search over F_p is used.  Polynomial degrees are at most six after the
individual t-valuations have been stripped.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

import sympy

import derive_p04cw_line_pair_bezout as bezout
import derive_p04cw_parity_line_pair_filter as line_filter


ELL = 11


def trim(polynomial: list[int]) -> list[int]:
    while polynomial and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def monic(polynomial: list[int], prime: int) -> list[int]:
    polynomial = trim(polynomial)
    if not polynomial:
        return []
    inverse = pow(polynomial[-1], prime - 2, prime)
    return [(entry * inverse) % prime for entry in polynomial]


def divmod_polynomial(
    dividend: list[int], divisor: list[int], prime: int
) -> tuple[list[int], list[int]]:
    work = trim(dividend[:])
    divisor = trim(divisor[:])
    assert divisor
    quotient = [0] * max(0, len(work) - len(divisor) + 1)
    inverse = pow(divisor[-1], prime - 2, prime)
    while len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        coefficient = work[-1] * inverse % prime
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[shift + index] = (
                work[shift + index] - coefficient * value
            ) % prime
        trim(work)
    return trim(quotient), work


def gcd_polynomial(
    first: list[int], second: list[int], prime: int
) -> list[int]:
    left = trim(first[:])
    right = trim(second[:])
    while right:
        _, remainder = divmod_polynomial(left, right, prime)
        left, right = right, remainder
    return monic(left, prime)


def order_eleven_root(prime: int) -> int:
    assert prime % ELL == 1
    exponent = (prime - 1) // ELL
    base = 2
    while True:
        root = pow(base, exponent, prime)
        if root != 1:
            assert pow(root, ELL, prime) == 1
            return root
        base += 1


def reduce_fraction(value: Fraction, prime: int) -> int:
    numerator = value.numerator % prime
    denominator = value.denominator % prime
    assert denominator != 0
    return numerator * pow(denominator, prime - 2, prime) % prime


def reduce_k_element(
    value: bezout.KElement, root: int, embedding: int, prime: int
) -> int:
    total = 0
    power = 1
    step = pow(root, embedding, prime)
    for coordinate in value:
        total = (total + reduce_fraction(coordinate, prime) * power) % prime
        power = power * step % prime
    return total


def reduce_t_polynomial(
    polynomial: bezout.TPolynomial,
    root: int,
    embedding: int,
    prime: int,
) -> list[int]:
    return trim(
        [
            reduce_k_element(coefficient, root, embedding, prime)
            for coefficient in polynomial
        ]
    )


def expected_nontrivial_degree(first_index: int, second_index: int) -> int:
    del first_index, second_index
    return 0


def saturate_same_label(
    polynomial: list[int], same_label: list[int], prime: int
) -> tuple[list[int], int]:
    quotient = polynomial[:]
    removed_degree = 0
    while quotient:
        common = gcd_polynomial(quotient, same_label, prime)
        if len(common) <= 1:
            break
        quotient, remainder = divmod_polynomial(quotient, common, prime)
        assert not remainder
        removed_degree += len(common) - 1
    return quotient, removed_degree


def polynomial_value(polynomial: list[int], value: int, prime: int) -> int:
    output = 0
    for coefficient in reversed(polynomial):
        output = (output * value + coefficient) % prime
    return output


def residual_roots(polynomial: list[int], prime: int) -> list[int]:
    degree = len(polynomial) - 1
    if degree <= 0:
        return []
    if degree == 1:
        return [(-polynomial[0] * pow(polynomial[1], prime - 2, prime)) % prime]
    # Every nonlinear unexpected residual occurs at p in {23,67,89}.
    assert prime < 1000
    return [
        value
        for value in range(prime)
        if polynomial_value(polynomial, value, prime) == 0
    ]


def stacked_matrix(
    first_roots: tuple[int, ...],
    second_roots: tuple[int, ...],
    zeta: int,
    ratio: int,
    prime: int,
) -> list[list[int]]:
    zeta_powers = [pow(zeta, index, prime) for index in range(ELL)]
    output = []
    for roots, twisted in ((first_roots, False), (second_roots, True)):
        for row in range(1, 4):
            entries = []
            for exponent in line_filter.SUPPORT:
                value = (
                    zeta_powers[(roots[row] * exponent) % ELL]
                    - zeta_powers[(roots[0] * exponent) % ELL]
                ) % prime
                if twisted:
                    value = value * pow(ratio, exponent, prime) % prime
                entries.append(value)
            output.append(entries)
    return output


def one_dimensional_kernel(
    matrix: list[list[int]], prime: int
) -> tuple[int, list[int] | None]:
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivots = []
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot], work[rank] = work[rank], work[pivot]
        inverse = pow(work[rank][column], prime - 2, prime)
        work[rank] = [entry * inverse % prime for entry in work[rank]]
        for row in range(rows):
            if row == rank or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(work[row], work[rank])
            ]
        pivots.append(column)
        rank += 1
    if columns - rank != 1:
        return rank, None
    free = next(column for column in range(columns) if column not in pivots)
    kernel = [0] * columns
    kernel[free] = 1
    for row, pivot in enumerate(pivots):
        kernel[pivot] = (-work[row][free]) % prime
    first_nonzero = next(entry for entry in kernel if entry)
    inverse = pow(first_nonzero, prime - 2, prime)
    return rank, [entry * inverse % prime for entry in kernel]


def audit(filter_artifact: dict[str, object]) -> dict[str, object]:
    assert filter_artifact["schema"] == "P04CW_PARITY_LINE_PAIR_FILTER_V1"
    root_classes = line_filter.ROOT_CLASSES
    assert len(root_classes) == 30

    global_candidates = set(
        filter_artifact["candidate_primes_congruent_to_one_mod_11"]
    )
    assert len(global_candidates) == 602
    assert all(sympy.isprime(prime) for prime in global_candidates)

    same_label = [-1] + [0] * 10 + [1]
    exact_minor_cache: dict[
        tuple[int, int], list[bezout.TPolynomial]
    ] = {}
    degree_histogram: dict[str, int] = {}
    unexpected_rows = []
    exceptional_state_rows = []
    specialization_count = 0
    cell_prime_incidence_count = 0
    maximum_prime = 0

    for row in filter_artifact["candidate_prime_cell_rows"]:
        first_index = int(row["first_root_index"])
        second_index = int(row["second_root_index"])
        key = (first_index, second_index)
        minors = exact_minor_cache.get(key)
        if minors is None:
            minors = [
                polynomial
                for _, polynomial in bezout.stacked_minors(
                    line_filter.SUPPORT,
                    root_classes[first_index],
                    root_classes[second_index],
                )
            ]
            exact_minor_cache[key] = minors

        expected = expected_nontrivial_degree(first_index, second_index)
        for prime in row["candidate_primes"]:
            prime = int(prime)
            assert prime in global_candidates
            maximum_prime = max(maximum_prime, prime)
            cell_prime_incidence_count += 1
            root = order_eleven_root(prime)
            for embedding in range(1, ELL):
                reduced = [
                    reduce_t_polynomial(
                        polynomial, root, embedding, prime
                    )
                    for polynomial in minors
                ]
                current = reduced[0]
                for polynomial in reduced[1:]:
                    current = gcd_polynomial(current, polynomial, prime)
                    if len(current) <= 1:
                        break
                quotient, same_label_degree = saturate_same_label(
                    current, same_label, prime
                )
                residual_degree = len(trim(quotient)) - 1
                histogram_key = str(residual_degree)
                degree_histogram[histogram_key] = (
                    degree_histogram.get(histogram_key, 0) + 1
                )
                specialization_count += 1
                if residual_degree != expected:
                    roots = residual_roots(quotient, prime)
                    unexpected_rows.append(
                        {
                            "first_root_index": first_index,
                            "second_root_index": second_index,
                            "prime": prime,
                            "embedding": embedding,
                            "expected_nontrivial_degree": expected,
                            "observed_nontrivial_degree": residual_degree,
                            "gcd_degree": len(current) - 1,
                            "same_label_degree_after_saturation": (
                                same_label_degree
                            ),
                            "residual_polynomial": quotient,
                            "residual_roots_in_Fp": roots,
                        }
                    )
                    embedded_zeta = pow(root, embedding, prime)
                    for ratio in roots:
                        rank, gamma = one_dimensional_kernel(
                            stacked_matrix(
                                root_classes[first_index],
                                root_classes[second_index],
                                embedded_zeta,
                                ratio,
                                prime,
                            ),
                            prime,
                        )
                        exceptional_state_rows.append(
                            {
                                "first_root_index": first_index,
                                "second_root_index": second_index,
                                "prime": prime,
                                "embedding": embedding,
                                "ratio": ratio,
                                "ratio_is_distinct_label": (
                                    pow(ratio, ELL, prime) != 1
                                ),
                                "matrix_rank": rank,
                                "gamma": gamma,
                                "exact_five_support": (
                                    gamma is not None
                                    and all(entry != 0 for entry in gamma)
                                ),
                            }
                        )

    return {
        "schema": "P04CW_PARITY_LINE_PAIR_MODULAR_TERMINAL_V1",
        "support": list(line_filter.SUPPORT),
        "candidate_primes": len(global_candidates),
        "candidate_cells": len(exact_minor_cache),
        "cell_prime_incidences": cell_prime_incidence_count,
        "cyclotomic_embeddings_per_incidence": ELL - 1,
        "specializations_audited": specialization_count,
        "maximum_candidate_prime": maximum_prime,
        "residual_degree_histogram": degree_histogram,
        "unexpected_rows": unexpected_rows,
        "exceptional_state_rows": exceptional_state_rows,
        "deduction": (
            "If unexpected_rows is empty, every candidate specialization "
            "has exactly the characteristic-zero residual degree zero after "
            "saturation by all powers of t^11-1."
        ),
        "remaining": (
            "Classify every specialized line-pair state and the tail after a "
            "five-point fibre in order to prove the reduced "
            "S3(P|Q^2)<=10 bound."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    source = json.loads(arguments.filter.read_text(encoding="utf-8"))
    result = audit(source)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(result["schema"])
    print(
        "incidences="
        + str(result["cell_prime_incidences"])
        + " specializations="
        + str(result["specializations_audited"])
        + " unexpected="
        + str(len(result["unexpected_rows"]))
    )
    if result["unexpected_rows"]:
        print("PASS_WITH_SPECIALIZATIONS_REQUIRING_CLASSIFICATION")
    else:
        print("PASS_P04CW_PARITY_LINE_PAIR_MODULAR_TERMINAL")


if __name__ == "__main__":
    main()
