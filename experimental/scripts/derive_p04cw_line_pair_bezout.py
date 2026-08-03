#!/usr/bin/env python3
"""Exact cyclotomic Bezout prototype for P04cw kernel-line pairs.

This is a route-development tool, not yet a promoted uniform certificate.
It works in Q(zeta_11)[t] using ten-coordinate arithmetic and records every
field element inverted by the Euclidean algorithm. Prime divisors of their
norms form a false-negative-free specialization filter for that computation.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path


ELL = 11
DEGREE = 10
KElement = tuple[Fraction, ...]
TPolynomial = list[KElement]
ZERO: KElement = (Fraction(0),) * DEGREE
ONE: KElement = (Fraction(1),) + (Fraction(0),) * (DEGREE - 1)
PERMUTATIONS = list(itertools.permutations(range(5)))


def k_add(first: KElement, second: KElement) -> KElement:
    return tuple(a + b for a, b in zip(first, second))


def k_neg(value: KElement) -> KElement:
    return tuple(-entry for entry in value)


def k_sub(first: KElement, second: KElement) -> KElement:
    return tuple(a - b for a, b in zip(first, second))


def z_times(value: KElement) -> KElement:
    top = value[-1]
    return (-top,) + tuple(value[index - 1] - top for index in range(1, DEGREE))


ZETA_POWERS: list[KElement] = [ONE]
for _ in range(1, 2 * DEGREE - 1):
    ZETA_POWERS.append(z_times(ZETA_POWERS[-1]))


def k_mul(first: KElement, second: KElement) -> KElement:
    output = [Fraction(0)] * DEGREE
    for first_index, first_value in enumerate(first):
        if first_value == 0:
            continue
        for second_index, second_value in enumerate(second):
            if second_value == 0:
                continue
            scale = first_value * second_value
            for index, entry in enumerate(ZETA_POWERS[first_index + second_index]):
                if entry:
                    output[index] += scale * entry
    return tuple(output)


def k_scale(value: KElement, scalar: Fraction) -> KElement:
    return tuple(scalar * entry for entry in value)


def fraction_determinant(matrix: list[list[Fraction]]) -> Fraction:
    work = [row[:] for row in matrix]
    determinant = Fraction(1)
    for column in range(len(work)):
        pivot = next(
            (row for row in range(column, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[pivot], work[column] = work[column], work[pivot]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant *= pivot_value
        for row in range(column + 1, len(work)):
            if work[row][column] == 0:
                continue
            factor = work[row][column] / pivot_value
            for target in range(column, len(work)):
                work[row][target] -= factor * work[column][target]
    return determinant


def multiplication_matrix(value: KElement) -> list[list[Fraction]]:
    columns = []
    for index in range(DEGREE):
        basis = [Fraction(0)] * DEGREE
        basis[index] = Fraction(1)
        columns.append(k_mul(value, tuple(basis)))
    return [
        [columns[column][row] for column in range(DEGREE)]
        for row in range(DEGREE)
    ]


def k_norm(value: KElement) -> Fraction:
    return fraction_determinant(multiplication_matrix(value))


INVERSE_CACHE: dict[KElement, KElement] = {}


def k_inverse(value: KElement) -> KElement:
    if value in INVERSE_CACHE:
        return INVERSE_CACHE[value]
    assert value != ZERO
    matrix = multiplication_matrix(value)
    augmented = [
        matrix[row] + [Fraction(1 if row == 0 else 0)]
        for row in range(DEGREE)
    ]
    rank = 0
    for column in range(DEGREE):
        pivot = next(
            (row for row in range(rank, DEGREE) if augmented[row][column]),
            None,
        )
        assert pivot is not None
        augmented[pivot], augmented[rank] = augmented[rank], augmented[pivot]
        pivot_value = augmented[rank][column]
        augmented[rank] = [entry / pivot_value for entry in augmented[rank]]
        for row in range(DEGREE):
            if row == rank or augmented[row][column] == 0:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(augmented[row], augmented[rank])
            ]
        rank += 1
    inverse = tuple(augmented[row][-1] for row in range(DEGREE))
    assert k_mul(value, inverse) == ONE
    INVERSE_CACHE[value] = inverse
    return inverse


def t_trim(polynomial: TPolynomial) -> TPolynomial:
    while polynomial and polynomial[-1] == ZERO:
        polynomial.pop()
    return polynomial


def t_strip_zero_root(polynomial: TPolynomial) -> tuple[int, TPolynomial]:
    valuation = 0
    while valuation < len(polynomial) and polynomial[valuation] == ZERO:
        valuation += 1
    return valuation, polynomial[valuation:]


def t_divmod(
    dividend: TPolynomial,
    divisor: TPolynomial,
    inverted: list[KElement],
) -> tuple[TPolynomial, TPolynomial]:
    work = dividend[:]
    quotient = [ZERO] * max(1, len(work) - len(divisor) + 1)
    lead = divisor[-1]
    inverted.append(lead)
    lead_inverse = k_inverse(lead)
    while work and len(work) >= len(divisor):
        shift = len(work) - len(divisor)
        coefficient = k_mul(work[-1], lead_inverse)
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[shift + index] = k_sub(
                work[shift + index], k_mul(coefficient, value)
            )
        t_trim(work)
    return t_trim(quotient), t_trim(work)


def t_gcd(
    first: TPolynomial, second: TPolynomial
) -> tuple[TPolynomial, list[KElement]]:
    left = t_trim(first[:])
    right = t_trim(second[:])
    inverted: list[KElement] = []
    while right:
        _, remainder = t_divmod(left, right, inverted)
        left, right = right, remainder
    if not left:
        return [], inverted
    inverted.append(left[-1])
    scale = k_inverse(left[-1])
    return [k_mul(entry, scale) for entry in left], inverted


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[first] > permutation[second]
        for first in range(5)
        for second in range(first + 1, 5)
    )
    return -1 if inversions % 2 else 1


def determinant_monomial_matrix(
    matrix: list[list[tuple[KElement, int]]]
) -> TPolynomial:
    coefficients: dict[int, KElement] = {}
    for permutation in PERMUTATIONS:
        degree = 0
        value = ONE
        for row, column in enumerate(permutation):
            coefficient, exponent = matrix[row][column]
            degree += exponent
            value = k_mul(value, coefficient)
        if permutation_sign(permutation) < 0:
            value = k_neg(value)
        coefficients[degree] = k_add(coefficients.get(degree, ZERO), value)
    output = [ZERO] * (max(coefficients) + 1)
    for degree, value in coefficients.items():
        output[degree] = value
    return t_trim(output)


def difference_coefficient(root: int, base: int, exponent: int) -> KElement:
    return k_sub(
        ZETA_POWERS[(root * exponent) % ELL],
        ZETA_POWERS[(base * exponent) % ELL],
    )


def stacked_minors(
    support: tuple[int, ...],
    first_roots: tuple[int, ...],
    second_roots: tuple[int, ...],
) -> list[tuple[int, TPolynomial]]:
    rows: list[list[tuple[KElement, int]]] = []
    for roots, twisted in ((first_roots, False), (second_roots, True)):
        for row in range(1, 4):
            rows.append(
                [
                    (
                        difference_coefficient(
                            roots[row], roots[0], exponent
                        ),
                        exponent if twisted else 0,
                    )
                    for exponent in support
                ]
            )
    output = []
    for omitted in range(6):
        determinant = determinant_monomial_matrix(
            [row for index, row in enumerate(rows) if index != omitted]
        )
        valuation, stripped = t_strip_zero_root(determinant)
        output.append((valuation, stripped))
    return output


def small_candidate_primes(
    inverted: list[KElement], limit: int
) -> list[int]:
    norms = [k_norm(value) for value in dict.fromkeys(inverted)]
    output = []
    for candidate in range(23, limit + 1, ELL):
        if not is_prime(candidate):
            continue
        if any(
            norm.numerator % candidate == 0
            or norm.denominator % candidate == 0
            for norm in norms
        ):
            output.append(candidate)
    return output


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    for divisor in range(2, math.isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def diagnostic(limit: int) -> dict[str, object]:
    support = (1, 3, 5, 7, 9)
    first_roots = (0, 1, 3, 8)
    second_roots = (0, 2, 4, 8)
    minors = stacked_minors(support, first_roots, second_roots)
    pair = None
    gcd = None
    inverted: list[KElement] = []
    for first, second in itertools.combinations(range(6), 2):
        candidate_gcd, candidate_inverted = t_gcd(
            minors[first][1], minors[second][1]
        )
        if len(candidate_gcd) == 1:
            pair = (first, second)
            gcd = candidate_gcd
            inverted = candidate_inverted
            break
    assert pair is not None and gcd == [ONE]
    norms = [k_norm(value) for value in dict.fromkeys(inverted)]
    candidates = small_candidate_primes(inverted, limit)
    assert 331 in candidates
    return {
        "support": list(support),
        "first_root_class": list(first_roots),
        "second_root_class": list(second_roots),
        "minor_t_valuations": [row[0] for row in minors],
        "minor_degrees_after_stripping": [len(row[1]) - 1 for row in minors],
        "coprime_minor_pair": list(pair),
        "characteristic_zero_gcd": "1 after stripping t-valuations",
        "distinct_inverted_field_elements": len(set(inverted)),
        "maximum_norm_numerator_bits": max(
            abs(value.numerator).bit_length() for value in norms
        ),
        "small_candidate_primes_congruent_to_one_mod_11": candidates,
        "contains_observed_specialization_331": True,
        "scope": (
            "One diagnostic support/root-pair cell only. The candidate list "
            "is a Bezout superset and is not a complete P04cw exceptional set."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1000)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    result = diagnostic(arguments.limit)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print("PASS_P04CW_DIAGNOSTIC_LINE_PAIR_BEZOUT")


if __name__ == "__main__":
    main()
