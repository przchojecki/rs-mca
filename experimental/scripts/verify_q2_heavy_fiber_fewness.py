#!/usr/bin/env python3
"""Q2 heavy-fiber fewness ledger for exact toy prefix fibers.

Status: EXPERIMENTAL / AUDIT. This finite ledger records r=3 and r=4
collision tails for the Q2 heavy-fiber fewness object. It is exact CPU code and
does not claim the worst-case quotient-fiber equidistribution theorem.
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


STATUS = "EXPERIMENTAL"
THEOREM_PROBLEM_ID = "Q2 heavy-fiber fewness; cor:periodic-support-count"
SCHEMA_VERSION = "q2-heavy-fiber-fewness-v1"
DEFAULT_OUTPUT = Path(
    "experimental/data/certificates/q2-heavy-fiber-fewness/"
    "q2_heavy_fiber_fewness.json"
)
ROWS = (
    {"p": 97, "n": 16, "support_size": 8, "prefix_width": 2},
    {"p": 97, "n": 16, "support_size": 8, "prefix_width": 3},
    {"p": 257, "n": 16, "support_size": 8, "prefix_width": 2},
)
THRESHOLDS = (1, 2, 4, 8)


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
    if (p - 1) % order:
        raise ValueError("order must divide p-1")
    omega = pow(primitive_root(p), (p - 1) // order, p)
    values = tuple(pow(omega, i, p) for i in range(order))
    assert len(set(values)) == order
    return values


def locator_coeffs(roots: tuple[int, ...], p: int) -> tuple[int, ...]:
    coeffs = [1]
    for root in roots:
        nxt = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            nxt[i] = (nxt[i] - coeff * root) % p
            nxt[i + 1] = (nxt[i + 1] + coeff) % p
        coeffs = nxt
    return tuple(coeffs)


def prefix_key(domain: tuple[int, ...], support: tuple[int, ...],
               support_size: int, width: int, p: int) -> tuple[int, ...]:
    coeffs = locator_coeffs(tuple(domain[i] for i in support), p)
    assert len(coeffs) == support_size + 1 and coeffs[-1] == 1
    return tuple(coeffs[support_size - i] for i in range(1, width + 1))


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def payload_hash(payload: dict[str, Any]) -> str:
    clone = {key: value for key, value in payload.items() if key != "payload_sha256"}
    blob = json.dumps(clone, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def support_intersection_size(items: tuple[tuple[int, ...], ...]) -> int:
    common = set(items[0])
    for item in items[1:]:
        common.intersection_update(item)
    return len(common)


def pairwise_intersection_profile(items: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(
        sorted(
            len(set(a).intersection(b))
            for a, b in itertools.combinations(items, 2)
        )
    )


def fiber_map(p: int, n: int, support_size: int, prefix_width: int) -> dict[tuple[int, ...], list[tuple[int, ...]]]:
    domain = subgroup(p, n)
    fibers: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
    for support in itertools.combinations(range(n), support_size):
        fibers[prefix_key(domain, support, support_size, prefix_width, p)].append(support)
    return dict(fibers)


def row_payload(p: int, n: int, support_size: int, prefix_width: int) -> dict[str, Any]:
    fibers = fiber_map(p, n, support_size, prefix_width)
    total = comb(n, support_size)
    parameter_count = p**prefix_width
    avg = Fraction(total, parameter_count)
    histogram = Counter(len(values) for values in fibers.values())
    max_size = max(histogram)
    moment_rows: dict[str, Any] = {}
    for r in (3, 4):
        power_moment = sum(size**r * count for size, count in histogram.items())
        collision_count = sum(comb(size, r) * count for size, count in histogram.items() if size >= r)
        excess = Fraction(power_moment, 1) / (avg**r)
        tails = []
        for threshold in THRESHOLDS:
            tail_count = sum(
                count
                for size, count in histogram.items()
                if size * parameter_count >= threshold * total
            )
            bound = excess / (threshold**r)
            tails.append(
                {
                    "T": threshold,
                    "tail_count": tail_count,
                    "excess_over_T_power": fraction_text(bound),
                    "tail_within_bound": Fraction(tail_count, 1) <= bound,
                }
            )
        common_core_hist: Counter[int] = Counter()
        pair_profile_hist: Counter[tuple[int, ...]] = Counter()
        tuple_count = 0
        for supports in fibers.values():
            if len(supports) < r:
                continue
            for items in itertools.combinations(supports, r):
                tuple_count += 1
                common_core_hist[support_intersection_size(items)] += 1
                pair_profile_hist[pairwise_intersection_profile(items)] += 1
        moment_rows[str(r)] = {
            "power_moment_sum": power_moment,
            "normalized_excess": fraction_text(excess),
            "unordered_collision_count": collision_count,
            "tuple_count_replayed": tuple_count,
            "common_core_histogram": {str(k): v for k, v in sorted(common_core_hist.items())},
            "pairwise_intersection_profile_histogram": {
                ",".join(map(str, key)): value
                for key, value in sorted(pair_profile_hist.items())
            },
            "tail_bounds": tails,
        }
    largest = sorted(
        fibers.items(),
        key=lambda item: (-len(item[1]), item[0]),
    )[:5]
    return {
        "label": f"f{p}_mu{n}_m{support_size}_w{prefix_width}",
        "p": p,
        "q_gen": p,
        "q_line": p,
        "q_chal": p,
        "n": n,
        "support_size": support_size,
        "prefix_width": prefix_width,
        "parameter_count": parameter_count,
        "support_count": total,
        "average_fiber_size": fraction_text(avg),
        "observed_fiber_count": len(fibers),
        "empty_parameter_count": parameter_count - len(fibers),
        "max_fiber_size": max_size,
        "fiber_size_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "largest_fibers": [
            {
                "key": list(key),
                "size": len(values),
                "supports": [list(support) for support in values[:12]],
                "truncated": len(values) > 12,
            }
            for key, values in largest
        ],
        "collision_ledgers": moment_rows,
    }


def build_certificate() -> dict[str, Any]:
    rows = [row_payload(**row) for row in ROWS]
    named = []
    for row in rows:
        for r, ledger in row["collision_ledgers"].items():
            for tail in ledger["tail_bounds"]:
                if not tail["tail_within_bound"]:
                    named.append(
                        {
                            "row": row["label"],
                            "r": int(r),
                            "T": tail["T"],
                            "tail_count": tail["tail_count"],
                            "bound": tail["excess_over_T_power"],
                        }
                    )
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "proof_status": STATUS,
        "claim": "finite exact r=3,4 heavy-fiber tail ledger for top-prefix locator fibers",
        "non_claims": [
            "No worst-case quotient-fiber equidistribution theorem is claimed.",
            "No deployed-size tail bound is claimed.",
            "The packet is distinct from the r=2 prefix-collision ledger and aggregate Gamma_r moments.",
        ],
        "rows": rows,
        "named_over_bound_findings": named,
    }
    payload["payload_sha256"] = payload_hash(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--emit-defaults", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    else:
        print(
            "q2_heavy_fiber_fewness: "
            f"status={STATUS} result=PASS rows={len(cert['rows'])} "
            f"findings={len(cert['named_over_bound_findings'])}"
        )
        print(args.output.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
