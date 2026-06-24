#!/usr/bin/env python3
"""Verify a finite separation between LD_sw and ABF/GG line-decodability.

The model is RS[F_13,{0,...,7},3] at agreement 5.  A nonconstant received line
with nonzero code direction has zero support-wise noncontained slopes, while a
close-codeword assignment on the same line is not captured by any code-line on
b=n+1 slopes.
"""

from __future__ import annotations

import argparse
import itertools
import json
from typing import Any


P = 13
N = 8
K = 3
AGREEMENT = 5
B_THRESHOLD = N + 1
P0_SLOPES = tuple(range(6))
P1_SLOPES = tuple(range(6, P))
DIRECTION_COEFFS = (0, 1, 0)


def eval_poly(coeffs: tuple[int, ...], x_value: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x_value + coeff) % P
    return value


def codewords() -> dict[tuple[int, ...], tuple[int, ...]]:
    domain = tuple(range(N))
    return {
        coeffs: tuple(eval_poly(coeffs, x_value) for x_value in domain)
        for coeffs in itertools.product(range(P), repeat=K)
    }


def word_add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % P for a, b in zip(left, right))


def word_scale(scalar: int, word: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((scalar * value) % P for value in word)


def word_sub(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a - b) % P for a, b in zip(left, right))


def is_zero_word(word: tuple[int, ...]) -> bool:
    return all(value == 0 for value in word)


def support_restriction(
    word: tuple[int, ...], support: tuple[int, ...]
) -> tuple[int, ...]:
    return tuple(word[index] for index in support)


def support_tables(
    codebook: dict[tuple[int, ...], tuple[int, ...]]
) -> dict[tuple[int, ...], set[tuple[int, ...]]]:
    tables: dict[tuple[int, ...], set[tuple[int, ...]]] = {}
    for size in range(AGREEMENT, N + 1):
        for support in itertools.combinations(range(N), size):
            tables[support] = {
                support_restriction(word, support)
                for word in codebook.values()
            }
    return tables


def agreement_count(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a == b for a, b in zip(left, right))


def close_codeword_coeffs(
    received: tuple[int, ...],
    codebook: dict[tuple[int, ...], tuple[int, ...]],
) -> list[tuple[int, ...]]:
    return [
        coeffs
        for coeffs, word in codebook.items()
        if agreement_count(received, word) >= AGREEMENT
    ]


def build_received_word(
    p0: tuple[int, ...], p1: tuple[int, ...]
) -> tuple[int, ...]:
    """Glue p0 and p1 along their common zeros at coordinates 0 and 1."""

    values: list[int] = []
    for index in range(N):
        if index in (0, 1, 2, 3, 4):
            values.append(p0[index])
        else:
            values.append(p1[index])
    return tuple(values)


def supportwise_bad_slopes_for_received_line(
    received: tuple[int, ...],
    direction: tuple[int, ...],
    support_code: dict[tuple[int, ...], set[tuple[int, ...]]],
) -> tuple[list[int], int]:
    """Return support-wise bad slopes for the line received + gamma*direction."""

    bad_slopes: set[int] = set()
    explaining_supports = 0
    for slope in range(P):
        line_word = word_add(received, word_scale(slope, direction))
        for support, restrictions in support_code.items():
            if support_restriction(line_word, support) not in restrictions:
                continue
            explaining_supports += 1
            contained = (
                support_restriction(received, support) in restrictions
                and support_restriction(direction, support) in restrictions
            )
            if not contained:
                bad_slopes.add(slope)
    return sorted(bad_slopes), explaining_supports


def scalar_solving(
    base: tuple[int, ...],
    direction: tuple[int, ...],
    target: tuple[int, ...],
) -> int | None:
    """Find gamma with base + gamma*direction = target, or return None."""

    solution: int | None = None
    for base_value, direction_value, target_value in zip(base, direction, target):
        rhs = (target_value - base_value) % P
        if direction_value == 0:
            if rhs != 0:
                return None
            continue
        candidate = (rhs * pow(direction_value, -1, P)) % P
        if solution is None:
            solution = candidate
        elif solution != candidate:
            return None
    return 0 if solution is None else solution


def code_line_assignment_agreement(
    base: tuple[int, ...],
    direction: tuple[int, ...],
    received_direction: tuple[int, ...],
    p0: tuple[int, ...],
    p1: tuple[int, ...],
) -> int:
    """Count slopes where a code-line agrees with the adversarial assignment."""

    shifted_direction = word_sub(direction, received_direction)
    if is_zero_word(shifted_direction):
        if base == p0:
            return len(P0_SLOPES)
        if base == p1:
            return len(P1_SLOPES)
        return 0

    agreement = 0
    gamma0 = scalar_solving(base, shifted_direction, p0)
    if gamma0 is not None and gamma0 in P0_SLOPES:
        agreement += 1
    gamma1 = scalar_solving(base, shifted_direction, p1)
    if gamma1 is not None and gamma1 in P1_SLOPES:
        agreement += 1
    return agreement


def max_code_line_assignment_agreement(
    codebook: dict[tuple[int, ...], tuple[int, ...]],
    received_direction: tuple[int, ...],
    p0: tuple[int, ...],
    p1: tuple[int, ...],
) -> dict[str, Any]:
    max_agreement = -1
    witnesses: list[dict[str, Any]] = []
    words = list(codebook.items())
    for base_coeffs, base in words:
        for direction_coeffs, direction in words:
            agreement = code_line_assignment_agreement(
                base, direction, received_direction, p0, p1
            )
            if agreement > max_agreement:
                max_agreement = agreement
                witnesses = [
                    {
                        "base_coeffs": base_coeffs,
                        "direction_coeffs": direction_coeffs,
                        "agreement": agreement,
                    }
                ]
            elif agreement == max_agreement and len(witnesses) < 5:
                witnesses.append(
                    {
                        "base_coeffs": base_coeffs,
                        "direction_coeffs": direction_coeffs,
                        "agreement": agreement,
                    }
                )
    return {
        "max_assignment_agreement": max_agreement,
        "sample_maximizers": witnesses,
    }


def bucket_obstruction_bound(bucket_sizes: tuple[int, ...]) -> int:
    return max(max(bucket_sizes), len(bucket_sizes))


def balanced_bucket_bound(bucket_count: int) -> int:
    return max((P + bucket_count - 1) // bucket_count, bucket_count)


def list_size_obstruction_threshold(b_threshold: int) -> int:
    if b_threshold <= 1:
        raise ValueError("b_threshold must be at least 2")
    return (P + b_threshold - 2) // (b_threshold - 1)


def automatic_list_size_bound(trigger_size: int, b_threshold: int) -> int:
    if b_threshold <= 1:
        raise ValueError("b_threshold must be at least 2")
    return (trigger_size - 1) // (b_threshold - 1)


def pigeonhole_collinearity_bound(trigger_size: int, list_size: int) -> int:
    if list_size <= 0:
        raise ValueError("list_size must be positive")
    return (trigger_size + list_size - 1) // list_size


def compute_report() -> dict[str, Any]:
    codebook = codewords()
    support_code = support_tables(codebook)
    p0 = codebook[(0, 0, 0)]
    p1 = codebook[(0, P - 1, 1)]
    received_direction = codebook[DIRECTION_COEFFS]
    received = build_received_word(p0, p1)
    full_code = set(codebook.values())
    close_coeffs = close_codeword_coeffs(received, codebook)

    bad_slopes, explaining_supports = supportwise_bad_slopes_for_received_line(
        received, received_direction, support_code
    )
    p0_agreement = agreement_count(received, p0)
    p1_agreement = agreement_count(received, p1)
    assignment_count = len(P0_SLOPES) + len(P1_SLOPES)
    line_contained = all(
        word_add(received, word_scale(slope, received_direction)) in full_code
        for slope in range(P)
    )
    max_report = max_code_line_assignment_agreement(
        codebook, received_direction, p0, p1
    )
    bucket_sizes = (len(P0_SLOPES), len(P1_SLOPES))
    bucket_bound = bucket_obstruction_bound(bucket_sizes)
    balanced_bound = balanced_bucket_bound(len(bucket_sizes))
    list_threshold = list_size_obstruction_threshold(B_THRESHOLD)
    automatic_bound = automatic_list_size_bound(P, B_THRESHOLD)
    pigeonhole_bound = pigeonhole_collinearity_bound(P, len(close_coeffs))

    checks = {
        "p0_and_p1_distinct": p0 != p1,
        "p0_and_p1_meet_at_0_and_1": p0[:2] == p1[:2] == (0, 0),
        "received_direction_is_nonzero_codeword": not is_zero_word(
            received_direction
        ),
        "received_line_is_not_contained_in_code": not line_contained,
        "p0_agrees_with_received_on_5": p0_agreement == AGREEMENT,
        "p1_agrees_with_received_on_5": p1_agreement == AGREEMENT,
        "nonconstant_line_has_no_ldsw_bad_slopes": bad_slopes == [],
        "assignment_uses_all_field_slopes": assignment_count == P,
        "assignment_is_close_on_every_slope": (
            p0_agreement >= AGREEMENT and p1_agreement >= AGREEMENT
        ),
        "max_code_line_agreement_is_7": (
            max_report["max_assignment_agreement"] == len(P1_SLOPES)
        ),
        "max_agreement_matches_bucket_obstruction": (
            max_report["max_assignment_agreement"] == bucket_bound
        ),
        "bucket_obstruction_matches_balanced_bound": (
            bucket_bound == balanced_bound
        ),
        "list_size_threshold_is_two": list_threshold == 2,
        "base_close_list_is_exactly_two": len(close_coeffs) == 2,
        "base_close_list_meets_threshold": len(close_coeffs) >= list_threshold,
        "automatic_list_size_bound_is_one": automatic_bound == 1,
        "close_list_is_first_obstructing_size": (
            len(close_coeffs) == automatic_bound + 1
        ),
        "pigeonhole_bound_for_actual_list_is_seven": pigeonhole_bound == 7,
        "list_threshold_below_collinearity_threshold": (
            list_threshold <= B_THRESHOLD - 1
        ),
        "abf_threshold_b_n_plus_1_fails": (
            max_report["max_assignment_agreement"] < B_THRESHOLD
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "COUNTEREXAMPLE / FINITE",
        "code": "RS[F_13,{0,...,7},3]",
        "p": P,
        "n": N,
        "k": K,
        "agreement": AGREEMENT,
        "delta": f"{N - AGREEMENT}/{N}",
        "abf_b_threshold": B_THRESHOLD,
        "p0_coeffs": [0, 0, 0],
        "p1_coeffs": [0, P - 1, 1],
        "received_direction_coeffs": list(DIRECTION_COEFFS),
        "p0_word": list(p0),
        "p1_word": list(p1),
        "received_word": list(received),
        "received_direction_word": list(received_direction),
        "close_codeword_coeffs": [list(coeffs) for coeffs in close_coeffs],
        "received_line_contained_in_code": line_contained,
        "p0_agreement": p0_agreement,
        "p1_agreement": p1_agreement,
        "received_line_ldsw_bad_slopes": bad_slopes,
        "received_line_explaining_support_count": explaining_supports,
        "assignment": {
            "p0_slopes": list(P0_SLOPES),
            "p1_slopes": list(P1_SLOPES),
            "bucket_sizes": list(bucket_sizes),
            "assigned_close_codewords": assignment_count,
            "m_bucket_obstruction_bound": bucket_bound,
            "balanced_m_bucket_bound": balanced_bound,
            "list_size_obstruction_threshold": list_threshold,
            "automatic_list_size_bound": automatic_bound,
            "pigeonhole_collinearity_bound": pigeonhole_bound,
        },
        **max_report,
        "interpretation": (
            "The nonconstant received line r+gamma*x has LD_sw contribution 0 "
            "at agreement 5, but an adversarial close-codeword assignment on "
            "the same line is not captured by any code-line on b=n+1=9 slopes."
        ),
        "checks": checks,
    }


def print_report(report: dict[str, Any]) -> None:
    print(
        "code={code} agreement={agreement} delta={delta} b={abf_b_threshold}".format(
            **report
        )
    )
    print(f"received direction coeffs: {report['received_direction_coeffs']}")
    print(
        "received line contained in code: "
        f"{report['received_line_contained_in_code']}"
    )
    print(f"p0 agreement with received word: {report['p0_agreement']}")
    print(f"p1 agreement with received word: {report['p1_agreement']}")
    print(
        "received-line LD_sw bad slopes: "
        f"{len(report['received_line_ldsw_bad_slopes'])}"
    )
    print(
        "assigned close codewords across slopes: "
        f"{report['assignment']['assigned_close_codewords']}"
    )
    print(
        "m-bucket obstruction bound: "
        f"{report['assignment']['m_bucket_obstruction_bound']}"
    )
    print(
        "balanced m-bucket bound: "
        f"{report['assignment']['balanced_m_bucket_bound']}"
    )
    print(
        "list-size obstruction threshold: "
        f"{report['assignment']['list_size_obstruction_threshold']}"
    )
    print(
        "automatic list-size bound: "
        f"{report['assignment']['automatic_list_size_bound']}"
    )
    print(
        "pigeonhole bound for actual close list: "
        f"{report['assignment']['pigeonhole_collinearity_bound']}"
    )
    print(
        "max code-line agreement with assignment: "
        f"{report['max_assignment_agreement']}"
    )
    print(f"threshold b=n+1: {report['abf_b_threshold']}")
    print(f"sample maximizer: {report['sample_maximizers'][0]}")
    print(f"status: {report['status']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()
    report = compute_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
