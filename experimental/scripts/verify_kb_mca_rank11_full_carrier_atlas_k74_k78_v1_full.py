#!/usr/bin/env python3
"""Reconstruct one compact K'=74..78 frontier and complete atlas reroute."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import tarfile
from pathlib import Path


ARCHIVES = list(Path(".").glob("*.tar.gz"))
ROOT = Path("repo") if ARCHIVES else Path(__file__).resolve().parents[2]
if ARCHIVES:
    with tarfile.open(ARCHIVES[0], "r:gz") as archive:
        archive.extractall(ROOT, filter="data")
PRIMARY_PATH = ROOT / "experimental/scripts/verify_kb_mca_rank11_full_carrier_atlas_k74_k78_v1.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PRIMARY = load_module("rank11_k74_k78_primary_for_full_replay", PRIMARY_PATH)
ATLAS = PRIMARY.ATLAS
BASE = ATLAS.BASE


def defect_tuple(label: str) -> tuple[int, int, int, int]:
    return tuple(
        int(re.search(rf"s{support}=([0-9]+)", label).group(1))
        for support in range(2, 6)
    )


def position23_group(kprime: int, baseline: dict[int, int]):
    q = kprime - 10
    ordinary = {}
    steps = {value: [] for value in range(1, 7)}
    carrier32 = []
    for s2 in range(q + 1):
        for s3 in range(q + 1):
            vector = BASE.carrier_base23_vector(kprime, baseline, s2, s3)
            m2, m3 = q - s2, q - s3
            if m2 > 0 and m3 > 0 and m3 <= m2:
                if s2 + s3 < q:
                    continue
                b2, b3 = m2 + 1, m3 + 2
                for name, union, dimension in (
                    ("T23", b2 + b3, 7),
                    ("A23", b2 + b3 - 1, 8),
                ):
                    charged = BASE.carrier_charged_vector(kprime, vector, union, dimension)
                    ordinary[charged] = f"s2={s2}/s3={s3}/{name}"
            elif m2 > 0 and m3 == 30 and m2 < 30:
                carrier32.append((s2, s3, vector))
            elif m2 > 0 and m3 - m2 in steps:
                steps[m3 - m2].append((s2, s3, vector))
            else:
                ordinary[vector] = f"s2={s2}/s3={s3}/U23"
    return BASE.componentwise_maximal_vectors(ordinary), steps, carrier32


def reconstruct(kprime: int, row: dict) -> dict[str, object]:
    q = kprime - 10
    baseline = ATLAS.baseline_caps(kprime)
    front23, steps, carrier32 = position23_group(kprime, baseline)
    exact45, _, front45 = BASE.carrier_exact45_rows(kprime, baseline)
    _, high = BASE.high_support_group(kprime, baseline)
    unsafe_by_defects = {}
    safe_maximum = (-1, "")
    evaluations = 0

    def retain(label: str, caps: tuple[int, ...]) -> None:
        nonlocal evaluations, safe_maximum
        evaluations += 1
        value = ATLAS.premium(caps)
        defects = defect_tuple(label)
        if value > row["safe_premium_ceiling"]:
            previous = unsafe_by_defects.get(defects)
            if previous is None or value > previous[0]:
                unsafe_by_defects[defects] = (value, label)
        elif value > safe_maximum[0]:
            safe_maximum = (value, label)

    for left_name, left in front23:
        for middle_name, middle in front45:
            local = ATLAS.combine(left, middle)
            for high_name, high_vector in high:
                retain(f"{left_name}/{middle_name}/{high_name}/ordinary", ATLAS.combine(local, high_vector))

    for s2, s3, left in carrier32:
        for s4, s5, middle in exact45:
            if (q - s4, q - s5) == (31, 31):
                continue
            local = ATLAS.combine(left, middle)
            for high_name, high_vector in high:
                retain(f"s2={s2}/s3={s3}/s4={s4}/s5={s5}/{high_name}/carrier32_plain", ATLAS.combine(local, high_vector))

    for offset, rows in steps.items():
        for s2, s3, left in rows:
            m2 = q - s2
            for s4, s5, middle in exact45:
                if q - s4 > m2:
                    continue
                local = ATLAS.combine(left, middle)
                for high_name, high_vector in high:
                    retain(f"s2={s2}/s3={s3}/s4={s4}/s5={s5}/{high_name}/offset{offset}_plain", ATLAS.combine(local, high_vector))

    unsafe = sorted(unsafe_by_defects)
    ranked = sorted(
        (value, defects, label)
        for defects, (value, label) in unsafe_by_defects.items()
    )
    digest = hashlib.sha256(json.dumps(unsafe, separators=(",", ":")).encode()).hexdigest()
    assert evaluations == row["plain_evaluations"]
    assert len(unsafe) == row["plain_unsafe_cells"]
    assert digest == row["unsafe_tuple_sha256"]
    assert ranked[-1][:2] == (row["unsafe_maximum"], tuple(row["unsafe_maximum_defects"]))
    assert ranked[0][:2] == (row["unsafe_minimum"], tuple(row["unsafe_minimum_defects"]))
    assert safe_maximum == (row["completion_premium"], row["safe_maximum_label"])

    routed = ATLAS.reroute_row(kprime, unsafe)
    assert routed["evaluations"] == row["reroute_evaluations"]
    assert routed["maximum"] == row["reroute_maximum"]
    assert tuple(routed["active_defects"]) == tuple(row["reroute_active_defects"])
    assert routed["active_geometry"] == row["reroute_active_geometry"]
    assert row["safe_premium_ceiling"] - routed["maximum"] == row["reroute_minimum_margin"] > 0
    assert all(value < row["safe_premium_ceiling"] for value in routed["cell_maxima"])
    return {
        "kprime": kprime,
        "plain_evaluations": evaluations,
        "unsafe_cells": len(unsafe),
        "unsafe_tuple_sha256": digest,
        "reroute_evaluations": routed["evaluations"],
        "reroute_maximum": routed["maximum"],
        "gap": row["gap"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--row", type=int, choices=range(74, 79), required=True)
    args = parser.parse_args()
    raw = PRIMARY.MANIFEST.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PRIMARY.MANIFEST_SHA256
    data = json.loads(raw)
    PRIMARY.validate(data)
    print(json.dumps(reconstruct(args.row, data["rows"][str(args.row)]), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
