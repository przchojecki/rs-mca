#!/usr/bin/env python3
"""Scan exact M1 quotient-fiber occupancy profiles.

Proof status: AUDIT / EXPERIMENTAL.

The formulas are proved in experimental/m1_quotient_periodic_overlap_profile.md.
For a quotient partition with N fibers of size M, this scanner enumerates every
fiber-occupancy histogram at a fixed support size and evaluates the exact
fixed-support strict exchange ledger for that class.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, List, Optional, Sequence

from verify_m1_quotient_remainder_profile import (
    choose,
    occupancy_family_size,
    occupancy_histograms,
    occupancy_profile_enumerator,
)


def log2_or_none(value: int) -> Optional[float]:
    if value <= 0:
        return None
    return round(math.log2(value), 6)


def format_log(value: Optional[float]) -> str:
    if value is None:
        return "empty"
    return f"{value:.2f}"


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


def retained_terms(
    strict_terms: Dict[int, int],
    top_terms: int,
) -> List[Dict[str, int]]:
    records = [
        {"exchange_size": exchange_size, "codegree": codegree}
        for exchange_size, codegree in sorted(
            strict_terms.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]
    if top_terms < 0:
        return records
    return records[:top_terms]


def weighted_correction(
    strict_terms: Dict[int, int],
    slack: int,
    line_field_size: int,
) -> int:
    return sum(
        codegree * line_field_size ** (slack - exchange_size)
        for exchange_size, codegree in strict_terms.items()
    )


def histogram_text(histogram: Sequence[int]) -> str:
    return ",".join(
        f"{occupancy}:{count}"
        for occupancy, count in enumerate(histogram)
        if count
    )


def scan_histograms(
    quotient_order: int,
    fiber_size: int,
    support_size: int,
    slack: int,
    line_field_size: Optional[int],
    top_histograms: int,
    top_terms: int,
) -> Dict[str, object]:
    histograms = occupancy_histograms(quotient_order, fiber_size, support_size)
    total_supports = choose(quotient_order * fiber_size, support_size)
    histogram_supports = 0
    records = []

    for histogram in histograms:
        family_size = occupancy_family_size(quotient_order, fiber_size, histogram)
        profile = occupancy_profile_enumerator(
            quotient_order,
            fiber_size,
            histogram,
        )
        strict_terms = {
            exchange_size: codegree
            for exchange_size, codegree in profile.items()
            if 0 < exchange_size < slack
        }
        strict_mass = sum(strict_terms.values())
        max_codegree = max(strict_terms.values()) if strict_terms else 0
        weighted = None
        if line_field_size is not None:
            weighted = weighted_correction(strict_terms, slack, line_field_size)

        histogram_supports += family_size
        records.append(
            {
                "histogram": list(histogram),
                "histogram_text": histogram_text(histogram),
                "class": classify_histogram(histogram),
                "family_size": family_size,
                "log2_family_size": log2_or_none(family_size),
                "strict_exchange_count": len(strict_terms),
                "strict_codegree_mass": strict_mass,
                "log2_strict_codegree_mass": log2_or_none(strict_mass),
                "max_strict_codegree": max_codegree,
                "log2_max_strict_codegree": log2_or_none(max_codegree),
                "weighted_correction": weighted,
                "log2_weighted_correction": (
                    None if weighted is None else log2_or_none(weighted)
                ),
                "strict_exchange_terms": retained_terms(strict_terms, top_terms),
            }
        )

    score_field = (
        "weighted_correction"
        if line_field_size is not None
        else "strict_codegree_mass"
    )
    records.sort(
        key=lambda item: (
            -int(item[score_field] or 0),
            -int(item["family_size"]),
            item["histogram_text"],
        )
    )
    retained = records if top_histograms < 0 else records[:top_histograms]
    active = [item for item in records if item["strict_codegree_mass"]]
    weighted_values = [
        int(item["weighted_correction"])
        for item in records
        if item["weighted_correction"] is not None
    ]

    return {
        "proof_status": "AUDIT / EXPERIMENTAL",
        "theorem_problem_id": "M1-quotient-fiber-occupancy-profile",
        "determinism": "deterministic histogram enumeration; no random seed",
        "quotient_order": quotient_order,
        "fiber_size": fiber_size,
        "domain_size": quotient_order * fiber_size,
        "support_size": support_size,
        "slack": slack,
        "line_field_size": line_field_size,
        "histogram_count": len(records),
        "strict_active_histogram_count": len(active),
        "total_supports": total_supports,
        "histogram_supports": histogram_supports,
        "histogram_supports_match_binomial": histogram_supports == total_supports,
        "max_log2_strict_codegree_mass": (
            None
            if not active
            else max(item["log2_strict_codegree_mass"] for item in active)
        ),
        "max_log2_weighted_correction": (
            None if not weighted_values else log2_or_none(max(weighted_values))
        ),
        "top_histograms": retained,
    }


def print_text(result: Dict[str, object]) -> None:
    print("M1 quotient-fiber occupancy-profile scan")
    print("proof_status: AUDIT / EXPERIMENTAL")
    print(
        "N={N} M={M} n={n} support={s} slack={t}".format(
            N=result["quotient_order"],
            M=result["fiber_size"],
            n=result["domain_size"],
            s=result["support_size"],
            t=result["slack"],
        )
    )
    print(
        "histograms={count} strict_active={active} supports_match={match}".format(
            count=result["histogram_count"],
            active=result["strict_active_histogram_count"],
            match=result["histogram_supports_match_binomial"],
        )
    )
    if result["line_field_size"] is not None:
        print(f"line_field_size={result['line_field_size']}")
    print()

    for item in result["top_histograms"]:
        assert isinstance(item, dict)
        weighted = ""
        if item["log2_weighted_correction"] is not None:
            weighted = " logR={}".format(
                format_log(item["log2_weighted_correction"])
            )
        print(
            "class={kind} h={hist} log|A|={size} "
            "logMass={mass} logMaxGamma={gamma}{weighted}".format(
                kind=item["class"],
                hist=item["histogram_text"],
                size=format_log(item["log2_family_size"]),
                mass=format_log(item["log2_strict_codegree_mass"]),
                gamma=format_log(item["log2_max_strict_codegree"]),
                weighted=weighted,
            )
        )
        terms = item["strict_exchange_terms"]
        if terms:
            formatted_terms = "; ".join(
                "j={j},Gamma={g}".format(
                    j=term["exchange_size"],
                    g=term["codegree"],
                )
                for term in terms
            )
            print(f"  terms: {formatted_terms}")


def positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan exact quotient-fiber occupancy exchange profiles."
    )
    parser.add_argument("--quotient-order", type=positive_int, required=True)
    parser.add_argument("--fiber-size", type=positive_int, required=True)
    parser.add_argument("--support-size", type=positive_int, required=True)
    parser.add_argument("--slack", type=positive_int, required=True)
    parser.add_argument("--line-field-size", type=positive_int, default=None)
    parser.add_argument(
        "--top-histograms",
        type=int,
        default=10,
        help="number of histogram records to retain; negative retains all",
    )
    parser.add_argument(
        "--top-terms",
        type=int,
        default=8,
        help="number of strict exchange terms retained per histogram",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
    )
    args = parser.parse_args()

    domain_size = args.quotient_order * args.fiber_size
    if args.support_size > domain_size:
        raise SystemExit("--support-size cannot exceed N*M")

    result = scan_histograms(
        quotient_order=args.quotient_order,
        fiber_size=args.fiber_size,
        support_size=args.support_size,
        slack=args.slack,
        line_field_size=args.line_field_size,
        top_histograms=args.top_histograms,
        top_terms=args.top_terms,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
