#!/usr/bin/env python3
"""Verify the axis9_dither exact-rate certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/axis9-dither/axis9_dither.json")

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "rho(C) := k/|L|",
    "one of 1/2, 1/4, 1/8, 1/16",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.axis9_dither.v1",
        "status": "PROVED",
        "source_dag_node": "axis9_dither",
        "verdict": "exact_rates_no_implicit_dither",
        "source": {
            "artifact": "abf26.pdf",
            "description": (
                "Arnon-Boneh-Fenzi, Open Problems in List Decoding and "
                "Correlated Agreement"
            ),
            "source_id": "IACR ePrint 2026/680",
            "page": 5,
            "sha256": EXPECTED_SHA,
        },
        "quote_fragments": REQUIRED_FRAGMENTS,
        "official_rates": ["1/2", "1/4", "1/8", "1/16"],
        "claim": (
            "The official rows use the printed exact rate set. Dimension "
            "dither is therefore an experimental or protocol-specific variant, "
            "not an implicit way to remove dyadic quotient structure from the "
            "official proof obligation."
        ),
        "ledger_consequence": {
            "official_row_shape": "k = rho n with rho in {1/2,1/4,1/8,1/16}",
            "dithered_row_status": "not official unless separately declared",
            "proof_obligation": "price active dyadic quotient cores at exact rates",
        },
        "non_claims": [
            "does not prove dithered rows are useless",
            "does not forbid protocol-design dither experiments",
            "does not change quotient-profile counts",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    missing = sorted(set(REQUIRED_FRAGMENTS) - set(cert["quote_fragments"]))
    require(not missing, "missing quote fragments: " + ", ".join(missing))
    require(cert["official_rates"] == ["1/2", "1/4", "1/8", "1/16"], "rate set mismatch")
    require("no_implicit_dither" in cert["verdict"], "verdict must reject implicit dither")


def emit_certificate(path: Path, cert: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", nargs="?", const=CERT_PATH, type=Path)
    parser.add_argument("--check", nargs="?", const=CERT_PATH, type=Path)
    parser.add_argument("--pdf", type=Path, help="Optional ABF26 PDF to hash-check")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit is not None:
        emit_certificate(args.emit, cert)
        print(f"WROTE: {args.emit}")
    if args.check is not None:
        loaded = json.loads(args.check.read_text())
        validate_certificate(loaded)
        print(f"PASS: certificate matches {args.check}")
    if args.pdf is not None:
        got = sha256(args.pdf)
        require(got == EXPECTED_SHA, f"PDF hash mismatch: {got}")
        print(f"PASS: PDF hash matches {EXPECTED_SHA}")
    if args.emit is None and args.check is None and args.pdf is None:
        validate_certificate(cert)
        print("PASS: axis9_dither packet")


if __name__ == "__main__":
    main()
