#!/usr/bin/env python3
"""Verify the M3 finite rank-node regular/singular dichotomy."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    K,
    N,
)


SCHEMA_VERSION = "f17-32-m3-rank-node-dichotomy-v1"
Q_LINE = 17**32
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
WINDOW_REF = (
    "experimental/data/certificates/hankel-regular-window-f17-385-426/"
    "f17_32_n512_k256_regular_window_plan.json"
)
GENERIC_MINOR_REF = (
    "experimental/data/certificates/hankel-f17-32-generic-regular-minor/"
    "f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def trim(poly: list[int], prime: int) -> list[int]:
    out = [entry % prime for entry in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_i in enumerate(left):
        for j, right_j in enumerate(right):
            out[i + j] = (out[i + j] + left_i * right_j) % prime
    return trim(out, prime)


def poly_eval(poly: list[int], value: int, prime: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % prime
        power = power * value % prime
    return total


def root_poly(roots: list[int], prime: int) -> list[int]:
    out = [1]
    for root in roots:
        out = poly_mul(out, [(-root) % prime, 1], prime)
    return out


def sanity_checks() -> list[dict[str, Any]]:
    prime = 17
    size = 4
    sharp_poly = root_poly(list(range(size)), prime)
    require(len(sharp_poly) - 1 == size, "sharpness degree mismatch")
    for node in range(size):
        require(poly_eval(sharp_poly, node, prime) == 0, "sharpness root mismatch")
    require(poly_eval(sharp_poly, size, prime) != 0, "sharpness nonroot mismatch")

    # A determinant of degree s can vanish at s tested nodes and still be
    # nonzero.  Thus the singularity certificate really needs s+1 nodes.
    return [
        {
            "prime": prime,
            "column_count": size,
            "determinant_low_to_high": sharp_poly,
            "vanishing_nodes": list(range(size)),
            "full_rank_node": size,
            "result": "s nodes are not enough; s+1 nodes are sharp",
        }
    ]


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    column_count = j_value + 1
    required_nodes = column_count + 1
    nodes = list(range(required_nodes))
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "column_count": column_count,
        "maximal_minor_degree_bound": column_count,
        "rank_test_nodes_required": required_nodes,
        "deterministic_node_encoding": "base-p low-to-high integer",
        "deterministic_node_first": nodes[0],
        "deterministic_node_last": nodes[-1],
        "deterministic_nodes_are_distinct": len(set(nodes)) == required_nodes,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    window = load_json(WINDOW_REF)
    generic = load_json(GENERIC_MINOR_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor field-order mismatch")
    require(window["window"]["A_min"] == A_MIN, "window A_min mismatch")
    require(window["window"]["A_max"] == A_MAX, "window A_max mismatch")
    require(generic["claim"]["regular_window"]["A_min"] == A_MIN, "generic A_min mismatch")
    require(generic["claim"]["regular_window"]["A_max"] == A_MAX, "generic A_max mismatch")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    require(all(record["t"] >= record["column_count"] for record in records), "not regular")
    require(all(record["deterministic_nodes_are_distinct"] for record in records), "node collision")
    require(max(record["deterministic_node_last"] for record in records) < Q_LINE, "node overflow")
    require(max(record["rank_test_nodes_required"] for record in records) == 129, "unexpected max nodes")
    require(min(record["rank_test_nodes_required"] for record in records) == 88, "unexpected min nodes")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "finite rank-node dichotomy for M3 regular Hankel buckets",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "q_line": Q_LINE,
            "domain_hash": descriptor["row"]["domain_hash"],
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "regular_window_plan": {"ref": WINDOW_REF, "sha256": sha256_file(WINDOW_REF)},
            "generic_regular_minor": {
                "ref": GENERIC_MINOR_REF,
                "sha256": sha256_file(GENERIC_MINOR_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "min_rank_test_nodes": min(record["rank_test_nodes_required"] for record in records),
            "max_rank_test_nodes": max(record["rank_test_nodes_required"] for record in records),
        },
        "theorem": {
            "setup": (
                "Let M(Z)=H_{t,j}(u)+Z H_{t,j}(v) be a t x s finite "
                "regular Hankel pencil with s=j+1 and t>=s."
            ),
            "nonsingular_branch": (
                "If rank M(z0)=s for one finite node z0, row elimination gives "
                "an s-row set R with det M_R(z0)!=0; hence det M_R(Z) is a "
                "nonzero maximal minor and the regular bucket is nonsingular."
            ),
            "singular_branch": (
                "If rank M(z_i)<s at s+1 distinct finite nodes, then every "
                "maximal minor has degree at most s and vanishes at s+1 "
                "distinct points.  Therefore every maximal minor is identically "
                "zero and the bucket is a genuine singular residual for M5."
            ),
            "deterministic_nodes": (
                "For the pinned F_17^32 row, the nodes encoded by integers "
                "0,1,...,s are distinct finite field elements for every "
                "385<=A<=426."
            ),
        },
        "agreement_records": records,
        "sanity_checks": sanity_checks(),
        "summary": {
            "agreement_count": len(records),
            "rank_test_nodes_min": min(record["rank_test_nodes_required"] for record in records),
            "rank_test_nodes_max": max(record["rank_test_nodes_required"] for record in records),
            "node_encoding": "integers 0..j+1 in the F_17^32 polynomial-basis encoding",
            "sharpness_checked": True,
        },
        "checks": [
            "regular-window parameters match the row descriptor",
            "all M3 agreements have t>=j+1",
            "j+2 deterministic finite nodes fit inside F_17^32",
            "s tested nodes are insufficient by an explicit degree-s determinant",
            "s+1 rank-deficient nodes force all maximal minors to vanish identically",
        ],
        "nonclaims": [
            "does not compute finite root tables for nonsingular buckets",
            "does not classify projective infinity",
            "does not perform tangent, quotient, extension, or subfield subtraction",
            "does not close M5 pivot charts after a singular declaration",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-node dichotomy certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-node dichotomy")
    print(
        "agreements={agreement_count}, rank-test nodes={rank_test_nodes_min}..{rank_test_nodes_max}".format(
            **summary
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
