#!/usr/bin/env python3
"""Exact E4 auxiliary-list evidence for the mixed-petal wide regime.

This verifier targets Fable's E4 evidence question:

    In the many-petal, sub-Johnson sunflower regime, do the auxiliary
    pieced-word lists stay small, or do they show amplification?

It does not enumerate full received words.  It enumerates the lower-dimensional
auxiliary problem isolated in
experimental/notes/l1/l1_full_list_quotient_proof_program.md Lemma 2:

    degree <= d polynomials W agreeing with
        tau_D(x) = c_i L_D(x) on x in T_i
    on at least a = d + ell petal points,

where ell = sigma + 1 is the petal size and R_P is set to 0.  The tested
family uses subgroup petals in F_109^*, ell=3, d=5, and petal counts crossing
the proof-program Johnson cutoff M_J = (d+ell)^2/(d ell).

Run:
    python3 experimental/scripts/verify_l1_petal_auxiliary_wide_regime.py
    python3 experimental/scripts/verify_l1_petal_auxiliary_wide_regime.py --emit
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scan_l1_full_list_quotient_conjecture import (  # noqa: E402
    eval_poly,
    interpolate_polynomial,
    multiply_by_linear,
    primitive_root,
    trim_poly,
)


ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "certificates"
    / "l1-petal-auxiliary-wide-regime"
    / "petal_auxiliary_wide_regime.json"
)


@dataclass(frozen=True)
class CaseSpec:
    label: str
    p: int
    ell: int
    d: int
    m_values: tuple[int, ...]
    scalar_schedule: str


def subgroup_domain(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    root = pow(primitive_root(p), (p - 1) // n, p)
    out: list[int] = []
    value = 1
    for _ in range(n):
        out.append(value)
        value = (value * root) % p
    if value != 1 or len(set(out)) != n:
        raise ValueError("subgroup generator has wrong order")
    return out


def locator(roots: Iterable[int], p: int) -> tuple[int, ...]:
    poly: tuple[int, ...] = (1,)
    for root in roots:
        poly = multiply_by_linear(poly, root, p)
    return trim_poly(poly)


def scalar_values(schedule: str, m: int, p: int) -> list[int]:
    if schedule == "linear":
        return list(range(1, m + 1))
    if schedule == "geometric":
        return [pow(2, index, p) for index in range(m)]
    raise ValueError(f"unknown scalar schedule: {schedule}")


def choose_defect_roots(domain: set[int], d: int, p: int) -> list[int]:
    roots: list[int] = []
    for value in range(2, p):
        if value not in domain:
            roots.append(value)
            if len(roots) == d:
                return roots
    raise ValueError("not enough defect roots outside the petal domain")


def petal_profile(
    hit_positions: list[int], petal_index: list[int], m: int, ell: int
) -> dict[str, object]:
    per_petal = [0] * m
    for position in hit_positions:
        per_petal[petal_index[position]] += 1
    positive = sorted((count for count in per_petal if count), reverse=True)
    return {
        "agreement": len(hit_positions),
        "touched_petals": len(positive),
        "full_petals": sum(1 for count in positive if count == ell),
        "max_petal_hits": max(positive, default=0),
        "positive_petal_hits_desc": positive,
    }


def enumerate_auxiliary_list(spec: CaseSpec, m: int) -> dict[str, object]:
    p, ell, d = spec.p, spec.ell, spec.d
    n = m * ell
    threshold = d + ell
    domain = subgroup_domain(p, n)
    petals = [domain[index * ell : (index + 1) * ell] for index in range(m)]
    roots = choose_defect_roots(set(domain), d, p)
    loc_d = locator(roots, p)
    scalars = scalar_values(spec.scalar_schedule, m, p)

    target: list[int] = []
    petal_index: list[int] = []
    for index, petal in enumerate(petals):
        scalar = scalars[index]
        for x_value in petal:
            target.append((scalar * eval_poly(loc_d, x_value, p)) % p)
            petal_index.append(index)

    seen: dict[tuple[int, ...], int] = {}
    listed: list[dict[str, object]] = []
    profile_histogram: Counter[str] = Counter()

    for support in itertools.combinations(range(n), d + 1):
        coeffs = trim_poly(
            interpolate_polynomial(
                [domain[position] for position in support],
                [target[position] for position in support],
                p,
            )
        )
        if coeffs in seen:
            continue

        values = [eval_poly(coeffs, x_value, p) for x_value in domain]
        hits = [position for position, value in enumerate(values) if value == target[position]]
        seen[coeffs] = len(hits)
        if len(hits) < threshold:
            continue

        profile = petal_profile(hits, petal_index, m, ell)
        key = ",".join(str(value) for value in profile["positive_petal_hits_desc"])
        profile_histogram[key] += 1
        listed.append(
            {
                "coefficients": list(coeffs),
                "agreement": len(hits),
                "profile": profile,
            }
        )

    listed.sort(
        key=lambda item: (
            -int(item["agreement"]),
            item["profile"]["positive_petal_hits_desc"],
            item["coefficients"],
        )
    )

    johnson_margin = threshold * threshold - n * d
    return {
        "label": spec.label,
        "p": p,
        "ell": ell,
        "sigma": ell - 1,
        "d": d,
        "m_petals": m,
        "n_petal_points": n,
        "scalar_schedule": spec.scalar_schedule,
        "defect_roots": roots,
        "agreement_threshold": threshold,
        "johnson_m_cutoff": str(Fraction(threshold * threshold, d * ell)),
        "johnson_margin": johnson_margin,
        "johnson_covered": johnson_margin > 0,
        "support_subsets_checked": math.comb(n, d + 1),
        "unique_degree_le_d_candidates_seen": len(seen),
        "auxiliary_list_size": len(listed),
        "max_agreement": max((int(item["agreement"]) for item in listed), default=0),
        "profile_histogram": dict(sorted(profile_histogram.items())),
        "top_witnesses": listed[:8],
    }


def run(quick: bool = False) -> dict[str, object]:
    specs = [
        CaseSpec(
            label="F109_subgroup_ell3_d5_linear",
            p=109,
            ell=3,
            d=5,
            m_values=(3, 4, 6, 9) if quick else (3, 4, 6, 9, 12),
            scalar_schedule="linear",
        ),
        CaseSpec(
            label="F109_subgroup_ell3_d5_geometric",
            p=109,
            ell=3,
            d=5,
            m_values=(3, 4, 6, 9),
            scalar_schedule="geometric",
        ),
    ]
    cases = [
        enumerate_auxiliary_list(spec, m)
        for spec in specs
        for m in spec.m_values
    ]

    wide_cases = [case for case in cases if not case["johnson_covered"]]
    nonzero_wide = [case for case in wide_cases if case["auxiliary_list_size"]]
    max_size = max((int(case["auxiliary_list_size"]) for case in cases), default=0)
    max_n = max((int(case["n_petal_points"]) for case in cases), default=1)
    status = (
        "NO_SUPERPOLY_SIGNAL_IN_EXACT_TOY_WINDOW"
        if max_size <= max_n**3
        else "AMPLIFICATION_ALERT"
    )
    return {
        "status": status,
        "target": "E4 pma_wide_residual",
        "model": "auxiliary pieced-word list for sunflower petals",
        "pre_registered_search_space": {
            "field": "F_109",
            "petal_domain": "multiplicative subgroup, chunked into consecutive exponent petals",
            "ell": 3,
            "d": 5,
            "agreement_threshold": "a=d+ell=8 (R_P=0 proof-program convention)",
            "petal_counts": "linear: 3,4,6,9,12 unless --quick; geometric: 3,4,6,9",
            "johnson_cutoff_M": str(Fraction(64, 15)),
        },
        "interpretation_table": {
            "bounded_or_poly": (
                "pma_wide_residual prior up; data supports attacking a "
                "correlated-target/descend proof rather than revising ImgFib"
            ),
            "superpoly_growth": (
                "COUNTEREXAMPLE track; isolate the sunflower mechanism and "
                "revise the L1/image-fiber residual"
            ),
        },
        "wide_cases_with_nonzero_auxiliary_list": len(nonzero_wide),
        "max_auxiliary_list_size": max_size,
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quick", action="store_true", help="skip the M=12 linear row")
    parser.add_argument("--emit", action="store_true", help=f"write {ARTIFACT}")
    args = parser.parse_args()

    output = run(quick=args.quick)

    print(f"E4 auxiliary-list evidence status: {output['status']}")
    for case in output["cases"]:
        print(
            "  "
            f"{case['label']} M={case['m_petals']} "
            f"n={case['n_petal_points']} "
            f"johnson_margin={case['johnson_margin']} "
            f"list={case['auxiliary_list_size']} "
            f"max_agreement={case['max_agreement']}"
        )

    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(Path.cwd())}")

    raise SystemExit(0)


if __name__ == "__main__":
    main()
