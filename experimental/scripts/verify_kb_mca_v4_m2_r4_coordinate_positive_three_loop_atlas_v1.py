#!/usr/bin/env python3
"""Verify the positive-coordinate three-loop compiler packet."""

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

import sympy as sp

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
    / "data/certificates/kb-mca-v4-m2-r4-coordinate-positive-three-loop-atlas-v1"
    / "kb_mca_v4_m2_r4_coordinate_positive_three_loop_atlas_v1.json"
)
SOURCE_FACET_PARENT = {
    "commit": "77b0971ebb443efd8487ee3809cd988ba183d00c",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.md",
    "note_blob_oid": "a74eb30e46d8941c1cc4c598b2fdff6a3daad657",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.py",
    "verifier_blob_oid": "8c1fd1318b180f27a3114a3a3beedd7e2ed3efbd",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r4-order2-source-facet-interpolation-v1/kb_mca_v4_m2_r4_order2_source_facet_interpolation_v1.json",
    "certificate_blob_oid": "c0f6f9496e4bf43b60358133372ce47bc9b5c8dd",
    "certificate_payload_sha256": "96c47c813c41f4b268b9826ed4866e14d44c5a8187487266a3de6f550cbbf6b6",
    "terminal": "M2_R4_ORDER_TWO_SOURCE_FACET_AND_DIAGONAL_INTERPOLATION_INTERFACES",
}
COEFFICIENT_PARENT = {
    "commit": "543db66fa66793690651a5f81ea90b8f8f81e66c",
    "note_path": "experimental/notes/frontier-adjacent/kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.md",
    "note_blob_oid": "f58c2ea9cea88dfc6be637e9f1f14e86e8862cc6",
    "verifier_path": "experimental/scripts/verify_kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.py",
    "verifier_blob_oid": "7cc4eb6e0560ca5c587f91623dc407892a07e2ca",
    "certificate_path": "experimental/data/certificates/kb-mca-v4-m2-r4-order2-source-subfield-coefficient-compilers-v1/kb_mca_v4_m2_r4_order2_source_subfield_coefficient_compilers_v1.json",
    "certificate_blob_oid": "033043e7a0969ea9f98207567b890b10e3077271",
    "certificate_payload_sha256": "f0b751301e56989bf6fbf19cf15e5ff8faa0d7d86e76278306950a488cdf5156",
    "terminal": "M2_R4_ORDER_TWO_SOURCE_SUBFIELD_AND_COEFFICIENT_COMPILERS",
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


def load_parent(parent: dict[str, str]) -> dict[str, Any]:
    for path_key, blob_key in (
        ("note_path", "note_blob_oid"),
        ("verifier_path", "verifier_blob_oid"),
        ("certificate_path", "certificate_blob_oid"),
    ):
        require(
            git_output("rev-parse", f"{parent['commit']}:{parent[path_key]}")
            == parent[blob_key],
            f"parent blob {parent[path_key]}",
        )
    data = parse_json(
        git_output("show", f"{parent['commit']}:{parent['certificate_path']}"),
        parent["certificate_path"],
    )
    require(data.get("payload_sha256") == parent["certificate_payload_sha256"],
            "parent payload")
    require(payload_hash(data) == data.get("payload_sha256"), "parent seal")
    require(data["conclusion"]["terminal"] == parent["terminal"],
            "parent terminal")
    require(data["conclusion"]["order_two_type_deleted"] is False,
            "parent scope")
    return data


def load_parents() -> None:
    source = load_parent(SOURCE_FACET_PARENT)
    coefficient = load_parent(COEFFICIENT_PARENT)
    profiles = source["coordinate_orientation"]["replay"][
        "exhaustive_K_pair_degree_profiles"
    ]
    require(profiles == [
        [[4, 4], [4, 4], [2, 2]],
        [[4, 4], [3, 3], [3, 3]],
    ], "source parent profiles")
    normal = coefficient["coordinate_coefficient_normal_form"]
    require(normal["source_eigenspace_dimensions"] == [8, 7],
            "coefficient parent dimensions")
    require(normal["positive_form"] == "A_2(W)T^2+A_0(W)+XT B_1(W)",
            "coefficient parent positive form")
    interpolation = coefficient["source_row_interpolation"]
    require(
        interpolation["complete_source_resultant"]
        == "Res_T(A,H) is proportional to B^2",
        "coefficient parent complete-source square",
    )
    source_note = git_output("show", f"{SOURCE_FACET_PARENT['commit']}:{SOURCE_FACET_PARENT['note_path']}")
    require("allowing `x_p=bx_p` at ramification" in source_note,
            "source parent ramified divisor")
    require("at ramification it is\n`H(T,x_p)^2`" in source_note,
            "source parent ramified square")
    require(coefficient["parent"] == SOURCE_FACET_PARENT,
            "coefficient-to-source parent pin")


COMMON_PROFILES = {
    "442": ((4, 4, 2), (1, 0, 2)),
    "433": ((4, 3, 3), (0, 2, 1)),
}


def permute_record(record, permutation):
    loops, multiplicities = record
    edge_values = {
        (0, 1): multiplicities[0],
        (0, 2): multiplicities[1],
        (1, 2): multiplicities[2],
    }
    return (
        tuple(loops[permutation[index]] for index in range(3)),
        tuple(
            edge_values[tuple(sorted((permutation[left], permutation[right])))]
            for left, right in ((0, 1), (0, 2), (1, 2))
        ),
    )


def common_loop_census() -> dict[str, Any]:
    replay = {}
    expected = {
        "442": (
            (((0, 0, 0), (3, 1, 1)), 1),
            (((0, 0, 1), (4, 0, 0)), 1),
            (((0, 1, 0), (2, 2, 0)), 2),
            (((1, 1, 0), (1, 1, 1)), 1),
            (((1, 1, 1), (2, 0, 0)), 1),
        ),
        "433": (
            (((0, 0, 0), (2, 2, 1)), 1),
            (((0, 0, 1), (3, 1, 0)), 2),
            (((1, 0, 0), (1, 1, 2)), 1),
            (((1, 0, 1), (2, 0, 1)), 2),
            (((1, 1, 1), (1, 1, 0)), 1),
        ),
    }
    for name, (degrees, equal_swap) in COMMON_PROFILES.items():
        solutions = set()
        for loops in itertools.product(range(2), repeat=3):
            for multiplicities in itertools.product(range(5), repeat=3):
                de, df, ef = multiplicities
                if sum(loops) + sum(multiplicities) != 5:
                    continue
                observed = (
                    2 * loops[0] + de + df,
                    2 * loops[1] + de + ef,
                    2 * loops[2] + df + ef,
                )
                if observed == degrees:
                    solutions.add((loops, multiplicities))
        unseen = set(solutions)
        orbits = []
        while unseen:
            representative = min(unseen)
            orbit = {representative, permute_record(representative, equal_swap)}
            require(orbit <= solutions, f"{name} equal-degree closure")
            unseen -= orbit
            orbits.append((representative, len(orbit)))
        observed_orbits = tuple(sorted(orbits))
        require(observed_orbits == expected[name], f"{name} common census")
        replay[name] = {
            "degrees": list(degrees),
            "labeled_count": len(solutions),
            "orbits": [
                {
                    "loops": list(record[0]),
                    "multiplicities": list(record[1]),
                    "orbit_size": size,
                }
                for record, size in observed_orbits
            ],
            "three_loop_orbit_count": sum(
                sum(record[0]) == 3 for record, _ in observed_orbits
            ),
        }
    require(sum(row["labeled_count"] for row in replay.values()) == 13,
            "common labeled total")
    require(sum(len(row["orbits"]) for row in replay.values()) == 10,
            "common orbit total")
    return replay


def minimum_cross_defect(multiplicity: int) -> int:
    return min(
        2 * math.comb(positive, 2)
        + 2 * math.comb(multiplicity - positive, 2)
        for positive in range(multiplicity + 1)
    )


def outside_skeleton_census() -> dict[str, Any]:
    solutions = set()
    for colored in itertools.product(range(3), repeat=3):
        if sum(colored) != 2:
            continue
        for multiplicities in itertools.product(range(6), repeat=3):
            de, df, ef = multiplicities
            if sum(multiplicities) != 5:
                continue
            degrees = (
                colored[0] + de + df,
                colored[1] + de + ef,
                colored[2] + df + ef,
            )
            if degrees == (4, 4, 4):
                solutions.add((colored, multiplicities))
    unseen = set(solutions)
    orbits = []
    for representative in sorted(solutions):
        if representative not in unseen:
            continue
        orbit = {
            permute_record(representative, permutation)
            for permutation in itertools.permutations(range(3))
        }
        require(orbit <= solutions, "outside permutation closure")
        unseen -= orbit
        orbits.append((representative, len(orbit)))
    expected = (
        (((0, 0, 2), (3, 1, 1)), 3),
        (((0, 1, 1), (2, 2, 1)), 3),
    )
    require(tuple(orbits) == expected, "outside skeleton orbits")
    rows = []
    for (colored, multiplicities), orbit_size in orbits:
        rows.append({
            "colored": list(colored),
            "multiplicities": list(multiplicities),
            "orbit_size": orbit_size,
            "minimum_additional_defect": sum(
                minimum_cross_defect(value) for value in multiplicities
            ),
        })
    require([row["minimum_additional_defect"] for row in rows] == [2, 0],
            "outside defect cut")
    return {
        "raw_labeled_count": len(solutions),
        "raw_orbits": rows,
        "common_loop_defect": 3,
        "component_defect_budget": 3,
        "survivor": {"colored": [0, 1, 1], "multiplicities": [2, 2, 1]},
    }


def permute_outside_record(record, permutation):
    colored, loops, multiplicities = record
    edge_values = {
        (0, 1): multiplicities[0],
        (0, 2): multiplicities[1],
        (1, 2): multiplicities[2],
    }
    return (
        tuple(colored[permutation[index]] for index in range(3)),
        tuple(loops[permutation[index]] for index in range(3)),
        tuple(
            edge_values[tuple(sorted((permutation[left], permutation[right])))]
            for left, right in ((0, 1), (0, 2), (1, 2))
        ),
    )


def residual_loop_workboard(common_census: dict[str, Any]) -> dict[str, Any]:
    common_names = {
        ("442", (0, 0, 0), (3, 1, 1)): "442-0a",
        ("442", (0, 0, 1), (4, 0, 0)): "442-1a",
        ("442", (0, 1, 0), (2, 2, 0)): "442-1b",
        ("442", (1, 1, 0), (1, 1, 1)): "442-2",
        ("442", (1, 1, 1), (2, 0, 0)): "442-3",
        ("433", (0, 0, 0), (2, 2, 1)): "433-0",
        ("433", (0, 0, 1), (3, 1, 0)): "433-1a",
        ("433", (1, 0, 0), (1, 1, 2)): "433-1b",
        ("433", (1, 0, 1), (2, 0, 1)): "433-2",
        ("433", (1, 1, 1), (1, 1, 0)): "433-3",
    }
    common_rows = []
    for profile in ("442", "433"):
        for row in common_census[profile]["orbits"]:
            loops = tuple(row["loops"])
            multiplicities = tuple(row["multiplicities"])
            loop_count = sum(loops)
            defect = loop_count + sum(
                minimum_cross_defect(value) for value in multiplicities
            )
            reason = "live"
            if loop_count > 1:
                reason = "global-loop-cap"
            elif defect > 3:
                reason = "common-defect-budget"
            common_rows.append({
                "name": common_names[(profile, loops, multiplicities)],
                "profile": profile,
                "loops": list(loops),
                "multiplicities": list(multiplicities),
                "orbit_size": row["orbit_size"],
                "loop_count": loop_count,
                "minimum_common_defect": defect,
                "verdict": reason,
            })

    outside_names = {
        ((0, 0, 2), (0, 0, 0), (3, 1, 1)): "O0a",
        ((0, 1, 1), (0, 0, 0), (2, 2, 1)): "O0b",
        ((0, 0, 2), (0, 0, 1), (4, 0, 0)): "O1a",
        ((0, 0, 2), (0, 1, 0), (2, 2, 0)): "O1b",
        ((0, 1, 1), (0, 0, 1), (3, 1, 0)): "O1c",
        ((0, 1, 1), (1, 0, 0), (1, 1, 2)): "O1d",
    }
    outside_rows = []
    raw_counts = {}
    for loop_count in (0, 1):
        solutions = set()
        for colored in itertools.product(range(3), repeat=3):
            if sum(colored) != 2:
                continue
            for loops in itertools.product(range(2), repeat=3):
                if sum(loops) != loop_count:
                    continue
                for multiplicities in itertools.product(range(6), repeat=3):
                    de, df, ef = multiplicities
                    if sum(multiplicities) + loop_count != 5:
                        continue
                    degrees = (
                        colored[0] + 2 * loops[0] + de + df,
                        colored[1] + 2 * loops[1] + de + ef,
                        colored[2] + 2 * loops[2] + df + ef,
                    )
                    if degrees == (4, 4, 4):
                        solutions.add((colored, loops, multiplicities))
        raw_counts[str(loop_count)] = len(solutions)
        unseen = set(solutions)
        for representative in sorted(solutions):
            if representative not in unseen:
                continue
            orbit = {
                permute_outside_record(representative, permutation)
                for permutation in itertools.permutations(range(3))
            }
            require(orbit <= solutions, "residual outside permutation closure")
            unseen -= orbit
            colored, loops, multiplicities = representative
            defect = sum(loops) + sum(
                minimum_cross_defect(value) for value in multiplicities
            )
            outside_rows.append({
                "name": outside_names[representative],
                "colored": list(colored),
                "loops": list(loops),
                "multiplicities": list(multiplicities),
                "orbit_size": len(orbit),
                "minimum_outside_defect": defect,
            })

    routes = {}
    for common in common_rows:
        if common["verdict"] != "live":
            continue
        allowed = []
        for outside in outside_rows:
            outside_loop_count = sum(outside["loops"])
            if common["loop_count"] + outside_loop_count > 1:
                continue
            if (common["minimum_common_defect"]
                    + outside["minimum_outside_defect"] > 3):
                continue
            allowed.append(outside["name"])
        require(allowed, f"empty residual route {common['name']}")
        routes[common["name"]] = allowed

    expected_routes = {
        "442-0a": ["O0b", "O1b", "O1d"],
        "442-1b": ["O0a", "O0b"],
        "433-0": ["O0a", "O0b", "O1b", "O1c", "O1d"],
        "433-1a": ["O0b"],
        "433-1b": ["O0a", "O0b"],
    }
    require(routes == expected_routes, "residual route table")
    live = [row for row in common_rows if row["verdict"] == "live"]
    require(len(live) == 5, "live common orbit count")
    require(sum(row["orbit_size"] for row in live) == 7,
            "live labeled common count")
    require(raw_counts == {"0": 6, "1": 18}, "outside raw counts")
    require(len(outside_rows) == 6, "outside orbit count")
    return {
        "component_defect_budget": 3,
        "maximum_positive_total_loop_count": 1,
        "common_rows": common_rows,
        "live_common_orbit_count": len(live),
        "live_common_labeled_count": sum(row["orbit_size"] for row in live),
        "outside_raw_counts_by_loop_count": raw_counts,
        "outside_orbits": outside_rows,
        "routes": routes,
        "representative_route_count": sum(len(value) for value in routes.values()),
    }


def product_row(w, product, a0, ai, a1):
    return (
        -a0**2 + (a0**2 - a1**2) * w - product,
        -(a1**2 + product) * w,
        (ai**2 - a1**2) * w - (ai**2 + product) * w**2,
        sp.Integer(0),
    )


def sum_row(source, target_sum):
    w = source**2
    return (
        target_sum,
        target_sum * w,
        target_sum * w**2,
        source * (w - 1),
    )


def common_matrix(a0, ai, a1, records):
    rows = []
    for source, product, target_sum in records:
        rows.append(product_row(source**2, product, a0, ai, a1))
        rows.append(sum_row(source, target_sum))
    return sp.Matrix(rows)


def polynomial_digest(polynomial, variables) -> str:
    terms = [
        [list(exponents), str(coefficient)]
        for exponents, coefficient in sp.Poly(polynomial, *variables).terms()
    ]
    return hashlib.sha256(canonical_json(terms).encode()).hexdigest()


def placement_role_orbits(profile: str):
    if profile == "442":
        assignments = {("H", "H", "L"), ("H", "L", "H"), ("L", "H", "H")}
    elif profile == "433":
        assignments = {("H", "L", "L"), ("L", "H", "L"), ("L", "L", "H")}
    else:
        raise VerificationError(f"unknown profile {profile}")
    unseen = set(assignments)
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {representative, (representative[1], representative[0], representative[2])}
        require(orbit <= assignments, f"{profile} ramified-swap closure")
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    return tuple(sorted(orbits))


def common_kernel_replay() -> dict[str, Any]:
    a0, ai, a1, d0, d1, d2, beta, w = sp.symbols(
        "a0 ai a1 d0 d1 d2 beta w"
    )
    denominator = d0 + d1 * w + d2 * w**2
    middle = (
        (a0**2 - a1**2) * d0
        - a1**2 * d1
        + (ai**2 - a1**2) * d2
    )
    numerator = -a0**2 * d0 + middle * w - ai**2 * d2 * w**2
    require(sp.expand(numerator.subs(w, 0) + a0**2 * denominator.subs(w, 0)) == 0,
            "zero loop interpolation")
    require(sp.expand(numerator.subs(w, 1) + a1**2 * denominator.subs(w, 1)) == 0,
            "one loop interpolation")
    require(sp.Poly(numerator, w).coeff_monomial(w**2) == -ai**2 * d2,
            "infinity loop interpolation")

    p, s, z = sp.symbols("p s z")
    h = sp.Matrix((d0, d1, d2, beta))
    require(
        sp.expand((sp.Matrix([product_row(w, p, a0, ai, a1)]) * h)[0]
                  - (numerator - p * denominator)) == 0,
        "common product row",
    )
    require(
        sp.expand((sp.Matrix([sum_row(z, s)]) * h)[0]
                  - (s * denominator.subs(w, z**2) + z * beta * (z**2 - 1))) == 0,
        "common sum row",
    )

    x, y, b, c = sp.symbols("x y b c")
    source_guard = x * y * (x**2 - 1) * (x**2 - y**2) * (y**2 - 1)
    cases = {
        "442_root_low": (
            common_matrix(1, b, c, ((x, b, 1 + b), (y, -b, 1 - b))),
            -source_guard * (b**2 - 1),
            (y - x) * (b**2 - c**2) + b * x * y * (x + y) * (c**2 - 1),
        ),
        "442_root_high": (
            common_matrix(1, b, c, ((x, c, 1 + c), (y, -c, 1 - c))),
            -source_guard * (c**2 - 1),
            (y - x) * (b**2 - c**2)
            + x * y * (
                x * (c - 1) * (b**2 + c)
                + y * (c + 1) * (b**2 - c)
            ),
        ),
        "433_root_low": (
            common_matrix(1, b, c, ((x, b, 1 + b), (y, c, 1 + c))),
            source_guard * (b + 1) * (c + 1),
            (y - x) * (b**2 - c**2)
            + (c - 1) * x * y * (b * (c + 1) * x - (b**2 + c) * y),
        ),
        "433_root_high": (
            common_matrix(1, b, c, ((x, c, 1 + c), (y, b * c, b + c))),
            source_guard * (b + c) * (c + 1),
            (b - c) * ((b + c) * y - (b * c + 1) * x)
            + x * y * (c - 1) * ((b**2 + c) * x - b * (c + 1) * y),
        ),
    }
    formulas = {
        "442_root_low": "(y-x)(b^2-c^2)+bxy(x+y)(c^2-1)",
        "442_root_high": "(y-x)(b^2-c^2)+xy[x(c-1)(b^2+c)+y(c+1)(b^2-c)]",
        "433_root_low": "(y-x)(b^2-c^2)+(c-1)xy[b(c+1)x-(b^2+c)y]",
        "433_root_high": "(b-c)[(b+c)y-(bc+1)x]+xy(c-1)[(b^2+c)x-b(c+1)y]",
    }
    role_orbits = {
        profile: placement_role_orbits(profile) for profile in ("442", "433")
    }
    require({profile: len(orbits) for profile, orbits in role_orbits.items()}
            == {"442": 2, "433": 2}, "common placement orbit count")
    replay = {}
    for name, (matrix, guard, residual) in cases.items():
        require(matrix.shape == (4, 4), f"{name} matrix shape")
        require(sp.expand(matrix.det() - guard * residual) == 0,
                f"{name} determinant")
        require(sp.total_degree(residual) == 6, f"{name} residual degree")
        replay[name] = {
            "matrix_shape": [4, 4],
            "residual": formulas[name],
            "residual_total_degree": 6,
            "residual_digest": polynomial_digest(residual, (x, y, b, c)),
        }
    return {
        "loop_normalization": {"ramified": ["0", "infinity"], "B1_root": "1"},
        "kernel_coordinates": ["d0", "d1", "d2", "beta"],
        "A2": "d0+d1 W+d2 W^2",
        "B1": "beta(W-1)",
        "A0": "-a0^2 d0+[(a0^2-a1^2)d0-a1^2 d1+(ainfinity^2-a1^2)d2]W-ainfinity^2 d2 W^2",
        "role_orbits": {
            profile: [[list(assignment) for assignment in orbit] for orbit in orbits]
            for profile, orbits in role_orbits.items()
        },
        "placement_count": len(replay),
        "placements": replay,
    }


PLACEMENT_COLORED_ENDPOINTS = {
    "442_root_low": ("c", "c"),
    "442_root_high": ("b", "b"),
    "433_root_low": ("b", "c"),
    "433_root_high": ("1", "b"),
}


def sign_orbits():
    unseen = set(itertools.product((1, -1), repeat=3))
    orbits = []
    while unseen:
        representative = min(unseen)
        orbit = {
            (
                representative[0] * flip_e,
                representative[1] * flip_f,
                representative[2] * flip_e * flip_f,
            )
            for flip_e, flip_f in itertools.product((1, -1), repeat=2)
        }
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    return tuple(sorted(orbits))


def signed_edges(placement: str, cycle_sign: int):
    left, right = PLACEMENT_COLORED_ENDPOINTS[placement]
    return (
        (left, "e", 1, "colored-left"),
        (right, "f", 1, "colored-right"),
        ("d", "e", 1, "internal-de-plus"),
        ("d", "e", -1, "internal-de-minus"),
        ("d", "f", 1, "internal-df-plus"),
        ("d", "f", -1, "internal-df-minus"),
        ("e", "f", cycle_sign, "internal-ef-cycle"),
    )


def signed_vieta_replay() -> dict[str, Any]:
    orbits = sign_orbits()
    invariants = sorted(
        representative[0] * representative[1] * representative[2]
        for representative, *_ in orbits
    )
    require(len(orbits) == 2 and invariants == [-1, 1], "sign quotient")
    symbols = {name: sp.Symbol(name) for name in ("b", "c", "d", "e", "f")}
    symbols["1"] = sp.Integer(1)
    lanes = {}
    for placement in PLACEMENT_COLORED_ENDPOINTS:
        for cycle_sign in (-1, 1):
            records = []
            for left, right, edge_sign, label in signed_edges(placement, cycle_sign):
                product = sp.expand(edge_sign * symbols[left] * symbols[right])
                squared_sum = sp.expand(
                    symbols[left] ** 2
                    + symbols[right] ** 2
                    + 2 * product
                )
                records.append({
                    "label": label,
                    "product": str(product),
                    "squared_sum": str(squared_sum),
                })
            require(len(records) == 7, f"{placement} lane size")
            lanes[f"{placement}:sigma={cycle_sign:+d}"] = records
    require(len(lanes) == 8, "signed lane count")

    a0, ai, a1, d0, d1, d2, beta, p, s, z, w = sp.symbols(
        "a0 ai a1 d0 d1 d2 beta p s z w"
    )
    denominator = d0 + d1 * w + d2 * w**2
    middle = (
        (a0**2 - a1**2) * d0
        - a1**2 * d1
        + (ai**2 - a1**2) * d2
    )
    numerator = -a0**2 * d0 + middle * w - ai**2 * d2 * w**2
    product_polynomial = sp.expand(numerator - p * denominator)
    sum_polynomial = sp.expand(beta**2 * w * (w - 1)**2 - s**2 * denominator**2)
    direct = z * beta * (z**2 - 1) + s * denominator.subs(w, z**2)
    conjugate = -z * beta * (z**2 - 1) + s * denominator.subs(w, z**2)
    require(sp.expand(direct * conjugate + sum_polynomial.subs(w, z**2)) == 0,
            "square-root-free sum equation")
    require(sp.degree(product_polynomial, w) <= 2, "product polynomial degree")
    require(sp.degree(sum_polynomial, w) <= 4, "sum polynomial degree")
    return {
        "raw_sign_assignments": 8,
        "sign_orbit_count": 2,
        "cycle_sign_invariants": invariants,
        "placement_count": len(PLACEMENT_COLORED_ENDPOINTS),
        "lane_count": len(lanes),
        "edges_per_lane": 7,
        "edge_record_count": sum(len(records) for records in lanes.values()),
        "outside_skeleton": "colored ae,a'f; internal de,-de,df,-df,sigma ef",
        "lanes": lanes,
        "edge_equations": {
            "P": "E(w)-pD(w)=0",
            "Q": "beta^2 w(w-1)^2-squared_sum D(w)^2=0",
            "P_max_degree": 2,
            "Q_max_degree": 4,
        },
        "saturation": [
            "beta",
            "D(w_i)",
            "w_i(w_i-1)(w_i-x^2)(w_i-y^2)",
            "all w_i-w_j",
            "all signed-target square-collision factors",
        ],
    }


def edge_eliminant_replay() -> dict[str, Any]:
    A, B, C, w = sp.symbols("A B C w")
    q0, q1, q2, q3, q4 = sp.symbols("q0:5")
    coefficients = (q0, q1, q2, q3, q4)
    polynomial = A * w**2 + B * w + C
    quartic = sum(coefficients[index] * w**index for index in range(5))
    r1 = (
        q4 * (-B**3 + 2 * A * B * C)
        + q3 * A * (B**2 - A * C)
        - q2 * A**2 * B
        + q1 * A**3
    )
    r0 = (
        q4 * (-B**2 * C + A * C**2)
        + q3 * A * B * C
        - q2 * A**2 * C
        + q0 * A**3
    )
    numerator = sp.expand(A * r0**2 - B * r0 * r1 + C * r1**2)
    quotient, remainder = sp.div(numerator, A**3)
    require(remainder == 0, "generic A^3 divisibility")
    resultant = sp.expand(sp.resultant(polynomial, quartic, w))
    require(sp.expand(quotient - resultant) == 0, "generic resultant identity")
    require(sp.expand(sp.rem(A**3 * quartic, polynomial, w) - r1 * w - r0) == 0,
            "generic pseudo-remainder")
    linear = sp.expand(
        q4 * C**4 - q3 * C**3 * B + q2 * C**2 * B**2
        - q1 * C * B**3 + q0 * B**4
    )
    require(sp.expand(B**4 * quartic.subs(w, -C / B) - linear) == 0,
            "linear degree-drop identity")

    a0, ai, a1, d0, d1, d2, beta, p, s2 = sp.symbols(
        "a0 ai a1 d0 d1 d2 beta p s2"
    )
    middle = (
        (a0**2 - a1**2) * d0
        - a1**2 * d1
        + (ai**2 - a1**2) * d2
    )
    edge_A = -(ai**2 + p) * d2
    edge_B = middle - p * d1
    edge_C = -(a0**2 + p) * d0
    edge_q = (
        -s2 * d0**2,
        beta**2 - 2 * s2 * d0 * d1,
        -2 * beta**2 - s2 * (d1**2 + 2 * d0 * d2),
        beta**2 - 2 * s2 * d1 * d2,
        -s2 * d2**2,
    )
    denominator = d0 + d1 * w + d2 * w**2
    edge_numerator = -a0**2 * d0 + middle * w - ai**2 * d2 * w**2
    require(
        sp.expand(edge_A * w**2 + edge_B * w + edge_C
                  - (edge_numerator - p * denominator)) == 0,
        "edge P coefficients",
    )
    require(
        sp.expand(sum(edge_q[index] * w**index for index in range(5))
                  - (beta**2 * w * (w - 1)**2 - s2 * denominator**2)) == 0,
        "edge Q coefficients",
    )
    variables = (A, B, C, q0, q1, q2, q3, q4)
    require(len(sp.Poly(resultant, *variables).terms()) == 22,
            "generic resultant term count")
    require(sp.total_degree(resultant) == 6, "generic resultant degree")
    require(sp.total_degree(linear) == 5, "linear eliminant degree")
    return {
        "P_coefficients": {
            "A": "-(ainfinity^2+p)d2",
            "B": "(a0^2-a1^2)d0-a1^2d1+(ainfinity^2-a1^2)d2-pd1",
            "C": "-(a0^2+p)d0",
        },
        "Q_coefficients": [
            "-squared_sum*d0^2",
            "beta^2-2*squared_sum*d0*d1",
            "-2*beta^2-squared_sum*(d1^2+2*d0*d2)",
            "beta^2-2*squared_sum*d1*d2",
            "-squared_sum*d2^2",
        ],
        "generic": {
            "condition": "A!=0",
            "identity": "A^3 Res(P,Q)=A R0^2-B R0 R1+C R1^2",
            "resultant_term_count": 22,
            "resultant_total_degree": 6,
            "resultant_digest": polynomial_digest(resultant, variables),
        },
        "degree_drop": {
            "condition": "A=0 iff p=-ainfinity^2; B!=0",
            "root": "w=-C/B",
            "linear_cut": "q4*C^4-q3*C^3*B+q2*C^2*B^2-q1*C*B^3+q0*B^4",
            "linear_total_degree": 5,
            "constant_subbranch": "A=B=0 implies C!=0 under collision guards, so no edge",
        },
        "resultant_is_only_necessary_before_saturation": True,
    }


def local_order(polynomial, variable) -> int:
    terms = sp.Poly(sp.expand(polynomial), variable).terms()
    return min(monomial[0] for monomial, coefficient in terms if coefficient)


def ramified_loop_multiplicity_replay() -> dict[str, Any]:
    u, a, t = sp.symbols("u a t")
    d0, d1, d2, e1, e2, c0, c1 = sp.symbols(
        "d0 d1 d2 e1 e2 c0 c1"
    )
    w = u**2
    denominator = d0 + d1 * w + d2 * w**2
    numerator = -a**2 * d0 + e1 * w + e2 * w**2
    odd = c0 + c1 * w
    row_plus = sp.expand(a**2 * denominator + numerator + a * u * odd)
    row_minus = sp.expand(a**2 * denominator + numerator - a * u * odd)
    row_other = sp.expand(t**2 * denominator + numerator + t * u * odd)
    require(sp.Poly(row_plus, u).coeff_monomial(u) == a * c0,
            "positive ramified tangent")
    require(sp.Poly(row_minus, u).coeff_monomial(u) == -a * c0,
            "negative ramified tangent")
    require(sp.expand(row_other.subs(u, 0) - d0 * (t**2 - a**2)) == 0,
            "other target branch unit")

    targets = tuple(range(-6, 0)) + tuple(range(1, 7))
    charts = (
        (1, 2 + 3 * u**2 + 5 * u**4, -2 + 13 * u**2 + 17 * u**4,
         u * (7 + 11 * u**2)),
        (2, 5 + 3 * u**2 + 2 * u**4, -20 + 17 * u**2 + 13 * u**4,
         u * (11 + 7 * u**2)),
    )
    orders = []
    for loop_target, d_value, e_value, odd_value in charts:
        product = sp.prod(
            target**2 * d_value + e_value + target * odd_value
            for target in targets
        )
        observed = local_order(product, u)
        required = local_order((u**2 * (1 + u)) ** 2, u)
        require((observed, required) == (2, 4), "ramified local-order mismatch")
        orders.append([observed, required])

    placements = []
    slots = ("ramified_zero", "ramified_infinity", "ordinary")
    for loop_count in (2, 3):
        for loops in itertools.combinations(slots, loop_count):
            branches = [slot for slot in loops if slot.startswith("ramified_")]
            require(branches, "multi-loop ramification")
            if "ordinary" in loops:
                b1_zero = "ordinary"
                live_branch = branches[0]
            else:
                b1_zero = "ramified_zero"
                live_branch = "ramified_infinity"
            require(live_branch in loops and live_branch != b1_zero,
                    "nonzero B1 branch loop")
            placements.append({
                "loops": list(loops),
                "B1_zero": b1_zero,
                "excluded_branch": live_branch,
            })
    require(len(placements) == 4, "multi-loop placement coverage")

    # At an ordinary source lift x!=0, an antipodal root pair has sum zero.
    # The T-linear coefficient of the positive normal form is x*B1, so the
    # ordinary Vieta row forces B1=0 there as well.
    ordinary_t, ordinary_x, ordinary_b1, ordinary_a2, ordinary_a0 = sp.symbols(
        "ordinary_t ordinary_x ordinary_b1 ordinary_a2 ordinary_a0"
    )
    ordinary_h = (
        ordinary_a2 * ordinary_t**2
        + ordinary_x * ordinary_b1 * ordinary_t
        + ordinary_a0
    )
    require(
        sp.Poly(ordinary_h, ordinary_t).coeff_monomial(ordinary_t)
        == ordinary_x * ordinary_b1,
        "ordinary loop Vieta coefficient",
    )
    return {
        "local_hypotheses": [
            "ramified antipodal star {a,-a}",
            "A2(branch)*a*B1(branch)!=0",
            "other signed target squares differ from a^2",
        ],
        "ordinary_resultant_local_order": 2,
        "complete_source_square_local_order": 4,
        "branch_chart_orders": orders,
        "multi_loop_placement_count": len(placements),
        "multi_loop_placements": placements,
        "deleted_common_loop_counts": [2, 3],
        "maximum_positive_common_loop_count": 1,
        "ordinary_loop_vieta_coefficient": "x*B1",
        "ordinary_loop_requires_B1_zero": True,
        "ramified_one_loop_requires_B1_zero": True,
        "maximum_positive_total_loop_count": 1,
        "outside_allowance_with_zero_common_loops": 1,
        "outside_allowance_with_one_common_loop": 0,
    }


def expected_certificate() -> dict[str, Any]:
    common_census = common_loop_census()
    data = {
        "schema": "kb-mca-v4-m2-r4-coordinate-positive-three-loop-atlas-v1",
        "parents": {
            "source_facet": SOURCE_FACET_PARENT,
            "coefficient_compiler": COEFFICIENT_PARENT,
        },
        "scope": {
            "workboard_item": "K3",
            "row": "KoalaBear MCA at 2^-128",
            "inner_degree": 2,
            "outer_subdegree": 4,
            "stabilizer_order": 2,
            "orientation": "coordinate",
            "source_parity": "positive",
            "common_pair_degree_profiles": [[4, 4, 2], [4, 3, 3]],
            "subcase": "positive coordinate loop census and residual graph workboard, with the three-loop atlas retained",
        },
        "loop_ramification_and_census": {
            "antipodal_target_type_repeats": False,
            "B1_nonzero": True,
            "maximum_nonramified_loop_count": 1,
            "three_loop_locations": ["ramified_zero", "ramified_infinity", "B1_root"],
            "all_profile_orbits": common_census,
            "total_labeled_skeletons": 13,
            "total_skeleton_orbits": 10,
            "three_loop_profile_count": 2,
        },
        "complete_outside_graph": outside_skeleton_census(),
        "common_kernel_and_placement_atlas": common_kernel_replay(),
        "signed_outside_vieta_atlas": signed_vieta_replay(),
        "outside_edge_eliminant": edge_eliminant_replay(),
        "ramified_loop_multiplicity_exclusion": ramified_loop_multiplicity_replay(),
        "positive_residual_loop_workboard": residual_loop_workboard(common_census),
        "conclusion": {
            "positive_two_loop_subcase_deleted": True,
            "positive_three_loop_subcase_deleted": True,
            "coordinate_positive_orientation_deleted": False,
            "order_two_type_deleted": False,
            "k3_status": "OPEN",
            "koalabear_row_status": "OPEN",
            "terminal": "M2_R4_COORDINATE_POSITIVE_GLOBAL_LOOP_CAP_AND_RESIDUAL_WORKBOARD",
        },
        "nonclaims": [
            "the eight-lane atlas is retained but no lane saturation is needed for the deletion",
            "no ordinary source-root norm is identified with divisor-weighted ramified incidence",
            "the thirteen residual graph routes remain only necessary, not algebraically realized",
            "no negative-parity, diagonal, or trivial-stabilizer conclusion",
            "no order-two type, K3, KoalaBear row, owner, payment, or Prize close",
        ],
    }
    data["payload_sha256"] = payload_hash(data)
    return data


def verify_data(data: dict[str, Any]) -> None:
    require(payload_hash(data) == data.get("payload_sha256"), "certificate seal")
    require(data == expected_certificate(), "certificate content")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda x: x["scope"].__setitem__("source_parity", "negative"),
        lambda x: x["scope"].__setitem__("common_pair_degree_profiles", [[4, 4, 2]]),
        lambda x: x["loop_ramification_and_census"].__setitem__("B1_nonzero", False),
        lambda x: x["loop_ramification_and_census"].__setitem__("maximum_nonramified_loop_count", 2),
        lambda x: x["loop_ramification_and_census"].__setitem__("total_skeleton_orbits", 9),
        lambda x: x["complete_outside_graph"].__setitem__("component_defect_budget", 4),
        lambda x: x["complete_outside_graph"]["survivor"].__setitem__("multiplicities", [3, 1, 1]),
        lambda x: x["common_kernel_and_placement_atlas"].__setitem__("placement_count", 3),
        lambda x: x["common_kernel_and_placement_atlas"]["placements"]["442_root_low"].__setitem__("residual_total_degree", 5),
        lambda x: x["common_kernel_and_placement_atlas"]["placements"]["433_root_high"].__setitem__("residual_digest", "0" * 64),
        lambda x: x["signed_outside_vieta_atlas"].__setitem__("sign_orbit_count", 3),
        lambda x: x["signed_outside_vieta_atlas"].__setitem__("lane_count", 7),
        lambda x: x["signed_outside_vieta_atlas"].__setitem__("edge_record_count", 55),
        lambda x: x["signed_outside_vieta_atlas"]["edge_equations"].__setitem__("Q_max_degree", 5),
        lambda x: x["signed_outside_vieta_atlas"].__setitem__("saturation", ["beta"]),
        lambda x: x["outside_edge_eliminant"]["generic"].__setitem__("resultant_term_count", 21),
        lambda x: x["outside_edge_eliminant"]["generic"].__setitem__("resultant_digest", "0" * 64),
        lambda x: x["outside_edge_eliminant"]["degree_drop"].__setitem__("root", "w=C/B"),
        lambda x: x["outside_edge_eliminant"].__setitem__("resultant_is_only_necessary_before_saturation", False),
        lambda x: x["ramified_loop_multiplicity_exclusion"].__setitem__("ordinary_resultant_local_order", 4),
        lambda x: x["ramified_loop_multiplicity_exclusion"].__setitem__("multi_loop_placement_count", 3),
        lambda x: x["ramified_loop_multiplicity_exclusion"].__setitem__("maximum_positive_common_loop_count", 2),
        lambda x: x["ramified_loop_multiplicity_exclusion"].__setitem__("maximum_positive_total_loop_count", 2),
        lambda x: x["ramified_loop_multiplicity_exclusion"].__setitem__("ordinary_loop_requires_B1_zero", False),
        lambda x: x["positive_residual_loop_workboard"].__setitem__("live_common_orbit_count", 6),
        lambda x: x["positive_residual_loop_workboard"].__setitem__("representative_route_count", 12),
        lambda x: x["positive_residual_loop_workboard"]["routes"].__setitem__("433-1a", ["O0a", "O0b"]),
        lambda x: x["conclusion"].__setitem__("positive_two_loop_subcase_deleted", False),
        lambda x: x["conclusion"].__setitem__("positive_three_loop_subcase_deleted", False),
        lambda x: x["conclusion"].__setitem__("order_two_type_deleted", True),
        lambda x: x["conclusion"].__setitem__("k3_status", "CLOSED"),
        lambda x: x["parents"]["source_facet"].__setitem__("certificate_payload_sha256", "0" * 64),
        lambda x: x["parents"]["coefficient_compiler"].__setitem__("commit", "0" * 40),
        lambda x: x.__setitem__("payload_sha256", "0" * 64),
    ]
    rejected = 0
    for mutation in mutations:
        hostile = copy.deepcopy(data)
        mutation(hostile)
        try:
            verify_data(hostile)
        except VerificationError:
            rejected += 1
    require(rejected == len(mutations), "tamper self-test")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    load_parents()
    expected = expected_certificate()
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(json.dumps(expected, indent=2, sort_keys=True) + "\n")
    if args.check or not args.write:
        require(CERTIFICATE.is_file(), "missing certificate")
        data = parse_json(CERTIFICATE.read_text(), str(CERTIFICATE))
        verify_data(data)
    else:
        data = expected
    rejected = tamper_selftest(data) if args.tamper_selftest else 0
    print(
        "KB_MCA_V4_M2_R4_COORDINATE_POSITIVE_THREE_LOOP_ATLAS_PASS "
        f"skeleton_orbits={data['loop_ramification_and_census']['total_skeleton_orbits']} "
        f"placements={data['common_kernel_and_placement_atlas']['placement_count']} "
        f"lanes={data['signed_outside_vieta_atlas']['lane_count']} "
        f"edge_records={data['signed_outside_vieta_atlas']['edge_record_count']} "
        f"local_orders={data['ramified_loop_multiplicity_exclusion']['ordinary_resultant_local_order']}/"
        f"{data['ramified_loop_multiplicity_exclusion']['complete_source_square_local_order']} "
        f"deleted_loops={','.join(str(value) for value in data['ramified_loop_multiplicity_exclusion']['deleted_common_loop_counts'])} "
        f"total_loop_cap={data['ramified_loop_multiplicity_exclusion']['maximum_positive_total_loop_count']} "
        f"residual_routes={data['positive_residual_loop_workboard']['representative_route_count']} "
        f"tamper_rejected={rejected}"
    )


if __name__ == "__main__":
    main()
