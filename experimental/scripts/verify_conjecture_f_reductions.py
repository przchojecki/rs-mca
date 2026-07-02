#!/usr/bin/env python3
"""Toy verifier for the Conjecture F reduction lemmas.

The proofs are elementary and live in the companion note.  This script checks
the identities over F_97 with H = mu_16:

* common-GCD division maps D_j(H) points injectively into D_{j-w}(H');
* quotient pullback g(Y) -> g(X^M) is exactly the M-periodic stratum;
* gcd-trivial projective pencils meet D_j(H) in at most floor(n/j) points.
* D_j(H) on a gcd-trivial projective plane equals j-fold concurrency for
  the evaluation-hyperplane arrangement.
* gcd-trivial projective-plane evaluation arrangements satisfy the weighted
  pair-counting bound #D_j <= binom(n,2)/(j-1).
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


P = 97
N = 16
J_GCD = 5
COMMON_DEGREE = 2
J_SCALE = 6
SCALE_M = 2
J_VOTING = 4
PENCIL_TRIALS = 500
PLANE_TRIALS = 25
SEED = 2026070202
OUTPUT = Path(
    "experimental/data/certificates/conjecture-f-reductions/"
    "conjecture_f_reductions_toy.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def primitive_root(p: int) -> int:
    factors = []
    m = p - 1
    d = 2
    while d * d <= m:
        if m % d == 0:
            factors.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        factors.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError(f"no primitive root for F_{p}")


def subgroup(order: int) -> list[int]:
    g = primitive_root(P)
    omega = pow(g, (P - 1) // order, P)
    values = [pow(omega, i, P) for i in range(order)]
    assert len(set(values)) == order
    return values


def trim(poly: tuple[int, ...]) -> tuple[int, ...]:
    out = list(poly)
    while len(out) > 1 and out[-1] % P == 0:
        out.pop()
    return tuple(x % P for x in out)


def poly_add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    n = max(len(a), len(b))
    return trim(tuple(((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % P for i in range(n)))


def poly_scale(c: int, a: tuple[int, ...]) -> tuple[int, ...]:
    return trim(tuple((c * x) % P for x in a))


def coeff_at(poly: tuple[int, ...], index: int) -> int:
    return poly[index] % P if index < len(poly) else 0


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
    rem = list(poly)
    div = trim(divisor)
    assert div[-1] == 1
    q = [0] * (max(0, len(rem) - len(div)) + 1)
    while len(rem) >= len(div):
        coeff = rem[-1] % P
        shift = len(rem) - len(div)
        q[shift] = coeff
        for i, di in enumerate(div):
            rem[shift + i] = (rem[shift + i] - coeff * di) % P
        while rem and rem[-1] % P == 0:
            rem.pop()
    assert not rem
    return trim(tuple(q))


def locator(roots: tuple[int, ...]) -> tuple[int, ...]:
    poly = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % P, 1))
    return poly


def compose_x_power(poly: tuple[int, ...], power: int) -> tuple[int, ...]:
    out = [0] * ((len(poly) - 1) * power + 1)
    for i, coeff in enumerate(poly):
        out[i * power] = coeff % P
    return trim(tuple(out))


def monic_degree_j(poly: tuple[int, ...], j: int) -> tuple[int, ...] | None:
    poly = trim(poly)
    if len(poly) != j + 1 or poly[-1] == 0:
        return None
    inv = pow(poly[-1], -1, P)
    return poly_scale(inv, poly)


def canonical_projective(poly: tuple[int, ...]) -> tuple[int, ...] | None:
    poly = trim(poly)
    for coeff in poly:
        if coeff % P:
            return poly_scale(pow(coeff, -1, P), poly)
    return None


def canonical_vector(values: tuple[int, ...]) -> tuple[int, ...] | None:
    for value in values:
        if value % P:
            inv = pow(value, -1, P)
            return tuple((inv * x) % P for x in values)
    return None


def divisor_set(H: list[int], j: int) -> set[tuple[int, ...]]:
    return {locator(tuple(combo)) for combo in itertools.combinations(H, j)}


def root_set(poly: tuple[int, ...], H: list[int]) -> set[int]:
    return {x for x in H if poly_eval(poly, x) == 0}


def check_gcd_reduction(H: list[int]) -> dict:
    common_roots = tuple(H[:COMMON_DEGREE])
    G = locator(common_roots)
    H_reduced = H[COMMON_DEGREE:]
    containing = [
        locator(tuple(combo))
        for combo in itertools.combinations(H, J_GCD)
        if set(common_roots).issubset(combo)
    ]
    images = {poly_div_exact(poly, G) for poly in containing}
    target = divisor_set(H_reduced, J_GCD - COMMON_DEGREE)
    linearity_ok = True
    rng = random.Random(SEED)
    for _ in range(25):
        a = rng.randrange(P)
        b = rng.randrange(P)
        q1 = rng.choice(tuple(images))
        q2 = rng.choice(tuple(images))
        left = poly_add(poly_scale(a, poly_mul(G, q1)), poly_scale(b, poly_mul(G, q2)))
        right = poly_mul(G, poly_add(poly_scale(a, q1), poly_scale(b, q2)))
        linearity_ok &= trim(left) == trim(right)
    ok = len(images) == len(containing) == comb(N - COMMON_DEGREE, J_GCD - COMMON_DEGREE)
    ok &= images == target
    ok &= linearity_ok
    return {
        "name": "common_gcd_reduction",
        "status": "PASS" if ok else "FAIL",
        "n": N,
        "j": J_GCD,
        "common_degree": COMMON_DEGREE,
        "source_count": len(containing),
        "image_count": len(images),
        "target_count": len(target),
        "linearity_spot_checks": 25,
    }


def check_scale_recursion(H: list[int]) -> dict:
    small_order = N // SCALE_M
    H_small = subgroup(small_order)
    small_divisors = divisor_set(H_small, J_SCALE // SCALE_M)
    image = {compose_x_power(g, SCALE_M) for g in small_divisors}
    periodic = set()
    for combo in itertools.combinations(range(N), J_SCALE):
        exponents = set(combo)
        is_union = all(((e + small_order) % N) in exponents for e in exponents)
        if is_union:
            periodic.add(locator(tuple(H[i] for i in combo)))
    roots_match = True
    for g in small_divisors:
        pulled = compose_x_power(g, SCALE_M)
        expected = {x for x in H if poly_eval(g, pow(x, SCALE_M, P)) == 0}
        roots_match &= root_set(pulled, H) == expected
    ok = image == periodic
    ok &= len(image) == comb(small_order, J_SCALE // SCALE_M)
    ok &= roots_match
    return {
        "name": "quotient_pullback_scale_recursion",
        "status": "PASS" if ok else "FAIL",
        "n": N,
        "M": SCALE_M,
        "j": J_SCALE,
        "small_order": small_order,
        "image_count": len(image),
        "periodic_count": len(periodic),
        "expected_count": comb(small_order, J_SCALE // SCALE_M),
    }


def independent(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    scalar = None
    for ai, bi in itertools.zip_longest(a, b, fillvalue=0):
        ai %= P
        bi %= P
        if bi == 0:
            if ai != 0:
                return True
            continue
        candidate = ai * pow(bi, -1, P) % P
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return True
    return False


def gcd_trivial_on_H(a: tuple[int, ...], b: tuple[int, ...], H: list[int]) -> bool:
    return all((poly_eval(a, x), poly_eval(b, x)) != (0, 0) for x in H)


def projective_line(a: tuple[int, ...], b: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [poly_add(a, poly_scale(z, b)) for z in range(P)] + [b]


def random_poly(rng: random.Random, max_degree: int) -> tuple[int, ...]:
    return trim(tuple(rng.randrange(P) for _ in range(max_degree + 1)))


def rank_polys(polys: list[tuple[int, ...]], width: int) -> int:
    rows = [[coeff_at(poly, i) for i in range(width)] for poly in polys]
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, len(rows)):
            if rows[row][col] % P:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, P)
        rows[rank] = [(inv * x) % P for x in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][col] % P:
                factor = rows[row][col]
                rows[row] = [
                    (rows[row][i] - factor * rows[rank][i]) % P
                    for i in range(width)
                ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def gcd_trivial_space(basis: list[tuple[int, ...]], H: list[int]) -> bool:
    return all(any(poly_eval(poly, x) != 0 for poly in basis) for x in H)


def projective_plane_points(basis: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    assert len(basis) == 3
    points = set()
    for a in range(P):
        for b in range(P):
            poly = poly_add(basis[0], poly_add(poly_scale(a, basis[1]), poly_scale(b, basis[2])))
            point = canonical_projective(poly)
            assert point is not None
            points.add(point)
    for b in range(P):
        poly = poly_add(basis[1], poly_scale(b, basis[2]))
        point = canonical_projective(poly)
        assert point is not None
        points.add(point)
    point = canonical_projective(basis[2])
    assert point is not None
    points.add(point)
    return points


def count_divisor_points(a: tuple[int, ...], b: tuple[int, ...],
                         D: set[tuple[int, ...]]) -> int:
    count = 0
    seen = set()
    for poly in projective_line(a, b):
        monic = monic_degree_j(poly, J_VOTING)
        if monic is not None and monic in D and monic not in seen:
            seen.add(monic)
            count += 1
    return count


def check_voting_bound(H: list[int]) -> dict:
    D = divisor_set(H, J_VOTING)
    bound = N // J_VOTING
    rng = random.Random(SEED + 1)
    max_count = 0
    accepted = 0
    attempts = 0

    # First include deterministic pencils through disjoint divisor points.
    divisor_list = sorted(D)
    for a in divisor_list[:30]:
        for b in divisor_list[-30:]:
            attempts += 1
            if independent(a, b) and gcd_trivial_on_H(a, b, H):
                count = count_divisor_points(a, b, D)
                max_count = max(max_count, count)
                accepted += 1
                if count > bound:
                    return {
                        "name": "dimension_one_voting_bound",
                        "status": "FAIL",
                        "counterexample_count": count,
                        "bound": bound,
                    }

    while accepted < PENCIL_TRIALS:
        attempts += 1
        a = random_poly(rng, J_VOTING)
        b = random_poly(rng, J_VOTING)
        if not independent(a, b):
            continue
        if not gcd_trivial_on_H(a, b, H):
            continue
        count = count_divisor_points(a, b, D)
        max_count = max(max_count, count)
        accepted += 1
        if count > bound:
            return {
                "name": "dimension_one_voting_bound",
                "status": "FAIL",
                "counterexample_count": count,
                "bound": bound,
            }
    return {
        "name": "dimension_one_voting_bound",
        "status": "PASS",
        "n": N,
        "j": J_VOTING,
        "projective_bound": bound,
        "accepted_pencils": accepted,
        "attempts": attempts,
        "max_observed_divisor_points": max_count,
    }


def check_hyperplane_concurrency(H: list[int]) -> dict:
    D_classes = {
        canonical_projective(poly)
        for poly in divisor_set(H, J_VOTING)
    }
    assert None not in D_classes
    rng = random.Random(SEED + 2)
    accepted = 0
    attempts = 0
    max_concurrent_points = 0
    total_points = P * P + P + 1
    while accepted < PLANE_TRIALS:
        attempts += 1
        basis = [random_poly(rng, J_VOTING) for _ in range(3)]
        if rank_polys(basis, J_VOTING + 1) != 3:
            continue
        if not gcd_trivial_space(basis, H):
            continue
        points = projective_plane_points(basis)
        if len(points) != total_points:
            return {
                "name": "hyperplane_concurrency_reformulation",
                "status": "FAIL",
                "reason": "projective plane point count mismatch",
                "observed_points": len(points),
                "expected_points": total_points,
            }
        concurrent = {
            point for point in points
            if len(root_set(point, H)) >= J_VOTING
        }
        divisor_points = points & D_classes
        if concurrent != divisor_points:
            return {
                "name": "hyperplane_concurrency_reformulation",
                "status": "FAIL",
                "reason": "concurrency set differs from D_j intersection",
                "concurrent_count": len(concurrent),
                "divisor_count": len(divisor_points),
            }
        max_concurrent_points = max(max_concurrent_points, len(concurrent))
        accepted += 1
    return {
        "name": "hyperplane_concurrency_reformulation",
        "status": "PASS",
        "n": N,
        "j": J_VOTING,
        "projective_dimension": 2,
        "plane_points_each": total_points,
        "accepted_planes": accepted,
        "attempts": attempts,
        "max_observed_concurrent_points": max_concurrent_points,
    }


def evaluation_lines(basis: list[tuple[int, ...]], H: list[int]) -> list[tuple[int, ...]]:
    lines = []
    for x in H:
        line = canonical_vector(tuple(poly_eval(poly, x) for poly in basis))
        if line is None:
            raise AssertionError("basis is not gcd-trivial on H")
        lines.append(line)
    return lines


def incidence_multiplicity(point: tuple[int, ...], line: tuple[int, ...]) -> bool:
    return sum((a * b) % P for a, b in zip(point, line)) % P == 0


def forced_duplicate_plane(H: list[int], rng: random.Random) -> list[tuple[int, ...]] | None:
    a, b = H[0], H[1]
    relation = [(pow(a, i, P) - pow(b, i, P)) % P for i in range(J_VOTING + 1)]
    pivot = next(i for i, value in enumerate(relation) if value)
    inv_pivot = pow(relation[pivot], -1, P)
    null_basis = []
    for free in range(J_VOTING + 1):
        if free == pivot:
            continue
        vec = [0] * (J_VOTING + 1)
        vec[free] = 1
        vec[pivot] = (-relation[free] * inv_pivot) % P
        null_basis.append(trim(tuple(vec)))

    for _ in range(200):
        basis = []
        for _row in range(3):
            poly = (0,)
            for vector in null_basis:
                poly = poly_add(poly, poly_scale(rng.randrange(P), vector))
            basis.append(poly)
        if rank_polys(basis, J_VOTING + 1) != 3:
            continue
        if not gcd_trivial_space(basis, H):
            continue
        if len(set(evaluation_lines(basis, H))) < len(H):
            return basis
    return None


def plane_pair_bound_record(basis: list[tuple[int, ...]], H: list[int]) -> dict:
    line_counts = Counter(evaluation_lines(basis, H))
    points = projective_plane_points(basis)
    high_points = 0
    cross_pair_sum = 0
    max_multiplicity_at_point = 0
    for point in points:
        incident = [
            multiplicity
            for line, multiplicity in line_counts.items()
            if incidence_multiplicity(point, line)
        ]
        total = sum(incident)
        max_multiplicity_at_point = max(max_multiplicity_at_point, total)
        for index, left in enumerate(incident):
            for right in incident[index + 1:]:
                cross_pair_sum += left * right
        if total >= J_VOTING:
            high_points += 1

    total_cross_pairs = 0
    counts = list(line_counts.values())
    for index, left in enumerate(counts):
        for right in counts[index + 1:]:
            total_cross_pairs += left * right

    return {
        "distinct_lines": len(line_counts),
        "max_line_multiplicity": max(counts),
        "high_points": high_points,
        "max_multiplicity_at_point": max_multiplicity_at_point,
        "cross_pair_sum": cross_pair_sum,
        "total_cross_pairs": total_cross_pairs,
        "weighted_bound_ok": high_points * (J_VOTING - 1) <= comb(N, 2),
        "simple_bound_ok": (
            len(line_counts) == N
            and high_points * comb(J_VOTING, 2) <= comb(N, 2)
        ),
    }


def check_plane_pair_counting_bound(H: list[int]) -> dict:
    rng = random.Random(SEED + 3)
    accepted = 0
    attempts = 0
    simple_planes = 0
    repeated_planes = 0
    max_concurrent_points = 0
    max_line_multiplicity = 0
    max_cross_pair_sum = 0
    while accepted < PLANE_TRIALS:
        attempts += 1
        basis = [random_poly(rng, J_VOTING) for _ in range(3)]
        if rank_polys(basis, J_VOTING + 1) != 3:
            continue
        if not gcd_trivial_space(basis, H):
            continue
        record = plane_pair_bound_record(basis, H)
        if record["cross_pair_sum"] != record["total_cross_pairs"]:
            return {
                "name": "projective_plane_pair_counting_bound",
                "status": "FAIL",
                "reason": "weighted pair-counting identity failed",
                "cross_pair_sum": record["cross_pair_sum"],
                "total_cross_pairs": record["total_cross_pairs"],
            }
        if record["max_line_multiplicity"] >= J_VOTING:
            return {
                "name": "projective_plane_pair_counting_bound",
                "status": "FAIL",
                "reason": "line multiplicity reached j in a gcd-trivial plane",
                "max_line_multiplicity": record["max_line_multiplicity"],
            }
        if not record["weighted_bound_ok"]:
            return {
                "name": "projective_plane_pair_counting_bound",
                "status": "FAIL",
                "reason": "weighted high-incidence bound failed",
                "high_points": record["high_points"],
            }
        max_concurrent_points = max(max_concurrent_points, record["high_points"])
        max_line_multiplicity = max(max_line_multiplicity, record["max_line_multiplicity"])
        max_cross_pair_sum = max(max_cross_pair_sum, record["cross_pair_sum"])
        if record["distinct_lines"] == N:
            simple_planes += 1
        else:
            repeated_planes += 1
        accepted += 1

    forced_repeated = 0
    for _ in range(5):
        basis = forced_duplicate_plane(H, rng)
        if basis is None:
            continue
        record = plane_pair_bound_record(basis, H)
        if record["distinct_lines"] == N or record["max_line_multiplicity"] < 2:
            return {
                "name": "projective_plane_pair_counting_bound",
                "status": "FAIL",
                "reason": "forced duplicate plane did not have repeated lines",
            }
        if (
            record["cross_pair_sum"] != record["total_cross_pairs"]
            or record["max_line_multiplicity"] >= J_VOTING
            or not record["weighted_bound_ok"]
        ):
            return {
                "name": "projective_plane_pair_counting_bound",
                "status": "FAIL",
                "reason": "forced duplicate plane failed weighted bound",
                "record": record,
            }
        forced_repeated += 1
        repeated_planes += 1
        max_concurrent_points = max(max_concurrent_points, record["high_points"])
        max_line_multiplicity = max(max_line_multiplicity, record["max_line_multiplicity"])
        max_cross_pair_sum = max(max_cross_pair_sum, record["cross_pair_sum"])

    return {
        "name": "projective_plane_pair_counting_bound",
        "status": "PASS",
        "n": N,
        "j": J_VOTING,
        "accepted_random_planes": accepted,
        "forced_repeated_line_planes": forced_repeated,
        "attempts": attempts,
        "random_simple_planes": simple_planes,
        "repeated_line_planes_total": repeated_planes,
        "weighted_bound_floor": comb(N, 2) // (J_VOTING - 1),
        "weighted_bound_rational": f"{comb(N, 2)}/{J_VOTING - 1}",
        "simple_bound_floor": comb(N, 2) // comb(J_VOTING, 2),
        "simple_bound_rational": f"{comb(N, 2)}/{comb(J_VOTING, 2)}",
        "max_observed_high_incidence_points": max_concurrent_points,
        "max_observed_line_multiplicity": max_line_multiplicity,
        "max_cross_pair_sum": max_cross_pair_sum,
    }


def build_report() -> dict:
    H = subgroup(N)
    checks = [
        check_gcd_reduction(H),
        check_scale_recursion(H),
        check_voting_bound(H),
        check_hyperplane_concurrency(H),
        check_plane_pair_counting_bound(H),
    ]
    return {
        "schema": "conjecture_f_reduction_toy_v1",
        "status": "EXPERIMENTAL_VERIFICATION_OF_PROVED_LEMMAS",
        "field": {"p": P},
        "domain": {"type": "mu_n", "n": N, "elements": H},
        "checks": checks,
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    report = build_report()
    print("=" * 72)
    print("Conjecture F reduction lemmas toy verifier")
    print("=" * 72)
    ok = True
    for check in report["checks"]:
        ok &= check["status"] == "PASS"
        print(f"[{check['status']}] {check['name']}")
        for key, value in check.items():
            if key not in {"name", "status"}:
                print(f"        {key}: {value}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
