#!/usr/bin/env python3
"""
Reference calculator for the v10 milestone-3 extension-pole floor.

Given a field size q, base-field size b, dimension k, and list size L, it prints

    N_ext = ceil( L(q-b) / (q-b+kL) )
    E_ext = N_ext/q as an integer numerator lower bound, and
    floor_density = L(q-b)/(q(q-b+kL)) as the analytic lower bound.

The --koalabear-demo mode computes the deployed sextic slack-two fiber values
from p=2^31-2^24+1, q=p^6, k=2^20, N=256, ell=130.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from math import comb, log2


def ceil_div(a: int, b: int) -> int:
    if b <= 0:
        raise ValueError("denominator must be positive")
    return -(-a // b)


def extension_floor(q: int, b: int, k: int, L: int) -> tuple[int, Fraction]:
    if not (0 < b < q):
        raise ValueError("need a proper extension: 0 < b < q")
    if k <= 0 or L <= 0:
        raise ValueError("k and L must be positive")
    m = q - b
    numerator = ceil_div(L * m, m + k * L)
    density = Fraction(L * m, q * (m + k * L))
    return numerator, density


def fmt_bits_fraction(x: Fraction) -> str:
    # Returns approximate log2(x), useful for tiny densities.
    return f"{log2(x.numerator) - log2(x.denominator):.6f}"


def run_values(q: int, b: int, k: int, L: int) -> None:
    N_ext, density = extension_floor(q, b, k, L)
    print(f"q={q}")
    print(f"b={b}")
    print(f"k={k}")
    print(f"L={L}")
    print(f"N_ext=ceil(L(q-b)/(q-b+kL))={N_ext}")
    print(f"log2(N_ext)={log2(N_ext):.6f}")
    print(f"density_fraction={density.numerator}/{density.denominator}")
    print(f"log2(density_floor)={fmt_bits_fraction(density)}")
    print(f"density_floor≈{float(density):.12g}")


def koalabear_demo() -> None:
    p = 2**31 - 2**24 + 1
    q = p**6
    k = 2**20
    binom = comb(256, 130)
    L = ceil_div(binom, p)
    print("KoalaBear sextic slack-two fiber demo")
    print(f"p={p}")
    print(f"log2(q)=6 log2(p)={6*log2(p):.6f}")
    print(f"binom(256,130)={binom}")
    print(f"log2(binom)={log2(binom):.6f}")
    print(f"L=ceil(binom/p)={L}")
    print(f"log2(L)={log2(L):.6f}")
    run_values(q=q, b=p, k=k, L=L)
    threshold = Fraction(1, 2**21)
    _, density = extension_floor(q, p, k, L)
    print(f"density > 2^-21? {density > threshold}")
    near_limit = Fraction(1, k) * Fraction(q - p, q)
    print(f"limit_log2=(1/k)(1-p/q): {fmt_bits_fraction(near_limit)}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--q", type=int, help="extension field size")
    parser.add_argument("--b", type=int, help="base/generated field size")
    parser.add_argument("--k", type=int, help="RS dimension")
    parser.add_argument("--L", type=int, help="certified list size")
    parser.add_argument("--koalabear-demo", action="store_true", help="run deployed KoalaBear sextic demo")
    args = parser.parse_args()

    if args.koalabear_demo:
        koalabear_demo()
        return 0

    missing = [name for name in ("q", "b", "k", "L") if getattr(args, name) is None]
    if missing:
        parser.error("provide --q --b --k --L, or use --koalabear-demo")
    run_values(args.q, args.b, args.k, args.L)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
