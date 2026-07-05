#!/usr/bin/env python3
"""Replay the knife_edge_census assembly packet."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


TARGET_EXP = 128
REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "knife_edge_census.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "knife-edge-census"
    / "knife_edge_census.json"
)
VALUESET_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "certified-valueset-lower"
    / "certified_valueset_lower.json"
)
WINDOW_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "quotient-census-window"
    / "quotient_census_window_compiler.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "knife_edge_census",
    "window": "B(q) in [L, K)",
    "dependency": "certified_valueset_lower -> knife_edge_census",
    "non_claim": "does not count primes inside the residual windows",
}

DEPENDENCY_EDGES = [
    ("census_bounded_scales", "census_exact_counts"),
    ("census_exact_counts", "census_window_arithmetic"),
    ("census_window_arithmetic", "knife_edge_census"),
    ("certified_valueset_lower", "knife_edge_census"),
]


def topological_order(edges: list[tuple[str, str]]) -> list[str]:
    nodes = sorted({node for edge in edges for node in edge})
    indegree = {node: 0 for node in nodes}
    children: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        children[src].append(dst)
        indegree[dst] += 1
    ready = deque(node for node in nodes if indegree[node] == 0)
    order: list[str] = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for child in children[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                ready.append(child)
    if len(order) != len(nodes):
        raise AssertionError("dependency graph has a cycle")
    return order


def classify_budget(budget: int, lower: int, upper: int) -> str:
    if not (0 <= lower <= upper):
        raise ValueError("need 0 <= lower <= upper")
    if budget < lower:
        return "CERTIFIED_BY_LOWER"
    if budget >= upper:
        return "DECIDED_BY_EXACT_UPPER"
    return "UNRESOLVED_WINDOW"


def q_interval(lower: int, upper: int) -> tuple[int, int] | None:
    if not (0 <= lower <= upper):
        raise ValueError("need 0 <= lower <= upper")
    if lower == upper:
        return None
    scale = 2**TARGET_EXP
    return lower * scale, upper * scale - 1


def window_logic_check() -> dict[str, object]:
    lower = 7
    upper = 10
    classified = {
        str(budget): classify_budget(budget, lower, upper)
        for budget in [6, 7, 8, 9, 10, 11]
    }
    expected = {
        "6": "CERTIFIED_BY_LOWER",
        "7": "UNRESOLVED_WINDOW",
        "8": "UNRESOLVED_WINDOW",
        "9": "UNRESOLVED_WINDOW",
        "10": "DECIDED_BY_EXACT_UPPER",
        "11": "DECIDED_BY_EXACT_UPPER",
    }
    if classified != expected:
        raise AssertionError(classified)

    sizes = [upper - candidate_lower for candidate_lower in range(0, upper + 1)]
    if sizes != sorted(sizes, reverse=True):
        raise AssertionError("window sizes are not monotone decreasing")
    if sizes[-1] != 0:
        raise AssertionError("L=K should give an empty window")

    interval = q_interval(lower, upper)
    if interval != (lower * 2**TARGET_EXP, upper * 2**TARGET_EXP - 1):
        raise AssertionError("q interval mismatch")
    if q_interval(upper, upper) is not None:
        raise AssertionError("empty budget window should have no q interval")

    return {
        "sample_lower": lower,
        "sample_upper": upper,
        "sample_classification": classified,
        "monotone_window_sizes": sizes,
        "q_interval_formula": "[L 2^128, K 2^128 - 1]",
        "all_checks_pass": True,
    }


def support_certificate_check() -> dict[str, object]:
    valueset = json.loads(VALUESET_CERT.read_text(encoding="utf-8"))
    window = json.loads(WINDOW_CERT.read_text(encoding="utf-8"))
    return {
        "certified_valueset_lower_exists": VALUESET_CERT.exists(),
        "certified_valueset_lower_status": valueset.get("status"),
        "quotient_window_exists": WINDOW_CERT.exists(),
        "quotient_window_status": window.get("status"),
        "quotient_window_has_census_window_arithmetic": "census_window_arithmetic"
        in window.get("dag_nodes", []),
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "knife-edge-census-v1",
        "status": "PROVED",
        "source_dag_node": "knife_edge_census",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "dependency_subdag": {
            "edges": [[src, dst] for src, dst in DEPENDENCY_EDGES],
            "topological_order": topological_order(DEPENDENCY_EDGES),
            "sink": "knife_edge_census",
        },
        "support_certificates": support_certificate_check(),
        "window_logic_check": window_logic_check(),
        "non_claims": [
            "does not count primes inside residual windows",
            "does not choose deployed v13 row primes",
            "does not replace row-specific certificates",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/knife_edge_census.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert.get("schema") != "knife-edge-census-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "knife_edge_census":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    support = cert["support_certificates"]
    if support.get("certified_valueset_lower_status") != "PROVED":
        raise AssertionError("certified value-set lower packet is not PROVED")
    if not support.get("quotient_window_has_census_window_arithmetic"):
        raise AssertionError("window compiler does not advertise census_window_arithmetic")
    if not cert["window_logic_check"].get("all_checks_pass"):
        raise AssertionError("window logic check failed")
    topological_order([tuple(edge) for edge in cert["dependency_subdag"]["edges"]])


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
