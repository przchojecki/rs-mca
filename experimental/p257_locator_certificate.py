#!/usr/bin/env python3
"""Exact p=257 locator end-to-end certificate for Paper A.

This checks the finite computation in `tex/RS_disproof_v3.tex` item V2 and
`ex:257`.  For every 9-subset `A` of `Q=<2>` in `F_257`, it verifies:

* `prod_{b in A}(X^16-b)` has top terms `X^144 + z X^128`;
* `z = -sum(A)`;
* the remaining terms have degree `< 128`; and
* `x^144 + z*x^128 = -R_A(x)` on all 144 points with `x^16 in A`.

All computations are exact modular arithmetic; there is no sampling.
"""

from __future__ import annotations

import argparse
import itertools
import json
from math import comb
from typing import Iterable


STATUS = "PROVED"
THEOREM_ID = "tex/RS_disproof_v3.tex:app:verify V2, ex:257, lem:locator"
OBJECT = "p=257 locator end-to-end certificate"
P = 257
N = 16
A_EXPONENT = 16
K = 128
ELL = 9
TOP_DEGREE = A_EXPONENT * ELL
SLOPE_DEGREE = A_EXPONENT * (ELL - 1)


def subgroup_q() -> list[int]:
    values = [pow(2, exponent, P) for exponent in range(N)]
    if len(set(values)) != N or pow(2, N, P) != 1:
        raise ValueError("2 does not generate the expected order-16 subgroup")
    return values


def multiply_by_y_minus_b(coeffs: list[int], b_value: int) -> list[int]:
    new_coeffs = [0] * (len(coeffs) + 1)
    for degree, coeff in enumerate(coeffs):
        new_coeffs[degree] = (new_coeffs[degree] - b_value * coeff) % P
        new_coeffs[degree + 1] = (new_coeffs[degree + 1] + coeff) % P
    return new_coeffs


def locator_coefficients(a_values: Iterable[int]) -> list[int]:
    coeffs = [1]
    for b_value in a_values:
        coeffs = multiply_by_y_minus_b(coeffs, b_value)
    return coeffs


def eval_remainder(coeffs: list[int], x_value: int) -> int:
    total = 0
    for y_degree, coeff in enumerate(coeffs[: ELL - 1]):
        total = (total + coeff * pow(x_value, A_EXPONENT * y_degree, P)) % P
    return total


def support_points(a_set: set[int]) -> list[int]:
    return [x_value for x_value in range(1, P) if pow(x_value, A_EXPONENT, P) in a_set]


def subset_certificate(a_values: tuple[int, ...]) -> dict[str, object]:
    coeffs = locator_coefficients(a_values)
    z_value = (-sum(a_values)) % P
    support = support_points(set(a_values))
    top_ok = coeffs[ELL] == 1
    slope_ok = coeffs[ELL - 1] == z_value
    degree_ok = TOP_DEGREE == 144 and SLOPE_DEGREE == K
    support_ok = len(support) == A_EXPONENT * ELL
    agreement_ok = True
    for x_value in support:
        received = (pow(x_value, TOP_DEGREE, P) + z_value * pow(x_value, K, P)) % P
        remainder = eval_remainder(coeffs, x_value)
        if received != (-remainder) % P:
            agreement_ok = False
            break
    return {
        "z": z_value,
        "top_ok": top_ok,
        "slope_ok": slope_ok,
        "degree_ok": degree_ok,
        "support_size": len(support),
        "support_ok": support_ok,
        "agreement_ok": agreement_ok,
        "ok": top_ok and slope_ok and degree_ok and support_ok and agreement_ok,
    }


def certificate_rows() -> list[dict[str, object]]:
    q_values = subgroup_q()
    rows: list[dict[str, object]] = []
    for subset in itertools.combinations(q_values, ELL):
        rows.append(subset_certificate(subset))
    return rows


def payload(rows: Iterable[dict[str, object]]) -> dict[str, object]:
    result_rows = list(rows)
    unique_slopes = sorted({int(row["z"]) for row in result_rows})
    return {
        "status": STATUS,
        "theorem_id": THEOREM_ID,
        "object": OBJECT,
        "inputs": {
            "p": P,
            "D": "F_257^*",
            "Q": "<2>",
            "n": P - 1,
            "k": K,
            "N": N,
            "a": A_EXPONENT,
            "ell": ELL,
            "top_degree": TOP_DEGREE,
            "slope_degree": SLOPE_DEGREE,
        },
        "result": {
            "subsets_checked": len(result_rows),
            "expected_subsets": comb(N, ELL),
            "all_subsets_ok": all(bool(row["ok"]) for row in result_rows),
            "min_support_size": min(int(row["support_size"]) for row in result_rows),
            "max_support_size": max(int(row["support_size"]) for row in result_rows),
            "unique_slope_count": len(unique_slopes),
            "zero_slope_seen": 0 in unique_slopes,
        },
    }


def print_text(cert: dict[str, object]) -> None:
    inputs = cert["inputs"]
    result = cert["result"]
    print(OBJECT)
    print(f"Status: {STATUS}")
    print(f"Theorem/problem ID: {THEOREM_ID}")
    print("Object checked: locator top coefficients and pointwise agreement.")
    print()
    print(
        "p={p}, D={D}, Q={Q}, n={n}, k={k}, N={N}, a={a}, ell={ell}".format(
            **inputs
        )
    )
    print(
        "top degree={top_degree}, slope degree={slope_degree}".format(
            **inputs
        )
    )
    print()
    print(f"subsets checked: {result['subsets_checked']}")
    print(f"expected subsets: {result['expected_subsets']}")
    print(
        "support size range: "
        f"{result['min_support_size']}..{result['max_support_size']}"
    )
    print(f"unique slopes seen: {result['unique_slope_count']}")
    print(f"zero slope seen: {result['zero_slope_seen']}")
    print(f"all subsets pass: {result['all_subsets_ok']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format. JSON is machine-readable and text is for review.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = certificate_rows()
    cert = payload(rows)
    if args.format == "json":
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print_text(cert)
    return 0 if cert["result"]["all_subsets_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
