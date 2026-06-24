#!/usr/bin/env python3
"""Counterexample-first scanner for a quotient-budgeted L1 locator conjecture.

This is EXPERIMENTAL evidence only.  It enumerates split-prime
monomial-prefix complement-locator fibers and separates each fiber by exact
cyclic stabilizer order.  The quotient budget is the exact mass with nontrivial
stabilizer; the primitive remainder is the exact stabilizer-one mass.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from math import comb, lgamma, log2
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


def mobius(value: int) -> int:
    factors = factorint(value)
    if any(exponent > 1 for exponent in factors.values()):
        return 0
    return -1 if len(factors) % 2 else 1


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


def primitive_root(p: int) -> int:
    if p == 2:
        return 1
    phi = p - 1
    primes = factorint(phi).keys()
    for candidate in range(2, p):
        if all(pow(candidate, phi // prime, p) != 1 for prime in primes):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def order_n_root(p: int, n: int) -> int:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    return pow(primitive_root(p), (p - 1) // n, p)


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    if k == 0 or k == n:
        return 0.0
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)) / LN2


def subset_mask(exponents: Iterable[int]) -> int:
    mask = 0
    for exponent in exponents:
        mask |= 1 << exponent
    return mask


def mask_to_exponents(mask: int, n: int) -> list[int]:
    return [index for index in range(n) if mask & (1 << index)]


def rotate_mask(mask: int, shift: int, n: int) -> int:
    shift %= n
    if shift == 0:
        return mask
    full = (1 << n) - 1
    return ((mask << shift) | (mask >> (n - shift))) & full


def stabilizer_order(mask: int, n: int) -> int:
    return sum(1 for shift in range(n) if rotate_mask(mask, shift, n) == mask)


def elementary_prefix_key(
    exponents: tuple[int, ...],
    root_powers: list[int],
    p: int,
    sigma: int,
) -> tuple[int, ...]:
    """Top locator coefficients below the monic leading term.

    If L_A(X) = prod_{e in A}(X - h^e), the returned key is
    (coeff X^{m-1}, coeff X^{m-2}, ...), truncated to sigma entries.
    """
    eff = min(sigma, len(exponents))
    elem = [0] * (eff + 1)
    elem[0] = 1
    used = 0
    for exponent in exponents:
        value = root_powers[exponent]
        used += 1
        top = min(used, eff)
        for index in range(top, 0, -1):
            elem[index] = (elem[index] + value * elem[index - 1]) % p
    return tuple(((-elem[index]) if index % 2 else elem[index]) % p
                 for index in range(1, eff + 1))


def fiber_stabilizer_ledger(members: list[int], n: int) -> dict[str, object]:
    divisors = positive_divisors(n)
    exact_direct = {divisor: 0 for divisor in divisors}
    for mask in members:
        exact_direct[stabilizer_order(mask, n)] += 1

    containing = {
        divisor: sum(count for order, count in exact_direct.items()
                     if order % divisor == 0)
        for divisor in divisors
    }
    exact_mobius = {
        divisor: sum(
            mobius(order // divisor) * containing[order]
            for order in divisors
            if order % divisor == 0
        )
        for divisor in divisors
    }
    return {
        "containing": containing,
        "exact": exact_mobius,
        "exact_direct": exact_direct,
        "mobius_inversion_ok": exact_direct == exact_mobius,
        "primitive": exact_mobius[1],
        "quotient_budget": sum(
            count for order, count in exact_mobius.items() if order > 1
        ),
    }


def scan_case(
    p: int,
    n: int,
    k: int,
    sigma: int,
    epsilon: float,
    alert_power: float,
    max_examples: int,
) -> dict[str, object]:
    a = k + sigma
    m = n - a
    if a < 0 or a > n:
        raise ValueError(f"need 0 <= k+sigma <= n, got n={n} k={k} sigma={sigma}")
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")

    root = order_n_root(p, n)
    root_powers = [pow(root, exponent, p) for exponent in range(n)]
    buckets: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for exponents in itertools.combinations(range(n), m):
        key = elementary_prefix_key(exponents, root_powers, p, sigma)
        buckets[key].append(subset_mask(exponents))

    divisors = positive_divisors(n)
    active_orders = [divisor for divisor in divisors if divisor > sigma]
    fiber_histogram: Counter[int] = Counter()
    primitive_histogram: Counter[int] = Counter()
    quotient_histogram: Counter[int] = Counter()
    max_fiber_size = 0
    max_primitive = -1
    max_quotient_budget = 0
    max_active_quotient_budget = 0
    mobius_ok = True
    primitive_examples: list[dict[str, object]] = []

    for key, members in buckets.items():
        ledger = fiber_stabilizer_ledger(members, n)
        exact = ledger["exact"]
        assert isinstance(exact, dict)
        primitive = int(ledger["primitive"])
        quotient_budget = int(ledger["quotient_budget"])
        active_quotient_budget = sum(int(exact[order]) for order in active_orders)
        size = len(members)
        fiber_histogram[size] += 1
        primitive_histogram[primitive] += 1
        quotient_histogram[quotient_budget] += 1
        max_fiber_size = max(max_fiber_size, size)
        max_quotient_budget = max(max_quotient_budget, quotient_budget)
        max_active_quotient_budget = max(
            max_active_quotient_budget,
            active_quotient_budget,
        )
        mobius_ok = mobius_ok and bool(ledger["mobius_inversion_ok"])
        if primitive > max_primitive:
            max_primitive = primitive
            primitive_examples = []
        if primitive == max_primitive and len(primitive_examples) < max_examples:
            primitive_examples.append({
                "top_sigma_key": list(key),
                "fiber_size": size,
                "primitive": primitive,
                "quotient_budget": quotient_budget,
                "active_quotient_budget": active_quotient_budget,
                "exact_stabilizer_counts": {
                    str(order): count for order, count in exact.items() if count
                },
                "members_sample_exponents": [
                    mask_to_exponents(mask, n) for mask in members[:max_examples]
                ],
            })

    total = comb(n, m)
    entropy_target = log2_binom(n, a)
    entropy_bits = sigma * log2(p)
    entropy_margin_bits = entropy_bits - (1.0 + epsilon) * entropy_target
    entropy_ratio = float("inf") if entropy_target == 0 else (
        entropy_bits / entropy_target
    )
    reserve_cleared = entropy_margin_bits >= -1e-12
    alert_threshold = n ** alert_power
    primitive_alert = reserve_cleared and max_primitive > alert_threshold

    return {
        "status": "EXPERIMENTAL/CONJECTURE_FALSIFICATION_SCAN",
        "params": {
            "p": p,
            "n": n,
            "k": k,
            "sigma": sigma,
            "a": a,
            "m": m,
            "epsilon": epsilon,
        },
        "total_divisors": total,
        "distinct_prefix_values": len(buckets),
        "fiber_size_histogram": dict(sorted(fiber_histogram.items())),
        "primitive_count_histogram": dict(sorted(primitive_histogram.items())),
        "quotient_budget_histogram": dict(sorted(quotient_histogram.items())),
        "max_fiber_size": max_fiber_size,
        "max_primitive_exact": max_primitive,
        "max_quotient_budget": max_quotient_budget,
        "max_active_quotient_budget": max_active_quotient_budget,
        "active_orders_gt_sigma": active_orders,
        "mobius_inversion_ok": mobius_ok,
        "entropy_bits": round(entropy_bits, 6),
        "entropy_target_bits": round(entropy_target, 6),
        "entropy_margin_bits": round(entropy_margin_bits, 6),
        "entropy_ratio": None if entropy_ratio == float("inf") else (
            round(entropy_ratio, 6)
        ),
        "reserve_cleared": reserve_cleared,
        "primitive_alert_threshold": round(alert_threshold, 6),
        "primitive_alert": primitive_alert,
        "max_primitive_examples": primitive_examples,
    }


def default_cases(max_m: int) -> list[tuple[int, int, int, int]]:
    cases: list[tuple[int, int, int, int]] = []
    for p in (17, 97):
        n = 16
        for k in range(4, 9):
            for sigma in range(1, 7):
                m = n - (k + sigma)
                if 0 <= m <= max_m:
                    cases.append((p, n, k, sigma))
    return cases


def parse_case(raw: str) -> tuple[int, int, int, int]:
    parts = [int(part.strip()) for part in raw.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("--case must have form p,n,k,sigma")
    return parts[0], parts[1], parts[2], parts[3]


def print_human(results: list[dict[str, object]]) -> None:
    header = "p   n   k  sig  m   reserve  margin    maxF  maxQ1  maxQB  alert"
    print(header)
    print("-" * len(header))
    for result in results:
        params = result["params"]
        assert isinstance(params, dict)
        print(
            f"{params['p']:<3} {params['n']:<3} {params['k']:<2} "
            f"{params['sigma']:<4} {params['m']:<3} "
            f"{str(result['reserve_cleared']):<7} "
            f"{result['entropy_margin_bits']:>7} "
            f"{result['max_fiber_size']:>6} "
            f"{result['max_primitive_exact']:>6} "
            f"{result['max_quotient_budget']:>6} "
            f"{str(result['primitive_alert']):<5}"
        )

    reserve_rows = [result for result in results if result["reserve_cleared"]]
    below_rows = [result for result in results if not result["reserve_cleared"]]
    alerts = [result for result in reserve_rows if result["primitive_alert"]]
    max_reserve = max(
        (int(result["max_primitive_exact"]) for result in reserve_rows),
        default=0,
    )
    max_below = max(
        (int(result["max_primitive_exact"]) for result in below_rows),
        default=0,
    )
    print()
    print(f"reserve-cleared rows: {len(reserve_rows)}")
    print(f"reserve-cleared primitive alerts: {len(alerts)}")
    print(f"max primitive in reserve-cleared rows: {max_reserve}")
    print(f"max primitive below reserve: {max_below}")
    if alerts:
        print("alert rows:")
        for result in alerts:
            params = result["params"]
            assert isinstance(params, dict)
            print(
                f"  p={params['p']} n={params['n']} k={params['k']} "
                f"sigma={params['sigma']} maxQ1={result['max_primitive_exact']}"
            )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        type=parse_case,
        help="scan one case p,n,k,sigma; may be repeated",
    )
    parser.add_argument(
        "--max-m",
        type=int,
        default=8,
        help="default-suite maximum complement size",
    )
    parser.add_argument(
        "--epsilon",
        type=float,
        default=0.0,
        help="entropy reserve slack in sigma log2(p) >= (1+epsilon) log2 binom(n,a)",
    )
    parser.add_argument(
        "--alert-power",
        type=float,
        default=1.0,
        help="heuristic primitive alert threshold n^alert_power",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        default=2,
        help="number of max-primitive example fibers to retain",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    cases = args.case if args.case else default_cases(args.max_m)
    results = [
        scan_case(p, n, k, sigma, args.epsilon, args.alert_power, args.max_examples)
        for p, n, k, sigma in cases
    ]
    if args.json:
        print(json.dumps({"results": results}, indent=2, sort_keys=True))
    else:
        print_human(results)
    return 1 if any(result["primitive_alert"] for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
