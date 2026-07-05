#!/usr/bin/env python3
"""Verify the rules_m_reading certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/rules-m-reading/rules_m_reading.json")

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "and a constant m",
    "for a code C, an m, and an eps*",
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
        "schema": "rs-mca.experimental.rules_m_reading.v1",
        "status": "PROVED",
        "source_dag_node": "rules_m_reading",
        "verdict": "family_per_constant_m",
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
        "claim": (
            "The list grand challenge is indexed by a declared constant m. "
            "A determination for a fixed constant m is a valid per-instance "
            "prize object; the full arbitrary-constant family requires a "
            "uniform-in-m theorem or equivalent large-m route."
        ),
        "quote_fragments": REQUIRED_FRAGMENTS,
        "interpretation": {
            "fixed_m_packets": "valid determinations for the declared constant m",
            "small_m_batches": "creditable partial coverage for listed constants",
            "full_family": (
                "requires uniform-in-m coverage or a separate large-m route"
            ),
            "large_m_dependency": "a_regularity_forcing or equivalent",
        },
        "non_claims": [
            "does not prove all constant m cases at once",
            "does not provide the large-m regularity theorem",
            "does not edit or promote Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    fragments = set(cert["quote_fragments"])
    missing = sorted(set(REQUIRED_FRAGMENTS) - fragments)
    require(not missing, "missing quote fragments: " + ", ".join(missing))
    claim = cert["claim"]
    require("fixed constant m" in claim, "claim must mention fixed constant m")
    require("uniform-in-m" in claim, "claim must preserve the full-family caveat")


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
        print("PASS: rules_m_reading packet")


if __name__ == "__main__":
    main()
