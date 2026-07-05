#!/usr/bin/env python3
"""Verify the KoalaBear frontier-adjacent upper-ledger packet (corrected).

Builds / checks:

    experimental/data/certificates/frontier-adjacent/
        koalabear_frontier_adjacent_a1116043_a1116044.json

MATERIAL CORRECTION (2026-07-05, found in post-submission review by the
external team): the original packet's UNDECIDED_WINDOW_OPEN verdict at
a = 1116044 was too conservative.  Composing two already-merged upstream
statements — ``lem:v13f1-identity-prefix-floor`` (the c=1 identity-prefix
list floor at K = k+1) with ``prop:quantitative-deep-list-floor`` (v12 main
tex; equivalently ``thm:quant-deep-point`` in the strict352 section, whose
conclusion is the LD_sw metric verbatim) — certifies

    LD_sw(C, m) >= M(m) = ceil( L(m) (q-n) / (q-n + k(L(m)-1)) ),
    L(m) = ceil( C(n, m) / p^(m-k-1) )        [K = k+1 route]

with no density trigger (any L >= 1 qualifies; the (q+k)/k trigger the
original packet measured against belongs only to the thm:A contrapositive,
and v12's own rem:quantitative-floor-vs-contrapositive prescribes the
quantitative form for exactly this under-trigger case).  The five-point
sweep m = 1116044..1116048 flips 1116044-1116047 MCA-unsafe (margins
+102.47 / +71.33 / +40.15 / +8.98 bits over B*) and fails at 1116048
(-22.20 bits).  The corrected MCA-unsafe edge is a0' = 1116047 and the
corrected adjacent open step is a0'+1 = 1116048; this file recomputes every
number of the original packet that depends on the open-step agreement.

Everything is exact integer arithmetic (Python stdlib only).  The certificate
comparisons are the ~2M-bit binomial inequalities of
``prop:v13f1-identity-frontier`` (c=1) and the graded-prefix scan predicates
(c=2, c=4), plus the quantitative deep-list sweep above; the quotient cell is
the exact ``U_sum`` safe sum of ``def:v13-quotient-status`` /
``prop:v13-quotient-safe-sum`` over the declared dyadic divisor family
{2,4,8,16,32}.  Binomials of the form ``C(2^21, ~1.1M)`` are computed by
Legendre prime-power factorization plus a product tree (``math.comb`` is
~1000x slower at this size); each such binomial takes well under a second.
The ``U_sum`` accumulation is additionally cross-checked modulo the Mersenne
prime 2^61-1 through an independent factorial-table computation path, now at
all three fully-tabled agreements {1116043, 1116044, 1116048}.

Runtime, measured (Apple Silicon, CPython 3.13): the full recomputation takes
~120 s wall, dominated by the exact ``U_sum`` accumulation plus its modular
cross-check (the c=2 divisor alone is most of it, ~1M-bit incremental
big-integer steps; the third modular table costs a few extra seconds).  The
anchor binomials take ~0.2-0.3 s each; prime powers and all other checks take
well under a second.  ``--check`` reruns the full recomputation and
byte-compares the regenerated JSON, so it costs the same as ``--write``; both
stay comfortably under the ~5 minute budget.

Floats in the JSON are informational (rounded to 4 decimals); every verdict
is decided by exact integer comparison.  A platform whose libm rounds log2
differently in the last ulp could shift a final printed decimal; regenerate
with ``--write`` in that case.

Usage:

    python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --write
    python3 experimental/scripts/verify_koalabear_frontier_adjacent.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import time
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "koalabear-frontier-adjacent-ledger-v2"

# ---------------------------------------------------------------------------
# Row constants (KoalaBear MCA row).
# ---------------------------------------------------------------------------
P = 2**31 - 2**24 + 1  # 2130706433
Q_LINE = P**6
N = 2**21
K = 2**20
A0 = 1116043  # trigger-route unsafe edge (prop:v13f1-identity-frontier)
A1 = A0 + 1  # 1116044, the ORIGINAL packet's open step (now flipped unsafe)
A_EDGE = 1116047  # corrected MCA-unsafe edge (quantitative deep-list route)
A_OPEN = A_EDGE + 1  # 1116048, the corrected adjacent open step
QUANT_SWEEP = (1116044, 1116045, 1116046, 1116047, 1116048)
TARGET_BITS = 128
BSTAR = Q_LINE // 2**TARGET_BITS

# Expected exact values for the quantitative sweep (material correction
# 2026-07-05); every one is recomputed from scratch below and these pins
# only guard against silent drift.
EXPECTED_QUANT_L_1116044 = 1973967916468083369044358670918132115633867608112
EXPECTED_QUANT_M_1116044 = 1931247427137429416005585529088676636591240959005
EXPECTED_QUANT_M_1116047 = 138634741058327852652
EXPECTED_QUANT_M_1116048 = 57198030366
EXPECTED_QUANT_MARGINS = {
    1116044: 102.4700,
    1116045: 71.3269,
    1116046: 40.1523,
    1116047: 8.9778,
    1116048: -22.1969,
}
# Upstream-printed budget, cross-checked against
# experimental/data/certificates/paid-ledger-functions/paid_ledger_functions.json.
BSTAR_UPSTREAM = 274980728111395087

# Declared dyadic quotient fiber family for the SAFE_SUM cell.
QUOT_FAMILY = (2, 4, 8, 16, 32)

# Independent prime for the U_sum cross-check (Mersenne prime M61).
XCHECK_PRIME = 2**61 - 1

OUTPUT_DIR = ROOT / "experimental/data/certificates/frontier-adjacent"
OUTPUT_PATH = OUTPUT_DIR / "koalabear_frontier_adjacent_a1116043_a1116044.json"

PAID_LEDGER_JSON_REF = (
    "experimental/data/certificates/paid-ledger-functions/paid_ledger_functions.json"
)
CORRIDOR_JSON_REF = (
    "experimental/data/certificates/corridor-unconditional-safe-edges/"
    "corridor_unconditional_safe_edges.json"
)
BCHKS_EDGE_NOTE_REF = "experimental/notes/audits/koalabear_bchks25_jmca_safe_edge_v1.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


# ---------------------------------------------------------------------------
# Exact big-integer helpers.
# ---------------------------------------------------------------------------


def sieve_primes(limit: int) -> list[int]:
    flags = bytearray([1]) * (limit + 1)
    flags[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(limit) + 1):
        if flags[i]:
            flags[i * i :: i] = bytearray(len(range(i * i, limit + 1, i)))
    return [i for i in range(2, limit + 1) if flags[i]]


def legendre_exponent(n: int, m: int, p: int) -> int:
    """Exponent of the prime p in C(n, m) (Kummer/Legendre)."""
    e = 0
    pk = p
    while pk <= n:
        e += n // pk - m // pk - (n - m) // pk
        pk *= p
    return e


def product_tree(vals: list[int]) -> int:
    if not vals:
        return 1
    while len(vals) > 1:
        nxt = [vals[i] * vals[i + 1] for i in range(0, len(vals) - 1, 2)]
        if len(vals) % 2:
            nxt.append(vals[-1])
        vals = nxt
    return vals[0]


class Comb:
    """Exact binomials via prime factorization; fast at the 2M-bit scale."""

    def __init__(self, limit: int) -> None:
        self.primes = sieve_primes(limit)

    def __call__(self, n: int, m: int) -> int:
        if m < 0 or m > n:
            return 0
        factors = []
        for p in self.primes:
            if p > n:
                break
            e = legendre_exponent(n, m, p)
            if e:
                factors.append(p**e)
        return product_tree(factors)


def comb_step_up(value: int, n: int, m: int) -> int:
    """C(n, m) -> C(n, m+1), exactly."""
    return value * (n - m) // (m + 1)


def log2_int(x: int) -> float:
    require(x > 0, "log2 of nonpositive integer")
    bl = x.bit_length()
    if bl <= 64:
        return math.log2(x)
    return (bl - 64) + math.log2(x >> (bl - 64))


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def fingerprint(x: int) -> dict[str, Any]:
    """Exact commitment to a very large integer without printing all digits."""
    raw = x.to_bytes((x.bit_length() + 7) // 8, "big")
    return {
        "bit_length": x.bit_length(),
        "log2": round(log2_int(x), 4),
        "sha256_bigendian_bytes": sha256(raw).hexdigest(),
        "mod_2_64": x % 2**64,
        "mod_m61": x % (2**61 - 1),
        "mod_m31": x % (2**31 - 1),
    }


def is_prime_small(n: int) -> bool:
    """Deterministic Miller-Rabin (valid far beyond the 64-bit range)."""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


# ---------------------------------------------------------------------------
# Prefix-floor certificates (identity scale and graded scales).
# ---------------------------------------------------------------------------


def cert_record(
    *,
    cert_id: str,
    route: str,
    scale_c: int,
    m: int,
    binom: int,
    upstream_printed_margin: str | None,
) -> dict[str, Any]:
    """One exact prefix-floor comparison at scale c.

    MCA route (K = k+1, thm:A deep-point conversion):
        C(n/c, m) * k > p^w * (q + k),   w = m - ceil((k+1)/c).
    LIST route (K = k):
        C(n/c, m) * 2^128 > p^w * q,     w = m - ceil(k/c)   [v13 form]
        C(n/c, m) > p^w * B*                                  [scan form]
    Both list forms are computed; their verdicts must agree.
    """
    scan_holds = None
    if route == "mca":
        w = m - ceil_div(K + 1, scale_c)
        lhs = binom * K
        rhs = pow(P, w) * (Q_LINE + K)
    else:
        w = m - ceil_div(K, scale_c)
        lhs = binom * 2**TARGET_BITS
        rhs = pow(P, w) * Q_LINE
        scan_holds = binom > pow(P, w) * BSTAR
    holds = lhs > rhs
    margin = round(log2_int(lhs) - log2_int(rhs), 4)
    record: dict[str, Any] = {
        "id": cert_id,
        "route": route,
        "scale_c": scale_c,
        "m": m,
        "agreement_a": scale_c * m,
        "w": w,
        "predicate": (
            f"C({N // scale_c},{m}) * k > p^{w} * (q_line + k)"
            if route == "mca"
            else f"C({N // scale_c},{m}) * 2^128 > p^{w} * q_line"
        ),
        "binomial_bits": binom.bit_length(),
        "binomial_sha256": sha256(
            binom.to_bytes((binom.bit_length() + 7) // 8, "big")
        ).hexdigest(),
        "holds": holds,
        "margin_bits": margin,
    }
    if route == "list":
        require(
            scan_holds == holds,
            f"{cert_id}: v13 form and scan form (C > p^w * B*) disagree",
        )
        record["scan_form_agrees"] = True
    if upstream_printed_margin is not None:
        record["upstream_printed_margin_bits"] = upstream_printed_margin
        require(
            abs(float(upstream_printed_margin) - margin) < 0.05,
            f"{cert_id}: recomputed margin {margin} does not reproduce "
            f"upstream printed {upstream_printed_margin}",
        )
    return record


def quant_cert_record(m: int, binom: int) -> dict[str, Any]:
    """One exact quantitative deep-list floor comparison at scale c = 1.

    Composition (both statements already merged upstream):
      1. lem:v13f1-identity-prefix-floor at K = k+1, w = m - k - 1: some
         received word U has L = ceil(C(n,m)/p^w) >= 1 distinct
         RS[F,D,k+1]-codewords agreeing with it on >= m > k points each
         (a closed-ball list around one U with per-codeword supports).
      2. prop:quantitative-deep-list-floor (tex/cs25_cap_v12.tex; the sharper
         internal denominator q-n+k(L-1) is the official conclusion of
         thm:quant-deep-point, strict352 section, stated for LD_sw verbatim):
         some single line (f_alpha, g_alpha) has at least
         M = ceil(L(q-n)/(q-n+k(L-1))) support-wise MCA-bad finite slopes.

    No density trigger: any L >= 1 qualifies (the (q+k)/k threshold belongs
    only to the thm:A contrapositive; rem:quantitative-floor-vs-contrapositive
    prescribes this form for the under-trigger case).  Verdict: unsafe iff
    M > B*.  Both the sharp (k(L-1)) and the weaker printed (kL) denominator
    ceilings are computed and must agree on this sweep.
    """
    w = m - K - 1
    require(w >= 0, f"quant_mca_m{m}: w must be nonnegative")
    list_floor = ceil_div(binom, pow(P, w))
    require(list_floor >= 1, f"quant_mca_m{m}: L >= 1 must hold")
    omega = Q_LINE - N  # |Omega| = q - n, poles alpha in F \ D
    m_sharp = ceil_div(list_floor * omega, omega + K * (list_floor - 1))
    m_weak = ceil_div(list_floor * omega, omega + K * list_floor)
    require(
        m_sharp == m_weak,
        f"quant_mca_m{m}: sharp k(L-1) and printed kL denominator ceilings "
        "must agree on this sweep",
    )
    holds = m_sharp > BSTAR
    margin = round(log2_int(m_sharp) - log2_int(BSTAR), 4)
    require(
        abs(margin - EXPECTED_QUANT_MARGINS[m]) < 0.01,
        f"quant_mca_m{m}: margin {margin} drifted from expected "
        f"{EXPECTED_QUANT_MARGINS[m]}",
    )
    return {
        "id": f"quant_mca_m{m}",
        "route": "quantitative_deep_list",
        "scale_c": 1,
        "m": m,
        "agreement_a": m,
        "w": w,
        "delta0_exact": f"{N - m}/{N}",
        "predicate": (
            f"M = ceil(L (q_line - n) / (q_line - n + k (L - 1))) > B*, "
            f"L = ceil(C({N},{m}) / p^{w})  [K = k+1 route]"
        ),
        "authority": "lem:v13f1-identity-prefix-floor + "
        "prop:quantitative-deep-list-floor (= thm:quant-deep-point for "
        "LD_sw); no density trigger in the hypotheses",
        "list_floor_L": list_floor,
        "list_floor_L_log2": round(log2_int(list_floor), 4),
        "M_bad_slopes": m_sharp,
        "M_log2": round(log2_int(m_sharp), 4),
        "conversion_lossless": m_sharp == list_floor,
        "weak_kL_denominator_ceiling_agrees": True,
        "holds": holds,
        "margin_bits": margin,
    }


# ---------------------------------------------------------------------------
# Quotient SAFE_SUM cell (def:v13-quotient-status / prop:v13-quotient-safe-sum).
# ---------------------------------------------------------------------------


def usum_divisor_exact(comb: Comb, c: int, agreement: int) -> tuple[int, int]:
    """Exact U_c(A) = sum_{B=A}^{n} C(n/c, floor(B/c)) C(n - c floor(B/c), B - c floor(B/c)).

    Returns (U_c(A), head_term) where head_term is the single B = A summand,
    so that U_c(A+1) = U_c(A) - head_term.  Iterates Q = floor(B/c) upward
    with an exact incremental outer binomial.
    """
    nc_field = N // c
    q_min = ceil_div(agreement - (c - 1), c)
    require(q_min == agreement // c, "q_min must equal floor(A/c)")
    outer = comb(nc_field, q_min)
    total = 0
    head_term = None
    q = q_min
    while q <= nc_field:
        rest = N - c * q
        s_lo = max(0, agreement - c * q)
        inner = 0
        for s in range(s_lo, c):
            if s <= rest:
                inner += math.comb(rest, s)
        if head_term is None:
            # the unique B = agreement summand: s = A - c floor(A/c).
            head_term = outer * math.comb(rest, s_lo)
        total += outer * inner
        if q < nc_field:
            outer = comb_step_up(outer, nc_field, q)
        q += 1
    require(head_term is not None, "empty U_sum range")
    return total, head_term


def usum_mod_check(
    per_divisor: dict[int, dict[int, int]], prime: int
) -> None:
    """Independent recomputation of every U_c(A) modulo prime.

    Uses factorial tables mod prime (a different computation path from the
    incremental big-integer loop) and compares residues.
    """
    max_field = N // min(QUOT_FAMILY)
    fact = [1] * (max_field + 1)
    for i in range(1, max_field + 1):
        fact[i] = fact[i - 1] * i % prime
    inv_fact = [0] * (max_field + 1)
    inv_fact[max_field] = pow(fact[max_field], prime - 2, prime)
    for i in range(max_field, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % prime
    max_s = max(QUOT_FAMILY)
    inv_small_fact = [
        pow(math.factorial(s) % prime, prime - 2, prime) for s in range(max_s)
    ]

    def comb_mod_small(top: int, s: int) -> int:
        num = 1
        for i in range(s):
            num = num * ((top - i) % prime) % prime
        return num * inv_small_fact[s] % prime

    for agreement, table in per_divisor.items():
        for c in QUOT_FAMILY:
            nc_field = N // c
            total = 0
            for q in range(agreement // c, nc_field + 1):
                rest = N - c * q
                s_lo = max(0, agreement - c * q)
                inner = 0
                for s in range(s_lo, c):
                    if s <= rest:
                        inner += comb_mod_small(rest, s)
                outer = (
                    fact[nc_field]
                    * inv_fact[q]
                    % prime
                    * inv_fact[nc_field - q]
                    % prime
                )
                total = (total + outer * (inner % prime)) % prime
            require(
                table[c] % prime == total,
                f"U_sum modular cross-check failed: c={c} A={agreement}",
            )


def usum_term_exact(
    comb: Comb, outer_cache: dict[tuple[int, int], int], c: int, agreement: int
) -> int:
    """The single B = agreement summand of U_c, exactly."""
    q_floor = agreement // c
    key = (c, q_floor)
    if key not in outer_cache:
        outer_cache[key] = comb(N // c, q_floor)
    rest = N - c * q_floor
    s = agreement - c * q_floor
    require(0 <= s < c and s <= rest, "usum term shape violated")
    return outer_cache[key] * math.comb(rest, s)


def compute_usum(comb: Comb) -> dict[int, dict[int, int]]:
    """Exact per-divisor U_sum at {A0, A1, A_OPEN}, cross-checked mod M61.

    U_c(A0) is accumulated once by the full incremental loop; the later
    agreements peel off the exact single-B head terms
    U_c(A+1) = U_c(A) - term_c(A) (the head terms use independently
    recomputed anchor binomials, consistency-checked against the loop's own
    head term at A0).
    """
    per: dict[int, dict[int, int]] = {A0: {}, A1: {}, A_OPEN: {}}
    outer_cache: dict[tuple[int, int], int] = {}
    for c in QUOT_FAMILY:
        u_a0, head_term = usum_divisor_exact(comb, c, A0)
        require(
            head_term == usum_term_exact(comb, outer_cache, c, A0),
            f"U_sum head-term consistency failed at c={c}",
        )
        per[A0][c] = u_a0
        running = u_a0
        for b in range(A0, A_OPEN):
            running -= usum_term_exact(comb, outer_cache, c, b)
            require(running > 0, f"U_sum positivity violated at c={c} B={b + 1}")
            if b + 1 == A1:
                per[A1][c] = running
        per[A_OPEN][c] = running
    usum_mod_check(per, XCHECK_PRIME)
    return per


def quotient_gate_block(agreement: int) -> dict[str, Any]:
    """Zone-(a) norm-exact gate arithmetic: (N'+2)^{N'} <= q_line^2 at rho=1/2."""
    q2 = Q_LINE * Q_LINE
    t = agreement - K
    per_order = []
    for order in QUOT_FAMILY:
        lhs = (order + 2) ** order
        require(lhs <= q2, f"norm-exact gate unexpectedly fails at N'={order}")
        per_order.append(
            {
                "N_prime": order,
                "ell_prime": order // 2 + 1,
                "gate": f"{order + 2}^{order} <= q_line^2",
                "lhs_log2": round(log2_int(lhs), 4),
                "holds": True,
                "zone": "ZONE_A_NORM_EXACT",
            }
        )
    require((60 + 2) ** 60 <= q2, "gate boundary: expected N'=60 to pass")
    require((62 + 2) ** 62 > q2, "gate boundary: expected N'=62 to fail")
    return {
        "definition": "(2 ell')^{N'} <= q_line^2 with ell' = rho N' + 1 = "
        "N'/2 + 1 (paid_ledger_functions.md Zone Tags)",
        "q_line_squared_log2": round(log2_int(q2), 4),
        "per_declared_order": per_order,
        "gate_boundary": {
            "last_even_order_passing": 60,
            "first_even_order_failing": 62,
        },
        "active_order_cutoff": {
            "convention": "N' <= n/t (proof_sketch/s2_paid_ledger.md section 5)",
            "t": t,
            "n_over_t": round(N / t, 4),
            "floor_n_over_t": N // t,
            "active_dyadic_orders": [o for o in QUOT_FAMILY if o <= N // t],
            "note": "N'=32 exceeds the s2 active cutoff and is included "
            "conservatively in the declared coverage family; a superset "
            "family only enlarges the safe sum "
            "(prop:v13-quotient-safe-sum union bound).",
        },
        "conclusion": "every declared order sits in ZONE_A_NORM_EXACT; the "
        "zone-(b) collision conjecture is vacuous at this step (no zone-(b) "
        "interval cell is consumed by this packet).",
    }


# ---------------------------------------------------------------------------
# Ledger assembly.
# ---------------------------------------------------------------------------


def landmark(name: str, agreement: int, status: str, source: str) -> dict[str, Any]:
    delta = Fraction(N - agreement, N)
    return {
        "name": name,
        "agreement_a": agreement,
        "delta_exact": f"{delta.numerator}/{delta.denominator}",
        "delta_float": round(float(delta), 7),
        "a_steps_from_1116048": agreement - A_OPEN,
        "status": status,
        "source": source,
    }


def build_certificate() -> dict[str, Any]:
    t_start = time.time()
    comb = Comb(N)

    # Self-test of the factorization binomial against math.comb.
    for n_t, m_t in ((5000, 2101), (4096, 2048), (6000, 1)):
        require(comb(n_t, m_t) == math.comb(n_t, m_t), "Comb self-test failed")

    require(is_prime_small(P), "p is not prime")
    require(BSTAR == BSTAR_UPSTREAM, "B* does not match the upstream printed value")
    paid_ledger = json.loads((ROOT / PAID_LEDGER_JSON_REF).read_text(encoding="utf-8"))
    require(
        any(
            f"q/2^128 budget floor = {BSTAR_UPSTREAM}" in d
            for chk in paid_ledger["checks"]
            for d in chk["details"]
        ),
        "paid-ledger-functions certificate does not print the expected B*",
    )
    corridor = (ROOT / CORRIDOR_JSON_REF).read_text(encoding="utf-8")
    require(
        "428878/2^21 ~ 0.2045" in corridor,
        "corridor packet does not print the proved Hab25-quadratic KoalaBear edge",
    )
    bchks_note = (ROOT / BCHKS_EDGE_NOTE_REF).read_text(encoding="utf-8")
    require(
        "A = n-r = 1493067" in bchks_note,
        "BCHKS25 conditional-edge note does not print a = 1493067",
    )

    # --- anchor binomials and incremental neighbours -----------------------
    t0 = time.time()
    c1 = {A0: comb(N, A0)}  # C(2^21, m)
    for m in range(A0, A_OPEN):
        c1[m + 1] = comb_step_up(c1[m], N, m)
    c2 = {558019: comb(N // 2, 558019)}  # C(2^20, m)
    for m in range(558019, 558023):
        c2[m + 1] = comb_step_up(c2[m], N // 2, m)
    c4_m = A1 // 4  # 279011; a = 1116044 lies on the c=4 grid (v2(a)=2)
    c4 = {c4_m: comb(N // 4, c4_m)}
    t_binom = time.time() - t0

    # --- exact prefix-floor certificates ------------------------------------
    certificates = [
        cert_record(
            cert_id="c1_mca_m1116043",
            route="mca",
            scale_c=1,
            m=A0,
            binom=c1[A0],
            upstream_printed_margin="+25.7",
        ),
        cert_record(
            cert_id="c1_mca_m1116044",
            route="mca",
            scale_c=1,
            m=A1,
            binom=c1[A1],
            upstream_printed_margin="-5.5",
        ),
        cert_record(
            cert_id="c1_list_m1116044",
            route="list",
            scale_c=1,
            m=1116044,
            binom=c1[1116044],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c1_list_m1116045",
            route="list",
            scale_c=1,
            m=1116045,
            binom=c1[1116045],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c1_list_m1116046",
            route="list",
            scale_c=1,
            m=1116046,
            binom=c1[1116046],
            upstream_printed_margin="+9.2",
        ),
        cert_record(
            cert_id="c1_list_m1116047",
            route="list",
            scale_c=1,
            m=1116047,
            binom=c1[1116047],
            upstream_printed_margin="-22.0",
        ),
        cert_record(
            cert_id="c2_mca_m558019",
            route="mca",
            scale_c=2,
            m=558019,
            binom=c2[558019],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c2_mca_m558020",
            route="mca",
            scale_c=2,
            m=558020,
            binom=c2[558020],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c2_mca_m558022",
            route="mca",
            scale_c=2,
            m=558022,
            binom=c2[558022],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c2_list_m558022",
            route="list",
            scale_c=2,
            m=558022,
            binom=c2[558022],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c2_list_m558023",
            route="list",
            scale_c=2,
            m=558023,
            binom=c2[558023],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c4_mca_m279011",
            route="mca",
            scale_c=4,
            m=c4_m,
            binom=c4[c4_m],
            upstream_printed_margin=None,
        ),
        cert_record(
            cert_id="c4_list_m279011",
            route="list",
            scale_c=4,
            m=c4_m,
            binom=c4[c4_m],
            upstream_printed_margin=None,
        ),
    ]
    # Material correction 2026-07-05: the quantitative deep-list sweep.
    quant_records = {m: quant_cert_record(m, c1[m]) for m in QUANT_SWEEP}
    certificates.extend(quant_records[m] for m in QUANT_SWEEP)
    by_id = {rec["id"]: rec for rec in certificates}

    # Quantitative-sweep pins (the corrected edge/open pair).
    for m in (1116044, 1116045, 1116046, 1116047):
        require(quant_records[m]["holds"], f"quantitative floor must pass at m={m}")
    require(
        not quant_records[A_OPEN]["holds"],
        f"quantitative floor must fail at m={A_OPEN}",
    )
    require(
        quant_records[1116044]["list_floor_L"] == EXPECTED_QUANT_L_1116044,
        "L(1116044) drifted from the triple-verified value",
    )
    require(
        quant_records[1116044]["M_bad_slopes"] == EXPECTED_QUANT_M_1116044,
        "M(1116044) drifted from the triple-verified value",
    )
    require(
        quant_records[A_EDGE]["M_bad_slopes"] == EXPECTED_QUANT_M_1116047,
        "M(1116047) drifted from the triple-verified value",
    )
    require(
        quant_records[A_EDGE]["conversion_lossless"],
        "the conversion must be lossless (M = L) at the new edge",
    )
    require(
        quant_records[A_OPEN]["M_bad_slopes"] == EXPECTED_QUANT_M_1116048,
        "M(1116048) drifted from the triple-verified value",
    )
    require(N - A_EDGE == 981105, "new-edge radius must be 981105")

    # Edge pins (adjacent-tight structure of the ORIGINAL routes; all still
    # true — only the row verdicts they were read as implying changed).
    require(by_id["c1_mca_m1116043"]["holds"], "c=1 MCA must pass at 1116043")
    require(not by_id["c1_mca_m1116044"]["holds"], "c=1 MCA must fail at 1116044")
    require(by_id["c1_list_m1116044"]["holds"], "c=1 LIST must pass at 1116044")
    require(by_id["c1_list_m1116045"]["holds"], "c=1 LIST must pass at 1116045")
    require(by_id["c1_list_m1116046"]["holds"], "c=1 LIST must pass at 1116046")
    require(not by_id["c1_list_m1116047"]["holds"], "c=1 LIST must fail at 1116047")
    require(by_id["c2_mca_m558019"]["holds"], "c=2 MCA must pass at m=558019")
    require(not by_id["c2_mca_m558020"]["holds"], "c=2 MCA must fail at m=558020")
    require(not by_id["c2_mca_m558022"]["holds"], "c=2 MCA must fail at m=558022")
    require(by_id["c2_list_m558022"]["holds"], "c=2 LIST must pass at m=558022")
    require(not by_id["c2_list_m558023"]["holds"], "c=2 LIST must fail at m=558023")
    require(not by_id["c4_mca_m279011"]["holds"], "c=4 MCA must fail at a=1116044")
    require(not by_id["c4_list_m279011"]["holds"], "c=4 LIST must fail at a=1116044")
    # a = 1116044 = 2^2 * 59 * 4729 sits on the c in {1,2,4} grids only.
    require(A1 % 4 == 0 and A1 % 8 != 0, "v2(1116044) must equal 2")
    require(4 * 59 * 4729 == A1, "1116044 must factor as 2^2 * 59 * 4729")
    require(is_prime_small(59) and is_prime_small(4729), "factor primality")

    # --- conversion-gap target (RETIRED by the material correction) ---------
    w_fail = A1 - K - 1  # 67467
    list_floor = ceil_div(c1[A1], pow(P, w_fail))  # list floor in RS[F,D,k+1]
    require(
        list_floor == quant_records[A1]["list_floor_L"],
        "the conversion-gap list floor and the quantitative-sweep L(1116044) "
        "must be the same integer",
    )
    log2_list_floor = log2_int(list_floor)
    log2_threshold = log2_int(Q_LINE + K) - log2_int(K)  # (q+k)/k
    gap_bits = log2_threshold - log2_list_floor
    mca_fail_margin = by_id["c1_mca_m1116044"]["margin_bits"]
    require(
        abs(gap_bits + mca_fail_margin) < 0.002,
        "conversion gap must agree with the c=1 MCA failure margin",
    )
    # Reverification of the original packet's printed values (still correct
    # as statements about the strong q/k trigger, and nothing else).
    require(abs(log2_list_floor - 160.4336) < 0.001, "list floor log2 drifted")
    require(abs(log2_threshold - 165.9321) < 0.001, "conversion threshold drifted")
    require(abs(gap_bits - 5.4985) < 0.001, "conversion gap drifted")
    require(abs(2**gap_bits - 45.21) < 0.05, "conversion gap factor drifted")
    conversion_gap = {
        "status_label": "RETIRED_BY_MATERIAL_CORRECTION_2026_07_05",
        "certified_list_floor_at_a1116044": {
            "code": "RS[F_p^6, D, k+1]",
            "construction": "lem:v13f1-identity-prefix-floor at c=1, "
            "m=1116044, w=67467; L = ceil(C(n,m)/p^w), exact integer",
            "value": list_floor,
            "log2": round(log2_list_floor, 4),
        },
        "strong_trigger_threshold": {
            "formula": "(q_line + k)/k  (prop:v13f1-identity-frontier proof: "
            "list > q/k + 1 with m >= k+1 admissibility, via thm:A "
            "contrapositive)",
            "log2": round(log2_threshold, 4),
        },
        "gap_bits_to_strong_trigger": round(gap_bits, 4),
        "gap_factor": round(2**gap_bits, 2),
        "retirement": "The original packet framed this 5.4985-bit number as "
        "the minimum new mathematics needed to flip a = 1116044.  That "
        "framing was wrong: the number is only the gap to the strong (q+k)/k "
        "trigger of the thm:A contrapositive.  prop:quantitative-deep-list-"
        "floor has no density trigger (any L >= 1 qualifies), and v12's own "
        "rem:quantitative-floor-vs-contrapositive prescribes it for exactly "
        "this under-trigger case; composing it with the same certified list "
        "floor flips a = 1116044 by +102.4700 bits with zero bits of new "
        "mathematics (see quant_mca_m1116044 and material_correction).  The "
        "analogous residual at the NEW open step a = 1116048 is different "
        "in kind: the quantitative conversion is already lossless there "
        "(M = L), so the -22.1969-bit shortfall is the prefix list floor "
        "itself, not the conversion — the next sharpening target is the "
        "floor, not the conversion constant.",
    }
    material_correction = {
        "date": "2026-07-05",
        "credit": "found in post-submission review by the external team",
        "what_changed": "the original verdict UNDECIDED_WINDOW_OPEN at "
        "a = 1116044 is corrected to UNSAFE_BY_PROVED_LOWER_BOUND "
        "(residual-label vocabulary: COUNTEREXAMPLE_NEW_FLOOR — a lower "
        "certificate crossing B* at the previously-open step); the same "
        "route flips 1116045-1116047, so the MCA-unsafe edge moves from "
        "1116043 to 1116047 and the adjacent open step from 1116044 to "
        "1116048.",
        "composition": "lem:v13f1-identity-prefix-floor (K = k+1: a closed-"
        "ball list of L = ceil(C(n,m)/p^w) distinct RS[F,D,k+1]-codewords "
        "around one received word, each agreeing on >= m > k points) + "
        "prop:quantitative-deep-list-floor (v12 main tex; sharp-denominator "
        "form = thm:quant-deep-point, strict352, stated for LD_sw): some "
        "single received line carries M = ceil(L(q-n)/(q-n+k(L-1))) "
        "support-wise MCA-bad finite slopes.  Slopes are values P_i(alpha) "
        "in the line field F_{p^6}; the count is a max over lines, never a "
        "family sum; both statements were already merged upstream when the "
        "original packet shipped.",
        "certificates": [f"quant_mca_m{m}" for m in QUANT_SWEEP],
        "new_unsafe_edge": A_EDGE,
        "new_open_step": A_OPEN,
        "certified_unsafe_delta_interval": "[981105/2097152, 1/2) = "
        "[0.4678273..., 1/2)  (previously [981109/2097152, 1/2))",
        "why_the_original_packet_under_claimed": "it measured the certified "
        "list floor only against the strong (q+k)/k deep-point trigger "
        "inherited from prop:v13f1-identity-frontier's proof route, and "
        "parked the ~2^160.40 quantitative number inside B_ext as "
        "hypothetical pending condition (i) of prop:v13-extension.  Both "
        "cautions conflated compiler hypotheses with the direct theorem: "
        "the trigger belongs to the thm:A contrapositive (the quantitative "
        "proposition needs no trigger), and condition (i) governs only "
        "extension-only CELL attribution in the upper ledger (the row "
        "verdict takes poles in Omega = F \\ D and never routes through the "
        "v13 extension compiler).",
        "consistency": "no proved-safe statement is contradicted (nearest "
        "unconditional safe radius delta ~ 0.2045; Johnson at a = 1482910; "
        "exactness zone at a >= 1747627); only the finite adjacent-pair "
        "prediction of prob:v13f1-frontier (a Problem, explicitly "
        "route-relative) is refuted at this row, and the conjectured pin "
        "moves to a* >= 1116048.  The new MCA edge 1116047 sits one step "
        "past upstream's proved list edge 1116046 — exactly the K = k+1 vs "
        "K = k offset (one fewer prefix slot, ~31.17 bits more list mass "
        "per step).",
    }

    # --- extension cell arithmetic ------------------------------------------
    m_gap = Q_LINE - P
    ext_pole = ceil_div(list_floor * m_gap, m_gap + K * (list_floor - 1))
    ext_excess = log2_int(ext_pole) - log2_int(BSTAR)
    extension_cell = {
        "status_label": "CONDITIONAL_ON_NAMED_INPUT",
        "row_type": "proper extension row: q_gen = p < q_line = p^6, so "
        "Paid_ext^only = 0 does NOT apply (paid_ledger_functions.md "
        "section 3)",
        "ext_pole_arithmetic": {
            "formula": "ExtPole(q_line, q_gen, kappa, L) = "
            "ceil(L (q_line - q_gen) / (q_line - q_gen + kappa (L-1))), "
            "kappa = k (prop:v13-extension official compiler denominator)",
            "kappa": K,
            "L": "the c=1 list floor at a = 1116044 (see "
            "conversion_gap_target)",
            "value_log2": round(log2_int(ext_pole), 4),
            "value_bit_length": ext_pole.bit_length(),
            "excess_over_budget_bits_if_certified": round(ext_excess, 4),
            "hypothetical_only": "arithmetic instantiation only, as an "
            "extension-only CELL value.  A valid ExtPole cell floor "
            "additionally requires the pole-conversion certificate "
            "conditions (i)/(ii) of prop:v13-extension; condition (i) "
            "(distinct pole values give distinct extension-only bad line "
            "parameters for THIS row) is not certified here.  SCOPE "
            "CORRECTION (2026-07-05): condition (i) blocks only the "
            "extension-only cell ATTRIBUTION in the upper ledger's "
            "first-match grammar; it does not gate the ROW verdict, which "
            "prop:quantitative-deep-list-floor delivers directly with poles "
            "in Omega = F \\ D (see material_correction and "
            "quant_mca_m1116044).  The original packet's reading of this "
            "caveat as parking the ~2^160.40 number entirely was the "
            "under-claim this correction fixes.",
        },
        "safe_side": "the safe-side chart classification (S6) of every "
        "extension-valued residual chart is explicitly undischarged "
        "(paid_ledger_functions.md DAG Discharge); no finite chart-family "
        "exhaustion theorem exists at this row, so the extension upper cell "
        "is OPEN pending the named input.",
        "named_input": "PR #284 (F1 minimal-field-descent packet): unique "
        "minimal field of definition B <= K <= F makes the S6/F1 chart "
        "split {K=B, B<K<F, K=F} exhaustive and mutually exclusive; cited "
        "as a structural input, not consumed as a bound.",
    }

    # --- quotient SAFE_SUM cell ----------------------------------------------
    t0 = time.time()
    usum_parts = compute_usum(comb)
    t_usum = time.time() - t0
    usum_totals = {a: sum(parts.values()) for a, parts in usum_parts.items()}
    require(
        usum_totals[A0] > usum_totals[A1] > usum_totals[A_OPEN] > 0,
        "U_sum monotonicity violated",
    )

    def usum_block(total: int, parts: dict[int, int]) -> dict[str, Any]:
        return {
            "status_label": "PAID_BY_THEOREM",
            "grade": "SAFE_SUM (no image-lcm or exact block-profile "
            "certificate is supplied at this row, so the EXACT_IMAGE / "
            "EXACT_SUPPORT grades of def:v13-quotient-status are not "
            "available)",
            "formula": "U_sum(n,A,C) = sum_{c in C} sum_{B=A}^{n} "
            "C(n/c, floor(B/c)) C(n - c floor(B/c), B - c floor(B/c))",
            "declared_family": list(QUOT_FAMILY),
            "coverage": "prop:v13-quotient-safe-sum: valid conservative "
            "upper numerator for the union of the DECLARED dyadic quotient "
            "cells only (declared-coverage hypothesis); it is not global "
            "quotient exhaustion and bounds no other cell.",
            "value_fingerprint": fingerprint(total),
            "per_divisor_log2": {
                str(c): round(log2_int(parts[c]), 4) for c in QUOT_FAMILY
            },
            "excess_over_budget_bits": round(
                log2_int(total) - log2_int(BSTAR), 4
            ),
            "note": "astronomically above B*, as expected for a "
            "support-count union bound at delta ~ 0.4678; the upper ledger "
            "documents it honestly rather than consuming it.",
        }

    # --- tangent cells --------------------------------------------------------
    r_tan_cap = (N - K) // 3  # 349525
    require(ceil_div(2 * N + K, 3) == N - r_tan_cap, "R_tan zone boundary")

    def tangent_block(agreement: int) -> dict[str, Any]:
        r = N - agreement
        return {
            "lower_floor": {
                "status_label": "PAID_BY_THEOREM",
                "value": r + 1,
                "value_log2": round(log2_int(r + 1), 4),
                "statement": f"LD_sw(C,{agreement}) >= n - a + 1 = {r + 1}: "
                "the moving-root witness half of prop:v13-tangent needs "
                "only n - r - 1 >= k, i.e. a >= k+1, which holds here; "
                "this is a LOWER floor (unsafe mass), not an upper cell.",
            },
            "upper_exact_cell": {
                "status_label": "OPEN",
                "value": "UNAVAILABLE",
                "reason": f"r = {r} > R_tan = {r_tan_cap} = floor((n-k)/3): "
                "Paid_tan^hi is UNAVAILABLE outside the high-agreement "
                "range by its own type (def:v13-tangent-cell, "
                "paid_ledger_functions.md section 1); a packet must use a "
                "different tangent/common-line theorem or leave the cell "
                "open.  No silent n - A + 1 upper value is printed.",
            },
        }

    # --- aperiodic cell --------------------------------------------------------
    def aperiodic_block(agreement: int) -> dict[str, Any]:
        t = agreement - K
        j = N - agreement
        return {
            "B_ap_regular": {
                "status_label": "CONJECTURAL_WITH_FALSIFIER",
                "value": "NONEXISTENT_BUCKET",
                "t": t,
                "j_plus_1": j + 1,
                "deficiency": j + 1 - t,
                "reason": "the regular overdetermined Hankel branch exists "
                f"only when t >= j+1 (towards-prize.md section 3); here "
                f"t = {t} << j+1 = {j + 1} (deficiency {j + 1 - t}), the "
                "deep underdetermined regime.  No proved formula for "
                "B_ap_regular or B_ap_pivot exists at this row.",
            },
            "B_ap_pivot": {
                "status_label": "CONJECTURAL_WITH_FALSIFIER",
                "value": "OPEN",
                "reason": "the M5/WP-2.6 pivot-chart program is developed "
                "only at deficiency 1 on the toy F_17^32 row; nothing is "
                "instantiable at deficiency ~9.1e5.",
            },
            "falsifier": "per the task's own wording, 'audit the "
            "aperiodic-band input separately': a staircase/SPI/XR "
            "population bound at this deficiency bounding the aperiodic "
            "band above, or an explicit aperiodic family whose exact mass "
            "exceeds the deficit (which would instead be "
            "COUNTEREXAMPLE_NEW_FLOOR).",
            "named_future_input": "PR #282 (XR eliminant packets: "
            "light-profile eliminant nonvanishing, coordinate hypersurface "
            "reduction, eliminant vanishing class) — cited as partial "
            "structural progress on this residual; its own text disclaims "
            "row-level adjacent upper-ledger status and defers to a "
            "separate staircase/SPI/XR rationing input.",
        }

    # --- sparse / plain-CA cell ------------------------------------------------
    johnson_a = math.isqrt(N * N // 2)
    require(
        johnson_a**2 <= N * N // 2 < (johnson_a + 1) ** 2,
        "Johnson agreement isqrt check failed",
    )
    require(johnson_a == 1482910, "Johnson agreement drifted")
    require(johnson_a - A_OPEN == 366862, "Johnson distance drifted")
    require(1493067 - A_OPEN == 377019, "conditional-edge distance drifted")
    require(
        ceil_div(2 * N + K, 3) - A_OPEN == 631579,
        "exactness-zone distance drifted",
    )
    landmarks = [
        landmark(
            "capacity agreement a = k (delta = 1 - rho = 1/2)",
            K,
            "reference point",
            "row parameters",
        ),
        landmark(
            "c=2 MCA prefix-floor edge (verified above, adjacent-tight)",
            1116038,
            "PROVED (recomputed here)",
            "c2_mca_m558019 / c2_mca_m558020",
        ),
        landmark(
            "c=1 identity-prefix MCA trigger-route edge a0 (verified above)",
            A0,
            "PROVED (recomputed here)",
            "c1_mca_m1116043 / c1_mca_m1116044; prop:v13f1-identity-frontier",
        ),
        landmark(
            "the ORIGINAL packet's open step, flipped MCA-unsafe by the "
            "2026-07-05 material correction",
            A1,
            "PROVED UNSAFE (recomputed here; was UNDECIDED in the original "
            "packet)",
            "quant_mca_m1116044; material_correction",
        ),
        landmark(
            "c=1 identity-prefix LIST unsafe edge (verified above)",
            1116046,
            "PROVED (recomputed here)",
            "c1_list_m1116046 / c1_list_m1116047",
        ),
        landmark(
            "corrected MCA-unsafe edge a0' (quantitative deep-list route, "
            "verified above)",
            A_EDGE,
            "PROVED (recomputed here)",
            "quant_mca_m1116047 / quant_mca_m1116048",
        ),
        landmark(
            "the corrected adjacent open step under audit",
            A_OPEN,
            "UNDECIDED (this packet, post-correction)",
            "thm:v13-windows; quant_mca_m1116048 fails at -22.1969 bits",
        ),
        landmark(
            "Johnson agreement floor(n/sqrt(2)) (1 - sqrt(rho) radius)",
            johnson_a,
            "reference point (no MCA theorem at this row)",
            "exact isqrt(n^2/2)",
        ),
        landmark(
            "conditional BCHKS25/Hab25 JMCA safe edge (gap G4: unproved "
            "linear-in-n Hab25 constant)",
            1493067,
            "CONDITIONAL_ON_NAMED_INPUT (not usable here)",
            BCHKS_EDGE_NOTE_REF,
        ),
        landmark(
            "half-distance / unique-decoding agreement (delta = 1/4)",
            N - (N - K) // 2,
            "reference point",
            "row parameters",
        ),
        landmark(
            "proved Hab25-quadratic safe edge on this row",
            N - 428878,
            "PROVED (imported; far below this step)",
            CORRIDOR_JSON_REF,
        ),
        landmark(
            "unconditional LD_sw-exactness zone start a = ceil((2n+k)/3) "
            "(equivalently r <= R_tan)",
            ceil_div(2 * N + K, 3),
            "PROVED zone boundary",
            "def:v13-tangent-cell / prop:v13-tangent",
        ),
    ]
    delta_open = Fraction(N - A_OPEN, N)
    sparse_cell = {
        "status_label": "OPEN",
        "reason": "no MCA/CA soundness theorem reaches delta = "
        f"{delta_open.numerator}/{delta_open.denominator} ~ "
        f"{round(float(delta_open), 7)} on this row: the proved "
        "Hab25-quadratic import certifies only delta <= 428878/2^21 ~ "
        "0.2045 (below the 1/4 edge); the 604085/2^21 ~ 0.2880502 edge is "
        "conditional on the unproved Hab25 linear-in-n constant (gap G4, "
        "integrated #272 audit); Johnson sits 366862 agreement steps above "
        "this step.  The strongest nearby proved list statement is the c=1 "
        "LIST edge at a = 1116046 (+9.1637 bits over the 2^128 list budget, "
        "two steps below); at this step the identity-prefix list floor in "
        "RS[F,D,k+1] is still >= 2^35.7 (quant_mca_m1116048's L), so any "
        "safety proof must in particular tolerate that certified list "
        "structure.",
        "delta_gap_to_conditional_radius": {
            "exact": "377019/2097152",
            "float": round(377019 / N, 7),
        },
        "delta_gap_to_johnson": {
            "exact": f"{johnson_a - A_OPEN}/2097152",
            "float": round((johnson_a - A_OPEN) / N, 7),
        },
        "delta_gap_to_unconditional_zone": {
            "exact": "631579/2097152",
            "float": round(631579 / N, 7),
        },
        "landmarks": landmarks,
    }

    # --- mu4 cell ---------------------------------------------------------------
    require((P - 1) % 4 == 0, "mu4 precondition 4 | p-1 fails")
    require(P - 1 == 2**24 * 127 and is_prime_small(127), "p-1 factorization")
    mu4_cell = {
        "status_label": "CONJECTURAL_WITH_FALSIFIER",
        "grade": "EMPIRICAL_NOT_A_THEOREM_AT_THIS_ROW",
        "count_if_transfers": 4,
        "precondition": "4 | p - 1 holds (p - 1 = 2^24 * 127), so the slope "
        "set mu_4 (4th roots of unity) exists in F_p",
        "evidence": "u - v = +/- n/4 monomial-line family with stable count "
        "|mu_4| = 4, engine-exact on toy rows (F_97: n=16 a=12; n=32 a=24, "
        "exhaustive 240-pair grid); external empirical evidence, and the "
        "tested agreements sit at a/n = 3/4, not at this step's "
        "a/n ~ 0.5322",
        "falsifier": "an exhaustive or theorem-backed count of the "
        "u - v = +/- n/4 monomial family at a deployed-shaped row "
        "contradicting +4",
        "note": "one-sided codeword lines contribute exactly 0 "
        "(forced-vacuous).  The +4 is never added to any theorem-backed "
        "total in this packet.",
    }

    # --- deficit and verdicts -----------------------------------------------
    # The deficit ledger now lives at the CORRECTED open step a = 1116048.
    # (The original a = 1116044 deficit ledger is mooted: the quantitative
    # route supplies ~2^160.40 of the ~2^57.93 needed there.)
    tangent_mass_open = N - A_OPEN + 1  # 981105
    quant_mass_open = quant_records[A_OPEN]["M_bad_slopes"]  # 57198030366
    proved_mass_open = max(tangent_mass_open, quant_mass_open)
    require(proved_mass_open == quant_mass_open, "quantitative floor must dominate")
    deficit = BSTAR + 1 - proved_mass_open
    require(deficit == 274980670913364722, "deficit arithmetic drifted")
    deficit_block = {
        "at_agreement": A_OPEN,
        "unsafety_gate": f"LD_sw(C,{A_OPEN}) >= B* + 1 = {BSTAR + 1}",
        "proved_lower_mass": proved_mass_open,
        "proved_lower_mass_log2": round(log2_int(proved_mass_open), 4),
        "proved_lower_mass_source": "max(tangent floor n-a+1 = "
        f"{tangent_mass_open}, quantitative deep-list floor M(1116048) = "
        f"{quant_mass_open}) — lower certificates are a MAXIMUM over "
        "witnesses, never a family sum (v12 lower-ledger convention); the "
        "quantitative floor dominates.",
        "budget_log2": round(log2_int(BSTAR), 4),
        "deficit": deficit,
        "deficit_log2": round(log2_int(deficit), 4),
        "known_over_budget_ratio": float(proved_mass_open / BSTAR),
        "structured_family_shortfall_bits": round(
            log2_int(BSTAR) - log2_int(proved_mass_open), 4
        ),
        "reading": "known mass 2^35.74 vs B* ~ 2^57.93: a -22.1969-bit "
        "shortfall, and it is the prefix list floor itself (the conversion "
        "is already lossless at this step, M = L), so the next sharpening "
        "target is the floor, not the conversion constant.  The empirical "
        "mu4 +4 is dominated and is not summed.",
        "moots": "the original packet's a = 1116044 deficit ledger "
        "(deficit 274980728110413979 against tangent mass 981109), mooted "
        "by quant_mca_m1116044.",
    }

    per_step_bits = round(math.log2(P) + math.log2(A0 + 1) - math.log2(N - A0), 4)

    verdict_a0 = {
        "verdict": "UNSAFE_BY_PROVED_LOWER_BOUND",
        "mechanism": "c=1 identity-prefix MCA floor "
        "(PAID_BY_EXACT_CERTIFICATE, margin "
        f"{by_id['c1_mca_m1116043']['margin_bits']:+.4f} bits, exact "
        "integer comparison c1_mca_m1116043): N(1116043) > B*, i.e. "
        f"N(1116043) >= B* + 1 = {BSTAR + 1}",
        "explicit_structured_floor": N - A0 + 1,
    }

    def flipped_verdict(m: int) -> dict[str, Any]:
        rec = quant_records[m]
        return {
            "verdict": "UNSAFE_BY_PROVED_LOWER_BOUND",
            "residual_label": "COUNTEREXAMPLE_NEW_FLOOR",
            "mechanism": "quantitative deep-list floor "
            f"(PAID_BY_EXACT_CERTIFICATE, margin {rec['margin_bits']:+.4f} "
            f"bits, exact integer comparison {rec['id']}): "
            f"LD_sw(C,{m}) >= M = {rec['M_bad_slopes']} > B*, via "
            "lem:v13f1-identity-prefix-floor + "
            "prop:quantitative-deep-list-floor (see material_correction)",
            "explicit_structured_floor": rec["M_bad_slopes"],
        }

    verdict_a1 = flipped_verdict(A1)
    verdict_a1["supersedes"] = (
        "UNDECIDED_WINDOW_OPEN (the original packet verdict; corrected "
        "2026-07-05, found in post-submission review by the external team)"
    )
    verdict_a1["list_object_at_this_agreement"] = (
        "additionally certified list-unsafe by two independent exact "
        "certificates (c1_list_m1116044 at "
        f"{by_id['c1_list_m1116044']['margin_bits']:+.4f} bits and the "
        "adjacent-tight c=2 edge c2_list_m558022 at "
        f"{by_id['c2_list_m558022']['margin_bits']:+.4f} bits)."
    )

    verdict_a_open = {
        "verdict": "UNDECIDED_WINDOW_OPEN",
        "mechanism": f"thm:v13-windows with L = {proved_mass_open} (the "
        "quantitative deep-list floor at m = 1116048; it dominates the "
        "tangent floor 981105, and lower certificates max rather than sum) "
        "<= B* and no finite upper certificate K (the upper ledger has OPEN "
        "cells: tangent-upper, aperiodic, sparse/CA, extension-chart); the "
        "budget sits in the unresolved window L <= B(q) < K.",
        "known_lower_mass": proved_mass_open,
        "known_lower_mass_log2": round(log2_int(proved_mass_open), 4),
        "budget": BSTAR,
        "budget_log2": round(log2_int(BSTAR), 4),
        "deficit_to_unsafety": deficit,
        "no_safety_theorem_in_range": "see sparse_plain_ca_cell landmarks",
    }

    def agreement_block(
        agreement: int,
        usum_total: int,
        usum_parts: dict[int, int],
        verdict: dict[str, Any],
    ) -> dict[str, Any]:
        delta = Fraction(N - agreement, N)
        return {
            "A": agreement,
            "r": N - agreement,
            "t": agreement - K,
            "j": N - agreement,
            "delta_exact": f"{delta.numerator}/{delta.denominator}",
            "delta_float": round(float(delta), 7),
            "budget": BSTAR,
            "B_tan": tangent_block(agreement),
            "B_quot_support": usum_block(usum_total, usum_parts),
            "B_quot_image": {
                "status_label": "OPEN",
                "value": "NO_CERTIFICATE",
                "reason": "no image-lcm certificate "
                "(thm:exact-quotient-image-lcm-ledger) is supplied at this "
                "row; the cell stays at the SAFE_SUM grade above.",
            },
            "B_ap": aperiodic_block(agreement),
            "B_ext": extension_cell,
            "sparse_plain_ca_cell": sparse_cell
            if agreement == A_OPEN
            else {
                "status_label": "OPEN",
                "reason": "same landmark geometry as at 1116048 (a few "
                "steps away); see the a=1116048 block.",
            },
            "mu4_family_cell": mu4_cell,
            "quotient_zone_gate": quotient_gate_block(agreement),
            "deduped_total_upper_bound": "NOT_FINITE_OPEN_CELLS: no finite "
            "U(a) exists because the tangent-upper, aperiodic, sparse/CA "
            "and extension-chart cells are OPEN; per agents.md no residual "
            "may be hidden in a point estimate, so no total is printed.",
            "verdict_block": verdict,
        }

    def flipped_agreement_block(m: int) -> dict[str, Any]:
        delta = Fraction(N - m, N)
        return {
            "A": m,
            "r": N - m,
            "t": m - K,
            "j": N - m,
            "delta_exact": f"{delta.numerator}/{delta.denominator}",
            "delta_float": round(float(delta), 7),
            "budget": BSTAR,
            "upper_ledger": "not built at this agreement: the row is "
            "certified unsafe by the quantitative deep-list floor, so per "
            "thm:v13-corridor only the largest certified-unsafe agreement "
            "and the first candidate safe step need full cell tables; the "
            "full tables in this packet sit at 1116043, 1116044 and "
            "1116048.",
            "verdict_block": flipped_verdict(m),
        }

    certificate = {
        "schema_version": SCHEMA_VERSION,
        "status": "EXPERIMENTAL / AUDIT",
        "object": "exact frontier-adjacent row packet on the KoalaBear MCA "
        "row (support-wise MCA finite-slope numerator vs the 2^-128 "
        "budget); corrected 2026-07-05 to edge/open pair {1116047, 1116048} "
        "(originally {1116043, 1116044})",
        "task_provenance": {
            "declared_task": "Before promotion to Paper D, build the exact "
            "upper ledger for the adjacent safe-side step, keep "
            "polynomial-loss quotient equidistribution out of finite "
            "one-step claims unless constants fit inside the printed bit "
            "margin, and audit the aperiodic-band input separately.",
            "source": "experimental/agents-log.md, 2026-07-04 entry 'CAP25 "
            "v13 identity-prefix frontier merge'; canonical spec: agents.md "
            "section 'The complete upper ledger to build at a0 + 1'",
            "correction_provenance": "material correction 2026-07-05, found "
            "in post-submission review by the external team; see "
            "material_correction",
        },
        "row": {
            "code": "RS[F_p^6, D, 2^20]",
            "field_line": "F_{p^6}, p = 2^31 - 2^24 + 1 (KoalaBear)",
            "p": P,
            "generated_field": "F_p (received words and domain are "
            "F_p-valued; lines sampled from F_{p^6})",
            "domain": "multiplicative subgroup D of F_p^x of order 2^21",
            "n": N,
            "k": K,
            "rho": "1/2",
            "mca_route_dimension": "floors built at K = k+1 then converted "
            "by the thm:A deep-point conversion, exactly as in "
            "prop:v13f1-identity-frontier",
        },
        "denominators": {
            "q_gen": P,
            "q_line": Q_LINE,
            "q_chal": Q_LINE,
            "q_list": Q_LINE,
            "sampler": "finite_affine (slopes z in F; the projective "
            "variant shifts numerator/denominator by 1 — immaterial at "
            "these margins)",
        },
        "target": {
            "epsilon": "2^-128",
            "budget_formula": "B* = floor(q_line / 2^128)",
            "budget": BSTAR,
            "budget_log2": round(log2_int(BSTAR), 4),
            "q_line_log2": round(log2_int(Q_LINE), 4),
        },
        "agreement_interval": {"a_min": A0, "a_max": A_OPEN},
        "endpoint_convention": "closed integer ball r = n - a; if an "
        "interior first safe agreement a* exists, the largest safe closed "
        "integer radius is n - a* and the real supremum (n - a* + 1)/n is "
        "not attained (cor:v13-endpoint)",
        "deduplication_rule": {
            "convention": "WP-2.3 first-match stratification tree T0-T7, "
            "evaluated first-match-wins; that order IS the dedup convention "
            "(wp2_3_stratification_case_tree.md).  Tangent filter: "
            "per-slope syndrome criterion u + z v = 0 (PR #171) as "
            "primary.",
            "application_here": "no cross-cell total is formed: the only "
            "finite theorem-backed upper cell (quotient SAFE_SUM) is never "
            "added to any other cell because the tangent-upper, aperiodic, "
            "sparse/CA and extension-chart cells are OPEN.  Internal dedup "
            "of the SAFE_SUM is the declared-family union bound of "
            "prop:v13-quotient-safe-sum plus lem:one-support-one-line "
            "(each fixed support pays at most one finite bad slope).",
        },
        "unsafe_certificates": certificates,
        "certificate_sensitivity": {
            "per_a_step_bits_at_edge": per_step_bits,
            "note": "one a-step multiplies RHS/LHS of the c=1 predicate by "
            "p (m+1)/(n-m) (~31.17 bits at the edge), and the quantitative "
            "deep-list floor decays by the same ~31.17 bits per step (only "
            "the comparison threshold differs: ~B* = 2^57.93 instead of "
            "the strong trigger 2^165.93, which is why the edge moves four "
            "steps): the 1116047/1116048 flip is generic "
            "threshold-crossing, not arithmetic structure.  The single "
            "structural coincidence: a = 1116044 is exactly the "
            "adjacent-tight c=2 LIST-route edge (m = 558022), giving a "
            "second independent list-unsafety certificate at precisely "
            "that agreement.",
        },
        "agreements": {
            str(A0): agreement_block(
                A0, usum_totals[A0], usum_parts[A0], verdict_a0
            ),
            str(A1): agreement_block(
                A1, usum_totals[A1], usum_parts[A1], verdict_a1
            ),
            "1116045": flipped_agreement_block(1116045),
            "1116046": flipped_agreement_block(1116046),
            str(A_EDGE): flipped_agreement_block(A_EDGE),
            str(A_OPEN): agreement_block(
                A_OPEN, usum_totals[A_OPEN], usum_parts[A_OPEN], verdict_a_open
            ),
        },
        "material_correction": material_correction,
        "conversion_gap_target": conversion_gap,
        "deficit_ledger": deficit_block,
        "corridor_statement": "per thm:v13-corridor the certified corridor "
        "is 1 + max A_unsafe = 1116048 <= a* <= min A_safe (A_safe empty "
        "in this packet -> convention a_max); the packet narrows nothing "
        "on the safe side.  The finite adjacent-pair prediction of "
        "prob:v13f1-frontier for this row (a* = 1116044) is REFUTED by the "
        "material correction; a* = 1116048 is the corrected conjectural "
        "adjacent value, and the quantitative route realizes all but the "
        "last ~1.5 steps of the asymptotic ceiling 1 - rho - g* = "
        "0.4678266 (def:v13f1-gstar), which survives.",
        "nonclaims": [
            "no adjacent pin is claimed: a* >= 1116048 is proved, "
            "a* = 1116048 is conjectural; the window at 1116048 stays open "
            "per thm:v13-windows",
            "no finite U(1116048) <= B* statement exists or is claimed: "
            "the upper ledger has OPEN cells (tangent-upper, aperiodic, "
            "sparse/CA, extension-chart), so no deduped finite total is "
            "printed",
            "the LIST-route certificates at 1116044 concern the companion "
            "list object; the MCA verdict there is decided by the separate "
            "quantitative deep-list certificate quant_mca_m1116044",
            "the ExtPole value remains hypothetical as an extension-only "
            "CELL value (condition (i) of prop:v13-extension is not "
            "certified at this row); the row verdicts never route through "
            "the extension compiler",
            "U_sum covers only the declared dyadic quotient cells "
            "{2,4,8,16,32}; it is not global quotient exhaustion",
            "the mu4 +4 is empirical toy-row evidence and is never added "
            "to a theorem-backed total",
            "no external safety import applies at delta ~ 0.4678: the "
            "proved Hab25-quadratic import reaches only ~0.2045, and the "
            "~0.2881 edge is conditional (gap G4)",
            "PRs #282 and #284 are cited as named future inputs only; this "
            "packet does not audit or consume them",
            "polynomial-loss quotient equidistribution is kept out of "
            "every finite claim, per the task instruction (a factor n^C "
            "costs 21C bits at n = 2^21 against the printed margins, the "
            "tightest being the +8.9778-bit edge certificate)",
        ],
        "replay": {
            "script": "experimental/scripts/verify_koalabear_frontier_adjacent.py",
            "command": "python3 experimental/scripts/"
            "verify_koalabear_frontier_adjacent.py --check",
            "determinism": "no randomness; exact integer arithmetic only; "
            "--check rebuilds the JSON and byte-compares",
            "big_integer_commitments": "values above ~2^200 are stored as "
            "fingerprints (bit_length, log2, sha256 of big-endian bytes, "
            "residues mod 2^64 / M61 / M31); the verifier recomputes the "
            "exact integers and re-derives every fingerprint; U_sum is "
            "additionally recomputed modulo M61 = 2^61-1 through an "
            "independent factorial-table path",
        },
        "source_artifacts": {
            "paid_ledger_functions": {
                "ref": PAID_LEDGER_JSON_REF,
                "sha256": sha256_file(PAID_LEDGER_JSON_REF),
            },
            "corridor_unconditional_safe_edges": {
                "ref": CORRIDOR_JSON_REF,
                "sha256": sha256_file(CORRIDOR_JSON_REF),
            },
            "bchks25_conditional_edge_note": {
                "ref": BCHKS_EDGE_NOTE_REF,
                "sha256": sha256_file(BCHKS_EDGE_NOTE_REF),
            },
        },
    }

    print(f"[timing] anchor binomials: {t_binom:.1f}s")
    print(f"[timing] U_sum exact + modular cross-check: {t_usum:.1f}s")
    print(f"[timing] total build: {time.time() - t_start:.1f}s")
    return certificate


def summarize(cert: dict[str, Any]) -> None:
    print("== unsafe certificates ==")
    for rec in cert["unsafe_certificates"]:
        print(
            f"  {rec['id']:>18}: a={rec['agreement_a']} "
            f"{'PASS' if rec['holds'] else 'FAIL'} "
            f"margin {rec['margin_bits']:+.4f} bits"
        )
    mc = cert["material_correction"]
    print(
        f"== material correction {mc['date']} == new unsafe edge "
        f"a0' = {mc['new_unsafe_edge']}, new open step {mc['new_open_step']}; "
        f"unsafe delta interval {mc['certified_unsafe_delta_interval']}"
    )
    gap = cert["conversion_gap_target"]
    print(
        "== retired trigger gap == list floor 2^"
        f"{gap['certified_list_floor_at_a1116044']['log2']} vs strong "
        f"trigger 2^{gap['strong_trigger_threshold']['log2']} -> "
        f"{gap['gap_bits_to_strong_trigger']} bits (gap to the q/k trigger "
        "only; RETIRED as a next-theorem target)"
    )
    dfc = cert["deficit_ledger"]
    print(
        f"== deficit at A={dfc['at_agreement']} == proved mass "
        f"{dfc['proved_lower_mass']} (2^{dfc['proved_lower_mass_log2']}) vs "
        f"B* 2^{dfc['budget_log2']}; deficit {dfc['deficit']}"
    )
    for a_key in sorted(cert["agreements"]):
        blk = cert["agreements"][a_key]
        line = f"== A={a_key} == verdict {blk['verdict_block']['verdict']}"
        if "B_quot_support" in blk:
            fp = blk["B_quot_support"]["value_fingerprint"]
            line += (
                f"; U_sum log2 {fp['log2']} "
                f"(+{blk['B_quot_support']['excess_over_budget_bits']} bits over B*)"
            )
        print(line)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build or check the KoalaBear frontier-adjacent ledger packet."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="build and write the JSON")
    mode.add_argument(
        "--check",
        nargs="?",
        const=str(OUTPUT_PATH),
        metavar="PATH",
        help="rebuild and byte-compare against the stored JSON",
    )
    args = parser.parse_args()

    cert = build_certificate()
    summarize(cert)
    payload = render(cert)
    if args.write:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(payload, encoding="utf-8")
        print(f"wrote {OUTPUT_PATH.relative_to(ROOT)}")
    else:
        path = Path(args.check)
        stored = path.read_text(encoding="utf-8")
        if stored != payload:
            raise AssertionError(f"frontier-adjacent ledger mismatch: {path}")
        print(f"check OK: {path} matches the full recomputation")


if __name__ == "__main__":
    main()
