#!/usr/bin/env python3
"""Fail-closed verifier for the 36-cell aligned-positive q-slice atlas.

The Sage compiler is the symbolic source of the polynomial hashes.  This
independent Python replay validates the registry and scope and recomputes all
36 source reconstructions at two exact rational fixtures.  No floating-point
arithmetic, random sampling, Groebner basis, or covariance shortcut is used.
"""

from __future__ import annotations

import argparse
import copy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "data/certificates/kb-mca-v4-m2-aligned-positive-qslice-atlas-v1"
    / "kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.json"
)
SCHEMA = "kb-mca-v4-m2-aligned-positive-qslice-atlas-v1"
PARENT = "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc"

VERTICES = {
    "v0": Fraction(2),
    "v1": Fraction(1, 2),
    "v2": "b",
    "v3": "b^-1",
}
EDGES = {
    "E01": ("v0", "v1"),
    "E02": ("v0", "v2"),
    "E03": ("v0", "v3"),
    "E12": ("v1", "v2"),
    "E13": ("v1", "v3"),
    "E23": ("v2", "v3"),
}
ASSIGNMENTS = {
    "F00": ("E01", "E02"),
    "F01": ("E01", "E03"),
    "F02": ("E01", "E12"),
    "F03": ("E01", "E13"),
    "F04": ("E02", "E23"),
    "F05": ("E03", "E23"),
    "F06": ("E12", "E23"),
    "F07": ("E13", "E23"),
    "M00": ("E02", "E03"),
    "M01": ("E02", "E12"),
    "M02": ("E03", "E13"),
    "M03": ("E12", "E13"),
}
B_INVERSION = {
    "F00": "F01",
    "F01": "F00",
    "F02": "F03",
    "F03": "F02",
    "F04": "F05",
    "F05": "F04",
    "F06": "F07",
    "F07": "F06",
    "M00": "M00",
    "M01": "M02",
    "M02": "M01",
    "M03": "M03",
}
TARGET_MULTIPLICITY = {
    "R02": [0, 2],
    "R11": [1, 1],
    "R20": [2, 0],
}
EXPECTED_TARGETS = {
    "R02": {
        "name": "crossed",
        "multiplicity": [0, 2],
        "Qc": "W^2 + ((-2)/d)*W + 1/d^2",
        "Qd": "W^2 + ((-2)/c)*W + 1/c^2",
    },
    "R11": {
        "name": "balanced",
        "multiplicity": [1, 1],
        "Qc": "W^2 + ((-c - d)/(c*d))*W + 1/(c*d)",
        "Qd": "W^2 + ((-c - d)/(c*d))*W + 1/(c*d)",
    },
    "R20": {
        "name": "identity",
        "multiplicity": [2, 0],
        "Qc": "W^2 + ((-2)/c)*W + 1/c^2",
        "Qd": "W^2 + ((-2)/d)*W + 1/d^2",
    },
}
EXPECTED_SOURCE_RECONSTRUCTION = {
    "q": "(T-c)(T-d)",
    "q0": "c*d",
    "q1": "-(c+d)",
    "F": "q0-w",
    "G": "1-w*q0",
    "M": "q1*(1-w)",
    "V": ["F+G*W", "M*(1+W)", "G+F*W"],
    "incidence": "V(a,z)=0, z=-N_a/D_a",
    "internal_target": "((l0+s*l1)E(a,r)+(l0+r*l1)E(a,s))/(s-r)",
    "U_basis": [
        "x0+x1*W+x2*W^2",
        "x3*(1+W^2)+x4*W",
        "x2+x1*W+x0*W^2",
    ],
    "G_source": "U(T,W)^2-W*V(T,W)^2",
    "forced_divisor": "(W-w)^2",
    "projective_target_pivot": "monic W^2 coefficient",
}
EXPECTED_LOCALIZER_POLICY = {
    "whole_line_normalization": True,
    "never_normalize_projective_coefficients_independently": True,
    "b_nonzero_chart_unit": True,
    "incidence_D_a_nonzero": True,
    "reconstruction_determinant_nonzero": True,
    "all_dropped_factors_require_named_parent_provenance": True,
    "generic_saturation_used": False,
    "groebner_search_used": False,
}
EXPECTED_EQUATION_HASH_DIGEST = (
    "9000ce461c3cdada584c61d381f6af845a4b44e20513ca6a2d9fe2bb5ef43e56"
)
EXPECTED_DENOMINATOR_HASH_DIGEST = (
    "cd9ecfc3f135b65c4c7e3aa1ff2cc6bf3827f8b232f757cbd8efe221a6397887"
)
EXPECTED_LOCALIZER_HASH_DIGEST = (
    "ca2def0d8c0443e892a63be3a4938dcdbac8a896faf52aed096b751a354d0f12"
)
EXPECTED_QUOTIENT_DIGEST = (
    "b567cd11280de5741ebdfd3711eef3da4ec3276d92d950eafabc836f9aedd8c9"
)
CLASSIFICATION_ORDER = [
    "DIRECT_SYSTEM_GENERATED",
    "LITERAL_SYMMETRY_AUDITED",
    "EXTERNAL_PROVENANCE_ANNOTATED_NOT_IMPORTED",
    "UNCLASSIFIED_QSLICE_GENERATED",
]
REJECTED_GLOBALIZATIONS = [
    "ENDPOINT_ONLY_MOBIUS_ORBIT",
    "DIAGONAL_W_MOBIUS_ORBIT",
    "FULL_SOURCE_SYSTEM_COVARIANCE",
]
EXPECTED_EXTERNAL_CELLS = {"F00-R02", "F00-R11", "F00-R20", "M00-R11"}
EXPECTED_EXTERNAL_PROVENANCE = {
    "F00-R02": (
        1135,
        "f0a1d20ea16721d9596a3520658406528f5ade9f",
        "31cddc835ed2e896aa1d94a953ea8518362628c8",
        "6953466a26b6f8bd80889cc6d69eca9c6866678f7cd6432308af58f8c25ecb10",
        "ec52873035a42fec4c3f19f429913197df872487c2a6137646dd81474c6fedf7",
        "EXTERNAL_PROVEN_REPRESENTATIVE_ONLY",
    ),
    "F00-R20": (
        1136,
        "9f5b7ffa8759f0372802792bc5baf589410cdd28",
        "1e083a5cac1bba0827ae2c6c9e72ffd9da03d3ba",
        "f4572ea4eeb082fa80fbbd531222ad128e5c017f61f04b08ab4f15644bb8efe3",
        "ce59e2be2417dd8681bce65d7f0d838850445dfccbd82d68c137387510ea7cb5",
        "EXTERNAL_PROVEN_REPRESENTATIVE_ONLY",
    ),
    "F00-R11": (
        1137,
        "272c185ef2f64e15283947aa62ed045ce29d2059",
        "177b3f49c4248eec471d8fef39c69a66493fb020",
        "9965c2cab06c145343413066427a81f66adad263eb856218e613d1893063868c",
        "a9e67b5cb40c0731f504636f06e2e99c9147b76e1d27dfee2b9d6855e9dca471",
        "EXTERNAL_PROVEN_REPRESENTATIVE_ONLY",
    ),
    "M00-R11": (
        1138,
        "cd41c6c71b5b7d114f4ca9b2f5c853ccdd3c341d",
        "f73d6a7841aec868f4e7788a688afbd9cffa117e",
        "5a42a8567a140b47b3aadbd77fead308298b7582a9bb4383e42dde0d54531566",
        "3f32af654c6527e97c036d09a07c1d5554923c484300d5c3141fd997cc3a7a05",
        "EXTERNAL_PROVEN_CANONICAL_REPRESENTATIVE_GREEN",
    ),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_sha(data: dict[str, Any]) -> str:
    copy_data = dict(data)
    copy_data.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(copy_data).encode()).hexdigest()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def trim(poly: list[Fraction]) -> list[Fraction]:
    result = list(poly)
    while len(result) > 1 and not result[-1]:
        result.pop()
    return result


def add(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return trim(
        [
            (left[index] if index < len(left) else Fraction(0))
            + (right[index] if index < len(right) else Fraction(0))
            for index in range(max(len(left), len(right)))
        ]
    )


def scale(poly: list[Fraction], scalar: Fraction) -> list[Fraction]:
    return trim([scalar * value for value in poly])


def multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, left_value in enumerate(left):
        for j, right_value in enumerate(right):
            result[i + j] += left_value * right_value
    return trim(result)


def divide_exact(
    dividend: list[Fraction], divisor: list[Fraction]
) -> list[Fraction]:
    work = trim(dividend)
    divisor = trim(divisor)
    require(divisor != [0], "zero polynomial divisor")
    quotient = [Fraction(0)] * max(1, len(work) - len(divisor) + 1)
    while len(work) >= len(divisor) and work != [0]:
        shift = len(work) - len(divisor)
        coefficient = work[-1] / divisor[-1]
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[index + shift] -= coefficient * value
        work = trim(work)
    require(work == [0], "forced-square division remainder")
    return trim(quotient)


def evaluate(poly: list[Fraction], point: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in reversed(poly):
        value = value * point + coefficient
    return value


def vertex_values(b: Fraction) -> dict[str, Fraction]:
    return {
        "v0": Fraction(2),
        "v1": Fraction(1, 2),
        "v2": b,
        "v3": 1 / b,
    }


def edge_vector(
    edge_id: str, values: dict[str, Fraction]
) -> tuple[Fraction, Fraction, Fraction]:
    left_id, right_id = EDGES[edge_id]
    left, right = values[left_id], values[right_id]
    return left * right, -(left + right), Fraction(1)


def target_coefficients(
    target_id: str, root_side: str, c: Fraction, d: Fraction
) -> list[Fraction]:
    if target_id == "R02":
        root = d if root_side == "c" else c
        return [1 / root**2, -2 / root, Fraction(1)]
    if target_id == "R11":
        return [1 / (c * d), -(c + d) / (c * d), Fraction(1)]
    require(target_id == "R20", "unknown target")
    root = c if root_side == "c" else d
    return [1 / root**2, -2 / root, Fraction(1)]


def exact_cell_values(
    assignment_id: str,
    target_id: str,
    fixture: dict[str, Any],
) -> list[str]:
    b = Fraction(fixture["b"])
    c = Fraction(fixture["c"])
    d = Fraction(fixture["d"])
    w = Fraction(fixture["w"])
    values = vertex_values(b)
    first_id, second_id = ASSIGNMENTS[assignment_id]
    first_vertices = set(EDGES[first_id])
    second_vertices = set(EDGES[second_id])
    common_ids = first_vertices & second_vertices
    require(len(common_ids) == 1, f"{assignment_id} common vertex")
    common_id = next(iter(common_ids))
    right_id = next(iter(first_vertices - {common_id}))
    left_id = next(iter(second_vertices - {common_id}))
    common = values[common_id]
    right = values[right_id]
    left = values[left_id]
    first = edge_vector(first_id, values)
    second = edge_vector(second_id, values)

    q0 = c * d
    q1 = -(c + d)
    f = q0 - w
    g = 1 - w * q0
    m = q1 * (1 - w)
    v = ([f, g], [m, m], [g, f])
    incidence = [
        sum(common**index * v[index][coefficient] for index in range(3))
        for coefficient in range(2)
    ]
    require(incidence[1] != 0, f"{assignment_id} fixture incidence denominator")
    z = -incidence[0] / incidence[1]
    vz = [evaluate(list(component), z) for component in v]
    require(
        vz[0] + common * vz[1] + common**2 * vz[2] == 0,
        f"{assignment_id} incidence identity",
    )
    linear_1 = vz[2]
    linear_0 = vz[1] + common * vz[2]
    denominator = left - right
    require(denominator != 0, f"{assignment_id} distinct internal stars")
    internal_target = tuple(
        (
            (linear_0 + left * linear_1) * first[index]
            + (linear_0 + right * linear_1) * second[index]
        )
        / denominator
        for index in range(3)
    )

    target_0, target_1, target_2 = internal_target
    require(1 - z**2 != 0, f"{assignment_id} z deck fixed")
    require(1 - q0 != 0, f"{assignment_id} reciprocal core")
    difference = (target_0 - target_2) / (1 - z**2)
    rhs_sum = target_0 + target_2
    rhs_source = -(
        (1 + q0) * (1 - w**2) * difference / (2 * (1 - q0))
    )
    block_det = (w - z) * (1 - w * z)
    require(block_det != 0, f"{assignment_id} forced/internal collision")
    sum_outer = (rhs_sum * w - 2 * z * rhs_source) / block_det
    x1 = ((1 + z**2) * rhs_source - (1 + w**2) * rhs_sum / 2) / block_det
    x0 = (sum_outer + difference) / 2
    x2 = (sum_outer - difference) / 2
    at_w_2 = x2 + x1 * w + x0 * w**2
    x3 = (target_1 * w - z * q1 * at_w_2) / block_det
    x4 = ((1 + z**2) * q1 * at_w_2 - (1 + w**2) * target_1) / block_det
    u = ([x0, x1, x2], [x3, x4, x3], [x2, x1, x0])

    def residual_at(root: Fraction) -> list[Fraction]:
        u_root = [Fraction(0)]
        v_root = [Fraction(0)]
        for index in range(3):
            u_root = add(u_root, scale(list(u[index]), root**index))
            v_root = add(v_root, scale(list(v[index]), root**index))
        norm = add(
            multiply(u_root, u_root),
            scale([Fraction(0)] + multiply(v_root, v_root), Fraction(-1)),
        )
        quotient = divide_exact(norm, [w**2, -2 * w, Fraction(1)])
        require(len(quotient) == 3, f"{assignment_id} residual degree")
        return quotient

    result: list[Fraction] = []
    for side, root in (("c", c), ("d", d)):
        observed = residual_at(root)
        target = target_coefficients(target_id, side, c, d)
        result.extend(
            (
                observed[0] - observed[2] * target[0],
                observed[1] - observed[2] * target[1],
            )
        )
    return [str(value) for value in result]


def validate(data: dict[str, Any]) -> None:
    require(data["schema"] == SCHEMA, "schema")
    require(data["payload_sha256"] == payload_sha(data), "payload")
    require(data["parent"]["commit"] == PARENT, "parent pin")
    require(data["scope"]["assignments"] == 12, "assignment count declaration")
    require(data["scope"]["targets_per_assignment"] == 3, "target count")
    require(data["scope"]["cells"] == 36, "cell count declaration")
    require(data["scope"]["ledger_movement"] == 0, "scope ledger movement")
    require(
        data["source_reconstruction"] == EXPECTED_SOURCE_RECONSTRUCTION,
        "source reconstruction formulas",
    )
    require(
        data["denominator_and_localizer_policy"] == EXPECTED_LOCALIZER_POLICY,
        "denominator/localizer policy",
    )

    registry_assignments = {
        key: tuple(value["edges"])
        for key, value in data["registry"]["assignments"].items()
    }
    require(registry_assignments == ASSIGNMENTS, "assignment registry")
    registry_edges = {
        key: tuple(value["vertices"])
        for key, value in data["registry"]["edges"].items()
    }
    require(registry_edges == EDGES, "edge registry")
    require(data["registry"]["targets"] == EXPECTED_TARGETS, "target registry")
    require(
        sum(value["kind"] == "fixed-moving" for value in data["assignments"])
        == 8,
        "fixed-moving count",
    )
    require(
        sum(value["kind"] == "moving-moving" for value in data["assignments"])
        == 4,
        "moving-moving count",
    )

    assignment_rows = {
        row["assignment_id"]: row for row in data["assignments"]
    }
    require(set(assignment_rows) == set(ASSIGNMENTS), "assignment rows")
    require(len(data["assignments"]) == len(assignment_rows), "duplicate assignment")
    for assignment_id, edges in ASSIGNMENTS.items():
        row = assignment_rows[assignment_id]
        require(
            (row["first_edge"], row["second_edge"]) == edges,
            f"{assignment_id} edge order",
        )
        common = set(EDGES[edges[0]]) & set(EDGES[edges[1]])
        require(common == {row["common_vertex"]}, f"{assignment_id} common")
        require(
            row["b_inversion_partner"] == B_INVERSION[assignment_id],
            f"{assignment_id} b inversion",
        )
        require(
            row["incidence"]["D_a_nonzero_source"]
            == "parent finite internal-label chart and J0/J1 disjointness",
            f"{assignment_id} incidence provenance",
        )
        require(
            set(row["reconstruction"]["named_units"])
            == {
                "z_not_deck_fixed",
                "core_not_reciprocal",
                "forced_internal_orbits_distinct",
            },
            f"{assignment_id} reconstruction units",
        )
        assignment_localizer = row["assignment_localizer"]
        require(
            assignment_localizer["formed_before_any_symmetry_reuse"] is True,
            f"{assignment_id} localizer chronology",
        )
        require(
            assignment_localizer["radical_factor_count"]
            == len(assignment_localizer["radical_factors"]),
            f"{assignment_id} localizer factor count",
        )
        require(
            assignment_localizer["radical_total_degree"]
            == sum(
                factor["degree"]
                for factor in assignment_localizer["radical_factors"]
            ),
            f"{assignment_id} localizer degree",
        )
        require(
            len(assignment_localizer["radical_factor_set_sha256"]) == 64,
            f"{assignment_id} localizer hash",
        )
        require(
            row["star_swap"]
            == {
                "target_changes_by_global_sign": True,
                "source_U_changes_by_global_sign": True,
                "G_unchanged": True,
            },
            f"{assignment_id} star swap",
        )

    require(data["classification_order"] == CLASSIFICATION_ORDER, "owner order")
    require(
        data["rejected_globalizations"] == REJECTED_GLOBALIZATIONS,
        "covariance rejection",
    )
    require(
        data["denominator_and_localizer_policy"]["whole_line_normalization"]
        is True,
        "whole-line policy",
    )
    require(
        data["denominator_and_localizer_policy"][
            "never_normalize_projective_coefficients_independently"
        ]
        is True,
        "independent normalization rejection",
    )
    require(
        data["denominator_and_localizer_policy"]["b_nonzero_chart_unit"] is True,
        "b nonzero chart unit",
    )
    require(
        data["denominator_and_localizer_policy"]["incidence_D_a_nonzero"] is True,
        "incidence denominator policy",
    )
    require(
        data["denominator_and_localizer_policy"][
            "reconstruction_determinant_nonzero"
        ]
        is True,
        "reconstruction denominator policy",
    )
    require(
        data["denominator_and_localizer_policy"]["generic_saturation_used"]
        is False,
        "generic saturation",
    )
    require(
        data["denominator_and_localizer_policy"]["groebner_search_used"]
        is False,
        "Groebner search",
    )

    cells = data["cells"]
    cell_ids = [cell["cell_id"] for cell in cells]
    expected_cells = {
        f"{assignment_id}-{target_id}"
        for assignment_id in ASSIGNMENTS
        for target_id in TARGET_MULTIPLICITY
    }
    require(len(cells) == 36, "cell length")
    require(len(set(cell_ids)) == 36, "duplicate cell")
    require(set(cell_ids) == expected_cells, "missing cell")
    fixtures = data["exact_rational_fixtures"]
    require([fixture["id"] for fixture in fixtures] == ["Q0", "Q1"], "fixtures")
    external_cells = set()
    for cell in cells:
        cell_id = cell["cell_id"]
        assignment_id, target_id = cell_id.split("-")
        require(cell["assignment_id"] == assignment_id, f"{cell_id} assignment")
        require(cell["target_id"] == target_id, f"{cell_id} target")
        require(
            cell["classification"] == "UNCLASSIFIED_QSLICE_GENERATED",
            f"{cell_id} classification",
        )
        require(cell["ledger_movement"] == 0, f"{cell_id} ledger")
        require(cell["c_d_companion_exact"] is True, f"{cell_id} companion")
        require(len(cell["equations"]) == 4, f"{cell_id} equations")
        require(
            cell["equation_order"]
            == ["c_constant", "c_linear", "d_constant", "d_linear"],
            f"{cell_id} equation order",
        )
        require(len(cell["line_normalization"]) == 4, f"{cell_id} normalization")
        for record in cell["line_normalization"]:
            require(
                record["mode"] == "WHOLE_PROJECTIVE_LINE_SINGLE_SCALAR",
                f"{cell_id} whole line",
            )
            require("denominator" in record, f"{cell_id} denominator record")
            require(
                len(record["denominator"]["sha256"]) == 64,
                f"{cell_id} denominator hash",
            )
        localizer = cell["cell_localizer"]
        require(
            localizer["radical_factor_count"]
            == len(localizer["radical_factors"]),
            f"{cell_id} localizer factor count",
        )
        require(
            localizer["radical_total_degree"]
            == sum(factor["degree"] for factor in localizer["radical_factors"]),
            f"{cell_id} localizer degree",
        )
        require(
            len(localizer["radical_factor_set_sha256"]) == 64,
            f"{cell_id} localizer hash",
        )
        require(
            localizer["provenance"]
            == [
                "b nonzero chart",
                "finite incidence denominator",
                "distinct internal stars",
                "positive reconstruction units",
                "four complete projective-line denominators",
            ],
            f"{cell_id} localizer provenance",
        )
        fixture_records = {
            record["fixture_id"]: record["values"]
            for record in cell["exact_rational_fixture_values"]
        }
        require(set(fixture_records) == {"Q0", "Q1"}, f"{cell_id} fixture rows")
        for fixture in fixtures:
            require(
                fixture_records[fixture["id"]]
                == exact_cell_values(assignment_id, target_id, fixture),
                f"{cell_id} exact fixture {fixture['id']}",
            )
        provenance = cell["external_provenance"]
        if provenance is not None:
            external_cells.add(cell_id)
            require(provenance["scope_imported"] is False, f"{cell_id} import")
            require(len(provenance["commit"]) == 40, f"{cell_id} pin")
            require(len(provenance["certificate_blob"]) == 40, f"{cell_id} blob")
            require(
                len(provenance["external_payload_sha256"]) == 64,
                f"{cell_id} external payload",
            )
            require(
                (
                    provenance["pull_request"],
                    provenance["commit"],
                    provenance["certificate_blob"],
                    provenance["certificate_sha256"],
                    provenance["external_payload_sha256"],
                    provenance["status"],
                )
                == EXPECTED_EXTERNAL_PROVENANCE[cell_id],
                f"{cell_id} exact external provenance",
            )
    require(external_cells == EXPECTED_EXTERNAL_CELLS, "external provenance cells")
    require(
        canonical_digest(
            [
                [
                    cell["cell_id"],
                    [equation["sha256"] for equation in cell["equations"]],
                ]
                for cell in cells
            ]
        )
        == EXPECTED_EQUATION_HASH_DIGEST,
        "equation hash registry",
    )
    require(
        canonical_digest(
            [
                [
                    cell["cell_id"],
                    [
                        line["denominator"]["sha256"]
                        for line in cell["line_normalization"]
                    ],
                ]
                for cell in cells
            ]
        )
        == EXPECTED_DENOMINATOR_HASH_DIGEST,
        "denominator hash registry",
    )
    require(
        canonical_digest(
            {
                "assignments": [
                    [
                        row["assignment_id"],
                        row["assignment_localizer"][
                            "radical_factor_set_sha256"
                        ],
                        [
                            factor["sha256"]
                            for factor in row["assignment_localizer"][
                                "radical_factors"
                            ]
                        ],
                    ]
                    for row in data["assignments"]
                ],
                "cells": [
                    [
                        cell["cell_id"],
                        cell["cell_localizer"]["radical_factor_set_sha256"],
                        [
                            factor["sha256"]
                            for factor in cell["cell_localizer"][
                                "radical_factors"
                            ]
                        ],
                    ]
                    for cell in cells
                ],
            }
        )
        == EXPECTED_LOCALIZER_HASH_DIGEST,
        "radical localizer hash registry",
    )

    literal = data["literal_symmetries"]
    require(literal["star_swap_global_sign"] is True, "star swap summary")
    require(literal["c_d_companion"] is True, "companion summary")
    require(literal["b_inversion_map"] == B_INVERSION, "b inversion map")
    checks = literal["b_inversion_checks"]
    require(len(checks) == 36, "b inversion check count")
    require(
        {record["source"] for record in checks} == expected_cells,
        "b inversion sources",
    )
    for record in checks:
        source_assignment, source_target = record["source"].split("-")
        require(
            record["target"]
            == f"{B_INVERSION[source_assignment]}-{source_target}",
            f"{record['source']} b inversion target",
        )
        require(
            record["equations_exact_after_b_unit"] is True,
            f"{record['source']} equation pullback",
        )
        require(
            record["localizers_exact_after_b_unit"] is True,
            f"{record['source']} localizer pullback",
        )
    quotient = literal["fixed_assignment_quotient_coordinates"]
    require(set(quotient) == {"M00", "M03"}, "fixed quotient assignments")
    for assignment in quotient.values():
        require(set(assignment) == set(TARGET_MULTIPLICITY), "quotient targets")
        for lines in assignment.values():
            require(len(lines) == 4, "quotient line count")
            for line in lines:
                require(line["parity"] == "even", "quotient parity")
                require(
                    line["relation"] == "delta^2=y^2-4",
                    "quotient relation",
                )
                require(
                    line["reduction_order"]
                    == "clear_complete_line_then_reduce",
                    "quotient reduction order",
                )
                require("quotient_metric" in line, "quotient metric")
                require(
                    line["lift_identity"] == "cleared=b^2*Q(y,c,d,w)",
                    "quotient lift identity",
                )
    require(
        canonical_digest(quotient) == EXPECTED_QUOTIENT_DIGEST,
        "fixed quotient registry",
    )

    provenance_policy = data["external_provenance_policy"]
    require(
        provenance_policy["pins_are_annotations_only"] is True,
        "pin policy",
    )
    require(
        provenance_policy["external_scopes_imported"] is False,
        "external scope policy",
    )
    require(
        provenance_policy["invalid_or_broader_orbit_scopes_imported"] is False,
        "invalid-scope policy",
    )
    cell_rows = {cell["cell_id"]: cell for cell in cells}
    require(
        provenance_policy["pins"]
        == {
            cell_id: cell_rows[cell_id]["external_provenance"]
            for cell_id in sorted(EXPECTED_EXTERNAL_CELLS)
        },
        "policy-level external pins",
    )
    require(
        all("no " in claim for claim in data["nonclaims"]),
        "nonclaim wording",
    )


def reseal(data: dict[str, Any]) -> None:
    data["payload_sha256"] = payload_sha(data)


def expect_failure(data: dict[str, Any], mutate: Callable[[dict[str, Any]], None]) -> None:
    changed = copy.deepcopy(data)
    mutate(changed)
    reseal(changed)
    try:
        validate(changed)
    except (AssertionError, KeyError, ValueError, ZeroDivisionError):
        return
    raise AssertionError("mutation unexpectedly passed")


def tamper_selftest(data: dict[str, Any]) -> int:
    mutations: list[Callable[[dict[str, Any]], None]] = [
        lambda value: value["cells"].pop(),
        lambda value: value["cells"].append(copy.deepcopy(value["cells"][0])),
        lambda value: value["rejected_globalizations"].pop(),
        lambda value: value["denominator_and_localizer_policy"].__setitem__(
            "incidence_D_a_nonzero", False
        ),
        lambda value: value["cells"][0]["cell_localizer"][
            "radical_factors"
        ].pop(),
        lambda value: value["cells"][0]["equations"][0].__setitem__(
            "sha256", "0" * 64
        ),
        lambda value: value["cells"][0]["line_normalization"][0][
            "denominator"
        ].__setitem__("sha256", "0" * 64),
        lambda value: value["cells"][0]["cell_localizer"].__setitem__(
            "radical_factor_set_sha256", "0" * 64
        ),
        lambda value: value["cells"][0]["cell_localizer"][
            "radical_factors"
        ][0].__setitem__("sha256", "0" * 64),
        lambda value: value["source_reconstruction"]["V"].__setitem__(
            0, "CHANGED"
        ),
        lambda value: value["registry"]["targets"]["R02"].__setitem__(
            "Qc", "CHANGED"
        ),
        lambda value: value["literal_symmetries"][
            "fixed_assignment_quotient_coordinates"
        ]["M00"]["R02"][0].__setitem__("parity", "odd"),
        lambda value: value["external_provenance_policy"]["pins"]["F00-R02"].__setitem__(
            "commit", "0" * 40
        ),
        lambda value: value["external_provenance_policy"].__setitem__(
            "invalid_or_broader_orbit_scopes_imported", True
        ),
        lambda value: value["denominator_and_localizer_policy"].__setitem__(
            "all_dropped_factors_require_named_parent_provenance", False
        ),
        lambda value: value["classification_order"].reverse(),
        lambda value: value["registry"]["assignments"]["F01"].__setitem__(
            "edges", ["E01", "E02"]
        ),
        lambda value: value["registry"]["targets"]["R11"].__setitem__(
            "multiplicity", [2, 0]
        ),
        lambda value: value["cells"][0]["line_normalization"][0].__setitem__(
            "mode", "COEFFICIENTWISE"
        ),
        lambda value: value["cells"][0]["external_provenance"].__setitem__(
            "scope_imported", True
        ),
        lambda value: value["cells"][0].__setitem__("ledger_movement", 1),
        lambda value: value["cells"][0].__setitem__("classification", "EMPTY"),
        lambda value: value["cells"][0].__setitem__(
            "classification", "PAID_OWNER"
        ),
        lambda value: value["cells"][0]["external_provenance"].__setitem__(
            "commit", "0" * 40
        ),
    ]
    for mutation in mutations:
        expect_failure(data, mutation)
    changed_payload = copy.deepcopy(data)
    changed_payload["payload_sha256"] = "0" * 64
    try:
        validate(changed_payload)
    except AssertionError:
        pass
    else:
        raise AssertionError("payload mutation unexpectedly passed")
    return len(mutations) + 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if not (args.check or args.tamper_selftest):
        parser.error("choose --check and/or --tamper-selftest")
    data = json.loads(CERTIFICATE.read_text())
    if args.check:
        validate(data)
        print(
            "PASS: aligned-positive q-slice atlas "
            f"cells={len(data['cells'])} payload={data['payload_sha256']}"
        )
    if args.tamper_selftest:
        count = tamper_selftest(data)
        print(f"PASS: {count}/{count} atlas mutations rejected")


if __name__ == "__main__":
    main()
