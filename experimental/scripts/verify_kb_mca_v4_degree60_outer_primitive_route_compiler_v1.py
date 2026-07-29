#!/usr/bin/env python3
"""Verify the degree-60 outer primitive-subdegree route compiler.

The load-bearing completeness replay lives in the companion Sage/GAP file.
This verifier binds the parent packets, reconstructs the 26-row transverse
ledger, applies the two m=12 deletions, intersects every remaining row with
the exact outer primitive-group catalogue, and checks the recursive
decomposition graph, its field-theoretic loop deletion, and the surviving
low-genus Nielsen passports.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Callable


if not __debug__:
    raise RuntimeError("optimized Python is not supported")


class VerificationError(RuntimeError):
    """Fail-closed certificate error."""


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-outer-primitive-route-compiler-v1"
    / "kb_mca_v4_degree60_outer_primitive_route_compiler_v1.json"
)
SOURCE_CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-degree60-source-pencil-rank-compiler-v1"
    / "kb_mca_v4_degree60_source_pencil_rank_compiler_v1.json"
)
M12_CUT_CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-m12-outer-subdegree-route-cut-v1"
    / "kb_mca_v4_m12_outer_subdegree_route_cut_v1.json"
)
M12_NORMAL_CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-m12-outer-normal-form-compiler-v1"
    / "kb_mca_v4_m12_outer_normal_form_compiler_v1.json"
)
SAGE_REPLAY = (
    ROOT
    / "scripts"
    / "replay_kb_mca_v4_degree60_outer_primitive_route_compiler_v1.sage"
)
WOLFRAM_REPLAY = (
    ROOT
    / "scripts"
    / "replay_kb_mca_v4_degree60_outer_primitive_route_compiler_v1.wl"
)

SOURCE_COMMIT = "e287c54252c7872e1745c7594cfef62b74a65cf5"
SOURCE_BLOB = "5c16c7884b349d7e474b8dfc1267ab357ef0d477"
SOURCE_PAYLOAD = (
    "6d4bc83e40e491f02f7d265b021628ff"
    "b7d52b1978c0655f83e5a9d3e0a9f4bb"
)
M12_CUT_COMMIT = "e368e5c8fc101ae0040b47265c2cd167e70dadd2"
M12_CUT_BLOB = "6ea55700f303869a850c79c66c331842e0eed385"
M12_CUT_PAYLOAD = (
    "4349f6ca07b991fe78b90c66feb1fdcb"
    "1df582ac19d34c50d354c3c91c9e6b63"
)
M12_NORMAL_COMMIT = "f7a42415bdb24c7e626b76394558bad100c5a874"
M12_NORMAL_BLOB = "8e0ecd7f5b008900ada67dbf80848e8dbbff8416"
M12_NORMAL_PAYLOAD = (
    "7eb4f4053f90cb4ca0d0f3379fa3f8f"
    "33522ae0ec9b3dc67f5c7e602150d22f0"
)

ALLOWED_SOURCE_INNER_DEGREES = {2, 3, 4, 5, 6, 10, 12, 30}
TERMINAL_INNER_DEGREES = {2, 3, 4, 6, 10, 12}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in output, f"duplicate JSON key: {key}")
        output[key] = value
    return output


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle, object_pairs_hook=reject_duplicate_keys)
    require(isinstance(value, dict), f"{path.name}: top level is not an object")
    return value


def canonical_bytes(data: dict[str, Any]) -> bytes:
    payload = copy.deepcopy(data)
    payload.pop("payload_sha256", None)
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def payload_hash(data: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_bytes(data)).hexdigest()


def git_blob_oid(path: Path) -> str:
    content = path.read_bytes()
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parent_packets() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source = load_json(SOURCE_CERTIFICATE)
    m12_cut = load_json(M12_CUT_CERTIFICATE)
    m12_normal = load_json(M12_NORMAL_CERTIFICATE)

    require(source["payload_sha256"] == SOURCE_PAYLOAD, "source payload")
    require(git_blob_oid(SOURCE_CERTIFICATE) == SOURCE_BLOB, "source blob")
    require(m12_cut["payload_sha256"] == M12_CUT_PAYLOAD, "m12 cut payload")
    require(git_blob_oid(M12_CUT_CERTIFICATE) == M12_CUT_BLOB, "m12 cut blob")
    require(
        m12_normal["payload_sha256"] == M12_NORMAL_PAYLOAD,
        "m12 normal-form payload",
    )
    require(
        git_blob_oid(M12_NORMAL_CERTIFICATE) == M12_NORMAL_BLOB,
        "m12 normal-form blob",
    )
    require(
        m12_cut["parent_stack"]["head_commit"] == SOURCE_COMMIT,
        "m12 cut source commit",
    )
    require(
        m12_normal["parent_stack"]["head_commit"] == M12_CUT_COMMIT,
        "m12 normal-form cut commit",
    )
    return source, m12_cut, m12_normal


def group(
    index: int,
    name: str,
    order: int,
    subdegrees: list[int],
) -> dict[str, Any]:
    require(subdegrees[0] == 1, "subdegree row lacks diagonal orbit")
    non_diagonal = list(subdegrees)
    non_diagonal.remove(1)
    return {
        "primitive_group_index": index,
        "structure": name,
        "order": order,
        "subdegrees": subdegrees,
        "non_diagonal_subdegrees": non_diagonal,
    }


def primitive_catalogue() -> list[dict[str, Any]]:
    return [
        {
            "degree": 30,
            "primitive_group_count": 4,
            "groups": [
                group(1, "PSL(2,29)", 12_180, [1, 29]),
                group(2, "PSL(2,29) : C2", 24_360, [1, 29]),
                group(
                    3,
                    "A30",
                    132_626_429_906_095_529_318_154_240_000_000,
                    [1, 29],
                ),
                group(
                    4,
                    "S30",
                    265_252_859_812_191_058_636_308_480_000_000,
                    [1, 29],
                ),
            ],
        },
        {
            "degree": 20,
            "primitive_group_count": 4,
            "groups": [
                group(1, "PSL(2,19)", 3_420, [1, 19]),
                group(2, "PSL(2,19) : C2", 6_840, [1, 19]),
                group(3, "A20", 1_216_451_004_088_320_000, [1, 19]),
                group(4, "S20", 2_432_902_008_176_640_000, [1, 19]),
            ],
        },
        {
            "degree": 15,
            "primitive_group_count": 6,
            "groups": [
                group(1, "A7", 2_520, [1, 14]),
                group(2, "A6", 360, [1, 6, 8]),
                group(3, "S6", 720, [1, 6, 8]),
                group(4, "A8", 20_160, [1, 14]),
                group(5, "A15", 653_837_184_000, [1, 14]),
                group(6, "S15", 1_307_674_368_000, [1, 14]),
            ],
        },
        {
            "degree": 10,
            "primitive_group_count": 9,
            "groups": [
                group(1, "A5", 60, [1, 3, 6]),
                group(2, "S5", 120, [1, 3, 6]),
                group(3, "A6", 360, [1, 9]),
                group(4, "A6 : C2", 720, [1, 9]),
                group(5, "S6", 720, [1, 9]),
                group(6, "A6 . C2", 720, [1, 9]),
                group(7, "(A6 : C2) : C2", 1_440, [1, 9]),
                group(8, "A10", 1_814_400, [1, 9]),
                group(9, "S10", 3_628_800, [1, 9]),
            ],
        },
        {
            "degree": 6,
            "primitive_group_count": 4,
            "groups": [
                group(1, "A5", 60, [1, 5]),
                group(2, "S5", 120, [1, 5]),
                group(3, "A6", 360, [1, 5]),
                group(4, "S6", 720, [1, 5]),
            ],
        },
        {
            "degree": 5,
            "primitive_group_count": 5,
            "groups": [
                group(1, "C5", 5, [1, 1, 1, 1, 1]),
                group(2, "D10", 10, [1, 2, 2]),
                group(3, "C5 : C4", 20, [1, 4]),
                group(4, "A5", 60, [1, 4]),
                group(5, "S5", 120, [1, 4]),
            ],
        },
    ]


def integer_partitions(total: int, maximum: int | None = None) -> list[tuple[int, ...]]:
    if total == 0:
        return [()]
    bound = total if maximum is None else min(total, maximum)
    output = []
    for first in range(bound, 0, -1):
        for tail in integer_partitions(total - first, first):
            output.append((first, *tail))
    return output


def permutation_from_cycle_type(cycle_type: tuple[int, ...]) -> list[int]:
    degree = sum(cycle_type)
    permutation = list(range(degree))
    offset = 0
    for length in cycle_type:
        cycle = list(range(offset, offset + length))
        offset += length
        for source, target in zip(cycle, cycle[1:] + cycle[:1], strict=True):
            permutation[source] = target
    return permutation


def permutation_index(permutation: list[int]) -> int:
    seen: set[int] = set()
    cycles = 0
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycles += 1
        point = start
        while point not in seen:
            seen.add(point)
            point = permutation[point]
    return len(permutation) - cycles


def induced_two_subset_permutation(permutation: list[int]) -> list[int]:
    subsets = list(itertools.combinations(range(len(permutation)), 2))
    lookup = {subset: index for index, subset in enumerate(subsets)}
    return [
        lookup[tuple(sorted((permutation[first], permutation[second])))]
        for first, second in subsets
    ]


def induced_intersection_one_orbital(permutation: list[int]) -> list[int]:
    subsets = list(itertools.combinations(range(len(permutation)), 2))
    subset_permutation = induced_two_subset_permutation(permutation)
    orbital = [
        (first_index, second_index)
        for first_index, first in enumerate(subsets)
        for second_index, second in enumerate(subsets)
        if len(set(first).intersection(second)) == 1
    ]
    require(len(orbital) == 120, "degree-fifteen r=8 orbital size")
    lookup = {pair: index for index, pair in enumerate(orbital)}
    return [
        lookup[
            (
                subset_permutation[first_index],
                subset_permutation[second_index],
            )
        ]
        for first_index, second_index in orbital
    ]


def m4_branch_cycle_ledger() -> dict[str, Any]:
    class_rows = []
    for cycle_type in integer_partitions(6):
        permutation = permutation_from_cycle_type(cycle_type)
        natural_index = permutation_index(permutation)
        point_index = permutation_index(
            induced_two_subset_permutation(permutation)
        )
        orbital_index = permutation_index(
            induced_intersection_one_orbital(permutation)
        )
        class_rows.append(
            {
                "natural_cycle_type": list(cycle_type),
                "natural_sign": -1 if natural_index % 2 else 1,
                "degree_fifteen_index": point_index,
                "r8_orbital_index": orbital_index,
            }
        )

    nonidentity = [
        row for row in class_rows if row["degree_fifteen_index"] > 0
    ]
    pole_index = next(
        index
        for index, row in enumerate(nonidentity)
        if row["natural_cycle_type"] == [5, 1]
    )

    def solutions(allowed_signs: set[int]) -> list[list[int]]:
        output: list[list[int]] = []

        def search(
            position: int,
            point_remaining: int,
            orbital_remaining: int,
            counts: list[int],
        ) -> None:
            if position == len(nonidentity):
                if (
                    point_remaining == 0
                    and orbital_remaining == 0
                    and counts[pole_index] >= 1
                ):
                    output.append(counts)
                return
            row = nonidentity[position]
            if row["natural_sign"] not in allowed_signs:
                search(
                    position + 1,
                    point_remaining,
                    orbital_remaining,
                    [*counts, 0],
                )
                return
            point_index = row["degree_fifteen_index"]
            orbital_index = row["r8_orbital_index"]
            maximum = min(
                point_remaining // point_index,
                orbital_remaining // orbital_index,
            )
            for count in range(maximum + 1):
                search(
                    position + 1,
                    point_remaining - count * point_index,
                    orbital_remaining - count * orbital_index,
                    [*counts, count],
                )

        for genus in range(3):
            search(0, 28, 2 * 120 - 2 + 2 * genus, [])
        return output

    a6_solutions = solutions({1})
    s6_solutions = solutions({-1, 1})
    require(a6_solutions == [], "A6 m4 branch ledger")
    require(len(s6_solutions) == 1, "S6 m4 branch ledger count")
    unique = s6_solutions[0]
    unique_rows = [
        {
            "natural_cycle_type": nonidentity[index]["natural_cycle_type"],
            "count": count,
        }
        for index, count in enumerate(unique)
        if count
    ]
    unique_sign = math.prod(
        row["natural_sign"] ** count
        for row, count in zip(nonidentity, unique, strict=True)
    )
    require(
        unique_rows
        == [
            {"natural_cycle_type": [5, 1], "count": 2},
            {"natural_cycle_type": [2, 1, 1, 1, 1], "count": 1},
        ],
        "S6 unique class multiset",
    )
    require(unique_sign == -1, "S6 unique product sign")
    return {
        "inner_degree": 4,
        "outer_degree": 15,
        "candidate_r": 8,
        "delta": 2,
        "outer_group_candidates": ["A6", "S6"],
        "outer_pole_cycle_type": [5, 5, 5],
        "underlying_natural_pole_cycle_type": [5, 1],
        "degree_fifteen_total_index": 28,
        "r8_orbital_degree": 120,
        "actual_curve_genus_upper_bound": 3,
        "outer_component_genus_upper_bound": 2,
        "allowed_r8_total_indices": [238, 240, 242],
        "class_index_table": class_rows,
        "A6_necessary_class_multisets": a6_solutions,
        "S6_necessary_class_multisets": [unique_rows],
        "S6_unique_multiset_product_sign": unique_sign,
        "S6_product_one_possible": False,
        "terminal": "M4_R8_PRIMITIVE_OUTER_BRANCH_CYCLE_CONTRADICTION",
    }


def permutation_from_cycles(
    degree: int, cycles: list[list[int]]
) -> list[int]:
    permutation = list(range(degree))
    support: set[int] = set()
    for cycle in cycles:
        require(len(cycle) >= 2, "witness cycle length")
        zero_based = [entry - 1 for entry in cycle]
        require(
            all(0 <= entry < degree for entry in zero_based),
            "witness cycle support",
        )
        require(
            not support.intersection(zero_based),
            "overlapping witness cycles",
        )
        support.update(zero_based)
        for source, target in zip(
            zero_based, zero_based[1:] + zero_based[:1], strict=True
        ):
            permutation[source] = target
    return permutation


def permutation_cycle_type(permutation: list[int]) -> list[int]:
    seen: set[int] = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        length = 0
        point = start
        while point not in seen:
            seen.add(point)
            length += 1
            point = permutation[point]
        lengths.append(length)
    return sorted(lengths, reverse=True)


def compose_permutations(
    left: list[int], right: list[int]
) -> list[int]:
    """Return left after right."""

    require(len(left) == len(right), "permutation degree mismatch")
    return [left[right[index]] for index in range(len(left))]


def inverse_permutation(permutation: list[int]) -> list[int]:
    inverse = [0] * len(permutation)
    for index, image in enumerate(permutation):
        inverse[image] = index
    return inverse


def generated_group(generators: list[list[int]]) -> list[list[int]]:
    degree = len(generators[0])
    identity = tuple(range(degree))
    moves = generators + [inverse_permutation(item) for item in generators]
    seen = {identity}
    queue = [list(identity)]
    while queue:
        current = queue.pop()
        for move in moves:
            product = compose_permutations(move, current)
            key = tuple(product)
            if key not in seen:
                seen.add(key)
                queue.append(product)
    return [list(item) for item in sorted(seen)]


def orbital_indices(
    group_elements: list[list[int]],
    generators: list[list[int]],
    subdegree: int,
) -> list[int]:
    stabilizer = [
        element for element in group_elements if element[0] == 0
    ]
    candidate_orbits = []
    used: set[int] = {0}
    for point in range(1, len(generators[0])):
        if point in used:
            continue
        orbit = {element[point] for element in stabilizer}
        used.update(orbit)
        candidate_orbits.append(orbit)
    matches = [orbit for orbit in candidate_orbits if len(orbit) == subdegree]
    require(len(matches) == 1, "witness suborbit is not unique")
    representative = min(matches[0])
    orbital = sorted(
        {(element[0], element[representative]) for element in group_elements}
    )
    require(
        len(orbital) == len(generators[0]) * subdegree,
        "witness orbital degree",
    )
    lookup = {pair: index for index, pair in enumerate(orbital)}
    output = []
    for generator in generators:
        induced = [
            lookup[(generator[first], generator[second])]
            for first, second in orbital
        ]
        output.append(permutation_index(induced))
    return output


def witness(
    degree: int,
    cycles: list[list[list[int]]],
    point_cycle_types: list[list[int]],
    expected_group_order: int,
    subdegree: int,
    component_indices: list[int],
) -> dict[str, Any]:
    require(len(cycles) == 3, "three-branch witness")
    generators = [
        permutation_from_cycles(degree, generator_cycles)
        for generator_cycles in cycles
    ]
    identity = list(range(degree))
    product = identity
    for generator in generators:
        product = compose_permutations(generator, product)
    require(product == identity, "branch witness product one")
    require(
        [permutation_cycle_type(item) for item in generators]
        == point_cycle_types,
        "branch witness point passport",
    )
    group_elements = generated_group(generators)
    require(
        len(group_elements) == expected_group_order,
        "branch witness generated group order",
    )
    require(
        orbital_indices(group_elements, generators, subdegree)
        == component_indices,
        "branch witness component indices",
    )
    component_degree = degree * subdegree
    genus_numerator = (
        sum(component_indices) - (2 * component_degree - 2)
    )
    require(genus_numerator in {0, 2}, "component genus bound")
    return {
        "generators_in_point_action_cycles": cycles,
        "generated_group_order": len(group_elements),
        "product_one": True,
        "point_cycle_types": point_cycle_types,
        "point_indices": [
            permutation_index(item) for item in generators
        ],
        "component_indices": component_indices,
        "component_genus": genus_numerator // 2,
    }


def nielsen_profile(
    *,
    m: int,
    outer_degree: int,
    subdegree: int,
    group_index: int,
    group_structure: str,
    group_order: int,
    gap_class_indices: list[int],
    point_cycle_types: list[list[int]],
    component_indices: list[int],
    witness_cycles: list[list[list[list[int]]]],
) -> dict[str, Any]:
    records = [
        witness(
            outer_degree,
            cycles,
            point_cycle_types,
            group_order,
            subdegree,
            component_indices,
        )
        for cycles in witness_cycles
    ]
    point_indices = records[0]["point_indices"]
    require(
        sum(point_indices) == 2 * outer_degree - 2,
        "point-cover genus zero",
    )
    require(
        all(record["point_indices"] == point_indices for record in records),
        "Nielsen witness point-index drift",
    )
    require(
        all(
            record["component_genus"] == records[0]["component_genus"]
            for record in records
        ),
        "Nielsen witness component-genus drift",
    )
    return {
        "m": m,
        "outer_degree": outer_degree,
        "subdegree": subdegree,
        "primitive_group_index": group_index,
        "structure": group_structure,
        "group_order": group_order,
        "gap_conjugacy_class_indices": gap_class_indices,
        "point_cycle_types": point_cycle_types,
        "point_indices": point_indices,
        "component_degree": outer_degree * subdegree,
        "component_indices": component_indices,
        "component_genus": records[0]["component_genus"],
        "simultaneous_conjugacy_orbit_count": len(records),
        "orbit_witnesses": records,
    }


def primitive_survivor_nielsen_ledger() -> dict[str, Any]:
    m6_profiles = [
        nielsen_profile(
            m=6,
            outer_degree=10,
            subdegree=r,
            group_index=1,
            group_structure="A5",
            group_order=60,
            gap_class_indices=[pole_class, 2, 3],
            point_cycle_types=[
                [5, 5],
                [3, 3, 3, 1],
                [2, 2, 2, 2, 1, 1],
            ],
            component_indices=indices,
            witness_cycles=[cycles],
        )
        for r, indices in [(3, [24, 20, 14]), (6, [48, 40, 30])]
        for pole_class, cycles in [
            (
                4,
                [
                    [[1, 2, 8, 10, 7], [3, 9, 6, 4, 5]],
                    [[1, 7, 6], [2, 9, 8], [3, 4, 10]],
                    [[1, 9], [3, 8], [4, 5], [6, 10]],
                ],
            ),
            (
                5,
                [
                    [[1, 2, 9, 10, 6], [3, 5, 4, 8, 7]],
                    [[1, 6, 5], [2, 3, 8], [4, 10, 9]],
                    [[1, 3], [2, 4], [5, 10], [7, 8]],
                ],
            ),
        ]
    ]
    m6_profiles.extend(
        [
            nielsen_profile(
                m=6,
                outer_degree=10,
                subdegree=3,
                group_index=2,
                group_structure="S5",
                group_order=120,
                gap_class_indices=[7, 2, 5],
                point_cycle_types=[
                    [5, 5],
                    [2, 2, 2, 1, 1, 1, 1],
                    [6, 3, 1],
                ],
                component_indices=[24, 12, 24],
                witness_cycles=[
                    [
                        [[1, 2, 8, 10, 7], [3, 9, 6, 4, 5]],
                        [[1, 7], [2, 9], [3, 10]],
                        [[1, 10, 5, 4, 6, 9], [2, 3, 8]],
                    ]
                ],
            ),
            nielsen_profile(
                m=6,
                outer_degree=10,
                subdegree=3,
                group_index=2,
                group_structure="S5",
                group_order=120,
                gap_class_indices=[7, 2, 6],
                point_cycle_types=[
                    [5, 5],
                    [2, 2, 2, 1, 1, 1, 1],
                    [4, 4, 2],
                ],
                component_indices=[24, 12, 22],
                witness_cycles=[
                    [
                        [[1, 2, 8, 10, 7], [3, 9, 6, 4, 5]],
                        [[3, 4], [6, 7], [8, 9]],
                        [[1, 7, 9, 2], [3, 6, 10, 8], [4, 5]],
                    ]
                ],
            ),
            nielsen_profile(
                m=6,
                outer_degree=10,
                subdegree=6,
                group_index=2,
                group_structure="S5",
                group_order=120,
                gap_class_indices=[7, 2, 6],
                point_cycle_types=[
                    [5, 5],
                    [2, 2, 2, 1, 1, 1, 1],
                    [4, 4, 2],
                ],
                component_indices=[48, 27, 45],
                witness_cycles=[
                    [
                        [[1, 2, 8, 10, 7], [3, 9, 6, 4, 5]],
                        [[3, 4], [6, 7], [8, 9]],
                        [[1, 7, 9, 2], [3, 6, 10, 8], [4, 5]],
                    ]
                ],
            ),
        ]
    )

    m10_profiles = [
        nielsen_profile(
            m=10,
            outer_degree=6,
            subdegree=5,
            group_index=1,
            group_structure="A5",
            group_order=60,
            gap_class_indices=[pole_class, 2, 5],
            point_cycle_types=[
                [5, 1],
                [2, 2, 1, 1],
                [3, 3],
            ],
            component_indices=[24, 14, 20],
            witness_cycles=[cycles],
        )
        for pole_class, cycles in [
            (
                3,
                [
                    [[2, 3, 4, 6, 5]],
                    [[1, 6], [4, 5]],
                    [[1, 4, 6], [2, 5, 3]],
                ],
            ),
            (
                4,
                [
                    [[2, 4, 5, 3, 6]],
                    [[1, 3], [5, 6]],
                    [[1, 5, 3], [2, 6, 4]],
                ],
            ),
        ]
    ]
    m10_profiles.extend(
        [
            nielsen_profile(
                m=10,
                outer_degree=6,
                subdegree=5,
                group_index=2,
                group_structure="S5",
                group_order=120,
                gap_class_indices=[4, 2, 5],
                point_cycle_types=[
                    [5, 1],
                    [4, 1, 1],
                    [2, 2, 2],
                ],
                component_indices=[24, 21, 15],
                witness_cycles=[
                    [
                        [[2, 3, 4, 6, 5]],
                        [[1, 4, 2, 6]],
                        [[1, 4], [2, 3], [5, 6]],
                    ]
                ],
            ),
            nielsen_profile(
                m=10,
                outer_degree=6,
                subdegree=5,
                group_index=3,
                group_structure="A6",
                group_order=360,
                gap_class_indices=[6, 2, 5],
                point_cycle_types=[
                    [5, 1],
                    [2, 2, 1, 1],
                    [4, 2],
                ],
                component_indices=[24, 14, 22],
                witness_cycles=[
                    [
                        [[1, 2, 3, 4, 5]],
                        [[1, 3], [4, 6]],
                        [[1, 2], [3, 5, 4, 6]],
                    ],
                    [
                        [[2, 3, 4, 6, 5]],
                        [[1, 2], [3, 6]],
                        [[1, 5, 6, 2], [3, 4]],
                    ],
                ],
            ),
            nielsen_profile(
                m=10,
                outer_degree=6,
                subdegree=5,
                group_index=3,
                group_structure="A6",
                group_order=360,
                gap_class_indices=[6, 3, 4],
                point_cycle_types=[
                    [5, 1],
                    [3, 1, 1, 1],
                    [3, 3],
                ],
                component_indices=[24, 16, 20],
                witness_cycles=[
                    [
                        [[1, 2, 3, 4, 5]],
                        [[1, 3, 6]],
                        [[1, 6, 2], [3, 5, 4]],
                    ]
                ],
            ),
            nielsen_profile(
                m=10,
                outer_degree=6,
                subdegree=5,
                group_index=3,
                group_structure="A6",
                group_order=360,
                gap_class_indices=[7, 2, 5],
                point_cycle_types=[
                    [5, 1],
                    [2, 2, 1, 1],
                    [4, 2],
                ],
                component_indices=[24, 14, 22],
                witness_cycles=[
                    [
                        [[1, 2, 3, 4, 6]],
                        [[1, 3], [4, 5]],
                        [[1, 2], [3, 6, 4, 5]],
                    ],
                    [
                        [[2, 3, 4, 5, 6]],
                        [[1, 2], [3, 5]],
                        [[1, 6, 5, 2], [3, 4]],
                    ],
                ],
            ),
            nielsen_profile(
                m=10,
                outer_degree=6,
                subdegree=5,
                group_index=3,
                group_structure="A6",
                group_order=360,
                gap_class_indices=[7, 3, 4],
                point_cycle_types=[
                    [5, 1],
                    [3, 1, 1, 1],
                    [3, 3],
                ],
                component_indices=[24, 16, 20],
                witness_cycles=[
                    [
                        [[1, 2, 3, 4, 6]],
                        [[1, 3, 5]],
                        [[1, 5, 2], [3, 6, 4]],
                    ]
                ],
            ),
            nielsen_profile(
                m=10,
                outer_degree=6,
                subdegree=5,
                group_index=4,
                group_structure="S6",
                group_order=720,
                gap_class_indices=[10, 2, 11],
                point_cycle_types=[
                    [5, 1],
                    [2, 1, 1, 1, 1],
                    [6],
                ],
                component_indices=[24, 9, 25],
                witness_cycles=[
                    [
                        [[1, 2, 3, 4, 5]],
                        [[1, 6]],
                        [[1, 6, 5, 4, 3, 2]],
                    ]
                ],
            ),
            nielsen_profile(
                m=10,
                outer_degree=6,
                subdegree=5,
                group_index=4,
                group_structure="S6",
                group_order=720,
                gap_class_indices=[10, 4, 6],
                point_cycle_types=[
                    [5, 1],
                    [2, 2, 2],
                    [3, 2, 1],
                ],
                component_indices=[24, 15, 21],
                witness_cycles=[
                    [
                        [[1, 2, 3, 4, 5]],
                        [[1, 2], [3, 5], [4, 6]],
                        [[2, 5], [3, 4, 6]],
                    ]
                ],
            ),
        ]
    )

    require(len(m6_profiles) == 7, "m6 Nielsen passport count")
    require(len(m10_profiles) == 9, "m10 Nielsen passport count")
    require(
        sum(
            row["simultaneous_conjugacy_orbit_count"]
            for row in m6_profiles + m10_profiles
        )
        == 18,
        "Nielsen orbit count",
    )
    return {
        "scope": (
            "primitive-compatible m=6 and m=10 rows after the exact "
            "outer-subdegree route compiler"
        ),
        "genus_input": (
            "g(Gamma)<=3 and delta>=4 force component genus at most one"
        ),
        "exhaustive_method": (
            "enumerate every nonidentity primitive-group conjugacy class; "
            "impose point-index sum 2*n-2, the required pole class, and "
            "component genus at most one; then enumerate every product-one "
            "generating tuple and quotient by simultaneous conjugacy"
        ),
        "all_survivors_have_three_branch_values": True,
        "m6_passports": m6_profiles,
        "m10_passports": m10_profiles,
        "passport_count": len(m6_profiles) + len(m10_profiles),
        "simultaneous_conjugacy_orbit_count": sum(
            row["simultaneous_conjugacy_orbit_count"]
            for row in m6_profiles + m10_profiles
        ),
        "terminal": "FINITE_PRIMITIVE_NIELSEN_TARGETS_UNPAID",
    }


def proper_divisors(value: int) -> list[int]:
    return [
        divisor
        for divisor in range(2, value)
        if value % divisor == 0
    ]


def route_table() -> list[dict[str, Any]]:
    rows = []
    for m in sorted(TERMINAL_INNER_DEGREES):
        n = 60 // m
        targets = []
        for right_degree in proper_divisors(n):
            new_inner = m * right_degree
            admitted = new_inner in ALLOWED_SOURCE_INNER_DEGREES
            field_compatible = not (m == 6 and right_degree == 5)
            if not admitted:
                terminal = "SOURCE_PROFILE_IMPOSSIBLE"
            elif not field_compatible:
                terminal = "M6_DEGREE5_OUTER_RIGHT_FACTOR_DELETED"
            elif new_inner == 30:
                terminal = "M30_REFINES_TO_M6"
            else:
                terminal = f"REENTER_INNER_DEGREE_{new_inner}"
            targets.append(
                {
                    "outer_right_degree": right_degree,
                    "new_inner_degree": new_inner,
                    "source_profile_admitted": admitted,
                    "field_compatible": field_compatible,
                    "terminal": terminal,
                }
            )
        rows.append(
            {
                "from_inner_degree": m,
                "outer_degree": n,
                "proper_outer_right_degrees": proper_divisors(n),
                "targets": targets,
            }
        )
    return rows


def flatten_parent_rows(source: dict[str, Any]) -> list[dict[str, int]]:
    output = []
    for row in source["transverse_outer_terminal"]["rows"]:
        m = int(row["m"])
        n = int(row["n"])
        for r, delta in row["r_delta"]:
            require(delta * r == 4 * m, "parent degree identity")
            require(delta <= m * m, "parent cover bound")
            require(r <= n - 1, "parent outer degree bound")
            output.append({"m": m, "n": n, "r": r, "delta": delta})
    return output


def decomposition_analysis(
    row: dict[str, int],
    target_rows: list[dict[str, int]],
) -> list[dict[str, Any]]:
    """Enumerate every proper outer right degree and its geometric exits."""

    rows_by_inner: dict[int, list[int]] = {}
    for candidate in target_rows:
        rows_by_inner.setdefault(candidate["m"], []).append(candidate["r"])
    # The m=30 source profile has outer degree two and is immediately refined
    # back to m=6 by the parent fifth-power extraction.
    rows_by_inner[30] = [1]

    output = []
    for right_degree in proper_divisors(row["n"]):
        new_inner = row["m"] * right_degree
        admitted = new_inner in ALLOWED_SOURCE_INNER_DEGREES
        field_obstruction = None
        if row["m"] == 6 and right_degree == 5:
            field_obstruction = (
                "M6_DEGREE5_OUTER_RIGHT_FACTOR_FIFTH_POWER_"
                "SPLIT_FIBER_CONTRADICTION"
            )
        same_fiber_possible = (
            admitted
            and field_obstruction is None
            and row["r"] <= right_degree - 1
        )
        transverse = []
        if admitted and field_obstruction is None:
            for image_r in sorted(set(rows_by_inner.get(new_inner, []))):
                numerator = right_degree * row["r"]
                if numerator % image_r != 0:
                    continue
                cover_degree = numerator // image_r
                if cover_degree <= right_degree * right_degree:
                    transverse.append(
                        {
                            "image_inner_degree": new_inner,
                            "image_r": image_r,
                            "cover_degree": cover_degree,
                            "degree_identity": (
                                f"{cover_degree}*{image_r}="
                                f"{right_degree}*{row['r']}"
                            ),
                        }
                    )
        output.append(
            {
                "outer_right_degree": right_degree,
                "new_inner_degree": new_inner,
                "source_profile_admitted": admitted,
                "field_obstruction": field_obstruction,
                "same_right_fiber_possible": same_fiber_possible,
                "transverse_image_targets": transverse,
                "viable": same_fiber_possible or bool(transverse),
            }
        )
    return output


def classify_rows(
    source: dict[str, Any],
    m12_cut: dict[str, Any],
    m12_normal: dict[str, Any],
    catalogue: list[dict[str, Any]],
    m4_ledger: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, int]]]:
    all_rows = flatten_parent_rows(source)
    deleted_pairs = {
        (12, int(row["r"]), int(row["delta"]))
        for row in m12_cut["conclusion"]["deleted_degree_twelve_rows"]
    }
    require(
        deleted_pairs == {(12, 1, 48), (12, 3, 16)},
        "m12 deleted rows",
    )
    catalogue_by_degree = {row["degree"]: row for row in catalogue}
    # The m=10,r=4 contradiction below is proved directly from its only
    # possible right-factor degrees, so it cannot be revived as the image of
    # a finer decomposition.
    target_rows = [
        row
        for row in all_rows
        if (row["m"], row["r"], row["delta"]) not in deleted_pairs
        and (row["m"], row["r"], row["delta"]) != (10, 4, 10)
    ]
    classified = []
    deleted = []

    for row in all_rows:
        key = (row["m"], row["r"], row["delta"])
        if key in deleted_pairs:
            deleted.append(dict(row))
            continue
        degree_catalogue = catalogue_by_degree[row["n"]]
        matches = [
            {
                "primitive_group_index": record["primitive_group_index"],
                "structure": record["structure"],
                "order": record["order"],
            }
            for record in degree_catalogue["groups"]
            if row["r"] in record["non_diagonal_subdegrees"]
        ]
        filtered_matches = list(matches)
        profile_filter = None
        if row["m"] == 4 and row["r"] == 8:
            require(
                m4_ledger["terminal"]
                == "M4_R8_PRIMITIVE_OUTER_BRANCH_CYCLE_CONTRADICTION",
                "m4 branch-cycle terminal",
            )
            filtered_matches = []
            profile_filter = (
                "M4_R8_PRIMITIVE_OUTER_BRANCH_CYCLE_CONTRADICTION"
            )
        if row["m"] == 12 and row["r"] == 4:
            require(
                m12_normal["branch_cycle_ledger"]["AGL_1_5_occurs"] is False,
                "m12 AGL profile filter",
            )
            filtered_matches = [
                match
                for match in matches
                if match["structure"] in {"A5", "S5"}
            ]
            profile_filter = "M12_TAME_POLYNOMIAL_BRANCH_LEDGER_EXCLUDES_F20"
        decomposition = decomposition_analysis(row, target_rows)
        decomposable_realization_possible = any(
            branch["viable"] for branch in decomposition
        )
        if filtered_matches:
            terminal = "PRIMITIVE_OUTER_COMPATIBLE_SURVIVOR"
        elif decomposable_realization_possible:
            terminal = "FORCED_STRICT_OUTER_DECOMPOSITION"
        else:
            terminal = "ACTUAL_PRODUCER_CONTRADICTION"
        classified.append(
            {
                **row,
                "raw_primitive_matches": matches,
                "profile_filter": profile_filter,
                "primitive_matches": filtered_matches,
                "decomposition_analysis": decomposition,
                "decomposable_realization_possible": (
                    decomposable_realization_possible
                ),
                "outer_primitivity_forced": (
                    bool(filtered_matches)
                    and not decomposable_realization_possible
                ),
                "terminal": terminal,
            }
        )
    return classified, deleted


def build_payload() -> dict[str, Any]:
    source, m12_cut, m12_normal = parent_packets()
    catalogue = primitive_catalogue()
    m4_ledger = m4_branch_cycle_ledger()
    nielsen_ledger = primitive_survivor_nielsen_ledger()
    rows, deleted = classify_rows(
        source, m12_cut, m12_normal, catalogue, m4_ledger
    )
    forced = [
        row
        for row in rows
        if row["terminal"] == "FORCED_STRICT_OUTER_DECOMPOSITION"
    ]
    contradictions = [
        row
        for row in rows
        if row["terminal"] == "ACTUAL_PRODUCER_CONTRADICTION"
    ]
    survivors = [
        row
        for row in rows
        if row["terminal"] == "PRIMITIVE_OUTER_COMPATIBLE_SURVIVOR"
    ]
    require(len(flatten_parent_rows(source)) == 26, "original row count")
    require(len(deleted) == 2, "parent deletion count")
    require(len(rows) == 24, "live row count")
    require(len(forced) == 18, "forced decomposition count")
    require(len(contradictions) == 1, "new contradiction count")
    require(
        [(row["m"], row["r"], row["delta"]) for row in contradictions]
        == [(10, 4, 10)],
        "new contradiction row",
    )
    require(len(survivors) == 5, "primitive survivor count")
    require(
        [(row["m"], row["r"], row["delta"]) for row in survivors]
        == [
            (6, 3, 8),
            (6, 6, 4),
            (10, 5, 8),
            (12, 2, 24),
            (12, 4, 12),
        ],
        "primitive survivor rows",
    )

    data: dict[str, Any] = {
        "schema": "kb-mca-v4-degree60-outer-primitive-route-compiler-v1",
        "statement": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "object": "MCA",
            "agreement": 1_116_048,
            "B_star": "274980728111395087",
            "endpoint_degree": 60,
            "component_u": 2,
            "status": (
                "PROVED_OUTER_PRIMITIVE_ROUTE_AND_LOW_GENUS_NIELSEN_"
                "COMPILER_ROW_OPEN"
            ),
            "ledger_movement": 0,
        },
        "parent_stack": {
            "head_commit": M12_NORMAL_COMMIT,
            "source_compiler": {
                "commit": SOURCE_COMMIT,
                "path": str(SOURCE_CERTIFICATE.relative_to(ROOT)),
                "blob_oid": SOURCE_BLOB,
                "payload_sha256": SOURCE_PAYLOAD,
                "imported_transverse_type_count": 26,
            },
            "m12_subdegree_cut": {
                "commit": M12_CUT_COMMIT,
                "path": str(M12_CUT_CERTIFICATE.relative_to(ROOT)),
                "blob_oid": M12_CUT_BLOB,
                "payload_sha256": M12_CUT_PAYLOAD,
                "deleted_types": [[12, 1, 48], [12, 3, 16]],
            },
            "m12_normal_forms": {
                "commit": M12_NORMAL_COMMIT,
                "path": str(M12_NORMAL_CERTIFICATE.relative_to(ROOT)),
                "blob_oid": M12_NORMAL_BLOB,
                "payload_sha256": M12_NORMAL_PAYLOAD,
                "imported_terminal": "M12_SIX_GEOMETRIC_OUTER_FAMILIES_UNPAID",
            },
        },
        "independent_replays": {
            "sage_gap": {
                "path": str(SAGE_REPLAY.relative_to(ROOT.parent)),
                "sha256": file_sha256(SAGE_REPLAY),
                "sage_version": "10.9",
                "gap_version": "4.14.0",
                "exact_primitive_group_count": 32,
                "necessary_low_genus_class_profile_count": 25,
                "generating_nielsen_passport_count": 16,
                "simultaneous_conjugacy_orbit_count": 18,
            },
            "wolfram": {
                "path": str(WOLFRAM_REPLAY.relative_to(ROOT.parent)),
                "sha256": file_sha256(WOLFRAM_REPLAY),
                "scope": (
                    "independent exact integer, permutation-index, genus, "
                    "field, and route arithmetic"
                ),
            },
            "live_wolfram_plugin": {
                "partition_identity": "26-2=18+1+5",
                "field_residues_and_gcd": [3, 4, 1],
                "m10_r4_three_exits_impossible": [True, True, True],
                "m4_A6_multiset_count": 0,
                "m4_S6_multiset_count": 1,
                "m4_S6_unique_product_sign": -1,
                "m6_component_genera": [0, 0, 0, 0, 1, 0, 1],
                "m10_component_genera": [0, 0, 1, 1, 1, 1, 1, 0, 1],
            },
        },
        "primitive_outer_lemma": {
            "hypothesis": (
                "F is geometrically indecomposable of degree n and C is a "
                "geometrically irreducible non-diagonal component of "
                "F(Y)=F(Z)"
            ),
            "conclusion": (
                "geometric monodromy is primitive of degree n and the "
                "bidegree r of C is a non-diagonal point-stabilizer subdegree"
            ),
            "contrapositive_terminal": "FORCED_STRICT_OUTER_DECOMPOSITION",
        },
        "decomposed_outer_component_lemma": {
            "setup": (
                "F=G composed s with e=deg(s); C has bidegree (r,r); "
                "Cprime is the image under s times s"
            ),
            "same_fiber_bound": (
                "if Cprime is diagonal then C is a same-s-fiber component "
                "and r<=e-1"
            ),
            "transverse_degree_identity": "epsilon*rprime=e*r",
            "cover_bound": "epsilon<=e^2",
            "source_profile_gate": (
                "the coarsened inner degree m*e must occur in the exhaustive "
                "source-profile table"
            ),
            "new_empty_row": {
                "m": 10,
                "n": 6,
                "r": 4,
                "delta": 10,
                "right_degree_two": "mprime=20 is source-profile impossible",
                "right_degree_three_same_fiber": "r=4>e-1=2",
                "right_degree_three_transverse": (
                    "G has degree two, so rprime=1 and epsilon=e*r=12>e^2=9"
                ),
                "terminal": "ACTUAL_PRODUCER_CONTRADICTION",
            },
        },
        "m6_degree_five_outer_right_factor_exclusion": {
            "setup": "m=6, deg(F)=10, F=G_2 composed s_5",
            "outer_poles": (
                "two K-rational poles of F, each of order five"
            ),
            "outer_zeros": (
                "ten distinct simple K-rational zeros of F"
            ),
            "pole_consequence": (
                "G_2 has two simple poles and s_5 is totally ramified "
                "above each"
            ),
            "coordinate_scope": (
                "the source coordinate z=H0/H1 is K-rational; only a "
                "geometric target normalization of s_5 is used"
            ),
            "normal_form": (
                "c*z^5 after the K-rational source coordinate and a "
                "geometric target change"
            ),
            "field_arithmetic": {
                "p": 2_130_706_433,
                "extension_degree": 6,
                "gcd_5_q_minus_1": 1,
                "fifth_power_permutates_K": True,
            },
            "contradiction": (
                "a split simple five-point K-fiber of s_5 is impossible"
            ),
            "terminal": "M6_DEGREE5_OUTER_RIGHT_FACTOR_DELETED",
        },
        "primitive_outer_catalogue": catalogue,
        "m4_r8_primitive_branch_cycle_exclusion": m4_ledger,
        "primitive_survivor_low_genus_nielsen_ledger": nielsen_ledger,
        "parent_deleted_rows": deleted,
        "live_row_classification": rows,
        "strict_outer_decomposition_routes": route_table(),
        "route_graph": {
            "admitted_edges": [
                [2, 4],
                [2, 6],
                [2, 10],
                [2, 12],
                [2, 30],
                [3, 6],
                [3, 12],
                [3, 30],
                [4, 12],
                [6, 12],
                [10, 30],
                [30, 6],
            ],
            "source_profile_impossible_targets": [[2, 20], [3, 15], [4, 20], [10, 20]],
            "field_deleted_edges": [[6, 30]],
            "nontrivial_strongly_connected_components": [],
            "route_graph_acyclic": True,
            "deleted_loop_terminal": "M6_DEGREE5_OUTER_RIGHT_FACTOR_DELETED",
        },
        "conclusion": {
            "original_transverse_type_count": 26,
            "parent_deleted_type_count": 2,
            "live_input_type_count": 24,
            "forced_strict_outer_decomposition_type_count": 18,
            "new_actual_producer_contradiction_type_count": 1,
            "new_actual_producer_contradiction": [10, 4, 10],
            "primitive_outer_survivor_type_count": 5,
            "primitive_outer_survivors": [
                [row["m"], row["r"], row["delta"]] for row in survivors
            ],
            "new_m6_m10_nielsen_passport_count": (
                nielsen_ledger["passport_count"]
            ),
            "new_m6_m10_simultaneous_conjugacy_orbit_count": (
                nielsen_ledger["simultaneous_conjugacy_orbit_count"]
            ),
            "m12_imported_geometric_family_count": 6,
            "terminal": (
                "ONE_NEW_EMPTY_EIGHTEEN_ACYCLIC_DECOMPOSITION_ROUTES_"
                "AND_FIVE_FINITE_PRIMITIVE_TARGETS"
            ),
            "m12_closed": False,
            "u2_closed": False,
            "K3_closed": False,
            "row_closed": False,
            "ledger_movement": 0,
        },
        "nonclaims": [
            "A forced outer decomposition is a recursive route, not a payment.",
            "The former m=6 to m=30 to m=6 loop is deleted by the exact split-fiber fifth-power contradiction.",
            "The m=4,r=8 primitive realization is empty, but the row itself routes through outer decomposition.",
            "No primitive survivor is deleted or assigned to an owner.",
            "The Nielsen passports and generating tuples do not prove a challenge-field normal form or source compatibility.",
            "No parameter-to-carrier, received-data, explaining-polynomial, or slope bridge is proved.",
            "No u=2, K3, or KoalaBear row closure is claimed.",
            "No ledger quantity moves.",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def validate(data: dict[str, Any]) -> dict[str, Any]:
    expected = build_payload()
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    require(data == expected, "certificate differs from exact reconstruction")
    conclusion = data["conclusion"]
    require(
        conclusion["live_input_type_count"]
        == conclusion["forced_strict_outer_decomposition_type_count"]
        + conclusion["new_actual_producer_contradiction_type_count"]
        + conclusion["primitive_outer_survivor_type_count"],
        "live partition count",
    )
    require(
        data["route_graph"]["nontrivial_strongly_connected_components"]
        == [],
        "route SCC",
    )
    require(data["route_graph"]["route_graph_acyclic"] is True, "route DAG")
    require(conclusion["ledger_movement"] == 0, "ledger movement")
    return {
        "original": conclusion["original_transverse_type_count"],
        "deleted": conclusion["parent_deleted_type_count"],
        "live": conclusion["live_input_type_count"],
        "forced": conclusion["forced_strict_outer_decomposition_type_count"],
        "contradictions": conclusion[
            "new_actual_producer_contradiction_type_count"
        ],
        "survivors": conclusion["primitive_outer_survivor_type_count"],
        "loop": data["route_graph"]["deleted_loop_terminal"],
        "payload": data["payload_sha256"],
    }


def mutate_path(
    data: dict[str, Any], path: tuple[object, ...], value: object
) -> dict[str, Any]:
    output = copy.deepcopy(data)
    target: Any = output
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    output["payload_sha256"] = payload_hash(output)
    return output


def tamper_selftest(data: dict[str, Any]) -> tuple[int, int]:
    mutations: list[tuple[str, tuple[object, ...], object]] = [
        ("status", ("statement", "status"), "SAFE"),
        ("agreement", ("statement", "agreement"), 1_116_047),
        ("budget", ("statement", "B_star"), "274980728111395086"),
        ("source-commit", ("parent_stack", "source_compiler", "commit"), "0" * 40),
        ("source-blob", ("parent_stack", "source_compiler", "blob_oid"), "0" * 40),
        (
            "source-payload",
            ("parent_stack", "source_compiler", "payload_sha256"),
            "0" * 64,
        ),
        ("m12-cut", ("parent_stack", "m12_subdegree_cut", "commit"), "0" * 40),
        (
            "m12-normal",
            ("parent_stack", "m12_normal_forms", "payload_sha256"),
            "0" * 64,
        ),
        (
            "sage-replay-hash",
            ("independent_replays", "sage_gap", "sha256"),
            "0" * 64,
        ),
        (
            "wolfram-replay-hash",
            ("independent_replays", "wolfram", "sha256"),
            "0" * 64,
        ),
        (
            "live-wolfram-gcd",
            (
                "independent_replays",
                "live_wolfram_plugin",
                "field_residues_and_gcd",
                2,
            ),
            5,
        ),
        (
            "lemma",
            ("primitive_outer_lemma", "contrapositive_terminal"),
            "PRIMITIVE_SURVIVOR",
        ),
        (
            "decomposed-cover-bound",
            ("decomposed_outer_component_lemma", "cover_bound"),
            "epsilon<=e",
        ),
        (
            "m6-field-gcd",
            (
                "m6_degree_five_outer_right_factor_exclusion",
                "field_arithmetic",
                "gcd_5_q_minus_1",
            ),
            5,
        ),
        (
            "catalogue-count",
            ("primitive_outer_catalogue", 2, "primitive_group_count"),
            5,
        ),
        (
            "catalogue-order",
            ("primitive_outer_catalogue", 2, "groups", 1, "order"),
            361,
        ),
        (
            "catalogue-subdegree",
            (
                "primitive_outer_catalogue",
                3,
                "groups",
                0,
                "non_diagonal_subdegrees",
                0,
            ),
            4,
        ),
        (
            "m4-orbital-index",
            (
                "m4_r8_primitive_branch_cycle_exclusion",
                "class_index_table",
                1,
                "r8_orbital_index",
            ),
            95,
        ),
        (
            "m4-product-sign",
            (
                "m4_r8_primitive_branch_cycle_exclusion",
                "S6_unique_multiset_product_sign",
            ),
            1,
        ),
        (
            "nielsen-passport-count",
            (
                "primitive_survivor_low_genus_nielsen_ledger",
                "passport_count",
            ),
            15,
        ),
        (
            "nielsen-class",
            (
                "primitive_survivor_low_genus_nielsen_ledger",
                "m6_passports",
                0,
                "gap_conjugacy_class_indices",
                0,
            ),
            5,
        ),
        (
            "nielsen-witness",
            (
                "primitive_survivor_low_genus_nielsen_ledger",
                "m6_passports",
                0,
                "orbit_witnesses",
                0,
                "generators_in_point_action_cycles",
                0,
                0,
                0,
            ),
            2,
        ),
        (
            "nielsen-orbit-count",
            (
                "primitive_survivor_low_genus_nielsen_ledger",
                "m10_passports",
                3,
                "simultaneous_conjugacy_orbit_count",
            ),
            1,
        ),
        (
            "nielsen-three-branch",
            (
                "primitive_survivor_low_genus_nielsen_ledger",
                "all_survivors_have_three_branch_values",
            ),
            False,
        ),
        (
            "nielsen-genus",
            (
                "primitive_survivor_low_genus_nielsen_ledger",
                "m10_passports",
                0,
                "component_genus",
            ),
            1,
        ),
        ("deleted-row", ("parent_deleted_rows", 0, "r"), 2),
        ("live-m", ("live_row_classification", 0, "m"), 3),
        ("live-r", ("live_row_classification", 0, "r"), 3),
        ("live-delta", ("live_row_classification", 0, "delta"), 5),
        (
            "live-terminal",
            ("live_row_classification", 0, "terminal"),
            "PRIMITIVE_OUTER_COMPATIBLE_SURVIVOR",
        ),
        (
            "primitive-match",
            (
                "live_row_classification",
                10,
                "primitive_matches",
            ),
            [{"primitive_group_index": 1, "structure": "FAKE", "order": 1}],
        ),
        (
            "profile-filter",
            ("live_row_classification", 23, "profile_filter"),
            None,
        ),
        (
            "decomposition-viability",
            (
                "live_row_classification",
                20,
                "decomposable_realization_possible",
            ),
            True,
        ),
        (
            "new-contradiction",
            ("conclusion", "new_actual_producer_contradiction"),
            [10, 5, 8],
        ),
        (
            "route-degree",
            (
                "strict_outer_decomposition_routes",
                0,
                "proper_outer_right_degrees",
                0,
            ),
            3,
        ),
        (
            "route-target",
            (
                "strict_outer_decomposition_routes",
                3,
                "targets",
                1,
                "new_inner_degree",
            ),
            12,
        ),
        ("route-edge", ("route_graph", "admitted_edges", 0, 1), 5),
        (
            "route-impossible",
            ("route_graph", "source_profile_impossible_targets", 0, 1),
            30,
        ),
        (
            "route-scc",
            ("route_graph", "nontrivial_strongly_connected_components"),
            [[6, 30]],
        ),
        ("route-dag", ("route_graph", "route_graph_acyclic"), False),
        (
            "forced-count",
            ("conclusion", "forced_strict_outer_decomposition_type_count"),
            17,
        ),
        (
            "survivor-count",
            ("conclusion", "primitive_outer_survivor_type_count"),
            7,
        ),
        (
            "survivor-row",
            ("conclusion", "primitive_outer_survivors", 0, 1),
            6,
        ),
        ("row-closure", ("conclusion", "row_closed"), True),
        ("movement", ("conclusion", "ledger_movement"), 1),
        ("nonclaim", ("nonclaims", 0), "Forced decomposition is paid."),
    ]
    passed = 0
    for name, path, value in mutations:
        candidate = mutate_path(data, path, value)
        try:
            validate(candidate)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")

    stale = copy.deepcopy(data)
    stale["statement"]["status"] = "SAFE"
    try:
        validate(stale)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: stale payload")

    duplicate = CERTIFICATE.read_text(encoding="utf-8").replace(
        '"schema":',
        '"schema": "DUPLICATE",\n  "schema":',
        1,
    )
    try:
        json.loads(duplicate, object_pairs_hook=reject_duplicate_keys)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: duplicate JSON key")
    return passed, len(mutations) + 2


def write_certificate() -> None:
    data = build_payload()
    CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
    CERTIFICATE.write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(CERTIFICATE)
    print(data["payload_sha256"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-hash", action="store_true")
    arguments = parser.parse_args()
    require(
        arguments.write
        or arguments.check
        or arguments.tamper_selftest
        or arguments.print_hash,
        "choose an action",
    )
    if arguments.write:
        write_certificate()
    if arguments.check or arguments.tamper_selftest or arguments.print_hash:
        data = load_json(CERTIFICATE)
        if arguments.print_hash:
            print(payload_hash(data))
        if arguments.check:
            result = validate(data)
            print(
                "PASS: original={original}, parent_deleted={deleted}, "
                "live={live}, forced_outer_decomposition={forced}, "
                "new_contradictions={contradictions}, "
                "primitive_survivors={survivors}".format(**result)
            )
            print(f"PASS: loop_terminal={result['loop']}")
            print(f"payload_sha256={result['payload']}")
        if arguments.tamper_selftest:
            passed, total = tamper_selftest(data)
            print(f"PASS: {passed}/{total} tamper mutations rejected")


if __name__ == "__main__":
    main()
