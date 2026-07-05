#!/usr/bin/env python3
"""Verify the axis1_batching certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/axis1-batching/axis1_batching.json")

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "Lines",
    "{f1 + gamma f2}_{gamma in F}",
    "family Flines",
    "only consider MCA with respect to the family of lines",
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
        "schema": "rs-mca.experimental.axis1_batching.v1",
        "status": "PROVED",
        "source_dag_node": "axis1_batching",
        "verdict": "official_mca_sampler_is_affine_line",
        "source": {
            "artifact": "abf26.pdf",
            "description": (
                "Arnon-Boneh-Fenzi, Open Problems in List Decoding and "
                "Correlated Agreement"
            ),
            "source_id": "IACR ePrint 2026/680",
            "pages": [3, 17],
            "sha256": EXPECTED_SHA,
        },
        "quote_fragments": REQUIRED_FRAGMENTS,
        "official_sampler": {
            "shape": "affine line",
            "formula": "{f1 + gamma f2}_{gamma in F}",
            "repo_form": "u + z v",
        },
        "claim": (
            "The official MCA object uses affine lines in two words. Nonlinear "
            "power-curve or polynomial-generator samplers are separate variants, "
            "not the default MCA batching shape."
        ),
        "non_claims": [
            "does not analyze polynomial-generator MCA",
            "does not prove a proximity bound",
            "does not decide CA or list objects",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    missing = sorted(set(REQUIRED_FRAGMENTS) - set(cert["quote_fragments"]))
    require(not missing, "missing quote fragments: " + ", ".join(missing))
    require(cert["official_sampler"]["repo_form"] == "u + z v", "repo sampler mismatch")


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
        print("PASS: axis1_batching packet")


if __name__ == "__main__":
    main()
