#!/usr/bin/env python3
"""E13 spread-exception finite-geometry census.

This verifier strengthens the E3 spread-design packet by classifying every
below-cap AG(2,4) line-subfamily exception in the replayed finite-geometry
cell, and by running bounded n=32 non-geometry control cells.

It is evidence, not a proof of the full spread-regime bound.

Run:
  python3 experimental/scripts/verify_e13_spread_exception_finite_geometry_census.py
  python3 experimental/scripts/verify_e13_spread_exception_finite_geometry_census.py --emit
  python3 experimental/scripts/verify_e13_spread_exception_finite_geometry_census.py --check experimental/data/certificates/spread-regime-design-evidence/e13_spread_exception_finite_geometry_census.json
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
    "e13_spread_exception_finite_geometry_census.json"
)


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


def ag24_parallel_classes() -> dict[tuple[int, ...], int]:
    def index(x: int, y: int) -> int:
        return 4 * x + y

    classes: list[set[tuple[int, ...]]] = []
    classes.append({
        tuple(sorted(index(x0, y) for y in range(4)))
        for x0 in range(4)
    })
    for slope in range(4):
        slope_class = set()
        for intercept in range(4):
            line = []
            for x in range(4):
                y = E3.gf4_add(E3.gf4_mul(slope, x), intercept)
                line.append(index(x, y))
            slope_class.add(tuple(sorted(line)))
        classes.append(slope_class)

    out: dict[tuple[int, ...], int] = {}
    for class_index, lines in enumerate(classes):
        for line in lines:
            out[line] = class_index
    expected = set(E3.affine_plane_order4_lines())
    if set(out) != expected:
        raise AssertionError("AG(2,4) parallel-class reconstruction failed")
    return out


def point_histogram(family: list[tuple[int, ...]], n: int) -> dict[str, int]:
    counts = [0] * n
    for block in family:
        for point in block:
            counts[point] += 1
    return {str(key): value for key, value in sorted(Counter(counts).items())}


def pair_intersection_histogram(family: list[tuple[int, ...]]) -> dict[str, int]:
    counts = Counter()
    for left, right in itertools.combinations(family, 2):
        counts[len(set(left) & set(right))] += 1
    return {str(key): value for key, value in sorted(counts.items())}


def ag24_geometry_signature(family: list[tuple[int, ...]], n: int) -> dict[str, Any]:
    line_classes = ag24_parallel_classes()
    class_hist = Counter(line_classes[tuple(block)] for block in family)
    point_hist = point_histogram(family, n)
    class_sizes = tuple(sorted(class_hist.values(), reverse=True))
    return {
        "classification": "finite_geometry_ag24_line_net",
        "parallel_class_size_signature": list(class_sizes),
        "parallel_class_histogram": {
            str(key): value for key, value in sorted(class_hist.items())
        },
        "point_multiplicity_histogram": point_hist,
        "max_point_multiplicity": max(int(key) for key, value in point_hist.items() if value),
        "pair_intersection_histogram": pair_intersection_histogram(family),
    }


def generic_signature(family: list[tuple[int, ...]], n: int) -> dict[str, Any]:
    return {
        "classification": "non_geometry_control_family",
        "point_multiplicity_histogram": point_histogram(family, n),
        "pair_intersection_histogram": pair_intersection_histogram(family),
    }


def stacked_rank(
    domain: list[int],
    family: list[tuple[int, ...]],
    t: int,
    slopes: list[int],
    p: int,
) -> int:
    return E3.rank_mod_p(E3.stacked_alignment_matrix(domain, family, t, slopes, p), p)


def subset_example(
    subset_indices: tuple[int, ...],
    family: list[tuple[int, ...]],
    rank: int,
    degree_deficiency: int,
    cert: dict[str, Any],
    signature: dict[str, Any],
) -> dict[str, Any]:
    return {
        "subset_indices": list(subset_indices),
        "family": [list(item) for item in family],
        "rank": rank,
        "degree_deficiency": degree_deficiency,
        "zero_restriction_locator_count": cert.get("zero_restriction_locator_count"),
        "signature": signature,
    }


def enumerate_subfamilies(
    *,
    name: str,
    family: list[tuple[int, ...]],
    n: int,
    j: int,
    t: int,
    p: int,
    modes: list[str],
    sizes: list[int],
    exhaustive_scope: str,
    signature_kind: str,
) -> dict[str, Any]:
    domain = E3.subgroup_domain(n, p)
    degree_cap = 2 * (j + t)
    rows = []
    unclassified = []
    for mode in modes:
        max_size = max(sizes)
        full_slopes = E3.slope_sequence(mode, max_size, p)
        for size in sizes:
            slopes = full_slopes[:size]
            rank_distribution: Counter[int] = Counter()
            loss_subsets = 0
            nondegenerate_loss_subsets = 0
            degenerate_loss_subsets = 0
            nondegenerate_classification: Counter[str] = Counter()
            nondegenerate_signature_types: Counter[Any] = Counter()
            first_nondegenerate = None
            first_degenerate = None

            for subset_indices in itertools.combinations(range(len(family)), size):
                subset = [family[idx] for idx in subset_indices]
                rank = stacked_rank(domain, subset, t, slopes, p)
                rank_distribution[rank] += 1
                degree_deficiency = min(size * t, degree_cap) - rank
                if degree_deficiency <= 0:
                    continue

                loss_subsets += 1
                cert = E3.nondegeneracy_certificate(domain, subset, t, slopes, p)
                if signature_kind == "ag24":
                    signature = ag24_geometry_signature(subset, n)
                else:
                    signature = generic_signature(subset, n)
                example = subset_example(
                    subset_indices,
                    subset,
                    rank,
                    degree_deficiency,
                    cert,
                    signature,
                )
                if cert["union_bound_certifies_nondegenerate_solution"]:
                    nondegenerate_loss_subsets += 1
                    classification = signature["classification"]
                    nondegenerate_classification[classification] += 1
                    signature_key = (
                        classification,
                        tuple(signature.get("parallel_class_size_signature", [])),
                        tuple(sorted(signature["point_multiplicity_histogram"].items())),
                    )
                    nondegenerate_signature_types[signature_key] += 1
                    if classification != "finite_geometry_ag24_line_net":
                        unclassified.append(example)
                    if first_nondegenerate is None:
                        first_nondegenerate = example
                else:
                    degenerate_loss_subsets += 1
                    if first_degenerate is None:
                        first_degenerate = example

            rows.append({
                "mode": mode,
                "size": size,
                "total_subsets": sum(rank_distribution.values()),
                "rank_distribution": {
                    str(key): value for key, value in sorted(rank_distribution.items())
                },
                "loss_subsets": loss_subsets,
                "nondegenerate_loss_subsets": nondegenerate_loss_subsets,
                "degenerate_loss_subsets": degenerate_loss_subsets,
                "nondegenerate_classification": {
                    key: value for key, value in sorted(nondegenerate_classification.items())
                },
                "nondegenerate_signature_type_count": len(nondegenerate_signature_types),
                "nondegenerate_signature_histogram": canonical_counter(
                    nondegenerate_signature_types
                ),
                "first_nondegenerate_example": first_nondegenerate,
                "first_degenerate_example": first_degenerate,
            })

    return {
        "name": name,
        "n": n,
        "j": j,
        "t": t,
        "A": n - j,
        "k": n - j - t,
        "prime": p,
        "family_size": len(family),
        "degree_cap": degree_cap,
        "modes": modes,
        "sizes": sizes,
        "exhaustive_scope": exhaustive_scope,
        "signature_kind": signature_kind,
        "rows": rows,
        "unclassified_nondegenerate_examples": unclassified[:5],
        "unclassified_nondegenerate_count": len(unclassified),
    }


def n32_control_family(case_name: str, prefix_size: int) -> tuple[list[tuple[int, ...]], int, int, int]:
    for case in E3.build_cases():
        if case["name"] == case_name:
            family = [tuple(sorted(item)) for item in case["family"][:prefix_size]]
            return family, case["n"], case["j"], case["t"]
    raise ValueError(case_name)


def build_report() -> dict[str, Any]:
    ag24 = enumerate_subfamilies(
        name="ag2_4_all_lines_exact_exception_census",
        family=E3.affine_plane_order4_lines(),
        n=16,
        j=4,
        t=2,
        p=E3.P,
        modes=["distinct_linear", "distinct_geometric"],
        sizes=[2, 3, 4, 5, 6, 7],
        exhaustive_scope=(
            "all subfamilies of all 20 AG(2,4) lines, in every size where "
            "the E3 packet observed below-cap loss or its first possible "
            "predecessors"
        ),
        signature_kind="ag24",
    )

    controls = []
    for case_name in ["greedy_32_j5_lambda1", "greedy_32_j6_lambda2"]:
        family, n, j, t = n32_control_family(case_name, 16)
        controls.append(enumerate_subfamilies(
            name=f"{case_name}_first16_control",
            family=family,
            n=n,
            j=j,
            t=t,
            p=E3.P,
            modes=["distinct_linear", "distinct_geometric"],
            sizes=[2, 3, 4, 5, 6],
            exhaustive_scope=(
                "all subfamilies of the first 16 deterministic E3 greedy "
                "blocks; this is a bounded non-geometry control, not a full "
                "n=32 support census"
            ),
            signature_kind="generic",
        ))

    all_cells = [ag24] + controls
    unclassified_count = sum(cell["unclassified_nondegenerate_count"] for cell in all_cells)
    ag24_nonzero = sum(
        row["nondegenerate_loss_subsets"]
        for row in ag24["rows"]
    )
    control_nonzero = sum(
        row["nondegenerate_loss_subsets"]
        for cell in controls
        for row in cell["rows"]
    )
    source = Path(__file__).read_text()
    return {
        "title": "E13 spread-exception finite-geometry census",
        "status": "EXPERIMENTAL / AUDIT",
        "dag_nodes": ["spread_exception_classification", "spread_regime_bound"],
        "fable_evidence_item": "E13",
        "question": (
            "In replayable small spread cells, do below-cap nondegenerate "
            "rank-loss exceptions embed in the finite-geometry AG/net class, "
            "or is there an unclassified non-geometric exception?"
        ),
        "method": (
            "Enumerate every subfamily in the AG(2,4) line-net cell at sizes "
            "2..7 and classify every below-cap nondegenerate loss by incidence "
            "signature.  Then run bounded n=32 non-geometry controls on the "
            "first 16 deterministic E3 greedy blocks."
        ),
        "non_claims": [
            "This is not a proof of spread_regime_bound.",
            "This does not enumerate all support families for every n in 16..32.",
            "The n=32 controls are bounded falsification cells, not exhaustive n=32 censuses.",
        ],
        "cells": all_cells,
        "ag24_nondegenerate_exception_count": ag24_nonzero,
        "n32_control_nondegenerate_exception_count": control_nonzero,
        "unclassified_nondegenerate_exception_count": unclassified_count,
        "overall_interpretation": (
            "UNCLASSIFIED_NON_GEOMETRY_EXCEPTION_FOUND"
            if unclassified_count
            else "AG24_EXCEPTIONS_CLASSIFIED_AND_N32_CONTROLS_CLEAN"
            if ag24_nonzero and control_nonzero == 0
            else "NO_NONDEGENERATE_EXCEPTIONS_IN_TESTED_CELLS"
        ),
        "script_sha256": sha256_text(source),
    }


def assert_report_invariants(report: dict[str, Any]) -> None:
    if report["overall_interpretation"] not in {
        "AG24_EXCEPTIONS_CLASSIFIED_AND_N32_CONTROLS_CLEAN",
        "UNCLASSIFIED_NON_GEOMETRY_EXCEPTION_FOUND",
    }:
        raise AssertionError(report["overall_interpretation"])
    if report["ag24_nondegenerate_exception_count"] != 373:
        raise AssertionError(report["ag24_nondegenerate_exception_count"])
    if report["unclassified_nondegenerate_exception_count"] != report["n32_control_nondegenerate_exception_count"]:
        raise AssertionError((
            report["unclassified_nondegenerate_exception_count"],
            report["n32_control_nondegenerate_exception_count"],
        ))
    ag24 = report["cells"][0]
    expected = {
        ("distinct_linear", 6): (435, 195, 240, 18),
        ("distinct_linear", 7): (2, 2, 0, 1),
        ("distinct_geometric", 6): (416, 176, 240, 18),
        ("distinct_geometric", 7): (0, 0, 0, 0),
    }
    for row in ag24["rows"]:
        key = (row["mode"], row["size"])
        if key in expected:
            loss, nondeg, deg, sigs = expected[key]
            if (
                row["loss_subsets"],
                row["nondegenerate_loss_subsets"],
                row["degenerate_loss_subsets"],
                row["nondegenerate_signature_type_count"],
            ) != (loss, nondeg, deg, sigs):
                raise AssertionError((key, row))
        elif row["loss_subsets"] != 0:
            raise AssertionError((key, row["loss_subsets"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
    parser.add_argument("--check", type=Path, help="recompute and compare with an existing artifact")
    args = parser.parse_args()

    report = build_report()
    assert_report_invariants(report)

    print(f"overall: {report['overall_interpretation']}")
    print(f"AG(2,4) nondegenerate exceptions: {report['ag24_nondegenerate_exception_count']}")
    print(f"n=32 control nondegenerate exceptions: {report['n32_control_nondegenerate_exception_count']}")
    for cell in report["cells"]:
        print(
            "{name}: unclassified={unclassified}, family_size={size}, sizes={sizes}".format(
                name=cell["name"],
                unclassified=cell["unclassified_nondegenerate_count"],
                size=cell["family_size"],
                sizes=cell["sizes"],
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
