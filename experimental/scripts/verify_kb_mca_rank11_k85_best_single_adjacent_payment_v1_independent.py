#!/usr/bin/env python3
"""Independent finite-coverage and arithmetic audit of the K'=85 payment."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k85-best-single-adjacent-payment-v1/manifest.json"
EXPECTED_SHA256 = "ae598632a204181a0ef0cc8895c077af22d16587f2ab209b7cebb3e26c2cb5ee"
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
base = load_module("rank11_split_pencil_base_for_k85_adjacent_audit", BASE_PATH)

assert data["schema"] == "kb-mca-rank11-k85-best-single-adjacent-payment-v1"
assert data["exact_parent"] == "cba05d4ca6c8cb08fd3444a72a55f298fe47b0bc"
assert data["previous_packet_sha256"] == "4317c574e73626e2491e3dcfc777ab7e09c98333493f9161eb432a5ecfa355e3"
source = data["source_prize_dag"]
assert source["commit"] == "c4fdef465aabc8abae7a18b9694bed9cf34e362b"
assert source["node"]["tree"] == "fc59f079d87a20f6c71f9b0b78345c2b518a0c44"
assert source["node"]["contract_sha256"] == "0a4dd3003a644b7e0e0354e34fbfb797590d193ea7f563f96507cf749deb7600"

coverage = data["coverage"]
ordinary = coverage["ordinary"]
raw = coverage["raw_offsets"]
residual = coverage["best_single_residual"]
assert ordinary["raw_rows"] == 7 * ordinary["source_units"]
all_offset_units = 5776 * arithmetic_sum(1, 74)
residual_source_units = 5776 * arithmetic_sum(34, 74)
assert raw["source_units_per_implementation"] == all_offset_units
assert raw["raw_rows_per_implementation"] == 7 * all_offset_units
assert raw["raw_safe_units_per_implementation"] + residual["unsafe_units_per_implementation"] == all_offset_units
assert residual["source_units_per_implementation"] == residual_source_units
assert residual["lanes"] == 41 and residual["jobs"] == 82
assert "no simultaneous" in residual["rule"]

row = data["k85"]
frontier = data["frontier"]
records, kprime, m, n = data["record_floor"], 85, row["m"], row["n"]
assert (row["q"], m, n) == (75, 67557, 1048661)
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
    ("route_pilot", "ap-d16UIhECIz7nYzMEAZr8d7"),
    ("raw_threshold_wave", "ap-rTfQtYZuTdgjfk5IWhal5W"),
    ("best_single_wave", "ap-avKuaBEl3bNsvVug235bXS"),
    ("component_payment", "ap-9R6TUWXTLwS11AiqMsAem5"),
]
assert data["claims"]["rank9_closed_prefix"] == [10, 85]
assert data["claims"]["rank9_remaining_interval"] == [86, 15528]
assert data["claims"]["first_open_rank9_row"] == 86
assert not data["claims"]["prize_problems_closed"]

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "closed_prefix": [10, 85],
    "first_open_rank9_row": 86,
    "margin": frontier["premium_ceiling_margin"],
    "gap": row["gap"],
    "ceiling_remainder": remainder,
}, sort_keys=True))
