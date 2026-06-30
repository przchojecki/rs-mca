#!/usr/bin/env python3
"""
verify_m1_beta2_p73_resolution.py

Exact certificate resolving the "p=73 anomalous node" in the M1 (BETA_2)
tame-fiber gate (note: experimental/notes/m1/m1_beta2_obstruction_floor.md).

The reduced degree-13 dihedral singular support of the beta-line pushforward
F_psi factors, in the inversion coordinate z = b + 1/b, as

    (z - 2)(z + 1)(9z + 14)(9z^2 - 6z - 23) * Q8(z).

The full-force gate computation (workflow wqrf9u807) found that the ONLY curve
nodes of the family sit at z = 2 (excised triple point), z = -1 (excised node),
and z = -14/9 (the 9z+14 unipotent transvection); the conic 9z^2-6z-23 and the
octic Q8 fibers are never nodes. A spurious "good node on a conic fiber" can
therefore occur only when a conic root coincides mod p with the 9z+14 node
z = -14/9, i.e. when p divides Res_z(9z+14, 9z^2-6z-23).

This script computes that resultant exactly over Z (and the conic-contamination
of the other two linear factors), then confirms by direct mod-p root-sharing
that p = 73 (besides the bad characteristic p = 3) is the UNIQUE prime of
coincidence. Hence the probe's p=73 "anomaly" is the 9z+14 transvection, NOT a
genuine conic degeneration.

Pure Python stdlib; exact integer/rational arithmetic; no network.
Status: AUDIT (exact finite certificate).
Usage: `python3 verify_m1_beta2_p73_resolution.py` (verbose)
       `python3 verify_m1_beta2_p73_resolution.py --check` (terse; exit 1 on failure)
"""

import sys
from fractions import Fraction

# Singular-support factors in z (coefficients high -> low degree).
NODE = (9, 14)        # 9z + 14, the interior transvection node z = -14/9
CONIC = (9, -6, -23)  # 9z^2 - 6z - 23
ZM2 = (1, -2)         # z - 2   (excised triple point)
ZP1 = (1, 1)          # z + 1   (excised node)


def _eval(coeffs, x):
    r = Fraction(0)
    for c in coeffs:
        r = r * x + c
    return r


def res_linear(lin, g):
    """Res_z(a*z + b, g) = a^deg(g) * g(-b/a), exact (an integer here)."""
    a, b = lin
    val = _eval(g, Fraction(-b, a)) * Fraction(a) ** (len(g) - 1)
    assert val.denominator == 1, "resultant should be an integer"
    return val.numerator


def factor(n):
    n = abs(n)
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def fmt_factor(n):
    f = factor(n)
    if not f:
        return str(n)
    body = " * ".join(f"{p}^{e}" if e > 1 else f"{p}" for p, e in sorted(f.items()))
    return ("-" if n < 0 else "") + body


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def conic_meets_node_mod_p(p):
    """True iff the conic and 9z+14 share a root in F_p (p != 3 so 9 is invertible)."""
    inv9 = pow(9, p - 2, p)
    z0 = (-14 * inv9) % p             # the node root z = -14/9 mod p
    return (9 * z0 * z0 - 6 * z0 - 23) % p == 0


def main(check=False):
    ok = True

    def line(s=""):
        if not check:
            print(s)

    R_node = res_linear(NODE, CONIC)
    R_zm2 = res_linear(ZM2, CONIC)
    R_zp1 = res_linear(ZP1, CONIC)

    line("M1 (BETA_2) p=73 resolution -- exact resultant certificate")
    line("")
    line(f"Res_z(9z+14, 9z^2-6z-23) = {R_node} = {fmt_factor(R_node)}")
    line(f"Res_z(z-2,   9z^2-6z-23) = {R_zm2} = {fmt_factor(R_zm2)}")
    line(f"Res_z(z+1,   9z^2-6z-23) = {R_zp1} = {fmt_factor(R_zp1)}")
    line("")

    ok &= (R_node == 657 and factor(R_node) == {3: 2, 73: 1})
    ok &= (R_zm2 == 1)
    ok &= (abs(R_zp1) == 8 and factor(R_zp1) == {2: 3})

    primes_gt3 = sorted(p for p in factor(R_node) if p > 3)
    line(f"Primes > 3 dividing Res(9z+14, conic): {primes_gt3}   (expect [73])")
    ok &= (primes_gt3 == [73])

    coincide = [p for p in range(5, 400) if is_prime(p) and conic_meets_node_mod_p(p)]
    line(f"Primes 5..400 where the conic and 9z+14 share a root mod p: {coincide}   (expect [73])")
    ok &= (coincide == [73])
    line("")
    line("=> p=73 is the UNIQUE prime > 3 at which a conic root meets the 9z+14")
    line("   transvection node, so the gate's 'anomalous good node on the conic at")
    line("   p=73' is that transvection -- not a conic degeneration.")
    line("")
    line(f"RESULT: {'PASS' if ok else 'FAIL'}")

    if check:
        print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(check="--check" in sys.argv))
