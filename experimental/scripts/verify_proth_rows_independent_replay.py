#!/usr/bin/env python3
"""E-2: independent replay of the four certified Proth prime rows.

Serves submission-package item (3) of proximity_prize_results_v4.tex — "a
reproducibility dossier containing literal row manifests, primality certificates,
source pins, exact replays". The theorem and the certificate are the maintainer's;
this script only CONFIRMS them from the literal integers, re-deriving every
quantity from p, n, k rather than reading it out of the JSON.

Independent means: nothing is taken from the certificate except p, n, k, s, u and
the Proth witness. B, B*, F_{n,k}, r_quad, the sign conditions, the endpoint
verdict and the compiler-window hypothesis are all recomputed and only then
compared against the packet's recorded values.

Checks per row:
  PC1  Proth: p = u*2^s + 1, u odd, u < 2^s, a0^((p-1)/2) = -1 (mod p)  => p prime
  PC2  n | p-1,  p < 2^256,  B*2^128 <= p < (B+1)*2^128
  B    B = floor(p/2^128) = B*  (full-field affine sampler, |Gamma| = |F_p| = p)
  SGN  F_{n,k}(B-1) >= 0 > F_{n,k}(B) with F_{n,k}(r) = r^2 - 3nr + n(n-k)
  RQ   r_quad = B-1 located by SGN
  CAV  the packet's recorded caveat: the naive closed form
       floor((3n - isqrt(n(5n+4k)))/2) OVERSHOOTS r_quad by one at rho in
       {1/2,1/4,1/8} and is correct only at 1/16.  Reproduced here as a check on
       the caveat itself, since a replay that silently used the closed form would
       certify three wrong rows.
  CW   compiler window 1 <= B <= min(r_rho+1, n-k-1)

Stdlib only, exact integers, no floats.
"""

from __future__ import annotations

import json
import sys
from math import isqrt
from pathlib import Path

CERT = (Path(__file__).resolve().parent.parent / "data" / "certificates" /
        "proth-rows" / "proth_rows.json")
TWO128 = 1 << 128
TWO256 = 1 << 256

errors: list[str] = []


def check(c: bool, m: str) -> None:
    if not c:
        errors.append(m)


def F(r: int, n: int, k: int) -> int:
    return r * r - 3 * n * r + n * (n - k)


def r_quad_by_sign(n: int, k: int, B: int) -> bool:
    """The paper's method: F is decreasing on [0,n], so F(B-1) >= 0 > F(B) locates
    the smaller root in (B-1, B], giving r_quad = B-1."""
    return F(B - 1, n, k) >= 0 > F(B, n, k)


def r_quad_naive(n: int, k: int) -> int:
    return (3 * n - isqrt(n * (5 * n + 4 * k))) // 2


def main() -> int:
    cert = json.loads(CERT.read_text())
    rows = cert["rows"]
    check(len(rows) == 4, f"expected four rows, found {len(rows)}")
    overshoot = {}

    for row in rows:
        rate, n, k = row["rate"], row["n"], row["k"]
        p, s, u, a0 = int(row["p"]), row["proth_s"], int(row["proth_u"]), row["proth_witness_a0"]
        tag = f"row {rate}"

        # --- PC1: Proth primality, recomputed -----------------------------
        check(p == u * 2**s + 1, f"{tag}: p != u*2^s + 1")
        check(u % 2 == 1, f"{tag}: u must be odd (else 2^s is not the exact 2-part)")
        check(u < 2**s, f"{tag}: Proth needs u < 2^s")
        check(pow(a0, (p - 1) // 2, p) == p - 1,
              f"{tag}: Proth witness fails, a0^((p-1)/2) != -1 mod p")

        # --- PC2: field arithmetic ----------------------------------------
        check((p - 1) % n == 0, f"{tag}: n does not divide p-1")
        check(p < TWO256, f"{tag}: p >= 2^256")
        B = p // TWO128
        check(B * TWO128 <= p < (B + 1) * TWO128, f"{tag}: B does not bracket p")
        check(B == row["B"], f"{tag}: recomputed B {B} != recorded {row['B']}")
        check(B == row["B_star"], f"{tag}: B != B* (full-field sampler identification)")
        check(0 < p - B * TWO128 < TWO128, f"{tag}: remainder outside (0, 2^128)")

        # --- SGN / RQ: the sign-condition location ------------------------
        check(r_quad_by_sign(n, k, B), f"{tag}: sign condition F(B-1) >= 0 > F(B) fails")
        check(F(B - 1, n, k) == int(row["F_B_minus_1"]), f"{tag}: F(B-1) drift")
        check(F(B, n, k) == int(row["F_B"]), f"{tag}: F(B) drift")
        check(B - 1 == row["r_quad"], f"{tag}: r_quad != B-1")

        # --- CAV: reproduce the recorded closed-form caveat ---------------
        naive = r_quad_naive(n, k)
        overshoot[rate] = naive - (B - 1)

        # --- CW: compiler window hypothesis -------------------------------
        bound = min((B - 1) + 1, n - k - 1)
        check(1 <= B <= bound, f"{tag}: compiler window 1 <= B <= min(r_rho+1, n-k-1) fails")
        check(n - k - 1 == row["n_minus_k_minus_1"], f"{tag}: n-k-1 drift")

    # The caveat is load-bearing: a replay using the closed form would certify
    # three of the four rows at the wrong radius.  Confirm it exactly.
    check(overshoot == {"1/2": 1, "1/4": 1, "1/8": 1, "1/16": 0},
          f"recorded closed-form caveat not reproduced: overshoots = {overshoot}")

    if errors:
        for e in errors:
            print("FAIL:", e)
        return 1

    print(
        "PROTH_ROWS_INDEPENDENT_REPLAY_PASS rows=4 "
        "proth=ok field_arithmetic=ok B_equals_Bstar=ok "
        "sign_condition=ok r_quad=B-1 compiler_window=ok "
        "closed_form_overshoot={1/2:1, 1/4:1, 1/8:1, 1/16:0} (caveat reproduced)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
