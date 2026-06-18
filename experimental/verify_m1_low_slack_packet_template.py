#!/usr/bin/env python3
"""Verify the low-slack residual-packet template on tiny scans.

Proof status: AUDIT.

This checks that the scanner's exact support enumeration agrees with the
residual-packet formula, first-nonzero frontier partition, terminal pure-zero
ledger, and positive-dither clearance in representative small cases.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from m1_support_occupancy_scan import scan_supports


CASES: Tuple[Dict[str, object], ...] = (
    {
        "name": "slack-two-depth-three-frontier",
        "params": (13, 12, 3, 2, 2),
        "active_depth": 3,
        "frontier_counts": {"2": 60},
    },
    {
        "name": "slack-two-positive-dither-clearance",
        "params": (13, 12, 5, 2, 2),
        "positive_dither": True,
    },
    {
        "name": "slack-two-terminal-power-cosets",
        "params": (13, 12, 7, 2, 2),
        "active_depth": 1,
        "frontier_counts": {"terminal": 4},
        "terminal_counts": {"3": 4, "4": 0, "5": 0},
    },
    {
        "name": "slack-two-first-nonzero-frontier",
        "params": (13, 12, 8, 2, 2),
        "active_depth": 2,
        "frontier_counts": {"2": 6},
    },
    {
        "name": "slack-three-positive-dither-clearance",
        "params": (13, 12, 4, 3, 2),
        "positive_dither": True,
    },
    {
        "name": "slack-three-active-first-frontier",
        "params": (13, 12, 7, 3, 2),
        "active_depth": 1,
        "terminal_counts": {"4": 0, "5": 0},
    },
)


def require_true(row: Dict[str, object], key: str) -> None:
    assert row[key] is True, (key, row[key])


def normalized_dict(value: Optional[object]) -> Dict[str, int]:
    if value is None:
        return {}
    assert isinstance(value, dict)
    return {str(key): int(count) for key, count in value.items()}


def audit_case(case: Dict[str, object]) -> Dict[str, object]:
    p, n, k, slack, quotient_order = case["params"]
    result = scan_supports(
        p=p,
        n=n,
        k=k,
        slack=slack,
        quotient_order=quotient_order,
        primitive=None,
        anchor_exp=None,
        direction_exp=None,
        max_supports=100000,
        top_histograms=0,
    )

    for key in (
        "canonical_residual_packet_lift_count_check",
        "canonical_residual_packet_slope_consistency_check",
        "canonical_terminal_pure_zero_chain_check",
        "canonical_first_nonzero_frontier_check",
        "canonical_small_residual_depth_gate_check",
    ):
        require_true(result, key)

    expected_active_depth = case.get("active_depth")
    if expected_active_depth is not None:
        assert result["canonical_superboundary_active_depth"] == expected_active_depth

    if case.get("positive_dither"):
        require_true(result, "canonical_positive_dither_clearance_applies")
        require_true(result, "canonical_positive_dither_clearance_check")
        require_true(result, "canonical_positive_dither_finite_prefix_check")

    expected_frontier = case.get("frontier_counts")
    if expected_frontier is not None:
        assert normalized_dict(
            result["canonical_first_nonzero_frontier_packet_counts"]
        ) == expected_frontier

    expected_terminal = case.get("terminal_counts")
    if expected_terminal is not None:
        assert normalized_dict(
            result["canonical_terminal_pure_zero_observed_packet_counts"]
        ) == expected_terminal
        assert normalized_dict(
            result["canonical_terminal_pure_zero_expected_packet_counts"]
        ) == expected_terminal

    return {
        "name": case["name"],
        "params": case["params"],
        "support_count": result["support_count"],
        "bad_slope_count": result["bad_slope_count"],
        "active_depth": result["canonical_superboundary_active_depth"],
        "positive_dither": result[
            "canonical_positive_dither_clearance_applies"
        ],
        "frontier_counts": normalized_dict(
            result["canonical_first_nonzero_frontier_packet_counts"]
        ),
        "terminal_counts": normalized_dict(
            result["canonical_terminal_pure_zero_observed_packet_counts"]
        ),
    }


def main() -> None:
    rows: List[Dict[str, object]] = [
        audit_case(case)
        for case in CASES
    ]
    for row in rows:
        print(row)
    print("M1 low-slack packet-template verifier passed")


if __name__ == "__main__":
    main()
