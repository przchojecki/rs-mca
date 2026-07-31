#!/usr/bin/env python3
"""Verify the KoalaBear m10 Scott-strip lower-degree router."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from itertools import combinations, permutations
from pathlib import Path
from typing import Any, Callable


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-m10-scott-strip-lower-degree-router-v1"
    / "kb_mca_v4_m10_scott_strip_lower_degree_router_v1.json"
)
SCHEMA = "kb-mca-v4-m10-scott-strip-lower-degree-router-v1"
COMPILER_COMMIT = "e287c54252c7872e1745c7594cfef62b74a65cf5"
COMPILER_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-degree60-source-pencil-rank-compiler-v1/"
    "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
)
COMPILER_BLOB = "5c16c7884b349d7e474b8dfc1267ab357ef0d477"
COMPILER_PAYLOAD = (
    "6d4bc83e40e491f02f7d265b021628ffb7d52b1978c0655f83e5a9d3e0a9f4bb"
)
FRONTIER_COMMIT = "c23eb801af8853d0369a72ea8834c84e7a3242f6"
FRONTIER_PATH = (
    "experimental/data/certificates/"
    "kb-mca-v4-m12-diagonal-socle-degree5-close-v1/"
    "kb_mca_v4_m12_diagonal_socle_degree5_close_v1.json"
)
FRONTIER_BLOB = "9e1bd3d89dac6409f148dc134fda46d3bf644c11"
FRONTIER_PAYLOAD = (
    "456b51c78e837c8a27ffda0b43409c63c88128b254be320723728868db096e6f"
)
M10_ROWS = [[1, 40], [2, 20], [4, 10], [5, 8]]
CATALOGUE = [
    {"group": "A5", "order": 60, "socle": "A5", "subdegrees": [1, 3, 6]},
    {"group": "S5", "order": 120, "socle": "A5", "subdegrees": [1, 3, 6]},
    {"group": "PSL(2,9)", "order": 360, "socle": "A6", "subdegrees": [1, 9]},
    {"group": "PGL(2,9)", "order": 720, "socle": "A6", "subdegrees": [1, 9]},
    {"group": "PSigmaL(2,9)", "order": 720, "socle": "A6", "subdegrees": [1, 9]},
    {"group": "M10", "order": 720, "socle": "A6", "subdegrees": [1, 9]},
    {"group": "PGammaL(2,9)", "order": 1_440, "socle": "A6", "subdegrees": [1, 9]},
    {"group": "A10", "order": 1_814_400, "socle": "A10", "subdegrees": [1, 9]},
    {"group": "S10", "order": 3_628_800, "socle": "A10", "subdegrees": [1, 9]},
]
EXPECTED_NONCLAIMS = [
    "Endpoints are not claimed to lack every degree-ten decomposition.",
    "No lower-degree transverse type is deleted or paid.",
    (
        "No endpoint-record census or carrier, data, explaining-polynomial, "
        "or slope bridge is claimed."
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


def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json(text: str, label: str) -> dict[str, Any]:
    try:
        value = json.loads(text, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, VerificationError) as error:
        raise VerificationError(f"cannot parse {label}: {error}") from error
    require(isinstance(value, dict), f"{label} is not an object")
    return value


def load_json(path: Path) -> dict[str, Any]:
    return parse_json(path.read_text(), str(path))


def git_output(*arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def exact_keys(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} is not an object")
    actual = set(value)
    require(actual == expected, f"{label} keys: {sorted(actual ^ expected)}")


def verify_schema(data: dict[str, Any]) -> None:
    exact_keys(
        data,
        {
            "schema",
            "payload_sha256",
            "statement",
            "parent_compiler",
            "incoming_frontier",
            "degree_ten_catalogue",
            "kernel_free_gate",
            "scott_strip_route",
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
            "endpoint_degree",
            "original_inner_degree",
            "original_outer_degree",
            "status",
            "ledger_movement",
        },
        "statement",
    )
    exact_keys(
        data["parent_compiler"],
        {
            "commit",
            "certificate_path",
            "certificate_blob_oid",
            "certificate_payload_sha256",
            "imported_terminal",
            "imported_m10_rows",
        },
        "parent compiler",
    )
    exact_keys(
        data["incoming_frontier"],
        {
            "commit",
            "certificate_path",
            "certificate_blob_oid",
            "certificate_payload_sha256",
            "imported_terminal",
            "global_transverse_type_count",
            "live_inner_degrees",
        },
        "incoming frontier",
    )
    for index, row in enumerate(data["degree_ten_catalogue"]):
        exact_keys(row, {"group", "order", "socle", "subdegrees"}, f"catalogue {index}")
    exact_keys(
        data["kernel_free_gate"],
        {
            "outer_point_stabilizer_order_upper_bound",
            "possible_inner_groups",
            "block_kernel_trivial",
            "global_groups",
            "flag_set",
            "flag_set_size",
            "A6_point_stabilizer_order",
            "A6_subdegrees",
            "S6_point_stabilizer_order",
            "S6_subdegrees",
            "subdegree_four_present",
            "terminal",
        },
        "kernel-free gate",
    )
    exact_keys(
        data["scott_strip_route"],
        {
            "derived_kernel",
            "subdirect_coordinate_count",
            "simple_socles",
            "support_partition_G_invariant",
            "support_sizes",
            "actual_suborbit_size",
            "actual_suborbit_transverse",
            "independent_other_block_orbit_size",
            "independent_support_size_survives",
            "all_socle_automorphisms_realized",
            "socle_action_centralizer_order",
            "column_block_size_formula",
            "secondary_inner_degrees",
            "terminal",
        },
        "Scott-strip route",
    )
    exact_keys(
        data["external_source_custody"],
        {
            "gap_primgrp_commit",
            "gap_degree10_entry_bytes",
            "gap_degree10_entry_sha256",
            "atlas_A6_page",
            "atlas_AutA6_degree10_page",
            "scott_doi",
            "scott_lemma_page",
        },
        "external source custody",
    )
    for index, binding in enumerate(data["source_bindings"]):
        exact_keys(
            binding,
            {"binding_id", "commit", "path", "blob_oid", "role"},
            f"binding {index}",
        )
    exact_keys(
        data["conclusion"],
        {
            "routed_m10_rows",
            "m10_terminal_type_count",
            "remaining_global_transverse_type_count",
            "remaining_inner_degrees",
            "terminal",
            "m10_routed",
            "all_m10_decompositions_nonexistent",
            "u2_closed",
            "K3_closed",
            "row_closed",
        },
        "conclusion",
    )
    require(isinstance(data["nonclaims"], list), "nonclaims is not a list")


def verify_statement_and_catalogue(data: dict[str, Any]) -> None:
    require(data["schema"] == SCHEMA, "schema")
    require(
        data["statement"]
        == {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "object": "MCA",
            "agreement": 1_116_048,
            "B_star": "274980728111395087",
            "endpoint_degree": 60,
            "original_inner_degree": 10,
            "original_outer_degree": 6,
            "status": "PROVED_M10_ROUTED_TO_INNER_DEGREES_2_3_6_OTHER_K3_ROWS_OPEN",
            "ledger_movement": 0,
        },
        "statement changed",
    )
    require(data["degree_ten_catalogue"] == CATALOGUE, "catalogue changed")
    require(len(CATALOGUE) == 9, "catalogue count")
    require({row["socle"] for row in CATALOGUE} == {"A5", "A6", "A10"}, "socles")
    require(
        [row["group"] for row in CATALOGUE if row["order"] <= 120] == ["A5", "S5"],
        "kernel-free candidates",
    )
    require(all(row["subdegrees"].count(1) == 1 for row in CATALOGUE), "fixed points")


POINTS = tuple(range(6))


def parity(permutation: tuple[int, ...]) -> int:
    return sum(
        permutation[i] > permutation[j]
        for i in POINTS
        for j in range(i + 1, 6)
    ) % 2


def flag_action(permutation: tuple[int, ...], flag: tuple[int, tuple[int, int]]):
    point, pair = flag
    return permutation[point], tuple(sorted(permutation[x] for x in pair))


def flag_subdegrees(group: list[tuple[int, ...]]):
    omega = [
        (point, pair)
        for point in POINTS
        for pair in combinations([x for x in POINTS if x != point], 2)
    ]
    base = (0, (1, 2))
    stabilizer = [g for g in group if flag_action(g, base) == base]
    unseen = set(omega)
    lengths = []
    while unseen:
        flag = min(unseen)
        orbit = {flag_action(g, flag) for g in stabilizer}
        unseen -= orbit
        lengths.append(len(orbit))
    return len(omega), len(stabilizer), sorted(lengths)


def verify_routes(data: dict[str, Any], *, run_flag_audit: bool) -> None:
    gate = data["kernel_free_gate"]
    expected_a6 = [1, 2] + [3] * 3 + [6] * 8
    expected_s6 = [1, 2] + [3] * 3 + [6] * 6 + [12]
    require(gate["outer_point_stabilizer_order_upper_bound"] == 120, "outer ceiling")
    require(gate["possible_inner_groups"] == ["A5", "S5"], "kernel-free groups")
    require(gate["block_kernel_trivial"] is True, "kernel-free flag")
    require(gate["global_groups"] == ["A6", "S6"], "global groups")
    require(
        gate["flag_set"]
        == "(i,A) with i in six points and A a disjoint two-subset",
        "flag set",
    )
    require(gate["flag_set_size"] == 60, "flag size")
    require(gate["A6_point_stabilizer_order"] == 6, "A6 stabilizer")
    require(gate["S6_point_stabilizer_order"] == 12, "S6 stabilizer")
    require(gate["A6_subdegrees"] == expected_a6, "A6 subdegrees")
    require(gate["S6_subdegrees"] == expected_s6, "S6 subdegrees")
    require(gate["subdegree_four_present"] is False, "subdegree four")
    require(gate["terminal"] == "KERNEL_FREE_M10_FLAG_ACTIONS_EXCLUDED", "flag terminal")
    if run_flag_audit:
        all_permutations = list(permutations(POINTS))
        a6 = [g for g in all_permutations if parity(g) == 0]
        require(flag_subdegrees(a6) == (60, 6, expected_a6), "A6 replay")
        require(flag_subdegrees(all_permutations) == (60, 12, expected_s6), "S6 replay")

    route = data["scott_strip_route"]
    require(route["derived_kernel"] == "D=[N,N]", "derived kernel")
    require(route["subdirect_coordinate_count"] == 6, "coordinate count")
    require(route["simple_socles"] == ["A5", "A6", "A10"], "route socles")
    require(route["support_partition_G_invariant"] is True, "support invariance")
    require(route["support_sizes"] == [1, 2, 3, 6], "support sizes")
    require(route["actual_suborbit_size"] == 4, "actual suborbit")
    require(route["actual_suborbit_transverse"] is True, "transversality")
    require(route["independent_other_block_orbit_size"] == 10, "independent orbit")
    require(10 > 4, "independent contradiction")
    require(route["independent_support_size_survives"] is False, "independent flag")
    require(route["all_socle_automorphisms_realized"] is True, "automorphisms")
    require(route["socle_action_centralizer_order"] == 1, "centralizer")
    require(route["column_block_size_formula"] == "support size t", "column size")
    require(route["secondary_inner_degrees"] == [2, 3, 6], "secondary degrees")
    require(all(degree < 10 for degree in route["secondary_inner_degrees"]), "strictness")
    require(
        route["terminal"] == "M10_STRICTLY_ROUTED_TO_LOWER_DECOMPOSITION",
        "route terminal",
    )


def verify_parents_and_bindings(
    data: dict[str, Any], *, check_git: bool
) -> None:
    parent = data["parent_compiler"]
    require(parent["commit"] == COMPILER_COMMIT, "compiler commit")
    require(parent["certificate_path"] == COMPILER_PATH, "compiler path")
    require(parent["certificate_blob_oid"] == COMPILER_BLOB, "compiler blob")
    require(parent["certificate_payload_sha256"] == COMPILER_PAYLOAD, "compiler payload")
    require(parent["imported_terminal"] == "TRANSVERSE_OUTER_CORRESPONDENCE_UNPAID", "compiler terminal")
    require(parent["imported_m10_rows"] == M10_ROWS, "compiler rows")

    frontier = data["incoming_frontier"]
    require(frontier["commit"] == FRONTIER_COMMIT, "frontier commit")
    require(frontier["certificate_path"] == FRONTIER_PATH, "frontier path")
    require(frontier["certificate_blob_oid"] == FRONTIER_BLOB, "frontier blob")
    require(frontier["certificate_payload_sha256"] == FRONTIER_PAYLOAD, "frontier payload")
    require(frontier["imported_terminal"] == "M12_DECOMPOSITION_ROW_EMPTY", "frontier terminal")
    require(frontier["global_transverse_type_count"] == 22, "incoming count")
    require(frontier["live_inner_degrees"] == [2, 3, 4, 6, 10], "incoming degrees")

    expected_bindings = [
        {
            "binding_id": "KB_M10_ROUTER::compiler_certificate",
            "commit": COMPILER_COMMIT,
            "path": COMPILER_PATH,
            "blob_oid": COMPILER_BLOB,
            "role": "terminal m10 transverse rows and primitive degree-ten group count",
        },
        {
            "binding_id": "KB_M10_ROUTER::compiler_note",
            "commit": COMPILER_COMMIT,
            "path": (
                "experimental/notes/frontier-adjacent/"
                "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.md"
            ),
            "blob_oid": "b4a69440c518f22189ec2060cb3a3a500a23e724",
            "role": "actual transverse size-four suborbit and geometric route scope",
        },
        {
            "binding_id": "KB_M10_ROUTER::incoming_frontier_certificate",
            "commit": FRONTIER_COMMIT,
            "path": FRONTIER_PATH,
            "blob_oid": FRONTIER_BLOB,
            "role": "22-type frontier after complete m12 deletion",
        },
    ]
    require(data["source_bindings"] == expected_bindings, "bindings changed")
    if not check_git:
        return
    for row in data["source_bindings"]:
        require(
            git_output("rev-parse", f"{row['commit']}:{row['path']}") == row["blob_oid"],
            f"binding blob {row['binding_id']}",
        )
    compiler = parse_json(
        git_output("show", f"{COMPILER_COMMIT}:{COMPILER_PATH}"), "compiler"
    )
    require(payload_hash(compiler) == compiler["payload_sha256"] == COMPILER_PAYLOAD, "compiler hash")
    m10 = next(
        row for row in compiler["transverse_outer_terminal"]["rows"] if row["m"] == 10
    )
    require(m10["r_delta"] == M10_ROWS, "historical m10 rows")
    degree10 = next(
        row
        for row in compiler["same_fiber_route_cut"]["small_degree_catalogue"]
        if row["degree"] == 10
    )
    require(degree10["primitive_group_count"] == 9, "historical group count")

    prior = parse_json(
        git_output("show", f"{FRONTIER_COMMIT}:{FRONTIER_PATH}"), "frontier"
    )
    require(payload_hash(prior) == prior["payload_sha256"] == FRONTIER_PAYLOAD, "frontier hash")
    require(prior["conclusion"]["remaining_global_transverse_type_count"] == 22, "historical count")


def verify_conclusion(data: dict[str, Any]) -> None:
    custody = data["external_source_custody"]
    require(custody["gap_primgrp_commit"] == "5612e113d50ac23a7d10945383936e20440b4e14", "GAP commit")
    require(custody["gap_degree10_entry_bytes"] == 1272, "entry bytes")
    require(
        custody["gap_degree10_entry_sha256"]
        == "9cf136ffbea68f3156bc2ff386b5aec7b510a77e13e77ad6a09904b02382a69e",
        "entry hash",
    )
    require(custody["scott_doi"] == "10.1090/pspum/037/604599", "Scott DOI")
    require(custody["scott_lemma_page"] == 328, "Scott page")
    require(
        custody["atlas_A6_page"] == "https://brauer.maths.qmul.ac.uk/Atlas/alt/A6/",
        "ATLAS A6 URL",
    )
    require(
        custody["atlas_AutA6_degree10_page"]
        == "https://brauer.maths.qmul.ac.uk/Atlas/v3/permrep/A6V4G1-p10B0",
        "ATLAS Aut(A6) URL",
    )

    conclusion = data["conclusion"]
    require(conclusion["routed_m10_rows"] == M10_ROWS, "routed rows")
    require(conclusion["m10_terminal_type_count"] == 0, "m10 type count")
    require(conclusion["remaining_global_transverse_type_count"] == 18, "global count")
    require(22 - len(M10_ROWS) == 18, "count arithmetic")
    require(conclusion["remaining_inner_degrees"] == [2, 3, 4, 6], "live degrees")
    require(conclusion["terminal"] == "M10_NO_TERMINAL_PRODUCER_ROUTES_TO_M2_M3_M6", "terminal")
    require(conclusion["m10_routed"] is True, "route flag")
    require(conclusion["all_m10_decompositions_nonexistent"] is False, "nonexistence overclaim")
    for key in ("u2_closed", "K3_closed", "row_closed"):
        require(conclusion[key] is False, f"forbidden close {key}")
    require(data["nonclaims"] == EXPECTED_NONCLAIMS, "nonclaims")


def verify_certificate(
    data: dict[str, Any], *, check_git: bool = True, run_flag_audit: bool = True
) -> None:
    verify_schema(data)
    require(payload_hash(data) == data["payload_sha256"], "payload hash")
    verify_statement_and_catalogue(data)
    verify_routes(data, run_flag_audit=run_flag_audit)
    verify_parents_and_bindings(data, check_git=check_git)
    verify_conclusion(data)


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("drop-group", lambda value: value["degree_ten_catalogue"].pop()),
        ("small-group", lambda value: value["degree_ten_catalogue"][2].__setitem__("order", 100)),
        ("add-subdegree-four", lambda value: value["kernel_free_gate"]["A6_subdegrees"].append(4)),
        ("flag-four", lambda value: value["kernel_free_gate"].__setitem__("subdegree_four_present", True)),
        ("new-support", lambda value: value["scott_strip_route"]["support_sizes"].append(4)),
        ("independent-survives", lambda value: value["scott_strip_route"].__setitem__("independent_support_size_survives", True)),
        ("centralizer", lambda value: value["scott_strip_route"].__setitem__("socle_action_centralizer_order", 2)),
        ("drop-degree", lambda value: value["scott_strip_route"]["secondary_inner_degrees"].pop()),
        ("not-strict", lambda value: value["scott_strip_route"].__setitem__("secondary_inner_degrees", [10])),
        ("parent-payload", lambda value: value["parent_compiler"].__setitem__("certificate_payload_sha256", "0" * 64)),
        ("binding", lambda value: value["source_bindings"][0].__setitem__("blob_oid", "0" * 40)),
        ("wrong-count", lambda value: value["conclusion"].__setitem__("remaining_global_transverse_type_count", 19)),
        ("claim-nonexistence", lambda value: value["conclusion"].__setitem__("all_m10_decompositions_nonexistent", True)),
        ("claim-K3", lambda value: value["conclusion"].__setitem__("K3_closed", True)),
        ("move-ledger", lambda value: value["statement"].__setitem__("ledger_movement", 1)),
        ("drop-nonclaim", lambda value: value["nonclaims"].pop()),
        ("extra-field", lambda value: value.__setitem__("extra", 1)),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, check_git=False, run_flag_audit=False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, check_git=False, run_flag_audit=False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload")
    try:
        parse_json('{"x":1,"x":2}', "duplicate test")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("duplicate key survived")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    arguments = parser.parse_args()
    if not arguments.check and not arguments.tamper_selftest:
        parser.error("at least one action is required")
    data = load_json(CERTIFICATE)
    verify_certificate(data)
    print("PASS: m10 routes strictly to inner degree 2, 3, or 6")
    if arguments.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
