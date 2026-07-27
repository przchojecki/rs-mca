#!/usr/bin/env python3
"""Replay the active KoalaBear C5/base, twist, and Frobenius-9208 adapter."""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_tangent_deep_source_rational_c5_adapter_v1 as prev

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-c5-twist-frobenius9208-adapter-v1"
)
ROW_PATH = CERT / "row_manifest.json"
MANIFEST_PATH = CERT / "manifest.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_c5_twist_frobenius9208_adapter_v1.schema.json"
)

ARCH = (
    "GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_"
    "C5_BASE_TWIST_FROBENIUS_9208_ADAPTER_V1"
)
BASE_PRIME = prev.BASE_PRIME
TWIST_CHARGE = BASE_PRIME - 1
FROBENIUS_DEGREE = 9_208
FROBENIUS_ANCHORS = 2 * (FROBENIUS_DEGREE + 1)
FROBENIUS_CHARGE = (FROBENIUS_DEGREE + 1) * (BASE_PRIME + 1)
PAID = prev.PAID + TWIST_CHARGE + FROBENIUS_CHARGE
REMAINING = prev.prev.base.B_STAR - PAID

TWIST_OWNER = "ACTIVE_V4_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST"
FROBENIUS_OWNER = (
    "ACTIVE_V4_PAIR_GLOBAL_SOURCE_FROBENIUS_"
    "EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_9208"
)
OWNER_ORDER = [
    *prev.OWNER_ORDER[:4],
    TWIST_OWNER,
    FROBENIUS_OWNER,
    *prev.OWNER_ORDER[4:],
]
SOURCE_PATHS = prev.SOURCE_PATHS + [
    "experimental/notes/m1/m1_kb_rank9_one_slack_twist_subline_owner_v1.md",
    (
        "experimental/notes/m1/"
        "m1_kb_rank9_bounded_slack_effective_multiplier_frobenius_owner_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_c5_twist_frobenius9208_adapter_v1.md"
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
    atom_ids = ["U_paid"] * 6 + ["U_Q", "U_BC", "U_new"]
    stages = []
    incoming = "COMPLETE_BAD_FINITE_SLOPES"
    for index, owner in enumerate(OWNER_ORDER):
        outgoing = "EMPTY" if index == len(OWNER_ORDER) - 1 else f"R{index + 1}"
        stages.append(
            {
                "atom_id": atom_ids[index],
                "owner_id": owner,
                "paid": index < 6,
                "residual_input": incoming,
                "residual_output": outgoing,
            }
        )
        incoming = outgoing
    return {
        "atom_order": prev.ATOM_ORDER,
        "chronology_stages": stages,
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
                "endpoint_legacy_accounting_imported": False,
                "legacy_first_match_state_imported": False,
                "legacy_full_stack_imported": False,
                "method": "PAIR_GLOBAL_SOURCE_ONLY_TWIST_AND_FROBENIUS_9208",
                "predecessor_architecture_id": prev.ARCH,
                "selector_data_imported": False,
            },
            "partition": partition(),
            "row_contract": predecessor["row_contract"],
            "source_bindings": source_bindings(),
            "source_owners": {
                **predecessor["source_owners"],
                "source_subline_common_twist": {
                    "cap": TWIST_CHARGE,
                    "earlier_tangent_labels_removed": True,
                    "pair_global": True,
                    "projective_subline_size": BASE_PRIME + 1,
                    "selector_independent": True,
                    "subset_stable": True,
                    "witness_exhaustive_for_qualifying_records": True,
                },
                "source_frobenius_effective_multiplier_9208": {
                    "anchor_count": FROBENIUS_ANCHORS,
                    "cap": FROBENIUS_CHARGE,
                    "determinant_degree_cap": FROBENIUS_CHARGE,
                    "endpoint_margin": 2,
                    "legacy_one_cut_gate_imported": False,
                    "max_effective_multiplier_degree": FROBENIUS_DEGREE,
                    "pair_global": True,
                    "selector_independent": True,
                    "subset_stable": True,
                    "supersedes_moving_cofactor_owner": True,
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
                    "owner_ids": OWNER_ORDER[:6],
                    "value": PAID,
                },
                {
                    "atom_id": "U_Q",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[6]],
                    "value": None,
                },
                {
                    "atom_id": "U_BC",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[7]],
                    "value": None,
                },
                {
                    "atom_id": "U_new",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[8]],
                    "value": None,
                },
            ],
            "closure_state": {
                "conditional_q_replayed": False,
                "known_sum": PAID,
                "legacy_endpoint_gate_imported": False,
                "legacy_recorded_U_paid": prev.prev.base.LEGACY_TOTAL,
                "legacy_stack_imported": False,
                "remaining_budget_after_known_sum": REMAINING,
                "row_closed": False,
                "unpaid_owner_ids": OWNER_ORDER[6:],
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
        "title": "KoalaBear active C5/base, twist, Frobenius-9208 adapter",
        "type": "object",
    }


def first_match(incoming: set[int], predicates: list[set[int]]) -> tuple[set[int], ...]:
    residual = set(incoming)
    cells = []
    for predicate in predicates:
        cell = residual & predicate
        cells.append(cell)
        residual -= cell
    cells.append(residual)
    return tuple(cells)


def check_regressions() -> None:
    universe = set(range(41))
    tangent = {0, 1, 2, 7}
    deep = {2, 3, 4, 8}
    rational = {1, 4, 5, 9, 13}
    base = {14, 15, 16, 17}
    twist = {5, 10, 15, 18, 22, 31}
    frobenius = {6, 10, 18, 19, 23, 32}
    q = {6, 11, 20, 24}
    bc = {11, 12, 21, 25}
    cells = first_match(
        universe,
        [tangent, deep, rational, base, twist, frobenius, q, bc],
    )
    need(len(cells) == len(OWNER_ORDER), "nine-cell partition")
    need(cells[4] == twist - tangent - deep - rational - base, "twist residual")
    need(
        cells[5] == frobenius - tangent - deep - rational - base - twist,
        "Frobenius residual",
    )
    need(set().union(*cells) == universe, "partition exhaustion")
    for index, left in enumerate(cells):
        for right in cells[index + 1 :]:
            need(left.isdisjoint(right), "partition disjointness")

    # On the intrinsic-base branch C5 owns the entire incoming residual.
    incoming_c5 = universe - tangent - deep - rational
    enabled = first_match(
        universe,
        [tangent, deep, rational, incoming_c5, twist, frobenius, q, bc],
    )
    need(enabled[3] == incoming_c5, "C5 owns incoming residual")
    need(all(not cell for cell in enabled[4:]), "C5 null tail")


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_c5_twist_frobenius9208_adapter_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED DIRECT ACTIVE-V4 OWNER EXTENSION",
        "2{,}130{,}706{,}432",
        "19{,}621{,}675{,}550{,}706",
        "19{,}625{,}940{,}372{,}935",
        "ACTIVE_V4_PAIR_GLOBAL_SOURCE_SUBLINE_COMMON_LINEAR_GCD_TWIST",
        "ACTIVE_V4_PAIR_GLOBAL_SOURCE_FROBENIUS_EFFECTIVE_MULTIPLIER_DEGREE_AT_MOST_9208",
        "legacy one-cut gate",
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
    twist = row["source_owners"]["source_subline_common_twist"]
    frob = row["source_owners"]["source_frobenius_effective_multiplier_9208"]
    need(twist["selector_independent"] is True, "twist selector independence")
    need(twist["subset_stable"] is True, "twist subset stability")
    need(frob["selector_independent"] is True, "Frobenius selector independence")
    need(frob["subset_stable"] is True, "Frobenius subset stability")
    need(frob["legacy_one_cut_gate_imported"] is False, "no legacy endpoint gate")
    need(frob["supersedes_moving_cofactor_owner"] is True, "no double charge")
    need(FROBENIUS_ANCHORS == 18_418, "endpoint anchor count")
    need(FROBENIUS_CHARGE == 19_621_675_550_706, "endpoint cap")
    need(PAID == 19_625_940_372_935, "paid total")
    need(REMAINING == 274_961_102_171_022_152, "remaining budget")
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
        lambda r, m: r["source_owners"]["source_subline_common_twist"].__setitem__(
            "subset_stable", False
        ),
        lambda r, m: r["source_owners"][
            "source_frobenius_effective_multiplier_9208"
        ].__setitem__("max_effective_multiplier_degree", 9_209),
        lambda r, m: r["source_owners"][
            "source_frobenius_effective_multiplier_9208"
        ].__setitem__("legacy_one_cut_gate_imported", True),
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
            print(f"twist_cap: {TWIST_CHARGE}")
            print(f"frobenius_9208_cap: {FROBENIUS_CHARGE}")
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
