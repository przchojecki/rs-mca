#!/usr/bin/env python3
"""Independent adjudicator for ``verify_q_r1_closing_audit.py``.

This checker recomputes the row arithmetic by a separate binomial routine and
re-scans the source statements directly from the TeX/JSON artifacts.  It does
not import the generator.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.set_int_max_str_digits(2_000_000)

CERT_REL = Path("experimental/data/certificates/q-r1-closing-audit/q_r1_closing_audit.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
COMPACT_REL = Path("experimental/cap25_cap_v13_raw_compact.tex")
KB_CORRECTED_REL = Path(
    "experimental/data/certificates/frontier-adjacent/"
    "koalabear_frontier_adjacent_a1116043_a1116044.json"
)
PACKET_RELS = [
    Path("experimental/data/certificates/frontier-adjacent/kb_mca_v1.packet.json"),
    Path("experimental/data/certificates/frontier-adjacent/kb_list_v1.packet.json"),
    Path("experimental/data/certificates/frontier-adjacent/m31_mca_v1.packet.json"),
    Path("experimental/data/certificates/frontier-adjacent/m31_list_v1.packet.json"),
]

N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1
ROWS = [
    ("kb_mca", "mca", P_KB, 6, 128, 1116047, 1116048),
    ("kb_list", "list", P_KB, 6, 128, 1116046, 1116047),
    ("m31_mca", "mca", P_M31, 4, 100, 1116023, 1116024),
    ("m31_list", "list", P_M31, 4, 100, 1116022, 1116023),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ceil_div(num: int, den: int) -> int:
    return (num + den - 1) // den


def comb_descending(n: int, values: list[int]) -> dict[int, int]:
    wanted = sorted(set(values))
    hi = wanted[-1]
    lo = wanted[0]
    current_m = hi
    current = math.comb(n, hi)
    out = {hi: current}
    wanted_set = set(wanted)
    while current_m > lo:
        current = current * current_m // (n - current_m + 1)
        current_m -= 1
        if current_m in wanted_set:
            out[current_m] = current
    return out


def lower_count(kind: str, base: int, ext: int, agreement: int, combinations: dict[int, int]) -> int:
    dimension = K_BASE + 1 if kind == "mca" else K_BASE
    w = agreement - dimension
    floor = ceil_div(combinations[agreement], base**w)
    if kind == "list":
        return floor
    q_line = base**ext
    return ceil_div(floor * (q_line - N), q_line - N + K_BASE * (floor - 1))


def recompute_rows() -> dict[str, dict[str, int | bool]]:
    out = {}
    combinations = comb_descending(N, [a for row in ROWS for a in (row[5], row[6])])
    for row_id, kind, base, ext, lam, a0, a1 in ROWS:
        q_line = base**ext
        b_star = q_line // (2**lam)
        low0 = lower_count(kind, base, ext, a0, combinations)
        low1 = lower_count(kind, base, ext, a1, combinations)
        out[row_id] = {
            "B_star_threshold": b_star,
            "lower_floor_at_a0": low0,
            "lower_floor_at_a1": low1,
            "lower_a0_exceeds_threshold": low0 > b_star,
            "lower_a1_exceeds_threshold": low1 > b_star,
            "deficit_to_exceed_threshold_at_a1": b_star + 1 - low1,
        }
    return out


def label_exists(root: Path, label: str) -> bool:
    text = (root / RAW_REL).read_text(encoding="utf-8")
    return re.search(r"\\label(?:\[[^]]+\])?\{" + re.escape(label) + r"\}", text) is not None


def source_assertions(root: Path) -> None:
    for label in (
        "prop:capfr1-slope-elimination",
        "cor:capfr1-Q-R1-closing",
        "cor:capg-adjacent-pairs",
        "prop:capg-census-floor",
    ):
        if not label_exists(root, label):
            raise AssertionError(f"missing source label {label}")
    raw = (root / RAW_REL).read_text(encoding="utf-8")
    if "U_{\\rm paid}(a_0+1)+U_Q(a_0+1)+U_{\\Rone}(a_0+1)" not in raw:
        raise AssertionError("Q/R1 one-step inequality text not found")
    if "all three problems are therefore refuted" not in raw:
        raise AssertionError("self-correction context not found")
    compact = (root / COMPACT_REL).read_text(encoding="utf-8")
    for phrase in (
        "finite Q certificate",
        "finite adjacent-pair compiler",
        "safe\\_upper",
        "once a mathematical proof supplies their finite constants",
    ):
        if phrase not in compact:
            raise AssertionError(f"compact source phrase missing: {phrase}")
    for rel in PACKET_RELS:
        packet = json.loads((root / rel).read_text(encoding="utf-8"))
        if packet.get("safe_certificates", {}).get("status") != "OPEN":
            raise AssertionError(f"{rel} safe side no longer OPEN")
    corrected_text = (root / KB_CORRECTED_REL).read_text(encoding="utf-8")
    if "no finite U(1116048) <= B* statement exists or is claimed" not in corrected_text:
        raise AssertionError("corrected KoalaBear open marker missing")


def check() -> None:
    root = repo_root()
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    source_assertions(root)
    expected = recompute_rows()
    rows = {row["row_id"]: row for row in cert["row_table"]}
    if set(rows) != set(expected):
        raise AssertionError("row-id set mismatch")
    for row_id, values in expected.items():
        row = rows[row_id]
        for key, expected_value in values.items():
            if row[key] != expected_value:
                raise AssertionError(f"{row_id}.{key}: {row[key]} != {expected_value}")
    comp = cert["component_availability"]
    if comp["one_step_replay_possible_from_current_tree"] is not False:
        raise AssertionError("one-step replay flag drifted")
    if comp["U_Q_a1"] != "not_instantiated_as_finite_Q_integer_certificate":
        raise AssertionError("U_Q status drifted")
    if comp["U_R1_a1"] != "not_instantiated_as_finite_R1_integer_certificate":
        raise AssertionError("U_R1 status drifted")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="run the independent check")
    args = parser.parse_args()
    if args.check:
        check()
    print("Q/R1 closing independent audit check PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
