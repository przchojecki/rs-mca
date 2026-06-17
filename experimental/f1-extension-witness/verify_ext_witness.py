#!/usr/bin/env python3
"""Standalone verifier for canonical-residue-witness.json.

This script deliberately avoids importing mca-frontier. It rechecks the witness
using only local finite-field arithmetic, Lagrange interpolation, and exhaustive
same-set support enumeration at the toy size n=8.
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT = ROOT / "canonical-residue-witness.json"


class ExtensionField:
    def __init__(self, p: int, modulus: list[int]):
        if len(modulus) < 2:
            raise ValueError("modulus must have degree at least 1")
        if modulus[-1] % p != 1:
            raise ValueError("modulus must be monic")
        self.p = p
        self.modulus = [x % p for x in modulus]
        self.degree = len(modulus) - 1
        self.zero = (0,) * self.degree
        self.one = (1,) + (0,) * (self.degree - 1)
        self.size = p ** self.degree

    def normalize(self, x):
        if isinstance(x, int):
            vals = [x]
        else:
            vals = list(x)
        vals = [(v % self.p) for v in vals[: self.degree]]
        vals += [0] * (self.degree - len(vals))
        return tuple(vals)

    def add(self, a, b):
        a, b = self.normalize(a), self.normalize(b)
        return tuple((a[i] + b[i]) % self.p for i in range(self.degree))

    def sub(self, a, b):
        a, b = self.normalize(a), self.normalize(b)
        return tuple((a[i] - b[i]) % self.p for i in range(self.degree))

    def neg(self, a):
        a = self.normalize(a)
        return tuple((-a[i]) % self.p for i in range(self.degree))

    def mul(self, a, b):
        a, b = self.normalize(a), self.normalize(b)
        coeff = [0] * (2 * self.degree - 1)
        for i, ai in enumerate(a):
            for j, bj in enumerate(b):
                coeff[i + j] = (coeff[i + j] + ai * bj) % self.p
        for deg in range(len(coeff) - 1, self.degree - 1, -1):
            lead = coeff[deg] % self.p
            if lead == 0:
                continue
            offset = deg - self.degree
            for j in range(self.degree):
                coeff[offset + j] = (coeff[offset + j] - lead * self.modulus[j]) % self.p
        return tuple(coeff[: self.degree])

    def pow(self, a, e: int):
        if e < 0:
            return self.pow(self.inv(a), -e)
        out = self.one
        base = self.normalize(a)
        while e:
            if e & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            e >>= 1
        return out

    def inv(self, a):
        a = self.normalize(a)
        if a == self.zero:
            raise ZeroDivisionError("division by zero")
        return self.pow(a, self.size - 2)

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    def is_zero(self, a):
        return self.normalize(a) == self.zero

    def elements(self):
        for coeffs in product(range(self.p), repeat=self.degree):
            yield tuple(coeffs)


def trim(poly: list[tuple[int, ...]], F: ExtensionField):
    out = list(poly)
    while out and F.is_zero(out[-1]):
        out.pop()
    return out


def poly_degree(poly: list[tuple[int, ...]], F: ExtensionField) -> int:
    return len(trim(poly, F)) - 1


def poly_add(a, b, F: ExtensionField):
    n = max(len(a), len(b))
    out = []
    for i in range(n):
        ai = a[i] if i < len(a) else F.zero
        bi = b[i] if i < len(b) else F.zero
        out.append(F.add(ai, bi))
    return trim(out, F)


def poly_mul(a, b, F: ExtensionField):
    if not a or not b:
        return []
    out = [F.zero] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = F.add(out[i + j], F.mul(ai, bj))
    return trim(out, F)


def poly_eval(poly, x, F: ExtensionField):
    acc = F.zero
    for coeff in reversed(poly):
        acc = F.add(F.mul(acc, x), coeff)
    return acc


def interpolate(xs, ys, F: ExtensionField):
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have equal length")
    out = []
    for i, xi in enumerate(xs):
        numer = [F.one]
        denom = F.one
        for j, xj in enumerate(xs):
            if i == j:
                continue
            numer = poly_mul(numer, [F.neg(xj), F.one], F)
            denom = F.mul(denom, F.sub(xi, xj))
        scale = F.div(ys[i], denom)
        term = [F.mul(c, scale) for c in numer]
        out = poly_add(out, term, F)
    return trim(out, F)


def is_base(F: ExtensionField, z) -> bool:
    z = F.normalize(z)
    return all(c == 0 for c in z[1:])


def verify(path: Path) -> None:
    w = json.loads(path.read_text())
    p = int(w["B"].split("_")[1])
    F = ExtensionField(p, w["modulus"])
    domain = [F.normalize(x) for x in w["domain"]]
    f = [F.normalize(x) for x in w["f"]]
    g = [F.normalize(x) for x in w["g"]]
    zstar = F.normalize(w["bad_slope_zstar"])
    S = list(w["agreement_set_S"])
    c = [F.normalize(x) for x in w["codeword_c_coeffs"]]
    n, k, errors = len(domain), int(w["k"]), int(w["errors"])

    def agrees(word, A) -> bool:
        coeffs = interpolate([domain[i] for i in A], [word[i] for i in A], F)
        return poly_degree(coeffs, F) < k

    h = [F.add(f[i], F.mul(zstar, g[i])) for i in range(n)]
    checks = {
        "zstar_in_F_minus_B": not is_base(F, zstar),
        "agreement_set_big_enough": len(S) >= n - errors,
        "codeword_is_low_degree": poly_degree(c, F) < k,
        "combination_matches_codeword_on_S": all(h[i] == poly_eval(c, domain[i], F) for i in S),
        "f_on_S_not_codeword": not agrees(f, S),
        "g_on_S_not_codeword": not agrees(g, S),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise SystemExit(f"FAIL canonical witness: {failed}")
    print("OK canonical witness")

    def same_set_failure(z) -> bool:
        hz = [F.add(f[i], F.mul(z, g[i])) for i in range(n)]
        for size in range(n, n - errors - 1, -1):
            for A in combinations(range(n), size):
                if agrees(hz, A) and not (agrees(f, A) and agrees(g, A)):
                    return True
        return False

    recount = sum(1 for z in F.elements() if not is_base(F, z) and same_set_failure(z))
    expected = int(w["num_F_bad_slopes"])
    if recount != expected:
        raise SystemExit(f"FAIL F\\B bad-slope recount: got {recount}, expected {expected}")
    print(f"OK F\\B bad-slope recount: {recount}")


def main() -> int:
    verify(DEFAULT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
