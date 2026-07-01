#!/usr/bin/env python3
"""
Canonical regular Hankel rank-drop eliminant scanner over a prime field.

For an affine received line f + Z g, supply syndrome vectors u=Syn(f) and
v=Syn(g), each of length r=n-k.  For exact agreement A, the regular Hankel
pencil is

    M_A(Z) = H_{t,j}(u) + Z H_{t,j}(v),
    j=n-A,  t=A-k.

When t >= j+1, this script computes every maximal minor, their monic squarefree
common gcd G_A^rd, and the roots in GF(p).  With --a, it also forms the
squarefree lcm of the exact-agreement gcds for A >= a that are regular and
nonsingular.

This is a certificate-prototyping tool for small examples; it is not optimized
for cryptographic challenge rows.

Examples:
    python regular_hankel_eliminant.py --p 101 --n 12 --k 5 --A 9 \
        --u 3,5,7,11,13,17,19 --v 2,4,8,16,32,64,27

    python regular_hankel_eliminant.py --p 101 --n 12 --k 5 --a 8 \
        --u 3,5,7,11,13,17,19 --v 2,4,8,16,32,64,27
"""
from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class ExactAgreementResult:
    A: int
    j: int
    t: int
    overdetermined: bool
    num_maximal_minors: int
    num_nonzero_minors: int
    hankel_singular: bool
    gcd_degree: int | None
    gcd_coeffs_low_to_high: list[int]
    roots: list[int]
    residual_reason: str | None


@dataclass(frozen=True)
class ClosedBallResult:
    p: int
    n: int
    k: int
    a: int
    r: int
    regular_exact_agreements: list[int]
    residual_exact_agreements: dict[str, list[int]]
    lcm_degree: int
    lcm_coeffs_low_to_high: list[int]
    roots: list[int]
    exact_results: list[ExactAgreementResult]


def parse_vec(raw: str, p: int, expected_len: int, name: str) -> list[int]:
    vals = [int(x.strip()) % p for x in raw.split(",") if x.strip()]
    if len(vals) != expected_len:
        raise SystemExit(f"{name} must have length r=n-k={expected_len}, got {len(vals)}")
    return vals


def hankel(vec: list[int], t: int, j: int) -> list[list[int]]:
    return [[vec[a + b] for b in range(j + 1)] for a in range(t)]


def trim(poly: list[int], p: int) -> list[int]:
    out = [value % p for value in poly]
    while out and out[-1] == 0:
        out.pop()
    return out


def degree(poly: list[int]) -> int:
    return len(poly) - 1


def is_zero(poly: list[int]) -> bool:
    return not poly


def monic(poly: list[int], p: int) -> list[int]:
    poly = trim(poly, p)
    if not poly:
        return []
    inv = pow(poly[-1], -1, p)
    return [(inv * coeff) % p for coeff in poly]


def poly_add(left: list[int], right: list[int], p: int) -> list[int]:
    length = max(len(left), len(right))
    out = [0] * length
    for i in range(length):
        out[i] = ((left[i] if i < len(left) else 0) + (right[i] if i < len(right) else 0)) % p
    return trim(out, p)


def poly_sub(left: list[int], right: list[int], p: int) -> list[int]:
    length = max(len(left), len(right))
    out = [0] * length
    for i in range(length):
        out[i] = ((left[i] if i < len(left) else 0) - (right[i] if i < len(right) else 0)) % p
    return trim(out, p)


def poly_mul(left: list[int], right: list[int], p: int) -> list[int]:
    if not left or not right:
        return []
    out = [0] * (len(left) + len(right) - 1)
    for i, a_i in enumerate(left):
        for j, b_j in enumerate(right):
            out[i + j] = (out[i + j] + a_i * b_j) % p
    return trim(out, p)


def poly_derivative(poly: list[int], p: int) -> list[int]:
    return trim([(i * coeff) % p for i, coeff in enumerate(poly[1:], start=1)], p)


def poly_divmod(numerator: list[int], denominator: list[int], p: int) -> tuple[list[int], list[int]]:
    numerator = trim(numerator, p)
    denominator = trim(denominator, p)
    if not denominator:
        raise ZeroDivisionError("polynomial division by zero")
    if degree(numerator) < degree(denominator):
        return [], numerator

    quotient = [0] * (degree(numerator) - degree(denominator) + 1)
    remainder = numerator[:]
    inv_lead = pow(denominator[-1], -1, p)
    while remainder and degree(remainder) >= degree(denominator):
        shift = degree(remainder) - degree(denominator)
        coeff = remainder[-1] * inv_lead % p
        quotient[shift] = coeff
        subtractor = [0] * shift + [(coeff * value) % p for value in denominator]
        remainder = poly_sub(remainder, subtractor, p)
    return trim(quotient, p), trim(remainder, p)


def poly_gcd(left: list[int], right: list[int], p: int) -> list[int]:
    left = trim(left, p)
    right = trim(right, p)
    while right:
        _, rem = poly_divmod(left, right, p)
        left, right = right, rem
    return monic(left, p)


def gcd_many(polys: Iterable[list[int]], p: int) -> list[int]:
    nonzero = [monic(f, p) for f in polys if not is_zero(f)]
    if not nonzero:
        return []
    g = nonzero[0]
    for f in nonzero[1:]:
        g = poly_gcd(g, f, p)
        if degree(g) == 0:
            break
    return g


def lcm_poly(a: list[int], b: list[int], p: int) -> list[int]:
    if is_zero(a) or is_zero(b):
        raise ValueError("lcm_poly expects nonzero polynomials")
    a = monic(a, p)
    b = monic(b, p)
    g = poly_gcd(a, b, p)
    quotient, remainder = poly_divmod(a, g, p)
    if remainder:
        raise AssertionError("gcd did not divide polynomial")
    return monic(poly_mul(quotient, b, p), p)


def squarefree_part(f: list[int], p: int) -> list[int]:
    f = monic(f, p)
    if not f or degree(f) <= 0:
        return f
    deriv = poly_derivative(f, p)
    if not deriv:
        # Rare inseparable case. Root enumeration remains exact below, but the
        # displayed degree may include multiplicity. For small prototype fields,
        # keep the monic polynomial rather than guessing p-th roots.
        return f
    g = poly_gcd(f, deriv, p)
    quotient, remainder = poly_divmod(f, g, p)
    if remainder:
        raise AssertionError("squarefree gcd did not divide polynomial")
    return monic(quotient, p)


def coeffs_low_to_high(f: list[int], p: int) -> list[int]:
    return trim(f, p)


def poly_eval(poly: list[int], value: int, p: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % p
        power = (power * value) % p
    return total


def roots_in_prime_field(f: list[int], p: int) -> list[int]:
    if is_zero(f):
        return list(range(p))
    if degree(f) <= 0:
        return []
    return [z for z in range(p) if poly_eval(f, z, p) == 0]


def det_poly_matrix(matrix: list[list[list[int]]], p: int) -> list[int]:
    size = len(matrix)
    if size == 0:
        return [1]
    if size == 1:
        return trim(matrix[0][0], p)

    total: list[int] = []
    for col, entry in enumerate(matrix[0]):
        if is_zero(entry):
            continue
        submatrix = [row[:col] + row[col + 1 :] for row in matrix[1:]]
        term = poly_mul(entry, det_poly_matrix(submatrix, p), p)
        if col % 2:
            total = poly_sub(total, term, p)
        else:
            total = poly_add(total, term, p)
    return trim(total, p)


def affine_entry(constant: int, linear: int, p: int) -> list[int]:
    return trim([constant % p, linear % p], p)


def maximal_minors(p: int, u: list[int], v: list[int], A: int, n: int, k: int) -> list[list[int]]:
    j = n - A
    t = A - k
    Hu = hankel(u, t, j)
    Hv = hankel(v, t, j)
    minors: list[list[int]] = []
    for row_idx in itertools.combinations(range(t), j + 1):
        mat = [
            [affine_entry(Hu[a][b], Hv[a][b], p) for b in range(j + 1)]
            for a in row_idx
        ]
        minors.append(det_poly_matrix(mat, p))
    return minors


def exact_agreement(p: int, n: int, k: int, A: int, u: list[int], v: list[int]) -> tuple[ExactAgreementResult, list[int] | None]:
    if not (k < A <= n):
        raise SystemExit("Need k < A <= n for exact agreement A.")
    j = n - A
    t = A - k
    if t < j + 1:
        return ExactAgreementResult(
            A=A, j=j, t=t, overdetermined=False, num_maximal_minors=0,
            num_nonzero_minors=0, hankel_singular=False, gcd_degree=None,
            gcd_coeffs_low_to_high=[], roots=[], residual_reason="underdetermined",
        ), None

    minors = maximal_minors(p, u, v, A, n, k)
    nonzero = [m for m in minors if not is_zero(m)]
    if not nonzero:
        return ExactAgreementResult(
            A=A, j=j, t=t, overdetermined=True, num_maximal_minors=len(minors),
            num_nonzero_minors=0, hankel_singular=True, gcd_degree=None,
            gcd_coeffs_low_to_high=[], roots=list(range(p)), residual_reason="hankel_singular",
        ), None

    g = squarefree_part(gcd_many(nonzero, p), p)
    roots = roots_in_prime_field(g, p)
    return ExactAgreementResult(
        A=A, j=j, t=t, overdetermined=True, num_maximal_minors=len(minors),
        num_nonzero_minors=len(nonzero), hankel_singular=False, gcd_degree=degree(g),
        gcd_coeffs_low_to_high=coeffs_low_to_high(g, p), roots=roots,
        residual_reason=None,
    ), g


def closed_ball(p: int, n: int, k: int, a: int, u: list[int], v: list[int]) -> ClosedBallResult:
    if not (k < a <= n):
        raise SystemExit("Need k < a <= n for threshold a.")
    exact_results: list[ExactAgreementResult] = []
    lcm = [1]
    regular: list[int] = []
    residual = {"underdetermined": [], "hankel_singular": []}

    for A in range(a, n + 1):
        result, g = exact_agreement(p, n, k, A, u, v)
        exact_results.append(result)
        if g is None:
            if result.residual_reason:
                residual[result.residual_reason].append(A)
            continue
        regular.append(A)
        lcm = lcm_poly(lcm, g, p)
    lcm = squarefree_part(lcm, p)
    roots = roots_in_prime_field(lcm, p)
    return ClosedBallResult(
        p=p, n=n, k=k, a=a, r=n-k,
        regular_exact_agreements=regular,
        residual_exact_agreements=residual,
        lcm_degree=degree(lcm),
        lcm_coeffs_low_to_high=coeffs_low_to_high(lcm, p),
        roots=roots,
        exact_results=exact_results,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, required=True, help="prime modulus")
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--k", type=int, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--A", type=int, help="single exact agreement")
    group.add_argument("--a", type=int, help="closed-ball threshold agreement")
    parser.add_argument("--u", required=True, help="comma-separated syndrome vector Syn(f)")
    parser.add_argument("--v", required=True, help="comma-separated syndrome vector Syn(g)")
    args = parser.parse_args()

    r = args.n - args.k
    u = parse_vec(args.u, args.p, r, "u")
    v = parse_vec(args.v, args.p, r, "v")
    if args.A is not None:
        result, _ = exact_agreement(args.p, args.n, args.k, args.A, u, v)
        print(json.dumps(asdict(result), indent=2, sort_keys=True))
    else:
        result = closed_ball(args.p, args.n, args.k, args.a, u, v)
        print(json.dumps(asdict(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
