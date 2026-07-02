#!/usr/bin/env python3
"""E3 spread-regime design evidence.

This is an EXPERIMENTAL / AUDIT verifier for Fable's E3 evidence item.
It does not prove a worst-case spread-regime theorem.  It tests whether
low-intersection co-support designs create hidden rank losses in the
split-locator, distinct-slope linear systems.

Run:
  python3 experimental/scripts/verify_spread_regime_design_evidence.py
  python3 experimental/scripts/verify_spread_regime_design_evidence.py --emit
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
    full_slopes = slope_sequence(name, len(family), p)
    rows = []
    first_saturation = None
    hidden_losses = []
    hidden_loss_nondegenerate_prefixes = []
    largest_nondegenerate_prefix = 0
    largest_nondegenerate_nullity = 0
    for prefix in range(1, len(family) + 1):
        matrix = stacked_alignment_matrix(domain, family[:prefix], t, full_slopes[:prefix], p)
        rank = rank_mod_p(matrix, p)
        equation_rows = prefix * t
        expected_rank = min(equation_rows, 2 * n)
        deficiency = expected_rank - rank
        nullity = 2 * n - rank
        if first_saturation is None and rank == 2 * n:
            first_saturation = prefix
        if equation_rows <= 2 * n and deficiency:
            hidden_losses.append({"prefix": prefix, "deficiency": deficiency})
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
        rows.append({
            "prefix_locators": prefix,
            "equation_rows": equation_rows,
            "rank": rank,
            "expected_ambient_rank": expected_rank,
            "deficiency_vs_ambient": deficiency,
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
    if name == "constant_one":
        classification = "same_slope_diagnostic_not_an_E3_distinct_slope_test"
    elif hidden_loss_nondegenerate_prefixes:
        classification = "candidate_nondegenerate_hidden_spread_dependency"
    elif hidden_losses:
        classification = "rank_loss_detected_but_degenerate_v_kernel"
    else:
        classification = "ambient_limited_no_hidden_distinct_slope_rank_loss"
    return {
        "slope_mode": name,
        "ambient_linear_bound_floor((2n-1)/t)": ambient_linear_bound,
        "first_prefix_with_full_ambient_rank": first_saturation,
        "ambient_bound_prefix_nondegeneracy_certificate": certificate,
        "largest_nondegenerate_prefix_certified": largest_nondegenerate_prefix,
        "largest_nondegenerate_prefix_nullity": largest_nondegenerate_nullity,
        "hidden_losses_before_ambient_saturation": summarize_prefix_records(hidden_losses),
        "hidden_loss_nondegenerate_prefixes": summarize_prefix_records(
            hidden_loss_nondegenerate_prefixes
        ),
        "sampled_prefix_rows": [
            row for row in rows
            if (
                row["prefix_locators"] in {1, 2, 3, 4, 8, 16, 32, 64}
                or row["prefix_locators"] == len(family)
                or row["prefix_locators"] == ambient_linear_bound
                or row["prefix_locators"] == first_saturation
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
        and result["hidden_loss_nondegenerate_prefixes"]["count"]
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
            "so any early rank loss is higher-order spread evidence."
        ),
        "interpretation_table": {
            "NO_NONDEGENERATE_DISTINCT_SPREAD_COUNTEREXAMPLE": (
                "No tested spread design produced a nondegenerate distinct-slope "
                "rank-loss prefix. Rank losses that do appear collapse into the "
                "S_T(v)=0 kernel, so they are not finite-slope mass."
            ),
            "CANDIDATE_SPREAD_COUNTEREXAMPLE": (
                "A nondegenerate distinct-slope rank loss before ambient "
                "saturation was found; package the minimal case as a "
                "counterexample candidate."
            ),
        },
        "prime": P,
        "seed": SEED,
        "cases": cases,
        "overall_interpretation": (
            "NO_NONDEGENERATE_DISTINCT_SPREAD_COUNTEREXAMPLE"
            if not hidden_cases
            else "CANDIDATE_SPREAD_COUNTEREXAMPLE"
        ),
        "hidden_cases": [case["name"] for case in hidden_cases],
        "script_sha256": sha256_text(source),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
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
                "hidden losses={losses}, hidden+nondeg={hnondeg}, "
                "largest nondeg={nondeg}".format(
                    mode=result["slope_mode"],
                    sat=result["first_prefix_with_full_ambient_rank"],
                    bound=result["ambient_linear_bound_floor((2n-1)/t)"],
                    losses=result["hidden_losses_before_ambient_saturation"]["count"],
                    hnondeg=result["hidden_loss_nondegenerate_prefixes"]["count"],
                    nondeg=result["largest_nondegenerate_prefix_certified"],
                )
            )
    print(f"overall: {report['overall_interpretation']}")

    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
