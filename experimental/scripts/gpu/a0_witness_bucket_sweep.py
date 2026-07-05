#!/usr/bin/env python3
"""A0 witness-bucket periodicity sweep for small prime fields.

Status: EXPERIMENTAL / AUDIT.  The script records exact agreement-support
bucket counts for one explicit pole-line-style slope in each small row.  It is
placed with accelerator-facing scanners, but the default packet uses stdlib
arithmetic only and is replayed by `verify_a0_witness_bucket.py`.
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
STATUS = "EXPERIMENTAL"
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


def line_values(domain: list[int], support: set[int], p: int, slope: int) -> tuple[list[int], list[int], list[int]]:
    g_values = [1] * len(domain)
    f_values = [(-slope) % p if index in support else domain[index] % p for index in range(len(domain))]
    y_values = [(f_values[index] + slope * g_values[index]) % p for index in range(len(domain))]
    return f_values, g_values, y_values


def support_records(p: int, n: int, k: int, a: int, slope: int, base_support: tuple[int, ...]) -> dict[str, Any]:
    domain = subgroup_domain(p, n)
    f_values, g_values, y_values = line_values(domain, set(base_support), p, slope)
    histogram: dict[str, int] = {}
    examples: list[dict[str, Any]] = []
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
                if len(examples) < 12:
                    examples.append({"support": list(support), "size": size, "degree": degree, "periodicity_scale": scale})
    base_parallel = all(f_values[i] == (-slope * g_values[i]) % p for i in base_support)
    return {
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "k": k,
        "a": a,
        "slope": slope,
        "domain": {"type": "multiplicative_subgroup", "values": domain},
        "line": {"f_values": f_values, "g_values": g_values},
        "base_support": list(base_support),
        "base_support_is_parallel": base_parallel,
        "candidate_supports_examined": sum(comb(n, size) for size in range(a, n + 1)),
        "agreement_supports_total": total,
        "periodicity_scale_histogram": dict(sorted(histogram.items(), key=lambda item: int(item[0]))),
        "periodic_witness_supports": periodic,
        "aperiodic_witness_supports": total - periodic,
        "all_recorded_supports_exact": True,
        "examples": examples,
    }


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def build_packet(p: int, n: int, k: int, a: int) -> dict[str, Any]:
    row = support_records(p, n, k, a, 1, tuple(range(a)))
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "proof_status": "AUDIT replay of a recorded finite sweep",
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "claim": "exact periodicity bucket counts for one recorded pole-line-style slope",
        "scope": [
            "The row enumerates every agreement support of size at least a for the recorded slope.",
            "The row is not a full identity-prefix-floor conversion theorem.",
        ],
        "rows": [row],
    }
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    specs = {
        "f5.json": (5, 4, 1, 2),
        "f7.json": (7, 6, 2, 3),
        "f13.json": (13, 12, 4, 5),
        "f17.json": (17, 16, 6, 7),
    }
    paths: list[Path] = []
    for name, spec in specs.items():
        payload = build_packet(*spec)
        path = out_dir / name
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate rows")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experimental/data/certificates/a0-witness-bucket"),
        help="certificate output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    paths = emit_defaults(args.out_dir)
    print("a0_witness_bucket_sweep: status=EXPERIMENTAL result=PASS")
    for path in paths:
        print(path.as_posix())


if __name__ == "__main__":
    main()
