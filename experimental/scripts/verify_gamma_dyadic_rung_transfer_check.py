#!/usr/bin/env python3
"""Independent checker for the dyadic rung-transfer certificate.

Status: AUDIT. This script replays the recorded constants by raw support
enumeration without using the quotient pullback shortcut.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from math import comb, gcd
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "Route-gamma; prob:band; cor:periodic-support-count"
DEFAULT_CERT = Path(
    "experimental/data/certificates/gamma-dyadic-rung-transfer/"
    "gamma_dyadic_rung_transfer.json"
)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(text: str) -> Fraction:
    num, den = text.split("/")
    return Fraction(int(num), int(den))


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def stabilizer_size(support: tuple[int, ...], n: int) -> int:
    S = set(support)
    return sum(1 for shift in range(n) if {(x + shift) % n for x in S} == S)


def periodic_supports(n: int, j: int, scale: int) -> set[tuple[int, ...]]:
    if scale <= 0 or n % scale or j % scale:
        return set()
    span = n // scale
    supports: set[tuple[int, ...]] = set()
    for reps in itertools.combinations(range(span), j // scale):
        support: list[int] = []
        for rep in reps:
            support.extend((rep + t * span) % n for t in range(scale))
        supports.add(tuple(sorted(support)))
    return supports


def exact_count_closed(n: int, j: int, scale: int) -> int:
    if scale <= 0 or n % scale or j % scale:
        return 0
    total = comb(n // scale, j // scale)
    for larger in divisors(gcd(n, j)):
        if larger > scale and larger % scale == 0:
            total -= exact_count_closed(n, j, larger)
    return total


def exact_count_bruteforce(n: int, j: int, scale: int) -> int:
    return sum(
        1
        for support in periodic_supports(n, j, scale)
        if stabilizer_size(support, n) == scale
    )


def check_row(row: dict[str, Any]) -> None:
    if not row["applicable"]:
        return
    n = row["n"]
    j = row["j"]
    scale = row["scale_c"]
    exact_parent = exact_count_bruteforce(n, j, scale)
    closed_parent = exact_count_closed(n, j, scale)
    quotient_exact = exact_count_bruteforce(n // scale, j // scale, 1)
    at_least = len(periodic_supports(n, j, scale))
    quotient_total = comb(n // scale, j // scale)

    assert exact_parent == row["parent_exact_scale_count"]
    assert at_least == row["parent_at_least_scale_count"]
    assert quotient_exact == row["quotient_exact_aperiodic_count"]
    assert quotient_total == row["quotient_total_count"]
    assert closed_parent == row["closed_periodic_support_count"]
    assert row["pullback_image_count"] == quotient_total
    assert parse_fraction(row["kappa_c"]) == Fraction(exact_parent, quotient_exact)
    for degree, data in row["sampler_degrees"].items():
        deg = int(degree)
        expected = Fraction(exact_parent, quotient_exact) * gcd(deg, n)
        assert data["power_curve_multiplicity"] == gcd(deg, n)
        assert parse_fraction(data["sampler_adjusted_kappa"]) == expected


def exact_log2_power_of_two(value: Fraction) -> int:
    assert value.denominator == 1
    x = value.numerator
    assert x > 0 and not (x & (x - 1))
    return x.bit_length() - 1


def check_ladders(cert: dict[str, Any]) -> None:
    rows = cert["rows"]
    for ladder in cert["ladder_products"]:
        active = [row for row in rows if row["m"] == ladder["m"] and row["applicable"]]
        product = Fraction(1, 1)
        for row in active:
            product *= parse_fraction(row["kappa_c"])
        assert fraction_text(product) == ladder["identity_transfer_product"]
        assert exact_log2_power_of_two(product) * 1000 == ladder["identity_log2_millibits"]
        for degree, data in ladder["sampler_adjusted_products"].items():
            adjusted = Fraction(1, 1)
            for row in active:
                adjusted *= parse_fraction(row["sampler_degrees"][degree]["sampler_adjusted_kappa"])
            assert fraction_text(adjusted) == data["product"]
            assert exact_log2_power_of_two(adjusted) * 1000 == data["log2_millibits"]
            assert (
                data["log2_millibits"] > data["acceptance_ceiling_millibits"]
            ) == data["exceeds_acceptance_ceiling"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, default=DEFAULT_CERT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = json.loads(args.check.read_text())
    assert cert["theorem_problem_id"] == THEOREM_PROBLEM_ID
    assert cert["payload_sha256"] == payload_hash(cert)
    for row in cert["rows"]:
        check_row(row)
    check_ladders(cert)
    result = {
        "status": STATUS,
        "result": "PASS",
        "certificate": args.check.as_posix(),
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "rows_checked": len(cert["rows"]),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "gamma_dyadic_rung_transfer_check: "
            f"status={STATUS} result=PASS file={args.check.as_posix()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
