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
        0.4744784060, 0.1604222370, 0.5008643049,
    ),
    (17, 16): (
        98, 1.5728968500, 1.5728968500, 1.0588235294,
        0.4632352941, 0.1210446885, 0.4787888411,
    ),
    (31, 6): (
        486, 2.3225806452, 2.3225806452, 2.2580645161,
        0.6634504452, 0.5956833972, 0.8916306427,
    ),
    (31, 10): (
        486, 1.8416183853, 3.1043892896, 3.1043892896,
        0.5965213065, 0.8914205479, 1.0725988356,
    ),
    (43, 6): (
        1568, 3.0697674419, 3.2558139535, 3.2558139535,
        1.1366043634, 0.6522692703, 1.3104673518,
    ),
    (43, 14): (
        1568, 2.5116279070, 4.1755606367, 4.1755606367,
        0.8267620588, 0.8830649777, 1.2096856024,
    ),
    (61, 10): (
        3638, 3.1564925354, 4.6342117655, 4.6342117655,
        1.0413952974, 1.1549828950, 1.5551493990,
    ),
    (61, 12): (
        3638, 3.7704918033, 5.0163934426, 5.0163934426,
        0.8927070383, 0.6915699414, 1.1292452524,
    ),
    (61, 20): (
        3638, 4.1651103505, 5.3219296886, 5.3219296886,
        1.0676033635, 0.9151432864, 1.4061522593,
    ),
    (73, 8): (
        4452, 3.3972602740, 3.9136778741, 3.9136778741,
        1.0215128288, 1.0631452044, 1.4743697586,
    ),
    (73, 12): (
        4452, 3.3972602740, 5.5068493151, 5.5068493151,
        0.8625907978, 1.0433365298, 1.3537407429,
    ),
    (97, 12): (
        8220, 2.4147368394, 3.6118420031, 3.6118420031,
        0.9058943297, 0.6312463166, 1.1041360644,
    ),
    (97, 16): (
        8220, 3.1778878253, 3.9489699606, 3.9489699606,
        0.8764288851, 0.8280980376, 1.2057669553,
    ),
    (109, 12): (
        11750, 3.9816513761, 5.6717827398, 5.6717827398,
        1.1119173117, 1.2278896782, 1.6565244248,
    ),
    (109, 18): (
        11750, 3.9816513761, 4.7522935780, 4.7522935780,
        0.9676363750, 0.8838514219, 1.3105393891,
    ),
    (109, 27): (
        11750, 3.9872656889, 4.6710181306, 4.6710181306,
        0.8757048097, 0.5079449321, 1.0123571345,
    ),
    (127, 9): (
        12406, 3.5511811024, 3.8582677165, 3.8582677165,
        0.9915857812, 0.7704811722, 1.2557402591,
    ),
    (127, 14): (
        12406, 4.8036624425, 5.1781602661, 5.1781602661,
        0.9401651247, 1.0542609262, 1.4125779845,
    ),
    (127, 18): (
        12406, 3.7751417349, 4.1417322835, 4.1417322835,
        0.8755124649, 0.5311890425, 1.0240526721,
    ),
    (127, 21): (
        12406, 4.8036624425, 4.8036624425, 4.6769325284,
        0.8972861099, 0.7390713327, 1.1624752892,
    ),
}

TOLERANCE = 1e-8


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


def audit_case(p: int, quotient_order: int) -> dict[str, Any]:
    matrix, point_count = good_pushforward_matrix(p, quotient_order)
    frobenius_square = centered_frobenius_square(matrix)
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
    two_sided_ratio = max_two_sided / p
    beta2_ratio = max_beta2 / p
    left_principal_ratio = max_left_principal / p
    frobenius_ratio = math.sqrt(frobenius_square) / p
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
    }


def compute_report() -> dict[str, Any]:
    rows = [audit_case(*case) for case in AUDIT_CASES]
    for row in rows:
        key = (row["p"], row["quotient_order"])
        (
            expected_count,
            expected_two_sided,
            expected_beta2,
            expected_left_principal,
            expected_frobenius,
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
        if abs(row["centered_frobenius_ratio"] - expected_frobenius) > TOLERANCE:
            raise AssertionError(
                (key, row["centered_frobenius_ratio"], expected_frobenius)
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
    max_two_sided_row = max(
        rows,
        key=lambda row: row["max_two_sided_coefficient_ratio"],
    )
    max_beta2_row = max(rows, key=lambda row: row["max_beta2_coefficient_ratio"])
    max_frobenius_row = max(rows, key=lambda row: row["centered_frobenius_ratio"])
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
    return {
        "status": "PASS",
        "proof_status": "EXPERIMENTAL / FINITE SPECTRAL AUDIT",
        "case_count": len(rows),
        "rows": rows,
        "max_two_sided_coefficient_row": max_two_sided_row,
        "max_beta2_coefficient_row": max_beta2_row,
        "max_centered_frobenius_row": max_frobenius_row,
        "max_beta_marginal_frobenius_row": max_marginal_row,
        "max_right_projected_frobenius_row": max_right_projected_row,
        "max_joint_collision_row": max_joint_collision_row,
        "max_nonnegative_sufficient_bound_row": max_nonnegative_bound_row,
        "interpretation": (
            "All audited good beta-pushforward matrices have p-scale full "
            "BETA_2 coefficients and p-scale centered Frobenius norm."
        ),
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"status: {report['status']}")
    print(f"cases: {report['case_count']}")
    for row in report["rows"]:
        print(
            "p={p} e={quotient_order} good={good_point_count} "
            "two_sided/p={max_two_sided_coefficient_ratio} "
            "beta2/p={max_beta2_coefficient_ratio} "
            "left_principal/p={max_left_principal_coefficient_ratio} "
            "frob/p={centered_frobenius_ratio} "
            "beta_marginal/p={beta_marginal_frobenius_ratio} "
            "right_projected/p={right_projected_frobenius_ratio} "
            "nonnull_bound/p={nonnegative_sufficient_bound_ratio} "
            "joint/p^2={joint_collision_ratio} "
            "parseval_error={parseval_error} "
            "marginal_parseval_error={marginal_parseval_error} "
            "pair_energy_error={pair_energy_error} "
            "pythagorean_error={pythagorean_error} "
            "component_error={component_centered_error}".format(**row)
        )
    max_two_sided = report["max_two_sided_coefficient_row"]
    max_beta2 = report["max_beta2_coefficient_row"]
    max_frobenius = report["max_centered_frobenius_row"]
    max_marginal = report["max_beta_marginal_frobenius_row"]
    max_right_projected = report["max_right_projected_frobenius_row"]
    max_joint_collision = report["max_joint_collision_row"]
    max_nonnegative_bound = report["max_nonnegative_sufficient_bound_row"]
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
        "max beta-marginal Frobenius row: "
        f"p={max_marginal['p']} e={max_marginal['quotient_order']} "
        f"ratio={max_marginal['beta_marginal_frobenius_ratio']}"
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
