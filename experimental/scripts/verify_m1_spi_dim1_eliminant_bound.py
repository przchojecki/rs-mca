#!/usr/bin/env python3
"""Verify the M1 SPI dimension-one eliminant degree arithmetic.

The companion note is symbolic.  This script checks the degree-propagation
recurrence for pseudo-division and records the pinned-row arithmetic producing
the 49408 cap.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/m1-spi-dim1-eliminant-bound/"
    "m1_spi_dim1_eliminant_bound.json"
)


NEG_INF = -10**18


@dataclass(frozen=True)
class Case:
    name: str
    n: int
    k: int
    agreement: int

    @property
    def t(self) -> int:
        return self.agreement - self.k

    @property
    def j(self) -> int:
        return self.n - self.agreement

    @property
    def delta(self) -> int:
        return self.n - self.j + 1


def max_deg(left: int, right: int) -> int:
    return left if left >= right else right


def add_deg(value: int, inc: int) -> int:
    if value <= NEG_INF // 2:
        return NEG_INF
    return value + inc


def pseudo_remainder_degree_profile(n: int, j: int, coeff_degree: int) -> list[int]:
    """Propagate Z-degree bounds through pseudo-division.

    The input polynomial is X^n - 1, whose nonzero coefficients have Z-degree
    zero.  The divisor L_Z has degree j in X and all coefficients have
    Z-degree at most coeff_degree.  At each pseudo-division step,

        R <- lc(L_Z) R - coeff(R, X^d) X^(d-j) L_Z.

    This function tracks only upper bounds for the Z-degrees of the
    coefficients of R.
    """

    if not 0 <= j <= n:
        raise ValueError("need 0 <= j <= n")

    degrees = [NEG_INF] * (n + 1)
    degrees[0] = 0
    degrees[n] = 0

    for d in range(n, j - 1, -1):
        pivot_degree = degrees[d]

        # Multiplication by the leading coefficient at this step.
        next_degrees = [add_deg(value, coeff_degree) for value in degrees]

        # Subtract the shifted pivot multiple of L_Z.
        if pivot_degree > NEG_INF // 2:
            for i in range(j + 1):
                target = d - j + i
                next_degrees[target] = max_deg(
                    next_degrees[target],
                    pivot_degree + coeff_degree,
                )

        # The top term is cancelled by construction.
        next_degrees[d] = NEG_INF
        degrees = next_degrees

    return [0 if value < 0 else value for value in degrees[:j]]


def analyze_case(case: Case) -> dict[str, Any]:
    if case.t != case.j:
        raise ValueError(f"{case.name}: expected deficiency-one boundary t=j")
    if case.t <= 0:
        raise ValueError(f"{case.name}: expected positive t")

    profile = pseudo_remainder_degree_profile(case.n, case.j, case.t)
    top_bound = case.delta * case.t
    global_bound = case.t + top_bound

    if max(profile) > top_bound:
        raise AssertionError((case, "pseudo-remainder degree bound failed", max(profile), top_bound))
    if len(profile) != case.j:
        raise AssertionError((case, "unexpected remainder length"))

    return {
        "name": case.name,
        "n": case.n,
        "k": case.k,
        "agreement": case.agreement,
        "t": case.t,
        "j": case.j,
        "delta": case.delta,
        "cramer_minor_degree_bound": case.t,
        "rank_drop_degree_cap": case.t,
        "top_pseudo_remainder_degree_bound": top_bound,
        "global_eliminant_degree_cap": global_bound,
        "degree_profile_max": max(profile),
        "degree_profile_min": min(profile) if profile else None,
        "degree_profile_first_last": [profile[0], profile[-1]] if profile else [],
        "all_coefficients_within_bound": True,
    }


def build_certificate() -> dict[str, Any]:
    cases = [
        Case("F_97/mu_16 acid-scale toy", n=16, k=8, agreement=12),
        Case("F_17^32 pinned A=384 row", n=512, k=256, agreement=384),
        Case("symbolic-size smoke n=32", n=32, k=16, agreement=24),
    ]
    payloads = [analyze_case(case) for case in cases]
    pinned = next(row for row in payloads if row["name"] == "F_17^32 pinned A=384 row")
    if pinned["global_eliminant_degree_cap"] != 49408:
        raise AssertionError(("pinned cap mismatch", pinned["global_eliminant_degree_cap"]))
    if pinned["top_pseudo_remainder_degree_bound"] != 49280:
        raise AssertionError(("pinned top bound mismatch", pinned["top_pseudo_remainder_degree_bound"]))

    return {
        "schema": "m1-spi-dim1-eliminant-bound-v1",
        "status": "PROVED_SYMBOLIC",
        "dag_target": "spi_dim1",
        "theorem": {
            "chart": "deficiency-one one-parameter split Hankel pencil with t=j",
            "rank_drop_cap": "degree <= t from a nonzero Cramer maximal minor",
            "top_chart_cap": "degree <= (n-j+1)t for each pseudo-remainder coefficient",
            "global_eliminant_or_residual": "degree <= t + (n-j+1)t, unless the top chart is identically valid",
            "pinned_row_cap": "n=512, k=256, A=384 gives 49408",
        },
        "cases": payloads,
        "non_claims": [
            "does not compute the F_17^32 root table",
            "does not classify identically valid residual pencils",
            "does not prove higher-dimensional SPI incidence",
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
    print("M1 SPI dimension-one eliminant bound")
    print(f"  schema: {cert['schema']}")
    for row in cert["cases"]:
        print(
            f"  {row['name']}: t=j={row['t']} delta={row['delta']} "
            f"top={row['top_pseudo_remainder_degree_bound']} "
            f"global={row['global_eliminant_degree_cap']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
