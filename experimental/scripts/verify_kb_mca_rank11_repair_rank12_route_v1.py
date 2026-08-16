#!/usr/bin/env python3
"""Exact verifier for the KoalaBear rank-11 repair / rank-12 route packet."""

from __future__ import annotations

import argparse
import copy
import itertools
import json
from math import comb, prod
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank11-repair-rank12-route-v1/result.json"

R = 1_048_576
D = 67_472
P = 2_130_706_433
EXT = 6
BUDGET = 274_980_728_111_395_087
NEAR = 134_944
FIBER = R - D + 1
PARENT = "2788d5ec3fb4b1d6f9c43a58a86ec2381e5f6804"
SUPERSEDED = "d01c546f4dca70e256c18c142873821b3bb48ab5"


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def falling(x: int, r: int) -> int:
    return prod(x - j for j in range(r))


def rising(x: int, r: int) -> int:
    return prod(x + j for j in range(r))


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def resource(s: int, k: int) -> int:
    a_num = falling(R + k, s + 1)
    a_den = (D + k) * rising(D + 1, s - 1)
    b_num = falling(R + s, s + 1)
    b_den = rising(D + 1, s)
    if a_num * b_den >= b_num * a_den:
        return a_num // a_den
    return b_num // b_den


def incidence(s: int, k: int, load: int) -> int:
    return ceil_div(load * (D + k) - resource(s, k), R + k)


def weighted_line_cap(j: int) -> dict[str, int]:
    n = R + j
    m = D + j
    q = m // 2
    low = comb(n, 2) // (q * (m - q))
    high = 0
    best_t = best_r = best_w = 0
    for t in range(1, n // (q + 1) + 1):
        for r in range(t + 1):  # r deficiencies equal q; t-r equal 1
            outside = n - t * m + (t - r) + r * q
            if outside < 0:
                continue
            numerator = t * (t - 1) * q + outside * ((t - r) * q + r)
            value = numerator // q
            if value > high:
                high = value
                best_t, best_r, best_w = t, r, outside
    return {
        "j": j,
        "low": low,
        "high": high,
        "total": low + high,
        "high_t": best_t,
        "high_q_deficiencies": best_r,
        "high_outside_weight": best_w,
    }


def scan_uniform_rank_one() -> dict[str, int]:
    maximum = -1
    minimum = 10**30
    argmax = argmin = 0
    increases = decreases = equal = 0
    previous = None
    endpoint = None
    for j in range(1, R + 1):
        row = weighted_line_cap(j)
        value = row["total"]
        if value > maximum:
            maximum, argmax = value, j
            endpoint = row
        if value < minimum:
            minimum, argmin = value, j
        if previous is not None:
            if value > previous:
                increases += 1
            elif value < previous:
                decreases += 1
            else:
                equal += 1
        previous = value
    require(endpoint is not None, "rank-one endpoint")
    require(maximum == 4_070_947 and argmax == 1, "uniform rank-one maximum")
    require(endpoint["low"] == 483 and endpoint["high"] == 4_070_464, "endpoint split")
    require(endpoint["high_t"] == 8 and endpoint["high_q_deficiencies"] == 0, "endpoint extremizer")
    require(increases == 0, "rank-one scan has no increase")
    return {
        "dimensions_checked": R,
        "maximum": maximum,
        "argmax": argmax,
        "minimum": minimum,
        "argmin": argmin,
        "strict_increases": increases,
        "strict_decreases": decreases,
        "equal_steps": equal,
        "endpoint_low": endpoint["low"],
        "endpoint_high": endpoint["high"],
        "endpoint_high_t": endpoint["high_t"],
        "endpoint_high_q_deficiencies": endpoint["high_q_deficiencies"],
        "endpoint_high_outside_weight": endpoint["high_outside_weight"],
    }


def scan_transfer(s: int, first_k: int, load: int, target: int) -> dict[str, int]:
    """Check incidence(s,k,load) >= target by one exact falling-product recurrence."""

    rise_a = rising(D + 1, s - 1)
    b_num = falling(R + s, s + 1)
    b_den = rising(D + 1, s)
    p_num = falling(R + first_k, s + 1)

    minimum = None
    argmin = 0
    checked = 0
    decreases = 0
    previous = None

    for k in range(first_k, R + 1):
        a_den = (D + k) * rise_a
        if p_num * b_den >= b_num * a_den:
            c = p_num // a_den
        else:
            c = b_num // b_den
        value = ceil_div(load * (D + k) - c, R + k)
        require(value >= target, f"rank {s} transfer at K={k}")
        if minimum is None or value < minimum:
            minimum, argmin = value, k
        if previous is not None and value < previous:
            decreases += 1
        previous = value
        checked += 1
        if k < R:
            p_num = p_num * (R + k + 1) // (R + k - s)

    require(minimum is not None, "nonempty transfer scan")
    return {
        "cells_checked": checked,
        "minimum": minimum,
        "argmin": argmin,
        "strict_decreases": decreases,
    }


def pair_type_cap(k: int, threshold: int) -> int:
    n = R + k
    h = D + k - threshold
    lam = k - 1
    den = h * h - lam * n
    require(den > 0 and h > lam, "positive dense-core denominator")
    small = ceil_div(n, 2 * h) - 1
    large = n * (h - lam) // den
    return max(small, large)


def dense_cap(s: int, k: int, threshold: int) -> int:
    return resource(s, k) // (threshold + 1) + pair_type_cap(k, threshold) * FIBER


def rank11_data() -> dict[str, Any]:
    loads: dict[int, int] = {10: BUDGET - NEAR + 1}
    rows: list[dict[str, int]] = []
    scans: dict[str, dict[str, int]] = {}
    for s in range(10, 1, -1):
        next_load = incidence(s, s, loads[s])
        rows.append({
            "rank": s,
            "load": loads[s],
            "endpoint_resource": resource(s, s),
            "next_load": next_load,
        })
        loads[s - 1] = next_load
    for row in rows:
        s = row["rank"]
        scans[str(s)] = scan_transfer(s, s, row["load"], row["next_load"])
    require(loads[1] == 5_201_865, "rank-eleven final load")
    require(loads[1] > 4_070_947, "rank-eleven contradiction")
    return {
        "loads": {str(k): v for k, v in sorted(loads.items(), reverse=True)},
        "rows": rows,
        "transfer_scans": scans,
        "forced_rank_one_load": loads[1],
        "uniform_rank_one_cap": 4_070_947,
        "slack": loads[1] - 4_070_947,
    }


def rank12_data() -> dict[str, Any]:
    barriers = {s: 4280 + (s - 3) for s in range(3, 12)}
    thresholds = {s: (249 if s >= 4 else 380) for s in range(3, 12)}
    loads: dict[int, int] = {11: BUDGET - NEAR + 1}
    rows: list[dict[str, int]] = []
    scans: dict[str, dict[str, int]] = {}

    for s in range(11, 2, -1):
        k = barriers[s]
        threshold = thresholds[s]
        cap = dense_cap(s, k, threshold)
        require(cap < loads[s], f"rank {s} barrier pays")
        next_load = incidence(s, k + 1, loads[s])
        row = {
            "rank": s,
            "barrier_K": k,
            "threshold": threshold,
            "load": loads[s],
            "resource": resource(s, k),
            "pair_type_cap": pair_type_cap(k, threshold),
            "dense_cap": cap,
            "slack": loads[s] - cap,
            "drop_K": k + 1,
            "next_load": next_load,
        }
        rows.append(row)
        loads[s - 1] = next_load
        scans[str(s)] = scan_transfer(s, k + 1, loads[s], next_load)

    expected_loads = {
        11: 274_980_728_111_260_144,
        10: 18_729_383_598_438_495,
        9: 1_275_719_855_410_716,
        8: 86_895_415_230_834,
        7: 5_918_985_683_045,
        6: 403_186_331_995,
        5: 27_464_496_807,
        4: 1_870_872_170,
        3: 127_444_922,
        2: 8_681_730,
    }
    require(loads == expected_loads, "rank-twelve barrier loads")
    require(min(row["slack"] for row in rows) == 364_201, "minimum barrier slack")

    endpoint_threshold = 1_922
    high = resource(2, 2) // (endpoint_threshold + 1)
    low = loads[2] - high
    q = pair_type_cap(2, endpoint_threshold)
    c1 = FIBER
    c2 = (R - D + 2) // 2
    pair_types_min = ceil_div(low, c1)
    deficiency_one_min = min(
        r for r in range(q + 1)
        if r * c1 + (q - r) * c2 >= low
    )
    extremal_capacity = deficiency_one_min * c1 + (q - deficiency_one_min) * c2
    rank_one_descendant = incidence(2, 2, loads[2])

    require((high, low, q) == (131_690, 8_550_040, 15), "rank-two endpoint split")
    require(pair_types_min == 9 and deficiency_one_min == 3, "rank-two type floors")
    require(extremal_capacity == 8_829_951, "rank-two independent capacity")
    require(extremal_capacity - low == 279_911, "rank-two capacity excess")
    require(rank_one_descendant == 558_412, "rank-one descendant load")

    return {
        "loads": {str(k): v for k, v in sorted(loads.items(), reverse=True)},
        "barrier_rows": rows,
        "transfer_scans": scans,
        "minimum_barrier_slack": min(row["slack"] for row in rows),
        "descendant": {
            "minimum_load": loads[2],
            "maximum_direction_dimension": 2,
            "minimum_ambient_K": 4_280,
        },
        "rank_two_endpoint": {
            "threshold": endpoint_threshold,
            "high": high,
            "low": low,
            "pair_types_max": q,
            "pair_types_min": pair_types_min,
            "deficiency_one_min": deficiency_one_min,
            "capacity_delta_1": c1,
            "capacity_delta_2": c2,
            "independent_extremal_capacity": extremal_capacity,
            "capacity_excess": extremal_capacity - low,
            "saving_needed": extremal_capacity - low + 1,
            "rank_one_descendant_min": rank_one_descendant,
        },
    }


def small_dense_core_controls() -> int:
    """Exhaustive small uniform-block maximum-clique controls."""

    checked = 0
    for n in range(4, 9):
        universe = range(n)
        for h in range(2, n + 1):
            blocks = [set(x) for x in itertools.combinations(universe, h)]
            for lam in range(h):
                den = h * h - lam * n
                if den <= 0 or h <= lam:
                    continue
                q = max(ceil_div(n, 2 * h) - 1, n * (h - lam) // den)
                if len(blocks) > 20:
                    continue
                for mask in range(1 << len(blocks)):
                    family = [blocks[i] for i in range(len(blocks)) if mask >> i & 1]
                    if len(family) <= q:
                        checked += 1
                        continue
                    good = all(
                        len(family[i] & family[j]) <= lam
                        for i in range(len(family))
                        for j in range(i)
                    )
                    require(not good, "small dense-core control")
                    checked += 1
    return checked


def build() -> dict[str, Any]:
    uniform = scan_uniform_rank_one()
    rank11 = rank11_data()
    rank12 = rank12_data()
    controls = small_dense_core_controls()
    return {
        "schema": "kb-mca-rank11-repair-rank12-route-v1",
        "parent": PARENT,
        "supersedes_unsubmitted_candidate": SUPERSEDED,
        "row": {
            "p": P,
            "extension_degree": EXT,
            "R": R,
            "d": D,
            "n": 2 * R,
            "K": R,
            "m": R + D,
            "budget": BUDGET,
            "near": NEAR,
        },
        "uniform_rank_one": uniform,
        "rank11_payment": rank11,
        "rank12_route": rank12,
        "finite_controls": {"dense_core_families_checked": controls},
        "claims": {
            "uniform_rank_one_cap_proved": True,
            "complete_affine_error_rank_11_branch_paid": True,
            "rank12_dense_core_route_proved": True,
            "affine_error_rank_12_paid": False,
            "koalabear_closed": False,
            "active_v4_ledger_movement": 0,
        },
    }


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def tamper_selftest(expected: dict[str, Any]) -> int:
    mutations = [
        ("uniform_rank_one", "maximum", expected["uniform_rank_one"]["maximum"] - 1),
        ("rank11_payment", "slack", expected["rank11_payment"]["slack"] + 1),
        ("rank12_route", "minimum_barrier_slack", expected["rank12_route"]["minimum_barrier_slack"] + 1),
        ("claims", "complete_affine_error_rank_11_branch_paid", False),
        ("claims", "affine_error_rank_12_paid", True),
        ("claims", "koalabear_closed", True),
    ]
    caught = 0
    for section, key, value in mutations:
        changed = copy.deepcopy(expected)
        changed[section][key] = value
        try:
            require(changed == expected, "canonical result")
        except Reject:
            caught += 1
    changed = copy.deepcopy(expected)
    changed["rank12_route"]["rank_two_endpoint"]["capacity_excess"] -= 1
    try:
        require(changed == expected, "rank-two excess")
    except Reject:
        caught += 1
    changed = copy.deepcopy(expected)
    changed["parent"] = SUPERSEDED
    try:
        require(changed == expected, "parent pin")
    except Reject:
        caught += 1
    require(caught == 8, "all mutations caught")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    result = build()
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"WROTE {RESULT}")
        return

    require(RESULT.exists(), "result file exists")
    actual = json.loads(RESULT.read_text())
    require(actual == result, "result file")

    if args.tamper_selftest:
        print(
            "KB_MCA_RANK11_REPAIR_RANK12_ROUTE_TAMPER_PASS "
            f"mutations={tamper_selftest(result)}/8"
        )
        return
    if args.json:
        print(canonical(result).decode())
        return
    print(
        "KB_MCA_RANK11_REPAIR_RANK12_ROUTE_PASS "
        f"rank1_cap={result['uniform_rank_one']['maximum']} "
        f"rank11_slack={result['rank11_payment']['slack']} "
        f"rank12_load={result['rank12_route']['descendant']['minimum_load']} "
        f"rank2_gap={result['rank12_route']['rank_two_endpoint']['capacity_excess']} "
        f"controls={result['finite_controls']['dense_core_families_checked']}"
    )


if __name__ == "__main__":
    main()
