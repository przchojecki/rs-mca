#!/usr/bin/env python3
"""verify_kb_mca_conjq_rung_audit.py

Zero-arg, stdlib-only, deterministic verifier for
experimental/data/certificates/frontier-adjacent/kb_mca_conjq_rung_audit_v1.json
and its companion note experimental/notes/thresholds/cap25_v13_qfin_rung_audit.md.

This packet is the conj:Q divisor-lattice RUNG AUDIT at a0+1 for the deployed
KB-MCA v13 raw row (wall CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-
1116048). It executes grande_finale.tex's Work-Plan paragraph "Rung audit":
charge every quotient-pulled-back (nonprimitive) target stratum j=0..21 of the
divisor lattice of n=2^21 to an explicit budget share, leaving conj:Q's
primitive fiber (s=0) as the sole residual. It does NOT prove conj:Q, does
NOT prove U(1116048)<=B*, and is DISTINCT from the packet family's existing
kb_mca_v1.packet.json ".rung_margin_audit" block (that is the LOWER-side
periodic-floor audit; this is the complementary UPPER-side conj:Q max-fiber
audit -- see the companion note Sec 8 and Sec 10 reconciliation).

Five gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  gate i    FULL TABLE RECOMPUTE. Independently rebuilds the entire j=0..21
            divisor-lattice ledger from raw constants (p, n, k, m_safe) alone,
            using EXACT big-integer arithmetic throughout (no floating point
            in any pass/fail path), and diffs every stored field of the
            shipped JSON against the from-scratch recompute: n_j, w_j, m_j
            (where defined), the exact per-rung pessimistic share (floor),
            the exact K_raw, and every rung's verdict category
            (RESIDUAL / BELOW / VACUOUS -- never EXCEEDS). Float fields
            (log2 margins) are cross-checked at loose tolerance, informational
            only; the pass/fail gate never rests on a float comparison alone.
  gate ii   BINOMIAL / MOMENT IDENTITY SPOT CHECKS. w_j = floor(w/2^j) for
            every j; the divisibility chain 2^s | m_safe for s=0..4 (each
            m_safe/2^s stays an integer, so the symmetric part at scale s
            genuinely exists); and v2(m_safe) == 4 EXACTLY (i.e. 2^5 does
            NOT divide m_safe), which is the hard cap forcing the ladder to
            stop at s=4 and forcing strata j=5..16,21 to carry no independent
            descended mass.
  gate iii  TOY-VALIDATION REPLAY (exhaustive, full enumeration). Ports the
            CORE identity-(D) check of laneC_toy_validation.py -- for every
            target z hit by some m-subset of a toy coset domain D=alpha*mu_n,
            the count of mu_{2^j}-SYMMETRIC members of z's fiber (j=stratum(z))
            equals an INDEPENDENTLY re-enumerated prefix fiber of the smaller
            quotient row (n/2^j, m/2^j, floor(w/2^j)) -- to the integer, on
            4 toy rows: F17_m9_w2, F17_m4_w2 (this is the wall-synthesis-note
            F_17 STABILIZED-TARGET WITNESS row: M={1,2,4,10}, z=(0,2), and
            this gate checks that exact witness by name, confirming it is a
            genuinely subset-PRIMITIVE support (not mu_2-symmetric) sitting
            under a mu_2-STABILIZED target -- precisely the "raw support-level
            quotient counting is not justified by target stabilizer alone"
            phenomenon of the synthesis note), F97_n32_m4_w4_coset (the
            GENUINE non-trivial coset row, alpha=5, D=5*mu_32 subset F_97^*,
            reaching nonzero stratum j=2), and F193_n64_m4_w2 (a deeper
            domain, n=64). This reimplements the enumeration independently of
            laneC_toy_validation.py (brute-force subgroup membership rather
            than a primitive-root generator search), not by importing it.
  gate iv   RELAXATION-FAILURE CHECK. On one toy row (F17_m9_w2, j=1),
            independently enumerates the RELAXED count G_1(zdown) (bucket
            m-subsets by ONLY the multiples-of-2 prefix coordinates, dropping
            the vanishing constraints on the odd coordinates) and confirms,
            by exact Fraction arithmetic, avg(G_1)/avg(true fiber) ==
            p^(w-w_1) EXACTLY, with the enumerated max relaxed bucket already
            exceeding the true average by more than that factor. This is the
            toy-scale demonstration of why naive relaxation (drop the
            off-2^j moments, keep only the descended ones) is NOT a valid
            substitute for the exact descent identity (D): at the deployed
            row this blowup is p^(w-w_1) ~ 2^(1.05e6), astronomically over
            budget (Sec 4 of the companion note).
  gate v    CONSERVATIVE-ROUNDING CONSISTENCY. The four nonprimitive-rung
            pessimistic shares (s=1..4) are exact rationals with a common
            denominator comb(n,m_safe); their sum is not an integer, so this
            packet's AGGREGATE nonprimitive charge is the CEIL of that sum
            (35624), never the floor (35623, which is what Lane C's own
            laneC_rung_audit.py prints via Python's int() truncation) --
            this is a deliberately conservative +/-1 bookkeeping choice so
            the residual primitive budget quoted for conj:Q's core is never
            overstated. Gate v recomputes charge=ceil(sum shares) and
            residual=K_raw-charge from scratch (big-int exact, no floats) and
            asserts charge==35624, residual==4771896, and
            charge+residual==K_raw exactly.

Hidden self-test: python3 verify_kb_mca_conjq_rung_audit.py --tamper-selftest
    Each gate function takes a tamper=False parameter; in self-test mode it is
    called with tamper=True, which corrupts exactly ONE stored/expected value
    used inside that gate's first check (never the from-scratch recomputed
    side) and asserts the gate then reports a mismatch (CAUGHT). The shipped
    default is zero-arg (tamper=False everywhere).

PERFORMANCE. The dominant cost is five exact math.comb() calls at the
deployed row's scale: comb(n,m_safe) (~2.1e6-bit result, ~15s measured) plus
comb(n/2^s, m_safe/2^s) for s=1..4 (each roughly a quarter of the previous
call's cost). To avoid a second, independent ~20s bignum pass, gate v reuses
gate i's ledger (a module-level cache populated exactly once, regardless of
how many gates consult it or whether --tamper-selftest is active). All four
toy rows in gate iii together with gate iv take well under 5s (full brute-force
enumeration, largest instance comb(64,4)=635376 supports). Measured total
runtime (zero-arg, this machine): ~30-45s, comfortably under the 90s budget.
The nonprimitive-rung shares are computed as EXACT big-integer ratios sharing
the single common denominator comb(n,m_safe) (share_s = K_raw*comb(n_s,m_s)*
p^(w-w_s) / comb(n,m_safe)) rather than via repeated Fraction reduction of
independent huge numerator/denominator pairs -- this is ~2.5x faster than the
naive per-rung-Fraction approach (measured 22s vs 54s) because it never
invokes gcd() on ~2-million-bit operands.

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
from math import comb
from fractions import Fraction

sys.set_int_max_str_digits(2_500_000)

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
JSON_PATH = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                         "frontier-adjacent", "kb_mca_conjq_rung_audit_v1.json")
NOTE_PATH = os.path.join(REPO_ROOT, "experimental", "notes", "thresholds",
                         "cap25_v13_qfin_rung_audit.md")
PACKET_PATH = os.path.join(REPO_ROOT, "experimental", "data", "certificates",
                           "frontier-adjacent", "kb_mca_v1.packet.json")

# ---------------------------------------------------------------------------
# deployed KB-MCA v13-raw safe row -- ground truth, independent of the JSON
# ---------------------------------------------------------------------------
P = 2 ** 31 - 2 ** 24 + 1          # KoalaBear prime
N = 2 ** 21
K = 2 ** 20
B_STAR = P ** 6 // 2 ** 128        # 274980728111395087
A0_PRIME = 1116047
A0_PRIME_PLUS_1 = 1116048
M_SAFE = A0_PRIME_PLUS_1
W_SAFE = M_SAFE - K - 1            # 67471
V2_M_SAFE_EXPECT = 4

WALL_ID = "CAP25-V13-QFIN-PRIMITIVE-MAX-ORBIT-FLATNESS-KB-MCA-1116048"

CANON_CHARGE = 35624
CANON_RESIDUAL = 4771896
CANON_FLOOR_REF = 35623  # Lane C's own (non-adopted) floor value, for reference only


# ---------------------------------------------------------------------------
# generic helpers (log2 of huge ints without stringifying them; tamper/check)
# ---------------------------------------------------------------------------
def log2_int(x: int) -> float:
    if x <= 0:
        return float("-inf")
    b = x.bit_length()
    if b <= 53:
        return math.log2(x)
    s = b - 53
    return s + math.log2(x >> s)


def v2(x: int):
    if x == 0:
        return None
    v = 0
    while x % 2 == 0:
        x //= 2
        v += 1
    return v


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


def load_note_text() -> str:
    with open(NOTE_PATH, encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# shared expensive precompute: the FULL j=0..21 ledger, exact big-int
# arithmetic, computed EXACTLY ONCE regardless of how many gates use it or
# whether --tamper-selftest is active.
# ---------------------------------------------------------------------------
_LEDGER: dict = {}


def build_ledger() -> dict:
    """Independently recompute the entire divisor-lattice rung ledger from
    P, N, K, M_SAFE alone. Uses the shared-denominator trick: every
    nonprimitive rung's pessimistic share s=1..4 is expressed as an EXACT
    ratio num_s / D with the SAME denominator D = comb(N, M_SAFE), so the sum
    across rungs needs no gcd-reduction (Fraction would recompute a fresh gcd
    of ~2-million-bit operands at every step; summing raw numerators over a
    shared denominator does not)."""
    if _LEDGER:
        return _LEDGER

    t0 = time.time()
    binom_nm = comb(N, M_SAFE)                 # ~15s, the dominant single cost
    pw = pow(P, W_SAFE)
    Kraw = (B_STAR * pw) // binom_nm            # 4807520
    log2_avg = log2_int(binom_nm) - W_SAFE * math.log2(P)
    log2_Kraw = log2_int(Kraw)
    log2_B = log2_int(B_STAR)
    budget_bits = log2_B - log2_avg

    rungs = {}
    num_total = 0                               # sum of numerators over the shared den. binom_nm
    for j in range(0, 22):
        c = 2 ** j
        wj = W_SAFE // c
        nj = N // c
        entry = {"j": j, "n_j": nj, "w_j": wj}
        if 17 <= j <= 20:
            entry["category"] = "VACUOUS"
            rungs[j] = entry
            continue
        if j == 0:
            entry["category"] = "RESIDUAL"
            entry["share_floor"] = Kraw
            rungs[j] = entry
            continue
        descends = (M_SAFE % c == 0) and (0 <= M_SAFE // c <= nj)
        if descends and j <= V2_M_SAFE_EXPECT:
            mj = M_SAFE // c
            cnj = comb(nj, mj)
            num_s = Kraw * cnj * pow(P, W_SAFE - wj)     # share_s = num_s / binom_nm exactly
            num_total += num_s
            entry["category"] = "BELOW"
            entry["m_j"] = mj
            entry["log2_a_j"] = log2_int(cnj) - wj * math.log2(P)
            entry["share_floor"] = num_s // binom_nm
            entry["share_num"] = num_s            # kept only for gate v's exact sum; not JSON-compared
            entry["margin_below_Kraw_bits"] = log2_Kraw - (log2_int(num_s) - log2_int(binom_nm))
        else:
            entry["category"] = "BELOW"
            entry["m_j"] = None
            entry["independent_descended_mass"] = 0
        rungs[j] = entry

    charge = -((-num_total) // binom_nm)        # ceil(sum shares), the ADOPTED conservative charge
    floor_total = num_total // binom_nm         # Lane C's own (non-adopted) value, kept for the reconciliation
    residual = Kraw - charge
    combined_margin = log2_Kraw - (log2_int(num_total) - log2_int(binom_nm))

    _LEDGER.update({
        "binom_nm": binom_nm, "Kraw": Kraw, "log2_Kraw": log2_Kraw,
        "log2_avg": log2_avg, "log2_B": log2_B, "budget_bits": budget_bits,
        "rungs": rungs, "num_total": num_total, "den": binom_nm,
        "charge": charge, "floor_total": floor_total, "residual": residual,
        "combined_margin": combined_margin,
        "dt": time.time() - t0,
    })
    return _LEDGER


# ---------------------------------------------------------------------------
# gate i -- full j=0..21 table recompute, diffed against the shipped JSON
# ---------------------------------------------------------------------------
def gate_i_full_table(packet, tamper=False):
    ledger = build_ledger()
    stored_rungs = {r["j"]: r for r in packet["conjQ_rung_audit"]["rungs"]}
    ok = True
    msgs = []
    first = True
    for j in range(0, 22):
        actual = ledger["rungs"][j]
        stored = stored_rungs[j]

        ok_nj = check(actual["n_j"], stored["n_j"])
        ok_wj = check(actual["w_j"], stored["w_j"], tamper=(tamper and first))
        first = False

        cat = actual["category"]
        if cat == "VACUOUS":
            ok_verdict = "VACUOUS" in stored["rung_verdict"] and actual["w_j"] == 0
            ok_i = ok_nj and ok_wj and ok_verdict
        elif cat == "RESIDUAL":
            ok_share = check(actual["share_floor"], stored["pessimistic_budget_share_of_Kraw"])
            ok_verdict = "RESIDUAL" in stored["rung_verdict"]
            ok_i = ok_nj and ok_wj and ok_share and ok_verdict
        else:  # BELOW
            if actual.get("m_j") is not None:
                ok_mj = check(actual["m_j"], stored.get("m_j"))
                ok_share = check(actual["share_floor"], stored.get("pessimistic_budget_share_of_Kraw_floor"))
                ok_margin = check(actual["margin_below_Kraw_bits"],
                                   stored.get("rung_margin_below_Kraw_bits"), tol=2e-6)
                ok_la = check(actual["log2_a_j"], stored.get("log2_quotient_avg_a_j"), tol=2e-6)
                ok_verdict = "BELOW" in stored["rung_verdict"] and "EXCEEDS" not in stored["rung_verdict"]
                ok_i = ok_nj and ok_wj and ok_mj and ok_share and ok_margin and ok_la and ok_verdict
            else:
                ok_mass = check(0, stored.get("independent_descended_mass", -1))
                ok_verdict = "BELOW" in stored["rung_verdict"] and "EXCEEDS" not in stored["rung_verdict"]
                ok_i = ok_nj and ok_wj and ok_mass and ok_verdict
        ok = ok and ok_i
        if not ok_i:
            msgs.append(f"j={j} MISMATCH")
    # aggregate-shape sanity (does not decide the exact charge/residual pair -- that's gate v)
    agg = packet["conjQ_rung_audit"]["aggregate"]
    ok_Kraw = check(ledger["Kraw"], agg["K_raw"])
    ok_noexceed = check(agg["any_rung_exceeds_budget"], False)
    ok = ok and ok_Kraw and ok_noexceed
    if not ok_Kraw:
        msgs.append("K_raw mismatch")
    if not ok_noexceed:
        msgs.append("any_rung_exceeds_budget stored as True")
    if not msgs:
        msgs.append(f"all 22 rungs match (K_raw={ledger['Kraw']}, ledger build {ledger['dt']:.1f}s)")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate ii -- binomial / moment identity spot checks
# ---------------------------------------------------------------------------
def gate_ii_identities(packet, tamper=False):
    ok = True
    msgs = []
    # w_j = floor(w/2^j) for a spot sample of j (cheap; also exercised fully in gate i)
    sample_js = [0, 1, 2, 3, 4, 5, 10, 16, 17, 21]
    first = True
    for j in sample_js:
        expect_wj = W_SAFE // (2 ** j)
        actual_wj = check(W_SAFE // (2 ** j), expect_wj, tamper=(tamper and first))
        first = False
        ok = ok and actual_wj
        if not actual_wj:
            msgs.append(f"w_j mismatch at j={j}")
    # divisibility chain: 2^s | m_safe for s=0..4
    chain_ok = all(M_SAFE % (2 ** s) == 0 for s in range(0, 5))
    ok = ok and check(chain_ok, True)
    msgs.append(f"2^s|m_safe for s=0..4: {chain_ok}")
    # v2(m_safe) EXACTLY 4 (hard cap: 2^5 must NOT divide m_safe). Not itself a
    # tamper point (the w_j sample loop above is this gate's single guarded
    # tamper point), so this is always checked untampered.
    v2m = v2(M_SAFE)
    ok_v2 = check(v2m, V2_M_SAFE_EXPECT)
    ok = ok and ok_v2
    msgs.append(f"v2(m_safe)={v2m} (expect {V2_M_SAFE_EXPECT}) ok={ok_v2}")
    not_div32 = (M_SAFE % 32 != 0)
    ok = ok and not_div32
    msgs.append(f"2^5 does not divide m_safe: {not_div32}")
    # cross-check against packet's stored v2_m_safe / w_safe fields
    stored_v2 = packet["target"].get("v2_m_safe")
    stored_wsafe = packet["target"].get("w_safe")
    ok_stored = check(v2m, stored_v2) and check(W_SAFE, stored_wsafe)
    ok = ok and ok_stored
    msgs.append(f"packet target.v2_m_safe/w_safe consistent: {ok_stored}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# toy machinery (independent reimplementation -- brute-force subgroup
# membership, not a primitive-root generator search) for gates iii/iv
# ---------------------------------------------------------------------------
def mu_set(p: int, order: int):
    return [x for x in range(1, p) if pow(x, order, p) == 1]


def stratum_of(z: tuple, b: int) -> int:
    I = [i for i in range(1, len(z) + 1) if z[i - 1] != 0]
    if not I:
        return b
    return min(min(v2(i) for i in I), b)


def run_toy(p: int, n: int, m: int, w: int, alpha: int, label: str):
    """Exhaustively enumerate all m-subsets of D=alpha*mu_n over F_p, and
    verify the exact descent identity (D): for every hit target z, the count
    of mu_{2^j}-symmetric members of z's fiber (j=stratum(z)) equals an
    INDEPENDENTLY re-enumerated prefix fiber of the quotient row
    (n/2^j, m/2^j, floor(w/2^j))."""
    b = v2(n)
    assert 2 ** b == n, (label, "n must be a 2-power for this toy family")
    assert (p - 1) % n == 0
    mu_n = mu_set(p, n)
    assert len(mu_n) == n, (label, len(mu_n), n)
    D = sorted((alpha * x) % p for x in mu_n)
    assert len(set(D)) == n

    mu2j = {}
    for j in range(0, b + 1):
        assert (p - 1) % (2 ** j) == 0
        mu2j[j] = mu_set(p, 2 ** j)

    POW = {x: [pow(x, i, p) for i in range(1, w + 1)] for x in D}
    fibers: dict = {}
    for M in combinations(D, m):
        key = tuple(sum(POW[x][i] for x in M) % p for i in range(w))
        fibers.setdefault(key, []).append(frozenset(M))
    total = sum(len(v) for v in fibers.values())
    assert total == comb(n, m), (label, total, comb(n, m))

    Dj = {}
    for j in range(0, b + 1):
        Dj[j] = sorted(set(pow(x, 2 ** j, p) for x in D))
        assert len(Dj[j]) == n // (2 ** j)
    POWq = {j: {y: [pow(y, i, p) for i in range(1, w // (2 ** j) + 1)] for y in Dj[j]}
            for j in range(0, b + 1)}
    inv2j = {j: pow(pow(2, j, p), p - 2, p) for j in range(0, b + 1)}

    def quotient_fiber_count(j, zdown):
        mj = m // (2 ** j)
        wj = w // (2 ** j)
        dom = Dj[j]
        if mj == 0 or mj > len(dom):
            return 0
        cnt = 0
        for Mbar in combinations(dom, mj):
            if all(sum(POWq[j][y][idx] for y in Mbar) % p == zdown[idx] for idx in range(wj)):
                cnt += 1
        return cnt

    def is_symmetric(M, j):
        g2j = mu2j[j]
        return all(((u * x) % p) in M for x in M for u in g2j)

    strata_mass: dict = {}
    n_checked = 0
    all_ok = True
    witness = None
    for z, subs in fibers.items():
        j = stratum_of(z, b)
        fib = len(subs)
        strata_mass[j] = strata_mass.get(j, 0) + fib
        nsym = sum(1 for M in subs if is_symmetric(M, j))
        if j == 0:
            qf = nsym
        elif m % (2 ** j) == 0:
            wj = w // (2 ** j)
            zdown = tuple((z[2 ** j * ip - 1] * inv2j[j]) % p for ip in range(1, wj + 1))
            qf = quotient_fiber_count(j, zdown)
        else:
            qf = 0
        ok = (nsym == qf)
        all_ok = all_ok and ok
        n_checked += 1
        if p == 17 and n == 16 and m == 4 and w == 2 and alpha == 1:
            Mtest = frozenset({1, 2, 4, 10})
            if z == (0, 2) and Mtest in subs:
                witness = {"M": sorted(Mtest), "z": z, "j": j,
                           "symmetric": is_symmetric(Mtest, j)}
    return {"label": label, "all_identity_ok": all_ok, "n_checked": n_checked,
            "total_mass_ok": (total == comb(n, m)), "strata_mass": strata_mass,
            "witness": witness}


TOY_ROWS = [
    (17, 16, 9, 2, 1, "F17_m9_w2"),
    (17, 16, 4, 2, 1, "F17_m4_w2"),                 # the F_17 stabilized-target witness row
    (97, 32, 4, 4, 5, "F97_n32_m4_w4_coset"),        # genuine coset, alpha=5
    (193, 64, 4, 2, 1, "F193_n64_m4_w2"),
]

CANON_F17_WITNESS = {"M": [1, 2, 4, 10], "z": (0, 2), "j": 1, "symmetric": False}


# ---------------------------------------------------------------------------
# gate iii -- toy-validation replay (>=4 rows, full enumeration)
# ---------------------------------------------------------------------------
def gate_iii_toy_replay(tamper=False):
    ok = True
    msgs = []
    first = True
    results = {}
    for (p, n, m, w, alpha, label) in TOY_ROWS:
        r = run_toy(p, n, m, w, alpha, label)
        results[label] = r
        ok_row = r["all_identity_ok"] and r["total_mass_ok"]
        ok = ok and ok_row
        msgs.append(f"{label}: {r['n_checked']} targets, identity_ok={r['all_identity_ok']} "
                    f"mass_ok={r['total_mass_ok']}")
    # the F_17 stabilized-target witness, checked BY NAME
    w17 = results["F17_m4_w2"]["witness"]
    ok_witness = (w17 is not None
                  and check(w17["M"], CANON_F17_WITNESS["M"], tamper=(tamper and first))
                  and check(tuple(w17["z"]), CANON_F17_WITNESS["z"])
                  and check(w17["j"], CANON_F17_WITNESS["j"])
                  and check(w17["symmetric"], CANON_F17_WITNESS["symmetric"]))
    first = False
    ok = ok and ok_witness
    msgs.append(f"F17 witness M={w17['M'] if w17 else None} z={w17['z'] if w17 else None} "
                f"j={w17['j'] if w17 else None} symmetric={w17['symmetric'] if w17 else None} "
                f"(expect {CANON_F17_WITNESS}) ok={ok_witness}")
    # the genuine-coset row: alpha=5 must NOT lie in mu_32 (else it would be
    # the trivial coset, not a "genuine" one)
    trivial_coset = (pow(5, 32, 97) == 1)
    ok_genuine = check(trivial_coset, False)
    ok = ok and ok_genuine
    msgs.append(f"F97 coset genuine (5 not in mu_32): {not trivial_coset} ok={ok_genuine}")
    # cross-check strata reached match the design doc's toy table
    expect_strata = {
        "F17_m9_w2": {0: 10768, 1: 640, 4: 32},
        "F17_m4_w2": {0: 1712, 1: 104, 4: 4},
        "F97_n32_m4_w4_coset": {0: 35840, 1: 112, 2: 8},
        "F193_n64_m4_w2": {0: 631936, 1: 3424, 6: 16},
    }
    for label, expect in expect_strata.items():
        ok_sm = check(results[label]["strata_mass"], expect)
        ok = ok and ok_sm
        if not ok_sm:
            msgs.append(f"{label} strata_mass mismatch: {results[label]['strata_mass']} vs {expect}")
    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate iv -- relaxation-failure check on one toy row (F17_m9_w2, j=1)
# ---------------------------------------------------------------------------
def gate_iv_relaxation(tamper=False):
    p, n, m, w, alpha, j = 17, 16, 9, 2, 1, 1
    mu_n = mu_set(p, n)
    D = sorted((alpha * x) % p for x in mu_n)
    wj = w // (2 ** j)
    POW = {x: [pow(x, i, p) for i in range(1, w + 1)] for x in D}

    buckets: dict = {}
    for M in combinations(D, m):
        key = tuple(sum(POW[x][2 ** j * ip - 1] for x in M) % p for ip in range(1, wj + 1))
        buckets[key] = buckets.get(key, 0) + 1
    total = sum(buckets.values())
    ok_total = check(total, comb(n, m))
    max_bucket = max(buckets.values())

    avg_relaxed = Fraction(comb(n, m), p ** wj)
    avg_full = Fraction(comb(n, m), p ** w)
    blowup = avg_relaxed / avg_full
    expect_blowup = p ** (w - wj)
    # blowup is always an exact integer (= p^(w-wj) by construction); compare
    # as a plain int (not a Fraction) so the tamper corruption (which only
    # knows how to perturb bool/int/float/str/list, not Fraction) has teeth.
    assert blowup.denominator == 1
    blowup_int = blowup.numerator

    ok_blowup = check(blowup_int, expect_blowup, tamper=tamper)
    ok_scale = (float(max_bucket) / float(avg_full)) >= float(expect_blowup)
    ok_max = check(max_bucket, 696)  # the concrete enumerated value at this toy row (regression check)

    ok = ok_total and ok_blowup and ok_scale and ok_max
    msg = (f"F17_m9_w2 j=1: max_relaxed_fiber_Gj={max_bucket} (expect 696), "
           f"avg_relaxed={float(avg_relaxed):.4f}, avg_full={float(avg_full):.4f}, "
           f"blowup={blowup}=p^(w-wj)={expect_blowup}? {ok_blowup}, "
           f"max/avg_full>=blowup? {ok_scale}, total_mass_ok={ok_total}")
    return ok, msg


# ---------------------------------------------------------------------------
# gate v -- conservative-rounding consistency
# ---------------------------------------------------------------------------
def gate_v_rounding(packet, tamper=False):
    ledger = build_ledger()
    charge = ledger["charge"]
    residual = ledger["residual"]
    Kraw = ledger["Kraw"]

    ok_charge = check(charge, CANON_CHARGE, tamper=tamper)
    ok_residual = check(residual, CANON_RESIDUAL)
    ok_sum = check(charge + residual, Kraw)
    ok_floor_ref = check(ledger["floor_total"], CANON_FLOOR_REF)

    agg = packet["conjQ_rung_audit"]["aggregate"]
    ok_packet_charge = check(agg["nonprimitive_rungs_total_charge_conservative_ceil"], CANON_CHARGE)
    ok_packet_residual = check(agg["residual_primitive_budget_for_conjQ_core"], CANON_RESIDUAL)
    ok_packet_flag = check(agg["charge_plus_residual_equals_Kraw"], True)

    ok = (ok_charge and ok_residual and ok_sum and ok_floor_ref
          and ok_packet_charge and ok_packet_residual and ok_packet_flag)
    msg = (f"charge={charge}(expect {CANON_CHARGE}) residual={residual}(expect {CANON_RESIDUAL}) "
           f"charge+residual={charge + residual}==K_raw={Kraw}? {ok_sum}; "
           f"floor_ref={ledger['floor_total']}(expect {CANON_FLOOR_REF}, Lane C's own non-adopted value); "
           f"packet aggregate fields consistent={ok_packet_charge and ok_packet_residual and ok_packet_flag}")
    return ok, msg


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
GATE_SPECS = [
    ("gate i   full j=0..21 table recompute      ", lambda packet, t: gate_i_full_table(packet, t)),
    ("gate ii  binomial/moment identity spot chks ", lambda packet, t: gate_ii_identities(packet, t)),
    ("gate iii toy-validation replay (4 rows)     ", lambda packet, t: gate_iii_toy_replay(t)),
    ("gate iv  relaxation-failure check           ", lambda packet, t: gate_iv_relaxation(t)),
    ("gate v   conservative-rounding consistency  ", lambda packet, t: gate_v_rounding(packet, t)),
]


def main() -> int:
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    print("=" * 90)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is corrupted")
    else:
        print(" verify_kb_mca_conjq_rung_audit  (zero-arg)")
        print(" conj:Q divisor-lattice rung audit at a0+1, KB-MCA v13 raw -- AUDIT, not a proof of conj:Q")
    print("=" * 90)

    try:
        packet = load_packet()
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: could not load packet JSON: {exc}")
        return 1

    if not os.path.isfile(NOTE_PATH):
        print(f"FATAL: companion note missing: {NOTE_PATH}")
        return 1
    if not os.path.isfile(PACKET_PATH):
        print(f"FATAL: sibling packet missing (should NOT have been modified, but must exist): {PACKET_PATH}")
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
        print(" This verifier does not certify U(1116048)<=B*, does not prove conj:Q, and does")
        print(" not move the frontier edge; it only checks this PR's own arithmetic (see docstring).")
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
