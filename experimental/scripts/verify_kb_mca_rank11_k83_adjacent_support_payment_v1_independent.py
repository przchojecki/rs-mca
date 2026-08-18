#!/usr/bin/env python3
"""Independent arithmetic audit of the K'=83 adjacent-support payment."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-k83-adjacent-support-payment-v1/manifest.json"
EXPECTED_SHA256 = "99e01210543223ae45aa8e1f88a49c11951a0b37fd2f3496c1ce1e886d04a3fd"
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
base = load_module("rank11_split_pencil_base_for_k83_adjacent_audit", BASE_PATH)
weights = {int(key): value for key, value in data["weights"].items()}


def vertex_cap(union: int, dimension: int, support: int) -> int:
    kprime, m = 83, 67555
    residual, outside = kprime - union - dimension, m - union
    wd = weights[support] * comb(m - support, 11 - support)
    wn = weights[support + 1] * comb(m - support - 1, 10 - support)
    answer = 0
    for inside in range(support - 1):
        a = support + 1 - inside
        b = outside - residual - support + 1 + inside
        rhs = comb(union, inside) * residual * comb(outside, support - inside)
        xmax = comb(union, inside) * residual * comb(outside, support - 1 - inside) // (support - inside)
        values = [Fraction(wn * rhs, a)]
        values.append(Fraction(wd * xmax, 1) + Fraction(wn * (rhs - b * xmax), a))
        answer += max(values).__floor__()
    answer += wd * (comb(union, support - 1) * residual + comb(union, support))
    answer += wn * (
        comb(union, support - 1) * residual * outside // 2
        + comb(union, support) * residual
        + comb(union, support + 1)
    )
    return answer


for item in data["fixed_union_theorem"]["k83_specializations"]:
    assert vertex_cap(item["union"], item["dimension"], item["support_pair"][0]) == item["weighted_cap"]

row = data["k83"]
records, kprime, m, n = data["record_floor"], 83, row["m"], row["n"]
chart = max(base.integral_core_offset_row(kprime, core)["chart"] for core in range(9, kprime))
marks = comb(n, 9) * chart
kernel = base.refined_kernel_capacity(kprime)
full = (marks + records * row["completion_premium"]) // 55
demand = records * comb(m, 11) - comb(n, 11)
numerator = records * 55 * comb(m, 11) - 55 * comb(n, 11) - 55 * kernel - marks - 1
ceiling, remainder = divmod(numerator, records)
assert (marks, kernel, full, full + kernel, demand, demand - full - kernel) == (
    row["rank_nine_marks"], row["kernel_capacity"], row["full_rank_capacity"],
    row["total_capacity"], row["required_component_incidence"], row["gap"],
)
assert ceiling == row["safe_premium_ceiling"]
assert ceiling - row["completion_premium"] == row["premium_ceiling_margin"] > 0
assert row["gap"] > 0 and 0 <= remainder < records
assert data["claims"]["rank9_closed_prefix"] == [10, 83]
assert data["claims"]["first_open_rank9_row"] == 84
assert not data["claims"]["prize_problems_closed"]

print(json.dumps({
    "manifest_sha256": EXPECTED_SHA256,
    "closed_prefix": [10, 83],
    "first_open_rank9_row": 84,
    "margin": row["premium_ceiling_margin"],
    "gap": row["gap"],
    "ceiling_remainder": remainder,
}, sort_keys=True))
