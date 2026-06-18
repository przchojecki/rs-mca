#!/usr/bin/env python3
"""Verify M1 quotient-fiber exchange profiles.

This checks the closed fixed-support enumerators in
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


def convolve(left, right):
    product = Counter()
    for left_exponent, left_coeff in left.items():
        for right_exponent, right_coeff in right.items():
            add_term(
                product,
                left_coeff * right_coeff,
                left_exponent + right_exponent,
            )
    return +product


def fiber_transition_enumerator(m, old_occupancy, new_occupancy):
    """Return the one-fiber exchange enumerator for fixed occupancies."""

    poly = Counter()
    overlap_min = max(0, old_occupancy + new_occupancy - m)
    overlap_max = min(old_occupancy, new_occupancy)
    for overlap in range(overlap_min, overlap_max + 1):
        coeff = (
            choose(old_occupancy, overlap)
            * choose(m - old_occupancy, new_occupancy - overlap)
        )
        add_term(poly, coeff, old_occupancy - overlap)
    return +poly


def occupancy_cross_profile_enumerator(N, m, source_histogram, target_histogram):
    """Fixed-source exchange enumerator between two occupancy histograms."""

    assert len(source_histogram) == m + 1
    assert len(target_histogram) == m + 1
    assert sum(source_histogram) == N
    assert sum(target_histogram) == N
    target = tuple(target_histogram)
    zero_counts = (0,) * (m + 1)
    dp = {zero_counts: Counter({0: 1})}

    for old_occupancy, count in enumerate(source_histogram):
        for _ in range(count):
            next_dp = {}
            for counts, poly in dp.items():
                for new_occupancy in range(m + 1):
                    if counts[new_occupancy] >= target[new_occupancy]:
                        continue
                    next_counts = list(counts)
                    next_counts[new_occupancy] += 1
                    next_counts = tuple(next_counts)
                    transition = fiber_transition_enumerator(
                        m,
                        old_occupancy,
                        new_occupancy,
                    )
                    updated = convolve(poly, transition)
                    if next_counts not in next_dp:
                        next_dp[next_counts] = Counter()
                    next_dp[next_counts].update(updated)
            dp = {counts: +poly for counts, poly in next_dp.items()}

    return +dp[target]


def occupancy_profile_enumerator(N, m, histogram):
    """Fixed-support exchange enumerator for one occupancy histogram."""

    return occupancy_cross_profile_enumerator(N, m, histogram, histogram)


def occupancy_family_size(N, m, histogram):
    assert len(histogram) == m + 1
    assert sum(histogram) == N
    remaining = N
    assignment_count = 1
    subset_count = 1
    for occupancy, count in enumerate(histogram):
        assignment_count *= choose(remaining, count)
        remaining -= count
        subset_count *= choose(m, occupancy) ** count
    return assignment_count * subset_count


def occupancy_histograms(N, m, support_size):
    rows = []

    def visit(occupancy, remaining_fibers, remaining_support, prefix):
        if occupancy == m + 1:
            if remaining_fibers == 0 and remaining_support == 0:
                rows.append(tuple(prefix))
            return

        max_count = remaining_fibers
        if occupancy:
            max_count = min(max_count, remaining_support // occupancy)
        for count in range(max_count + 1):
            prefix.append(count)
            visit(
                occupancy + 1,
                remaining_fibers - count,
                remaining_support - occupancy * count,
                prefix,
            )
            prefix.pop()

    visit(0, N, support_size, [])
    return tuple(rows)


def whole_fiber_histogram(N, m, L):
    histogram = [0] * (m + 1)
    histogram[0] = N - L
    histogram[m] = L
    return tuple(histogram)


def one_remainder_histogram(N, m, L, b):
    histogram = [0] * (m + 1)
    histogram[0] = N - L - 1
    histogram[b] = 1
    histogram[m] = L
    return tuple(histogram)


def whole_fiber_formula_enumerator(N, m, L):
    poly = Counter()
    for h in range(0, min(L, N - L) + 1):
        add_term(poly, choose(L, h) * choose(N - L, h), h * m)
    return +poly


def support_from_fiber_subsets(fiber_subsets):
    out = set()
    for subset in fiber_subsets:
        out.update(subset)
    return frozenset(out)


def occupancy_histogram_family(N, m, histogram):
    fibers = [
        tuple((fiber_index, point_index) for point_index in range(m))
        for fiber_index in range(N)
    ]
    choices_by_size = {
        size: tuple(combinations(fibers[0], size))
        for size in range(m + 1)
    }
    family = []

    def visit_occupancies(index, remaining, occupancies):
        if index == N:
            if all(count == 0 for count in remaining):
                fiber_choices = []
                for fiber_index, occupancy in enumerate(occupancies):
                    choices = []
                    for local_choice in choices_by_size[occupancy]:
                        choices.append(
                            tuple(
                                (fiber_index, point_index)
                                for _, point_index in local_choice
                            )
                        )
                    fiber_choices.append(tuple(choices))
                for selected in product_tuples(fiber_choices):
                    family.append(support_from_fiber_subsets(selected))
            return

        for occupancy, count in enumerate(remaining):
            if count == 0:
                continue
            next_remaining = list(remaining)
            next_remaining[occupancy] -= 1
            visit_occupancies(
                index + 1,
                tuple(next_remaining),
                occupancies + (occupancy,),
            )

    visit_occupancies(0, tuple(histogram), ())
    return family


def product_tuples(items):
    if not items:
        yield ()
        return
    first, *rest = items
    for value in first:
        for suffix in product_tuples(rest):
            yield (value,) + suffix


def brute_occupancy_profile_enumerator(N, m, histogram):
    family = occupancy_histogram_family(N, m, histogram)
    fixed = family[0]
    return Counter(len(fixed - other) for other in family)


def brute_occupancy_cross_profile_enumerator(
    N,
    m,
    source_histogram,
    target_histogram,
):
    source_family = occupancy_histogram_family(N, m, source_histogram)
    target_family = occupancy_histogram_family(N, m, target_histogram)
    fixed = source_family[0]
    return Counter(len(fixed - other) for other in target_family)


def verify_occupancy_profile_case(N, m, histogram):
    formula = occupancy_profile_enumerator(N, m, histogram)
    brute = brute_occupancy_profile_enumerator(N, m, histogram)
    assert formula == brute, (N, m, histogram, formula, brute)
    assert sum(formula.values()) == occupancy_family_size(N, m, histogram)
    return formula


def verify_occupancy_cross_profile_case(N, m, source_histogram, target_histogram):
    formula = occupancy_cross_profile_enumerator(
        N,
        m,
        source_histogram,
        target_histogram,
    )
    brute = brute_occupancy_cross_profile_enumerator(
        N,
        m,
        source_histogram,
        target_histogram,
    )
    assert formula == brute, (
        N,
        m,
        source_histogram,
        target_histogram,
        formula,
        brute,
    )
    assert sum(formula.values()) == occupancy_family_size(
        N,
        m,
        target_histogram,
    )
    return formula


def verify_occupancy_profile_specializations():
    rows = []
    whole_cases = [
        (5, 3, 2),
        (6, 4, 2),
        (7, 3, 3),
    ]
    for N, m, L in whole_cases:
        histogram = whole_fiber_histogram(N, m, L)
        general = occupancy_profile_enumerator(N, m, histogram)
        expected = whole_fiber_formula_enumerator(N, m, L)
        assert general == expected, (N, m, L, general, expected)
        rows.append(("whole", N, m, L, dict(sorted(general.items()))))

    remainder_cases = [
        (5, 4, 1, 1),
        (6, 3, 2, 1),
        (7, 4, 3, 2),
    ]
    for N, m, L, b in remainder_cases:
        histogram = one_remainder_histogram(N, m, L, b)
        general = occupancy_profile_enumerator(N, m, histogram)
        expected = formula_enumerator(N, m, L, b)
        assert general == expected, (N, m, L, b, general, expected)
        rows.append(("remainder", N, m, L, b, dict(sorted(general.items()))))

    brute_cases = [
        (4, 3, (1, 2, 1, 0)),
        (4, 3, (1, 1, 1, 1)),
        (5, 2, (1, 2, 2)),
    ]
    for case in brute_cases:
        formula = verify_occupancy_profile_case(*case)
        rows.append(("brute",) + case + (dict(sorted(formula.items())),))

    return tuple(rows)


def verify_occupancy_cross_profile_specializations():
    rows = []
    cases = [
        (4, 3, (1, 2, 1, 0), (1, 1, 1, 1)),
        (4, 3, (1, 1, 1, 1), (1, 2, 1, 0)),
        (5, 2, (1, 2, 2), (2, 1, 2)),
        (5, 3, (1, 2, 1, 1), (0, 4, 0, 1)),
    ]
    for case in cases:
        formula = verify_occupancy_cross_profile_case(*case)
        rows.append(case + (dict(sorted(formula.items())),))

    symmetric_cases = [
        (4, 3, (1, 2, 1, 0), (0, 4, 0, 0)),
        (5, 2, (2, 1, 2), (1, 3, 1)),
    ]
    for N, m, left, right in symmetric_cases:
        left_to_right = occupancy_cross_profile_enumerator(N, m, left, right)
        right_to_left = occupancy_cross_profile_enumerator(N, m, right, left)
        left_size = occupancy_family_size(N, m, left)
        right_size = occupancy_family_size(N, m, right)
        for exponent in set(left_to_right) | set(right_to_left):
            assert left_size * left_to_right[exponent] == (
                right_size * right_to_left[exponent]
            ), (N, m, left, right, exponent, left_to_right, right_to_left)

    return tuple(rows)


def verify_occupancy_histogram_exhaustion():
    rows = []
    cases = [
        (4, 3, 4),
        (5, 2, 5),
        (5, 4, 6),
        (6, 3, 7),
    ]
    for N, m, support_size in cases:
        histograms = occupancy_histograms(N, m, support_size)
        assert histograms
        total = 0
        for histogram in histograms:
            assert len(histogram) == m + 1
            assert sum(histogram) == N
            assert sum(
                occupancy * count
                for occupancy, count in enumerate(histogram)
            ) == support_size
            family_size = occupancy_family_size(N, m, histogram)
            profile = occupancy_profile_enumerator(N, m, histogram)
            assert sum(profile.values()) == family_size
            total += family_size
        assert total == choose(N * m, support_size), (
            N,
            m,
            support_size,
            total,
            choose(N * m, support_size),
        )
        rows.append((N, m, support_size, len(histograms), total))
    return tuple(rows)


def verify_occupancy_union_johnson_recovery():
    rows = []
    cases = [
        (4, 3, 4),
        (5, 2, 5),
        (5, 3, 6),
    ]
    for N, m, support_size in cases:
        histograms = occupancy_histograms(N, m, support_size)
        domain_size = N * m
        max_exchange = min(support_size, domain_size - support_size)
        johnson = Counter(
            {
                exchange: choose(support_size, exchange)
                * choose(domain_size - support_size, exchange)
                for exchange in range(0, max_exchange + 1)
            }
        )
        ordered = Counter()
        for source in histograms:
            fixed_source = Counter()
            source_size = occupancy_family_size(N, m, source)
            for target in histograms:
                profile = occupancy_cross_profile_enumerator(N, m, source, target)
                fixed_source.update(profile)
                for exchange, count in profile.items():
                    ordered[exchange] += source_size * count
            assert fixed_source == johnson, (
                N,
                m,
                support_size,
                source,
                fixed_source,
                johnson,
            )

        support_layer_size = choose(domain_size, support_size)
        for exchange, count in johnson.items():
            assert ordered[exchange] == support_layer_size * count, (
                N,
                m,
                support_size,
                exchange,
                ordered[exchange],
                support_layer_size * count,
            )
        rows.append((N, m, support_size, len(histograms), dict(sorted(johnson.items()))))
    return tuple(rows)


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


def dither_menu_capacity(menu_size, safe_gap):
    pairs = menu_size // 2
    singleton = menu_size % 2
    return pairs * (3 * safe_gap + 1) + singleton * safe_gap


def exact_min_menu_size_for_gap(window_length, safe_gap):
    even_pairs = ceil_div(window_length, 3 * safe_gap + 1)
    even_size = 2 * even_pairs
    if window_length <= safe_gap:
        odd_size = 1
    else:
        odd_pairs = ceil_div(window_length - safe_gap, 3 * safe_gap + 1)
        odd_size = 2 * odd_pairs + 1
    return min(even_size, odd_size)


def exact_min_safe_gap_for_menu_size(window_length, menu_size):
    pairs = menu_size // 2
    singleton = menu_size % 2
    coefficient = 3 * pairs + singleton
    offset = pairs
    return max(1, ceil_div(max(0, window_length - offset), coefficient))


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


def exists_dither_menu_cover(t_start, t_end, max_menu_size, max_gap):
    candidates = range(t_start - max_gap, t_end + max_gap + 1)
    for size in range(1, max_menu_size + 1):
        for menu in combinations(candidates, size):
            if menu_covers_window(t_start, t_end, menu, max_gap):
                return True, menu
    return False, ()


def exact_dither_menu_construction(t_start, t_end, menu_size, max_gap):
    cursor = t_start
    menu = []
    for _ in range(menu_size // 2):
        if cursor > t_end:
            break
        menu.extend([cursor + max_gap, cursor + 2 * max_gap])
        cursor += 3 * max_gap + 1
    if menu_size % 2 and cursor <= t_end:
        menu.append(cursor + max_gap)
    return tuple(menu)


def verify_dither_menu_covering_bound(t_start, t_end, max_gap):
    assert 1 <= t_start <= t_end
    assert max_gap >= 1
    window_length = t_end - t_start + 1
    exact_minimum = exact_min_menu_size_for_gap(window_length, max_gap)
    coarse_lower_bound = ceil_div(window_length, 2 * max_gap)
    assert coarse_lower_bound <= exact_minimum

    construction = exact_dither_menu_construction(
        t_start,
        t_end,
        exact_minimum,
        max_gap,
    )
    assert len(construction) <= exact_minimum
    assert menu_covers_window(t_start, t_end, construction, max_gap)
    assert dither_menu_capacity(exact_minimum, max_gap) >= window_length
    if exact_minimum > 1:
        assert dither_menu_capacity(exact_minimum - 1, max_gap) < window_length

    candidates = range(t_start - max_gap, t_end + max_gap + 1)
    for size in range(exact_minimum):
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

    return exact_minimum, coarse_lower_bound, construction


def verify_exact_dither_menu_capacity_grid(max_window_length, max_menu_size, max_gap):
    rows = []
    for window_length in range(1, max_window_length + 1):
        for gap in range(1, max_gap + 1):
            t_start = 1
            t_end = window_length
            exact_minimum, _, construction = verify_dither_menu_covering_bound(
                t_start,
                t_end,
                gap,
            )
            capacity_minimum = min(
                size
                for size in range(1, exact_minimum + 2)
                if dither_menu_capacity(size, gap) >= window_length
            )
            assert exact_minimum == capacity_minimum
            assert len(construction) <= exact_minimum
            assert menu_covers_window(t_start, t_end, construction, gap)

        for menu_size in range(1, max_menu_size + 1):
            forced_gap = exact_min_safe_gap_for_menu_size(
                window_length,
                menu_size,
            )
            capacity_gap = min(
                gap
                for gap in range(1, forced_gap + 2)
                if dither_menu_capacity(menu_size, gap) >= window_length
            )
            assert forced_gap == capacity_gap
            construction = exact_dither_menu_construction(
                1,
                window_length,
                menu_size,
                forced_gap,
            )
            assert menu_covers_window(1, window_length, construction, forced_gap)
            if forced_gap > 1:
                exists, menu = exists_dither_menu_cover(
                    1,
                    window_length,
                    menu_size,
                    forced_gap - 1,
                )
                assert not exists, (window_length, menu_size, forced_gap, menu)
            rows.append((window_length, menu_size, forced_gap))
    return rows


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
    forced_gap = exact_min_safe_gap_for_menu_size(window_length, menu_size)
    assert 1 <= forced_gap <= max_gap
    assert dither_menu_capacity(menu_size, max_gap) >= window_length
    if forced_gap > 1:
        assert dither_menu_capacity(menu_size, forced_gap - 1) < window_length

    candidates = range(t_start - max_gap, t_end + max_gap + 1)
    valid_menus = [
        menu
        for menu in combinations(candidates, menu_size)
        if menu_covers_window(t_start, t_end, menu, max_gap)
    ]
    assert valid_menus

    scale_thresholds = []
    adaptive_mass = n - k0 - 1
    for m in dyadic_divisors(k0):
        if m < t_end + max_gap:
            continue
        side_floor = min(k0 // m, (n - k0) // m)
        mass_threshold = side_floor * choose(m, forced_gap) - 1
        assert mass_threshold > 0
        weighted_threshold = mass_threshold * q ** (t_start - max_gap)
        mass_dominates = mass_threshold > adaptive_mass
        weighted_dominates = mass_threshold > adaptive_mass * q ** (max_gap - 1)
        window_weighted_dominates = (
            mass_threshold
            > adaptive_mass * q ** (t_end - 1 - (t_start - max_gap))
        )
        scale_thresholds.append(
            (
                m,
                mass_threshold,
                weighted_threshold,
                mass_dominates,
                weighted_dominates,
                window_weighted_dominates,
            )
        )
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
        for (
            m,
            mass_threshold,
            weighted_threshold,
            mass_dominates,
            weighted_dominates,
            window_weighted_dominates,
        ) in scale_thresholds:
            strict = verify_two_sided_fixed_dither_stable_tail(n, k0, r, t, m)
            correction = weighted_strict_correction(strict, t, q)
            adaptive_correction = adaptive_mass * q ** (t - 1)
            adaptive_window_correction = adaptive_mass * q ** (t_end - 1)
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
            assert (mass_threshold > adaptive_mass) == mass_dominates
            if mass_dominates:
                assert sum(strict.values()) > adaptive_mass
            if weighted_dominates:
                assert correction > adaptive_correction
            if window_weighted_dominates:
                assert correction > adaptive_window_correction

    return forced_gap, tuple(scale_thresholds), len(valid_menus)


def verify_adaptive_threshold_closed_form(n, k0, forced_gap, max_gap, q):
    assert forced_gap >= 1
    assert max_gap >= forced_gap
    assert q > 1

    side_total = min(k0, n - k0)
    adaptive_mass = n - k0 - 1
    weighted_factor = q ** (max_gap - 1)
    rows = []
    for m in dyadic_divisors(k0):
        if m <= 1 or m < forced_gap or n % m:
            continue
        side_floor = min(k0 // m, (n - k0) // m)
        assert side_floor == side_total // m

        mass_floor = side_floor * choose(m, forced_gap) - 1
        closed_numerator = side_total * choose(m - 1, forced_gap - 1)
        assert closed_numerator % forced_gap == 0
        closed_floor = closed_numerator // forced_gap - 1
        assert mass_floor == closed_floor

        mass_dominates = mass_floor > adaptive_mass
        mass_threshold = closed_numerator > forced_gap * (n - k0)
        assert mass_dominates == mass_threshold

        weighted_dominates = mass_floor > adaptive_mass * weighted_factor
        weighted_threshold = closed_numerator > forced_gap * (
            adaptive_mass * weighted_factor + 1
        )
        assert weighted_dominates == weighted_threshold

        rows.append((m, mass_floor, mass_dominates, weighted_dominates))

    assert rows
    return tuple(rows)


def verify_window_weighted_threshold_closed_form(
    n,
    k0,
    forced_gap,
    max_gap,
    window_length,
    q,
):
    assert forced_gap >= 1
    assert max_gap >= forced_gap
    assert window_length >= 1
    assert q > 1

    side_total = min(k0, n - k0)
    adaptive_mass = n - k0 - 1
    window_factor = q ** (window_length + max_gap - 2)
    rows = []
    for m in dyadic_divisors(k0):
        if m <= 1 or m < forced_gap or n % m:
            continue
        side_floor = min(k0 // m, (n - k0) // m)
        assert side_floor == side_total // m

        mass_floor = side_floor * choose(m, forced_gap) - 1
        closed_numerator = side_total * choose(m - 1, forced_gap - 1)
        assert mass_floor == closed_numerator // forced_gap - 1

        window_weighted_dominates = mass_floor > adaptive_mass * window_factor
        window_threshold = closed_numerator > forced_gap * (
            adaptive_mass * window_factor + 1
        )
        assert window_weighted_dominates == window_threshold

        rows.append((m, mass_floor, window_weighted_dominates))

    assert rows
    return tuple(rows)


def adaptive_competitive_menu_size_formula(window_length):
    quotient, remainder = divmod(window_length, 4)
    if remainder == 0:
        return 2 * quotient
    if remainder == 1:
        return 2 * quotient + 1
    return 2 * quotient + 2


def verify_adaptive_competitive_menu_size(max_window_length, max_menu_size):
    rows = []
    for window_length in range(1, max_window_length + 1):
        formula_size = adaptive_competitive_menu_size_formula(window_length)
        exact_size = exact_min_menu_size_for_gap(window_length, 1)
        assert formula_size == exact_size
        assert dither_menu_capacity(exact_size, 1) >= window_length
        if exact_size > 1:
            assert dither_menu_capacity(exact_size - 1, 1) < window_length

        for menu_size in range(1, max_menu_size + 1):
            forced_gap = exact_min_safe_gap_for_menu_size(
                window_length,
                menu_size,
            )
            assert (forced_gap == 1) == (menu_size >= exact_size)

        rows.append((window_length, exact_size))
    return tuple(rows)


def verify_finite_menu_large_scale_dichotomy(max_window_length, max_menu_size):
    rows = []
    for window_length in range(1, max_window_length + 1):
        adaptive_size = adaptive_competitive_menu_size_formula(window_length)
        for menu_size in range(1, max_menu_size + 1):
            forced_gap = exact_min_safe_gap_for_menu_size(
                window_length,
                menu_size,
            )
            if menu_size >= adaptive_size:
                assert forced_gap == 1
                regime = "finite_prefix_linear"
                degree = 1
            else:
                assert forced_gap >= 2
                regime = "forced_superlinear_tail"
                degree = forced_gap
            rows.append((window_length, menu_size, forced_gap, regime, degree))
    return tuple(rows)


def verify_gap_one_menu_linear_tail(n, k0, t_start, t_end, q):
    assert k0 <= n - k0
    window_length = t_end - t_start + 1
    menu_size = adaptive_competitive_menu_size_formula(window_length)
    menu = exact_dither_menu_construction(t_start, t_end, menu_size, 1)
    assert menu_covers_window(t_start, t_end, menu, 1)
    if menu_size > 1:
        assert not menu_covers_window(t_start, t_end, menu[:-1], 1)

    adaptive_mass = n - k0 - 1
    rows = []
    for t in range(t_start, t_end + 1):
        choices = [r for r in menu if r != t and abs(t - r) == 1]
        assert choices, (t_start, t_end, menu, t)
        for r in choices:
            expected_mass = n - k0 - 1 if r == t - 1 else k0 - 1
            assert expected_mass <= adaptive_mass
            for m in dyadic_divisors(k0):
                if m < t + 1:
                    continue
                strict = verify_two_sided_fixed_dither_stable_tail(
                    n,
                    k0,
                    r,
                    t,
                    m,
                )
                correction = weighted_strict_correction(strict, t, q)
                assert dict(strict) == {1: expected_mass}
                assert correction == expected_mass * q ** (t - 1)
                assert correction <= adaptive_mass * q ** (t - 1)
            rows.append((t, r, expected_mass))

    return menu_size, tuple(menu), tuple(rows)


def verify_gap_one_window_scale_confinement(n, k0, t_start, t_end):
    assert 1 <= t_start <= t_end
    menu_size = adaptive_competitive_menu_size_formula(t_end - t_start + 1)
    menu = exact_dither_menu_construction(t_start, t_end, menu_size, 1)
    assert menu_covers_window(t_start, t_end, menu, 1)

    finite_prefix = [m for m in dyadic_divisors(k0) if m <= t_end]
    expected_count = 0 if t_end < 2 else t_end.bit_length() - 1
    expected_count = min(expected_count, len(dyadic_divisors(k0)))
    assert len(finite_prefix) == expected_count

    rows = []
    for t in range(t_start, t_end + 1):
        choices = [r for r in menu if r != t and abs(t - r) == 1]
        assert choices
        for r in choices:
            for m in dyadic_divisors(k0):
                if m <= t_end:
                    continue
                if r == t - 1:
                    N = n // m
                    L = k0 // m
                    profile = maximal_dither_all_scale_enumerator(N, m, L, t)
                    expected = Counter({1: n - k0 - 1})
                else:
                    N = n // m
                    L = k0 // m - 1
                    profile = co_maximal_dither_all_scale_enumerator(N, m, L, t)
                    expected = Counter({1: k0 - 1})
                assert profile == expected, (n, k0, t_start, t_end, t, r, m)
            rows.append((t, r))

    return tuple(finite_prefix), tuple(rows)


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


def co_maximal_dither_all_scale_enumerator(N, m, L, t):
    assert 0 <= L <= N - 1
    return maximal_dither_all_scale_enumerator(N, m, N - L - 1, t)


def verify_co_maximal_dither_all_scale_case(N, m, L, t):
    full = formula_enumerator(N, m, L, m - 1)
    strict = Counter(
        {exponent: coeff for exponent, coeff in full.items() if 0 < exponent < t}
    )
    all_scale = co_maximal_dither_all_scale_enumerator(N, m, L, t)
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


def expected_co_maximal_dither_profile(n, k0, m, t):
    expected = Counter({1: k0 - 1})
    if m == t:
        expected[t - 1] += n - k0
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


def verify_co_maximal_dither_scale_confinement(n, k0, t):
    small_scales = [m for m in dyadic_divisors(k0) if m < t]
    nonlinear_scales = []

    for m in dyadic_divisors(k0):
        N = n // m
        L = k0 // m - 1
        assert 0 <= L <= N - 1
        profile = co_maximal_dither_all_scale_enumerator(N, m, L, t)
        if m >= t:
            expected = expected_co_maximal_dither_profile(n, k0, m, t)
            assert profile == expected, (n, k0, m, t, profile, expected)
        else:
            nonlinear_scales.append(m)

    assert nonlinear_scales == small_scales
    return small_scales


def verify_adaptive_maximal_dither_window_baseline(n, k0, t_start, t_end, q):
    assert 1 <= t_start <= t_end
    assert q > 1
    stable_scales = [m for m in dyadic_divisors(k0) if m > t_end]
    assert stable_scales
    rows = []
    for t in range(t_start, t_end + 1):
        for m in stable_scales:
            N = n // m
            L = k0 // m
            profile = maximal_dither_all_scale_enumerator(N, m, L, t)
            expected = Counter({1: n - k0 - 1})
            assert profile == expected, (n, k0, t_start, t_end, t, m, profile)
            correction = weighted_strict_correction(profile, t, q)
            expected_correction = (n - k0 - 1) * q ** (t - 1)
            assert correction == expected_correction, (
                n,
                k0,
                t,
                m,
                q,
                correction,
                expected_correction,
            )
            rows.append((t, m, correction))
    max_correction = max(value for _, _, value in rows)
    assert max_correction == (n - k0 - 1) * q ** (t_end - 1)
    return stable_scales, max_correction


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
    occupancy_rows = verify_occupancy_profile_specializations()
    print(f"fiber occupancy profile cases={occupancy_rows}")
    occupancy_cross_rows = verify_occupancy_cross_profile_specializations()
    print(f"fiber occupancy cross-profile cases={occupancy_cross_rows}")
    occupancy_exhaustion = verify_occupancy_histogram_exhaustion()
    print(f"fiber occupancy histogram exhaustion={occupancy_exhaustion}")
    occupancy_johnson = verify_occupancy_union_johnson_recovery()
    print(f"fiber occupancy Johnson recovery={occupancy_johnson}")

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
        exact_minimum, coarse_lower_bound, construction = (
            verify_dither_menu_covering_bound(*case)
        )
        print(
            f"t0,t1,D={case}: exact_menu={exact_minimum}, "
            f"coarse_lower={coarse_lower_bound}, construction={construction}"
        )
    capacity_grid = verify_exact_dither_menu_capacity_grid(
        max_window_length=10,
        max_menu_size=4,
        max_gap=3,
    )
    print(
        "exact dither-menu capacity grid passed: "
        f"{len(capacity_grid)} forced-gap cases"
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
    threshold_cases = [
        (256, 128, 1, 3, 17),
        (256, 128, 2, 3, 17),
        (256, 64, 2, 3, 17),
        (1024, 128, 2, 3, 257),
        (1024, 256, 3, 3, 17),
    ]
    for case in threshold_cases:
        rows = verify_adaptive_threshold_closed_form(*case)
        print(f"n,k0,E,D,q={case}: adaptive_thresholds={rows}")
    window_threshold_cases = [
        (256, 128, 3, 3, 8, 17),
        (2**20, 2**19, 4, 4, 4, 17),
    ]
    for case in window_threshold_cases:
        rows = verify_window_weighted_threshold_closed_form(*case)
        print(f"n,k0,E,D,L,q={case}: window_weighted_thresholds={rows}")
    adaptive_menu_rows = verify_adaptive_competitive_menu_size(
        max_window_length=20,
        max_menu_size=12,
    )
    print(f"adaptive-competitive menu sizes={adaptive_menu_rows}")
    dichotomy_rows = verify_finite_menu_large_scale_dichotomy(
        max_window_length=12,
        max_menu_size=8,
    )
    print(f"finite-menu large-scale dichotomy cases={len(dichotomy_rows)}")
    gap_one_menu_cases = [
        (256, 128, 5, 12, 17),
        (1024, 256, 9, 15, 257),
    ]
    for case in gap_one_menu_cases:
        menu_size, menu, rows = verify_gap_one_menu_linear_tail(*case)
        print(
            f"n,k0,t0,t1,q={case}: gap_one_menu_size={menu_size}, "
            f"menu={menu}, linear_rows={rows}"
        )
    gap_one_confinement_cases = [
        (256, 128, 5, 12),
        (1024, 256, 9, 15),
        (1024, 128, 13, 17),
    ]
    for case in gap_one_confinement_cases:
        prefix, rows = verify_gap_one_window_scale_confinement(*case)
        print(
            f"n,k0,t0,t1={case}: gap_one_prefix={prefix}, "
            f"served_rows={rows}"
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
    co_maximal_cases = [
        (8, 8, 3, 6),
        (4, 16, 1, 6),
        (10, 10, 4, 6),
        (6, 4, 2, 5),
    ]
    for case in co_maximal_cases:
        all_scale = verify_co_maximal_dither_all_scale_case(*case)
        print(
            f"N,m,L,t={case}: H_comax={dict(sorted(all_scale.items()))}, "
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
        co_small_scales = verify_co_maximal_dither_scale_confinement(*case)
        print(
            f"n,k0,t={case}: small_scales={small_scales}, "
            f"co_small_scales={co_small_scales}"
        )
    adaptive_window_cases = [
        (256, 128, 5, 8, 17),
        (256, 64, 8, 13, 17),
        (1024, 256, 9, 15, 257),
    ]
    for case in adaptive_window_cases:
        stable_scales, max_correction = (
            verify_adaptive_maximal_dither_window_baseline(*case)
        )
        print(
            f"n,k0,t0,t1,q={case}: adaptive_scales={stable_scales}, "
            f"max_R={max_correction}"
        )
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
