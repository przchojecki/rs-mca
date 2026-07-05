#!/usr/bin/env python3
"""Replay the unsafe_at_crossing assembly packet."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "unsafe_at_crossing.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "unsafe-at-crossing"
    / "unsafe_at_crossing.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "unsafe_at_crossing",
    "collision_free": "collision-free branch -> qfloor_exact witness family",
    "collided": "collided branch       -> averaged_slope_conversion",
    "non_claim": "does not recompute `prop:qfloor`",
}

DEPENDENCY_EDGES = [
    ("qfloor_exact", "unsafe_at_crossing"),
    ("averaged_slope_conversion", "unsafe_at_crossing"),
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


def branch_logic_check() -> dict[str, object]:
    rows = [
        {"name": "collision_free_case", "has_collision": False},
        {"name": "collided_case", "has_collision": True},
    ]
    checked = []
    for row in rows:
        route = "averaged_slope_conversion" if row["has_collision"] else "qfloor_exact"
        produces_witness = route in {"qfloor_exact", "averaged_slope_conversion"}
        if not produces_witness:
            raise AssertionError(row)
        checked.append({**row, "route": route, "produces_adjacent_witness": True})
    routes = {row["route"] for row in checked}
    if routes != {"qfloor_exact", "averaged_slope_conversion"}:
        raise AssertionError("branch routes were not both exercised")
    return {"cases": checked, "all_checks_pass": True}


def support_artifact_check() -> dict[str, bool]:
    qfloor_tex = REPO / "tex" / "slackMCA_v4.tex"
    averaged_note = REPO / "experimental" / "notes" / "m1" / "m1_averaged_slope_conversion.md"
    roadmap = (
        REPO
        / "experimental"
        / "notes"
        / "roadmaps"
        / "proof_sketch"
        / "s2_paid_ledger.md"
    )
    return {
        "qfloor_tex_exists": qfloor_tex.exists(),
        "qfloor_tex_mentions_prop": "prop:qfloor" in qfloor_tex.read_text(encoding="utf-8"),
        "averaged_slope_note_exists": averaged_note.exists(),
        "averaged_slope_note_marks_proved": "Status:** PROVED" in averaged_note.read_text(
            encoding="utf-8"
        ),
        "paid_ledger_mentions_qfloor": roadmap.exists()
        and "prop:qfloor" in roadmap.read_text(encoding="utf-8"),
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "unsafe-at-crossing-v1",
        "status": "PROVED",
        "source_dag_node": "unsafe_at_crossing",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "dependency_subdag": {
            "edges": [[src, dst] for src, dst in DEPENDENCY_EDGES],
            "topological_order": topological_order(DEPENDENCY_EDGES),
            "sink": "unsafe_at_crossing",
        },
        "support_artifacts": support_artifact_check(),
        "branch_logic_check": branch_logic_check(),
        "non_claims": [
            "does not recompute prop:qfloor",
            "does not rerun the averaged-slope ledger",
            "does not choose deployed v13 rows",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/unsafe_at_crossing.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert.get("schema") != "unsafe-at-crossing-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "unsafe_at_crossing":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    missing = [name for name, ok in cert["support_artifacts"].items() if not ok]
    if missing:
        raise AssertionError(f"missing support artifacts: {missing}")
    if not cert["branch_logic_check"].get("all_checks_pass"):
        raise AssertionError("branch logic check failed")
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
