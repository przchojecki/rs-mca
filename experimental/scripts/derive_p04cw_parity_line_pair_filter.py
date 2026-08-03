#!/usr/bin/env python3
"""Exact characteristic filter for the P04cw reduced parity quintic.

The script scans all unordered pairs of four-root translation classes for the
single reduced support A={1,2,3,4,5}. After saturation by t^11-1, every
characteristic-zero stacked-minor gcd is constant. Diagonal cells can contain
repeated powers of t-1, but these still represent the same quotient label.
The script records a false-negative-free set of prime characteristics where
concurrency between genuinely distinct labels may specialize.
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


ROOT_CLASSES = sorted(
    {
        canonical_translation(roots)
        for roots in itertools.combinations(range(ELL), 4)
    }
)
assert len(ROOT_CLASSES) == 30


def t_same_label_polynomial() -> bezout.TPolynomial:
    output = [bezout.ZERO] * 12
    output[0] = bezout.k_neg(bezout.ONE)
    output[11] = bezout.ONE
    return output


def residual_degree(
    gcd: bezout.TPolynomial,
) -> tuple[int, int, list[bezout.KElement]]:
    same_label = t_same_label_polynomial()
    quotient = gcd[:]
    inverted: list[bezout.KElement] = []
    saturated_degree = 0
    while quotient:
        trivial, step_inverted = bezout.t_gcd(quotient, same_label)
        inverted.extend(step_inverted)
        if len(trivial) <= 1:
            break
        quotient, remainder = bezout.t_divmod(
            quotient, trivial, inverted
        )
        assert remainder == []
        saturated_degree += len(trivial) - 1
    return saturated_degree, len(quotient) - 1, inverted


def scan() -> dict[str, object]:
    integer_norms: set[int] = set()
    characteristic_zero_rows = []
    operation_rows = []
    specialization_rows = []
    factor_cache: dict[int, dict[int, int]] = {}
    candidate_primes: set[int] = set()
    cells = 0
    total_minors = 0
    total_euclidean_inversions = 0
    maximum_minor_degree = 0
    maximum_norm_bits = 0

    for first_index, second_index in itertools.combinations_with_replacement(
        range(len(ROOT_CLASSES)), 2
    ):
        first = ROOT_CLASSES[first_index]
        second = ROOT_CLASSES[second_index]
        minors = bezout.stacked_minors(SUPPORT, first, second)
        current = minors[0][1]
        inverted: list[bezout.KElement] = []
        for _, polynomial in minors[1:]:
            current, step_inverted = bezout.t_gcd(current, polynomial)
            inverted.extend(step_inverted)
            if len(current) == 1:
                break
        trivial_degree, nontrivial_degree, cleanup_inverted = residual_degree(
            current
        )
        inverted.extend(cleanup_inverted)
        if nontrivial_degree > 0:
            characteristic_zero_rows.append(
                {
                    "first_root_class": list(first),
                    "second_root_class": list(second),
                    "gcd_degree": len(current) - 1,
                    "same_label_degree": trivial_degree,
                    "nontrivial_degree": nontrivial_degree,
                }
            )

        unique_inverted = list(dict.fromkeys(inverted))
        norms = [bezout.k_norm(value) for value in unique_inverted]
        local_norm_integers: set[int] = set()
        for norm in norms:
            for integer in (abs(norm.numerator), norm.denominator):
                if integer > 1:
                    integer_norms.add(integer)
                    local_norm_integers.add(integer)
                    maximum_norm_bits = max(
                        maximum_norm_bits, integer.bit_length()
                    )
        local_candidates: set[int] = set()
        for integer in local_norm_integers:
            if integer not in factor_cache:
                factors = {
                    int(prime): int(exponent)
                    for prime, exponent in sympy.factorint(integer).items()
                }
                assert math.prod(
                    prime**exponent
                    for prime, exponent in factors.items()
                ) == integer
                factor_cache[integer] = factors
            local_candidates.update(
                prime
                for prime in factor_cache[integer]
                if prime % ELL == 1
            )
        candidate_primes.update(local_candidates)
        if local_candidates:
            specialization_rows.append(
                {
                    "first_root_index": first_index,
                    "second_root_index": second_index,
                    "candidate_primes": sorted(local_candidates),
                }
            )
        cells += 1
        total_minors += len(minors)
        total_euclidean_inversions += len(unique_inverted)
        maximum_minor_degree = max(
            maximum_minor_degree,
            *(len(polynomial) - 1 for _, polynomial in minors),
        )
        if cells % 50 == 0:
            operation_rows.append(
                {
                    "cells": cells,
                    "unique_norm_integers": len(integer_norms),
                    "characteristic_zero_nontrivial": len(
                        characteristic_zero_rows
                    ),
                }
            )

    factor_rows = []
    for integer in sorted(integer_norms):
        factors = factor_cache[integer]
        factor_rows.append(
            {
                "integer": str(integer),
                "factors": [
                    [prime, exponent]
                    for prime, exponent in sorted(factors.items())
                ],
            }
        )

    serialized_factors = json.dumps(
        factor_rows, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    return {
        "schema": "P04CW_PARITY_LINE_PAIR_FILTER_V1",
        "support": list(SUPPORT),
        "root_translation_classes": len(ROOT_CLASSES),
        "unordered_root_class_pairs": cells,
        "stacked_five_by_five_minors": total_minors,
        "characteristic_zero_nontrivial_rows": characteristic_zero_rows,
        "candidate_primes_congruent_to_one_mod_11": sorted(candidate_primes),
        "candidate_prime_cell_rows": specialization_rows,
        "norm_factorizations": factor_rows,
        "norm_factorization_sha256": hashlib.sha256(
            serialized_factors
        ).hexdigest(),
        "operation_counts": {
            "distinct_inverted_field_elements_summed_by_cell": (
                total_euclidean_inversions
            ),
            "unique_norm_integers": len(integer_norms),
            "maximum_minor_degree": maximum_minor_degree,
            "maximum_norm_integer_bits": maximum_norm_bits,
            "progress_checkpoints": operation_rows,
        },
        "deduction": (
            "Outside the candidate primes, two distinct quotient labels "
            "cannot both have fibre at least four for the reduced quintic; "
            "all powers supported on t^11=1 have been saturated away."
        ),
        "remaining": (
            "Audit every candidate characteristic and separately classify "
            "the tail after a five-point fibre to prove S3(P|Q^2)<=10."
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
    print("P04CW_PARITY_LINE_PAIR_FILTER_V1")
    print(
        "cells="
        + str(result["unordered_root_class_pairs"])
        + " candidates="
        + str(len(result["candidate_primes_congruent_to_one_mod_11"]))
        + " char0_nontrivial="
        + str(len(result["characteristic_zero_nontrivial_rows"]))
    )
    print("PASS_P04CW_PARITY_LINE_PAIR_FILTER")


if __name__ == "__main__":
    main()
