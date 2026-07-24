#!/usr/bin/env python3
"""Independent arithmetic replay for the M31 ten-packet gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-all-weight-source-calibrated-ten-packet-gate-v1/manifest.json"
)


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="ascii"))

    n = 2**21
    K = 2**20
    a = 1_116_023
    R = n - a
    w = a - K
    budget = 16_777_215
    deep = 1_001_282
    degrees = R - w
    shallow = budget - deep
    closure_rhs = shallow - 1

    source_list = 6_796_405
    source_companions = source_list - 1
    quotient_universe = 1_024 - 1
    quotient_size = 544
    maximum_exchange = min(quotient_size, quotient_universe - quotient_size)
    minimum_exchange = ceil_div(w + 1, 2_048)
    positive_exchange_degrees = maximum_exchange - minimum_exchange + 1
    same_degree_floor = ceil_div(
        source_companions, positive_exchange_degrees
    )

    cap9 = closure_rhs - 9 * degrees
    cap10 = closure_rhs - 10 * degrees
    obstruction = source_companions - cap10
    source_slack = cap9 - source_companions

    need((R, w, degrees) == (981_129, 67_447, 913_682), "degree interval")
    need((shallow, closure_rhs) == (15_775_933, 15_775_932), "shallow gate")
    need((minimum_exchange, maximum_exchange) == (33, 479), "source range")
    need(positive_exchange_degrees == 447, "source shell count")
    need(same_degree_floor == 15_205, "source same-degree floor")
    need(cap9 == 7_552_794, "cap nine")
    need(cap10 == 6_639_112, "cap ten")
    need(obstruction == 157_292, "ten obstruction")
    need(source_slack == 756_390, "nine slack")

    gate = data["additive_gate"]
    source = data["fixed_remainder_source"]
    need(gate["legal_exchange_degree_count"] == degrees, "manifest degrees")
    need(gate["forced_shallow_nonanchors"] == shallow, "manifest shallow")
    need(gate["closure_rhs"] == closure_rhs, "manifest rhs")
    need(gate["structured_cap_at_primitive_cap_9"] == cap9, "manifest cap9")
    need(gate["structured_cap_at_primitive_cap_10"] == cap10, "manifest cap10")
    need(gate["source_compatible_primitive_cap_max"] == 9, "manifest max c")
    need(source["same_degree_companion_floor"] == same_degree_floor, "manifest floor")
    need(source["minimum_quotient_exchange"] == minimum_exchange, "manifest minimum")
    need(source["maximum_quotient_exchange"] == maximum_exchange, "manifest maximum")
    need(source["source_floor_slack_at_cap_9"] == source_slack, "manifest slack")
    need(source["cap_10_obstruction_excess"] == obstruction, "manifest obstruction")
    print("independent M31 all-weight ten-packet gate: PASS")


if __name__ == "__main__":
    main()
