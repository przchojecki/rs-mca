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
    (17, 8): (98, 1.1361004999, 0.4744784060),
    (17, 16): (98, 1.5728968500, 0.4632352941),
    (31, 6): (486, 2.3225806452, 0.6634504452),
    (31, 10): (486, 1.8416183853, 0.5965213065),
    (43, 6): (1568, 3.0697674419, 1.1366043634),
    (43, 14): (1568, 2.5116279070, 0.8267620588),
    (61, 10): (3638, 3.1564925354, 1.0413952974),
    (61, 12): (3638, 3.7704918033, 0.8927070383),
    (61, 20): (3638, 4.1651103505, 1.0676033635),
    (73, 8): (4452, 3.3972602740, 1.0215128288),
    (73, 12): (4452, 3.3972602740, 0.8625907978),
    (97, 12): (8220, 2.4147368394, 0.9058943297),
    (97, 16): (8220, 3.1778878253, 0.8764288851),
    (109, 12): (11750, 3.9816513761, 1.1119173117),
    (109, 18): (11750, 3.9816513761, 0.9676363750),
    (109, 27): (11750, 3.9872656889, 0.8757048097),
    (127, 9): (12406, 3.5511811024, 0.9915857812),
    (127, 14): (12406, 4.8036624425, 0.9401651247),
    (127, 18): (12406, 3.7751417349, 0.8755124649),
    (127, 21): (12406, 4.8036624425, 0.8972861099),
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


def spectral_energy(matrix: list[list[int]]) -> tuple[float, float]:
    order = len(matrix)
    root = cmath.exp(2j * math.pi / order)
    energy = 0.0
    max_coefficient = 0.0
    for left_character in range(1, order):
        for right_character in range(1, order):
            coefficient = 0j
            for left in range(order):
                for right in range(order):
                    coefficient += matrix[left][right] * root ** (
                        left_character * left + right_character * right
                    )
            energy += abs(coefficient) ** 2
            max_coefficient = max(max_coefficient, abs(coefficient))
    return energy, max_coefficient


def audit_case(p: int, quotient_order: int) -> dict[str, Any]:
    matrix, point_count = good_pushforward_matrix(p, quotient_order)
    frobenius_square = centered_frobenius_square(matrix)
    energy, max_coefficient = spectral_energy(matrix)
    parseval_error = abs(energy / (quotient_order * quotient_order) - frobenius_square)
    if parseval_error > TOLERANCE:
        raise AssertionError((p, quotient_order, energy, frobenius_square))
    max_ratio = max_coefficient / p
    frobenius_ratio = math.sqrt(frobenius_square) / p
    return {
        "p": p,
        "quotient_order": quotient_order,
        "good_point_count": point_count,
        "max_coefficient_ratio": round(max_ratio, 10),
        "centered_frobenius_ratio": round(frobenius_ratio, 10),
        "parseval_error": round(parseval_error, 12),
    }


def compute_report() -> dict[str, Any]:
    rows = [audit_case(*case) for case in AUDIT_CASES]
    for row in rows:
        key = (row["p"], row["quotient_order"])
        expected_count, expected_max, expected_frobenius = EXPECTED_ROWS[key]
        if row["good_point_count"] != expected_count:
            raise AssertionError((key, row["good_point_count"], expected_count))
        if abs(row["max_coefficient_ratio"] - expected_max) > TOLERANCE:
            raise AssertionError((key, row["max_coefficient_ratio"], expected_max))
        if abs(row["centered_frobenius_ratio"] - expected_frobenius) > TOLERANCE:
            raise AssertionError(
                (key, row["centered_frobenius_ratio"], expected_frobenius)
            )
    max_coefficient_row = max(rows, key=lambda row: row["max_coefficient_ratio"])
    max_frobenius_row = max(rows, key=lambda row: row["centered_frobenius_ratio"])
    return {
        "status": "PASS",
        "proof_status": "EXPERIMENTAL / FINITE SPECTRAL AUDIT",
        "case_count": len(rows),
        "rows": rows,
        "max_coefficient_row": max_coefficient_row,
        "max_centered_frobenius_row": max_frobenius_row,
        "interpretation": (
            "All audited good beta-pushforward matrices have p-scale centered "
            "Frobenius norm and p-scale nonprincipal Fourier coefficients."
        ),
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"status: {report['status']}")
    print(f"cases: {report['case_count']}")
    for row in report["rows"]:
        print(
            "p={p} e={quotient_order} good={good_point_count} "
            "max/p={max_coefficient_ratio} frob/p={centered_frobenius_ratio} "
            "parseval_error={parseval_error}".format(**row)
        )
    max_coefficient = report["max_coefficient_row"]
    max_frobenius = report["max_centered_frobenius_row"]
    print(
        "max coefficient row: "
        f"p={max_coefficient['p']} e={max_coefficient['quotient_order']} "
        f"ratio={max_coefficient['max_coefficient_ratio']}"
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
