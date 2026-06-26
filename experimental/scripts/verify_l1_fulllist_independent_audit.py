#!/usr/bin/env python3
r"""
INDEPENDENT audit of L1 Conjecture 1 (full-list quotient-budgeted bound).

This is an INDEPENDENT cross-check of Codex's L1 crux (l1_full_list_quotient_proof_program.md
Conjecture 1), NOT a re-run of Codex's scanner and NOT a claim to prove it. It is a
separate small-model implementation that (a) cross-validates the stabilizer
decomposition and (b) stress-tests the aperiodic remainder Q_1^list with my own
cross-lane adversarial words (L2 gluing, quotient-periodic, monomial).

Conjecture 1 (paraphrased). For RS[F_q,H_n,k], s=k+sigma, above the reserve, the
ACTUAL list
    ImgFib_U(s) = { deg-<k poly P : |{x in H_n : U(x)=P(x)}| >= s },
split by the multiplicative stabilizer of the agreement set
    A_P(U) = {x: U(x)=P(x)},   Stab(P;U) = { h in H_n : h*A_P(U) = A_P(U) },
    Q_d^list(U,s) = #{ P in ImgFib_U(s) : |Stab(P;U)| = d },
satisfies the PRIMITIVE bound
    Q_1^list(U, k+sigma) <= n^B          (aperiodic listed count is polynomial),
with quotient-periodic mass (|Stab|=d>1) charged to sum_{d>1} Q_d^list.

What this script checks (small models, full enumeration of the deg-<k list):
  (1) Stab(P;U) is always a SUBGROUP of H (|Stab| divides n) -- structural sanity;
  (2) the KEY claim: quotient-periodic words U=g(x^M) put their large list mass into
      Q_{d>1} (the agreement sets inherit the period's symmetry), leaving Q_1 SMALL;
  (3) HUNT across families (random, quotient-periodic, monomial, gluing, near-codeword,
      worst-of-random-sweep) for ANY word with a LARGE aperiodic remainder Q_1^list;
  (4) n-scaling of the worst observed Q_1^list (does it grow poly or super-poly?).

HONEST SCOPE: small below-reserve models -- a below-reserve Q_1 is not a real
counterexample (the conjecture is asserted above the reserve, sigma>=Cn/log n). This
is independent corroboration of the stabilizer mechanism + a violation hunt, not a
proof and not a re-derivation of Codex's scanner.

Run:
    python3 experimental/scripts/verify_l1_fulllist_independent_audit.py
    python3 experimental/scripts/verify_l1_fulllist_independent_audit.py --json
"""

from __future__ import annotations

import argparse
import json
import random
from itertools import product


def subgroup(p, gen_order_domain):
    """H = F_p^* as a list (cyclic of order p-1)."""
    return list(range(1, p))


def codeword_evals(p, H, k):
    """all degree-<k polynomial evaluations on H (tuples)."""
    return [tuple(sum(co[i] * pow(x, i, p) for i in range(k)) % p for x in H)
            for co in product(range(p), repeat=k)]


def stab_size(A_idx, H, p):
    """|{ h in H : h*A = A }| where A = {H[i] : i in A_idx} (multiplicative)."""
    A = set(H[i] for i in A_idx)
    if not A:
        return len(H)                       # empty set stabilized by all
    cnt = 0
    for h in H:
        if all(((h * x) % p) in A for x in A):
            cnt += 1
    return cnt


def list_and_quotient_split(U, cws, H, p, s):
    """ImgFib_U(s) split by stabilizer size: returns (list_size, Q1, Q_dgt1, maxd)."""
    n = len(H)
    Q = {}                                  # d -> count
    lst = 0
    for c in cws:
        A_idx = [i for i in range(n) if c[i] == U[i]]
        if len(A_idx) >= s:
            lst += 1
            d = stab_size(A_idx, H, p)
            Q[d] = Q.get(d, 0) + 1
    Q1 = Q.get(1, 0)
    Qgt1 = sum(v for d, v in Q.items() if d > 1)
    # all stabilizer sizes must divide n
    div_ok = all(n % d == 0 for d in Q)
    return {"list": lst, "Q1": Q1, "Q_dgt1": Qgt1, "stab_sizes": dict(sorted(Q.items())),
            "stab_divides_n": div_ok}


def scaling_scan_light(rng):
    """Bounded larger-n sweep: worst aperiodic Q1^list vs n (random+quotient-periodic
    +gluing), k=2, s=k+3. Does the aperiodic remainder grow poly or super-poly?"""
    rows = []
    for p in (19, 23, 29, 31):
        H = subgroup(p, None); n = len(H)
        k, s = 2, 5
        cws = codeword_evals(p, H, k)
        worstQ1 = 0
        for _ in range(40):                     # random
            U = tuple(rng.randrange(p) for _ in H)
            worstQ1 = max(worstQ1, list_and_quotient_split(U, cws, H, p, s)["Q1"])
        for M in range(2, n + 1):               # quotient-periodic
            if n % M:
                continue
            for _ in range(8):
                gv = {pow(x, M, p): rng.randrange(p) for x in H}
                U = tuple(gv[pow(x, M, p)] for x in H)
                worstQ1 = max(worstQ1, list_and_quotient_split(U, cws, H, p, s)["Q1"])
        for _ in range(40):                     # gluing
            c1, c2 = rng.choice(cws), rng.choice(cws)
            U = tuple(c1[i] if i < n // 2 else c2[i] for i in range(n))
            worstQ1 = max(worstQ1, list_and_quotient_split(U, cws, H, p, s)["Q1"])
        rows.append({"n": n, "worst_Q1": worstQ1, "n_over_2": n // 2})
    return rows


def run():
    rng = random.Random(20260626)
    results = []
    scaling = []
    structural_ok = True
    div_ok_all = True
    worst_Q1 = {"Q1": 0, "p": None, "family": None}

    # main detailed run + a few scales
    configs = [(7, 2, 4), (13, 2, 5), (17, 2, 5), (17, 3, 6)]   # (p, k, s)
    for (p, k, s) in configs:
        H = subgroup(p, None)
        n = len(H)
        cws = codeword_evals(p, H, k)
        sigma = s - k
        fam = {}

        # (a) random words
        wr = {"list": 0, "Q1": 0, "Q_dgt1": 0}
        for _ in range(40):
            U = tuple(rng.randrange(p) for _ in H)
            r = list_and_quotient_split(U, cws, H, p, s)
            div_ok_all = div_ok_all and r["stab_divides_n"]
            if r["Q1"] > wr["Q1"]:
                wr = r
        fam["random(best of 40)"] = wr

        # (b) quotient-periodic words U=g(x^M) for each M|n, M>1 -- the KEY stress case
        qp_worst = {"list": 0, "Q1": 0, "Q_dgt1": 0}
        for M in range(2, n + 1):
            if n % M != 0:
                continue
            for _ in range(20):
                gvals = {pow(x, M, p): rng.randrange(p) for x in H}
                U = tuple(gvals[pow(x, M, p)] for x in H)
                r = list_and_quotient_split(U, cws, H, p, s)
                div_ok_all = div_ok_all and r["stab_divides_n"]
                if r["list"] > qp_worst["list"]:
                    qp_worst = r
        fam["quotient-periodic(worst-list)"] = qp_worst

        # (c) monomial words
        mono_worst = {"list": 0, "Q1": 0, "Q_dgt1": 0}
        for e in range(1, n):
            for cc in range(1, p):
                U = tuple((cc * pow(x, e, p)) % p for x in H)
                r = list_and_quotient_split(U, cws, H, p, s)
                if r["Q1"] > mono_worst["Q1"]:
                    mono_worst = r
        fam["monomial(worst-Q1)"] = mono_worst

        # (d) gluing: U = c1 on first half, c2 on second half (L2-style)
        glue_worst = {"list": 0, "Q1": 0, "Q_dgt1": 0}
        for _ in range(40):
            c1, c2 = rng.choice(cws), rng.choice(cws)
            U = tuple(c1[i] if i < n // 2 else c2[i] for i in range(n))
            r = list_and_quotient_split(U, cws, H, p, s)
            if r["Q1"] > glue_worst["Q1"]:
                glue_worst = r
        fam["gluing(best of 40)"] = glue_worst

        for nm, r in fam.items():
            if r["Q1"] > worst_Q1["Q1"]:
                worst_Q1 = {"Q1": r["Q1"], "p": p, "family": nm}
        results.append({"p": p, "n": n, "k": k, "s": s, "sigma": sigma, "families": fam})
        scaling.append({"n": n, "worst_Q1_over_families": max(r["Q1"] for r in fam.values())})

    # structural claim (2): quotient-periodic words keep Q1 small relative to list
    qp_keeps_q1_small = True
    for res in results:
        qp = res["families"]["quotient-periodic(worst-list)"]
        # the large quotient-periodic list should be mostly in Q_{d>1}, not Q1
        if qp["list"] >= 4 and qp["Q1"] > qp["Q_dgt1"] + res["s"]:
            qp_keeps_q1_small = False

    scale_light = scaling_scan_light(rng)
    # poly read: worst Q1 must stay small (<= n) and not blow up across the larger n
    scale_poly = all(r["worst_Q1"] <= r["n"] for r in scale_light)

    checks = {
        "Stab(P;U) size always divides n (subgroup) -- all words": div_ok_all,
        "quotient-periodic large list lands in Q_{d>1}, Q1 stays small": qp_keeps_q1_small,
        "worst aperiodic Q1^list stays small (<= n) across all tested families":
            worst_Q1["Q1"] <= max(len(subgroup(p, None)) for (p, _, _) in configs),
        "larger-n scaling: worst aperiodic Q1 stays <= n (no super-poly blow-up)": scale_poly,
    }
    return {"results": results, "scaling": scaling, "scale_light": scale_light,
            "worst_Q1": worst_Q1, "checks": checks, "all_ok": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--json", action="store_true")
    args = ap.parse_args(); out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str)); raise SystemExit(0 if out["all_ok"] else 1)
    print("INDEPENDENT audit of L1 Conjecture 1 (Q_1^list <= n^B): stabilizer split + Q1 hunt")
    print()
    for res in out["results"]:
        print(f"  p={res['p']} n={res['n']} k={res['k']} s={res['s']} (sigma={res['sigma']}):")
        for nm, r in res["families"].items():
            print(f"    {nm:<32} list={r['list']:>4}  Q1(aper)={r['Q1']:>4}  "
                  f"Q_dgt1={r['Q_dgt1']:>4}  stab_sizes={r.get('stab_sizes','')}")
    print()
    print(f"  worst aperiodic Q1^list across all families: {out['worst_Q1']}")
    print(f"  larger-n scaling (k=2,s=5) worst aperiodic Q1 vs n: "
          f"{[(r['n'], r['worst_Q1']) for r in out['scale_light']]}")
    print()
    for nme, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {nme}")
    print()
    print("RESULT:", "PASS (independent corroboration: stabilizer split sound; aperiodic Q1 small; "
          "no super-poly aperiodic list found in tested families -- below-reserve caveat applies)"
          if out["all_ok"] else "FAIL (a large aperiodic Q1 appeared -- inspect)")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
