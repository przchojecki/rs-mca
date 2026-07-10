#!/usr/bin/env python3
"""Exact checks for the h=3 char-zero classification.

This script is intentionally local and lightweight.  It verifies the
cyclotomic classification for small orders by exact polynomial reduction modulo
Phi_n, and it checks the banked norm-gate shapes exactly modulo their activating
primes.  No floating point is used.
"""

from __future__ import annotations

import itertools
import math
from functools import lru_cache
from dataclasses import dataclass

import sympy as sp


X = sp.Symbol("X")


def cyclotomic_residue(n: int, terms: list[tuple[int, int]]) -> tuple[int, ...]:
    """Return canonical coefficients of sum c*X^e in Z[X]/Phi_n."""
    phi = sp.Poly(sp.cyclotomic_poly(n, X), X, domain=sp.ZZ)
    poly = sp.Poly(0, X, domain=sp.ZZ)
    for coeff, exp in terms:
        poly += sp.Poly(coeff * X ** (exp % n), X, domain=sp.ZZ)
    rem = poly.rem(phi)
    return tuple(int(rem.nth(i)) for i in range(phi.degree()))


@lru_cache(maxsize=None)
def residue_basis(n: int) -> tuple[tuple[int, ...], ...]:
    """Residues of X^e for e=0..n-1 in Z[X]/Phi_n."""
    return tuple(cyclotomic_residue(n, [(1, e)]) for e in range(n))


def vec_add(*vectors: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(coords) for coords in zip(*vectors))


def vec_sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x - y for x, y in zip(a, b))


def e1_terms(a: tuple[int, ...], b: tuple[int, ...]) -> list[tuple[int, int]]:
    return [(1, x) for x in a] + [(-1, y) for y in b]


def e2_terms(a: tuple[int, ...], b: tuple[int, ...]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for u, v in itertools.combinations(a, 2):
        out.append((1, u + v))
    for u, v in itertools.combinations(b, 2):
        out.append((-1, u + v))
    return out


def is_zero_residue(n: int, terms: list[tuple[int, int]]) -> bool:
    return all(c == 0 for c in cyclotomic_residue(n, terms))


def is_toral_triple(n: int, triple: tuple[int, int, int]) -> bool:
    if n % 3:
        return False
    step = n // 3
    residues = sorted((triple[0] + j * step) % n for j in range(3))
    return sorted(triple) == residues


def primitive_root_mod_prime(p: int, n: int) -> int:
    assert (p - 1) % n == 0
    for cand in range(2, p):
        z = pow(cand, (p - 1) // n, p)
        if z == 1:
            continue
        y = z
        order = 1
        while y != 1:
            y = y * z % p
            order += 1
            if order > n:
                break
        if order == n:
            return z
    raise RuntimeError(f"no primitive {n}-th root found modulo {p}")


def eval_mod_prime(p: int, zeta: int, terms: list[tuple[int, int]]) -> int:
    return sum(coeff * pow(zeta, exp, p) for coeff, exp in terms) % p


@dataclass(frozen=True)
class RowCheck:
    n: int
    char0_trade_pairs: int
    expected_toral_pairs: int


def enumerate_char0_row(n: int) -> RowCheck:
    basis = residue_basis(n)
    buckets: dict[
        tuple[tuple[int, ...], tuple[int, ...]], list[tuple[int, int, int]]
    ] = {}
    for triple in itertools.combinations(range(n), 3):
        e1 = vec_add(*(basis[a] for a in triple))
        e2 = vec_add(
            *(basis[(u + v) % n] for u, v in itertools.combinations(triple, 2))
        )
        buckets.setdefault((e1, e2), []).append(triple)
    found = 0
    expected = math.comb(n // 3, 2) if n % 3 == 0 else 0
    bad: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for members in buckets.values():
        if len(members) < 2:
            continue
        for i, a in enumerate(members):
            aset = set(a)
            for b in members[i + 1 :]:
                if aset & set(b):
                    continue
                found += 1
                if not (is_toral_triple(n, a) and is_toral_triple(n, b)):
                    bad.append((a, b))
    if bad:
        # Double-check any apparent bad row with the slower direct reducer
        # before reporting it as a classification counterexample.
        confirmed_bad = []
        for a, b in bad:
            if set(a) & set(b):
                continue
            if not is_zero_residue(n, e1_terms(a, b)):
                continue
            if not is_zero_residue(n, e2_terms(a, b)):
                continue
            confirmed_bad.append((a, b))
        if confirmed_bad:
            raise AssertionError(
                f"non-toral char-zero h=3 trades at n={n}: {confirmed_bad[:3]}"
            )
    if found != expected:
        raise AssertionError(
            f"toral count mismatch at n={n}: found {found}, expected {expected}"
        )
    return RowCheck(n=n, char0_trade_pairs=found, expected_toral_pairs=expected)


@dataclass(frozen=True)
class NormGateShape:
    n: int
    p: int
    a: tuple[int, int, int]
    b: tuple[int, int, int]


BANKED_NORM_GATE_SHAPES = [
    NormGateShape(96, 9601, (0, 15, 39), (7, 31, 48)),
    NormGateShape(96, 13249, (0, 10, 48), (38, 81, 91)),
    NormGateShape(96, 18433, (0, 3, 82), (35, 54, 79)),
]


def check_norm_gate(shape: NormGateShape) -> dict[str, object]:
    n, p, a, b = shape.n, shape.p, shape.a, shape.b
    e1_zero_char0 = is_zero_residue(n, e1_terms(a, b))
    e2_zero_char0 = is_zero_residue(n, e2_terms(a, b))
    zeta = primitive_root_mod_prime(p, n)
    e1_mod = eval_mod_prime(p, zeta, e1_terms(a, b))
    e2_mod = eval_mod_prime(p, zeta, e2_terms(a, b))
    if e1_zero_char0 or e2_zero_char0:
        raise AssertionError(
            f"expected nonzero char-zero obstructions for {shape}, "
            f"got E1_zero={e1_zero_char0}, E2_zero={e2_zero_char0}"
        )
    if e1_mod != 0 or e2_mod != 0:
        raise AssertionError(
            f"expected activation modulo p for {shape}, got E1={e1_mod}, E2={e2_mod}"
        )
    return {
        "n": n,
        "p": p,
        "shape": [list(a), list(b)],
        "char0_nonzero": [not e1_zero_char0, not e2_zero_char0],
        "mod_p_zero": [e1_mod == 0, e2_mod == 0],
    }


def activation_bound(n: int) -> int:
    return math.floor(sp.totient(n) * math.log(6) / (2 * math.log(n)))


def main() -> None:
    rows = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 21, 24, 30, 36, 48, 96]
    row_checks = [enumerate_char0_row(n) for n in rows]
    gate_checks = [check_norm_gate(s) for s in BANKED_NORM_GATE_SHAPES]

    print("Exact char-zero classification rows:")
    for r in row_checks:
        print(
            f"  n={r.n:2d}: trades={r.char0_trade_pairs}, "
            f"toral_expected={r.expected_toral_pairs}, "
            f"activation_bound={activation_bound(r.n) if r.n > 1 else 0}"
        )
    print("Banked norm-gate shapes:")
    for g in gate_checks:
        print(
            f"  n={g['n']} p={g['p']} shape={g['shape']} "
            f"char0_nonzero={g['char0_nonzero']} mod_p_zero={g['mod_p_zero']}"
        )
    print("CHAR0_CLASSIFICATION_PASS")


if __name__ == "__main__":
    main()
