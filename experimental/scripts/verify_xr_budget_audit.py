#!/usr/bin/env python3
"""verify_xr_budget_audit.py — DAG node xr_target_budget_audit (step-zero budget audit).

Recomputes, per clean-rate decision row, the exact integer aperiodic allowance

    s = B* - B_quot(A) - B_tan(A)

at the safe-side decision candidate A (first A beyond the last census-realizable
quotient-unsafe point) and at A+1, and prints the verdict per row:
s = 0  => face 4 is rigidity/emptiness;  s >= 1 => face 4 is bounded-multiplicity
forcing at multiplicity s+1.

Conventions (documented in experimental/notes/roadmaps/xr_budget_audit.md):
  B*      = floor(q_line / 2^128) exactly (s4 gate; qa3_e14 C4).
  B_quot  = census_bounded_scales class count (QA.7): coset-support classes at
            dyadic quotient scales N' | n active when N' <= n/t (s2 sect.5),
            l' cosets with l'/N' = j/n, j = n - A; l' must be integral
            (a union of l' cosets of size M = n/N' has j = l'*M exactly).
            Char-0 counts C(N', l') are UPPER bounds on the value-set class
            count, so computed s is a LOWER bound (safe direction).
  B_tan   = tangent staircase term, s2_paid_ledger.md sect.1:
            B_tan(A) <= n - A + 1 (PROVED-cited #147 staircase range).
            Exact ( = n - A + 1) on the fully-pinned envelope
            log2 q in [128, 166.4] (s8_s9 sect."assembly") -> pinned row only.
            For the 2^250 / 2^255.9 rows the staircase-active question is
            ambiguous: both variants 0 and n - A + 1 are carried (task spec).
  s range = [B* - B_quot_ub - (n-A+1),  B* - B_quot_strict - 0]
            with B_quot_ub the floor-rounded all-active-scale sum (conservative)
            and B_quot_strict the exact integral-l' count.

Stdlib only, deterministic, no network, no git. Exit 0 iff all PASS.
"""

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

PASS = []
FAIL = []

CERT_PATH = Path(
    "experimental/data/certificates/xr-budget-audit/"
    "xr_budget_audit_certificate.json"
)


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {name}" + (f"  ({detail})" if detail else ""))


def flag(name, detail=""):
    print(f"[FLAG] {name}" + (f"  ({detail})" if detail else ""))


# ---------------------------------------------------------------- B* per row

def iroot(x: int, r: int) -> int:
    """floor(x**(1/r)) for positive ints, exact (Newton + certify)."""
    if x < 0 or r < 1:
        raise ValueError
    g = 1 << (-(-x.bit_length() // r))  # >= true root
    while True:
        ng = ((r - 1) * g + x // g ** (r - 1)) // r
        if ng >= g:
            break
        g = ng
    while g ** r > x:
        g -= 1
    assert g ** r <= x < (g + 1) ** r
    return g


B_STAR_PINNED = 17 ** 32 >> 128                 # floor(17^32 / 2^128)
B_STAR_ROWC = 1 << 122                          # floor(2^250 / 2^128), exact
B_STAR_PRIZE = iroot(1 << 1279, 10)             # floor(2^(255.9-128)) = floor(2^127.9)

check("pinned B* = 6 (qa3_e14 C1(a) coherence)", B_STAR_PINNED == 6)
check("prize B* = floor(2^127.9) exact 10th root",
      B_STAR_PRIZE ** 10 <= (1 << 1279) < (B_STAR_PRIZE + 1) ** 10,
      f"B*={B_STAR_PRIZE} log2~{math.log2(B_STAR_PRIZE):.6f}")


# ------------------------------------------------------- census count engine

def strict_count(n, k, A, Np):
    """Exact census class count at scale N' for agreement A: C(N', j/M) if the
    ratio is realizable (M | j, 1 <= l' <= N'-1, trivial classes excluded),
    else 0. Char-0 upper bound on the value-set class count."""
    j = n - A
    M = n // Np
    if j % M:
        return 0
    lp = j // M
    if lp < 1 or lp > Np - 1:
        return 0
    return math.comb(Np, lp)


def floor_count(n, k, A, Np):
    """Floor-rounded variant: C(N', floor(j*N'/n)), trivial l' excluded.
    Plateau-constant (== the integral right-edge count); used only for the
    conservative B_quot upper bound."""
    lp = (n - A) * Np // n
    if lp < 1 or lp > Np - 1:
        return 0
    return math.comb(Np, lp)


def active_scales(n, A, k):
    """Dyadic N' | n with N' <= n/t, t = A - k (s2 sect.5), N' >= 2."""
    t = A - k
    out = []
    Np = 2
    while Np <= n and Np * t <= n:
        out.append(Np)
        Np *= 2
    return out


def bquot_strict(n, k, A):
    return max([strict_count(n, k, A, Np) for Np in active_scales(n, A, k)],
               default=0)


def bquot_ub(n, k, A):
    return sum(floor_count(n, k, A, Np) for Np in active_scales(n, A, k))


def edge_count(Np, RD):
    """Census count at the plateau right edge t = n/N': l' = N'(1-1/RD) - 1,
    i.e. C(N', N'/RD + 1) by symmetry — the same argument rho*N'+1 as
    prop:qfloor / the #213 A_2 and planted families."""
    return math.comb(Np, Np // RD + 1)


def deciding_scale(RD, bstar, n):
    """Smallest dyadic N' (RD | N') with edge_count > B*, certified upward
    monotone along the chain to N' = n (exact comb to 2^13, then the rigorous
    bound C(N,l) >= 2^(N*H(l/N))/(N+1))."""
    Np = RD
    while edge_count(Np, RD) <= bstar:
        Np *= 2
    dec = Np
    # upward closure: every larger dyadic scale also exceeds B*
    while Np <= n:
        if Np <= 1 << 13:
            ok = edge_count(Np, RD) > bstar
        else:
            l = Np // RD + 1
            x = l / Np
            h = -x * math.log2(x) - (1 - x) * math.log2(1 - x)
            ok = Np * h - math.log2(Np + 1) > math.log2(float(bstar)) + 1
        if not ok:
            raise AssertionError(f"chain not upward-closed at N'={Np}")
        Np *= 2
    return dec


# ------------------------------------------------------------- E14 ZM checks

def zm_negative_exact(n, k, A, q_log2_num, q_log2_den):
    """Exact: n^3 * C(n, j) * q^(1-t) < 1 with q = 2^(num/den), i.e.
    (n^3 C(n,j))^den < 2^(num*(t-1))."""
    t = A - k
    lhs = (n ** 3 * math.comb(n, n - A)) ** q_log2_den
    return lhs < 1 << (q_log2_num * (t - 1))


def zm_negative_entropy_ub(n, k, A, q_log2):
    """Prize scale: rigorous direction via C(n,j) <= 2^(n H(j/n)) (float H;
    margins here are ~1e11 bits, dwarfing float error)."""
    t = A - k
    x = (n - A) / n
    h = -x * math.log2(x) - (1 - x) * math.log2(1 - x)
    return 3 * math.log2(n) + n * h + q_log2 * (1 - t) < -1e6


# ------------------------------------------------------------------- the rows

# Cross-reference constants (cited, not computed here):
# #213 pipeline dyadic crossings at budget_bits=128 — fork commit d642a419,
# experimental/data/certificates/clean-rate-corridor-pipeline (git show only):
P213_DYADIC = {4: 256, 8: 256, 16: 512}
# qa3_e14_fm_margin_tables.md Table 1 A* (FM crossing) per row:
QA3_ASTAR = {("RowC", 4): 259, ("RowC", 8): 130, ("RowC", 16): 65,
             ("prize", 4): 556770474277, ("prize", 8): 279600463335,
             ("prize", 16): 140382131271}
# qa3_e14 Table 2 corridor left ends A_quot (continuous-beta convention):
QA3_AQUOT = {("RowC", 4): 263, ("RowC", 8): 133, ("RowC", 16): 67,
             ("prize", 4): 562650789977, ("prize", 8): 284000672694,
             ("prize", 16): 143186674147}

print()
print("== calibration row: pinned n=512, k=256, q=17^32 (rate 1/2) ==")
n, k, bstar = 512, 256, B_STAR_PINNED
# tangent-decided: B_tan = n - A + 1 exact (staircase envelope log2 q in
# [128,166.4] covers 32*log2 17 = 130.80 -> staircase active, s8_s9).
A = 507
check("pinned: A=506 unsafe by tangent alone (n-A+1 = 7 > B*)",
      512 - 506 + 1 > bstar)
check("pinned: strict census B_quot(506..508) = 0 (no coset class: 256 | j fails)",
      all(bquot_strict(n, k, a) == 0 for a in (506, 507, 508)))
check("pinned: quotient realizable-unsafe ends at N'=8 edge (C(8,3)=56>6, C(4,1)=4<=6)",
      edge_count(8, 2) == 56 and edge_count(8, 2) > bstar
      and math.comb(4, 1) <= bstar)
s_507 = bstar - (n - A + 1) - bquot_strict(n, k, A)
s_508 = bstar - (n - 508 + 1) - bquot_strict(n, k, 508)
check("pinned: safe-side candidate A = 507 (first total <= B*), s = 0 EXACT",
      s_507 == 0, f"B*=6, B_tan=6, B_quot=0")
check("pinned: s(A+1=508) = 1 EXACT", s_508 == 1)
flag("pinned DEDUP is load-bearing: the Paper-B A_2(2,2) = 1 trivial class, if "
     "added to B_tan without dedup, gives s = -1 at the PROVED-safe A=507; the "
     "N'=2 whole-line class is inside the tangent count (S1 dedup).")
print("VERDICT pinned: s = 0 at A=507 -> face 4 = RIGIDITY/EMPTINESS "
      "(calibration: reproduces the proved tangent-pinned 506/507 threshold); "
      "s = 1 at A=508.")

ROWS = [
    ("RowC", 1024, 4, B_STAR_ROWC, (250, 1)),
    ("RowC", 1024, 8, B_STAR_ROWC, (250, 1)),
    ("RowC", 1024, 16, B_STAR_ROWC, (250, 1)),
    ("prize", 1 << 41, 4, B_STAR_PRIZE, (2559, 10)),
    ("prize", 1 << 41, 8, B_STAR_PRIZE, (2559, 10)),
    ("prize", 1 << 41, 16, B_STAR_PRIZE, (2559, 10)),
]

table = []
for name, n, RD, bstar, (qnum, qden) in ROWS:
    k = n // RD
    print()
    print(f"== {name} n={n} rate 1/{RD} (k={k}), B* = {bstar} ==")
    dec = deciding_scale(RD, bstar, n)
    check(f"{name} 1/{RD}: deciding dyadic scale N'_dec = {dec} "
          f"matches #213 dyadic crossing", dec == P213_DYADIC[RD],
          f"C({dec},{dec//RD+1}) > B* >= C({dec//2},{dec//2//RD+1}), "
          f"log2 edge = {math.log2(edge_count(dec, RD)):.2f}")
    t_dec = n // dec
    A_last = k + t_dec           # last census-realizable unsafe point
    A = A_last + 1               # safe-side candidate
    check(f"{name} 1/{RD}: last unsafe realizable point A={A_last} "
          f"(l' = {dec - dec//RD - 1} integral, count > B*)",
          strict_count(n, k, A_last, dec) == edge_count(dec, RD)
          and strict_count(n, k, A_last, dec) > bstar)
    # candidate + A+1 budgets
    rows_out = []
    for a in (A, A + 1):
        j = n - a
        bq_s = bquot_strict(n, k, a)
        bq_u = bquot_ub(n, k, a)
        btan_hi = n - a + 1
        s_lo = bstar - bq_u - btan_hi
        s_hi = bstar - bq_s
        rows_out.append((a, j, bq_s, bq_u, btan_hi, s_lo, s_hi))
    (A0, j0, bqs0, bqu0, bt0, slo0, shi0), (A1, j1, bqs1, bqu1, bt1, slo1, shi1) = rows_out
    check(f"{name} 1/{RD}: candidate A={A0}: strict census B_quot = 0 "
          f"(j={j0} odd -> no active coset scale divides)", bqs0 == 0 and j0 % 2 == 1)
    check(f"{name} 1/{RD}: candidate total <= B* under BOTH B_quot variants "
          f"and worst-case B_tan", bqu0 + bt0 <= bstar and bqu1 + bt1 <= bstar,
          f"B_quot_ub={bqu0} (log2~{math.log2(bqu0):.2f}), B_tan<= {bt0}")
    check(f"{name} 1/{RD}: s >= 1 at A and A+1 under ALL variants "
          f"(B_tan in [0, n-A+1], B_quot in [strict, floor-rounded sum])",
          slo0 >= 1 and slo1 >= 1,
          f"s_lo(A)={slo0} log2~{math.log2(slo0):.4f}")
    # E14 reconciliation
    if name == "RowC":
        zm_ok = zm_negative_exact(n, k, A0, qnum, qden)
    else:
        zm_ok = zm_negative_entropy_ub(n, k, A0, qnum / qden)
    check(f"{name} 1/{RD}: E14 reconciliation: ZM(A) < 0 (aperiodic FM integer-zero "
          f"already holds at the candidate)", zm_ok)
    check(f"{name} 1/{RD}: candidate >= qa3 A_zero = A*+2 (E14 offset convention)",
          A0 >= QA3_ASTAR[(name, RD)] + 2,
          f"A={A0}, A*={QA3_ASTAR[(name, RD)]}")
    daq = QA3_AQUOT[(name, RD)] - A0
    flag(f"{name} 1/{RD}: candidate sits {daq} steps LEFT of qa3 Table-2 A_quot "
         f"(continuous-beta A_2 convention vs exact dyadic census; the dyadic "
         f"undershoot, cf. s7-F2). Verdict identical at both points.")
    print(f"  A = {A0}:  B* = {bstar}")
    print(f"            B_quot: strict = 0, floor-rounded-sum <= {bqu0}")
    print(f"            B_tan in [0, {bt0}]")
    print(f"            s in [{slo0}, {shi0}]")
    print(f"  A+1={A1}:  s in [{slo1}, {shi1}]")
    print(f"VERDICT {name} 1/{RD}: s >= 1 (indeed log2 s ~ "
          f"{math.log2(slo0):.2f}) -> face 4 = BOUNDED-MULTIPLICITY FORCING "
          f"at multiplicity s+1; the emptiness form is NOT budget-forced here.")
    table.append((name, RD, A0, bstar, bqu0, bt0, slo0, shi0))

print()
print("== summary table (row, rate, A, B*, B_quot_ub, B_tan_max, s_lo, s_hi) ==")
print("pinned 1/2  A=507  B*=6  B_quot=0  B_tan=6  s=0 ;  A=508 s=1   [EXACT]")
for name, RD, A0, bstar, bqu, bt, slo, shi in table:
    print(f"{name} 1/{RD}  A={A0}  B*={bstar}  B_quot_ub={bqu}  "
          f"B_tan_max={bt}  s_lo={slo}  s_hi={shi}")

certificate = {
    "dag_node": "xr_target_budget_audit",
    "status": "AUDIT: exact clean-rate integer allowance recomputed",
    "pinned_calibration": {
        "row": "pinned",
        "rate": "1/2",
        "n": 512,
        "k": 256,
        "A": 507,
        "B_star": B_STAR_PINNED,
        "B_quot": 0,
        "B_tan": 6,
        "s": s_507,
        "A_plus_1": 508,
        "s_A_plus_1": s_508,
    },
    "rows": [
        {
            "row": name,
            "rate": f"1/{RD}",
            "A": A0,
            "B_star": bstar,
            "B_quot_ub": bqu,
            "B_tan_max": bt,
            "s_lo": slo,
            "s_hi": shi,
        }
        for name, RD, A0, bstar, bqu, bt, slo, shi in table
    ],
}

if "--write-certificate" in sys.argv:
    CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(f"wrote {CERT_PATH}")
else:
    if CERT_PATH.exists():
        checked_in = json.loads(CERT_PATH.read_text())
        check("checked-in JSON certificate matches deterministic build", checked_in == certificate)
    else:
        check("checked-in JSON certificate exists", False, str(CERT_PATH))

print()
print(f"{len(PASS)} PASS, {len(FAIL)} FAIL")
sys.exit(0 if not FAIL else 1)
