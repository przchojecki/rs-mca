#!/usr/bin/env python3
"""Verify the KoalaBear inner-degree-12 diagonal-socle close.

This exact replay checks immutable parent custody, the complete terminal
degree-12 group ledger, Scott-strip arithmetic, the exceptional paired M12
actions, the secondary block system, challenge-field fifth-power arithmetic,
scope guards, and a fail-closed certificate payload.  It does not search the
endpoint-record space or claim a ledger payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
from collections import deque
from pathlib import Path
from typing import Any, Callable, Iterable


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-m12-diagonal-socle-degree5-close-v1"
    / "kb_mca_v4_m12_diagonal_socle_degree5_close_v1.json"
)

P = 2_130_706_433
FIELD_DEGREE = 6
EXPECTED_SCHEMA = "kb-mca-v4-m12-diagonal-socle-degree5-close-v1"
EXPECTED_STATUS = "PROVED_M12_DECOMPOSITION_ROW_EMPTY_OTHER_K3_ROWS_OPEN"
EXPECTED_ROUTE_COMMIT = "e368e5c8fc101ae0040b47265c2cd167e70dadd2"
EXPECTED_ROUTE_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-m12-outer-subdegree-route-cut-v1/"
    "kb_mca_v4_m12_outer_subdegree_route_cut_v1.json"
)
EXPECTED_ROUTE_BLOB = "6ea55700f303869a850c79c66c331842e0eed385"
EXPECTED_ROUTE_PAYLOAD = (
    "4349f6ca07b991fe78b90c66feb1fdcb1df582ac19d34c50d354c3c91c9e6b63"
)
EXPECTED_DEGREE5_COMMIT = "a14a05d9ba80068133e93e2fa77d6d1dc8828829"
EXPECTED_DEGREE5_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-degree60-decomposition-source-fiber-adapter-v1/"
    "kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.json"
)
EXPECTED_DEGREE5_BLOB = "911bac3c1c5d1b4cd9822c59939d60e832b7ef23"
EXPECTED_DEGREE5_PAYLOAD = (
    "638190df24415e5609fa9c2f50dde8fd22bd150f60e7bef5cd1496cb22d75b4e"
)
EXPECTED_NORMAL_COMMIT = "f7a42415bdb24c7e626b76394558bad100c5a874"
EXPECTED_NORMAL_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-m12-outer-normal-form-compiler-v1/"
    "kb_mca_v4_m12_outer_normal_form_compiler_v1.json"
)
EXPECTED_NORMAL_BLOB = "8e0ecd7f5b008900ada67dbf80848e8dbbff8416"
EXPECTED_NORMAL_PAYLOAD = (
    "7eb4f4053f90cb4ca0d0f3379fa3f8f33522ae0ec9b3dc67f5c7e602150d22f0"
)

CATALOGUE = [
    {"group": "M11", "order": 7_920, "simple_socle": "M11", "subdegrees": [1, 11]},
    {"group": "M12", "order": 95_040, "simple_socle": "M12", "subdegrees": [1, 11]},
    {
        "group": "PSL(2,11)",
        "order": 660,
        "simple_socle": "PSL(2,11)",
        "subdegrees": [1, 11],
    },
    {
        "group": "PGL(2,11)",
        "order": 1_320,
        "simple_socle": "PSL(2,11)",
        "subdegrees": [1, 11],
    },
    {
        "group": "A12",
        "order": 239_500_800,
        "simple_socle": "A12",
        "subdegrees": [1, 11],
    },
    {
        "group": "S12",
        "order": 479_001_600,
        "simple_socle": "A12",
        "subdegrees": [1, 11],
    },
]

EXPECTED_NONCLAIMS = [
    "No surviving type outside inner degree twelve is deleted or paid.",
    "No endpoint-record census is claimed.",
    (
        "No parameter-to-carrier, received-data, explaining-polynomial, "
        "or slope bridge is proved."
    ),
    "No u=2, K3, or KoalaBear row closure is claimed.",
    "No ledger quantity moves.",
]


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json_text(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicate_pairs)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} must contain a JSON object")
    return value


def load_json(path: Path) -> dict[str, Any]:
    try:
        return parse_json_text(path.read_text(), str(path))
    except OSError as error:
        raise VerificationError(f"cannot read certificate: {path}") from error


def git_output(*arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(
            f"git {' '.join(arguments)} failed: {error.stderr.strip()}"
        ) from error
    return completed.stdout.strip()


def exact_keys(value: Any, keys: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} must be an object")
    actual = set(value)
    require(
        actual == keys,
        f"{label} keys mismatch: missing={sorted(keys - actual)}, "
        f"extra={sorted(actual - keys)}",
    )


def exact_schema(data: dict[str, Any]) -> None:
    exact_keys(
        data,
        {
            "schema",
            "payload_sha256",
            "statement",
            "parent_route_cut",
            "degree_twelve_primitive_catalogue",
            "block_kernel_socle",
            "scott_strip_dichotomy",
            "m12_cross_action_audit",
            "outer_subdegree_conclusion",
            "diagonal_normalizer_columns",
            "degree_five_import",
            "external_source_custody",
            "source_bindings",
            "conclusion",
            "nonclaims",
        },
        "certificate",
    )
    exact_keys(
        data["statement"],
        {
            "workboard_item",
            "row",
            "object",
            "agreement",
            "B_star",
            "deployed_characteristic",
            "challenge_field_degree",
            "endpoint_degree",
            "component_u",
            "original_inner_degree",
            "original_outer_degree",
            "status",
            "ledger_movement",
        },
        "statement",
    )
    exact_keys(
        data["parent_route_cut"],
        {
            "commit",
            "certificate_path",
            "certificate_blob_oid",
            "certificate_payload_sha256",
            "imported_terminal",
            "imported_rows",
            "imported_global_transverse_type_count",
        },
        "parent_route_cut",
    )
    require(
        isinstance(data["degree_twelve_primitive_catalogue"], list),
        "catalogue must be a list",
    )
    for index, row in enumerate(data["degree_twelve_primitive_catalogue"]):
        exact_keys(
            row,
            {"group", "order", "simple_socle", "subdegrees"},
            f"catalogue[{index}]",
        )
    exact_keys(
        data["block_kernel_socle"],
        {
            "original_block_count",
            "original_block_size",
            "outer_point_stabilizer_order_upper_bound",
            "minimum_terminal_inner_group_order",
            "kernel_projection_nontrivial",
            "kernel_projection_contains_simple_socle",
            "derived_kernel",
            "derived_projection",
            "subdirect_product",
        },
        "block_kernel_socle",
    )
    exact_keys(
        data["scott_strip_dichotomy"],
        {
            "source",
            "strip_support_partition_G_invariant",
            "outer_block_action_degree",
            "outer_block_action_primitive",
            "invariant_support_partitions",
            "independent_case",
            "diagonal_case",
            "actual_suborbit_size",
            "actual_suborbit_meets_other_block",
            "independent_other_block_orbit_size",
            "independent_case_survives",
            "terminal",
        },
        "scott_strip_dichotomy",
    )
    exact_keys(
        data["m12_cross_action_audit"],
        {
            "degree",
            "action_12a_generator_a_cycles",
            "action_12a_generator_b_cycles",
            "action_12b_generator_a_cycles",
            "action_12b_generator_b_cycles",
            "paired_group_order",
            "action_12a_point_stabilizer_order",
            "same_action_orbit_lengths",
            "cross_action_orbit_lengths",
            "opposite_action_has_short_orbit",
        },
        "m12_cross_action_audit",
    )
    exact_keys(
        data["outer_subdegree_conclusion"],
        {
            "diagonal_point_stabilizer_orbits_in_equivalent_action",
            "actual_suborbit_size",
            "points_contributed_per_met_block",
            "projected_block_count",
            "surviving_outer_subdegree",
            "surviving_delta",
            "deleted_row",
            "all_five_degree_twelve_actions_equivalent",
            "terminal",
        },
        "outer_subdegree_conclusion",
    )
    exact_keys(
        data["diagonal_normalizer_columns"],
        {
            "common_socle_action_degree",
            "common_socle_action_faithful",
            "common_socle_action_two_transitive",
            "centralizer_in_Sym12_order",
            "normalizer_restrictions_implement_one_automorphism",
            "normalizer_restrictions_equal_across_original_blocks",
            "action_form",
            "secondary_block_count",
            "secondary_block_size",
            "secondary_blocks",
            "monodromy_intermediate_field_correspondence",
            "luroth_theorem",
            "secondary_inner_degree",
            "secondary_outer_degree",
            "terminal",
        },
        "diagonal_normalizer_columns",
    )
    exact_keys(
        data["degree_five_import"],
        {
            "commit",
            "certificate_path",
            "certificate_blob_oid",
            "certificate_payload_sha256",
            "quantifier",
            "imported_inner_degree",
            "imported_terminal",
            "p_mod_5",
            "q_mod_5",
            "gcd_5_q_minus_1",
            "fifth_power_map_on_K_is_bijective",
        },
        "degree_five_import",
    )
    exact_keys(
        data["external_source_custody"],
        {
            "gap_primgrp_commit",
            "gap_degree12_entry_sha256",
            "scott_doi",
            "scott_lemma_page",
            "atlas_m12_four_generator_files_sha256",
        },
        "external_source_custody",
    )
    require(isinstance(data["source_bindings"], list), "bindings must be a list")
    for index, binding in enumerate(data["source_bindings"]):
        exact_keys(
            binding,
            {"binding_id", "commit", "path", "blob_oid", "role"},
            f"source_bindings[{index}]",
        )
    exact_keys(
        data["conclusion"],
        {
            "deleted_by_this_packet",
            "remaining_degree_twelve_type_count",
            "remaining_global_transverse_type_count",
            "remaining_inner_degrees",
            "normal_form_families_without_actual_producer",
            "terminal",
            "m12_closed",
            "u2_closed",
            "K3_closed",
            "row_closed",
        },
        "conclusion",
    )


def verify_statement_and_parents(data: dict[str, Any]) -> None:
    require(data["schema"] == EXPECTED_SCHEMA, "schema mismatch")
    statement = data["statement"]
    expected_statement = {
        "workboard_item": "K3",
        "row": "KoalaBear MCA at 2^-128",
        "object": "MCA",
        "agreement": 1_116_048,
        "B_star": "274980728111395087",
        "deployed_characteristic": P,
        "challenge_field_degree": FIELD_DEGREE,
        "endpoint_degree": 60,
        "component_u": 2,
        "original_inner_degree": 12,
        "original_outer_degree": 5,
        "status": EXPECTED_STATUS,
        "ledger_movement": 0,
    }
    require(statement == expected_statement, "statement changed")

    parent = data["parent_route_cut"]
    require(parent["commit"] == EXPECTED_ROUTE_COMMIT, "route commit")
    require(parent["certificate_path"] == EXPECTED_ROUTE_PATH, "route path")
    require(parent["certificate_blob_oid"] == EXPECTED_ROUTE_BLOB, "route blob")
    require(
        parent["certificate_payload_sha256"] == EXPECTED_ROUTE_PAYLOAD,
        "route payload",
    )
    require(
        parent["imported_terminal"] == "M12_TRANSVERSE_TYPES_R2_R4_UNPAID",
        "route terminal",
    )
    require(
        parent["imported_rows"] == [{"r": 2, "delta": 24}, {"r": 4, "delta": 12}],
        "route rows",
    )
    require(parent["imported_global_transverse_type_count"] == 24, "route count")


def set_partitions(items: tuple[int, ...]) -> Iterable[tuple[frozenset[int], ...]]:
    if not items:
        yield ()
        return
    first, *rest = items
    for partition in set_partitions(tuple(rest)):
        yield (frozenset({first}),) + partition
        for index in range(len(partition)):
            blocks = list(partition)
            blocks[index] = blocks[index] | {first}
            yield tuple(sorted(blocks, key=lambda block: min(block)))


def canonical_partition(
    partition: Iterable[Iterable[int]],
) -> tuple[tuple[int, ...], ...]:
    return tuple(sorted(tuple(sorted(block)) for block in partition))


def verify_catalogue_and_scott(data: dict[str, Any]) -> None:
    catalogue = data["degree_twelve_primitive_catalogue"]
    require(catalogue == CATALOGUE, "degree-twelve catalogue changed")
    require(len(catalogue) == 6, "terminal group count")
    require(min(row["order"] for row in catalogue) == 660, "minimum group order")
    require(
        {row["simple_socle"] for row in catalogue}
        == {"M11", "M12", "PSL(2,11)", "A12"},
        "simple socle set",
    )
    require(all(row["subdegrees"] == [1, 11] for row in catalogue), "subdegrees")

    kernel = data["block_kernel_socle"]
    expected_kernel = {
        "original_block_count": 5,
        "original_block_size": 12,
        "outer_point_stabilizer_order_upper_bound": 24,
        "minimum_terminal_inner_group_order": 660,
        "kernel_projection_nontrivial": True,
        "kernel_projection_contains_simple_socle": True,
        "derived_kernel": "D=[N,N]",
        "derived_projection": "projection_i(D)=S_i",
        "subdirect_product": "D<=S_0 x S_1 x S_2 x S_3 x S_4",
    }
    require(kernel == expected_kernel, "block-kernel ledger changed")
    require(24 < 660, "kernel nontriviality inequality")

    rotation = {index: (index + 1) % 5 for index in range(5)}
    invariant = set()
    for partition in set_partitions(tuple(range(5))):
        key = canonical_partition(partition)
        image = canonical_partition(
            tuple(frozenset(rotation[item] for item in block) for block in partition)
        )
        if image == key:
            invariant.add(key)
    require(
        invariant
        == {
            ((0,), (1,), (2,), (3,), (4,)),
            ((0, 1, 2, 3, 4),),
        },
        "five-cycle invariant partitions",
    )

    scott = data["scott_strip_dichotomy"]
    require(
        scott["source"] == "Scott lemma, Proc. Symp. Pure Math. 37 (1980), p.328",
        "Scott source",
    )
    require(scott["strip_support_partition_G_invariant"] is True, "strip invariance")
    require(scott["outer_block_action_degree"] == 5, "outer block degree")
    require(scott["outer_block_action_primitive"] is True, "outer primitivity")
    require(
        scott["invariant_support_partitions"]
        == ["five_singletons", "one_five_point_part"],
        "support partition labels",
    )
    require(
        scott["independent_case"] == "D=S_0 x S_1 x S_2 x S_3 x S_4",
        "independent case",
    )
    require(
        scott["diagonal_case"] == "D is one full twisted diagonal strip",
        "diagonal case",
    )
    require(scott["actual_suborbit_size"] == 4, "actual suborbit size")
    require(scott["actual_suborbit_meets_other_block"] is True, "transversality")
    require(scott["independent_other_block_orbit_size"] == 12, "independent orbit")
    require(12 > 4, "independent product contradiction")
    require(scott["independent_case_survives"] is False, "independent survives")
    require(scott["terminal"] == "DERIVED_BLOCK_KERNEL_FULL_DIAGONAL", "Scott terminal")


def permutation(degree: int, cycles: list[list[int]]) -> bytes:
    result = list(range(degree))
    for cycle in cycles:
        require(len(cycle) >= 2, "generator has a singleton cycle")
        points = [point - 1 for point in cycle]
        require(all(0 <= point < degree for point in points), "cycle point range")
        require(len(points) == len(set(points)), "repeated point in cycle")
        for source, target in zip(points, points[1:] + points[:1]):
            require(result[source] == source, "overlapping cycles")
            result[source] = target
    require(sorted(result) == list(range(degree)), "not a permutation")
    return bytes(result)


def compose(left: bytes, right: bytes) -> bytes:
    return bytes(left[right[index]] for index in range(len(left)))


def enumerate_paired_m12(audit: dict[str, Any]) -> tuple[int, int, list[int], list[int]]:
    degree = audit["degree"]
    require(degree == 12, "M12 audit degree")
    a1 = permutation(degree, audit["action_12a_generator_a_cycles"])
    a2 = permutation(degree, audit["action_12a_generator_b_cycles"])
    b1 = permutation(degree, audit["action_12b_generator_a_cycles"])
    b2 = permutation(degree, audit["action_12b_generator_b_cycles"])
    generators = (a1 + b1, a2 + b2)
    identity = bytes(range(degree)) * 2
    group = {identity}
    queue = deque((identity,))
    while queue:
        element = queue.popleft()
        left, right = element[:degree], element[degree:]
        for generator in generators:
            candidate = (
                compose(generator[:degree], left)
                + compose(generator[degree:], right)
            )
            if candidate not in group:
                group.add(candidate)
                queue.append(candidate)
    stabilizer = tuple(element for element in group if element[0] == 0)
    same = sorted(
        {len({element[point] for element in stabilizer}) for point in range(degree)}
    )
    cross = sorted(
        {
            len({element[degree + point] for element in stabilizer})
            for point in range(degree)
        }
    )
    return len(group), len(stabilizer), same, cross


def verify_cross_action_and_outer_cut(
    data: dict[str, Any], *, run_group_audit: bool = True
) -> None:
    audit = data["m12_cross_action_audit"]
    require(
        audit["action_12a_generator_a_cycles"]
        == [[1, 4], [3, 10], [5, 11], [6, 12]],
        "M12 12a generator a",
    )
    require(
        audit["action_12a_generator_b_cycles"]
        == [[1, 8, 9], [2, 3, 4], [5, 12, 11], [6, 10, 7]],
        "M12 12a generator b",
    )
    require(
        audit["action_12b_generator_a_cycles"]
        == [[2, 3], [5, 6], [8, 9], [11, 12]],
        "M12 12b generator a",
    )
    require(
        audit["action_12b_generator_b_cycles"]
        == [[1, 2, 4], [3, 5, 7], [6, 8, 10], [9, 11, 12]],
        "M12 12b generator b",
    )
    expected = (95_040, 7_920, [1, 11], [12])
    require(
        (
            audit["paired_group_order"],
            audit["action_12a_point_stabilizer_order"],
            audit["same_action_orbit_lengths"],
            audit["cross_action_orbit_lengths"],
        )
        == expected,
        "M12 orbit ledger",
    )
    if run_group_audit:
        require(enumerate_paired_m12(audit) == expected, "paired M12 reconstruction")
    require(audit["opposite_action_has_short_orbit"] is False, "cross-action flag")

    outer = data["outer_subdegree_conclusion"]
    require(
        outer["diagonal_point_stabilizer_orbits_in_equivalent_action"] == [1, 11],
        "equivalent-action orbits",
    )
    require(outer["actual_suborbit_size"] == 4, "outer actual suborbit")
    require(outer["points_contributed_per_met_block"] == 1, "points per block")
    computed_projection = (
        outer["actual_suborbit_size"] // outer["points_contributed_per_met_block"]
    )
    require(computed_projection == outer["projected_block_count"] == 4, "projection")
    require(outer["surviving_outer_subdegree"] == 4, "surviving r")
    require(outer["surviving_delta"] == 12, "surviving delta")
    require(outer["surviving_outer_subdegree"] * outer["surviving_delta"] == 48, "r-delta")
    require(outer["deleted_row"] == {"r": 2, "delta": 24}, "deleted Dickson row")
    require(outer["all_five_degree_twelve_actions_equivalent"] is True, "actions")
    require(
        outer["terminal"] == "M12_R2_DICKSON_ROW_EMPTY_R4_FORCES_EQUIVALENT_ACTIONS",
        "outer terminal",
    )


def act(point: tuple[int, int], inner: tuple[int, ...], outer: tuple[int, ...]) -> tuple[int, int]:
    x, block = point
    return inner[x], outer[block]


def verify_secondary_decomposition(data: dict[str, Any]) -> None:
    columns = data["diagonal_normalizer_columns"]
    require(columns["common_socle_action_degree"] == 12, "common action degree")
    require(columns["common_socle_action_faithful"] is True, "faithful action")
    require(columns["common_socle_action_two_transitive"] is True, "2-transitive")
    require(columns["centralizer_in_Sym12_order"] == 1, "centralizer")
    require(
        columns["normalizer_restrictions_implement_one_automorphism"] is True,
        "one automorphism",
    )
    require(
        columns["normalizer_restrictions_equal_across_original_blocks"] is True,
        "equal restrictions",
    )
    require(columns["action_form"] == "g(x,i)=(n_g(x),pi_g(i))", "action form")

    inner = tuple((7 * x + 5) % 12 for x in range(12))
    require(len(set(inner)) == 12, "sample inner permutation")
    outer = (1, 2, 3, 4, 0)
    model_columns = [
        {(x, block) for block in range(5)}
        for x in range(12)
    ]
    images = [{act(point, inner, outer) for point in column} for column in model_columns]
    require(all(image in model_columns for image in images), "column preservation")
    require(len(model_columns) == columns["secondary_block_count"] == 12, "column count")
    require(
        {len(column) for column in model_columns}
        == {columns["secondary_block_size"]}
        == {5},
        "column size",
    )
    require(
        columns["secondary_blocks"] == "C_x={(x,0),(x,1),(x,2),(x,3),(x,4)}",
        "column description",
    )
    require(columns["monodromy_intermediate_field_correspondence"] is True, "block-field")
    require(columns["luroth_theorem"] is True, "Luroth gate")
    require(columns["secondary_inner_degree"] == 5, "secondary inner degree")
    require(columns["secondary_outer_degree"] == 12, "secondary outer degree")
    require(5 * 12 == 60, "secondary degree product")
    require(
        columns["terminal"] == "SECOND_GEOMETRIC_DECOMPOSITION_INNER_DEGREE_5",
        "secondary terminal",
    )

    imported = data["degree_five_import"]
    require(imported["commit"] == EXPECTED_DEGREE5_COMMIT, "degree5 commit")
    require(imported["certificate_path"] == EXPECTED_DEGREE5_PATH, "degree5 path")
    require(imported["certificate_blob_oid"] == EXPECTED_DEGREE5_BLOB, "degree5 blob")
    require(imported["certificate_payload_sha256"] == EXPECTED_DEGREE5_PAYLOAD, "degree5 payload")
    require(
        imported["quantifier"]
        == "every geometric decomposition of the residual degree-60 endpoint map",
        "degree5 quantifier",
    )
    require(imported["imported_inner_degree"] == 5, "imported degree")
    require(
        imported["imported_terminal"]
        == "DELETED_CHALLENGE_FIELD_FIFTH_POWER_FIBER_CONTRADICTION",
        "degree5 terminal",
    )
    q = P**FIELD_DEGREE
    require(imported["p_mod_5"] == P % 5 == 3, "p modulo five")
    require(imported["q_mod_5"] == q % 5 == 4, "q modulo five")
    require(imported["gcd_5_q_minus_1"] == math.gcd(5, q - 1) == 1, "fifth gcd")
    require(imported["fifth_power_map_on_K_is_bijective"] is True, "fifth bijectivity")


def verify_external_sources(data: dict[str, Any]) -> None:
    require(
        data["external_source_custody"]
        == {
            "gap_primgrp_commit": "5612e113d50ac23a7d10945383936e20440b4e14",
            "gap_degree12_entry_sha256": "9165e7e00ecebd79aaa1272ac83747529839a86191c859b56d49c01d88d12166",
            "scott_doi": "10.1090/pspum/037/604599",
            "scott_lemma_page": 328,
            "atlas_m12_four_generator_files_sha256": "55af41251add2886aedb2ebf04dfb522776768a245dd9e6cd8369094cf84aa38",
        },
        "external source custody changed",
    )


def verify_bindings(
    data: dict[str, Any], *, check_git_history: bool = True
) -> None:
    expected = [
        ("KB_M12_CLOSE::route_cut_certificate", EXPECTED_ROUTE_COMMIT, EXPECTED_ROUTE_PATH, EXPECTED_ROUTE_BLOB),
        (
            "KB_M12_CLOSE::route_cut_note",
            EXPECTED_ROUTE_COMMIT,
            "experimental/notes/frontier-adjacent/kb_mca_v4_m12_outer_subdegree_route_cut_v1.md",
            "7e1afd7dd2ea66688d8ec7446b8b7c46c2f1414b",
        ),
        ("KB_M12_CLOSE::degree5_certificate", EXPECTED_DEGREE5_COMMIT, EXPECTED_DEGREE5_PATH, EXPECTED_DEGREE5_BLOB),
        (
            "KB_M12_CLOSE::degree5_note",
            EXPECTED_DEGREE5_COMMIT,
            "experimental/notes/frontier-adjacent/kb_mca_v4_degree60_decomposition_source_fiber_adapter_v1.md",
            "e15b77679b7dbc0bb28cf5642a04bb4c71e61429",
        ),
        ("KB_M12_CLOSE::normal_form_certificate", EXPECTED_NORMAL_COMMIT, EXPECTED_NORMAL_PATH, EXPECTED_NORMAL_BLOB),
        (
            "KB_M12_CLOSE::normal_form_note",
            EXPECTED_NORMAL_COMMIT,
            "experimental/notes/frontier-adjacent/kb_mca_v4_m12_outer_normal_form_compiler_v1.md",
            "5a36de4a27d80d5a885aa0751db9fc37d9744aab",
        ),
    ]
    actual = [
        (binding["binding_id"], binding["commit"], binding["path"], binding["blob_oid"])
        for binding in data["source_bindings"]
    ]
    require(actual == expected, "source bindings changed")
    if not check_git_history:
        return
    for binding in data["source_bindings"]:
        git_output("cat-file", "-e", f"{binding['commit']}^{{commit}}")
        actual_blob = git_output("rev-parse", f"{binding['commit']}:{binding['path']}")
        require(actual_blob == binding["blob_oid"], f"blob mismatch: {binding['binding_id']}")

    route = parse_json_text(
        git_output("show", f"{EXPECTED_ROUTE_COMMIT}:{EXPECTED_ROUTE_PATH}"),
        "historical route certificate",
    )
    require(payload_hash(route) == route["payload_sha256"], "route self-hash")
    require(route["payload_sha256"] == EXPECTED_ROUTE_PAYLOAD, "route payload")
    require(route["surviving_degree_twelve_rows"] == data["parent_route_cut"]["imported_rows"], "route rows")
    require(route["conclusion"]["remaining_global_transverse_type_count"] == 24, "route count")
    require(route["conclusion"]["terminal"] == "M12_TRANSVERSE_TYPES_R2_R4_UNPAID", "route terminal")

    compiler_head = route["parent_stack"]["head_commit"]
    compiler_path = route["parent_stack"]["certificate_path"]
    compiler = parse_json_text(
        git_output("show", f"{compiler_head}:{compiler_path}"),
        "historical source-pencil compiler certificate",
    )
    require(payload_hash(compiler) == compiler["payload_sha256"], "compiler self-hash")
    degree_twelve = next(
        row for row in compiler["same_fiber_route_cut"]["small_degree_catalogue"]
        if row["degree"] == 12
    )
    require(degree_twelve["primitive_group_count"] == 6, "compiler degree12 count")
    require(degree_twelve["subdegree_rows"] == [[1, 11]] * 6, "compiler degree12 rows")

    degree5 = parse_json_text(
        git_output("show", f"{EXPECTED_DEGREE5_COMMIT}:{EXPECTED_DEGREE5_PATH}"),
        "historical degree5 certificate",
    )
    require(payload_hash(degree5) == degree5["payload_sha256"], "degree5 self-hash")
    require(degree5["payload_sha256"] == EXPECTED_DEGREE5_PAYLOAD, "degree5 payload")
    profile5 = next(row for row in degree5["profiles"] if row["inner_degree"] == 5)
    require(
        profile5["terminal"] == "DELETED_CHALLENGE_FIELD_FIFTH_POWER_FIBER_CONTRADICTION",
        "historical degree5 terminal",
    )
    require(
        degree5["statement"]["decomposition_scope"]
        == "every geometric decomposition f=F composed with h forced by the residual actual Q=6,s=6,u=2 component theorem",
        "historical degree5 quantifier",
    )

    normal = parse_json_text(
        git_output("show", f"{EXPECTED_NORMAL_COMMIT}:{EXPECTED_NORMAL_PATH}"),
        "historical normal-form certificate",
    )
    require(payload_hash(normal) == normal["payload_sha256"], "normal self-hash")
    require(normal["payload_sha256"] == EXPECTED_NORMAL_PAYLOAD, "normal payload")
    require(normal["conclusion"]["geometric_family_count"] == 6, "normal family count")
    require(normal["conclusion"]["terminal"] == "M12_SIX_GEOMETRIC_OUTER_FAMILIES_UNPAID", "normal terminal")


def verify_conclusion(data: dict[str, Any]) -> None:
    conclusion = data["conclusion"]
    require(
        conclusion["deleted_by_this_packet"]
        == [{"r": 2, "delta": 24}, {"r": 4, "delta": 12}],
        "deleted rows",
    )
    require(conclusion["remaining_degree_twelve_type_count"] == 0, "m12 count")
    require(conclusion["remaining_global_transverse_type_count"] == 22, "global count")
    require(24 - len(conclusion["deleted_by_this_packet"]) == 22, "frontier arithmetic")
    require(conclusion["remaining_inner_degrees"] == [2, 3, 4, 6, 10], "live degrees")
    require(conclusion["normal_form_families_without_actual_producer"] == 6, "family count")
    require(conclusion["terminal"] == "M12_DECOMPOSITION_ROW_EMPTY", "terminal")
    require(conclusion["m12_closed"] is True, "m12 close flag")
    for key in ("u2_closed", "K3_closed", "row_closed"):
        require(conclusion[key] is False, f"forbidden closure claim: {key}")
    require(data["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims changed")


def verify_certificate(
    data: dict[str, Any],
    *,
    check_git_bindings: bool = True,
    run_group_audit: bool = True,
) -> None:
    exact_schema(data)
    digest = data["payload_sha256"]
    require(
        isinstance(digest, str)
        and len(digest) == 64
        and all(character in "0123456789abcdef" for character in digest),
        "payload_sha256 is not a lowercase SHA-256 digest",
    )
    require(payload_hash(data) == digest, "payload hash mismatch")
    verify_statement_and_parents(data)
    verify_catalogue_and_scott(data)
    verify_cross_action_and_outer_cut(data, run_group_audit=run_group_audit)
    verify_secondary_decomposition(data)
    verify_external_sources(data)
    verify_conclusion(data)
    verify_bindings(data, check_git_history=check_git_bindings)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def run_tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("restore-r2", lambda value: value["conclusion"].__setitem__("remaining_degree_twelve_type_count", 1)),
        ("wrong-global-count", lambda value: value["conclusion"].__setitem__("remaining_global_transverse_type_count", 23)),
        ("claim-K3-close", lambda value: value["conclusion"].__setitem__("K3_closed", True)),
        ("move-ledger", lambda value: value["statement"].__setitem__("ledger_movement", 1)),
        ("drop-catalogue-row", lambda value: value["degree_twelve_primitive_catalogue"].pop()),
        ("small-inner-group", lambda value: value["degree_twelve_primitive_catalogue"][2].__setitem__("order", 12)),
        ("new-subdegree", lambda value: value["degree_twelve_primitive_catalogue"][0].__setitem__("subdegrees", [1, 5, 6])),
        ("kernel-trivial", lambda value: value["block_kernel_socle"].__setitem__("kernel_projection_nontrivial", False)),
        ("third-strip-partition", lambda value: value["scott_strip_dichotomy"]["invariant_support_partitions"].append("two_plus_three")),
        ("independent-survives", lambda value: value["scott_strip_dichotomy"].__setitem__("independent_case_survives", True)),
        ("short-M12-cross-orbit", lambda value: value["m12_cross_action_audit"].__setitem__("cross_action_orbit_lengths", [1, 11])),
        ("mutate-M12-generator", lambda value: value["m12_cross_action_audit"]["action_12b_generator_a_cycles"][0].__setitem__(1, 4)),
        ("retain-Dickson-row", lambda value: value["outer_subdegree_conclusion"].__setitem__("surviving_outer_subdegree", 2)),
        ("nontrivial-centralizer", lambda value: value["diagonal_normalizer_columns"].__setitem__("centralizer_in_Sym12_order", 2)),
        ("wrong-column-size", lambda value: value["diagonal_normalizer_columns"].__setitem__("secondary_block_size", 4)),
        ("weaken-degree5-quantifier", lambda value: value["degree_five_import"].__setitem__("quantifier", "one decomposition")),
        ("nonbijective-fifth-power", lambda value: value["degree_five_import"].__setitem__("fifth_power_map_on_K_is_bijective", False)),
        ("source-binding", lambda value: value["source_bindings"][0].__setitem__("blob_oid", "0" * 40)),
        ("drop-nonclaim", lambda value: value["nonclaims"].pop()),
        ("extra-top-level-field", lambda value: value.__setitem__("extra", 1)),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(
                candidate,
                check_git_bindings=False,
                run_group_audit=False,
            )
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")

    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(
            bad_hash,
            check_git_bindings=False,
            run_group_audit=False,
        )
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload-hash")

    try:
        parse_json_text('{"duplicate":1,"duplicate":2}', "duplicate-key test")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: duplicate-json-key")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify the committed certificate")
    parser.add_argument(
        "--tamper-selftest",
        action="store_true",
        help="run fail-closed semantic mutation tests",
    )
    arguments = parser.parse_args()
    if not arguments.check and not arguments.tamper_selftest:
        parser.error("at least one of --check or --tamper-selftest is required")

    certificate = load_json(CERTIFICATE)
    verify_certificate(certificate, check_git_bindings=True)
    print("PASS: m=12 row empty via diagonal socle and secondary inner degree five")
    if arguments.tamper_selftest:
        count = run_tamper_selftest(certificate)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
