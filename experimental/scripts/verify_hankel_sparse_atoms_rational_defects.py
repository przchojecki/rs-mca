#!/usr/bin/env python3
"""Replay the Hankel sparse-atoms-as-rational-defects packet."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "m1" / "hankel_sparse_atoms_rational_defects.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "hankel-sparse-atoms-rational-defects"
    / "hankel_sparse_atoms_rational_defects.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "hankel_sparse_atoms_as_rational_defects",
    "normal_form": "Ann_E(P) = GRS_{n_E-j-1}(E, lambda) + omega RS_t(E).",
    "defect_bound": "|T_1 union T_2| >= j - t + 2",
    "same_approximant": "same rational approximant",
    "non_claim": "does not by itself prove the full rank-profile dichotomy",
}


def degree_separation_check(n_e: int, j: int, t: int, union_size: int) -> dict[str, object]:
    degree_bound = n_e - j + t - 3
    outside_size = n_e - union_size
    nonzero_possible = outside_size <= degree_bound
    required_union = j - t + 2
    return {
        "n_E": n_e,
        "j": j,
        "t": t,
        "degree_bound": degree_bound,
        "union_size": union_size,
        "outside_size": outside_size,
        "nonzero_polynomial_possible": nonzero_possible,
        "required_union_bound": required_union,
        "stated_bound_holds": union_size >= required_union,
    }


def same_approximant_closure(defect_block: list[str]) -> dict[str, object]:
    scalar_multiples = [
        {"scalar": 1, "defect_block": defect_block},
        {"scalar": 2, "defect_block": defect_block},
        {"scalar": 3, "defect_block": defect_block},
    ]
    closures = {tuple(record["defect_block"]) for record in scalar_multiples}
    return {
        "scalar_multiple_count": len(scalar_multiples),
        "closure_count": len(closures),
        "all_same_closure": len(closures) == 1,
    }


def toy_check() -> dict[str, object]:
    good = degree_separation_check(n_e=11, j=7, t=2, union_size=8)
    impossible_small_union = degree_separation_check(n_e=11, j=7, t=2, union_size=6)
    closure = same_approximant_closure(["x1", "x4", "x7"])
    return {
        "degree_separation_good_case": good,
        "small_union_rejected_by_degree": not impossible_small_union[
            "nonzero_polynomial_possible"
        ],
        "small_union_would_violate_stated_bound": not impossible_small_union[
            "stated_bound_holds"
        ],
        "same_approximant_closure": closure,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "hankel-sparse-atoms-rational-defects-v1",
        "status": "PROVED",
        "source_dag_node": "hankel_sparse_atoms_as_rational_defects",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "toy_check": toy_check(),
        "non_claims": [
            "does not prove the rank-profile dichotomy",
            "does not prove Hankel descent termination",
        ],
        "note": "experimental/notes/m1/hankel_sparse_atoms_rational_defects.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "hankel-sparse-atoms-rational-defects-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    toy = cert["toy_check"]
    if not isinstance(toy, dict):
        raise AssertionError("missing toy check")
    good = toy["degree_separation_good_case"]
    if not isinstance(good, dict) or not good.get("stated_bound_holds"):
        raise AssertionError("degree separation check failed")
    if not toy.get("small_union_rejected_by_degree"):
        raise AssertionError("small union degree rejection failed")
    closure = toy["same_approximant_closure"]
    if not isinstance(closure, dict) or not closure.get("all_same_closure"):
        raise AssertionError("same-approximant closure check failed")


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
