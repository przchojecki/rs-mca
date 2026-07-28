#!/usr/bin/env python3
"""Independent replay of the KoalaBear abstract source-map packet compiler."""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-source-map-class-compiler-v1/manifest.json"
)
SCHEMA = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_source_map_class_compiler_v1.schema.json"
)
ROW = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-source-pencil-image-owner-v1/row_manifest.json"
)
ACTIVE = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-source-pencil-image-owner-v1/manifest.json"
)

SCHEMA_ID = "rs-mca-kb-v4-source-map-class-compiler-v1"
ARCHITECTURE = (
    "GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_"
    "TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1"
)
PARTITION = "7a57fa877417920862ed2fe2e5c569852555f78b73b046d320d5e7a65d98ebaa"
ROW_FILE_SHA = "0bb30bcd9e0d5349f6afa98e4c01eee288390eecf682d887ba51df981651e403"
ROW_PAYLOAD = "0f94535da1e28deb7e2ed3577e9b0a196f147c9fde8502fda9a935f9b5b4e921"
ACTIVE_FILE_SHA = "741681ff61a41a5c43f88fe7362839bb361b60be8ad19b1d3c59f292a8bf79e6"
ACTIVE_PAYLOAD = "0ba2155dea1a337b17fe23d7da303b5fa3b13d4958777b977a9e768842072bf5"
UNIT = "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE"
P = 2_130_706_433
SCAN = (9_209, 913_631)
OPEN = (134_943, 213_050)
EQUALITY_R = 134_943
CAP = 68

OWNER_ORDER = [
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
]
OWNER_TO_ATOM = {
    **{owner: "U_paid" for owner in OWNER_ORDER[:7]},
    OWNER_ORDER[7]: "U_Q",
    OWNER_ORDER[8]: "U_BC",
    OWNER_ORDER[9]: "U_new",
}

ACTIVE_ONLY = "ACTIVE_PARTITION_ONLY"
CONIC_P6 = "EQUALITY_Q6_U2_CONIC_P6"
CONIC_P2C4 = "EQUALITY_Q6_U2_CONIC_P2_PLUS_C4"
QUARTIC_SIMPLE = "EQUALITY_Q6_U2_QUARTIC_SIMPLE_VERTEX"
QUARTIC_DEGENERATE = "EQUALITY_Q6_U2_QUARTIC_REPEATED_OR_RAMIFIED"
NON_U2 = "EQUALITY_NON_U2_OR_U3_COMPONENT"
GENERAL_EXCESS = "EQUALITY_GENERAL_EXCESS_DELTA_AT_LEAST_E"
MAP_PACKET = "EQUALITY_RANK3_SOURCE_MAP_CLASS_PACKET"
LATER_SLACK = "LATER_SLACK_134944_TO_213050"
CHARGED_BRANCHES = {
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
LOCAL_TERMINALS = {
    CONIC_P6: "UNPAID_PRIMITIVE_Q6_U2_CONIC_P6",
    CONIC_P2C4: "UNPAID_PRIMITIVE_Q6_U2_CONIC_P2_PLUS_C4",
    QUARTIC_SIMPLE: "UNPAID_PRIMITIVE_Q6_U2_QUARTIC_SIMPLE_VERTEX",
    QUARTIC_DEGENERATE: "UNPAID_PRIMITIVE_Q6_U2_QUARTIC_REPEATED_OR_RAMIFIED",
    NON_U2: "UNPAID_PRIMITIVE_EQUALITY_NON_U2_OR_U3_COMPONENT",
    GENERAL_EXCESS: "UNPAID_PRIMITIVE_EQUALITY_GENERAL_EXCESS",
    LATER_SLACK: "UNPAID_PRIMITIVE_LATER_SLACK_134944_TO_213050",
}
PACKET_SMALL = "DECLARED_CONDITIONAL_SOURCE_MAP_PACKET_AT_MOST_68_NOT_GLOBALLY_BANKABLE"
PACKET_LARGE = "UNPAID_PRIMITIVE_SOURCE_MAP_PACKET_AT_LEAST_69"


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        need(key not in result, f"duplicate key: {key}")
        result[key] = value
    return result


def reject_float(_value: str) -> Any:
    raise RuntimeError("float forbidden")


def reject_constant(_value: str) -> Any:
    raise RuntimeError("nonfinite value forbidden")


def canonical(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load(path: Path, *, canonical_required: bool = True) -> dict[str, Any]:
    raw = path.read_bytes()
    need(len(raw) <= 64 * 1024 * 1024, f"size: {path}")
    value = json.loads(
        raw.decode("ascii"),
        object_pairs_hook=unique_object,
        parse_float=reject_float,
        parse_constant=reject_constant,
    )
    need(type(value) is dict, f"object: {path}")
    if canonical_required:
        need(raw == canonical(value), f"canonical bytes: {path}")
    return value


def safe_path(text: str) -> Path:
    need(type(text) is str and text.isascii(), "ASCII path")
    pure = PurePosixPath(text)
    need(
        not pure.is_absolute() and "." not in pure.parts and ".." not in pure.parts,
        "safe path",
    )
    path = ROOT.joinpath(*pure.parts)
    need(path.is_file() and not path.is_symlink(), f"regular file: {text}")
    need(path.resolve().is_relative_to(ROOT.resolve()), f"contained path: {text}")
    return path


def payload_sha(document: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(document)
    unsigned.pop("payload_sha256", None)
    return sha(canonical(unsigned))


def slope_key(value: Any) -> tuple[int, ...]:
    need(type(value) is list and len(value) == 6, "six slope coordinates")
    need(
        all(type(x) is int and not isinstance(x, bool) and 0 <= x < P for x in value),
        "base-field slope coordinates",
    )
    return tuple(value)


def residue_key(vector: Any, modulus: Any) -> str:
    need(modulus == P, "fixed projective base field")
    need(type(vector) is list and len(vector) == 3, "residue vector")
    need(
        all(type(x) is int and not isinstance(x, bool) and 0 <= x < P for x in vector),
        "residue entries",
    )
    pivot = next((x for x in vector if x), None)
    need(pivot is not None, "nonzero residue vector")
    inverse = pow(pivot, P - 2, P)
    return ":".join(str((x * inverse) % P) for x in vector)


def fixture_slope(index: int) -> list[int]:
    return [index, 0, 0, 0, 0, 0]


def fixture_claim(
    owner: str,
    graph_record_id: str,
    case_id: str,
    slope_coordinates: list[int],
) -> dict[str, Any]:
    return {
        "owner_id": owner,
        "graph_record_id": graph_record_id,
        "declared_evidence_id": f"fixture-evidence::{graph_record_id}::{owner}",
        "target_received_line_id": f"fixture-line::{case_id}",
        "target_slope_coordinates": copy.deepcopy(slope_coordinates),
    }


def fixture_record(
    case_id: str,
    witness_id: str,
    graph_record_id: str,
    slope_coordinates: list[int],
    r: int,
    branch: str,
    vector: list[int],
    owners: list[str],
    *,
    residue_line_id: str | None = None,
    packet_id: str | None = None,
    source_map_class_id: str | None = None,
) -> dict[str, Any]:
    is_packet = branch == MAP_PACKET
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
        "declared_branch_evidence_flags": [],
        "declared_owner_candidates": [
            fixture_claim(owner, graph_record_id, case_id, slope_coordinates)
            for owner in owners
        ],
    }


def build_fixture() -> dict[str, Any]:
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
    context = {
        "architecture_id": ARCHITECTURE,
        "partition_sha256": PARTITION,
        "unit": UNIT,
        "quantifier": "ONE_ABSTRACT_RECORD_SET_IN_ONE_DECLARED_PROVENANCE_CONTEXT",
        "received_line_id": f"fixture-line::{case_id}",
        "source_id": f"fixture-source::{case_id}",
        "selector_id": f"fixture-selector::{case_id}",
        "context_digest": f"fixture-context::{case_id}",
        "record_mode": "ABSTRACT_REGRESSION_ONLY",
        "field_base_prime": P,
        "field_extension_degree": 6,
        "field_encoding_id": "OPAQUE_GF_P6_FIXED_POWER_BASIS_V1",
        "extension_modulus_sha256": "1" * 64,
        "basis_sha256": "2" * 64,
        "domain_generator_sha256": "3" * 64,
        "slope_encoding": "SIX_BASE_FIELD_COORDINATES_IN_FIXED_POWER_BASIS",
        "complete_reciprocal_rank_regime": "COMPLETE_RECIPROCAL_RANK_THREE_ONLY",
        "declared_source_context_bindings": {
            "f": f"fixture-f::{case_id}",
            "g": f"fixture-g::{case_id}",
            "V": f"fixture-V::{case_id}",
            "H_V": f"fixture-HV::{case_id}",
            "K0": f"fixture-K0::{case_id}",
            "d_V": 981_105,
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
    return {
        "schema": SCHEMA_ID + "-producer-records",
        "context": context,
        "records": records,
    }


def active_terminal(owner: str, branch: str) -> tuple[str | None, bool]:
    if owner in OWNER_ORDER[:7]:
        need(branch == ACTIVE_ONLY, "paid owner only on active branch")
        return f"DECLARED_ACTIVE_FIRST_MATCH_OWNER::{owner}", True
    if owner == OWNER_ORDER[7]:
        need(branch == ACTIVE_ONLY, "U_Q only on active branch")
        return "DECLARED_UNPAID_ACTIVE_OWNER::ACTIVE_V4_BOUNDARY_PREFIX_Q", False
    if owner == OWNER_ORDER[8]:
        need(branch == ACTIVE_ONLY, "U_BC only on active branch")
        return "DECLARED_UNPAID_ACTIVE_OWNER::ACTIVE_V4_BALANCED_CORE", False
    need(branch != ACTIVE_ONLY, "final complement has explicit local branch")
    if branch == MAP_PACKET:
        return None, False
    return LOCAL_TERMINALS[branch], False


def replay(producer: dict[str, Any]) -> dict[str, Any]:
    context = producer["context"]
    need(context["record_mode"] == "ABSTRACT_REGRESSION_ONLY", "abstract mode")
    need(context["field_base_prime"] == P, "base prime")
    need(context["field_extension_degree"] == 6, "extension degree")
    need(
        context["field_encoding_id"] == "OPAQUE_GF_P6_FIXED_POWER_BASIS_V1",
        "field encoding",
    )
    need(
        context["slope_encoding"]
        == "SIX_BASE_FIELD_COORDINATES_IN_FIXED_POWER_BASIS",
        "slope encoding",
    )
    need(
        context["complete_reciprocal_rank_regime"]
        == "COMPLETE_RECIPROCAL_RANK_THREE_ONLY",
        "rank-three isolation",
    )
    need(context["semantic_evidence_validation_present"] is False, "semantic gap explicit")
    source_context = context["declared_source_context_bindings"]
    need(source_context["affine_difference_rank"] == 9, "declared affine rank")
    need(source_context["column_rank"] == 10, "declared column rank")
    need(source_context["dimension_K0"] == 8, "declared kernel dimension")
    need(
        type(source_context["K0_basis_r1_through_r8"]) is list
        and len(source_context["K0_basis_r1_through_r8"]) == 8,
        "declared kernel basis",
    )

    grouped: dict[tuple[int, ...], list[dict[str, Any]]] = defaultdict(list)
    witnesses: set[str] = set()
    for raw in producer["records"]:
        record = copy.deepcopy(raw)
        witness = record["witness_id"]
        need(witness not in witnesses, "unique witness")
        witnesses.add(witness)
        for key in ("received_line_id", "source_id", "selector_id", "context_digest"):
            need(record[key] == context[key], f"same context field: {key}")
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
            need(type(record[key]) is str and bool(record[key]), f"declared field: {key}")
        need(
            type(record["declared_deficit"]) is int
            and not isinstance(record["declared_deficit"], bool)
            and record["declared_deficit"] >= 0,
            "declared deficit",
        )
        branch = record["local_branch"]
        need(branch in CHARGED_BRANCHES, "charged branch only")
        need(SCAN[0] <= record["r"] <= SCAN[1], "proved scan universe")
        if branch == ACTIVE_ONLY:
            need(record["declared_branch_evidence_flags"] == [], "active flags empty")
        elif branch == LATER_SLACK:
            need(OPEN[0] < record["r"] <= OPEN[1], "later interval")
            need(record["declared_branch_evidence_flags"] == [], "later flags empty")
        else:
            need(record["r"] == EQUALITY_R, "equality r")
            need(record["declared_branch_evidence_flags"] == [], "open branch flags empty")
        slope = slope_key(record["slope_coordinates"])
        record["_slope"] = slope
        record["_direction"] = residue_key(
            record["residue_direction_vector"],
            record["residue_direction_modulus"],
        )
        need(
            type(record["declared_rational_source_map_class_id"]) is str
            and bool(record["declared_rational_source_map_class_id"]),
            "declared source-map class id",
        )
        is_packet = branch == MAP_PACKET
        need(
            is_packet
            == (
                type(record["residue_line_id_or_null"]) is str
                and bool(record["residue_line_id_or_null"])
            ),
            "residue-line packet metadata",
        )
        need(
            is_packet
            == (
                type(record["source_map_packet_id_or_null"]) is str
                and bool(record["source_map_packet_id_or_null"])
            ),
            "packet id metadata",
        )
        need(record["source_map_packet_exhaustive"] is is_packet, "packet exhaustiveness shape")
        owners = set()
        for claim in record["declared_owner_candidates"]:
            owner = claim["owner_id"]
            need(owner in OWNER_ORDER and owner not in owners, "declared owner set")
            owners.add(owner)
            need(claim["graph_record_id"] == record["graph_record_id"], "same graph target")
            need(claim["target_received_line_id"] == record["received_line_id"], "same line target")
            need(
                slope_key(claim["target_slope_coordinates"]) == slope,
                "same slope target",
            )
        need(bool(owners), "nonempty owner candidates")
        grouped[slope].append(record)

    classifications: list[dict[str, Any]] = []
    direction_to_slopes: dict[str, set[tuple[int, ...]]] = defaultdict(set)
    for slope in sorted(grouped):
        rows = grouped[slope]
        for field in (
            "r",
            "graph_record_id",
            "local_branch",
            "residue_line_id_or_null",
            "source_map_packet_id_or_null",
            "source_map_packet_exhaustive",
            "declared_rational_source_map_class_id",
            "_direction",
        ):
            need(len({json.dumps(row[field], sort_keys=True) for row in rows}) == 1, f"one {field}")
        candidates = {
            claim["owner_id"]
            for row in rows
            for claim in row["declared_owner_candidates"]
        }
        selected = next(owner for owner in OWNER_ORDER if owner in candidates)
        branch = rows[0]["local_branch"]
        terminal, paid = active_terminal(selected, branch)
        direction = rows[0]["_direction"]
        direction_to_slopes[direction].add(slope)
        classifications.append(
            {
                "slope_coordinates": list(slope),
                "r": rows[0]["r"],
                "graph_record_id": rows[0]["graph_record_id"],
                "witness_count": len(rows),
                "projective_residue_direction_key": direction,
                "declared_rational_source_map_class_id": rows[0][
                    "declared_rational_source_map_class_id"
                ],
                "declared_owner_candidates": [
                    owner for owner in OWNER_ORDER if owner in candidates
                ],
                "selected_declared_owner": selected,
                "atom_id": OWNER_TO_ATOM[selected],
                "would_route_to_paid_active_owner_if_semantically_certified": paid,
                "local_branch": branch,
                "residue_line_id_or_null": rows[0]["residue_line_id_or_null"],
                "source_map_packet_id_or_null": rows[0]["source_map_packet_id_or_null"],
                "source_map_packet_exhaustive": rows[0][
                    "source_map_packet_exhaustive"
                ],
                "terminal": terminal,
            }
        )

    packet_ids_by_line: dict[str, set[str]] = defaultdict(set)
    packets: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in classifications:
        if row["local_branch"] == MAP_PACKET:
            packet_ids_by_line[row["residue_line_id_or_null"]].add(
                row["source_map_packet_id_or_null"]
            )
            packets[
                (
                    row["residue_line_id_or_null"],
                    row["source_map_packet_id_or_null"],
                )
            ].append(row)
    need(
        all(len(packet_ids) == 1 for packet_ids in packet_ids_by_line.values()),
        "one exhaustive packet per residue line",
    )
    packet_summaries = []
    for (line_id, packet_id), rows in sorted(packets.items()):
        class_count = len(
            {row["declared_rational_source_map_class_id"] for row in rows}
        )
        terminal = PACKET_SMALL if class_count <= CAP else PACKET_LARGE
        for row in rows:
            need(row["terminal"] is None, "collective packet terminal")
            row["terminal"] = terminal
        packet_summaries.append(
            {
                "residue_line_id": line_id,
                "source_map_packet_id": packet_id,
                "declared_exhaustive": True,
                "distinct_charged_slopes": len(rows),
                "distinct_declared_rational_source_map_classes": class_count,
                "derived_terminal": terminal,
            }
        )
    need(all(row["terminal"] is not None for row in classifications), "explicit terminals")

    direction_multiplicities = sorted(
        len(slopes) for slopes in direction_to_slopes.values()
    )
    diagnostics = {
        "raw_witness_records": len(producer["records"]),
        "distinct_charged_slopes": len(classifications),
        "duplicate_witness_records_removed": len(producer["records"])
        - len(classifications),
        "distinct_projective_residue_directions": len(direction_to_slopes),
        "projective_residue_direction_multiplicities": direction_multiplicities,
        "slopes_in_shared_projective_residue_directions": sum(
            size for size in direction_multiplicities if size > 1
        ),
        "distinct_slopes_collapsed_by_residue_direction": 0,
        "owner_histogram": dict(
            sorted(Counter(row["selected_declared_owner"] for row in classifications).items())
        ),
        "terminal_histogram": dict(
            sorted(Counter(row["terminal"] for row in classifications).items())
        ),
        "source_map_packets": packet_summaries,
        "selection_sha256": sha(canonical(classifications)),
    }
    return {"classifications": classifications, "diagnostics": diagnostics}


def main() -> None:
    manifest = load(MANIFEST)
    schema = load(SCHEMA, canonical_required=False)
    need(schema["$id"] == SCHEMA_ID, "schema id")
    need(schema["additionalProperties"] is False, "top-level closed schema")
    need(set(manifest) == set(schema["required"]), "exact manifest keys")
    need(manifest["payload_sha256"] == payload_sha(manifest), "payload seal")
    need(manifest["schema"] == SCHEMA_ID, "manifest schema")
    need(manifest["architecture_id"] == ARCHITECTURE, "architecture")
    need(manifest["partition_sha256"] == PARTITION, "partition")

    need(sha(ROW.read_bytes()) == ROW_FILE_SHA, "row file pin")
    need(sha(ACTIVE.read_bytes()) == ACTIVE_FILE_SHA, "active file pin")
    row = load(ROW, canonical_required=False)
    active = load(ACTIVE, canonical_required=False)
    need(row["payload_sha256"] == ROW_PAYLOAD, "row payload pin")
    need(active["payload_sha256"] == ACTIVE_PAYLOAD, "active payload pin")
    partition = row["partition"]
    body = {
        key: partition[key]
        for key in (
            "atom_order",
            "chronology_stages",
            "owner_order",
            "residual_rule",
            "witness_exhaustive",
        )
    }
    need(sha(canonical(body)[:-1]) == PARTITION, "partition recomputation")
    need(partition["owner_order"] == OWNER_ORDER, "owner chronology")

    for binding in manifest["source_bindings"]:
        need(
            sha(safe_path(binding["path"]).read_bytes()) == binding["sha256"],
            "source binding",
        )
    for binding in manifest["upstream_bindings"]:
        path = safe_path(binding["path"])
        need(sha(path.read_bytes()) == binding["file_sha256"], "upstream binding")
        document = load(path, canonical_required=False)
        need(
            document.get("payload_sha256") == binding["payload_sha256_or_null"],
            "upstream payload",
        )

    fixture = manifest["regression_fixture"]
    producer = build_fixture()
    need(sha(canonical(producer)) == fixture["producer_sha256"], "producer digest")
    replayed = replay(producer)
    need(sha(canonical(replayed)) == fixture["compiled_sha256"], "compiled digest")
    need(replayed["diagnostics"] == fixture["diagnostics"], "independent diagnostics")
    packets = {
        row["source_map_packet_id"]: row
        for row in replayed["diagnostics"]["source_map_packets"]
    }
    need(
        packets["fixture-packet-small"][
            "distinct_declared_rational_source_map_classes"
        ]
        == 3,
        "small packet",
    )
    need(packets["fixture-packet-small"]["derived_terminal"] == PACKET_SMALL, "small terminal")
    need(
        packets["fixture-packet-large"][
            "distinct_declared_rational_source_map_classes"
        ]
        == 69,
        "large packet",
    )
    need(packets["fixture-packet-large"]["derived_terminal"] == PACKET_LARGE, "large terminal")

    need(
        residue_key([1, 2, 3], P) == residue_key([2, 4, 6], P),
        "projective scaling",
    )
    need(
        residue_key([1, 2, 3], P) != residue_key([1, 2, 4], P),
        "distinct residue directions",
    )
    reserve = 270_780_212_960_575_880
    carrier = 1_894_736
    cap68_charge = (67 * P + 68) * carrier
    cap69_charge = (68 * P + 69) * carrier
    need(cap68_charge == 270_487_454_459_300_144, "cap-68 charge")
    need(reserve - cap68_charge == 292_758_501_275_736, "cap-68 margin")
    need(cap69_charge == 274_524_580_645_231_568, "cap-69 charge")
    need(cap69_charge - reserve == 3_744_367_684_655_688, "cap-69 deficit")

    need(manifest["closure_state"]["additional_charge"] == 0, "zero movement")
    need(manifest["closure_state"]["row_closed"] is False, "row open")
    need(
        manifest["producer_contract"]["semantic_evidence_validation_present"]
        is False,
        "semantic validator absent",
    )
    need(
        manifest["closure_state"]["recursive_any_69_subset_deletion_proved"]
        is False,
        "recursive theorem open",
    )
    print("PASS: independent abstract source-map packet compiler replay")
    print("charged_slopes=82")
    print("residue_directions=81")
    print("packet_classes=3,69")
    print("ledger_movement=0")


if __name__ == "__main__":
    main()
