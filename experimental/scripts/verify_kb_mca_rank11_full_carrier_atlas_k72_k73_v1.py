#!/usr/bin/env python3
"""Verify the supplemental K'=72,73 full-carrier-atlas certificate."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from functools import cache
from math import comb
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-full-carrier-atlas-k72-k73-v1/manifest.json"
MANIFEST_SHA256 = "4978f7b692bdee734e302b55c9c5597d1dc0d21674ab219b5a440b8718a41725"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
SUPPORTS = tuple(range(2, 10))
WEIGHTS = {support: comb(11 - support, 2) for support in SUPPORTS}


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"module {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BASE = load_module("rank11_split_pencil_base_for_full_atlas", BASE_PATH)


def baseline_caps(kprime: int) -> dict[int, int]:
    q = kprime - 10
    m = 67472 + kprime
    return {
        support: (
            BASE.completion_defect_row(
                q, m, support, {2: 7, 3: 2, 4: 1, 5: 0}[support]
            )["active_cap"]
            if support <= 5
            else BASE.universal_completion_row(q, m, support)["incidence_cap"]
        )
        for support in SUPPORTS
    }


def combine(*vectors) -> tuple[int, ...]:
    return tuple(min(items) for items in zip(*vectors))


def premium(caps) -> int:
    return sum(WEIGHTS[support] * caps[support - 2] for support in SUPPORTS)


@cache
def fixed_union_cap(kprime: int, union: int, dimension: int):
    return BASE.carrier_charged_vector(
        kprime, (10**500,) * len(SUPPORTS), union, dimension
    )


@cache
def joint45_weighted_cap(kprime: int, union: int, dimension: int) -> int:
    m = 67472 + kprime
    outside = m - union
    degree = kprime - 1 - union
    rank3_cap = degree - dimension + 4
    completion = rank3_cap - 3

    def lower(support: int) -> int:
        total = comb(union, support)
        for external in range(1, support):
            total += (
                comb(union, support - external)
                * comb(outside, external - 1)
                * completion
                // external
            )
        return total

    top4 = min(
        completion * comb(outside, 3) // 4,
        completion * comb(outside, 4) // (outside - rank3_cap),
    )
    top5 = (
        completion * comb(outside, 4)
        - (outside - rank3_cap) * top4
    ) // 5
    decrement = (outside - rank3_cap + 4) // 5
    require(
        WEIGHTS[4] * comb(m - 4, 7)
        >= WEIGHTS[5] * decrement * comb(m - 5, 6),
        "joint charge endpoint",
    )
    incidence4 = (lower(4) + top4) * comb(m - 4, 7)
    incidence5 = (lower(5) + top5) * comb(m - 5, 6)
    return WEIGHTS[4] * incidence4 + WEIGHTS[5] * incidence5


def mixed_cases(m2: int, offset3: int, m4: int, m5: int):
    b2 = m2 + 1
    b3 = m2 + offset3 + 2
    outside3 = offset3 + 1
    cases = {
        "T23": [(b2 + b3, 7)],
        "A23": [(b2 + b3 - 1, 8)],
    }

    def higher(support: int, maximum: int):
        if maximum <= 0:
            return {f"E{support}": []}
        carrier = maximum + support - 1
        rows = {
            f"T{support}": [(b2 + carrier, 10 - support)],
            f"A{support}": [(b2 + carrier - 1, 11 - support)],
        }
        if maximum <= m2:
            return rows
        offset = maximum - m2
        outside = support + offset - 2
        for overlap in range(min(outside3, offset) + 1):
            union = b2 + outside3 + outside - overlap
            dimension = 11 - support if overlap >= 1 else 10 - support
            rows[f"N{support}_t{overlap}"] = [(union, dimension)]
        return rows

    for name4, charges4 in higher(4, m4).items():
        for name5, charges5 in higher(5, m5).items():
            cases[f"F23__{name4}__{name5}"] = charges4 + charges5
    return cases


def charged_rows(kprime: int, local: tuple[int, ...], cases: dict):
    rows = {}
    for name, charges in cases.items():
        candidate = local
        joint = None
        for union, dimension in charges:
            candidate = combine(candidate, fixed_union_cap(kprime, union, dimension))
            if dimension >= 5:
                coupled = joint45_weighted_cap(kprime, union, dimension)
                joint = coupled if joint is None else min(joint, coupled)
        rows.setdefault((candidate, joint), name)
    return rows


def reroute_row(kprime: int, defects_list) -> dict[str, Any]:
    q = kprime - 10
    baseline = baseline_caps(kprime)
    exact45, _, _ = BASE.carrier_exact45_rows(kprime, baseline)
    middle_by_defects = {(a, b): vector for a, b, vector in exact45}
    _, high = BASE.high_support_group(kprime, baseline)
    maximum = (-1, (), "")
    evaluations = 0
    margins = []
    for defects in defects_list:
        s2, s3, s4, s5 = defects
        m2, m3, m4, m5 = (q - value for value in defects)
        left = BASE.carrier_base23_vector(kprime, baseline, s2, s3)
        local = combine(left, middle_by_defects[(s4, s5)])
        cases = mixed_cases(m2, m3 - m2, m4, m5)
        cell_maximum = (-1, "")
        for (candidate, joint), name in charged_rows(kprime, local, cases).items():
            for high_name, high_vector in high:
                evaluations += 1
                caps = combine(candidate, high_vector)
                value = premium(caps)
                if joint is not None:
                    old45 = sum(
                        WEIGHTS[support] * caps[support - 2]
                        for support in (4, 5)
                    )
                    value -= old45 - min(old45, joint)
                cell_maximum = max(cell_maximum, (value, f"{name}/{high_name}"))
        margins.append(cell_maximum[0])
        maximum = max(maximum, (cell_maximum[0], tuple(defects), cell_maximum[1]))
    return {
        "evaluations": evaluations,
        "maximum": maximum[0],
        "active_defects": maximum[1],
        "active_geometry": maximum[2],
        "cell_maxima": margins,
    }


def active_safe_premium(kprime: int, defects) -> int:
    baseline = baseline_caps(kprime)
    s2, s3, s4, s5 = defects
    left = BASE.carrier_base23_vector(kprime, baseline, s2, s3)
    exact45, _, _ = BASE.carrier_exact45_rows(kprime, baseline)
    middle = next(
        vector for a, b, vector in exact45 if (a, b) == (s4, s5)
    )
    _, high = BASE.high_support_group(kprime, baseline)
    right = next(
        vector for label, vector in high if label == "c6F/c7F/c8F/c9F"
    )
    return premium(combine(left, middle, right))


def validate(data: object, replay: bool = True) -> dict[str, Any]:
    require(isinstance(data, dict), "manifest object")
    require(data["schema"] == "kb-mca-rank11-full-carrier-atlas-k72-k73-v1", "schema")
    require(data["exact_parent"] == "1ca90d4c570e3630b62c4cca084549282f1d7418", "parent")
    require(len(data["source_prize_dag"]["nodes"]) == 4, "source node count")
    require(data["record_floor"] == 274980728111260126, "record floor")
    results = {}
    for kprime in (72, 73):
        row = data["rows"][str(kprime)]
        q = kprime - 10
        require((row["q"], row["m"], row["n"]) == (q, 67472 + kprime, 1048576 + kprime), "row parameters")
        defects = [tuple(values) for values in row["unsafe_defect_tuples"]]
        require(len(defects) == row["plain_unsafe_cells"], "unsafe count")
        require(len(set(defects)) == len(defects), "unsafe uniqueness")
        require(all(q - values[1] > q - values[0] > 0 for values in defects), "positive offset")
        require(active_safe_premium(kprime, row["safe_maximum_defects"]) == row["completion_premium"], "safe premium")
        require(row["completion_premium"] + row["premium_ceiling_margin"] == row["safe_premium_ceiling"], "premium margin")
        require(len(row["geometry_lanes"]) == 7, "geometry lanes")
        require(all(lane["maximum"] < row["completion_premium"] for lane in row["geometry_lanes"]), "geometry maxima")
        if replay:
            routed = reroute_row(kprime, defects)
            require(routed["evaluations"] == row["reroute_evaluations"], "reroute evaluations")
            require(routed["maximum"] == row["reroute_maximum"], "reroute maximum")
            require(
                tuple(row["reroute_active_defects"]) in defects,
                "source active defects",
            )
            require(all(value < row["safe_premium_ceiling"] for value in routed["cell_maxima"]), "reroute safety")
        core_rows = {
            core: BASE.integral_core_offset_row(kprime, core)["chart"]
            for core in range(9, kprime)
        }
        marks = comb(row["n"], 9) * max(core_rows.values())
        kernel = BASE.refined_kernel_capacity(kprime)
        records = data["record_floor"]
        full = (marks + records * row["completion_premium"]) // 55
        demand = records * comb(row["m"], 11) - comb(row["n"], 11)
        ceiling = (
            records * 55 * comb(row["m"], 11)
            - 55 * comb(row["n"], 11)
            - 55 * kernel
            - marks
            - 1
        ) // records
        require(marks == row["rank_nine_marks"], "marks")
        require(kernel == row["kernel_capacity"], "kernel")
        require(full == row["full_rank_capacity"], "full capacity")
        require(full + kernel == row["total_capacity"], "total capacity")
        require(demand == row["required_component_incidence"], "demand")
        require(demand - full - kernel == row["gap"] > 0, "positive gap")
        require(ceiling == row["safe_premium_ceiling"], "ceiling")
        results[str(kprime)] = {"unsafe_cells": len(defects), "gap": row["gap"]}
    require(data["claims"]["rank9_closed_prefix"] == [10, 73], "closed prefix")
    require(data["claims"]["rank9_remaining_interval"] == [74, 15528], "remaining interval")
    require(not data["claims"]["rank11_paid"] and not data["claims"]["KoalaBear_closed"], "nonclaims")
    return results


def tamper_selftest(data: dict) -> int:
    mutations = (
        lambda item: item.__setitem__("exact_parent", "0" * 40),
        lambda item: item["source_prize_dag"]["nodes"].pop(next(iter(item["source_prize_dag"]["nodes"]))),
        lambda item: item["rows"]["72"]["unsafe_defect_tuples"].pop(),
        lambda item: item["rows"]["73"].__setitem__("completion_premium", item["rows"]["73"]["completion_premium"] + 1),
        lambda item: item["rows"]["72"].__setitem__("gap", -1),
        lambda item: item["claims"].__setitem__("KoalaBear_closed", True),
    )
    rejected = 0
    for mutate in mutations:
        trial = copy.deepcopy(data)
        mutate(trial)
        try:
            validate(trial, replay=False)
        except (Reject, KeyError, TypeError, ValueError, StopIteration):
            rejected += 1
    require(rejected == len(mutations), "tamper rejection")
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    raw = MANIFEST.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA256, "manifest hash")
    data = json.loads(raw)
    result = validate(data)
    result["manifest_sha256"] = MANIFEST_SHA256
    if args.tamper_selftest:
        result["tamper_rejected"] = tamper_selftest(data)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Reject as exc:
        print(f"REJECT: {exc}", file=sys.stderr)
        raise SystemExit(1)
