#!/usr/bin/env python3
"""Independent checker for the Q2 heavy-fiber fewness packet.

Status: AUDIT. The checker enumerates the full recorded parameter space and
recomputes every observed prefix fiber from raw support assignments.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from math import comb
from pathlib import Path
from typing import Any


STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "Q2 heavy-fiber fewness; cor:periodic-support-count"
DEFAULT_CERT = Path(
    "experimental/data/certificates/q2-heavy-fiber-fewness/"
    "q2_heavy_fiber_fewness.json"
)


def primitive_root(p: int) -> int:
    factors: list[int] = []
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.append(d)
            while value % d == 0:
                value //= d
        d += 1 if d == 2 else 2
    if value > 1:
        factors.append(value)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise ValueError(f"no primitive root for F_{p}")


def subgroup(p: int, order: int) -> tuple[int, ...]:
    omega = pow(primitive_root(p), (p - 1) // order, p)
    values = tuple(pow(omega, i, p) for i in range(order))
    assert len(set(values)) == order
    return values


def elementary_prefix(domain: tuple[int, ...], support: tuple[int, ...],
                      width: int, p: int) -> tuple[int, ...]:
    # Direct elementary-symmetric route, independent of locator multiplication.
    values = tuple(domain[i] for i in support)
    out = []
    for r in range(1, width + 1):
        total = 0
        for combo in itertools.combinations(values, r):
            prod = 1
            for value in combo:
                prod = (prod * value) % p
            total = (total + prod) % p
        out.append(((-1) ** r * total) % p)
    return tuple(out)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(text: str) -> Fraction:
    num, den = text.split("/")
    return Fraction(int(num), int(den))


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def raw_fibers(p: int, n: int, support_size: int, width: int) -> dict[tuple[int, ...], list[tuple[int, ...]]]:
    domain = subgroup(p, n)
    all_keys = list(itertools.product(range(p), repeat=width))
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = {key: [] for key in all_keys}
    for support in itertools.combinations(range(n), support_size):
        fibers[elementary_prefix(domain, support, width, p)].append(support)
    return fibers


def common_core(items: tuple[tuple[int, ...], ...]) -> int:
    common = set(items[0])
    for item in items[1:]:
        common.intersection_update(item)
    return len(common)


def pair_profile(items: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(sorted(len(set(a).intersection(b)) for a, b in itertools.combinations(items, 2)))


def check_row(row: dict[str, Any]) -> None:
    fibers_all = raw_fibers(row["p"], row["n"], row["support_size"], row["prefix_width"])
    nonempty = {key: values for key, values in fibers_all.items() if values}
    histogram = Counter(len(values) for values in nonempty.values())
    total = comb(row["n"], row["support_size"])
    parameter_count = row["p"] ** row["prefix_width"]
    avg = Fraction(total, parameter_count)
    assert parameter_count == row["parameter_count"]
    assert total == row["support_count"]
    assert fraction_text(avg) == row["average_fiber_size"]
    assert len(nonempty) == row["observed_fiber_count"]
    assert parameter_count - len(nonempty) == row["empty_parameter_count"]
    assert max(histogram) == row["max_fiber_size"]
    assert {str(k): v for k, v in sorted(histogram.items())} == row["fiber_size_histogram"]
    for r_text, ledger in row["collision_ledgers"].items():
        r = int(r_text)
        power_moment = sum(size**r * count for size, count in histogram.items())
        collision_count = sum(comb(size, r) * count for size, count in histogram.items() if size >= r)
        excess = Fraction(power_moment, 1) / (avg**r)
        assert power_moment == ledger["power_moment_sum"]
        assert collision_count == ledger["unordered_collision_count"]
        assert fraction_text(excess) == ledger["normalized_excess"]
        core_hist: Counter[int] = Counter()
        profile_hist: Counter[tuple[int, ...]] = Counter()
        tuple_count = 0
        for supports in nonempty.values():
            if len(supports) < r:
                continue
            for items in itertools.combinations(supports, r):
                tuple_count += 1
                core_hist[common_core(items)] += 1
                profile_hist[pair_profile(items)] += 1
        assert tuple_count == ledger["tuple_count_replayed"]
        assert {str(k): v for k, v in sorted(core_hist.items())} == ledger["common_core_histogram"]
        assert {
            ",".join(map(str, key)): value
            for key, value in sorted(profile_hist.items())
        } == ledger["pairwise_intersection_profile_histogram"]
        for tail in ledger["tail_bounds"]:
            T = tail["T"]
            tail_count = sum(
                1
                for values in fibers_all.values()
                if len(values) * parameter_count >= T * total
            )
            bound = excess / (T**r)
            assert tail_count == tail["tail_count"]
            assert fraction_text(bound) == tail["excess_over_T_power"]
            assert (Fraction(tail_count, 1) <= bound) == tail["tail_within_bound"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, default=DEFAULT_CERT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = json.loads(args.check.read_text())
    assert cert["theorem_problem_id"] == THEOREM_PROBLEM_ID
    assert cert["payload_sha256"] == payload_hash(cert)
    for row in cert["rows"]:
        check_row(row)
    result = {
        "status": STATUS,
        "result": "PASS",
        "certificate": args.check.as_posix(),
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "rows_checked": len(cert["rows"]),
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(
            "q2_heavy_fiber_fewness_check: "
            f"status={STATUS} result=PASS file={args.check.as_posix()}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
