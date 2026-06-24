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
    (17, 8): (98, 1.1361004999, 1.1361004999, 1.0588235294, 0.4744784060),
    (17, 16): (98, 1.5728968500, 1.5728968500, 1.0588235294, 0.4632352941),
    (31, 6): (486, 2.3225806452, 2.3225806452, 2.2580645161, 0.6634504452),
    (31, 10): (486, 1.8416183853, 3.1043892896, 3.1043892896, 0.5965213065),
    (43, 6): (1568, 3.0697674419, 3.2558139535, 3.2558139535, 1.1366043634),
    (43, 14): (1568, 2.5116279070, 4.1755606367, 4.1755606367, 0.8267620588),
    (61, 10): (3638, 3.1564925354, 4.6342117655, 4.6342117655, 1.0413952974),
    (61, 12): (3638, 3.7704918033, 5.0163934426, 5.0163934426, 0.8927070383),
    (61, 20): (3638, 4.1651103505, 5.3219296886, 5.3219296886, 1.0676033635),
    (73, 8): (4452, 3.3972602740, 3.9136778741, 3.9136778741, 1.0215128288),
    (73, 12): (4452, 3.3972602740, 5.5068493151, 5.5068493151, 0.8625907978),
    (97, 12): (8220, 2.4147368394, 3.6118420031, 3.6118420031, 0.9058943297),
    (97, 16): (8220, 3.1778878253, 3.9489699606, 3.9489699606, 0.8764288851),
    (109, 12): (11750, 3.9816513761, 5.6717827398, 5.6717827398, 1.1119173117),
    (109, 18): (11750, 3.9816513761, 4.7522935780, 4.7522935780, 0.9676363750),
    (109, 27): (11750, 3.9872656889, 4.6710181306, 4.6710181306, 0.8757048097),
    (127, 9): (12406, 3.5511811024, 3.8582677165, 3.8582677165, 0.9915857812),
    (127, 14): (12406, 4.8036624425, 5.1781602661, 5.1781602661, 0.9401651247),
    (127, 18): (12406, 3.7751417349, 4.1417322835, 4.1417322835, 0.8755124649),
    (127, 21): (12406, 4.8036624425, 4.8036624425, 4.6769325284, 0.8972861099),
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


def spectral_stats(matrix: list[list[int]]) -> tuple[float, float, float, float]:
    order = len(matrix)
    root = cmath.exp(2j * math.pi / order)
    energy = 0.0
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
                max_left_principal = max(max_left_principal, coefficient_size)
            else:
                energy += coefficient_size ** 2
                max_two_sided = max(max_two_sided, coefficient_size)
    return energy, max_two_sided, max_beta2, max_left_principal


def audit_case(p: int, quotient_order: int) -> dict[str, Any]:
    matrix, point_count = good_pushforward_matrix(p, quotient_order)
    frobenius_square = centered_frobenius_square(matrix)
    pair_square = centered_pair_energy_square(matrix)
    energy, max_two_sided, max_beta2, max_left_principal = spectral_stats(matrix)
    parseval_error = abs(energy / (quotient_order * quotient_order) - frobenius_square)
    pair_energy_error = abs(pair_square - frobenius_square)
    if parseval_error > TOLERANCE:
        raise AssertionError((p, quotient_order, energy, frobenius_square))
    if pair_energy_error > TOLERANCE:
        raise AssertionError((p, quotient_order, pair_square, frobenius_square))
    two_sided_ratio = max_two_sided / p
    beta2_ratio = max_beta2 / p
    left_principal_ratio = max_left_principal / p
    frobenius_ratio = math.sqrt(frobenius_square) / p
    return {
        "p": p,
        "quotient_order": quotient_order,
        "good_point_count": point_count,
        "max_two_sided_coefficient_ratio": round(two_sided_ratio, 10),
        "max_beta2_coefficient_ratio": round(beta2_ratio, 10),
        "max_left_principal_coefficient_ratio": round(left_principal_ratio, 10),
        "centered_frobenius_ratio": round(frobenius_ratio, 10),
        "parseval_error": round(parseval_error, 12),
        "pair_energy_error": round(pair_energy_error, 12),
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
    max_two_sided_row = max(
        rows,
        key=lambda row: row["max_two_sided_coefficient_ratio"],
    )
    max_beta2_row = max(rows, key=lambda row: row["max_beta2_coefficient_ratio"])
    max_frobenius_row = max(rows, key=lambda row: row["centered_frobenius_ratio"])
    return {
        "status": "PASS",
        "proof_status": "EXPERIMENTAL / FINITE SPECTRAL AUDIT",
        "case_count": len(rows),
        "rows": rows,
        "max_two_sided_coefficient_row": max_two_sided_row,
        "max_beta2_coefficient_row": max_beta2_row,
        "max_centered_frobenius_row": max_frobenius_row,
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
            "parseval_error={parseval_error} "
            "pair_energy_error={pair_energy_error}".format(**row)
        )
    max_two_sided = report["max_two_sided_coefficient_row"]
    max_beta2 = report["max_beta2_coefficient_row"]
    max_frobenius = report["max_centered_frobenius_row"]
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
