#!/usr/bin/env python3
"""Exact dyadic rung-transfer constants for toy quotient rows.

Status: EXPERIMENTAL / AUDIT. The script computes finite exact constants for
the Route-gamma transfer object tied to prob:band, def:periodicity-scale,
cor:periodic-support-count, lem:v13-quot-pullback, and thm:fiber-descent.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from math import comb, gcd
from pathlib import Path
from typing import Any

REDUCTIONS_PATH = Path(__file__).resolve().with_name(
    "verify_conjecture_f_reductions.py"
)
SPEC = importlib.util.spec_from_file_location("conjecture_f_reductions", REDUCTIONS_PATH)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"cannot load {REDUCTIONS_PATH}")
REDUCTIONS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REDUCTIONS)

P = REDUCTIONS.P
compose_x_power = REDUCTIONS.compose_x_power
divisor_set = REDUCTIONS.divisor_set
locator = REDUCTIONS.locator
subgroup = REDUCTIONS.subgroup


STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "Route-gamma; prob:band; cor:periodic-support-count"
SCHEMA_VERSION = "gamma-dyadic-rung-transfer-v1"
DEFAULT_OUTPUT = Path(
    "experimental/data/certificates/gamma-dyadic-rung-transfer/"
    "gamma_dyadic_rung_transfer.json"
)
CEILING_MILLIBITS = {
    2: 1199,
    3: 2068,
    4: 1993,
    5: 1107,
}
SAMPLER_DEGREES = (1, 2, 3)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def exact_periodic_count(n: int, j: int, scale: int) -> int:
    if scale <= 0 or n % scale or j % scale:
        return 0
    total = comb(n // scale, j // scale)
    for larger in divisors(gcd(n, j)):
        if larger > scale and larger % scale == 0:
            total -= exact_periodic_count(n, j, larger)
    return total


def periodic_supports_at_least(n: int, j: int, scale: int) -> set[tuple[int, ...]]:
    if n % scale or j % scale:
        return set()
    coset_span = n // scale
    supports: set[tuple[int, ...]] = set()
    for reps in itertools.combinations(range(coset_span), j // scale):
        support: list[int] = []
        for rep in reps:
            support.extend((rep + t * coset_span) % n for t in range(scale))
        supports.add(tuple(sorted(support)))
    return supports


def stabilizer_size(support: tuple[int, ...], n: int) -> int:
    S = set(support)
    return sum(1 for shift in range(n) if {(x + shift) % n for x in S} == S)


def periodic_supports_exact(n: int, j: int, scale: int) -> set[tuple[int, ...]]:
    return {
        support
        for support in periodic_supports_at_least(n, j, scale)
        if stabilizer_size(support, n) == scale
    }


def support_locator(H: list[int], support: tuple[int, ...]) -> tuple[int, ...]:
    return locator(tuple(H[i] for i in support))


def row_for(m: int, scale: int) -> dict[str, Any]:
    n = 2**m
    j = n // 2
    if scale > n or n % scale or j % scale:
        return {
            "m": m,
            "n": n,
            "j": j,
            "scale_c": scale,
            "applicable": False,
            "reason": "scale does not divide both n and j",
        }

    H = subgroup(n)
    Hq = subgroup(n // scale)
    quotient_j = j // scale

    parent_exact_supports = periodic_supports_exact(n, j, scale)
    parent_exact_count = len(parent_exact_supports)
    quotient_exact_count = exact_periodic_count(n // scale, quotient_j, 1)
    closed_parent_count = exact_periodic_count(n, j, scale)
    parent_at_least = {
        support_locator(H, support)
        for support in periodic_supports_at_least(n, j, scale)
    }
    pulled = {
        compose_x_power(poly, scale)
        for poly in divisor_set(Hq, quotient_j)
    }
    at_least_count = len(parent_at_least)
    quotient_total = comb(n // scale, quotient_j)

    if parent_at_least != pulled:
        raise AssertionError(f"pullback mismatch at n={n}, scale={scale}")
    if parent_exact_count != closed_parent_count:
        raise AssertionError(f"inclusion-exclusion mismatch at n={n}, scale={scale}")
    if parent_exact_count != quotient_exact_count:
        raise AssertionError(f"exact-scale transfer mismatch at n={n}, scale={scale}")

    kappa = Fraction(parent_exact_count, quotient_exact_count)
    sampler = {
        str(degree): {
            "power_curve_multiplicity": gcd(degree, n),
            "sampler_adjusted_kappa": fraction_text(kappa * gcd(degree, n)),
        }
        for degree in SAMPLER_DEGREES
    }
    return {
        "m": m,
        "n": n,
        "j": j,
        "scale_c": scale,
        "applicable": True,
        "parent_exact_scale_count": parent_exact_count,
        "parent_at_least_scale_count": at_least_count,
        "quotient_exact_aperiodic_count": quotient_exact_count,
        "quotient_total_count": quotient_total,
        "closed_periodic_support_count": closed_parent_count,
        "pullback_image_count": len(pulled),
        "kappa_c": fraction_text(kappa),
        "sampler_degrees": sampler,
    }


def exact_log2_power_of_two(value: Fraction) -> int | None:
    if value.denominator != 1:
        return None
    x = value.numerator
    if x <= 0 or x & (x - 1):
        return None
    return x.bit_length() - 1


def build_certificate() -> dict[str, Any]:
    rows = [row_for(m, c) for m in range(2, 6) for c in (2, 4, 8)]
    ladder_rows: list[dict[str, Any]] = []
    for m in range(2, 6):
        active = [row for row in rows if row["m"] == m and row["applicable"]]
        identity = Fraction(1, 1)
        for row in active:
            num, den = row["kappa_c"].split("/")
            identity *= Fraction(int(num), int(den))
        adjusted: dict[str, Any] = {}
        for degree in SAMPLER_DEGREES:
            product = Fraction(1, 1)
            for row in active:
                text = row["sampler_degrees"][str(degree)]["sampler_adjusted_kappa"]
                num, den = text.split("/")
                product *= Fraction(int(num), int(den))
            log2_value = exact_log2_power_of_two(product)
            if log2_value is None:
                raise AssertionError("sampler products should be powers of two in dyadic rows")
            ceiling = CEILING_MILLIBITS[m]
            adjusted[str(degree)] = {
                "product": fraction_text(product),
                "log2_millibits": log2_value * 1000,
                "acceptance_ceiling_millibits": ceiling,
                "exceeds_acceptance_ceiling": log2_value * 1000 > ceiling,
            }
        identity_log2 = exact_log2_power_of_two(identity)
        assert identity_log2 == 0
        ladder_rows.append(
            {
                "m": m,
                "n": 2**m,
                "active_scales": [row["scale_c"] for row in active],
                "identity_transfer_product": fraction_text(identity),
                "identity_log2_millibits": identity_log2 * 1000,
                "acceptance_ceiling_millibits": CEILING_MILLIBITS[m],
                "identity_exceeds_acceptance_ceiling": False,
                "sampler_adjusted_products": adjusted,
            }
        )
    named_findings = [
        {
            "m": ladder["m"],
            "n": ladder["n"],
            "sampler_degree": int(degree),
            "product": data["product"],
            "log2_millibits": data["log2_millibits"],
            "acceptance_ceiling_millibits": data["acceptance_ceiling_millibits"],
        }
        for ladder in ladder_rows
        for degree, data in ladder["sampler_adjusted_products"].items()
        if data["exceeds_acceptance_ceiling"]
    ]
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "proof_status": STATUS,
        "claim": "finite exact dyadic transfer constants for Route-gamma toy rows",
        "field": {"q_gen": P, "q_line": P, "q_chal": P},
        "row_rule": "n=2^m, j=n/2, scale c in {2,4,8}",
        "non_claims": [
            "No asymptotic tower-transfer theorem is claimed.",
            "No resolution of prob:band is claimed.",
            "The rung-transfer constants are distinct from the rung-margin calculation in PR #329.",
        ],
        "rows": rows,
        "ladder_products": ladder_rows,
        "named_over_ceiling_findings": named_findings,
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--emit-defaults", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print(
            "gamma_dyadic_rung_transfer: "
            f"status={STATUS} result=PASS rows={len(cert['rows'])} "
            f"findings={len(cert['named_over_ceiling_findings'])}"
        )
        print(args.output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
