#!/usr/bin/env python3
"""Locally replay the source-bound cell-5 xi=3 pairings 7, 8, and 11."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path

from replay_kb_mca_v4_433_1b_cell5_xi3_pairings345_v1 import (
    PRIME,
    evaluate_row,
    load_compiler,
    make_structure,
)


SOURCE_COMMIT = "28b3bc8ab13e94c25088e904251eb5cf49e68ad2"
SOURCE_HASHES = {
    "template_7": "ed5c0a3883180e43e2f380fc76971a4a645fe0260679ed27374cd2bfc844d2df",
    "template_8": "58ed9e191436e0a629d2c7a263151d50d54910d226eee4c35c0bb55abf2a1b8b",
    "template_11": "8f2fe8ca53863b2220ae60558b3f8d64269eec0f3952138679f2bc3a7069698b",
    "tower": "68c18173d4133f66a85136b1ecc33235f7e979c26b6f96d8592030901a8a335c",
    "kernel": "627a8df8bb8a2da4e11488658d1c2145b8c65ef7fbcef3f0f4f53f9d05ea752d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_paths(dag_root: Path) -> dict[str, Path]:
    directory = dag_root / "experiments/prize_resolution"
    return {
        "template_7": directory / (
            "rate_half_kb_positive_433_1b_cell4_xi3_"
            "pairing7_quadratic_resultant_signfree_modal.py"
        ),
        "template_8": directory / (
            "rate_half_kb_positive_433_1b_cell4_xi3_"
            "pairing8_quadratic_resultant_signfree_modal.py"
        ),
        "template_11": directory / (
            "rate_half_kb_positive_433_1b_cell4_xi3_"
            "pairing11_quadratic_resultant_signfree_modal.py"
        ),
        "tower": directory / (
            "rate_half_kb_positive_433_1b_cell5_four_basis_tower_result.json"
        ),
        "kernel": directory / (
            "rate_half_kb_positive_433_1b_cell5_compact_kernel_result.json"
        ),
    }


def verify_sources(dag_root: Path, paths: dict[str, Path]) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=dag_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if head != SOURCE_COMMIT:
        raise RuntimeError(f"source commit mismatch: {head}")
    observed = {name: sha256(path) for name, path in paths.items()}
    if observed != SOURCE_HASHES:
        raise RuntimeError(f"source hash mismatch: {observed}")


def all_cases() -> tuple[tuple[int, ...], ...]:
    signs = tuple(itertools.product((-1, 1), repeat=2))
    return tuple(
        (*epsilon, sigma_c, pairing)
        for pairing in (7, 8, 11)
        for epsilon in signs
        for sigma_c in (-1, 1)
    )


def parse_indices(text: str) -> list[int]:
    if text == "all":
        return list(range(24))
    indices = sorted({int(value) for value in text.split(",") if value})
    if any(index < 0 or index >= 24 for index in indices):
        raise ValueError("indices must lie in 0..23")
    return indices


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dag-root", required=True, type=Path)
    parser.add_argument("--indices", default="all")
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()

    paths = source_paths(arguments.dag_root)
    verify_sources(arguments.dag_root, paths)
    tower = json.loads(paths["tower"].read_text())
    structure = arguments.output.with_suffix(".structure.json")
    make_structure(tower, structure)
    compilers = {
        pairing: load_compiler(paths[f"template_{pairing}"], structure, paths["kernel"])
        for pairing in (7, 8, 11)
    }
    rows = []
    cases = all_cases()
    for index in parse_indices(arguments.indices):
        started = time.perf_counter()
        row = dict(evaluate_row(cases[index], compilers, tower))
        row.pop("timings", None)
        row["local_case_index"] = index
        row["local_elapsed_seconds"] = round(time.perf_counter() - started, 6)
        rows.append(row)
        print(json.dumps({
            "case_index": index,
            "case": cases[index],
            "status": row["status"],
            "target_excluded": row["target_excluded"],
            "witness_count": row["witness_count"],
            "unresolved": row["unresolved"],
        }, sort_keys=True), flush=True)
    structure.unlink()
    payload = {
        "schema": "kb-mca-v4-433-1b-cell5-xi3-pairings7811-raw-replay-v1",
        "field": PRIME,
        "source_commit": SOURCE_COMMIT,
        "source_sha256": SOURCE_HASHES,
        "rows": rows,
    }
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
