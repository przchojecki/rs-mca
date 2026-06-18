#!/usr/bin/env python3
"""Verify the finite full-domain slack-three cube-coset audit.

Proof status: AUDIT / EXPERIMENTAL.

This checks the finite enumeration used in
experimental/m1_support_coefficient_test.md for the full-domain slack-three
first-superboundary beta ledger. It enumerates beta values by cube coset for
prime fields with p == 1 mod 3 below the analytic threshold 271.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from mca_slope_scan import make_domain
from m1_support_occupancy_scan import (
    full_domain_slack_three_beta_class_data,
    slack_three_first_superboundary_shape_ledger,
)


ANALYTIC_THRESHOLD = 271
SATURATION_THRESHOLD = 103
EXPECTED_UNSATURATED_BELOW_271 = (
    7,
    13,
    19,
    31,
    37,
    43,
    61,
    67,
    73,
    79,
    97,
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


def primes_one_mod_three_below(bound: int) -> List[int]:
    return [
        value
        for value in range(5, bound)
        if value % 3 == 1 and is_prime(value)
    ]


def cube_coset_row(p: int) -> Dict[str, object]:
    _, domain = make_domain(p, p - 1, None)
    ledger = slack_three_first_superboundary_shape_ledger(
        p=p,
        domain=domain,
        support_size=4,
        quotient_order=1,
        fiber_size=p - 1,
    )
    data = full_domain_slack_three_beta_class_data(p)
    assert data is not None
    return {
        "p": p,
        "beta_count": int(ledger["beta_count"]),
        "zero_beta_count": int(data["zero_beta_count"]),
        "cube_coset_beta_counts": tuple(
            int(count) for count in ledger["nonzero_cube_coset_beta_counts"]
        ),
        "hit_cube_cosets": int(ledger["nonzero_cube_coset_count"]),
        "total_cube_cosets": int(ledger["total_nonzero_cube_coset_count"]),
        "saturates": (
            int(ledger["nonzero_cube_coset_count"])
            == int(ledger["total_nonzero_cube_coset_count"])
        ),
        "analytic_lower_bound": int(data["cube_coset_beta_lower_bound"]),
        "analytic_certificate": bool(data["cube_coset_saturation_certificate"]),
    }


def audit_below_threshold() -> Tuple[List[Dict[str, object]], List[int]]:
    rows = [
        cube_coset_row(p)
        for p in primes_one_mod_three_below(ANALYTIC_THRESHOLD)
    ]
    unsaturated = [int(row["p"]) for row in rows if not row["saturates"]]
    return rows, unsaturated


def main() -> None:
    rows, unsaturated = audit_below_threshold()
    expected = list(EXPECTED_UNSATURATED_BELOW_271)
    assert unsaturated == expected
    assert all(
        row["saturates"]
        for row in rows
        if int(row["p"]) >= SATURATION_THRESHOLD
    )
    assert not any(
        row["analytic_certificate"]
        for row in rows
        if int(row["p"]) < ANALYTIC_THRESHOLD
    )

    sample_rows = [
        row
        for row in rows
        if int(row["p"]) in (37, 97, 103, 109)
    ]
    print(
        "full-domain slack-three finite cube-coset audit "
        f"primes={len(rows)} threshold={SATURATION_THRESHOLD}"
    )
    print(f"unsaturated_below_{ANALYTIC_THRESHOLD}={tuple(unsaturated)}")
    print(f"sample_rows={tuple(sample_rows)}")
    print("M1 slack-three full-domain finite cube-coset audit passed")


if __name__ == "__main__":
    main()
