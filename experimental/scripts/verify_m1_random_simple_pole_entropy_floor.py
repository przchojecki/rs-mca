#!/usr/bin/env python3
r"""
Verify the exact integer arithmetic for the M1 random simple-pole entropy
floor over the row

    F = F_17[z]/(z^32 - 3),  |H| = 512,  k = 256.

The proof note gives the general lower bound

    M_a = ceil(q C_a / (C_a + R_a q^(a-k))),

where q=17^32, C_a=binom(512,a), and

    R_a = sum_{v=0}^{a-k-1} binom(a,v) binom(512-a,v) / q^v.

This script computes the integer form exactly:

    D_a = R_a q^(a-k)
        = sum_v binom(a,v) binom(512-a,v) q^(a-k-v),
    M_a = ceil(q C_a / (C_a + D_a)).

Run:
    python3 experimental/scripts/verify_m1_random_simple_pole_entropy_floor.py
    python3 experimental/scripts/verify_m1_random_simple_pole_entropy_floor.py --json
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any

N = 512
K = 256
Q = 17**32
TWO128 = 2**128
CERTIFICATE = Path("experimental/data/m1_random_simple_pole_entropy_floor.json")

EXPECTED = {
    257: Q,
    258: Q,
    259: Q - 68_904,
    260: 33_439_260_151_101_646_297_506_087_371_119_470,
    # These two rows are included to document where this second-moment method
    # stops being numerically useful.
    261: 1,
    262: 1,
}


def ceil_div(num: int, den: int) -> int:
    return -(-num // den)


def lower_bound(a: int) -> tuple[int, int, int, int]:
    """Return (M_a, C_a, D_a, denominator) for the specialized row."""
    c_a = comb(N, a)
    s = a - K
    d_a = 0
    for v in range(a - K):
        d_a += comb(a, v) * comb(N - a, v) * Q ** (s - v)

    denominator = c_a + d_a
    m_a = ceil_div(Q * c_a, denominator)
    return m_a, c_a, d_a, denominator


def computed_certificate() -> dict[str, Any]:
    records = []
    for agreement in [257, 258, 259, 260]:
        lower, _c_a, _d_a, _den = lower_bound(agreement)
        if lower == Q:
            display = "17^32"
        elif agreement == 259:
            display = "17^32 - 68904"
        else:
            display = str(lower)

        record: dict[str, Any] = {
            "agreement": agreement,
            "badSlopesLower": display,
            "badSlopesLowerExact": str(lower),
            "missingFiniteSlopes": str(Q - lower),
        }
        if agreement == 260:
            record["gt"] = "2^114"
        records.append(record)

    stop_checks = []
    for agreement in [261, 262]:
        lower, _c_a, _d_a, _den = lower_bound(agreement)
        stop_checks.append({
            "agreement": agreement,
            "badSlopesLowerExact": str(lower),
        })

    return {
        "status": "PROVED / FINITE-SLOPE LOWER-BOUND / AUDIT",
        "row": "RS[F_17^32,H,256]",
        "field": "F_17[z]/(z^32 - 3)",
        "domain": "H=<z>, |H|=512",
        "predicate": "finite-slope support-wise LD/MCA",
        "q": "17^32",
        "qExact": str(Q),
        "n": N,
        "k": K,
        "degreeConvention": "base code deg < k; numerator deg <= k",
        "records": records,
        "methodStopChecks": stop_checks,
        "denominatorCheck": {
            "floor(q/2^128)": Q // TWO128,
        },
        "nonclaims": [
            "not a safe-side bound",
            "not ordinary list decoding",
            "not interleaved list size",
            "not protocol soundness",
            "finite slopes only",
            "separate existence statements",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = computed_certificate()
    actual = json.loads(path.read_text(encoding="utf-8"))
    assert actual == expected, f"certificate mismatch: {path}"


def print_human_summary() -> None:
    print("q =", Q)
    print("floor(q/2^128) =", Q // TWO128)
    print()

    for a in sorted(EXPECTED):
        m_a, c_a, d_a, denominator = lower_bound(a)
        assert m_a == EXPECTED[a], (a, m_a, EXPECTED[a])

        print(f"a={a}")
        print("  C_a =", c_a)
        print("  D_a =", d_a)
        print("  denominator =", denominator)
        print("  lower =", m_a)
        print("  missing =", Q - m_a)
        print("  floor_log2_lower =", m_a.bit_length() - 1)

    assert EXPECTED[257] == Q
    assert EXPECTED[258] == Q
    assert EXPECTED[259] == Q - 68_904
    assert EXPECTED[260] > 2**114
    assert Q // TWO128 == 6
    assert 6 * TWO128 < Q < 7 * TWO128
    check_certificate(CERTIFICATE)

    print()
    print("random simple-pole entropy floor checks passed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the computed certificate JSON after checking it",
    )
    args = parser.parse_args()

    if args.json:
        check_certificate(CERTIFICATE)
        print(json.dumps(computed_certificate(), indent=2, sort_keys=False))
    else:
        print_human_summary()


if __name__ == "__main__":
    main()
