#!/usr/bin/env python3
"""Verify the compact K'=74..78 full-carrier-atlas certificate."""

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
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-full-carrier-atlas-k74-k78-v1/manifest.json"
MANIFEST_SHA256 = "20dff5ce1c9634f9cd99e2cbacd4809fc860894f4549265a6f8b69176c0843c4"
ATLAS_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k72_k73_v1.py"
ROWS = tuple(range(74, 79))
SOURCE_PINS = {
    "74": ("7147009ffc0bc3ef5a5f0acbb794d019a8571baf", "7800a9e860586e1d05ab283c76405c6f53f1c4dd8a84275f451f058df6132e43"),
    "75": ("fcfbf1f1676728ffe32babd351f2c58923c70cb3", "ebab9ef2d31d53d4f826e88bd65107b8b0ea8b495285037a9ec3db94fbbf2231"),
    "76": ("92be39613893dfe29f4592bfc145274226b4b1b4", "73e786205127e30c03437231c90b89c9192bcfa4820204a36ad97e465e5f1b1a"),
    "77": ("411e6daf6822ad5138346a41d48aab19870d5b00", "f7d35e9aae271f6b8a885148b04a73e29b7a7f3074cce5641fd6e64b627e906b"),
    "78": ("0c3e8fc8ffe6ef478c1b0548c39440890efe6663", "cfc78701bda81ac3928a6750e39b2b3c7baceb59ec05a2de35e58f0debd9ad9b"),
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


ATLAS = load_module("rank11_k72_k73_atlas_for_k74_k78", ATLAS_PATH)


def validate(data: object) -> dict[str, object]:
    require(isinstance(data, dict), "manifest object")
    require(data["schema"] == "kb-mca-rank11-full-carrier-atlas-k74-k78-v1", "schema")
    require(data["exact_parent"] == "5d3cda9475b03777c488e35ab152231bd338da71", "parent")
    require(data["previous_packet_sha256"] == "4978f7b692bdee734e302b55c9c5597d1dc0d21674ab219b5a440b8718a41725", "previous packet")
    source = data["source_prize_dag"]
    require(source["commit"] == "9526b45dccc343a8070c86aaa45a23f1f499e7e0", "source commit")
    require(set(source["nodes"]) == set(SOURCE_PINS), "source rows")
    for key, (tree, contract) in SOURCE_PINS.items():
        require(source["nodes"][key]["tree"] == tree, f"source tree {key}")
        require(source["nodes"][key]["contract_sha256"] == contract, f"source contract {key}")
    require(data["record_floor"] == 274980728111260126, "record floor")
    require(set(data["rows"]) == {str(value) for value in ROWS}, "row set")

    results = {}
    for kprime in ROWS:
        row = data["rows"][str(kprime)]
        q, m, n = kprime - 10, 67472 + kprime, 1048576 + kprime
        require((row["q"], row["m"], row["n"]) == (q, m, n), f"parameters {kprime}")
        require(row["plain_evaluations"] > row["plain_unsafe_cells"] > 0, f"plain counts {kprime}")
        require(re.fullmatch(r"[0-9a-f]{64}", row["unsafe_tuple_sha256"]) is not None, f"tuple digest {kprime}")
        require(row["unsafe_maximum"] >= row["unsafe_minimum"] > row["safe_premium_ceiling"], f"unsafe range {kprime}")
        require(row["completion_premium"] + row["premium_ceiling_margin"] == row["safe_premium_ceiling"], f"premium margin {kprime}")
        require(row["reroute_maximum"] + row["reroute_minimum_margin"] == row["safe_premium_ceiling"], f"reroute margin {kprime}")
        require(row["reroute_evaluations"] >= row["plain_unsafe_cells"], f"reroute count {kprime}")
        lanes = row["geometry_lanes"]
        require([item["lane"] for item in lanes] == ["carrier32_geom", "one_geom", "two_geom", "three_geom", "four_geom", "five_geom", "six_geom"], f"lane names {kprime}")
        require(sum(item["evaluations"] for item in lanes) == row["geometry_total_evaluations"], f"lane count {kprime}")
        require(max(item["maximum"] for item in lanes) < row["completion_premium"], f"lane safety {kprime}")

        core_rows = {
            core: ATLAS.BASE.integral_core_offset_row(kprime, core)["chart"]
            for core in range(9, kprime)
        }
        marks = comb(n, 9) * max(core_rows.values())
        kernel = ATLAS.BASE.refined_kernel_capacity(kprime)
        records = data["record_floor"]
        full = (marks + records * row["completion_premium"]) // 55
        demand = records * comb(m, 11) - comb(n, 11)
        ceiling = (
            records * 55 * comb(m, 11)
            - 55 * comb(n, 11)
            - 55 * kernel
            - marks
            - 1
        ) // records
        require(marks == row["rank_nine_marks"], f"marks {kprime}")
        require(kernel == row["kernel_capacity"], f"kernel {kprime}")
        require(full == row["full_rank_capacity"], f"full capacity {kprime}")
        require(full + kernel == row["total_capacity"], f"total capacity {kprime}")
        require(demand == row["required_component_incidence"], f"demand {kprime}")
        require(demand - full - kernel == row["gap"] > 0, f"positive gap {kprime}")
        require(ceiling == row["safe_premium_ceiling"], f"ceiling {kprime}")
        results[str(kprime)] = {"unsafe_cells": row["plain_unsafe_cells"], "gap": row["gap"]}

    claims = data["claims"]
    require(claims["rank9_closed_rows"] == list(ROWS), "closed rows")
    require(claims["rank9_closed_prefix"] == [10, 78], "closed prefix")
    require(claims["rank9_remaining_interval"] == [79, 15528], "remaining rank nine")
    require(claims["rank8_remaining_interval"] == [22, 22525], "remaining rank eight")
    require(not claims["chronology_owner"] and not claims["rank11_paid"], "rank eleven nonclaims")
    require(claims["active_v4_ledger_movement"] == 0 and not claims["KoalaBear_closed"], "global nonclaims")
    return results


def tamper_selftest(data: dict) -> int:
    mutations = (
        lambda item: item.__setitem__("exact_parent", "0" * 40),
        lambda item: item["source_prize_dag"]["nodes"]["74"].__setitem__("tree", "0" * 40),
        lambda item: item["rows"]["75"].__setitem__("unsafe_tuple_sha256", "0" * 63),
        lambda item: item["rows"]["76"].__setitem__("premium_ceiling_margin", 0),
        lambda item: item["rows"]["77"]["geometry_lanes"][0].__setitem__("maximum", 10**100),
        lambda item: item["rows"]["78"].__setitem__("gap", -1),
        lambda item: item["claims"].__setitem__("rank9_closed_prefix", [10, 79]),
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
