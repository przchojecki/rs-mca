#!/usr/bin/env python3
"""Verifier for the corridor unconditional safe-edge certificate.

Six clean-rate corridor rows (xr_budget_audit.md conventions):
Row C n = 2^10, k in {256, 128, 64}, q_line idealized 2^250 (prime unpinned,
qa3 flag C1(b)), B* = floor(q_line/2^128) = 2^122 exact; prize-max n = 2^41,
k in {2^39, 2^38, 2^37}, q_line idealized 2^255.9, B* = floor(2^127.9) =
integer 10th root of 2^1279. Budget rule: epsilon <= 2^-128 certified as
count <= B*. Sampler: finite_affine (slopes z in F, denominator q_line).
Closed integer radius grid r = n - a; supremum open at the first
unadmitted point.

Two independently proof-audited unconditional MCA imports (external audits
at github.com/latifkasuli/mca, commit 3fea63a):

GKL24 (ePrint 2024/1810 v3, Thm 3; docs/gkl24-proof-audit.md): for any
linear code with min relative distance Delta_C, any eta > 0 and
delta <= 1 - (1 - Delta_C + eta)^(1/3)  (eta INSIDE the radical),

  q * eps_mca(C, delta) < (n+6)/eta + 2/(eta*(cbrt(x) - sqrt(x))),
  x = 1 - Delta_C + eta.

RS rows: Delta_C = 1 - (k-1)/n; integer radius r admissible iff
(n-r)^3 > (k-1)*n^2 (exact gate). This certificate pins eta = eta* =
((n-r)/n)^3 - (k-1)/n, so x = beta^3 with beta = (n-r)/n and the budget
comparison B_GKL <= B* is decided by exact rationals after one squaring:

  2/(eta*(beta - beta^{3/2})) <= B* - (n+6)/eta*
    <=>  beta - c >= beta^{3/2}, c := 2/((B* - (n+6)/eta*) * eta*)
    <=>  beta >= c  and  (beta - c)^2 >= beta^3.

Hab25 (ePrint 2025/2110, Thm 2; docs/bchks25-thm46-import-audit.md,
section "Hab25 proof audit"): with rho_B = (k-1)/n, integer m >= 3, at
gamma = 1 - (1 + 1/(2m)) sqrt(rho_B),

  q * eps_mca(C, gamma) <= (l^7/3)(rho_B n)^2, l = (m+1/2)/sqrt(rho_B)
                        = (2m+1)^7 n^{7/2} / (2^7 * 3 * (k-1)^{3/2}).

Exact integer forms: radius r admitted at band m iff
(2m+1)^2 (k-1) n <= 4 m^2 (n-r)^2; budget B_note(m) <= B* iff
(2m+1)^14 n^7 <= 9 * 2^14 * (k-1)^3 * B*^2. The admitted-m set at radius
r is an up-set [m_min(r), inf) and the budget-admitted set a down-set
[3, m_max], so r is certified iff m_min(r) <= m_max, and failure at r+1
is exactly: (n-r-1)^2 <= (k-1)n (past the Johnson grid: no m at all), or
budget failure at m = m_min(r+1) (hence at every admitted m).

Modes:
  --write   regenerate the certificate JSON deterministically
  --check   recompute every row (edges, exact gate values, budget
            inequalities, adjacent failures) and compare to the JSON
Runs in well under a second; stdlib only; no floats in any verdict
(floats appear only in reported log2 margins).
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from math import isqrt, log2
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT = (
    HERE.parent
    / "data"
    / "certificates"
    / "corridor-unconditional-safe-edges"
    / "corridor_unconditional_safe_edges.json"
)

BSTAR_ROWC = 2**122
BSTAR_PRIZE_EXPECTED = 317494674775468773183020924238786383963

# (row, n, k, q_line description, B*, current edge r (BCIKS20 (1-rho)/2 via
#  cor:conditional-half packaging), corridor decision candidate A)
ROWS = [
    ("RowC-1/4", 2**10, 256, "idealized 2^250, prime unpinned (qa3 flag C1(b))", BSTAR_ROWC, 384, 261),
    ("RowC-1/8", 2**10, 128, "idealized 2^250, prime unpinned (qa3 flag C1(b))", BSTAR_ROWC, 448, 133),
    ("RowC-1/16", 2**10, 64, "idealized 2^250, prime unpinned (qa3 flag C1(b))", BSTAR_ROWC, 480, 67),
    ("prize-1/4", 2**41, 2**39, "idealized 2^255.9 (prize-max convention)", BSTAR_PRIZE_EXPECTED, 824633720832, 558345748481),
    ("prize-1/8", 2**41, 2**38, "idealized 2^255.9 (prize-max convention)", BSTAR_PRIZE_EXPECTED, 962072674304, 283467841537),
    ("prize-1/16", 2**41, 2**37, "idealized 2^255.9 (prize-max convention)", BSTAR_PRIZE_EXPECTED, 1030792151040, 141733920769),
]

# Pinned claims (recomputed, not trusted, by --check).
GKL24_R = {
    "RowC-1/4": 379,
    "RowC-1/8": 513,
    "RowC-1/16": 619,
    "prize-1/4": 813725411113,
    "prize-1/8": 1099511627777,
    "prize-1/16": 1326340298262,
}
HAB25_R = {
    "RowC-1/4": 512,
    "RowC-1/8": 663,
    "RowC-1/16": 769,
    "prize-1/4": 1092724518963,
    "prize-1/8": 1415997755216,
    "prize-1/16": 1644686143216,
}
HAB25_M_WITNESS = {
    "RowC-1/4": 256,
    "RowC-1/8": 477,
    "RowC-1/16": 127,
    "prize-1/4": 81,
    "prize-1/8": 70,
    "prize-1/16": 60,
}
HAB25_M_MAX = {
    "RowC-1/4": 21145,
    "RowC-1/8": 18211,
    "RowC-1/16": 15670,
    "prize-1/4": 81,
    "prize-1/8": 70,
    "prize-1/16": 60,
}


def iroot(x: int, e: int) -> int:
    """floor(x ** (1/e)) for x >= 0, exact."""
    if x < 0:
        raise ValueError("negative radicand")
    if x == 0:
        return 0
    hi = 1 << (x.bit_length() // e + 1)
    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**e <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo


def sqrt_ub(x: Fraction, scale: int = 2**200) -> Fraction:
    """Rational upper bound on sqrt(x), x >= 0."""
    return Fraction(isqrt((x.numerator * scale * scale) // x.denominator) + 1, scale)


def flog2(x: Fraction) -> float:
    return log2(x.numerator) - log2(x.denominator)


# ---------------------------------------------------------------- GKL24 ----

def gkl24_edge(n: int, k: int) -> int:
    """Largest r with (n-r)^3 > (k-1)*n^2 (exact integer admissibility gate)."""
    rhs = (k - 1) * n * n
    a = iroot(rhs, 3) + 1
    while a**3 <= rhs:
        a += 1
    assert (a - 1) ** 3 <= rhs < a**3
    return n - a


def gkl24_budget_ok(n: int, k: int, r: int, bstar: int) -> bool:
    """Exact check B_GKL(r, eta*) <= B* (see module docstring)."""
    beta = Fraction(n - r, n)
    eta = beta**3 - Fraction(k - 1, n)
    if eta <= 0:
        return False
    t1 = Fraction(n + 6) / eta
    rem = bstar - t1
    if rem <= 0:
        return False
    c = Fraction(2) / (rem * eta)
    return beta >= c and (beta - c) ** 2 >= beta**3


def gkl24_bound_ub(n: int, k: int, r: int) -> Fraction:
    """Certified rational upper bound on B_GKL(r, eta*) for reporting."""
    beta = Fraction(n - r, n)
    eta = beta**3 - Fraction(k - 1, n)
    assert eta > 0
    diff_lb = beta - sqrt_ub(beta**3)
    assert diff_lb > 0
    return Fraction(n + 6) / eta + Fraction(2) / (eta * diff_lb)


# ---------------------------------------------------------------- Hab25 ----

def hab25_budget_ok(n: int, k: int, m: int, bstar: int) -> bool:
    return (2 * m + 1) ** 14 * n**7 <= 9 * 2**14 * (k - 1) ** 3 * bstar * bstar


def hab25_m_max(n: int, k: int, bstar: int) -> int:
    rhs = 9 * 2**14 * (k - 1) ** 3 * bstar * bstar
    t = iroot(rhs // n**7, 14)
    while t**14 * n**7 > rhs:
        t -= 1
    while (t + 1) ** 14 * n**7 <= rhs:
        t += 1
    m = (t - 1) // 2
    assert hab25_budget_ok(n, k, m, bstar) and not hab25_budget_ok(n, k, m + 1, bstar)
    return m


def hab25_radius_ok(n: int, k: int, r: int, m: int) -> bool:
    return (2 * m + 1) ** 2 * (k - 1) * n <= 4 * m * m * (n - r) ** 2


def hab25_amin_at_band(n: int, k: int, m: int) -> int:
    """Smallest agreement-complement A = n - r admitted at band m."""
    c = (2 * m + 1) ** 2 * (k - 1) * n
    a = isqrt(c // (4 * m * m))
    while 4 * m * m * a * a < c:
        a += 1
    while a > 1 and 4 * m * m * (a - 1) ** 2 >= c:
        a -= 1
    return a


def hab25_m_min(n: int, k: int, r: int) -> int | None:
    """Smallest m >= 3 admitting radius r; None iff (n-r)^2 <= (k-1)n."""
    a = n - r
    if a * a <= (k - 1) * n:
        return None
    hi = 1
    while not hab25_radius_ok(n, k, r, hi):
        hi *= 2
    lo = 1
    while lo < hi:
        mid = (lo + hi) // 2
        if hab25_radius_ok(n, k, r, mid):
            hi = mid
        else:
            lo = mid + 1
    return max(lo, 3)


def hab25_bound_log2(n: int, k: int, m: int) -> float:
    """log2 of B_note(m) = (2m+1)^7 n^{7/2} / (2^7 * 3 * (k-1)^{3/2})."""
    return 7 * log2(2 * m + 1) + 3.5 * log2(n) - 7 - log2(3) - 1.5 * log2(k - 1)


def johnson_grid_edge(n: int, k: int) -> int:
    """Largest r with r/n < 1 - sqrt((k-1)/n): (n-r)^2 > (k-1)n (context only)."""
    kk = (k - 1) * n
    a = isqrt(kk)
    while a * a <= kk:
        a += 1
    assert a * a > kk >= (a - 1) ** 2
    return n - a


# -------------------------------------------------------------- payload ----

IMPORTS = {
    "gkl24": {
        "name": "GKL24 Theorem 3 (l = 1) via the Definition-8 bridge",
        "statement": (
            "Let C be any linear code in F_q^n with minimum relative distance "
            "Delta_C, let eta > 0 and delta <= 1 - (1 - Delta_C + eta)^(1/3) "
            "(eta inside the radical; 1.5-Johnson endpoint open). Then, in the "
            "normalization of def:mca, q * eps_mca(C, delta) < "
            "(n+6)/eta + 2/(eta * ((1-Delta_C+eta)^(1/3) - (1-Delta_C+eta)^(1/2))). "
            "For C = RS[F,D,k] (upstream convention, dim k), Delta_C = 1-(k-1)/n "
            "and an integer radius r is admissible iff (n-r)^3 > (k-1)*n^2. "
            "For l >= 1 independent batching challenges multiply the bound by l "
            "(GKL24 Thm 4). Projective sampler: numerator +1, denominator q+1."
        ),
        "provenance": {
            "source": "Gao-Kan-Li, Linear Proximity Gaps for Linear Codes within the 1.5 Johnson Bound, Cryptology ePrint 2024/1810, v3 (2025-03-30)",
            "source_sha256_prefix": "bdab46f002f8",
            "proof_status": "PROOF-COMPLETE for the mutual form (external line-by-line audit; 12 recoverable errata closed in-audit; zero external proof dependencies; Definition-8 <=> def:mca bridge proved in the audit, >=-direction unconditional, equivalence on delta < Delta_C)",
            "audit": "github.com/latifkasuli/mca docs/gkl24-proof-audit.md @ 3fea63a",
            "caveats": "ePrint, not peer-reviewed; v3 follows a v1 with an acknowledged critical mistake (found by Kopparty; v1 was RS-only); re-verify the live ePrint version/date against the pinned sha256 when this import lands",
        },
    },
    "hab25": {
        "name": "Hab25 Theorem 2 (M = 1 affine line = def:mca verbatim)",
        "statement": (
            "Let C = RS[F_q, D, k_note] with |D| = n and dimension k_note + 1 "
            "(upstream bridge: k_note = k - 1, rho_B = (k-1)/n). For every "
            "integer m >= 3, at gamma = 1 - (1 + 1/(2m)) * sqrt(rho_B): "
            "q * eps_mca(C, gamma) <= (l^7/3) * (rho_B * n)^2 with "
            "l = (m + 1/2)/sqrt(rho_B), i.e. "
            "<= (2m+1)^7 * n^(7/2) / (2^7 * 3 * (k-1)^(3/2)). Every "
            "delta <= gamma is covered by monotonicity of the def:mca event. "
            "Projective sampler: numerator +1, denominator q+1."
        ),
        "provenance": {
            "source": "Ulrich Haboeck, A note on mutual correlated agreement for Reed-Solomon codes, Cryptology ePrint 2025/2110 (2025-11-17)",
            "proof_status": "PROVED (external line-by-line audit: Definition 1 = def:mca event at M = 1 verbatim; quadratic error; bookkeeping gaps G1-G3 closed in-audit; all deferrals verified against BCIKS20 ECCC TR20-083). The improved linear-in-n constant of BCHKS25 Thm 4.6 and M > 1 remain sketch-only (gap G4) and are NOT used here.",
            "audit": "github.com/latifkasuli/mca docs/bchks25-thm46-import-audit.md, section 'Hab25 proof audit' @ 3fea63a",
            "caveats": "ePrint, not peer-reviewed; re-verify the live ePrint version at import time",
        },
    },
}

NONCLAIMS = [
    "Below-band move only: the corridor band decision candidates (delta_A ~ 0.745 / 0.870 / 0.935, A = k + n/N'_dec + 1) and the five certification/counting blockers of the clean-rate program are untouched; nothing here decides any corridor row.",
    "Row C q_line is idealized 2^250 with the literal ~2^250 prime unpinned (qa3 flag C1(b)); prize q_line 2^255.9 is the prize-max convention. All margins are >= 43.9 bits except the Hab25 prize edges, which are budget-sharp by construction; any literal prime at those scales inherits the verdicts via the pinned exact B*.",
    "Both imports are ePrints, not peer-reviewed venues; a live-version check against the pinned artifacts (GKL24 v3 sha256 bdab46f002f8..., Hab25 2025/2110) is recommended when this packet is merged.",
    "No deployed-KoalaBear claim: on the rho = 1/2, q = p^6 ~ 2^185.9 row the proved Hab25 quadratic bound certifies only delta <= 428878/2^21 ~ 0.2045 < 1/4 (below the existing edge) and the linear-in-n constant remains conditional per the #272 packet (gap G4).",
    "GKL24 adds nothing at rate 1/4 (1.5-Johnson < (1-rho)/2 exactly when Delta_C <= 3 - sqrt(5); RS rates rho >= sqrt(5) - 2): the rate-1/4 GKL24 edges 379 / 813725411113 sit below the current 384 / 824633720832 and are recorded as cross-checks only.",
    "Claims are for the l = 1 / M = 1 affine line (= def:mca) only; l > 1 affine subspaces (GKL24 Thm 4) are available at cost factor l, and M > 1 curves are NOT covered (Hab25 asserts them without proof).",
    "No supremum claim: closed integer radius grid only, open at the first unadmitted point per the M0 freeze conventions.",
]


def gkl24_row(name: str, n: int, k: int, bstar: int, r_cur: int) -> dict:
    r = gkl24_edge(n, k)
    assert r == GKL24_R[name]
    beta = Fraction(n - r, n)
    eta = beta**3 - Fraction(k - 1, n)
    assert gkl24_budget_ok(n, k, r, bstar)
    b_ub = gkl24_bound_ub(n, k, r)
    return {
        "r": r,
        "delta": f"{r}/{n}",
        "delta_float": round(r / n, 6),
        "admissibility_gate": {
            "lhs_(n-r)^3": str((n - r) ** 3),
            "rhs_(k-1)n^2": str((k - 1) * n * n),
            "holds": True,
            "next_lhs_(n-r-1)^3": str((n - r - 1) ** 3),
            "fails_at_r_plus_1": True,
        },
        "eta_star": f"{eta.numerator}/{eta.denominator}",
        "bound_log2_upper": round(flog2(b_ub), 3),
        "budget_ok_exact": True,
        "margin_bits": round(flog2(Fraction(bstar)) - flog2(b_ub), 2),
        "min_qline_log2_for_2^-128": round(flog2(b_ub) + 128, 1),
        "gain_vs_current_r": r - r_cur,
        "supersedes_current": r > r_cur,
    }


def hab25_row(name: str, n: int, k: int, bstar: int, r_cur: int) -> dict:
    m_max = hab25_m_max(n, k, bstar)
    assert m_max == HAB25_M_MAX[name]
    r = n - hab25_amin_at_band(n, k, m_max)
    assert r == HAB25_R[name]
    m_w = hab25_m_min(n, k, r)
    assert m_w == HAB25_M_WITNESS[name]
    assert m_w is not None and 3 <= m_w <= m_max
    assert hab25_radius_ok(n, k, r, m_w) and hab25_budget_ok(n, k, m_w, bstar)
    m_next = hab25_m_min(n, k, r + 1)
    if m_next is None:
        adjacent = {
            "r_plus_1": r + 1,
            "mode": "past_johnson_grid",
            "witness": f"(n-r-1)^2 = {(n - r - 1) ** 2} <= (k-1)n = {(k - 1) * n}: no integer m admits the radius",
        }
    else:
        assert m_next > m_max and not hab25_budget_ok(n, k, m_next, bstar)
        adjacent = {
            "r_plus_1": r + 1,
            "mode": "budget",
            "m_min": m_next,
            "witness": f"m_min(r+1) = {m_next} > m_max = {m_max}; B_note(m_min) exceeds B* (exact 14th-power check), and B_note is increasing in m",
        }
    bl2 = hab25_bound_log2(n, k, m_w)
    return {
        "r": r,
        "delta": f"{r}/{n}",
        "delta_float": round(r / n, 6),
        "m_witness": m_w,
        "m_budget_max": m_max,
        "bound_log2_at_witness": round(bl2, 3),
        "budget_ok_exact": True,
        "margin_bits": round(flog2(Fraction(bstar)) - bl2, 2),
        "adjacent_failure": adjacent,
        "gain_vs_current_r": r - r_cur,
        "supersedes_current": r > r_cur,
    }


def payload() -> dict:
    rows = []
    for name, n, k, qdesc, bstar, r_cur, a_dec in ROWS:
        g = gkl24_row(name, n, k, bstar, r_cur)
        h = hab25_row(name, n, k, bstar, r_cur)
        assert h["r"] > r_cur and h["r"] >= g["r"]
        rows.append(
            {
                "row": name,
                "n": n,
                "k": k,
                "rho": f"{Fraction(k, n).numerator}/{Fraction(k, n).denominator}",
                "q_line": qdesc,
                "Bstar": str(bstar),
                "current_edge_r": r_cur,
                "current_edge_source": "BCIKS20 (1-rho)/2 import (cor:conditional-half packaging; fully published)",
                "gkl24_15J": g,
                "hab25_johnson_quadratic": h,
                "johnson_grid_edge_r": johnson_grid_edge(n, k),
                "corridor_decision_candidate_A": a_dec,
                "certified_safe_edge_r": h["r"],
                "certified_safe_edge_source": "hab25_johnson_quadratic",
            }
        )
    return {
        "schema": "corridor-unconditional-safe-edges-v1",
        "object": (
            "unconditional below-band safe-edge re-baseline for the six "
            "clean-rate corridor rows, from two independently proof-audited "
            "MCA imports (GKL24 1.5-Johnson linear-in-n; Hab25 Johnson "
            "quadratic-in-n); certified safe edges in def:mca normalization"
        ),
        "sampler": "finite_affine",
        "epsilon_rule": "epsilon <= 2^-128 certified as count <= B* = floor(q_line/2^128); closed integer radius grid, supremum open at the first unadmitted point (M0 freeze conventions)",
        "budgets": {
            "rowC_Bstar": str(BSTAR_ROWC),
            "prize_Bstar": str(BSTAR_PRIZE_EXPECTED),
            "prize_Bstar_definition": "exact integer 10th root of 2^1279 = floor(2^127.9) (xr_budget_audit.md section 1)",
        },
        "imports": IMPORTS,
        "rows": rows,
        "nonclaims": NONCLAIMS,
        "external_audit_commit": "github.com/latifkasuli/mca @ 3fea63a (docs/gkl24-proof-audit.md; docs/bchks25-thm46-import-audit.md incl. 'Hab25 proof audit'; docs/gkl24-corridor-import-audit.md)",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    assert iroot(2**1279, 10) == BSTAR_PRIZE_EXPECTED, "prize B* pin failed"

    if args.write:
        CERT.parent.mkdir(parents=True, exist_ok=True)
        CERT.write_text(json.dumps(payload(), indent=1, sort_keys=True) + "\n")
        print(f"wrote {CERT}")
    if args.check:
        recorded = json.loads(CERT.read_text())
        expected = payload()  # every assert inside re-runs the exact checks
        if recorded != expected:
            print(
                "FAIL: certificate JSON does not match deterministic regeneration",
                file=sys.stderr,
            )
            raise SystemExit(1)
        checks = 0
        for name, n, k, _qdesc, bstar, r_cur, _a in ROWS:
            rg = GKL24_R[name]
            assert (n - rg) ** 3 > (k - 1) * n * n
            assert (n - rg - 1) ** 3 <= (k - 1) * n * n
            assert gkl24_budget_ok(n, k, rg, bstar)
            rh, mw, mmax = HAB25_R[name], HAB25_M_WITNESS[name], HAB25_M_MAX[name]
            assert hab25_radius_ok(n, k, rh, mw)
            assert hab25_budget_ok(n, k, mw, bstar)
            assert not hab25_budget_ok(n, k, mmax + 1, bstar)
            m_next = hab25_m_min(n, k, rh + 1)
            assert m_next is None or (
                m_next > mmax and not hab25_budget_ok(n, k, m_next, bstar)
            )
            assert rh > r_cur
            checks += 7
        print(f"PASS: JSON reproduced deterministically; {checks} exact integer checks across 6 rows (edges, gates, budgets, adjacent failures)")
    if not (args.write or args.check):
        parser.error("pass --write and/or --check")


if __name__ == "__main__":
    main()
