#!/usr/bin/env python3
"""Exact characteristic filter for the P04cw five-plus-triple tail.

For each five-root translation class B, the fibre at the normalized quotient
label H fixes a projective quintic P(Z)=sum_(e=1)^5 gamma_e Z^e.  For each
three-root translation class C, two polynomials in the quotient-label ratio t
encode a triple fibre on tH.  Their gcd is saturated by t^11-1.

Every field element inverted by the characteristic-zero Euclidean reductions
is normed and factored.  The resulting prime/cell list is a false-negative-free
specialization filter.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy

import derive_p04cw_line_pair_bezout as bezout


ELL = 11
SUPPORT = (1, 2, 3, 4, 5)


def canonical_translation(roots: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted((root + shift) % ELL for root in roots))
        for shift in range(ELL)
    )


def root_classes(size: int) -> list[tuple[int, ...]]:
    return sorted(
        {
            canonical_translation(roots)
            for roots in itertools.combinations(range(ELL), size)
        }
    )


FIVE_ROOT_CLASSES = root_classes(5)
TRIPLE_ROOT_CLASSES = root_classes(3)
assert len(FIVE_ROOT_CLASSES) == 42
assert len(TRIPLE_ROOT_CLASSES) == 15


def determinant(matrix: list[list[bezout.KElement]]) -> bezout.KElement:
    size = len(matrix)
    output = bezout.ZERO
    for permutation in itertools.permutations(range(size)):
        value = bezout.ONE
        inversions = 0
        for first in range(size):
            for second in range(first + 1, size):
                inversions += permutation[first] > permutation[second]
        for row, column in enumerate(permutation):
            value = bezout.k_mul(value, matrix[row][column])
        output = (
            bezout.k_sub(output, value)
            if inversions % 2
            else bezout.k_add(output, value)
        )
    return output


def anchor_kernel(
    roots: tuple[int, ...]
) -> tuple[tuple[bezout.KElement, ...], bezout.KElement]:
    matrix = [
        [
            bezout.difference_coefficient(roots[row], roots[0], exponent)
            for exponent in SUPPORT
        ]
        for row in range(1, 5)
    ]
    gamma = []
    for omitted in range(5):
        minor = [
            [entry for column, entry in enumerate(row) if column != omitted]
            for row in matrix
        ]
        value = determinant(minor)
        gamma.append(bezout.k_neg(value) if omitted % 2 else value)
    assert any(value != bezout.ZERO for value in gamma)
    pivot = next(value for value in gamma if value != bezout.ZERO)
    return tuple(gamma), pivot


def triple_polynomials(
    gamma: tuple[bezout.KElement, ...], roots: tuple[int, ...]
) -> list[bezout.TPolynomial]:
    output = []
    for row in range(1, 3):
        polynomial = [bezout.ZERO] * (max(SUPPORT) + 1)
        for exponent, coefficient in zip(SUPPORT, gamma):
            difference = bezout.difference_coefficient(
                roots[row], roots[0], exponent
            )
            polynomial[exponent] = bezout.k_mul(coefficient, difference)
        _, stripped = bezout.t_strip_zero_root(polynomial)
        output.append(stripped)
    return output


def same_label_polynomial() -> bezout.TPolynomial:
    output = [bezout.ZERO] * 12
    output[0] = bezout.k_neg(bezout.ONE)
    output[11] = bezout.ONE
    return output


def saturated_gcd(
    polynomials: list[bezout.TPolynomial],
) -> tuple[bezout.TPolynomial, int, list[bezout.KElement]]:
    current, inverted = bezout.t_gcd(polynomials[0], polynomials[1])
    same_label = same_label_polynomial()
    removed_degree = 0
    while current:
        common, step_inverted = bezout.t_gcd(current, same_label)
        inverted.extend(step_inverted)
        if len(common) <= 1:
            break
        current, remainder = bezout.t_divmod(current, common, inverted)
        assert not remainder
        removed_degree += len(common) - 1
    return current, removed_degree, inverted


def factor_integers(
    integers: set[int], cache: dict[int, dict[int, int]]
) -> set[int]:
    output = set()
    for integer in integers:
        if integer not in cache:
            factors = {
                int(prime): int(exponent)
                for prime, exponent in sympy.factorint(integer).items()
            }
            assert math.prod(
                prime**exponent for prime, exponent in factors.items()
            ) == integer
            cache[integer] = factors
        output.update(
            prime for prime in cache[integer] if prime % ELL == 1
        )
    return output


def scan() -> dict[str, object]:
    factor_cache: dict[int, dict[int, int]] = {}
    integer_norms: set[int] = set()
    candidate_primes: set[int] = set()
    specialization_rows = []
    characteristic_zero_rows = []
    anchor_rows = []
    maximum_norm_bits = 0
    inversion_count = 0

    for five_index, five_roots in enumerate(FIVE_ROOT_CLASSES):
        gamma, pivot = anchor_kernel(five_roots)
        assert all(value != bezout.ZERO for value in gamma)
        pivot_norm = bezout.k_norm(pivot)
        anchor_integers = {
            abs(integer)
            for integer in (pivot_norm.numerator, pivot_norm.denominator)
            if abs(integer) > 1
        }
        anchor_candidates = factor_integers(anchor_integers, factor_cache)
        integer_norms.update(anchor_integers)
        candidate_primes.update(anchor_candidates)
        anchor_rows.append(
            {
                "five_root_index": five_index,
                "five_root_class": list(five_roots),
                "pivot_norm": str(pivot_norm),
                "rank_drop_candidate_primes": sorted(anchor_candidates),
            }
        )

        for triple_index, triple_roots in enumerate(TRIPLE_ROOT_CLASSES):
            polynomials = triple_polynomials(gamma, triple_roots)
            residual, removed_degree, inverted = saturated_gcd(polynomials)
            if len(residual) > 1:
                characteristic_zero_rows.append(
                    {
                        "five_root_index": five_index,
                        "triple_root_index": triple_index,
                        "residual_degree": len(residual) - 1,
                        "same_label_degree_removed": removed_degree,
                    }
                )
            unique_inverted = list(dict.fromkeys(inverted))
            inversion_count += len(unique_inverted)
            local_integers = set(anchor_integers)
            for value in unique_inverted:
                norm = bezout.k_norm(value)
                for integer in (abs(norm.numerator), norm.denominator):
                    if integer > 1:
                        local_integers.add(integer)
                        integer_norms.add(integer)
                        maximum_norm_bits = max(
                            maximum_norm_bits, integer.bit_length()
                        )
            local_candidates = factor_integers(local_integers, factor_cache)
            candidate_primes.update(local_candidates)
            if local_candidates:
                specialization_rows.append(
                    {
                        "five_root_index": five_index,
                        "triple_root_index": triple_index,
                        "candidate_primes": sorted(local_candidates),
                    }
                )

    factor_rows = [
        {
            "integer": str(integer),
            "factors": [
                [prime, exponent]
                for prime, exponent in sorted(factor_cache[integer].items())
            ],
        }
        for integer in sorted(integer_norms)
    ]
    serialized = json.dumps(
        factor_rows, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return {
        "schema": "P04CW_FIVE_TRIPLE_FILTER_V1",
        "support": list(SUPPORT),
        "five_root_translation_classes": len(FIVE_ROOT_CLASSES),
        "triple_root_translation_classes": len(TRIPLE_ROOT_CLASSES),
        "five_triple_cells": len(FIVE_ROOT_CLASSES) * len(TRIPLE_ROOT_CLASSES),
        "anchor_rows": anchor_rows,
        "characteristic_zero_nontrivial_rows": characteristic_zero_rows,
        "candidate_primes_congruent_to_one_mod_11": sorted(candidate_primes),
        "candidate_prime_cell_rows": specialization_rows,
        "norm_factorizations": factor_rows,
        "norm_factorization_sha256": hashlib.sha256(serialized).hexdigest(),
        "operation_counts": {
            "distinct_inverted_field_elements_summed_by_cell": inversion_count,
            "unique_norm_integers": len(integer_norms),
            "maximum_norm_integer_bits": maximum_norm_bits,
        },
        "deduction": (
            "Outside the candidate primes, every normalized five-point "
            "fibre has no distinct quotient label carrying a triple fibre "
            "if characteristic_zero_nontrivial_rows is empty."
        ),
        "remaining": (
            "Audit candidate specializations and compute Q^2 spectra of "
            "every exact-five anchor state."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    result = scan()
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(result["schema"])
    print(
        "cells="
        + str(result["five_triple_cells"])
        + " candidates="
        + str(len(result["candidate_primes_congruent_to_one_mod_11"]))
        + " char0_nontrivial="
        + str(len(result["characteristic_zero_nontrivial_rows"]))
    )
    print("PASS_P04CW_FIVE_TRIPLE_FILTER")


if __name__ == "__main__":
    main()
