#!/usr/bin/env python3
"""Verify the M4 affine-pivot low-direction-rank compression theorem."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-m4-affine-pivot-compression-v1"
Q_LINE = 17**32
TARGET_BITS = 128
BUDGET = Q_LINE // 2**TARGET_BITS
A_MIN = 385
A_MAX = 426
RANK_BOUNDARY = 6
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
PROJECTIVE_BUDGET_SPLIT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/"
    "f17_32_n512_k256_m3_m4_projective_budget_split.json"
)
AMBIENT_SHARPNESS_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-rank6-ambient-sharpness/"
    "f17_32_n512_k256_m3_m4_rank6_ambient_sharpness.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def mat_mul(left: list[list[int]], right: list[list[int]], prime: int) -> list[list[int]]:
    rows = len(left)
    inner = len(right)
    cols = len(right[0])
    require(all(len(row) == inner for row in left), "left matrix shape mismatch")
    require(all(len(row) == cols for row in right), "right matrix shape mismatch")
    out = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(inner):
            if left[i][k] == 0:
                continue
            for j in range(cols):
                out[i][j] = (out[i][j] + left[i][k] * right[k][j]) % prime
    return out


def mat_add(left: list[list[int]], right: list[list[int]], prime: int) -> list[list[int]]:
    require(len(left) == len(right), "matrix row mismatch")
    require(len(left[0]) == len(right[0]), "matrix column mismatch")
    return [
        [(left[i][j] + right[i][j]) % prime for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def mat_scale(matrix: list[list[int]], scalar: int, prime: int) -> list[list[int]]:
    return [[scalar * entry % prime for entry in row] for row in matrix]


def eye(size: int) -> list[list[int]]:
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]


def det_mod(matrix: list[list[int]], prime: int) -> int:
    size = len(matrix)
    work = [[entry % prime for entry in row] for row in matrix]
    determinant = 1
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
            determinant = (-determinant) % prime
        pivot_value = work[col][col] % prime
        determinant = determinant * pivot_value % prime
        inv_pivot = pow(pivot_value, -1, prime)
        for row in range(col + 1, size):
            factor = work[row][col] * inv_pivot % prime
            if factor == 0:
                continue
            for j in range(col, size):
                work[row][j] = (work[row][j] - factor * work[col][j]) % prime
    return determinant % prime


def inv_mod(matrix: list[list[int]], prime: int) -> list[list[int]]:
    size = len(matrix)
    work = [[entry % prime for entry in row] + eye(size)[i] for i, row in enumerate(matrix)]
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if work[row][col] % prime:
                pivot = row
                break
        require(pivot is not None, "matrix is singular")
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
        inv_pivot = pow(work[col][col] % prime, -1, prime)
        for j in range(2 * size):
            work[col][j] = work[col][j] * inv_pivot % prime
        for row in range(size):
            if row == col:
                continue
            factor = work[row][col] % prime
            if factor == 0:
                continue
            for j in range(2 * size):
                work[row][j] = (work[row][j] - factor * work[col][j]) % prime
    return [row[size:] for row in work]


def sanity_checks() -> list[dict[str, Any]]:
    checks = []
    prime = 17
    for size, rank, z0 in [(4, 2, 3), (7, 6, 5), (8, 3, 0)]:
        m0 = [[(1 if i == j else 0) + (i + 2 * j + z0) % prime for j in range(size)] for i in range(size)]
        while det_mod(m0, prime) == 0:
            m0[0][0] = (m0[0][0] + 1) % prime
        p_mat = [[(i + 1) * (a + 2) % prime for a in range(rank)] for i in range(size)]
        q_mat = [[(a + 3) * (j + 1) % prime for j in range(size)] for a in range(rank)]
        direction = mat_mul(p_mat, q_mat, prime)
        inv_m0 = inv_mod(m0, prime)
        compressed = mat_mul(mat_mul(q_mat, inv_m0, prime), p_mat, prime)
        for w in [0, 1, 2, 6, 11]:
            lhs = det_mod(mat_add(m0, mat_scale(direction, w, prime), prime), prime)
            rhs = det_mod(m0, prime) * det_mod(
                mat_add(eye(rank), mat_scale(compressed, w, prime), prime),
                prime,
            ) % prime
            require(lhs == rhs, "matrix determinant lemma sanity check failed")
        checks.append(
            {
                "prime": prime,
                "matrix_size": size,
                "rank": rank,
                "base_slope": z0,
                "tested_offsets": [0, 1, 2, 6, 11],
                "result": "passed",
            }
        )
    return checks


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    minor_size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": minor_size,
        "maximal_row_set_count": comb(t_value, minor_size),
        "rank6_compressed_size": RANK_BOUNDARY,
        "compression_ratio_note": f"{minor_size}x{minor_size} determinant -> {RANK_BOUNDARY}x{RANK_BOUNDARY} determinant",
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    budget_split = load_json(PROJECTIVE_BUDGET_SPLIT_REF)
    ambient_sharpness = load_json(AMBIENT_SHARPNESS_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(
        budget_split["schema_version"] == "f17-32-m3-m4-projective-budget-split-v1",
        "unexpected projective-budget schema",
    )
    require(
        ambient_sharpness["schema_version"] == "f17-32-m3-m4-rank6-ambient-sharpness-v1",
        "unexpected ambient sharpness schema",
    )
    for name, data in [("budget", budget_split), ("ambient", ambient_sharpness)]:
        require(data["window"]["A_min"] == A_MIN, f"{name} A_min mismatch")
        require(data["window"]["A_max"] == A_MAX, f"{name} A_max mismatch")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )
    require(BUDGET == 6, "unexpected finite budget")

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(total_row_sets == budget_split["window"]["all_row_set_total"], "budget total mismatch")
    require(total_row_sets == ambient_sharpness["window"]["all_row_set_total"], "ambient total mismatch")
    require(all(record["minor_size"] > RANK_BOUNDARY for record in records), "minor size too small")

    sanity = sanity_checks()

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "affine-pivot compression for low-direction-rank M3 regular buckets",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_budget": BUDGET,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "projective_budget_split": {
                "ref": PROJECTIVE_BUDGET_SPLIT_REF,
                "sha256": sha256_file(PROJECTIVE_BUDGET_SPLIT_REF),
            },
            "rank6_ambient_sharpness": {
                "ref": AMBIENT_SHARPNESS_REF,
                "sha256": sha256_file(AMBIENT_SHARPNESS_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "theorem": {
            "statement": (
                "Fix an exact agreement A, a maximal row set R, and a finite "
                "base slope z0 for which M_R(z0)=H_R(u)+z0 H_R(v) is "
                "invertible.  If H_R(v)=P_R Q_R has rank at most r, then "
                "for w=z-z0 the determinant satisfies "
                "det(M_R(z))=det(M_R(z0))*det(I_r+w Q_R M_R(z0)^{-1} P_R)."
            ),
            "rank6_consequence": (
                "For the endpoint-sensitive rank-6 boundary, every affine "
                "pivot chart reduces the original 87..128 dimensional "
                "maximal-minor determinant to a 6x6 determinant."
            ),
            "proof_skeleton": [
                "Write M_R(z0+w)=M_R(z0)+w P_R Q_R.",
                "Factor out M_R(z0) on the left.",
                "Apply Sylvester's determinant identity det(I_m+w M^{-1}P Q)=det(I_r+w Q M^{-1}P).",
                "The compressed determinant has degree at most r and has exactly the same finite roots inside the affine pivot chart.",
            ],
            "rank6_boundary_use": [
                "The ambient sharpness packet shows rank 6 cannot be closed by rank and endpoint counting alone.",
                "This compression theorem identifies the next Hankel-specific finite-root object: the gcd of 6x6 affine-pivot compressed determinants across row-set charts.",
                "A rank-6 closure can now target endpoint payment/emptiness or prove that the compressed common root table has at most five surviving roots.",
            ],
        },
        "field_audit": {
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "sanity_checks": sanity,
        "summary": {
            "agreement_count": len(records),
            "rank6_compressed_size": RANK_BOUNDARY,
            "minor_size_min": min(record["minor_size"] for record in records),
            "minor_size_max": max(record["minor_size"] for record in records),
            "finite_budget": BUDGET,
            "sanity_check_count": len(sanity),
        },
        "checks": [
            "dependency windows are 385..426",
            "dependency row-set totals agree",
            "all M3 minor sizes are larger than the rank-6 boundary",
            "determinant identity sanity checks pass over F_17",
            "the theorem is chart-local and requires an invertible finite base slope",
        ],
        "nonclaims": [
            "does not compute rank-6 root tables",
            "does not prove rank-6 projective safety",
            "does not assert that every row set has an invertible z0 in a chosen finite subatlas",
            "does not duplicate synthetic low-rank Cauchy packets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"affine-pivot compression certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    window = certificate["window"]
    print("F_17^32 M3/M4 affine-pivot compression")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print(
        "minor sizes {minor_size_min}..{minor_size_max}; rank-6 charts compress to {rank6_compressed_size}x{rank6_compressed_size}".format(
            **summary
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
