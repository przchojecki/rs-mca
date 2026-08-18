#!/usr/bin/env python3
"""Independent arithmetic audit of the K'=72,73 carrier-atlas packet."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-full-carrier-atlas-k72-k73-v1/manifest.json"
EXPECTED_SHA256 = "4978f7b692bdee734e302b55c9c5597d1dc0d21674ab219b5a440b8718a41725"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
WEIGHTS = {support: comb(11 - support, 2) for support in range(2, 10)}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


raw = MANIFEST.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
data = json.loads(raw)
base = load_module("rank11_split_pencil_base_for_independent_atlas", BASE_PATH)


def baseline(kprime: int):
    q = kprime - 10
    m = 67472 + kprime
    return {
        d: (
            base.completion_defect_row(q, m, d, {2: 7, 3: 2, 4: 1, 5: 0}[d])["active_cap"]
            if d <= 5
            else base.universal_completion_row(q, m, d)["incidence_cap"]
        )
        for d in range(2, 10)
    }


def meet(*vectors):
    return tuple(min(values) for values in zip(*vectors))


def flat_vector(kprime: int, union: int, dimension: int):
    return tuple(
        base.multicarrier_collision_cap(kprime, 67472 + kprime, union, dimension, d)
        if dimension + 1 > d
        else 10**500
        for d in range(2, 10)
    )


def joint_charge(kprime: int, union: int, dimension: int):
    m = 67472 + kprime
    outside = m - union
    residual = kprime - union - dimension
    rank3 = residual + 3

    def lower(d):
        return comb(union, d) + sum(
            comb(union, d - j) * comb(outside, j - 1) * residual // j
            for j in range(1, d)
        )

    x4 = min(
        residual * comb(outside, 3) // 4,
        residual * comb(outside, 4) // (outside - rank3),
    )
    x5 = (residual * comb(outside, 4) - (outside - rank3) * x4) // 5
    return (
        21 * (lower(4) + x4) * comb(m - 4, 7)
        + 15 * (lower(5) + x5) * comb(m - 5, 6)
    )


def atlas(m2: int, offset3: int, m4: int, m5: int):
    b2 = m2 + 1
    out3 = offset3 + 1
    b3 = b2 + out3
    answer = {"T23": [(b2 + b3, 7)], "A23": [(b2 + b3 - 1, 8)]}

    def positions(d, maximum):
        if maximum <= 0:
            return {f"E{d}": []}
        carrier = maximum + d - 1
        rows = {f"T{d}": [(b2 + carrier, 10 - d)], f"A{d}": [(b2 + carrier - 1, 11 - d)]}
        if maximum > m2:
            offset = maximum - m2
            outside = d + offset - 2
            for overlap in range(min(out3, offset) + 1):
                rows[f"N{d}_t{overlap}"] = [
                    (b2 + out3 + outside - overlap, 11 - d if overlap else 10 - d)
                ]
        return rows

    for n4, c4 in positions(4, m4).items():
        for n5, c5 in positions(5, m5).items():
            answer[f"F23__{n4}__{n5}"] = c4 + c5
    return answer


checks = 0
for kprime in (72, 73):
    row = data["rows"][str(kprime)]
    q = kprime - 10
    caps0 = baseline(kprime)
    exact45, _, _ = base.carrier_exact45_rows(kprime, caps0)
    middle = {(a, b): vector for a, b, vector in exact45}
    _, high = base.high_support_group(kprime, caps0)
    global_maximum = (-1, (), "")
    evaluations = 0
    for defects in row["unsafe_defect_tuples"]:
        s2, s3, s4, s5 = defects
        m2, m3, m4, m5 = (q - value for value in defects)
        local = meet(
            base.carrier_base23_vector(kprime, caps0, s2, s3),
            middle[(s4, s5)],
        )
        charges = {}
        for name, fixed in atlas(m2, m3 - m2, m4, m5).items():
            candidate = local
            joint = None
            for union, dimension in fixed:
                candidate = meet(candidate, flat_vector(kprime, union, dimension))
                if dimension >= 5:
                    value = joint_charge(kprime, union, dimension)
                    joint = value if joint is None else min(joint, value)
            charges.setdefault((candidate, joint), name)
        cell = (-1, "")
        for (candidate, joint), name in charges.items():
            for high_name, high_vector in high:
                vector = meet(candidate, high_vector)
                value = sum(WEIGHTS[d] * vector[d - 2] for d in range(2, 10))
                if joint is not None:
                    old = 21 * vector[2] + 15 * vector[3]
                    value -= old - min(old, joint)
                cell = max(cell, (value, f"{name}/{high_name}"))
                evaluations += 1
        global_maximum = max(global_maximum, (cell[0], tuple(defects), cell[1]))
        assert cell[0] < row["safe_premium_ceiling"]
        checks += 1
    assert evaluations == row["reroute_evaluations"]
    assert global_maximum[0] == row["reroute_maximum"]
    assert tuple(row["reroute_active_defects"]) in {
        tuple(values) for values in row["unsafe_defect_tuples"]
    }
    records = data["record_floor"]
    full = (row["rank_nine_marks"] + records * row["completion_premium"]) // 55
    demand = records * comb(row["m"], 11) - comb(row["n"], 11)
    assert full == row["full_rank_capacity"]
    assert demand - full - row["kernel_capacity"] == row["gap"] > 0

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "rerouted_cells": checks,
    "reroute_evaluations": sum(data["rows"][str(k)]["reroute_evaluations"] for k in (72, 73)),
    "closed_prefix": data["claims"]["rank9_closed_prefix"],
}, sort_keys=True))
