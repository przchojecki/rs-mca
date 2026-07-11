#!/usr/bin/env python3
"""Regression verifier for the B2 twisted Hankel transform packet.

The script checks exact small-field instances of the divisor identities,
uniform subset Fourier inversion, the nonsingular twisted Hankel transform,
and the abstract polar/endpoint cancellation lemmas.  It does not prove the
deployed CHG estimate or identify the deployed zero-fiber twist with e_0.

Status: PROVED EXACT REDUCTIONS AND FULL-RANK BRIDGE / OPEN SIGNED CHG ESTIMATE.
"""
from __future__ import annotations

import argparse
import cmath
import copy
import hashlib
import itertools
import json
import math
import random
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Sequence


THEOREM_ID = "b2-twisted-hankel-transform-v1"
STATUS = "PROVED EXACT REDUCTIONS AND FULL-RANK BRIDGE / OPEN SIGNED CHG ESTIMATE"
SEED = 20260711
TOL = 2.0e-9
CERT = Path(
    "experimental/data/certificates/b2-twisted-hankel-transform-v1/"
    "b2_twisted_hankel_transform_v1.json"
)
NOTE = Path("experimental/notes/roadmaps/b2_twisted_hankel_transform_v1.md")
PRIOR = Path("experimental/notes/roadmaps/b2_hankel_gauss_reduction.md")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def normalize(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 12)
    if isinstance(value, complex):
        return {"real": round(value.real, 12), "imag": round(value.imag, 12)}
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    return value


def payload_hash(payload: dict[str, Any]) -> str:
    clean = copy.deepcopy(payload)
    clean.pop("payload_sha256", None)
    encoded = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def vectors(p: int, length: int) -> Iterable[tuple[int, ...]]:
    return itertools.product(range(p), repeat=length)


def dot(left: Sequence[int], right: Sequence[int], p: int) -> int:
    return sum(a * b for a, b in zip(left, right)) % p


def trim(poly: Sequence[int], p: int) -> tuple[int, ...]:
    result = [value % p for value in poly]
    while result and result[-1] == 0:
        result.pop()
    return tuple(result)


def poly_add(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return trim(
        [
            (left[i] if i < len(left) else 0)
            + (right[i] if i < len(right) else 0)
            for i in range(size)
        ],
        p,
    )


def poly_sub(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return trim(
        [
            (left[i] if i < len(left) else 0)
            - (right[i] if i < len(right) else 0)
            for i in range(size)
        ],
        p,
    )


def poly_scale(poly: Sequence[int], scalar: int, p: int) -> tuple[int, ...]:
    return trim([(scalar * value) % p for value in poly], p)


def poly_mul(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    if not left or not right:
        return ()
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] = (result[i + j] + a * b) % p
    return trim(result, p)


def poly_divmod(
    numerator: Sequence[int], denominator: Sequence[int], p: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    num = list(trim(numerator, p))
    den = trim(denominator, p)
    if not den:
        raise ZeroDivisionError("zero polynomial")
    if len(num) < len(den):
        return (), tuple(num)
    quotient = [0] * (len(num) - len(den) + 1)
    inv_lead = pow(den[-1], -1, p)
    while num and len(num) >= len(den):
        shift = len(num) - len(den)
        factor = num[-1] * inv_lead % p
        quotient[shift] = factor
        for index, coefficient in enumerate(den):
            num[shift + index] = (num[shift + index] - factor * coefficient) % p
        while num and num[-1] == 0:
            num.pop()
    return trim(quotient, p), trim(num, p)


def divides(divisor: Sequence[int], value: Sequence[int], p: int) -> bool:
    return not poly_divmod(value, divisor, p)[1]


def poly_monic(poly: Sequence[int], p: int) -> tuple[int, ...]:
    value = trim(poly, p)
    if not value:
        return ()
    return poly_scale(value, pow(value[-1], -1, p), p)


def poly_gcd(left: Sequence[int], right: Sequence[int], p: int) -> tuple[int, ...]:
    a = trim(left, p)
    b = trim(right, p)
    while b:
        _, remainder = poly_divmod(a, b, p)
        a, b = b, remainder
    return poly_monic(a, p)


def poly_derivative(poly: Sequence[int], p: int) -> tuple[int, ...]:
    return trim([index * poly[index] for index in range(1, len(poly))], p)


def poly_shift(poly: Sequence[int], amount: int, p: int) -> tuple[int, ...]:
    if not poly:
        return ()
    return trim([0] * amount + list(poly), p)


def poly_eval(poly: Sequence[int], point: int, p: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * point + coefficient) % p
    return value


def locator(points: Sequence[int], p: int) -> tuple[int, ...]:
    result: tuple[int, ...] = (1,)
    for point in points:
        result = poly_mul(result, ((-point) % p, 1), p)
    return result


def primitive_root(p: int) -> int:
    factors = []
    value = p - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise AssertionError("primitive root not found")


def roots_of_unity(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n:
        raise ValueError("n must divide p-1")
    generator = primitive_root(p)
    root = pow(generator, (p - 1) // n, p)
    points = tuple(pow(root, index, p) for index in range(n))
    if len(set(points)) != n:
        raise AssertionError("root order mismatch")
    return points


def legendre(value: int, p: int) -> int:
    value %= p
    if value == 0:
        return 0
    result = pow(value, (p - 1) // 2, p)
    return -1 if result == p - 1 else result


def matrix_det(matrix: Sequence[Sequence[int]], p: int) -> int:
    work = [list(row) for row in matrix]
    determinant = 1
    size = len(work)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column] % p), None)
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column] % p
        determinant = determinant * pivot_value % p
        inverse = pow(pivot_value, -1, p)
        for row in range(column + 1, size):
            factor = work[row][column] * inverse % p
            for index in range(column, size):
                work[row][index] = (work[row][index] - factor * work[column][index]) % p
    return determinant % p


def matrix_inverse(matrix: Sequence[Sequence[int]], p: int) -> tuple[tuple[int, ...], ...]:
    size = len(matrix)
    work = [
        [value % p for value in row]
        + [1 if row_index == column else 0 for column in range(size)]
        for row_index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column] % p), None)
        if pivot is None:
            raise ZeroDivisionError("singular matrix")
        work[column], work[pivot] = work[pivot], work[column]
        inverse = pow(work[column][column], -1, p)
        work[column] = [(value * inverse) % p for value in work[column]]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column] % p
            work[row] = [
                (work[row][index] - factor * work[column][index]) % p
                for index in range(2 * size)
            ]
    return tuple(tuple(row[size:]) for row in work)


def quadratic_form(vector: Sequence[int], matrix: Sequence[Sequence[int]], p: int) -> int:
    return sum(
        vector[i] * matrix[i][j] * vector[j]
        for i in range(len(vector))
        for j in range(len(vector))
    ) % p


def hankel(vector: Sequence[int], c: int) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(vector[i + j] for j in range(c)) for i in range(c))


def square_coefficients(vector: Sequence[int], p: int) -> tuple[int, ...]:
    return poly_mul(vector, vector, p)


@lru_cache(maxsize=None)
def projective_polynomials(p: int, degree_bound: int) -> tuple[tuple[int, ...], ...]:
    if degree_bound < 0:
        return ()
    result = []
    length = degree_bound + 1
    for first_nonzero in range(length):
        suffix_length = length - first_nonzero - 1
        for suffix in vectors(p, suffix_length):
            result.append(tuple([0] * first_nonzero + [1] + list(suffix)))
    return tuple(result)


def fixed_add(
    left: Sequence[int], right: Sequence[int], length: int, p: int
) -> tuple[int, ...]:
    return tuple(
        (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        )
        % p
        for index in range(length)
    )


def homogeneous_divides(
    divisor: Sequence[int],
    divisor_degree: int,
    value: Sequence[int],
    ambient_degree: int,
    p: int,
) -> bool:
    """Test divisibility of fixed-degree binary forms after dehomogenization.

    A coefficient vector in P(V_j) represents a homogeneous binary form of
    degree exactly j, even when its dehomogenization has degree below j.  The
    quotient must therefore have dehomogenized degree at most D-j.
    """
    if not trim(value, p):
        return True
    quotient, remainder = poly_divmod(value, divisor, p)
    return not remainder and len(quotient) - 1 <= ambient_degree - divisor_degree


@lru_cache(maxsize=None)
def omega_cached(
    p: int, degree_bound: int, ambient_degree: int, value: tuple[int, ...]
) -> int:
    if degree_bound < 0:
        return 0
    return sum(
        homogeneous_divides(divisor, degree_bound, value, ambient_degree, p)
        for divisor in projective_polynomials(p, degree_bound)
    )


def omega(
    value: Sequence[int], degree_bound: int, p: int, ambient_degree: int
) -> int:
    fixed = tuple((value[index] if index < len(value) else 0) % p for index in range(ambient_degree + 1))
    return omega_cached(p, degree_bound, ambient_degree, fixed)


@lru_cache(maxsize=None)
def roots_of_additive_character(p: int) -> tuple[complex, ...]:
    return tuple(cmath.exp(2j * math.pi * value / p) for value in range(p))


def cyc_zero(p: int) -> tuple[int, ...]:
    return (0,) * p


def cyc_monomial(p: int, exponent: int, coefficient: int = 1) -> tuple[int, ...]:
    result = [0] * p
    result[exponent % p] = coefficient
    return tuple(result)


def cyc_add(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def cyc_scale(value: Sequence[int], coefficient: int) -> tuple[int, ...]:
    return tuple(coefficient * item for item in value)


def cyc_shift(value: Sequence[int], exponent: int) -> tuple[int, ...]:
    p = len(value)
    result = [0] * p
    for index, coefficient in enumerate(value):
        result[(index + exponent) % p] += coefficient
    return tuple(result)


def cyc_mul(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    p = len(left)
    result = [0] * p
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[(i + j) % p] += a * b
    return tuple(result)


def cyc_pow(value: Sequence[int], exponent: int) -> tuple[int, ...]:
    result = cyc_monomial(len(value), 0)
    base = tuple(value)
    power = exponent
    while power:
        if power & 1:
            result = cyc_mul(result, base)
        base = cyc_mul(base, base)
        power >>= 1
    return result


def cyc_canonical(value: Sequence[int]) -> tuple[int, ...]:
    """Canonical coordinates in Z[zeta_p] using Phi_p=1+...+X^(p-1)."""
    anchor = value[-1]
    return tuple(item - anchor for item in value[:-1])


def cyc_equal(left: Sequence[int], right: Sequence[int]) -> bool:
    return cyc_canonical(left) == cyc_canonical(right)


def cyc_complex(value: Sequence[int]) -> complex:
    roots = roots_of_additive_character(len(value))
    return sum(coefficient * roots[index] for index, coefficient in enumerate(value))


def gauss_cyclotomic(p: int) -> tuple[int, ...]:
    result = cyc_zero(p)
    for value in range(p):
        result = cyc_add(result, cyc_monomial(p, value * value))
    return result


@lru_cache(maxsize=None)
def nonsingular_hankels(
    p: int, c: int
) -> tuple[tuple[tuple[int, ...], int, tuple[tuple[int, ...], ...]], ...]:
    result = []
    for b in vectors(p, 2 * c - 1):
        matrix = hankel(b, c)
        determinant = matrix_det(matrix, p)
        if determinant:
            result.append((tuple(b), determinant, matrix_inverse(matrix, p)))
    return tuple(result)


def twisted_transform_direct(p: int, c: int, z: Sequence[int], P: Sequence[int]) -> complex:
    roots = roots_of_additive_character(p)
    total = 0j
    for b, determinant, inverse in nonsingular_hankels(p, c):
        phase = (dot(P, b, p) - quadratic_form(z, inverse, p)) % p
        total += legendre(determinant, p) * roots[phase]
    return total


def twisted_transform_direct_cyclotomic(
    p: int, c: int, z: Sequence[int], P: Sequence[int]
) -> tuple[int, ...]:
    total = cyc_zero(p)
    for b, determinant, inverse in nonsingular_hankels(p, c):
        phase = (dot(P, b, p) - quadratic_form(z, inverse, p)) % p
        total = cyc_add(total, cyc_monomial(p, phase, legendre(determinant, p)))
    return total


def twisted_transform_formula(p: int, c: int, z: Sequence[int], P: Sequence[int]) -> complex:
    roots = roots_of_additive_character(p)
    gauss = sum(roots[(value * value) % p] for value in range(p))
    total = 0j
    dimension = 2 * c - 1
    P_tuple = tuple(value % p for value in P)
    for x in vectors(p, c):
        square = square_coefficients(x, p)
        y = fixed_add(P_tuple, square, dimension, p)
        indicator = int(not trim(y, p))
        bracket = p**dimension * indicator - p ** (c - 1) * (
            omega(y, c - 1, p, dimension - 1)
            - omega(y, c - 2, p, dimension - 1)
        )
        total += roots[(2 * dot(z, x, p)) % p] * bracket
    return total / (gauss**c)


def twisted_transform_numerator_cyclotomic(
    p: int, c: int, z: Sequence[int], P: Sequence[int]
) -> tuple[int, ...]:
    total = cyc_zero(p)
    dimension = 2 * c - 1
    P_tuple = tuple(value % p for value in P)
    for x in vectors(p, c):
        square = square_coefficients(x, p)
        y = fixed_add(P_tuple, square, dimension, p)
        indicator = int(not trim(y, p))
        bracket = p**dimension * indicator - p ** (c - 1) * (
            omega(y, c - 1, p, dimension - 1)
            - omega(y, c - 2, p, dimension - 1)
        )
        total = cyc_add(total, cyc_monomial(p, 2 * dot(z, x, p), bracket))
    return total


def check_twisted_case(
    p: int, c: int, pairs: Sequence[tuple[tuple[int, ...], tuple[int, ...]]]
) -> dict[str, Any]:
    maximum_error = 0.0
    exact_mismatch_count = 0
    gauss_power = cyc_pow(gauss_cyclotomic(p), c)
    for z, P in pairs:
        direct_exact = twisted_transform_direct_cyclotomic(p, c, z, P)
        numerator_exact = twisted_transform_numerator_cyclotomic(p, c, z, P)
        scaled_direct = cyc_mul(gauss_power, direct_exact)
        if not cyc_equal(scaled_direct, numerator_exact):
            exact_mismatch_count += 1
            raise AssertionError(
                (p, c, z, P, cyc_canonical(scaled_direct), cyc_canonical(numerator_exact))
            )
        direct = cyc_complex(direct_exact)
        formula = twisted_transform_formula(p, c, z, P)
        error = abs(direct - formula)
        maximum_error = max(maximum_error, error)
        if error > TOL * max(1.0, abs(direct), abs(formula)):
            raise AssertionError((p, c, z, P, direct, formula, error))
    return {
        "p": p,
        "c": c,
        "pair_count": len(pairs),
        "nonsingular_hankel_count": len(nonsingular_hankels(p, c)),
        "arithmetic": "exact cyclotomic coefficient comparison modulo Phi_p",
        "exact_mismatch_count": exact_mismatch_count,
        "max_error": maximum_error,
        "pass": True,
    }


def divisor_difference(p: int, k: int, P: Sequence[int], x: Sequence[int]) -> int:
    ambient_degree = 2 * k
    y = fixed_add(P, square_coefficients(x, p), ambient_degree + 1, p)
    return omega(y, k, p, ambient_degree) - omega(y, k - 1, p, ambient_degree)


def polar_condition_degree_k(z: Sequence[int], Q: Sequence[int], p: int) -> bool:
    return dot(z, tuple(Q) + (0,) * (len(z) - len(Q)), p) == 0


def polar_condition_degree_k_minus_one(z: Sequence[int], Q: Sequence[int], p: int) -> bool:
    padded = tuple(Q) + (0,) * (len(z) - len(Q))
    shifted = (0,) + tuple(Q) + (0,) * max(0, len(z) - len(Q) - 1)
    return dot(z, padded[: len(z)], p) == 0 and dot(z, shifted[: len(z)], p) == 0


def polar_original(p: int, k: int, z: Sequence[int], P: Sequence[int]) -> tuple[int, ...]:
    total = cyc_zero(p)
    for x in vectors(p, k + 1):
        total = cyc_add(
            total,
            cyc_monomial(p, 2 * dot(z, x, p), divisor_difference(p, k, P, x)),
        )
    return total


def polar_filtered(p: int, k: int, z: Sequence[int], P: Sequence[int]) -> tuple[int, ...]:
    total = cyc_zero(p)
    for Q in projective_polynomials(p, k):
        if not polar_condition_degree_k(z, Q, p):
            continue
        for x in vectors(p, k + 1):
            if homogeneous_divides(
                Q,
                k,
                fixed_add(P, square_coefficients(x, p), 2 * k + 1, p),
                2 * k,
                p,
            ):
                total = cyc_add(total, cyc_monomial(p, 2 * dot(z, x, p)))
    for Q in projective_polynomials(p, k - 1):
        if not polar_condition_degree_k_minus_one(z, Q, p):
            continue
        for x in vectors(p, k + 1):
            if homogeneous_divides(
                Q,
                k - 1,
                fixed_add(P, square_coefficients(x, p), 2 * k + 1, p),
                2 * k,
                p,
            ):
                total = cyc_add(total, cyc_monomial(p, 2 * dot(z, x, p), -1))
    return total


def endpoint_descended(
    p: int, k: int, beta: int, P: Sequence[int]
) -> tuple[int, ...]:
    total = cyc_zero(p)
    for x in vectors(p, k + 1):
        y = fixed_add(P, square_coefficients(x, p), 2 * k + 1, p)
        constant = y[0] if y else 0
        if constant % p:
            continue
        quotient = tuple(y[1:])
        bracket = omega(quotient, k - 1, p, 2 * k - 1) - omega(
            quotient, k - 2, p, 2 * k - 1
        )
        total = cyc_add(total, cyc_monomial(p, 2 * beta * x[0], bracket))
    return total


def check_polar_cases(rng: random.Random) -> dict[str, Any]:
    p = 3
    k = 2
    maximum_filter_error = 0.0
    maximum_endpoint_error = 0.0
    for _ in range(24):
        P = tuple(rng.randrange(p) for _ in range(2 * k + 1))
        z = tuple(rng.randrange(p) for _ in range(k + 1))
        original = polar_original(p, k, z, P)
        filtered = polar_filtered(p, k, z, P)
        filter_error = abs(cyc_complex(original) - cyc_complex(filtered))
        maximum_filter_error = max(maximum_filter_error, filter_error)
        if not cyc_equal(original, filtered):
            raise AssertionError(("polar", P, z, original, filtered))
        for beta in (1, 2):
            endpoint = (beta, 0, 0)
            original_endpoint = polar_original(p, k, endpoint, P)
            descended = endpoint_descended(p, k, beta, P)
            endpoint_error = abs(cyc_complex(original_endpoint) - cyc_complex(descended))
            maximum_endpoint_error = max(maximum_endpoint_error, endpoint_error)
            if not cyc_equal(original_endpoint, descended):
                raise AssertionError(("endpoint", P, beta, original_endpoint, descended))
    return {
        "p": p,
        "k": k,
        "sample_count": 24,
        "arithmetic": "exact cyclotomic coefficient comparison modulo Phi_p",
        "exact_filter_mismatch_count": 0,
        "exact_endpoint_mismatch_count": 0,
        "max_polar_filter_error": maximum_filter_error,
        "max_endpoint_descent_error": maximum_endpoint_error,
        "pass": True,
    }


def check_divisor_toy(p: int, n: int, c: int) -> dict[str, Any]:
    h = n // 2
    m = h - c
    w = c - 1
    H = roots_of_unity(p, n)
    zero_count = 0
    checked = 0
    x_n_minus_one = tuple([(-1) % p] + [0] * (n - 1) + [1])
    for subset in itertools.combinations(H, m):
        checked += 1
        complement = tuple(point for point in H if point not in set(subset))
        Q = locator(subset, p)
        R = locator(complement, p)
        moments_zero = all(
            sum(pow(point, degree, p) for point in subset) % p == 0
            for degree in range(1, w + 1)
        )
        q_gap = all(Q[m - degree] % p == 0 for degree in range(1, w + 1))
        if moments_zero != q_gap:
            raise AssertionError("Newton gap equivalence failed")
        if not moments_zero:
            continue
        zero_count += 1
        if not all(R[n - m - degree] % p == 0 for degree in range(1, w + 1)):
            raise AssertionError("complement gap failed")
        if poly_mul(Q, R, p) != x_n_minus_one:
            raise AssertionError("complement product failed")

        D_Q = poly_sub(poly_shift(poly_derivative(Q, p), 1, p), poly_scale(Q, m, p), p)
        D_R = poly_sub(
            poly_shift(poly_derivative(R, p), 1, p), poly_scale(R, n - m, p), p
        )
        bezout = poly_add(poly_mul(D_Q, R, p), poly_mul(Q, D_R, p), p)
        if bezout != (n % p,):
            raise AssertionError(("Bezout", subset, bezout))
        inv_n = pow(n, -1, p)
        f = poly_scale(poly_mul(D_Q, R, p), inv_n, p)
        for point in H:
            expected = int(point in subset)
            if poly_eval(f, point, p) != expected:
                raise AssertionError("interpolation formula failed")

        x_m = tuple([0] * m + [1])
        u = poly_sub(x_m, Q, p)
        s = poly_shift(u, c, p)
        s_squared_minus_one = poly_sub(poly_mul(s, s, p), (1,), p)
        if not divides(Q, s_squared_minus_one, p):
            raise AssertionError("dyadic divisor relation failed")
        q_plus = poly_gcd(Q, poly_sub(s, (1,), p), p)
        q_minus = poly_gcd(Q, poly_add(s, (1,), p), p)
        if poly_mul(q_plus, q_minus, p) != Q:
            raise AssertionError("dyadic factor split failed")

    return {
        "p": p,
        "n": n,
        "c": c,
        "w": w,
        "m": m,
        "subset_count": checked,
        "zero_fiber_count": zero_count,
        "pass": True,
    }


def check_uniform_fourier() -> dict[str, Any]:
    p = 7
    n = 6
    m = 2
    w = 1
    c = 2
    H = roots_of_unity(p, n)
    direct = [0] * p
    for subset in itertools.combinations(H, m):
        direct[sum(subset) % p] += 1
    transformed = []
    maximum_error = 0.0
    line_values = []
    expected_line_exact = cyc_monomial(p, 0, math.comb(n, m) * p)
    for v in range(p):
        total = cyc_zero(p)
        line = cyc_zero(p)
        for u0 in range(p):
            for u1 in range(p):
                product = cyc_monomial(p, 0)
                for point in H:
                    factor = cyc_add(
                        cyc_monomial(p, 0),
                        cyc_monomial(p, u0 + u1 * point),
                    )
                    product = cyc_mul(product, factor)
                term = cyc_shift(product, -m * u0 - u1 * v)
                total = cyc_add(total, term)
                if u1 == 0:
                    line = cyc_add(line, term)
        expected = cyc_monomial(p, 0, direct[v] * p**c)
        if not cyc_equal(total, expected):
            raise AssertionError(("exact Fourier", v, cyc_canonical(total), cyc_canonical(expected)))
        if not cyc_equal(line, expected_line_exact):
            raise AssertionError(("exact mean line", v, cyc_canonical(line)))
        value = cyc_complex(total) / (p**c)
        line_value = cyc_complex(line) / (p**c)
        transformed.append(value.real)
        line_values.append(line_value.real)
        maximum_error = max(maximum_error, abs(value - direct[v]))
        if abs(value - direct[v]) > TOL:
            raise AssertionError((v, value, direct[v]))
    mean = math.comb(n, m) / (p**w)
    if max(abs(value - mean) for value in line_values) > TOL:
        raise AssertionError("mean-line identity failed")
    return {
        "p": p,
        "n": n,
        "m": m,
        "w": w,
        "direct_counts": direct,
        "fourier_counts": transformed,
        "mean_line": mean,
        "arithmetic": "exact cyclotomic coefficient comparison modulo Phi_p",
        "exact_mismatch_count": 0,
        "max_error": maximum_error,
        "pass": True,
    }


def check_oa_route_cut() -> dict[str, Any]:
    p = 7
    n = 6
    c = 2
    d = n - c
    m = 2
    direct_max = max(check_uniform_fourier()["direct_counts"])
    rows = []
    for r, s in ((1, 0), (0, 1), (1, 1), (2, 1)):
        t = r + s
        right = p ** (d - t) * math.comb(n, t) * math.comb(t, r)
        left = direct_max * math.comb(m, r) * math.comb(n - m, s)
        if left > right:
            raise AssertionError("OA factorial-moment inequality failed")
        rows.append({"r": r, "s": s, "left": left, "right": right})
    return {"p": p, "n": n, "c": c, "direct_max": direct_max, "rows": rows, "pass": True}


def note_contract(root: Path) -> dict[str, bool]:
    note = (root / NOTE).read_text(encoding="utf-8")
    prior = (root / PRIOR).read_text(encoding="utf-8")
    checks = {
        "proved_transform_status": "TWISTED NONSINGULAR HANKEL TRANSFORM: PROVED" in note,
        "full_rank_bridge_proved": "FULL-RANK CHG NORMALIZATION BRIDGE: PROVED" in note,
        "endpoint_bridge_proved": "FULL-RANK DEPLOYED ZERO-FIBER ENDPOINT IDENTIFICATION: PROVED" in note,
        "chg_open": "FULL CHG RANK-STRATUM ESTIMATE / LS / N(0) <= n^3: OPEN" in note,
        "no_n0_claim": "does **not** prove" in note and "N(0) <= n^3" in note,
        "nonsingular_scope": "nonsingular/full-rank ordinary" in note,
        "fourier_convention": "unnormalized plus-sign Fourier transform" in note,
        "omega_normalization": "Divisors are homogeneous and projective" in note,
        "elkies_specialization": "Elkies Theorem 1 specialization" in note
        and "D=2c-2" in note
        and "m=c-1" in note,
        "exact_cyclotomic_guard": "exact cyclotomic arithmetic" in note
        and "Phi_p(X)=1+X+...+X^(p-1)" in note,
        "proof_code_map": "Proof-to-code correspondence" in note,
        "toy_census_scoped": "CHG-linked toy cancellation census" in note
        and "does not identify" in note,
        "endpoint_application": "companion normalization note" in note
        and "z_Z(0)" in note,
        "kopparty_claim_removed": "does not invoke a\nKopparty--Wang" in note,
        "prior_note_updated": "TWISTED NONSINGULAR TRANSFORM NOW AVAILABLE" in prior
        and "zero-fiber endpoint identification" in prior
        and "signed Hankel--Salie" in prior,
    }
    if not all(checks.values()):
        raise AssertionError({key: value for key, value in checks.items() if not value})
    return checks


def deployed_parameters() -> dict[str, Any]:
    n = 2**21
    w = 67471
    c = w + 1
    h = n // 2
    m = 981104
    checks = {
        "m_equals_h_minus_c": m == h - c,
        "n_minus_m_equals_h_plus_c": n - m == h + c,
        "n_equals_2m_plus_2c": n == 2 * m + 2 * c,
        "r_star_equals_2m": n - 2 * w - 2 == 2 * m,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {"n": n, "w": w, "c": c, "h": h, "m": m, "checks": checks}


def build_payload(root: Path) -> dict[str, Any]:
    rng = random.Random(SEED)
    exhaustive_pairs = [
        (tuple(z), tuple(P)) for z in vectors(3, 2) for P in vectors(3, 3)
    ]
    p5_all = [(tuple(z), tuple(P)) for z in vectors(5, 2) for P in vectors(5, 3)]
    p3_c3_all = [(tuple(z), tuple(P)) for z in vectors(3, 3) for P in vectors(3, 5)]
    p5_pairs = rng.sample(p5_all, 200)
    p3_c3_pairs = rng.sample(p3_c3_all, 200)

    payload: dict[str, Any] = {
        "theorem_id": THEOREM_ID,
        "status": STATUS,
        "seed": SEED,
        "source_base_commit": "36de5bfc",
        "deployed_parameters": deployed_parameters(),
        "divisor_toys": [check_divisor_toy(17, 16, 2), check_divisor_toy(17, 16, 3)],
        "uniform_fourier": check_uniform_fourier(),
        "twisted_hankel_cases": [
            check_twisted_case(3, 2, exhaustive_pairs),
            check_twisted_case(5, 2, p5_pairs),
            check_twisted_case(3, 3, p3_c3_pairs),
        ],
        "polar_endpoint": check_polar_cases(rng),
        "oa_route_cut": check_oa_route_cut(),
        "note_contract": note_contract(root),
        "claims": [
            "exact zero-fiber complementary divisor gaps and Bezout certificate",
            "exact uniform subset-Fourier identity",
            "exact nonsingular twisted Hankel transform",
            "exact abstract polar filtering and endpoint descent",
        ],
        "nonclaims": [
            "N(0) <= n^3",
            "max_v N(v) <= n^3",
            "CHG rank-stratum estimate",
            "lower-rank pseudodeterminant transform",
            "deployed zero-fiber endpoint-twist identification",
            "LS or SV* closure",
        ],
    }
    payload = normalize(payload)
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def validate_payload(actual: dict[str, Any], expected: dict[str, Any]) -> None:
    if actual.get("payload_sha256") != payload_hash(actual):
        raise AssertionError("certificate payload hash mismatch")
    if normalize(actual) != normalize(expected):
        raise AssertionError("certificate does not match recomputed payload")


def write_payload(root: Path, payload: dict[str, Any]) -> None:
    path = root / CERT
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tamper_selftest(root: Path, expected: dict[str, Any]) -> int:
    source = json.loads((root / CERT).read_text(encoding="utf-8"))
    mutations = []

    changed = copy.deepcopy(source)
    changed["status"] = "PROVED N(0) <= n^3"
    mutations.append(changed)

    changed = copy.deepcopy(source)
    changed["twisted_hankel_cases"][0]["max_error"] = 1.0
    mutations.append(changed)

    changed = copy.deepcopy(source)
    changed["note_contract"]["endpoint_bridge_proved"] = False
    mutations.append(changed)

    changed = copy.deepcopy(source)
    changed["nonclaims"].remove("N(0) <= n^3")
    mutations.append(changed)

    changed = copy.deepcopy(source)
    changed["payload_sha256"] = "0" * 64
    mutations.append(changed)

    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        for index, mutation in enumerate(mutations):
            path = Path(directory) / f"tampered_{index}.json"
            path.write_text(json.dumps(mutation), encoding="utf-8")
            loaded = json.loads(path.read_text(encoding="utf-8"))
            try:
                validate_payload(loaded, expected)
            except AssertionError:
                rejected += 1
    if rejected != len(mutations):
        raise AssertionError("tamper self-test failed")
    return rejected


def print_summary(payload: dict[str, Any]) -> None:
    print(f"theorem_id: {payload['theorem_id']}")
    print(f"status: {payload['status']}")
    print(f"seed: {payload['seed']}")
    for row in payload["twisted_hankel_cases"]:
        print(
            "twisted_hankel: "
            f"p={row['p']} c={row['c']} pairs={row['pair_count']} "
            f"max_error={row['max_error']:.3e} PASS"
        )
    polar = payload["polar_endpoint"]
    print(
        "polar_endpoint: "
        f"filter_error={polar['max_polar_filter_error']:.3e} "
        f"descent_error={polar['max_endpoint_descent_error']:.3e} PASS"
    )
    print("result: PASS")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="regenerate the JSON certificate")
    parser.add_argument("--check", action="store_true", help="recompute and check the certificate")
    parser.add_argument(
        "--tamper-selftest", action="store_true", help="verify that certificate mutations are rejected"
    )
    args = parser.parse_args()
    if not (args.write or args.check or args.tamper_selftest):
        args.check = True

    root = repo_root()
    expected = build_payload(root)
    if args.write:
        write_payload(root, expected)
        print(f"wrote: {CERT.as_posix()}")
    if args.check:
        actual = json.loads((root / CERT).read_text(encoding="utf-8"))
        validate_payload(actual, expected)
    if args.tamper_selftest:
        rejected = tamper_selftest(root, expected)
        print(f"tamper_mutations_rejected: {rejected}")
    print_summary(expected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
