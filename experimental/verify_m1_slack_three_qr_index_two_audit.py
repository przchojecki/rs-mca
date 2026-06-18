#!/usr/bin/env python3
"""Verify the quadratic-residue index-two slack-three finite audit.

Proof status: AUDIT / EXPERIMENTAL.

This checks the exact finite range below the conditional uniform threshold
P_16=38026 for D=(F_p^*)^2 and p == 5 mod 6. In this case D^3=D, so the
nonzero split-cubic beta image has two D^3 cosets to hit.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from mca_slope_scan import make_domain
from m1_support_occupancy_scan import (
    slack_three_cube_coset_coverage_data,
    slack_three_split_cubic_beta_ledger,
)


ANALYTIC_THRESHOLD = 38026
SATURATION_THRESHOLD = 1049
EXPECTED_UNSATURATED_BELOW_38026 = (
    5,
    11,
    17,
    23,
    29,
    41,
    47,
    53,
    59,
    71,
    83,
    89,
    101,
    107,
    113,
    131,
    137,
    149,
    167,
    173,
    179,
    191,
    197,
    227,
    233,
    239,
    251,
    257,
    269,
    281,
    317,
    347,
    359,
    383,
    401,
    431,
    467,
    491,
    503,
    587,
    617,
    647,
    653,
    701,
    1031,
)


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


def primes_five_mod_six_below(bound: int) -> List[int]:
    return [
        value
        for value in range(5, bound)
        if value % 6 == 5 and is_prime(value)
    ]


def index_two_row(p: int) -> Dict[str, object]:
    n = (p - 1) // 2
    _, domain = make_domain(p, n, None)
    ledger = slack_three_split_cubic_beta_ledger(p, domain)
    certificate = slack_three_cube_coset_coverage_data(p, n)
    return {
        "p": p,
        "n": n,
        "beta_count": int(ledger["beta_count"]),
        "cube_coset_beta_counts": tuple(
            int(count) for count in ledger["nonzero_cube_coset_beta_counts"]
        ),
        "hit_cube_cosets": int(ledger["nonzero_cube_coset_count"]),
        "total_cube_cosets": int(ledger["total_nonzero_cube_coset_count"]),
        "saturates": (
            int(ledger["nonzero_cube_coset_count"])
            == int(ledger["total_nonzero_cube_coset_count"])
        ),
        "coverage_lower_bound": int(
            certificate["admissible_parameter_lower_bound"]
        ),
        "coverage_certificate": bool(certificate["saturation_certificate"]),
        "uniform_prime_threshold": int(
            certificate["uniform_prime_threshold"]
        ),
    }


def audit_below_threshold() -> Tuple[List[Dict[str, object]], List[int]]:
    rows = [
        index_two_row(p)
        for p in primes_five_mod_six_below(ANALYTIC_THRESHOLD)
    ]
    unsaturated = [int(row["p"]) for row in rows if not row["saturates"]]
    return rows, unsaturated


def main() -> None:
    rows, unsaturated = audit_below_threshold()
    expected = list(EXPECTED_UNSATURATED_BELOW_38026)
    assert unsaturated == expected
    assert all(
        row["saturates"]
        for row in rows
        if int(row["p"]) >= SATURATION_THRESHOLD
    )
    assert all(
        int(row["uniform_prime_threshold"]) == ANALYTIC_THRESHOLD
        for row in rows
    )

    sample_rows = [
        row
        for row in rows
        if int(row["p"]) in (701, 1031, 1049, 1061)
    ]
    print(
        "slack-three QR index-two finite cube-coset audit "
        f"primes={len(rows)} threshold={SATURATION_THRESHOLD}"
    )
    print(f"unsaturated_below_{ANALYTIC_THRESHOLD}={tuple(unsaturated)}")
    print(f"sample_rows={tuple(sample_rows)}")
    print("M1 slack-three QR index-two finite audit passed")


if __name__ == "__main__":
    main()
