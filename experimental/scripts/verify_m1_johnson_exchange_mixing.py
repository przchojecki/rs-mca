#!/usr/bin/env python3
"""Verify Johnson exchange-mixing lemmas for the XR support side.

The theorem is symbolic: for the Johnson graph J(n,j), degree d=j(n-j),
and any family A of j-subsets with density delta,

    E_1(A) <= delta^2 + (1 - n/d) delta(1-delta),

where E_1(A)=Pr[T_0,T_1 in A] for the one-exchange walk.  Equality is attained
by a point-dictator family {T: x in T}.  The proof note derives this from the
standard Johnson eigenvalue gap theta_0-theta_1=n.

The verifier also checks the endpoint multi-exchange bound

    Pr[T_0 in A and T_s in A] <= delta^2 + lambda_*^s delta(1-delta),

where lambda_* is the largest absolute nontrivial normalized Johnson
eigenvalue.  This is the reusable endpoint form for multi-exchange XR tests.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import combinations
import json
from math import comb
from pathlib import Path
import random


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m1-johnson-exchange-mixing"
    / "m1_johnson_exchange_mixing_certificate.json"
)


Vertex = tuple[int, ...]


def vertices(n: int, j: int) -> list[Vertex]:
    return [tuple(c) for c in combinations(range(n), j)]


def neighbors(vertex: Vertex, n: int) -> list[Vertex]:
    present = set(vertex)
    missing = [x for x in range(n) if x not in present]
    out = []
    for y in vertex:
        base = present - {y}
        for x in missing:
            out.append(tuple(sorted(base | {x})))
    return out


def degree(n: int, j: int) -> int:
    return j * (n - j)


def theta(n: int, j: int, i: int) -> int:
    return (j - i) * (n - j - i) - i


def lambda_second(n: int, j: int) -> Fraction:
    return Fraction(theta(n, j, 1), theta(n, j, 0))


def lambda_abs(n: int, j: int) -> Fraction:
    top = theta(n, j, 0)
    max_i = min(j, n - j)
    return max(Fraction(abs(theta(n, j, i)), top) for i in range(1, max_i + 1))


def density(n: int, j: int, family: set[Vertex]) -> Fraction:
    return Fraction(len(family), comb(n, j))


def one_exchange_energy(n: int, j: int, family: set[Vertex]) -> Fraction:
    if not family:
        return Fraction(0, 1)
    fam = set(family)
    directed_internal = 0
    for vertex in fam:
        directed_internal += sum(1 for nb in neighbors(vertex, n) if nb in fam)
    return Fraction(directed_internal, comb(n, j) * degree(n, j))


def endpoint_energy(n: int, j: int, family: set[Vertex], steps: int) -> Fraction:
    """Return Pr[T_0 in A and T_steps in A] for the Johnson walk."""
    verts = vertices(n, j)
    fam = set(family)
    weights = {vertex: Fraction(1, len(verts)) for vertex in fam}
    if steps == 0:
        return sum(weights.values(), Fraction(0, 1))
    deg = degree(n, j)
    for _ in range(steps):
        nxt: dict[Vertex, Fraction] = {}
        for vertex, weight in weights.items():
            share = weight / deg
            for nb in neighbors(vertex, n):
                nxt[nb] = nxt.get(nb, Fraction(0, 1)) + share
        weights = nxt
    return sum(weight for vertex, weight in weights.items() if vertex in fam)


def adjacency_matrix(n: int, j: int, verts: list[Vertex]) -> list[list[int]]:
    index = {vertex: i for i, vertex in enumerate(verts)}
    matrix = [[0 for _ in verts] for _ in verts]
    for i, vertex in enumerate(verts):
        for nb in neighbors(vertex, n):
            matrix[i][index[nb]] += 1
    return matrix


def int_matrix_multiply(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    size = len(a)
    out = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for k in range(size):
            if a[i][k] == 0:
                continue
            aik = a[i][k]
            for j in range(size):
                if b[k][j] != 0:
                    out[i][j] += aik * b[k][j]
    return out


def adjacency_powers(n: int, j: int, max_steps: int, verts: list[Vertex]) -> list[list[list[int]]]:
    size = len(verts)
    identity = [[int(i == j) for j in range(size)] for i in range(size)]
    powers = [identity]
    if max_steps == 0:
        return powers
    base = adjacency_matrix(n, j, verts)
    powers.append(base)
    for _ in range(2, max_steps + 1):
        powers.append(int_matrix_multiply(powers[-1], base))
    return powers


def endpoint_energy_from_adjacency_power(mask: int, power: list[list[int]], deg_power: int) -> Fraction:
    indices = [i for i in range(len(power)) if mask & (1 << i)]
    total = 0
    for i in indices:
        row = power[i]
        for j in indices:
            total += row[j]
    return Fraction(total, len(power) * deg_power)


def mixing_bound(n: int, j: int, delta: Fraction) -> Fraction:
    lam = lambda_second(n, j)
    return delta * delta + lam * delta * (1 - delta)


def endpoint_mixing_bound(n: int, j: int, delta: Fraction, steps: int) -> Fraction:
    if steps == 0:
        return delta
    lam = lambda_abs(n, j)
    return delta * delta + (lam ** steps) * delta * (1 - delta)


def point_dictator_endpoint_formula(n: int, j: int, steps: int) -> Fraction:
    delta = Fraction(j, n)
    lam = lambda_second(n, j)
    return delta * delta + (lam ** steps) * delta * (1 - delta)


def survival_bound(n: int, j: int, delta: Fraction) -> Fraction | None:
    if delta == 0:
        return None
    return mixing_bound(n, j, delta) / delta


def fraction_payload(value: Fraction | None) -> dict[str, object] | None:
    if value is None:
        return None
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "float": float(value),
    }


def point_dictator_family(n: int, j: int, point: int = 0) -> set[Vertex]:
    return {vertex for vertex in vertices(n, j) if point in vertex}


def fixed_core_family(n: int, j: int, core_size: int) -> set[Vertex]:
    core = set(range(core_size))
    return {vertex for vertex in vertices(n, j) if core.issubset(vertex)}


def block_profile_family(n: int, j: int, block_size: int, profile: tuple[int, ...]) -> set[Vertex]:
    blocks = []
    cursor = 0
    for _ in profile:
        blocks.append(set(range(cursor, cursor + block_size)))
        cursor += block_size
    if cursor != n:
        raise ValueError("blocks do not cover domain")
    out = set()
    for vertex in vertices(n, j):
        vset = set(vertex)
        if tuple(len(vset & block) for block in blocks) == profile:
            out.add(vertex)
    return out


def check_family(n: int, j: int, name: str, family: set[Vertex]) -> dict[str, object]:
    delta = density(n, j, family)
    energy = one_exchange_energy(n, j, family)
    bound = mixing_bound(n, j, delta)
    if energy > bound:
        raise AssertionError((n, j, name, energy, bound))
    survival = energy / delta if delta else None
    return {
        "name": name,
        "n": n,
        "j": j,
        "vertex_count": comb(n, j),
        "family_size": len(family),
        "density": fraction_payload(delta),
        "one_exchange_energy": fraction_payload(energy),
        "one_exchange_survival_given_inside": fraction_payload(survival),
        "mixing_bound": fraction_payload(bound),
        "survival_bound": fraction_payload(survival_bound(n, j, delta)),
        "slack_bound_minus_energy": fraction_payload(bound - energy),
        "attains_bound": energy == bound,
    }


def check_endpoint_family(
    n: int,
    j: int,
    name: str,
    family: set[Vertex],
    steps_list: tuple[int, ...],
) -> dict[str, object]:
    delta = density(n, j, family)
    rows = []
    for steps in steps_list:
        energy = endpoint_energy(n, j, family, steps)
        bound = endpoint_mixing_bound(n, j, delta, steps)
        if energy > bound:
            raise AssertionError((n, j, name, steps, energy, bound))
        rows.append({
            "steps": steps,
            "endpoint_energy": fraction_payload(energy),
            "endpoint_bound": fraction_payload(bound),
            "slack_bound_minus_energy": fraction_payload(bound - energy),
        })
    return {
        "name": name,
        "n": n,
        "j": j,
        "family_size": len(family),
        "density": fraction_payload(delta),
        "lambda_abs": fraction_payload(lambda_abs(n, j)),
        "rows": rows,
    }


def exhaustive_small_graph() -> dict[str, object]:
    n, j = 6, 2
    verts = vertices(n, j)
    checked = 0
    equality_count = 0
    max_slack = Fraction(0, 1)
    endpoint_steps = (0, 1, 2, 3, 4)
    powers = adjacency_powers(n, j, max(endpoint_steps), verts)
    endpoint_checks = 0
    deg = degree(n, j)
    deg_powers = {steps: deg ** steps for steps in endpoint_steps}
    for mask in range(1 << len(verts)):
        family = {verts[i] for i in range(len(verts)) if mask & (1 << i)}
        delta = density(n, j, family)
        energy = one_exchange_energy(n, j, family)
        bound = mixing_bound(n, j, delta)
        if energy > bound:
            raise AssertionError(("exhaustive", mask, energy, bound))
        checked += 1
        if energy == bound:
            equality_count += 1
        max_slack = max(max_slack, bound - energy)
        for steps in endpoint_steps:
            endpoint = endpoint_energy_from_adjacency_power(mask, powers[steps], deg_powers[steps])
            endpoint_bound = endpoint_mixing_bound(n, j, delta, steps)
            if endpoint > endpoint_bound:
                raise AssertionError(("endpoint_exhaustive", mask, steps, endpoint, endpoint_bound))
            endpoint_checks += 1
    return {
        "name": "exhaustive_J_6_2",
        "n": n,
        "j": j,
        "vertex_count": len(verts),
        "families_checked": checked,
        "equality_families": equality_count,
        "endpoint_steps_checked": list(endpoint_steps),
        "endpoint_inequalities_checked": endpoint_checks,
        "max_slack": fraction_payload(max_slack),
        "status": "PASS",
    }


def structured_cases() -> list[dict[str, object]]:
    return [
        check_family(12, 4, "point_dictator_fixed_root", point_dictator_family(12, 4)),
        check_family(12, 4, "fixed_two_root_core", fixed_core_family(12, 4, 2)),
        check_family(16, 8, "balanced_four_blocks", block_profile_family(16, 8, 4, (2, 2, 2, 2))),
        check_family(16, 8, "frozen_full_blocks", block_profile_family(16, 8, 4, (4, 4, 0, 0))),
    ]


def sampled_cases() -> list[dict[str, object]]:
    rng = random.Random(2026070211)
    cases = []
    for n, j, size, samples in [(8, 3, 12, 24), (10, 4, 30, 24)]:
        verts = vertices(n, j)
        for sample in range(samples):
            family = set(rng.sample(verts, size))
            cases.append(check_family(n, j, f"random_{n}_{j}_{sample}", family))
    return cases


def endpoint_cases() -> list[dict[str, object]]:
    rows = []
    point = point_dictator_family(12, 4)
    point_row = check_endpoint_family(12, 4, "point_dictator_fixed_root", point, (0, 1, 2, 3, 4, 5))
    for row in point_row["rows"]:
        expected = point_dictator_endpoint_formula(12, 4, row["steps"])
        actual = Fraction(row["endpoint_energy"]["numerator"], row["endpoint_energy"]["denominator"])
        if actual != expected:
            raise AssertionError(("point_dictator_formula", row["steps"], actual, expected))
        row["point_dictator_signed_formula"] = fraction_payload(expected)
        row["attains_signed_formula"] = True
    rows.append(point_row)
    rows.append(check_endpoint_family(12, 4, "fixed_two_root_core", fixed_core_family(12, 4, 2), (1, 2, 3, 4, 5)))
    rows.append(check_endpoint_family(16, 8, "balanced_four_blocks", block_profile_family(16, 8, 4, (2, 2, 2, 2)), (1, 2, 3, 4)))
    rows.append(check_endpoint_family(16, 8, "frozen_full_blocks", block_profile_family(16, 8, 4, (4, 4, 0, 0)), (1, 2, 3, 4)))
    return rows


def spectral_gap_rows() -> list[dict[str, object]]:
    rows = []
    for n, j in [(6, 2), (12, 4), (16, 8), (512, 128), (512, 247)]:
        d = degree(n, j)
        gap = theta(n, j, 0) - theta(n, j, 1)
        if gap != n:
            raise AssertionError((n, j, gap))
        rows.append({
            "n": n,
            "j": j,
            "degree": d,
            "theta_0": theta(n, j, 0),
            "theta_1": theta(n, j, 1),
            "theta_0_minus_theta_1": gap,
            "lambda_second": fraction_payload(lambda_second(n, j)),
            "lambda_abs": fraction_payload(lambda_abs(n, j)),
        })
    return rows


def build_artifact() -> dict[str, object]:
    exhaustive = exhaustive_small_graph()
    structured = structured_cases()
    sampled = sampled_cases()
    endpoints = endpoint_cases()
    point_case = structured[0]
    ok = (
        exhaustive["status"] == "PASS"
        and point_case["attains_bound"]
        and all(row["slack_bound_minus_energy"]["numerator"] >= 0 for row in structured + sampled)
        and all(
            endpoint_row["slack_bound_minus_energy"]["numerator"] >= 0
            for case in endpoints
            for endpoint_row in case["rows"]
        )
    )
    return {
        "schema_version": "m1-johnson-exchange-mixing-v1",
        "dag_target": "averaged_xr",
        "status": "PROVED / COMBINATORIAL + FINITE REPLAY" if ok else "FAILED",
        "classification": (
            "JOHNSON_EXCHANGE_MIXING_BOUND_VERIFIED"
            if ok
            else "JOHNSON_EXCHANGE_MIXING_CHECK_FAILED"
        ),
        "theorem": {
            "graph": "Johnson graph J(n,j)",
            "degree": "d=j(n-j)",
            "density": "delta=|A|/binom(n,j)",
            "one_exchange_energy": "E1(A)=Pr[T0,T1 in A]",
            "bound": "E1(A) <= delta^2 + (1-n/d) delta(1-delta)",
            "endpoint_bound": "Pr[T0,Ts in A] <= delta^2 + lambda_*^s delta(1-delta)",
            "equality_model": "point dictator / one fixed root family",
        },
        "spectral_gap_rows": spectral_gap_rows(),
        "exhaustive_small_graph": exhaustive,
        "structured_cases": structured,
        "endpoint_cases": endpoints,
        "sampled_family_count": len(sampled),
        "sampled_cases_sha256_like_summary": {
            "all_checked": True,
            "max_slack_float": max(row["slack_bound_minus_energy"]["float"] for row in sampled),
            "min_slack_float": min(row["slack_bound_minus_energy"]["float"] for row in sampled),
        },
        "nonclaims": [
            "does not prove the XR inverse theorem",
            "does not classify high-energy families beyond the point-dictator equality model",
            "does not bound killed-walk/all-intermediate exchange energy",
            "does not enumerate Reed-Solomon word pairs",
            "does not prove an M1 safe-side threshold",
        ],
    }


def write_artifact() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(build_artifact(), indent=2, sort_keys=True) + "\n")


def replay_artifact() -> tuple[bool, list[str]]:
    if not ARTIFACT.exists():
        return False, ["artifact missing; rerun with --emit"]
    actual = json.loads(ARTIFACT.read_text())
    expected = build_artifact()
    return actual == expected, [
        f"artifact path: {ARTIFACT.relative_to(REPO)}",
        f"classification: {actual.get('classification')}",
        f"exhaustive families checked: {actual['exhaustive_small_graph']['families_checked']}",
        f"endpoint inequalities checked: {actual['exhaustive_small_graph']['endpoint_inequalities_checked']}",
        f"sampled families checked: {actual['sampled_family_count']}",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    args = parser.parse_args()
    if args.emit:
        write_artifact()

    artifact = build_artifact()
    replay_ok, replay_lines = replay_artifact()
    ok = artifact["classification"] == "JOHNSON_EXCHANGE_MIXING_BOUND_VERIFIED" and replay_ok

    print("=" * 78)
    print("M1 Johnson exchange-mixing lemma")
    print("=" * 78)
    print(f"classification: {artifact['classification']}")
    print(f"exhaustive J(6,2) families: {artifact['exhaustive_small_graph']['families_checked']}")
    print(f"endpoint inequalities: {artifact['exhaustive_small_graph']['endpoint_inequalities_checked']}")
    for row in artifact["structured_cases"]:
        print(
            "{name}: density={delta:.6g}, E1={energy:.6g}, bound={bound:.6g}, equality={eq}".format(
                name=row["name"],
                delta=row["density"]["float"],
                energy=row["one_exchange_energy"]["float"],
                bound=row["mixing_bound"]["float"],
                eq=row["attains_bound"],
            )
        )
    print(f"[{'PASS' if replay_ok else 'FAIL'}] artifact replay")
    for line in replay_lines:
        print(f"       {line}")
    print("-" * 78)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
