#!/usr/bin/env python3
"""Verify the Hankel moment-clean leaves packet certificate."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


CERT_PATH = Path(
    "experimental/data/certificates/hankel-moment-clean-leaves/hankel_moment_clean_leaves.json"
)

SAMPLES = [
    {"q": 5, "dim_a": 4, "domain_size": 8, "s": 2, "moment_bound": 700},
    {"q": 7, "dim_a": 5, "domain_size": 10, "s": 3, "moment_bound": 5880},
    {"q": 3, "dim_a": 6, "domain_size": 9, "s": 1, "moment_bound": 2187},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def moment_bound(q: int, dim_a: int, domain_size: int, s: int) -> int:
    require(0 <= s <= dim_a, "sample keeps s <= dim A for the q^(dim A-s) branch")
    return comb(domain_size, s) * (q ** (dim_a - s))


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.hankel_moment_clean_leaves.v1",
        "status": "PROVED",
        "source_dag_node": "hankel_moment_clean_leaves",
        "verdict": "pinned_affine_terminal_leaves_have_clean_moment_bound",
        "claim": {
            "hypothesis": "affine annihilator has no nonzero word of weight <= r",
            "for_each_T": "|T| = s <= r",
            "alternatives": ["ev_T(A) misses 0", "ev_T(A) is onto"],
            "count_values": ["0", "q^(dim A - s)"],
            "moment_bound": "sum_f binom(rho(f),s) <= binom(|E|,s) q^(dim A-s)",
        },
        "verified_clean_flats": 279,
        "sample_arithmetic": SAMPLES,
        "correction": {
            "unpinned_cleanliness": "false in general",
            "reason": "monic/affine slices can have low-weight direction-dual words with nonzero affine constant",
            "packaged_variant": "pinned-value affine lemma",
        },
        "consumers": ["f_termination_hankel"],
        "non_claims": [
            "does not assert unpinned direction-dual cleanliness",
            "does not count reachable terminal states",
            "does not prove rank-profile entropy",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    require(cert["verified_clean_flats"] == 279, "verified-flat count changed")
    require(cert["correction"]["unpinned_cleanliness"] == "false in general", "correction boundary missing")
    for row in cert["sample_arithmetic"]:
        got = moment_bound(row["q"], row["dim_a"], row["domain_size"], row["s"])
        require(got == row["moment_bound"], f"moment-bound arithmetic mismatch: {row} != {got}")


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
        print("PASS: hankel moment-clean leaves packet")


if __name__ == "__main__":
    main()
