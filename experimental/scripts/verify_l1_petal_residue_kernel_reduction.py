#!/usr/bin/env python3
"""Replay the L1 petal residue-kernel reduction dependency packet.

This is a logic/certificate checker, not an algebraic search.  It freezes the
proved local reductions and verifies that the only live mathematical payload is
the actual squarefree classification ledger.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


DEFAULT_CERT = Path(
    "experimental/data/certificates/l1-petal-residue-kernel-reduction/"
    "l1_petal_residue_kernel_reduction.json"
)

PROVED = "PROVED"
CONDITIONAL = "CONDITIONAL_ON_LEDGER"
TARGET = "TARGET_PAYLOAD"


NODES: dict[str, dict[str, Any]] = {
    "petal_residue_kernel_linear_bound": {
        "status": PROVED,
        "claim": "Lemma 13 supplies dim K_{I,d} <= c + 1.",
        "source": "l1_full_list_quotient_proof_program.md Lemma 13",
    },
    "petal_realizable_kernel_injection": {
        "status": PROVED,
        "claim": (
            "Exact realizable full-petal extras inject into squarefree "
            "locator points in K_{I,d}."
        ),
        "source": "Lemma 8 plus l1_coset_chart_residue_bridge_v1.md",
    },
    "petal_squarefree_classification_counting_soundness": {
        "status": PROVED,
        "claim": (
            "A finite charged/uncharged classification with c-independent "
            "exponents gives a c-independent polynomial bound."
        ),
        "source": "finite union counting",
    },
    "petal_squarefree_classification_ledger_soundness": {
        "status": PROVED,
        "claim": (
            "A complete ledger with paid charged records and bounded "
            "uncharged records implies the squarefree classification payload."
        ),
        "source": "ledger semantics",
    },
    "petal_squarefree_classification_ledger_payload": {
        "status": TARGET,
        "claim": (
            "Construct the actual classification ledger for squarefree "
            "realizable locator points in residue-line kernels."
        ),
        "source": "remaining L1 residual task",
    },
    "petal_squarefree_kernel_classification_payload": {
        "status": CONDITIONAL,
        "claim": "The charged/uncharged squarefree-kernel classification holds.",
    },
    "petal_kernel_realizable_sparsity": {
        "status": CONDITIONAL,
        "claim": (
            "Squarefree realizable locator points in K_{I,d} are uniformly "
            "polynomial in the growing-excess corridor."
        ),
    },
    "petal_realizable_extra_uniformity": {
        "status": CONDITIONAL,
        "claim": (
            "Exact realizable full-petal extras are uniformly polynomial "
            "through the injection into squarefree kernel points."
        ),
    },
    "petal_residue_line_uniformity": {
        "status": CONDITIONAL,
        "claim": (
            "The residue-line contribution is uniformly bounded using the "
            "linear ambient ceiling and realizable-extra uniformity."
        ),
    },
    "petal_mixed_amplification_step": {
        "status": CONDITIONAL,
        "claim": (
            "Residue-line uniformity gives the c -> c+1 mixed-amplification "
            "transition with c-independent polynomial exponents."
        ),
    },
}


EDGES = [
    (
        "petal_squarefree_classification_ledger_payload",
        "petal_squarefree_kernel_classification_payload",
    ),
    (
        "petal_squarefree_classification_ledger_soundness",
        "petal_squarefree_kernel_classification_payload",
    ),
    (
        "petal_squarefree_kernel_classification_payload",
        "petal_kernel_realizable_sparsity",
    ),
    (
        "petal_squarefree_classification_counting_soundness",
        "petal_kernel_realizable_sparsity",
    ),
    ("petal_kernel_realizable_sparsity", "petal_realizable_extra_uniformity"),
    ("petal_realizable_kernel_injection", "petal_realizable_extra_uniformity"),
    ("petal_realizable_extra_uniformity", "petal_residue_line_uniformity"),
    ("petal_residue_kernel_linear_bound", "petal_residue_line_uniformity"),
    ("petal_residue_line_uniformity", "petal_mixed_amplification_step"),
]


CONDITIONAL_NODES = {
    "petal_squarefree_kernel_classification_payload",
    "petal_kernel_realizable_sparsity",
    "petal_realizable_extra_uniformity",
    "petal_residue_line_uniformity",
    "petal_mixed_amplification_step",
}


def topological_order(nodes: dict[str, dict[str, Any]], edges: list[tuple[str, str]]) -> list[str]:
    indegree = {node: 0 for node in nodes}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        if src not in nodes:
            raise AssertionError(f"unknown source node: {src}")
        if dst not in nodes:
            raise AssertionError(f"unknown target node: {dst}")
        outgoing[src].append(dst)
        indegree[dst] += 1

    ready = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    order = []
    while ready:
        node = ready.popleft()
        order.append(node)
        for dst in sorted(outgoing[node]):
            indegree[dst] -= 1
            if indegree[dst] == 0:
                ready.append(dst)

    if len(order) != len(nodes):
        raise AssertionError("dependency graph is cyclic")
    return order


def dependencies(edges: list[tuple[str, str]]) -> dict[str, list[str]]:
    deps: dict[str, list[str]] = defaultdict(list)
    for src, dst in edges:
        deps[dst].append(src)
    return {node: sorted(values) for node, values in deps.items()}


def validate_certificate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "l1-petal-residue-kernel-reduction-v1":
        raise AssertionError("unexpected schema")
    nodes = cert["nodes"]
    edges = [tuple(edge) for edge in cert["edges"]]
    order = topological_order(nodes, edges)
    if order != cert["topological_order"]:
        raise AssertionError("topological order mismatch")

    live = cert["live_payload_assumptions"]
    if live != ["petal_squarefree_classification_ledger_payload"]:
        raise AssertionError("unexpected live payload assumptions")

    for node, data in nodes.items():
        status = data["status"]
        if status == CONDITIONAL and node not in CONDITIONAL_NODES:
            raise AssertionError(f"unexpected conditional node: {node}")
        if node in CONDITIONAL_NODES and status != CONDITIONAL:
            raise AssertionError(f"conditional node has wrong status: {node}")
        if status == TARGET and node not in live:
            raise AssertionError(f"target payload not listed live: {node}")
        if status == PROVED and node in live:
            raise AssertionError(f"live payload cannot be proved: {node}")

    deps = dependencies(edges)
    for node in CONDITIONAL_NODES:
        if not deps.get(node):
            raise AssertionError(f"conditional node has no dependencies: {node}")


def build_certificate() -> dict[str, Any]:
    order = topological_order(NODES, EDGES)
    json_edges = [[src, dst] for src, dst in EDGES]
    cert = {
        "schema": "l1-petal-residue-kernel-reduction-v1",
        "status": "CONDITIONAL_ON_SQUAREFREE_CLASSIFICATION_LEDGER",
        "agents_md_priority": (
            "Highest-value item 4: primitive L1 image-fiber theorem and "
            "mixed-petal/growing-defect residuals."
        ),
        "note": "experimental/notes/l1/l1_petal_residue_kernel_reduction.md",
        "nodes": NODES,
        "edges": json_edges,
        "topological_order": order,
        "live_payload_assumptions": ["petal_squarefree_classification_ledger_payload"],
        "non_claims": [
            "does not construct the squarefree classification ledger",
            "does not close the primitive image-fiber theorem",
            "does not claim ambient residue-kernel flatness",
            "does not replace the fixed-excess compiler",
        ],
    }
    validate_certificate(cert)
    return cert


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("l1-petal-residue-kernel reduction certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    print("  live payloads:")
    for item in cert["live_payload_assumptions"]:
        print(f"    - {item}")
    print("  topological order:")
    for item in cert["topological_order"]:
        print(f"    - {item}: {cert['nodes'][item]['status']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        DEFAULT_CERT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_CERT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {DEFAULT_CERT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        validate_certificate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
