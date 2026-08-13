#!/usr/bin/env python3
"""Independent python-flint rank and integer replay."""

import json
from pathlib import Path

from flint import nmod_mat


root = Path(__file__).resolve().parents[2]
manifest = json.loads((root / "experimental/data/certificates/kb-mca-v4-guarded-record-local-core-owner-route-cut-v1/manifest.json").read_text())
fixture = manifest["fixture"]
p = fixture["field"]
domain = fixture["domain"]
k = fixture["k"]
u = fixture["received_line"]["u"]
v = fixture["received_line"]["v"]
minima = []
for item in fixture["explanations"]:
    slope = item["slope"]
    word = [(a + slope * b) % p for a, b in zip(u, v)]
    for s in range(6):
        rows = [
            [(value * pow(x, j, p)) % p for j in range(s + 1)]
            + [(-pow(x, j, p)) % p for j in range(s + k)]
            for x, value in zip(domain, word)
        ]
        matrix = nmod_mat(rows, p)
        if matrix.rank() < matrix.ncols():
            minima.append(s)
            break
assert minima == [3] * 7
guard = manifest["deployed_guard"]
assert guard["near_rational_2w"] == 134944
assert guard["joint_charge"] == 134975
assert guard["remaining_after_both"] == 274980728111260112
assert guard["pr1160_d1_upper"] < guard["balanced_guard"]
print("KB_MCA_V4_GUARDED_CORE_OWNER_FLINT_PASS d1=%s joint_charge=%d remaining=%d" % (minima, guard["joint_charge"], guard["remaining_after_both"]))
