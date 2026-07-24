#!/usr/bin/env python3
"""Fail-closed replay for the M31 weighted-head/interlaced-source packet."""

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
    "m31-rank7-weighted-head-interlaced-source-route-cut-v1"
)
MANIFEST_PATH = CERTIFICATE_DIRECTORY / "manifest.json"
README_PATH = CERTIFICATE_DIRECTORY / "README.md"
SCHEMA_PATH = ROOT / (
    "experimental/data/schemas/"
    "m31_rank7_weighted_head_interlaced_source_route_cut_v1.schema.json"
)
PRIMARY_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_weighted_head_interlaced_source_route_cut_v1.py"
)
SAGE_PATH = ROOT / (
    "experimental/scripts/"
    "verify_m31_rank7_weighted_head_interlaced_source_route_cut_v1.sage"
)
PACKET_PATH = Path(__file__).resolve()
NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_weighted_head_interlaced_source_route_cut_v1.md"
)
COMMON_V_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_common_v_split_flat_pairwise_crt_equivalence_v1.md"
)
MASTER_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_shallow_master_denominator_cut_v1.md"
)
EFFECTIVE_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_rank7_effective_deficit_one_pivot_route_cut_v1.md"
)
V4_NOTE_PATH = ROOT / (
    "experimental/notes/thresholds/"
    "m31_list_v4_global_completion_compiler.md"
)

PREDECESSOR_PACKETS = [
    ROOT
    / (
        "experimental/scripts/"
        "verify_m31_common_v_split_flat_pairwise_crt_packet_v1.py"
    ),
    ROOT
    / (
        "experimental/scripts/"
        "verify_m31_rank7_shallow_master_denominator_cut_packet_v1.py"
    ),
    ROOT
    / (
        "experimental/scripts/"
        "verify_m31_rank7_effective_deficit_one_pivot_route_cut_packet_v1.py"
    ),
]

SCHEMA_ID = "m31-rank7-weighted-head-interlaced-source-route-cut-v1"
THEOREM_ID = "M31_RANK7_WEIGHTED_HEAD_INTERLACED_SOURCE_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_RANK7_WEIGHTED_HEAD_INTERLACED_SOURCE_V1"
STATUS = "PROVED_WEIGHTED_HEAD_AND_SOURCE_OBSTRUCTION_ROW_OPEN"


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


def source_specifications() -> list[tuple[str, Path, str]]:
    return [
        ("schema", SCHEMA_PATH, "Closed certificate schema."),
        (
            "primary",
            PRIMARY_PATH,
            "Exact deployed arithmetic, existence proof, and mutations.",
        ),
        (
            "independent_sage",
            SAGE_PATH,
            "Independent arithmetic and direct finite-field realization.",
        ),
        ("packet", PACKET_PATH, "Fail-closed packet replay."),
        ("note", NOTE_PATH, "Proof, v4 chronology, and nonclaims."),
        ("readme", README_PATH, "Replay instructions and scope."),
        (
            "common_v_predecessor",
            COMMON_V_NOTE_PATH,
            "Pairwise Wronskian criterion for one common unit.",
        ),
        (
            "master_denominator_predecessor",
            MASTER_NOTE_PATH,
            "Master-denominator and exact full-gcd adapter.",
        ),
        (
            "effective_deficit_predecessor",
            EFFECTIVE_NOTE_PATH,
            "Endpoint effective-deficit terminal.",
        ),
        (
            "v4_chronology",
            V4_NOTE_PATH,
            "Five-atom LIST chronology and signed credit gate.",
        ),
    ]


def validate_schema(schema: dict[str, Any]) -> None:
    require(
        schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema",
        "schema dialect",
    )
    require(schema.get("$id") == SCHEMA_ID, "schema id")
    require(schema.get("type") == "object", "schema top-level type")
    require(schema.get("additionalProperties") is False, "schema closed")
    expected_required = {
        "architecture",
        "boundary_layout",
        "checks",
        "common_unit",
        "cofactor_pivot_theorem",
        "cofactor_slice_marginal",
        "dual_domain_per_label_compiler",
        "endpoint_relaxation",
        "impact",
        "interlaced_H_selection",
        "master_normalization",
        "no_second_cofactor_pivot_witness",
        "nonclaims",
        "payload_sha256",
        "recursive_full_line_compiler",
        "row",
        "schema",
        "source_bindings",
        "source_consequence",
        "split_numerators",
        "status",
        "theorem_id",
        "two_stage_pivot_johnson_theorem",
        "v4_chronology",
        "weighted_head_theorem",
    }
    require(set(schema.get("required", [])) == expected_required, "schema required")
    properties = schema.get("properties")
    require(type(properties) is dict, "schema properties object")
    require(set(properties) == expected_required, "schema property closure")
    require(properties["schema"].get("const") == SCHEMA_ID, "schema const")
    require(
        properties["theorem_id"].get("const") == THEOREM_ID,
        "theorem const",
    )
    require(
        properties["architecture"].get("const") == ARCHITECTURE_ID,
        "architecture const",
    )
    require(properties["status"].get("const") == STATUS, "status const")
    require(properties["source_bindings"].get("minItems") == 10, "source min")
    require(properties["source_bindings"].get("maxItems") == 10, "source max")
    require(properties["nonclaims"].get("minItems") == 7, "nonclaim min")
    require(properties["nonclaims"].get("maxItems") == 7, "nonclaim max")


def validate_source_bindings(payload: dict[str, Any]) -> None:
    bindings = payload.get("source_bindings")
    require(type(bindings) is list, "source bindings list")
    specifications = source_specifications()
    require(len(bindings) == len(specifications), "source binding count")
    for record, (binding_id, path, role) in zip(
        bindings, specifications, strict=True
    ):
        require(type(record) is dict, f"source binding object: {binding_id}")
        require(
            set(record) == {"binding_id", "path", "role", "sha256"},
            f"source binding keys: {binding_id}",
        )
        require(record["binding_id"] == binding_id, f"source id: {binding_id}")
        require(
            record["path"] == str(path.relative_to(ROOT)),
            f"source path: {binding_id}",
        )
        require(record["role"] == role, f"source role: {binding_id}")
        require(record["sha256"] == sha256_path(path), f"source hash: {binding_id}")


def validate_payload(payload: dict[str, Any]) -> None:
    require(payload.get("payload_sha256") == payload_hash(payload), "payload hash")
    require(payload.get("schema") == SCHEMA_ID, "payload schema")
    require(payload.get("theorem_id") == THEOREM_ID, "payload theorem")
    require(payload.get("architecture") == ARCHITECTURE_ID, "payload architecture")
    require(payload.get("status") == STATUS, "payload status")

    row = payload.get("row")
    require(type(row) is dict, "row object")
    require(
        (
            row.get("field_prime"),
            row.get("n"),
            row.get("K"),
            row.get("agreement"),
            row.get("radius"),
            row.get("slack"),
            row.get("B_star"),
            row.get("forbidden_list_size"),
        )
        == (
            2_147_483_647,
            2_097_152,
            1_048_576,
            1_116_023,
            981_129,
            67_447,
            16_777_215,
            16_777_216,
        ),
        "deployed row constants",
    )

    weighted = payload.get("weighted_head_theorem")
    stage = payload.get("two_stage_pivot_johnson_theorem")
    cofactor = payload.get("cofactor_pivot_theorem")
    require(weighted.get("status") == "PROVED_SOURCE_BOUND", "weighted status")
    require(stage.get("status") == "PROVED_SOURCE_BOUND", "two-stage status")
    require(cofactor.get("status") == "PROVED_SOURCE_BOUND", "cofactor status")
    require(stage.get("r_zero_cap") == 1, "rank-zero cap")
    require(cofactor.get("Phi_endpoint") == 3_983_444, "Phi endpoint")
    require(cofactor.get("F_at_endpoint_cutoff") == 412_817, "fixed-G cap")

    recursive = payload.get("recursive_full_line_compiler")
    require(type(recursive) is dict, "recursive compiler object")
    require(recursive.get("status") == "PROVED_SOURCE_BOUND", "recursive status")
    require(
        recursive.get("algorithm") == "EXACT_MONOTONE_DEQUE_O_7D",
        "recursive algorithm",
    )
    full = recursive.get("full_top_six_frontier")
    require(full.get("Q") == 26_143, "recursive frontier Q")
    require(full.get("head") == 15_775_194, "recursive frontier head")
    require(full.get("target_margin") == 738, "recursive frontier margin")
    require(full.get("next_Q") == 26_144, "recursive next Q")
    require(full.get("next_coarse_head") == 15_776_151, "recursive next coarse")
    exact_next = full.get("next_exact_relaxation")
    require(exact_next.get("head_cap") == 15_776_148, "recursive next exact")
    require(
        exact_next.get("top_six") == [284_730, 614, 545, 545, 545, 545],
        "recursive next top six",
    )
    require(exact_next.get("tail_full_classes") == 1_272, "recursive tail classes")
    require(exact_next.get("tail_remainder") == 365, "recursive tail remainder")
    source_lifted = full.get("next_source_lifted_bound")
    require(
        source_lifted.get("head_cap") == 15_345_533,
        "source-lifted head",
    )
    require(
        source_lifted.get("objective_numerator") == 5_046_040_936_511,
        "source-lifted numerator",
    )
    require(
        source_lifted.get("target_margin") == 430_399,
        "source-lifted target margin",
    )
    require(
        source_lifted.get("largest_class_size") == 283_663,
        "source-lifted largest class",
    )
    require(
        source_lifted.get("largest_residual_dimension") == 3_862,
        "source-lifted residual dimension",
    )
    require(
        source_lifted.get("initial_common_zero_reduction", {}).get(
            "conclusion"
        )
        == "T_ZERO_IS_WORST_CASE",
        "source-lifted common-zero reduction",
    )
    dual = payload.get("dual_domain_per_label_compiler")
    require(type(dual) is dict, "dual-domain compiler object")
    require(
        dual.get("status") == "PROVED_SOURCE_BOUND_AND_SHARP_METHOD_ROUTE_CUT",
        "dual-domain status",
    )
    positive = dual.get("Q26193_positive")
    require(positive.get("schedule") == "x(k)=44835-floor(67*k/10)", "Q26193 schedule")
    require(positive.get("head_cap") == 15_775_776, "Q26193 head")
    require(
        positive.get("objective_numerator") == 5_186_744_182_280,
        "Q26193 numerator",
    )
    require(positive.get("target_margin") == 156, "Q26193 target margin")
    require(positive.get("coarse_survivor_count") == 239, "Q26193 survivors")
    require(positive.get("refined_count") == 239, "Q26193 refinements")
    require(positive.get("remaining_survivor_count") == 0, "Q26193 closure")
    require(
        (
            positive.get("raw_dual_cap_first"),
            positive.get("raw_dual_cap_last"),
            positive.get("raw_dual_cap_monotonicity_violations"),
        )
        == (7_899_882, 12_277_361, 0),
        "Q26193 linear raw caps",
    )
    zero_reduction = dual.get("global_E0_common_zero_reduction")
    require(zero_reduction.get("last_unpaid_t") == 23_729, "E0-zero last unpaid")
    require(zero_reduction.get("first_paid_t") == 23_730, "E0-zero first paid")
    require(
        zero_reduction.get("uniqueness_margin") == 211_415,
        "E0-zero line uniqueness",
    )
    negative = dual.get("Q26194_tangent_scan")
    require(
        negative.get("schedule")
        == "x(k)=max(k-1,w+k-isqrt((A_E+k)(k-1))-11)",
        "Q26194 tangent schedule",
    )
    require(negative.get("head_cap") == 15_800_402, "Q26194 head")
    require(
        negative.get("objective_numerator") == 5_194_824_788_248,
        "Q26194 numerator",
    )
    no_split = dual.get("Q26194_schedule_independent_route_cut")
    require(no_split.get("Phi_Q") == 4_008_251, "Q26194 Phi")
    require(len(no_split.get("intervals", [])) == 7, "Q26194 interval count")
    require(
        no_split.get("minimum_excess_over_old") == 192,
        "Q26194 no-split excess",
    )
    require(
        no_split.get("conclusion")
        == "NO_LEGAL_SPLIT_IMPROVES_THIS_CLASS",
        "Q26194 route-cut conclusion",
    )

    endpoint = payload.get("endpoint_relaxation")
    require(endpoint.get("g") == 354_972, "endpoint g")
    require(endpoint.get("delta") == 26_144, "endpoint deficit")
    require(endpoint.get("q") == 26_144, "endpoint cofactor")
    require(endpoint.get("count") == 15_775_933, "endpoint count")
    require(endpoint.get("H_degree") == 328_828, "endpoint H degree")
    require(
        endpoint.get("classification")
        == "EXACT_INTEGER_MARGINAL_REJECTED_BY_PLANTED_ROOT_SOURCE_LIFT",
        "endpoint source rejection",
    )
    require(endpoint.get("B6") == 22_416_731, "endpoint B6")
    require(
        endpoint.get("weighted_E_margin") == 16_806_136_372_775,
        "weighted margin",
    )
    stage_data = endpoint.get("two_stage_common_zero_johnson")
    require(stage_data.get("Q_15187_head") == 14_589_030, "Q15187 rejected")
    require(stage_data.get("frontier_Q") == 15_838, "frontier Q")
    require(stage_data.get("frontier_head") == 15_774_764, "frontier head")
    require(stage_data.get("frontier_forced_tail") == 1_169, "frontier tail")
    require(stage_data.get("next_Q") == 15_839, "next Q")
    require(stage_data.get("next_head") == 15_776_639, "next head")
    require(
        stage_data.get("next_optimizer") == [5_453_288, 6, 4_513],
        "next optimizer",
    )
    require(
        stage_data.get("next_rank_caps")
        == [1, 13, 162, 2_240, 30_191, 405_788, 5_453_288],
        "next rank caps",
    )
    require(
        endpoint.get("histogram_sha256")
        == "c393b083f7b71a8b03c8823153cae6e4c81044cd3924bfae002f8dd257a853d5",
        "histogram digest",
    )

    marginal = payload.get("cofactor_slice_marginal")
    require(marginal.get("proper_slice_count") == 39, "slice count")
    require(marginal.get("slice_capacity") == 412_817, "slice capacity")
    require(marginal.get("slice_counts", [])[-1] == 88_887, "last slice")
    require(
        marginal.get("root_load_histogram") == {"2": 45_300, "3": 309_672},
        "root load histogram",
    )
    require(marginal.get("lcm_G_equals_P") is True, "cyclic lcm")
    require(marginal.get("intersection_all_Q_empty") is True, "cyclic intersection")

    layout = payload.get("boundary_layout")
    require(layout.get("T32_blocks") == 65_536, "T32 block count")
    require(layout.get("T2_pairs") == 1_048_576, "T2 pair count")
    numerators = payload.get("split_numerators")
    require(numerators.get("union_degree") == 354_972, "numerator lcm degree")
    require(numerators.get("degree_each") == 67_448, "numerator degrees")
    interlaced = payload.get("interlaced_H_selection")
    require(interlaced.get("pairwise_disjoint") is True, "H disjointness")
    require(interlaced.get("H_roots_per_T32_max") == 2, "H block cap")
    common = payload.get("common_unit")
    require(common.get("W_ij_nonzero_on_all_E0") is True, "Wronskian gate")
    require(common.get("forbidden_label_count_max") == 5_886_774, "label count")
    master = payload.get("master_normalization")
    require(master.get("q_i") == 287_524, "source cofactor degree")
    require(master.get("delta_i") == 287_524, "source deficit")
    require(master.get("common_zero_on_ZP") is False, "exact lcm no-common-zero")
    source = payload.get("source_consequence")
    require(source.get("companions") == 7, "source companions")
    require(source.get("total_certified_codewords") == 8, "source lower floor")
    require(source.get("zero_anchored_rank") == 7, "source rank")
    require(source.get("rigor") == "PROVED_EXISTENCE", "source rigor")
    impact = payload.get("impact")
    require(impact.get("row_closed") is False, "row remains open")
    require(impact.get("ledger_movement") == 0, "no ledger movement")
    chronology = payload.get("v4_chronology")
    require(chronology.get("signed_Xi46_payment") is False, "no signed credit")
    require(chronology.get("first_match_payment") is False, "no first-match payment")
    require(len(payload.get("nonclaims", [])) == 7, "seven nonclaims")
    require(type(payload.get("checks")) is int and payload["checks"] >= 1, "check count")
    validate_source_bindings(payload)


def validate_sage(record: dict[str, Any]) -> None:
    require(
        record.get("schema")
        == "m31-rank7-weighted-head-interlaced-source-sage-v1",
        "Sage schema",
    )
    require(record.get("payload_sha256") == payload_hash(record), "Sage hash")
    weighted = record.get("weighted")
    require(weighted.get("two_stage_Q15187", {}).get("head") == 14_589_030, "Sage Q15187")
    require(weighted.get("two_stage_Q15838_head") == 15_774_764, "Sage Q15838")
    require(
        weighted.get("two_stage_Q15839", {}).get("head") == 15_776_639,
        "Sage Q15839",
    )
    require(weighted.get("B6") == 22_416_731, "Sage B6")
    require(weighted.get("Phi") == 3_983_444, "Sage Phi")
    require(weighted.get("F_endpoint_cutoff") == 412_817, "Sage fixed-G")
    recursive = record.get("recursive_full_line")
    require(
        recursive.get("two_tier_Q26052_head") == 15_775_392,
        "Sage recursive Q26052",
    )
    require(
        recursive.get("coupled_Q26143_head") == 15_775_194,
        "Sage coupled Q26143",
    )
    require(
        recursive.get("Q26144_source_lifted_head") == 15_345_533,
        "Sage source-lifted Q26144",
    )
    require(
        recursive.get("Q26144_source_lifted_numerator")
        == 5_046_040_936_511,
        "Sage source-lifted numerator",
    )
    require(
        recursive.get("Q26144_source_lifted_optimizer")
        == [
            283_663,
            3_862,
            15_294_703,
            15_295_049,
            15_294_703,
            3_861,
            3_857,
            1_014_887,
            3_846,
            772,
            1_014_383,
            757,
        ],
        "Sage source-lifted optimizer",
    )
    require(
        recursive.get("common_zero_reduction", {}).get("planted_min_increment")
        == 1_331,
        "Sage common-zero reduction",
    )
    dual = record.get("dual_domain")
    require(dual.get("Q26193_head") == 15_775_776, "Sage Q26193 head")
    require(
        dual.get("Q26193_numerator") == 5_186_744_182_280,
        "Sage Q26193 numerator",
    )
    require(
        dual.get("Q26193_schedule") == "x(k)=44835-floor(67*k/10)",
        "Sage Q26193 schedule",
    )
    require(
        dual.get("Q26193_first_raw") == [2_788, 26_156, 7_899_882],
        "Sage Q26193 first raw cap",
    )
    require(
        dual.get("Q26193_last_raw") == [3_026, 24_561, 12_277_361],
        "Sage Q26193 last raw cap",
    )
    require(
        dual.get("Q26193_remaining_survivors") == 0,
        "Sage Q26193 closure",
    )
    require(dual.get("Q26194_head") == 15_800_402, "Sage Q26194 head")
    require(
        dual.get("Q26194_numerator") == 5_194_824_788_248,
        "Sage Q26194 numerator",
    )
    require(dual.get("Q26194_minimum_excess") == 192, "Sage Q26194 route cut")
    require(
        len(dual.get("Q26194_route_intervals", [])) == 7,
        "Sage Q26194 intervals",
    )
    require(
        dual.get("E0_zero_branch", {}).get("t_23730_cap") == 15_774_894,
        "Sage E0-zero threshold",
    )
    cyclic = record.get("cyclic_marginal")
    require(cyclic.get("slice_count") == 39, "Sage slice count")
    require(cyclic.get("root_load_2") == 45_300, "Sage root load two")
    require(cyclic.get("root_load_3") == 309_672, "Sage root load three")
    toy = record.get("toy")
    require(toy.get("field") == 101, "Sage toy field")
    require(toy.get("rank") == 3, "Sage toy rank")
    require(toy.get("full_gcd") is True, "Sage toy full gcd")
    require(toy.get("exact_lcm") is True, "Sage toy exact lcm")
    require(toy.get("complete_agreement_blocks") == [False] * 3, "Sage toy agreement")
    require(toy.get("complete_error_blocks") == [False] * 3, "Sage toy error")
    require(
        record.get("no_second_pivot", {}).get("evaluation_column_rank") == 1,
        "Sage no-second-pivot witness",
    )


def run_tamper_selftest() -> int:
    manifest = load(MANIFEST_PATH)
    validate_payload(manifest)
    mutations = [
        ("prime", ("row", "field_prime"), 2_147_483_645),
        ("weighted", ("endpoint_relaxation", "weighted_E_margin"), 0),
        (
            "stage",
            ("endpoint_relaxation", "two_stage_common_zero_johnson", "next_head"),
            15_776_638,
        ),
        (
            "source-lift",
            (
                "recursive_full_line_compiler",
                "full_top_six_frontier",
                "next_source_lifted_bound",
                "head_cap",
            ),
            15_345_534,
        ),
        (
            "source-lift-common-zero",
            (
                "recursive_full_line_compiler",
                "full_top_six_frontier",
                "next_source_lifted_bound",
                "initial_common_zero_reduction",
                "conclusion",
            ),
            "T_POSITIVE_MAY_BE_WORSE",
        ),
        (
            "dual-Q26193",
            ("dual_domain_per_label_compiler", "Q26193_positive", "head_cap"),
            15_775_777,
        ),
        (
            "dual-Q26194",
            (
                "dual_domain_per_label_compiler",
                "Q26194_schedule_independent_route_cut",
                "minimum_excess_over_old",
            ),
            191,
        ),
        ("Phi", ("cofactor_pivot_theorem", "Phi_endpoint"), 1_268_269),
        ("slice", ("cofactor_slice_marginal", "proper_slice_count"), 42),
        ("lcm", ("cofactor_slice_marginal", "lcm_G_equals_P"), False),
        ("rank", ("source_consequence", "zero_anchored_rank"), 6),
        ("ledger", ("impact", "ledger_movement"), 1),
        ("credit", ("v4_chronology", "signed_Xi46_payment"), True),
        ("source-hash", ("source_bindings", 0, "sha256"), "0" * 64),
    ]
    passed = 0
    for label, path, value in mutations:
        candidate = copy.deepcopy(manifest)
        target: Any = candidate
        for component in path[:-1]:
            target = target[component]
        target[path[-1]] = value
        candidate = seal(candidate)
        try:
            validate_payload(candidate)
        except VerificationError:
            passed += 1
            continue
        raise VerificationError(f"semantic mutation accepted: {label}")

    hostile = [
        b'{"a":1,"a":1}\n',
        b'{"a":1.0}\n',
        b'{"a":NaN}\n',
        b'{"a":"\\u00e9"}\n ',
        b'{"a":1} \n',
        b'[]\n',
    ]
    for index, raw in enumerate(hostile):
        try:
            decode(raw, canonical=True)
        except VerificationError:
            passed += 1
            continue
        raise VerificationError(f"hostile JSON accepted: {index}")
    print(f"[PASS] packet mutations {passed}/{len(mutations) + len(hostile)}")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument(
        "--skip-predecessors",
        action="store_true",
        help="Developer-only narrow replay; the default packet is cumulative.",
    )
    arguments = parser.parse_args()

    if arguments.tamper_selftest:
        run_tamper_selftest()
        return 0

    schema = load(SCHEMA_PATH, canonical=False)
    validate_schema(schema)
    manifest = load(MANIFEST_PATH)
    validate_payload(manifest)

    normal = decode(run([sys.executable, str(PRIMARY_PATH), "--json"]), canonical=True)
    optimized = decode(
        run([sys.executable, "-O", str(PRIMARY_PATH), "--json"]),
        canonical=True,
    )
    deep_exact(normal, optimized, "optimized")
    deep_exact(normal, manifest, "manifest")
    run([sys.executable, str(PRIMARY_PATH), "--check"])
    run([sys.executable, str(PRIMARY_PATH), "--tamper-selftest"])

    sage = decode(run(["/usr/local/bin/sage", str(SAGE_PATH)]), canonical=True)
    validate_sage(sage)

    if not arguments.skip_predecessors:
        for predecessor in PREDECESSOR_PACKETS:
            run([sys.executable, str(predecessor)])

    run_tamper_selftest()
    print(
        "[PASS] M31 weighted-head/interlaced-source packet "
        f"checks={CHECKS} payload={manifest['payload_sha256']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
