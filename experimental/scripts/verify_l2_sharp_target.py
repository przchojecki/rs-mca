#!/usr/bin/env python3
"""Stress tests for the exact L2 sharp interleaved-list target.

This verifier is deliberately small.  It tests the part of L2 that is not
settled by the support-intersection bridge: over-agreement can create
interleaved mass, so the falsification target is whether that mass can grow like
a Cartesian product rather than like a polynomial support-overlap codegree.

The script checks three finite objects.

1. The aligned quotient packet count used as Quot_mu in the target note.
2. The abstract K_{m,m} grid over-agreement design and its size formula.
3. A realized Reed-Solomon K_{2,2} gluing over a prime-field multiplicative
   subgroup, computed by exact list enumeration, together with its punctured
   codegree profile.

Standard library only.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from math import comb


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def e_empty(r_size: int, b_size: int, mu: int) -> int:
    """# of mu ordered b-subsets of [r_size] with empty common intersection."""
    if b_size < 0 or b_size > r_size:
        return 0
    return sum(
        (-1) ** j * comb(r_size, j) * comb(r_size - j, b_size - j) ** mu
        for j in range(b_size + 1)
    )


def h_thresh(a: int, tau: int, fiber_size: int) -> int:
    return ceil_div(a - tau, fiber_size) if a > tau else 0


def aligned_quotient_packet(
    quotient_order: int,
    ell: int,
    mu: int,
    a: int,
    tau: int,
    fiber_size: int,
) -> int:
    """Exact aligned quotient-core count L_mu(a,tau)."""
    q_minus_omitted = quotient_order - 1
    h_val = h_thresh(a, tau, fiber_size)
    if h_val > ell:
        return 0
    return sum(
        comb(q_minus_omitted, c)
        * e_empty(q_minus_omitted - c, ell - c, mu)
        for c in range(max(h_val, 0), ell + 1)
    )


def aligned_quotient_budget(n: int, k: int, a: int, mu: int) -> dict:
    """A concrete conservative aligned quotient budget.

    For every subgroup fiber size M dividing both n and k, take the worst slack
    overlap tau in [0,M-1] and sum the resulting aligned packet counts.  This is
    intentionally a budget, not a claim that all packets are disjoint.
    """
    packets = []
    total = 0
    for fiber_size in range(2, min(n, k) + 1):
        if n % fiber_size or k % fiber_size:
            continue
        quotient_order = n // fiber_size
        ell = k // fiber_size
        if ell <= 0 or ell > quotient_order - 1:
            continue
        candidates = [
            aligned_quotient_packet(quotient_order, ell, mu, a, tau, fiber_size)
            for tau in range(fiber_size)
        ]
        best = max(candidates)
        best_tau = candidates.index(best)
        if best:
            packets.append(
                {
                    "M": fiber_size,
                    "N": quotient_order,
                    "ell": ell,
                    "tau": best_tau,
                    "packet": best,
                }
            )
            total += best
    return {"total": total, "packets": packets}


def primitive_root(p: int) -> int:
    phi = p - 1
    factors = []
    x = phi
    d = 2
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, phi // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root found for p={p}")


def subgroup(p: int, n: int) -> list[int]:
    if (p - 1) % n:
        raise ValueError(f"n={n} does not divide p-1={p-1}")
    gen = pow(primitive_root(p), (p - 1) // n, p)
    out = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * gen) % p
    if len(set(out)) != n:
        raise ValueError("subgroup generator has wrong order")
    return out


def eval_poly(coeffs: tuple[int, ...], x: int, p: int) -> int:
    total = 0
    power = 1
    for c in coeffs:
        total = (total + c * power) % p
        power = (power * x) % p
    return total


def all_codewords(p: int, h_values: list[int], k: int) -> list[tuple[int, ...]]:
    return [
        tuple(eval_poly(coeffs, x, p) for x in h_values)
        for coeffs in itertools.product(range(p), repeat=k)
    ]


def vanish_values(p: int, h_values: list[int], root_indices: list[int]) -> tuple[int, ...]:
    vals = []
    roots = [h_values[i] for i in root_indices]
    for x in h_values:
        y = 1
        for r in roots:
            y = (y * (x - r)) % p
        vals.append(y)
    return tuple(vals)


def choose_filler(p: int, forbidden: set[int]) -> int:
    for y in range(p):
        if y not in forbidden:
            return y
    raise ValueError("field too small to choose filler")


def support_families(word: tuple[int, ...], codewords: list[tuple[int, ...]], a: int) -> list[frozenset[int]]:
    supports = []
    seen = set()
    for cw in codewords:
        supp = frozenset(i for i, y in enumerate(word) if cw[i] == y)
        if len(supp) >= a and supp not in seen:
            supports.append(supp)
            seen.add(supp)
    return supports


def interleaved_count(families: list[list[frozenset[int]]], a: int) -> int:
    count = 0
    for supports in itertools.product(*families):
        common = set(supports[0])
        for supp in supports[1:]:
            common &= supp
            if len(common) < a:
                break
        if len(common) >= a:
            count += 1
    return count


def punctured_johnson_bound(s: int, k: int, a: int) -> dict:
    """Elementary pairwise-overlap bound for an [s,k] punctured RS code.

    Distinct degree-<k codewords agree on at most k-1 puncture points.  If L
    agreement supports of size >=a have pairwise overlaps <=k-1, incidence
    counting gives L <= s(s-k+1)/(a^2-s(k-1)) when the denominator is positive.
    """
    if 2 * a > s + k - 1:
        return {"mode": "unique", "bound": 1, "denominator": None}
    denom = a * a - s * (k - 1)
    if denom <= 0:
        return {"mode": "none", "bound": None, "denominator": denom}
    numerator = s * (s - k + 1)
    return {
        "mode": "johnson",
        "bound": numerator // denom,
        "numerator": numerator,
        "denominator": denom,
    }


def johnson_anchor_threshold(k: int, a: int) -> dict:
    """First anchor support size not controlled by punctured Johnson."""
    if k <= 1:
        return {
            "k": k,
            "a": a,
            "sigma": a - k,
            "threshold": None,
            "johnson_controls_through": None,
            "excess_over_a": None,
            "formula_excess": None,
        }
    threshold = ceil_div(a * a, k - 1)
    sigma = a - k
    formula_excess = ceil_div(a * (sigma + 1), k - 1)
    return {
        "k": k,
        "a": a,
        "sigma": sigma,
        "threshold": threshold,
        "johnson_controls_through": threshold - 1,
        "excess_over_a": threshold - a,
        "formula_excess": formula_excess,
    }


def two_row_codegree_profile(families: list[list[frozenset[int]]], a: int) -> dict:
    """Return row-1 anchored punctured-list/codegree data for two support families."""
    row1, row2 = families
    inners = [
        sum(1 for supp2 in row2 if len(supp1 & supp2) >= a)
        for supp1 in row1
    ]
    return {
        "inner_codegrees": inners,
        "codegree_sum": sum(inners),
        "max_inner_codegree": max(inners) if inners else 0,
        "all_inner_unique": all(value <= 1 for value in inners),
    }


def support_size_histogram(family: list[frozenset[int]]) -> dict[int, int]:
    hist: dict[int, int] = {}
    for supp in family:
        hist[len(supp)] = hist.get(len(supp), 0) + 1
    return dict(sorted(hist.items()))


def exact_a_locator_count(family: list[frozenset[int]], a: int) -> int:
    """Count exact a-subsets lying in full agreement supports."""
    return sum(comb(len(supp), a) for supp in family if len(supp) >= a)


def shell_codegree_bound(families: list[list[frozenset[int]]], k: int, a: int) -> dict:
    """Deterministic two-row shell bound from punctured Johnson plus tail."""
    row1, row2 = families
    threshold = johnson_anchor_threshold(k, a)
    threshold_value = threshold["threshold"]
    row1_hist = support_size_histogram(row1)
    controlled_terms = []
    controlled_bound = 0
    tail_count = 0
    for s, count in row1_hist.items():
        if threshold_value is None or s < threshold_value:
            profile = punctured_johnson_bound(s, k, a)
            if profile["bound"] is None:
                raise ValueError("shell below Johnson threshold was not controlled")
            contribution = count * profile["bound"]
            controlled_terms.append(
                {
                    "support_size": s,
                    "count": count,
                    "mode": profile["mode"],
                    "per_anchor_bound": profile["bound"],
                    "contribution": contribution,
                }
            )
            controlled_bound += contribution
        else:
            tail_count += count

    row2_list_size = len(row2)
    tail_trivial_bound = tail_count * row2_list_size
    exact_count = exact_a_locator_count(row1, a)
    if threshold_value is None or threshold_value > max((len(s) for s in row1), default=0):
        tail_count_from_exact_a = 0
    else:
        tail_count_from_exact_a = exact_count // comb(threshold_value, a)
    return {
        "row1_support_histogram": row1_hist,
        "row2_list_size": row2_list_size,
        "johnson_threshold": threshold,
        "controlled_terms": controlled_terms,
        "controlled_bound": controlled_bound,
        "tail_count": tail_count,
        "tail_trivial_bound": tail_trivial_bound,
        "exact_a_locator_count_row1": exact_count,
        "tail_count_bound_from_exact_a": tail_count_from_exact_a,
        "total_bound": controlled_bound + tail_trivial_bound,
    }


def kmm_grid_design(k: int, a: int, m: int) -> dict:
    """Abstract K_{m,m} grid design obeying the same-row RS overlap cap."""
    overlap_cap = k - 1
    cell_size = a - overlap_cap
    if cell_size <= 0:
        raise ValueError("need a >= k for a nontrivial design")
    n_min = overlap_cap + m * m * cell_size
    row_support_size = overlap_cap + m * cell_size
    return {
        "k": k,
        "a": a,
        "m": m,
        "overlap_cap": overlap_cap,
        "cell_size": cell_size,
        "minimum_n": n_min,
        "row_support_size": row_support_size,
        "interleaved_edges": m * m,
        "grid_edges_at_n_min": (n_min - overlap_cap) // cell_size,
    }


def realized_rs_k22() -> dict:
    """Exact RS enumeration for a prime-field K_{2,2} gluing witness."""
    p, n, k, a, m = 29, 14, 3, 5, 2
    h_values = subgroup(p, n)
    codewords = all_codewords(p, h_values, k)
    overlap_cap = k - 1
    core = list(range(overlap_cap))
    cell_size = a - overlap_cap
    cells = []
    cursor = overlap_cap
    for _ in range(m * m):
        cells.append(list(range(cursor, cursor + cell_size)))
        cursor += cell_size
    assert cursor == n

    vanish = vanish_values(p, h_values, core)
    # Row-1 codewords c_i and row-2 codewords d_j.  All agree on the core and
    # otherwise differ by scalar multiples of the same vanishing polynomial.
    c_rows = [tuple((lam * y) % p for y in vanish) for lam in (1, 2)]
    d_rows = [tuple((lam * y) % p for y in vanish) for lam in (3, 4)]

    word1 = [None] * n
    word2 = [None] * n
    for idx in core:
        word1[idx] = 0
        word2[idx] = 0
    for i in range(m):
        for j in range(m):
            for idx in cells[i * m + j]:
                word1[idx] = c_rows[i][idx]
                word2[idx] = d_rows[j][idx]
    for idx in range(n):
        if word1[idx] is None:
            word1[idx] = choose_filler(p, {cw[idx] for cw in c_rows})
        if word2[idx] is None:
            word2[idx] = choose_filler(p, {cw[idx] for cw in d_rows})

    families = [
        support_families(tuple(word1), codewords, a),
        support_families(tuple(word2), codewords, a),
    ]
    interleaved = interleaved_count(families, a)
    product_bound = len(families[0]) * len(families[1])
    max_base = max(len(families[0]), len(families[1]))
    support_sizes = [[len(s) for s in fam] for fam in families]
    common_profile = {}
    for supp1, supp2 in itertools.product(*families):
        r = len(supp1 & supp2)
        common_profile[r] = common_profile.get(r, 0) + 1
    codegree_profile = two_row_codegree_profile(families, a)
    shell_bound = shell_codegree_bound(families, k, a)
    johnson_profiles = [
        punctured_johnson_bound(len(supp), k, a)
        for supp in families[0]
    ]
    threshold = johnson_anchor_threshold(k, a)
    large_anchor_flags = [
        threshold["threshold"] is not None and len(supp) >= threshold["threshold"]
        for supp in families[0]
    ]
    johnson_ok = all(
        profile["bound"] is not None and inner <= profile["bound"]
        for inner, profile in zip(
            codegree_profile["inner_codegrees"], johnson_profiles
        )
    )

    return {
        "p": p,
        "n": n,
        "k": k,
        "a": a,
        "m": m,
        "base_lists": [len(families[0]), len(families[1])],
        "max_base": max_base,
        "product_bound": product_bound,
        "interleaved": interleaved,
        "mass_creation": interleaved > max_base,
        "saving_vs_cartesian": interleaved / product_bound if product_bound else None,
        "support_sizes": support_sizes,
        "common_intersection_profile": dict(sorted(common_profile.items())),
        "punctured_codegree_profile": codegree_profile,
        "codegree_identity_holds": codegree_profile["codegree_sum"] == interleaved,
        "shell_codegree_bound": shell_bound,
        "punctured_johnson_profiles": johnson_profiles,
        "johnson_anchor_threshold": threshold,
        "large_anchor_flags": large_anchor_flags,
        "punctured_johnson_ok": johnson_ok,
        "kmm_grid_model": kmm_grid_design(k, a, m),
    }


def run() -> dict:
    quotient_example = aligned_quotient_budget(n=64, k=16, a=18, mu=2)
    threshold_example = johnson_anchor_threshold(k=16, a=18)
    designs = [kmm_grid_design(k=3, a=5, m=m) for m in (2, 3, 4, 5)]
    witness = realized_rs_k22()
    checks = {
        "quotient_budget_nonnegative": quotient_example["total"] >= 0,
        "kmm_grid_formula": all(d["interleaved_edges"] == d["grid_edges_at_n_min"] for d in designs),
        "rs_witness_creates_mass": witness["mass_creation"],
        "rs_witness_realizes_k22": witness["interleaved"] == witness["product_bound"] == 4,
        "rs_witness_codegree_identity": witness["codegree_identity_holds"],
        "rs_witness_shell_bound": witness["interleaved"] <= witness["shell_codegree_bound"]["total_bound"],
        "rs_witness_punctured_johnson": witness["punctured_johnson_ok"],
    }
    return {
        "status": "EXPERIMENTAL / FALSIFICATION",
        "aligned_quotient_budget_example": quotient_example,
        "johnson_anchor_threshold_example": threshold_example,
        "kmm_designs": designs,
        "realized_rs_k22": witness,
        "checks": checks,
        "pass": all(checks.values()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args(argv)

    result = run()
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"L2 sharp-target stress test ({result['status']})")
        qb = result["aligned_quotient_budget_example"]
        print(f"  aligned quotient budget example: total={qb['total']}, packets={len(qb['packets'])}")
        jt = result["johnson_anchor_threshold_example"]
        print(
            "  Johnson anchor threshold example: "
            f"k={jt['k']}, a={jt['a']}, threshold={jt['threshold']}, "
            f"controls_s<={jt['johnson_controls_through']}, "
            f"excess={jt['excess_over_a']}"
        )
        print("  K_{m,m} abstract designs:")
        for d in result["kmm_designs"]:
            print(
                f"    m={d['m']}: n_min={d['minimum_n']}, "
                f"edges={d['interleaved_edges']}, grid_edges={d['grid_edges_at_n_min']}"
            )
        w = result["realized_rs_k22"]
        print("  realized RS K_{2,2} witness:")
        print(
            f"    F_{w['p']}, n={w['n']}, k={w['k']}, a={w['a']}: "
            f"base={w['base_lists']}, interleaved={w['interleaved']}, "
            f"product={w['product_bound']}, creates_mass={w['mass_creation']}"
        )
        print(
            f"    punctured codegrees={w['punctured_codegree_profile']['inner_codegrees']}, "
            f"sum={w['punctured_codegree_profile']['codegree_sum']}, "
            f"max={w['punctured_codegree_profile']['max_inner_codegree']}"
        )
        print(
            f"    Johnson threshold={w['johnson_anchor_threshold']}, "
            f"large_anchor_flags={w['large_anchor_flags']}"
        )
        sb = w["shell_codegree_bound"]
        print(
            f"    shell bound={sb['total_bound']} "
            f"(controlled={sb['controlled_bound']}, tail={sb['tail_trivial_bound']}), "
            f"row1_exact_a={sb['exact_a_locator_count_row1']}, "
            f"tail_from_exact_a<={sb['tail_count_bound_from_exact_a']}"
        )
        print(f"    punctured Johnson profiles={w['punctured_johnson_profiles']}")
        print(f"  RESULT: {'PASS' if result['pass'] else 'FAIL'}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
