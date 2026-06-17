#!/usr/bin/env python3
"""Finite-length quotient-profile and dimension-dither scanner.

Proof status: AUDIT / EXPERIMENTAL.

The exact-divisibility profile implements the quantity from snarks_v4.tex:

    Qprof_H(a,k) =
      max_{M | gcd(n,k), M > 1, a-k < M, k/M <= n/M - 1}
        log2 binom(n/M - 1, k/M).

For dyadic domains n=2^m, the script compares k0=rho*n with dithered
dimensions k=k0-r.  It also records a separate remainder-variant diagnostic
suggested by the quotient-hygiene section: if k = M*floor(k/M)+rem, then the
remainder construction can meet target slack sigma=a-k by using a support
inside one M-coset of size sigma+rem, provided sigma+rem < M.

The exact profile is the certificate quantity.  The remainder diagnostic is a
finite-length warning signal for small-remainder dimensions, not a replacement
for the exact profile.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Iterable, List, Optional, Sequence

DEFAULT_RATES = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16))
DEFAULT_ETAS = (Fraction(1, 64), Fraction(1, 32), Fraction(1, 16))
LOG2 = math.log(2)


@dataclass(frozen=True)
class ScaleRecord:
    """One quotient scale contribution."""

    M: int
    N: int
    quotient_dimension: int
    log2_list_size: float
    remainder: Optional[int] = None
    support_inside_coset: Optional[int] = None

    def to_json(self) -> Dict[str, object]:
        result: Dict[str, object] = {
            "M_coset_size": self.M,
            "N_quotient_order": self.N,
            "quotient_dimension": self.quotient_dimension,
            "log2_list_size": round(self.log2_list_size, 6),
        }
        if self.remainder is not None:
            result["remainder"] = self.remainder
        if self.support_inside_coset is not None:
            result["support_inside_coset"] = self.support_inside_coset
        return result


def parse_fraction(raw: str) -> Fraction:
    try:
        return Fraction(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid fraction: {raw}") from exc


def parse_fraction_list(raw: str) -> List[Fraction]:
    if not raw:
        return []
    return [parse_fraction(part.strip()) for part in raw.split(",") if part.strip()]


def fraction_label(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    if k == 0 or k == n:
        return 0.0
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / LOG2


def divisors_of_power_of_two(n: int) -> List[int]:
    if n <= 0 or n & (n - 1):
        raise ValueError(f"expected a positive power of two, got n={n}")
    divisors = []
    value = 1
    while value <= n:
        divisors.append(value)
        value <<= 1
    return divisors


def ceil_fraction_times(value: Fraction, n: int) -> int:
    numerator = value.numerator * n
    return (numerator + value.denominator - 1) // value.denominator


def exact_scales(n: int, k: int, sigma: int) -> List[ScaleRecord]:
    records = []
    for M in divisors_of_power_of_two(n):
        if M <= 1 or k % M != 0 or sigma >= M:
            continue
        N = n // M
        quotient_dimension = k // M
        if quotient_dimension < 1 or quotient_dimension > N - 1:
            continue
        records.append(
            ScaleRecord(
                M=M,
                N=N,
                quotient_dimension=quotient_dimension,
                log2_list_size=log2_binom(N - 1, quotient_dimension),
            )
        )
    records.sort(key=lambda item: (-item.log2_list_size, item.M))
    return records


def remainder_scales(n: int, k: int, sigma: int) -> List[ScaleRecord]:
    records = []
    for M in divisors_of_power_of_two(n):
        if M <= 1:
            continue
        N = n // M
        quotient_dimension = k // M
        if quotient_dimension < 1 or quotient_dimension > N - 1:
            continue
        remainder = k % M
        support_inside_coset = sigma + remainder
        if support_inside_coset >= M:
            continue
        records.append(
            ScaleRecord(
                M=M,
                N=N,
                quotient_dimension=quotient_dimension,
                log2_list_size=log2_binom(N - 1, quotient_dimension),
                remainder=remainder,
                support_inside_coset=support_inside_coset,
            )
        )
    records.sort(key=lambda item: (-item.log2_list_size, item.M))
    return records


def profile_value(records: Sequence[ScaleRecord]) -> Optional[float]:
    if not records:
        return None
    return records[0].log2_list_size


def best_record(records: Sequence[Dict[str, object]], key: str) -> Dict[str, object]:
    def score(record: Dict[str, object]) -> tuple:
        value = record[key]
        numeric = -1.0 if value is None else float(value)
        return (numeric, int(record["dither"]))

    return min(records, key=score)


def retained_scales(records: Sequence[ScaleRecord], top_scales: int) -> List[Dict[str, object]]:
    if top_scales < 0:
        return [item.to_json() for item in records]
    return [item.to_json() for item in records[:top_scales]]


def scan_case(
    m: int,
    rate: Fraction,
    eta: Fraction,
    max_dither: int,
    top_scales: int,
) -> Dict[str, object]:
    n = 1 << m
    if (rate * n).denominator != 1:
        raise ValueError(f"rate {rate} does not give integral k at n=2^{m}")
    k0 = int(rate * n)
    sigma = ceil_fraction_times(eta, n)
    dither_records = []

    for dither in range(max_dither + 1):
        k = k0 - dither
        if k <= 0:
            continue
        exact = exact_scales(n, k, sigma)
        remainder = remainder_scales(n, k, sigma)
        dither_records.append(
            {
                "dither": dither,
                "k": k,
                "gcd_n_k": math.gcd(n, k),
                "sigma": sigma,
                "rate_actual": k / n,
                "rate_loss": dither / n,
                "exact_profile_log2": (
                    None if profile_value(exact) is None else round(profile_value(exact), 6)
                ),
                "exact_active_scales": retained_scales(exact, top_scales),
                "remainder_profile_log2": (
                    None
                    if profile_value(remainder) is None
                    else round(profile_value(remainder), 6)
                ),
                "remainder_active_scales": retained_scales(remainder, top_scales),
            }
        )

    return {
        "m": m,
        "n": n,
        "rate_nominal": fraction_label(rate),
        "eta": fraction_label(eta),
        "k0": k0,
        "sigma": sigma,
        "max_dither": max_dither,
        "exact_rate": dither_records[0],
        "one_step_dither": next(
            (record for record in dither_records if record["dither"] == 1),
            None,
        ),
        "best_exact_dither": best_record(dither_records, "exact_profile_log2"),
        "best_remainder_dither": best_record(dither_records, "remainder_profile_log2"),
        "dithers": dither_records,
    }


def scan(
    m_min: int,
    m_max: int,
    rates: Iterable[Fraction],
    etas: Iterable[Fraction],
    max_dither: int,
    top_scales: int,
) -> Dict[str, object]:
    cases = []
    for m in range(m_min, m_max + 1):
        for rate in rates:
            for eta in etas:
                if (rate * (1 << m)).denominator == 1:
                    cases.append(scan_case(m, rate, eta, max_dither, top_scales))
    return {
        "proof_status": "AUDIT / EXPERIMENTAL",
        "theorem_problem_id": "L3-quotient-profile-dimension-dithering",
        "determinism": "deterministic finite divisor scan; no random seed",
        "object_checked": (
            "exact Qprof_H(a,k) from snarks_v4.tex plus a separate "
            "small-remainder quotient-core diagnostic"
        ),
        "cases": cases,
    }


def format_value(value: object) -> str:
    if value is None:
        return "empty"
    return f"{float(value):.2f}"


def format_scales(scales: Sequence[Dict[str, object]]) -> str:
    if not scales:
        return "-"
    pieces = []
    for scale in scales:
        piece = (
            f"M={scale['M_coset_size']},N={scale['N_quotient_order']},"
            f"log={float(scale['log2_list_size']):.1f}"
        )
        if "remainder" in scale:
            piece += (
                f",rem={scale['remainder']},T={scale['support_inside_coset']}"
            )
        pieces.append(piece)
    return "; ".join(pieces)


def print_text(result: Dict[str, object]) -> None:
    print("Quotient-profile dimension-dither scan")
    print("proof_status: AUDIT / EXPERIMENTAL")
    print("exact object: Qprof_H(a,k) at a=k+sigma")
    print("remainder object: diagnostic for sigma+remainder < M")
    print()

    for case in result["cases"]:
        exact = case["exact_rate"]
        one = case["one_step_dither"]
        best_exact = case["best_exact_dither"]
        best_remainder = case["best_remainder_dither"]
        print(
            "m={m:>2} n=2^{m:<2} rho={rho:<4} eta={eta:<5} sigma={sigma:<6} "
            "k0={k0}".format(
                m=case["m"],
                rho=case["rate_nominal"],
                eta=case["eta"],
                sigma=case["sigma"],
                k0=case["k0"],
            )
        )
        print(
            "  r=0 exact={exact} remainder={remainder} gcd={gcd}".format(
                exact=format_value(exact["exact_profile_log2"]),
                remainder=format_value(exact["remainder_profile_log2"]),
                gcd=exact["gcd_n_k"],
            )
        )
        if one is not None:
            print(
                "  r=1 exact={exact} remainder={remainder} gcd={gcd}".format(
                    exact=format_value(one["exact_profile_log2"]),
                    remainder=format_value(one["remainder_profile_log2"]),
                    gcd=one["gcd_n_k"],
                )
            )
        print(
            "  best exact r={r} value={value}; best remainder r={rr} value={rvalue}".format(
                r=best_exact["dither"],
                value=format_value(best_exact["exact_profile_log2"]),
                rr=best_remainder["dither"],
                rvalue=format_value(best_remainder["remainder_profile_log2"]),
            )
        )
        print("  active exact scales: " + format_scales(exact["exact_active_scales"]))
        print(
            "  active remainder scales: "
            + format_scales(exact["remainder_active_scales"])
        )
        print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan dyadic quotient-profile obstructions under dimension dithering."
    )
    parser.add_argument("--m-min", type=int, default=8, help="minimum m for n=2^m")
    parser.add_argument("--m-max", type=int, default=20, help="maximum m for n=2^m")
    parser.add_argument(
        "--rates",
        type=parse_fraction_list,
        default=list(DEFAULT_RATES),
        help="comma-separated nominal rates, e.g. 1/2,1/4",
    )
    parser.add_argument(
        "--etas",
        type=parse_fraction_list,
        default=list(DEFAULT_ETAS),
        help="comma-separated reserves eta, e.g. 1/64,1/32,1/16",
    )
    parser.add_argument(
        "--max-dither",
        type=int,
        default=16,
        help="scan k=rho*n-r for 0 <= r <= max-dither",
    )
    parser.add_argument(
        "--top-scales",
        type=int,
        default=-1,
        help="number of active scales retained per dither; negative retains all",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    args = parser.parse_args()

    if args.m_min < 1 or args.m_max < args.m_min:
        raise SystemExit("require 1 <= --m-min <= --m-max")
    if args.max_dither < 0:
        raise SystemExit("--max-dither must be nonnegative")
    result = scan(
        m_min=args.m_min,
        m_max=args.m_max,
        rates=args.rates,
        etas=args.etas,
        max_dither=args.max_dither,
        top_scales=args.top_scales,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
