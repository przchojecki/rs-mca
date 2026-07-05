#!/usr/bin/env python3
"""Exact small-row W_z Hankel-pencil split-locator sweep.

Status: EXPERIMENTAL / AUDIT.  The scanner builds the finite-field pencil
`A(l)+zB(l)=0` from recorded syndrome vectors and counts split locators in
each slope fiber.  The default rows are small enough for exact stdlib replay;
no accelerator is required for the committed certificate.
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
STATUS = "EXPERIMENTAL"
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


def sweep_row(p: int, n: int, j: int, codim: int, k: int, a: int, label: str) -> dict[str, Any]:
    domain = subgroup_domain(p, n)
    f_values, g_values = source_vectors(p, n)
    u = syndrome(f_values, domain, j + codim, p)
    v = syndrome(g_values, domain, j + codim, p)
    locators: list[tuple[tuple[int, ...], list[int], int]] = []
    for support in itertools.combinations(range(n), j):
        coeffs = signed_locator_coeffs([domain[index] for index in support], j, p)
        locators.append((support, coeffs, periodicity_scale(support, n)))
    slope_summary: list[dict[str, int]] = []
    witnesses: list[dict[str, Any]] = []
    max_aperiodic = -1
    for z in range(p):
        total = 0
        aperiodic = 0
        periodic = 0
        examples: list[dict[str, Any]] = []
        for support, coeffs, scale in locators:
            if solves(coeffs, u, v, z, codim, p):
                total += 1
                if scale == 1:
                    aperiodic += 1
                else:
                    periodic += 1
                if len(examples) < 5:
                    examples.append({"support": list(support), "coefficients": coeffs, "periodicity_scale": scale})
        slope_summary.append({"z": z, "total": total, "aperiodic": aperiodic, "periodic": periodic})
        if aperiodic > max_aperiodic:
            max_aperiodic = aperiodic
            witnesses = [{"z": z, "examples": examples}]
        elif aperiodic == max_aperiodic:
            witnesses.append({"z": z, "examples": examples})
    density_ceiling = (comb(n, j) + p**codim - 1) // (p**codim)
    flagged = [item for item in slope_summary if item["aperiodic"] > density_ceiling]
    deep_rhs = n - a + 1
    return {
        "label": label,
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "k": k,
        "a": a,
        "j": j,
        "codim": codim,
        "domain": {"type": "multiplicative_subgroup", "values": domain},
        "source": {"f_values": f_values, "g_values": g_values},
        "u_syndrome": u,
        "v_syndrome": v,
        "locators_total": comb(n, j),
        "slopes_total": p,
        "incidence_tests": p * comb(n, j),
        "density_predictor_ceiling": density_ceiling,
        "max_aperiodic": max_aperiodic,
        "max_slopes": [item["z"] for item in slope_summary if item["aperiodic"] == max_aperiodic],
        "flagged_over_density_slopes": flagged,
        "deep_gate_rhs": deep_rhs,
        "deep_gate_pass": max_aperiodic <= deep_rhs,
        "slope_summary": slope_summary,
        "witnesses": witnesses[:8],
    }


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def finalize(payload: dict[str, Any]) -> dict[str, Any]:
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def build_deep_gate() -> dict[str, Any]:
    return finalize(
        {
            "schema_version": SCHEMA_VERSION,
            "status": STATUS,
            "proof_status": "AUDIT replay of exact finite sweep",
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "claim": "deep-gate row where max aperiodic W_z occupancy is bounded by n-a+1",
            "rows": [sweep_row(41, 40, 3, 3, 10, 40, "deep_gate_f41")],
            "scope": ["Finite Hankel-pencil incidence row; not a global line-decoding theorem."],
        }
    )


def build_band_sweep() -> dict[str, Any]:
    return finalize(
        {
            "schema_version": SCHEMA_VERSION,
            "status": STATUS,
            "proof_status": "AUDIT replay of exact finite sweep",
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "claim": "small exact W_z slope sweeps with over-density flags relative to the naive density ceiling",
            "rows": [
                sweep_row(31, 30, 3, 2, 10, 20, "band_sweep_f31"),
                sweep_row(41, 40, 3, 2, 14, 27, "band_sweep_f41"),
            ],
            "scope": [
                "All slopes are swept for the recorded finite rows.",
                "The packet does not claim a complete prob:band refutation.",
            ],
        }
    )


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    payloads = {
        "deep_gate_f41.json": build_deep_gate(),
        "band_sweep_f41_f31.json": build_band_sweep(),
    }
    paths: list[Path] = []
    for name, payload in payloads.items():
        path = out_dir / name
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        paths.append(path)
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write default certificate files")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experimental/data/certificates/wz-slope-sweep"),
        help="certificate output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    paths = emit_defaults(args.out_dir)
    print("wz_slope_sweep: status=EXPERIMENTAL result=PASS")
    for path in paths:
        print(path.as_posix())


if __name__ == "__main__":
    main()
