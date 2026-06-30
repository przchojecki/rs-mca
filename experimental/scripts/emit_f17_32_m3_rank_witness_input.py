#!/usr/bin/env python3
"""Emit a concrete F_17^32 M3 rank-witness regular-minor input.

This is a stress input for the Paper D v9 regular-window pipeline.  It uses the
pinned F_17^32 row descriptor and builds a synthetic syndrome pencil at a
selected exact agreement A.  The construction is deliberately simple:

    u_m = 0,
    v_m = sum_i x_i^m,

where x_i are the first j+1 domain elements from the descriptor.  At slope 1 the
prefix Hankel minor is Z^(j+1) times a shifted Vandermonde square, so
rank_at_nodes finds a full-rank specialization and the extractor can emit the
closed-form synthetic root table {0} without determinant interpolation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (
    Field,
    K,
    MODULUS,
    N,
    P,
)


DEFAULT_AGREEMENT = 426
ROW_DESCRIPTOR = REPO_ROOT / (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/hankel-regular-minor-inputs/"
    "f17_32_n512_k256_a426_rank_witness_input.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def power_sum_syndrome(
    field: Field,
    nodes: list[tuple[int, ...]],
    length: int,
) -> list[int]:
    syndrome = []
    powers = [field.one for _ in nodes]
    for exponent in range(length):
        total = field.zero
        if exponent == 0:
            total = field.normalize(len(nodes))
        else:
            for power in powers:
                total = tuple(
                    (total[index] + power[index]) % field.p
                    for index in range(field.degree)
                )
        syndrome.append(field.encode(total))
        powers = [field.mul(power, node) for power, node in zip(powers, nodes)]
    return syndrome


def build_input(agreement: int = DEFAULT_AGREEMENT) -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR)
    field = Field(P, MODULUS)
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    if t_value < size:
        raise ValueError("selected agreement is not regular overdetermined")
    length = t_value + j_value
    if length > N - K:
        raise ValueError("selected agreement needs more syndrome entries than n-k")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    nodes = [field.decode(value) for value in domain_encodings[:size]]
    v_syndrome = power_sum_syndrome(field, nodes, length)
    return {
        "schema_version": "regular-hankel-minor-extractor-input-v1",
        "row": {
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor; "
                "synthetic M3 rank-witness syndrome uses the first j+1 elements"
            ),
        },
        "field_model": {
            "kind": "polynomial_basis",
            "p": P,
            "degree": field.degree,
            "modulus": MODULUS,
            "encoding": "base-p low-to-high coefficients",
        },
        "agreement_threshold": agreement,
        "exact_agreements": [agreement],
        "sampler": "finite_affine_line",
        "certificate_mode": "zero_u_monomial_roots",
        "line_syndrome": {
            "u": [0 for _ in range(length)],
            "v": v_syndrome,
            "field_encoding": "base-p low-to-high integer",
            "description": (
                "synthetic M3 rank witness: u=0 and v_m=sum_i x_i^m for "
                "the first j+1 descriptor-domain elements"
            ),
            "length": length,
            "witness_slope": 1,
            "witness_node_prefix_count": size,
            "rank_witness_reason": (
                "u=0 makes the prefix determinant a nonzero monomial in the slope"
            ),
        },
        "row_set_strategy": {"type": "rank_at_nodes"},
        "status": "PROVED / AUDIT",
        "nonclaims": [
            "synthetic syndrome pencil only",
            "not a worst-case MCA row bound",
            "not a worst-case row root table over F_17^32",
            "not a quotient/tangent subtraction table",
        ],
    }


def check_input(path: Path, agreement: int) -> None:
    expected = render(build_input(agreement))
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-witness input mismatch: {path}")


def print_summary(packet: dict[str, Any]) -> None:
    row = packet["row"]
    agreement = packet["exact_agreements"][0]
    j_value = row["n"] - agreement
    t_value = agreement - row["k"]
    print("F_17^32 M3 rank-witness extractor input")
    print(
        "row: {field}, n={n}, k={k}, A={agreement}, j={j}, t={t}".format(
            agreement=agreement,
            j=j_value,
            t=t_value,
            **row,
        )
    )
    print(
        "syndrome_length={length}, witness_prefix={prefix}, mode={mode}".format(
            length=packet["line_syndrome"]["length"],
            prefix=packet["line_syndrome"]["witness_node_prefix_count"],
            mode=packet["certificate_mode"],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agreement", type=int, default=DEFAULT_AGREEMENT)
    parser.add_argument("--write", type=Path, help="write deterministic input JSON")
    parser.add_argument("--check", type=Path, help="check deterministic input JSON")
    parser.add_argument("--json", action="store_true", help="print input JSON")
    args = parser.parse_args()

    packet = build_input(args.agreement)
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_input(args.check, args.agreement)
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
