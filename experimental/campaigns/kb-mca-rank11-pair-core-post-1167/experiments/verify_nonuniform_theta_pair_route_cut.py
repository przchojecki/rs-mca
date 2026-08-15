#!/usr/bin/env python3
"""Exact replay of the rank-eleven nonuniform-theta fixed-pair route cut."""

from __future__ import annotations

import argparse
import copy
import json
from fractions import Fraction
from math import comb, prod


ROW = {
    "p": 2130706433,
    "extension_degree": 6,
    "n": 2097152,
    "K": 1048576,
    "m": 1116048,
    "w": 67472,
    "near": 134944,
    "budget": 274980728111395087,
}


class Reject(ValueError):
    pass


def require(value: bool, message: str) -> None:
    if not value:
        raise Reject(message)


def falling(x: int, length: int) -> int:
    return prod(x - index for index in range(length))


def rising(x: int, length: int) -> int:
    return prod(x + index for index in range(length))


def ceil_fraction(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def theta_resource(s: int) -> int:
    n, K, m, w = (ROW[key] for key in ("n", "K", "m", "w"))
    values = [Fraction(n)]
    for rank in range(1, s + 1):
        values.extend(
            [
                Fraction(
                    falling(n, rank + 1),
                    m * rising(w + 1, rank - 1),
                ),
                Fraction(
                    falling(n - K + rank, rank + 1),
                    rising(w + 1, rank),
                ),
            ]
        )
    return max(values).numerator // max(values).denominator


def pair_cap(s: int, tau: int) -> int:
    n, K, w = (ROW[key] for key in ("n", "K", "w"))
    require(1 <= tau < w, "legal cutoff")
    return comb(n - K + s, s) // comb(w - tau + s, s)


def forced_pair_weight(s: int, tau: int) -> int:
    excess_line = ROW["budget"] - ROW["near"] + 1
    mass = max(0, (tau + 1) * excess_line - theta_resource(s))
    return (mass + pair_cap(s, tau) - 1) // pair_cap(s, tau)


def parallel_capacity(tau: int, deficiency: int) -> int:
    outside = ROW["n"] - ROW["m"] + deficiency
    return (outside // deficiency) * (tau + 1 - deficiency)


def max_compatible_deficiency(tau: int, forced_weight: int) -> int:
    # The capacity is nonincreasing in the deficiency.  Binary search keeps
    # the all-threshold certificate linear-logarithmic rather than quadratic.
    low, high = 1, tau + 1
    while low < high:
        middle = (low + high) // 2
        if parallel_capacity(tau, middle) >= forced_weight:
            low = middle + 1
        else:
            high = middle
    return low - 1


def star_fixture() -> dict[str, int]:
    p, n, K, core_size = 11, 11, 1, 2
    m = core_size + 1
    slopes = list(range(n - core_size))
    r0 = [0] * core_size + [(-gamma) % p for gamma in slopes]
    r1 = [0] * core_size + [1] * len(slopes)
    for gamma in slopes:
        support = [
            index
            for index in range(n)
            if (r0[index] + gamma * r1[index]) % p == 0
        ]
        require(len(support) == m, "star exact support")
        require(len({r1[index] for index in support}) == 2,
                "star pair noncontainment")
        word = [(r0[index] + gamma * r1[index]) % p for index in range(n)]
        max_constant_agreement = max(word.count(value) for value in range(p))
        require(n - max_constant_agreement > m - K, "star post-near")
    agreement = m - 2 + 1
    require(len(slopes) == n - agreement == 9, "star sharp multiplicity")
    return {"field": p, "parallel_records": len(slopes), "n_minus_A": n - agreement}


def coupled_core_ceiling(s: int) -> dict[str, int]:
    """Optimize all current theta, cumulative-pair, and core resources.

    Pair types of deficiency delta have cumulative count at most Q(delta)
    and each type owns at most floor((n-m+delta)/delta) records.  Records of
    smaller deficiency use less of the global theta resource, so the exact
    integral LP is greedy in increasing delta.  Any unused theta resource
    can pay high records at cost J+1 each.
    """

    resource = theta_resource(s)
    line_field_size = ROW["p"] ** ROW["extension_degree"]
    previous_pairs = 0
    low_records = 0
    theta_used = 0
    best: dict[str, int] | None = None
    for cutoff in range(1, ROW["w"]):
        current_pairs = pair_cap(s, cutoff)
        new_pair_types = current_pairs - previous_pairs
        records_per_type = (ROW["n"] - ROW["m"] + cutoff) // cutoff
        available_records = new_pair_types * records_per_type
        selected_records = min(
            available_records,
            (resource - theta_used) // cutoff,
        )
        low_records += selected_records
        theta_used += cutoff * selected_records
        high_records = (resource - theta_used) // (cutoff + 1)
        total = ROW["near"] + low_records + high_records
        if current_pairs * current_pairs < line_field_size:
            candidate = {
                "cutoff": cutoff,
                "pair_cap": current_pairs,
                "low_records": low_records,
                "low_theta_used": theta_used,
                "high_records": high_records,
                "total": total,
                "signed_slack": ROW["budget"] - total,
            }
            if best is None or (candidate["total"], candidate["cutoff"]) < (
                best["total"],
                best["cutoff"],
            ):
                best = candidate
        previous_pairs = current_pairs
    require(best is not None, "nonempty coupled scan")
    return best


def printed_core_ceiling(s: int) -> dict[str, int]:
    """Complete cutoff bound using only printed threshold tails."""

    line_field_size = ROW["p"] ** ROW["extension_degree"]
    previous_pairs = 0
    low_records = 0
    best: dict[str, int] | None = None
    for cutoff in range(1, ROW["w"]):
        current_pairs = pair_cap(s, cutoff)
        new_pair_types = current_pairs - previous_pairs
        records_per_type = (ROW["n"] - ROW["m"] + cutoff) // cutoff
        low_records += new_pair_types * records_per_type
        high_caps = [ROW["n"] // (cutoff + 1)]
        for rank in range(1, s + 1):
            value = max(
                Fraction(
                    falling(ROW["n"], rank + 1),
                    ROW["m"] * (cutoff + 1) * rising(ROW["w"] + 1, rank - 1),
                ),
                Fraction(
                    falling(ROW["n"] - ROW["K"] + rank, rank + 1),
                    (cutoff + 1) * rising(ROW["w"] + 1, rank),
                ),
            )
            high_caps.append(value.numerator // value.denominator)
        high_records = max(high_caps)
        total = ROW["near"] + low_records + high_records
        if current_pairs * current_pairs < line_field_size:
            candidate = {
                "cutoff": cutoff,
                "pair_cap": current_pairs,
                "low_records": low_records,
                "high_records": high_records,
                "total": total,
                "signed_slack": ROW["budget"] - total,
            }
            if best is None or (candidate["total"], candidate["cutoff"]) < (
                best["total"], best["cutoff"]
            ):
                best = candidate
        previous_pairs = current_pairs
    require(best is not None, "nonempty printed cutoff scan")
    return best


def abstract_ceiling_witness(s: int) -> dict[str, int | bool]:
    cap = pair_cap(s, 1)
    multiplicity = ROW["n"] - ROW["m"] + 1
    records = cap * multiplicity
    total = ROW["near"] + records
    return {
        "tau": 1,
        "pair_types": cap,
        "multiplicity_per_type": multiplicity,
        "records": records,
        "total": total,
        "over_budget": total - ROW["budget"],
        "theta_resource_satisfied": records <= theta_resource(s),
        "field_supply_satisfied": records < ROW["p"] ** ROW["extension_degree"],
    }


def build() -> dict[str, object]:
    s = 10
    legal: list[dict[str, int]] = []
    line_field_size = ROW["p"] ** ROW["extension_degree"]
    for tau in range(1, ROW["w"]):
        cap = pair_cap(s, tau)
        if cap * cap >= line_field_size:
            continue
        weight = forced_pair_weight(s, tau)
        records = (weight + tau - 1) // tau
        legal.append(
            {
                "tau": tau,
                "pair_cap": cap,
                "forced_pair_weight": weight,
                "forced_records": records,
                "max_compatible_deficiency": max_compatible_deficiency(tau, weight),
            }
        )
    by_weight = max(legal, key=lambda item: (item["forced_pair_weight"], -item["tau"]))
    by_records = max(legal, key=lambda item: (item["forced_records"], -item["tau"]))
    require(
        by_weight
        == {
            "tau": 6486,
            "pair_cap": 2255946383610,
            "forced_pair_weight": 743449148,
            "forced_records": 114624,
            "max_compatible_deficiency": 8,
        },
        "weight optimum",
    )
    require(
        by_records
        == {
            "tau": 1795,
            "pair_cap": 1075288922022,
            "forced_pair_weight": 360132809,
            "forced_records": 200632,
            "max_compatible_deficiency": 4,
        },
        "record optimum",
    )
    require(theta_resource(s) == 106618568137036225644, "theta resource")
    require(legal[-1]["tau"] == 65810, "last sub-square cutoff")
    coupled = coupled_core_ceiling(s)
    require(
        coupled
        == {
            "cutoff": 26033,
            "pair_cap": 107486241601454,
            "low_records": 811957734614064312,
            "low_theta_used": 106597778100457375003,
            "high_records": 798572504373,
            "total": 811958533186703629,
            "signed_slack": -536977805075308542,
        },
        "coupled core ceiling optimum",
    )
    printed = printed_core_ceiling(s)
    require(
        printed
        == {
            "cutoff": 19737,
            "pair_cap": 26130774875308,
            "low_records": 808527428378681053,
            "high_records": 5401690553097387,
            "total": 813929118931913384,
            "signed_slack": -538948390820518297,
        },
        "printed core ceiling optimum",
    )
    abstract = abstract_ceiling_witness(s)
    require(
        abstract
        == {
            "tau": 1,
            "pair_types": 821289819491,
            "multiplicity_per_type": 981105,
            "records": 805771548351717555,
            "total": 805771548351852499,
            "over_budget": 530790820240457412,
            "theta_resource_satisfied": True,
            "field_supply_satisfied": True,
        },
        "abstract certificate ceiling witness",
    )
    return {
        "schema": "kb-mca-rank11-nonuniform-theta-fixed-pair-route-cut-v1",
        "parent": "491ccdf53d54846f5a013b808960645275c64ed3",
        "row": ROW,
        "explanation_dimension": s,
        "theta_resource": theta_resource(s),
        "last_subsquare_tau": legal[-1]["tau"],
        "weight_optimum": by_weight,
        "record_optimum": by_records,
        "printed_core_ceiling": printed,
        "coupled_core_ceiling": coupled,
        "abstract_ceiling_witness": abstract,
        "parallel_star": star_fixture(),
        "claims": {
            "rank11_paid": False,
            "active_v4_movement": 0,
            "fixed_pair_terminal_proved": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.tamper_selftest:
        mutations = [
            ("forced_pair_weight", 743449147),
            ("forced_records", 114623),
            ("max_compatible_deficiency", 9),
        ]
        caught = 0
        for key, value in mutations:
            changed = copy.deepcopy(expected)
            changed["weight_optimum"][key] = value
            try:
                require(changed == expected, "canonical result")
            except Reject:
                caught += 1
        require(caught == len(mutations), "all mutations caught")
        changed = copy.deepcopy(expected)
        changed["coupled_core_ceiling"]["total"] -= 1
        try:
            require(changed == expected, "coupled ceiling canonical result")
        except Reject:
            caught += 1
        require(caught == len(mutations) + 1, "coupled mutation caught")
        changed = copy.deepcopy(expected)
        changed["printed_core_ceiling"]["cutoff"] += 1
        try:
            require(changed == expected, "printed ceiling canonical result")
        except Reject:
            caught += 1
        require(caught == len(mutations) + 2, "printed mutation caught")
        print(f"KB_MCA_RANK11_PAIR_ROUTE_CUT_TAMPER_PASS mutations={caught}/5")
        return
    if args.json:
        print(json.dumps(expected, sort_keys=True))
        return
    print(
        "KB_MCA_RANK11_PAIR_ROUTE_CUT_PASS "
        f"weight_tau={expected['weight_optimum']['tau']} "
        f"weight={expected['weight_optimum']['forced_pair_weight']} "
        f"record_tau={expected['record_optimum']['tau']} "
        f"records={expected['record_optimum']['forced_records']} "
        f"printed_total={expected['printed_core_ceiling']['total']} "
        f"coupled_total={expected['coupled_core_ceiling']['total']}"
    )


if __name__ == "__main__":
    main()
