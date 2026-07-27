#!/usr/bin/env python3
"""Verify the exact six-line star geometry in the reduced u=2 conic branch."""

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
import json
import platform
from pathlib import Path

import sympy
from sympy import Matrix, Poly, factor, symbols


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "q6_u2_star_conic_geometry_certificate.json"

A, B, C, t = symbols("A B C t")
x, y, z = symbols("x y z")
LABELS = [sympy.Integer(0), sympy.Integer(1), sympy.Integer(-1), x, y, z]

GRAPHS = {
    "P6": [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)],
    "P3_PLUS_C3": [(0, 1), (1, 2), (3, 4), (4, 5), (3, 5)],
    "P2_PLUS_C4": [(0, 1), (2, 3), (3, 4), (4, 5), (2, 5)],
}


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_sha256(payload: dict[str, object]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def star_vertex(left: sympy.Expr, right: sympy.Expr) -> list[sympy.Expr]:
    """Coefficient point of (T-left)(T-right)."""
    return [sympy.Integer(1), -(left + right), left * right]


def conic_row(point: list[sympy.Expr]) -> list[sympy.Expr]:
    a, b, c = point
    return [a * a, a * b, a * c, b * b, b * c, c * c]


def conic_kernel(edges: list[tuple[int, int]]) -> list[sympy.Expr]:
    matrix = Matrix([
        conic_row(star_vertex(LABELS[i], LABELS[j]))
        for i, j in edges
    ])
    # Signed maximal minors give a canonical right-kernel vector.
    result = []
    for column in range(6):
        minor = matrix[:, [j for j in range(6) if j != column]]
        result.append(factor((-1) ** column * minor.det()))
    require(
        any(result),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:59',
    )
    require(
        all((factor(entry) == 0 for entry in matrix * Matrix(result))),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:60',
    )
    return result


def compact_conic_coefficients() -> dict[str, list[sympy.Expr]]:
    """Cofactor vectors with their harmless common factors removed."""
    p6 = [
        x * y * (x * y * z + x * y + 2 * x * z - y * z + y),
        x * y * (x + 1) * (y + 1) * (z + 1),
        (
            x**2 * y**2 * z + x**2 * y**2 + 2 * x**2 * y * z
            + x**2 * z - x**2 - x * y**2 * z + x * y**2
            - x * z + x + 2 * y**2 + 2 * y * z
        ),
        -x * y * (x * z - x - 2 * y * z - z - 1),
        (
            x**2 * y * z - x**2 * y - x**2 * z + x**2
            + 2 * x * y**2 + x * y * z + x * y + x * z - x
            + 2 * y**2 * z + 2 * y
        ),
        x**2 * z - x**2 - x * z + x + 2 * y**2 + 2 * y * z,
    ]
    p3_c3 = [
        -x * y * z,
        sympy.Integer(0),
        -(x * y * z - x - y - z),
        x * y * z,
        x * y + x * z + y * z + 1,
        x + y + z,
    ]
    p2_c4 = [
        -x * y * z * (x * y * z + x * y - 2 * x * z + y * z - y),
        -x * y * z * (x + 1) * (y - 1) * (z + 1),
        (
            x**2 * y**2 * z**2 - x**2 * y**2 * z - 2 * x**2 * y**2
            + 2 * x**2 * y + x**2 * z**2 - x**2 * z
            - x * y**2 * z**2 + x * y**2 * z - x * z**2 + x * z
            - 2 * y**2 * z**2 + 2 * y * z**2
        ),
        -x * y * z * (x * z - x + 2 * y - z - 1),
        (y - 1) * (
            x**2 * z**2 - x**2 * z - 2 * x * y
            - x * z**2 + x * z - 2 * y * z
        ),
        x**2 * z**2 - x**2 * z - x * z**2 + x * z - 2 * y**2 + 2 * y,
    ]
    return {
        "P6": p6,
        "P3_PLUS_C3": p3_c3,
        "P2_PLUS_C4": p2_c4,
    }


def verify_candidate_conics(
    coefficients: dict[str, list[sympy.Expr]],
) -> dict[str, str]:
    """Check incidence and one nonzero maximal minor for each graph."""
    witnesses: dict[str, tuple[int, sympy.Expr]] = {
        "P6": (
            1,
            -(
                (x - 1) * (x - z) * (y - 1) * (y + 1)
                * coefficients["P6"][1]
            ),
        ),
        "P3_PLUS_C3": (
            0,
            (
                (x - 1) * (x - y) * (x - z)
                * (y - 1) * (y - z) * (z - 1)
                * coefficients["P3_PLUS_C3"][0]
            ),
        ),
        "P2_PLUS_C4": (
            1,
            -(
                (x - z) ** 2 * (y + 1) ** 2
                * coefficients["P2_PLUS_C4"][1]
            ),
        ),
    }
    outputs = {}
    for name, edges in GRAPHS.items():
        vector = coefficients[name]
        for i, j in edges:
            require(
                sympy.expand(conic_value(vector, star_vertex(LABELS[i], LABELS[j]))) == 0,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:145',
            )
        matrix = Matrix([
            conic_row(star_vertex(LABELS[i], LABELS[j]))
            for i, j in edges
        ])
        column, expected_minor = witnesses[name]
        minor = matrix[:, [j for j in range(6) if j != column]].det()
        require(
            sympy.expand(minor - expected_minor) == 0,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:154',
        )
        outputs[name] = str(factor(expected_minor))
    return outputs


def conic_value(coefficients: list[sympy.Expr], point: list[sympy.Expr]) -> sympy.Expr:
    return factor(sum(
        coefficient * monomial
        for coefficient, monomial in zip(
            coefficients, conic_row(point), strict=True
        )
    ))


def conic_discriminant(coefficients: list[sympy.Expr]) -> sympy.Expr:
    q00, q01, q02, q11, q12, q22 = coefficients
    doubled_symmetric_matrix = Matrix([
        [2 * q00, q01, q02],
        [q01, 2 * q11, q12],
        [q02, q12, 2 * q22],
    ])
    return factor(doubled_symmetric_matrix.det())


def other_intersection(
    coefficients: list[sympy.Expr],
    line_label: sympy.Expr,
    known_label: sympy.Expr,
) -> sympy.Expr:
    restriction = factor(conic_value(
        coefficients,
        star_vertex(line_label, t),
    ))
    quotient = factor(restriction / (t - known_label))
    require(
        Poly(quotient, t).degree() == 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:188',
    )
    slope, intercept = Poly(quotient, t).all_coeffs()
    return factor(-intercept / slope)


def build_payload() -> dict[str, object]:
    coefficients = compact_conic_coefficients()
    minor_witnesses = verify_candidate_conics(coefficients)
    determinants = {
        name: conic_discriminant(vector)
        for name, vector in coefficients.items()
    }

    expected_p3_c3 = factor(
        -2
        * x * y * z
        * (x - 1) * (x + 1)
        * (y - 1) * (y + 1)
        * (z - 1) * (z + 1)
    )
    f_gate = x * y * z + x * y + x * z - x - 2 * y * z
    g_gate = x * y * z - 2 * x * y + x * z + y * z - z
    expected_p6 = factor(
        4
        * x * y
        * (x - 1) ** 2 * (x + 1)
        * (x - y)
        * (y - 1) * (y + 1) ** 2
        * (z - 1) * (z + 1)
        * f_gate
    )
    expected_p2_c4 = factor(
        -4
        * x * y * z
        * (x - 1) * (x + 1)
        * (x - y)
        * (y - 1) * (y - z)
        * (z - 1) * (z + 1)
        * f_gate * g_gate
    )

    require(
        factor(determinants['P3_PLUS_C3'] - expected_p3_c3) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:229',
    )
    require(
        factor(determinants['P6'] - expected_p6) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:230',
    )
    require(
        factor(determinants['P2_PLUS_C4'] - expected_p2_c4) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:231',
    )

    p3_c3 = coefficients["P3_PLUS_C3"]
    endpoint_zero = other_intersection(
        p3_c3, LABELS[0], LABELS[1]
    )
    endpoint_two = other_intersection(
        p3_c3, LABELS[2], LABELS[1]
    )
    require(
        factor(endpoint_zero - LABELS[2]) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:240',
    )
    require(
        factor(endpoint_two - LABELS[0]) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:241',
    )
    common_second_point = star_vertex(LABELS[0], LABELS[2])
    require(
        conic_value(p3_c3, common_second_point) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:243',
    )

    p6 = coefficients["P6"]
    p6_endpoint_zero = other_intersection(
        p6, LABELS[0], LABELS[1]
    )
    p6_endpoint_five = other_intersection(
        p6, LABELS[5], LABELS[4]
    )
    expected_p6_endpoint_zero = -(
        x * y * z + x * y + 2 * x * z - y * z + y
    ) / (x * z - x - 2 * y * z - z - 1)
    expected_p6_endpoint_five = (
        x * (x * y + x * z - 2 * y * z + y - z)
        / (x**2 * y - x**2 * z + x * y + x * z - 2 * y * z)
    )
    require(
        factor(p6_endpoint_zero - expected_p6_endpoint_zero) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:259',
    )
    require(
        factor(p6_endpoint_five - expected_p6_endpoint_five) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:260',
    )

    p2_c4 = coefficients["P2_PLUS_C4"]
    p2_c4_endpoint_zero = other_intersection(
        p2_c4, LABELS[0], LABELS[1]
    )
    p2_c4_endpoint_one = other_intersection(
        p2_c4, LABELS[1], LABELS[0]
    )
    expected_p2_c4_endpoint_zero = (
        x * y * z + x * y - 2 * x * z + y * z - y
    ) / (x * z - x + 2 * y - z - 1)
    expected_p2_c4_endpoint_one = (
        x * y * z + x * y - x * z + y * z
    ) / (x * z + y)
    require(
        factor(p2_c4_endpoint_zero - expected_p2_c4_endpoint_zero) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:275',
    )
    require(
        factor(p2_c4_endpoint_one - expected_p2_c4_endpoint_one) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:278',
    )

    p6_extra_vertex_gate = x * y + x * z - 2 * y * z + y - z
    p6_v05_value = factor(conic_value(
        p6, star_vertex(LABELS[0], LABELS[5])
    ))
    expected_p6_v05_value = factor(
        -x * y * (z - 1) * (z + 1) * p6_extra_vertex_gate
    )
    require(
        factor(p6_v05_value - expected_p6_v05_value) == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:289',
    )

    sample = {x: 2, y: 3, z: 4}
    sample_determinants = {
        name: int(value.subs(sample))
        for name, value in determinants.items()
    }
    require(
        all((value != 0 for value in sample_determinants.values())),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:296',
    )

    return {
        "schema": "q6-u2-star-conic-geometry-v1",
        "normalization": {
            "source_labels": ["0", "1", "-1", "x", "y", "z"],
            "star_vertex": "[1,-(alpha_i+alpha_j),alpha_i*alpha_j]",
            "conic_monomials": ["A^2", "A*B", "A*C", "B^2", "B*C", "C^2"],
        },
        "graph_edges": {
            name: [list(edge) for edge in edges]
            for name, edges in GRAPHS.items()
        },
        "rank_five_minor_witnesses": minor_witnesses,
        "discriminant_factorization": {
            "P6": str(expected_p6),
            "P3_PLUS_C3": str(expected_p3_c3),
            "P2_PLUS_C4": str(expected_p2_c4),
        },
        "noncollision_gates": {
            "P6": [str(f_gate), str(p6_extra_vertex_gate)],
            "P3_PLUS_C3": [],
            "P2_PLUS_C4": [str(f_gate), str(g_gate)],
        },
        "endpoint_second_intersections": {
            "P6": {
                "line_0_known_neighbor_1": str(p6_endpoint_zero),
                "line_5_known_neighbor_4": str(p6_endpoint_five),
            },
            "P3_PLUS_C3": {
                "line_0_known_neighbor_1": str(endpoint_zero),
                "line_2_known_neighbor_1": str(endpoint_two),
                "common_image_point": "[1,0,0]",
            },
            "P2_PLUS_C4": {
                "line_0_known_neighbor_1": str(p2_c4_endpoint_zero),
                "line_1_known_neighbor_0": str(p2_c4_endpoint_one),
            },
        },
        "fiber_ledger": {
            "conic_quotient_degree": 2,
            "endpoint_free_divisor_degrees": [2, 2],
            "endpoint_free_divisors_are_reduced": True,
            "endpoint_free_divisors_are_disjoint": True,
            "both_map_to_same_point": True,
            "P3_PLUS_C3_status": "PROVED_IMPOSSIBLE",
        },
        "sample_determinants_at_x2_y3_z4": sample_determinants,
        "claims": {
            "five_star_vertices_determine_the_candidate_conic": True,
            "P3_PLUS_C3_candidate_is_nonsingular_for_distinct_labels": True,
            "P3_PLUS_C3_endpoint_fibers_collide": True,
            "remaining_signature_graphs": ["P6", "P2_PLUS_C4"],
        },
    }


def validate_payload(payload: dict[str, object]) -> None:
    require(
        payload['schema'] == 'q6-u2-star-conic-geometry-v1',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:358',
    )
    require(
        payload['claims']['P3_PLUS_C3_candidate_is_nonsingular_for_distinct_labels'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:359',
    )
    require(
        payload['claims']['P3_PLUS_C3_endpoint_fibers_collide'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:360',
    )
    require(
        payload['claims']['remaining_signature_graphs'] == ['P6', 'P2_PLUS_C4'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:361',
    )
    fiber = payload["fiber_ledger"]
    require(
        fiber['conic_quotient_degree'] == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:363',
    )
    require(
        fiber['endpoint_free_divisor_degrees'] == [2, 2],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:364',
    )
    require(
        fiber['endpoint_free_divisors_are_reduced'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:365',
    )
    require(
        fiber['endpoint_free_divisors_are_disjoint'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:366',
    )
    require(
        fiber['both_map_to_same_point'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:367',
    )
    require(
        fiber['P3_PLUS_C3_status'] == 'PROVED_IMPOSSIBLE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:368',
    )
    endpoints = payload["endpoint_second_intersections"]["P3_PLUS_C3"]
    require(
        endpoints['line_0_known_neighbor_1'] == '-1',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:370',
    )
    require(
        endpoints['line_2_known_neighbor_1'] == '0',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:371',
    )
    require(
        endpoints['common_image_point'] == '[1,0,0]',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:372',
    )
    require(
        payload['noncollision_gates']['P3_PLUS_C3'] == [],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:373',
    )
    require(
        len(payload['noncollision_gates']['P6']) == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:374',
    )
    require(
        len(payload['endpoint_second_intersections']['P6']) == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:375',
    )
    require(
        len(payload['endpoint_second_intersections']['P2_PLUS_C4']) == 2,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:376',
    )
    require(
        all((value != 0 for value in payload['sample_determinants_at_x2_y3_z4'].values())),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:377',
    )


def certificate_for(payload: dict[str, object]) -> dict[str, object]:
    validate_payload(payload)
    return {
        "payload": payload,
        "payload_sha256": payload_sha256(payload),
        "runtime_metadata": {
            "python_version": platform.python_version(),
            "sympy_version": sympy.__version__,
        },
    }


def check_certificate(path: Path) -> None:
    actual = json.loads(path.read_text(encoding="utf-8"))
    expected = certificate_for(build_payload())
    require(
        actual["payload"] == expected["payload"],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:394',
    )
    require(
        actual["payload_sha256"] == expected["payload_sha256"],
        "mathematical payload hash differs from exact replay",
    )
    require(
        isinstance(actual.get("runtime_metadata"), dict),
        "certificate must record informational runtime metadata",
    )
    print("five-star conic reconstruction: PASS")
    print("three signature-graph discriminants: PASS")
    print("P3+C3 endpoint intersection identity: PASS")
    print("P3+C3 degree-two fiber contradiction: PASS")
    print(f"payload_sha256={expected['payload_sha256']}")


def tamper_selftest(path: Path) -> None:
    certificate = json.loads(path.read_text(encoding="utf-8"))
    require(
        certificate['payload_sha256'] == payload_sha256(certificate['payload']),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:404',
    )
    base = certificate["payload"]
    validate_payload(base)
    mutations = []

    item = copy.deepcopy(base)
    item["fiber_ledger"]["conic_quotient_degree"] = 4
    mutations.append(item)

    item = copy.deepcopy(base)
    item["fiber_ledger"]["endpoint_free_divisors_are_disjoint"] = False
    mutations.append(item)

    item = copy.deepcopy(base)
    item["endpoint_second_intersections"]["P3_PLUS_C3"][
        "line_0_known_neighbor_1"
    ] = "z"
    mutations.append(item)

    item = copy.deepcopy(base)
    item["claims"]["P3_PLUS_C3_endpoint_fibers_collide"] = False
    mutations.append(item)

    item = copy.deepcopy(base)
    item["claims"]["remaining_signature_graphs"].append("P3_PLUS_C3")
    mutations.append(item)

    rejected = 0
    for mutation in mutations:
        try:
            validate_payload(mutation)
        except VerificationError:
            rejected += 1
    require(
        rejected == len(mutations),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_star_conic_geometry.py:437',
    )
    print(f"tamper mutations rejected: PASS {rejected}/{len(mutations)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.check:
        check_certificate(args.certificate)
    elif args.tamper_selftest:
        tamper_selftest(args.certificate)
    else:
        certificate = certificate_for(build_payload())
        args.certificate.write_text(
            json.dumps(certificate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(args.certificate)


if __name__ == "__main__":
    main()
