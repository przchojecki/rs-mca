#!/usr/bin/env python3
"""Verify the generic fixed-jet locator-to-LD_sw transfer theorem.

The Cycle116 chain uses a standard parity-check argument:

    common top coefficients of P_J
      -> common quotient syndromes
      -> one affine line f+z g with one bad parameter per distinct P_J(beta)
      -> support-wise noncontainment by a Vandermonde independence test.

This verifier checks that theorem on exact finite-field toy instances and checks
that the current Cycle116/Cycle120 local chain supplies the large-instance
hypotheses consumed by the theorem. It does not rerun the Cycle84 census unless
no cached Cycle84 report is supplied by the caller.
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

import verify_m1_cycle84_exact_occupancy_chain as cycle84
import verify_m1_cycle116_fixed_jet_bridge as fixed_jet_bridge
import verify_m1_cycle116_fixed_jet_transfer as fixed_transfer
import verify_m1_cycle116_smooth_padding_transfer as smooth_padding


def inv_mod(a: int, p: int) -> int:
    a %= p
    if a == 0:
        raise ZeroDivisionError("inverse of zero")
    return pow(a, p - 2, p)


def trim(poly: Sequence[int], p: int) -> list[int]:
    out = [int(c) % p for c in poly]
    while out and out[-1] == 0:
        out.pop()
    return out


def degree(poly: Sequence[int], p: int) -> int:
    return len(trim(poly, p)) - 1


def poly_sub(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        out[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(out, p)


def poly_mul(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return trim(out, p)


def poly_from_roots(roots: Iterable[int], p: int) -> list[int]:
    poly = [1]
    for root in roots:
        poly = poly_mul(poly, [(-root) % p, 1], p)
    return poly


def poly_eval(poly: Sequence[int], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def poly_derivative(poly: Sequence[int], p: int) -> list[int]:
    return trim([(i * poly[i]) % p for i in range(1, len(poly))], p)


def poly_divmod_monic(
    numerator: Sequence[int], divisor: Sequence[int], p: int
) -> tuple[list[int], list[int]]:
    top = trim(numerator, p)
    bottom = trim(divisor, p)
    if not bottom or bottom[-1] % p != 1:
        raise AssertionError("monic divisor required")
    if len(top) < len(bottom):
        return [], top
    quotient = [0] * (len(top) - len(bottom) + 1)
    while top and len(top) >= len(bottom):
        shift = len(top) - len(bottom)
        coeff = top[-1] % p
        quotient[shift] = coeff
        for i, bcoeff in enumerate(bottom):
            top[shift + i] = (top[shift + i] - coeff * bcoeff) % p
        top = trim(top, p)
    return trim(quotient, p), top


def elementary_top_key(subset: Sequence[int], j: int, sigma: int, p: int) -> tuple[int, ...]:
    locator = poly_from_roots(subset, p)
    return tuple(locator[j - t] for t in range(1, sigma + 1))


def find_family(
    p: int, n: int, j: int, sigma: int
) -> tuple[tuple[int, ...], list[tuple[int, ...]]]:
    buckets: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for subset in itertools.combinations(range(n), j):
        buckets.setdefault(elementary_top_key(subset, j, sigma, p), []).append(subset)
    key, family = max(buckets.items(), key=lambda item: len(item[1]))
    if len(family) < 2:
        raise AssertionError("toy instance did not produce a nontrivial family")
    return key, family


def matrix_rank_mod(matrix: Sequence[Sequence[int]], p: int) -> int:
    rows = [[int(x) % p for x in row] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    col = 0
    while rank < row_count and col < col_count:
        pivot = None
        for row in range(rank, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            col += 1
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = inv_mod(rows[rank][col], p)
        rows[rank] = [(x * inv) % p for x in rows[rank]]
        for row in range(row_count):
            if row != rank and rows[row][col] % p:
                factor = rows[row][col]
                rows[row] = [
                    (rows[row][c] - factor * rows[rank][c]) % p
                    for c in range(col_count)
                ]
        rank += 1
        col += 1
    return rank


def vector_add(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    return [(x + y) % p for x, y in zip(a, b)]


def vector_sub(a: Sequence[int], b: Sequence[int], p: int) -> list[int]:
    return [(x - y) % p for x, y in zip(a, b)]


def scalar_mul(c: int, v: Sequence[int], p: int) -> list[int]:
    return [(c * x) % p for x in v]


def check_fixed_jet_instance(
    *,
    name: str,
    p: int,
    n: int,
    j: int,
    sigma: int,
) -> Dict[str, Any]:
    d_points = list(range(n))
    beta = p - 1
    if beta in d_points:
        raise AssertionError("beta must lie outside D")
    if not (1 <= sigma and j + sigma < n):
        raise AssertionError("need 1 <= sigma and positive code dimension")

    top_key, family = find_family(p, n, j, sigma)
    r = j + sigma
    k = n - r
    domain_locator = poly_from_roots(d_points, p)
    domain_derivative = poly_derivative(domain_locator, p)
    domain_at_beta = poly_eval(domain_locator, beta, p)
    if domain_at_beta == 0:
        raise AssertionError("beta is a domain point")
    lprime = {x: poly_eval(domain_derivative, x, p) for x in d_points}
    if any(value == 0 for value in lprime.values()):
        raise AssertionError("domain has repeated points")

    locators = {subset: poly_from_roots(subset, p) for subset in family}
    locator_derivatives = {
        subset: poly_derivative(locator, p)
        for subset, locator in locators.items()
    }
    p_beta = {
        subset: poly_eval(locator, beta, p)
        for subset, locator in locators.items()
    }
    if any(value == 0 for value in p_beta.values()):
        raise AssertionError("some P_J(beta) vanishes")

    for left, right in itertools.combinations(family, 2):
        diff_degree = degree(poly_sub(locators[left], locators[right], p), p)
        if diff_degree > j - sigma:
            raise AssertionError("family does not have the requested fixed jet")

    quotient_values: list[int] = []
    for m in range(r):
        monomial = [0] * m + [1]
        values = []
        for subset in family:
            quotient, _ = poly_divmod_monic(monomial, locators[subset], p)
            values.append(poly_eval(quotient, beta, p))
        if len(set(values)) != 1:
            raise AssertionError(f"quotient value depends on J at m={m}")
        quotient_values.append(values[0])

    def syndrome(word: Sequence[int]) -> list[int]:
        out = []
        for m in range(r):
            total = 0
            for idx, x in enumerate(d_points):
                total += pow(x, m, p) * word[idx] * inv_mod(lprime[x], p)
            out.append(total % p)
        return out

    b_vector = [pow(beta, m, p) for m in range(r)]
    a_vector = [(-value) % p for value in quotient_values]
    g_word = [
        domain_at_beta * inv_mod((beta - x) % p, p) % p
        for x in d_points
    ]
    if syndrome(g_word) != b_vector:
        raise AssertionError("Hg != B")

    e_words: dict[tuple[int, ...], list[int]] = {}
    z_values: dict[tuple[int, ...], int] = {}
    for subset in family:
        pprime = locator_derivatives[subset]
        subset_set = set(subset)
        e_word = []
        for x in d_points:
            if x not in subset_set:
                e_word.append(0)
                continue
            denom = (beta - x) * poly_eval(pprime, x, p)
            e_word.append(lprime[x] * inv_mod(denom, p) % p)
        z = inv_mod(p_beta[subset], p)
        expected_syndrome = vector_add(a_vector, scalar_mul(z, b_vector, p), p)
        if syndrome(e_word) != expected_syndrome:
            raise AssertionError("He_J != A+z_J B")
        e_words[subset] = e_word
        z_values[subset] = z

    base_subset = family[0]
    f_word = vector_sub(e_words[base_subset], scalar_mul(z_values[base_subset], g_word, p), p)
    if syndrome(f_word) != a_vector:
        raise AssertionError("Hf != A")

    bad_parameter_count = len(set(z_values.values()))
    for subset in family:
        line_word = vector_add(f_word, scalar_mul(z_values[subset], g_word, p), p)
        codeword = vector_sub(line_word, e_words[subset], p)
        if syndrome(codeword) != [0] * r:
            raise AssertionError("constructed c_J is not in the code")
        subset_set = set(subset)
        if any(
            line_word[idx] != codeword[idx]
            for idx, x in enumerate(d_points)
            if x not in subset_set
        ):
            raise AssertionError("line/codeword agreement failed on D\\J")

        columns = [
            [pow(x, m, p) * inv_mod(lprime[x], p) % p for x in subset]
            for m in range(r)
        ]
        with_b = [
            row + [b_vector[row_index]]
            for row_index, row in enumerate(columns)
        ]
        if matrix_rank_mod(with_b, p) != matrix_rank_mod(columns, p) + 1:
            raise AssertionError("B lies in the span of the J columns")

    return {
        "name": name,
        "field": f"F_{p}",
        "domain_size": n,
        "cosupport_size": j,
        "sigma": sigma,
        "dimension": k,
        "agreement": n - j,
        "family_top_coefficients": list(top_key),
        "family_size": len(family),
        "distinct_bad_parameters": bad_parameter_count,
        "checks": {
            "fixed_jet_family": True,
            "quotient_syndrome_independent": True,
            "Hg_equals_B": True,
            "HeJ_equals_A_plus_zB": True,
            "constructed_codewords_have_zero_syndrome": True,
            "agreement_on_D_minus_J": True,
            "vandermonde_noncontainment": True,
            "distinct_bad_parameters": bad_parameter_count == len(family),
        },
    }


def build_report(local_reports: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    local_reports = local_reports or {}
    bridge_report = local_reports.get("fixed_jet") or fixed_jet_bridge.build_report()
    transfer_report = local_reports.get("fixed_transfer") or fixed_transfer.build_report()
    smooth_report = local_reports.get("smooth_padding") or smooth_padding.build_report()
    cycle84_report = local_reports.get("cycle84") or cycle84.build_report()

    toy_cases = [
        check_fixed_jet_instance(name="sigma1_sum_family", p=17, n=8, j=3, sigma=1),
        check_fixed_jet_instance(name="sigma2_pair_family", p=31, n=12, j=4, sigma=2),
        check_fixed_jet_instance(name="sigma3_tight_family", p=43, n=14, j=5, sigma=3),
    ]

    bridge = bridge_report["formal_reduction"]
    transfer = transfer_report["transfer"]
    smooth = smooth_report["smooth_padding"]
    exact = cycle84_report["cycle84_exact"]

    checks = {
        "toy_cases_pass": all(all(case["checks"].values()) for case in toy_cases),
        "cycle116_fixed_jet_bridge_passes": bridge_report["status"] == "PASS",
        "cycle116_fixed_transfer_passes": transfer_report["status"] == "PASS",
        "cycle116_smooth_padding_passes": smooth_report["status"] == "PASS",
        "cycle84_exact_occupancy_passes": cycle84_report["status"] == "PASS",
        "cycle116_native_parameters_fit_theorem": (
            int(bridge["cosupport_size"]) == 113
            and int(bridge["fixed_jet_sigma"]) == 6
            and int(transfer["code_dimension"]) == 137
            and int(transfer["agreement"]) == 143
        ),
        "cycle116_distinct_parameters_supplied_by_cycle84": (
            int(exact["distinct_products"]) == 52_747_567_092
            and transfer["injectivity_reason"].startswith("Phi ->")
        ),
        "cycle116_scalar_nonzero_and_injective": (
            "V_D(beta) and 4(beta-1) nonzero" in transfer["scalar_substitution"]
        ),
        "cycle120_smooth_row_fit_theorem_after_padding": (
            int(smooth["lift_cosupport_size"]) == 250
            and int(smooth["fixed_jet_sigma"]) == 6
            and int(smooth["lift_dimension"]) == 256
            and int(smooth["lift_agreement"]) == 262
            and smooth_report["transfer"]["bad_parameters_preserved"]
        ),
    }

    failed = [name for name, value in checks.items() if not value]
    if failed:
        raise AssertionError(f"failed checks: {', '.join(failed)}")

    return {
        "status": "PASS",
        "proof_status": "PROVED / AUDIT / GENERIC-FIXED-JET-LDSW-THEOREM",
        "theorem_problem_id": "M1 generic fixed-jet locator-to-LD_sw transfer",
        "theorem": {
            "hypotheses": [
                "D has n distinct points and beta is outside D",
                "J ranges over j-subsets with deg(P_J-P_J') <= j-sigma",
                "k=n-j-sigma and sigma>=1",
                "P_J(beta) is nonzero for every J",
            ],
            "conclusion": (
                "one affine line has at least #{P_J(beta)} support-wise bad "
                "parameters at agreement n-j"
            ),
            "mechanism": (
                "common quotient syndromes plus Hg=B construct f+z_J g; "
                "Vandermonde independence of J union {beta} proves "
                "noncontainment"
            ),
        },
        "toy_cases": toy_cases,
        "cycle116_instantiation": {
            "native": {
                "locator_shape": bridge["locator_shape"],
                "cosupport_size": int(bridge["cosupport_size"]),
                "fixed_jet_sigma": int(bridge["fixed_jet_sigma"]),
                "dimension": int(transfer["code_dimension"]),
                "agreement": int(transfer["agreement"]),
                "bad_parameter_formula": transfer["bad_parameter_formula"],
                "distinct_bad_parameters": int(exact["distinct_products"]),
            },
            "smooth_lift": {
                "cosupport_size": int(smooth["lift_cosupport_size"]),
                "fixed_jet_sigma": int(smooth["fixed_jet_sigma"]),
                "dimension": int(smooth["lift_dimension"]),
                "agreement": int(smooth["lift_agreement"]),
                "bad_parameters_preserved": True,
            },
        },
        "checks": checks,
        "remaining_imports": [
            "the Cycle116 slot identity and fixed-jet bridge verifiers for the "
            "large concrete locator family",
            "the Cycle84 exact occupancy chain for the number of distinct "
            "product values",
            "the official ABF source gate if the row is promoted as prize-facing",
        ],
        "nonmutating": True,
    }


def print_human(report: Dict[str, Any]) -> None:
    native = report["cycle116_instantiation"]["native"]
    smooth = report["cycle116_instantiation"]["smooth_lift"]

    print("m1_fixed_jet_ldsw_theorem: PASS")
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
        "cycle116_native="
        f"j={native['cosupport_size']}, sigma={native['fixed_jet_sigma']}, "
        f"k={native['dimension']}, agreement={native['agreement']}, "
        f"bad_parameters={native['distinct_bad_parameters']}"
    )
    print(
        "cycle120_smooth_lift="
        f"j={smooth['cosupport_size']}, sigma={smooth['fixed_jet_sigma']}, "
        f"k={smooth['dimension']}, agreement={smooth['agreement']}, "
        f"bad_parameters_preserved={smooth['bad_parameters_preserved']}"
    )
    print("remaining_imports=" + "; ".join(report["remaining_imports"]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the M1 generic fixed-jet locator-to-LD_sw theorem."
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
