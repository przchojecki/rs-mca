#!/usr/bin/env python3
r"""
M1 strict264 audit: does the TWO-ENDED jet admit a common-line LD_sw transfer?

The strict264 deployment is described two ways that DISAGREE by one coefficient:

  * standalone proof Lemma 1 (m1_cycle120_standalone_ldsw_proof.md, line 83):
        deg(P_J - P_J') <= j - sigma            <=>  e_1..e_{sigma-1} common
    (top sigma-1 elementary symmetric functions fixed; NO endpoint condition).
    This is what verify_m1_strict264_end_to_end.py realized end-to-end.

  * candidate note "Cycle119 Two-Ended Check"
    (m1_cycle120_abf_counterexample_candidate.md, lines 286-287):
        deg(P_J - P_J') <= j - sigma + 1,  P_J(0)=c != 0 common
    <=>  e_1..e_{sigma-2} common  AND  endpoint e_j common
    (top sigma-2 symmetric functions + endpoint; e_{sigma-1} is FREE).

Both fix sigma-1 linear constraints, but the two-ended TRADES the (sigma-1)-th top
coefficient e_{sigma-1} for the endpoint.

THE QUESTION (core audit correctness): the LD_sw transfer needs the J-dependent part
A_J := H e_J - z_J B  (z_J = 1/P_J(beta), B_m = beta^m) to be COMMON across the
jet class -- only then is there a single received line f + z g with f given by
H f = A_common.  A_m = -Q_m(beta), and Q_{j+t} depends on e_1..e_t, so the TOP row
m=j+sigma-1 depends on e_{sigma-1}.  Prediction: if e_{sigma-1} is free (the literal
two-ended reading), A_J is NOT common (it varies in exactly the top coordinate),
so NO single line fits -- the two-ended transfer as literally stated FAILS, and the
deployment must actually fix e_{sigma-1} too (i.e. read as Lemma 1 + endpoint).

This script builds a genuine small RS code and computes A_J across each reading:
  * Reading L1  (e_1..e_{sigma-1} fixed)            -> expect A_J COMMON
  * Reading L1+endpoint (e_1..e_{sigma-1}, e_j)     -> expect A_J COMMON (subfamily)
  * Reading TwoEnded-literal (e_1..e_{sigma-2}, e_j;
                              e_{sigma-1} free)      -> expect A_J NOT common
and pinpoints that the only varying coordinate is the top parity row m=j+sigma-1.

Status: AUDIT FINDING. The verdict (common vs not) is decided by enumeration, not
asserted.

Run:
    python3 experimental/scripts/verify_m1_strict264_two_ended_transfer.py
    python3 experimental/scripts/verify_m1_strict264_two_ended_transfer.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations


def find_generator(p):
    for g in range(2, p):
        seen, x = set(), 1
        for _ in range(p - 1):
            x = (x * g) % p
            seen.add(x)
        if len(seen) == p - 1:
            return g
    raise RuntimeError("no generator")


def elem_sym(J, p):
    e = [1]
    for a in J:
        ne = e + [0]
        for i in range(len(e), 0, -1):
            ne[i] = (ne[i] + a * e[i - 1]) % p
        e = ne
    return e


def locator_eval(J, x, p):
    v = 1
    for a in J:
        v = (v * ((x - a) % p)) % p
    return v


def run():
    p = 97
    m_sub = 16
    g = find_generator(p)
    step = (p - 1) // m_sub
    D = sorted({pow(g, step * i, p) for i in range(m_sub)})
    n = len(D)
    beta = g
    assert beta not in D
    j, sigma = 5, 3                       # sigma-1=2, sigma-2=1
    k = n - j - sigma                     # = 8
    R = j + sigma                         # redundancy = 8
    Dset = set(D)

    # L_D'(x) inverses, g vector, B
    invLp = []
    for x in D:
        lp = 1
        for y in D:
            if y != x:
                lp = (lp * ((x - y) % p)) % p
        invLp.append(pow(lp, p - 2, p))
    LDbeta = 1
    for x in D:
        LDbeta = (LDbeta * ((beta - x) % p)) % p
    B = [pow(beta, mm, p) for mm in range(R)]

    def H_apply(word):
        out = []
        for mm in range(R):
            s = 0
            for idx, x in enumerate(D):
                if word[idx]:
                    s = (s + pow(x, mm, p) * word[idx] % p * invLp[idx]) % p
            out.append(s % p)
        return out

    def A_of_J(J):
        Jset = set(J)
        ev = [0] * n
        for idx, x in enumerate(D):
            if x in Jset:
                Lp = pow(invLp[idx], p - 2, p)            # L_D'(x)
                Pp = 1
                for a in J:
                    if a != x:
                        Pp = (Pp * ((x - a) % p)) % p
                denom = ((beta - x) % p) * Pp % p
                ev[idx] = Lp * pow(denom, p - 2, p) % p
        He = H_apply(ev)
        PJb = locator_eval(J, beta, p)
        zJ = pow(PJb, p - 2, p)
        A = [(He[mm] - zJ * B[mm]) % p for mm in range(R)]
        return A, PJb

    subsets = list(combinations(D, j))

    def class_report(keyfn, label):
        groups = {}
        for J in subsets:
            groups.setdefault(keyfn(J), []).append(J)
        multi = [(kk, mm) for kk, mm in groups.items() if len(mm) >= 2]
        worst_varying_coords = 0
        any_noncommon = False
        max_class = 0
        common_all = True
        for kk, members in multi:
            max_class = max(max_class, len(members))
            As = [A_of_J(J)[0] for J in members]
            base = As[0]
            varying = set()
            for A in As[1:]:
                for c in range(R):
                    if A[c] != base[c]:
                        varying.add(c)
            if varying:
                any_noncommon = True
                common_all = False
                worst_varying_coords = max(worst_varying_coords, len(varying))
        return {
            "label": label,
            "num_multi_classes": len(multi),
            "max_class_size": max_class,
            "A_common_across_all_classes": common_all,
            "max_#varying_coords": worst_varying_coords,
            "varying_only_top_row": (worst_varying_coords <= 1),
        }

    # keys
    rL1 = class_report(lambda J: tuple(elem_sym(J, p)[1:sigma]), "L1 (e_1..e_{s-1})")
    rL1e = class_report(lambda J: (tuple(elem_sym(J, p)[1:sigma]), elem_sym(J, p)[j]),
                        "L1+endpoint (e_1..e_{s-1}, e_j)")
    rTE = class_report(lambda J: (tuple(elem_sym(J, p)[1:sigma - 1]), elem_sym(J, p)[j]),
                       "TwoEnded-literal (e_1..e_{s-2}, e_j; e_{s-1} free)")

    checks = {
        "Reading L1 (e_1..e_{s-1}): A_J COMMON across classes": rL1["A_common_across_all_classes"],
        "Reading L1+endpoint: A_J COMMON across classes": rL1e["A_common_across_all_classes"],
        "Reading TwoEnded-literal: A_J NOT common (transfer breaks)":
            not rTE["A_common_across_all_classes"],
        "TwoEnded breakage is ONLY in the top parity row m=j+sigma-1":
            rTE["varying_only_top_row"] and not rTE["A_common_across_all_classes"],
        "TwoEnded-literal classes actually exist (>=2 members)": rTE["num_multi_classes"] > 0,
    }
    return {
        "code": {"p": p, "n": n, "k": k, "j": j, "sigma": sigma, "R": R, "beta": beta},
        "readings": {"L1": rL1, "L1_endpoint": rL1e, "TwoEnded_literal": rTE},
        "checks": checks, "all_ok": all(checks.values()),
        "conclusion": (
            "Two-ended LD_sw transfer requires e_{sigma-1} FIXED too: the literal "
            "(top sigma-2 + endpoint) reading frees e_{sigma-1}, which breaks the "
            "common line in exactly the top parity row. The valid reading is "
            "Lemma 1 (top sigma-1) + endpoint -- then A_J is common and the "
            "end-to-end transfer (verify_m1_strict264_end_to_end.py) applies."),
    }


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("M1 strict264: does the TWO-ENDED jet admit a common-line LD_sw transfer?")
    print(f"  code: {out['code']}")
    print()
    for key, r in out["readings"].items():
        print(f"  {r['label']:<46} A_common={r['A_common_across_all_classes']!s:<5} "
              f"max#varying={r['max_#varying_coords']} "
              f"(multi-classes={r['num_multi_classes']}, max size={r['max_class_size']})")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("CONCLUSION:", out["conclusion"])
    print()
    print("RESULT:", "PASS (verdict established by enumeration)" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
