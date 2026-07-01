#!/usr/bin/env python3
"""Search the M3 low-rank endpoint-capacity spectral target.

This is a counterexample-first utility for PR #170's normalized low-rank target:

    gcd(Phi_{m,r,0}, Phi_{m,r,1}) = 1,

where Phi_{m,r,h}=det(I+Z K_h) for the consecutive F_17^32 subgroup window.
It deliberately does not write a certificate.  Use it to probe ranks beyond the
current low-rank2..12 packet before deciding whether a larger packet is worth
emitting.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.extract_regular_hankel_minors import (  # noqa: E402
    fpoly_degree,
    fpoly_gcd,
    hash_json,
)
from experimental.scripts import (  # noqa: E402
    verify_f17_32_m3_low_rank2_12_v10_affine_gcd as packet,
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agreement-min",
        type=int,
        default=426,
        help="minimum exact agreement A to probe; default is first frontier probe 426",
    )
    parser.add_argument(
        "--agreement-max",
        type=int,
        default=426,
        help="maximum exact agreement A to probe; default is first frontier probe 426",
    )
    parser.add_argument(
        "--rank-min",
        type=int,
        default=13,
        help="minimum low-rank update size to probe; default is first uncertified rank 13",
    )
    parser.add_argument(
        "--rank-max",
        type=int,
        default=13,
        help="maximum low-rank update size to probe; default is first uncertified rank 13",
    )
    parser.add_argument(
        "--stop-on-collision",
        action="store_true",
        help="stop at the first positive common gcd degree",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the full probe record JSON instead of the compact summary",
    )
    return parser.parse_args()


def validate_range(
    agreement_min: int,
    agreement_max: int,
    rank_min: int,
    rank_max: int,
) -> None:
    require(
        packet.AGREEMENT_MIN <= agreement_min <= agreement_max <= packet.AGREEMENT_MAX,
        "agreement range must lie inside the PR #170 M3 window",
    )
    require(1 <= rank_min <= rank_max, "rank range must be nonempty")
    require(
        rank_max <= packet.N - agreement_min + 1,
        "rank_max exceeds available consecutive update nodes",
    )


def probe_records(
    agreement_min: int,
    agreement_max: int,
    rank_min: int,
    rank_max: int,
    stop_on_collision: bool,
) -> dict[str, Any]:
    row_descriptor = packet.load_json(packet.ROW_DESCRIPTOR_REF)
    field = packet.field_from_descriptor(row_descriptor)
    domain = [
        field.decode(value)
        for value in row_descriptor["domain"]["domain_encodings"]
    ]
    require(len(domain) == packet.N, "domain length")
    require(all(not field.is_zero(node) for node in domain), "domain contains zero")

    ranks = list(range(rank_min, rank_max + 1))
    base_nodes: list[tuple[int, ...]] = []
    denominators: list[tuple[int, ...]] = []
    base_determinant = field.one
    base_product = field.one
    records: list[dict[str, Any]] = []
    gcd_histogram: Counter[int] = Counter()
    degree_failures = 0

    for size in range(1, packet.N - agreement_min + 2):
        new_node = domain[size - 1]
        new_denominator = field.one
        for old_node in base_nodes:
            new_denominator = field.mul(
                new_denominator,
                field.sub(new_node, old_node),
            )
        for index, old_node in enumerate(base_nodes):
            denominators[index] = field.mul(
                denominators[index],
                field.sub(old_node, new_node),
            )
        denominators.append(new_denominator)
        base_nodes.append(new_node)
        base_determinant = field.mul(
            base_determinant,
            field.mul(new_denominator, new_denominator),
        )
        base_product = field.mul(base_product, new_node)

        agreement = packet.N - size + 1
        if not (agreement_min <= agreement <= agreement_max):
            continue

        j = packet.N - agreement
        t = agreement - packet.K
        require(size == j + 1, f"A={agreement}: size mismatch")
        require(t > j + packet.SHIFT, f"A={agreement}: shifted rows unavailable")

        update_nodes = domain[size : size + rank_max]
        basis_values = packet.lagrange_basis_values(
            field,
            base_nodes,
            denominators,
            update_nodes,
        )
        prefix_kernel = packet.weighted_kernel(
            field,
            basis_values,
            [field.one] * size,
            [field.one] * rank_max,
        )
        shifted_kernel = packet.weighted_kernel(
            field,
            basis_values,
            [field.inv(node) for node in base_nodes],
            update_nodes,
        )
        shifted_scale = field.mul(base_determinant, base_product)

        for rank in ranks:
            prefix_coefficients = packet.determinant_coefficients_from_kernel(
                field,
                prefix_kernel,
                rank,
                base_determinant,
            )
            shifted_coefficients = packet.determinant_coefficients_from_kernel(
                field,
                shifted_kernel,
                rank,
                shifted_scale,
            )
            prefix_degree = fpoly_degree(prefix_coefficients, field)
            shifted_degree = fpoly_degree(shifted_coefficients, field)
            common_degree = fpoly_degree(
                fpoly_gcd(prefix_coefficients, shifted_coefficients, field),
                field,
            )
            if prefix_degree != rank or shifted_degree != rank:
                degree_failures += 1
            gcd_histogram[common_degree] += 1
            record = {
                "A": agreement,
                "m": size,
                "rank": rank,
                "rank_capacity": size // 2,
                "within_endpoint_capacity": rank <= size // 2,
                "prefix_degree": prefix_degree,
                "shifted_degree": shifted_degree,
                "common_gcd_degree": common_degree,
                "prefix_hash": hash_json(
                    [field.encode(coefficient) for coefficient in prefix_coefficients]
                ),
                "shifted_hash": hash_json(
                    [field.encode(coefficient) for coefficient in shifted_coefficients]
                ),
            }
            records.append(record)
            if stop_on_collision and common_degree > 0:
                return summary(records, gcd_histogram, degree_failures)

    return summary(records, gcd_histogram, degree_failures)


def summary(
    records: list[dict[str, Any]],
    gcd_histogram: Counter[int],
    degree_failures: int,
) -> dict[str, Any]:
    collisions = [
        record
        for record in records
        if record["common_gcd_degree"] > 0
    ]
    return {
        "schema_version": "f17-32-m3-low-rank-spectral-target-search-v1",
        "status": "EXPERIMENTAL / AUDIT",
        "claim": "counterexample-first exact probe for the PR #170 synthetic low-rank spectral target",
        "record_count": len(records),
        "degree_failure_count": degree_failures,
        "common_gcd_degree_histogram": {
            str(key): value for key, value in sorted(gcd_histogram.items())
        },
        "collision_count": len(collisions),
        "first_collision": collisions[0] if collisions else None,
        "records": records,
    }


def print_summary(result: dict[str, Any]) -> None:
    print("F_17^32 M3 low-rank spectral target search")
    print(f"status: {result['status']}")
    print(f"records: {result['record_count']}")
    print(f"degree failures: {result['degree_failure_count']}")
    print(f"common gcd degree histogram: {result['common_gcd_degree_histogram']}")
    if result["first_collision"] is None:
        print("first collision: none")
    else:
        print(f"first collision: {result['first_collision']}")


def main() -> None:
    args = parse_args()
    validate_range(
        args.agreement_min,
        args.agreement_max,
        args.rank_min,
        args.rank_max,
    )
    result = probe_records(
        args.agreement_min,
        args.agreement_max,
        args.rank_min,
        args.rank_max,
        args.stop_on_collision,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    print_summary(result)


if __name__ == "__main__":
    main()
