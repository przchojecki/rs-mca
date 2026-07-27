#!/usr/bin/env python3
"""Replay the histogram after the reciprocal-kernel interval sweep."""

from __future__ import annotations

import argparse
import copy
import hashlib
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_post_second_successor_full_histogram_replay_v1 as old
import verify_kb_mca_v4_reciprocal_kernel_plane_sweep_v1 as sweep

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-post-reciprocal-kernel-plane-sweep-full-histogram-replay-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_post_reciprocal_kernel_plane_sweep_full_histogram_replay_v1.schema.json"
)

ARCH = sweep.ARCH
PARTITION_DIGEST = sweep.PARTITION_DIGEST
B_REMAINING = old.B_REMAINING

HISTOGRAM_PAID = old.HISTOGRAM_PAID
FIRST_GAP_OWNER = old.FIRST_GAP_OWNER
NEXT_SLACK_THEOREM = old.NEXT_SLACK_THEOREM
SUCCESSOR_THEOREM = old.SUCCESSOR_THEOREM
SECOND_SUCCESSOR_THEOREM = old.SECOND_SUCCESSOR_THEOREM
RECIPROCAL_KERNEL_SWEEP = (
    "PAID_RECIPROCAL_KERNEL_PLANE_SWEEP_ZERO_CHARGE"
)
OPEN = (
    "UNPAID_ACTIVE_FULL_OUTSIDE_SOURCE_COUPLED_PACKING_"
    "SLACK_134943_TO_213050"
)

EXPECTED_INTERVALS = [
    [old.old.old.old.SCAN_R_MIN, 67_470, HISTOGRAM_PAID],
    [67_471, 67_471, FIRST_GAP_OWNER],
    [67_472, 67_472, NEXT_SLACK_THEOREM],
    [67_473, 67_473, SUCCESSOR_THEOREM],
    [67_474, 67_474, SECOND_SUCCESSOR_THEOREM],
    [67_475, 134_942, RECIPROCAL_KERNEL_SWEEP],
    [134_943, 213_050, OPEN],
    [213_051, old.old.old.old.SCAN_R_MAX, HISTOGRAM_PAID],
]
EXPECTED_COUNTS = {
    HISTOGRAM_PAID: 758_843,
    FIRST_GAP_OWNER: 1,
    NEXT_SLACK_THEOREM: 1,
    SUCCESSOR_THEOREM: 1,
    SECOND_SUCCESSOR_THEOREM: 1,
    RECIPROCAL_KERNEL_SWEEP: 67_468,
    OPEN: 78_108,
}

Failure = old.Failure
need = old.need
seal = old.seal
dump = old.dump
load = old.load
file_digest = old.file_digest
canonical_bytes = old.canonical_bytes

UPSTREAM_CERTIFICATES = {
    "post_second_successor_histogram": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-post-second-successor-full-histogram-replay-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'b0212943d8dfe070c0d36cc9105c52ca60b5380d47b07eb4c1f9e560ade99fd9'
        ),
    },
    "reciprocal_kernel_plane_sweep": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-reciprocal-kernel-plane-sweep-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            'dabd61e2242b5ec6ec5b19ce8966b8375cae5624091768b6c5cbc4dabdf4984c'
        ),
    },
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_second_successor_full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_reciprocal_kernel_plane_sweep_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_reciprocal_kernel_plane_sweep_full_histogram_replay_v1.md"
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
    if sweep.R_MIN <= r <= sweep.R_MAX:
        return RECIPROCAL_KERNEL_SWEEP
    inherited = old.terminal(r)
    return OPEN if inherited == old.OPEN else inherited


def endpoint(r: int) -> dict[str, Any]:
    record = old.endpoint(r)
    record["terminal"] = terminal(r)
    return record


def route_record(r: int) -> list[Any]:
    need(134_943 <= r <= 213_050, "route outside current gap")
    need(terminal(r) == OPEN, "route is paid")
    return old.route_record(r)


def scan() -> dict[str, Any]:
    scan_r_min = old.old.old.old.SCAN_R_MIN
    scan_r_max = old.old.old.old.SCAN_R_MAX
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
                    old.old.old.old.source_size(r),
                    old.old.old.old.carrier_size(r),
                    old.old.old.old.x_floor(r),
                    old.old.old.old.line_cap(r),
                    old.old.old.old.histogram_cap(r),
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
    need(route_count == 78_108, "route count")
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
                134_942,
                134_943,
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
                "U_paid": sweep.upper.plane.active.PAID,
                "B_remaining": B_REMAINING,
                "additional_charge": 0,
            },
            "contracts": {
                "complete_selector_rebuilt_after_seven_owner_deletion": True,
                "post_second_successor_histogram_bound": True,
                "reciprocal_kernel_plane_theorem_bound": True,
                "reciprocal_kernel_interval_paid_with_zero_additional_charge": True,
                "first_open_slack_is_strict_equality_boundary": True,
                "legacy_selector_state_imported": False,
                "full_histogram_recomputed_at_unchanged_reserve": True,
            },
            "scan": scan(),
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_POST_RECIPROCAL_KERNEL_PLANE_SWEEP_"
                "FULL_HISTOGRAM_REPLAY_OPEN_INTERVAL_"
                "134943_TO_213050_ROW_OPEN"
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
        "title": (
            "KoalaBear post-reciprocal-kernel-plane-sweep "
            "full-histogram replay"
        ),
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_reciprocal_kernel_plane_sweep_"
        "full_histogram_replay_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED RECIPROCAL-KERNEL SWEEP REPLAY",
        "134,943..213,050",
        "78,108",
        "67,475..134,942",
        "strict equality boundary",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(
        cert["contracts"]["post_second_successor_histogram_bound"] is True,
        "post-second-successor replay",
    )
    need(
        cert["contracts"]["reciprocal_kernel_plane_theorem_bound"] is True,
        "sweep theorem",
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
            "post_second_successor_histogram_bound", False
        ),
        lambda d: d["contracts"].__setitem__(
            "reciprocal_kernel_plane_theorem_bound", False
        ),
        lambda d: d["contracts"].__setitem__(
            "reciprocal_kernel_interval_paid_with_zero_additional_charge",
            False,
        ),
        lambda d: d["contracts"].__setitem__(
            "legacy_selector_state_imported", True
        ),
        lambda d: d["contracts"].__setitem__(
            "first_open_slack_is_strict_equality_boundary", False
        ),
        lambda d: d["scan"]["intervals"][5].__setitem__(1, 134_943),
        lambda d: d["scan"].__setitem__("route_cut_count", 78_109),
        lambda d: d["upstream_certificates"][
            "reciprocal_kernel_plane_sweep"
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
