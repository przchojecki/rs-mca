#!/usr/bin/env python3
"""Verify the one-remainder-fiber M1 quotient exchange profile.

This checks the closed fixed-support enumerator in
experimental/m1_quotient_periodic_overlap_profile.md against brute-force
enumeration for small quotient partitions.
"""

from collections import Counter
from itertools import combinations
from math import comb


def choose(n, k):
    if k < 0 or k > n:
        return 0
    return comb(n, k)


def add_term(poly, coeff, exponent):
    if coeff:
        poly[exponent] += coeff


def formula_enumerator(N, m, L, r):
    poly = Counter()

    for h in range(0, L + 1):
        for ell in range(0, r + 1):
            coeff = choose(L, h) * choose(N - L - 1, h)
            coeff *= choose(r, ell) * choose(m - r, ell)
            add_term(poly, coeff, h * m + ell)

    for h in range(0, L):
        coeff = L * choose(m, r) * choose(L - 1, h) * choose(N - L - 1, h)
        add_term(poly, coeff, h * m + m - r)

    for h in range(0, L):
        coeff = L * choose(m, r) * choose(L - 1, h)
        coeff *= choose(N - L - 1, h + 1)
        add_term(poly, coeff, (h + 1) * m)

    for h in range(1, L + 1):
        coeff = (N - L - 1) * choose(m, r) * choose(L, h)
        coeff *= choose(N - L - 2, h - 1)
        add_term(poly, coeff, h * m)

    for h in range(0, L + 1):
        coeff = (N - L - 1) * choose(m, r) * choose(L, h)
        coeff *= choose(N - L - 2, h)
        add_term(poly, coeff, h * m + r)

    return +poly


def large_fiber_strict_enumerator(N, m, L, b, t):
    assert t <= m
    poly = Counter()

    for ell in range(1, min(b, m - b, t - 1) + 1):
        coeff = choose(b, ell) * choose(m - b, ell)
        add_term(poly, coeff, ell)

    if b < t:
        add_term(poly, (N - L - 1) * choose(m, b), b)

    if m - b < t:
        add_term(poly, L * choose(m, b), m - b)

    return +poly


def support(fibers, whole_indices, partial_index, partial_points):
    out = set()
    for index in whole_indices:
        out.update(fibers[index])
    out.update(partial_points)
    return frozenset(out)


def remainder_family(N, m, L, r):
    fibers = [
        tuple((fiber_index, point_index) for point_index in range(m))
        for fiber_index in range(N)
    ]
    family = []
    for whole_indices in combinations(range(N), L):
        whole_set = set(whole_indices)
        for partial_index in range(N):
            if partial_index in whole_set:
                continue
            for partial_points in combinations(fibers[partial_index], r):
                family.append(
                    support(fibers, whole_indices, partial_index, partial_points)
                )
    return family


def brute_enumerator(N, m, L, r):
    family = remainder_family(N, m, L, r)
    fixed = family[0]
    return Counter(len(fixed - other) for other in family)


def verify_case(N, m, L, r):
    brute = brute_enumerator(N, m, L, r)
    formula = formula_enumerator(N, m, L, r)
    assert brute == formula, (N, m, L, r, brute, formula)
    family_size = choose(N, L) * (N - L) * choose(m, r)
    assert sum(formula.values()) == family_size
    return family_size, formula


def verify_large_fiber_case(N, m, L, b, t):
    full = formula_enumerator(N, m, L, b)
    strict = Counter(
        {exponent: coeff for exponent, coeff in full.items() if 0 < exponent < t}
    )
    truncation = large_fiber_strict_enumerator(N, m, L, b, t)
    assert strict == truncation, (N, m, L, b, t, strict, truncation)
    return truncation


def stable_large_scale_enumerator(N, m, L, d, t):
    assert 1 <= d < t
    assert m >= t + d
    poly = Counter()

    for ell in range(1, d + 1):
        coeff = choose(d, ell) * choose(m - d, ell)
        add_term(poly, coeff, ell)

    add_term(poly, (N - L - 1) * choose(m, d), d)
    return +poly


def verify_stable_large_scale_case(N, m, L, d, t):
    full = formula_enumerator(N, m, L, d)
    strict = Counter(
        {exponent: coeff for exponent, coeff in full.items() if 0 < exponent < t}
    )
    stable = stable_large_scale_enumerator(N, m, L, d, t)
    assert strict == stable, (N, m, L, d, t, strict, stable)
    assert sum(stable.values()) == (N - L) * choose(m, d) - 1
    return stable


def stable_co_remainder_enumerator(N, m, L, d, t):
    assert 1 <= d < t
    assert m >= t + d
    return stable_large_scale_enumerator(N, m, N - L - 1, d, t)


def verify_complement_duality_case(N, m, L, b):
    left = formula_enumerator(N, m, L, b)
    right = formula_enumerator(N, m, N - L - 1, m - b)
    assert left == right, (N, m, L, b, left, right)
    return left


def verify_stable_co_remainder_case(N, m, L, d, t):
    full = formula_enumerator(N, m, L, m - d)
    strict = Counter(
        {exponent: coeff for exponent, coeff in full.items() if 0 < exponent < t}
    )
    stable = stable_co_remainder_enumerator(N, m, L, d, t)
    assert strict == stable, (N, m, L, d, t, strict, stable)
    assert sum(stable.values()) == (L + 1) * choose(m, d) - 1
    return stable


def verify_two_sided_fixed_dither_stable_tail(n, k0, r0, t, m):
    d = t - r0
    e = abs(d)
    assert 1 <= e < t
    assert m >= t + e
    assert k0 % m == 0
    assert m <= k0
    N = n // m

    if d > 0:
        L = k0 // m
        full = formula_enumerator(N, m, L, d)
        expected = ((n - k0) // m) * choose(m, d) - 1
    else:
        L = k0 // m - 1
        full = formula_enumerator(N, m, L, m - e)
        expected = (k0 // m) * choose(m, e) - 1

    strict = Counter(
        {exponent: coeff for exponent, coeff in full.items() if 0 < exponent < t}
    )
    assert sum(strict.values()) == expected, (n, k0, r0, t, m, strict, expected)
    return strict


def two_sided_weighted_formula(n, k0, r0, t, m, q):
    d = t - r0
    e = abs(d)
    assert 1 <= e < t
    assert m >= t + e
    assert k0 % m == 0

    if d > 0:
        side_coeff = (n - k0) // m - 1
    else:
        side_coeff = k0 // m - 1

    correction = sum(
        choose(e, ell) * choose(m - e, ell) * q ** (t - ell)
        for ell in range(1, e + 1)
    )
    correction += side_coeff * choose(m, e) * q ** (t - e)
    return correction


def verify_two_sided_fixed_dither_weighted_tail(n, k0, r0, t, m, q):
    strict = verify_two_sided_fixed_dither_stable_tail(n, k0, r0, t, m)
    correction = weighted_strict_correction(strict, t, q)
    expected = two_sided_weighted_formula(n, k0, r0, t, m, q)
    assert correction == expected, (n, k0, r0, t, m, q, correction, expected)
    return correction


def fixed_window_radius(t_start, t_end, r):
    return max(abs(t_start - r), abs(t_end - r))


def ceil_div(numerator, denominator):
    return (numerator + denominator - 1) // denominator


def safe_gap_for_menu(t, menu):
    gaps = [abs(t - r) for r in menu if r != t]
    if not gaps:
        return None
    return min(gaps)


def menu_covers_window(t_start, t_end, menu, max_gap):
    for t in range(t_start, t_end + 1):
        gap = safe_gap_for_menu(t, menu)
        if gap is None or gap > max_gap:
            return False
    return True


def dither_menu_block_construction(t_start, t_end, max_gap):
    return tuple(range(t_start - 1, t_end, max_gap))


def verify_dither_menu_covering_bound(t_start, t_end, max_gap):
    assert 1 <= t_start <= t_end
    assert max_gap >= 1
    window_length = t_end - t_start + 1
    lower_bound = ceil_div(window_length, 2 * max_gap)
    upper_bound = ceil_div(window_length, max_gap)

    construction = dither_menu_block_construction(t_start, t_end, max_gap)
    assert len(construction) == upper_bound
    assert menu_covers_window(t_start, t_end, construction, max_gap)

    candidates = range(t_start - max_gap, t_end + max_gap + 1)
    for size in range(lower_bound):
        for menu in combinations(candidates, size):
            assert not menu_covers_window(t_start, t_end, menu, max_gap), (
                t_start,
                t_end,
                max_gap,
                menu,
            )

    for r in candidates:
        covered = [
            t
            for t in range(t_start, t_end + 1)
            if t != r and abs(t - r) <= max_gap
        ]
        assert len(covered) <= 2 * max_gap

    return lower_bound, upper_bound, construction


def verify_dither_menu_stable_tail_lower_bound(
    n,
    k0,
    t_start,
    t_end,
    max_gap,
    menu_size,
    q,
):
    assert max_gap < t_start
    assert q > 1
    window_length = t_end - t_start + 1
    minimum_menu_size = ceil_div(window_length, 2 * max_gap)
    assert menu_size >= minimum_menu_size
    forced_gap = ceil_div(window_length, 2 * menu_size)
    assert 1 <= forced_gap <= max_gap

    candidates = range(t_start - max_gap, t_end + max_gap + 1)
    valid_menus = [
        menu
        for menu in combinations(candidates, menu_size)
        if menu_covers_window(t_start, t_end, menu, max_gap)
    ]
    assert valid_menus

    scale_thresholds = []
    for m in dyadic_divisors(k0):
        if m < t_end + max_gap:
            continue
        side_floor = min(k0 // m, (n - k0) // m)
        mass_threshold = side_floor * choose(m, forced_gap) - 1
        assert mass_threshold > 0
        weighted_threshold = mass_threshold * q ** (t_start - max_gap)
        scale_thresholds.append((m, mass_threshold, weighted_threshold))
    assert scale_thresholds

    for menu in valid_menus:
        witness = None
        for t in range(t_start, t_end + 1):
            safe_choices = [
                (abs(t - r), r)
                for r in menu
                if r != t and abs(t - r) <= max_gap
            ]
            assert safe_choices
            gap, r = min(safe_choices)
            if gap >= forced_gap:
                witness = (t, r, gap)
                break
        assert witness is not None, (t_start, t_end, max_gap, menu_size, menu)

        t, r, gap = witness
        for m, mass_threshold, weighted_threshold in scale_thresholds:
            strict = verify_two_sided_fixed_dither_stable_tail(n, k0, r, t, m)
            correction = weighted_strict_correction(strict, t, q)
            assert sum(strict.values()) >= mass_threshold, (
                n,
                k0,
                t_start,
                t_end,
                max_gap,
                menu_size,
                menu,
                witness,
                m,
                strict,
                mass_threshold,
            )
            assert correction >= weighted_threshold, (
                n,
                k0,
                t_start,
                t_end,
                max_gap,
                menu_size,
                q,
                menu,
                witness,
                m,
                correction,
                weighted_threshold,
            )

    return forced_gap, tuple(scale_thresholds), len(valid_menus)


def verify_fixed_window_stable_tail_minimax(n, k0, t_start, t_end):
    assert 1 <= t_start <= t_end
    window_length = t_end - t_start + 1
    search_start = t_start - window_length - 3
    search_end = t_end + window_length + 3
    candidates = range(search_start, search_end + 1)

    radii = {
        r: fixed_window_radius(t_start, t_end, r)
        for r in candidates
    }
    center_radius = min(radii.values())
    assert center_radius == window_length // 2

    center_dithers = tuple(r for r, radius in radii.items() if radius == center_radius)
    assert all(t_start <= r <= t_end for r in center_dithers)

    zero_gap_free_radii = {
        r: radius
        for r, radius in radii.items()
        if not (t_start <= r <= t_end)
    }
    zero_gap_radius = min(zero_gap_free_radii.values())
    assert zero_gap_radius == window_length
    assert t_start - 1 in zero_gap_free_radii
    assert t_end + 1 in zero_gap_free_radii

    witnesses = []
    endpoint_cases = (
        (t_start - 1, t_end, "upper"),
        (t_end + 1, t_start, "lower"),
    )
    for r0, endpoint, side in endpoint_cases:
        gap = abs(endpoint - r0)
        assert gap == window_length
        if gap >= endpoint:
            continue
        for m in dyadic_divisors(k0):
            if m < endpoint + gap:
                continue
            strict = verify_two_sided_fixed_dither_stable_tail(
                n,
                k0,
                r0,
                endpoint,
                m,
            )
            if side == "upper":
                expected = ((n - k0) // m) * choose(m, gap) - 1
            else:
                expected = (k0 // m) * choose(m, gap) - 1
            assert sum(strict.values()) == expected
            assert max(strict) == gap
            witnesses.append((r0, endpoint, m, gap, sum(strict.values())))

    assert witnesses
    return center_radius, zero_gap_radius, tuple(witnesses)


def verify_adjacent_slack_remainder_obstruction(n, k0, t0, m):
    assert m >= t0 + 3
    assert k0 % m == 0
    N = n // m
    L = k0 // m
    t = t0 + 1

    full = formula_enumerator(N, m, L, 2)
    strict = Counter(
        {exponent: coeff for exponent, coeff in full.items() if 0 < exponent < t}
    )
    expected_mass = (n - k0) * (m - 1) // 2 - 1
    assert sum(strict.values()) == expected_mass, (n, k0, t0, m, strict)

    stable = stable_large_scale_enumerator(N, m, L, 2, t)
    assert strict == stable, (n, k0, t0, m, strict, stable)
    return strict


def maximal_dither_all_scale_enumerator(N, m, L, t):
    assert m >= 2
    A = N - L - 1
    poly = Counter()

    for h in range(0, L + 1):
        if h * m + 1 < t:
            coeff = choose(L, h) * choose(A, h) * (m * (A - h + 1) - 1)
            add_term(poly, coeff, h * m + 1)

    for h in range(1, L + 1):
        if h * m < t:
            coeff = choose(L, h) * choose(A, h) * (1 + 2 * m * h)
            add_term(poly, coeff, h * m)

        if h * m - 1 < t:
            coeff = m * h * choose(L, h) * choose(A, h - 1)
            add_term(poly, coeff, h * m - 1)

    return +poly


def verify_maximal_dither_all_scale_case(N, m, L, t):
    full = formula_enumerator(N, m, L, 1)
    strict = Counter(
        {exponent: coeff for exponent, coeff in full.items() if 0 < exponent < t}
    )
    all_scale = maximal_dither_all_scale_enumerator(N, m, L, t)
    assert strict == all_scale, (N, m, L, t, strict, all_scale)
    return all_scale


def dyadic_divisors(value):
    out = []
    scale = 2
    while scale <= value:
        if value % scale == 0:
            out.append(scale)
        scale *= 2
    return out


def dyadic_scale_first_codegree(n, k0, r, t, m):
    assert n % m == 0
    assert k0 % m == 0
    support_size = k0 + t - r
    if t <= m or support_size % m:
        return 0
    if support_size < m or support_size > n - m:
        return 0

    quotient_order = n // m
    quotient_support = support_size // m
    return quotient_support * (quotient_order - quotient_support)


def scale_two_codegree(n, k0, r, t):
    assert n % 2 == 0
    assert k0 % 2 == 0
    return dyadic_scale_first_codegree(n, k0, r, t, 2)


def count_residue_interval(start, end, residue, modulus):
    if start > end:
        return 0
    first = start + ((residue - start) % modulus)
    if first > end:
        return 0
    return 1 + (end - first) // modulus


def verify_adjacent_slack_dither_obstruction(n, k0, t_start, t_end, r_start, r_end):
    assert 3 <= t_start <= t_end
    assert n % 2 == 0
    assert k0 % 2 == 0

    rows = []
    for r in range(r_start, r_end + 1):
        active_slacks = []
        for t in range(t_start, t_end + 1):
            support_size = k0 + t - r
            assert 2 <= support_size <= n - 2

            codegree = scale_two_codegree(n, k0, r, t)
            should_survive = (t - r) % 2 == 0
            assert bool(codegree) == should_survive, (n, k0, t, r, codegree)
            if should_survive:
                expected = support_size * (n - support_size) // 4
                assert codegree == expected, (n, k0, t, r, codegree, expected)
                active_slacks.append(t)

        window_size = t_end - t_start + 1
        assert len(active_slacks) in {window_size // 2, (window_size + 1) // 2}

        for t in range(t_start, t_end):
            left = bool(scale_two_codegree(n, k0, r, t))
            right = bool(scale_two_codegree(n, k0, r, t + 1))
            assert left != right, (n, k0, r, t, left, right)

        rows.append((r, tuple(active_slacks)))
    return rows


def verify_fixed_dither_slack_window_ledger(n, k0, t_start, t_end, r_values, scales):
    rows = []
    for r in r_values:
        for m in scales:
            assert m in dyadic_divisors(k0)
            eligible_start = max(t_start, m + 1)
            active_slacks = []

            for t in range(eligible_start, t_end + 1):
                support_size = k0 + t - r
                assert m <= support_size <= n - m

                codegree = dyadic_scale_first_codegree(n, k0, r, t, m)
                should_survive = (t - r) % m == 0
                assert bool(codegree) == should_survive, (n, k0, t, r, m, codegree)

                if should_survive:
                    quotient_support = support_size // m
                    quotient_order = n // m
                    expected = quotient_support * (quotient_order - quotient_support)
                    assert codegree == expected, (n, k0, t, r, m, codegree, expected)
                    active_slacks.append(t)

            expected_count = count_residue_interval(eligible_start, t_end, r, m)
            assert len(active_slacks) == expected_count, (n, k0, r, m, active_slacks)

            eligible_length = max(0, t_end - eligible_start + 1)
            if eligible_length:
                lower = eligible_length // m
                upper = (eligible_length + m - 1) // m
                assert lower <= len(active_slacks) <= upper

            for block_start in range(eligible_start, t_end - m + 2):
                block_end = block_start + m - 1
                block_count = count_residue_interval(block_start, block_end, r, m)
                assert block_count == 1, (n, k0, r, m, block_start, block_count)

            rows.append((r, m, tuple(active_slacks)))
    return rows


def expected_maximal_dither_profile(n, k0, m, t):
    expected = Counter({1: n - k0 - 1})
    if m == t:
        expected[t - 1] += k0
    return +expected


def verify_maximal_dither_scale_confinement(n, k0, t):
    small_scales = [m for m in dyadic_divisors(k0) if m < t]
    expected_small_count = 0 if t <= 2 else (t - 1).bit_length() - 1
    expected_small_count = min(expected_small_count, len(dyadic_divisors(k0)))
    assert len(small_scales) == expected_small_count

    nonlinear_scales = []
    for m in dyadic_divisors(k0):
        N = n // m
        L = k0 // m
        profile = maximal_dither_all_scale_enumerator(N, m, L, t)
        if m >= t:
            expected = expected_maximal_dither_profile(n, k0, m, t)
            assert profile == expected, (n, k0, m, t, profile, expected)
        else:
            nonlinear_scales.append(m)

    assert nonlinear_scales == small_scales
    return small_scales


def weighted_strict_correction(poly, t, q):
    return sum(coeff * q ** (t - exponent) for exponent, coeff in poly.items())


def verify_maximal_dither_random_line_ledger(n, k0, t, q):
    rows = []
    for m in dyadic_divisors(k0):
        N = n // m
        L = k0 // m
        profile = maximal_dither_all_scale_enumerator(N, m, L, t)
        correction = weighted_strict_correction(profile, t, q)
        if m > t:
            expected = (n - k0 - 1) * q ** (t - 1)
            assert correction == expected, (n, k0, t, q, m, correction, expected)
        elif m == t:
            expected = (n - k0 - 1) * q ** (t - 1) + k0 * q
            assert correction == expected, (n, k0, t, q, m, correction, expected)
        rows.append((m, correction))
    return rows


def main():
    cases = [
        (5, 4, 1, 1),
        (5, 4, 2, 1),
        (6, 3, 2, 1),
        (6, 5, 2, 2),
        (7, 4, 3, 2),
    ]
    for case in cases:
        family_size, enumerator = verify_case(*case)
        print(
            f"N,m,L,r={case}: |A_REM|={family_size}, "
            f"H={dict(sorted(enumerator.items()))}"
        )
    large_fiber_cases = [
        (7, 5, 2, 1, 3),
        (8, 6, 3, 2, 4),
        (9, 7, 2, 3, 5),
        (8, 4, 3, 1, 4),
    ]
    for case in large_fiber_cases:
        strict = verify_large_fiber_case(*case)
        print(f"N,m,L,b,t={case}: H_<t={dict(sorted(strict.items()))}")
    stable_cases = [
        (8, 8, 4, 1, 5),
        (4, 16, 2, 1, 5),
        (2, 32, 1, 1, 5),
        (8, 8, 4, 2, 5),
        (4, 16, 2, 2, 5),
        (2, 32, 1, 2, 5),
        (10, 10, 4, 3, 6),
    ]
    for case in stable_cases:
        stable = verify_stable_large_scale_case(*case)
        print(
            f"N,m,L,d,t={case}: H_stable={dict(sorted(stable.items()))}, "
            f"mass={sum(stable.values())}"
        )
    duality_cases = [
        (6, 5, 2, 1),
        (7, 4, 3, 2),
        (8, 6, 2, 5),
        (9, 7, 4, 3),
    ]
    for case in duality_cases:
        dual = verify_complement_duality_case(*case)
        print(
            f"N,m,L,b={case}: H_dual={dict(sorted(dual.items()))}, "
            f"mass={sum(dual.values())}"
        )
    co_remainder_cases = [
        (8, 8, 3, 1, 5),
        (4, 16, 1, 1, 5),
        (8, 8, 3, 2, 5),
        (4, 16, 1, 2, 5),
        (10, 10, 4, 3, 6),
    ]
    for case in co_remainder_cases:
        stable = verify_stable_co_remainder_case(*case)
        print(
            f"N,m,L,d,t={case}: H_costable={dict(sorted(stable.items()))}, "
            f"mass={sum(stable.values())}"
        )
    two_sided_tail_cases = [
        (256, 128, 5, 8, 16),
        (256, 128, 8, 5, 16),
        (1024, 256, 8, 12, 32),
        (1024, 256, 12, 8, 32),
        (1024, 512, 9, 14, 32),
        (1024, 512, 14, 9, 32),
    ]
    for case in two_sided_tail_cases:
        stable = verify_two_sided_fixed_dither_stable_tail(*case)
        print(
            f"n,k0,r0,t,m={case}: H_twosided={dict(sorted(stable.items()))}, "
            f"mass={sum(stable.values())}"
        )
    two_sided_weighted_cases = [
        (256, 128, 5, 8, 16, 17),
        (256, 128, 8, 5, 16, 17),
        (1024, 256, 8, 12, 32, 17),
        (1024, 256, 12, 8, 32, 17),
        (1024, 512, 9, 14, 32, 257),
        (1024, 512, 14, 9, 32, 257),
    ]
    for case in two_sided_weighted_cases:
        correction = verify_two_sided_fixed_dither_weighted_tail(*case)
        print(f"n,k0,r0,t,m,q={case}: R_twosided={correction}")
    minimax_cases = [
        (256, 128, 5, 8),
        (256, 64, 8, 13),
        (1024, 256, 9, 15),
    ]
    for case in minimax_cases:
        center_radius, zero_gap_radius, witnesses = (
            verify_fixed_window_stable_tail_minimax(*case)
        )
        print(
            f"n,k0,t0,t1={case}: center_radius={center_radius}, "
            f"zero_gap_radius={zero_gap_radius}, witnesses={witnesses}"
        )
    menu_covering_cases = [
        (5, 9, 1),
        (5, 12, 2),
        (8, 16, 2),
        (10, 19, 3),
    ]
    for case in menu_covering_cases:
        lower_bound, upper_bound, construction = (
            verify_dither_menu_covering_bound(*case)
        )
        print(
            f"t0,t1,D={case}: menu_lower={lower_bound}, "
            f"block_upper={upper_bound}, construction={construction}"
        )
    menu_tail_cases = [
        (256, 128, 5, 8, 2, 2, 17),
        (256, 64, 8, 13, 2, 2, 17),
        (1024, 256, 9, 15, 3, 2, 257),
    ]
    for case in menu_tail_cases:
        forced_gap, thresholds, valid_menu_count = (
            verify_dither_menu_stable_tail_lower_bound(*case)
        )
        print(
            f"n,k0,t0,t1,D,C,q={case}: forced_gap={forced_gap}, "
            f"valid_menus={valid_menu_count}, tail_thresholds={thresholds}"
        )
    adjacent_remainder_cases = [
        (256, 128, 5, 8),
        (256, 128, 5, 16),
        (1024, 256, 8, 16),
        (1024, 256, 8, 32),
    ]
    for case in adjacent_remainder_cases:
        strict = verify_adjacent_slack_remainder_obstruction(*case)
        print(
            f"n,k0,t0,m={case}: H_adjacent_rem={dict(sorted(strict.items()))}, "
            f"mass={sum(strict.values())}"
        )
    maximal_cases = [
        (8, 2, 4, 6),
        (8, 4, 4, 6),
        (8, 6, 4, 6),
        (8, 8, 4, 6),
        (4, 16, 2, 6),
        (3, 4, 2, 5),
        (10, 3, 4, 8),
    ]
    for case in maximal_cases:
        all_scale = verify_maximal_dither_all_scale_case(*case)
        print(
            f"N,m,L,t={case}: H_max={dict(sorted(all_scale.items()))}, "
            f"mass={sum(all_scale.values())}"
        )
    confinement_cases = [
        (256, 128, 5),
        (256, 64, 8),
        (1024, 256, 9),
        (1024, 128, 17),
    ]
    for case in confinement_cases:
        small_scales = verify_maximal_dither_scale_confinement(*case)
        print(f"n,k0,t={case}: small_scales={small_scales}")
    obstruction_cases = [
        (64, 16, 3, 9, 0, 4),
        (256, 128, 4, 12, -1, 3),
    ]
    for case in obstruction_cases:
        rows = verify_adjacent_slack_dither_obstruction(*case)
        print(f"n,k0,t0,t1,r0,r1={case}: scale2_active={rows}")
    window_ledger_cases = [
        (128, 64, 3, 18, range(0, 4), [2, 4, 8]),
        (256, 64, 5, 24, range(-1, 3), [2, 4, 8, 16]),
    ]
    for case in window_ledger_cases:
        rows = verify_fixed_dither_slack_window_ledger(*case)
        print(f"n,k0,t0,t1,rs,scales={case}: window_active={rows}")
    random_line_cases = [
        (256, 128, 5, 17),
        (256, 64, 8, 17),
        (1024, 256, 9, 257),
        (1024, 128, 17, 257),
    ]
    for case in random_line_cases:
        rows = verify_maximal_dither_random_line_ledger(*case)
        print(f"n,k0,t,q={case}: R_MAX={rows}")
    print("M1 quotient remainder profile verifier passed")


if __name__ == "__main__":
    main()
