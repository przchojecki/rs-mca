#!/usr/bin/env python3
"""Independent checker for the capg adjacent-pair margin audit."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.set_int_max_str_digits(2_000_000)

CERT_REL = Path("experimental/data/certificates/capg-adjacent-pairs/capg_adjacent_pair_margins.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
SCALE = 1000
N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1
ROWS = {
    "kb_mca": ("mca", P_KB, 6, 128, 1116047, 1116048),
    "kb_list": ("list", P_KB, 6, 128, 1116046, 1116047),
    "m31_mca": ("mca", P_M31, 4, 100, 1116023, 1116024),
    "m31_list": ("list", P_M31, 4, 100, 1116022, 1116023),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ceil_div(num: int, den: int) -> int:
    return (num + den - 1) // den


def comb_descending(n: int, values: list[int]) -> dict[int, int]:
    vals = sorted(set(values))
    current_m = vals[-1]
    current = math.comb(n, current_m)
    out = {current_m: current}
    wanted = set(vals)
    while current_m > vals[0]:
        current = current * current_m // (n - current_m + 1)
        current_m -= 1
        if current_m in wanted:
            out[current_m] = current
    return out


def lower(kind: str, base: int, ext: int, agreement: int, combos: dict[int, int]) -> int:
    dimension = K_BASE + 1 if kind == "mca" else K_BASE
    floor = ceil_div(combos[agreement], base ** (agreement - dimension))
    if kind == "list":
        return floor
    q_line = base**ext
    return ceil_div(floor * (q_line - N), q_line - N + K_BASE * (floor - 1))


def floor_log2_scaled(num: int, den: int, scale: int = SCALE) -> int:
    lhs = pow(num, scale)
    rhs_base = pow(den, scale)
    lo = -scale * (den.bit_length() + 2)
    hi = scale * (num.bit_length() + 2)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid >= 0:
            ok = lhs >= (rhs_base << mid)
        else:
            ok = (lhs << (-mid)) >= rhs_base
        if ok:
            lo = mid
        else:
            hi = mid
    return lo


def check_source_labels(root: Path) -> None:
    text = (root / RAW_REL).read_text(encoding="utf-8")
    for label in ("prop:capg-moved-frontier", "cor:capg-adjacent-pairs"):
        if re.search(r"\\label(?:\[[^]]+\])?\{" + re.escape(label) + r"\}", text) is None:
            raise AssertionError(f"missing label {label}")


def check() -> None:
    root = repo_root()
    check_source_labels(root)
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    combos = comb_descending(N, [a for row in ROWS.values() for a in (row[4], row[5])])
    by_id = {row["row_id"]: row for row in cert["rows"]}
    if set(by_id) != set(ROWS):
        raise AssertionError("row-id mismatch")
    for row_id, (kind, base, ext, lam, a0, a1) in ROWS.items():
        b_star = (base**ext) // (2**lam)
        low0 = lower(kind, base, ext, a0, combos)
        low1 = lower(kind, base, ext, a1, combos)
        rec = by_id[row_id]
        checks = {
            "B_star_threshold": b_star,
            "lower_floor_at_a0": low0,
            "lower_floor_at_a1": low1,
            "pass_margin_scaled_bits_floor": floor_log2_scaled(low0, b_star),
            "fail_margin_scaled_bits_floor": floor_log2_scaled(b_star, low1),
            "deficit_to_exceed_threshold_at_a1": b_star + 1 - low1,
        }
        for key, expected in checks.items():
            if rec[key] != expected:
                raise AssertionError(f"{row_id}.{key}: {rec[key]} != {expected}")
    if cert["summary"]["tightest_fail_margin_row"] != "m31_list":
        raise AssertionError("tightest row drift")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    print("capg adjacent-pair independent margin check PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
