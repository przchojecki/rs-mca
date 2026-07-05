#!/usr/bin/env python3
"""Replay Kronecker/BM singular-bucket certificates.

Status: AUDIT.  The verifier rebuilds every finite-field object, checks that
`det(H(u)+Z H(v))` is the zero polynomial, verifies the recorded constant
kernel chain, and enumerates all split-locator occupants with exact
periodicity tags.
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


def trim(poly: list[int], p: int) -> list[int]:
    out = [value % p for value in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


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


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def replay_row(record: dict[str, Any]) -> dict[str, Any]:
    p = int(record["p"])
    n = int(record["n"])
    j = int(record["j"])
    domain = subgroup_domain(p, n)
    require(record["domain"]["values"] == domain, "domain mismatch")
    kernel_support = tuple(record["kernel_support"])
    kernel = signed_locator_coeffs([domain[index] for index in kernel_support], j, p)
    require(record["kernel_vector"] == kernel, "kernel mismatch")
    u_sequence = recurrence_sequence(kernel, [1, 2, 3, 4, 5][:j], 2 * j + 1, p)
    v_sequence = recurrence_sequence(kernel, [2, 5, 7, 11, 13][:j], 2 * j + 1, p)
    m0 = hankel(u_sequence, j)
    m1 = hankel(v_sequence, j)
    require(record["u_sequence"] == u_sequence, "u sequence mismatch")
    require(record["v_sequence"] == v_sequence, "v sequence mismatch")
    require(record["hankel_u"] == m0, "H(u) mismatch")
    require(record["hankel_v"] == m1, "H(v) mismatch")
    require(all(value == 0 for value in mat_vec(m0, kernel, p)), "H(u) kernel failure")
    require(all(value == 0 for value in mat_vec(m1, kernel, p)), "H(v) kernel failure")
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


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "schema mismatch")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload.get("payload_sha256") == sha256_payload(payload), "payload hash mismatch")
    any_oracle = False
    for record in payload["rows"]:
        actual = replay_row(record)
        for key, value in actual.items():
            require(record[key] == value, f"{key} mismatch for {record['label']}")
        require(record["determinant_identically_zero"], "singular determinant is not identically zero")
        require(record["aperiodic_occupants"] == 0, "aperiodic singular occupant found")
        any_oracle = any_oracle or record["oracle_gate"]
    require(any_oracle, "missing F_17 oracle row")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, nargs="+", required=True, help="certificate JSON file(s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.check:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check_payload(payload)
        print(f"kronecker_bm_singular_bucket: status=AUDIT result=PASS file={path.as_posix()}")


if __name__ == "__main__":
    main()
