#!/usr/bin/env python3
"""Verify the C-4 post-impossibility certifier toy pipeline.

C-4 asks for the certifier pipeline after the height/multiplier
impossibility: direct mod-p MITM bands, plus an exact complete solver mode as
the totality anchor.  This toy packet uses N'=16, p=12289, and certifies all
ternary kernel relations of weight <= 6.

The verifier intentionally avoids heavy search.  It runs two independent
complete enumerators:

* split meet-in-the-middle over the first and second half of the exponents;
* branch-and-bound depth-first enumeration with an explicit weight bound.

Both must produce the same relation set, and every relation must be generated
by the antipodal cyclotomic identities zeta^i + zeta^{i+N/2}=0.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "experimental/data/certificates/c4-certifier-pipeline-toy/"
    "c4_certifier_pipeline_toy.json"
)

SCHEMA_VERSION = "c4-certifier-pipeline-toy-v1"
DAG_NODES = [
    "QA.16",
    "QA.18",
    "height_only_impossibility",
    "weight_graded_mitm",
    "certifier_uniformity",
]
TOY_N = 16
TOY_P = 12289
TOY_MAX_WEIGHT = 6

Vector = tuple[int, ...]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    remaining = value
    trial = 2
    while trial * trial <= remaining:
        if remaining % trial == 0:
            factors.append(trial)
            while remaining % trial == 0:
                remaining //= trial
        trial += 1 if trial == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root for F_{p}")


def zeta_of_order(p: int, n: int) -> int:
    require((p - 1) % n == 0, "N must divide p-1")
    zeta = pow(primitive_root(p), (p - 1) // n, p)
    require(pow(zeta, n, p) == 1, "zeta^N != 1")
    for factor in prime_factors(n):
        require(pow(zeta, n // factor, p) != 1, "zeta has smaller order")
    return zeta


def powers(zeta: int, n: int, p: int) -> tuple[int, ...]:
    return tuple(pow(zeta, idx, p) for idx in range(n))


def vector_sum_mod(vector: Vector, zeta_powers: tuple[int, ...], p: int) -> int:
    return sum(coefficient * zeta_powers[idx] for idx, coefficient in enumerate(vector)) % p


def weight(vector: Vector) -> int:
    return sum(1 for entry in vector if entry)


def canonical_vector(vector: Iterable[int]) -> Vector | None:
    out = tuple(vector)
    if not any(out):
        return None
    for entry in out:
        if entry:
            return out if entry > 0 else tuple(-x for x in out)
    raise AssertionError("unreachable")


def is_antipodal_cyclotomic(vector: Vector) -> bool:
    half = len(vector) // 2
    return len(vector) % 2 == 0 and all(vector[idx] == vector[idx + half] for idx in range(half))


def relation_histogram(relations: set[Vector]) -> dict[str, int]:
    counts: Counter[int] = Counter(weight(vector) for vector in relations)
    return {str(key): counts[key] for key in sorted(counts)}


@dataclass(frozen=True)
class Assignment:
    vector: Vector
    residue: int
    weight: int


def half_assignments(indices: range, zeta_powers: tuple[int, ...], p: int, max_weight: int) -> list[Assignment]:
    assignments: list[Assignment] = []
    for coefficients in product((-1, 0, 1), repeat=len(indices)):
        w = sum(1 for coefficient in coefficients if coefficient)
        if w > max_weight:
            continue
        vector = [0] * len(zeta_powers)
        residue = 0
        for local_idx, coefficient in enumerate(coefficients):
            if coefficient == 0:
                continue
            idx = indices.start + local_idx
            vector[idx] = coefficient
            residue = (residue + coefficient * zeta_powers[idx]) % p
        assignments.append(Assignment(tuple(vector), residue, w))
    return assignments


def mitm_relations(n: int, p: int, max_weight: int) -> tuple[set[Vector], dict[str, Any]]:
    zeta = zeta_of_order(p, n)
    zeta_powers = powers(zeta, n, p)
    half = n // 2
    left = half_assignments(range(0, half), zeta_powers, p, max_weight)
    right = half_assignments(range(half, n), zeta_powers, p, max_weight)
    right_by_residue: dict[int, list[Assignment]] = defaultdict(list)
    for assignment in right:
        right_by_residue[assignment.residue].append(assignment)

    relations: set[Vector] = set()
    pair_checks = 0
    for left_assignment in left:
        target = (-left_assignment.residue) % p
        for right_assignment in right_by_residue.get(target, []):
            pair_checks += 1
            total_weight = left_assignment.weight + right_assignment.weight
            if total_weight == 0 or total_weight > max_weight:
                continue
            combined = tuple(a + b for a, b in zip(left_assignment.vector, right_assignment.vector))
            canonical = canonical_vector(combined)
            if canonical is not None:
                relations.add(canonical)

    metadata = {
        "split": [half, n - half],
        "left_assignments": len(left),
        "right_assignments": len(right),
        "matching_residue_pair_checks": pair_checks,
        "relations_found": len(relations),
        "relation_weight_histogram": relation_histogram(relations),
    }
    return relations, metadata


def branch_and_bound_relations(n: int, p: int, max_weight: int) -> tuple[set[Vector], dict[str, Any]]:
    zeta = zeta_of_order(p, n)
    zeta_powers = powers(zeta, n, p)
    relations: set[Vector] = set()
    nodes_visited = 0
    leaves_checked = 0
    vector = [0] * n

    def dfs(idx: int, used_weight: int, residue: int) -> None:
        nonlocal nodes_visited, leaves_checked
        nodes_visited += 1
        if used_weight > max_weight:
            return
        if idx == n:
            leaves_checked += 1
            if used_weight and residue % p == 0:
                canonical = canonical_vector(vector)
                if canonical is not None:
                    relations.add(canonical)
            return
        remaining = n - idx
        if used_weight > max_weight or used_weight + remaining < 1:
            return
        vector[idx] = 0
        dfs(idx + 1, used_weight, residue)
        if used_weight < max_weight:
            vector[idx] = 1
            dfs(idx + 1, used_weight + 1, (residue + zeta_powers[idx]) % p)
            vector[idx] = -1
            dfs(idx + 1, used_weight + 1, (residue - zeta_powers[idx]) % p)
        vector[idx] = 0

    dfs(0, 0, 0)
    metadata = {
        "nodes_visited": nodes_visited,
        "leaves_checked": leaves_checked,
        "relations_found": len(relations),
        "relation_weight_histogram": relation_histogram(relations),
        "complete": True,
    }
    return relations, metadata


def expected_antipodal_count(n: int, max_weight: int) -> int:
    half = n // 2
    total = 0
    for pair_count in range(1, max_weight // 2 + 1):
        total += math.comb(half, pair_count) * (2 ** (pair_count - 1))
    return total


def relation_records(relations: set[Vector]) -> list[dict[str, Any]]:
    records = []
    for vector in sorted(relations, key=lambda row: (weight(row), row)):
        records.append(
            {
                "support": [idx for idx, entry in enumerate(vector) if entry],
                "signs": [entry for entry in vector if entry],
                "weight": weight(vector),
            }
        )
    return records


def cost_table() -> list[dict[str, Any]]:
    rows = []
    n = 128
    for target_weight in (12, 14, 16):
        half_weight = target_weight // 2
        states = math.comb(n, half_weight) * (2 ** half_weight)
        rows.append(
            {
                "N_prime": n,
                "target_weight_w": target_weight,
                "half_weight": half_weight,
                "cost_model": "binom(N', w/2) * 2^(w/2)",
                "state_count": states,
                "log2_state_count": round(math.log2(states), 6),
            }
        )
    return rows


def build_certificate() -> dict[str, Any]:
    zeta = zeta_of_order(TOY_P, TOY_N)
    zeta_powers = powers(zeta, TOY_N, TOY_P)
    mitm, mitm_meta = mitm_relations(TOY_N, TOY_P, TOY_MAX_WEIGHT)
    bnb, bnb_meta = branch_and_bound_relations(TOY_N, TOY_P, TOY_MAX_WEIGHT)
    require(mitm == bnb, "MITM and branch-and-bound relation sets differ")
    require(len(mitm) == expected_antipodal_count(TOY_N, TOY_MAX_WEIGHT), "unexpected relation count")
    require(all(is_antipodal_cyclotomic(vector) for vector in mitm), "non-cyclotomic relation found")
    require(all(vector_sum_mod(vector, zeta_powers, TOY_P) == 0 for vector in mitm), "bad relation in set")

    records = relation_records(mitm)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": "TOY_TOTALITY_ANCHOR / DIRECT_MOD_P_MITM",
        "task_id": "C-4",
        "dag_nodes": DAG_NODES,
        "post_impossibility_policy": {
            "height_only": "scoping only; full N'=128 cells exceed p<2^256 by height alone",
            "multiplier": "not used; direct mod-p MITM enumerates sparse sums of zeta powers",
            "totality_anchor": "complete branch-and-bound mode independently enumerates the finite toy row",
        },
        "mitm_cost_table_for_N128": cost_table(),
        "toy_row": {
            "N_prime": TOY_N,
            "p": TOY_P,
            "primitive_root": primitive_root(TOY_P),
            "zeta_order_N": zeta,
            "max_weight": TOY_MAX_WEIGHT,
            "zeta_powers": list(zeta_powers),
        },
        "mitm_certificate": mitm_meta,
        "branch_and_bound_certificate": bnb_meta,
        "comparison": {
            "relation_sets_equal": True,
            "all_relations_antipodal_cyclotomic": True,
            "non_cyclotomic_relation_count": 0,
            "expected_antipodal_relation_count": expected_antipodal_count(TOY_N, TOY_MAX_WEIGHT),
            "relation_set_sha256": sha256_json(records),
        },
        "printed_certificate": {
            "format": "support/sign rows, canonicalized up to global sign",
            "relation_count": len(records),
            "sample_relations": records[:24],
        },
        "nonclaims": [
            "does not run N'=128 or any heavy search",
            "does not prove certifier uniformity for every admissible prime",
            "does not use or rescue the multiplier route",
            "does not exclude non-cyclotomic relations at N'=32; this is only the printed N'=16 toy anchor",
        ],
    }
    payload["payload_sha256"] = sha256_json(payload)
    return payload


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    if actual != expected:
        raise AssertionError(f"certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    toy = certificate["toy_row"]
    comparison = certificate["comparison"]
    print("C-4 certifier pipeline toy")
    print(f"status: {certificate['status']}")
    print(
        "N'={N_prime}, p={p}, w<={max_weight}, relations={expected_antipodal_relation_count}, noncyclotomic={non_cyclotomic_relation_count}".format(
            **toy, **comparison
        )
    )
    print("N'=128 cost table:", certificate["mitm_cost_table_for_N128"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="write deterministic C-4 toy JSON, optionally to PATH",
    )
    parser.add_argument(
        "--check",
        nargs="?",
        const=OUTPUT,
        type=Path,
        help="check deterministic C-4 toy JSON, optionally at PATH",
    )
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check, certificate)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
