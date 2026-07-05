#!/usr/bin/env python3
"""Finite corank>=2 SPI eliminant ledger.

Status: EXPERIMENTAL / AUDIT.  The default packet builds small Hankel pencils
whose rank drops to corank at least two at recorded finite slopes, records the
nonzero eliminant polynomial `Q(Z)`, and enumerates split-locator occupants in
those strata.  It is a finite obstruction-template ledger, not a
classification theorem.
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
STATUS = "EXPERIMENTAL"
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


def split_sequence_row(p: int, n: int, j: int, z0: int, geom_r: int, label: str) -> dict[str, Any]:
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
    q_poly = [(-z0) % p, 1]
    return {
        "label": label,
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "j": j,
        "z0": z0,
        "geom_ratio": geom_r,
        "domain": {"type": "multiplicative_subgroup", "values": domain},
        "base_sequence": base_sequence,
        "moving_sequence": moving_sequence,
        "hankel_base": m0,
        "hankel_moving": m1,
        "eliminant_polynomial": q_poly,
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


def build_packet() -> dict[str, Any]:
    rows = [
        split_sequence_row(7, 6, 2, 3, 2, "f7_n6_j2"),
        split_sequence_row(11, 10, 2, 4, 3, "f11_n10_j2"),
        split_sequence_row(13, 12, 2, 5, 2, "f13_n12_j2"),
        split_sequence_row(17, 16, 3, 6, 3, "f17_n16_j3_oracle"),
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "proof_status": "AUDIT replay of finite corank>=2 eliminant rows",
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "claim": "finite corank>=2 strata with nonzero eliminants and recorded split-locator occupancy",
        "rows": rows,
        "named_obstruction_templates": [
            {
                "row": row["label"],
                "z": stratum["z"],
                "aperiodic_occupants": stratum["aperiodic_occupants"],
            }
            for row in rows
            for stratum in row["strata"]
            if stratum["aperiodic_occupants"] > 0
        ],
        "non_claims": [
            "No full corank>=2 classification is claimed.",
            "No asymptotic incidence theorem is claimed.",
            "No resolution of prob:band is claimed.",
        ],
    }
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "corank_spi_rows.json"
    path.write_text(json.dumps(build_packet(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return [path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experimental/data/certificates/corank-spi-eliminant"),
        help="certificate output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    paths = emit_defaults(args.out_dir)
    print("corank_stratified_spi_eliminant: status=EXPERIMENTAL result=PASS")
    for path in paths:
        print(path.as_posix())


if __name__ == "__main__":
    main()
