#!/usr/bin/env python3
"""QA.22 verifier: staircase budget column at the clean-rate candidates.

This is exact arithmetic for the six rows in xr_budget_audit.md.  It prices
the X-4 quotient-coset staircase term

    C(n/M - 1, floor(A/M)),       M | n, M > t=A-k,

with the X-4 convention that the tail B is fixed.  It also carries the
Chebyshev/dihedral fixed-tail analogue on the quotient row.  The unsupported
variant that chooses arbitrary tails inside a size-M coset is intentionally not
used here; it is not the X-4 term and it can be enormous.

Exit 0 iff every checked budget inequality passes and the pinned certificate
matches the recomputed summary.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Any


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "qa22-staircase-budget",
    "qa22_staircase_budget.json",
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


def iroot(x: int, r: int) -> int:
    if x < 0 or r <= 0:
        raise ValueError("bad root input")
    lo, hi = 0, 1
    while hi**r <= x:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**r <= x:
            lo = mid
        else:
            hi = mid
    return lo


def log2_big(x: int | None) -> float | None:
    if x is None:
        return None
    if x <= 0:
        return None
    bits = x.bit_length()
    if bits <= 53:
        return math.log2(x)
    return bits - 53 + math.log2(x >> (bits - 53))


def log2_str(x: int | None) -> str:
    val = log2_big(x)
    return "n/a" if val is None else f"{val:.4f}"


def comb(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    return math.comb(n, k)


def powers_of_two_dividing(n: int) -> list[int]:
    out = []
    m = 1
    while m <= n:
        if n % m == 0:
            out.append(m)
        m *= 2
    return out


def quotient_staircase_term(n: int, A: int, M: int) -> dict[str, Any]:
    """X-4 fixed-tail quotient staircase term."""
    N = n // M
    h, b = divmod(A, M)
    term = comb(N - 1, h)
    return {
        "M": M,
        "quotient_n": N,
        "h_floor_A_over_M": h,
        "tail_b": b,
        "form": "b=0" if b == 0 else "b>0",
        "term": term,
        "log2_term": log2_big(term),
    }


def inversion_subsets_with_fixed_tail(N: int, h: int, b: int) -> int:
    """Chebyshev analogue of the fixed-tail staircase term.

    On a cyclic quotient row of even length N, inversion has two fixed points
    and (N-2)/2 moving pairs.

    * b = 0: no tail is removed; count all inversion-closed h-subsets.
    * b > 0: the staircase tail is pinned at one fixed quotient cell; count
      inversion-closed h-subsets of the remaining cells.

    This is the exact fixed-tail analogue, not multiplied by tail choices.
    """
    if N == 1:
        return 1 if h == 0 else 0
    if N % 2:
        raise ValueError("dihedral quotient length should be even in these rows")
    pairs = (N - 2) // 2
    fixed_available = 2 if b == 0 else 1
    total = 0
    for f in range(fixed_available + 1):
        rem = h - f
        if rem >= 0 and rem % 2 == 0:
            total += comb(fixed_available, f) * comb(pairs, rem // 2)
    return total


def row_terms(label: str, n: int, rate_den: int, A: int, bstar: int) -> dict[str, Any]:
    k = n // rate_den
    t = A - k
    terms = []
    transported = []
    for M in powers_of_two_dividing(n):
        if M <= t:
            continue
        qterm = quotient_staircase_term(n, A, M)
        dterm = inversion_subsets_with_fixed_tail(qterm["quotient_n"], qterm["h_floor_A_over_M"], qterm["tail_b"])
        term = {
            **qterm,
            "quotient_term_log2": log2_big(qterm["term"]),
            "dihedral_fixed_tail_term": dterm,
            "dihedral_fixed_tail_log2": log2_big(dterm),
        }
        terms.append(term)
        transported.append(
            {
                "M": M,
                "scale_n_over_M": qterm["quotient_n"],
                "quotient_k_floor": k // M,
                "quotient_A_floor": qterm["h_floor_A_over_M"],
                "tail_b": qterm["tail_b"],
                "term": qterm["term"],
                "dihedral_fixed_tail_term": dterm,
            }
        )

    qsum = sum(term["term"] for term in terms)
    dsum = sum(term["dihedral_fixed_tail_term"] for term in terms)
    staircase = qsum + dsum
    qmax = max((term["term"] for term in terms), default=0)
    dmax = max((term["dihedral_fixed_tail_term"] for term in terms), default=0)
    b_tan_max = n - A + 1
    poly = 16 * n**3
    total = staircase + b_tan_max + poly
    residual_after_poly_tan = bstar - b_tan_max - poly
    margin_total_bits = log2_big(bstar) - log2_big(total) if total > 0 else None
    staircase_room_bits = (
        log2_big(residual_after_poly_tan) - log2_big(staircase)
        if residual_after_poly_tan > 0 and staircase > 0
        else None
    )

    tag = f"{label} 1/{rate_den}"
    check(f"{tag}: has admissible staircase scales M|n, M>t", bool(terms), f"count={len(terms)}")
    check(
        f"{tag}: X-4 staircase + B_tan_max + 16n^3 <= B*",
        total <= bstar,
        f"log2 total={log2_str(total)}, log2 B*={log2_str(bstar)}, margin_bits={margin_total_bits:.4f}",
    )
    check(
        f"{tag}: staircase alone fits residual after B_tan_max and 16n^3",
        staircase <= residual_after_poly_tan,
        f"log2 staircase={log2_str(staircase)}, residual_room_bits={staircase_room_bits:.4f}",
    )
    check(f"{tag}: max staircase term <= staircase sum", qmax <= qsum and dmax <= dsum)

    return {
        "label": label,
        "rate": f"1/{rate_den}",
        "n": n,
        "k": k,
        "A": A,
        "t": t,
        "B_star": bstar,
        "B_tan_max": b_tan_max,
        "poly_16n3": poly,
        "quotient_staircase_sum": qsum,
        "quotient_staircase_max": qmax,
        "dihedral_fixed_tail_sum": dsum,
        "dihedral_fixed_tail_max": dmax,
        "staircase_total": staircase,
        "budget_total": total,
        "budget_ok": total <= bstar,
        "margin_total_bits": margin_total_bits,
        "staircase_room_after_poly_tan_bits": staircase_room_bits,
        "terms": terms,
        "transported_quotient_row_table": transported,
    }


B_STAR_ROWC = 1 << 122
B_STAR_PRIZE = iroot(1 << 1279, 10)
ROWS = [
    ("RowC", 1024, 4, 261, B_STAR_ROWC),
    ("RowC", 1024, 8, 133, B_STAR_ROWC),
    ("RowC", 1024, 16, 67, B_STAR_ROWC),
    ("prize", 1 << 41, 4, 558345748481, B_STAR_PRIZE),
    ("prize", 1 << 41, 8, 283467841537, B_STAR_PRIZE),
    ("prize", 1 << 41, 16, 141733920769, B_STAR_PRIZE),
]


def main() -> None:
    check(
        "prize B* is floor(2^127.9)",
        B_STAR_PRIZE**10 <= (1 << 1279) < (B_STAR_PRIZE + 1) ** 10,
        f"B*={B_STAR_PRIZE}",
    )
    rows = [row_terms(*row) for row in ROWS]
    result = {
        "node": "x4_exactlist_staircase_split",
        "task": "QA.22",
        "status": "PASS: staircase budget column fits all six clean-rate candidates",
        "formula": {
            "quotient": "sum_{M|n, M>t} C(n/M - 1, floor(A/M)) with fixed tail B",
            "dihedral_fixed_tail": "inversion-closed h-subsets on the quotient row, with no tail if b=0 and one fixed tail removed if b>0",
            "budget_check": "quotient + dihedral_fixed_tail + B_tan_max + 16*n^3 <= B*",
        },
        "checks": NCHECK,
        "rows": rows,
    }

    if "--write-certificate" in sys.argv:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w") as fh:
            json.dump(result, fh, indent=2, sort_keys=True)
            fh.write("\n")

    expected = None
    if os.path.exists(CERT):
        with open(CERT) as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", result == expected)

    print("\nrow summary:")
    for row in rows:
        print(
            f"{row['label']:5s} {row['rate']:>4s} A={row['A']:<13d} "
            f"log2(Qsum)={log2_str(row['quotient_staircase_sum']):>9s} "
            f"log2(Dsum)={log2_str(row['dihedral_fixed_tail_sum']):>9s} "
            f"log2(total)={log2_str(row['budget_total']):>9s} "
            f"margin={row['margin_total_bits']:.4f} bits "
            f"stair-room={row['staircase_room_after_poly_tan_bits']:.4f} bits"
        )

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print("  -", name)
        print("\nrecomputed summary:")
        print(json.dumps(result, indent=2, sort_keys=True))
        sys.exit(1)
    print(f"\nPASS: {NCHECK} QA.22 staircase budget checks")


if __name__ == "__main__":
    main()
