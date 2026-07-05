#!/usr/bin/env python3
"""Independent checker for the growing-dimensional d=3 census packet.

Status: AUDIT. The checker rebuilds domain locators, recomputes stabilizers,
checks gcd-triviality through polynomial gcd plus domain roots, and recounts
each recorded max witness from raw support enumeration.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "rem:v13-conjf-open; prob:band; thm:v13-dim2"
SCHEMA_VERSION = "growing-dim-conjf-d3-v2"
DEFAULT_CERT = Path(
    "experimental/data/certificates/growing-dim-conjf-d3/"
    "growing_dim_conjf_d3.json"
)


def primitive_root(p: int) -> int:
    factors: list[int] = []
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root for F_{p}")


def subgroup(p: int, n: int) -> tuple[int, ...]:
    omega = pow(primitive_root(p), (p - 1) // n, p)
    values = tuple(pow(omega, i, p) for i in range(n))
    assert len(set(values)) == n
    return values


def trim(poly: tuple[int, ...]) -> tuple[int, ...]:
    out = [x % CURRENT_P for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return tuple(out)


CURRENT_P = 97


def poly_eval(poly: tuple[int, ...], x: int, p: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % p
    return acc


def poly_divmod(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    a_work = [x % p for x in a]
    b_work = [x % p for x in b]
    while len(a_work) > 1 and a_work[-1] == 0:
        a_work.pop()
    while len(b_work) > 1 and b_work[-1] == 0:
        b_work.pop()
    if b_work == [0]:
        raise ZeroDivisionError
    q = [0] * max(1, (len(a_work) - len(b_work) + 1))
    inv = pow(b_work[-1], -1, p)
    while len(a_work) >= len(b_work) and a_work != [0]:
        coeff = a_work[-1] * inv % p
        shift = len(a_work) - len(b_work)
        q[shift] = coeff
        for i, value in enumerate(b_work):
            a_work[shift + i] = (a_work[shift + i] - coeff * value) % p
        while len(a_work) > 1 and a_work[-1] == 0:
            a_work.pop()
    return tuple(q), tuple(a_work)


def poly_gcd(a: tuple[int, ...], b: tuple[int, ...], p: int) -> tuple[int, ...]:
    aa = tuple(x % p for x in a)
    bb = tuple(x % p for x in b)
    while bb != (0,):
        _q, rem = poly_divmod(aa, bb, p)
        aa, bb = bb, rem
    inv = pow(aa[-1], -1, p)
    return tuple((inv * x) % p for x in aa)


def space_gcd(basis: list[tuple[int, ...]], p: int) -> tuple[int, ...]:
    g = basis[0]
    for poly in basis[1:]:
        g = poly_gcd(g, poly, p)
    return g


def matrix_rank(rows: list[list[int]], p: int) -> int:
    if not rows:
        return 0
    work = [[x % p for x in row] for row in rows]
    rank = 0
    width = len(work[0])
    for col in range(width):
        pivot = None
        for row in range(rank, len(work)):
            if work[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inv = pow(work[rank][col], -1, p)
        work[rank] = [(inv * value) % p for value in work[rank]]
        for row in range(len(work)):
            if row != rank and work[row][col]:
                factor = work[row][col]
                work[row] = [
                    (work[row][i] - factor * work[rank][i]) % p
                    for i in range(width)
                ]
        rank += 1
    return rank


def canonical_basis(basis: list[tuple[int, ...]], width: int, p: int) -> list[tuple[int, ...]]:
    rows = [[poly[i] % p if i < len(poly) else 0 for i in range(width)] for poly in basis]
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, len(rows)):
            if rows[row][col]:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, p)
        rows[rank] = [(inv * x) % p for x in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][col]:
                factor = rows[row][col]
                rows[row] = [(rows[row][i] - factor * rows[rank][i]) % p for i in range(width)]
        rank += 1
        if rank == len(rows):
            break
    return [tuple(row) for row in rows[:rank]]


def canonical_vector(vector: tuple[int, ...], p: int) -> tuple[int, ...]:
    for value in vector:
        if value % p:
            inv = pow(value, -1, p)
            return tuple((inv * item) % p for item in vector)
    raise ValueError("zero vector has no projective representative")


def evaluation_normal(point: int, width: int, p: int) -> tuple[int, ...]:
    return canonical_vector(tuple(pow(point, degree, p) for degree in range(width)), p)


def normal_is_evaluation(normal: tuple[int, ...], domain: tuple[int, ...], p: int) -> bool:
    width = len(normal)
    return any(normal == evaluation_normal(point, width, p) for point in domain)


def hyperplane_basis_from_normal(normal: tuple[int, ...], p: int) -> list[tuple[int, ...]]:
    width = len(normal)
    pivot = next(index for index, value in enumerate(normal) if value % p)
    inv = pow(normal[pivot], -1, p)
    basis: list[tuple[int, ...]] = []
    for free_col in range(width):
        if free_col == pivot:
            continue
        row = [0] * width
        row[free_col] = 1
        row[pivot] = (-normal[free_col] * inv) % p
        basis.append(tuple(row))
    return canonical_basis(basis, width, p)


def in_span(poly: tuple[int, ...], basis: list[tuple[int, ...]], width: int, p: int) -> bool:
    rows = [[item[i] if i < len(item) else 0 for i in range(width)] for item in basis]
    rank = matrix_rank(rows, p)
    rows.append([poly[i] if i < len(poly) else 0 for i in range(width)])
    return matrix_rank(rows, p) == rank


def locator(domain: tuple[int, ...], support: tuple[int, ...], p: int) -> tuple[int, ...]:
    coeffs = [1]
    for index in support:
        root = domain[index]
        nxt = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            nxt[i] = (nxt[i] - coeff * root) % p
            nxt[i + 1] = (nxt[i + 1] + coeff) % p
        coeffs = nxt
    return tuple(coeffs)


def stabilizer_size(support: tuple[int, ...], n: int) -> int:
    S = set(support)
    return sum(1 for shift in range(n) if {(x + shift) % n for x in S} == S)


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def recount_witness(row: dict[str, Any], witness: dict[str, Any]) -> tuple[int, int]:
    p = row["p"]
    n = row["n"]
    j = row["j"]
    width = j + 1
    domain = subgroup(p, n)
    assert list(domain) == row["domain"]
    basis = [tuple(item) for item in witness["basis"]]
    assert matrix_rank([[poly[i] if i < len(poly) else 0 for i in range(width)] for poly in basis], p) == len(basis)
    if "normal" in witness:
        normal = canonical_vector(tuple(witness["normal"]), p)
        assert not normal_is_evaluation(normal, domain, p)
        assert hyperplane_basis_from_normal(normal, p) == basis
    gcd_poly = space_gcd(basis, p)
    assert all(poly_eval(gcd_poly, point, p) != 0 for point in domain)
    aperiodic = 0
    periodic = 0
    shown_aperiodic = {tuple(item["support"]) for item in witness["aperiodic_hits"]}
    shown_periodic = {tuple(item["support"]) for item in witness["periodic_hits"]}
    for support in itertools.combinations(range(n), j):
        poly = locator(domain, support, p)
        if not in_span(poly, basis, width, p):
            continue
        scale = stabilizer_size(support, n)
        if scale == 1:
            aperiodic += 1
            if support in shown_aperiodic:
                shown_aperiodic.remove(support)
        else:
            periodic += 1
            if support in shown_periodic:
                shown_periodic.remove(support)
    assert not shown_aperiodic
    assert not shown_periodic
    return aperiodic, periodic


def check_evaluation_hyperplane_calibration(row: dict[str, Any]) -> None:
    p = row["p"]
    n = row["n"]
    j = row["j"]
    width = j + 1
    domain = subgroup(p, n)
    calibration = row["evaluation_hyperplane_calibration"]
    assert calibration["total_through_point"] == comb(n - 1, j - 1)
    assert calibration["periodic_through_point"] == 7
    assert calibration["aperiodic_through_point"] == comb(n - 1, j - 1) - 7
    assert calibration["aperiodic_through_point"] == 448
    assert calibration["dim3_envelope_binom_n_3"] == comb(n, 3)
    stored_by_index = {
        item["point_index"]: item for item in calibration["point_rows"]
    }
    assert len(stored_by_index) == n
    for point_index, point in enumerate(domain):
        normal = evaluation_normal(point, width, p)
        by_containment = {"total": 0, "aperiodic": 0, "periodic": 0}
        by_normal = {"total": 0, "aperiodic": 0, "periodic": 0}
        for support in itertools.combinations(range(n), j):
            poly = locator(domain, support, p)
            scale = stabilizer_size(support, n)
            if point_index in support:
                by_containment["total"] += 1
                by_containment["aperiodic" if scale == 1 else "periodic"] += 1
            if sum(normal[i] * poly[i] for i in range(width)) % p == 0:
                by_normal["total"] += 1
                by_normal["aperiodic" if scale == 1 else "periodic"] += 1
        assert by_containment == by_normal
        assert by_containment["total"] == comb(n - 1, j - 1)
        assert by_containment["periodic"] == 7
        assert by_containment["aperiodic"] == 448
        stored = stored_by_index[point_index]
        assert stored["point"] == point
        assert tuple(stored["normal"]) == normal
        assert stored["total_through_point"] == by_containment["total"]
        assert stored["aperiodic_through_point"] == by_containment["aperiodic"]
        assert stored["periodic_through_point"] == by_containment["periodic"]


def check_row(row: dict[str, Any]) -> None:
    n = row["n"]
    j = row["j"]
    total = comb(n, j)
    assert row["total_Dloc_j"] == total
    ap = 0
    per = 0
    for support in itertools.combinations(range(n), j):
        if stabilizer_size(support, n) == 1:
            ap += 1
        else:
            per += 1
    assert row["aperiodic_Dloc_j"] == ap
    assert row["periodic_Dloc_j"] == per
    check_evaluation_hyperplane_calibration(row)
    for dim_text, dim_row in row["dimension_rows"].items():
        max_count = dim_row["max_aperiodic_incidence"]
        for witness in dim_row["max_witnesses"]:
            aperiodic, periodic = recount_witness(row, witness)
            assert aperiodic == max_count
            assert periodic == witness["periodic_hit_count"]
        if dim_text == "2":
            assert dim_row["dim2_comparison_binom_j_2"] == comb(j, 2)
            assert dim_row["exceeds_dim2_comparison"] == (max_count > comb(j, 2))
        if dim_text == "3":
            assert dim_row["dim3_envelope_binom_n_3"] == comb(n, 3)
            assert dim_row["exceeds_dim3_envelope"] == (max_count > comb(n, 3))
            directed = dim_row["directed_search"]
            assert directed["samples_requested"] >= 60_000
            assert directed["over_envelope_count"] == 0
            directed_witness = directed["max_witness"]
            directed_aperiodic, directed_periodic = recount_witness(row, directed_witness)
            assert directed_aperiodic == directed["max_aperiodic_incidence"]
            assert directed_periodic == directed["max_periodic_hits_in_candidate"]
            assert directed_aperiodic <= comb(n, 3)
            assert max_count >= directed_aperiodic


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, default=DEFAULT_CERT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = json.loads(args.check.read_text())
    assert cert["schema_version"] == SCHEMA_VERSION
    assert cert["theorem_problem_id"] == THEOREM_PROBLEM_ID
    assert cert["payload_sha256"] == payload_hash(cert)
    for row in cert["rows"]:
        check_row(row)
    result = {
        "status": STATUS,
        "result": "PASS",
        "certificate": args.check.as_posix(),
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "rows_checked": len(cert["rows"]),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "growing_dim_conjf_d3_check: "
            f"status={STATUS} result=PASS file={args.check.as_posix()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
