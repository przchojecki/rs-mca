#!/usr/bin/env python3
"""Verify the KoalaBear m4 adjacency-orbital genus exclusion."""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
import subprocess
from pathlib import Path
from typing import Any, Callable

if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


EXPERIMENTAL = Path(__file__).resolve().parents[1]
REPO_ROOT = EXPERIMENTAL.parent
CERTIFICATE = (
    EXPERIMENTAL
    / "data/certificates/kb-mca-v4-m4-adjacency-genus-exclusion-v1"
    / "kb_mca_v4_m4_adjacency_genus_exclusion_v1.json"
)
SOURCE_PARENT = {
    "commit": "59c4449ca0f5cee929dd39fc7b5ae8b0a33877f4",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-primitive-subdegree4-route-cut-v1/kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.json",
    "certificate_blob_oid": "7e8a79db97dc56125f25d9a190c3b0c3adca158a",
    "certificate_payload_sha256": "21a8ca7800745c2c94876d48473801e84f4d9c8f9e6ce5b53e8b8bd66b699962",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_degree60_primitive_subdegree4_route_cut_v1.md",
    "note_blob_oid": "5d0ec0315fca34de80c22983b76bbafa12dd5661",
    "imported_component_u": 2,
    "imported_source_bidegree": [2, 4],
    "imported_self_correspondence_bidegree": [4, 4],
    "imported_source_genus_upper_bound": 3,
    "imported_birationality": True,
}
TRANSVERSE_PARENT = {
    "commit": "e287c54252c7872e1745c7594cfef62b74a65cf5",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-degree60-source-pencil-rank-compiler-v1/kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json",
    "certificate_blob_oid": "5c16c7884b349d7e474b8dfc1267ab357ef0d477",
    "certificate_payload_sha256": "6d4bc83e40e491f02f7d265b021628ffb7d52b1978c0655f83e5a9d3e0a9f4bb",
    "imported_terminal": "TRANSVERSE_OUTER_CORRESPONDENCE",
    "imported_degree_identity": "delta*r=4*m",
    "imported_m4_row": [8, 2],
}
PASSPORT_PARENT = {
    "commit": "4e33c7be8b3b29848e0ceb8fd7f50dce45fb2eed",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m4-a6s6-genus-zero-passport-reduction-v1/kb_mca_v4_m4_a6s6_genus_zero_passport_reduction_v1.json",
    "certificate_blob_oid": "c9be4609a28f4c4b89c099e09a359f833dbf7e1b",
    "certificate_payload_sha256": "c9cfbbf394e479f93d8d8378d886331c8afbbaf338e6fc6b21f55e3e1c485fd7",
    "imported_terminal": "M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS",
    "imported_passport_count": 4,
}
EXPECTED_PARENT_PASSPORTS = [
    ["A6", ["5.1", "2.2.1.1", "4.2"]],
    ["S6", ["5.1", "2.1.1.1.1", "2.2.1.1", "2.2.2"]],
    ["S6", ["5.1", "2.1.1.1.1", "6"]],
    ["S6", ["5.1", "2.2.2", "3.2.1"]],
]
PAIR_MASKS = tuple(
    sum(1 << letter for letter in pair)
    for pair in itertools.combinations(range(6), 2)
)
ADJACENCY = tuple(
    (left, right)
    for left in PAIR_MASKS
    for right in PAIR_MASKS
    if (left & right).bit_count() == 1
)
CYCLE_TYPES = (
    (6,),
    (5, 1),
    (4, 2),
    (3, 2, 1),
    (2, 1, 1, 1, 1),
    (2, 2, 1, 1),
    (2, 2, 2),
)
PASSPORTS = (
    ("A6_542", "A6", ((5, 1), (2, 2, 1, 1), (4, 2))),
    (
        "S6_four_point",
        "S6",
        ((5, 1), (2, 1, 1, 1, 1), (2, 2, 1, 1), (2, 2, 2)),
    ),
    ("S6_652", "S6", ((5, 1), (2, 1, 1, 1, 1), (6,))),
    ("S6_562", "S6", ((5, 1), (2, 2, 2), (3, 2, 1))),
)
EXPECTED_PASSPORT_ROWS = {
    "A6_542": (246, 4, 7),
    "S6_four_point": (264, 13, 25),
    "S6_652": (244, 3, 5),
    "S6_562": (250, 6, 11),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = copy.deepcopy(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicates(pairs):
    result = {}
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


def git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=REPO_ROOT, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as error:
        raise VerificationError(error.stderr.strip()) from error
    return result.stdout.strip()


def cycle_label(cycle_type: tuple[int, ...]) -> str:
    return ".".join(map(str, cycle_type))


def representative(cycle_type: tuple[int, ...]) -> tuple[int, ...]:
    value = list(range(6))
    offset = 0
    for length in cycle_type:
        cycle = list(range(offset, offset + length))
        for index, point in enumerate(cycle):
            value[point] = cycle[(index + 1) % length]
        offset += length
    require(offset == 6, "letter cycle is not degree six")
    return tuple(value)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[point]] for point in range(6))


def permutation_power(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(6))
    for _ in range(exponent):
        result = compose(value, result)
    return result


def permutation_sign(value: tuple[int, ...]) -> int:
    inversions = sum(
        value[left] > value[right]
        for left in range(6)
        for right in range(left + 1, 6)
    )
    return -1 if inversions % 2 else 1


def transport_mask(value: tuple[int, ...], mask: int) -> int:
    return sum(
        1 << value[letter] for letter in range(6) if mask & (1 << letter)
    )


def induced_adjacency_action(value: tuple[int, ...]) -> tuple[int, ...]:
    index = {state: position for position, state in enumerate(ADJACENCY)}
    return tuple(
        index[(transport_mask(value, left), transport_mask(value, right))]
        for left, right in ADJACENCY
    )


def direct_cycles(action: tuple[int, ...]) -> list[int]:
    unseen = set(range(len(action)))
    lengths = []
    while unseen:
        start = min(unseen)
        point = start
        length = 0
        while point in unseen:
            unseen.remove(point)
            point = action[point]
            length += 1
        lengths.append(length)
    return sorted(lengths, reverse=True)


def fixed_adjacency_states(value: tuple[int, ...]) -> int:
    return sum(
        transport_mask(value, left) == left
        and transport_mask(value, right) == right
        for left, right in ADJACENCY
    )


def cycle_row(cycle_type: tuple[int, ...]) -> dict[str, Any]:
    value = representative(cycle_type)
    order = math.lcm(*cycle_type)
    fixed_points = [
        fixed_adjacency_states(permutation_power(value, exponent))
        for exponent in range(order)
    ]
    require(sum(fixed_points) % order == 0, "Burnside average is nonintegral")
    burnside_count = sum(fixed_points) // order
    direct = direct_cycles(induced_adjacency_action(value))
    require(burnside_count == len(direct), "cycle-count implementations disagree")
    return {
        "letter_cycle_type": cycle_label(cycle_type),
        "letter_order": order,
        "fixed_points_of_powers": fixed_points,
        "cycle_count_burnside": burnside_count,
        "cycle_count_direct": len(direct),
        "adjacency_cycle_type": direct,
        "index": len(ADJACENCY) - len(direct),
    }


def group_rows() -> dict[str, Any]:
    symmetric = tuple(itertools.permutations(range(6)))
    alternating = tuple(value for value in symmetric if permutation_sign(value) == 1)
    base_pair = PAIR_MASKS[0]
    base_state = ADJACENCY[0]
    rows = {}
    for name, group in (("S6", symmetric), ("A6", alternating)):
        stabilizer = tuple(
            value
            for value in group
            if transport_mask(value, base_pair) == base_pair
        )
        unseen = set(PAIR_MASKS)
        subdegrees = []
        while unseen:
            seed = min(unseen)
            current = {transport_mask(value, seed) for value in stabilizer}
            subdegrees.append(len(current))
            unseen -= current
        orbit = {
            (
                transport_mask(value, base_state[0]),
                transport_mask(value, base_state[1]),
            )
            for value in group
        }
        require(sorted(subdegrees) == [1, 6, 8], f"{name} subdegrees")
        require(len(orbit) == 120, f"{name} adjacency transitivity")
        rows[name] = {
            "order": len(group),
            "pair_stabilizer_order": len(stabilizer),
            "pair_subdegrees": sorted(subdegrees),
            "ordered_adjacency_orbit": len(orbit),
        }
    require(rows["S6"]["order"] == 720, "S6 order")
    require(rows["A6"]["order"] == 360, "A6 order")
    return rows


def build_certificate() -> dict[str, Any]:
    require(len(PAIR_MASKS) == 15, "pair count")
    require(len(ADJACENCY) == 120, "adjacency count")
    cycle_rows = [cycle_row(cycle_type) for cycle_type in CYCLE_TYPES]
    by_type = {row["letter_cycle_type"]: row for row in cycle_rows}
    passport_rows = []
    for name, group, cycle_types in PASSPORTS:
        total_index = sum(by_type[cycle_label(kind)]["index"] for kind in cycle_types)
        genus_numerator = -2 * len(ADJACENCY) + total_index
        require(genus_numerator % 2 == 0, "outer genus is nonintegral")
        outer_genus = 1 + genus_numerator // 2
        minimum_source_genus = 2 * outer_genus - 1
        require(
            (total_index, outer_genus, minimum_source_genus)
            == EXPECTED_PASSPORT_ROWS[name],
            f"{name} genus row",
        )
        require(minimum_source_genus > 3, f"{name} did not contradict source")
        passport_rows.append(
            {
                "name": name,
                "group": group,
                "letter_cycle_types": [cycle_label(kind) for kind in cycle_types],
                "total_adjacency_branch_index": total_index,
                "outer_adjacency_genus": outer_genus,
                "minimum_degree_two_source_genus": minimum_source_genus,
                "actual_source_genus_upper_bound": 3,
                "contradiction_margin": minimum_source_genus - 3,
                "excluded": True,
            }
        )
    result = {
        "schema": "kb-mca-v4-m4-adjacency-genus-exclusion-v1",
        "payload_sha256": "",
        "statement": {
            "row": "KoalaBear MCA at 2^-128",
            "workboard_item": "K3",
            "terminal": "M4_TRANSVERSE_ROW_EMPTY_BY_ADJACENCY_GENUS",
            "ledger_movement": 0,
        },
        "parent_source_route": copy.deepcopy(SOURCE_PARENT),
        "parent_transverse_compiler": copy.deepcopy(TRANSVERSE_PARENT),
        "parent_passport_reduction": copy.deepcopy(PASSPORT_PARENT),
        "geometry": {
            "source_component_bidegree": [2, 4],
            "source_arithmetic_genus": 3,
            "source_normalization_genus_upper_bound": 3,
            "birational_self_correspondence_bidegree": [4, 4],
            "outer_component_bidegree": [8, 8],
            "component_to_outer_degree": 2,
            "deployed_characteristic": 2130706433,
            "degree_two_map_separable": True,
            "riemann_hurwitz_source_lower_bound": "g_source>=2*g_outer-1",
        },
        "orbital": {
            "letters": 6,
            "two_subsets": len(PAIR_MASKS),
            "relation": "ordered_distinct_pairs_intersecting_in_one_letter",
            "ordered_adjacency_states": len(ADJACENCY),
            "group_rows": group_rows(),
        },
        "branch_cycle_rows": cycle_rows,
        "passport_rows": passport_rows,
        "conclusion": {
            "exhaustive_passports_excluded": 4,
            "m4_transverse_row_empty": True,
            "independent_frontier_before": 9,
            "independent_frontier_after": 8,
            "remaining_inner_degrees": [2, 3],
            "remaining_type_counts": {"m2": 3, "m3": 5},
            "terminal": "M4_TRANSVERSE_ROW_EMPTY_BY_ADJACENCY_GENUS",
        },
        "source_bindings": {
            "permutation_action": "exact S6 enumeration on ordered adjacent two-subsets",
            "cycle_count_method_one": "direct induced-permutation cycle traversal",
            "cycle_count_method_two": "Burnside average of fixed points of powers",
            "curve_genus": "tame Riemann-Hurwitz on the connected 120-sheet orbital cover",
            "source_contradiction": "separable degree-two Riemann-Hurwitz",
        },
        "nonclaims": [
            "no inner-degree-two or inner-degree-three deletion",
            "no carrier, received-data, explaining-polynomial, or slope owner",
            "no u2, K3, KoalaBear row, endpoint, or prize closure",
            "no ledger movement",
        ],
    }
    result["payload_sha256"] = payload_hash(result)
    return result


def load_parent(binding: dict[str, Any], label: str) -> dict[str, Any]:
    commit = binding["commit"]
    path = binding["certificate_path"]
    require(
        git_output("rev-parse", f"{commit}:{path}")
        == binding["certificate_blob_oid"],
        f"{label} certificate blob",
    )
    parent = parse_json(git_output("show", f"{commit}:{path}"), label)
    require(
        payload_hash(parent)
        == parent["payload_sha256"]
        == binding["certificate_payload_sha256"],
        f"{label} payload",
    )
    return parent


def verify_parent_bindings() -> None:
    source = load_parent(SOURCE_PARENT, "source route parent")
    require(source["statement"]["component_u"] == 2, "source u")
    require(
        source["statement"]["downstairs_component_bidegree"] == [4, 4],
        "source self-correspondence bidegree",
    )
    require(
        source["complete_source_quartic_defect_gate"][
            "rational_plane_quartic_arithmetic_genus"
        ]
        == 3,
        "source genus upper bound",
    )
    require(
        git_output(
            "rev-parse", f"{SOURCE_PARENT['commit']}:{SOURCE_PARENT['note_path']}"
        )
        == SOURCE_PARENT["note_blob_oid"],
        "source note blob",
    )
    source_note = git_output(
        "show", f"{SOURCE_PARENT['commit']}:{SOURCE_PARENT['note_path']}"
    )
    require("bidegree \\((u,2u)\\)" in source_note, "source bidegree theorem")
    require("this map is birational" in source_note, "source birationality theorem")
    require("Thus \\(H_0\\to\\Gamma\\) is birational" in source_note, "source gate")

    transverse = load_parent(TRANSVERSE_PARENT, "transverse parent")
    terminal = transverse["transverse_outer_terminal"]
    require(terminal["terminal"] == "TRANSVERSE_OUTER_CORRESPONDENCE", "transverse terminal")
    require(terminal["degree_identity"] == "delta*r=4*m", "degree identity")
    m4 = next(row for row in terminal["rows"] if row["m"] == 4)
    require([8, 2] in m4["r_delta"], "m4 r-delta row")

    passports = load_parent(PASSPORT_PARENT, "passport parent")
    require(
        passports["conclusion"]["terminal"]
        == "M4_A6S6_GEOMETRIC_FRONTIER_FOUR_PASSPORTS",
        "passport terminal",
    )
    require(
        passports["conclusion"]["retained"] == EXPECTED_PARENT_PASSPORTS,
        "passport frontier",
    )


def verify_certificate(data: dict[str, Any], check_git: bool = True) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "payload hash")
    expected = build_certificate()
    require(data == expected, "certificate differs from exact reconstruction")
    if check_git:
        verify_parent_bindings()


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(original: dict[str, Any]) -> int:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("source-parent", lambda row: row["parent_source_route"].__setitem__("note_blob_oid", "0" * 40)),
        ("transverse-parent", lambda row: row["parent_transverse_compiler"].__setitem__("imported_degree_identity", "delta*r=2*m")),
        ("passport-parent", lambda row: row["parent_passport_reduction"].__setitem__("imported_passport_count", 3)),
        ("source-genus", lambda row: row["geometry"].__setitem__("source_normalization_genus_upper_bound", 4)),
        ("map-degree", lambda row: row["geometry"].__setitem__("component_to_outer_degree", 1)),
        ("separability", lambda row: row["geometry"].__setitem__("degree_two_map_separable", False)),
        ("group-order", lambda row: row["orbital"]["group_rows"]["A6"].__setitem__("order", 720)),
        ("orbit", lambda row: row["orbital"].__setitem__("ordered_adjacency_states", 60)),
        ("fixed-points", lambda row: row["branch_cycle_rows"][0]["fixed_points_of_powers"].__setitem__(0, 119)),
        ("cycle-count", lambda row: row["branch_cycle_rows"][1].__setitem__("cycle_count_burnside", 23)),
        ("cycle-type", lambda row: row["branch_cycle_rows"][2]["adjacency_cycle_type"].pop()),
        ("index", lambda row: row["passport_rows"][0].__setitem__("total_adjacency_branch_index", 244)),
        ("genus", lambda row: row["passport_rows"][1].__setitem__("outer_adjacency_genus", 12)),
        ("source-lower", lambda row: row["passport_rows"][2].__setitem__("minimum_degree_two_source_genus", 3)),
        ("drop-passport", lambda row: row["passport_rows"].pop()),
        ("frontier", lambda row: row["conclusion"].__setitem__("independent_frontier_after", 9)),
        ("nonclaim", lambda row: row["nonclaims"].pop()),
    ]
    passed = 0
    for name, mutate in mutations:
        candidate = copy.deepcopy(original)
        mutate(candidate)
        reseal(candidate)
        try:
            verify_certificate(candidate, False)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    bad_hash = copy.deepcopy(original)
    bad_hash["payload_sha256"] = "0" * 64
    try:
        verify_certificate(bad_hash, False)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: payload")
    try:
        parse_json('{"x":1,"x":2}', "duplicate")
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("duplicate key survived")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not args.write and not args.check and not args.tamper_selftest:
        parser.error("at least one action is required")
    if args.write:
        verify_parent_bindings()
        data = build_certificate()
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        print(f"WROTE: {CERTIFICATE.relative_to(REPO_ROOT)}")
    data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
    verify_certificate(data, True)
    print("PASS: all four m4 passports are excluded by adjacency genus")
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} tamper mutations rejected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
