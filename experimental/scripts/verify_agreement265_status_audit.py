#!/usr/bin/env python3
"""Verify the agreement-265 finite-slope status audit."""

from __future__ import annotations

import argparse
import json
import sys
from math import comb
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

import experimental.scripts.verify_m1_coset_packet_finite_slope_floors as floors
import experimental.scripts.verify_m1_random_simple_pole_entropy_floor as random_floor


Q = 17**32
TARGET_DENOMINATOR = 2**128
GATE = Q // TARGET_DENOMINATOR
FIRST_UNSAFE_NUMERATOR = GATE + 1


def rows_by_agreement(certificate: dict[str, Any]) -> dict[int, dict[str, Any]]:
    rows: dict[int, dict[str, Any]] = {}
    for record in certificate["records"]:
        lower = int(record["badSlopesLower"])
        for agreement in range(
            int(record["agreementStart"]),
            int(record["agreementEnd"]) + 1,
        ):
            rows[agreement] = {
                "agreement": agreement,
                "lower": lower,
                "formula": record["badSlopesLowerFormula"],
                "source_start": int(record["agreementStart"]),
                "source_end": int(record["agreementEnd"]),
            }
    return rows


def random_floor_rows() -> dict[int, dict[str, Any]]:
    random_floor.check_certificate(random_floor.CERTIFICATE)
    rows: dict[int, dict[str, Any]] = {}
    for record in random_floor.computed_certificate()["records"]:
        agreement = int(record["agreement"])
        rows[agreement] = {
            "agreement": agreement,
            "lower": int(record["badSlopesLowerExact"]),
            "formula": record["badSlopesLower"],
            "source": "random simple-pole entropy floor",
        }
    return rows


def status_certificate() -> dict[str, Any]:
    floors.validate_math()
    floors.validate_json(floors.DATA_PATH)
    rows = random_floor_rows()
    coset_rows = rows_by_agreement(floors.certificate())
    overlap = sorted(set(rows) & set(coset_rows))
    if overlap:
        raise AssertionError(("overlapping source rows", overlap))
    rows.update(coset_rows)

    required_rows = list(range(257, 289))
    missing = [agreement for agreement in required_rows if agreement not in rows]
    if missing:
        raise AssertionError(("missing lower-floor rows", missing))

    weak = [
        (agreement, rows[agreement]["lower"])
        for agreement in required_rows
        if rows[agreement]["lower"] < FIRST_UNSAFE_NUMERATOR
    ]
    if weak:
        raise AssertionError(("row does not clear unsafe gate", weak))

    if GATE != 6:
        raise AssertionError(("unexpected gate", GATE))
    if FIRST_UNSAFE_NUMERATOR != 7:
        raise AssertionError(("unexpected first unsafe numerator", FIRST_UNSAFE_NUMERATOR))
    if comb(31, 16) != 300540195:
        raise AssertionError("binom(31,16) mismatch")
    if comb(16, 9) != 11440:
        raise AssertionError("binom(16,9) mismatch")
    if rows[265]["lower"] != comb(31, 16):
        raise AssertionError(("a=265 lower mismatch", rows[265]))
    if rows[288]["lower"] != comb(16, 9):
        raise AssertionError(("a=288 lower mismatch", rows[288]))
    if rows[257]["lower"] != Q:
        raise AssertionError(("a=257 lower mismatch", rows[257]))
    if rows[258]["lower"] != Q:
        raise AssertionError(("a=258 lower mismatch", rows[258]))
    if rows[259]["lower"] != Q - 68_904:
        raise AssertionError(("a=259 lower mismatch", rows[259]))

    return {
        "status": "PROVED-CONSEQUENCE / AUDIT",
        "predicate": "finite-slope support-wise LD_sw / MCA",
        "row": "RS[F_17^32,H,256]",
        "n": floors.N,
        "k": floors.K,
        "q": str(Q),
        "floor_q_over_2_128": GATE,
        "first_unsafe_numerator": FIRST_UNSAFE_NUMERATOR,
        "old_target": "LD_sw(C,265) <= 6",
        "old_target_status": "false under the finite-slope support-wise convention",
        "explicit_lower_floor_interval": [257, 288],
        "agreement_257_lower": rows[257]["lower"],
        "agreement_257_lower_formula": rows[257]["formula"],
        "agreement_259_lower": rows[259]["lower"],
        "agreement_259_lower_formula": rows[259]["formula"],
        "agreement_260_lower": rows[260]["lower"],
        "agreement_260_lower_formula": rows[260]["formula"],
        "agreement_265_lower": rows[265]["lower"],
        "agreement_265_lower_formula": rows[265]["formula"],
        "agreement_288_lower": rows[288]["lower"],
        "agreement_288_lower_formula": rows[288]["formula"],
        "certified_unsafe_agreement_interval": [257, 288],
        "monotone_unsafe_through": 288,
        "first_not_ruled_out_by_this_floor": 289,
        "nonclaims": [
            "does not prove LD_sw(C,289) <= 6",
            "does not classify all finite slopes",
            "does not count projective slopes",
            "does not change the high-agreement 506/507 threshold package",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="print JSON summary")
    args = parser.parse_args()

    cert = status_certificate()
    if args.json:
        print(json.dumps(cert, indent=2))
        return

    print("agreement-265 finite-slope status audit")
    print("q =", cert["q"])
    print("floor(q/2^128) =", cert["floor_q_over_2_128"])
    print(
        "a=257 lower =",
        cert["agreement_257_lower"],
        f"({cert['agreement_257_lower_formula']})",
    )
    print(
        "a=265 lower =",
        cert["agreement_265_lower"],
        f"({cert['agreement_265_lower_formula']})",
    )
    print(
        "a=288 lower =",
        cert["agreement_288_lower"],
        f"({cert['agreement_288_lower_formula']})",
    )
    print("old target:", cert["old_target"], "is false")
    print("first not ruled out by this floor:", cert["first_not_ruled_out_by_this_floor"])


if __name__ == "__main__":
    main()
