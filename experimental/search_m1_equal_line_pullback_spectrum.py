#!/usr/bin/env python3
"""Scan the full character spectrum of the M1 equal-line pullback target."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import asdict, dataclass
from typing import Iterable, List

import numpy as np


@dataclass
class SpectrumCase:
    p: int
    character_count: int
    violation_count: int
    violation_domain_ge_counts: dict[str, int]
    violation_max_domain_size: int
    near_295_count: int
    near_295_domain_ge_counts: dict[str, int]
    near_295_max_domain_size: int
    best_ratio_to_p: float
    best_abs: float
    best_exponent: int
    best_order: int
    best_max_domain_size: int
    m1_grid_tuple_count: int
    m1_grid_violation_count: int
    m1_grid_near_295_count: int
    m1_grid_best_ratio_to_p: float
    m1_grid_best_abs: float
    m1_grid_best_exponent: int
    m1_grid_best_order: int
    diagonal_tuple_count: int
    diagonal_violation_count: int
    diagonal_near_295_count: int
    diagonal_best_ratio_to_p: float
    diagonal_best_abs: float
    diagonal_best_exponent: int
    diagonal_best_order: int
    elapsed_seconds: float


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def primes_up_to(limit: int) -> Iterable[int]:
    for value in range(5, limit + 1):
        if is_prime(value):
            yield value


def prime_factors(value: int) -> List[int]:
    factors: List[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def divisors(value: int) -> List[int]:
    result: List[int] = []
    for divisor in range(1, int(math.sqrt(value)) + 1):
        if value % divisor == 0:
            result.append(divisor)
            if divisor * divisor != value:
                result.append(value // divisor)
    return sorted(result)


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def log_table(p: int) -> np.ndarray:
    root = primitive_root(p)
    table = np.zeros(p, dtype=np.int64)
    value = 1
    for exponent in range(p - 1):
        table[value] = exponent
        value = (value * root) % p
    return table


def quadratic_table(p: int) -> np.ndarray:
    table = -np.ones(p, dtype=np.int8)
    table[0] = 0
    residues = (np.arange(1, p, dtype=np.int64) ** 2) % p
    table[residues] = 1
    return table


def shape_b(s: int, p: int) -> int:
    return (s * s + s + 1) % p


def shape_d(s: int, x: int, p: int) -> int:
    return (4 * shape_b(s, p) * x - s * s) % p


def pullback_histogram(p: int, logs: np.ndarray, quadratic: np.ndarray) -> np.ndarray:
    """Return additive log histogram for the single-character pullback sum.

    The normalized main term is

        chi_2(-1) sum_{s!=-1,B(s)!=0} sum_x
          alpha(B(s)) alpha^(-2)(x) alpha^3(x-1)
          chi_2(4B(s)x-s^2).

    For fixed `p`, every nonzero Kummer factor contributes only through the
    exponent

        log B(s) - 2 log x + 3 log(x-1) mod p-1.

    A single FFT of this histogram therefore gives the value for every
    multiplicative character `alpha` of `F_p^*` at once.
    """
    order = p - 1
    values = np.arange(p, dtype=np.int64)
    x_mask = (values != 0) & (values != 1)
    x_values = values[x_mask]
    x_exponents = (-2 * logs[x_values] + 3 * logs[(x_values - 1) % p]) % order
    histogram = np.zeros(order, dtype=np.float64)

    for s in range(p):
        if s == p - 1:
            continue
        b_value = shape_b(s, p)
        if b_value == 0:
            continue
        d_values = (4 * b_value * x_values - s * s) % p
        exponents = (logs[b_value] + x_exponents) % order
        histogram += np.bincount(
            exponents,
            weights=quadratic[d_values].astype(np.float64),
            minlength=order,
        )
    return histogram


def direct_pullback_value(
    p: int,
    exponent: int,
    logs: np.ndarray,
    quadratic: np.ndarray,
) -> complex:
    order = p - 1
    zeta = np.exp(2j * np.pi / order)

    def alpha(value: int) -> complex:
        value %= p
        if value == 0:
            return 0j
        return zeta ** ((exponent * int(logs[value])) % order)

    total = 0j
    for s in range(p):
        if s == p - 1:
            continue
        b_value = shape_b(s, p)
        if b_value == 0:
            continue
        alpha_b = alpha(b_value)
        for x in range(p):
            total += (
                alpha_b
                * alpha(x).conjugate()
                * alpha(x).conjugate()
                * alpha(x - 1)
                * alpha(x - 1)
                * alpha(x - 1)
                * int(quadratic[shape_d(s, x, p)])
            )
    return int(quadratic[p - 1]) * total


def spectrum_values(p: int, histogram: np.ndarray, quadratic: np.ndarray) -> np.ndarray:
    return int(quadratic[p - 1]) * np.fft.ifft(histogram) * (p - 1)


def character_order(group_order: int, exponent: int) -> int:
    return group_order // math.gcd(group_order, exponent)


def max_equal_line_domain_size(group_order: int, exponent: int) -> int:
    order = character_order(group_order, exponent)
    if order <= 3:
        return 0
    if order % 2 == 0:
        return 2 * group_order // order
    return group_order // order


def domain_size_array(group_order: int) -> np.ndarray:
    return np.array(
        [
            max_equal_line_domain_size(group_order, exponent)
            for exponent in range(group_order)
        ],
        dtype=np.int64,
    )


def equal_line_tuple_exponents(p: int, e: int) -> List[int]:
    """Return full character-group exponents from equal-line M1 tuples."""
    if (p - 1) % e != 0:
        return []
    n = (p - 1) // e
    h = e * math.gcd(2, n)
    lift = h // e
    scale = (p - 1) // h
    exponents: List[int] = []
    for a in range(1, e):
        line_exponent = (lift * a) % h
        for d in range(1, h):
            if (3 * line_exponent + 2 * d) % h != 0:
                continue
            alpha_exponent = (line_exponent + d) % h
            if alpha_exponent == 0:
                continue
            if h % 2 == 0 and alpha_exponent == h // 2:
                continue
            exponents.append((alpha_exponent * scale) % (p - 1))
    return exponents


def tuple_exponents_for_grid(p: int, max_character_order: int) -> List[int]:
    exponents: List[int] = []
    for e in range(2, max_character_order + 1):
        exponents.extend(equal_line_tuple_exponents(p, e))
    return exponents


def tuple_exponents_for_diagonal(p: int, n: int) -> List[int]:
    if (p - 1) % n != 0:
        return []
    return equal_line_tuple_exponents(p, (p - 1) // n)


def summarize_exponents(
    p: int,
    magnitudes: np.ndarray,
    exponents: List[int],
    tolerance: float,
) -> dict[str, object]:
    if not exponents:
        return {
            "tuple_count": 0,
            "violation_count": 0,
            "near_295_count": 0,
            "best_ratio_to_p": 0.0,
            "best_abs": 0.0,
            "best_exponent": 0,
            "best_order": 0,
        }
    exponent_array = np.array(exponents, dtype=np.int64)
    selected = magnitudes[exponent_array]
    best_index = int(np.argmax(selected))
    best_exponent = int(exponent_array[best_index])
    best_abs = float(selected[best_index])
    return {
        "tuple_count": len(exponents),
        "violation_count": int(np.count_nonzero(selected > 3 * p + tolerance)),
        "near_295_count": int(np.count_nonzero(selected > 2.95 * p)),
        "best_ratio_to_p": round(best_abs / p, 10),
        "best_abs": round(best_abs, 10),
        "best_exponent": best_exponent,
        "best_order": (p - 1) // math.gcd(p - 1, best_exponent),
    }


def validate_spectrum(p: int) -> None:
    logs = log_table(p)
    quadratic = quadratic_table(p)
    histogram = pullback_histogram(p, logs, quadratic)
    spectrum = spectrum_values(p, histogram, quadratic)
    exponents = [1, 2, max(1, (p - 1) // 3), p - 2]
    for exponent in sorted(set(exponents)):
        direct = direct_pullback_value(p, exponent, logs, quadratic)
        error = abs(direct - spectrum[exponent])
        if error > 1e-8 * max(1, p):
            raise AssertionError((p, exponent, direct, spectrum[exponent], error))


def validate_equal_line_domain_filter(p: int) -> None:
    group_order = p - 1
    appearances: dict[int, List[int]] = {}
    for n in divisors(group_order):
        e = group_order // n
        if e < 2:
            continue
        h = e * math.gcd(2, n)
        enumerated = set(equal_line_tuple_exponents(p, e))
        expected = {
            exponent
            for exponent in range(1, group_order)
            if character_order(group_order, exponent) > 3
            and h % character_order(group_order, exponent) == 0
        }
        if enumerated != expected:
            raise AssertionError((p, n, e, sorted(enumerated ^ expected)[:10]))
        for exponent in enumerated:
            appearances.setdefault(exponent, []).append(n)
    for exponent in range(1, group_order):
        actual = max(appearances.get(exponent, [0]))
        expected = max_equal_line_domain_size(group_order, exponent)
        if actual != expected:
            raise AssertionError((p, exponent, actual, expected))


def threshold_counts(
    mask: np.ndarray,
    domain_sizes: np.ndarray,
    thresholds: List[int],
) -> dict[str, int]:
    return {
        str(threshold): int(np.count_nonzero(mask & (domain_sizes >= threshold)))
        for threshold in thresholds
    }


def scan_prime(
    p: int,
    tolerance: float,
    m1_max_character_order: int,
    diagonal_n: int,
    domain_thresholds: List[int],
) -> SpectrumCase:
    start = time.monotonic()
    logs = log_table(p)
    quadratic = quadratic_table(p)
    histogram = pullback_histogram(p, logs, quadratic)
    spectrum = spectrum_values(p, histogram, quadratic)
    magnitudes = np.abs(spectrum)

    active = np.ones(p - 1, dtype=bool)
    active[0] = False
    active[(p - 1) // 2] = False
    active_magnitudes = np.where(active, magnitudes, -1.0)
    best_exponent = int(np.argmax(active_magnitudes))
    best_abs = float(magnitudes[best_exponent])
    character_count = int(np.count_nonzero(active))
    domain_sizes = domain_size_array(p - 1)
    violation_mask = (magnitudes > 3 * p + tolerance) & active
    near_295_mask = (magnitudes > 2.95 * p) & active
    m1_grid = summarize_exponents(
        p,
        magnitudes,
        tuple_exponents_for_grid(p, m1_max_character_order),
        tolerance,
    )
    diagonal = summarize_exponents(
        p,
        magnitudes,
        tuple_exponents_for_diagonal(p, diagonal_n),
        tolerance,
    )

    return SpectrumCase(
        p=p,
        character_count=character_count,
        violation_count=int(np.count_nonzero(violation_mask)),
        violation_domain_ge_counts=threshold_counts(
            violation_mask,
            domain_sizes,
            domain_thresholds,
        ),
        violation_max_domain_size=int(
            np.max(domain_sizes[violation_mask]) if np.any(violation_mask) else 0
        ),
        near_295_count=int(np.count_nonzero(near_295_mask)),
        near_295_domain_ge_counts=threshold_counts(
            near_295_mask,
            domain_sizes,
            domain_thresholds,
        ),
        near_295_max_domain_size=int(
            np.max(domain_sizes[near_295_mask]) if np.any(near_295_mask) else 0
        ),
        best_ratio_to_p=round(best_abs / p, 10),
        best_abs=round(best_abs, 10),
        best_exponent=best_exponent,
        best_order=(p - 1) // math.gcd(p - 1, best_exponent),
        best_max_domain_size=int(domain_sizes[best_exponent]),
        m1_grid_tuple_count=int(m1_grid["tuple_count"]),
        m1_grid_violation_count=int(m1_grid["violation_count"]),
        m1_grid_near_295_count=int(m1_grid["near_295_count"]),
        m1_grid_best_ratio_to_p=float(m1_grid["best_ratio_to_p"]),
        m1_grid_best_abs=float(m1_grid["best_abs"]),
        m1_grid_best_exponent=int(m1_grid["best_exponent"]),
        m1_grid_best_order=int(m1_grid["best_order"]),
        diagonal_tuple_count=int(diagonal["tuple_count"]),
        diagonal_violation_count=int(diagonal["violation_count"]),
        diagonal_near_295_count=int(diagonal["near_295_count"]),
        diagonal_best_ratio_to_p=float(diagonal["best_ratio_to_p"]),
        diagonal_best_abs=float(diagonal["best_abs"]),
        diagonal_best_exponent=int(diagonal["best_exponent"]),
        diagonal_best_order=int(diagonal["best_order"]),
        elapsed_seconds=round(time.monotonic() - start, 4),
    )


def scan_primes(
    prime_limit: int,
    tolerance: float,
    m1_max_character_order: int,
    diagonal_n: int,
    domain_thresholds: List[int],
) -> List[SpectrumCase]:
    return [
        scan_prime(
            p,
            tolerance,
            m1_max_character_order,
            diagonal_n,
            domain_thresholds,
        )
        for p in primes_up_to(prime_limit)
    ]


def top_rows(rows: List[SpectrumCase], top_count: int) -> List[dict[str, object]]:
    return [
        asdict(row)
        for row in sorted(
            rows,
            key=lambda item: item.best_ratio_to_p,
            reverse=True,
        )[:top_count]
    ]


def sum_count_dicts(rows: List[dict[str, int]]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for row in rows:
        for key, value in row.items():
            totals[key] = totals.get(key, 0) + value
    return totals


def summarize(rows: List[SpectrumCase], top_count: int) -> dict[str, object]:
    return {
        "prime_count": len(rows),
        "character_count": sum(row.character_count for row in rows),
        "violation_count": sum(row.violation_count for row in rows),
        "violation_domain_ge_counts": sum_count_dicts(
            [row.violation_domain_ge_counts for row in rows]
        ),
        "violation_max_domain_size": max(
            (row.violation_max_domain_size for row in rows),
            default=0,
        ),
        "near_295_count": sum(row.near_295_count for row in rows),
        "near_295_domain_ge_counts": sum_count_dicts(
            [row.near_295_domain_ge_counts for row in rows]
        ),
        "near_295_max_domain_size": max(
            (row.near_295_max_domain_size for row in rows),
            default=0,
        ),
        "top": top_rows(rows, top_count),
        "m1_grid_case_count": sum(row.m1_grid_tuple_count > 0 for row in rows),
        "m1_grid_tuple_count": sum(row.m1_grid_tuple_count for row in rows),
        "m1_grid_violation_count": sum(
            row.m1_grid_violation_count for row in rows
        ),
        "m1_grid_near_295_count": sum(row.m1_grid_near_295_count for row in rows),
        "m1_grid_top": [
            asdict(row)
            for row in sorted(
                (row for row in rows if row.m1_grid_tuple_count),
                key=lambda item: item.m1_grid_best_ratio_to_p,
                reverse=True,
            )[:top_count]
        ],
        "diagonal_case_count": sum(row.diagonal_tuple_count > 0 for row in rows),
        "diagonal_tuple_count": sum(row.diagonal_tuple_count for row in rows),
        "diagonal_violation_count": sum(row.diagonal_violation_count for row in rows),
        "diagonal_near_295_count": sum(row.diagonal_near_295_count for row in rows),
        "diagonal_top": [
            asdict(row)
            for row in sorted(
                (row for row in rows if row.diagonal_tuple_count),
                key=lambda item: item.diagonal_best_ratio_to_p,
                reverse=True,
            )[:top_count]
        ],
    }


def print_text_report(summary: dict[str, object]) -> None:
    print("M1 equal-line pullback character-spectrum scan")
    print(
        "grid:",
        f"primes={summary['prime_count']}",
        f"characters={summary['character_count']}",
        f"violations={summary['violation_count']}",
        f"near_2.95p={summary['near_295_count']}",
    )
    print(
        "violation n_max thresholds:",
        " ".join(
            f">={key}:{value}"
            for key, value in summary["violation_domain_ge_counts"].items()
        ),
        f"max={summary['violation_max_domain_size']}",
    )
    print(
        "near_2.95p n_max thresholds:",
        " ".join(
            f">={key}:{value}"
            for key, value in summary["near_295_domain_ge_counts"].items()
        ),
        f"max={summary['near_295_max_domain_size']}",
    )
    print("top results:")
    for row in summary["top"]:
        print(
            "  "
            f"ratio={row['best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"exponent={row['best_exponent']}",
            f"order={row['best_order']}",
            f"n_max={row['best_max_domain_size']}",
            f"violations={row['violation_count']}",
            f"near_2.95p={row['near_295_count']}",
        )
    print(
        "M1 equal-line grid:",
        f"cases={summary['m1_grid_case_count']}",
        f"tuples={summary['m1_grid_tuple_count']}",
        f"violations={summary['m1_grid_violation_count']}",
        f"near_2.95p={summary['m1_grid_near_295_count']}",
    )
    for row in summary["m1_grid_top"]:
        print(
            "  "
            f"ratio={row['m1_grid_best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"exponent={row['m1_grid_best_exponent']}",
            f"order={row['m1_grid_best_order']}",
            f"tuples={row['m1_grid_tuple_count']}",
        )
    print(
        "M1 diagonal:",
        f"cases={summary['diagonal_case_count']}",
        f"tuples={summary['diagonal_tuple_count']}",
        f"violations={summary['diagonal_violation_count']}",
        f"near_2.95p={summary['diagonal_near_295_count']}",
    )
    for row in summary["diagonal_top"]:
        print(
            "  "
            f"ratio={row['diagonal_best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"exponent={row['diagonal_best_exponent']}",
            f"order={row['diagonal_best_order']}",
            f"tuples={row['diagonal_tuple_count']}",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("smoke", "report"), default="smoke")
    parser.add_argument("--prime-limit", type=int, default=None)
    parser.add_argument("--m1-max-character-order", type=int, default=None)
    parser.add_argument("--diagonal-n", type=int, default=None)
    parser.add_argument("--domain-thresholds", default="4,6,8,12,16,20,32")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--tolerance", type=float, default=1e-7)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="compare the FFT spectrum against direct sums for small primes",
    )
    return parser.parse_args()


def parse_domain_thresholds(raw: str) -> List[int]:
    thresholds = [int(part) for part in raw.split(",") if part.strip()]
    if any(threshold <= 0 for threshold in thresholds):
        raise ValueError(raw)
    return sorted(set(thresholds))


def fill_preset(args: argparse.Namespace) -> argparse.Namespace:
    defaults = {
        "report": {
            "prime_limit": 1601,
            "m1_max_character_order": 24,
            "diagonal_n": 20,
        },
        "smoke": {
            "prime_limit": 199,
            "m1_max_character_order": 18,
            "diagonal_n": 20,
        },
    }
    if args.prime_limit is None:
        args.prime_limit = defaults[args.preset]["prime_limit"]
    if args.m1_max_character_order is None:
        args.m1_max_character_order = defaults[args.preset][
            "m1_max_character_order"
        ]
    if args.diagonal_n is None:
        args.diagonal_n = defaults[args.preset]["diagonal_n"]
    return args


def main() -> None:
    args = fill_preset(parse_args())
    if args.validate:
        for p in (5, 7, 11, 17, 29):
            validate_spectrum(p)
            validate_equal_line_domain_filter(p)
    domain_thresholds = parse_domain_thresholds(str(args.domain_thresholds))
    rows = scan_primes(
        int(args.prime_limit),
        float(args.tolerance),
        int(args.m1_max_character_order),
        int(args.diagonal_n),
        domain_thresholds,
    )
    summary = summarize(rows, int(args.top))
    summary["parameters"] = {
        "preset": args.preset,
        "prime_limit": args.prime_limit,
        "top": args.top,
        "tolerance": args.tolerance,
        "m1_max_character_order": args.m1_max_character_order,
        "diagonal_n": args.diagonal_n,
        "domain_thresholds": domain_thresholds,
        "validated": bool(args.validate),
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_text_report(summary)


if __name__ == "__main__":
    main()
