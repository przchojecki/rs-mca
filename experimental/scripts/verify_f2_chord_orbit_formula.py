#!/usr/bin/env python3
"""Replay checks for the F2 chord-orbit formula."""

from __future__ import annotations

import cmath
from math import sqrt


def prime_factors(n: int) -> set[int]:
    out: set[int] = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def primitive_root(q: int) -> int:
    factors = prime_factors(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // r, q) != 1 for r in factors):
            return g
    raise ValueError(f"no primitive root found for {q}")


def verify_row(q: int, n: int) -> dict[str, object]:
    assert (q - 1) % n == 0
    m = (q - 1) // n
    g = primitive_root(q)

    dlog: dict[int, int] = {}
    value = 1
    for i in range(q - 1):
        dlog[value] = i
        value = (value * g) % q

    H = {x for x, exponent in dlog.items() if exponent % m == 0}
    assert len(H) == n

    direct = [0] * q
    for x in H:
        for y in H:
            direct[(x + y) % q] += 1

    for c in range(1, q):
        for h in H:
            assert direct[(c * h) % q] == direct[c], (q, n, c, h)

    angle = 2j * cmath.pi / (q - 1)

    def chi(k: int, x: int) -> complex:
        return cmath.exp(angle * n * k * dlog[x])

    jacobi: dict[tuple[int, int], complex] = {}
    root_q = sqrt(q)
    for k1 in range(m):
        for k2 in range(m):
            total = 0j
            for s in range(2, q):
                total += chi(k1, s) * chi(k2, (1 - s) % q)
            jacobi[(k1, k2)] = total
            if k1 and k2 and (k1 + k2) % m:
                assert abs(abs(total) - root_q) < 1e-6, (q, n, k1, k2, total)

    delta = 1 if q - 1 in H else 0
    inv2 = pow(2, q - 2, q)
    max_err = 0.0
    kappas: dict[int, int] = {}
    bound = (q + 1 + (m - 1) * (m - 2) * root_q) / (2 * m * m) + 0.5

    for orbit in range(m):
        c = pow(g, orbit, q)
        error_term = 0j
        for k1 in range(1, m):
            for k2 in range(1, m):
                if (k1 + k2) % m == 0:
                    continue
                error_term += chi(k1, c) * chi(k2, c) * jacobi[(k1, k2)]

        in_H = 1 if c in H else 0
        formula = (q + 1 - 2 * m * in_H - m * delta + error_term) / (m * m)
        assert abs(formula.imag) < 1e-6, (q, n, orbit, formula)
        err = abs(formula.real - direct[c])
        assert err < 1e-6, (q, n, orbit, formula, direct[c])
        max_err = max(max_err, err)

        diagonal = 1 if (c * inv2) % q in H else 0
        assert (direct[c] - diagonal) % 2 == 0
        kappa = (direct[c] - diagonal) // 2
        direct_kappa = 0
        ordered = sorted(H)
        for i, x in enumerate(ordered):
            for y in ordered[i + 1 :]:
                if (x + y) % q == c:
                    direct_kappa += 1
        assert direct_kappa == kappa, (q, n, orbit, direct_kappa, kappa)
        if not in_H:
            assert kappa <= bound + 1e-9, (q, n, orbit, kappa, bound)
        kappas[orbit] = kappa

    return {
        "q": q,
        "n": n,
        "m": m,
        "delta": delta,
        "max_err": max_err,
        "bound": round(bound, 6),
        "kappas": kappas,
    }


def main() -> None:
    rows = [(17, 16), (97, 16), (97, 32), (193, 32), (193, 64), (257, 64)]
    for q, n in rows:
        row = verify_row(q, n)
        print(
            f"q={q} n={n} m={row['m']} delta={row['delta']} "
            f"max_err={row['max_err']:.2e} kappa_bound={row['bound']} "
            f"orbit_kappas={row['kappas']}"
        )
    print("F2_CHORD_ORBIT_FORMULA_PASS")


if __name__ == "__main__":
    main()
