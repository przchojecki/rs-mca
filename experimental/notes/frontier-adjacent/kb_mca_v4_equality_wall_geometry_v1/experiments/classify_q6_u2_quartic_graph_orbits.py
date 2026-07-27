#!/usr/bin/env python3
"""Classify the u=2 simple-vertex quartic cases by pole-graph symmetry."""

from __future__ import annotations
class VerificationError(RuntimeError):
    """Raised when an exact verifier condition fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(str(message))


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )



import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "q6_u2_quartic_graph_orbits.json"
PARTITIONS = ((6,), (4, 2), (3, 3), (2, 2, 2))
LEFT_PAIRS = list(itertools.combinations(range(6), 2))
LEFT_PAIR_INDEX = {
    pair: index for index, pair in enumerate(LEFT_PAIRS)
}


def pole_graph(partition: tuple[int, ...]) -> list[tuple[int, int]]:
    edges: set[tuple[int, int]] = set()
    offset = 0
    for size in partition:
        for index in range(size):
            left = offset + index
            right = offset + index
            previous_right = offset + (index - 1) % size
            edges.add((left, right))
            edges.add((left, previous_right))
        offset += size
    require(
        offset == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:34',
    )
    require(
        len(edges) == 12,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:35',
    )
    require(
        all((sum((left == vertex for left, _ in edges)) == 2 for vertex in range(6))),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:36',
    )
    require(
        all((sum((right == vertex for _, right in edges)) == 2 for vertex in range(6))),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:40',
    )
    return sorted(edges)


def four_cycle_masks(
    partition: tuple[int, ...],
    edges: list[tuple[int, int]],
) -> set[int]:
    edge_index = {edge: index for index, edge in enumerate(edges)}
    masks: set[int] = set()
    offset = 0
    for size in partition:
        component_edges = set()
        for index in range(size):
            left = offset + index
            component_edges.add((left, offset + index))
            component_edges.add(
                (left, offset + (index - 1) % size)
            )
        if size == 2:
            mask = 0
            for edge in component_edges:
                mask |= 1 << edge_index[edge]
            masks.add(mask)
        offset += size
    return masks


def automorphisms(
    edges: list[tuple[int, int]],
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    edge_set = set(edges)
    permutations = list(itertools.permutations(range(6)))
    result = []
    for left_permutation in permutations:
        transformed_left_neighbors = {
            left_permutation[left]: {
                right for candidate, right in edges if candidate == left
            }
            for left in range(6)
        }
        for right_permutation in permutations:
            valid = True
            for left in range(6):
                mapped_left = left_permutation[left]
                mapped_neighbors = {
                    right_permutation[right]
                    for candidate, right in edges
                    if candidate == left
                }
                target_neighbors = {
                    right
                    for candidate, right in edge_set
                    if candidate == mapped_left
                }
                if mapped_neighbors != target_neighbors:
                    valid = False
                    break
            if valid:
                result.append((left_permutation, right_permutation))
    require(
        result,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:103',
    )
    return result


def connected_components(graph_mask: int) -> int:
    adjacency = [set() for _ in range(6)]
    for index, (left, right) in enumerate(LEFT_PAIRS):
        if graph_mask & (1 << index):
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen: set[int] = set()
    components = 0
    for vertex in range(6):
        if vertex in seen:
            continue
        components += 1
        stack = [vertex]
        seen.add(vertex)
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
    return components


def transformation_maps(
    edges: list[tuple[int, int]],
    group: list[tuple[tuple[int, ...], tuple[int, ...]]],
) -> list[tuple[list[int], list[int]]]:
    edge_index = {edge: index for index, edge in enumerate(edges)}
    maps = []
    for left_permutation, right_permutation in group:
        free_map = [
            edge_index[
                (
                    left_permutation[left],
                    right_permutation[right],
                )
            ]
            for left, right in edges
        ]
        graph_map = [
            LEFT_PAIR_INDEX[
                tuple(
                    sorted(
                        (
                            left_permutation[left],
                            left_permutation[right],
                        )
                    )
                )
            ]
            for left, right in LEFT_PAIRS
        ]
        maps.append((free_map, graph_map))
    return maps


def transform_mask(mask: int, mapping: list[int]) -> int:
    result = 0
    for source, target in enumerate(mapping):
        if mask & (1 << source):
            result |= 1 << target
    return result


def raw_cases(
    edges: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    cases = []
    for selected_free_indices in itertools.combinations(range(12), 4):
        edge_counts = [0] * 6
        free_mask = 0
        for index in selected_free_indices:
            free_mask |= 1 << index
            edge_counts[edges[index][0]] += 1

        required_degrees = [1 + count for count in edge_counts]
        for selected_graph_indices in itertools.combinations(
            range(15), 5
        ):
            degrees = [0] * 6
            graph_mask = 0
            for index in selected_graph_indices:
                graph_mask |= 1 << index
                left, right = LEFT_PAIRS[index]
                degrees[left] += 1
                degrees[right] += 1
            if degrees == required_degrees:
                cases.append((free_mask, graph_mask))
    require(
        len(cases) == 11130,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:195',
    )
    return cases


def classify(partition: tuple[int, ...]) -> dict[str, object]:
    edges = pole_graph(partition)
    group = automorphisms(edges)
    maps = transformation_maps(edges, group)
    cases = raw_cases(edges)
    paid_cycle_masks = four_cycle_masks(partition, edges)

    orbit_members: dict[tuple[int, int], int] = {}
    orbit_types: dict[tuple[int, int], str] = {}
    orbit_cycle_union: dict[tuple[int, int], bool] = {}
    for free_mask, graph_mask in cases:
        canonical = min(
            (
                transform_mask(free_mask, free_map),
                transform_mask(graph_mask, graph_map),
            )
            for free_map, graph_map in maps
        )
        orbit_members[canonical] = orbit_members.get(canonical, 0) + 1
        components = connected_components(graph_mask)
        branch = "tree" if components == 1 else "cyclic"
        previous = orbit_types.setdefault(canonical, branch)
        require(
            previous == branch,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:221',
        )
        is_cycle_union = free_mask in paid_cycle_masks
        previous_cycle = orbit_cycle_union.setdefault(
            canonical, is_cycle_union
        )
        require(
            previous_cycle == is_cycle_union,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:226',
        )

    tree_orbits = sum(
        branch == "tree" for branch in orbit_types.values()
    )
    cyclic_orbits = sum(
        branch == "cyclic" for branch in orbit_types.values()
    )
    tree_cases = sum(
        orbit_members[key]
        for key, branch in orbit_types.items()
        if branch == "tree"
    )
    cyclic_cases = sum(
        orbit_members[key]
        for key, branch in orbit_types.items()
        if branch == "cyclic"
    )
    require(
        tree_cases == 8730,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:244',
    )
    require(
        cyclic_cases == 2400,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:245',
    )
    cycle_union_orbits = sum(orbit_cycle_union.values())
    cycle_union_cases = sum(
        orbit_members[key]
        for key, is_cycle_union in orbit_cycle_union.items()
        if is_cycle_union
    )
    open_representatives = []
    for (free_mask, graph_mask), orbit_size in sorted(
        orbit_members.items()
    ):
        if orbit_cycle_union[(free_mask, graph_mask)]:
            continue
        open_representatives.append(
            {
                "free_pole_edges": [
                    list(edges[index])
                    for index in range(len(edges))
                    if free_mask & (1 << index)
                ],
                "complement_graph_edges": [
                    list(LEFT_PAIRS[index])
                    for index in range(len(LEFT_PAIRS))
                    if graph_mask & (1 << index)
                ],
                "branch": orbit_types[(free_mask, graph_mask)],
                "orbit_size": orbit_size,
            }
        )

    representative_digests = [
        hashlib.sha256(
            json.dumps(
                representative,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest()
        for representative in open_representatives
    ]
    orbit_size_histogram: dict[str, int] = {}
    stabilizer_size_histogram: dict[str, int] = {}
    branch_histogram: dict[str, int] = {}
    for representative in open_representatives:
        orbit_size = representative["orbit_size"]
        stabilizer_size = len(group) // orbit_size
        branch = representative["branch"]
        orbit_size_histogram[str(orbit_size)] = (
            orbit_size_histogram.get(str(orbit_size), 0) + 1
        )
        stabilizer_size_histogram[str(stabilizer_size)] = (
            stabilizer_size_histogram.get(str(stabilizer_size), 0) + 1
        )
        branch_histogram[branch] = branch_histogram.get(branch, 0) + 1

    return {
        "partition": list(partition),
        "pole_graph_edges": len(edges),
        "automorphism_group_size": len(group),
        "raw_cases": len(cases),
        "orbits": len(orbit_members),
        "tree_orbits": tree_orbits,
        "cyclic_orbits": cyclic_orbits,
        "tree_cases": tree_cases,
        "cyclic_cases": cyclic_cases,
        "cycle_union_orbits": cycle_union_orbits,
        "cycle_union_cases": cycle_union_cases,
        "noncycle_orbits": len(orbit_members) - cycle_union_orbits,
        "noncycle_cases": len(cases) - cycle_union_cases,
        "minimum_orbit_size": min(orbit_members.values()),
        "maximum_orbit_size": max(orbit_members.values()),
        "orbit_size_sum": sum(orbit_members.values()),
        "open_representative_count": len(open_representatives),
        "open_representative_digests": representative_digests,
        "open_representative_digest_chain_sha256": hashlib.sha256(
            "".join(representative_digests).encode()
        ).hexdigest(),
        "open_orbit_size_histogram": orbit_size_histogram,
        "open_stabilizer_size_histogram": stabilizer_size_histogram,
        "open_branch_histogram": branch_histogram,
        "complete_sorted_output_sha256": hashlib.sha256(
            json.dumps(
                open_representatives,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest(),
    }


def payload() -> dict[str, object]:
    rows = [classify(partition) for partition in PARTITIONS]
    input_universe = {
        "partitions": [list(partition) for partition in PARTITIONS],
        "left_pairs": [list(pair) for pair in LEFT_PAIRS],
        "free_pole_edges_per_case": 4,
        "complement_edges_per_case": 5,
    }
    data: dict[str, object] = {
        "status": "PROVED_FINITE_REDUCTION_TARGET_OPEN",
        "classification": rows,
        "input_universe_sha256": hashlib.sha256(
            json.dumps(
                input_universe,
                sort_keys=True,
                separators=(",", ":"),
            ).encode()
        ).hexdigest(),
        "claims": {
            "raw_simple_vertex_cases": 11130,
            "pole_graph_symmetry_quotient": "PROVED",
            "symbolic_quartic_elimination": "OPEN",
            "ramified_or_repeated_vertex_branch": "OPEN",
            "owner_payment": "NONE",
        },
    }
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()
    data["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return data


def validate(data: dict[str, object]) -> None:
    require(
        data['status'] == 'PROVED_FINITE_REDUCTION_TARGET_OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:317',
    )
    rows = data["classification"]
    require(
        [row['partition'] for row in rows] == [list(partition) for partition in PARTITIONS],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:319',
    )
    expected_rows = [
        {
            "automorphism_group_size": 12,
            "orbits": 985,
            "tree_orbits": 768,
            "cyclic_orbits": 217,
            "cycle_union_cases": 0,
            "cycle_union_orbits": 0,
            "noncycle_cases": 11130,
            "noncycle_orbits": 985,
            "minimum_orbit_size": 3,
            "maximum_orbit_size": 12,
        },
        {
            "automorphism_group_size": 32,
            "orbits": 490,
            "tree_orbits": 359,
            "cyclic_orbits": 131,
            "cycle_union_cases": 6,
            "cycle_union_orbits": 2,
            "noncycle_cases": 11124,
            "noncycle_orbits": 488,
            "minimum_orbit_size": 2,
            "maximum_orbit_size": 32,
        },
        {
            "automorphism_group_size": 72,
            "orbits": 188,
            "tree_orbits": 138,
            "cyclic_orbits": 50,
            "cycle_union_cases": 0,
            "cycle_union_orbits": 0,
            "noncycle_cases": 11130,
            "noncycle_orbits": 188,
            "minimum_orbit_size": 9,
            "maximum_orbit_size": 72,
        },
        {
            "automorphism_group_size": 384,
            "orbits": 79,
            "tree_orbits": 53,
            "cyclic_orbits": 26,
            "cycle_union_cases": 18,
            "cycle_union_orbits": 2,
            "noncycle_cases": 11112,
            "noncycle_orbits": 77,
            "minimum_orbit_size": 6,
            "maximum_orbit_size": 384,
        },
    ]
    for row, expected in zip(rows, expected_rows, strict=True):
        require(
            row['pole_graph_edges'] == 12,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:373',
        )
        require(
            row['raw_cases'] == 11130,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:374',
        )
        require(
            row['tree_cases'] == 8730,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:375',
        )
        require(
            row['cyclic_cases'] == 2400,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:376',
        )
        for key, value in expected.items():
            require(
                row[key] == value,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:378',
            )
        require(
            row['tree_orbits'] + row['cyclic_orbits'] == row['orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:379',
        )
        require(
            row['cycle_union_orbits'] + row['noncycle_orbits'] == row['orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:380',
        )
        require(
            row['cycle_union_cases'] + row['noncycle_cases'] == 11130,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:381',
        )
        require(
            row['orbit_size_sum'] == 11130,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:382',
        )
        require(
            row['minimum_orbit_size'] >= 1,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:383',
        )
        require(
            row['maximum_orbit_size'] <= row['automorphism_group_size'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:384',
        )
        representative_digests = row["open_representative_digests"]
        require(
            row["open_representative_count"] == row['noncycle_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:386',
        )
        require(
            len(representative_digests) == row['noncycle_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:387',
        )
        require(
            len(set(representative_digests)) == len(representative_digests),
            "open representative digests must be unique",
        )
        require(
            all(
                len(digest) == 64
                and set(digest) <= set("0123456789abcdef")
                for digest in representative_digests
            ),
            "open representative digests must be canonical SHA-256 values",
        )
        require(
            row["open_representative_digest_chain_sha256"]
            == hashlib.sha256("".join(representative_digests).encode()).hexdigest(),
            "representative digest chain must bind the ordered digest list",
        )
        require(
            sum(row["open_orbit_size_histogram"].values())
            == row["noncycle_orbits"],
            "orbit-size histogram must cover every open orbit",
        )
        require(
            sum(
                int(size) * count
                for size, count in row["open_orbit_size_histogram"].items()
            )
            == row["noncycle_cases"],
            "orbit-size histogram must cover every open labeled case",
        )
        require(
            sum(row["open_stabilizer_size_histogram"].values())
            == row["noncycle_orbits"],
            "stabilizer histogram must cover every open orbit",
        )
        require(
            row["open_branch_histogram"]
            == {
                "tree": row["tree_orbits"] - row["cycle_union_orbits"],
                "cyclic": row["cyclic_orbits"],
            },
            "branch histogram must match the open orbit split",
        )
        require(
            len(row["complete_sorted_output_sha256"]) == 64,
            "complete sorted-output digest must be SHA-256",
        )

    claims = data["claims"]
    require(
        claims['raw_simple_vertex_cases'] == 11130,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:441',
    )
    require(
        claims['pole_graph_symmetry_quotient'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:442',
    )
    require(
        claims['symbolic_quartic_elimination'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:443',
    )
    require(
        claims['ramified_or_repeated_vertex_branch'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:444',
    )
    require(
        claims['owner_payment'] == 'NONE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:445',
    )

    supplied_hash = data["payload_sha256"]
    unhashed = dict(data)
    del unhashed["payload_sha256"]
    canonical = json.dumps(
        unhashed, sort_keys=True, separators=(",", ":")
    ).encode()
    require(
        supplied_hash == hashlib.sha256(canonical).hexdigest(),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:453',
    )


def rehash(data: dict[str, object]) -> None:
    data.pop("payload_sha256", None)
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()
    data["payload_sha256"] = hashlib.sha256(canonical).hexdigest()


def tamper_selftest(data: dict[str, object]) -> int:
    mutations: list[dict[str, object]] = []

    forged = copy.deepcopy(data)
    forged["classification"][0]["raw_cases"] = 11129
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][1]["tree_cases"] = 8729
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][2]["orbits"] += 1
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["symbolic_quartic_elimination"] = "PROVED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["owner_payment"] = "BOOKED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["classification"][0]["open_representative_digests"][0] = (
        "0" * 64
    )
    mutations.append(forged)

    rejected = 0
    for forged in mutations:
        rehash(forged)
        try:
            validate(forged)
        except VerificationError:
            rejected += 1
    require(
        rejected == len(mutations),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:500',
    )
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    data = payload()
    validate(data)
    if args.emit:
        CERTIFICATE.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        checked = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        require(
            checked == data,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/classify_q6_u2_quartic_graph_orbits.py:520',
        )
    rejected = tamper_selftest(data) if args.tamper_selftest else 0

    for row in data["classification"]:
        partition = "+".join(str(value) for value in row["partition"])
        print(
            f"partition={partition} aut={row['automorphism_group_size']} "
            f"orbits={row['orbits']} "
            f"tree={row['tree_orbits']} cyclic={row['cyclic_orbits']} "
            f"paid={row['cycle_union_orbits']} "
            f"open={row['noncycle_orbits']}"
        )
    if args.tamper_selftest:
        print(f"tamper mutations rejected: PASS {rejected}/6")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
