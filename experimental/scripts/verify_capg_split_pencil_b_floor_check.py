#!/usr/bin/env python3
"""Independent checker for the capg split-pencil base-field floor audit."""
from __future__ import annotations

import argparse
import itertools
import json
import math
import re
import sys
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)

CERT_REL = Path("experimental/data/certificates/capg-split-pencil-b/capg_split_pencil_b_floor.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
N_ROWS = {
    "oracle_f7_n6_k3_m4": (7, 6, 3, 4, 2, (2,)),
    "f17_n16_k8_m10_qp2": (17, 16, 8, 10, 2, (3, 4)),
    "f17_n16_k8_m10_qp4": (17, 16, 8, 10, 4, (3, 4)),
    "f17_n16_k6_m9_qp4": (17, 16, 6, 9, 4, (4, 5)),
    "f97_n16_k8_m10_qp2": (97, 16, 8, 10, 2, (3, 4)),
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ceil_div(num: int, den: int) -> int:
    return (num + den - 1) // den


def element_order(x: int, p: int) -> int:
    y = 1
    for i in range(1, p):
        y = (y * x) % p
        if y == 1:
            return i
    raise AssertionError("order not found")


def subgroup_by_order(p: int, n: int) -> list[int]:
    return sorted(x for x in range(1, p) if element_order(x, p) in divisors(n))


def divisors(n: int) -> set[int]:
    return {d for d in range(1, n + 1) if n % d == 0}


def locator_prefix_by_multiplication(support: tuple[int, ...], prefix_len: int, p: int) -> tuple[int, ...]:
    coeffs = [1]
    for a in support:
        nxt = [0] * (len(coeffs) + 1)
        for i, c in enumerate(coeffs):
            nxt[i] = (nxt[i] - a * c) % p
            nxt[i + 1] = (nxt[i + 1] + c) % p
        coeffs = nxt
    degree = len(support)
    return tuple(coeffs[degree - r] % p for r in range(1, prefix_len + 1))


def recompute_profile(row_id: str, d1: int) -> dict[str, int | bool]:
    p, n, k, m, ext, _dvals = N_ROWS[row_id]
    w = m - k
    boundary = d1 == w + 1
    m_prime = k - 1 + d1
    level_size = m if boundary else m_prime
    prefix_len = w if boundary else d1 - 1
    multiplier = 1 if boundary else math.comb(m_prime, m)
    expected = ceil_div(math.comb(n, level_size), p**prefix_len)
    domain = subgroup_by_order(p, n)
    counts: dict[tuple[int, ...], int] = {}
    for support in itertools.combinations(domain, level_size):
        key = locator_prefix_by_multiplication(support, prefix_len, p)
        counts[key] = counts.get(key, 0) + 1
    heaviest_count = max(counts.values())
    m_b = multiplier * expected
    observed = multiplier * heaviest_count
    q = p**ext
    omega = n - m
    q_num = math.comb(n, omega)
    q_den = 1 if w <= 1 else q ** (w - 1)
    return {
        "fiber_floor_ceiling": expected,
        "heaviest_prefix_count": heaviest_count,
        "M_B_integer_with_ceiling": m_b,
        "observed_base_field_census_lower": observed,
        "q_generic_below_M_B_integer": q_num < m_b * q_den,
    }


def check_source_labels(root: Path) -> None:
    text = (root / RAW_REL).read_text(encoding="utf-8")
    for label in ("prop:capg-census-floor", "prob:capg-split-pencil-B", "rem:capg-subfield-scope"):
        if re.search(r"\\label(?:\[[^]]+\])?\{" + re.escape(label) + r"\}", text) is None:
            raise AssertionError(f"missing label {label}")


def check() -> None:
    root = repo_root()
    check_source_labels(root)
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    all_profiles = cert["oracle_gate"]["profiles"] + cert["profiles"]
    for profile in all_profiles:
        expected = recompute_profile(profile["row_id"], profile["d1"])
        for key, val in expected.items():
            if profile[key] != val:
                raise AssertionError(f"{profile['row_id']} d1={profile['d1']} {key}: {profile[key]} != {val}")
    if cert["summary"]["full_split_pencil_upper_bound_tested"]:
        raise AssertionError("scope flag drifted")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    print("capg split-pencil-B floor independent check PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
