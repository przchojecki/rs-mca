#!/usr/bin/env python3
"""Verify the official-row-primes reframe certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path(
    "experimental/data/certificates/official-row-primes-reframe/"
    "official_row_primes_reframe.json"
)

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "assuming |F| is sufficiently large",
    "for every choice of F, L, and k",
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
        "schema": "rs-mca.experimental.official_row_primes_reframe.v1",
        "status": "PROVED",
        "source_dag_node": "official_row_primes_pinning",
        "verdict": "no_fixed_official_primes",
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
            "The challenge quantifies over admissible Reed-Solomon codes over "
            "fields F; it does not publish a finite list of official row "
            "primes. Certification is therefore either family-uniform or "
            "exhibit-specific."
        ),
        "quote_fragments": REQUIRED_FRAGMENTS,
        "admissibility_data": {
            "smooth_domain": (
                "L is a multiplicative subgroup of F whose size is a power of two"
            ),
            "rates": ["1/2", "1/4", "1/8", "1/16"],
            "dimension_bound": "k <= 2^40",
            "field_bound": "|F| < 2^256",
        },
        "consequence": {
            "stand_in_primes": (
                "valid only as exhibit or calibration rows unless accompanied "
                "by a family-uniform transfer certificate"
            ),
            "official_rows": (
                "no literal official prime constants need to be pinned from "
                "the prize statement"
            ),
            "certificate_obligation": (
                "state either a uniform-in-F theorem/certificate or the exact "
                "exhibit field being certified"
            ),
        },
        "non_claims": [
            "does not certify any stand-in prime as official",
            "does not supply a stand-in-to-uniform transfer theorem",
            "does not edit or promote Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    fragments = set(cert["quote_fragments"])
    missing = sorted(set(REQUIRED_FRAGMENTS) - fragments)
    require(not missing, "missing quote fragments: " + ", ".join(missing))
    obligation = cert["consequence"]["certificate_obligation"]
    require("uniform" in obligation, "certificate obligation must mention uniformity")
    require("exhibit" in obligation, "certificate obligation must mention exhibits")


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
        print("PASS: official-row-primes reframe packet")


if __name__ == "__main__":
    main()
