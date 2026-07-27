#!/usr/bin/env python3
"""Replay the KoalaBear first-gap base-rational source-pencil image owner."""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path
from typing import Any

import verify_kb_mca_v4_c5_twist_frobenius9208_adapter_v1 as prev

ROOT = Path(__file__).resolve().parents[2]
CERT = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-first-gap-source-pencil-image-owner-v1"
)
ROW_PATH = CERT / "row_manifest.json"
MANIFEST_PATH = CERT / "manifest.json"
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "kb_mca_v4_first_gap_source_pencil_image_owner_v1.schema.json"
)

ARCH = (
    "GRANDE_FINALE_V4_KB_MCA_TANGENT_DEEP_SOURCE_RATIONAL_"
    "C5_BASE_TWIST_FROBENIUS_9208_FIRST_GAP_PENCIL_IMAGE_ADAPTER_V1"
)
OWNER = "ACTIVE_V4_FIRST_GAP_BASE_RATIONAL_SOURCE_PENCIL_IMAGE"
SOURCE_DEGREE = 67_472
SOURCE_SIZE = 2 * SOURCE_DEGREE
DOMAIN_SIZE = 2_097_152
OFF_SOURCE_DOMAIN = DOMAIN_SIZE - SOURCE_SIZE
PROJECTIVE_POINT_CAP = prev.BASE_PRIME + 1
OWNER_CAP = PROJECTIVE_POINT_CAP * OFF_SOURCE_DOMAIN
PAID = prev.PAID + OWNER_CAP
REMAINING = prev.REMAINING - OWNER_CAP

OWNER_ORDER = [
    *prev.OWNER_ORDER[:6],
    OWNER,
    *prev.OWNER_ORDER[6:],
]
ATOM_ORDER = ["U_paid", "U_Q", "U_BC", "U_new"]

UPSTREAM_CERTIFICATES = {
    "source_interpolation_pencil": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-first-gap-source-interpolation-pencil-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '12ee94cc29fe136af4ae9c801fbb1c0ad8291d0be08cf4b51b0ce43c5c910afa'
        ),
    },
    "complement_locator_linearization": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-first-gap-complement-locator-linearization-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '2e324cf51a372b92741e6efeb114c8b8e458a2d20e47c8f5899d94470ea57963'
        ),
    },
    "projective_residue_c5_rank_dichotomy": {
        "path": (
            "experimental/data/certificates/"
            "kb-mca-v4-first-gap-projective-residue-c5-rank-dichotomy-v1/"
            "certificate.json"
        ),
        "payload_sha256": (
            '99bb10644bf532974e723e47c5875494598d5ed2ea5507c15d4111916272f92c'
        ),
    },
}

SOURCE_PATHS = prev.SOURCE_PATHS + [
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_interpolation_pencil_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_complement_locator_linearization_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_projective_residue_c5_rank_dichotomy_v1.md"
    ),
    (
        "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_pencil_image_owner_v1.md"
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


def upstream_bindings() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for key, contract in UPSTREAM_CERTIFICATES.items():
        path = ROOT / contract["path"]
        need(path.is_file(), f"missing upstream certificate: {key}")
        result[key] = {
            **contract,
            "file_sha256": file_digest(path),
        }
    return result


def partition_body() -> dict[str, Any]:
    atom_ids = ["U_paid"] * 7 + ["U_Q", "U_BC", "U_new"]
    stages = []
    incoming = "COMPLETE_BAD_FINITE_SLOPES"
    for index, owner in enumerate(OWNER_ORDER):
        outgoing = "EMPTY" if index == len(OWNER_ORDER) - 1 else f"R{index + 1}"
        stages.append(
            {
                "atom_id": atom_ids[index],
                "owner_id": owner,
                "paid": index < 7,
                "residual_input": incoming,
                "residual_output": outgoing,
            }
        )
        incoming = outgoing
    return {
        "atom_order": ATOM_ORDER,
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
                "method": "PAIR_GLOBAL_BASE_RATIONAL_SOURCE_PENCIL_IMAGE",
                "predecessor_architecture_id": prev.ARCH,
                "selector_data_imported": False,
                "weighted_determinant_packing_imported": False,
            },
            "partition": partition(),
            "row_contract": predecessor["row_contract"],
            "source_bindings": source_bindings(),
            "source_owners": {
                **predecessor["source_owners"],
                "first_gap_base_rational_source_pencil_image": {
                    "all_qualifying_first_gap_slopes_owned": True,
                    "base_projective_point_cap": PROJECTIVE_POINT_CAP,
                    "cap": OWNER_CAP,
                    "first_gap_slack": 67_471,
                    "map_image_cap_per_projective_point": OFF_SOURCE_DOMAIN,
                    "off_source_domain_size": OFF_SOURCE_DOMAIN,
                    "pair_global": True,
                    "selector_independent": True,
                    "source_degree": SOURCE_DEGREE,
                    "source_pencil_dimension": 2,
                    "source_size": SOURCE_SIZE,
                    "subset_stable": True,
                    "uses_map_injectivity": False,
                },
            },
            "upstream_certificates": upstream_bindings(),
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
                    "owner_ids": OWNER_ORDER[:7],
                    "value": PAID,
                },
                {
                    "atom_id": "U_Q",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[7]],
                    "value": None,
                },
                {
                    "atom_id": "U_BC",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[8]],
                    "value": None,
                },
                {
                    "atom_id": "U_new",
                    "bankable": False,
                    "owner_ids": [OWNER_ORDER[9]],
                    "value": None,
                },
            ],
            "closure_state": {
                "first_gap_full_outside_rank_two_paid": True,
                "known_sum": PAID,
                "remaining_budget_after_known_sum": REMAINING,
                "remaining_full_outside_slack_interval": [67_472, 209_568],
                "row_closed": False,
                "unpaid_owner_ids": OWNER_ORDER[7:],
            },
            "partition_sha256": row["partition"]["partition_sha256"],
            "row_manifest_binding": {
                "path": str(ROW_PATH.relative_to(ROOT)).replace("\\", "/"),
                "sha256": file_digest(ROW_PATH),
            },
            "source_bindings": source_bindings(),
            "upstream_certificates": upstream_bindings(),
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
        "title": "KoalaBear first-gap source-pencil image owner",
        "type": "object",
    }


def first_match(
    incoming: set[int], predicates: list[set[int]]
) -> tuple[set[int], ...]:
    residual = set(incoming)
    cells = []
    for predicate in predicates:
        cell = residual & predicate
        cells.append(cell)
        residual -= cell
    cells.append(residual)
    return tuple(cells)


def check_upstream_payloads(bindings: dict[str, dict[str, str]]) -> None:
    for key, binding in bindings.items():
        payload = load(ROOT / binding["path"])
        need(
            payload.get("payload_sha256") == binding["payload_sha256"],
            f"upstream payload mismatch: {key}",
        )


def check_arithmetic() -> None:
    need(SOURCE_SIZE == 134_944, "source size")
    need(OFF_SOURCE_DOMAIN == 1_962_208, "off-source domain")
    need(PROJECTIVE_POINT_CAP == 2_130_706_434, "projective point cap")
    need(OWNER_CAP == 4_180_889_210_446_272, "owner cap")
    need(PAID == 4_200_515_150_819_207, "paid subtotal")
    need(REMAINING == 270_780_212_960_575_880, "remaining reserve")
    need(OWNER_CAP < prev.REMAINING, "owner fits predecessor reserve")


def check_partition_regression() -> None:
    universe = set(range(53))
    predicates = [
        {0, 1, 2, 7},
        {2, 3, 4, 8},
        {1, 4, 5, 9, 13},
        {14, 15, 16, 17},
        {5, 10, 15, 18, 22, 31},
        {6, 10, 18, 19, 23, 32},
        {6, 20, 24, 33, 41},
        {11, 20, 24, 34, 42},
        {11, 12, 21, 25, 43},
    ]
    cells = first_match(universe, predicates)
    need(len(cells) == len(OWNER_ORDER), "ten-cell partition")
    expected_pencil = predicates[6] - set().union(*predicates[:6])
    need(cells[6] == expected_pencil, "first-gap residual intersection")
    need(set().union(*cells) == universe, "partition exhaustion")
    for index, left in enumerate(cells):
        for right in cells[index + 1 :]:
            need(left.isdisjoint(right), "partition disjointness")


def check_toy_image_union() -> None:
    # Four projective points and five domain points: each point contributes
    # at most one finite output per input, independently of injectivity.
    domain = range(5)
    images = []
    for a, b in [(1, 0), (0, 1), (1, 1), (1, 2)]:
        image = set()
        for x in domain:
            denominator = (b * x + 1) % 7
            if denominator:
                image.add((-(a * x + b) * pow(denominator, -1, 7)) % 7)
        need(len(image) <= len(domain), "per-map image cap")
        images.append(image)
    need(len(set().union(*images)) <= 4 * len(domain), "union image cap")


def check_sources() -> None:
    note = (
        ROOT
        / "experimental/notes/frontier-adjacent/"
        "kb_mca_v4_first_gap_source_pencil_image_owner_v1.md"
    ).read_text(encoding="utf-8")
    for anchor in [
        "PROVED PAIR-GLOBAL FIRST-GAP OWNER",
        "ACTIVE_V4_FIRST_GAP_BASE_RATIONAL_SOURCE_PENCIL_IMAGE",
        "4{,}180{,}889{,}210{,}446{,}272",
        "4{,}200{,}515{,}150{,}819{,}207",
        "270{,}780{,}212{,}960{,}575{,}880",
        "carrier is forced",
        "no first-gap full-outside coefficient-rank-two selected slope",
        "does not need",
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
    owner = row["source_owners"]["first_gap_base_rational_source_pencil_image"]
    need(owner["selector_independent"] is True, "selector independence")
    need(owner["subset_stable"] is True, "subset stability")
    need(owner["uses_map_injectivity"] is False, "no map injectivity")
    need(
        owner["all_qualifying_first_gap_slopes_owned"] is True,
        "first-gap coverage",
    )
    check_upstream_payloads(row["upstream_certificates"])
    check_arithmetic()
    check_partition_regression()
    check_toy_image_union()
    check_sources()


def emit() -> None:
    CERT.mkdir(parents=True, exist_ok=True)
    row = expected_row()
    dump(ROW_PATH, row)
    dump(MANIFEST_PATH, expected_manifest(row))
    dump(SCHEMA_PATH, expected_schema(row["partition"]["partition_sha256"]))


def tamper_selftest() -> None:
    emit()
    row = expected_row()
    manifest = expected_manifest(row)
    schema = expected_schema(row["partition"]["partition_sha256"])
    mutations = [
        lambda r, m: r["source_owners"][
            "first_gap_base_rational_source_pencil_image"
        ].__setitem__("selector_independent", False),
        lambda r, m: r["source_owners"][
            "first_gap_base_rational_source_pencil_image"
        ].__setitem__("cap", OWNER_CAP - 1),
        lambda r, m: r["source_owners"][
            "first_gap_base_rational_source_pencil_image"
        ].__setitem__("uses_map_injectivity", True),
        lambda r, m: r["upstream_certificates"][
            "projective_residue_c5_rank_dichotomy"
        ].__setitem__("payload_sha256", "0" * 64),
        lambda r, m: m["atoms"][0].__setitem__("value", PAID - 1),
        lambda r, m: m["closure_state"].__setitem__(
            "first_gap_full_outside_rank_two_paid", False
        ),
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
            print(f"base_projective_point_cap: {PROJECTIVE_POINT_CAP}")
            print(f"off_source_domain: {OFF_SOURCE_DOMAIN}")
            print(f"first_gap_owner_cap: {OWNER_CAP}")
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
