#!/usr/bin/env python3
"""Verifier for the first in-repo COMPLETE adjacent staircase certificate on the
LIST route at an enumerable toy row.

Row: RS[F_17, D, k=8] with D = mu_16 = F_17^x (full multiplicative group),
n=16, rho=1/2, list route (K=k=8, no MCA conversion).  Toy sampler denominator
Q_list = p^k = 17^8 (a toy list-denominator convention -- deployed list rows
denominate by the shared Q = q_line = |F| of prop:q-exact-target, not p^k);
eps* = 2^-29; B* = floor(eps* Q_list) = 12.  Closed-ball endpoint convention,
agreement threshold ">= a".

Headline staircase at a0=10 / a0+1=11:

    L(10) = 32  >  B* = 12  >=  U(11) = 7.

The unsafe side L(10)=32 is the EXACT worst-received-word list-(>=a0) count,
obtained by full enumeration of all C(16,10)=8008 ten-subsets bucketed by their
depth-w=2 signed elementary-symmetric prefix mod 17; the heaviest bucket has 32
members at the NULL prefix z*=(0,0), i.e. the received word y = X^10 on D, and
all 32 codewords c_M = X^10 - ell_M are reconstructed (deg<8, agreement exactly
10, pairwise distinct).  This realizes prop:prefix-witness (grande_finale.tex)
end-to-end.  The safe side U(11)=7 is the unconditional all-received-words
Johnson/Cauchy-Schwarz packing bound, valid because a0+1=11 is ABOVE the Johnson
radius sqrt(n(k-1))=sqrt(112)~=10.58.

There is NO residual / conditional cell: this is a complete two-sided
certificate for the GRAMMAR of def:staircase on the list route.  It does NOT
exercise the hard row-sharp-Q cell that the deployed BELOW-Johnson-radius rows
need (see honest_gap in the packet and the companion note).

Usage:
    python3 experimental/scripts/verify_toy_complete_adjacent_list_staircase.py
        -> recompute everything from scratch, cross-check the shipped packet
           JSON field-by-field, run tamper self-tests; exit 0 iff all PASS.

    python3 experimental/scripts/verify_toy_complete_adjacent_list_staircase.py --emit
        -> (re)generate the packet JSON from the recomputed values.

Stdlib python3 only.  Runs in well under 90 s (all enumerations are <= 8008).
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path

# ----------------------------------------------------------------------------
# Fixed row parameters (toy list row).
# ----------------------------------------------------------------------------
P = 17           # prime field F_p
N = 16           # n = |D|
K = 8            # k (list route: K_list = k)
T = K - 1        # 7 : two distinct deg-<k codewords agree on <= k-1 points
RHO_NUM, RHO_DEN = 1, 2
A0 = 10          # unsafe agreement (headline)
A1 = A0 + 1      # 11 : safe agreement (headline)
W0 = A0 - K      # 2 : prefix depth at a0
LAMBDA = 29      # eps* = 2^-lambda
A_COMP0 = 11     # companion unsafe agreement
A_COMP1 = 12     # companion safe agreement

CERT_REL = "experimental/data/certificates/frontier-adjacent/toy_complete_adjacent_list_staircase_v1.json"
NOTE_REL = "experimental/notes/frontier-adjacent/toy_complete_adjacent_list_staircase_v1.md"
VERIFIER_REL = "experimental/scripts/verify_toy_complete_adjacent_list_staircase.py"
REPO_BASE = "53bb5df"


# ----------------------------------------------------------------------------
# Field / domain.
# ----------------------------------------------------------------------------
def mult_order(x: int, p: int) -> int:
    o, v = 1, x % p
    while v != 1:
        v = (v * x) % p
        o += 1
    return o


def build_D(p: int, n: int) -> list[int]:
    """D = mu_n, the n-th roots of unity in F_p (needs n | p-1); sorted."""
    assert (p - 1) % n == 0, "need n | p-1"
    g = next(c for c in range(2, p) if mult_order(c, p) == p - 1)
    h = pow(g, (p - 1) // n, p)
    D, v = [], 1
    for _ in range(n):
        D.append(v)
        v = (v * h) % p
    assert len(set(D)) == n
    return sorted(D)


# ----------------------------------------------------------------------------
# Polynomial helpers over F_p (coefficients low -> high).
# ----------------------------------------------------------------------------
def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                r[i + j] = (r[i + j] + ai * bj) % p
    return r


def ell(subset, p: int) -> list[int]:
    """Monic vanishing polynomial prod (X - x); coeffs low->high, leading 1."""
    r = [1]
    for x in subset:
        r = poly_mul(r, [(-x) % p, 1], p)
    return r


def prefix_of(subset, p: int, w: int):
    """Signed elementary-symmetric prefix (coeff of X^{a-1}, ..., X^{a-w})."""
    a = len(subset)
    c = ell(subset, p)          # c[a] = 1 leading
    return tuple(c[a - 1 - j] for j in range(w))


def poly_eval(coeffs, x: int, p: int) -> int:
    r = 0
    for a in reversed(coeffs):
        r = (r * x + a) % p
    return r % p


def poly_sub(a, b, p):
    m = max(len(a), len(b))
    a = list(a) + [0] * (m - len(a))
    b = list(b) + [0] * (m - len(b))
    return [(ai - bi) % p for ai, bi in zip(a, b)]


def deg(coeffs) -> int:
    d = len(coeffs) - 1
    while d > 0 and coeffs[d] == 0:
        d -= 1
    return d if any(coeffs) else -1


# ----------------------------------------------------------------------------
# Unsafe side: exact max prefix fiber by full enumeration.
# ----------------------------------------------------------------------------
def max_fiber(D, p: int, a: int, k: int):
    """Return (L, zbest, n_buckets, fiber_subsets) for agreement a, EXACT."""
    w = a - k
    buckets: dict[tuple, list] = {}
    for S in itertools.combinations(D, a):
        z = prefix_of(S, p, w)
        buckets.setdefault(z, []).append(S)
    zbest = max(buckets, key=lambda z: len(buckets[z]))
    L = len(buckets[zbest])
    return L, zbest, len(buckets), buckets[zbest]


def reconstruct_codewords(D, p, a, k, zbest, fiber):
    """Reconstruct c_M = U_z - ell_M for M in fiber; verify each gate.

    Returns (Uz_coeffs, Uz_evals, codewords) where codewords is a sorted list of
    coefficient tuples (length k).  Raises AssertionError on any gate failure.
    """
    w = a - k
    Uz = [0] * (a + 1)
    Uz[a] = 1
    for j in range(w):
        Uz[a - 1 - j] = zbest[j]
    Uz_evals = [poly_eval(Uz, x, p) for x in D]

    codewords = []
    for M in fiber:
        lM = ell(M, p)
        c = poly_sub(Uz, lM, p)
        assert deg(c) < k, ("deg", M, deg(c))
        c_evals = [poly_eval(c, x, p) for x in D]
        agree = sum(1 for i in range(len(D)) if c_evals[i] == Uz_evals[i])
        assert agree == a, ("agree", M, agree)
        aset = frozenset(D[i] for i in range(len(D)) if c_evals[i] == Uz_evals[i])
        assert aset == frozenset(M), ("aset", M)
        c = list(c) + [0] * (k - len(c))     # pad to length k
        codewords.append(tuple(c[:k]))
    assert len(set(codewords)) == len(fiber), "codewords not pairwise distinct"
    return Uz, Uz_evals, sorted(codewords)


# ----------------------------------------------------------------------------
# Safe side: all-words upper ledger cells.
# ----------------------------------------------------------------------------
def johnson(n, a, t):
    """Johnson/Cauchy-Schwarz packing bound; None if radius invalid (a^2<=nt)."""
    if a * a <= n * t:
        return None
    return (n * (a - t)) // (a * a - n * t)


def unique_decoding_cap(n, a, t):
    """Unique decoding: if 2a-n>t then at most ONE codeword in the list."""
    return 1 if 2 * a - n > t else None


def upper_ledger(n, a, t):
    cells = []
    u = unique_decoding_cap(n, a, t)
    if u is not None:
        cells.append(["unique_decoding", u])
    j = johnson(n, a, t)
    if j is not None:
        cells.append(["johnson_packing", j])
    best = min(c[1] for c in cells) if cells else None
    return best, cells


# ----------------------------------------------------------------------------
# Budget / margins.
# ----------------------------------------------------------------------------
def budget(p, k, lam):
    """B* = floor(2^-lam * p^k) via exact integer arithmetic (no float)."""
    return (p ** k) >> lam


def bits(x, y):
    return math.log2(x / y)


# ----------------------------------------------------------------------------
# Recompute the whole certificate from scratch.
# ----------------------------------------------------------------------------
def recompute():
    D = build_D(P, N)
    Q_list = P ** K
    B_star = budget(P, K, LAMBDA)

    # Unsafe headline.
    L0, zbest, nb0, fiber0 = max_fiber(D, P, A0, K)
    id_floor = -(-math.comb(N, A0) // P ** W0)   # ceil(C(n,a)/p^w)
    Uz, Uz_evals, codewords = reconstruct_codewords(D, P, A0, K, zbest, fiber0)

    # Safe headline.
    U1, cells1 = upper_ledger(N, A1, T)
    J1 = johnson(N, A1, T)
    uq1 = unique_decoding_cap(N, A1, T)
    a1_above_radius = A1 * A1 > N * T

    # a=12 activation of unique decoding.
    U12, cells12 = upper_ledger(N, 12, T)
    uq12 = unique_decoding_cap(N, 12, T)
    J12 = johnson(N, 12, T)

    # Companion pair 11 / 12.
    Lc, zc, nbc, fiberc = max_fiber(D, P, A_COMP0, K)
    Ucomp, cells_comp = upper_ledger(N, A_COMP1, T)

    codewords_blob = json.dumps(codewords, separators=(",", ":")).encode()
    codewords_sha = hashlib.sha256(codewords_blob).hexdigest()

    return {
        "D": D, "Q_list": Q_list, "B_star": B_star,
        "L0": L0, "zbest": list(zbest), "n_buckets_a0": nb0,
        "id_prefix_floor": id_floor, "excess": L0 - id_floor,
        "Uz": Uz, "Uz_evals": Uz_evals, "codewords": codewords,
        "codewords_sha256": codewords_sha,
        "U1": U1, "cells1": cells1, "J1": J1, "uq1": uq1,
        "a1_above_johnson_radius": a1_above_radius,
        "U12": U12, "uq12": uq12, "J12": J12,
        "Lc": Lc, "Ucomp": Ucomp, "cells_comp": cells_comp,
        "margin_unsafe": round(bits(L0, B_star), 3),
        "margin_safe": round(bits(B_star, U1), 3),
        "total_sep": round(bits(L0, U1), 3),
        "comp_total_sep": round(bits(Lc, Ucomp), 3),
    }


# ----------------------------------------------------------------------------
# Build the packet dict from the recomputed values.
# ----------------------------------------------------------------------------
def build_packet(r):
    n_johnson_radius = math.isqrt(N * T)
    return {
        "meta": {
            "artifact": "toy_complete_adjacent_list_staircase_v1",
            "title": "first in-repo complete two-sided adjacent staircase "
                     "certificate on the list route (enumerable toy row)",
            "schema": "frontier-adjacent row-packet (agents.md L135-152 style), "
                      "complete-toy variant",
            "companion_note": NOTE_REL,
            "companion_verifier": VERIFIER_REL,
            "source_draft": "gradient/g4 session draft (g4_note.md, "
                            "g4_certificate.py, g4_verify.py, g4_row_packet.json); "
                            "adapted to the repo frontier-adjacent schema, numbers "
                            "recomputed from scratch by the companion verifier",
            "date": "2026-07-07",
            "repo_base_commit": REPO_BASE,
            "status": "PROVED / COMPLETE / NO RESIDUAL (toy scale, list route)",
            "supports_labels": ["thm:finite", "def:staircase", "lem:integer-budget",
                                "lem:first-match-ledger", "prop:prefix-witness",
                                "rem:endpoint"],
            "supports_tasks": ["E1 (more finite adjacent examples)",
                               "Good-first-PR #6 (adjacent example)"],
            "object": "list-route base-code list-size numerator B_list(a); "
                      "adjacent staircase certificate of def:staircase",
            "label_hygiene": "cites only promoted grande_finale.tex labels; NOT the "
                             "grande_finale_work/*.tex working-draft labels "
                             "(e.g. thm:finite-next-compiler, prop:finite-packet-"
                             "unsafe), which are already absorbed into the promoted "
                             "tex under the labels above",
        },
        "thm_finite_instance": {
            "compiler_theorem": "thm:finite (grande_finale.tex L1917, 'adjacent "
                                "criterion from an explicit upper bound')",
            "hypothesis": "unsafe inequality at a0 (banked identity-prefix theorem, "
                          "prop:prefix-witness) AND a proved upper bound "
                          "B(a0+1) <= U(a0+1) <= B*",
            "instantiated_here": "unsafe L(10)=32 > B*=12 (enumerated prop:prefix-"
                                 "witness fiber) AND proved U(11)=7 <= B*=12 (Johnson "
                                 "packing, all words) -- both halves proved, list route",
            "conclusion": "first safe integer agreement = a0+1 = 11; delta*_C(eps*) "
                          "pinned to one integer step (closed-ball convention, "
                          "lem:integer-budget)",
            "significance": "first list-route instantiation of the certificate "
                            "condition of thm:finite in the repo (toy scale). "
                            "thm:finite is stated there for the four deployed rows; "
                            "its proof is row-generic via def:staircase + "
                            "lem:integer-budget. Here U is a single unconditional "
                            "Johnson cell, not the deployed first-match ledger of "
                            "lem:first-match-ledger; the deployed rows' U cell "
                            "remains open at prop:q-exact-target / prob:row-sharp-q.",
        },
        "scope_of_first_claim": {
            "claim": "First in-repo COMPLETE two-sided adjacent staircase "
                     "certificate on the LIST route whose unsafe side is a fully "
                     "ENUMERATED exact worst-received-word max prefix-fiber with "
                     "its entire maximal codeword list reconstructed and verified "
                     "(prop:prefix-witness realized end-to-end), paired with an "
                     "all-received-words safe cell, with ZERO residual/conditional "
                     "cells.",
            "not_claimed_unqualified_first": "This is NOT the repo's first "
                     "complete adjacent staircase certificate. Complete two-sided "
                     "adjacent certificates already exist on the LD_sw / "
                     "support-wise-MCA (line-decoding) route, paid by closed-form "
                     "or structural theorems, at toy through prize scale.",
            "prior_complete_adjacent_certificates_other_routes": [
                {"path": "experimental/data/certificates/adjacent-threshold-pins-"
                         "multirate/adjacent_threshold_pins.json",
                 "route": "LD_sw", "safe_side_paid_by": "tangent theorem "
                 "LD_sw=n-A+1 at r=R3=floor((n-k)/3)", "scale": "toy..prize (64 rows)"},
                {"path": "experimental/data/certificates/a426-two-core-exact-"
                         "threshold-v26/", "route": "LD_sw",
                 "safe_side_paid_by": "two-core closure theorem (r=R3+1)",
                 "scale": "deployed prime field"},
                {"path": "experimental/data/certificates/m1-a407-a408-residual-"
                         "design-threshold-v1/", "route": "LD_sw",
                 "safe_side_paid_by": "exact-support reduction / residual-design "
                 "theorem (status PROVED_ADJACENT_THRESHOLD_ROW)",
                 "scale": "deployed prime field"},
            ],
            "prior_list_route_status": "All prior LIST-route two-sided-shaped "
                     "packets leave the safe side OPEN/conditional "
                     "(cap25-v13-identity-frontier, frontier-adjacent/*.packet.json, "
                     "list-planted-arithmetic) or are lower-bound / closed-form-count "
                     "only; none enumerates the worst received word and reconstructs "
                     "its codeword list. The only prior list enumeration+dedup "
                     "artifact (l1-petal-fixed-excess/e15_worst_word_challenge.json) "
                     "is a toy tightness probe, explicitly not a safe-side proof and "
                     "not framed as an adjacent budget crossing.",
            "not_claimed_prize": "This does NOT close any deployed dense-frontier "
                     "row; those sit BELOW their Johnson radius where no universal "
                     "packing cell exists and prob:row-sharp-q is still required.",
        },
        "row": {
            "route": "list (base-code list size; K_list = k, no MCA conversion)",
            "F": P, "B": P, "beta_log2_B": round(math.log2(P), 6),
            "D": "mu_16 = F_17^x (full multiplicative group; n = p-1)",
            "n": N, "k": K, "rho": "1/2", "K_list": K,
            "min_distance_d": N - K + 1,
            "unique_decode_agreement_threshold": N - (N - K + 1 - 1) // 2,
        },
        "denominators": {
            "Q_list": {"value": r["Q_list"], "expr": "p^k = 17^8",
                       "desc": "toy sampler denominator = number of deg-<k "
                               "codewords; also the list-size budget denominator. "
                               "NOTE: this Q_list = p^k is a TOY list-denominator "
                               "convention, not the deployed rows' shared "
                               "Q = q_line = |field|^ext convention of "
                               "prop:q-exact-target"},
            "q_gen": {"value": P, "desc": "|B|, pigeonhole base for the "
                                          "identity-prefix construction"},
            "q_chal": {"value": "not protocol-bound (toy)"},
        },
        "target": {
            "epsilon_star": "2^-29",
            "epsilon_star_note": "non-cryptographic at toy scale by design; only "
                                 "the integer staircase L>B*>=U transfers, not the "
                                 "probabilistic reading",
            "B_star": {"value": r["B_star"],
                       "formula": "floor(eps* * Q_list) = floor(17^8 >> 29)"},
        },
        "agreement_interval": {
            "a0_unsafe": A0, "a0_plus_1_safe": A1,
            "endpoint_convention": "closed ball; agreement counts positions where "
                                   "the codeword EQUALS the received word; "
                                   "threshold '>= a' (equality positions counted)",
            "endpoint_radii_rem_endpoint": {
                "first_proved_unsafe_closed_grid_radius": "(n-a0)/n = 6/16 = 3/8",
                "largest_attained_safe_closed_grid_radius": "(n-a0-1)/n = 5/16",
                "real_supremum_caveat": "recorded as a real supremum over closed "
                    "integer balls, the safe-radius threshold sits at the upper "
                    "edge of the unit interval (3/8), NOT attained at the unsafe "
                    "endpoint; the convention must be printed with the proof "
                    "(rem:endpoint, grande_finale.tex L1929)",
            },
        },
        "unsafe_certificates": {
            "statement": "B_list(a0) >= L(a0) > B*",
            "L_a0": r["L0"], "B_star": r["B_star"],
            "inequality_holds": r["L0"] > r["B_star"],
            "value_is": "EXACT max prefix fiber = exact list-(>=a0) count for the "
                        "witness word U_z (prop:prefix-witness: the >=a0 list of "
                        "U_z is exactly {U_z - ell_M : M in Fib_w(z)})",
            "witness_prefix_z_star": r["zbest"],
            "witness_word_Uz_coeffs_low_to_high": r["Uz"],
            "witness_word_Uz_evals_on_D": r["Uz_evals"],
            "n_buckets": r["n_buckets_a0"],
            "codewords_sha256": r["codewords_sha256"],
            "status": "PAID_BY_EXACT_CERTIFICATE",
            "paid_by": "full enumeration of C(16,10)=8008 ten-subsets bucketed by "
                       "depth-2 signed elementary-symmetric prefix mod 17; heaviest "
                       "bucket 32 at null prefix z*=(0,0); all 32 codewords "
                       "c_M = X^10 - ell_M reconstructed and verified (deg<8, "
                       "agreement exactly 10, pairwise distinct)",
        },
        "safe_certificates": {
            "statement": "B_list(a0+1) <= U(a0+1) <= B*",
            "U_a0_plus_1": r["U1"], "B_star": r["B_star"],
            "inequality_holds": r["U1"] <= r["B_star"],
            "binding_cell": "johnson_packing",
            "johnson_value": r["J1"],
            "johnson_radius_check": {
                "a1_squared": A1 * A1, "n_times_t": N * T,
                "above_radius": r["a1_above_johnson_radius"],
                "johnson_radius_floor_sqrt_nt": n_johnson_radius,
                "note": "the safe cell EXISTS only because a0+1=11 is above the "
                        "Johnson radius sqrt(n(k-1))=sqrt(112)~=10.58; at a=10, "
                        "a^2=100 < n*t=112 and the bound is vacuous",
            },
            "unique_decoding_at_a1": {
                "two_a_minus_n": 2 * A1 - N, "t": T,
                "active": r["uq1"] is not None,
                "note": "inactive at a=11 (2*11-16=6 <= 7)",
            },
            "status": "PAID_BY_EXACT_CERTIFICATE",
            "paid_by": "unconditional Johnson/Cauchy-Schwarz packing bound for ALL "
                       "received words: distinct deg-<8 codewords agree on <= 7 "
                       "points, so L <= n(a-t)/(a^2-nt) = 16*4/(121-112) = 64/9, "
                       "hence L <= 7; no fiber, prefix, or genericity assumption",
        },
        "safe_cell_table": [
            {"cell": "paid_Q_prefix_boundary / row-sharp-Q", "value_at_a0_plus_1": 0,
             "status": "PAID_BY_THEOREM",
             "note": "zero at this row BY THEOREM: the all-words Johnson packing "
                     "cell caps the entire list at a0+1 (a0+1 is above the Johnson "
                     "radius), so under first-match the residual prefix-boundary "
                     "family is empty; no row-sharp Q input is consumed. Contrast "
                     "the deployed below-radius rows, where this cell is the open "
                     "prob:row-sharp-q."},
            {"cell": "paid_johnson_packing (all-words)", "value_at_a0_plus_1": r["J1"],
             "status": "PAID_BY_EXACT_CERTIFICATE"},
            {"cell": "paid_unique_decoding", "value_at_a0_plus_1": None,
             "status": "PAID_BY_EXACT_CERTIFICATE",
             "active_at_a": ">=12 (2a-n>k-1); inactive at a=11"},
            {"cell": "paid_tangent / paid_quotient / paid_extension",
             "value_at_a0_plus_1": 0, "status": "PAID_BY_THEOREM",
             "note": "zero additional under first-match: the Johnson cell already "
                     "caps the whole list for every word, so these cells contribute "
                     "nothing beyond it; the extension cell is moreover zero by the "
                     "generating-row rule (q_gen = q_line = p forces "
                     "Paid_ext^only = 0, "
                     "experimental/notes/thresholds/paid_ledger_functions.md)"},
            {"cell": "explicitly_named_residuals", "value_at_a0_plus_1": 0,
             "status": "PAID_BY_THEOREM",
             "note": "empty by the covering cell: the single unconditional all-words "
                     "Johnson bound leaves no unpaid branch; no "
                     "CONDITIONAL_ON_NAMED_INPUT anywhere in this ledger"},
        ],
        "paid_cells_summary": [
            {"cell": "lower_max_fiber", "status": "PAID_BY_EXACT_CERTIFICATE",
             "value": r["L0"]},
            {"cell": "upper_johnson_packing", "status": "PAID_BY_EXACT_CERTIFICATE",
             "value": r["J1"]},
            {"cell": "upper_unique_decoding", "status": "PAID_BY_EXACT_CERTIFICATE",
             "value": None, "active_at_a": ">=12"},
        ],
        "residual_cells": [],
        "residual_status": "No residual cells: the upper ledger at a0+1 is a single "
                           "unconditional all-received-words combinatorial cell "
                           "(Johnson packing); no CONDITIONAL_ON_NAMED_INPUT branch.",
        "deduplication_rule": "list route: codewords indexed by distinct m-subsets "
                      "M in Fib_w(z) are automatically distinct (ell_M = U_z - c_M "
                      "recovers M as its root set); verified len(set(codewords))=32. "
                      "No first-match slope collapse needed (that is an MCA-route "
                      "device).",
        "margins": {
            "unsafe_bits": r["margin_unsafe"], "safe_bits": r["margin_safe"],
            "total_separation_bits": r["total_sep"],
            "note": "unsafe = log2(L(a0)/B*), safe = log2(B*/U(a0+1)), total = "
                    "log2(L(a0)/U(a0+1)) = unsafe + safe",
        },
        "floor_vs_truth": {
            "id_prefix_average_floor": r["id_prefix_floor"],
            "id_prefix_floor_formula": "ceil(C(16,10)/17^2) = ceil(8008/289)",
            "exact_max_fiber": r["L0"],
            "null_prefix_excess": r["excess"],
            "note": "the deployed L(a)=ceil(C(n,a)/p^w) staircase is an AVERAGE "
                    "floor, not the true worst word; here the exact heaviest fiber "
                    "(32) exceeds the average floor (28) by 4 (null-prefix excess). "
                    "Small independent datum on floor-vs-truth gaps.",
        },
        "companion_pair": {
            "a0_unsafe": A_COMP0, "a0_plus_1_safe": A_COMP1,
            "L_a0": r["Lc"], "U_a0_plus_1": r["Ucomp"],
            "budget_window_B_star": [r["Ucomp"], r["Lc"] - 1],
            "safe_cell": "unique_decoding (2*12-16=8 > 7)",
            "safe_cell_johnson_also": r["J12"],
            "total_separation_bits": r["comp_total_sep"],
            "note": "recorded, non-headline: a SECOND adjacent pair on the same row "
                    "whose safe side is the unique-decoding cell (U=1) rather than "
                    "Johnson. Its budget window {1,2} needs a smaller eps* than the "
                    "headline B*=12; tighter margins, trivial safe cell.",
        },
        "honest_gap": [
            {"id": "no-hard-Q-cell", "status": "SCOPE",
             "claim": "The safe side here is a WORD-INDEPENDENT packing cell that "
                      "exists ONLY ABOVE the Johnson radius (a^2 > n(k-1)). The four "
                      "deployed rows sit far BELOW their Johnson radius, where no "
                      "universal packing cell exists and the safe side genuinely "
                      "requires prob:row-sharp-q (the row-sharp Q max-fiber atom). "
                      "Per prop:q-exact-target (grande_finale.tex L1956), that open "
                      "cell is a prefix-boundary max-fiber at w = a+ - K = 67471 "
                      "(KoalaBear) / 67447 (Mersenne-31) whose exact constants must "
                      "fit the printed row margins (22.20/22.01/3.26/3.07 bits). "
                      "This toy validates the certificate GRAMMAR end-to-end; it "
                      "does NOT exercise that hard cell."},
            {"id": "toy-epsilon", "status": "SCOPE",
             "claim": "eps* = 2^-29 is non-cryptographic at toy scale (F_17 is far "
                      "too small for eps* to mean protocol soundness). Only the "
                      "integer staircase L > B* >= U transfers; the probabilistic "
                      "reading does not. Deployed rows use eps* in {2^-128, 2^-100}."},
            {"id": "floor-is-not-truth", "status": "DATUM",
             "claim": "The identity-prefix average floor ceil(C(n,a)/p^w)=28 is "
                      "loose; the exact worst-word fiber is 32. The certificate uses "
                      "the EXACT enumerated 32, confirming the deployed L(a) formula "
                      "is a floor, not the true B_list."},
        ],
        "non_claims": [
            "does not close any deployed dense-frontier adjacent row",
            "does not prove or bound row-sharp Q (prob:row-sharp-q); it sidesteps "
            "it via the above-Johnson-radius packing cell",
            "does not claim prize-metric movement; experimental grammar/template "
            "plus honest-gap documentation only",
            "does not claim to be the first complete adjacent certificate "
            "unqualified (prior LD_sw-route complete certs exist; see "
            "scope_of_first_claim)",
        ],
        "witness": {
            "D": r["D"],
            "z_star": r["zbest"],
            "Uz_coeffs_low_to_high": r["Uz"],
            "Uz_evals_on_D": r["Uz_evals"],
            "codewords_deg_lt_k_low_to_high": r["codewords"],
            "codewords_sha256": r["codewords_sha256"],
        },
        "replay": "python3 " + VERIFIER_REL + "  (zero-arg: recompute from "
                  "scratch, cross-check this JSON field-by-field, tamper "
                  "self-tests, exit 0 = PASS). --emit regenerates this file.",
        "output_standard": {
            "input_parameters": {"p": P, "n": N, "k": K, "rho": "1/2",
                                 "lambda": LAMBDA, "route": "list"},
            "object_checked": "adjacent staircase L(a0)>B*>=U(a0+1) for the list "
                              "numerator, def:staircase",
            "result": "L(10)=%d > B*=%d >= U(11)=%d" % (r["L0"], r["B_star"], r["U1"]),
            "certificate": "exact enumeration + reconstruction (unsafe) + Johnson "
                           "packing (safe); reproducibility: this verifier, stdlib "
                           "python3, deterministic",
            "supports_id": "def:staircase / prop:prefix-witness / task E1 / GFP #6",
            "verdict": "PROVED (toy scale, list route, complete/no residual)",
        },
    }


# ----------------------------------------------------------------------------
# Cross-check the shipped JSON against recomputed values.
# ----------------------------------------------------------------------------
def _num_fields(r):
    """Flat list of (name, recomputed_value) numeric fields the JSON must match."""
    return [
        ("row.n", N), ("row.k", K), ("row.min_distance_d", N - K + 1),
        ("denominators.Q_list", r["Q_list"]),
        ("target.B_star", r["B_star"]),
        ("agreement_interval.a0_unsafe", A0),
        ("agreement_interval.a0_plus_1_safe", A1),
        ("unsafe.L_a0", r["L0"]),
        ("unsafe.n_buckets", r["n_buckets_a0"]),
        ("unsafe.z_star", tuple(r["zbest"])),
        ("safe.U_a0_plus_1", r["U1"]),
        ("safe.johnson", r["J1"]),
        ("safe.a1_sq", A1 * A1), ("safe.n_t", N * T),
        ("margins.unsafe", r["margin_unsafe"]),
        ("margins.safe", r["margin_safe"]),
        ("margins.total", r["total_sep"]),
        ("floor.id_floor", r["id_prefix_floor"]),
        ("floor.excess", r["excess"]),
        ("companion.L", r["Lc"]), ("companion.U", r["Ucomp"]),
        ("companion.total", r["comp_total_sep"]),
        ("codewords_sha256", r["codewords_sha256"]),
    ]


def _packet_value(pkt, key):
    """Pull the field named `key` out of a packet dict."""
    m = {
        "row.n": lambda p: p["row"]["n"],
        "row.k": lambda p: p["row"]["k"],
        "row.min_distance_d": lambda p: p["row"]["min_distance_d"],
        "denominators.Q_list": lambda p: p["denominators"]["Q_list"]["value"],
        "target.B_star": lambda p: p["target"]["B_star"]["value"],
        "agreement_interval.a0_unsafe": lambda p: p["agreement_interval"]["a0_unsafe"],
        "agreement_interval.a0_plus_1_safe": lambda p: p["agreement_interval"]["a0_plus_1_safe"],
        "unsafe.L_a0": lambda p: p["unsafe_certificates"]["L_a0"],
        "unsafe.n_buckets": lambda p: p["unsafe_certificates"]["n_buckets"],
        "unsafe.z_star": lambda p: tuple(p["unsafe_certificates"]["witness_prefix_z_star"]),
        "safe.U_a0_plus_1": lambda p: p["safe_certificates"]["U_a0_plus_1"],
        "safe.johnson": lambda p: p["safe_certificates"]["johnson_value"],
        "safe.a1_sq": lambda p: p["safe_certificates"]["johnson_radius_check"]["a1_squared"],
        "safe.n_t": lambda p: p["safe_certificates"]["johnson_radius_check"]["n_times_t"],
        "margins.unsafe": lambda p: p["margins"]["unsafe_bits"],
        "margins.safe": lambda p: p["margins"]["safe_bits"],
        "margins.total": lambda p: p["margins"]["total_separation_bits"],
        "floor.id_floor": lambda p: p["floor_vs_truth"]["id_prefix_average_floor"],
        "floor.excess": lambda p: p["floor_vs_truth"]["null_prefix_excess"],
        "companion.L": lambda p: p["companion_pair"]["L_a0"],
        "companion.U": lambda p: p["companion_pair"]["U_a0_plus_1"],
        "companion.total": lambda p: p["companion_pair"]["total_separation_bits"],
        "codewords_sha256": lambda p: p["witness"]["codewords_sha256"],
    }
    return m[key](pkt)


def cross_check(pkt, r):
    diffs = []
    for name, val in _num_fields(r):
        got = _packet_value(pkt, name)
        if got != val:
            diffs.append(f"{name}: json={got!r} != recomputed={val!r}")
    return diffs


def witness_hash_binding(pkt, r):
    """Hash the SHIPPED witness codeword array and bind it to BOTH shipped
    sha256 pointers (witness block + unsafe-certificate block) and to the
    recomputed hash.  Closes the pointer-vs-array gap: corrupting a codeword
    coefficient while leaving the sha256 pointers untouched now fails."""
    arr = pkt["witness"]["codewords_deg_lt_k_low_to_high"]
    blob = json.dumps(arr, separators=(",", ":")).encode()
    h = hashlib.sha256(blob).hexdigest()
    ok = (h == pkt["witness"]["codewords_sha256"]
          == pkt["unsafe_certificates"]["codewords_sha256"]
          == r["codewords_sha256"])
    return ok, h


# ----------------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------------
def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def emit(r):
    pkt = build_packet(r)
    path = repo_root() / CERT_REL
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(pkt, f, indent=1)
        f.write("\n")
    print(f"wrote {CERT_REL}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true",
                    help="(re)generate the packet JSON and exit")
    args = ap.parse_args()

    print("=" * 78)
    print("Toy complete adjacent LIST staircase certificate -- verifier")
    print("row: F_17, D=mu_16, n=16, k=8, rho=1/2, list route; eps*=2^-29")
    print("=" * 78)

    r = recompute()

    if args.emit:
        emit(r)
        return 0

    gates = []

    # G1 domain
    ok = (len(r["D"]) == N and r["D"] == sorted(set(r["D"]))
          and r["D"] == list(range(1, N + 1)))
    gates.append(("G1 domain D=mu_16=F_17^x (n=16, distinct)", ok,
                  f"D={r['D']}"))

    # G2 budget
    ok = (r["Q_list"] == 17 ** 8 == 6975757441 and r["B_star"] == 12)
    gates.append(("G2 budget Q=17^8, B*=floor(2^-29 Q)=12", ok,
                  f"Q={r['Q_list']}, B*={r['B_star']}"))

    # G3 unsafe max fiber
    ok = (r["L0"] == 32 and tuple(r["zbest"]) == (0, 0)
          and r["n_buckets_a0"] == 289 and r["id_prefix_floor"] == 28
          and r["excess"] == 4)
    gates.append(("G3 unsafe: max fiber 32 at z*=(0,0), 289 buckets, floor 28", ok,
                  f"L(10)={r['L0']}, z*={r['zbest']}, buckets={r['n_buckets_a0']}, "
                  f"idfloor={r['id_prefix_floor']}, excess={r['excess']}"))

    # G4 witness reconstruction (32 codewords deg<8, agreement 10, distinct)
    ok = (len(r["codewords"]) == 32
          and all(deg(list(c)) < K for c in r["codewords"])
          and len(set(r["codewords"])) == 32
          and r["Uz"] == [0] * 10 + [1])
    gates.append(("G4 witness: 32 codewords c_M=X^10-ell_M (deg<8, agree=10, distinct)",
                  ok, f"|codewords|={len(r['codewords'])}, "
                      f"sha={r['codewords_sha256'][:16]}..., Uz=X^10"))

    # G5 unsafe inequality
    ok = r["L0"] > r["B_star"]
    gates.append(("G5 unsafe inequality L(10)=32 > B*=12", ok,
                  f"{r['L0']} > {r['B_star']} = {ok}"))

    # G6 safe cell Johnson, radius valid, unique-decoding inactive
    ok = (r["J1"] == 7 and r["U1"] == 7 and r["a1_above_johnson_radius"]
          and A1 * A1 == 121 and N * T == 112 and r["uq1"] is None)
    gates.append(("G6 safe: Johnson J(11)=7 (a^2=121>nt=112), unique-dec inactive",
                  ok, f"J(11)={r['J1']}, U(11)={r['U1']}, "
                      f"121>112={r['a1_above_johnson_radius']}, uq11={r['uq1']}"))

    # G7 safe inequality
    ok = r["U1"] <= r["B_star"]
    gates.append(("G7 safe inequality U(11)=7 <= B*=12", ok,
                  f"{r['U1']} <= {r['B_star']} = {ok}"))

    # G8 unique-decoding activation at a=12
    ok = (r["uq12"] == 1 and r["U12"] == 1 and r["J12"] == 2)
    gates.append(("G8 unique decoding activates at a=12 (U(12)=1; Johnson 2)", ok,
                  f"uq(12)={r['uq12']}, U(12)={r['U12']}, J(12)={r['J12']}"))

    # G9 margins to 3 decimals
    ok = (r["margin_unsafe"] == 1.415 and r["margin_safe"] == 0.778
          and r["total_sep"] == 2.193)
    gates.append(("G9 margins: unsafe 1.415, safe 0.778, total 2.193 bits", ok,
                  f"{r['margin_unsafe']}/{r['margin_safe']}/{r['total_sep']}"))

    # G10 companion
    ok = (r["Lc"] == 3 and r["Ucomp"] == 1 and r["comp_total_sep"] == 1.585)
    gates.append(("G10 companion 11/12: L(11)=3 > {1,2} >= U(12)=1 (sep 1.585)", ok,
                  f"L(11)={r['Lc']}, U(12)={r['Ucomp']}, sep={r['comp_total_sep']}"))

    # G10b endpoint radii (rem:endpoint): unsafe (n-a0)/n=6/16=3/8, safe 5/16
    r_unsafe = math.gcd(N - A0, N)
    r_safe = math.gcd(N - A1, N)
    ok = ((N - A0, N) == (6, 16) and ((N - A0) // r_unsafe, N // r_unsafe) == (3, 8)
          and (N - A1, N) == (5, 16))
    gates.append(("G10b endpoint radii: unsafe 6/16=3/8, safe 5/16 (rem:endpoint)",
                  ok, f"first unsafe grid radius {N-A0}/{N}=3/8, "
                      f"largest safe grid radius {N-A1}/{N}"))

    # G11 JSON cross-check
    cert_path = repo_root() / CERT_REL
    if not cert_path.exists():
        gates.append(("G11 JSON cross-check", False,
                      f"shipped packet not found at {CERT_REL} (run --emit first)"))
        pkt = None
    else:
        pkt = json.loads(cert_path.read_text())
        diffs = cross_check(pkt, r)
        gates.append(("G11 shipped JSON matches recompute (every numeric field)",
                      not diffs, "all fields match" if not diffs
                      else "; ".join(diffs)))

    # G12 witness-array hash binding: the SHIPPED codeword array must hash to
    # BOTH shipped sha256 pointers AND the recomputed hash (closes the
    # pointer-vs-array gap: a corrupted array with untouched pointers fails).
    if pkt is not None:
        okh, hgot = witness_hash_binding(pkt, r)
        gates.append(("G12 shipped witness array sha256 == both shipped pointers "
                      "== recompute", okh,
                      f"sha256(shipped array)={hgot[:16]}...; equals witness "
                      f"pointer, unsafe-cert pointer, recompute: {okh}"))
    else:
        gates.append(("G12 witness-array hash binding", False,
                      "no shipped JSON (run --emit first)"))

    # Tamper self-tests: mutate a loaded copy and confirm the JSON-facing gates
    # (field cross-check + witness hash binding) CATCH it.
    tampers = []
    if pkt is not None:
        def detected(bad):
            return bool(cross_check(bad, r)) or not witness_hash_binding(bad, r)[0]
        for label, mut in [
            ("T1 corrupt B_star 12->13", lambda p: p["target"]["B_star"].__setitem__("value", 13)),
            ("T2 corrupt L(a0) 32->31", lambda p: p["unsafe_certificates"].__setitem__("L_a0", 31)),
            ("T3 corrupt Johnson 7->8", lambda p: p["safe_certificates"].__setitem__("johnson_value", 8)),
            ("T5 corrupt witness codeword coeff [0][0] (sha pointers untouched)",
             lambda p: p["witness"]["codewords_deg_lt_k_low_to_high"][0].__setitem__(
                 0, (p["witness"]["codewords_deg_lt_k_low_to_high"][0][0] + 1) % 17)),
        ]:
            bad = json.loads(json.dumps(pkt))
            mut(bad)
            tampers.append((label, detected(bad)))
    else:
        tampers.append(("T1-T3,T5 (skipped: no shipped JSON)", False))

    # Structural tamper: the Johnson guard must REJECT a=10 (below radius).
    guard_ok = (johnson(N, A0, T) is None and A0 * A0 < N * T)
    tampers.append(("T4 Johnson radius guard rejects a=10 (a^2=100<112)", guard_ok))

    print()
    all_ok = True
    for label, ok, detail in gates:
        all_ok = all_ok and ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        print(f"         {detail}")
    print("  --- tamper self-tests (each must be CAUGHT) ---")
    for label, caught in tampers:
        all_ok = all_ok and caught
        print(f"  [{'CAUGHT' if caught else 'MISSED'}] {label}")

    print("=" * 78)
    if all_ok:
        print("RESULT: ALL GATES PASS  |  L(10)=32 > B*=12 >= U(11)=7  |  "
              "COMPLETE / NO RESIDUAL (toy list row)")
    else:
        print("RESULT: FAILURE")
    print("=" * 78)
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
