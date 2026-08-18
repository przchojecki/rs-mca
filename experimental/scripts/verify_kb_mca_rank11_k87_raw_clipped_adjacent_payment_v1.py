#!/usr/bin/env python3
"""Verify the compact K'=87 raw-clipped adjacent-support payment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k87-raw-clipped-adjacent-payment-v1/manifest.json"
MANIFEST_SHA256 = "ec81aa702181ba7a683e9f2a1afeb942a968c7d0232d6e3e7f3e44669d3f0f8a"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
SOURCE_COMMIT = "b869fb9dd2e740e323bee74e7ee72475905901f5"
ROW_TREE = "1c00acd2b2293b97623bbbec695d98aa8689d218"
THEOREM_TREE = "f1e826876806f3e30287f4e64d86f655714af081"
SOURCE_CONTRACT = "fc0699db0b33a5ff6a6fe04b918e5cbd5eefe3e9b29b9acd7816880b31cf7c88"
SOURCE_HASHES_DIGEST = "f3f32dee35800d3ed36039f16d9cb2539532111c44987efe63310ac65457bcd2"
EXPECTED_DEPENDENCIES = [
    "kb-mca-rank11-k86-best-single-adjacent-payment-v1",
    "single completion carrier",
    "full-completion pairwise carrier atlas",
    "base-field-normalized fixed-union adjacent-support census",
    "raw-clipped adjacent-support circuit coupling",
]
EXPECTED_CAPTURES = {
    "ordinary": (
        "ap-t1IWAsyDidGwq0ZwwYO6yI",
        "06a550c1f65be3c2a7c4d96590188f5de6ca792c1f87e638f2fa7d5163b43519",
    ),
    "raw_threshold_wave": (
        "ap-xwOdMdTBRKtC2aIHtpRSw0",
        "2722d7811cf29e425bd67fd49a46f586efe2f21c0dda698e369dcfe4fd48b449",
    ),
    "component_payment": (
        "ap-JAw6W5GHktZA9TXLxcpMUY",
        "883f659486162495750adbc80c97d3224cdae6b3bdebf3429492a33189d95312",
    ),
}
EXPECTED_CLIPPED_APPS = [
    "ap-iXONaPwRxMHjwZR515sOyi",
    "ap-dJ2eUU9a0u0jcJjXZiefIU",
    "ap-xr0f01RFscUvWkrGvn7VGk",
    "ap-qFATW8MSFF0dzBoqm4ekA9",
    "ap-KzzGy55iKSUXT04uVv7UOh",
    "ap-TLGJytlHAZRLOm0pn0e8Oh",
]
DEFICITS = {2: 36, 3: 28, 4: 21, 5: 15, 6: 10, 7: 6, 8: 3, 9: 1}


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


BASE = load_module("rank11_split_pencil_base_for_k87_raw_clipped", BASE_PATH)


def theorem_rows(spec: dict[str, int]):
    kprime = spec["kprime"]
    m = spec["m"]
    union = spec["union"]
    dimension = spec["vanishing_dimension"]
    support = spec["lower_support"]
    residual, outside = kprime - union - dimension, m - union
    rows = []
    for inside in range(support - 1):
        high_coefficient = support + 1 - inside
        low_coefficient = outside - residual - support + 1 + inside
        rhs = comb(union, inside) * residual * comb(outside, support - inside)
        low_cap = (
            comb(union, inside)
            * residual
            * comb(outside, support - 1 - inside)
            // (support - inside)
        )
        rows.append((inside, high_coefficient, low_coefficient, rhs, low_cap))
    direct_low = comb(union, support - 1) * residual + comb(union, support)
    direct_high = (
        comb(union, support - 1) * residual * outside // 2
        + comb(union, support) * residual
        + comb(union, support + 1)
    )
    return rows, direct_low, direct_high


def lower_orientation_optimum(spec: dict[str, int]) -> Fraction:
    rows, direct_low, direct_high = theorem_rows(spec)
    support, m = spec["lower_support"], spec["m"]
    raw_low = spec["lower_circuit_cap"]
    raw_high = spec["upper_circuit_cap"]
    ordered = sorted(rows, key=lambda row: Fraction(row[2], row[1]))
    maximum_low = min(raw_low, direct_low + sum(row[4] for row in rows))
    maximum_high_at_zero = Fraction(direct_high) + sum(
        Fraction(row[3], row[1]) for row in rows
    )
    candidates = {Fraction(0), Fraction(maximum_low)}
    start, current_high = Fraction(direct_low), maximum_high_at_zero
    if start <= maximum_low:
        candidates.add(start)
    for _, high_coefficient, low_coefficient, _, low_cap in ordered:
        end = start + low_cap
        clipped_end = min(end, Fraction(maximum_low))
        if start <= maximum_low:
            candidates.update((start, clipped_end))
            loss = Fraction(low_coefficient, high_coefficient)
            crossing = start + (current_high - raw_high) / loss
            if start <= crossing <= clipped_end:
                candidates.add(crossing)
        current_high -= Fraction(low_coefficient * low_cap, high_coefficient)
        start = end

    def evaluate(total_low: Fraction) -> Fraction:
        remaining = max(Fraction(0), total_low - direct_low)
        loss = Fraction(0)
        for _, high_coefficient, low_coefficient, _, low_cap in ordered:
            used = min(remaining, Fraction(low_cap))
            loss += Fraction(low_coefficient, high_coefficient) * used
            remaining -= used
        require(remaining == 0, "lower allocation")
        total_high = min(Fraction(raw_high), maximum_high_at_zero - loss)
        weight_low = DEFICITS[support] * comb(m - support, 11 - support)
        weight_high = DEFICITS[support + 1] * comb(m - support - 1, 10 - support)
        return weight_low * total_low + weight_high * total_high

    return max(evaluate(candidate) for candidate in candidates)


def canonical_digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def validate(data: object) -> dict[str, object]:
    require(isinstance(data, dict), "manifest object")
    require(data["schema"] == "kb-mca-rank11-k87-raw-clipped-adjacent-payment-v1", "schema")
    require(data["exact_parent"] == "7214947e5f7bd2b350f056ee2bbf75c5c4effd06", "parent")
    require(data["previous_packet_sha256"] == "d0869e5755252d08a59bfe763fd33c5032796ebc67ca410c7432d98d05762072", "previous packet")

    source = data["source_prize_dag"]
    require(source["repository"] == "AllenGrahamHart/rs-mca-prize-dag", "source repository")
    require(source["commit"] == SOURCE_COMMIT, "source commit")
    require(source["row_node"] == {
        "id": "rate_half_mca_rank11_k87_raw_clipped_adjacent_payment",
        "tree": ROW_TREE,
        "contract_sha256": SOURCE_CONTRACT,
    }, "row source")
    require(source["theorem_node"] == {
        "id": "rate_half_mca_sparse_circuit_raw_clipped_adjacent_support_coupling",
        "tree": THEOREM_TREE,
    }, "theorem source")
    require(data["dependencies"] == EXPECTED_DEPENDENCIES, "dependency chain")
    require(canonical_digest(data["source_hashes"]) == SOURCE_HASHES_DIGEST, "source custody")

    theorem = data["raw_clipped_theorem"]
    require("exact eleven-set extension factors" in theorem["claim"], "normalization claim")
    require("overlapping pair bounds are never added" in theorem["composition_rule"], "composition rule")
    spec = theorem["k87_specialization"]
    require(
        (spec["kprime"], spec["m"], spec["union"], spec["vanishing_dimension"], spec["lower_support"])
        == (87, 67559, 34, 6, 5),
        "theorem specialization",
    )
    optimum = lower_orientation_optimum(spec)
    require(optimum.numerator == spec["weighted_optimum_numerator"], "theorem numerator")
    require(optimum.denominator == spec["weighted_optimum_denominator"] == 3, "theorem denominator")
    require(optimum.numerator // optimum.denominator == spec["weighted_optimum_floor"], "theorem floor")

    coverage = data["coverage"]
    require(coverage["partition"] == "ordinary plus offsets 1..76", "partition")
    ordinary = coverage["ordinary"]
    require(ordinary["jobs"] == 2, "ordinary jobs")
    require(ordinary["raw_rows"] == 7 * ordinary["source_units"], "ordinary rows")
    require((ordinary["raw_safe_units"], ordinary["expanded_units"]) == (121895, 4385), "ordinary split")
    require(ordinary["audit_geometry_rows"] == ordinary["primary_geometry_rows"] == 2940875, "ordinary geometry")
    require("fresh complete" in ordinary["custody_scope"], "ordinary custody")

    raw = coverage["raw_offsets"]
    require((raw["lanes"], raw["jobs"]) == (76, 152), "raw jobs")
    offset_units = sum((77 - offset) * 6084 for offset in range(1, 77))
    require(raw["source_units_per_implementation"] == offset_units, "raw source units")
    require(raw["raw_rows_per_implementation"] == 7 * offset_units, "raw rows")
    require(raw["raw_safe_units_per_implementation"] + raw["raw_unsafe_units_per_implementation"] == offset_units, "raw split")
    require(raw["unsafe_offset_interval"] == [1, 43], "unsafe interval")
    require(raw["fully_safe_offset_interval"] == [44, 76], "safe interval")

    clipped = coverage["raw_clipped_residual"]
    require((clipped["lanes"], clipped["jobs"]) == (43, 86), "clipped jobs")
    clipped_sources = sum((77 - offset) * 6084 for offset in range(1, 44))
    require(clipped["source_units_per_implementation"] == clipped_sources, "clipped sources")
    require(clipped["unsafe_units_per_implementation"] == raw["raw_unsafe_units_per_implementation"], "residual conservation")
    require(clipped["profiles_per_implementation"] == 77179660, "clipped profiles")
    require("support-disjoint" in clipped["rule"], "clipped composition scope")

    frontier = data["frontier"]
    require(frontier["global_lane"] == "offset9", "global lane")
    require(frontier["global_branch"] == "s2=55/s3=46/s4=37/s5=30/offset9/c6F/c7F/c8F/c9F", "global branch")
    require(ordinary["premium"] < frontier["completion_premium"], "ordinary below frontier")
    require(frontier["completion_premium"] + frontier["premium_ceiling_margin"] == frontier["safe_premium_ceiling"], "premium margin")
    require(frontier["premium_ceiling_margin"] > 0, "positive premium margin")

    row = data["k87"]
    require((row["q"], row["m"], row["n"]) == (77, 67559, 1048663), "row parameters")
    records = data["record_floor"]
    chart = max(BASE.integral_core_offset_row(87, core)["chart"] for core in range(9, 87))
    marks = comb(row["n"], 9) * chart
    kernel = BASE.refined_kernel_capacity(87)
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
    ranges = data["raw_clipped_captures"]
    require([item["app_id"] for item in ranges] == EXPECTED_CLIPPED_APPS, "clipped apps")
    expected_start = 1
    for item in ranges:
        start, end = item["offsets"]
        require(start == expected_start and start <= end, "clipped range partition")
        expected_start = end + 1
        require(len(item["sha256"]) == 64, "clipped hash")
    require(expected_start == 44, "clipped range endpoint")
    require(data["raw_clipped_merged_sha256"] == "6f8064320850e0009c18c967e2b61ec5b4d77c51e1c2afb4bee6fc41921e5cd8", "merged custody")

    claims = data["claims"]
    require(claims["rank9_closed_prefix"] == [10, 87], "closed prefix")
    require(claims["rank9_remaining_interval"] == [88, 15528], "remaining interval")
    require(claims["first_open_rank9_row"] == 88, "first open row")
    require(not any(claims[name] for name in ("rank11_paid", "KoalaBear_closed", "LIST_closed", "MCA_closed", "prize_problems_closed")), "nonclaims")
    return {
        "closed_prefix": [10, 87],
        "first_open_rank9_row": 88,
        "theorem_floor": spec["weighted_optimum_floor"],
        "premium": frontier["completion_premium"],
        "margin": frontier["premium_ceiling_margin"],
        "gap": row["gap"],
    }


def tamper_selftest(data: dict) -> int:
    mutations = [
        lambda item: item["source_prize_dag"].__setitem__("commit", "0" * 40),
        lambda item: item["raw_clipped_theorem"]["k87_specialization"].__setitem__("weighted_optimum_numerator", 0),
        lambda item: item["raw_clipped_theorem"].__setitem__("composition_rule", "compose all pairs"),
        lambda item: item["coverage"]["ordinary"].__setitem__("source_units", 542839),
        lambda item: item["coverage"]["raw_offsets"].__setitem__("source_units_per_implementation", 17801783),
        lambda item: item["coverage"]["raw_clipped_residual"].__setitem__("unsafe_units_per_implementation", 511676),
        lambda item: item["raw_clipped_captures"][2].__setitem__("offsets", [14, 20]),
        lambda item: item["frontier"].__setitem__("completion_premium", item["frontier"]["completion_premium"] + 1),
        lambda item: item["k87"].__setitem__("gap", -1),
        lambda item: item["claims"].__setitem__("first_open_rank9_row", 87),
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
