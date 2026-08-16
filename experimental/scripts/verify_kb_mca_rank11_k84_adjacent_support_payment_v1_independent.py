#!/usr/bin/env python3
"""Independent arithmetic audit of the K'=84 adjacent-support payment."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k84-adjacent-support-payment-v1/manifest.json"
EXPECTED_SHA256 = "4317c574e73626e2491e3dcfc777ab7e09c98333493f9161eb432a5ecfa355e3"
BASE_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_dense_locator_split_pencil_v1.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


raw = MANIFEST.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256
data = json.loads(raw)
base = load_module("rank11_split_pencil_base_for_k84_adjacent_audit", BASE_PATH)

assert data["schema"] == "kb-mca-rank11-k84-adjacent-support-payment-v1"
assert data["previous_packet_sha256"] == "99e01210543223ae45aa8e1f88a49c11951a0b37fd2f3496c1ce1e886d04a3fd"
assert data["source_prize_dag"]["commit"] == "9a0baa42b35790f1e0d383e18dd721bcb7d9a86c"
assert data["source_prize_dag"]["node"]["tree"] == "354e3859f7654bcec417f2dcd92b506a9984a7b2"
assert data["source_prize_dag"]["node"]["contract_sha256"] == "6cdb8f6495f90001bafe26e656566f6483d8505f565a69ebe57d2a6717d07cd3"

coverage = data["coverage"]
assert coverage["lanes"] == 74 and coverage["jobs"] == 148
assert coverage["source_units"] == 457938 + sum((74 - offset) * 5625 for offset in range(1, 74))
assert coverage["raw_rows"] == 7 * coverage["source_units"]
assert coverage["ordinary_raw_rows"] == 7 * 457938
assert coverage["audit_geometry_rows"] >= coverage["primary_geometry_rows"] > 0

row = data["k84"]
frontier = data["frontier"]
records, kprime, m, n = data["record_floor"], 84, row["m"], row["n"]
assert (row["q"], m, n) == (74, 67556, 1048660)
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
assert ceiling == frontier["safe_premium_ceiling"]
assert ceiling - frontier["completion_premium"] == frontier["premium_ceiling_margin"] > 0
assert row["gap"] > 0 and 0 <= remainder < records
assert [(item["role"], item["app_id"], item["sha256"]) for item in data["captures"]] == [
    ("primary_wave", "ap-1oAXY3d5xqakObFjYF0Ck6", "884e7bc9ee9c78b49e1324bb3c11ca0ca3d6044114f2bc88dd4cee196b2c916a"),
    ("audit_wave", "ap-CE1YUXVUmNXrwze1lDP6Wn", "11420a74fbebe5f63d717e633c9914c9089c3fb92546051e267c03b60ee1a850"),
    ("compact_merger", "ap-UwcGaJZm4Wst0Ozq1NMRIp", "abc5638fba58fee000c0e8552ea449c4f8058713da3b784a989bf454235633a8"),
    ("component_payment", "ap-H3we0j1uIdfDebkyKPSRbR", "58b8a3077d2dc80444b91a9b0057f6ad47a9fd07a0bce0456904522cc4d054c5"),
]
assert data["claims"]["rank9_closed_prefix"] == [10, 84]
assert data["claims"]["rank9_remaining_interval"] == [85, 15528]
assert data["claims"]["first_open_rank9_row"] == 85
assert not data["claims"]["prize_problems_closed"]

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "closed_prefix": [10, 84],
    "first_open_rank9_row": 85,
    "margin": frontier["premium_ceiling_margin"],
    "gap": row["gap"],
    "ceiling_remainder": remainder,
}, sort_keys=True))
