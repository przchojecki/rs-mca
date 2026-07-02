#!/usr/bin/env python3
"""FM1 exact aperiodic first moment verifier.

This script supports the note
  experimental/notes/m1/fm1_exact_aperiodic_first_moment.md

It checks the two finite pieces behind the general proof:

1. For every split locator on the F_13 toy row (n=12,k=3,A=8),
   the locator-syndrome map has full rank t=A-k=5.
2. On the tiny F_5 row (n=4,k=1,A=3), brute-force enumeration over all
   word pairs agrees exactly with

       binom(n,j) * (1 - q^-t) * q^(1-t).

Run:
  python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py
  python3 experimental/scripts/verify_fm1_exact_aperiodic_first_moment.py --emit
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from math import comb
from pathlib import Path


OUTPUT = Path("experimental/data/certificates/fm1-exact-first-moment/fm1_exact_first_moment.json")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rank_mod_p(matrix: list[list[int]], p: int) -> int:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    m = [[x % p for x in row] for row in matrix]
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if m[i][c] % p), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        inv = pow(m[r][c], -1, p)
        m[r] = [(x * inv) % p for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(x - f * y) % p for x, y in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


def poly_mul_mod_p(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def locator_poly(roots: tuple[int, ...], p: int) -> list[int]:
    poly = [1]
    for r in roots:
        poly = poly_mul_mod_p(poly, [(-r) % p, 1], p)
    return poly


def eval_poly(poly: list[int], x: int, p: int) -> int:
    value = 0
    power = 1
    for coeff in poly:
        value = (value + coeff * power) % p
        power = (power * x) % p
    return value


def syndrome_matrix(domain: list[int], roots: tuple[int, ...], t: int, p: int) -> list[list[int]]:
    ell = locator_poly(roots, p)
    rows = []
    for m in range(1, t + 1):
        rows.append([(eval_poly(ell, x, p) * pow(x, m, p)) % p for x in domain])
    return rows


def syndrome_vector(word: tuple[int, ...], matrix: list[list[int]], p: int) -> tuple[int, ...]:
    return tuple(sum(row[i] * word[i] for i in range(len(word))) % p for row in matrix)


def in_span(a: tuple[int, ...], b: tuple[int, ...], p: int) -> bool:
    if all(x == 0 for x in b):
        return False
    scalar = None
    for ai, bi in zip(a, b):
        if bi:
            s = ai * pow(bi, -1, p) % p
            if scalar is None:
                scalar = s
            elif scalar != s:
                return False
        elif ai:
            return False
    return True


def expected_value(q: int, n: int, k: int, agreement: int) -> Fraction:
    t = agreement - k
    j = n - agreement
    return Fraction(comb(n, j) * (q ** t - 1) * q, q ** (2 * t))


def check_f13_surjectivity() -> tuple[bool, dict]:
    p, n, k, agreement = 13, 12, 3, 8
    t, j = agreement - k, n - agreement
    domain = list(range(1, p))
    hist = {}
    bad = []
    for roots in itertools.combinations(domain, j):
        rank = rank_mod_p(syndrome_matrix(domain, roots, t, p), p)
        hist[rank] = hist.get(rank, 0) + 1
        if rank != t:
            bad.append(roots)
    formula = expected_value(p, n, k, agreement)
    data = {
        "field": f"F_{p}",
        "n": n,
        "k": k,
        "agreement": agreement,
        "t": t,
        "j": j,
        "locator_count": comb(n, j),
        "rank_histogram": hist,
        "all_syndrome_maps_surjective": not bad,
        "bad_rank_roots": bad[:5],
        "expected_aligned_locators": {
            "numerator": formula.numerator,
            "denominator": formula.denominator,
            "decimal": float(formula),
        },
    }
    return not bad and hist == {t: comb(n, j)}, data


def check_f5_bruteforce() -> tuple[bool, dict]:
    p, n, k, agreement = 5, 4, 1, 3
    t, j = agreement - k, n - agreement
    domain = list(range(1, p))
    locators = list(itertools.combinations(domain, j))
    matrices = [syndrome_matrix(domain, roots, t, p) for roots in locators]
    words = list(itertools.product(range(p), repeat=n))
    total_aligned = 0
    aligned_hist = {}
    for u in words:
        au = [syndrome_vector(u, matrix, p) for matrix in matrices]
        for v in words:
            count = 0
            for a, matrix in zip(au, matrices):
                b = syndrome_vector(v, matrix, p)
                if in_span(a, b, p):
                    count += 1
            total_aligned += count
            aligned_hist[count] = aligned_hist.get(count, 0) + 1
    total_pairs = p ** (2 * n)
    mean = Fraction(total_aligned, total_pairs)
    expected = expected_value(p, n, k, agreement)
    rank_hist = {}
    for matrix in matrices:
        rank = rank_mod_p(matrix, p)
        rank_hist[rank] = rank_hist.get(rank, 0) + 1
    data = {
        "field": f"F_{p}",
        "n": n,
        "k": k,
        "agreement": agreement,
        "t": t,
        "j": j,
        "locator_count": len(locators),
        "word_count": len(words),
        "pair_count": total_pairs,
        "total_aligned_locators": total_aligned,
        "rank_histogram": rank_hist,
        "aligned_locator_count_histogram": aligned_hist,
        "bruteforce_mean": {
            "numerator": mean.numerator,
            "denominator": mean.denominator,
            "decimal": float(mean),
        },
        "formula_mean": {
            "numerator": expected.numerator,
            "denominator": expected.denominator,
            "decimal": float(expected),
        },
    }
    return mean == expected and rank_hist == {t: len(locators)}, data


def build_report() -> dict:
    ok_f13, f13 = check_f13_surjectivity()
    ok_f5, f5 = check_f5_bruteforce()
    source = Path(__file__).read_text()
    return {
        "schema": "fm1_exact_first_moment_v1",
        "status": "PROVED_LOCAL_VERIFICATION",
        "dag_node": "fm1",
        "statement": "E[# aligned split locators] = binom(n,j)(1-q^-t)q^(1-t)",
        "definition": (
            "For a split degree-j locator ell, set a=S_ell(u), b=S_ell(v) in F_q^t. "
            "The locator is aligned when b != 0 and a lies in the one-dimensional span of b."
        ),
        "checks": {
            "f13_surjectivity": f13,
            "f5_bruteforce": f5,
        },
        "passed": ok_f13 and ok_f5,
        "script_sha256": sha256_text(source),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    report = build_report()
    print("=" * 74)
    print("FM1 exact aperiodic first moment")
    print("=" * 74)
    for name, data in report["checks"].items():
        print(f"\n[{'PASS' if report['passed'] else 'CHECK'}] {name}")
        print(
            "        {field}: n={n}, k={k}, A={agreement}, t={t}, j={j}, "
            "locators={locator_count}, ranks={rank_histogram}".format(**data)
        )
        if name == "f13_surjectivity":
            ev = data["expected_aligned_locators"]
            print(f"        formula expectation = {ev['numerator']}/{ev['denominator']} = {ev['decimal']:.12f}")
        else:
            bf = data["bruteforce_mean"]
            fm = data["formula_mean"]
            print(f"        brute mean = {bf['numerator']}/{bf['denominator']} = {bf['decimal']:.12f}")
            print(f"        formula    = {fm['numerator']}/{fm['denominator']} = {fm['decimal']:.12f}")
            print(f"        total aligned locators over all word pairs = {data['total_aligned_locators']}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
