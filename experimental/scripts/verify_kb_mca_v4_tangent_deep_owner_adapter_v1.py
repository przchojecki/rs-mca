#!/usr/bin/env python3
"""Replay the KoalaBear v4 tangent-plus-deep owner adapter.

This verifier checks the exact first-match structure, source bindings, integer
ledger, finite set regressions, and fail-closed artifact hashes. The Lean
kernel and cited source theorems, not this script, carry the proof.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERT = ROOT / "experimental/data/certificates/kb-mca-v4-tangent-deep-owner-adapter-v1"
ROW_PATH = CERT / "row_manifest.json"
MANIFEST_PATH = CERT / "manifest.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/kb_mca_v4_tangent_deep_owner_adapter_v1.schema.json"
)

ARCH = "GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_OWNER_ADAPTER_V1"
P = 2_130_706_433
EXTENSION_DEGREE = 6
N = 2_097_152
K = 1_048_576
A = 1_116_048
REDUNDANCY = N - K
TANGENT_CHARGE = N - A
DEEP_RADIUS = REDUNDANCY // 3
DEEP_AGREEMENT = N - DEEP_RADIUS
DEEP_CHARGE = DEEP_RADIUS + 1
PAID = TANGENT_CHARGE + DEEP_CHARGE
B_STAR = 274_980_728_111_395_087
REMAINING = B_STAR - PAID
LEGACY_TOTAL = 422_354_730_332

OWNER_ORDER = [
    "SOURCE_COORDINATE_TANGENT_IMAGE",
    "ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER",
    "ACTIVE_V4_BOUNDARY_PREFIX_Q",
    "ACTIVE_V4_BALANCED_CORE",
    "UNPAID_V4_COMPLEMENT",
]
ATOM_ORDER = ["U_paid", "U_Q", "U_BC", "U_new"]

SOURCE_PATHS = [
    "experimental/rs_mca_thresholds.tex",
    "experimental/lean/rs_mca_thresholds/RsMcaThresholds/ExactSparsification.lean",
    "experimental/notes/frontier-adjacent/kb_mca_v4_tangent_source_adapter_v1.md",
    "experimental/notes/m1/m1_kb_branch2_rank_deep_owner_v1.md",
    "experimental/notes/m1/m1_kb_branch3_deep_ccl_tdd_v1.md",
    "experimental/notes/frontier-adjacent/kb_mca_v4_tangent_deep_owner_adapter_v1.md",
    "experimental/lean/kb_mca_v4_tangent_deep_owner_adapter/KbMcaV4TangentDeepOwnerAdapter.lean",
    "experimental/lean/kb_mca_v4_tangent_deep_owner_adapter/CORRESPONDENCE.md",
]


class Failure(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if not ok:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    body = copy.deepcopy(value)
    body["payload_sha256"] = digest(value)
    return body


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(
            json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)
            + "\n"
        )


def source_bindings() -> list[dict[str, str]]:
    result = []
    for path_text in SOURCE_PATHS:
        path = ROOT / path_text
        need(path.is_file(), f"missing source: {path_text}")
        result.append(
            {
                "binding_id": path.stem.upper().replace("-", "_"),
                "hash": file_digest(path),
                "hash_kind": "SHA256",
                "path": path_text,
            }
        )
    return result


def partition_body() -> dict[str, Any]:
    return {
        "atom_order": ATOM_ORDER,
        "chronology_stages": [
            {
                "atom_id": "U_paid",
                "owner_id": OWNER_ORDER[0],
                "paid": True,
                "residual_input": "COMPLETE_BAD_FINITE_SLOPES",
                "residual_output": "R1",
            },
            {
                "atom_id": "U_paid",
                "owner_id": OWNER_ORDER[1],
                "paid": True,
                "residual_input": "R1",
                "residual_output": "R2",
            },
            {
                "atom_id": "U_Q",
                "owner_id": OWNER_ORDER[2],
                "paid": False,
                "residual_input": "R2",
                "residual_output": "R3",
            },
            {
                "atom_id": "U_BC",
                "owner_id": OWNER_ORDER[3],
                "paid": False,
                "residual_input": "R3",
                "residual_output": "R4",
            },
            {
                "atom_id": "U_new",
                "owner_id": OWNER_ORDER[4],
                "paid": False,
                "residual_input": "R4",
                "residual_output": "EMPTY",
            },
        ],
        "owner_order": OWNER_ORDER,
        "residual_rule": "ITERATED_EXACT_SET_DIFFERENCE",
        "witness_exhaustive": True,
    }


def partition() -> dict[str, Any]:
    body = partition_body()
    return {
        **body,
        "partition_digest_method": "SHA256_CANONICAL_JSON_OF_PARTITION_BODY",
        "partition_sha256": digest(body),
    }


def expected_row() -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "bridge": {
                "active_reproof": True,
                "conditional_q_replayed": False,
                "legacy_first_match_state_imported": False,
                "legacy_full_stack_imported": False,
                "method": "TANGENT_FRONTLOADING_PLUS_INTRINSIC_DEEP_MCA_ENVELOPE",
                "paid_union_identity": "T_UNION_D_INDEPENDENT_OF_LOCAL_ORDER",
            },
            "partition": partition(),
            "row_contract": {
                "B_star": B_STAR,
                "agreement": A,
                "code": {"dimension": K, "redundancy": REDUNDANCY},
                "domain": {"cardinality": N},
                "field": {
                    "base_prime": P,
                    "cardinality": str(P**EXTENSION_DEGREE),
                    "extension_degree": EXTENSION_DEGREE,
                },
                "projection_and_unit": "DISTINCT_BAD_FINITE_SLOPES_PER_RECEIVED_LINE",
            },
            "source_bindings": source_bindings(),
            "source_owners": {
                "deep": {
                    "agreement": DEEP_AGREEMENT,
                    "charge": DEEP_CHARGE,
                    "gate": {
                        "lhs": 3 * DEEP_RADIUS,
                        "relation": "<=",
                        "rhs": REDUNDANCY,
                    },
                    "intrinsic_predicate": (
                        "EXISTS_EXACT_NONCONTAINED_WITNESS_WITH_"
                        "ACTUAL_ERROR_WEIGHT_AT_MOST_DEEP_RADIUS"
                    ),
                    "monotone_under_prior_deletions": True,
                    "radius": DEEP_RADIUS,
                },
                "tangent": {
                    "canonical_translation": "PUBLIC_FIRST_COMMON_SP3",
                    "charge": TANGENT_CHARGE,
                    "translation_preserves_complete_bad_slope_set": True,
                    "union_over_alternative_translations_forbidden": True,
                },
            },
        }
    )


def expected_manifest(row: dict[str, Any]) -> dict[str, Any]:
    part_digest = row["partition"]["partition_sha256"]
    return seal(
        {
            "architecture_id": ARCH,
            "atoms": [
                {
                    "atom_id": "U_paid",
                    "bankable": True,
                    "owner_ids": OWNER_ORDER[:2],
                    "value": PAID,
                },
                {
                    "atom_id": "U_Q",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[2]],
                    "value": None,
                },
                {
                    "atom_id": "U_BC",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[3]],
                    "value": None,
                },
                {
                    "atom_id": "U_new",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[4]],
                    "value": None,
                },
            ],
            "closure_state": {
                "conditional_q_replayed": False,
                "known_sum": PAID,
                "legacy_recorded_U_paid": LEGACY_TOTAL,
                "legacy_stack_imported": False,
                "remaining_budget_after_known_sum": REMAINING,
                "row_closed": False,
                "unpaid_owner_ids": OWNER_ORDER[2:],
            },
            "partition_sha256": part_digest,
            "row_manifest_binding": {
                "path": str(ROW_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_digest(ROW_PATH),
            },
            "source_bindings": source_bindings(),
        }
    )


def expected_schema(part_digest: str) -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "additionalProperties": True,
        "properties": {
            "architecture_id": {"const": ARCH},
            "partition_sha256": {"const": part_digest},
            "payload_sha256": {"pattern": "^[0-9a-f]{64}$", "type": "string"},
        },
        "required": ["architecture_id", "partition_sha256", "payload_sha256"],
        "title": "KoalaBear v4 tangent-plus-deep owner adapter manifest",
        "type": "object",
    }


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Failure(f"cannot read {path}: {exc}") from exc
    need(isinstance(value, dict), f"{path} must contain a JSON object")
    return value


def first_match(
    incoming: set[int],
    tangent: set[int],
    deep: set[int],
    q: set[int],
    bc: set[int],
) -> tuple[set[int], set[int], set[int], set[int], set[int]]:
    z_t = incoming & tangent
    r1 = incoming - z_t
    z_d = r1 & deep
    r2 = r1 - z_d
    z_q = r2 & q
    r3 = r2 - z_q
    z_bc = r3 & bc
    z_new = r3 - z_bc
    return z_t, z_d, z_q, z_bc, z_new


def check_regressions() -> None:
    universe = set(range(19))
    predicates = [
        ({0, 1, 2, 7}, {2, 3, 4, 8}, {4, 5, 9}, {5, 6, 10}),
        (set(), universe, {1, 3}, {2, 4}),
        (universe, universe, universe, universe),
    ]
    for tangent, deep, q, bc in predicates:
        cells = first_match(universe, tangent, deep, q, bc)
        need(set().union(*cells) == universe, "finite exhaustion")
        for i, left in enumerate(cells):
            for right in cells[i + 1 :]:
                need(left.isdisjoint(right), "finite pairwise disjointness")
        legacy_paid = (universe & deep) | ((universe - deep) & tangent)
        active_paid = cells[0] | cells[1]
        need(legacy_paid == active_paid, "frontloading regression")


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_owner_adapter_v1.md"
    ).read_text(encoding="utf-8")
    lean = (
        ROOT
        / "experimental/lean/kb_mca_v4_tangent_deep_owner_adapter/"
        "KbMcaV4TangentDeepOwnerAdapter.lean"
    ).read_text(encoding="utf-8")
    corr = (
        ROOT
        / "experimental/lean/kb_mca_v4_tangent_deep_owner_adapter/"
        "CORRESPONDENCE.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED DIRECT ACTIVE-V4 RE-PROOF",
        "U_{\\rm paid}=981{,}104+349{,}526=1{,}330{,}630",
        "ACTIVE_V4_INTRINSIC_DEEP_MCA_WEIGHT_OWNER",
        "274{,}980{,}728{,}110{,}064{,}457",
        "conditional Q packet",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")
    need(lean.startswith("import Std\r\n") or lean.startswith("import Std\n"),
         "Lean module must import Std only")
    for token in ["sorry", "axiom ", "admit", "import Mathlib"]:
        need(token not in lean, f"forbidden Lean token: {token}")
    for declaration in [
        "activeOwner_cases_of_bad",
        "firstOwner_unique",
        "frontload_tangent_paid_union",
        "activeDeep_characterization",
        "deployedConstantsExact",
    ]:
        need(f"theorem {declaration}" in lean, f"missing Lean theorem: {declaration}")
    need("Expected `#print axioms` output" in corr, "correspondence axiom boundary")


def validate(row: dict[str, Any], manifest: dict[str, Any], schema: dict[str, Any]) -> None:
    expected_r = expected_row()
    need(row == expected_r, "row manifest differs from exact replay")
    expected_m = expected_manifest(row)
    need(manifest == expected_m, "manifest differs from exact replay")
    expected_s = expected_schema(row["partition"]["partition_sha256"])
    need(schema == expected_s, "schema differs from exact replay")
    need(3 * DEEP_RADIUS <= REDUNDANCY, "deep gate")
    need(DEEP_AGREEMENT == 1_747_627, "deep agreement")
    need(DEEP_CHARGE == 349_526, "deep charge")
    need(67_472 + 282_054 == DEEP_CHARGE, "legacy decomposition provenance")
    need(PAID == 1_330_630, "paid total")
    need(REMAINING == 274_980_728_110_064_457, "remaining budget")
    need(int(row["row_contract"]["field"]["cardinality"]) == P**6, "field order")
    need((P**6) // 2**128 == B_STAR, "budget floor")
    check_regressions()
    check_sources()


def emit() -> None:
    row = expected_row()
    dump(ROW_PATH, row)
    manifest = expected_manifest(row)
    dump(MANIFEST_PATH, manifest)
    dump(SCHEMA_PATH, expected_schema(row["partition"]["partition_sha256"]))


def tamper_selftest() -> None:
    row = expected_row()
    dump(ROW_PATH, row)
    manifest = expected_manifest(row)
    schema = expected_schema(row["partition"]["partition_sha256"])
    mutations = [
        ("paid total", lambda r, m: m["atoms"][0].__setitem__("value", PAID + 1)),
        (
            "owner order",
            lambda r, m: r["partition"]["owner_order"].reverse(),
        ),
        (
            "deep gate",
            lambda r, m: r["source_owners"]["deep"]["gate"].__setitem__("lhs", REDUNDANCY + 1),
        ),
        (
            "legacy import",
            lambda r, m: m["closure_state"].__setitem__("legacy_stack_imported", True),
        ),
        ("Q null", lambda r, m: m["atoms"][1].__setitem__("value", 1)),
    ]
    passed = 0
    for label, mutate in mutations:
        bad_row = copy.deepcopy(row)
        bad_manifest = copy.deepcopy(manifest)
        mutate(bad_row, bad_manifest)
        try:
            validate(bad_row, bad_manifest, schema)
        except Failure:
            passed += 1
        else:
            raise Failure(f"tamper accepted: {label}")
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
            row = load(ROW_PATH)
            manifest = load(MANIFEST_PATH)
            schema = load(SCHEMA_PATH)
            validate(row, manifest, schema)
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {row['partition']['partition_sha256']}")
            print(f"row_payload_sha256: {row['payload_sha256']}")
            print(f"manifest_payload_sha256: {manifest['payload_sha256']}")
            print(f"paid: {PAID}")
            print(f"remaining: {REMAINING}")
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
