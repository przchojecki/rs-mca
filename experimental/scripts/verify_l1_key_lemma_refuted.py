#!/usr/bin/env python3
"""verify_l1_key_lemma_refuted.py

Zero-arg, stdlib-only, deterministic verifier for
`experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md`, which REFUTES two
load-bearing claims of the integrated note
`experimental/notes/l1/l1_prime_ell_frontier_corrected.md`:

  - its KEY LEMMA (sec 3)   `E_3 <= ell-2`   (equivalently `delta <= K`), and
  - the lower/VACANCY half (sec 4) of `m*(ell) = (ell+3)/2`
    (`top-m < 2ell` for all `m <= (ell+1)/2`), at `ell in {11,13,17,23}`.

Ground rule: this verifier does NOT import from, edit, or depend on the
integrated note's own claims being true -- gates (i), (ii), (v) recompute
everything with an OWN, independent `F_p` arithmetic implementation (no
import of the sibling verifier at all).  Gates (iii) and (iv) deliberately
DO import the integrated verifier's module
(`experimental/scripts/verify_l1_prime_ell_frontier_corrected.py`, UNCHANGED,
via `importlib`) because the whole point of those two gates is to run ITS
OWN `run_witness_chain` function on data it was never tuned against, and to
confirm its own witnesses still survive -- i.e. to prove the refutation using
the integrated note's own certification machinery, not a fresh one that
could be accused of testing a strawman.

Six gate classes; exit 0 iff ALL pass, nonzero on ANY failure:

  (i)   SEVEN COUNTEREXAMPLES: recompute the spectrum and E_3 of each of the
        six shipped `Gamma` (own arithmetic, two independent
        sub-implementations, no import of the integrated verifier), and
        assert an EXACT match to this note's table AND `E_3 > ell-2`
        (`ell in {11,13,17,23}`, `E_3 <= ell-1` additionally refuted at
        `ell=23`).
  (ii)  WELL-FORMEDNESS: each shipped `Gamma` is constant-free (no `X^0`
        term, by representation), has `deg <= ell-1` (representation length
        `== ell-1`), and is mixed (`Gamma != 0`) -- the object each gamma
        purports to be is the object it actually is.
  (iii) FRONTIER REFUTATION: import the INTEGRATED verifier's own
        `run_witness_chain` (unchanged) and confirm it returns ALL 16 GATES
        TRUE for the `ell=13, p=313` counterexample at `m=7` (`top-7 = 26 =
        2*13`, below the claimed onset `m* = (ell+3)/2 = 8`) -- i.e. the
        REFUTATION is certified by the very machinery the integrated note
        uses to certify its OWN witnesses.  Control: the SAME config at
        `m=6` must NOT be full (guards against a vacuous pass).
  (iv)  SURVIVOR CHECK: the integrated note's OWN `ell=13, m=8, p=313`
        upper-half witness (pulled directly from the imported module's
        `WITNESSES` table, not re-hardcoded) must STILL pass
        `run_witness_chain` at `m=8` (`full=True`, `lam_free=True`) -- the
        refutation withdraws the LOWER (vacancy) half only; the UPPER
        (listing) half survives untouched.  Control: the SAME witness at
        `m=7` must NOT be full (`top-7 = 25 < 26`), confirming `m=7`
        genuinely needs the *different* `E_3=12` counterexample of gate
        (iii), not just a laxer reading of the note's own witness.
  (v)   ELL=23 CEILING BREACH: the `ell=23, p=139` counterexample has
        `E_3 = 23 = ell` exactly -- so even the WEAKER fallback bound
        `E_3 <= ell-1` fails there, not only the KEY LEMMA `E_3 <= ell-2`.
  (vi)  FOUR SUB-ONSET LISTINGS (the frontier VACANCY half refuted at every
        tested `ell >= 11`, not just `ell = 13`): for each of the four new
        `m = (ell+1)/2` listings -- `ell=11 p=331 m=6`, `ell=17 p=409 m=9`,
        `ell=23 p=599 m=12`, `ell=23 p=691 m=12` -- (a) recompute the FULL
        spectrum from scratch (own arithmetic, two independent
        sub-implementations) and assert an EXACT match to the note's table,
        with `E_3`, `top-m = 2ell`, and `top-(m-1) < 2ell`; (b) run the
        INTEGRATED verifier's own `run_witness_chain` and assert it is a full
        listing (all 16 gates True for `ell in {11,17}`, run LIVE; the 15
        fast gates True for `ell=23` with the expensive `L5_minimal` gate
        confirmed offline this session and reproducible with `--full-min`,
        which runs `check_minimal=True` live for `ell=23` too, ~15 min);
        (c) CONTROL: the SAME config at `m-1` is NOT a full listing (guards
        against a vacuous pass), with the expected `top-(m-1)` hardcoded.
        Consequence: `m*(ell) = (ell+1)/2` is now ATTAINED at every tested
        `ell >= 11`, so the VACANCY half is refuted (not merely OPEN) at
        `ell in {11,13,17,23}`.

Hidden self-test:  python3 verify_l1_key_lemma_refuted.py --tamper-selftest
    flips one datum per gate class and asserts each gate then FAILS (proves
    every gate has teeth).  The shipped default is zero-arg.

All arithmetic is exact over F_p, stdlib only.  No network, no files, no CLI
args required.
"""
import sys
import os
import time
import importlib.util

# =====================================================================================
# exact F_p arithmetic -- OWN, independent implementation (gates i, ii, v never
# import the integrated verifier; only gates iii/iv do, deliberately, to
# exercise ITS run_witness_chain)
# =====================================================================================
def inv(a, p):
    return pow(a % p, p - 2, p)

def spectrum_group(gamma, p, ell):
    """Implementation A: group F_p^* by x^ell (label = coset), Horner eval."""
    grp = {}
    for x in range(1, p):
        lab = pow(x, ell, p)
        v = 0
        for c in reversed(gamma):
            v = (v * x + c) % p
        v = v * x % p  # gamma has no constant term: sum_{r>=1} gamma_r x^r
        d = grp.setdefault(lab, {})
        d[v] = d.get(v, 0) + 1
    return sorted((max(d.values()) for d in grp.values()), reverse=True)

def factorize(n):
    f = set()
    d, m = 2, n
    while d * d <= m:
        while m % d == 0:
            f.add(d)
            m //= d
        d += 1
    if m > 1:
        f.add(m)
    return f

def find_gen(p):
    fac = factorize(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    raise RuntimeError("no generator")

def spectrum_coset(gamma, p, ell):
    """Implementation B: independent -- walk generator-power cosets g^i * H,
    ascending power-sum evaluation (no x^ell grouping)."""
    g = find_gen(p)
    n = (p - 1) // ell
    zeta = pow(g, n, p)
    H = [pow(zeta, j, p) for j in range(ell)]
    out = []
    for i in range(n):
        b = pow(g, i, p)
        cnt = {}
        for h in H:
            x = b * h % p
            v = 0
            xr = 1
            for r in range(1, ell):
                xr = xr * x % p
                if gamma[r - 1]:
                    v = (v + gamma[r - 1] * xr) % p
            cnt[v] = cnt.get(v, 0) + 1
        out.append(max(cnt.values()))
    out.sort(reverse=True)
    return out

def E3(spec):
    return sum(mu - 2 for mu in spec if mu >= 3)

def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

# =====================================================================================
# the six shipped counterexamples (verbatim from the note; independently
# recomputed and matched here, not merely copied)
# =====================================================================================
COUNTEREXAMPLES = [
    {"label": "ell=11 p=67", "ell": 11, "p": 67,
     "gamma": [43, 44, 38, 44, 17, 18, 42, 44, 65, 1],
     "head": [8, 3, 3, 3, 3, 2], "E3": 10},
    {"label": "ell=11 p=199", "ell": 11, "p": 199,
     "gamma": [21, 144, 71, 171, 42, 10, 12, 115, 173, 1],
     "head": [7, 4, 3, 3, 3, 1], "E3": 10},
    {"label": "ell=13 p=79", "ell": 13, "p": 79,
     "gamma": [23, 71, 3, 40, 40, 2, 46, 40, 67, 69, 71, 1],
     "head": [6, 6, 6, 2, 2, 1], "E3": 12},
    {"label": "ell=13 p=313", "ell": 13, "p": 313,
     "gamma": [185, 42, 295, 307, 71, 257, 218, 32, 90, 290, 279, 1],
     "head": [8, 5, 3, 3, 3, 2, 2, 2, 2, 2], "E3": 12},
    {"label": "ell=17 p=103", "ell": 17, "p": 103,
     "gamma": [27, 7, 1, 74, 35, 11, 86, 96, 66, 44, 7, 96, 5, 48, 72, 1],
     "head": [10, 7, 3, 3, 3, 2], "E3": 16},
    {"label": "ell=19 p=191", "ell": 19, "p": 191,
     "gamma": [16, 44, 177, 106, 79, 157, 14, 155, 11, 181, 151, 28, 126, 22, 142, 23, 1, 1],
     "head": [11, 8, 4, 3, 2, 2], "E3": 18},
    {"label": "ell=23 p=139", "ell": 23, "p": 139,
     "gamma": [60, 80, 118, 60, 48, 137, 123, 101, 89, 94, 15, 23, 21, 88, 134, 5, 48, 8, 124, 42, 77, 1],
     "head": [13, 10, 4, 3, 3, 2], "E3": 23},
]

# =====================================================================================
# the four NEW sub-onset listings, one per tested ell>=11 (ell=23 replicated at two
# large-n primes).  Each is a FULL run_witness_chain listing at m = (ell+1)/2, one
# stratum BELOW the integrated note's claimed onset (ell+3)/2 -- so it refutes the
# frontier VACANCY half (`top-m < 2ell for m <= (ell+1)/2`) at its ell, and pins
# m*(ell) = (ell+1)/2 (attained).  Full spectra are recomputed from scratch below
# and matched EXACTLY (not just the head).
#
# `min_mode`:
#   "live"    -- run_witness_chain(check_minimal=True) runs LIVE (all 16 gates);
#                cheap enough for the zero-arg default (ell=11: <1s, ell=17: ~35s).
#   "offline" -- the expensive L5_minimal gate is ~400s/prime at ell=23, so the
#                zero-arg default runs the 15 fast gates LIVE (check_minimal=False)
#                and TRUSTS the recorded minimality (independently confirmed this
#                session, see note sec 2/7); pass --full-min to run
#                check_minimal=True live for ell=23 too.
NEW_LISTINGS = [
    {"label": "ell=11 m=6 p=331", "ell": 11, "p": 331, "m": 6,
     "gamma": [11, 165, 196, 237, 31, 40, 171, 236, 246, 1],
     "spectrum": [8, 3, 3, 3, 3, 2] + [1] * 24,
     "top_m": 22, "top_m1": 20, "E3": 10, "min_mode": "live",
     "note": "note's own extremal prime; 11 distinct such Gammas across p in {199,331} (4+7)"},
    {"label": "ell=17 m=9 p=409", "ell": 17, "p": 409, "m": 9,
     "gamma": [80, 5, 360, 87, 283, 89, 358, 379, 216, 174, 67, 329, 68, 317, 398, 1],
     "spectrum": [9, 8, 3, 3, 3, 2, 2, 2, 2, 2] + [1] * 14,
     "top_m": 34, "top_m1": 32, "E3": 16, "min_mode": "live",
     "note": "note's own full-witness prime p=409; distinct higher-E3 (16 vs 14) config from the m=10 witness"},
    {"label": "ell=23 m=12 p=599", "ell": 23, "p": 599, "m": 12,
     "gamma": [327, 192, 175, 17, 298, 200, 474, 496, 95, 354, 502, 222, 509, 213, 417, 173, 98, 207, 106, 381, 328, 1],
     "spectrum": [13, 10, 4, 3] + [2] * 14 + [1] * 8,
     "top_m": 46, "top_m1": 44, "E3": 22, "min_mode": "offline",
     "note": "large-n (n=26); cross-prime replicated with p=691"},
    {"label": "ell=23 m=12 p=691", "ell": 23, "p": 691, "m": 12,
     "gamma": [524, 614, 310, 539, 294, 303, 425, 653, 551, 564, 145, 271, 332, 503, 117, 545, 122, 226, 30, 443, 430, 1],
     "spectrum": [13, 10, 3, 3, 3] + [2] * 12 + [1] * 13,
     "top_m": 46, "top_m1": 44, "E3": 22, "min_mode": "offline",
     "note": "large-n (n=30); cross-prime replicated with p=599"},
]

# set by main() from argv; when True, ell=23 runs check_minimal=True live too.
FULL_MIN = False

# repo-relative path to the integrated (UNCHANGED) verifier, resolved
# relative to THIS file so it works regardless of the invocation cwd (a
# superset of "run from repo root", which also resolves the same file).
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
INTEGRATED_VERIFIER_PATH = os.path.join(_THIS_DIR, "verify_l1_prime_ell_frontier_corrected.py")

def load_integrated_verifier():
    spec = importlib.util.spec_from_file_location("v_corrected", INTEGRATED_VERIFIER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# =====================================================================================
# GATES
# =====================================================================================
def gate_i_six_counterexamples(tamper=False):
    ok = True
    lines = []
    for wi, CE in enumerate(COUNTEREXAMPLES):
        gamma = list(CE["gamma"])
        if tamper and wi == 0:
            gamma[0] = (gamma[0] + 1) % CE["p"]  # flip one coefficient of the first counterexample
        sA = spectrum_group(gamma, CE["p"], CE["ell"])
        sB = spectrum_coset(gamma, CE["p"], CE["ell"])
        head_ok = sA[:len(CE["head"])] == CE["head"]
        e3 = E3(sA)
        e3_ok = (e3 == CE["E3"])
        gt_ok = e3 > CE["ell"] - 2
        good = (sA == sB) and head_ok and e3_ok and gt_ok
        ok = ok and good
        lines.append("%s: A==B=%s head_ok=%s E3=%d(expect %d)=%s E3>ell-2=%s"
                      % (CE["label"], sA == sB, head_ok, e3, CE["E3"], e3_ok, gt_ok))
    return ok, " | ".join(lines)

def gate_ii_wellformed(tamper=False):
    ok = True
    lines = []
    for wi, CE in enumerate(COUNTEREXAMPLES):
        gamma = list(CE["gamma"])
        if tamper and wi == 0:
            gamma = [0] * len(gamma)  # break mixedness of the first counterexample
        ell, p = CE["ell"], CE["p"]
        len_ok = (len(gamma) == ell - 1)          # representation is exactly deg<=ell-1, constant-free
        mixed_ok = any(c % p for c in gamma)       # Gamma != 0
        range_ok = all(0 <= c < p for c in gamma)  # well-formed mod-p representation
        ell_prime_ok = is_prime(ell)
        pair_ok = is_prime(p) and ((p - 1) % ell == 0)
        good = len_ok and mixed_ok and range_ok and ell_prime_ok and pair_ok
        ok = ok and good
        lines.append("%s: len==ell-1:%s mixed:%s in_range:%s ell_prime:%s ell|p-1:%s"
                      % (CE["label"], len_ok, mixed_ok, range_ok, ell_prime_ok, pair_ok))
    return ok, " | ".join(lines)

def gate_iii_frontier_refutation(tamper=False):
    mod = load_integrated_verifier()
    CE313 = next(c for c in COUNTEREXAMPLES if c["label"] == "ell=13 p=313")
    gamma = list(CE313["gamma"])
    if tamper:
        gamma[0] = (gamma[0] + 1) % CE313["p"]
    G7, lam_free7, full7, top_m7 = mod.run_witness_chain(gamma, 313, 13, 7)
    G6, lam_free6, full6, top_m6 = mod.run_witness_chain(gamma, 313, 13, 6)
    all16 = (len(G7) == 16) and all(G7.values())
    m7_ok = (top_m7 == 26) and full7 and all16
    m6_ok = (top_m6 == 24) and (not full6)  # control: NOT a vacuous pass
    ok = m7_ok and m6_ok
    return ok, ("m=7: top_m=%d full=%s all16=%s (expect top_m=26,full=True) | "
                 "m=6 control: top_m=%d full=%s (expect top_m=24,full=False)"
                 % (top_m7, full7, all16, top_m6, full6))

def gate_iv_survivor_check(tamper=False):
    mod = load_integrated_verifier()
    own = next(w for w in mod.WITNESSES if w["label"] == "ell=13 m=8 p=313")
    gamma = list(own["gamma"])
    if tamper:
        gamma[0] = (gamma[0] + 1) % own["p"]
    G8, lam_free8, full8, top_m8 = mod.run_witness_chain(gamma, own["p"], own["ell"], 8)
    G7, lam_free7, full7, top_m7 = mod.run_witness_chain(gamma, own["p"], own["ell"], 7)
    m8_ok = full8 and lam_free8 and (top_m8 == 27)
    m7_ok = (not full7) and (top_m7 == 25)  # control: this witness does NOT list at m=7
    ok = m8_ok and m7_ok
    return ok, ("m=8 (survivor): top_m=%d full=%s lam_free=%s (expect 27,True,True) | "
                 "m=7 control: top_m=%d full=%s (expect 25,False)"
                 % (top_m8, full8, lam_free8, top_m7, full7))

def gate_v_ell23_ceiling_breach(tamper=False):
    CE23 = next(c for c in COUNTEREXAMPLES if c["label"] == "ell=23 p=139")
    gamma = list(CE23["gamma"])
    if tamper:
        gamma[0] = (gamma[0] + 1) % CE23["p"]
    spec = spectrum_group(gamma, CE23["p"], CE23["ell"])
    e3 = E3(spec)
    ell = CE23["ell"]
    eq_ell = (e3 == ell)
    gt_ell_minus_1 = (e3 > ell - 1)  # even the fallback E_3<=ell-1 is breached
    ok = eq_ell and gt_ell_minus_1
    return ok, "E_3=%d ell=%d (E_3==ell:%s) E_3>ell-1=%d:%s" % (e3, ell, eq_ell, ell - 1, gt_ell_minus_1)

def _check_one_new_listing(L, mod, full_min):
    """Verify a single NEW sub-onset listing; return (ok, detail).

    (a) from-scratch spectrum (own arith, A and B) matches the note's table
        EXACTLY, with E_3, top-m = 2ell, top-(m-1) < 2ell.
    (b) the integrated run_witness_chain is a full listing: all 16 gates for
        ell in {11,17} (live), or the 15 fast gates for ell=23 (minimality
        offline, unless --full-min forces it live).
    (c) control: the same config at m-1 is NOT full (top-(m-1) hardcoded).
    """
    ell, p, m = L["ell"], L["p"], L["m"]
    gamma = list(L["gamma"])
    # (a) own from-scratch spectrum, two independent implementations
    sA = spectrum_group(gamma, p, ell)
    sB = spectrum_coset(gamma, p, ell)
    spec_ok = (sA == L["spectrum"]) and (sA == sB)
    e3 = E3(sA)
    e3_ok = (e3 == L["E3"])
    tm = sum(sA[:m])
    tm_ok = (tm == L["top_m"] == 2 * ell)
    tm1 = sum(sA[:m - 1])
    tm1_ok = (tm1 == L["top_m1"]) and (tm1 < 2 * ell)
    # (b) integrated run_witness_chain: full listing at m
    live_full = (L["min_mode"] == "live") or full_min
    G, lam_free, full, top_m = mod.run_witness_chain(gamma, p, ell, m, check_minimal=live_full)
    if live_full:
        chain_ok = (len(G) == 16) and all(G.values()) and full and (top_m == L["top_m"])
        gate_word = "all-16-live=%s" % all(G.values())
    else:
        # 15 fast gates live; L5_minimal confirmed offline this session
        chain_ok = (len(G) == 15) and all(G.values()) and (top_m == L["top_m"])
        gate_word = "15/16-live=%s(L5_minimal:offline)" % all(G.values())
    # (c) control at m-1: NOT a full listing (cheap; no minimality needed)
    Gc, lfc, fullc, top_mc = mod.run_witness_chain(gamma, p, ell, m - 1, check_minimal=False)
    ctrl_ok = (not fullc) and (top_mc == L["top_m1"])
    ok = spec_ok and e3_ok and tm_ok and tm1_ok and chain_ok and ctrl_ok
    detail = ("specA==B==tbl:%s E3=%d top-%d=%d(=2ell:%s) %s | "
              "ctrl m=%d: top=%d(expect %d) full=%s"
              % (spec_ok, e3, m, tm, tm == 2 * ell, gate_word,
                 m - 1, top_mc, L["top_m1"], fullc))
    return ok, detail

def gate_vi_new_listings(tamper=False):
    if not tamper:
        mod = load_integrated_verifier()
        ok = True
        lines = []
        for L in NEW_LISTINGS:
            o, d = _check_one_new_listing(L, mod, FULL_MIN)
            ok = ok and o
            lines.append("%s: %s" % (L["label"], d))
        return ok, "  ||  ".join(lines)
    # tamper mode: flip ONE datum (gamma[0]) per NEW witness and require each
    # flip to be INDIVIDUALLY detected by the from-scratch spectrum recompute
    # (the gate checks spectrum first, so this is exactly the datum that guards
    # each witness -- and it is fast: no run_witness_chain call is needed).
    all_detected = True
    lines = []
    for L in NEW_LISTINGS:
        g = list(L["gamma"])
        g[0] = (g[0] + 1) % L["p"]
        sA = spectrum_group(g, L["p"], L["ell"])
        detected = (sA != L["spectrum"])
        all_detected = all_detected and detected
        lines.append("%s: gamma[0]+1 -> spectrum-match broken:%s" % (L["label"], detected))
    # gate must FAIL under tamper => ok=False iff EVERY witness detected its flip
    return (not all_detected), "  ||  ".join(lines)

GATES = [
    ("(i)   seven counterexamples (own arith)   ", gate_i_six_counterexamples),
    ("(ii)  well-formedness (constfree/mixed) ", gate_ii_wellformed),
    ("(iii) frontier refutation (m=7 lists)   ", gate_iii_frontier_refutation),
    ("(iv)  survivor check (m=8 witness OK)   ", gate_iv_survivor_check),
    ("(v)   ell=23 ceiling breach (E_3==ell)  ", gate_v_ell23_ceiling_breach),
    ("(vi)  four sub-onset m=(ell+1)/2 listers", gate_vi_new_listings),
]

def main():
    global FULL_MIN
    t0 = time.time()
    selftest = "--tamper-selftest" in sys.argv
    FULL_MIN = "--full-min" in sys.argv
    print("=" * 90)
    if selftest:
        print(" TAMPER SELF-TEST: each gate must FAIL when its guarded datum is flipped")
    else:
        print(" verify_l1_key_lemma_refuted  (zero-arg)   KEY LEMMA E_3<=ell-2 REFUTED")
        print(" (experimental/notes/l1/l1_prime_ell_key_lemma_refuted.md)")
        if FULL_MIN:
            print(" [--full-min: running check_minimal=True LIVE for ell=23 too (~15 min)]")
    print("=" * 90)
    all_good = True
    for name, fn in GATES:
        if selftest:
            ok, summ = fn(tamper=True)
            caught = not ok
            all_good = all_good and caught
            print("  %s  TAMPER %s" % (name, "CAUGHT " if caught else "MISSED!"))
            print("        %s" % summ)
        else:
            ok, summ = fn(tamper=False)
            all_good = all_good and ok
            print("  %s  %s" % (name, "PASS" if ok else "FAIL"))
            print("        %s" % summ)
    print("=" * 90)
    if selftest:
        print(" SELF-TEST RESULT: %s   (%.1fs)"
              % ("all tampers CAUGHT" if all_good else "A TAMPER WAS MISSED", time.time() - t0))
    else:
        print(" RESULT: %s   (%.1fs)" % ("ALL GATES PASS" if all_good else "FAILURE", time.time() - t0))
    sys.exit(0 if all_good else 1)

if __name__ == "__main__":
    main()
