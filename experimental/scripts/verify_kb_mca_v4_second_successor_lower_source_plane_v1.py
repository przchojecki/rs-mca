#!/usr/bin/env python3
"""Verify the r=67,474 lower source-plane payments."""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_next_slack_source_plane_closure_v1 as plane
import verify_kb_mca_v4_post_successor_full_histogram_replay_v1 as replay

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-second-successor-lower-source-plane-v1"
)
CERT_PATH = CERT / "certificate.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_second_successor_lower_source_plane_v1.schema.json"
)

ARCH = replay.ARCH
PARTITION_DIGEST = replay.PARTITION_DIGEST
R = 67_474
X = 0
S = plane.pencil.T + R + 1
E = (S + 1) // 2
CARRIER = plane.pencil.N - S
COMPLEMENT = plane.pencil.J + X
ZERO_LOCATOR = CARRIER - COMPLEMENT
FORCED_COMMON = plane.pencil.A_AGREEMENT - X - S
DIRECT_CAP = (plane.active.prev.BASE_PRIME + 1) * CARRIER
MARGIN = replay.B_REMAINING - DIRECT_CAP

Failure = replay.Failure
need = replay.need
seal = replay.seal
dump = replay.dump
load = replay.load
file_digest = replay.file_digest

UPSTREAM_CERTIFICATES = {
    "source_plane_theorem": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-next-slack-source-plane-closure-v1/certificate.json"
        ),
        "payload_sha256": (
            'e4d51dcaea7ba2591ca314ecd73248fe0a79e07244176dab8b20c78d8d1e4064'
        ),
    },
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
}

SOURCE_PATHS = [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_next_slack_source_plane_closure_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_post_successor_full_histogram_replay_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_lower_source_plane_v1.md"
    ),
]


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


def upstream_bindings() -> dict[str, dict[str, str]]:
    result = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        payload = load(path)
        need(
            payload.get("payload_sha256") == contract["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )
        result[key] = {**contract, "file_sha256": file_digest(path)}
    return result


def deployed_arithmetic() -> dict[str, Any]:
    need(S == 134_947, "source size")
    need(E == 67_474, "reduced degree")
    need(S == 2 * E - 1, "source-plane identity")
    need(2 * (E + 1) - S == 3, "source dimension")
    need(FORCED_COMMON == plane.pencil.K - 1 - E, "complete forced gcd")
    need(FORCED_COMMON == ZERO_LOCATOR, "split zero locator")
    need(DIRECT_CAP == 4_180_882_818_326_970, "direct cap")
    need(MARGIN == 266_599_330_142_248_910, "reserve margin")
    return {
        "r": R,
        "x": X,
        "source_size": S,
        "reduced_degree": E,
        "source_dimension": 3,
        "carrier_size": CARRIER,
        "complement_size": COMPLEMENT,
        "zero_locator_size": ZERO_LOCATOR,
        "forced_common_root_size": FORCED_COMMON,
        "direct_cap": DIRECT_CAP,
        "reserve_margin": MARGIN,
    }


def expected_certificate() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "partition_sha256": PARTITION_DIGEST,
            "counted_object": (
                "R=67474 FULL-OUTSIDE COEFFICIENT-RANK-TWO LINES WITH X=0"
            ),
            "active_ledger": {
                "U_paid": plane.active.PAID,
                "B_remaining": replay.B_REMAINING,
                "additional_charge": 0,
            },
            "theorem": {
                "source_size_is_2e_minus_1": True,
                "source_interpolation_dimension": 3,
                "forced_split_gcd_is_complete": True,
                "source_plane_theorem_uniformly_instantiated": True,
                "full_base_span_post_c5_is_impossible": True,
                "base_span_at_most_two_directly_paid": True,
                "same_moving_root_containment": True,
                "x0_stratum_paid": True,
                "x1_lower_extra_gcd_descends_to_source_plane": True,
                "x1_lower_same_moving_root_containment": True,
                "x1_lower_stratum_paid": True,
                "x1_upper_dimension_five_open": True,
                "whole_slack_paid": False,
            },
            "deployed_arithmetic": deployed_arithmetic(),
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
            "status": (
                "PROVED_SECOND_SUCCESSOR_LOWER_SOURCE_PLANE_PAYMENTS_"
                "DIMENSION_FIVE_UPPER_STRATUM_OPEN_ROW_OPEN"
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
        "title": "KoalaBear second-successor lower source-plane payments",
        "type": "object",
    }


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_second_successor_lower_source_plane_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED X=0 AND X=1 LOWER-STRATUM PAYMENTS",
        "\\boxed{e=67{,}474,\\qquad s=2e-1.}",
        "forced common divisor is exactly the complete split zero locator",
        "Uniform source-plane theorem",
        "4{,}180{,}882{,}818{,}326{,}970",
        "division by this scalar leaves the selected slope unchanged",
        "complete \\(x=1,e=67{,}474\\) stratum is paid",
        "only the upper \\(x=1\\) degree remains",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(cert: dict[str, Any], schema: dict[str, Any]) -> None:
    need(cert == expected_certificate(), "certificate differs from exact replay")
    need(schema == expected_schema(), "schema differs from exact replay")
    need(cert["active_ledger"]["additional_charge"] == 0, "zero charge")
    need(cert["theorem"]["x0_stratum_paid"] is True, "x=0 payment")
    need(
        cert["theorem"]["x1_lower_stratum_paid"] is True,
        "x=1 lower payment",
    )
    need(cert["theorem"]["whole_slack_paid"] is False, "whole-slack status")
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
        lambda d: d["active_ledger"].__setitem__("additional_charge", 1),
        lambda d: d["theorem"].__setitem__(
            "source_interpolation_dimension", 4
        ),
        lambda d: d["theorem"].__setitem__(
            "forced_split_gcd_is_complete", False
        ),
        lambda d: d["theorem"].__setitem__(
            "source_plane_theorem_uniformly_instantiated", False
        ),
        lambda d: d["theorem"].__setitem__(
            "full_base_span_post_c5_is_impossible", False
        ),
        lambda d: d["theorem"].__setitem__("x0_stratum_paid", False),
        lambda d: d["theorem"].__setitem__(
            "x1_lower_extra_gcd_descends_to_source_plane", False
        ),
        lambda d: d["theorem"].__setitem__(
            "x1_lower_same_moving_root_containment", False
        ),
        lambda d: d["theorem"].__setitem__(
            "x1_lower_stratum_paid", False
        ),
        lambda d: d["theorem"].__setitem__("whole_slack_paid", True),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "zero_locator_size", ZERO_LOCATOR - 1
        ),
        lambda d: d["deployed_arithmetic"].__setitem__(
            "direct_cap", DIRECT_CAP + 1
        ),
        lambda d: d["upstream_certificates"][
            "source_plane_theorem"
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
            print(f"r: {R}")
            print(f"x: {X}")
            print(f"direct_cap: {DIRECT_CAP}")
            print(f"reserve_margin: {MARGIN}")
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
