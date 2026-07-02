#!/usr/bin/env python3
"""E3 spread-regime design evidence.

This is an EXPERIMENTAL / AUDIT verifier for Fable's E3 evidence item.
It does not prove a worst-case spread-regime theorem.  It tests whether
low-intersection co-support designs create hidden rank losses in the
split-locator, distinct-slope linear systems.

Run:
  python3 experimental/scripts/verify_spread_regime_design_evidence.py
  python3 experimental/scripts/verify_spread_regime_design_evidence.py --emit
  python3 experimental/scripts/verify_spread_regime_design_evidence.py --ag24-census --emit
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/spread-regime-design-evidence/"
    "spread_regime_design_evidence.json"
)
CENSUS_OUTPUT = Path(
    "experimental/data/certificates/spread-regime-design-evidence/"
    "ag24_exception_census.json"
)

P = 193
SEED = 2026070203


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inv_mod(x: int, p: int = P) -> int:
    return pow(x % p, -1, p)


def rank_mod_p(matrix: list[list[int]], p: int = P) -> int:
    if not matrix:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])
    work = [[entry % p for entry in row] for row in matrix]
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if work[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        factor = inv_mod(work[rank][col], p)
        work[rank] = [(factor * x) % p for x in work[rank]]
        for row in range(rows):
            if row != rank and work[row][col] % p:
                multiple = work[row][col]
                work[row] = [
                    (work[row][idx] - multiple * work[rank][idx]) % p
                    for idx in range(cols)
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def rref_mod_p(matrix: list[list[int]], p: int = P) -> tuple[list[list[int]], list[int]]:
    if not matrix:
        return [], []
    rows = len(matrix)
    cols = len(matrix[0])
    work = [[entry % p for entry in row] for row in matrix]
    rank = 0
    pivots: list[int] = []
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if work[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        factor = inv_mod(work[rank][col], p)
        work[rank] = [(factor * x) % p for x in work[rank]]
        for row in range(rows):
            if row != rank and work[row][col] % p:
                multiple = work[row][col]
                work[row] = [
                    (work[row][idx] - multiple * work[rank][idx]) % p
                    for idx in range(cols)
                ]
        pivots.append(col)
        rank += 1
        if rank == rows:
            break
    return work[:rank], pivots


def nullspace_basis(matrix: list[list[int]], width: int, p: int = P) -> list[list[int]]:
    if matrix:
        rref, pivots = rref_mod_p(matrix, p)
    else:
        rref, pivots = [], []
    pivot_set = set(pivots)
    basis: list[list[int]] = []
    for free_col in range(width):
        if free_col in pivot_set:
            continue
        vector = [0] * width
        vector[free_col] = 1
        for row_idx, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-rref[row_idx][free_col]) % p
        basis.append(vector)
    return basis


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    if not matrix:
        return []
    return [list(column) for column in zip(*matrix)]


def canonical_vector(values: list[int], p: int = P) -> list[int]:
    for value in values:
        if value % p:
            factor = inv_mod(value, p)
            return [(factor * entry) % p for entry in values]
    return [entry % p for entry in values]


def factor_int(n: int) -> list[int]:
    factors = []
    d = 2
    value = n
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(p: int = P) -> int:
    factors = factor_int(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for {p}")


def subgroup_domain(n: int, p: int = P) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    generator = pow(primitive_root(p), (p - 1) // n, p)
    domain = [pow(generator, idx, p) for idx in range(n)]
    if len(set(domain)) != n:
        raise AssertionError("subgroup generator has wrong order")
    return domain


def poly_mul_mod_p(left: list[int], right: list[int], p: int = P) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, ai in enumerate(left):
        for j, bj in enumerate(right):
            out[i + j] = (out[i + j] + ai * bj) % p
    return out


def locator_poly(roots: list[int], p: int = P) -> list[int]:
    poly = [1]
    for root in roots:
        poly = poly_mul_mod_p(poly, [(-root) % p, 1], p)
    return poly


def eval_poly(poly: list[int], x: int, p: int = P) -> int:
    value = 0
    power = 1
    for coeff in poly:
        value = (value + coeff * power) % p
        power = (power * x) % p
    return value


def trim_poly(poly: list[int], p: int = P) -> list[int]:
    out = [entry % p for entry in poly]
    while out and out[-1] == 0:
        out.pop()
    return out


def add_scaled_poly(target: list[int], poly: list[int], scale: int, p: int = P) -> None:
    if len(target) < len(poly):
        target.extend([0] * (len(poly) - len(target)))
    for idx, coeff in enumerate(poly):
        target[idx] = (target[idx] + scale * coeff) % p


def syndrome_matrix_for_indices(
    domain: list[int],
    root_indices: tuple[int, ...],
    t: int,
    p: int = P,
) -> list[list[int]]:
    roots = [domain[idx] for idx in root_indices]
    locator = locator_poly(roots, p)
    rows = []
    for m in range(1, t + 1):
        rows.append([
            (eval_poly(locator, x, p) * pow(x, m, p)) % p
            for x in domain
        ])
    return rows


def stacked_alignment_matrix(
    domain: list[int],
    family: list[tuple[int, ...]],
    t: int,
    slopes: list[int],
    p: int = P,
) -> list[list[int]]:
    n = len(domain)
    rows: list[list[int]] = []
    for roots, slope in zip(family, slopes):
        syndrome_rows = syndrome_matrix_for_indices(domain, roots, t, p)
        for row in syndrome_rows:
            rows.append(row + [(slope * entry) % p for entry in row])
    if rows and len(rows[0]) != 2 * n:
        raise AssertionError("alignment matrix has wrong width")
    return rows


def gf4_add(a: int, b: int) -> int:
    return a ^ b


def gf4_mul(a: int, b: int) -> int:
    result = 0
    aa = a
    bb = b
    while bb:
        if bb & 1:
            result ^= aa
        bb >>= 1
        aa <<= 1
        if aa & 0b100:
            aa ^= 0b111
    return result & 0b11


def affine_plane_order4_lines() -> list[tuple[int, ...]]:
    def index(x: int, y: int) -> int:
        return 4 * x + y

    lines = []
    for x0 in range(4):
        lines.append(tuple(index(x0, y) for y in range(4)))
    for slope in range(4):
        for intercept in range(4):
            line = []
            for x in range(4):
                y = gf4_add(gf4_mul(slope, x), intercept)
                line.append(index(x, y))
            lines.append(tuple(sorted(line)))
    if len(set(lines)) != 20:
        raise AssertionError("AG(2,4) line construction failed")
    return sorted(set(lines))


def greedy_packing(
    n: int,
    j: int,
    max_intersection: int,
    target_size: int,
    seed: int,
    attempts: int,
) -> list[tuple[int, ...]]:
    rng = random.Random(seed)
    family: list[tuple[int, ...]] = []
    seen: set[tuple[int, ...]] = set()
    for _ in range(attempts):
        candidate = tuple(sorted(rng.sample(range(n), j)))
        if candidate in seen:
            continue
        seen.add(candidate)
        cand_set = set(candidate)
        if all(len(cand_set & set(existing)) <= max_intersection for existing in family):
            family.append(candidate)
            if len(family) >= target_size:
                break
    return family


def pairwise_stats(family: list[tuple[int, ...]], n: int, j: int, t: int) -> dict[str, Any]:
    overlaps = []
    support_intersections = []
    for left, right in itertools.combinations(family, 2):
        c = len(set(left) & set(right))
        overlaps.append(c)
        support_intersections.append(n - (2 * j - c))
    histogram = Counter(overlaps)
    support_histogram = Counter(support_intersections)
    k = n - j - t
    threshold = j - t
    return {
        "max_cosupport_intersection": max(overlaps) if overlaps else 0,
        "cosupport_intersection_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "fm1_dependency_threshold_c_ge": threshold,
        "all_pairs_below_fm1_dependency_threshold": all(c < threshold for c in overlaps),
        "k": k,
        "max_support_intersection": max(support_intersections) if support_intersections else 0,
        "support_intersection_histogram": {
            str(key): value for key, value in sorted(support_histogram.items())
        },
        "all_support_intersections_lt_k": all(s < k for s in support_intersections),
    }


def slope_sequence(mode: str, count: int, p: int = P) -> list[int]:
    if mode == "distinct_linear":
        if count >= p:
            raise ValueError("too many slopes for distinct_linear")
        return list(range(1, count + 1))
    if mode == "distinct_geometric":
        slopes = []
        value = 1
        for _ in range(count):
            slopes.append(value)
            value = (value * 5) % p
        if len(set(slopes)) != count:
            raise ValueError("geometric slopes repeated")
        return slopes
    if mode == "constant_one":
        return [1] * count
    raise ValueError(mode)


def moment_row(domain: list[int], degree: int, p: int = P) -> list[int]:
    return [pow(x, degree, p) for x in domain]


def degree_moment_basis(
    domain: list[int],
    max_degree: int,
    slope_mode: str,
    p: int = P,
) -> list[list[int]]:
    n = len(domain)
    basis: list[list[int]] = []
    if slope_mode == "constant_one":
        for degree in range(1, max_degree + 1):
            row = moment_row(domain, degree, p)
            basis.append(row + row)
    else:
        zeros = [0] * n
        for degree in range(1, max_degree + 1):
            row = moment_row(domain, degree, p)
            basis.append(row + zeros)
        for degree in range(1, max_degree + 1):
            row = moment_row(domain, degree, p)
            basis.append(zeros + row)
    return basis


def degree_moment_inclusion_certificate(
    domain: list[int],
    matrix: list[list[int]],
    max_degree: int,
    slope_mode: str,
    p: int = P,
) -> dict[str, Any]:
    basis = degree_moment_basis(domain, max_degree, slope_mode, p)
    basis_rank = rank_mod_p(basis, p)
    matrix_rank = rank_mod_p(matrix, p)
    joined_rank = rank_mod_p(basis + matrix, p)
    included = joined_rank == basis_rank
    return {
        "max_degree": max_degree,
        "basis_rows": len(basis),
        "basis_rank": basis_rank,
        "matrix_rank": matrix_rank,
        "joined_rank": joined_rank,
        "rowspace_included_in_degree_moment_basis": included,
    }


def row_dependency_certificate(
    domain: list[int],
    family: list[tuple[int, ...]],
    t: int,
    slopes: list[int],
    p: int = P,
) -> dict[str, Any]:
    matrix = stacked_alignment_matrix(domain, family, t, slopes, p)
    rank = rank_mod_p(matrix, p)
    left_nullspace = [
        canonical_vector(vector, p)
        for vector in nullspace_basis(transpose(matrix), len(matrix), p)
    ]
    relation_records = []
    for relation in left_nullspace:
        u_poly: list[int] = []
        v_poly: list[int] = []
        entries = []
        row_idx = 0
        for line_idx, roots in enumerate(family):
            locator = locator_poly([domain[idx] for idx in roots], p)
            for moment in range(1, t + 1):
                coeff = relation[row_idx]
                row_idx += 1
                moment_poly = [0] * moment + locator
                add_scaled_poly(u_poly, moment_poly, coeff, p)
                add_scaled_poly(v_poly, moment_poly, coeff * slopes[line_idx], p)
                entries.append({
                    "line_index": line_idx,
                    "moment": moment,
                    "coefficient": coeff,
                    "slope": slopes[line_idx],
                })
        u_poly = trim_poly(u_poly, p)
        v_poly = trim_poly(v_poly, p)
        relation_records.append({
            "entries": entries,
            "u_polynomial_coefficients": u_poly,
            "v_polynomial_coefficients": v_poly,
            "u_polynomial_zero": not u_poly,
            "v_polynomial_zero": not v_poly,
        })
    if not all(
        item["u_polynomial_zero"] and item["v_polynomial_zero"]
        for item in relation_records
    ):
        raise AssertionError("row dependency did not produce zero polynomial identities")
    return {
        "row_count": len(matrix),
        "rank": rank,
        "left_nullity": len(left_nullspace),
        "expected_left_nullity": len(matrix) - rank,
        "relations": relation_records,
    }


def nondegeneracy_certificate(
    domain: list[int],
    family: list[tuple[int, ...]],
    t: int,
    slopes: list[int],
    p: int = P,
) -> dict[str, Any]:
    n = len(domain)
    matrix = stacked_alignment_matrix(domain, family, t, slopes, p)
    basis = nullspace_basis(matrix, 2 * n, p)
    nullity = len(basis)
    if nullity == 0:
        return {
            "nullity": 0,
            "p_greater_than_locator_count": p > len(family),
            "all_v_syndrome_restrictions_nonzero": False,
            "union_bound_certifies_nondegenerate_solution": False,
        }

    zero_restrictions = []
    for idx, roots in enumerate(family):
        syndrome_rows = syndrome_matrix_for_indices(domain, roots, t, p)
        restriction_rows = []
        for syn_row in syndrome_rows:
            restriction_rows.append([
                sum(syn_row[col] * vector[n + col] for col in range(n)) % p
                for vector in basis
            ])
        restriction_rank = rank_mod_p(restriction_rows, p)
        if restriction_rank == 0:
            zero_restrictions.append(idx)

    p_large = p > len(family)
    all_nonzero = not zero_restrictions
    return {
        "nullity": nullity,
        "p_greater_than_locator_count": p_large,
        "all_v_syndrome_restrictions_nonzero": all_nonzero,
        "zero_restriction_locator_count": len(zero_restrictions),
        "zero_restriction_first_indices": zero_restrictions[:12],
        "union_bound_certifies_nondegenerate_solution": p_large and all_nonzero,
        "logic": (
            "Inside the nullspace, each condition S_T(v)=0 is a proper linear "
            "subspace. Since p is larger than the number of tested locators, "
            "the union of these proper subspaces cannot cover the nullspace."
        ),
    }


def v_zero_restriction_indices(
    domain: list[int],
    nullspace: list[list[int]],
    family: list[tuple[int, ...]],
    t: int,
    p: int = P,
) -> list[int]:
    n = len(domain)
    zero_restrictions = []
    for idx, roots in enumerate(family):
        syndrome_rows = syndrome_matrix_for_indices(domain, roots, t, p)
        restriction_rows = []
        for syn_row in syndrome_rows:
            restriction_rows.append([
                sum(syn_row[col] * vector[n + col] for col in range(n)) % p
                for vector in nullspace
            ])
        restriction_rank = rank_mod_p(restriction_rows, p)
        if restriction_rank == 0:
            zero_restrictions.append(idx)
    return zero_restrictions


def cap_saturation_degeneracy_certificate(
    domain: list[int],
    prefix_family: list[tuple[int, ...]],
    full_family: list[tuple[int, ...]],
    t: int,
    slopes: list[int],
    degree_cap: int,
    p: int = P,
) -> dict[str, Any]:
    n = len(domain)
    matrix = stacked_alignment_matrix(domain, prefix_family, t, slopes, p)
    rank = rank_mod_p(matrix, p)
    nullspace = nullspace_basis(matrix, 2 * n, p)
    prefix_zero = v_zero_restriction_indices(domain, nullspace, prefix_family, t, p)
    full_zero = v_zero_restriction_indices(domain, nullspace, full_family, t, p)
    saturated = rank == degree_cap
    return {
        "prefix_size": len(prefix_family),
        "rank": rank,
        "degree_cap": degree_cap,
        "saturates_degree_cap": saturated,
        "nullity": len(nullspace),
        "prefix_v_zero_restriction_count": len(prefix_zero),
        "full_family_v_zero_restriction_count": len(full_zero),
        "full_family_size": len(full_family),
        "cap_saturation_forces_v_zero_on_full_tested_family": (
            saturated and len(full_zero) == len(full_family)
        ),
        "logic": (
            "For distinct slopes, degree-cap saturation means the rowspace is "
            "the full W_u plus W_v moment quotient. The nullspace therefore "
            "annihilates W_v, so every tested locator syndrome S_T(v) is zero."
        ),
    }


def explicit_ag24_exception_witnesses(domain: list[int], p: int = P) -> list[dict[str, Any]]:
    witnesses = [
        {
            "name": "six_line_linear_exception",
            "slope_mode": "distinct_linear",
            "family": [
                (0, 1, 2, 3),
                (0, 4, 8, 12),
                (0, 5, 10, 15),
                (0, 6, 11, 13),
                (2, 5, 11, 12),
                (12, 13, 14, 15),
            ],
        },
        {
            "name": "seven_line_linear_exception",
            "slope_mode": "distinct_linear",
            "family": [
                (0, 4, 8, 12),
                (0, 5, 10, 15),
                (1, 4, 11, 14),
                (1, 5, 9, 13),
                (2, 6, 10, 14),
                (3, 6, 9, 12),
                (3, 7, 11, 15),
            ],
        },
    ]
    rows = []
    for witness in witnesses:
        family = [tuple(item) for item in witness["family"]]
        t = 2
        j = 4
        slopes = slope_sequence(witness["slope_mode"], len(family), p)
        matrix = stacked_alignment_matrix(domain, family, t, slopes, p)
        rank = rank_mod_p(matrix, p)
        equation_rows = len(family) * t
        degree_cap = 2 * (j + t)
        degree_deficiency = min(equation_rows, degree_cap) - rank
        cert = nondegeneracy_certificate(domain, family, t, slopes, p)
        stats = pairwise_stats(family, len(domain), j, t)
        if not stats["all_pairs_below_fm1_dependency_threshold"]:
            raise AssertionError(f"{witness['name']} is not a spread witness")
        if degree_deficiency <= 0:
            raise AssertionError(f"{witness['name']} has no below-cap rank loss")
        if not cert["union_bound_certifies_nondegenerate_solution"]:
            raise AssertionError(f"{witness['name']} is degenerate")
        relation_certificate = row_dependency_certificate(
            domain,
            family,
            t,
            slopes,
            p,
        )
        rows.append({
            "name": witness["name"],
            "slope_mode": witness["slope_mode"],
            "family": [list(item) for item in family],
            "slopes": slopes,
            "t": t,
            "j": j,
            "equation_rows": equation_rows,
            "rank": rank,
            "degree_cap": degree_cap,
            "degree_deficiency": degree_deficiency,
            "pairwise_spread_stats": stats,
            "nondegeneracy_certificate": cert,
            "row_dependency_certificate": relation_certificate,
            "interpretation": (
                "bounded_nonzero_finite_slope_below_cap_exception"
            ),
        })
    return rows


def precomputed_stacked_matrix(
    block_rows: dict[tuple[int, int], list[list[int]]],
    subset_indices: tuple[int, ...],
) -> list[list[int]]:
    matrix = []
    for position, line_idx in enumerate(subset_indices):
        matrix.extend(block_rows[(position, line_idx)])
    return matrix


def ag24_exception_census(p: int = P) -> dict[str, Any]:
    family = affine_plane_order4_lines()
    domain = subgroup_domain(16, p)
    t = 2
    j = 4
    n = 16
    modes = ["distinct_linear", "distinct_geometric"]
    sizes = [6, 7]

    syndrome_rows_by_line = {
        idx: syndrome_matrix_for_indices(domain, line, t, p)
        for idx, line in enumerate(family)
    }
    rows = []
    for mode in modes:
        max_size = max(sizes)
        slopes = slope_sequence(mode, max_size, p)
        block_rows = {}
        for position in range(max_size):
            slope = slopes[position]
            for line_idx, syndrome_rows in syndrome_rows_by_line.items():
                block_rows[(position, line_idx)] = [
                    row + [(slope * entry) % p for entry in row]
                    for row in syndrome_rows
                ]

        for size in sizes:
            rank_distribution: Counter[int] = Counter()
            zero_restriction_distribution: Counter[int] = Counter()
            point_multiplicity_distribution: Counter[int] = Counter()
            point_histogram_distribution: Counter[str] = Counter()
            loss_subsets = 0
            nondegenerate_loss_subsets = 0
            degenerate_loss_subsets = 0
            first_nondegenerate_example = None
            first_degenerate_example = None
            for subset_indices in itertools.combinations(range(len(family)), size):
                matrix = precomputed_stacked_matrix(block_rows, subset_indices)
                rank = rank_mod_p(matrix, p)
                rank_distribution[rank] += 1
                degree_cap = 2 * (j + t)
                degree_deficiency = min(size * t, degree_cap) - rank
                if degree_deficiency <= 0:
                    continue
                loss_subsets += 1
                subset = [family[idx] for idx in subset_indices]
                cert = nondegeneracy_certificate(domain, subset, t, slopes[:size], p)
                zero_count = cert.get("zero_restriction_locator_count", -1)
                zero_restriction_distribution[zero_count] += 1
                point_counts = [0] * n
                for line in subset:
                    for point in line:
                        point_counts[point] += 1
                max_point_multiplicity = max(point_counts)
                point_multiplicity_distribution[max_point_multiplicity] += 1
                point_hist = {
                    str(key): value
                    for key, value in sorted(Counter(point_counts).items())
                }
                point_histogram_distribution[json.dumps(point_hist, sort_keys=True)] += 1
                example = {
                    "subset_indices": list(subset_indices),
                    "family": [list(item) for item in subset],
                    "rank": rank,
                    "degree_deficiency": degree_deficiency,
                    "zero_restriction_locator_count": zero_count,
                    "point_multiplicity_histogram": point_hist,
                    "max_point_multiplicity": max_point_multiplicity,
                }
                if cert["union_bound_certifies_nondegenerate_solution"]:
                    nondegenerate_loss_subsets += 1
                    if first_nondegenerate_example is None:
                        first_nondegenerate_example = example
                else:
                    degenerate_loss_subsets += 1
                    if first_degenerate_example is None:
                        first_degenerate_example = example

            total_subsets = sum(rank_distribution.values())
            rows.append({
                "mode": mode,
                "size": size,
                "total_subsets": total_subsets,
                "rank_distribution": {
                    str(key): value for key, value in sorted(rank_distribution.items())
                },
                "loss_subsets": loss_subsets,
                "nondegenerate_loss_subsets": nondegenerate_loss_subsets,
                "degenerate_loss_subsets": degenerate_loss_subsets,
                "zero_restriction_distribution_on_losses": {
                    str(key): value
                    for key, value in sorted(zero_restriction_distribution.items())
                },
                "max_point_multiplicity_distribution_on_losses": {
                    str(key): value
                    for key, value in sorted(point_multiplicity_distribution.items())
                },
                "point_histogram_distribution_on_losses": {
                    key: value
                    for key, value in sorted(point_histogram_distribution.items())
                },
                "first_nondegenerate_example": first_nondegenerate_example,
                "first_degenerate_example": first_degenerate_example,
            })

    return {
        "title": "AG(2,4) bounded exception census for E3",
        "status": "EXPERIMENTAL / AUDIT",
        "prime": p,
        "n": n,
        "j": j,
        "t": t,
        "degree_cap": 2 * (j + t),
        "family": "all 20 lines of AG(2,4)",
        "sizes": sizes,
        "modes": modes,
        "rows": rows,
    }


def summarize_prefix_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {
            "count": 0,
            "first": None,
            "last": None,
            "max_deficiency": 0,
            "records_sha256": sha256_text("[]"),
        }
    return {
        "count": len(records),
        "first": records[0],
        "last": records[-1],
        "max_deficiency": max(record["deficiency"] for record in records),
        "records_sha256": sha256_text(json.dumps(records, sort_keys=True)),
    }


def analyze_slope_mode(
    name: str,
    domain: list[int],
    family: list[tuple[int, ...]],
    t: int,
    p: int = P,
) -> dict[str, Any]:
    n = len(domain)
    j = len(family[0])
    degree_cap = j + t if name == "constant_one" else min(2 * n, 2 * (j + t))
    full_slopes = slope_sequence(name, len(family), p)
    rows = []
    first_saturation = None
    hidden_losses = []
    hidden_loss_nondegenerate_prefixes = []
    degree_cap_losses = []
    degree_cap_loss_nondegenerate_prefixes = []
    first_degree_cap_prefix = None
    full_matrix = stacked_alignment_matrix(domain, family, t, full_slopes, p)
    rowspace_certificate = degree_moment_inclusion_certificate(
        domain,
        full_matrix,
        j + t,
        name,
        p,
    )
    if not rowspace_certificate["rowspace_included_in_degree_moment_basis"]:
        raise AssertionError(f"{name} rows are not in the degree-moment basis")
    if rowspace_certificate["basis_rank"] > degree_cap:
        raise AssertionError(f"{name} basis rank exceeds declared degree cap")
    largest_nondegenerate_prefix = 0
    largest_nondegenerate_nullity = 0
    for prefix in range(1, len(family) + 1):
        matrix = stacked_alignment_matrix(domain, family[:prefix], t, full_slopes[:prefix], p)
        rank = rank_mod_p(matrix, p)
        equation_rows = prefix * t
        expected_rank = min(equation_rows, 2 * n)
        expected_degree_rank = min(equation_rows, degree_cap)
        deficiency = expected_rank - rank
        degree_deficiency = expected_degree_rank - rank
        nullity = 2 * n - rank
        if first_saturation is None and rank == 2 * n:
            first_saturation = prefix
        if first_degree_cap_prefix is None and rank == degree_cap:
            first_degree_cap_prefix = prefix
        if equation_rows <= 2 * n and deficiency:
            hidden_losses.append({"prefix": prefix, "deficiency": deficiency})
        if equation_rows <= degree_cap and degree_deficiency:
            degree_cap_losses.append({"prefix": prefix, "deficiency": degree_deficiency})
        cert = nondegeneracy_certificate(
            domain,
            family[:prefix],
            t,
            full_slopes[:prefix],
            p,
        )
        if cert["union_bound_certifies_nondegenerate_solution"]:
            largest_nondegenerate_prefix = prefix
            largest_nondegenerate_nullity = cert["nullity"]
            if equation_rows <= 2 * n and deficiency:
                hidden_loss_nondegenerate_prefixes.append({
                    "prefix": prefix,
                    "deficiency": deficiency,
                    "nullity": cert["nullity"],
                })
            if equation_rows <= degree_cap and degree_deficiency:
                degree_cap_loss_nondegenerate_prefixes.append({
                    "prefix": prefix,
                    "deficiency": degree_deficiency,
                    "nullity": cert["nullity"],
                })
        rows.append({
            "prefix_locators": prefix,
            "equation_rows": equation_rows,
            "rank": rank,
            "expected_ambient_rank": expected_rank,
            "deficiency_vs_ambient": deficiency,
            "expected_degree_cap_rank": expected_degree_rank,
            "deficiency_vs_degree_cap": degree_deficiency,
            "nullity": nullity,
        })

    ambient_linear_bound = (2 * n - 1) // t
    certificate = nondegeneracy_certificate(
        domain,
        family[:max(1, min(len(family), ambient_linear_bound))],
        t,
        full_slopes[:max(1, min(len(family), ambient_linear_bound))],
        p,
    )
    if first_saturation is None:
        first_saturation = len(family) + 1
    if first_degree_cap_prefix is None:
        first_degree_cap_prefix = len(family) + 1
    cap_degeneracy = None
    if name != "constant_one" and first_degree_cap_prefix <= len(family):
        cap_degeneracy = cap_saturation_degeneracy_certificate(
            domain,
            family[:first_degree_cap_prefix],
            family,
            t,
            full_slopes[:first_degree_cap_prefix],
            degree_cap,
            p,
        )
        if not cap_degeneracy["cap_saturation_forces_v_zero_on_full_tested_family"]:
            raise AssertionError(f"{name} cap saturation did not force v-zero")
    if name == "constant_one":
        classification = (
            "same_slope_design_specific_degree_loss"
            if degree_cap_losses
            else "same_slope_degree_cap_diagnostic_not_an_E3_distinct_slope_test"
        )
    elif degree_cap_loss_nondegenerate_prefixes:
        classification = "candidate_nondegenerate_design_specific_spread_dependency"
    elif degree_cap_losses:
        classification = "design_specific_rank_loss_detected_but_degenerate_v_kernel"
    elif hidden_losses:
        classification = "moment_quotient_cap_limited_no_extra_dependency"
    else:
        classification = "ambient_limited_before_moment_cap"
    return {
        "slope_mode": name,
        "ambient_linear_bound_floor((2n-1)/t)": ambient_linear_bound,
        "degree_moment_rank_cap": degree_cap,
        "degree_moment_rank_cap_formula": (
            "j+t for constant-slope rows; 2(j+t) for distinct-slope rows"
        ),
        "degree_moment_rowspace_certificate": rowspace_certificate,
        "first_prefix_with_full_ambient_rank": first_saturation,
        "first_prefix_reaching_degree_moment_cap": first_degree_cap_prefix,
        "ambient_bound_prefix_nondegeneracy_certificate": certificate,
        "largest_nondegenerate_prefix_certified": largest_nondegenerate_prefix,
        "largest_nondegenerate_prefix_nullity": largest_nondegenerate_nullity,
        "hidden_losses_before_ambient_saturation": summarize_prefix_records(hidden_losses),
        "hidden_loss_nondegenerate_prefixes": summarize_prefix_records(
            hidden_loss_nondegenerate_prefixes
        ),
        "degree_cap_losses": summarize_prefix_records(degree_cap_losses),
        "degree_cap_loss_nondegenerate_prefixes": summarize_prefix_records(
            degree_cap_loss_nondegenerate_prefixes
        ),
        "cap_saturation_degeneracy_certificate": cap_degeneracy,
        "sampled_prefix_rows": [
            row for row in rows
            if (
                row["prefix_locators"] in {1, 2, 3, 4, 8, 16, 32, 64}
                or row["prefix_locators"] == len(family)
                or row["prefix_locators"] == ambient_linear_bound
                or row["prefix_locators"] == first_saturation
                or row["prefix_locators"] == first_degree_cap_prefix
            )
        ],
        "all_prefix_rows_sha256": sha256_text(json.dumps(rows, sort_keys=True)),
        "classification": classification,
    }


def build_cases() -> list[dict[str, Any]]:
    return [
        {
            "name": "ag2_4_lines",
            "construction": "all 20 lines of AG(2,4), pairwise intersections 0 or 1",
            "n": 16,
            "j": 4,
            "t": 2,
            "family": affine_plane_order4_lines(),
        },
        {
            "name": "greedy_32_j5_lambda1",
            "construction": "deterministic random-greedy 5-subset packing, pairwise intersections <= 1",
            "n": 32,
            "j": 5,
            "t": 3,
            "family": greedy_packing(32, 5, 1, 48, SEED + 1, 200000),
        },
        {
            "name": "greedy_32_j6_lambda2",
            "construction": "deterministic random-greedy 6-subset packing, pairwise intersections <= 2",
            "n": 32,
            "j": 6,
            "t": 3,
            "family": greedy_packing(32, 6, 2, 64, SEED + 2, 200000),
        },
        {
            "name": "greedy_64_j6_lambda1",
            "construction": "deterministic random-greedy 6-subset packing, pairwise intersections <= 1",
            "n": 64,
            "j": 6,
            "t": 4,
            "family": greedy_packing(64, 6, 1, 80, SEED + 3, 300000),
        },
    ]


def analyze_case(case: dict[str, Any]) -> dict[str, Any]:
    n = case["n"]
    j = case["j"]
    t = case["t"]
    family = [tuple(sorted(item)) for item in case["family"]]
    if len(set(family)) != len(family):
        raise AssertionError(f"duplicate blocks in {case['name']}")
    domain = subgroup_domain(n, P)
    stats = pairwise_stats(family, n, j, t)
    if not stats["all_pairs_below_fm1_dependency_threshold"]:
        raise AssertionError(f"{case['name']} is not in the spread regime")
    if not stats["all_support_intersections_lt_k"]:
        raise AssertionError(f"{case['name']} has support intersections >= k")
    mode_results = [
        analyze_slope_mode(mode, domain, family, t, P)
        for mode in ["distinct_linear", "distinct_geometric", "constant_one"]
    ]
    distinct_candidates = [
        result for result in mode_results
        if result["slope_mode"] != "constant_one"
        and result["degree_cap_loss_nondegenerate_prefixes"]["count"]
    ]
    return {
        "name": case["name"],
        "construction": case["construction"],
        "field": f"F_{P}",
        "n": n,
        "j": j,
        "t": t,
        "A": n - j,
        "k": n - j - t,
        "family_size": len(family),
        "pairwise_spread_stats": stats,
        "slope_mode_results": mode_results,
        "interpretation": (
            "NO_NONDEGENERATE_DISTINCT_SPREAD_COUNTEREXAMPLE"
            if not distinct_candidates
            else "CANDIDATE_SPREAD_COUNTEREXAMPLE"
        ),
    }


def build_report() -> dict[str, Any]:
    cases = [analyze_case(case) for case in build_cases()]
    ag24_domain = subgroup_domain(16, P)
    ag24_exceptions = explicit_ag24_exception_witnesses(ag24_domain, P)
    hidden_cases = [case for case in cases if case["interpretation"] == "CANDIDATE_SPREAD_COUNTEREXAMPLE"]
    source = Path(__file__).read_text()
    return {
        "title": "E3 spread-regime design evidence",
        "status": "EXPERIMENTAL / AUDIT",
        "dag_nodes": ["spread_regime_bound", "r2_rigidity"],
        "fable_evidence_item": "E3",
        "pre_registered_question": (
            "Can co-support designs with pairwise support intersections < k "
            "create hidden distinct-slope alignment dependencies before the "
            "ambient 2n-variable rank limit?"
        ),
        "method": (
            "For each design family, stack the linear systems "
            "S_T(u)+z_T S_T(v)=0 over F_193 for distinct slopes z_T. "
            "Pairwise intersections are below the FM1 dependency threshold, "
            "and the verifier compares rank both to the ambient 2n variable space "
            "and to the proved degree-moment cap 2(j+t)."
        ),
        "interpretation_table": {
            "NO_NONDEGENERATE_DISTINCT_SPREAD_COUNTEREXAMPLE": (
                "No tested spread design produced a nondegenerate distinct-slope "
                "rank-loss prefix beyond the degree-moment cap. Ambient rank "
                "losses are explained by the universal moment quotient."
            ),
            "BOUNDED_EXCEPTION_WITNESS_FOUND": (
                "A bounded-size AG(2,4) subfamily has nondegenerate below-cap "
                "rank loss. This does not show growth, but it rules out a "
                "literal no-exception lemma."
            ),
            "CANDIDATE_SPREAD_COUNTEREXAMPLE": (
                "A nondegenerate distinct-slope rank loss below the "
                "degree-moment cap was found; package the minimal case as a "
                "counterexample candidate."
            ),
        },
        "prime": P,
        "seed": SEED,
        "cases": cases,
        "ag24_below_cap_exception_witnesses": ag24_exceptions,
        "overall_interpretation": (
            "CANDIDATE_SPREAD_COUNTEREXAMPLE"
            if hidden_cases
            else "BOUNDED_EXCEPTION_WITNESS_FOUND"
            if ag24_exceptions
            else "NO_NONDEGENERATE_DISTINCT_SPREAD_COUNTEREXAMPLE"
        ),
        "hidden_cases": [case["name"] for case in hidden_cases],
        "script_sha256": sha256_text(source),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
    parser.add_argument(
        "--ag24-census",
        action="store_true",
        help="run the heavier exact AG(2,4) 6/7-line exception census",
    )
    args = parser.parse_args()

    report = build_report()
    for case in report["cases"]:
        print(
            "[{status}] {name}: n={n}, j={j}, t={t}, size={size}, "
            "max co-intersection={maxc}, interpretation={interp}".format(
                status="PASS" if case["interpretation"] == "NO_NONDEGENERATE_DISTINCT_SPREAD_COUNTEREXAMPLE" else "HIT",
                name=case["name"],
                n=case["n"],
                j=case["j"],
                t=case["t"],
                size=case["family_size"],
                maxc=case["pairwise_spread_stats"]["max_cosupport_intersection"],
                interp=case["interpretation"],
            )
        )
        for result in case["slope_mode_results"]:
            print(
                "    {mode}: first full rank prefix={sat}, bound={bound}, "
                "degree cap={dcap} at prefix={dpre}, degree losses={dlosses}, "
                "largest nondeg={nondeg}".format(
                    mode=result["slope_mode"],
                    sat=result["first_prefix_with_full_ambient_rank"],
                    bound=result["ambient_linear_bound_floor((2n-1)/t)"],
                    dcap=result["degree_moment_rank_cap"],
                    dpre=result["first_prefix_reaching_degree_moment_cap"],
                    dlosses=result["degree_cap_losses"]["count"],
                    nondeg=result["largest_nondegenerate_prefix_certified"],
                )
            )
            cap_cert = result["cap_saturation_degeneracy_certificate"]
            if cap_cert is not None:
                print(
                    "        cap saturation v-zero: {zero}/{total}".format(
                        zero=cap_cert["full_family_v_zero_restriction_count"],
                        total=cap_cert["full_family_size"],
                    )
                )
    print(f"overall: {report['overall_interpretation']}")
    for witness in report["ag24_below_cap_exception_witnesses"]:
        print(
            "    AG(2,4) exception {name}: size={size}, rank={rank}/{cap}, "
            "nondegenerate={nondeg}".format(
                name=witness["name"],
                size=len(witness["family"]),
                rank=witness["rank"],
                cap=min(witness["equation_rows"], witness["degree_cap"]),
                nondeg=witness["nondegeneracy_certificate"][
                    "union_bound_certifies_nondegenerate_solution"
                ],
            )
        )

    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")

    if args.ag24_census:
        census = ag24_exception_census(P)
        for row in census["rows"]:
            print(
                "    census {mode} size={size}: losses={loss}, nondeg={nondeg}, ranks={ranks}".format(
                    mode=row["mode"],
                    size=row["size"],
                    loss=row["loss_subsets"],
                    nondeg=row["nondegenerate_loss_subsets"],
                    ranks=row["rank_distribution"],
                )
            )
        if args.emit:
            CENSUS_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
            CENSUS_OUTPUT.write_text(json.dumps(census, indent=2, sort_keys=True) + "\n")
            print(f"wrote {CENSUS_OUTPUT}")


if __name__ == "__main__":
    main()
