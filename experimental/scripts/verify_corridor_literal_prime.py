#!/usr/bin/env python3
"""E-1: a literal admissible corridor prime, and the six-row replay at that prime.

Fills the printed TODO in proximity_prize_results_v4.tex (remark after
thm:corridor): "The prize-scale corridor packet uses a pinned exact budget
convention corresponding to a line field near 2^255.9; it does not yet pin one
literal prime in the paper. ... A final row release should add a literal
admissible field and rerun the same exact comparisons."

The corridor safe edges depend on q ONLY through B* = floor(q/2^128), so pinning a
literal prime with the packet's printed B* makes every printed radius replay
digit-exactly.  That is the content of this file.

Stdlib only, exact integers, no floats in any verdict.
"""

from __future__ import annotations

import math
import sys

# --- the literal prime ----------------------------------------------------
P_AUX = 309485010219174763933204481                 # = 8796093033515 * 2^45 + 1
D_AUX, J_AUX = 8796093033515, 45
Q = 108037839417390090843359763492907651258221714407500997496797919767622829735937
S_MULT = 158747337183671499011314909792715251078

# --- printed values being reproduced (v4 tab:corridor / the #275 packet) ---
PRINTED_R = {"prize-1/4": 1092724518963, "prize-1/8": 1415997755216,
             "prize-1/16": 1644686143216}
PRINTED_M = {"prize-1/4": 81, "prize-1/8": 70, "prize-1/16": 60}
PRINTED_GKL = {"prize-1/4": 813725411113, "prize-1/8": 1099511627777,
               "prize-1/16": 1326340298262}
ROWS = [("prize-1/4", 2**41, 2**39), ("prize-1/8", 2**41, 2**38),
        ("prize-1/16", 2**41, 2**37)]

errors: list[str] = []


def check(c: bool, m: str) -> None:
    if not c:
        errors.append(m)


def iroot(n: int, k: int) -> int:
    x = 1 << ((n.bit_length() + k - 1) // k + 1)
    while True:
        y = ((k - 1) * x + n // x ** (k - 1)) // k
        if y >= x:
            return x
        x = y


BSTAR = iroot(2**1279, 10)
check(BSTAR**10 <= 2**1279 < (BSTAR + 1) ** 10, "B* is not the integer 10th root of 2^1279")
check(BSTAR == 317494674775468773183020924238786383963, "B* drift vs the upstream pin")

# --- 1. the auxiliary Proth prime P ---------------------------------------
check(P_AUX == D_AUX * 2**J_AUX + 1, "P is not of the stated Proth form")
check(D_AUX % 2 == 1, "d must be odd so 2^45 is the exact 2-part of P-1")
check(D_AUX < 2**J_AUX, "Proth's theorem needs d < 2^j")
check((2**J_AUX) ** 2 > P_AUX, "F_P = 2^j must exceed sqrt(P)")
proth_base = next((a for a in (3, 5, 7, 11, 13)
                   if pow(a, (P_AUX - 1) // 2, P_AUX) == P_AUX - 1), None)
check(proth_base is not None, "no Proth witness for P")

# --- 2. the corridor prime q ----------------------------------------------
check(Q == 2**41 * P_AUX * S_MULT + 1, "q does not match its stated factorisation")
check(Q < 2**256, "q must be below 2^256")
check(Q.bit_length() == 256, "q must be a 256-bit integer")
check((Q - 1) % 2**41 == 0, "2^41 must divide q-1 (order-2^41 evaluation domain)")
check(Q >> 128 == BSTAR, "floor(q/2^128) must equal the printed budget B*")

F = 2**41 * P_AUX                                    # certified factored part
check(F * F > Q, "Pocklington needs F^2 > q")
poc_base = None
for a in (2, 3, 5, 7, 11, 13, 17, 19, 23):
    if pow(a, Q - 1, Q) != 1:
        continue
    if math.gcd(pow(a, (Q - 1) // 2, Q) - 1, Q) == 1 and \
       math.gcd(pow(a, (Q - 1) // P_AUX, Q) - 1, Q) == 1:
        poc_base = a
        break
check(poc_base is not None, "no Pocklington witness for q")

# --- 3. the six-row replay at the literal prime ---------------------------
def budget_ok(m, n, k, B):
    return (2 * m + 1) ** 14 * n**7 <= 9 * 2**14 * (k - 1) ** 3 * B * B


def admitted(r, m, n, k):
    return (2 * m + 1) ** 2 * (k - 1) * n <= 4 * m * m * (n - r) ** 2


def m_max(n, k, B):
    lo, hi = 3, 1
    while budget_ok(hi, n, k, B):
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        lo, hi = (mid, hi) if budget_ok(mid, n, k, B) else (lo, mid - 1)
    return lo


def m_min(r, n, k, mm):
    if not admitted(r, mm, n, k):
        return None
    lo, hi = 3, mm
    while lo < hi:
        mid = (lo + hi) // 2
        lo, hi = (lo, mid) if admitted(r, mid, n, k) else (mid + 1, hi)
    return lo


for name, n, k in ROWS:
    mm = m_max(n, k, BSTAR)
    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        mn = m_min(mid, n, k, mm)
        lo, hi = (mid, hi) if (mn is not None and mn <= mm) else (lo, mid - 1)
    r, mn = lo, m_min(lo, n, k, mm)
    check(r == PRINTED_R[name], f"{name}: safe edge {r} != printed {PRINTED_R[name]}")
    check(mn == PRINTED_M[name], f"{name}: witness band {mn} != printed {PRINTED_M[name]}")
    check(mm == PRINTED_M[name], f"{name}: m_max {mm} != printed {PRINTED_M[name]}")
    adj = m_min(r + 1, n, k, mm)
    check(adj is None or adj > mm, f"{name}: adjacent failure at r+1 not exhibited")
    g = PRINTED_GKL[name]
    check((n - g) ** 3 > (k - 1) * n * n, f"{name}: GKL24 gate fails at its printed edge")
    check(not ((n - g - 1) ** 3 > (k - 1) * n * n), f"{name}: GKL24 gate does not fail at r+1")

if errors:
    for e in errors:
        print("FAIL:", e)
    sys.exit(1)

print(
    "CORRIDOR_LITERAL_PRIME_PASS "
    f"q={Q} bits={Q.bit_length()} v2(q-1)={((Q-1)&-(Q-1)).bit_length()-1} "
    f"Bstar_match=yes proth_base={proth_base} pocklington_base={poc_base} "
    "six_rows=digit-exact adjacent_failures=exhibited"
)
