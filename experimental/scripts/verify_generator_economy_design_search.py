#!/usr/bin/env python3
"""E12 generator-economy toy design search.

This is an EXPERIMENTAL evidence verifier for the Row-C / far-pair lane.  It
does not prove a density theorem and does not use locator-fiber counts.

Model:
* represent an l-sum center by an l-subset S of Z/NZ;
* a pair difference is the coefficient vector 1_S - 1_T in Z[zeta_N];
* two differences use the same template generator if they differ by a
  cyclotomic unit/sign, i.e. by a cyclic shift and multiplication by +/-1.

Thus the "generator count" below is the number of unit/sign difference
templates needed to certify all pairs if each template receives its own norm
check.  This is the conservative template-generator baseline; it does not try
to compress templates through a multiplicative semigroup.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from functools import lru_cache
from math import comb
from pathlib import Path
from typing import Any


EXACT_CASES = ((16, 8), (16, 9))
SAMPLED_CASES = ((32, 16), (32, 17))
SAMPLED_REP_COUNT = 512
TEMPLATE_BUDGETS = (8, 16, 32, 64, 128, 256)
OUTPUT = Path(
    "experimental/data/certificates/generator-economy-design-search/"
    "generator_economy_design_search.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bitmask(combo: tuple[int, ...] | list[int]) -> int:
    mask = 0
    for value in combo:
        mask |= 1 << value
    return mask


def rotate_mask(mask: int, n: int, shift: int) -> int:
    shift %= n
    if shift == 0:
        return mask
    full = (1 << n) - 1
    return ((mask << shift) & full) | (mask >> (n - shift))


@lru_cache(maxsize=None)
def orbit_masks(mask: int, n: int) -> tuple[int, ...]:
    return tuple(sorted({rotate_mask(mask, n, shift) for shift in range(n)}))


def canonical_mask(mask: int, n: int) -> int:
    return orbit_masks(mask, n)[0]


def mask_to_set(mask: int, n: int) -> list[int]:
    return [idx for idx in range(n) if (mask >> idx) & 1]


def canonical_difference_template(left: int, right: int, n: int) -> tuple[int, ...]:
    diff = [
        ((left >> idx) & 1) - ((right >> idx) & 1)
        for idx in range(n)
    ]
    best: tuple[int, ...] | None = None
    for sign in (1, -1):
        signed = [sign * entry for entry in diff]
        for shift in range(n):
            candidate = tuple(signed[(idx - shift) % n] for idx in range(n))
            if best is None or candidate < best:
                best = candidate
    assert best is not None
    return best


def exact_orbit_representatives(n: int, ell: int) -> list[int]:
    return sorted({
        canonical_mask(bitmask(combo), n)
        for combo in itertools.combinations(range(n), ell)
    })


def sampled_orbit_representatives(n: int, ell: int, count: int, seed: int) -> list[int]:
    rng = random.Random(seed)
    reps: set[int] = set()

    structured: list[tuple[int, ...]] = [tuple(range(ell))]
    if 2 * ell <= n:
        structured.append(tuple(range(0, 2 * ell, 2)))
    for step in range(1, n):
        candidate = tuple(sorted({(idx * step) % n for idx in range(ell)}))
        if len(candidate) == ell:
            structured.append(candidate)
    for candidate in structured:
        reps.add(canonical_mask(bitmask(candidate), n))

    while len(reps) < count:
        reps.add(canonical_mask(bitmask(rng.sample(range(n), ell)), n))
    return sorted(reps)


def orbit_representatives(n: int, ell: int, sampled: bool) -> list[int]:
    if sampled:
        return sampled_orbit_representatives(
            n, ell, SAMPLED_REP_COUNT, seed=2026070312 + n + ell
        )
    return exact_orbit_representatives(n, ell)


@lru_cache(maxsize=None)
def intra_orbit_templates(rep: int, n: int) -> frozenset[tuple[int, ...]]:
    orbit = orbit_masks(rep, n)
    templates = {
        canonical_difference_template(rep, other, n)
        for other in orbit
        if other != rep
    }
    return frozenset(templates)


@lru_cache(maxsize=None)
def cross_orbit_templates(rep_a: int, rep_b: int, n: int) -> frozenset[tuple[int, ...]]:
    if rep_a > rep_b:
        rep_a, rep_b = rep_b, rep_a
    if rep_a == rep_b:
        return intra_orbit_templates(rep_a, n)
    templates = {
        canonical_difference_template(rep_a, other, n)
        for other in orbit_masks(rep_b, n)
    }
    return frozenset(templates)


def singleton_germ(n: int) -> dict[str, Any]:
    rep = 1
    return {
        "ell": 1,
        "orbit_size": len(orbit_masks(rep, n)),
        "template_generators": len(intra_orbit_templates(rep, n)),
        "expected_template_generators": n // 2,
        "status": "PASS" if len(intra_orbit_templates(rep, n)) == n // 2 else "FAIL",
    }


def best_single_orbits(reps: list[int], n: int, limit: int = 5) -> list[dict[str, Any]]:
    rows = []
    for rep in reps:
        rows.append({
            "representative": mask_to_set(rep, n),
            "orbit_size": len(orbit_masks(rep, n)),
            "template_generators": len(intra_orbit_templates(rep, n)),
        })
    rows.sort(key=lambda row: (-row["orbit_size"], row["template_generators"], row["representative"]))
    return rows[:limit]


def greedy_orbit_union(reps: list[int], n: int, budget: int) -> dict[str, Any]:
    chosen: list[int] = []
    templates: set[tuple[int, ...]] = set()
    while True:
        best: tuple[tuple[float, int, int, int], int, set[tuple[int, ...]]] | None = None
        for rep in reps:
            if rep in chosen:
                continue
            new_templates = set(intra_orbit_templates(rep, n))
            for chosen_rep in chosen:
                new_templates |= set(cross_orbit_templates(rep, chosen_rep, n))
            new_templates -= templates
            if len(templates) + len(new_templates) > budget:
                continue
            orbit_size = len(orbit_masks(rep, n))
            # Prefer large size per new template, then large orbits, then fewer
            # new templates.  The final negative rep is just a deterministic tie-break.
            denominator = max(1, len(new_templates))
            score = (
                orbit_size / denominator,
                orbit_size,
                -len(new_templates),
                -rep,
            )
            if best is None or score > best[0]:
                best = (score, rep, new_templates)
        if best is None:
            break
        _score, rep, new_templates = best
        chosen.append(rep)
        templates |= new_templates
    return {
        "template_budget": budget,
        "family_size": sum(len(orbit_masks(rep, n)) for rep in chosen),
        "template_generators_used": len(templates),
        "orbit_count": len(chosen),
        "orbit_size_prefix": [len(orbit_masks(rep, n)) for rep in chosen[:8]],
        "representative_prefix": [mask_to_set(rep, n) for rep in chosen[:5]],
    }


def run_case(n: int, ell: int, sampled: bool) -> dict[str, Any]:
    reps = orbit_representatives(n, ell, sampled)
    greedy_rows = [greedy_orbit_union(reps, n, budget) for budget in TEMPLATE_BUDGETS]
    best_ratio_row = max(
        (row for row in greedy_rows if row["family_size"]),
        key=lambda row: (
            row["family_size"] / max(1, row["template_generators_used"]),
            row["family_size"],
        ),
    )
    return {
        "N_prime": n,
        "ell_prime": ell,
        "mode": "sampled_orbit_reps" if sampled else "exact_all_orbit_reps",
        "orbit_representatives": len(reps),
        "ambient_class_count": comb(n, ell) if not sampled else None,
        "sampled_rep_count": len(reps) if sampled else None,
        "singleton_root_difference_germ": singleton_germ(n),
        "best_single_orbits": best_single_orbits(reps, n),
        "greedy_orbit_union_rows": greedy_rows,
        "best_family_size_per_template": {
            "ratio": best_ratio_row["family_size"]
            / max(1, best_ratio_row["template_generators_used"]),
            "row": best_ratio_row,
        },
    }


def build_certificate() -> dict[str, Any]:
    cases = [run_case(n, ell, sampled=False) for n, ell in EXACT_CASES]
    cases.extend(run_case(n, ell, sampled=True) for n, ell in SAMPLED_CASES)
    early_cap = all(
        max(row["family_size"] for row in case["greedy_orbit_union_rows"]) <= 2 * max(TEMPLATE_BUDGETS)
        for case in cases
    )
    payload = {
        "schema": "generator_economy_design_search.v1",
        "roadmap_task": "E12 / QA.15 / generator_economy",
        "status": "EXPERIMENTAL_EVIDENCE",
        "object": (
            "l-subset centers in Z/NZ; pair differences 1_S-1_T in Z[zeta_N] "
            "modulo cyclic unit shifts and sign"
        ),
        "template_generator_interpretation": (
            "one norm check per unit/sign difference template; no multiplicative "
            "semigroup compression is attempted"
        ),
        "template_budgets": list(TEMPLATE_BUDGETS),
        "cases": cases,
        "interpretation": {
            "outcome": "CYCLIC_GERM_LIFTS_BUT_EARLY_TEMPLATE_CAP_IN_TOYS",
            "early_cap_seen": early_cap,
            "summary": (
                "The singleton root-difference germ lifts to l-sum cyclic orbits: "
                "an orbit of size N uses at most N/2 unit/sign templates.  Greedy "
                "unions at N=16 exact and N=32 sampled grow only roughly linearly "
                "with the template budget, so this baseline does not yet exhibit "
                "a large K/poly-style generator-economy design."
            ),
            "next_step": (
                "Try genuinely multiplicative compression of templates, or import "
                "abelian difference-set constructions; plain cyclic-orbit unions "
                "appear capped early."
            ),
        },
        "nonclaims": [
            "does not prove nonexistence of generator-economy designs",
            "does not use or estimate locator-fiber counts",
            "does not certify actual Row-C values modulo a prime",
            "does not attempt multiplicative semigroup factorization among templates",
            "N=32 cases use deterministic sampled orbit representatives",
        ],
    }
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = sha256_text(normalized)
    return payload


def print_summary(certificate: dict[str, Any]) -> None:
    print(certificate["schema"])
    print(certificate["interpretation"]["outcome"])
    for case in certificate["cases"]:
        print(
            f"N={case['N_prime']} ell={case['ell_prime']} "
            f"mode={case['mode']} reps={case['orbit_representatives']}"
        )
        print("  singleton germ:", case["singleton_root_difference_germ"])
        for row in case["greedy_orbit_union_rows"]:
            print(
                "  budget={template_budget} size={family_size} "
                "g={template_generators_used} orbits={orbit_count}".format(**row)
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="write certificate JSON")
    parser.add_argument("--check", type=Path, help="check an existing certificate JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    if args.check:
        existing = json.loads(args.check.read_text())
        if existing != certificate:
            raise SystemExit(f"certificate mismatch: {args.check}")
    if not args.emit and not args.check:
        print_summary(certificate)


if __name__ == "__main__":
    main()
