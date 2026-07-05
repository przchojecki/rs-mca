#!/usr/bin/env python3
"""Replay Q1 prefix-collision ledger certificates with stdlib arithmetic."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from math import comb, gcd
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "q1-prefix-collision-ledger-v1"
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
    for used, value in enumerate(values, start=1):
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


def recompute_row(record: dict[str, Any]) -> dict[str, Any]:
    p = int(record["p"])
    n = int(record["n"])
    m = int(record["m"])
    w = int(record["w"])
    domain = subgroup_domain(p, n)
    rows = []
    hist: Counter[tuple[int, ...]] = Counter()
    for indices in itertools.combinations(range(n), m):
        key = signed_prefix([domain[index] for index in indices], w, p)
        rows.append({"indices": indices, "key": key})
        hist[key] += 1
    size_hist = Counter(hist.values())
    second = sum(count * count for count in hist.values())
    max_fiber = max(hist.values()) if hist else 0
    out = {
        "total_subsets": comb(n, m),
        "distinct_prefix_values": len(hist),
        "fiber_size_histogram": {str(k): v for k, v in sorted(size_hist.items())},
        "max_fiber": max_fiber,
        "second_moment": second,
        "density_heuristic": {
            "denominator": p ** w,
            "average_fiber": ratio_string(comb(n, m), p ** w),
            "max_over_average": ratio_string(max_fiber * (p ** w), comb(n, m)),
        },
    }
    pair = record["pair_strata"]
    if pair["coverage"] == "full-ordered-pair-enumeration":
        strata: Counter[tuple[int, int]] = Counter()
        rigidity_ok = True
        min_nontrivial_exchange: int | None = None
        for left in rows:
            left_set = set(left["indices"])
            for right in rows:
                if left["key"] != right["key"]:
                    continue
                right_set = set(right["indices"])
                e = len(left_set - right_set)
                scale = periodicity_scale(left_set.symmetric_difference(right_set), n) if left_set != right_set else n
                strata[(e, scale)] += 1
                if left_set != right_set and e < w + 1:
                    rigidity_ok = False
                if left_set != right_set:
                    min_nontrivial_exchange = e if min_nontrivial_exchange is None else min(min_nontrivial_exchange, e)
        out["pair_strata"] = {
            "coverage": "full-ordered-pair-enumeration",
            "ordered_pairs_examined": len(rows) * len(rows),
            "same_prefix_ordered_pairs": sum(strata.values()),
            "strata": {f"e={e},scale={scale}": count for (e, scale), count in sorted(strata.items())},
            "rigidity_e_ge_w_plus_1_for_nontrivial_pairs": rigidity_ok,
            "minimum_nontrivial_exchange_size": min_nontrivial_exchange,
            "stratified_sum_equals_second_moment": sum(strata.values()) == second,
            "w_plus_1_divides_n": n % (w + 1) == 0,
        }
    return out


def sha256_payload(payload: dict[str, Any]) -> str:
    clean = json.loads(json.dumps(payload, sort_keys=True))
    clean.pop("payload_sha256", None)
    blob = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def check_payload(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA_VERSION, "schema mismatch")
    require(payload.get("theorem_problem_id") == THEOREM_PROBLEM_ID, "theorem/problem id mismatch")
    require(payload.get("payload_sha256") == sha256_payload(payload), "payload hash mismatch")
    for record in payload["rows"]:
        actual = recompute_row(record)
        for key in ("total_subsets", "distinct_prefix_values", "fiber_size_histogram", "max_fiber", "second_moment", "density_heuristic"):
            require(record[key] == actual[key], f"{key} mismatch for {(record['p'], record['n'], record['m'], record['w'])}")
        if record["pair_strata"]["coverage"] == "full-ordered-pair-enumeration":
            actual_pair = actual["pair_strata"]
            for key in (
                "ordered_pairs_examined",
                "same_prefix_ordered_pairs",
                "strata",
                "rigidity_e_ge_w_plus_1_for_nontrivial_pairs",
                "minimum_nontrivial_exchange_size",
                "stratified_sum_equals_second_moment",
                "w_plus_1_divides_n",
            ):
                require(record["pair_strata"][key] == actual_pair[key], f"pair {key} mismatch")
            require(record["pair_strata"]["stratified_sum_equals_second_moment"], "pair strata do not sum to second moment")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, nargs="+", required=True, help="certificate JSON file(s)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for path in args.check:
        payload = json.loads(path.read_text(encoding="utf-8"))
        check_payload(payload)
        print(f"q1_prefix_collision_ledger: status=AUDIT result=PASS file={path.as_posix()}")


if __name__ == "__main__":
    main()
