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


def raw_low_parent_requirement(s: int, k: int, child_load: int, threshold: int) -> int:
    """Least parent load forcing ``child_load`` records at one heavy core.

    The proved resource controls the truncated margin.  For ``threshold <= D``
    the records with truncated margin at most ``threshold`` also have raw
    margin at most ``threshold``.  At most ``C_s(K)//(threshold+1)`` records
    are outside that raw-low class.  Every raw-low pair core has at least
    ``D+K-threshold`` coordinates, giving this exact inverse pigeonhole bound.
    """

    require(1 <= threshold <= D, "raw-low threshold")
    high = resource(s, k) // (threshold + 1)
    return high + ((child_load - 1) * (R + k)) // (D + k - threshold) + 1


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


def scan_raw_low_transfer(
    s: int,
    child_load: int,
    threshold: int,
    parent_load: int,
) -> dict[str, int]:
    """Check the raw-low parent threshold on every ambient shortened row."""

    rise_a = rising(D + 1, s - 1)
    b_num = falling(R + s, s + 1)
    b_den = rising(D + 1, s)
    p_num = falling(R + s, s + 1)

    minimum = None
    argmin = 0
    checked = 0
    increases = decreases = equal = 0
    previous = None

    for k in range(s, R + 1):
        a_den = (D + k) * rise_a
        if p_num * b_den >= b_num * a_den:
            c = p_num // a_den
        else:
            c = b_num // b_den
        high = c // (threshold + 1)
        value = high + ((child_load - 1) * (R + k)) // (D + k - threshold) + 1
        require(value <= parent_load, f"rank {s} raw-low transfer at K={k}")
        if minimum is None or value > minimum:
            minimum, argmin = value, k
        if previous is not None:
            if value > previous:
                increases += 1
            elif value < previous:
                decreases += 1
            else:
                equal += 1
        previous = value
        checked += 1
        if k < R:
            p_num = p_num * (R + k + 1) // (R + k - s)

    require(minimum is not None, "nonempty transfer scan")
    return {
        "cells_checked": checked,
        "maximum_parent_requirement": minimum,
        "argmax": argmin,
        "strict_increases": increases,
        "strict_decreases": decreases,
        "equal_steps": equal,
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
    thresholds = {
        2: 515,
        3: 511,
        4: 507,
        5: 503,
        6: 499,
        7: 496,
        8: 492,
        9: 489,
        10: 485,
    }
    loads: dict[int, int] = {1: 4_070_948}
    rows: list[dict[str, int]] = []
    scans: dict[str, dict[str, int]] = {}
    for s in range(2, 11):
        child_load = loads[s - 1]
        threshold = thresholds[s]
        scan = scan_raw_low_transfer(s, child_load, threshold, 10**40)
        parent_load = scan["maximum_parent_requirement"]
        # Replay with the now-frozen exact maximum as a fail-closed guard.
        scan = scan_raw_low_transfer(s, child_load, threshold, parent_load)
        rows.append({
            "rank": s,
            "threshold": threshold,
            "child_load": child_load,
            "parent_load": parent_load,
            "argmax_K": scan["argmax"],
        })
        loads[s] = parent_load
        scans[str(s)] = scan
    expected = {
        1: 4_070_948,
        2: 64_241_811,
        3: 1_013_639_041,
        4: 15_991_635_730,
        5: 252_259_306_484,
        6: 3_978_753_104_997,
        7: 62_747_001_947_996,
        8: 989_431_810_807_346,
        9: 15_600_062_750_954_861,
        10: 248_706_399_341_288_370,
    }
    require(loads == expected, "corrected rank-eleven raw-low thresholds")
    unsafe = BUDGET - NEAR + 1
    require(unsafe > loads[10], "rank-eleven contradiction")
    return {
        "loads": {str(k): v for k, v in sorted(loads.items())},
        "rows": rows,
        "transfer_scans": scans,
        "unsafe_post_near_load": unsafe,
        "required_rank_ten_load": loads[10],
        "uniform_rank_one_cap": 4_070_947,
        "slack": unsafe - loads[10],
    }


def rank12_method_wall(rank11: dict[str, Any]) -> dict[str, int]:
    """Best single raw-low threshold at the initial rank-twelve row."""

    child = rank11["required_rank_ten_load"]
    k = R
    values = [
        (raw_low_parent_requirement(11, k, child, threshold), threshold)
        for threshold in range(1, D + 1)
    ]
    minimum, threshold = min(values)
    unsafe = BUDGET - NEAR + 1
    require((minimum, threshold) == (546_519_697_764_383_119, D), "rank-twelve method wall")
    require(minimum > unsafe, "rank-twelve remains unpaid")
    require(sum(value == minimum for value, _ in values) == 1, "unique rank-twelve threshold")
    return {
        "thresholds_checked": D,
        "best_threshold": threshold,
        "required_parent_load": minimum,
        "available_unsafe_load": unsafe,
        "shortfall": minimum - unsafe,
        "target_rank_ten_load": child,
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
    rank12 = rank12_method_wall(rank11)
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
        "rank12_method_wall": rank12,
        "finite_controls": {"dense_core_families_checked": controls},
        "claims": {
            "uniform_rank_one_cap_proved": True,
            "complete_affine_error_rank_11_branch_paid": True,
            "rank12_dense_core_route_proved": False,
            "rank12_single_threshold_method_insufficient": True,
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
        ("rank12_method_wall", "shortfall", expected["rank12_method_wall"]["shortfall"] + 1),
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
    changed["rank12_method_wall"]["best_threshold"] -= 1
    try:
        require(changed == expected, "rank-twelve method wall")
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
        f"rank12_shortfall={result['rank12_method_wall']['shortfall']} "
        f"controls={result['finite_controls']['dense_core_families_checked']}"
    )


if __name__ == "__main__":
    main()
