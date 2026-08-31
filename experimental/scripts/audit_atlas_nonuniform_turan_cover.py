#!/usr/bin/env python3
"""Independent parser and exhaustive audit for the frozen Atlas cover."""

from __future__ import annotations

import argparse
import hashlib
import json
from math import comb, prod
from pathlib import Path


EXPECTED_CARDINALITY = 762_054_269_114


def weak_compositions(total: int, length: int):
    separators = length - 1
    slots = total + separators
    if separators == 0:
        yield (total,)
        return
    from itertools import combinations

    for cuts in combinations(range(slots), separators):
        boundaries = (-1,) + cuts + (slots,)
        yield tuple(boundaries[index + 1] - boundaries[index] - 1 for index in range(length))


def parse_cover(path: Path):
    raw = path.read_bytes()
    tokens = raw.decode("ascii").split()
    cursor = 0

    def take() -> str:
        nonlocal cursor
        if cursor == len(tokens):
            raise AssertionError("truncated cover")
        value = tokens[cursor]
        cursor += 1
        return value

    if take() != "ATLAS_NONUNIFORM_HIERARCHICAL_COVER_V1":
        raise AssertionError("cover magic")
    rows, witness_size, face_size = (int(take()) for _ in range(3))
    block_count = int(take())
    blocks = []
    for block_index in range(block_count):
        size, threshold, colors, pattern_count = (int(take()) for _ in range(4))
        patterns = tuple(
            tuple(int(take()) for _ in range(colors)) for _ in range(pattern_count)
        )
        blocks.append((block_index, size, threshold, colors, patterns))
    if cursor != len(tokens):
        raise AssertionError("trailing cover tokens")
    return raw, rows, witness_size, face_size, tuple(blocks)


def audit(cover_path: Path, output_path: Path) -> dict:
    raw, rows, witness_size, face_size, blocks = parse_cover(cover_path)
    if (rows, witness_size, face_size) != (509, 35, 8):
        raise AssertionError("fixture parameters")
    if not blocks or sum(block[1] for block in blocks) != rows:
        raise AssertionError("block partition")

    global_cases = 0
    for occupancy in weak_compositions(witness_size, len(blocks)):
        global_cases += 1
        if not any(value >= block[2] for value, block in zip(occupancy, blocks)):
            raise AssertionError(f"global miss {occupancy}")

    block_reports = []
    selected_total = 0
    for block_index, size, threshold, colors, patterns in blocks:
        if not 2 <= colors <= 8 or threshold < face_size:
            raise AssertionError("block dimensions")
        if not patterns or len(patterns) != len(set(patterns)):
            raise AssertionError("empty or duplicate pattern family")
        if any(
            len(pattern) != colors or any(value < 0 for value in pattern)
            or sum(pattern) != face_size
            for pattern in patterns
        ):
            raise AssertionError("invalid pattern")

        local_cases = 0
        min_cover = None
        max_cover = 0
        for occupancy in weak_compositions(threshold, colors):
            local_cases += 1
            covering = sum(
                all(pattern[color] <= occupancy[color] for color in range(colors))
                for pattern in patterns
            )
            if covering == 0:
                raise AssertionError(f"local miss in block {block_index}: {occupancy}")
            min_cover = covering if min_cover is None else min(min_cover, covering)
            max_cover = max(max_cover, covering)

        color_sizes = tuple(size // colors + (color < size % colors) for color in range(colors))
        selected = sum(
            prod(comb(color_sizes[color], pattern[color]) for color in range(colors))
            for pattern in patterns
        )
        selected_total += selected
        block_reports.append(
            {
                "block_index": block_index,
                "block_size": size,
                "local_witness_size": threshold,
                "colors": colors,
                "color_sizes": list(color_sizes),
                "pattern_count": len(patterns),
                "local_distribution_count": local_cases,
                "minimum_cover_multiplicity": min_cover,
                "maximum_cover_multiplicity": max_cover,
                "selected_eight_subsets": selected,
            }
        )

    if selected_total != EXPECTED_CARDINALITY:
        raise AssertionError("unexpected certified cardinality")

    report = {
        "schema": "atlas-nonuniform-hierarchical-cover-independent-audit/v1",
        "status": "PASS_INDEPENDENT_NONUNIFORM_HIERARCHICAL_35_TO_8_COVER",
        "row_count": rows,
        "global_witness_size": witness_size,
        "face_size": face_size,
        "global_block_distribution_count": global_cases,
        "block_reports": block_reports,
        "selected_eight_subsets": selected_total,
        "cover_sha256": hashlib.sha256(raw).hexdigest(),
        "proof_scope": "Exact coverage and cardinality only; no optimality claim.",
    }
    canonical = (json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "ascii"
    )
    report["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cover", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    report = audit(args.cover, args.output)
    print(
        "PASS independent nonuniform cover selected={}".format(
            report["selected_eight_subsets"]
        )
    )


if __name__ == "__main__":
    main()
