#!/usr/bin/env python3
"""Verify the subgroup Hankel VTDV packet certificate."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


CERT_PATH = Path("experimental/data/certificates/vtdv/vtdv.json")


class Field(Protocol):
    zero: Any
    one: Any

    def add(self, x: Any, y: Any) -> Any: ...
    def mul(self, x: Any, y: Any) -> Any: ...
    def pow(self, x: Any, n: int) -> Any: ...
    def eq(self, x: Any, y: Any) -> bool: ...
    def encode(self, x: Any) -> Any: ...


@dataclass(frozen=True)
class PrimeField:
    p: int

    @property
    def zero(self) -> int:
        return 0

    @property
    def one(self) -> int:
        return 1

    def add(self, x: int, y: int) -> int:
        return (x + y) % self.p

    def mul(self, x: int, y: int) -> int:
        return (x * y) % self.p

    def pow(self, x: int, n: int) -> int:
        return pow(x % self.p, n, self.p)

    def eq(self, x: int, y: int) -> bool:
        return (x - y) % self.p == 0

    def encode(self, x: int) -> int:
        return x % self.p


@dataclass(frozen=True)
class QuadraticField:
    p: int
    nonsquare: int

    @property
    def zero(self) -> tuple[int, int]:
        return (0, 0)

    @property
    def one(self) -> tuple[int, int]:
        return (1, 0)

    def add(self, x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def mul(self, x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
        a, b = x
        c, d = y
        return ((a * c + b * d * self.nonsquare) % self.p, (a * d + b * c) % self.p)

    def pow(self, x: tuple[int, int], n: int) -> tuple[int, int]:
        out = self.one
        base = x
        exp = n
        while exp:
            if exp & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            exp >>= 1
        return out

    def eq(self, x: tuple[int, int], y: tuple[int, int]) -> bool:
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p) == (0, 0)

    def encode(self, x: tuple[int, int]) -> list[int]:
        return [x[0] % self.p, x[1] % self.p]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def weighted_moment(field: Field, points: list[Any], weights: list[Any], word: list[Any], m: int) -> Any:
    acc = field.zero
    for x, lam, ux in zip(points, weights, word):
        acc = field.add(acc, field.mul(field.mul(lam, ux), field.pow(x, m)))
    return acc


def hankel_from_moments(field: Field, points: list[Any], weights: list[Any], word: list[Any], t: int, j: int) -> list[list[Any]]:
    return [[weighted_moment(field, points, weights, word, i + c) for c in range(j + 1)] for i in range(t)]


def hankel_vtdv(field: Field, points: list[Any], weights: list[Any], word: list[Any], t: int, j: int) -> list[list[Any]]:
    rows: list[list[Any]] = []
    for i in range(t):
        row = []
        for c in range(j + 1):
            acc = field.zero
            for x, lam, ux in zip(points, weights, word):
                acc = field.add(acc, field.mul(field.mul(field.pow(x, i), field.mul(lam, ux)), field.pow(x, c)))
            row.append(acc)
        rows.append(row)
    return rows


def check_identity(field: Field, points: list[Any], weights: list[Any], word: list[Any], t: int, j: int) -> dict[str, Any]:
    direct = hankel_from_moments(field, points, weights, word, t, j)
    factored = hankel_vtdv(field, points, weights, word, t, j)
    for r, (left, right) in enumerate(zip(direct, factored)):
        for c, (a, b) in enumerate(zip(left, right)):
            require(field.eq(a, b), f"VTDV mismatch at {(r, c)}")
    return {
        "point_count": len(points),
        "t": t,
        "j": j,
        "first_row": [field.encode(x) for x in direct[0]],
    }


def build_prime_sample() -> dict[str, Any]:
    field = PrimeField(17)
    points = [1, 2, 4, 8]
    weights = [3, 5, 7, 11]
    word = [6, 10, 15, 9]
    return check_identity(field, points, weights, word, t=3, j=4) | {"field": "F_17"}


def build_quadratic_sample() -> dict[str, Any]:
    field = QuadraticField(3, 2)
    alpha = (0, 1)
    points = [field.one, alpha, field.pow(alpha, 2), field.pow(alpha, 3)]
    weights = [(1, 1), (2, 1), (1, 2), (2, 2)]
    word = [(2, 0), (1, 1), (0, 2), (2, 1)]
    return check_identity(field, points, weights, word, t=3, j=3) | {"field": "F_9"}


def build_certificate() -> dict[str, Any]:
    return {
        "schema": "rs-mca.experimental.vtdv.v1",
        "status": "PROVED",
        "source_dag_node": "vtdv",
        "verdict": "weighted_hankel_moment_matrix_factors_as_V_transpose_Du_V",
        "claim": {
            "moments": "S_m = sum_{x in H} lambda_x u_x x^m",
            "hankel_block": "M_u[i,c] = S_{i+c}",
            "factorization": "M_u = V_t^T D_u V_{j+1}",
            "diagonal": "D_u[x,x] = lambda_x u_x",
            "entry_check": "sum_x x^i lambda_x u_x x^c = S_{i+c}",
        },
        "samples": [build_prime_sample(), build_quadratic_sample()],
        "consumers": ["fm1", "counting_frame", "displacement_uniform", "f1_pencil_nf", "u1_cramer"],
        "non_claims": [
            "does not classify bad slopes",
            "does not count locator fibers",
            "does not prove displacement-uniformity by itself",
            "does not edit Papers A-D",
        ],
    }


def validate_certificate(cert: dict[str, Any]) -> None:
    expected = build_certificate()
    require(cert == expected, "certificate does not match expected packet")
    require(cert["status"] == "PROVED", "packet must remain PROVED")
    require(cert["claim"]["factorization"] == "M_u = V_t^T D_u V_{j+1}", "factorization string changed")
    require([sample["field"] for sample in cert["samples"]] == ["F_17", "F_9"], "prime/extension samples missing")


def emit_certificate(path: Path, cert: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", nargs="?", const=CERT_PATH, type=Path)
    parser.add_argument("--check", nargs="?", const=CERT_PATH, type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit is not None:
        emit_certificate(args.emit, cert)
        print(f"WROTE: {args.emit}")
    if args.check is not None:
        loaded = json.loads(args.check.read_text())
        validate_certificate(loaded)
        print(f"PASS: certificate matches {args.check}")
    if args.emit is None and args.check is None:
        validate_certificate(cert)
        print("PASS: vtdv packet")


if __name__ == "__main__":
    main()
