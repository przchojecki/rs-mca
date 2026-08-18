#!/usr/bin/env python3
"""Verify the compact K'=83 adjacent-support carrier payment."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k83-adjacent-support-payment-v1/manifest.json"
MANIFEST_SHA256 = "99e01210543223ae45aa8e1f88a49c11951a0b37fd2f3496c1ce1e886d04a3fd"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
SOURCE_PINS = {
    "adjacent_flat": ("9371c74006cd60469ed8204c6a63a980e5bc4d2e", "f13522164ec476abbfd3dbed10980921e8a9eb571393adad835c7c42d51388ce"),
    "single_carrier": ("6bdb49f65ff1cae876358405a874bd67008a576d", "288f425069d636b697ee6960e2a00980a69faa4dcb34e464d8093956a170e48b"),
    "support56": ("56dad9cc81887640c12c566256152ecbba98c1f2", "9bcc185828e42e0ca16133c166688c2491615e42065b90a4072481179e28dd06"),
    "adjacent_support": ("c8c6a32f0a18892647d0135df319a63ce7c3d6c7", "7bd4c049776213cf1aacfe4f2804aa485e19d3aca1102dd696d46d0e89989772"),
    "payment83": ("cdabbd7b4b0e84828ff48546f58e84d5db35923b", "aad7bc6273d52454832597c3d66e25731d8eba30d8fb92a97588f2ba8cadad47"),
    "pairwise_wall83": ("d3435f689de644a982fe6496441400a32ef29269", "06a01a521241157263a72b3d90539bfbbc74c9a367603136efb173165c363187"),
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


BASE = load_module("rank11_split_pencil_base_for_k83_adjacent", BASE_PATH)


def adjacent_weighted_cap(
    kprime: int,
    m: int,
    union: int,
    dimension: int,
    support: int,
    weights: dict[int, int],
) -> int:
    require(2 <= support <= dimension - 1, "dimension range")
    outside = m - union
    residual = kprime - union - dimension
    require(residual >= 0 and outside >= residual + support - 1, "residual")
    wd = weights[support] * comb(m - support, 11 - support)
    wn = weights[support + 1] * comb(m - support - 1, 10 - support)
    total = 0
    for inside in range(support - 1):
        choices = comb(union, inside)
        low = choices * residual * comb(outside, support - 1 - inside) // (support - inside)
        rhs = choices * residual * comb(outside, support - inside)
        coefficient = outside - residual - support + 1 + inside
        slope = (support + 1 - inside) * wd - coefficient * wn
        total += (wn * rhs + max(slope, 0) * low) // (support + 1 - inside)
    count_d = comb(union, support - 1) * residual + comb(union, support)
    count_next = (
        comb(union, support - 1) * residual * outside // 2
        + comb(union, support) * residual
        + comb(union, support + 1)
    )
    return total + wd * count_d + wn * count_next


def validate(data: object) -> dict[str, object]:
    require(isinstance(data, dict), "manifest object")
    require(data["schema"] == "kb-mca-rank11-k83-adjacent-support-payment-v1", "schema")
    require(data["exact_parent"] == "6b4902ccc5b4df02dddaea4969f3278dfc829953", "parent")
    require(data["previous_packet_sha256"] == "b5ef760938b36d09877fcda1d87c597de4f553a193af0050c05ddf24bfda2523", "previous packet")
    source = data["source_prize_dag"]
    require(source["commit"] == "f6849a90abfa9c8fe2e7b62dfbd2e510165957d1", "source commit")
    require(set(source["nodes"]) == set(SOURCE_PINS), "source nodes")
    for key, (tree, contract) in SOURCE_PINS.items():
        require(source["nodes"][key]["tree"] == tree, f"source tree {key}")
        require(source["nodes"][key]["contract_sha256"] == contract, f"source contract {key}")

    theorem = data["fixed_union_theorem"]
    require(theorem["dimension_range"] == "2<=d<=g-1", "dimension hypothesis")
    require(theorem["inside_range"] == "0<=i<=d-2", "inside range")
    require(theorem["composition"] == "support-disjoint adjacent pairs only", "composition")
    weights = {int(key): value for key, value in data["weights"].items()}
    for row in theorem["k83_specializations"]:
        value = adjacent_weighted_cap(
            83, 67555, row["union"], row["dimension"],
            row["support_pair"][0], weights,
        )
        require(value == row["weighted_cap"], "weighted specialization")

    row = data["k83"]
    require((row["q"], row["m"], row["n"]) == (73, 67555, 1048659), "row parameters")
    require((row["lanes"], row["jobs"]) == (73, 146), "coverage")
    require(row["ordinary_raw_rows"] == 7 * row["ordinary_units"], "ordinary rows")
    require(sum((73 - offset) * 5476 for offset in range(1, 73)) == 14390928, "offset units")
    require(row["completion_premium"] + row["premium_ceiling_margin"] == row["safe_premium_ceiling"], "premium margin")
    require(row["premium_ceiling_margin"] > 0, "positive margin")

    kprime, m, n = 83, row["m"], row["n"]
    chart = max(
        BASE.integral_core_offset_row(kprime, core)["chart"]
        for core in range(9, kprime)
    )
    marks = comb(n, 9) * chart
    kernel = BASE.refined_kernel_capacity(kprime)
    records = data["record_floor"]
    full = (marks + records * row["completion_premium"]) // 55
    demand = records * comb(m, 11) - comb(n, 11)
    ceiling = (
        records * 55 * comb(m, 11) - 55 * comb(n, 11)
        - 55 * kernel - marks - 1
    ) // records
    require(marks == row["rank_nine_marks"], "marks")
    require(kernel == row["kernel_capacity"], "kernel")
    require(full == row["full_rank_capacity"], "full capacity")
    require(full + kernel == row["total_capacity"], "total capacity")
    require(demand == row["required_component_incidence"], "demand")
    require(demand - full - kernel == row["gap"] > 0, "gap")
    require(ceiling == row["safe_premium_ceiling"], "ceiling")

    claims = data["claims"]
    require(claims["rank9_closed_prefix"] == [10, 83], "closed prefix")
    require(claims["rank9_remaining_interval"] == [84, 15528], "remaining interval")
    require(claims["first_pairwise_atlas_wall"] == 83, "method wall")
    require(claims["first_open_rank9_row"] == 84, "first open row")
    require(not claims["rank11_paid"] and not claims["KoalaBear_closed"] and not claims["prize_problems_closed"], "nonclaims")
    require(len(data["captures"]) == 4 and all(len(item[1]) == 64 for item in data["captures"]), "captures")
    return {"closed_prefix": [10, 83], "premium": row["completion_premium"], "margin": row["premium_ceiling_margin"], "gap": row["gap"]}


def tamper_selftest(data: dict) -> int:
    mutations = [
        lambda item: item["source_prize_dag"].__setitem__("commit", "0" * 40),
        lambda item: item["fixed_union_theorem"]["k83_specializations"][0].__setitem__("weighted_cap", 0),
        lambda item: item["k83"].__setitem__("completion_premium", item["k83"]["completion_premium"] + 1),
        lambda item: item["k83"].__setitem__("gap", -1),
        lambda item: item["claims"].__setitem__("first_open_rank9_row", 83),
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
