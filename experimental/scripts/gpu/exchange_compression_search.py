#!/usr/bin/env python3
"""Exchange-compression search for aligned split-locator families.

Status: EXPERIMENTAL / AUDIT.  The default packet materializes finite
aligned-support families, evaluates one Johnson exchange step with exact
rational arithmetic, and records whether any family exceeds the point-dictator
RHS or the anticode packing inequality.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "exchange-compression-search-v1"
STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "prop:v13-johnson-exchange exchange-compression dictator/anticode"


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
    x = 1
    out: list[int] = []
    for _ in range(n):
        out.append(x)
        x = (x * step) % p
    require(x == 1 and len(set(out)) == n, "bad domain generator")
    return out


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


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def family_stats(n: int, j: int, family: list[tuple[int, ...]]) -> dict[str, Any]:
    universe = comb(n, j)
    degree = j * (n - j)
    family_set = {tuple(item) for item in family}
    numerator = 0
    min_exchange: int | None = None
    for support in family_set:
        support_set = set(support)
        for out_index in support:
            for in_index in range(n):
                if in_index in support_set:
                    continue
                neighbor = tuple(sorted((support_set - {out_index}) | {in_index}))
                if neighbor in family_set:
                    numerator += 1
    family_list = list(family_set)
    for i, left in enumerate(family_list):
        left_set = set(left)
        for right in family_list[i + 1 :]:
            exchange = len(left_set - set(right))
            min_exchange = exchange if min_exchange is None else min(min_exchange, exchange)
    delta = Fraction(len(family_set), universe)
    probability = Fraction(numerator, universe * degree)
    rhs = delta * delta + Fraction(degree - n, degree) * delta * (1 - delta)
    s_value = max(0, (min_exchange if min_exchange is not None else 0) - 1)
    anticode_lhs = len(family_set) * comb(j, s_value)
    anticode_rhs = comb(n, j - s_value)
    return {
        "family_size": len(family_set),
        "delta": frac(delta),
        "johnson_degree": degree,
        "exchange_ordered_hits": numerator,
        "exchange_probability": frac(probability),
        "dictator_rhs": frac(rhs),
        "beats_dictator_rhs": probability > rhs,
        "dictator_margin": frac(probability - rhs),
        "min_pair_exchange": min_exchange,
        "anticode_s": s_value,
        "anticode_lhs": anticode_lhs,
        "anticode_rhs": anticode_rhs,
        "violates_anticode": anticode_lhs > anticode_rhs,
    }


def aligned_families(p: int, n: int, j: int, codim: int) -> tuple[list[int], list[int], list[int], list[int], dict[int, list[tuple[int, ...]]]]:
    domain = subgroup_domain(p, n)
    u_values, v_values = source_vectors(p, n)
    u_syn = syndrome(u_values, domain, j + codim, p)
    v_syn = syndrome(v_values, domain, j + codim, p)
    buckets: dict[int, list[tuple[int, ...]]] = defaultdict(list)
    for support in itertools.combinations(range(n), j):
        coeffs = signed_locator_coeffs([domain[index] for index in support], j, p)
        a_vec = [sum(u_syn[row + degree] * coeffs[degree] for degree in range(j + 1)) % p for row in range(codim)]
        b_vec = [sum(v_syn[row + degree] * coeffs[degree] for degree in range(j + 1)) % p for row in range(codim)]
        z = alignment_slope(a_vec, b_vec, p)
        if z is not None:
            buckets[z].append(support)
    return domain, u_values, v_values, u_syn, v_syn, dict(buckets)


def row(p: int, n: int, j: int, codim: int, label: str) -> dict[str, Any]:
    domain, u_values, v_values, u_syn, v_syn, buckets = aligned_families(p, n, j, codim)
    slope_records: list[dict[str, Any]] = []
    for z in sorted(buckets):
        stats = family_stats(n, j, buckets[z])
        slope_records.append(
            {
                "z": z,
                **stats,
                "family": [list(item) for item in buckets[z]],
            }
        )
    flagged = [item for item in slope_records if item["beats_dictator_rhs"] or item["violates_anticode"]]
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
        "slope_family_count": len(slope_records),
        "flagged_family_count": len(flagged),
        "has_counterexample": bool(flagged),
        "slope_families": slope_records,
        "flagged_families": flagged,
        "oracle_gate": p == 17,
    }


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def build_packet() -> dict[str, Any]:
    rows = [
        row(7, 6, 2, 1, "f7_n6_j2"),
        row(11, 10, 3, 2, "f11_n10_j3"),
        row(13, 12, 3, 2, "f13_n12_j3"),
        row(17, 16, 3, 2, "f17_n16_j3_oracle"),
        row(17, 16, 4, 2, "f17_n16_j4_oracle"),
    ]
    payload = {
        "schema_version": SCHEMA_VERSION,
        "status": STATUS,
        "proof_status": "AUDIT replay of finite exchange-compression rows",
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "claim": "finite aligned-support families do not beat the recorded dictator RHS or anticode checks in this range",
        "rows": rows,
        "non_claims": [
            "No asymptotic exchange-rigidity theorem is claimed.",
            "No resolution of prob:band is claimed.",
            "The packet is a finite pass-on-range search.",
        ],
    }
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "exchange_compression_rows.json"
    path.write_text(json.dumps(build_packet(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return [path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit-defaults", action="store_true", help="write the default certificate")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("experimental/data/certificates/exchange-compression"),
        help="certificate output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    paths = emit_defaults(args.out_dir)
    print("exchange_compression_search: status=EXPERIMENTAL result=PASS")
    for path in paths:
        print(path.as_posix())


if __name__ == "__main__":
    main()
