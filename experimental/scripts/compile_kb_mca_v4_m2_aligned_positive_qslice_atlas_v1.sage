#!/usr/bin/env sage
"""Compile the complete aligned-positive diagonal (1,1,2) q-slice atlas.

This is a bounded symbolic compiler, not a Groebner search.  It rebuilds the
positive source form separately for each of the twelve compatible unordered
source-star assignments and imposes each of the three aligned residual-root
distributions.  The output is therefore 12 * 3 = 36 direct systems.

Only literal identities are used:

* swapping the two source stars negates U and leaves G=U^2-WV^2 unchanged;
* exchanging c and d exchanges the two root slices;
* b -> b^-1 gives the ten declared assignment pairings/fixed assignments.

In particular this script does not use a Mobius or diagonal-W covariance
argument and it performs no unbounded saturation or Groebner calculation.
"""

import argparse
import hashlib
import json
from pathlib import Path


PARENT_COMMIT = "c2edcfa5cbfb8a41e7dea04ae1b34325c90ed5dc"
DEPLOYED_PRIME = ZZ(2130706433)
SCHEMA = "kb-mca-v4-m2-aligned-positive-qslice-atlas-v1"
CERTIFICATE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data/certificates/kb-mca-v4-m2-aligned-positive-qslice-atlas-v1"
    / "kb_mca_v4_m2_aligned_positive_qslice_atlas_v1.json"
)


def canonical_json(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=lambda item: int(item) if item in ZZ else str(item),
    )


def sha_text(value):
    return hashlib.sha256(str(value).encode()).hexdigest()


def payload_sha(data):
    copy = dict(data)
    copy.pop("payload_sha256", None)
    return hashlib.sha256(canonical_json(copy).encode()).hexdigest()


R = PolynomialRing(QQ, names=("b", "c", "d", "w"), order="degrevlex")
b, c, d, w = R.gens()
K = R.fraction_field()
bK, cK, dK, wK = map(K, R.gens())
KW = PolynomialRing(K, "W")
W = KW.gen()
Y_RING = PolynomialRing(QQ, names=("y", "c", "d", "w"), order="degrevlex")
yY, cY, dY, wY = Y_RING.gens()
Y_FIELD = Y_RING.fraction_field()
B_UNIVARIATE = PolynomialRing(Y_FIELD, "beta")
beta = B_UNIVARIATE.gen()
TO_B_UNIVARIATE = R.hom([beta, cY, dY, wY], B_UNIVARIATE)
TO_K_FROM_Y = Y_RING.hom([bK + 1 / bK, cK, dK, wK], K)


def primitive(value):
    value = R(value)
    if not value:
        return value
    value = R(value / value.content())
    return -value if value.leading_coefficient() < 0 else value


def strip_b_unit(value):
    """Remove a monomial b-unit and primitive-normalize on b != 0."""
    value = primitive(value)
    if not value:
        return value
    valuation = min(monomial.degree(b) for monomial in value.monomials())
    return primitive(value // (b**valuation))


def inverse_b_chart(value):
    """Pull back by b -> b^-1 modulo the declared b != 0 chart unit."""
    value = strip_b_unit(value)
    degree = value.degree(b)
    return strip_b_unit(value(b=1 / b) * b**degree)


def swap_cd_chart(value):
    return primitive(R(value)(c=d, d=c))


def metric(value):
    value = R(value)
    return {
        "degree": int(value.total_degree()),
        "degrees_b_c_d_w": [int(value.degree(g)) for g in R.gens()],
        "terms": int(len(value.monomials())),
        "sha256": sha_text(value),
    }


def y_metric(value):
    value = Y_RING(value)
    return {
        "degree": int(value.total_degree()),
        "degrees_y_c_d_w": [int(value.degree(g)) for g in Y_RING.gens()],
        "terms": int(len(value.monomials())),
        "sha256": sha_text(value),
    }


def palindromic_to_y(value):
    value = strip_b_unit(value)
    degree = value.degree(b)
    assert degree % 2 == 0
    assert inverse_b_chart(value) == value
    half = degree // 2
    univariate = B_UNIVARIATE(TO_B_UNIVARIATE(value))
    coefficients = [Y_RING(univariate[index]) for index in range(degree + 1)]
    assert all(
        coefficients[index] == coefficients[degree - index]
        for index in range(degree + 1)
    )
    chebyshev = [Y_RING(2), yY]
    for _ in range(2, half + 1):
        chebyshev.append(yY * chebyshev[-1] - chebyshev[-2])
    result = coefficients[half]
    for index in range(1, half + 1):
        result += coefficients[half + index] * chebyshev[index]
    result = Y_RING(result)
    assert K(value) == bK**half * TO_K_FROM_Y(result)
    return result, half


def rational_metric(value):
    value = K(value)
    return {
        "numerator": metric(primitive(value.numerator())),
        "denominator": metric(primitive(value.denominator())),
    }


RADICAL_FACTOR_CACHE = {}


def radical_localizer_factors(factors):
    result = {}
    for value in factors:
        value = strip_b_unit(value)
        if value.is_constant():
            continue
        key = str(value)
        if key not in RADICAL_FACTOR_CACHE:
            RADICAL_FACTOR_CACHE[key] = tuple(
                strip_b_unit(factor) for factor, _ in value.factor()
            )
        for factor in RADICAL_FACTOR_CACHE[key]:
            result[str(factor)] = factor
    return [result[key] for key in sorted(result)]


def localizer_record(factors):
    normalized = radical_localizer_factors(factors)
    canonical = [str(value) for value in normalized]
    return {
        "radical_factor_count": len(normalized),
        "radical_total_degree": sum(
            int(value.total_degree()) for value in normalized
        ),
        "radical_factor_set_sha256": hashlib.sha256(
            canonical_json(canonical).encode()
        ).hexdigest(),
        "radical_factors": [metric(value) for value in normalized],
    }


def factor_records(value):
    value = primitive(value)
    if value.is_constant():
        return []
    return [
        {
            "factor": str(primitive(factor)),
            "exponent": int(exponent),
            "metric": metric(primitive(factor)),
        }
        for factor, exponent in value.factor()
    ]


VERTEX_IDS = ("v0", "v1", "v2", "v3")
VERTEX_FORMULAS = {
    "v0": K(2),
    "v1": K(1) / 2,
    "v2": bK,
    "v3": K(1) / bK,
}
EDGE_VERTEX_IDS = {
    "E01": ("v0", "v1"),
    "E02": ("v0", "v2"),
    "E03": ("v0", "v3"),
    "E12": ("v1", "v2"),
    "E13": ("v1", "v3"),
    "E23": ("v2", "v3"),
}
ASSIGNMENT_EDGES = {
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
ASSIGNMENT_KIND = {
    key: ("fixed-moving" if key.startswith("F") else "moving-moving")
    for key in ASSIGNMENT_EDGES
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
TARGETS = {
    "R02": {
        "name": "crossed",
        "multiplicity": [0, 2],
        "Qc": (W - 1 / dK) ** 2,
        "Qd": (W - 1 / cK) ** 2,
    },
    "R11": {
        "name": "balanced",
        "multiplicity": [1, 1],
        "Qc": (W - 1 / cK) * (W - 1 / dK),
        "Qd": (W - 1 / cK) * (W - 1 / dK),
    },
    "R20": {
        "name": "identity",
        "multiplicity": [2, 0],
        "Qc": (W - 1 / cK) ** 2,
        "Qd": (W - 1 / dK) ** 2,
    },
}
EXACT_FIXTURES = (
    {"id": "Q0", "b": 3, "c": 5, "d": 7, "w": 11},
    {"id": "Q1", "b": 4, "c": 6, "d": 9, "w": 13},
)
EXTERNAL_PROVENANCE = {
    "F00-R02": {
        "pull_request": 1135,
        "commit": "f0a1d20ea16721d9596a3520658406528f5ade9f",
        "certificate_blob": "31cddc835ed2e896aa1d94a953ea8518362628c8",
        "certificate_sha256": "6953466a26b6f8bd80889cc6d69eca9c6866678f7cd6432308af58f8c25ecb10",
        "external_payload_sha256": "ec52873035a42fec4c3f19f429913197df872487c2a6137646dd81474c6fedf7",
        "status": "EXTERNAL_PROVEN_REPRESENTATIVE_ONLY",
        "scope_imported": False,
    },
    "F00-R20": {
        "pull_request": 1136,
        "commit": "9f5b7ffa8759f0372802792bc5baf589410cdd28",
        "certificate_blob": "1e083a5cac1bba0827ae2c6c9e72ffd9da03d3ba",
        "certificate_sha256": "f4572ea4eeb082fa80fbbd531222ad128e5c017f61f04b08ab4f15644bb8efe3",
        "external_payload_sha256": "ce59e2be2417dd8681bce65d7f0d838850445dfccbd82d68c137387510ea7cb5",
        "status": "EXTERNAL_PROVEN_REPRESENTATIVE_ONLY",
        "scope_imported": False,
    },
    "F00-R11": {
        "pull_request": 1137,
        "commit": "272c185ef2f64e15283947aa62ed045ce29d2059",
        "certificate_blob": "177b3f49c4248eec471d8fef39c69a66493fb020",
        "certificate_sha256": "9965c2cab06c145343413066427a81f66adad263eb856218e613d1893063868c",
        "external_payload_sha256": "a9e67b5cb40c0731f504636f06e2e99c9147b76e1d27dfee2b9d6855e9dca471",
        "status": "EXTERNAL_PROVEN_REPRESENTATIVE_ONLY",
        "scope_imported": False,
    },
    "M00-R11": {
        "pull_request": 1138,
        "commit": "cd41c6c71b5b7d114f4ca9b2f5c853ccdd3c341d",
        "certificate_blob": "f73d6a7841aec868f4e7788a688afbd9cffa117e",
        "certificate_sha256": "5a42a8567a140b47b3aadbd77fead308298b7582a9bb4383e42dde0d54531566",
        "external_payload_sha256": "3f32af654c6527e97c036d09a07c1d5554923c484300d5c3141fd997cc3a7a05",
        "status": "EXTERNAL_PROVEN_CANONICAL_REPRESENTATIVE_GREEN",
        "scope_imported": False,
    },
}


def edge(edge_id):
    left_id, right_id = EDGE_VERTEX_IDS[edge_id]
    left, right = VERTEX_FORMULAS[left_id], VERTEX_FORMULAS[right_id]
    return vector(K, (left * right, -(left + right), 1))


def evaluation(point):
    return matrix(
        K,
        (
            (1, point, point**2, 0, 0),
            (0, 0, 0, 1 + point**2, point),
            (point**2, point, 1, 0, 0),
        ),
    )


def assignment_geometry(assignment_id):
    first_id, second_id = ASSIGNMENT_EDGES[assignment_id]
    first_vertices = set(EDGE_VERTEX_IDS[first_id])
    second_vertices = set(EDGE_VERTEX_IDS[second_id])
    common_ids = sorted(first_vertices & second_vertices)
    assert len(common_ids) == 1
    common_id = common_ids[0]
    right_id = next(iter(first_vertices - {common_id}))
    left_id = next(iter(second_vertices - {common_id}))
    return {
        "first_edge": first_id,
        "second_edge": second_id,
        "common_vertex": common_id,
        "first_other_vertex": right_id,
        "second_other_vertex": left_id,
    }


def normalize_equation(value):
    value = K(value)
    cleared = R(value.numerator())
    denominator = primitive(value.denominator())
    equation = primitive(cleared)
    scalar = K(equation) / K(cleared)
    assert scalar.numerator().is_constant()
    assert scalar.denominator().is_constant()
    assert K(equation) == scalar * K(value.denominator()) * value
    return (
        equation,
        {
            "denominator": metric(denominator),
            "normalizing_scalar": str(QQ(scalar)),
            "mode": "WHOLE_PROJECTIVE_LINE_SINGLE_SCALAR",
        },
        denominator,
    )


def projective_equations(observed, target):
    assert target.is_monic() and target.degree() == 2
    raw = tuple(
        K(observed[index] - observed[2] * target[index]) for index in (0, 1)
    )
    return tuple(normalize_equation(value) for value in raw), raw


def exact_fixture_values(values):
    records = []
    for fixture in EXACT_FIXTURES:
        substitutions = {
            b: QQ(fixture["b"]),
            c: QQ(fixture["c"]),
            d: QQ(fixture["d"]),
            w: QQ(fixture["w"]),
        }
        evaluated = [QQ(value.subs(substitutions)) for value in values]
        records.append(
            {
                "fixture_id": fixture["id"],
                "values": [str(value) for value in evaluated],
            }
        )
    return records


def build_assignment(assignment_id):
    geometry = assignment_geometry(assignment_id)
    common = VERTEX_FORMULAS[geometry["common_vertex"]]
    right = VERTEX_FORMULAS[geometry["first_other_vertex"]]
    left = VERTEX_FORMULAS[geometry["second_other_vertex"]]
    first = edge(geometry["first_edge"])
    second = edge(geometry["second_edge"])

    q0, q1 = cK * dK, -(cK + dK)
    f, g, m = q0 - wK, 1 - wK * q0, q1 * (1 - wK)
    v = vector(KW, (f + g * W, m * (1 + W), g + f * W))
    v_common = v[0] + common * v[1] + common**2 * v[2]
    assert v_common.degree() == 1
    incidence_numerator = K(v_common[0])
    incidence_denominator = K(v_common[1])
    z = -incidence_numerator / incidence_denominator
    vz = vector(K, (entry(z) for entry in v))
    assert vz[0] + common * vz[1] + common**2 * vz[2] == 0
    linear_1 = vz[2]
    linear_0 = vz[1] + common * vz[2]

    target_internal = (
        (linear_0 + left * linear_1) * first
        + (linear_0 + right * linear_1) * second
    ) / (left - right)
    swapped_target = (
        (linear_0 + right * linear_1) * second
        + (linear_0 + left * linear_1) * first
    ) / (right - left)
    assert swapped_target == -target_internal

    # Solve the positive evaluation isomorphism in two explicit blocks.  This
    # is the universal source reconstruction, and avoids hiding a 5 x 5
    # inverse behind a computer-algebra call.  The only divisions are by
    #
    #   1-z^2, 1-cd, (w-z)(1-wz),
    #
    # all named parent label/deck-orbit units.
    target_0, target_1, target_2 = target_internal
    difference = (target_0 - target_2) / (1 - z**2)
    rhs_sum = target_0 + target_2
    rhs_source = -(
        (1 + q0) * (1 - wK**2) * difference / (2 * (1 - q0))
    )
    block_det = wK * (1 + z**2) - z * (1 + wK**2)
    assert block_det == (wK - z) * (1 - wK * z)
    sum_outer = (rhs_sum * wK - 2 * z * rhs_source) / block_det
    x1 = ((1 + z**2) * rhs_source - (1 + wK**2) * rhs_sum / 2) / block_det
    x0 = (sum_outer + difference) / 2
    x2 = (sum_outer - difference) / 2
    at_w_2 = x2 + x1 * wK + x0 * wK**2
    x3 = (target_1 * wK - z * q1 * at_w_2) / block_det
    x4 = ((1 + z**2) * q1 * at_w_2 - (1 + wK**2) * target_1) / block_det
    solution = vector(K, (x0, x1, x2, x3, x4))
    at_w, at_z = evaluation(wK), evaluation(z)
    coefficient_matrix = matrix(
        K,
        (
            at_w[0] - q0 * at_w[2],
            at_w[1] - q1 * at_w[2],
            *at_z.rows(),
        ),
    )
    assert coefficient_matrix * solution == vector(K, (0, 0, *target_internal))
    u = vector(
        KW,
        (
            solution[0] + solution[1] * W + solution[2] * W**2,
            solution[3] * (1 + W**2) + solution[4] * W,
            solution[2] + solution[1] * W + solution[0] * W**2,
        ),
    )

    def residual_at(root):
        u_root = sum(u[index] * root**index for index in range(3))
        v_root = sum(v[index] * root**index for index in range(3))
        divisor = (W - wK) ** 2
        quotient, remainder = (u_root**2 - W * v_root**2).quo_rem(divisor)
        assert remainder == 0
        assert quotient.degree() == 2
        return quotient

    residual_c = residual_at(cK)
    residual_d = residual_at(dK)
    reconstruction_units = {
        "z_not_deck_fixed": K(1 - z**2),
        "core_not_reciprocal": K(1 - q0),
        "forced_internal_orbits_distinct": K(block_det),
    }
    assignment_localizer_factors = [R(b)]
    for value in (
        incidence_denominator,
        K(left - right),
        *reconstruction_units.values(),
    ):
        for factor in (
            primitive(K(value).numerator()),
            primitive(K(value).denominator()),
        ):
            if not factor.is_constant():
                assignment_localizer_factors.append(factor)

    cells = {}
    equations_by_target = {}
    for target_id, target_data in TARGETS.items():
        c_lines, c_raw = projective_equations(residual_c, target_data["Qc"])
        d_lines, d_raw = projective_equations(residual_d, target_data["Qd"])
        lines = (*c_lines, *d_lines)
        raw_lines = (*c_raw, *d_raw)
        equations = tuple(line[0] for line in lines)
        audits = tuple(line[1] for line in lines)
        line_denominators = tuple(line[2] for line in lines)
        cell_localizer_factors = (
            *assignment_localizer_factors,
            *line_denominators,
        )
        assert swap_cd_chart(equations[0]) == equations[2]
        assert swap_cd_chart(equations[1]) == equations[3]
        cell_id = f"{assignment_id}-{target_id}"
        equations_by_target[target_id] = {
            "equations": equations,
            "localizer_factors": cell_localizer_factors,
        }
        cells[cell_id] = {
            "cell_id": cell_id,
            "assignment_id": assignment_id,
            "target_id": target_id,
            "classification": "UNCLASSIFIED_QSLICE_GENERATED",
            "equation_order": [
                "c_constant",
                "c_linear",
                "d_constant",
                "d_linear",
            ],
            "equations": [metric(value) for value in equations],
            "line_normalization": list(audits),
            "cell_localizer": {
                **localizer_record(cell_localizer_factors),
                "provenance": [
                    "b nonzero chart",
                    "finite incidence denominator",
                    "distinct internal stars",
                    "positive reconstruction units",
                    "four complete projective-line denominators",
                ],
            },
            "exact_rational_fixture_values": exact_fixture_values(raw_lines),
            "c_d_companion_exact": True,
            "external_provenance": EXTERNAL_PROVENANCE.get(cell_id),
            "ledger_movement": 0,
        }

    assignment = {
        "assignment_id": assignment_id,
        "kind": ASSIGNMENT_KIND[assignment_id],
        **geometry,
        "edge_formulas": {
            edge_id: (
                f"(T-{EDGE_VERTEX_IDS[edge_id][0]})"
                f"(T-{EDGE_VERTEX_IDS[edge_id][1]})"
            )
            for edge_id in ASSIGNMENT_EDGES[assignment_id]
        },
        "incidence": {
            "formula": "z=-N_a/D_a",
            "common_vertex": geometry["common_vertex"],
            "numerator": rational_metric(incidence_numerator),
            "denominator": rational_metric(incidence_denominator),
            "D_a_nonzero_source": "parent finite internal-label chart and J0/J1 disjointness",
        },
        "reconstruction": {
            "matrix_shape": [5, 5],
            "explicit_block_formula": True,
            "named_units": {
                name: rational_metric(value)
                for name, value in reconstruction_units.items()
            },
            "determinant_nonzero_source": "parent equation (9.23) positive evaluation isomorphism",
            "solution_unique": True,
        },
        "assignment_localizer": {
            **localizer_record(assignment_localizer_factors),
            "formed_before_any_symmetry_reuse": True,
        },
        "star_swap": {
            "target_changes_by_global_sign": True,
            "source_U_changes_by_global_sign": True,
            "G_unchanged": True,
        },
        "b_inversion_partner": B_INVERSION[assignment_id],
    }
    return assignment, cells, equations_by_target


def fixed_assignment_quotient_record(assignment_id, equations_by_target):
    """Record exact y/delta descent data only on literal fixed assignments."""
    assert B_INVERSION[assignment_id] == assignment_id
    records = {}
    for target_id, system in equations_by_target.items():
        equations = system["equations"]
        line_records = []
        for equation in equations:
            reduced = strip_b_unit(equation)
            pulled = inverse_b_chart(reduced)
            if pulled == reduced:
                parity = "even"
            elif pulled == -reduced:
                parity = "odd"
            else:
                raise AssertionError(
                    f"{assignment_id}-{target_id} is not b-inversion eigen"
                )
            assert parity == "even"
            quotient, b_power = palindromic_to_y(reduced)
            line_records.append(
                {
                    "parity": parity,
                    "cleared_metric": metric(reduced),
                    "quotient_metric": y_metric(quotient),
                    "lift_identity": f"cleared=b^{b_power}*Q(y,c,d,w)",
                    "quotient_coordinates": ["y=b+b^-1", "delta=b-b^-1"],
                    "relation": "delta^2=y^2-4",
                    "reduction_order": "clear_complete_line_then_reduce",
                }
            )
        records[target_id] = line_records
    return records


def expected_certificate():
    assignments = []
    cells = {}
    equation_cache = {}
    quotient_records = {}
    for assignment_id in ASSIGNMENT_EDGES:
        assignment, new_cells, equations_by_target = build_assignment(assignment_id)
        assignments.append(assignment)
        cells.update(new_cells)
        equation_cache[assignment_id] = equations_by_target
        if B_INVERSION[assignment_id] == assignment_id:
            quotient_records[assignment_id] = fixed_assignment_quotient_record(
                assignment_id, equations_by_target
            )

    # Verify the literal b-inversion pullbacks after complete-line clearing.
    symmetry_checks = []
    for assignment_id, partner_id in B_INVERSION.items():
        for target_id in TARGETS:
            left = equation_cache[assignment_id][target_id]
            right = equation_cache[partner_id][target_id]
            assert len(left["equations"]) == len(right["equations"]) == 4
            for left_equation, right_equation in zip(
                left["equations"], right["equations"]
            ):
                assert inverse_b_chart(left_equation) == strip_b_unit(
                    right_equation
                )
            left_localizer = sorted(
                {
                    str(inverse_b_chart(value))
                    for value in radical_localizer_factors(
                        left["localizer_factors"]
                    )
                }
            )
            right_localizer = sorted(
                {
                    str(strip_b_unit(value))
                    for value in radical_localizer_factors(
                        right["localizer_factors"]
                    )
                }
            )
            if left_localizer != right_localizer:
                raise AssertionError(
                    f"localizer pullback mismatch {assignment_id}-{target_id} "
                    f"to {partner_id}-{target_id}: "
                    f"left_only={sorted(set(left_localizer)-set(right_localizer))} "
                    f"right_only={sorted(set(right_localizer)-set(left_localizer))}"
                )
            symmetry_checks.append(
                {
                    "source": f"{assignment_id}-{target_id}",
                    "target": f"{partner_id}-{target_id}",
                    "equations_exact_after_b_unit": True,
                    "localizers_exact_after_b_unit": True,
                }
            )

    registry = {
        "vertices": {
            "v0": "2",
            "v1": "1/2",
            "v2": "b",
            "v3": "b^-1",
        },
        "edges": {
            edge_id: {
                "vertices": list(vertices),
                "formula": f"(T-{vertices[0]})(T-{vertices[1]})",
            }
            for edge_id, vertices in EDGE_VERTEX_IDS.items()
        },
        "assignments": {
            assignment_id: {
                "edges": list(edges),
                "kind": ASSIGNMENT_KIND[assignment_id],
            }
            for assignment_id, edges in ASSIGNMENT_EDGES.items()
        },
        "targets": {
            target_id: {
                "name": target["name"],
                "multiplicity": target["multiplicity"],
                "Qc": str(target["Qc"]),
                "Qd": str(target["Qd"]),
            }
            for target_id, target in TARGETS.items()
        },
    }
    data = {
        "schema": SCHEMA,
        "parent": {
            "commit": PARENT_COMMIT,
            "interface": "universal source-facet census equations (9.17)-(9.24)",
            "imported": [
                "positive reciprocal source form",
                "forced-square divisibility",
                "finite internal-label incidence chart",
                "positive evaluation isomorphism",
            ],
        },
        "field": {
            "prime": int(DEPLOYED_PRIME),
            "challenge_extension_degree": 6,
            "symbolic_compiler_field": "QQ",
        },
        "exact_rational_fixtures": list(EXACT_FIXTURES),
        "scope": {
            "branch": "saturated source-line diagonal (1,1,2), aligned-positive",
            "assignments": 12,
            "targets_per_assignment": 3,
            "cells": 36,
            "cell_status": "UNCLASSIFIED_QSLICE_GENERATED",
            "ledger_movement": 0,
        },
        "registry": registry,
        "source_reconstruction": {
            "q": "(T-c)(T-d)",
            "q0": "c*d",
            "q1": "-(c+d)",
            "F": "q0-w",
            "G": "1-w*q0",
            "M": "q1*(1-w)",
            "V": [
                "F+G*W",
                "M*(1+W)",
                "G+F*W",
            ],
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
        },
        "denominator_and_localizer_policy": {
            "whole_line_normalization": True,
            "never_normalize_projective_coefficients_independently": True,
            "b_nonzero_chart_unit": True,
            "incidence_D_a_nonzero": True,
            "reconstruction_determinant_nonzero": True,
            "all_dropped_factors_require_named_parent_provenance": True,
            "generic_saturation_used": False,
            "groebner_search_used": False,
        },
        "classification_order": [
            "DIRECT_SYSTEM_GENERATED",
            "LITERAL_SYMMETRY_AUDITED",
            "EXTERNAL_PROVENANCE_ANNOTATED_NOT_IMPORTED",
            "UNCLASSIFIED_QSLICE_GENERATED",
        ],
        "assignments": assignments,
        "cells": [cells[key] for key in sorted(cells)],
        "literal_symmetries": {
            "star_swap_global_sign": True,
            "c_d_companion": True,
            "b_inversion_map": B_INVERSION,
            "b_inversion_checks": symmetry_checks,
            "fixed_assignment_quotient_coordinates": quotient_records,
        },
        "rejected_globalizations": [
            "ENDPOINT_ONLY_MOBIUS_ORBIT",
            "DIAGONAL_W_MOBIUS_ORBIT",
            "FULL_SOURCE_SYSTEM_COVARIANCE",
        ],
        "external_provenance_policy": {
            "pins_are_annotations_only": True,
            "external_scopes_imported": False,
            "invalid_or_broader_orbit_scopes_imported": False,
            "pins": EXTERNAL_PROVENANCE,
        },
        "nonclaims": [
            "no q-slice system is declared empty by this atlas",
            "no external theorem is imported onto the parent-only base",
            "no Mobius or diagonal-W covariance",
            "no owner or charge",
            "no complete (1,1,2) deletion",
            "no K3 or KoalaBear row closure",
        ],
    }
    assert len(data["assignments"]) == 12
    assert len(data["cells"]) == 36
    assert len({cell["cell_id"] for cell in data["cells"]}) == 36
    data["payload_sha256"] = payload_sha(data)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not (args.emit or args.check):
        parser.error("choose --emit or --check")

    expected = expected_certificate()
    if args.emit:
        CERTIFICATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE_PATH.write_text(
            json.dumps(
                expected,
                indent=2,
                default=lambda item: int(item) if item in ZZ else str(item),
            )
            + "\n"
        )
        print(f"WROTE {CERTIFICATE_PATH}")
    if args.check:
        observed = json.loads(CERTIFICATE_PATH.read_text())
        assert observed == expected
        assert observed["payload_sha256"] == payload_sha(observed)
        print(
            "PASS: aligned-positive q-slice atlas "
            f"cells={len(observed['cells'])} "
            f"payload={observed['payload_sha256']}"
        )


if __name__ == "__main__":
    main()
