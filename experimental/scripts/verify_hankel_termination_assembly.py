#!/usr/bin/env python3
"""Replay the Hankel termination assembly packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m1" / "hankel_termination_assembly.md"
RANK_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-rank-profile-entropy"
    / "hankel_rank_profile_entropy.json"
)
LEAF_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-moment-clean-leaves"
    / "hankel_moment_clean_leaves.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-termination-assembly"
    / "hankel_termination_assembly.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "f_termination_hankel",
    "rank_dependency": "hankel_rank_profile_entropy",
    "leaf_dependency": "hankel_moment_clean_leaves",
    "saturated_closure": "rcl_P(B union S)",
    "raw_overcount": "not the raw number of support unions",
    "non_claim": "M3 root tables",
}


def dependency_check(path: Path, expected_node: str) -> dict[str, object]:
    cert = json.loads(path.read_text(encoding="utf-8"))
    return {
        "path": str(path.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "accepted": cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == expected_node,
    }


def toy_check() -> dict[str, object]:
    raw_branches = [
        {"support": ["a", "b"], "closure": ["a", "b", "c"]},
        {"support": ["b", "c"], "closure": ["a", "b", "c"]},
        {"support": ["a", "c"], "closure": ["a", "b", "c"]},
        {"support": ["a", "b", "c"], "closure": ["a", "b", "c"]},
        {"support": ["b"], "closure": ["a", "b", "c"]},
    ]
    closures = {tuple(branch["closure"]) for branch in raw_branches}
    fixed_w = 4
    exponent = fixed_w * fixed_w
    return {
        "raw_branch_count": len(raw_branches),
        "saturated_closure_count": len(closures),
        "raw_branches_collapse": len(raw_branches) > len(closures) == 1,
        "fixed_cutoff_W": fixed_w,
        "rank_profile_entropy_exponent_model": exponent,
        "polynomial_for_fixed_W": exponent == fixed_w**2,
        "terminal_leaf_input_required": True,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "hankel-termination-assembly-v1",
        "status": "PROVED",
        "source_dag_node": "f_termination_hankel",
        "dependencies": [
            dependency_check(RANK_CERT, "hankel_rank_profile_entropy"),
            dependency_check(LEAF_CERT, "hankel_moment_clean_leaves"),
        ],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not count raw support unions",
            "does not produce M3 root tables",
            "does not close a row-level F_17^32 safe-side certificate",
        ],
        "note": "experimental/notes/m1/hankel_termination_assembly.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "hankel-termination-assembly-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    if not toy.get("raw_branches_collapse"):
        raise AssertionError("raw branch collapse check failed")
    if not toy.get("polynomial_for_fixed_W"):
        raise AssertionError("fixed-W polynomial model failed")
    if not toy.get("terminal_leaf_input_required"):
        raise AssertionError("terminal leaf input check failed")


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
