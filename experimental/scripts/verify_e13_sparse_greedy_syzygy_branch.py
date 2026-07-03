#!/usr/bin/env python3
"""E13 sparse-greedy syzygy branch certificate.

This follow-up to the E13 spread-exception census replays the bounded n=32
control exceptions and certifies the exact algebraic row-dependency carried by
each one.  It turns the opaque "unclassified non-geometry" bucket into a named
finite-model branch: one-dimensional, full-support sparse-greedy syzygies.

Run:
  python3 experimental/scripts/verify_e13_sparse_greedy_syzygy_branch.py
  python3 experimental/scripts/verify_e13_sparse_greedy_syzygy_branch.py --emit
  python3 experimental/scripts/verify_e13_sparse_greedy_syzygy_branch.py --check experimental/data/certificates/spread-regime-design-evidence/e13_sparse_greedy_syzygy_branch.json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/spread-regime-design-evidence/"
    "e13_sparse_greedy_syzygy_branch.json"
)

CELLS = [
    {
        "case_name": "greedy_32_j5_lambda1",
        "slope_mode": "distinct_geometric",
        "size": 5,
    },
    {
        "case_name": "greedy_32_j6_lambda2",
        "slope_mode": "distinct_linear",
        "size": 6,
    },
    {
        "case_name": "greedy_32_j6_lambda2",
        "slope_mode": "distinct_geometric",
        "size": 6,
    },
]


def load_e3_module() -> Any:
    path = Path(__file__).with_name("verify_spread_regime_design_evidence.py")
    spec = importlib.util.spec_from_file_location("verify_spread_regime_design_evidence", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


E3 = load_e3_module()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_counter(counter: Counter[Any]) -> dict[str, int]:
    return {
        json.dumps(key, sort_keys=True) if not isinstance(key, str) else key: value
        for key, value in sorted(counter.items(), key=lambda item: json.dumps(item[0], sort_keys=True))
    }


def get_case(case_name: str, prefix_size: int = 16) -> tuple[list[tuple[int, ...]], int, int, int]:
    for case in E3.build_cases():
        if case["name"] == case_name:
            family = [tuple(sorted(item)) for item in case["family"][:prefix_size]]
            return family, case["n"], case["j"], case["t"]
    raise ValueError(case_name)


def point_histogram(family: list[tuple[int, ...]], n: int) -> dict[str, int]:
    counts = [0] * n
    for block in family:
        for point in block:
            counts[point] += 1
    return {str(key): value for key, value in sorted(Counter(counts).items())}


def pair_intersection_histogram(family: list[tuple[int, ...]]) -> dict[str, int]:
    counts: Counter[int] = Counter()
    for left, right in itertools.combinations(family, 2):
        counts[len(set(left) & set(right))] += 1
    return {str(key): value for key, value in sorted(counts.items())}


def relation_coefficients_by_block(relation: dict[str, Any], size: int, t: int) -> list[list[int]]:
    entries = relation["entries"]
    if len(entries) != size * t:
        raise AssertionError("relation has the wrong number of entries")
    blocks = []
    for block_index in range(size):
        coeffs = [
            entries[block_index * t + moment]["coefficient"]
            for moment in range(t)
        ]
        blocks.append(coeffs)
    return blocks


def coefficient_weight_histogram(coefficients_by_block: list[list[int]], p: int) -> dict[str, int]:
    weights = Counter(
        sum(1 for coeff in block if coeff % p)
        for block in coefficients_by_block
    )
    return {str(key): value for key, value in sorted(weights.items())}


def exception_record(
    *,
    subset_indices: tuple[int, ...],
    family: list[tuple[int, ...]],
    n: int,
    j: int,
    t: int,
    slopes: list[int],
    rank: int,
    degree_deficiency: int,
    p: int,
) -> dict[str, Any]:
    domain = E3.subgroup_domain(n, p)
    relation = E3.row_dependency_certificate(
        domain,
        family,
        t,
        slopes,
        p,
    )
    if relation["left_nullity"] != 1:
        raise AssertionError(("left_nullity", subset_indices, relation["left_nullity"]))
    coeffs = relation_coefficients_by_block(relation["relations"][0], len(family), t)
    zero_blocks = [idx for idx, block in enumerate(coeffs) if not any(c % p for c in block)]
    if zero_blocks:
        raise AssertionError(("zero relation block", subset_indices, zero_blocks))
    relation_digest = sha256_text(json.dumps(coeffs, sort_keys=True))
    deletion_records = []
    for remove_index in range(len(family)):
        subfamily = [block for idx, block in enumerate(family) if idx != remove_index]
        subslopes = [slope for idx, slope in enumerate(slopes) if idx != remove_index]
        subrank = E3.rank_mod_p(
            E3.stacked_alignment_matrix(domain, subfamily, t, subslopes, p),
            p,
        )
        expected = min(len(subfamily) * t, 2 * (j + t))
        deletion_records.append({
            "removed_locator_position": remove_index,
            "rank": subrank,
            "expected_degree_cap_rank": expected,
            "degree_deficiency": expected - subrank,
        })
    if any(record["degree_deficiency"] for record in deletion_records):
        raise AssertionError(("nonminimal syzygy", subset_indices, deletion_records))
    return {
        "subset_indices": list(subset_indices),
        "family": [list(item) for item in family],
        "rank": rank,
        "degree_deficiency": degree_deficiency,
        "relation_left_nullity": relation["left_nullity"],
        "relation_full_locator_support": True,
        "relation_coefficients_by_block": coeffs,
        "relation_coefficient_weight_histogram": coefficient_weight_histogram(coeffs, p),
        "relation_coefficients_sha256": relation_digest,
        "single_deletion_independence": True,
        "single_deletion_rank_records": deletion_records,
        "point_multiplicity_histogram": point_histogram(family, n),
        "pair_intersection_histogram": pair_intersection_histogram(family),
    }


def analyze_cell(cell: dict[str, Any]) -> dict[str, Any]:
    case_name = cell["case_name"]
    slope_mode = cell["slope_mode"]
    size = cell["size"]
    universe, n, j, t = get_case(case_name)
    p = E3.P
    domain = E3.subgroup_domain(n, p)
    slopes = E3.slope_sequence(slope_mode, size, p)
    degree_cap = 2 * (j + t)
    exceptions = []
    rank_distribution: Counter[int] = Counter()
    loss_subsets = 0
    degenerate_loss_subsets = 0

    for subset_indices in itertools.combinations(range(len(universe)), size):
        family = [universe[idx] for idx in subset_indices]
        matrix = E3.stacked_alignment_matrix(domain, family, t, slopes, p)
        rank = E3.rank_mod_p(matrix, p)
        rank_distribution[rank] += 1
        degree_deficiency = min(size * t, degree_cap) - rank
        if degree_deficiency <= 0:
            continue
        loss_subsets += 1
        cert = E3.nondegeneracy_certificate(domain, family, t, slopes, p)
        if not cert["union_bound_certifies_nondegenerate_solution"]:
            degenerate_loss_subsets += 1
            continue
        exceptions.append(exception_record(
            subset_indices=subset_indices,
            family=family,
            n=n,
            j=j,
            t=t,
            slopes=slopes,
            rank=rank,
            degree_deficiency=degree_deficiency,
            p=p,
        ))

    weight_hist = Counter()
    point_hist_types = Counter()
    pair_hist_types = Counter()
    deletion_deficiencies = Counter()
    for record in exceptions:
        weight_hist.update({
            tuple(sorted(record["relation_coefficient_weight_histogram"].items())): 1
        })
        point_hist_types[tuple(sorted(record["point_multiplicity_histogram"].items()))] += 1
        pair_hist_types[tuple(sorted(record["pair_intersection_histogram"].items()))] += 1
        for deletion_record in record["single_deletion_rank_records"]:
            deletion_deficiencies[deletion_record["degree_deficiency"]] += 1

    return {
        "case_name": case_name,
        "slope_mode": slope_mode,
        "size": size,
        "n": n,
        "j": j,
        "t": t,
        "A": n - j,
        "k": n - j - t,
        "prime": p,
        "family_universe_size": len(universe),
        "degree_cap": degree_cap,
        "slopes": slopes,
        "total_subsets": sum(rank_distribution.values()),
        "rank_distribution": {
            str(key): value for key, value in sorted(rank_distribution.items())
        },
        "loss_subsets": loss_subsets,
        "degenerate_loss_subsets": degenerate_loss_subsets,
        "nondegenerate_syzygy_exceptions": len(exceptions),
        "all_exceptions_have_one_dimensional_left_nullspace": all(
            record["relation_left_nullity"] == 1 for record in exceptions
        ),
        "all_relations_have_full_locator_support": all(
            record["relation_full_locator_support"] for record in exceptions
        ),
        "all_single_deletions_are_independent": all(
            record["single_deletion_independence"] for record in exceptions
        ),
        "single_deletion_deficiency_histogram": {
            str(key): value for key, value in sorted(deletion_deficiencies.items())
        },
        "relation_weight_type_histogram": canonical_counter(weight_hist),
        "point_histogram_type_count": len(point_hist_types),
        "pair_histogram_type_count": len(pair_hist_types),
        "exception_records": exceptions,
    }


def build_report() -> dict[str, Any]:
    cells = [analyze_cell(cell) for cell in CELLS]
    source = Path(__file__).read_text()
    total_exceptions = sum(cell["nondegenerate_syzygy_exceptions"] for cell in cells)
    return {
        "title": "E13 sparse-greedy syzygy branch certificate",
        "status": "EXPERIMENTAL / AUDIT",
        "dag_nodes": ["spread_exception_classification", "spread_regime_bound"],
        "fable_evidence_item": "E13 follow-up",
        "question": (
            "Do the n=32 non-geometry controls from the E13 census share an "
            "exact algebraic structure that can be named as a separate branch?"
        ),
        "method": (
            "Replay the bounded n=32 control cells from E13. For every "
            "nondegenerate below-cap rank loss, compute the left-nullspace "
            "relation and verify the two zero-polynomial identities using the "
            "E3 row-dependency certificate."
        ),
        "interpretation": (
            "All replayed n=32 control exceptions are one-dimensional, "
            "full-locator-support sparse-greedy syzygies, and every one-block "
            "deletion is independent. This does not pay or bound the branch "
            "asymptotically, but it replaces the opaque unclassified bucket by "
            "a precise algebraic target."
        ),
        "non_claims": [
            "This is not a proof of spread_regime_bound.",
            "This does not classify every n=32 support family.",
            "This does not show the sparse-greedy branch is paid or bounded uniformly.",
        ],
        "total_nondegenerate_syzygy_exceptions": total_exceptions,
        "all_exceptions_have_one_dimensional_left_nullspace": all(
            cell["all_exceptions_have_one_dimensional_left_nullspace"]
            for cell in cells
        ),
        "all_relations_have_full_locator_support": all(
            cell["all_relations_have_full_locator_support"] for cell in cells
        ),
        "all_single_deletions_are_independent": all(
            cell["all_single_deletions_are_independent"] for cell in cells
        ),
        "cells": cells,
        "script_sha256": sha256_text(source),
    }


def assert_report_invariants(report: dict[str, Any]) -> None:
    if report["total_nondegenerate_syzygy_exceptions"] != 71:
        raise AssertionError(report["total_nondegenerate_syzygy_exceptions"])
    if not report["all_exceptions_have_one_dimensional_left_nullspace"]:
        raise AssertionError("left-nullity invariant failed")
    if not report["all_relations_have_full_locator_support"]:
        raise AssertionError("full-support invariant failed")
    if not report["all_single_deletions_are_independent"]:
        raise AssertionError("single-deletion independence failed")
    expected = {
        ("greedy_32_j5_lambda1", "distinct_geometric", 5): (1, 1, 0),
        ("greedy_32_j6_lambda2", "distinct_linear", 6): (36, 58, 22),
        ("greedy_32_j6_lambda2", "distinct_geometric", 6): (34, 56, 22),
    }
    for cell in report["cells"]:
        key = (cell["case_name"], cell["slope_mode"], cell["size"])
        if key not in expected:
            raise AssertionError(key)
        nondeg, loss, deg = expected[key]
        got = (
            cell["nondegenerate_syzygy_exceptions"],
            cell["loss_subsets"],
            cell["degenerate_loss_subsets"],
        )
        if got != (nondeg, loss, deg):
            raise AssertionError((key, got))
        if cell["single_deletion_deficiency_histogram"] != {"0": nondeg * cell["size"]}:
            raise AssertionError((key, cell["single_deletion_deficiency_histogram"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
    parser.add_argument("--check", type=Path, help="recompute and compare with an existing artifact")
    args = parser.parse_args()

    report = build_report()
    assert_report_invariants(report)
    print(f"total sparse-greedy syzygy exceptions: {report['total_nondegenerate_syzygy_exceptions']}")
    print(
        "one-dimensional left nullspace: "
        f"{report['all_exceptions_have_one_dimensional_left_nullspace']}"
    )
    print(f"full locator support: {report['all_relations_have_full_locator_support']}")
    print(f"single-deletion independent: {report['all_single_deletions_are_independent']}")
    for cell in report["cells"]:
        print(
            "{case} {mode} size={size}: nondeg={nondeg}, loss={loss}, degenerate={deg}".format(
                case=cell["case_name"],
                mode=cell["slope_mode"],
                size=cell["size"],
                nondeg=cell["nondegenerate_syzygy_exceptions"],
                loss=cell["loss_subsets"],
                deg=cell["degenerate_loss_subsets"],
            )
        )

    if args.check:
        expected = json.loads(args.check.read_text())
        if expected != report:
            raise AssertionError(f"artifact mismatch: {args.check}")
        print(f"checked {args.check}")

    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()
