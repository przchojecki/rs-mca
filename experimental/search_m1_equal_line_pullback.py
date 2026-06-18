#!/usr/bin/env python3
"""Stress scan the M1 equal-line single-character pullback target."""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import asdict, dataclass
from typing import Iterable, List, Tuple

import numpy as np


Tuple4 = Tuple[int, int, int, int]


@dataclass
class PullbackCase:
    p: int
    n: int
    e: int
    h: int
    tuple_count: int
    violation_count: int
    best_ratio_to_p: float
    best_abs: float
    best_tuple: Tuple4
    best_alpha_exponent: int
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


def character_table(p: int, order: int, logs: np.ndarray) -> np.ndarray:
    table = np.zeros((order, p), dtype=np.complex128)
    for exponent in range(order):
        table[exponent, 1:] = np.exp(
            2j * np.pi * exponent * logs[1:] / order
        )
    return table


def quadratic_character_array(values: np.ndarray, p: int) -> np.ndarray:
    result = np.zeros(values.shape, dtype=np.float64)
    flat_values = (values.ravel() % p).astype(np.int64)
    flat_result = result.ravel()
    for index, value in enumerate(flat_values):
        if value == 0:
            continue
        flat_result[index] = 1.0 if pow(int(value), (p - 1) // 2, p) == 1 else -1.0
    return result


def scan_case(
    p: int,
    e: int,
    tolerance: float,
) -> PullbackCase:
    start = time.monotonic()
    n = (p - 1) // e
    h = e * math.gcd(2, n)
    lift = h // e
    logs = log_table(p)
    characters = character_table(p, h, logs)
    values = np.arange(p, dtype=np.int64)
    s_values, x_values = np.meshgrid(values, values, indexing="ij")
    b_values = (values * values + values + 1) % p
    d_values = (4 * ((s_values * s_values + s_values + 1) % p) * x_values)
    d_values -= s_values * s_values
    d_values %= p
    quadratic = quadratic_character_array(d_values, p)
    s_open_mask = values != p - 1
    chi_minus_one = 1.0 if p % 4 == 1 else -1.0

    best_abs = -1.0
    best_tuple = (0, 0, 0, 0)
    best_alpha_exponent = 0
    tuple_count = 0
    violation_count = 0

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
            tuple_count += 1
            alpha_b = characters[alpha_exponent, b_values] * s_open_mask
            alpha_x = (
                characters[(-2 * alpha_exponent) % h, values]
                * characters[(3 * alpha_exponent) % h, (values - 1) % p]
            )
            value = chi_minus_one * np.sum(
                alpha_b[:, None] * alpha_x[None, :] * quadratic
            )
            magnitude = float(abs(value))
            if magnitude > 3 * p + tolerance:
                violation_count += 1
            if magnitude > best_abs:
                best_abs = magnitude
                best_tuple = (a, a, 0, d)
                best_alpha_exponent = alpha_exponent

    return PullbackCase(
        p=p,
        n=n,
        e=e,
        h=h,
        tuple_count=tuple_count,
        violation_count=violation_count,
        best_ratio_to_p=round(best_abs / p, 10),
        best_abs=round(best_abs, 10),
        best_tuple=best_tuple,
        best_alpha_exponent=best_alpha_exponent,
        elapsed_seconds=round(time.monotonic() - start, 4),
    )


def scan_grid(
    prime_limit: int,
    max_character_order: int,
    tolerance: float,
) -> List[PullbackCase]:
    rows: List[PullbackCase] = []
    for p in primes_up_to(prime_limit):
        for e in range(2, max_character_order + 1):
            if (p - 1) % e != 0:
                continue
            rows.append(scan_case(p, e, tolerance))
    return rows


def top_rows(rows: List[PullbackCase], top_count: int) -> List[dict[str, object]]:
    return [
        asdict(row)
        for row in sorted(
            rows,
            key=lambda item: item.best_ratio_to_p,
            reverse=True,
        )[:top_count]
    ]


def summarize(rows: List[PullbackCase], top_count: int) -> dict[str, object]:
    return {
        "case_count": len(rows),
        "tuple_count": sum(row.tuple_count for row in rows),
        "violation_count": sum(row.violation_count for row in rows),
        "top": top_rows(rows, top_count),
    }


def print_text_report(summary: dict[str, object]) -> None:
    print("M1 equal-line pullback scan")
    print(
        "grid:",
        f"cases={summary['case_count']}",
        f"tuples={summary['tuple_count']}",
        f"violations={summary['violation_count']}",
    )
    print("top results:")
    for row in summary["top"]:
        print(
            "  "
            f"ratio={row['best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"n={row['n']}",
            f"e={row['e']}",
            f"h={row['h']}",
            f"tuple={tuple(row['best_tuple'])}",
            f"alpha={row['best_alpha_exponent']}",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("smoke", "report"), default="smoke")
    parser.add_argument("--prime-limit", type=int, default=None)
    parser.add_argument("--max-character-order", type=int, default=None)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--tolerance", type=float, default=1e-7)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    return parser.parse_args()


def fill_preset(args: argparse.Namespace) -> argparse.Namespace:
    if args.preset == "report":
        defaults = {"prime_limit": 500, "max_character_order": 24}
    else:
        defaults = {"prime_limit": 199, "max_character_order": 18}
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    return args


def main() -> None:
    args = fill_preset(parse_args())
    rows = scan_grid(
        prime_limit=int(args.prime_limit),
        max_character_order=int(args.max_character_order),
        tolerance=float(args.tolerance),
    )
    summary = summarize(rows, int(args.top))
    summary["parameters"] = {
        "preset": args.preset,
        "prime_limit": args.prime_limit,
        "max_character_order": args.max_character_order,
        "top": args.top,
        "tolerance": args.tolerance,
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_text_report(summary)


if __name__ == "__main__":
    main()
