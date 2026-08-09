#!/usr/bin/env python3
"""Compute the complete cell-11 signed-pair resultant in the exact tower."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

import sympy as sp
from flint import fmpz_mod_poly_ctx

from verify_kb_mca_v4_433_1b_cell11_compact_tower_v1 import (
    CERTIFICATE as TOWER_CERTIFICATE,
    verify as verify_tower_certificate,
)


P = 2_130_706_433
POLY_CTX = fmpz_mod_poly_ctx(P)
POLY_TYPE = type(POLY_CTX.zero())


class RF:
    """Canonical rational function in r over F_p."""

    __slots__ = ("numer", "denom")

    def __init__(self, numer=0, denom=1):
        if isinstance(numer, RF):
            if denom != 1:
                raise TypeError("second denominator supplied")
            self.numer, self.denom = numer.numer, numer.denom
            return
        numer = numer if isinstance(numer, POLY_TYPE) else POLY_CTX([int(numer) % P])
        denom = denom if isinstance(denom, POLY_TYPE) else POLY_CTX([int(denom) % P])
        if denom.is_zero():
            raise ZeroDivisionError("zero rational-function denominator")
        if numer.is_zero():
            self.numer, self.denom = POLY_CTX.zero(), POLY_CTX.one()
            return
        common = numer.gcd(denom)
        numer //= common
        denom //= common
        scale = pow(int(denom[denom.degree()]), -1, P)
        self.numer, self.denom = numer * scale, denom * scale

    @staticmethod
    def coerce(value):
        if isinstance(value, RF):
            return value
        if isinstance(value, (int, POLY_TYPE)):
            return RF(value)
        return NotImplemented

    def __add__(self, other):
        other = RF.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        common = self.denom.gcd(other.denom)
        left = self.denom // common
        right = other.denom // common
        return RF(self.numer * right + other.numer * left, left * other.denom)

    __radd__ = __add__

    def __neg__(self):
        return RF(-self.numer, self.denom)

    def __sub__(self, other):
        other = RF.coerce(other)
        return NotImplemented if other is NotImplemented else self + (-other)

    def __rsub__(self, other):
        other = RF.coerce(other)
        return NotImplemented if other is NotImplemented else other - self

    def __mul__(self, other):
        other = RF.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        left_common = self.numer.gcd(other.denom)
        right_common = other.numer.gcd(self.denom)
        return RF(
            (self.numer // left_common) * (other.numer // right_common),
            (self.denom // right_common) * (other.denom // left_common),
        )

    __rmul__ = __mul__

    def inverse(self):
        if self.numer.is_zero():
            raise ZeroDivisionError("inverse of zero")
        return RF(self.denom, self.numer)

    def __truediv__(self, other):
        other = RF.coerce(other)
        return NotImplemented if other is NotImplemented else self * other.inverse()

    def __rtruediv__(self, other):
        other = RF.coerce(other)
        return NotImplemented if other is NotImplemented else other / self

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result, base, power = RF(1), self, exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result

    def __eq__(self, other):
        other = RF.coerce(other)
        return other is not NotImplemented and self.numer == other.numer and self.denom == other.denom

    def is_zero(self):
        return self.numer.is_zero()

    def record(self):
        return {
            "numerator": self.numer.str(),
            "denominator": self.denom.str(),
            "numerator_degree": -1 if self.numer.is_zero() else int(self.numer.degree()),
            "denominator_degree": int(self.denom.degree()),
        }

    def specialize(self, r_value):
        denominator = int(self.denom(r_value)) % P
        if denominator == 0:
            raise ZeroDivisionError("RF specialization denominator")
        return int(self.numer(r_value)) * pow(denominator, -1, P) % P


T_U = None
T_V = None
B_U = None
B_V = None


class TQuad:
    """Element a0+a1*t with t^2=T_U*t+T_V."""

    __slots__ = ("constant", "linear")

    def __init__(self, constant=0, linear=0):
        self.constant = RF(constant)
        self.linear = RF(linear)

    @staticmethod
    def coerce(value):
        if isinstance(value, TQuad):
            return value
        converted = RF.coerce(value)
        return NotImplemented if converted is NotImplemented else TQuad(converted)

    def __add__(self, other):
        other = TQuad.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return TQuad(self.constant + other.constant, self.linear + other.linear)

    __radd__ = __add__

    def __neg__(self):
        return TQuad(-self.constant, -self.linear)

    def __sub__(self, other):
        other = TQuad.coerce(other)
        return NotImplemented if other is NotImplemented else self + (-other)

    def __rsub__(self, other):
        other = TQuad.coerce(other)
        return NotImplemented if other is NotImplemented else other - self

    def __mul__(self, other):
        other = TQuad.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return TQuad(
            self.constant * other.constant + self.linear * other.linear * T_V,
            self.constant * other.linear + self.linear * other.constant
            + self.linear * other.linear * T_U,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent):
        if exponent < 0:
            raise ValueError("negative TQuad exponent")
        result, base, power = TQuad(1), self, exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result

    def inverse(self):
        norm = (
            self.constant * self.constant
            + self.constant * self.linear * T_U
            - self.linear * self.linear * T_V
        )
        return TQuad(
            (self.constant + self.linear * T_U) / norm,
            -self.linear / norm,
        )

    def __truediv__(self, other):
        other = TQuad.coerce(other)
        return NotImplemented if other is NotImplemented else self * other.inverse()

    def __eq__(self, other):
        other = TQuad.coerce(other)
        return (
            other is not NotImplemented
            and self.constant == other.constant and self.linear == other.linear
        )

    def is_zero(self):
        return self.constant.is_zero() and self.linear.is_zero()

    def divide_rf(self, denominator):
        denominator = RF(denominator)
        return TQuad(self.constant / denominator, self.linear / denominator)

    def record(self):
        return [self.constant.record(), self.linear.record()]

    def specialize(self, r_value, t_value):
        return (
            self.constant.specialize(r_value)
            + self.linear.specialize(r_value) * t_value
        ) % P


class BQuad:
    """Element A0+A1*b over TQuad with b^2=B_U*b+B_V."""

    __slots__ = ("constant", "linear")

    def __init__(self, constant=0, linear=0):
        self.constant = TQuad.coerce(constant)
        self.linear = TQuad.coerce(linear)
        if self.constant is NotImplemented or self.linear is NotImplemented:
            raise TypeError("cannot coerce BQuad coefficient")

    @staticmethod
    def coerce(value):
        if isinstance(value, BQuad):
            return value
        converted = TQuad.coerce(value)
        return NotImplemented if converted is NotImplemented else BQuad(converted)

    def __add__(self, other):
        other = BQuad.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return BQuad(self.constant + other.constant, self.linear + other.linear)

    __radd__ = __add__

    def __neg__(self):
        return BQuad(-self.constant, -self.linear)

    def __sub__(self, other):
        other = BQuad.coerce(other)
        return NotImplemented if other is NotImplemented else self + (-other)

    def __rsub__(self, other):
        other = BQuad.coerce(other)
        return NotImplemented if other is NotImplemented else other - self

    def __mul__(self, other):
        other = BQuad.coerce(other)
        if other is NotImplemented:
            return NotImplemented
        return BQuad(
            self.constant * other.constant + self.linear * other.linear * B_V,
            self.constant * other.linear + self.linear * other.constant
            + self.linear * other.linear * B_U,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent):
        if exponent < 0:
            raise ValueError("negative BQuad exponent")
        result, base, power = BQuad(1), self, exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result

    def inverse(self):
        norm = (
            self.constant * self.constant
            + self.constant * self.linear * B_U
            - self.linear * self.linear * B_V
        )
        return BQuad(
            (self.constant + self.linear * B_U) / norm,
            -self.linear / norm,
        )

    def __truediv__(self, other):
        other = BQuad.coerce(other)
        return NotImplemented if other is NotImplemented else self * other.inverse()

    def __eq__(self, other):
        other = BQuad.coerce(other)
        return (
            other is not NotImplemented
            and self.constant == other.constant and self.linear == other.linear
        )

    def is_zero(self):
        return self.constant.is_zero() and self.linear.is_zero()

    def divide_rf(self, denominator):
        return BQuad(
            self.constant.divide_rf(denominator), self.linear.divide_rf(denominator)
        )

    def record(self):
        return [self.constant.record(), self.linear.record()]

    def specialize(self, r_value, t_value, b_value):
        return (
            self.constant.specialize(r_value, t_value)
            + self.linear.specialize(r_value, t_value) * b_value
        ) % P


def sparse_poly(expression, variable):
    polynomial = sp.Poly(expression, variable, modulus=P)
    coefficients = {}
    for (degree,), coefficient in polynomial.terms():
        coefficients[degree] = int(coefficient) % P
    maximum = max(coefficients, default=0)
    return POLY_CTX([coefficients.get(index, 0) for index in range(maximum + 1)])


def rf_from_r(expression, r):
    return RF(sparse_poly(expression, r))


def eval_t(expression, t, r):
    polynomial = sp.Poly(expression, t, r, modulus=P)
    result = TQuad(0)
    r_element = RF(POLY_CTX([0, 1]))
    for (et, er), coefficient in polynomial.terms():
        result += (int(coefficient) % P) * (TQuad(0, 1) ** et) * (r_element ** er)
    return result


def eval_tower(expression, t, r, c, b, c_element):
    polynomial = sp.Poly(expression, t, r, c, b, modulus=P)
    result = BQuad(0)
    elements = (
        BQuad(TQuad(0, 1)),
        BQuad(RF(POLY_CTX([0, 1]))),
        c_element,
        BQuad(0, 1),
    )
    maxima = [max((term[0][index] for term in polynomial.terms()), default=0) for index in range(4)]
    powers = [[BQuad(1)] for _ in range(4)]
    for index, maximum in enumerate(maxima):
        for _ in range(maximum):
            powers[index].append(powers[index][-1] * elements[index])
    for exponents, coefficient in polynomial.terms():
        term = BQuad(int(coefficient) % P)
        for index, exponent in enumerate(exponents):
            term *= powers[index][exponent]
        result += term
    return result


def trim(poly):
    return {degree: value for degree, value in poly.items() if not value.is_zero()}


def poly_add(left, right):
    result = dict(left)
    for degree, value in right.items():
        result[degree] = result.get(degree, BQuad(0)) + value
    return trim(result)


def poly_neg(poly):
    return {degree: -value for degree, value in poly.items()}


def poly_sub(left, right):
    return poly_add(left, poly_neg(right))


def poly_mul(left, right):
    result = {}
    for left_degree, left_value in left.items():
        for right_degree, right_value in right.items():
            degree = left_degree + right_degree
            result[degree] = result.get(degree, BQuad(0)) + left_value * right_value
    return trim(result)


def poly_pow(poly, exponent):
    result, base, power = {0: BQuad(1)}, poly, exponent
    while power:
        if power & 1:
            result = poly_mul(result, base)
        base = poly_mul(base, base)
        power //= 2
    return result


def poly_scale(poly, scalar):
    scalar = BQuad.coerce(scalar)
    return trim({degree: value * scalar for degree, value in poly.items()})


def poly_eval(poly, value):
    result = BQuad(0)
    for degree in range(max(poly, default=-1), -1, -1):
        result = result * value + poly.get(degree, BQuad(0))
    return result


def poly_divmod(dividend, divisor):
    quotient = {}
    remainder = dict(dividend)
    divisor_degree = max(divisor)
    divisor_leading = divisor[divisor_degree]
    while remainder and max(remainder) >= divisor_degree:
        degree = max(remainder) - divisor_degree
        coefficient = remainder[max(remainder)] / divisor_leading
        quotient[degree] = coefficient
        remainder = poly_sub(remainder, poly_scale(
            {index + degree: value for index, value in divisor.items()},
            coefficient,
        ))
    return trim(quotient), trim(remainder)


def remove_factor(poly, factor):
    exponent = 0
    residual = poly
    while residual:
        quotient, remainder = poly_divmod(residual, factor)
        if remainder:
            break
        exponent += 1
        residual = quotient
    return exponent, residual


def outer_add(left, right):
    result = dict(left)
    for degree, value in right.items():
        result[degree] = poly_add(result.get(degree, {}), value)
    return {degree: value for degree, value in result.items() if value}


def outer_neg(poly):
    return {degree: poly_neg(value) for degree, value in poly.items()}


def outer_sub(left, right):
    return outer_add(left, outer_neg(right))


def outer_mul(left, right):
    result = {}
    for left_degree, left_value in left.items():
        for right_degree, right_value in right.items():
            degree = left_degree + right_degree
            result[degree] = poly_add(
                result.get(degree, {}), poly_mul(left_value, right_value)
            )
    return {degree: value for degree, value in result.items() if value}


def outer_pow(poly, exponent):
    result, base, power = {0: {0: BQuad(1)}}, poly, exponent
    while power:
        if power & 1:
            result = outer_mul(result, base)
        base = outer_mul(base, base)
        power //= 2
    return result


def outer_constant(poly_w0):
    return {0: poly_w0}


def outer_bquad(value):
    return {0: {0: BQuad.coerce(value)}}


def determinant(matrix):
    size = len(matrix)
    dp = {0: {0: BQuad(1)}}
    for row in range(size):
        next_dp = {}
        for mask, value in dp.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                inversions = sum(1 for old in range(column + 1, size) if mask & (1 << old))
                term = poly_mul(value, matrix[row][column])
                if inversions & 1:
                    term = poly_neg(term)
                new_mask = mask | (1 << column)
                next_dp[new_mask] = poly_add(next_dp.get(new_mask, {}), term)
        dp = next_dp
    return dp[(1 << size) - 1]


def resultant_w1(left, right):
    left_degree, right_degree = max(left), max(right)
    left_desc = [left.get(index, {}) for index in range(left_degree, -1, -1)]
    right_desc = [right.get(index, {}) for index in range(right_degree, -1, -1)]
    size = left_degree + right_degree
    zero = {}
    matrix = []
    for shift in range(right_degree):
        matrix.append([zero] * shift + left_desc + [zero] * (right_degree - 1 - shift))
    for shift in range(left_degree):
        matrix.append([zero] * shift + right_desc + [zero] * (left_degree - 1 - shift))
    if any(len(row) != size for row in matrix):
        raise RuntimeError("invalid Sylvester matrix")
    return determinant(matrix)


def canonical_hash(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def element_record(value):
    record = value.record()
    return {"sha256": canonical_hash(record), "coordinates": record}


def element_profile(value):
    record = element_record(value)
    numerator_degrees = []
    denominator_degrees = []
    for t_coordinate in value.record():
        for rf_coordinate in t_coordinate:
            numerator_degrees.append(rf_coordinate["numerator_degree"])
            denominator_degrees.append(rf_coordinate["denominator_degree"])
    return {
        "sha256": record["sha256"],
        "max_r_numerator_degree": max(numerator_degrees, default=-1),
        "max_r_denominator_degree": max(denominator_degrees, default=-1),
    }


def norm_tquad(value):
    return (
        value.constant * value.constant
        + value.constant * value.linear * T_U
        - value.linear * value.linear * T_V
    )


def norm_bquad(value):
    return norm_tquad(
        value.constant * value.constant
        + value.constant * value.linear * B_U
        - value.linear * value.linear * B_V
    )


def sqrt_rf(value):
    numerator_scalar, numerator_factors = value.numer.factor()
    denominator_scalar, denominator_factors = value.denom.factor()
    rows = [*numerator_factors, *denominator_factors]
    if any(int(multiplicity) % 2 for _, multiplicity in rows):
        return None
    scalar = int(numerator_scalar) * pow(int(denominator_scalar), -1, P) % P
    scalar_root = sp.sqrt_mod(scalar, P, all_roots=False)
    if scalar_root is None:
        return None
    numerator_root = POLY_CTX([int(scalar_root)])
    denominator_root = POLY_CTX.one()
    for factor, multiplicity in numerator_factors:
        numerator_root *= factor ** (int(multiplicity) // 2)
    for factor, multiplicity in denominator_factors:
        denominator_root *= factor ** (int(multiplicity) // 2)
    result = RF(numerator_root, denominator_root)
    if result * result != value:
        raise RuntimeError("RF square-root reconstruction failed")
    return result


def sqrt_tquad(value):
    norm_root = sqrt_rf(norm_tquad(value))
    if norm_root is None:
        return None
    trace = RF(2) * value.constant + value.linear * T_U
    for signed_norm in (norm_root, -norm_root):
        trace_root = sqrt_rf(trace + RF(2) * signed_norm)
        if trace_root is None or trace_root.is_zero():
            continue
        linear = value.linear / trace_root
        constant = (trace_root - linear * T_U) / RF(2)
        candidate = TQuad(constant, linear)
        if candidate * candidate == value:
            return candidate
    if value.linear.is_zero():
        constant = sqrt_rf(value.constant)
        if constant is not None:
            return TQuad(constant)
        shifted_square = T_V + T_U * T_U / RF(4)
        linear = sqrt_rf(value.constant / shifted_square)
        if linear is not None:
            candidate = TQuad(-linear * T_U / RF(2), linear)
            if candidate * candidate == value:
                return candidate
    return None


def sqrt_bquad(value):
    norm_root = sqrt_tquad(
        value.constant * value.constant
        + value.constant * value.linear * B_U
        - value.linear * value.linear * B_V
    )
    if norm_root is None:
        return None
    trace = TQuad(2) * value.constant + value.linear * B_U
    for signed_norm in (norm_root, -norm_root):
        trace_root = sqrt_tquad(trace + TQuad(2) * signed_norm)
        if trace_root is None or trace_root.is_zero():
            continue
        linear = value.linear / trace_root
        constant = (trace_root - linear * B_U) / TQuad(2)
        candidate = BQuad(constant, linear)
        if candidate * candidate == value:
            return candidate
    if value.linear.is_zero():
        constant = sqrt_tquad(value.constant)
        if constant is not None:
            return BQuad(constant)
        shifted_square = B_V + B_U * B_U / TQuad(4)
        linear = sqrt_tquad(value.constant / shifted_square)
        if linear is not None:
            candidate = BQuad(-linear * B_U / TQuad(2), linear)
            if candidate * candidate == value:
                return candidate
    return None


def factor_record(polynomial):
    scalar, factors = polynomial.factor()
    return {
        "scalar": int(scalar),
        "factors": [
            {
                "polynomial": factor.str(),
                "degree": int(factor.degree()),
                "multiplicity": int(multiplicity),
            }
            for factor, multiplicity in factors
        ],
    }


def quadratic_roots(a, b, c):
    a, b, c = a % P, b % P, c % P
    if a == 0:
        return [] if b == 0 else [(-c * pow(b, -1, P)) % P]
    discriminant = (b * b - 4 * a * c) % P
    roots = sp.sqrt_mod(discriminant, P, all_roots=True)
    inverse = pow(2 * a % P, -1, P)
    return sorted({((-b + int(root)) * inverse) % P for root in roots})


def specialize_poly(poly, r_value, t_value, b_value):
    return {
        degree: value.specialize(r_value, t_value, b_value)
        for degree, value in poly.items()
    }


def evaluate_fp_poly(poly, value):
    result = 0
    for degree in range(max(poly, default=-1), -1, -1):
        result = (result * value + poly.get(degree, 0)) % P
    return result


def outer_specialize(poly, w0_value, r_value, t_value, b_value):
    output = {}
    for w1_degree, w0_poly in poly.items():
        coefficient = poly_eval(w0_poly, BQuad(w0_value))
        output[w1_degree] = coefficient.specialize(r_value, t_value, b_value)
    return {degree: value for degree, value in output.items() if value}


def polynomial_record(poly):
    degrees = sorted(poly)
    rows = {str(degree): element_record(poly[degree]) for degree in degrees}
    numerator_degrees = []
    denominator_degrees = []
    for value in poly.values():
        for t_coordinate in (value.constant, value.linear):
            for rf_coordinate in (t_coordinate.constant, t_coordinate.linear):
                numerator_degrees.append(-1 if rf_coordinate.numer.is_zero() else int(rf_coordinate.numer.degree()))
                denominator_degrees.append(int(rf_coordinate.denom.degree()))
    return {
        "degree": max(degrees, default=-1),
        "nonzero_coefficients": len(degrees),
        "max_r_numerator_degree": max(numerator_degrees, default=-1),
        "max_r_denominator_degree": max(denominator_degrees, default=-1),
        "sha256": canonical_hash(rows),
        "coefficients": rows,
    }


def polynomial_profile(poly):
    record = polynomial_record(poly)
    record.pop("coefficients")
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--scan-r-values", type=int, default=256)
    parser.add_argument("--seed", type=int, default=43311)
    arguments = parser.parse_args()

    tower_bytes = TOWER_CERTIFICATE.read_bytes()
    tower_payload = json.loads(tower_bytes)
    verify_tower_certificate(tower_payload)
    raw = tower_payload["exact_replay"]
    selected = next(row for row in raw["charts"] if row["c_row"] == 5)
    t, r, c, b = sp.symbols("t r c b")
    base = sp.sympify(selected["base"]["expression"])
    b_relation = sp.sympify(selected["b_relation"]["expression"])
    c_relation = sp.sympify(selected["c_relation"]["expression"])

    global T_U, T_V, B_U, B_V
    base_coefficients = sp.Poly(base, t).all_coeffs()
    if len(base_coefficients) != 3:
        raise RuntimeError("base relation is not quadratic in t")
    base_leading, base_linear, base_constant = (rf_from_r(value, r) for value in base_coefficients)
    T_U, T_V = -base_linear / base_leading, -base_constant / base_leading

    b_coefficients = sp.Poly(b_relation, b).all_coeffs()
    if len(b_coefficients) != 3:
        raise RuntimeError("b relation is not quadratic in b")
    b_leading = rf_from_r(b_coefficients[0], r)
    B_U = (-eval_t(b_coefficients[1], t, r)).divide_rf(b_leading)
    B_V = (-eval_t(b_coefficients[2], t, r)).divide_rf(b_leading)

    c_coefficients = sp.Poly(c_relation, c).all_coeffs()
    if len(c_coefficients) != 2:
        raise RuntimeError("c relation is not linear in c")
    c_leading = rf_from_r(c_coefficients[0], r)
    c_constant = eval_tower(c_coefficients[1], t, r, c, b, BQuad(0))
    c_element = (-c_constant).divide_rf(c_leading)

    tower_checks = {
        "base": eval_tower(base, t, r, c, b, c_element).is_zero(),
        "b_relation": eval_tower(b_relation, t, r, c, b, c_element).is_zero(),
        "c_relation": eval_tower(c_relation, t, r, c, b, c_element).is_zero(),
    }
    if not all(tower_checks.values()):
        raise RuntimeError(f"tower substitution failed: {tower_checks}")

    kernel = [
        eval_tower(sp.sympify(row["expression"]), t, r, c, b, c_element)
        for row in raw["kernel"]["kernel"]
    ]
    if kernel[6] + kernel[7] != BQuad(0):
        raise RuntimeError("B1 opposition lost")
    a2 = kernel[:3]
    a0 = kernel[3:6]
    k = kernel[6]

    one_outer = outer_bquad(BQuad(1))
    w0_outer = {0: {1: BQuad(1)}}
    w1_outer = {1: {0: BQuad(1)}}

    def form(coefficients, variable):
        result = {}
        for index, coefficient in enumerate(coefficients):
            result = outer_add(result, outer_mul(outer_bquad(coefficient), outer_pow(variable, index)))
        return result

    d0, d1 = form(a2, w0_outer), form(a2, w1_outer)
    n0, n1 = form(a0, w0_outer), form(a0, w1_outer)
    raw_product = outer_add(outer_mul(n1, d0), outer_mul(n0, d1))
    raw_square = outer_sub(
        outer_sub(
            outer_mul(
                outer_mul(
                    outer_mul(outer_bquad(k * k), w0_outer),
                    outer_pow(outer_sub(one_outer, w0_outer), 2),
                ),
                outer_pow(d1, 2),
            ),
            outer_mul(
                outer_mul(
                    outer_mul(outer_bquad(k * k), w1_outer),
                    outer_pow(outer_sub(one_outer, w1_outer), 2),
                ),
                outer_pow(d0, 2),
            ),
        ),
        outer_mul(outer_bquad(BQuad(4)), outer_mul(outer_mul(n0, d0), outer_pow(d1, 2))),
    )
    resultant = resultant_w1(raw_product, raw_square)

    n0_w0, d0_w0 = n0[0], d0[0]
    w0 = {1: BQuad(1)}
    t_element = BQuad(TQuad(0, 1))
    r_element = BQuad(RF(POLY_CTX([0, 1])))
    factors = {
        "N0": n0_w0,
        "D0": d0_w0,
        "w0_minus_one": poly_sub(w0, {0: BQuad(1)}),
        "w0_plus_one": poly_add(w0, {0: BQuad(1)}),
        "w0_minus_t2": poly_sub(w0, {0: t_element**2}),
        "w0_minus_r2": poly_sub(w0, {0: r_element**2}),
        "w0_plus_r2": poly_add(w0, {0: r_element**2}),
    }
    candidate = poly_mul(
        poly_mul(factors["N0"], poly_pow(factors["D0"], 5)),
        poly_mul(
            poly_pow(factors["w0_minus_t2"], 2),
            poly_mul(factors["w0_minus_r2"], factors["w0_plus_r2"]),
        ),
    )
    result_degree, candidate_degree = max(resultant), max(candidate)
    if result_degree != 16 or candidate_degree != 16:
        raise RuntimeError(f"unexpected degrees {result_degree}, {candidate_degree}")
    cross = poly_sub(
        poly_scale(resultant, candidate[candidate_degree]),
        poly_scale(candidate, resultant[result_degree]),
    )
    label_evaluations = {
        "zero": element_record(poly_eval(resultant, BQuad(0))),
        "one": element_record(poly_eval(resultant, BQuad(1))),
        "minus_one": element_record(poly_eval(resultant, BQuad(-1))),
        "t2": element_record(poly_eval(resultant, t_element**2)),
        "r2": element_record(poly_eval(resultant, r_element**2)),
        "minus_r2": element_record(poly_eval(resultant, -(r_element**2))),
    }
    label_roots_zero = {
        name: all(
            coordinate["numerator"] == "0"
            for t_coordinate in row["coordinates"]
            for coordinate in t_coordinate
        )
        for name, row in label_evaluations.items()
    }
    residual = resultant
    guard_divisibility = {}
    for name in (
        "N0", "D0", "w0_minus_t2", "w0_plus_one", "w0_minus_one",
        "w0_minus_r2", "w0_plus_r2",
    ):
        exponent, residual = remove_factor(residual, factors[name])
        guard_divisibility[name] = exponent
    if max(residual, default=-1) != 2:
        raise RuntimeError(f"expected quadratic primitive residual, got {max(residual, default=-1)}")
    residual_discriminant = (
        residual[1] * residual[1] - BQuad(4) * residual[2] * residual[0]
    )
    discriminant_norm = norm_bquad(residual_discriminant)
    discriminant_norm_factors = {
        "numerator": factor_record(discriminant_norm.numer),
        "denominator": factor_record(discriminant_norm.denom),
    }
    discriminant_norm_square = all(
        row["multiplicity"] % 2 == 0
        for side in discriminant_norm_factors.values()
        for row in side["factors"]
    ) and all(
        pow(side["scalar"] % P, (P - 1) // 2, P) in (0, 1)
        for side in discriminant_norm_factors.values()
    )
    residual_discriminant_root = sqrt_bquad(residual_discriminant)
    residual_discriminant_square = residual_discriminant_root is not None
    residual_roots = []
    if residual_discriminant_square:
        for signed_root in (residual_discriminant_root, -residual_discriminant_root):
            root = (-residual[1] + signed_root) / (BQuad(2) * residual[2])
            if poly_eval(residual, root) != BQuad(0):
                raise RuntimeError("quadratic root reconstruction failed")
            residual_roots.append(element_record(root))
    extracted = poly_mul(
        poly_mul(factors["N0"], poly_pow(factors["D0"], 5)),
        poly_mul(
            factors["w0_minus_t2"],
            poly_mul(factors["w0_plus_one"], residual),
        ),
    )
    extracted_factorization_exact = not poly_sub(resultant, extracted)
    if not extracted_factorization_exact:
        raise RuntimeError("extracted residual factorization failed to reconstruct")

    generator = random.Random(arguments.seed)
    scan = {"attempted_r_values": 0, "tower_points": 0, "residual_roots": 0,
            "guarded_residual_roots": 0, "witness": None}
    for _ in range(arguments.scan_r_values):
        r_value = generator.randrange(P)
        scan["attempted_r_values"] += 1
        try:
            tu, tv = T_U.specialize(r_value), T_V.specialize(r_value)
        except ZeroDivisionError:
            continue
        for t_value in quadratic_roots(1, -tu, -tv):
            try:
                bu = B_U.specialize(r_value, t_value)
                bv = B_V.specialize(r_value, t_value)
            except ZeroDivisionError:
                continue
            for b_value in quadratic_roots(1, -bu, -bv):
                try:
                    c_value = c_element.specialize(r_value, t_value, b_value)
                except ZeroDivisionError:
                    continue
                scan["tower_points"] += 1
                guard_values = (
                    b_value, c_value, r_value, t_value,
                    b_value - 1, b_value + 1, c_value - 1, c_value + 1,
                    b_value - c_value, b_value + c_value,
                    r_value*r_value - 1, r_value*r_value + 1,
                    t_value*t_value - 1, t_value*t_value + 1,
                    t_value*t_value - r_value*r_value,
                    t_value*t_value + r_value*r_value,
                )
                if any(value % P == 0 for value in guard_values):
                    continue
                residual_fp = specialize_poly(residual, r_value, t_value, b_value)
                w0_roots = quadratic_roots(
                    residual_fp.get(2, 0), residual_fp.get(1, 0),
                    residual_fp.get(0, 0),
                )
                scan["residual_roots"] += len(w0_roots)
                labels = {1, P - 1, r_value*r_value % P,
                          (-r_value*r_value) % P, t_value*t_value % P}
                for w0_value in w0_roots:
                    n0_value = evaluate_fp_poly(
                        specialize_poly(n0_w0, r_value, t_value, b_value),
                        w0_value,
                    )
                    d0_value = evaluate_fp_poly(
                        specialize_poly(d0_w0, r_value, t_value, b_value),
                        w0_value,
                    )
                    if w0_value in labels or w0_value == 0 or n0_value == 0 or d0_value == 0:
                        continue
                    scan["guarded_residual_roots"] += 1
                    product_fp = outer_specialize(
                        raw_product, w0_value, r_value, t_value, b_value
                    )
                    square_fp = outer_specialize(
                        raw_square, w0_value, r_value, t_value, b_value
                    )
                    product_roots = quadratic_roots(
                        product_fp.get(2, 0), product_fp.get(1, 0),
                        product_fp.get(0, 0),
                    )
                    for w1_value in product_roots:
                        if evaluate_fp_poly(square_fp, w1_value) != 0:
                            continue
                        if w1_value == 0 or w1_value == w0_value or w1_value in labels:
                            continue
                        scan["witness"] = {
                            "r": r_value, "t": t_value, "b": b_value,
                            "c": c_value, "w0": w0_value, "w1": w1_value,
                            "N0": n0_value, "D0": d0_value,
                            "raw_product": evaluate_fp_poly(product_fp, w1_value),
                            "raw_square": evaluate_fp_poly(square_fp, w1_value),
                        }
                        break
                    if scan["witness"] is not None:
                        break
                if scan["witness"] is not None:
                    break
            if scan["witness"] is not None:
                break
        if scan["witness"] is not None:
            break

    payload = {
        "schema": "kb-mca-v4-433-1b-cell11-signed-pair-guard-raw-v1",
        "field": P,
        "source_tower_certificate": str(TOWER_CERTIFICATE.relative_to(TOWER_CERTIFICATE.parents[4])),
        "source_tower_sha256": hashlib.sha256(tower_bytes).hexdigest(),
        "cell": 11,
        "epsilon": [-1, -1],
        "pivot": 1,
        "selected_c_row": 5,
        "tower_relation_profiles": {
            "t_u": T_U.record(), "t_v": T_V.record(),
            "b_u": element_profile(BQuad(B_U)),
            "b_v": element_profile(BQuad(B_V)),
            "c": element_profile(c_element),
        },
        "tower_checks": tower_checks,
        "kernel_profiles": [element_profile(value) for value in kernel],
        "b1_opposite": True,
        "raw_product_w1_degree": max(raw_product),
        "raw_square_w1_degree": max(raw_square),
        "resultant": polynomial_profile(resultant),
        "guard_factors": {name: polynomial_profile(value) for name, value in factors.items()},
        "falsified_1a_candidate": polynomial_profile(candidate),
        "falsified_1a_candidate_cross": polynomial_profile(cross),
        "falsified_1a_guard_identity": (
            "N0*D0^5*(w0-t^2)^2*(w0-r^2)*(w0+r^2)"
        ),
        "cross_remainder_zero": not cross,
        "label_evaluation_profiles": {
            name: {
                "sha256": row["sha256"],
                "zero": label_roots_zero[name],
            }
            for name, row in label_evaluations.items()
        },
        "label_roots_zero": label_roots_zero,
        "guard_divisibility": guard_divisibility,
        "exact_factorization": (
            "resultant=N0*D0^5*(w0-t^2)*(w0+1)*Q2"
        ),
        "exact_factorization_reconstructs": extracted_factorization_exact,
        "guard_residual": polynomial_profile(residual),
        "guard_residual_discriminant": element_profile(residual_discriminant),
        "guard_residual_discriminant_norm": {
            "sha256": canonical_hash(discriminant_norm.record()),
            "numerator_degree": int(discriminant_norm.numer.degree()),
            "denominator_degree": int(discriminant_norm.denom.degree()),
        },
        "guard_residual_discriminant_norm_factors": discriminant_norm_factors,
        "guard_residual_discriminant_norm_square": discriminant_norm_square,
        "guard_residual_discriminant_square": residual_discriminant_square,
        "guard_residual_discriminant_root": (
            None if residual_discriminant_root is None
            else element_profile(residual_discriminant_root)
        ),
        "guard_residual_roots": [
            {"sha256": row["sha256"]} for row in residual_roots
        ],
        "deployed_fiber_scan": {
            "seed": arguments.seed,
            "limit": arguments.scan_r_values,
            **scan,
        },
        "leading_exception_classified": False,
        "sign_transport_complete": False,
        "role_orbit_11_closed": False,
    }
    arguments.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "resultant": {key: payload["resultant"][key] for key in (
            "degree", "nonzero_coefficients", "max_r_numerator_degree",
            "max_r_denominator_degree", "sha256",
        )},
        "candidate_sha256": payload["falsified_1a_candidate"]["sha256"],
        "cross_remainder_zero": not cross,
        "cross_degree": max(cross, default=-1),
        "label_roots_zero": label_roots_zero,
        "guard_divisibility": guard_divisibility,
        "guard_residual_degree": max(residual, default=-1),
        "guard_residual_discriminant_norm_square": discriminant_norm_square,
        "guard_residual_discriminant_square": residual_discriminant_square,
        "deployed_witness_found": scan["witness"] is not None,
        "deployed_fiber_scan": scan,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
