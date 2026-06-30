#!/usr/bin/env python3
"""Exact evaluator for the M1 sparse-certificate density budget.

This is an AUDIT helper for the local M1 sparse-certificate chain in
``experimental/notes/m1/m1_same_slope_root_slice_lemma.md``.  It evaluates the
integer ceiling

    R_Z(a0,L) = ceil(R_dens(a0,L)) - 1

from (RKSQINTBUDGET), using exact rational arithmetic.  If an endpoint
footprint cap S is supplied, it also uses the optimal compatible far-factor

    L_S = floor((S+1)/(2D)).

With ``--target-R`` it prints the exact density inequalities that would close
that target support budget.

With ``--scan-targets-up-to`` it scans exact active target thresholds for
integer budgets and certifies the monotonicity from (RKSQTARGETMONO).

With ``--baseline-a0`` it uses the unconditional reduced-support density floor
``a0=2/e`` from (RKSQMINALPHA).

With ``--quartic-window`` it evaluates the first nontrivial palette case
``e=4`` from (RKSQQUARTICCOUNT/RKSQQUARTICFAR).  If ``--quartic-m`` and
``--target-R`` are also supplied, it computes the exact minimum number of
one-class residual supports forced by the selected-side and missing-side
quartic inequalities.

With ``--residual-m``, ``--target-R``, and ``--e``, it computes the exact
integer feasibility interval for the sparse certificate class counts
``K_ap`` and ``C_ap`` at that residual size, and the minimum integer target
budget ``R`` for which any class-count certificate can exist.

When ``--e`` is supplied, it also reports the monotone far-star class-count
floor at ``m_ap=L D``.

The script does not prove the missing global row-basis/core-image density
bound.  It tells a finite checker what support budget that hypothetical bound
would close, and what near-star template ledger remains.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from fractions import Fraction
from typing import Any


def positive_int(text: str) -> int:
    try:
        value = int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not an integer: {text}") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return value


def nonnegative_int(text: str) -> int:
    try:
        value = int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not an integer: {text}") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return value


def even_positive_int(text: str) -> int:
    value = positive_int(text)
    if value % 2:
        raise argparse.ArgumentTypeError("must be even")
    return value


def rational(text: str) -> Fraction:
    try:
        value = Fraction(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not a rational number: {text}") from exc
    return value


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def floor_sqrt_fraction(value: Fraction) -> int:
    if value < 0:
        raise ValueError("cannot take square root of a negative rational")
    return math.isqrt(value.numerator // value.denominator)


def fraction_record(value: Fraction) -> dict[str, Any]:
    try:
        decimal = float(value)
    except OverflowError:
        decimal = None
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": decimal,
        "text": str(value),
    }


def square_threshold_record(value: Fraction) -> dict[str, Any]:
    try:
        sqrt_decimal = math.sqrt(float(value))
    except OverflowError:
        sqrt_decimal = None
    return {
        "square": fraction_record(value),
        "sqrt_decimal": sqrt_decimal if value >= 0 else None,
        "comparison": "alpha_ap^2 > square",
    }


def active_target_kind(selected_square: Fraction, missing: Fraction) -> str:
    if missing < 0:
        return "missing"
    if selected_square <= missing * missing:
        return "selected"
    return "missing"


def active_target_record(selected_square: Fraction, missing: Fraction) -> dict[str, Any]:
    active_kind = active_target_kind(selected_square, missing)
    if active_kind == "selected":
        return {
            "active_side": "selected",
            "threshold": square_threshold_record(selected_square),
            "strict_condition": "alpha_ap^2 > selected_side_square",
            "reason": "selected_side_at_most_missing_side",
        }
    return {
        "active_side": "missing",
        "threshold": fraction_record(missing),
        "strict_condition": "alpha_ap > missing_side",
        "reason": "missing_side_is_negative"
        if missing < 0
        else "missing_side_below_selected_side",
    }


def target_components(
    q: int,
    far_factor: int,
    support_budget: int,
) -> tuple[Fraction, Fraction]:
    selected_denominator = (q - 3) * far_factor + 2
    selected_square = (
        Fraction(support_budget * selected_denominator, far_factor)
        / ((q - 1) * (q - 1))
    )
    missing = (
        Fraction(1)
        - Fraction(far_factor - 1, far_factor)
        * Fraction(q + 1 - support_budget, q - 1)
    )
    return selected_square, missing


def target_leq(
    left_selected_square: Fraction,
    left_missing: Fraction,
    right_selected_square: Fraction,
    right_missing: Fraction,
) -> bool:
    left_kind = active_target_kind(left_selected_square, left_missing)
    right_kind = active_target_kind(right_selected_square, right_missing)
    if left_kind == "missing" and right_kind == "missing":
        return left_missing <= right_missing
    if left_kind == "missing":
        return (
            left_missing < 0
            or left_missing * left_missing <= right_selected_square
        )
    if right_kind == "missing":
        return (
            right_missing >= 0
            and left_selected_square <= right_missing * right_missing
        )
    return left_selected_square <= right_selected_square


def target_scan(q: int, far_factor: int, max_support_budget: int) -> dict[str, Any]:
    rows = []
    previous: tuple[Fraction, Fraction] | None = None
    monotone = True
    for support_budget in range(max_support_budget + 1):
        selected_square, missing = target_components(q, far_factor, support_budget)
        if previous is not None and not target_leq(
            previous[0],
            previous[1],
            selected_square,
            missing,
        ):
            monotone = False
        previous = (selected_square, missing)
        rows.append(
            {
                "R": support_budget,
                "active_scalar_target": active_target_record(
                    selected_square, missing
                ),
                "selected_side_square": fraction_record(selected_square),
                "missing_side": fraction_record(missing),
            }
        )
    return {
        "max_R": max_support_budget,
        "monotone_non_decreasing": monotone,
        "rows": rows,
        "certificate": (
            "Exact branch-aware comparisons of A_target(q,R,L) for "
            "R=0..max_R; theorem RKSQTARGETMONO proves this for all R."
        ),
    }


def quartic_window_report(args: argparse.Namespace, far_factor: int) -> dict[str, Any]:
    q = args.q
    d_cap = args.D
    selected_denominator = (q - 3) * far_factor + 2
    selected_threshold = Fraction(
        (q - 1) * (q - 1) * far_factor,
        4 * selected_denominator,
    )
    missing_threshold = (
        Fraction(q + 1)
        - Fraction(far_factor, 2 * (far_factor - 1)) * (q - 1)
    )
    quartic_threshold = max(selected_threshold, missing_threshold)
    report: dict[str, Any] = {
        "object": "m1_quartic_palette_partial_window",
        "status": "AUDIT",
        "theorem_problem_id": (
            "M1 / RKSQQUARTICCOUNT / RKSQQUARTICFAR / RKSQQUARTICHALF"
        ),
        "e": 4,
        "selected_side_R_threshold": fraction_record(selected_threshold),
        "missing_side_half_line_R_threshold": fraction_record(missing_threshold),
        "combined_far_sparse_R_threshold": fraction_record(quartic_threshold),
        "combined_integer_R_Z": ceil_fraction(quartic_threshold) - 1,
        "certificate": (
            "For e=4, P_ap/m_ap is forced above both the selected-side "
            "and missing-side lower bounds. Since P_ap<=m_ap, a far-star "
            "sparse certificate is impossible for integer R<=combined_R_Z."
        ),
    }
    if args.target_R is not None:
        selected_square, _ = target_components(q, far_factor, args.target_R)
        missing_fraction = (
            Fraction(2 * (far_factor - 1), far_factor)
            * Fraction(q + 1 - args.target_R, q - 1)
        )
        report["target_R"] = args.target_R
        report["target_partial_fraction_bounds"] = {
            "selected_side_square": fraction_record(selected_square),
            "selected_side_expression": (
                "P_ap/m_ap >= 2(1 - sqrt(selected_side_square))"
            ),
            "selected_side_impossible_from_P_le_m": selected_square < Fraction(1, 4),
            "missing_side": fraction_record(missing_fraction),
            "missing_side_expression": (
                "P_ap/m_ap >= 2((L-1)/L)(q+1-R)/(q-1)"
            ),
            "missing_side_impossible_from_P_le_m": missing_fraction > 1,
            "far_sparse_branch_excluded": args.target_R <= (
                ceil_fraction(quartic_threshold) - 1
            ),
        }
    if args.quartic_m is not None:
        if args.target_R is None:
            raise ValueError("--quartic-m requires --target-R")
        residual_size = args.quartic_m
        sparse_size_condition = residual_size > d_cap
        selected_rhs = Fraction(
            4
            * args.target_R
            * ((q - 3) * residual_size * residual_size + 2 * residual_size * d_cap),
            (q - 1) * (q - 1),
        )
        selected_max_full_class_mass = floor_sqrt_fraction(selected_rhs)
        selected_min_partial = max(0, 2 * residual_size - selected_max_full_class_mass)
        missing_min_partial = ceil_fraction(
            Fraction(
                2 * (residual_size - d_cap) * (q + 1 - args.target_R),
                q - 1,
            )
        )
        missing_min_partial = max(0, missing_min_partial)
        min_partial = max(selected_min_partial, missing_min_partial)
        report["finite_residual_size"] = {
            "m_ap": residual_size,
            "requires_sparse_size_condition_m_gt_D": sparse_size_condition,
            "selected_side_rhs_for_(2m-P)^2": fraction_record(selected_rhs),
            "selected_side_max_2m_minus_P": selected_max_full_class_mass,
            "selected_side_min_P_ap": selected_min_partial,
            "missing_side_min_P_ap": missing_min_partial,
            "forced_min_P_ap": min_partial,
            "impossible_for_this_m": (not sparse_size_condition) or min_partial > residual_size,
        }
    return report


def finite_sparse_feasibility_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.e is None:
        raise ValueError("--residual-m requires --e")
    if args.target_R is None:
        raise ValueError("--residual-m requires --target-R")
    q = args.q
    d_cap = args.D
    residual_size = args.residual_m
    h = args.e // 2
    total_classes = h * residual_size
    max_missing_classes = (h - 1) * residual_size
    star_bound = (
        (q - 3) * residual_size * residual_size + 2 * residual_size * d_cap
    )
    selected_rhs = Fraction(
        h
        * h
        * args.target_R
        * star_bound,
        (q - 1) * (q - 1),
    )
    max_selected_classes = min(total_classes, floor_sqrt_fraction(selected_rhs))
    selected_forced_missing = max(0, total_classes - max_selected_classes)
    missing_forced_missing = max(
        0,
        ceil_fraction(
            Fraction(
                h
                * (residual_size - d_cap)
                * (q + 1 - args.target_R),
                q - 1,
            )
        ),
    )
    forced_missing_classes = max(selected_forced_missing, missing_forced_missing)
    selected_upper = total_classes - forced_missing_classes
    sparse_size_condition = residual_size > d_cap
    feasible = (
        sparse_size_condition
        and forced_missing_classes <= max_missing_classes
        and selected_upper >= residual_size
    )
    target_floor = sparse_target_floor_report(q, d_cap, args.e, residual_size)
    selected_min_target = target_floor["selected_side_min_target_R_at_K_eq_m"]
    missing_min_target = target_floor["missing_side_min_target_R_at_K_eq_m"]
    minimal_target = target_floor["minimal_target_R_for_class_count_feasibility"]
    feasible_for_some_target = target_floor[
        "class_count_feasible_for_some_R_leq_q_plus_one"
    ]
    return {
        "object": "m1_finite_sparse_certificate_feasibility",
        "status": "AUDIT",
        "theorem_problem_id": "M1 / RKSQSPCERT1 / RKSQSPCERT2",
        "e": args.e,
        "h": h,
        "target_R": args.target_R,
        "m_ap": residual_size,
        "requires_sparse_size_condition_m_gt_D": sparse_size_condition,
        "total_palette_classes_hm": total_classes,
        "selected_class_range_unconditional": [residual_size, total_classes],
        "missing_class_range_unconditional": [0, max_missing_classes],
        "selected_side_rhs_for_K_ap_squared": fraction_record(selected_rhs),
        "selected_side_max_K_ap": max_selected_classes,
        "selected_side_min_C_ap": selected_forced_missing,
        "missing_side_min_C_ap": missing_forced_missing,
        "forced_min_C_ap": forced_missing_classes,
        "selected_side_min_target_R_at_K_eq_m": selected_min_target,
        "missing_side_min_target_R_at_K_eq_m": missing_min_target,
        "minimal_target_R_for_class_count_feasibility": minimal_target,
        "class_count_feasible_for_some_R_leq_q_plus_one": feasible_for_some_target,
        "target_R_meets_minimum_class_count_floor": (
            args.target_R >= minimal_target if minimal_target is not None else False
        ),
        "feasible_K_ap_interval": [residual_size, selected_upper]
        if feasible
        else None,
        "feasible_C_ap_interval": [forced_missing_classes, max_missing_classes]
        if feasible
        else None,
        "sparse_certificate_arithmetically_possible": feasible,
        "certificate": (
            "Exact integer restatement of RKSQSPCERT1/RKSQSPCERT2 at fixed "
            "m_ap. Feasibility requires m_ap>D, m_ap<=K_ap<=hm_ap, "
            "0<=C_ap<=(h-1)m_ap, K_ap+C_ap=hm_ap, and both support-budget "
            "inequalities. The minimum target budget is attained at K_ap=m_ap."
        ),
    }


def sparse_target_floor_report(
    q: int,
    d_cap: int,
    e: int,
    residual_size: int,
) -> dict[str, Any]:
    h = e // 2
    if residual_size <= d_cap:
        return {
            "object": "m1_sparse_class_count_target_floor",
            "status": "AUDIT",
            "e": e,
            "h": h,
            "m_ap": residual_size,
            "requires_sparse_size_condition_m_gt_D": False,
            "selected_side_min_target_R_at_K_eq_m": None,
            "missing_side_min_target_R_at_K_eq_m": None,
            "minimal_target_R_for_class_count_feasibility": None,
            "class_count_feasible_for_some_R_leq_q_plus_one": False,
        }
    star_bound = (
        (q - 3) * residual_size * residual_size + 2 * residual_size * d_cap
    )
    if star_bound <= 0:
        raise ValueError("require positive sparse star bound")
    max_missing_classes = (h - 1) * residual_size
    selected_min_target = ceil_fraction(
        Fraction(
            (q - 1) * (q - 1) * residual_size * residual_size,
            h * h * star_bound,
        )
    )
    missing_min_target = max(
        0,
        q
        + 1
        - (
            ((q - 1) * max_missing_classes)
            // (h * (residual_size - d_cap))
        ),
    )
    minimal_target = max(selected_min_target, missing_min_target)
    return {
        "object": "m1_sparse_class_count_target_floor",
        "status": "AUDIT",
        "e": e,
        "h": h,
        "m_ap": residual_size,
        "requires_sparse_size_condition_m_gt_D": True,
        "selected_side_min_target_R_at_K_eq_m": selected_min_target,
        "missing_side_min_target_R_at_K_eq_m": missing_min_target,
        "minimal_target_R_for_class_count_feasibility": minimal_target,
        "class_count_feasible_for_some_R_leq_q_plus_one": minimal_target <= q + 1,
        "certificate": (
            "For fixed m_ap, RKSQSPCERT1/RKSQSPCERT2 first become "
            "class-count feasible at K_ap=m_ap."
        ),
    }


def far_star_sparse_floor_report(
    q: int,
    d_cap: int,
    e: int,
    far_factor: int,
) -> dict[str, Any]:
    h = e // 2
    if far_factor < 2:
        raise ValueError("far-star floor requires L>=2")
    selected_argument = Fraction(
        (q - 1) * (q - 1) * far_factor,
        h * h * ((q - 3) * far_factor + 2),
    )
    missing_argument = Fraction(
        (q - 1) * (h - 1) * far_factor,
        h * (far_factor - 1),
    )
    selected_min_target = ceil_fraction(selected_argument)
    missing_min_target = max(
        0,
        q + 1 - (missing_argument.numerator // missing_argument.denominator),
    )
    minimal_target = max(selected_min_target, missing_min_target)
    boundary_residual_size = far_factor * d_cap
    fixed_boundary = sparse_target_floor_report(q, d_cap, e, boundary_residual_size)
    assert selected_min_target == fixed_boundary[
        "selected_side_min_target_R_at_K_eq_m"
    ]
    assert missing_min_target == fixed_boundary[
        "missing_side_min_target_R_at_K_eq_m"
    ]
    assert minimal_target == fixed_boundary[
        "minimal_target_R_for_class_count_feasibility"
    ]
    return {
        "object": "m1_far_star_sparse_class_count_floor",
        "status": "AUDIT",
        "e": e,
        "h": h,
        "L": far_factor,
        "minimum_residual_size_m_ge_LD": boundary_residual_size,
        "selected_side_closed_form_argument": fraction_record(selected_argument),
        "missing_side_closed_form_floor_argument": fraction_record(
            missing_argument
        ),
        "selected_side_min_target_R_at_K_eq_m": selected_min_target,
        "missing_side_min_target_R_at_K_eq_m": missing_min_target,
        "minimal_target_R_for_class_count_feasibility": minimal_target,
        "selected_side_min_target_R_at_m_eq_LD": selected_min_target,
        "missing_side_min_target_R_at_m_eq_LD": missing_min_target,
        "minimal_target_R_for_far_star_class_count_feasibility": minimal_target,
        "class_count_feasible_for_some_R_leq_q_plus_one": minimal_target <= q + 1,
        "D_independent_closed_form": True,
        "certificate": (
            "Substituting m_ap=LD into R_min(m_ap) cancels D. Since "
            "R_min(m_ap) is nondecreasing for m_ap>D, every class-count "
            "sparse certificate with m_ap>=LD requires this boundary floor."
        ),
    }


def template_bound(q: int, footprint_cap: int, e: int) -> int:
    h = e // 2
    return sum(
        math.comb(q + 1, footprint_size)
        * (1 << (h * math.comb(footprint_size, 2)))
        for footprint_size in range(footprint_cap + 1)
    )


def compute_report(args: argparse.Namespace) -> dict[str, Any]:
    q = args.q
    d_cap = args.D
    if args.baseline_a0 and args.a0 is not None:
        raise ValueError("provide only one of --a0 or --baseline-a0")
    if args.baseline_a0:
        if args.e is None:
            raise ValueError("--baseline-a0 requires --e")
        a0 = Fraction(2, args.e)
    else:
        if args.a0 is None:
            raise ValueError("provide --a0 or --baseline-a0")
        a0 = args.a0
    if not (Fraction(0) <= a0 <= Fraction(1)):
        raise ValueError("--a0 must satisfy 0 <= a0 <= 1")
    if args.R is not None and args.R > q + 1:
        raise ValueError("--R must be at most q+1")
    if args.target_R is not None and args.target_R > q + 1:
        raise ValueError("--target-R must be at most q+1")
    if args.scan_targets_up_to is not None and args.scan_targets_up_to > q + 1:
        raise ValueError("--scan-targets-up-to must be at most q+1")
    if args.quartic_m is not None and not args.quartic_window:
        raise ValueError("--quartic-m requires --quartic-window")
    if args.residual_m is not None:
        if args.e is None:
            raise ValueError("--residual-m requires --e")
        if args.target_R is None:
            raise ValueError("--residual-m requires --target-R")

    if args.L is not None:
        far_factor = args.L
        if far_factor < 2:
            raise ValueError("--L must be at least 2")
        footprint_cap = min(q + 1, max(0, 2 * far_factor * d_cap - 1))
        footprint_source = "from_L"
    else:
        if args.S < 4 * d_cap - 1:
            raise ValueError("--S must be at least 4D-1")
        far_factor = (args.S + 1) // (2 * d_cap)
        if far_factor < 2:
            raise ValueError("derived L_S must be at least 2")
        footprint_cap = min(q + 1, args.S)
        footprint_source = "from_S"

    selected_denominator = (q - 3) * far_factor + 2
    if selected_denominator <= 0:
        raise ValueError("require q-3+2/L > 0")

    r_sel = (
        a0
        * a0
        * (q - 1)
        * (q - 1)
        * far_factor
        / selected_denominator
    )
    r_miss = (
        Fraction(q + 1)
        - Fraction(far_factor, far_factor - 1) * (1 - a0) * (q - 1)
    )
    r_dens = max(r_sel, r_miss)
    r_z = ceil_fraction(r_dens) - 1
    target_selected_square = target_missing = None
    if args.target_R is not None:
        target_selected_square, target_missing = target_components(
            q, far_factor, args.target_R
        )

    report: dict[str, Any] = {
        "object": "m1_sparse_certificate_density_budget",
        "status": "AUDIT",
        "theorem_problem_id": (
            "M1 / RKSQALPHA0 / RKSQBUDGET / RKSQINTBUDGET / RKSQTRADE"
        ),
        "q": q,
        "D": d_cap,
        "a0": fraction_record(a0),
        "a0_source": "baseline_2_over_e" if args.baseline_a0 else "input",
        "L": far_factor,
        "footprint_cap": footprint_cap,
        "footprint_source": footprint_source,
        "R_sel": fraction_record(r_sel),
        "R_miss": fraction_record(r_miss),
        "R_dens": fraction_record(r_dens),
        "R_Z": r_z,
        "proof_certificate": (
            "Exact Fraction arithmetic. R_Z=ceil(max(R_sel,R_miss))-1, so "
            "an integer R satisfies R<R_dens iff R<=R_Z."
        ),
        "notes": [
            "This script assumes a separate theorem proves alpha_ap >= a0.",
            "Closed budgets leave the endpoint-star, D-small, large-support, "
            "or near-star template branches from the M1 local theorem.",
        ],
    }

    if args.e is not None:
        far_star_floor = far_star_sparse_floor_report(
            q,
            d_cap,
            args.e,
            far_factor,
        )
        if args.R is not None:
            far_star_floor["queried_R_excluded_by_class_count_floor"] = (
                args.R
                < far_star_floor[
                    "minimal_target_R_for_far_star_class_count_feasibility"
                ]
            )
        if args.target_R is not None:
            far_star_floor["target_R_excluded_by_class_count_floor"] = (
                args.target_R
                < far_star_floor[
                    "minimal_target_R_for_far_star_class_count_feasibility"
                ]
            )
        report["far_star_sparse_class_count_floor"] = far_star_floor

    if args.R is not None:
        report["queried_R"] = args.R
        report["queried_R_closes_far_sparse_branch"] = args.R <= r_z

    if args.target_R is not None:
        assert target_selected_square is not None
        assert target_missing is not None
        report["target_R"] = args.target_R
        report["required_density_to_close_target_R"] = {
            "selected_side": square_threshold_record(target_selected_square),
            "missing_side": fraction_record(target_missing),
            "active_scalar_target": active_target_record(
                target_selected_square, target_missing
            ),
            "certificate": (
                "For an integer target R, alpha_ap > theta_L(q,R) is "
                "equivalent to either alpha_ap^2 > "
                "R(q-3+2/L)/(q-1)^2 or alpha_ap > "
                "1-((L-1)/L)(q+1-R)/(q-1)."
            ),
        }

    if args.scan_targets_up_to is not None:
        report["target_scan"] = target_scan(
            q, far_factor, args.scan_targets_up_to
        )

    if args.quartic_window:
        report["quartic_palette_window"] = quartic_window_report(args, far_factor)

    if args.residual_m is not None:
        report["finite_sparse_certificate_feasibility"] = (
            finite_sparse_feasibility_report(args)
        )

    if args.e is not None:
        exact_template_bound = None
        omitted_reason = None
        if footprint_cap <= args.template_exact_limit:
            exact_template_bound = template_bound(q, footprint_cap, args.e)
        else:
            omitted_reason = (
                "footprint_cap exceeds --template-exact-limit; rerun with a "
                "larger limit if this exact integer is needed"
            )
        report["e"] = args.e
        report["template_bound"] = {
            "formula": (
                "sum_{s=0}^{footprint_cap} binom(q+1,s) "
                "2^((e/2) binom(s,2))"
            ),
            "exact": exact_template_bound,
            "omitted_reason": omitted_reason,
            "template_exact_limit": args.template_exact_limit,
        }

    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", type=positive_int, required=True)
    parser.add_argument("--D", type=positive_int, required=True)
    parser.add_argument("--a0", type=rational)
    parser.add_argument("--baseline-a0", action="store_true")
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--L", type=positive_int)
    selector.add_argument("--S", type=nonnegative_int)
    parser.add_argument("--R", type=nonnegative_int)
    parser.add_argument("--target-R", type=nonnegative_int)
    parser.add_argument("--scan-targets-up-to", type=nonnegative_int)
    parser.add_argument("--e", type=even_positive_int)
    parser.add_argument("--template-exact-limit", type=nonnegative_int, default=64)
    parser.add_argument("--quartic-window", action="store_true")
    parser.add_argument("--quartic-m", type=positive_int)
    parser.add_argument("--residual-m", type=positive_int)
    parser.add_argument("--pretty", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = compute_report(args)
    except ValueError as exc:
        parser.error(str(exc))
    json.dump(report, sys.stdout, indent=2 if args.pretty else None, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
