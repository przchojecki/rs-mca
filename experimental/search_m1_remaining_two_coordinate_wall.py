#!/usr/bin/env python3
"""Targeted scans for the remaining M1 two-coordinate Kummer wall.

The scan is intentionally restricted to the canonical active pair
`(a,b,c)=(a,b,0)`.  The other two active pairs are equivalent by the symmetry
of `A=uv+uw+vw-1` on `u+v+w=-1`.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import asdict, dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np


Tuple4 = Tuple[int, int, int, int]


@dataclass
class CaseResult:
    mode: str
    p: int
    n: int
    e: int
    h: int
    scanned_tuple_count: int
    best_abs: float
    best_ratio_to_p: float
    best_tuple: Tuple4
    best_line_monodromies: Tuple[int, int, int]
    best_projective_equal_pair: bool
    best_equal_line_monodromy: bool
    best_line_conic_resonant: bool
    violation_count: int
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


def field_arrays(p: int) -> Tuple[np.ndarray, np.ndarray]:
    values = np.arange(p, dtype=np.int64)
    u_values, v_values = np.meshgrid(values, values, indexing="ij")
    conic_values = -(
        u_values * u_values
        + v_values * v_values
        + u_values * v_values
        + u_values
        + v_values
        + 1
    )
    conic_values %= p
    principal_coordinate_open = ((-1 - u_values - v_values) % p) != 0
    return conic_values, principal_coordinate_open


def line_monodromies(e: int, h: int, a: int, b: int, d: int) -> Tuple[int, int, int]:
    lift = h // e
    first = (lift * a) % h
    second = (lift * b) % h
    infinity = (-(first + second + 2 * d)) % h
    return first, second, infinity


def projective_class(e: int, h: int, a: int, b: int, d: int) -> str:
    first, second, infinity = line_monodromies(e, h, a, b, d)
    if infinity == 0:
        return "infinity_unramified"
    if (
        (first + second) % h == 0
        or (first + infinity) % h == 0
        or (second + infinity) % h == 0
    ):
        return "projective_reciprocal"
    return "ramified_nonreciprocal"


def has_projective_equal_pair(monodromies: Tuple[int, int, int]) -> bool:
    first, second, infinity = monodromies
    return first == second or first == infinity or second == infinity


def has_line_conic_resonance(
    monodromies: Tuple[int, int, int],
    conic_exponent: int,
    character_order: int,
) -> bool:
    return any(
        (line_exponent + conic_exponent) % character_order == 0
        for line_exponent in monodromies
    )


def scan_case(
    p: int,
    e: int,
    logs: np.ndarray,
    conic_values: np.ndarray,
    principal_coordinate_open: np.ndarray,
    diagonal_only: bool,
    asymmetric_only: bool,
    nonresonant_only: bool,
    resonant_only: bool,
    tolerance: float,
) -> CaseResult:
    n = (p - 1) // e
    h = e * math.gcd(2, n)
    chi = character_table(p, e, logs)
    psi = character_table(p, h, logs)
    active_characters = chi[1:e]

    best_abs = -1.0
    best_tuple = (0, 0, 0, 0)
    scanned_tuple_count = 0
    violation_count = 0
    start = time.monotonic()

    for d in range(1, h):
        weight_matrix = psi[d, conic_values] * principal_coordinate_open
        if diagonal_only:
            values = np.einsum(
                "ai,ij,aj->a",
                active_characters,
                weight_matrix,
                active_characters,
                optimize=True,
            )
            candidates = ((index, index, value) for index, value in enumerate(values))
        else:
            values = active_characters @ weight_matrix @ active_characters.T
            candidates = (
                (a_index, b_index, values[a_index, b_index])
                for a_index in range(e - 1)
                for b_index in range(e - 1)
            )
        for a_index, b_index, value in candidates:
            a = a_index + 1
            b = b_index + 1
            if projective_class(e, h, a, b, d) != "ramified_nonreciprocal":
                continue
            monodromies = line_monodromies(e, h, a, b, d)
            if asymmetric_only and has_projective_equal_pair(monodromies):
                continue
            line_conic_resonant = has_line_conic_resonance(monodromies, d, h)
            if nonresonant_only and line_conic_resonant:
                continue
            if resonant_only and not line_conic_resonant:
                continue
            scanned_tuple_count += 1
            magnitude = float(abs(value))
            if magnitude > 4 * p + tolerance:
                violation_count += 1
            if magnitude > best_abs:
                best_abs = magnitude
                best_tuple = (a, b, 0, d)

    if scanned_tuple_count:
        monodromies = line_monodromies(
            e,
            h,
            best_tuple[0],
            best_tuple[1],
            best_tuple[3],
        )
    else:
        best_abs = 0.0
        monodromies = (0, 0, 0)
    best_line_conic_resonant = (
        False
        if not scanned_tuple_count
        else has_line_conic_resonance(monodromies, best_tuple[3], h)
    )
    return CaseResult(
        mode=(
            "diagonal"
            if diagonal_only
            else (
                "asymmetric_line_conic_resonant_wall"
                if resonant_only
                else (
                    "asymmetric_nonresonant_wall"
                    if nonresonant_only
                    else "asymmetric_wall" if asymmetric_only else "remaining_wall"
                )
            )
        ),
        p=p,
        n=n,
        e=e,
        h=h,
        scanned_tuple_count=scanned_tuple_count,
        best_abs=round(best_abs, 10),
        best_ratio_to_p=round(best_abs / p, 10),
        best_tuple=best_tuple,
        best_line_monodromies=monodromies,
        best_projective_equal_pair=has_projective_equal_pair(monodromies),
        best_equal_line_monodromy=(monodromies[0] == monodromies[1] == monodromies[2]),
        best_line_conic_resonant=best_line_conic_resonant,
        violation_count=violation_count,
        elapsed_seconds=round(time.monotonic() - start, 4),
    )


def scan_grid(
    prime_limit: int,
    max_character_order: int,
    asymmetric_only: bool,
    nonresonant_only: bool,
    resonant_only: bool,
    tolerance: float,
) -> List[CaseResult]:
    results: List[CaseResult] = []
    for p in primes_up_to(prime_limit):
        logs = log_table(p)
        conic_values, principal_coordinate_open = field_arrays(p)
        for e in range(2, max_character_order + 1):
            if (p - 1) % e != 0:
                continue
            results.append(
                scan_case(
                    p,
                    e,
                    logs,
                    conic_values,
                    principal_coordinate_open,
                    diagonal_only=False,
                    asymmetric_only=asymmetric_only,
                    nonresonant_only=nonresonant_only,
                    resonant_only=resonant_only,
                    tolerance=tolerance,
                )
            )
    return results


def scan_diagonal_family(
    n: int,
    prime_limit: int,
    tolerance: float,
) -> List[CaseResult]:
    results: List[CaseResult] = []
    for p in primes_up_to(prime_limit):
        if (p - 1) % n != 0:
            continue
        e = (p - 1) // n
        if e < 2:
            continue
        logs = log_table(p)
        conic_values, principal_coordinate_open = field_arrays(p)
        results.append(
            scan_case(
                p,
                e,
                logs,
                conic_values,
                principal_coordinate_open,
                diagonal_only=True,
                asymmetric_only=False,
                nonresonant_only=False,
                resonant_only=False,
                tolerance=tolerance,
            )
        )
    return results


def top_results(results: List[CaseResult], top_count: int) -> List[Dict[str, object]]:
    return [
        asdict(result)
        for result in sorted(
            results,
            key=lambda item: item.best_ratio_to_p,
            reverse=True,
        )[:top_count]
    ]


def summarize_results(
    grid_results: List[CaseResult],
    asymmetric_results: List[CaseResult],
    nonresonant_results: List[CaseResult],
    resonant_results: List[CaseResult],
    diagonal_results: List[CaseResult],
    top_count: int,
) -> Dict[str, object]:
    all_results = grid_results + diagonal_results
    return {
        "grid_case_count": len(grid_results),
        "grid_scanned_tuple_count": sum(
            result.scanned_tuple_count for result in grid_results
        ),
        "grid_violation_count": sum(result.violation_count for result in grid_results),
        "grid_top": top_results(grid_results, top_count),
        "asymmetric_case_count": len(asymmetric_results),
        "asymmetric_scanned_tuple_count": sum(
            result.scanned_tuple_count for result in asymmetric_results
        ),
        "asymmetric_violation_count": sum(
            result.violation_count for result in asymmetric_results
        ),
        "asymmetric_top": top_results(asymmetric_results, top_count),
        "nonresonant_case_count": len(nonresonant_results),
        "nonresonant_scanned_tuple_count": sum(
            result.scanned_tuple_count for result in nonresonant_results
        ),
        "nonresonant_violation_count": sum(
            result.violation_count for result in nonresonant_results
        ),
        "nonresonant_top": top_results(nonresonant_results, top_count),
        "resonant_case_count": len(resonant_results),
        "resonant_scanned_tuple_count": sum(
            result.scanned_tuple_count for result in resonant_results
        ),
        "resonant_violation_count": sum(
            result.violation_count for result in resonant_results
        ),
        "resonant_top": top_results(resonant_results, top_count),
        "diagonal_case_count": len(diagonal_results),
        "diagonal_scanned_tuple_count": sum(
            result.scanned_tuple_count for result in diagonal_results
        ),
        "diagonal_violation_count": sum(
            result.violation_count for result in diagonal_results
        ),
        "diagonal_top": top_results(diagonal_results, top_count),
        "overall_violation_count": sum(
            result.violation_count for result in all_results
        ),
        "overall_top": top_results(all_results, top_count),
    }


def print_text_report(summary: Dict[str, object]) -> None:
    print("M1 remaining two-coordinate wall scan")
    print(
        "grid:",
        f"cases={summary['grid_case_count']}",
        f"remaining_tuples={summary['grid_scanned_tuple_count']}",
        f"violations={summary['grid_violation_count']}",
    )
    print(
        "asymmetric:",
        f"cases={summary['asymmetric_case_count']}",
        f"tuples={summary['asymmetric_scanned_tuple_count']}",
        f"violations={summary['asymmetric_violation_count']}",
    )
    print(
        "nonresonant:",
        f"cases={summary['nonresonant_case_count']}",
        f"tuples={summary['nonresonant_scanned_tuple_count']}",
        f"violations={summary['nonresonant_violation_count']}",
    )
    print(
        "line-conic resonant:",
        f"cases={summary['resonant_case_count']}",
        f"tuples={summary['resonant_scanned_tuple_count']}",
        f"violations={summary['resonant_violation_count']}",
    )
    print(
        "diagonal:",
        f"cases={summary['diagonal_case_count']}",
        f"remaining_tuples={summary['diagonal_scanned_tuple_count']}",
        f"violations={summary['diagonal_violation_count']}",
    )
    print(f"overall violations={summary['overall_violation_count']}")
    print("top results:")
    for row in summary["overall_top"]:
        print(
            "  "
            f"ratio={row['best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"n={row['n']}",
            f"e={row['e']}",
            f"h={row['h']}",
            f"tuple={tuple(row['best_tuple'])}",
            f"lines={tuple(row['best_line_monodromies'])}",
            f"equal_pair={row['best_projective_equal_pair']}",
            f"equal_lines={row['best_equal_line_monodromy']}",
            f"line_conic_res={row['best_line_conic_resonant']}",
            f"mode={row['mode']}",
        )
    print("top line-conic resonant asymmetric results:")
    for row in summary["resonant_top"]:
        print(
            "  "
            f"ratio={row['best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"n={row['n']}",
            f"e={row['e']}",
            f"h={row['h']}",
            f"tuple={tuple(row['best_tuple'])}",
            f"lines={tuple(row['best_line_monodromies'])}",
            f"line_conic_res={row['best_line_conic_resonant']}",
            f"mode={row['mode']}",
        )
    print("top asymmetric results:")
    for row in summary["asymmetric_top"]:
        print(
            "  "
            f"ratio={row['best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"n={row['n']}",
            f"e={row['e']}",
            f"h={row['h']}",
            f"tuple={tuple(row['best_tuple'])}",
            f"lines={tuple(row['best_line_monodromies'])}",
            f"line_conic_res={row['best_line_conic_resonant']}",
            f"mode={row['mode']}",
        )
    print("top nonresonant asymmetric results:")
    for row in summary["nonresonant_top"]:
        print(
            "  "
            f"ratio={row['best_ratio_to_p']:.10f}",
            f"p={row['p']}",
            f"n={row['n']}",
            f"e={row['e']}",
            f"h={row['h']}",
            f"tuple={tuple(row['best_tuple'])}",
            f"lines={tuple(row['best_line_monodromies'])}",
            f"line_conic_res={row['best_line_conic_resonant']}",
            f"mode={row['mode']}",
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preset", choices=("smoke", "report"), default="smoke")
    parser.add_argument("--prime-limit", type=int, default=None)
    parser.add_argument("--max-character-order", type=int, default=None)
    parser.add_argument("--diagonal-n", type=int, default=None)
    parser.add_argument("--diagonal-prime-limit", type=int, default=None)
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--tolerance", type=float, default=1e-7)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    return parser.parse_args()


def fill_preset(args: argparse.Namespace) -> argparse.Namespace:
    if args.preset == "report":
        defaults = {
            "prime_limit": 500,
            "max_character_order": 24,
            "diagonal_n": 20,
            "diagonal_prime_limit": 1601,
        }
    else:
        defaults = {
            "prime_limit": 199,
            "max_character_order": 18,
            "diagonal_n": 20,
            "diagonal_prime_limit": 461,
        }
    for key, value in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, value)
    return args


def main() -> None:
    args = fill_preset(parse_args())
    grid_results = scan_grid(
        prime_limit=int(args.prime_limit),
        max_character_order=int(args.max_character_order),
        asymmetric_only=False,
        nonresonant_only=False,
        resonant_only=False,
        tolerance=float(args.tolerance),
    )
    asymmetric_results = scan_grid(
        prime_limit=int(args.prime_limit),
        max_character_order=int(args.max_character_order),
        asymmetric_only=True,
        nonresonant_only=False,
        resonant_only=False,
        tolerance=float(args.tolerance),
    )
    nonresonant_results = scan_grid(
        prime_limit=int(args.prime_limit),
        max_character_order=int(args.max_character_order),
        asymmetric_only=True,
        nonresonant_only=True,
        resonant_only=False,
        tolerance=float(args.tolerance),
    )
    resonant_results = scan_grid(
        prime_limit=int(args.prime_limit),
        max_character_order=int(args.max_character_order),
        asymmetric_only=True,
        nonresonant_only=False,
        resonant_only=True,
        tolerance=float(args.tolerance),
    )
    diagonal_results = scan_diagonal_family(
        n=int(args.diagonal_n),
        prime_limit=int(args.diagonal_prime_limit),
        tolerance=float(args.tolerance),
    )
    summary = summarize_results(
        grid_results,
        asymmetric_results,
        nonresonant_results,
        resonant_results,
        diagonal_results,
        int(args.top),
    )
    summary["parameters"] = {
        "preset": args.preset,
        "prime_limit": args.prime_limit,
        "max_character_order": args.max_character_order,
        "diagonal_n": args.diagonal_n,
        "diagonal_prime_limit": args.diagonal_prime_limit,
        "top": args.top,
        "tolerance": args.tolerance,
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print_text_report(summary)


if __name__ == "__main__":
    main()
