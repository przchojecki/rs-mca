#!/usr/bin/env python3
"""Replay the active KoalaBear tangent/deep/source-rational/C5 adapter."""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_tangent_deep_source_rational_adapter_v1 as prev

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-tangent-deep-source-rational-c5-adapter-v1"
)
ROW_PATH = CERT / "row_manifest.json"
MANIFEST_PATH = CERT / "manifest.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.schema.json"
)

ARCH = (
    "GRANDE_FINALE_V4_KB_MCA_"
    "TANGENT_DEEP_SOURCE_RATIONAL_C5_BASE_ADAPTER_V1"
)
BASE_PRIME = 2_130_706_433
C5_CHARGE = BASE_PRIME + 1
PAID = prev.PAID + C5_CHARGE
REMAINING = prev.base.B_STAR - PAID
OWNER_ORDER = [
    prev.OWNER_ORDER[0],
    prev.OWNER_ORDER[1],
    prev.OWNER_ORDER[2],
    "ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5_OR_RESIDUAL_BASE",
    prev.OWNER_ORDER[3],
    prev.OWNER_ORDER[4],
    prev.OWNER_ORDER[5],
]
ATOM_ORDER = prev.ATOM_ORDER
SOURCE_PATHS = prev.SOURCE_PATHS + [
    "experimental/notes/m1/m1_kb_projective_base_pair_c5_owner_v1.md",
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.md"
    ),
]

Failure = prev.Failure
need = prev.need
digest = prev.digest
seal = prev.seal
dump = prev.dump
load = prev.load
file_digest = prev.file_digest


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


def partition_body() -> dict[str, Any]:
    atom_ids = [
        "U_paid",
        "U_paid",
        "U_paid",
        "U_paid",
        "U_Q",
        "U_BC",
        "U_new",
    ]
    residuals = [
        ("COMPLETE_BAD_FINITE_SLOPES", "R1"),
        ("R1", "R2"),
        ("R2", "R3"),
        ("R3", "R4"),
        ("R4", "R5"),
        ("R5", "R6"),
        ("R6", "EMPTY"),
    ]
    return {
        "atom_order": ATOM_ORDER,
        "chronology_stages": [
            {
                "atom_id": atom_ids[i],
                "owner_id": owner,
                "paid": i < 4,
                "residual_input": residuals[i][0],
                "residual_output": residuals[i][1],
            }
            for i, owner in enumerate(OWNER_ORDER)
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
    predecessor = prev.expected_row()
    return seal(
        {
            "architecture_id": ARCH,
            "bridge": {
                "active_reproof": True,
                "conditional_q_replayed": False,
                "legacy_first_match_state_imported": False,
                "legacy_full_stack_imported": False,
                "method": "PAIR_GLOBAL_PROJECTIVE_BASE_C5_BASE_MAX_INSERTION",
                "predecessor_architecture_id": prev.ARCH,
                "selector_data_imported": False,
            },
            "partition": partition(),
            "row_contract": predecessor["row_contract"],
            "source_bindings": source_bindings(),
            "source_owners": {
                **predecessor["source_owners"],
                "projective_base_c5_or_residual_base": {
                    "cap": C5_CHARGE,
                    "c5_enabled_if": (
                        "POSITIVE_SYNDROME_RANK_AND_"
                        "INTRINSIC_PROJECTIVE_FIELD_EQUALS_BASE"
                    ),
                    "c5_owns_entire_incoming_residual_if_enabled": True,
                    "fallback_owner": "INCOMING_RESIDUAL_INTERSECT_BASE_SLOPES",
                    "joint_max_not_sum": True,
                    "pair_global": True,
                    "projective_line_size": C5_CHARGE,
                    "residual_base_cap": BASE_PRIME,
                    "subset_stable": True,
                    "witness_exhaustive": True,
                },
            },
        }
    )


def expected_manifest(row: dict[str, Any]) -> dict[str, Any]:
    return seal(
        {
            "architecture_id": ARCH,
            "atoms": [
                {
                    "atom_id": "U_paid",
                    "bankable": True,
                    "owner_ids": OWNER_ORDER[:4],
                    "value": PAID,
                },
                {
                    "atom_id": "U_Q",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[4]],
                    "value": None,
                },
                {
                    "atom_id": "U_BC",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[5]],
                    "value": None,
                },
                {
                    "atom_id": "U_new",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[6]],
                    "value": None,
                },
            ],
            "closure_state": {
                "conditional_q_replayed": False,
                "known_sum": PAID,
                "legacy_recorded_U_paid": prev.base.LEGACY_TOTAL,
                "legacy_stack_imported": False,
                "remaining_budget_after_known_sum": REMAINING,
                "row_closed": False,
                "unpaid_owner_ids": OWNER_ORDER[4:],
            },
            "partition_sha256": row["partition"]["partition_sha256"],
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
        "title": "KoalaBear v4 tangent-deep-source-rational-C5/base adapter manifest",
        "type": "object",
    }


def first_match(
    incoming: set[int],
    predicates: list[set[int]],
) -> tuple[set[int], ...]:
    residual = set(incoming)
    cells = []
    for predicate in predicates:
        cell = residual & predicate
        cells.append(cell)
        residual -= cell
    cells.append(residual)
    return tuple(cells)


def check_regressions() -> None:
    universe = set(range(29))
    tangent = {0, 1, 2, 7}
    deep = {2, 3, 4, 8}
    source_rational = {1, 4, 5, 9, 13}
    residual_base = {14, 15, 16, 17}
    q = {5, 6, 10}
    bc = {6, 11, 12}

    disabled = first_match(
        universe,
        [tangent, deep, source_rational, residual_base, q, bc],
    )
    need(len(disabled) == 7, "seven non-C5 cells")
    need(
        disabled[3]
        == (universe - tangent - deep - source_rational) & residual_base,
        "C5-disabled residual-base cell",
    )
    need(set().union(*disabled) == universe, "disabled-C5 exhaustion")

    incoming_c5 = universe - tangent - deep - source_rational
    enabled = first_match(
        universe,
        [tangent, deep, source_rational, incoming_c5, q, bc],
    )
    need(enabled[3] == incoming_c5, "enabled C5 owns exact incoming residual")
    need(not enabled[4] and not enabled[5] and not enabled[6], "null tail")
    for cells in (disabled, enabled):
        for i, left in enumerate(cells):
            for right in cells[i + 1 :]:
                need(left.isdisjoint(right), "finite pairwise disjointness")


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED DIRECT ACTIVE-V4 OWNER EXTENSION",
        "2{,}130{,}706{,}434",
        "2{,}134{,}115{,}797",
        "ACTIVE_V4_PAIR_PROJECTIVE_BASE_C5",
        "joint maximum",
        "# PROVED",
    ]:
        need(anchor in note, f"missing note anchor: {anchor}")


def validate(
    row: dict[str, Any],
    manifest: dict[str, Any],
    schema: dict[str, Any],
) -> None:
    need(row == expected_row(), "row manifest differs from exact replay")
    need(manifest == expected_manifest(row), "manifest differs from exact replay")
    need(
        schema == expected_schema(row["partition"]["partition_sha256"]),
        "schema differs from exact replay",
    )
    c5 = row["source_owners"]["projective_base_c5_or_residual_base"]
    need(c5["pair_global"] is True, "pair-global C5/base")
    need(c5["subset_stable"] is True, "C5/base subset stability")
    need(c5["witness_exhaustive"] is True, "C5 witness exhaustion")
    need(
        c5["c5_owns_entire_incoming_residual_if_enabled"] is True,
        "C5 whole incoming residual",
    )
    need(c5["joint_max_not_sum"] is True, "C5/base maximum")
    need(c5["residual_base_cap"] == BASE_PRIME, "residual base cap")
    need(C5_CHARGE == 2_130_706_434, "C5 cap")
    need(PAID == 2_134_115_797, "paid total")
    need(REMAINING == 274_980_725_977_279_290, "remaining budget")
    check_regressions()
    check_sources()


def emit() -> None:
    row = expected_row()
    dump(ROW_PATH, row)
    dump(MANIFEST_PATH, expected_manifest(row))
    dump(SCHEMA_PATH, expected_schema(row["partition"]["partition_sha256"]))


def tamper_selftest() -> None:
    row = expected_row()
    dump(ROW_PATH, row)
    manifest = expected_manifest(row)
    schema = expected_schema(row["partition"]["partition_sha256"])
    mutations = [
        lambda r, m: r["source_owners"][
            "projective_base_c5_or_residual_base"
        ].__setitem__(
            "pair_global", False
        ),
        lambda r, m: r["source_owners"][
            "projective_base_c5_or_residual_base"
        ].__setitem__(
            "c5_owns_entire_incoming_residual_if_enabled", False
        ),
        lambda r, m: r["source_owners"][
            "projective_base_c5_or_residual_base"
        ].__setitem__(
            "cap", C5_CHARGE - 1
        ),
        lambda r, m: m["atoms"][0].__setitem__("value", PAID - 1),
        lambda r, m: r["partition"]["owner_order"].reverse(),
    ]
    passed = 0
    for mutate in mutations:
        bad_row = copy.deepcopy(row)
        bad_manifest = copy.deepcopy(manifest)
        mutate(bad_row, bad_manifest)
        try:
            validate(bad_row, bad_manifest, schema)
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
            row = load(ROW_PATH)
            manifest = load(MANIFEST_PATH)
            schema = load(SCHEMA_PATH)
            validate(row, manifest, schema)
            print(f"architecture: {ARCH}")
            print(f"partition_sha256: {row['partition']['partition_sha256']}")
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
