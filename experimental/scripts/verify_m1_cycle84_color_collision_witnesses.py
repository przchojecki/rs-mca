#!/usr/bin/env python3
"""Verify compact Cycle84 color-shell and collision-witness clauses.

This nonmutating verifier supports
experimental/notes/m1/m1_cycle116_finite_chain_contract.md. It uses the
normalized slot table from verify_m1_cycle116_slot_identities.py to check:

* the exact seven-slot color shell size P0;
* six explicit product collisions, plus their tau partners, giving twelve
  verified double fibers;
* the formal energy-saturation implication: if the remaining heavy Cycle84
  census proves ordered off-diagonal energy D <= 24, then these twelve double
  fibers account for all collisions and the distinct-product count is
  52,747,567,092.

It does not prove the global D <= 24 energy upper bound.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_slot_identities as slot


EXPECTED_COLOR_SHELL_SIZE = 52_747_567_104
EXPECTED_DISTINCT_PRODUCTS = 52_747_567_092
EXPECTED_DOUBLE_FIBERS = 12
EXPECTED_ORDERED_ENERGY = 24
TARGET_COLOR = 4
SLOT_COUNT = 7
KEYS_PER_SLOT = 48

WITNESS_PAIRS = [
    {
        "tuple_A": [4, 26, 46, 12, 32, 22, 40],
        "tuple_B": [16, 27, 7, 1, 41, 24, 14],
        "product": [3, 16, 6, 13, 15, 10, 10, 11, 8, 5, 12, 9, 13, 6, 4, 3],
    },
    {
        "tuple_A": [26, 27, 7, 1, 41, 24, 14],
        "tuple_B": [10, 26, 46, 12, 32, 22, 40],
        "product": [16, 5, 1, 9, 3, 7, 2, 0, 16, 5, 11, 6, 16, 3, 5, 4],
    },
    {
        "tuple_A": [4, 26, 46, 23, 33, 2, 40],
        "tuple_B": [16, 27, 7, 18, 40, 0, 14],
        "product": [12, 0, 11, 2, 1, 16, 11, 8, 2, 16, 8, 13, 7, 11, 2, 2],
    },
    {
        "tuple_A": [26, 27, 7, 18, 40, 0, 14],
        "tuple_B": [10, 26, 46, 23, 33, 2, 40],
        "product": [11, 13, 10, 14, 13, 14, 15, 2, 16, 2, 7, 9, 9, 4, 7],
    },
    {
        "tuple_A": [4, 26, 29, 12, 33, 2, 20],
        "tuple_B": [16, 27, 38, 1, 40, 0, 32],
        "product": [16, 2, 11, 4, 11, 9, 1, 12, 15, 1, 14, 0, 12, 12, 13, 1],
    },
    {
        "tuple_A": [26, 27, 38, 1, 40, 0, 32],
        "tuple_B": [10, 26, 29, 12, 33, 2, 20],
        "product": [3, 8, 9, 9, 15, 7, 8, 1, 16, 12, 14, 7, 16, 4, 16, 6],
    },
]


FieldElt = Tuple[int, ...]


def key_seed_shift(key: int) -> Tuple[int, int]:
    return key // 16 + 1, key % 16


def key_color(key: int) -> int:
    seed, shift = key_seed_shift(key)
    return slot.color(seed, shift)


def tau_key(key: int) -> int:
    seed, shift = key_seed_shift(key)
    if seed == 1:
        return 16 + (shift + 6) % 16
    if seed == 2:
        return (shift + 10) % 16
    return 32 + (shift + 8) % 16


def tau_tuple(keys: Sequence[int]) -> Tuple[int, ...]:
    return tuple(tau_key(key) for key in keys)


def color_sum(keys: Sequence[int]) -> int:
    return sum(key_color(key) for key in keys) % 16


def build_slot_values() -> Dict[Tuple[int, int], FieldElt]:
    beta_squared = slot.fmul(slot.BETA, slot.BETA)
    seed_polys = {
        seed: slot.prime_poly_from_roots(
            pow(3, exponent, slot.P) for exponent in exponents
        )
        for seed, exponents in slot.E_SETS.items()
    }
    return {
        (t, key): slot.normalized_u(
            seed_polys,
            beta_squared,
            t,
            key_seed_shift(key)[0],
            key_seed_shift(key)[1],
        )
        for t in range(1, SLOT_COUNT + 1)
        for key in range(KEYS_PER_SLOT)
    }


def tuple_product(
    keys: Sequence[int],
    table: Dict[Tuple[int, int], FieldElt],
) -> FieldElt:
    if len(keys) != SLOT_COUNT:
        raise AssertionError(("bad tuple length", keys))
    out = slot.ONE
    for t, key in enumerate(keys, 1):
        if not 0 <= key < KEYS_PER_SLOT:
            raise AssertionError(("bad key", keys))
        out = slot.fmul(out, table[(t, key)])
    return out


def color_distribution() -> Dict[int, int]:
    counts = {color: 0 for color in range(16)}
    for key in range(KEYS_PER_SLOT):
        counts[key_color(key)] += 1
    return counts


def color_shell_size(counts: Dict[int, int]) -> int:
    dp = [0] * 16
    dp[0] = 1
    for _ in range(SLOT_COUNT):
        nxt = [0] * 16
        for current, current_count in enumerate(dp):
            if current_count == 0:
                continue
            for color, color_count in counts.items():
                nxt[(current + color) % 16] += current_count * color_count
        dp = nxt
    return dp[TARGET_COLOR]


def verify_witnesses(table: Dict[Tuple[int, int], FieldElt]) -> Dict[str, Any]:
    witness_tuples = set()
    collision_products = set()
    tau_collision_products = set()

    for index, witness in enumerate(WITNESS_PAIRS, 1):
        tuple_a = tuple(witness["tuple_A"])
        tuple_b = tuple(witness["tuple_B"])
        expected_product = slot.field(witness["product"])
        tau_a = tau_tuple(tuple_a)
        tau_b = tau_tuple(tuple_b)

        for keys in (tuple_a, tuple_b, tau_a, tau_b):
            if color_sum(keys) != TARGET_COLOR:
                raise AssertionError((index, keys, "wrong color"))
            if tau_tuple(tau_tuple(keys)) != keys:
                raise AssertionError((index, keys, "tau not involutive"))
            witness_tuples.add(keys)

        product_a = tuple_product(tuple_a, table)
        product_b = tuple_product(tuple_b, table)
        if product_a != product_b or product_a != expected_product:
            raise AssertionError((index, "witness product mismatch"))

        tau_product_a = tuple_product(tau_a, table)
        tau_product_b = tuple_product(tau_b, table)
        if tau_product_a != tau_product_b:
            raise AssertionError((index, "tau product mismatch"))

        collision_products.add(product_a)
        tau_collision_products.add(tau_product_a)

    if len(witness_tuples) != 4 * len(WITNESS_PAIRS):
        raise AssertionError("witness tuples are not all distinct")
    if len(collision_products) != len(WITNESS_PAIRS):
        raise AssertionError("base collision products are not distinct")
    if len(tau_collision_products) != len(WITNESS_PAIRS):
        raise AssertionError("tau collision products are not distinct")
    if collision_products & tau_collision_products:
        raise AssertionError("base and tau collision products overlap")

    return {
        "tau_orbits": len(WITNESS_PAIRS),
        "verified_double_fibers": 2 * len(WITNESS_PAIRS),
        "verified_witness_tuples": len(witness_tuples),
        "ordered_energy_contribution": 4 * len(WITNESS_PAIRS),
    }


def build_report() -> Dict[str, Any]:
    slot_report = slot.build_report()
    table = build_slot_values()
    counts = color_distribution()
    shell_size = color_shell_size(counts)
    witnesses = verify_witnesses(table)

    checks = {
        "slot_identity_replay_passes": slot_report["status"] == "PASS",
        "color_shell_size_matches": shell_size == EXPECTED_COLOR_SHELL_SIZE,
        "six_tau_orbits_verified": witnesses["tau_orbits"] == 6,
        "twelve_double_fibers_verified": (
            witnesses["verified_double_fibers"] == EXPECTED_DOUBLE_FIBERS
        ),
        "ordered_energy_contribution_24": (
            witnesses["ordered_energy_contribution"] == EXPECTED_ORDERED_ENERGY
        ),
        "energy_saturation_would_give_exact_occupancy": (
            shell_size - witnesses["verified_double_fibers"]
            == EXPECTED_DISTINCT_PRODUCTS
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / FINITE-MODEL-WITNESS-VERIFIED / CONDITIONAL",
        "theorem_problem_id": "M1 Cycle84 color shell and collision witnesses",
        "slot_table_digest": slot_report["slot_table"]["digest_sha256"],
        "color_shell": {
            "target_color": TARGET_COLOR,
            "per_slot_color_distribution": {
                str(color): count for color, count in counts.items() if count
            },
            "compatible_tuple_count": shell_size,
        },
        "collision_witnesses": witnesses,
        "energy_saturation_reduction": {
            "import_needed": "ordered off-diagonal energy D <= 24",
            "verified_energy_lower_bound": witnesses["ordered_energy_contribution"],
            "if_import_holds_then_distinct_products": EXPECTED_DISTINCT_PRODUCTS,
            "if_import_holds_then_m_max": 2,
            "if_import_holds_then_no_fibers_of_size_at_least_3": True,
        },
        "checks": checks,
        "imports_required": [
            "projected tau-folded duplicate-bin completeness",
            "official ABF source gate verification",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    shell = report["color_shell"]
    witnesses = report["collision_witnesses"]
    reduction = report["energy_saturation_reduction"]

    print("m1_cycle84_color_collision_witnesses: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(f"slot_table_digest={report['slot_table_digest']}")
    print(
        "color_shell="
        f"target={shell['target_color']}, "
        f"count={shell['compatible_tuple_count']}, "
        f"per_slot={shell['per_slot_color_distribution']}"
    )
    print(
        "collision_witnesses="
        f"tau_orbits={witnesses['tau_orbits']}, "
        f"double_fibers={witnesses['verified_double_fibers']}, "
        f"energy_contribution={witnesses['ordered_energy_contribution']}"
    )
    print(
        "energy_saturation="
        f"if {reduction['import_needed']}, then distinct_products="
        f"{reduction['if_import_holds_then_distinct_products']} and "
        f"m_max={reduction['if_import_holds_then_m_max']}"
    )
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify compact Cycle84 color-shell/collision witnesses."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the audit report as JSON",
    )
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
