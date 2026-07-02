#!/usr/bin/env python3
"""FM1 exact aperiodic first moment verifier.

This script supports the note
  experimental/notes/m1/fm1_exact_aperiodic_first_moment.md

It checks the two finite pieces behind the general proof:

1. For every split locator on the F_13 toy row (n=12,k=3,A=8),
   the locator-syndrome map has full rank t=A-k=5.
2. For every ordered pair of F_13 split locators, the joint rank is
   2t - max(0,t-j+|R cap T|).
3. On the tiny F_5 row (n=4,k=1,A=3), brute-force enumeration over all
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
import math
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


def joint_alignment_probability(q: int, t: int, h: int) -> Fraction:
    """Probability that both locators align in the standard defect-h fiber product."""
    assert 0 <= h <= t
    favorable = (
        q * (q ** h - 1) * q ** (2 * (t - h))
        + q ** 2 * (q ** (t - h) - 1) ** 2
    )
    total = q ** (2 * (2 * t - h))
    return Fraction(favorable, total)


def second_moment_formula(q: int, n: int, k: int, agreement: int) -> Fraction:
    t = agreement - k
    j = n - agreement
    total = Fraction(0, 1)
    for c in range(j + 1):
        if j - c > n - j:
            continue
        ordered_pairs = comb(n, j) * comb(j, c) * comb(n - j, j - c)
        h = max(0, t - j + c)
        total += ordered_pairs * joint_alignment_probability(q, t, h)
    return total


def standard_fiber_product(q: int, t: int, h: int) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    assert 0 <= h <= t
    commons = list(itertools.product(range(q), repeat=h))
    tails = list(itertools.product(range(q), repeat=t - h))
    return [
        (common + left, common + right)
        for common in commons
        for left in tails
        for right in tails
    ]


def log2_comb(n: int, r: int) -> float:
    return (math.lgamma(n + 1) - math.lgamma(r + 1) - math.lgamma(n - r + 1)) / math.log(2)


def fm1_log2_upper(q: int, n: int, k: int, agreement: int) -> float:
    """Upper log2 of FM1 expectation, dropping the factor (1-q^-t)<1."""
    t = agreement - k
    j = n - agreement
    return log2_comb(n, j) + (1 - t) * math.log2(q)


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


def check_f13_joint_rank_formula() -> tuple[bool, dict]:
    p, n, k, agreement = 13, 12, 3, 8
    t, j = agreement - k, n - agreement
    domain = list(range(1, p))
    locators = list(itertools.combinations(domain, j))
    matrices = {
        roots: syndrome_matrix(domain, roots, t, p)
        for roots in locators
    }
    rank_by_overlap: dict[int, dict[int, int]] = {}
    bad = []
    for roots_r in locators:
        set_r = set(roots_r)
        matrix_r = matrices[roots_r]
        for roots_t in locators:
            c = len(set_r.intersection(roots_t))
            expected_defect = max(0, t - j + c)
            expected_rank = 2 * t - expected_defect
            rank = rank_mod_p(matrix_r + matrices[roots_t], p)
            rank_by_overlap.setdefault(c, {})
            rank_by_overlap[c][rank] = rank_by_overlap[c].get(rank, 0) + 1
            if rank != expected_rank:
                bad.append({
                    "R": roots_r,
                    "T": roots_t,
                    "overlap": c,
                    "rank": rank,
                    "expected_rank": expected_rank,
                })
                if len(bad) >= 5:
                    break
        if len(bad) >= 5:
            break
    expected_hist = {}
    for c in range(j + 1):
        count_t = comb(j, c) * comb(n - j, j - c)
        if count_t:
            rank = 2 * t - max(0, t - j + c)
            expected_hist[c] = {rank: len(locators) * count_t}
    data = {
        "field": f"F_{p}",
        "n": n,
        "k": k,
        "agreement": agreement,
        "t": t,
        "j": j,
        "locator_count": len(locators),
        "ordered_pair_count": len(locators) ** 2,
        "rank_by_overlap": rank_by_overlap,
        "expected_rank_by_overlap": expected_hist,
        "bad_pairs": bad,
        "formula": "rank = 2t - max(0,t-j+|R cap T|)",
    }
    return not bad and rank_by_overlap == expected_hist, data


def check_fiber_product_joint_probability() -> tuple[bool, dict]:
    q, t = 5, 2
    checks = []
    ok = True
    for h in range(t + 1):
        elements = standard_fiber_product(q, t, h)
        favorable = 0
        for a_r, a_t in elements:
            for b_r, b_t in elements:
                if in_span(a_r, b_r, q) and in_span(a_t, b_t, q):
                    favorable += 1
        brute = Fraction(favorable, len(elements) ** 2)
        formula = joint_alignment_probability(q, t, h)
        checks.append({
            "h": h,
            "fiber_product_size": len(elements),
            "favorable_pairs": favorable,
            "bruteforce_probability": {
                "numerator": brute.numerator,
                "denominator": brute.denominator,
                "decimal": float(brute),
            },
            "formula_probability": {
                "numerator": formula.numerator,
                "denominator": formula.denominator,
                "decimal": float(formula),
            },
        })
        ok &= brute == formula
    return ok, {
        "field": f"F_{q}",
        "t": t,
        "checked_defects": checks,
        "formula": (
            "P_h = [q(q^h-1)q^(2(t-h)) + q^2(q^(t-h)-1)^2] / q^(4t-2h)"
        ),
    }


def check_f5_bruteforce() -> tuple[bool, dict]:
    p, n, k, agreement = 5, 4, 1, 3
    t, j = agreement - k, n - agreement
    domain = list(range(1, p))
    locators = list(itertools.combinations(domain, j))
    matrices = [syndrome_matrix(domain, roots, t, p) for roots in locators]
    words = list(itertools.product(range(p), repeat=n))
    total_aligned = 0
    total_aligned_square = 0
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
            total_aligned_square += count * count
            aligned_hist[count] = aligned_hist.get(count, 0) + 1
    total_pairs = p ** (2 * n)
    mean = Fraction(total_aligned, total_pairs)
    expected = expected_value(p, n, k, agreement)
    second_moment = Fraction(total_aligned_square, total_pairs)
    expected_second_moment = second_moment_formula(p, n, k, agreement)
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
        "total_aligned_locator_square_sum": total_aligned_square,
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
        "bruteforce_second_moment": {
            "numerator": second_moment.numerator,
            "denominator": second_moment.denominator,
            "decimal": float(second_moment),
        },
        "formula_second_moment": {
            "numerator": expected_second_moment.numerator,
            "denominator": expected_second_moment.denominator,
            "decimal": float(expected_second_moment),
        },
    }
    return (
        mean == expected
        and second_moment == expected_second_moment
        and rank_hist == {t: len(locators)}
    ), data


def check_f17_regular_window_tail() -> tuple[bool, dict]:
    """FM1/Markov consumer scale for the F_17^32 regular M3 window.

    This is not a worst-case theorem.  It records that a random pair has
    astronomically small probability of even one aligned split locator in the
    385..426 window, so any worst-case mass must be structured.
    """
    q, n, k = 17 ** 32, 512, 256
    rows = []
    ok = True
    for agreement in range(385, 427):
        t = agreement - k
        j = n - agreement
        upper = fm1_log2_upper(q, n, k, agreement)
        rows.append({
            "agreement": agreement,
            "t": t,
            "j": j,
            "log2_fm1_expectation_upper": upper,
            "markov_probability_at_least_one_upper_log2": upper,
        })
        ok &= upper < -16_000
    endpoints = {row["agreement"]: row for row in rows if row["agreement"] in {385, 426}}
    ok &= -16_340 < endpoints[385]["log2_fm1_expectation_upper"] < -16_320
    ok &= -21_790 < endpoints[426]["log2_fm1_expectation_upper"] < -21_760
    data = {
        "field": "F_17^32",
        "q": q,
        "n": n,
        "k": k,
        "agreement_range": [385, 426],
        "row_count": len(rows),
        "max_log2_fm1_expectation_upper": max(row["log2_fm1_expectation_upper"] for row in rows),
        "min_log2_fm1_expectation_upper": min(row["log2_fm1_expectation_upper"] for row in rows),
        "endpoint_rows": endpoints,
        "all_markov_one_locator_bounds_below_2^-16000": all(
            row["markov_probability_at_least_one_upper_log2"] < -16_000 for row in rows
        ),
        "interpretation": (
            "By Markov, a random word-pair has probability at most the FM1 "
            "expectation of containing any aligned split locator. This does not "
            "bound worst-case pairs."
        ),
    }
    return ok, data


def build_report() -> dict:
    ok_f13, f13 = check_f13_surjectivity()
    ok_joint, joint = check_f13_joint_rank_formula()
    ok_fiber, fiber = check_fiber_product_joint_probability()
    ok_f5, f5 = check_f5_bruteforce()
    ok_window, window = check_f17_regular_window_tail()
    source = Path(__file__).read_text()
    return {
        "schema": "fm1_exact_first_moment_v1",
        "status": "PROVED_LOCAL_VERIFICATION",
        "dag_node": "fm1",
        "statement": "E[# aligned split locators] = binom(n,j)(1-q^-t)q^(1-t)",
        "second_moment_statement": (
            "E[N_A^2] is the ordered-overlap sum of the exact defect-h joint "
            "alignment probabilities."
        ),
        "definition": (
            "For a split degree-j locator ell, set a=S_ell(u), b=S_ell(v) in F_q^t. "
            "The locator is aligned when b != 0 and a lies in the one-dimensional span of b."
        ),
        "checks": {
            "f13_surjectivity": f13,
            "f13_joint_rank_formula": joint,
            "f5_fiber_product_joint_probability": fiber,
            "f5_bruteforce": f5,
            "f17_regular_window_markov_tail": window,
        },
        "passed": ok_f13 and ok_joint and ok_fiber and ok_f5 and ok_window,
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
        if name == "f13_surjectivity":
            print(
                "        {field}: n={n}, k={k}, A={agreement}, t={t}, j={j}, "
                "locators={locator_count}, ranks={rank_histogram}".format(**data)
            )
            ev = data["expected_aligned_locators"]
            print(f"        formula expectation = {ev['numerator']}/{ev['denominator']} = {ev['decimal']:.12f}")
        elif name == "f13_joint_rank_formula":
            print(
                "        {field}: ordered pairs={ordered_pair_count}, "
                "rank_by_overlap={rank_by_overlap}".format(**data)
            )
        elif name == "f5_fiber_product_joint_probability":
            summary = {
                row["h"]: (
                    row["formula_probability"]["numerator"],
                    row["formula_probability"]["denominator"],
                )
                for row in data["checked_defects"]
            }
            print(f"        {data['field']}: t={data['t']}, probabilities by h={summary}")
        elif name == "f5_bruteforce":
            print(
                "        {field}: n={n}, k={k}, A={agreement}, t={t}, j={j}, "
                "locators={locator_count}, ranks={rank_histogram}".format(**data)
            )
            bf = data["bruteforce_mean"]
            fm = data["formula_mean"]
            print(f"        brute mean = {bf['numerator']}/{bf['denominator']} = {bf['decimal']:.12f}")
            print(f"        formula    = {fm['numerator']}/{fm['denominator']} = {fm['decimal']:.12f}")
            bs = data["bruteforce_second_moment"]
            fs = data["formula_second_moment"]
            print(
                f"        brute second moment = {bs['numerator']}/{bs['denominator']} = "
                f"{bs['decimal']:.12f}"
            )
            print(
                f"        formula second moment = {fs['numerator']}/{fs['denominator']} = "
                f"{fs['decimal']:.12f}"
            )
            print(f"        total aligned locators over all word pairs = {data['total_aligned_locators']}")
        elif name == "f17_regular_window_markov_tail":
            e385 = data["endpoint_rows"][385]["log2_fm1_expectation_upper"]
            e426 = data["endpoint_rows"][426]["log2_fm1_expectation_upper"]
            print(f"        A=385 log2 expectation upper = {e385:.1f}")
            print(f"        A=426 log2 expectation upper = {e426:.1f}")
            print(
                "        all A in 385..426 have Markov one-locator probability "
                f"< 2^-16000: {data['all_markov_one_locator_bounds_below_2^-16000']}"
            )
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not report["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
