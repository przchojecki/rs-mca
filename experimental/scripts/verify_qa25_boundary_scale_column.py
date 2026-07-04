#!/usr/bin/env python3
"""QA.25 verifier: boundary-scale zero-sum column arithmetic.

This is the arithmetic repair prompted by the X-8 boundary-scale construction.
QA.22 prices the strict quotient staircase at dyadic scales M > t.  X-8 shows
that the first lower boundary scale also has a chargeable zero-sum quotient
column: choose primitive antipodal-free quotient patterns and require their
quotient value sum to vanish.

The official rows often have non-dyadic t.  Since the multiplicative domains in
the campaign are 2-power rows, the verifier records the dyadic boundary
predecessor

    M0 = 2^floor(log2 t),        M0 <= t < 2 M0,

and labels exact literal M=t realizability separately.  The count is the
row-shape envelope used by the X-8 repair node; it does not assert that a
non-2-power t is itself a subgroup of mu_n.

For quotient length R = n/M0 and e = floor(t/M0), the primitive boundary pattern
counting model is

    boundary_mass ~= 2^(R/2) / q^e,

with q_min = B* 2^128 the conservative smallest field size compatible with the
row's B*.  The verifier carries both floor and ceil exact integer columns and
uses the ceil column for budget checks.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
QA22_CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qa22-staircase-budget",
    "qa22_staircase_budget.json",
)
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qa25-boundary-scale-column",
    "qa25_boundary_scale_column.json",
)

FAILS: list[str] = []
NCHECK = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"   ({detail})"
    print(line)
    if not cond:
        FAILS.append(name)


def ceil_div(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("ceil_div denominator must be positive")
    return (a + b - 1) // b


def ceil_root(x: int, r: int) -> int:
    """ceil(x ** (1/r)) for nonnegative integers."""
    if x < 0 or r <= 0:
        raise ValueError("bad root input")
    if x <= 1:
        return x
    lo, hi = 0, 1
    while hi**r < x:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**r < x:
            lo = mid
        else:
            hi = mid
    return hi


def log2_big(x: int | None) -> float | None:
    if x is None or x <= 0:
        return None
    bits = x.bit_length()
    if bits <= 53:
        return math.log2(x)
    return bits - 53 + math.log2(x >> (bits - 53))


def log2_str(x: int | None) -> str:
    val = log2_big(x)
    return "n/a" if val is None else f"{val:.4f}"


def prev_power_two(x: int) -> int:
    if x < 1:
        raise ValueError("positive input required")
    return 1 << (x.bit_length() - 1)


def boundary_crossover_bstar(raw_patterns: int, equations: int) -> int:
    """Smallest integer B* for which ceil(raw / (B* 2^128)^e) <= B*.

    This is exact.  The inequality is equivalent to

        raw <= B*^(e+1) 2^(128e).
    """
    scaled = ceil_div(raw_patterns, 1 << (128 * equations))
    return max(1, ceil_root(scaled, equations + 1))


def boundary_row(row: dict[str, Any]) -> dict[str, Any]:
    label = str(row["label"])
    rate = str(row["rate"])
    n = int(row["n"])
    t = int(row["t"])
    bstar = int(row["B_star"])
    q_min = bstar << 128
    m0 = prev_power_two(t)
    r = n // m0
    equations = max(1, t // m0)
    raw_antipodal = 1 << (r // 2)
    raw_all_quotient_subsets = 1 << r
    denom = q_min**equations
    mass_floor = raw_antipodal // denom
    mass_ceil = ceil_div(raw_antipodal, denom)
    full_floor = raw_all_quotient_subsets // denom
    full_ceil = ceil_div(raw_all_quotient_subsets, denom)
    bstar_cross = boundary_crossover_bstar(raw_antipodal, equations)
    q_cross_min = bstar_cross << 128
    old_total = int(row["budget_total"])
    repaired_total = old_total + mass_ceil
    rid = f"{label} {rate}"

    check(f"{rid}: boundary predecessor M0 divides n", n % m0 == 0, f"M0={m0}")
    check(f"{rid}: quotient length is even", r % 2 == 0, f"R={r}")
    check(
        f"{rid}: row is above the exact QA.25 crossover",
        bstar >= bstar_cross,
        f"log2 B*={log2_str(bstar)}, log2 B*_cross={log2_str(bstar_cross)}",
    )
    check(
        f"{rid}: boundary ceil mass fits B*",
        mass_ceil <= bstar,
        f"log2 mass={log2_str(mass_ceil)}, log2 B*={log2_str(bstar)}",
    )
    check(
        f"{rid}: QA.22 total plus boundary column still fits B*",
        repaired_total <= bstar,
        f"log2 repaired={log2_str(repaired_total)}, log2 B*={log2_str(bstar)}",
    )

    return {
        "label": label,
        "rate": rate,
        "n": n,
        "k": int(row["k"]),
        "A": int(row["A"]),
        "t": t,
        "B_star": bstar,
        "q_min_from_B_star": q_min,
        "boundary_M0": m0,
        "literal_M_equals_t": m0 == t,
        "quotient_R_n_over_M0": r,
        "zero_sum_equations_e_floor_t_over_M0": equations,
        "raw_antipodal_free_patterns_2_to_R_over_2": raw_antipodal,
        "raw_all_quotient_subsets_2_to_R_diagnostic": raw_all_quotient_subsets,
        "boundary_mass_floor": mass_floor,
        "boundary_mass_ceil_budgeted": mass_ceil,
        "diagnostic_full_subset_mass_floor": full_floor,
        "diagnostic_full_subset_mass_ceil": full_ceil,
        "B_star_crossover": bstar_cross,
        "q_min_crossover": q_cross_min,
        "log2_boundary_mass_ceil": log2_big(mass_ceil),
        "log2_B_star_crossover": log2_big(bstar_cross),
        "log2_q_min_crossover": log2_big(q_cross_min),
        "log2_q_min_margin_above_crossover": (
            log2_big(q_min) - log2_big(q_cross_min)
            if q_min > 0 and q_cross_min > 0
            else None
        ),
        "qa22_budget_total": old_total,
        "repaired_budget_total": repaired_total,
        "repaired_budget_ok": repaired_total <= bstar,
    }


def load_qa22() -> dict[str, Any]:
    with open(QA22_CERT, encoding="utf-8") as fh:
        return json.load(fh)


def build_certificate() -> dict[str, Any]:
    qa22 = load_qa22()
    check("QA.22 source certificate has six rows", len(qa22["rows"]) == 6)
    rows = [boundary_row(row) for row in qa22["rows"]]
    check(
        "all six campaign candidates pass after adding QA.25 boundary column",
        all(row["repaired_budget_ok"] for row in rows),
    )
    return {
        "task": "QA.25 boundary-scale zero-sum column",
        "node": "u2c_boundary_scale_column",
        "source": "qa22_staircase_budget.json",
        "status": "PASS: exact crossover arithmetic; all six campaign candidates fit after adding the boundary column",
        "convention": {
            "boundary_scale": "M0 = largest 2-power <= t, with literal M=t flagged separately",
            "primitive_counting_model": "antipodal-free quotient patterns: ceil(2^(R/2) / q_min^e)",
            "R": "n/M0",
            "e": "floor(t/M0); equals 1 on all six campaign rows",
            "q_min": "B* * 2^128, the conservative smallest q compatible with B*",
            "crossover": "smallest B* with ceil(2^(R/2)/(B* 2^128)^e) <= B*",
            "diagnostic_full_subset_column": "2^R/q_min^e is emitted but not budgeted; it is the unstripped quotient subset count, not the primitive boundary column",
        },
        "checks": NCHECK,
        "rows": rows,
    }


def main() -> int:
    write = "--write-certificate" in sys.argv
    cert = build_certificate()
    if write:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[write] {CERT}")

    expected = None
    if os.path.exists(CERT):
        with open(CERT, encoding="utf-8") as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", cert == expected)

    print("\nrow summary:")
    for row in cert["rows"]:
        literal = "literal" if row["literal_M_equals_t"] else "dyadic-proxy"
        print(
            f"{row['label']:5s} {row['rate']:>4s} "
            f"M0={row['boundary_M0']:<12d} R={row['quotient_R_n_over_M0']:<4d} "
            f"{literal:12s} "
            f"log2(boundary ceil)={log2_str(row['boundary_mass_ceil_budgeted']):>8s} "
            f"log2(B*_cross)={log2_str(row['B_star_crossover']):>8s} "
            f"q-margin={row['log2_q_min_margin_above_crossover']:.4f} bits "
            f"log2(repaired total)={log2_str(row['repaired_budget_total']):>9s}"
        )

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print("  -", name)
        print("\nrecomputed summary:")
        print(json.dumps(cert, indent=2, sort_keys=True))
        return 1

    print(f"\nPASS: {NCHECK} QA.25 boundary-column arithmetic checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
