#!/usr/bin/env python3
"""Replay the certified_valueset_lower assembly packet."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "certified_valueset_lower.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "certified-valueset-lower"
    / "certified_valueset_lower.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "certified_valueset_lower",
    "injective_family": "|F| > B*",
    "generator_route": "Generator-design route",
    "lattice_route": "Alternative lattice route",
    "non_claim": "does not run lattice enumeration",
}

DEPENDENCY_EDGES = [
    ("graded_collision_radius", "certified_valueset_lower"),
    ("far_pair_separation", "certified_valueset_lower"),
    ("certifier_uniformity", "certified_valueset_lower"),
    ("kernel_lattice_reframing", "lattice_cone_certificate"),
    ("weight_graded_mitm", "lattice_cone_certificate"),
    ("integer_code_distance_cert", "lattice_cone_certificate"),
    ("lattice_cone_certificate", "certified_valueset_lower"),
    ("lattice_cone_certificate", "certifier_uniformity"),
]

GREEN_INPUTS = [
    "graded_collision_radius",
    "far_pair_separation",
    "certifier_uniformity",
    "kernel_lattice_reframing",
    "weight_graded_mitm",
    "integer_code_distance_cert",
    "lattice_cone_certificate",
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


def injection_logic_check() -> dict[str, object]:
    cases = [
        {
            "name": "accepted_distinct_family",
            "budget": 4,
            "values": [0, 3, 7, 11, 18],
            "expect_proves_lower": True,
        },
        {
            "name": "rejected_collision_family",
            "budget": 4,
            "values": [0, 3, 7, 11, 11],
            "expect_proves_lower": False,
        },
        {
            "name": "rejected_small_distinct_family",
            "budget": 5,
            "values": [0, 3, 7, 11, 18],
            "expect_proves_lower": False,
        },
    ]
    checked = []
    for case in cases:
        values = case["values"]
        family_size = len(values)
        image_size = len(set(values))
        proves_lower = family_size == image_size and image_size > case["budget"]
        if proves_lower != case["expect_proves_lower"]:
            raise AssertionError(case)
        checked.append(
            {
                "name": case["name"],
                "family_size": family_size,
                "image_size": image_size,
                "budget": case["budget"],
                "proves_lower": proves_lower,
            }
        )
    return {"cases": checked, "all_checks_pass": True}


def support_artifact_check() -> dict[str, bool]:
    paths = {
        "graded_collision_radius_note": REPO
        / "experimental"
        / "notes"
        / "thresholds"
        / "graded_collision_radius.md",
        "graded_collision_radius_certificate": REPO
        / "experimental"
        / "data"
        / "certificates"
        / "graded-collision-radius"
        / "graded_collision_radius.json",
        "cluster_certificates_note": REPO
        / "experimental"
        / "notes"
        / "thresholds"
        / "cluster_certificates.md",
        "cluster_certificates_certificate": REPO
        / "experimental"
        / "data"
        / "certificates"
        / "cluster-certificates"
        / "cluster_certificates.json",
        "certifier_pipeline_toy_certificate": REPO
        / "experimental"
        / "data"
        / "certificates"
        / "c4-certifier-pipeline-toy"
        / "c4_certifier_pipeline_toy.json",
    }
    return {name: path.exists() for name, path in paths.items()}


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    order = topological_order(DEPENDENCY_EDGES)
    cert = {
        "schema": "certified-valueset-lower-v1",
        "status": "PROVED",
        "source_dag_node": "certified_valueset_lower",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "dependency_subdag": {
            "edges": [[src, dst] for src, dst in DEPENDENCY_EDGES],
            "topological_order": order,
            "green_inputs": GREEN_INPUTS,
            "sink": "certified_valueset_lower",
        },
        "support_artifacts": support_artifact_check(),
        "injection_logic_check": injection_logic_check(),
        "non_claims": [
            "does not print a deployed row family",
            "does not run lattice enumeration",
            "does not count primes inside census windows",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/certified_valueset_lower.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert.get("schema") != "certified-valueset-lower-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "certified_valueset_lower":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    missing = [name for name, ok in cert["support_artifacts"].items() if not ok]
    if missing:
        raise AssertionError(f"missing support artifacts: {missing}")
    if not cert["injection_logic_check"].get("all_checks_pass"):
        raise AssertionError("injection logic check failed")
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
