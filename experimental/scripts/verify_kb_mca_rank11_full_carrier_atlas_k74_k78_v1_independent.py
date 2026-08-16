#!/usr/bin/env python3
"""Independent payment audit for the compact K'=74..78 atlas packet."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-full-carrier-atlas-k74-k78-v1/manifest.json"
EXPECTED_SHA256 = "20dff5ce1c9634f9cd99e2cbacd4809fc860894f4549265a6f8b69176c0843c4"
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
base = load_module("rank11_split_pencil_base_for_k74_k78_independent", BASE_PATH)
records = data["record_floor"]
gaps = {}

for kprime in range(74, 79):
    row = data["rows"][str(kprime)]
    m, n = 67472 + kprime, 1048576 + kprime
    chart = max(
        base.integral_core_offset_row(kprime, core)["chart"]
        for core in range(9, kprime)
    )
    marks = comb(n, 9) * chart
    kernel = base.refined_kernel_capacity(kprime)
    full = (marks + records * row["completion_premium"]) // 55
    demand = records * comb(m, 11) - comb(n, 11)
    assert marks == row["rank_nine_marks"]
    assert kernel == row["kernel_capacity"]
    assert full == row["full_rank_capacity"]
    assert full + kernel == row["total_capacity"]
    assert demand == row["required_component_incidence"]
    assert demand - full - kernel == row["gap"] > 0
    assert row["safe_premium_ceiling"] - row["completion_premium"] == row["premium_ceiling_margin"] > 0
    assert row["safe_premium_ceiling"] - row["reroute_maximum"] == row["reroute_minimum_margin"] > 0
    assert all(lane["maximum"] < row["completion_premium"] for lane in row["geometry_lanes"])
    gaps[str(kprime)] = row["gap"]

assert data["claims"]["rank9_closed_prefix"] == [10, 78]
assert data["claims"]["rank9_remaining_interval"] == [79, 15528]
assert not data["claims"]["rank11_paid"]
assert not data["claims"]["KoalaBear_closed"]

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "rows": list(range(74, 79)),
    "gaps": gaps,
    "closed_prefix": [10, 78],
}, sort_keys=True))
