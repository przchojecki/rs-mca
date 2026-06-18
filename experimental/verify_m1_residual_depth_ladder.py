#!/usr/bin/env python3
"""Audit lossless residual-depth frontier shifts across small ladders.

Proof status: AUDIT / EXPERIMENTAL.

This is a counterexample-first finite check for the M1 residual-depth
mechanism.  It enumerates normalized residual packets of a fixed size and
compares the inherited zero-frontier slice at slack T with the whole catalog at
slack T+1, including exact quotient-lift weights.  A mismatch would refute the
lossless frontier-shift bookkeeping used by the additive-error route.
"""

from __future__ import annotations

import math
from collections import Counter
from itertools import combinations
from typing import Dict, List, Sequence, Tuple, Union

from m1_support_occupancy_scan import (
    elementary_symmetric_prefix,
    expected_residual_packet_lift_count,
)
from mca_slope_scan import make_domain


Packet = Tuple[int, ...]


CaseValue = Union[int, str]


CASES: Tuple[Dict[str, CaseValue], ...] = (
    {
        "name": "full-domain-slack-two-depth-three",
        "p": 13,
        "n": 12,
        "quotient_order": 2,
        "support_size": 5,
        "residual_size": 5,
        "min_slack": 2,
    },
    {
        "name": "full-domain-slack-two-depth-four",
        "p": 17,
        "n": 16,
        "quotient_order": 2,
        "support_size": 6,
        "residual_size": 6,
        "min_slack": 2,
    },
    {
        "name": "one-whole-fiber-lift-weighted",
        "p": 19,
        "n": 18,
        "quotient_order": 3,
        "support_size": 11,
        "residual_size": 5,
        "min_slack": 2,
    },
)


def first_frontier(values: Sequence[int], slack: int, p: int) -> Tuple[str, int]:
    sym = elementary_symmetric_prefix(values, len(values), p)
    for degree in range(slack, len(values)):
        if sym[degree] % p:
            sign = -1 if degree % 2 else 1
            return (str(degree), (sign * sym[degree]) % p)
    return ("terminal", 0)


def touched_fiber_count(
    packet: Packet,
    value_to_index: Dict[int, int],
    quotient_order: int,
) -> int:
    return len({value_to_index[value] % quotient_order for value in packet})


def catalog(
    *,
    p: int,
    domain: Sequence[int],
    value_to_index: Dict[int, int],
    slack: int,
    support_size: int,
    quotient_order: int,
    residual_size: int,
) -> Dict[str, object]:
    fiber_size = len(domain) // quotient_order
    packets_by_frontier: Dict[str, set[Packet]] = {}
    weight_by_frontier: Counter[str] = Counter()
    slope_histograms: Dict[str, Counter[int]] = {}
    packet_weights: Dict[Packet, int] = {}

    other_values = [value for value in domain if value != 1]
    for tail in combinations(other_values, residual_size - 1):
        packet = tuple(sorted((1, *tail)))
        sym = elementary_symmetric_prefix(packet, slack - 1, p)
        if any(sym[degree] % p for degree in range(1, slack)):
            continue

        frontier, slope = first_frontier(packet, slack, p)
        touched = touched_fiber_count(packet, value_to_index, quotient_order)
        weight = expected_residual_packet_lift_count(
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            residual_size=residual_size,
            touched_fibers=touched,
        )
        packets_by_frontier.setdefault(frontier, set()).add(packet)
        weight_by_frontier[frontier] += weight
        slope_histograms.setdefault(frontier, Counter())[slope] += weight
        packet_weights[packet] = weight

    all_packets = (
        set().union(*packets_by_frontier.values())
        if packets_by_frontier
        else set()
    )
    total_weight = sum(packet_weights.values())
    return {
        "slack": slack,
        "depth": residual_size - slack,
        "packet_count": len(all_packets),
        "support_weight": total_weight,
        "frontier_packet_counts": {
            key: len(packets)
            for key, packets in sorted(
                packets_by_frontier.items(),
                key=lambda item: (
                    math.inf if item[0] == "terminal" else int(item[0])
                ),
            )
        },
        "frontier_support_weights": dict(sorted(weight_by_frontier.items())),
        "packets_by_frontier": packets_by_frontier,
        "packet_weights": packet_weights,
        "slope_histograms": slope_histograms,
    }


def inherited_packet_set(row: Dict[str, object]) -> set[Packet]:
    slack_key = str(row["slack"])
    packets_by_frontier = row["packets_by_frontier"]
    assert isinstance(packets_by_frontier, dict)
    inherited: set[Packet] = set()
    for key, packets in packets_by_frontier.items():
        if key == slack_key:
            continue
        inherited.update(packets)
    return inherited


def inherited_weight(row: Dict[str, object]) -> int:
    packets = inherited_packet_set(row)
    weights = row["packet_weights"]
    assert isinstance(weights, dict)
    return sum(int(weights[packet]) for packet in packets)


def inherited_slope_histograms(row: Dict[str, object]) -> Dict[str, Dict[int, int]]:
    slack_key = str(row["slack"])
    histograms = row["slope_histograms"]
    assert isinstance(histograms, dict)
    return {
        key: dict(histogram)
        for key, histogram in histograms.items()
        if key != slack_key
    }


def transition_rows(case: Dict[str, CaseValue]) -> List[Dict[str, object]]:
    p = int(case["p"])
    n = int(case["n"])
    quotient_order = int(case["quotient_order"])
    support_size = int(case["support_size"])
    residual_size = int(case["residual_size"])
    min_slack = int(case["min_slack"])
    _, domain = make_domain(p, n, None)
    value_to_index = {value: index for index, value in enumerate(domain)}

    catalogs = {
        slack: catalog(
            p=p,
            domain=domain,
            value_to_index=value_to_index,
            slack=slack,
            support_size=support_size,
            quotient_order=quotient_order,
            residual_size=residual_size,
        )
        for slack in range(min_slack, residual_size)
    }

    rows: List[Dict[str, object]] = []
    for slack in range(min_slack, residual_size - 1):
        current = catalogs[slack]
        nxt = catalogs[slack + 1]
        current_inherited = inherited_packet_set(current)
        next_packets = nxt["packet_weights"].keys()
        next_packet_set = set(next_packets)
        packet_check = current_inherited == next_packet_set
        weight_check = inherited_weight(current) == int(nxt["support_weight"])
        slope_check = inherited_slope_histograms(current) == {
            key: dict(histogram)
            for key, histogram in nxt["slope_histograms"].items()
        }
        rows.append(
            {
                "case": case["name"],
                "p": p,
                "n": n,
                "quotient_order": quotient_order,
                "support_size": support_size,
                "residual_size": residual_size,
                "shift": f"{slack}->{slack + 1}",
                "current_depth": residual_size - slack,
                "new_frontier_packets": len(
                    current["packets_by_frontier"].get(str(slack), set())
                ),
                "new_frontier_weight": int(
                    current["frontier_support_weights"].get(str(slack), 0)
                ),
                "inherited_packets": len(current_inherited),
                "inherited_weight": inherited_weight(current),
                "next_packets": len(next_packet_set),
                "next_weight": int(nxt["support_weight"]),
                "packet_check": packet_check,
                "weight_check": weight_check,
                "slope_histogram_check": slope_check,
                "current_frontier_packet_counts": current[
                    "frontier_packet_counts"
                ],
                "next_frontier_packet_counts": nxt["frontier_packet_counts"],
            }
        )
    return rows


def main() -> None:
    rows: List[Dict[str, object]] = []
    for case in CASES:
        rows.extend(transition_rows(case))

    for row in rows:
        print(row)
        assert row["packet_check"], row
        assert row["weight_check"], row
        assert row["slope_histogram_check"], row

    print("M1 residual-depth ladder audit passed")


if __name__ == "__main__":
    main()
