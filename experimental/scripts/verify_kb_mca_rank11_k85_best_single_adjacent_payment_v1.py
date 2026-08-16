#!/usr/bin/env python3
"""Verify the compact K'=85 best-single adjacent payment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k85-best-single-adjacent-payment-v1/manifest.json"
MANIFEST_SHA256 = "ae598632a204181a0ef0cc8895c077af22d16587f2ab209b7cebb3e26c2cb5ee"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
SOURCE_COMMIT = "c4fdef465aabc8abae7a18b9694bed9cf34e362b"
SOURCE_TREE = "fc59f079d87a20f6c71f9b0b78345c2b518a0c44"
SOURCE_CONTRACT = "0a4dd3003a644b7e0e0354e34fbfb797590d193ea7f563f96507cf749deb7600"
EXPECTED_DEPENDENCIES = [
    "kb-mca-rank11-k84-adjacent-support-payment-v1",
    "single completion carrier",
    "full-completion pairwise carrier atlas",
    "fixed-union support-4/5 coupling",
    "fixed-union support-5/6 coupling",
    "fixed-union adjacent-support coupling",
]
EXPECTED_CAPTURES = {
    "route_pilot": ("ap-d16UIhECIz7nYzMEAZr8d7", "5a6ee4f212571eae022ed943c6062e95f6b6a2ccb186dbf4338f1b0cf2f45327"),
    "raw_threshold_wave": ("ap-rTfQtYZuTdgjfk5IWhal5W", "5832710721306c16477523b02303fb6f45fb293f6ea53c71e26bad2a9babac13"),
    "best_single_wave": ("ap-avKuaBEl3bNsvVug235bXS", "a2a47722b66ff40ed83b44c47dc725b341700ffc2c9653a61e63f7dff1fedfa8"),
    "component_payment": ("ap-9R6TUWXTLwS11AiqMsAem5", "e3bf7fdbd3c6b87ea2bb82bd2520f6ffff5e76353e0698e8df7494bf75745799"),
}
EXPECTED_SOURCES = {
    "ordinary_primary": "363cae26e7c0258b27ec27da25b313f8214f6211aa1b891b8c7f506d4987d043",
    "ordinary_independent": "b0bf02ad6dbf6a6c47556a0e8f8d59a82802f83feec1146d22e8ef4b1b7ecaec",
    "ordinary_merger": "32aa55ce1a31605c7d72678e51855af808a92ccf70a70f029aeaa11d0930134f",
    "raw_primary": "b13ab1262105d53694407a9c448362bfa85b7914e6fce6242b715f2436c63b3b",
    "raw_independent": "90380f5d1f8191172dae43e90b9802873ed6f680a2bc41a49d50d3dade10f59c",
    "raw_merger": "28d9289be8c0e741a364a72884e171154ff0186ea732b1f1cdda3990c3ea333c",
    "best_single_primary": "2c94b7432cd4c9d37a49288298761cbff9227a07f694fe80ec259ef19e724505",
    "best_single_independent": "f9a01624b5a11fbc30f58a4f4afca2aa75d9af96b35c69edddcdc7eef5e1fa1f",
    "best_single_base": "cd1e9d2706c48be390387953c4abeea46958af258f132700809cf2393a5e4a90",
    "best_single_merger": "e5c8012cd13ca6c17395fa1be91ce45f0af66042f65d2c58186c1feff3868040",
    "component_payment": "8e3fa571c1930f11a8c0a38b6595ff6e4b712158d2d84792912db5c88285ebe8",
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


BASE = load_module("rank11_split_pencil_base_for_k85_adjacent", BASE_PATH)


def validate(data: object) -> dict[str, object]:
    require(isinstance(data, dict), "manifest object")
    require(data["schema"] == "kb-mca-rank11-k85-best-single-adjacent-payment-v1", "schema")
    require(data["exact_parent"] == "cba05d4ca6c8cb08fd3444a72a55f298fe47b0bc", "parent")
    require(data["previous_packet_sha256"] == "4317c574e73626e2491e3dcfc777ab7e09c98333493f9161eb432a5ecfa355e3", "previous packet")

    source = data["source_prize_dag"]
    require(source["repository"] == "AllenGrahamHart/rs-mca-prize-dag", "source repository")
    require(source["commit"] == SOURCE_COMMIT, "source commit")
    require(source["node"]["id"] == "rate_half_mca_rank11_k85_best_single_adjacent_payment", "source node")
    require(source["node"]["tree"] == SOURCE_TREE, "source tree")
    require(source["node"]["contract_sha256"] == SOURCE_CONTRACT, "source contract")
    require(data["dependencies"] == EXPECTED_DEPENDENCIES, "dependency chain")

    coverage = data["coverage"]
    require(coverage["partition"] == "ordinary plus offsets 1..74", "partition")
    ordinary = coverage["ordinary"]
    require(ordinary["jobs"] == 2, "ordinary jobs")
    require(ordinary["raw_rows"] == 7 * ordinary["source_units"], "ordinary rows")
    require((ordinary["raw_safe_units"], ordinary["expanded_units"]) == (114561, 2439), "ordinary split")
    require(ordinary["audit_geometry_rows"] >= ordinary["primary_geometry_rows"] > 0, "ordinary geometry")

    raw = coverage["raw_offsets"]
    require((raw["lanes"], raw["jobs"]) == (74, 148), "raw jobs")
    offset_units = sum((75 - offset) * 5776 for offset in range(1, 75))
    require(raw["source_units_per_implementation"] == offset_units, "raw source units")
    require(raw["raw_rows_per_implementation"] == 7 * offset_units, "raw rows")
    require(raw["raw_safe_units_per_implementation"] + raw["raw_unsafe_units_per_implementation"] == offset_units, "raw split")
    require(raw["unsafe_offset_interval"] == [1, 41], "unsafe interval")
    require(raw["fully_safe_offset_interval"] == [42, 74], "safe interval")

    residual = coverage["best_single_residual"]
    require((residual["lanes"], residual["jobs"]) == (41, 82), "residual jobs")
    residual_sources = sum((75 - offset) * 5776 for offset in range(1, 42))
    require(residual["source_units_per_implementation"] == residual_sources, "residual sources")
    require(residual["unsafe_units_per_implementation"] == raw["raw_unsafe_units_per_implementation"], "residual conservation")
    require(residual["profiles_per_implementation"] == 49090656, "residual profiles")
    require("no simultaneous overlapping-edge composition" in residual["rule"], "single-edge scope")

    frontier = data["frontier"]
    require(frontier["global_lane"] == "offset11", "global lane")
    require(frontier["global_branch"] == "s2=56/s3=45/s4=58/s5=37/offset11/c6F/c7F/c8F/c9F", "global branch")
    require(ordinary["premium"] < frontier["completion_premium"], "ordinary below frontier")
    require(frontier["completion_premium"] + frontier["premium_ceiling_margin"] == frontier["safe_premium_ceiling"], "premium margin")
    require(frontier["premium_ceiling_margin"] > 0, "positive premium margin")

    row = data["k85"]
    require((row["q"], row["m"], row["n"]) == (75, 67557, 1048661), "row parameters")
    records = data["record_floor"]
    chart = max(BASE.integral_core_offset_row(85, core)["chart"] for core in range(9, 85))
    marks = comb(row["n"], 9) * chart
    kernel = BASE.refined_kernel_capacity(85)
    full = (marks + records * frontier["completion_premium"]) // 55
    demand = records * comb(row["m"], 11) - comb(row["n"], 11)
    numerator = records * 55 * comb(row["m"], 11) - 55 * comb(row["n"], 11) - 55 * kernel - marks - 1
    ceiling, remainder = divmod(numerator, records)
    require(marks == row["rank_nine_marks"], "rank-nine marks")
    require(kernel == row["kernel_capacity"], "kernel capacity")
    require(full == row["full_rank_capacity"], "full-rank capacity")
    require(full + kernel == row["total_capacity"], "total capacity")
    require(demand == row["required_component_incidence"], "required incidence")
    require(demand - full - kernel == row["gap"] > 0, "component gap")
    require((ceiling, remainder) == (frontier["safe_premium_ceiling"], row["ceiling_remainder"]), "safe ceiling")

    captures = {item["role"]: (item["app_id"], item["sha256"]) for item in data["captures"]}
    require(captures == EXPECTED_CAPTURES, "capture custody")
    require(data["source_hashes"] == EXPECTED_SOURCES, "source custody")
    claims = data["claims"]
    require(claims["rank9_closed_prefix"] == [10, 85], "closed prefix")
    require(claims["rank9_remaining_interval"] == [86, 15528], "remaining interval")
    require(claims["first_open_rank9_row"] == 86, "first open row")
    require(not claims["rank11_paid"] and not claims["KoalaBear_closed"] and not claims["prize_problems_closed"], "nonclaims")
    return {
        "closed_prefix": [10, 85],
        "first_open_rank9_row": 86,
        "premium": frontier["completion_premium"],
        "margin": frontier["premium_ceiling_margin"],
        "gap": row["gap"],
    }


def tamper_selftest(data: dict) -> int:
    mutations = [
        lambda item: item["source_prize_dag"].__setitem__("commit", "0" * 40),
        lambda item: item["coverage"]["raw_offsets"].__setitem__("source_units_per_implementation", 16028399),
        lambda item: item["coverage"]["best_single_residual"].__setitem__("unsafe_units_per_implementation", 331532),
        lambda item: item["coverage"]["best_single_residual"].__setitem__("rule", "compose all edges"),
        lambda item: item["frontier"].__setitem__("completion_premium", item["frontier"]["completion_premium"] + 1),
        lambda item: item["k85"].__setitem__("gap", -1),
        lambda item: item["claims"].__setitem__("first_open_rank9_row", 85),
    ]
    caught = 0
    for mutate in mutations:
        hostile = copy.deepcopy(data)
        mutate(hostile)
        try:
            validate(hostile)
        except (Reject, AssertionError, KeyError, TypeError, ValueError):
            caught += 1
    require(caught == len(mutations), "tamper selftest")
    return caught


def main() -> None:
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


if __name__ == "__main__":
    main()
