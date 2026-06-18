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
EXPECTED_ORBIT_SIZES = (8, 16, 16)
EXPECTED_ORBIT_REPRESENTATIVES = (
    {
        "orbit_size": 16,
        "complements": (
            (1, 2, 3, 4, 6, 9),
            (5, 8, 10, 11, 12, 13),
        ),
        "linear_gap": {"alpha": 3, "beta": 13},
    },
    {
        "orbit_size": 16,
        "complements": (
            (1, 2, 4, 11, 14, 15),
            (6, 8, 9, 12, 13, 16),
        ),
        "linear_gap": {"alpha": 16, "beta": 5},
    },
    {
        "orbit_size": 8,
        "complements": (
            (1, 2, 5, 6, 7, 13),
            (4, 10, 11, 12, 15, 16),
        ),
        "linear_gap": {"alpha": 13, "beta": 0},
    },
)


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


def poly_remainder(poly: list[int], divisor: list[int]) -> list[int]:
    rem = trim_poly(poly[:])
    div = trim_poly(divisor[:])
    if not div:
        raise ValueError("divisor must be nonzero")
    inverse_lead = pow(div[-1], -1, P)
    while rem and len(rem) >= len(div):
        shift = len(rem) - len(div)
        scale = (rem[-1] * inverse_lead) % P
        for index, coeff in enumerate(div):
            rem[index + shift] = (rem[index + shift] - scale * coeff) % P
        trim_poly(rem)
    return rem


def divides_xn_minus_one(poly: list[int]) -> bool:
    xn_minus_one = [P - 1] + [0] * (N - 1) + [1]
    return not poly_remainder(xn_minus_one, poly)


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


def support_complement(support: Iterable[int]) -> tuple[int, ...]:
    return tuple(sorted(set(domain()) - set(support)))


def scale_support(support: Iterable[int], scalar: int) -> tuple[int, ...]:
    return tuple(sorted((scalar * value) % P for value in support))


def normalize_pair(
    first: Iterable[int],
    second: Iterable[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    first_tuple = tuple(sorted(first))
    second_tuple = tuple(sorted(second))
    ordered = sorted((first_tuple, second_tuple))
    return ordered[0], ordered[1]


def orbit_key(
    first: Iterable[int],
    second: Iterable[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    return min(
        normalize_pair(
            scale_support(first, scalar),
            scale_support(second, scalar),
        )
        for scalar in domain()
    )


def linear_locator_gap(
    first: Iterable[int],
    second: Iterable[int],
) -> dict[str, int]:
    first_locator = locator_polynomial(first)
    second_locator = locator_polynomial(second)
    size = max(len(first_locator), len(second_locator))
    difference = []
    for index in range(size):
        first_coeff = first_locator[index] if index < len(first_locator) else 0
        second_coeff = second_locator[index] if index < len(second_locator) else 0
        difference.append((first_coeff - second_coeff) % P)
    if any(difference[index] for index in range(2, len(difference))):
        raise AssertionError("locator gap is not linear")
    return {
        "alpha": difference[1] if len(difference) > 1 else 0,
        "beta": difference[0] if difference else 0,
    }


def pair_stabilizer(
    first: Iterable[int],
    second: Iterable[int],
) -> list[int]:
    normalized = normalize_pair(first, second)
    return [
        scalar
        for scalar in domain()
        if normalize_pair(
            scale_support(first, scalar),
            scale_support(second, scalar),
        )
        == normalized
    ]


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


def complement_prefix_partition_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    support_to_complement: dict[tuple[int, ...], set[tuple[int, ...]]] = (
        defaultdict(set)
    )
    complement_to_support: dict[tuple[int, ...], set[tuple[int, ...]]] = (
        defaultdict(set)
    )
    for support_prefix, supports in fibers.items():
        for support in supports:
            complement_prefix = elementary_prefix(support_complement(support))
            support_to_complement[support_prefix].add(complement_prefix)
            complement_to_support[complement_prefix].add(support_prefix)

    support_partition_ok = all(
        len(values) == 1 for values in support_to_complement.values()
    )
    complement_partition_ok = all(
        len(values) == 1 for values in complement_to_support.values()
    )
    if not support_partition_ok or not complement_partition_ok:
        raise AssertionError("support/complement prefix partitions differ")

    return {
        "checked": True,
        "support_prefix_values": len(support_to_complement),
        "complement_prefix_values": len(complement_to_support),
        "partitions_agree": True,
        "complement_size": N - AGREEMENT,
        "locator_gap_degree_bound": N - AGREEMENT - SIGMA - 1,
    }


def co_large_bound_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    complement_size = N - AGREEMENT
    gap_dimension = max(complement_size - SIGMA, 0)
    upper_bound = P**gap_dimension
    maximum_fiber_size = max(len(values) for values in fibers.values())
    if maximum_fiber_size > upper_bound:
        raise AssertionError("co-large prefix bound failed")
    return {
        "checked": True,
        "complement_size": complement_size,
        "gap_dimension": gap_dimension,
        "field_bound": upper_bound,
        "maximum_fiber_size": maximum_fiber_size,
        "holds": True,
    }


def divisor_gap_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    gap_degree_bound = N - AGREEMENT - SIGMA - 1
    gap_degrees: Counter[int] = Counter()
    nonzero_gaps: set[tuple[int, ...]] = set()
    total_parameters = 0

    for supports in fibers.values():
        base_locator = locator_polynomial(support_complement(supports[0]))
        seen_gaps: set[tuple[int, ...]] = set()
        for support in supports:
            locator = locator_polynomial(support_complement(support))
            if not divides_xn_minus_one(locator):
                raise AssertionError("complement locator does not divide X^n-1")
            gap = tuple(poly_sub(locator, base_locator))
            if gap in seen_gaps:
                raise AssertionError("divisor-gap parametrization is not injective")
            seen_gaps.add(gap)
            degree = poly_degree(list(gap))
            if degree > gap_degree_bound:
                raise AssertionError("divisor gap exceeds degree bound")
            gap_degrees[degree] += 1
            if gap:
                nonzero_gaps.add(gap)
            total_parameters += 1
        if len(seen_gaps) != len(supports):
            raise AssertionError("divisor-gap count mismatch")

    return {
        "checked": True,
        "gap_degree_bound": gap_degree_bound,
        "parameterized_supports": total_parameters,
        "zero_gap_count": gap_degrees[-1],
        "nonzero_gap_count": total_parameters - gap_degrees[-1],
        "distinct_nonzero_gaps": len(nonzero_gaps),
        "gap_degree_histogram": dict(sorted(gap_degrees.items())),
    }


def divisor_gap_graph_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    component_sizes = Counter(len(supports) for supports in fibers.values())
    vertices = sum(size * count for size, count in component_sizes.items())
    edge_count = sum(
        count * size * (size - 1) // 2
        for size, count in component_sizes.items()
    )
    nontrivial_components = sum(
        count for size, count in component_sizes.items() if size > 1
    )
    max_component = max(component_sizes)
    if vertices != comb(N, AGREEMENT):
        raise AssertionError("divisor-gap graph vertex count mismatch")
    if max_component != max(EXPECTED_HISTOGRAM):
        raise AssertionError("unexpected divisor-gap graph maximum component")
    return {
        "checked": True,
        "vertices": vertices,
        "components": len(fibers),
        "component_size_histogram": dict(sorted(component_sizes.items())),
        "nontrivial_components": nontrivial_components,
        "edge_count": edge_count,
        "max_component_size": max_component,
        "components_are_cliques": True,
    }


def complement_orbit_report(
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]],
) -> dict[str, Any]:
    orbit_members: dict[
        tuple[tuple[int, ...], tuple[int, ...]],
        list[dict[str, Any]],
    ] = defaultdict(list)
    all_gaps_linear = True

    for prefix, supports in sorted(fibers.items()):
        if len(supports) == 1:
            continue
        first_support, second_support = supports
        first_complement = support_complement(first_support)
        second_complement = support_complement(second_support)
        if elementary_prefix(first_complement) != elementary_prefix(
            second_complement
        ):
            raise AssertionError("complement prefixes do not match")
        try:
            gap = linear_locator_gap(first_complement, second_complement)
        except AssertionError:
            all_gaps_linear = False
            raise
        orbit_members[orbit_key(first_complement, second_complement)].append(
            {
                "prefix": prefix,
                "linear_gap": gap,
            }
        )

    representatives = []
    for key in sorted(orbit_members):
        first, second = key
        representatives.append(
            {
                "orbit_size": len(orbit_members[key]),
                "complements": [list(first), list(second)],
                "linear_gap": linear_locator_gap(first, second),
                "stabilizer": pair_stabilizer(first, second),
            }
        )

    orbit_sizes = tuple(sorted(row["orbit_size"] for row in representatives))
    expected_representatives = [
        {
            "orbit_size": row["orbit_size"],
            "complements": [list(part) for part in row["complements"]],
            "linear_gap": row["linear_gap"],
        }
        for row in EXPECTED_ORBIT_REPRESENTATIVES
    ]
    observed_representatives = [
        {
            "orbit_size": row["orbit_size"],
            "complements": row["complements"],
            "linear_gap": row["linear_gap"],
        }
        for row in representatives
    ]
    if orbit_sizes != EXPECTED_ORBIT_SIZES:
        raise AssertionError("unexpected complement orbit sizes")
    if observed_representatives != expected_representatives:
        raise AssertionError("unexpected complement orbit representatives")

    return {
        "complement_prefix_equivalence_checked": True,
        "all_locator_gaps_linear": all_gaps_linear,
        "dilation_orbits": len(representatives),
        "orbit_size_histogram": dict(
            sorted(Counter(row["orbit_size"] for row in representatives).items())
        ),
        "representatives": representatives,
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
    complement_partition = complement_prefix_partition_report(fibers)
    divisor_gaps = divisor_gap_report(fibers)
    divisor_graph = divisor_gap_graph_report(fibers)
    co_large_bound = co_large_bound_report(fibers)
    complement_orbits = complement_orbit_report(fibers)

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
        "complement_prefix_lemma_report": complement_partition,
        "divisor_gap_report": divisor_gaps,
        "divisor_gap_graph_report": divisor_graph,
        "co_large_bound_report": co_large_bound,
        "complement_orbit_report": complement_orbits,
        "example": verify_example(fibers),
        "passed": True,
    }


def print_text(cert: dict[str, Any]) -> None:
    inputs = cert["inputs"]
    distribution = cert["prefix_distribution"]
    collisions = cert["collision_report"]
    complement_partition = cert["complement_prefix_lemma_report"]
    divisor_gaps = cert["divisor_gap_report"]
    divisor_graph = cert["divisor_gap_graph_report"]
    co_large_bound = cert["co_large_bound_report"]
    complement_orbits = cert["complement_orbit_report"]
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
    print(
        "support/complement prefix partitions agree: "
        f"{complement_partition['partitions_agree']} "
        f"({complement_partition['support_prefix_values']} values)"
    )
    print(
        "divisor-gap parametrization: "
        f"{divisor_gaps['parameterized_supports']} supports, "
        f"{divisor_gaps['nonzero_gap_count']} nonzero gaps, "
        f"degree bound {divisor_gaps['gap_degree_bound']}"
    )
    print(
        "divisor-gap graph: "
        f"{divisor_graph['components']} components, "
        f"{divisor_graph['nontrivial_components']} nontrivial, "
        f"{divisor_graph['edge_count']} edges"
    )
    print(
        "co-large field bound: "
        f"max fiber {co_large_bound['maximum_fiber_size']} <= "
        f"{co_large_bound['field_bound']}"
    )
    print(
        "complement dilation orbits: "
        f"{complement_orbits['dilation_orbits']} with size histogram "
        f"{complement_orbits['orbit_size_histogram']}"
    )
    print(
        "all complement locator gaps linear: "
        f"{complement_orbits['all_locator_gaps_linear']}"
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
