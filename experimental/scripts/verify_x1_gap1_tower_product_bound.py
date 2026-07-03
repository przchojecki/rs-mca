#!/usr/bin/env python3
"""Verifier for the GAP-1 intermediate-field tower product bound.

This is a finite sanity check for
experimental/notes/x1/x1_gap1_tower_product_bound.md.

Model:
  B = F_17
  F = B[alpha] / (alpha^4 - gamma)
  K = B(alpha^2), so alpha^2 is intermediate-field valued but not B-valued.

For period M=2, the two isotypic characters should map into one K-line each:
  r=0 -> K
  r=1 -> alpha*K

The verifier checks all small K_2-stable support choices in H_16 <= B^* and
confirms that the multi-character image rank is no larger than the sum of the
per-character ranks.
"""

from __future__ import annotations

import argparse
import itertools
import json

from verify_x1_gap1_nonequivariant_periodic_evidence import (
    BinomialField,
    binomial_irreducible,
    lagrange_eval_weights,
    primitive_root,
    rank_mod_p,
    subgroup,
)


def in_k_line(value: tuple[int, ...], twist: int) -> bool:
    """Check membership in alpha^twist * B(alpha^2) in the degree-4 basis."""

    if twist % 2 == 0:
        return value[1] == 0 and value[3] == 0
    return value[0] == 0 and value[2] == 0


def analyze_support(
    field: BinomialField,
    omega: int,
    p: int,
    n: int,
    period: int,
    cosets: tuple[int, ...],
    active_chars: tuple[int, ...],
) -> dict[str, object]:
    zeta = pow(omega, n // period, p)
    support: list[int] = []
    positions: list[tuple[int, int]] = []
    for coset in cosets:
        rep = pow(omega, coset, p)
        current = rep
        for j in range(period):
            support.append(current)
            positions.append((coset, j))
            current = (current * zeta) % p

    weights = lagrange_eval_weights(field, support, field.alpha)
    slopes_by_char: dict[int, list[tuple[int, ...]]] = {char: [] for char in active_chars}
    all_basis: list[tuple[int, ...]] = []
    line_membership_ok = True

    for coset in cosets:
        for char in active_chars:
            slope = field.zero
            for index, (point_coset, j) in enumerate(positions):
                if point_coset != coset:
                    continue
                scalar = pow(zeta, (j * char) % period, p)
                slope = field.add(slope, field.scale_base(weights[index], scalar))
            slopes_by_char[char].append(slope)
            all_basis.append(slope)
            if not in_k_line(slope, char):
                line_membership_ok = False

    per_char_rank = {
        str(char): rank_mod_p(slopes, p) for char, slopes in slopes_by_char.items()
    }
    product_rank = sum(per_char_rank.values())
    actual_rank = rank_mod_p(all_basis, p)
    return {
        "cosets": list(cosets),
        "active_chars": list(active_chars),
        "per_character_ranks": per_char_rank,
        "product_rank": product_rank,
        "actual_rank": actual_rank,
        "line_membership_ok": line_membership_ok,
        "product_bound_ok": actual_rank <= product_rank,
    }


def run() -> dict[str, object]:
    p = 17
    n = 16
    period = 2
    degree = 4
    gamma = primitive_root(p)
    if not binomial_irreducible(p, degree, gamma):
        raise ValueError("configured binomial extension was not irreducible")
    field = BinomialField(p, degree, gamma)
    omega, _ = subgroup(p, n)

    beta = field.pow(field.alpha, 2)
    beta_squared = field.pow(beta, 2)
    intermediate_checks = {
        "alpha^2_not_in_B": beta[1] != 0 or beta[2] != 0 or beta[3] != 0,
        "alpha^2_in_K_basis": beta[0] == 0 and beta[1] == 0 and beta[3] == 0,
        "alpha^4_in_B": beta_squared[1] == 0 and beta_squared[2] == 0 and beta_squared[3] == 0,
    }

    total_cosets = n // period
    active_sets = ((0,), (1,), (0, 1))
    rows: list[dict[str, object]] = []
    for count in range(1, 5):
        for cosets in itertools.combinations(range(total_cosets), count):
            for active_chars in active_sets:
                rows.append(analyze_support(field, omega, p, n, period, cosets, active_chars))

    all_line_ok = all(bool(row["line_membership_ok"]) for row in rows)
    all_product_ok = all(bool(row["product_bound_ok"]) for row in rows)
    max_actual_rank = max(int(row["actual_rank"]) for row in rows)
    max_product_rank = max(int(row["product_rank"]) for row in rows)
    return {
        "title": "X1 GAP-1 intermediate-field tower product verifier",
        "field_model": f"F_{p}[alpha]/(alpha^4-{gamma})",
        "intermediate_field": "K=F_17(alpha^2)",
        "period": period,
        "rows_checked": len(rows),
        "intermediate_checks": intermediate_checks,
        "all_line_membership_ok": all_line_ok,
        "all_product_bounds_ok": all_product_ok,
        "max_actual_rank": max_actual_rank,
        "max_product_rank": max_product_rank,
        "all_ok": all(intermediate_checks.values()) and all_line_ok and all_product_ok,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, sort_keys=True))
    else:
        print(out["title"])
        print(f"field: {out['field_model']}; {out['intermediate_field']}")
        print(f"rows checked: {out['rows_checked']}")
        print(f"max rank: actual={out['max_actual_rank']} product={out['max_product_rank']}")
        for key, value in out["intermediate_checks"].items():
            print(f"  [{'OK ' if value else 'FAIL'}] {key}")
        print(f"  [{'OK ' if out['all_line_membership_ok'] else 'FAIL'}] character images land in K-lines")
        print(f"  [{'OK ' if out['all_product_bounds_ok'] else 'FAIL'}] multi-character rank <= product rank")
        print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
