#!/usr/bin/env python3
"""Stress tests for the exact L2 sharp interleaved-list target.

This verifier is deliberately small.  It tests the part of L2 that is not
settled by the support-intersection bridge: over-agreement can create
interleaved mass, so the falsification target is whether that mass can grow like
a Cartesian product rather than like a polynomial support-overlap codegree.

The script checks twenty-one finite objects.

1. The all-remainder quotient packet count used as Quot_rem_mu in the target.
2. The Johnson-shell weights used in the codegree reduction.
3. The abstract K_{m,m} grid over-agreement design and its size formula.
4. An explicit dithered all-remainder quotient packet with M not dividing k.
5. The dyadic active-scale clearance criterion for small dimension dithers.
6. The regular/row-irregular split of the interleaved support count.
7. The simultaneous feasible-support fiber behind the regular exact-row core.
8. The locator-syndrome equations defining that simultaneous fiber.
9. The equivalent weighted residue-moment equations.
10. The support-pair rank law behind the random regular-core second moment.
11. The multi-support high-overlap cluster-rank upper bound.
12. The connected high-overlap cluster count by union excess.
13. The rank-corrected ledger for low-overlap closure-component intersections.
14. A cyclic low-overlap closed-part rank-deficit family.
15. The constant locator-ratio subfamily of cyclic triangles.
16. Full-rank fixed-length cyclic necklaces in the same low-overlap model.
17. Rank-deficient fixed-length cyclic necklaces, counted by dependency data.
18. Clean simple cycles with arbitrary adjacent low-overlap edge sizes.
19. The projective functional incidence reduction for clean-cycle defects.
20. A locator-syzygy witness and pivot-forcing reduction for lower selected
   clean-cycle rank.
21. A realized Reed-Solomon K_{2,2} gluing over a prime-field multiplicative
   subgroup, computed by exact list enumeration, together with its punctured
   codegree profile.

Standard library only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from fractions import Fraction
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


def poly_scale(poly: list[int], scalar: int, p: int) -> list[int]:
    return trim_poly([(scalar * coeff) % p for coeff in poly])


def poly_divmod(
    numerator: list[int], denominator: list[int], p: int
) -> tuple[list[int], list[int]]:
    numerator = trim_poly(numerator[:])
    denominator = trim_poly(denominator[:])
    if denominator == [0]:
        raise ValueError("polynomial division by zero")
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    denominator_degree = poly_degree(denominator)
    denominator_lead_inv = pow(denominator[-1], -1, p)
    while numerator != [0] and poly_degree(numerator) >= denominator_degree:
        shift = poly_degree(numerator) - denominator_degree
        coeff = numerator[-1] * denominator_lead_inv % p
        quotient[shift] = coeff
        subtract = [0] * shift + poly_scale(denominator, coeff, p)
        numerator = poly_add(numerator, subtract, p, sign=-1)
    return trim_poly(quotient), trim_poly(numerator)


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


def support_pair_rank_profile() -> dict:
    """Brute-force the two-support feasibility rank law for one random row."""
    p, n, k, a = 7, 6, 2, 3
    h_values = subgroup(p, n)
    codewords = all_codewords(p, h_values, k)
    rows = []
    for intersection_size in range(a + 1):
        first = tuple(range(a))
        second = tuple(
            list(range(intersection_size))
            + list(range(a, a + (a - intersection_size)))
        )
        union = sorted(set(first) | set(second))
        union_index = {idx: pos for pos, idx in enumerate(union)}
        feasible_first = {
            tuple(cw[idx] for idx in first)
            for cw in codewords
        }
        feasible_second = {
            tuple(cw[idx] for idx in second)
            for cw in codewords
        }
        brute_count = 0
        for assignment in itertools.product(range(p), repeat=len(union)):
            first_values = tuple(assignment[union_index[idx]] for idx in first)
            second_values = tuple(assignment[union_index[idx]] for idx in second)
            if first_values in feasible_first and second_values in feasible_second:
                brute_count += 1
        expected_dimension = 2 * k - min(intersection_size, k)
        probability_exponent = len(union) - expected_dimension
        rows.append(
            {
                "intersection": intersection_size,
                "union_size": len(union),
                "expected_dimension": expected_dimension,
                "brute_count": brute_count,
                "expected_count": p**expected_dimension,
                "probability_exponent": probability_exponent,
                "independent_exponent": 2 * (a - k),
            }
        )
    return {
        "p": p,
        "n": n,
        "k": k,
        "a": a,
        "rows": rows,
        "all_counts_match": all(
            row["brute_count"] == row["expected_count"] for row in rows
        ),
        "below_k_independent": all(
            row["probability_exponent"] == row["independent_exponent"]
            for row in rows
            if row["intersection"] < k
        ),
        "above_k_surplus": all(
            row["probability_exponent"]
            == 2 * a - row["intersection"] - k
            for row in rows
            if row["intersection"] >= k
        ),
    }


def connected_components_count(edges: list[tuple[int, int]], vertex_count: int) -> int:
    parent = list(range(vertex_count))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    for left, right in edges:
        union(left, right)
    return len({find(idx) for idx in range(vertex_count)})


def matrix_rank_mod(matrix: list[list[int]], p: int) -> int:
    rows = [
        [entry % p for entry in row]
        for row in matrix
        if any(entry % p for entry in row)
    ]
    if not rows:
        return 0
    rank = 0
    column_count = len(rows[0])
    for column in range(column_count):
        pivot = None
        for row in range(rank, len(rows)):
            if rows[row][column] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][column], -1, p)
        rows[rank] = [(entry * inv) % p for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or rows[row][column] % p == 0:
                continue
            factor = rows[row][column] % p
            rows[row] = [
                (rows[row][idx] - factor * rows[rank][idx]) % p
                for idx in range(column_count)
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def high_overlap_components(supports: list[tuple[int, ...]], k: int) -> list[set[int]]:
    parent = list(range(len(supports)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_y] = root_x

    for i in range(len(supports)):
        for j in range(i + 1, len(supports)):
            if len(set(supports[i]) & set(supports[j])) >= k:
                union(i, j)
    components: dict[int, set[int]] = {}
    for idx in range(len(supports)):
        components.setdefault(find(idx), set()).add(idx)
    return list(components.values())


def closure_components(supports: list[tuple[int, ...]], k: int) -> list[set[int]]:
    components = high_overlap_components(supports, k)
    changed = True
    while changed:
        changed = False
        for i in range(len(components)):
            if changed:
                break
            union_i = set().union(*[set(supports[idx]) for idx in components[i]])
            for j in range(i + 1, len(components)):
                union_j = set().union(*[set(supports[idx]) for idx in components[j]])
                if len(union_i & union_j) >= k:
                    components[i] |= components[j]
                    del components[j]
                    changed = True
                    break
    return components


def component_unions(
    supports: list[tuple[int, ...]],
    components: list[set[int]],
) -> list[set[int]]:
    return [
        set().union(*[set(supports[idx]) for idx in component])
        for component in components
    ]


def component_overlap_edges(part_unions: list[set[int]]) -> list[tuple[int, int]]:
    return [
        (i, j)
        for i in range(len(part_unions))
        for j in range(i + 1, len(part_unions))
        if part_unions[i] & part_unions[j]
    ]


def is_forest(edges: list[tuple[int, int]], vertex_count: int) -> bool:
    return len(edges) == vertex_count - connected_components_count(
        edges, vertex_count
    )


def cross_constraint_rank(
    p: int,
    h_values: list[int],
    k: int,
    part_unions: list[set[int]],
) -> int:
    rows = []
    part_count = len(part_unions)
    for i in range(part_count):
        for j in range(i + 1, part_count):
            for idx in sorted(part_unions[i] & part_unions[j]):
                row = [0] * (part_count * k)
                power = 1
                x = h_values[idx]
                for degree in range(k):
                    row[i * k + degree] = (row[i * k + degree] + power) % p
                    row[j * k + degree] = (row[j * k + degree] - power) % p
                    power = (power * x) % p
                rows.append(row)
    return matrix_rank_mod(rows, p)


def feasible_assignment_count(
    p: int,
    codewords: list[tuple[int, ...]],
    supports: list[tuple[int, ...]],
) -> int:
    union = sorted(set().union(*[set(support) for support in supports]))
    union_index = {idx: pos for pos, idx in enumerate(union)}
    feasible_by_support = [
        {tuple(cw[idx] for idx in support) for cw in codewords}
        for support in supports
    ]
    count = 0
    for assignment in itertools.product(range(p), repeat=len(union)):
        if all(
            tuple(assignment[union_index[idx]] for idx in support)
            in feasible_values
            for support, feasible_values in zip(supports, feasible_by_support)
        ):
            count += 1
    return count


def support_cluster_rank_profile() -> dict:
    """Brute-force examples for the high-overlap cluster-rank upper bound."""
    p, n, k, a = 7, 6, 2, 3
    h_values = subgroup(p, n)
    codewords = all_codewords(p, h_values, k)
    examples = [
        {
            "name": "diagonal_component",
            "supports": [(0, 1, 2), (0, 1, 2), (0, 1, 2)],
        },
        {
            "name": "one_high_overlap_component",
            "supports": [(0, 1, 2), (1, 2, 3), (0, 2, 3)],
        },
        {
            "name": "mixed_high_low_path",
            "supports": [(0, 1, 2), (1, 2, 3), (3, 4, 5)],
        },
        {
            "name": "aggregate_union_merge",
            "supports": [(0, 1, 2), (0, 3, 4), (1, 3, 4)],
        },
        {
            "name": "connected_chain_four_distinct",
            "supports": [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)],
        },
        {
            "name": "low_overlap_cycle",
            "supports": [(0, 1, 2), (2, 3, 4), (0, 4, 5)],
        },
    ]
    rows = []
    for example in examples:
        supports = example["supports"]
        edges = [
            (i, j)
            for i in range(len(supports))
            for j in range(i + 1, len(supports))
            if len(set(supports[i]) & set(supports[j])) >= k
        ]
        components = connected_components_count(edges, len(supports))
        closed_components = closure_components(supports, k)
        closed_component_count = len(closed_components)
        union_size = len(set().union(*[set(support) for support in supports]))
        union_excess = union_size - a
        distinct_supports = len({frozenset(support) for support in supports})
        brute_count = feasible_assignment_count(p, codewords, supports)
        dimension_upper_bound = k * components
        closure_dimension_upper_bound = k * closed_component_count
        rows.append(
            {
                "name": example["name"],
                "supports": [list(support) for support in supports],
                "high_overlap_edges": [list(edge) for edge in edges],
                "components": components,
                "closure_components": closed_component_count,
                "union_size": union_size,
                "union_excess": union_excess,
                "distinct_supports": distinct_supports,
                "support_capacity_bound": comb(a + union_excess, a),
                "dimension_upper_bound": dimension_upper_bound,
                "closure_dimension_upper_bound": closure_dimension_upper_bound,
                "brute_count": brute_count,
                "count_upper_bound": p**dimension_upper_bound,
                "closure_count_upper_bound": p**closure_dimension_upper_bound,
                "probability_exponent_bound": union_size - dimension_upper_bound,
                "closure_probability_exponent_bound": union_size
                - closure_dimension_upper_bound,
            }
        )
    row_by_name = {row["name"]: row for row in rows}
    return {
        "p": p,
        "n": n,
        "k": k,
        "a": a,
        "rows": rows,
        "all_counts_bounded": all(
            row["brute_count"] <= row["count_upper_bound"] for row in rows
        ),
        "diagonal_component_zero_loss": row_by_name["diagonal_component"][
            "probability_exponent_bound"
        ]
        == a - k,
        "nondiagonal_connected_extra_loss": row_by_name[
            "one_high_overlap_component"
        ]["probability_exponent_bound"]
        == a - k + 1,
        "connected_union_excess_tradeoff": all(
            row["probability_exponent_bound"] == a - k + row["union_excess"]
            for row in rows
            if row["components"] == 1
        ),
        "distinct_support_capacity": all(
            row["distinct_supports"] <= row["support_capacity_bound"]
            for row in rows
        ),
        "connected_high_overlap_tight": row_by_name["one_high_overlap_component"][
            "brute_count"
        ]
        == row_by_name["one_high_overlap_component"]["count_upper_bound"],
        "connected_chain_loss": row_by_name["connected_chain_four_distinct"][
            "probability_exponent_bound"
        ]
        == a - k + row_by_name["connected_chain_four_distinct"]["union_excess"],
        "aggregate_union_closure_merges": row_by_name["aggregate_union_merge"][
            "components"
        ]
        == 2
        and row_by_name["aggregate_union_merge"]["closure_components"] == 1,
        "closure_rank_counts": all(
            row["brute_count"] <= row["closure_count_upper_bound"] for row in rows
        ),
        "aggregate_union_closure_sharpens": row_by_name["aggregate_union_merge"][
            "closure_probability_exponent_bound"
        ]
        > row_by_name["aggregate_union_merge"]["probability_exponent_bound"],
        "low_overlap_bound_can_be_loose": row_by_name["low_overlap_cycle"][
            "brute_count"
        ]
        < row_by_name["low_overlap_cycle"]["count_upper_bound"],
    }


def connected_cluster_count_profile() -> dict:
    """Count connected high-overlap support tuples by union excess."""
    n, k, a, tuple_size = 6, 2, 3, 3
    moment_q, mu = 31, 2
    supports = [tuple(support) for support in itertools.combinations(range(n), a)]
    rows_by_excess: dict[int, int] = {}
    for support_tuple in itertools.product(supports, repeat=tuple_size):
        edges = [
            (i, j)
            for i in range(tuple_size)
            for j in range(i + 1, tuple_size)
            if len(set(support_tuple[i]) & set(support_tuple[j])) >= k
        ]
        if connected_components_count(edges, tuple_size) != 1:
            continue
        union_size = len(set().union(*[set(support) for support in support_tuple]))
        union_excess = union_size - a
        rows_by_excess[union_excess] = rows_by_excess.get(union_excess, 0) + 1
    rows = []
    diagonal_scale_count = comb(n, a)
    positive_actual_ratio = Fraction(0, 1)
    positive_bound_ratio = Fraction(0, 1)
    for union_excess, count in sorted(rows_by_excess.items()):
        union_size = a + union_excess
        support_capacity = comb(union_size, a)
        upper_bound = comb(n, union_size) * support_capacity**tuple_size
        actual_ratio = Fraction(count, diagonal_scale_count * moment_q ** (mu * union_excess))
        bound_ratio = Fraction(
            upper_bound,
            diagonal_scale_count * moment_q ** (mu * union_excess),
        )
        if union_excess > 0:
            positive_actual_ratio += actual_ratio
            positive_bound_ratio += bound_ratio
        rows.append(
            {
                "union_excess": union_excess,
                "connected_tuples": count,
                "union_choices": comb(n, union_size),
                "support_capacity": support_capacity,
                "count_upper_bound": upper_bound,
                "entropy_exponent_extra": union_excess,
                "actual_relative_to_diagonal": {
                    "numerator": actual_ratio.numerator,
                    "denominator": actual_ratio.denominator,
                },
                "bound_relative_to_diagonal": {
                    "numerator": bound_ratio.numerator,
                    "denominator": bound_ratio.denominator,
                },
            }
        )
    return {
        "n": n,
        "k": k,
        "a": a,
        "tuple_size": tuple_size,
        "moment_q": moment_q,
        "mu": mu,
        "rows": rows,
        "positive_actual_relative_to_diagonal": {
            "numerator": positive_actual_ratio.numerator,
            "denominator": positive_actual_ratio.denominator,
        },
        "positive_bound_relative_to_diagonal": {
            "numerator": positive_bound_ratio.numerator,
            "denominator": positive_bound_ratio.denominator,
        },
        "all_counts_bounded": all(
            row["connected_tuples"] <= row["count_upper_bound"]
            for row in rows
        ),
        "diagonal_count_exact": rows[0]["union_excess"] == 0
        and rows[0]["connected_tuples"] == comb(n, a),
        "has_positive_excess_clusters": any(
            row["union_excess"] > 0 and row["connected_tuples"] > 0
            for row in rows
        ),
        "positive_excess_bound_below_diagonal": positive_bound_ratio < 1,
        "positive_excess_actual_below_diagonal": positive_actual_ratio < 1,
    }


def closure_signature_profile() -> dict:
    """Count all ordered support triples by k-closed component signature."""
    p, n, k, a, tuple_size = 7, 6, 2, 3, 3
    h_values = subgroup(p, n)
    supports = [tuple(support) for support in itertools.combinations(range(n), a)]
    rows_by_signature: dict[tuple[int, int, int, int, int, int, bool], int] = {}
    for support_tuple in itertools.product(supports, repeat=tuple_size):
        closed_components = closure_components(list(support_tuple), k)
        part_unions = component_unions(list(support_tuple), closed_components)
        closed_count = len(closed_components)
        union_size = len(set().union(*[set(support) for support in support_tuple]))
        sum_part_union_size = sum(len(part_union) for part_union in part_unions)
        cross_overlap_defect = sum_part_union_size - union_size
        cross_rank = cross_constraint_rank(p, h_values, k, part_unions)
        global_excess = union_size - a * closed_count
        corrected_excess = global_excess + cross_rank
        overlap_edges = component_overlap_edges(part_unions)
        overlap_is_forest = is_forest(overlap_edges, closed_count)
        signature = (
            closed_count,
            union_size,
            global_excess,
            cross_rank,
            corrected_excess,
            cross_overlap_defect,
            overlap_is_forest,
        )
        rows_by_signature[signature] = rows_by_signature.get(signature, 0) + 1
    rows = []
    for (
        closed_count,
        union_size,
        global_excess,
        cross_rank,
        corrected_excess,
        cross_overlap_defect,
        overlap_is_forest,
    ), count in sorted(rows_by_signature.items()):
        union_bound = comb(n, union_size) * comb(union_size, a) ** tuple_size
        rows.append(
            {
                "closed_components": closed_count,
                "union_size": union_size,
                "global_excess": global_excess,
                "cross_constraint_rank": cross_rank,
                "rank_corrected_excess": corrected_excess,
                "cross_overlap_defect": cross_overlap_defect,
                "component_union_excess": global_excess + cross_overlap_defect,
                "overlap_is_forest": overlap_is_forest,
                "tuple_count": count,
                "union_count_bound": union_bound,
                "entropy_exponent": union_size - k * closed_count,
                "rank_corrected_entropy_exponent": union_size
                - k * closed_count
                + cross_rank,
            }
        )
    forest_rows = [row for row in rows if row["overlap_is_forest"]]
    return {
        "p": p,
        "n": n,
        "k": k,
        "a": a,
        "tuple_size": tuple_size,
        "rows": rows,
        "total_tuples": sum(row["tuple_count"] for row in rows),
        "expected_total_tuples": len(supports) ** tuple_size,
        "all_counts_bounded": all(
            row["tuple_count"] <= row["union_count_bound"] for row in rows
        ),
        "has_negative_global_excess": any(
            row["global_excess"] < 0 for row in rows
        ),
        "has_zero_global_excess": any(
            row["global_excess"] == 0 for row in rows
        ),
        "has_positive_global_excess": any(
            row["global_excess"] > 0 for row in rows
        ),
        "has_cyclic_overlap_graph": any(
            not row["overlap_is_forest"] for row in rows
        ),
        "forest_rank_cancels_overlap_defect": all(
            row["cross_constraint_rank"] == row["cross_overlap_defect"]
            and row["rank_corrected_excess"] == row["component_union_excess"]
            for row in forest_rows
        ),
        "two_part_rank_cancels_overlap_defect": all(
            row["cross_constraint_rank"] == row["cross_overlap_defect"]
            and row["rank_corrected_excess"] == row["component_union_excess"]
            for row in rows
            if row["closed_components"] == 2
        ),
        "rank_corrected_excess_nonnegative": all(
            row["rank_corrected_excess"] >= 0 for row in rows
        ),
    }


def cyclic_overlap_rank_deficit_profile() -> dict:
    """Finite instances where cyclic low-overlap components do not factor."""
    p, n, mu = 17, 16, 2
    h_values = subgroup(p, n)
    rows = []
    for k in range(3, 7):
        block_size = k - 1
        a = 2 * block_size
        first = set(range(block_size))
        second = set(range(block_size, 2 * block_size))
        third = set(range(2 * block_size, 3 * block_size))
        supports = [
            tuple(sorted(first | second)),
            tuple(sorted(first | third)),
            tuple(sorted(second | third)),
        ]
        closed_components = closure_components(supports, k)
        part_unions = component_unions(supports, closed_components)
        closed_count = len(closed_components)
        union_size = len(set().union(*[set(support) for support in supports]))
        cross_overlap_defect = (
            sum(len(part_union) for part_union in part_unions) - union_size
        )
        cross_rank = cross_constraint_rank(p, h_values, k, part_unions)
        global_excess = union_size - a * closed_count
        rank_corrected_excess = global_excess + cross_rank
        product_diagonal_exponent = closed_count * (a - k)
        rank_corrected_exponent = product_diagonal_exponent + rank_corrected_excess
        diagonal_exponent = a - k
        family_count = (
            comb(n, block_size)
            * comb(n - block_size, block_size)
            * comb(n - 2 * block_size, block_size)
        )
        diagonal_count = comb(n, a)
        relative_to_diagonal = Fraction(
            family_count,
            diagonal_count
            * p ** (mu * (rank_corrected_exponent - diagonal_exponent)),
        )
        overlap_edges = component_overlap_edges(part_unions)
        rows.append(
            {
                "k": k,
                "a": a,
                "block_size": block_size,
                "supports": [list(support) for support in supports],
                "closed_components": closed_count,
                "overlap_edges": [list(edge) for edge in overlap_edges],
                "overlap_is_forest": is_forest(overlap_edges, closed_count),
                "union_size": union_size,
                "global_excess": global_excess,
                "cross_overlap_defect": cross_overlap_defect,
                "cross_constraint_rank": cross_rank,
                "rank_deficit_vs_overlap": cross_overlap_defect - cross_rank,
                "rank_corrected_excess": rank_corrected_excess,
                "family_count": family_count,
                "diagonal_count": diagonal_count,
                "product_diagonal_exponent": product_diagonal_exponent,
                "rank_corrected_exponent": rank_corrected_exponent,
                "diagonal_exponent": diagonal_exponent,
                "relative_to_diagonal": {
                    "numerator": relative_to_diagonal.numerator,
                    "denominator": relative_to_diagonal.denominator,
                },
                "surplus_over_product_diagonal": product_diagonal_exponent
                - rank_corrected_exponent,
            }
        )
    deficit_rows = [row for row in rows if row["k"] >= 4]
    return {
        "p": p,
        "n": n,
        "mu": mu,
        "rows": rows,
        "all_three_part_cycles": all(
            row["closed_components"] == 3
            and len(row["overlap_edges"]) == 3
            and not row["overlap_is_forest"]
            for row in rows
        ),
        "rank_formula_holds": all(
            row["cross_constraint_rank"] == 2 * row["k"] for row in rows
        ),
        "excess_formula_holds": all(
            row["rank_corrected_excess"] == 3 - row["k"] for row in rows
        ),
        "exponent_formula_holds": all(
            row["rank_corrected_exponent"] == 2 * row["k"] - 3
            for row in rows
        ),
        "has_negative_rank_corrected_excess": any(
            row["rank_corrected_excess"] < 0 for row in rows
        ),
        "deficit_grows_after_k_three": all(
            row["surplus_over_product_diagonal"] == row["k"] - 3
            and row["rank_deficit_vs_overlap"] == row["k"] - 3
            for row in deficit_rows
        ),
        "relative_exponent_is_block_size": all(
            row["rank_corrected_exponent"] - row["diagonal_exponent"]
            == row["block_size"]
            for row in rows
        ),
        "generic_triangle_family_below_diagonal": all(
            row["relative_to_diagonal"]["numerator"]
            < row["relative_to_diagonal"]["denominator"]
            for row in rows
        ),
    }


def constant_ratio_triangle_profile() -> dict:
    """Count cyclic triangles where the locator ratio is constant on C."""
    p, n, mu = 17, 16, 2
    h_values = subgroup(p, n)
    rows = []
    for r in range(2, 6):
        subsets = [tuple(subset) for subset in itertools.combinations(range(n), r)]
        locators = {
            subset: vanish_values(p, h_values, list(subset))
            for subset in subsets
        }
        inverse_locators = {
            subset: tuple(
                0 if idx in subset else pow(value, -1, p)
                for idx, value in enumerate(values)
            )
            for subset, values in locators.items()
        }
        exact_count = 0
        max_ratio_bucket = 0
        example = None
        for a_block in subsets:
            a_set = set(a_block)
            complement_a = [idx for idx in range(n) if idx not in a_set]
            locator_a = locators[a_block]
            for b_block in itertools.combinations(complement_a, r):
                b_set = set(b_block)
                remaining = [idx for idx in complement_a if idx not in b_set]
                inverse_b = inverse_locators[tuple(b_block)]
                buckets: dict[int, list[int]] = {}
                for idx in remaining:
                    ratio = (locator_a[idx] * inverse_b[idx]) % p
                    if ratio == 1:
                        continue
                    buckets.setdefault(ratio, []).append(idx)
                for ratio, indices in buckets.items():
                    if len(indices) < r:
                        continue
                    exact_count += comb(len(indices), r)
                    if len(indices) > max_ratio_bucket:
                        max_ratio_bucket = len(indices)
                        example = {
                            "A": list(a_block),
                            "B": list(b_block),
                            "ratio": ratio,
                            "bucket": indices,
                        }
        count_bound = (p - 2) * comb(n, r) * comb(n - r, r)
        diagonal_count = comb(n, 2 * r)
        triangle_family_count = (
            comb(n, r) * comb(n - r, r) * comb(n - 2 * r, r)
        )
        nonconstant_count = triangle_family_count - exact_count
        exponent_gap = r - 1
        nonconstant_exponent_gap = r
        exact_relative = Fraction(
            exact_count,
            diagonal_count * p ** (mu * exponent_gap),
        )
        bound_relative = Fraction(
            count_bound,
            diagonal_count * p ** (mu * exponent_gap),
        )
        combined_exact_relative = exact_relative + Fraction(
            nonconstant_count,
            diagonal_count * p ** (mu * nonconstant_exponent_gap),
        )
        combined_bound_relative = bound_relative + Fraction(
            triangle_family_count,
            diagonal_count * p ** (mu * nonconstant_exponent_gap),
        )
        rows.append(
            {
                "r": r,
                "k": r + 1,
                "a": 2 * r,
                "triangle_family_count": triangle_family_count,
                "nonconstant_count": nonconstant_count,
                "exact_count": exact_count,
                "count_bound": count_bound,
                "diagonal_count": diagonal_count,
                "rank_corrected_exponent": 2 * r - 2,
                "diagonal_exponent": r - 1,
                "exponent_gap": exponent_gap,
                "nonconstant_exponent_gap": nonconstant_exponent_gap,
                "max_ratio_bucket": max_ratio_bucket,
                "example": example,
                "exact_relative_to_diagonal": {
                    "numerator": exact_relative.numerator,
                    "denominator": exact_relative.denominator,
                },
                "bound_relative_to_diagonal": {
                    "numerator": bound_relative.numerator,
                    "denominator": bound_relative.denominator,
                },
                "combined_exact_relative_to_diagonal": {
                    "numerator": combined_exact_relative.numerator,
                    "denominator": combined_exact_relative.denominator,
                },
                "combined_bound_relative_to_diagonal": {
                    "numerator": combined_bound_relative.numerator,
                    "denominator": combined_bound_relative.denominator,
                },
            }
        )
    return {
        "p": p,
        "n": n,
        "mu": mu,
        "rows": rows,
        "all_counts_bounded": all(
            row["exact_count"] <= row["count_bound"] for row in rows
        ),
        "all_buckets_degree_bounded": all(
            row["max_ratio_bucket"] <= row["r"] for row in rows
        ),
        "exact_relative_below_diagonal": all(
            row["exact_relative_to_diagonal"]["numerator"]
            < row["exact_relative_to_diagonal"]["denominator"]
            for row in rows
        ),
        "bound_relative_below_diagonal": all(
            row["bound_relative_to_diagonal"]["numerator"]
            < row["bound_relative_to_diagonal"]["denominator"]
            for row in rows
        ),
        "exponent_gap_formula": all(
            row["exponent_gap"] == row["r"] - 1 for row in rows
        ),
        "combined_exact_relative_below_diagonal": all(
            row["combined_exact_relative_to_diagonal"]["numerator"]
            < row["combined_exact_relative_to_diagonal"]["denominator"]
            for row in rows
        ),
        "combined_bound_relative_below_diagonal": all(
            row["combined_bound_relative_to_diagonal"]["numerator"]
            < row["combined_bound_relative_to_diagonal"]["denominator"]
            for row in rows
        ),
    }


def full_rank_cyclic_necklace_profile() -> dict:
    """Check full-rank cyclic low-overlap necklaces beyond triangles."""
    p, n, mu = 31, 30, 2
    h_values = subgroup(p, n)
    rows = []
    for cycle_len in range(3, 7):
        for r in range(2, 7):
            k = r + 1
            a = 2 * r
            if cycle_len > k or cycle_len * r > n:
                continue
            edge_blocks = [
                set(range(block * r, (block + 1) * r))
                for block in range(cycle_len)
            ]
            supports = [
                tuple(sorted(edge_blocks[idx] | edge_blocks[(idx + 1) % cycle_len]))
                for idx in range(cycle_len)
            ]
            closed_components = closure_components(supports, k)
            part_unions = component_unions(supports, closed_components)
            overlap_edges = component_overlap_edges(part_unions)
            union_size = len(set().union(*[set(support) for support in supports]))
            global_excess = union_size - cycle_len * a
            cross_rank = cross_constraint_rank(p, h_values, k, part_unions)
            locator_rows = []
            for edge_block in edge_blocks:
                roots = [h_values[idx] for idx in sorted(edge_block)]
                locator = poly_from_roots(p, roots)
                locator_rows.append(locator + [0] * (k - len(locator)))
            locator_rank = matrix_rank_mod(locator_rows, p)
            expected_cross_rank = (cycle_len - 1) * k - cycle_len + locator_rank
            product_diagonal_exponent = cycle_len * (a - k)
            rank_corrected_exponent = (
                product_diagonal_exponent + global_excess + cross_rank
            )
            diagonal_exponent = a - k
            exponent_gap = rank_corrected_exponent - diagonal_exponent
            expected_gap = (cycle_len - 2) * r
            family_count = 1
            for block in range(cycle_len):
                family_count *= comb(n - block * r, r)
            diagonal_count = comb(n, a)
            relative_to_diagonal = Fraction(
                family_count,
                diagonal_count * p ** (mu * exponent_gap),
            )
            rows.append(
                {
                    "cycle_len": cycle_len,
                    "r": r,
                    "k": k,
                    "a": a,
                    "supports": [list(support) for support in supports],
                    "closed_components": len(closed_components),
                    "overlap_edges": [list(edge) for edge in overlap_edges],
                    "overlap_is_forest": is_forest(overlap_edges, len(part_unions)),
                    "union_size": union_size,
                    "global_excess": global_excess,
                    "locator_rank": locator_rank,
                    "cross_constraint_rank": cross_rank,
                    "expected_cross_constraint_rank": expected_cross_rank,
                    "product_diagonal_exponent": product_diagonal_exponent,
                    "rank_corrected_exponent": rank_corrected_exponent,
                    "diagonal_exponent": diagonal_exponent,
                    "exponent_gap": exponent_gap,
                    "expected_exponent_gap": expected_gap,
                    "family_count": family_count,
                    "diagonal_count": diagonal_count,
                    "relative_to_diagonal": {
                        "numerator": relative_to_diagonal.numerator,
                        "denominator": relative_to_diagonal.denominator,
                    },
                }
            )
    return {
        "p": p,
        "n": n,
        "mu": mu,
        "rows": rows,
        "cycle_lengths_seen": sorted({row["cycle_len"] for row in rows}),
        "covers_cycle_lengths_three_through_six": {3, 4, 5, 6}
        <= {row["cycle_len"] for row in rows},
        "all_closed_parts_singleton": all(
            row["closed_components"] == row["cycle_len"] for row in rows
        ),
        "all_overlap_graphs_cyclic": all(
            len(row["overlap_edges"]) == row["cycle_len"]
            and not row["overlap_is_forest"]
            for row in rows
        ),
        "all_locators_full_rank": all(
            row["locator_rank"] == row["cycle_len"] for row in rows
        ),
        "cross_rank_formula_holds": all(
            row["cross_constraint_rank"] == row["expected_cross_constraint_rank"]
            for row in rows
        ),
        "exponent_gap_formula_holds": all(
            row["exponent_gap"] == row["expected_exponent_gap"]
            for row in rows
        ),
        "relative_bound_below_diagonal": all(
            row["relative_to_diagonal"]["numerator"]
            < row["relative_to_diagonal"]["denominator"]
            for row in rows
        ),
    }


def rank_deficient_cyclic_necklace_profile() -> dict:
    """Check the dependency-count bound for rank-deficient necklaces."""
    p, n, mu = 31, 30, 2
    rows = []
    for cycle_len in range(3, 7):
        for r in range(2, 7):
            k = r + 1
            a = 2 * r
            if cycle_len > k or cycle_len * r > n:
                continue
            chosen_blocks_count = 1
            for block in range(cycle_len - 1):
                chosen_blocks_count *= comb(n - block * r, r)
            coefficient_choices = p ** (cycle_len - 2)
            count_bound = cycle_len * coefficient_choices * chosen_blocks_count
            diagonal_count = comb(n, a)
            exponent_gap_lower_bound = (cycle_len - 2) * (r - 1)
            relative_bound = Fraction(
                count_bound,
                diagonal_count * p ** (mu * exponent_gap_lower_bound),
            )
            rows.append(
                {
                    "cycle_len": cycle_len,
                    "r": r,
                    "k": k,
                    "a": a,
                    "pivot_choices": cycle_len,
                    "coefficient_choices": coefficient_choices,
                    "chosen_blocks_count": chosen_blocks_count,
                    "count_bound": count_bound,
                    "diagonal_count": diagonal_count,
                    "locator_rank_lower_bound": 2,
                    "exponent_gap_lower_bound": exponent_gap_lower_bound,
                    "relative_bound_to_diagonal": {
                        "numerator": relative_bound.numerator,
                        "denominator": relative_bound.denominator,
                    },
                }
            )
    return {
        "p": p,
        "n": n,
        "mu": mu,
        "rows": rows,
        "cycle_lengths_seen": sorted({row["cycle_len"] for row in rows}),
        "covers_cycle_lengths_three_through_six": {3, 4, 5, 6}
        <= {row["cycle_len"] for row in rows},
        "coefficient_choice_formula_holds": all(
            row["coefficient_choices"] == p ** (row["cycle_len"] - 2)
            for row in rows
        ),
        "exponent_gap_lower_bound_formula_holds": all(
            row["exponent_gap_lower_bound"]
            == (row["cycle_len"] - 2) * (row["r"] - 1)
            for row in rows
        ),
        "relative_bound_below_diagonal": all(
            row["relative_bound_to_diagonal"]["numerator"]
            < row["relative_bound_to_diagonal"]["denominator"]
            for row in rows
        ),
    }


def evaluation_span_intersection_dimension(
    p: int,
    h_values: list[int],
    k: int,
    edge_blocks: list[set[int]],
) -> int:
    """Dimension of the common intersection of edge evaluation spans."""
    offsets = []
    cursor = 0
    edge_lists = [sorted(edge_block) for edge_block in edge_blocks]
    for edge_list in edge_lists:
        offsets.append(cursor)
        cursor += len(edge_list)
    rows = []
    for edge_idx in range(1, len(edge_blocks)):
        for degree in range(k):
            row = [0] * cursor
            for local_idx, idx in enumerate(edge_lists[0]):
                column = offsets[0] + local_idx
                row[column] = (row[column] - pow(h_values[idx], degree, p)) % p
            for local_idx, idx in enumerate(edge_lists[edge_idx]):
                column = offsets[edge_idx] + local_idx
                row[column] = (
                    row[column]
                    + pow(h_values[idx], degree, p)
                ) % p
            rows.append(row)
    return cursor - matrix_rank_mod(rows, p)


def clean_cycle_rank_profile() -> dict:
    """Check the exact rank formula for clean simple low-overlap cycles."""
    p, n, mu = 31, 30, 2
    h_values = subgroup(p, n)
    examples = [
        {"name": "triangle_necklace", "cycle_len": 3, "k": 5, "a": 8, "edges": [4, 4, 4]},
        {"name": "private_mass_square", "cycle_len": 4, "k": 5, "a": 9, "edges": [4, 4, 4, 4]},
        {"name": "uneven_square", "cycle_len": 4, "k": 6, "a": 10, "edges": [5, 4, 5, 3]},
        {"name": "small_pair_square", "cycle_len": 4, "k": 6, "a": 10, "edges": [5, 1, 5, 1]},
        {"name": "uneven_pentagon", "cycle_len": 5, "k": 6, "a": 10, "edges": [5, 5, 4, 4, 3]},
    ]
    rows = []
    for example in examples:
        cycle_len = example["cycle_len"]
        k = example["k"]
        a = example["a"]
        edge_sizes = example["edges"]
        private_sizes = [
            a - edge_sizes[idx - 1] - edge_sizes[idx]
            for idx in range(cycle_len)
        ]
        if any(size < 0 for size in private_sizes):
            raise ValueError(f"negative private size in {example['name']}")
        cursor = 0
        edge_blocks = []
        for edge_size in edge_sizes:
            edge_blocks.append(set(range(cursor, cursor + edge_size)))
            cursor += edge_size
        private_blocks = []
        for private_size in private_sizes:
            private_blocks.append(set(range(cursor, cursor + private_size)))
            cursor += private_size
        if cursor > n:
            raise ValueError(f"example {example['name']} exceeds n={n}")
        supports = []
        for idx in range(cycle_len):
            support = (
                edge_blocks[idx - 1]
                | edge_blocks[idx]
                | private_blocks[idx]
            )
            supports.append(tuple(sorted(support)))
        closed_components = closure_components(supports, k)
        part_unions = component_unions(supports, closed_components)
        overlap_edges = component_overlap_edges(part_unions)
        union_size = len(set().union(*[set(support) for support in supports]))
        edge_total = sum(edge_sizes)
        expected_union_size = cycle_len * a - edge_total
        vanishing_basis = []
        for edge_block in edge_blocks:
            roots = [h_values[idx] for idx in sorted(edge_block)]
            locator = poly_from_roots(p, roots)
            for power in range(k - len(edge_block)):
                basis_poly = poly_mul(locator, monomial(power), p)
                vanishing_basis.append(basis_poly + [0] * (k - len(basis_poly)))
        vanishing_sum_rank = matrix_rank_mod(vanishing_basis, p)
        selected_domain_dim = sum(k - edge_size for edge_size in edge_sizes)
        syzygy_kernel_dim = selected_domain_dim - vanishing_sum_rank
        expected_generic_syzygy_kernel_dim = max(0, selected_domain_dim - k)
        syzygy_kernel_excess = (
            syzygy_kernel_dim - expected_generic_syzygy_kernel_dim
        )
        dual_intersection_dim = evaluation_span_intersection_dimension(
            p, h_values, k, edge_blocks
        )
        rank_defect = k - vanishing_sum_rank
        cross_rank = cross_constraint_rank(p, h_values, k, part_unions)
        expected_cross_rank = edge_total + vanishing_sum_rank - k
        product_diagonal_exponent = cycle_len * (a - k)
        rank_corrected_exponent = (
            product_diagonal_exponent - edge_total + cross_rank
        )
        expected_rank_corrected_exponent = (
            cycle_len * (a - k) + vanishing_sum_rank - k
        )
        diagonal_exponent = a - k
        exponent_gap = rank_corrected_exponent - diagonal_exponent
        expected_exponent_gap = (cycle_len - 1) * (a - k) + vanishing_sum_rank - k
        min_edge_pair_sum, min_pair_left, min_pair_right = min(
            (edge_sizes[left] + edge_sizes[right], left, right)
            for left in range(cycle_len)
            for right in range(left + 1, cycle_len)
        )
        min_edge_size = min(edge_sizes)
        min_edge_index = edge_sizes.index(min_edge_size)
        two_edge_lower_bound = (
            k if min_edge_pair_sum <= k else 2 * k - min_edge_pair_sum
        )
        two_edge_defect_upper_bound = max(0, min_edge_pair_sum - k)
        private_block_bound = 1
        for private_size in private_sizes:
            private_block_bound *= comb(n, private_size)
        edge_block_bound = 1
        for edge_size in edge_sizes:
            edge_block_bound *= comb(n, edge_size)
        projective_functional_count = (p**k - 1) // (p - 1)
        crude_projective_tuple_bound = (
            projective_functional_count * edge_block_bound * private_block_bound
        )
        one_edge_tuple_bound = (
            comb(n, min_edge_size)
            * (p**min_edge_size - 1)
            // (p - 1)
            * private_block_bound
        )
        for idx, edge_size in enumerate(edge_sizes):
            if idx != min_edge_index:
                one_edge_tuple_bound *= comb(n, edge_size)
        saving_ratio = Fraction(one_edge_tuple_bound, crude_projective_tuple_bound)
        expected_saving_ratio = Fraction(
            p**min_edge_size - 1,
            p**k - 1,
        )
        two_edge_gap_lower_bound = (
            (cycle_len - 1) * (a - k) - two_edge_defect_upper_bound
        )
        gap_power = mu * two_edge_gap_lower_bound
        if gap_power >= 0:
            one_edge_relative_bound = Fraction(
                one_edge_tuple_bound,
                comb(n, a) * p**gap_power,
            )
        else:
            one_edge_relative_bound = Fraction(
                one_edge_tuple_bound * p ** (-gap_power),
                comb(n, a),
            )
        two_edge_common_functional_dim = two_edge_defect_upper_bound
        if two_edge_common_functional_dim == 0:
            two_edge_tuple_bound = 0
        else:
            left_size = edge_sizes[min_pair_left]
            right_size = edge_sizes[min_pair_right]
            two_edge_tuple_bound = (
                comb(n, left_size)
                * comb(n - left_size, right_size)
                * (p**two_edge_common_functional_dim - 1)
                // (p - 1)
                * private_block_bound
            )
            for idx, edge_size in enumerate(edge_sizes):
                if idx not in (min_pair_left, min_pair_right):
                    two_edge_tuple_bound *= comb(n, edge_size)
        if gap_power >= 0:
            two_edge_relative_bound = Fraction(
                two_edge_tuple_bound,
                comb(n, a) * p**gap_power,
            )
        else:
            two_edge_relative_bound = Fraction(
                two_edge_tuple_bound * p ** (-gap_power),
                comb(n, a),
            )
        all_edge_expected_selected_rank = min(
            k, sum(k - edge_size for edge_size in edge_sizes)
        )
        all_edge_expected_common_dim = k - all_edge_expected_selected_rank
        all_edge_disjoint_block_count = 1
        used_points = 0
        for edge_size in edge_sizes:
            all_edge_disjoint_block_count *= comb(n - used_points, edge_size)
            used_points += edge_size
        if all_edge_expected_common_dim == 0:
            all_edge_full_rank_tuple_bound = 0
        else:
            all_edge_full_rank_tuple_bound = (
                all_edge_disjoint_block_count
                * (p**all_edge_expected_common_dim - 1)
                // (p - 1)
                * private_block_bound
            )
        all_edge_full_rank_gap_lower_bound = (
            (cycle_len - 1) * (a - k) - all_edge_expected_common_dim
        )
        all_edge_gap_power = mu * all_edge_full_rank_gap_lower_bound
        if all_edge_gap_power >= 0:
            all_edge_full_rank_relative_bound = Fraction(
                all_edge_full_rank_tuple_bound,
                comb(n, a) * p**all_edge_gap_power,
            )
        else:
            all_edge_full_rank_relative_bound = Fraction(
                all_edge_full_rank_tuple_bound * p ** (-all_edge_gap_power),
                comb(n, a),
            )
        rows.append(
            {
                "name": example["name"],
                "cycle_len": cycle_len,
                "k": k,
                "a": a,
                "edge_sizes": edge_sizes,
                "private_sizes": private_sizes,
                "min_edge_size": min_edge_size,
                "min_edge_index": min_edge_index,
                "supports": [list(support) for support in supports],
                "closed_components": len(closed_components),
                "overlap_edges": [list(edge) for edge in overlap_edges],
                "overlap_is_forest": is_forest(overlap_edges, len(part_unions)),
                "union_size": union_size,
                "expected_union_size": expected_union_size,
                "edge_total": edge_total,
                "min_edge_pair_sum": min_edge_pair_sum,
                "min_edge_pair_indices": [min_pair_left, min_pair_right],
                "two_edge_rank_lower_bound": two_edge_lower_bound,
                "two_edge_defect_upper_bound": two_edge_defect_upper_bound,
                "two_edge_common_functional_dim": two_edge_common_functional_dim,
                "vanishing_sum_rank": vanishing_sum_rank,
                "selected_domain_dim": selected_domain_dim,
                "syzygy_kernel_dim": syzygy_kernel_dim,
                "expected_generic_syzygy_kernel_dim": (
                    expected_generic_syzygy_kernel_dim
                ),
                "syzygy_kernel_excess": syzygy_kernel_excess,
                "rank_defect": rank_defect,
                "dual_intersection_dimension": dual_intersection_dim,
                "cross_constraint_rank": cross_rank,
                "expected_cross_constraint_rank": expected_cross_rank,
                "product_diagonal_exponent": product_diagonal_exponent,
                "rank_corrected_exponent": rank_corrected_exponent,
                "expected_rank_corrected_exponent": expected_rank_corrected_exponent,
                "diagonal_exponent": diagonal_exponent,
                "exponent_gap": exponent_gap,
                "expected_exponent_gap": expected_exponent_gap,
                "two_edge_gap_lower_bound": two_edge_gap_lower_bound,
                "private_block_bound": private_block_bound,
                "edge_block_bound": edge_block_bound,
                "crude_projective_tuple_bound": crude_projective_tuple_bound,
                "one_edge_tuple_bound": one_edge_tuple_bound,
                "saving_ratio": {
                    "numerator": saving_ratio.numerator,
                    "denominator": saving_ratio.denominator,
                },
                "expected_saving_ratio": {
                    "numerator": expected_saving_ratio.numerator,
                    "denominator": expected_saving_ratio.denominator,
                },
                "one_edge_relative_bound_to_diagonal": {
                    "numerator": one_edge_relative_bound.numerator,
                    "denominator": one_edge_relative_bound.denominator,
                },
                "two_edge_tuple_bound": two_edge_tuple_bound,
                "two_edge_relative_bound_to_diagonal": {
                    "numerator": two_edge_relative_bound.numerator,
                    "denominator": two_edge_relative_bound.denominator,
                },
                "all_edge_expected_selected_rank": all_edge_expected_selected_rank,
                "all_edge_expected_common_dim": all_edge_expected_common_dim,
                "all_edge_disjoint_block_count": all_edge_disjoint_block_count,
                "all_edge_full_rank_tuple_bound": all_edge_full_rank_tuple_bound,
                "all_edge_full_rank_gap_lower_bound": (
                    all_edge_full_rank_gap_lower_bound
                ),
                "all_edge_full_rank_relative_bound_to_diagonal": {
                    "numerator": all_edge_full_rank_relative_bound.numerator,
                    "denominator": all_edge_full_rank_relative_bound.denominator,
                },
            }
        )
    return {
        "p": p,
        "n": n,
        "mu": mu,
        "rows": rows,
        "all_clean_cycles": all(
            row["closed_components"] == row["cycle_len"]
            and len(row["overlap_edges"]) == row["cycle_len"]
            and not row["overlap_is_forest"]
            and row["union_size"] == row["expected_union_size"]
            for row in rows
        ),
        "cross_rank_formula_holds": all(
            row["cross_constraint_rank"] == row["expected_cross_constraint_rank"]
            for row in rows
        ),
        "rank_corrected_exponent_formula_holds": all(
            row["rank_corrected_exponent"]
            == row["expected_rank_corrected_exponent"]
            for row in rows
        ),
        "exponent_gap_formula_holds": all(
            row["exponent_gap"] == row["expected_exponent_gap"]
            for row in rows
        ),
        "contains_uneven_edges": any(
            len(set(row["edge_sizes"])) > 1 for row in rows
        ),
        "contains_private_mass": any(
            any(size > 0 for size in row["private_sizes"]) for row in rows
        ),
        "two_edge_lower_bound_holds": all(
            row["vanishing_sum_rank"] >= row["two_edge_rank_lower_bound"]
            for row in rows
        ),
        "dual_defect_formula_holds": all(
            row["dual_intersection_dimension"] == row["rank_defect"]
            for row in rows
        ),
        "two_edge_defect_bound_holds": all(
            row["rank_defect"] <= row["two_edge_defect_upper_bound"]
            for row in rows
        ),
        "small_pair_forces_full_rank": all(
            row["vanishing_sum_rank"] == row["k"]
            for row in rows
            if row["min_edge_pair_sum"] <= row["k"]
        ),
        "contains_small_pair_case": any(
            row["min_edge_pair_sum"] <= row["k"] for row in rows
        ),
        "one_edge_tuple_bound_saves": all(
            row["one_edge_tuple_bound"] <= row["crude_projective_tuple_bound"]
            for row in rows
        ),
        "one_edge_saving_formula_holds": all(
            row["saving_ratio"] == row["expected_saving_ratio"]
            for row in rows
        ),
        "one_edge_relative_bound_clears_nontriangle_examples": all(
            row["name"] == "triangle_necklace"
            or row["one_edge_relative_bound_to_diagonal"]["numerator"]
            < row["one_edge_relative_bound_to_diagonal"]["denominator"]
            for row in rows
        ),
        "one_edge_relative_bound_records_triangle_coarseness": any(
            row["name"] == "triangle_necklace"
            and row["one_edge_relative_bound_to_diagonal"]["numerator"]
            > row["one_edge_relative_bound_to_diagonal"]["denominator"]
            for row in rows
        ),
        "two_edge_tuple_bound_saves_on_examples": all(
            row["two_edge_tuple_bound"] <= row["one_edge_tuple_bound"]
            for row in rows
        ),
        "two_edge_tuple_bound_forbids_small_pair_examples": all(
            row["two_edge_tuple_bound"] == 0
            for row in rows
            if row["min_edge_pair_sum"] <= row["k"]
        ),
        "two_edge_relative_bound_clears_nontriangle_examples": all(
            row["name"] == "triangle_necklace"
            or row["two_edge_relative_bound_to_diagonal"]["numerator"]
            < row["two_edge_relative_bound_to_diagonal"]["denominator"]
            for row in rows
        ),
        "two_edge_relative_bound_records_triangle_coarseness": any(
            row["name"] == "triangle_necklace"
            and row["two_edge_relative_bound_to_diagonal"]["numerator"]
            > row["two_edge_relative_bound_to_diagonal"]["denominator"]
            for row in rows
        ),
        "all_edge_selected_rank_full_on_examples": all(
            row["vanishing_sum_rank"] == row["all_edge_expected_selected_rank"]
            for row in rows
        ),
        "selected_syzygy_kernel_formula_holds": all(
            row["syzygy_kernel_dim"]
            == row["selected_domain_dim"] - row["vanishing_sum_rank"]
            for row in rows
        ),
        "selected_syzygy_no_excess_on_examples": all(
            row["syzygy_kernel_excess"] == 0 for row in rows
        ),
        "all_edge_full_rank_tuple_bound_saves_on_examples": all(
            row["all_edge_full_rank_tuple_bound"] <= row["two_edge_tuple_bound"]
            for row in rows
        ),
        "all_edge_full_rank_relative_clears_examples": all(
            row["all_edge_full_rank_relative_bound_to_diagonal"]["numerator"]
            < row["all_edge_full_rank_relative_bound_to_diagonal"]["denominator"]
            for row in rows
        ),
        "all_edge_full_rank_clears_triangle_example": any(
            row["name"] == "triangle_necklace"
            and row["all_edge_full_rank_relative_bound_to_diagonal"]["numerator"]
            < row["all_edge_full_rank_relative_bound_to_diagonal"]["denominator"]
            for row in rows
        ),
    }


def locator_syzygy_witness_profile() -> dict:
    """A small lower-rank selected-edge witness for the syzygy formulation."""
    p, n, k = 7, 6, 3
    h_values = subgroup(p, n)
    edge_blocks = [set(block) for block in ((0, 1), (2, 5), (3, 4))]
    locators = [
        poly_from_roots(p, [h_values[idx] for idx in sorted(edge_block)])
        for edge_block in edge_blocks
    ]
    locator_rows = [
        locator + [0] * (k - len(locator))
        for locator in locators
    ]
    vanishing_basis = []
    for edge_block, locator in zip(edge_blocks, locators):
        for power in range(k - len(edge_block)):
            basis_poly = poly_mul(locator, monomial(power), p)
            vanishing_basis.append(basis_poly + [0] * (k - len(basis_poly)))
    selected_rank = matrix_rank_mod(vanishing_basis, p)
    locator_rank = matrix_rank_mod(locator_rows, p)
    selected_domain_dim = sum(k - len(edge_block) for edge_block in edge_blocks)
    expected_full_rank = min(k, selected_domain_dim)
    syzygy_kernel_dim = selected_domain_dim - selected_rank
    expected_generic_kernel_dim = max(0, selected_domain_dim - k)
    syzygy_kernel_excess = syzygy_kernel_dim - expected_generic_kernel_dim
    common_functional_dim = k - selected_rank
    expected_full_rank_common_dim = k - expected_full_rank
    syzygy_coefficients = [[1], [5], [1]]
    syzygy_sum = [0]
    for locator, coeff_poly in zip(locators, syzygy_coefficients):
        syzygy_sum = poly_add(syzygy_sum, poly_mul(locator, coeff_poly, p), p)
    pivot = 0
    nonpivot_sum = [0]
    for idx, (locator, coeff_poly) in enumerate(
        zip(locators, syzygy_coefficients)
    ):
        if idx == pivot:
            continue
        nonpivot_sum = poly_add(nonpivot_sum, poly_mul(locator, coeff_poly, p), p)
    forced_numerator = poly_scale(nonpivot_sum, -1, p)
    forced_locator, forcing_remainder = poly_divmod(
        forced_numerator, syzygy_coefficients[pivot], p
    )
    forced_roots = [
        idx
        for idx, x_value in enumerate(h_values)
        if eval_poly(tuple(forced_locator), x_value, p) == 0
    ]
    return {
        "p": p,
        "n": n,
        "k": k,
        "edge_blocks": [sorted(edge_block) for edge_block in edge_blocks],
        "locators": locators,
        "syzygy_coefficients": syzygy_coefficients,
        "syzygy_sum": syzygy_sum,
        "selected_domain_dim": selected_domain_dim,
        "selected_rank": selected_rank,
        "expected_full_rank": expected_full_rank,
        "locator_rank": locator_rank,
        "syzygy_kernel_dim": syzygy_kernel_dim,
        "expected_generic_kernel_dim": expected_generic_kernel_dim,
        "syzygy_kernel_excess": syzygy_kernel_excess,
        "common_functional_dim": common_functional_dim,
        "expected_full_rank_common_dim": expected_full_rank_common_dim,
        "has_nontrivial_syzygy_excess": syzygy_kernel_excess > 0,
        "rank_defect_equals_syzygy_excess": (
            expected_full_rank - selected_rank == syzygy_kernel_excess
        ),
        "necklace_locator_rank_matches_selected_rank": locator_rank == selected_rank,
        "pivot_index": pivot,
        "forced_locator": forced_locator,
        "forcing_remainder": forcing_remainder,
        "forced_roots": forced_roots,
        "syzygy_sum_zero": syzygy_sum == [0],
        "pivot_forcing_remainder_zero": forcing_remainder == [0],
        "pivot_forcing_recovers_locator": forced_locator == locators[pivot],
        "pivot_forcing_roots_match": forced_roots == sorted(edge_blocks[pivot]),
    }


def projective_normalize(vector: tuple[int, ...], p: int) -> tuple[int, ...]:
    """Normalize a nonzero vector up to scalar."""
    for entry in vector:
        if entry % p:
            inv = pow(entry, -1, p)
            return tuple((value * inv) % p for value in vector)
    raise ValueError("cannot projectivize zero vector")


def functional_incidence_profile() -> dict:
    """Finite profile for the projective functional incidence reduction."""
    p, n, k = 7, 6, 4
    h_values = subgroup(p, n)
    projective_functionals = sorted(
        {
            projective_normalize(tuple(coeffs), p)
            for coeffs in itertools.product(range(p), repeat=k)
            if any(coeffs)
        }
    )
    subsets_by_size = {
        size: [tuple(subset) for subset in itertools.combinations(range(n), size)]
        for size in range(1, k)
    }
    basis_by_subset = {}
    for subsets in subsets_by_size.values():
        for subset in subsets:
            basis_by_subset[subset] = [
                [pow(h_values[idx], degree, p) for degree in range(k)]
                for idx in subset
            ]
    representation_counts = {
        size: {functional: 0 for functional in projective_functionals}
        for size in subsets_by_size
    }
    representing_subsets = {
        functional: {size: [] for size in subsets_by_size}
        for functional in projective_functionals
    }
    for size, subsets in subsets_by_size.items():
        for subset in subsets:
            basis = basis_by_subset[subset]
            basis_rank = matrix_rank_mod(basis, p)
            for functional in projective_functionals:
                if matrix_rank_mod(basis + [list(functional)], p) == basis_rank:
                    representation_counts[size][functional] += 1
                    representing_subsets[functional][size].append(subset)

    forbidden_small_disjoint = []
    for functional in projective_functionals:
        for left_size in subsets_by_size:
            for right_size in subsets_by_size:
                if left_size + right_size > k:
                    continue
                for left in representing_subsets[functional][left_size]:
                    left_set = set(left)
                    for right in representing_subsets[functional][right_size]:
                        if left_set.isdisjoint(right):
                            forbidden_small_disjoint.append(
                                {
                                    "functional": functional,
                                    "left": left,
                                    "right": right,
                                }
                            )
                            break
                    if forbidden_small_disjoint:
                        break
                if forbidden_small_disjoint:
                    break
            if forbidden_small_disjoint:
                break
        if forbidden_small_disjoint:
            break

    distribution = {}
    for size, counts in representation_counts.items():
        histogram: dict[int, int] = {}
        for count in counts.values():
            histogram[count] = histogram.get(count, 0) + 1
        distribution[size] = dict(sorted(histogram.items()))
    one_edge_incidence = {
        size: sum(counts.values())
        for size, counts in representation_counts.items()
    }
    expected_one_edge_incidence = {
        size: comb(n, size) * (p**size - 1) // (p - 1)
        for size in subsets_by_size
    }
    two_edge_disjoint_incidence = {}
    expected_two_edge_disjoint_incidence = {}
    for left_size in subsets_by_size:
        for right_size in subsets_by_size:
            key = f"{left_size},{right_size}"
            total = 0
            for functional in projective_functionals:
                for left in representing_subsets[functional][left_size]:
                    left_set = set(left)
                    for right in representing_subsets[functional][right_size]:
                        if left_set.isdisjoint(right):
                            total += 1
            common_dim = max(0, left_size + right_size - k)
            two_edge_disjoint_incidence[key] = total
            expected_two_edge_disjoint_incidence[key] = (
                0
                if common_dim == 0
                else comb(n, left_size)
                * comb(n - left_size, right_size)
                * (p**common_dim - 1)
                // (p - 1)
            )

    singleton_represented = [
        functional
        for functional, counts in representation_counts[1].items()
        if counts
    ]
    minimal_support_size = {
        functional: next(
            (
                size
                for size in sorted(subsets_by_size)
                if representation_counts[size][functional]
            ),
            None,
        )
        for functional in projective_functionals
    }
    minimal_supports = {
        functional: (
            representing_subsets[functional][minimal_support_size[functional]]
            if minimal_support_size[functional] is not None
            else []
        )
        for functional in projective_functionals
    }
    small_support_formula_failures = []
    small_support_bound_failures = []
    disjoint_minimal_support_failures = []
    for functional in projective_functionals:
        min_size = minimal_support_size[functional]
        if min_size is None:
            continue
        for size in subsets_by_size:
            actual = representation_counts[size][functional]
            if min_size + size <= k:
                expected = (
                    comb(n - min_size, size - min_size)
                    if size >= min_size
                    else 0
                )
                if actual != expected:
                    small_support_formula_failures.append(
                        {
                            "functional": functional,
                            "minimal_support": min_size,
                            "size": size,
                            "actual": actual,
                            "expected": expected,
                        }
                    )
            if 2 * size <= k:
                bound = comb(n - 1, size - 1)
                if actual > bound:
                    small_support_bound_failures.append(
                        {
                            "functional": functional,
                            "size": size,
                            "actual": actual,
                            "bound": bound,
                        }
                    )
            if min_size + size <= k:
                for minimal_support in minimal_supports[functional]:
                    minimal_set = set(minimal_support)
                    for subset in representing_subsets[functional][size]:
                        if minimal_set.isdisjoint(subset):
                            disjoint_minimal_support_failures.append(
                                {
                                    "functional": functional,
                                    "minimal_support": minimal_support,
                                    "size": size,
                                    "subset": subset,
                                }
                            )
                            break
                    if disjoint_minimal_support_failures:
                        break
            if disjoint_minimal_support_failures:
                break
        if disjoint_minimal_support_failures:
            break

    minimal_support_distribution: dict[int | None, int] = {}
    for min_size in minimal_support_size.values():
        minimal_support_distribution[min_size] = (
            minimal_support_distribution.get(min_size, 0) + 1
        )
    domain_evaluations = {
        projective_normalize(
            tuple(pow(x, degree, p) for degree in range(k)), p
        )
        for x in h_values
    }

    return {
        "p": p,
        "n": n,
        "k": k,
        "projective_functional_count": len(projective_functionals),
        "expected_projective_functional_count": (p**k - 1) // (p - 1),
        "representation_count_distribution": distribution,
        "one_edge_incidence": one_edge_incidence,
        "expected_one_edge_incidence": expected_one_edge_incidence,
        "one_edge_incidence_formula_holds": one_edge_incidence
        == expected_one_edge_incidence,
        "two_edge_disjoint_incidence": two_edge_disjoint_incidence,
        "expected_two_edge_disjoint_incidence": expected_two_edge_disjoint_incidence,
        "two_edge_disjoint_incidence_formula_holds": two_edge_disjoint_incidence
        == expected_two_edge_disjoint_incidence,
        "minimal_support_distribution": {
            "none" if size is None else str(size): count
            for size, count in sorted(
                minimal_support_distribution.items(),
                key=lambda item: -1 if item[0] is None else item[0],
            )
        },
        "max_representation_counts": {
            size: max(counts.values())
            for size, counts in representation_counts.items()
        },
        "small_support_formula_failures": small_support_formula_failures,
        "small_support_formula_holds": not small_support_formula_failures,
        "small_support_bound_failures": small_support_bound_failures,
        "small_support_bound_holds": not small_support_bound_failures,
        "disjoint_minimal_support_failures": disjoint_minimal_support_failures,
        "small_edge_isolation_holds": not disjoint_minimal_support_failures,
        "singleton_represented_count": len(singleton_represented),
        "domain_evaluation_count": len(domain_evaluations),
        "singleton_represented_are_domain_evaluations": set(singleton_represented)
        == domain_evaluations,
        "small_disjoint_representation_violations": forbidden_small_disjoint,
        "small_disjoint_representations_forbidden": not forbidden_small_disjoint,
    }


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


def simultaneous_fiber_profile(
    families: list[list[frozenset[int]]], a: int, domain_size: int
) -> dict:
    """Count a-subsets that are feasible for every row.

    For RS with a>=k, each feasible a-set determines at most one codeword in
    each row.  This profile computes the simultaneous support fiber and splits
    it according to whether the induced full supports are all exactly that
    a-set, i.e. the regular exact-row core.
    """
    total = 0
    regular_exact = 0
    row_irregular = 0
    max_row_choices = 0
    duplicate_choice_sets = 0
    for subset in itertools.combinations(range(domain_size), a):
        s_set = frozenset(subset)
        row_choices = [
            [support for support in family if s_set <= support]
            for family in families
        ]
        if any(not choices for choices in row_choices):
            continue
        total += 1
        max_row_choices = max(
            max_row_choices, max(len(choices) for choices in row_choices)
        )
        if any(len(choices) > 1 for choices in row_choices):
            duplicate_choice_sets += 1
        chosen = [choices[0] for choices in row_choices]
        if all(support == s_set for support in chosen):
            regular_exact += 1
        else:
            row_irregular += 1
    return {
        "simultaneous_a_sets": total,
        "regular_exact_a_sets": regular_exact,
        "row_irregular_a_sets": row_irregular,
        "max_row_choices_per_a_set": max_row_choices,
        "duplicate_choice_a_sets": duplicate_choice_sets,
    }


def interpolate_subset_poly(
    p: int, h_values: list[int], word: tuple[int, ...], subset: frozenset[int]
) -> list[int]:
    """Degree-<|subset| interpolant of word on subset."""
    out = [0]
    for idx in subset:
        xi = h_values[idx]
        basis = [1]
        denominator = 1
        for jdx in subset:
            if jdx == idx:
                continue
            xj = h_values[jdx]
            basis = poly_mul(basis, [(-xj) % p, 1], p)
            denominator = (denominator * (xi - xj)) % p
        scale = word[idx] * pow(denominator, p - 2, p)
        term = [(scale * coeff) % p for coeff in basis]
        out = poly_add(out, term, p)
    return trim_poly(out)


def top_syndrome(poly: list[int], k: int, a: int) -> tuple[int, ...]:
    """Coefficients in degrees k,...,a-1 of a degree-<a interpolant."""
    return tuple(poly[degree] if degree < len(poly) else 0 for degree in range(k, a))


def residue_moments(
    p: int,
    h_values: list[int],
    word: tuple[int, ...],
    subset: frozenset[int],
    sigma: int,
) -> tuple[int, ...]:
    """Weighted moments sum_s word(s) s^j / L'_S(s), j<sigma."""
    moments = []
    for power in range(sigma):
        total = 0
        for idx in subset:
            xi = h_values[idx]
            derivative = 1
            for jdx in subset:
                if jdx != idx:
                    derivative = (derivative * (xi - h_values[jdx])) % p
            total = (
                total
                + word[idx] * pow(xi, power, p) * pow(derivative, p - 2, p)
            ) % p
        moments.append(total)
    return tuple(moments)


def top_syndrome_from_moments(
    locator: list[int], moments: tuple[int, ...], k: int, a: int, p: int
) -> tuple[int, ...]:
    """Recover top interpolant coefficients from residue moments."""
    coeffs = locator + [0] * (a + 1 - len(locator))
    values = []
    for degree in range(k, a):
        total = 0
        for r in range(degree + 1, a + 1):
            moment_index = r - degree - 1
            total = (total + coeffs[r] * moments[moment_index]) % p
        values.append(total)
    return tuple(values)


def simultaneous_syndrome_profile(
    words: list[tuple[int, ...]],
    h_values: list[int],
    families: list[list[frozenset[int]]],
    k: int,
    a: int,
    p: int,
) -> dict:
    """Verify that simultaneous fibers are the common zero locus of syndromes."""
    simultaneous_zero = 0
    regular_exact = 0
    row_irregular = 0
    support_family_mismatches = 0
    moment_formula_mismatches = 0
    moment_zero_mismatches = 0
    for subset in itertools.combinations(range(len(h_values)), a):
        s_set = frozenset(subset)
        locator = poly_from_roots(p, [h_values[idx] for idx in s_set])
        full_supports = []
        row_zero = []
        for word in words:
            interpolant = interpolate_subset_poly(p, h_values, word, s_set)
            syndrome = top_syndrome(interpolant, k, a)
            moments = residue_moments(p, h_values, word, s_set, a - k)
            moment_syndrome = top_syndrome_from_moments(locator, moments, k, a, p)
            if moment_syndrome != syndrome:
                moment_formula_mismatches += 1
            if all(value == 0 for value in moments) != all(
                value == 0 for value in syndrome
            ):
                moment_zero_mismatches += 1
            is_zero = all(value == 0 for value in syndrome)
            row_zero.append(is_zero)
            if is_zero:
                full_supports.append(
                    frozenset(
                        idx
                        for idx, x in enumerate(h_values)
                        if eval_poly(tuple(interpolant), x, p) == word[idx]
                    )
                )
            else:
                full_supports.append(frozenset())
        family_contains = [
            any(s_set <= support for support in family)
            for family in families
        ]
        if row_zero != family_contains:
            support_family_mismatches += 1
        if all(row_zero):
            simultaneous_zero += 1
            if all(support == s_set for support in full_supports):
                regular_exact += 1
            else:
                row_irregular += 1
    return {
        "simultaneous_syndrome_zero_a_sets": simultaneous_zero,
        "regular_exact_a_sets": regular_exact,
        "row_irregular_a_sets": row_irregular,
        "support_family_mismatches": support_family_mismatches,
        "moment_formula_mismatches": moment_formula_mismatches,
        "moment_zero_mismatches": moment_zero_mismatches,
        "syndrome_length": a - k,
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
    y_values = tuple(eval_poly(tuple(y_poly), x, p) for x in h_values)
    positions = {x: idx for idx, x in enumerate(h_values)}
    coset_index_by_position = {}
    for coset_index, alpha in enumerate(quotient_values):
        for x in cosets[alpha]:
            coset_index_by_position[positions[x]] = coset_index

    rows = []
    polynomials = []
    advertised_supports = []
    advertised_support_indices = set()
    max_interpolant_degree = -1
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
        agreement_set = set(agreement)
        support_indices = frozenset(positions[x] for x in support)
        interpolant = interpolate_subset_poly(p, h_values, y_values, support_indices)
        syndrome = top_syndrome(interpolant, k, a)
        moments = residue_moments(p, h_values, y_values, support_indices, sigma)
        max_interpolant_degree = max(max_interpolant_degree, poly_degree(interpolant))
        rows.append(
            {
                "quotient_subset": quotient_subset,
                "degree": poly_degree(p_poly),
                "interpolant_degree": poly_degree(interpolant),
                "interpolant_matches_codeword": trim_poly(interpolant[:])
                == trim_poly(p_poly[:]),
                "top_syndrome_zero": all(value == 0 for value in syndrome),
                "residue_moments_zero": all(value == 0 for value in moments),
                "advertised_support_size": len(support),
                "agreement_size": len(agreement),
                "advertised_support_contained": support.issubset(agreement_set),
                "advertised_support_exact": support == agreement_set,
            }
        )
        polynomials.append(tuple(trim_poly(p_poly[:])))
        advertised_supports.append(frozenset(support))
        advertised_support_indices.add(support_indices)

    expected_count = comb(quotient_order - 1, ell)
    formula_count = aligned_quotient_packet(
        quotient_order, ell, mu=2, a=a, tau=partial, fiber_size=fiber_size
    )
    zero_moment_supports = 0
    exact_zero_moment_supports = 0
    overagreement_zero_moment_supports = 0
    advertised_zero_moment_supports = 0
    moment_zero_mismatches = 0
    occupancy_hist: dict[tuple[int, ...], int] = {}
    residual_occupancy_hist: dict[tuple[int, ...], int] = {}
    zero_moment_polynomials = set()
    advertised_zero_moment_polynomials = set()
    residual_zero_moment_polynomials = set()
    agreement_size_hist: dict[int, int] = {}
    zero_moment_support_index_sets = []
    for subset in itertools.combinations(range(n), a):
        support_indices = frozenset(subset)
        interpolant = interpolate_subset_poly(p, h_values, y_values, support_indices)
        syndrome_zero = all(value == 0 for value in top_syndrome(interpolant, k, a))
        moments_zero = all(
            value == 0
            for value in residue_moments(p, h_values, y_values, support_indices, sigma)
        )
        if syndrome_zero != moments_zero:
            moment_zero_mismatches += 1
        if not syndrome_zero:
            continue
        zero_moment_supports += 1
        zero_moment_support_index_sets.append(support_indices)
        interpolant_key = tuple(trim_poly(interpolant[:]))
        zero_moment_polynomials.add(interpolant_key)
        full_support = frozenset(
            idx
            for idx, x in enumerate(h_values)
            if eval_poly(tuple(interpolant), x, p) == y_values[idx]
        )
        agreement_size_hist[len(full_support)] = (
            agreement_size_hist.get(len(full_support), 0) + 1
        )
        if full_support == support_indices:
            exact_zero_moment_supports += 1
        else:
            overagreement_zero_moment_supports += 1
        if support_indices in advertised_support_indices:
            advertised_zero_moment_supports += 1
            advertised_zero_moment_polynomials.add(interpolant_key)
        else:
            residual_zero_moment_polynomials.add(interpolant_key)
        occupancy = [0] * quotient_order
        for idx in support_indices:
            occupancy[coset_index_by_position[idx]] += 1
        profile = tuple(sorted(occupancy, reverse=True))
        occupancy_hist[profile] = occupancy_hist.get(profile, 0) + 1
        if support_indices not in advertised_support_indices:
            residual_occupancy_hist[profile] = (
                residual_occupancy_hist.get(profile, 0) + 1
            )
    active_scale_rows = []
    active_quotient_supports = set()
    for active_m in active_remainder_scales(n, k, a):
        active_cosets: dict[int, list[int]] = {}
        for x in h_values:
            active_cosets.setdefault(pow(x, active_m, p), []).append(x)
        active_index_by_position = {}
        for coset_index, alpha in enumerate(active_cosets):
            for x in active_cosets[alpha]:
                active_index_by_position[positions[x]] = coset_index
        active_n = len(active_cosets)
        active_ell = a // active_m
        active_u = a - active_m * active_ell
        shape_values = [active_m] * active_ell
        if active_u:
            shape_values.append(active_u)
        shape_values.extend([0] * (active_n - len(shape_values)))
        active_shape = tuple(sorted(shape_values, reverse=True))
        matching_supports = set()
        for support_indices in zero_moment_support_index_sets:
            occupancy = [0] * active_n
            for idx in support_indices:
                occupancy[active_index_by_position[idx]] += 1
            if tuple(sorted(occupancy, reverse=True)) == active_shape:
                matching_supports.add(support_indices)
        active_quotient_supports.update(matching_supports)
        active_scale_rows.append(
            {
                "M": active_m,
                "shape": list(active_shape),
                "zero_moment_supports_with_shape": len(matching_supports),
            }
        )
    residual_supports = set(zero_moment_support_index_sets) - active_quotient_supports

    def pair_count(left: set[frozenset[int]], right: set[frozenset[int]]) -> int:
        return sum(1 for s_left in left for s_right in right if len(s_left & s_right) >= a)

    zero_support_set = set(zero_moment_support_index_sets)
    equal_row_profile = {
        "all_supports": len(zero_support_set),
        "all_cartesian_pairs": len(zero_support_set) ** 2,
        "all_interleaved_pairs": pair_count(zero_support_set, zero_support_set),
        "quotient_supports": len(active_quotient_supports),
        "quotient_interleaved_pairs": pair_count(
            active_quotient_supports, active_quotient_supports
        ),
        "residual_supports": len(residual_supports),
        "residual_interleaved_pairs": pair_count(residual_supports, residual_supports),
        "mixed_interleaved_pairs": pair_count(
            active_quotient_supports, residual_supports
        )
        + pair_count(residual_supports, active_quotient_supports),
    }
    dilation_rows = []
    for shift, multiplier in enumerate(h_values):
        permutation = {
            idx: positions[(multiplier * x) % p]
            for idx, x in enumerate(h_values)
        }

        def dilate_family(family: set[frozenset[int]]) -> set[frozenset[int]]:
            return {frozenset(permutation[idx] for idx in support) for support in family}

        dilated_zero = dilate_family(zero_support_set)
        dilated_quotient = dilate_family(active_quotient_supports)
        dilated_residual = dilate_family(residual_supports)
        dilation_rows.append(
            {
                "shift": shift,
                "all_overlap": len(zero_support_set & dilated_zero),
                "quotient_overlap": len(active_quotient_supports & dilated_quotient),
                "residual_overlap": len(residual_supports & dilated_residual),
                "mixed_overlap": len(active_quotient_supports & dilated_residual)
                + len(residual_supports & dilated_quotient),
            }
        )
    nontrivial_dilations = [row for row in dilation_rows if row["shift"] != 0]
    dilation_profile = {
        "rows": dilation_rows,
        "max_nontrivial_all_overlap": max(
            (row["all_overlap"] for row in nontrivial_dilations), default=0
        ),
        "max_nontrivial_residual_overlap": max(
            (row["residual_overlap"] for row in nontrivial_dilations), default=0
        ),
        "max_nontrivial_mixed_overlap": max(
            (row["mixed_overlap"] for row in nontrivial_dilations), default=0
        ),
    }
    zero_moment_profile = {
        "all_a_subsets": comb(n, a),
        "zero_moment_supports": zero_moment_supports,
        "distinct_zero_moment_polynomials": len(zero_moment_polynomials),
        "advertised_zero_moment_polynomials": len(advertised_zero_moment_polynomials),
        "residual_zero_moment_polynomials": len(residual_zero_moment_polynomials),
        "advertised_residual_polynomial_overlap": len(
            advertised_zero_moment_polynomials & residual_zero_moment_polynomials
        ),
        "exact_zero_moment_supports": exact_zero_moment_supports,
        "overagreement_zero_moment_supports": overagreement_zero_moment_supports,
        "advertised_zero_moment_supports": advertised_zero_moment_supports,
        "extra_zero_moment_supports": zero_moment_supports
        - advertised_zero_moment_supports,
        "moment_zero_mismatches": moment_zero_mismatches,
        "occupancy_histogram": [
            {"occupancy": list(profile), "count": count}
            for profile, count in sorted(occupancy_hist.items(), reverse=True)
        ],
        "residual_occupancy_histogram": [
            {"occupancy": list(profile), "count": count}
            for profile, count in sorted(residual_occupancy_hist.items(), reverse=True)
        ],
        "agreement_size_histogram": [
            {"agreement": size, "count": count}
            for size, count in sorted(agreement_size_hist.items())
        ],
        "active_quotient_shape_profile": active_scale_rows,
        "active_quotient_shape_union": len(active_quotient_supports),
        "active_quotient_shape_residual": zero_moment_supports
        - len(active_quotient_supports),
        "equal_row_profile": equal_row_profile,
        "dilation_profile": dilation_profile,
    }
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
        "max_interpolant_degree": max_interpolant_degree,
        "min_agreement": min(row["agreement_size"] for row in rows),
        "all_degrees_below_k": all(row["degree"] < k for row in rows),
        "all_interpolants_match_codewords": all(
            row["interpolant_matches_codeword"] for row in rows
        ),
        "all_advertised_supports_zero_syndrome": all(
            row["top_syndrome_zero"] for row in rows
        ),
        "all_advertised_supports_zero_moments": all(
            row["residue_moments_zero"] for row in rows
        ),
        "all_advertised_supports_size_a": all(
            row["advertised_support_size"] == a for row in rows
        ),
        "all_advertised_supports_contained": all(
            row["advertised_support_contained"] for row in rows
        ),
        "all_advertised_supports_exact": all(
            row["advertised_support_exact"] for row in rows
        ),
        "zero_moment_profile": zero_moment_profile,
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
    fiber_profile = simultaneous_fiber_profile(families, a, n)
    syndrome_profile = simultaneous_syndrome_profile(
        [tuple(word1), tuple(word2)], h_values, families, k, a, p
    )
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
        "simultaneous_fiber_profile": fiber_profile,
        "simultaneous_syndrome_profile": syndrome_profile,
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
    support_pair_profile = support_pair_rank_profile()
    support_cluster_profile = support_cluster_rank_profile()
    connected_cluster_profile = connected_cluster_count_profile()
    closure_signature = closure_signature_profile()
    cyclic_rank_deficit = cyclic_overlap_rank_deficit_profile()
    constant_ratio_triangles = constant_ratio_triangle_profile()
    full_rank_necklaces = full_rank_cyclic_necklace_profile()
    rank_deficient_necklaces = rank_deficient_cyclic_necklace_profile()
    clean_cycles = clean_cycle_rank_profile()
    locator_syzygy_witness = locator_syzygy_witness_profile()
    functional_incidence = functional_incidence_profile()
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
        "dithered_quotient_witness_interpolants": dithered_witness[
            "all_interpolants_match_codewords"
        ],
        "dithered_quotient_witness_syndromes": dithered_witness[
            "all_advertised_supports_zero_syndrome"
        ]
        and dithered_witness["all_advertised_supports_zero_moments"],
        "dithered_quotient_witness_exact_support": dithered_witness[
            "all_advertised_supports_size_a"
        ]
        and dithered_witness["all_advertised_supports_contained"]
        and dithered_witness["all_advertised_supports_exact"],
        "dithered_quotient_zero_moment_profile": dithered_witness[
            "zero_moment_profile"
        ]["zero_moment_supports"]
        == 42
        and dithered_witness["zero_moment_profile"]["exact_zero_moment_supports"]
        == 42
        and dithered_witness["zero_moment_profile"]["advertised_zero_moment_supports"]
        == dithered_witness["constructed_count"]
        and dithered_witness["zero_moment_profile"]["extra_zero_moment_supports"]
        == 39
        and dithered_witness["zero_moment_profile"]["moment_zero_mismatches"]
        == 0,
        "dithered_quotient_zero_moment_distinct": dithered_witness[
            "zero_moment_profile"
        ]["distinct_zero_moment_polynomials"]
        == 42
        and dithered_witness["zero_moment_profile"][
            "advertised_zero_moment_polynomials"
        ]
        == 3
        and dithered_witness["zero_moment_profile"][
            "residual_zero_moment_polynomials"
        ]
        == 39
        and dithered_witness["zero_moment_profile"][
            "advertised_residual_polynomial_overlap"
        ]
        == 0
        and dithered_witness["zero_moment_profile"]["agreement_size_histogram"]
        == [{"agreement": 9, "count": 42}],
        "dithered_quotient_active_shape_profile": dithered_witness[
            "zero_moment_profile"
        ]["active_quotient_shape_profile"]
        == [
            {"M": 4, "shape": [4, 4, 1, 0], "zero_moment_supports_with_shape": 3},
            {"M": 8, "shape": [8, 1], "zero_moment_supports_with_shape": 1},
        ]
        and dithered_witness["zero_moment_profile"]["active_quotient_shape_union"]
        == 3
        and dithered_witness["zero_moment_profile"]["active_quotient_shape_residual"]
        == 39,
        "dithered_quotient_equal_row_diagonal": dithered_witness[
            "zero_moment_profile"
        ]["equal_row_profile"]
        == {
            "all_supports": 42,
            "all_cartesian_pairs": 1764,
            "all_interleaved_pairs": 42,
            "quotient_supports": 3,
            "quotient_interleaved_pairs": 3,
            "residual_supports": 39,
            "residual_interleaved_pairs": 39,
            "mixed_interleaved_pairs": 0,
        },
        "dithered_quotient_dilation_separates_residuals": dithered_witness[
            "zero_moment_profile"
        ]["dilation_profile"]["rows"][0]
        == {
            "shift": 0,
            "all_overlap": 42,
            "quotient_overlap": 3,
            "residual_overlap": 39,
            "mixed_overlap": 0,
        }
        and dithered_witness["zero_moment_profile"]["dilation_profile"][
            "max_nontrivial_all_overlap"
        ]
        == 0
        and dithered_witness["zero_moment_profile"]["dilation_profile"][
            "max_nontrivial_residual_overlap"
        ]
        == 0
        and dithered_witness["zero_moment_profile"]["dilation_profile"][
            "max_nontrivial_mixed_overlap"
        ]
        == 0,
        "dithered_quotient_witness_agreement": dithered_witness[
            "all_advertised_supports_size_a"
        ]
        and dithered_witness["all_advertised_supports_contained"],
        "dithered_quotient_witness_distinct": dithered_witness[
            "distinct_polynomials"
        ]
        == dithered_witness["constructed_count"],
        "support_pair_rank_counts": support_pair_profile["all_counts_match"],
        "support_pair_rank_independence_below_k": support_pair_profile[
            "below_k_independent"
        ],
        "support_pair_rank_surplus_above_k": support_pair_profile[
            "above_k_surplus"
        ],
        "support_cluster_rank_counts": support_cluster_profile[
            "all_counts_bounded"
        ],
        "support_cluster_rank_diagonal_zero_loss": support_cluster_profile[
            "diagonal_component_zero_loss"
        ],
        "support_cluster_rank_nondiagonal_extra_loss": support_cluster_profile[
            "nondiagonal_connected_extra_loss"
        ],
        "support_cluster_rank_union_excess_tradeoff": support_cluster_profile[
            "connected_union_excess_tradeoff"
        ],
        "support_cluster_rank_distinct_capacity": support_cluster_profile[
            "distinct_support_capacity"
        ],
        "support_cluster_rank_connected_tight": support_cluster_profile[
            "connected_high_overlap_tight"
        ],
        "support_cluster_rank_chain_loss": support_cluster_profile[
            "connected_chain_loss"
        ],
        "support_cluster_rank_aggregate_closure": support_cluster_profile[
            "aggregate_union_closure_merges"
        ],
        "support_cluster_rank_closure_counts": support_cluster_profile[
            "closure_rank_counts"
        ],
        "support_cluster_rank_closure_sharpens": support_cluster_profile[
            "aggregate_union_closure_sharpens"
        ],
        "support_cluster_rank_low_overlap_loose": support_cluster_profile[
            "low_overlap_bound_can_be_loose"
        ],
        "connected_cluster_count_bound": connected_cluster_profile[
            "all_counts_bounded"
        ],
        "connected_cluster_count_diagonal": connected_cluster_profile[
            "diagonal_count_exact"
        ],
        "connected_cluster_count_positive_excess": connected_cluster_profile[
            "has_positive_excess_clusters"
        ],
        "connected_cluster_bound_clears_positive_excess": connected_cluster_profile[
            "positive_excess_bound_below_diagonal"
        ],
        "connected_cluster_actual_clears_positive_excess": connected_cluster_profile[
            "positive_excess_actual_below_diagonal"
        ],
        "closure_signature_counts_bound": closure_signature["all_counts_bounded"],
        "closure_signature_total": closure_signature["total_tuples"]
        == closure_signature["expected_total_tuples"],
        "closure_signature_has_negative_excess": closure_signature[
            "has_negative_global_excess"
        ],
        "closure_signature_has_zero_excess": closure_signature[
            "has_zero_global_excess"
        ],
        "closure_signature_has_positive_excess": closure_signature[
            "has_positive_global_excess"
        ],
        "closure_signature_has_cyclic_overlap_graph": closure_signature[
            "has_cyclic_overlap_graph"
        ],
        "closure_signature_forest_rank_cancels": closure_signature[
            "forest_rank_cancels_overlap_defect"
        ],
        "closure_signature_two_part_rank_cancels": closure_signature[
            "two_part_rank_cancels_overlap_defect"
        ],
        "closure_signature_rank_corrected_nonnegative": closure_signature[
            "rank_corrected_excess_nonnegative"
        ],
        "cyclic_rank_deficit_three_part_cycles": cyclic_rank_deficit[
            "all_three_part_cycles"
        ],
        "cyclic_rank_deficit_rank_formula": cyclic_rank_deficit[
            "rank_formula_holds"
        ],
        "cyclic_rank_deficit_excess_formula": cyclic_rank_deficit[
            "excess_formula_holds"
        ],
        "cyclic_rank_deficit_exponent_formula": cyclic_rank_deficit[
            "exponent_formula_holds"
        ],
        "cyclic_rank_deficit_negative_exists": cyclic_rank_deficit[
            "has_negative_rank_corrected_excess"
        ],
        "cyclic_rank_deficit_grows": cyclic_rank_deficit[
            "deficit_grows_after_k_three"
        ],
        "cyclic_rank_deficit_relative_exponent": cyclic_rank_deficit[
            "relative_exponent_is_block_size"
        ],
        "cyclic_rank_deficit_below_diagonal": cyclic_rank_deficit[
            "generic_triangle_family_below_diagonal"
        ],
        "constant_ratio_triangle_counts_bound": constant_ratio_triangles[
            "all_counts_bounded"
        ],
        "constant_ratio_triangle_degree_bound": constant_ratio_triangles[
            "all_buckets_degree_bounded"
        ],
        "constant_ratio_triangle_exact_clears": constant_ratio_triangles[
            "exact_relative_below_diagonal"
        ],
        "constant_ratio_triangle_bound_clears": constant_ratio_triangles[
            "bound_relative_below_diagonal"
        ],
        "constant_ratio_triangle_exponent_gap": constant_ratio_triangles[
            "exponent_gap_formula"
        ],
        "constant_ratio_triangle_combined_exact_clears": constant_ratio_triangles[
            "combined_exact_relative_below_diagonal"
        ],
        "constant_ratio_triangle_combined_bound_clears": constant_ratio_triangles[
            "combined_bound_relative_below_diagonal"
        ],
        "full_rank_necklace_closed_parts": full_rank_necklaces[
            "all_closed_parts_singleton"
        ],
        "full_rank_necklace_cycle_lengths": full_rank_necklaces[
            "covers_cycle_lengths_three_through_six"
        ],
        "full_rank_necklace_cyclic_overlap": full_rank_necklaces[
            "all_overlap_graphs_cyclic"
        ],
        "full_rank_necklace_locator_rank": full_rank_necklaces[
            "all_locators_full_rank"
        ],
        "full_rank_necklace_cross_rank": full_rank_necklaces[
            "cross_rank_formula_holds"
        ],
        "full_rank_necklace_exponent_gap": full_rank_necklaces[
            "exponent_gap_formula_holds"
        ],
        "full_rank_necklace_below_diagonal": full_rank_necklaces[
            "relative_bound_below_diagonal"
        ],
        "rank_deficient_necklace_cycle_lengths": rank_deficient_necklaces[
            "covers_cycle_lengths_three_through_six"
        ],
        "rank_deficient_necklace_coefficients": rank_deficient_necklaces[
            "coefficient_choice_formula_holds"
        ],
        "rank_deficient_necklace_exponent_gap": rank_deficient_necklaces[
            "exponent_gap_lower_bound_formula_holds"
        ],
        "rank_deficient_necklace_below_diagonal": rank_deficient_necklaces[
            "relative_bound_below_diagonal"
        ],
        "clean_cycle_shape": clean_cycles["all_clean_cycles"],
        "clean_cycle_cross_rank": clean_cycles["cross_rank_formula_holds"],
        "clean_cycle_rank_corrected_exponent": clean_cycles[
            "rank_corrected_exponent_formula_holds"
        ],
        "clean_cycle_exponent_gap": clean_cycles["exponent_gap_formula_holds"],
        "clean_cycle_has_uneven_edges": clean_cycles["contains_uneven_edges"],
        "clean_cycle_has_private_mass": clean_cycles["contains_private_mass"],
        "clean_cycle_two_edge_lower_bound": clean_cycles[
            "two_edge_lower_bound_holds"
        ],
        "clean_cycle_dual_defect": clean_cycles["dual_defect_formula_holds"],
        "clean_cycle_two_edge_defect_bound": clean_cycles[
            "two_edge_defect_bound_holds"
        ],
        "clean_cycle_small_pair_full_rank": clean_cycles[
            "small_pair_forces_full_rank"
        ],
        "clean_cycle_has_small_pair_case": clean_cycles[
            "contains_small_pair_case"
        ],
        "clean_cycle_one_edge_tuple_saves": clean_cycles[
            "one_edge_tuple_bound_saves"
        ],
        "clean_cycle_one_edge_saving_formula": clean_cycles[
            "one_edge_saving_formula_holds"
        ],
        "clean_cycle_one_edge_relative_clears_nontriangle": clean_cycles[
            "one_edge_relative_bound_clears_nontriangle_examples"
        ],
        "clean_cycle_one_edge_triangle_coarse": clean_cycles[
            "one_edge_relative_bound_records_triangle_coarseness"
        ],
        "clean_cycle_two_edge_tuple_saves": clean_cycles[
            "two_edge_tuple_bound_saves_on_examples"
        ],
        "clean_cycle_two_edge_small_pair_forbidden": clean_cycles[
            "two_edge_tuple_bound_forbids_small_pair_examples"
        ],
        "clean_cycle_two_edge_relative_clears_nontriangle": clean_cycles[
            "two_edge_relative_bound_clears_nontriangle_examples"
        ],
        "clean_cycle_two_edge_triangle_coarse": clean_cycles[
            "two_edge_relative_bound_records_triangle_coarseness"
        ],
        "clean_cycle_all_edge_selected_rank_full": clean_cycles[
            "all_edge_selected_rank_full_on_examples"
        ],
        "clean_cycle_selected_syzygy_formula": clean_cycles[
            "selected_syzygy_kernel_formula_holds"
        ],
        "clean_cycle_selected_syzygy_no_excess": clean_cycles[
            "selected_syzygy_no_excess_on_examples"
        ],
        "clean_cycle_all_edge_tuple_saves": clean_cycles[
            "all_edge_full_rank_tuple_bound_saves_on_examples"
        ],
        "clean_cycle_all_edge_relative_clears": clean_cycles[
            "all_edge_full_rank_relative_clears_examples"
        ],
        "clean_cycle_all_edge_clears_triangle": clean_cycles[
            "all_edge_full_rank_clears_triangle_example"
        ],
        "functional_incidence_projective_count": functional_incidence[
            "projective_functional_count"
        ]
        == functional_incidence["expected_projective_functional_count"],
        "functional_incidence_singletons": functional_incidence[
            "singleton_represented_count"
        ]
        == functional_incidence["domain_evaluation_count"]
        and functional_incidence["singleton_represented_are_domain_evaluations"],
        "functional_incidence_small_disjoint_forbidden": functional_incidence[
            "small_disjoint_representations_forbidden"
        ],
        "functional_incidence_small_support_formula": functional_incidence[
            "small_support_formula_holds"
        ],
        "functional_incidence_small_support_bound": functional_incidence[
            "small_support_bound_holds"
        ],
        "functional_incidence_small_edge_isolation": functional_incidence[
            "small_edge_isolation_holds"
        ],
        "functional_incidence_one_edge_formula": functional_incidence[
            "one_edge_incidence_formula_holds"
        ],
        "functional_incidence_two_edge_disjoint_formula": functional_incidence[
            "two_edge_disjoint_incidence_formula_holds"
        ],
        "locator_syzygy_witness_has_excess": locator_syzygy_witness[
            "has_nontrivial_syzygy_excess"
        ],
        "locator_syzygy_witness_rank_defect": locator_syzygy_witness[
            "rank_defect_equals_syzygy_excess"
        ],
        "locator_syzygy_witness_necklace_rank": locator_syzygy_witness[
            "necklace_locator_rank_matches_selected_rank"
        ],
        "locator_syzygy_witness_sum_zero": locator_syzygy_witness[
            "syzygy_sum_zero"
        ],
        "locator_syzygy_witness_pivot_remainder": locator_syzygy_witness[
            "pivot_forcing_remainder_zero"
        ],
        "locator_syzygy_witness_pivot_locator": locator_syzygy_witness[
            "pivot_forcing_recovers_locator"
        ],
        "locator_syzygy_witness_pivot_roots": locator_syzygy_witness[
            "pivot_forcing_roots_match"
        ],
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
        "rs_witness_simultaneous_fiber_surjects": witness[
            "simultaneous_fiber_profile"
        ]["simultaneous_a_sets"]
        >= witness["interleaved"],
        "rs_witness_regular_core_is_exact_fiber": witness[
            "simultaneous_fiber_profile"
        ]["regular_exact_a_sets"]
        == witness["regular_irregular_profile"]["regular_exact_row_count"],
        "rs_witness_fiber_uniqueness": witness[
            "simultaneous_fiber_profile"
        ]["max_row_choices_per_a_set"]
        == 1
        and witness["simultaneous_fiber_profile"]["duplicate_choice_a_sets"] == 0,
        "rs_witness_syndrome_matches_fiber": witness[
            "simultaneous_syndrome_profile"
        ]["simultaneous_syndrome_zero_a_sets"]
        == witness["simultaneous_fiber_profile"]["simultaneous_a_sets"]
        and witness["simultaneous_syndrome_profile"]["regular_exact_a_sets"]
        == witness["simultaneous_fiber_profile"]["regular_exact_a_sets"]
        and witness["simultaneous_syndrome_profile"]["row_irregular_a_sets"]
        == witness["simultaneous_fiber_profile"]["row_irregular_a_sets"],
        "rs_witness_syndrome_matches_support_families": witness[
            "simultaneous_syndrome_profile"
        ]["support_family_mismatches"]
        == 0,
        "rs_witness_moments_match_syndromes": witness[
            "simultaneous_syndrome_profile"
        ]["moment_formula_mismatches"]
        == 0
        and witness["simultaneous_syndrome_profile"]["moment_zero_mismatches"]
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
        "support_pair_rank_profile": support_pair_profile,
        "support_cluster_rank_profile": support_cluster_profile,
        "connected_cluster_count_profile": connected_cluster_profile,
        "closure_signature_profile": closure_signature,
        "cyclic_overlap_rank_deficit_profile": cyclic_rank_deficit,
        "constant_ratio_triangle_profile": constant_ratio_triangles,
        "full_rank_cyclic_necklace_profile": full_rank_necklaces,
        "rank_deficient_cyclic_necklace_profile": rank_deficient_necklaces,
        "clean_cycle_rank_profile": clean_cycles,
        "locator_syzygy_witness_profile": locator_syzygy_witness,
        "functional_incidence_profile": functional_incidence,
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
            f"max_interpolant_degree={dq_witness['max_interpolant_degree']}, "
            f"min_agreement={dq_witness['min_agreement']}, "
            f"exact_supports={dq_witness['all_advertised_supports_exact']}, "
            f"zero_moments={dq_witness['all_advertised_supports_zero_moments']}"
        )
        qprof = dq_witness["zero_moment_profile"]
        dprof = qprof["dilation_profile"]
        print(
            "    quotient word zero-moment profile: "
            f"all_a_subsets={qprof['all_a_subsets']}, "
            f"zero={qprof['zero_moment_supports']}, "
            f"advertised={qprof['advertised_zero_moment_supports']}, "
            f"extra={qprof['extra_zero_moment_supports']}, "
            f"distinct_polys={qprof['distinct_zero_moment_polynomials']}, "
            f"residual_polys={qprof['residual_zero_moment_polynomials']}, "
            f"active_shapes={qprof['active_quotient_shape_profile']}, "
            f"active_shape_residual={qprof['active_quotient_shape_residual']}, "
            f"residual_occupancy={qprof['residual_occupancy_histogram']}, "
            f"equal_row={qprof['equal_row_profile']}, "
            f"dilation_identity={dprof['rows'][0]}, "
            f"max_nontrivial_dilation=({dprof['max_nontrivial_all_overlap']}, "
            f"{dprof['max_nontrivial_residual_overlap']}, "
            f"{dprof['max_nontrivial_mixed_overlap']})"
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
        sp = result["support_pair_rank_profile"]
        sp_rows = [
            {
                "r": row["intersection"],
                "dim": row["expected_dimension"],
                "exp": row["probability_exponent"],
                "count": row["brute_count"],
            }
            for row in sp["rows"]
        ]
        print(
            "  support-pair rank profile: "
            f"F_{sp['p']}, n={sp['n']}, k={sp['k']}, a={sp['a']}, rows={sp_rows}"
        )
        sc = result["support_cluster_rank_profile"]
        sc_rows = [
            {
                "name": row["name"],
                "components": row["components"],
                "closure_components": row["closure_components"],
                "union": row["union_size"],
                "excess": row["union_excess"],
                "distinct": row["distinct_supports"],
                "dim_bound": row["dimension_upper_bound"],
                "closure_dim_bound": row["closure_dimension_upper_bound"],
                "count": row["brute_count"],
                "bound": row["count_upper_bound"],
                "closure_bound": row["closure_count_upper_bound"],
            }
            for row in sc["rows"]
        ]
        print(
            "  support-cluster rank profile: "
            f"F_{sc['p']}, n={sc['n']}, k={sc['k']}, a={sc['a']}, rows={sc_rows}"
        )
        cc = result["connected_cluster_count_profile"]
        print(
            "  connected cluster count profile: "
            f"n={cc['n']}, k={cc['k']}, a={cc['a']}, "
            f"tuple_size={cc['tuple_size']}, q={cc['moment_q']}, mu={cc['mu']}, "
            f"positive_actual={cc['positive_actual_relative_to_diagonal']}, "
            f"positive_bound={cc['positive_bound_relative_to_diagonal']}, "
            f"rows={cc['rows']}"
        )
        cs = result["closure_signature_profile"]
        print(
            "  closure signature profile: "
            f"F_{cs['p']}, n={cs['n']}, k={cs['k']}, a={cs['a']}, "
            f"tuple_size={cs['tuple_size']}, rows={cs['rows']}"
        )
        cyc = result["cyclic_overlap_rank_deficit_profile"]
        print(
            "  cyclic overlap rank-deficit profile: "
            f"F_{cyc['p']}, n={cyc['n']}, rows={cyc['rows']}"
        )
        const_ratio = result["constant_ratio_triangle_profile"]
        print(
            "  constant-ratio triangle profile: "
            f"F_{const_ratio['p']}, n={const_ratio['n']}, "
            f"rows={const_ratio['rows']}"
        )
        necklaces = result["full_rank_cyclic_necklace_profile"]
        print(
            "  full-rank cyclic necklace profile: "
            f"F_{necklaces['p']}, n={necklaces['n']}, "
            f"rows={necklaces['rows']}"
        )
        deficient_necklaces = result["rank_deficient_cyclic_necklace_profile"]
        print(
            "  rank-deficient cyclic necklace profile: "
            f"F_{deficient_necklaces['p']}, n={deficient_necklaces['n']}, "
            f"rows={deficient_necklaces['rows']}"
        )
        clean_cycles = result["clean_cycle_rank_profile"]
        print(
            "  clean simple-cycle rank profile: "
            f"F_{clean_cycles['p']}, n={clean_cycles['n']}, "
            f"rows={clean_cycles['rows']}"
        )
        syz = result["locator_syzygy_witness_profile"]
        print(
            "  locator syzygy witness: "
            f"F_{syz['p']}, n={syz['n']}, k={syz['k']}, "
            f"blocks={syz['edge_blocks']}, locators={syz['locators']}, "
            f"rank={syz['selected_rank']}, "
            f"expected_full={syz['expected_full_rank']}, "
            f"kernel={syz['syzygy_kernel_dim']}, "
            f"excess={syz['syzygy_kernel_excess']}, "
            f"pivot={syz['pivot_index']}, "
            f"forced_locator={syz['forced_locator']}, "
            f"forced_roots={syz['forced_roots']}"
        )
        finc = result["functional_incidence_profile"]
        print(
            "  functional incidence profile: "
            f"F_{finc['p']}, n={finc['n']}, k={finc['k']}, "
            f"projective={finc['projective_functional_count']}, "
            f"max_counts={finc['max_representation_counts']}, "
            f"one_edge={finc['one_edge_incidence']}, "
            f"two_edge_disjoint={finc['two_edge_disjoint_incidence']}, "
            f"small_disjoint_forbidden={finc['small_disjoint_representations_forbidden']}"
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
        fib = w["simultaneous_fiber_profile"]
        print(
            "    simultaneous fiber: "
            f"a_sets={fib['simultaneous_a_sets']}, "
            f"regular_exact={fib['regular_exact_a_sets']}, "
            f"row_irregular={fib['row_irregular_a_sets']}, "
            f"max_row_choices={fib['max_row_choices_per_a_set']}"
        )
        syn = w["simultaneous_syndrome_profile"]
        print(
            "    locator syndromes: "
            f"zero_a_sets={syn['simultaneous_syndrome_zero_a_sets']}, "
            f"regular_exact={syn['regular_exact_a_sets']}, "
            f"row_irregular={syn['row_irregular_a_sets']}, "
            f"mismatches={syn['support_family_mismatches']}, "
            f"moment_formula_mismatches={syn['moment_formula_mismatches']}, "
            f"moment_zero_mismatches={syn['moment_zero_mismatches']}"
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
