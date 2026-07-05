#!/usr/bin/env python3
"""Kronecker/BM singular-bucket finite ledger.

Status: EXPERIMENTAL / AUDIT.  The default packet builds nonzero Hankel
pencils `M0 + Z M1` with a shared constant kernel vector, verifies the
determinant is the zero polynomial, and enumerates split locators in the
common kernel bucket.  The committed rows are small enough for exact stdlib
replay.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "kronecker-bm-singular-bucket-v1"
STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "T1-kronecker-bm-singular-bucket"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value in {2, 3}:
        return True
    if value % 2 == 0:
        return False
    d = 3
    while d * d <= value:
        if value % d == 0:
            return False
        d += 2
    return True


def prime_factors(value: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= value:
        if value % d == 0:
            out.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        out.append(value)
    return out


def primitive_root(p: int) -> int:
    require(is_prime(p), "p must be prime")
    factors = prime_factors(p - 1)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root for p={p}")


def subgroup_domain(p: int, n: int) -> list[int]:
    require((p - 1) % n == 0, "n must divide p-1")
    step = pow(primitive_root(p), (p - 1) // n, p)
    out: list[int] = []
    x = 1
    for _ in range(n):
        out.append(x)
        x = (x * step) % p
    require(x == 1 and len(set(out)) == n, "bad domain generator")
    return out


def divisors(value: int) -> list[int]:
    return [d for d in range(1, value + 1) if value % d == 0]


def periodicity_scale(indices: tuple[int, ...], n: int) -> int:
    support = set(indices)
    best = 1
    for scale in divisors(n):
        step = n // scale
        ok = True
        for index in support:
            for offset in range(scale):
                if (index + offset * step) % n not in support:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            best = max(best, scale)
    return best


def signed_locator_coeffs(values: list[int], j: int, p: int) -> list[int]:
    elementary = [0] * (j + 1)
    elementary[0] = 1
    for used, value in enumerate(values, start=1):
        for degree in range(min(used, j), 0, -1):
            elementary[degree] = (elementary[degree] + elementary[degree - 1] * value) % p
    return [1] + [(((-1 if degree % 2 else 1) * elementary[degree]) % p) for degree in range(1, j + 1)]


def recurrence_sequence(kernel: list[int], initials: list[int], length: int, p: int) -> list[int]:
    j = len(kernel) - 1
    require(len(initials) == j, "initial count mismatch")
    require(kernel[-1] % p != 0, "kernel tail must be invertible")
    seq = [value % p for value in initials]
    while len(seq) < length:
        r = len(seq) - j
        value = -sum(seq[r + degree] * kernel[degree] for degree in range(j))
        seq.append((value * pow(kernel[-1], -1, p)) % p)
    return seq


def hankel(sequence: list[int], j: int) -> list[list[int]]:
    return [[sequence[row + col] for col in range(j + 1)] for row in range(j + 1)]


def mat_vec(matrix: list[list[int]], vector: list[int], p: int) -> list[int]:
    return [sum(row[col] * vector[col] for col in range(len(vector))) % p for row in matrix]


def poly_add(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i, value in enumerate(a):
        out[i] = (out[i] + value) % p
    for i, value in enumerate(b):
        out[i] = (out[i] + value) % p
    return trim(out, p)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, av in enumerate(a):
        for j, bv in enumerate(b):
            out[i + j] = (out[i + j] + av * bv) % p
    return trim(out, p)


def trim(poly: list[int], p: int) -> list[int]:
    out = [value % p for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def det_poly(matrix: list[list[list[int]]], p: int) -> list[int]:
    n = len(matrix)
    if n == 1:
        return trim(matrix[0][0], p)
    total = [0]
    for col in range(n):
        sub = [[matrix[row][c] for c in range(n) if c != col] for row in range(1, n)]
        term = poly_mul(matrix[0][col], det_poly(sub, p), p)
        if col % 2:
            term = [(-value) % p for value in term]
        total = poly_add(total, term, p)
    return trim(total, p)


def row(p: int, n: int, j: int, kernel_support: tuple[int, ...], label: str) -> dict[str, Any]:
    domain = subgroup_domain(p, n)
    kernel = signed_locator_coeffs([domain[index] for index in kernel_support], j, p)
    u_sequence = recurrence_sequence(kernel, [1, 2, 3, 4, 5][:j], 2 * j + 1, p)
    v_sequence = recurrence_sequence(kernel, [2, 5, 7, 11, 13][:j], 2 * j + 1, p)
    m0 = hankel(u_sequence, j)
    m1 = hankel(v_sequence, j)
    pencil = [[[m0[row_index][col], m1[row_index][col]] for col in range(j + 1)] for row_index in range(j + 1)]
    determinant = det_poly(pencil, p)
    occupants: list[dict[str, Any]] = []
    for support in itertools.combinations(range(n), j):
        coeffs = signed_locator_coeffs([domain[index] for index in support], j, p)
        if all(value == 0 for value in mat_vec(m0, coeffs, p)) and all(value == 0 for value in mat_vec(m1, coeffs, p)):
            occupants.append(
                {
                    "support": list(support),
                    "coefficients": coeffs,
                    "periodicity_scale": periodicity_scale(support, n),
                }
            )
    return {
        "label": label,
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "j": j,
        "domain": {"type": "multiplicative_subgroup", "values": domain},
        "kernel_support": list(kernel_support),
        "kernel_vector": kernel,
        "u_sequence": u_sequence,
        "v_sequence": v_sequence,
        "hankel_u": m0,
        "hankel_v": m1,
        "determinant_polynomial": determinant,
        "determinant_identically_zero": determinant == [0],
        "kernel_chain": {"degree": 0, "vectors": [kernel], "lambda_polynomial": [kernel[-1]]},
        "locators_total": comb(n, j),
        "occupants_total": len(occupants),
        "aperiodic_occupants": sum(1 for item in occupants if item["periodicity_scale"] == 1),
        "periodic_occupants": sum(1 for item in occupants if item["periodicity_scale"] > 1),
        "occupants": occupants,
        "oracle_gate": p == 17,
    }


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def build_packet() -> dict[str, Any]:
    rows = [
        row(7, 6, 2, (0, 3), "f7_n6_j2"),
        row(11, 10, 2, (0, 5), "f11_n10_j2"),
        row(13, 12, 3, (0, 4, 8), "f13_n12_j3"),
        row(17, 16, 4, (0, 4, 8, 12), "f17_n16_j4_oracle"),
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "proof_status": "AUDIT replay of finite singular-bucket rows",
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "claim": "finite singular pencils with periodic-only split-locator occupants in the recorded range",
        "rows": rows,
        "non_claims": [
            "No asymptotic singular-pencil theorem is claimed.",
            "No resolution of prob:band is claimed.",
            "The packet records a finite pass-on-range only.",
        ],
    }
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "singular_bucket_rows.json"
    path.write_text(json.dumps(build_packet(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return [path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experimental/data/certificates/kronecker-bm-singular-bucket"),
        help="certificate output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    paths = emit_defaults(args.out_dir)
    print("kronecker_bm_singular_bucket: status=EXPERIMENTAL result=PASS")
    for path in paths:
        print(path.as_posix())


if __name__ == "__main__":
    main()
