#!/usr/bin/env python3
"""Fail-closed packet replay for the M31 rank-seven master cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-shallow-master-denominator-cut-v1/manifest.json"
)
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_rank7_shallow_master_denominator_cut_v1.schema.json"
)
PRIMARY_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_shallow_master_denominator_cut_v1.py"
)
SAGE_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_shallow_master_denominator_cut_v1.sage"
)
PACKET_PATH = Path(__file__).resolve()
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_shallow_master_denominator_cut_v1.md"
)
README_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-shallow-master-denominator-cut-v1/README.md"
)
PARENT_MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-truncated-weight-flag-route-cut-v1/manifest.json"
)
PARENT_PACKET_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_truncated_weight_flag_route_cut_packet_v1.py"
)
PARENT_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_truncated_weight_flag_route_cut_v1.md"
)
ALL_WEIGHT_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_all_weight_anchor_exchange_pade_bijection_v1.md"
)
BOUNDARY_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_boundary_common_v_cross_g_route_cut_v1.md"
)
FIXED_G_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_fixed_g_universal_rs_embedding_v1.md"
)
GRANDE_FINALE_PATH = ROOT / "experimental/grande_finale.tex"

SCHEMA_ID = "m31-rank7-shallow-master-denominator-cut-summary-v1"
THEOREM_ID = "M31_RANK7_SHALLOW_MASTER_DENOMINATOR_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_RANK7_MASTER_DENOMINATOR_V1"
STATUS = "PROVED_MASTER_NORMALIZATION_FIXED_G_AND_HARMONIC_FLANK_ROW_OPEN"
PARENT_PAYLOAD = (
    "914ee52fa6c4df6697268ca36d825f01361cad4a6a9d6d1c3f0edd822f379cd8"
)
SOURCE_PREFIX = "M31_RANK7_MASTER_DENOMINATOR_CUT::"

EXPECTED_SAGE = (
    b"M31_RANK7_SHALLOW_MASTER_DENOMINATOR_CUT_SAGE_V1\n"
    b"proper_slice_maximum=9471941\n"
    b"full_slice_transition=328677:15776081,328678:15775927\n"
    b"harmonic_paid_range=354973..354998\n"
    b"harmonic_transition=354972:15776055,354973:15775843\n"
    b"toy_pairs=461\n"
    b"toy_global_rank=6\n"
    b"toy_max_proper_slice_rank=4\n"
    b"PASS\n"
)


class VerificationError(RuntimeError):
    pass


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON encoding") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    require(path.is_file(), f"source exists: {path}")
    return sha256_bytes(path.read_bytes())


def payload_hash(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_bytes(canonical_json(unsigned))


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_hash(result)
    return result


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN/infinity JSON forbidden")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def decode(raw: bytes, *, canonical: bool) -> dict[str, Any]:
    require(len(raw) <= 64 * 1024 * 1024, "JSON size cap")
    try:
        value = json.loads(
            raw.decode("ascii"),
            object_pairs_hook=unique_object,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError("valid ASCII JSON") from exc
    require(type(value) is dict, "top-level JSON object")
    if canonical:
        require(raw == canonical_json(value), "canonical JSON bytes")
    return value


def load(path: Path, *, canonical: bool = True) -> dict[str, Any]:
    require(path.is_file(), f"file exists: {path}")
    return decode(path.read_bytes(), canonical=canonical)


def deep_exact(actual: Any, expected: Any, path: str = "payload") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def run(command: Sequence[str], *, timeout: int = 1800) -> bytes:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    sage_home = Path(environment.get("RS_MCA_SAGE_HOME", "/tmp/rs-mca-sage-home"))
    sage_home.mkdir(parents=True, exist_ok=True)
    environment["HOME"] = str(sage_home)
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    require(
        completed.returncode == 0,
        f"subprocess success: {' '.join(command)}\n"
        f"{completed.stderr.decode(errors='replace')}",
    )
    return completed.stdout


def source_specifications() -> list[tuple[str, Path, str | None, str]]:
    return [
        ("packet_schema", SCHEMA_PATH, None, "Closed packet schema."),
        ("primary_exact_replay", PRIMARY_PATH, None, "Exact Python arithmetic and mutations."),
        ("independent_sage_replay", SAGE_PATH, None, "Independent arithmetic and GF(13) master control."),
        ("packet_verifier", PACKET_PATH, None, "Fail-closed packet and source replay."),
        ("theorem_note", NOTE_PATH, None, "Proof, source bridge, and exact residual."),
        ("packet_readme", README_PATH, None, "Replay and nonclaim instructions."),
        ("parent_manifest", PARENT_MANIFEST_PATH, PARENT_PAYLOAD, "Sealed rank-seven predecessor."),
        ("parent_packet_verifier", PARENT_PACKET_PATH, None, "Fail-closed predecessor replay."),
        ("parent_note", PARENT_NOTE_PATH, None, "Immediate rank-seven residual source."),
        ("all_weight_bijection", ALL_WEIGHT_NOTE_PATH, None, "Canonical all-weight pair source."),
        ("boundary_shallow_source", BOUNDARY_NOTE_PATH, None, "Base-field shallow family and tail cap."),
        ("fixed_g_embedding_source", FIXED_G_NOTE_PATH, None, "Ordinary fixed-G obstruction and scope."),
        ("grande_finale_compilers", GRANDE_FINALE_PATH, None, "Affine-span and codimension-one theorems."),
    ]


def source_bindings() -> list[dict[str, Any]]:
    bindings = []
    for role, path, internal, scope in source_specifications():
        bindings.append(
            {
                "binding_id": SOURCE_PREFIX + role,
                "internal_payload_sha256": internal,
                "path": path.relative_to(ROOT).as_posix(),
                "role": role,
                "scope": scope,
                "sha256": sha256_path(path),
            }
        )
    return bindings


def build_expected() -> tuple[dict[str, Any], bytes, bytes]:
    normal = run([sys.executable, str(PRIMARY_PATH), "--check"])
    optimized = run([sys.executable, "-O", str(PRIMARY_PATH), "--check"])
    require(normal == optimized, "primary normal/optimized parity")
    primary = decode(normal, canonical=True)
    primary.pop("payload_sha256", None)
    primary["source_bindings"] = source_bindings()
    return seal(primary), normal, optimized


def validate_schema(payload: dict[str, Any]) -> None:
    schema = load(SCHEMA_PATH, canonical=False)
    require(schema.get("additionalProperties") is False, "closed schema")
    properties = schema.get("properties")
    required = schema.get("required")
    require(type(properties) is dict and type(required) is list, "schema shape")
    require(set(payload) == set(properties) == set(required), "schema exact keys")
    for key, specification in properties.items():
        if isinstance(specification, dict) and "const" in specification:
            require(payload[key] == specification["const"], f"schema const: {key}")


def validate_semantics(payload: dict[str, Any]) -> None:
    require(payload["payload_sha256"] == payload_hash(payload), "payload seal")
    require(payload["schema"] == SCHEMA_ID, "schema id")
    require(payload["theorem_id"] == THEOREM_ID, "theorem id")
    require(payload["architecture"] == ARCHITECTURE_ID, "architecture id")
    require(payload["status"] == STATUS, "status")
    require(payload["parent_payload_sha256"] == PARENT_PAYLOAD, "parent pin")

    fixed_g = payload["fixed_g_slice_cut"]
    require(fixed_g["proper_slice_rank_cap"] == 6, "proper-slice rank")
    require(fixed_g["proper_slice_maximum"] == 9_471_941, "proper-slice cap")
    require(fixed_g["full_slice_threshold"] == 328_678, "full-slice threshold")
    require(
        fixed_g["full_slice_threshold_records"]
        == {"328677": 15_776_081, "328678": 15_775_927},
        "full-slice transition",
    )

    harmonic = payload["harmonic_flank"]
    require(harmonic["new_paid_range"] == [354_973, 354_998], "harmonic range")
    require(harmonic["new_paid_union_count"] == 26, "harmonic count")
    require(harmonic["adjacent_failure_excess"] == 123, "adjacent failure")
    require(harmonic["first_payment_margin"] == 89, "first margin")

    residual = payload["residual_partition"]
    require(residual["new_rank7_union_range"] == [72_428, 354_972], "residual")
    require(residual["new_rank7_union_count"] == 282_545, "residual count")
    require(
        residual["terminal"] == "UNPAID_RANK7_MIXED_G_FIXED_SYNDROME_INCIDENCE",
        "terminal",
    )

    require(
        payload["impact"]
        == {
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "pure_fixed_g_union_values_removed": 26_321,
            "rank7_closed": False,
            "rank7_union_values_removed": 26,
            "rank8_and_above_closed": False,
            "row_closed": False,
        },
        "honest impact",
    )


def validate_sources(payload: dict[str, Any]) -> None:
    bindings = payload["source_bindings"]
    require(type(bindings) is list and len(bindings) == 13, "source count")
    deep_exact(bindings, source_bindings(), "source_bindings")
    parent = load(PARENT_MANIFEST_PATH)
    require(parent.get("payload_sha256") == PARENT_PAYLOAD, "parent payload")


def verify_full() -> dict[str, Any]:
    expected, normal, optimized = build_expected()
    manifest = load(MANIFEST_PATH)
    deep_exact(manifest, expected)
    validate_schema(manifest)
    validate_semantics(manifest)
    validate_sources(manifest)

    tamper_normal = run([sys.executable, str(PRIMARY_PATH), "--tamper-selftest"])
    tamper_optimized = run(
        [sys.executable, "-O", str(PRIMARY_PATH), "--tamper-selftest"]
    )
    require(tamper_normal == tamper_optimized, "primary tamper parity")
    tamper = decode(tamper_normal, canonical=True)
    require(tamper["mutations"] == tamper["detected"] == 14, "primary mutations")

    sage_raw = run(["sage", str(SAGE_PATH)])
    require(sage_raw == EXPECTED_SAGE, "exact Sage replay")
    parent_raw = run([sys.executable, str(PARENT_PACKET_PATH)])

    return {
        "schema": "m31-rank7-master-denominator-packet-replay-v1",
        "checks": CHECKS + 1,
        "payload_sha256": manifest["payload_sha256"],
        "primary_sha256": sha256_bytes(normal),
        "primary_normal_equals_optimized": normal == optimized,
        "primary_mutations_detected": tamper["detected"],
        "primary_tamper_normal_equals_optimized": (
            tamper_normal == tamper_optimized
        ),
        "sage_sha256": sha256_bytes(sage_raw),
        "sage_exact_replay": True,
        "source_bindings": len(manifest["source_bindings"]),
        "parent_payload_sha256": PARENT_PAYLOAD,
        "parent_replay_sha256": sha256_bytes(parent_raw),
        "rank7_closed": False,
        "row_closed": False,
        "ledger_movement": 0,
    }


def packet_tamper_selftest() -> dict[str, Any]:
    expected, _, _ = build_expected()
    semantic_mutations = [
        (("row", "shallow_size"), 15_775_934),
        (("fixed_g_slice_cut", "proper_slice_rank_cap"), 7),
        (("fixed_g_slice_cut", "proper_slice_maximum"), 9_471_942),
        (("fixed_g_slice_cut", "full_slice_threshold"), 328_677),
        (("harmonic_flank", "new_paid_range"), [354_972, 354_998]),
        (("harmonic_flank", "new_paid_union_count"), 27),
        (("harmonic_flank", "first_payment_margin"), 88),
        (("residual_partition", "new_rank7_union_count"), 282_546),
        (("impact", "rank7_closed"), True),
        (("impact", "ledger_movement"), 1),
        (("parent_payload_sha256",), "0" * 64),
        (("payload_sha256",), "0" * 64),
        (("source_bindings", 0, "sha256"), "0" * 64),
    ]
    detected = 0
    for path, value in semantic_mutations:
        mutant = copy.deepcopy(expected)
        cursor: Any = mutant
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        try:
            deep_exact(mutant, expected)
        except VerificationError:
            detected += 1
        else:
            raise VerificationError(f"semantic mutation escaped: {path}")

    hostile = [
        b'{"a":1,"a":2}\n',
        b'{"a":1.5}\n',
        b'{"a":NaN}\n',
        b'{ "a":1}\n',
    ]
    hostile_detected = 0
    for raw in hostile:
        try:
            decode(raw, canonical=True)
        except VerificationError:
            hostile_detected += 1
        else:
            raise VerificationError("hostile parser mutation escaped")
    require(detected == len(semantic_mutations), "semantic mutations")
    require(hostile_detected == len(hostile), "hostile mutations")
    return {
        "schema": "m31-rank7-master-denominator-packet-tamper-v1",
        "semantic_mutations": len(semantic_mutations),
        "semantic_detected": detected,
        "hostile_mutations": len(hostile),
        "hostile_detected": hostile_detected,
        "all_detected": True,
        "base_payload_sha256": expected["payload_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write_manifest:
            expected, _, _ = build_expected()
            MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
            MANIFEST_PATH.write_bytes(canonical_json(expected))
            print(expected["payload_sha256"])
            return 0
        result = packet_tamper_selftest() if args.tamper_selftest else verify_full()
        sys.stdout.buffer.write(canonical_json(result))
        return 0
    except (
        VerificationError,
        KeyError,
        OSError,
        subprocess.TimeoutExpired,
    ) as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
