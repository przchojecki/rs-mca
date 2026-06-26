#!/usr/bin/env python3
"""Verify the F1 syndrome-pencil normal form on small extension fields.

Status: AUDIT / EXPERIMENTAL.

The proof note is field-independent. This verifier checks the statement in
quadratic extensions F_p[u]/(u^2-d), with the RS domain embedded in F_p. For
each case it exhaustively compares direct interpolation on S = D \\ T against

    (H(Syn(f)) + z H(Syn(g))) ell_T = 0,

and checks that noncontainment is exactly H(Syn(g)) ell_T != 0.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from math import comb
from typing import Iterable, Sequence

Element = tuple[int, int]
Matrix = list[list[Element]]

CASES = (
    {"p": 5, "n": 4, "k": 2, "agreement": 3},
    {"p": 7, "n": 6, "k": 3, "agreement": 5},
    {"p": 7, "n": 6, "k": 2, "agreement": 4},
    {"p": 17, "n": 8, "k": 4, "agreement": 6},
    {"p": 17, "n": 8, "k": 3, "agreement": 5},
)

QUADRIC_ONLY_CASES = (
    {
        "name": "full-rank determinant quadric",
        "p": 17,
        "j": 3,
        "u": ((3, 1), (5, 2), (7, 4), (11, 8), (13, 3)),
        "v": ((2, 6), (4, 5), (8, 7), (9, 1), (15, 12)),
        "expected_rank": 4,
        "expected_zero": False,
        "expected_global_rank_defective": False,
    },
    {
        "name": "kernel-ruling zero quadric",
        "p": 17,
        "j": 3,
        "u": ((1, 0), (0, 0), (0, 0), (0, 0), (1, 0)),
        "v": ((2, 0), (0, 0), (0, 0), (0, 0), (2, 0)),
        "expected_rank": 2,
        "expected_zero": True,
        "expected_global_rank_defective": False,
    },
    {
        "name": "global rank-one pencil",
        "p": 17,
        "j": 3,
        "u": ((1, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
        "v": ((2, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
        "expected_rank": 1,
        "expected_zero": True,
        "expected_global_rank_defective": True,
    },
)

REDUCED_LINE_SECTION_CASES = (
    {
        "name": "transverse determinant line",
        "p": 5,
        "generators": (
            (((1, 0), (0, 0)), ((0, 0), (0, 0))),
            (((0, 0), (0, 0)), ((0, 0), (1, 0))),
        ),
        "expected_contained": False,
        "expected_zero_points": 2,
        "expected_slope_count": 1,
        "expected_common_kernel": False,
        "expected_common_image": False,
    },
    {
        "name": "common-kernel ruling line",
        "p": 5,
        "generators": (
            (((1, 0), (4, 0)), ((0, 0), (0, 0))),
            (((0, 0), (0, 0)), ((1, 0), (4, 0))),
        ),
        "expected_contained": True,
        "expected_zero_points": 26,
        "expected_slope_count": 1,
        "expected_common_kernel": True,
        "expected_common_image": False,
    },
    {
        "name": "common-image ruling line",
        "p": 5,
        "generators": (
            (((1, 0), (0, 0)), ((0, 0), (0, 0))),
            (((0, 0), (1, 0)), ((0, 0), (0, 0))),
        ),
        "expected_contained": True,
        "expected_zero_points": 26,
        "expected_slope_count": 25,
        "expected_common_kernel": False,
        "expected_common_image": True,
    },
)

J2_FIBER_ONLY_CASES = (
    {
        "name": "rank-two unique split quadratic",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((1, 0), (0, 0), (1, 0)),
            ((0, 0), (1, 0), (5, 0)),
        ),
        "expected_rank": 2,
        "expected_landings": 1,
    },
    {
        "name": "rank-one fixed-sum fiber",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((0, 0), (1, 0), (5, 0)),
            ((0, 0), (0, 0), (0, 0)),
        ),
        "expected_rank": 1,
        "expected_landings": 2,
    },
    {
        "name": "rank-one star fiber",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((1, 0), (1, 0), (1, 0)),
            ((0, 0), (0, 0), (0, 0)),
        ),
        "expected_rank": 1,
        "expected_landings": 5,
    },
    {
        "name": "rank-zero unrestricted fiber",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((0, 0), (0, 0), (0, 0)),
            ((0, 0), (0, 0), (0, 0)),
        ),
        "expected_rank": 0,
        "expected_landings": 15,
    },
)

J3_FIBER_ONLY_CASES = (
    {
        "name": "rank-two line through two fixed roots",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((1, 0), (1, 0), (1, 0), (1, 0)),
            ((1, 0), (2, 0), (4, 0), (1, 0)),
        ),
        "expected_rank": 2,
        "expected_monic_rank": 2,
        "expected_landings": 4,
    },
    {
        "name": "rank-one plane through one fixed root",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((1, 0), (1, 0), (1, 0), (1, 0)),
            ((0, 0), (0, 0), (0, 0), (0, 0)),
        ),
        "expected_rank": 1,
        "expected_monic_rank": 1,
        "expected_landings": 10,
    },
    {
        "name": "rank-two monic-rank-defective branch",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((1, 0), (1, 0), (1, 0), (1, 0)),
            ((2, 0), (2, 0), (2, 0), (3, 0)),
        ),
        "expected_rank": 2,
        "expected_monic_rank": 1,
        "expected_landings": 0,
    },
    {
        "name": "rank-zero unrestricted cubics",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "rows": (
            ((0, 0), (0, 0), (0, 0), (0, 0)),
            ((0, 0), (0, 0), (0, 0), (0, 0)),
        ),
        "expected_rank": 0,
        "expected_monic_rank": 0,
        "expected_landings": 20,
    },
)

GENERAL_FIXED_SLOPE_CASES = (
    {
        "name": "j4 rank-two fiber through two fixed roots",
        "p": 11,
        "domain": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "j": 4,
        "rows": (
            ((1, 0), (2, 0), (4, 0), (8, 0), (5, 0)),
            ((1, 0), (5, 0), (3, 0), (4, 0), (9, 0)),
        ),
        "expected_rank": 2,
        "expected_monic_rank": 2,
        "expected_landings": 28,
    },
    {
        "name": "j5 rank-two fiber through two fixed roots",
        "p": 11,
        "domain": (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        "j": 5,
        "rows": (
            ((1, 0), (2, 0), (4, 0), (8, 0), (5, 0), (10, 0)),
            ((1, 0), (5, 0), (3, 0), (4, 0), (9, 0), (1, 0)),
        ),
        "expected_rank": 2,
        "expected_monic_rank": 2,
        "expected_landings": 56,
    },
)

ROW_CUT_RESONANCE_CASES = (
    {
        "name": "j4 fixed-root row cut",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "j": 4,
        "alpha": 2,
        "rows": (
            ((1, 0), (2, 0), (4, 0), (1, 0), (2, 0)),
        ),
        "expected_rank": 1,
        "expected_landings": 10,
        "expected_star_span_rank": 4,
    },
    {
        "name": "j4 unrestricted zero row cut",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "j": 4,
        "rows": (
            ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0)),
        ),
        "expected_rank": 0,
        "expected_landings": 15,
    },
    {
        "name": "j4 nonstar c2 row cut",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "j": 4,
        "rows": (
            ((0, 0), (0, 0), (1, 0), (0, 0), (0, 0)),
        ),
        "expected_rank": 1,
        "expected_landings": 6,
        "expected_full_star_count": 0,
        "expected_star_free_bound": 15,
        "expected_max_root_slice": 4,
    },
)

GLOBAL_MONIC_RANK_ONE_CASES = (
    {
        "name": "global finite root star",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "alpha": 2,
        "u": ((1, 0), (2, 0), (4, 0), (1, 0), (3, 0)),
        "v": ((3, 0), (6, 0), (5, 0), (3, 0), (4, 0)),
        "kind": "finite",
    },
    {
        "name": "global finite root contained star",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "alpha": 2,
        "u": ((1, 0), (2, 0), (4, 0), (1, 0), (2, 0)),
        "v": ((3, 0), (6, 0), (5, 0), (3, 0), (6, 0)),
        "kind": "finite",
    },
    {
        "name": "global finite root outside domain",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "alpha": 0,
        "u": ((1, 0), (0, 0), (0, 0), (0, 0), (3, 0)),
        "v": ((2, 0), (0, 0), (0, 0), (0, 0), (4, 0)),
        "kind": "finite",
    },
    {
        "name": "global infinity root",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "u": ((0, 0), (0, 0), (0, 0), (1, 0), (3, 0)),
        "v": ((0, 0), (0, 0), (0, 0), (2, 0), (4, 0)),
        "kind": "infinity",
    },
    {
        "name": "global j4 finite root star",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "j": 4,
        "alpha": 2,
        "u": ((1, 0), (2, 0), (4, 0), (1, 0), (2, 0), (3, 0)),
        "v": ((3, 0), (6, 0), (5, 0), (3, 0), (6, 0), (4, 0)),
        "kind": "finite",
    },
    {
        "name": "global j4 finite root contained star",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "j": 4,
        "alpha": 2,
        "u": ((1, 0), (2, 0), (4, 0), (1, 0), (2, 0), (4, 0)),
        "v": ((3, 0), (6, 0), (5, 0), (3, 0), (6, 0), (5, 0)),
        "kind": "finite",
    },
    {
        "name": "global j4 finite root outside domain",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "j": 4,
        "alpha": 0,
        "u": ((1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (3, 0)),
        "v": ((2, 0), (0, 0), (0, 0), (0, 0), (0, 0), (4, 0)),
        "kind": "finite",
    },
    {
        "name": "global j4 infinity root",
        "p": 7,
        "domain": (1, 2, 3, 4, 5, 6),
        "j": 4,
        "u": ((0, 0), (0, 0), (0, 0), (0, 0), (1, 0), (3, 0)),
        "v": ((0, 0), (0, 0), (0, 0), (0, 0), (2, 0), (4, 0)),
        "kind": "infinity",
    },
)


@dataclass(frozen=True)
class QuadraticField:
    p: int
    d: int

    @property
    def zero(self) -> Element:
        return (0, 0)

    @property
    def one(self) -> Element:
        return (1, 0)

    def element(self, a: int, b: int = 0) -> Element:
        return (a % self.p, b % self.p)

    def elements(self) -> Iterable[Element]:
        for a in range(self.p):
            for b in range(self.p):
                yield (a, b)

    def add(self, x: Element, y: Element) -> Element:
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def neg(self, x: Element) -> Element:
        return ((-x[0]) % self.p, (-x[1]) % self.p)

    def sub(self, x: Element, y: Element) -> Element:
        return self.add(x, self.neg(y))

    def mul(self, x: Element, y: Element) -> Element:
        a = x[0] * y[0] + self.d * x[1] * y[1]
        b = x[0] * y[1] + x[1] * y[0]
        return (a % self.p, b % self.p)

    def inv(self, x: Element) -> Element:
        norm = (x[0] * x[0] - self.d * x[1] * x[1]) % self.p
        if norm == 0:
            raise ZeroDivisionError(x)
        inv_norm = pow(norm, -1, self.p)
        return ((x[0] * inv_norm) % self.p, (-x[1] * inv_norm) % self.p)

    def div(self, x: Element, y: Element) -> Element:
        return self.mul(x, self.inv(y))

    def pow(self, x: Element, exponent: int) -> Element:
        result = self.one
        value = x
        e = exponent
        while e:
            if e & 1:
                result = self.mul(result, value)
            value = self.mul(value, value)
            e >>= 1
        return result


def least_nonsquare(p: int) -> int:
    for value in range(2, p):
        if pow(value, (p - 1) // 2, p) == p - 1:
            return value
    raise ValueError(f"no nonsquare modulo {p}")


def factorize(value: int) -> set[int]:
    factors: set[int] = set()
    trial = 2
    remaining = value
    while trial * trial <= remaining:
        while remaining % trial == 0:
            factors.add(trial)
            remaining //= trial
        trial += 1
    if remaining > 1:
        factors.add(remaining)
    return factors


def primitive_root(p: int) -> int:
    factors = factorize(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // q, p) != 1 for q in factors):
            return candidate
    raise ValueError(f"no primitive root modulo {p}")


def subgroup_points(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} must divide p-1={p-1}")
    generator = primitive_root(p)
    step = pow(generator, (p - 1) // n, p)
    points = [1]
    for _ in range(1, n):
        points.append((points[-1] * step) % p)
    if len(set(points)) != n:
        raise AssertionError("subgroup generation failed")
    return points


def deterministic_word(field: QuadraticField, points: Sequence[Element], salt: int) -> list[Element]:
    values = []
    for index, x in enumerate(points):
        a = (salt + 3 * index + 2 * x[0] + x[0] * x[0]) % field.p
        b = (2 * salt + index * index + x[0] + 1) % field.p
        values.append(field.element(a, b))
    return values


def dual_weights(field: QuadraticField, points: Sequence[Element]) -> list[Element]:
    weights = []
    for i, xi in enumerate(points):
        denominator = field.one
        for j, xj in enumerate(points):
            if i == j:
                continue
            denominator = field.mul(denominator, field.sub(xi, xj))
        weights.append(field.inv(denominator))
    return weights


def base_dual_weights(p: int, points: Sequence[int]) -> list[int]:
    weights = []
    for i, xi in enumerate(points):
        denominator = 1
        for j, xj in enumerate(points):
            if i == j:
                continue
            denominator = (denominator * (xi - xj)) % p
        weights.append(pow(denominator, -1, p))
    return weights


def syndrome(
    field: QuadraticField,
    points: Sequence[Element],
    weights: Sequence[Element],
    word: Sequence[Element],
    r: int,
) -> list[Element]:
    out = []
    for m in range(r):
        total = field.zero
        for x, lam, y in zip(points, weights, word):
            total = field.add(total, field.mul(field.mul(lam, field.pow(x, m)), y))
        out.append(total)
    return out


def base_syndrome(
    p: int,
    points: Sequence[int],
    weights: Sequence[int],
    values: Sequence[int],
    r: int,
) -> list[int]:
    out = []
    for m in range(r):
        total = 0
        for x, lam, value in zip(points, weights, values):
            total = (total + lam * pow(x, m, p) * value) % p
        out.append(total)
    return out


def locator_coefficients(field: QuadraticField, roots: Sequence[Element]) -> list[Element]:
    coeffs = [field.one]
    for root in roots:
        next_coeffs = [field.zero] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            next_coeffs[i] = field.sub(next_coeffs[i], field.mul(root, coeff))
            next_coeffs[i + 1] = field.add(next_coeffs[i + 1], coeff)
        coeffs = next_coeffs
    return coeffs


def hankel_product(
    field: QuadraticField,
    vector: Sequence[Element],
    locator: Sequence[Element],
    t: int,
) -> list[Element]:
    out = []
    for m in range(t):
        total = field.zero
        for ell, coeff in enumerate(locator):
            total = field.add(total, field.mul(vector[m + ell], coeff))
        out.append(total)
    return out


def decimated_hankel_product(
    field: QuadraticField,
    vector: Sequence[Element],
    quotient_locator: Sequence[Element],
    fiber_size: int,
    t: int,
) -> list[Element]:
    out = []
    for m in range(t):
        total = field.zero
        for s, coeff in enumerate(quotient_locator):
            total = field.add(total, field.mul(vector[m + fiber_size * s], coeff))
        out.append(total)
    return out


def vector_add(field: QuadraticField, left: Sequence[Element], right: Sequence[Element]) -> list[Element]:
    return [field.add(x, y) for x, y in zip(left, right)]


def scalar_vector_mul(field: QuadraticField, scalar: Element, vector: Sequence[Element]) -> list[Element]:
    return [field.mul(scalar, value) for value in vector]


def is_zero_vector(field: QuadraticField, vector: Sequence[Element]) -> bool:
    return all(value == field.zero for value in vector)


def projective_slope(
    field: QuadraticField,
    a_vector: Sequence[Element],
    b_vector: Sequence[Element],
) -> Element | None:
    if is_zero_vector(field, b_vector):
        return None
    pivot = next(index for index, value in enumerate(b_vector) if value != field.zero)
    scalar = field.div(a_vector[pivot], b_vector[pivot])
    if all(
        a_value == field.mul(scalar, b_value)
        for a_value, b_value in zip(a_vector, b_vector)
    ):
        return field.neg(scalar)
    return None


def interpolate_values(
    field: QuadraticField,
    xs: Sequence[Element],
    ys: Sequence[Element],
    eval_points: Sequence[Element],
) -> list[Element]:
    values = []
    for x in eval_points:
        total = field.zero
        for i, xi in enumerate(xs):
            numerator = field.one
            denominator = field.one
            for j, xj in enumerate(xs):
                if i == j:
                    continue
                numerator = field.mul(numerator, field.sub(x, xj))
                denominator = field.mul(denominator, field.sub(xi, xj))
            total = field.add(total, field.mul(ys[i], field.div(numerator, denominator)))
        values.append(total)
    return values


def explained_on_support(
    field: QuadraticField,
    points: Sequence[Element],
    word: Sequence[Element],
    support: Sequence[int],
    k: int,
) -> bool:
    sample = tuple(support[:k])
    xs = [points[i] for i in sample]
    ys = [word[i] for i in sample]
    eval_points = [points[i] for i in support]
    expected = [word[i] for i in support]
    return interpolate_values(field, xs, ys, eval_points) == expected


def matrix_rank(field: QuadraticField, matrix: Matrix) -> int:
    if not matrix:
        return 0
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0])
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv_pivot = field.inv(mat[rank][col])
        mat[rank] = [field.mul(inv_pivot, value) for value in mat[rank]]
        for row in range(rows):
            if row == rank or mat[row][col] == field.zero:
                continue
            factor = mat[row][col]
            mat[row] = [
                field.sub(value, field.mul(factor, pivot_value))
                for value, pivot_value in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def hankel_matrix(vector: Sequence[Element], t: int, j: int) -> Matrix:
    return [[vector[m + ell] for ell in range(j + 1)] for m in range(t)]


def dot(field: QuadraticField, left: Sequence[Element], right: Sequence[Element]) -> Element:
    total = field.zero
    for x, y in zip(left, right):
        total = field.add(total, field.mul(x, y))
    return total


def determinant_from_rows(
    field: QuadraticField,
    rows: Sequence[Sequence[Element]],
    vector: Sequence[Element],
) -> Element:
    a0 = dot(field, rows[0], vector)
    a1 = dot(field, rows[1], vector)
    b0 = dot(field, rows[2], vector)
    b1 = dot(field, rows[3], vector)
    return field.sub(field.mul(a0, b1), field.mul(a1, b0))


def determinant_quadratic_coefficients(
    field: QuadraticField,
    rows: Sequence[Sequence[Element]],
) -> dict[tuple[int, int], Element]:
    width = len(rows[0])
    coeffs: dict[tuple[int, int], Element] = {}
    a0, a1, b0, b1 = rows
    for i in range(width):
        coeffs[(i, i)] = field.sub(field.mul(a0[i], b1[i]), field.mul(a1[i], b0[i]))
        for j in range(i + 1, width):
            left = field.add(field.mul(a0[i], b1[j]), field.mul(a0[j], b1[i]))
            right = field.add(field.mul(a1[i], b0[j]), field.mul(a1[j], b0[i]))
            coeffs[(i, j)] = field.sub(left, right)
    return coeffs


def eval_quadratic_coefficients(
    field: QuadraticField,
    coeffs: dict[tuple[int, int], Element],
    vector: Sequence[Element],
) -> Element:
    total = field.zero
    for (i, j), coeff in coeffs.items():
        monomial = field.mul(vector[i], vector[j])
        total = field.add(total, field.mul(coeff, monomial))
    return total


def is_zero_quadratic(
    field: QuadraticField,
    coeffs: dict[tuple[int, int], Element],
) -> bool:
    return all(value == field.zero for value in coeffs.values())


def has_common_kernel_ruling(field: QuadraticField, rows: Sequence[Sequence[Element]]) -> bool:
    a0, a1, b0, b1 = rows
    zero = [field.zero] * len(a0)
    if list(b0) == zero and list(b1) == zero:
        return True
    for slope in field.elements():
        if (
            vector_add(field, a0, scalar_vector_mul(field, slope, b0)) == zero
            and vector_add(field, a1, scalar_vector_mul(field, slope, b1)) == zero
        ):
            return True
    return False


def has_common_image_ruling(field: QuadraticField, rows: Sequence[Sequence[Element]]) -> bool:
    a0, a1, b0, b1 = rows
    zero = [field.zero] * len(a0)
    if list(a0) == zero and list(b0) == zero:
        return True
    for ratio in field.elements():
        if (
            scalar_vector_mul(field, ratio, a0) == list(a1)
            and scalar_vector_mul(field, ratio, b0) == list(b1)
        ):
            return True
    return False


def projective_line_parameters(field: QuadraticField) -> list[tuple[Element, Element]]:
    return [(field.one, value) for value in field.elements()] + [(field.zero, field.one)]


def line_matrix(
    field: QuadraticField,
    first: Matrix,
    second: Matrix,
    left: Element,
    right: Element,
) -> Matrix:
    return [
        [
            field.add(field.mul(left, first[row][col]), field.mul(right, second[row][col]))
            for col in range(2)
        ]
        for row in range(2)
    ]


def matrix_determinant_2x2(field: QuadraticField, matrix: Matrix) -> Element:
    return field.sub(
        field.mul(matrix[0][0], matrix[1][1]),
        field.mul(matrix[0][1], matrix[1][0]),
    )


def is_scalar_multiple(
    field: QuadraticField,
    left: Sequence[Element],
    right: Sequence[Element],
) -> bool:
    pivot = None
    for index, value in enumerate(right):
        if value != field.zero:
            pivot = index
            break
    if pivot is None:
        return all(value == field.zero for value in left)
    scalar = field.div(left[pivot], right[pivot])
    return all(
        left_value == field.mul(scalar, right_value)
        for left_value, right_value in zip(left, right)
    )


def pencil_at_slope(
    field: QuadraticField,
    left: Matrix,
    right: Matrix,
    slope: Element,
) -> Matrix:
    return [
        [
            field.add(left[row][col], field.mul(slope, right[row][col]))
            for col in range(len(left[0]))
        ]
        for row in range(len(left))
    ]


def contract_row_at_root(
    field: QuadraticField,
    row: Sequence[Element],
    alpha: Element,
) -> list[Element]:
    return [
        field.sub(row[index + 1], field.mul(alpha, row[index]))
        for index in range(len(row) - 1)
    ]


def standard_basis(field: QuadraticField, width: int) -> list[list[Element]]:
    basis = []
    for index in range(width):
        vector = [field.zero] * width
        vector[index] = field.one
        basis.append(vector)
    return basis


def run_quadric_case(params: dict[str, object]) -> dict[str, object]:
    p = int(params["p"])
    j = int(params["j"])
    t = 2
    field = QuadraticField(p=p, d=least_nonsquare(p))
    u = [tuple(value) for value in params["u"]]
    v = [tuple(value) for value in params["v"]]
    left = hankel_matrix(u, t, j)
    right = hankel_matrix(v, t, j)
    rows = left + right
    rank = matrix_rank(field, rows)
    coeffs = determinant_quadratic_coefficients(field, rows)
    zero_quadric = is_zero_quadratic(field, coeffs)
    common_kernel_ruling = has_common_kernel_ruling(field, rows)
    common_image_ruling = has_common_image_ruling(field, rows)
    rank_defective_slopes = [
        slope
        for slope in field.elements()
        if matrix_rank(field, pencil_at_slope(field, left, right, slope)) <= 1
    ]
    global_rank_defective = len(rank_defective_slopes) == field.p * field.p

    mismatches: list[dict[str, object]] = []
    if rank != params["expected_rank"]:
        mismatches.append(
            {"type": "quadric_rank", "expected": params["expected_rank"], "actual": rank}
        )
    if zero_quadric != params["expected_zero"]:
        mismatches.append(
            {
                "type": "quadric_zero",
                "expected": params["expected_zero"],
                "actual": zero_quadric,
            }
        )
    if zero_quadric and rank > 2:
        mismatches.append({"type": "zero_quadric_rank_bound", "rank": rank})
    if zero_quadric and rank >= 2 and not (common_kernel_ruling or common_image_ruling):
        mismatches.append(
            {
                "type": "zero_quadric_ruling_missing",
                "common_kernel": common_kernel_ruling,
                "common_image": common_image_ruling,
            }
        )
    if global_rank_defective != params["expected_global_rank_defective"]:
        mismatches.append(
            {
                "type": "global_rank_defective",
                "expected": params["expected_global_rank_defective"],
                "actual": global_rank_defective,
            }
        )
    if not global_rank_defective and len(rank_defective_slopes) > 2:
        mismatches.append(
            {
                "type": "rank_defective_bound",
                "rank_defective_slopes": rank_defective_slopes[:5],
                "count": len(rank_defective_slopes),
            }
        )

    samples = standard_basis(field, j + 1)
    width = j + 1
    samples.extend(
        vector_add(field, samples[left], samples[right])
        for left in range(width)
        for right in range(left + 1, width)
    )
    for sample in samples:
        det_value = determinant_from_rows(field, rows, sample)
        coeff_value = eval_quadratic_coefficients(field, coeffs, sample)
        if det_value != coeff_value:
            mismatches.append(
                {
                    "type": "quadric_coefficient_eval",
                    "sample": sample,
                    "determinant": det_value,
                    "coefficients": coeff_value,
                }
            )
            break

    return {
        "name": params["name"],
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "j": j,
        "rank": rank,
        "zero_quadric": zero_quadric,
        "common_kernel_ruling": common_kernel_ruling,
        "common_image_ruling": common_image_ruling,
        "rank_defective_slope_count": len(rank_defective_slopes),
        "global_rank_defective": global_rank_defective,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def run_reduced_line_case(params: dict[str, object]) -> dict[str, object]:
    p = int(params["p"])
    field = QuadraticField(p=p, d=least_nonsquare(p))
    generators = [
        [[tuple(entry) for entry in row] for row in generator]
        for generator in params["generators"]
    ]
    first, second = generators
    rows = [
        [first[0][0], second[0][0]],
        [first[1][0], second[1][0]],
        [first[0][1], second[0][1]],
        [first[1][1], second[1][1]],
    ]
    common_kernel = has_common_kernel_ruling(field, rows)
    common_image = has_common_image_ruling(field, rows)
    zero_points = 0
    slopes: set[Element] = set()
    for left, right in projective_line_parameters(field):
        matrix = line_matrix(field, first, second, left, right)
        if matrix_determinant_2x2(field, matrix) != field.zero:
            continue
        zero_points += 1
        slope = projective_slope(
            field,
            [matrix[0][0], matrix[1][0]],
            [matrix[0][1], matrix[1][1]],
        )
        if slope is not None:
            slopes.add(slope)

    contained = zero_points == field.p * field.p + 1
    mismatches: list[dict[str, object]] = []
    if contained != params["expected_contained"]:
        mismatches.append(
            {
                "type": "line_contained",
                "expected": params["expected_contained"],
                "actual": contained,
            }
        )
    if zero_points != params["expected_zero_points"]:
        mismatches.append(
            {
                "type": "line_zero_points",
                "expected": params["expected_zero_points"],
                "actual": zero_points,
            }
        )
    if len(slopes) != params["expected_slope_count"]:
        mismatches.append(
            {
                "type": "line_slope_count",
                "expected": params["expected_slope_count"],
                "actual": len(slopes),
            }
        )
    if common_kernel != params["expected_common_kernel"]:
        mismatches.append(
            {
                "type": "line_common_kernel",
                "expected": params["expected_common_kernel"],
                "actual": common_kernel,
            }
        )
    if common_image != params["expected_common_image"]:
        mismatches.append(
            {
                "type": "line_common_image",
                "expected": params["expected_common_image"],
                "actual": common_image,
            }
        )
    if not contained and zero_points > 2:
        mismatches.append({"type": "line_transverse_bound", "zero_points": zero_points})
    if contained and common_kernel and len(slopes) > 1:
        mismatches.append({"type": "line_common_kernel_slope_bound", "slopes": len(slopes)})

    return {
        "name": params["name"],
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "contained_in_quadric": contained,
        "zero_points": zero_points,
        "slope_count": len(slopes),
        "common_kernel_ruling": common_kernel,
        "common_image_ruling": common_image,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def run_j2_fiber_case(params: dict[str, object]) -> dict[str, object]:
    p = int(params["p"])
    field = QuadraticField(p=p, d=least_nonsquare(p))
    domain = [field.element(int(value)) for value in params["domain"]]
    rows = [[tuple(entry) for entry in row] for row in params["rows"]]
    rank = matrix_rank(field, rows)
    landings = 0
    for x, y in itertools.combinations(domain, 2):
        locator = locator_coefficients(field, [x, y])
        if all(dot(field, row, locator) == field.zero for row in rows):
            landings += 1

    mismatches: list[dict[str, object]] = []
    if rank != params["expected_rank"]:
        mismatches.append(
            {"type": "j2_fiber_rank", "expected": params["expected_rank"], "actual": rank}
        )
    if landings != params["expected_landings"]:
        mismatches.append(
            {
                "type": "j2_fiber_landing_count",
                "expected": params["expected_landings"],
                "actual": landings,
            }
        )
    if rank == 2 and landings > 1:
        mismatches.append({"type": "j2_rank2_bound", "landings": landings})
    if rank == 1 and landings > len(domain):
        mismatches.append(
            {"type": "j2_rank1_bound", "landings": landings, "n": len(domain)}
        )

    return {
        "name": params["name"],
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "domain_size": len(domain),
        "rank": rank,
        "landings": landings,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def run_j3_fiber_case(params: dict[str, object]) -> dict[str, object]:
    p = int(params["p"])
    field = QuadraticField(p=p, d=least_nonsquare(p))
    domain = [field.element(int(value)) for value in params["domain"]]
    rows = [[tuple(entry) for entry in row] for row in params["rows"]]
    monic_rows = [row[:3] for row in rows]
    rank = matrix_rank(field, rows)
    monic_rank = matrix_rank(field, monic_rows)
    landings = 0
    for roots in itertools.combinations(domain, 3):
        locator = locator_coefficients(field, roots)
        if all(dot(field, row, locator) == field.zero for row in rows):
            landings += 1

    mismatches: list[dict[str, object]] = []
    if rank != params["expected_rank"]:
        mismatches.append(
            {"type": "j3_fiber_rank", "expected": params["expected_rank"], "actual": rank}
        )
    if monic_rank != params["expected_monic_rank"]:
        mismatches.append(
            {
                "type": "j3_fiber_monic_rank",
                "expected": params["expected_monic_rank"],
                "actual": monic_rank,
            }
        )
    if landings != params["expected_landings"]:
        mismatches.append(
            {
                "type": "j3_fiber_landing_count",
                "expected": params["expected_landings"],
                "actual": landings,
            }
        )
    if monic_rank == 2 and landings > len(domain):
        mismatches.append(
            {"type": "j3_monic_rank2_bound", "landings": landings, "n": len(domain)}
        )

    return {
        "name": params["name"],
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "domain_size": len(domain),
        "rank": rank,
        "monic_rank": monic_rank,
        "landings": landings,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def run_general_fixed_slope_case(params: dict[str, object]) -> dict[str, object]:
    p = int(params["p"])
    j = int(params["j"])
    field = QuadraticField(p=p, d=least_nonsquare(p))
    domain = [field.element(int(value)) for value in params["domain"]]
    rows = [[tuple(entry) for entry in row] for row in params["rows"]]
    monic_rows = [row[:j] for row in rows]
    rank = matrix_rank(field, rows)
    monic_rank = matrix_rank(field, monic_rows)
    landings = 0
    for roots in itertools.combinations(domain, j):
        locator = locator_coefficients(field, roots)
        if all(dot(field, row, locator) == field.zero for row in rows):
            landings += 1

    regular_bound = comb(len(domain), j - 2)
    mismatches: list[dict[str, object]] = []
    if rank != params["expected_rank"]:
        mismatches.append(
            {
                "type": "general_fiber_rank",
                "expected": params["expected_rank"],
                "actual": rank,
            }
        )
    if monic_rank != params["expected_monic_rank"]:
        mismatches.append(
            {
                "type": "general_fiber_monic_rank",
                "expected": params["expected_monic_rank"],
                "actual": monic_rank,
            }
        )
    if landings != params["expected_landings"]:
        mismatches.append(
            {
                "type": "general_fiber_landing_count",
                "expected": params["expected_landings"],
                "actual": landings,
            }
        )
    if monic_rank == 2 and landings > regular_bound:
        mismatches.append(
            {
                "type": "general_monic_rank2_bound",
                "landings": landings,
                "bound": regular_bound,
            }
        )

    return {
        "name": params["name"],
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "domain_size": len(domain),
        "j": j,
        "rank": rank,
        "monic_rank": monic_rank,
        "landings": landings,
        "regular_bound": regular_bound,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def run_row_cut_resonance_case(params: dict[str, object]) -> dict[str, object]:
    p = int(params["p"])
    j = int(params["j"])
    field = QuadraticField(p=p, d=least_nonsquare(p))
    domain = [field.element(int(value)) for value in params["domain"]]
    rows = [[tuple(entry) for entry in row] for row in params["rows"]]
    rank = matrix_rank(field, rows)
    landings = 0
    landing_locators = []
    for roots in itertools.combinations(domain, j):
        locator = locator_coefficients(field, roots)
        if all(dot(field, row, locator) == field.zero for row in rows):
            landings += 1
            landing_locators.append((roots, locator))

    rank_one_bound = comb(len(domain), j - 1)
    alpha = field.element(int(params["alpha"])) if "alpha" in params else None
    star_locators = [
        locator for roots, locator in landing_locators if alpha is not None and alpha in roots
    ]
    star_span_rank = matrix_rank(field, star_locators)
    root_slice_counts = {
        root: sum(1 for roots, _locator in landing_locators if root in roots)
        for root in domain
    }
    full_star_size = comb(len(domain) - 1, j - 1)
    full_star_count = sum(1 for count in root_slice_counts.values() if count == full_star_size)
    max_root_slice = max(root_slice_counts.values(), default=0)
    star_free_bound = len(domain) * comb(len(domain) - 1, j - 2) // j
    evaluation_row = (
        [field.pow(alpha, degree) for degree in range(j + 1)]
        if alpha is not None
        else []
    )
    row_is_evaluation = (
        bool(rows)
        and alpha is not None
        and is_scalar_multiple(field, rows[0], evaluation_row)
    )
    mismatches: list[dict[str, object]] = []
    if rank != params["expected_rank"]:
        mismatches.append(
            {
                "type": "row_cut_rank",
                "expected": params["expected_rank"],
                "actual": rank,
            }
        )
    if landings != params["expected_landings"]:
        mismatches.append(
            {
                "type": "row_cut_landing_count",
                "expected": params["expected_landings"],
                "actual": landings,
            }
        )
    if rank == 1 and landings > rank_one_bound:
        mismatches.append(
            {
                "type": "row_cut_rank_one_bound",
                "landings": landings,
                "bound": rank_one_bound,
            }
        )
    if "expected_star_span_rank" in params and star_span_rank != params["expected_star_span_rank"]:
        mismatches.append(
            {
                "type": "row_cut_star_span_rank",
                "expected": params["expected_star_span_rank"],
                "actual": star_span_rank,
            }
        )
    if alpha is not None and rank == 1 and not row_is_evaluation:
        mismatches.append({"type": "row_cut_not_evaluation"})
    if "expected_full_star_count" in params and full_star_count != params["expected_full_star_count"]:
        mismatches.append(
            {
                "type": "row_cut_full_star_count",
                "expected": params["expected_full_star_count"],
                "actual": full_star_count,
            }
        )
    if "expected_star_free_bound" in params and star_free_bound != params["expected_star_free_bound"]:
        mismatches.append(
            {
                "type": "row_cut_star_free_bound_value",
                "expected": params["expected_star_free_bound"],
                "actual": star_free_bound,
            }
        )
    if "expected_max_root_slice" in params and max_root_slice != params["expected_max_root_slice"]:
        mismatches.append(
            {
                "type": "row_cut_max_root_slice",
                "expected": params["expected_max_root_slice"],
                "actual": max_root_slice,
            }
        )
    if rank == 1 and full_star_count == 0 and landings > star_free_bound:
        mismatches.append(
            {
                "type": "row_cut_star_free_bound",
                "landings": landings,
                "bound": star_free_bound,
            }
        )

    return {
        "name": params["name"],
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "domain_size": len(domain),
        "j": j,
        "rank": rank,
        "landings": landings,
        "rank_one_bound": rank_one_bound,
        "star_span_rank": star_span_rank,
        "row_is_evaluation": row_is_evaluation,
        "full_star_count": full_star_count,
        "max_root_slice": max_root_slice,
        "star_free_bound": star_free_bound,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def run_global_monic_rank_one_case(params: dict[str, object]) -> dict[str, object]:
    p = int(params["p"])
    j = int(params.get("j", 3))
    field = QuadraticField(p=p, d=least_nonsquare(p))
    domain = [field.element(int(value)) for value in params["domain"]]
    u = [tuple(value) for value in params["u"]]
    v = [tuple(value) for value in params["v"]]
    left = hankel_matrix(u, 2, j)
    right = hankel_matrix(v, 2, j)
    complements = [
        (roots, locator_coefficients(field, roots))
        for roots in itertools.combinations(domain, j)
    ]
    kind = str(params["kind"])
    alpha = field.element(int(params["alpha"])) if kind == "finite" else None
    alpha_in_domain = alpha in domain if alpha is not None else False
    finite_vector = None
    if alpha is not None:
        finite_vector = [field.pow(alpha, degree) for degree in range(j + 1)]
    infinity_vector = [field.zero] * j + [field.one]

    mismatches: list[dict[str, object]] = []
    nonzero_slope_count = 0
    scalar_zero_slope_count = 0
    max_nonzero_landings = 0
    max_scalar_zero_landings = 0
    contraction_zero_slope_count = 0
    max_contracted_landings = 0
    max_zero_contraction_landings = 0
    noncontained_slopes: set[Element] = set()
    nonzero_noncontained_slopes: set[Element] = set()
    all_slope_subsets_removed = 0

    for slope in field.elements():
        pencil = pencil_at_slope(field, left, right, slope)
        monic_rank = matrix_rank(field, [row[:j] for row in pencil])
        if monic_rank > 1:
            mismatches.append(
                {"type": "global_monic_rank", "slope": slope, "monic_rank": monic_rank}
            )
            continue

        landings = [
            (roots, locator)
            for roots, locator in complements
            if all(dot(field, row, locator) == field.zero for row in pencil)
        ]
        noncontained_landings = [
            roots
            for roots, locator in landings
            if any(dot(field, row, locator) != field.zero for row in right)
        ]
        if noncontained_landings:
            noncontained_slopes.add(slope)
        row0 = pencil[0]
        if kind == "finite":
            assert finite_vector is not None and alpha is not None
            scalar = row0[0]
            expected_row = [field.mul(scalar, value) for value in finite_vector]
            if row0 != expected_row:
                mismatches.append(
                    {
                        "type": "finite_twisted_row",
                        "slope": slope,
                        "row0": row0,
                        "expected": expected_row,
                    }
                )
                continue
            if scalar == field.zero:
                scalar_zero_slope_count += 1
                max_scalar_zero_landings = max(max_scalar_zero_landings, len(landings))
                continue
            if noncontained_landings:
                nonzero_noncontained_slopes.add(slope)
            nonzero_slope_count += 1
            max_nonzero_landings = max(max_nonzero_landings, len(landings))
            if not alpha_in_domain and landings:
                mismatches.append(
                    {
                        "type": "outside_root_landing",
                        "slope": slope,
                        "landings": [roots for roots, _locator in landings[:5]],
                    }
                )
            if alpha_in_domain and any(alpha not in roots for roots, _locator in landings):
                mismatches.append(
                    {
                        "type": "finite_root_star_violation",
                        "slope": slope,
                        "alpha": alpha,
                        "landings": [roots for roots, _locator in landings[:5]],
                    }
                )
            expected_star = comb(len(domain) - 1, j - 1) if alpha_in_domain else 0
            if alpha_in_domain and len(landings) > expected_star:
                mismatches.append(
                    {
                        "type": "finite_root_star_bound",
                        "slope": slope,
                        "landings": len(landings),
                    }
                    )
            if alpha_in_domain:
                contracted = contract_row_at_root(field, pencil[1], alpha)
                contracted_zero = is_zero_vector(field, contracted)
                if contracted_zero:
                    contraction_zero_slope_count += 1
                    max_zero_contraction_landings = max(
                        max_zero_contraction_landings, len(landings)
                    )
                    if len(landings) != expected_star:
                        mismatches.append(
                            {
                                "type": "zero_contraction_star_count",
                                "slope": slope,
                                "landings": len(landings),
                                "expected": expected_star,
                            }
                        )
                else:
                    max_contracted_landings = max(max_contracted_landings, len(landings))
                    contracted_bound = comb(len(domain) - 1, j - 2)
                    if len(landings) > contracted_bound:
                        mismatches.append(
                            {
                                "type": "contracted_fixed_root_bound",
                                "slope": slope,
                                "landings": len(landings),
                                "bound": contracted_bound,
                            }
                        )
                for roots, locator in landings:
                    if alpha not in roots:
                        continue
                    other_roots = [root for root in roots if root != alpha]
                    if len(other_roots) != j - 1:
                        continue
                    contracted_constant = contract_row_at_root(field, left[1], alpha)
                    contracted_slope = contract_row_at_root(field, right[1], alpha)
                    residual_locator = locator_coefficients(field, other_roots)
                    if (
                        dot(field, contracted_constant, residual_locator) == field.zero
                        and dot(field, contracted_slope, residual_locator) == field.zero
                    ):
                        if any(dot(field, row, locator) != field.zero for row in right):
                            mismatches.append(
                                {
                                    "type": "all_slope_pair_not_removed",
                                    "roots": roots,
                                }
                            )
                        else:
                            all_slope_subsets_removed += 1
        else:
            scalar = row0[j]
            expected_row = [field.mul(scalar, value) for value in infinity_vector]
            if row0 != expected_row:
                mismatches.append(
                    {
                        "type": "infinity_twisted_row",
                        "slope": slope,
                        "row0": row0,
                        "expected": expected_row,
                    }
                )
                continue
            if scalar == field.zero:
                scalar_zero_slope_count += 1
                max_scalar_zero_landings = max(max_scalar_zero_landings, len(landings))
                continue
            if noncontained_landings:
                nonzero_noncontained_slopes.add(slope)
            nonzero_slope_count += 1
            max_nonzero_landings = max(max_nonzero_landings, len(landings))
            if landings:
                mismatches.append(
                    {
                        "type": "infinity_nonzero_landing",
                        "slope": slope,
                        "landings": [roots for roots, _locator in landings[:5]],
                    }
                )
    if kind == "finite" and alpha_in_domain:
        bound = comb(len(domain) - 1, j - 1)
        if len(nonzero_noncontained_slopes) > bound:
            mismatches.append(
                {
                    "type": "finite_root_noncontained_slope_bound",
                    "count": len(nonzero_noncontained_slopes),
                    "bound": bound,
                }
            )
        if len(noncontained_slopes) > bound + 1:
            mismatches.append(
                {
                    "type": "finite_root_total_slope_bound",
                    "count": len(noncontained_slopes),
                    "bound": bound + 1,
                }
            )
    elif len(noncontained_slopes) > 1:
        mismatches.append(
            {
                "type": "empty_or_infinity_total_slope_bound",
                "count": len(noncontained_slopes),
            }
        )

    return {
        "name": params["name"],
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "domain_size": len(domain),
        "j": j,
        "kind": kind,
        "nonzero_slope_count": nonzero_slope_count,
        "scalar_zero_slope_count": scalar_zero_slope_count,
        "max_nonzero_landings": max_nonzero_landings,
        "max_scalar_zero_landings": max_scalar_zero_landings,
        "contraction_zero_slope_count": contraction_zero_slope_count,
        "max_contracted_landings": max_contracted_landings,
        "max_zero_contraction_landings": max_zero_contraction_landings,
        "noncontained_slope_count": len(noncontained_slopes),
        "nonzero_noncontained_slope_count": len(nonzero_noncontained_slopes),
        "all_slope_subsets_removed": all_slope_subsets_removed,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def divisors(value: int) -> list[int]:
    return [candidate for candidate in range(2, value) if value % candidate == 0]


def quotient_periodic_checks(
    field: QuadraticField,
    points: Sequence[Element],
    u: Sequence[Element],
    v: Sequence[Element],
    n: int,
    j: int,
    t: int,
) -> tuple[int, list[dict[str, object]]]:
    mismatches: list[dict[str, object]] = []
    checks = 0
    for fiber_size in divisors(n):
        if j % fiber_size != 0:
            continue
        quotient_size = j // fiber_size
        quotient_fibers: dict[Element, list[int]] = {}
        for index, point in enumerate(points):
            quotient_fibers.setdefault(field.pow(point, fiber_size), []).append(index)
        if any(len(fiber) != fiber_size for fiber in quotient_fibers.values()):
            mismatches.append(
                {
                    "type": "quotient_fiber_size",
                    "fiber_size": fiber_size,
                    "fiber_sizes": sorted(len(fiber) for fiber in quotient_fibers.values()),
                }
            )
            continue
        quotient_points = sorted(quotient_fibers)
        if quotient_size == 0 or quotient_size > len(quotient_points):
            continue
        for quotient_subset in itertools.combinations(quotient_points, quotient_size):
            complement = tuple(
                sorted(
                    index
                    for quotient_point in quotient_subset
                    for index in quotient_fibers[quotient_point]
                )
            )
            direct_locator = locator_coefficients(
                field,
                [points[index] for index in complement],
            )
            quotient_locator = locator_coefficients(field, quotient_subset)
            pullback_locator = [field.zero] * (j + 1)
            for s, coeff in enumerate(quotient_locator):
                pullback_locator[fiber_size * s] = coeff
            direct_u = hankel_product(field, u, direct_locator, t)
            direct_v = hankel_product(field, v, direct_locator, t)
            decimated_u = decimated_hankel_product(field, u, quotient_locator, fiber_size, t)
            decimated_v = decimated_hankel_product(field, v, quotient_locator, fiber_size, t)
            checks += 1
            if direct_locator != pullback_locator:
                mismatches.append(
                    {
                        "type": "quotient_locator_pullback",
                        "fiber_size": fiber_size,
                        "quotient_subset": quotient_subset,
                        "direct_locator": direct_locator,
                        "pullback_locator": pullback_locator,
                    }
                )
            if direct_u != decimated_u or direct_v != decimated_v:
                mismatches.append(
                    {
                        "type": "quotient_decimated_hankel",
                        "fiber_size": fiber_size,
                        "quotient_subset": quotient_subset,
                    }
                )
            if t == 2:
                direct_slope = projective_slope(field, direct_u, direct_v)
                decimated_slope = projective_slope(field, decimated_u, decimated_v)
                if direct_slope != decimated_slope:
                    mismatches.append(
                        {
                            "type": "quotient_projective_slope",
                            "fiber_size": fiber_size,
                            "quotient_subset": quotient_subset,
                            "direct_slope": direct_slope,
                            "decimated_slope": decimated_slope,
                        }
                    )
    return checks, mismatches


def fixed_slope_j2_checks(
    field: QuadraticField,
    points: Sequence[Element],
    u: Sequence[Element],
    v: Sequence[Element],
    n: int,
    j: int,
    t: int,
) -> tuple[dict[str, int], list[dict[str, object]]]:
    if j != 2 or t != 2:
        return {"checks": 0, "max_rank2_landings": 0, "max_rank1_landings": 0}, []

    left = hankel_matrix(u, t, j)
    right = hankel_matrix(v, t, j)
    complements = [
        locator_coefficients(field, [points[left_index], points[right_index]])
        for left_index, right_index in itertools.combinations(range(n), 2)
    ]
    mismatches: list[dict[str, object]] = []
    max_rank2_landings = 0
    max_rank1_landings = 0
    checks = 0

    for slope in field.elements():
        pencil = pencil_at_slope(field, left, right, slope)
        rank = matrix_rank(field, pencil)
        landings = sum(
            1
            for locator in complements
            if all(dot(field, row, locator) == field.zero for row in pencil)
        )
        checks += 1
        if rank == 2:
            max_rank2_landings = max(max_rank2_landings, landings)
            if landings > 1:
                mismatches.append(
                    {
                        "type": "j2_rank2_fiber_bound",
                        "slope": slope,
                        "landings": landings,
                    }
                )
        elif rank == 1:
            max_rank1_landings = max(max_rank1_landings, landings)
            if landings > n:
                mismatches.append(
                    {
                        "type": "j2_rank1_fiber_bound",
                        "slope": slope,
                        "landings": landings,
                        "n": n,
                    }
                )
    return {
        "checks": checks,
        "max_rank2_landings": max_rank2_landings,
        "max_rank1_landings": max_rank1_landings,
    }, mismatches


def fixed_slope_j3_checks(
    field: QuadraticField,
    points: Sequence[Element],
    u: Sequence[Element],
    v: Sequence[Element],
    n: int,
    j: int,
    t: int,
) -> tuple[dict[str, int], list[dict[str, object]]]:
    if j != 3 or t != 2:
        return {"checks": 0, "max_monic_rank2_landings": 0}, []

    left = hankel_matrix(u, t, j)
    right = hankel_matrix(v, t, j)
    complements = [
        locator_coefficients(field, [points[a], points[b], points[c]])
        for a, b, c in itertools.combinations(range(n), 3)
    ]
    mismatches: list[dict[str, object]] = []
    max_monic_rank2_landings = 0
    checks = 0

    for slope in field.elements():
        pencil = pencil_at_slope(field, left, right, slope)
        monic_rank = matrix_rank(field, [row[:3] for row in pencil])
        landings = sum(
            1
            for locator in complements
            if all(dot(field, row, locator) == field.zero for row in pencil)
        )
        checks += 1
        if monic_rank == 2:
            max_monic_rank2_landings = max(max_monic_rank2_landings, landings)
            if landings > n:
                mismatches.append(
                    {
                        "type": "j3_monic_rank2_fiber_bound",
                        "slope": slope,
                        "landings": landings,
                        "n": n,
                    }
                )
    return {
        "checks": checks,
        "max_monic_rank2_landings": max_monic_rank2_landings,
    }, mismatches


def run_case(params: dict[str, int]) -> dict[str, object]:
    p = params["p"]
    n = params["n"]
    k = params["k"]
    agreement = params["agreement"]
    r = n - k
    j = n - agreement
    t = agreement - k
    if t <= 0 or j < 0 or t != r - j:
        raise ValueError(f"inconsistent case {params}")

    field = QuadraticField(p=p, d=least_nonsquare(p))
    base_points = subgroup_points(p, n)
    points = [field.element(x) for x in base_points]
    weights = dual_weights(field, points)
    base_weights = base_dual_weights(p, base_points)
    f_word = deterministic_word(field, points, salt=1)
    g_word = deterministic_word(field, points, salt=4)
    u = syndrome(field, points, weights, f_word, r)
    v = syndrome(field, points, weights, g_word, r)
    coordinate_syndrome_passed = True
    for word, syn in ((f_word, u), (g_word, v)):
        for coord in (0, 1):
            base_values = [value[coord] for value in word]
            base_syn = base_syndrome(p, base_points, base_weights, base_values, r)
            coordinate_syndrome_passed &= base_syn == [value[coord] for value in syn]

    mismatches: list[dict[str, object]] = []
    if not coordinate_syndrome_passed:
        mismatches.append({"type": "coordinate_syndrome"})
    bad_slopes: set[Element] = set()
    support_count = 0
    slope_tests = 0
    max_reduced_dimension = 0
    projective_gate_supports = 0
    quotient_checks, quotient_mismatches = quotient_periodic_checks(
        field, points, u, v, n, j, t
    )
    mismatches.extend(quotient_mismatches)
    j2_fiber_summary, j2_fiber_mismatches = fixed_slope_j2_checks(
        field, points, u, v, n, j, t
    )
    mismatches.extend(j2_fiber_mismatches)
    j3_fiber_summary, j3_fiber_mismatches = fixed_slope_j3_checks(
        field, points, u, v, n, j, t
    )
    mismatches.extend(j3_fiber_mismatches)

    for complement in itertools.combinations(range(n), j):
        support = tuple(index for index in range(n) if index not in complement)
        complement_points = [points[index] for index in complement]
        locator = locator_coefficients(field, complement_points)
        hu = hankel_product(field, u, locator, t)
        hv = hankel_product(field, v, locator, t)

        stacked = hankel_matrix(u, t, j) + hankel_matrix(v, t, j)
        reduced_dimension = matrix_rank(field, stacked)
        max_reduced_dimension = max(max_reduced_dimension, reduced_dimension)
        if reduced_dimension > 2 * t:
            mismatches.append(
                {
                    "type": "reduced_dimension_bound",
                    "complement": complement,
                    "reduced_dimension": reduced_dimension,
                    "2t": 2 * t,
                }
            )

        f_explained = explained_on_support(field, points, f_word, support, k)
        g_explained = explained_on_support(field, points, g_word, support, k)
        support_bad_slopes: set[Element] = set()

        for z in field.elements():
            line_word = [
                field.add(f_value, field.mul(z, g_value))
                for f_value, g_value in zip(f_word, g_word)
            ]
            direct_explained = explained_on_support(field, points, line_word, support, k)
            pencil_value = vector_add(field, hu, scalar_vector_mul(field, z, hv))
            pencil_explained = is_zero_vector(field, pencil_value)
            direct_bad = direct_explained and not (f_explained and g_explained)
            pencil_bad = pencil_explained and not is_zero_vector(field, hv)
            slope_tests += 1
            if direct_explained != pencil_explained or direct_bad != pencil_bad:
                mismatches.append(
                    {
                        "type": "criterion",
                        "complement": complement,
                        "z": z,
                        "direct_explained": direct_explained,
                        "pencil_explained": pencil_explained,
                        "direct_bad": direct_bad,
                        "pencil_bad": pencil_bad,
                    }
                )
                continue
            if pencil_bad:
                bad_slopes.add(z)
                support_bad_slopes.add(z)

        gated_slope = projective_slope(field, hu, hv)
        if gated_slope is None:
            if support_bad_slopes:
                mismatches.append(
                    {
                        "type": "projective_gate_missing",
                        "complement": complement,
                        "support_bad_slopes": sorted(support_bad_slopes),
                    }
                )
        else:
            projective_gate_supports += 1
            if support_bad_slopes != {gated_slope}:
                mismatches.append(
                    {
                        "type": "projective_gate_slope",
                        "complement": complement,
                        "gated_slope": gated_slope,
                        "support_bad_slopes": sorted(support_bad_slopes),
                    }
                )
        support_count += 1

    return {
        "params": {
            **params,
            "field": f"F_{p}[u]/(u^2-{field.d})",
            "r": r,
            "j": j,
            "t": t,
            "domain": base_points,
        },
        "support_complements": support_count,
        "slope_tests": slope_tests,
        "bad_slope_count": len(bad_slopes),
        "projective_gate_supports": projective_gate_supports,
        "coordinate_syndrome_passed": coordinate_syndrome_passed,
        "quotient_periodic_checks": quotient_checks,
        "j2_fiber_checks": j2_fiber_summary["checks"],
        "j2_max_rank2_landings": j2_fiber_summary["max_rank2_landings"],
        "j2_max_rank1_landings": j2_fiber_summary["max_rank1_landings"],
        "j3_fiber_checks": j3_fiber_summary["checks"],
        "j3_max_monic_rank2_landings": j3_fiber_summary["max_monic_rank2_landings"],
        "max_reduced_dimension": max_reduced_dimension,
        "dimension_bound": 2 * t,
        "passed": not mismatches,
        "mismatches": mismatches[:5],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON certificate")
    args = parser.parse_args()

    records = [run_case(case) for case in CASES]
    quadric_records = [run_quadric_case(case) for case in QUADRIC_ONLY_CASES]
    reduced_line_records = [
        run_reduced_line_case(case) for case in REDUCED_LINE_SECTION_CASES
    ]
    j2_fiber_records = [run_j2_fiber_case(case) for case in J2_FIBER_ONLY_CASES]
    j3_fiber_records = [run_j3_fiber_case(case) for case in J3_FIBER_ONLY_CASES]
    general_fixed_slope_records = [
        run_general_fixed_slope_case(case) for case in GENERAL_FIXED_SLOPE_CASES
    ]
    row_cut_records = [
        run_row_cut_resonance_case(case) for case in ROW_CUT_RESONANCE_CASES
    ]
    global_monic_records = [
        run_global_monic_rank_one_case(case) for case in GLOBAL_MONIC_RANK_ONE_CASES
    ]
    passed = all(
        record["passed"]
        for record in (
            records
            + quadric_records
            + reduced_line_records
            + j2_fiber_records
            + j3_fiber_records
            + general_fixed_slope_records
            + row_cut_records
            + global_monic_records
        )
    )
    certificate = {
        "status": "AUDIT / EXPERIMENTAL",
        "theorem": "F1 syndrome-pencil normal form",
        "passed": passed,
        "cases": records,
        "quadric_only_cases": quadric_records,
        "reduced_line_section_cases": reduced_line_records,
        "j2_fiber_only_cases": j2_fiber_records,
        "j3_fiber_only_cases": j3_fiber_records,
        "general_fixed_slope_cases": general_fixed_slope_records,
        "row_cut_resonance_cases": row_cut_records,
        "global_monic_rank_one_cases": global_monic_records,
    }
    if args.json:
        print(json.dumps(certificate, indent=2))
    else:
        print("F1 syndrome-pencil normal-form verifier")
        for record in records:
            params = record["params"]
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {params['field']}, n={params['n']}, k={params['k']}, "
                f"agreement={params['agreement']}, j={params['j']}, t={params['t']}: "
                f"{record['slope_tests']} slope/support tests, "
                f"{record['bad_slope_count']} bad slopes, "
                f"{record['projective_gate_supports']} gated supports, "
                f"coordinate syndrome={'OK' if record['coordinate_syndrome_passed'] else 'FAIL'}, "
                f"quotient checks={record['quotient_periodic_checks']}, "
                f"j2 fiber checks={record['j2_fiber_checks']}, "
                f"j2 rank2 max={record['j2_max_rank2_landings']}, "
                f"j2 rank1 max={record['j2_max_rank1_landings']}, "
                f"j3 fiber checks={record['j3_fiber_checks']}, "
                f"j3 monic-rank2 max={record['j3_max_monic_rank2_landings']}, "
                f"max dim(V)={record['max_reduced_dimension']} <= {record['dimension_bound']}"
            )
        for record in quadric_records:
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {record['name']}: {record['field']}, j={record['j']}, "
                f"rank={record['rank']}, zero_quadric={record['zero_quadric']}, "
                f"common_kernel={record['common_kernel_ruling']}, "
                f"common_image={record['common_image_ruling']}, "
                f"rank-defective slopes={record['rank_defective_slope_count']}, "
                f"global_rank_defective={record['global_rank_defective']}"
            )
        for record in reduced_line_records:
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {record['name']}: {record['field']}, "
                f"contained={record['contained_in_quadric']}, "
                f"zero points={record['zero_points']}, slopes={record['slope_count']}, "
                f"common_kernel={record['common_kernel_ruling']}, "
                f"common_image={record['common_image_ruling']}"
            )
        for record in j2_fiber_records:
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {record['name']}: {record['field']}, "
                f"|D|={record['domain_size']}, rank={record['rank']}, "
                f"landings={record['landings']}"
            )
        for record in j3_fiber_records:
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {record['name']}: {record['field']}, "
                f"|D|={record['domain_size']}, rank={record['rank']}, "
                f"monic_rank={record['monic_rank']}, landings={record['landings']}"
            )
        for record in general_fixed_slope_records:
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {record['name']}: {record['field']}, "
                f"|D|={record['domain_size']}, j={record['j']}, "
                f"monic_rank={record['monic_rank']}, landings={record['landings']} "
                f"<= {record['regular_bound']}"
            )
        for record in row_cut_records:
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {record['name']}: {record['field']}, "
                f"|D|={record['domain_size']}, j={record['j']}, "
                f"rank={record['rank']}, landings={record['landings']} "
                f"<= {record['rank_one_bound']}, "
                f"star span={record['star_span_rank']}, "
                f"evaluation row={record['row_is_evaluation']}, "
                f"full stars={record['full_star_count']}, "
                f"max root slice={record['max_root_slice']}, "
                f"star-free bound={record['star_free_bound']}"
            )
        for record in global_monic_records:
            flag = "PASS" if record["passed"] else "FAIL"
            print(
                f"  [{flag}] {record['name']}: {record['field']}, "
                f"|D|={record['domain_size']}, j={record['j']}, kind={record['kind']}, "
                f"nonzero slopes={record['nonzero_slope_count']}, "
                f"scalar-zero slopes={record['scalar_zero_slope_count']}, "
                f"max nonzero landings={record['max_nonzero_landings']}, "
                f"contraction-zero slopes={record['contraction_zero_slope_count']}, "
                f"max contracted landings={record['max_contracted_landings']}, "
                f"max zero-contraction landings={record['max_zero_contraction_landings']}, "
                f"noncontained slopes={record['noncontained_slope_count']}, "
                f"nonzero noncontained slopes={record['nonzero_noncontained_slope_count']}, "
                f"all-slope subsets removed={record['all_slope_subsets_removed']}"
            )
        print(f"RESULT: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
