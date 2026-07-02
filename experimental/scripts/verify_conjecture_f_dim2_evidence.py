#!/usr/bin/env python3
"""Evidence packet for Conjecture F in projective dimension two.

This is an EXPERIMENTAL verifier, not a proof.  It follows the E7 evidence
plan from the roadmap/DAG lane:

* exactly enumerate all projective planes in P(K[X]_{<=3}) for
  K = F_17 and H = F_17^*;
* classify common-root planes as the paid tangent/common-divisor shape;
* record the maximum primitive intersection with D_3(H);
* sample genuine Hankel-kernel projective planes at n=16, j=5, t=3;
* test the pre-registered QF.4 prediction that the sampled top j=5
  kernel planes beating the simple-line pair bound contain twin
  evaluation-line classes.
* check both runs against the fixed-dimensional Conjecture F consumer bound
  proved in the companion reduction-lemma package.

The exact census is small because projective planes in P^3 are hyperplanes:
(17^4 - 1)/(17 - 1) = 5220.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from math import comb
from pathlib import Path
from typing import Any


P = 17
N = 16
J_EXACT = 3
J_KERNEL = 5
T_KERNEL = 3
KERNEL_SAMPLE_COUNT = 2048
SEED = 2026070207
OUTPUT = Path(
    "experimental/data/certificates/conjecture-f-dim2-evidence/"
    "conjecture_f_dim2_n16_f17.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inv(x: int) -> int:
    return pow(x % P, -1, P)


def canonical_vector(values: tuple[int, ...]) -> tuple[int, ...] | None:
    for value in values:
        if value % P:
            factor = inv(value)
            return tuple((factor * x) % P for x in values)
    return None


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a * b for a, b in zip(left, right)) % P


def poly_mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % P
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def locator(roots: tuple[int, ...]) -> tuple[int, ...]:
    poly = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % P, 1))
    return poly


def divisor_locators(domain: list[int], degree: int) -> list[tuple[int, ...]]:
    return [locator(tuple(combo)) for combo in itertools.combinations(domain, degree)]


def eval_vector(x: int, degree: int) -> tuple[int, ...]:
    return tuple(pow(x, i, P) for i in range(degree + 1))


def rank_mod_p(rows: list[tuple[int, ...]] | list[list[int]], width: int | None = None) -> int:
    if not rows:
        return 0
    if width is None:
        width = len(rows[0])
    work = [[entry % P for entry in row[:width]] for row in rows]
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col] % P:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        factor = inv(work[rank][col])
        work[rank] = [(factor * x) % P for x in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % P:
                multiple = work[row][col]
                work[row] = [
                    (work[row][i] - multiple * work[rank][i]) % P
                    for i in range(width)
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def in_rowspace(vector: tuple[int, ...], rows: list[tuple[int, ...]], width: int) -> bool:
    return rank_mod_p(rows + [vector], width) == rank_mod_p(rows, width)


def nullspace_basis(rows: list[tuple[int, ...]], width: int) -> list[tuple[int, ...]]:
    work = [[entry % P for entry in row] for row in rows]
    rank = 0
    pivots: list[int] = []
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col] % P:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        factor = inv(work[rank][col])
        work[rank] = [(factor * x) % P for x in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % P:
                multiple = work[row][col]
                work[row] = [
                    (work[row][i] - multiple * work[rank][i]) % P
                    for i in range(width)
                ]
        pivots.append(col)
        rank += 1
        if rank == len(work):
            break

    pivot_set = set(pivots)
    basis: list[tuple[int, ...]] = []
    for free in range(width):
        if free in pivot_set:
            continue
        vector = [0] * width
        vector[free] = 1
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-work[row][free]) % P
        basis.append(tuple(vector))
    return basis


def line_profile_for_plane(rowspace: list[tuple[int, ...]], degree: int, domain: list[int]) -> dict[str, Any]:
    basis = nullspace_basis(rowspace, degree + 1)
    lines = []
    for x in domain:
        restricted = tuple(dot(eval_vector(x, degree), vector) for vector in basis)
        line = canonical_vector(restricted)
        if line is None:
            raise AssertionError("rowspace has a common root; line profile is not primitive")
        lines.append(line)
    counts = Counter(lines)
    twin_sizes = sorted((count for count in counts.values() if count >= 2), reverse=True)
    return {
        "distinct_evaluation_lines": len(counts),
        "max_line_multiplicity": max(counts.values()),
        "twin_class_count": len(twin_sizes),
        "twin_point_count": sum(twin_sizes),
        "twin_class_sizes": twin_sizes,
        "multiplicity_histogram": {
            str(key): value for key, value in sorted(Counter(counts.values()).items())
        },
    }


def projective_functionals(width: int) -> list[tuple[int, ...]]:
    seen: set[tuple[int, ...]] = set()
    out: list[tuple[int, ...]] = []
    for values in itertools.product(range(P), repeat=width):
        if not any(values):
            continue
        canonical = canonical_vector(values)
        assert canonical is not None
        if canonical not in seen:
            seen.add(canonical)
            out.append(canonical)
    return out


def proper_quotient_orders(n: int, j: int) -> list[int]:
    return [m for m in range(2, n + 1) if n % m == 0 and j % m == 0]


def exact_j3_plane_census(domain: list[int]) -> dict[str, Any]:
    degree = J_EXACT
    divisors = divisor_locators(domain, degree)
    functionals = projective_functionals(degree + 1)
    expected_planes = (P ** (degree + 1) - 1) // (P - 1)
    hit_distribution: Counter[int] = Counter()
    primitive_distribution: Counter[int] = Counter()
    common_distribution: Counter[int] = Counter()
    top_primitive: list[dict[str, Any]] = []
    common_root_planes = 0
    primitive_planes = 0
    primitive_max = -1
    common_hit_values: set[int] = set()

    for functional in functionals:
        hits = sum(1 for loc in divisors if dot(functional, loc) == 0)
        common_roots = [
            x for x in domain
            if canonical_vector(eval_vector(x, degree)) == functional
        ]
        hit_distribution[hits] += 1
        if common_roots:
            common_root_planes += 1
            common_distribution[hits] += 1
            common_hit_values.add(hits)
            continue

        primitive_planes += 1
        primitive_distribution[hits] += 1
        if hits > primitive_max:
            primitive_max = hits
            top_primitive = []
        if hits == primitive_max and len(top_primitive) < 12:
            profile = line_profile_for_plane([functional], degree, domain)
            top_primitive.append({
                "hit_count": hits,
                "functional": list(functional),
                **profile,
            })

    weighted_pair_bound = comb(N, 2) // (degree - 1)
    simple_line_bound = comb(N, 2) // comb(degree, 2)
    status = (
        len(functionals) == expected_planes
        and common_root_planes == N
        and common_hit_values == {comb(N - 1, degree - 1)}
        and primitive_max <= weighted_pair_bound
    )

    return {
        "name": "exact_projective_plane_census_j3",
        "status": "PASS" if status else "FAIL",
        "field": f"F_{P}",
        "domain": "F_17^*",
        "n": N,
        "j": degree,
        "projective_planes_enumerated": len(functionals),
        "expected_projective_planes": expected_planes,
        "divisor_points": len(divisors),
        "proper_quotient_orders": proper_quotient_orders(N, degree),
        "common_root_planes": common_root_planes,
        "common_root_hit_count": comb(N - 1, degree - 1),
        "primitive_planes": primitive_planes,
        "primitive_max_hits": primitive_max,
        "primitive_top_plane_count": primitive_distribution[primitive_max],
        "weighted_pair_bound_floor": weighted_pair_bound,
        "weighted_pair_bound_rational": f"{comb(N, 2)}/{degree - 1}",
        "simple_line_bound_floor": simple_line_bound,
        "simple_line_bound_rational": f"{comb(N, 2)}/{comb(degree, 2)}",
        "all_plane_hit_distribution": {
            str(key): value for key, value in sorted(hit_distribution.items())
        },
        "primitive_hit_distribution": {
            str(key): value for key, value in sorted(primitive_distribution.items())
        },
        "common_root_hit_distribution": {
            str(key): value for key, value in sorted(common_distribution.items())
        },
        "top_primitive_examples": top_primitive,
    }


def random_hankel_rows(rng: random.Random, degree: int, rows: int) -> list[tuple[int, ...]]:
    syndrome = [rng.randrange(P) for _ in range(degree + rows)]
    return [
        tuple(syndrome[row + col] for col in range(degree + 1))
        for row in range(rows)
    ]


def kernel_plane_sample_j5(domain: list[int]) -> dict[str, Any]:
    degree = J_KERNEL
    rows = T_KERNEL
    divisors = divisor_locators(domain, degree)
    simple_line_bound = comb(N, 2) // comb(degree, 2)
    rng = random.Random(SEED)
    accepted = 0
    attempts = 0
    common_root_planes = 0
    hit_distribution: Counter[int] = Counter()
    primitive_distribution: Counter[int] = Counter()
    primitive_max = -1
    top_planes_with_twins = 0
    top_planes_without_twins = 0
    top_planes_above_simple_bound = 0
    top_planes_above_simple_bound_without_twins = 0
    top_primitive: list[dict[str, Any]] = []

    while accepted < KERNEL_SAMPLE_COUNT:
        attempts += 1
        rowspace = random_hankel_rows(rng, degree, rows)
        if rank_mod_p(rowspace, degree + 1) != rows:
            continue
        accepted += 1
        hits = sum(
            1 for loc in divisors
            if all(dot(row, loc) == 0 for row in rowspace)
        )
        common_roots = [
            x for x in domain
            if in_rowspace(eval_vector(x, degree), rowspace, degree + 1)
        ]
        hit_distribution[hits] += 1
        if common_roots:
            common_root_planes += 1
            continue

        primitive_distribution[hits] += 1
        if hits > primitive_max:
            primitive_max = hits
            top_planes_with_twins = 0
            top_planes_without_twins = 0
            top_planes_above_simple_bound = 0
            top_planes_above_simple_bound_without_twins = 0
            top_primitive = []
        if hits == primitive_max and len(top_primitive) < 8:
            profile = line_profile_for_plane(rowspace, degree, domain)
            top_primitive.append({
                "hit_count": hits,
                "hankel_rows": [list(row) for row in rowspace],
                **profile,
            })
        if hits == primitive_max:
            profile = line_profile_for_plane(rowspace, degree, domain)
            has_twins = profile["twin_class_count"] > 0
            top_planes_with_twins += int(has_twins)
            top_planes_without_twins += int(not has_twins)
            if hits > simple_line_bound:
                top_planes_above_simple_bound += 1
                top_planes_above_simple_bound_without_twins += int(not has_twins)

    weighted_pair_bound = comb(N, 2) // (degree - 1)
    status = (
        accepted == KERNEL_SAMPLE_COUNT
        and proper_quotient_orders(N, degree) == []
        and primitive_max <= weighted_pair_bound
        and top_planes_above_simple_bound_without_twins == 0
    )
    return {
        "name": "sampled_hankel_kernel_planes_j5_t3",
        "status": "PASS" if status else "FAIL",
        "field": f"F_{P}",
        "domain": "F_17^*",
        "n": N,
        "j": degree,
        "t": rows,
        "seed": SEED,
        "accepted_full_rank_kernel_planes": accepted,
        "attempts": attempts,
        "divisor_points": len(divisors),
        "proper_quotient_orders": proper_quotient_orders(N, degree),
        "common_root_planes_seen": common_root_planes,
        "primitive_max_hits": primitive_max,
        "primitive_top_plane_count_in_sample": primitive_distribution[primitive_max],
        "weighted_pair_bound_floor": weighted_pair_bound,
        "weighted_pair_bound_rational": f"{comb(N, 2)}/{degree - 1}",
        "simple_line_bound_floor": simple_line_bound,
        "simple_line_bound_rational": f"{comb(N, 2)}/{comb(degree, 2)}",
        "qf4_prediction": (
            "Every sampled primitive top j=5 kernel plane whose hit count "
            "exceeds the simple-line bound has at least one twin "
            "evaluation-line class."
        ),
        "primitive_top_planes_with_twins": top_planes_with_twins,
        "primitive_top_planes_without_twins": top_planes_without_twins,
        "primitive_top_planes_above_simple_bound": top_planes_above_simple_bound,
        "primitive_top_planes_above_simple_bound_without_twins": (
            top_planes_above_simple_bound_without_twins
        ),
        "all_sample_hit_distribution": {
            str(key): value for key, value in sorted(hit_distribution.items())
        },
        "primitive_sample_hit_distribution": {
            str(key): value for key, value in sorted(primitive_distribution.items())
        },
        "top_primitive_examples": top_primitive,
    }


def fixed_dimension_consistency_check(domain: list[int]) -> dict[str, Any]:
    exact_degree = J_EXACT
    exact_divisors = divisor_locators(domain, exact_degree)
    exact_violations = 0
    exact_max_slack = 0
    exact_sharp_common_root_planes = 0
    for functional in projective_functionals(exact_degree + 1):
        hits = sum(1 for loc in exact_divisors if dot(functional, loc) == 0)
        common_roots = [
            x for x in domain
            if canonical_vector(eval_vector(x, exact_degree)) == functional
        ]
        bound = comb(N - len(common_roots), 2)
        if hits > bound:
            exact_violations += 1
        exact_max_slack = max(exact_max_slack, bound - hits)
        if common_roots and hits == bound:
            exact_sharp_common_root_planes += 1

    kernel_degree = J_KERNEL
    kernel_divisors = divisor_locators(domain, kernel_degree)
    rng = random.Random(SEED)
    accepted = 0
    attempts = 0
    kernel_violations = 0
    kernel_max_hits = 0
    kernel_min_slack = None
    while accepted < KERNEL_SAMPLE_COUNT:
        attempts += 1
        rowspace = random_hankel_rows(rng, kernel_degree, T_KERNEL)
        if rank_mod_p(rowspace, kernel_degree + 1) != T_KERNEL:
            continue
        accepted += 1
        hits = sum(
            1 for loc in kernel_divisors
            if all(dot(row, loc) == 0 for row in rowspace)
        )
        common_roots = [
            x for x in domain
            if in_rowspace(eval_vector(x, kernel_degree), rowspace, kernel_degree + 1)
        ]
        bound = comb(N - len(common_roots), 2)
        slack = bound - hits
        if hits > bound:
            kernel_violations += 1
        kernel_max_hits = max(kernel_max_hits, hits)
        kernel_min_slack = slack if kernel_min_slack is None else min(kernel_min_slack, slack)

    ok = exact_violations == 0 and kernel_violations == 0 and accepted == KERNEL_SAMPLE_COUNT
    return {
        "name": "fixed_dimension_theorem_consistency",
        "status": "PASS" if ok else "FAIL",
        "consumer": "Conjecture F fixed-dimensional/common-root bound",
        "projective_dimension": 2,
        "j3_exact_planes_checked": len(projective_functionals(exact_degree + 1)),
        "j3_violations": exact_violations,
        "j3_sharp_common_root_planes": exact_sharp_common_root_planes,
        "j3_max_bound_slack": exact_max_slack,
        "j5_sampled_kernel_planes_checked": accepted,
        "j5_attempts": attempts,
        "j5_violations": kernel_violations,
        "j5_max_hits": kernel_max_hits,
        "j5_min_bound_slack": kernel_min_slack,
    }


def build_report() -> dict[str, Any]:
    domain = list(range(1, P))
    checks = [
        exact_j3_plane_census(domain),
        kernel_plane_sample_j5(domain),
        fixed_dimension_consistency_check(domain),
    ]
    return {
        "schema": "conjecture_f_dim2_evidence_v1",
        "status": "EXPERIMENTAL_EVIDENCE",
        "roadmap_task": "E7 / Conjecture F dimension-2 evidence",
        "object": "D_j(H) intersections with projective planes in locator coefficient space",
        "field": {"p": P},
        "domain": {"type": "multiplicative_group", "n": N, "elements": domain},
        "notes": [
            "The j=3 projective-plane census is exhaustive.",
            "The j=5 Hankel-kernel-plane run is deterministic sampling only.",
            "Both tested j values have gcd(n,j)=1, so no proper quotient-pullback stratum is present.",
        ],
        "checks": checks,
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
    args = parser.parse_args()

    report = build_report()
    print("=" * 78)
    print("Conjecture F dimension-2 evidence verifier")
    print("=" * 78)
    ok = True
    for check in report["checks"]:
        ok &= check["status"] == "PASS"
        print(f"[{check['status']}] {check['name']}")
        for key, value in check.items():
            if key not in {"name", "status", "top_primitive_examples"}:
                print(f"        {key}: {value}")
        print(f"        top_primitive_examples: {len(check.get('top_primitive_examples', []))} recorded")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
