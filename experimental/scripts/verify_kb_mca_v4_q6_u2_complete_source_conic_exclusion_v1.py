#!/usr/bin/env python3
"""Verify the complete-source exclusion of the reduced Q=6,s=6,u=2 conic.

The mathematical proof is divisor-theoretic.  This verifier binds its exact
integer/orbit consequences:

* twelve quartic source rows saturate twice the degree-24 source divisor;
* reciprocal, D4, and D5 fixed-point/orbit residues are impossible;
* the historical 2+2+2 graph frontier has 324 cases in ten representatives,
  all deleted by the same signature-independent terminal.

It does not replace the proof that the source rows divide the producer
fibres, or the proof that a conic component factors through a degree-two
quotient.  Those dependencies are named in the certificate and note.
"""

from __future__ import annotations

import argparse
import copy
import functools
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


if not __debug__:
    raise RuntimeError("verifier refuses optimized Python execution")


class VerificationError(RuntimeError):
    """Raised when a certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1"
    / "kb_mca_v4_q6_u2_complete_source_conic_exclusion_v1.json"
)

LEFT_PAIRS = list(itertools.combinations(range(6), 2))
POLE_EDGES = [
    (0, 0),
    (0, 1),
    (1, 0),
    (1, 1),
    (2, 2),
    (2, 3),
    (3, 2),
    (3, 3),
    (4, 4),
    (4, 5),
    (5, 4),
    (5, 5),
]
TERMINAL = "DELETED_BY_COMPLETE_SOURCE_DIVISOR_PROFILE_OBSTRUCTION"


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(value: dict[str, Any]) -> str:
    unhashed = dict(value)
    unhashed.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(unhashed).encode()).hexdigest()


def reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerificationError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_pairs,
    )


def transform_mask(mask: int, mapping: list[int]) -> int:
    transformed = 0
    for index, target in enumerate(mapping):
        if mask & (1 << index):
            transformed |= 1 << target
    return transformed


@functools.cache
def automorphisms() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    edge_set = set(POLE_EDGES)
    permutations = list(itertools.permutations(range(6)))
    result = []
    for left_permutation in permutations:
        for right_permutation in permutations:
            if {
                (
                    left_permutation[left],
                    right_permutation[right],
                )
                for left, right in POLE_EDGES
            } == edge_set:
                result.append((left_permutation, right_permutation))
    require(len(result) == 384, "2+2+2 pole automorphism group")
    return result


def transformation_maps(
    group: list[tuple[tuple[int, ...], tuple[int, ...]]],
) -> list[tuple[list[int], list[int]]]:
    pole_index = {edge: index for index, edge in enumerate(POLE_EDGES)}
    pair_index = {pair: index for index, pair in enumerate(LEFT_PAIRS)}
    maps = []
    for left_permutation, right_permutation in group:
        free_map = [
            pole_index[
                (
                    left_permutation[left],
                    right_permutation[right],
                )
            ]
            for left, right in POLE_EDGES
        ]
        signature_map = [
            pair_index[
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
        maps.append((free_map, signature_map))
    return maps


def component_sizes(edges: list[tuple[int, int]]) -> tuple[int, ...]:
    adjacency = {vertex: set() for vertex in range(6)}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    unseen = set(range(6))
    sizes = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        stack = [seed]
        size = 0
        while stack:
            vertex = stack.pop()
            size += 1
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        sizes.append(size)
    return tuple(sorted(sizes))


def is_cycle_union(free_mask: int) -> bool:
    cycle_masks = []
    for offset in (0, 2, 4):
        mask = 0
        for index, (left, right) in enumerate(POLE_EDGES):
            if left in {offset, offset + 1}:
                mask |= 1 << index
        cycle_masks.append(mask)
    return free_mask in cycle_masks


def raw_cases() -> list[tuple[int, int]]:
    cases = []
    for selected in itertools.combinations(range(len(LEFT_PAIRS)), 5):
        degrees = [0] * 6
        signature_mask = 0
        for index in selected:
            signature_mask |= 1 << index
            left, right = LEFT_PAIRS[index]
            degrees[left] += 1
            degrees[right] += 1
        if sorted(degrees) != [1, 1, 2, 2, 2, 2]:
            continue
        endpoints = {
            vertex for vertex, degree in enumerate(degrees) if degree == 1
        }
        free_mask = 0
        for index, (left, _) in enumerate(POLE_EDGES):
            if left in endpoints:
                free_mask |= 1 << index
        require(free_mask.bit_count() == 4, "four component edge roots")
        cases.append((free_mask, signature_mask))
    require(len(cases) == 465, "raw conic graph cases")
    return cases


@functools.cache
def graph_frontier() -> dict[str, Any]:
    group = automorphisms()
    maps = transformation_maps(group)
    members: dict[tuple[int, int], int] = {}
    cycle_status: dict[tuple[int, int], bool] = {}
    for free_mask, signature_mask in raw_cases():
        canonical = min(
            (
                transform_mask(free_mask, free_map),
                transform_mask(signature_mask, signature_map),
            )
            for free_map, signature_map in maps
        )
        members[canonical] = members.get(canonical, 0) + 1
        status = is_cycle_union(free_mask)
        require(
            cycle_status.setdefault(canonical, status) == status,
            "cycle-union status is orbit-invariant",
        )

    cycle_union_cases = sum(
        members[key] for key, status in cycle_status.items() if status
    )
    p3c3_cases = 0
    representatives = []
    for (free_mask, signature_mask), orbit_size in sorted(members.items()):
        if cycle_status[(free_mask, signature_mask)]:
            continue
        signature_edges = [
            LEFT_PAIRS[index]
            for index in range(len(LEFT_PAIRS))
            if signature_mask & (1 << index)
        ]
        sizes = component_sizes(signature_edges)
        if sizes == (3, 3):
            p3c3_cases += orbit_size
            continue
        graph_type = {
            (6,): "P6",
            (2, 4): "P2_PLUS_C4",
        }[sizes]
        free_edges = [
            POLE_EDGES[index]
            for index in range(len(POLE_EDGES))
            if free_mask & (1 << index)
        ]
        degrees = [0] * 6
        for left, right in signature_edges:
            degrees[left] += 1
            degrees[right] += 1
        endpoint_rows = [
            vertex for vertex, degree in enumerate(degrees) if degree == 1
        ]
        representatives.append(
            {
                "id": f"R{len(representatives):02d}",
                "signature_graph_type": graph_type,
                "orbit_size": orbit_size,
                "endpoint_rows": endpoint_rows,
                "free_pole_edges": [list(edge) for edge in free_edges],
                "common_signature_edges": [
                    list(edge) for edge in signature_edges
                ],
                "terminal": TERMINAL,
            }
        )

    require(cycle_union_cases == 93, "cycle-union case count")
    require(p3c3_cases == 48, "P3+C3 case count")
    require(len(representatives) == 10, "ten graph representatives")
    require(
        sum(rep["orbit_size"] for rep in representatives) == 324,
        "324 post-star cases",
    )
    return {
        "pole_partition": [2, 2, 2],
        "automorphism_group_order": len(group),
        "raw_cases": 465,
        "cycle_union_cases": cycle_union_cases,
        "P3_PLUS_C3_cases": p3c3_cases,
        "post_star_cases": 324,
        "post_star_orbits": 10,
        "signature_case_histogram": {
            "P6": sum(
                rep["orbit_size"]
                for rep in representatives
                if rep["signature_graph_type"] == "P6"
            ),
            "P2_PLUS_C4": sum(
                rep["orbit_size"]
                for rep in representatives
                if rep["signature_graph_type"] == "P2_PLUS_C4"
            ),
        },
        "representatives": representatives,
    }


def d4_rows() -> list[dict[str, Any]]:
    rows = []
    for ramified_source_count in range(3):
        simple_size = 24 - 2 * ramified_source_count
        double_support_size = ramified_source_count
        double_orbit_possible = double_support_size % 4 == 0
        simple_orbit_possible = (simple_size - 2) % 4 == 0
        rows.append(
            {
                "ramified_source_count": ramified_source_count,
                "simple_support_size": simple_size,
                "double_support_size": double_support_size,
                "g_fixed_points_already_simple": 2,
                "double_stratum_orbit_condition": (
                    f"{double_support_size} == 0 (mod 4)"
                ),
                "simple_stratum_orbit_condition": (
                    f"{simple_size} == 2 (mod 4)"
                ),
                "double_stratum_possible": double_orbit_possible,
                "simple_stratum_possible": simple_orbit_possible,
                "compatible": (
                    double_orbit_possible and simple_orbit_possible
                ),
            }
        )
    return rows


def d5_rows() -> list[dict[str, Any]]:
    rows = []
    for ramified_source_count in range(3):
        simple_size = 24 - 2 * ramified_source_count
        double_support_size = ramified_source_count
        required_simple_fixed = simple_size % 5
        required_double_fixed = double_support_size
        fixed_points_required = (
            required_simple_fixed + required_double_fixed
        )
        if ramified_source_count == 2:
            reason = (
                "both g-fixed points would be the two b-fixed double "
                "roots, forcing iota=b"
            )
        else:
            reason = (
                f"requires {fixed_points_required} distinct g-fixed "
                "points but a nonidentity projectivity has two"
            )
        rows.append(
            {
                "ramified_source_count": ramified_source_count,
                "simple_support_size": simple_size,
                "double_support_size": double_support_size,
                "required_simple_g_fixed_points": required_simple_fixed,
                "required_double_g_fixed_points": required_double_fixed,
                "total_required_g_fixed_points": fixed_points_required,
                "compatible": False,
                "contradiction": reason,
            }
        )
    return rows


def build_payload() -> dict[str, Any]:
    data: dict[str, Any] = {
        "format": (
            "kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1"
        ),
        "status": "PROVED_COMPLETE_SOURCE_REDUCED_CONIC_EXCLUSION",
        "dependencies": {
            "source_reduction_commit": (
                "44542e91e459364a521870ed2ebde7f6fe5055bf"
            ),
            "conic_classification_commit": (
                "f42ad6ab64cda5f1d4061b73e739f8944ebb13eb"
            ),
            "manual_integration_commit": (
                "0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d"
            ),
            "source_fiber_parent_commit": (
                "8eaf2137094326756054e10ddcda7649df32b529"
            ),
            "required_results": [
                "H_DIVIDES_F_OUT_DIVIDES_M",
                "B_IS_COMPLETE_TWELVE_SOURCE_PULLBACK",
                "CONIC_COMPONENT_FACTORS_THROUGH_SEPARABLE_DEGREE_TWO_CHI",
                "RAMIFIED_COMMON_CONIC_BRANCHES_EXCLUDED",
                "REDUCED_PROFILES_ARE_RECIPROCAL_D4_D5",
            ],
        },
        "complete_source_saturation": {
            "source_count": 12,
            "row_binary_degree": 4,
            "complete_source_binary_degree": 24,
            "component_source_degree": 2,
            "left_total_degree": 48,
            "right_total_degree": 48,
            "local_inequality": (
                "sum_i ord_x H(alpha_i,-) <= 2 ord_x B"
            ),
            "global_identity": (
                "sum_i div H(alpha_i,-) = 2 div B"
            ),
            "product_identity": (
                "product_i H(alpha_i,-) is proportional to B^2"
            ),
            "conclusions": [
                "div(B) is invariant under the conic involution iota",
                (
                    "an iota-fixed B-root cannot have multiplicity one"
                ),
            ],
        },
        "profiles": {
            "RECIPROCAL": {
                "common_source_count": 5,
                "complete_source_count": 12,
                "J_fixed_source_count": 2,
                "fixed_sources_in_common_set": 1,
                "forced_fixed_sources_in_complement": 1,
                "forced_pole_multiplicity": 1,
                "required_iota_fixed_pole_multiplicity_parity": "even",
                "compatible": False,
                "terminal": TERMINAL,
            },
            "D4": {
                "g_order": 4,
                "g_fixed_point_count": 2,
                "nonfixed_orbit_size": 4,
                "common_fixed_points": 2,
                "ramification_rows": d4_rows(),
                "compatible": False,
                "terminal": TERMINAL,
            },
            "D5": {
                "g_order": 5,
                "g_fixed_point_count": 2,
                "nonfixed_orbit_size": 5,
                "common_fixed_points": 0,
                "ramification_rows": d5_rows(),
                "compatible": False,
                "terminal": TERMINAL,
            },
        },
        "graph_frontier_control": graph_frontier(),
        "conclusion": {
            "scope": (
                "all reduced Q=6,s=6,u=2 conic-image components, "
                "independent of pole partition and signature"
            ),
            "terminal": TERMINAL,
            "ledger_movement": 0,
            "closes": "REDUCED_CONIC_IMAGE_BRANCH",
            "still_open": [
                "u=2 birational-quartic image branch",
                "u=3 component branch",
                "KoalaBear row and cap-68 theorem",
            ],
        },
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def validate(data: dict[str, Any]) -> None:
    require(
        data["format"]
        == "kb-mca-v4-q6-u2-complete-source-conic-exclusion-v1",
        "format",
    )
    require(
        data["status"] == "PROVED_COMPLETE_SOURCE_REDUCED_CONIC_EXCLUSION",
        "status",
    )
    require(data["payload_sha256"] == payload_hash(data), "payload hash")
    dependencies = data["dependencies"]
    require(
        dependencies["source_reduction_commit"]
        == "44542e91e459364a521870ed2ebde7f6fe5055bf",
        "source-reduction commit",
    )
    require(
        dependencies["conic_classification_commit"]
        == "f42ad6ab64cda5f1d4061b73e739f8944ebb13eb",
        "conic-classification commit",
    )
    require(
        dependencies["manual_integration_commit"]
        == "0f7476f0fcbc5d1a1d3eed0c03221aaa48f5767d",
        "manual-integration commit",
    )
    require(
        dependencies["source_fiber_parent_commit"]
        == "8eaf2137094326756054e10ddcda7649df32b529",
        "source-fiber parent commit",
    )

    saturation = data["complete_source_saturation"]
    require(saturation["source_count"] == 12, "twelve sources")
    require(saturation["row_binary_degree"] == 4, "quartic rows")
    require(
        saturation["complete_source_binary_degree"] == 24,
        "degree-24 complete source divisor",
    )
    require(
        saturation["component_source_degree"] == 2,
        "source degree two",
    )
    require(
        saturation["left_total_degree"]
        == saturation["source_count"] * saturation["row_binary_degree"]
        == 48,
        "left divisor degree",
    )
    require(
        saturation["right_total_degree"]
        == 2 * saturation["complete_source_binary_degree"]
        == 48,
        "right divisor degree",
    )
    require(
        saturation["global_identity"]
        == "sum_i div H(alpha_i,-) = 2 div B",
        "global divisor saturation identity",
    )
    require(
        saturation["conclusions"]
        == [
            "div(B) is invariant under the conic involution iota",
            "an iota-fixed B-root cannot have multiplicity one",
        ],
        "saturation conclusions",
    )

    profiles = data["profiles"]
    require(set(profiles) == {"RECIPROCAL", "D4", "D5"}, "profiles")
    reciprocal = profiles["RECIPROCAL"]
    require(
        reciprocal["complete_source_count"] % 2 == 0,
        "reciprocal complete set parity",
    )
    require(
        reciprocal["common_source_count"] % 2 == 1,
        "reciprocal common set parity",
    )
    require(
        reciprocal["fixed_sources_in_common_set"] == 1,
        "one common reciprocal fixed source",
    )
    require(
        reciprocal["forced_fixed_sources_in_complement"] == 1,
        "second reciprocal fixed source",
    )
    require(
        reciprocal["forced_pole_multiplicity"] == 1,
        "reciprocal fixed fibre is unramified",
    )
    require(not reciprocal["compatible"], "reciprocal excluded")

    d4 = profiles["D4"]
    require(
        (d4["g_order"], d4["g_fixed_point_count"])
        == (4, 2),
        "D4 action",
    )
    require(d4["common_fixed_points"] == 2, "D4 common fixed pair")
    expected_d4 = [
        (0, 24, 0, True, False),
        (1, 22, 1, False, True),
        (2, 20, 2, False, False),
    ]
    actual_d4 = [
        (
            row["ramified_source_count"],
            row["simple_support_size"],
            row["double_support_size"],
            row["double_stratum_possible"],
            row["simple_stratum_possible"],
        )
        for row in d4["ramification_rows"]
    ]
    require(actual_d4 == expected_d4, "D4 ramification table")
    require(
        all(not row["compatible"] for row in d4["ramification_rows"]),
        "D4 rows excluded",
    )
    require(not d4["compatible"], "D4 excluded")

    d5 = profiles["D5"]
    require(
        (d5["g_order"], d5["g_fixed_point_count"])
        == (5, 2),
        "D5 action",
    )
    require(d5["common_fixed_points"] == 0, "D5 common fixed count")
    expected_d5 = [
        (0, 24, 0, 4, 0, 4),
        (1, 22, 1, 2, 1, 3),
        (2, 20, 2, 0, 2, 2),
    ]
    actual_d5 = [
        (
            row["ramified_source_count"],
            row["simple_support_size"],
            row["double_support_size"],
            row["required_simple_g_fixed_points"],
            row["required_double_g_fixed_points"],
            row["total_required_g_fixed_points"],
        )
        for row in d5["ramification_rows"]
    ]
    require(actual_d5 == expected_d5, "D5 ramification table")
    require(
        all(not row["compatible"] for row in d5["ramification_rows"]),
        "D5 rows excluded",
    )
    require(not d5["compatible"], "D5 excluded")

    frontier = data["graph_frontier_control"]
    require(frontier == graph_frontier(), "regenerated graph frontier")
    require(
        frontier["signature_case_histogram"]
        == {"P6": 288, "P2_PLUS_C4": 36},
        "signature case histogram",
    )
    expected_orbits = [48, 24, 24, 48, 12, 48, 48, 24, 24, 24]
    require(
        [row["orbit_size"] for row in frontier["representatives"]]
        == expected_orbits,
        "representative orbit sizes",
    )
    require(
        all(
            row["endpoint_rows"] == [0, 2]
            for row in frontier["representatives"]
        ),
        "canonical endpoint rows",
    )
    require(
        all(
            row["terminal"] == TERMINAL
            for row in frontier["representatives"]
        ),
        "uniform representative terminal",
    )

    conclusion = data["conclusion"]
    require(
        conclusion["closes"] == "REDUCED_CONIC_IMAGE_BRANCH",
        "closed branch",
    )
    require(conclusion["ledger_movement"] == 0, "zero ledger movement")
    require(
        conclusion["terminal"] == TERMINAL,
        "conclusion terminal",
    )


def rehash(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_hash(data)


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[dict[str, Any]] = []

    def mutate(path: tuple[Any, ...], value: Any) -> None:
        forged = copy.deepcopy(data)
        target: Any = forged
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        rehash(forged)
        mutations.append(forged)

    mutate(("complete_source_saturation", "source_count"), 11)
    mutate(
        ("dependencies", "conic_classification_commit"),
        "f42ad6ab6",
    )
    mutate(("complete_source_saturation", "row_binary_degree"), 3)
    mutate(
        ("complete_source_saturation", "complete_source_binary_degree"),
        23,
    )
    mutate(("complete_source_saturation", "component_source_degree"), 3)
    mutate(("complete_source_saturation", "left_total_degree"), 44)
    mutate(("complete_source_saturation", "right_total_degree"), 46)
    mutate(
        ("complete_source_saturation", "global_identity"),
        "only an inequality",
    )
    mutate(
        ("complete_source_saturation", "conclusions", 0),
        "div(B) invariance is open",
    )
    mutate(("profiles", "RECIPROCAL", "common_source_count"), 4)
    mutate(
        ("profiles", "RECIPROCAL", "fixed_sources_in_common_set"),
        0,
    )
    mutate(
        ("profiles", "RECIPROCAL", "forced_pole_multiplicity"),
        2,
    )
    mutate(("profiles", "RECIPROCAL", "compatible"), True)
    mutate(
        ("profiles", "D4", "ramification_rows", 0, "simple_support_size"),
        22,
    )
    mutate(
        (
            "profiles",
            "D4",
            "ramification_rows",
            1,
            "double_stratum_possible",
        ),
        True,
    )
    mutate(("profiles", "D4", "common_fixed_points"), 0)
    mutate(("profiles", "D4", "compatible"), True)
    mutate(
        (
            "profiles",
            "D5",
            "ramification_rows",
            0,
            "required_simple_g_fixed_points",
        ),
        2,
    )
    mutate(
        (
            "profiles",
            "D5",
            "ramification_rows",
            2,
            "required_double_g_fixed_points",
        ),
        1,
    )
    mutate(("profiles", "D5", "common_fixed_points"), 2)
    mutate(("profiles", "D5", "compatible"), True)
    mutate(("graph_frontier_control", "post_star_cases"), 323)
    mutate(
        (
            "graph_frontier_control",
            "signature_case_histogram",
            "P6",
        ),
        287,
    )
    mutate(
        (
            "graph_frontier_control",
            "representatives",
            0,
            "orbit_size",
        ),
        47,
    )
    mutate(
        (
            "graph_frontier_control",
            "representatives",
            4,
            "signature_graph_type",
        ),
        "P6",
    )
    mutate(
        (
            "graph_frontier_control",
            "representatives",
            9,
            "terminal",
        ),
        "UNPAID_PRIMITIVE",
    )
    mutate(("conclusion", "closes"), "NOTHING")
    mutate(("conclusion", "ledger_movement"), 1)
    mutate(("conclusion", "terminal"), "UNRESOLVED")

    rejected = 0
    for forged in mutations:
        try:
            validate(forged)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "all mutations rejected")
    duplicate_rejected = 0
    try:
        json.loads(
            '{"status":"first","status":"forged"}',
            object_pairs_hook=reject_duplicate_pairs,
        )
    except VerificationError:
        duplicate_rejected = 1
    require(duplicate_rejected == 1, "duplicate JSON key rejected")
    return rejected + duplicate_rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-hash", action="store_true")
    args = parser.parse_args()

    data = build_payload()
    validate(data)
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.check:
        require(CERTIFICATE.exists(), "certificate is missing")
        committed = load_json(CERTIFICATE)
        require(committed == data, "committed certificate differs")
        validate(committed)
    rejected = tamper_selftest(data) if args.tamper_selftest else 0

    if args.print_hash:
        print(data["payload_sha256"])
        return 0
    print(f"status={data['status']}")
    print(
        "divisor_identity="
        + data["complete_source_saturation"]["global_identity"]
    )
    for profile_name, profile in data["profiles"].items():
        print(
            f"profile={profile_name} compatible={profile['compatible']} "
            f"terminal={profile['terminal']}"
        )
    frontier = data["graph_frontier_control"]
    print(
        "2+2+2_frontier="
        f"{frontier['post_star_cases']}_cases/"
        f"{frontier['post_star_orbits']}_orbits"
    )
    print(f"ledger_movement={data['conclusion']['ledger_movement']}")
    if args.tamper_selftest:
        print(f"tamper_selftest={rejected}/{rejected}")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
