#!/usr/bin/env python3
"""Replay the full histogram after the zero-charge r=67,474 theorem."""

from __future__ import annotations

import argparse
import copy
import hashlib
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_post_successor_full_histogram_replay_v1 as old
import verify_kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1 as upper

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-post-second-successor-full-histogram-replay-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_post_second_successor_full_histogram_replay_v1.schema.json"
)

ARCH = upper.ARCH
PARTITION_DIGEST = upper.PARTITION_DIGEST
B_REMAINING = old.B_REMAINING

HISTOGRAM_PAID = old.HISTOGRAM_PAID
FIRST_GAP_OWNER = old.FIRST_GAP_OWNER
NEXT_SLACK_THEOREM = old.NEXT_SLACK_THEOREM
SUCCESSOR_THEOREM = old.SUCCESSOR_THEOREM
SECOND_SUCCESSOR_THEOREM = (
    "PAID_SECOND_SUCCESSOR_SOURCE_PLANES_AND_"
    "INTRINSIC_RELATIONS_ZERO_CHARGE"
)
OPEN = (
    "UNPAID_ACTIVE_FULL_OUTSIDE_SOURCE_COUPLED_PACKING_"
    "SLACK_67475_TO_213050"
)

EXPECTED_INTERVALS = [
    [old.old.old.SCAN_R_MIN, 67_470, HISTOGRAM_PAID],
    [67_471, 67_471, FIRST_GAP_OWNER],
    [67_472, 67_472, NEXT_SLACK_THEOREM],
    [67_473, 67_473, SUCCESSOR_THEOREM],
    [67_474, 67_474, SECOND_SUCCESSOR_THEOREM],
    [67_475, 213_050, OPEN],
    [213_051, old.old.old.SCAN_R_MAX, HISTOGRAM_PAID],
]
EXPECTED_COUNTS = {
    HISTOGRAM_PAID: 758_843,
    FIRST_GAP_OWNER: 1,
    NEXT_SLACK_THEOREM: 1,
    SUCCESSOR_THEOREM: 1,
    SECOND_SUCCESSOR_THEOREM: 1,
    OPEN: 145_576,
}

Failure = old.Failure
need = old.need
seal = old.seal
dump = old.dump
load = old.load
file_digest = old.file_digest
canonical_bytes = old.old.canonical_bytes

UPSTREAM_CERTIFICATES = {
    "post_successor_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-successor-full-histogram-replay-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'ae88f5c221aabda5df2c221c85b3b91a32b88a1179a0f289be1ad470a0c880eb'
        ),
    },
    "second_successor_lower_strata": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-second-successor-lower-source-plane-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'fdeb2f6101420ad6f0e5e4bec6bb5d917980ecfa7d84aee52e92f74a1265526a'
        ),
    },
    "second_successor_upper_stratum": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-second-successor-upper-intrinsic-plane-descent-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '3e7f870adb5f39d5766ffda0cdc3ee248a8f8e0892099734c442e035ed07c177'
        ),
    },
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_successor_full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_lower_source_plane_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_upper_intrinsic_plane_descent_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_second_successor_full_histogram_replay_v1.md"
    ),
]


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


def upstream_bindings() -> dict[str, dict[str, str]]:
    bindings = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        payload = load(path)
        need(
            payload.get("payload_sha256") == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        bindings[key] = {**contract, "file_sha256": file_digest(path)}
    return bindings


def terminal(r: int) -> str:
    if r == 67_474:
        return SECOND_SUCCESSOR_THEOREM
    inherited = old.terminal(r)
    return OPEN if inherited == old.OPEN else inherited


def endpoint(r: int) -> dict[str, Any]:
    record = old.endpoint(r)
    record["terminal"] = terminal(r)
    return record


def route_record(r: int) -> list[Any]:
    need(67_475 <= r <= 213_050, "route outside current gap")
    need(terminal(r) == OPEN, "route is paid")
    return old.route_record(r)


def scan() -> dict[str, Any]:
    scan_r_min = old.old.old.SCAN_R_MIN
    scan_r_max = old.old.old.SCAN_R_MAX
    intervals: list[list[Any]] = []
    counts = {key: 0 for key in EXPECTED_COUNTS}
    scan_digest = hashlib.sha256()
    route_digest = hashlib.sha256()
    interval_start = scan_r_min
    previous_terminal = terminal(scan_r_min)
    previous_r = scan_r_min
    route_count = 0

    for r in range(scan_r_min, scan_r_max + 1):
        current = terminal(r)
        counts[current] += 1
        scan_digest.update(
            canonical_bytes(
                [
                    r,
                    old.old.old.source_size(r),
                    old.old.old.carrier_size(r),
                    old.old.old.x_floor(r),
                    old.old.old.line_cap(r),
                    old.old.old.histogram_cap(r),
                    current,
                ]
            )
        )
        if current == OPEN:
            route_digest.update(canonical_bytes(route_record(r)))
            route_count += 1
        if r > scan_r_min and current != previous_terminal:
            intervals.append([interval_start, r - 1, previous_terminal])
            interval_start = r
            previous_terminal = current
        previous_r = r
    intervals.append([interval_start, previous_r, previous_terminal])

    need(intervals == EXPECTED_INTERVALS, "interval partition")
    need(counts == EXPECTED_COUNTS, "terminal counts")
    need(route_count == 145_576, "route count")
    return {
        "scan_r_min": scan_r_min,
        "scan_r_max": scan_r_max,
        "scan_count": scan_r_max - scan_r_min + 1,
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
                67_474,
                67_475,
                213_050,
                213_051,
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
                "U_paid": upper.plane.active.PAID,
                "B_remaining": B_REMAINING,
                "additional_charge": 0,
            },
            "contracts": {
                "complete_selector_rebuilt_after_seven_owner_deletion": True,
                "second_successor_lower_strata_paid": True,
                "second_successor_upper_stratum_paid": True,
                "second_successor_slack_paid_with_zero_additional_charge": True,
                "legacy_selector_state_imported": False,
                "full_histogram_recomputed_at_unchanged_reserve": True,
            },
            "scan": scan(),
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_POST_SECOND_SUCCESSOR_FULL_HISTOGRAM_REPLAY_"
                "OPEN_INTERVAL_67475_TO_213050_ROW_OPEN"
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
        "title": "KoalaBear post-second-successor full-histogram replay",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_second_successor_full_histogram_replay_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED SECOND-SUCCESSOR ZERO-CHARGE REPLAY",
        "67,475..213,050",
        "145,576",
        "cubic relation kernel",
        "saturated rank-two kernel",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["contracts"]["second_successor_lower_strata_paid"] is True,
        "lower theorem",
    )
    need(
        cert["contracts"]["second_successor_upper_stratum_paid"] is True,
        "upper theorem",
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
            "second_successor_lower_strata_paid", False
        ),
        lambda d: d["contracts"].__setitem__(
            "second_successor_upper_stratum_paid", False
        ),
        lambda d: d["contracts"].__setitem__(
            "second_successor_slack_paid_with_zero_additional_charge", False
        ),
        lambda d: d["contracts"].__setitem__(
            "legacy_selector_state_imported", True
        ),
        lambda d: d["scan"]["intervals"][5].__setitem__(0, 67_474),
        lambda d: d["scan"].__setitem__("route_cut_count", 145_577),
        lambda d: d["upstream_certificates"][
            "second_successor_upper_stratum"
        ].__setitem__("payload_sha256", "0" * 64),
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
