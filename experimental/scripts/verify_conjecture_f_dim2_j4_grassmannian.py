#!/usr/bin/env python3
"""E10 j=4 Grassmannian census for Conjecture F dimension-two evidence.

This is an exhaustive evidence replay, not a theorem.  It enumerates every
projective plane in P(F_17[X]_{<=4}) by the dual projective-line Grassmannian,
counts its intersection with D_4(F_17^*), removes common-root paid planes, and
records how the primitive maximum sits relative to the pair-bound envelope.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from math import comb
from pathlib import Path
from typing import Any, Iterable


P = 17
N = 16
J = 4
WIDTH = J + 1
OUTPUT = Path(
    "experimental/data/certificates/conjecture-f-dim2-evidence/"
    "conjecture_f_dim2_j4_grassmannian.json"
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


def eval_vector(x: int, degree: int) -> tuple[int, ...]:
    return tuple(pow(x, i, P) for i in range(degree + 1))


def divisor_locators(domain: list[int], degree: int) -> list[tuple[int, ...]]:
    return [locator(tuple(combo)) for combo in itertools.combinations(domain, degree)]


def projective_points(width: int) -> list[tuple[int, ...]]:
    points: list[tuple[int, ...]] = []
    for pivot in range(width):
        prefix = (0,) * pivot + (1,)
        for suffix in itertools.product(range(P), repeat=width - pivot - 1):
            points.append(prefix + suffix)
    return points


def rank_mod_p(rows: list[tuple[int, ...]] | list[list[int]], width: int) -> int:
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


def rref_key(rows: list[tuple[int, ...]], width: int) -> tuple[tuple[int, ...], ...] | None:
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
    if rank < 2:
        return None
    return tuple(tuple(row) for row in work[:rank])


def nullspace_basis(rows: list[tuple[int, ...]], width: int) -> list[tuple[int, ...]]:
    work = [[entry % P for entry in row[:width]] for row in rows]
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


def iter_rref_lines(width: int) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    """Yield every two-dimensional subspace of F_p^width in RREF form."""
    for first_pivot in range(width - 1):
        for second_pivot in range(first_pivot + 1, width):
            free_positions: list[tuple[int, int]] = []
            for col in range(first_pivot + 1, second_pivot):
                free_positions.append((0, col))
            for col in range(second_pivot + 1, width):
                free_positions.append((0, col))
                free_positions.append((1, col))
            for values in itertools.product(range(P), repeat=len(free_positions)):
                row1 = [0] * width
                row2 = [0] * width
                row1[first_pivot] = 1
                row2[second_pivot] = 1
                for (row, col), value in zip(free_positions, values):
                    if row == 0:
                        row1[col] = value
                    else:
                        row2[col] = value
                yield tuple(row1), tuple(row2)


def gaussian_binomial_5_3() -> int:
    return ((P ** 5 - 1) * (P ** 4 - 1)) // ((P ** 2 - 1) * (P - 1))


def point_masks(points: list[tuple[int, ...]], divisors: list[tuple[int, ...]]) -> dict[tuple[int, ...], int]:
    masks: dict[tuple[int, ...], int] = {}
    for point in points:
        mask = 0
        for index, loc in enumerate(divisors):
            if dot(point, loc) == 0:
                mask |= 1 << index
        masks[point] = mask
    return masks


def common_root_line_keys(points: list[tuple[int, ...]], domain: list[int]) -> set[tuple[tuple[int, ...], ...]]:
    eval_points = {canonical_vector(eval_vector(x, J)) for x in domain}
    assert None not in eval_points
    common: set[tuple[tuple[int, ...], ...]] = set()
    for ev in eval_points:
        assert ev is not None
        for point in points:
            key = rref_key([ev, point], WIDTH)
            if key is not None:
                common.add(key)
    return common


def line_profile(rowspace: list[tuple[int, ...]], domain: list[int]) -> dict[str, Any]:
    basis = nullspace_basis(rowspace, WIDTH)
    lines = []
    for x in domain:
        restricted = tuple(dot(eval_vector(x, J), vector) for vector in basis)
        line = canonical_vector(restricted)
        if line is None:
            raise AssertionError("primitive top plane unexpectedly has a common root")
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


def build_certificate() -> dict[str, Any]:
    domain = list(range(1, P))
    divisors = divisor_locators(domain, J)
    points = projective_points(WIDTH)
    masks = point_masks(points, divisors)
    common_keys = common_root_line_keys(points, domain)

    expected_lines = gaussian_binomial_5_3()
    all_distribution: Counter[int] = Counter()
    primitive_distribution: Counter[int] = Counter()
    common_distribution: Counter[int] = Counter()
    primitive_planes = 0
    common_planes = 0
    primitive_max = -1
    top_examples: list[dict[str, Any]] = []
    top_with_twins = 0
    top_without_twins = 0
    primitive_above_simple = 0
    total_lines = 0

    for row1, row2 in iter_rref_lines(WIDTH):
        total_lines += 1
        hits = (masks[row1] & masks[row2]).bit_count()
        all_distribution[hits] += 1
        key = (row1, row2)
        if key in common_keys:
            common_planes += 1
            common_distribution[hits] += 1
            continue

        primitive_planes += 1
        primitive_distribution[hits] += 1
        if hits > comb(N, 2) // comb(J, 2):
            primitive_above_simple += 1
        if hits > primitive_max:
            primitive_max = hits
            top_examples = []
            top_with_twins = 0
            top_without_twins = 0
        if hits == primitive_max:
            profile = line_profile([row1, row2], domain)
            has_twins = profile["twin_class_count"] > 0
            top_with_twins += int(has_twins)
            top_without_twins += int(not has_twins)
            if len(top_examples) < 12:
                top_examples.append({
                    "hit_count": hits,
                    "dual_rref_rows": [list(row1), list(row2)],
                    **profile,
                })

    simple_bound_floor = comb(N, 2) // comb(J, 2)
    weighted_bound_floor = comb(N, 2) // (J - 1)
    ok = (
        total_lines == expected_lines
        and len(points) == (P ** WIDTH - 1) // (P - 1)
        and primitive_planes + common_planes == total_lines
        and primitive_max <= weighted_bound_floor
        and top_without_twins == 0
    )
    return {
        "schema": "conjecture_f_dim2_j4_grassmannian_v1",
        "status": "PASS" if ok else "FAIL",
        "roadmap_task": "E10 / dim-2 skeleton predictions / j=4 Grassmannian census",
        "field": {"p": P},
        "domain": {"type": "F_p_star", "n": N, "elements": domain},
        "parameters": {
            "j": J,
            "ambient_projective_space": "P^4",
            "projective_plane_vector_dimension": 3,
            "dual_line_vector_dimension": 2,
        },
        "counts": {
            "projective_dual_points": len(points),
            "expected_projective_dual_points": (P ** WIDTH - 1) // (P - 1),
            "projective_planes_enumerated": total_lines,
            "expected_projective_planes": expected_lines,
            "common_root_paid_planes": common_planes,
            "primitive_planes": primitive_planes,
            "divisor_points": len(divisors),
            "proper_quotient_orders": [m for m in range(2, N + 1) if N % m == 0 and J % m == 0],
        },
        "pair_bound_envelope": {
            "simple_line_bound_floor": simple_bound_floor,
            "simple_line_bound_rational": f"{comb(N, 2)}/{comb(J, 2)}",
            "weighted_pair_bound_floor": weighted_bound_floor,
            "weighted_pair_bound_rational": f"{comb(N, 2)}/{J - 1}",
            "primitive_max_hits": primitive_max,
            "primitive_top_plane_count": primitive_distribution[primitive_max],
            "primitive_planes_above_simple_bound": primitive_above_simple,
            "top_planes_with_twins": top_with_twins,
            "top_planes_without_twins": top_without_twins,
        },
        "distributions": {
            "all_plane_hit_distribution": {
                str(key): value for key, value in sorted(all_distribution.items())
            },
            "primitive_hit_distribution": {
                str(key): value for key, value in sorted(primitive_distribution.items())
            },
            "common_root_hit_distribution": {
                str(key): value for key, value in sorted(common_distribution.items())
            },
        },
        "top_primitive_examples": top_examples,
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }


def print_summary(cert: dict[str, Any]) -> None:
    print("Conjecture F E10 j=4 Grassmannian census")
    print(f"  status: {cert['status']}")
    print(f"  projective planes: {cert['counts']['projective_planes_enumerated']}")
    print(f"  primitive planes: {cert['counts']['primitive_planes']}")
    print(f"  common-root paid planes: {cert['counts']['common_root_paid_planes']}")
    print(f"  primitive max hits: {cert['pair_bound_envelope']['primitive_max_hits']}")
    print(f"  simple bound floor: {cert['pair_bound_envelope']['simple_line_bound_floor']}")
    print(f"  weighted bound floor: {cert['pair_bound_envelope']['weighted_pair_bound_floor']}")
    print(f"  top planes with twins: {cert['pair_bound_envelope']['top_planes_with_twins']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="compare a stored certificate with a fresh run")
    args = parser.parse_args()

    cert = build_certificate()
    print_summary(cert)
    if args.check:
        stored = json.loads(args.check.read_text())
        if stored != cert:
            raise SystemExit(f"certificate mismatch: {args.check}")
        print(f"checked {args.check}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if cert["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
