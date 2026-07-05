#!/usr/bin/env python3
"""Verify the rules_freeze citation certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/rules-freeze/rules_freeze.json")

EXPECTED_SHA = "426a979c13cc61db0f2cdb909067ef4c9f24438859fe0a7a337d2b19b07fcaa5"
REQUIRED_FRAGMENTS = [
    "multiplicative subgroup of F whose size is a power of two",
    "rho(C) := k/|L|",
    "one of 1/2, 1/4, 1/8, 1/16",
    "k <= 2^40",
    "|F| < 2^256",
    "and a constant m",
    "for a code C, an m, and an eps*",
    "2^-128",
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
        "schema": "rs-mca.experimental.rules_freeze.v1",
        "status": "PROVED",
        "source_dag_node": "rules_freeze",
        "source_dag_dependencies": ["field_cap_check", "rules_m_reading"],
        "verdict": "official_prize_box_pinned_by_abf26_page5",
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
        "claim": {
            "smooth_domain": "multiplicative subgroup of F of power-of-two size",
            "target_range": {"k_max": "2^40", "field_size_lt": "2^256"},
            "official_rates": ["1/2", "1/4", "1/8", "1/16"],
            "list_arity": "per declared constant m",
            "gate": {"epsilon_star": "2^-128", "list_budget": "epsilon_star * |F|"},
        },
        "interpretation": {
            "coset_language": (
                "Coset-form analysis is a conservative superset of the "
                "subgroup wording unless a packet explicitly uses subgroup-only "
                "normalization."
            ),
            "axis9_dither": "official rows have exact listed rates; no implicit dither",
            "s0_zero_open": "rules layer contributes no remaining open convention axis",
            "m_handling": (
                "fixed constant-m determinations are valid per-instance packets"
            ),
        },
        "non_claims": [
            "does not prove a safe or unsafe threshold",
            "does not promote v13 experimental rows into Paper D",
            "does not edit Papers A-D",
            "does not decide future external prize-page drift",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    missing = sorted(set(REQUIRED_FRAGMENTS) - set(cert["quote_fragments"]))
    require(not missing, "missing quote fragments: " + ", ".join(missing))
    claim = cert["claim"]
    require(claim["target_range"]["k_max"] == "2^40", "k cap mismatch")
    require(claim["target_range"]["field_size_lt"] == "2^256", "field cap mismatch")
    require(claim["official_rates"] == ["1/2", "1/4", "1/8", "1/16"], "rate set mismatch")
    require("constant m" in claim["list_arity"], "list arity reading mismatch")
    require(cert["source"]["sha256"] == EXPECTED_SHA, "source SHA mismatch")


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
        print("PASS: rules_freeze packet")


if __name__ == "__main__":
    main()
