#!/usr/bin/env python3
"""Exact arithmetic compiler for quotient-core planted list lower bounds.

This verifier packages the arithmetic consequence of Paper B's quotient-core
list obstruction.  It does not prove the safe-side list bound; it checks the
integer count and budget-window arithmetic used by planted lower certificates.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from math import comb, gcd, isqrt
from pathlib import Path
from typing import Any


EPS_BITS = 128
OFFICIAL_RATES = [(1, 2), (1, 4), (1, 8), (1, 16)]
BUDGET_BITS = [64, 96, 128]
DEFAULT_CERT = Path(
    "experimental/data/certificates/list-planted-arithmetic/"
    "list_planted_arithmetic_compiler.json"
)


@dataclass(frozen=True)
class Scale:
    M: int
    quotient_order: int
    quotient_dimension: int
    count: int


def divisors(n: int) -> list[int]:
    out: list[int] = []
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            out.append(d)
            if d * d != n:
                out.append(n // d)
    return sorted(out)


def planted_count(n: int, k: int, M: int) -> int:
    if n <= 0 or k <= 0 or M <= 0:
        raise ValueError("n, k, and M must be positive")
    if n % M or k % M:
        raise ValueError("M must divide both n and k")
    N = n // M
    K = k // M
    if K > N - 1:
        raise ValueError("quotient dimension must satisfy k/M <= n/M - 1")
    return comb(N - 1, K)


def active_scales(n: int, k: int, sigma: int) -> list[Scale]:
    if not (1 <= sigma <= n - k):
        raise ValueError("sigma must lie in the positive list-decoding slack range")
    rows: list[Scale] = []
    for M in divisors(gcd(n, k)):
        if sigma < M and k // M <= n // M - 1:
            rows.append(
                Scale(
                    M=M,
                    quotient_order=n // M,
                    quotient_dimension=k // M,
                    count=planted_count(n, k, M),
                )
            )
    return rows


def max_active_count(n: int, k: int, sigma: int) -> tuple[int, Scale | None]:
    rows = active_scales(n, k, sigma)
    if not rows:
        return 0, None
    best = max(rows, key=lambda row: (row.count, row.quotient_order, row.M))
    return best.count, best


def dyadic_crossing(rate_num: int, rate_den: int, budget_bits: int) -> dict[str, Any]:
    budget = (1 << budget_bits) - 1
    last_below: dict[str, Any] | None = None
    first_above: dict[str, Any] | None = None
    rows: list[dict[str, Any]] = []
    for exponent in range(1, 16):
        N = 1 << exponent
        if (rate_num * N) % rate_den:
            continue
        K = (rate_num * N) // rate_den
        if K > N - 1:
            continue
        count = comb(N - 1, K)
        row = {
            "quotient_order": N,
            "quotient_dimension": K,
            "count": count,
            "count_bit_length": count.bit_length(),
            "beats_budget": count > budget,
        }
        rows.append(row)
        if count <= budget:
            last_below = row
        elif first_above is None:
            first_above = row
            break
    if first_above is None:
        raise AssertionError(f"no crossing found for rate {rate_num}/{rate_den}")
    return {
        "rate": f"{rate_num}/{rate_den}",
        "budget_bits": budget_bits,
        "budget_floor": budget,
        "last_not_certified_by_this_scale": last_below,
        "first_planted_unsafe_scale": first_above,
        "slack_boundary": {
            "unsafe_lower_certificate_when": (
                f"sigma < n/{first_above['quotient_order']}"
            ),
            "previous_dyadic_boundary": (
                None
                if last_below is None
                else f"n/{last_below['quotient_order']}"
            ),
        },
        "checked_prefix": rows,
    }


def budget_window(lower_count: int, upper_count: int) -> dict[str, Any]:
    if not (0 <= lower_count < upper_count):
        raise ValueError("need 0 <= lower_count < upper_count")
    q_min = lower_count << EPS_BITS
    q_max = (upper_count << EPS_BITS) - 1
    return {
        "budget_interval": [lower_count, upper_count - 1],
        "q_interval_for_floor_q_over_2_128": [q_min, q_max],
        "number_of_budget_values": upper_count - lower_count,
        "q_interval_size": q_max - q_min + 1,
    }


def sample_profile(n: int, rate_num: int, rate_den: int, sigma_denoms: list[int]) -> list[dict[str, Any]]:
    if (rate_num * n) % rate_den:
        raise ValueError("n must be divisible by the rate denominator")
    k = (rate_num * n) // rate_den
    out: list[dict[str, Any]] = []
    for denom in sigma_denoms:
        sigma = n // denom
        count, best = max_active_count(n, k, sigma)
        out.append(
            {
                "n": n,
                "rate": f"{rate_num}/{rate_den}",
                "sigma": sigma,
                "sigma_over_n": f"1/{denom}",
                "max_planted_count": count,
                "max_planted_count_bit_length": count.bit_length() if count else 0,
                "best_scale": None
                if best is None
                else {
                    "M": best.M,
                    "quotient_order": best.quotient_order,
                    "quotient_dimension": best.quotient_dimension,
                    "count": best.count,
                },
            }
        )
    return out


def self_tests() -> None:
    assert planted_count(16, 8, 2) == comb(7, 4)
    assert planted_count(512, 256, 4) == comb(127, 64)
    scales = active_scales(512, 256, 3)
    assert {row.M for row in scales} == {4, 8, 16, 32, 64, 128, 256}
    assert max_active_count(512, 256, 3)[0] == comb(127, 64)
    assert max_active_count(512, 256, 4)[0] == comb(63, 32)
    # Strict activity matters: sigma = M deactivates that quotient core.
    assert all(row.M > 4 for row in active_scales(512, 256, 4))

    for budget_bits in BUDGET_BITS:
        for rate_num, rate_den in OFFICIAL_RATES:
            crossing = dyadic_crossing(rate_num, rate_den, budget_bits)
            low = crossing["last_not_certified_by_this_scale"]
            high = crossing["first_planted_unsafe_scale"]
            if low is not None:
                assert low["count"] <= crossing["budget_floor"]
            assert high["count"] > crossing["budget_floor"]
            window = budget_window(low["count"] if low else 0, high["count"])
            assert window["number_of_budget_values"] == high["count"] - (
                low["count"] if low else 0
            )


def build_certificate() -> dict[str, Any]:
    self_tests()
    crossings: list[dict[str, Any]] = []
    windows: list[dict[str, Any]] = []
    for budget_bits in BUDGET_BITS:
        for rate_num, rate_den in OFFICIAL_RATES:
            crossing = dyadic_crossing(rate_num, rate_den, budget_bits)
            crossings.append(crossing)
            low = crossing["last_not_certified_by_this_scale"]
            high = crossing["first_planted_unsafe_scale"]
            lower_count = 0 if low is None else low["count"]
            windows.append(
                {
                    "rate": crossing["rate"],
                    "budget_bits": budget_bits,
                    "lower_scale_count": lower_count,
                    "upper_scale_count": high["count"],
                    **budget_window(lower_count, high["count"]),
                }
            )

    profiles: list[dict[str, Any]] = []
    for n in [1 << 20, 1 << 40]:
        for rate_num, rate_den in OFFICIAL_RATES:
            profiles.extend(
                sample_profile(
                    n,
                    rate_num,
                    rate_den,
                    sigma_denoms=[128, 256, 512],
                )
            )

    return {
        "schema": "list-planted-arithmetic-v1",
        "status": "PROVED_ARITHMETIC_COMPILER__CITES_PAPER_B_QCORE",
        "object": {
            "code": "RS[F_q,H,k] with |H|=n",
            "list_radius": "1 - rho - sigma/n",
            "agreement": "k + sigma",
            "lower_bound_object": "Lst(C,1-rho-sigma/n)",
            "budget": "floor(q_list / 2^128)",
            "endpoint": "strict qcore activity condition 1 <= sigma < M",
        },
        "paper_dependency": {
            "source": "tex/slackMCA_v4.tex",
            "theorem": "thm:qcore",
            "used_statement": (
                "If M|k, k/M <= n/M - 1, and 1 <= sigma < M, then a "
                "received word has at least binom(n/M - 1, k/M) codewords "
                "at agreement k + sigma."
            ),
        },
        "compiler_theorem": {
            "active_scale_set": (
                "{M | gcd(n,k): sigma < M and k/M <= n/M - 1}"
            ),
            "planted_count_at_scale_M": "binom(n/M - 1, k/M)",
            "compiled_lower_bound": (
                "Lst(C,1-rho-sigma/n) >= max_M binom(n/M - 1,k/M)"
            ),
            "unsafe_test": (
                "max_M binom(n/M - 1,k/M) > floor(q_list/2^128)"
            ),
        },
        "dyadic_crossings": crossings,
        "budget_windows": windows,
        "sample_active_profiles": profiles,
        "non_claims": [
            "This packet is a lower-bound/planted arithmetic compiler only.",
            "It does not prove the matching ImgFib safe-side upper bound.",
            "It does not bound non-planted sunflower or petal extras.",
        ],
    }


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("list-planted-arithmetic certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  crossings: {len(cert['dyadic_crossings'])}")
    for row in cert["dyadic_crossings"]:
        high = row["first_planted_unsafe_scale"]
        low = row["last_not_certified_by_this_scale"]
        low_text = "none" if low is None else f"N={low['quotient_order']} bits={low['count_bit_length']}"
        print(
            "  "
            + f"rate {row['rate']} budget_bits {row['budget_bits']}: "
            + f"last<= {low_text}; first> N={high['quotient_order']} "
            + f"bits={high['count_bit_length']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    cert = build_certificate()

    if args.emit:
        DEFAULT_CERT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_CERT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {DEFAULT_CERT}")

    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")

    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
