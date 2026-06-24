#!/usr/bin/env python3
"""Stress tests for the exact L2 sharp interleaved-list target.

This verifier is deliberately small.  It tests the part of L2 that is not
settled by the support-intersection bridge: over-agreement can create
interleaved mass, so the falsification target is whether that mass can grow like
a Cartesian product rather than like a polynomial support-overlap codegree.

The script checks seven finite objects.

1. The all-remainder quotient packet count used as Quot_rem_mu in the target.
2. The Johnson-shell weights used in the codegree reduction.
3. The abstract K_{m,m} grid over-agreement design and its size formula.
4. An explicit dithered all-remainder quotient packet with M not dividing k.
5. The dyadic active-scale clearance criterion for small dimension dithers.
6. The regular/row-irregular split of the interleaved support count.
7. A realized Reed-Solomon K_{2,2} gluing over a prime-field multiplicative
   subgroup, computed by exact list enumeration, together with its punctured
   codegree profile.

Standard library only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from math import ceil, comb, log


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def e_empty(r_size: int, b_size: int, mu: int) -> int:
    """# of mu ordered b-subsets of [r_size] with empty common intersection."""
    if b_size < 0 or b_size > r_size:
        return 0
    return sum(
        (-1) ** j * comb(r_size, j) * comb(r_size - j, b_size - j) ** mu
        for j in range(b_size + 1)
    )


def h_thresh(a: int, tau: int, fiber_size: int) -> int:
    return ceil_div(a - tau, fiber_size) if a > tau else 0


def aligned_quotient_packet(
    quotient_order: int,
    ell: int,
    mu: int,
    a: int,
    tau: int,
    fiber_size: int,
) -> int:
    """Exact aligned quotient-core count L_mu(a,tau)."""
    q_minus_omitted = quotient_order - 1
    h_val = h_thresh(a, tau, fiber_size)
    if h_val > ell:
        return 0
    return sum(
        comb(q_minus_omitted, c)
        * e_empty(q_minus_omitted - c, ell - c, mu)
        for c in range(max(h_val, 0), ell + 1)
    )


def aligned_quotient_budget(n: int, k: int, a: int, mu: int) -> dict:
    """A concrete conservative aligned quotient budget.

    For every subgroup fiber size M dividing both n and k, take the worst slack
    overlap tau in [0,M-1] and sum the resulting aligned packet counts.  This is
    intentionally a budget, not a claim that all packets are disjoint.
    """
    packets = []
    total = 0
    for fiber_size in range(2, min(n, k) + 1):
        if n % fiber_size or k % fiber_size:
            continue
        quotient_order = n // fiber_size
        ell = k // fiber_size
        if ell <= 0 or ell > quotient_order - 1:
            continue
        candidates = [
            aligned_quotient_packet(quotient_order, ell, mu, a, tau, fiber_size)
            for tau in range(fiber_size)
        ]
        best = max(candidates)
        best_tau = candidates.index(best)
        if best:
            packets.append(
                {
                    "M": fiber_size,
                    "N": quotient_order,
                    "ell": ell,
                    "tau": best_tau,
                    "packet": best,
                }
            )
            total += best
    return {"total": total, "packets": packets}


def remainder_quotient_budget(n: int, k: int, a: int, mu: int) -> dict:
    """Conservative aligned quotient budget for all remainders.

    For M | n with M > a-k, write a = M*ell + u, 0 <= u < M.  The quotient-core
    packet uses ell full non-omitted M-cosets plus u points in one omitted
    M-coset.  When M | k this specializes to the previous divisible packet.
    """
    packets = []
    total = 0
    sigma = a - k
    if sigma < 0:
        raise ValueError("expected a >= k")
    for fiber_size in range(2, n + 1):
        if n % fiber_size or fiber_size <= sigma:
            continue
        quotient_order = n // fiber_size
        q_minus_omitted = quotient_order - 1
        ell = a // fiber_size
        partial = a - fiber_size * ell
        if ell <= 0 or ell > q_minus_omitted:
            continue
        candidates = [
            aligned_quotient_packet(
                quotient_order, ell, mu, a, tau, fiber_size
            )
            for tau in range(partial + 1)
        ]
        best = max(candidates)
        best_tau = candidates.index(best)
        if best:
            packets.append(
                {
                    "M": fiber_size,
                    "N": quotient_order,
                    "ell": ell,
                    "partial": partial,
                    "tau": best_tau,
                    "packet": best,
                    "divides_k": k % fiber_size == 0,
                }
            )
            total += best
    return {"total": total, "packets": packets}


def active_remainder_scales(n: int, k: int, a: int) -> list[int]:
    """Scales with a nonempty all-remainder quotient packet."""
    sigma = a - k
    return [
        fiber_size
        for fiber_size in range(2, n + 1)
        if n % fiber_size == 0
        and fiber_size > sigma
        and (a // fiber_size) > 0
        and (a // fiber_size) <= n // fiber_size - 1
    ]


def next_power_of_two_above(x: int) -> int:
    power = 1
    while power <= x:
        power *= 2
    return power


def dyadic_remainder_dither_scan(
    n: int, k0: int, sigma: int, max_r: int, mu: int
) -> dict:
    """Scan k=k0-r and record all-remainder active scales."""
    threshold = next_power_of_two_above(sigma)
    rows = []
    for r in range(max_r + 1):
        k = k0 - r
        if k <= 0:
            continue
        a = k + sigma
        active = active_remainder_scales(n, k, a)
        budget = remainder_quotient_budget(n, k, a, mu)
        rows.append(
            {
                "r": r,
                "k": k,
                "a": a,
                "active_M": active,
                "budget_total": budget["total"],
            }
        )
    first_clear = next((row["r"] for row in rows if not row["active_M"]), None)
    return {
        "n": n,
        "k0": k0,
        "sigma": sigma,
        "mu": mu,
        "next_power_above_sigma": threshold,
        "predicted_clearance_condition": f"a < {threshold}",
        "first_clear_r": first_clear,
        "rows": rows,
    }


def primitive_root(p: int) -> int:
    phi = p - 1
    factors = []
    x = phi
    d = 2
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root found for p={p}")


def subgroup(p: int, n: int) -> list[int]:
    if (p - 1) % n:
        raise ValueError(f"n={n} does not divide p-1={p-1}")
    gen = pow(primitive_root(p), (p - 1) // n, p)
    out = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * gen) % p
    if len(set(out)) != n:
        raise ValueError("subgroup generator has wrong order")
    return out


def eval_poly(coeffs: tuple[int, ...], x: int, p: int) -> int:
    total = 0
    power = 1
    for c in coeffs:
        total = (total + c * power) % p
        power = (power * x) % p
    return total


def trim_poly(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def poly_degree(poly: list[int]) -> int:
    return len(trim_poly(poly[:])) - 1


def poly_add(a: list[int], b: list[int], p: int, sign: int = 1) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i, coeff in enumerate(a):
        out[i] = (out[i] + coeff) % p
    for i, coeff in enumerate(b):
        out[i] = (out[i] + sign * coeff) % p
    return trim_poly(out)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            out[i + j] = (out[i + j] + ca * cb) % p
    return trim_poly(out)


def monomial(power: int, coeff: int = 1) -> list[int]:
    out = [0] * (power + 1)
    out[power] = coeff
    return out


def poly_from_roots(p: int, roots: list[int]) -> list[int]:
    out = [1]
    for root in roots:
        out = poly_mul(out, [(-root) % p, 1], p)
    return out


def x_power_minus_alpha(power: int, alpha: int, p: int) -> list[int]:
    return trim_poly([(-alpha) % p] + [0] * (power - 1) + [1])


def all_codewords(p: int, h_values: list[int], k: int) -> list[tuple[int, ...]]:
    return [
        tuple(eval_poly(coeffs, x, p) for x in h_values)
        for coeffs in itertools.product(range(p), repeat=k)
    ]


def vanish_values(p: int, h_values: list[int], root_indices: list[int]) -> tuple[int, ...]:
    vals = []
    roots = [h_values[i] for i in root_indices]
    for x in h_values:
        y = 1
        for r in roots:
            y = (y * (x - r)) % p
        vals.append(y)
    return tuple(vals)


def choose_filler(p: int, forbidden: set[int]) -> int:
    for y in range(p):
        if y not in forbidden:
            return y
    raise ValueError("field too small to choose filler")


def support_families(word: tuple[int, ...], codewords: list[tuple[int, ...]], a: int) -> list[frozenset[int]]:
    supports = []
    seen = set()
    for cw in codewords:
        supp = frozenset(i for i, y in enumerate(word) if cw[i] == y)
        if len(supp) >= a and supp not in seen:
            supports.append(supp)
            seen.add(supp)
    return supports


def interleaved_count(families: list[list[frozenset[int]]], a: int) -> int:
    count = 0
    for supports in itertools.product(*families):
        common = set(supports[0])
        for supp in supports[1:]:
            common &= supp
            if len(common) < a:
                break
        if len(common) >= a:
            count += 1
    return count


def regular_irregular_profile(families: list[list[frozenset[int]]], a: int) -> dict:
    """Split interleaved tuples by exact-row regularity.

    A regular tuple has every row support of size exactly a. Then the common
    intersection condition forces all row supports to be the same a-set. Every
    other listed tuple has at least one row support of size >a and belongs to
    the row-irregular shell controlled by the codegree reduction.
    """
    common_profile: dict[int, int] = {}
    regular = 0
    row_irregular = 0
    common_overagreement = 0
    regular_diagonal = True
    for supports in itertools.product(*families):
        common = set(supports[0])
        for supp in supports[1:]:
            common &= supp
            if len(common) < a:
                break
        common_size = len(common)
        if common_size < a:
            continue
        common_profile[common_size] = common_profile.get(common_size, 0) + 1
        if all(len(supp) == a for supp in supports):
            regular += 1
            regular_diagonal = regular_diagonal and len(set(supports)) == 1
        else:
            row_irregular += 1
        if common_size > a:
            common_overagreement += 1
    total = regular + row_irregular
    return {
        "regular_exact_row_count": regular,
        "row_irregular_count": row_irregular,
        "common_overagreement_count": common_overagreement,
        "total": total,
        "regular_diagonal": regular_diagonal,
        "common_intersection_profile": dict(sorted(common_profile.items())),
    }


def punctured_johnson_bound(s: int, k: int, a: int) -> dict:
    """Elementary pairwise-overlap bound for an [s,k] punctured RS code.

    Distinct degree-<k codewords agree on at most k-1 puncture points.  If L
    agreement supports of size >=a have pairwise overlaps <=k-1, incidence
    counting gives L <= s(s-k+1)/(a^2-s(k-1)) when the denominator is positive.
    """
    if 2 * a > s + k - 1:
        return {"mode": "unique", "bound": 1, "denominator": None}
    denom = a * a - s * (k - 1)
    if denom <= 0:
        return {"mode": "none", "bound": None, "denominator": denom}
    numerator = s * (s - k + 1)
    return {
        "mode": "johnson",
        "bound": numerator // denom,
        "numerator": numerator,
        "denominator": denom,
    }


def johnson_anchor_threshold(k: int, a: int) -> dict:
    """First anchor support size not controlled by punctured Johnson."""
    if k <= 1:
        return {
            "k": k,
            "a": a,
            "sigma": a - k,
            "threshold": None,
            "johnson_controls_through": None,
            "excess_over_a": None,
            "formula_excess": None,
        }
    threshold = ceil_div(a * a, k - 1)
    sigma = a - k
    formula_excess = ceil_div(a * (sigma + 1), k - 1)
    return {
        "k": k,
        "a": a,
        "sigma": sigma,
        "threshold": threshold,
        "johnson_controls_through": threshold - 1,
        "excess_over_a": threshold - a,
        "formula_excess": formula_excess,
    }


def two_row_codegree_profile(families: list[list[frozenset[int]]], a: int) -> dict:
    """Return row-1 anchored punctured-list/codegree data for two support families."""
    row1, row2 = families
    inners = [
        sum(1 for supp2 in row2 if len(supp1 & supp2) >= a)
        for supp1 in row1
    ]
    return {
        "inner_codegrees": inners,
        "codegree_sum": sum(inners),
        "max_inner_codegree": max(inners) if inners else 0,
        "all_inner_unique": all(value <= 1 for value in inners),
    }


def support_size_histogram(family: list[frozenset[int]]) -> dict[int, int]:
    hist: dict[int, int] = {}
    for supp in family:
        hist[len(supp)] = hist.get(len(supp), 0) + 1
    return dict(sorted(hist.items()))


def exact_a_locator_count(family: list[frozenset[int]], a: int) -> int:
    """Count exact a-subsets lying in full agreement supports."""
    return sum(comb(len(supp), a) for supp in family if len(supp) >= a)


def cumulative_list_size(family: list[frozenset[int]], threshold: int) -> int:
    return sum(1 for supp in family if len(supp) >= threshold)


def johnson_shell_weight(n: int, k: int, a: int, power: int = 1) -> dict:
    """Total Johnson weight across controlled support-size shells."""
    if power < 1:
        raise ValueError("power must be positive")
    threshold = johnson_anchor_threshold(k, a)
    threshold_value = threshold["threshold"]
    if threshold_value is None:
        return {
            "johnson_threshold": threshold,
            "power": power,
            "controlled_shells": [],
            "exact_weight_sum": 0,
            "harmonic_upper_bound": None,
        }
    controlled_max = min(n, threshold_value - 1)
    shells = []
    exact_weight_sum = 0
    for s in range(a, controlled_max + 1):
        profile = punctured_johnson_bound(s, k, a)
        if profile["bound"] is None:
            raise ValueError("controlled shell has no Johnson bound")
        shells.append(
            {
                "support_size": s,
                "mode": profile["mode"],
                "weight": profile["bound"],
                "powered_weight": profile["bound"] ** power,
            }
        )
        exact_weight_sum += profile["bound"] ** power
    harmonic_upper_bound = ceil((n ** (2 * power)) * (2 + log(max(2, n))))
    return {
        "johnson_threshold": threshold,
        "power": power,
        "controlled_shells": shells,
        "exact_weight_sum": exact_weight_sum,
        "harmonic_upper_bound": harmonic_upper_bound,
    }


def l1_shell_reduction_bound(
    families: list[list[frozenset[int]]], n: int, k: int, a: int
) -> dict:
    """Two-row bound using only one-row cumulative shell list sizes."""
    row1, row2 = families
    weight = johnson_shell_weight(n, k, a)
    threshold = weight["johnson_threshold"]["threshold"]
    controlled_max = min(n, threshold - 1) if threshold is not None else n
    if controlled_max >= a:
        row1_max_controlled_list = max(
            cumulative_list_size(row1, t) for t in range(a, controlled_max + 1)
        )
    else:
        row1_max_controlled_list = 0
    row1_tail_list = (
        cumulative_list_size(row1, threshold) if threshold is not None else 0
    )
    row1_base_list = cumulative_list_size(row1, a)
    row2_base_list = cumulative_list_size(row2, a)
    controlled_bound = row1_max_controlled_list * weight["exact_weight_sum"]
    tail_bound = row1_tail_list * row2_base_list
    return {
        "johnson_shell_weight": weight,
        "row1_base_list": row1_base_list,
        "row1_max_controlled_list": row1_max_controlled_list,
        "row1_tail_list": row1_tail_list,
        "row2_base_list": row2_base_list,
        "controlled_bound": controlled_bound,
        "tail_bound": tail_bound,
        "total_bound": controlled_bound + tail_bound,
    }


def shell_codegree_bound(families: list[list[frozenset[int]]], k: int, a: int) -> dict:
    """Deterministic two-row shell bound from punctured Johnson plus tail."""
    row1, row2 = families
    threshold = johnson_anchor_threshold(k, a)
    threshold_value = threshold["threshold"]
    row1_hist = support_size_histogram(row1)
    controlled_terms = []
    controlled_bound = 0
    tail_count = 0
    for s, count in row1_hist.items():
        if threshold_value is None or s < threshold_value:
            profile = punctured_johnson_bound(s, k, a)
            if profile["bound"] is None:
                raise ValueError("shell below Johnson threshold was not controlled")
            contribution = count * profile["bound"]
            controlled_terms.append(
                {
                    "support_size": s,
                    "count": count,
                    "mode": profile["mode"],
                    "per_anchor_bound": profile["bound"],
                    "contribution": contribution,
                }
            )
            controlled_bound += contribution
        else:
            tail_count += count

    row2_list_size = len(row2)
    tail_trivial_bound = tail_count * row2_list_size
    exact_count = exact_a_locator_count(row1, a)
    if threshold_value is None or threshold_value > max((len(s) for s in row1), default=0):
        tail_count_from_exact_a = 0
    else:
        tail_count_from_exact_a = exact_count // comb(threshold_value, a)
    return {
        "row1_support_histogram": row1_hist,
        "row2_list_size": row2_list_size,
        "johnson_threshold": threshold,
        "controlled_terms": controlled_terms,
        "controlled_bound": controlled_bound,
        "tail_count": tail_count,
        "tail_trivial_bound": tail_trivial_bound,
        "exact_a_locator_count_row1": exact_count,
        "tail_count_bound_from_exact_a": tail_count_from_exact_a,
        "total_bound": controlled_bound + tail_trivial_bound,
    }


def kmm_grid_design(k: int, a: int, m: int) -> dict:
    """Abstract K_{m,m} grid design obeying the same-row RS overlap cap."""
    overlap_cap = k - 1
    cell_size = a - overlap_cap
    if cell_size <= 0:
        raise ValueError("need a >= k for a nontrivial design")
    n_min = overlap_cap + m * m * cell_size
    row_support_size = overlap_cap + m * cell_size
    return {
        "k": k,
        "a": a,
        "m": m,
        "overlap_cap": overlap_cap,
        "cell_size": cell_size,
        "minimum_n": n_min,
        "row_support_size": row_support_size,
        "interleaved_edges": m * m,
        "grid_edges_at_n_min": (n_min - overlap_cap) // cell_size,
    }


def realized_dithered_quotient_packet() -> dict:
    """Construct an all-remainder quotient packet with M not dividing k."""
    p, n, k, a, fiber_size = 17, 16, 7, 9, 4
    sigma = a - k
    ell = a // fiber_size
    partial = a - fiber_size * ell
    quotient_order = n // fiber_size
    h_values = subgroup(p, n)
    cosets: dict[int, list[int]] = {}
    for x in h_values:
        cosets.setdefault(pow(x, fiber_size, p), []).append(x)
    quotient_values = list(cosets)
    omitted = quotient_values[0]
    partial_points = cosets[omitted][:partial]
    l_t = poly_from_roots(p, partial_points)
    y_poly = poly_mul(monomial(fiber_size * ell), l_t, p)

    rows = []
    polynomials = []
    advertised_supports = []
    for quotient_subset in itertools.combinations(quotient_values[1:], ell):
        l_a = [1]
        support = set(partial_points)
        for alpha in quotient_subset:
            l_a = poly_mul(l_a, x_power_minus_alpha(fiber_size, alpha, p), p)
            support.update(cosets[alpha])
        p_poly = poly_mul(
            l_t,
            poly_add(monomial(fiber_size * ell), l_a, p, sign=-1),
            p,
        )
        agreement = [
            x
            for x in h_values
            if eval_poly(tuple(p_poly), x, p) == eval_poly(tuple(y_poly), x, p)
        ]
        rows.append(
            {
                "quotient_subset": quotient_subset,
                "degree": poly_degree(p_poly),
                "advertised_support_size": len(support),
                "agreement_size": len(agreement),
                "advertised_support_contained": support.issubset(set(agreement)),
            }
        )
        polynomials.append(tuple(trim_poly(p_poly[:])))
        advertised_supports.append(frozenset(support))

    expected_count = comb(quotient_order - 1, ell)
    formula_count = aligned_quotient_packet(
        quotient_order, ell, mu=2, a=a, tau=partial, fiber_size=fiber_size
    )
    return {
        "p": p,
        "n": n,
        "k": k,
        "a": a,
        "sigma": sigma,
        "M": fiber_size,
        "M_divides_k": k % fiber_size == 0,
        "N": quotient_order,
        "ell": ell,
        "partial": partial,
        "constructed_count": len(rows),
        "expected_diagonal_count": expected_count,
        "formula_count_mu2_tau_partial": formula_count,
        "distinct_polynomials": len(set(polynomials)),
        "distinct_advertised_supports": len(set(advertised_supports)),
        "max_degree": max(row["degree"] for row in rows),
        "min_agreement": min(row["agreement_size"] for row in rows),
        "all_degrees_below_k": all(row["degree"] < k for row in rows),
        "all_advertised_supports_size_a": all(
            row["advertised_support_size"] == a for row in rows
        ),
        "all_advertised_supports_contained": all(
            row["advertised_support_contained"] for row in rows
        ),
        "rows": rows,
    }


def realized_rs_k22() -> dict:
    """Exact RS enumeration for a prime-field K_{2,2} gluing witness."""
    p, n, k, a, m = 29, 14, 3, 5, 2
    h_values = subgroup(p, n)
    codewords = all_codewords(p, h_values, k)
    overlap_cap = k - 1
    core = list(range(overlap_cap))
    cell_size = a - overlap_cap
    cells = []
    cursor = overlap_cap
    for _ in range(m * m):
        cells.append(list(range(cursor, cursor + cell_size)))
        cursor += cell_size
    assert cursor == n

    vanish = vanish_values(p, h_values, core)
    # Row-1 codewords c_i and row-2 codewords d_j.  All agree on the core and
    # otherwise differ by scalar multiples of the same vanishing polynomial.
    c_rows = [tuple((lam * y) % p for y in vanish) for lam in (1, 2)]
    d_rows = [tuple((lam * y) % p for y in vanish) for lam in (3, 4)]

    word1 = [None] * n
    word2 = [None] * n
    for idx in core:
        word1[idx] = 0
        word2[idx] = 0
    for i in range(m):
        for j in range(m):
            for idx in cells[i * m + j]:
                word1[idx] = c_rows[i][idx]
                word2[idx] = d_rows[j][idx]
    for idx in range(n):
        if word1[idx] is None:
            word1[idx] = choose_filler(p, {cw[idx] for cw in c_rows})
        if word2[idx] is None:
            word2[idx] = choose_filler(p, {cw[idx] for cw in d_rows})

    families = [
        support_families(tuple(word1), codewords, a),
        support_families(tuple(word2), codewords, a),
    ]
    interleaved = interleaved_count(families, a)
    product_bound = len(families[0]) * len(families[1])
    max_base = max(len(families[0]), len(families[1]))
    support_sizes = [[len(s) for s in fam] for fam in families]
    regular_profile = regular_irregular_profile(families, a)
    codegree_profile = two_row_codegree_profile(families, a)
    shell_bound = shell_codegree_bound(families, k, a)
    l1_reduction_bound = l1_shell_reduction_bound(families, n, k, a)
    johnson_profiles = [
        punctured_johnson_bound(len(supp), k, a)
        for supp in families[0]
    ]
    threshold = johnson_anchor_threshold(k, a)
    large_anchor_flags = [
        threshold["threshold"] is not None and len(supp) >= threshold["threshold"]
        for supp in families[0]
    ]
    johnson_ok = all(
        profile["bound"] is not None and inner <= profile["bound"]
        for inner, profile in zip(
            codegree_profile["inner_codegrees"], johnson_profiles
        )
    )

    return {
        "p": p,
        "n": n,
        "k": k,
        "a": a,
        "m": m,
        "base_lists": [len(families[0]), len(families[1])],
        "max_base": max_base,
        "product_bound": product_bound,
        "interleaved": interleaved,
        "mass_creation": interleaved > max_base,
        "saving_vs_cartesian": interleaved / product_bound if product_bound else None,
        "support_sizes": support_sizes,
        "common_intersection_profile": regular_profile[
            "common_intersection_profile"
        ],
        "regular_irregular_profile": regular_profile,
        "punctured_codegree_profile": codegree_profile,
        "codegree_identity_holds": codegree_profile["codegree_sum"] == interleaved,
        "shell_codegree_bound": shell_bound,
        "l1_shell_reduction_bound": l1_reduction_bound,
        "punctured_johnson_profiles": johnson_profiles,
        "johnson_anchor_threshold": threshold,
        "large_anchor_flags": large_anchor_flags,
        "punctured_johnson_ok": johnson_ok,
        "kmm_grid_model": kmm_grid_design(k, a, m),
    }


def run() -> dict:
    quotient_example = aligned_quotient_budget(n=64, k=16, a=18, mu=2)
    remainder_quotient_example = remainder_quotient_budget(n=64, k=16, a=18, mu=2)
    dithered_quotient_example = {
        "divisible_only": aligned_quotient_budget(n=64, k=15, a=17, mu=2),
        "all_remainders": remainder_quotient_budget(n=64, k=15, a=17, mu=2),
    }
    active_scale_examples = {
        "divisible": active_remainder_scales(n=64, k=16, a=18),
        "dithered": active_remainder_scales(n=64, k=15, a=17),
    }
    dyadic_dither_scan = dyadic_remainder_dither_scan(
        n=64, k0=16, sigma=2, max_r=15, mu=2
    )
    threshold_example = johnson_anchor_threshold(k=16, a=18)
    shell_weight_example = johnson_shell_weight(n=64, k=16, a=18)
    fixed_arity_shell_weight_example = johnson_shell_weight(
        n=64, k=16, a=18, power=2
    )
    designs = [kmm_grid_design(k=3, a=5, m=m) for m in (2, 3, 4, 5)]
    dithered_witness = realized_dithered_quotient_packet()
    witness = realized_rs_k22()
    checks = {
        "quotient_budget_nonnegative": quotient_example["total"] >= 0,
        "remainder_budget_extends_divisible": remainder_quotient_example["total"]
        >= quotient_example["total"],
        "dithered_remainder_budget_detects_packets": dithered_quotient_example[
            "all_remainders"
        ]["total"]
        > dithered_quotient_example["divisible_only"]["total"],
        "active_remainder_scales_match_budget": active_scale_examples[
            "dithered"
        ]
        == [
            packet["M"]
            for packet in dithered_quotient_example["all_remainders"]["packets"]
        ],
        "dyadic_dither_scan_starts_active": dyadic_dither_scan["rows"][0][
            "active_M"
        ]
        == [4, 8, 16],
        "dyadic_dither_scan_first_clear": dyadic_dither_scan["first_clear_r"]
        == 15,
        "dyadic_dither_scan_clearance_condition": all(
            bool(row["active_M"])
            == (row["a"] >= dyadic_dither_scan["next_power_above_sigma"])
            for row in dyadic_dither_scan["rows"]
        ),
        "dithered_quotient_witness_count": dithered_witness[
            "constructed_count"
        ]
        == dithered_witness["expected_diagonal_count"]
        == dithered_witness["formula_count_mu2_tau_partial"],
        "dithered_quotient_witness_degree": dithered_witness[
            "all_degrees_below_k"
        ],
        "dithered_quotient_witness_agreement": dithered_witness[
            "all_advertised_supports_size_a"
        ]
        and dithered_witness["all_advertised_supports_contained"],
        "dithered_quotient_witness_distinct": dithered_witness[
            "distinct_polynomials"
        ]
        == dithered_witness["constructed_count"],
        "kmm_grid_formula": all(d["interleaved_edges"] == d["grid_edges_at_n_min"] for d in designs),
        "rs_witness_creates_mass": witness["mass_creation"],
        "rs_witness_realizes_k22": witness["interleaved"] == witness["product_bound"] == 4,
        "rs_witness_codegree_identity": witness["codegree_identity_holds"],
        "rs_witness_regular_irregular_split": witness[
            "regular_irregular_profile"
        ]["total"]
        == witness["interleaved"]
        and witness["regular_irregular_profile"]["regular_exact_row_count"] == 0
        and witness["regular_irregular_profile"]["row_irregular_count"]
        == witness["interleaved"],
        "rs_witness_no_common_overagreement": witness[
            "regular_irregular_profile"
        ]["common_overagreement_count"]
        == 0,
        "rs_witness_shell_bound": witness["interleaved"] <= witness["shell_codegree_bound"]["total_bound"],
        "rs_witness_l1_shell_reduction": witness["interleaved"]
        <= witness["l1_shell_reduction_bound"]["total_bound"],
        "rs_witness_l1_shell_monotonicity": witness["l1_shell_reduction_bound"][
            "row1_max_controlled_list"
        ]
        <= witness["l1_shell_reduction_bound"]["row1_base_list"],
        "rs_witness_punctured_johnson": witness["punctured_johnson_ok"],
    }
    return {
        "status": "EXPERIMENTAL / FALSIFICATION",
        "aligned_quotient_budget_example": quotient_example,
        "remainder_quotient_budget_example": remainder_quotient_example,
        "dithered_quotient_budget_example": dithered_quotient_example,
        "active_remainder_scale_examples": active_scale_examples,
        "dyadic_remainder_dither_scan": dyadic_dither_scan,
        "johnson_anchor_threshold_example": threshold_example,
        "johnson_shell_weight_example": shell_weight_example,
        "fixed_arity_johnson_shell_weight_example": fixed_arity_shell_weight_example,
        "kmm_designs": designs,
        "realized_dithered_quotient_packet": dithered_witness,
        "realized_rs_k22": witness,
        "checks": checks,
        "pass": all(checks.values()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args(argv)

    result = run()
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"L2 sharp-target stress test ({result['status']})")
        qb = result["aligned_quotient_budget_example"]
        print(f"  aligned quotient budget example: total={qb['total']}, packets={len(qb['packets'])}")
        rqb = result["remainder_quotient_budget_example"]
        print(
            "  all-remainder quotient budget example: "
            f"total={rqb['total']}, packets={len(rqb['packets'])}"
        )
        dqb = result["dithered_quotient_budget_example"]
        active = result["active_remainder_scale_examples"]
        print(
            "  dithered quotient budget example (n=64,k=15,a=17): "
            f"divisible_total={dqb['divisible_only']['total']}, "
            f"all_remainders_total={dqb['all_remainders']['total']}, "
            f"active_M={active['dithered']}"
        )
        dscan = result["dyadic_remainder_dither_scan"]
        print(
            "  dyadic all-remainder dither scan: "
            f"n={dscan['n']}, k0={dscan['k0']}, sigma={dscan['sigma']}, "
            f"next_power={dscan['next_power_above_sigma']}, "
            f"first_clear_r={dscan['first_clear_r']}"
        )
        dq_witness = result["realized_dithered_quotient_packet"]
        print(
            "  realized dithered quotient packet: "
            f"F_{dq_witness['p']}, n={dq_witness['n']}, "
            f"k={dq_witness['k']}, a={dq_witness['a']}, "
            f"M={dq_witness['M']}, ell={dq_witness['ell']}, "
            f"partial={dq_witness['partial']}, "
            f"count={dq_witness['constructed_count']}, "
            f"max_degree={dq_witness['max_degree']}, "
            f"min_agreement={dq_witness['min_agreement']}"
        )
        jt = result["johnson_anchor_threshold_example"]
        print(
            "  Johnson anchor threshold example: "
            f"k={jt['k']}, a={jt['a']}, threshold={jt['threshold']}, "
            f"controls_s<={jt['johnson_controls_through']}, "
            f"excess={jt['excess_over_a']}"
        )
        jw = result["johnson_shell_weight_example"]
        print(
            "  Johnson shell weight example: "
            f"exact={jw['exact_weight_sum']}, "
            f"harmonic_bound={jw['harmonic_upper_bound']}"
        )
        fjw = result["fixed_arity_johnson_shell_weight_example"]
        print(
            "  fixed-arity Johnson shell weight example: "
            f"power={fjw['power']}, exact={fjw['exact_weight_sum']}, "
            f"harmonic_bound={fjw['harmonic_upper_bound']}"
        )
        print("  K_{m,m} abstract designs:")
        for d in result["kmm_designs"]:
            print(
                f"    m={d['m']}: n_min={d['minimum_n']}, "
                f"edges={d['interleaved_edges']}, grid_edges={d['grid_edges_at_n_min']}"
            )
        w = result["realized_rs_k22"]
        print("  realized RS K_{2,2} witness:")
        print(
            f"    F_{w['p']}, n={w['n']}, k={w['k']}, a={w['a']}: "
            f"base={w['base_lists']}, interleaved={w['interleaved']}, "
            f"product={w['product_bound']}, creates_mass={w['mass_creation']}"
        )
        print(
            f"    punctured codegrees={w['punctured_codegree_profile']['inner_codegrees']}, "
            f"sum={w['punctured_codegree_profile']['codegree_sum']}, "
            f"max={w['punctured_codegree_profile']['max_inner_codegree']}"
        )
        reg = w["regular_irregular_profile"]
        print(
            "    regular split: "
            f"regular={reg['regular_exact_row_count']}, "
            f"row_irregular={reg['row_irregular_count']}, "
            f"common_overagreement={reg['common_overagreement_count']}, "
            f"profile={reg['common_intersection_profile']}"
        )
        print(
            f"    Johnson threshold={w['johnson_anchor_threshold']}, "
            f"large_anchor_flags={w['large_anchor_flags']}"
        )
        sb = w["shell_codegree_bound"]
        print(
            f"    shell bound={sb['total_bound']} "
            f"(controlled={sb['controlled_bound']}, tail={sb['tail_trivial_bound']}), "
            f"row1_exact_a={sb['exact_a_locator_count_row1']}, "
            f"tail_from_exact_a<={sb['tail_count_bound_from_exact_a']}"
        )
        l1b = w["l1_shell_reduction_bound"]
        print(
            f"    L1-shell reduction bound={l1b['total_bound']} "
            f"(controlled={l1b['controlled_bound']}, tail={l1b['tail_bound']}), "
            f"base_list={l1b['row1_base_list']}, "
            f"max_controlled_list={l1b['row1_max_controlled_list']}"
        )
        print(f"    punctured Johnson profiles={w['punctured_johnson_profiles']}")
        print(f"  RESULT: {'PASS' if result['pass'] else 'FAIL'}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
