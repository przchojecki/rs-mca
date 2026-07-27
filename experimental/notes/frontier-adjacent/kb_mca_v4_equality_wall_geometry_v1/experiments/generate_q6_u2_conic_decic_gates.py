#!/usr/bin/env python3
"""Emit exact u=2 conic free-pair/common-decic gate templates."""

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
import math
from pathlib import Path

import classify_q6_u2_conic_graph_orbits as conic


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "q6_u2_conic_decic_gate_templates.json"


def add(left: list[int], right: list[int], prime: int) -> list[int]:
    require(
        len(left) == len(right),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:21',
    )
    return [
        (left[index] + right[index]) % prime
        for index in range(len(left))
    ]


def scale(polynomial: list[int], scalar: int, prime: int) -> list[int]:
    return [scalar * coefficient % prime for coefficient in polynomial]


def multiply(
    left: list[int], right: list[int], prime: int
) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index]
                + left_value * right_value
            ) % prime
    return result


def linear_power(
    linear: tuple[int, int], exponent: int, prime: int
) -> list[int]:
    x_coefficient, y_coefficient = linear
    return [
        (
            math.comb(exponent, y_degree)
            * pow(x_coefficient, exponent - y_degree, prime)
            * pow(y_coefficient, y_degree, prime)
        )
        % prime
        for y_degree in range(exponent + 1)
    ]


def compose(
    polynomial: list[int],
    matrix: tuple[int, int, int],
    prime: int,
) -> list[int]:
    """Compose a binary form with [[a,b],[c,-a]]."""
    c, a, b = matrix
    degree = len(polynomial) - 1
    result = [0] * (degree + 1)
    for y_degree, coefficient in enumerate(polynomial):
        if not coefficient:
            continue
        x_part = linear_power((a, b), degree - y_degree, prime)
        y_part = linear_power((c, -a), y_degree, prime)
        term = scale(multiply(x_part, y_part, prime), coefficient, prime)
        result = add(result, term, prime)
    return result


def cross(left: list[int], right: list[int], prime: int) -> list[int]:
    require(
        len(left) == len(right) == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:80',
    )
    return [
        (left[1] * right[2] - left[2] * right[1]) % prime,
        (left[2] * right[0] - left[0] * right[2]) % prime,
        (left[0] * right[1] - left[1] * right[0]) % prime,
    ]


def pair_row(quadratic: list[int], prime: int) -> list[int]:
    require(
        len(quadratic) == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:89',
    )
    a_coefficient, b_coefficient, c_coefficient = quadratic
    return [
        c_coefficient % prime,
        b_coefficient % prime,
        -a_coefficient % prime,
    ]


def candidate(
    first_quadratic: list[int],
    second_quadratic: list[int],
    prime: int,
) -> list[int]:
    return cross(
        pair_row(first_quadratic, prime),
        pair_row(second_quadratic, prime),
        prime,
    )


def determinant_parameter(matrix: list[int], prime: int) -> int:
    c, a, b = matrix
    return (a * a + b * c) % prime


def common_decic(
    psi_numerator: list[int],
    psi_denominator: list[int],
    labels: list[int],
    prime: int,
) -> list[int]:
    require(
        len(psi_numerator) == len(psi_denominator) == 3,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:121',
    )
    result = [1]
    for label in labels:
        fiber = add(
            psi_numerator,
            scale(psi_denominator, -label, prime),
            prime,
        )
        result = multiply(result, fiber, prime)
    require(
        len(result) == 11,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:130',
    )
    return result


def source_quintic(labels: list[int], prime: int) -> list[int]:
    result = [1]
    for label in labels:
        result = multiply(result, [1, -label % prime], prime)
    require(
        len(result) == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:138',
    )
    return result


def reciprocal_source_gate(
    first_source_pair: list[int],
    second_source_pair: list[int],
    labels: list[int],
    prime: int,
) -> dict[str, object]:
    matrix = candidate(first_source_pair, second_source_pair, prime)
    determinant = determinant_parameter(matrix, prime)
    quintic = source_quintic(labels, prime)
    transformed = compose(quintic, tuple(matrix), prime)
    minors = proportional_minors(quintic, transformed, prime)
    c_value, a_value, b_value = matrix
    fixed_labels = []
    for label in labels:
        denominator = (c_value * label - a_value) % prime
        if not denominator:
            continue
        image = (
            (a_value * label + b_value)
            * pow(denominator, prime - 2, prime)
        ) % prime
        if image == label:
            fixed_labels.append(label)
    return {
        "candidate_c_a_b": matrix,
        "determinant_parameter": determinant,
        "common_quintic_coefficients": quintic,
        "transformed_quintic_coefficients": transformed,
        "proportionality_minors": minors,
        "fixed_common_labels": fixed_labels,
        "invariant_with_one_fixed_label": (
            determinant != 0
            and all(value == 0 for value in minors)
            and len(fixed_labels) == 1
        ),
    }


def proportional_minors(
    left: list[int], right: list[int], prime: int
) -> list[int]:
    require(
        len(left) == len(right),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:183',
    )
    pivot = next(
        (
            index
            for index, pair in enumerate(zip(left, right, strict=True))
            if pair != (0, 0)
        ),
        None,
    )
    require(
        pivot is not None,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:192',
    )
    return [
        (
            left[index] * right[pivot]
            - right[index] * left[pivot]
        )
        % prime
        for index in range(len(left))
        if index != pivot
    ]


def invariance_gate(
    first_quadratic: list[int],
    second_quadratic: list[int],
    psi_numerator: list[int],
    psi_denominator: list[int],
    labels: list[int],
    prime: int,
) -> dict[str, object]:
    matrix = candidate(first_quadratic, second_quadratic, prime)
    determinant = determinant_parameter(matrix, prime)
    decic = common_decic(
        psi_numerator, psi_denominator, labels, prime
    )
    transformed = compose(decic, tuple(matrix), prime)
    minors = proportional_minors(decic, transformed, prime)
    return {
        "candidate_c_a_b": matrix,
        "determinant_parameter": determinant,
        "common_decic_coefficients": decic,
        "transformed_decic_coefficients": transformed,
        "proportionality_minors": minors,
        "invariant": determinant != 0 and all(value == 0 for value in minors),
    }


def demo() -> dict[str, object]:
    prime = 101
    # The two root pairs are {2, 1/2} and {3, 1/3}.
    first = [1, 48, 1]
    second = [1, 64, 1]
    # psi(x)=x^2. The five quotient labels are stable under w -> 1/w.
    psi_numerator = [1, 0, 0]
    psi_denominator = [0, 0, 1]
    labels = [16, 19, 25, 97, 100]
    good = invariance_gate(
        first,
        second,
        psi_numerator,
        psi_denominator,
        labels,
        prime,
    )
    require(
        good['candidate_c_a_b'] == [16, 0, 16],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:246',
    )
    require(
        good['determinant_parameter'] != 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:247',
    )
    require(
        good['invariant'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:248',
    )

    bad_labels = labels[:-1] + [2]
    bad = invariance_gate(
        first,
        second,
        psi_numerator,
        psi_denominator,
        bad_labels,
        prime,
    )
    require(
        bad['invariant'] is False,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:259',
    )
    require(
        any((value != 0 for value in bad['proportionality_minors'])),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:260',
    )

    # The endpoint neighbor pairs on the source line are
    # {4,1/4} and {9,1/9}; they determine w -> 1/w.
    first_source_pair = [1, 21, 1]
    second_source_pair = [1, 47, 1]
    source_gate = reciprocal_source_gate(
        first_source_pair,
        second_source_pair,
        labels,
        prime,
    )
    require(
        source_gate['candidate_c_a_b'] == [26, 0, 26],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:272',
    )
    require(
        source_gate['invariant_with_one_fixed_label'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:273',
    )
    require(
        source_gate['fixed_common_labels'] == [100],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:274',
    )

    return {
        "field": prime,
        "free_quadratics": [first, second],
        "deck_map": {
            "numerator": psi_numerator,
            "denominator": psi_denominator,
        },
        "invariant_common_labels": labels,
        "candidate_c_a_b": good["candidate_c_a_b"],
        "candidate_nondegenerate": True,
        "invariance_minors": good["proportionality_minors"],
        "tampered_common_labels": bad_labels,
        "tampered_nonzero_minor_count": sum(
            value != 0 for value in bad["proportionality_minors"]
        ),
        "reciprocal_source_quintic_gate": {
            "endpoint_source_quadratics": [
                first_source_pair,
                second_source_pair,
            ],
            **source_gate,
        },
    }


def endpoint_templates() -> list[dict[str, object]]:
    conic_data = conic.payload()
    conic.validate(conic_data)
    templates = []
    for row in conic_data["classification"]:
        representatives = [
            representative
            for representative in row["free_pair_quotient"][
                "representatives"
            ]
            if not representative["cycle_union"]
        ]
        templates.append(
            {
                "partition": row["partition"],
                "open_endpoint_orbits": len(representatives),
                "reciprocal_open_orbits": sum(
                    representative["reciprocal_compatible"]
                    for representative in representatives
                ),
                "representatives": representatives,
            }
        )
    return templates


def payload() -> dict[str, object]:
    data: dict[str, object] = {
        "status": "PROVED_GATE_REDUCTION_TARGET_OPEN",
        "gate_schema": {
            "free_quadratic_coefficients": "[A_r,B_r,C_r]",
            "pair_row": "[C_r,B_r,-A_r]",
            "candidate": "cross(pair_row_j,pair_row_k)=(c,a,b)",
            "nondegeneracy": "a^2+b*c != 0",
            "common_decic": "product_k(psi_n-alpha_k*psi_d)",
            "invariance": "C_K(M(X,Y)) proportional to C_K(X,Y)",
            "coefficient_gate_count": 10,
            "reciprocal_source_gate": (
                "endpoint source pairs determine J; "
                "A_K(J(X,Y)) proportional to A_K(X,Y); "
                "exactly one common label fixed"
            ),
        },
        "surviving_reduced_quotient_profiles": {
            "reciprocal": {
                "degree": 2,
                "normal_form": "w + mu^2/w",
                "common_labels": "one fixed label plus two reciprocal pairs",
            },
            "order_4": {
                "degree": 4,
                "normal_form": "D4(w,a)=w^4-4*a*w^2+2*a^2",
                "common_labels": (
                    "one total-ramification label plus one "
                    "complete unramified four-fiber"
                ),
            },
            "order_5": {
                "degree": 5,
                "normal_form": "D5(w,a)=w^5-5*a*w^3+5*a^2*w",
                "common_labels": "one complete unramified five-fiber",
            },
        },
        "endpoint_templates": endpoint_templates(),
        "finite_field_regression": demo(),
        "claims": {
            "two_free_pairs_determine_candidate": "PROVED",
            "common_decic_gate_generator": "PROVED",
            "deployed_gate_factorization": "OPEN",
            "conic_exclusion": "OPEN",
            "payment": "NONE",
        },
    }
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()
    data["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return data


def validate(data: dict[str, object]) -> None:
    require(
        data['status'] == 'PROVED_GATE_REDUCTION_TARGET_OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:382',
    )
    schema = data["gate_schema"]
    require(
        schema['coefficient_gate_count'] == 10,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:384',
    )
    require(
        schema['nondegeneracy'] == 'a^2+b*c != 0',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:385',
    )
    profiles = data["surviving_reduced_quotient_profiles"]
    require(
        sorted(profiles) == ['order_4', 'order_5', 'reciprocal'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:387',
    )
    require(
        [profiles[key]['degree'] for key in sorted(profiles)] == [4, 5, 2],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:388',
    )
    require(
        profiles['order_4']['normal_form'] == 'D4(w,a)=w^4-4*a*w^2+2*a^2',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:389',
    )
    require(
        profiles['order_5']['normal_form'] == 'D5(w,a)=w^5-5*a*w^3+5*a^2*w',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:392',
    )
    require(
        len(data['endpoint_templates']) == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:395',
    )
    require(
        [row['open_endpoint_orbits'] for row in data['endpoint_templates']] == [3, 3, 2, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:396',
    )
    require(
        [row['reciprocal_open_orbits'] for row in data['endpoint_templates']] == [2, 2, 1, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:400',
    )
    require(
        [row['partition'] for row in data['endpoint_templates']] == [[6], [4, 2], [3, 3], [2, 2, 2]],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:404',
    )
    for row in data["endpoint_templates"]:
        require(
            len(row['representatives']) == row['open_endpoint_orbits'],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:408',
        )
        for representative in row["representatives"]:
            require(
                representative['cycle_union'] is False,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:410',
            )
            require(
                len(representative['endpoint_rows']) == 2,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:411',
            )
            require(
                len(representative['free_pole_edges']) == 4,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:412',
            )

    regression = data["finite_field_regression"]
    require(
        regression['field'] == 101,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:415',
    )
    require(
        regression['candidate_c_a_b'] == [16, 0, 16],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:416',
    )
    require(
        regression['candidate_nondegenerate'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:417',
    )
    require(
        regression['invariance_minors'] == [0] * 10,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:418',
    )
    require(
        regression['tampered_nonzero_minor_count'] >= 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:419',
    )
    reciprocal_gate = regression["reciprocal_source_quintic_gate"]
    require(
        reciprocal_gate['candidate_c_a_b'] == [26, 0, 26],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:421',
    )
    require(
        reciprocal_gate['determinant_parameter'] != 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:422',
    )
    require(
        reciprocal_gate['proportionality_minors'] == [0] * 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:423',
    )
    require(
        reciprocal_gate['fixed_common_labels'] == [100],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:424',
    )
    require(
        reciprocal_gate['invariant_with_one_fixed_label'] is True,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:425',
    )

    claims = data["claims"]
    require(
        claims['two_free_pairs_determine_candidate'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:428',
    )
    require(
        claims['common_decic_gate_generator'] == 'PROVED',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:429',
    )
    require(
        claims['deployed_gate_factorization'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:430',
    )
    require(
        claims['conic_exclusion'] == 'OPEN',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:431',
    )
    require(
        claims['payment'] == 'NONE',
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:432',
    )

    supplied_hash = data["payload_sha256"]
    unhashed = dict(data)
    del unhashed["payload_sha256"]
    canonical = json.dumps(
        unhashed, sort_keys=True, separators=(",", ":")
    ).encode()
    require(
        supplied_hash == hashlib.sha256(canonical).hexdigest(),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:440',
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
    forged["endpoint_templates"][0]["open_endpoint_orbits"] = 4
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["gate_schema"]["coefficient_gate_count"] = 9
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["finite_field_regression"]["candidate_nondegenerate"] = False
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["deployed_gate_factorization"] = "PROVED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["claims"]["payment"] = "BOOKED"
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["surviving_reduced_quotient_profiles"]["order_5"]["degree"] = 10
    mutations.append(forged)

    forged = copy.deepcopy(data)
    forged["finite_field_regression"]["reciprocal_source_quintic_gate"][
        "fixed_common_labels"
    ] = [1, 100]
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
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:491',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/experiments/generate_q6_u2_conic_decic_gates.py:511',
        )
    rejected = tamper_selftest(data) if args.tamper_selftest else 0

    for row in data["endpoint_templates"]:
        partition = "+".join(str(value) for value in row["partition"])
        print(
            f"partition={partition} "
            f"open_endpoint_orbits={row['open_endpoint_orbits']} "
            f"reciprocal_open_orbits={row['reciprocal_open_orbits']}"
        )
    print("two-free-pair candidate: PASS")
    print("common-decic gate regression: PASS")
    print("reciprocal source-quintic gate: PASS")
    print("reciprocal/Dickson quotient profiles: PASS")
    if args.tamper_selftest:
        print(f"tamper mutations rejected: PASS {rejected}/7")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
