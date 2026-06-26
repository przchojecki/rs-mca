#!/usr/bin/env python3
"""Verify the F1 arbitrary-anchor locator-split and sunflower packet.

This checks the finite packet in
experimental/notes/f1/f1_arbitrary_anchor_locator_split.md over
F_17[t]/(t^2-3).  It verifies:

* two supports with the same monic-anchor readout modulo hatE split into
  different support-wise bad slopes under an arbitrary anchor;
* the core-k sunflower construction realizes floor((n-k)/sigma) bad slopes;
* the core-k choice maximizes the sunflower floor among all core sizes c<=k.
* a non-sunflower k-degenerate support packing also realizes the same
  floor, confirming that the remaining obstruction must use dense overlaps.
* high-overlap pairs are possible exactly when 1/E is degree-<k on the
  overlap; the F_17^2 packet has four such four-point gates and no contained
  five-point support.
* a gated four-point core realizes 12 bad slopes, beating the free
  support-packing floor of 6 in this finite packet.
* the exact multi-support compatibility linear system is solvable on the
  constructed packets and rejects a blocked high-overlap pair.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations

Element = tuple[int, int]
Poly = list[Element]

P = 17
D = 3
ZERO = (0, 0)
ONE = (1, 0)
ALPHA = (0, 1)


def elt(a: int, b: int = 0) -> Element:
    return (a % P, b % P)


def add(x: Element, y: Element) -> Element:
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def neg(x: Element) -> Element:
    return ((-x[0]) % P, (-x[1]) % P)


def sub(x: Element, y: Element) -> Element:
    return add(x, neg(y))


def mul(x: Element, y: Element) -> Element:
    return (
        (x[0] * y[0] + D * x[1] * y[1]) % P,
        (x[0] * y[1] + x[1] * y[0]) % P,
    )


def inv(x: Element) -> Element:
    norm = (x[0] * x[0] - D * x[1] * x[1]) % P
    if norm == 0:
        raise ZeroDivisionError(x)
    norm_inv = pow(norm, -1, P)
    return ((x[0] * norm_inv) % P, (-x[1] * norm_inv) % P)


def div(x: Element, y: Element) -> Element:
    return mul(x, inv(y))


def trim(poly: Poly) -> Poly:
    out = poly[:]
    while len(out) > 1 and out[-1] == ZERO:
        out.pop()
    return out


def poly_add(left: Poly, right: Poly) -> Poly:
    out = []
    for idx in range(max(len(left), len(right))):
        x = left[idx] if idx < len(left) else ZERO
        y = right[idx] if idx < len(right) else ZERO
        out.append(add(x, y))
    return trim(out)


def poly_sub(left: Poly, right: Poly) -> Poly:
    return poly_add(left, [neg(coeff) for coeff in right])


def poly_scale(scalar: Element, poly: Poly) -> Poly:
    return trim([mul(scalar, coeff) for coeff in poly])


def poly_mul(left: Poly, right: Poly) -> Poly:
    out = [ZERO for _ in range(len(left) + len(right) - 1)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = add(out[i + j], mul(x, y))
    return trim(out)


def poly_eval(poly: Poly, x: Element) -> Element:
    value = ZERO
    for coeff in reversed(poly):
        value = add(mul(value, x), coeff)
    return value


def poly_degree(poly: Poly) -> int:
    return len(trim(poly)) - 1


def elt_pow(x: Element, exponent: int) -> Element:
    value = ONE
    for _ in range(exponent):
        value = mul(value, x)
    return value


def interpolate(points: tuple[int, ...], values: list[Element]) -> Poly:
    result: Poly = [ZERO]
    for i, xi_raw in enumerate(points):
        xi = elt(xi_raw)
        basis: Poly = [ONE]
        denominator = ONE
        for j, xj_raw in enumerate(points):
            if i == j:
                continue
            xj = elt(xj_raw)
            basis = poly_mul(basis, [neg(xj), ONE])
            denominator = mul(denominator, sub(xi, xj))
        result = poly_add(result, poly_scale(div(values[i], denominator), basis))
    return trim(result)


def locator(support: tuple[int, ...]) -> Poly:
    out: Poly = [ONE]
    for x in support:
        out = poly_mul(out, [neg(elt(x)), ONE])
    return out


def values(poly: Poly, support: tuple[int, ...]) -> dict[int, Element]:
    return {x: poly_eval(poly, elt(x)) for x in support}


def direction_not_low_degree(e_poly: Poly, support: tuple[int, ...], k: int) -> bool:
    direction_values = [neg(inv(poly_eval(e_poly, elt(x)))) for x in support[:k]]
    candidate = interpolate(support[:k], direction_values)
    if poly_degree(candidate) >= k:
        raise AssertionError("direction interpolant should have degree < k")
    return any(
        poly_eval(candidate, elt(x)) != neg(inv(poly_eval(e_poly, elt(x))))
        for x in support[k:]
    )


def residue_is_low_degree_on_subset(
    e_poly: Poly, subset: tuple[int, ...], k: int
) -> bool:
    """Return whether x -> 1/E(x) is degree < k on subset."""
    if len(subset) <= k:
        return True
    values_on_seed = [inv(poly_eval(e_poly, elt(x))) for x in subset[:k]]
    candidate = interpolate(subset[:k], values_on_seed)
    if poly_degree(candidate) >= k:
        raise AssertionError("seed interpolant should have degree < k")
    return all(
        poly_eval(candidate, elt(x)) == inv(poly_eval(e_poly, elt(x)))
        for x in subset[k:]
    )


def linear_rank_and_consistency(matrix: list[list[Element]]) -> tuple[bool, int]:
    """Return consistency and coefficient rank for an augmented F-matrix."""
    if not matrix:
        return True, 0
    rows = [row[:] for row in matrix]
    row_count = len(rows)
    col_count = len(rows[0]) - 1
    rank = 0
    for col in range(col_count):
        pivot = None
        for idx in range(rank, row_count):
            if rows[idx][col] != ZERO:
                pivot = idx
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv_pivot = inv(rows[rank][col])
        rows[rank] = [mul(value, inv_pivot) for value in rows[rank]]
        for idx in range(row_count):
            if idx == rank or rows[idx][col] == ZERO:
                continue
            factor = rows[idx][col]
            rows[idx] = [
                sub(rows[idx][j], mul(factor, rows[rank][j]))
                for j in range(col_count + 1)
            ]
        rank += 1

    for row in rows:
        if all(value == ZERO for value in row[:col_count]) and row[-1] != ZERO:
            return False, rank
    return True, rank


def compatibility_system_stats(
    e_poly: Poly,
    supports: tuple[tuple[int, ...], ...],
    slopes: tuple[Element, ...],
    k: int,
) -> dict[str, int | bool]:
    """Solve P_i-P_j=(z_j-z_i)/E on all support overlaps."""
    if len(supports) != len(slopes):
        raise AssertionError("support and slope counts differ")
    variable_count = len(supports) * k
    rows: list[list[Element]] = []
    equation_count = 0
    for i in range(len(supports)):
        for j in range(i + 1, len(supports)):
            overlap = sorted(set(supports[i]).intersection(supports[j]))
            for x_raw in overlap:
                x = elt(x_raw)
                row = [ZERO for _ in range(variable_count + 1)]
                for degree in range(k):
                    power = elt_pow(x, degree)
                    row[i * k + degree] = add(row[i * k + degree], power)
                    row[j * k + degree] = sub(row[j * k + degree], power)
                row[-1] = div(sub(slopes[j], slopes[i]), poly_eval(e_poly, x))
                rows.append(row)
                equation_count += 1
    consistent, rank = linear_rank_and_consistency(rows)
    return {
        "consistent": consistent,
        "rank": rank,
        "equations": equation_count,
        "variables": variable_count,
        "nullity": variable_count - rank if consistent else -1,
    }


def quotient_for_zero_core(
    e_poly: Poly, slope: Element, core: tuple[int, ...]
) -> Poly:
    core_values = [neg(div(slope, poly_eval(e_poly, elt(x)))) for x in core]
    r_poly = interpolate(core, core_values) if core else [ZERO]
    return poly_add([slope], poly_mul(e_poly, r_poly))


def quotient_for_anchor_constraints(
    e_poly: Poly,
    slope: Element,
    overlap: tuple[int, ...],
    anchor: dict[int, Element],
    k: int,
) -> Poly:
    """Return Q=slope+E*P matching an existing anchor on overlap."""
    p_values = [
        div(sub(anchor[x], slope), poly_eval(e_poly, elt(x)))
        for x in overlap
    ]
    seed_size = min(len(overlap), k)
    p_poly = interpolate(overlap[:seed_size], p_values[:seed_size]) if overlap else [ZERO]
    if poly_degree(p_poly) >= k:
        raise AssertionError("interpolant should have degree < k")
    for x, value in zip(overlap, p_values):
        if poly_eval(p_poly, elt(x)) != value:
            raise AssertionError("old anchor constraints fail the low-degree gate")
    return poly_add([slope], poly_mul(e_poly, p_poly))


def verify_core_optimization(n: int, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    floors = {c: (n - c) // (a - c) for c in range(k + 1)}
    optimized = (n - k) // sigma
    if max(floors.values()) != optimized:
        raise AssertionError((floors, optimized))

    real_values = [Fraction(n - c, a - c) for c in range(k + 1)]
    if real_values != sorted(real_values):
        raise AssertionError(real_values)

    return {"floors": floors, "optimized": optimized}


def verify_core_optimization_grid(max_n: int = 80) -> int:
    checked = 0
    for n in range(2, max_n + 1):
        for k in range(1, n):
            for sigma in range(1, n - k + 1):
                verify_core_optimization(n, k, sigma)
                checked += 1
    return checked


def verify_locator_split_packet(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    support_s = (1, 3, 4, 7, 9)
    support_t = (1, 2, 11, 12, 16)
    if len(support_s) != a or len(support_t) != a:
        raise AssertionError("wrong support sizes")
    if set(support_s).intersection(support_t) != {1}:
        raise AssertionError("expected one-point overlap")

    locator_s = locator(support_s)
    locator_t = locator(support_t)
    roots_hat_e = (ZERO, ALPHA, neg(ALPHA))
    readout_s = tuple(poly_eval(locator_s, root) for root in roots_hat_e)
    readout_t = tuple(poly_eval(locator_t, root) for root in roots_hat_e)
    if readout_s != readout_t:
        raise AssertionError("locator readouts should agree modulo hatE")
    if readout_s != (elt(9), elt(2, 5), elt(2, 12)):
        raise AssertionError(readout_s)

    q_s: Poly = [ZERO]
    q_t = poly_add([ONE], poly_mul(e_poly, [neg(inv(poly_eval(e_poly, elt(1))))]))
    if poly_degree(q_s) >= a or poly_degree(q_t) >= a:
        raise AssertionError("witness degree too large")
    if poly_eval(q_s, elt(1)) != ZERO or poly_eval(q_t, elt(1)) != ZERO:
        raise AssertionError("anchor values disagree on overlap")

    anchor: dict[int, Element] = {}
    anchor.update(values(q_s, support_s))
    for x, value in values(q_t, support_t).items():
        if x in anchor and anchor[x] != value:
            raise AssertionError("anchor conflict")
        anchor[x] = value

    if not all(poly_eval(q_s, elt(x)) == anchor[x] for x in support_s):
        raise AssertionError("slope 0 witness fails")
    if not all(poly_eval(q_t, elt(x)) == anchor[x] for x in support_t):
        raise AssertionError("slope 1 witness fails")

    if not direction_not_low_degree(e_poly, support_s, k):
        raise AssertionError("slope 0 should be noncontained")
    if not direction_not_low_degree(e_poly, support_t, k):
        raise AssertionError("slope 1 should be noncontained")

    return {
        "support_s": support_s,
        "support_t": support_t,
        "shared_hatE_readout": readout_s,
    }


def verify_sunflower_floor_packet(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    domain = tuple(range(1, 17))
    core = (1, 2, 3)
    petals = ((4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15))
    supports = tuple(tuple(core + petal) for petal in petals)
    slopes = tuple(elt(i) for i in range(len(supports)))
    expected_floor = (len(domain) - k) // sigma
    if len(supports) != expected_floor:
        raise AssertionError((len(supports), expected_floor))

    anchor = {x: ZERO for x in core}
    q_polys = []
    for support, slope, petal in zip(supports, slopes, petals):
        q_poly = quotient_for_zero_core(e_poly, slope, core)
        if poly_degree(q_poly) >= a:
            raise AssertionError("sunflower witness degree too large")
        q_polys.append(q_poly)
        for x in petal:
            if x in anchor:
                raise AssertionError("petals should be disjoint")
            anchor[x] = poly_eval(q_poly, elt(x))

    for support, slope, q_poly in zip(supports, slopes, q_polys):
        if not all(poly_eval(q_poly, elt(x)) == anchor[x] for x in support):
            raise AssertionError("sunflower witness does not match anchor")
        q_minus_slope = poly_sub(q_poly, [slope])
        if not all(poly_eval(q_minus_slope, root) == ZERO for root in (ZERO, ALPHA)):
            raise AssertionError("sunflower witness has wrong residue modulo E")
        if not direction_not_low_degree(e_poly, support, k):
            raise AssertionError("sunflower support should be noncontained")

    return {"core": core, "supports": supports, "slope_count": len(slopes)}


def verify_degenerate_support_packet(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    """Check a k-degenerate extremal packet that has no common sunflower core."""
    a = k + sigma
    domain = tuple(range(1, 17))
    supports = (
        (1, 2, 3, 4, 5),
        (1, 2, 3, 6, 7),
        (1, 4, 6, 8, 9),
        (2, 5, 8, 10, 11),
        (3, 7, 10, 12, 13),
        (4, 9, 12, 14, 15),
    )
    slopes = tuple(elt(i) for i in range(len(supports)))
    expected_floor = (len(domain) - k) // sigma
    if len(supports) != expected_floor:
        raise AssertionError((len(supports), expected_floor))
    if set(supports[0]).intersection(*map(set, supports[1:])):
        raise AssertionError("packet should not be a common-core sunflower")

    anchor: dict[int, Element] = {}
    q_polys = []
    seen: set[int] = set()
    union_sizes = []
    overlap_sizes = []
    for support, slope in zip(supports, slopes):
        if len(support) != a:
            raise AssertionError("wrong support size")
        overlap = tuple(x for x in support if x in seen)
        if len(overlap) > k:
            raise AssertionError("support family is not k-degenerate")
        q_poly = quotient_for_anchor_constraints(e_poly, slope, overlap, anchor, k)
        if poly_degree(q_poly) >= a:
            raise AssertionError("degenerate witness degree too large")
        q_polys.append(q_poly)

        for x in overlap:
            if poly_eval(q_poly, elt(x)) != anchor[x]:
                raise AssertionError("new witness failed old anchor constraint")
        for x in support:
            value = poly_eval(q_poly, elt(x))
            if x in anchor and anchor[x] != value:
                raise AssertionError("anchor conflict in degenerate packet")
            anchor[x] = value
        seen.update(support)
        union_sizes.append(len(seen))
        overlap_sizes.append(len(overlap))

    if len(seen) != k + len(supports) * sigma:
        raise AssertionError("extremal degenerate packet should add exactly sigma each step")

    for support, slope, q_poly in zip(supports, slopes, q_polys):
        if not all(poly_eval(q_poly, elt(x)) == anchor[x] for x in support):
            raise AssertionError("degenerate witness does not match anchor")
        q_minus_slope = poly_sub(q_poly, [slope])
        if not all(poly_eval(q_minus_slope, root) == ZERO for root in (ZERO, ALPHA)):
            raise AssertionError("degenerate witness has wrong residue modulo E")
        if not direction_not_low_degree(e_poly, support, k):
            raise AssertionError("degenerate support should be noncontained")

    return {
        "supports": supports,
        "slope_count": len(slopes),
        "union_size": len(seen),
        "union_sizes": tuple(union_sizes),
        "overlap_sizes": tuple(overlap_sizes),
    }


def verify_high_overlap_pair_gate(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    domain = tuple(range(1, 17))

    gated_overlaps = tuple(
        subset
        for subset in combinations(domain, k + 1)
        if residue_is_low_degree_on_subset(e_poly, subset, k)
    )
    expected_overlaps = (
        (1, 6, 11, 16),
        (2, 4, 13, 15),
        (4, 6, 8, 12),
        (5, 9, 11, 13),
    )
    if gated_overlaps != expected_overlaps:
        raise AssertionError(gated_overlaps)

    contained_supports = tuple(
        support
        for support in combinations(domain, a)
        if residue_is_low_degree_on_subset(e_poly, support, k)
    )
    if contained_supports:
        raise AssertionError("full active supports should stay noncontained")

    pairs_per_gate = (len(domain) - (k + 1)) * (len(domain) - (k + 1) - 1) // 2
    high_overlap_pair_count = len(gated_overlaps) * pairs_per_gate
    counted_pair_count = sum(
        len(tuple(combinations(tuple(x for x in domain if x not in overlap), 2)))
        for overlap in gated_overlaps
    )
    expected_pair_count = 264
    if counted_pair_count != high_overlap_pair_count:
        raise AssertionError((counted_pair_count, high_overlap_pair_count))
    if high_overlap_pair_count != expected_pair_count:
        raise AssertionError((high_overlap_pair_count, expected_pair_count))

    overlap = gated_overlaps[0]
    support_s = tuple(sorted(overlap + (2,)))
    support_t = tuple(sorted(overlap + (3,)))
    if len(set(support_s).intersection(support_t)) != k + 1:
        raise AssertionError("expected a high-overlap pair")

    q_s: Poly = [ZERO]
    anchor = {x: ZERO for x in support_s}
    q_t = quotient_for_anchor_constraints(e_poly, ONE, overlap, anchor, k)
    for x in overlap:
        if poly_eval(q_t, elt(x)) != ZERO:
            raise AssertionError("high-overlap witness failed the gate")
    for x in support_t:
        value = poly_eval(q_t, elt(x))
        if x in anchor and anchor[x] != value:
            raise AssertionError("high-overlap anchor conflict")
        anchor[x] = value

    if not all(poly_eval(q_s, elt(x)) == anchor[x] for x in support_s):
        raise AssertionError("slope 0 high-overlap witness fails")
    if not all(poly_eval(q_t, elt(x)) == anchor[x] for x in support_t):
        raise AssertionError("slope 1 high-overlap witness fails")
    if not direction_not_low_degree(e_poly, support_s, k):
        raise AssertionError("support_s should be noncontained")
    if not direction_not_low_degree(e_poly, support_t, k):
        raise AssertionError("support_t should be noncontained")

    blocked_overlap = (1, 2, 3, 4)
    if residue_is_low_degree_on_subset(e_poly, blocked_overlap, k):
        raise AssertionError("blocked overlap unexpectedly passed the gate")

    return {
        "gated_overlaps": gated_overlaps,
        "contained_supports": len(contained_supports),
        "high_overlap_pair_count": high_overlap_pair_count,
        "example_supports": (support_s, support_t),
    }


def verify_gated_core_floor_packet(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    domain = tuple(range(1, 17))
    gated_core = (1, 6, 11, 16)
    c = len(gated_core)
    if c <= k or c >= a:
        raise AssertionError("expected a genuinely dense proper core")
    if not residue_is_low_degree_on_subset(e_poly, gated_core, k):
        raise AssertionError("core should pass the residue low-degree gate")

    support_floor = (len(domain) - k) // sigma
    gated_floor = (len(domain) - c) // (a - c)
    if support_floor != 6 or gated_floor != 12 or gated_floor <= support_floor:
        raise AssertionError((support_floor, gated_floor))

    petals = tuple(x for x in domain if x not in gated_core)
    supports = tuple(tuple(sorted(gated_core + (petal,))) for petal in petals)
    slopes = tuple(elt(i) for i in range(gated_floor))
    if len(supports) != gated_floor:
        raise AssertionError("wrong gated-core support count")

    anchor = {x: ZERO for x in gated_core}
    q_polys = []
    for support, slope, petal in zip(supports, slopes, petals):
        q_poly = quotient_for_anchor_constraints(e_poly, slope, gated_core, anchor, k)
        if poly_degree(q_poly) >= a:
            raise AssertionError("gated-core witness degree too large")
        if not all(poly_eval(q_poly, elt(x)) == ZERO for x in gated_core):
            raise AssertionError("gated-core witness failed core anchor")
        anchor[petal] = poly_eval(q_poly, elt(petal))
        q_polys.append(q_poly)

    for support, slope, q_poly in zip(supports, slopes, q_polys):
        if not all(poly_eval(q_poly, elt(x)) == anchor[x] for x in support):
            raise AssertionError("gated-core witness does not match anchor")
        q_minus_slope = poly_sub(q_poly, [slope])
        if not all(poly_eval(q_minus_slope, root) == ZERO for root in (ZERO, ALPHA)):
            raise AssertionError("gated-core witness has wrong residue modulo E")
        if not direction_not_low_degree(e_poly, support, k):
            raise AssertionError("gated-core support should be noncontained")

    return {
        "core": gated_core,
        "slope_count": len(slopes),
        "free_packing_floor": support_floor,
        "gated_floor": gated_floor,
        "supports": supports,
        "slopes": slopes,
    }


def verify_compatibility_system(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    core = (1, 6, 11, 16)
    domain = tuple(range(1, 17))
    gated_supports = tuple(tuple(sorted(core + (x,))) for x in domain if x not in core)
    gated_slopes = tuple(elt(i) for i in range(len(gated_supports)))
    gated_stats = compatibility_system_stats(e_poly, gated_supports, gated_slopes, k)
    if not gated_stats["consistent"]:
        raise AssertionError("gated-core compatibility system should be solvable")

    degenerate_supports = (
        (1, 2, 3, 4, 5),
        (1, 2, 3, 6, 7),
        (1, 4, 6, 8, 9),
        (2, 5, 8, 10, 11),
        (3, 7, 10, 12, 13),
        (4, 9, 12, 14, 15),
    )
    degenerate_slopes = tuple(elt(i) for i in range(len(degenerate_supports)))
    degenerate_stats = compatibility_system_stats(
        e_poly, degenerate_supports, degenerate_slopes, k
    )
    if not degenerate_stats["consistent"]:
        raise AssertionError("k-degenerate compatibility system should be solvable")

    blocked_supports = (
        (1, 2, 3, 4, 5),
        (1, 2, 3, 4, 6),
    )
    blocked_slopes = (ZERO, ONE)
    if len(set(blocked_supports[0]).intersection(blocked_supports[1])) != k + 1:
        raise AssertionError("blocked pair should share k+1 points")
    blocked_stats = compatibility_system_stats(e_poly, blocked_supports, blocked_slopes, k)
    if blocked_stats["consistent"]:
        raise AssertionError("blocked high-overlap pair should be inconsistent")

    if a != len(blocked_supports[0]):
        raise AssertionError("blocked support size mismatch")

    return {
        "gated": gated_stats,
        "degenerate": degenerate_stats,
        "blocked": blocked_stats,
    }


@dataclass(frozen=True)
class Verification:
    core_optimization: dict[str, object]
    core_grid_checks: int
    locator_split: dict[str, object]
    sunflower: dict[str, object]
    degenerate_support: dict[str, object]
    high_overlap_gate: dict[str, object]
    gated_core: dict[str, object]
    compatibility: dict[str, object]


def verify() -> Verification:
    k = 3
    sigma = 2
    n = 16
    e_poly = [ZERO, neg(ALPHA), ONE]  # E=X(X-alpha)
    if not all(poly_eval(e_poly, elt(x)) != ZERO for x in range(1, 17)):
        raise AssertionError("E should be nonzero on D=F_17^*")
    return Verification(
        core_optimization=verify_core_optimization(n, k, sigma),
        core_grid_checks=verify_core_optimization_grid(),
        locator_split=verify_locator_split_packet(e_poly, k, sigma),
        sunflower=verify_sunflower_floor_packet(e_poly, k, sigma),
        degenerate_support=verify_degenerate_support_packet(e_poly, k, sigma),
        high_overlap_gate=verify_high_overlap_pair_gate(e_poly, k, sigma),
        gated_core=verify_gated_core_floor_packet(e_poly, k, sigma),
        compatibility=verify_compatibility_system(e_poly, k, sigma),
    )


def main() -> None:
    result = verify()
    print("f1_arbitrary_anchor_split: PASS")
    print(
        "core floor optimization: "
        f"max={result.core_optimization['optimized']} "
        f"floors={result.core_optimization['floors']}"
    )
    print(f"core optimization grid checks: {result.core_grid_checks}")
    print(
        "locator split: supports="
        f"{result.locator_split['support_s']} and {result.locator_split['support_t']}"
    )
    print(
        "sunflower floor: "
        f"{result.sunflower['slope_count']} slopes on core {result.sunflower['core']}"
    )
    print(
        "degenerate support floor: "
        f"{result.degenerate_support['slope_count']} slopes, "
        f"union size {result.degenerate_support['union_size']}, "
        f"overlaps={result.degenerate_support['overlap_sizes']}"
    )
    print(
        "high-overlap gate: "
        f"{len(result.high_overlap_gate['gated_overlaps'])} four-point gates, "
        f"{result.high_overlap_gate['high_overlap_pair_count']} support pairs, "
        f"contained supports={result.high_overlap_gate['contained_supports']}"
    )
    print(
        "gated core floor: "
        f"{result.gated_core['slope_count']} slopes on core {result.gated_core['core']} "
        f"(free floor {result.gated_core['free_packing_floor']})"
    )
    print(
        "compatibility system: "
        f"gated rank={result.compatibility['gated']['rank']} "
        f"degenerate rank={result.compatibility['degenerate']['rank']} "
        f"blocked consistent={result.compatibility['blocked']['consistent']}"
    )


if __name__ == "__main__":
    main()
