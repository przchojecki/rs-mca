#!/usr/bin/env python3
"""Replay the full-outside carrier compiler on the active six-owner reserve."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1 as active
import verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1 as legacy

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-active-carrier-incidence-replay-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_active_carrier_incidence_replay_v1.schema.json"
)

ARCH = active.ARCH
PARTITION_DIGEST = active.partition()["partition_sha256"]
B_REMAINING = active.REMAINING
SCAN_R_MIN = active.FROBENIUS_DEGREE + 1
SCAN_R_MAX = legacy.SCAN_R_MAX

PAID_ONE_CUT = "PAID_ACTIVE_FULL_OUTSIDE_RICH_PENCIL_CARRIER_ONE_CUT"
PAID_COARSE = "PAID_ACTIVE_FULL_OUTSIDE_M2B_COARSE_CARRIER"
OPEN = (
    "UNPAID_ACTIVE_FULL_OUTSIDE_LOW_X_DETERMINANT_PACKING_"
    "SLACK_67467_TO_236112"
)
EXPECTED_INTERVALS = [
    [9_209, 67_466, PAID_ONE_CUT],
    [67_467, 236_112, OPEN],
    [236_113, 330_348, PAID_ONE_CUT],
    [330_349, 913_631, PAID_COARSE],
]
EXPECTED_COUNTS = {
    PAID_ONE_CUT: 152_494,
    PAID_COARSE: 583_283,
    OPEN: 168_646,
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_c5_twist_frobenius9208_adapter_v1.md"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-c5-twist-frobenius9208-adapter-v1/manifest.json"
    ),
    (
        "experimental/notes/m1/"
        "m1_kb_rank9_full_outside_carrier_incidence_splice_v1.md"
    ),
    (
        "experimental/scripts/"
        "verify_m1_kb_rank9_full_outside_carrier_incidence_splice_v1.py"
    ),
    (
        "experimental/data/certificates/"
        "m1-kb-rank9-full-outside-carrier-incidence-splice-v1/"
        "m1_kb_rank9_full_outside_carrier_incidence_splice_v1.json"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_active_carrier_incidence_replay_v1.md"
    ),
]

Failure = active.Failure
need = active.need
seal = active.seal
dump = active.dump
load = active.load
file_digest = active.file_digest


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def source_bindings() -> list[dict[str, str]]:
    result = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        result.append(
            {
                "binding_id": (
                    f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}"
                ),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return result


def source_size(r: int) -> int:
    return legacy.T + r + 1


def carrier_size(r: int) -> int:
    return legacy.N - source_size(r)


def x_floor(r: int) -> int:
    return (source_size(r) + 1) // 2 - r


def line_cap(r: int) -> int:
    floor = x_floor(r)
    return 1 + legacy.J // floor if floor >= 1 else legacy.J + 1


def coarse_cap(r: int) -> int:
    return math.comb(carrier_size(r), legacy.SELECTOR_RANK) // legacy.MU_ZERO


def one_cut_tail(r: int) -> int:
    ambient = math.comb(carrier_size(r), legacy.SELECTOR_RANK)
    need(ambient // legacy.MU_ZERO > B_REMAINING, "coarse branch")
    excess = ambient + 1 - (B_REMAINING + 1) * legacy.MU_ZERO
    required_high = max(0, (excess + legacy.MU_GAIN - 1) // legacy.MU_GAIN)
    result = B_REMAINING + 1 - required_high
    need(result >= 0, "no useful one-cut threshold")
    return result


def low_deficit_cap(r: int) -> int:
    return (
        line_cap(r)
        * math.comb(carrier_size(r), legacy.CORE_RANK)
        // legacy.CORE_BASIS_COUNT
    )


def terminal(r: int) -> str:
    if coarse_cap(r) <= B_REMAINING:
        return PAID_COARSE
    return PAID_ONE_CUT if low_deficit_cap(r) <= one_cut_tail(r) else OPEN


def endpoint(r: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "r": r,
        "source_size": source_size(r),
        "carrier_size": carrier_size(r),
        "x_floor": x_floor(r),
        "line_cap": line_cap(r),
        "coarse_cap": str(coarse_cap(r)),
        "terminal": terminal(r),
    }
    if coarse_cap(r) > B_REMAINING:
        tail = one_cut_tail(r)
        low = low_deficit_cap(r)
        result.update(
            {
                "one_cut_tail": str(tail),
                "low_deficit_cap": str(low),
                "tail_margin": str(tail - low),
            }
        )
    return result


def scan() -> dict[str, Any]:
    intervals: list[list[Any]] = []
    counts = {PAID_ONE_CUT: 0, PAID_COARSE: 0, OPEN: 0}
    row_digest = hashlib.sha256()
    route_digest = hashlib.sha256()
    interval_start = SCAN_R_MIN
    previous_terminal = terminal(SCAN_R_MIN)
    previous_r = SCAN_R_MIN

    for r in range(SCAN_R_MIN, SCAN_R_MAX + 1):
        current = terminal(r)
        counts[current] += 1
        row_digest.update(
            canonical_bytes(
                [
                    r,
                    source_size(r),
                    carrier_size(r),
                    x_floor(r),
                    line_cap(r),
                    coarse_cap(r),
                    None if coarse_cap(r) <= B_REMAINING else one_cut_tail(r),
                    None if coarse_cap(r) <= B_REMAINING else low_deficit_cap(r),
                    current,
                ]
            )
        )
        if current == OPEN:
            tail = one_cut_tail(r)
            low_count = tail + 1
            chosen_x = max(1, x_floor(r))
            chosen_e = (source_size(r) + 1) // 2
            chosen_u = chosen_e - chosen_x
            chosen_h = r - chosen_u
            line_count = (low_count + line_cap(r) - 1) // line_cap(r)
            bases_used = line_count * legacy.CORE_BASIS_COUNT
            ambient_bases = math.comb(carrier_size(r), legacy.CORE_RANK)
            need(chosen_h >= 0, "route h")
            need(chosen_u >= legacy.CUTOFF_D + 1, "route high deficit")
            need(r - (legacy.CUTOFF_D + 1) > active.FROBENIUS_DEGREE, "endpoint owner")
            need(bases_used <= ambient_bases, "route basis capacity")
            route_digest.update(
                canonical_bytes(
                    [
                        r,
                        tail,
                        low_count,
                        chosen_x,
                        chosen_e,
                        chosen_u,
                        chosen_h,
                        line_count,
                        bases_used,
                        ambient_bases,
                    ]
                )
            )
        if r > SCAN_R_MIN and current != previous_terminal:
            intervals.append([interval_start, r - 1, previous_terminal])
            interval_start = r
            previous_terminal = current
        previous_r = r
    intervals.append([interval_start, previous_r, previous_terminal])
    need(intervals == EXPECTED_INTERVALS, "interval partition")
    need(counts == EXPECTED_COUNTS, "terminal counts")
    return {
        "scan_r_min": SCAN_R_MIN,
        "scan_r_max": SCAN_R_MAX,
        "scan_count": SCAN_R_MAX - SCAN_R_MIN + 1,
        "scan_sha256": row_digest.hexdigest(),
        "route_cut_sha256": route_digest.hexdigest(),
        "intervals": intervals,
        "terminal_counts": counts,
        "endpoint_records": [
            endpoint(r)
            for r in [
                9_209,
                67_466,
                67_467,
                236_112,
                236_113,
                330_348,
                330_349,
                913_631,
            ]
        ],
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE",
            "active_ledger": {
                "U_paid": active.PAID,
                "B_remaining": B_REMAINING,
                "additional_charge": 0,
            },
            "contracts": {
                "complete_selector_rebuilt_after_active_owner_deletion": True,
                "endpoint_owner_floor_r": SCAN_R_MIN,
                "legacy_degree_195_selector_state_imported": False,
                "source_pair_and_translation_unchanged": True,
                "one_cut_formula_recomputed_at_active_budget": True,
            },
            "scan": scan(),
            "source_bindings": source_bindings(),
            "status": (
                "PROVED_ACTIVE_TWO_RANGE_FULL_OUTSIDE_CLOSURE_"
                "ZERO_ADDITIONAL_CHARGE_INTERMEDIATE_GAP_OPEN_ROW_OPEN"
            ),
        }
    )


def expected_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": True,
        "properties": {
            "architecture_id": {"const": ARCH},
            "partition_sha256": {"const": PARTITION_DIGEST},
            "payload_sha256": {"pattern": "^[0-9a-f]{64}$", "type": "string"},
        },
        "required": ["architecture_id", "partition_sha256", "payload_sha256"],
        "title": "KoalaBear active carrier-incidence replay",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_active_carrier_incidence_replay_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED ACTIVE BRANCH COMPILER",
        "9{,}209\\ldots67{,}466",
        "67{,}467\\ldots236{,}112",
        "236{,}113\\ldots330{,}348",
        "330{,}349\\ldots913{,}631",
        "274{,}961{,}102{,}171{,}022{,}152",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def check_upstream_one_cut() -> None:
    for r in [9_209, 67_466, 67_467, 236_112, 236_113, 330_348]:
        imported = legacy.TANGENT.one_cut_gate(
            B_REMAINING,
            legacy.CUTOFF_D,
            carrier_size(r),
            1,
        )
        need(
            int(imported["largest_sufficient_low_deficit_cap_T_star"])
            == one_cut_tail(r),
            f"upstream one-cut tail at r={r}",
        )
        need(
            int(imported["cap_at_T_star"]) == B_REMAINING,
            f"upstream cap at r={r}",
        )
        need(
            int(imported["cap_at_T_star_plus_1"]) == B_REMAINING + 1,
            f"upstream sharpness at r={r}",
        )


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero movement")
    need(
        cert["contracts"]["legacy_degree_195_selector_state_imported"] is False,
        "no legacy selector state",
    )
    check_upstream_one_cut()
    check_sources()


def emit() -> None:
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    mutations = [
        lambda d: d["active_ledger"].__setitem__("B_remaining", B_REMAINING + 1),
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["contracts"].__setitem__(
            "legacy_degree_195_selector_state_imported", True
        ),
        lambda d: d["scan"]["intervals"][1].__setitem__(1, 236_097),
        lambda d: d["scan"]["terminal_counts"].__setitem__(OPEN, 168_645),
    ]
    passed = 0
    for mutate in mutations:
        bad = copy.deepcopy(cert)
        mutate(bad)
        try:
            validate(bad, schema)
        except Failure:
            passed += 1
        else:
            raise Failure("tamper accepted")
    need(passed == len(mutations), "tamper count")
    print(f"tamper-selftest: PASS {passed}/{len(mutations)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.emit:
            emit()
        if args.check:
            cert = load(CERT_PATH)
            schema = load(SCHEMA_PATH)
            validate(cert, schema)
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {PARTITION_DIGEST}")
            print(f"B_remaining: {B_REMAINING}")
            print(f"intervals: {cert['scan']['intervals']}")
            print(f"scan_sha256: {cert['scan']['scan_sha256']}")
            print("check: PASS")
        if args.tamper_selftest:
            tamper_selftest()
        if not (args.emit or args.check or args.tamper_selftest):
            parser.error("choose --emit, --check, or --tamper-selftest")
    except Failure as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
