#!/usr/bin/env python3
"""Independent audit of P04cv parity transport and exceptional profiles."""

from __future__ import annotations

import argparse
import itertools
import json
import math
import re
from collections import Counter
from pathlib import Path


ELL = 11


def prime_factors(value: int) -> list[int]:
    output = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            output.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        output.append(value)
    return output


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // factor, prime) != 1
            for factor in factors
        ):
            return candidate
    raise AssertionError("primitive root not found")


def spectrum(
    prime: int, support: list[int], gamma: list[int]
) -> list[int]:
    generator = primitive_root(prime)
    quotient = (prime - 1) // ELL
    zeta = pow(generator, quotient, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ELL)]
    output = []
    for label in range(quotient):
        representative = pow(generator, label, prime)
        values = [
            sum(
                coefficient
                * pow(representative * point % prime, exponent, prime)
                for coefficient, exponent in zip(gamma, support)
            )
            % prime
            for point in subgroup
        ]
        output.append(max(Counter(values).values()))
    return output


def parse_max_fibre_state(output: str) -> tuple[list[int], list[int]]:
    support_match = re.search(r"max_fibre_support=([0-9,]+)", output)
    gamma_match = re.search(r"max_fibre_gamma=([0-9,]+)", output)
    assert support_match and gamma_match
    support = [int(value) for value in support_match.group(1).strip(",").split(",")]
    gamma = [int(value) for value in gamma_match.group(1).strip(",").split(",")]
    assert len(support) == len(gamma) == 5
    return support, gamma


def parity_transport_audit() -> dict[str, object]:
    prime = 331
    generator = primitive_root(prime)
    quotient = (prime - 1) // ELL
    zeta = pow(generator, quotient, prime)
    subgroup = [pow(zeta, index, prime) for index in range(ELL)]
    rows = []
    for support, gamma in (
        ([2, 4, 6, 8, 10], [1, 7, 19, 41, 83]),
        ([1, 3, 5, 7, 9], [1, 11, 23, 47, 97]),
    ):
        original = spectrum(prime, support, gamma)
        reduced = []
        for label in range(quotient):
            representative = pow(generator, label, prime)
            if support[0] % 2 == 0:
                reduced_representative = representative * representative % prime
                values = [
                    sum(
                        gamma[index]
                        * pow(reduced_representative * point % prime, index + 1, prime)
                        for index in range(5)
                    )
                    % prime
                    for point in subgroup
                ]
            else:
                reduced_representative = pow(
                    representative * representative % prime, -1, prime
                )
                reversed_gamma = list(reversed(gamma))
                values = [
                    sum(
                        reversed_gamma[index]
                        * pow(reduced_representative * point % prime, index + 1, prime)
                        for index in range(5)
                    )
                    % prime
                    for point in subgroup
                ]
            reduced.append(max(Counter(values).values()))
        assert original == reduced
        counts = Counter(original)
        assert all(count % 2 == 0 for count in counts.values())
        rows.append(
            {
                "support": support,
                "spectrum_histogram": [
                    [value, count] for value, count in sorted(counts.items())
                ],
            }
        )
    return {"prime": prime, "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    arguments = parser.parse_args()
    certificate = json.loads(arguments.certificate.read_text(encoding="utf-8"))
    assert certificate["schema"] == (
        "P04CV_EXACT_FIVE_PARITY_AND_SIX_FIBRE_REDUCTION_V1"
    )
    gaps = Counter()
    for support in itertools.combinations(range(1, ELL), 5):
        gaps[math.gcd(*(entry - support[0] for entry in support[1:]))] += 1
    assert gaps == Counter({1: 250, 2: 2})

    exceptional_rows = []
    for prime in (199, 419):
        row = certificate["exceptional_censuses"]["complete_available_rows"][
            str(prime)
        ]
        support, gamma = parse_max_fibre_state(row["stdout"])
        values = spectrum(prime, support, gamma)
        histogram = Counter(values)
        expected = (
            Counter({1: 9, 2: 8, 6: 1})
            if prime == 199
            else Counter({1: 32, 2: 5, 6: 1})
        )
        assert histogram == expected
        assert sum(sorted(values, reverse=True)[:6]) <= 20
        exceptional_rows.append(
            {
                "prime": prime,
                "support": support,
                "gamma": gamma,
                "histogram": [
                    [value, count] for value, count in sorted(histogram.items())
                ],
            }
        )

    parity = parity_transport_audit()
    print("P04CV_INDEPENDENT_PARITY_AND_EXCEPTIONAL_AUDIT_V1")
    print("exceptional=" + json.dumps(exceptional_rows, sort_keys=True))
    print("parity=" + json.dumps(parity, sort_keys=True))
    print("PASS_P04CV_INDEPENDENT_PARITY_AND_EXCEPTIONAL_PROFILES")


if __name__ == "__main__":
    main()
