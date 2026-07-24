#!/usr/bin/env python3
"""Fail-closed packet replay for the M31 rank-seven split-tail route cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys
from math import comb
from pathlib import Path
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_DIRECTORY = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-split-divisor-tail-route-cut-v1"
)
MANIFEST_PATH = CERTIFICATE_DIRECTORY / "manifest.json"
README_PATH = CERTIFICATE_DIRECTORY / "README.md"
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_rank7_split_divisor_tail_route_cut_v1.schema.json"
)
PRIMARY_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_split_divisor_tail_route_cut_v1.py"
)
SAGE_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_split_divisor_tail_route_cut_v1.sage"
)
PACKET_PATH = Path(__file__).resolve()
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_split_divisor_tail_route_cut_v1.md"
)
PARENT_MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-shallow-master-denominator-cut-v1/manifest.json"
)
PARENT_PACKET_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_shallow_master_denominator_cut_packet_v1.py"
)
PARENT_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_shallow_master_denominator_cut_v1.md"
)
FIXED_G_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_fixed_g_universal_rs_embedding_v1.md"
)
GRANDE_FINALE_PATH = ROOT / "experimental/grande_finale.tex"

SCHEMA_ID = "m31-rank7-split-divisor-tail-route-cut-summary-v1"
THEOREM_ID = "M31_RANK7_SPLIT_DIVISOR_TAIL_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_BASE_FIELD_BOUNDARY_RANK7_SPLIT_DIVISOR_TAIL_V1"
STATUS = (
    "PROVED_CUMULATIVE_HEAD_SCALAR_ROUTE_CUT_AND_TOY_REALIZATION_ROW_OPEN"
)
PARENT_PAYLOAD = (
    "8135b49370b491cc14defb6c9e62648148fa2420a3d0cc45084ba00410eca239"
)
SOURCE_PREFIX = "M31_RANK7_SPLIT_DIVISOR_TAIL_ROUTE_CUT::"


class VerificationError(RuntimeError):
    """Raised when a fail-closed packet gate fails."""


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


def canonical_body(value: Any) -> bytes:
    return canonical_json(value)[:-1]


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
        (
            "primary_exact_replay",
            PRIMARY_PATH,
            None,
            "All-g integer scan, GF(31) fixture, and mutations.",
        ),
        (
            "independent_sage_replay",
            SAGE_PATH,
            None,
            "Independent exact GF(31) full-gcd and rank replay.",
        ),
        ("packet_verifier", PACKET_PATH, None, "Fail-closed packet replay."),
        ("theorem_note", NOTE_PATH, None, "Proof, route cut, and missing theorem."),
        ("packet_readme", README_PATH, None, "Replay and nonclaim instructions."),
        (
            "parent_manifest",
            PARENT_MANIFEST_PATH,
            PARENT_PAYLOAD,
            "Sealed rank-seven master-denominator predecessor.",
        ),
        (
            "parent_packet_verifier",
            PARENT_PACKET_PATH,
            None,
            "Fail-closed predecessor replay.",
        ),
        (
            "parent_theorem_note",
            PARENT_NOTE_PATH,
            None,
            "Master normalization and residual source.",
        ),
        (
            "fixed_g_embedding_source",
            FIXED_G_NOTE_PATH,
            None,
            "Fixed-syndrome ordinary-RS source theorem.",
        ),
        (
            "affine_span_compiler_source",
            GRANDE_FINALE_PATH,
            None,
            "Recursive affine-span and harmonic resource theorems.",
        ),
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

    row = payload["row"]
    require(row["residual_g_range"] == [72_428, 354_972], "residual range")
    require(row["shallow_forbidden_size"] == 15_775_933, "forbidden size")
    require(row["shallow_target"] == 15_775_932, "target")

    transition = payload["transition_scan"]
    require(transition["g_cells"] == 282_545, "all-g cell count")
    require(transition["interval_count"] == 2_465, "interval count")
    require(
        transition["interval_sha256"]
        == "e3c0bc60f3c1e3918a2499cf1baa746f8dfd363c6d74f26af1a345ab5453787f",
        "interval digest",
    )
    endpoint = transition["endpoint_records"]["354972"]
    require(endpoint["q_star"] == 2_463, "endpoint q-star")
    require(endpoint["C_q_star"] == 15_774_894, "endpoint head")
    require(endpoint["forced_tail"] == 1_039, "endpoint forced tail")
    require(endpoint["histogram_first_moment"] == 4_678_598_254, "moment")

    histogram = payload["adversarial_histogram"]
    require(
        histogram["maximum_proper_bucket"]
        == {"count": 1_700, "g": 354_957, "q": 2_462},
        "proper bucket extremizer",
    )
    require(
        histogram["minimum_proper_slice_ceiling"] == 1_182_429,
        "minimum proper-slice ceiling",
    )
    require(
        histogram["minimum_bucket_to_slice_ceiling_margin"]
        == {
            "bucket": 1_700,
            "cap": 1_182_429,
            "g": 354_957,
            "margin": 1_180_729,
            "q": 2_462,
        },
        "proper-slice margin",
    )

    harmonic = payload["joint_harmonic_extremizer"]["minimum_integer_interval"]
    require(
        harmonic
        == {
            "d6": 1_270_586,
            "e": 65_515,
            "g": 354_972,
            "high": 10_411_790,
            "low": 10_411_669,
            "width": 122,
        },
        "harmonic primal endpoint",
    )
    transport = payload["joint_harmonic_extremizer"]["endpoint_transport"]
    rows = transport["rows"]
    require(
        transport["g"] == 354_972
        and transport["b_classes"] == [0, 65_515],
        "endpoint transport coordinates",
    )
    require(
        transport["b_zero_total"] == 10_411_669
        and transport["b_e_total"] == 5_364_264,
        "endpoint transport columns",
    )
    require(type(rows) is list and len(rows) == 2_465, "transport row count")
    require(
        transport["rows_sha256"] == sha256_bytes(canonical_json(rows)),
        "transport table seal",
    )
    require(
        transport["rows_sha256"]
        == "e2e89b305b732bad92e139d2bf89c0476f5bf89eb73b314a02b36361bba509ca",
        "transport table digest",
    )
    cumulative = 0
    for deficit, row in enumerate(rows):
        require(
            type(row) is list
            and len(row) == 3
            and all(type(value) is int for value in row),
            "transport row shape",
        )
        require(row[0] == deficit, "transport q order")
        require(row[1] >= 0 and row[2] >= 0, "transport row nonnegative")
        cumulative += row[1] + row[2]
        if deficit <= 2_463:
            expected_head = comb(693_611, 7) // comb(
                67_447 - deficit + 7,
                7,
            )
            require(cumulative == expected_head, "transport q marginal")
    require(cumulative == 15_775_933, "transport total")
    require(
        sum(row[1] for row in rows) == 10_411_669
        and sum(row[2] for row in rows) == 5_364_264,
        "transport column marginals",
    )
    require(
        payload["joint_harmonic_extremizer"]["scope"]
        == (
            "EXACT_JOINT_Q_B_INTEGER_MARGINAL_RELAXATION; "
            "NO_COMMON_T_OR_SOURCE_REALIZATION"
        ),
        "transport scope",
    )

    toy = payload["prefix_fiber_source_family"]["gf31_positive_w_fixture"]
    require(toy["tail_count"] == 7_864, "GF31 tail count")
    require(toy["total_list_size"] == 7_865, "GF31 total")
    require(toy["deficit_histogram"] == {"0": 1, "1": 7_864}, "GF31 histogram")
    require(toy["linear_rank"] == 7, "GF31 rank")
    require(toy["agreement"] == 8, "GF31 agreement")
    require(toy["every_full_gcd_exact"] is True, "GF31 exact gcd")
    require(toy["master_lcm_restored"] is True, "GF31 exact lcm")
    require(toy["no_common_zero_on_P"] is True, "GF31 no common zero")

    require(
        payload["missing_theorem"]["name"]
        == "JOINT_HEAD_TAIL_FULL_GCD_INCIDENCE",
        "missing theorem",
    )
    require(
        payload["impact"]
        == {
            "current_inequality_route_cut": True,
            "ledger_movement": 0,
            "new_green_local_theorem": True,
            "official_endpoint_movement": 0,
            "rank7_closed": False,
            "rank8_and_above_closed": False,
            "row_closed": False,
        },
        "honest impact",
    )


def validate_sources(payload: dict[str, Any]) -> None:
    bindings = payload["source_bindings"]
    require(type(bindings) is list and len(bindings) == 11, "source count")
    deep_exact(bindings, source_bindings(), "source_bindings")
    parent = load(PARENT_MANIFEST_PATH)
    require(parent.get("payload_sha256") == PARENT_PAYLOAD, "parent payload")


def validate_sage(raw: bytes) -> dict[str, Any]:
    record = decode(raw, canonical=True)
    digest = record.pop("payload_sha256", None)
    require(type(digest) is str, "Sage payload present")
    require(digest == sha256_bytes(canonical_body(record)), "Sage payload seal")
    require(
        record
        == {
            "agreement": 8,
            "deficit_histogram": {"0": 1, "1": 7_864},
            "every_full_gcd_exact": True,
            "field_prime": 31,
            "linear_rank": 7,
            "master_lcm_restored": True,
            "message_dimension": 7,
            "mutation_rejected": True,
            "no_common_zero_on_P": True,
            "restorer_count": 1,
            "schema": "m31-rank7-split-divisor-tail-gf31-sage-replay-v1",
            "scope": "EXACT_GF31_SOURCE_FIXTURE_NOT_DEPLOYED_M31",
            "tail_count": 7_864,
            "total_list_size": 7_865,
        },
        "independent Sage semantics",
    )
    record["payload_sha256"] = digest
    return record


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
    require(tamper["mutations"] == tamper["detected"] == 24, "primary mutations")

    sage_raw = run(["sage", str(SAGE_PATH)])
    sage = validate_sage(sage_raw)
    parent_raw = run([sys.executable, str(PARENT_PACKET_PATH)])

    return {
        "schema": "m31-rank7-split-divisor-tail-packet-replay-v1",
        "checks": CHECKS + 1,
        "payload_sha256": manifest["payload_sha256"],
        "primary_sha256": sha256_bytes(normal),
        "primary_normal_equals_optimized": normal == optimized,
        "primary_mutations_detected": tamper["detected"],
        "primary_tamper_normal_equals_optimized": (
            tamper_normal == tamper_optimized
        ),
        "sage_payload_sha256": sage["payload_sha256"],
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
        (("row", "shallow_forbidden_size"), 15_775_932),
        (("row", "residual_g_range"), [72_428, 354_973]),
        (("transition_scan", "interval_count"), 2_464),
        (("transition_scan", "endpoint_records", "354972", "q_star"), 2_464),
        (("transition_scan", "endpoint_records", "354972", "forced_tail"), 1_038),
        (
            ("adversarial_histogram", "maximum_proper_bucket", "count"),
            1_701,
        ),
        (
            (
                "adversarial_histogram",
                "minimum_bucket_to_slice_ceiling_margin",
                "margin",
            ),
            1_180_728,
        ),
        (
            (
                "joint_harmonic_extremizer",
                "minimum_integer_interval",
                "width",
            ),
            121,
        ),
        (
            (
                "joint_harmonic_extremizer",
                "endpoint_transport",
                "rows",
                0,
                1,
            ),
            10_411_668,
        ),
        (
            (
                "prefix_fiber_source_family",
                "gf31_positive_w_fixture",
                "tail_count",
            ),
            7_863,
        ),
        (
            (
                "prefix_fiber_source_family",
                "gf31_positive_w_fixture",
                "linear_rank",
            ),
            6,
        ),
        (
            (
                "prefix_fiber_source_family",
                "gf31_positive_w_fixture",
                "master_lcm_restored",
            ),
            False,
        ),
        (("missing_theorem", "name"), "TAIL_ONLY"),
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
        "schema": "m31-rank7-split-divisor-tail-packet-tamper-v1",
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
    parser.add_argument("--emit-expected", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    try:
        if args.write_manifest or args.emit_expected:
            expected, _, _ = build_expected()
            if args.write_manifest:
                MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
                MANIFEST_PATH.write_bytes(canonical_json(expected))
                print(expected["payload_sha256"])
            else:
                sys.stdout.buffer.write(canonical_json(expected))
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
