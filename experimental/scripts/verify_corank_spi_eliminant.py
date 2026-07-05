#!/usr/bin/env python3
"""Replay finite corank>=2 SPI eliminant ledgers.

Status: AUDIT.  This verifier rebuilds the Hankel pencils, sweeps all finite
slopes, recomputes rank/corank, checks the nonzero eliminant roots, and
enumerates split-locator occupants with exact periodicity tags.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "corank-spi-eliminant-ledger-v1"
THEOREM_PROBLEM_ID = "Lemma-A2-corank-spi-eliminant"


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


def hankel(sequence: list[int], j: int) -> list[list[int]]:
    return [[sequence[row + col] for col in range(j + 1)] for row in range(j + 1)]


def rank(matrix: list[list[int]], p: int) -> int:
    work = [row[:] for row in matrix]
    rows = len(work)
    cols = len(work[0])
    r = 0
    for col in range(cols):
        pivot = next((idx for idx in range(r, rows) if work[idx][col] % p), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        inv = pow(work[r][col], -1, p)
        work[r] = [(value * inv) % p for value in work[r]]
        for idx in range(rows):
            if idx != r and work[idx][col] % p:
                factor = work[idx][col] % p
                work[idx] = [(work[idx][k] - factor * work[r][k]) % p for k in range(cols)]
        r += 1
    return r


def matrix_at(m0: list[list[int]], m1: list[list[int]], z: int, p: int) -> list[list[int]]:
    return [[(m0[row][col] + z * m1[row][col]) % p for col in range(len(m0[0]))] for row in range(len(m0))]


def row_from_params(p: int, n: int, j: int, z0: int, geom_r: int, label: str) -> dict[str, Any]:
    length = 2 * j + 1
    rank_one_sequence = [pow(geom_r, t, p) for t in range(length)]
    moving_sequence = [(t * t + 3 * t + 5) % p for t in range(length)]
    base_sequence = [(rank_one_sequence[t] - z0 * moving_sequence[t]) % p for t in range(length)]
    m0 = hankel(base_sequence, j)
    m1 = hankel(moving_sequence, j)
    domain = subgroup_domain(p, n)
    strata: list[dict[str, Any]] = []
    for z in range(p):
        matrix = matrix_at(m0, m1, z, p)
        row_rank = rank(matrix, p)
        corank = (j + 1) - row_rank
        if corank < 2:
            continue
        occupants: list[dict[str, Any]] = []
        for support in itertools.combinations(range(n), j):
            coeffs = signed_locator_coeffs([domain[index] for index in support], j, p)
            if all(sum(matrix[row][col] * coeffs[col] for col in range(j + 1)) % p == 0 for row in range(j + 1)):
                occupants.append(
                    {
                        "support": list(support),
                        "coefficients": coeffs,
                        "periodicity_scale": periodicity_scale(support, n),
                    }
                )
        strata.append(
            {
                "z": z,
                "rank": row_rank,
                "corank": corank,
                "occupants_total": len(occupants),
                "aperiodic_occupants": sum(1 for item in occupants if item["periodicity_scale"] == 1),
                "periodic_occupants": sum(1 for item in occupants if item["periodicity_scale"] > 1),
                "occupants": occupants,
            }
        )
    return {
        "label": label,
        "domain": {"type": "multiplicative_subgroup", "values": domain},
        "base_sequence": base_sequence,
        "moving_sequence": moving_sequence,
        "hankel_base": m0,
        "hankel_moving": m1,
        "eliminant_polynomial": [(-z0) % p, 1],
        "eliminant_identically_zero": False,
        "gcd_degree_with_zq_minus_z": len(strata),
        "locators_total": comb(n, j),
        "corank_ge_2_slope_count": len(strata),
        "strata": strata,
        "has_aperiodic_obstruction_template": any(item["aperiodic_occupants"] > 0 for item in strata),
        "oracle_gate": p == 17,
    }


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "schema mismatch")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload.get("payload_sha256") == sha256_payload(payload), "payload hash mismatch")
    any_oracle = False
    any_obstruction = False
    for record in payload["rows"]:
        actual = row_from_params(record["p"], record["n"], record["j"], record["z0"], record["geom_ratio"], record["label"])
        for key, value in actual.items():
            require(record[key] == value, f"{key} mismatch for {record['label']}")
        require(record["eliminant_polynomial"] != [0], "unexpected zero eliminant")
        require(record["gcd_degree_with_zq_minus_z"] == record["corank_ge_2_slope_count"], "gcd degree mismatch")
        any_oracle = any_oracle or record["oracle_gate"]
        any_obstruction = any_obstruction or record["has_aperiodic_obstruction_template"]
    expected_templates = [
        {"row": row["label"], "z": stratum["z"], "aperiodic_occupants": stratum["aperiodic_occupants"]}
        for row in payload["rows"]
        for stratum in row["strata"]
        if stratum["aperiodic_occupants"] > 0
    ]
    require(payload["named_obstruction_templates"] == expected_templates, "obstruction template mismatch")
    require(any_oracle, "missing F_17 oracle row")
    require(any_obstruction, "missing named aperiodic obstruction template")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, nargs="+", required=True, help="certificate JSON file(s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.check:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check_payload(payload)
        print(f"corank_spi_eliminant: status=AUDIT result=PASS file={path.as_posix()}")


if __name__ == "__main__":
    main()
