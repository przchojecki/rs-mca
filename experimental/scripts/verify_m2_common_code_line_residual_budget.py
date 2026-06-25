#!/usr/bin/env python3
"""Verify the M2 common-code-line residual budget on small RS codes."""

from __future__ import annotations

import itertools
import json
from typing import Any


def eval_poly(coeffs: tuple[int, ...], x_value: int, prime: int) -> int:
    value = 0
    for coeff in reversed(coeffs):
        value = (value * x_value + coeff) % prime
    return value


def codewords(prime: int, dimension: int, domain: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        tuple(eval_poly(coeffs, x, prime) for x in domain)
        for coeffs in itertools.product(range(prime), repeat=dimension)
    }


def restriction(word: tuple[int, ...], support: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(word[i] for i in support)


def support_tables(
    words: set[tuple[int, ...]],
    n: int,
    agreement: int,
) -> dict[tuple[int, ...], set[tuple[int, ...]]]:
    return {
        support: {restriction(word, support) for word in words}
        for size in range(agreement, n + 1)
        for support in itertools.combinations(range(n), size)
    }


def word_add(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> tuple[int, ...]:
    return tuple((a + b) % prime for a, b in zip(left, right))


def word_sub(left: tuple[int, ...], right: tuple[int, ...], prime: int) -> tuple[int, ...]:
    return tuple((a - b) % prime for a, b in zip(left, right))


def word_scale(scalar: int, word: tuple[int, ...], prime: int) -> tuple[int, ...]:
    return tuple((scalar * value) % prime for value in word)


def supportwise_bad_slopes(
    f: tuple[int, ...],
    g: tuple[int, ...],
    prime: int,
    support_code: dict[tuple[int, ...], set[tuple[int, ...]]],
) -> tuple[list[int], list[tuple[int, tuple[int, ...]]]]:
    bad: set[int] = set()
    witnesses: list[tuple[int, tuple[int, ...]]] = []
    for slope in range(prime):
        line_word = word_add(f, word_scale(slope, g, prime), prime)
        for support, restrictions in support_code.items():
            if restriction(line_word, support) not in restrictions:
                continue
            contained = (
                restriction(f, support) in restrictions
                and restriction(g, support) in restrictions
            )
            if not contained:
                bad.add(slope)
                witnesses.append((slope, support))
    return sorted(bad), witnesses


def residual_report(
    *,
    label: str,
    prime: int,
    n: int,
    k: int,
    agreement: int,
    common_support: tuple[int, ...],
    f: tuple[int, ...],
    g: tuple[int, ...],
    c_f: tuple[int, ...],
    c_g: tuple[int, ...],
) -> dict[str, Any]:
    if agreement + len(common_support) - n < k:
        raise AssertionError("common support does not meet the MDS zero threshold")

    domain = tuple(range(n))
    words = codewords(prime, k, domain)
    support_code = support_tables(words, n, agreement)
    bad_slopes, witnesses = supportwise_bad_slopes(f, g, prime, support_code)

    f_res = word_sub(f, c_f, prime)
    g_res = word_sub(g, c_g, prime)
    omega = tuple(i for i in range(n) if i not in set(common_support))
    h = max(1, agreement - len(common_support))
    c0 = sum(1 for i in omega if f_res[i] == 0 and g_res[i] == 0)
    error_budget = n - agreement
    support_defect = len(omega)
    defect_h = max(1, support_defect - error_budget)
    if defect_h != h:
        raise AssertionError("defect-coordinate residual threshold mismatch")
    residual_bound = None
    if h > c0:
        residual_bound = (len(omega) - c0) // (h - c0)
    generic_no_common_bound = support_defect // defect_h

    residual_zero_counts = {
        slope: sum((f_res[i] + slope * g_res[i]) % prime == 0 for i in omega)
        for slope in range(prime)
    }

    for slope in bad_slopes:
        if residual_zero_counts[slope] < h:
            raise AssertionError(f"bad slope {slope} has too few residual zeros")
    if residual_bound is not None and len(bad_slopes) > residual_bound:
        raise AssertionError("support-wise bad slopes exceed residual bound")

    return {
        "label": label,
        "prime": prime,
        "n": n,
        "k": k,
        "agreement": agreement,
        "error_budget": error_budget,
        "common_support_size": len(common_support),
        "support_defect": support_defect,
        "omega_size": len(omega),
        "h": h,
        "c0": c0,
        "residual_bound": residual_bound,
        "generic_no_common_bound": generic_no_common_bound,
        "bad_slope_count": len(bad_slopes),
        "bad_slopes": bad_slopes,
        "witness_count": len(witnesses),
        "residual_zero_counts_on_bad_slopes": {
            str(slope): residual_zero_counts[slope] for slope in bad_slopes
        },
        "bound_verified": residual_bound is None or len(bad_slopes) <= residual_bound,
    }


def spike_case() -> dict[str, Any]:
    prime = 13
    n = 8
    k = 3
    agreement = n - 1
    spike_index = 7
    common_support = tuple(i for i in range(n) if i != spike_index)
    spike = tuple(1 if i == spike_index else 0 for i in range(n))
    base_slope = 4
    zero = (0,) * n
    f = word_scale(base_slope, spike, prime)
    g = spike
    report = residual_report(
        label="spike",
        prime=prime,
        n=n,
        k=k,
        agreement=agreement,
        common_support=common_support,
        f=f,
        g=g,
        c_f=zero,
        c_g=zero,
    )
    expected = [(-base_slope) % prime]
    if report["bad_slopes"] != expected or report["residual_bound"] != 1:
        raise AssertionError("spike case did not realize the sharp residual bound")
    return report


def deterministic_residual_case() -> dict[str, Any]:
    prime = 17
    n = 9
    k = 3
    agreement = 7
    common_support = tuple(range(5))
    zero = (0,) * n
    f = [0] * n
    g = [0] * n
    # Omega has four positions. The residual threshold is h=2. The chosen
    # residual pairs make each non-common outside coordinate point to a
    # distinct slope, so no slope has two residual zeros.
    for index, value in zip(range(5, 9), (1, 2, 3, 4)):
        f[index] = value
        g[index] = 1
    report = residual_report(
        label="distinct_outside_slopes",
        prime=prime,
        n=n,
        k=k,
        agreement=agreement,
        common_support=common_support,
        f=tuple(f),
        g=tuple(g),
        c_f=zero,
        c_g=zero,
    )
    if report["residual_bound"] != 2 or report["bad_slope_count"] > 2:
        raise AssertionError("deterministic residual case violated the expected bound")
    return report


def sharp_common_zero_residual_case() -> dict[str, Any]:
    prime = 17
    n = 10
    k = 3
    agreement = 8
    common_support = tuple(range(5))
    zero = (0,) * n
    f = [0] * n
    g = [0] * n
    # Here e=2, s=5, so h=s-e=3. One outside coordinate is a common
    # residual zero, leaving the sharp finite residual budget
    # (5-1)/(3-1)=2. Two private blocks of size h-c0=2 realize it.
    block_slopes = (3, 11)
    for slope, block in zip(block_slopes, ((6, 7), (8, 9))):
        for index in block:
            f[index] = (-slope) % prime
            g[index] = 1
    report = residual_report(
        label="sharp_one_common_residual_zero",
        prime=prime,
        n=n,
        k=k,
        agreement=agreement,
        common_support=common_support,
        f=tuple(f),
        g=tuple(g),
        c_f=zero,
        c_g=zero,
    )
    if report["h"] != 3 or report["c0"] != 1 or report["residual_bound"] != 2:
        raise AssertionError("common residual-zero case has wrong residual budget")
    if report["bad_slopes"] != sorted(block_slopes):
        raise AssertionError("common residual-zero case did not attain the bound")
    return report


def exhaustive_minimax_case(
    *,
    label: str,
    prime: int,
    n: int,
    k: int,
    agreement: int,
    common_support_size: int,
    common_zero_count: int,
) -> dict[str, Any]:
    common_support = tuple(range(common_support_size))
    omega = tuple(i for i in range(n) if i not in set(common_support))
    h = max(1, agreement - common_support_size)
    if agreement + common_support_size - n < k:
        raise AssertionError("exhaustive minimax case does not meet MDS forcing")
    if h <= common_zero_count:
        raise AssertionError("exhaustive minimax case needs positive denominator")

    expected = min(prime, (len(omega) - common_zero_count) // (h - common_zero_count))
    words = codewords(prime, k, tuple(range(n)))
    support_code = support_tables(words, n, agreement)
    max_bad = -1
    maximizer: dict[str, Any] | None = None
    assignment_count = 0

    for values in itertools.product(range(prime), repeat=2 * len(omega)):
        f = [0] * n
        g = [0] * n
        c0 = 0
        for index, coord in enumerate(omega):
            f_value = values[2 * index]
            g_value = values[2 * index + 1]
            f[coord] = f_value
            g[coord] = g_value
            if f_value == 0 and g_value == 0:
                c0 += 1
        if c0 != common_zero_count:
            continue
        assignment_count += 1
        bad_slopes, _ = supportwise_bad_slopes(tuple(f), tuple(g), prime, support_code)
        if len(bad_slopes) > max_bad:
            max_bad = len(bad_slopes)
            maximizer = {
                "f_on_omega": [f[i] for i in omega],
                "g_on_omega": [g[i] for i in omega],
                "bad_slopes": bad_slopes,
            }

    if max_bad != expected:
        raise AssertionError(
            f"exhaustive minimax {label} found max {max_bad}, expected {expected}"
        )
    return {
        "label": label,
        "prime": prime,
        "n": n,
        "k": k,
        "agreement": agreement,
        "common_support_size": common_support_size,
        "omega_size": len(omega),
        "h": h,
        "c0": common_zero_count,
        "expected_minimax": expected,
        "exhaustive_max_bad_slope_count": max_bad,
        "assignment_count": assignment_count,
        "sample_maximizer": maximizer,
    }


def threshold_necessity_counterexample() -> dict[str, Any]:
    prime = 17
    n = 8
    k = 3
    agreement = 4
    common_support = tuple(range(6))
    zero = (0,) * n
    f = [0] * n
    g = [0] * n
    f[7] = 1
    g[6] = 1

    words = codewords(prime, k, tuple(range(n)))
    support_code = support_tables(words, n, agreement)
    bad_slopes, witnesses = supportwise_bad_slopes(
        tuple(f), tuple(g), prime, support_code
    )

    omega = tuple(i for i in range(n) if i not in set(common_support))
    h = max(1, agreement - len(common_support))
    c0 = 0
    naive_residual_bound = (len(omega) - c0) // (h - c0)
    overlap_floor = agreement + len(common_support) - n

    formula_slopes = {
        ((6 - r1) * (6 - r2) * pow((7 - r1) * (7 - r2), -1, prime)) % prime
        for r1, r2 in itertools.combinations(common_support, 2)
    }
    expected = sorted({0} | formula_slopes)

    if overlap_floor >= k:
        raise AssertionError("threshold counterexample unexpectedly meets MDS forcing")
    if bad_slopes != expected:
        raise AssertionError("threshold counterexample slope set changed")
    if len(bad_slopes) <= naive_residual_bound:
        raise AssertionError("threshold counterexample does not violate residual bound")

    return {
        "label": "threshold_necessity_counterexample",
        "prime": prime,
        "n": n,
        "k": k,
        "agreement": agreement,
        "common_support_size": len(common_support),
        "omega_size": len(omega),
        "overlap_floor": overlap_floor,
        "h": h,
        "c0": c0,
        "naive_residual_bound": naive_residual_bound,
        "bad_slope_count": len(bad_slopes),
        "bad_slopes": bad_slopes,
        "formula_slope_count": len(formula_slopes),
        "witness_count": len(witnesses),
        "threshold_holds": overlap_floor >= k,
        "bound_violated_without_threshold": len(bad_slopes) > naive_residual_bound,
    }


def common_zero_degeneracy_case(prime: int) -> dict[str, Any]:
    if prime < 7 or prime % 2 == 0:
        raise AssertionError("common-zero degeneracy case expects an odd prime >= 7")

    n = prime
    k = 3
    agreement = (prime + 3) // 2
    common_support = tuple(range(agreement))
    omega = tuple(i for i in range(prime) if i not in set(common_support))
    common_zero = omega[0]
    private_points = omega[1:]
    private_count = len(private_points)
    f = [0] * n
    g = [0] * n
    slopes = tuple(range(1, private_count + 1))
    for point, slope in zip(private_points, slopes):
        f[point] = (-slope) % prime
        g[point] = 1

    words = codewords(prime, k, tuple(range(n)))

    def support_is_bad(slope: int, support: tuple[int, ...]) -> bool:
        restrictions = {restriction(word, support) for word in words}
        line_word = word_add(tuple(f), word_scale(slope, tuple(g), prime), prime)
        contained = (
            restriction(tuple(f), support) in restrictions
            and restriction(tuple(g), support) in restrictions
        )
        return restriction(line_word, support) in restrictions and not contained

    witness_base = common_support[: agreement - 2]
    witnesses: dict[int, tuple[int, ...]] = {}
    for point, slope in zip(private_points, slopes):
        support = witness_base + (common_zero, point)
        if not support_is_bad(slope, support):
            raise AssertionError("common-zero degeneracy witness failed")
        witnesses[slope] = support

    h = max(1, agreement - len(common_support))
    c0 = sum(1 for i in omega if f[i] == 0 and g[i] == 0)
    overlap_floor = agreement + len(common_support) - n
    if overlap_floor < k:
        raise AssertionError("common-zero degeneracy should meet MDS forcing")
    if h != c0:
        raise AssertionError("common-zero degeneracy should have h=c0")

    return {
        "label": f"common_zero_degeneracy_p{prime}",
        "prime": prime,
        "n": n,
        "k": k,
        "agreement": agreement,
        "common_support_size": len(common_support),
        "omega_size": len(omega),
        "overlap_floor": overlap_floor,
        "h": h,
        "c0": c0,
        "certified_bad_slope_count": len(witnesses),
        "threshold_holds": overlap_floor >= k,
        "denominator_positive": h > c0,
        "sample_witnesses": {
            str(key): witnesses[key] for key in sorted(witnesses)[: min(5, len(witnesses))]
        },
    }


def threshold_failure_family_case(prime: int) -> dict[str, Any]:
    if prime < 7:
        raise AssertionError("threshold family needs at least five usable units")

    n = prime
    k = 3
    agreement = 4
    common_support = tuple(i for i in range(prime) if i not in (0, 1))
    f = tuple(1 if i == 1 else 0 for i in range(n))
    g = tuple(1 if i == 0 else 0 for i in range(n))
    words = codewords(prime, k, tuple(range(n)))

    def support_is_bad(slope: int, support: tuple[int, ...]) -> bool:
        restrictions = {restriction(word, support) for word in words}
        line_word = word_add(f, word_scale(slope, g, prime), prime)
        contained = (
            restriction(f, support) in restrictions
            and restriction(g, support) in restrictions
        )
        return restriction(line_word, support) in restrictions and not contained

    witnesses: dict[int, tuple[int, ...]] = {}
    zero_support = (2, 3, 4, 0)
    if not support_is_bad(0, zero_support):
        raise AssertionError("zero slope is not witnessed in threshold family")
    witnesses[0] = zero_support

    for slope in range(1, prime):
        support = None
        for unit in range(1, prime):
            if unit == 1:
                continue
            other = (slope * pow(unit, -1, prime)) % prime
            if other in (0, 1) or other == unit:
                continue
            r1 = (unit * pow(unit - 1, -1, prime)) % prime
            r2 = (other * pow(other - 1, -1, prime)) % prime
            candidate = (r1, r2, 0, 1)
            if r1 in (0, 1) or r2 in (0, 1) or r1 == r2:
                continue
            if support_is_bad(slope, candidate):
                support = candidate
                break
        if support is None:
            raise AssertionError(f"slope {slope} has no threshold-family witness")
        witnesses[slope] = support

    omega = (0, 1)
    h = max(1, agreement - len(common_support))
    c0 = 0
    naive_residual_bound = len(omega) // h
    overlap_floor = agreement + len(common_support) - n

    if overlap_floor >= k:
        raise AssertionError("threshold family unexpectedly meets MDS forcing")
    if len(witnesses) != prime:
        raise AssertionError("threshold family did not witness every slope")

    return {
        "label": f"threshold_failure_family_p{prime}",
        "prime": prime,
        "n": n,
        "k": k,
        "agreement": agreement,
        "common_support_size": len(common_support),
        "omega_size": len(omega),
        "overlap_floor": overlap_floor,
        "h": h,
        "c0": c0,
        "naive_residual_bound": naive_residual_bound,
        "bad_slope_count": len(witnesses),
        "threshold_holds": overlap_floor >= k,
        "bound_violated_without_threshold": len(witnesses) > naive_residual_bound,
        "sample_witnesses": {str(key): witnesses[key] for key in range(min(prime, 5))},
    }


def main() -> None:
    reports = [
        spike_case(),
        deterministic_residual_case(),
        sharp_common_zero_residual_case(),
        exhaustive_minimax_case(
            label="exhaustive_minimax_no_common_zero",
            prime=5,
            n=5,
            k=2,
            agreement=4,
            common_support_size=3,
            common_zero_count=0,
        ),
        exhaustive_minimax_case(
            label="exhaustive_minimax_one_common_zero",
            prime=7,
            n=6,
            k=2,
            agreement=5,
            common_support_size=3,
            common_zero_count=1,
        ),
        common_zero_degeneracy_case(11),
        common_zero_degeneracy_case(17),
        threshold_failure_family_case(7),
        threshold_failure_family_case(11),
        threshold_failure_family_case(17),
        threshold_necessity_counterexample(),
    ]
    for report in reports:
        if "residual_bound" in report:
            print(
                "{label}: p={prime} n={n} k={k} agreement={agreement} "
                "b={common_support_size} e={error_budget} s={support_defect} "
                "h={h} c0={c0} bad={bad_slope_count} "
                "bound={residual_bound}".format(**report)
            )
        elif "expected_minimax" in report:
            print(
                "{label}: p={prime} n={n} k={k} agreement={agreement} "
                "b={common_support_size} omega={omega_size} h={h} c0={c0} "
                "max={exhaustive_max_bad_slope_count} expected={expected_minimax} "
                "assignments={assignment_count}".format(**report)
            )
        else:
            count = report.get("bad_slope_count", report.get("certified_bad_slope_count"))
            print(
                "{label}: p={prime} n={n} k={k} agreement={agreement} "
                "b={common_support_size} overlap={overlap_floor} "
                "h={h} c0={c0} bad={count}".format(count=count, **report)
            )
    print("m2_common_code_line_residual_budget: PASS")
    print("CERT " + json.dumps(reports, sort_keys=True))


if __name__ == "__main__":
    main()
