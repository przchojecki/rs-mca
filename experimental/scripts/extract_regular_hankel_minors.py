#!/usr/bin/env python3
"""Extract regular overdetermined Hankel-minor certificates from row data.

This is the first reusable M3 extractor for the Paper D v9 atlas.  It reads
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
from itertools import combinations, product
from pathlib import Path
from typing import Any


DEFAULT_MAX_ROOT_ENUM_FIELD_SIZE = 10000
DEFAULT_MAX_BAD_SLOPE_SUBSETS = 200000
ZERO_U_MONOMIAL_MODE = "zero_u_monomial_roots"


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
    residual_label: str | None = None
    residual_reason: str | None = None


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
    if row_config.get("type") == "rank_at_nodes":
        row_sets, row_set_audit = rank_pivot_row_sets_mod(u, v, t, size, prime)
    else:
        row_sets = candidate_row_sets(t, size, row_config)
        row_set_audit = {
            "source": row_config.get("type", "prefix"),
            "node": None,
            "nodes_tested": None,
        }
    if spec.get("certificate_mode") == ZERO_U_MONOMIAL_MODE:
        if any(value % prime for value in u):
            raise ValueError("zero_u_monomial_roots needs u=0")
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
                [0] * size + [leading],
                [0],
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
            residual_label="unknown",
            residual_reason="all tested zero-u monomial leading coefficients vanished",
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
        residual_label="unknown",
        residual_reason=(
            row_set_audit.get("singularity_proof")
            or "all tested regular maximal minors vanished"
        ),
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
    if row_config.get("type") == "rank_at_nodes":
        row_sets, row_set_audit = rank_pivot_row_sets_field(u, v, t, size, field)
    else:
        row_sets = candidate_row_sets(t, size, row_config)
        row_set_audit = {
            "source": row_config.get("type", "prefix"),
            "node": None,
            "nodes_tested": None,
        }
    if spec.get("certificate_mode") == ZERO_U_MONOMIAL_MODE:
        if any(not field.is_zero(value) for value in u):
            raise ValueError("zero_u_monomial_roots needs u=0")
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
                [field.zero] * size + [leading],
                [field.zero],
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
            residual_label="unknown",
            residual_reason="all tested zero-u monomial leading coefficients vanished",
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
        residual_label="unknown",
        residual_reason=(
            row_set_audit.get("singularity_proof")
            or "all tested regular maximal minors vanished"
        ),
    )


def result_to_packet_item(result: ExtractionResult, prime: int) -> dict[str, Any]:
    item: dict[str, Any] = {
        "A": result.exact_agreement,
        "j": result.j,
        "t": result.t,
        "status": result.status,
    }
    if result.status == "regular_minor":
        assert result.row_set is not None
        if result.polynomial is None:
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
    return item


def result_to_packet_item_field(
    result: ExtractionResult,
    field: PolynomialBasisField,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "A": result.exact_agreement,
        "j": result.j,
        "t": result.t,
        "status": result.status,
    }
    if result.status == "regular_minor":
        assert result.row_set is not None
        if result.polynomial is None:
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
        if roots_encoded is not None:
            item["regular_minor_data"] = {
                "coefficients_ascending": polynomial_encoded,
                "roots": roots_encoded,
                "field_encoding": "base-p low-to-high integer",
                "p": field.p,
                "field_extension_degree": field.degree,
            }
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
        "sampler": spec.get("sampler", "finite_affine_line"),
        "removed_ledgers": spec.get("removed_ledgers", []),
        "exact_agreements": [
            result_to_packet_item(result, prime) for result in results
        ],
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": (
                "rank_at_nodes full-rank specialization over the base prime field"
                if spec.get("certificate_mode") == "rank_witness_bound"
                else "zero-u monomial closed-form root certificate over the base prime field"
                if spec.get("certificate_mode") == ZERO_U_MONOMIAL_MODE
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
    if all_roots_enumerated:
        packet["declared_aperiodic_numerator"] = len(root_union)
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
        "sampler": spec.get("sampler", "finite_affine_line"),
        "removed_ledgers": spec.get("removed_ledgers", []),
        "exact_agreements": [
            result_to_packet_item_field(result, field) for result in results
        ],
        "extractor": {
            "name": "regular-hankel-minor-extractor",
            "method": (
                "rank_at_nodes full-rank specialization over a polynomial-basis finite field"
                if spec.get("certificate_mode") == "rank_witness_bound"
                else "zero-u monomial closed-form root certificate over a polynomial-basis finite field"
                if spec.get("certificate_mode") == ZERO_U_MONOMIAL_MODE
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
    if all_roots_enumerated:
        packet["declared_aperiodic_numerator"] = len(root_union)
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
            root_keys = [
                key for key in data if key.startswith("roots_mod_") or key == "roots"
            ]
            roots: list[int] | str = data[root_keys[0]] if root_keys else "not_enumerated"
            print(
                "A={A} j={j} t={t} row_set={row_set} degree={degree} "
                "roots={roots} tested={tested}".format(
                    A=item["A"],
                    j=item["j"],
                    t=item["t"],
                    row_set=item["regular_minor"]["row_set"],
                    degree=item["regular_minor"]["degree"],
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
