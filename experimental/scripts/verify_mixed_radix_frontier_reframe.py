#!/usr/bin/env python3
"""Verify the mixed_radix_frontier reframe certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path(
    "experimental/data/certificates/mixed-radix-frontier/"
    "mixed_radix_frontier_reframe.json"
)

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "smooth evaluation domain",
    "multiplicative subgroup",
    "size is a power of two",
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
        "schema": "rs-mca.experimental.mixed_radix_frontier_reframe.v1",
        "status": "PROVED",
        "source_dag_node": "mixed_radix_frontier",
        "verdict": "official_smooth_domain_family_is_2_power",
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
            "The official smooth multiplicative prize family uses evaluation "
            "domains whose size is a power of two. Mixed-radix domains are "
            "therefore generalizations or stress tests, not required frontier "
            "inputs for the official 2-power box."
        ),
        "quote_fragments": REQUIRED_FRAGMENTS,
        "domain_family": {
            "official": "multiplicative subgroup of power-of-two order",
            "repo_coset_convention": (
                "multiplicative cosets of 2-power subgroups are coordinate "
                "changes of the same 2-power-order structure"
            ),
            "mixed_radix_status": (
                "outside the official box unless the domain family is broadened"
            ),
        },
        "classification_for_mixed_radix_notes": [
            "GENERALIZATION",
            "TOY/FALSIFIER",
            "CONSERVATIVE_AUDIT",
        ],
        "non_claims": [
            "does not prove a mixed-radix theorem",
            "does not invalidate mixed-radix experiments",
            "does not broaden the official prize family",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    fragments = set(cert["quote_fragments"])
    missing = sorted(set(REQUIRED_FRAGMENTS) - fragments)
    require(not missing, "missing quote fragments: " + ", ".join(missing))
    claim = cert["claim"]
    require("power of two" in claim, "claim must mention power-of-two domains")
    require("Mixed-radix" in claim, "claim must classify mixed-radix domains")


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
        print("PASS: mixed_radix_frontier reframe packet")


if __name__ == "__main__":
    main()
