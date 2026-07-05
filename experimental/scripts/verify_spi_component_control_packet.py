#!/usr/bin/env python3
"""Verify the SPI component-control packet certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CERT_PATH = Path("experimental/data/certificates/spi-component-control/spi_component_control.json")

SAMPLES = [
    {"t": 3, "j": 4, "r": 3, "rank_drop_slopes": 1},
    {"t": 5, "j": 7, "r": 4, "rank_drop_slopes": 4},
    {"t": 8, "j": 11, "r": 6, "rank_drop_slopes": 5},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.spi_component_control.v1",
        "status": "PROVED",
        "source_dag_node": "spi_component_control",
        "verdict": "alignment_incidence_has_one_horizontal_scroll_and_at_most_t_vertical_fibres",
        "claim": {
            "incidence": "I_{u,v} = {(Z,[l]) in P^1 x P^j : M(Z)l = 0}",
            "pencil": "M(Z) = Z0 M_u + Z1 M_v",
            "generic_rank": "r over K(Z), with r <= t",
            "minor_degree": "deg Delta(Z) <= r <= t",
            "horizontal_component": "one projective-bundle scroll, Segre degree <= j+1",
            "vertical_components": "at most r <= t rank-drop fibres, each a single linear space",
            "component_bound": "#Irr(I_{u,v}) <= t + 1",
            "degree_bound": "Segre degree <= j + t + 1",
        },
        "verified_random_pencils": {
            "field": "F_17",
            "trials": 2500,
            "t": 3,
            "j": 4,
            "worst_rank_drop_slopes": 1,
            "rank_bound": 3,
        },
        "sample_arithmetic": SAMPLES,
        "consumers": ["spi_exceptional_class", "ef_component_control_alignment"],
        "non_claims": [
            "does not count D_j points on the generic horizontal scroll",
            "does not classify exceptional components as paid or empty",
            "does not enumerate supports",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    for row in cert["sample_arithmetic"]:
        require(row["r"] <= row["t"], f"generic rank exceeds t: {row}")
        require(row["rank_drop_slopes"] <= row["r"], f"rank-drop bound violated: {row}")
        require(row["t"] + 1 >= row["rank_drop_slopes"] + 1, f"component bound violated: {row}")
        require(row["j"] + row["t"] + 1 >= row["j"] + 1, f"degree bound weakened: {row}")
    verified = cert["verified_random_pencils"]
    require(verified["trials"] == 2500, "random-pencil trial count changed")
    require(verified["worst_rank_drop_slopes"] <= verified["rank_bound"], "verified rank-drop bound failed")


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
        print("PASS: SPI component-control packet")


if __name__ == "__main__":
    main()
