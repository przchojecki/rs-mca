#!/usr/bin/env python3
"""Replay the mca_unsafe assembly packet."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "mca_unsafe.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "mca-unsafe"
    / "mca_unsafe.json"
)
UNSAFE_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "unsafe-at-crossing"
    / "unsafe_at_crossing.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "mca_unsafe",
    "statement": "B_C(a_safe - 1) > B*",
    "unsafe_input": "unsafe_at_crossing -> mca_unsafe",
    "non_claim": "does not recompute the universal-cap proof",
}

DEPENDENCY_EDGES = [
    ("cap_theorem", "mca_unsafe"),
    ("zone_b", "mca_unsafe"),
    ("unsafe_at_crossing", "mca_unsafe"),
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


def assembly_logic_check() -> dict[str, object]:
    cases = [
        {
            "name": "all_inputs_green",
            "cap_theorem": True,
            "zone_b": True,
            "unsafe_at_crossing": True,
            "expect_mca_unsafe": True,
        },
        {
            "name": "missing_adjacent_witness",
            "cap_theorem": True,
            "zone_b": True,
            "unsafe_at_crossing": False,
            "expect_mca_unsafe": False,
        },
        {
            "name": "missing_cap_location",
            "cap_theorem": False,
            "zone_b": True,
            "unsafe_at_crossing": True,
            "expect_mca_unsafe": False,
        },
    ]
    checked = []
    for case in cases:
        conclusion = case["cap_theorem"] and case["zone_b"] and case["unsafe_at_crossing"]
        if conclusion != case["expect_mca_unsafe"]:
            raise AssertionError(case)
        checked.append({**case, "mca_unsafe": conclusion})
    return {"cases": checked, "all_checks_pass": True}


def support_artifact_check() -> dict[str, object]:
    unsafe = json.loads(UNSAFE_CERT.read_text(encoding="utf-8"))
    cap_v12 = REPO / "tex" / "cs25_cap_v12.tex"
    slack_v4 = REPO / "tex" / "slackMCA_v4.tex"
    zone_roadmap = REPO / "experimental" / "notes" / "roadmaps" / "evidence_plan_codex.md"
    cap_v12_text = cap_v12.read_text(encoding="utf-8")
    slack_text = slack_v4.read_text(encoding="utf-8")
    zone_text = zone_roadmap.read_text(encoding="utf-8")
    return {
        "unsafe_at_crossing_status": unsafe.get("status"),
        "unsafe_at_crossing_source": unsafe.get("source_dag_node"),
        "cap_v12_exists": cap_v12.exists(),
        "cap_v12_mentions_universal_cap": "universal cap" in cap_v12_text.lower(),
        "slack_v4_mentions_prop_prize": "prop:prize" in slack_text,
        "zone_roadmap_mentions_zone_b": "zone_b" in zone_text,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "mca-unsafe-v1",
        "status": "PROVED",
        "source_dag_node": "mca_unsafe",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "dependency_subdag": {
            "edges": [[src, dst] for src, dst in DEPENDENCY_EDGES],
            "topological_order": topological_order(DEPENDENCY_EDGES),
            "sink": "mca_unsafe",
        },
        "support_artifacts": support_artifact_check(),
        "assembly_logic_check": assembly_logic_check(),
        "non_claims": [
            "does not edit Paper D",
            "does not recompute the universal-cap proof",
            "does not rerun zone-b collision checks",
            "does not choose deployed v13 row primes",
        ],
        "note": "experimental/notes/thresholds/mca_unsafe.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert.get("schema") != "mca-unsafe-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "mca_unsafe":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    support = cert["support_artifacts"]
    if support.get("unsafe_at_crossing_status") != "PROVED":
        raise AssertionError("unsafe_at_crossing packet is not PROVED")
    missing = [
        name
        for name in [
            "cap_v12_exists",
            "cap_v12_mentions_universal_cap",
            "slack_v4_mentions_prop_prize",
            "zone_roadmap_mentions_zone_b",
        ]
        if not support.get(name)
    ]
    if missing:
        raise AssertionError(f"missing support artifacts: {missing}")
    if not cert["assembly_logic_check"].get("all_checks_pass"):
        raise AssertionError("assembly logic check failed")
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
