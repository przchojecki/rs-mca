#!/usr/bin/env python3
r"""
Verifier for l1_general_reconstruction_collapse.md.

Checks, for background-free sunflower words with ARBITRARY petal
configurations (no coset structure), the candidate "Lemma 8.5" package:

  (1) SUB-ell IMPOSSIBILITY. A nonempty kernel set E (deg W_E <= |E|) with
      |E| < ell exists iff all scalars are equal (the degenerate
      U-is-a-codeword instance). Checked exhaustively both directions.

  (2) AGREEMENT FORMULA (Lemma B). For EVERY kernel set E (not only
      minimal ones), the reconstruction P_E = W_E * L_{C\E} agrees with U
      exactly on (all petals) u (C\E) u {x in E : W_E(x)=0}; in particular
      its exact missed core is M(E) = E \ Z(W_E).

  (3) BIJECTION (Theorem). The divisibility-minimal kernel sets (subset-
      lattice minimality, blockers of every size >= 1) coincide exactly
      with the exact missed cores of the full brute-force list-decoded
      full-petal codewords, across consecutive-block, random, and coset
      petal shapes.

  (4) COROLLARY SPOT-CHECK. t=3 coset instances: minimal sets == {beta
      coset} when resonant else empty (PR #218's Theorem 4 re-derived from
      the general lemma), over 200 scalar vectors covering both resonance
      classes. (t>=5 instances are covered in the companion note's
      evidence, not gated here.)

HONEST SCOPE: finite verification of the lemma's statements on decode-
feasible instances; the lemma's proof lives in the companion note. The
open growth question (#minimal kernel sets in the asymptotic regime) is
NOT addressed here.

Run:
    python3 verify_l1_general_reconstruction_collapse.py [--json]
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    eval_poly,
    interpolate_polynomial,
    poly_degree,
    trim_poly,
)
from verify_l1_full_petal_growing_defect_witnesses import (  # noqa: E402
    crt_residue_degree,
    exact_list_decode,
    locator,
)


def det_rng(seed: int):
    state = seed

    def rand(n: int) -> int:
        nonlocal state
        state = (state * 1103515245 + 12345) % (2**31)
        return state % n

    return rand


def sample(rand, pool: list[int], m: int) -> list[int]:
    pool = pool[:]
    out = []
    for _ in range(m):
        out.append(pool.pop(rand(len(pool))))
    return out


def crt_rep(petals, scalars, target, p):
    """Degree-< t*ell CRT representative of (c_i * target mod L_{T_i}),
    computed by interpolation through all petal points."""
    xs, ys = [], []
    for pt, c in zip(petals, scalars):
        for x in pt:
            xs.append(x)
            ys.append(c * eval_poly(target, x, p) % p)
    return list(trim_poly(interpolate_polynomial(xs, ys, p)))


def poly_mul(A, B, p):
    C = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        if a:
            for j, b in enumerate(B):
                C[i + j] = (C[i + j] + a * b) % p
    return C


class Instance:
    def __init__(self, p, petals, scalars, core):
        self.p, self.petals, self.scalars, self.core = p, petals, scalars, core
        self.ell, self.t = len(petals[0]), len(petals)
        self.domain = [x for pt in petals for x in pt] + core
        assert len(set(self.domain)) == len(self.domain)
        self.k = len(core) + 1
        self.s = self.k + self.ell - 1
        self.L_C = locator(core, p)
        self.u = {x: 0 for x in core}
        for pt, c in zip(petals, scalars):
            for x in pt:
                self.u[x] = c * eval_poly(self.L_C, x, p) % p

    def kernel_map(self, max_size):
        km = {}
        for size in range(1, max_size + 1):
            for E in itertools.combinations(self.core, size):
                L_E = locator(list(E), self.p)
                km[frozenset(E)] = (
                    crt_residue_degree(self.petals, self.scalars, L_E, self.p) <= size
                )
        return km

    def reconstruction(self, E):
        L_E = locator(sorted(E), self.p)
        W = crt_rep(self.petals, self.scalars, L_E, self.p)
        rest = [x for x in self.core if x not in E]
        P = poly_mul(W, list(locator(rest, self.p)), self.p)
        agr = frozenset(
            x for x in self.domain if eval_poly(tuple(P), x, self.p) == self.u[x]
        )
        return W, agr


def check_sub_ell() -> dict:
    checked, viol = 0, []
    rand = det_rng(97531)
    for p in (19, 23, 31, 37):
        for ell, t in ((2, 3), (3, 3), (3, 2), (4, 3), (5, 2)):
            for shape in ("consec", "random"):
                for trial in range(4):
                    if shape == "consec":
                        pts = list(range(1, 1 + t * ell))
                    else:
                        pts = sample(rand, list(range(1, p)), t * ell)
                    petals = [pts[i * ell:(i + 1) * ell] for i in range(t)]
                    pool = [x for x in range(1, p) if x not in pts]
                    if len(pool) < 5:
                        continue
                    core = sample(rand, pool, 5)
                    for degenerate in (False, True):
                        if degenerate:
                            scalars = [3] * t
                        else:
                            scalars = [1 + rand(p - 1) for _ in range(t)]
                            if len(set(scalars)) == 1:
                                scalars[0] = scalars[0] % (p - 1) + 1
                        inst = Instance(p, petals, scalars, core)
                        found = False
                        for size in range(1, ell):
                            for E in itertools.combinations(core, size):
                                L_E = locator(list(E), p)
                                if crt_residue_degree(petals, scalars, L_E, p) <= size:
                                    found = True
                        checked += 1
                        if found != degenerate:
                            viol.append((p, ell, t, shape, scalars, "found" if found else "none"))
    return {"checked": checked, "violations": viol[:5], "ok": not viol}


def bijection_on(inst: Instance) -> tuple[bool, dict]:
    km = inst.kernel_map((inst.t - 1) * inst.ell)

    def minimal(E):
        if not km[E]:
            return False
        return not any(
            km[frozenset(F)]
            for size in range(1, len(E))
            for F in itertools.combinations(sorted(E), size)
        )

    kernel_sets = [E for E, ok in km.items() if ok]
    minimals = sorted(
        (sorted(E) for E in kernel_sets if len(E) >= inst.ell and minimal(frozenset(E))),
        key=lambda x: (len(x), x),
    )

    # Lemma B on every kernel set
    lemma_b_ok = True
    for E in kernel_sets:
        W, agr = inst.reconstruction(E)
        z = {x for x in E if eval_poly(tuple(W), x, inst.p) == 0}
        expected = (
            {x for pt in inst.petals for x in pt}
            | (set(inst.core) - set(E))
            | z
        )
        if agr != frozenset(expected):
            lemma_b_ok = False

    listed = exact_list_decode(inst.domain, inst.u, inst.k, inst.s, inst.p)
    planted = [frozenset(inst.core) | frozenset(pt) for pt in inst.petals]
    decoded = sorted(
        (sorted(set(inst.core) - agr)
         for agr in listed.values()
         if agr not in planted
         and all(set(pt) <= agr for pt in inst.petals)
         and len(set(inst.core) - agr) > 0),
        key=lambda x: (len(x), x),
    )
    ok = (minimals == decoded) and lemma_b_ok
    return ok, {
        "n_kernel_sets": len(kernel_sets),
        "minimals": minimals,
        "decoded_missed_cores": decoded,
        "lemma_b_ok": lemma_b_ok,
    }


def check_bijection() -> dict:
    rand = det_rng(24680)
    total, failures, nonzero = 0, [], 0
    for p in (19, 23, 29, 31):
        for ell, t in ((2, 3), (3, 3), (2, 4), (2, 2), (3, 2)):
            for shape in ("consec", "random"):
                for trial in range(3):
                    if shape == "consec":
                        pts = list(range(1, 1 + t * ell))
                    else:
                        pts = sample(rand, list(range(1, p)), t * ell)
                    petals = [pts[i * ell:(i + 1) * ell] for i in range(t)]
                    pool = [x for x in range(1, p) if x not in pts]
                    if len(pool) < 6:
                        continue
                    core = sample(rand, pool, 6)
                    scalars = sample(rand, list(range(1, p)), t)
                    inst = Instance(p, petals, scalars, core)
                    ok, info = bijection_on(inst)
                    total += 1
                    nonzero += bool(info["minimals"])
                    if not ok:
                        failures.append((p, ell, t, shape, scalars, info))
    return {
        "instances": total,
        "instances_with_nonzero_count": nonzero,
        "failures": failures[:3],
        "ok": not failures,
    }


def check_coset_corollary() -> dict:
    """t=3 coset instances: minimals == {beta coset} iff resonant."""
    p = 19
    H = [1, 7, 11]
    all_cosets = []
    seen = set()
    for g in range(1, p):
        if g in seen:
            continue
        cs = sorted(g * h % p for h in H)
        all_cosets.append(cs)
        seen.update(cs)
    petals = all_cosets[:3]
    labels = [pow(cs[0], 3, p) for cs in petals]
    rest_pts = [x for cs in all_cosets[3:] for x in cs]
    checked, viol, res_seen, non_seen = 0, [], 0, 0

    def beta_of(scalars):
        s0 = s1 = 0
        for a, c in zip(labels, scalars):
            lp = 1
            for b in labels:
                if b != a:
                    lp = lp * (a - b) % p
            w = c * pow(lp, p - 3 + 1, p) % p  # c / lp
            s0 = (s0 + w) % p
            s1 = (s1 + w * a) % p
        return None if s0 == 0 else s1 * pow(s0, p - 2, p) % p

    coset_by_label = {pow(cs[0], 3, p): cs for cs in all_cosets[3:]}
    for scalars in itertools.permutations(range(1, 8), 3):
        beta = beta_of(list(scalars))
        if beta is None:
            continue
        resonant = beta in coset_by_label
        core = rest_pts[:]  # all three remaining cosets
        inst = Instance(p, petals, list(scalars), core)
        km = inst.kernel_map(2 * 3 - 1)  # sizes 1..2ell-1 (interior window)
        minimals = []
        for E, okk in km.items():
            if not okk or len(E) < 3:
                continue
            if not any(
                km[frozenset(F)]
                for size in range(1, len(E))
                for F in itertools.combinations(sorted(E), size)
            ):
                minimals.append(sorted(E))
        expect = [sorted(coset_by_label[beta])] if resonant else []
        checked += 1
        res_seen += resonant
        non_seen += not resonant
        if sorted(minimals) != sorted(expect):
            viol.append((list(scalars), beta, resonant, minimals, expect))
    return {
        "checked": checked,
        "resonant_seen": res_seen,
        "nonresonant_seen": non_seen,
        "violations": viol[:3],
        "ok": not viol and res_seen > 0 and non_seen > 0,
    }


def check_range_necessity() -> dict:
    """Reproduce the G1-audit counterexamples showing the kernel-set range
    restriction ell <= |E| <= (t-1)ell is essential, not cosmetic."""
    # (a) over-broad 'minimal kernel set' whose reconstruction is NOT listed
    p = 17
    inst = Instance(p, [[1, 2], [3, 4], [5, 6]], [3, 10, 5], [8, 9, 10, 11, 12])
    E = frozenset(inst.core)  # |E| = 5 > (t-1)ell = 4
    L_E = locator(sorted(E), p)
    broad_kernel = crt_residue_degree(inst.petals, inst.scalars, L_E, p) <= len(E)
    W, agr = inst.reconstruction(E)
    m_e = {x for x in E if eval_poly(tuple(W), x, p) != 0}
    not_listed = len(agr) < inst.s
    a_ok = broad_kernel and m_e == set(E) and not_listed

    # (b) Lemma A's conclusion fails at |D| >= t*ell
    inst2 = Instance(p, [[1, 2], [3, 4], [5, 6]], [5, 2, 3], [8, 10, 11, 12, 13, 14])
    D = frozenset(inst2.core)  # |D| = 6 = t*ell
    E2 = frozenset({8, 10, 12, 13})
    dD = crt_residue_degree(inst2.petals, inst2.scalars, locator(sorted(D), p), p)
    dE = crt_residue_degree(inst2.petals, inst2.scalars, locator(sorted(E2), p), p)
    _, agr_D = inst2.reconstruction(D)
    _, agr_E = inst2.reconstruction(E2)
    b_ok = dD <= len(D) and dE <= len(E2) and agr_D != agr_E

    return {"overbroad_not_listed": a_ok, "lemma_a_out_of_range_fails": b_ok,
            "ok": a_ok and b_ok}


def run() -> dict:
    c1 = check_sub_ell()
    c2c3 = check_bijection()
    c4 = check_coset_corollary()
    c5 = check_range_necessity()
    checks = {
        "(1) sub-ell kernel sets iff all-equal scalars": c1["ok"],
        "(2)+(3) Lemma B agreement formula + bijection vs decode": c2c3["ok"],
        "(4) t=3 coset corollary (PR #218 re-derived)": c4["ok"],
        "(5) range restriction is essential (G1 counterexamples)": c5["ok"],
    }
    return {
        "sub_ell": c1,
        "bijection": c2c3,
        "coset_corollary": c4,
        "range_necessity": c5,
        "checks": checks,
        "all_ok": all(checks.values()),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str))
        raise SystemExit(0 if out["all_ok"] else 1)
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    print(f"    sub-ell: {out['sub_ell']['checked']} instance-classes")
    print(f"    bijection: {out['bijection']['instances']} instances "
          f"({out['bijection']['instances_with_nonzero_count']} with nonzero counts)")
    print(f"    coset corollary: {out['coset_corollary']['checked']} scalar vectors "
          f"({out['coset_corollary']['resonant_seen']} resonant / "
          f"{out['coset_corollary']['nonresonant_seen']} non-resonant)")
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
