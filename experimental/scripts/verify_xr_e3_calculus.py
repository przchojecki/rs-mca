#!/usr/bin/env python3
"""Verify xr_e3_calculus.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Callable, Iterable


REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "experimental" / "data" / "certificates" / "xr-e3-calculus" / "xr_e3_calculus.json"


Vertex = tuple[int, ...]
Predicate = Callable[[Vertex], bool]


@dataclass(frozen=True)
class CheckResult:
    name: str
    status: str
    details: list[str]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vertices(n: int, j: int) -> list[Vertex]:
    return list(combinations(range(n), j))


def neighbors(vertex: Vertex, n: int) -> Iterable[Vertex]:
    present = set(vertex)
    missing = [x for x in range(n) if x not in present]
    for removed in vertex:
        base = present - {removed}
        for added in missing:
            yield tuple(sorted(base | {added}))


def degree(n: int, j: int) -> int:
    return j * (n - j)


def endpoint_correlation(n: int, j: int, predicate: Predicate, steps: int) -> Fraction:
    verts = vertices(n, j)
    total = len(verts)
    weights: dict[Vertex, Fraction] = {
        v: Fraction(1, total) for v in verts if predicate(v)
    }
    if steps == 0:
        return sum(weights.values(), Fraction(0, 1))
    deg = degree(n, j)
    for _ in range(steps):
        nxt: Counter[Vertex] = Counter()
        for v, weight in weights.items():
            share = weight / deg
            for nb in neighbors(v, n):
                nxt[nb] += share
        weights = dict(nxt)
    return sum(weight for v, weight in weights.items() if predicate(v))


def killed_energy(n: int, j: int, predicate: Predicate, steps: int) -> Fraction:
    verts = vertices(n, j)
    total = len(verts)
    weights: dict[Vertex, Fraction] = {
        v: Fraction(1, total) for v in verts if predicate(v)
    }
    if steps == 0:
        return sum(weights.values(), Fraction(0, 1))
    deg = degree(n, j)
    for _ in range(steps):
        nxt: Counter[Vertex] = Counter()
        for v, weight in weights.items():
            share = weight / deg
            for nb in neighbors(v, n):
                if predicate(nb):
                    nxt[nb] += share
        weights = dict(nxt)
    return sum(weights.values(), Fraction(0, 1))


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "float": float(value),
        "log2": math.log2(float(value)) if value > 0 else None,
    }


def fixed_core_predicate(c: int) -> Predicate:
    core = set(range(c))
    return lambda vertex: core.issubset(vertex)


def fixed_core_density(n: int, j: int, c: int) -> Fraction:
    if c > j:
        return Fraction(0, 1)
    return Fraction(math.comb(n - c, j - c), math.comb(n, j))


def fixed_core_killed_formula(n: int, j: int, c: int, steps: int) -> Fraction:
    return fixed_core_density(n, j, c) * Fraction(j - c, j) ** steps


def point_dictator_endpoint_formula(n: int, j: int, steps: int) -> Fraction:
    delta = Fraction(j, n)
    lam = Fraction(1, 1) - Fraction(n, j * (n - j))
    return delta * delta + (lam ** steps) * delta * (1 - delta)


def block_profile_predicate(blocks: list[set[int]], profile: tuple[int, ...]) -> Predicate:
    def predicate(vertex: Vertex) -> bool:
        v = set(vertex)
        return tuple(len(v & block) for block in blocks) == profile

    return predicate


def block_profile_density(n: int, j: int, block_sizes: tuple[int, ...], profile: tuple[int, ...]) -> Fraction:
    count = 1
    for size, selected in zip(block_sizes, profile):
        count *= math.comb(size, selected)
    return Fraction(count, math.comb(n, j))


def block_profile_gamma(n: int, j: int, block_sizes: tuple[int, ...], profile: tuple[int, ...]) -> Fraction:
    internal = sum(selected * (size - selected) for size, selected in zip(block_sizes, profile))
    return Fraction(internal, degree(n, j))


def block_profile_killed_formula(
    n: int,
    j: int,
    block_sizes: tuple[int, ...],
    profile: tuple[int, ...],
    steps: int,
) -> Fraction:
    return block_profile_density(n, j, block_sizes, profile) * block_profile_gamma(n, j, block_sizes, profile) ** steps


def make_blocks(block_sizes: tuple[int, ...]) -> list[set[int]]:
    blocks = []
    cursor = 0
    for size in block_sizes:
        blocks.append(set(range(cursor, cursor + size)))
        cursor += size
    return blocks


def check_endpoint_e2_consistency() -> tuple[CheckResult, list[dict[str, object]]]:
    rows = []
    for n, j in [(6, 2), (8, 3), (12, 4), (16, 8)]:
        predicate = fixed_core_predicate(1)
        for steps in [0, 1, 2, 3]:
            observed = endpoint_correlation(n, j, predicate, steps)
            expected = point_dictator_endpoint_formula(n, j, steps)
            require(observed == expected, f"point dictator endpoint formula failed for {(n, j, steps)}")
        delta = Fraction(j, n)
        lam = Fraction(1, 1) - Fraction(n, j * (n - j))
        c2 = endpoint_correlation(n, j, predicate, 2)
        rows.append(
            {
                "n": n,
                "j": j,
                "delta": fraction_record(delta),
                "lambda": fraction_record(lam),
                "C_2": fraction_record(c2),
                "C_2_minus_delta_squared": fraction_record(c2 - delta * delta),
                "lambda_squared_variance": fraction_record(lam * lam * delta * (1 - delta)),
            }
        )
    return (
        CheckResult(
            "endpoint E2 consistency",
            "PASS",
            [
                "checked C_s(point dictator)=delta^2+lambda^s delta(1-delta) for s=0..3",
                "C_2-delta^2 equals lambda^2 times the Johnson first-mode variance",
            ],
        ),
        rows,
    )


def check_fixed_core_killed_e3() -> tuple[CheckResult, list[dict[str, object]]]:
    rows = []
    for n, j, c in [(12, 4, 1), (12, 4, 2), (16, 8, 2), (12, 6, 3)]:
        predicate = fixed_core_predicate(c)
        for steps in [0, 1, 2, 3]:
            observed = killed_energy(n, j, predicate, steps)
            expected = fixed_core_killed_formula(n, j, c, steps)
            require(observed == expected, f"fixed-core killed formula failed for {(n, j, c, steps)}")
        density = fixed_core_density(n, j, c)
        k3 = fixed_core_killed_formula(n, j, c, 3)
        random_baseline = density ** 4
        rows.append(
            {
                "n": n,
                "j": j,
                "core_size": c,
                "density": fraction_record(density),
                "K_3": fraction_record(k3),
                "random_same_density_delta^4": fraction_record(random_baseline),
                "K_3_over_delta^4": fraction_record(k3 / random_baseline) if random_baseline else None,
            }
        )
    return (
        CheckResult(
            "fixed-core killed E3",
            "PASS",
            [
                "checked K_s(A_C)=density*((j-c)/j)^s for s=0..3",
                "fixed-core K_3 is explicitly large relative to the independent delta^4 baseline in the tested paid models",
            ],
        ),
        rows,
    )


def check_block_profile_killed_e3() -> tuple[CheckResult, list[dict[str, object]]]:
    cases = [
        ("balanced_four_blocks", 16, 8, (4, 4, 4, 4), (2, 2, 2, 2)),
        ("unbalanced_active", 16, 8, (4, 4, 4, 4), (3, 2, 2, 1)),
        ("frozen_full_blocks", 16, 8, (4, 4, 4, 4), (4, 4, 0, 0)),
    ]
    rows = []
    for name, n, j, block_sizes, profile in cases:
        predicate = block_profile_predicate(make_blocks(block_sizes), profile)
        for steps in [0, 1, 2, 3]:
            observed = killed_energy(n, j, predicate, steps)
            expected = block_profile_killed_formula(n, j, block_sizes, profile, steps)
            require(observed == expected, f"block-profile killed formula failed for {name}, step {steps}")
        gamma = block_profile_gamma(n, j, block_sizes, profile)
        k3 = block_profile_killed_formula(n, j, block_sizes, profile, 3)
        rows.append(
            {
                "name": name,
                "n": n,
                "j": j,
                "block_sizes": list(block_sizes),
                "profile": list(profile),
                "density": fraction_record(block_profile_density(n, j, block_sizes, profile)),
                "gamma": fraction_record(gamma),
                "K_3": fraction_record(k3),
                "active_profile": gamma > 0,
            }
        )
    require(rows[0]["active_profile"] is True and rows[0]["K_3"]["numerator"] > 0, "balanced profile should be active")
    require(rows[-1]["active_profile"] is False and rows[-1]["K_3"]["numerator"] == 0, "frozen full blocks should be invisible")
    return (
        CheckResult(
            "block-profile killed E3",
            "PASS",
            [
                "checked K_s(profile)=density*gamma^s for s=0..3",
                "active folded profiles have positive K_3",
                "frozen full-block quotient profile has gamma=0 and K_3=0",
            ],
        ),
        rows,
    )


def build_result() -> dict[str, object]:
    endpoint_check, endpoint_rows = check_endpoint_e2_consistency()
    core_check, core_rows = check_fixed_core_killed_e3()
    profile_check, profile_rows = check_block_profile_killed_e3()
    script = Path(__file__).resolve()
    return {
        "status": "PROVED_XR_E3_CALCULUS",
        "dag_nodes": ["xr_e3_calculus"],
        "object": "Johnson endpoint correlation and killed exchange energy",
        "script": str(script.relative_to(REPO)),
        "script_sha256": file_sha256(script),
        "checks": [asdict(endpoint_check), asdict(core_check), asdict(profile_check)],
        "endpoint_e2_rows": endpoint_rows,
        "fixed_core_killed_e3_rows": core_rows,
        "block_profile_killed_e3_rows": profile_rows,
        "non_claims": [
            "does not prove the XR inverse theorem",
            "does not enumerate Reed-Solomon word-pair aligned-locator sets",
            "does not certify an M1 or list threshold",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    parser.add_argument("--check", default=str(OUT), help="certificate path to replay")
    args = parser.parse_args()

    result = build_result()
    if args.emit:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUT.relative_to(REPO)}")
    else:
        expected = json.loads(Path(args.check).read_text())
        require(expected == result, "certificate does not match verifier output; rerun with --emit")
        print(result["status"])
        for check in result["checks"]:
            print(f"  {check['name']}: {check['status']}")


if __name__ == "__main__":
    main()
