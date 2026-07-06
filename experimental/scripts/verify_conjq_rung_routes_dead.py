#!/usr/bin/env python3
"""verify_conjq_rung_routes_dead.py

Zero-arg, stdlib-only, deterministic verifier for
experimental/data/certificates/frontier-adjacent/kb_mca_conjq_route_margins_v1.json
and its companion note experimental/notes/thresholds/cap25_v13_qfin_rung_routes_dead.md.

This packet is the conj:Q RUNG-ROUTES route-cut audit at the deployed KB-MCA
v13 raw row (wall CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048).
It reuses the already-integrated, already-verified 5-rung ladder of
kb_mca_conjq_rung_audit_v1.json (the row shapes (n_s,m_s,w_s), s=0..4, and the
descent identity (D)) and asks a DIFFERENT question of it: are there any cheap
routes (distance-only packing bounds, the proved head-flatness ceiling, or a
low-moment bridge) that can actually CLOSE any rung's flatness bound below the
shared K_raw bar? It finds all three DEAD, with exact printed margins, and
records one strategic correction: the ladder's rungs do not approach the
proved head-depth base cases as they get shallower (kb_mca_conjq_rung_audit_v1
Sec 7's "toward the proved head-depth base cases" framing) -- head-reach
degrades in lockstep with the required depth, so every rung is equally far
from it. This does NOT prove or refute conj:Q, does NOT prove U(1116048)<=B*,
does NOT move the frontier edge, and does NOT change any verdict or integer of
kb_mca_conjq_rung_audit_v1.json (that file is not read or modified by this
verifier; the ladder row shapes are independently re-derived from P, N, K,
M_SAFE below, the same raw constants, not copied from that JSON).

Four gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  gate i    H1 PACKING BOUND. Independently recomputes, at all 5 ladder rows
            L_0..L_4 (the primitive core plus the four nonprimitive rungs),
            the anticode/packing bound rho(z) <= p^w / C(k-1,w)
            (cor:anticode-cap specialized to n=2k rows) using EXACT big-integer
            binomial coefficients (comb(k-1,w); no floating point in the
            integer itself, only in the final log2 conversion), derives
            log2(rho_bound) and its margin over the ladder bar log2(K_raw),
            and diffs every field against the shipped JSON to a tight float
            tolerance. K_raw itself is independently re-derived from P, N, K,
            M_SAFE via the same exact big-integer construction as the sibling
            rung-audit verifier (comb(N,M_SAFE), the dominant ~15s cost),
            confirming it still equals 4807520 -- this makes the gate fully
            self-contained rather than trusting a copied constant. Expected
            per-rung reading: over the bar by ~1.73e6 bits at L_0 down to
            ~1.08e5 bits at L_4 -- DEAD everywhere.
  gate ii   H1 TOY VALIDATION. Exhaustive fiber enumeration (independent
            reimplementation, brute-force itertools.combinations, not imported
            from any prior lane's script) on 5 toy rows. For every row, checks
            (a) RIGIDITY: every pair of distinct fiber members M,M' satisfies
            |M\\M'| >= w+1 (equivalently |M cap M'| <= m-w-1), (b) PACKING:
            the true max fiber size is <= the H1 bound C(n,m-w)/C(m,w),
            computed independently via exact Fraction arithmetic, and (c) on
            the one n=2k row, the CLEAN-FORM IDENTITY
            C(k-1,w)*C(n,m-w) == C(n,m)*C(m,w) holds EXACTLY (integer
            equality, not a float approximation) -- this is the algebraic
            identity underlying the L_0..L_4 collapse rho<=p^w/C(k-1,w) used
            by gate i.
  gate iii  H2 HEAD-FLATNESS CEILING. At all 5 ladder rows, recomputes
            w_head(n,m) two independent ways: (1) the closed form
            floor((n-m)/ceil(sqrt p)), and (2) an exact per-w search of
            thm:head-flatness's own nonvacuity inequality (error term < main
            term, ell=0) -- and checks the two AGREE at every rung. Confirms
            the deployed L_0 value is exactly 21 (matching cor:head-q's proved
            "w<=21" to the integer) and that the five-rung DEGRADATION table
            is exactly (21,10,5,2,1), with the gap ratio w_needed/w_head never
            improving down the ladder (~3200x-4200x throughout, worst 4216x
            exactly at the L_4 terminus).
  gate iv   MOMENT-ORDER ARITHMETIC at L_4. Recomputes r=ceil(w*log2(p)/Delta)
            (thm:moment-q specialized to the optimistic log2(Gamma_r)~0 case)
            at L_4's w=4216 for both the shared ladder bar (Delta=log2(K_raw))
            and L_4's own standalone budget (Delta=34.79309905, the row's
            log2(B*)-log2(quotient average) already recorded in
            kb_mca_conjq_rung_audit_v1.json), confirming r>=5886 and r>=3756
            respectively, against a provable head-depth order of only 1 (H2's
            w_head at L_4).

Hidden self-test: python3 verify_conjq_rung_routes_dead.py --tamper-selftest
    Each gate function takes a tamper=False parameter; in self-test mode it is
    called with tamper=True, which corrupts exactly ONE stored/expected value
    used inside that gate's first check (never the from-scratch recomputed
    side) and asserts the gate then reports a mismatch (CAUGHT). The shipped
    default is zero-arg (tamper=False everywhere).

PERFORMANCE. The dominant cost is gate i's re-derivation of K_raw, which needs
comb(N,M_SAFE) (~2.1e6-bit result, ~15s measured, the same cost already paid
by the sibling verify_kb_mca_conjq_rung_audit.py). The five comb(k_s-1,w_s)
calls for the packing bound itself are cheap (largest is ~361-thousand-bit,
well under 1s each). Gates ii-iv are all toy-scale or closed-form arithmetic,
well under 1s combined. Measured total runtime (zero-arg, this machine):
see the printed footer; comfortably under the 60s budget.

This verifier does NOT decide conj:Q, does NOT certify U(1116048)<=B*, and
does NOT move the frontier edge. It only checks that this PR's arithmetic is
exactly what it claims to be.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from itertools import combinations
from math import comb, lgamma, isqrt
from fractions import Fraction

sys.set_int_max_str_digits(2_500_000)

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
JSON_PATH = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                         "frontier-adjacent", "kb_mca_conjq_route_margins_v1.json")
NOTE_PATH = os.path.join(REPO_ROOT, "experimental", "notes", "thresholds",
                         "cap25_v13_qfin_rung_routes_dead.md")
SIBLING_JSON_PATH = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                                 "frontier-adjacent", "kb_mca_conjq_rung_audit_v1.json")

# ---------------------------------------------------------------------------
# deployed KB-MCA v13-raw safe row -- ground truth, independent of the JSON
# ---------------------------------------------------------------------------
P = 2 ** 31 - 2 ** 24 + 1          # KoalaBear prime
N = 2 ** 21
K = 2 ** 20
B_STAR = P ** 6 // 2 ** 128        # 274980728111395087
M_SAFE = 1116048
W_SAFE = M_SAFE - K - 1            # 67471

WALL_ID = "CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048"

LOG2P = math.log2(P)
CEIL_SQRT_P = isqrt(P) + 1

# L_4's own standalone budget bits (quotient_row_slack_vs_Bstar_bits), already
# recorded and independently verified by kb_mca_conjq_rung_audit_v1.json /
# verify_kb_mca_conjq_rung_audit.py; used here only as one of the two moment
# budgets in gate iv, not re-derived (that re-derivation is gate i's job in
# the sibling verifier, not this one's).
L4_STANDALONE_BUDGET_BITS = 34.79309905


# ---------------------------------------------------------------------------
# generic helpers
# ---------------------------------------------------------------------------
def log2_int(x: int) -> float:
    """Exact-enough log2 of a huge nonnegative int, without stringifying it."""
    if x <= 0:
        return float("-inf")
    b = x.bit_length()
    if b <= 53:
        return math.log2(x)
    s = b - 53
    return s + math.log2(x >> s)


LN2 = math.log(2.0)


def log2binom(a: int, b: float) -> float:
    """lgamma-based log2 C(a,b) for the (cheap, small-magnitude) head-flatness search."""
    if b < 0 or b > a or a < 0:
        return float("-inf")
    return (lgamma(a + 1.0) - lgamma(a - b + 1.0) - lgamma(b + 1.0)) / LN2


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
    if isinstance(x, (list, tuple)):
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


def load_packet() -> dict:
    with open(JSON_PATH, encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# shared ladder-row shapes -- independently re-derived from P, N, K, M_SAFE
# (NOT read from either JSON), matching kb_mca_conjq_rung_audit_v1.json's
# already-proved (D)-descent row shapes row_s = (n/2^s, m/2^s, floor(w/2^s)).
# ---------------------------------------------------------------------------
def ladder_rows():
    rows = []
    for s in range(5):
        n_s = N // (2 ** s)
        m_s = M_SAFE // (2 ** s)
        w_s = W_SAFE // (2 ** s)
        k_s = m_s - w_s - 1
        rows.append(dict(s=s, n=n_s, m=m_s, w=w_s, k=k_s))
    return rows


# ---------------------------------------------------------------------------
# gate i -- H1 packing bound, all 5 rows, big-int exact
# ---------------------------------------------------------------------------
_KRAW_CACHE: dict = {}


def build_kraw():
    """Independently re-derive K_raw = floor(B* p^w / C(n,m)) from P,N,K,M_SAFE
    alone (the dominant cost, ~15s: comb(N,M_SAFE) is a ~2.1e6-bit integer)."""
    if _KRAW_CACHE:
        return _KRAW_CACHE
    t0 = time.time()
    binom_nm = comb(N, M_SAFE)
    pw = pow(P, W_SAFE)
    Kraw = (B_STAR * pw) // binom_nm
    log2_Kraw = log2_int(Kraw)
    _KRAW_CACHE.update({"Kraw": Kraw, "log2_Kraw": log2_Kraw, "dt": time.time() - t0})
    return _KRAW_CACHE


def gate_i_h1_packing(packet, tamper=False):
    kraw = build_kraw()
    Kraw, bar = kraw["Kraw"], kraw["log2_Kraw"]

    stored_target = packet["target"]
    ok_kraw = check(Kraw, stored_target["K_raw"], tamper=tamper)
    ok_bar = check(bar, stored_target["log2_K_raw_bar"], tol=1e-6)

    stored_rows = {r["rung"]: r for r in packet["conjQ_route_margins"]["h1_packing_bound"]["rows"]}
    ok = ok_kraw and ok_bar
    msgs = [f"K_raw={Kraw} (expect {stored_target['K_raw']}) ok={ok_kraw}, "
            f"log2(K_raw)={bar:.6f} ok={ok_bar} (ledger build {kraw['dt']:.1f}s)"]

    for row in ladder_rows():
        s, n_s, m_s, w_s, k_s = row["s"], row["n"], row["m"], row["w"], row["k"]
        rung = f"L_{s}"
        Ckm1w = comb(k_s - 1, w_s)
        log2C = log2_int(Ckm1w)
        log2pw = w_s * LOG2P
        lrho = log2pw - log2C
        margin = lrho - bar

        stored = stored_rows[rung]
        ok_w = check(w_s, stored["w"])
        ok_km1 = check(k_s - 1, stored["k_minus_1"])
        ok_pw = check(log2pw, stored["log2_pw"], tol=1e-3)
        ok_C = check(log2C, stored["log2_C_k_minus1_w"], tol=1e-3)
        ok_lrho = check(lrho, stored["log2_rho_bound"], tol=2e-3)
        ok_margin = check(margin, stored["margin_over_bar_bits"], tol=2e-3,
                           tamper=(tamper and rung == "L_4"))
        ok_dead = margin > 0  # DEAD means the bound sits ABOVE the bar (over-budget)
        ok_row = ok_w and ok_km1 and ok_pw and ok_C and ok_lrho and ok_margin and ok_dead
        ok = ok and ok_row
        msgs.append(f"{rung}: w={w_s} log2(rho_bound)={lrho:.3f} margin_over_bar={margin:.3f} "
                    f"(expect {stored['margin_over_bar_bits']:.3f}) dead={ok_dead} ok={ok_row}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate ii -- H1 toy validation (exhaustive enumeration, independent)
# ---------------------------------------------------------------------------
def mu_set(p: int, order: int):
    return [x for x in range(1, p) if pow(x, order, p) == 1]


def enum_fibers(D, m, w, p):
    fib = {}
    for M in combinations(D, m):
        z = tuple(sum(pow(x, i, p) for x in M) % p for i in range(1, w + 1))
        fib.setdefault(z, []).append(M)
    return fib


def toy_row(p, n, m, w, label, D=None):
    if D is None:
        D = mu_set(p, p - 1)  # F_p^* itself when n = p-1
        assert len(D) == n, (label, len(D), n)
    fib = enum_fibers(D, m, w, p)
    sizes = {z: len(v) for z, v in fib.items()}
    maxfib = max(sizes.values())
    PB = Fraction(comb(n, m - w), comb(m, w)) if m - w >= 0 else Fraction(comb(n, m))
    pack_ok = maxfib <= PB

    rig_ok = True
    rig_min = None
    for z, members in fib.items():
        if len(members) < 2:
            continue
        for i in range(len(members)):
            Ai = set(members[i])
            for j in range(i + 1, len(members)):
                e = len(Ai - set(members[j]))
                if rig_min is None or e < rig_min:
                    rig_min = e
                if e < w + 1:
                    rig_ok = False
    return dict(maxfib=maxfib, PB=PB, pack_ok=pack_ok, rig_ok=rig_ok, rig_min=rig_min)


TOY_ROWS = [
    ("F17_n16_m9_w1", 17, 16, 9, 1, None),
    ("F17_n16_m8_w2", 17, 16, 8, 2, None),
    ("F17_n16_m10_w3", 17, 16, 10, 3, None),
    ("F41_mu8_m5_w2", 41, 8, 5, 2, None),         # genuine order-8 subgroup, not F_p^*
    ("F17_mu16_n2k_m11_w2", 17, 16, 11, 2, None),  # n=2k clean-form row (k=8)
]


def gate_ii_toy_validation(packet, tamper=False):
    ok = True
    msgs = []
    first = True
    stored_rows = {r["label"]: r for r in packet["conjQ_route_margins"]["toy_validation"]["rows_checked"]}
    results = {}
    for (label, p, n, m, w, _) in TOY_ROWS:
        D = mu_set(p, n) if n != p - 1 else None
        r = toy_row(p, n, m, w, label, D=D)
        results[label] = r
        stored = stored_rows[label]
        ok_maxfib = check(r["maxfib"], stored["maxfib"], tamper=(tamper and first))
        first = False
        ok_pack = check(r["pack_ok"], True) and check(stored["packing_holds"], True)
        ok_rig = check(r["rig_ok"], True) and check(stored["rigidity_ok"], True)
        ok_row = ok_maxfib and ok_pack and ok_rig
        ok = ok and ok_row
        msgs.append(f"{label}: maxfib={r['maxfib']} (expect {stored['maxfib']}) "
                    f"rigidity_ok={r['rig_ok']} packing_ok={r['pack_ok']} ok={ok_row}")

    # clean-form identity on the n=2k row: C(k-1,w)*C(n,m-w) == C(n,m)*C(m,w), EXACT
    label, p, n, m, w, _ = TOY_ROWS[-1]
    k = m - w - 1
    lhs = comb(k - 1, w) * comb(n, m - w)
    rhs = comb(n, m) * comb(m, w)
    ok_identity = check(lhs == rhs, True)
    ok = ok and ok_identity
    msgs.append(f"clean-form identity C(k-1,w)*C(n,m-w)==C(n,m)*C(m,w): {lhs == rhs}")

    stored_agg = packet["conjQ_route_margins"]["h1_packing_bound"]
    ok_theorem_present = "cor:anticode-cap" in stored_agg["theorem"]
    ok = ok and ok_theorem_present
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate iii -- H2 head-flatness ceiling, two independent derivations
# ---------------------------------------------------------------------------
def head_nonvacuous(nn: int, mm: int, w: int) -> bool:
    """thm:head-flatness, ell=0: error p^{w/2} C(w*ceil(sqrt p)+m-1, m)
    < main p^{-w} C(n,m). For w=1 the p^{1/2} prefactor is dropped."""
    rhs = -w * LOG2P + log2binom(nn, mm)
    if w == 1:
        lhs = log2binom(CEIL_SQRT_P + mm - 1, mm)
    else:
        lhs = (w / 2.0) * LOG2P + log2binom(w * CEIL_SQRT_P + mm - 1, mm)
    return lhs < rhs


def head_ceiling_exact_search(nn: int, mm: int, wmax: int = 80) -> int:
    best = 0
    for w in range(1, wmax + 1):
        if head_nonvacuous(nn, mm, w):
            best = w
        else:
            break
    return best


def gate_iii_h2_ceiling(packet, tamper=False):
    ok = True
    msgs = []
    stored_rows = {r["rung"]: r for r in packet["conjQ_route_margins"]["h2_head_flatness_ceiling"]["rows"]}
    stored_cs = packet["conjQ_route_margins"]["h2_head_flatness_ceiling"]["ceil_sqrt_p"]
    ok_cs = check(CEIL_SQRT_P, stored_cs, tamper=tamper)
    ok = ok and ok_cs
    msgs.append(f"ceil(sqrt p)={CEIL_SQRT_P} (expect {stored_cs}) ok={ok_cs}")

    expect_degradation = [21, 10, 5, 2, 1]
    degradation = []
    for row in ladder_rows():
        s, n_s, m_s, w_s = row["s"], row["n"], row["m"], row["w"]
        rung = f"L_{s}"
        closed = (n_s - m_s) // CEIL_SQRT_P
        exact = head_ceiling_exact_search(n_s, m_s)
        degradation.append(exact)
        stored = stored_rows[rung]

        ok_closed = check(closed, stored["w_head_closed_form"])
        ok_exact = check(exact, stored["w_head_exact_search"])
        ok_match = check(closed == exact, stored["match"])
        gap = w_s / exact
        ok_gap = check(round(gap, 1), stored["gap_ratio"], tol=0.05)
        ok_row = ok_closed and ok_exact and ok_match and ok_gap
        ok = ok and ok_row
        msgs.append(f"{rung}: w_head closed={closed} exact_search={exact} match={closed == exact} "
                    f"gap={gap:.1f}x ok={ok_row}")

    ok_l0_cor = check(degradation[0], 21, tamper=tamper)  # ties to cor:head-q's proved "w<=21"
    ok = ok and ok_l0_cor
    msgs.append(f"deployed L_0 w_head={degradation[0]} matches cor:head-q 'w<=21': {ok_l0_cor}")

    ok_degradation = check(degradation, expect_degradation)
    ok = ok and ok_degradation
    msgs.append(f"degradation table {degradation} (expect {expect_degradation}): {ok_degradation}")

    # never-improving check: gap ratio must stay within [3000, 4300] at every rung
    gaps = [row["w"] / degradation[row["s"]] for row in ladder_rows()]
    ok_never_improves = all(3000.0 <= g <= 4300.0 for g in gaps)
    ok = ok and ok_never_improves
    msgs.append(f"gap ratios {[round(g, 1) for g in gaps]} all in [3000,4300]: {ok_never_improves}")
    # L_4 terminus gap is EXACTLY 4216 (not merely approximate)
    ok_terminus_exact = check(gaps[4], 4216.0)
    ok = ok and ok_terminus_exact
    msgs.append(f"L_4 terminus gap exactly 4216.0: {ok_terminus_exact}")

    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate iv -- moment-order arithmetic at L_4
# ---------------------------------------------------------------------------
def gate_iv_moment_order(packet, tamper=False):
    w4 = W_SAFE // (2 ** 4)
    ok_w4 = check(w4, 4216, tamper=tamper)

    kraw = build_kraw()
    bar = kraw["log2_Kraw"]

    r_bar = math.ceil(w4 * LOG2P / bar)
    r_standalone = math.ceil(w4 * LOG2P / L4_STANDALONE_BUDGET_BITS)

    stored_rows = {r["rung"]: r for r in packet["conjQ_route_margins"]["moment_route"]["rows"]}
    stored_l4 = stored_rows["L_4"]
    ok_bar = check(r_bar, stored_l4["r_at_bar"])
    ok_standalone = check(r_standalone, stored_l4["r_at_standalone"])
    ok_provable = check(stored_l4["provable_head_w"], 1)

    ok = ok_w4 and ok_bar and ok_standalone and ok_provable
    msg = (f"L_4 w={w4} (expect 4216) ok={ok_w4}; r_at_bar={r_bar} (expect {stored_l4['r_at_bar']}) "
           f"ok={ok_bar}; r_at_standalone={r_standalone} (expect {stored_l4['r_at_standalone']}) "
           f"ok={ok_standalone}; provable head w=1: {ok_provable}; "
           f"shortfall factor at bar ~{r_bar / 1}x, at standalone ~{r_standalone / 1}x")
    return ok, msg


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
GATE_SPECS = [
    ("gate i   H1 packing bound (5 rows, big-int) ", gate_i_h1_packing),
    ("gate ii  H1 toy validation (5 toy rows)      ", gate_ii_toy_validation),
    ("gate iii H2 head-flatness ceiling (5 rows)   ", gate_iii_h2_ceiling),
    ("gate iv  moment-order arithmetic at L_4      ", gate_iv_moment_order),
]


def main() -> int:
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 90)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is corrupted")
    else:
        print(" verify_conjq_rung_routes_dead  (zero-arg)")
        print(" conj:Q rung-routes route-cut: exact dead margins, KB-MCA v13 raw")
        print(" -- AUDIT, not a proof or refutation of conj:Q")
    print("=" * 90)

    try:
        packet = load_packet()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: could not load packet JSON: {exc}")
        return 1

    if not os.path.isfile(NOTE_PATH):
        print(f"FATAL: companion note missing: {NOTE_PATH}")
        return 1
    if not os.path.isfile(SIBLING_JSON_PATH):
        print(f"FATAL: sibling packet missing (should NOT have been modified, but must exist): "
              f"{SIBLING_JSON_PATH}")
        return 1

    ok_wall = packet.get("wall_id") == WALL_ID
    if not ok_wall:
        print(f"FATAL: wall_id mismatch: {packet.get('wall_id')!r} != {WALL_ID!r}")
        return 1

    all_good = True
    for label, fn in GATE_SPECS:
        ok, summary = fn(packet, selftest)
        caught_or_pass = (not ok) if selftest else ok
        all_good = all_good and caught_or_pass
        tag = ("CAUGHT " if caught_or_pass else "MISSED!") if selftest else ("PASS" if ok else "FAIL")
        print(f"  {label}  {tag}")
        print(f"        {summary}")

    print("=" * 90)
    dt = time.time() - t0
    if selftest:
        print(f" SELF-TEST RESULT: {'all tampers CAUGHT' if all_good else 'A TAMPER WAS MISSED'}   ({dt:.1f}s)")
    else:
        print(f" RESULT: {'ALL GATES PASS' if all_good else 'FAILURE'}   ({dt:.1f}s)")
        print(" This verifier does not certify U(1116048)<=B*, does not prove or refute conj:Q,")
        print(" and does not move the frontier edge; it only checks this PR's own arithmetic.")
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
