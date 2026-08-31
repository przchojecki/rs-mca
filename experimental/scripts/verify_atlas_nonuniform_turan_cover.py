#!/usr/bin/env python3
"""Freeze and exactly audit a nonuniform hierarchical T(509,35,8) cover."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


EXPECTED_CARDINALITY = 762_054_269_114


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def balanced_sizes(total: int, parts: int) -> tuple[int, ...]:
    return tuple((total + parts - 1 - index) // parts for index in range(parts))


def selected_count(
    pattern: tuple[int, ...], color_sizes: tuple[int, ...]
) -> int:
    return math.prod(
        math.comb(size, multiplicity)
        for size, multiplicity in zip(color_sizes, pattern)
    )


def freeze(payload: dict) -> bytes:
    lines = [
        "ATLAS_NONUNIFORM_HIERARCHICAL_COVER_V1",
        "{} {} {}".format(
            payload["row_count"],
            payload["global_witness_size"],
            payload["face_size"],
        ),
        str(len(payload["block_records"])),
    ]
    for record in payload["block_records"]:
        patterns = record["selected_patterns"]
        lines.append(
            "{} {} {} {}".format(
                record["block_size"],
                record["local_witness_size"],
                record["colors"],
                len(patterns),
            )
        )
        lines.extend(" ".join(map(str, pattern)) for pattern in patterns)
    return ("\n".join(lines) + "\n").encode("ascii")


def audit(optimizer_path: Path, cover_path: Path, output_path: Path) -> dict:
    optimizer_bytes = optimizer_path.read_bytes()
    payload = json.loads(optimizer_bytes)
    if payload.get("schema") != "atlas-nonuniform-hierarchical-cover-cp-sat/v1":
        raise AssertionError("optimizer schema")
    payload_body = dict(payload)
    reported_payload_sha256 = payload_body.pop("payload_sha256", None)
    canonical_payload = json.dumps(
        payload_body, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    if hashlib.sha256(canonical_payload).hexdigest() != reported_payload_sha256:
        raise AssertionError("optimizer payload hash")
    rows = int(payload["row_count"])
    witness_size = int(payload["global_witness_size"])
    face_size = int(payload["face_size"])
    if (rows, witness_size, face_size) != (509, 35, 8):
        raise AssertionError("global parameters")

    records = payload["block_records"]
    blocks = tuple(int(record["block_size"]) for record in records)
    thresholds = tuple(int(record["local_witness_size"]) for record in records)
    if tuple(map(int, payload["block_sizes"])) != blocks or sum(blocks) != rows:
        raise AssertionError("block partition")
    if tuple(map(int, payload["local_witness_sizes"])) != thresholds:
        raise AssertionError("local thresholds")
    pigeonhole_budget = sum(threshold - 1 for threshold in thresholds)
    if pigeonhole_budget >= witness_size:
        raise AssertionError("pigeonhole budget")
    if int(payload["pigeonhole_budget"]) != pigeonhole_budget:
        raise AssertionError("reported pigeonhole budget")

    global_distributions = tuple(compositions(witness_size, len(blocks)))
    uncovered_global = tuple(
        distribution
        for distribution in global_distributions
        if all(value < threshold for value, threshold in zip(distribution, thresholds))
    )
    if uncovered_global:
        raise AssertionError("uncovered global block distribution")

    block_audits = []
    exact_total = 0
    for block_index, record in enumerate(records):
        if int(record["block_index"]) != block_index:
            raise AssertionError("block index")
        size = blocks[block_index]
        threshold = thresholds[block_index]
        colors = int(record["colors"])
        if threshold < face_size or not 2 <= colors <= 8:
            raise AssertionError("local dimensions")
        color_sizes = balanced_sizes(size, colors)
        if tuple(map(int, record["color_sizes"])) != color_sizes:
            raise AssertionError("color sizes")
        patterns = tuple(tuple(map(int, pattern)) for pattern in record["selected_patterns"])
        if len(patterns) != len(set(patterns)):
            raise AssertionError("duplicate local pattern")
        if any(
            len(pattern) != colors or min(pattern) < 0 or sum(pattern) != face_size
            for pattern in patterns
        ):
            raise AssertionError("malformed local pattern")

        local_distributions = tuple(compositions(threshold, colors))
        multiplicities = tuple(
            sum(
                all(left <= right for left, right in zip(pattern, distribution))
                for pattern in patterns
            )
            for distribution in local_distributions
        )
        if not multiplicities or min(multiplicities) < 1:
            raise AssertionError("uncovered local distribution")
        exact_block = sum(selected_count(pattern, color_sizes) for pattern in patterns)
        if int(record["exact_selected_eight_subsets"]) != exact_block:
            raise AssertionError("block cardinality")
        if int(record["selected_pattern_count"]) != len(patterns):
            raise AssertionError("block pattern count")
        exact_total += exact_block
        block_audits.append(
            {
                "block_index": block_index,
                "block_size": size,
                "local_witness_size": threshold,
                "colors": colors,
                "color_sizes": list(color_sizes),
                "pattern_count": len(patterns),
                "local_distribution_count": len(local_distributions),
                "minimum_cover_multiplicity": min(multiplicities),
                "maximum_cover_multiplicity": max(multiplicities),
                "selected_eight_subsets": exact_block,
            }
        )
    if int(payload["exact_selected_eight_subsets"]) != exact_total:
        raise AssertionError("global cardinality")
    if exact_total != EXPECTED_CARDINALITY:
        raise AssertionError("unexpected certified cardinality")

    cover_bytes = freeze(payload)
    cover_path.write_bytes(cover_bytes)
    report = {
        "schema": "atlas-nonuniform-hierarchical-cover-freeze-audit/v1",
        "status": "PASS_EXACT_NONUNIFORM_HIERARCHICAL_35_TO_8_COVER",
        "row_count": rows,
        "global_witness_size": witness_size,
        "face_size": face_size,
        "block_sizes": list(blocks),
        "local_witness_sizes": list(thresholds),
        "pigeonhole_budget": pigeonhole_budget,
        "global_block_distribution_count": len(global_distributions),
        "block_audits": block_audits,
        "selected_eight_subsets": exact_total,
        "previous_uniform_six_color_selected_eight_subsets": 911_798_442_756,
        "reduction_factor_against_uniform_six_color": 911_798_442_756 / exact_total,
        "previous_parity_selected_eight_subsets": 2_725_371_892_323,
        "reduction_factor_against_parity": 2_725_371_892_323 / exact_total,
        "optimizer_status": payload["status"],
        "optimizer_claims_optimality": payload["status"] == "OPTIMAL",
        "optimizer_payload_sha256": reported_payload_sha256,
        "cover_sha256": hashlib.sha256(cover_bytes).hexdigest(),
        "proof_summary": [
            "Every 35-composition across the macroblocks reaches at least one recorded local threshold.",
            "Every color composition at that local threshold dominates a frozen weight-eight pattern for the same block.",
            "Therefore every 35-subset of the 509 rows contains a frozen selected eight-face.",
        ],
    }
    canonical = (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "ascii"
    )
    report["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("optimizer", type=Path)
    parser.add_argument("cover", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = audit(args.optimizer, args.cover, args.output)
    print(
        "PASS Atlas nonuniform cover blocks={} selected={}".format(
            report["block_sizes"], report["selected_eight_subsets"]
        )
    )


if __name__ == "__main__":
    main()
