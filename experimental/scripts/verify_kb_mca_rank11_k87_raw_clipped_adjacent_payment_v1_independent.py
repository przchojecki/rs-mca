#!/usr/bin/env python3
"""Independent coverage, theorem, and arithmetic audit for K'=87."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k87-raw-clipped-adjacent-payment-v1/manifest.json"
EXPECTED_SHA256 = "ec81aa702181ba7a683e9f2a1afeb942a968c7d0232d6e3e7f3e44669d3f0f8a"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"
DEFICITS = {2: 36, 3: 28, 4: 21, 5: 15, 6: 10, 7: 6, 8: 3, 9: 1}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arithmetic_sum(first: int, last: int) -> int:
    return (last - first + 1) * (first + last) // 2


def upper_orientation_optimum(spec: dict[str, int]) -> Fraction:
    kprime, m = spec["kprime"], spec["m"]
    union, dimension = spec["union"], spec["vanishing_dimension"]
    support = spec["lower_support"]
    raw_low, raw_high = spec["lower_circuit_cap"], spec["upper_circuit_cap"]
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
    full_low = direct_low + sum(row[4] for row in rows)
    free_high = Fraction(direct_high) + sum(
        Fraction(row[3] - row[2] * row[4], row[1]) for row in rows
    )
    ordered = sorted(rows, key=lambda row: Fraction(row[1], row[2]))
    maximum_high = min(
        Fraction(raw_high),
        Fraction(direct_high) + sum(Fraction(row[3], row[1]) for row in rows),
    )
    candidates = {Fraction(0), maximum_high}
    if 0 <= free_high <= maximum_high:
        candidates.add(free_high)
    start, current_low = free_high, Fraction(full_low)
    for _, high_coefficient, low_coefficient, _, low_cap in ordered:
        width = Fraction(low_coefficient * low_cap, high_coefficient)
        end = start + width
        clipped_end = min(end, maximum_high)
        if start <= maximum_high:
            candidates.update((start, clipped_end))
            crossing = start + (current_low - raw_low) / Fraction(high_coefficient, low_coefficient)
            if start <= crossing <= clipped_end:
                candidates.add(crossing)
        current_low -= low_cap
        start = end

    def evaluate(total_high: Fraction) -> Fraction:
        extra = max(Fraction(0), total_high - free_high)
        loss_low = Fraction(0)
        for _, high_coefficient, low_coefficient, _, low_cap in ordered:
            width = Fraction(low_coefficient * low_cap, high_coefficient)
            used = min(extra, width)
            loss_low += Fraction(high_coefficient, low_coefficient) * used
            extra -= used
        assert extra == 0
        total_low = min(Fraction(raw_low), Fraction(full_low) - loss_low)
        weight_low = DEFICITS[support] * comb(m - support, 11 - support)
        weight_high = DEFICITS[support + 1] * comb(m - support - 1, 10 - support)
        return weight_low * total_low + weight_high * total_high

    return max(evaluate(candidate) for candidate in candidates)


raw_bytes = MANIFEST.read_bytes()
assert hashlib.sha256(raw_bytes).hexdigest() == EXPECTED_SHA256
data = json.loads(raw_bytes)
base = load_module("rank11_split_pencil_base_for_k87_raw_clipped_audit", BASE_PATH)

assert data["schema"] == "kb-mca-rank11-k87-raw-clipped-adjacent-payment-v1"
assert data["exact_parent"] == "7214947e5f7bd2b350f056ee2bbf75c5c4effd06"
assert data["previous_packet_sha256"] == "d0869e5755252d08a59bfe763fd33c5032796ebc67ca410c7432d98d05762072"
source = data["source_prize_dag"]
assert source["commit"] == "b869fb9dd2e740e323bee74e7ee72475905901f5"
assert source["row_node"]["tree"] == "1c00acd2b2293b97623bbbec695d98aa8689d218"
assert source["row_node"]["contract_sha256"] == "fc0699db0b33a5ff6a6fe04b918e5cbd5eefe3e9b29b9acd7816880b31cf7c88"
assert source["theorem_node"]["tree"] == "f1e826876806f3e30287f4e64d86f655714af081"

theorem = data["raw_clipped_theorem"]
assert "extension factors" in theorem["claim"]
assert "only support-disjoint" in theorem["composition_rule"]
spec = theorem["k87_specialization"]
optimum = upper_orientation_optimum(spec)
assert optimum == Fraction(spec["weighted_optimum_numerator"], spec["weighted_optimum_denominator"])
assert optimum.denominator == 3
assert optimum.numerator // optimum.denominator == spec["weighted_optimum_floor"]

coverage = data["coverage"]
ordinary = coverage["ordinary"]
raw = coverage["raw_offsets"]
clipped = coverage["raw_clipped_residual"]
assert ordinary["raw_rows"] == 7 * ordinary["source_units"]
assert ordinary["primary_geometry_rows"] == ordinary["audit_geometry_rows"]
all_offset_units = 6084 * arithmetic_sum(1, 76)
clipped_source_units = 6084 * arithmetic_sum(34, 76)
assert raw["source_units_per_implementation"] == all_offset_units
assert raw["raw_rows_per_implementation"] == 7 * all_offset_units
assert raw["raw_safe_units_per_implementation"] + clipped["unsafe_units_per_implementation"] == all_offset_units
assert clipped["source_units_per_implementation"] == clipped_source_units
assert clipped["lanes"] == 43 and clipped["jobs"] == 86
assert "support-disjoint" in clipped["rule"]

ranges = data["raw_clipped_captures"]
assert [(item["offsets"][0], item["offsets"][1]) for item in ranges] == [
    (1, 4), (5, 12), (13, 20), (21, 28), (29, 36), (37, 43)
]
assert len({item["app_id"] for item in data["captures"] + ranges}) == 9
assert data["raw_clipped_merged_sha256"] == "6f8064320850e0009c18c967e2b61ec5b4d77c51e1c2afb4bee6fc41921e5cd8"

row = data["k87"]
frontier = data["frontier"]
records, kprime, m, n = data["record_floor"], 87, row["m"], row["n"]
assert (row["q"], m, n) == (77, 67559, 1048663)
chart = max(base.integral_core_offset_row(kprime, core)["chart"] for core in range(9, kprime))
marks = comb(n, 9) * chart
kernel = base.refined_kernel_capacity(kprime)
full = (marks + records * frontier["completion_premium"]) // 55
demand = records * comb(m, 11) - comb(n, 11)
numerator = records * 55 * comb(m, 11) - 55 * comb(n, 11) - 55 * kernel - marks - 1
ceiling, remainder = divmod(numerator, records)
assert (marks, kernel, full, full + kernel, demand, demand - full - kernel) == (
    row["rank_nine_marks"], row["kernel_capacity"], row["full_rank_capacity"],
    row["total_capacity"], row["required_component_incidence"], row["gap"],
)
assert (ceiling, remainder) == (frontier["safe_premium_ceiling"], row["ceiling_remainder"])
assert ceiling - frontier["completion_premium"] == frontier["premium_ceiling_margin"] > 0
assert row["gap"] > 0
assert data["claims"]["rank9_closed_prefix"] == [10, 87]
assert data["claims"]["rank9_remaining_interval"] == [88, 15528]
assert data["claims"]["first_open_rank9_row"] == 88
assert not data["claims"]["prize_problems_closed"]

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "closed_prefix": [10, 87],
    "first_open_rank9_row": 88,
    "theorem_orientation": "upper-support",
    "theorem_floor": spec["weighted_optimum_floor"],
    "margin": frontier["premium_ceiling_margin"],
    "gap": row["gap"],
    "ceiling_remainder": remainder,
}, sort_keys=True))
