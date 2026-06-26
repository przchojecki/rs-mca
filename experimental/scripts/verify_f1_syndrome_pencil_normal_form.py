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
from typing import Iterable, Sequence

Element = tuple[int, int]
Matrix = list[list[Element]]

CASES = (
    {"p": 5, "n": 4, "k": 2, "agreement": 3},
    {"p": 7, "n": 6, "k": 3, "agreement": 5},
    {"p": 7, "n": 6, "k": 2, "agreement": 4},
    {"p": 17, "n": 8, "k": 4, "agreement": 6},
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
    passed = all(record["passed"] for record in records)
    certificate = {
        "status": "AUDIT / EXPERIMENTAL",
        "theorem": "F1 syndrome-pencil normal form",
        "passed": passed,
        "cases": records,
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
                f"max dim(V)={record['max_reduced_dimension']} <= {record['dimension_bound']}"
            )
        print(f"RESULT: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
