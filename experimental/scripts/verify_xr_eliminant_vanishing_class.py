#!/usr/bin/env python3
"""Replay the XR eliminant-vanishing class reduction.

This certificate composes the XR light-profile nonvanishing packet with the
coordinate hypersurface reduction.  It verifies the dependency logic and keeps
the remaining hypersurface population problem explicit.
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
    / "xr-eliminant-vanishing-class"
    / "xr_eliminant_vanishing_class.json"
)


DEPENDENCIES = [
    "xr_profile_eliminant_nonvanishing",
    "xr_coordinate_hypersurface_reduction",
]


def build_certificate() -> dict[str, Any]:
    cert = {
        "schema": "xr-eliminant-vanishing-class-v1",
        "status": "PROVED_REDUCTION",
        "source_dag_node": "xr_eliminant_vanishing_class",
        "depends_on": DEPENDENCIES,
        "implication": [
            {
                "from": "xr_profile_eliminant_nonvanishing",
                "to": "no unpaid light profile has identically vanishing eliminant",
            },
            {
                "from": "xr_coordinate_hypersurface_reduction",
                "to": (
                    "coordinate-special stagnation in a nonzero profile lies "
                    "on a proper bounded-degree hypersurface"
                ),
            },
        ],
        "conclusion": (
            "The identically vanishing light-profile class is removed; the "
            "remaining branch is hypersurface population/rationing."
        ),
        "remaining_named_input": "staircase/SPI/XR hypersurface rationing",
        "non_claims": [
            "does not count points on the hypersurface",
            "does not prove the full XR light-triangle residual",
            "does not produce an adjacent deployed upper certificate",
        ],
        "note": "experimental/notes/m1/xr_eliminant_vanishing_class.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "xr-eliminant-vanishing-class-v1":
        raise AssertionError("unexpected schema")
    if cert["status"] != "PROVED_REDUCTION":
        raise AssertionError("unexpected status")
    if cert["depends_on"] != DEPENDENCIES:
        raise AssertionError("dependency order changed")
    if "identically vanishing" not in cert["conclusion"]:
        raise AssertionError("conclusion must remove the old class")
    if "hypersurface" not in cert["remaining_named_input"].lower():
        raise AssertionError("remaining input must name hypersurface rationing")
    if len(cert["non_claims"]) < 3:
        raise AssertionError("non-claims are incomplete")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("xr-eliminant-vanishing-class certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    print("  dependencies:")
    for dep in cert["depends_on"]:
        print(f"    - {dep}")
    print(f"  remaining input: {cert['remaining_named_input']}")


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
