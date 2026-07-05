#!/usr/bin/env python3
"""Replay the XR coordinate hypersurface reduction certificate.

This is a logic replay for the determinantal-locus implication:
rank drop is contained in the zero set of every maximal minor; if one cleared
minor is nonzero on a chart, the coordinate-special rank-drop locus is contained
in a proper bounded-degree hypersurface.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "xr-coordinate-hypersurface-reduction"
    / "xr_coordinate_hypersurface_reduction.json"
)


IMPLICATIONS = [
    {
        "input": "xr_triangle_eliminant_form",
        "claim": (
            "The light-triangle normal-form matrix E exists, and rank "
            "stagnation is the vanishing of all 3t x 3t maximal minors."
        ),
        "status": "PROVED",
    },
    {
        "input": "xr_profile_eliminant_nonvanishing",
        "claim": (
            "For the profile, at least one cleared maximal minor Delta is "
            "not the zero polynomial."
        ),
        "status": "PROVED_OR_SUPPLIED_BY_PROFILE_CERTIFICATE",
    },
    {
        "input": "determinantal_locus_logic",
        "claim": (
            "The common zero set of all maximal minors is contained in the "
            "zero set of any chosen maximal minor."
        ),
        "status": "PROVED_FORMALITY",
    },
    {
        "input": "nonzero_polynomial_geometry",
        "claim": (
            "The zero set of a nonzero polynomial on the profile chart is a "
            "proper hypersurface; after denominator clearing, the degree is "
            "bounded by the cleared determinant degree."
        ),
        "status": "PROVED_FORMALITY",
    },
]


def build_certificate() -> dict[str, Any]:
    cert = {
        "schema": "xr-coordinate-hypersurface-reduction-v1",
        "status": "PROVED_REDUCTION",
        "source_dag_node": "xr_coordinate_hypersurface_reduction",
        "depends_on": [
            "xr_triangle_eliminant_form",
            "xr_profile_eliminant_nonvanishing",
        ],
        "implications": IMPLICATIONS,
        "conclusion": (
            "Inside any light profile chart with a nonzero cleared maximal "
            "minor Delta, the coordinate-special rank-stagnation locus is "
            "contained in the proper hypersurface Delta=0."
        ),
        "degree_bound": (
            "degree(Delta) after clearing chart denominators; fixed by the "
            "printed chart and chosen maximal minor"
        ),
        "non_claims": [
            "does not count points on the hypersurface",
            "does not produce an adjacent deployed upper certificate",
            "does not replace the staircase/SPI/XR rationing input",
        ],
        "note": "experimental/notes/m1/xr_coordinate_hypersurface_reduction.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "xr-coordinate-hypersurface-reduction-v1":
        raise AssertionError("unexpected schema")
    if cert["status"] != "PROVED_REDUCTION":
        raise AssertionError("unexpected status")
    required = {"xr_triangle_eliminant_form", "xr_profile_eliminant_nonvanishing"}
    if set(cert["depends_on"]) != required:
        raise AssertionError("dependency set mismatch")
    claims = {item["input"]: item for item in cert["implications"]}
    for item in required | {"determinantal_locus_logic", "nonzero_polynomial_geometry"}:
        if item not in claims:
            raise AssertionError(f"missing implication: {item}")
    if "Delta=0" not in cert["conclusion"]:
        raise AssertionError("conclusion does not name the hypersurface")
    if not cert["non_claims"]:
        raise AssertionError("non-claims must be explicit")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("xr-coordinate-hypersurface reduction certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    print("  dependencies:")
    for dep in cert["depends_on"]:
        print(f"    - {dep}")
    print(f"  conclusion: {cert['conclusion']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text())
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
