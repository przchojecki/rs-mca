#!/usr/bin/env python3
"""E15 worst-word sunflower challenge.

This is an EXPERIMENTAL / AUDIT verifier for the list-side E15 work order.  It
tests whether structured sunflower words beat the planted sunflower count in
small replayable cells.

The n=16 cells are exhaustive over all agreement sets of size s.  The n=32 and
n=64 cells are structured scans: bounded-excess full-petal CRT candidates and
minimal-defect two-petal pencil candidates.  They are evidence only, not a
worst-case list-size theorem.

Run:
  python3 experimental/scripts/verify_e15_worst_word_challenge.py
  python3 experimental/scripts/verify_e15_worst_word_challenge.py --emit
  python3 experimental/scripts/verify_e15_worst_word_challenge.py --check experimental/data/certificates/l1-petal-fixed-excess/e15_worst_word_challenge.json
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
    "experimental/data/certificates/l1-petal-fixed-excess/"
    "e15_worst_word_challenge.json"
)
P = 193


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def inv_mod(x: int, p: int = P) -> int:
    return pow(x % p, -1, p)


def trim(poly: list[int], p: int = P) -> tuple[int, ...]:
    out = [x % p for x in poly]
    while out and out[-1] == 0:
        out.pop()
    return tuple(out)


def poly_mul(left: tuple[int, ...], right: tuple[int, ...], p: int = P) -> tuple[int, ...]:
    out = [0] * (len(left) + len(right) - 1)
    for i, ai in enumerate(left):
        for j, bj in enumerate(right):
            out[i + j] = (out[i + j] + ai * bj) % p
    return trim(out, p)


def poly_add(left: tuple[int, ...], right: tuple[int, ...], p: int = P) -> tuple[int, ...]:
    size = max(len(left), len(right))
    out = [0] * size
    for idx in range(size):
        out[idx] = (
            (left[idx] if idx < len(left) else 0)
            + (right[idx] if idx < len(right) else 0)
        ) % p
    return trim(out, p)


def poly_scale(poly: tuple[int, ...], scalar: int, p: int = P) -> tuple[int, ...]:
    return trim([scalar * coeff for coeff in poly], p)


def poly_eval(poly: tuple[int, ...], x: int, p: int = P) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x + coeff) % p
    return value


def interpolate(points: list[tuple[int, int]], p: int = P) -> tuple[int, ...]:
    poly: tuple[int, ...] = ()
    for i, (x_i, y_i) in enumerate(points):
        basis: tuple[int, ...] = (1,)
        denom = 1
        for j, (x_j, _) in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, ((-x_j) % p, 1), p)
            denom = (denom * (x_i - x_j)) % p
        term = poly_scale(basis, y_i * inv_mod(denom, p), p)
        poly = poly_add(poly, term, p)
    return poly


def polynomial_through(indices: list[int], domain: list[int], values: list[int], k: int) -> tuple[int, ...] | None:
    if len(indices) < k:
        raise ValueError("need at least k interpolation points")
    base = indices[:k]
    poly = interpolate([(domain[idx], values[idx]) for idx in base], P)
    if len(poly) > k:
        return None
    if all(poly_eval(poly, domain[idx], P) == values[idx] % P for idx in indices):
        return poly
    return None


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
    raise ValueError("no primitive root")


def subgroup_domain(n: int, p: int = P) -> list[int]:
    if (p - 1) % n:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    generator = pow(primitive_root(p), (p - 1) // n, p)
    domain = [pow(generator, idx, p) for idx in range(n)]
    if len(set(domain)) != n:
        raise AssertionError("wrong subgroup order")
    return domain


def locator(roots: list[int], p: int = P) -> tuple[int, ...]:
    poly: tuple[int, ...] = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % p, 1), p)
    return poly


def cyclic_order(n: int, step: int) -> list[int]:
    if not 0 <= step < n:
        raise ValueError(step)
    if step == 0:
        return list(range(n))
    if __import__("math").gcd(step, n) != 1:
        raise ValueError("step must be coprime to n")
    return [(step * idx) % n for idx in range(n)]


def shuffled_order(n: int, seed: int) -> list[int]:
    out = list(range(n))
    random.Random(seed).shuffle(out)
    return out


def layout_order(n: int, mode: str) -> list[int]:
    if mode.startswith("cyclic_step_"):
        return cyclic_order(n, int(mode.rsplit("_", 1)[1]))
    if mode.startswith("shuffle_"):
        return shuffled_order(n, int(mode.rsplit("_", 1)[1]))
    raise ValueError(mode)


def scalar_sequence(count: int, mode: str, p: int = P) -> list[int]:
    if mode == "linear":
        return list(range(1, count + 1))
    if mode == "geometric":
        out = []
        value = 1
        for _ in range(count):
            out.append(value)
            value = (value * 5) % p
        if len(set(out)) != count:
            raise AssertionError("geometric scalars repeated")
        return out
    raise ValueError(mode)


def sunflower_word(n: int, k: int, sigma: int, layout: str, scalar_mode: str) -> dict[str, Any]:
    domain = subgroup_domain(n, P)
    ell = sigma + 1
    order = layout_order(n, layout)
    core = sorted(order[: k - 1])
    rest = order[k - 1 :]
    petal_count = len(rest) // ell
    petals = [sorted(rest[i * ell : (i + 1) * ell]) for i in range(petal_count)]
    background = sorted(rest[petal_count * ell :])
    core_locator = locator([domain[idx] for idx in core], P)
    scalars = scalar_sequence(petal_count, scalar_mode, P)
    values = [0] * n
    for scalar, petal in zip(scalars, petals):
        for idx in petal:
            values[idx] = scalar * poly_eval(core_locator, domain[idx], P) % P
    planted = {
        poly_scale(core_locator, scalar, P)
        for scalar in scalars
    }
    return {
        "n": n,
        "k": k,
        "sigma": sigma,
        "s": k + sigma,
        "ell": ell,
        "layout": layout,
        "scalar_mode": scalar_mode,
        "domain": domain,
        "core": core,
        "petals": petals,
        "background": background,
        "values": values,
        "core_locator": core_locator,
        "scalars": scalars,
        "planted_polynomials": planted,
    }


def agreement_set(poly: tuple[int, ...], word: dict[str, Any]) -> tuple[int, ...]:
    return tuple(
        idx
        for idx, x in enumerate(word["domain"])
        if poly_eval(poly, x, P) == word["values"][idx] % P
    )


def pattern(poly: tuple[int, ...], word: dict[str, Any]) -> dict[str, Any]:
    agreement = set(agreement_set(poly, word))
    return {
        "is_planted": poly in word["planted_polynomials"],
        "agreement": len(agreement),
        "core_agreement": len(agreement & set(word["core"])),
        "background_agreement": len(agreement & set(word["background"])),
        "petal_agreements": [
            len(agreement & set(petal)) for petal in word["petals"]
        ],
    }


def classify_pattern(record: dict[str, Any], ell: int) -> str:
    if record["is_planted"]:
        return "planted"
    petal_counts = record["petal_agreements"]
    full = sum(1 for count in petal_counts if count == ell)
    touched = sum(1 for count in petal_counts if count)
    if full >= 2 and full == touched:
        return "full_petal"
    if touched >= 2:
        return "mixed_petal"
    if touched == 1:
        return "one_petal_nonplanted"
    return "background_or_core_only"


EXACT_N16_PARAMETER_CELLS = [
    # Toy official rates k/n in {1/16, 1/8, 1/4, 1/2}, with small slacks.
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 4),
    (8, 1),
    (8, 2),
    (8, 3),
]


def exact_n16_cell(k: int, sigma: int, layout: str, scalar_mode: str) -> dict[str, Any]:
    word = sunflower_word(16, k, sigma, layout, scalar_mode)
    found: dict[tuple[int, ...], dict[str, Any]] = {}
    for indices in itertools.combinations(range(word["n"]), word["s"]):
        poly = polynomial_through(list(indices), word["domain"], word["values"], word["k"])
        if poly is None:
            continue
        rec = pattern(poly, word)
        if rec["agreement"] >= word["s"]:
            found[poly] = rec
    class_counts = Counter(classify_pattern(rec, word["ell"]) for rec in found.values())
    nonplanted = sum(1 for poly in found if poly not in word["planted_polynomials"])
    first_nonplanted = []
    for poly, rec in found.items():
        if poly in word["planted_polynomials"]:
            continue
        first_nonplanted.append({
            "polynomial_coefficients": list(poly),
            "class": classify_pattern(rec, word["ell"]),
            **rec,
        })
        if len(first_nonplanted) >= 5:
            break
    return {
        "kind": "exact_all_agreement_sets",
        "n": word["n"],
        "k": word["k"],
        "sigma": word["sigma"],
        "s": word["s"],
        "layout": layout,
        "scalar_mode": scalar_mode,
        "petal_count_M": len(word["petals"]),
        "background_size": len(word["background"]),
        "agreement_sets_checked": __import__("math").comb(word["n"], word["s"]),
        "list_size": len(found),
        "planted_count": len(word["planted_polynomials"]),
        "nonplanted_count": nonplanted,
        "beats_planted": len(found) > len(word["planted_polynomials"]),
        "class_counts": dict(sorted(class_counts.items())),
        "first_nonplanted_examples": first_nonplanted,
    }


def structured_full_petal_scan(
    n: int,
    k: int,
    sigma: int,
    layout: str,
    scalar_mode: str,
    max_excess: int,
) -> dict[str, Any]:
    word = sunflower_word(n, k, sigma, layout, scalar_mode)
    core = word["core"]
    petals = word["petals"]
    ell = word["ell"]
    found: dict[tuple[int, ...], dict[str, Any]] = {}
    candidates = 0
    for excess in range(max_excess + 1):
        d = ell + excess
        for touched_count in range(2, len(petals) + 1):
            if d > (touched_count - 1) * ell:
                continue
            for touched in itertools.combinations(range(len(petals)), touched_count):
                touched_points = sorted(
                    point for petal_idx in touched for point in petals[petal_idx]
                )
                for missed_core in itertools.combinations(core, d):
                    agreement = sorted((set(core) - set(missed_core)) | set(touched_points))
                    if len(agreement) < word["s"]:
                        continue
                    candidates += 1
                    poly = polynomial_through(agreement, word["domain"], word["values"], word["k"])
                    if poly is None or poly in word["planted_polynomials"]:
                        continue
                    rec = pattern(poly, word)
                    if rec["agreement"] >= word["s"]:
                        found[poly] = {**rec, "first_source": {
                            "excess": excess,
                            "core_defect": d,
                            "touched_petals": list(touched),
                        }}
    class_counts = Counter(classify_pattern(rec, ell) for rec in found.values())
    return {
        "kind": "structured_full_petal_bounded_excess_scan",
        "n": n,
        "k": k,
        "sigma": sigma,
        "s": word["s"],
        "layout": layout,
        "scalar_mode": scalar_mode,
        "petal_count_M": len(petals),
        "background_size": len(word["background"]),
        "max_excess": max_excess,
        "candidates_checked": candidates,
        "unique_nonplanted_candidates": len(found),
        "planted_count": len(word["planted_polynomials"]),
        "beats_planted": len(found) + len(word["planted_polynomials"]) > len(word["planted_polynomials"]),
        "class_counts": dict(sorted(class_counts.items())),
        "first_examples": list(found.values())[:5],
    }


def two_petal_pencil_scan(
    n: int,
    k: int,
    sigma: int,
    layout: str,
    scalar_mode: str,
) -> dict[str, Any]:
    word = sunflower_word(n, k, sigma, layout, scalar_mode)
    domain = word["domain"]
    ell = word["ell"]
    petal_locators = [
        locator([domain[idx] for idx in petal], P) for petal in word["petals"]
    ]
    missed_core_locators = [
        (
            missed_core,
            locator([domain[idx] for idx in missed_core], P),
        )
        for missed_core in itertools.combinations(word["core"], ell)
    ]
    solutions = []
    checked = 0
    for i, j in itertools.combinations(range(len(word["petals"])), 2):
        left = petal_locators[i]
        right = petal_locators[j]
        pencil = {
            poly_add(poly_scale(left, 1 + beta, P), poly_scale(right, -beta, P), P): beta
            for beta in range(P)
        }
        for missed_core, ld in missed_core_locators:
            checked += 1
            if ld in pencil:
                solutions.append({
                    "petal_pair": [i, j],
                    "missed_core": list(missed_core),
                    "beta": pencil[ld],
                })
    return {
        "kind": "minimal_defect_two_petal_pencil_scan",
        "n": n,
        "k": k,
        "sigma": sigma,
        "s": word["s"],
        "layout": layout,
        "scalar_mode": scalar_mode,
        "petal_count_M": len(word["petals"]),
        "background_size": len(word["background"]),
        "candidate_pairs_checked": checked,
        "nonplanted_pencil_solutions": len(solutions),
        "planted_count": len(word["planted_polynomials"]),
        "beats_planted": bool(solutions),
        "first_solutions": solutions[:5],
    }


def build_report() -> dict[str, Any]:
    exact_layouts = ["cyclic_step_1", "shuffle_1501"]
    scalar_modes = ["linear", "geometric"]
    exact_cells = [
        exact_n16_cell(k, sigma, layout, scalar_mode)
        for k, sigma in EXACT_N16_PARAMETER_CELLS
        for layout in exact_layouts
        for scalar_mode in scalar_modes
    ]
    n32_cells = [
        structured_full_petal_scan(32, 16, 3, layout, scalar_mode, max_excess=2)
        for layout in ["cyclic_step_1", "cyclic_step_3", "shuffle_3201"]
        for scalar_mode in scalar_modes
    ]
    n64_cells = [
        two_petal_pencil_scan(64, 32, 3, layout, scalar_mode)
        for layout in ["cyclic_step_1", "cyclic_step_3", "shuffle_6401"]
        for scalar_mode in scalar_modes
    ]
    cells = exact_cells + n32_cells + n64_cells
    beating_cells = [cell for cell in cells if cell["beats_planted"]]
    nonplanted_hits = [
        cell for cell in cells
        if cell.get("nonplanted_count", 0)
        or cell.get("unique_nonplanted_candidates", 0)
        or cell.get("nonplanted_pencil_solutions", 0)
    ]
    exact_beating_cells = [cell for cell in exact_cells if cell["beats_planted"]]
    exact_sigma_one_beating_cells = [
        cell for cell in exact_beating_cells if cell["sigma"] == 1
    ]
    exact_sigma_ge_two_beating_cells = [
        cell for cell in exact_beating_cells if cell["sigma"] >= 2
    ]
    source = Path(__file__).read_text()
    return {
        "schema": "e15-worst-word-challenge-v1",
        "status": "EXPERIMENTAL_AUDIT",
        "roadmap_task": "E15 / worst-word challenge / QL.2",
        "question": (
            "Do structured sunflower words in small replayable cells beat the "
            "planted sunflower list at matched radius?"
        ),
        "method": {
            "exact_cells": (
                "n=16: for toy official rates k in {1,2,4,8} and selected "
                "small sigma, enumerate every agreement subset of size s=k+sigma "
                "and deduplicate degree-<k codewords."
            ),
            "n32_cells": (
                "n=32,k=16,sigma=3: scan all full-petal candidates with "
                "cofactor excess d-ell<=2 for selected adversarial layouts."
            ),
            "n64_cells": (
                "n=64,k=32,sigma=3: scan minimal-defect two-petal locator "
                "pencils for selected adversarial layouts."
            ),
        },
        "field": f"F_{P}",
        "cells": cells,
        "summary": {
            "cell_count": len(cells),
            "beating_cell_count": len(beating_cells),
            "nonplanted_hit_cell_count": len(nonplanted_hits),
            "total_exact_n16_list_size": sum(cell["list_size"] for cell in exact_cells),
            "total_exact_n16_nonplanted_count": sum(
                cell["nonplanted_count"] for cell in exact_cells
            ),
            "exact_n16_beating_cell_count": len(exact_beating_cells),
            "exact_n16_sigma_one_beating_cell_count": len(exact_sigma_one_beating_cells),
            "exact_n16_sigma_ge_two_beating_cell_count": len(exact_sigma_ge_two_beating_cells),
            "total_exact_n16_agreement_sets_checked": sum(
                cell["agreement_sets_checked"] for cell in exact_cells
            ),
            "total_n32_candidates_checked": sum(cell["candidates_checked"] for cell in n32_cells),
            "total_n64_pencil_candidates_checked": sum(cell["candidate_pairs_checked"] for cell in n64_cells),
        },
        "overall_interpretation": (
            "NO_STRUCTURED_CHALLENGER_FOUND_IN_BOUNDED_CELLS"
            if not beating_cells and not nonplanted_hits
            else "STRUCTURED_NONPLANTED_CHALLENGER_FOUND"
        ),
        "non_claims": [
            "This is not a proof of the L1 safe-side theorem.",
            "The n=32 and n=64 scans are structured challenger cells, not exhaustive list decoding.",
            "A clean result here only grounds the worst_word_planted heuristic in these cells.",
        ],
        "script_sha256": sha256_text(source),
    }


def assert_invariants(report: dict[str, Any]) -> None:
    if report["overall_interpretation"] != "STRUCTURED_NONPLANTED_CHALLENGER_FOUND":
        raise AssertionError(report["overall_interpretation"])
    if report["summary"]["cell_count"] != 72:
        raise AssertionError(report["summary"]["cell_count"])
    if report["summary"]["beating_cell_count"] != 12:
        raise AssertionError(report["summary"]["beating_cell_count"])
    if report["summary"]["nonplanted_hit_cell_count"] != 12:
        raise AssertionError(report["summary"]["nonplanted_hit_cell_count"])
    if report["summary"]["exact_n16_sigma_one_beating_cell_count"] != 12:
        raise AssertionError(report["summary"])
    if report["summary"]["exact_n16_sigma_ge_two_beating_cell_count"] != 0:
        raise AssertionError(report["summary"])
    for cell in report["cells"]:
        if cell["kind"] == "exact_all_agreement_sets":
            if cell["sigma"] >= 2 and cell["list_size"] != cell["planted_count"]:
                raise AssertionError(cell)
            if cell["sigma"] == 1 and cell["beats_planted"] != (cell["k"] in {2, 4, 8}):
                raise AssertionError(cell)
        if cell["kind"] == "structured_full_petal_bounded_excess_scan":
            if cell["unique_nonplanted_candidates"] != 0:
                raise AssertionError(cell)
        if cell["kind"] == "minimal_defect_two_petal_pencil_scan":
            if cell["nonplanted_pencil_solutions"] != 0:
                raise AssertionError(cell)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
    parser.add_argument("--check", type=Path, help="recompute and compare with an existing artifact")
    args = parser.parse_args()

    report = build_report()
    assert_invariants(report)
    print(f"overall: {report['overall_interpretation']}")
    print(f"cells: {report['summary']['cell_count']}")
    print(f"n32 candidates checked: {report['summary']['total_n32_candidates_checked']}")
    print(f"n64 pencil candidates checked: {report['summary']['total_n64_pencil_candidates_checked']}")

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
