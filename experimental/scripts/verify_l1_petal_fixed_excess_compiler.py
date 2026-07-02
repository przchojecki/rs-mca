#!/usr/bin/env python3
"""Compiler for fixed-excess full-petal sunflower bounds.

This packages Lemma 16 of l1_full_list_quotient_proof_program.md into exact
integer layer bounds for fixed cofactor excess d-ell <= E.  It is a compiler
for an existing proof, not a fresh exhaustive list decoder.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


DEFAULT_CERT = Path(
    "experimental/data/certificates/l1-petal-fixed-excess/"
    "l1_petal_fixed_excess_compiler.json"
)
MAX_EXCESS = 6


def layer_bound(petal_count: int, field_size: int, excess: int) -> int:
    """Lemma-16 bound for one full-petal cofactor-excess layer."""
    if petal_count < 2:
        raise ValueError("need at least two petals")
    if field_size < 2:
        raise ValueError("field_size must be at least 2")
    if excess < 0:
        raise ValueError("excess must be nonnegative")
    if excess == 0:
        return comb(petal_count, 2) * field_size
    return (1 << petal_count) * (field_size ** (excess + 1))


def cumulative_bound(petal_count: int, field_size: int, max_excess: int) -> int:
    return sum(layer_bound(petal_count, field_size, e) for e in range(max_excess + 1))


def layer_table(petal_count: int, field_size: int, max_excess: int = MAX_EXCESS) -> dict[str, Any]:
    rows = []
    for excess in range(max_excess + 1):
        bound = layer_bound(petal_count, field_size, excess)
        rows.append({
            "excess_e": excess,
            "defect": "d = ell + e",
            "bound": bound,
            "bound_bit_length": bound.bit_length(),
            "source": "binom(M,2) q" if excess == 0 else "2^M q^(e+1)",
        })
    total = cumulative_bound(petal_count, field_size, max_excess)
    return {
        "petal_count_M": petal_count,
        "field_size_q": field_size,
        "max_excess_E": max_excess,
        "layers": rows,
        "cumulative_bound": total,
        "cumulative_bound_bit_length": total.bit_length(),
    }


def lower_cutoff_profile(log2_n: int, q_power: int, max_excess: int) -> dict[str, Any]:
    """Exact growth profile when M = log2(n) and q = n^q_power."""
    n = 1 << log2_n
    q = n ** q_power
    petal_count = log2_n
    table = layer_table(petal_count, q, max_excess)
    rows = []
    for row in table["layers"]:
        ceil_log2_bound = row["bound"].bit_length()
        rows.append({
            **row,
            "ceil_log2_bound": ceil_log2_bound,
            "n_power_upper_as_fraction": f"{ceil_log2_bound}/{log2_n}",
        })
    return {
        "n": n,
        "log2_n": log2_n,
        "petal_count_M": petal_count,
        "field_size_q": q,
        "q_power": q_power,
        "max_excess_E": max_excess,
        "layers": rows,
        "cumulative_bound_bit_length": table["cumulative_bound_bit_length"],
        "polynomial_exponent_rule": (
            "for fixed E, 2^M q^(E+1) <= n^(1 + q_power*(E+1)) "
            "when M=log2(n)"
        ),
    }


def self_tests() -> None:
    assert layer_bound(5, 101, 0) == 10 * 101
    assert layer_bound(5, 101, 1) == 32 * 101**2
    assert cumulative_bound(5, 101, 2) == 10 * 101 + 32 * 101**2 + 32 * 101**3
    for M in [4, 8, 16]:
        for q in [17, 101, 257]:
            prev = 0
            for e in range(MAX_EXCESS + 1):
                current = layer_bound(M, q, e)
                assert current > prev
                prev = current
    profile = lower_cutoff_profile(log2_n=20, q_power=2, max_excess=MAX_EXCESS)
    top = profile["layers"][-1]
    assert top["bound"] == (1 << 20) * ((1 << 40) ** 7)
    assert top["n_power_upper_as_fraction"] == "301/20"


def build_certificate() -> dict[str, Any]:
    self_tests()
    toy_tables = [
        layer_table(petal_count=4, field_size=17),
        layer_table(petal_count=8, field_size=101),
        layer_table(petal_count=16, field_size=257),
    ]
    lower_cutoff = [
        lower_cutoff_profile(log2_n=20, q_power=1, max_excess=MAX_EXCESS),
        lower_cutoff_profile(log2_n=20, q_power=2, max_excess=MAX_EXCESS),
        lower_cutoff_profile(log2_n=40, q_power=1, max_excess=MAX_EXCESS),
        lower_cutoff_profile(log2_n=40, q_power=2, max_excess=MAX_EXCESS),
    ]
    return {
        "schema": "l1-petal-fixed-excess-v1",
        "status": "PROVED_COMPILER__CITES_L1_LEMMA_16",
        "roadmap_task": "Q2.9 / petal_fixed_excess",
        "object": {
            "setting": "background-free full-petal sunflower listed codewords",
            "petal_count": "M",
            "petal_size": "ell",
            "core_defect": "d = ell + e",
            "fixed_excess_range_checked": f"0 <= e <= {MAX_EXCESS}",
        },
        "lemma_dependency": {
            "source": "experimental/notes/l1/l1_full_list_quotient_proof_program.md",
            "lemma": "Lemma 16. Cofactor-Budgeted Full-Petal Layers",
            "used_bound": (
                "for ell <= d <= ell+E, count <= binom(M,2)q + "
                "2^M sum_{e=1}^E q^(e+1)"
            ),
        },
        "per_layer_formula": {
            "e=0": "binom(M,2) q",
            "e>=1": "2^M q^(e+1)",
        },
        "toy_growth_tables": toy_tables,
        "lower_cutoff_profiles": lower_cutoff,
        "conclusion": (
            "At the L1 lower cutoff M=O(log n) and q=poly(n), every fixed "
            "cofactor-excess full-petal layer is polynomially bounded; any "
            "full-petal obstruction must use growing excess."
        ),
        "non_claim": (
            "This packet does not close mixed-petal sunflower amplification "
            "and does not enumerate actual list codewords beyond the Lemma-16 "
            "upper-bound compiler."
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
    print("l1-petal-fixed-excess certificate")
    print(f"  schema: {cert['schema']}")
    for table in cert["toy_growth_tables"]:
        print(
            f"  M={table['petal_count_M']} q={table['field_size_q']} "
            f"E={table['max_excess_E']} total_bits={table['cumulative_bound_bit_length']}"
        )
    for profile in cert["lower_cutoff_profiles"]:
        top = profile["layers"][-1]
        print(
            f"  lower-cutoff log2n={profile['log2_n']} q=n^{profile['q_power']} "
            f"top_e={top['excess_e']} exponent_bound={top['n_power_upper_as_fraction']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        DEFAULT_CERT.parent.mkdir(parents=True, exist_ok=True)
        DEFAULT_CERT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {DEFAULT_CERT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
