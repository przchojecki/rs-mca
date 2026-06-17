#!/usr/bin/env python3
"""Run the psi_2 restricted-subset frontier scan.

Proof status: EXPERIMENTAL. This script is a deterministic heuristic scanner,
not a proof. It reports the exact parameters, object checked, and output path
used for each run.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import numpy as np
from sympy import primitive_root


PROOF_STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "psi2-restricted-subset-frontier-scan"
DETERMINISM = "deterministic; no random seed"
DEFAULT_N = 32
DEFAULT_L = 18
DEFAULT_CHUNK_CELLS = 15_000_000
DEFAULT_OUTPUT = "frontier_results.txt"


def subgroup(p: int, order: int) -> list[int]:
    if (p - 1) % order != 0:
        raise ValueError(f"expected order={order} to divide p-1 for p={p}")
    generator = primitive_root(p)
    step = (p - 1) // order
    return [pow(generator, step * i, p) for i in range(order)]


def half_states(
    elems: list[int],
    p: int,
    lmax: int,
) -> dict[int, tuple[np.ndarray[Any, np.dtype[np.int64]], np.ndarray[Any, np.dtype[np.int64]]]]:
    by_size: dict[int, set[tuple[int, int]]] = {0: {(0, 0)}}
    for x_value in elems:
        new_states: dict[int, set[tuple[int, int]]] = {}
        for size, states in by_size.items():
            if size + 1 > lmax:
                continue
            target = new_states.setdefault(size + 1, set())
            for first_sum, second_sum in states:
                target.add(
                    (
                        (first_sum + x_value) % p,
                        (second_sum + first_sum * x_value) % p,
                    )
                )
        for size, states in new_states.items():
            by_size.setdefault(size, set()).update(states)

    output: dict[
        int,
        tuple[np.ndarray[Any, np.dtype[np.int64]], np.ndarray[Any, np.dtype[np.int64]]],
    ] = {}
    for size, states in by_size.items():
        if not states:
            continue
        array = np.array(sorted(states), dtype=np.int64)
        output[size] = (array[:, 0].copy(), array[:, 1].copy())
    return output


def psi2_cover(
    p: int,
    order: int,
    subset_size: int,
    chunk_cells: int,
) -> tuple[int, int]:
    quotient = subgroup(p, order)
    half = order // 2
    left_states = half_states(quotient[:half], p, subset_size)
    right_states = half_states(quotient[half:], p, subset_size)
    bitmap = np.zeros(p * p, dtype=bool)

    for left_size in range(0, subset_size + 1):
        right_size = subset_size - left_size
        if left_size not in left_states or right_size not in right_states:
            continue

        first_left, second_left = left_states[left_size]
        first_right, second_right = right_states[right_size]
        chunk = max(1, chunk_cells // max(1, len(first_right)))
        for start in range(0, len(first_left), chunk):
            first_left_slice = first_left[start : start + chunk, None]
            second_left_slice = second_left[start : start + chunk, None]
            first_fingerprint = (
                first_left_slice + first_right[None, :]
            ) % p
            second_fingerprint = (
                second_left_slice
                + second_right[None, :]
                + first_left_slice * first_right[None, :]
            ) % p
            bitmap[(first_fingerprint * p + second_fingerprint).ravel()] = True

    return int(bitmap.sum()), p * p


def scan_prime(
    p: int,
    order: int,
    subset_size: int,
    chunk_cells: int,
) -> dict[str, Any]:
    start_time = time.time()
    covered, total = psi2_cover(p, order, subset_size, chunk_cells)
    elapsed_seconds = time.time() - start_time
    return {
        "p": p,
        "N": order,
        "l": subset_size,
        "covered": covered,
        "total": total,
        "onto": covered == total,
        "missing": total - covered,
        "elapsed_seconds": elapsed_seconds,
    }


def format_result(result: dict[str, Any]) -> str:
    return (
        f"p={result['p']:>6} N={result['N']:>3} l={result['l']:>3}: "
        f"coverage {result['covered']:>9}/{result['total']:<9} "
        f"onto={str(result['onto']):>5} "
        f"missing={result['missing']:<8} "
        f"[{result['elapsed_seconds']:5.1f}s]"
    )


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    results = [
        scan_prime(prime, args.order, args.subset_size, args.chunk_cells)
        for prime in args.primes
    ]
    return {
        "metadata": {
            "proof_status": PROOF_STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "determinism": DETERMINISM,
            "object_checked": (
                "psi_2 elementary-symmetric fingerprints for l-element "
                "subsets of an order-N subgroup of F_p^*"
            ),
            "N": args.order,
            "l": args.subset_size,
            "chunk_cells": args.chunk_cells,
            "output_path": str(args.output) if args.output else None,
            "write_output": not args.no_write,
        },
        "results": results,
    }


def format_text(report: dict[str, Any]) -> str:
    metadata = report["metadata"]
    lines = [
        "Frontier psi_2 scan",
        f"proof_status: {metadata['proof_status']}",
        f"theorem_problem_id: {metadata['theorem_problem_id']}",
        f"determinism: {metadata['determinism']}",
        f"object_checked: {metadata['object_checked']}",
        f"parameters: N={metadata['N']} l={metadata['l']} "
        f"chunk_cells={metadata['chunk_cells']}",
        f"output_path: {metadata['output_path']}",
        f"write_output: {metadata['write_output']}",
        "results:",
    ]
    if not report["results"]:
        lines.append("  - <none>")
    else:
        lines.extend(f"  - {format_result(result)}" for result in report["results"])
    return "\n".join(lines)


def append_results(output_path: Path, report: dict[str, Any]) -> None:
    metadata = report["metadata"]
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(
            "# "
            f"proof_status={metadata['proof_status']} "
            f"theorem_problem_id={metadata['theorem_problem_id']} "
            f"N={metadata['N']} l={metadata['l']} "
            f"chunk_cells={metadata['chunk_cells']}\n"
        )
        for result in report["results"]:
            handle.write(format_result(result) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the psi_2 restricted-subset frontier scan."
    )
    parser.add_argument(
        "primes",
        metavar="p",
        nargs="+",
        type=int,
        help="Prime fields to scan. The subgroup order N must divide p-1.",
    )
    parser.add_argument(
        "-N",
        "--order",
        type=int,
        default=DEFAULT_N,
        help=f"Multiplicative subgroup order. Defaults to {DEFAULT_N}.",
    )
    parser.add_argument(
        "-l",
        "--subset-size",
        type=int,
        default=DEFAULT_L,
        help=f"Subset size for the psi_2 scan. Defaults to {DEFAULT_L}.",
    )
    parser.add_argument(
        "--chunk-cells",
        type=int,
        default=DEFAULT_CHUNK_CELLS,
        help=(
            "Approximate maximum broadcast cell budget per chunk. "
            f"Defaults to {DEFAULT_CHUNK_CELLS}."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(DEFAULT_OUTPUT),
        help=(
            "Text file to append run metadata and result lines to. "
            f"Defaults to {DEFAULT_OUTPUT}."
        ),
    )
    parser.add_argument(
        "--no-write",
        action="store_true",
        help="Do not append result lines to an output file.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Stdout format. Defaults to text.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report), flush=True)

    if not args.no_write and args.output:
        append_results(args.output, report)


if __name__ == "__main__":
    main()
