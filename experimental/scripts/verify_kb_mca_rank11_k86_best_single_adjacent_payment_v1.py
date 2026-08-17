#!/usr/bin/env python3
"""Verify the compact K'=86 best-single adjacent payment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k86-best-single-adjacent-payment-v1/manifest.json"
MANIFEST_SHA256 = "d0869e5755252d08a59bfe763fd33c5032796ebc67ca410c7432d98d05762072"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
SOURCE_COMMIT = "a0f03f3af3b8bffb303dfe8e0b338b40e49da5ee"
SOURCE_TREE = "5d5e1503591ec1ebca92847538f3b1a7d6ef6dfb"
SOURCE_CONTRACT = "b318de9938264a3306372b473513b1975e6941204a39c03d07a5ff16b62e896f"
EXPECTED_DEPENDENCIES = [
    "kb-mca-rank11-k85-best-single-adjacent-payment-v1",
    "single completion carrier",
    "full-completion pairwise carrier atlas",
    "fixed-union support-4/5 coupling",
    "fixed-union support-5/6 coupling",
    "fixed-union adjacent-support coupling",
]
EXPECTED_CAPTURES = {
    "ordinary_slice": (
        "ap-OP9ryrK2YdHRg463E43ktv",
        "d343b18cfef00d6a1dff8634a2ffe8b8574d25a59cf44f43d4c3862e47c8a4d8",
    ),
    "raw_threshold_wave": (
        "ap-kjz4PvurdW9cunGO3pse1N",
        "7aa3c934e610aa717ba25b8b7acf424c0f59ad068ec294eac5b448d9abb81612",
    ),
    "best_single_wave": (
        "ap-HSdSkI0KYmWfnz0jL0Bron",
        "bc67b9fa9ffa6b386d5d5f9e053e2d5a99a8451f2e9ae8d03c0095cc6f867349",
    ),
    "component_payment": (
        "ap-3mwC5dZ9yYxOTcOJx9JygE",
        "252d9dfa3f4c6e819a706a54e437aae1337907473e3dd3113bff460764007f3e",
    ),
}
EXPECTED_SOURCES = {
    "ordinary_primary": "ca6ffd6766d1e4aac72d98ea09fa30c5d1b100a01c2e51e5e7673bfc92f33106",
    "ordinary_independent": "ceab00de841839ee0c76eb440e847f27aeb524d11dc6646742f774991817a2ef",
    "ordinary_slice_checker": "1e1320d542a8187749cbd83a5cb7f174fb79f3cc0e208f4bc57bbae9b37686c8",
    "raw_primary": "e37b36fec4eab6286e353e54027b87235f0369947c814e795bcbff7a7aa8a68d",
    "raw_independent": "429336fefdf47623184b2d2f2e21953f50be7fe07dda2c1e8ba054e4af637d74",
    "raw_merger": "2a32a19df70f098fee290c96545d704f1de1479a995876c50876d8fc79d25f86",
    "best_single_primary": "8a2ec9877e317798e615e14d0e23b2f0c65d927a109985c7aec160c1cc65db97",
    "best_single_independent": "ad37ddbfa7920e57ad912b523751d9415944f8e16459c49bb7973a86e386cd10",
    "best_single_shared_core": "2eb7f85cf6fb4311874f453c75fc868796dbc726599462e12b640e98fe2a9939",
    "best_single_k85_primary": "2c94b7432cd4c9d37a49288298761cbff9227a07f694fe80ec259ef19e724505",
    "best_single_k85_independent": "f9a01624b5a11fbc30f58a4f4afca2aa75d9af96b35c69edddcdc7eef5e1fa1f",
    "best_single_k85_base": "cd1e9d2706c48be390387953c4abeea46958af258f132700809cf2393a5e4a90",
    "best_single_merger": "d7e83244e5b674c05c710d4930b85616115616d9ac53bd068328a8db7dd1e932",
    "component_payment": "fc2f9a1c6f406063ca305a6744852680fdf363c422fa6a9586db9b071752cc65",
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


BASE = load_module("rank11_split_pencil_base_for_k86_adjacent", BASE_PATH)


def validate(data: object) -> dict[str, object]:
    require(isinstance(data, dict), "manifest object")
    require(data["schema"] == "kb-mca-rank11-k86-best-single-adjacent-payment-v1", "schema")
    require(data["exact_parent"] == "7356a104a4ec2d21f6c0fc32a3fb3c394cf5e8cf", "parent")
    require(data["previous_packet_sha256"] == "ae598632a204181a0ef0cc8895c077af22d16587f2ab209b7cebb3e26c2cb5ee", "previous packet")

    source = data["source_prize_dag"]
    require(source["repository"] == "AllenGrahamHart/rs-mca-prize-dag", "source repository")
    require(source["commit"] == SOURCE_COMMIT, "source commit")
    require(source["node"]["id"] == "rate_half_mca_rank11_k86_best_single_adjacent_payment", "source node")
    require(source["node"]["tree"] == SOURCE_TREE, "source tree")
    require(source["node"]["contract_sha256"] == SOURCE_CONTRACT, "source contract")
    require(data["dependencies"] == EXPECTED_DEPENDENCIES, "dependency chain")

    coverage = data["coverage"]
    require(coverage["partition"] == "ordinary plus offsets 1..75", "partition")
    ordinary = coverage["ordinary"]
    require(ordinary["jobs"] == 2, "ordinary jobs")
    require(ordinary["raw_rows"] == 7 * ordinary["source_units"], "ordinary rows")
    require((ordinary["raw_safe_units"], ordinary["expanded_units"]) == (115523, 3037), "ordinary split")
    require(ordinary["audit_geometry_rows"] >= ordinary["primary_geometry_rows"] > 0, "ordinary geometry")
    require("broader incomplete pilot" in ordinary["custody_scope"], "ordinary custody scope")

    raw = coverage["raw_offsets"]
    require((raw["lanes"], raw["jobs"]) == (75, 150), "raw jobs")
    offset_units = sum((76 - offset) * 5929 for offset in range(1, 76))
    require(raw["source_units_per_implementation"] == offset_units, "raw source units")
    require(raw["raw_rows_per_implementation"] == 7 * offset_units, "raw rows")
    require(raw["raw_safe_units_per_implementation"] + raw["raw_unsafe_units_per_implementation"] == offset_units, "raw split")
    require(raw["unsafe_offset_interval"] == [1, 42], "unsafe interval")
    require(raw["fully_safe_offset_interval"] == [43, 75], "safe interval")

    residual = coverage["best_single_residual"]
    require((residual["lanes"], residual["jobs"]) == (42, 84), "residual jobs")
    residual_sources = sum((76 - offset) * 5929 for offset in range(1, 43))
    require(residual["source_units_per_implementation"] == residual_sources, "residual sources")
    require(residual["unsafe_units_per_implementation"] == raw["raw_unsafe_units_per_implementation"], "residual conservation")
    require(residual["profiles_per_implementation"] == 62159220, "residual profiles")
    require("no simultaneous overlapping-edge composition" in residual["rule"], "single-edge scope")

    frontier = data["frontier"]
    require(frontier["global_lane"] == "offset32", "global lane")
    require(frontier["global_branch"] == "s2=73/s3=41/s4=39/s5=57/offset32/c6F/c7F/c8F/c9F", "global branch")
    require(ordinary["premium"] < frontier["completion_premium"], "ordinary below frontier")
    require(frontier["completion_premium"] + frontier["premium_ceiling_margin"] == frontier["safe_premium_ceiling"], "premium margin")
    require(frontier["premium_ceiling_margin"] > 0, "positive premium margin")

    row = data["k86"]
    require((row["q"], row["m"], row["n"]) == (76, 67558, 1048662), "row parameters")
    records = data["record_floor"]
    chart = max(BASE.integral_core_offset_row(86, core)["chart"] for core in range(9, 86))
    marks = comb(row["n"], 9) * chart
    kernel = BASE.refined_kernel_capacity(86)
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
    require(claims["rank9_closed_prefix"] == [10, 86], "closed prefix")
    require(claims["rank9_remaining_interval"] == [87, 15528], "remaining interval")
    require(claims["first_open_rank9_row"] == 87, "first open row")
    require(not claims["rank11_paid"] and not claims["KoalaBear_closed"] and not claims["prize_problems_closed"], "nonclaims")
    return {
        "closed_prefix": [10, 86],
        "first_open_rank9_row": 87,
        "premium": frontier["completion_premium"],
        "margin": frontier["premium_ceiling_margin"],
        "gap": row["gap"],
    }


def tamper_selftest(data: dict) -> int:
    mutations = [
        lambda item: item["source_prize_dag"].__setitem__("commit", "0" * 40),
        lambda item: item["coverage"]["ordinary"].__setitem__("custody_scope", "complete batch"),
        lambda item: item["coverage"]["raw_offsets"].__setitem__("source_units_per_implementation", 16897649),
        lambda item: item["coverage"]["best_single_residual"].__setitem__("unsafe_units_per_implementation", 415412),
        lambda item: item["coverage"]["best_single_residual"].__setitem__("rule", "compose all edges"),
        lambda item: item["frontier"].__setitem__("completion_premium", item["frontier"]["completion_premium"] + 1),
        lambda item: item["k86"].__setitem__("gap", -1),
        lambda item: item["claims"].__setitem__("first_open_rank9_row", 86),
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
