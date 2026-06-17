#!/usr/bin/env python3
"""Verify the F_17 aperiodic monomial-prefix collision certificate.

The certificate is a finite L1 route cut: after generated-field entropy clears
and the Paper B quotient-core profile is empty, the monomial-prefix map
Phi_4 on 10-subsets of F_17^* still has aperiodic finite-field collisions.
The maximum fiber size in this toy instance is only 2, so this does not refute
the prefix local-limit target; it refutes an aperiodic-injectivity route.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from math import comb, gcd, log2
from typing import Any, Iterable


STATUS = "PROVED finite certificate; COUNTEREXAMPLE to injectivity route"
P = 17
N = 16
K = 6
SIGMA = 4
AGREEMENT = K + SIGMA
GENERATOR = 3
EXAMPLE_PREFIX = (8, 12, 13, 7)
EXAMPLE_S = (1, 2, 3, 4, 5, 6, 7, 9, 10, 12)
EXAMPLE_T = (1, 2, 3, 8, 10, 11, 13, 14, 15, 16)
EXPECTED_HISTOGRAM = {1: 7928, 2: 40}


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


def domain() -> list[int]:
    values = list(range(1, P))
    generated = {pow(GENERATOR, exponent, P) for exponent in range(N)}
    if generated != set(values):
        raise ValueError("GENERATOR is not primitive in F_17^*")
    return values


def elementary_prefix(support: Iterable[int]) -> tuple[int, ...]:
    coeffs = [0] * (SIGMA + 1)
    coeffs[0] = 1
    for value in support:
        for index in range(SIGMA, 0, -1):
            coeffs[index] = (
                coeffs[index] + coeffs[index - 1] * value
            ) % P
    return tuple(coeffs[1:])


def trim_poly(poly: list[int]) -> list[int]:
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def poly_degree(poly: list[int]) -> int:
    return len(trim_poly(poly[:])) - 1


def poly_sub(left: list[int], right: list[int]) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        left_coeff = left[index] if index < len(left) else 0
        right_coeff = right[index] if index < len(right) else 0
        out[index] = (left_coeff - right_coeff) % P
    return trim_poly(out)


def poly_eval(poly: list[int], value: int) -> int:
    total = 0
    for coeff in reversed(poly):
        total = (total * value + coeff) % P
    return total


def multiply_by_linear(poly: list[int], root: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for index, coeff in enumerate(poly):
        out[index] = (out[index] - root * coeff) % P
        out[index + 1] = (out[index + 1] + coeff) % P
    return trim_poly(out)


def locator_polynomial(support: Iterable[int]) -> list[int]:
    poly = [1]
    for value in support:
        poly = multiply_by_linear(poly, value)
    return poly


def monomial_prefix_polynomial(prefix: tuple[int, ...]) -> list[int]:
    poly = [0] * (AGREEMENT + 1)
    poly[AGREEMENT] = 1
    for index, coeff in enumerate(prefix, start=1):
        sign = -1 if index % 2 else 1
        poly[AGREEMENT - index] = (sign * coeff) % P
    return poly


def codeword_from_support(prefix: tuple[int, ...], support: Iterable[int]) -> list[int]:
    return poly_sub(
        monomial_prefix_polynomial(prefix),
        locator_polynomial(support),
    )


def subgroup(order: int) -> set[int]:
    if N % order != 0:
        raise ValueError("order must divide N")
    step = N // order
    return {pow(GENERATOR, step * exponent, P) for exponent in range(order)}


def cosets_of_subgroup(order: int) -> list[set[int]]:
    kernel = subgroup(order)
    remaining = set(domain())
    cosets: list[set[int]] = []
    while remaining:
        representative = next(iter(remaining))
        coset = {(representative * value) % P for value in kernel}
        cosets.append(coset)
        remaining -= coset
    return cosets


def is_union_of_cosets(values: set[int], order: int) -> bool:
    return all(
        not (values & coset) or coset <= values
        for coset in cosets_of_subgroup(order)
    )


def active_quotient_cores() -> list[int]:
    out: list[int] = []
    for order in positive_divisors(gcd(N, K)):
        if order > 1 and SIGMA < order and K // order <= N // order - 1:
            out.append(order)
    return out


def prefix_fibers() -> dict[tuple[int, ...], list[tuple[int, ...]]]:
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for support in itertools.combinations(domain(), AGREEMENT):
        fibers[elementary_prefix(support)].append(support)
    return fibers


def verify_example(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    example_fiber = fibers[EXAMPLE_PREFIX]
    if sorted(example_fiber) != sorted([EXAMPLE_S, EXAMPLE_T]):
        raise AssertionError("example fiber mismatch")

    word = monomial_prefix_polynomial(EXAMPLE_PREFIX)
    codewords = []
    for support in (EXAMPLE_S, EXAMPLE_T):
        codeword = codeword_from_support(EXAMPLE_PREFIX, support)
        if poly_degree(codeword) >= K:
            raise AssertionError("example codeword has degree >= k")
        for value in support:
            if poly_eval(codeword, value) != poly_eval(word, value):
                raise AssertionError("example codeword does not agree on support")
        codewords.append(codeword)

    return {
        "prefix": EXAMPLE_PREFIX,
        "supports": [list(EXAMPLE_S), list(EXAMPLE_T)],
        "word_coefficients_low_to_high": word,
        "codeword_coefficients_low_to_high": codewords,
        "codeword_degrees": [poly_degree(codeword) for codeword in codewords],
    }


def collision_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    quotient_exception_orders = [
        order for order in positive_divisors(N) if order > SIGMA
    ]
    collisions = []
    all_aperiodic = True
    for prefix, supports in sorted(fibers.items()):
        if len(supports) == 1:
            continue
        if len(supports) != 2:
            raise AssertionError("unexpected fiber size above two")
        first = set(supports[0])
        second = set(supports[1])
        difference = first ^ second
        union_flags = {
            str(order): is_union_of_cosets(difference, order)
            for order in quotient_exception_orders
        }
        if any(union_flags.values()):
            all_aperiodic = False
        collisions.append(
            {
                "prefix": prefix,
                "symmetric_difference_size": len(difference),
                "quotient_union_flags": union_flags,
            }
        )

    return {
        "quotient_exception_orders_checked": quotient_exception_orders,
        "collision_fibers": len(collisions),
        "all_collision_fibers_aperiodic": all_aperiodic,
        "symmetric_difference_histogram": dict(
            sorted(
                Counter(
                    row["symmetric_difference_size"] for row in collisions
                ).items()
            )
        ),
    }


def build_certificate() -> dict[str, Any]:
    fibers = prefix_fibers()
    histogram = Counter(len(values) for values in fibers.values())
    entropy_margin = SIGMA * log2(P) - log2(comb(N, AGREEMENT))

    if dict(histogram) != EXPECTED_HISTOGRAM:
        raise AssertionError("unexpected prefix fiber histogram")
    if entropy_margin <= 0:
        raise AssertionError("entropy margin should be positive")
    if active_quotient_cores():
        raise AssertionError("quotient-core profile should be empty")

    collisions = collision_report(fibers)
    if not collisions["all_collision_fibers_aperiodic"]:
        raise AssertionError("found quotient-periodic collision")

    return {
        "status": STATUS,
        "inputs": {
            "field": "F_17",
            "p": P,
            "domain": "F_17^*",
            "n": N,
            "k": K,
            "sigma": SIGMA,
            "agreement": AGREEMENT,
            "generator": GENERATOR,
        },
        "entropy_ledger": {
            "margin_bits": entropy_margin,
            "clears": entropy_margin > 0,
        },
        "quotient_core_ledger": {
            "gcd_n_k": gcd(N, K),
            "active_quotient_cores": active_quotient_cores(),
            "empty": not active_quotient_cores(),
        },
        "prefix_distribution": {
            "total_supports": comb(N, AGREEMENT),
            "distinct_prefix_values": len(fibers),
            "fiber_size_histogram": dict(sorted(histogram.items())),
            "maximum_fiber_size": max(histogram),
        },
        "collision_report": collisions,
        "example": verify_example(fibers),
        "passed": True,
    }


def print_text(cert: dict[str, Any]) -> None:
    inputs = cert["inputs"]
    distribution = cert["prefix_distribution"]
    collisions = cert["collision_report"]
    print("L1 aperiodic prefix-collision certificate")
    print(f"Status: {cert['status']}")
    print(
        "p={p}, n={n}, k={k}, sigma={sigma}, agreement={agreement}".format(
            **inputs
        )
    )
    print(
        "entropy margin bits: "
        f"{cert['entropy_ledger']['margin_bits']:.6f}"
    )
    print(
        "active quotient cores: "
        f"{cert['quotient_core_ledger']['active_quotient_cores']}"
    )
    print(f"total supports: {distribution['total_supports']}")
    print(f"distinct prefix values: {distribution['distinct_prefix_values']}")
    print(f"fiber histogram: {distribution['fiber_size_histogram']}")
    print(f"maximum fiber size: {distribution['maximum_fiber_size']}")
    print(f"collision fibers: {collisions['collision_fibers']}")
    print(
        "all collision fibers aperiodic for orders "
        f"{collisions['quotient_exception_orders_checked']}: "
        f"{collisions['all_collision_fibers_aperiodic']}"
    )
    print(
        "symmetric-difference histogram: "
        f"{collisions['symmetric_difference_histogram']}"
    )
    print(f"example prefix: {cert['example']['prefix']}")
    print("passed: True")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    cert = build_certificate()
    if args.format == "json":
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print_text(cert)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
