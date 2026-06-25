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


def main() -> None:
    reports = [
        spike_case(),
        deterministic_residual_case(),
        sharp_common_zero_residual_case(),
    ]
    for report in reports:
        print(
            "{label}: p={prime} n={n} k={k} agreement={agreement} "
            "b={common_support_size} e={error_budget} s={support_defect} "
            "h={h} c0={c0} bad={bad_slope_count} "
            "bound={residual_bound}".format(**report)
        )
    print("m2_common_code_line_residual_budget: PASS")
    print("CERT " + json.dumps(reports, sort_keys=True))


if __name__ == "__main__":
    main()
