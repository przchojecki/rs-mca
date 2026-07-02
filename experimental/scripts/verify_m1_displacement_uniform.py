#!/usr/bin/env python3
"""Verify uniform subgroup Hankel displacement identities.

This is the Q2.5 / displacement_uniform packet.  It checks the elementary
algebra behind the spectral/XR route over three fields:

    (F_13, mu_4), (F_17, mu_16), (F_49, mu_16).

The proof note gives the symbolic argument; this script independently replays
the finite identities from the V^T D V factorization.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, Sequence


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "m1-displacement-uniform"
    / "m1_displacement_uniform_certificate.json"
)


class Field:
    name: str
    order: int

    def zero(self):
        raise NotImplementedError

    def one(self):
        raise NotImplementedError

    def elements(self) -> Iterable[object]:
        raise NotImplementedError

    def add(self, a, b):
        raise NotImplementedError

    def neg(self, a):
        raise NotImplementedError

    def mul(self, a, b):
        raise NotImplementedError

    def pow(self, a, e: int):
        out = self.one()
        base = a
        while e:
            if e & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            e >>= 1
        return out

    def sub(self, a, b):
        return self.add(a, self.neg(b))

    def inv(self, a):
        if a == self.zero():
            raise ZeroDivisionError("zero inverse")
        return self.pow(a, self.order - 2)

    def div(self, a, b):
        return self.mul(a, self.inv(b))

    def is_zero(self, a) -> bool:
        return a == self.zero()

    def encode(self, a):
        return a


class PrimeField(Field):
    def __init__(self, p: int):
        self.p = p
        self.order = p
        self.name = f"F_{p}"

    def zero(self):
        return 0

    def one(self):
        return 1

    def elements(self):
        return range(self.p)

    def add(self, a, b):
        return (a + b) % self.p

    def neg(self, a):
        return (-a) % self.p

    def mul(self, a, b):
        return (a * b) % self.p


class QuadraticField(Field):
    """F_p[u]/(u^2-d), with d a nonsquare."""

    def __init__(self, p: int, d: int):
        self.p = p
        self.d = d % p
        self.order = p * p
        self.name = f"F_{p}^2[u^2={self.d}]"

    def zero(self):
        return (0, 0)

    def one(self):
        return (1, 0)

    def elements(self):
        for a in range(self.p):
            for b in range(self.p):
                yield (a, b)

    def add(self, a, b):
        return ((a[0] + b[0]) % self.p, (a[1] + b[1]) % self.p)

    def neg(self, a):
        return ((-a[0]) % self.p, (-a[1]) % self.p)

    def mul(self, a, b):
        return (
            (a[0] * b[0] + a[1] * b[1] * self.d) % self.p,
            (a[0] * b[1] + a[1] * b[0]) % self.p,
        )

    def encode(self, a):
        return [a[0], a[1]]


def mat_zero(rows: int, cols: int, field: Field):
    return [[field.zero() for _ in range(cols)] for _ in range(rows)]


def mat_identity(n: int, field: Field):
    out = mat_zero(n, n, field)
    for i in range(n):
        out[i][i] = field.one()
    return out


def mat_transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def mat_add(a, b, field: Field):
    return [
        [field.add(a[i][j], b[i][j]) for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def mat_scalar_mul(scalar, matrix, field: Field):
    return [[field.mul(scalar, value) for value in row] for row in matrix]


def mat_mul(a, b, field: Field):
    rows, inner, cols = len(a), len(b), len(b[0])
    out = mat_zero(rows, cols, field)
    for i in range(rows):
        for k in range(inner):
            if field.is_zero(a[i][k]):
                continue
            for j in range(cols):
                out[i][j] = field.add(out[i][j], field.mul(a[i][k], b[k][j]))
    return out


def mat_diag(values, field: Field):
    out = mat_zero(len(values), len(values), field)
    for i, value in enumerate(values):
        out[i][i] = value
    return out


def det(matrix, field: Field):
    n = len(matrix)
    a = [row[:] for row in matrix]
    out = field.one()
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if not field.is_zero(a[row][col]):
                pivot = row
                break
        if pivot is None:
            return field.zero()
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            out = field.neg(out)
        pivot_value = a[col][col]
        out = field.mul(out, pivot_value)
        inv_pivot = field.inv(pivot_value)
        for row in range(col + 1, n):
            factor = field.mul(a[row][col], inv_pivot)
            if field.is_zero(factor):
                continue
            for j in range(col, n):
                a[row][j] = field.sub(a[row][j], field.mul(factor, a[col][j]))
    return out


def mat_inverse(matrix, field: Field):
    n = len(matrix)
    a = [matrix[i][:] + mat_identity(n, field)[i][:] for i in range(n)]
    for col in range(n):
        pivot = None
        for row in range(col, n):
            if not field.is_zero(a[row][col]):
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
        inv_pivot = field.inv(a[col][col])
        for j in range(2 * n):
            a[col][j] = field.mul(a[col][j], inv_pivot)
        for row in range(n):
            if row == col:
                continue
            factor = a[row][col]
            if field.is_zero(factor):
                continue
            for j in range(2 * n):
                a[row][j] = field.sub(a[row][j], field.mul(factor, a[col][j]))
    return [row[n:] for row in a]


def vandermonde(points: Sequence[object], cols: int, field: Field):
    return [[field.pow(x, c) for c in range(cols)] for x in points]


def moment_square(points: Sequence[object], h: int, size: int, field: Field):
    v = vandermonde(points, size, field)
    d = mat_diag([field.pow(x, h) for x in points], field)
    return mat_mul(mat_transpose(v), mat_mul(d, v, field), field)


def weighted_hankel(points: Sequence[object], weights: Sequence[object], rows: int, cols: int, field: Field):
    out = mat_zero(rows, cols, field)
    for a in range(rows):
        for b in range(cols):
            total = field.zero()
            for x, w in zip(points, weights):
                total = field.add(total, field.mul(w, field.pow(x, a + b)))
            out[a][b] = total
    return out


def poly_eval_at_roots(points: Sequence[object], z, field: Field):
    out = field.one()
    for x in points:
        out = field.mul(out, field.sub(z, x))
    return out


def poly_derivative_at_root(points: Sequence[object], i: int, field: Field):
    out = field.one()
    xi = points[i]
    for j, xj in enumerate(points):
        if i == j:
            continue
        out = field.mul(out, field.sub(xi, xj))
    return out


def element_order(value, field: Field):
    if value == field.zero():
        return 0
    out = field.one()
    for e in range(1, field.order):
        out = field.mul(out, value)
        if out == field.one():
            return e
    raise ValueError("no order found")


def find_order_element(field: Field, order: int):
    for value in field.elements():
        if element_order(value, field) == order:
            return value
    raise ValueError(f"no element of order {order} in {field.name}")


@dataclass(frozen=True)
class Case:
    name: str
    field: Field
    subgroup_order: int
    m: int
    r: int
    shifts: tuple[int, ...]


def check_case(case: Case) -> dict[str, object]:
    field = case.field
    alpha = find_order_element(field, case.subgroup_order)
    subgroup = [field.pow(alpha, i) for i in range(case.subgroup_order)]
    x_points = subgroup[: case.m]
    y_points = subgroup[case.m : case.m + case.r]

    if len(set(map(str, subgroup))) != case.subgroup_order:
        raise AssertionError(f"{case.name}: subgroup powers not distinct")
    if case.m + case.r > case.subgroup_order:
        raise AssertionError(f"{case.name}: Cauchy window wraps")

    # General rectangular subgroup Hankel factorization H = V^T D V.
    rows = min(case.m, 4)
    cols = min(case.m + 1, 5)
    weights = [field.add(field.pow(x, 2), field.one()) for x in subgroup]
    direct_hankel = weighted_hankel(subgroup, weights, rows, cols, field)
    v_rows = vandermonde(subgroup, rows, field)
    v_cols = vandermonde(subgroup, cols, field)
    factored_hankel = mat_mul(
        mat_transpose(v_rows),
        mat_mul(mat_diag(weights, field), v_cols, field),
        field,
    )
    hankel_factorization_ok = direct_hankel == factored_hankel

    # Toeplitz-Cauchy displacement and Lagrange interpolation factorization.
    cauchy = []
    for a in range(case.r):
        row = []
        for i in range(case.m):
            exponent = case.m + a - i
            denom = field.sub(field.one(), field.pow(alpha, exponent))
            if field.is_zero(denom):
                raise AssertionError(f"{case.name}: Cauchy denominator vanished")
            row.append(field.inv(denom))
        cauchy.append(row)

    displaced = mat_zero(case.r, case.m, field)
    for a in range(case.r):
        for i in range(case.m):
            multiplier = field.mul(field.pow(alpha, a), field.pow(alpha, case.m - i))
            displaced[a][i] = field.sub(cauchy[a][i], field.mul(multiplier, cauchy[a][i]))
    cauchy_displacement_ok = all(
        displaced[a][i] == field.one()
        for a in range(case.r)
        for i in range(case.m)
    )

    vx = vandermonde(x_points, case.m, field)
    vy = vandermonde(y_points, case.m, field)
    lagrange = mat_mul(vy, mat_inverse(vx, field), field)
    right_diag = []
    for i, xi in enumerate(x_points):
        right_diag.append(field.neg(field.div(field.inv(xi), poly_derivative_at_root(x_points, i, field))))
    lagrange_from_cauchy = mat_mul(
        mat_diag([poly_eval_at_roots(x_points, y, field) for y in y_points], field),
        mat_mul(cauchy, mat_diag(right_diag, field), field),
        field,
    )
    lagrange_cauchy_ok = lagrange == lagrange_from_cauchy

    shift_payloads = []
    determinant_lemma_ok = True
    determinant_base_ok = True
    for h in case.shifts:
        a_matrix = moment_square(x_points, h, case.m, field)
        b_matrix = moment_square(y_points, h, case.m, field)
        det_a = det(a_matrix, field)
        vx_det = det(vx, field)
        prod_x_h = field.one()
        for x in x_points:
            prod_x_h = field.mul(prod_x_h, field.pow(x, h))
        base_formula = field.mul(field.mul(vx_det, vx_det), prod_x_h)
        determinant_base_ok &= det_a == base_formula and not field.is_zero(det_a)

        inv_a = mat_inverse(a_matrix, field)
        vy_h = vandermonde(y_points, case.m, field)
        dy = mat_diag([field.pow(y, h) for y in y_points], field)
        kernel = mat_mul(dy, mat_mul(vy_h, mat_mul(inv_a, mat_transpose(vy_h), field), field), field)
        identity_r = mat_identity(case.r, field)
        evaluations_checked = 0
        for z in field.elements():
            left = det(mat_add(a_matrix, mat_scalar_mul(z, b_matrix, field), field), field)
            right = field.mul(
                det_a,
                det(mat_add(identity_r, mat_scalar_mul(z, kernel, field), field), field),
            )
            evaluations_checked += 1
            if left != right:
                determinant_lemma_ok = False
                raise AssertionError(f"{case.name}: determinant lemma failed at h={h}, z={field.encode(z)}")
        shift_payloads.append({
            "h": h,
            "det_A": field.encode(det_a),
            "det_VX": field.encode(vx_det),
            "evaluations_checked": evaluations_checked,
            "kernel_size": case.r,
        })

    ok = all([
        hankel_factorization_ok,
        cauchy_displacement_ok,
        lagrange_cauchy_ok,
        determinant_base_ok,
        determinant_lemma_ok,
    ])
    return {
        "case": case.name,
        "field": field.name,
        "field_order": field.order,
        "subgroup_order": case.subgroup_order,
        "alpha": field.encode(alpha),
        "m": case.m,
        "r": case.r,
        "nonvanishing_hypotheses": {
            "alpha_exact_order": element_order(alpha, field) == case.subgroup_order,
            "m_plus_r_at_most_subgroup_order": case.m + case.r <= case.subgroup_order,
            "distinct_x_points": len({str(x) for x in x_points}) == case.m,
            "cauchy_denominators_nonzero": True,
            "det_VX_nonzero": not field.is_zero(det(vx, field)),
        },
        "checks": {
            "rectangular_hankel_vtdv_factorization": hankel_factorization_ok,
            "toeplitz_cauchy_rank_one_displacement": cauchy_displacement_ok,
            "lagrange_matrix_cauchy_factorization": lagrange_cauchy_ok,
            "base_hankel_determinant_formula": determinant_base_ok,
            "matrix_determinant_lemma_kernel_reduction": determinant_lemma_ok,
        },
        "shift_checks": shift_payloads,
        "status": "PASS" if ok else "FAIL",
    }


def build_cases() -> list[Case]:
    return [
        Case("F13_mu4", PrimeField(13), 4, 3, 1, (0, 1, 2)),
        Case("F17_mu16", PrimeField(17), 16, 7, 4, (0, 1, 3)),
        Case("F49_mu16", QuadraticField(7, 3), 16, 6, 3, (0, 2, 5)),
    ]


def build_artifact() -> dict[str, object]:
    cases = [check_case(case) for case in build_cases()]
    ok = all(case["status"] == "PASS" for case in cases)
    return {
        "schema_version": "m1-displacement-uniform-v1",
        "dag_target": "displacement_uniform",
        "status": "PROVED / ALGEBRA + FINITE REPLAY" if ok else "FAILED",
        "classification": (
            "SUBGROUP_HANKEL_DISPLACEMENT_IDENTITIES_VERIFIED"
            if ok
            else "SUBGROUP_HANKEL_DISPLACEMENT_CHECK_FAILED"
        ),
        "theorem_scope": [
            "Hankel moment matrices factor as V^T D V over any field",
            "square subgroup-Hankel blocks have determinant det(V_X)^2 prod_X x^h",
            "low-rank support additions reduce by the matrix determinant lemma",
            "contiguous subgroup Lagrange matrices factor through Toeplitz-Cauchy kernels",
            "the Toeplitz-Cauchy kernel has rank-one displacement C-U C V = 1",
        ],
        "cases": cases,
        "nonclaims": [
            "does not prove spectral disjointness",
            "does not prove the XR inverse theorem",
            "does not close Front alpha or Front beta",
            "does not assert any M1 safe-side threshold",
        ],
    }


def write_artifact() -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(build_artifact(), indent=2, sort_keys=True) + "\n")


def check_artifact_replay() -> tuple[bool, list[str]]:
    if not ARTIFACT.exists():
        return False, ["artifact missing; rerun with --emit"]
    actual = json.loads(ARTIFACT.read_text())
    expected = build_artifact()
    return actual == expected, [
        f"artifact path: {ARTIFACT.relative_to(REPO)}",
        f"classification: {actual.get('classification')}",
        f"cases: {', '.join(case['case'] for case in actual.get('cases', []))}",
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON certificate")
    args = parser.parse_args()
    if args.emit:
        write_artifact()

    artifact = build_artifact()
    replay_ok, replay_details = check_artifact_replay()
    if args.emit:
        replay_ok, replay_details = check_artifact_replay()
    ok = artifact["classification"] == "SUBGROUP_HANKEL_DISPLACEMENT_IDENTITIES_VERIFIED" and replay_ok

    print("=" * 78)
    print("M1 displacement-uniform identities")
    print("=" * 78)
    for case in artifact["cases"]:
        checks = case["checks"]
        print(f"[{case['status']:4}] {case['case']} over {case['field']} with mu_{case['subgroup_order']}")
        print(f"       alpha={case['alpha']}  m={case['m']}  r={case['r']}")
        print(f"       checks={sum(bool(v) for v in checks.values())}/{len(checks)}")
        print(f"       shifts={len(case['shift_checks'])}")
    print(f"[{'PASS' if replay_ok else 'FAIL'}] artifact replay")
    for line in replay_details:
        print(f"       {line}")
    print("-" * 78)
    print(f"classification: {artifact['classification']}")
    print("-" * 78)
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
