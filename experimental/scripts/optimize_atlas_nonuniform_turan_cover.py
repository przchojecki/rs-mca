#!/usr/bin/env python3
"""Optimize an exact nonuniform hierarchical T(509,35,8) cover."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from ortools.sat.python import cp_model


ROW_COUNT = 509
WITNESS_SIZE = 35
FACE_SIZE = 8


def compositions(total: int, parts: int):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def balanced_sizes(total: int, parts: int) -> tuple[int, ...]:
    return tuple((total + parts - 1 - index) // parts for index in range(parts))


def parse_csv(value: str) -> tuple[int, ...]:
    result = tuple(int(item) for item in value.split(",") if item)
    if not result:
        raise ValueError("empty integer list")
    return result


def pattern_weight(pattern: tuple[int, ...], color_sizes: tuple[int, ...]) -> int:
    return math.prod(
        math.comb(size, multiplicity)
        for size, multiplicity in zip(color_sizes, pattern)
    )


def lift_patterns(
    patterns: tuple[tuple[int, ...], ...], target_colors: int
) -> tuple[tuple[int, ...], ...]:
    """Refine the final color until every pattern has target_colors entries."""
    lifted = set(patterns)
    if not lifted:
        return ()
    source_colors = len(next(iter(lifted)))
    if any(len(pattern) != source_colors for pattern in lifted):
        raise ValueError("hint patterns have inconsistent color counts")
    while source_colors > target_colors:
        lifted = {
            pattern[:-2] + (pattern[-2] + pattern[-1],)
            for pattern in lifted
        }
        source_colors -= 1
    while source_colors < target_colors:
        lifted = {
            pattern[:-1] + (left, pattern[-1] - left)
            for pattern in lifted
            for left in range(pattern[-1] + 1)
        }
        source_colors += 1
    return tuple(sorted(lifted))


def load_hint(
    path: Path | None,
    block_sizes: tuple[int, ...],
    thresholds: tuple[int, ...],
    colors: tuple[int, ...],
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    if path is None:
        return tuple(() for _ in block_sizes)
    payload = json.loads(path.read_text(encoding="ascii"))
    if "block_records" in payload:
        records = payload["block_records"]
        if len(records) != len(block_sizes):
            raise ValueError("hint block count mismatch")
        result = []
        for record, size, threshold, color_count in zip(
            records, block_sizes, thresholds, colors
        ):
            del size, threshold
            result.append(
                lift_patterns(
                    tuple(
                        tuple(map(int, pattern))
                        for pattern in record["selected_patterns"]
                    ),
                    color_count,
                )
            )
        return tuple(result)

    patterns = tuple(tuple(map(int, pattern)) for pattern in payload["selected_patterns"])
    return tuple(lift_patterns(patterns, color_count) for color_count in colors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--block-sizes", default="170,170,169")
    parser.add_argument("--local-witnesses", default="12,12,12")
    parser.add_argument("--colors", default="6,6,6")
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--random-seed", type=int, default=1)
    args = parser.parse_args()

    block_sizes = parse_csv(args.block_sizes)
    thresholds = parse_csv(args.local_witnesses)
    colors = parse_csv(args.colors)
    if not (len(block_sizes) == len(thresholds) == len(colors)):
        raise ValueError("block, threshold and color lists must have equal lengths")
    if sum(block_sizes) != ROW_COUNT:
        raise ValueError(f"block sizes must sum to {ROW_COUNT}")
    if sum(threshold - 1 for threshold in thresholds) >= WITNESS_SIZE:
        raise ValueError("pigeonhole condition sum(h_j-1) < 35 is required")
    if any(threshold < FACE_SIZE for threshold in thresholds):
        raise ValueError("every local witness threshold must be at least eight")
    if any(not 2 <= color_count <= 8 for color_count in colors):
        raise ValueError("color counts must lie in 2..8")

    hints = load_hint(args.hint, block_sizes, thresholds, colors)
    model = cp_model.CpModel()
    block_data = []
    objective_terms = []

    for block_index, (size, threshold, color_count, hint) in enumerate(
        zip(block_sizes, thresholds, colors, hints)
    ):
        color_sizes = balanced_sizes(size, color_count)
        faces = tuple(compositions(FACE_SIZE, color_count))
        witnesses = tuple(compositions(threshold, color_count))
        weights = tuple(pattern_weight(face, color_sizes) for face in faces)
        face_index = {face: index for index, face in enumerate(faces)}
        if any(face not in face_index for face in hint):
            raise ValueError(f"hint for block {block_index} has an inadmissible pattern")

        selected = [
            model.new_bool_var(f"x_{block_index}_{face_index}")
            for face_index in range(len(faces))
        ]
        cover_lists = []
        for witness in witnesses:
            covered_by = [
                index
                for index, face in enumerate(faces)
                if all(left <= right for left, right in zip(face, witness))
            ]
            if not covered_by:
                raise RuntimeError(
                    f"uncoverable block {block_index} witness pattern: {witness}"
                )
            model.add(sum(selected[index] for index in covered_by) >= 1)
            cover_lists.append(covered_by)

        hinted = set(hint)
        for face, variable in zip(faces, selected):
            model.add_hint(variable, int(face in hinted))
        objective_terms.extend(
            weight * variable for weight, variable in zip(weights, selected)
        )
        block_data.append(
            (color_sizes, faces, witnesses, weights, selected, cover_lists, hint)
        )

    model.minimize(sum(objective_terms))
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.random_seed
    solver.parameters.log_search_progress = False
    status = solver.solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        raise RuntimeError(f"CP-SAT returned {solver.status_name(status)}")

    block_records = []
    exact_total = 0
    for block_index, (
        size,
        threshold,
        color_count,
        data,
    ) in enumerate(zip(block_sizes, thresholds, colors, block_data)):
        color_sizes, faces, witnesses, weights, selected, cover_lists, hint = data
        chosen_indices = tuple(
            index for index, variable in enumerate(selected) if solver.boolean_value(variable)
        )
        chosen = tuple(faces[index] for index in chosen_indices)
        chosen_set = set(chosen_indices)
        multiplicities = tuple(
            sum(index in chosen_set for index in cover_list)
            for cover_list in cover_lists
        )
        if min(multiplicities) < 1:
            raise RuntimeError(f"block {block_index} does not cover every witness")
        exact_size = sum(weights[index] for index in chosen_indices)
        exact_total += exact_size
        block_records.append(
            {
                "block_index": block_index,
                "block_size": size,
                "local_witness_size": threshold,
                "colors": color_count,
                "color_sizes": list(color_sizes),
                "face_pattern_count": len(faces),
                "witness_pattern_count": len(witnesses),
                "selected_pattern_count": len(chosen),
                "selected_patterns": [list(face) for face in chosen],
                "exact_selected_eight_subsets": exact_size,
                "minimum_witness_cover_multiplicity": min(multiplicities),
                "maximum_witness_cover_multiplicity": max(multiplicities),
                "hint_pattern_count": len(hint),
                "hint_exact_selected_eight_subsets": sum(
                    pattern_weight(face, color_sizes) for face in hint
                ),
            }
        )

    rounded_objective = round(solver.objective_value)
    if exact_total != rounded_objective:
        raise RuntimeError("exact objective and CP-SAT objective disagree")
    report = {
        "schema": "atlas-nonuniform-hierarchical-cover-cp-sat/v1",
        "status": solver.status_name(status),
        "row_count": ROW_COUNT,
        "global_witness_size": WITNESS_SIZE,
        "face_size": FACE_SIZE,
        "block_sizes": list(block_sizes),
        "local_witness_sizes": list(thresholds),
        "pigeonhole_budget": sum(threshold - 1 for threshold in thresholds),
        "block_records": block_records,
        "exact_selected_eight_subsets": exact_total,
        "best_objective_bound": int(math.ceil(solver.best_objective_bound)),
        "relative_bound_gap": (exact_total - solver.best_objective_bound) / exact_total,
        "wall_time_seconds": solver.wall_time,
        "branches": solver.num_branches,
        "conflicts": solver.num_conflicts,
        "random_seed": args.random_seed,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode("ascii")
    report["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="ascii")
    print(
        "{} Atlas nonuniform blocks={} selected={} bound={} gap={:.9f} seconds={:.3f}".format(
            report["status"],
            len(block_sizes),
            exact_total,
            report["best_objective_bound"],
            report["relative_bound_gap"],
            report["wall_time_seconds"],
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
