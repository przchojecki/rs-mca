#!/usr/bin/env python3
"""Verify slack-three cube-coset coverage certificate samples.

Proof status: AUDIT / EXPERIMENTAL.

This audits the conditional proper-subgroup cube-coset coverage certificate
from experimental/m1_support_coefficient_test.md. It uses the split-cubic
beta ledger, so exact beta-coset counts are computed in one pass through D
rather than by enumerating conic pairs.
"""

from __future__ import annotations

from typing import Dict, List, Sequence

from mca_slope_scan import make_domain
from m1_support_occupancy_scan import (
    slack_three_cube_coset_coverage_data,
    slack_three_cube_coset_uniform_prime_threshold,
    slack_three_split_cubic_beta_ledger,
)


SAMPLES = (
    {
        "name": "proper-subgroup-index-two-certificate",
        "p": 38039,
        "n": 19019,
        "expect_certificate": True,
        "expect_coset_beta_counts": (404, 416),
        "expect_lower_bound": 14,
        "expect_uniform_prime_threshold": 38026,
    },
    {
        "name": "full-domain-index-three-certificate",
        "p": 2017,
        "n": 2016,
        "expect_certificate": True,
        "expect_coset_beta_counts": (100, 116, 116),
        "expect_lower_bound": 116,
        "expect_uniform_prime_threshold": 1522,
    },
    {
        "name": "proper-subgroup-small-control",
        "p": 71,
        "n": 35,
        "expect_certificate": False,
        "expect_coset_beta_counts": (4,),
        "expect_lower_bound": 0,
        "expect_uniform_prime_threshold": 38026,
    },
)


def split_cubic_beta_coset_row(p: int, n: int) -> Dict[str, object]:
    _, domain = make_domain(p, n, None)
    beta_ledger = slack_three_split_cubic_beta_ledger(p, domain)
    beta_counts = tuple(beta_ledger["nonzero_cube_coset_beta_counts"])
    total_cosets = int(beta_ledger["total_nonzero_cube_coset_count"])
    exact_min_ordered = 0
    if len(beta_counts) == total_cosets and beta_counts:
        exact_min_ordered = 6 * min(beta_counts)

    certificate = slack_three_cube_coset_coverage_data(p, n)
    lower_bound = int(certificate["admissible_parameter_lower_bound"])
    return {
        "p": p,
        "n": n,
        "domain_index": (p - 1) // n,
        "cube_cosets_hit": len(beta_counts),
        "total_cube_cosets": total_cosets,
        "zero_beta_count": int(beta_ledger["zero_beta_count"]),
        "beta_count": int(beta_ledger["beta_count"]),
        "candidate_beta_count": int(beta_ledger["candidate_beta_count"]),
        "root_count_histogram": beta_ledger["root_count_histogram"],
        "coset_beta_counts": beta_counts,
        "coverage_lower_bound": lower_bound,
        "coverage_certificate": bool(certificate["saturation_certificate"]),
        "uniform_prime_threshold": int(
            certificate["uniform_prime_threshold"]
        ),
        "uniform_threshold_applies": bool(
            certificate["uniform_threshold_applies"]
        ),
        "exact_min_ordered_parameter_count": exact_min_ordered,
        "lower_bound_check": exact_min_ordered >= lower_bound,
    }


def verify_sample(sample: Dict[str, object]) -> Dict[str, object]:
    row = split_cubic_beta_coset_row(int(sample["p"]), int(sample["n"]))
    expected_counts: Sequence[int] = sample["expect_coset_beta_counts"]
    assert row["coverage_certificate"] == sample["expect_certificate"]
    assert row["coverage_lower_bound"] == sample["expect_lower_bound"]
    assert row["uniform_prime_threshold"] == sample[
        "expect_uniform_prime_threshold"
    ]
    assert row["coset_beta_counts"] == tuple(expected_counts)
    assert row["lower_bound_check"]
    if row["uniform_threshold_applies"]:
        assert row["coverage_certificate"]
    if sample["expect_certificate"]:
        assert row["cube_cosets_hit"] == row["total_cube_cosets"]
        assert row["coverage_lower_bound"] > 0
    return {"name": sample["name"], **row}


def verify_uniform_thresholds() -> None:
    expected = {
        1: 226,
        2: 730,
        3: 1522,
        4: 2602,
        8: 9802,
        16: 38026,
        48: 335242,
    }
    observed = {
        denominator: slack_three_cube_coset_uniform_prime_threshold(
            denominator
        )
        for denominator in expected
    }
    assert observed == expected


def main() -> None:
    verify_uniform_thresholds()
    rows: List[Dict[str, object]] = [
        verify_sample(sample)
        for sample in SAMPLES
    ]
    for row in rows:
        print(row)
    print("M1 slack-three cube-coset coverage verifier passed")


if __name__ == "__main__":
    main()
