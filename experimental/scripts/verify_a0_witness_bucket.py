#!/usr/bin/env python3
"""Replay A0 witness-bucket periodicity certificates.

Status: AUDIT.  This stdlib-only verifier reconstructs each recorded prime
field row, checks the support-collinearity witness, enumerates every agreement
support of size at least `a`, and matches the recorded periodicity buckets.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "a0-witness-bucket-v1"
THEOREM_PROBLEM_ID = "A0-witness-bucket-periodicity"


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


def interpolate_degree(xs: list[int], ys: list[int], p: int) -> int:
    require(len(xs) == len(ys), "point count mismatch")
    coeff = [0] * len(xs)
    for i, x_i in enumerate(xs):
        basis = [1]
        denom = 1
        for j, x_j in enumerate(xs):
            if i == j:
                continue
            basis = [0] + basis
            for degree in range(len(basis) - 1):
                basis[degree] = (basis[degree] - x_j * basis[degree + 1]) % p
            denom = (denom * (x_i - x_j)) % p
        scale = (ys[i] * pow(denom, -1, p)) % p
        for degree, value in enumerate(basis):
            coeff[degree] = (coeff[degree] + scale * value) % p
    while coeff and coeff[-1] % p == 0:
        coeff.pop()
    return len(coeff) - 1 if coeff else -1


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def replay_row(record: dict[str, Any]) -> dict[str, Any]:
    p = int(record["p"])
    n = int(record["n"])
    k = int(record["k"])
    a = int(record["a"])
    slope = int(record["slope"])
    domain = subgroup_domain(p, n)
    require(record["domain"]["values"] == domain, "domain mismatch")
    f_values = [int(x) % p for x in record["line"]["f_values"]]
    g_values = [int(x) % p for x in record["line"]["g_values"]]
    require(len(f_values) == n and len(g_values) == n, "line length mismatch")
    base_support = tuple(int(i) for i in record["base_support"])
    require(all(f_values[i] == (-slope * g_values[i]) % p for i in base_support), "base support is not parallel")
    require(any(g_values[i] % p != 0 for i in base_support), "parallel witness is zero")
    y_values = [(f_values[i] + slope * g_values[i]) % p for i in range(n)]
    histogram: dict[str, int] = {}
    total = 0
    periodic = 0
    for size in range(a, n + 1):
        for support in itertools.combinations(range(n), size):
            degree = interpolate_degree([domain[i] for i in support], [y_values[i] for i in support], p)
            if degree < k:
                total += 1
                scale = periodicity_scale(support, n)
                histogram[str(scale)] = histogram.get(str(scale), 0) + 1
                if scale > 1:
                    periodic += 1
    return {
        "candidate_supports_examined": sum(comb(n, size) for size in range(a, n + 1)),
        "agreement_supports_total": total,
        "periodicity_scale_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "periodic_witness_supports": periodic,
        "aperiodic_witness_supports": total - periodic,
    }


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "schema mismatch")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload.get("payload_sha256") == sha256_payload(payload), "payload hash mismatch")
    for record in payload["rows"]:
        actual = replay_row(record)
        for key, value in actual.items():
            require(record[key] == value, f"{key} mismatch for {(record['p'], record['n'], record['k'], record['a'])}")
        require(record["agreement_supports_total"] > 0, "missing agreement support")
        require(record["aperiodic_witness_supports"] > 0, "missing aperiodic support")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, nargs="+", required=True, help="certificate JSON file(s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.check:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check_payload(payload)
        print(f"a0_witness_bucket: status=AUDIT result=PASS file={path.as_posix()}")


if __name__ == "__main__":
    main()
