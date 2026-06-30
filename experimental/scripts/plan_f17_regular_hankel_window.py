#!/usr/bin/env python3
"""Plan the F_17^32 regular Hankel-minor window.

This script is an M3 audit helper for the Paper D v9 atlas.  It does not
compute determinants over F_17^32.  Instead it records the exact arithmetic of
the first non-tangent regular window for the prize-facing row:

    RS[F_17^32, H, 256], |H| = 512.

The output is a deterministic JSON plan saying which exact agreements are
regular overdetermined, which prefix maximal minors are syntactically defined,
how many determinant evaluations interpolation would need, and why the raw
degree bounds do not by themselves clear the 2^-128 finite-slope budget.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_N = 512
DEFAULT_K = 256
DEFAULT_FIELD = "F_17^32"
DEFAULT_FIELD_ORDER = 17**32
DEFAULT_EPSILON_DENOMINATOR = 2**128
DEFAULT_DOMAIN_HASH = "35904a892e0319b3805e91438ec2733427a351a72ce9654428d6a33bd3575b92"
DEFAULT_ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)


def ceil_div(numerator: int, denominator: int) -> int:
    return -(-numerator // denominator)


def regular_start(n: int, k: int) -> int:
    """Smallest A with t=A-k >= j+1=n-A+1."""
    return ceil_div(n + k + 1, 2)


def tangent_start(n: int, k: int) -> int:
    """Smallest A in the high-agreement tangent-exact range."""
    return n - ((n - k) // 3)


def agreement_record(a_value: int, n: int, k: int) -> dict[str, Any]:
    j_value = n - a_value
    t_value = a_value - k
    minor_size = j_value + 1
    prefix_max_syndrome_index = 2 * j_value
    full_hankel_max_syndrome_index = (t_value - 1) + j_value
    return {
        "A": a_value,
        "j": j_value,
        "t": t_value,
        "regular_overdetermined": t_value >= minor_size,
        "minor_size": minor_size,
        "degree_bound": minor_size,
        "interpolation_evaluations": minor_size + 1,
        "prefix_row_set": {"start": 0, "stop_inclusive": j_value},
        "prefix_max_syndrome_index": prefix_max_syndrome_index,
        "full_hankel_max_syndrome_index": full_hankel_max_syndrome_index,
        "syndrome_length_required_for_full_window": n - k,
        "prefix_minor_defined_by_syndrome_length": (
            prefix_max_syndrome_index < n - k
        ),
        "full_window_defined_by_syndrome_length": (
            full_hankel_max_syndrome_index < n - k
        ),
        "packet_outcome_needed": "nonzero minor with root table, or singular declaration",
    }


def build_plan(
    n: int = DEFAULT_N,
    k: int = DEFAULT_K,
    field: str = DEFAULT_FIELD,
    field_order: int = DEFAULT_FIELD_ORDER,
    epsilon_denominator: int = DEFAULT_EPSILON_DENOMINATOR,
    a_min: int | None = None,
    a_max: int | None = None,
) -> dict[str, Any]:
    reg_start = regular_start(n, k)
    tan_start = tangent_start(n, k)
    if a_min is None:
        a_min = reg_start
    if a_max is None:
        a_max = tan_start - 1
    if a_min > a_max:
        raise ValueError("empty agreement window")

    records = [agreement_record(a_value, n, k) for a_value in range(a_min, a_max + 1)]
    degree_bounds = [record["degree_bound"] for record in records]
    interpolation_evaluations = [
        record["interpolation_evaluations"] for record in records
    ]
    budget = field_order // epsilon_denominator
    all_regular = all(record["regular_overdetermined"] for record in records)
    all_prefix_defined = all(
        record["prefix_minor_defined_by_syndrome_length"] for record in records
    )
    all_full_defined = all(
        record["full_window_defined_by_syndrome_length"] for record in records
    )

    return {
        "schema_version": "regular-hankel-window-plan-v1",
        "status": "AUDIT",
        "row": {
            "field": field,
            "field_order": field_order,
            "n": n,
            "k": k,
            "domain_description": "multiplicative subgroup H with |H|=512",
            "domain_hash": DEFAULT_DOMAIN_HASH,
            "row_descriptor_ref": DEFAULT_ROW_DESCRIPTOR_REF,
            "syndrome_length": n - k,
        },
        "window": {
            "A_min": a_min,
            "A_max": a_max,
            "agreements": len(records),
            "regular_start": reg_start,
            "tangent_exact_start": tan_start,
            "reason": "regular overdetermined but below tangent exactness",
        },
        "conditions": {
            "regular_overdetermined": "t=A-k >= j+1=n-A+1",
            "regular_start_formula": "ceil((n+k+1)/2)",
            "tangent_exact_start_formula": "n-floor((n-k)/3)",
            "prefix_minor": "rows 0..j, columns 0..j of H_t,j(u)+Z H_t,j(v)",
        },
        "budget_context": {
            "epsilon": "2^-128",
            "line_denominator": field_order,
            "budget_numerator": budget,
            "degree_bound_min": min(degree_bounds),
            "degree_bound_max": max(degree_bounds),
            "degree_bound_sum": sum(degree_bounds),
            "degree_only_closes_safe_side": sum(degree_bounds) <= budget,
            "interpretation": (
                "degree bounds alone are far above the finite-slope budget; "
                "the useful object is the actual root table or a singular bucket"
            ),
        },
        "summary": {
            "all_regular_overdetermined": all_regular,
            "all_prefix_minors_defined_by_syndrome_length": all_prefix_defined,
            "all_full_hankel_windows_defined_by_syndrome_length": all_full_defined,
            "minor_size_min": min(record["minor_size"] for record in records),
            "minor_size_max": max(record["minor_size"] for record in records),
            "total_interpolation_evaluations": sum(interpolation_evaluations),
            "max_prefix_syndrome_index": max(
                record["prefix_max_syndrome_index"] for record in records
            ),
            "max_full_hankel_syndrome_index": max(
                record["full_hankel_max_syndrome_index"] for record in records
            ),
        },
        "adapter_contract": [
            "supply syndrome vectors u,v of length n-k over F_17^32",
            "supply deterministic F_17^32 addition, multiplication, inversion, and determinant arithmetic",
            "supply at least degree_bound+1 distinct finite slopes for interpolation at each A",
            "emit a v9 aperiodic-hankel-eliminant packet with removed tangent and quotient ledgers",
            "for every A, record a nonzero minor root table or declare the first singular bucket",
        ],
        "per_agreement": records,
        "nonclaims": [
            "does not compute any F_17^32 determinant",
            "does not enumerate roots in the prize field",
            "does not prove a safe-side MCA bound",
            "does not classify singular buckets",
        ],
    }


def render(plan: dict[str, Any]) -> str:
    return json.dumps(plan, indent=2, sort_keys=True) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_plan(path: Path) -> None:
    expected = render(build_plan())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"regular-window plan mismatch: {path}")


def print_summary(plan: dict[str, Any]) -> None:
    row = plan["row"]
    window = plan["window"]
    summary = plan["summary"]
    budget = plan["budget_context"]
    print("F_17^32 regular Hankel-window plan")
    print(
        "row: {field}, n={n}, k={k}, syndrome_length={syndrome_length}".format(
            **row
        )
    )
    print(
        "window: A={A_min}..{A_max} ({agreements} agreements), "
        "regular_start={regular_start}, tangent_start={tangent_exact_start}".format(
            **window
        )
    )
    print(
        "minor sizes: {minor_size_min}..{minor_size_max}; "
        "total interpolation evaluations={total_interpolation_evaluations}".format(
            **summary
        )
    )
    print(
        "budget numerator={budget_numerator}; degree-bound sum={degree_bound_sum}; "
        "degree-only closes={degree_only_closes_safe_side}".format(**budget)
    )
    print("next: supply F_17^32 row data and compute root/singularity outcomes")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic plan JSON")
    parser.add_argument("--check", type=Path, help="check deterministic plan JSON")
    parser.add_argument("--json", action="store_true", help="print plan JSON")
    args = parser.parse_args()

    plan = build_plan()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(plan), encoding="utf-8")
    if args.check:
        check_plan(args.check)
    if args.json:
        print(render(plan), end="")
        return
    print_summary(plan)


if __name__ == "__main__":
    main()
