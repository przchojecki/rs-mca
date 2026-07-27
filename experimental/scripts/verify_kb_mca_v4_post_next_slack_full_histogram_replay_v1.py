#!/usr/bin/env python3
"""Replay the full histogram after the zero-charge r=67,472 theorem."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_next_slack_source_plane_closure_v1 as closure
import verify_kb_mca_v4_post_first_gap_full_histogram_replay_v1 as old

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-post-next-slack-full-histogram-replay-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_post_next_slack_full_histogram_replay_v1.schema.json"
)

ARCH = closure.ARCH
PARTITION_DIGEST = closure.PARTITION_DIGEST
B_REMAINING = closure.active.REMAINING

HISTOGRAM_PAID = old.HISTOGRAM_PAID
FIRST_GAP_OWNER = old.FIRST_GAP_OWNER
NEXT_SLACK_THEOREM = "PAID_NEXT_SLACK_SOURCE_PLANE_ZERO_CHARGE"
OPEN = (
    "UNPAID_ACTIVE_FULL_OUTSIDE_SOURCE_COUPLED_PACKING_"
    "SLACK_67473_TO_213050"
)

EXPECTED_INTERVALS = [
    [old.SCAN_R_MIN, 67_470, HISTOGRAM_PAID],
    [67_471, 67_471, FIRST_GAP_OWNER],
    [67_472, 67_472, NEXT_SLACK_THEOREM],
    [67_473, 213_050, OPEN],
    [213_051, old.SCAN_R_MAX, HISTOGRAM_PAID],
]
EXPECTED_COUNTS = {
    HISTOGRAM_PAID: 758_843,
    FIRST_GAP_OWNER: 1,
    NEXT_SLACK_THEOREM: 1,
    OPEN: 145_578,
}

Failure = closure.Failure
need = closure.need
seal = closure.seal
dump = closure.dump
load = closure.load
file_digest = closure.file_digest

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_first_gap_full_histogram_replay_v1.md"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-post-first-gap-full-histogram-replay-v1/"
        "certificate.json"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_next_slack_source_plane_closure_v1.md"
    ),
    (
        "experimental/data/certificates/"
        "kb-mca-v4-next-slack-source-plane-closure-v1/"
        "certificate.json"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_next_slack_full_histogram_replay_v1.md"
    ),
]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def source_bindings() -> list[dict[str, str]]:
    bindings = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        bindings.append(
            {
                "binding_id": (
                    f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}"
                ),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return bindings


def terminal(r: int) -> str:
    if r == 67_471:
        return FIRST_GAP_OWNER
    if r == 67_472:
        return NEXT_SLACK_THEOREM
    return (
        HISTOGRAM_PAID
        if old.histogram_cap(r) <= B_REMAINING
        else OPEN
    )


def endpoint(r: int) -> dict[str, Any]:
    cap = old.histogram_cap(r)
    return {
        "r": r,
        "source_size": old.source_size(r),
        "carrier_size": old.carrier_size(r),
        "x_floor": old.x_floor(r),
        "line_cap": old.line_cap(r),
        "full_histogram_cap": str(cap),
        "budget_minus_cap": str(B_REMAINING - cap),
        "terminal": terminal(r),
    }


def route_record(r: int) -> list[Any]:
    need(67_473 <= r <= 213_050, "route outside current gap")
    need(terminal(r) == OPEN, "route is paid")
    return old.route_record(r)


def scan() -> dict[str, Any]:
    intervals: list[list[Any]] = []
    counts = {key: 0 for key in EXPECTED_COUNTS}
    scan_digest = hashlib.sha256()
    route_digest = hashlib.sha256()
    interval_start = old.SCAN_R_MIN
    previous_terminal = terminal(old.SCAN_R_MIN)
    previous_r = old.SCAN_R_MIN
    route_count = 0

    for r in range(old.SCAN_R_MIN, old.SCAN_R_MAX + 1):
        current = terminal(r)
        counts[current] += 1
        scan_digest.update(
            canonical_bytes(
                [
                    r,
                    old.source_size(r),
                    old.carrier_size(r),
                    old.x_floor(r),
                    old.line_cap(r),
                    old.histogram_cap(r),
                    current,
                ]
            )
        )
        if current == OPEN:
            route_digest.update(canonical_bytes(route_record(r)))
            route_count += 1
        if r > old.SCAN_R_MIN and current != previous_terminal:
            intervals.append([interval_start, r - 1, previous_terminal])
            interval_start = r
            previous_terminal = current
        previous_r = r
    intervals.append([interval_start, previous_r, previous_terminal])

    need(intervals == EXPECTED_INTERVALS, "interval partition")
    need(counts == EXPECTED_COUNTS, "terminal counts")
    need(route_count == 145_578, "route count")
    return {
        "scan_r_min": old.SCAN_R_MIN,
        "scan_r_max": old.SCAN_R_MAX,
        "scan_count": old.SCAN_R_MAX - old.SCAN_R_MIN + 1,
        "scan_sha256": scan_digest.hexdigest(),
        "route_cut_sha256": route_digest.hexdigest(),
        "route_cut_count": route_count,
        "intervals": intervals,
        "terminal_counts": counts,
        "endpoint_records": [
            endpoint(r)
            for r in [
                9_209,
                67_470,
                67_471,
                67_472,
                67_473,
                213_050,
                213_051,
                913_631,
            ]
        ],
    }


def expected_certificate() -> dict[str, Any]:
    upstream = load(closure.CERT_PATH)
    need(
        upstream["payload_sha256"]
        == 'e4d51dcaea7ba2591ca314ecd73248fe0a79e07244176dab8b20c78d8d1e4064',
        "next-slack payload",
    )
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE",
            "active_ledger": {
                "U_paid": closure.active.PAID,
                "B_remaining": B_REMAINING,
                "additional_charge": 0,
            },
            "contracts": {
                "complete_selector_rebuilt_after_seven_owner_deletion": True,
                "first_gap_paid_by_source_pencil_owner": True,
                "next_slack_paid_by_zero_charge_source_plane_theorem": True,
                "legacy_selector_state_imported": False,
                "full_histogram_recomputed_at_unchanged_reserve": True,
            },
            "scan": scan(),
            "source_bindings": source_bindings(),
            "status": (
                "PROVED_POST_NEXT_SLACK_FULL_HISTOGRAM_REPLAY_"
                "HIGHER_SOURCE_GAP_OPEN_ROW_OPEN"
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
        "title": "KoalaBear post-next-slack full-histogram replay",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_next_slack_full_histogram_replay_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED ZERO-CHARGE BRANCH REPLAY",
        "67,473..213,050",
        "145,578",
        "-893,351,646,969",
        "299,103,637,240",
        "four-dimensional source",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["contracts"][
            "next_slack_paid_by_zero_charge_source_plane_theorem"
        ]
        is True,
        "next-slack theorem",
    )
    need(
        cert["contracts"]["legacy_selector_state_imported"] is False,
        "no selector import",
    )
    check_sources()


def emit() -> None:
    CERT.mkdir(parents=True, exist_ok=True)
    dump(CERT_PATH, expected_certificate())
    dump(SCHEMA_PATH, expected_schema())


def tamper_selftest() -> None:
    cert = expected_certificate()
    schema = expected_schema()
    validate(cert, schema)
    mutations = [
        lambda d: d["active_ledger"].__setitem__("B_remaining", B_REMAINING + 1),
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["contracts"].__setitem__(
            "next_slack_paid_by_zero_charge_source_plane_theorem", False
        ),
        lambda d: d["contracts"].__setitem__(
            "legacy_selector_state_imported", True
        ),
        lambda d: d["scan"]["intervals"][3].__setitem__(0, 67_472),
        lambda d: d["scan"].__setitem__("route_cut_count", 145_579),
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
            print(f"route_cut_sha256: {cert['scan']['route_cut_sha256']}")
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
