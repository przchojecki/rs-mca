#!/usr/bin/env python3
"""Verify the t=2 Hankel determinant gate and one-exchange core lift.

Proof status: PROVED-LOCAL / EXACT FINITE VERIFICATION.

In the M1 Hankel-pencil normal form, set t=2 and write

    a_T = H_2(Syn(Y)) ell_T,        b_T = H_2(Syn(phi)) ell_T.

Then a complement T contributes a finite noncontained slope exactly when
b_T != 0 and a_T is a scalar multiple of b_T.  The scalar is unique.

The useful packet fact is the same-slope one-exchange lift: if
T_1=R union {x} and T_2=R union {y} are distinct one-exchange complements
with the same slope lambda, then

    H_3(Syn(Y)-lambda Syn(phi)) ell_R = 0.

Thus that local collision is already visible as a higher-slack/root-slice
Hankel core, rather than as unexplained primitive slope growth.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from typing import Sequence

from scan_m1_exact_target_v0 import (
    cyclic_subgroup,
    quotient_representatives,
    support_records,
)
from verify_m1_exact_target_hankel_equivalence import (
    classify_pair_hankel,
    hankel_annihilates,
    locator_coeffs,
    support_hankel_records,
    syndrome,
    syndrome_difference,
)


def hankel_apply(
    syn: Sequence[int],
    locator: Sequence[int],
    row_count: int,
    p: int,
) -> tuple[int, ...]:
    return tuple(
        sum(locator[offset] * syn[row + offset] for offset in range(len(locator))) % p
        for row in range(row_count)
    )


def solve_unique_slope(
    target_vector: Sequence[int],
    direction_vector: Sequence[int],
    p: int,
) -> int | None:
    """Return lambda with target=lambda*direction, or None."""
    pivot = next(
        (index for index, value in enumerate(direction_vector) if value % p),
        None,
    )
    if pivot is None:
        return None
    slope = target_vector[pivot] * pow(direction_vector[pivot], -1, p) % p
    if all(
        target_vector[index] % p == slope * direction_vector[index] % p
        for index in range(len(target_vector))
    ):
        return slope
    return None


def one_exchange(left: Sequence[int], right: Sequence[int], j: int) -> bool:
    return len(set(left) & set(right)) == j - 1


def core_indices(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(sorted(set(left) & set(right)))


def analyze_case(
    p: int,
    k: int,
    max_quotient_pairs: int,
    max_examples: int,
) -> dict[str, object]:
    n = p - 1
    t = 2
    a = k + t
    j = n - a
    if not (0 < k < a <= n):
        raise ValueError("case must satisfy 0 < k and k+2 <= p-1")
    if j < 1:
        raise ValueError("one-exchange complements require j >= 1")

    domain = cyclic_subgroup(p, n)
    supports = support_records(n, a)
    support_hankels = support_hankel_records(domain, supports, p)
    reps = quotient_representatives(domain, k, p)
    quotient_pair_count = len(reps) ** 2
    if quotient_pair_count > max_quotient_pairs:
        raise ValueError(
            f"would scan {quotient_pair_count} quotient pairs; "
            f"raise --max-quotient-pairs to run this exact case"
        )

    support_complements = [
        tuple(record["complement_indices"]) for record in support_hankels
    ]
    support_stabilizers = [
        int(record["stabilizer_order"]) for record in support_hankels
    ]
    locators = [tuple(record["locator"]) for record in support_hankels]
    syns = [syndrome(rep, domain, k, p) for rep in reps]
    h2_values = [
        [hankel_apply(syn, locator, t, p) for locator in locators]
        for syn in syns
    ]

    bad_histogram: Counter[int] = Counter()
    primitive_histogram: Counter[int] = Counter()
    periodic_histogram: Counter[int] = Counter()
    slope_fiber_histogram: Counter[int] = Counter()
    primitive_slope_fiber_histogram: Counter[int] = Counter()
    one_exchange_edge_histogram: Counter[int] = Counter()
    primitive_one_exchange_edge_histogram: Counter[int] = Counter()

    max_bad = 0
    max_periodic = 0
    max_primitive = 0
    max_slope_fiber = 0
    max_primitive_slope_fiber = 0
    max_one_exchange_edges = 0
    max_primitive_one_exchange_edges = 0
    lifted_core_checks = 0
    lifted_noncontained_core_edges = 0
    lifted_direction_zero_core_edges = 0
    examples: list[dict[str, object]] = []

    for phi_index, phi_syn in enumerate(syns):
        phi_h2 = h2_values[phi_index]
        for y_index, y_syn in enumerate(syns):
            y_h2 = h2_values[y_index]
            supports_by_slope: dict[int, list[int]] = defaultdict(list)
            periodic_slopes: set[int] = set()

            for support_index, (target_vector, direction_vector) in enumerate(
                zip(y_h2, phi_h2, strict=True)
            ):
                slope = solve_unique_slope(target_vector, direction_vector, p)
                if slope is None:
                    continue
                supports_by_slope[slope].append(support_index)
                if support_stabilizers[support_index] > 1:
                    periodic_slopes.add(slope)

            slope_loop = classify_pair_hankel(
                phi_syn,
                y_syn,
                p,
                t,
                support_hankels,
            )
            determinant_bad = sorted(supports_by_slope)
            determinant_periodic = sorted(periodic_slopes)
            determinant_primitive = sorted(
                slope for slope in supports_by_slope if slope not in periodic_slopes
            )
            if (
                determinant_bad != slope_loop["bad_slopes"]
                or determinant_periodic != slope_loop["periodic_slopes"]
                or determinant_primitive != slope_loop["primitive_slopes"]
            ):
                raise AssertionError(
                    {
                        "kind": "t2-determinant-gate-mismatch",
                        "p": p,
                        "k": k,
                        "phi_index": phi_index,
                        "Y_index": y_index,
                        "determinant_bad": determinant_bad,
                        "hankel_bad": slope_loop["bad_slopes"],
                        "determinant_periodic": determinant_periodic,
                        "hankel_periodic": slope_loop["periodic_slopes"],
                        "determinant_primitive": determinant_primitive,
                        "hankel_primitive": slope_loop["primitive_slopes"],
                    }
                )

            bad_count = len(supports_by_slope)
            periodic_count = len(periodic_slopes)
            primitive_count = bad_count - periodic_count
            bad_histogram[bad_count] += 1
            periodic_histogram[periodic_count] += 1
            primitive_histogram[primitive_count] += 1
            max_bad = max(max_bad, bad_count)
            max_periodic = max(max_periodic, periodic_count)
            max_primitive = max(max_primitive, primitive_count)

            pair_one_exchange_edges = 0
            pair_primitive_one_exchange_edges = 0

            for slope, support_indices in supports_by_slope.items():
                slope_fiber_histogram[len(support_indices)] += 1
                max_slope_fiber = max(max_slope_fiber, len(support_indices))
                is_primitive_slope = slope not in periodic_slopes
                if is_primitive_slope:
                    primitive_slope_fiber_histogram[len(support_indices)] += 1
                    max_primitive_slope_fiber = max(
                        max_primitive_slope_fiber,
                        len(support_indices),
                    )

                for left, right in itertools.combinations(support_indices, 2):
                    left_complement = support_complements[left]
                    right_complement = support_complements[right]
                    if not one_exchange(left_complement, right_complement, j):
                        continue
                    pair_one_exchange_edges += 1
                    if is_primitive_slope:
                        pair_primitive_one_exchange_edges += 1
                    core = core_indices(left_complement, right_complement)
                    core_locator = locator_coeffs(domain, core, p)
                    target_syn = syndrome_difference(y_syn, slope, phi_syn, p)
                    if not hankel_annihilates(target_syn, core_locator, t + 1, p):
                        raise AssertionError(
                            {
                                "kind": "same-slope-one-exchange-lift-failed",
                                "p": p,
                                "k": k,
                                "slope": slope,
                                "left_complement": list(left_complement),
                                "right_complement": list(right_complement),
                                "core": list(core),
                                "target_syndrome": list(target_syn),
                                "core_locator": list(core_locator),
                            }
                        )
                    lifted_core_checks += 1
                    if hankel_annihilates(phi_syn, core_locator, t + 1, p):
                        lifted_direction_zero_core_edges += 1
                    else:
                        lifted_noncontained_core_edges += 1

                    if len(examples) < max_examples:
                        examples.append(
                            {
                                "phi_index": phi_index,
                                "Y_index": y_index,
                                "lambda": slope,
                                "left_complement": list(left_complement),
                                "right_complement": list(right_complement),
                                "core": list(core),
                                "core_locator": list(core_locator),
                                "core_direction_nonzero": not hankel_annihilates(
                                    phi_syn,
                                    core_locator,
                                    t + 1,
                                    p,
                                ),
                            }
                        )

            one_exchange_edge_histogram[pair_one_exchange_edges] += 1
            primitive_one_exchange_edge_histogram[pair_primitive_one_exchange_edges] += 1
            max_one_exchange_edges = max(max_one_exchange_edges, pair_one_exchange_edges)
            max_primitive_one_exchange_edges = max(
                max_primitive_one_exchange_edges,
                pair_primitive_one_exchange_edges,
            )

    return {
        "status": "PASS",
        "params": {
            "p": p,
            "n": n,
            "k": k,
            "a": a,
            "t": t,
            "j": j,
            "domain": domain,
            "support_count": len(supports),
            "periodic_support_count": sum(1 for order in support_stabilizers if order > 1),
            "quotient_class_count": len(reps),
            "quotient_pair_count": quotient_pair_count,
        },
        "max_bad_slopes": max_bad,
        "max_periodic_budget": max_periodic,
        "max_primitive_remainder": max_primitive,
        "max_slope_fiber_size": max_slope_fiber,
        "max_primitive_slope_fiber_size": max_primitive_slope_fiber,
        "max_same_slope_one_exchange_edges": max_one_exchange_edges,
        "max_primitive_same_slope_one_exchange_edges": max_primitive_one_exchange_edges,
        "lifted_core_checks": lifted_core_checks,
        "lifted_noncontained_core_edges": lifted_noncontained_core_edges,
        "lifted_direction_zero_core_edges": lifted_direction_zero_core_edges,
        "bad_count_histogram": dict(sorted(bad_histogram.items())),
        "periodic_count_histogram": dict(sorted(periodic_histogram.items())),
        "primitive_count_histogram": dict(sorted(primitive_histogram.items())),
        "slope_fiber_size_histogram": dict(sorted(slope_fiber_histogram.items())),
        "primitive_slope_fiber_size_histogram": dict(
            sorted(primitive_slope_fiber_histogram.items())
        ),
        "same_slope_one_exchange_edge_histogram": dict(
            sorted(one_exchange_edge_histogram.items())
        ),
        "primitive_same_slope_one_exchange_edge_histogram": dict(
            sorted(primitive_one_exchange_edge_histogram.items())
        ),
        "lift_examples": examples,
    }


def parse_case(value: str) -> tuple[int, int]:
    parts = value.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("case must have form p,k")
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("case entries must be integers") from exc


def print_summary(results: Sequence[dict[str, object]]) -> None:
    print("M1 t=2 Hankel one-exchange lift verifier")
    for result in results:
        params = result["params"]
        print(
            "case "
            f"p={params['p']} n={params['n']} k={params['k']} "
            f"a={params['a']} j={params['j']}: "
            f"quotient_pairs={params['quotient_pair_count']} "
            f"max_bad={result['max_bad_slopes']} "
            f"max_primitive={result['max_primitive_remainder']} "
            f"max_fiber={result['max_slope_fiber_size']} "
            f"one_exchange_lifts={result['lifted_core_checks']}"
        )
    print("PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        type=parse_case,
        dest="cases",
        help="case p,k with t fixed to 2; may be supplied multiple times",
    )
    parser.add_argument(
        "--max-quotient-pairs",
        type=int,
        default=250_000,
        help="guardrail for exact quotient-pair enumeration",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        default=3,
        help="number of same-slope one-exchange lift examples retained",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = args.cases or [(5, 1), (7, 3)]
    results = [
        analyze_case(
            p=p,
            k=k,
            max_quotient_pairs=args.max_quotient_pairs,
            max_examples=args.max_examples,
        )
        for p, k in cases
    ]
    if args.json:
        print(json.dumps({"status": "PASS", "cases": results}, indent=2, sort_keys=True))
    else:
        print_summary(results)


if __name__ == "__main__":
    main()
