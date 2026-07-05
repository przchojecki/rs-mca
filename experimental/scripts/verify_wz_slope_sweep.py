#!/usr/bin/env python3
"""Replay exact W_z Hankel-pencil slope-sweep certificates.

Status: AUDIT.  The verifier is stdlib-only: it reconstructs the domain,
syndrome vectors, split-locator coefficients, cyclic periodicity tags, and the
full per-slope incidence table recorded in the certificate JSON.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "wz-slope-sweep-v1"
THEOREM_PROBLEM_ID = "A-side-Wz-syndrome-annihilator"


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


def source_vectors(p: int, n: int) -> tuple[list[int], list[int]]:
    f_values = [((i + 1) * (i + 3) + 7) % p for i in range(n)]
    g_values = [((i + 2) * (i + 5) * (i + 7) + 3) % p for i in range(n)]
    return f_values, g_values


def syndrome(values: list[int], domain: list[int], length: int, p: int) -> list[int]:
    return [sum(values[i] * pow(domain[i], r, p) for i in range(len(domain))) % p for r in range(length)]


def solves(coeffs: list[int], u: list[int], v: list[int], z: int, codim: int, p: int) -> bool:
    j = len(coeffs) - 1
    for row in range(codim):
        total = 0
        for degree in range(j + 1):
            total = (total + ((u[row + degree] + z * v[row + degree]) % p) * coeffs[degree]) % p
        if total != 0:
            return False
    return True


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
    f_values, g_values = source_vectors(p, n)
    require(record["source"]["f_values"] == f_values, "f source mismatch")
    require(record["source"]["g_values"] == g_values, "g source mismatch")
    u = syndrome(f_values, domain, j + codim, p)
    v = syndrome(g_values, domain, j + codim, p)
    require(record["u_syndrome"] == u, "u syndrome mismatch")
    require(record["v_syndrome"] == v, "v syndrome mismatch")
    locators: list[tuple[tuple[int, ...], list[int], int]] = []
    for support in itertools.combinations(range(n), j):
        coeffs = signed_locator_coeffs([domain[index] for index in support], j, p)
        locators.append((support, coeffs, periodicity_scale(support, n)))
    slope_summary: list[dict[str, int]] = []
    max_aperiodic = -1
    for z in range(p):
        total = 0
        aperiodic = 0
        periodic = 0
        for _support, coeffs, scale in locators:
            if solves(coeffs, u, v, z, codim, p):
                total += 1
                if scale == 1:
                    aperiodic += 1
                else:
                    periodic += 1
        slope_summary.append({"z": z, "total": total, "aperiodic": aperiodic, "periodic": periodic})
        max_aperiodic = max(max_aperiodic, aperiodic)
    density_ceiling = (comb(n, j) + p**codim - 1) // (p**codim)
    return {
        "locators_total": comb(n, j),
        "slopes_total": p,
        "incidence_tests": p * comb(n, j),
        "density_predictor_ceiling": density_ceiling,
        "max_aperiodic": max_aperiodic,
        "max_slopes": [item["z"] for item in slope_summary if item["aperiodic"] == max_aperiodic],
        "flagged_over_density_slopes": [item for item in slope_summary if item["aperiodic"] > density_ceiling],
        "deep_gate_rhs": int(record["n"]) - int(record["a"]) + 1,
        "deep_gate_pass": max_aperiodic <= int(record["n"]) - int(record["a"]) + 1,
        "slope_summary": slope_summary,
    }


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "schema mismatch")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload.get("payload_sha256") == sha256_payload(payload), "payload hash mismatch")
    for record in payload["rows"]:
        actual = replay_row(record)
        for key, value in actual.items():
            require(record[key] == value, f"{key} mismatch for {record['label']}")
        for witness in record["witnesses"]:
            for example in witness["examples"]:
                coeffs = signed_locator_coeffs([record["domain"]["values"][i] for i in example["support"]], record["j"], record["p"])
                require(coeffs == example["coefficients"], "witness coefficient mismatch")
                require(periodicity_scale(tuple(example["support"]), record["n"]) == example["periodicity_scale"], "witness scale mismatch")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, nargs="+", required=True, help="certificate JSON file(s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.check:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check_payload(payload)
        print(f"wz_slope_sweep: status=AUDIT result=PASS file={path.as_posix()}")


if __name__ == "__main__":
    main()
