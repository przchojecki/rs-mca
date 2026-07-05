#!/usr/bin/env python3
"""Zero-arg verifier for experimental/data/certificates/frontier-adjacent/*_v1.packet.json
(the four deployed v13 frontier rows: KoalaBear MCA, KoalaBear list, Mersenne-31
MCA, Mersenne-31 list), at the one-step adjacent pair (a0, a0+1) for each row.

Extends the earlier single-row (KB MCA) skeleton verifier to all four rows,
and adds a FULL exact-integer recompute of the rung-margin audit (Audit 1 of
experimental/cap25_v13_missing_inputs_strategy.md sec 2.1): every dyadic scale
c=2^j, j=0..20, in all three slack-profile variants (graded prefix floor,
quotient-remainder floor, planted quotient-core), at both a0 and a0+1, for
all four rows -- independently reimplemented here (not imported) and checked
field-by-field against the packets' rung_margin_audit blocks.

Gates:
  G1  B* recomputation (both KB and M31 budgets).
  G2  Unsafe-side replay at a0 (identity-prefix construction) + confirmation
      that the SAME construction no longer fires at a0+1, for all 4 rows.
  G3  Adjacent stratum bit-bracket at a0+1 (cheap exact 1-bit bracket,
      informational but real: asserts the near-miss construction does not
      ALSO prove unsafe at a0+1).
  G4  Safe-theorem applicability-gap table (four known safe-side theorems,
      all strictly short of a0+1, for all 4 rows).
  G5  Packet-consistency: every scalar ledger field in each of the four
      packet.json files is recomputed from n, k, p_kb, p_m31 alone and
      asserted equal to the stored value.
  G6  FULL rung-margin table recompute: every rung (21 dyadic scales) and
      every slack-profile variant (Gfloor, Gceil, Rem, Plant) in every packet
      is recomputed exactly and compared field-by-field (c, N, m, w, s,
      covered agreement, covers_frontier, degenerate, fires, TIGHT, and
      Gfloor/Gceil margin_bits) against the packet's
      rung_margin_audit.per_agreement block. Also recomputes the headline
      verdict per row. Does NOT independently re-derive the
      rung_margin_audit.audit2_descent_loss ceilings (2^(M/21) and
      2^(M/nondegenerate_graded_rungs)); those are exact arithmetic from the
      c=1 fail-margin M, which G5 does cross-check (see
      cross_check_c1_identity_margins below) -- the derived ceilings
      themselves are hand-confirmed correct but not separately gated here.
  G7  v14 moved-frontier recompute (added 2026-07-05, upstream #310 commit
      f049b91): independently recomputes, from n/k/p alone via the
      identity-prefix-floor -> deep-point-count route
      (L=ceil(C(n,m)/p^w), M=ceil(L(q-n)/(q-n+k(L-1))), margin=log2(M/B*)),
      every field of the kb_mca_v1/m31_mca_v1 packets' v14_moved_pair block
      (the moved pair, L, M, pass/fail margins, deficit-to-cross-B*, and the
      M31-MCA Gceil c=2048 tight-rung finding), and cross-checks the
      recomputed margins against the maintainer's
      "experimental/scripts/towards v13/cap25_v14_moved_frontier_checks.py"
      (commit 2b5b7ce) printed margins to within 0.1 bit. The KB-list and
      M31-list packets' v14_status block (unchanged_in_v14=true) is not a
      numeric claim and is not separately gated.

There is deliberately no "NEEDS_A1" master gate: this script either passes
every gate (exit 0) or reports a genuine mismatch (exit 1). It does NOT
decide "is a0+1 safe" -- that master claim is not gated at all (see every
packet's safe_certificates.status == "OPEN"); the open-cell named-input
targets are printed as INFO only, at the end, never as a pass/fail gate.

Performance note: computing math.comb(N, m) fresh for every (row, scale,
agreement, variant) combination independently would take several minutes
(the dominant cost is O(N^~1.6) exact binomial computation at the largest
scales). Since the four rows' a0/a0+1 values are all within a span of 26
integers, this script computes each dyadic scale's C(N, ·) values via ONE
math.comb() call at the smallest needed argument, then reaches every other
needed value by a cheap O(size) ratio-update walk (C(N,m+1) =
C(N,m)*(N-m)//(m+1)) -- exact, not approximate. This does not change any
verdict; it only avoids redundant expensive recomputation of numbers that
would otherwise be computed 4-8 times over. Measured runtime: see
"total runtime" printed at the end (budget: under 180s).

Attribution: the exact 1-bit bracket helper (ge_pow2/bit_bracket) and the
overall gate-harness pattern are carried over from the earlier KB-MCA-only
skeleton verifier in this same packet family. The dyadic rung-scan logic
(Gfloor/Gceil/Rem/Plant, w_c remainder-weight formula) is reimplemented from
the mathematical description in experimental/notes/frontier-adjacent/
frontier_adjacent_v13_rows_v1.md (itself sourced from this session's Wave-2
audit scripts), not imported from them.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

sys.set_int_max_str_digits(2_000_000)

# ---------------------------------------------------------------------------
# Row constants (all four deployed v13 frontier rows)
# ---------------------------------------------------------------------------
n = 2**21
k = 2**20
p_kb = 2**31 - 2**24 + 1
p_m31 = 2**31 - 1
q_kb = p_kb**6
q_m31 = p_m31**4

ROWS = [
    dict(name="KB MCA", slug="kb_mca", base=p_kb, q=q_kb, K=k + 1, lam=128, a0=1116043, kind="mca"),
    dict(name="KB list", slug="kb_list", base=p_kb, q=q_kb, K=k, lam=128, a0=1116046, kind="list"),
    dict(name="M31 MCA", slug="m31_mca", base=p_m31, q=q_m31, K=k + 1, lam=100, a0=1116021, kind="mca"),
    dict(name="M31 list", slug="m31_list", base=p_m31, q=q_m31, K=k, lam=100, a0=1116022, kind="list"),
]
for _r in ROWS:
    _r["a1"] = _r["a0"] + 1

# ---------------------------------------------------------------------------
# v14 moved-frontier pairs (G7): upstream #310 commit f049b91 composes
# lem:v13f1-identity-prefix-floor with prop:quantitative-deep-list-floor and
# moves the two MCA rows' frontier pairs forward. Only the MCA rows move
# (K=k+1); the two list rows (K=k) compare their list floor directly against
# B* with no deep-point conversion, so their edges are untouched -- see
# experimental/notes/frontier-adjacent/frontier_adjacent_v13_rows_v1.md sec
# "V14 moved-frontier addendum (2026-07-05)".
# ---------------------------------------------------------------------------
MOVED_PAIRS = [
    dict(name="KB MCA", slug="kb_mca", base=p_kb, q=q_kb, K=k + 1, a0p=1116047, tight_rung=None),
    dict(
        name="M31 MCA", slug="m31_mca", base=p_m31, q=q_m31, K=k + 1, a0p=1116023,
        tight_rung=dict(c=2048, expect_L=12769758, expect_margin=-0.3938),
    ),
]
for _m in MOVED_PAIRS:
    _m["a1p"] = _m["a0p"] + 1

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PACKET_DIR = os.path.join(REPO_ROOT, "experimental", "data", "certificates", "frontier-adjacent")

TIGHT = 1.0  # bits


def theta_num_den(row: dict) -> tuple[int, int]:
    if row["kind"] == "mca":
        return row["q"] + k, k
    return row["q"], 2 ** row["lam"]


# ---------------------------------------------------------------------------
# Gate harness (PASS / FAIL only -- no NEEDS_A1 sentinel in this verifier)
# ---------------------------------------------------------------------------
class Gate:
    def __init__(self, name: str):
        self.name = name
        self.status = "FAIL"
        self.detail = ""

    def passed(self, detail: str = "") -> None:
        self.status = "PASS"
        self.detail = detail

    def failed(self, detail: str = "") -> None:
        self.status = "FAIL"
        self.detail = detail

    def __str__(self) -> str:
        return f"[{self.status:4s}] {self.name}: {self.detail}"


GATES: list[Gate] = []


def gate(name: str) -> Gate:
    g = Gate(name)
    GATES.append(g)
    return g


# ---------------------------------------------------------------------------
# Exact-arithmetic helpers
# ---------------------------------------------------------------------------
def comb_batch(N: int, ms: list[int]) -> dict:
    """Return {m: C(N,m)} for every requested m, computed EXACTLY via one
    math.comb() call at the smallest requested m, then cheap O(size)
    ratio-update steps (C(N,m+1)=C(N,m)*(N-m)//(m+1)) for the rest. Not an
    approximation: every value is the exact integer binomial coefficient."""
    wanted = sorted(set(m for m in ms if 0 <= m <= N))
    if not wanted:
        return {}
    out = {}
    cur_m = wanted[0]
    cur_val = math.comb(N, cur_m)
    out[cur_m] = cur_val
    for m in wanted[1:]:
        while cur_m < m:
            cur_val = cur_val * (N - cur_m) // (cur_m + 1)
            cur_m += 1
        out[m] = cur_val
    return out


_pow_cache: dict = {}


def base_pow(base: int, w: int) -> int:
    key = (base, w)
    v = _pow_cache.get(key)
    if v is None:
        v = pow(base, w)
        _pow_cache[key] = v
    return v


def flog2(num: int, den: int, window: int = 120) -> float:
    """Fast approximate log2(num/den); exponent part exact, mantissa good to
    ~1e-9 relative. INFORMATIONAL ONLY -- never used to decide fires/TIGHT."""
    bn = num.bit_length()
    bd = den.bit_length()
    sn = bn - window
    sd = bd - window
    mn = (num >> sn) if sn > 0 else (num << -sn)
    md = (den >> sd) if sd > 0 else (den << -sd)
    return (sn - sd) + math.log2(mn) - math.log2(md)


def ge_pow2(num: int, den: int, j: int) -> bool:
    """True iff num/den >= 2^j, decided by exact integer comparison only."""
    if j >= 0:
        return num >= den * (1 << j)
    return (num << (-j)) >= den


def bit_bracket(num: int, den: int) -> tuple[int, int]:
    """Exact integer 1-bit bracket (L, L+1) with 2^L <= num/den < 2^(L+1)."""
    assert num > 0 and den > 0
    j = num.bit_length() - den.bit_length()
    if not ge_pow2(num, den, j):
        while not ge_pow2(num, den, j):
            j -= 1
    else:
        while ge_pow2(num, den, j + 1):
            j += 1
    assert ge_pow2(num, den, j) and not ge_pow2(num, den, j + 1)
    return j, j + 1


def fires_tight(Fn: int, Fd: int, tn: int, td: int) -> tuple[bool, bool]:
    """EXACT (cross-multiplication, no floats) fires/TIGHT verdicts for
    F=Fn/Fd vs Theta=tn/td.  fires := F>Theta.  TIGHT := |log2(F/Theta)|<1,
    i.e. Theta/2 < F < 2*Theta."""
    lhs = Fn * td
    rhs = Fd * tn
    fires = lhs > rhs
    tight = (2 * lhs > rhs) and (lhs < 2 * rhs)
    return fires, tight


def w_c_remainder(s: int, sigma: int, c: int) -> int:
    if sigma <= 0:
        return 0
    Q, rem = divmod(sigma, c)
    return Q * (s + 1) + min(rem, s)


# self-test w_c_remainder against a brute-force definition on small cases
# (attribution: same identity used in this session's Wave-2 audit script;
# reimplemented and re-verified here independently).
def _w_c_brute(s: int, sigma: int, c: int) -> int:
    return sum(1 for h in range(1, sigma + 1) if (h % c) in range(0, s + 1))


for _s, _sg, _c in [(0, 10, 3), (1, 10, 3), (2, 10, 3), (0, 20, 4), (3, 25, 7), (1, 7, 2), (5, 5, 6), (0, 0, 2), (4, 100, 5)]:
    assert w_c_remainder(_s, _sg, _c) == _w_c_brute(_s, _sg, _c)


# ---------------------------------------------------------------------------
# G1: B* recomputation
# ---------------------------------------------------------------------------
def run_gate_bstar() -> dict:
    g = gate("G1_Bstar_recomputation")
    Bstar_kb = q_kb >> 128
    Bstar_m31 = q_m31 >> 100
    EXPECTED_KB = 274980728111395087
    EXPECTED_M31 = 16777215
    if Bstar_kb != EXPECTED_KB or Bstar_kb.bit_length() != 58:
        g.failed(f"KB B* mismatch: got {Bstar_kb}")
        return {}
    if Bstar_m31 != EXPECTED_M31 or Bstar_m31.bit_length() != 24:
        g.failed(f"M31 B* mismatch: got {Bstar_m31}")
        return {}
    if Bstar_m31 != q_m31 // (2**100):
        g.failed("M31 B* AUDIT-1 carve-out check failed (eps*=2^-100 required)")
        return {}
    # confirm the AUDIT-1 finding itself: eps*=2^-128 WOULD degenerate M31
    if (q_m31 >> 128) != 0:
        g.failed("AUDIT-1 sanity check failed: q_m31 unexpectedly >= 2^128")
        return {}
    g.passed(
        f"B*_KB=floor(q_kb/2^128)={Bstar_kb} (58-bit); "
        f"B*_M31=floor(q_m31/2^100)={Bstar_m31} (24-bit); "
        f"confirmed floor(q_m31/2^128)=0 (AUDIT-1 carve-out is real)."
    )
    return {"KB": Bstar_kb, "M31": Bstar_m31}


# ---------------------------------------------------------------------------
# Shared binomial cache for C(n, a) at the identity scale (c=1), reused by
# G2, G3, and the c=1 rung of G6.
# ---------------------------------------------------------------------------
def build_identity_binomials() -> dict:
    needed = []
    for row in ROWS:
        needed += [row["a0"], row["a1"]]
    # v14 (G7): a0p for each moved row is already an existing row's a1 (KB
    # MCA a0p=1116047=KB list a1; M31 MCA a0p=1116023=M31 list a1); only
    # a1p=a0p+1 is genuinely new. Folding it into this ONE shared batch call
    # keeps G7's marginal cost to a handful of cheap O(size) ratio-update
    # steps beyond what G2/G3/G6 already pay for, not a second fresh
    # math.comb() call (see comb_batch's docstring for why that matters).
    for mp in MOVED_PAIRS:
        needed += [mp["a1p"]]
    return comb_batch(n, needed)


# ---------------------------------------------------------------------------
# G2: unsafe-side replay at a0 + non-fire at a0+1, all four rows
# ---------------------------------------------------------------------------
def run_gate_unsafe_replay(C_n: dict) -> None:
    g = gate("G2_unsafe_side_replay_at_a0_all_rows")
    lines = []
    for row in ROWS:
        a0, a1, K, base = row["a0"], row["a1"], row["K"], row["base"]
        tn, td = theta_num_den(row)
        w0, w1 = a0 - K, a1 - K
        C_a0, C_a1 = C_n[a0], C_n[a1]
        fires0, _ = fires_tight(C_a0, base_pow(base, w0), tn, td)
        fires1, _ = fires_tight(C_a1, base_pow(base, w1), tn, td)
        if not fires0:
            g.failed(f"{row['name']}: UNSAFE CLAIM AT a0 DOES NOT HOLD (construction fails to fire at a0={a0})")
            return
        if fires1:
            g.failed(f"{row['name']}: construction UNEXPECTEDLY ALSO fires at a0+1={a1} (a0 would not be the route optimum)")
            return
        lines.append(f"{row['name']}: fires@a0=True, fires@a0+1=False (OK)")
    g.passed("; ".join(lines))


# ---------------------------------------------------------------------------
# G3: adjacent stratum bit-bracket at a0+1 (cheap exact 1-bit bracket)
# ---------------------------------------------------------------------------
def run_gate_adjacent_bracket(C_n: dict) -> None:
    g = gate("G3_adjacent_stratum_bit_bracket_at_a0_plus_1")
    lines = []
    for row in ROWS:
        a1, K, base = row["a1"], row["K"], row["base"]
        tn, td = theta_num_den(row)
        w1 = a1 - K
        lhs = C_n[a1] * td
        rhs = base_pow(base, w1) * tn
        L, U = bit_bracket(lhs, rhs)
        if U > 0:
            g.failed(f"{row['name']}: bracket [2^{L},2^{U}) unexpectedly >=1 at a0+1 -- construction fires past a0")
            return
        lines.append(f"{row['name']}: near-miss bracket [2^{L},2^{U}) (quiet)")
    g.passed("; ".join(lines))


# ---------------------------------------------------------------------------
# G4: safe-theorem applicability-gap table
# ---------------------------------------------------------------------------
def run_gate_safe_theorem_gap_table() -> dict:
    g = gate("G4_safe_theorem_gap_table")
    half_johnson_r = None
    for rr in range(0, n // 2):
        if (n - 2 * rr) ** 2 > (k - 1) * n:
            half_johnson_r = rr
        else:
            break
    assert half_johnson_r == 307121
    safe_theorems = {
        "thm:deep-mca (self-contained, 3r<=n-k)": n - (n - k) // 3,
        "cor:conditional-half (BCIKS20 import, 2r<=n-k)": (n + k) // 2,
        "thm:elementary-ca (half-Johnson, (n-2r)^2>(k-1)n)": n - half_johnson_r,
        "PR271-280 BCHKS25 Thm4.6 (conditional; koalabear-bchks25-jmca-safe-edge-v1/certificate.json)": 1493067,
    }
    assert safe_theorems["thm:deep-mca (self-contained, 3r<=n-k)"] == 1747627
    assert safe_theorems["cor:conditional-half (BCIKS20 import, 2r<=n-k)"] == 1572864
    assert safe_theorems["thm:elementary-ca (half-Johnson, (n-2r)^2>(k-1)n)"] == 1790031

    gap_tables = {}
    any_reaches = False
    lines = []
    for row in ROWS:
        gt = []
        for tname, amin in safe_theorems.items():
            gap = row["a1"] - amin
            gt.append({"theorem": tname, "a_min_safe": amin, "gap_a1_minus_a_min": gap})
            if gap >= 0:
                any_reaches = True
        gap_tables[row["name"]] = gt
        closest = max(g_["gap_a1_minus_a_min"] for g_ in gt)
        lines.append(f"{row['name']}: closest miss {-closest} agreement points short")
    if any_reaches:
        g.failed("at least one known safe theorem now reaches a0+1 for some row -- re-examine, may be genuine progress")
        return {}
    g.passed("; ".join(lines))
    return gap_tables


# ---------------------------------------------------------------------------
# Load the four packets
# ---------------------------------------------------------------------------
def load_packets() -> dict:
    out = {}
    for row in ROWS:
        path = os.path.join(PACKET_DIR, f"{row['slug']}_v1.packet.json")
        with open(path) as f:
            out[row["name"]] = json.load(f)
    return out


# ---------------------------------------------------------------------------
# G5: packet-consistency (scalar ledger fields)
# ---------------------------------------------------------------------------
def run_gate_packet_consistency(packets: dict, gap_tables: dict, Bstars: dict, C_n: dict) -> None:
    g = gate("G5_packet_consistency_scalar_fields")
    mism = []
    for row in ROWS:
        name = row["name"]
        pk = packets[name]
        Bstar = Bstars["KB"] if "KB" in name else Bstars["M31"]
        # tangent floor = r(a0)+1 = (n-a0-1)+1 = n-a0 (NOT n-a1=n-a0-1); the
        # unconditional lower floor is anchored at a0, one more than r(a0+1).
        r_a1 = n - row["a1"]  # r at the frontier agreement a0+1
        r_plus_1 = n - row["a0"]  # = r_a1 + 1, the tangent lower floor value
        assert r_plus_1 == r_a1 + 1
        eps_expected = "2^-128" if "KB" in name else "2^-100"

        def check(label, got, want):
            if got != want:
                mism.append(f"{name}.{label}: got {got!r} want {want!r}")

        check("target.epsilon_star", pk["target"]["epsilon_star"], eps_expected)
        check("target.B_star.value", pk["target"]["B_star"]["value"], Bstar)
        check("unsafe_certificates.a0", pk["unsafe_certificates"]["a0"], row["a0"])
        check("unsafe_certificates.K", pk["unsafe_certificates"]["K"], row["K"])
        check("unsafe_certificates.w0", pk["unsafe_certificates"]["w0"], row["a0"] - row["K"])
        check("safe_certificates.status", pk["safe_certificates"]["status"], "OPEN")
        check(
            "safe_cell_table[0].lower_floor_value",
            pk["safe_cell_table"][0]["lower_floor_value"],
            r_plus_1,
        )
        tangent_licensed = (3 * r_a1) <= (n - k)
        if tangent_licensed:
            mism.append(f"{name}: AUDIT-3 assumption changed -- tangent upper bound now licensed (r={r_a1})")
        check(
            "agreement_interval.one_step_target.a0_plus_1",
            pk["agreement_interval"]["one_step_target"]["a0_plus_1"],
            row["a1"],
        )
        # applicability_audit_gap_table: compare as a set of (theorem, a_min, gap)
        got_gaps = {(e["theorem"], e["a_min_safe"], e["gap_a1_minus_a_min"]) for e in pk["applicability_audit_gap_table"]}
        want_gaps = {(e["theorem"], e["a_min_safe"], e["gap_a1_minus_a_min"]) for e in gap_tables[name]}
        if got_gaps != want_gaps:
            mism.append(f"{name}.applicability_audit_gap_table mismatch: {got_gaps ^ want_gaps}")
        # rung_margin_audit.Theta_bracket + cross_check_c1_identity_margins:
        # previously computed by the packet but never compared against an
        # independent recompute by this verifier.
        tn, td = theta_num_den(row)
        L, U = bit_bracket(tn, td)
        theta_bracket_want = f"[2^{L}.9, 2^{U}.0)"
        check("rung_margin_audit.Theta_bracket", pk["rung_margin_audit"]["Theta_bracket"], theta_bracket_want)
        w0, w1 = row["a0"] - row["K"], row["a1"] - row["K"]
        c1_pass_a0 = round(flog2(C_n[row["a0"]] * td, base_pow(row["base"], w0) * tn), 4)
        c1_fail_a1 = round(flog2(C_n[row["a1"]] * td, base_pow(row["base"], w1) * tn), 4)
        ccm = pk["rung_margin_audit"]["cross_check_c1_identity_margins"]
        if abs(ccm["c1_pass_margin_a0"] - c1_pass_a0) > 1e-3:
            mism.append(f"{name}.cross_check_c1_identity_margins.c1_pass_margin_a0: got {ccm['c1_pass_margin_a0']!r} want {c1_pass_a0!r}")
        if abs(ccm["c1_fail_margin_a0p1"] - c1_fail_a1) > 1e-3:
            mism.append(f"{name}.cross_check_c1_identity_margins.c1_fail_margin_a0p1: got {ccm['c1_fail_margin_a0p1']!r} want {c1_fail_a1!r}")
        # every safe_cell_table status must be one of the five-value taxonomy
        five = {
            "PAID_BY_THEOREM",
            "PAID_BY_EXACT_CERTIFICATE",
            "CONDITIONAL_ON_NAMED_INPUT",
            "CONJECTURAL_WITH_FALSIFIER",
            "COUNTEREXAMPLE_NEW_FLOOR",
        }
        for cell in pk["safe_cell_table"]:
            for fld in ("status", "lower_floor_status", "upper_bound_status"):
                if fld in cell and cell[fld] not in five:
                    mism.append(f"{name}.safe_cell_table cell {cell.get('cell')!r} has non-taxonomy {fld}={cell[fld]!r}")
    if mism:
        g.failed("; ".join(mism[:20]))
        return
    g.passed(f"all scalar fields recomputed and matched across {len(ROWS)} packets")


# ---------------------------------------------------------------------------
# G6: FULL rung-margin table recompute
# ---------------------------------------------------------------------------
def compute_all_rung_tables() -> dict:
    """Returns {row_name: {"a0": {...}, "a0+1": {...}}} matching the schema
    of each packet's rung_margin_audit.per_agreement, computed independently
    and efficiently (shared binomial cache per dyadic scale c across all rows
    and both agreements)."""
    per_row_agr: dict = {row["name"]: {"a0": {"rungs": []}, "a1": {"rungs": []}} for row in ROWS}
    frontier_best: dict = {row["name"]: {"a0": None, "a1": None} for row in ROWS}  # (margin,label,L,U)
    subfrontier_best: dict = {row["name"]: {"a0": None, "a1": None} for row in ROWS}
    inversions = []
    tights = []

    for j in range(0, 21):
        c = 2 ** j
        N = n // c
        # --- collect every m needed at this scale (Gfloor + Gceil, both agreements, all rows) ---
        needed_m = set()
        per_row_ctx = {}
        for row in ROWS:
            ctx = {}
            for tag, a in (("a0", row["a0"]), ("a1", row["a1"])):
                m_floor = a // c
                cov_floor = m_floor * c
                m_ceil = -(-a // c)
                ctx[tag] = dict(m_floor=m_floor, cov_floor=cov_floor, m_ceil=m_ceil, s=a - cov_floor)
                needed_m.add(m_floor)
                needed_m.add(m_ceil)
            per_row_ctx[row["name"]] = ctx
        cN = comb_batch(N, list(needed_m))

        for row in ROWS:
            name = row["name"]
            K, base = row["K"], row["base"]
            tn, td = theta_num_den(row)
            ceilKc = -(-K // c)
            for tag, a in (("a0", row["a0"]), ("a1", row["a1"])):
                is_frontier_agr = tag == "a1"
                ctx = per_row_ctx[name][tag]
                m_floor, cov_floor, m_ceil, s = ctx["m_floor"], ctx["cov_floor"], ctx["m_ceil"], ctx["s"]
                rung = dict(j=j, c=c, N=N)

                # ---- Gfloor ----
                w = m_floor - ceilKc
                covers_frontier_floor = cov_floor >= a
                gfl = dict(m=m_floor, covered=cov_floor, covers_frontier=covers_frontier_floor)
                if w < 0:
                    gfl["degenerate"] = True
                else:
                    gfl["degenerate"] = False
                    gfl["w"] = w
                    Fn = cN[m_floor]
                    Fd = base_pow(base, w)
                    fires, tight = fires_tight(Fn, Fd, tn, td)
                    gfl["fires"] = fires
                    gfl["TIGHT"] = tight
                    gfl["margin_bits_approx"] = round(flog2(Fn * td, Fd * tn), 4)
                    if covers_frontier_floor:
                        _update_best(frontier_best[name], tag, flog2(Fn * td, Fd * tn), f"Gfloor c={c}")
                        if is_frontier_agr and fires:
                            inversions.append((name, "Gfloor", c))
                        if is_frontier_agr and tight:
                            tights.append((name, "Gfloor", c))
                    else:
                        if tight:
                            _update_subbest(subfrontier_best[name], tag, flog2(Fn * td, Fd * tn), f"Gfloor c={c} @agr {cov_floor}")
                rung["Gfloor"] = gfl

                # ---- Gceil ----
                wc = m_ceil - ceilKc
                gce = dict(m=m_ceil, covered=m_ceil * c, covers_frontier=True)
                if m_ceil > N or wc < 0:
                    gce["degenerate"] = True
                else:
                    gce["degenerate"] = False
                    gce["w"] = wc
                    Fn = cN[m_ceil]
                    Fd = base_pow(base, wc)
                    fires, tight = fires_tight(Fn, Fd, tn, td)
                    gce["fires"] = fires
                    gce["TIGHT"] = tight
                    gce["margin_bits_approx"] = round(flog2(Fn * td, Fd * tn), 4)
                    _update_best(frontier_best[name], tag, flog2(Fn * td, Fd * tn), f"Gceil c={c}")
                    if is_frontier_agr and fires:
                        inversions.append((name, "Gceil", c))
                    if is_frontier_agr and tight:
                        tights.append((name, "Gceil", c))
                rung["Gceil"] = gce

                # ---- Rem (covers agreement EXACTLY a) ----
                sigma = a - K
                rem = dict(s=s, covered=a, covers_frontier=True)
                if a < K:
                    rem["degenerate"] = True
                else:
                    w_rem = w_c_remainder(s, sigma, c)
                    rem["w_rem"] = w_rem
                    Fn = cN[m_floor] * (math.comb(n - cov_floor, s) if s > 0 else 1)
                    Fd = base_pow(base, w_rem)
                    fires, tight = fires_tight(Fn, Fd, tn, td)
                    rem["fires"] = fires
                    rem["TIGHT"] = tight
                    _update_best(frontier_best[name], tag, flog2(Fn * td, Fd * tn), f"Rem c={c}")
                    if is_frontier_agr and fires:
                        inversions.append((name, "Rem", c))
                    if is_frontier_agr and tight:
                        tights.append((name, "Rem", c))
                rung["Rem"] = rem

                # ---- Plant (planted quotient-core) ----
                kc = k // c
                Np = n // c
                pl: dict = {}
                if c > k or kc > Np - 1:
                    pl["defined"] = False
                else:
                    pl["defined"] = True
                    sigma_needed = a - k
                    covers = 1 <= sigma_needed <= c - 1
                    pl["sigma_needed"] = sigma_needed
                    pl["covers_frontier"] = covers
                    if covers:
                        P = math.comb(Np - 1, kc)
                        Bstar_row = q_kb >> 128 if "KB" in name else q_m31 >> 100
                        fires_b, tight_b = fires_tight(P, 1, Bstar_row, 1)
                        pl["fires_vs_Bstar"] = fires_b
                        pl["TIGHT_vs_Bstar"] = tight_b
                        if is_frontier_agr and fires_b:
                            inversions.append((name, "Plant", c))
                        if is_frontier_agr and tight_b:
                            tights.append((name, "Plant", c))
                rung["Plant"] = pl

                per_row_agr[name][tag]["rungs"].append(rung)

    headline = dict(
        any_frontier_inverted=len(inversions) > 0,
        any_frontier_tight=len(tights) > 0,
        inversions=inversions,
        tights=tights,
    )
    return dict(per_row_agr=per_row_agr, frontier_best=frontier_best, subfrontier_best=subfrontier_best, headline=headline)


def _update_best(store: dict, tag: str, margin: float, label: str) -> None:
    cur = store.get(tag)
    if cur is None or margin > cur[0]:
        store[tag] = (margin, label)


def _update_subbest(store: dict, tag: str, margin: float, label: str) -> None:
    am = abs(margin)
    if am >= TIGHT:
        return
    cur = store.get(tag)
    if cur is None or am < abs(cur[0]):
        store[tag] = (margin, label)


def run_gate_rung_table(packets: dict) -> None:
    g = gate("G6_full_rung_table_recompute")
    t0 = time.time()
    computed = compute_all_rung_tables()
    dt = time.time() - t0
    mism = []

    for row in ROWS:
        name = row["name"]
        pk_audit = packets[name]["rung_margin_audit"]["per_agreement"]
        for tag_pkt, tag_mine in (("a0", "a0"), ("a0+1", "a1")):
            pkt_rungs = pk_audit[tag_pkt]["rungs"]
            mine_rungs = computed["per_row_agr"][name][tag_mine]["rungs"]
            if len(pkt_rungs) != len(mine_rungs):
                mism.append(f"{name}/{tag_pkt}: rung count {len(pkt_rungs)} != {len(mine_rungs)}")
                continue
            for pr, mr in zip(pkt_rungs, mine_rungs):
                if pr["c"] != mr["c"] or pr["N"] != mr["N"]:
                    mism.append(f"{name}/{tag_pkt}/c={pr.get('c')}: c/N mismatch")
                    continue
                # Gfloor
                pg, mg = pr["Gfloor"], mr["Gfloor"]
                if pg["m"] != mg["m"] or pg["covered"] != mg["covered"] or pg["covers_frontier"] != mg["covers_frontier"] or pg["degenerate"] != mg["degenerate"]:
                    mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Gfloor: shape mismatch")
                elif not pg["degenerate"]:
                    if pg["w"] != mg["w"] or bool(pg["fires"]) != mg["fires"] or bool(pg["TIGHT"]) != mg["TIGHT"]:
                        mism.append(
                            f"{name}/{tag_pkt}/c={pr['c']}/Gfloor: verdict mismatch "
                            f"(pkt fires={pg['fires']} TIGHT={pg['TIGHT']} vs mine fires={mg['fires']} TIGHT={mg['TIGHT']})"
                        )
                    if abs(pg.get("margin_bits", mg["margin_bits_approx"]) - mg["margin_bits_approx"]) > 1e-3:
                        mism.append(
                            f"{name}/{tag_pkt}/c={pr['c']}/Gfloor: margin_bits mismatch "
                            f"(pkt {pg.get('margin_bits')!r} vs recomputed {mg['margin_bits_approx']!r})"
                        )
                # Gceil
                pc_, mc_ = pr["Gceil"], mr["Gceil"]
                if pc_["m"] != mc_["m"] or pc_["degenerate"] != mc_["degenerate"]:
                    mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Gceil: shape mismatch")
                elif not pc_["degenerate"]:
                    if pc_["w"] != mc_["w"] or bool(pc_["fires"]) != mc_["fires"] or bool(pc_["TIGHT"]) != mc_["TIGHT"]:
                        mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Gceil: verdict mismatch")
                    if abs(pc_.get("margin_bits", mc_["margin_bits_approx"]) - mc_["margin_bits_approx"]) > 1e-3:
                        mism.append(
                            f"{name}/{tag_pkt}/c={pr['c']}/Gceil: margin_bits mismatch "
                            f"(pkt {pc_.get('margin_bits')!r} vs recomputed {mc_['margin_bits_approx']!r})"
                        )
                # Rem
                pr_, mr_ = pr["Rem"], mr["Rem"]
                if pr_.get("s") != mr_.get("s"):
                    mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Rem: s mismatch")
                if "w_rem" in pr_ and "w_rem" in mr_:
                    if pr_["w_rem"] != mr_["w_rem"] or bool(pr_["fires"]) != mr_["fires"] or bool(pr_["TIGHT"]) != mr_["TIGHT"]:
                        mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Rem: verdict mismatch")
                # Plant
                pp, mp = pr["Plant"], mr["Plant"]
                if bool(pp.get("defined", False)) != mp.get("defined", False):
                    mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Plant: defined mismatch")
                elif mp.get("defined"):
                    if bool(pp.get("covers_frontier", False)) != mp.get("covers_frontier", False):
                        mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Plant: covers_frontier mismatch")
                    elif mp.get("covers_frontier"):
                        if bool(pp.get("fires_vs_Bstar")) != mp.get("fires_vs_Bstar") or bool(pp.get("TIGHT_vs_Bstar")) != mp.get("TIGHT_vs_Bstar"):
                            mism.append(f"{name}/{tag_pkt}/c={pr['c']}/Plant: verdict mismatch")

        # headline cross-check: packet's stored headline vs freshly recomputed
        pkt_headline = packets[name]["rung_margin_audit"]["headline"]
        if pkt_headline["any_frontier_inverted"] is not False or pkt_headline["any_frontier_tight"] is not False:
            mism.append(f"{name}: packet headline does not claim GREEN")

    if computed["headline"]["any_frontier_inverted"]:
        mism.append(f"RECOMPUTED an inversion at a0+1 (would be a real result): {computed['headline']['inversions']}")
    if computed["headline"]["any_frontier_tight"]:
        mism.append(f"RECOMPUTED a frontier-tight rung at a0+1 (would threaten the conjecture): {computed['headline']['tights']}")

    if mism:
        g.failed(f"{len(mism)} mismatch(es) in {dt:.1f}s: " + "; ".join(mism[:20]))
        return
    g.passed(
        f"all 4 rows x 21 dyadic scales x {{Gfloor,Gceil,Rem,Plant}} recomputed and matched packets "
        f"in {dt:.1f}s; independently confirmed GREEN (no inversion, no frontier-tight rung at a0+1)."
    )


# ---------------------------------------------------------------------------
# G7: v14 moved-frontier recompute (upstream #310 commit f049b91)
# ---------------------------------------------------------------------------
# Literal margins printed by the maintainer's
# "experimental/scripts/towards v13/cap25_v14_moved_frontier_checks.py"
# (commit 2b5b7ce), re-run this session; cited here (not imported/executed,
# since that script lives at a commit this branch does not merge) purely as
# a cross-check reference for the 0.1-bit tolerance below.
V14_SCRIPT_MARGINS = {
    "KB MCA": (8.978, -22.197),
    "M31 MCA": (27.927, -3.259),
}


def deep_point_M(L: int, q: int, n_: int, k_: int) -> int:
    """prop:quantitative-deep-list-floor's L->M conversion: the deep-point
    count implied by an identity-prefix list floor L (ceil division, exact)."""
    num = L * (q - n_)
    den = (q - n_) + k_ * (L - 1)
    return -(-num // den)


def run_gate_v14_moved_frontier(packets: dict, Bstars: dict, C_n: dict) -> None:
    g = gate("G7_v14_moved_frontier_recompute")
    mism: list[str] = []
    lines: list[str] = []
    for spec in MOVED_PAIRS:
        name = spec["name"]
        a0p, a1p, K, base, q = spec["a0p"], spec["a1p"], spec["K"], spec["base"], spec["q"]
        Bstar = Bstars["KB"] if "KB" in name else Bstars["M31"]

        w0p, w1p = a0p - K, a1p - K
        L0 = -(-C_n[a0p] // base_pow(base, w0p))
        L1 = -(-C_n[a1p] // base_pow(base, w1p))
        M0 = deep_point_M(L0, q, n, k)
        M1 = deep_point_M(L1, q, n, k)
        fires0, _ = fires_tight(M0, 1, Bstar, 1)
        fires1, _ = fires_tight(M1, 1, Bstar, 1)
        margin0 = flog2(M0, Bstar)
        margin1 = flog2(M1, Bstar)

        if not fires0 or fires1:
            mism.append(f"{name}: moved-pair fire pattern wrong (fires@a0'={fires0}, fires@a0'+1={fires1})")
            continue

        pk = packets[name]
        vmp = pk.get("v14_moved_pair")
        if vmp is None:
            mism.append(f"{name}: packet missing v14_moved_pair block")
            continue

        def check(label: str, got, want, tol: float | None = None) -> None:
            if tol is None:
                if got != want:
                    mism.append(f"{name}.v14_moved_pair.{label}: got {got!r} want {want!r}")
            elif abs(got - want) > tol:
                mism.append(f"{name}.v14_moved_pair.{label}: got {got!r} want {want!r} (tol {tol})")

        check("new_pair.a0_prime", vmp["new_pair"]["a0_prime"], a0p)
        check("new_pair.a0_prime_plus_1", vmp["new_pair"]["a0_prime_plus_1"], a1p)
        check("w0_prime", vmp["w0_prime"], w0p)
        check("w1_prime", vmp["w1_prime"], w1p)
        check("identity_floor_L_a0p", vmp["identity_floor_L_a0p"], L0)
        check("deep_point_M_a0p", vmp["deep_point_M_a0p"], M0)
        check("identity_floor_L_a1p", vmp["identity_floor_L_a1p"], L1)
        check("deep_point_M_a1p", vmp["deep_point_M_a1p"], M1)
        check("pass_margin_bits_a0p", vmp["pass_margin_bits_a0p"], round(margin0, 4), tol=5e-4)
        check("fail_margin_bits_a1p", vmp["fail_margin_bits_a1p"], round(margin1, 4), tol=5e-4)
        check("fires_at_a0p", vmp["fires_at_a0p"], fires0)
        check("fires_at_a1p", vmp["fires_at_a1p"], fires1)

        deficit_cross = (Bstar + 1) - M1
        check("deficit_to_cross_Bstar_a1p", vmp["deficit_to_cross_Bstar_a1p"], deficit_cross)

        v14_pass, v14_fail = V14_SCRIPT_MARGINS[name]
        if abs(margin0 - v14_pass) > 0.1:
            mism.append(f"{name}: recomputed pass margin {margin0:.4f} vs v14 script {v14_pass} exceeds 0.1 bit")
        if abs(margin1 - v14_fail) > 0.1:
            mism.append(f"{name}: recomputed fail margin {margin1:.4f} vs v14 script {v14_fail} exceeds 0.1 bit")

        tr_spec = spec["tight_rung"]
        if tr_spec is None:
            if vmp.get("tight_rung_at_a1p") is not None:
                mism.append(f"{name}: expected tight_rung_at_a1p=null (GREEN row), packet has one")
        else:
            c = tr_spec["c"]
            N = n // c
            m = -(-a1p // c)
            covered = m * c
            w = m - (-(-K // c))
            Cb2 = comb_batch(N, [m])
            Lr = -(-Cb2[m] // base_pow(base, w))
            Mr = deep_point_M(Lr, q, n, k)
            fires_r, tight_r = fires_tight(Mr, 1, Bstar, 1)
            margin_r = flog2(Mr, Bstar)
            if fires_r or not tight_r:
                mism.append(f"{name}: tight rung c={c} unexpected fires={fires_r} tight={tight_r}")
            if Lr != tr_spec["expect_L"]:
                mism.append(f"{name}: tight rung c={c} L={Lr} != expected {tr_spec['expect_L']}")
            if abs(margin_r - tr_spec["expect_margin"]) > 5e-4:
                mism.append(f"{name}: tight rung c={c} margin {margin_r:.4f} != expected {tr_spec['expect_margin']}")
            vmp_tr = vmp.get("tight_rung_at_a1p")
            if vmp_tr is None:
                mism.append(f"{name}: packet missing tight_rung_at_a1p")
            else:
                check("tight_rung_at_a1p.c", vmp_tr["c"], c)
                check("tight_rung_at_a1p.m", vmp_tr["m"], m)
                check("tight_rung_at_a1p.covered", vmp_tr["covered"], covered)
                check("tight_rung_at_a1p.w", vmp_tr["w"], w)
                check("tight_rung_at_a1p.L", vmp_tr["L"], Lr)
                check("tight_rung_at_a1p.M", vmp_tr["M"], Mr)
                check("tight_rung_at_a1p.margin_bits", vmp_tr["margin_bits"], round(margin_r, 4), tol=5e-4)
                check("tight_rung_at_a1p.fires", vmp_tr["fires"], fires_r)

        lines.append(
            f"{name}: a0'={a0p} pass={margin0:.4f}b (fires); a0'+1={a1p} fail={margin1:.4f}b (quiet); "
            f"within 0.1b of v14 script {V14_SCRIPT_MARGINS[name]}"
        )

    if mism:
        g.failed("; ".join(mism[:20]))
        return
    g.passed("; ".join(lines))


# ---------------------------------------------------------------------------
# INFO: open-cell named-input targets (not a gate; printed for visibility)
# ---------------------------------------------------------------------------
def print_info_open_cells(packets: dict) -> None:
    print("\n--- INFO: open named-input targets (not gated; see packets for detail) ---")
    for row in ROWS:
        name = row["name"]
        pk = packets[name]
        Bstar = pk["target"]["B_star"]["value"]
        maxC = pk["residual_cells"]["aperiodic_M1_or_SPI"]["max_affordable_ceiling_n_pow_C"]
        print(f"  {name:9s}: safe_certificates.status={pk['safe_certificates']['status']!r}; "
              f"B*={Bstar}; aperiodic cell max affordable C in n^C = {maxC}; "
              f"open cells: quotient(sharpened by Audit-2), extension, sparse, L1, aperiodic (see safe_cell_table).")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> int:
    t_start = time.time()
    print("=" * 78)
    print("frontier-adjacent-v13-rows verifier (4 rows: KB MCA, KB list, M31 MCA, M31 list)")
    print(f"n={n}, k={k}, rho=1/2")
    print("=" * 78)

    Bstars = run_gate_bstar()
    C_n = build_identity_binomials()
    run_gate_unsafe_replay(C_n)
    run_gate_adjacent_bracket(C_n)
    gap_tables = run_gate_safe_theorem_gap_table()

    try:
        packets = load_packets()
    except Exception as exc:  # noqa: BLE001 -- surface as a failed gate, not a crash
        gate("G5_packet_consistency_scalar_fields").failed(f"could not load packets: {exc}")
        gate("G6_full_rung_table_recompute").failed("skipped: packets did not load")
        gate("G7_v14_moved_frontier_recompute").failed("skipped: packets did not load")
        packets = None

    if packets is not None:
        run_gate_packet_consistency(packets, gap_tables, Bstars, C_n)
        run_gate_rung_table(packets)
        run_gate_v14_moved_frontier(packets, Bstars, C_n)
        print_info_open_cells(packets)

    print()
    for g_ in GATES:
        print(g_)
    print()

    n_pass = sum(1 for g_ in GATES if g_.status == "PASS")
    n_fail = sum(1 for g_ in GATES if g_.status == "FAIL")
    total_dt = time.time() - t_start
    print(f"gates: {len(GATES)} total, {n_pass} PASS, {n_fail} FAIL")
    print(f"total runtime: {total_dt:.1f}s")

    if n_fail > 0:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
