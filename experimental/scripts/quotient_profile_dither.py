#!/usr/bin/env python3
"""Finite-length quotient-profile and dimension-dither scanner.

Proof status: AUDIT / EXPERIMENTAL.

The exact-divisibility profile implements the quantity from snarks_v5.tex:

    Qprof_H(a,k) =
      max_{M | gcd(n,k), M > 1, a-k < M, k/M <= n/M - 1}
        log2 binom(n/M - 1, k/M).

For dyadic domains n=2^m, the script compares k0=rho*n with dithered
dimensions k=k0-r.  It also records a separate remainder-variant diagnostic
suggested by the quotient-hygiene section: if k = M*floor(k/M)+rem, then the
remainder construction can meet target slack sigma=a-k by using a support
inside one M-coset of size sigma+rem, provided sigma+rem < M.

The exact profile is the certificate quantity.  The remainder diagnostic is a
finite-length warning signal for small-remainder dimensions, not a replacement
for the exact profile.

With --slack-window START:END, the script also reports the proved dyadic
first-exchange slack-window ledger L_win(r) from
experimental/m1_quotient_periodic_overlap_profile.md.  For each fixed dither
r and dyadic scale M, active whole-fiber quotient slacks in the requested
window are exactly the residue class t == r mod M, subject to the strict and
endpoint eligibility checks.  It also reports the exact one-remainder strict
codegree mass obtained by truncating the proved H_REM formula to exponents
below the target slack.

The same window mode reports the theorem-backed minimax gap certificate for
fixed dither over the slack interval.  Over integer dithers the smallest
possible max |t-r| is the interval-center radius, while avoiding an exact
k0-support slack forces max |t-r| to be the full window length.

If --target-stable-gap D is supplied, the same report includes the finite-menu
covering certificate: a C-value menu safely covers at most
floor(C/2)(3D+1)+(C mod 2)D consecutive slacks, and the scanner emits the exact
capacity threshold and a capacity-achieving construction.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

DEFAULT_RATES = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16))
DEFAULT_ETAS = (Fraction(1, 64), Fraction(1, 32), Fraction(1, 16))
LOG2 = math.log(2)


@dataclass(frozen=True)
class ScaleRecord:
    """One quotient scale contribution."""

    M: int
    N: int
    quotient_dimension: int
    log2_list_size: float
    remainder: Optional[int] = None
    support_inside_coset: Optional[int] = None

    def to_json(self) -> Dict[str, object]:
        result: Dict[str, object] = {
            "M_coset_size": self.M,
            "N_quotient_order": self.N,
            "quotient_dimension": self.quotient_dimension,
            "log2_list_size": round(self.log2_list_size, 6),
        }
        if self.remainder is not None:
            result["remainder"] = self.remainder
        if self.support_inside_coset is not None:
            result["support_inside_coset"] = self.support_inside_coset
        return result


@dataclass(frozen=True)
class WindowLedgerEntry:
    """One active first-exchange whole-fiber quotient entry in a slack window."""

    slack: int
    M: int
    N: int
    support_size: int
    quotient_support: int
    first_codegree: int
    log2_first_codegree: float
    first_exchange_complete: bool

    def to_json(self) -> Dict[str, object]:
        return {
            "slack": self.slack,
            "M_coset_size": self.M,
            "N_quotient_order": self.N,
            "support_size": self.support_size,
            "quotient_support": self.quotient_support,
            "first_codegree": self.first_codegree,
            "log2_first_codegree": round(self.log2_first_codegree, 6),
            "first_exchange_complete_for_scale": self.first_exchange_complete,
        }


@dataclass(frozen=True)
class RemainderWindowEntry:
    """One strict one-remainder quotient packet in a slack window."""

    slack: int
    M: int
    N: int
    support_size: int
    quotient_support: int
    remainder: int
    strict_codegree_mass: int
    log2_strict_codegree_mass: float
    large_fiber_formula: bool
    stable_large_scale_formula: bool
    stable_tail_side: Optional[str]
    stable_weighted_correction: Optional[int]
    log2_stable_weighted_correction: Optional[float]
    dither_gap: int

    def to_json(self) -> Dict[str, object]:
        result: Dict[str, object] = {
            "slack": self.slack,
            "M_coset_size": self.M,
            "N_quotient_order": self.N,
            "support_size": self.support_size,
            "quotient_support": self.quotient_support,
            "remainder": self.remainder,
            "strict_codegree_mass": self.strict_codegree_mass,
            "log2_strict_codegree_mass": round(self.log2_strict_codegree_mass, 6),
            "large_fiber_formula_complete": self.large_fiber_formula,
            "stable_large_scale_formula": self.stable_large_scale_formula,
            "dither_gap": self.dither_gap,
        }
        if self.stable_tail_side is not None:
            result["stable_tail_side"] = self.stable_tail_side
        if self.stable_weighted_correction is not None:
            result["stable_weighted_correction"] = self.stable_weighted_correction
            assert self.log2_stable_weighted_correction is not None
            result["log2_stable_weighted_correction"] = round(
                self.log2_stable_weighted_correction,
                6,
            )
        return result


@dataclass(frozen=True)
class MenuTailLowerBoundEntry:
    """One stable-tail lower-bound scale forced by a finite dither menu."""

    M: int
    N: int
    forced_gap: int
    side_coefficient_floor: int
    adaptive_linear_mass: int
    stable_tail_mass_lower_bound: int
    log2_stable_tail_mass_lower_bound: float
    log2_mass_over_adaptive_linear: float
    stable_tail_weighted_lower_bound: Optional[int]
    log2_stable_tail_weighted_lower_bound: Optional[float]
    log2_same_slack_weighted_over_adaptive: Optional[float]
    log2_window_weighted_over_adaptive: Optional[float]

    def to_json(self) -> Dict[str, object]:
        result: Dict[str, object] = {
            "M_coset_size": self.M,
            "N_quotient_order": self.N,
            "forced_gap": self.forced_gap,
            "side_coefficient_floor": self.side_coefficient_floor,
            "adaptive_linear_mass": self.adaptive_linear_mass,
            "stable_tail_mass_lower_bound": self.stable_tail_mass_lower_bound,
            "log2_stable_tail_mass_lower_bound": round(
                self.log2_stable_tail_mass_lower_bound,
                6,
            ),
            "log2_mass_over_adaptive_linear": round(
                self.log2_mass_over_adaptive_linear,
                6,
            ),
        }
        if self.stable_tail_weighted_lower_bound is not None:
            result["stable_tail_weighted_lower_bound"] = (
                self.stable_tail_weighted_lower_bound
            )
            assert self.log2_stable_tail_weighted_lower_bound is not None
            result["log2_stable_tail_weighted_lower_bound"] = round(
                self.log2_stable_tail_weighted_lower_bound,
                6,
            )
            assert self.log2_same_slack_weighted_over_adaptive is not None
            result["log2_same_slack_weighted_over_adaptive"] = round(
                self.log2_same_slack_weighted_over_adaptive,
                6,
            )
            assert self.log2_window_weighted_over_adaptive is not None
            result["log2_window_weighted_over_adaptive"] = round(
                self.log2_window_weighted_over_adaptive,
                6,
            )
        return result


def parse_fraction(raw: str) -> Fraction:
    try:
        return Fraction(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid fraction: {raw}") from exc


def parse_fraction_list(raw: str) -> List[Fraction]:
    if not raw:
        return []
    return [parse_fraction(part.strip()) for part in raw.split(",") if part.strip()]


def parse_slack_window(raw: str) -> Tuple[int, int]:
    if ":" not in raw:
        raise argparse.ArgumentTypeError("expected slack window START:END")
    start_text, end_text = raw.split(":", 1)
    try:
        start = int(start_text)
        end = int(end_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid slack window: {raw}") from exc
    if start < 0 or end < start:
        raise argparse.ArgumentTypeError("require 0 <= START <= END")
    return start, end


def fixed_window_radius(slack_window: Tuple[int, int], dither: int) -> int:
    start, end = slack_window
    return max(abs(start - dither), abs(end - dither))


def fixed_window_minimax_summary(
    slack_window: Tuple[int, int],
    max_dither: int,
) -> Dict[str, object]:
    start, end = slack_window
    window_length = end - start + 1
    scanned_dithers = list(range(max_dither + 1))

    scanned_radius = {
        dither: fixed_window_radius(slack_window, dither)
        for dither in scanned_dithers
    }
    scanned_min_radius = min(scanned_radius.values())
    scanned_best = [
        dither
        for dither, radius in scanned_radius.items()
        if radius == scanned_min_radius
    ]

    zero_gap_free = [
        dither for dither in scanned_dithers if not (start <= dither <= end)
    ]
    if zero_gap_free:
        zero_gap_radius = {
            dither: scanned_radius[dither] for dither in zero_gap_free
        }
        scanned_zero_gap_min_radius: Optional[int] = min(zero_gap_radius.values())
        scanned_zero_gap_best: Optional[List[int]] = [
            dither
            for dither, radius in zero_gap_radius.items()
            if radius == scanned_zero_gap_min_radius
        ]
    else:
        scanned_zero_gap_min_radius = None
        scanned_zero_gap_best = None

    return {
        "window_length": window_length,
        "unconstrained_integer_min_radius": window_length // 2,
        "zero_gap_free_integer_min_radius": window_length,
        "left_zero_gap_free_dither": start - 1,
        "right_zero_gap_free_dither": end + 1,
        "left_zero_gap_free_stable_endpoint_eligible": start > 1,
        "right_zero_gap_free_stable_endpoint_eligible": window_length < start,
        "scanned_min_radius": scanned_min_radius,
        "scanned_best_dithers": scanned_best,
        "scanned_zero_gap_free_min_radius": scanned_zero_gap_min_radius,
        "scanned_zero_gap_free_best_dithers": scanned_zero_gap_best,
    }


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def dither_menu_capacity(menu_size: int, safe_gap: int) -> int:
    pairs = menu_size // 2
    singleton = menu_size % 2
    return pairs * (3 * safe_gap + 1) + singleton * safe_gap


def exact_min_menu_size_for_gap(window_length: int, safe_gap: int) -> int:
    even_pairs = ceil_div(window_length, 3 * safe_gap + 1)
    even_size = 2 * even_pairs
    if window_length <= safe_gap:
        odd_size = 1
    else:
        odd_pairs = ceil_div(window_length - safe_gap, 3 * safe_gap + 1)
        odd_size = 2 * odd_pairs + 1
    return min(even_size, odd_size)


def exact_min_safe_gap_for_menu_size(window_length: int, menu_size: int) -> int:
    pairs = menu_size // 2
    singleton = menu_size % 2
    coefficient = 3 * pairs + singleton
    offset = pairs
    return max(1, ceil_div(max(0, window_length - offset), coefficient))


def exact_dither_menu_construction(
    slack_window: Tuple[int, int],
    menu_size: int,
    safe_gap: int,
) -> List[int]:
    start, end = slack_window
    cursor = start
    menu = []
    for _ in range(menu_size // 2):
        if cursor > end:
            break
        menu.extend([cursor + safe_gap, cursor + 2 * safe_gap])
        cursor += 3 * safe_gap + 1
    if menu_size % 2 and cursor <= end:
        menu.append(cursor + safe_gap)
    return menu


def dither_menu_covering_summary(
    slack_window: Tuple[int, int],
    target_stable_gap: int,
    dither_menu_size: Optional[int],
) -> Dict[str, object]:
    start, end = slack_window
    window_length = end - start + 1
    exact_min_menu_size = exact_min_menu_size_for_gap(
        window_length,
        target_stable_gap,
    )
    exact_construction = exact_dither_menu_construction(
        slack_window,
        exact_min_menu_size,
        target_stable_gap,
    )
    adaptive_competitive_menu_size = exact_min_menu_size_for_gap(
        window_length,
        1,
    )
    adaptive_competitive_construction = exact_dither_menu_construction(
        slack_window,
        adaptive_competitive_menu_size,
        1,
    )
    summary = {
        "target_stable_gap": target_stable_gap,
        "window_length": window_length,
        "coarse_menu_size_lower_bound": ceil_div(
            window_length,
            2 * target_stable_gap,
        ),
        "exact_min_menu_size_for_target_gap": exact_min_menu_size,
        "exact_capacity_for_target_gap": dither_menu_capacity(
            exact_min_menu_size,
            target_stable_gap,
        ),
        "exact_capacity_construction_dithers": exact_construction,
        "exact_min_menu_size_for_asymptotic_adaptive_competitiveness": (
            adaptive_competitive_menu_size
        ),
        "gap_one_capacity_for_adaptive_competitive_menu": (
            dither_menu_capacity(adaptive_competitive_menu_size, 1)
        ),
        "adaptive_competitive_construction_dithers": (
            adaptive_competitive_construction
        ),
    }
    if dither_menu_size is not None:
        forced_gap = exact_min_safe_gap_for_menu_size(
            window_length,
            dither_menu_size,
        )
        summary["queried_menu_size"] = dither_menu_size
        summary["coverage_possible_by_exact_capacity"] = (
            target_stable_gap >= forced_gap
        )
        summary["capacity_at_target_gap"] = dither_menu_capacity(
            dither_menu_size,
            target_stable_gap,
        )
        summary["exact_forced_safe_gap_lower_bound"] = forced_gap
        summary["exact_forced_gap_construction_dithers"] = (
            exact_dither_menu_construction(
                slack_window,
                dither_menu_size,
                forced_gap,
            )
        )
        summary["stable_tail_condition_D_lt_t_start"] = target_stable_gap < start
        summary["queried_menu_asymptotically_adaptive_competitive"] = (
            forced_gap == 1
        )
        if forced_gap == 1:
            summary["large_scale_menu_regime"] = "finite_prefix_linear"
            summary["nonlinear_prefix_max_scale"] = end
            summary["forced_tail_binomial_degree"] = 1
        else:
            summary["large_scale_menu_regime"] = "forced_superlinear_tail"
            summary["nonlinear_prefix_max_scale"] = None
            summary["forced_tail_binomial_degree"] = forced_gap
        summary["asymptotic_adaptive_menu_size_deficit"] = max(
            0,
            adaptive_competitive_menu_size - dither_menu_size,
        )
    return summary


def retained_menu_tail_entries(
    records: Sequence[MenuTailLowerBoundEntry],
    top_scales: int,
) -> List[Dict[str, object]]:
    if top_scales < 0:
        return [item.to_json() for item in records]
    return [item.to_json() for item in records[:top_scales]]


def dither_menu_tail_lower_bound_summary(
    n: int,
    k0: int,
    slack_window: Tuple[int, int],
    target_stable_gap: int,
    dither_menu_size: int,
    top_scales: int,
    line_field_size: Optional[int],
) -> Dict[str, object]:
    start, end = slack_window
    window_length = end - start + 1
    forced_gap = exact_min_safe_gap_for_menu_size(window_length, dither_menu_size)
    coverage_possible = target_stable_gap >= forced_gap
    stable_eligible = coverage_possible and target_stable_gap < start
    adaptive_linear_mass = n - k0 - 1

    records = []
    if stable_eligible:
        for M in divisors_of_power_of_two(n):
            if M <= 1 or M > k0 or k0 % M:
                continue
            if M < end + target_stable_gap:
                continue
            side_floor = min(k0 // M, (n - k0) // M)
            mass_lower_bound = side_floor * choose(M, forced_gap) - 1
            if mass_lower_bound <= 0:
                continue
            log2_mass_ratio = math.log2(mass_lower_bound) - math.log2(
                adaptive_linear_mass
            )
            weighted_lower_bound = None
            log2_weighted_lower_bound = None
            log2_same_slack_weighted_ratio = None
            log2_window_weighted_ratio = None
            if line_field_size is not None:
                weighted_lower_bound = (
                    mass_lower_bound
                    * line_field_size ** (start - target_stable_gap)
                )
                log2_weighted_lower_bound = math.log2(weighted_lower_bound)
                log2_same_slack_weighted_ratio = (
                    log2_mass_ratio
                    - (target_stable_gap - 1) * math.log2(line_field_size)
                )
                log2_window_weighted_ratio = (
                    log2_mass_ratio
                    - (end - 1 - (start - target_stable_gap))
                    * math.log2(line_field_size)
                )
            records.append(
                MenuTailLowerBoundEntry(
                    M=M,
                    N=n // M,
                    forced_gap=forced_gap,
                    side_coefficient_floor=side_floor,
                    adaptive_linear_mass=adaptive_linear_mass,
                    stable_tail_mass_lower_bound=mass_lower_bound,
                    log2_stable_tail_mass_lower_bound=math.log2(mass_lower_bound),
                    log2_mass_over_adaptive_linear=log2_mass_ratio,
                    stable_tail_weighted_lower_bound=weighted_lower_bound,
                    log2_stable_tail_weighted_lower_bound=(
                        log2_weighted_lower_bound
                    ),
                    log2_same_slack_weighted_over_adaptive=(
                        log2_same_slack_weighted_ratio
                    ),
                    log2_window_weighted_over_adaptive=(
                        log2_window_weighted_ratio
                    ),
                )
            )

    records.sort(
        key=lambda item: (
            -(
                item.log2_stable_tail_weighted_lower_bound
                if item.log2_stable_tail_weighted_lower_bound is not None
                else item.log2_stable_tail_mass_lower_bound
            ),
            item.M,
        )
    )
    weighted_values = [
        item.log2_stable_tail_weighted_lower_bound
        for item in records
        if item.log2_stable_tail_weighted_lower_bound is not None
    ]
    weighted_ratio_values = [
        item.log2_same_slack_weighted_over_adaptive
        for item in records
        if item.log2_same_slack_weighted_over_adaptive is not None
    ]
    window_weighted_ratio_values = [
        item.log2_window_weighted_over_adaptive
        for item in records
        if item.log2_window_weighted_over_adaptive is not None
    ]
    mass_dominating_scales = [
        item.M for item in records if item.log2_mass_over_adaptive_linear > 0
    ]
    weighted_dominating_scales = [
        item.M
        for item in records
        if (
            item.log2_same_slack_weighted_over_adaptive is not None
            and item.log2_same_slack_weighted_over_adaptive > 0
        )
    ]
    window_weighted_dominating_scales = [
        item.M
        for item in records
        if (
            item.log2_window_weighted_over_adaptive is not None
            and item.log2_window_weighted_over_adaptive > 0
        )
    ]
    return {
        "target_stable_gap": target_stable_gap,
        "queried_menu_size": dither_menu_size,
        "line_field_size": line_field_size,
        "exact_forced_safe_gap_lower_bound": forced_gap,
        "coverage_possible_by_exact_capacity": coverage_possible,
        "capacity_at_target_gap": dither_menu_capacity(
            dither_menu_size,
            target_stable_gap,
        ),
        "stable_tail_lower_bound_applicable": stable_eligible,
        "stable_eligible_scale_count": len(records),
        "adaptive_linear_mass_per_stable_scale": adaptive_linear_mass,
        "menu_mass_dominates_adaptive_scale_count": len(
            mass_dominating_scales
        ),
        "min_scale_mass_dominates_adaptive_linear": (
            None if not mass_dominating_scales else min(mass_dominating_scales)
        ),
        "max_log2_stable_tail_mass_lower_bound": (
            None
            if not records
            else round(
                max(item.log2_stable_tail_mass_lower_bound for item in records),
                6,
            )
        ),
        "max_log2_mass_over_adaptive_linear": (
            None
            if not records
            else round(
                max(item.log2_mass_over_adaptive_linear for item in records),
                6,
            )
        ),
        "max_log2_stable_tail_weighted_lower_bound": (
            None if not weighted_values else round(max(weighted_values), 6)
        ),
        "max_log2_same_slack_weighted_over_adaptive": (
            None
            if not weighted_ratio_values
            else round(max(weighted_ratio_values), 6)
        ),
        "max_log2_window_weighted_over_adaptive": (
            None
            if not window_weighted_ratio_values
            else round(max(window_weighted_ratio_values), 6)
        ),
        "same_slack_weighted_dominates_adaptive_scale_count": len(
            weighted_dominating_scales
        ),
        "min_scale_same_slack_weighted_dominates_adaptive": (
            None
            if not weighted_dominating_scales
            else min(weighted_dominating_scales)
        ),
        "window_weighted_dominates_adaptive_scale_count": len(
            window_weighted_dominating_scales
        ),
        "min_scale_window_weighted_dominates_adaptive": (
            None
            if not window_weighted_dominating_scales
            else min(window_weighted_dominating_scales)
        ),
        "entries": retained_menu_tail_entries(records, top_scales),
    }


def adaptive_maximal_window_summary(
    n: int,
    k0: int,
    slack_window: Tuple[int, int],
    line_field_size: Optional[int],
) -> Dict[str, object]:
    start, end = slack_window
    stable_scales = [
        M
        for M in divisors_of_power_of_two(n)
        if M > 1 and M <= k0 and k0 % M == 0 and M > end
    ]
    linear_mass = n - k0 - 1
    result = {
        "adaptive_dither_rule": "r(t)=t-1",
        "large_scale_condition": "M_coset_size > slack_window.end",
        "stable_scale_count": len(stable_scales),
        "linear_mass_per_stable_scale": linear_mass,
        "max_log2_linear_mass_per_stable_scale": round(math.log2(linear_mass), 6),
        "stable_scales": stable_scales,
    }
    if line_field_size is not None:
        max_weighted = linear_mass * line_field_size ** (end - 1)
        result["line_field_size"] = line_field_size
        result["max_weighted_correction_per_stable_scale"] = max_weighted
        result["max_log2_weighted_correction_per_stable_scale"] = round(
            math.log2(max_weighted),
            6,
        )
    return result


def fraction_label(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    if k == 0 or k == n:
        return 0.0
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / LOG2


def divisors_of_power_of_two(n: int) -> List[int]:
    if n <= 0 or n & (n - 1):
        raise ValueError(f"expected a positive power of two, got n={n}")
    divisors = []
    value = 1
    while value <= n:
        divisors.append(value)
        value <<= 1
    return divisors


def ceil_fraction_times(value: Fraction, n: int) -> int:
    numerator = value.numerator * n
    return (numerator + value.denominator - 1) // value.denominator


def choose(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def exact_scales(n: int, k: int, sigma: int) -> List[ScaleRecord]:
    records = []
    for M in divisors_of_power_of_two(n):
        if M <= 1 or k % M != 0 or sigma >= M:
            continue
        N = n // M
        quotient_dimension = k // M
        if quotient_dimension < 1 or quotient_dimension > N - 1:
            continue
        records.append(
            ScaleRecord(
                M=M,
                N=N,
                quotient_dimension=quotient_dimension,
                log2_list_size=log2_binom(N - 1, quotient_dimension),
            )
        )
    records.sort(key=lambda item: (-item.log2_list_size, item.M))
    return records


def remainder_scales(n: int, k: int, sigma: int) -> List[ScaleRecord]:
    records = []
    for M in divisors_of_power_of_two(n):
        if M <= 1:
            continue
        N = n // M
        quotient_dimension = k // M
        if quotient_dimension < 1 or quotient_dimension > N - 1:
            continue
        remainder = k % M
        support_inside_coset = sigma + remainder
        if support_inside_coset >= M:
            continue
        records.append(
            ScaleRecord(
                M=M,
                N=N,
                quotient_dimension=quotient_dimension,
                log2_list_size=log2_binom(N - 1, quotient_dimension),
                remainder=remainder,
                support_inside_coset=support_inside_coset,
            )
        )
    records.sort(key=lambda item: (-item.log2_list_size, item.M))
    return records


def profile_value(records: Sequence[ScaleRecord]) -> Optional[float]:
    if not records:
        return None
    return records[0].log2_list_size


def slack_window_entries(
    n: int,
    k0: int,
    dither: int,
    slack_window: Tuple[int, int],
) -> List[WindowLedgerEntry]:
    start, end = slack_window
    records = []
    for M in divisors_of_power_of_two(n):
        if M <= 1 or M > k0 or k0 % M:
            continue
        for slack in range(max(start, M + 1), end + 1):
            support_size = k0 + slack - dither
            if support_size < M or support_size > n - M:
                continue
            if (slack - dither) % M:
                continue

            N = n // M
            quotient_support = support_size // M
            codegree = quotient_support * (N - quotient_support)
            records.append(
                WindowLedgerEntry(
                    slack=slack,
                    M=M,
                    N=N,
                    support_size=support_size,
                    quotient_support=quotient_support,
                    first_codegree=codegree,
                    log2_first_codegree=math.log2(codegree),
                    first_exchange_complete=slack <= 2 * M,
                )
            )
    records.sort(key=lambda item: (-item.log2_first_codegree, item.slack, item.M))
    return records


def retained_window_entries(
    records: Sequence[WindowLedgerEntry],
    top_scales: int,
) -> List[Dict[str, object]]:
    if top_scales < 0:
        return [item.to_json() for item in records]
    return [item.to_json() for item in records[:top_scales]]


def slack_window_summary(
    records: Sequence[WindowLedgerEntry],
    top_scales: int,
) -> Dict[str, object]:
    return {
        "active_entry_count": len(records),
        "active_scale_count": len({item.M for item in records}),
        "active_slack_count": len({item.slack for item in records}),
        "max_log2_first_codegree": (
            None
            if not records
            else round(max(item.log2_first_codegree for item in records), 6)
        ),
        "entries": retained_window_entries(records, top_scales),
    }


def remainder_strict_codegree_mass(N: int, M: int, L: int, b: int, slack: int) -> int:
    """Return sum_{1 <= j < slack} [y^j] H_REM(y)."""

    mass = 0

    max_h = (slack - 1) // M
    for h in range(0, max_h + 1):
        max_ell = min(b, M - b, slack - 1 - h * M)
        for ell in range(0, max_ell + 1):
            exponent = h * M + ell
            if exponent == 0:
                continue
            mass += (
                choose(L, h)
                * choose(N - L - 1, h)
                * choose(b, ell)
                * choose(M - b, ell)
            )

    max_h = (slack - 1 - (M - b)) // M
    for h in range(0, max_h + 1):
        mass += (
            L
            * choose(M, b)
            * choose(L - 1, h)
            * choose(N - L - 1, h)
        )

    max_h = (slack - 1) // M - 1
    for h in range(0, max_h + 1):
        mass += (
            L
            * choose(M, b)
            * choose(L - 1, h)
            * choose(N - L - 1, h + 1)
        )

    max_h = (slack - 1) // M
    for h in range(1, max_h + 1):
        mass += (
            (N - L - 1)
            * choose(M, b)
            * choose(L, h)
            * choose(N - L - 2, h - 1)
        )

    max_h = (slack - 1 - b) // M
    for h in range(0, max_h + 1):
        mass += (
            (N - L - 1)
            * choose(M, b)
            * choose(L, h)
            * choose(N - L - 2, h)
        )

    return mass


def two_sided_stable_tail(
    n: int,
    k0: int,
    dither_gap: int,
    M: int,
    slack: int,
) -> Optional[Tuple[str, int]]:
    e = abs(dither_gap)
    if not (1 <= e < slack and M >= slack + e):
        return None
    if dither_gap > 0:
        return "above", ((n - k0) // M) * choose(M, e) - 1
    return "below", (k0 // M) * choose(M, e) - 1


def two_sided_stable_weighted_correction(
    n: int,
    k0: int,
    dither_gap: int,
    M: int,
    slack: int,
    q: int,
) -> int:
    e = abs(dither_gap)
    if dither_gap > 0:
        side_coeff = (n - k0) // M - 1
    else:
        side_coeff = k0 // M - 1

    correction = sum(
        choose(e, ell) * choose(M - e, ell) * q ** (slack - ell)
        for ell in range(1, e + 1)
    )
    correction += side_coeff * choose(M, e) * q ** (slack - e)
    return correction


def retained_remainder_entries(
    records: Sequence[RemainderWindowEntry],
    top_scales: int,
) -> List[Dict[str, object]]:
    if top_scales < 0:
        return [item.to_json() for item in records]
    return [item.to_json() for item in records[:top_scales]]


def remainder_window_entries(
    n: int,
    k0: int,
    dither: int,
    slack_window: Tuple[int, int],
    line_field_size: Optional[int],
) -> List[RemainderWindowEntry]:
    start, end = slack_window
    records = []
    for M in divisors_of_power_of_two(n):
        if M <= 1 or M > k0 or k0 % M:
            continue
        N = n // M
        for slack in range(max(start, 1), end + 1):
            support_size = k0 + slack - dither
            if support_size <= 0 or support_size >= n:
                continue
            dither_gap = slack - dither
            b = support_size % M
            if b == 0:
                continue
            L = support_size // M
            if L > N - 1:
                continue
            mass = remainder_strict_codegree_mass(N, M, L, b, slack)
            if not mass:
                continue
            stable_tail = None
            if (
                (dither_gap > 0 and b == dither_gap)
                or (dither_gap < 0 and b == M + dither_gap)
            ):
                stable_tail = two_sided_stable_tail(
                    n,
                    k0,
                    dither_gap,
                    M,
                    slack,
                )
            stable_side = None
            stable_weighted = None
            log2_stable_weighted = None
            stable_mass_matches = False
            if stable_tail is not None:
                stable_side, stable_mass = stable_tail
                stable_mass_matches = mass == stable_mass
                if not stable_mass_matches:
                    raise AssertionError("stable tail mass mismatch")
                if line_field_size is not None:
                    stable_weighted = two_sided_stable_weighted_correction(
                        n,
                        k0,
                        dither_gap,
                        M,
                        slack,
                        line_field_size,
                    )
                    log2_stable_weighted = math.log2(stable_weighted)
            records.append(
                RemainderWindowEntry(
                    slack=slack,
                    M=M,
                    N=N,
                    support_size=support_size,
                    quotient_support=L,
                    remainder=b,
                    strict_codegree_mass=mass,
                    log2_strict_codegree_mass=math.log2(mass),
                    large_fiber_formula=slack <= M,
                    stable_large_scale_formula=stable_mass_matches,
                    stable_tail_side=stable_side,
                    stable_weighted_correction=stable_weighted,
                    log2_stable_weighted_correction=log2_stable_weighted,
                    dither_gap=dither_gap,
                )
            )
    records.sort(
        key=lambda item: (-item.log2_strict_codegree_mass, item.slack, item.M)
    )
    return records


def remainder_window_summary(
    records: Sequence[RemainderWindowEntry],
    top_scales: int,
) -> Dict[str, object]:
    stable_weighted_values = [
        item.log2_stable_weighted_correction
        for item in records
        if item.log2_stable_weighted_correction is not None
    ]
    return {
        "active_entry_count": len(records),
        "active_scale_count": len({item.M for item in records}),
        "active_slack_count": len({item.slack for item in records}),
        "stable_entry_count": sum(
            1 for item in records if item.stable_large_scale_formula
        ),
        "max_log2_strict_codegree_mass": (
            None
            if not records
            else round(max(item.log2_strict_codegree_mass for item in records), 6)
        ),
        "max_log2_stable_weighted_correction": (
            None
            if not stable_weighted_values
            else round(max(stable_weighted_values), 6)
        ),
        "entries": retained_remainder_entries(records, top_scales),
    }


def best_record(records: Sequence[Dict[str, object]], key: str) -> Dict[str, object]:
    def score(record: Dict[str, object]) -> tuple:
        value = record[key]
        numeric = -1.0 if value is None else float(value)
        return (numeric, int(record["dither"]))

    return min(records, key=score)


def best_window_record(records: Sequence[Dict[str, object]]) -> Optional[Dict[str, object]]:
    candidates = [record for record in records if "slack_window_ledger" in record]
    if not candidates:
        return None

    def score(record: Dict[str, object]) -> tuple:
        ledger = record["slack_window_ledger"]
        assert isinstance(ledger, dict)
        value = ledger["max_log2_first_codegree"]
        numeric = -1.0 if value is None else float(value)
        return (numeric, int(ledger["active_entry_count"]), int(record["dither"]))

    return min(candidates, key=score)


def best_remainder_window_record(
    records: Sequence[Dict[str, object]],
    weighted: bool,
) -> Optional[Dict[str, object]]:
    candidates = [record for record in records if "remainder_window_ledger" in record]
    if not candidates:
        return None
    if weighted:
        candidates = [
            record
            for record in candidates
            if record["remainder_window_ledger"][
                "max_log2_stable_weighted_correction"
            ]
            is not None
        ]
        if not candidates:
            return None

    def score(record: Dict[str, object]) -> tuple:
        ledger = record["remainder_window_ledger"]
        assert isinstance(ledger, dict)
        key = (
            "max_log2_stable_weighted_correction"
            if weighted
            else "max_log2_strict_codegree_mass"
        )
        value = ledger[key]
        numeric = -1.0 if value is None else float(value)
        return (numeric, int(ledger["active_entry_count"]), int(record["dither"]))

    return min(candidates, key=score)


def retained_scales(records: Sequence[ScaleRecord], top_scales: int) -> List[Dict[str, object]]:
    if top_scales < 0:
        return [item.to_json() for item in records]
    return [item.to_json() for item in records[:top_scales]]


def scan_case(
    m: int,
    rate: Fraction,
    eta: Fraction,
    max_dither: int,
    top_scales: int,
    slack_window: Optional[Tuple[int, int]],
    line_field_size: Optional[int],
    target_stable_gap: Optional[int],
    dither_menu_size: Optional[int],
) -> Dict[str, object]:
    n = 1 << m
    if (rate * n).denominator != 1:
        raise ValueError(f"rate {rate} does not give integral k at n=2^{m}")
    k0 = int(rate * n)
    sigma = ceil_fraction_times(eta, n)
    dither_records = []

    for dither in range(max_dither + 1):
        k = k0 - dither
        if k <= 0:
            continue
        exact = exact_scales(n, k, sigma)
        remainder = remainder_scales(n, k, sigma)
        record = {
            "dither": dither,
            "k": k,
            "gcd_n_k": math.gcd(n, k),
            "sigma": sigma,
            "rate_actual": k / n,
            "rate_loss": dither / n,
            "exact_profile_log2": (
                None if profile_value(exact) is None else round(profile_value(exact), 6)
            ),
            "exact_active_scales": retained_scales(exact, top_scales),
            "remainder_profile_log2": (
                None
                if profile_value(remainder) is None
                else round(profile_value(remainder), 6)
            ),
            "remainder_active_scales": retained_scales(remainder, top_scales),
        }
        if slack_window is not None:
            window_entries = slack_window_entries(n, k0, dither, slack_window)
            record["slack_window_ledger"] = slack_window_summary(
                window_entries,
                top_scales,
            )
            rem_window_entries = remainder_window_entries(
                n,
                k0,
                dither,
                slack_window,
                line_field_size,
            )
            record["remainder_window_ledger"] = remainder_window_summary(
                rem_window_entries,
                top_scales,
            )
        dither_records.append(record)

    result = {
        "m": m,
        "n": n,
        "rate_nominal": fraction_label(rate),
        "eta": fraction_label(eta),
        "k0": k0,
        "sigma": sigma,
        "max_dither": max_dither,
        "exact_rate": dither_records[0],
        "one_step_dither": next(
            (record for record in dither_records if record["dither"] == 1),
            None,
        ),
        "best_exact_dither": best_record(dither_records, "exact_profile_log2"),
        "best_remainder_dither": best_record(dither_records, "remainder_profile_log2"),
        "dithers": dither_records,
    }
    if slack_window is not None:
        result["slack_window"] = {"start": slack_window[0], "end": slack_window[1]}
        result["best_window_dither"] = best_window_record(dither_records)
        result["best_remainder_window_dither"] = best_remainder_window_record(
            dither_records,
            weighted=False,
        )
        result["adaptive_maximal_window_baseline"] = (
            adaptive_maximal_window_summary(
                n,
                k0,
                slack_window,
                line_field_size,
            )
        )
        if line_field_size is not None:
            result["line_field_size"] = line_field_size
            result["best_weighted_stable_tail_dither"] = (
                best_remainder_window_record(dither_records, weighted=True)
            )
        if target_stable_gap is not None and dither_menu_size is not None:
            result["dither_menu_tail_lower_bound"] = (
                dither_menu_tail_lower_bound_summary(
                    n,
                    k0,
                    slack_window,
                    target_stable_gap,
                    dither_menu_size,
                    top_scales,
                    line_field_size,
                )
            )
    return result


def scan(
    m_min: int,
    m_max: int,
    rates: Iterable[Fraction],
    etas: Iterable[Fraction],
    max_dither: int,
    top_scales: int,
    slack_window: Optional[Tuple[int, int]],
    line_field_size: Optional[int],
    target_stable_gap: Optional[int],
    dither_menu_size: Optional[int],
) -> Dict[str, object]:
    cases = []
    for m in range(m_min, m_max + 1):
        for rate in rates:
            for eta in etas:
                if (rate * (1 << m)).denominator == 1:
                    cases.append(
                        scan_case(
                            m,
                            rate,
                            eta,
                            max_dither,
                            top_scales,
                            slack_window,
                            line_field_size,
                            target_stable_gap,
                            dither_menu_size,
                        )
                    )
    return {
        "proof_status": "AUDIT / EXPERIMENTAL",
        "theorem_problem_id": "L3-quotient-profile-dimension-dithering",
        "determinism": "deterministic finite divisor scan; no random seed",
        "object_checked": (
            "exact Qprof_H(a,k) from snarks_v5.tex plus a separate "
            "small-remainder quotient-core diagnostic, optionally including "
            "the proved fixed-dither slack-window first-exchange ledger and "
            "the exact one-remainder strict codegree ledger, plus optional "
            "fixed-window and finite-menu dither covering certificates"
        ),
        "slack_window": (
            None
            if slack_window is None
            else {"start": slack_window[0], "end": slack_window[1]}
        ),
        "fixed_window_minimax": (
            None
            if slack_window is None
            else fixed_window_minimax_summary(slack_window, max_dither)
        ),
        "dither_menu_covering": (
            None
            if slack_window is None or target_stable_gap is None
            else dither_menu_covering_summary(
                slack_window,
                target_stable_gap,
                dither_menu_size,
            )
        ),
        "line_field_size": line_field_size,
        "cases": cases,
    }


def format_value(value: object) -> str:
    if value is None:
        return "empty"
    return f"{float(value):.2f}"


def format_scales(scales: Sequence[Dict[str, object]]) -> str:
    if not scales:
        return "-"
    pieces = []
    for scale in scales:
        piece = (
            f"M={scale['M_coset_size']},N={scale['N_quotient_order']},"
            f"log={float(scale['log2_list_size']):.1f}"
        )
        if "remainder" in scale:
            piece += (
                f",rem={scale['remainder']},T={scale['support_inside_coset']}"
            )
        pieces.append(piece)
    return "; ".join(pieces)


def format_window_entries(entries: Sequence[Dict[str, object]]) -> str:
    if not entries:
        return "-"
    pieces = []
    for entry in entries:
        pieces.append(
            "t={t},M={M},logGamma={log:.1f}".format(
                t=entry["slack"],
                M=entry["M_coset_size"],
                log=float(entry["log2_first_codegree"]),
            )
        )
    return "; ".join(pieces)


def format_remainder_entries(entries: Sequence[Dict[str, object]]) -> str:
    if not entries:
        return "-"
    pieces = []
    for entry in entries:
        weighted = ""
        if "log2_stable_weighted_correction" in entry:
            weighted = ",logR={:.1f}".format(
                float(entry["log2_stable_weighted_correction"])
            )
        pieces.append(
            "t={t},M={M},b={b},d={d},logMass={log:.1f}{stable}{side}{weighted}".format(
                t=entry["slack"],
                M=entry["M_coset_size"],
                b=entry["remainder"],
                d=entry["dither_gap"],
                log=float(entry["log2_strict_codegree_mass"]),
                stable=",stable" if entry["stable_large_scale_formula"] else "",
                side=(
                    ",{}".format(entry["stable_tail_side"])
                    if "stable_tail_side" in entry
                    else ""
                ),
                weighted=weighted,
            )
        )
    return "; ".join(pieces)


def print_text(result: Dict[str, object]) -> None:
    print("Quotient-profile dimension-dither scan")
    print("proof_status: AUDIT / EXPERIMENTAL")
    print("exact object: Qprof_H(a,k) at a=k+sigma")
    print("remainder object: diagnostic for sigma+remainder < M")
    if result["slack_window"] is not None:
        window = result["slack_window"]
        assert isinstance(window, dict)
        print(
            "slack-window object: L_win(r) for t={start}..{end}".format(
                start=window["start"],
                end=window["end"],
            )
        )
        minimax = result["fixed_window_minimax"]
        assert isinstance(minimax, dict)
        print(
            (
                "fixed-window minimax: center radius {center}, "
                "no-exact-k0 radius {free}, scanned no-exact-k0 {scan} at r={best}"
            ).format(
                center=minimax["unconstrained_integer_min_radius"],
                free=minimax["zero_gap_free_integer_min_radius"],
                scan=(
                    "none"
                    if minimax["scanned_zero_gap_free_min_radius"] is None
                    else minimax["scanned_zero_gap_free_min_radius"]
                ),
                best=(
                    "-"
                    if minimax["scanned_zero_gap_free_best_dithers"] is None
                    else ",".join(
                        str(item)
                        for item in minimax["scanned_zero_gap_free_best_dithers"]
                    )
                ),
            )
        )
        menu_covering = result.get("dither_menu_covering")
        if menu_covering is not None:
            assert isinstance(menu_covering, dict)
            print(
                (
                    "dither-menu covering: gap<={gap} exactly needs {exact} "
                    "dithers; adaptive-competitive menu needs {adaptive}; "
                    "coarse lower bound {lower}; regime={regime}"
                ).format(
                    gap=menu_covering["target_stable_gap"],
                    exact=menu_covering["exact_min_menu_size_for_target_gap"],
                    adaptive=menu_covering[
                        "exact_min_menu_size_for_asymptotic_adaptive_competitiveness"
                    ],
                    lower=menu_covering["coarse_menu_size_lower_bound"],
                    regime=menu_covering.get("large_scale_menu_regime", "-"),
                )
            )
    if result.get("line_field_size") is not None:
        print(f"line field size for weighted stable tails: {result['line_field_size']}")
    print()

    for case in result["cases"]:
        exact = case["exact_rate"]
        one = case["one_step_dither"]
        best_exact = case["best_exact_dither"]
        best_remainder = case["best_remainder_dither"]
        best_window = case.get("best_window_dither")
        best_rem_window = case.get("best_remainder_window_dither")
        best_weighted_tail = case.get("best_weighted_stable_tail_dither")
        menu_tail_bound = case.get("dither_menu_tail_lower_bound")
        adaptive_baseline = case.get("adaptive_maximal_window_baseline")
        print(
            "m={m:>2} n=2^{m:<2} rho={rho:<4} eta={eta:<5} sigma={sigma:<6} "
            "k0={k0}".format(
                m=case["m"],
                rho=case["rate_nominal"],
                eta=case["eta"],
                sigma=case["sigma"],
                k0=case["k0"],
            )
        )
        print(
            "  r=0 exact={exact} remainder={remainder} gcd={gcd}".format(
                exact=format_value(exact["exact_profile_log2"]),
                remainder=format_value(exact["remainder_profile_log2"]),
                gcd=exact["gcd_n_k"],
            )
        )
        if one is not None:
            print(
                "  r=1 exact={exact} remainder={remainder} gcd={gcd}".format(
                    exact=format_value(one["exact_profile_log2"]),
                    remainder=format_value(one["remainder_profile_log2"]),
                    gcd=one["gcd_n_k"],
                )
            )
        print(
            "  best exact r={r} value={value}; best remainder r={rr} value={rvalue}".format(
                r=best_exact["dither"],
                value=format_value(best_exact["exact_profile_log2"]),
                rr=best_remainder["dither"],
                rvalue=format_value(best_remainder["remainder_profile_log2"]),
            )
        )
        if best_window is not None:
            ledger = best_window["slack_window_ledger"]
            assert isinstance(ledger, dict)
            print(
                "  best window r={r} max_logGamma={value} entries={entries}".format(
                    r=best_window["dither"],
                    value=format_value(ledger["max_log2_first_codegree"]),
                    entries=ledger["active_entry_count"],
                )
            )
        if best_rem_window is not None:
            ledger = best_rem_window["remainder_window_ledger"]
            assert isinstance(ledger, dict)
            print(
                "  best remainder-window r={r} max_logMass={value} entries={entries}".format(
                    r=best_rem_window["dither"],
                    value=format_value(ledger["max_log2_strict_codegree_mass"]),
                    entries=ledger["active_entry_count"],
                )
            )
        if best_weighted_tail is not None:
            ledger = best_weighted_tail["remainder_window_ledger"]
            assert isinstance(ledger, dict)
            print(
                (
                    "  best weighted stable-tail r={r} "
                    "max_logR={value} stable_entries={entries}"
                ).format(
                    r=best_weighted_tail["dither"],
                    value=format_value(ledger["max_log2_stable_weighted_correction"]),
                    entries=ledger["stable_entry_count"],
                )
            )
        if menu_tail_bound is not None:
            assert isinstance(menu_tail_bound, dict)
            print(
                (
                    "  menu tail lower bound C={menu} forced_gap>={gap} "
                    "max_logMass>={value} max_logR>={weighted} "
                    "max_log_vs_adapt={ratio} "
                    "first_adapt_dom_scale={first_scale} "
                    "first_winR_dom_scale={first_window_scale} "
                    "scales={scales}"
                ).format(
                    menu=menu_tail_bound["queried_menu_size"],
                    gap=menu_tail_bound["exact_forced_safe_gap_lower_bound"],
                    value=format_value(
                        menu_tail_bound["max_log2_stable_tail_mass_lower_bound"]
                    ),
                    weighted=format_value(
                        menu_tail_bound[
                            "max_log2_stable_tail_weighted_lower_bound"
                        ]
                    ),
                    ratio=format_value(
                        menu_tail_bound["max_log2_mass_over_adaptive_linear"]
                    ),
                    first_scale=format_value(
                        menu_tail_bound[
                            "min_scale_mass_dominates_adaptive_linear"
                        ]
                    ),
                    first_window_scale=format_value(
                        menu_tail_bound[
                            "min_scale_window_weighted_dominates_adaptive"
                        ]
                    ),
                    scales=menu_tail_bound["stable_eligible_scale_count"],
                )
            )
        if adaptive_baseline is not None:
            assert isinstance(adaptive_baseline, dict)
            print(
                (
                    "  adaptive maximal baseline stable_scales={scales} "
                    "logMass={mass} max_logR={weighted}"
                ).format(
                    scales=adaptive_baseline["stable_scale_count"],
                    mass=format_value(
                        adaptive_baseline[
                            "max_log2_linear_mass_per_stable_scale"
                        ]
                    ),
                    weighted=format_value(
                        adaptive_baseline.get(
                            "max_log2_weighted_correction_per_stable_scale"
                        )
                    ),
                )
            )
        print("  active exact scales: " + format_scales(exact["exact_active_scales"]))
        print(
            "  active remainder scales: "
            + format_scales(exact["remainder_active_scales"])
        )
        if "slack_window_ledger" in exact:
            ledger = exact["slack_window_ledger"]
            assert isinstance(ledger, dict)
            entries = ledger["entries"]
            assert isinstance(entries, list)
            print("  r=0 window entries: " + format_window_entries(entries))
        if "remainder_window_ledger" in exact:
            ledger = exact["remainder_window_ledger"]
            assert isinstance(ledger, dict)
            entries = ledger["entries"]
            assert isinstance(entries, list)
            print(
                "  r=0 remainder-window entries: "
                + format_remainder_entries(entries)
            )
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan dyadic quotient-profile obstructions under dimension dithering."
    )
    parser.add_argument("--m-min", type=int, default=8, help="minimum m for n=2^m")
    parser.add_argument("--m-max", type=int, default=20, help="maximum m for n=2^m")
    parser.add_argument(
        "--rates",
        type=parse_fraction_list,
        default=list(DEFAULT_RATES),
        help="comma-separated nominal rates, e.g. 1/2,1/4",
    )
    parser.add_argument(
        "--etas",
        type=parse_fraction_list,
        default=list(DEFAULT_ETAS),
        help="comma-separated reserves eta, e.g. 1/64,1/32,1/16",
    )
    parser.add_argument(
        "--max-dither",
        type=int,
        default=16,
        help="scan k=rho*n-r for 0 <= r <= max-dither",
    )
    parser.add_argument(
        "--top-scales",
        type=int,
        default=-1,
        help="number of active scales retained per dither; negative retains all",
    )
    parser.add_argument(
        "--slack-window",
        type=parse_slack_window,
        default=None,
        help="optional inclusive slack window START:END for the proved L_win(r) ledger",
    )
    parser.add_argument(
        "--line-field-size",
        type=int,
        default=None,
        help="optional q_line used to report weighted stable one-remainder tails",
    )
    parser.add_argument(
        "--target-stable-gap",
        type=int,
        default=None,
        help=(
            "optional D for the theorem-backed finite-menu covering bound; "
            "requires --slack-window"
        ),
    )
    parser.add_argument(
        "--dither-menu-size",
        type=int,
        default=None,
        help=(
            "optional C for stable-tail lower bounds from a C-value dither menu; "
            "requires --target-stable-gap"
        ),
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    args = parser.parse_args()

    if args.m_min < 1 or args.m_max < args.m_min:
        raise SystemExit("require 1 <= --m-min <= --m-max")
    if args.max_dither < 0:
        raise SystemExit("--max-dither must be nonnegative")
    if args.line_field_size is not None and args.line_field_size <= 1:
        raise SystemExit("--line-field-size must be greater than one")
    if args.target_stable_gap is not None and args.target_stable_gap < 1:
        raise SystemExit("--target-stable-gap must be positive")
    if args.dither_menu_size is not None and args.dither_menu_size < 1:
        raise SystemExit("--dither-menu-size must be positive")
    if args.target_stable_gap is not None and args.slack_window is None:
        raise SystemExit("--target-stable-gap requires --slack-window")
    if args.dither_menu_size is not None and args.target_stable_gap is None:
        raise SystemExit("--dither-menu-size requires --target-stable-gap")
    result = scan(
        m_min=args.m_min,
        m_max=args.m_max,
        rates=args.rates,
        etas=args.etas,
        max_dither=args.max_dither,
        top_scales=args.top_scales,
        slack_window=args.slack_window,
        line_field_size=args.line_field_size,
        target_stable_gap=args.target_stable_gap,
        dither_menu_size=args.dither_menu_size,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
