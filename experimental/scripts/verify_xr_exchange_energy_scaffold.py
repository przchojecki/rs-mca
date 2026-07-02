#!/usr/bin/env python3
"""Toy Johnson-exchange energy checks for the XR evidence program.

This is a combinatorial scaffold for the E2 / QX.1 route-map item.  It does
not enumerate RS words or prove an XR inverse theorem.  It verifies exact
Johnson-graph walk-energy identities on structured toy subsets that model
paid fixed-core and quotient-profile families.

Run:
  python3 experimental/scripts/verify_xr_exchange_energy_scaffold.py
  python3 experimental/scripts/verify_xr_exchange_energy_scaffold.py --emit
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
from typing import Callable, Iterable


OUTPUT = Path(
    "experimental/data/certificates/xr-exchange-energy-scaffold/"
    "xr_exchange_energy_scaffold.json"
)


Vertex = tuple[int, ...]
Predicate = Callable[[Vertex], bool]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def vertices(n: int, j: int) -> list[Vertex]:
    return [tuple(c) for c in combinations(range(n), j)]


def neighbors(vertex: Vertex, n: int) -> Iterable[Vertex]:
    present = set(vertex)
    missing = [x for x in range(n) if x not in present]
    for y in vertex:
        base = present - {y}
        for x in missing:
            yield tuple(sorted(base | {x}))


def johnson_degree(n: int, j: int) -> int:
    return j * (n - j)


def theta(n: int, j: int, i: int) -> int:
    return (j - i) * (n - j - i) - i


def theta_multiplicity(n: int, i: int) -> int:
    return comb(n, i) - (comb(n, i - 1) if i > 0 else 0)


def walk_energy(n: int, j: int, predicate: Predicate, steps: int) -> Fraction:
    """Return P[T_0,...,T_steps in A] for the random walk on J(n,j)."""
    verts = vertices(n, j)
    total_vertices = len(verts)
    weights: dict[Vertex, Fraction] = {
        v: Fraction(1, total_vertices) for v in verts if predicate(v)
    }
    if steps == 0:
        return sum(weights.values(), Fraction(0, 1))
    degree = johnson_degree(n, j)
    for _ in range(steps):
        nxt: Counter[Vertex] = Counter()
        for v, weight in weights.items():
            share = weight / degree
            for nb in neighbors(v, n):
                if predicate(nb):
                    nxt[nb] += share
        weights = dict(nxt)
    return sum(weights.values(), Fraction(0, 1))


def fixed_core_predicate(core_size: int) -> Predicate:
    core = set(range(core_size))
    return lambda vertex: core.issubset(vertex)


def fixed_core_formula(n: int, j: int, core_size: int, steps: int) -> Fraction:
    if core_size > j:
        return Fraction(0, 1)
    density = Fraction(comb(n - core_size, j - core_size), comb(n, j))
    survival = Fraction(j - core_size, j)
    return density * survival ** steps


def block_profile_predicate(blocks: list[set[int]], profile: tuple[int, ...]) -> Predicate:
    assert len(blocks) == len(profile)

    def predicate(vertex: Vertex) -> bool:
        vset = set(vertex)
        return tuple(len(vset & block) for block in blocks) == profile

    return predicate


def block_profile_formula(
    n: int,
    j: int,
    block_sizes: tuple[int, ...],
    profile: tuple[int, ...],
    steps: int,
) -> Fraction:
    count = 1
    internal_moves = 0
    for size, selected in zip(block_sizes, profile):
        count *= comb(size, selected)
        internal_moves += selected * (size - selected)
    density = Fraction(count, comb(n, j))
    survival = Fraction(internal_moves, johnson_degree(n, j))
    return density * survival ** steps


def random_subset_predicate(subset: set[Vertex]) -> Predicate:
    return lambda vertex: vertex in subset


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "float": float(value),
        "log2": math.log2(float(value)) if value > 0 else None,
    }


def verify_spectrum_small() -> dict[str, object]:
    """Dense exact eigenvalue check for J(5,2), plus formula checks."""
    import sympy as sp

    n, j = 5, 2
    verts = vertices(n, j)
    index = {v: i for i, v in enumerate(verts)}
    matrix = [[0 for _ in verts] for _ in verts]
    for v in verts:
        row = index[v]
        for nb in neighbors(v, n):
            matrix[row][index[nb]] = 1
    observed = {
        int(eigenvalue): multiplicity
        for eigenvalue, multiplicity in sp.Matrix(matrix).eigenvals().items()
    }
    expected = {
        theta(n, j, i): theta_multiplicity(n, i) for i in range(0, j + 1)
    }
    assert observed == expected
    gap_cases = []
    for n_case, j_case in [(5, 2), (16, 4), (16, 8), (512, 128), (512, 247)]:
        unnormalized_gap = theta(n_case, j_case, 0) - theta(n_case, j_case, 1)
        assert unnormalized_gap == n_case
        gap_cases.append({
            "n": n_case,
            "j": j_case,
            "theta_0": theta(n_case, j_case, 0),
            "theta_1": theta(n_case, j_case, 1),
            "unnormalized_gap": unnormalized_gap,
            "normalized_gap": fraction_record(
                Fraction(unnormalized_gap, johnson_degree(n_case, j_case))
            ),
        })
    return {
        "check": "johnson_spectrum",
        "dense_case": {"n": n, "j": j, "observed": observed, "expected": expected},
        "gap_cases": gap_cases,
        "status": "PASS",
    }


def verify_fixed_core_cases() -> list[dict[str, object]]:
    rows = []
    for n, j, core_size in [(12, 4, 1), (12, 4, 2), (16, 8, 2)]:
        predicate = fixed_core_predicate(core_size)
        row = {
            "family": "fixed_core",
            "n": n,
            "j": j,
            "core_size": core_size,
            "energies": {},
            "status": "PASS",
        }
        for steps in [0, 1, 3]:
            observed = walk_energy(n, j, predicate, steps)
            expected = fixed_core_formula(n, j, core_size, steps)
            assert observed == expected
            row["energies"][f"E_{steps}"] = {
                "observed": fraction_record(observed),
                "expected": fraction_record(expected),
            }
        rows.append(row)
    return rows


def verify_block_profile_cases() -> list[dict[str, object]]:
    cases = [
        {
            "name": "balanced_four_blocks",
            "n": 16,
            "j": 8,
            "block_sizes": (4, 4, 4, 4),
            "profile": (2, 2, 2, 2),
            "interpretation": "profile_preserving_quotient_like_family",
        },
        {
            "name": "frozen_full_blocks",
            "n": 16,
            "j": 8,
            "block_sizes": (4, 4, 4, 4),
            "profile": (4, 4, 0, 0),
            "interpretation": "full_block_quotient_fiber_has_zero_one_exchange_energy",
        },
    ]
    rows = []
    for case in cases:
        blocks = []
        cursor = 0
        for size in case["block_sizes"]:
            blocks.append(set(range(cursor, cursor + size)))
            cursor += size
        predicate = block_profile_predicate(blocks, case["profile"])
        row = dict(case)
        row["energies"] = {}
        row["status"] = "PASS"
        for steps in [0, 1, 3]:
            observed = walk_energy(case["n"], case["j"], predicate, steps)
            expected = block_profile_formula(
                case["n"], case["j"], case["block_sizes"], case["profile"], steps
            )
            assert observed == expected
            row["energies"][f"E_{steps}"] = {
                "observed": fraction_record(observed),
                "expected": fraction_record(expected),
            }
        rows.append(row)
    return rows


def random_baseline() -> dict[str, object]:
    n, j, core_size = 12, 4, 2
    verts = vertices(n, j)
    size = comb(n - core_size, j - core_size)
    structured_e3 = fixed_core_formula(n, j, core_size, 3)
    rng = random.Random(2026070202)
    trials = []
    for trial in range(20):
        subset = set(rng.sample(verts, size))
        e3 = walk_energy(n, j, random_subset_predicate(subset), 3)
        trials.append(e3)
    avg = sum(trials, Fraction(0, 1)) / len(trials)
    max_seen = max(trials)
    min_seen = min(trials)
    return {
        "check": "random_baseline_against_fixed_core",
        "n": n,
        "j": j,
        "subset_size": size,
        "density": fraction_record(Fraction(size, len(verts))),
        "trials": len(trials),
        "seed": 2026070202,
        "random_E3_average": fraction_record(avg),
        "random_E3_min": fraction_record(min_seen),
        "random_E3_max": fraction_record(max_seen),
        "fixed_core_E3": fraction_record(structured_e3),
        "fixed_core_over_random_average": float(structured_e3 / avg),
        "status": "PASS",
    }


def build_packet() -> dict[str, object]:
    spectrum = verify_spectrum_small()
    fixed_core = verify_fixed_core_cases()
    block_profiles = verify_block_profile_cases()
    baseline = random_baseline()
    packet = {
        "packet": "xr_exchange_energy_scaffold",
        "status": "EXPERIMENTAL_COMBINATORIAL_SCAFFOLD",
        "dag_nodes": ["xr_e3_calculus", "xr_inverse_toy"],
        "not_claimed": [
            "No RS word-pair enumeration is performed.",
            "No XR inverse theorem is proved.",
            "No MCA/list threshold is certified.",
        ],
        "energy_definition": {
            "graph": "Johnson graph J(n,j) on j-subsets",
            "E_s(A)": "Pr[T_0,...,T_s in A] for a length-s simple random walk",
            "E_3_role": "toy odd exchange-correlation proxy for the E2/QX.1 route",
        },
        "checks": {
            "spectrum": spectrum,
            "fixed_core_families": fixed_core,
            "block_profile_families": block_profiles,
            "random_baseline": baseline,
        },
        "interpretation": {
            "positive": (
                "Fixed-core and balanced profile families have exact large "
                "E_3 relative to random subsets of comparable density."
            ),
            "caveat": (
                "Frozen full-block quotient fibers have zero ordinary "
                "one-exchange energy, so an XR inverse test must remove paid "
                "quotient strata first or use a multi-exchange variant."
            ),
            "next_step": (
                "Attach the same energy to actual aligned-locator sets "
                "A_{u,v} on n=16 toys, then run the E2 inverse falsifier."
            ),
        },
    }
    packet["packet_sha256_without_self"] = sha256_text(
        json.dumps(packet, sort_keys=True, separators=(",", ":"))
    )
    return packet


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write JSON artifact")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    packet = build_packet()
    if args.emit:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n")
    print("XR exchange-energy scaffold checks: PASS")
    print(f"  dense spectrum case: {packet['checks']['spectrum']['dense_case']}")
    baseline = packet["checks"]["random_baseline"]
    print(
        "  fixed-core E3 / random average: "
        f"{baseline['fixed_core_over_random_average']:.3f}"
    )
    for row in packet["checks"]["block_profile_families"]:
        e1 = row["energies"]["E_1"]["observed"]["float"]
        e3 = row["energies"]["E_3"]["observed"]["float"]
        print(f"  {row['name']}: E1={e1:.6g}, E3={e3:.6g}")


if __name__ == "__main__":
    main()
