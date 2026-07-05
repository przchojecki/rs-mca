#!/usr/bin/env python3
"""Prefix-collision second-moment ledger for split locators.

Status: EXPERIMENTAL / AUDIT.  The script computes prefix fibers
`Phi_w(M)=((-1)^i e_i(M))_{i<=w}` for fixed-size subsets of a multiplicative
domain and records exact second moments.  Direct pair strata are emitted for
small rows; larger rows are exact histogram rows with that scope stated.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from math import comb, gcd
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "q1-prefix-collision-ledger-v1"
STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "Q-prefix-collision-flatness"


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


def signed_prefix(values: Iterable[int], w: int, p: int) -> tuple[int, ...]:
    elementary = [0] * (w + 1)
    elementary[0] = 1
    used = 0
    for value in values:
        used += 1
        for degree in range(min(used, w), 0, -1):
            elementary[degree] = (elementary[degree] + elementary[degree - 1] * value) % p
    return tuple(((-1 if degree % 2 else 1) * elementary[degree]) % p for degree in range(1, w + 1))


def periodicity_scale(indices: Iterable[int], n: int) -> int:
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


def ratio_string(numer: int, denom: int) -> str:
    g = gcd(abs(numer), abs(denom))
    numer //= g
    denom //= g
    return f"{numer}/{denom}" if denom != 1 else str(numer)


def subset_rows(p: int, n: int, m: int, w: int) -> list[dict[str, Any]]:
    domain = subgroup_domain(p, n)
    rows = []
    for indices in itertools.combinations(range(n), m):
        key = signed_prefix([domain[index] for index in indices], w, p)
        rows.append({"indices": indices, "key": key, "scale": periodicity_scale(indices, n)})
    return rows


def direct_pair_strata(rows: list[dict[str, Any]], n: int, max_pairs: int) -> dict[str, Any] | None:
    pair_count = len(rows) * len(rows)
    if pair_count > max_pairs:
        return None
    strata: Counter[tuple[int, int]] = Counter()
    rigidity_ok = True
    min_nontrivial_exchange: int | None = None
    examples = []
    for left in rows:
        left_set = set(left["indices"])
        for right in rows:
            if left["key"] != right["key"]:
                continue
            right_set = set(right["indices"])
            e = len(left_set - right_set)
            scale = periodicity_scale(left_set.symmetric_difference(right_set), n) if left_set != right_set else n
            strata[(e, scale)] += 1
            if left_set != right_set and e < len(left["key"]) + 1:
                rigidity_ok = False
            if left_set != right_set:
                min_nontrivial_exchange = e if min_nontrivial_exchange is None else min(min_nontrivial_exchange, e)
            if left_set != right_set and len(examples) < 8:
                examples.append({"left": list(left["indices"]), "right": list(right["indices"]), "exchange_size": e, "difference_scale": scale})
    return {
        "coverage": "full-ordered-pair-enumeration",
        "ordered_pairs_examined": pair_count,
        "same_prefix_ordered_pairs": sum(strata.values()),
        "strata": {f"e={e},scale={scale}": count for (e, scale), count in sorted(strata.items())},
        "rigidity_e_ge_w_plus_1_for_nontrivial_pairs": rigidity_ok,
        "minimum_nontrivial_exchange_size": min_nontrivial_exchange,
        "examples": examples,
    }


def row(p: int, n: int, m: int, w: int, max_pairs: int) -> dict[str, Any]:
    rows = subset_rows(p, n, m, w)
    hist: Counter[tuple[int, ...]] = Counter(item["key"] for item in rows)
    size_hist = Counter(hist.values())
    second_moment = sum(count * count for count in hist.values())
    max_fiber = max(hist.values()) if hist else 0
    max_keys = sorted(key for key, count in hist.items() if count == max_fiber)
    pair = direct_pair_strata(rows, n, max_pairs)
    if pair is not None:
        pair["stratified_sum_equals_second_moment"] = pair["same_prefix_ordered_pairs"] == second_moment
        pair["w_plus_1_divides_n"] = n % (w + 1) == 0
    total = comb(n, m)
    density_denominator = p ** w
    return {
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "m": m,
        "w": w,
        "object": "Phi_w prefix fibers on m-subsets without replacement",
        "total_subsets": total,
        "distinct_prefix_values": len(hist),
        "fiber_size_histogram": {str(k): v for k, v in sorted(size_hist.items())},
        "max_fiber": max_fiber,
        "max_prefixes": [list(key) for key in max_keys[:8]],
        "second_moment": second_moment,
        "density_heuristic": {
            "denominator": density_denominator,
            "average_fiber": ratio_string(total, density_denominator),
            "max_over_average": ratio_string(max_fiber * density_denominator, total),
        },
        "pair_strata": pair
        if pair is not None
        else {
            "coverage": "histogram-only",
            "ordered_pairs_examined": None,
            "same_prefix_ordered_pairs": second_moment,
            "rigidity_e_ge_w_plus_1_for_nontrivial_pairs": None,
        },
    }


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def finalize(payload: dict[str, Any]) -> dict[str, Any]:
    payload["payload_sha256"] = sha256_payload(payload)
    return payload


def build_l2_constant() -> dict[str, Any]:
    rows = [
        row(5, 4, 2, 1, 2_000_000),
        row(7, 6, 3, 2, 2_000_000),
        row(11, 10, 4, 2, 2_000_000),
        row(17, 16, 6, 4, 2_000_000),
    ]
    return finalize(
        {
            "schema_version": SCHEMA_VERSION,
            "status": STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "claim": "exact prefix-fiber second moments for recorded finite rows",
            "proof_status": "EXPERIMENTAL with AUDIT replay",
            "rows": rows,
            "non_claims": [
                "No worst-case flatness theorem is claimed.",
                "Histogram-only rows do not include direct ordered-pair strata.",
            ],
        }
    )


def build_beta_envelope() -> dict[str, Any]:
    rows = [
        row(5, 4, 2, 1, 2_000_000),
        row(7, 6, 3, 2, 2_000_000),
        row(11, 10, 4, 2, 2_000_000),
        row(17, 16, 6, 4, 2_000_000),
        row(41, 40, 5, 2, 0),
    ]
    return finalize(
        {
            "schema_version": SCHEMA_VERSION,
            "status": STATUS,
            "theorem_problem_id": THEOREM_PROBLEM_ID,
            "claim": "measured beta-envelope table for prefix-fiber occupancy",
            "proof_status": "EXPERIMENTAL",
            "rows": rows,
            "non_claims": [
                "The table is measured evidence, not an asymptotic envelope theorem.",
                "The F_41 row is exact for the histogram but omits direct pair strata.",
            ],
        }
    )


def emit_defaults(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    payloads = {
        "l2_constant.json": build_l2_constant(),
        "beta_envelope_table.json": build_beta_envelope(),
    }
    paths = []
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
        default=Path("experimental/data/certificates/q1-prefix-collision"),
        help="certificate output directory",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.emit_defaults:
        raise SystemExit("nothing requested; use --emit-defaults")
    paths = emit_defaults(args.out_dir)
    print("q1_prefix_collision_ledger: status=EXPERIMENTAL result=PASS")
    for path in paths:
        print(path.as_posix())


if __name__ == "__main__":
    main()
