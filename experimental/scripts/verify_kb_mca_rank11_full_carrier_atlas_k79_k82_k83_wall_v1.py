#!/usr/bin/env python3
"""Verify the compact K'=79..82 atlas packet and exact K'=83 route cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-full-carrier-atlas-k79-k82-k83-wall-v1/manifest.json"
MANIFEST_SHA256 = "b5ef760938b36d09877fcda1d87c597de4f553a193af0050c05ddf24bfda2523"
ATLAS_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k72_k73_v1.py"
ROWS = tuple(range(79, 83))
SOURCE_PINS = {
    "79": ("ce03af23683142272324ff89626d72ef4f876e40", "29f26c362ce70c3f2f7bd5a8e911baa2d6f3a72fb30bcd066fbe60a1c16eb4cb"),
    "80": ("58fc3109875e1acbe9032cb2b1d614dac7e03374", "90a2e102c402a5323aad41fba6f99f9965defd593f690b429993c459ee1ebba3"),
    "81": ("0f2b7a1c4e5dc58a2c18a7aec71e816b0aae2145", "0f55a47938c6ad528b68a212f7cb51237be84ad1309594a8c8c39dbcf9464525"),
    "82": ("583733740a63d106039b638e5c001e4287d40e79", "bef30d74e322c5ae37ad22c09fe8d7bf657b8a6f037cc1b6d9c2e14f5727c926"),
    "83_wall": ("60862e5d5feeecb0fd8717e1a7ac027791e726d3", "2df88cbc5fdbe8cffde25d064cf3e00e0a339857d34c0917ae2e5a58d3402c08"),
}


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


ATLAS = load_module("rank11_k72_k73_atlas_for_k79_k83", ATLAS_PATH)
BASE = ATLAS.BASE


def row_ceiling(kprime: int) -> int:
    m, n = 67472 + kprime, 1048576 + kprime
    chart = max(
        BASE.integral_core_offset_row(kprime, core)["chart"]
        for core in range(9, kprime)
    )
    marks = comb(n, 9) * chart
    kernel = BASE.refined_kernel_capacity(kprime)
    records = 274980728111260126
    return (
        records * 55 * comb(m, 11)
        - 55 * comb(n, 11)
        - 55 * kernel
        - marks
        - 1
    ) // records


def replay_wall83(expected: dict) -> dict[str, object]:
    kprime = 83
    q = kprime - 10
    defects = tuple(expected["defects"])
    m2, m3, m4, m5 = (q - value for value in defects)
    baseline = ATLAS.baseline_caps(kprime)
    left = BASE.carrier_base23_vector(
        kprime, baseline, defects[0], defects[1]
    )
    exact45, _, _ = BASE.carrier_exact45_rows(kprime, baseline)
    middle = next(
        vector
        for s4, s5, vector in exact45
        if (s4, s5) == defects[2:]
    )
    local = ATLAS.combine(left, middle)
    _, high = BASE.high_support_group(kprime, baseline)
    cases = ATLAS.mixed_cases(m2, m3 - m2, m4, m5)
    charges = cases[expected["label"]]
    require(charges == [(29, 6), (29, 6)], "wall charges")

    pairwise = local
    joint45 = None
    for union, dimension in charges:
        pairwise = ATLAS.combine(
            pairwise, ATLAS.fixed_union_cap(kprime, union, dimension)
        )
        coupled = ATLAS.joint45_weighted_cap(kprime, union, dimension)
        joint45 = coupled if joint45 is None else min(joint45, coupled)

    def premium(vector: tuple[int, ...]) -> int:
        caps = vector
        value = ATLAS.premium(caps)
        old45 = sum(
            ATLAS.WEIGHTS[support] * caps[support - 2]
            for support in (4, 5)
        )
        require(joint45 is not None, "joint charge")
        return value - old45 + min(old45, joint45)

    pairwise_maximum = max(
        premium(ATLAS.combine(pairwise, vector)) for _, vector in high
    )
    intersection_rows = []
    for overlap45 in range(4):
        union = 32 - overlap45
        triple = ATLAS.combine(
            pairwise, ATLAS.fixed_union_cap(kprime, union, 4)
        )
        maximum = max(
            premium(ATLAS.combine(triple, vector)) for _, vector in high
        )
        intersection_rows.append({
            "overlap45": overlap45,
            "triple_union": union,
            "triple_dimension": 4,
            "maximum": maximum,
            "margin": row_ceiling(kprime) - maximum,
        })

    branch_free = []
    for item in expected["branch_free_baseline"]:
        checkpoint = item["kprime"]
        caps = ATLAS.baseline_caps(checkpoint)
        value = ATLAS.premium(tuple(caps[s] for s in ATLAS.SUPPORTS))
        ceiling = row_ceiling(checkpoint)
        branch_free.append({
            "kprime": checkpoint,
            "baseline_premium": value,
            "safe_premium_ceiling": ceiling,
            "margin": ceiling - value,
        })

    return {
        "defects": list(defects),
        "completion_maxima": [m2, m3, m4, m5],
        "label": expected["label"],
        "pairwise_charges": [list(charge) for charge in charges],
        "pairwise_maximum": pairwise_maximum,
        "safe_premium_ceiling": row_ceiling(kprime),
        "pairwise_margin": row_ceiling(kprime) - pairwise_maximum,
        "forced_intersection_rows": intersection_rows,
        "branch_free_baseline": branch_free,
    }


def validate(data: object) -> dict[str, object]:
    require(isinstance(data, dict), "manifest object")
    require(
        data["schema"]
        == "kb-mca-rank11-full-carrier-atlas-k79-k82-k83-wall-v1",
        "schema",
    )
    require(
        data["exact_parent"] == "0b6cb72c025ddaafbddd92e3daf398e5993ef320",
        "parent",
    )
    require(
        data["previous_packet_sha256"]
        == "20dff5ce1c9634f9cd99e2cbacd4809fc860894f4549265a6f8b69176c0843c4",
        "previous packet",
    )
    source = data["source_prize_dag"]
    require(
        source["commit"] == "42ad09faf86b9a3624a361b2cc8d1a57f201501c",
        "source commit",
    )
    require(set(source["nodes"]) == set(SOURCE_PINS), "source nodes")
    for key, (tree, contract) in SOURCE_PINS.items():
        require(source["nodes"][key]["tree"] == tree, f"source tree {key}")
        require(
            source["nodes"][key]["contract_sha256"] == contract,
            f"source contract {key}",
        )
    require(data["record_floor"] == 274980728111260126, "record floor")
    require(set(data["rows"]) == {str(value) for value in ROWS}, "row set")

    results = {}
    for kprime in ROWS:
        row = data["rows"][str(kprime)]
        q, m, n = kprime - 10, 67472 + kprime, 1048576 + kprime
        require(
            (row["q"], row["m"], row["n"]) == (q, m, n),
            f"parameters {kprime}",
        )
        require(
            row["plain_evaluations"] > row["plain_unsafe_cells"] > 0,
            f"plain counts {kprime}",
        )
        require(
            re.fullmatch(r"[0-9a-f]{64}", row["unsafe_tuple_sha256"])
            is not None,
            f"tuple digest {kprime}",
        )
        require(
            row["unsafe_maximum"]
            >= row["unsafe_minimum"]
            > row["safe_premium_ceiling"],
            f"unsafe range {kprime}",
        )
        require(
            row["completion_premium"] + row["premium_ceiling_margin"]
            == row["safe_premium_ceiling"],
            f"premium margin {kprime}",
        )
        require(
            row["reroute_maximum"] + row["reroute_minimum_margin"]
            == row["safe_premium_ceiling"],
            f"reroute margin {kprime}",
        )
        require(
            row["reroute_evaluations"] >= row["plain_unsafe_cells"],
            f"reroute count {kprime}",
        )
        lanes = row["geometry_lanes"]
        require(
            [item["lane"] for item in lanes]
            == [
                "carrier32_geom", "one_geom", "two_geom", "three_geom",
                "four_geom", "five_geom", "six_geom",
            ],
            f"lane names {kprime}",
        )
        require(
            sum(item["evaluations"] for item in lanes)
            == row["geometry_total_evaluations"],
            f"lane count {kprime}",
        )
        require(
            max(item["maximum"] for item in lanes)
            < row["completion_premium"],
            f"lane safety {kprime}",
        )

        chart = max(
            BASE.integral_core_offset_row(kprime, core)["chart"]
            for core in range(9, kprime)
        )
        marks = comb(n, 9) * chart
        kernel = BASE.refined_kernel_capacity(kprime)
        records = data["record_floor"]
        full = (marks + records * row["completion_premium"]) // 55
        demand = records * comb(m, 11) - comb(n, 11)
        require(marks == row["rank_nine_marks"], f"marks {kprime}")
        require(kernel == row["kernel_capacity"], f"kernel {kprime}")
        require(full == row["full_rank_capacity"], f"full {kprime}")
        require(full + kernel == row["total_capacity"], f"total {kprime}")
        require(
            demand == row["required_component_incidence"], f"demand {kprime}"
        )
        require(
            demand - full - kernel == row["gap"] > 0, f"gap {kprime}"
        )
        require(
            row_ceiling(kprime) == row["safe_premium_ceiling"],
            f"ceiling {kprime}",
        )
        results[str(kprime)] = {
            "unsafe_cells": row["plain_unsafe_cells"],
            "gap": row["gap"],
        }

    wall = replay_wall83(data["wall83"])
    require(wall == data["wall83"], "wall replay")
    require(wall["pairwise_margin"] < 0, "wall sign")
    require(
        all(item["margin"] < 0 for item in wall["forced_intersection_rows"]),
        "intersection wall sign",
    )

    claims = data["claims"]
    require(claims["rank9_closed_rows"] == list(ROWS), "closed rows")
    require(claims["rank9_closed_prefix"] == [10, 82], "closed prefix")
    require(claims["rank9_remaining_interval"] == [83, 15528], "remaining")
    require(claims["first_pairwise_atlas_wall"] == 83, "wall row")
    require(
        not claims["chronology_owner"] and not claims["rank11_paid"],
        "rank eleven nonclaims",
    )
    require(
        claims["active_v4_ledger_movement"] == 0
        and not claims["KoalaBear_closed"],
        "global nonclaims",
    )
    results["wall83"] = {
        "deficit": -wall["pairwise_margin"],
        "intersection_rows": len(wall["forced_intersection_rows"]),
    }
    return results


def tamper_selftest(data: dict) -> int:
    mutations = (
        lambda item: item.__setitem__("exact_parent", "0" * 40),
        lambda item: item["source_prize_dag"]["nodes"]["79"].__setitem__(
            "tree", "0" * 40
        ),
        lambda item: item["rows"]["80"].__setitem__(
            "unsafe_tuple_sha256", "0" * 63
        ),
        lambda item: item["rows"]["81"].__setitem__(
            "premium_ceiling_margin", 0
        ),
        lambda item: item["rows"]["82"]["geometry_lanes"][0].__setitem__(
            "maximum", 10**100
        ),
        lambda item: item["wall83"].__setitem__("pairwise_margin", 1),
        lambda item: item["claims"].__setitem__(
            "rank9_closed_prefix", [10, 83]
        ),
        lambda item: item["claims"].__setitem__("KoalaBear_closed", True),
    )
    rejected = 0
    for mutate in mutations:
        trial = copy.deepcopy(data)
        mutate(trial)
        try:
            validate(trial)
        except (Reject, KeyError, TypeError, ValueError):
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
