#!/usr/bin/env python3
"""Sharp norm-height constants for the quotient e1 collision gate.

For a quotient order N and quotient agreement ell, a nonzero e1 difference
has coefficient l1 height at most 2*ell.  Hence every conjugate is bounded by
2*ell and the cyclotomic norm is bounded by (2*ell)^phi(N).  This verifier
turns that exact exponent into frontier tables for deployed bit budgets.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sympy


OUTPUT = Path(
    "experimental/data/certificates/row-c-e1-sampling/"
    "e1_sharp_norm_height_constants.json"
)
RATES = [(1, 2), (1, 4), (1, 8), (1, 16)]
BIT_BUDGETS = [128, 192, 256]
ROW_C_N = 2**10
ROW_C_COMPATIBLE_ORDERS = [64, 128, 256]


@dataclass(frozen=True)
class HeightRow:
    rate: str
    N_prime: int
    ell_prime: int
    phi_N: int
    height_base: int
    height_bound: int
    height_bound_bit_length: int
    exponent_shape: str


def phi(n: int) -> int:
    result = n
    m = n
    p = 2
    while p * p <= m:
        if m % p == 0:
            result -= result // p
            while m % p == 0:
                m //= p
        p += 1
    if m > 1:
        result -= result // m
    return result


def ell_for_rate(N: int, rate_num: int, rate_den: int) -> int | None:
    if (rate_num * N) % rate_den:
        return None
    return (rate_num * N) // rate_den + 1


def height_row(N: int, rate_num: int, rate_den: int) -> HeightRow:
    ell = ell_for_rate(N, rate_num, rate_den)
    if ell is None:
        raise ValueError("rate*N must be integral")
    ph = phi(N)
    base = 2 * ell
    bound = base**ph
    return HeightRow(
        rate=f"{rate_num}/{rate_den}",
        N_prime=N,
        ell_prime=ell,
        phi_N=ph,
        height_base=base,
        height_bound=bound,
        height_bound_bit_length=bound.bit_length(),
        exponent_shape="phi(N') * log2(2 ell')",
    )


def row_payload(row: HeightRow) -> dict[str, Any]:
    return {
        "rate": row.rate,
        "N_prime": row.N_prime,
        "ell_prime": row.ell_prime,
        "phi_N": row.phi_N,
        "height_base_2ell": row.height_base,
        "height_bound": row.height_bound,
        "height_bound_bit_length": row.height_bound_bit_length,
        "exponent_shape": row.exponent_shape,
        "dyadic_simplification": (
            "(N'/2) * log2(2 ell')" if row.N_prime & (row.N_prime - 1) == 0 else None
        ),
    }


def certified_by_bits(row: HeightRow, bits: int) -> bool:
    return row.height_bound < (1 << bits)


def frontier(
    rate_num: int,
    rate_den: int,
    bits: int,
    mode: str,
    max_order: int = 2048,
) -> dict[str, Any]:
    if mode not in {"even_prefix", "dyadic"}:
        raise ValueError(mode)
    passing: list[HeightRow] = []
    first_failing: HeightRow | None = None
    for N in range(2, max_order + 1):
        if mode == "even_prefix" and N % 2:
            continue
        if mode == "dyadic" and N & (N - 1):
            continue
        ell = ell_for_rate(N, rate_num, rate_den)
        if ell is None:
            continue
        row = height_row(N, rate_num, rate_den)
        if certified_by_bits(row, bits):
            passing.append(row)
        elif first_failing is None:
            first_failing = row
            break
    if not passing:
        raise AssertionError("frontier has no passing rows")
    best = passing[-1]
    return {
        "rate": f"{rate_num}/{rate_den}",
        "bit_budget": bits,
        "mode": mode,
        "certified_condition": "(2 ell')^phi(N') < 2^bit_budget",
        "frontier_meaning": (
            "all compatible even orders up to this value pass"
            if mode == "even_prefix"
            else "all compatible dyadic orders up to this value pass"
        ),
        "max_certified": row_payload(best),
        "first_failing_after_frontier": None
        if first_failing is None
        else row_payload(first_failing),
    }


def row_c_prime() -> int:
    """Smallest prime p > 2^250 with p = 1 mod 1024."""
    p = (1 << 250) + ((1 - (1 << 250)) % ROW_C_N)
    while not sympy.isprime(p):
        p += ROW_C_N
    return p


def row_c_orders() -> list[dict[str, Any]]:
    p = row_c_prime()
    out = []
    for N in ROW_C_COMPATIBLE_ORDERS:
        row = height_row(N, 1, 2)
        out.append({
            **row_payload(row),
            "row_c_prime_bit_length": p.bit_length(),
            "certified_for_row_c_prime": row.height_bound < p,
        })
    return out


def self_tests() -> None:
    assert phi(64) == 32
    assert phi(128) == 64
    assert height_row(80, 1, 2).ell_prime == 41
    assert height_row(80, 1, 2).height_bound_bit_length == 204
    f = frontier(1, 2, 256, "even_prefix")
    assert f["max_certified"]["N_prime"] == 84
    assert f["first_failing_after_frontier"]["N_prime"] == 86
    d = frontier(1, 2, 256, "dyadic")
    assert d["max_certified"]["N_prime"] == 64
    assert d["first_failing_after_frontier"]["N_prime"] == 128
    rows = row_c_orders()
    assert rows[0]["certified_for_row_c_prime"] is True
    assert rows[1]["certified_for_row_c_prime"] is False
    assert rows[2]["certified_for_row_c_prime"] is False


def build_certificate() -> dict[str, Any]:
    self_tests()
    frontiers = []
    for bits in BIT_BUDGETS:
        for rate_num, rate_den in RATES:
            frontiers.append(frontier(rate_num, rate_den, bits, "even_prefix"))
            frontiers.append(frontier(rate_num, rate_den, bits, "dyadic"))
    return {
        "schema": "e1-sharp-norm-height-constants-v1",
        "status": "PROVED_ARITHMETIC_COMPILER",
        "roadmap_task": "are_sharp_constant",
        "theorem": {
            "norm_height_bound": "|Norm(Delta)| <= (2 ell')^phi(N')",
            "split_prime_transfer_gate": (
                "if p > (2 ell')^phi(N'), distinct characteristic-zero "
                "e1 classes cannot collide modulo a fixed embedding at p"
            ),
            "true_exponent_shape": "phi(N') log(2 ell')",
            "dyadic_shape": "(N'/2) log(2 ell')",
        },
        "frontiers": frontiers,
        "row_c_compatible_orders": row_c_orders(),
        "non_claim": (
            "This is a height-only transfer gate.  It deliberately shows that "
            "pure height certifies Row-C N'=64 but not N'=128 or N'=256."
        ),
    }


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("e1 sharp norm-height constants")
    print(f"  schema: {cert['schema']}")
    for row in cert["frontiers"]:
        if row["bit_budget"] == 256 and row["mode"] == "even_prefix":
            best = row["max_certified"]
            fail = row["first_failing_after_frontier"]
            print(
                f"  bits=256 rate={row['rate']} even-prefix: "
                f"Nmax={best['N_prime']} bits={best['height_bound_bit_length']} "
                f"next={fail['N_prime'] if fail else None}"
            )
    for row in cert["row_c_compatible_orders"]:
        print(
            f"  Row-C N'={row['N_prime']} height_bits={row['height_bound_bit_length']} "
            f"certified={row['certified_for_row_c_prime']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
