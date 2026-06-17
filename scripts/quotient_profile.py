#!/usr/bin/env python3
"""Scan the exact-divisibility quotient-core profile from Paper C.

The profile is

    max log2 binom(n/M - 1, k/M)

over divisors M | gcd(n, k) with M > 1, sigma = a - k < M, and
k/M <= n/M - 1.  The empty maximum is reported as an empty profile.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Any


LOG2 = math.log(2.0)


def positive_int(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def nonnegative_int(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def factor_integer(value: int) -> dict[int, int]:
    """Return a trial-division factorization, intended for smooth dimensions."""
    factors: dict[int, int] = {}
    remaining = value

    count = 0
    while remaining % 2 == 0:
        count += 1
        remaining //= 2
    if count:
        factors[2] = count

    divisor = 3
    limit = math.isqrt(remaining)
    while divisor <= limit and remaining > 1:
        count = 0
        while remaining % divisor == 0:
            count += 1
            remaining //= divisor
        if count:
            factors[divisor] = count
            limit = math.isqrt(remaining)
        divisor += 2

    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1

    return factors


def divisors(value: int) -> list[int]:
    out = [1]
    for prime, exponent in factor_integer(value).items():
        powers = [prime**power for power in range(exponent + 1)]
        out = [base * power for base in out for power in powers]
    return sorted(out)


def binary_entropy(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def log2_binomial(top: int, bottom: int, exact_threshold: int) -> dict[str, Any]:
    if bottom < 0 or bottom > top:
        raise ValueError("invalid binomial arguments")

    if bottom == 0 or bottom == top:
        return {
            "exact": True,
            "estimate_bits": 0.0,
            "lower_bits": 0.0,
            "upper_bits": 0.0,
        }

    if top <= exact_threshold:
        exact_bits = math.log2(math.comb(top, bottom))
        return {
            "exact": True,
            "estimate_bits": exact_bits,
            "lower_bits": exact_bits,
            "upper_bits": exact_bits,
        }

    ratio = bottom / top
    entropy_upper = top * binary_entropy(ratio)
    entropy_lower = max(0.0, entropy_upper - math.log2(top + 1))
    lgamma_estimate = (
        math.lgamma(top + 1)
        - math.lgamma(bottom + 1)
        - math.lgamma(top - bottom + 1)
    ) / LOG2
    return {
        "exact": False,
        "estimate_bits": lgamma_estimate,
        "lower_bits": entropy_lower,
        "upper_bits": entropy_upper,
    }


def budget_summary(
    active_rows: list[dict[str, Any]],
    n: int,
    list_exponent: float | None,
    gamma_bits: float,
) -> dict[str, Any]:
    if not active_rows:
        budget_bits = None
        if list_exponent is not None:
            budget_bits = list_exponent * math.log2(n) + gamma_bits
        return {
            "empty": True,
            "estimate_bits": None,
            "lower_bits": None,
            "upper_bits": None,
            "attaining_divisor": None,
            "budget_bits": budget_bits,
            "budget_decision": "clears_budget"
            if list_exponent is not None
            else "not_requested",
        }

    estimate_row = max(active_rows, key=lambda row: row["log2_binom_estimate_bits"])
    lower_bits = max(row["log2_binom_lower_bits"] for row in active_rows)
    upper_bits = max(row["log2_binom_upper_bits"] for row in active_rows)
    estimate_bits = estimate_row["log2_binom_estimate_bits"]

    if list_exponent is None:
        budget_bits = None
        decision = "not_requested"
    else:
        budget_bits = list_exponent * math.log2(n) + gamma_bits
        if upper_bits <= budget_bits:
            decision = "clears_budget"
        elif lower_bits > budget_bits:
            decision = "fails_budget"
        else:
            decision = "inconclusive_with_entropy_bounds"

    return {
        "empty": False,
        "estimate_bits": estimate_bits,
        "lower_bits": lower_bits,
        "upper_bits": upper_bits,
        "attaining_divisor": estimate_row["M"],
        "budget_bits": budget_bits,
        "budget_decision": decision,
    }


def compute_profile(
    n: int,
    k: int,
    a: int,
    exact_threshold: int,
    list_exponent: float | None,
    gamma_bits: float,
    include_inactive: bool,
) -> dict[str, Any]:
    if not (1 <= k <= n):
        raise ValueError("expected 1 <= k <= n")
    if not (k <= a <= n):
        raise ValueError("expected k <= a <= n")

    sigma = a - k
    gcd_n_k = math.gcd(n, k)
    gcd_divisors = divisors(gcd_n_k)
    active_rows: list[dict[str, Any]] = []
    inactive_rows: list[dict[str, Any]] = []

    for scale in gcd_divisors:
        if scale <= 1:
            continue

        quotient_order = n // scale
        quotient_dimension = k // scale
        reasons: list[str] = []
        if sigma >= scale:
            reasons.append("sigma>=M")
        if quotient_dimension > quotient_order - 1:
            reasons.append("k/M>n/M-1")

        if reasons:
            if include_inactive:
                inactive_rows.append(
                    {
                        "M": scale,
                        "n_over_M": quotient_order,
                        "k_over_M": quotient_dimension,
                        "inactive_reasons": reasons,
                    }
                )
            continue

        binom_top = quotient_order - 1
        binom_bottom = quotient_dimension
        log_data = log2_binomial(binom_top, binom_bottom, exact_threshold)
        active_rows.append(
            {
                "M": scale,
                "n_over_M": quotient_order,
                "k_over_M": quotient_dimension,
                "binomial_top": binom_top,
                "binomial_bottom": binom_bottom,
                "log2_binom_estimate_bits": log_data["estimate_bits"],
                "log2_binom_lower_bits": log_data["lower_bits"],
                "log2_binom_upper_bits": log_data["upper_bits"],
                "binomial_log_exact": log_data["exact"],
            }
        )

    report: dict[str, Any] = {
        "n": n,
        "k": k,
        "a": a,
        "sigma": sigma,
        "gcd_n_k": gcd_n_k,
        "divisor_count_gcd": len(gcd_divisors),
        "active_count": len(active_rows),
        "active_divisors": active_rows,
        "qprofile": budget_summary(active_rows, n, list_exponent, gamma_bits),
    }
    if include_inactive:
        report["inactive_divisors"] = inactive_rows
    return report


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def bits_text(value: float | None) -> str:
    if value is None:
        return "empty"
    if value == 0.0:
        return "0"
    if abs(value) >= 1000:
        return f"{value:.3f}"
    return f"{value:.6f}".rstrip("0").rstrip(".")


def print_profile(report: dict[str, Any]) -> None:
    profile = report["qprofile"]
    print(
        "n={n} k={k} a={a} sigma={sigma} gcd(n,k)={gcd}".format(
            n=report["n"],
            k=report["k"],
            a=report["a"],
            sigma=report["sigma"],
            gcd=report["gcd_n_k"],
        )
    )
    if profile["empty"]:
        print("Qprof_H(a,k): empty exact-divisibility profile")
    else:
        print(
            "Qprof_H(a,k): estimate={estimate} bits, bounds=[{lower}, {upper}] "
            "at M={scale}".format(
                estimate=bits_text(profile["estimate_bits"]),
                lower=bits_text(profile["lower_bits"]),
                upper=bits_text(profile["upper_bits"]),
                scale=profile["attaining_divisor"],
            )
        )

    if profile["budget_decision"] != "not_requested":
        print(
            "budget: {budget} bits, decision={decision}".format(
                budget=bits_text(profile["budget_bits"]),
                decision=profile["budget_decision"],
            )
        )

    if not report["active_divisors"]:
        return

    print()
    print("active quotient scales")
    print("M n/M k/M binom_top binom_bottom log2_estimate log2_bounds exact")
    for row in report["active_divisors"]:
        print(
            "{M} {nM} {kM} {top} {bottom} {estimate} [{lower}, {upper}] {exact}"
            .format(
                M=row["M"],
                nM=row["n_over_M"],
                kM=row["k_over_M"],
                top=row["binomial_top"],
                bottom=row["binomial_bottom"],
                estimate=bits_text(row["log2_binom_estimate_bits"]),
                lower=bits_text(row["log2_binom_lower_bits"]),
                upper=bits_text(row["log2_binom_upper_bits"]),
                exact=str(row["binomial_log_exact"]).lower(),
            )
        )

    inactive_rows = report.get("inactive_divisors", [])
    if inactive_rows:
        print()
        print("inactive quotient scales")
        print("M n/M k/M reasons")
        for row in inactive_rows:
            print(
                "{M} {nM} {kM} {reasons}".format(
                    M=row["M"],
                    nM=row["n_over_M"],
                    kM=row["k_over_M"],
                    reasons=",".join(row["inactive_reasons"]),
                )
            )


def print_sweep(report: dict[str, Any]) -> None:
    print(
        "dyadic sweep n={n} rho=1/{den} sigma={sigma} r={r_min}..{r_max}"
        .format(
            n=report["n"],
            den=report["rho_den"],
            sigma=report["sigma"],
            r_min=report["r_min"],
            r_max=report["r_max"],
        )
    )
    print("r k gcd active best_M qprofile_estimate_bits budget_decision")
    for item in report["rows"]:
        profile = item["profile"]["qprofile"]
        best_scale = profile["attaining_divisor"]
        print(
            "{r} {k} {gcd} {active} {best} {bits} {decision}".format(
                r=item["r"],
                k=item["profile"]["k"],
                gcd=item["profile"]["gcd_n_k"],
                active=item["profile"]["active_count"],
                best=best_scale if best_scale is not None else "-",
                bits=bits_text(profile["estimate_bits"]),
                decision=profile["budget_decision"],
            )
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute the exact-divisibility quotient-core profile."
    )
    parser.add_argument("--n", type=positive_int, required=True, help="domain size")
    parser.add_argument("--k", type=positive_int, help="dimension")
    parser.add_argument("--a", type=positive_int, help="agreement size")
    parser.add_argument("--sigma", type=nonnegative_int, help="agreement slack a-k")
    parser.add_argument(
        "--list-exponent",
        type=float,
        help="target exponent B_L in Qprof_H(a,k) <= B_L log2(n) + Gamma_Q",
    )
    parser.add_argument(
        "--gamma-bits",
        type=float,
        default=0.0,
        help="additive quotient-profile budget Gamma_Q in bits",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    parser.add_argument(
        "--exact-threshold",
        type=nonnegative_int,
        default=5000,
        help="compute exact binomial logs when n/M-1 is at most this value",
    )
    parser.add_argument(
        "--include-inactive",
        action="store_true",
        help="include divisor scales rejected by the profile predicate",
    )
    parser.add_argument(
        "--dyadic-sweep",
        action="store_true",
        help="compare k=n/rho_den-r for r_min <= r <= r_max",
    )
    parser.add_argument(
        "--rho-den",
        type=positive_int,
        choices=(2, 4, 8, 16),
        help="dyadic rate denominator for --dyadic-sweep",
    )
    parser.add_argument(
        "--r-min",
        type=nonnegative_int,
        default=0,
        help="first dither amount for --dyadic-sweep",
    )
    parser.add_argument(
        "--r-max",
        type=nonnegative_int,
        default=16,
        help="last dither amount for --dyadic-sweep",
    )
    return parser


def normal_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.k is None:
        raise ValueError("normal mode requires --k")
    if args.a is None and args.sigma is None:
        raise ValueError("normal mode requires --a or --sigma")
    if args.a is not None and args.sigma is not None:
        raise ValueError("use either --a or --sigma, not both")

    agreement = args.a if args.a is not None else args.k + args.sigma
    return compute_profile(
        n=args.n,
        k=args.k,
        a=agreement,
        exact_threshold=args.exact_threshold,
        list_exponent=args.list_exponent,
        gamma_bits=args.gamma_bits,
        include_inactive=args.include_inactive,
    )


def sweep_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.k is not None or args.a is not None:
        raise ValueError("--dyadic-sweep uses --n, --rho-den, --sigma, and r bounds")
    if args.rho_den is None:
        raise ValueError("--dyadic-sweep requires --rho-den")
    if args.sigma is None:
        raise ValueError("--dyadic-sweep requires --sigma")
    if args.r_min > args.r_max:
        raise ValueError("expected --r-min <= --r-max")
    if not is_power_of_two(args.n):
        raise ValueError("--dyadic-sweep expects n to be a power of two")
    if args.n % args.rho_den != 0:
        raise ValueError("expected rho_den to divide n")

    base_dimension = args.n // args.rho_den
    rows: list[dict[str, Any]] = []
    for r_value in range(args.r_min, args.r_max + 1):
        dimension = base_dimension - r_value
        if dimension < 1:
            continue
        agreement = dimension + args.sigma
        profile = compute_profile(
            n=args.n,
            k=dimension,
            a=agreement,
            exact_threshold=args.exact_threshold,
            list_exponent=args.list_exponent,
            gamma_bits=args.gamma_bits,
            include_inactive=False,
        )
        rows.append({"r": r_value, "profile": profile})

    return {
        "mode": "dyadic_sweep",
        "n": args.n,
        "rho_den": args.rho_den,
        "sigma": args.sigma,
        "r_min": args.r_min,
        "r_max": args.r_max,
        "base_dimension": base_dimension,
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = sweep_report(args) if args.dyadic_sweep else normal_report(args)
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "json":
        json.dump(report, sys.stdout, indent=2, sort_keys=True)
        print()
    elif args.dyadic_sweep:
        print_sweep(report)
    else:
        print_profile(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
