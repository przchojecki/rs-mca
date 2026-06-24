#!/usr/bin/env python3
"""Verify the generic two-ended fixed-jet LD_sw transfer theorem.

Cycle119 uses a stricter agreement target than Cycle116. The relevant locator
families have one fewer common top coefficient, but also have a common nonzero
constant coefficient. This verifier checks the abstract parity-check theorem
on exact finite-field toy instances and checks that the current Cycle119 row
instantiates it as the strict-ball addendum to the Cycle120 M1 chain.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import verify_m1_cycle84_color_collision_witnesses as color_shell
import verify_m1_cycle84_exact_occupancy_chain as cycle84
import verify_m1_cycle116_fixed_jet_bridge as fixed_jet_bridge
import verify_m1_cycle116_fixed_jet_transfer as fixed_transfer
import verify_m1_cycle116_smooth_padding_transfer as smooth_padding
import verify_m1_cycle120_gate_arithmetic as gate
import verify_m1_fixed_jet_ldsw_theorem as fixed_jet_theorem


NATIVE_COSUPPORT_SIZE = 113
NATIVE_AGREEMENT = 143
NATIVE_REMAINDER_MAX_DEGREE = 107
CYCLE119_A_SIZE = 120
CYCLE119_R_SIZE = 136
CYCLE119_COSUPPORT_SIZE = 249
CYCLE119_SIGMA = 7
CYCLE119_DIMENSION = 256
CYCLE119_AGREEMENT = 263
CYCLE119_DISTANCE = 249
EXPECTED_BAD_PARAMETERS = 52_747_567_092


def poly_add(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return fixed_jet_theorem.trim(out, p)


def dot(a: Sequence[int], b: Sequence[int], p: int) -> int:
    return sum(x * y for x, y in zip(a, b)) % p


def coeff(poly: Sequence[int], degree: int) -> int:
    return int(poly[degree]) if degree < len(poly) else 0


def two_ended_key(subset: Sequence[int], j: int, sigma: int, p: int) -> tuple[int, ...]:
    locator = fixed_jet_theorem.poly_from_roots(subset, p)
    top_degrees = range(j - sigma + 2, j)
    return (locator[0],) + tuple(locator[degree] for degree in top_degrees)


def find_two_ended_family(
    p: int, n: int, j: int, sigma: int
) -> tuple[tuple[int, ...], list[tuple[int, ...]]]:
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for subset in itertools.combinations(range(1, n + 1), j):
        locator = fixed_jet_theorem.poly_from_roots(subset, p)
        if locator[0] == 0 or fixed_jet_theorem.poly_eval(locator, p - 1, p) == 0:
            continue
        buckets.setdefault(two_ended_key(subset, j, sigma, p), []).append(subset)

    key, family = max(buckets.items(), key=lambda item: len(item[1]))
    bad_values = {
        fixed_jet_theorem.poly_eval(
            fixed_jet_theorem.poly_from_roots(subset, p), p - 1, p
        )
        for subset in family
    }
    if len(family) < 2 or len(bad_values) < 2:
        raise AssertionError("toy instance did not produce a two-ended family")
    return key, family


def solve_square(matrix: Sequence[Sequence[int]], rhs: Sequence[int], p: int) -> list[int]:
    rows = [
        [int(x) % p for x in row] + [int(value) % p]
        for row, value in zip(matrix, rhs)
    ]
    size = len(rows)
    if size == 0 or any(len(row) != size + 1 for row in rows):
        raise AssertionError("square solve needs an n by n matrix")

    rank = 0
    for col in range(size):
        pivot = None
        for row in range(rank, size):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            raise AssertionError("singular matrix")
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = fixed_jet_theorem.inv_mod(rows[rank][col], p)
        rows[rank] = [(x * inv) % p for x in rows[rank]]
        for row in range(size):
            if row != rank and rows[row][col] % p:
                factor = rows[row][col]
                rows[row] = [
                    (rows[row][c] - factor * rows[rank][c]) % p
                    for c in range(size + 1)
                ]
        rank += 1

    return [rows[row][-1] % p for row in range(size)]


def solve_span_coefficients(
    columns: Sequence[Sequence[int]], target: Sequence[int], p: int
) -> list[int]:
    if not columns:
        raise AssertionError("empty column span")
    row_count = len(target)
    col_count = len(columns)
    rows = [
        [int(columns[col][row]) % p for col in range(col_count)]
        + [int(target[row]) % p]
        for row in range(row_count)
    ]

    rank = 0
    pivot_cols: list[int] = []
    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = fixed_jet_theorem.inv_mod(rows[rank][col], p)
        rows[rank] = [(x * inv) % p for x in rows[rank]]
        for row in range(row_count):
            if row != rank and rows[row][col] % p:
                factor = rows[row][col]
                rows[row] = [
                    (rows[row][c] - factor * rows[rank][c]) % p
                    for c in range(col_count + 1)
                ]
        pivot_cols.append(col)
        rank += 1

    for row in range(rank, row_count):
        if all(rows[row][col] % p == 0 for col in range(col_count)):
            if rows[row][-1] % p:
                raise AssertionError("target is not in the column span")

    solution = [0] * col_count
    for row, col in enumerate(pivot_cols):
        solution[col] = rows[row][-1] % p
    return solution


def selected_coefficient_matrix(
    locator: Sequence[int], j: int, sigma: int, p: int
) -> tuple[list[int], list[list[int]]]:
    selected_degrees = [0] + [j + offset for offset in range(1, sigma)]
    matrix: list[list[int]] = []
    for degree in selected_degrees:
        row = []
        for basis_degree in range(sigma):
            basis = [0] * basis_degree + [1]
            product = fixed_jet_theorem.poly_mul(locator, basis, p)
            row.append(coeff(product, degree) % p)
        matrix.append(row)
    return selected_degrees, matrix


def check_two_ended_instance(
    *,
    name: str,
    p: int,
    n: int,
    j: int,
    sigma: int,
) -> Dict[str, Any]:
    d_points = list(range(1, n + 1))
    beta = p - 1
    if beta in d_points or 0 in d_points:
        raise AssertionError("toy domain must avoid beta and zero")
    if not (2 <= sigma and j + sigma < n):
        raise AssertionError("need sigma>=2 and positive code dimension")

    key, family = find_two_ended_family(p, n, j, sigma)
    r = j + sigma
    k = n - r
    domain_locator = fixed_jet_theorem.poly_from_roots(d_points, p)
    domain_derivative = fixed_jet_theorem.poly_derivative(domain_locator, p)
    domain_at_beta = fixed_jet_theorem.poly_eval(domain_locator, beta, p)
    lprime = {x: fixed_jet_theorem.poly_eval(domain_derivative, x, p) for x in d_points}

    locators = {subset: fixed_jet_theorem.poly_from_roots(subset, p) for subset in family}
    selected_degrees, selected_matrix = selected_coefficient_matrix(
        locators[family[0]], j, sigma, p
    )
    transpose = [list(col) for col in zip(*selected_matrix)]
    eval_row = [pow(beta, degree, p) for degree in range(sigma)]
    selected_functional = solve_square(transpose, eval_row, p)

    a_syndrome = [0] * r
    for degree, value in zip(selected_degrees, selected_functional):
        a_syndrome[degree] = (-value) % p

    beta_column = [pow(beta, degree, p) for degree in range(r)]
    g_word = [
        domain_at_beta * fixed_jet_theorem.inv_mod((beta - x) % p, p) % p
        for x in d_points
    ]

    def syndrome(word: Sequence[int]) -> list[int]:
        out = []
        for degree in range(r):
            total = 0
            for idx, x in enumerate(d_points):
                total += (
                    pow(x, degree, p)
                    * word[idx]
                    * fixed_jet_theorem.inv_mod(lprime[x], p)
                )
            out.append(total % p)
        return out

    if syndrome(g_word) != beta_column:
        raise AssertionError("Hg does not equal the beta column")

    e_words: dict[tuple[int, ...], list[int]] = {}
    z_values: dict[tuple[int, ...], int] = {}
    for left, right in itertools.combinations(family, 2):
        diff_degree = fixed_jet_theorem.degree(
            fixed_jet_theorem.poly_sub(locators[left], locators[right], p), p
        )
        if diff_degree > j - sigma + 1:
            raise AssertionError("two-ended top jet is not common")

    for subset in family:
        locator = locators[subset]
        if selected_coefficient_matrix(locator, j, sigma, p)[1] != selected_matrix:
            raise AssertionError("selected coefficient matrix varies with J")
        p_beta = fixed_jet_theorem.poly_eval(locator, beta, p)
        if p_beta == 0:
            raise AssertionError("P_J(beta) vanishes")
        z = fixed_jet_theorem.inv_mod(p_beta, p)

        for basis_degree in range(sigma):
            basis = [0] * basis_degree + [1]
            annihilator = fixed_jet_theorem.poly_mul(locator, basis, p)
            padded = annihilator + [0] * (r - len(annihilator))
            if dot(padded[:r], a_syndrome, p) != -pow(beta, basis_degree, p) % p:
                raise AssertionError("selected functional does not recover A(beta)")
            if dot(padded[:r], beta_column, p) != (
                p_beta * pow(beta, basis_degree, p)
            ) % p:
                raise AssertionError("beta column has wrong annihilator value")

        y = poly_add(a_syndrome, fixed_jet_theorem.scalar_mul(z, beta_column, p), p)
        y += [0] * (r - len(y))
        columns = [
            [
                pow(x, degree, p) * fixed_jet_theorem.inv_mod(lprime[x], p) % p
                for degree in range(r)
            ]
            for x in subset
        ]
        if fixed_jet_theorem.matrix_rank_mod(
            [[column[row] for column in columns] for row in range(r)], p
        ) != j:
            raise AssertionError("support columns do not have full rank")
        coeffs = solve_span_coefficients(columns, y[:r], p)
        e_word = [0] * n
        point_index = {x: idx for idx, x in enumerate(d_points)}
        for x, value in zip(subset, coeffs):
            e_word[point_index[x]] = value
        if syndrome(e_word) != y[:r]:
            raise AssertionError("constructed support error has wrong syndrome")

        e_words[subset] = e_word
        z_values[subset] = z

    base_subset = family[0]
    f_word = fixed_jet_theorem.vector_sub(
        e_words[base_subset],
        fixed_jet_theorem.scalar_mul(z_values[base_subset], g_word, p),
        p,
    )

    for subset in family:
        z = z_values[subset]
        line_word = fixed_jet_theorem.vector_add(
            f_word, fixed_jet_theorem.scalar_mul(z, g_word, p), p
        )
        codeword = fixed_jet_theorem.vector_sub(line_word, e_words[subset], p)
        if syndrome(codeword) != [0] * r:
            raise AssertionError("constructed agreement word is not a codeword")
        subset_set = set(subset)
        for idx, x in enumerate(d_points):
            if x not in subset_set and line_word[idx] != codeword[idx]:
                raise AssertionError("line/codeword agreement failed")

        columns = [
            [pow(x, degree, p) * fixed_jet_theorem.inv_mod(lprime[x], p) % p for x in subset]
            for degree in range(r)
        ]
        with_beta = [
            row + [beta_column[row_index]]
            for row_index, row in enumerate(columns)
        ]
        if (
            fixed_jet_theorem.matrix_rank_mod(with_beta, p)
            != fixed_jet_theorem.matrix_rank_mod(columns, p) + 1
        ):
            raise AssertionError("beta column lies in the support span")

    return {
        "name": name,
        "field": f"F_{p}",
        "domain_size": n,
        "cosupport_size": j,
        "sigma": sigma,
        "dimension": k,
        "agreement": n - j,
        "two_ended_key": list(key),
        "selected_degrees": selected_degrees,
        "family_size": len(family),
        "distinct_bad_parameters": len(set(z_values.values())),
        "checks": {
            "two_ended_family": True,
            "selected_matrix_common": True,
            "selected_functional_recovers_beta_evaluation": True,
            "support_errors_constructed": True,
            "constructed_codewords_have_zero_syndrome": True,
            "agreement_on_D_minus_J": True,
            "vandermonde_noncontainment": True,
            "distinct_bad_parameters": len(set(z_values.values())) >= 2,
        },
    }


def rstar_points() -> list[smooth_padding.KElt]:
    return smooth_padding.inclusive_odd_slice(CYCLE119_A_SIZE, 255)


def product_constant(roots: Iterable[smooth_padding.KElt]) -> smooth_padding.KElt:
    out = smooth_padding.K_ONE
    count = 0
    for root in roots:
        out = smooth_padding.kmul(out, root)
        count += 1
    if count % 2:
        out = smooth_padding.kmul(smooth_padding.K_MINUS_ONE, out)
    return out


def build_report(local_reports: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    local_reports = local_reports or {}
    bridge_report = local_reports.get("fixed_jet") or fixed_jet_bridge.build_report()
    transfer_report = local_reports.get("fixed_transfer") or fixed_transfer.build_report()
    smooth_report = local_reports.get("smooth_padding") or smooth_padding.build_report()
    cycle84_report = local_reports.get("cycle84") or cycle84.build_report()
    color_report = local_reports.get("color_shell") or color_shell.build_report()
    gate_report = local_reports.get("gate") or gate.build_report()

    toy_cases = [
        check_two_ended_instance(
            name="sigma2_endpoint_family", p=17, n=6, j=2, sigma=2
        ),
        check_two_ended_instance(
            name="sigma3_endpoint_family", p=17, n=8, j=4, sigma=3
        ),
        check_two_ended_instance(
            name="sigma4_endpoint_family", p=17, n=11, j=4, sigma=4
        ),
        check_two_ended_instance(
            name="sigma5_endpoint_family", p=17, n=14, j=5, sigma=5
        ),
        check_two_ended_instance(
            name="sigma6_endpoint_family", p=23, n=17, j=6, sigma=6
        ),
    ]

    bridge = bridge_report["formal_reduction"]
    transfer = transfer_report["transfer"]
    smooth = smooth_report["smooth_padding"]
    exact = cycle84_report["cycle84_exact"]
    gate_arithmetic = gate_report["arithmetic"]
    rstar = rstar_points()
    p_rstar_beta = smooth_padding.product_at_beta(rstar)
    p_rstar_zero = product_constant(rstar)
    native_constant_exponent = (
        sum(range(1, 8)) + int(color_report["color_shell"]["target_color"])
    ) % 16

    checks = {
        "toy_cases_pass": all(all(case["checks"].values()) for case in toy_cases),
        "cycle116_fixed_jet_bridge_passes": bridge_report["status"] == "PASS",
        "cycle116_fixed_transfer_passes": transfer_report["status"] == "PASS",
        "cycle116_smooth_padding_passes": smooth_report["status"] == "PASS",
        "cycle84_exact_occupancy_passes": cycle84_report["status"] == "PASS",
        "color_shell_endpoint_passes": color_report["status"] == "PASS",
        "cycle120_gate_arithmetic_passes": gate_report["status"] == "PASS",
        "native_constant_is_minus_one_on_color_shell": (
            native_constant_exponent == 0
        ),
        "rstar_size_136": len(rstar) == CYCLE119_R_SIZE,
        "rstar_beta_nonzero": p_rstar_beta != smooth_padding.K_ZERO,
        "rstar_constant_nonzero": p_rstar_zero != smooth_padding.K_ZERO,
        "cycle119_sizes_match": (
            NATIVE_COSUPPORT_SIZE + CYCLE119_R_SIZE == CYCLE119_COSUPPORT_SIZE
            and NATIVE_AGREEMENT + CYCLE119_A_SIZE == CYCLE119_AGREEMENT
            and (
                CYCLE119_DIMENSION
                + CYCLE119_COSUPPORT_SIZE
                + CYCLE119_SIGMA
                == 512
            )
        ),
        "cycle119_two_ended_degree_bound": (
            CYCLE119_R_SIZE + NATIVE_REMAINDER_MAX_DEGREE
            == CYCLE119_COSUPPORT_SIZE - CYCLE119_SIGMA + 1
            == 243
        ),
        "cycle119_distinct_parameters_preserved": (
            int(exact["distinct_products"]) == EXPECTED_BAD_PARAMETERS
            and "Phi ->" in transfer["injectivity_reason"]
            and "P_T(beta)=4(beta-1)Phi(T)" in bridge_report["scalar_reduction"][
                "product_scalar"
            ]
        ),
        "cycle119_strict_ball_gate": (
            int(gate_arithmetic["cycle119_agreement"]) == CYCLE119_AGREEMENT
            and int(gate_arithmetic["cycle119_distance"]) == CYCLE119_DISTANCE
            and CYCLE119_DISTANCE < int(gate_arithmetic["distance_radius"])
        ),
        "cycle116_closed_row_still_recorded": (
            int(smooth["lift_agreement"]) == 262
            and int(gate_arithmetic["cycle116_agreement"]) == 262
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "PROVED / AUDIT / TWO-ENDED-FIXED-JET-LDSW-THEOREM",
        "theorem_problem_id": "M1 generic two-ended fixed-jet LD_sw transfer",
        "theorem": {
            "hypotheses": [
                "D has n distinct nonzero points and beta is outside D",
                "J ranges over j-subsets with common nonzero P_J(0)",
                "deg(P_J-P_J') <= j-sigma+1 for every pair J,J'",
                "k=n-j-sigma, sigma>=2, and P_J(beta) is nonzero",
            ],
            "conclusion": (
                "one affine line has at least #{P_J(beta)} support-wise bad "
                "parameters at agreement n-j"
            ),
            "mechanism": (
                "selected syndrome coordinates 0,j+1,...,j+sigma-1 recover "
                "A(beta) for every deg A<sigma; the beta column supplies the "
                "line direction and Vandermonde independence proves "
                "noncontainment"
            ),
        },
        "toy_cases": toy_cases,
        "cycle119_instantiation": {
            "field": "F_17^32",
            "domain_size": 512,
            "dimension": CYCLE119_DIMENSION,
            "cosupport_size": CYCLE119_COSUPPORT_SIZE,
            "sigma": CYCLE119_SIGMA,
            "agreement": CYCLE119_AGREEMENT,
            "distance": CYCLE119_DISTANCE,
            "strict_delta_bound": gate_arithmetic["cycle119_delta_bound"],
            "bad_parameters": int(exact["distinct_products"]),
            "native_color_shell_target": int(color_report["color_shell"]["target_color"]),
            "native_constant": "-1",
            "A_star_size": CYCLE119_A_SIZE,
            "R_star_size": CYCLE119_R_SIZE,
            "R_star_range": [CYCLE119_A_SIZE, 255],
            "P_Rstar_beta_nonzero": True,
            "P_Rstar_zero_nonzero": True,
            "two_ended_degree_bound": (
                "deg(P_Rstar(P_T-P_T')) <= 136+107=243=249-7+1"
            ),
            "product_scalar": (
                "P_Tstar(beta)=P_Rstar(beta)*4(beta-1)*Phi(T)"
            ),
        },
        "checks": checks,
        "remaining_imports": [
            "the Cycle84 exact occupancy chain for the number of distinct Phi values",
            "the Cycle116 slot identity and color-shell verifiers for the large "
            "concrete locator family",
            "the official ABF source gate if the row is promoted as prize-facing",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    inst = report["cycle119_instantiation"]

    print("m1_two_ended_fixed_jet_ldsw_theorem: PASS")
    print(f"status={report['proof_status']}")
    print(f"theorem_problem_id={report['theorem_problem_id']}")
    print(
        "toy_cases="
        + ", ".join(
            f"{case['name']}:family={case['family_size']},"
            f"bad={case['distinct_bad_parameters']},sigma={case['sigma']}"
            for case in report["toy_cases"]
        )
    )
    print(
        "cycle119="
        f"n={inst['domain_size']}, k={inst['dimension']}, "
        f"j={inst['cosupport_size']}, sigma={inst['sigma']}, "
        f"agreement={inst['agreement']}, distance={inst['distance']}, "
        f"bad_parameters={inst['bad_parameters']}"
    )
    print(
        "strict_ball="
        f"delta_bound={inst['strict_delta_bound']}, "
        f"A_star={inst['A_star_size']}, R_star={inst['R_star_size']}"
    )
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M1 generic two-ended fixed-jet LD_sw theorem."
    )
    parser.add_argument("--json", action="store_true", help="print JSON report")
    args = parser.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
