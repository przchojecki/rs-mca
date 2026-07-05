#!/usr/bin/env python3
"""Verify the field_cap_check certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/field-cap-check/field_cap_check.json")

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "rho(C) is one of 1/2, 1/4, 1/8, 1/16",
    "eps* = 2^-128",
    "k <= 2^40",
    "|F| < 2^256",
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
        "schema": "rs-mca.experimental.field_cap_check.v1",
        "status": "PROVED",
        "source_dag_node": "field_cap_check",
        "verdict": "official_rates_epsilon_dimension_and_field_caps_pinned",
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
        "constants": {
            "rates": ["1/2", "1/4", "1/8", "1/16"],
            "epsilon_star": "2^-128",
            "dimension_bound": "k <= 2^40",
            "field_bound": "|F| < 2^256",
        },
        "uses": [
            "B* = floor(epsilon* Q) budget magnitudes",
            "field-size admissibility checks",
            "tower and generated-field ledger separation",
        ],
        "non_claims": [
            "does not compute a row threshold",
            "does not certify any specific exhibit field",
            "does not merge generated, line, challenge, or ambient field ledgers",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    constants = cert["constants"]
    require(constants["dimension_bound"] == "k <= 2^40", "dimension cap mismatch")
    require(constants["field_bound"] == "|F| < 2^256", "field cap mismatch")
    missing = sorted(set(REQUIRED_FRAGMENTS) - set(cert["quote_fragments"]))
    require(not missing, "missing quote fragments: " + ", ".join(missing))


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
        print("PASS: field_cap_check packet")


if __name__ == "__main__":
    main()
