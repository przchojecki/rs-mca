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


def overlap_decomposition(q: int, n: int, k: int, agreement: int) -> dict:
    t = agreement - k
    j = n - agreement
    independent_pair_probability = joint_alignment_probability(q, t, 0)
    locator_count = comb(n, j)
    mean = expected_value(q, n, k, agreement)
    baseline = locator_count * locator_count * independent_pair_probability
    records = []
    correction = Fraction(0, 1)
    for c in range(j + 1):
        if j - c > n - j:
            continue
        ordered_pairs = comb(n, j) * comb(j, c) * comb(n - j, j - c)
        h = max(0, t - j + c)
        probability = joint_alignment_probability(q, t, h)
        excess = probability - independent_pair_probability
        contribution = ordered_pairs * excess
        correction += contribution
        records.append({
            "overlap": c,
            "defect_h": h,
            "ordered_pairs": ordered_pairs,
            "probability": {
                "numerator": probability.numerator,
                "denominator": probability.denominator,
            },
            "excess_over_independent": {
                "numerator": excess.numerator,
                "denominator": excess.denominator,
            },
            "excess_contribution": {
                "numerator": contribution.numerator,
                "denominator": contribution.denominator,
            },
        })
    second = second_moment_formula(q, n, k, agreement)
    variance = second - mean * mean
    relative_variance = variance / (mean * mean) if mean else Fraction(0, 1)
    chebyshev_zero_upper_bound = relative_variance
    chebyshev_half_mean_upper_bound = 4 * relative_variance
    return {
        "q": q,
        "n": n,
        "k": k,
        "agreement": agreement,
        "t": t,
        "j": j,
        "locator_count": locator_count,
        "defect_positive_overlap_threshold": j - t + 1,
        "mean": {
            "numerator": mean.numerator,
            "denominator": mean.denominator,
        },
        "baseline_independent_second_moment": {
            "numerator": baseline.numerator,
            "denominator": baseline.denominator,
        },
        "correction": {
            "numerator": correction.numerator,
            "denominator": correction.denominator,
        },
        "second_moment": {
            "numerator": second.numerator,
            "denominator": second.denominator,
        },
        "variance": {
            "numerator": variance.numerator,
            "denominator": variance.denominator,
        },
        "relative_variance": {
            "numerator": relative_variance.numerator,
            "denominator": relative_variance.denominator,
            "decimal": float(relative_variance),
        },
        "chebyshev_zero_probability_upper_bound": {
            "numerator": chebyshev_zero_upper_bound.numerator,
            "denominator": chebyshev_zero_upper_bound.denominator,
            "decimal": float(chebyshev_zero_upper_bound),
        },
        "chebyshev_half_mean_deviation_upper_bound": {
            "numerator": chebyshev_half_mean_upper_bound.numerator,
            "denominator": chebyshev_half_mean_upper_bound.denominator,
            "decimal": float(chebyshev_half_mean_upper_bound),
        },
        "records": records,
    }


def integer_record(value: int) -> dict:
    return {
        "value": value,
        "log2": math.log2(value) if value > 0 else None,
    }


def fraction_record(value: Fraction) -> dict:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": float(value),
        "log2": math.log2(float(value)) if value > 0 else None,
    }


def dependency_neighborhood(n: int, j: int, t: int) -> dict:
    """Johnson-distance dependency graph induced by the joint-rank formula."""
    locator_count = comb(n, j)
    max_distance = min(j, n - j)
    distance_counts = [
        comb(j, distance) * comb(n - j, distance)
        for distance in range(max_distance + 1)
    ]
    assert sum(distance_counts) == locator_count
    dependent_radius = min(t - 1, max_distance)
    dependent_including_self = sum(distance_counts[:dependent_radius + 1])
    dependent_excluding_self = dependent_including_self - 1
    independent_neighbors = locator_count - dependent_including_self
    rows = []
    if max_distance <= 12:
        for distance, count in enumerate(distance_counts):
            rows.append({
                "johnson_distance": distance,
                "overlap": j - distance,
                "neighbor_count": count,
                "defect_h": max(0, t - distance),
                "pairwise_independent_at_this_distance": distance >= t,
            })
    return {
        "n": n,
        "j": j,
        "t": t,
        "locator_count": integer_record(locator_count),
        "max_johnson_distance": max_distance,
        "dependent_radius": dependent_radius,
        "dependent_neighbors_including_self": integer_record(dependent_including_self),
        "dependent_degree_excluding_self": integer_record(dependent_excluding_self),
        "independent_neighbors": integer_record(independent_neighbors),
        "distance_table": rows,
        "formula": "degree = sum_{d=1}^{min(t-1,j,n-j)} binom(j,d)binom(n-j,d)",
    }


def check_dependency_graph_consumer() -> tuple[bool, dict]:
    examples = [
        dependency_neighborhood(12, 4, 2),
        dependency_neighborhood(64, 24, 4),
        dependency_neighborhood(512, 127, 129),
        dependency_neighborhood(512, 247, 9),
    ]
    ok = True
    for example in examples:
        n, j, t = example["n"], example["j"], example["t"]
        max_distance = example["max_johnson_distance"]
        expected_radius = min(t - 1, max_distance)
        ok &= example["dependent_radius"] == expected_radius
        if t == 1:
            ok &= example["dependent_degree_excluding_self"]["value"] == 0
        if t > max_distance:
            ok &= example["independent_neighbors"]["value"] == 0
        if example["distance_table"]:
            ok &= all(
                row["defect_h"] == max(0, t - row["johnson_distance"])
                for row in example["distance_table"]
            )
            ok &= all(
                row["pairwise_independent_at_this_distance"]
                == (row["johnson_distance"] >= t)
                for row in example["distance_table"]
            )
    return ok, {
        "statement": (
            "Locator indicators for R,T are pairwise independent whenever "
            "Johnson distance d(R,T) >= t; all covariance is supported in "
            "the radius-(t-1) Johnson ball."
        ),
        "examples": examples,
    }


def check_dependency_degree_concentration() -> tuple[bool, dict]:
    rows = []
    ok = True
    for q, n, k, agreement in [(7, 6, 2, 3), (11, 10, 3, 5), (13, 12, 3, 8)]:
        t = agreement - k
        j = n - agreement
        mean = expected_value(q, n, k, agreement)
        second = second_moment_formula(q, n, k, agreement)
        variance = second - mean * mean
        neighborhood = dependency_neighborhood(n, j, t)
        dependency = neighborhood["dependent_neighbors_including_self"]["value"]
        coarse_dependency_bound = n ** (2 * (t - 1))
        variance_bound = dependency * mean
        relative_variance = variance / (mean * mean)
        relative_bound = Fraction(dependency, 1) / mean
        coarse_relative_bound = Fraction(coarse_dependency_bound, 1) / mean
        ok &= dependency <= coarse_dependency_bound
        ok &= variance <= variance_bound
        ok &= relative_variance <= relative_bound
        ok &= relative_bound <= coarse_relative_bound
        rows.append({
            "q": q,
            "n": n,
            "k": k,
            "agreement": agreement,
            "t": t,
            "j": j,
            "mean": fraction_record(mean),
            "variance": fraction_record(variance),
            "dependency_neighborhood_size": dependency,
            "coarse_dependency_bound_n_power": coarse_dependency_bound,
            "variance_upper_bound": fraction_record(variance_bound),
            "relative_variance": fraction_record(relative_variance),
            "relative_variance_upper_bound": fraction_record(relative_bound),
            "coarse_relative_variance_upper_bound": fraction_record(coarse_relative_bound),
            "mean_over_dependency": fraction_record(mean / dependency),
            "criterion_gives_nonzero_probability": relative_bound < 1,
        })
    return ok, {
        "statement": (
            "Since covariance is supported in the radius-(t-1) Johnson ball "
            "and every joint event is contained in one locator event, "
            "Var(N_A) <= E[N_A] * D_t where D_t is the dependency "
            "neighborhood size. Hence Var(N_A)/E[N_A]^2 <= D_t/E[N_A]."
        ),
        "rows": rows,
    }


def check_exponent_concentration_consumer() -> tuple[bool, dict]:
    rows = []
    ok = True
    for n, t, reserve in [(16, 1, 2), (512, 9, 4), (2 ** 20, 4, 8)]:
        radius_exponent = 2 * (t - 1)
        mean_threshold = n ** (radius_exponent + reserve)
        dependency_bound = n ** radius_exponent
        relative_bound = Fraction(dependency_bound, mean_threshold)
        target = Fraction(1, n ** reserve)
        ok &= relative_bound == target
        rows.append({
            "n": n,
            "t": t,
            "reserve_exponent_s": reserve,
            "dependency_exponent_budget": radius_exponent,
            "mean_threshold_exponent": radius_exponent + reserve,
            "relative_variance_bound": fraction_record(relative_bound),
            "target_n_power": f"n^-{reserve}",
        })
    return ok, {
        "statement": (
            "Using D_t(n,j) <= n^(2(t-1)), if E[N_A] >= n^(2(t-1)+s), "
            "then Var(N_A)/E[N_A]^2 <= n^-s."
        ),
        "rows": rows,
    }


def check_random_pair_phase_criterion() -> tuple[bool, dict]:
    finite_rows = []
    ok = True
    for q, n, k, agreement in [(13, 12, 3, 8), (7, 6, 2, 3), (11, 10, 3, 5)]:
        t = agreement - k
        j = n - agreement
        mean = expected_value(q, n, k, agreement)
        neighborhood = dependency_neighborhood(n, j, t)
        dependency = neighborhood["dependent_neighbors_including_self"]["value"]
        zero_upper = Fraction(dependency, 1) / mean
        half_deviation_upper = 4 * zero_upper
        finite_rows.append({
            "q": q,
            "n": n,
            "k": k,
            "agreement": agreement,
            "t": t,
            "j": j,
            "mean": fraction_record(mean),
            "markov_nonempty_upper": fraction_record(mean),
            "dependency_neighborhood_size": dependency,
            "chebyshev_zero_upper": fraction_record(zero_upper),
            "chebyshev_half_mean_deviation_upper": fraction_record(half_deviation_upper),
            "phase_reading": (
                "low_mean_empty" if mean < 1 else
                "dependency_dominated_nonempty" if zero_upper < 1 else
                "borderline_for_this_coarse_consumer"
            ),
        })
    ok &= finite_rows[0]["phase_reading"] == "low_mean_empty"
    ok &= finite_rows[1]["phase_reading"] == "dependency_dominated_nonempty"
    ok &= finite_rows[2]["phase_reading"] == "borderline_for_this_coarse_consumer"

    exponent_rows = []
    for n, t, low_s, high_s, rel_s in [(512, 9, 8, 4, 2), (2 ** 20, 4, 16, 8, 3)]:
        low_mean = Fraction(1, n ** low_s)
        high_mean = Fraction(n ** (2 * (t - 1) + high_s), 1)
        zero_bound = Fraction(n ** (2 * (t - 1)), 1) / high_mean
        rel_eps = Fraction(1, n ** rel_s)
        concentrated_mean = Fraction(n ** (2 * (t - 1) + high_s + 2 * rel_s), 1)
        rel_deviation_bound = (
            Fraction(n ** (2 * (t - 1)), 1)
            / (rel_eps * rel_eps * concentrated_mean)
        )
        ok &= low_mean == Fraction(1, n ** low_s)
        ok &= zero_bound == Fraction(1, n ** high_s)
        ok &= rel_deviation_bound == Fraction(1, n ** high_s)
        exponent_rows.append({
            "n": n,
            "t": t,
            "low_mean_exponent_s": low_s,
            "low_phase_markov_bound": fraction_record(low_mean),
            "high_mean_exponent": 2 * (t - 1) + high_s,
            "high_phase_zero_bound": fraction_record(zero_bound),
            "relative_error_exponent_r": rel_s,
            "concentrated_mean_exponent": 2 * (t - 1) + high_s + 2 * rel_s,
            "relative_deviation_probability_bound": fraction_record(rel_deviation_bound),
        })

    return ok, {
        "statement": (
            "FM1 gives a random-pair phase criterion: if the mean is tiny, "
            "Markov makes aligned locators unlikely; if the mean dominates "
            "the dependency neighborhood, Chebyshev makes nonemptiness and "
            "relative concentration likely."
        ),
        "finite_rows": finite_rows,
        "exponent_rows": exponent_rows,
    }


def paley_zygmund_nonzero_bound(q: int, n: int, k: int, agreement: int) -> Fraction:
    mean = expected_value(q, n, k, agreement)
    second = second_moment_formula(q, n, k, agreement)
    if second == 0:
        return Fraction(0, 1)
    return mean * mean / second


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


def check_overlap_excess_decomposition() -> tuple[bool, dict]:
    examples = []
    ok = True
    for q, n, k, agreement in [(7, 6, 2, 3), (11, 10, 3, 5)]:
        decomp = overlap_decomposition(q, n, k, agreement)
        baseline = Fraction(
            decomp["baseline_independent_second_moment"]["numerator"],
            decomp["baseline_independent_second_moment"]["denominator"],
        )
        correction = Fraction(
            decomp["correction"]["numerator"],
            decomp["correction"]["denominator"],
        )
        second = Fraction(
            decomp["second_moment"]["numerator"],
            decomp["second_moment"]["denominator"],
        )
        variance = Fraction(
            decomp["variance"]["numerator"],
            decomp["variance"]["denominator"],
        )
        t, j = decomp["t"], decomp["j"]
        threshold = decomp["defect_positive_overlap_threshold"]
        low_excess_zero = all(
            rec["defect_h"] == 0
            and rec["excess_over_independent"]["numerator"] == 0
            for rec in decomp["records"]
            if rec["overlap"] < threshold
        )
        high_excess_positive = all(
            rec["defect_h"] > 0
            and rec["excess_over_independent"]["numerator"] > 0
            for rec in decomp["records"]
            if rec["overlap"] >= threshold
        )
        example = {
            **decomp,
            "baseline_plus_correction_matches_second_moment": baseline + correction == second,
            "correction_matches_variance": correction == variance,
            "low_overlap_excess_zero": low_excess_zero,
            "high_overlap_excess_positive": high_excess_positive,
        }
        if t == 1:
            mean = expected_value(q, n, k, agreement)
            variance = second - mean * mean
            locator_count = comb(n, j)
            p1 = Fraction((q ** t - 1) * q, q ** (2 * t))
            expected_variance = locator_count * p1 * (1 - p1)
            example["slack_one_pairwise_independence_variance"] = {
                "variance": {
                    "numerator": variance.numerator,
                    "denominator": variance.denominator,
                },
                "formula": {
                    "numerator": expected_variance.numerator,
                    "denominator": expected_variance.denominator,
                },
                "matches": variance == expected_variance,
            }
            ok &= variance == expected_variance
        ok &= baseline + correction == second
        ok &= correction == variance
        ok &= low_excess_zero
        ok &= high_excess_positive
        examples.append(example)
    return ok, {
        "formula": "E[N^2] = E_indep[N^2] + sum_{c>=j-t+1} ordered_pairs(c)(P_h-P_0)",
        "examples": examples,
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
    actual_nonzero_probability = Fraction(total_pairs - aligned_hist.get(0, 0), total_pairs)
    pz_nonzero_bound = paley_zygmund_nonzero_bound(p, n, k, agreement)
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
        "actual_nonzero_probability": {
            "numerator": actual_nonzero_probability.numerator,
            "denominator": actual_nonzero_probability.denominator,
            "decimal": float(actual_nonzero_probability),
        },
        "paley_zygmund_nonzero_lower_bound": {
            "numerator": pz_nonzero_bound.numerator,
            "denominator": pz_nonzero_bound.denominator,
            "decimal": float(pz_nonzero_bound),
        },
    }
    return (
        mean == expected
        and second_moment == expected_second_moment
        and actual_nonzero_probability >= pz_nonzero_bound
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
    ok_overlap, overlap = check_overlap_excess_decomposition()
    ok_dependency, dependency = check_dependency_graph_consumer()
    ok_dep_concentration, dep_concentration = check_dependency_degree_concentration()
    ok_exp_concentration, exp_concentration = check_exponent_concentration_consumer()
    ok_phase, phase = check_random_pair_phase_criterion()
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
        "paley_zygmund_consumer": "Pr[N_A>0] >= E[N_A]^2 / E[N_A^2]",
        "overlap_excess_statement": (
            "The variance is the second-moment excess over independent locator "
            "indicators, supported exactly on overlaps c >= j-t+1."
        ),
        "chebyshev_consumer": (
            "Pr[N_A=0] <= Var(N_A)/E[N_A]^2 and "
            "Pr[|N_A-E[N_A]| >= eps E[N_A]] <= Var(N_A)/(eps^2 E[N_A]^2)."
        ),
        "dependency_degree_concentration_consumer": (
            "If E[N_A] is larger than the radius-(t-1) Johnson dependency "
            "neighborhood D_t, then the exact second moment is concentrated "
            "by Var(N_A)/E[N_A]^2 <= D_t/E[N_A]."
        ),
        "exponent_concentration_consumer": (
            "Since D_t(n,j) <= n^(2(t-1)), the sufficient condition "
            "E[N_A] >= n^(2(t-1)+s) gives relative variance at most n^-s."
        ),
        "random_pair_phase_criterion": (
            "Markov controls the low-mean phase; Chebyshev and the dependency "
            "neighborhood control the high-mean phase."
        ),
        "definition": (
            "For a split degree-j locator ell, set a=S_ell(u), b=S_ell(v) in F_q^t. "
            "The locator is aligned when b != 0 and a lies in the one-dimensional span of b."
        ),
        "checks": {
            "f13_surjectivity": f13,
            "f13_joint_rank_formula": joint,
            "f5_fiber_product_joint_probability": fiber,
            "overlap_excess_decomposition": overlap,
            "dependency_graph_consumer": dependency,
            "dependency_degree_concentration": dep_concentration,
            "exponent_concentration_consumer": exp_concentration,
            "random_pair_phase_criterion": phase,
            "f5_bruteforce": f5,
            "f17_regular_window_markov_tail": window,
        },
        "passed": (
            ok_f13
            and ok_joint
            and ok_fiber
            and ok_overlap
            and ok_dependency
            and ok_dep_concentration
            and ok_exp_concentration
            and ok_phase
            and ok_f5
            and ok_window
        ),
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
        elif name == "overlap_excess_decomposition":
            for example in data["examples"]:
                print(
                    "        q={q}, n={n}, k={k}, A={agreement}, t={t}, j={j}: "
                    "threshold c>={defect_positive_overlap_threshold}, "
                    "matches={baseline_plus_correction_matches_second_moment}, "
                    "relvar={relvar:.6g}".format(
                        relvar=example["relative_variance"]["decimal"],
                        **example,
                    )
                )
        elif name == "dependency_graph_consumer":
            for example in data["examples"]:
                print(
                    "        n={n}, j={j}, t={t}: dependent radius={dependent_radius}, "
                    "degree log2={deg:.3f}, independent neighbors log2={ind:.3f}".format(
                        n=example["n"],
                        j=example["j"],
                        t=example["t"],
                        dependent_radius=example["dependent_radius"],
                        deg=example["dependent_degree_excluding_self"]["log2"] or 0.0,
                        ind=example["independent_neighbors"]["log2"] or 0.0,
                    )
                )
        elif name == "dependency_degree_concentration":
            for row in data["rows"]:
                print(
                    "        q={q}, n={n}, k={k}, A={agreement}: "
                    "D={dependency_neighborhood_size}, relvar={rel:.6g}, "
                    "D/E={bound:.6g}".format(
                        rel=row["relative_variance"]["decimal"],
                        bound=row["relative_variance_upper_bound"]["decimal"],
                        **row,
                    )
                )
        elif name == "exponent_concentration_consumer":
            for row in data["rows"]:
                print(
                    "        n={n}, t={t}, s={reserve_exponent_s}: "
                    "mean exponent {mean_threshold_exponent} -> relvar <= {target_n_power}".format(
                        **row
                    )
                )
        elif name == "random_pair_phase_criterion":
            for row in data["finite_rows"]:
                print(
                    "        q={q}, n={n}, k={k}, A={agreement}: "
                    "mean={mean:.6g}, zero_bound={zero:.6g}, phase={phase}".format(
                        q=row["q"],
                        n=row["n"],
                        k=row["k"],
                        agreement=row["agreement"],
                        mean=row["mean"]["decimal"],
                        zero=row["chebyshev_zero_upper"]["decimal"],
                        phase=row["phase_reading"],
                    )
                )
            for row in data["exponent_rows"]:
                print(
                    "        n={n}, t={t}: low <= n^-{low}, high zero <= {high}".format(
                        n=row["n"],
                        t=row["t"],
                        low=row["low_mean_exponent_s"],
                        high=row["high_phase_zero_bound"]["decimal"],
                    )
                )
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
            nz = data["actual_nonzero_probability"]
            pz = data["paley_zygmund_nonzero_lower_bound"]
            print(
                f"        actual Pr[N>0] = {nz['numerator']}/{nz['denominator']} = "
                f"{nz['decimal']:.12f}"
            )
            print(
                f"        Paley-Zygmund lower bound = {pz['numerator']}/{pz['denominator']} = "
                f"{pz['decimal']:.12f}"
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
