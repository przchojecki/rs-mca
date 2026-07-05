#!/usr/bin/env python3
"""Replay the Hankel support-lattice accounting packet."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m1" / "hankel_support_lattice_accounting.md"
DUAL_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-dual-distance-frame"
    / "hankel_dual_distance_frame.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-support-lattice-accounting"
    / "hankel_support_lattice_accounting.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "f_support_lattice",
    "dependency": "f_dual_distance_frame",
    "closed_sets": "closed-set lattice",
    "memoization": "Memoizing by this closed state",
    "non_claim": "family-specific polynomial bound",
}


def closure(seed: frozenset[str], supports: list[frozenset[str]]) -> frozenset[str]:
    current = set(seed)
    changed = True
    while changed:
        changed = False
        for support in supports:
            if current.intersection(support) and not support.issubset(current):
                current.update(support)
                changed = True
    return frozenset(current)


def generated_closed_sets(universe: set[str], supports: list[frozenset[str]]) -> list[list[str]]:
    closed: set[frozenset[str]] = {frozenset()}
    for size in range(1, len(universe) + 1):
        for seed in itertools.combinations(sorted(universe), size):
            closed.add(closure(frozenset(seed), supports))
    return [sorted(item) for item in sorted(closed, key=lambda s: (len(s), sorted(s)))]


def toy_check() -> dict[str, object]:
    universe = {"a", "b", "c"}
    supports = [frozenset({"a", "b"}), frozenset({"b", "c"})]
    closed = generated_closed_sets(universe, supports)
    histories = [
        [frozenset({"a", "b"}), frozenset({"b", "c"})],
        [frozenset({"b", "c"}), frozenset({"a", "b"})],
        [frozenset({"a", "b"}), frozenset({"a", "b"})],
    ]
    endpoints = [
        sorted(closure(frozenset().union(*history), supports)) for history in histories
    ]
    dim_budget = 2
    degree_budget = 1
    strict_chain = [[], ["a", "b"], ["a", "b", "c"]]
    return {
        "universe": sorted(universe),
        "supports": [sorted(support) for support in supports],
        "closed_sets": closed,
        "closed_set_count": len(closed),
        "binary_histories": [[sorted(step) for step in history] for history in histories],
        "history_endpoints": endpoints,
        "opposite_histories_memoize_together": endpoints[0] == endpoints[1],
        "repeated_branch_memoizes": endpoints[2] == ["a", "b", "c"],
        "strict_chain_length": len(strict_chain) - 1,
        "chain_budget": dim_budget + degree_budget,
        "chain_bound_holds": len(strict_chain) - 1 <= dim_budget + degree_budget,
    }


def dependency_check() -> dict[str, object]:
    cert = json.loads(DUAL_CERT.read_text(encoding="utf-8"))
    return {
        "path": str(DUAL_CERT.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "accepted": cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == "f_dual_distance_frame",
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "hankel-support-lattice-accounting-v1",
        "status": "PROVED",
        "source_dag_node": "f_support_lattice",
        "dependencies": [dependency_check()],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove a uniform polynomial closed-set bound",
            "does not classify Hankel sparse-dual supports",
        ],
        "note": "experimental/notes/m1/hankel_support_lattice_accounting.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "hankel-support-lattice-accounting-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    for key in [
        "opposite_histories_memoize_together",
        "repeated_branch_memoizes",
        "chain_bound_holds",
    ]:
        if not toy.get(key):
            raise AssertionError(f"failed toy check: {key}")


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
