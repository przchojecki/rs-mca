#!/usr/bin/env python3
"""Finite-field regression for the homogeneous resultant factorization."""

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
import hashlib
import json
from pathlib import Path

from verify_complement_locator_interpolation_descent import (
    FIELD,
    add,
    bivariate_mul,
    divmod_poly,
    evaluate,
    lagrange,
    mul,
    scale,
    sub,
    trim,
)


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "homogeneous_resultant_factorization_certificate.json"


def det_poly(matrix: list[list[list[int]]]) -> list[int]:
    size = len(matrix)
    if size == 1:
        return matrix[0][0]
    total = [0]
    for column in range(size):
        minor = [
            row[:column] + row[column + 1 :]
            for row in matrix[1:]
        ]
        term = mul(matrix[0][column], det_poly(minor))
        total = add(total, term) if column % 2 == 0 else sub(total, term)
    return trim(total)


def resultant_t(
    first: list[list[int]], second: list[list[int]]
) -> list[int]:
    first = list(first)
    second = list(second)
    while len(first) > 1 and first[-1] == [0]:
        first.pop()
    while len(second) > 1 and second[-1] == [0]:
        second.pop()
    degree_first = len(first) - 1
    degree_second = len(second) - 1
    width = degree_first + degree_second
    first_high = list(reversed(first))
    second_high = list(reversed(second))
    matrix: list[list[list[int]]] = []
    for shift in range(degree_second):
        matrix.append(
            [[0]] * shift
            + first_high
            + [[0]] * (width - shift - len(first_high))
        )
    for shift in range(degree_first):
        matrix.append(
            [[0]] * shift
            + second_high
            + [[0]] * (width - shift - len(second_high))
        )
    return det_poly(matrix)


def source_factor(
    source_points: list[int], omitted: int
) -> list[int]:
    result = [1]
    for index, point in enumerate(source_points):
        if index != omitted:
            result = mul(result, [(-point) % FIELD, 1])
    return result


def regression() -> dict[str, object]:
    # Three projective source values: 0, 1, infinity. In the affine chart,
    # lambda=t(t-1), while P is a quadratic parameter form.
    source_points = [10, 20, 30]
    residuals = [
        [(-40) % FIELD, 1],
        [(-41) % FIELD, 1],
        mul([(-42) % FIELD, 1], [(-43) % FIELD, 1]),
    ]
    source_coefficients = [
        mul(source_factor(source_points, index), residuals[index])
        for index in range(3)
    ]
    q1, q2, q3 = source_coefficients

    # P=Q1(t-1)+Q2*t+Q3*t(t-1).
    p_bivariate = [
        scale(q1, -1),
        sub(add(q1, q2), q3),
        q3,
    ]
    lambda_t = [0, -1 % FIELD, 1]

    carrier_roots = [2, 3, 4, 5, 6, 7, 8]
    carrier = [1]
    for root in carrier_roots:
        carrier = mul(carrier, [(-root) % FIELD, 1])

    # Construct the unique affine Q_aff with the required values on the
    # three source points. The source linear forms are t, t-1, and 1.
    source_linear_forms = [(0, 1), (-1, 1), (1, 0)]
    q0_values = []
    q1_values = []
    for index, sigma in enumerate(source_points):
        kappa = evaluate(source_coefficients[index], sigma)
        carrier_value = evaluate(carrier, sigma)
        constant, linear = source_linear_forms[index]
        q0_values.append(carrier_value * constant * pow(kappa, -1, FIELD))
        q1_values.append(carrier_value * linear * pow(kappa, -1, FIELD))
    q_aff = [
        lagrange(source_points, q0_values),
        lagrange(source_points, q1_values),
    ]

    numerator = bivariate_mul(p_bivariate, q_aff)
    while len(numerator) < len(lambda_t):
        numerator.append([0])
    for degree, coefficient in enumerate(lambda_t):
        numerator[degree] = sub(
            numerator[degree], scale(carrier, coefficient)
        )

    source_locator = [1]
    for sigma in source_points:
        source_locator = mul(
            source_locator, [(-sigma) % FIELD, 1]
        )
    companion = []
    for coefficient in numerator:
        quotient, remainder = divmod_poly(coefficient, source_locator)
        require(
            remainder == [0],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:144',
        )
        companion.append(quotient)

    resultant = resultant_t(p_bivariate, companion)
    residual_product = [1]
    for residual in residuals:
        residual_product = mul(residual_product, residual)
    predicted = mul(mul(carrier, carrier), residual_product)
    scalar, remainder = divmod_poly(resultant, predicted)
    require(
        remainder == [0],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:153',
    )
    require(
        len(scalar) == 1 and scalar[0] != 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:154',
    )

    source_product = [1]
    for coefficient in source_coefficients:
        source_product = mul(source_product, coefficient)
    source_square = mul(source_locator, source_locator)
    recovered_residuals, source_remainder = divmod_poly(
        source_product, source_square
    )
    require(
        source_remainder == [0],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:163',
    )
    require(
        recovered_residuals == residual_product,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:164',
    )

    return {
        "field": FIELD,
        "splitting_degree": 3,
        "source_points": source_points,
        "carrier_roots": carrier_roots,
        "residual_degrees": [len(poly) - 1 for poly in residuals],
        "parameter_degrees": {
            "Pbar": len(p_bivariate) - 1,
            "C": len(companion) - 1,
        },
        "x_degrees": {
            "carrier": len(carrier) - 1,
            "residual_product": len(residual_product) - 1,
            "resultant": len(resultant) - 1,
            "predicted": len(predicted) - 1,
        },
        "resultant_scalar": scalar[0],
        "resultant_nonzero": resultant != [0],
        "factorization_exact": remainder == [0] and len(scalar) == 1,
        "source_factorization_exact": (
            source_remainder == [0]
            and recovered_residuals == residual_product
        ),
    }


def payload() -> dict[str, object]:
    result = {
        "status": "PROVED_EXACT_FACTORIZATION_ROUTE_CUT",
        "finite_regression": regression(),
        "theorem": {
            "resultant": (
                "Res(Pbar,C)=unit*R_U^(a-1)*product_j(Rtilde_j)"
            ),
            "resultant_zero": "IMPOSSIBLE",
            "extra_divisor": "ONLY_RESIDUAL_SOURCE_MULTIPLIERS",
            "next_target": "MINIMUM_ROW_COMPLEMENTARY_DEFECT_RIGIDITY",
            "cap_68": "OPEN",
            "active_owner": "NONE",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    finite = data["finite_regression"]
    require(
        finite['factorization_exact'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:216',
    )
    require(
        finite['source_factorization_exact'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:217',
    )
    require(
        finite['resultant_nonzero'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:218',
    )
    require(
        finite['parameter_degrees'] == {'Pbar': 2, 'C': 3},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:219',
    )
    require(
        finite['x_degrees']['resultant'] == 18,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:220',
    )
    require(
        finite['x_degrees']['predicted'] == 18,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:221',
    )
    require(
        finite['residual_degrees'] == [1, 1, 2],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:222',
    )


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
            json.dumps(data, indent=2, sort_keys=True) + "\n"
        )
    if args.check:
        require(
            json.loads(CERTIFICATE.read_text()) == data,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_homogeneous_resultant_factorization.py:239',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["finite_regression"]["x_degrees"]["resultant"] -= 1
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("homogeneous resultant factorization: PASS")
    print("resultant-zero route cut: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
