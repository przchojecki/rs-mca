#!/usr/bin/env python3
"""Verify the KoalaBear v4 abstract first-match/terminal route cut.

The exact theorem here is deliberately syntactic: for one finite abstract
record set it checks a fixed ``GF(p^6)`` coordinate encoding, deduplicates
charged slopes, applies the live ten-owner chronology to *declared*
candidates, and derives the cap-68/69 terminal collectively from complete
residue-line packets.  It does not validate mathematical membership in an
owner or local branch, construct the missing source-bound selector, or move
any ledger value.

Optimized execution is refused.  The script never writes a certificate;
``--print-template`` emits canonical JSON to stdout.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any, Callable


if not __debug__:
    raise RuntimeError("optimized execution is forbidden")


SCHEMA_ID = "rs-mca-kb-v4-source-map-class-compiler-v1"
COMPILER_ID = "KB_MCA_V4_SOURCE_MAP_CLASS_COMPILER_V1"
ARTIFACT_KIND = "ABSTRACT_FIRST_MATCH_AND_TERMINAL_SCHEMA_ROUTE_CUT"
ARCHITECTURE_ID = (
    "GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_"
    "TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1"
)
PARTITION_SHA256 = (
    "7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa"
)
UNIT = "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE"
QUANTIFIER = "ONE_ABSTRACT_RECORD_SET_IN_ONE_DECLARED_PROVENANCE_CONTEXT"

P = 2_130_706_433
Q = 93_571_093_019_388_561_295_270_373_781_649_880_353_786_165_192_103_559_169
N = 2_097_152
K = 1_048_576
AGREEMENT = 1_116_048
B_STAR = 274_980_728_111_395_087
U_PAID = 4_200_515_150_819_207
B_REMAINING = 270_780_212_960_575_880
OPEN_R_MIN = 134_943
OPEN_R_MAX = 213_050
OPEN_R_COUNT = OPEN_R_MAX - OPEN_R_MIN + 1
LATER_SLACK_COUNT = OPEN_R_MAX - OPEN_R_MIN
SCAN_R_MIN = 9_209
SCAN_R_MAX = 913_631
EQUALITY_R = OPEN_R_MIN
EQUALITY_S = 202_416
EQUALITY_E = 134_944
EQUALITY_C = 67_472
CARRIER_SIZE = 1_894_736
LOCATOR_DEGREE = 981_105
RANK_LE_TWO_CAP = 4_037_126_185_931_424
REQUIRED_LOCATOR_INCIDENCE_CAP = 275_995_141_152
SOURCE_MAP_CLASS_CAP = 68
SOURCE_MAP_CLASS_CAP_MARGIN = 292_758_501_275_736
GENERIC_KERNEL_FREE_CAP = 63
FIELD_EXTENSION_DEGREE = 6
FIELD_ENCODING_ID = "OPAQUE_GF_P6_FIXED_POWER_BASIS_V1"
SLOPE_ENCODING = "SIX_BASE_FIELD_COORDINATES_IN_FIXED_POWER_BASIS"
ABSTRACT_RECORD_MODE = "ABSTRACT_REGRESSION_ONLY"
RANK_LE_TWO_REGIME = "COMPLETE_RECIPROCAL_RANK_AT_MOST_TWO_ONLY"
RANK_THREE_REGIME = "COMPLETE_RECIPROCAL_RANK_THREE_ONLY"

ATOM_ORDER = ("U_paid", "U_Q", "U_BC", "U_new")
OWNER_ORDER = (
    "SOURCE_COORDINATE_TANGENT_IMAGE",
    "ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER",
    "ACTIVE_V4_PAIR_GLOBAL_BOUNDED_DEGREE_SOURCE_RATIONAL",
    "ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5_OR_RESIDUAL_BASE",
    "ACTIVE_V4_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST",
    "ACTIVE_V4_PAIR_GLOBAL_SOURCE_FROBENIUS_EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_9208",
    "ACTIVE_V4_FIRST_GAP_BASE_RATIONAL_SOURCE_PENCIL_IMAGE",
    "ACTIVE_V4_BOUNDARY_PREFIX_Q",
    "ACTIVE_V4_BALANCED_CORE",
    "UNPAID_V4_COMPLEMENT",
)
OWNER_TO_ATOM = {
    **{owner: "U_paid" for owner in OWNER_ORDER[:7]},
    OWNER_ORDER[7]: "U_Q",
    OWNER_ORDER[8]: "U_BC",
    OWNER_ORDER[9]: "U_new",
}
PAID_OWNERS = frozenset(OWNER_ORDER[:7])

ACTIVE_ONLY = "ACTIVE_PARTITION_ONLY"
HISTOGRAM_OUTSIDE = "HISTOGRAM_PAID_OUTSIDE_OPEN_INTERVAL"
RANK_LE_TWO = "EQUALITY_COMPLETE_RECIPROCAL_RANK_AT_MOST_TWO"
NORMALIZATION_EXCLUDED = "EQUALITY_NORMALIZATION_EXCLUDED_Q1_OR_SPLIT_DEGREE_2_TO_11"
LINE_OR_DECK_EXCLUDED = (
    "EQUALITY_Q6_U2_LINE_OR_CONIC_WITH_ONE_OR_TWO_DECK_BRANCH_POINTS_EXCLUDED"
)
P3C3_EXCLUDED = "EQUALITY_Q6_U2_CONIC_P3_PLUS_C3_EXCLUDED"
CONIC_P6 = "EQUALITY_Q6_U2_CONIC_P6"
CONIC_P2C4 = "EQUALITY_Q6_U2_CONIC_P2_PLUS_C4"
QUARTIC_SIMPLE = "EQUALITY_Q6_U2_QUARTIC_SIMPLE_VERTEX"
QUARTIC_DEGENERATE = "EQUALITY_Q6_U2_QUARTIC_REPEATED_OR_RAMIFIED"
NON_U2 = "EQUALITY_NON_U2_OR_U3_COMPONENT"
GENERAL_EXCESS = "EQUALITY_GENERAL_EXCESS_DELTA_AT_LEAST_E"
MAP_PACKET = "EQUALITY_RANK3_SOURCE_MAP_CLASS_PACKET"
LATER_SLACK = "LATER_SLACK_134944_TO_213050"

LOCAL_BRANCHES = (
    ACTIVE_ONLY,
    HISTOGRAM_OUTSIDE,
    RANK_LE_TWO,
    NORMALIZATION_EXCLUDED,
    LINE_OR_DECK_EXCLUDED,
    P3C3_EXCLUDED,
    CONIC_P6,
    CONIC_P2C4,
    QUARTIC_SIMPLE,
    QUARTIC_DEGENERATE,
    NON_U2,
    GENERAL_EXCESS,
    MAP_PACKET,
    LATER_SLACK,
)

LOCAL_TERMINALS = {
    HISTOGRAM_OUTSIDE: "DECLARED_UPSTREAM_POST_RECIPROCAL_HISTOGRAM_PAYMENT",
    RANK_LE_TWO: "DECLARED_UPSTREAM_COMPLETE_RECIPROCAL_RANK_AT_MOST_TWO_PAYMENT",
    NORMALIZATION_EXCLUDED: "DECLARED_UPSTREAM_NORMALIZATION_EXCLUSION",
    LINE_OR_DECK_EXCLUDED: (
        "DECLARED_UPSTREAM_Q6_U2_LINE_OR_ONE_TWO_DECK_BRANCH_EXCLUSION"
    ),
    P3C3_EXCLUDED: "DECLARED_UPSTREAM_Q6_U2_P3_PLUS_C3_EXCLUSION",
    CONIC_P6: "UNPAID_PRIMITIVE_Q6_U2_CONIC_P6",
    CONIC_P2C4: "UNPAID_PRIMITIVE_Q6_U2_CONIC_P2_PLUS_C4",
    QUARTIC_SIMPLE: "UNPAID_PRIMITIVE_Q6_U2_QUARTIC_SIMPLE_VERTEX",
    QUARTIC_DEGENERATE: "UNPAID_PRIMITIVE_Q6_U2_QUARTIC_REPEATED_OR_RAMIFIED",
    NON_U2: "UNPAID_PRIMITIVE_EQUALITY_NON_U2_OR_U3_COMPONENT",
    GENERAL_EXCESS: "UNPAID_PRIMITIVE_EQUALITY_GENERAL_EXCESS",
    LATER_SLACK: "UNPAID_PRIMITIVE_LATER_SLACK_134944_TO_213050",
}
MAP_PACKET_AT_MOST_68 = (
    "DECLARED_CONDITIONAL_SOURCE_MAP_PACKET_AT_MOST_68_NOT_GLOBALLY_BANKABLE"
)
MAP_PACKET_AT_LEAST_69 = "UNPAID_PRIMITIVE_SOURCE_MAP_PACKET_AT_LEAST_69"

REQUIRED_FLAGS = {
    HISTOGRAM_OUTSIDE: frozenset({"POST_RECIPROCAL_HISTOGRAM_TERMINAL_VERIFIED"}),
    RANK_LE_TWO: frozenset({"COMPLETE_RECIPROCAL_RANK_AT_MOST_TWO"}),
    NORMALIZATION_EXCLUDED: frozenset({"NORMALIZATION_Q1_OR_SPLIT_2_TO_11_EXCLUDED"}),
    LINE_OR_DECK_EXCLUDED: frozenset(
        {"Q6_U2_LINE_OR_CONIC_WITH_ONE_OR_TWO_DECK_BRANCH_POINTS_EXCLUDED"}
    ),
    P3C3_EXCLUDED: frozenset({"P3C3_ALL_60_LABELED_GRAPHS_EXCLUDED"}),
}

RANK_THREE_BRANCHES = frozenset(
    {
        NORMALIZATION_EXCLUDED,
        LINE_OR_DECK_EXCLUDED,
        P3C3_EXCLUDED,
        CONIC_P6,
        CONIC_P2C4,
        QUARTIC_SIMPLE,
        QUARTIC_DEGENERATE,
        NON_U2,
        GENERAL_EXCESS,
        MAP_PACKET,
    }
)
CHARGED_RECORD_BRANCHES = frozenset(
    {
        ACTIVE_ONLY,
        CONIC_P6,
        CONIC_P2C4,
        QUARTIC_SIMPLE,
        QUARTIC_DEGENERATE,
        NON_U2,
        GENERAL_EXCESS,
        MAP_PACKET,
        LATER_SLACK,
    }
)
IMPORTED_NONCHARGED_SCOPE_BRANCHES = frozenset(
    {
        HISTOGRAM_OUTSIDE,
        RANK_LE_TWO,
        NORMALIZATION_EXCLUDED,
        LINE_OR_DECK_EXCLUDED,
        P3C3_EXCLUDED,
    }
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_source_map_class_compiler_v1.schema.json"
)
NOTE_PATH = (
    ROOT
    / "experimental/notes/frontier-adjacent/"
    "kb_mca_v4_source_map_class_compiler_v1.md"
)
DEFAULT_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-source-map-class-compiler-v1/manifest.json"
)
ROW_MANIFEST_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-source-pencil-image-owner-v1/row_manifest.json"
)
ACTIVE_MANIFEST_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-source-pencil-image-owner-v1/manifest.json"
)

SOURCE_PATHS = (
    "experimental/grande_finale.tex",
    "experimental/notes/m1/m1_kb_rank9_deployed_source_incidence_contract_v1.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_post_reciprocal_kernel_plane_sweep_full_histogram_replay_v1.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_locator_cylinder_reduction_v1.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_residue_line_partition_reduction_v1.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_kernel_kronecker_source_normalization_v1.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_fixed_domain_rank16_normalization_v1.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_normalization_v2/README.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/README.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/target/q6_u2_two_signature_conic_elimination_target.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/target/q6_u2_star_quartic_elimination_target.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_p3c3_v1/README.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_source_map_class_compiler_v1.md",
)

UPSTREAM_ARTIFACTS = (
    (
        "active_row_manifest",
        "experimental/data/certificates/kb-mca-v4-first-gap-source-pencil-image-owner-v1/row_manifest.json",
    ),
    (
        "active_ledger_manifest",
        "experimental/data/certificates/kb-mca-v4-first-gap-source-pencil-image-owner-v1/manifest.json",
    ),
    (
        "post_reciprocal_histogram",
        "experimental/data/certificates/kb-mca-v4-post-reciprocal-kernel-plane-sweep-full-histogram-replay-v1/certificate.json",
    ),
    (
        "equality_locator_cylinder",
        "experimental/data/certificates/kb-mca-v4-equality-wall-locator-cylinder-reduction-v1/certificate.json",
    ),
    (
        "equality_residue_line",
        "experimental/data/certificates/kb-mca-v4-equality-wall-residue-line-partition-reduction-v1/certificate.json",
    ),
    (
        "equality_kernel_normalization",
        "experimental/data/certificates/kb-mca-v4-equality-wall-kernel-kronecker-source-normalization-v1/certificate.json",
    ),
    (
        "equality_fixed_domain",
        "experimental/data/certificates/kb-mca-v4-equality-wall-fixed-domain-rank16-normalization-v1/certificate.json",
    ),
    (
        "equality_normalization_metadata",
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_normalization_v2/metadata.json",
    ),
    (
        "q6_geometry_metadata",
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/metadata.json",
    ),
    (
        "q6_line_conic_certificate",
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/q6_u2_line_conic_quotient_certificate.json",
    ),
    (
        "q6_conic_orbits",
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/q6_u2_conic_graph_orbits.json",
    ),
    (
        "q6_quartic_orbits",
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/q6_u2_quartic_graph_orbits.json",
    ),
    (
        "p3c3_metadata",
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_p3c3_v1/metadata.json",
    ),
)


class VerificationError(RuntimeError):
    """Raised when a certificate or producer contract fails closed."""


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
        raise VerificationError("noncanonical JSON value") from exc
    return (text + "\n").encode("ascii")


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def digest_path(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def payload_digest(document: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(document)
    unsigned.pop("payload_sha256", None)
    return digest_bytes(canonical_json(unsigned))


def seal(document: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(document)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = payload_digest(result)
    return result


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_float(_value: str) -> Any:
    raise VerificationError("floating-point JSON is forbidden")


def reject_constant(_value: str) -> Any:
    raise VerificationError("NaN and infinity are forbidden")


def strict_load(path: Path, *, canonical: bool = True) -> dict[str, Any]:
    raw = path.read_bytes()
    require(len(raw) <= 64 * 1024 * 1024, f"file size: {path}")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"non-ASCII JSON: {path}") from exc
    value = json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )
    require(type(value) is dict, f"JSON object required: {path}")
    if canonical:
        require(raw == canonical_json(value), f"canonical JSON bytes: {path}")
    return value


def repo_path(value: str) -> Path:
    require(type(value) is str and value.isascii(), "source path ASCII")
    pure = PurePosixPath(value)
    require(not pure.is_absolute(), "source path relative")
    require("." not in pure.parts and ".." not in pure.parts, "canonical source path")
    path = ROOT.joinpath(*pure.parts)
    require(path.exists() and path.is_file(), f"source exists: {value}")
    require(not path.is_symlink(), f"source is not a symlink: {value}")
    require(path.resolve().is_relative_to(ROOT.resolve()), f"source contained: {value}")
    return path


def deep_exact(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"{path}: exact type")
    if type(expected) is dict:
        require(set(actual) == set(expected), f"{path}: exact keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"{path}: exact length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            deep_exact(left, right, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path}: exact value")


def partition_body(partition: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "atom_order",
        "chronology_stages",
        "owner_order",
        "residual_rule",
        "witness_exhaustive",
    )
    return {key: partition[key] for key in keys}


def validate_active_partition() -> dict[str, Any]:
    row = strict_load(ROW_MANIFEST_PATH, canonical=False)
    active = strict_load(ACTIVE_MANIFEST_PATH, canonical=False)
    require(row["architecture_id"] == ARCHITECTURE_ID, "row architecture")
    partition = row["partition"]
    require(tuple(partition["owner_order"]) == OWNER_ORDER, "active owner order")
    require(tuple(partition["atom_order"]) == ATOM_ORDER, "active atom order")
    computed = digest_bytes(canonical_json(partition_body(partition))[:-1])
    require(computed == PARTITION_SHA256, "active partition digest recomputation")
    require(partition["partition_sha256"] == PARTITION_SHA256, "active partition digest field")
    require(
        partition["residual_rule"] == "ITERATED_EXACT_SET_DIFFERENCE",
        "active residual rule",
    )
    require(partition["witness_exhaustive"] is True, "active partition exhaustion")
    require(active["architecture_id"] == ARCHITECTURE_ID, "ledger architecture")
    require(active["partition_sha256"] == PARTITION_SHA256, "ledger partition")
    require(active["closure_state"]["known_sum"] == U_PAID, "active U_paid")
    require(
        active["closure_state"]["remaining_budget_after_known_sum"] == B_REMAINING,
        "active reserve",
    )
    require(active["closure_state"]["row_closed"] is False, "active row remains open")
    return {"row": row, "active": active}


def source_bindings() -> list[dict[str, str]]:
    result = []
    for index, path_text in enumerate(SOURCE_PATHS):
        path = repo_path(path_text)
        result.append(
            {
                "binding_id": f"SOURCE_{index:02d}_{path.stem.upper().replace('-', '_')}",
                "path": path_text,
                "sha256": digest_path(path),
            }
        )
    return result


def upstream_bindings() -> list[dict[str, Any]]:
    result = []
    for role, path_text in UPSTREAM_ARTIFACTS:
        path = repo_path(path_text)
        document = strict_load(path, canonical=False)
        result.append(
            {
                "role": role,
                "path": path_text,
                "file_sha256": digest_path(path),
                "payload_sha256_or_null": document.get("payload_sha256"),
                "status_or_null": document.get("status"),
            }
        )
    return result


def is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def slope_key(coordinates: Any) -> tuple[int, ...]:
    require(
        type(coordinates) is list and len(coordinates) == FIELD_EXTENSION_DEGREE,
        "slope has six fixed-basis coordinates",
    )
    result = []
    for coordinate in coordinates:
        require(
            type(coordinate) is int and not isinstance(coordinate, bool),
            "slope coordinate type",
        )
        require(0 <= coordinate < P, "slope coordinate range")
        result.append(coordinate)
    return tuple(result)


def projective_key(vector: list[int], modulus: int) -> str:
    require(modulus == P, "projective modulus is the fixed base prime")
    require(type(vector) is list and len(vector) == 3, "projective vector length")
    normalized = []
    for entry in vector:
        require(type(entry) is int and not isinstance(entry, bool), "projective entry type")
        require(0 <= entry < modulus, "projective entry range")
        normalized.append(entry)
    pivot = next((entry for entry in normalized if entry != 0), None)
    require(pivot is not None, "projective vector nonzero")
    inverse = pow(pivot, modulus - 2, modulus)
    return ":".join(str((entry * inverse) % modulus) for entry in normalized)


RECORD_KEYS = {
    "witness_id",
    "graph_record_id",
    "received_line_id",
    "source_id",
    "selector_id",
    "context_digest",
    "slope_coordinates",
    "r",
    "local_branch",
    "residue_line_id_or_null",
    "source_map_packet_id_or_null",
    "source_map_packet_exhaustive",
    "residue_direction_modulus",
    "residue_direction_vector",
    "declared_rational_source_map_class_id",
    "declared_support_id",
    "declared_codeword_id",
    "declared_error_values_id",
    "declared_error_support_id",
    "declared_deficit",
    "declared_z_coordinates_id",
    "declared_split_squarefree_locator_id",
    "declared_locator_equation_id",
    "declared_delta_nonzero_id",
    "declared_locator_kernel_equation_id",
    "declared_locator_nondegeneracy_id",
    "declared_moving_root_equation_id",
    "declared_moving_root_bridge",
    "declared_source_compatible",
    "declared_branch_evidence_flags",
    "declared_owner_candidates",
}
CLAIM_KEYS = {
    "owner_id",
    "graph_record_id",
    "declared_evidence_id",
    "target_received_line_id",
    "target_slope_coordinates",
}
PRODUCER_KEYS = {"schema", "context", "records"}
SOURCE_CONTEXT_KEYS = {
    "f",
    "g",
    "V",
    "H_V",
    "K0",
    "d_V",
    "y0",
    "y1",
    "H1",
    "H2",
    "u",
    "v",
    "c0",
    "c1",
    "epsilon0",
    "epsilon1",
    "Sigma",
    "K0_basis_r1_through_r8",
    "transverse_two_column_condition",
    "affine_difference_rank",
    "column_rank",
    "K0_equals_D_intersection_KV",
    "dimension_K0",
}
CONTEXT_KEYS = {
    "architecture_id",
    "partition_sha256",
    "unit",
    "quantifier",
    "received_line_id",
    "source_id",
    "selector_id",
    "context_digest",
    "record_mode",
    "field_base_prime",
    "field_extension_degree",
    "field_encoding_id",
    "extension_modulus_sha256",
    "basis_sha256",
    "domain_generator_sha256",
    "slope_encoding",
    "complete_reciprocal_rank_regime",
    "declared_source_context_bindings",
    "declared_complete_selector",
    "declared_selector_universe_exhaustive",
    "declared_same_H_V_for_all_records",
    "declared_same_K0_for_all_records",
    "declared_same_domain_for_all_records",
    "semantic_evidence_validation_present",
}

LOCAL_EVIDENCE_ROLE = {
    HISTOGRAM_OUTSIDE: "post_reciprocal_histogram",
    RANK_LE_TWO: "equality_locator_cylinder",
    NORMALIZATION_EXCLUDED: "equality_normalization_metadata",
    LINE_OR_DECK_EXCLUDED: "q6_line_conic_certificate",
    P3C3_EXCLUDED: "p3c3_metadata",
    CONIC_P6: "q6_conic_orbits",
    CONIC_P2C4: "q6_conic_orbits",
    QUARTIC_SIMPLE: "q6_quartic_orbits",
    QUARTIC_DEGENERATE: "q6_quartic_orbits",
    NON_U2: "q6_geometry_metadata",
    GENERAL_EXCESS: "q6_geometry_metadata",
    MAP_PACKET: "equality_residue_line",
    LATER_SLACK: "post_reciprocal_histogram",
}


def validate_branch(
    branch: str,
    r: int,
    flags: frozenset[str],
    rank_regime: str,
) -> None:
    require(branch in CHARGED_RECORD_BRANCHES, "charged-record branch")
    require(SCAN_R_MIN <= r <= SCAN_R_MAX, "r lies in the proved scan universe")
    if branch == ACTIVE_ONLY:
        require(not flags, "active-only branch has no local proof flags")
        return
    if branch == LATER_SLACK:
        require(OPEN_R_MIN < r <= OPEN_R_MAX, "later-slack interval")
    else:
        require(r == EQUALITY_R, "equality branch r")
    required = REQUIRED_FLAGS.get(branch, frozenset())
    require(required <= flags, f"required proof flags: {branch}")
    require(flags == required, f"no unrecognized proof flags: {branch}")
    if branch in RANK_THREE_BRANCHES:
        require(rank_regime == RANK_THREE_REGIME, "rank-three packet regime")


def terminal_for(owner: str, branch: str) -> tuple[str | None, bool]:
    if owner in PAID_OWNERS:
        require(branch == ACTIVE_ONLY, "paid active owner cannot import local branch")
        return f"DECLARED_ACTIVE_FIRST_MATCH_OWNER::{owner}", True
    if owner == OWNER_ORDER[7]:
        require(branch == ACTIVE_ONLY, "U_Q owner cannot import local branch")
        return "DECLARED_UNPAID_ACTIVE_OWNER::ACTIVE_V4_BOUNDARY_PREFIX_Q", False
    if owner == OWNER_ORDER[8]:
        require(branch == ACTIVE_ONLY, "U_BC owner cannot import local branch")
        return "DECLARED_UNPAID_ACTIVE_OWNER::ACTIVE_V4_BALANCED_CORE", False
    require(owner == OWNER_ORDER[9], "only final complement may be locally refined")
    require(branch != ACTIVE_ONLY, "final complement requires explicit local terminal")
    if branch == MAP_PACKET:
        return None, False
    return LOCAL_TERMINALS[branch], False


def compile_records(producer: dict[str, Any]) -> dict[str, Any]:
    require(set(producer) == PRODUCER_KEYS, "producer top-level keys")
    require(producer["schema"] == SCHEMA_ID + "-producer-records", "producer schema")
    context = producer["context"]
    require(type(context) is dict and set(context) == CONTEXT_KEYS, "producer context keys")
    require(context["architecture_id"] == ARCHITECTURE_ID, "producer architecture")
    require(context["partition_sha256"] == PARTITION_SHA256, "producer partition")
    require(context["unit"] == UNIT, "producer unit")
    require(context["quantifier"] == QUANTIFIER, "producer quantifier")
    require(context["record_mode"] == ABSTRACT_RECORD_MODE, "abstract-only record mode")
    require(context["field_base_prime"] == P, "fixed field base prime")
    require(
        context["field_extension_degree"] == FIELD_EXTENSION_DEGREE,
        "fixed field extension degree",
    )
    require(context["field_encoding_id"] == FIELD_ENCODING_ID, "fixed field encoding id")
    require(context["slope_encoding"] == SLOPE_ENCODING, "fixed slope encoding")
    for key in (
        "extension_modulus_sha256",
        "basis_sha256",
        "domain_generator_sha256",
    ):
        require(is_sha256(context[key]), f"context SHA-256: {key}")
    rank_regime = context["complete_reciprocal_rank_regime"]
    require(rank_regime == RANK_THREE_REGIME, "rank-three charged-record regime")
    for key in ("received_line_id", "source_id", "selector_id", "context_digest"):
        require(type(context[key]) is str and bool(context[key]), f"context string: {key}")
    source_context = context["declared_source_context_bindings"]
    require(
        type(source_context) is dict and set(source_context) == SOURCE_CONTEXT_KEYS,
        "declared source-context binding keys",
    )
    for key, value in source_context.items():
        if key == "d_V":
            require(
                type(value) is int and not isinstance(value, bool) and value >= 0,
                "declared d_V",
            )
        elif key == "K0_basis_r1_through_r8":
            require(
                type(value) is list
                and len(value) == 8
                and all(type(entry) is str and bool(entry) for entry in value),
                "declared K0 basis",
            )
        elif key in {
            "transverse_two_column_condition",
            "K0_equals_D_intersection_KV",
        }:
            require(value is True, f"declared source predicate: {key}")
        elif key == "affine_difference_rank":
            require(value == 9, "declared affine-difference rank")
        elif key == "column_rank":
            require(value == 10, "declared column rank")
        elif key == "dimension_K0":
            require(value == 8, "declared K0 dimension")
        else:
            require(type(value) is str and bool(value), f"declared source binding: {key}")
    for key in (
        "declared_complete_selector",
        "declared_selector_universe_exhaustive",
        "declared_same_H_V_for_all_records",
        "declared_same_K0_for_all_records",
        "declared_same_domain_for_all_records",
    ):
        require(context[key] is True, f"declared producer context assertion: {key}")
    require(
        context["semantic_evidence_validation_present"] is False,
        "semantic evidence is explicitly unvalidated",
    )

    records = producer["records"]
    require(type(records) is list and bool(records), "nonempty producer records")
    witnesses: set[str] = set()
    grouped: dict[tuple[int, ...], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        require(type(record) is dict and set(record) == RECORD_KEYS, "record exact keys")
        witness_id = record["witness_id"]
        require(type(witness_id) is str and bool(witness_id), "witness id")
        require(witness_id not in witnesses, "witness id unique")
        witnesses.add(witness_id)
        for key in ("graph_record_id", "received_line_id", "source_id", "selector_id", "context_digest"):
            require(type(record[key]) is str and bool(record[key]), f"record string: {key}")
        require(record["received_line_id"] == context["received_line_id"], "same received line")
        require(record["source_id"] == context["source_id"], "same source")
        require(record["selector_id"] == context["selector_id"], "same selector")
        require(record["context_digest"] == context["context_digest"], "same context digest")
        for key in (
            "declared_support_id",
            "declared_codeword_id",
            "declared_error_values_id",
            "declared_error_support_id",
            "declared_z_coordinates_id",
            "declared_split_squarefree_locator_id",
            "declared_locator_equation_id",
            "declared_delta_nonzero_id",
            "declared_locator_kernel_equation_id",
            "declared_locator_nondegeneracy_id",
            "declared_moving_root_equation_id",
        ):
            require(type(record[key]) is str and bool(record[key]), f"record declaration: {key}")
        require(
            type(record["declared_deficit"]) is int
            and not isinstance(record["declared_deficit"], bool)
            and record["declared_deficit"] >= 0,
            "declared deficit",
        )
        require(record["declared_moving_root_bridge"] is True, "declared moving-root bridge")
        require(record["declared_source_compatible"] is True, "declared source compatibility")
        slope = slope_key(record["slope_coordinates"])
        r = record["r"]
        require(type(r) is int and not isinstance(r, bool), "r integer")
        flags_raw = record["declared_branch_evidence_flags"]
        require(type(flags_raw) is list, "declared branch-evidence flags list")
        require(
            all(type(flag) is str and bool(flag) for flag in flags_raw),
            "declared branch-evidence flag strings",
        )
        require(len(flags_raw) == len(set(flags_raw)), "declared branch-evidence flags unique")
        flags = frozenset(flags_raw)
        branch = record["local_branch"]
        validate_branch(branch, r, flags, rank_regime)
        residue_line_id = record["residue_line_id_or_null"]
        packet_id = record["source_map_packet_id_or_null"]
        packet_exhaustive = record["source_map_packet_exhaustive"]
        if branch == MAP_PACKET:
            require(
                type(residue_line_id) is str and bool(residue_line_id),
                "map packet residue-line id",
            )
            require(type(packet_id) is str and bool(packet_id), "map packet id")
            require(packet_exhaustive is True, "declared complete map packet")
        else:
            require(residue_line_id is None, "non-packet residue-line id is null")
            require(packet_id is None, "non-packet source-map packet id is null")
            require(packet_exhaustive is False, "non-packet exhaustiveness is false")
        residue_direction_key = projective_key(
            record["residue_direction_vector"],
            record["residue_direction_modulus"],
        )
        source_map_class_id = record["declared_rational_source_map_class_id"]
        require(
            type(source_map_class_id) is str and bool(source_map_class_id),
            "declared rational source-map class id",
        )
        claims = record["declared_owner_candidates"]
        require(type(claims) is list and bool(claims), "declared owner candidates nonempty")
        claim_owners = set()
        for claim in claims:
            require(type(claim) is dict and set(claim) == CLAIM_KEYS, "owner claim keys")
            owner = claim["owner_id"]
            require(owner in OWNER_ORDER, "owner in active chronology")
            require(owner not in claim_owners, "owner claim unique per witness")
            claim_owners.add(owner)
            require(
                claim["graph_record_id"] == record["graph_record_id"],
                "declared owner retained at same graph record",
            )
            require(
                type(claim["declared_evidence_id"]) is str
                and bool(claim["declared_evidence_id"]),
                "declared owner evidence id",
            )
            require(
                claim["target_received_line_id"] == record["received_line_id"],
                "declared owner target retained at same line",
            )
            require(
                slope_key(claim["target_slope_coordinates"]) == slope,
                "declared owner target retained at same slope",
            )
        prepared = copy.deepcopy(record)
        prepared["_slope_key"] = slope
        prepared["_residue_direction_key"] = residue_direction_key
        grouped[slope].append(prepared)

    classifications: list[dict[str, Any]] = []
    residue_direction_to_slopes: dict[str, set[tuple[int, ...]]] = defaultdict(set)
    for slope in sorted(grouped):
        group = grouped[slope]
        branches = {record["local_branch"] for record in group}
        rs = {record["r"] for record in group}
        residue_direction_keys = {
            record["_residue_direction_key"] for record in group
        }
        source_map_class_ids = {
            record["declared_rational_source_map_class_id"] for record in group
        }
        graph_records = {record["graph_record_id"] for record in group}
        flags = {tuple(record["declared_branch_evidence_flags"]) for record in group}
        residue_lines = {record["residue_line_id_or_null"] for record in group}
        packet_ids = {record["source_map_packet_id_or_null"] for record in group}
        packet_exhaustive_values = {
            record["source_map_packet_exhaustive"] for record in group
        }
        require(len(branches) == 1, "one branch per slope")
        require(len(rs) == 1, "one r per slope")
        require(
            len(residue_direction_keys) == 1,
            "one projective residue direction per slope",
        )
        require(
            len(source_map_class_ids) == 1,
            "one declared rational source-map class per slope",
        )
        require(len(graph_records) == 1, "one canonical graph record per slope")
        require(len(flags) == 1, "one declared branch-evidence record per slope")
        require(len(residue_lines) == 1, "one residue line per slope")
        require(len(packet_ids) == 1, "one source-map packet per slope")
        require(len(packet_exhaustive_values) == 1, "one packet-exhaustiveness value per slope")
        candidates = {
            claim["owner_id"]
            for record in group
            for claim in record["declared_owner_candidates"]
        }
        require(bool(candidates), "at least one declared owner candidate per slope")
        selected_owner = next(owner for owner in OWNER_ORDER if owner in candidates)
        branch = next(iter(branches))
        terminal, paid = terminal_for(selected_owner, branch)
        residue_direction_key = next(iter(residue_direction_keys))
        source_map_class_id = next(iter(source_map_class_ids))
        residue_direction_to_slopes[residue_direction_key].add(slope)
        classifications.append(
            {
                "slope_coordinates": list(slope),
                "r": next(iter(rs)),
                "graph_record_id": next(iter(graph_records)),
                "witness_count": len(group),
                "projective_residue_direction_key": residue_direction_key,
                "declared_rational_source_map_class_id": source_map_class_id,
                "declared_owner_candidates": [
                    owner for owner in OWNER_ORDER if owner in candidates
                ],
                "selected_declared_owner": selected_owner,
                "atom_id": OWNER_TO_ATOM[selected_owner],
                "would_route_to_paid_active_owner_if_semantically_certified": paid,
                "local_branch": branch,
                "residue_line_id_or_null": next(iter(residue_lines)),
                "source_map_packet_id_or_null": next(iter(packet_ids)),
                "source_map_packet_exhaustive": next(iter(packet_exhaustive_values)),
                "terminal": terminal,
            }
        )

    packet_ids_by_residue_line: dict[str, set[str]] = defaultdict(set)
    packet_rows: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in classifications:
        if row["local_branch"] == MAP_PACKET:
            packet_ids_by_residue_line[row["residue_line_id_or_null"]].add(
                row["source_map_packet_id_or_null"]
            )
            packet_rows[
                (
                    row["residue_line_id_or_null"],
                    row["source_map_packet_id_or_null"],
                )
            ].append(row)
    require(
        all(len(packet_ids) == 1 for packet_ids in packet_ids_by_residue_line.values()),
        "one declared exhaustive packet per residue line per invocation",
    )
    packet_summaries = []
    for (residue_line_id, packet_id), rows in sorted(packet_rows.items()):
        require(
            all(row["source_map_packet_exhaustive"] is True for row in rows),
            "map packet declared exhaustive",
        )
        class_count = len(
            {row["declared_rational_source_map_class_id"] for row in rows}
        )
        terminal = (
            MAP_PACKET_AT_MOST_68
            if class_count <= SOURCE_MAP_CLASS_CAP
            else MAP_PACKET_AT_LEAST_69
        )
        for row in rows:
            require(row["terminal"] is None, "map packet terminal derived collectively")
            row["terminal"] = terminal
        packet_summaries.append(
            {
                "residue_line_id": residue_line_id,
                "source_map_packet_id": packet_id,
                "declared_exhaustive": True,
                "distinct_charged_slopes": len(rows),
                "distinct_declared_rational_source_map_classes": class_count,
                "derived_terminal": terminal,
            }
        )
    require(all(row["terminal"] is not None for row in classifications), "all terminals explicit")

    terminal_histogram = Counter(row["terminal"] for row in classifications)
    owner_histogram = Counter(row["selected_declared_owner"] for row in classifications)
    direction_multiplicities = sorted(
        len(slopes) for slopes in residue_direction_to_slopes.values()
    )
    shared_direction_slopes = sum(
        size for size in direction_multiplicities if size > 1
    )
    selection_digest = digest_bytes(canonical_json(classifications))
    return {
        "classifications": classifications,
        "diagnostics": {
            "raw_witness_records": len(records),
            "distinct_charged_slopes": len(classifications),
            "duplicate_witness_records_removed": len(records) - len(classifications),
            "distinct_projective_residue_directions": len(
                residue_direction_to_slopes
            ),
            "projective_residue_direction_multiplicities": direction_multiplicities,
            "slopes_in_shared_projective_residue_directions": shared_direction_slopes,
            "distinct_slopes_collapsed_by_residue_direction": 0,
            "owner_histogram": dict(sorted(owner_histogram.items())),
            "terminal_histogram": dict(sorted(terminal_histogram.items())),
            "source_map_packets": packet_summaries,
            "selection_sha256": selection_digest,
        },
    }


def claim(
    owner: str,
    graph_record_id: str,
    received_line_id: str,
    slope_coordinates: list[int],
) -> dict[str, Any]:
    return {
        "owner_id": owner,
        "graph_record_id": graph_record_id,
        "declared_evidence_id": f"fixture-evidence::{graph_record_id}::{owner}",
        "target_received_line_id": received_line_id,
        "target_slope_coordinates": copy.deepcopy(slope_coordinates),
    }


def fixture_slope(index: int) -> list[int]:
    require(type(index) is int and 0 <= index < P, "fixture slope index")
    return [index, 0, 0, 0, 0, 0]


def fixture_record(
    case_id: str,
    witness_id: str,
    graph_record_id: str,
    slope_coordinates: list[int],
    r: int,
    branch: str,
    vector: list[int],
    owners: list[str],
    flags: list[str] | None = None,
    *,
    residue_line_id: str | None = None,
    packet_id: str | None = None,
    source_map_class_id: str | None = None,
) -> dict[str, Any]:
    is_packet = branch == MAP_PACKET
    require(is_packet == (residue_line_id is not None), "fixture residue-line metadata")
    require(is_packet == (packet_id is not None), "fixture packet metadata")
    return {
        "witness_id": witness_id,
        "graph_record_id": graph_record_id,
        "received_line_id": f"fixture-line::{case_id}",
        "source_id": f"fixture-source::{case_id}",
        "selector_id": f"fixture-selector::{case_id}",
        "context_digest": f"fixture-context::{case_id}",
        "slope_coordinates": slope_coordinates,
        "r": r,
        "local_branch": branch,
        "residue_line_id_or_null": residue_line_id,
        "source_map_packet_id_or_null": packet_id,
        "source_map_packet_exhaustive": is_packet,
        "residue_direction_modulus": P,
        "residue_direction_vector": vector,
        "declared_rational_source_map_class_id": (
            f"fixture-source-map-class::{graph_record_id}"
            if source_map_class_id is None
            else source_map_class_id
        ),
        "declared_support_id": f"fixture-support::{witness_id}",
        "declared_codeword_id": f"fixture-codeword::{witness_id}",
        "declared_error_values_id": f"fixture-errors::{witness_id}",
        "declared_error_support_id": f"fixture-error-support::{witness_id}",
        "declared_deficit": 0,
        "declared_z_coordinates_id": f"fixture-z-coordinates::{witness_id}",
        "declared_split_squarefree_locator_id": f"fixture-locator::{witness_id}",
        "declared_locator_equation_id": f"fixture-locator::{witness_id}",
        "declared_delta_nonzero_id": f"fixture-delta-nonzero::{witness_id}",
        "declared_locator_kernel_equation_id": (
            f"fixture-locator-kernel::{witness_id}"
        ),
        "declared_locator_nondegeneracy_id": (
            f"fixture-locator-nondegenerate::{witness_id}"
        ),
        "declared_moving_root_equation_id": f"fixture-moving-root::{witness_id}",
        "declared_moving_root_bridge": True,
        "declared_source_compatible": True,
        "declared_branch_evidence_flags": [] if flags is None else flags,
        "declared_owner_candidates": [
            claim(
                owner,
                graph_record_id,
                f"fixture-line::{case_id}",
                slope_coordinates,
            )
            for owner in owners
        ],
    }


def fixture_context(case_id: str, rank_regime: str) -> dict[str, Any]:
    return {
        "architecture_id": ARCHITECTURE_ID,
        "partition_sha256": PARTITION_SHA256,
        "unit": UNIT,
        "quantifier": QUANTIFIER,
        "received_line_id": f"fixture-line::{case_id}",
        "source_id": f"fixture-source::{case_id}",
        "selector_id": f"fixture-selector::{case_id}",
        "context_digest": f"fixture-context::{case_id}",
        "record_mode": ABSTRACT_RECORD_MODE,
        "field_base_prime": P,
        "field_extension_degree": FIELD_EXTENSION_DEGREE,
        "field_encoding_id": FIELD_ENCODING_ID,
        "extension_modulus_sha256": "1" * 64,
        "basis_sha256": "2" * 64,
        "domain_generator_sha256": "3" * 64,
        "slope_encoding": SLOPE_ENCODING,
        "complete_reciprocal_rank_regime": rank_regime,
        "declared_source_context_bindings": {
            "f": f"fixture-f::{case_id}",
            "g": f"fixture-g::{case_id}",
            "V": f"fixture-V::{case_id}",
            "H_V": f"fixture-HV::{case_id}",
            "K0": f"fixture-K0::{case_id}",
            "d_V": LOCATOR_DEGREE,
            "y0": f"fixture-y0::{case_id}",
            "y1": f"fixture-y1::{case_id}",
            "H1": f"fixture-H1::{case_id}",
            "H2": f"fixture-H2::{case_id}",
            "u": f"fixture-u::{case_id}",
            "v": f"fixture-v::{case_id}",
            "c0": f"fixture-c0::{case_id}",
            "c1": f"fixture-c1::{case_id}",
            "epsilon0": f"fixture-epsilon0::{case_id}",
            "epsilon1": f"fixture-epsilon1::{case_id}",
            "Sigma": f"fixture-Sigma::{case_id}",
            "K0_basis_r1_through_r8": [
                f"fixture-r{index}::{case_id}" for index in range(1, 9)
            ],
            "transverse_two_column_condition": True,
            "affine_difference_rank": 9,
            "column_rank": 10,
            "K0_equals_D_intersection_KV": True,
            "dimension_K0": 8,
        },
        "declared_complete_selector": True,
        "declared_selector_universe_exhaustive": True,
        "declared_same_H_V_for_all_records": True,
        "declared_same_K0_for_all_records": True,
        "declared_same_domain_for_all_records": True,
        "semantic_evidence_validation_present": False,
    }


def fixture_producer() -> dict[str, Any]:
    case_id = "rank-three"
    complement = OWNER_ORDER[-1]
    records = [
        fixture_record(case_id, "w0a", "g0", fixture_slope(0), EQUALITY_R, ACTIVE_ONLY, [1, 0, 1], [OWNER_ORDER[4], complement]),
        fixture_record(case_id, "w0b", "g0", fixture_slope(0), EQUALITY_R, ACTIVE_ONLY, [2, 0, 2], [OWNER_ORDER[0], complement]),
        fixture_record(case_id, "w1a", "g1", fixture_slope(1), EQUALITY_R, CONIC_P6, [1, 2, 3], [complement]),
        fixture_record(case_id, "w1b", "g1", fixture_slope(1), EQUALITY_R, CONIC_P6, [2, 4, 6], [complement]),
        fixture_record(case_id, "w2", "g2", fixture_slope(2), EQUALITY_R, CONIC_P2C4, [3, 6, 9], [complement]),
        fixture_record(case_id, "w3", "g3", fixture_slope(3), EQUALITY_R, ACTIVE_ONLY, [1, 1, 0], [OWNER_ORDER[7], complement]),
        fixture_record(case_id, "w4", "g4", fixture_slope(4), EQUALITY_R, ACTIVE_ONLY, [1, 1, 1], [OWNER_ORDER[8], complement]),
        fixture_record(case_id, "w5", "g5", fixture_slope(5), 134_944, LATER_SLACK, [1, 1, 2], [complement]),
        fixture_record(case_id, "w10", "g10", fixture_slope(10), EQUALITY_R, QUARTIC_SIMPLE, [1, 1, 7], [complement]),
        fixture_record(case_id, "w11", "g11", fixture_slope(11), EQUALITY_R, QUARTIC_DEGENERATE, [1, 1, 8], [complement]),
        fixture_record(case_id, "w12", "g12", fixture_slope(12), EQUALITY_R, NON_U2, [1, 1, 9], [complement]),
        fixture_record(case_id, "w13", "g13", fixture_slope(13), EQUALITY_R, GENERAL_EXCESS, [1, 1, 10], [complement]),
    ]
    for index in range(3):
        records.append(
            fixture_record(
                case_id,
                f"w-small-{index}",
                f"g-small-{index}",
                fixture_slope(100 + index),
                EQUALITY_R,
                MAP_PACKET,
                [1, 100 + index, 1],
                [complement],
                residue_line_id="fixture-residue-small",
                packet_id="fixture-packet-small",
                source_map_class_id=f"fixture-small-class::{index}",
            )
        )
    for index in range(69):
        records.append(
            fixture_record(
                case_id,
                f"w-large-{index}",
                f"g-large-{index}",
                fixture_slope(200 + index),
                EQUALITY_R,
                MAP_PACKET,
                [1, 1_000 + index, 1],
                [complement],
                residue_line_id="fixture-residue-large",
                packet_id="fixture-packet-large",
                source_map_class_id=f"fixture-large-class::{index}",
            )
        )
    return {
        "schema": SCHEMA_ID + "-producer-records",
        "context": fixture_context(case_id, RANK_THREE_REGIME),
        "records": records,
    }


def geometry_inventory() -> dict[str, Any]:
    conic_path = repo_path(
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/"
        "experiments/q6_u2_conic_graph_orbits.json"
    )
    quartic_path = repo_path(
        "experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/"
        "experiments/q6_u2_quartic_graph_orbits.json"
    )
    conic = strict_load(conic_path, canonical=False)
    quartic = strict_load(quartic_path, canonical=False)
    require(conic["claims"]["pre_star_geometry_labeled_cases"] == 465, "conic pre-star count")
    require(conic["claims"]["reduced_conic_labeled_cases"] == 405, "conic reduced count")
    require(conic["claims"]["P3_PLUS_C3_status"] == "PROVED_IMPOSSIBLE", "P3C3 status")
    require(
        conic["claims"]["surviving_signature_graphs"] == ["P6", "P2_PLUS_C4"],
        "conic surviving signatures",
    )
    conic_open_after_p3c3 = []
    endpoint_orbits = []
    reciprocal_orbits = []
    for row in conic["classification"]:
        signature_orbits = row["open_signature_orbit_histogram"]
        conic_open_after_p3c3.append(row["open_orbits"] - signature_orbits["P3_PLUS_C3"])
        endpoint_orbits.append(row["free_pair_quotient"]["open_orbits"])
        reciprocal_orbits.append(row["free_pair_quotient"]["reciprocal_open_orbits"])
    require(conic_open_after_p3c3 == [46, 30, 10, 10], "conic residual orbit counts")
    require(endpoint_orbits == [3, 3, 2, 1], "endpoint orbit counts")
    require(reciprocal_orbits == [2, 2, 1, 1], "reciprocal endpoint orbit counts")
    quartic_open = [row["open_representative_count"] for row in quartic["classification"]]
    require(quartic_open == [985, 488, 188, 77], "quartic residual orbit counts")
    return {
        "normalization_surviving_split_degrees": [12, 13, 14, 15, 16],
        "q6_u2_conic": {
            "pre_star_labeled_cases": 465,
            "p3c3_excluded_labeled_cases": 60,
            "surviving_labeled_cases": 405,
            "surviving_signatures": ["P6", "P2_PLUS_C4"],
            "pole_partitions": [[6], [4, 2], [3, 3], [2, 2, 2]],
            "surviving_orbits_after_p3c3": conic_open_after_p3c3,
            "endpoint_pair_orbits": endpoint_orbits,
            "reciprocal_endpoint_pair_orbits": reciprocal_orbits,
        },
        "q6_u2_quartic": {
            "open_simple_vertex_orbits": quartic_open,
            "repeated_or_ramified_branch": "OPEN",
        },
        "scope_warning": (
            "The conic orbit totals are local symmetry quotients and are not a "
            "partition or census of all slopes on a received line."
        ),
    }


def terminal_registry() -> list[dict[str, Any]]:
    result = []
    for owner in OWNER_ORDER:
        if owner in PAID_OWNERS:
            status = "EXISTING_ACTIVE_PAID_OWNER"
        elif owner in OWNER_ORDER[7:9]:
            status = "EXISTING_ACTIVE_UNPAID_OWNER"
        else:
            status = "FINAL_ACTIVE_UNPAID_COMPLEMENT_REFINED_BELOW"
        result.append(
            {
                "kind": "ACTIVE_FIRST_MATCH_OWNER",
                "owner_id": owner,
                "atom_id": OWNER_TO_ATOM[owner],
                "status": status,
            }
        )
    for branch in LOCAL_BRANCHES[1:]:
        if branch == MAP_PACKET:
            result.extend(
                [
                    {
                        "kind": "ABSTRACT_COLLECTIVE_PACKET_THRESHOLD",
                        "local_branch": branch,
                        "terminal": MAP_PACKET_AT_MOST_68,
                        "status": "CONDITIONAL_SYNTAX_ONLY_NOT_GLOBALLY_BANKABLE",
                    },
                    {
                        "kind": "ABSTRACT_COLLECTIVE_PACKET_THRESHOLD",
                        "local_branch": branch,
                        "terminal": MAP_PACKET_AT_LEAST_69,
                        "status": "EXPLICIT_UNPAID_PRIMITIVE",
                    },
                ]
            )
            continue
        terminal = LOCAL_TERMINALS[branch]
        if branch in IMPORTED_NONCHARGED_SCOPE_BRANCHES:
            kind = "IMPORTED_NONCHARGED_SCOPE_DECLARATION"
            status = "UPSTREAM_SCOPE_BOUND_BUT_RECORD_MEMBERSHIP_UNVALIDATED"
        else:
            kind = "ABSTRACT_CHARGED_RECORD_TERMINAL"
            status = "EXPLICIT_UNPAID_PRIMITIVE"
        result.append(
            {
                "kind": kind,
                "local_branch": branch,
                "terminal": terminal,
                "status": status,
            }
        )
    return result


def expected_manifest() -> dict[str, Any]:
    validate_active_partition()
    fixture = fixture_producer()
    compiled = compile_records(copy.deepcopy(fixture))
    classifications = compiled["classifications"]
    by_slope = {
        tuple(row["slope_coordinates"]): row for row in classifications
    }
    packet_by_id = {
        row["source_map_packet_id"]: row
        for row in compiled["diagnostics"]["source_map_packets"]
    }
    return seal(
        {
            "schema": SCHEMA_ID,
            "compiler_id": COMPILER_ID,
            "artifact_kind": ARTIFACT_KIND,
            "architecture_id": ARCHITECTURE_ID,
            "partition_sha256": PARTITION_SHA256,
            "row_contract": {
                "field_base_prime": P,
                "field_extension_degree": 6,
                "field_cardinality": str(Q),
                "domain_size": N,
                "code_dimension": K,
                "agreement": AGREEMENT,
                "B_star": B_STAR,
                "unit": UNIT,
                "quantifier": QUANTIFIER,
                "field_encoding_id": FIELD_ENCODING_ID,
                "slope_encoding": SLOPE_ENCODING,
            },
            "active_partition": {
                "atom_order": list(ATOM_ORDER),
                "owner_order": list(OWNER_ORDER),
                "paid_owner_count": 7,
                "residual_rule": "ITERATED_EXACT_SET_DIFFERENCE",
                "witness_exhaustive": True,
                "compiler_operates_on_declared_candidates_only": True,
                "semantic_owner_membership_validated": False,
                "target_received_line_coordinates_compared": True,
                "target_slope_coordinates_compared": True,
                "target_graph_record_id_compared": True,
            },
            "producer_contract": {
                "provenance_key": [
                    "received_line_id",
                    "source_id",
                    "selector_id",
                    "context_digest",
                ],
                "charged_key": ["received_line_id", "slope_coordinates"],
                "diagnostic_residue_direction_key": [
                    "received_line_id",
                    "projective_residue_direction_key",
                ],
                "collective_packet_class_key": [
                    "residue_line_id_or_null",
                    "source_map_packet_id_or_null",
                    "declared_rational_source_map_class_id",
                ],
                "charged_slopes_are_never_collapsed_by_shared_residue_direction": True,
                "multiple_witnesses_for_one_slope_are_deduplicated": True,
                "one_canonical_graph_record_per_slope_required": True,
                "projective_residue_scaling_is_deduplicated": True,
                "rational_source_map_class_is_not_inferred_from_residue_direction": True,
                "map_packet_threshold_is_derived_collectively": True,
                "excluded_upstream_components_are_not_charged_records": True,
                "accepted_record_mode": ABSTRACT_RECORD_MODE,
                "accepted_complete_reciprocal_rank_regime": RANK_THREE_REGIME,
                "semantic_evidence_validation_present": False,
                "deployed_complete_selector_producer_present": False,
                "accepted_record_keys": sorted(RECORD_KEYS),
                "accepted_context_keys": sorted(CONTEXT_KEYS),
                "required_but_unvalidated_deployed_context_fields": [
                    "f",
                    "g",
                    "V",
                    "H_V",
                    "K0",
                    "d_V",
                    "y0",
                    "y1",
                    "c0",
                    "c1",
                    "epsilon0",
                    "epsilon1",
                    "Sigma",
                    "H1",
                    "H2",
                    "K0_basis_r1_through_r8",
                    "u",
                    "v",
                    "transverse_two_column_condition",
                    "affine_difference_rank_9",
                    "column_rank_10",
                    "K0_equals_D_intersection_KV",
                    "dimension_K0_equals_8",
                ],
                "required_but_unvalidated_per_slope_fields": [
                    "eta",
                    "S_eta",
                    "c_eta",
                    "e_eta",
                    "E_eta",
                    "delta_eta",
                    "z_eta_1_through_z_eta_8",
                    "O_eta",
                    "ell_O_eta",
                    "Delta_eta_nonzero",
                    "(H1+eta*H2)ell_O_eta=0",
                    "H2_ell_O_eta_nonzero",
                ],
                "required_but_unvalidated_rich_graph_line_fields": [
                    "alpha",
                    "beta",
                    "a_L",
                    "b_L",
                    "Z_L",
                    "M_L",
                    "x_L",
                    "beta_L",
                    "P_L",
                    "Q_L",
                    "pointwise_source_lift_equations",
                    "codeword_pencil_zero",
                    "G_L_or_zero_case",
                    "divisibility_degree_plant_inequalities",
                ],
            },
            "exact_scope": {
                "proved_scan_interval": [SCAN_R_MIN, SCAN_R_MAX],
                "open_slack_interval": [OPEN_R_MIN, OPEN_R_MAX],
                "open_slack_count": OPEN_R_COUNT,
                "later_slack_interval": [OPEN_R_MIN + 1, OPEN_R_MAX],
                "later_slack_count": LATER_SLACK_COUNT,
                "equality_wall": {
                    "r": EQUALITY_R,
                    "s": EQUALITY_S,
                    "e": EQUALITY_E,
                    "c": EQUALITY_C,
                    "carrier_size": CARRIER_SIZE,
                    "locator_degree": LOCATOR_DEGREE,
                    "rank_at_most_two_cap": RANK_LE_TWO_CAP,
                    "required_locator_incidence_cap": REQUIRED_LOCATOR_INCIDENCE_CAP,
                    "sufficient_source_map_class_cap": SOURCE_MAP_CLASS_CAP,
                    "cap68_reserve_margin": SOURCE_MAP_CLASS_CAP_MARGIN,
                    "generic_kernel_free_cap": GENERIC_KERNEL_FREE_CAP,
                },
                "packet_threshold_scope": {
                    "counted_object": (
                        "DECLARED_RATIONAL_SOURCE_MAP_CLASS_IDS_WITHIN_ONE_"
                        "DECLARED_EXHAUSTIVE_RESIDUE_LINE_PACKET"
                    ),
                    "projective_residue_direction_is_not_the_source_map_class": True,
                    "semantic_packet_membership_validated": False,
                    "at_most_68_terminal_globally_bankable": False,
                    "at_least_69_terminal_unpaid": True,
                },
                "imported_noncharged_scope_branches": sorted(
                    IMPORTED_NONCHARGED_SCOPE_BRANCHES
                ),
                "geometry_inventory": geometry_inventory(),
            },
            "terminal_registry": terminal_registry(),
            "regression_fixture": {
                "classification": "ABSTRACT_RANK_THREE_ISOLATED_REGRESSION_ONLY",
                "deployed_field_instantiated": False,
                "received_word_constructed": False,
                "complete_selector_producer_constructed": False,
                "semantic_branch_membership_validated": False,
                "semantic_owner_membership_validated": False,
                "producer_sha256": digest_bytes(canonical_json(fixture)),
                "compiled_sha256": digest_bytes(canonical_json(compiled)),
                "diagnostics": compiled["diagnostics"],
                "controls": {
                    "first_match": {
                        "slope_coordinates": by_slope[tuple(fixture_slope(0))][
                            "slope_coordinates"
                        ],
                        "declared_owner_candidates": by_slope[
                            tuple(fixture_slope(0))
                        ]["declared_owner_candidates"],
                        "selected_declared_owner": by_slope[
                            tuple(fixture_slope(0))
                        ]["selected_declared_owner"],
                    },
                    "scaled_duplicate_witnesses": {
                        "slope_coordinates": by_slope[tuple(fixture_slope(1))][
                            "slope_coordinates"
                        ],
                        "witness_count": by_slope[tuple(fixture_slope(1))][
                            "witness_count"
                        ],
                        "projective_residue_direction_key": by_slope[
                            tuple(fixture_slope(1))
                        ]["projective_residue_direction_key"],
                    },
                    "shared_residue_direction_distinct_slopes": {
                        "slope_coordinates": [
                            by_slope[tuple(fixture_slope(1))]["slope_coordinates"],
                            by_slope[tuple(fixture_slope(2))]["slope_coordinates"],
                        ],
                        "projective_residue_direction_key": by_slope[
                            tuple(fixture_slope(1))
                        ]["projective_residue_direction_key"],
                        "charged_slope_count": 2,
                    },
                    "small_collective_packet": packet_by_id[
                        "fixture-packet-small"
                    ],
                    "large_collective_packet": packet_by_id[
                        "fixture-packet-large"
                    ],
                    "terminal_histogram": compiled["diagnostics"]["terminal_histogram"],
                },
            },
            "closure_state": {
                "U_paid_before": U_PAID,
                "U_paid_after": U_PAID,
                "B_remaining_before": B_REMAINING,
                "B_remaining_after": B_REMAINING,
                "additional_charge": 0,
                "U_Q": None,
                "U_BC": None,
                "U_new": None,
                "row_closed": False,
                "global_spread_routing_closed": False,
                "complete_selector_source_family_coverage": False,
                "same_record_primitive_owner_emission": False,
                "cap68_uniformly_proved": False,
                "recursive_any_69_subset_deletion_proved": False,
                "first_open_slack_after_packet": OPEN_R_MIN,
                "terminal": (
                    "UNBOUND_DEPLOYED_SOURCE_EVIDENCE_COMPLETE_SELECTOR_AND_"
                    "RECURSIVE_ANY_69_SUBSET_SAME_RECORD_OWNER"
                ),
                "maximal_missing_theorem": (
                    "EVERY_RESIDUAL_RECEIVED_LINE_HAS_A_SEMANTICALLY_VALIDATED_COMPLETE_"
                    "SOURCE_SELECTOR; ON_EVERY_RANK_THREE_RESIDUE_LINE, EVERY_SURVIVING_"
                    "69_CLASS_SUBSET_EMITS_A_PRIOR_OWNER_FOR_AT_LEAST_ONE_CLASS_AT_THE_"
                    "SAME_GRAPH_RECORD, ITERABLY_UNTIL_AT_MOST_68_CLASSES_REMAIN, OR_A_"
                    "DIRECT_RESIDUAL_BOUND_PAYS; ALL_NON_MAP_EQUALITY_BRANCHES_AND_LATER_"
                    "SLACKS_ARE_SEPARATELY_CLOSED"
                ),
            },
            "route_cuts": {
                "conditional_target_N_30119370885234533_from_pr1091_bankable": False,
                "reason_pr1091": (
                    "It inherits conditional U_Q and a conditional halving allocation; "
                    "no canonical chart producer is present."
                ),
                "fixed_union_nu10_payment_additive_across_unbounded_unions": False,
                "reason_pr1106": (
                    "It pays one fixed union and is already duplicated in the integrated "
                    "low-excess carrier packet; no aggregation theorem is present."
                ),
                "local_q6_orbit_counts_are_global_slope_census": False,
                "equality_u2_r134943_chain_is_exhaustive_for_open_interval": False,
                "abstract_declared_owner_candidates_are_bankable_evidence": False,
                "projective_residue_direction_is_rational_source_map_class": False,
            },
            "source_bindings": source_bindings(),
            "upstream_bindings": upstream_bindings(),
            "audit": {
                "proof": (
                    "EXACT_ABSTRACT_FIRST_MATCH_DEDUPLICATION_FIXED_GF_P6_ENCODING_"
                    "AND_COLLECTIVE_PACKET_THRESHOLD_MECHANICS"
                ),
                "empirical_evidence": "ABSTRACT_REGRESSION_FIXTURE_ONLY",
                "conjecture": "NO_GLOBAL_PAYMENT_BANKED",
                "global_verdict": "YELLOW_ROW_OPEN",
                "layer_cake_dyadic_summability": "NOT_APPLICABLE",
                "moment_markov_chebyshev": "NOT_APPLICABLE",
            },
            "nonclaims": [
                "No deployed source-bound record validator, received word, or complete selector is constructed.",
                "No declared branch label, evidence id, completeness Boolean, or owner candidate is treated as mathematical evidence.",
                "No imported exclusion is represented as a charged slope or zero-charge slope record.",
                "No local orbit count is promoted to a global slope census.",
                "No projective residue direction is identified with a rational source-map class.",
                "No two slopes are identified merely because their residue directions agree.",
                "No owner is transferred between graph records, selectors, or received lines.",
                "No cap 68 theorem, packet exhaustiveness theorem, or recursive 69-subset deletion theorem is asserted.",
                "The rank-at-most-two packet cap is not mixed additively with rank-three records.",
                "No later slack r=134944 through 213050 is classified geometrically.",
                "No U_Q, U_BC, or U_new value is invented.",
                "No active ledger value, official endpoint, or row status moves.",
            ],
        }
    )


def validate_manifest(document: dict[str, Any]) -> None:
    schema = strict_load(SCHEMA_PATH, canonical=False)
    require(schema["$id"] == SCHEMA_ID, "schema id")
    require(schema["additionalProperties"] is False, "top-level-closed schema")
    require(set(document) == set(schema["required"]), "schema top-level keys")
    expected = expected_manifest()
    deep_exact(document, expected)
    require(document["payload_sha256"] == payload_digest(document), "payload seal")
    require(document["closure_state"]["additional_charge"] == 0, "zero movement")
    require(document["closure_state"]["row_closed"] is False, "row remains open")
    require(
        document["producer_contract"]["deployed_complete_selector_producer_present"] is False,
        "no producer invented",
    )
    diagnostics = document["regression_fixture"]["diagnostics"]
    require(diagnostics["raw_witness_records"] == 84, "fixture witness count")
    require(diagnostics["distinct_charged_slopes"] == 82, "fixture slope count")
    require(
        diagnostics["distinct_projective_residue_directions"] == 81,
        "fixture residue-direction count",
    )
    require(
        diagnostics["distinct_slopes_collapsed_by_residue_direction"] == 0,
        "no slope collapse",
    )
    controls = document["regression_fixture"]["controls"]
    require(
        controls["first_match"]["selected_declared_owner"] == OWNER_ORDER[0],
        "first-match owner",
    )
    require(controls["scaled_duplicate_witnesses"]["witness_count"] == 2, "duplicate witness dedup")
    require(
        controls["scaled_duplicate_witnesses"]["projective_residue_direction_key"]
        == controls["shared_residue_direction_distinct_slopes"][
            "projective_residue_direction_key"
        ],
        "shared residue-direction control",
    )
    require(
        len(
            {
                tuple(row)
                for row in controls["shared_residue_direction_distinct_slopes"][
                    "slope_coordinates"
                ]
            }
        )
        == 2,
        "distinct slopes retained",
    )
    require(
        controls["small_collective_packet"][
            "distinct_declared_rational_source_map_classes"
        ]
        == 3,
        "small packet has three declared source-map classes",
    )
    require(
        controls["small_collective_packet"]["derived_terminal"]
        == MAP_PACKET_AT_MOST_68,
        "small packet derives cap-68 conditional terminal",
    )
    require(
        controls["large_collective_packet"][
            "distinct_declared_rational_source_map_classes"
        ]
        == 69,
        "large packet has 69 declared source-map classes",
    )
    require(
        controls["large_collective_packet"]["derived_terminal"]
        == MAP_PACKET_AT_LEAST_69,
        "large packet derives unpaid 69-class terminal",
    )
    require(
        all(
            LOCAL_TERMINALS[branch] not in diagnostics["terminal_histogram"]
            for branch in IMPORTED_NONCHARGED_SCOPE_BRANCHES
        ),
        "imported exclusions are absent from charged fixture terminals",
    )
    fixture = fixture_producer()
    forward = compile_records(copy.deepcopy(fixture))
    fixture["records"].reverse()
    reverse = compile_records(fixture)
    require(forward == reverse, "compiler input-order invariance")


Mutation = tuple[str, Callable[[dict[str, Any]], None]]


def manifest_mutations() -> list[Mutation]:
    return [
        ("architecture", lambda d: d.__setitem__("architecture_id", "bad")),
        ("partition", lambda d: d.__setitem__("partition_sha256", "0" * 64)),
        ("owner-order", lambda d: d["active_partition"]["owner_order"].reverse()),
        ("atom-order", lambda d: d["active_partition"]["atom_order"].reverse()),
        ("owner-count", lambda d: d["active_partition"].__setitem__("paid_owner_count", 8)),
        ("same-record", lambda d: d["active_partition"].__setitem__("target_graph_record_id_compared", False)),
        ("semantic-owner", lambda d: d["active_partition"].__setitem__("semantic_owner_membership_validated", True)),
        ("charged-key", lambda d: d["producer_contract"].__setitem__("charged_key", ["projective_residue_direction_key"])),
        ("collapse", lambda d: d["producer_contract"].__setitem__("charged_slopes_are_never_collapsed_by_shared_residue_direction", False)),
        ("map-conflation", lambda d: d["producer_contract"].__setitem__("rational_source_map_class_is_not_inferred_from_residue_direction", False)),
        ("semantic-validator", lambda d: d["producer_contract"].__setitem__("semantic_evidence_validation_present", True)),
        ("producer", lambda d: d["producer_contract"].__setitem__("deployed_complete_selector_producer_present", True)),
        ("scan", lambda d: d["exact_scope"].__setitem__("proved_scan_interval", [0, SCAN_R_MAX])),
        ("interval", lambda d: d["exact_scope"].__setitem__("open_slack_interval", [134_943, 134_943])),
        ("later-count", lambda d: d["exact_scope"].__setitem__("later_slack_count", 0)),
        ("packet-bank", lambda d: d["exact_scope"]["packet_threshold_scope"].__setitem__("at_most_68_terminal_globally_bankable", True)),
        ("conic-partition", lambda d: d["exact_scope"]["geometry_inventory"]["q6_u2_conic"].__setitem__("surviving_orbits_after_p3c3", [46, 30, 10, 10, 309])),
        ("quartic-payment", lambda d: d["exact_scope"]["geometry_inventory"]["q6_u2_quartic"].__setitem__("repeated_or_ramified_branch", "PAID")),
        ("fixture-deployed", lambda d: d["regression_fixture"].__setitem__("deployed_field_instantiated", True)),
        ("fixture-semantic", lambda d: d["regression_fixture"].__setitem__("semantic_branch_membership_validated", True)),
        ("fixture-collapse", lambda d: d["regression_fixture"]["diagnostics"].__setitem__("distinct_slopes_collapsed_by_residue_direction", 1)),
        ("packet-69", lambda d: d["regression_fixture"]["controls"]["large_collective_packet"].__setitem__("distinct_declared_rational_source_map_classes", 68)),
        ("movement", lambda d: d["closure_state"].__setitem__("additional_charge", 1)),
        ("paid-after", lambda d: d["closure_state"].__setitem__("U_paid_after", U_PAID + 1)),
        ("uq", lambda d: d["closure_state"].__setitem__("U_Q", 0)),
        ("row-closed", lambda d: d["closure_state"].__setitem__("row_closed", True)),
        ("global-closed", lambda d: d["closure_state"].__setitem__("global_spread_routing_closed", True)),
        ("cap68", lambda d: d["closure_state"].__setitem__("cap68_uniformly_proved", True)),
        ("recursive-69", lambda d: d["closure_state"].__setitem__("recursive_any_69_subset_deletion_proved", True)),
        ("pr1091", lambda d: d["route_cuts"].__setitem__("conditional_target_N_30119370885234533_from_pr1091_bankable", True)),
        ("pr1106", lambda d: d["route_cuts"].__setitem__("fixed_union_nu10_payment_additive_across_unbounded_unions", True)),
        ("orbit-census", lambda d: d["route_cuts"].__setitem__("local_q6_orbit_counts_are_global_slope_census", True)),
        ("scope-exhaustive", lambda d: d["route_cuts"].__setitem__("equality_u2_r134943_chain_is_exhaustive_for_open_interval", True)),
        ("declared-bankable", lambda d: d["route_cuts"].__setitem__("abstract_declared_owner_candidates_are_bankable_evidence", True)),
        ("source-hash", lambda d: d["source_bindings"][0].__setitem__("sha256", "0" * 64)),
        ("upstream-hash", lambda d: d["upstream_bindings"][0].__setitem__("file_sha256", "0" * 64)),
        ("global-green", lambda d: d["audit"].__setitem__("global_verdict", "GREEN_CLOSED")),
        ("nonclaim", lambda d: d["nonclaims"].pop()),
    ]


def producer_mutations() -> list[Mutation]:
    return [
        ("selector-mix", lambda d: d["records"][0].__setitem__("selector_id", "other")),
        ("source-mix", lambda d: d["records"][0].__setitem__("source_id", "other")),
        ("line-mix", lambda d: d["records"][0].__setitem__("received_line_id", "other")),
        ("context-mix", lambda d: d["records"][0].__setitem__("context_digest", "other")),
        ("selector-not-complete", lambda d: d["context"].__setitem__("declared_complete_selector", False)),
        ("selector-not-exhaustive", lambda d: d["context"].__setitem__("declared_selector_universe_exhaustive", False)),
        ("H-mix", lambda d: d["context"].__setitem__("declared_same_H_V_for_all_records", False)),
        ("K0-mix", lambda d: d["context"].__setitem__("declared_same_K0_for_all_records", False)),
        ("domain-mix", lambda d: d["context"].__setitem__("declared_same_domain_for_all_records", False)),
        ("semantic-self-certification", lambda d: d["context"].__setitem__("semantic_evidence_validation_present", True)),
        ("deployed-mode", lambda d: d["context"].__setitem__("record_mode", "DEPLOYED_SOURCE_BOUND")),
        ("rank-regime-mix", lambda d: d["context"].__setitem__("complete_reciprocal_rank_regime", RANK_LE_TWO_REGIME)),
        ("field-prime", lambda d: d["context"].__setitem__("field_base_prime", 101)),
        ("field-degree", lambda d: d["context"].__setitem__("field_extension_degree", 1)),
        ("field-hash", lambda d: d["context"].__setitem__("basis_sha256", "bad")),
        ("source-context-field", lambda d: d["context"]["declared_source_context_bindings"].pop("Sigma")),
        ("witness-duplicate", lambda d: d["records"][1].__setitem__("witness_id", "w0a")),
        ("graph-record-mix", lambda d: d["records"][1].__setitem__("graph_record_id", "other")),
        ("slope-direction-mix", lambda d: d["records"][1].__setitem__("residue_direction_vector", [1, 0, 0])),
        ("slope-source-map-mix", lambda d: d["records"][1].__setitem__("declared_rational_source_map_class_id", "other")),
        ("branch-mix", lambda d: d["records"][1].__setitem__("local_branch", CONIC_P6)),
        ("zero-direction", lambda d: d["records"][2].__setitem__("residue_direction_vector", [0, 0, 0])),
        ("wrong-modulus", lambda d: d["records"][2].__setitem__("residue_direction_modulus", 101)),
        ("missing-bridge", lambda d: d["records"][2].__setitem__("declared_moving_root_bridge", False)),
        ("source-incompatible", lambda d: d["records"][2].__setitem__("declared_source_compatible", False)),
        ("empty-source-map", lambda d: d["records"][2].__setitem__("declared_rational_source_map_class_id", "")),
        ("negative-deficit", lambda d: d["records"][2].__setitem__("declared_deficit", -1)),
        ("owner-unknown", lambda d: d["records"][2]["declared_owner_candidates"][0].__setitem__("owner_id", "FAKE")),
        ("owner-record-transfer", lambda d: d["records"][2]["declared_owner_candidates"][0].__setitem__("graph_record_id", "g999")),
        ("owner-line-transfer", lambda d: d["records"][2]["declared_owner_candidates"][0].__setitem__("target_received_line_id", "other")),
        ("owner-slope-transfer", lambda d: d["records"][2]["declared_owner_candidates"][0].__setitem__("target_slope_coordinates", fixture_slope(999))),
        ("no-owner", lambda d: d["records"][2].__setitem__("declared_owner_candidates", [])),
        ("paid-local-branch", lambda d: d["records"][0].__setitem__("local_branch", CONIC_P6)),
        ("complement-active-only", lambda d: d["records"][2].__setitem__("local_branch", ACTIVE_ONLY)),
        ("later-at-equality", lambda d: d["records"][7].__setitem__("r", EQUALITY_R)),
        ("outside-scan", lambda d: d["records"][7].__setitem__("r", 0)),
        ("forbidden-excluded-record", lambda d: d["records"][8].__setitem__("local_branch", P3C3_EXCLUDED)),
        ("invented-branch-flag", lambda d: d["records"][8]["declared_branch_evidence_flags"].append("FAKE")),
        ("bool-slope-coordinate", lambda d: d["records"][2].__setitem__("slope_coordinates", [True, 0, 0, 0, 0, 0])),
        ("short-slope-coordinate", lambda d: d["records"][2].__setitem__("slope_coordinates", [1, 0, 0])),
        ("large-slope-coordinate", lambda d: d["records"][2].__setitem__("slope_coordinates", [P, 0, 0, 0, 0, 0])),
        ("bool-direction-entry", lambda d: d["records"][2].__setitem__("residue_direction_vector", [True, 2, 3])),
        ("duplicate-owner-claim", lambda d: d["records"][2]["declared_owner_candidates"].append(copy.deepcopy(d["records"][2]["declared_owner_candidates"][0]))),
        ("packet-not-exhaustive", lambda d: d["records"][12].__setitem__("source_map_packet_exhaustive", False)),
        ("packet-id-null", lambda d: d["records"][12].__setitem__("source_map_packet_id_or_null", None)),
        ("packet-split-same-line", lambda d: d["records"][13].__setitem__("source_map_packet_id_or_null", "other")),
        ("packet-paid-owner", lambda d: d["records"][12]["declared_owner_candidates"][0].__setitem__("owner_id", OWNER_ORDER[0])),
        ("nonpacket-packet-id", lambda d: d["records"][2].__setitem__("source_map_packet_id_or_null", "bad")),
        ("record-extra-key", lambda d: d["records"][2].__setitem__("extra", 1)),
    ]


def rehash(document: dict[str, Any]) -> None:
    document["payload_sha256"] = payload_digest(document)


def run_tamper_selftest() -> int:
    passed = 0
    baseline = expected_manifest()
    for name, mutate in manifest_mutations():
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        rehash(candidate)
        try:
            validate_manifest(candidate)
        except (VerificationError, KeyError, TypeError, ValueError):
            passed += 1
        else:
            raise VerificationError(f"manifest mutation escaped: {name}")
    fixture = fixture_producer()
    for name, mutate in producer_mutations():
        candidate = copy.deepcopy(fixture)
        mutate(candidate)
        try:
            compile_records(candidate)
        except (VerificationError, KeyError, TypeError, ValueError, StopIteration):
            passed += 1
        else:
            raise VerificationError(f"producer mutation escaped: {name}")
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--compile-records", type=Path)
    args = parser.parse_args()

    selected = sum(
        bool(value)
        for value in (
            args.check,
            args.print_template,
            args.tamper_selftest,
            args.compile_records is not None,
        )
    )
    require(selected == 1, "select exactly one action")

    if args.print_template:
        sys.stdout.buffer.write(canonical_json(expected_manifest()))
        return
    if args.compile_records is not None:
        producer = strict_load(args.compile_records)
        sys.stdout.buffer.write(canonical_json(compile_records(producer)))
        return

    document = strict_load(args.manifest)
    validate_manifest(document)
    if args.tamper_selftest:
        count = run_tamper_selftest()
        print(f"PASS: {count} mutations rejected")
    else:
        print("PASS: KoalaBear v4 abstract source-map packet compiler")
        print(f"checks={CHECKS}")
        print(f"partition_sha256={PARTITION_SHA256}")
        print(f"first_open_slack={OPEN_R_MIN}")
        print("ledger_movement=0")
        print(
            "terminal=UNBOUND_DEPLOYED_SOURCE_EVIDENCE_COMPLETE_SELECTOR_"
            "AND_RECURSIVE_ANY_69_SUBSET_SAME_RECORD_OWNER"
        )


if __name__ == "__main__":
    try:
        main()
    except (VerificationError, OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
