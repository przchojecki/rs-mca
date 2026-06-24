#!/usr/bin/env python3
"""Verify the Cycle116 slot-block co-support assembly.

This nonmutating verifier checks the finite-field geometry behind the stated
Cycle116 co-support

    J_T = {1} union union_{t=1}^7 eta^t Y_{i_t,a_t}.

It proves the size and disjointness assertions used by the fixed-jet bridge:
the singleton lies in the inactive eta^0 H32 coset, the seven slot blocks lie
in seven disjoint active cosets, each block has size 16, and therefore every
seven-slot tuple has co-support size 1+7*16=113.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Set, Tuple


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_slot_identities as slot_ids


FieldElt = slot_ids.FieldElt
FieldPoly = slot_ids.FieldPoly

H32_SIZE = 32
ACTIVE_COSETS = tuple(range(1, 8))
SLOT_BLOCK_SIZE = 16
SLOT_CHOICES_PER_COSET = 3 * 16
COSUPPORT_SIZE = 1 + len(ACTIVE_COSETS) * SLOT_BLOCK_SIZE
ALL_TUPLE_COUNT = SLOT_CHOICES_PER_COSET ** len(ACTIVE_COSETS)


def field_poly_mul(a: Sequence[FieldElt], b: Sequence[FieldElt]) -> FieldPoly:
    if not a or not b:
        return []
    out = [slot_ids.ZERO] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = slot_ids.fadd(out[i + j], slot_ids.fmul(ai, bj))
    while len(out) > 1 and out[-1] == slot_ids.ZERO:
        out.pop()
    return out


def h32_elements() -> Tuple[FieldElt, ...]:
    return tuple(slot_ids.fpow(slot_ids.ETA, 8 * index) for index in range(H32_SIZE))


def d0_elements() -> Set[FieldElt]:
    return {slot_ids.fpow(slot_ids.ETA, exponent) for exponent in range(256)}


def coset_elements(t: int, h32: Iterable[FieldElt]) -> Set[FieldElt]:
    eta_t = slot_ids.fpow(slot_ids.ETA, t)
    return {slot_ids.fmul(eta_t, y) for y in h32}


def y_set(seed: int, shift: int, h32: Iterable[FieldElt]) -> Set[FieldElt]:
    target_squares = {
        slot_ids.emb(pow(3, exponent, slot_ids.P))
        for exponent in slot_ids.b_set(seed, shift)
    }
    return {y for y in h32 if slot_ids.fpow(y, 2) in target_squares}


def active_block(t: int, seed: int, shift: int, h32: Iterable[FieldElt]) -> Set[FieldElt]:
    eta_t = slot_ids.fpow(slot_ids.ETA, t)
    return {slot_ids.fmul(eta_t, y) for y in y_set(seed, shift, h32)}


def locator_product_from_blocks(
    tuple_choices: Sequence[Tuple[int, int]],
    h32: Iterable[FieldElt],
) -> Tuple[Set[FieldElt], FieldPoly, FieldPoly]:
    if len(tuple_choices) != len(ACTIVE_COSETS):
        raise AssertionError("expected one (seed, shift) choice for each active coset")

    roots = {slot_ids.ONE}
    product = slot_ids.poly_from_roots([slot_ids.ONE])
    for t, (seed, shift) in zip(ACTIVE_COSETS, tuple_choices):
        block = active_block(t, seed, shift, h32)
        roots.update(block)
        product = field_poly_mul(product, slot_ids.poly_from_roots(sorted(block)))

    direct = slot_ids.poly_from_roots(sorted(roots))
    return roots, product, direct


def build_report() -> Dict[str, Any]:
    h32 = h32_elements()
    d0 = d0_elements()
    cosets = {t: coset_elements(t, h32) for t in range(8)}

    y_sets: Dict[Tuple[int, int], Set[FieldElt]] = {
        (seed, shift): y_set(seed, shift, h32)
        for seed in (1, 2, 3)
        for shift in range(16)
    }
    active_blocks: Dict[Tuple[int, int, int], Set[FieldElt]] = {
        (t, seed, shift): active_block(t, seed, shift, h32)
        for t in ACTIVE_COSETS
        for seed in (1, 2, 3)
        for shift in range(16)
    }

    representative_tuples = [
        tuple((1, 0) for _ in ACTIVE_COSETS),
        tuple((2, 7) for _ in ACTIVE_COSETS),
        tuple(((t % 3) + 1, (5 * t) % 16) for t in ACTIVE_COSETS),
    ]
    representative_checks = []
    for choices in representative_tuples:
        roots, product, direct = locator_product_from_blocks(choices, h32)
        representative_checks.append(
            {
                "choices": [
                    {"t": t, "seed": seed, "shift": shift}
                    for t, (seed, shift) in zip(ACTIVE_COSETS, choices)
                ],
                "root_count": len(roots),
                "locator_degree": len(product) - 1,
                "direct_locator_degree": len(direct) - 1,
                "product_matches_direct_locator": product == direct,
            }
        )

    checks = {
        "eta_order_256": slot_ids.fpow(slot_ids.ETA, 256) == slot_ids.ONE
        and slot_ids.fpow(slot_ids.ETA, 128) != slot_ids.ONE,
        "D0_size_256": len(d0) == 256,
        "H32_size_32": len(set(h32)) == H32_SIZE,
        "H32_subset_D0": set(h32).issubset(d0),
        "eight_cosets_partition_D0": set().union(*cosets.values()) == d0,
        "eight_cosets_disjoint": all(
            cosets[left].isdisjoint(cosets[right])
            for left in range(8)
            for right in range(left)
        ),
        "singleton_one_in_inactive_coset": slot_ids.ONE in cosets[0],
        "singleton_one_not_in_active_cosets": all(
            slot_ids.ONE not in cosets[t] for t in ACTIVE_COSETS
        ),
        "all_Y_sets_have_size_16": all(
            len(values) == SLOT_BLOCK_SIZE for values in y_sets.values()
        ),
        "all_Y_sets_subset_H32": all(
            values.issubset(set(h32)) for values in y_sets.values()
        ),
        "all_48_Y_sets_distinct": (
            len({frozenset(values) for values in y_sets.values()})
            == SLOT_CHOICES_PER_COSET
        ),
        "slot_block_count_336": len(active_blocks) == 7 * SLOT_CHOICES_PER_COSET,
        "all_active_blocks_have_size_16": all(
            len(values) == SLOT_BLOCK_SIZE for values in active_blocks.values()
        ),
        "all_active_blocks_in_expected_coset": all(
            values.issubset(cosets[t])
            for (t, _seed, _shift), values in active_blocks.items()
        ),
        "active_blocks_disjoint_from_singleton": all(
            slot_ids.ONE not in values for values in active_blocks.values()
        ),
        "active_cosets_pairwise_disjoint": all(
            cosets[left].isdisjoint(cosets[right])
            for left in ACTIVE_COSETS
            for right in ACTIVE_COSETS
            if left < right
        ),
        "cosupport_size_formula_113": COSUPPORT_SIZE == 113,
        "all_representative_locator_products_match": all(
            item["root_count"] == COSUPPORT_SIZE
            and item["locator_degree"] == COSUPPORT_SIZE
            and item["direct_locator_degree"] == COSUPPORT_SIZE
            and item["product_matches_direct_locator"]
            for item in representative_checks
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / FINITE-MODEL-SLOT-ASSEMBLY-VERIFIED",
        "theorem_problem_id": "M1 Cycle116 slot-block co-support assembly",
        "assembly": {
            "field": "F_17[X]/(X^16+X^8+3)",
            "native_domain": "D0=<eta>",
            "native_domain_size": len(d0),
            "inactive_coset": "eta^0 H32 contains singleton {1}",
            "active_cosets": list(ACTIVE_COSETS),
            "subcoset_size": H32_SIZE,
            "slot_choices_per_active_coset": SLOT_CHOICES_PER_COSET,
            "slot_block_size": SLOT_BLOCK_SIZE,
            "slot_block_count": len(active_blocks),
            "cosupport_formula": "1 + 7*16",
            "cosupport_size": COSUPPORT_SIZE,
            "all_tuple_count": ALL_TUPLE_COUNT,
            "all_tuple_size_proof": (
                "one singleton in eta^0 H32 plus one 16-point block in each "
                "pairwise-disjoint active coset eta^t H32, t=1,...,7"
            ),
        },
        "representative_locator_checks": representative_checks,
        "checks": checks,
        "imports_required": [
            "Cycle116 slot identity replay for the fixed-jet and evaluation identities",
            "source comparison that the external Cycle116 packet uses this co-support",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    assembly = report["assembly"]
    print("m1_cycle116_slot_assembly: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "assembly="
        f"D0_size={assembly['native_domain_size']}, "
        f"active_cosets={assembly['active_cosets']}, "
        f"slot_blocks={assembly['slot_block_count']}, "
        f"block_size={assembly['slot_block_size']}, "
        f"cosupport_size={assembly['cosupport_size']}"
    )
    print(f"all_tuple_count={assembly['all_tuple_count']}")
    print(f"all_tuple_size_proof={assembly['all_tuple_size_proof']}")
    print(
        "representative_locator_checks="
        + ", ".join(
            f"degree {item['locator_degree']} match={item['product_matches_direct_locator']}"
            for item in report["representative_locator_checks"]
        )
    )
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the Cycle116 slot-block co-support assembly."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
