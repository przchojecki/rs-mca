#!/usr/bin/env python3
"""verify_entropy_inverse_trade_reconciliation.py

Zero-arg, stdlib-only, deterministic verifier for the companion note
experimental/notes/thresholds/cap25_v13_entropy_inverse_trade_reconciliation.md.

The note is a reconciliation/scoping memo (base commit upstream/main 53bb5df, "Add
logarithmic moment route to grande finale"): it pins that rem:entropy-inverse-skeleton's
step-2 "signed trade satisfying the first w moment equations" (grande_finale.tex l.861-863)
is exactly a depth-w shift pair (prop:prefix-rigidity l.660 / prop:second-moment l.676 /
prop:newton l.551), proves that as a one-page lemma (lem:trade-is-shift-pair), and scopes
the Proximity-Prize DAG's PTE trade branch (star_pte_lemma / x81-x83 / h3/h4 / x24, all
PROVED; active_core_count_bound / h4_sparse_norm_gate, TARGET) as step-3-relevant prior
art in the low-support window. It makes NO claim on prob:entropy-inverse-q, leaves skeleton
steps 4-6 untouched, and moves no frontier edge.

This verifier checks only the note's OWN mechanical claims. Four gate classes; exit 0 iff
ALL pass (normal mode), nonzero on ANY failure. Under --tamper-selftest each gate corrupts
exactly one guarded expected value and must then report CAUGHT.

  gate i    CROSS-REFERENCE / STATUS AUDIT (reads repo files at the working tree, which is
            base 53bb5df plus this packet -- it does not touch grande_finale.tex,
            cap25_cap_v13_raw.tex, the prize DAG, or the L1 note).
            (a) LABELS AT PINNED LINES: every grande_finale.tex label the memo cites carries
                its \\label{...} at the exact pinned line.
            (b) ZERO CROSS-REFERENCE, BOTH DIRECTIONS: grande_finale.tex contains none of the
                PTE node ids / whole-word "PTE"; cap25_cap_v13_raw.tex contains no
                grande_finale/logmoment/entropy-inverse token; no roadmap note contains
                entropy-inverse/logmoment. Every pinned pair asserted == 0. (Whole-word
                "PTE" is used so the substring in "attempted" is not a false positive.)
            (c) DAG NODE STATUSES: parsed from prize_dag.json match the memo's table
                (7 PROVED nodes, 2 TARGET nodes).
            (d) STEP-3 NON-CONTACT: the L1 route-kill note carries the mu_11/F_23 signature
                and mentions "Tao" zero times (it kills a folk heuristic, not Tao05), while
                grande_finale.tex does cite Tao05 -- so the two never contact.
  gate ii   DICTIONARY LEMMA BY ENUMERATION (independent reimplementation; imports nothing).
            Row p=97, D=mu_16 subset F_97^x, m=6, w=2 (char 97 > w, so prop:newton applies).
            FORWARD: group all C(16,6)=8008 subsets by the coefficient prefix Phi_w; check the
            power-sum partition is identical (prop:newton at the toy); then for every
            off-diagonal ordered fiber pair form (R,S,T) and verify it is a depth-w shift pair
            -- |S|=|T|, e>=w+1, S,T disjoint, deg(ell_S-ell_T)<=e-w-1, the power sums agree on
            S,T, and the identity ell_M0-ell_M = ell_R(ell_S-ell_T) holds. All pinned counts
            (fibers, off-diagonal pairs, the e-distribution) diffed; 0 failures required.
            BACKWARD: for two fixed common parts R (|R|=3 -> e=3 top stratum; |R|=2 -> e=4)
            enumerate depth-w shift pairs (S,T) over D\\R and verify each closes to a fiber
            pair (Phi_w(R u S)=Phi_w(R u T)); counts pinned and cross-checked against the
            forward pairs with that exact common part (a bijection test).
  gate iii  CHAR B > w AT THE FOUR DEPLOYED ROWS (big-int). prop:newton's hypothesis, hence
            the "first w moment equations" = power-sum reading, is available at every deployed
            adjacent row: char B = p ~ 2^31 exceeds w in {67471, 67447} by ~10^4x. Constants
            are the same ones verify_gammar_order_floor.py pins (KB-MCA/KB-list w=67471 at
            P_KB; M31-MCA/M31-list w=67447 at P_M31).
  gate iv   (the --tamper-selftest mode itself; not a separate gate) -- see above.

PERFORMANCE (zero-arg): dominated by gate ii's forward enumeration of C(16,6)=8008 subsets
and the backward |R|=2 sweep (~2.1x10^5 disjoint 4-subset pairs). Measured total well under
60s (typically ~2s); see printed footer.

This verifier does NOT evaluate anything at deployed w, does NOT prove or refute
prob:entropy-inverse-q, does NOT touch skeleton steps 4-6, and asserts no asymptotic-Q
statement. It only checks this note's cross-references, its dictionary lemma at a toy row,
and one big-int inequality.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from itertools import combinations
from math import comb

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
EXP = os.path.join(REPO_ROOT, "experimental")
GF_PATH = os.path.join(EXP, "grande_finale.tex")
RAW_PATH = os.path.join(EXP, "cap25_cap_v13_raw.tex")
DAG_PATH = os.path.join(EXP, "data", "prize-dag", "prize_dag.json")
L1_PATH = os.path.join(EXP, "notes", "l1", "l1_coset_mixed_vacancy_threshold.md")
ROADMAP_DIR = os.path.join(EXP, "notes", "roadmaps")
NOTE_PATH = os.path.join(EXP, "notes", "thresholds",
                         "cap25_v13_entropy_inverse_trade_reconciliation.md")

WALL_ID = "CAP25-V13-ENTROPY-INVERSE-TRADE-RECONCILIATION"
BASE_COMMIT = "53bb5df"

# ---------------------------------------------------------------------------
# gate i pins (all verified by hand against base 53bb5df; see the note)
# ---------------------------------------------------------------------------
# grande_finale.tex: label -> the exact 1-based line carrying its \label{...}
GF_LABEL_LINES = {
    "prop:newton": 551,
    "prop:prefix-rigidity": 660,
    "prop:second-moment": 676,
    "prop:moment-sandwich": 705,
    "thm:moment-q": 721,
    "def:primitive-logmoment": 752,
    "thm:logmoment-equivalence": 769,
    "prob:entropy-inverse-q": 823,
    "rem:standard-inverse-gap": 837,
    "prop:vandermonde-kills-low-rank": 841,
    "cor:asymp-q-from-entropy-inverse": 853,
    "rem:entropy-inverse-skeleton": 861,
    "prop:sp-pullback": 1084,
    "thm:coeff-quotient-extract": 1130,
    "prop:top-stratum-quotient-sieve": 1163,
    "prop:gamma2-ledger": 1199,
    "thm:sp-proper": 1822,
}

# tokens that must be ABSENT (count == 0) from grande_finale.tex (whole-word PTE avoids the
# "attem-pte-d" substring; node-id tokens are literal and cannot false-positive).
GF_ABSENT_LITERAL = ["star_pte_lemma", "x81_minimal", "x82_square", "x83_uniform",
                     "h3_param_lemma", "h4_terminal_dichotomy", "prize_dag",
                     "active_core_count"]
GF_ABSENT_WORD = ["PTE"]  # matched with \bPTE\b

# tokens that must be ABSENT from cap25_cap_v13_raw.tex (the reverse direction)
RAW_ABSENT_LITERAL = ["grande_finale", "thm:logmoment", "logmoment",
                      "entropy-inverse", "entropy_inverse"]

# tokens that must be ABSENT from every roadmap note
ROADMAP_ABSENT_LITERAL = ["entropy-inverse", "entropy_inverse", "logmoment"]

# prize_dag.json node id -> expected status
DAG_STATUS = {
    "x24_char0_dyadic_descent": "PROVED",
    "star_pte_lemma": "PROVED",
    "x81_minimal_trade_square_shift": "PROVED",
    "x82_square_shift_certifier_keys": "PROVED",
    "x83_uniform_square_shift_obstruction_gate": "PROVED",
    "h3_param_lemma": "PROVED",
    "h4_terminal_dichotomy": "PROVED",
    "active_core_count_bound": "TARGET",
    "h4_sparse_norm_gate": "TARGET",
}

# ---------------------------------------------------------------------------
# gate ii pins (independently recomputed below; these are the certificate)
# ---------------------------------------------------------------------------
TOY_P, TOY_N, TOY_M, TOY_W = 97, 16, 6, 2
FWD_N_FIBERS = 4728
FWD_NONSINGLETON = 2224
FWD_TOT_SUBSETS = 8008          # == comb(16, 6)
FWD_SUM_NZ2 = 17384
FWD_OFFDIAG = 9376              # == FWD_SUM_NZ2 - FWD_TOT_SUBSETS
FWD_BY_E = {3: 3840, 4: 3472, 5: 2016, 6: 48}   # sums to FWD_OFFDIAG; e in [w+1, min(m,n-m)]
BWD_RA_COUNT = 6               # fixed R = D[0:3], |R|=3 -> e=3 (top stratum, constant shift)
BWD_RB_COUNT = 28              # fixed R = D[0:2], |R|=2 -> e=4

# ---------------------------------------------------------------------------
# gate iii pins (same constants as verify_gammar_order_floor.py)
# ---------------------------------------------------------------------------
P_KB = 2 ** 31 - 2 ** 24 + 1        # KoalaBear prime = 2130706433
P_M31 = 2 ** 31 - 1                 # Mersenne-31 prime = 2147483647
DEPLOYED_ROWS = [
    # (label, w, p)
    ("KB-MCA", 67471, P_KB),
    ("KB-list", 67471, P_KB),
    ("M31-MCA", 67447, P_M31),
    ("M31-list", 67447, P_M31),
]


# ---------------------------------------------------------------------------
# generic tamper helper (same discipline as verify_gammar_order_floor.py)
# ---------------------------------------------------------------------------
def _corrupt(x):
    if isinstance(x, bool):
        return not x
    if isinstance(x, int):
        return x + 1
    if isinstance(x, str):
        return x + "_TAMPERED_NONEXISTENT"
    if isinstance(x, dict):
        return {k: (v + 1 if isinstance(v, int) and not isinstance(v, bool) else v)
                for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return list(x[:-1]) if x else [999999]
    return x


def check(actual, expected, *, tamper=False):
    if tamper:
        expected = _corrupt(expected)
    return actual == expected


# ---------------------------------------------------------------------------
# small finite-field / polynomial machinery (independent reimplementation)
# ---------------------------------------------------------------------------
def primitive_root(p):
    phi = p - 1
    facs = []
    x = phi
    d = 2
    while d * d <= x:
        if x % d == 0:
            facs.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        facs.append(x)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in facs):
            return g
    raise RuntimeError("no primitive root")


def mult_subgroup(p, n):
    assert (p - 1) % n == 0, f"n={n} must divide p-1={p-1}"
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    D = []
    cur = 1
    for _ in range(n):
        D.append(cur)
        cur = (cur * h) % p
    assert len(set(D)) == n
    return sorted(D)


def poly_from_roots(roots, p):
    """monic prod (X - x); returns coeff list c with c[i] = coeff of X^i, c[-1]=1."""
    c = [1]
    for x in roots:
        nc = [0] * (len(c) + 1)
        for i, ci in enumerate(c):
            nc[i] = (nc[i] + ci * (-x)) % p
            nc[i + 1] = (nc[i + 1] + ci) % p
        c = nc
    return c


def poly_deg(coeffs, p):
    d = -1
    for i, ci in enumerate(coeffs):
        if ci % p != 0:
            d = i
    return d


def phi_w(rootvals, p, m, w):
    """the w coefficients immediately below the leading term of the monic degree-m locator."""
    c = poly_from_roots(rootvals, p)          # length m+1, c[m] = 1
    return tuple(c[m - 1 - j] % p for j in range(w))


def power_sums(rootvals, p, w):
    return tuple(sum(pow(x, i + 1, p) for x in rootvals) % p for i in range(w))


# ---------------------------------------------------------------------------
# gate i -- cross-reference / status audit
# ---------------------------------------------------------------------------
def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def gate_i_crossref(tamper=False):
    msgs = []
    ok = True

    # (a) labels at pinned lines
    gf_lines = _read(GF_PATH).splitlines()
    bad_lines = []
    first = True
    for label, ln in GF_LABEL_LINES.items():
        want_line = ln
        if tamper and first:                       # corrupt one expected line number
            want_line = _corrupt(ln)
            first = False
        present = 1 <= want_line <= len(gf_lines) and f"\\label{{{label}}}" in gf_lines[want_line - 1]
        if not present:
            bad_lines.append(f"{label}@{want_line}")
        ok = ok and present
    msgs.append(f"(a) {len(GF_LABEL_LINES)} labels at pinned lines: "
                f"{'all present' if not bad_lines else 'MISSING ' + ','.join(bad_lines)}")

    # (b) zero cross-reference, both directions
    gf_text = _read(GF_PATH)
    raw_text = _read(RAW_PATH)
    zero_ok = True
    for tok in GF_ABSENT_LITERAL:
        zero_ok = zero_ok and check(gf_text.count(tok), 0)
    for tok in GF_ABSENT_WORD:
        zero_ok = zero_ok and check(len(re.findall(r"\b" + re.escape(tok) + r"\b", gf_text)), 0)
    for tok in RAW_ABSENT_LITERAL:
        zero_ok = zero_ok and check(raw_text.count(tok), 0)
    roadmap_hits = 0
    for fn in os.listdir(ROADMAP_DIR):
        if not fn.endswith(".md"):
            continue
        t = _read(os.path.join(ROADMAP_DIR, fn))
        for tok in ROADMAP_ABSENT_LITERAL:
            roadmap_hits += t.count(tok)
    # tamper: corrupt the expected roadmap-hit count (expected 0)
    zero_ok = zero_ok and check(roadmap_hits, 0, tamper=tamper)
    ok = ok and zero_ok
    msgs.append(f"(b) zero-cross-reference both directions: GF<-PTE, RAW<-GF/logmoment, "
                f"roadmaps<-entropy/logmoment (roadmap_hits={roadmap_hits}): {zero_ok}")

    # (c) DAG node statuses
    dag = json.loads(_read(DAG_PATH))
    nodes = {n["id"]: n for n in dag["nodes"]}
    status_ok = check(dag.get("root"), "prize")
    first_s = True
    for nid, want in DAG_STATUS.items():
        got = nodes.get(nid, {}).get("status")
        status_ok = status_ok and check(got, want, tamper=(tamper and first_s))
        first_s = False
    ok = ok and status_ok
    n_proved = sum(1 for v in DAG_STATUS.values() if v == "PROVED")
    n_target = sum(1 for v in DAG_STATUS.values() if v == "TARGET")
    msgs.append(f"(c) DAG statuses (root=prize; {n_proved} PROVED, {n_target} TARGET): {status_ok}")

    # (d) step-3 non-contact
    l1_text = _read(L1_PATH)
    has_sig = ("mu_11" in l1_text) and ("F_23" in l1_text) and ("UNSOUND" in l1_text)
    tao_in_l1 = len(re.findall(r"Tao", l1_text))
    tao_in_gf = gf_text.count("Tao05")
    noncontact = has_sig and check(tao_in_l1, 0, tamper=tamper) and (tao_in_gf >= 1)
    ok = ok and noncontact
    msgs.append(f"(d) step-3 non-contact: L1 has mu_11/F_23 route-kill, Tao-in-L1={tao_in_l1}, "
                f"Tao05-in-GF={tao_in_gf}: {noncontact}")

    return ok, "; ".join(msgs)


# ---------------------------------------------------------------------------
# gate ii -- dictionary lemma by enumeration
# ---------------------------------------------------------------------------
def _toy_forward(D, p, m, w):
    """group all m-subsets by Phi_w; check every off-diagonal pair is a shift pair."""
    fibers = {}
    ps_blocks = {}
    for combo in combinations(range(len(D)), m):
        rv = [D[i] for i in combo]
        fibers.setdefault(phi_w(rv, p, m, w), []).append(combo)
        ps_blocks.setdefault(power_sums(rv, p, w), []).append(combo)
    # prop:newton at the toy: coeff-prefix partition == power-sum partition
    newton_ok = (sorted(tuple(sorted(v)) for v in fibers.values())
                 == sorted(tuple(sorted(v)) for v in ps_blocks.values()))

    n_fibers = len(fibers)
    nonsing = sum(1 for v in fibers.values() if len(v) >= 2)
    tot = sum(len(v) for v in fibers.values())
    sum_nz2 = sum(len(v) ** 2 for v in fibers.values())
    offdiag = sum_nz2 - tot

    Ra = frozenset(D[i] for i in range(3))    # |R|=3 -> e=3
    Rb = frozenset(D[i] for i in range(2))    # |R|=2 -> e=4
    by_e = {}
    fail = 0
    cnt_Ra = cnt_Rb = 0
    for members in fibers.values():
        if len(members) < 2:
            continue
        sets = [set(D[i] for i in c) for c in members]
        polys = [poly_from_roots(sorted(s), p) for s in sets]
        for a in range(len(members)):
            Ma, lMa = sets[a], polys[a]
            for b in range(len(members)):
                if a == b:
                    continue
                Mb, lMb = sets[b], polys[b]
                R = Ma & Mb
                S = Ma - Mb
                T = Mb - Ma
                e = len(S)
                A = poly_from_roots(sorted(S), p)
                B = poly_from_roots(sorted(T), p)
                AB = [(A[i] - B[i]) % p for i in range(len(A))]
                good = (len(S) == len(T) and e >= w + 1 and S.isdisjoint(T)
                        and poly_deg(AB, p) <= e - w - 1
                        and power_sums(sorted(S), p, w) == power_sums(sorted(T), p, w))
                # structural identity ell_M0 - ell_M == ell_R * (ell_S - ell_T)
                lR = poly_from_roots(sorted(R), p)
                prod = [0] * (len(lR) + len(AB) - 1)
                for i, ci in enumerate(lR):
                    for j, cj in enumerate(AB):
                        prod[i + j] = (prod[i + j] + ci * cj) % p
                lhs = [(lMa[i] - lMb[i]) % p for i in range(len(lMa))]
                L = max(len(lhs), len(prod))
                lhs += [0] * (L - len(lhs))
                prod += [0] * (L - len(prod))
                good = good and (lhs == prod)
                if not good:
                    fail += 1
                by_e[e] = by_e.get(e, 0) + 1
                if frozenset(R) == Ra:
                    cnt_Ra += 1
                if frozenset(R) == Rb:
                    cnt_Rb += 1
    return dict(n_fibers=n_fibers, nonsing=nonsing, tot=tot, sum_nz2=sum_nz2,
                offdiag=offdiag, by_e=by_e, fail=fail, newton_ok=newton_ok,
                cnt_Ra=cnt_Ra, cnt_Rb=cnt_Rb)


def _toy_backward(Rset, e, D, p, m, w):
    """enumerate depth-w shift pairs over D\\R; verify each closes to a fiber pair."""
    Rvals = set(Rset)
    Drest = [x for x in D if x not in Rvals]
    cnt = 0
    closed = 0
    for S in combinations(Drest, e):
        Sset = set(S)
        rest = [x for x in Drest if x not in Sset]
        A = poly_from_roots(list(S), p)
        for T in combinations(rest, e):
            B = poly_from_roots(list(T), p)
            AB = [(A[i] - B[i]) % p for i in range(len(A))]
            if poly_deg(AB, p) <= e - w - 1:
                cnt += 1
                if phi_w(list(Rset) + list(S), p, m, w) == phi_w(list(Rset) + list(T), p, m, w):
                    closed += 1
    return cnt, closed


def gate_ii_dictionary(tamper=False):
    D = mult_subgroup(TOY_P, TOY_N)
    fwd = _toy_forward(D, TOY_P, TOY_M, TOY_W)

    ok = True
    ok = ok and check(fwd["n_fibers"], FWD_N_FIBERS)
    ok = ok and check(fwd["nonsing"], FWD_NONSINGLETON)
    ok = ok and check(fwd["tot"], FWD_TOT_SUBSETS) and check(FWD_TOT_SUBSETS, comb(TOY_N, TOY_M))
    ok = ok and check(fwd["sum_nz2"], FWD_SUM_NZ2)
    ok = ok and check(fwd["offdiag"], FWD_OFFDIAG)
    ok = ok and check(fwd["by_e"], FWD_BY_E, tamper=tamper)   # guarded datum for tamper
    ok = ok and check(fwd["fail"], 0)                         # every fiber pair IS a shift pair
    ok = ok and fwd["newton_ok"]                              # prop:newton at the toy
    ok = ok and check(sum(FWD_BY_E.values()), FWD_OFFDIAG)

    Ra = [D[i] for i in range(3)]
    Rb = [D[i] for i in range(2)]
    cnt_a, closed_a = _toy_backward(Ra, 3, D, TOY_P, TOY_M, TOY_W)
    cnt_b, closed_b = _toy_backward(Rb, 4, D, TOY_P, TOY_M, TOY_W)
    # every enumerated shift pair closes to a fiber pair
    ok = ok and check(closed_a, cnt_a) and check(closed_b, cnt_b)
    # counts match the pins and the forward pairs with that exact common part (bijection)
    ok = ok and check(cnt_a, BWD_RA_COUNT) and check(cnt_a, fwd["cnt_Ra"])
    ok = ok and check(cnt_b, BWD_RB_COUNT) and check(cnt_b, fwd["cnt_Rb"])

    msg = (f"row p=97 D=mu_16 m=6 w=2: FWD fibers={fwd['n_fibers']} "
           f"offdiag={fwd['offdiag']} by_e={dict(sorted(fwd['by_e'].items()))} "
           f"failures={fwd['fail']} newton_partition_equal={fwd['newton_ok']}; "
           f"BWD R|3|->e3: pairs={cnt_a} closed={closed_a} (fwd {fwd['cnt_Ra']}); "
           f"R|2|->e4: pairs={cnt_b} closed={closed_b} (fwd {fwd['cnt_Rb']})")
    return ok, msg


# ---------------------------------------------------------------------------
# gate iii -- char B > w at the four deployed rows (big-int)
# ---------------------------------------------------------------------------
def gate_iii_char_gt_w(tamper=False):
    ok = True
    parts = []
    first = True
    for label, w, p in DEPLOYED_ROWS:
        w_chk = w
        if tamper and first:                 # corrupt one expected w so char>w flips risk
            w_chk = _corrupt(p)               # force w_chk > p to break the inequality
            first = False
        gt = p > w_chk
        ok = ok and gt
        parts.append(f"{label}: p={p} > w={w_chk}: {gt}")
    msg = "char B > w (prop:newton hypothesis) -- " + "; ".join(parts)
    return ok, msg


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
GATE_SPECS = [
    ("gate i   cross-reference / status audit     ", gate_i_crossref),
    ("gate ii  dictionary lemma by enumeration    ", gate_ii_dictionary),
    ("gate iii char B > w at four deployed rows   ", gate_iii_char_gt_w),
]


def main() -> int:
    t0 = time.time()
    argv = sys.argv[1:]
    selftest = "--tamper-selftest" in argv

    print("=" * 92)
    if selftest:
        print(f" TAMPER SELF-TEST [{WALL_ID}]: each gate must FAIL when its guarded datum is corrupted")
    else:
        print(f" verify_entropy_inverse_trade_reconciliation  (zero-arg)   base {BASE_COMMIT}")
        print(" AUDIT + one PROVED toy lemma; no claim on prob:entropy-inverse-q, steps 4-6, or the frontier")
    print("=" * 92)

    for req in (NOTE_PATH, GF_PATH, RAW_PATH, DAG_PATH, L1_PATH):
        if not os.path.isfile(req):
            print(f"FATAL: required file missing: {req}")
            return 1

    all_good = True
    for label, fn in GATE_SPECS:
        try:
            ok, summary = fn(selftest)
        except Exception as exc:  # noqa: BLE001
            print(f"  {label}  ERROR   {exc}")
            return 1
        caught_or_pass = (not ok) if selftest else ok
        all_good = all_good and caught_or_pass
        tag = ("CAUGHT " if caught_or_pass else "MISSED!") if selftest else ("PASS" if ok else "FAIL")
        print(f"  {label}  {tag}   ({time.time() - t0:.1f}s elapsed)")
        print(f"        {summary}")

    print("=" * 92)
    dt = time.time() - t0
    if selftest:
        print(f" SELF-TEST RESULT: {'all tampers CAUGHT' if all_good else 'A TAMPER WAS MISSED'}   ({dt:.1f}s)")
    else:
        print(f" RESULT: {'ALL GATES PASS' if all_good else 'FAILURE'}   ({dt:.1f}s)")
        print(" This verifier checks only the note's own cross-references, its toy dictionary")
        print(" lemma, and char B > w; it makes no claim on prob:entropy-inverse-q.")
    return 0 if all_good else 1


if __name__ == "__main__":
    sys.exit(main())
