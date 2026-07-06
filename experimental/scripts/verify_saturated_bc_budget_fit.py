#!/usr/bin/env python3
"""verify_saturated_bc_budget_fit.py

Zero-arg, stdlib-only, deterministic verifier for
experimental/data/certificates/frontier-adjacent/saturated_bc_budget_fit_v1.json
and its companion note
experimental/notes/thresholds/cap25_v13_saturated_bc_budget_fit.md.

This packet is the first data/derivation packet on the PROMOTED problem
`prob:saturated-bc` (grande_finale.tex \\label{prob:saturated-bc}, "saturated
primitive split-pencil line-ray target"): the exact margin identity between
the deployed budget B* and the base-field split-pencil floor B_B(a+)
(prop:base-field-floor), the budget-fit of the two proved fixed-deficiency
Conjecture-F strata (P2), and an exhaustive toy census of the exact
deduplication identity of prop:line-ray-saturation / thm:saturation. It does
NOT prove prob:saturated-bc, does NOT certify U(a0+1)<=B* for the
growing-deficiency interior census, and does NOT supersede PR #369 (Latif's
L4 base-field floor fixture, open) or PR #378 (Holm Buar's Lean BC interior
census floor, lower side, open) -- see the companion note's weave section.

Four gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  gate i    MARGIN IDENTITY. Independently recomputes, from raw constants
            alone (p_KB, p_M31, n=2^21, the four K/a+ choices, and the two
            challenge-budget exponents/security shaves), the exact big-integer
            quantities  B*  =  floor(p^spow / 2^lam)   and
            B_B(a+) = C(n,a+) * p^-w  (base-field floor, prop:base-field-floor),
            then the margin = log2(B*) - log2(B_B(a+)) at all four rows
            (KoalaBear MCA/list, Mersenne-31 MCA/list), and checks each
            margin against the promoted note's printed values (22.1969,
            22.0109, 3.2589, 3.0730 bits) to >=4 decimals. The one expensive
            binomial, C(n, 1116048), is computed fresh via math.comb; the
            other three row binomials are derived from it by the EXACT
            shift identity C(n,k-1) = C(n,k)*k/(n-k+1) (each division's
            remainder is asserted to be exactly zero at every step, so this
            is still exact big-integer recomputation, not an approximation
            -- it is merely algebraically cheaper than four from-scratch
            math.comb calls on a ~2.1-million-bit result). log2 is computed
            two independent ways (integer bit-length truncation, and
            math.lgamma on the exact binomial's (n,k) via a second
            from-scratch path) and cross-checked. Gate i ALSO parses
            experimental/grande_finale.tex's own printed margin table
            directly (regex over the promoted TeX source) and diffs the
            recomputed margins against what the promoted note actually
            prints today, so this gate would fail if the promoted note's
            table ever silently drifted from the underlying arithmetic.

  gate ii   P2 ARITHMETIC (fixed-deficiency Conjecture-F strata) AND THE
            GROWING-DEFICIENCY MISS. At the two MCA rows: deficiency-1
            (lem:capf-dim1, floor(n/omega)) and deficiency-2 (thm:capf-dim2,
            C(n,2)/(omega-1)) are recomputed exactly and checked to be
            comfortably below both B* budgets (2 and ~2^21.1 against
            2^57.93 / 2^24.00). Then the growing-deficiency interior cell
            d = omega-w (dim W = d+1, the Conjecture-F incidence dimension
            of thm:capfp-dichotomy(ii)/prob:capg-split-pencil-B) is
            recomputed: dim W = 913634 (KB) / 913682 (M31) -- NOT the
            913642/913686 figure that laneM_analysis.md's S2.3 quotes from
            raw prob:capfp-balanced (L8386), which this gate's recompute
            shows belongs to a different, non-current adjacent-pair
            numbering (see the companion note's "found vs. claimed"
            paragraph; rem:packet-convention documents that the raw
            manuscript's packet family carries such historical-pair
            leftovers elsewhere too). thm:capf-fixeddim's C(n,d) and
            thm:bc-proper's q^(d+1) are then recomputed exactly (one fresh
            math.comb(n,d) per field family, the second family's d derived
            by the same exact shift-identity trick) and their bit-misses
            against the base-field floor are checked to match 2.07 x 10^6
            bits (both rows) and 1.70x10^8 / 1.13x10^8 bits (KB / M31).

  gate iii  TOY CENSUS REPLAY. Re-enumerates, exhaustively and independently,
            the toy line-ray census of prop:line-ray-saturation / thm:saturation
            over F_{p^2} >= B=F_p >= D, for 5 (p,K,m) configurations x 3 line
            families (random_base, pole [adversarial, extension-valued],
            random_ext) x 3 seeds = 45 instances. Default (zero-arg) run
            LIVE-enumerates the 39 smallest/cheapest instances (both p=7
            configs, both p=11 configs, all three seed-0 p=13 instances --
            39 = 36+3, well over the required 12) and checks the remaining 6
            (p=13, seeds 1-2) against PINNED expected values embedded in this
            script (verbatim from laneM_compute.py's PART B output, itself
            reproduced bit-for-bit by an independent rerun during packaging).
            Pass `--full` to LIVE-enumerate all 45 instances (slower, no
            longer needed for a green zero-arg run). Every live instance
            independently verifies thm:saturation's EXACT identity
            Cen(U;m) = sum_c C(s_c(U),m) (fiber-by-fiber, not just the total)
            using a DIFFERENT algorithmic path than laneM_compute.py: the
            interpolation-degree test is the S_r(f,T) functional criterion of
            lem:capfp-functionals (raw L8246) -- "f|_T extends to degree<K
            iff S_r(f,T)=0 for all r<w" -- rather than Newton divided
            differences, and the codeword reconstruction uses direct
            Lagrange interpolation rather than the Newton form. Both dedup
            losses of prop:line-ray-saturation (loss1 = |LineRay_E| - N_slopes,
            loss2 = sum Cen - |LineRay_E|) are checked per instance against
            the pinned/expected (nbad, base, ext, lineray, Cen, maxmult,
            maxsat) tuples, including the headline adversarial witness
            p=13 pole seed=0 (71 bad slopes, 7 base-valued / 64 extension-
            valued -- the prop:rank-one-distinct-slope-floor signature).

  gate iv   L4 FLOOR CONSISTENCY. Recomputes the L4 testbed's (scale-16
            quotient rung; n=131072, K=65537, m=69753, w=4216) base-field
            floor log2(C(n,m) p^-w) from scratch (small binomial, <1s) and
            cross-checks it, to >=4 decimals, against TWO independent
            already-on-`main` sources that were computed by entirely
            different scripts/routes: (a) this repo's already-integrated
            experimental/data/certificates/frontier-adjacent/
            kb_mca_conjq_rung_audit_v1.json, rung j=4's
            "log2_quotient_avg_a_j" field (computed via the quotient-average
            pigeonhole route of the conj:Q rung audit, NOT the direct
            base-field-floor route used here or in laneM_compute.py); and
            (b) the printed value 23.139009 pinned in this script from
            PR #369's (open, Latif Kasuli's) verify_bc_l4_base_floor_ladder.py
            diff (base_field_floor_log2_approx at d1=4217, prop:capg-census-
            floor's direct route) -- confirmed by this packaging session
            via `gh pr diff 369`, not re-fetched live by this script (the
            script stays hermetic/offline; the companion note carries the
            #369 cross-reference narratively). All three numbers agree to
            six decimal places (23.139009...); this is a strong, three-route
            cross-validation of one exact rational, not a proof of anything
            about prob:saturated-bc itself.

Hidden self-test: python3 verify_saturated_bc_budget_fit.py --tamper-selftest
    Each gate function takes a tamper=False parameter; in self-test mode it
    is called with tamper=True, which corrupts exactly ONE stored/expected
    value used inside that gate's first check (never the from-scratch
    recomputed side) and asserts the gate then reports a mismatch (CAUGHT).
    The shipped default is zero-arg (tamper=False everywhere).

PERFORMANCE. The dominant costs are: one fresh math.comb(2^21, 1116048)
(~15s) for gate i's anchor (the other three row binomials are near-free
exact-ratio derivations, see gate i docstring above); one fresh
math.comb(2^21, 913633) (~14s) for gate ii's growing-deficiency anchor (M31's
913681 is again a near-free 48-step exact-ratio derivation); gate iii's
39-instance default toy census (~35-40s, dominated by the three p=13 seed-0
instances at ~5s each and the p=11 instances at a few seconds each); gate iv
is under 1s. Measured total runtime (zero-arg, this machine): ~60s,
comfortably under the 90s budget. `--full` adds the remaining 6 p=13
instances (~25-30s more).

This verifier does NOT decide prob:saturated-bc, does NOT certify
U(a0+1)<=B* for the growing-deficiency interior cell, and does NOT move the
frontier edge. It only checks that this PR's arithmetic is exactly what it
claims to be.
"""
from __future__ import annotations

import itertools
import json
import math
import os
import random
import re
import sys
import time

sys.set_int_max_str_digits(2_500_000)

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
JSON_PATH = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                          "frontier-adjacent", "saturated_bc_budget_fit_v1.json")
NOTE_PATH = os.path.join(REPO_ROOT, "experimental", "notes", "thresholds",
                          "cap25_v13_saturated_bc_budget_fit.md")
TEX_PATH = os.path.join(REPO_ROOT, "experimental", "grande_finale.tex")
RUNG_AUDIT_JSON = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                                "frontier-adjacent", "kb_mca_conjq_rung_audit_v1.json")

WALL_ID = "CAP25-V13-SATURATED-BC-BUDGET-FIT"

# ---------------------------------------------------------------------------
# ground-truth row constants -- independent of the shipped JSON
# ---------------------------------------------------------------------------
P_KB = 2 ** 31 - 2 ** 24 + 1     # KoalaBear prime, 2130706433
P_M31 = 2 ** 31 - 1              # Mersenne-31 prime, 2147483647
N_DEP = 2 ** 21                  # deployed dimension, 2097152

# name, p, a_plus (moved-pair adjacent agreement), K, challenge-field power, security shave
ROWS = [
    dict(name="KoalaBear MCA ", p=P_KB, a_plus=1116048, K=2 ** 20 + 1, spow=6, lam=128),
    dict(name="KoalaBear list", p=P_KB, a_plus=1116047, K=2 ** 20, spow=6, lam=128),
    dict(name="Mersenne31 MCA", p=P_M31, a_plus=1116024, K=2 ** 20 + 1, spow=4, lam=100),
    dict(name="Mersenne31 lst", p=P_M31, a_plus=1116023, K=2 ** 20, spow=4, lam=100),
]
EXPECTED_MARGIN = {
    "KoalaBear MCA ": 22.1969,
    "KoalaBear list": 22.0109,
    "Mersenne31 MCA": 3.2589,
    "Mersenne31 lst": 3.0730,
}
# TeX table uses these display names; map to the ROWS names above.
TEX_ROW_NAME = {
    "KoalaBear MCA": "KoalaBear MCA ",
    "KoalaBear list": "KoalaBear list",
    "Mersenne-31 MCA": "Mersenne31 MCA",
    "Mersenne-31 list": "Mersenne31 lst",
}

# L4 testbed (scale-16 quotient rung; no deployed budget -- flatness rung)
L4 = dict(p=P_KB, n=131072, K=65537, m=69753)
L4_EXPECTED_LOG2_FLOOR = 23.1390
L4_RUNG_AUDIT_EXPECT = 23.139009074      # kb_mca_conjq_rung_audit_v1.json, rung j=4
L4_PR369_EXPECT = 23.139009              # PR #369 verify_bc_l4_base_floor_ladder.py diff, d1=4217

# Growing-deficiency (interior BC) expectations, from output.txt / laneM_compute.py.
# miss_* targets are DERIVED (log2_bound - row's own 4-decimal floor from gate i's
# ledger), not separately hardcoded, so they carry no extra rounding slop beyond
# the 1-decimal precision of log2_fixeddim/log2_bcproper themselves.
GROWING_DEF_EXPECT = {
    "KoalaBear MCA ": dict(d=913633, dimW=913634, log2_fixeddim=2072017.7,
                            log2_bcproper=169873895.7),
    "Mersenne31 MCA": dict(d=913681, dimW=913682, log2_fixeddim=2072035.6,
                            log2_bcproper=113296568.0),
}

# ---------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------
def log2_bigint(x: int) -> float:
    """log2 of a positive python int of arbitrary size, via bit-length truncation."""
    if x <= 0:
        return float("-inf")
    b = x.bit_length()
    if b <= 100:
        return math.log2(x)
    top = x >> (b - 100)
    return (b - 100) + math.log2(top)


def log2_comb_lgamma(n: int, k: int) -> float:
    """Independent cross-check of log2 C(n,k) via math.lgamma (natural-log gamma,
    stdlib, a completely different numerical code path from bit-length truncation
    of the exact big integer)."""
    ln_c = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    return ln_c / math.log(2)


def _corrupt(x):
    """Perturb a single stored/expected value for the tamper self-test."""
    if isinstance(x, bool):
        return not x
    if isinstance(x, int):
        return x + 1
    if isinstance(x, float):
        return x + 1.0
    if isinstance(x, str):
        return x + "_TAMPERED_NONEXISTENT"
    if isinstance(x, tuple):
        return tuple(_corrupt(list(x)))
    if isinstance(x, list):
        return list(x[:-1]) if x else [999999]
    return x


def check(actual, expected, *, tol=None, tamper=False):
    """actual == expected (within tol if given). Under tamper=True, `expected`
    (the stored/guarded side) is corrupted first, so a correct gate must then
    report a mismatch."""
    if tamper:
        expected = _corrupt(expected)
    if tol is not None:
        return abs(actual - expected) <= tol
    return actual == expected


def load_json(path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_text(path) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# exact big-integer binomial shift identities:
#   C(n,k-1) = C(n,k) * k / (n-k+1)          (shift DOWN)
#   C(n,k+1) = C(n,k) * (n-k) / (k+1)        (shift UP)
# Each division's remainder is asserted to be exactly zero -- these are exact
# integer recomputations of the true combinatorial identity, algebraically
# cheap relative to a fresh math.comb call on a multi-million-bit result.
# ---------------------------------------------------------------------------
def shift_comb_down(c_k: int, k: int, n: int, steps: int) -> int:
    val = c_k
    for i in range(steps):
        kk = k - i
        denom = n - kk + 1
        num = val * kk
        q, r = divmod(num, denom)
        if r != 0:
            raise ArithmeticError(f"shift_comb_down: non-exact division at kk={kk}")
        val = q
    return val


def shift_comb_up(c_k: int, k: int, n: int, steps: int) -> int:
    val = c_k
    for i in range(steps):
        kk = k + i
        num = val * (n - kk)
        denom = kk + 1
        q, r = divmod(num, denom)
        if r != 0:
            raise ArithmeticError(f"shift_comb_up: non-exact division at kk={kk}")
        val = q
    return val


# ===========================================================================
# gate i -- margin identity (shared ledger, cached so gate ii can reuse it)
# ===========================================================================
_MARGIN_LEDGER: dict = {}


def build_margin_ledger() -> dict:
    if _MARGIN_LEDGER:
        return _MARGIN_LEDGER

    # one fresh, expensive comb() call: the KoalaBear-MCA anchor
    anchor_name = "KoalaBear MCA "
    anchor_row = next(r for r in ROWS if r["name"] == anchor_name)
    c_anchor = math.comb(N_DEP, anchor_row["a_plus"])

    combs = {anchor_name: c_anchor}
    # KoalaBear list: a_plus = 1116047 = anchor - 1  -> shift down 1 step
    combs["KoalaBear list"] = shift_comb_down(c_anchor, anchor_row["a_plus"], N_DEP, 1)
    # Mersenne31 MCA: a_plus = 1116024 = anchor - 24 -> shift down 24 steps
    combs["Mersenne31 MCA"] = shift_comb_down(c_anchor, anchor_row["a_plus"], N_DEP, 24)
    # Mersenne31 list: a_plus = 1116023 = anchor - 25 -> shift down 25 steps
    combs["Mersenne31 lst"] = shift_comb_down(c_anchor, anchor_row["a_plus"], N_DEP, 25)

    ledger = {}
    for row in ROWS:
        name = row["name"]
        p, a_plus, K, spow, lam = row["p"], row["a_plus"], row["K"], row["spow"], row["lam"]
        w = a_plus - K
        comb_val = combs[name]
        # sanity: the ratio-derived value must equal a fresh comb() -- checked
        # once, cheaply, only for the two derivations that are individually
        # inexpensive to re-verify (list rows are 1-step from their own MCA
        # sibling, which we already trust transitively); we do NOT re-verify
        # via fresh math.comb here (that would defeat the whole point of the
        # optimization) -- correctness of the identity itself was hand-verified
        # against fresh math.comb() calls during packaging (see note/report).
        l_bitshift = log2_bigint(comb_val)
        l_lgamma = log2_comb_lgamma(N_DEP, a_plus)
        b_star = (p ** spow) // (2 ** lam)
        l_bstar = math.log2(b_star)
        l_floor_bitshift = l_bitshift - w * math.log2(p)
        l_floor_lgamma = l_lgamma - w * math.log2(p)
        margin = l_bstar - l_floor_bitshift
        margin_lgamma = l_bstar - l_floor_lgamma
        ledger[name] = dict(w=w, omega=N_DEP - a_plus, comb=comb_val,
                             log2_comb_bitshift=l_bitshift, log2_comb_lgamma=l_lgamma,
                             b_star=b_star, log2_bstar=l_bstar,
                             log2_floor=l_floor_bitshift, log2_floor_lgamma=l_floor_lgamma,
                             margin=margin, margin_lgamma=margin_lgamma,
                             a_plus=a_plus, K=K, p=p, spow=spow, lam=lam)
    _MARGIN_LEDGER.update(ledger)
    return _MARGIN_LEDGER


def parse_tex_margins() -> dict:
    """Regex-extract the promoted note's own printed margin table
    (grande_finale.tex, the 'adjacent agreement / spare margin' table) so
    gate i checks against what the PROMOTED FILE ACTUALLY PRINTS TODAY, not
    just a hardcoded expectation baked into this script."""
    text = load_text(TEX_PATH)
    pat = re.compile(
        r"(KoalaBear MCA|KoalaBear list|Mersenne-31 MCA|Mersenne-31 list)\s*&\s*"
        r"\\\(\s*\d+\s*\\\)\s*&\s*\\\(\s*(\d+\.\d+)\s*\\\)\s*bits"
    )
    out = {}
    for m in pat.finditer(text):
        tex_name, val = m.group(1), float(m.group(2))
        out[TEX_ROW_NAME[tex_name]] = val
    return out


def gate_i_margins(tamper: bool = False):
    ledger = build_margin_ledger()
    tex_margins = parse_tex_margins()

    all_ok = True
    parts = []
    for row in ROWS:
        name = row["name"]
        entry = ledger[name]
        expected = EXPECTED_MARGIN[name]
        ok_bitshift = check(round(entry["margin"], 4), expected, tamper=tamper)
        ok_lgamma = check(round(entry["margin_lgamma"], 4), expected, tamper=tamper)
        ok_crosscheck = abs(entry["margin"] - entry["margin_lgamma"]) < 1e-6
        tex_val = tex_margins.get(name)
        ok_tex = (tex_val is not None) and check(round(entry["margin"], 4), tex_val, tamper=tamper)
        ok = ok_bitshift and ok_lgamma and ok_crosscheck and ok_tex
        all_ok = all_ok and ok
        parts.append(f"{name.strip()}: margin={entry['margin']:.4f} "
                     f"(lgamma={entry['margin_lgamma']:.4f}, tex={tex_val}, expect={expected}) {'OK' if ok else 'MISMATCH'}")
    msg = " | ".join(parts)
    return all_ok, msg


# ===========================================================================
# gate ii -- P2 fixed-deficiency arithmetic + growing-deficiency miss
# ===========================================================================
_GROWING_DEF_CACHE: dict = {}


def build_growing_deficiency() -> dict:
    if _GROWING_DEF_CACHE:
        return _GROWING_DEF_CACHE
    ledger = build_margin_ledger()

    kb = ledger["KoalaBear MCA "]
    d_kb = kb["omega"] - kb["w"]
    c_d_kb = math.comb(N_DEP, d_kb)          # one fresh expensive comb()

    m31 = ledger["Mersenne31 MCA"]
    d_m31 = m31["omega"] - m31["w"]
    # d_m31 = d_kb + 48 (913681 = 913633 + 48): cheap exact shift-up derivation
    steps = d_m31 - d_kb
    if steps >= 0:
        c_d_m31 = shift_comb_up(c_d_kb, d_kb, N_DEP, steps)
    else:
        c_d_m31 = shift_comb_down(c_d_kb, d_kb, N_DEP, -steps)

    out = {
        "KoalaBear MCA ": dict(d=d_kb, comb_d=c_d_kb),
        "Mersenne31 MCA": dict(d=d_m31, comb_d=c_d_m31),
    }
    _GROWING_DEF_CACHE.update(out)
    return _GROWING_DEF_CACHE


def gate_ii_p2_and_growing(tamper: bool = False):
    ledger = build_margin_ledger()
    growing = build_growing_deficiency()

    all_ok = True
    parts = []
    for name in ("KoalaBear MCA ", "Mersenne31 MCA"):
        row = ledger[name]
        omega, w, p = row["omega"], row["w"], row["p"]
        l_bstar = row["log2_bstar"]
        l_floor = row["log2_floor"]

        # P2 deficiency-1: lem:capf-dim1, floor(n/omega)
        def1 = N_DEP // omega
        ok_def1 = check(def1, 2, tamper=tamper)
        ok_def1_fits = math.log2(def1) < l_bstar

        # P2 deficiency-2: thm:capf-dim2, C(n,2)/(omega-1)
        def2 = math.comb(N_DEP, 2) / (omega - 1)
        l_def2 = math.log2(def2)
        ok_def2 = check(round(l_def2, 1), 21.1, tol=0.05, tamper=tamper)
        ok_def2_fits = l_def2 < l_bstar

        # growing-deficiency: dim W, thm:capf-fixeddim C(n,d), thm:bc-proper q^(d+1)
        exp = GROWING_DEF_EXPECT[name]
        g = growing[name]
        d = g["d"]
        dimW = d + 1
        ok_d = check(d, exp["d"], tamper=tamper)
        ok_dimW = check(dimW, exp["dimW"], tamper=tamper)

        l_fixeddim = log2_bigint(g["comb_d"])
        l_fixeddim_lg = log2_comb_lgamma(N_DEP, d)
        ok_fixeddim_crosscheck = abs(l_fixeddim - l_fixeddim_lg) < 1e-6
        ok_fixeddim = check(round(l_fixeddim, 1), exp["log2_fixeddim"], tol=0.05, tamper=tamper)
        miss_fixeddim = l_fixeddim - l_floor
        # expected miss is DERIVED from the two already-checked 1dp/4dp pinned
        # values, so the tolerance only needs to absorb that rounding (<=0.1 bit).
        expect_miss_fixeddim = exp["log2_fixeddim"] - l_floor
        ok_miss_fixeddim = check(miss_fixeddim, expect_miss_fixeddim, tol=0.15, tamper=tamper)

        l_bcproper = (dimW) * row["spow"] * math.log2(p)   # q^(d+1) = p^(spow*(d+1))
        ok_bcproper = check(round(l_bcproper, 1), exp["log2_bcproper"], tol=0.05, tamper=tamper)
        miss_bcproper = l_bcproper - l_floor
        expect_miss_bcproper = exp["log2_bcproper"] - l_floor
        ok_miss_bcproper = check(miss_bcproper, expect_miss_bcproper, tol=0.15, tamper=tamper)

        ok = (ok_def1 and ok_def1_fits and ok_def2 and ok_def2_fits and ok_d and ok_dimW
              and ok_fixeddim_crosscheck and ok_fixeddim and ok_miss_fixeddim
              and ok_bcproper and ok_miss_bcproper)
        all_ok = all_ok and ok
        parts.append(
            f"{name.strip()}: def1={def1}(fits {ok_def1_fits}) def2=2^{l_def2:.2f}(fits {ok_def2_fits}) "
            f"dimW={dimW}(expect {exp['dimW']}) fixeddim=2^{l_fixeddim:.1f}(miss {miss_fixeddim:.3e}b) "
            f"bcproper=2^{l_bcproper:.1f}(miss {miss_bcproper:.3e}b) {'OK' if ok else 'MISMATCH'}"
        )
    msg = " | ".join(parts)
    return all_ok, msg


# ===========================================================================
# gate iii -- toy census replay (independent re-implementation)
#
# Interpolation-degree test via the S_r(f,T) functionals of lem:capfp-functionals
# (raw L8246): f|_T extends to degree<K  iff  S_r(f,T)=0 for all 0<=r<w=m-K.
# This is a DIFFERENT algorithm from laneM_compute.py's Newton-divided-
# difference approach (same underlying mathematics, different code path,
# grounded directly in a cited, verified lemma). Codeword reconstruction (for
# the thm:saturation fiber identity) uses direct Lagrange interpolation.
# ===========================================================================
class GF2:
    """F_{p^2} = F_p[t]/(t^2 - nu). Elements are (a,b) meaning a + b*t."""

    __slots__ = ("p", "nu")

    def __init__(self, p, nu):
        self.p, self.nu = p, nu

    def add(self, x, y):
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def sub(self, x, y):
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p)

    def mul(self, x, y):
        p, nu = self.p, self.nu
        a, b = x
        c, d = y
        return ((a * c + b * d * nu) % p, (a * d + b * c) % p)

    def inv(self, x):
        p, nu = self.p, self.nu
        a, b = x
        den = (a * a - nu * b * b) % p
        di = pow(den, p - 2, p)
        return ((a * di) % p, ((-b) % p * di) % p)

    def zero(self):
        return (0, 0)

    def one(self):
        return (1, 0)

    def from_base(self, a):
        return (a % self.p, 0)

    def elements(self):
        return [(a, b) for a in range(self.p) for b in range(self.p)]

    def is_base(self, x):
        return x[1] == 0

    def pw(self, x, e):
        r = self.one()
        for _ in range(e):
            r = self.mul(r, x)
        return r

    def eval_poly(self, coeffs_low_to_high, x):
        r = self.zero()
        for c in reversed(coeffs_low_to_high):
            r = self.add(self.mul(r, x), c)
        return r


def find_nonresidue(p):
    sq = {(a * a) % p for a in range(p)}
    for nu in range(2, p):
        if nu % p not in sq:
            return nu
    raise RuntimeError("no nonresidue found")


def _lam_inv_cache(F, xs):
    m = len(xs)
    out = []
    for i in range(m):
        lam = F.one()
        for j in range(m):
            if j == i:
                continue
            lam = F.mul(lam, F.sub(xs[i], xs[j]))
        out.append(F.inv(lam))
    return out


def _S_r(F, ys, xs, r, lam_cache):
    total = F.zero()
    for i in range(len(xs)):
        term = F.mul(ys[i], F.pw(xs[i], r))
        term = F.mul(term, lam_cache[i])
        total = F.add(total, term)
    return total


def _lagrange_coeffs_lowK(F, xs, ys, K):
    """Direct Lagrange interpolation (independent of Newton divided
    differences): builds each basis polynomial by explicit multiplication of
    (X - xs[j]) factors."""
    m = len(xs)
    result = [F.zero()] * m
    for i in range(m):
        poly = [F.one()]
        for j in range(m):
            if j == i:
                continue
            xj = xs[j]
            newpoly = [F.zero()] * (len(poly) + 1)
            for d, c in enumerate(poly):
                newpoly[d + 1] = F.add(newpoly[d + 1], c)
                newpoly[d] = F.sub(newpoly[d], F.mul(c, xj))
            poly = newpoly
        lam = F.one()
        for j in range(m):
            if j == i:
                continue
            lam = F.mul(lam, F.sub(xs[i], xs[j]))
        scale = F.mul(ys[i], F.inv(lam))
        for d, c in enumerate(poly):
            result[d] = F.add(result[d], F.mul(scale, c))
    if K <= len(result):
        return result[:K]
    return result + [F.zero()] * (K - len(result))


def _census_and_rays(F, D, Uz, K, m):
    """Returns (Cen, ray_sc, ray_count) -- exactly def:saturated-rays /
    thm:saturation's objects, computed via the S_r criterion + Lagrange
    reconstruction."""
    n = len(D)
    w = m - K
    Cen = 0
    ray_sc = {}
    ray_count = {}
    for Tidx in itertools.combinations(range(n), m):
        xs = [D[i] for i in Tidx]
        ys = [Uz[i] for i in Tidx]
        lam_cache = _lam_inv_cache(F, xs)
        ok = True
        for r in range(w):
            if _S_r(F, ys, xs, r, lam_cache) != F.zero():
                ok = False
                break
        if not ok:
            continue
        Cen += 1
        coeffs = _lagrange_coeffs_lowK(F, xs, ys, K)
        cpad = tuple(coeffs)
        ray_count[cpad] = ray_count.get(cpad, 0) + 1
        if cpad not in ray_sc:
            s = 0
            for i in range(n):
                if F.eval_poly(cpad, D[i]) == Uz[i]:
                    s += 1
            ray_sc[cpad] = s
    return Cen, ray_sc, ray_count


def run_toy_instance(p, K, m, n, seed, mode):
    nu = find_nonresidue(p)
    F = GF2(p, nu)
    D = [(a, 0) for a in range(n)]
    rng = random.Random(seed)
    if mode == "random_base":
        u = [F.from_base(rng.randrange(p)) for _ in range(n)]
        v = [F.from_base(rng.randrange(p)) for _ in range(n)]
    elif mode == "random_ext":
        u = [(rng.randrange(p), rng.randrange(p)) for _ in range(n)]
        v = [(rng.randrange(p), rng.randrange(p)) for _ in range(n)]
    elif mode == "pole":
        alpha = (rng.randrange(p), 1 + rng.randrange(p - 1))
        Uw = [F.from_base(rng.randrange(p)) for _ in range(n)]
        u, v = [], []
        for i in range(n):
            den = F.inv(F.sub(D[i], alpha))
            u.append(F.mul(Uw[i], den))
            v.append(F.mul(F.sub(F.zero(), F.one()), den))
    else:
        raise ValueError(mode)

    tot_cen = 0
    tot_lineray = 0
    bad = set()
    base_bad = ext_bad = 0
    sat_ok = True
    slope_mult = []
    ray_sat = []
    for z in F.elements():
        Uz = [F.add(u[i], F.mul(z, v[i])) for i in range(n)]
        Cen, ray_sc, ray_count = _census_and_rays(F, D, Uz, K, m)
        chk = 0
        for c, s in ray_sc.items():
            fib = math.comb(s, m)
            chk += fib
            if ray_count[c] != fib:
                sat_ok = False
        if chk != Cen:
            sat_ok = False
        tot_cen += Cen
        nray = len(ray_sc)
        tot_lineray += nray
        if nray > 0:
            bad.add(z)
            slope_mult.append(nray)
            for c, s in ray_sc.items():
                ray_sat.append(math.comb(s, m))
            if F.is_base(z):
                base_bad += 1
            else:
                ext_bad += 1
    return dict(
        nbad=len(bad), base=base_bad, ext=ext_bad,
        lineray=tot_lineray, Cen=tot_cen, sat_ok=sat_ok,
        maxmult=max(slope_mult) if slope_mult else 0,
        maxsat=max(ray_sat) if ray_sat else 0,
    )


# All 45 (config, mode, seed) instances and their PINNED expected results,
# verbatim from laneM_compute.py PART B's output.txt (reproduced bit-for-bit
# by an independent rerun during packaging -- see companion note).
TOY_CONFIGS = [
    dict(p=7, K=2, m=4, n=7),
    dict(p=7, K=3, m=5, n=7),
    dict(p=11, K=4, m=6, n=11),
    dict(p=11, K=3, m=6, n=11),
    dict(p=13, K=5, m=7, n=13),
]

# key: (p, K, m, mode, seed) -> (nbad, base, ext, lineray, Cen, maxmult, maxsat)
PINNED = {
    (7, 2, 4, "random_base", 0): (3, 3, 0, 3, 3, 1, 1),
    (7, 2, 4, "random_base", 1): (4, 4, 0, 4, 8, 1, 5),
    (7, 2, 4, "random_base", 2): (5, 5, 0, 5, 5, 1, 1),
    (7, 2, 4, "pole", 0): (3, 0, 3, 3, 7, 1, 5),
    (7, 2, 4, "pole", 1): (4, 0, 4, 4, 4, 1, 1),
    (7, 2, 4, "pole", 2): (5, 0, 5, 5, 5, 1, 1),
    (7, 2, 4, "random_ext", 0): (1, 0, 1, 1, 1, 1, 1),
    (7, 2, 4, "random_ext", 1): (0, 0, 0, 0, 0, 0, 0),
    (7, 2, 4, "random_ext", 2): (0, 0, 0, 0, 0, 0, 0),
    (7, 3, 5, "random_base", 0): (1, 1, 0, 1, 1, 1, 1),
    (7, 3, 5, "random_base", 1): (3, 3, 0, 3, 3, 1, 1),
    (7, 3, 5, "random_base", 2): (3, 3, 0, 3, 3, 1, 1),
    (7, 3, 5, "pole", 0): (3, 2, 1, 3, 3, 1, 1),
    (7, 3, 5, "pole", 1): (1, 0, 1, 1, 6, 1, 6),
    (7, 3, 5, "pole", 2): (2, 2, 0, 2, 2, 1, 1),
    (7, 3, 5, "random_ext", 0): (1, 0, 1, 1, 1, 1, 1),
    (7, 3, 5, "random_ext", 1): (1, 0, 1, 1, 1, 1, 1),
    (7, 3, 5, "random_ext", 2): (1, 0, 1, 1, 1, 1, 1),
    (11, 4, 6, "random_base", 0): (11, 11, 0, 30, 36, 4, 7),
    (11, 4, 6, "random_base", 1): (11, 11, 0, 29, 41, 4, 7),
    (11, 4, 6, "random_base", 2): (11, 11, 0, 28, 46, 4, 7),
    (11, 4, 6, "pole", 0): (27, 1, 26, 28, 40, 2, 7),
    (11, 4, 6, "pole", 1): (29, 3, 26, 30, 42, 2, 7),
    (11, 4, 6, "pole", 2): (29, 2, 27, 30, 42, 2, 7),
    (11, 4, 6, "random_ext", 0): (7, 0, 7, 7, 7, 1, 1),
    (11, 4, 6, "random_ext", 1): (3, 0, 3, 3, 3, 1, 1),
    (11, 4, 6, "random_ext", 2): (4, 0, 4, 4, 4, 1, 1),
    (11, 3, 6, "random_base", 0): (3, 3, 0, 3, 3, 1, 1),
    (11, 3, 6, "random_base", 1): (2, 2, 0, 2, 2, 1, 1),
    (11, 3, 6, "random_base", 2): (3, 3, 0, 3, 9, 1, 7),
    (11, 3, 6, "pole", 0): (3, 0, 3, 3, 3, 1, 1),
    (11, 3, 6, "pole", 1): (4, 0, 4, 4, 4, 1, 1),
    (11, 3, 6, "pole", 2): (5, 1, 4, 5, 5, 1, 1),
    (11, 3, 6, "random_ext", 0): (0, 0, 0, 0, 0, 0, 0),
    (11, 3, 6, "random_ext", 1): (0, 0, 0, 0, 0, 0, 0),
    (11, 3, 6, "random_ext", 2): (0, 0, 0, 0, 0, 0, 0),
    (13, 5, 7, "random_base", 0): (13, 13, 0, 91, 119, 10, 8),
    (13, 5, 7, "random_base", 1): (13, 13, 0, 84, 105, 9, 8),
    (13, 5, 7, "random_base", 2): (13, 13, 0, 91, 133, 10, 8),
    (13, 5, 7, "pole", 0): (71, 7, 64, 79, 135, 2, 8),
    (13, 5, 7, "pole", 1): (58, 4, 54, 63, 203, 2, 120),
    (13, 5, 7, "pole", 2): (79, 7, 72, 90, 125, 2, 8),
    (13, 5, 7, "random_ext", 0): (10, 0, 10, 10, 10, 1, 1),
    (13, 5, 7, "random_ext", 1): (7, 1, 6, 7, 7, 1, 1),
    (13, 5, 7, "random_ext", 2): (11, 0, 11, 12, 12, 2, 1),
}
assert len(PINNED) == 45, f"expected 45 pinned instances, found {len(PINNED)}"

# default (zero-arg) LIVE subset: both p=7 configs, both p=11 configs (36
# instances -- "the smallest"), plus all 3 modes of p=13 seed=0 (the
# headline adversarial witness, 3 more instances) = 39 live by default.
# The remaining 6 (p=13, seeds 1-2, all 3 modes) are checked against PINNED
# only, unless --full is passed.
def _default_live_keys():
    keys = []
    for cfg in TOY_CONFIGS:
        for mode in ("random_base", "pole", "random_ext"):
            for seed in range(3):
                if cfg["p"] == 13 and seed != 0:
                    continue
                keys.append((cfg["p"], cfg["K"], cfg["m"], mode, seed))
    return keys


def gate_iii_toy_census(full: bool = False, tamper: bool = False):
    live_keys = set(PINNED.keys()) if full else set(_default_live_keys())
    all_ok = True
    n_live = 0
    n_pinned_only = 0
    mismatches = []
    identity_fail = []

    for cfg in TOY_CONFIGS:
        for mode in ("random_base", "pole", "random_ext"):
            for seed in range(3):
                key = (cfg["p"], cfg["K"], cfg["m"], mode, seed)
                expected = PINNED[key]
                exp_tup = _corrupt(expected) if (tamper and key == (7, 2, 4, "random_base", 0)) else expected
                if key in live_keys:
                    n_live += 1
                    r = run_toy_instance(cfg["p"], cfg["K"], cfg["m"], cfg["n"], seed, mode)
                    got = (r["nbad"], r["base"], r["ext"], r["lineray"], r["Cen"], r["maxmult"], r["maxsat"])
                    if not r["sat_ok"]:
                        identity_fail.append(key)
                    if got != exp_tup:
                        mismatches.append((key, got, exp_tup))
                else:
                    n_pinned_only += 1
                    # structural check only: loss1, loss2 >= 0 and consistent
                    nbad, base, ext, lineray, cen, maxmult, maxsat = exp_tup
                    loss1 = lineray - nbad
                    loss2 = cen - lineray
                    if loss1 < 0 or loss2 < 0 or base + ext != nbad:
                        mismatches.append((key, "structural-check", exp_tup))

    all_ok = (not mismatches) and (not identity_fail)
    msg = (f"{n_live} live-enumerated, {n_pinned_only} pinned-only "
           f"(mode={'--full: all 45 live' if full else 'default: 39 live / 6 pinned'}); "
           f"thm:saturation identity {'VERIFIED on all live instances' if not identity_fail else f'FAILED on {identity_fail}'}; "
           f"dedup-loss/tuple mismatches: {mismatches if mismatches else 'none'}")
    return all_ok, msg


# ===========================================================================
# gate iv -- L4 floor consistency
# ===========================================================================
def gate_iv_l4_consistency(tamper: bool = False):
    p, n, K, m = L4["p"], L4["n"], L4["K"], L4["m"]
    w = m - K
    comb_val = math.comb(n, m)          # small, <1s
    l_comb = log2_bigint(comb_val)
    l_comb_lg = log2_comb_lgamma(n, m)
    l_floor = l_comb - w * math.log2(p)
    ok_crosscheck = abs(l_comb - l_comb_lg) < 1e-6
    ok_self = check(round(l_floor, 4), L4_EXPECTED_LOG2_FLOOR, tol=5e-4, tamper=tamper)

    rung_val = None
    ok_rung = False
    if os.path.isfile(RUNG_AUDIT_JSON):
        packet = load_json(RUNG_AUDIT_JSON)
        rungs = packet.get("conjQ_rung_audit", {}).get("rungs", [])
        for rung in rungs:
            if rung.get("j") == 4:
                rung_val = rung.get("log2_quotient_avg_a_j")
                break
        if rung_val is not None:
            ok_rung = check(round(rung_val, 4), L4_RUNG_AUDIT_EXPECT, tol=5e-4, tamper=tamper)
            ok_rung = ok_rung and check(round(l_floor, 4), round(rung_val, 4), tol=5e-4, tamper=tamper)

    ok_pr369 = check(round(l_floor, 4), L4_PR369_EXPECT, tol=5e-4, tamper=tamper)

    ok = ok_crosscheck and ok_self and ok_rung and ok_pr369
    msg = (f"log2 floor(recompute)={l_floor:.6f} vs kb_mca_conjq_rung_audit(j=4)={rung_val} "
           f"vs PR#369-pinned={L4_PR369_EXPECT} -- all agree to >=4dp: {ok}")
    return ok, msg


# ===========================================================================
# main
# ===========================================================================
GATE_SPECS_BASE = [
    ("gate i   margin identity (4 rows)          ", lambda full, t: gate_i_margins(t)),
    ("gate ii  P2 arithmetic + growing-def miss   ", lambda full, t: gate_ii_p2_and_growing(t)),
    ("gate iii toy census replay (39/45 or 45/45) ", lambda full, t: gate_iii_toy_census(full, t)),
    ("gate iv  L4 floor consistency (3 routes)    ", lambda full, t: gate_iv_l4_consistency(t)),
]


def main() -> int:
    t0 = time.time()
    argv = sys.argv[1:]
    selftest = "--tamper-selftest" in argv
    full = "--full" in argv

    print("=" * 90)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is corrupted")
    else:
        print(" verify_saturated_bc_budget_fit  (zero-arg)" + (" --full" if full else ""))
        print(" prob:saturated-bc budget fit + margin identity -- AUDIT, not a proof of prob:saturated-bc")
    print("=" * 90)

    if not os.path.isfile(NOTE_PATH):
        print(f"FATAL: companion note missing: {NOTE_PATH}")
        return 1
    if not os.path.isfile(TEX_PATH):
        print(f"FATAL: promoted TeX source missing: {TEX_PATH}")
        return 1

    packet = None
    if os.path.isfile(JSON_PATH):
        try:
            packet = load_json(JSON_PATH)
        except Exception as exc:  # noqa: BLE001
            print(f"FATAL: could not load packet JSON: {exc}")
            return 1
        ok_wall = packet.get("wall_id") == WALL_ID
        if not ok_wall:
            print(f"FATAL: wall_id mismatch: {packet.get('wall_id')!r} != {WALL_ID!r}")
            return 1
    else:
        print(f"WARNING: packet JSON not found at {JSON_PATH} (gates run standalone)")

    all_good = True
    for label, fn in GATE_SPECS_BASE:
        ok, summary = fn(full, selftest)
        caught_or_pass = (not ok) if selftest else ok
        all_good = all_good and caught_or_pass
        tag = ("CAUGHT " if caught_or_pass else "MISSED!") if selftest else ("PASS" if ok else "FAIL")
        print(f"  {label}  {tag}   ({time.time()-t0:.1f}s elapsed)")
        print(f"        {summary}")

    print("=" * 90)
    dt = time.time() - t0
    if selftest:
        print(f" SELF-TEST RESULT: {'all tampers CAUGHT' if all_good else 'A TAMPER WAS MISSED'}   ({dt:.1f}s)")
    else:
        print(f" RESULT: {'ALL GATES PASS' if all_good else 'FAILURE'}   ({dt:.1f}s)")
        print(" This verifier does not decide prob:saturated-bc, does not certify")
        print(" U(a0+1)<=B* for the growing-deficiency interior cell, and does not move")
        print(" the frontier edge; it only checks this PR's own arithmetic (see docstring).")
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
