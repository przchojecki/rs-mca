#!/usr/bin/env python3
"""Verify the axis8_generating certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/axis8-generating/axis8_generating.json")

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "C := RS[F, L, k]",
    "L subset F",
    "smooth evaluation domain",
    "multiplicative subgroup",
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
        "schema": "rs-mca.experimental.axis8_generating.v1",
        "status": "PROVED",
        "source_dag_node": "axis8_generating",
        "depends_on": ["field_cap_check"],
        "verdict": "non_generating_rows_are_admissible_and_must_be_priced",
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
        "inference": (
            "The source constrains the ambient field F and smooth subgroup L "
            "but does not require L to generate F. A subgroup contained in a "
            "proper subfield of an admissible ambient F is therefore not "
            "excluded by the official family definition."
        ),
        "ledger_consequence": {
            "non_generating_case": "live/admissible",
            "required_response": (
                "price by extension-lift, F1 descent, or another named "
                "tower-case theorem"
            ),
            "forbidden_shortcut": (
                "do not merge generated-field entropy with ambient-field "
                "budget without a transfer theorem"
            ),
        },
        "non_claims": [
            "does not prove an extension-line MCA theorem",
            "does not assert every tower case creates an obstruction",
            "does not merge generated-field and ambient-field ledgers",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    missing = sorted(set(REQUIRED_FRAGMENTS) - set(cert["quote_fragments"]))
    require(not missing, "missing quote fragments: " + ", ".join(missing))
    require("field_cap_check" in cert["depends_on"], "field cap dependency missing")
    inference = cert["inference"]
    require("does not require L to generate F" in inference, "missing generation inference")
    consequence = cert["ledger_consequence"]
    require(consequence["non_generating_case"] == "live/admissible", "wrong verdict")


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
        print("PASS: axis8_generating packet")


if __name__ == "__main__":
    main()
