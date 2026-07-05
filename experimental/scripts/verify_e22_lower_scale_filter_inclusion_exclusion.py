#!/usr/bin/env python3
"""Verify the E22 lower-scale filter inclusion-exclusion packet."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / (
    "experimental/data/certificates/e22-lower-scale-filter-inclusion-exclusion/"
    "e22_lower_scale_filter_inclusion_exclusion.json"
)
PROFILE_CERT = ROOT / (
    "experimental/data/certificates/e22-residual-profile-generating-function/"
    "e22_residual_profile_generating_function.json"
)
SCHEMA = "e22-lower-scale-filter-inclusion-exclusion-v1"
DAG_NODE = "e22_lower_scale_filter_inclusion_exclusion"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_certificate() -> dict[str, Any]:
    cert = json.loads(CERT.read_text(encoding="utf-8"))
    require(cert.get("schema") == SCHEMA, "unexpected schema")
    require(cert.get("dag_node") == DAG_NODE, "unexpected DAG node")
    require(cert.get("status") == "PROVED", "status must remain PROVED")
    require(
        cert.get("dependencies") == ["e22_residual_profile_generating_function"],
        "unexpected dependency list",
    )
    dep = json.loads(PROFILE_CERT.read_text(encoding="utf-8"))
    require(dep.get("dag_node") == "e22_residual_profile_generating_function", "bad dependency")
    require(dep.get("status") == "PROVED", "dependency must be PROVED")
    return cert


def powerset(items: Iterable[int]) -> Iterable[tuple[int, ...]]:
    items = list(items)
    for r in range(len(items) + 1):
        yield from combinations(items, r)


def weight(objects: set[int], weights: dict[int, int]) -> int:
    return sum(weights[obj] for obj in objects)


def inclusion_exclusion(
    universe: set[int],
    events: list[set[int]],
    weights: dict[int, int],
) -> int:
    total = 0
    for subset in powerset(range(len(events))):
        if subset:
            intersection = set.intersection(*(events[i] for i in subset))
        else:
            intersection = universe
        total += (-1) ** len(subset) * weight(intersection, weights)
    return total


def verify_weighted_families() -> int:
    universe = set(range(9))
    weights = {i: (i * i + 3 * i + 1) % 7 + 1 for i in universe}
    event_families = [
        [{0, 1, 4, 7}, {2, 4, 6}, {1, 3, 5, 7}],
        [{0, 2, 8}, {0, 1, 2, 3}, {5, 6}, {2, 6, 7, 8}],
    ]
    for events in event_families:
        direct = weight(universe - set.union(*events), weights)
        require(
            inclusion_exclusion(universe, events, weights) == direct,
            "weighted inclusion-exclusion failed",
        )
    return len(event_families)


def main() -> None:
    cert = load_certificate()
    checked = verify_weighted_families()
    require(checked == cert["finite_checks"][0]["event_family_count"], "unexpected check count")
    print(f"PASS: {DAG_NODE} weighted inclusion-exclusion checks passed ({checked} families)")


if __name__ == "__main__":
    main()

