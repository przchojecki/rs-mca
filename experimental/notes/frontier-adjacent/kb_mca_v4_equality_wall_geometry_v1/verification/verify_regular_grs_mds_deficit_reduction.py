#!/usr/bin/env python3
"""Verify the exact arithmetic and a finite-field model of the GRS reduction."""

from __future__ import annotations
class VerificationError(RuntimeError):
    """Raised when an exact verifier condition fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(str(message))


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )



import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "regular_grs_mds_deficit_certificate.json"

J = 981_105
C = 67_472
A = 12
H_MIN = 118_077
R_VALUES = range(65, 70)


def inv(x: int, p: int) -> int:
    return pow(x % p, p - 2, p)


def rank_mod(matrix: list[list[int]], p: int) -> int:
    a = [[x % p for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((r for r in range(rank, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = inv(a[rank][col], p)
        a[rank] = [(scale * x) % p for x in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][col]:
                continue
            factor = a[r][col]
            a[r] = [
                (a[r][j] - factor * a[rank][j]) % p
                for j in range(cols)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def poly_eval(a: list[int], x: int, p: int) -> int:
    out = 0
    for coeff in reversed(a):
        out = (out * x + coeff) % p
    return out


def finite_grs_regression() -> dict[str, int | bool]:
    p = 101
    a = 5
    r = 9
    roots = list(range(1, a + 1))
    points = list(range(20, 20 + r))

    lam = [1]
    for alpha in roots:
        lam = poly_mul(lam, [(-alpha) % p, 1], p)

    ell = []
    for omitted in roots:
        value = [1]
        for alpha in roots:
            if alpha != omitted:
                value = poly_mul(value, [(-alpha) % p, 1], p)
        ell.append(value)

    weights = [inv(poly_eval(lam, t, p), p) for t in points]
    evaluation = [
        [
            weights[i] * poly_eval(ell[j], points[i], p) % p
            for i in range(r)
        ]
        for j in range(a)
    ]

    # A full-column-rank coefficient matrix for the Q_j.
    q_matrix = [
        [pow(j + 2, degree, p) for j in range(a)]
        for degree in range(a + 3)
    ]
    locator_rows = [
        [
            sum(q_matrix[row][j] * evaluation[j][i] for j in range(a)) % p
            for i in range(r)
        ]
        for row in range(len(q_matrix))
    ]

    grs_rows = [
        [weights[i] * pow(points[i], degree, p) % p for i in range(r)]
        for degree in range(a)
    ]
    t_grs_rows = grs_rows + [
        [points[i] * value % p for i, value in enumerate(row)]
        for row in grs_rows
    ]

    locator_rank = rank_mod(locator_rows, p)
    grs_rank = rank_mod(grs_rows, p)
    combined_rank = rank_mod(locator_rows + grs_rows, p)
    expanded_rank = rank_mod(t_grs_rows, p)

    return {
        "field": p,
        "a": a,
        "R": r,
        "locator_rank": locator_rank,
        "grs_rank": grs_rank,
        "combined_rank": combined_rank,
        "expanded_rank": expanded_rank,
        "pass": (
            locator_rank == a
            and grs_rank == a
            and combined_rank == a
            and expanded_rank == a + 1
        ),
    }


def a12_ledger() -> list[dict[str, int]]:
    rows = []
    for r in R_VALUES:
        h_max = min(132_382, (11 * J) // (r - 11) - C)
        d_min = C + H_MIN
        d_max = C + h_max
        deficit_min = 11 * J - (r - 11) * d_min
        deficit_max = 11 * J - (r - 11) * d_max
        n_min = J + d_min
        n_max = J + d_max
        forced_min = n_min - deficit_min
        forced_max = n_max - deficit_max
        distinct_vertices = (forced_min + H_MIN - 1) // H_MIN
        residual_budget_max = 12 * h_max - 1_416_923
        rows.append(
            {
                "R": r,
                "h_min": H_MIN,
                "h_max": h_max,
                "deficit_at_h_min": deficit_min,
                "deficit_at_h_max": deficit_max,
                "forced_min_weight_at_h_min": forced_min,
                "forced_min_weight_at_h_max": forced_max,
                "distinct_vertex_floor": distinct_vertices,
                "residual_budget_at_h_max": residual_budget_max,
            }
        )
    return rows


def payload() -> dict[str, object]:
    result = {
        "status": "PROVED_REDUCTION_OPEN_FINAL_CAP",
        "constants": {"J": J, "c": C, "a": A, "h_min": H_MIN},
        "finite_grs_regression": finite_grs_regression(),
        "a12_ledger": a12_ledger(),
        "claims": {
            "regular_code": "weighted GRS_a",
            "regular_dimension": "a",
            "one_step_expansion_dimension": "a+1",
            "mds_deficit": "(a-1)J-(R-a+1)(c+h)",
            "cap_68": "OPEN",
        },
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def check_payload(data: dict[str, object]) -> None:
    require(
        data['finite_grs_regression']['pass'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:189',
    )
    rows = data["a12_ledger"]
    expected_h_max = [132_382, 128_749, 125_245, 121_864, 118_599]
    expected_forced = [394_145, 579_694, 765_243, 950_792, 1_136_341]
    expected_vertices = [4, 5, 7, 9, 10]
    expected_budgets = [171_661, 128_065, 86_017, 45_445, 6_265]
    require(
        [row['h_max'] for row in rows] == expected_h_max,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:195',
    )
    require(
        [row['forced_min_weight_at_h_min'] for row in rows] == expected_forced,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:196',
    )
    require(
        [row['distinct_vertex_floor'] for row in rows] == expected_vertices,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:197',
    )
    require(
        [row['residual_budget_at_h_max'] for row in rows] == expected_budgets,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:198',
    )
    require(
        12 * H_MIN - 1416923 == 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:199',
    )
    require(
        all((row['deficit_at_h_min'] >= 0 for row in rows)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:200',
    )
    require(
        all((row['deficit_at_h_max'] >= 0 for row in rows)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_regular_grs_mds_deficit_reduction.py:201',
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    data = payload()
    check_payload(data)

    if args.emit:
        CERTIFICATE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")

    if args.check:
        disk = json.loads(CERTIFICATE.read_text())
        require(disk == data, 'certificate mismatch')

    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["a12_ledger"][0]["h_max"] += 1
        try:
            check_payload(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("regular weighted-GRS regression: PASS")
    print("a=12 exact MDS-deficit ledger: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
