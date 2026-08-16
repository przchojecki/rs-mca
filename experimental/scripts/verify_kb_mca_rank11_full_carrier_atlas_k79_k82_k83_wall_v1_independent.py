#!/usr/bin/env python3
"""Independent payment audit for K'=79..82 and the K'=83 route cut."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-full-carrier-atlas-k79-k82-k83-wall-v1/manifest.json"
EXPECTED_SHA256 = "b5ef760938b36d09877fcda1d87c597de4f553a193af0050c05ddf24bfda2523"
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
base = load_module("rank11_split_pencil_base_for_k79_k83_independent", BASE_PATH)
records = data["record_floor"]
gaps = {}

for kprime in range(79, 83):
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
    ceiling = (
        records * 55 * comb(m, 11)
        - 55 * comb(n, 11)
        - 55 * kernel
        - marks
        - 1
    ) // records
    assert marks == row["rank_nine_marks"]
    assert kernel == row["kernel_capacity"]
    assert full == row["full_rank_capacity"]
    assert full + kernel == row["total_capacity"]
    assert demand == row["required_component_incidence"]
    assert demand - full - kernel == row["gap"] > 0
    assert ceiling == row["safe_premium_ceiling"]
    assert ceiling - row["completion_premium"] == row["premium_ceiling_margin"] > 0
    assert ceiling - row["reroute_maximum"] == row["reroute_minimum_margin"] > 0
    assert all(
        lane["maximum"] < row["completion_premium"]
        for lane in row["geometry_lanes"]
    )
    gaps[str(kprime)] = row["gap"]

wall = data["wall83"]
assert wall["pairwise_maximum"] + wall["pairwise_margin"] == wall["safe_premium_ceiling"]
assert wall["pairwise_margin"] < 0
assert [row["triple_union"] for row in wall["forced_intersection_rows"]] == [32, 31, 30, 29]
assert all(
    row["maximum"] == wall["pairwise_maximum"]
    and row["margin"] == wall["pairwise_margin"]
    for row in wall["forced_intersection_rows"]
)
assert all(
    row["baseline_premium"] + row["margin"] == row["safe_premium_ceiling"]
    and row["margin"] < 0
    for row in wall["branch_free_baseline"]
)
assert data["claims"]["rank9_closed_prefix"] == [10, 82]
assert data["claims"]["rank9_remaining_interval"] == [83, 15528]
assert data["claims"]["first_pairwise_atlas_wall"] == 83
assert not data["claims"]["rank11_paid"]
assert not data["claims"]["KoalaBear_closed"]

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "rows": list(range(79, 83)),
    "gaps": gaps,
    "closed_prefix": [10, 82],
    "wall83_deficit": -wall["pairwise_margin"],
}, sort_keys=True))
