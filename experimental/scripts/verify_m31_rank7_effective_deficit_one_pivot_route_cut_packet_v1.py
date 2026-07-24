#!/usr/bin/env python3
"""Fail-closed packet replay for the M31 rank-seven one-pivot route cut."""

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
CERTIFICATE_DIRECTORY = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-effective-deficit-one-pivot-route-cut-v1"
)
MANIFEST_PATH = CERTIFICATE_DIRECTORY / "manifest.json"
README_PATH = CERTIFICATE_DIRECTORY / "README.md"
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_rank7_effective_deficit_one_pivot_route_cut_v1.schema.json"
)
PRIMARY_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_effective_deficit_one_pivot_route_cut_v1.py"
)
SAGE_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_effective_deficit_one_pivot_route_cut_v1.sage"
)
PACKET_PATH = Path(__file__).resolve()
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_effective_deficit_one_pivot_route_cut_v1.md"
)
PARENT_MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-split-divisor-tail-route-cut-v1/manifest.json"
)
PARENT_PACKET_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_split_divisor_tail_route_cut_packet_v1.py"
)
PARENT_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_split_divisor_tail_route_cut_v1.md"
)
GRANDE_FINALE_PATH = ROOT / "experimental/grande_finale.tex"
FIXED_G_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_fixed_g_universal_rs_embedding_v1.md"
)
SHORTENING_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_varying_g_affine_span_shortening_route_cut_v1.md"
)
C2048_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_c2048_vt_multitemplate_global_rank_route_cut.md"
)

SCHEMA_ID = "m31-rank7-effective-deficit-one-pivot-route-cut-summary-v1"
THEOREM_ID = "M31_RANK7_EFFECTIVE_DEFICIT_ONE_PIVOT_ROUTE_CUT_V1"
ARCHITECTURE_ID = (
    "M31_BASE_FIELD_BOUNDARY_RANK7_EFFECTIVE_DEFICIT_ONE_PIVOT_V1"
)
STATUS = "PROVED_ONE_PIVOT_HEAD_AND_FIXED_G_CLOSURE_ROUTE_CUT_ROW_OPEN"
PARENT_PAYLOAD = (
    "7d5df76a7188a66188cabfce710d4b4cb692be6a8e12428c99887ab882453625"
)
SOURCE_PREFIX = "M31_RANK7_EFFECTIVE_DEFICIT_ONE_PIVOT::"


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
    require(len(raw) <= 16 * 1024 * 1024, "JSON size cap")
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
            "All-g H_Q scan, endpoint relaxation, and mutations.",
        ),
        (
            "independent_sage_replay",
            SAGE_PATH,
            None,
            "Independent all-g arithmetic and fixed-H toy replay.",
        ),
        ("packet_verifier", PACKET_PATH, None, "Fail-closed packet replay."),
        ("theorem_note", NOTE_PATH, None, "Proof, closure, and route cut."),
        ("packet_readme", README_PATH, None, "Replay and nonclaim instructions."),
        (
            "parent_manifest",
            PARENT_MANIFEST_PATH,
            PARENT_PAYLOAD,
            "Sealed split-divisor tail predecessor.",
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
            "Cumulative q-head theorem and scalar resources.",
        ),
        (
            "affine_span_compiler_source",
            GRANDE_FINALE_PATH,
            None,
            "Recursive affine-span compiler.",
        ),
        (
            "fixed_g_embedding_source",
            FIXED_G_NOTE_PATH,
            None,
            "Fixed-G arbitrary ordinary-RS embedding.",
        ),
        (
            "fixed_g_endpoint_source",
            SHORTENING_NOTE_PATH,
            None,
            "Johnson residual endpoint payment.",
        ),
        (
            "c2048_module_source",
            C2048_NOTE_PATH,
            None,
            "Integrated rank-2048 free-module degree filtration.",
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
    require(row["rank"] == 7, "rank")

    frontier = payload["frontier_scan"]
    require(frontier["g_cells"] == 282_545, "all-g cells")
    require(frontier["interval_count"] == 38_569, "interval count")
    require(
        frontier["interval_sha256"]
        == "4e2e2d6ddf919ace174a1cdd3f8df78520d0608a90c87fa231a5075cb8d13b52",
        "interval digest",
    )
    require(frontier["cutoff_range"] == [-23_382, 15_186], "cutoff range")
    require(frontier["zero_tail_closure_upper_cells"] == 204, "zero-tail cells")
    require(
        frontier["maximum_tail_closure_upper"]
        == {"value": 1_852, "g": 354_397, "cutoff": 15_129},
        "maximum tail upper",
    )

    fixed_g = payload["fixed_g_rank7_consequence"]
    require(
        fixed_g["scope"]
        == "PURE_FULL_G_ZERO_ANCHORED_LINEAR_RANK_AT_MOST_SEVEN_ONLY",
        "fixed-G scope",
    )
    require(fixed_g["H_0_at_217542"] == 15_775_952, "fixed-G before")
    require(fixed_g["H_0_at_217543"] == 15_775_767, "fixed-G after")
    require(fixed_g["remaining_interval"] == [72_860, 217_542], "fixed-G open")
    require(fixed_g["remaining_g_cells"] == 144_683, "fixed-G open cells")

    endpoint = payload["endpoint_relaxation"]
    require(endpoint["cutoff"] == 15_186, "endpoint cutoff")
    require(endpoint["H_0"] == 3_268_160, "endpoint H0")
    require(endpoint["H_cutoff"] == 15_774_749, "endpoint cap")
    require(endpoint["H_cutoff_plus_one"] == 15_776_606, "endpoint next")
    require(endpoint["forced_tail_at_cutoff_plus_one"] == 1_184, "tail")
    require(endpoint["tail_closure_upper"] == 1_183, "tail upper")
    require(
        endpoint["histogram_sha256"]
        == "7189e2ededaac854d54ee469451cf6e2f8afe5817c39d47ac65c355d1d04f4a0",
        "histogram digest",
    )
    require(endpoint["first_moment"] == 122_692_619_370, "first moment")
    require(endpoint["second_moment"] == 1_411_089_367_885_678, "second moment")
    resources = endpoint["scalar_resources"]
    require(
        set(resources)
        == {
            "first_pivot",
            "colored_E",
            "colored_S",
            "cross_block",
            "affine_line",
        },
        "scalar resource keys",
    )
    require(
        all(record["lhs"] <= record["rhs"] for record in resources.values()),
        "scalar resources feasible",
    )
    require(
        endpoint["scalar_resources_sha256"]
        == sha256_bytes(canonical_json(resources))
        == "58789a52f5d9ba4dfc47a36b589232d34e7d447158c6d9c91bbe3e8cc3022dbe",
        "scalar resource seal",
    )
    harmonic = endpoint["harmonic"]
    require(
        harmonic
        == {
            "q6_cap": 222_004,
            "q6_winner": 5,
            "q6_raw": 222_004,
            "d6": 1_270_586,
            "layer": 65_515,
            "low": 10_411_669,
            "high": 10_411_790,
            "integer_width": 122,
            "b_zero_total": 10_411_669,
            "b_layer_total": 5_364_264,
            "transport_rows": 15_188,
            "transport_sha256": (
                "c3b09d3958cd5b6ebc4c78c937e3f86e5a5d95d632c3be7db3c136efbde6bb79"
            ),
            "unique_split_row": [11_539, 202, 946],
            "minimum_b_zero_placement_margin": 277_918,
            "minimum_b_layer_placement_margin": 572_181,
        },
        "harmonic record",
    )
    require(
        endpoint["scope"]
        == (
            "EXACT_INTEGER_H_Q_AND_SCALAR_HARMONIC_MARGINAL_RELAXATION; "
            "NO_COMMON_SUPPORT_OR_SOURCE_REALIZATION"
        ),
        "endpoint nonrealization scope",
    )

    route = payload["structural_route_cut"]
    require(
        route["fixed_H_divisibility_fiber"]["deep_affine_dimension_upper"]
        == "min(7,delta-w)",
        "fixed-H deep rank",
    )
    require(
        route["balanced_boundary_layouts"]["block_size_32"]["H"]
        ["raised_occupancy"]
        == 6,
        "32-block interlacing",
    )
    require(
        route["balanced_boundary_layouts"]["block_size_2048"]["H"]
        ["raised_occupancy"]
        == 345,
        "2048-block interlacing",
    )
    require(
        route["nonintegrated_pr1073_quantifier_cut"]["dependency"] is False,
        "PR1073 nondependency",
    )
    require(
        route["balanced_boundary_layouts"]["nonclaim"]
        == (
            "This is a support-layout falsifier of an automatic domain "
            "adapter, not a source-compatible prefix/full-gcd family."
        ),
        "layout nonclaim",
    )
    require(
        payload["nonclaims"]
        == [
            "The endpoint histogram is not a source family.",
            "The q-b transport does not construct one common support layer.",
            "Fixed-H uniqueness does not bound the number of possible H.",
            "The deep exact-gcd fiber is not asserted to be affine.",
            "PR #1073 is not an owner or dependency of this packet.",
            "No complete 32- or 2048-point fiber is forced by cardinality.",
            "No v4 atom or official row value moves.",
        ],
        "critical nonclaims",
    )
    require(
        payload["one_pivot_theorem"]["floor_order"]
        == "inner=numerator//denominator; bound=(N-z)*inner//m",
        "nested floor order",
    )
    require(
        payload["one_pivot_theorem"]["specialized_bound"]
        == (
            "N_delta(<=Q)<=H_Q(g)=floor(R/(g-Q)*"
            "floor(C(R-g+w+6,6)/C(w-Q+6,6)))"
        ),
        "specialized one-pivot bound",
    )
    require(
        payload["one_pivot_theorem"]
        == {
            "ambient_statement": (
                "|L|<=floor((N-z)/m * "
                "floor(C(N-d+k-1,k-1)/C(v+z+k-1,k-1)))"
            ),
            "hypotheses": [
                "W is a k-dimensional linear subspace of RS(E,d)",
                "the received table is nowhere zero on E",
                "m=d+v and 1<=d<=m<=N-z",
                "z is the common-zero count of W",
                "k>=1; the k=0 list is empty for m>0",
            ],
            "floor_order": (
                "inner=numerator//denominator; bound=(N-z)*inner//m"
            ),
            "effective_deficit": "delta_i=q_i-s_i=g-deg(H_i)",
            "specialized_bound": (
                "N_delta(<=Q)<=H_Q(g)=floor(R/(g-Q)*"
                "floor(C(R-g+w+6,6)/C(w-Q+6,6)))"
            ),
            "rank_monotonicity": (
                "After weakening z to zero, the raw inner cap is "
                "nondecreasing for k<=7 because R-(g-w)>=w-Q."
            ),
            "negative_Q": (
                "Negative Q is legal for delta-heads, not q-heads; "
                "Q>=g-R keeps g-Q<=R."
            ),
        },
        "complete one-pivot theorem record",
    )

    require(
        payload["missing_theorem"]["name"]
        == "CROSS_COFACTOR_INTERLACED_H_AND_DEEP_FIBER_INCIDENCE",
        "missing theorem",
    )
    require(
        payload["missing_theorem"]["deep_subterminal"]
        == (
            "Uniformly control the delta>w fixed-H divisibility fibers "
            "and their aggregation across H."
        ),
        "deep-fiber terminal",
    )
    require(
        payload["impact"]
        == {
            "new_green_one_pivot_theorem": True,
            "new_fixed_g_rank7_payment": [217_543, 354_972],
            "current_scalar_route_cut": True,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "rank7_closed": False,
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


def validate_sage(raw: bytes) -> dict[str, Any]:
    record = decode(raw, canonical=True)
    digest = record.pop("payload_sha256", None)
    require(type(digest) is str, "Sage payload present")
    require(digest == sha256_bytes(canonical_body(record)), "Sage payload seal")
    expected = {
        "schema": "m31-rank7-effective-deficit-one-pivot-sage-replay-v1",
        "scope": "INDEPENDENT_EXACT_ARITHMETIC_AND_FIXED_H_TOY_CONTROL",
        "frontier_interval_count": 38_569,
        "frontier_interval_sha256": (
            "4e2e2d6ddf919ace174a1cdd3f8df78520d0608a90c87fa231a5075cb8d13b52"
        ),
        "frontier_cutoff_range": [-23_382, 15_186],
        "zero_tail_cells": 204,
        "maximum_tail_upper": [1_852, 354_397, 15_129],
        "endpoint_cutoff": 15_186,
        "endpoint_H_0": 3_268_160,
        "endpoint_H_cutoff": 15_774_749,
        "endpoint_H_next": 15_776_606,
        "endpoint_tail": 1_184,
        "endpoint_histogram_sha256": (
            "7189e2ededaac854d54ee469451cf6e2f8afe5817c39d47ac65c355d1d04f4a0"
        ),
        "endpoint_first_moment": 122_692_619_370,
        "endpoint_second_moment": 1_411_089_367_885_678,
        "fixed_g_transition": [217_543, 15_775_767],
        "module_profiles": {
            "d": [140, 805],
            "old_tail_H": [172, 252],
            "new_tail_H": [165, 1_865],
        },
        "fixed_H_toy": {
            "field": 31,
            "message_dimension": 5,
            "moderate_fiber_size": 1,
            "deep_fiber_size": 961,
            "deep_affine_rank": 2,
        },
    }
    deep_exact(record, expected, "sage")
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
    require(tamper["mutations"] == tamper["detected"] == 28, "primary mutations")

    sage_raw = run(["sage", str(SAGE_PATH)])
    sage = validate_sage(sage_raw)
    parent_raw = run([sys.executable, str(PARENT_PACKET_PATH)])

    return {
        "schema": "m31-rank7-effective-deficit-one-pivot-packet-replay-v1",
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
        "fixed_g_rank7_paid_from": 217_543,
        "rank7_closed": False,
        "row_closed": False,
        "ledger_movement": 0,
    }


def set_path(payload: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    payload["payload_sha256"] = payload_hash(payload)


def packet_tamper_selftest() -> dict[str, Any]:
    expected, _, _ = build_expected()
    semantic_mutations = [
        (("row", "shallow_forbidden_size"), 15_775_932),
        (("row", "residual_g_range"), [72_428, 354_973]),
        (("frontier_scan", "interval_count"), 38_568),
        (("frontier_scan", "interval_sha256"), "0" * 64),
        (("frontier_scan", "cutoff_range"), [-23_381, 15_186]),
        (
            ("frontier_scan", "maximum_tail_closure_upper", "value"),
            1_851,
        ),
        (
            ("fixed_g_rank7_consequence", "H_0_at_217543"),
            15_775_768,
        ),
        (
            ("fixed_g_rank7_consequence", "remaining_interval"),
            [72_860, 217_541],
        ),
        (("endpoint_relaxation", "cutoff"), 15_185),
        (("endpoint_relaxation", "H_cutoff"), 15_774_750),
        (("endpoint_relaxation", "histogram_sha256"), "1" * 64),
        (
            ("endpoint_relaxation", "harmonic", "transport_sha256"),
            "2" * 64,
        ),
        (
            ("endpoint_relaxation", "scalar_resources"),
            {},
        ),
        (
            ("endpoint_relaxation", "harmonic", "q6_cap"),
            0,
        ),
        (
            ("endpoint_relaxation", "scope"),
            "SOURCE_REALIZATION_AND_ROW_CLOSURE",
        ),
        (
            (
                "structural_route_cut",
                "balanced_boundary_layouts",
                "block_size_2048",
                "H",
                "raised_occupancy",
            ),
            346,
        ),
        (
            (
                "structural_route_cut",
                "balanced_boundary_layouts",
                "nonclaim",
            ),
            "This is a source-compatible counterexample.",
        ),
        (
            (
                "structural_route_cut",
                "nonintegrated_pr1073_quantifier_cut",
                "dependency",
            ),
            True,
        ),
        (
            ("nonclaims",),
            ["The endpoint histogram is a source family."],
        ),
        (
            ("one_pivot_theorem", "floor_order"),
            "MERGE_THE_FLOORS",
        ),
        (
            ("one_pivot_theorem", "specialized_bound"),
            "N_delta(<=Q)<=B_star",
        ),
        (
            ("one_pivot_theorem", "ambient_statement"),
            "THE BOUND HOLDS WITHOUT HYPOTHESES",
        ),
        (
            ("one_pivot_theorem", "hypotheses"),
            ["the received table may vanish"],
        ),
        (
            ("one_pivot_theorem", "effective_deficit"),
            "delta_i=q_i+s_i",
        ),
        (("missing_theorem", "name"), "AUTO_PAID"),
        (("impact", "ledger_movement"), 1),
        (("impact", "rank7_closed"), True),
        (("impact", "row_closed"), True),
    ]
    detected = 0
    for path, value in semantic_mutations:
        candidate = copy.deepcopy(expected)
        set_path(candidate, path, value)
        try:
            validate_semantics(candidate)
        except (KeyError, TypeError, VerificationError):
            detected += 1
    require(detected == len(semantic_mutations), "semantic mutations detected")

    hostile = [
        b'{"a":1,"a":2}\n',
        b'{"x":1.5}\n',
        b'{"x":NaN}\n',
        '{"x":"é"}\n'.encode("utf-8"),
        b'{ "x":1 }\n',
    ]
    hostile_detected = 0
    for raw in hostile:
        try:
            decode(raw, canonical=True)
        except VerificationError:
            hostile_detected += 1
    require(hostile_detected == len(hostile), "hostile JSON detected")
    return {
        "schema": "m31-rank7-effective-deficit-one-pivot-packet-tamper-v1",
        "semantic_mutations": len(semantic_mutations),
        "semantic_detected": detected,
        "hostile_mutations": len(hostile),
        "hostile_detected": hostile_detected,
        "all_detected": (
            detected == len(semantic_mutations)
            and hostile_detected == len(hostile)
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--tamper-selftest", action="store_true")
    group.add_argument("--emit-expected", action="store_true")
    args = parser.parse_args()
    if args.tamper_selftest:
        result = packet_tamper_selftest()
    elif args.emit_expected:
        result, _, _ = build_expected()
    else:
        result = verify_full()
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
