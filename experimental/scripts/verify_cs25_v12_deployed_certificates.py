#!/usr/bin/env python3
"""Replay the exact integer certificates printed in Paper D v12.

This is an AUDIT verifier for the deployed certificate table in
``tex/cs25_cap_v12.tex``.  It checks the integer inequalities behind the PF,
XH, MC, HJ, CH, PR, and RF verdict rows using exact Python integers only.  It
does not prove the cited theorems; it verifies that the printed deployed-row
arithmetic is reproducible.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


DEFAULT_PACKET = Path(
    "experimental/data/certificates/cs25-v12-deployed-certificates/"
    "cs25_v12_deployed_certificates.json"
)


class AuditError(Exception):
    """Raised when a deployed certificate check fails."""


def load_packet(path: Path) -> dict[str, Any]:
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AuditError(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(packet, dict):
        raise AuditError("packet must be a JSON object")
    if packet.get("schema_version") != "cs25-v12-deployed-certificates-v1":
        raise AuditError("unexpected schema_version")
    if not isinstance(packet.get("rows"), dict):
        raise AuditError("packet.rows must be an object")
    if not isinstance(packet.get("checks"), list):
        raise AuditError("packet.checks must be an array")
    return packet


def base_prime(expr: str) -> int:
    if expr == "2^31 - 2^24 + 1":
        return 2**31 - 2**24 + 1
    if expr == "2^31 - 1":
        return 2**31 - 1
    raise AuditError(f"unsupported base prime expression {expr!r}")


def row_params(packet: dict[str, Any], row_id: str) -> dict[str, int]:
    row = packet["rows"].get(row_id)
    if not isinstance(row, dict):
        raise AuditError(f"unknown row {row_id!r}")
    for key in ("base_prime", "n", "k"):
        if key not in row:
            raise AuditError(f"row {row_id}: missing {key}")
    p = base_prime(row["base_prime"])
    degree = int(row.get("extension_degree", 1))
    return {
        "p": p,
        "q": p**degree,
        "n": int(row["n"]),
        "k": int(row["k"]),
        "target_power": int(row.get("target_power", 0)),
    }


def require_int(item: dict[str, Any], key: str) -> int:
    value = item.get(key)
    if not isinstance(value, int):
        raise AuditError(f"{item.get('id', '<check>')}: {key} must be an integer")
    return value


def bit_length(value: int) -> int:
    if value <= 0:
        return 0
    return value.bit_length()


def strict_check(name: str, lhs: int, rhs: int, details: list[str]) -> list[str]:
    if lhs <= rhs:
        raise AuditError(f"{name}: inequality failed")
    slack = lhs - rhs
    return [
        *details,
        f"lhs_bits={lhs.bit_length()} rhs_bits={rhs.bit_length()} "
        f"slack_bits={bit_length(slack)}",
    ]


def check_delta_excess(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    if "delta_excess" not in item:
        return []
    c = require_int(item, "c")
    m = require_int(item, "m")
    expected = require_int(item, "delta_excess")
    actual = c * m - row["k"]
    if actual != expected:
        raise AuditError(
            f"{item['id']}: delta_excess mismatch: {actual} != {expected}"
        )
    return [f"Delta=c*m-k={actual}"]


def check_prefix_mca(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    n_big = require_int(item, "N")
    m = require_int(item, "m")
    w = require_int(item, "w")
    lhs = comb(n_big, m) * row["k"]
    rhs = row["p"] ** w * (row["q"] + row["k"])
    return strict_check(
        item["label"],
        lhs,
        rhs,
        [
            f"binom({n_big},{m}) > p^{w}(q/k+1), checked as "
            "binom*k > p^w(q+k)",
            *check_delta_excess(item, row),
        ],
    )


def check_prefix_list(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    n_big = require_int(item, "N")
    m = require_int(item, "m")
    w = require_int(item, "w")
    target_power = require_int(item, "target_power")
    lhs = comb(n_big, m) * 2**target_power
    rhs = row["p"] ** w * row["q"]
    return strict_check(
        item["label"],
        lhs,
        rhs,
        [
            f"binom({n_big},{m}) > p^{w}*2^-{target_power}*q, checked as "
            "binom*2^target > p^w*q",
            *check_delta_excess(item, row),
        ],
    )


def check_explicit_head_mca(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    n_big = require_int(item, "count_N")
    m = require_int(item, "count_m")
    lhs = comb(n_big, m) * row["k"]
    rhs = row["q"] + row["k"]
    return strict_check(
        item["label"],
        lhs,
        rhs,
        [
            f"binom({n_big},{m}) > q/k+1, checked as binom*k > q+k",
        ],
    )


def check_explicit_head_list(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    n_big = require_int(item, "count_N")
    m = require_int(item, "count_m")
    target_power = require_int(item, "target_power")
    lhs = comb(n_big, m) * 2**target_power
    rhs = row["q"]
    return strict_check(
        item["label"],
        lhs,
        rhs,
        [
            f"binom({n_big},{m}) > 2^-{target_power}*q, checked as "
            "binom*2^target > q",
        ],
    )


def check_mutual_from_correlated(
    item: dict[str, Any], packet: dict[str, Any]
) -> list[str]:
    r = require_int(item, "r")
    rows = item.get("rows")
    if not isinstance(rows, list) or not rows:
        raise AuditError(f"{item['id']}: rows must be a nonempty list")
    details = []
    for row_id in rows:
        if not isinstance(row_id, str):
            raise AuditError(f"{item['id']}: row ids must be strings")
        row = row_params(packet, row_id)
        if r != (row["n"] - row["k"]) // 2:
            raise AuditError(f"{item['id']}: r is not floor((n-k)/2) for {row_id}")
        if 2 * r > row["n"] - row["k"]:
            raise AuditError(f"{item['id']}: half-distance inequality failed")
        details.append(f"{row_id}: 2r={2*r} <= n-k={row['n']-row['k']}")
    return details


def check_half_johnson(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    r = require_int(item, "r")
    l2 = require_int(item, "L2")
    target_power = require_int(item, "target_power")
    n = row["n"]
    k = row["k"]
    gap = (n - 2 * r) ** 2 - (k - 1) * n
    if n - 2 * r <= 0:
        raise AuditError(f"{item['id']}: n-2r must be positive")
    if gap <= 0:
        raise AuditError(f"{item['id']}: Johnson gap must be positive")
    johnson_lhs = (l2 + 1) * gap
    johnson_rhs = n * (n - 2 * r - k + 1)
    if johnson_lhs <= johnson_rhs:
        raise AuditError(f"{item['id']}: HJ list-size certificate failed")
    error_lhs = (1 + (r + 1) * l2) * 2**target_power
    error_rhs = row["q"]
    if error_lhs >= error_rhs:
        raise AuditError(f"{item['id']}: HJ denominator inequality failed")
    return [
        f"n-2r={n-2*r}; Johnson gap={gap}",
        f"(L2+1)*gap > n*(n-2r-k+1), slack_bits="
        f"{(johnson_lhs-johnson_rhs).bit_length()}",
        f"(1+(r+1)L2)/q < 2^-{target_power}, slack_bits="
        f"{(error_rhs-error_lhs).bit_length()}",
    ]


def check_conditional_half_import(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    r = require_int(item, "r")
    target_power = require_int(item, "target_power")
    if 2 * r > row["n"] - row["k"]:
        raise AuditError(f"{item['id']}: half-distance radius is too large")
    lhs = row["n"] * 2**target_power
    rhs = row["q"]
    if lhs >= rhs:
        raise AuditError(f"{item['id']}: n/q < 2^-target failed")
    return [
        f"2r={2*r} <= n-k={row['n']-row['k']}",
        f"n/q < 2^-{target_power}, slack_bits={(rhs-lhs).bit_length()}",
    ]


def check_profile(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    n_big = require_int(item, "count_N")
    m = require_int(item, "count_m")
    kappa_power = require_int(item, "kappa_power")
    list_floor = (comb(n_big, m) + row["p"] - 1) // row["p"]
    kappa = 2**kappa_power
    # Table inequality: L > 1 + kappa*q*T, where q*T=(q-n)/k.
    lhs = list_floor * row["k"]
    rhs = row["k"] + kappa * (row["q"] - row["n"])
    if lhs <= rhs:
        raise AuditError(f"{item['id']}: strict profile inequality failed")
    floor_lhs = (list_floor - 1) * row["k"]
    floor_rhs = kappa * (row["q"] - row["n"])
    if floor_lhs < floor_rhs:
        raise AuditError(f"{item['id']}: kappa floor certificate failed")
    return [
        f"L=ceil(binom({n_big},{m})/p), kappa=2^{kappa_power}",
        f"L*k > k+kappa*(q-n), slack_bits={(lhs-rhs).bit_length()}",
        f"floor((L-1)k/(q-n)) >= kappa, slack_bits="
        f"{(floor_lhs-floor_rhs).bit_length()}",
    ]


def check_rational_floor(item: dict[str, Any], row: dict[str, int]) -> list[str]:
    n_big = require_int(item, "N")
    m = require_int(item, "m")
    w = require_int(item, "w")
    dominance_power = require_int(item, "dominance_power")
    lhs = comb(n_big, m)
    rhs = row["p"] ** w * 2**dominance_power
    if lhs <= rhs:
        raise AuditError(f"{item['id']}: rational-floor inequality failed")
    details = [
        f"binom({n_big},{m}) > p^{w}*2^{dominance_power}",
        f"lhs_bits={lhs.bit_length()} rhs_bits={rhs.bit_length()} "
        f"slack_bits={(lhs-rhs).bit_length()}",
    ]
    margin_power = item.get("margin_power")
    if isinstance(margin_power, int):
        margin_rhs = rhs * 2**margin_power
        if lhs <= margin_rhs:
            raise AuditError(f"{item['id']}: margin 2^{margin_power} failed")
        details.append(
            f"margin exceeds 2^{margin_power}, slack_bits="
            f"{(lhs-margin_rhs).bit_length()}"
        )
    return details


def run_check(item: dict[str, Any], packet: dict[str, Any]) -> list[str]:
    if not isinstance(item.get("id"), str) or not isinstance(item.get("label"), str):
        raise AuditError("each check needs string id and label")
    kind = item.get("kind")
    if kind == "mutual_from_correlated":
        return check_mutual_from_correlated(item, packet)
    row_id = item.get("row")
    if not isinstance(row_id, str):
        raise AuditError(f"{item['id']}: row must be a string")
    row = row_params(packet, row_id)
    if kind == "prefix_mca":
        return check_prefix_mca(item, row)
    if kind == "prefix_list":
        return check_prefix_list(item, row)
    if kind == "explicit_head_mca":
        return check_explicit_head_mca(item, row)
    if kind == "explicit_head_list":
        return check_explicit_head_list(item, row)
    if kind == "half_johnson":
        return check_half_johnson(item, row)
    if kind == "conditional_half_import":
        return check_conditional_half_import(item, row)
    if kind == "profile":
        return check_profile(item, row)
    if kind == "rational_floor":
        return check_rational_floor(item, row)
    raise AuditError(f"{item['id']}: unknown check kind {kind!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    args = parser.parse_args()

    packet = load_packet(args.packet)
    print("=" * 74)
    print("AUDIT: Paper D v12 deployed certificate table exact arithmetic")
    print("=" * 74)

    failed = 0
    checks = packet["checks"]
    for item in checks:
        try:
            details = run_check(item, packet)
        except AuditError as exc:
            failed += 1
            print(f"\n[FAIL] {item.get('label', item.get('id', '<check>'))}")
            print(f"       {exc}")
            continue
        print(f"\n[PASS] {item['label']} ({item['id']})")
        for line in details:
            print(f"       {line}")

    print("\n" + "-" * 74)
    print(f"implemented PASS: {len(checks) - failed}   FAIL: {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
