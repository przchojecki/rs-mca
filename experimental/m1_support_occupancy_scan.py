#!/usr/bin/env python3
"""Scan M1 support-coefficient incidences by quotient-fiber occupancy.

Proof status: AUDIT / EXPERIMENTAL.

This is a tiny-field scanner for the support-coefficient criterion in
experimental/m1_support_coefficient_test.md. It enumerates exact supports of
size k+t, computes Pi_S(f), Pi_S(g), records the bad slope contributed by each
collinear noncontained support, and labels the support by its quotient-fiber
occupancy histogram.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from itertools import combinations
from typing import Dict, List, Optional, Sequence, Tuple

from mca_slope_scan import fraction_string, inv, make_domain
from verify_m1_quotient_remainder_profile import occupancy_family_size


def monomial_word(domain: Sequence[int], exponent: int, p: int) -> Tuple[int, ...]:
    return tuple(pow(x, exponent, p) for x in domain)


def solve_coefficients(xs: Sequence[int], ys: Sequence[int], p: int) -> List[int]:
    size = len(xs)
    matrix = [
        [pow(xs[row], col, p) for col in range(size)] + [ys[row] % p]
        for row in range(size)
    ]

    pivot_row = 0
    for col in range(size):
        pivot = None
        for row in range(pivot_row, size):
            if matrix[row][col] % p:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular interpolation matrix")

        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inv(matrix[pivot_row][col], p)
        matrix[pivot_row] = [(entry * scale) % p for entry in matrix[pivot_row]]

        for row in range(size):
            if row == pivot_row or matrix[row][col] % p == 0:
                continue
            factor = matrix[row][col] % p
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[pivot_row][idx]) % p
                for idx in range(size + 1)
            ]
        pivot_row += 1

    return [matrix[row][size] % p for row in range(size)]


def top_coefficients(
    values: Sequence[int],
    domain: Sequence[int],
    support: Sequence[int],
    k: int,
    slack: int,
    p: int,
) -> Tuple[int, ...]:
    xs = [domain[index] for index in support]
    ys = [values[index] for index in support]
    coeffs = solve_coefficients(xs, ys, p)
    return tuple(coeffs[k : k + slack])


def slope_from_top_coefficients(
    anchor_top: Sequence[int],
    direction_top: Sequence[int],
    p: int,
) -> Optional[int]:
    if all(entry % p == 0 for entry in anchor_top):
        if all(entry % p == 0 for entry in direction_top):
            return None
    if all(entry % p == 0 for entry in direction_top):
        return None

    pivot = next(index for index, entry in enumerate(direction_top) if entry % p)
    scalar = anchor_top[pivot] * inv(direction_top[pivot], p)
    scalar %= p
    for left, right in zip(anchor_top, direction_top):
        if (left - scalar * right) % p:
            return None
    return (-scalar) % p


def elementary_symmetric_prefix(
    values: Sequence[int],
    max_degree: int,
    p: int,
) -> Tuple[int, ...]:
    """Return e_0,...,e_max_degree for the supplied field values."""

    coeffs = [0] * (max_degree + 1)
    coeffs[0] = 1
    for value in values:
        for degree in range(max_degree, 0, -1):
            coeffs[degree] += value * coeffs[degree - 1]
            coeffs[degree] %= p
    return tuple(coeffs)


def residual_support_indices(
    support: Sequence[int],
    quotient_order: int,
    fiber_size: int,
) -> Tuple[int, ...]:
    support_set = set(support)
    residual = []
    for fiber in range(quotient_order):
        fiber_indices = [
            fiber + quotient_order * offset
            for offset in range(fiber_size)
        ]
        occupied = [index for index in fiber_indices if index in support_set]
        if len(occupied) == fiber_size:
            continue
        residual.extend(occupied)
    return tuple(residual)


def canonical_slope_from_symmetric_prefix(
    values: Sequence[int],
    slack: int,
    p: int,
) -> Optional[int]:
    sym = elementary_symmetric_prefix(values, slack, p)
    if any(sym[degree] % p for degree in range(1, slack)):
        return None
    sign = -1 if slack % 2 else 1
    return (sign * sym[slack]) % p


def occupancy_histogram(
    support: Sequence[int],
    quotient_order: int,
    fiber_size: int,
) -> Tuple[int, ...]:
    occupancies = [0] * quotient_order
    for index in support:
        occupancies[index % quotient_order] += 1
    histogram = [0] * (fiber_size + 1)
    for occupancy in occupancies:
        histogram[occupancy] += 1
    return tuple(histogram)


def histogram_text(histogram: Sequence[int]) -> str:
    return ",".join(
        f"{occupancy}:{count}"
        for occupancy, count in enumerate(histogram)
        if count
    )


def classify_histogram(histogram: Sequence[int]) -> str:
    fiber_size = len(histogram) - 1
    partial = [
        (occupancy, count)
        for occupancy, count in enumerate(histogram)
        if 0 < occupancy < fiber_size and count
    ]
    if not partial:
        return "whole_fiber"
    if len(partial) == 1 and partial[0][1] == 1:
        return "one_remainder"
    if len(partial) == 1:
        return "single_partial_occupancy"
    return "mixed_partial_occupancy"


def empty_histogram_record(histogram: Sequence[int]) -> Dict[str, object]:
    return {
        "histogram": list(histogram),
        "histogram_text": histogram_text(histogram),
        "class": classify_histogram(histogram),
        "support_count": 0,
        "predicted_support_count": 0,
        "contained_support_count": 0,
        "no_slope_support_count": 0,
        "incidence_count": 0,
        "canonical_zero_prefix_support_count": 0,
        "canonical_residual_zero_prefix_support_count": 0,
        "bad_slopes": set(),
        "slope_histogram": Counter(),
    }


def retained_histograms(
    records: Sequence[Dict[str, object]],
    top_histograms: int,
) -> List[Dict[str, object]]:
    retained = records if top_histograms < 0 else records[:top_histograms]
    output = []
    for record in retained:
        slope_histogram = record["slope_histogram"]
        assert isinstance(slope_histogram, Counter)
        bad_slopes = record["bad_slopes"]
        assert isinstance(bad_slopes, set)
        item = {
            key: value
            for key, value in record.items()
            if key not in {"bad_slopes", "slope_histogram"}
        }
        item["bad_slope_count"] = len(bad_slopes)
        item["bad_slopes"] = sorted(bad_slopes)
        item["slope_histogram"] = {
            str(slope): count for slope, count in sorted(slope_histogram.items())
        }
        output.append(item)
    return output


def scan_supports(
    p: int,
    n: int,
    k: int,
    slack: int,
    quotient_order: int,
    primitive: Optional[int],
    anchor_exp: Optional[int],
    direction_exp: Optional[int],
    max_supports: int,
    top_histograms: int,
) -> Dict[str, object]:
    support_size = k + slack
    if support_size > n:
        raise ValueError("require k + slack <= n")
    if n % quotient_order:
        raise ValueError("--quotient-order must divide --n")
    fiber_size = n // quotient_order

    total_supports = math.comb(n, support_size)
    if total_supports > max_supports:
        raise ValueError(
            f"scan needs {total_supports} supports; raise --max-supports to run it"
        )

    primitive, domain = make_domain(p, n, primitive)
    anchor_exp = k + slack if anchor_exp is None else anchor_exp
    direction_exp = k if direction_exp is None else direction_exp
    anchor = monomial_word(domain, anchor_exp, p)
    direction = monomial_word(domain, direction_exp, p)
    canonical_line = anchor_exp == k + slack and direction_exp == k
    low_deficit_limit = min(slack - 1, fiber_size - 1)
    canonical_formula_mismatches = 0
    low_deficit_mismatches = 0
    residual_zero_prefix_mismatches = 0
    canonical_zero_prefix_count = 0
    canonical_residual_zero_prefix_count = 0

    records: Dict[Tuple[int, ...], Dict[str, object]] = {}
    bad_slopes = set()
    incidence_count = 0
    contained_count = 0
    no_slope_count = 0

    for support in combinations(range(n), support_size):
        histogram = occupancy_histogram(support, quotient_order, fiber_size)
        if histogram not in records:
            records[histogram] = empty_histogram_record(histogram)
        record = records[histogram]
        record["support_count"] = int(record["support_count"]) + 1

        support_values = [domain[index] for index in support]
        residual = residual_support_indices(
            support,
            quotient_order,
            fiber_size,
        )
        residual_values = [domain[index] for index in residual]
        support_sym = elementary_symmetric_prefix(support_values, slack, p)
        residual_sym = elementary_symmetric_prefix(residual_values, slack, p)
        for degree in range(1, low_deficit_limit + 1):
            if support_sym[degree] != residual_sym[degree]:
                low_deficit_mismatches += 1
        residual_zero_prefix = all(
            residual_sym[degree] % p == 0 for degree in range(1, slack)
        )
        if residual_zero_prefix:
            canonical_residual_zero_prefix_count += 1
            record["canonical_residual_zero_prefix_support_count"] = (
                int(record["canonical_residual_zero_prefix_support_count"]) + 1
            )

        anchor_top = top_coefficients(anchor, domain, support, k, slack, p)
        direction_top = top_coefficients(direction, domain, support, k, slack, p)
        slope = slope_from_top_coefficients(anchor_top, direction_top, p)

        if canonical_line:
            canonical_slope = canonical_slope_from_symmetric_prefix(
                support_values,
                slack,
                p,
            )
            if canonical_slope is not None:
                canonical_zero_prefix_count += 1
                record["canonical_zero_prefix_support_count"] = (
                    int(record["canonical_zero_prefix_support_count"]) + 1
                )
            if slack <= fiber_size and (canonical_slope is not None) != (
                residual_zero_prefix
            ):
                residual_zero_prefix_mismatches += 1
            if slope != canonical_slope:
                canonical_formula_mismatches += 1

        contained = all(entry == 0 for entry in anchor_top) and all(
            entry == 0 for entry in direction_top
        )
        if contained:
            contained_count += 1
            record["contained_support_count"] = (
                int(record["contained_support_count"]) + 1
            )
            continue

        if slope is None:
            no_slope_count += 1
            record["no_slope_support_count"] = (
                int(record["no_slope_support_count"]) + 1
            )
            continue

        incidence_count += 1
        bad_slopes.add(slope)
        record["incidence_count"] = int(record["incidence_count"]) + 1
        record_bad_slopes = record["bad_slopes"]
        assert isinstance(record_bad_slopes, set)
        record_bad_slopes.add(slope)
        slope_histogram = record["slope_histogram"]
        assert isinstance(slope_histogram, Counter)
        slope_histogram[slope] += 1

    for histogram, record in records.items():
        predicted = occupancy_family_size(quotient_order, fiber_size, histogram)
        record["predicted_support_count"] = predicted
        record["support_count_matches_prediction"] = (
            int(record["support_count"]) == predicted
        )
        record_outcomes = (
            int(record["contained_support_count"])
            + int(record["no_slope_support_count"])
            + int(record["incidence_count"])
        )
        record["support_outcome_partition"] = (
            record_outcomes == int(record["support_count"])
        )

    ordered_records = sorted(
        records.values(),
        key=lambda item: (
            -int(item["incidence_count"]),
            -len(item["bad_slopes"]),
            -int(item["support_count"]),
            str(item["histogram_text"]),
        ),
    )
    support_count_sum = sum(int(item["support_count"]) for item in ordered_records)
    predictions_match = all(
        bool(item["support_count_matches_prediction"]) for item in ordered_records
    )
    record_outcomes_match = all(
        bool(item["support_outcome_partition"]) for item in ordered_records
    )
    outcome_count_sum = contained_count + no_slope_count + incidence_count
    outcome_partition = outcome_count_sum == total_supports and record_outcomes_match

    return {
        "proof_status": "AUDIT / EXPERIMENTAL",
        "theorem_problem_id": "M1-support-coefficient-occupancy-scan",
        "determinism": "deterministic exact support enumeration; no random seed",
        "parameters": {
            "prime": p,
            "domain_order": n,
            "primitive_generator": primitive,
            "k": k,
            "rho": fraction_string(k, n),
            "slack": slack,
            "support_size": support_size,
            "quotient_order": quotient_order,
            "fiber_size": fiber_size,
            "anchor_exponent": anchor_exp,
            "direction_exponent": direction_exp,
        },
        "domain": list(domain),
        "support_count": total_supports,
        "scanned_support_count": support_count_sum,
        "histogram_count": len(ordered_records),
        "histogram_counts_match_binomial": support_count_sum == total_supports,
        "histogram_counts_match_formula": predictions_match,
        "support_outcome_partition": outcome_partition,
        "canonical_line": canonical_line,
        "canonical_symmetric_formula_check": (
            canonical_formula_mismatches == 0 if canonical_line else None
        ),
        "canonical_symmetric_formula_mismatch_count": (
            canonical_formula_mismatches if canonical_line else None
        ),
        "canonical_zero_prefix_support_count": (
            canonical_zero_prefix_count if canonical_line else None
        ),
        "canonical_residual_zero_prefix_support_count": (
            canonical_residual_zero_prefix_count if canonical_line else None
        ),
        "canonical_residual_zero_prefix_match": (
            residual_zero_prefix_mismatches == 0
            if canonical_line and slack <= fiber_size
            else None
        ),
        "canonical_residual_zero_prefix_mismatch_count": (
            residual_zero_prefix_mismatches
            if canonical_line and slack <= fiber_size
            else None
        ),
        "low_deficit_whole_fiber_invisibility": low_deficit_mismatches == 0,
        "low_deficit_checked_degrees": list(range(1, low_deficit_limit + 1)),
        "low_deficit_mismatch_count": low_deficit_mismatches,
        "contained_support_count": contained_count,
        "no_slope_support_count": no_slope_count,
        "incidence_count": incidence_count,
        "bad_slope_count": len(bad_slopes),
        "bad_slopes": sorted(bad_slopes),
        "bad_slope_density": fraction_string(len(bad_slopes), p),
        "top_histograms": retained_histograms(ordered_records, top_histograms),
    }


def print_text(result: Dict[str, object]) -> None:
    params = result["parameters"]
    assert isinstance(params, dict)
    print("M1 support-coefficient occupancy scan")
    print("proof_status: AUDIT / EXPERIMENTAL")
    print(
        "p={p} n={n} k={k} slack={t} support={s} quotient_order={N}".format(
            p=params["prime"],
            n=params["domain_order"],
            k=params["k"],
            t=params["slack"],
            s=params["support_size"],
            N=params["quotient_order"],
        )
    )
    print(
        "supports={supports} histograms={histograms} incidences={inc} "
        "bad_slopes={slopes} density={density}".format(
            supports=result["support_count"],
            histograms=result["histogram_count"],
            inc=result["incidence_count"],
            slopes=result["bad_slope_count"],
            density=result["bad_slope_density"],
        )
    )
    print(
        "histogram_counts_match_binomial={binom} "
        "histogram_counts_match_formula={formula} "
        "support_outcome_partition={partition}".format(
            binom=result["histogram_counts_match_binomial"],
            formula=result["histogram_counts_match_formula"],
            partition=result["support_outcome_partition"],
        )
    )
    print(
        "low_deficit_whole_fiber_invisibility={ok} degrees={degrees}".format(
            ok=result["low_deficit_whole_fiber_invisibility"],
            degrees=result["low_deficit_checked_degrees"],
        )
    )
    if result["canonical_line"]:
        print(
            "canonical_symmetric_formula_check={formula} "
            "zero_prefix_supports={zero} "
            "residual_zero_prefix_match={residual}".format(
                formula=result["canonical_symmetric_formula_check"],
                zero=result["canonical_zero_prefix_support_count"],
                residual=result["canonical_residual_zero_prefix_match"],
            )
        )
    print()

    for record in result["top_histograms"]:
        assert isinstance(record, dict)
        print(
            "class={kind} h={hist} supports={supports} "
            "incidences={inc} slopes={slopes}".format(
                kind=record["class"],
                hist=record["histogram_text"],
                supports=record["support_count"],
                inc=record["incidence_count"],
                slopes=record["bad_slope_count"],
            )
        )
        if record["slope_histogram"]:
            slopes = ", ".join(
                f"{slope}:{count}"
                for slope, count in record["slope_histogram"].items()
            )
            print(f"  slope histogram: {slopes}")


def positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan exact-support Pi_S incidences by quotient occupancy."
    )
    parser.add_argument("--prime", type=positive_int, required=True)
    parser.add_argument("--n", type=positive_int, required=True)
    parser.add_argument("--k", type=positive_int, required=True)
    parser.add_argument("--slack", type=positive_int, required=True)
    parser.add_argument("--quotient-order", type=positive_int, required=True)
    parser.add_argument("--primitive", type=positive_int, default=None)
    parser.add_argument("--anchor-exp", type=int, default=None)
    parser.add_argument("--direction-exp", type=int, default=None)
    parser.add_argument("--max-supports", type=positive_int, default=200_000)
    parser.add_argument(
        "--top-histograms",
        type=int,
        default=10,
        help="number of histogram records to retain; negative retains all",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = scan_supports(
        p=args.prime,
        n=args.n,
        k=args.k,
        slack=args.slack,
        quotient_order=args.quotient_order,
        primitive=args.primitive,
        anchor_exp=args.anchor_exp,
        direction_exp=args.direction_exp,
        max_supports=args.max_supports,
        top_histograms=args.top_histograms,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
