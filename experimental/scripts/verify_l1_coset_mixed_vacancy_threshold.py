#!/usr/bin/env python3
r"""
Verifier for l1_coset_mixed_vacancy_threshold.md.

Background-free coset sunflower over F_p: H = mu_ell (order-ell, ell | p-1);
t coset petals T_i = a_i H (locators X^ell - alpha_i, alpha_i = a_i^ell);
m core cosets, C = union of b_j H; distinct nonzero scalars c_i; received word
U = c_i L_C on petal i, 0 on C.  k = m*ell+1, s = (m+1)*ell.  By the PR #219
bijection (l1_general_reconstruction_collapse.md), listed full-petal codewords
biject with divisibility-minimal kernel sets E (ell <= |E| <= (t-1)ell,
deg W_E <= |E|), E = exact missed core.  MIXED = not a union of full H-cosets;
PRIMITIVE = trivial stabilizer Stab_H(E) = {1}.

Gates:

  (i)  BASE THEOREM (m <= t).  For a grid of coset configs with m <= t: the
       entire affine lift space of full-petal codewords (deg <= m*ell) is
       H-invariant (support on exponents divisible by ell), verified by exact
       Gaussian elimination over F_p; AND, independently, every minimal kernel
       set enumerated over the core is a coset union (mixed-minimal count 0).
       This is Theorem A: m <= t  =>  no mixed minimal kernel sets.

  (ii) SHARPNESS (m = t+1).  Explicit mixed minimal kernel sets at (t=3,ell=4)
       and (t=4,ell=3), the first m where mixed appears, so the m <= t floor is
       not vacuous and cannot be pushed to m <= t+1.

  (iii) REFUTATION (composite ell, m < ell).  Three explicit witnesses at
       ell=6, t=3, m=4 (< ell), p in {487, 2011, 499}: each E is a kernel set,
       divisibility-minimal (EXHAUSTIVE over all proper subsets of size >= ell),
       has M(E)=E, is NOT a coset union (mixed), and P_E is a genuine listed
       codeword (agreement s, exact missed core E).  So the naive "m < ell =>
       no mixed minimal kernel set" is FALSE for composite ell.  Each witness is
       IMPRIMITIVE (|Stab_H(E)| = 3): it descends to the quotient ledger.

  (iv) SAMPLING-ARTIFACT CORRECTION.  (t=4,ell=3,m=5) has a PRIMITIVE
       (|Stab_H(E)| = 1) mixed minimal kernel set at p=8101, scalars
       [3487,4735,3412,6002] -- superseding an earlier informally-sampled zero.

HONEST SCOPE: finite verification of stated theorem instances and explicit
certificates; the proof of Theorem A lives in the companion note.  The open
target -- PRIMITIVE mixed-vacancy for m < ell -- is NOT gated here (no primitive
mixed minimal set is asserted to exist at m < ell; none is known).

Run:
    python3 verify_l1_coset_mixed_vacancy_threshold.py [--json]

stdlib-only, offline, deterministic; exit 0 iff every gate passes.
"""
from __future__ import annotations
import argparse
import itertools
import json


# ---------- polynomial algebra over F_p (own, stdlib-only) ----------
def pmul(a, b, p):
    C = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                C[i + j] = (C[i + j] + ai * bj) % p
    while len(C) > 1 and C[-1] == 0:
        C.pop()
    return C


def loc(roots, p):
    o = [1]
    for r in roots:
        o = pmul(o, [(-r) % p, 1], p)
    return o


def peval(a, x, p):
    v = 0
    for c in reversed(a):
        v = (v * x + c) % p
    return v


def interp(xs, ys, p):
    """Lagrange interpolation; returns coeff list (low->high), trimmed."""
    res = [0]
    for j in range(len(xs)):
        num, den = [1], 1
        for k in range(len(xs)):
            if k == j:
                continue
            num = pmul(num, [(-xs[k]) % p, 1], p)
            den = den * (xs[j] - xs[k]) % p
        sca = ys[j] * pow(den, -1, p) % p
        term = [c * sca % p for c in num]
        if len(term) > len(res):
            res += [0] * (len(term) - len(res))
        for i, c in enumerate(term):
            res[i] = (res[i] + c) % p
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res


# ---------- coset construction (own; for the base-theorem grid) ----------
def prim_root(p):
    n, f, d = p - 1, set(), 2
    while d * d <= n:
        while n % d == 0:
            f.add(d)
            n //= d
        d += 1
    if n > 1:
        f.add(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in f):
            return g
    raise RuntimeError


def all_cosets(p, ell):
    g = prim_root(p)
    h = pow(g, (p - 1) // ell, p)
    H = sorted({pow(h, j, p) for j in range(ell)})
    out, used = [], set()
    for x in range(1, p):
        if x in used:
            continue
        cs = sorted(x * e % p for e in H)
        if len(cs) == ell and not (set(cs) & used):
            out.append(cs)
            used |= set(cs)
    return out, H


# ---------- sunflower kernel-set primitives ----------
def W_of(E, petals, c, p):
    """Degree-<t*ell CRT rep of (c_i L_E mod X^ell-alpha_i), via interpolation
    through all petal points."""
    LE = loc(sorted(E), p)
    xs, ys = [], []
    for pt, ci in zip(petals, c):
        for x in pt:
            xs.append(x)
            ys.append(ci * peval(LE, x, p) % p)
    return interp(xs, ys, p)


def is_kernel(E, petals, c, p, ell, top):
    if not (ell <= len(E) <= top):
        return False
    return len(W_of(E, petals, c, p)) - 1 <= len(E)


def derive_H(petals, p):
    inv0 = pow(petals[0][0], -1, p)
    return sorted((x * inv0) % p for x in petals[0])


def is_coset_union(E, H, p):
    Es = set(E)
    return all((x * h) % p in Es for x in E for h in H)


def stab_order(E, H, p):
    Es = set(E)
    return sum(1 for h in H if set((x * h) % p for x in E) == Es)


def minimal_exhaustive(E, petals, c, p, ell, top):
    """True iff no proper nonempty subset (necessarily size >= ell for distinct
    scalars) is a kernel set.  EXHAUSTIVE over sizes ell..|E|-1."""
    d = len(E)
    for r in range(ell, d):
        for sub in itertools.combinations(sorted(E), r):
            if is_kernel(sub, petals, c, p, ell, top):
                return False
    return True


# ---------- Gaussian elimination: full-petal lift space over F_p ----------
def solve_space(A, b, p):
    """Solve A x = b over F_p.  Return (particular, nullbasis) or None if
    inconsistent.  A: list of rows; b: rhs."""
    m = len(A)
    n = len(A[0]) if m else 0
    M = [row[:] + [b[i] % p] for i, row in enumerate(A)]
    piv = {}
    r = 0
    for col in range(n):
        pr = next((i for i in range(r, m) if M[i][col] % p != 0), None)
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][col], -1, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for i in range(m):
            if i != r and M[i][col] % p != 0:
                f = M[i][col]
                M[i] = [(M[i][k] - f * M[r][k]) % p for k in range(n + 1)]
        piv[col] = r
        r += 1
        if r == m:
            break
    for i in range(r, m):
        if M[i][n] % p != 0:
            return None  # inconsistent
    particular = [0] * n
    for col, row in piv.items():
        particular[col] = M[row][n] % p
    free = [c for c in range(n) if c not in piv]
    nullbasis = []
    for fc in free:
        v = [0] * n
        v[fc] = 1
        for col, row in piv.items():
            v[col] = (-M[row][fc]) % p
        nullbasis.append(v)
    return particular, nullbasis


# ---------- gate (i): base theorem ----------
def check_base_theorem():
    grid = [
        (29, 2, 2, [1, 2]), (29, 2, 3, [1, 2, 3]),
        (31, 3, 2, [1, 2]), (31, 3, 3, [1, 2, 3]),
        (41, 4, 2, [1, 2]), (41, 4, 3, [1, 2, 3]),
    ]
    scalar_banks = {2: [[2, 3, 5], [7, 11, 13]], 3: [[2, 3, 5], [4, 7, 9]],
                    4: [[3, 5, 7], [2, 9, 11]]}
    configs, fails = 0, []
    for p, ell, t, _ in grid:
        cs, H = all_cosets(p, ell)
        for m in range(1, t + 1):  # m <= t
            petals = cs[:t]
            core = sorted(x for cc in cs[t:t + m] for x in cc)
            top = (t - 1) * ell
            LC = loc(core, p)
            for cbank in scalar_banks[ell]:
                c = [cbank[i] % p for i in range(t)]
                if len(set(c)) != t or 0 in c:
                    continue
                configs += 1
                # --- structural: lift space H-invariant ---
                A, b = [], []
                for pt, ci in zip(petals, c):
                    for x in pt:
                        A.append([pow(x, a, p) for a in range(m * ell + 1)])
                        b.append(ci * peval(LC, x, p) % p)
                sol = solve_space(A, b, p)
                struct_ok = True
                if sol is not None:  # empty lift => vacuously H-invariant
                    part, nb = sol
                    vecs = [part] + nb
                    struct_ok = all(
                        all(v[a] == 0 for a in range(len(v)) if a % ell != 0)
                        for v in vecs
                    )
                # --- enumeration: no mixed minimal kernel set ---
                K = []
                for d in range(ell, top + 1):
                    for E in itertools.combinations(core, d):
                        if len(W_of(E, petals, c, p)) - 1 <= d:
                            K.append(frozenset(E))
                Kset = set(K)
                mixed_minimal = 0
                for E in K:
                    if any(F < E for F in Kset):
                        continue  # not minimal
                    if not is_coset_union(sorted(E), H, p):
                        mixed_minimal += 1
                if not struct_ok or mixed_minimal != 0:
                    fails.append((p, ell, t, m, c, struct_ok, mixed_minimal))
    return {"configs": configs, "failures": fails[:5], "ok": not fails}


# ---------- embedded witnesses (generated + independently pre-verified) ----------
WITNESSES = {
    # composite-ell m<ell refutation (all IMPRIMITIVE, |Stab|=3)
    "A_p487": dict(
        p=487, ell=6, t=3, m=4, c=[486, 317, 379],
        petals=[[1, 232, 233, 254, 255, 486], [2, 21, 23, 464, 466, 485],
                [3, 209, 212, 275, 278, 484]],
        core=[4, 5, 6, 7, 42, 46, 63, 69, 163, 170, 186, 191, 296, 301, 317, 324,
              418, 424, 441, 445, 480, 481, 482, 483],
        E=[4, 5, 6, 42, 63, 170, 186, 296, 324, 418, 441, 480],
        stab=3, agree=30),
    "B_p2011": dict(
        p=2011, ell=6, t=3, m=4, c=[381, 1494, 991],
        petals=[[1, 205, 206, 1805, 1806, 2010], [2, 410, 412, 1599, 1601, 2009],
                [3, 615, 618, 1393, 1396, 2008]],
        core=[4, 5, 6, 7, 569, 576, 775, 781, 820, 824, 981, 986, 1025, 1030,
              1187, 1191, 1230, 1236, 1435, 1442, 2004, 2005, 2006, 2007],
        E=[5, 7, 569, 781, 824, 981, 1025, 1191, 1236, 1435, 2005, 2007],
        stab=3, agree=30),
    "C_p499": dict(
        p=499, ell=6, t=3, m=4, c=[97, 23, 83],
        petals=[[1, 139, 140, 359, 360, 498], [2, 219, 221, 278, 280, 497],
                [3, 79, 82, 417, 420, 496]],
        core=[4, 5, 6, 7, 18, 25, 57, 61, 158, 164, 196, 201, 298, 303, 335, 341,
              438, 442, 474, 481, 492, 493, 494, 495],
        E=[5, 6, 7, 18, 61, 158, 196, 298, 335, 442, 474, 495],
        stab=3, agree=30),
    # sharpness (3,4) at m=t+1 (IMPRIMITIVE here, |Stab|=2)
    "D_sharp_34": dict(
        p=8161, ell=4, t=3, m=4, c=[2408, 3412, 6002],
        petals=[[1, 202, 7959, 8160], [2, 404, 7757, 8159], [3, 606, 7555, 8158]],
        core=[4, 5, 6, 7, 808, 1010, 1212, 1414, 6747, 6949, 7151, 7353,
              8154, 8155, 8156, 8157],
        E=[4, 5, 6, 7, 8154, 8155, 8156, 8157],
        stab=2, agree=20),
    # sharpness (4,3) at m=t+1 AND the sampled-zero correction (PRIMITIVE, |Stab|=1)
    "E_corr_43": dict(
        p=8101, ell=3, t=4, m=5, c=[3487, 4735, 3412, 6002],
        petals=[[1, 2217, 5883], [2, 3665, 4434], [3, 1447, 6651], [4, 767, 7330]],
        core=[5, 6, 7, 8, 9, 676, 1534, 2894, 2984, 3751, 4341, 5112, 5201,
              6559, 7418],
        E=[5, 6, 7, 8, 9, 676, 1534, 2894, 2984],
        stab=1, agree=18),
}


def verify_witness(w):
    p, ell, t, m = w["p"], w["ell"], w["t"], w["m"]
    petals, core, c, E = w["petals"], w["core"], w["c"], w["E"]
    top = (t - 1) * ell
    k = m * ell + 1
    s = (m + 1) * ell
    H = derive_H(petals, p)
    info = {}
    # config sanity: genuine mu_ell cosets, background-free, distinct scalars
    info["H_order"] = (len(H) == ell)
    dom = [x for pt in petals for x in pt] + core
    info["background_free"] = (len(set(dom)) == len(dom) and 0 not in dom)
    info["petals_are_cosets"] = all(
        set((pt[0] * h) % p for h in H) == set(pt) for pt in petals)
    info["core_cosets"] = (len(core) == m * ell)
    info["scalars_distinct_nonzero"] = (len(set(c)) == t and 0 not in c)
    info["E_in_core"] = set(E) <= set(core)
    # kernel-set membership
    WE = W_of(E, petals, c, p)
    degWE = len(WE) - 1
    info["in_range"] = (ell <= len(E) <= top)
    info["is_kernel"] = (degWE <= len(E))
    info["degWE"] = degWE
    # M(E) = E
    info["M(E)=E"] = not any(peval(WE, x, p) == 0 for x in E)
    # minimality (EXHAUSTIVE)
    info["minimal"] = minimal_exhaustive(E, petals, c, p, ell, top)
    # mixed (not a coset union)
    info["mixed"] = not is_coset_union(E, H, p)
    # stabilizer
    so = stab_order(E, H, p)
    info["stab"] = so
    info["stab_matches"] = (so == w["stab"])
    info["primitive"] = (so == 1)
    # P_E listed with exact missed core E
    CmE = [x for x in core if x not in set(E)]
    PE = pmul(WE, loc(CmE, p), p)
    info["degPE_ok"] = (len(PE) - 1 <= k - 1)
    LC = loc(core, p)
    agree, missed = 0, []
    for pt, ci in zip(petals, c):
        for x in pt:
            if peval(PE, x, p) == ci * peval(LC, x, p) % p:
                agree += 1
    for x in core:
        if peval(PE, x, p) == 0:
            agree += 1
        else:
            missed.append(x)
    info["agree"] = agree
    info["listed"] = (agree >= s)
    info["agree_matches"] = (agree == w["agree"])
    info["missed=E"] = (sorted(missed) == sorted(E))
    info["s"] = s
    # REQUIRED pass conditions (descriptive fields primitive/stab/degWE/agree/s
    # are recorded but NOT gating).
    required = ["H_order", "background_free", "petals_are_cosets", "core_cosets",
                "scalars_distinct_nonzero", "E_in_core", "in_range", "is_kernel",
                "M(E)=E", "minimal", "mixed", "stab_matches", "degPE_ok",
                "listed", "agree_matches", "missed=E"]
    ok = all(info[key] for key in required)
    return ok, info


# ---------- gate (ii): sharpness ----------
def check_sharpness():
    fails, detail = [], {}
    for name in ("D_sharp_34", "E_corr_43"):
        w = WITNESSES[name]
        ok, info = verify_witness(w)
        detail[name] = {"t": w["t"], "ell": w["ell"], "m": w["m"],
                        "mtplus1": w["m"] == w["t"] + 1, "stab": info["stab"],
                        "listed_mixed_minimal": ok}
        if not ok or w["m"] != w["t"] + 1:
            fails.append((name, info))
    return {"witnesses": detail, "failures": fails[:2], "ok": not fails}


# ---------- gate (iii): composite-ell refutation ----------
def check_refutation():
    fails, detail = [], {}
    for name in ("A_p487", "B_p2011", "C_p499"):
        w = WITNESSES[name]
        ok, info = verify_witness(w)
        detail[name] = {
            "p": w["p"], "t": w["t"], "ell": w["ell"], "m": w["m"],
            "m_lt_ell": w["m"] < w["ell"], "degWE": info["degWE"],
            "minimal": info["minimal"], "mixed": info["mixed"],
            "M(E)=E": info["M(E)=E"], "listed": info["listed"],
            "agree": info["agree"], "stab": info["stab"],
            "imprimitive": info["stab"] > 1,
        }
        if not (ok and w["m"] < w["ell"] and info["stab"] > 1):
            fails.append((name, info))
    return {"witnesses": detail, "failures": fails[:3], "ok": not fails}


# ---------- gate (iv): sampling-artifact correction ----------
def check_correction():
    w = WITNESSES["E_corr_43"]
    ok, info = verify_witness(w)
    good = ok and info["stab"] == 1 and info["mixed"] and info["minimal"] and info["listed"]
    return {
        "config": "(t=4,ell=3,m=5) p=8101 c=[3487,4735,3412,6002]",
        "primitive_mixed_minimal_listed": good,
        "stab": info["stab"], "agree": info["agree"], "s": info["s"],
        "supersedes": "earlier sampled mixed=0 at (t=4,ell=3,m=5)",
        "ok": good,
    }


def run():
    g1 = check_base_theorem()
    g2 = check_sharpness()
    g3 = check_refutation()
    g4 = check_correction()
    checks = {
        "(i) base theorem m<=t: lift H-invariant + zero mixed minimal": g1["ok"],
        "(ii) sharpness: mixed minimal at m=t+1 for (3,4) and (4,3)": g2["ok"],
        "(iii) composite-ell m<ell refutation (487/2011/499, imprimitive)": g3["ok"],
        "(iv) (4,3,m=5) primitive mixed minimal (sampled-zero correction)": g4["ok"],
    }
    return {"base_theorem": g1, "sharpness": g2, "refutation": g3,
            "correction": g4, "checks": checks, "all_ok": all(checks.values())}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2, default=str))
        raise SystemExit(0 if out["all_ok"] else 1)
    for name, ok in out["checks"].items():
        print(f"  [{'OK ' if ok else 'FAIL'}] {name}")
    print(f"    base theorem: {out['base_theorem']['configs']} coset configs (m<=t)")
    print(f"    refutation witnesses: "
          f"{', '.join(k for k in out['refutation']['witnesses'])}")
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    raise SystemExit(0 if out["all_ok"] else 1)


if __name__ == "__main__":
    main()
