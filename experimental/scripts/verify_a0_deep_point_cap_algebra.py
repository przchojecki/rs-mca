#!/usr/bin/env python3
"""Verify the A0 deep-point cap algebra with exact rational arithmetic."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from typing import Any


def ceil_div(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def cap_bound(q: int, n: int, k: int) -> Fraction:
    return Fraction(q - n, 2 * k * q)


def deep_point_density(q: int, n: int, k: int, list_size: int) -> Fraction:
    omega = q - n
    return Fraction(list_size * omega, q * (omega + k * (list_size - 1)))


def certificate(q: int, n: int, k: int, list_size: int) -> dict[str, Any]:
    if not (q > n > 0 and k > 0 and list_size > 0):
        raise ValueError("expected q>n>0, k>0, and list_size>0")

    fiber_hypothesis = k * list_size >= q + k
    residual = k * list_size - q + n + k
    deep_density = deep_point_density(q, n, k, list_size)
    target = cap_bound(q, n, k)
    weak_inequality_holds = deep_density >= target
    strict_inequality_holds = deep_density > target

    if fiber_hypothesis and residual <= 0:
        raise AssertionError("fiber hypothesis should force a positive residual")
    if (residual >= 0) != weak_inequality_holds:
        raise AssertionError("residual sign does not match weak density comparison")
    if (residual > 0) != strict_inequality_holds:
        raise AssertionError("residual sign does not match strict density comparison")

    return {
        "q": q,
        "n": n,
        "k": k,
        "list_size": list_size,
        "fiber_hypothesis_kL_ge_q_plus_k": fiber_hypothesis,
        "residual_kL_minus_q_plus_n_plus_k": residual,
        "deep_density_num": deep_density.numerator,
        "deep_density_den": deep_density.denominator,
        "cap_bound_num": target.numerator,
        "cap_bound_den": target.denominator,
        "deep_density_ge_cap_bound": weak_inequality_holds,
        "deep_density_gt_cap_bound": strict_inequality_holds,
    }


def grid_certificates() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for q in range(7, 80):
        for n in range(2, q):
            for k in range(1, n + 1):
                min_list_size = ceil_div(q + k, k)
                for list_size in (min_list_size, min_list_size + 1):
                    row = certificate(q, n, k, list_size)
                    if not row["fiber_hypothesis_kL_ge_q_plus_k"]:
                        raise AssertionError("chosen list size should meet fiber hypothesis")
                    if not row["deep_density_gt_cap_bound"]:
                        raise AssertionError("deep-point route failed the cap bound")
                    rows.append(row)
    return rows


def boundary_examples() -> list[dict[str, Any]]:
    examples = [
        {"label": "small_boundary", "q": 17, "n": 16, "k": 4},
        {"label": "medium_half_rate", "q": 257, "n": 128, "k": 64},
        {"label": "large_symbolic_scale", "q": 2**64, "n": 2**21, "k": 2**20},
    ]
    rows = []
    for item in examples:
        q = int(item["q"])
        n = int(item["n"])
        k = int(item["k"])
        list_size = ceil_div(q + k, k)
        row = certificate(q, n, k, list_size)
        row["label"] = item["label"]
        rows.append(row)
    return rows


def run() -> dict[str, Any]:
    grid = grid_certificates()
    examples = boundary_examples()
    return {
        "status": "PASS",
        "claim": (
            "L >= q/k+1 and M >= L/(1+k(L-1)/(q-n)) imply "
            "M/q > (1/(2k))(1-n/q)"
        ),
        "grid_case_count": len(grid),
        "grid_min_residual": min(
            row["residual_kL_minus_q_plus_n_plus_k"] for row in grid
        ),
        "boundary_examples": examples,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    print("a0_deep_point_cap_algebra: PASS")
    print(result["claim"])
    print(f"grid cases checked: {result['grid_case_count']}")
    print(f"minimum residual kL-q+n+k on grid: {result['grid_min_residual']}")
    for row in result["boundary_examples"]:
        print(
            "{label}: q={q} n={n} k={k} L={list_size} residual={residual} "
            "deep>cap={ok}".format(
                label=row["label"],
                q=row["q"],
                n=row["n"],
                k=row["k"],
                list_size=row["list_size"],
                residual=row["residual_kL_minus_q_plus_n_plus_k"],
                ok=row["deep_density_gt_cap_bound"],
            )
        )


if __name__ == "__main__":
    main()
