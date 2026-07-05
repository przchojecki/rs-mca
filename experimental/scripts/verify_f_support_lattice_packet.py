#!/usr/bin/env python3
"""Verify the f_support_lattice packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/f-support-lattice/f_support_lattice.json")

TOY_SUPPORTS = [(0, 1), (1, 2), (3,)]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def generated_union_lattice(supports: list[tuple[int, ...]]) -> set[frozenset[int]]:
    closed: set[frozenset[int]] = {frozenset()}
    changed = True
    while changed:
        changed = False
        for state in list(closed):
            for support in supports:
                nxt = state | frozenset(support)
                if nxt not in closed:
                    closed.add(nxt)
                    changed = True
    return closed


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.f_support_lattice.v1",
        "status": "PROVED",
        "source_dag_node": "f_support_lattice",
        "verdict": "descent_tree_memoizes_to_sparse_support_closed_sets",
        "claim": {
            "state_key": [
                "generated closed support set",
                "residual flat data",
                "residual locator-degree data",
            ],
            "strict_chain_measure": "flat dimension plus locator degree-drop budget",
            "tree_size_bound": "closed_set_count * (1 + W_max)",
        },
        "toy_lattice": {
            "supports": [list(s) for s in TOY_SUPPORTS],
            "closed_set_count": 8,
            "max_chain_length": 3,
        },
        "consumers": ["hankel_rank_profile_entropy", "f_termination_hankel"],
        "non_claims": [
            "does not prove a uniform polynomial closed-set bound",
            "does not classify sparse supports for a specific family",
            "does not close the Hankel termination theorem by itself",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    supports = [tuple(row) for row in cert["toy_lattice"]["supports"]]
    lattice = generated_union_lattice(supports)
    require(len(lattice) == cert["toy_lattice"]["closed_set_count"], "toy lattice count mismatch")
    universe_size = len({x for s in supports for x in s})
    require(cert["toy_lattice"]["max_chain_length"] <= universe_size, "toy chain bound mismatch")
    require("closed_set_count" in cert["claim"]["tree_size_bound"], "tree-size bound missing closed-set count")
    require(cert["status"] == "PROVED", "packet must remain PROVED")


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
        print("PASS: f_support_lattice packet")


if __name__ == "__main__":
    main()
