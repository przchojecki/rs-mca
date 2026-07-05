#!/usr/bin/env python3
"""Verify offline affine-shear eca/emca staircase packets.

The packet records full offline enumeration over finite-slope-preserving
affine-shear representatives.  This checker is deliberately stdlib-only: it
checks packet integrity, staircase invariants, and every recorded argmax slope
list using exact restricted-code membership tests over F_q.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
CERT_PATH = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "exact-worstcase-eca-emca-staircase"
    / "exact_worstcase_eca_emca_staircase_m4_q19_q23_gpu_rows.json"
)
SCHEMA_VERSION = "exact-worstcase-eca-emca-affine-quotient-gpu-v1"
THEOREM_PROBLEM_ID = "towards-prize thm:sparsify; finite m=4 affine-shear eca/emca staircase"
REQUIRED_ROWS = {(19, 18, 14), (23, 22, 18)}
REQUIRED_RADII = (0, 1, 2, 3)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def render(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rref_modp(matrix: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []
    row_count = len(rows)
    col_count = len(rows[0])
    pivots: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if rows[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inv = pow(rows[pivot_row][col] % p, p - 2, p)
        rows[pivot_row] = [(value * inv) % p for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or rows[row][col] % p == 0:
                continue
            factor = rows[row][col] % p
            rows[row] = [
                (value - factor * rows[pivot_row][idx]) % p
                for idx, value in enumerate(rows[row])
            ]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return rows, pivots


def generator_rows(p: int, domain: tuple[int, ...], k: int) -> list[list[int]]:
    return [[pow(x, degree, p) for x in domain] for degree in range(k)]


def nullspace_check_matrix_for_subset(
    generator: list[list[int]], subset: tuple[int, ...], p: int
) -> list[list[tuple[int, int]]]:
    matrix = [[row[index] % p for index in subset] for row in generator]
    rref, pivots = rref_modp(matrix, p)
    pivot_set = set(pivots)
    free_cols = [col for col in range(len(subset)) if col not in pivot_set]
    basis: list[list[tuple[int, int]]] = []
    for free_col in free_cols:
        vector = [0] * len(subset)
        vector[free_col] = 1
        for row_index, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-rref[row_index][free_col]) % p
        basis.append(
            [
                (subset[col], coefficient % p)
                for col, coefficient in enumerate(vector)
                if coefficient % p
            ]
        )
    return basis


def build_subset_tables(
    p: int, n: int, k: int, r: int, domain: tuple[int, ...]
) -> list[list[list[tuple[int, int]]]]:
    generator = generator_rows(p, domain, k)
    tables: list[list[list[tuple[int, int]]]] = []
    all_indices = tuple(range(n))
    for removed_size in range(r + 1):
        for removed in itertools.combinations(all_indices, removed_size):
            removed_set = set(removed)
            subset = tuple(index for index in all_indices if index not in removed_set)
            tables.append(nullspace_check_matrix_for_subset(generator, subset, p))
    return tables


def in_restricted_code(word: tuple[int, ...], checks: list[list[tuple[int, int]]], p: int) -> bool:
    return all(sum(coeff * word[index] for index, coeff in row) % p == 0 for row in checks)


def add_scaled(f1: tuple[int, ...], gamma: int, f2: tuple[int, ...], p: int) -> tuple[int, ...]:
    return tuple((a + gamma * b) % p for a, b in zip(f1, f2, strict=True))


def mca_bad_slopes(
    f1: tuple[int, ...],
    f2: tuple[int, ...],
    p: int,
    tables: list[list[list[tuple[int, int]]]],
) -> tuple[int, ...]:
    bad: list[int] = []
    for gamma in range(p):
        point = add_scaled(f1, gamma, f2, p)
        for checks in tables:
            if in_restricted_code(point, checks, p) and not in_restricted_code(f2, checks, p):
                bad.append(gamma)
                break
    return tuple(bad)


def pair_far(
    f1: tuple[int, ...],
    f2: tuple[int, ...],
    p: int,
    tables: list[list[list[tuple[int, int]]]],
) -> bool:
    return all(
        not (in_restricted_code(f1, checks, p) and in_restricted_code(f2, checks, p))
        for checks in tables
    )


def ca_bad_slopes(
    f1: tuple[int, ...],
    f2: tuple[int, ...],
    p: int,
    tables: list[list[list[tuple[int, int]]]],
) -> tuple[int, ...]:
    if not pair_far(f1, f2, p, tables):
        return ()
    bad: list[int] = []
    for gamma in range(p):
        point = add_scaled(f1, gamma, f2, p)
        if any(in_restricted_code(point, checks, p) for checks in tables):
            bad.append(gamma)
    return tuple(bad)


def representative_count(q: int, m: int) -> int:
    projective_m = 1 + (q**m - 1) // (q - 1)
    projective_quotient = 1 + (q ** (m - 1) - 1) // (q - 1)
    return projective_m + (projective_m - 1) * projective_quotient


def check_argmax(
    record: dict[str, Any],
    *,
    kind: str,
    q: int,
    n: int,
    tables: list[list[list[tuple[int, int]]]],
    expected_count: int,
) -> None:
    f1 = tuple(int(value) for value in record["eps1"])
    f2 = tuple(int(value) for value in record["eps2"])
    require(len(f1) == n and len(f2) == n, f"{kind} word length mismatch")
    slopes = ca_bad_slopes(f1, f2, q, tables) if kind == "eca" else mca_bad_slopes(f1, f2, q, tables)
    require(list(slopes) == record["bad_slopes"], f"{kind} bad_slopes mismatch")
    require(len(slopes) == expected_count, f"{kind} numerator mismatch")


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "bad schema_version")
    expected_hash = payload.get("payload_sha256")
    without_hash = {key: value for key, value in payload.items() if key != "payload_sha256"}
    require(expected_hash == sha256_text(render(without_hash)), "payload_sha256 mismatch")
    require(payload.get("status") == "AUDIT / EXPERIMENTAL", "bad status")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "bad theorem_problem_id")
    require(payload.get("endpoint_conventions", {}).get("finite_slopes_only") is True, "missing finite-slope convention")

    rows = payload.get("rows", [])
    observed_rows = {(int(row["q"]), int(row["n"]), int(row["k"])) for row in rows}
    require(observed_rows == REQUIRED_ROWS, f"unexpected row set: {sorted(observed_rows)}")

    for row in rows:
        q = int(row["q"])
        n = int(row["n"])
        k = int(row["k"])
        m = n - k
        require((q, n, k) in REQUIRED_ROWS, "unexpected q,n,k row")
        require(row.get("m") == m, "bad m=n-k")
        require(m == 4, "this packet is restricted to m=4 rows")
        require(row.get("offline_provenance") is True, "missing offline provenance flag")
        require(row.get("affine_shear_orbit_reduction_exact") is True, "missing affine-shear exact flag")
        require(row.get("representative_mode") == "affine-shear", "bad representative mode")
        require(row.get("representatives_total") == representative_count(q, m), "bad representative count")
        require(row.get("raw_pair_classes_total") == q ** (2 * m), "bad raw pair count")
        domain = tuple(int(value) for value in row["domain"])
        require(domain == tuple(range(n)), "unexpected affine domain")
        radii = row.get("radii", [])
        require(tuple(int(radius["r"]) for radius in radii) == REQUIRED_RADII, "unexpected radius set")
        previous_emca = -1
        for radius in radii:
            r = int(radius["r"])
            require(radius["agreement"] == n - r, "bad agreement")
            require(radius["delta"] == f"{r}/{n}", "bad delta")
            recomputed_sparsify_rhs = max(int(radius["eca_num"]), int(radius["sigma_num"]))
            require(radius["sparsify_rhs"] == recomputed_sparsify_rhs, "recorded sparsify_rhs mismatch")
            require(radius["emca_num"] == recomputed_sparsify_rhs, "recomputed sparsify mismatch")
            require(radius["emca_num"] == radius["sparsify_rhs"], "sparsify mismatch")
            require(radius["sparsify_holds"] is True, "sparsify flag mismatch")
            require(radius["eca_num"] <= radius["emca_num"], "eca exceeds emca")
            require(radius["sigma_num"] <= radius["emca_num"], "sigma exceeds emca")
            require(radius["emca_num"] >= previous_emca, "emca is not monotone")
            require(radius["emca_num"] <= q, "finite-slope numerator exceeds q")
            tables = build_subset_tables(q, n, k, r, domain)
            check_argmax(
                radius["argmax_eca"],
                kind="eca",
                q=q,
                n=n,
                tables=tables,
                expected_count=int(radius["eca_num"]),
            )
            check_argmax(
                radius["argmax_emca"],
                kind="emca",
                q=q,
                n=n,
                tables=tables,
                expected_count=int(radius["emca_num"]),
            )
            check_argmax(
                radius["argmax_sigma"],
                kind="sigma",
                q=q,
                n=n,
                tables=tables,
                expected_count=int(radius["sigma_num"]),
            )
            previous_emca = int(radius["emca_num"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, default=CERT_PATH)
    args = parser.parse_args()
    payload = json.loads(args.check.read_text(encoding="utf-8"))
    check_payload(payload)
    print("exact affine-shear eca/emca packet verifier")
    print("  object: finite-slope CA/MCA staircase numerators")
    print(f"  theorem_problem_id: {THEOREM_PROBLEM_ID}")
    print("  status: AUDIT; offline rows checked by exact argmax replay")
    for row in payload["rows"]:
        nums = ", ".join(f"r={radius['r']}:emca={radius['emca_num']}" for radius in row["radii"])
        print(f"  row F_{row['q']} n={row['n']} k={row['k']}: {nums}")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
