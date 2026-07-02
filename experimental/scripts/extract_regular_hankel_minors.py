#!/usr/bin/env python3
"""Extract regular overdetermined Hankel-minor certificates from row data.

This is the first reusable M3 extractor for the Paper D v12 atlas.  It reads
syndrome-pencil input, tries candidate maximal Hankel row minors for each exact
agreement, and emits an ``aperiodic-hankel-eliminant-v1`` packet.

The determinant polynomial is recovered by interpolation from numeric
determinants, avoiding the factorial permutation determinant used by the first
hard-coded toy verifier.  The current implementation supports prime fields
``F_p`` and polynomial-basis extension fields supplied by the input JSON.  The
extension path uses encoded integer root tables so the existing v9 checker can
still audit degrees, root hashes, and declared numerators.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha256
import json
from itertools import combinations, permutations, product
from pathlib import Path
from typing import Any


DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE = 10000
DEFAULT_MAX_BAD_SLOPE_SUBSETS = 200000
ZERO_U_MONOMIAL_MODE = "zero_u_monomial_roots"
SCALAR_MULTIPLE_MODE = "scalar_multiple_roots"
ONE_SPIKE_LINEAR_MODE = "one_spike_linear_roots"
LOW_RANK_UPDATE_MODE = "low_rank_update_bound"
MINOR_GCD_MODE = "minor_gcd_roots"
ZERO_U_GCD_METHOD = "zero_u_monomial"
RANK_AT_NODES_FAMILY_STRATEGY = "rank_at_nodes_family"


def sampler_audit(row_field: str, sampler: str, field_size: int) -> dict[str, Any]:
    if sampler == "finite_affine_line":
        denominator = field_size
        denominator_formula = "|F|"
    elif sampler == "projective_line":
        denominator = field_size + 1
        denominator_formula = "|P^1(F)| = |F| + 1"
    else:
        denominator = field_size
        denominator_formula = "sampler-specific parameter count"
    return {
        "sampler": sampler,
        "slope_field": row_field,
        "slope_field_order": field_size,
        "denominator": denominator,
        "denominator_formula": denominator_formula,
        "field_role": "q_line",
        "extension_denominator_warning": (
            "extension-valued slope packets are divided by the slope field "
            "order, not by the base field"
        ),
    }


def mod(value: int, prime: int) -> int:
    return value % prime


def trim(poly: list[int], prime: int) -> list[int]:
    out = [mod(coeff, prime) for coeff in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % prime
    return trim(out, prime)


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_coeff in enumerate(left):
        for j, right_coeff in enumerate(right):
            out[i + j] = (out[i + j] + left_coeff * right_coeff) % prime
    return trim(out, prime)


def poly_scale(poly: list[int], scalar: int, prime: int) -> list[int]:
    return trim([(scalar * coeff) % prime for coeff in poly], prime)


def poly_eval(poly: list[int], value: int, prime: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % prime
        power = (power * value) % prime
    return total


def poly_degree(poly: list[int], prime: int) -> int:
    return len(trim(poly, prime)) - 1


def poly_divmod(
    numerator: list[int],
    denominator: list[int],
    prime: int,
) -> tuple[list[int], list[int]]:
    work = trim(numerator, prime)
    divisor = trim(denominator, prime)
    if divisor == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [0] * max(1, len(work) - len(divisor) + 1)
    while len(work) >= len(divisor) and work != [0]:
        coeff = work[-1] * pow(divisor[-1], -1, prime) % prime
        shift = len(work) - len(divisor)
        quotient[shift] = coeff
        subtractor = [0] * shift + [(coeff * term) % prime for term in divisor]
        work = trim(
            [
                (
                    (work[index] if index < len(work) else 0)
                    - (subtractor[index] if index < len(subtractor) else 0)
                )
                % prime
                for index in range(max(len(work), len(subtractor)))
            ],
            prime,
        )
    return trim(quotient, prime), work


def poly_monic(poly: list[int], prime: int) -> list[int]:
    out = trim(poly, prime)
    if out == [0]:
        return out
    return poly_scale(out, pow(out[-1], -1, prime), prime)


def poly_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    a = trim(left, prime)
    b = trim(right, prime)
    if a == [0]:
        return poly_monic(b, prime)
    if b == [0]:
        return poly_monic(a, prime)
    while b != [0]:
        _quotient, remainder = poly_divmod(a, b, prime)
        a, b = b, remainder
    return poly_monic(a, prime)


def poly_gcd_many(polynomials: list[list[int]], prime: int) -> list[int]:
    if not polynomials:
        raise ValueError("need at least one polynomial for gcd")
    out = polynomials[0]
    for polynomial in polynomials[1:]:
        out = poly_gcd(out, polynomial, prime)
    return poly_monic(out, prime)


def linear_power_mod(constant: int, exponent: int, prime: int) -> list[int]:
    out = [1]
    factor = [constant % prime, 1]
    for _ in range(exponent):
        out = poly_mul(out, factor, prime)
    return out


def divide_by_linear_root_mod(
    poly: list[int],
    root: int,
    prime: int,
) -> list[int] | None:
    coeffs = trim(poly, prime)
    degree = len(coeffs) - 1
    if degree <= 0:
        return None
    root %= prime
    quotient = [0] * degree
    quotient[-1] = coeffs[degree]
    for index in range(degree - 1, 0, -1):
        quotient[index - 1] = (coeffs[index] + root * quotient[index]) % prime
    remainder = (coeffs[0] + root * quotient[0]) % prime
    if remainder != 0:
        return None
    return trim(quotient, prime)


def split_linear_root_certificate_mod(
    poly: list[int],
    roots: list[int] | None,
    prime: int,
) -> dict[str, Any] | None:
    if roots is None:
        return None
    work = trim(poly, prime)
    factors = []
    for root in sorted(set(root % prime for root in roots)):
        multiplicity = 0
        while len(work) > 1:
            quotient = divide_by_linear_root_mod(work, root, prime)
            if quotient is None:
                break
            multiplicity += 1
            work = quotient
        if multiplicity:
            factors.append({"root": root, "multiplicity": multiplicity})
    factor_roots = sorted(factor["root"] for factor in factors)
    if len(work) == 1 and work[0] % prime != 0 and factor_roots == sorted(
        set(root % prime for root in roots)
    ):
        return {
            "kind": "split_linear_factorization",
            "leading_coefficient": work[0] % prime,
            "factors": factors,
        }
    return None


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def hash_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def optional_file_hash(path_text: str | None) -> str | None:
    if path_text is None:
        return None
    path = Path(path_text)
    if not path.exists():
        return None
    return hash_file(path)


def parse_prime_field(field_name: str) -> int:
    if not (field_name.startswith("F_") and field_name[2:].isdigit()):
        raise ValueError(f"only prime fields F_p are supported, got {field_name!r}")
    prime = int(field_name[2:])
    if prime < 2:
        raise ValueError("field prime must be at least 2")
    return prime


class PolynomialBasisField:
    """Finite field F_p[X]/(modulus), with low-degree-first coefficients."""

    def __init__(self, prime: int, modulus: list[int]):
        if prime < 2:
            raise ValueError("field prime must be at least 2")
        if len(modulus) < 2:
            raise ValueError("field modulus must have positive degree")
        if modulus[-1] % prime != 1:
            raise ValueError("field modulus must be monic in low-to-high form")
        self.p = prime
        self.modulus = [coeff % prime for coeff in modulus]
        self.degree = len(modulus) - 1
        self.size = prime**self.degree
        self.zero = (0,) * self.degree
        self.one = (1,) + (0,) * (self.degree - 1)

    @classmethod
    def from_spec(cls, spec: dict[str, Any]) -> "PolynomialBasisField":
        if spec.get("kind") != "polynomial_basis":
            raise ValueError("field_model.kind must be polynomial_basis")
        return cls(int(spec["p"]), [int(value) for value in spec["modulus"]])

    def normalize(self, value: Any) -> tuple[int, ...]:
        if isinstance(value, int):
            coeffs = [value % self.p]
        elif isinstance(value, list):
            coeffs = [int(entry) % self.p for entry in value]
        elif isinstance(value, tuple):
            coeffs = [int(entry) % self.p for entry in value]
        else:
            raise ValueError(f"unsupported field element {value!r}")
        if len(coeffs) > self.degree:
            raise ValueError("field element has too many coefficients")
        coeffs += [0] * (self.degree - len(coeffs))
        return tuple(coeffs)

    def encode(self, value: Any) -> int:
        elem = self.normalize(value)
        total = 0
        place = 1
        for coeff in elem:
            total += coeff * place
            place *= self.p
        return total

    def decode(self, value: int) -> tuple[int, ...]:
        if value < 0 or value >= self.size:
            raise ValueError("encoded field element outside field range")
        coeffs = []
        remaining = value
        for _ in range(self.degree):
            coeffs.append(remaining % self.p)
            remaining //= self.p
        return tuple(coeffs)

    def add(self, left: Any, right: Any) -> tuple[int, ...]:
        a = self.normalize(left)
        b = self.normalize(right)
        return tuple((a[i] + b[i]) % self.p for i in range(self.degree))

    def sub(self, left: Any, right: Any) -> tuple[int, ...]:
        a = self.normalize(left)
        b = self.normalize(right)
        return tuple((a[i] - b[i]) % self.p for i in range(self.degree))

    def neg(self, value: Any) -> tuple[int, ...]:
        elem = self.normalize(value)
        return tuple((-coeff) % self.p for coeff in elem)

    def mul(self, left: Any, right: Any) -> tuple[int, ...]:
        a = self.normalize(left)
        b = self.normalize(right)
        coeffs = [0] * (2 * self.degree - 1)
        for i, a_i in enumerate(a):
            for j, b_j in enumerate(b):
                coeffs[i + j] = (coeffs[i + j] + a_i * b_j) % self.p
        for deg in range(len(coeffs) - 1, self.degree - 1, -1):
            lead = coeffs[deg] % self.p
            if lead == 0:
                continue
            offset = deg - self.degree
            for j in range(self.degree):
                coeffs[offset + j] = (
                    coeffs[offset + j] - lead * self.modulus[j]
                ) % self.p
        return tuple(coeffs[: self.degree])

    def pow(self, value: Any, exponent: int) -> tuple[int, ...]:
        if exponent < 0:
            return self.pow(self.inv(value), -exponent)
        out = self.one
        base = self.normalize(value)
        while exponent:
            if exponent & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            exponent >>= 1
        return out

    def inv(self, value: Any) -> tuple[int, ...]:
        elem = self.normalize(value)
        if elem == self.zero:
            raise ZeroDivisionError("division by zero")
        return self.pow(elem, self.size - 2)

    def div(self, left: Any, right: Any) -> tuple[int, ...]:
        return self.mul(left, self.inv(right))

    def is_zero(self, value: Any) -> bool:
        return self.normalize(value) == self.zero

    def elements(self):
        for coeffs in product(range(self.p), repeat=self.degree):
            yield coeffs


def determinant_mod(matrix: list[list[int]], prime: int) -> int:
    """Return det(matrix) over F_prime by Gaussian elimination."""
    size = len(matrix)
    work = [[entry % prime for entry in row] for row in matrix]
    det = 1
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if work[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            det = (-det) % prime
        pivot_value = work[col][col] % prime
        det = (det * pivot_value) % prime
        inv_pivot = pow(pivot_value, -1, prime)
        for row in range(col + 1, size):
            factor = (work[row][col] * inv_pivot) % prime
            if factor == 0:
                continue
            for entry_col in range(col, size):
                work[row][entry_col] = (
                    work[row][entry_col] - factor * work[col][entry_col]
                ) % prime
    return det % prime


def interpolate(points: list[tuple[int, int]], prime: int) -> list[int]:
    """Interpolate the unique degree < len(points) polynomial over F_prime."""
    out = [0]
    for index, (x_i, y_i) in enumerate(points):
        basis = [1]
        denominator = 1
        for other_index, (x_j, _y_j) in enumerate(points):
            if other_index == index:
                continue
            basis = poly_mul(basis, [(-x_j) % prime, 1], prime)
            denominator = (denominator * (x_i - x_j)) % prime
        scale = y_i * pow(denominator, -1, prime)
        out = poly_add(out, poly_scale(basis, scale, prime), prime)
    return trim(out, prime)


def matrix_at_slope(
    u: list[int],
    v: list[int],
    row_set: list[int],
    cols: int,
    slope: int,
    prime: int,
) -> list[list[int]]:
    return [
        [(u[row + col] + slope * v[row + col]) % prime for col in range(cols)]
        for row in row_set
    ]


def determinant_polynomial_by_interpolation(
    u: list[int],
    v: list[int],
    row_set: list[int],
    cols: int,
    prime: int,
) -> list[int]:
    degree_bound = cols
    if prime <= degree_bound:
        raise ValueError(
            f"need prime > degree bound for base-field interpolation, got {prime} <= {degree_bound}"
        )
    points = []
    for slope in range(degree_bound + 1):
        det = determinant_mod(matrix_at_slope(u, v, row_set, cols, slope, prime), prime)
        points.append((slope, det))
    poly = interpolate(points, prime)
    for slope, det in points:
        if poly_eval(poly, slope, prime) != det:
            raise AssertionError(("interpolation check failed", slope, det, poly))
    return poly


def locator_coefficients(roots: tuple[int, ...], prime: int) -> list[int]:
    coeffs = [1]
    for root in roots:
        coeffs = poly_mul(coeffs, [(-root) % prime, 1], prime)
    return coeffs


def hankel_times_locator(
    syndrome: list[int], t: int, locator: list[int], prime: int
) -> list[int]:
    j = len(locator) - 1
    return [
        sum(syndrome[row + col] * locator[col] for col in range(j + 1)) % prime
        for row in range(t)
    ]


def finite_bad_slopes_for_exact_agreement(
    u: list[int],
    v: list[int],
    domain: list[int],
    n: int,
    k: int,
    exact_agreement: int,
    prime: int,
) -> list[int]:
    j = n - exact_agreement
    t = exact_agreement - k
    slopes: set[int] = set()
    for roots in combinations(domain, j):
        locator = locator_coefficients(roots, prime)
        a_vec = hankel_times_locator(u, t, locator, prime)
        b_vec = hankel_times_locator(v, t, locator, prime)
        if all(value == 0 for value in b_vec):
            continue
        candidate = None
        consistent = True
        for a_i, b_i in zip(a_vec, b_vec):
            if b_i == 0:
                if a_i != 0:
                    consistent = False
                    break
                continue
            slope = (-a_i * pow(b_i, -1, prime)) % prime
            if candidate is None:
                candidate = slope
            elif candidate != slope:
                consistent = False
                break
        if consistent and candidate is not None:
            slopes.add(candidate)
    return sorted(slopes)


def zero_u_monomial_minor_records_mod(
    u: list[int],
    v: list[int],
    row_sets: list[list[int]],
    visible_length: int,
    size: int,
    prime: int,
) -> tuple[list[list[int]], list[dict[str, Any]]]:
    if any(value % prime for value in u[:visible_length]):
        raise ValueError("zero_u_monomial gcd method needs u=0 on the visible window")
    polynomials = []
    family_records = []
    for row_set in row_sets:
        leading = determinant_mod(
            [[v[row + col] % prime for col in range(size)] for row in row_set],
            prime,
        )
        polynomial = [0] if leading == 0 else [0] * size + [leading]
        polynomials.append(polynomial)
        family_records.append(
            {
                "row_set": row_set,
                "coefficients": polynomial,
                "degree": poly_degree(polynomial, prime)
                if polynomial != [0]
                else -1,
            }
        )
    return polynomials, family_records


def normalize_field_input_value(
    value: Any,
    field: PolynomialBasisField,
    encoding: str | None,
) -> tuple[int, ...]:
    if encoding in {
        "base-p low-to-high integer",
        "base-p low-to-high encoded integer",
        "encoded_integer",
    }:
        if not isinstance(value, int):
            raise ValueError("encoded field input values must be integers")
        return field.decode(value)
    return field.normalize(value)


def normalize_field_input_list(
    values: list[Any],
    field: PolynomialBasisField,
    encoding: str | None,
) -> list[tuple[int, ...]]:
    return [normalize_field_input_value(value, field, encoding) for value in values]


def n_choose_k(n: int, k: int) -> int:
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    numerator = 1
    denominator = 1
    for value in range(1, k + 1):
        numerator *= n - k + value
        denominator *= value
    return numerator // denominator


def fpoly_trim(
    poly: list[tuple[int, ...]], field: PolynomialBasisField
) -> list[tuple[int, ...]]:
    out = [field.normalize(coeff) for coeff in poly]
    while len(out) > 1 and field.is_zero(out[-1]):
        out.pop()
    if not out:
        return [field.zero]
    return out


def fpoly_add(
    left: list[tuple[int, ...]],
    right: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    size = max(len(left), len(right))
    out = [field.zero] * size
    for index in range(size):
        left_coeff = left[index] if index < len(left) else field.zero
        right_coeff = right[index] if index < len(right) else field.zero
        out[index] = field.add(left_coeff, right_coeff)
    return fpoly_trim(out, field)


def fpoly_mul(
    left: list[tuple[int, ...]],
    right: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    out = [field.zero] * (len(left) + len(right) - 1)
    for i, left_coeff in enumerate(left):
        for j, right_coeff in enumerate(right):
            out[i + j] = field.add(out[i + j], field.mul(left_coeff, right_coeff))
    return fpoly_trim(out, field)


def fpoly_scale(
    poly: list[tuple[int, ...]],
    scalar: tuple[int, ...],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    return fpoly_trim([field.mul(coeff, scalar) for coeff in poly], field)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = 0
    for left_index, left in enumerate(permutation):
        for right in permutation[left_index + 1 :]:
            if left > right:
                inversions += 1
    return -1 if inversions % 2 else 1


def fpoly_determinant(
    matrix: list[list[list[tuple[int, ...]]]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    size = len(matrix)
    if size == 0:
        return [field.one]
    total = [field.zero]
    for permutation in permutations(range(size)):
        term = [field.one]
        for row, col in enumerate(permutation):
            term = fpoly_mul(term, matrix[row][col], field)
        if permutation_sign(permutation) < 0:
            term = fpoly_scale(term, field.neg(field.one), field)
        total = fpoly_add(total, term, field)
    return fpoly_trim(total, field)


def fpoly_eval(
    poly: list[tuple[int, ...]],
    value: tuple[int, ...],
    field: PolynomialBasisField,
) -> tuple[int, ...]:
    total = field.zero
    power = field.one
    for coeff in poly:
        total = field.add(total, field.mul(coeff, power))
        power = field.mul(power, value)
    return total


def fpoly_degree(
    poly: list[tuple[int, ...]], field: PolynomialBasisField
) -> int:
    return len(fpoly_trim(poly, field)) - 1


def fpoly_is_zero(
    poly: list[tuple[int, ...]], field: PolynomialBasisField
) -> bool:
    trimmed = fpoly_trim(poly, field)
    return len(trimmed) == 1 and field.is_zero(trimmed[0])


def fpoly_divmod(
    numerator: list[tuple[int, ...]],
    denominator: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    work = fpoly_trim(numerator, field)
    divisor = fpoly_trim(denominator, field)
    if fpoly_is_zero(divisor, field):
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [field.zero] * max(1, len(work) - len(divisor) + 1)
    while len(work) >= len(divisor) and not fpoly_is_zero(work, field):
        coeff = field.div(work[-1], divisor[-1])
        shift = len(work) - len(divisor)
        quotient[shift] = coeff
        subtractor = [field.zero] * shift + [
            field.mul(coeff, term) for term in divisor
        ]
        size = max(len(work), len(subtractor))
        work = fpoly_trim(
            [
                field.sub(
                    work[index] if index < len(work) else field.zero,
                    subtractor[index] if index < len(subtractor) else field.zero,
                )
                for index in range(size)
            ],
            field,
        )
    return fpoly_trim(quotient, field), work


def fpoly_monic(
    poly: list[tuple[int, ...]], field: PolynomialBasisField
) -> list[tuple[int, ...]]:
    out = fpoly_trim(poly, field)
    if fpoly_is_zero(out, field):
        return out
    return fpoly_scale(out, field.inv(out[-1]), field)


def fpoly_gcd(
    left: list[tuple[int, ...]],
    right: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    a = fpoly_trim(left, field)
    b = fpoly_trim(right, field)
    if fpoly_is_zero(a, field):
        return fpoly_monic(b, field)
    if fpoly_is_zero(b, field):
        return fpoly_monic(a, field)
    while not fpoly_is_zero(b, field):
        _quotient, remainder = fpoly_divmod(a, b, field)
        a, b = b, remainder
    return fpoly_monic(a, field)


def fpoly_gcd_many(
    polynomials: list[list[tuple[int, ...]]], field: PolynomialBasisField
) -> list[tuple[int, ...]]:
    if not polynomials:
        raise ValueError("need at least one polynomial for gcd")
    out = polynomials[0]
    for polynomial in polynomials[1:]:
        out = fpoly_gcd(out, polynomial, field)
    return fpoly_monic(out, field)


def fpoly_linear_power(
    constant: tuple[int, ...],
    exponent: int,
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    out = [field.one]
    factor = [constant, field.one]
    for _ in range(exponent):
        out = fpoly_mul(out, factor, field)
    return out


def fpoly_divide_by_linear_root(
    poly: list[tuple[int, ...]],
    root: tuple[int, ...],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]] | None:
    coeffs = fpoly_trim(poly, field)
    degree = len(coeffs) - 1
    if degree <= 0:
        return None
    root = field.normalize(root)
    quotient = [field.zero] * degree
    quotient[-1] = coeffs[degree]
    for index in range(degree - 1, 0, -1):
        quotient[index - 1] = field.add(
            coeffs[index], field.mul(root, quotient[index])
        )
    remainder = field.add(coeffs[0], field.mul(root, quotient[0]))
    if not field.is_zero(remainder):
        return None
    return fpoly_trim(quotient, field)


def split_linear_root_certificate_field(
    poly: list[tuple[int, ...]],
    roots: list[tuple[int, ...]] | None,
    field: PolynomialBasisField,
) -> dict[str, Any] | None:
    if roots is None:
        return None
    work = fpoly_trim(poly, field)
    root_set = sorted({field.encode(root) for root in roots})
    factors = []
    for root_encoding in root_set:
        root = field.decode(root_encoding)
        multiplicity = 0
        while len(work) > 1:
            quotient = fpoly_divide_by_linear_root(work, root, field)
            if quotient is None:
                break
            multiplicity += 1
            work = quotient
        if multiplicity:
            factors.append({"root": root_encoding, "multiplicity": multiplicity})
    factor_roots = sorted(factor["root"] for factor in factors)
    if len(work) == 1 and not field.is_zero(work[0]) and factor_roots == root_set:
        return {
            "kind": "split_linear_factorization",
            "leading_coefficient": field.encode(work[0]),
            "field_encoding": "base-p low-to-high integer",
            "factors": factors,
        }
    return None


def field_square_root(
    value: tuple[int, ...],
    field: PolynomialBasisField,
) -> tuple[int, ...] | None:
    value = field.normalize(value)
    if field.is_zero(value):
        return field.zero
    if field.pow(value, (field.size - 1) // 2) != field.one:
        return None

    odd_part = field.size - 1
    two_power = 0
    while odd_part % 2 == 0:
        two_power += 1
        odd_part //= 2

    nonsquare = None
    for encoding in range(2, min(field.size, 10000)):
        candidate = field.decode(encoding)
        if field.pow(candidate, (field.size - 1) // 2) != field.one:
            nonsquare = candidate
            break
    if nonsquare is None:
        raise ValueError("could not find a nonsquare for Tonelli-Shanks")

    m = two_power
    c = field.pow(nonsquare, odd_part)
    t = field.pow(value, odd_part)
    root = field.pow(value, (odd_part + 1) // 2)
    while t != field.one:
        i = 1
        t_power = field.mul(t, t)
        while t_power != field.one:
            i += 1
            if i >= m:
                raise ValueError("Tonelli-Shanks failed to converge")
            t_power = field.mul(t_power, t_power)
        b = field.pow(c, 1 << (m - i - 1))
        root = field.mul(root, b)
        t = field.mul(t, field.mul(b, b))
        c = field.mul(b, b)
        m = i
    return root


def quadratic_roots_field(
    coefficients: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]] | None:
    polynomial = fpoly_trim(coefficients, field)
    if len(polynomial) != 3 or field.is_zero(polynomial[2]):
        return None
    c0, c1, c2 = polynomial
    discriminant = field.sub(
        field.mul(c1, c1),
        field.mul(field.mul(field.normalize(4), c2), c0),
    )
    sqrt_discriminant = field_square_root(discriminant, field)
    if sqrt_discriminant is None:
        return []
    denominator_inverse = field.inv(field.mul(field.normalize(2), c2))
    roots = {
        field.encode(
            field.mul(field.add(field.neg(c1), signed_sqrt), denominator_inverse)
        )
        for signed_sqrt in (sqrt_discriminant, field.neg(sqrt_discriminant))
    }
    return [field.decode(root) for root in sorted(roots)]


def quadratic_root_certificate_field(
    coefficients: list[tuple[int, ...]],
    roots: list[tuple[int, ...]] | None,
    field: PolynomialBasisField,
) -> dict[str, Any] | None:
    if roots is None:
        return None
    polynomial = fpoly_trim(coefficients, field)
    if len(polynomial) != 3 or field.is_zero(polynomial[2]):
        return None
    c0, c1, c2 = polynomial
    discriminant = field.sub(
        field.mul(c1, c1),
        field.mul(field.mul(field.normalize(4), c2), c0),
    )
    sqrt_discriminant = field_square_root(discriminant, field)
    if sqrt_discriminant is None:
        if roots == []:
            return {
                "kind": "quadratic_discriminant_nonsquare",
                "field_encoding": "base-p low-to-high integer",
                "coefficients_ascending": [
                    field.encode(coefficient) for coefficient in polynomial
                ],
                "discriminant": field.encode(discriminant),
                "euler_witness": field.encode(
                    field.pow(discriminant, (field.size - 1) // 2)
                ),
                "root_formula": "no roots because the discriminant is nonsquare",
                "roots": [],
            }
        return None
    formula_roots = quadratic_roots_field(polynomial, field)
    if formula_roots is None:
        return None
    if sorted(field.encode(root) for root in formula_roots) != sorted(
        field.encode(root) for root in roots
    ):
        return None
    return {
        "kind": "quadratic_discriminant_split",
        "field_encoding": "base-p low-to-high integer",
        "coefficients_ascending": [
            field.encode(coefficient) for coefficient in polynomial
        ],
        "discriminant": field.encode(discriminant),
        "sqrt_discriminant": field.encode(sqrt_discriminant),
        "root_formula": "(-b +/- sqrt(discriminant))/(2a)",
        "roots": sorted(field.encode(root) for root in roots),
    }


def determinant_field(
    matrix: list[list[tuple[int, ...]]], field: PolynomialBasisField
) -> tuple[int, ...]:
    size = len(matrix)
    work = [[field.normalize(entry) for entry in row] for row in matrix]
    det = field.one
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if not field.is_zero(work[row][col]):
                pivot = row
                break
        if pivot is None:
            return field.zero
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            det = field.neg(det)
        pivot_value = work[col][col]
        det = field.mul(det, pivot_value)
        inv_pivot = field.inv(pivot_value)
        for row in range(col + 1, size):
            factor = field.mul(work[row][col], inv_pivot)
            if field.is_zero(factor):
                continue
            for entry_col in range(col, size):
                work[row][entry_col] = field.sub(
                    work[row][entry_col],
                    field.mul(factor, work[col][entry_col]),
                )
    return det


def interpolate_field(
    points: list[tuple[tuple[int, ...], tuple[int, ...]]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    out = [field.zero]
    for index, (x_i, y_i) in enumerate(points):
        basis = [field.one]
        denominator = field.one
        for other_index, (x_j, _y_j) in enumerate(points):
            if other_index == index:
                continue
            basis = fpoly_mul(basis, [field.neg(x_j), field.one], field)
            denominator = field.mul(denominator, field.sub(x_i, x_j))
        scale = field.div(y_i, denominator)
        out = fpoly_add(out, fpoly_scale(basis, scale, field), field)
    return fpoly_trim(out, field)


def matrix_at_slope_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    row_set: list[int],
    cols: int,
    slope: tuple[int, ...],
    field: PolynomialBasisField,
) -> list[list[tuple[int, ...]]]:
    return [
        [field.add(u[row + col], field.mul(slope, v[row + col])) for col in range(cols)]
        for row in row_set
    ]


def determinant_polynomial_by_interpolation_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    row_set: list[int],
    cols: int,
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    degree_bound = cols
    if field.size <= degree_bound:
        raise ValueError(
            f"need field size > degree bound for interpolation, got {field.size} <= {degree_bound}"
        )
    nodes = [field.decode(index) for index in range(degree_bound + 1)]
    points = []
    for slope in nodes:
        det = determinant_field(
            matrix_at_slope_field(u, v, row_set, cols, slope, field),
            field,
        )
        points.append((slope, det))
    poly = interpolate_field(points, field)
    for slope, det in points:
        if fpoly_eval(poly, slope, field) != det:
            raise AssertionError(("extension interpolation check failed", slope, det))
    return poly


def locator_coefficients_field(
    roots: tuple[tuple[int, ...], ...], field: PolynomialBasisField
) -> list[tuple[int, ...]]:
    coeffs = [field.one]
    for root in roots:
        coeffs = fpoly_mul(coeffs, [field.neg(root), field.one], field)
    return coeffs


def hankel_times_locator_field(
    syndrome: list[tuple[int, ...]],
    t: int,
    locator: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    j = len(locator) - 1
    out = []
    for row in range(t):
        total = field.zero
        for col in range(j + 1):
            total = field.add(total, field.mul(syndrome[row + col], locator[col]))
        out.append(total)
    return out


def finite_bad_slopes_for_exact_agreement_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    domain: list[tuple[int, ...]],
    n: int,
    k: int,
    exact_agreement: int,
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    j = n - exact_agreement
    t = exact_agreement - k
    slopes: dict[int, tuple[int, ...]] = {}
    for roots in combinations(domain, j):
        locator = locator_coefficients_field(roots, field)
        a_vec = hankel_times_locator_field(u, t, locator, field)
        b_vec = hankel_times_locator_field(v, t, locator, field)
        if all(field.is_zero(value) for value in b_vec):
            continue
        candidate = None
        consistent = True
        for a_i, b_i in zip(a_vec, b_vec):
            if field.is_zero(b_i):
                if not field.is_zero(a_i):
                    consistent = False
                    break
                continue
            slope = field.neg(field.div(a_i, b_i))
            if candidate is None:
                candidate = slope
            elif candidate != slope:
                consistent = False
                break
        if consistent and candidate is not None:
            slopes[field.encode(candidate)] = candidate
    return [slopes[key] for key in sorted(slopes)]


def zero_u_monomial_minor_records_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    row_sets: list[list[int]],
    visible_length: int,
    size: int,
    field: PolynomialBasisField,
) -> tuple[list[list[tuple[int, ...]]], list[dict[str, Any]]]:
    if any(not field.is_zero(value) for value in u[:visible_length]):
        raise ValueError("zero_u_monomial gcd method needs u=0 on the visible window")
    polynomials = []
    family_records = []
    for row_set in row_sets:
        leading = determinant_field(
            [[v[row + col] for col in range(size)] for row in row_set],
            field,
        )
        polynomial = (
            [field.zero]
            if field.is_zero(leading)
            else [field.zero] * size + [leading]
        )
        polynomials.append(polynomial)
        family_records.append(
            {
                "row_set": row_set,
                "coefficients": polynomial,
                "degree": fpoly_degree(polynomial, field)
                if not fpoly_is_zero(polynomial, field)
                else -1,
            }
        )
    return polynomials, family_records


def vandermonde_square_field(
    nodes: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[int, ...]:
    out = field.one
    for left_index, left in enumerate(nodes):
        for right in nodes[left_index + 1 :]:
            diff = field.sub(right, left)
            out = field.mul(out, field.mul(diff, diff))
    return out


def one_spike_linear_coefficients_field(
    base_nodes: list[tuple[int, ...]],
    spike: tuple[int, ...],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    """Return [C0, C1] for det(V_X V_X^T + Z w_y w_y^T)."""

    c0 = vandermonde_square_field(base_nodes, field)
    c1 = field.zero
    for index, node in enumerate(base_nodes):
        numerator = field.one
        denominator = field.one
        for other_index, other in enumerate(base_nodes):
            if other_index == index:
                continue
            num_diff = field.sub(spike, other)
            den_diff = field.sub(node, other)
            numerator = field.mul(numerator, field.mul(num_diff, num_diff))
            denominator = field.mul(denominator, field.mul(den_diff, den_diff))
        c1 = field.add(c1, field.mul(c0, field.div(numerator, denominator)))
    return [c0, c1]


def one_spike_syndrome_field(
    nodes: list[tuple[int, ...]],
    length: int,
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    powers = [field.one for _ in nodes]
    out = []
    for exponent in range(length):
        if exponent == 0:
            total = field.normalize(len(nodes))
        else:
            total = field.zero
            for power in powers:
                total = field.add(total, power)
        out.append(total)
        powers = [field.mul(power, node) for power, node in zip(powers, nodes)]
    return out


def one_spike_linear_data_field(
    spec: dict[str, Any],
    size: int,
    visible_length: int,
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[list[tuple[int, ...]], tuple[int, ...], list[tuple[int, ...]]]:
    data = spec.get("one_spike_linear")
    if not isinstance(data, dict):
        raise ValueError("one_spike_linear_roots needs one_spike_linear metadata")
    base_encodings = data.get("base_node_encodings")
    if not isinstance(base_encodings, list):
        raise ValueError("one_spike_linear.base_node_encodings must be a list")
    if len(base_encodings) != size:
        raise ValueError("one_spike_linear base-node count must equal minor size")
    spike_encoding = data.get("spike_encoding")
    if not isinstance(spike_encoding, int):
        raise ValueError("one_spike_linear.spike_encoding must be an integer")
    base_nodes = [field.decode(int(value)) for value in base_encodings]
    spike = field.decode(spike_encoding)
    expected_u = one_spike_syndrome_field(base_nodes, visible_length, field)
    expected_v = one_spike_syndrome_field([spike], visible_length, field)
    if u[:visible_length] != expected_u:
        raise ValueError("one_spike_linear u moments do not match base nodes")
    if v[:visible_length] != expected_v:
        raise ValueError("one_spike_linear v moments do not match spike")
    return base_nodes, spike, one_spike_linear_coefficients_field(
        base_nodes, spike, field
    )


def low_rank_update_coefficients_field(
    base_nodes: list[tuple[int, ...]],
    update_nodes: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    """Return coefficients for det(V_X V_X^T + Z V_Y V_Y^T).

    This optimized form assumes ``len(base_nodes)`` is the prefix minor size.
    It computes Cauchy-Binet terms by replacing d base nodes with d update
    nodes and scaling the base Vandermonde square.
    """

    if not update_nodes:
        raise ValueError("low-rank update needs at least one update node")
    if len(set(base_nodes)) != len(base_nodes):
        raise ValueError("low-rank update base nodes must be distinct")
    if len(set(update_nodes)) != len(update_nodes):
        raise ValueError("low-rank update nodes must be distinct")
    if set(base_nodes).intersection(update_nodes):
        raise ValueError("low-rank update nodes must be disjoint from base nodes")

    c0 = vandermonde_square_field(base_nodes, field)
    coefficients = [field.zero] * (len(update_nodes) + 1)
    coefficients[0] = c0
    base_denominators = []
    for index, node in enumerate(base_nodes):
        denominator = field.one
        for other_index, other in enumerate(base_nodes):
            if other_index == index:
                continue
            diff = field.sub(node, other)
            denominator = field.mul(denominator, field.mul(diff, diff))
        base_denominators.append(denominator)
    base_denominator_inverses = [field.inv(value) for value in base_denominators]

    update_to_all_base: dict[tuple[int, ...], tuple[int, ...]] = {}
    update_to_base_inverse_squares: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for update in update_nodes:
        product_all = field.one
        inverse_squares = []
        for base in base_nodes:
            diff = field.sub(update, base)
            diff_square = field.mul(diff, diff)
            product_all = field.mul(product_all, diff_square)
            inverse_squares.append(field.inv(diff_square))
        update_to_all_base[update] = product_all
        update_to_base_inverse_squares[update] = inverse_squares

    base_indices = range(len(base_nodes))
    for update_count in range(1, len(update_nodes) + 1):
        if update_count > len(base_nodes):
            break
        total = field.zero
        for update_subset in combinations(update_nodes, update_count):
            update_vandermonde = vandermonde_square_field(list(update_subset), field)
            for removed_indices in combinations(base_indices, update_count):
                removed_nodes = [base_nodes[index] for index in removed_indices]
                removed_vandermonde = vandermonde_square_field(removed_nodes, field)
                numerator = update_vandermonde
                for update in update_subset:
                    update_product = update_to_all_base[update]
                    for index in removed_indices:
                        update_product = field.mul(
                            update_product,
                            update_to_base_inverse_squares[update][index],
                        )
                    numerator = field.mul(numerator, update_product)

                denominator_inverse = removed_vandermonde
                for index in removed_indices:
                    denominator_inverse = field.mul(
                        denominator_inverse, base_denominator_inverses[index]
                    )
                total = field.add(
                    total,
                    field.mul(c0, field.mul(numerator, denominator_inverse)),
                )
        coefficients[update_count] = total
    return coefficients


def field_batch_inverses(
    values: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    if not values:
        return []
    prefixes = []
    product_value = field.one
    normalized_values = [field.normalize(value) for value in values]
    for value in normalized_values:
        if field.is_zero(value):
            raise ZeroDivisionError("batch inversion of zero")
        prefixes.append(product_value)
        product_value = field.mul(product_value, value)
    inverse_product = field.inv(product_value)
    inverses = [field.zero] * len(normalized_values)
    for index in range(len(normalized_values) - 1, -1, -1):
        inverses[index] = field.mul(inverse_product, prefixes[index])
        inverse_product = field.mul(inverse_product, normalized_values[index])
    return inverses


def low_rank_lagrange_kernel_field(
    base_nodes: list[tuple[int, ...]],
    update_nodes: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[list[tuple[int, ...]]]:
    denominators = []
    for index, base in enumerate(base_nodes):
        denominator = field.one
        for other_index, other in enumerate(base_nodes):
            if other_index == index:
                continue
            denominator = field.mul(denominator, field.sub(base, other))
        denominators.append(denominator)
    denominator_inverses = field_batch_inverses(denominators, field)

    basis_values_by_update = []
    for update in update_nodes:
        update_differences = []
        product_all = field.one
        for base in base_nodes:
            difference = field.sub(update, base)
            update_differences.append(difference)
            product_all = field.mul(product_all, difference)
        difference_inverses = field_batch_inverses(update_differences, field)
        basis_values = []
        for difference_inverse, denominator_inverse in zip(
            difference_inverses, denominator_inverses
        ):
            basis_values.append(
                field.mul(
                    product_all,
                    field.mul(difference_inverse, denominator_inverse),
                )
            )
        basis_values_by_update.append(basis_values)

    kernel = []
    for left_values in basis_values_by_update:
        row = []
        for right_values in basis_values_by_update:
            entry = field.zero
            for left, right in zip(left_values, right_values):
                entry = field.add(entry, field.mul(left, right))
            row.append(entry)
        kernel.append(row)
    return kernel


def low_rank_compression_coefficients_field(
    base_nodes: list[tuple[int, ...]],
    update_nodes: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[list[tuple[int, ...]], dict[str, Any]]:
    """Return det(H_X)det(I+ZK) coefficients and sidecar data."""

    kernel = low_rank_lagrange_kernel_field(base_nodes, update_nodes, field)
    kernel_polynomial_matrix = [
        [
            [field.one if row == col else field.zero, kernel[row][col]]
            for col in range(len(update_nodes))
        ]
        for row in range(len(update_nodes))
    ]
    kernel_coefficients = fpoly_determinant(kernel_polynomial_matrix, field)
    base_determinant = vandermonde_square_field(base_nodes, field)
    hankel_coefficients = fpoly_scale(kernel_coefficients, base_determinant, field)
    sidecar = {
        "kind": "square_base_lagrange_kernel",
        "formula": "Delta(Z)=det(H_X) det(I+Z K), K_ab=sum_i L_i(y_a)L_i(y_b)",
        "base_node_count": len(base_nodes),
        "update_rank": len(update_nodes),
        "base_hankel_determinant": field.encode(base_determinant),
        "kernel": [[field.encode(entry) for entry in row] for row in kernel],
        "kernel_det_coefficients_ascending": [
            field.encode(coefficient) for coefficient in kernel_coefficients
        ],
        "hankel_coefficients_ascending": [
            field.encode(coefficient) for coefficient in hankel_coefficients
        ],
    }
    return hankel_coefficients, sidecar


def low_rank_update_data_field(
    spec: dict[str, Any],
    size: int,
    visible_length: int,
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[
    list[tuple[int, ...]],
    list[tuple[int, ...]],
    list[tuple[int, ...]],
    dict[str, Any],
]:
    data = spec.get("low_rank_update")
    if not isinstance(data, dict):
        raise ValueError("low_rank_update_bound needs low_rank_update metadata")
    base_encodings = data.get("base_node_encodings")
    if not isinstance(base_encodings, list):
        raise ValueError("low_rank_update.base_node_encodings must be a list")
    if len(base_encodings) != size:
        raise ValueError("low-rank update base-node count must equal minor size")
    update_encodings = data.get("update_node_encodings")
    if not isinstance(update_encodings, list) or not update_encodings:
        raise ValueError("low_rank_update.update_node_encodings must be a nonempty list")
    if not all(isinstance(value, int) for value in update_encodings):
        raise ValueError("low_rank_update.update_node_encodings must be integers")
    base_nodes = [field.decode(int(value)) for value in base_encodings]
    update_nodes = [field.decode(int(value)) for value in update_encodings]
    expected_u = one_spike_syndrome_field(base_nodes, visible_length, field)
    expected_v = one_spike_syndrome_field(update_nodes, visible_length, field)
    if u[:visible_length] != expected_u:
        raise ValueError("low_rank_update u moments do not match base nodes")
    if v[:visible_length] != expected_v:
        raise ValueError("low_rank_update v moments do not match update nodes")
    polynomial, compression_audit = low_rank_compression_coefficients_field(
        base_nodes, update_nodes, field
    )
    return base_nodes, update_nodes, polynomial, compression_audit


@dataclass(frozen=True)
class ExtractionResult:
    exact_agreement: int
    j: int
    t: int
    status: str
    row_set: list[int] | None
    polynomial: list[Any] | None
    roots: list[Any] | None
    enumerated_bad_slopes: list[Any] | None
    tested_row_sets: int
    row_set_source: str | None = None
    rank_pivot_node: Any | None = None
    rank_pivot_nodes_tested: int | None = None
    rank_pivot_nodes_required: int | None = None
    rank_pivot_test_nodes: list[Any] | None = None
    rank_pivot_witness_records: list[dict[str, Any]] | None = None
    residual_label: str | None = None
    residual_reason: str | None = None
    residual_audit: dict[str, Any] | None = None
    regular_minor_audit: dict[str, Any] | None = None
    minor_family_records: list[dict[str, Any]] | None = None


def candidate_row_sets(t: int, size: int, config: dict[str, Any]) -> list[list[int]]:
    explicit = config.get("candidate_row_sets")
    if explicit is not None:
        rows = [[int(value) for value in row_set] for row_set in explicit]
    else:
        strategy = config.get("type", "prefix")
        if strategy == "prefix":
            rows = [list(range(size))]
        elif strategy == "contiguous":
            limit = int(config.get("limit", max(0, t - size + 1)))
            rows = [
                list(range(start, start + size))
                for start in range(max(0, t - size + 1))
            ][:limit]
        else:
            raise ValueError(f"unknown row_set_strategy {strategy!r}")
    for row_set in rows:
        if len(row_set) != size:
            raise ValueError(("bad row_set size", row_set, size))
        if len(set(row_set)) != len(row_set):
            raise ValueError(("duplicate row in row_set", row_set))
        if min(row_set) < 0 or max(row_set) >= t:
            raise ValueError(("row_set outside Hankel row range", row_set, t))
    return rows


def full_rank_row_set_mod(
    matrix: list[list[int]], prime: int, size: int
) -> list[int] | None:
    basis: list[tuple[int, list[int]]] = []
    row_set: list[int] = []
    for row_index, row in enumerate(matrix):
        work = [entry % prime for entry in row]
        for pivot_col, basis_row in basis:
            if work[pivot_col] == 0:
                continue
            factor = work[pivot_col]
            work = [
                (work[col] - factor * basis_row[col]) % prime
                for col in range(size)
            ]
        pivot_col = next((col for col, value in enumerate(work) if value), None)
        if pivot_col is None:
            continue
        inv = pow(work[pivot_col], -1, prime)
        work = [(value * inv) % prime for value in work]
        basis.append((pivot_col, work))
        row_set.append(row_index)
        if len(row_set) == size:
            return row_set
    return None


def rank_pivot_row_sets_mod(
    u: list[int],
    v: list[int],
    t: int,
    size: int,
    prime: int,
) -> tuple[list[list[int]], dict[str, Any]]:
    if prime <= size:
        raise ValueError(
            f"rank_at_nodes needs at least size+1 distinct slopes, got {prime} <= {size}"
        )
    nodes = list(range(size + 1))
    for index, node in enumerate(nodes):
        matrix = matrix_at_slope(u, v, list(range(t)), size, node, prime)
        row_set = full_rank_row_set_mod(matrix, prime, size)
        if row_set is not None:
            return [row_set], {
                "source": "rank_at_nodes",
                "node": node,
                "nodes_tested": index + 1,
                "nodes_required_for_singularity_proof": size + 1,
            }
    return [], {
        "source": "rank_at_nodes",
        "node": None,
        "nodes_tested": len(nodes),
        "nodes_required_for_singularity_proof": size + 1,
        "singularity_proof": (
            "all maximal minors have degree <= size and vanish at size+1 "
            "distinct slopes, so they vanish identically"
        ),
    }


def rank_node_family_row_sets_mod(
    u: list[int],
    v: list[int],
    t: int,
    size: int,
    prime: int,
    config: dict[str, Any],
) -> tuple[list[list[int]], dict[str, Any]]:
    if prime <= size:
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} needs at least size+1 distinct "
            f"slopes, got {prime} <= {size}"
        )
    required = size + 1
    node_limit = int(config.get("node_limit", required))
    if node_limit < required:
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} node_limit must be at least "
            f"size+1={required}"
        )
    if node_limit > prime:
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} node_limit={node_limit} exceeds "
            f"field size {prime}"
        )
    row_sets_by_key: dict[tuple[int, ...], list[int]] = {}
    witness_records: list[dict[str, Any]] = []
    first_node: int | None = None
    nodes = list(range(node_limit))
    for node in nodes:
        matrix = matrix_at_slope(u, v, list(range(t)), size, node, prime)
        row_set = full_rank_row_set_mod(matrix, prime, size)
        if row_set is None:
            continue
        if first_node is None:
            first_node = node
        key = tuple(row_set)
        if key in row_sets_by_key:
            continue
        row_sets_by_key[key] = row_set
        witness_records.append({"node": node, "row_set": row_set})
    if row_sets_by_key:
        return list(row_sets_by_key.values()), {
            "source": RANK_AT_NODES_FAMILY_STRATEGY,
            "node": first_node,
            "nodes_tested": len(nodes),
            "nodes_required_for_singularity_proof": required,
            "test_nodes": nodes,
            "witness_records": witness_records,
        }
    return [], {
        "source": RANK_AT_NODES_FAMILY_STRATEGY,
        "node": None,
        "nodes_tested": len(nodes),
        "nodes_required_for_singularity_proof": required,
        "test_nodes": nodes,
        "witness_records": [],
        "singularity_proof": (
            "all maximal minors have degree <= size and vanish at size+1 "
            "distinct slopes, so they vanish identically"
        ),
    }


def full_rank_row_set_field(
    matrix: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
    size: int,
) -> list[int] | None:
    basis: list[tuple[int, list[tuple[int, ...]]]] = []
    row_set: list[int] = []
    for row_index, row in enumerate(matrix):
        work = [field.normalize(entry) for entry in row]
        for pivot_col, basis_row in basis:
            if field.is_zero(work[pivot_col]):
                continue
            factor = work[pivot_col]
            work = [
                field.sub(work[col], field.mul(factor, basis_row[col]))
                for col in range(size)
            ]
        pivot_col = next(
            (col for col, value in enumerate(work) if not field.is_zero(value)),
            None,
        )
        if pivot_col is None:
            continue
        inv = field.inv(work[pivot_col])
        work = [field.mul(value, inv) for value in work]
        basis.append((pivot_col, work))
        row_set.append(row_index)
        if len(row_set) == size:
            return row_set
    return None


def rank_pivot_row_sets_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    t: int,
    size: int,
    field: PolynomialBasisField,
) -> tuple[list[list[int]], dict[str, Any]]:
    if field.size <= size:
        raise ValueError(
            f"rank_at_nodes needs at least size+1 distinct slopes, got {field.size} <= {size}"
        )
    nodes = [field.decode(index) for index in range(size + 1)]
    for index, node in enumerate(nodes):
        matrix = matrix_at_slope_field(u, v, list(range(t)), size, node, field)
        row_set = full_rank_row_set_field(matrix, field, size)
        if row_set is not None:
            return [row_set], {
                "source": "rank_at_nodes",
                "node": field.encode(node),
                "nodes_tested": index + 1,
                "nodes_required_for_singularity_proof": size + 1,
                "field_encoding": "base-p low-to-high integer",
            }
    return [], {
        "source": "rank_at_nodes",
        "node": None,
        "nodes_tested": len(nodes),
        "nodes_required_for_singularity_proof": size + 1,
        "field_encoding": "base-p low-to-high integer",
        "singularity_proof": (
            "all maximal minors have degree <= size and vanish at size+1 "
            "distinct slopes, so they vanish identically"
        ),
    }


def rank_node_family_row_sets_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    t: int,
    size: int,
    field: PolynomialBasisField,
    config: dict[str, Any],
) -> tuple[list[list[int]], dict[str, Any]]:
    if field.size <= size:
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} needs at least size+1 distinct "
            f"slopes, got {field.size} <= {size}"
        )
    required = size + 1
    node_limit = int(config.get("node_limit", required))
    if node_limit < required:
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} node_limit must be at least "
            f"size+1={required}"
        )
    if node_limit > field.size:
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} node_limit={node_limit} exceeds "
            f"field size {field.size}"
        )
    row_sets_by_key: dict[tuple[int, ...], list[int]] = {}
    witness_records: list[dict[str, Any]] = []
    first_node: int | None = None
    node_encodings = list(range(node_limit))
    for node_encoding in node_encodings:
        node = field.decode(node_encoding)
        matrix = matrix_at_slope_field(u, v, list(range(t)), size, node, field)
        row_set = full_rank_row_set_field(matrix, field, size)
        if row_set is None:
            continue
        if first_node is None:
            first_node = node_encoding
        key = tuple(row_set)
        if key in row_sets_by_key:
            continue
        row_sets_by_key[key] = row_set
        witness_records.append({"node": node_encoding, "row_set": row_set})
    if row_sets_by_key:
        return list(row_sets_by_key.values()), {
            "source": RANK_AT_NODES_FAMILY_STRATEGY,
            "node": first_node,
            "nodes_tested": len(node_encodings),
            "nodes_required_for_singularity_proof": required,
            "test_nodes": node_encodings,
            "witness_records": witness_records,
            "field_encoding": "base-p low-to-high integer",
        }
    return [], {
        "source": RANK_AT_NODES_FAMILY_STRATEGY,
        "node": None,
        "nodes_tested": len(node_encodings),
        "nodes_required_for_singularity_proof": required,
        "test_nodes": node_encodings,
        "witness_records": [],
        "field_encoding": "base-p low-to-high integer",
        "singularity_proof": (
            "all maximal minors have degree <= size and vanish at size+1 "
            "distinct slopes, so they vanish identically"
        ),
    }


def visible_proportional_scalar_mod(
    u: list[int],
    v: list[int],
    visible_length: int,
    prime: int,
) -> int | None:
    scalar: int | None = None
    for index in range(visible_length):
        u_i = u[index] % prime
        v_i = v[index] % prime
        if v_i == 0:
            if u_i != 0:
                return None
            continue
        candidate = (u_i * pow(v_i, -1, prime)) % prime
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return None
    return scalar


def proportional_residual_audit_mod(
    spec: dict[str, Any],
    u: list[int],
    v: list[int],
    visible_length: int,
    prime: int,
) -> dict[str, Any] | None:
    scalar = visible_proportional_scalar_mod(u, v, visible_length, prime)
    if scalar is None:
        return None
    full_proportional = len(u) == len(v) and all(
        (u_i - scalar * v_i) % prime == 0 for u_i, v_i in zip(u, v)
    )
    tangent_root = (-scalar) % prime
    declared_tangent_root = spec["line_syndrome"].get("tangent_root")
    if (
        declared_tangent_root is not None
        and int(declared_tangent_root) % prime != tangent_root
    ):
        raise ValueError("declared tangent_root does not match u=c*v")
    can_charge_tangent = full_proportional
    return {
        "residual_classification": "proportional_window_tangent"
        if can_charge_tangent
        else "proportional_window_single_slope",
        "scalar_multiple_u_over_v": scalar,
        "residual_single_slope": tangent_root,
        "full_syndrome_proportional": full_proportional,
        "residual_charge": "tangent_common_code_line"
        if can_charge_tangent
        else "tail_check_required",
    }


def visible_proportional_scalar_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    visible_length: int,
    field: PolynomialBasisField,
) -> tuple[int, ...] | None:
    scalar: tuple[int, ...] | None = None
    for index in range(visible_length):
        u_i = u[index]
        v_i = v[index]
        if v_i == field.zero:
            if u_i != field.zero:
                return None
            continue
        candidate = field.mul(u_i, field.inv(v_i))
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return None
    return scalar


def proportional_residual_audit_field(
    spec: dict[str, Any],
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    visible_length: int,
    field: PolynomialBasisField,
) -> dict[str, Any] | None:
    scalar = visible_proportional_scalar_field(u, v, visible_length, field)
    if scalar is None:
        return None
    full_proportional = len(u) == len(v) and all(
        field.sub(u_i, field.mul(scalar, v_i)) == field.zero
        for u_i, v_i in zip(u, v)
    )
    tangent_root = field.encode(field.neg(scalar))
    declared_tangent_root = spec["line_syndrome"].get("tangent_root")
    if (
        declared_tangent_root is not None
        and int(declared_tangent_root) != tangent_root
    ):
        raise ValueError("declared tangent_root does not match u=c*v")
    can_charge_tangent = full_proportional
    return {
        "residual_classification": "proportional_window_tangent"
        if can_charge_tangent
        else "proportional_window_single_slope",
        "scalar_multiple_u_over_v": field.encode(scalar),
        "residual_single_slope": tangent_root,
        "full_syndrome_proportional": full_proportional,
        "residual_charge": "tangent_common_code_line"
        if can_charge_tangent
        else "tail_check_required",
    }


def proportional_residual_label(audit: dict[str, Any] | None) -> str:
    if audit and audit.get("residual_charge") == "tangent_common_code_line":
        return "tangent"
    return "unknown"


def proportional_residual_reason(
    base_reason: str,
    audit: dict[str, Any] | None,
) -> str:
    if audit is None:
        return base_reason
    tail = (
        "classifies the residual as tangent/common-code-line"
        if audit["residual_charge"] == "tangent_common_code_line"
        else (
            "compresses the residual to one slope, but a tail check is needed "
            "before tangent charging"
        )
    )
    return (
        base_reason
        + "; visible Hankel window is proportional; the proportional-window "
        "lemma "
        + tail
    )


def add_rank_pivot_test_nodes(audit: dict[str, Any]) -> None:
    source = audit.get("row_set_source")
    if not isinstance(source, str) or not source.startswith("rank_at_nodes"):
        return
    if "rank_pivot_test_nodes" in audit:
        return
    tested = audit.get("rank_pivot_nodes_tested")
    if isinstance(tested, int):
        audit["rank_pivot_test_nodes"] = list(range(tested))


def extract_for_agreement(
    spec: dict[str, Any],
    exact_agreement: int,
    prime: int,
) -> ExtractionResult:
    row = spec["row"]
    n = int(row["n"])
    k = int(row["k"])
    u = [value % prime for value in spec["line_syndrome"]["u"]]
    v = [value % prime for value in spec["line_syndrome"]["v"]]
    j = n - exact_agreement
    t = exact_agreement - k
    size = j + 1
    if t < size:
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "residual_obstruction",
            None,
            None,
            None,
            None,
            0,
            residual_label="unknown",
            residual_reason="regular overdetermined condition t>=j+1 fails",
        )
    if len(u) < t + j or len(v) < t + j:
        raise ValueError(
            f"syndrome length must be at least t+j={t + j} for A={exact_agreement}"
        )

    row_config = spec.get("row_set_strategy", {"type": "prefix"})
    if (
        row_config.get("type") == RANK_AT_NODES_FAMILY_STRATEGY
        and spec.get("certificate_mode") != MINOR_GCD_MODE
    ):
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} is only supported with "
            f"certificate_mode={MINOR_GCD_MODE}"
        )
    if row_config.get("type") == "rank_at_nodes":
        row_sets, row_set_audit = rank_pivot_row_sets_mod(u, v, t, size, prime)
    elif row_config.get("type") == RANK_AT_NODES_FAMILY_STRATEGY:
        row_sets, row_set_audit = rank_node_family_row_sets_mod(
            u, v, t, size, prime, row_config
        )
    else:
        row_sets = candidate_row_sets(t, size, row_config)
        row_set_audit = {
            "source": row_config.get("type", "prefix"),
            "node": None,
            "nodes_tested": None,
        }
    if spec.get("certificate_mode") in {ONE_SPIKE_LINEAR_MODE, LOW_RANK_UPDATE_MODE}:
        raise ValueError(
            f"{spec.get('certificate_mode')} currently requires a "
            "polynomial-basis field_model"
        )
    if spec.get("certificate_mode") in {ZERO_U_MONOMIAL_MODE, SCALAR_MULTIPLE_MODE}:
        scalar = 0
        if spec.get("certificate_mode") == SCALAR_MULTIPLE_MODE:
            scalar = int(spec["line_syndrome"]["scalar_multiple_u_over_v"]) % prime
        proportional_audit = proportional_residual_audit_mod(
            spec, u, v, t + j, prime
        )
        if (
            proportional_audit is None
            or proportional_audit["scalar_multiple_u_over_v"] != scalar
        ):
            raise ValueError("scalar-multiple closed-form roots need u=c*v on the visible window")
        tested = 0
        for row_set in row_sets:
            tested += 1
            leading = determinant_mod(
                [[v[row + col] % prime for col in range(size)] for row in row_set],
                prime,
            )
            if leading == 0:
                continue
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "regular_minor",
                row_set,
                poly_scale(linear_power_mod(scalar, size, prime), leading, prime),
                [(-scalar) % prime],
                None,
                tested,
                row_set_source=row_set_audit["source"],
                rank_pivot_node=row_set_audit.get("node"),
                rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
                rank_pivot_nodes_required=row_set_audit.get(
                    "nodes_required_for_singularity_proof"
                ),
            )
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "residual_obstruction",
            None,
            None,
            None,
            None,
            tested,
            row_set_source=row_set_audit["source"],
            rank_pivot_node=row_set_audit.get("node"),
            rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
            rank_pivot_nodes_required=row_set_audit.get(
                "nodes_required_for_singularity_proof"
            ),
            residual_label=proportional_residual_label(proportional_audit),
            residual_reason=proportional_residual_reason(
                row_set_audit.get("singularity_proof")
                or "all tested scalar-multiple leading coefficients vanished",
                proportional_audit,
            ),
            residual_audit=proportional_audit,
        )
    if spec.get("certificate_mode") == MINOR_GCD_MODE:
        row_set_source = f"{row_set_audit['source']}_minor_gcd"
        if spec.get("minor_gcd_method") == ZERO_U_GCD_METHOD:
            row_set_source += f"_{ZERO_U_GCD_METHOD}"
            polynomials, family_records = zero_u_monomial_minor_records_mod(
                u, v, row_sets, t + j, size, prime
            )
        else:
            polynomials = []
            family_records = []
            for row_set in row_sets:
                polynomial = determinant_polynomial_by_interpolation(
                    u, v, row_set, size, prime
                )
                polynomial = trim(polynomial, prime)
                polynomials.append(polynomial)
                family_records.append(
                    {
                        "row_set": row_set,
                        "coefficients": polynomial,
                        "degree": poly_degree(polynomial, prime)
                        if polynomial != [0]
                        else -1,
                    }
                )
        nonzero_polynomials = [
            polynomial for polynomial in polynomials if polynomial != [0]
        ]
        if nonzero_polynomials:
            gcd_polynomial = poly_gcd_many(nonzero_polynomials, prime)
            roots: list[int] | None = None
            bad_slopes: list[int] | None = None
            if (
                spec.get("minor_gcd_method") == ZERO_U_GCD_METHOD
                and gcd_polynomial == [0] * size + [1]
            ):
                roots = [0]
            elif prime <= int(
                spec.get("max_root_enum_field_size", DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE)
            ):
                roots = [
                    value
                    for value in range(prime)
                    if poly_eval(gcd_polynomial, value, prime) == 0
                ]
            domain = spec.get("row", {}).get("domain")
            if domain is not None and spec.get("enumerate_split_bad_slopes", False):
                domain_values = [int(value) % prime for value in domain]
                subset_count = n_choose_k(len(domain_values), j)
                if subset_count <= int(
                    spec.get(
                        "max_bad_slope_subsets", DEFAULT_MAX_BAD_SLOPE_SUBSETS
                    )
                ):
                    bad_slopes = finite_bad_slopes_for_exact_agreement(
                        u,
                        v,
                        domain_values,
                        n,
                        k,
                        exact_agreement,
                        prime,
                    )
                    if roots is not None and not set(bad_slopes).issubset(roots):
                        raise AssertionError(
                            (
                                "bad slopes not contained in common gcd roots",
                                exact_agreement,
                            )
                        )
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "regular_minor",
                None,
                gcd_polynomial,
                roots,
                bad_slopes,
                len(row_sets),
                row_set_source=row_set_source,
                rank_pivot_node=row_set_audit.get("node"),
                rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
                rank_pivot_nodes_required=row_set_audit.get(
                    "nodes_required_for_singularity_proof"
                ),
                rank_pivot_test_nodes=row_set_audit.get("test_nodes"),
                rank_pivot_witness_records=row_set_audit.get("witness_records"),
                minor_family_records=family_records,
            )
        residual_reason = row_set_audit.get(
            "singularity_proof"
        ) or "all audited maximal-minor determinant polynomials vanished"
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "residual_obstruction",
            None,
            None,
            None,
            None,
            len(row_sets),
            row_set_source=row_set_source,
            rank_pivot_node=row_set_audit.get("node"),
            rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
            rank_pivot_nodes_required=row_set_audit.get(
                "nodes_required_for_singularity_proof"
            ),
            rank_pivot_test_nodes=row_set_audit.get("test_nodes"),
            rank_pivot_witness_records=row_set_audit.get("witness_records"),
            residual_label="unknown",
            residual_reason=residual_reason,
        )
    if (
        spec.get("certificate_mode") == "rank_witness_bound"
        and row_set_audit["source"] == "rank_at_nodes"
        and row_sets
    ):
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "regular_minor",
            row_sets[0],
            None,
            None,
            None,
            1,
            row_set_source=row_set_audit["source"],
            rank_pivot_node=row_set_audit.get("node"),
            rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
            rank_pivot_nodes_required=row_set_audit.get(
                "nodes_required_for_singularity_proof"
            ),
        )
    tested = 0
    for row_set in row_sets:
        tested += 1
        polynomial = determinant_polynomial_by_interpolation(
            u, v, row_set, size, prime
        )
        if any(coeff % prime for coeff in polynomial):
            roots: list[int] | None = None
            bad_slopes: list[int] | None = None
            if prime <= int(
                spec.get("max_root_enum_field_size", DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE)
            ):
                roots = [
                    value
                    for value in range(prime)
                    if poly_eval(polynomial, value, prime) == 0
                ]
            domain = spec.get("row", {}).get("domain")
            if domain is not None and spec.get("enumerate_split_bad_slopes", False):
                domain_values = [int(value) % prime for value in domain]
                subset_count = n_choose_k(len(domain_values), j)
                if subset_count <= int(
                    spec.get(
                        "max_bad_slope_subsets", DEFAULT_MAX_BAD_SLOPE_SUBSETS
                    )
                ):
                    bad_slopes = finite_bad_slopes_for_exact_agreement(
                        u,
                        v,
                        domain_values,
                        n,
                        k,
                        exact_agreement,
                        prime,
                    )
                    if roots is not None and not set(bad_slopes).issubset(roots):
                        raise AssertionError(
                            ("bad slopes not contained in roots", exact_agreement)
                        )
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "regular_minor",
                row_set,
                polynomial,
                roots,
                bad_slopes,
                tested,
                row_set_source=row_set_audit["source"],
                rank_pivot_node=row_set_audit.get("node"),
                rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
                rank_pivot_nodes_required=row_set_audit.get(
                    "nodes_required_for_singularity_proof"
                ),
            )

    residual_reason = row_set_audit.get(
        "singularity_proof"
    ) or "all tested regular maximal minors vanished"
    proportional_audit = proportional_residual_audit_mod(spec, u, v, t + j, prime)
    return ExtractionResult(
        exact_agreement,
        j,
        t,
        "residual_obstruction",
        None,
        None,
        None,
        None,
        tested,
        row_set_source=row_set_audit["source"],
        rank_pivot_node=row_set_audit.get("node"),
        rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
        rank_pivot_nodes_required=row_set_audit.get(
            "nodes_required_for_singularity_proof"
        ),
        residual_label=proportional_residual_label(proportional_audit),
        residual_reason=proportional_residual_reason(
            residual_reason, proportional_audit
        ),
        residual_audit=proportional_audit,
    )


def extract_for_agreement_field(
    spec: dict[str, Any],
    exact_agreement: int,
    field: PolynomialBasisField,
) -> ExtractionResult:
    row = spec["row"]
    n = int(row["n"])
    k = int(row["k"])
    syndrome = spec["line_syndrome"]
    syndrome_encoding = syndrome.get("field_encoding", spec.get("field_element_encoding"))
    u = normalize_field_input_list(syndrome["u"], field, syndrome_encoding)
    v = normalize_field_input_list(syndrome["v"], field, syndrome_encoding)
    j = n - exact_agreement
    t = exact_agreement - k
    size = j + 1
    if t < size:
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "residual_obstruction",
            None,
            None,
            None,
            None,
            0,
            residual_label="unknown",
            residual_reason="regular overdetermined condition t>=j+1 fails",
        )
    if len(u) < t + j or len(v) < t + j:
        raise ValueError(
            f"syndrome length must be at least t+j={t + j} for A={exact_agreement}"
        )

    row_config = spec.get("row_set_strategy", {"type": "prefix"})
    if (
        row_config.get("type") == RANK_AT_NODES_FAMILY_STRATEGY
        and spec.get("certificate_mode") != MINOR_GCD_MODE
    ):
        raise ValueError(
            f"{RANK_AT_NODES_FAMILY_STRATEGY} is only supported with "
            f"certificate_mode={MINOR_GCD_MODE}"
        )
    if row_config.get("type") == "rank_at_nodes":
        row_sets, row_set_audit = rank_pivot_row_sets_field(u, v, t, size, field)
    elif row_config.get("type") == RANK_AT_NODES_FAMILY_STRATEGY:
        row_sets, row_set_audit = rank_node_family_row_sets_field(
            u, v, t, size, field, row_config
        )
    else:
        row_sets = candidate_row_sets(t, size, row_config)
        row_set_audit = {
            "source": row_config.get("type", "prefix"),
            "node": None,
            "nodes_tested": None,
        }
    if spec.get("certificate_mode") == ONE_SPIKE_LINEAR_MODE:
        row_set = list(range(size))
        _base_nodes, _spike, polynomial = one_spike_linear_data_field(
            spec, size, t + j, u, v, field
        )
        if field.is_zero(polynomial[1]):
            roots = [] if not field.is_zero(polynomial[0]) else None
        else:
            roots = [field.neg(field.div(polynomial[0], polynomial[1]))]
        if roots is None:
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "residual_obstruction",
                None,
                None,
                None,
                None,
                1,
                row_set_source="one_spike_linear_prefix",
                residual_label="unknown",
                residual_reason=(
                    "one-spike linear determinant has zero constant and linear "
                    "coefficients for the prefix row set"
                ),
            )
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "regular_minor",
            row_set,
            polynomial,
            roots,
            None,
            1,
            row_set_source="one_spike_linear_prefix",
        )
    if spec.get("certificate_mode") == LOW_RANK_UPDATE_MODE:
        row_set = list(range(size))
        base_nodes, update_nodes, polynomial, compression_audit = (
            low_rank_update_data_field(
                spec, size, t + j, u, v, field
            )
        )
        if fpoly_is_zero(polynomial, field):
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "residual_obstruction",
                None,
                None,
                None,
                None,
                1,
                row_set_source="low_rank_update_prefix",
                residual_label="unknown",
                residual_reason=(
                    "low-rank update determinant vanished identically for "
                    "the prefix row set"
                ),
                regular_minor_audit=compression_audit,
            )
        roots = (
            quadratic_roots_field(polynomial, field)
            if len(update_nodes) == 2
            else None
        )
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "regular_minor",
            row_set,
            polynomial,
            roots,
            None,
            1,
            row_set_source=f"low_rank_update_prefix_rank{len(update_nodes)}",
            regular_minor_audit=compression_audit,
        )
    if spec.get("certificate_mode") in {ZERO_U_MONOMIAL_MODE, SCALAR_MULTIPLE_MODE}:
        scalar = field.zero
        if spec.get("certificate_mode") == SCALAR_MULTIPLE_MODE:
            scalar = normalize_field_input_value(
                spec["line_syndrome"]["scalar_multiple_u_over_v"],
                field,
                syndrome_encoding,
            )
        proportional_audit = proportional_residual_audit_field(
            spec, u, v, t + j, field
        )
        if (
            proportional_audit is None
            or proportional_audit["scalar_multiple_u_over_v"] != field.encode(scalar)
        ):
            raise ValueError("scalar-multiple closed-form roots need u=c*v on the visible window")
        tested = 0
        for row_set in row_sets:
            tested += 1
            leading = determinant_field(
                [[v[row + col] for col in range(size)] for row in row_set],
                field,
            )
            if field.is_zero(leading):
                continue
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "regular_minor",
                row_set,
                fpoly_scale(fpoly_linear_power(scalar, size, field), leading, field),
                [field.neg(scalar)],
                None,
                tested,
                row_set_source=row_set_audit["source"],
                rank_pivot_node=row_set_audit.get("node"),
                rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
                rank_pivot_nodes_required=row_set_audit.get(
                    "nodes_required_for_singularity_proof"
                ),
            )
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "residual_obstruction",
            None,
            None,
            None,
            None,
            tested,
            row_set_source=row_set_audit["source"],
            rank_pivot_node=row_set_audit.get("node"),
            rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
            rank_pivot_nodes_required=row_set_audit.get(
                "nodes_required_for_singularity_proof"
            ),
            residual_label=proportional_residual_label(proportional_audit),
            residual_reason=proportional_residual_reason(
                row_set_audit.get("singularity_proof")
                or "all tested scalar-multiple leading coefficients vanished",
                proportional_audit,
            ),
            residual_audit=proportional_audit,
        )
    if spec.get("certificate_mode") == MINOR_GCD_MODE:
        row_set_source = f"{row_set_audit['source']}_minor_gcd"
        if spec.get("minor_gcd_method") == ZERO_U_GCD_METHOD:
            row_set_source += f"_{ZERO_U_GCD_METHOD}"
            polynomials, family_records = zero_u_monomial_minor_records_field(
                u, v, row_sets, t + j, size, field
            )
        else:
            polynomials = []
            family_records = []
            for row_set in row_sets:
                polynomial = determinant_polynomial_by_interpolation_field(
                    u, v, row_set, size, field
                )
                polynomial = fpoly_trim(polynomial, field)
                polynomials.append(polynomial)
                family_records.append(
                    {
                        "row_set": row_set,
                        "coefficients": polynomial,
                        "degree": fpoly_degree(polynomial, field)
                        if not fpoly_is_zero(polynomial, field)
                        else -1,
                    }
                )
        nonzero_polynomials = [
            polynomial for polynomial in polynomials if not fpoly_is_zero(polynomial, field)
        ]
        if nonzero_polynomials:
            gcd_polynomial = fpoly_gcd_many(nonzero_polynomials, field)
            roots: list[tuple[int, ...]] | None = None
            bad_slopes: list[tuple[int, ...]] | None = None
            if (
                spec.get("minor_gcd_method") == ZERO_U_GCD_METHOD
                and gcd_polynomial == [field.zero] * size + [field.one]
            ):
                roots = [field.zero]
            elif field.size <= int(
                spec.get("max_root_enum_field_size", DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE)
            ):
                roots = [
                    value
                    for value in field.elements()
                    if field.is_zero(fpoly_eval(gcd_polynomial, value, field))
                ]
            domain = spec.get("row", {}).get("domain")
            if domain is not None and spec.get("enumerate_split_bad_slopes", False):
                domain_encoding = spec.get("row", {}).get(
                    "field_encoding", spec.get("field_element_encoding")
                )
                domain_values = normalize_field_input_list(
                    domain, field, domain_encoding
                )
                subset_count = n_choose_k(len(domain_values), j)
                if subset_count <= int(
                    spec.get(
                        "max_bad_slope_subsets", DEFAULT_MAX_BAD_SLOPE_SUBSETS
                    )
                ):
                    bad_slopes = finite_bad_slopes_for_exact_agreement_field(
                        u,
                        v,
                        domain_values,
                        n,
                        k,
                        exact_agreement,
                        field,
                    )
                    if roots is not None:
                        root_codes = {field.encode(root) for root in roots}
                        bad_codes = {field.encode(slope) for slope in bad_slopes}
                        if not bad_codes.issubset(root_codes):
                            raise AssertionError(
                                (
                                    "bad slopes not contained in common gcd roots",
                                    exact_agreement,
                                )
                            )
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "regular_minor",
                None,
                gcd_polynomial,
                roots,
                bad_slopes,
                len(row_sets),
                row_set_source=row_set_source,
                rank_pivot_node=row_set_audit.get("node"),
                rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
                rank_pivot_nodes_required=row_set_audit.get(
                    "nodes_required_for_singularity_proof"
                ),
                rank_pivot_test_nodes=row_set_audit.get("test_nodes"),
                rank_pivot_witness_records=row_set_audit.get("witness_records"),
                minor_family_records=family_records,
            )
        residual_reason = row_set_audit.get(
            "singularity_proof"
        ) or "all audited maximal-minor determinant polynomials vanished"
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "residual_obstruction",
            None,
            None,
            None,
            None,
            len(row_sets),
            row_set_source=row_set_source,
            rank_pivot_node=row_set_audit.get("node"),
            rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
            rank_pivot_nodes_required=row_set_audit.get(
                "nodes_required_for_singularity_proof"
            ),
            rank_pivot_test_nodes=row_set_audit.get("test_nodes"),
            rank_pivot_witness_records=row_set_audit.get("witness_records"),
            residual_label="unknown",
            residual_reason=residual_reason,
        )
    if (
        spec.get("certificate_mode") == "rank_witness_bound"
        and row_set_audit["source"] == "rank_at_nodes"
        and row_sets
    ):
        return ExtractionResult(
            exact_agreement,
            j,
            t,
            "regular_minor",
            row_sets[0],
            None,
            None,
            None,
            1,
            row_set_source=row_set_audit["source"],
            rank_pivot_node=row_set_audit.get("node"),
            rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
            rank_pivot_nodes_required=row_set_audit.get(
                "nodes_required_for_singularity_proof"
            ),
        )
    tested = 0
    for row_set in row_sets:
        tested += 1
        polynomial = determinant_polynomial_by_interpolation_field(
            u, v, row_set, size, field
        )
        if any(not field.is_zero(coeff) for coeff in polynomial):
            roots: list[tuple[int, ...]] | None = None
            bad_slopes: list[tuple[int, ...]] | None = None
            if field.size <= int(
                spec.get("max_root_enum_field_size", DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE)
            ):
                roots = [
                    value
                    for value in field.elements()
                    if field.is_zero(fpoly_eval(polynomial, value, field))
                ]
            domain = spec.get("row", {}).get("domain")
            if domain is not None and spec.get("enumerate_split_bad_slopes", False):
                domain_encoding = spec.get("row", {}).get(
                    "field_encoding", spec.get("field_element_encoding")
                )
                domain_values = normalize_field_input_list(
                    domain, field, domain_encoding
                )
                subset_count = n_choose_k(len(domain_values), j)
                if subset_count <= int(
                    spec.get(
                        "max_bad_slope_subsets", DEFAULT_MAX_BAD_SLOPE_SUBSETS
                    )
                ):
                    bad_slopes = finite_bad_slopes_for_exact_agreement_field(
                        u,
                        v,
                        domain_values,
                        n,
                        k,
                        exact_agreement,
                        field,
                    )
                    if roots is not None:
                        root_codes = {field.encode(root) for root in roots}
                        bad_codes = {field.encode(slope) for slope in bad_slopes}
                        if not bad_codes.issubset(root_codes):
                            raise AssertionError(
                                ("bad slopes not contained in roots", exact_agreement)
                            )
            return ExtractionResult(
                exact_agreement,
                j,
                t,
                "regular_minor",
                row_set,
                polynomial,
                roots,
                bad_slopes,
                tested,
                row_set_source=row_set_audit["source"],
                rank_pivot_node=row_set_audit.get("node"),
                rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
                rank_pivot_nodes_required=row_set_audit.get(
                    "nodes_required_for_singularity_proof"
                ),
            )

    residual_reason = row_set_audit.get(
        "singularity_proof"
    ) or "all tested regular maximal minors vanished"
    proportional_audit = proportional_residual_audit_field(spec, u, v, t + j, field)
    return ExtractionResult(
        exact_agreement,
        j,
        t,
        "residual_obstruction",
        None,
        None,
        None,
        None,
        tested,
        row_set_source=row_set_audit["source"],
        rank_pivot_node=row_set_audit.get("node"),
        rank_pivot_nodes_tested=row_set_audit.get("nodes_tested"),
        rank_pivot_nodes_required=row_set_audit.get(
            "nodes_required_for_singularity_proof"
        ),
        residual_label=proportional_residual_label(proportional_audit),
        residual_reason=proportional_residual_reason(
            residual_reason, proportional_audit
        ),
        residual_audit=proportional_audit,
    )


def prime_projective_infinity_audit(
    result: ExtractionResult,
    prime: int,
) -> dict[str, Any]:
    top_degree = result.j + 1
    assert result.polynomial is not None
    top_coefficient = (
        result.polynomial[top_degree] % prime
        if top_degree < len(result.polynomial)
        else 0
    )
    status = "empty" if top_coefficient != 0 else "nonempty"
    return {
        "projective_point": "[0:1]",
        "status": status,
        "top_degree": top_degree,
        "top_coefficient": top_coefficient,
        "contribution": 0 if status == "empty" else 1,
        "reason": (
            "homogenized regular-minor determinant evaluates to its top "
            "finite-patch coefficient at projective infinity"
        ),
    }


def prime_projective_infinity_gcd_audit(
    result: ExtractionResult,
    prime: int,
) -> dict[str, Any]:
    top_degree = result.j + 1
    assert result.minor_family_records is not None
    top_records = []
    first_nonzero: int | None = None
    for record in result.minor_family_records:
        coefficients = record["coefficients"]
        top_coefficient = (
            coefficients[top_degree] % prime if top_degree < len(coefficients) else 0
        )
        if top_coefficient and first_nonzero is None:
            first_nonzero = top_coefficient
        top_records.append(
            {
                "row_set": record["row_set"],
                "top_coefficient": top_coefficient,
            }
        )
    status = "empty" if first_nonzero is not None else "nonempty"
    return {
        "projective_point": "[0:1]",
        "status": status,
        "top_degree": top_degree,
        "top_coefficient": first_nonzero or 0,
        "top_coefficients": top_records,
        "contribution": 0 if status == "empty" else 1,
        "reason": (
            "projective infinity is excluded exactly when at least one audited "
            "maximal-minor homogenization has nonzero top coefficient"
        ),
    }


def field_projective_infinity_audit(
    result: ExtractionResult,
    field: PolynomialBasisField,
) -> dict[str, Any]:
    top_degree = result.j + 1
    assert result.polynomial is not None
    top_coefficient = (
        field.normalize(result.polynomial[top_degree])
        if top_degree < len(result.polynomial)
        else field.zero
    )
    status = "empty" if not field.is_zero(top_coefficient) else "nonempty"
    return {
        "projective_point": "[0:1]",
        "status": status,
        "top_degree": top_degree,
        "top_coefficient": field.encode(top_coefficient),
        "field_encoding": "base-p low-to-high integer",
        "contribution": 0 if status == "empty" else 1,
        "reason": (
            "homogenized regular-minor determinant evaluates to its top "
            "finite-patch coefficient at projective infinity"
        ),
    }


def field_projective_infinity_gcd_audit(
    result: ExtractionResult,
    field: PolynomialBasisField,
) -> dict[str, Any]:
    top_degree = result.j + 1
    assert result.minor_family_records is not None
    top_records = []
    first_nonzero: tuple[int, ...] | None = None
    for record in result.minor_family_records:
        coefficients = record["coefficients"]
        top_coefficient = (
            field.normalize(coefficients[top_degree])
            if top_degree < len(coefficients)
            else field.zero
        )
        if not field.is_zero(top_coefficient) and first_nonzero is None:
            first_nonzero = top_coefficient
        top_records.append(
            {
                "row_set": record["row_set"],
                "top_coefficient": field.encode(top_coefficient),
            }
        )
    status = "empty" if first_nonzero is not None else "nonempty"
    return {
        "projective_point": "[0:1]",
        "status": status,
        "top_degree": top_degree,
        "top_coefficient": field.encode(first_nonzero or field.zero),
        "top_coefficients": top_records,
        "field_encoding": "base-p low-to-high integer",
        "contribution": 0 if status == "empty" else 1,
        "reason": (
            "projective infinity is excluded exactly when at least one audited "
            "maximal-minor homogenization has nonzero top coefficient"
        ),
    }


def projective_infinity_union_count(items: list[dict[str, Any]]) -> int:
    return int(
        any(
            isinstance(item.get("projective_infinity"), dict)
            and item["projective_infinity"].get("contribution", 0) > 0
            for item in items
        )
    )


def result_to_packet_item(
    result: ExtractionResult,
    prime: int,
    sampler: str,
    emit_split_root_certificate: bool,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "A": result.exact_agreement,
        "j": result.j,
        "t": result.t,
        "status": result.status,
    }
    if result.status == "regular_minor":
        if result.minor_family_records is not None:
            assert result.polynomial is not None
            degree = poly_degree(result.polynomial, prime)
            roots = result.roots
            row_sets = [
                record["row_set"] for record in result.minor_family_records
            ]
            item["regular_minor_gcd"] = {
                "row_sets": row_sets,
                "polynomial_ref": (
                    f"inline:regular_minor_gcd_data.gcd_coefficients_mod_{prime}_ascending"
                ),
                "degree": degree,
                "root_hash": hash_json(
                    roots
                    if roots is not None
                    else {
                        "roots": "not_enumerated",
                        "degree_bound": degree,
                        "row_sets": row_sets,
                    }
                ),
                "minor_count": len(result.minor_family_records),
                "containment": (
                    "rank-defect slopes make every audited maximal minor vanish, "
                    "so they are contained in the common gcd roots"
                ),
            }
            item["regular_minor_gcd_data"] = {
                f"gcd_coefficients_mod_{prime}_ascending": result.polynomial,
                f"minor_polynomials_mod_{prime}_ascending": result.minor_family_records,
            }
            if roots is not None:
                item["regular_minor_gcd_data"][f"roots_mod_{prime}"] = roots
                if emit_split_root_certificate:
                    root_certificate = split_linear_root_certificate_mod(
                        result.polynomial, roots, prime
                    )
                    if root_certificate is not None:
                        item["regular_minor_gcd_data"]["root_certificate"] = (
                            root_certificate
                        )
                if result.enumerated_bad_slopes is not None:
                    item["regular_minor_gcd_data"][
                        f"enumerated_bad_slopes_mod_{prime}"
                    ] = result.enumerated_bad_slopes
            item["extractor_audit"] = {
                "tested_row_sets": result.tested_row_sets,
                "row_set_source": result.row_set_source,
                "rank_pivot_node": result.rank_pivot_node,
                "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
                "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
                "root_count": len(roots) if roots is not None else "not_enumerated",
                "gcd_degree": degree,
                "certificate_mode": MINOR_GCD_MODE,
            }
            if result.rank_pivot_test_nodes is not None:
                item["extractor_audit"]["rank_pivot_test_nodes"] = (
                    result.rank_pivot_test_nodes
                )
            if result.rank_pivot_witness_records is not None:
                item["extractor_audit"]["rank_pivot_witness_records"] = (
                    result.rank_pivot_witness_records
                )
            if result.row_set_source and result.row_set_source.endswith(
                f"_minor_gcd_{ZERO_U_GCD_METHOD}"
            ):
                item["extractor_audit"]["minor_gcd_method"] = ZERO_U_GCD_METHOD
            add_rank_pivot_test_nodes(item["extractor_audit"])
            if sampler == "projective_line":
                item["projective_infinity"] = prime_projective_infinity_gcd_audit(
                    result, prime
                )
            return item
        assert result.row_set is not None
        if result.polynomial is None:
            if sampler == "projective_line":
                raise ValueError(
                    "projective_line regular-minor packets need an inline "
                    "determinant polynomial to certify [0:1]"
                )
            degree = result.j + 1
            item["regular_minor"] = {
                "row_set": result.row_set,
                "polynomial_ref": "rank_witness:determinant_nonzero_at_pivot_node",
                "degree": degree,
                "root_hash": hash_json(
                    {
                        "roots": "not_enumerated",
                        "degree_bound": degree,
                        "row_set": result.row_set,
                        "rank_pivot_node": result.rank_pivot_node,
                    }
                ),
            }
            item["extractor_audit"] = {
                "tested_row_sets": result.tested_row_sets,
                "row_set_source": result.row_set_source,
                "rank_pivot_node": result.rank_pivot_node,
                "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
                "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
                "root_count": "not_enumerated",
                "degree_bound": degree,
                "certificate_mode": "rank_witness_bound",
            }
            add_rank_pivot_test_nodes(item["extractor_audit"])
            return item
        assert result.polynomial is not None
        degree = poly_degree(result.polynomial, prime)
        roots = result.roots
        item["regular_minor"] = {
            "row_set": result.row_set,
            "polynomial_ref": (
                f"inline:regular_minor.coefficients_mod_{prime}_ascending"
            ),
            "degree": degree,
            "root_hash": hash_json(
                roots
                if roots is not None
                else {
                    "roots": "not_enumerated",
                    "degree_bound": degree,
                    "row_set": result.row_set,
                }
            ),
        }
        item["regular_minor_polynomial_data"] = {
            f"coefficients_mod_{prime}_ascending": result.polynomial
        }
        if roots is not None:
            item["regular_minor_data"] = {
                f"coefficients_mod_{prime}_ascending": result.polynomial,
                f"roots_mod_{prime}": roots,
            }
            if emit_split_root_certificate:
                root_certificate = split_linear_root_certificate_mod(
                    result.polynomial, roots, prime
                )
                if root_certificate is not None:
                    item["regular_minor_data"]["root_certificate"] = root_certificate
            if result.enumerated_bad_slopes is not None:
                item["regular_minor_data"][
                    f"enumerated_bad_slopes_mod_{prime}"
                ] = result.enumerated_bad_slopes
        item["extractor_audit"] = {
            "tested_row_sets": result.tested_row_sets,
            "row_set_source": result.row_set_source,
            "rank_pivot_node": result.rank_pivot_node,
            "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
            "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
            "root_count": len(roots) if roots is not None else "not_enumerated",
            "degree_bound": degree,
        }
        if sampler == "projective_line":
            item["projective_infinity"] = prime_projective_infinity_audit(
                result, prime
            )
    else:
        item["residual_label"] = result.residual_label or "unknown"
        item["residual_reason"] = result.residual_reason
        item["extractor_audit"] = {
            "tested_row_sets": result.tested_row_sets,
            "row_set_source": result.row_set_source,
            "rank_pivot_node": result.rank_pivot_node,
            "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
            "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
        }
        if result.residual_audit is not None:
            item["extractor_audit"].update(result.residual_audit)
    add_rank_pivot_test_nodes(item["extractor_audit"])
    return item


def result_to_packet_item_field(
    result: ExtractionResult,
    field: PolynomialBasisField,
    sampler: str,
    emit_split_root_certificate: bool,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "A": result.exact_agreement,
        "j": result.j,
        "t": result.t,
        "status": result.status,
    }
    if result.status == "regular_minor":
        if result.minor_family_records is not None:
            assert result.polynomial is not None
            polynomial = [field.normalize(coeff) for coeff in result.polynomial]
            polynomial_encoded = [field.encode(coeff) for coeff in polynomial]
            degree = fpoly_degree(polynomial, field)
            roots = result.roots
            roots_encoded = (
                sorted(field.encode(root) for root in roots)
                if roots is not None
                else None
            )
            row_sets = [
                record["row_set"] for record in result.minor_family_records
            ]
            minor_records = []
            for record in result.minor_family_records:
                record_coefficients = [
                    field.normalize(coeff) for coeff in record["coefficients"]
                ]
                minor_records.append(
                    {
                        "row_set": record["row_set"],
                        "coefficients": [
                            field.encode(coeff) for coeff in record_coefficients
                        ],
                        "degree": fpoly_degree(record_coefficients, field)
                        if not fpoly_is_zero(record_coefficients, field)
                        else -1,
                    }
                )
            item["regular_minor_gcd"] = {
                "row_sets": row_sets,
                "polynomial_ref": "inline:regular_minor_gcd_data.gcd_coefficients_ascending",
                "degree": degree,
                "root_hash": hash_json(
                    roots_encoded
                    if roots_encoded is not None
                    else {
                        "roots": "not_enumerated",
                        "degree_bound": degree,
                        "row_sets": row_sets,
                    }
                ),
                "minor_count": len(result.minor_family_records),
                "containment": (
                    "rank-defect slopes make every audited maximal minor vanish, "
                    "so they are contained in the common gcd roots"
                ),
            }
            item["regular_minor_gcd_data"] = {
                "gcd_coefficients_ascending": polynomial_encoded,
                "minor_polynomials_ascending": minor_records,
                "field_encoding": "base-p low-to-high integer",
                "p": field.p,
                "field_extension_degree": field.degree,
            }
            if roots_encoded is not None:
                item["regular_minor_gcd_data"]["roots"] = roots_encoded
                if emit_split_root_certificate:
                    root_certificate = split_linear_root_certificate_field(
                        polynomial, roots, field
                    )
                    if root_certificate is not None:
                        item["regular_minor_gcd_data"]["root_certificate"] = (
                            root_certificate
                        )
                if result.enumerated_bad_slopes is not None:
                    item["regular_minor_gcd_data"]["enumerated_bad_slopes"] = sorted(
                        field.encode(slope) for slope in result.enumerated_bad_slopes
                    )
            item["extractor_audit"] = {
                "tested_row_sets": result.tested_row_sets,
                "row_set_source": result.row_set_source,
                "rank_pivot_node": result.rank_pivot_node,
                "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
                "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
                "root_count": (
                    len(roots_encoded) if roots_encoded is not None else "not_enumerated"
                ),
                "gcd_degree": degree,
                "field_size": field.size,
                "certificate_mode": MINOR_GCD_MODE,
            }
            if result.rank_pivot_test_nodes is not None:
                item["extractor_audit"]["rank_pivot_test_nodes"] = (
                    result.rank_pivot_test_nodes
                )
            if result.rank_pivot_witness_records is not None:
                item["extractor_audit"]["rank_pivot_witness_records"] = (
                    result.rank_pivot_witness_records
                )
            if result.row_set_source and result.row_set_source.endswith(
                f"_minor_gcd_{ZERO_U_GCD_METHOD}"
            ):
                item["extractor_audit"]["minor_gcd_method"] = ZERO_U_GCD_METHOD
            add_rank_pivot_test_nodes(item["extractor_audit"])
            if sampler == "projective_line":
                item["projective_infinity"] = field_projective_infinity_gcd_audit(
                    result, field
                )
            return item
        assert result.row_set is not None
        if result.polynomial is None:
            if sampler == "projective_line":
                raise ValueError(
                    "projective_line regular-minor packets need an inline "
                    "determinant polynomial to certify [0:1]"
                )
            degree = result.j + 1
            item["regular_minor"] = {
                "row_set": result.row_set,
                "polynomial_ref": "rank_witness:determinant_nonzero_at_pivot_node",
                "degree": degree,
                "root_hash": hash_json(
                    {
                        "roots": "not_enumerated",
                        "degree_bound": degree,
                        "row_set": result.row_set,
                        "rank_pivot_node": result.rank_pivot_node,
                    }
                ),
            }
            item["extractor_audit"] = {
                "tested_row_sets": result.tested_row_sets,
                "row_set_source": result.row_set_source,
                "rank_pivot_node": result.rank_pivot_node,
                "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
                "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
                "root_count": "not_enumerated",
                "degree_bound": degree,
                "field_size": field.size,
                "certificate_mode": "rank_witness_bound",
            }
            add_rank_pivot_test_nodes(item["extractor_audit"])
            return item
        assert result.polynomial is not None
        polynomial = [field.normalize(coeff) for coeff in result.polynomial]
        polynomial_encoded = [field.encode(coeff) for coeff in polynomial]
        degree = fpoly_degree(polynomial, field)
        roots = result.roots
        roots_encoded = (
            sorted(field.encode(root) for root in roots)
            if roots is not None
            else None
        )
        item["regular_minor"] = {
            "row_set": result.row_set,
            "polynomial_ref": "inline:regular_minor.coefficients_ascending",
            "degree": degree,
            "root_hash": hash_json(
                roots_encoded
                if roots_encoded is not None
                else {
                    "roots": "not_enumerated",
                    "degree_bound": degree,
                    "row_set": result.row_set,
                }
            ),
        }
        item["regular_minor_polynomial_data"] = {
            "coefficients_ascending": polynomial_encoded,
            "field_encoding": "base-p low-to-high integer",
            "p": field.p,
            "field_extension_degree": field.degree,
        }
        if result.regular_minor_audit is not None:
            item["regular_minor_polynomial_data"]["low_rank_compression"] = (
                result.regular_minor_audit
            )
        if roots_encoded is not None:
            item["regular_minor_data"] = {
                "coefficients_ascending": polynomial_encoded,
                "roots": roots_encoded,
                "field_encoding": "base-p low-to-high integer",
                "p": field.p,
                "field_extension_degree": field.degree,
            }
            if emit_split_root_certificate:
                root_certificate = split_linear_root_certificate_field(
                    polynomial, roots, field
                )
                if root_certificate is not None:
                    item["regular_minor_data"]["root_certificate"] = root_certificate
                quadratic_certificate = quadratic_root_certificate_field(
                    polynomial, roots, field
                )
                if quadratic_certificate is not None:
                    item["regular_minor_data"]["quadratic_root_certificate"] = (
                        quadratic_certificate
                    )
            if result.enumerated_bad_slopes is not None:
                item["regular_minor_data"]["enumerated_bad_slopes"] = sorted(
                    field.encode(slope) for slope in result.enumerated_bad_slopes
                )
        item["extractor_audit"] = {
            "tested_row_sets": result.tested_row_sets,
            "row_set_source": result.row_set_source,
            "rank_pivot_node": result.rank_pivot_node,
            "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
            "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
            "root_count": (
                len(roots_encoded) if roots_encoded is not None else "not_enumerated"
            ),
            "degree_bound": degree,
            "field_size": field.size,
        }
        if sampler == "projective_line":
            item["projective_infinity"] = field_projective_infinity_audit(
                result, field
            )
    else:
        item["residual_label"] = result.residual_label or "unknown"
        item["residual_reason"] = result.residual_reason
        item["extractor_audit"] = {
            "tested_row_sets": result.tested_row_sets,
            "row_set_source": result.row_set_source,
            "rank_pivot_node": result.rank_pivot_node,
            "rank_pivot_nodes_tested": result.rank_pivot_nodes_tested,
            "rank_pivot_nodes_required": result.rank_pivot_nodes_required,
        }
        if result.residual_audit is not None:
            item["extractor_audit"].update(result.residual_audit)
    add_rank_pivot_test_nodes(item["extractor_audit"])
    return item


def build_packet(spec: dict[str, Any], input_ref: str | None = None) -> dict[str, Any]:
    if "field_model" in spec:
        return build_packet_field(spec, input_ref)

    row = spec["row"]
    prime = parse_prime_field(row["field"])
    agreements = [int(value) for value in spec["exact_agreements"]]
    results = [extract_for_agreement(spec, agreement, prime) for agreement in agreements]
    all_roots_enumerated = all(
        result.status == "regular_minor" and result.roots is not None
        for result in results
    )
    root_union = sorted(
        {
            root
            for result in results
            if result.roots is not None
            for root in result.roots
        }
    )
    bad_union = sorted(
        {
            slope
            for result in results
            if result.enumerated_bad_slopes is not None
            for slope in result.enumerated_bad_slopes
        }
    )
    if bad_union and not set(bad_union).issubset(root_union):
        raise AssertionError(("closed-range bad slopes not contained in roots"))

    sampler = spec.get("sampler", "finite_affine_line")
    emit_split_root_certificate = bool(
        spec.get("emit_split_root_certificate", False)
    )
    exact_items = [
        result_to_packet_item(
            result, prime, sampler, emit_split_root_certificate
        )
        for result in results
    ]
    projective_infinity_count = (
        projective_infinity_union_count(exact_items)
        if sampler == "projective_line"
        else 0
    )

    packet: dict[str, Any] = {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "row": {
            "n": int(row["n"]),
            "k": int(row["k"]),
            "field": row["field"],
            "domain_hash": row.get("domain_hash")
            or hash_json(row.get("domain", row.get("domain_description", ""))),
            "domain_description": row.get(
                "domain_description", "domain supplied in extractor input"
            ),
        },
        "agreement_threshold": int(spec.get("agreement_threshold", min(agreements))),
        "sampler": sampler,
        "removed_ledgers": spec.get("removed_ledgers", []),
        "exact_agreements": exact_items,
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": (
                "rank_at_nodes full-rank specialization over the base prime field"
                if spec.get("certificate_mode") == "rank_witness_bound"
                else "zero-u monomial closed-form root certificate over the base prime field"
                if spec.get("certificate_mode") == ZERO_U_MONOMIAL_MODE
                else "scalar-multiple closed-form root certificate over the base prime field"
                if spec.get("certificate_mode") == SCALAR_MULTIPLE_MODE
                else "common-gcd root certificate over audited maximal minors"
                if spec.get("certificate_mode") == MINOR_GCD_MODE
                and spec.get("minor_gcd_method") != ZERO_U_GCD_METHOD
                else "zero-u closed-form common-gcd certificate over audited maximal minors"
                if spec.get("certificate_mode") == MINOR_GCD_MODE
                and spec.get("minor_gcd_method") == ZERO_U_GCD_METHOD
                else "numeric determinant interpolation over the base prime field"
            ),
            "input_ref": input_ref,
            "input_sha256": optional_file_hash(input_ref),
            "row_set_strategy": spec.get("row_set_strategy", {"type": "prefix"}),
            "scope": "prime-field syndrome pencils only",
        },
        "status": spec.get("status", "EXPERIMENTAL"),
        "nonclaims": spec.get(
            "nonclaims",
            [
                "not a prize-row threshold theorem",
                "not an extension-field row adapter",
                "not a singular pivot-chart certificate",
            ],
        ),
    }
    if "certificate_mode" in spec:
        packet["extractor"]["certificate_mode"] = spec["certificate_mode"]
    if "minor_gcd_method" in spec:
        packet["extractor"]["minor_gcd_method"] = spec["minor_gcd_method"]
    if "claim_scope" in spec:
        packet["claim_scope"] = spec["claim_scope"]
    if all_roots_enumerated:
        packet["declared_aperiodic_numerator"] = (
            len(root_union) + projective_infinity_count
        )
        packet["root_union_table_ref"] = f"inline:root_union_mod_{prime}"
        packet[f"root_union_mod_{prime}"] = root_union
        packet[f"enumerated_bad_slope_union_mod_{prime}"] = bad_union
    else:
        packet["root_union_table_ref"] = "not_enumerated"
        packet["regular_root_bound_sum"] = sum(
            (
                poly_degree(result.polynomial, prime)
                if result.polynomial is not None
                else result.j + 1
            )
            for result in results
            if result.status == "regular_minor"
        )
    return packet


def build_packet_field(
    spec: dict[str, Any], input_ref: str | None = None
) -> dict[str, Any]:
    row = spec["row"]
    field = PolynomialBasisField.from_spec(spec["field_model"])
    agreements = [int(value) for value in spec["exact_agreements"]]
    results = [
        extract_for_agreement_field(spec, agreement, field)
        for agreement in agreements
    ]
    all_roots_enumerated = all(
        result.status == "regular_minor" and result.roots is not None
        for result in results
    )
    root_union = sorted(
        {
            field.encode(root)
            for result in results
            if result.roots is not None
            for root in result.roots
        }
    )
    bad_union = sorted(
        {
            field.encode(slope)
            for result in results
            if result.enumerated_bad_slopes is not None
            for slope in result.enumerated_bad_slopes
        }
    )
    if bad_union and not set(bad_union).issubset(root_union):
        raise AssertionError(("closed-range bad slopes not contained in roots"))

    sampler = spec.get("sampler", "finite_affine_line")
    emit_split_root_certificate = bool(
        spec.get("emit_split_root_certificate", False)
    )
    exact_items = [
        result_to_packet_item_field(
            result, field, sampler, emit_split_root_certificate
        )
        for result in results
    ]
    projective_infinity_count = (
        projective_infinity_union_count(exact_items)
        if sampler == "projective_line"
        else 0
    )

    packet: dict[str, Any] = {
        "schema_version": "aperiodic-hankel-eliminant-v1",
        "row": {
            "n": int(row["n"]),
            "k": int(row["k"]),
            "field": row["field"],
            "domain_hash": row.get("domain_hash")
            or hash_json(row.get("domain", row.get("domain_description", ""))),
            "domain_description": row.get(
                "domain_description", "domain supplied in extractor input"
            ),
        },
        "agreement_threshold": int(spec.get("agreement_threshold", min(agreements))),
        "sampler": sampler,
        "sampler_audit": sampler_audit(row["field"], sampler, field.size),
        "removed_ledgers": spec.get("removed_ledgers", []),
        "exact_agreements": exact_items,
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": (
                "rank_at_nodes full-rank specialization over a polynomial-basis finite field"
                if spec.get("certificate_mode") == "rank_witness_bound"
                else "zero-u monomial closed-form root certificate over a polynomial-basis finite field"
                if spec.get("certificate_mode") == ZERO_U_MONOMIAL_MODE
                else "scalar-multiple closed-form root certificate over a polynomial-basis finite field"
                if spec.get("certificate_mode") == SCALAR_MULTIPLE_MODE
                else "one-spike linear closed-form root certificate over a polynomial-basis finite field"
                if spec.get("certificate_mode") == ONE_SPIKE_LINEAR_MODE
                else "low-rank update closed-form root/degree-bound certificate over a polynomial-basis finite field"
                if spec.get("certificate_mode") == LOW_RANK_UPDATE_MODE
                else "common-gcd audit of numeric determinant minors over a polynomial-basis finite field"
                if spec.get("certificate_mode") == MINOR_GCD_MODE
                and spec.get("minor_gcd_method") != ZERO_U_GCD_METHOD
                else "zero-u closed-form common-gcd audit over a polynomial-basis finite field"
                if spec.get("certificate_mode") == MINOR_GCD_MODE
                and spec.get("minor_gcd_method") == ZERO_U_GCD_METHOD
                else "numeric determinant interpolation over a polynomial-basis finite field"
            ),
            "input_ref": input_ref,
            "input_sha256": optional_file_hash(input_ref),
            "row_set_strategy": spec.get("row_set_strategy", {"type": "prefix"}),
            "scope": "prime-power syndrome pencils with explicit polynomial-basis model",
            "field_model": {
                "kind": "polynomial_basis",
                "p": field.p,
                "degree": field.degree,
                "modulus": field.modulus,
                "encoding": "base-p low-to-high integer",
            },
        },
        "status": spec.get("status", "EXPERIMENTAL"),
        "nonclaims": spec.get(
            "nonclaims",
            [
                "not a prize-row threshold theorem",
                "not a singular pivot-chart certificate",
            ],
        ),
    }
    if "certificate_mode" in spec:
        packet["extractor"]["certificate_mode"] = spec["certificate_mode"]
    if "minor_gcd_method" in spec:
        packet["extractor"]["minor_gcd_method"] = spec["minor_gcd_method"]
    if "claim_scope" in spec:
        packet["claim_scope"] = spec["claim_scope"]
    if all_roots_enumerated:
        packet["declared_aperiodic_numerator"] = (
            len(root_union) + projective_infinity_count
        )
        packet["root_union_table_ref"] = "inline:root_union"
        packet["root_union"] = root_union
        packet["enumerated_bad_slope_union"] = bad_union
    else:
        packet["root_union_table_ref"] = "not_enumerated"
        packet["regular_root_bound_sum"] = sum(
            (
                fpoly_degree(result.polynomial, field)
                if result.polynomial is not None
                else result.j + 1
            )
            for result in results
            if result.status == "regular_minor"
        )
    return packet


def render(packet: dict[str, Any]) -> str:
    return json.dumps(packet, indent=2, sort_keys=True) + "\n"


def check_packet(spec_path: Path, packet_path: Path) -> None:
    expected = render(build_packet(load_json(spec_path), str(spec_path)))
    actual = packet_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"packet mismatch: {packet_path}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def print_summary(packet: dict[str, Any]) -> None:
    print("regular Hankel-minor extractor")
    print(
        "row: {field}, n={n}, k={k}, threshold={threshold}".format(
            field=packet["row"]["field"],
            n=packet["row"]["n"],
            k=packet["row"]["k"],
            threshold=packet["agreement_threshold"],
        )
    )
    for item in packet["exact_agreements"]:
        if item["status"] == "regular_minor":
            data = item.get("regular_minor_data", {})
            certificate = item.get("regular_minor")
            rows: Any = certificate["row_set"] if isinstance(certificate, dict) else None
            degree: Any = certificate["degree"] if isinstance(certificate, dict) else None
            if "regular_minor_gcd" in item:
                data = item.get("regular_minor_gcd_data", {})
                certificate = item["regular_minor_gcd"]
                rows = f"{certificate['minor_count']} row sets"
                degree = certificate["degree"]
            root_keys = [
                key for key in data if key.startswith("roots_mod_") or key == "roots"
            ]
            roots: list[int] | str = data[root_keys[0]] if root_keys else "not_enumerated"
            print(
                "A={A} j={j} t={t} rows={rows} degree={degree} "
                "roots={roots} tested={tested}".format(
                    A=item["A"],
                    j=item["j"],
                    t=item["t"],
                    rows=rows,
                    degree=degree,
                    roots=roots,
                    tested=item["extractor_audit"]["tested_row_sets"],
                )
            )
        else:
            print(
                "A={A} j={j} t={t} residual={label} tested={tested}".format(
                    A=item["A"],
                    j=item["j"],
                    t=item["t"],
                    label=item.get("residual_label"),
                    tested=item["extractor_audit"]["tested_row_sets"],
                )
            )
    if "declared_aperiodic_numerator" in packet:
        print(f"declared_aperiodic_numerator={packet['declared_aperiodic_numerator']}")
    else:
        print(f"regular_root_bound_sum={packet.get('regular_root_bound_sum')}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="regular-minor extractor input JSON")
    parser.add_argument("--write", type=Path, help="write deterministic v9 packet")
    parser.add_argument("--check", type=Path, help="check deterministic v9 packet")
    parser.add_argument("--json", action="store_true", help="print packet JSON")
    args = parser.parse_args()

    spec = load_json(args.input)
    packet = build_packet(spec, str(args.input))

    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_packet(args.input, args.check)
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
