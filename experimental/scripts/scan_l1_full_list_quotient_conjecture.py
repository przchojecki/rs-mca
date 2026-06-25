#!/usr/bin/env python3
"""Falsification scanner for the repaired full L1 list conjecture.

This is EXPERIMENTAL evidence only.  It scans the repaired arbitrary-word
object, i.e. the actual Reed-Solomon list / image fiber, not the raw support
fiber.  Listed codewords are separated by the cyclic stabilizer of their
maximal agreement set, giving an exact quotient budget and a primitive
remainder analogous to the monomial-prefix scanner.

Two modes are available:

* exact sparse-syndrome enumeration for all received-word cosets when the
  low-weight error ball is small;
* random/adversarial received-word sampling using k-subset interpolation near
  the entropy boundary, including glued-codeword sunflower attacks.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
from collections import Counter, defaultdict
from math import comb, isqrt, lgamma, log2
from typing import Iterable


LN2 = 0.6931471805599453


def factorint(value: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def primitive_root(p: int) -> int:
    if p == 2:
        return 1
    phi = p - 1
    factors = factorint(phi).keys()
    for candidate in range(2, p):
        if all(pow(candidate, phi // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def subgroup(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    root = pow(primitive_root(p), (p - 1) // n, p)
    out = []
    current = 1
    for _ in range(n):
        out.append(current)
        current = (current * root) % p
    return out


def positive_divisors(value: int) -> list[int]:
    small: list[int] = []
    large: list[int] = []
    divisor = 1
    while divisor * divisor <= value:
        if value % divisor == 0:
            small.append(divisor)
            if divisor != value // divisor:
                large.append(value // divisor)
        divisor += 1
    return small + large[::-1]


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    if k == 0 or k == n:
        return 0.0
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)) / LN2


def ball_size(n: int, r: int, q: int) -> int:
    return sum(comb(n, weight) * ((q - 1) ** weight) for weight in range(r + 1))


def rotate_mask(mask: int, shift: int, n: int) -> int:
    shift %= n
    if shift == 0:
        return mask
    full = (1 << n) - 1
    return ((mask << shift) | (mask >> (n - shift))) & full


def stabilizer_order(mask: int, n: int) -> int:
    return sum(1 for shift in range(n) if rotate_mask(mask, shift, n) == mask)


def mask_to_exponents(mask: int, n: int) -> list[int]:
    return [index for index in range(n) if mask & (1 << index)]


def mask_from_indices(indices: Iterable[int]) -> int:
    mask = 0
    for index in indices:
        mask |= 1 << index
    return mask


def trim_poly(coeffs: Iterable[int]) -> tuple[int, ...]:
    out = list(coeffs)
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_degree(coeffs: Iterable[int]) -> int:
    return len(trim_poly(coeffs)) - 1


def poly_add(left: Iterable[int], right: Iterable[int], p: int) -> tuple[int, ...]:
    left_values = tuple(left)
    right_values = tuple(right)
    size = max(len(left_values), len(right_values))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left_values[index] if index < len(left_values) else 0)
            + (right_values[index] if index < len(right_values) else 0)
        ) % p
    return trim_poly(out)


def poly_scale(coeffs: Iterable[int], scalar: int, p: int) -> tuple[int, ...]:
    return trim_poly((scalar * coeff) % p for coeff in coeffs)


def multiply_by_linear(coeffs: Iterable[int], root: int, p: int) -> tuple[int, ...]:
    values = tuple(coeffs)
    out = [0] * (len(values) + 1)
    for index, coeff in enumerate(values):
        out[index] = (out[index] - root * coeff) % p
        out[index + 1] = (out[index + 1] + coeff) % p
    return trim_poly(out)


def interpolate_polynomial(xs: list[int], ys: list[int], p: int) -> tuple[int, ...]:
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have the same length")
    if len(set(xs)) != len(xs):
        raise ValueError("interpolation points must be distinct")
    result: tuple[int, ...] = ()
    for j, x_j in enumerate(xs):
        basis: tuple[int, ...] = (1,)
        denominator = 1
        for m, x_m in enumerate(xs):
            if m == j:
                continue
            basis = multiply_by_linear(basis, x_m, p)
            denominator = (denominator * (x_j - x_m)) % p
        result = poly_add(
            result,
            poly_scale(basis, ys[j] * pow(denominator, -1, p), p),
            p,
        )
    return result


def eval_poly(coeffs: Iterable[int], x_value: int, p: int) -> int:
    out = 0
    for coeff in reversed(tuple(coeffs)):
        out = (out * x_value + coeff) % p
    return out


def poly_values(coeffs: Iterable[int], domain: list[int], p: int) -> tuple[int, ...]:
    return tuple(eval_poly(coeffs, x_value, p) for x_value in domain)


def matrix_rref(matrix: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    column_count = len(rows[0]) if rows else 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column] % p),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column] % p, -1, p)
        rows[pivot_row] = [(value * inverse) % p for value in rows[pivot_row]]
        for row_index, row in enumerate(rows):
            if row_index == pivot_row:
                continue
            factor = row[column] % p
            if factor:
                rows[row_index] = [
                    (entry - factor * pivot_entry) % p
                    for entry, pivot_entry in zip(row, rows[pivot_row], strict=True)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivot_columns


def parity_check_matrix(domain: list[int], k: int, p: int) -> list[list[int]]:
    generator = [[pow(x_value, degree, p) for x_value in domain] for degree in range(k)]
    rref, pivots = matrix_rref(generator, p)
    pivot_set = set(pivots)
    free_columns = [
        column for column in range(len(domain)) if column not in pivot_set
    ]
    rows: list[list[int]] = []
    for free in free_columns:
        vector = [0] * len(domain)
        vector[free] = 1
        for row_index, pivot_column in enumerate(pivots):
            vector[pivot_column] = (-rref[row_index][free]) % p
        rows.append(vector)
    return rows


def syndrome_from_support(
    columns: list[tuple[int, ...]],
    support: tuple[int, ...],
    values: tuple[int, ...],
    p: int,
) -> tuple[int, ...]:
    if not support:
        return tuple(0 for _ in columns[0]) if columns else ()
    out = [0] * len(columns[0])
    for position, value in zip(support, values, strict=True):
        column = columns[position]
        for row_index, entry in enumerate(column):
            out[row_index] = (out[row_index] + value * entry) % p
    return tuple(out)


def agreement_mask_from_error_support(support: tuple[int, ...], n: int) -> int:
    error_mask = 0
    for position in support:
        error_mask |= 1 << position
    return ((1 << n) - 1) ^ error_mask


def entropy_report(p: int, n: int, k: int, s: int, epsilon: float) -> dict[str, object]:
    sigma = s - k
    entropy_target = log2_binom(n, s)
    entropy_bits = sigma * log2(p)
    margin = entropy_bits - (1.0 + epsilon) * entropy_target
    r = n - s
    mean = ball_size(n, r, p) / (p ** (n - k))
    return {
        "sigma": sigma,
        "radius": r,
        "entropy_bits": round(entropy_bits, 6),
        "entropy_target_bits": round(entropy_target, 6),
        "entropy_margin_bits": round(margin, 6),
        "reserve_cleared": margin >= -1e-12,
        "sparse_syndrome_ball_mean": mean,
    }


def johnson_full_list_profile(n: int, k: int, s: int) -> dict[str, object]:
    """Return the proved arbitrary-word full-list Johnson bound, if active."""
    denominator = s * s - n * (k - 1)
    numerator = n * (n - k + 1)
    unique_decoding = 2 * s > n + k - 1
    profile: dict[str, object] = {
        "status": "PROVED/FULL_LIST_JOHNSON_REGION",
        "condition": "s^2 > n(k-1)",
        "unique_decoding_condition": "2s > n+k-1",
        "unique_decoding": unique_decoding,
        "johnson_denominator": denominator,
        "johnson_numerator": numerator,
        "in_johnson_region": denominator > 0,
        "bound": None,
        "bound_reason": "outside-johnson-region",
    }
    if unique_decoding:
        profile["bound"] = 1
        profile["bound_reason"] = "unique-decoding"
    elif denominator > 0:
        profile["bound"] = numerator // denominator
        profile["bound_reason"] = "second-moment-johnson"
    return profile


def johnson_slack_needed(n: int, k: int, s: int) -> int:
    """Minimum slack needed to move threshold s into the Johnson region."""
    threshold = n * (k - 1)
    if s * s > threshold:
        return 0
    return isqrt(threshold) + 1 - s


def johnson_bound_report(
    profile: dict[str, object],
    max_total: int,
    max_primitive: int,
) -> dict[str, object]:
    bound = profile.get("bound")
    if not isinstance(bound, int):
        return {
            "johnson_bound_checked": False,
            "johnson_bound_holds_for_max_list": None,
            "johnson_bound_holds_for_max_primitive": None,
        }
    return {
        "johnson_bound_checked": True,
        "johnson_bound_holds_for_max_list": max_total <= bound,
        "johnson_bound_holds_for_max_primitive": max_primitive <= bound,
    }


def empty_ledger(n: int) -> dict[int, int]:
    return {divisor: 0 for divisor in positive_divisors(n)}


def exact_syndrome_scan(
    p: int,
    n: int,
    k: int,
    s: int,
    epsilon: float,
    alert_power: float,
    max_ball: int,
    max_examples: int,
) -> dict[str, object]:
    r = n - s
    low_weight_ball = ball_size(n, r, p)
    min_distance = n - k + 1
    entropy = entropy_report(p, n, k, s, epsilon)
    johnson_profile = johnson_full_list_profile(n, k, s)
    threshold = n ** alert_power

    if 2 * r < min_distance:
        primitive_syndromes = 0
        primitive_example: dict[str, object] | None = None
        for weight in range(r + 1):
            for support in itertools.combinations(range(n), weight):
                agreement_mask = agreement_mask_from_error_support(support, n)
                if stabilizer_order(agreement_mask, n) == 1:
                    primitive_syndromes += (p - 1) ** weight
                    if primitive_example is None:
                        primitive_example = {
                            "certificate": "minimum-distance injective on ball",
                            "error_support": list(support),
                            "agreement_set": mask_to_exponents(agreement_mask, n),
                            "list_size": 1,
                            "primitive": 1,
                            "quotient_budget": 0,
                        }
        quotient_syndromes = low_weight_ball - primitive_syndromes
        max_primitive = 1 if primitive_syndromes else 0
        max_quotient = 1 if quotient_syndromes else 0
        primitive_alert = bool(entropy["reserve_cleared"]) and max_primitive > threshold
        johnson_report = johnson_bound_report(
            johnson_profile,
            1 if low_weight_ball else 0,
            max_primitive,
        )
        return {
            "status": "EXPERIMENTAL/FULL_LIST_EXACT_SYNDROME_SCAN",
            "mode": "exact-syndrome",
            "params": {"p": p, "n": n, "k": k, "s": s, **entropy},
            "johnson_full_list_profile": johnson_profile,
            "low_weight_ball_size": low_weight_ball,
            "occupied_syndromes": low_weight_ball,
            "minimum_distance": min_distance,
            "unique_decoding_shortcut": True,
            "max_list_size": 1 if low_weight_ball else 0,
            "max_primitive_exact": max_primitive,
            "max_quotient_budget": max_quotient,
            "list_size_histogram": {1: low_weight_ball},
            "primitive_count_histogram": {
                key: value
                for key, value in {0: quotient_syndromes, 1: primitive_syndromes}.items()
                if value
            },
            "primitive_alert_threshold": round(threshold, 6),
            "primitive_alert": primitive_alert,
            **johnson_report,
            "max_primitive_examples": (
                [primitive_example] if primitive_example is not None else []
            ),
        }

    if low_weight_ball > max_ball:
        raise ValueError(
            f"low-weight ball has {low_weight_ball} vectors, above --max-ball"
        )

    domain = subgroup(p, n)
    checks = parity_check_matrix(domain, k, p)
    columns = [tuple(row[index] for row in checks) for index in range(n)]
    syndromes: dict[tuple[int, ...], dict[int, int]] = defaultdict(lambda: empty_ledger(n))

    for weight in range(r + 1):
        for support in itertools.combinations(range(n), weight):
            agreement_mask = agreement_mask_from_error_support(support, n)
            stab = stabilizer_order(agreement_mask, n)
            value_iter = [()] if weight == 0 else itertools.product(range(1, p), repeat=weight)
            for values in value_iter:
                z = syndrome_from_support(columns, support, values, p)
                syndromes[z][stab] += 1

    max_total = 0
    max_primitive = 0
    max_quotient = 0
    total_histogram: Counter[int] = Counter()
    primitive_histogram: Counter[int] = Counter()
    examples: list[dict[str, object]] = []
    for z, ledger in syndromes.items():
        total = sum(ledger.values())
        primitive = ledger.get(1, 0)
        quotient = total - primitive
        total_histogram[total] += 1
        primitive_histogram[primitive] += 1
        max_quotient = max(max_quotient, quotient)
        if primitive > max_primitive or total > max_total:
            if primitive > max_primitive:
                examples = []
            max_total = max(max_total, total)
            max_primitive = max(max_primitive, primitive)
        if primitive == max_primitive and len(examples) < max_examples:
            examples.append({
                "syndrome": list(z),
                "list_size": total,
                "primitive": primitive,
                "quotient_budget": quotient,
                "exact_stabilizer_counts": {
                    str(order): count for order, count in ledger.items() if count
                },
            })

    primitive_alert = bool(entropy["reserve_cleared"]) and max_primitive > threshold
    johnson_report = johnson_bound_report(johnson_profile, max_total, max_primitive)
    return {
        "status": "EXPERIMENTAL/FULL_LIST_EXACT_SYNDROME_SCAN",
        "mode": "exact-syndrome",
        "params": {"p": p, "n": n, "k": k, "s": s, **entropy},
        "johnson_full_list_profile": johnson_profile,
        "low_weight_ball_size": low_weight_ball,
        "occupied_syndromes": len(syndromes),
        "minimum_distance": min_distance,
        "unique_decoding_shortcut": False,
        "max_list_size": max_total,
        "max_primitive_exact": max_primitive,
        "max_quotient_budget": max_quotient,
        "list_size_histogram": dict(sorted(total_histogram.items())),
        "primitive_count_histogram": dict(sorted(primitive_histogram.items())),
        "primitive_alert_threshold": round(threshold, 6),
        "primitive_alert": primitive_alert,
        **johnson_report,
        "max_primitive_examples": examples,
    }


def img_list_from_values(
    values: list[int],
    domain: list[int],
    k: int,
    s: int,
    p: int,
) -> dict[tuple[int, ...], int]:
    n = len(domain)
    listed: dict[tuple[int, ...], int] = {}
    for support in itertools.combinations(range(n), k):
        xs = [domain[index] for index in support]
        ys = [values[index] for index in support]
        poly = interpolate_polynomial(xs, ys, p)
        if poly_degree(poly) >= k:
            continue
        codeword = poly_values(poly, domain, p)
        if codeword in listed:
            continue
        agreement = sum(
            1 for left, right in zip(codeword, values, strict=True) if left == right
        )
        if agreement >= s:
            mask = 0
            for index, (left, right) in enumerate(zip(codeword, values, strict=True)):
                if left == right:
                    mask |= 1 << index
            listed[codeword] = mask
    return listed


def img_list_from_support_subsets(
    values: list[int],
    domain: list[int],
    k: int,
    s: int,
    p: int,
) -> dict[tuple[int, ...], int]:
    n = len(domain)
    listed: dict[tuple[int, ...], int] = {}
    for support in itertools.combinations(range(n), s):
        xs = [domain[index] for index in support]
        ys = [values[index] for index in support]
        poly = interpolate_polynomial(xs, ys, p)
        if poly_degree(poly) >= k:
            continue
        codeword = poly_values(poly, domain, p)
        if codeword in listed:
            continue
        mask = 0
        agreement = 0
        for index, (left, right) in enumerate(zip(codeword, values, strict=True)):
            if left == right:
                mask |= 1 << index
                agreement += 1
        if agreement >= s:
            listed[codeword] = mask
    return listed


def img_list(
    values: list[int],
    domain: list[int],
    k: int,
    s: int,
    p: int,
    decoder: str,
) -> dict[tuple[int, ...], int]:
    if decoder == "support":
        return img_list_from_support_subsets(values, domain, k, s, p)
    if decoder == "k-subset":
        return img_list_from_values(values, domain, k, s, p)
    if comb(len(domain), s) <= comb(len(domain), k):
        return img_list_from_support_subsets(values, domain, k, s, p)
    return img_list_from_values(values, domain, k, s, p)


def eval_random_poly(domain: list[int], coeffs: list[int], p: int) -> list[int]:
    return [eval_poly(coeffs, x_value, p) for x_value in domain]


def locator_polynomial(domain: list[int], indices: list[int], p: int) -> tuple[int, ...]:
    poly: tuple[int, ...] = (1,)
    for index in indices:
        poly = multiply_by_linear(poly, domain[index], p)
    return poly


def sunflower_word_from_blocks(
    p: int,
    n: int,
    k: int,
    s: int,
    core: list[int],
    petals: list[list[int]],
    name: str,
) -> dict[str, object] | None:
    """Build U from P_i = c_i L_core on core+petal_i.

    The background scalar is 0 and the petal scalars are 1,2,..., so each
    listed codeword has exact agreement set core union petal_i as long as the
    scalars are distinct in F_p.  This is a deliberate high-multiplicity attack,
    not random sampling.
    """
    if not petals or len(petals) >= p:
        return None
    domain = subgroup(p, n)
    core_locator = locator_polynomial(domain, core, p)
    values = [0] * n
    intended_sets: list[list[int]] = []
    for scalar, petal in enumerate(petals, start=1):
        intended = sorted(core + petal)
        intended_sets.append(intended)
        for index in petal:
            values[index] = (scalar * eval_poly(core_locator, domain[index], p)) % p
    intended_stabilizers = [
        stabilizer_order(sum(1 << index for index in intended), n)
        for intended in intended_sets
    ]
    return {
        "name": name,
        "values": values,
        "sunflower": {
            "core": sorted(core),
            "petals": [sorted(petal) for petal in petals],
            "intended_list_size": len(petals),
            "intended_agreement_sets": intended_sets,
            "intended_stabilizer_orders": intended_stabilizers,
        },
    }


def sunflower_words(
    p: int,
    n: int,
    k: int,
    s: int,
    seed: int,
    random_count: int,
) -> list[dict[str, object]]:
    if not (0 < k < s <= n):
        return []
    core_size = k - 1
    petal_size = s - core_size
    if core_size < 0 or petal_size <= 0:
        return []

    words: list[dict[str, object]] = []
    core = list(range(core_size))
    remaining = [index for index in range(n) if index not in core]
    petal_count = min(len(remaining) // petal_size, p - 1)
    petals = [
        remaining[i * petal_size:(i + 1) * petal_size]
        for i in range(petal_count)
    ]
    word = sunflower_word_from_blocks(
        p,
        n,
        k,
        s,
        core,
        petals,
        name=f"sunflower-sequential-m{petal_count}",
    )
    if word is not None:
        words.append(word)

    rng = random.Random(seed + 7919)
    for index in range(random_count):
        shuffled = list(range(n))
        rng.shuffle(shuffled)
        core = sorted(shuffled[:core_size])
        remaining = shuffled[core_size:]
        petal_count = min(len(remaining) // petal_size, p - 1)
        petals = [
            remaining[i * petal_size:(i + 1) * petal_size]
            for i in range(petal_count)
        ]
        word = sunflower_word_from_blocks(
            p,
            n,
            k,
            s,
            core,
            petals,
            name=f"sunflower-random-{index}-m{petal_count}",
        )
        if word is not None:
            words.append(word)
    return words


def classify_sunflower_listing(
    listed_masks: Iterable[int],
    sunflower: dict[str, object],
    n: int,
    max_extra_examples: int,
) -> dict[str, object]:
    core = set(sunflower["core"])
    petals = [set(petal) for petal in sunflower["petals"]]
    petal_size = len(petals[0]) if petals else 0
    k = len(core) + 1
    s = len(core) + petal_size
    johnson_slack = johnson_slack_needed(n, k, s)
    petal_union = set().union(*petals) if petals else set()
    background = set(range(n)) - core - petal_union
    intended_masks = {
        mask_from_indices(intended)
        for intended in sunflower["intended_agreement_sets"]
    }
    listed_mask_set = set(listed_masks)
    planted_present = listed_mask_set & intended_masks
    missing_planted = intended_masks - listed_mask_set
    extra_masks = sorted(listed_mask_set - intended_masks)
    profile_histogram: Counter[tuple[int, int, int, int, int, int]] = Counter()
    parameter_histogram: Counter[
        tuple[
            int, int, int, int, int, int, int, int, int, int,
            int, int, int, int, int, int, int, int,
        ]
    ] = Counter()
    extra_examples: list[dict[str, object]] = []
    johnson_covered_extras = 0
    for mask in extra_masks:
        agreement = set(mask_to_exponents(mask, n))
        agreement_size = len(agreement)
        agreement_slack = agreement_size - s
        johnson_covered = agreement_slack >= johnson_slack
        johnson_unique_covered = 2 * agreement_size > n + k - 1
        if johnson_covered:
            johnson_covered_extras += 1
        petal_hits = [len(agreement & petal) for petal in petals]
        positive_petal_hits = [hit for hit in petal_hits if hit]
        positive_petal_hits_desc = sorted(positive_petal_hits, reverse=True)
        core_hits = len(agreement & core)
        core_defect = len(core) - core_hits
        background_hits = len(agreement & background)
        touched_petals = len(positive_petal_hits)
        petal_deficit = sum(
            len(petal) - hit
            for hit, petal in zip(petal_hits, petals, strict=True)
            if hit
        )
        max_petal_hit = positive_petal_hits_desc[0] if positive_petal_hits_desc else 0
        second_petal_hit = (
            positive_petal_hits_desc[1] if len(positive_petal_hits_desc) >= 2 else 0
        )
        positive_petal_deficits = sorted(
            len(petal) - hit
            for hit, petal in zip(petal_hits, petals, strict=True)
            if hit
        )
        best_two_petal_deficit = (
            positive_petal_deficits[0] + positive_petal_deficits[1]
            if len(positive_petal_deficits) >= 2
            else -1
        )
        best_background_petal_deficit = (
            (petal_size - background_hits) + (petal_size - max_petal_hit)
            if positive_petal_hits
            else -1
        )
        cofactor_excess = core_defect - petal_size
        anchor_exponent = max(
            0,
            core_defect - max(background_hits, max_petal_hit) + 1,
        )
        two_anchor_exponent = (
            2 * cofactor_excess + best_two_petal_deficit + 2
            if best_two_petal_deficit >= 0
            else -1
        )
        background_petal_exponent = (
            2 * cofactor_excess + best_background_petal_deficit + 2
            if best_background_petal_deficit >= 0
            else -1
        )
        valid_anchor_deficits = [
            value
            for value in (best_two_petal_deficit, best_background_petal_deficit)
            if value >= 0
        ]
        best_anchor_deficit = (
            min(valid_anchor_deficits) if valid_anchor_deficits else -1
        )
        valid_anchor_exponents = [
            value
            for value in (two_anchor_exponent, background_petal_exponent)
            if value >= 0
        ]
        best_anchor_exponent = (
            min(valid_anchor_exponents) if valid_anchor_exponents else -1
        )
        petal_cofactor_exponent = max(0, core_defect - max_petal_hit + 1)
        background_quotient_exponent = max(0, core_defect - background_hits + 1)
        required_petal_hits = petal_size + core_defect - background_hits
        width_floor_a1 = (
            max(0, -(-required_petal_hits // max_petal_hit))
            if max_petal_hit > 0
            else -1
        )
        remaining_after_largest = max(0, required_petal_hits - max_petal_hit)
        width_floor_a2 = (
            1 + max(0, -(-remaining_after_largest // second_petal_hit))
            if second_petal_hit > 0
            else (1 if remaining_after_largest == 0 else -1)
        )
        width_gate_slack = (
            2 * (touched_petals - 1) * petal_size
            - (
                (touched_petals - 1) * best_two_petal_deficit
                + 2 * max(0, cofactor_excess + best_background_petal_deficit)
            )
            if touched_petals >= 2
            and best_two_petal_deficit >= 0
            and best_background_petal_deficit >= 0
            else -1
        )
        list_condition_slack = (
            background_hits + sum(petal_hits) - (petal_size + core_defect)
        )
        profile = (
            agreement_size,
            core_hits,
            sum(petal_hits),
            touched_petals,
            max_petal_hit,
            sum(1 for hit, petal in zip(petal_hits, petals, strict=True)
                if hit == len(petal)),
        )
        parameter_profile = (
            core_defect,
            background_hits,
            touched_petals,
            petal_deficit,
            max_petal_hit,
            second_petal_hit,
            best_two_petal_deficit,
            best_background_petal_deficit,
            cofactor_excess,
            anchor_exponent,
            two_anchor_exponent,
            background_petal_exponent,
            best_anchor_deficit,
            best_anchor_exponent,
            width_floor_a1,
            width_floor_a2,
            width_gate_slack,
            list_condition_slack,
        )
        profile_histogram[profile] += 1
        parameter_histogram[parameter_profile] += 1
        if len(extra_examples) < max_extra_examples:
            extra_examples.append({
                "agreement_set": sorted(agreement),
                "agreement_size": agreement_size,
                "agreement_slack": agreement_slack,
                "johnson_slack_needed": johnson_slack,
                "johnson_covered": johnson_covered,
                "johnson_unique_covered": johnson_unique_covered,
                "core_hits": core_hits,
                "core_defect": core_defect,
                "background_hits": background_hits,
                "total_petal_hits": sum(petal_hits),
                "petal_hits": petal_hits,
                "positive_petals": touched_petals,
                "petal_deficit": petal_deficit,
                "max_petal_hit": max_petal_hit,
                "second_petal_hit": second_petal_hit,
                "best_two_petal_deficit": (
                    best_two_petal_deficit
                    if best_two_petal_deficit >= 0
                    else None
                ),
                "best_background_petal_deficit": (
                    best_background_petal_deficit
                    if best_background_petal_deficit >= 0
                    else None
                ),
                "cofactor_excess": cofactor_excess,
                "background_anchor_exponent": anchor_exponent,
                "two_anchor_exponent": (
                    two_anchor_exponent if two_anchor_exponent >= 0 else None
                ),
                "background_petal_exponent": (
                    background_petal_exponent
                    if background_petal_exponent >= 0
                    else None
                ),
                "best_anchor_deficit": (
                    best_anchor_deficit if best_anchor_deficit >= 0 else None
                ),
                "best_anchor_exponent": (
                    best_anchor_exponent if best_anchor_exponent >= 0 else None
                ),
                "width_floor_a1": (
                    width_floor_a1 if width_floor_a1 >= 0 else None
                ),
                "width_floor_a2": (
                    width_floor_a2 if width_floor_a2 >= 0 else None
                ),
                "width_gate_slack": (
                    width_gate_slack if width_gate_slack >= 0 else None
                ),
                "petal_cofactor_exponent": petal_cofactor_exponent,
                "background_quotient_exponent": background_quotient_exponent,
                "list_condition_slack": list_condition_slack,
                "full_petals": [
                    index for index, (hit, petal) in enumerate(
                        zip(petal_hits, petals, strict=True),
                        start=1,
                    )
                    if hit == len(petal)
                ],
            })
    return {
        "planted_present_count": len(planted_present),
        "planted_missing_count": len(missing_planted),
        "extra_count": len(extra_masks),
        "johnson_slack_needed": johnson_slack,
        "johnson_covered_extra_count": johnson_covered_extras,
        "extra_profile_histogram": {
            (
                f"agreement={profile[0]},core={profile[1]},"
                f"petal_hits={profile[2]},petals={profile[3]},"
                f"max_petal={profile[4]},full_petals={profile[5]}"
            ): count
            for profile, count in sorted(profile_histogram.items())
        },
        "extra_parameter_histogram": {
            (
                f"d={profile[0]},r={profile[1]},t={profile[2]},"
                f"u={profile[3]},a_star={profile[4]},"
                f"second={profile[5]},pair_def={profile[6]},"
                f"bg_pair_def={profile[7]},excess={profile[8]},"
                f"anchor_exp={profile[9]},two_anchor_exp={profile[10]},"
                f"bg_petal_exp={profile[11]},gate_def={profile[12]},"
                f"gate_exp={profile[13]},width1={profile[14]},"
                f"width2={profile[15]},width_gate_slack={profile[16]},"
                f"list_slack={profile[17]}"
            ): count
            for profile, count in sorted(parameter_histogram.items())
        },
        "extra_examples": extra_examples,
    }


def sampled_words(
    p: int,
    n: int,
    k: int,
    s: int,
    sample_count: int,
    seed: int,
    sunflower_count: int,
) -> list[dict[str, object]]:
    domain = subgroup(p, n)
    rng = random.Random(seed)
    words: list[dict[str, object]] = [
        {"name": "zero", "values": [0] * n},
        {"name": "monomial-x^k", "values": [pow(x_value, k, p) for x_value in domain]},
    ]
    for index in range(sample_count):
        values = [rng.randrange(p) for _ in range(n)]
        words.append({"name": f"random-{index}", "values": values})

    for errors in range(1, min(4, n - k) + 1):
        coeffs = [rng.randrange(p) for _ in range(k)]
        values = eval_random_poly(domain, coeffs, p)
        for position in rng.sample(range(n), errors):
            values[position] = (values[position] + 1 + rng.randrange(p - 1)) % p
        words.append({"name": f"planted-radius-{errors}", "values": values})

    for d in positive_divisors(n):
        if d == 1 or n % d or k % d:
            continue
        quotient_n = n // d
        quotient_k = k // d
        quotient_domain = subgroup(p, quotient_n)
        quotient_position = {value: index for index, value in enumerate(quotient_domain)}
        quotient_values = [rng.randrange(p) for _ in range(quotient_n)]
        values = [
            quotient_values[quotient_position[pow(x_value, d, p)]]
            for x_value in domain
        ]
        words.append({"name": f"folded-random-d{d}", "values": values})
        coeffs = [rng.randrange(p) for _ in range(max(1, quotient_k))]
        quotient_codeword = eval_random_poly(quotient_domain, coeffs, p)
        values = [
            quotient_codeword[quotient_position[pow(x_value, d, p)]]
            for x_value in domain
        ]
        words.append({"name": f"folded-codeword-d{d}", "values": values})
    words.extend(sunflower_words(p, n, k, s, seed, sunflower_count))
    return words


def sample_scan(
    p: int,
    n: int,
    k: int,
    s: int,
    epsilon: float,
    alert_power: float,
    samples: int,
    seed: int,
    sunflower_count: int,
    decoder: str,
    max_examples: int,
) -> dict[str, object]:
    domain = subgroup(p, n)
    entropy = entropy_report(p, n, k, s, epsilon)
    johnson_profile = johnson_full_list_profile(n, k, s)
    threshold = n ** alert_power
    max_total = 0
    max_primitive = 0
    max_quotient = 0
    examples: list[dict[str, object]] = []
    rows: list[dict[str, object]] = []
    sunflower_rows = 0
    sunflower_rows_with_extras = 0
    sunflower_max_extra_count = 0
    sunflower_johnson_covered_extras = 0
    sunflower_extra_profile_summary: Counter[str] = Counter()
    sunflower_extra_parameter_summary: Counter[str] = Counter()

    for word in sampled_words(p, n, k, s, samples, seed, sunflower_count):
        values = word["values"]
        assert isinstance(values, list)
        listed = img_list(values, domain, k, s, p, decoder)
        ledger = empty_ledger(n)
        for agreement_mask in listed.values():
            ledger[stabilizer_order(agreement_mask, n)] += 1
        agreement_size_histogram = Counter(
            len(mask_to_exponents(agreement_mask, n))
            for agreement_mask in listed.values()
        )
        total = len(listed)
        primitive = ledger.get(1, 0)
        quotient = total - primitive
        row = {
            "name": word["name"],
            "list_size": total,
            "primitive": primitive,
            "quotient_budget": quotient,
            "agreement_size_histogram": dict(sorted(agreement_size_histogram.items())),
            "max_agreement_size": (
                max(agreement_size_histogram) if agreement_size_histogram else 0
            ),
            "exact_stabilizer_counts": {
                str(order): count for order, count in ledger.items() if count
            },
        }
        if "sunflower" in word:
            sunflower_rows += 1
            row["sunflower"] = word["sunflower"]
            intended = int(word["sunflower"]["intended_list_size"])
            row["sunflower_intended_survives"] = total >= intended
            row["sunflower_extra_list_count"] = total - intended
            sunflower = word["sunflower"]
            assert isinstance(sunflower, dict)
            classification = classify_sunflower_listing(
                listed.values(),
                sunflower,
                n,
                max_examples,
            )
            row["sunflower_listing_classification"] = classification
            extra_count = int(classification["extra_count"])
            if extra_count:
                sunflower_rows_with_extras += 1
                sunflower_max_extra_count = max(sunflower_max_extra_count, extra_count)
            sunflower_johnson_covered_extras += int(
                classification["johnson_covered_extra_count"]
            )
            for profile, count in classification["extra_profile_histogram"].items():
                sunflower_extra_profile_summary[profile] += int(count)
            for profile, count in classification["extra_parameter_histogram"].items():
                sunflower_extra_parameter_summary[profile] += int(count)
        rows.append(row)
        max_quotient = max(max_quotient, quotient)
        if primitive > max_primitive or total > max_total:
            if primitive > max_primitive:
                examples = []
            max_total = max(max_total, total)
            max_primitive = max(max_primitive, primitive)
        if primitive == max_primitive and len(examples) < max_examples:
            sample_masks = list(itertools.islice(listed.values(), max_examples))
            row = dict(row)
            row["agreement_sets_sample"] = [
                mask_to_exponents(mask, n) for mask in sample_masks
            ]
            examples.append(row)

    primitive_alert = bool(entropy["reserve_cleared"]) and max_primitive > threshold
    rows.sort(key=lambda row: (int(row["primitive"]), int(row["list_size"])), reverse=True)
    johnson_report = johnson_bound_report(johnson_profile, max_total, max_primitive)
    return {
        "status": "EXPERIMENTAL/FULL_LIST_SAMPLE_SCAN",
        "mode": "sample",
        "params": {"p": p, "n": n, "k": k, "s": s, "decoder": decoder, **entropy},
        "johnson_full_list_profile": johnson_profile,
        "words_scanned": len(rows),
        "max_list_size": max_total,
        "max_primitive_exact": max_primitive,
        "max_quotient_budget": max_quotient,
        "primitive_alert_threshold": round(threshold, 6),
        "primitive_alert": primitive_alert,
        **johnson_report,
        "top_rows": rows[: min(12, len(rows))],
        "max_primitive_examples": examples,
        "sunflower_summary": {
            "rows": sunflower_rows,
            "rows_with_extras": sunflower_rows_with_extras,
            "max_extra_count": sunflower_max_extra_count,
            "johnson_covered_extra_count": sunflower_johnson_covered_extras,
            "extra_profile_summary": dict(sorted(sunflower_extra_profile_summary.items())),
            "extra_parameter_summary": dict(
                sorted(sunflower_extra_parameter_summary.items())
            ),
        },
    }


def seed_sweep_scan(
    p: int,
    n: int,
    k: int,
    s: int,
    epsilon: float,
    alert_power: float,
    samples: int,
    seed_start: int,
    seed_count: int,
    sunflower_count: int,
    decoder: str,
    max_examples: int,
) -> dict[str, object]:
    seed_results = [
        sample_scan(
            p,
            n,
            k,
            s,
            epsilon,
            alert_power,
            samples,
            seed,
            sunflower_count,
            decoder,
            max_examples,
        )
        for seed in range(seed_start, seed_start + seed_count)
    ]
    if not seed_results:
        raise ValueError("seed_count must be positive")

    entropy = entropy_report(p, n, k, s, epsilon)
    johnson_profile = johnson_full_list_profile(n, k, s)
    max_list_size = max(int(result["max_list_size"]) for result in seed_results)
    max_primitive = max(int(result["max_primitive_exact"]) for result in seed_results)
    max_quotient = max(int(result["max_quotient_budget"]) for result in seed_results)
    primitive_alert = any(bool(result["primitive_alert"]) for result in seed_results)
    sunflower_rows = 0
    sunflower_rows_with_extras = 0
    sunflower_max_extra_count = 0
    sunflower_johnson_covered_extras = 0
    profile_summary: Counter[str] = Counter()
    parameter_summary: Counter[str] = Counter()
    top_seed_rows: list[dict[str, object]] = []
    for seed, result in zip(range(seed_start, seed_start + seed_count), seed_results, strict=True):
        sunflower_summary = result["sunflower_summary"]
        assert isinstance(sunflower_summary, dict)
        sunflower_rows += int(sunflower_summary["rows"])
        sunflower_rows_with_extras += int(sunflower_summary["rows_with_extras"])
        sunflower_max_extra_count = max(
            sunflower_max_extra_count,
            int(sunflower_summary["max_extra_count"]),
        )
        sunflower_johnson_covered_extras += int(
            sunflower_summary.get("johnson_covered_extra_count", 0)
        )
        for profile, count in sunflower_summary["extra_profile_summary"].items():
            profile_summary[str(profile)] += int(count)
        for profile, count in sunflower_summary["extra_parameter_summary"].items():
            parameter_summary[str(profile)] += int(count)
        top_rows = result["top_rows"]
        assert isinstance(top_rows, list)
        top_seed_rows.append({
            "seed": seed,
            "max_list_size": result["max_list_size"],
            "max_primitive_exact": result["max_primitive_exact"],
            "max_quotient_budget": result["max_quotient_budget"],
            "primitive_alert": result["primitive_alert"],
            "top_row": top_rows[0] if top_rows else None,
        })
    top_seed_rows.sort(
        key=lambda row: (
            int(row["max_primitive_exact"]),
            int(row["max_list_size"]),
        ),
        reverse=True,
    )
    return {
        "status": "EXPERIMENTAL/FULL_LIST_SUNFLOWER_SEED_SWEEP",
        "mode": "seed-sweep",
        "params": {
            "p": p,
            "n": n,
            "k": k,
            "s": s,
            "decoder": decoder,
            "seed_start": seed_start,
            "seed_count": seed_count,
            "sunflowers_per_seed": sunflower_count,
            **entropy,
        },
        "johnson_full_list_profile": johnson_profile,
        "words_scanned": sum(int(result["words_scanned"]) for result in seed_results),
        "max_list_size": max_list_size,
        "max_primitive_exact": max_primitive,
        "max_quotient_budget": max_quotient,
        "primitive_alert_threshold": n ** alert_power,
        "primitive_alert": primitive_alert,
        **johnson_bound_report(johnson_profile, max_list_size, max_primitive),
        "top_seed_rows": top_seed_rows[:max_examples],
        "sunflower_summary": {
            "rows": sunflower_rows,
            "rows_with_extras": sunflower_rows_with_extras,
            "max_extra_count": sunflower_max_extra_count,
            "johnson_covered_extra_count": sunflower_johnson_covered_extras,
            "extra_profile_summary": dict(sorted(profile_summary.items())),
            "extra_parameter_summary": dict(sorted(parameter_summary.items())),
        },
    }


def parse_case(raw: str) -> tuple[int, int, int, int]:
    parts = [int(part.strip()) for part in raw.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--case must have form p,n,k,s")
    return parts[0], parts[1], parts[2], parts[3]


def default_exact_cases() -> list[tuple[int, int, int, int]]:
    return [
        (5, 4, 2, 3),
        (7, 6, 3, 5),
        (11, 10, 5, 9),
        (13, 12, 6, 10),
        (17, 16, 8, 13),
    ]


def default_sample_cases() -> list[tuple[int, int, int, int]]:
    return [
        (17, 16, 8, 11),
        (17, 16, 8, 12),
        (17, 16, 6, 10),
        (97, 16, 8, 10),
    ]


def print_human(results: list[dict[str, object]]) -> None:
    header = "mode            p   n   k   s   sig  r   reserve  maxL  maxQ1  maxQB  alert"
    print(header)
    print("-" * len(header))
    for result in results:
        params = result["params"]
        assert isinstance(params, dict)
        print(
            f"{str(result['mode']):<15} "
            f"{params['p']:<3} {params['n']:<3} {params['k']:<3} {params['s']:<3} "
            f"{params['sigma']:<4} {params['radius']:<3} "
            f"{str(params['reserve_cleared']):<7} "
            f"{result['max_list_size']:>5} "
            f"{result['max_primitive_exact']:>6} "
            f"{result['max_quotient_budget']:>6} "
            f"{str(result['primitive_alert']):<5}"
        )
    reserve = [result for result in results if result["params"]["reserve_cleared"]]
    alerts = [result for result in reserve if result["primitive_alert"]]
    print()
    print(f"reserve-cleared scans: {len(reserve)}")
    print(f"reserve-cleared primitive alerts: {len(alerts)}")
    print(
        "max primitive in reserve-cleared scans: "
        + str(max((int(result["max_primitive_exact"]) for result in reserve), default=0))
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--exact-case", action="append", type=parse_case)
    parser.add_argument("--sample-case", action="append", type=parse_case)
    parser.add_argument("--skip-exact", action="store_true")
    parser.add_argument("--skip-sample", action="store_true")
    parser.add_argument("--max-ball", type=int, default=3_000_000)
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--sunflowers", type=int, default=3)
    parser.add_argument(
        "--seed-sweep-count",
        type=int,
        default=0,
        help="if positive, aggregate sample mode over this many consecutive seeds",
    )
    parser.add_argument(
        "--decoder",
        choices=["auto", "k-subset", "support"],
        default="auto",
        help="decoder for sample mode; support enumerates s-subsets",
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--epsilon", type=float, default=0.0)
    parser.add_argument("--alert-power", type=float, default=1.0)
    parser.add_argument("--max-examples", type=int, default=2)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    results: list[dict[str, object]] = []
    if not args.skip_exact:
        for p, n, k, s in args.exact_case or default_exact_cases():
            results.append(
                exact_syndrome_scan(
                    p,
                    n,
                    k,
                    s,
                    args.epsilon,
                    args.alert_power,
                    args.max_ball,
                    args.max_examples,
                )
            )
    if not args.skip_sample:
        for p, n, k, s in args.sample_case or default_sample_cases():
            if args.seed_sweep_count > 0:
                results.append(
                    seed_sweep_scan(
                        p,
                        n,
                        k,
                        s,
                        args.epsilon,
                        args.alert_power,
                        args.samples,
                        args.seed,
                        args.seed_sweep_count,
                        args.sunflowers,
                        args.decoder,
                        args.max_examples,
                    )
                )
            else:
                results.append(
                    sample_scan(
                        p,
                        n,
                        k,
                        s,
                        args.epsilon,
                        args.alert_power,
                        args.samples,
                        args.seed,
                        args.sunflowers,
                        args.decoder,
                        args.max_examples,
                    )
                )

    if args.json:
        print(json.dumps({"results": results}, indent=2, sort_keys=True))
    else:
        print_human(results)
    return 1 if any(result["primitive_alert"] for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
