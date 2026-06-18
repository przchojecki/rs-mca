#!/usr/bin/env python3
"""Verify the M1 residual-depth frontier shift in small audited cases.

Proof status: AUDIT.

The algebraic shift is c_{T,d}=0 iff the same packet lies in the
depth-(d-1) catalog at slack T+1. This verifier checks the first implemented
d=2 ledger by comparing the second-superboundary zero-slope catalog with the
next-slack first-superboundary catalog, including exact-support lift weights.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from m1_support_occupancy_scan import second_superboundary_shape_coset_ledger
from mca_slope_scan import make_domain


CASES: Tuple[Tuple[int, int, int, int, int, str], ...] = (
    # Slack two, active lift gate, small full-domain quotient.
    (17, 16, 2, 8, 12, "slack-two-active-full-domain"),
    # Slack two, active lift gate, proper lift-window sample.
    (97, 48, 2, 8, 20, "slack-two-active-proper-window"),
    # Slack two, inactive lift gate; parameters still match, active counts vanish.
    (97, 48, 2, 8, 21, "slack-two-inactive-lift-gate"),
    # Slack three, active lift gate for the next fixed-template layer.
    (41, 20, 3, 10, 15, "slack-three-active"),
    # Slack three, inactive lift gate.
    (41, 20, 3, 10, 14, "slack-three-inactive-lift-gate"),
)


def transition_row(
    p: int,
    n: int,
    slack: int,
    fiber_size: int,
    support_size: int,
    name: str,
) -> Dict[str, object]:
    quotient_order = n // fiber_size
    _, domain = make_domain(p, n, None)
    ledger = second_superboundary_shape_coset_ledger(
        p=p,
        domain=domain,
        slack=slack,
        support_size=support_size,
        quotient_order=quotient_order,
        fiber_size=fiber_size,
    )
    checks = (
        bool(ledger["next_slack_transition_parameter_check"]),
        bool(ledger["next_slack_transition_active_parameter_check"]),
        bool(ledger["next_slack_transition_packet_count_check"]),
        bool(ledger["next_slack_transition_support_count_check"]),
    )
    assert all(checks)
    return {
        "name": name,
        "p": p,
        "n": n,
        "slack": slack,
        "support_size": support_size,
        "quotient_order": quotient_order,
        "fiber_size": fiber_size,
        "zero_parameters": int(ledger["zero_parameter_count"]),
        "next_slack_parameters": int(
            ledger["next_slack_first_parameter_count"]
        ),
        "active_zero_parameters": int(ledger["active_zero_parameter_count"]),
        "next_slack_active_parameters": int(
            ledger["next_slack_first_active_parameter_count"]
        ),
        "zero_packets": int(ledger["zero_packet_count"]),
        "next_slack_packets": int(ledger["next_slack_first_packet_count"]),
        "zero_support_weight": int(ledger["zero_weighted_support_count"]),
        "next_slack_support_weight": int(
            ledger["next_slack_first_weighted_support_count"]
        ),
    }


def main() -> None:
    rows: List[Dict[str, object]] = [
        transition_row(*case)
        for case in CASES
    ]
    for row in rows:
        print(row)
    print("M1 residual-depth frontier shift verifier passed")


if __name__ == "__main__":
    main()
