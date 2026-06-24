#!/usr/bin/env python3
"""Verify the Cycle120 domain-generated field ledger.

The Cycle120 row is stated over K=F_17^32 with smooth domain H=<theta> of
order 512.  For field-ledger purposes it matters that H is not merely embedded
in K: the generator theta itself should generate the full field over F_17.

This verifier checks that fact in two equivalent ways:

* ord_512(17)=32, so an element of order 512 has degree 32 over F_17;
* theta is not fixed by Frobenius x -> x^(17^d) for any proper d|32.

It also checks the native eta ledger in F_17^16.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle116_field_lift_contract as field_lift
import verify_m1_cycle116_smooth_padding_transfer as smooth_padding
import verify_m1_cycle116_slot_identities as slot_ids


BASE = 17
ETA_ORDER = 256
THETA_ORDER = 512
NATIVE_DEGREE = 16
LIFT_DEGREE = 32
PROPER_NATIVE_DEGREES = (1, 2, 4, 8)
PROPER_LIFT_DEGREES = (1, 2, 4, 8, 16)


def multiplicative_order_mod(base: int, modulus: int) -> int:
    if modulus <= 1:
        raise ValueError("modulus must be > 1")
    value = base % modulus
    order = 1
    while value != 1:
        value = (value * base) % modulus
        order += 1
        if order > modulus:
            raise AssertionError("order search failed")
    return order


def eta_frobenius(degree: int) -> slot_ids.FieldElt:
    return slot_ids.fpow(slot_ids.ETA, BASE**degree)


def theta_frobenius(degree: int) -> smooth_padding.KElt:
    return smooth_padding.kpow(smooth_padding.K_THETA, BASE**degree)


def build_report() -> Dict[str, Any]:
    field_report = field_lift.build_report()
    smooth_report = smooth_padding.build_report()

    eta_proper_fixed = {
        str(degree): eta_frobenius(degree) == slot_ids.ETA
        for degree in PROPER_NATIVE_DEGREES
    }
    theta_proper_fixed = {
        str(degree): theta_frobenius(degree) == smooth_padding.K_THETA
        for degree in PROPER_LIFT_DEGREES
    }

    checks = {
        "field_lift_contract_passes": field_report["status"] == "PASS",
        "smooth_padding_transfer_passes": smooth_report["status"] == "PASS",
        "ord_256_of_17_is_16": (
            multiplicative_order_mod(BASE, ETA_ORDER) == NATIVE_DEGREE
        ),
        "ord_512_of_17_is_32": (
            multiplicative_order_mod(BASE, THETA_ORDER) == LIFT_DEGREE
        ),
        "eta_fixed_by_17_16_frobenius": (
            eta_frobenius(NATIVE_DEGREE) == slot_ids.ETA
        ),
        "eta_not_in_proper_subfield": not any(eta_proper_fixed.values()),
        "theta_fixed_by_17_32_frobenius": (
            theta_frobenius(LIFT_DEGREE) == smooth_padding.K_THETA
        ),
        "theta_not_in_proper_subfield": not any(theta_proper_fixed.values()),
        "theta_square_recovers_eta": (
            smooth_padding.kmul(smooth_padding.K_THETA, smooth_padding.K_THETA)
            == (slot_ids.ETA, slot_ids.ZERO)
        ),
        "domain_generator_has_order_512": (
            smooth_padding.kpow(smooth_padding.K_THETA, THETA_ORDER)
            == smooth_padding.K_ONE
            and smooth_padding.kpow(smooth_padding.K_THETA, THETA_ORDER // 2)
            == smooth_padding.K_MINUS_ONE
        ),
        "field_sizes_match_ledgers": (
            int(field_report["field"]["field_size"]) == BASE**NATIVE_DEGREE
            and int(field_report["field"]["lifted_field_size"]) == BASE**LIFT_DEGREE
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "AUDIT / DOMAIN-GENERATED-FIELD-LEDGER",
        "theorem_problem_id": "M1 Cycle120 domain-generated field ledger",
        "field_ledger": {
            "base_field": "F_17",
            "native_generator": "eta",
            "native_order": ETA_ORDER,
            "native_generated_degree": NATIVE_DEGREE,
            "native_field": "F_17^16",
            "lift_generator": "theta",
            "lift_order": THETA_ORDER,
            "lift_generated_degree": LIFT_DEGREE,
            "lift_field": "F_17^32",
            "q_gen": BASE**LIFT_DEGREE,
            "q_code": BASE**LIFT_DEGREE,
            "q_line": BASE**LIFT_DEGREE,
        },
        "frobenius": {
            "eta_proper_subfield_fixed": eta_proper_fixed,
            "theta_proper_subfield_fixed": theta_proper_fixed,
            "eta_fixed_at_degree_16": True,
            "theta_fixed_at_degree_32": True,
        },
        "checks": checks,
        "imports_required": [
            "Cycle116 field/lift contract",
            "Cycle116 smooth-padding domain decomposition",
            "official ABF source gate verification for prize-facing use",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    ledger = report["field_ledger"]

    print("m1_cycle120_domain_field_ledger: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "native="
        f"{ledger['native_generator']} order {ledger['native_order']} "
        f"generates {ledger['native_field']} over {ledger['base_field']}"
    )
    print(
        "lift="
        f"{ledger['lift_generator']} order {ledger['lift_order']} "
        f"generates {ledger['lift_field']} over {ledger['base_field']}"
    )
    print(
        "ledgers="
        f"q_gen=q_code=q_line={ledger['q_gen']}"
    )
    print("imports_required=" + "; ".join(report["imports_required"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the Cycle120 domain-generated field ledger."
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
