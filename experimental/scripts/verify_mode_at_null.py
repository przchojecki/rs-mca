#!/usr/bin/env python3
"""Replay mode-at-null extremality packets with stdlib arithmetic.

Status: AUDIT.  The verifier reconstructs the multiplicative subgroup, signed
split-locator coefficients, Hankel syndrome vectors, alignment slopes, point
dictator occupancies, and periodicity-scale tags for every recorded row.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "mode-at-null-extremality-v1"
THEOREM_PROBLEM_ID = "T2-mode-at-null-extremality"


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
    factors: list[int] = []
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


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
    x = 1
    out: list[int] = []
    for _ in range(n):
        out.append(x)
        x = (x * step) % p
    require(x == 1 and len(set(out)) == n, "bad multiplicative domain")
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


def source_vectors(p: int, n: int) -> tuple[list[int], list[int]]:
    u_values = [((i + 1) * (i + 3) + 7) % p for i in range(n)]
    v_values = [((i + 2) * (i + 5) * (i + 7) + 3) % p for i in range(n)]
    return u_values, v_values


def syndrome(values: list[int], domain: list[int], length: int, p: int) -> list[int]:
    return [sum(values[i] * pow(domain[i], r, p) for i in range(len(domain))) % p for r in range(length)]


def alignment_slope(a_vec: list[int], b_vec: list[int], p: int) -> int | None:
    if all(value % p == 0 for value in b_vec):
        return None
    z: int | None = None
    for a_value, b_value in zip(a_vec, b_vec):
        if b_value % p:
            candidate = (a_value * pow(b_value, -1, p)) % p
            if z is None:
                z = candidate
            elif z != candidate:
                return None
        elif a_value % p:
            return None
    return z


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def replay_row(record: dict[str, Any]) -> dict[str, Any]:
    p = int(record["p"])
    n = int(record["n"])
    j = int(record["j"])
    codim = int(record["codim"])
    domain = subgroup_domain(p, n)
    require(record["domain"]["values"] == domain, "domain mismatch")
    u_values, v_values = source_vectors(p, n)
    require(record["source"]["u_values"] == u_values, "u source mismatch")
    require(record["source"]["v_values"] == v_values, "v source mismatch")
    u_syn = syndrome(u_values, domain, j + codim, p)
    v_syn = syndrome(v_values, domain, j + codim, p)
    require(record["u_syndrome"] == u_syn, "u syndrome mismatch")
    require(record["v_syndrome"] == v_syn, "v syndrome mismatch")
    slope_buckets: dict[int, list[dict[str, Any]]] = {z: [] for z in range(p)}
    for support in itertools.combinations(range(n), j):
        coeffs = signed_locator_coeffs([domain[index] for index in support], j, p)
        a_vec = [sum(u_syn[row_index + degree] * coeffs[degree] for degree in range(j + 1)) % p for row_index in range(codim)]
        b_vec = [sum(v_syn[row_index + degree] * coeffs[degree] for degree in range(j + 1)) % p for row_index in range(codim)]
        z = alignment_slope(a_vec, b_vec, p)
        if z is None:
            continue
        slope_buckets[z].append(
            {
                "support": list(support),
                "coefficients": coeffs,
                "periodicity_scale": periodicity_scale(support, n),
                "a_vector": a_vec,
                "b_vector": b_vec,
            }
        )
    slope_summary: list[dict[str, Any]] = []
    flagged: list[dict[str, Any]] = []
    for z in range(p):
        bucket = slope_buckets[z]
        aperiodic = [item for item in bucket if item["periodicity_scale"] == 1]
        periodic = len(bucket) - len(aperiodic)
        dictator_counts = [sum(1 for item in bucket if point in item["support"]) for point in range(n)]
        null_occupancy = max(dictator_counts) if dictator_counts else 0
        null_points = [index for index, count in enumerate(dictator_counts) if count == null_occupancy]
        inversion = len(aperiodic) > null_occupancy
        slope_record = {
            "z": z,
            "aligned_total": len(bucket),
            "aperiodic": len(aperiodic),
            "periodic": periodic,
            "best_point_dictator_occupancy": null_occupancy,
            "best_point_dictator_points": null_points,
            "non_null_aperiodic_exceeds_dictator": inversion,
        }
        slope_summary.append(slope_record)
        if inversion:
            flagged.append({**slope_record, "examples": aperiodic[:6]})
    return {
        "locators_total": comb(n, j),
        "aligned_total": sum(item["aligned_total"] for item in slope_summary),
        "slopes_total": p,
        "flagged_slope_count": len(flagged),
        "proxy_inversion_flagged": bool(flagged),
        "slope_summary": slope_summary,
        "flagged_slopes": flagged,
        "oracle_gate": p == 17,
        "oracle_gate_statement": "F_17 split-locator enumeration is included and replayed exactly" if p == 17 else None,
    }


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "schema mismatch")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload.get("payload_sha256") == sha256_payload(payload), "payload hash mismatch")
    any_proxy_inversion = False
    any_oracle = False
    for record in payload["rows"]:
        actual = replay_row(record)
        for key, value in actual.items():
            require(record[key] == value, f"{key} mismatch for {record['label']}")
        any_proxy_inversion = any_proxy_inversion or actual["proxy_inversion_flagged"]
        any_oracle = any_oracle or actual["oracle_gate"]
        for flagged in record["flagged_slopes"]:
            require(flagged["non_null_aperiodic_exceeds_dictator"], "flagged slope is not an inversion")
            for example in flagged["examples"]:
                support = tuple(example["support"])
                coeffs = signed_locator_coeffs([record["domain"]["values"][index] for index in support], record["j"], record["p"])
                require(coeffs == example["coefficients"], "example coefficient mismatch")
                require(periodicity_scale(support, record["n"]) == 1, "example is not aperiodic")
    require(any_proxy_inversion, "packet has no finite proxy inversion")
    require(any_oracle, "missing F_17 oracle-gate row")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, nargs="+", required=True, help="certificate JSON file(s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.check:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check_payload(payload)
        print(f"mode_at_null: status=AUDIT result=PASS file={path.as_posix()}")


if __name__ == "__main__":
    main()
