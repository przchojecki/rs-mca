#!/usr/bin/env python3
"""Exhaustive toy replay for the Conjecture F dimension-two skeleton.

The companion note proves the incidence reduction.  This script checks every
projective plane W in F_17[X]_{<=3}, with H = F_17^*, against the theorem:
common-root planes are paid, twin-line branches reduce by common divisors to
projective lines, and the twin-free residual obeys the sharp pair count.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path


P = 17
J = 3
WIDTH = J + 1
OUTPUT = Path(
    "experimental/data/certificates/conjecture-f-dim2-skeleton/"
    "conjecture_f_dim2_skeleton.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def trim(poly: tuple[int, ...]) -> tuple[int, ...]:
    out = [x % P for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


def coeffs(poly: tuple[int, ...], width: int) -> tuple[int, ...]:
    return tuple(poly[i] % P if i < len(poly) else 0 for i in range(width))


def poly_add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    width = max(len(a), len(b))
    return trim(tuple(
        ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % P
        for i in range(width)
    ))


def poly_scale(c: int, poly: tuple[int, ...]) -> tuple[int, ...]:
    return trim(tuple((c * x) % P for x in poly))


def poly_mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % P
    return trim(tuple(out))


def poly_eval(poly: tuple[int, ...], x: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % P
    return acc


def poly_div_exact(poly: tuple[int, ...], divisor: tuple[int, ...]) -> tuple[int, ...]:
    rem = list(trim(poly))
    div = trim(divisor)
    if div[-1] != 1:
        raise ValueError("divisor must be monic")
    quotient = [0] * (max(0, len(rem) - len(div)) + 1)
    while len(rem) >= len(div):
        factor = rem[-1] % P
        shift = len(rem) - len(div)
        quotient[shift] = factor
        for i, coeff in enumerate(div):
            rem[shift + i] = (rem[shift + i] - factor * coeff) % P
        while rem and rem[-1] % P == 0:
            rem.pop()
    if rem:
        raise ValueError(f"non-exact division: {poly} / {divisor}")
    return trim(tuple(quotient))


def locator(roots: tuple[int, ...]) -> tuple[int, ...]:
    poly = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % P, 1))
    return poly


def canonical_vector(values: tuple[int, ...]) -> tuple[int, ...] | None:
    for value in values:
        if value % P:
            inv = pow(value, -1, P)
            return tuple((inv * x) % P for x in values)
    return None


def dot(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(a, b)) % P


def rank_vectors(vectors: list[tuple[int, ...]], width: int) -> int:
    work = [list(v[:width]) + [0] * max(0, width - len(v)) for v in vectors]
    work = [[x % P for x in row[:width]] for row in work if any(x % P for x in row)]
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
        inv = pow(work[rank][col], -1, P)
        work[rank] = [(inv * x) % P for x in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % P:
                factor = work[row][col]
                work[row] = [
                    (work[row][i] - factor * work[rank][i]) % P
                    for i in range(width)
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def nullspace(rows: list[tuple[int, ...]], width: int) -> list[tuple[int, ...]]:
    if not rows:
        return [tuple(1 if i == j else 0 for i in range(width)) for j in range(width)]
    work = [[x % P for x in row[:width]] for row in rows]
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
        inv = pow(work[rank][col], -1, P)
        work[rank] = [(inv * x) % P for x in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col] % P:
                factor = work[row][col]
                work[row] = [
                    (work[row][i] - factor * work[rank][i]) % P
                    for i in range(width)
                ]
        pivots.append(col)
        rank += 1
        if rank == len(work):
            break

    pivot_set = set(pivots)
    basis = []
    for free in range(width):
        if free in pivot_set:
            continue
        vec = [0] * width
        vec[free] = 1
        for row, pivot_col in enumerate(pivots):
            vec[pivot_col] = (-work[row][free]) % P
        basis.append(tuple(vec))
    return basis


def projective_normals(width: int) -> list[tuple[int, ...]]:
    normals = []
    for values in itertools.product(range(P), repeat=width):
        if not any(values):
            continue
        if canonical_vector(values) == values:
            normals.append(values)
    return normals


def poly_linear_combination(coefficients: tuple[int, ...], basis: list[tuple[int, ...]]) -> tuple[int, ...]:
    out = (0,)
    for coeff, poly in zip(coefficients, basis):
        out = poly_add(out, poly_scale(coeff, poly))
    return out


def subspace_vanishing_basis(basis: list[tuple[int, ...]], roots: tuple[int, ...]) -> list[tuple[int, ...]]:
    rows = [tuple(poly_eval(poly, root) for poly in basis) for root in roots]
    coefficient_basis = nullspace(rows, len(basis))
    return [poly_linear_combination(coeffs_, basis) for coeffs_ in coefficient_basis]


def in_span(poly: tuple[int, ...], basis: list[tuple[int, ...]], width: int) -> bool:
    base = [coeffs(b, width) for b in basis]
    return rank_vectors(base, width) == rank_vectors(base + [coeffs(poly, width)], width)


def line_groups(basis: list[tuple[int, ...]], H: list[int]) -> tuple[dict[tuple[int, ...], tuple[int, ...]], list[int]]:
    groups: dict[tuple[int, ...], list[int]] = {}
    common_roots = []
    for root in H:
        values = tuple(poly_eval(poly, root) for poly in basis)
        line = canonical_vector(values)
        if line is None:
            common_roots.append(root)
        else:
            groups.setdefault(line, []).append(root)
    return {line: tuple(roots) for line, roots in groups.items()}, common_roots


def fail(reason: str, **details: object) -> None:
    payload = {"status": "FAIL", "reason": reason}
    payload.update(details)
    raise AssertionError(json.dumps(payload, sort_keys=True))


def build_report() -> dict:
    H = list(range(1, P))
    divisors = [
        (combo, locator(combo))
        for combo in itertools.combinations(H, J)
    ]
    normals = projective_normals(WIDTH)

    checked_gcd_trivial = 0
    common_root_paid = 0
    simple_planes = 0
    twin_planes = 0
    planes_with_hits = 0
    total_hits = 0
    total_residual_hits = 0
    total_twin_branch_hits = 0
    max_hits = 0
    max_residual_hits = 0
    max_twin_classes = 0
    max_twin_class_size = 0
    max_twin_group_hits = 0
    max_reduced_rank = 0
    max_common_roots = 0
    tight_residual_planes = 0
    residual_bound_slack_min: int | None = None
    twin_examples = []

    for normal in normals:
        basis = [trim(vec) for vec in nullspace([normal], WIDTH)]
        if len(basis) != 3 or rank_vectors([coeffs(poly, WIDTH) for poly in basis], WIDTH) != 3:
            fail("normal did not define a projective plane", normal=normal, basis=basis)

        groups, common_roots = line_groups(basis, H)
        if common_roots:
            common_root_paid += 1
            max_common_roots = max(max_common_roots, len(common_roots))
            continue

        checked_gcd_trivial += 1
        twin_groups = [roots for roots in groups.values() if len(roots) >= 2]
        singleton_count = sum(1 for roots in groups.values() if len(roots) == 1)
        if twin_groups:
            twin_planes += 1
        else:
            simple_planes += 1
        max_twin_classes = max(max_twin_classes, len(twin_groups))
        max_twin_class_size = max(
            max_twin_class_size,
            max((len(group) for group in twin_groups), default=0),
        )

        hits = [
            (combo, poly)
            for combo, poly in divisors
            if dot(normal, coeffs(poly, WIDTH)) == 0
        ]
        if hits:
            planes_with_hits += 1
        total_hits += len(hits)
        max_hits = max(max_hits, len(hits))

        residual_hits = []
        for combo, poly in hits:
            roots = set(combo)
            touches_twin = False
            for group in twin_groups:
                group_set = set(group)
                if roots & group_set:
                    touches_twin = True
                    if not group_set <= roots:
                        fail(
                            "hit met a twin class without containing all twins",
                            normal=normal,
                            group=group,
                            roots=combo,
                        )
            if not touches_twin:
                residual_hits.append((combo, poly))

        residual_bound_numerator = comb(singleton_count, 2)
        residual_weight = len(residual_hits) * comb(J, 2)
        if residual_weight > residual_bound_numerator:
            fail(
                "residual singleton-pair bound failed",
                normal=normal,
                residual_hits=len(residual_hits),
                singleton_count=singleton_count,
            )
        slack = residual_bound_numerator - residual_weight
        residual_bound_slack_min = slack if residual_bound_slack_min is None else min(residual_bound_slack_min, slack)
        if slack == 0 and residual_hits:
            tight_residual_planes += 1
        total_residual_hits += len(residual_hits)
        max_residual_hits = max(max_residual_hits, len(residual_hits))

        for group in twin_groups:
            group_set = set(group)
            group_hits = [
                (combo, poly)
                for combo, poly in hits
                if group_set <= set(combo)
            ]
            if not group_hits:
                continue
            total_twin_branch_hits += len(group_hits)
            max_twin_group_hits = max(max_twin_group_hits, len(group_hits))
            G = locator(group)
            vanishing_basis = subspace_vanishing_basis(basis, group)
            reduced_j = J - len(group)
            reduced_basis = [poly_div_exact(poly, G) for poly in vanishing_basis]
            reduced_rank = rank_vectors([coeffs(poly, reduced_j + 1) for poly in reduced_basis], reduced_j + 1)
            if reduced_rank > 2:
                fail(
                    "twin branch did not reduce to projective dimension <= 1",
                    normal=normal,
                    group=group,
                    reduced_rank=reduced_rank,
                )
            max_reduced_rank = max(max_reduced_rank, reduced_rank)

            for combo, poly in group_hits:
                reduced = poly_div_exact(poly, G)
                remaining = tuple(root for root in combo if root not in group_set)
                if reduced != locator(remaining):
                    fail(
                        "reduced twin hit is not the remaining locator",
                        normal=normal,
                        group=group,
                        roots=combo,
                    )
                if not in_span(reduced, reduced_basis, reduced_j + 1):
                    fail(
                        "reduced twin hit left the reduced projective line",
                        normal=normal,
                        group=group,
                        roots=combo,
                    )

            if len(twin_examples) < 10:
                twin_examples.append({
                    "normal": list(normal),
                    "group": list(group),
                    "group_hits": len(group_hits),
                    "reduced_j": reduced_j,
                    "reduced_vector_rank": reduced_rank,
                    "reduced_projective_dimension": reduced_rank - 1,
                })

    return {
        "schema": "conjecture_f_dim2_skeleton_v1",
        "status": "PASS",
        "dag_node": "f_dim2_skeleton",
        "field": {"p": P},
        "domain": {"type": "F_p_star", "n": len(H), "elements": H},
        "parameters": {"j": J, "ambient_vector_dimension": WIDTH, "projective_dimension": 2},
        "claims_checked": {
            "common_root_planes_routed_to_paid_branch": True,
            "twin_classes_are_all_or_none": True,
            "twin_branches_reduce_to_projective_lines": True,
            "residual_obeys_singleton_pair_bound": True,
        },
        "counts": {
            "projective_planes_total": len(normals),
            "common_root_paid_planes": common_root_paid,
            "gcd_trivial_planes_checked": checked_gcd_trivial,
            "simple_planes": simple_planes,
            "twin_planes": twin_planes,
            "planes_with_divisor_hits": planes_with_hits,
            "degree_j_locators": len(divisors),
            "total_divisor_hits": total_hits,
            "total_residual_hits": total_residual_hits,
            "total_twin_branch_hits": total_twin_branch_hits,
        },
        "maxima": {
            "common_roots_in_paid_plane": max_common_roots,
            "hits_per_plane": max_hits,
            "twin_classes_per_plane": max_twin_classes,
            "twin_class_size": max_twin_class_size,
            "twin_group_hits": max_twin_group_hits,
            "residual_hits_per_plane": max_residual_hits,
            "reduced_vector_rank": max_reduced_rank,
            "reduced_projective_dimension": max_reduced_rank - 1,
        },
        "residual_pair_bound": {
            "weight_per_residual_hit": comb(J, 2),
            "tight_nonempty_planes": tight_residual_planes,
            "minimum_slack": residual_bound_slack_min,
        },
        "sample_twin_reductions": twin_examples,
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="compare a stored certificate with a fresh run")
    args = parser.parse_args()

    report = build_report()
    print("=" * 72)
    print("Conjecture F dimension-two skeleton verifier")
    print("=" * 72)
    print(f"status: {report['status']}")
    print(f"projective planes: {report['counts']['projective_planes_total']}")
    print(f"gcd-trivial planes checked: {report['counts']['gcd_trivial_planes_checked']}")
    print(f"twin planes: {report['counts']['twin_planes']}")
    print(f"max residual hits per plane: {report['maxima']['residual_hits_per_plane']}")
    print(f"max reduced projective dimension: {report['maxima']['reduced_projective_dimension']}")

    if args.check:
        stored = json.loads(args.check.read_text())
        if stored != report:
            raise SystemExit(f"certificate mismatch: {args.check}")
        print(f"checked {args.check}")

    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")

    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
