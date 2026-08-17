#!/usr/bin/env python3
"""Independent finite-coverage and arithmetic audit of the K'=86 payment."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k86-best-single-adjacent-payment-v1/manifest.json"
EXPECTED_SHA256 = "d0869e5755252d08a59bfe763fd33c5032796ebc67ca410c7432d98d05762072"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arithmetic_sum(first: int, last: int) -> int:
    return (last - first + 1) * (first + last) // 2


raw_bytes = MANIFEST.read_bytes()
assert hashlib.sha256(raw_bytes).hexdigest() == EXPECTED_SHA256
data = json.loads(raw_bytes)
base = load_module("rank11_split_pencil_base_for_k86_adjacent_audit", BASE_PATH)

assert data["schema"] == "kb-mca-rank11-k86-best-single-adjacent-payment-v1"
assert data["exact_parent"] == "7356a104a4ec2d21f6c0fc32a3fb3c394cf5e8cf"
assert data["previous_packet_sha256"] == "ae598632a204181a0ef0cc8895c077af22d16587f2ab209b7cebb3e26c2cb5ee"
source = data["source_prize_dag"]
assert source["commit"] == "a0f03f3af3b8bffb303dfe8e0b338b40e49da5ee"
assert source["node"]["tree"] == "5d5e1503591ec1ebca92847538f3b1a7d6ef6dfb"
assert source["node"]["contract_sha256"] == "b318de9938264a3306372b473513b1975e6941204a39c03d07a5ff16b62e896f"

coverage = data["coverage"]
ordinary = coverage["ordinary"]
raw = coverage["raw_offsets"]
residual = coverage["best_single_residual"]
assert ordinary["raw_rows"] == 7 * ordinary["source_units"]
assert "broader incomplete pilot" in ordinary["custody_scope"]
all_offset_units = 5929 * arithmetic_sum(1, 75)
residual_source_units = 5929 * arithmetic_sum(34, 75)
assert raw["source_units_per_implementation"] == all_offset_units
assert raw["raw_rows_per_implementation"] == 7 * all_offset_units
assert raw["raw_safe_units_per_implementation"] + residual["unsafe_units_per_implementation"] == all_offset_units
assert residual["source_units_per_implementation"] == residual_source_units
assert residual["lanes"] == 42 and residual["jobs"] == 84
assert "no simultaneous" in residual["rule"]

row = data["k86"]
frontier = data["frontier"]
records, kprime, m, n = data["record_floor"], 86, row["m"], row["n"]
assert (row["q"], m, n) == (76, 67558, 1048662)
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
assert [(item["role"], item["app_id"]) for item in data["captures"]] == [
    ("ordinary_slice", "ap-OP9ryrK2YdHRg463E43ktv"),
    ("raw_threshold_wave", "ap-kjz4PvurdW9cunGO3pse1N"),
    ("best_single_wave", "ap-HSdSkI0KYmWfnz0jL0Bron"),
    ("component_payment", "ap-3mwC5dZ9yYxOTcOJx9JygE"),
]
assert data["claims"]["rank9_closed_prefix"] == [10, 86]
assert data["claims"]["rank9_remaining_interval"] == [87, 15528]
assert data["claims"]["first_open_rank9_row"] == 87
assert not data["claims"]["prize_problems_closed"]

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "closed_prefix": [10, 86],
    "first_open_rank9_row": 87,
    "margin": frontier["premium_ceiling_margin"],
    "gap": row["gap"],
    "ceiling_remainder": remainder,
}, sort_keys=True))
