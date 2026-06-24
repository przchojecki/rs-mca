#!/usr/bin/env python3
"""Verify the M1 good beta-pushforward spectral audit rows."""

from __future__ import annotations

import argparse
import cmath
import json
import math
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

import experimental.scripts.verify_m1_depth_two_line_conic_resonance_reduction as m1


AUDIT_CASES = (
    (17, 8),
    (17, 16),
    (31, 6),
    (31, 10),
    (43, 6),
    (43, 14),
    (61, 10),
    (61, 12),
    (61, 20),
    (73, 8),
    (73, 12),
    (97, 12),
    (97, 16),
    (109, 12),
    (109, 18),
    (109, 27),
    (127, 9),
    (127, 14),
    (127, 18),
    (127, 21),
)

EXPECTED_ROWS = {
    (17, 8): (
        98, 1.1361004999, 1.1361004999, 1.0588235294,
        0.4744784060, 0.2235100611, 0.1604222370, 0.5008643049,
    ),
    (17, 16): (
        98, 1.5728968500, 1.5728968500, 1.0588235294,
        0.4632352941, 0.2694629736, 0.1210446885, 0.4787888411,
    ),
    (31, 6): (
        486, 2.3225806452, 2.3225806452, 2.2580645161,
        0.6634504452, 0.5521691216, 0.5956833972, 0.8916306427,
    ),
    (31, 10): (
        486, 1.8416183853, 3.1043892896, 3.1043892896,
        0.5965213065, 0.3935483871, 0.8914205479, 1.0725988356,
    ),
    (43, 6): (
        1568, 3.0697674419, 3.2558139535, 3.2558139535,
        1.1366043634, 0.9002934041, 0.6522692703, 1.3104673518,
    ),
    (43, 14): (
        1568, 2.5116279070, 4.1755606367, 4.1755606367,
        0.8267620588, 0.5021779037, 0.8830649777, 1.2096856024,
    ),
    (61, 10): (
        3638, 3.1564925354, 4.6342117655, 4.6342117655,
        1.0413952974, 0.7253908491, 1.1549828950, 1.5551493990,
    ),
    (61, 12): (
        3638, 3.7704918033, 5.0163934426, 5.0163934426,
        0.8927070383, 0.6368113387, 0.6915699414, 1.1292452524,
    ),
    (61, 20): (
        3638, 4.1651103505, 5.3219296886, 5.3219296886,
        1.0676033635, 0.5499480809, 0.9151432864, 1.4061522593,
    ),
    (73, 8): (
        4452, 3.3972602740, 3.9136778741, 3.9136778741,
        1.0215128288, 0.7235353976, 1.0631452044, 1.4743697586,
    ),
    (73, 12): (
        4452, 3.3972602740, 5.5068493151, 5.5068493151,
        0.8625907978, 0.4811884192, 1.0433365298, 1.3537407429,
    ),
    (97, 12): (
        8220, 2.4147368394, 3.6118420031, 3.6118420031,
        0.9058943297, 0.3631084660, 0.6312463166, 1.1041360644,
    ),
    (97, 16): (
        8220, 3.1778878253, 3.9489699606, 3.9489699606,
        0.8764288851, 0.3376091912, 0.8280980376, 1.2057669553,
    ),
    (109, 12): (
        11750, 3.9816513761, 5.6717827398, 5.6717827398,
        1.1119173117, 0.8039426154, 1.2278896782, 1.6565244248,
    ),
    (109, 18): (
        11750, 3.9816513761, 4.7522935780, 4.7522935780,
        0.9676363750, 0.4518468641, 0.8838514219, 1.3105393891,
    ),
    (109, 27): (
        11750, 3.9872656889, 4.6710181306, 4.6710181306,
        0.8757048097, 0.3973402927, 0.5079449321, 1.0123571345,
    ),
    (127, 9): (
        12406, 3.5511811024, 3.8582677165, 3.8582677165,
        0.9915857812, 0.7258323902, 0.7704811722, 1.2557402591,
    ),
    (127, 14): (
        12406, 4.8036624425, 5.1781602661, 5.1781602661,
        0.9401651247, 0.4350589111, 1.0542609262, 1.4125779845,
    ),
    (127, 18): (
        12406, 3.7751417349, 4.1417322835, 4.1417322835,
        0.8755124649, 0.4019596469, 0.5311890425, 1.0240526721,
    ),
    (127, 21): (
        12406, 4.8036624425, 4.8036624425, 4.6769325284,
        0.8972861099, 0.3888406786, 0.7390713327, 1.1624752892,
    ),
}

EXPECTED_PRINCIPAL_TRACE_ROWS = {
    17: (194, 62, -14, 15, 19, -48),
    31: (758, 142, -66, 33, 33, -132),
    43: (1526, 238, 168, 45, 45, 78),
    61: (3246, 354, -178, 63, 63, -304),
    73: (4782, 402, 284, 75, 75, 134),
    97: (8670, 546, 380, 99, 99, 182),
    109: (11022, 642, -370, 111, 111, -592),
    127: (15184, 692, 502, 129, 129, 244),
}

EXPECTED_BETA_FIBER_SINGULAR_ROWS = {
    17: ((1, 8, 15), (1, 8, 15)),
    31: ((1, 5, 25), (1, 5, 25)),
    43: ((1, 6, 16, 35, 36), (1, 6, 16, 19, 20, 28, 34, 35, 36)),
    61: ((1, 13, 47), (1, 13, 47)),
    73: ((1, 2, 8, 37, 64), (1, 2, 4, 8, 37, 40, 42, 55, 64)),
    97: ((1, 24, 35, 61, 93), (1, 12, 24, 32, 35, 61, 89, 93, 94)),
    109: ((1, 45, 63), (1, 38, 45, 63, 66)),
    127: ((1, 19, 107), (1, 19, 20, 107, 108)),
}

EXPECTED_BETA_FIBER_TRACE_ROWS = {
    17: (4, 5, 1, 8, -14),
    31: (16, 30, 56, 1, -66),
    43: (10, 10, 78, 1, 168),
    61: (20, 4, 116, 1, -178),
    73: (17, 18, 138, 1, 284),
    97: (17, 17, 186, 1, 380),
    109: (29, 59, 212, 1, -370),
    127: (24, 15, 248, 1, 502),
}

BETA_SUPPORT_Z_DEGREE_EIGHT = (
    6561,
    8019,
    -57348,
    -85860,
    164403,
    318429,
    -110031,
    -450805,
    -217802,
)

EXPECTED_BETA_FIBER_QUOTIENT_SUPPORT_ROWS = {
    17: ((2, 6), (2, 6, 16)),
    31: ((2, 30), (2, 26, 30)),
    43: ((2, 5, 8, 10, 42), (2, 5, 8, 10, 34, 42)),
    61: ((2, 60), (2, 12, 60)),
    73: ((2, 9, 39, 59, 72), (2, 9, 39, 59, 72)),
    97: ((2, 4, 20, 29, 96), (2, 4, 20, 29, 96)),
    109: ((2, 104, 108), (2, 59, 104, 108)),
    127: ((1, 2, 126), (1, 2, 69, 126)),
}

TOLERANCE = 1e-8
BETA_TRACE_CACHE: dict[int, list[int]] = {}
BETA_INVERSION_CACHE: dict[int, dict[str, int]] = {}
BETA_LEFT_TRACE_CACHE: dict[tuple[int, int], list[list[complex]]] = {}
BETA_RATIO_RESONANCE_CACHE: dict[int, dict[str, int]] = {}


def good_pushforward_matrix(p: int, quotient_order: int) -> tuple[list[list[int]], int]:
    logs = m1.log_table(p)
    matrix = [[0 for _ in range(quotient_order)] for _ in range(quotient_order)]
    point_count = 0
    for alpha in range(1, p):
        alpha_label = logs[alpha] % quotient_order
        for ratio in range(1, p):
            if not m1.ratio_surface_beta_pushforward_good(p, alpha, ratio):
                continue
            roots = m1.ratio_surface_affine_beta_roots(p, alpha, ratio)
            for beta in roots:
                discriminant = m1.ratio_surface_binary_discriminants(
                    p,
                    alpha,
                    beta,
                    ratio,
                )[0]
                if discriminant == 0:
                    continue
                beta_label = logs[beta] % quotient_order
                matrix[alpha_label][beta_label] += m1.legendre(discriminant, p)
                point_count += 1
    return matrix, point_count


def principal_trace_case(p: int) -> dict[str, Any]:
    direct_trace = 0
    base_trace = 0
    full_middle_trace = 0
    full_branch_trace = 0
    good_base_count = 0
    deleted_base_count = 0
    for alpha in range(1, p):
        for ratio in range(1, p):
            middle_factor = m1.ratio_surface_beta_middle_factor(
                p,
                alpha,
                ratio,
            )
            branch_factor = m1.ratio_surface_beta_branch_factor(
                p,
                alpha,
                ratio,
            )
            full_middle_trace += m1.legendre(ratio * middle_factor, p)
            full_branch_trace += m1.legendre(alpha * branch_factor, p)
            if not m1.ratio_surface_beta_pushforward_good(p, alpha, ratio):
                deleted_base_count += 1
                continue
            good_base_count += 1
            direct_contribution = 0
            for beta in m1.ratio_surface_affine_beta_roots(p, alpha, ratio):
                discriminant = m1.ratio_surface_binary_discriminants(
                    p,
                    alpha,
                    beta,
                    ratio,
                )[0]
                direct_contribution += m1.legendre(discriminant, p)
            base_contribution = (
                m1.legendre(ratio * middle_factor, p)
                + m1.legendre(alpha * branch_factor, p)
            )
            if direct_contribution != base_contribution:
                raise AssertionError(
                    (
                        p,
                        alpha,
                        ratio,
                        direct_contribution,
                        base_contribution,
                    )
                )
            direct_trace += direct_contribution
            base_trace += base_contribution
    if direct_trace != base_trace:
        raise AssertionError((p, direct_trace, base_trace))
    expected_middle_trace = p + 2 * m1.legendre(-3, p)
    expected_branch_trace = p + 2
    if full_middle_trace != expected_middle_trace:
        raise AssertionError((p, full_middle_trace, expected_middle_trace))
    if full_branch_trace != expected_branch_trace:
        raise AssertionError((p, full_branch_trace, expected_branch_trace))
    deleted_correction = base_trace - full_middle_trace - full_branch_trace
    if abs(deleted_correction) > 2 * deleted_base_count:
        raise AssertionError((p, deleted_correction, deleted_base_count))
    return {
        "p": p,
        "good_base_count": good_base_count,
        "deleted_base_count": deleted_base_count,
        "principal_trace": direct_trace,
        "full_middle_trace": full_middle_trace,
        "full_branch_trace": full_branch_trace,
        "expected_full_middle_trace": expected_middle_trace,
        "expected_full_branch_trace": expected_branch_trace,
        "deleted_correction": deleted_correction,
        "principal_trace_ratio": round(abs(direct_trace) / p, 10),
        "full_torus_trace_ratio": round(
            abs(full_middle_trace + full_branch_trace) / p,
            10,
        ),
        "deleted_correction_ratio": round(abs(deleted_correction) / p, 10),
        "deleted_base_ratio": round(deleted_base_count / p, 10),
    }


def alpha_marginal_reduction_case(
    p: int,
    quotient_order: int,
    matrix: list[list[int]],
) -> dict[str, Any]:
    logs = m1.log_table(p)
    root = cmath.exp(2j * math.pi / quotient_order)
    deleted_base_count = 0
    for alpha in range(1, p):
        for ratio in range(1, p):
            deleted_base_count += int(
                not m1.ratio_surface_beta_pushforward_good(p, alpha, ratio)
            )

    inverse_minus_two = pow(-2, -1, p)
    row_sums = [sum(row) for row in matrix]
    max_alpha_coefficient = 0.0
    max_full_middle = 0.0
    max_full_branch = 0.0
    max_boundary = 0.0
    max_matrix_formula_error = 0.0
    max_branch_formula_error = 0.0

    for character_exponent in range(1, quotient_order):
        matrix_coefficient = sum(
            row_sums[label] * root ** (character_exponent * label)
            for label in range(quotient_order)
        )
        good_base = 0j
        full_middle = 0j
        full_branch = 0j
        for alpha in range(1, p):
            psi = root ** (character_exponent * (logs[alpha] % quotient_order))
            for ratio in range(1, p):
                middle_factor = m1.ratio_surface_beta_middle_factor(
                    p,
                    alpha,
                    ratio,
                )
                branch_factor = m1.ratio_surface_beta_branch_factor(
                    p,
                    alpha,
                    ratio,
                )
                middle_term = m1.legendre(ratio * middle_factor, p)
                branch_term = m1.legendre(alpha * branch_factor, p)
                full_middle += psi * middle_term
                full_branch += psi * branch_term
                if m1.ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    good_base += psi * (middle_term + branch_term)

        psi_minus_two = root ** (
            character_exponent * (logs[(-2) % p] % quotient_order)
        )
        psi_inverse_minus_two = root ** (
            character_exponent * (logs[inverse_minus_two] % quotient_order)
        )
        expected_full_branch = p * (1 + psi_minus_two + psi_inverse_minus_two)
        boundary = good_base - full_middle - full_branch
        matrix_formula_error = abs(matrix_coefficient - good_base)
        branch_formula_error = abs(full_branch - expected_full_branch)

        if matrix_formula_error > 1000 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    quotient_order,
                    character_exponent,
                    matrix_coefficient,
                    good_base,
                )
            )
        if branch_formula_error > 1000 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    quotient_order,
                    character_exponent,
                    full_branch,
                    expected_full_branch,
                )
            )
        if abs(boundary) > 2 * deleted_base_count + 1000 * TOLERANCE:
            raise AssertionError(
                (p, quotient_order, character_exponent, boundary)
            )

        max_alpha_coefficient = max(max_alpha_coefficient, abs(matrix_coefficient))
        max_full_middle = max(max_full_middle, abs(full_middle))
        max_full_branch = max(max_full_branch, abs(full_branch))
        max_boundary = max(max_boundary, abs(boundary))
        max_matrix_formula_error = max(
            max_matrix_formula_error,
            matrix_formula_error,
        )
        max_branch_formula_error = max(
            max_branch_formula_error,
            branch_formula_error,
        )

    return {
        "p": p,
        "quotient_order": quotient_order,
        "max_alpha_marginal_coefficient_ratio": round(
            max_alpha_coefficient / p,
            10,
        ),
        "max_alpha_full_middle_ratio": round(max_full_middle / p, 10),
        "max_alpha_full_branch_ratio": round(max_full_branch / p, 10),
        "max_alpha_boundary_ratio": round(max_boundary / p, 10),
        "max_alpha_matrix_formula_error": round(max_matrix_formula_error, 12),
        "max_alpha_branch_formula_error": round(max_branch_formula_error, 12),
    }


def alpha_middle_elliptic_case(p: int) -> dict[str, Any]:
    expected_singular = tuple(sorted({1, (-3) % p, (-pow(3, -1, p)) % p}))
    singular_parameters = []
    max_fiber_trace = 0
    max_fiber_trace_parameter = 0
    for alpha in range(1, p):
        discriminant = (
            48
            * alpha
            * alpha
            * (alpha - 1)
            * (alpha - 1)
            * (alpha + 3)
            * (3 * alpha + 1)
        ) % p
        repeated_root = False
        fiber_trace = 0
        linear = (-3 * alpha * alpha - 2 * alpha - 3) % p
        for ratio in range(p):
            middle_factor = m1.ratio_surface_beta_middle_factor(
                p,
                alpha,
                ratio,
            )
            cubic_value = ratio * middle_factor % p
            cubic_derivative = (
                12 * alpha * ratio * ratio + 2 * linear * ratio + 4 * alpha
            ) % p
            repeated_root = repeated_root or (
                cubic_value == 0 and cubic_derivative == 0
            )
            if ratio != 0:
                fiber_trace += m1.legendre(cubic_value, p)
        if repeated_root != (discriminant == 0):
            raise AssertionError((p, alpha, repeated_root, discriminant))
        if repeated_root:
            singular_parameters.append(alpha)
        else:
            if abs(fiber_trace) > 2 * math.sqrt(p) + TOLERANCE:
                raise AssertionError((p, alpha, fiber_trace))
        if abs(fiber_trace) > max_fiber_trace:
            max_fiber_trace = abs(fiber_trace)
            max_fiber_trace_parameter = alpha
    if tuple(singular_parameters) != expected_singular:
        raise AssertionError((p, singular_parameters, expected_singular))
    return {
        "p": p,
        "singular_parameters": singular_parameters,
        "max_fiber_trace": max_fiber_trace,
        "max_fiber_trace_parameter": max_fiber_trace_parameter,
        "max_fiber_trace_sqrt_ratio": round(max_fiber_trace / math.sqrt(p), 10),
        "max_fiber_trace_p_ratio": round(max_fiber_trace / p, 10),
    }


def poly_value_mod(p: int, value: int, coefficients: tuple[int, ...]) -> int:
    total = 0
    for coefficient in coefficients:
        total = (total * value + coefficient) % p
    return total


def beta_fiber_delta_alpha_derivative(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    a = alpha
    b = beta
    r = ratio
    return (
        -6 * a * a * r * r
        + 2
        * a
        * (3 * b * b * r - b * r * r - b * r + 3 * r * r * r - r * r + 3 * r)
        - 3 * b * b * r * r
        + b * b * r
        - 3 * b * b
        + b * r * r
        + b * r
        - 3 * r * r
    ) % p


def beta_fiber_delta_ratio_derivative(
    p: int,
    alpha: int,
    beta: int,
    ratio: int,
) -> int:
    a = alpha
    b = beta
    r = ratio
    return (
        -4 * a * a * a * r
        + a
        * a
        * (3 * b * b - 2 * b * r - b + 9 * r * r - 2 * r + 3)
        + a * (-6 * b * b * r + b * b + 2 * b * r + b - 6 * r)
        + 2 * b * b
    ) % p


def beta_fiber_singular_support_value(p: int, beta: int) -> int:
    quartic = poly_value_mod(p, beta, (9, -6, -5, -6, 9))
    degree_sixteen = poly_value_mod(
        p,
        beta,
        (
            6561,
            8019,
            -4860,
            -29727,
            4023,
            57528,
            54777,
            -73453,
            -139136,
            -73453,
            54777,
            57528,
            4023,
            -29727,
            -4860,
            8019,
            6561,
        ),
    )
    return (
        beta
        * (beta - 1)
        * (beta * beta + beta + 1)
        * (9 * beta * beta + 14 * beta + 9)
        * quartic
        * degree_sixteen
    ) % p


def beta_fiber_singular_quotient_support_value(p: int, z_value: int) -> int:
    degree_eight = poly_value_mod(p, z_value, BETA_SUPPORT_Z_DEGREE_EIGHT)
    return (
        (z_value - 2)
        * (z_value + 1)
        * (9 * z_value + 14)
        * (9 * z_value * z_value - 6 * z_value - 23)
        * degree_eight
    ) % p


def beta_fiber_singularity_case(p: int) -> dict[str, Any]:
    singular_beta_values = []
    support_beta_values = []
    singular_point_count = 0
    for beta in range(1, p):
        in_support = beta_fiber_singular_support_value(p, beta) == 0
        if in_support:
            support_beta_values.append(beta)
        beta_is_singular = False
        for alpha in range(1, p):
            for ratio in range(1, p):
                if m1.ratio_surface_delta(p, alpha, beta, ratio) != 0:
                    continue
                if beta_fiber_delta_alpha_derivative(p, alpha, beta, ratio) != 0:
                    continue
                if beta_fiber_delta_ratio_derivative(p, alpha, beta, ratio) != 0:
                    continue
                if not in_support:
                    raise AssertionError((p, beta, alpha, ratio, "off-support"))
                beta_is_singular = True
                singular_point_count += 1
        if beta_is_singular:
            singular_beta_values.append(beta)
    return {
        "p": p,
        "singular_beta_values": singular_beta_values,
        "support_beta_values": support_beta_values,
        "singular_beta_count": len(singular_beta_values),
        "support_beta_count": len(support_beta_values),
        "singular_point_count": singular_point_count,
    }


def beta_fiber_quotient_support_case(p: int) -> dict[str, Any]:
    beta_orbits: dict[int, list[int]] = {}
    max_support_inversion_error = 0
    for beta in range(1, p):
        inverse_beta = pow(beta, -1, p)
        beta_in_support = beta_fiber_singular_support_value(p, beta) == 0
        inverse_in_support = (
            beta_fiber_singular_support_value(p, inverse_beta) == 0
        )
        max_support_inversion_error = max(
            max_support_inversion_error,
            abs(int(beta_in_support) - int(inverse_in_support)),
        )
        z_value = (beta + inverse_beta) % p
        beta_orbits.setdefault(z_value, []).append(beta)

    support_z_values = sorted(
        z_value
        for z_value, orbit in beta_orbits.items()
        if any(beta_fiber_singular_support_value(p, beta) == 0 for beta in orbit)
    )
    quotient_polynomial_roots = sorted(
        z_value
        for z_value in range(p)
        if beta_fiber_singular_quotient_support_value(p, z_value) == 0
    )
    quotient_image_roots = sorted(
        z_value
        for z_value in beta_orbits
        if beta_fiber_singular_quotient_support_value(p, z_value) == 0
    )
    if max_support_inversion_error != 0:
        raise AssertionError((p, max_support_inversion_error))
    if support_z_values != quotient_image_roots:
        raise AssertionError((p, support_z_values, quotient_image_roots))
    if len(quotient_polynomial_roots) > 13:
        raise AssertionError((p, quotient_polynomial_roots))
    return {
        "p": p,
        "support_z_values": support_z_values,
        "quotient_polynomial_roots": quotient_polynomial_roots,
        "quotient_image_roots": quotient_image_roots,
        "support_z_count": len(support_z_values),
        "quotient_polynomial_root_count": len(quotient_polynomial_roots),
        "nonimage_root_count": (
            len(quotient_polynomial_roots) - len(quotient_image_roots)
        ),
        "max_support_inversion_error": max_support_inversion_error,
    }


def beta_ratio_resonance_case(p: int) -> dict[str, int]:
    if p in BETA_RATIO_RESONANCE_CACHE:
        return BETA_RATIO_RESONANCE_CACHE[p]
    fixed_ratio_counts = {beta_ratio: 0 for beta_ratio in range(1, p)}
    split_base_count = 0
    for alpha in range(1, p):
        for ratio in range(1, p):
            if not m1.ratio_surface_beta_pushforward_good(p, alpha, ratio):
                continue
            discriminant = m1.ratio_surface_beta_discriminant(p, alpha, ratio)
            if m1.legendre(discriminant, p) != 1:
                continue
            roots = m1.ratio_surface_affine_beta_roots(p, alpha, ratio)
            if len(roots) != 2:
                raise AssertionError((p, alpha, ratio, roots))
            root_ratio = roots[0] * pow(roots[1], -1, p) % p
            inverse_ratio = pow(root_ratio, -1, p)
            if m1.ratio_surface_beta_ratio_resonance(
                p,
                alpha,
                ratio,
                root_ratio,
            ) != 0:
                raise AssertionError((p, alpha, ratio, roots, root_ratio))
            if m1.ratio_surface_beta_ratio_resonance(
                p,
                alpha,
                ratio,
                inverse_ratio,
            ) != 0:
                raise AssertionError((p, alpha, ratio, roots, inverse_ratio))
            fixed_ratio_counts[root_ratio] += 1
            split_base_count += 1
    max_fixed_ratio = max(
        fixed_ratio_counts,
        key=lambda beta_ratio: fixed_ratio_counts[beta_ratio],
    )
    max_fixed_ratio_count = fixed_ratio_counts[max_fixed_ratio]
    if max_fixed_ratio_count > 4 * (p - 1):
        raise AssertionError((p, max_fixed_ratio, max_fixed_ratio_count))

    BETA_RATIO_RESONANCE_CACHE[p] = {
        "p": p,
        "max_fixed_ratio": max_fixed_ratio,
        "max_fixed_ratio_count": max_fixed_ratio_count,
        "split_base_count": split_base_count,
    }
    return BETA_RATIO_RESONANCE_CACHE[p]


def beta_sheet_quotient_energy_case(
    p: int,
    quotient_order: int,
) -> dict[str, float | int]:
    logs = m1.log_table(p)
    root = cmath.exp(2j * math.pi / quotient_order)
    ratio_case = beta_ratio_resonance_case(p)
    split_base_count = 0
    same_quotient_count = 0
    exact_energy = 0.0
    for alpha in range(1, p):
        for ratio in range(1, p):
            if not m1.ratio_surface_beta_pushforward_good(p, alpha, ratio):
                continue
            if m1.legendre(m1.ratio_surface_beta_discriminant(p, alpha, ratio), p) != 1:
                continue
            roots = m1.ratio_surface_affine_beta_roots(p, alpha, ratio)
            if len(roots) != 2:
                raise AssertionError((p, quotient_order, alpha, ratio, roots))
            labels = [logs[beta] % quotient_order for beta in roots]
            same_quotient_count += int(labels[0] == labels[1])
            split_base_count += 1
            for exponent in range(1, quotient_order):
                beta_kernel = (
                    root ** (exponent * labels[0])
                    + root ** (exponent * labels[1])
                )
                exact_energy += abs(beta_kernel) ** 2
    if split_base_count != ratio_case["split_base_count"]:
        raise AssertionError((p, quotient_order, split_base_count, ratio_case))

    formula_energy = (
        (2 * quotient_order - 4) * split_base_count
        + 2 * quotient_order * same_quotient_count
    )
    if abs(exact_energy - formula_energy) > 1000 * TOLERANCE:
        raise AssertionError((p, quotient_order, exact_energy, formula_energy))
    quotient_kernel_size = (p - 1) // quotient_order
    same_quotient_bound = 4 * (p - 1) * quotient_kernel_size
    if same_quotient_count > same_quotient_bound:
        raise AssertionError(
            (p, quotient_order, same_quotient_count, same_quotient_bound)
        )
    energy_bound = (
        (2 * quotient_order - 4) * (p - 1) * (p - 1)
        + 2 * quotient_order * same_quotient_bound
    )
    if formula_energy > energy_bound:
        raise AssertionError((p, quotient_order, formula_energy, energy_bound))
    return {
        "split_base_count": split_base_count,
        "same_quotient_count": same_quotient_count,
        "same_quotient_bound": same_quotient_bound,
        "formula_energy": round(formula_energy),
        "energy_bound": energy_bound,
        "energy_ratio": round(formula_energy / ((p - 1) * (p - 1)), 10),
        "max_fixed_ratio": ratio_case["max_fixed_ratio"],
        "max_fixed_ratio_count": ratio_case["max_fixed_ratio_count"],
        "max_fixed_ratio_bound": 4 * (p - 1),
        "max_formula_error": round(abs(exact_energy - formula_energy), 12),
    }


def exact_beta_trace_vector(p: int) -> list[int]:
    if p in BETA_TRACE_CACHE:
        return BETA_TRACE_CACHE[p]
    traces = [0 for _ in range(p)]
    for beta in range(1, p):
        trace = 0
        for alpha in range(1, p):
            for ratio in range(1, p):
                if not m1.ratio_surface_beta_pushforward_good(p, alpha, ratio):
                    continue
                if m1.ratio_surface_delta(p, alpha, beta, ratio) != 0:
                    continue
                discriminant = m1.ratio_surface_binary_discriminants(
                    p,
                    alpha,
                    beta,
                    ratio,
                )[0]
                sign = m1.legendre(discriminant, p)
                if sign == 0:
                    raise AssertionError((p, beta, alpha, ratio, "zero-sign"))
                base_sign = m1.legendre(
                    ratio
                    * m1.ratio_surface_beta_middle_factor(p, alpha, ratio),
                    p,
                )
                if sign != base_sign:
                    raise AssertionError((p, beta, alpha, ratio, sign, base_sign))
                trace += sign
        traces[beta] = trace
    BETA_TRACE_CACHE[p] = traces
    return traces


def beta_fiber_trace_case(p: int) -> dict[str, Any]:
    traces = exact_beta_trace_vector(p)
    max_regular_trace = 0
    max_regular_beta = 0
    max_support_trace = 0
    max_support_beta = 0
    regular_beta_count = 0
    support_beta_count = 0
    for beta in range(1, p):
        trace_size = abs(traces[beta])
        if beta_fiber_singular_support_value(p, beta) == 0:
            support_beta_count += 1
            if trace_size > max_support_trace:
                max_support_trace = trace_size
                max_support_beta = beta
        else:
            regular_beta_count += 1
            if trace_size > max_regular_trace:
                max_regular_trace = trace_size
                max_regular_beta = beta
    return {
        "p": p,
        "regular_beta_count": regular_beta_count,
        "support_beta_count": support_beta_count,
        "max_regular_trace": max_regular_trace,
        "max_regular_beta": max_regular_beta,
        "max_regular_trace_sqrt_ratio": round(
            max_regular_trace / math.sqrt(p),
            10,
        ),
        "max_regular_trace_p_ratio": round(max_regular_trace / p, 10),
        "max_support_trace": max_support_trace,
        "max_support_beta": max_support_beta,
        "max_support_trace_p_ratio": round(max_support_trace / p, 10),
        "total_trace": sum(traces),
    }


def beta_marginal_trace_reduction_case(
    p: int,
    quotient_order: int,
    matrix: list[list[int]],
) -> dict[str, Any]:
    traces = exact_beta_trace_vector(p)
    logs = m1.log_table(p)
    root = cmath.exp(2j * math.pi / quotient_order)
    column_sums = [
        sum(matrix[row][column] for row in range(quotient_order))
        for column in range(quotient_order)
    ]
    grouped_traces = [0 for _ in range(quotient_order)]
    for beta in range(1, p):
        grouped_traces[logs[beta] % quotient_order] += traces[beta]
    if grouped_traces != column_sums:
        raise AssertionError((p, quotient_order, grouped_traces, column_sums))

    max_coefficient = 0.0
    max_formula_error = 0.0
    for character_exponent in range(1, quotient_order):
        trace_coefficient = sum(
            traces[beta]
            * root ** (character_exponent * (logs[beta] % quotient_order))
            for beta in range(1, p)
        )
        matrix_coefficient = sum(
            column_sums[label] * root ** (character_exponent * label)
            for label in range(quotient_order)
        )
        formula_error = abs(trace_coefficient - matrix_coefficient)
        if formula_error > 1000 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    quotient_order,
                    character_exponent,
                    trace_coefficient,
                    matrix_coefficient,
                )
            )
        max_formula_error = max(max_formula_error, formula_error)
        max_coefficient = max(max_coefficient, abs(trace_coefficient))
    return {
        "p": p,
        "quotient_order": quotient_order,
        "max_beta_marginal_coefficient_ratio": round(max_coefficient / p, 10),
        "max_beta_marginal_trace_formula_error": round(
            max_formula_error,
            12,
        ),
    }


def beta_marginal_chebyshev_quotient_case(
    p: int,
    quotient_order: int,
    matrix: list[list[int]],
) -> dict[str, float | int]:
    traces = exact_beta_trace_vector(p)
    logs = m1.log_table(p)
    root = cmath.exp(2j * math.pi / quotient_order)
    column_sums = [
        sum(matrix[row][column] for row in range(quotient_order))
        for column in range(quotient_order)
    ]

    beta_orbits: dict[int, list[int]] = {}
    quotient_traces: dict[int, int] = {}
    max_orbit_trace_error = 0
    for beta in range(1, p):
        z_value = (beta + pow(beta, -1, p)) % p
        beta_orbits.setdefault(z_value, []).append(beta)
    for z_value, orbit in beta_orbits.items():
        if len(orbit) not in (1, 2):
            raise AssertionError((p, z_value, orbit))
        trace_value = traces[orbit[0]]
        for beta in orbit:
            max_orbit_trace_error = max(
                max_orbit_trace_error,
                abs(trace_value - traces[beta]),
            )
        quotient_traces[z_value] = trace_value
    if max_orbit_trace_error != 0:
        raise AssertionError((p, max_orbit_trace_error))

    max_formula_error = 0.0
    max_kernel_size = 0.0
    max_second_moment_error = 0.0
    max_nonquadratic_second_moment = 0.0
    quadratic_second_moment = 0.0
    for character_exponent in range(1, quotient_order):
        direct_coefficient = sum(
            column_sums[label] * root ** (character_exponent * label)
            for label in range(quotient_order)
        )
        quotient_coefficient = 0j
        kernel_second_moment = 0.0
        for z_value, orbit in beta_orbits.items():
            chebyshev_kernel = sum(
                root ** (character_exponent * (logs[beta] % quotient_order))
                for beta in orbit
            )
            max_kernel_size = max(max_kernel_size, abs(chebyshev_kernel))
            kernel_second_moment += abs(chebyshev_kernel) ** 2
            quotient_coefficient += quotient_traces[z_value] * chebyshev_kernel
        is_quadratic_character = (
            quotient_order % 2 == 0
            and character_exponent == quotient_order // 2
        )
        expected_second_moment = (2 * p - 4) if is_quadratic_character else (p - 3)
        second_moment_error = abs(kernel_second_moment - expected_second_moment)
        if second_moment_error > 1000 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    quotient_order,
                    character_exponent,
                    kernel_second_moment,
                    expected_second_moment,
                )
            )
        max_second_moment_error = max(
            max_second_moment_error,
            second_moment_error,
        )
        if is_quadratic_character:
            quadratic_second_moment = kernel_second_moment
        else:
            max_nonquadratic_second_moment = max(
                max_nonquadratic_second_moment,
                kernel_second_moment,
            )
        formula_error = abs(direct_coefficient - quotient_coefficient)
        if formula_error > 1000 * TOLERANCE:
            raise AssertionError(
                (
                    p,
                    quotient_order,
                    character_exponent,
                    direct_coefficient,
                    quotient_coefficient,
                )
            )
        max_formula_error = max(max_formula_error, formula_error)
    return {
        "quotient_point_count": len(beta_orbits),
        "fixed_orbit_count": sum(
            1 for orbit in beta_orbits.values() if len(orbit) == 1
        ),
        "paired_orbit_count": sum(
            1 for orbit in beta_orbits.values() if len(orbit) == 2
        ),
        "max_orbit_trace_error": max_orbit_trace_error,
        "max_chebyshev_kernel_size": round(max_kernel_size, 12),
        "max_chebyshev_second_moment_error": round(max_second_moment_error, 12),
        "max_nonquadratic_second_moment": round(max_nonquadratic_second_moment, 12),
        "quadratic_second_moment": round(quadratic_second_moment, 12),
        "max_chebyshev_formula_error": round(max_formula_error, 12),
    }


def exact_beta_left_trace_vectors(
    p: int,
    quotient_order: int,
) -> list[list[complex]]:
    cache_key = (p, quotient_order)
    if cache_key in BETA_LEFT_TRACE_CACHE:
        return BETA_LEFT_TRACE_CACHE[cache_key]
    logs = m1.log_table(p)
    root = cmath.exp(2j * math.pi / quotient_order)
    traces = [[0j for _ in range(p)] for _ in range(quotient_order)]
    for alpha in range(1, p):
        alpha_label = logs[alpha] % quotient_order
        left_values = [
            root ** (left_character * alpha_label)
            for left_character in range(quotient_order)
        ]
        for ratio in range(1, p):
            if not m1.ratio_surface_beta_pushforward_good(p, alpha, ratio):
                continue
            for beta in m1.ratio_surface_affine_beta_roots(p, alpha, ratio):
                discriminant = m1.ratio_surface_binary_discriminants(
                    p,
                    alpha,
                    beta,
                    ratio,
                )[0]
                sign = m1.legendre(discriminant, p)
                for left_character, left_value in enumerate(left_values):
                    traces[left_character][beta] += sign * left_value
    BETA_LEFT_TRACE_CACHE[cache_key] = traces
    return traces


def beta_line_dihedral_quotient_case(
    p: int,
    quotient_order: int,
    matrix: list[list[int]],
) -> dict[str, float | int]:
    logs = m1.log_table(p)
    root = cmath.exp(2j * math.pi / quotient_order)
    traces = exact_beta_left_trace_vectors(p, quotient_order)
    beta_orbits: dict[int, list[int]] = {}
    for beta in range(1, p):
        z_value = (beta + pow(beta, -1, p)) % p
        beta_orbits.setdefault(z_value, []).append(beta)

    max_trace_inversion_error = 0.0
    max_grouped_matrix_error = 0.0
    max_dihedral_formula_error = 0.0
    for left_character in range(quotient_order):
        inverse_left = (-left_character) % quotient_order
        grouped_beta_trace = [0j for _ in range(quotient_order)]
        for beta in range(1, p):
            inverse_beta = pow(beta, -1, p)
            max_trace_inversion_error = max(
                max_trace_inversion_error,
                abs(traces[left_character][inverse_beta] - traces[inverse_left][beta]),
            )
            grouped_beta_trace[logs[beta] % quotient_order] += traces[
                left_character
            ][beta]
        for right in range(quotient_order):
            matrix_group = sum(
                matrix[left][right] * root ** (left_character * left)
                for left in range(quotient_order)
            )
            max_grouped_matrix_error = max(
                max_grouped_matrix_error,
                abs(grouped_beta_trace[right] - matrix_group),
            )

        for right_character in range(1, quotient_order):
            direct_coefficient = sum(
                grouped_beta_trace[right] * root ** (right_character * right)
                for right in range(quotient_order)
            )
            quotient_coefficient = 0j
            for orbit in beta_orbits.values():
                if len(orbit) == 1:
                    beta = orbit[0]
                    beta_label = logs[beta] % quotient_order
                    quotient_coefficient += (
                        root ** (right_character * beta_label)
                        * traces[left_character][beta]
                    )
                    continue
                beta = orbit[0]
                beta_label = logs[beta] % quotient_order
                quotient_coefficient += (
                    root ** (right_character * beta_label)
                    * traces[left_character][beta]
                )
                quotient_coefficient += (
                    root ** (-right_character * beta_label)
                    * traces[inverse_left][beta]
                )
            max_dihedral_formula_error = max(
                max_dihedral_formula_error,
                abs(direct_coefficient - quotient_coefficient),
            )
    if max_trace_inversion_error > 1000 * TOLERANCE:
        raise AssertionError((p, quotient_order, max_trace_inversion_error))
    if max_grouped_matrix_error > 1000 * TOLERANCE:
        raise AssertionError((p, quotient_order, max_grouped_matrix_error))
    if max_dihedral_formula_error > 1000 * TOLERANCE:
        raise AssertionError((p, quotient_order, max_dihedral_formula_error))
    return {
        "quotient_point_count": len(beta_orbits),
        "max_trace_inversion_error": round(max_trace_inversion_error, 12),
        "max_grouped_matrix_error": round(max_grouped_matrix_error, 12),
        "max_dihedral_formula_error": round(max_dihedral_formula_error, 12),
    }


def centered_frobenius_square(matrix: list[list[int]]) -> float:
    order = len(matrix)
    row_sums = [sum(row) for row in matrix]
    column_sums = [
        sum(matrix[row][column] for row in range(order))
        for column in range(order)
    ]
    total = sum(row_sums)
    norm_square = 0.0
    for row in range(order):
        for column in range(order):
            centered = (
                matrix[row][column]
                - row_sums[row] / order
                - column_sums[column] / order
                + total / (order * order)
            )
            norm_square += centered * centered
    return norm_square


def alpha_marginal_square(matrix: list[list[int]]) -> float:
    order = len(matrix)
    row_sums = [sum(row) for row in matrix]
    total = sum(row_sums)
    return sum((row_sum - total / order) ** 2 for row_sum in row_sums) / order


def beta_marginal_square(matrix: list[list[int]]) -> float:
    order = len(matrix)
    row_sums = [sum(row) for row in matrix]
    column_sums = [
        sum(matrix[row][column] for row in range(order))
        for column in range(order)
    ]
    total = sum(row_sums)
    return sum((column_sum - total / order) ** 2 for column_sum in column_sums) / order


def right_projected_frobenius_square(matrix: list[list[int]]) -> float:
    order = len(matrix)
    norm_square = 0.0
    for row in range(order):
        row_sum = sum(matrix[row])
        for column in range(order):
            centered = matrix[row][column] - row_sum / order
            norm_square += centered * centered
    return norm_square


def fiber_product_components(matrix: list[list[int]]) -> dict[str, float]:
    order = len(matrix)
    row_sums = [sum(row) for row in matrix]
    column_sums = [
        sum(matrix[row][column] for row in range(order))
        for column in range(order)
    ]
    total = sum(row_sums)
    joint_collision = sum(entry * entry for row in matrix for entry in row)
    alpha_collision = sum(row_sum * row_sum for row_sum in row_sums)
    beta_collision = sum(column_sum * column_sum for column_sum in column_sums)
    total_collision = total * total
    return {
        "joint_collision": float(joint_collision),
        "alpha_collision": float(alpha_collision),
        "beta_collision": float(beta_collision),
        "total_collision": float(total_collision),
        "centered_from_components": (
            joint_collision
            - alpha_collision / order
            - beta_collision / order
            + total_collision / (order * order)
        ),
        "marginal_from_components": (
            beta_collision / order - total_collision / (order * order)
        ),
        "right_projected_from_components": joint_collision - alpha_collision / order,
    }


def centered_pair_energy_square(matrix: list[list[int]]) -> float:
    order = len(matrix)
    norm_square = 0.0
    for left in range(order):
        for right in range(order):
            for other_left in range(order):
                left_kernel = (1 if left == other_left else 0) - 1 / order
                for other_right in range(order):
                    right_kernel = (1 if right == other_right else 0) - 1 / order
                    norm_square += (
                        matrix[left][right]
                        * matrix[other_left][other_right]
                        * left_kernel
                        * right_kernel
                    )
    return norm_square


def spectral_stats(
    matrix: list[list[int]],
) -> tuple[float, float, float, float, float]:
    order = len(matrix)
    root = cmath.exp(2j * math.pi / order)
    two_sided_energy = 0.0
    left_principal_energy = 0.0
    max_two_sided = 0.0
    max_beta2 = 0.0
    max_left_principal = 0.0
    for left_character in range(order):
        for right_character in range(1, order):
            coefficient = 0j
            for left in range(order):
                for right in range(order):
                    coefficient += matrix[left][right] * root ** (
                        left_character * left + right_character * right
                    )
            coefficient_size = abs(coefficient)
            max_beta2 = max(max_beta2, coefficient_size)
            if left_character == 0:
                left_principal_energy += coefficient_size ** 2
                max_left_principal = max(max_left_principal, coefficient_size)
            else:
                two_sided_energy += coefficient_size ** 2
                max_two_sided = max(max_two_sided, coefficient_size)
    return (
        two_sided_energy,
        left_principal_energy,
        max_two_sided,
        max_beta2,
        max_left_principal,
    )


def beta_line_quotient_reduction_case(matrix: list[list[int]]) -> dict[str, float]:
    order = len(matrix)
    root = cmath.exp(2j * math.pi / order)
    max_formula_error = 0.0
    max_two_sided = 0.0
    max_any = 0.0
    for left_character in range(order):
        grouped_beta_trace = []
        for right in range(order):
            grouped_beta_trace.append(
                sum(
                    matrix[left][right] * root ** (left_character * left)
                    for left in range(order)
                )
            )
        for right_character in range(1, order):
            beta_line_coefficient = sum(
                grouped_beta_trace[right] * root ** (right_character * right)
                for right in range(order)
            )
            direct_coefficient = 0j
            for left in range(order):
                for right in range(order):
                    direct_coefficient += matrix[left][right] * root ** (
                        left_character * left + right_character * right
                    )
            coefficient_size = abs(beta_line_coefficient)
            max_any = max(max_any, coefficient_size)
            if left_character != 0:
                max_two_sided = max(max_two_sided, coefficient_size)
            max_formula_error = max(
                max_formula_error,
                abs(beta_line_coefficient - direct_coefficient),
            )
    return {
        "max_beta_line_any_coefficient": round(max_any, 10),
        "max_beta_line_two_sided_coefficient": round(max_two_sided, 10),
        "max_beta_line_formula_error": round(max_formula_error, 12),
    }


def beta_prime_inversion_case(p: int) -> dict[str, int]:
    if p in BETA_INVERSION_CACHE:
        return BETA_INVERSION_CACHE[p]
    good_base_count = 0
    split_point_count = 0
    for alpha in range(1, p):
        inverse_alpha = pow(alpha, -1, p)
        for ratio in range(1, p):
            inverse_ratio = pow(ratio, -1, p)
            is_good = m1.ratio_surface_beta_pushforward_good(p, alpha, ratio)
            inverse_is_good = m1.ratio_surface_beta_pushforward_good(
                p,
                inverse_alpha,
                inverse_ratio,
            )
            if is_good != inverse_is_good:
                raise AssertionError(
                    (p, alpha, ratio, inverse_alpha, inverse_ratio)
                )
            if not is_good:
                continue
            good_base_count += 1
            roots = m1.ratio_surface_affine_beta_roots(p, alpha, ratio)
            inverse_roots = sorted(pow(beta, -1, p) for beta in roots)
            expected_roots = sorted(
                m1.ratio_surface_affine_beta_roots(
                    p,
                    inverse_alpha,
                    inverse_ratio,
                )
            )
            if inverse_roots != expected_roots:
                raise AssertionError(
                    (
                        p,
                        alpha,
                        ratio,
                        roots,
                        inverse_alpha,
                        inverse_ratio,
                        expected_roots,
                    )
                )
            for beta in roots:
                inverse_beta = pow(beta, -1, p)
                sign = m1.legendre(
                    m1.ratio_surface_binary_discriminants(
                        p,
                        alpha,
                        beta,
                        ratio,
                    )[0],
                    p,
                )
                inverse_sign = m1.legendre(
                    m1.ratio_surface_binary_discriminants(
                        p,
                        inverse_alpha,
                        inverse_beta,
                        inverse_ratio,
                    )[0],
                    p,
                )
                if sign != inverse_sign:
                    raise AssertionError(
                        (
                            p,
                            alpha,
                            beta,
                            ratio,
                            sign,
                            inverse_alpha,
                            inverse_beta,
                            inverse_ratio,
                            inverse_sign,
                        )
                    )
                split_point_count += 1

    traces = exact_beta_trace_vector(p)
    beta_trace_inversion_error = 0
    for beta in range(1, p):
        inverse_beta = pow(beta, -1, p)
        beta_trace_inversion_error = max(
            beta_trace_inversion_error,
            abs(traces[beta] - traces[inverse_beta]),
        )
    if beta_trace_inversion_error != 0:
        raise AssertionError((p, beta_trace_inversion_error))
    BETA_INVERSION_CACHE[p] = {
        "p": p,
        "good_base_count": good_base_count,
        "split_point_count": split_point_count,
        "beta_trace_inversion_error": beta_trace_inversion_error,
    }
    return BETA_INVERSION_CACHE[p]


def beta_inversion_symmetry_case(
    p: int,
    matrix: list[list[int]],
) -> dict[str, float | int]:
    prime_case = beta_prime_inversion_case(p)
    order = len(matrix)
    root = cmath.exp(2j * math.pi / order)
    matrix_error = 0
    for left in range(order):
        for right in range(order):
            matrix_error = max(
                matrix_error,
                abs(matrix[left][right] - matrix[-left % order][-right % order]),
            )
    if matrix_error != 0:
        raise AssertionError((p, order, matrix_error))

    max_grouped_trace_error = 0.0
    max_coefficient_error = 0.0
    for left_character in range(order):
        grouped_beta_trace = []
        inverse_grouped_beta_trace = []
        for right in range(order):
            grouped_beta_trace.append(
                sum(
                    matrix[left][right] * root ** (left_character * left)
                    for left in range(order)
                )
            )
            inverse_grouped_beta_trace.append(
                sum(
                    matrix[left][right] * root ** (-left_character * left)
                    for left in range(order)
                )
            )
        for right in range(order):
            max_grouped_trace_error = max(
                max_grouped_trace_error,
                abs(
                    grouped_beta_trace[right]
                    - inverse_grouped_beta_trace[-right % order]
                ),
            )
        for right_character in range(1, order):
            coefficient = sum(
                grouped_beta_trace[right] * root ** (right_character * right)
                for right in range(order)
            )
            inverse_coefficient = sum(
                inverse_grouped_beta_trace[right]
                * root ** (-right_character * right)
                for right in range(order)
            )
            max_coefficient_error = max(
                max_coefficient_error,
                abs(coefficient - inverse_coefficient),
            )
    if max_grouped_trace_error > TOLERANCE:
        raise AssertionError((p, order, max_grouped_trace_error))
    if max_coefficient_error > TOLERANCE:
        raise AssertionError((p, order, max_coefficient_error))
    return {
        "good_base_count": prime_case["good_base_count"],
        "split_point_count": prime_case["split_point_count"],
        "beta_trace_inversion_error": prime_case["beta_trace_inversion_error"],
        "matrix_inversion_error": matrix_error,
        "max_grouped_trace_inversion_error": round(max_grouped_trace_error, 12),
        "max_coefficient_inversion_error": round(max_coefficient_error, 12),
    }


def audit_case(p: int, quotient_order: int) -> dict[str, Any]:
    matrix, point_count = good_pushforward_matrix(p, quotient_order)
    frobenius_square = centered_frobenius_square(matrix)
    alpha_marginal = alpha_marginal_square(matrix)
    marginal_square = beta_marginal_square(matrix)
    right_projected_square = right_projected_frobenius_square(matrix)
    components = fiber_product_components(matrix)
    pair_square = centered_pair_energy_square(matrix)
    (
        two_sided_energy,
        left_principal_energy,
        max_two_sided,
        max_beta2,
        max_left_principal,
    ) = spectral_stats(matrix)
    alpha_reduction = alpha_marginal_reduction_case(p, quotient_order, matrix)
    beta_reduction = beta_marginal_trace_reduction_case(
        p,
        quotient_order,
        matrix,
    )
    beta_chebyshev = beta_marginal_chebyshev_quotient_case(
        p,
        quotient_order,
        matrix,
    )
    beta_line_reduction = beta_line_quotient_reduction_case(matrix)
    beta_inversion = beta_inversion_symmetry_case(p, matrix)
    beta_dihedral = beta_line_dihedral_quotient_case(
        p,
        quotient_order,
        matrix,
    )
    beta_sheet_energy = beta_sheet_quotient_energy_case(p, quotient_order)
    parseval_error = abs(
        two_sided_energy / (quotient_order * quotient_order) - frobenius_square
    )
    marginal_parseval_error = abs(
        left_principal_energy / (quotient_order * quotient_order)
        - marginal_square
    )
    pair_energy_error = abs(pair_square - frobenius_square)
    pythagorean_error = abs(
        right_projected_square - frobenius_square - marginal_square
    )
    component_centered_error = abs(
        components["centered_from_components"] - frobenius_square
    )
    component_marginal_error = abs(
        components["marginal_from_components"] - marginal_square
    )
    component_right_error = abs(
        components["right_projected_from_components"] - right_projected_square
    )
    joint_decomposition_error = abs(
        components["joint_collision"]
        - frobenius_square
        - alpha_marginal
        - marginal_square
        - components["total_collision"] / (quotient_order * quotient_order)
    )
    if parseval_error > TOLERANCE:
        raise AssertionError((p, quotient_order, two_sided_energy, frobenius_square))
    if marginal_parseval_error > TOLERANCE:
        raise AssertionError(
            (p, quotient_order, left_principal_energy, marginal_square)
        )
    if pair_energy_error > TOLERANCE:
        raise AssertionError((p, quotient_order, pair_square, frobenius_square))
    if pythagorean_error > TOLERANCE:
        raise AssertionError(
            (p, quotient_order, right_projected_square, frobenius_square)
        )
    if component_centered_error > TOLERANCE:
        raise AssertionError(
            (p, quotient_order, components["centered_from_components"])
        )
    if component_marginal_error > TOLERANCE:
        raise AssertionError(
            (p, quotient_order, components["marginal_from_components"])
        )
    if component_right_error > TOLERANCE:
        raise AssertionError(
            (p, quotient_order, components["right_projected_from_components"])
        )
    if joint_decomposition_error > TOLERANCE:
        raise AssertionError((p, quotient_order, joint_decomposition_error))
    beta_line_any_ratio = (
        beta_line_reduction["max_beta_line_any_coefficient"] / p
    )
    beta_line_two_sided_ratio = (
        beta_line_reduction["max_beta_line_two_sided_coefficient"] / p
    )
    if abs(beta_line_any_ratio - max_beta2 / p) > TOLERANCE:
        raise AssertionError((p, quotient_order, beta_line_any_ratio, max_beta2 / p))
    if abs(beta_line_two_sided_ratio - max_two_sided / p) > TOLERANCE:
        raise AssertionError(
            (p, quotient_order, beta_line_two_sided_ratio, max_two_sided / p)
        )
    if beta_line_reduction["max_beta_line_formula_error"] > TOLERANCE:
        raise AssertionError((p, quotient_order, beta_line_reduction))
    two_sided_ratio = max_two_sided / p
    beta2_ratio = max_beta2 / p
    left_principal_ratio = max_left_principal / p
    frobenius_ratio = math.sqrt(frobenius_square) / p
    alpha_marginal_ratio = math.sqrt(alpha_marginal) / p
    marginal_ratio = math.sqrt(marginal_square) / p
    right_projected_ratio = math.sqrt(right_projected_square) / p
    nonnegative_bound_ratio = math.sqrt(
        components["joint_collision"]
        + components["total_collision"] / (quotient_order * quotient_order)
    ) / p
    return {
        "p": p,
        "quotient_order": quotient_order,
        "good_point_count": point_count,
        "max_two_sided_coefficient_ratio": round(two_sided_ratio, 10),
        "max_beta2_coefficient_ratio": round(beta2_ratio, 10),
        "max_left_principal_coefficient_ratio": round(left_principal_ratio, 10),
        "centered_frobenius_ratio": round(frobenius_ratio, 10),
        "alpha_marginal_frobenius_ratio": round(alpha_marginal_ratio, 10),
        "beta_marginal_frobenius_ratio": round(marginal_ratio, 10),
        "right_projected_frobenius_ratio": round(right_projected_ratio, 10),
        "nonnegative_sufficient_bound_ratio": round(nonnegative_bound_ratio, 10),
        "joint_collision_ratio": round(
            components["joint_collision"] / (p * p),
            10,
        ),
        "alpha_collision_ratio": round(
            components["alpha_collision"] / (quotient_order * p * p),
            10,
        ),
        "beta_collision_ratio": round(
            components["beta_collision"] / (quotient_order * p * p),
            10,
        ),
        "total_collision_ratio": round(
            components["total_collision"]
            / (quotient_order * quotient_order * p * p),
            10,
        ),
        "parseval_error": round(parseval_error, 12),
        "marginal_parseval_error": round(marginal_parseval_error, 12),
        "pair_energy_error": round(pair_energy_error, 12),
        "pythagorean_error": round(pythagorean_error, 12),
        "component_centered_error": round(component_centered_error, 12),
        "component_marginal_error": round(component_marginal_error, 12),
        "component_right_error": round(component_right_error, 12),
        "joint_decomposition_error": round(joint_decomposition_error, 12),
        "alpha_marginal_reduction": alpha_reduction,
        "beta_marginal_reduction": beta_reduction,
        "beta_marginal_chebyshev_quotient": beta_chebyshev,
        "beta_line_quotient_reduction": {
            "max_beta_line_any_coefficient_ratio": round(beta_line_any_ratio, 10),
            "max_beta_line_two_sided_coefficient_ratio": round(
                beta_line_two_sided_ratio,
                10,
            ),
            "max_beta_line_formula_error": beta_line_reduction[
                "max_beta_line_formula_error"
            ],
        },
        "beta_inversion_symmetry": beta_inversion,
        "beta_line_dihedral_quotient": beta_dihedral,
        "beta_sheet_quotient_energy": beta_sheet_energy,
    }


def compute_report() -> dict[str, Any]:
    rows = [audit_case(*case) for case in AUDIT_CASES]
    principal_trace_rows = [
        principal_trace_case(p) for p in sorted({case[0] for case in AUDIT_CASES})
    ]
    alpha_middle_elliptic_rows = [
        alpha_middle_elliptic_case(p)
        for p in sorted({case[0] for case in AUDIT_CASES})
    ]
    beta_fiber_singularity_rows = [
        beta_fiber_singularity_case(p)
        for p in sorted({case[0] for case in AUDIT_CASES})
    ]
    beta_fiber_quotient_support_rows = [
        beta_fiber_quotient_support_case(p)
        for p in sorted({case[0] for case in AUDIT_CASES})
    ]
    beta_fiber_trace_rows = [
        beta_fiber_trace_case(p) for p in sorted({case[0] for case in AUDIT_CASES})
    ]
    for row in rows:
        key = (row["p"], row["quotient_order"])
        (
            expected_count,
            expected_two_sided,
            expected_beta2,
            expected_left_principal,
            expected_frobenius,
            expected_alpha_marginal,
            expected_marginal,
            expected_right_projected,
        ) = EXPECTED_ROWS[key]
        if row["good_point_count"] != expected_count:
            raise AssertionError((key, row["good_point_count"], expected_count))
        if abs(row["max_two_sided_coefficient_ratio"] - expected_two_sided) > TOLERANCE:
            raise AssertionError(
                (key, row["max_two_sided_coefficient_ratio"], expected_two_sided)
            )
        if abs(row["max_beta2_coefficient_ratio"] - expected_beta2) > TOLERANCE:
            raise AssertionError(
                (key, row["max_beta2_coefficient_ratio"], expected_beta2)
            )
        if (
            abs(row["max_left_principal_coefficient_ratio"] - expected_left_principal)
            > TOLERANCE
        ):
            raise AssertionError(
                (
                    key,
                    row["max_left_principal_coefficient_ratio"],
                    expected_left_principal,
                )
            )
        beta_reduction_ratio = row["beta_marginal_reduction"][
            "max_beta_marginal_coefficient_ratio"
        ]
        if abs(beta_reduction_ratio - expected_left_principal) > TOLERANCE:
            raise AssertionError((key, beta_reduction_ratio, expected_left_principal))
        if abs(row["centered_frobenius_ratio"] - expected_frobenius) > TOLERANCE:
            raise AssertionError(
                (key, row["centered_frobenius_ratio"], expected_frobenius)
            )
        if (
            abs(row["alpha_marginal_frobenius_ratio"] - expected_alpha_marginal)
            > TOLERANCE
        ):
            raise AssertionError(
                (
                    key,
                    row["alpha_marginal_frobenius_ratio"],
                    expected_alpha_marginal,
                )
            )
        if abs(row["beta_marginal_frobenius_ratio"] - expected_marginal) > TOLERANCE:
            raise AssertionError(
                (key, row["beta_marginal_frobenius_ratio"], expected_marginal)
            )
        if (
            abs(row["right_projected_frobenius_ratio"] - expected_right_projected)
            > TOLERANCE
        ):
            raise AssertionError(
                (
                    key,
                    row["right_projected_frobenius_ratio"],
                    expected_right_projected,
                )
            )
    for row in principal_trace_rows:
        expected = EXPECTED_PRINCIPAL_TRACE_ROWS[row["p"]]
        actual = (
            row["good_base_count"],
            row["deleted_base_count"],
            row["principal_trace"],
            row["full_middle_trace"],
            row["full_branch_trace"],
            row["deleted_correction"],
        )
        if actual != expected:
            raise AssertionError((row["p"], actual, expected))
    for row in beta_fiber_trace_rows:
        expected = EXPECTED_BETA_FIBER_TRACE_ROWS[row["p"]]
        actual = (
            row["max_regular_trace"],
            row["max_regular_beta"],
            row["max_support_trace"],
            row["max_support_beta"],
            row["total_trace"],
        )
        if actual != expected:
            raise AssertionError((row["p"], actual, expected))
    for row in beta_fiber_singularity_rows:
        expected = EXPECTED_BETA_FIBER_SINGULAR_ROWS[row["p"]]
        actual = (
            tuple(row["singular_beta_values"]),
            tuple(row["support_beta_values"]),
        )
        if actual != expected:
            raise AssertionError((row["p"], actual, expected))
    for row in beta_fiber_quotient_support_rows:
        expected = EXPECTED_BETA_FIBER_QUOTIENT_SUPPORT_ROWS[row["p"]]
        actual = (
            tuple(row["support_z_values"]),
            tuple(row["quotient_polynomial_roots"]),
        )
        if actual != expected:
            raise AssertionError((row["p"], actual, expected))
    max_two_sided_row = max(
        rows,
        key=lambda row: row["max_two_sided_coefficient_ratio"],
    )
    max_beta2_row = max(rows, key=lambda row: row["max_beta2_coefficient_ratio"])
    max_frobenius_row = max(rows, key=lambda row: row["centered_frobenius_ratio"])
    max_alpha_marginal_row = max(
        rows,
        key=lambda row: row["alpha_marginal_frobenius_ratio"],
    )
    max_alpha_marginal_coefficient_row = max(
        rows,
        key=lambda row: row["alpha_marginal_reduction"][
            "max_alpha_marginal_coefficient_ratio"
        ],
    )
    max_alpha_full_middle_row = max(
        rows,
        key=lambda row: row["alpha_marginal_reduction"][
            "max_alpha_full_middle_ratio"
        ],
    )
    max_marginal_row = max(
        rows,
        key=lambda row: row["beta_marginal_frobenius_ratio"],
    )
    max_right_projected_row = max(
        rows,
        key=lambda row: row["right_projected_frobenius_ratio"],
    )
    max_joint_collision_row = max(rows, key=lambda row: row["joint_collision_ratio"])
    max_nonnegative_bound_row = max(
        rows,
        key=lambda row: row["nonnegative_sufficient_bound_ratio"],
    )
    max_principal_trace_row = max(
        principal_trace_rows,
        key=lambda row: row["principal_trace_ratio"],
    )
    max_alpha_middle_fiber_row = max(
        alpha_middle_elliptic_rows,
        key=lambda row: row["max_fiber_trace_sqrt_ratio"],
    )
    max_beta_fiber_support_row = max(
        beta_fiber_singularity_rows,
        key=lambda row: row["support_beta_count"],
    )
    max_beta_quotient_support_row = max(
        beta_fiber_quotient_support_rows,
        key=lambda row: row["support_z_count"],
    )
    max_beta_sheet_energy_row = max(
        rows,
        key=lambda row: row["beta_sheet_quotient_energy"]["energy_ratio"],
    )
    max_beta_fixed_ratio_row = max(
        rows,
        key=lambda row: row["beta_sheet_quotient_energy"][
            "max_fixed_ratio_count"
        ],
    )
    max_beta_regular_trace_row = max(
        beta_fiber_trace_rows,
        key=lambda row: row["max_regular_trace_sqrt_ratio"],
    )
    max_beta_support_trace_row = max(
        beta_fiber_trace_rows,
        key=lambda row: row["max_support_trace_p_ratio"],
    )
    return {
        "status": "PASS",
        "proof_status": "EXPERIMENTAL / FINITE SPECTRAL AUDIT",
        "case_count": len(rows),
        "rows": rows,
        "principal_trace_rows": principal_trace_rows,
        "alpha_middle_elliptic_rows": alpha_middle_elliptic_rows,
        "beta_fiber_singularity_rows": beta_fiber_singularity_rows,
        "beta_fiber_quotient_support_rows": beta_fiber_quotient_support_rows,
        "beta_fiber_trace_rows": beta_fiber_trace_rows,
        "max_two_sided_coefficient_row": max_two_sided_row,
        "max_beta2_coefficient_row": max_beta2_row,
        "max_centered_frobenius_row": max_frobenius_row,
        "max_alpha_marginal_frobenius_row": max_alpha_marginal_row,
        "max_alpha_marginal_coefficient_row": max_alpha_marginal_coefficient_row,
        "max_alpha_full_middle_row": max_alpha_full_middle_row,
        "max_beta_marginal_frobenius_row": max_marginal_row,
        "max_right_projected_frobenius_row": max_right_projected_row,
        "max_joint_collision_row": max_joint_collision_row,
        "max_nonnegative_sufficient_bound_row": max_nonnegative_bound_row,
        "max_principal_trace_row": max_principal_trace_row,
        "max_alpha_middle_fiber_row": max_alpha_middle_fiber_row,
        "max_beta_fiber_support_row": max_beta_fiber_support_row,
        "max_beta_quotient_support_row": max_beta_quotient_support_row,
        "max_beta_sheet_energy_row": max_beta_sheet_energy_row,
        "max_beta_fixed_ratio_row": max_beta_fixed_ratio_row,
        "max_beta_regular_trace_row": max_beta_regular_trace_row,
        "max_beta_support_trace_row": max_beta_support_trace_row,
        "interpretation": (
            "All audited good beta-pushforward matrices have p-scale full "
            "BETA_2 coefficients, p-scale centered Frobenius norm, and "
            "p-scale principal total trace."
        ),
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"status: {report['status']}")
    print(f"cases: {report['case_count']}")
    for row in report["rows"]:
        alpha_reduction = row["alpha_marginal_reduction"]
        beta_reduction = row["beta_marginal_reduction"]
        beta_chebyshev = row["beta_marginal_chebyshev_quotient"]
        beta_line_reduction = row["beta_line_quotient_reduction"]
        beta_inversion = row["beta_inversion_symmetry"]
        beta_dihedral = row["beta_line_dihedral_quotient"]
        beta_sheet = row["beta_sheet_quotient_energy"]
        print(
            "p={p} e={quotient_order} good={good_point_count} "
            "two_sided/p={max_two_sided_coefficient_ratio} "
            "beta2/p={max_beta2_coefficient_ratio} "
            "left_principal/p={max_left_principal_coefficient_ratio} "
            "frob/p={centered_frobenius_ratio} "
            "alpha_marginal/p={alpha_marginal_frobenius_ratio} "
            "alpha_coeff/p={alpha_coeff_ratio} "
            "beta_marginal/p={beta_marginal_frobenius_ratio} "
            "beta_coeff/p={beta_coeff_ratio} "
            "right_projected/p={right_projected_frobenius_ratio} "
            "nonnull_bound/p={nonnegative_sufficient_bound_ratio} "
            "joint/p^2={joint_collision_ratio} "
            "parseval_error={parseval_error} "
            "marginal_parseval_error={marginal_parseval_error} "
            "pair_energy_error={pair_energy_error} "
            "pythagorean_error={pythagorean_error} "
            "component_error={component_centered_error} "
            "chebyshev_error={chebyshev_error} "
            "chebyshev_l2_error={chebyshev_l2_error} "
            "beta_line_error={beta_line_error} "
            "dihedral_error={dihedral_error} "
            "sheet_energy/p2={sheet_energy_ratio} "
            "inversion_error={inversion_error}".format(
                alpha_coeff_ratio=alpha_reduction[
                    "max_alpha_marginal_coefficient_ratio"
                ],
                beta_coeff_ratio=beta_reduction[
                    "max_beta_marginal_coefficient_ratio"
                ],
                beta_line_error=beta_line_reduction[
                    "max_beta_line_formula_error"
                ],
                dihedral_error=beta_dihedral["max_dihedral_formula_error"],
                sheet_energy_ratio=beta_sheet["energy_ratio"],
                chebyshev_error=beta_chebyshev["max_chebyshev_formula_error"],
                chebyshev_l2_error=beta_chebyshev[
                    "max_chebyshev_second_moment_error"
                ],
                inversion_error=beta_inversion["max_coefficient_inversion_error"],
                **row,
            )
        )
    max_two_sided = report["max_two_sided_coefficient_row"]
    max_beta2 = report["max_beta2_coefficient_row"]
    max_frobenius = report["max_centered_frobenius_row"]
    max_alpha_marginal = report["max_alpha_marginal_frobenius_row"]
    max_alpha_coefficient = report["max_alpha_marginal_coefficient_row"]
    max_alpha_middle = report["max_alpha_full_middle_row"]
    max_marginal = report["max_beta_marginal_frobenius_row"]
    max_right_projected = report["max_right_projected_frobenius_row"]
    max_joint_collision = report["max_joint_collision_row"]
    max_nonnegative_bound = report["max_nonnegative_sufficient_bound_row"]
    coef_key = "max_alpha_marginal_coefficient_ratio"
    max_alpha_middle_fiber = report["max_alpha_middle_fiber_row"]
    max_beta_regular_trace = report["max_beta_regular_trace_row"]
    max_beta_support_trace = report["max_beta_support_trace_row"]
    max_beta_quotient_support = report["max_beta_quotient_support_row"]
    max_beta_sheet_energy = report["max_beta_sheet_energy_row"]
    max_beta_fixed_ratio = report["max_beta_fixed_ratio_row"]
    print(
        "max two-sided coefficient row: "
        f"p={max_two_sided['p']} e={max_two_sided['quotient_order']} "
        f"ratio={max_two_sided['max_two_sided_coefficient_ratio']}"
    )
    print(
        "max BETA_2 coefficient row: "
        f"p={max_beta2['p']} e={max_beta2['quotient_order']} "
        f"ratio={max_beta2['max_beta2_coefficient_ratio']}"
    )
    print(
        "max centered Frobenius row: "
        f"p={max_frobenius['p']} e={max_frobenius['quotient_order']} "
        f"ratio={max_frobenius['centered_frobenius_ratio']}"
    )
    print(
        "max alpha-marginal Frobenius row: "
        f"p={max_alpha_marginal['p']} "
        f"e={max_alpha_marginal['quotient_order']} "
        f"ratio={max_alpha_marginal['alpha_marginal_frobenius_ratio']}"
    )
    print(
        "max alpha-marginal coefficient row: "
        f"p={max_alpha_coefficient['p']} "
        f"e={max_alpha_coefficient['quotient_order']} "
        "ratio="
        f"{max_alpha_coefficient['alpha_marginal_reduction'][coef_key]}"
    )
    print(
        "max alpha full-middle row: "
        f"p={max_alpha_middle['p']} e={max_alpha_middle['quotient_order']} "
        "ratio="
        f"{max_alpha_middle['alpha_marginal_reduction']['max_alpha_full_middle_ratio']}"
    )
    print(
        "max alpha-middle elliptic fiber row: "
        f"p={max_alpha_middle_fiber['p']} "
        f"a={max_alpha_middle_fiber['max_fiber_trace_parameter']} "
        f"ratio={max_alpha_middle_fiber['max_fiber_trace_sqrt_ratio']}"
    )
    print(
        "max beta-marginal Frobenius row: "
        f"p={max_marginal['p']} e={max_marginal['quotient_order']} "
        f"ratio={max_marginal['beta_marginal_frobenius_ratio']}"
    )
    print(
        "max beta regular-fiber trace row: "
        f"p={max_beta_regular_trace['p']} "
        f"beta={max_beta_regular_trace['max_regular_beta']} "
        f"ratio={max_beta_regular_trace['max_regular_trace_sqrt_ratio']}"
    )
    print(
        "max beta support-fiber trace row: "
        f"p={max_beta_support_trace['p']} "
        f"beta={max_beta_support_trace['max_support_beta']} "
        f"ratio={max_beta_support_trace['max_support_trace_p_ratio']}"
    )
    print(
        "max right-projected Frobenius row: "
        f"p={max_right_projected['p']} "
        f"e={max_right_projected['quotient_order']} "
        f"ratio={max_right_projected['right_projected_frobenius_ratio']}"
    )
    print(
        "max joint collision row: "
        f"p={max_joint_collision['p']} "
        f"e={max_joint_collision['quotient_order']} "
        f"ratio={max_joint_collision['joint_collision_ratio']}"
    )
    print(
        "max nonnegative sufficient bound row: "
        f"p={max_nonnegative_bound['p']} "
        f"e={max_nonnegative_bound['quotient_order']} "
        f"ratio={max_nonnegative_bound['nonnegative_sufficient_bound_ratio']}"
    )
    for row in report["principal_trace_rows"]:
        print(
            "principal trace row: "
            f"p={row['p']} good_base={row['good_base_count']} "
            f"deleted_base={row['deleted_base_count']} "
            f"T/p={row['principal_trace_ratio']} "
            f"full_torus/p={row['full_torus_trace_ratio']} "
            f"deleted_correction/p={row['deleted_correction_ratio']}"
        )
    max_principal_trace = report["max_principal_trace_row"]
    print(
        "max principal trace row: "
        f"p={max_principal_trace['p']} "
        f"ratio={max_principal_trace['principal_trace_ratio']}"
    )
    for row in report["alpha_middle_elliptic_rows"]:
        print(
            "alpha-middle elliptic row: "
            f"p={row['p']} singular={tuple(row['singular_parameters'])} "
            f"max_fiber/sqrtp={row['max_fiber_trace_sqrt_ratio']}"
        )
    for row in report["beta_fiber_singularity_rows"]:
        print(
            "beta-fiber singular row: "
            f"p={row['p']} singular={tuple(row['singular_beta_values'])} "
            f"support_count={row['support_beta_count']} "
            f"singular_points={row['singular_point_count']}"
        )
    for row in report["beta_fiber_quotient_support_rows"]:
        print(
            "beta-fiber quotient support row: "
            f"p={row['p']} support_z={tuple(row['support_z_values'])} "
            "quotient_roots="
            f"{tuple(row['quotient_polynomial_roots'])}"
        )
    for row in report["beta_fiber_trace_rows"]:
        print(
            "beta-fiber trace row: "
            f"p={row['p']} max_regular/sqrtp="
            f"{row['max_regular_trace_sqrt_ratio']} "
            f"max_support/p={row['max_support_trace_p_ratio']} "
            f"total={row['total_trace']}"
        )
    max_beta_fiber_support = report["max_beta_fiber_support_row"]
    print(
        "max beta-fiber support row: "
        f"p={max_beta_fiber_support['p']} "
        f"support_count={max_beta_fiber_support['support_beta_count']}"
    )
    print(
        "max beta-fiber quotient support row: "
        f"p={max_beta_quotient_support['p']} "
        f"support_z_count={max_beta_quotient_support['support_z_count']} "
        "quotient_root_count="
        f"{max_beta_quotient_support['quotient_polynomial_root_count']}"
    )
    print(
        "max beta-sheet quotient energy row: "
        f"p={max_beta_sheet_energy['p']} "
        f"e={max_beta_sheet_energy['quotient_order']} "
        "ratio="
        f"{max_beta_sheet_energy['beta_sheet_quotient_energy']['energy_ratio']}"
    )
    print(
        "max beta fixed-ratio row: "
        f"p={max_beta_fixed_ratio['p']} "
        f"e={max_beta_fixed_ratio['quotient_order']} "
        "count="
        f"{max_beta_fixed_ratio['beta_sheet_quotient_energy']['max_fixed_ratio_count']}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()
    report = compute_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
