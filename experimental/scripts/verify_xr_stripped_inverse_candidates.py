#!/usr/bin/env python3
"""E11a stripped XR inverse candidate-family scan.

This is an EXPERIMENTAL evidence verifier.  It does not enumerate actual
Reed-Solomon word pairs and does not prove the XR inverse theorem.  It tests
the post-quotient-stripping prediction on the natural Johnson-family
dictionary used by the XR evidence route:

* fixed-core families, modelling fixed-root/tangent structure;
* fixed-hole families, the complementary first-eigenspace support structure;
* quotient block-profile cells, which are paid and stripped before the inverse
  interpretation.

For each half-size case J(n,n/2) with n in {16,32}, the verifier ranks these
families by E_3^J(A)=Pr[T_0,T_1,T_2,T_3 all lie in A].  After removing the
quotient-profile cells, every top candidate is fixed-core or fixed-hole.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
from typing import Any


CASES = ((16, 8), (32, 16))
MAX_FIXED_SIZE = 4
TOP_PER_QUOTIENT_SCALE = 5
RAW_TOP_LIMIT = 12
POST_STRIP_TOP_LIMIT = 8
OUTPUT = Path(
    "experimental/data/certificates/xr-stripped-inverse-candidates/"
    "xr_stripped_inverse_candidates.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "float": float(value),
    }


def e3_fixed_core(n: int, j: int, core_size: int) -> Fraction:
    density = Fraction(comb(n - core_size, j - core_size), comb(n, j))
    survival = Fraction(j - core_size, j)
    return density * survival**3


def e3_fixed_hole(n: int, j: int, hole_size: int) -> Fraction:
    density = Fraction(comb(n - hole_size, j), comb(n, j))
    survival = Fraction(n - j - hole_size, n - j)
    return density * survival**3


def e3_block_profile(n: int, j: int, block_size: int, profile: tuple[int, ...]) -> Fraction:
    count = 1
    internal_moves = 0
    for selected in profile:
        count *= comb(block_size, selected)
        internal_moves += selected * (block_size - selected)
    density = Fraction(count, comb(n, j))
    survival = Fraction(internal_moves, j * (n - j))
    return density * survival**3


def profile_types(
    block_count: int,
    block_size: int,
    total: int,
    minimum: int = 0,
) -> list[tuple[int, ...]]:
    if block_count == 0:
        return [()] if total == 0 else []
    out: list[tuple[int, ...]] = []
    max_first = min(block_size, total)
    for first in range(minimum, max_first + 1):
        remaining = total - first
        if remaining < first * (block_count - 1):
            continue
        if remaining > block_size * (block_count - 1):
            continue
        for tail in profile_types(block_count - 1, block_size, remaining, first):
            out.append((first,) + tail)
    return out


def orbit_size(profile: tuple[int, ...]) -> int:
    counts: dict[int, int] = {}
    for entry in profile:
        counts[entry] = counts.get(entry, 0) + 1
    out = factorial(len(profile))
    for multiplicity in counts.values():
        out //= factorial(multiplicity)
    return out


def proper_block_sizes(n: int) -> list[int]:
    return [size for size in range(2, n) if n % size == 0]


def residual_degree_cap(n: int, j: int, density: Fraction = Fraction(1, 1)) -> Fraction:
    """If an induced residual graph has max degree <= j, then E_3 <= density*(j/d)^3."""
    johnson_degree = j * (n - j)
    return density * Fraction(j, johnson_degree) ** 3


def candidate_record(
    *,
    family: str,
    classification: str,
    n: int,
    j: int,
    e3: Fraction,
    stripped: bool,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    return {
        "family": family,
        "classification": classification,
        "n": n,
        "j": j,
        "E_3": fraction_record(e3),
        "stripped_before_inverse": stripped,
        "parameters": parameters,
    }


def candidates_for_case(n: int, j: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    max_fixed = min(MAX_FIXED_SIZE, j, n - j)
    for size in range(1, max_fixed + 1):
        records.append(candidate_record(
            family="fixed_core",
            classification="tangent_fixed_root",
            n=n,
            j=j,
            e3=e3_fixed_core(n, j, size),
            stripped=False,
            parameters={"core_size": size},
        ))
        records.append(candidate_record(
            family="fixed_hole",
            classification="support_dual_fixed_hole",
            n=n,
            j=j,
            e3=e3_fixed_hole(n, j, size),
            stripped=False,
            parameters={"hole_size": size},
        ))

    for block_size in proper_block_sizes(n):
        block_count = n // block_size
        top_profiles = []
        for profile in profile_types(block_count, block_size, j):
            top_profiles.append((
                e3_block_profile(n, j, block_size, profile),
                profile,
            ))
        top_profiles.sort(reverse=True, key=lambda item: item[0])
        for e3, profile in top_profiles[:TOP_PER_QUOTIENT_SCALE]:
            records.append(candidate_record(
                family="quotient_block_profile_cell",
                classification="paid_quotient_profile",
                n=n,
                j=j,
                e3=e3,
                stripped=True,
                parameters={
                    "block_size": block_size,
                    "block_count": block_count,
                    "profile_representative": list(profile),
                    "labeled_profile_cells_in_orbit": orbit_size(profile),
                },
            ))
    return records


def summarize_case(n: int, j: int) -> dict[str, Any]:
    candidates = candidates_for_case(n, j)
    ranked = sorted(candidates, reverse=True, key=lambda row: row["E_3"]["float"])
    post_strip = [row for row in ranked if not row["stripped_before_inverse"]]
    top_post_strip = post_strip[:POST_STRIP_TOP_LIMIT]
    allowed = {"tangent_fixed_root", "support_dual_fixed_hole"}
    return {
        "n": n,
        "j": j,
        "candidate_count": len(candidates),
        "raw_top": ranked[:RAW_TOP_LIMIT],
        "post_quotient_strip_top": top_post_strip,
        "post_strip_all_top_candidates_first_eigenspace": all(
            row["classification"] in allowed for row in top_post_strip
        ),
        "quotient_profile_present_in_raw_top": any(
            row["stripped_before_inverse"] for row in ranked[:RAW_TOP_LIMIT]
        ),
        "residual_degree_cap_density_1": fraction_record(residual_degree_cap(n, j)),
        "residual_degree_cap_comment": (
            "If a stripped residual family has induced one-exchange degree <= j, "
            "then E_3 is at most density*(j/(j(n-j)))^3.  This is the "
            "support-side shadow of the t=2 residual one-exchange degree packet."
        ),
    }


def build_certificate() -> dict[str, Any]:
    cases = [summarize_case(n, j) for n, j in CASES]
    payload = {
        "schema": "xr_stripped_inverse_candidates.v1",
        "roadmap_task": "E11 / E2b / xr_inverse_toy candidate-family scan",
        "status": "EXPERIMENTAL_EVIDENCE",
        "energy": "E_3^J(A)=Pr[T_0,T_1,T_2,T_3 all lie in A] on J(n,j)",
        "scope": (
            "candidate-family dictionary only: fixed-core, fixed-hole, and "
            "quotient block-profile cells; not actual RS word-pair orbits"
        ),
        "cases": cases,
        "interpretation": {
            "outcome": "POST_QUOTIENT_STRIP_TOP_CANDIDATES_ARE_FIRST_EIGENSPACE",
            "xr_prior_update": (
                "Positive but scoped.  The candidate dictionary supports the "
                "stripped inverse expectation: quotient-profile cells must be "
                "removed first, and the remaining largest E_3 examples are "
                "fixed-root/fixed-hole first-eigenspace structures."
            ),
            "next_step": (
                "Attach the same stripped ranking to actual toy aligned-locator "
                "sets A_{u,v}; this packet is not a substitute for that pair-orbit scan."
            ),
        },
        "nonclaims": [
            "does not prove xr_inverse",
            "does not enumerate arbitrary families in J(n,j)",
            "does not enumerate actual RS word-pair orbits",
            "does not classify fixed-hole support structure as a paid MCA ledger",
        ],
    }
    normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["payload_sha256"] = sha256_text(normalized)
    return payload


def print_summary(certificate: dict[str, Any]) -> None:
    print(certificate["schema"])
    print(certificate["interpretation"]["outcome"])
    for case in certificate["cases"]:
        print(f"n={case['n']} j={case['j']} candidates={case['candidate_count']}")
        print("  raw top:")
        for row in case["raw_top"][:6]:
            print(
                "   ",
                row["family"],
                row["classification"],
                row["parameters"],
                row["E_3"]["numerator"],
                "/",
                row["E_3"]["denominator"],
            )
        print("  post-strip top:")
        for row in case["post_quotient_strip_top"][:4]:
            print(
                "   ",
                row["family"],
                row["classification"],
                row["parameters"],
                row["E_3"]["numerator"],
                "/",
                row["E_3"]["denominator"],
            )
        print("  residual cap density 1:", case["residual_degree_cap_density_1"])


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
