#!/usr/bin/env python3
"""Verify the compact K'=84 adjacent-support carrier payment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k84-adjacent-support-payment-v1/manifest.json"
MANIFEST_SHA256 = "4317c574e73626e2491e3dcfc777ab7e09c98333493f9161eb432a5ecfa355e3"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
SOURCE_COMMIT = "9a0baa42b35790f1e0d383e18dd721bcb7d9a86c"
SOURCE_TREE = "354e3859f7654bcec417f2dcd92b506a9984a7b2"
SOURCE_CONTRACT = "6cdb8f6495f90001bafe26e656566f6483d8505f565a69ebe57d2a6717d07cd3"
EXPECTED_DEPENDENCIES = [
    "kb-mca-rank11-k83-adjacent-support-payment-v1",
    "single completion carrier",
    "full-completion pairwise carrier atlas",
    "fixed-union support-4/5 coupling",
    "fixed-union support-5/6 coupling",
    "fixed-union adjacent-support coupling",
]
EXPECTED_CAPTURES = {
    "primary_wave": ("ap-1oAXY3d5xqakObFjYF0Ck6", "884e7bc9ee9c78b49e1324bb3c11ca0ca3d6044114f2bc88dd4cee196b2c916a"),
    "audit_wave": ("ap-CE1YUXVUmNXrwze1lDP6Wn", "11420a74fbebe5f63d717e633c9914c9089c3fb92546051e267c03b60ee1a850"),
    "compact_merger": ("ap-UwcGaJZm4Wst0Ozq1NMRIp", "abc5638fba58fee000c0e8552ea449c4f8058713da3b784a989bf454235633a8"),
    "component_payment": ("ap-H3we0j1uIdfDebkyKPSRbR", "58b8a3077d2dc80444b91a9b0057f6ad47a9fd07a0bce0456904522cc4d054c5"),
}
EXPECTED_SOURCES = {
    "primary_router": "a3f55cf0627f63b9786d3f44f526bb44c62d223152424099f1039df04d272a20",
    "independent_router": "a9a323316bcbef966ad97ca3e24f66220aa41baf8d5115e7ca3f3205e3e37249",
    "merger": "11ef8d98a1cc07db73f4f6e6a17ebb975210a475cf08a8eaa525c4a5ea2a415a",
    "component_payment": "391232fc91db032d2599c18e47ad5f9368cf3b9650ede0634972ad118f941207",
    "checkpointed_batch_runner": "bbe9f1100d8d6add611794e24e02d57ab0f57903a15195a944e6fe640ca98922",
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


BASE = load_module("rank11_split_pencil_base_for_k84_adjacent", BASE_PATH)


def validate(data: object) -> dict[str, object]:
    require(isinstance(data, dict), "manifest object")
    require(data["schema"] == "kb-mca-rank11-k84-adjacent-support-payment-v1", "schema")
    require(data["exact_parent"] == "e356ef800479d3e3c4c00218b63b1ae898b58362", "parent")
    require(data["previous_packet_sha256"] == "99e01210543223ae45aa8e1f88a49c11951a0b37fd2f3496c1ce1e886d04a3fd", "previous packet")

    source = data["source_prize_dag"]
    require(source["repository"] == "AllenGrahamHart/rs-mca-prize-dag", "source repository")
    require(source["commit"] == SOURCE_COMMIT, "source commit")
    require(source["node"]["id"] == "rate_half_mca_rank11_k84_adjacent_support_carrier_payment", "source node")
    require(source["node"]["tree"] == SOURCE_TREE, "source tree")
    require(source["node"]["contract_sha256"] == SOURCE_CONTRACT, "source contract")

    require(data["dependencies"] == EXPECTED_DEPENDENCIES, "dependency chain")
    coverage = data["coverage"]
    require(coverage["partition"] == "ordinary plus offsets 1..73", "partition")
    require((coverage["lanes"], coverage["jobs"]) == (74, 148), "lane coverage")
    offset_units = sum((74 - offset) * 5625 for offset in range(1, 74))
    require(coverage["source_units"] == coverage["ordinary_units"] + offset_units, "source units")
    require(coverage["raw_rows"] == 7 * coverage["source_units"], "raw rows")
    require(coverage["ordinary_raw_rows"] == 7 * coverage["ordinary_units"], "ordinary rows")
    require((coverage["ordinary_raw_safe_units"], coverage["ordinary_expanded_units"]) == (108047, 1621), "ordinary split")
    require(coverage["primary_geometry_rows"] == 268721026, "primary geometry")
    require(coverage["audit_geometry_rows"] == 520900317 >= coverage["primary_geometry_rows"], "audit geometry")

    frontier = data["frontier"]
    require(frontier["global_lane"] == "ordinary", "global lane")
    require(frontier["global_branch"] == "s2=74/s3=55/s4=45/s5=37/ordinary-single/c6d3/c7d2/c8d1/c9d0/raw-safe", "global branch")
    require(frontier["completion_premium"] + frontier["premium_ceiling_margin"] == frontier["safe_premium_ceiling"], "premium margin")
    require(frontier["premium_ceiling_margin"] > 0, "positive premium margin")

    row = data["k84"]
    require((row["q"], row["m"], row["n"]) == (74, 67556, 1048660), "row parameters")
    records = data["record_floor"]
    chart = max(BASE.integral_core_offset_row(84, core)["chart"] for core in range(9, 84))
    marks = comb(row["n"], 9) * chart
    kernel = BASE.refined_kernel_capacity(84)
    full = (marks + records * frontier["completion_premium"]) // 55
    demand = records * comb(row["m"], 11) - comb(row["n"], 11)
    ceiling = (
        records * 55 * comb(row["m"], 11) - 55 * comb(row["n"], 11)
        - 55 * kernel - marks - 1
    ) // records
    require(marks == row["rank_nine_marks"], "rank-nine marks")
    require(kernel == row["kernel_capacity"], "kernel capacity")
    require(full == row["full_rank_capacity"], "full-rank capacity")
    require(full + kernel == row["total_capacity"], "total capacity")
    require(demand == row["required_component_incidence"], "required incidence")
    require(demand - full - kernel == row["gap"] > 0, "component gap")
    require(ceiling == frontier["safe_premium_ceiling"], "safe ceiling")

    require(len(data["captures"]) == 4, "capture count")
    captures = {item["role"]: (item["app_id"], item["sha256"]) for item in data["captures"]}
    require(captures == EXPECTED_CAPTURES, "capture custody")
    require(data["source_hashes"] == EXPECTED_SOURCES, "source custody")
    claims = data["claims"]
    require(claims["rank9_closed_prefix"] == [10, 84], "closed prefix")
    require(claims["rank9_remaining_interval"] == [85, 15528], "remaining interval")
    require(claims["first_open_rank9_row"] == 85, "first open row")
    require(not claims["rank11_paid"] and not claims["KoalaBear_closed"] and not claims["prize_problems_closed"], "nonclaims")
    return {
        "closed_prefix": [10, 84],
        "first_open_rank9_row": 85,
        "premium": frontier["completion_premium"],
        "margin": frontier["premium_ceiling_margin"],
        "gap": row["gap"],
    }


def tamper_selftest(data: dict) -> int:
    mutations = [
        lambda item: item["source_prize_dag"].__setitem__("commit", "0" * 40),
        lambda item: item["coverage"].__setitem__("source_units", item["coverage"]["source_units"] - 1),
        lambda item: item["frontier"].__setitem__("completion_premium", item["frontier"]["completion_premium"] + 1),
        lambda item: item["k84"].__setitem__("gap", -1),
        lambda item: item["captures"][0].__setitem__("sha256", "0" * 64),
        lambda item: item["claims"].__setitem__("first_open_rank9_row", 84),
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
