#!/usr/bin/env python3
"""Verify the deep_point packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/deep-point/deep_point.json")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.deep_point.v1",
        "status": "PROVED",
        "source_dag_node": "deep_point",
        "verdict": "bad_slope_vectors_equal_deep_point_images_for_simple_pole_lines",
        "identities": {
            "base": (
                "Bad_CA(f_alpha,g_alpha;delta_a) = Bad_MCA(f_alpha,g_alpha;delta_a) "
                "= {P(alpha): deg(P)<k+1 and P agrees with U on >=a points}"
            ),
            "interleaved": (
                "BadVec(alpha;a) = {(P_1(alpha),...,P_mu(alpha)): each deg(P_i)<k+1 "
                "and all P_i agree with U_i on a common >=a support}"
            ),
        },
        "bridge_scope": {
            "line_shape": "f_alpha(x)=U(x)/(x-alpha), g_alpha(x)=-1/(x-alpha)",
            "deep_point_condition": "alpha notin D",
            "direction": "forward list-to-bad-slope bridge",
            "object": "support/column-distance agreement",
        },
        "upstream_evidence": [
            "experimental/notes/x1/x1_deep_point_interleaved_bridge.md",
            "experimental/scripts/verify_x1_deep_point_identity.py",
            "experimental/scripts/verify_x1_interleaved_deep_point.py",
        ],
        "consumers": ["codegree"],
        "non_claims": [
            "does not prove list_safe",
            "does not prove a deployed adjacent upper certificate",
            "does not prove full list-to-MCA equivalence outside the simple-pole bridge",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require("Bad_CA" in cert["identities"]["base"], "base identity missing Bad_CA")
    require("BadVec" in cert["identities"]["interleaved"], "interleaved identity missing BadVec")
    require(cert["bridge_scope"]["deep_point_condition"] == "alpha notin D", "deep point condition mismatch")
    require(cert["consumers"] == ["codegree"], "consumer list mismatch")


def emit_certificate(path: Path, cert: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", nargs="?", const=CERT_PATH, type=Path)
    parser.add_argument("--check", nargs="?", const=CERT_PATH, type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit is not None:
        emit_certificate(args.emit, cert)
        print(f"WROTE: {args.emit}")
    if args.check is not None:
        loaded = json.loads(args.check.read_text())
        validate_certificate(loaded)
        print(f"PASS: certificate matches {args.check}")
    if args.emit is None and args.check is None:
        validate_certificate(cert)
        print("PASS: deep_point packet")


if __name__ == "__main__":
    main()
