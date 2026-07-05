#!/usr/bin/env python3
"""Mode-at-null extremality check for split-locator alignment rows.

Status: EXPERIMENTAL / AUDIT.  The default packet enumerates finite
prime-field rows and records cases where a non-null aperiodic alignment fiber
exceeds the best point-dictator occupancy in the same slope fiber.

The committed packet is small enough for exact CPU enumeration and stdlib
replay by `verify_mode_at_null.py`; no accelerator path is used for these rows.
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
STATUS = "EXPERIMENTAL / AUDIT"
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


def row(p: int, n: int, j: int, codim: int, label: str) -> dict[str, Any]:
    domain = subgroup_domain(p, n)
    u_values, v_values = source_vectors(p, n)
    u_syn = syndrome(u_values, domain, j + codim, p)
    v_syn = syndrome(v_values, domain, j + codim, p)
    slope_buckets: dict[int, list[dict[str, Any]]] = {z: [] for z in range(p)}
    all_examples: list[dict[str, Any]] = []
    for support in itertools.combinations(range(n), j):
        coeffs = signed_locator_coeffs([domain[index] for index in support], j, p)
        a_vec = [sum(u_syn[row_index + degree] * coeffs[degree] for degree in range(j + 1)) % p for row_index in range(codim)]
        b_vec = [sum(v_syn[row_index + degree] * coeffs[degree] for degree in range(j + 1)) % p for row_index in range(codim)]
        z = alignment_slope(a_vec, b_vec, p)
        if z is None:
            continue
        scale = periodicity_scale(support, n)
        record = {
            "support": list(support),
            "coefficients": coeffs,
            "periodicity_scale": scale,
            "a_vector": a_vec,
            "b_vector": b_vec,
        }
        slope_buckets[z].append(record)
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
        examples = aperiodic[:6]
        slope_record = {
            "z": z,
            "aligned_total": len(bucket),
            "aperiodic": len(aperiodic),
            "periodic": periodic,
            "best_point_dictator_occupancy": null_occupancy,
            "best_point_dictator_points": null_points,
            "non_null_aperiodic_exceeds_dictator": inversion,
            "examples": examples,
        }
        slope_summary.append({key: value for key, value in slope_record.items() if key != "examples"})
        if inversion:
            flagged.append(slope_record)
            all_examples.extend(examples)
    return {
        "label": label,
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "j": j,
        "codim": codim,
        "domain": {"type": "multiplicative_subgroup", "values": domain},
        "source": {"u_values": u_values, "v_values": v_values},
        "u_syndrome": u_syn,
        "v_syndrome": v_syn,
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


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def finalize(payload: dict[str, Any]) -> dict[str, Any]:
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def build_default_packet() -> dict[str, Any]:
    rows = [
        row(5, 4, 2, 1, "f5_n4_j2"),
        row(7, 6, 2, 1, "f7_n6_j2"),
        row(7, 6, 3, 1, "f7_n6_j3"),
        row(11, 10, 3, 2, "f11_n10_j3"),
        row(13, 12, 3, 2, "f13_n12_j3"),
        row(17, 16, 3, 2, "f17_n16_j3_oracle"),
        row(17, 16, 4, 2, "f17_n16_j4_oracle"),
    ]
    return finalize(
        {
            "schema_version": SCHEMA_VERSION,
            "status": STATUS,
            "proof_status": "AUDIT replay of finite proxy-occupancy-inversion rows",
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "claim": "finite rows where non-null aperiodic alignment occupancy can exceed the best point-dictator occupancy",
            "rows": rows,
            "non_claims": [
                "No asymptotic worst-case bound is claimed.",
                "No resolution of prob:band is claimed.",
                "The packet tests a concrete finite alignment family only.",
            ],
        }
    )


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "mode_at_null_rows.json"
    path.write_text(json.dumps(build_default_packet(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return [path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default finite packet")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experimental/data/certificates/mode-at-null"),
        help="certificate output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    paths = emit_defaults(args.out_dir)
    print("mode_at_null_extremality: status=EXPERIMENTAL result=PASS")
    for path in paths:
        print(path.as_posix())


if __name__ == "__main__":
    main()
