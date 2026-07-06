#!/usr/bin/env python3
"""Independent checker for the toy primitive shift-pair ledger.

The generator groups locator coefficients.  This checker reconstructs the same
finite rows through power-sum signatures and tests periodicity by explicit
multiplication by subgroup elements of each candidate scale.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)

THEOREM_PROBLEM_ID = "prob:capg-shiftpairs / prob:capg-active-shiftpairs"
PROOF_STATUS = "AUDIT"
CERT_REL = Path("experimental/data/certificates/capg-shiftpairs/capg_shiftpairs_primitive_ledger.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")


@dataclass(frozen=True)
class Row:
    row_id: str
    p: int
    n: int
    w: int
    e: int
    removed_indices: tuple[int, ...] = ()


ROWS = [
    Row("oracle_f5_mu4_w1_e2", 5, 4, 1, 2),
    Row("f17_mu16_w1_e2", 17, 16, 1, 2),
    Row("f17_mu16_w2_e3", 17, 16, 2, 3),
    Row("f17_mu16_w3_e4", 17, 16, 3, 4),
    Row("f17_mu16_w2_e4", 17, 16, 2, 4),
    Row("f17_mu16_minus_one_w1_e2", 17, 16, 1, 2, (0,)),
    Row("f31_mu15_w2_e3", 31, 15, 2, 3),
    Row("f31_mu15_w4_e5", 31, 15, 4, 5),
    Row("f97_mu16_w2_e3", 97, 16, 2, 3),
    Row("f97_mu16_w3_e4", 97, 16, 3, 4),
]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def factor(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    prime_factors = factor(p - 1)
    for g in range(2, p):
        ok = True
        for r in prime_factors:
            if pow(g, (p - 1) // r, p) == 1:
                ok = False
                break
        if ok:
            return g
    raise AssertionError(f"no primitive root for F_{p}")


def subgroup_mu(p: int, n: int) -> list[int]:
    gen = primitive_root(p)
    step = pow(gen, (p - 1) // n, p)
    return [pow(step, i, p) for i in range(n)]


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def power_signature(indices: tuple[int, ...], values: list[int], p: int, w: int) -> tuple[int, ...]:
    if w >= p:
        raise AssertionError("power-sum route requires w < p")
    return tuple(sum(pow(values[i], j, p) for i in indices) % p for j in range(1, w + 1))


def scale_periodic_by_action(indices: tuple[int, ...], values: list[int], p: int, n: int, scale: int) -> bool:
    if len(indices) % scale != 0:
        return False
    index_by_value = {value: idx for idx, value in enumerate(values)}
    multiplier = values[n // scale]
    index_set = set(indices)
    for idx in indices:
        moved = index_by_value[(values[idx] * multiplier) % p]
        if moved not in index_set:
            return False
    return True


def common_scales_by_action(
    left: tuple[int, ...],
    right: tuple[int, ...],
    values: list[int],
    p: int,
    n: int,
) -> list[int]:
    out = []
    for scale in divisors(n):
        if scale < 2:
            continue
        if scale_periodic_by_action(left, values, p, n, scale) and scale_periodic_by_action(
            right, values, p, n, scale
        ):
            out.append(scale)
    return out


def enumerate_counts(row: Row) -> dict[str, int | None]:
    values = subgroup_mu(row.p, row.n)
    available = tuple(i for i in range(row.n) if i not in set(row.removed_indices))
    buckets: dict[tuple[int, ...], list[tuple[int, tuple[int, ...]]]] = {}
    for combo in itertools.combinations(available, row.e):
        sig = power_signature(combo, values, row.p, row.w)
        mask = sum(1 << i for i in combo)
        buckets.setdefault(sig, []).append((mask, combo))
    total = 0
    pullback = 0
    primitive = 0
    prototype_seen = 0
    for members in buckets.values():
        for left_mask, left in members:
            for right_mask, right in members:
                if left == right or (left_mask & right_mask):
                    continue
                scales = common_scales_by_action(left, right, values, row.p, row.n)
                total += 1
                if row.e == row.w + 1 and row.e in scales:
                    prototype_seen += 1
                if scales:
                    pullback += 1
                else:
                    primitive += 1
    expected = None
    if not row.removed_indices and row.e == row.w + 1 and row.n % row.e == 0:
        fibers = row.n // row.e
        expected = fibers * (fibers - 1)
    return {
        "sp_ordered_pairs": total,
        "pullback_pairs": pullback,
        "primitive_pairs": primitive,
        "prototype_expected_pairs": expected,
        "prototype_pairs_seen_by_scale_e": prototype_seen if expected is not None else None,
    }


def check_source_labels(root: Path) -> None:
    text = (root / RAW_REL).read_text(encoding="utf-8")
    for label in (
        "thm:capg-second-moment",
        "rem:capg-prototype",
        "prob:capg-shiftpairs",
        "prob:capg-active-shiftpairs",
    ):
        if re.search(r"\\label(?:\[[^]]+\])?\{" + re.escape(label) + r"\}", text) is None:
            raise AssertionError(f"missing label {label}")


def check() -> None:
    root = repo_root()
    check_source_labels(root)
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    by_id = {row["row_id"]: row for row in cert["rows"]}
    if set(by_id) != {row.row_id for row in ROWS}:
        raise AssertionError("row-id mismatch")
    for row in ROWS:
        observed = enumerate_counts(row)
        recorded = by_id[row.row_id]
        for key, value in observed.items():
            if recorded[key] != value:
                raise AssertionError(f"{row.row_id}.{key}: {recorded[key]} != {value}")
        if recorded["sp_ordered_pairs"] != recorded["pullback_pairs"] + recorded["primitive_pairs"]:
            raise AssertionError(f"{row.row_id}: partition mismatch")
    oracle = by_id["oracle_f5_mu4_w1_e2"]
    if oracle["sp_ordered_pairs"] != 2 or oracle["primitive_pairs"] != 0:
        raise AssertionError("oracle row drift")
    if cert["summary"]["total_primitive_pairs"] != sum(
        by_id[row.row_id]["primitive_pairs"] for row in ROWS if not row.row_id.startswith("oracle_")
    ):
        raise AssertionError("summary primitive total mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check()
    print("capg shift-pair primitive independent check PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
