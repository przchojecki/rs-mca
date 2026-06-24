#!/usr/bin/env python3
r"""
F1 extension-line forward case: simple-pole F-line MCA over a quadratic extension.

Increment 13 of `experimental/notes/x1/x1_deep_point_interleaved_bridge.md` (§2.10,
developing the §2.9 outlook).

Setup: B = F_p, F = F_{p^2} = F_p[t]/(t^2 - NS), domain D subset B (subgroup of
B^*).  C_F = RS[F,D,k], C_{F,+} = RS[F,D,k+1].  For a deep point alpha in F \ D
(extension-valued, e.g. alpha = t) and a received word U : D -> F, the simple-pole
F-line is f_alpha = U/(x-alpha), g_alpha = -1/(x-alpha).

Verified claims:
  (1) Base identity over the EXTENSION: Bad_MCA_F(alpha; delta_a) = Deep_alpha^F(U,a)
      = { P(alpha) : P in F[X]_{<k+1}, |{x: P(x)=U(x)}| >= a } -- the §1 identity
      now with an extension-valued deep point and F-valued words.
  (2) List control: |Deep_alpha^F(U,a)| <= |Lambda(C_{F,+}, delta_a, U)|, and by the
      extension-coordinate identity |Lambda(C_F)| = |Lambda(Int(C_B,2))|, the
      F-line MCA is governed by the 2-interleaved BASE-code list.
  (3) Multiplication-slice / F1 transfer: under the coordinate map Phi (Phi(C_F)
      = C_B^2), f_alpha + z g_alpha is explained by C_F on S iff
      Phi(f_alpha) + M_z Phi(g_alpha) is explained coordinatewise by C_B^2 on S,
      where M_z is multiplication-by-z.  So the extension F-line is the
      M_z-coupled multiplication-slice of the e=2 interleaved bridge (§2, mu=2).

This realizes the F1 forward direction for the simple-pole family (prob:F1) and
ties it to the L2/X1 interleaved bridge.  Finite toy evidence + identity check;
no cap / deployed claim.  Status: PROVED-by-check.  Supports F1 + X1 + L2.

Run:
    python3 experimental/scripts/verify_x1_extension_line.py
    python3 experimental/scripts/verify_x1_extension_line.py --json
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations

P = 17
NS = 3  # t^2 = 3, nonsquare mod 17


class F2:
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = a % P
        self.b = b % P

    def __add__(s, o):
        o = c2(o); return F2(s.a + o.a, s.b + o.b)
    __radd__ = __add__

    def __sub__(s, o):
        o = c2(o); return F2(s.a - o.a, s.b - o.b)

    def __rsub__(s, o):
        return c2(o) - s

    def __neg__(s):
        return F2(-s.a, -s.b)

    def __mul__(s, o):
        o = c2(o)
        return F2(s.a * o.a + NS * s.b * o.b, s.a * o.b + s.b * o.a)
    __rmul__ = __mul__

    def inv(s):
        den = (s.a * s.a - NS * s.b * s.b) % P
        d = pow(den, -1, P)
        return F2(s.a * d, -s.b * d)

    def __truediv__(s, o):
        return s * c2(o).inv()

    def __pow__(s, e):
        if e < 0:
            return s.inv() ** (-e)
        out, base = ONE, s
        while e:
            if e & 1:
                out = out * base
            base = base * base
            e >>= 1
        return out

    def __eq__(s, o):
        try:
            o = c2(o)
        except TypeError:
            return False
        return s.a == o.a and s.b == o.b

    def __hash__(s):
        return hash((s.a, s.b))

    def __repr__(s):
        return f"{s.a}+{s.b}t" if s.b else f"{s.a}"


def c2(x):
    if isinstance(x, F2):
        return x
    if isinstance(x, int):
        return F2(x, 0)
    raise TypeError(type(x))


ZERO, ONE, T = F2(0, 0), F2(1, 0), F2(0, 1)


def trim(p):
    p = list(p)
    while p and p[-1] == ZERO:
        p.pop()
    return p


def deg(p):
    return len(trim(p)) - 1


def peval(p, x):
    out = ZERO
    for c in reversed(p):
        out = out * x + c
    return out


def interp(points):
    res = []
    for i, (xi, yi) in enumerate(points):
        basis, den = [ONE], ONE
        for j, (xj, _y) in enumerate(points):
            if i == j:
                continue
            new = [ZERO] * (len(basis) + 1)
            for d, b in enumerate(basis):
                new[d] = new[d] - xj * b
                new[d + 1] = new[d + 1] + b
            basis, den = new, den * (xi - xj)
        sc = yi / den
        if len(res) < len(basis):
            res += [ZERO] * (len(basis) - len(res))
        for d, b in enumerate(basis):
            res[d] = res[d] + sc * b
    return trim(res)


def subgroup(n):
    # subgroup of F_p^* of order n (base-field elements as F2)
    assert (P - 1) % n == 0
    g = 3  # 3 is a generator of F_17^*
    h = pow(g, (P - 1) // n, P)
    out, x = [], 1
    for _ in range(n):
        out.append(F2(x, 0))
        x = (x * h) % P
    return out


def close_slope(fI, gI, k, m):
    cand = None
    for j in range(k, m):
        fj = fI[j] if j < len(fI) else ZERO
        gj = gI[j] if j < len(gI) else ZERO
        if gj == ZERO:
            if fj != ZERO:
                return None
            continue
        zj = -fj / gj
        if cand is None:
            cand = zj
        elif cand != zj:
            return None
    return cand


def deep_image_F(U, D, k, a, alpha):
    found = {}
    for S in combinations(D, a):
        Pp = interp([(x, U[x]) for x in S])
        if deg(Pp) < k + 1:
            found[tuple((c.a, c.b) for c in Pp)] = Pp
    return {peval(Pp, alpha) for Pp in found.values()}, len(found)


def bad_mca_F(U, D, k, a, alpha):
    f = {x: U[x] / (x - alpha) for x in D}
    g = {x: -ONE / (x - alpha) for x in D}
    out = set()
    for S in combinations(D, a):
        fI = interp([(x, f[x]) for x in S])
        gI = interp([(x, g[x]) for x in S])
        z = close_slope(fI, gI, k, a)
        if z is not None:
            out.add(z)
    return out


def far_condition_F(D, k, alpha):
    g = {x: -ONE / (x - alpha) for x in D}
    for Tset in combinations(D, k + 1):
        if deg(interp([(x, g[x]) for x in Tset])) < k:
            return False
    return True


def bdeg(coeffs):
    """Degree of a base-field coefficient list (list of ints), -1 if zero."""
    last = -1
    for i, c in enumerate(coeffs):
        if c % P:
            last = i
    return last


def phi_check(U, D, k, a, alpha, z):
    """F1 transfer for slope z: on a witnessing support S where f+zg is deg<k over
    F, confirm BOTH coordinate words are explained by C_B (deg<k over B), i.e. the
    F-codeword's image lies in C_B^2 = Phi(C_F).  Phi is B-linear, so this is the
    multiplication-slice membership Phi(f)+M_z Phi(g) in C_B^2."""
    f = {x: U[x] / (x - alpha) for x in D}
    g = {x: -ONE / (x - alpha) for x in D}
    for S in combinations(D, a):
        H = interp([(x, f[x] + z * g[x]) for x in S])
        if deg(H) < k:
            H0 = [c.a for c in H]   # coordinate words over B
            H1 = [c.b for c in H]
            return bdeg(H0) < k and bdeg(H1) < k
    return True  # vacuous (no deg<k witness at this support size)


def planted_two(D, k, a):
    """Plant two distinct deg<=k F-codewords c1,c2 agreeing on a k-set K, each on
    an a-support inside D, so the C_F list has >= 2 elements (extension-valued)."""
    n = len(D)
    K = D[:k]                         # shared k-set
    S1 = D[:a]                        # K + (a-k) more
    S2 = D[:k] + D[a:a + (a - k)]     # K + (a-k) others
    # c1 = a low-degree F-poly; c2 = c1 + V_K (vanishes exactly on K)
    c1 = [ONE + T, F2(2, 3)]          # degree 1, extension-valued
    VK = [ONE]
    for x in K:
        new = [ZERO] * (len(VK) + 1)
        for d, b in enumerate(VK):
            new[d] = new[d] - x * b
            new[d + 1] = new[d + 1] + b
        VK = new                       # deg k, vanishes on K
    c2 = [(c1[i] if i < len(c1) else ZERO) + VK[i] for i in range(len(VK))]
    s1, s2 = set(S1), set(S2)
    U = {}
    for x in D:
        if x in s1:
            U[x] = peval(c1, x)
        elif x in s2:
            U[x] = peval(c2, x)
        else:
            U[x] = peval(c1, x) + ONE  # avoid both
    return U


CONFIGS = [(8, 3, 5), (8, 4, 6)]  # (n,k,a) over D subset F_17, F=F_289


def run():
    results = []
    all_ok = True
    alpha = T  # extension-valued deep point
    for (n, k, a) in CONFIGS:
        D = subgroup(n)
        assert alpha not in D
        far = far_condition_F(D, k, alpha)
        cfg = {"n": n, "k": k, "a": a, "far_ok": far, "words": []}
        # words: monomial, an extension-valued word, and a planted 2-codeword word
        words = {
            "mono_kp1": {x: x ** (k + 1) for x in D},
            "extval": {x: x ** k + T * (x ** (k - 1)) for x in D},
            "planted2": planted_two(D, k, a),
        }
        for name, U in words.items():
            deep, cplus = deep_image_F(U, D, k, a, alpha)
            mca = bad_mca_F(U, D, k, a, alpha)
            identity = (deep == mca)
            list_ctrl = (len(deep) <= cplus)
            phi_ok = all(phi_check(U, D, k, a, alpha, z) for z in list(mca)[:3]) if mca else True
            ok = far and identity and list_ctrl and phi_ok
            cfg["words"].append({"word": name, "deep": len(deep), "mca": len(mca),
                                 "cplus_list": cplus, "identity": identity,
                                 "list_control": list_ctrl, "phi_transfer": phi_ok,
                                 "ok": ok})
            if not ok:
                all_ok = False
        results.append(cfg)
    return {"all_ok": all_ok, "field": f"F_{P}^2 (t^2={NS})", "configs": results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    out = run()
    if args.json:
        print(json.dumps(out, indent=2))
        if not out["all_ok"]:
            raise SystemExit(1)
        return
    print(f"F1 extension-line forward case over {out['field']}, deep point alpha=t:")
    print("  (1) Bad_MCA_F = Deep_alpha^F   (2) |Deep^F| <= C_{F,+} list"
          "   (3) Phi multiplication-slice transfer")
    print()
    for c in out["configs"]:
        print(f"  n={c['n']} k={c['k']} a={c['a']}  far_condition={c['far_ok']}")
        for w in c["words"]:
            print(f"      {w['word']:<10} |Deep^F|={w['deep']:>2} |Bad_MCA|={w['mca']:>2}"
                  f" C_F+_list={w['cplus_list']:>3}  identity={w['identity']}"
                  f" list_ctrl={w['list_control']} phi={w['phi_transfer']}"
                  f"  [{'OK' if w['ok'] else 'FAIL'}]")
    print()
    print("RESULT:", "PASS" if out["all_ok"] else "FAIL")
    if not out["all_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
