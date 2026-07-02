#!/usr/bin/env python3
"""Replay the exact constants in the promoted towards-prize v2 note.

This AUDIT verifier checks the ordinary locator constants ``alpha_rho`` and the
quadratic-envelope fallback used in ``tex/towards-prize.tex``.  The TeX says
the four envelope instances were verified exactly at ``n=2^15`` and
``q=2^256-1``; this script replays those comparisons and also checks the
ordinary-locator cap criterion at the same endpoint.
"""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path
from typing import Any


DEFAULT_PACKET = Path(
    "experimental/data/certificates/towards-prize-v2-constant-audit/"
    "towards_prize_v2_constants.json"
)


class AuditError(Exception):
    """Raised when a towards-prize v2 constant check fails."""


def parse_fraction(value: str) -> tuple[int, int]:
    parts = value.split("/")
    if len(parts) != 2:
        raise AuditError(f"expected rational string a/b, got {value!r}")
    num = int(parts[0])
    den = int(parts[1])
    if den <= 0:
        raise AuditError(f"bad denominator in {value!r}")
    return num, den


def ceil_div(num: int, den: int) -> int:
    return -(-num // den)


def load_packet(path: Path) -> dict[str, Any]:
    try:
        packet = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AuditError(f"{path}: invalid JSON: {exc}") from exc
    if packet.get("schema_version") != "towards-prize-v2-constants-v1":
        raise AuditError("unexpected schema_version")
    if not isinstance(packet.get("rates"), list):
        raise AuditError("packet.rates must be an array")
    return packet


def strict_inequality(label: str, lhs: int, rhs: int) -> str:
    if lhs <= rhs:
        raise AuditError(f"{label}: inequality failed")
    return (
        f"lhs_bits={lhs.bit_length()} rhs_bits={rhs.bit_length()} "
        f"slack_bits={(lhs-rhs).bit_length()}"
    )


def check_alpha_side_conditions(
    rho: tuple[int, int],
    alpha: tuple[int, int],
    g: tuple[int, int],
    n: int,
) -> list[str]:
    rho_num, rho_den = rho
    alpha_num, alpha_den = alpha
    g_num, g_den = g
    if alpha_num * g_den <= g_num * alpha_den:
        raise AuditError("alpha_rho must be strictly larger than g_rho")
    # The proof uses rho + alpha + 2^-15 < 1.
    lhs = (rho_num * alpha_den * 2**15
           + alpha_num * rho_den * 2**15
           + rho_den * alpha_den)
    rhs = rho_den * alpha_den * 2**15
    if lhs >= rhs:
        raise AuditError("rho + alpha + 2^-15 < 1 failed")
    s = ceil_div(alpha_num * n, alpha_den)
    return [
        f"s=ceil(alpha*n)={s}",
        f"alpha>g checked as {alpha_num}*{g_den}>{g_num}*{alpha_den}",
        "rho+alpha+2^-15<1",
    ]


def check_ordinary_locator(row: dict[str, Any], n: int, q: int) -> list[str]:
    rho = parse_fraction(row["rho"])
    alpha = parse_fraction(row["alpha"])
    g = parse_fraction(row["g"])
    rho_num, rho_den = rho
    if n * rho_num % rho_den:
        raise AuditError(f"{row['rho']}: n*rho must be integral")
    k = n * rho_num // rho_den
    alpha_details = check_alpha_side_conditions(rho, alpha, g, n)
    s = ceil_div(alpha[0] * n, alpha[1])
    if s != int(row["ordinary_expected_s"]):
        raise AuditError(f"{row['rho']}: ordinary s mismatch")
    m = k + s
    w = s - 1
    lhs = comb(n, m) * k
    rhs = q**w * (q + k)
    margin = strict_inequality(
        f"{row['rho']} ordinary locator cap", lhs, rhs
    )
    return [
        *alpha_details,
        f"ordinary cap: binom({n},{m}) > q^{w}(q/k+1), "
        "checked as binom*k > q^w(q+k)",
        margin,
    ]


def check_quadratic_envelope(row: dict[str, Any], n: int, q: int) -> list[str]:
    rho = parse_fraction(row["rho"])
    g = parse_fraction(row["g"])
    rho_num, rho_den = rho
    if n * rho_num % rho_den:
        raise AuditError(f"{row['rho']}: n*rho must be integral")
    k = n * rho_num // rho_den
    g_n = g[0] * n // g[1]
    if g[0] * n % g[1]:
        raise AuditError(f"{row['rho']}: g*n must be integral at n_min")
    m = ceil_div(k + 1 + g_n, 2)
    w = m - ceil_div(k + 1, 2)
    if m != int(row["quadratic_expected_m"]):
        raise AuditError(f"{row['rho']}: quadratic m mismatch")
    if w != int(row["quadratic_expected_w"]):
        raise AuditError(f"{row['rho']}: quadratic w mismatch")
    lhs = comb(n // 2, m) * k
    rhs = q**w * (q + k)
    margin = strict_inequality(
        f"{row['rho']} quadratic envelope cap", lhs, rhs
    )
    return [
        f"g*n={g_n}; m=ceil((k+1+g*n)/2)={m}; "
        f"w=m-ceil((k+1)/2)={w}",
        f"quadratic cap: binom({n//2},{m}) > q^{w}(q/k+1), "
        "checked as binom*k > q^w(q+k)",
        margin,
    ]


def check_endpoint_error_floor(n: int) -> list[str]:
    # Worst case from towards-prize v2: k <= 2^40, n <= 16k <= 2^44,
    # q >= 2^128.  Check (1/(2k))*(1-n/q) > 2^-128 at the worst endpoint.
    k = 2**40
    q = 2**128
    worst_n = 16 * k
    lhs = (q - worst_n) * 2**128
    rhs = 2 * k * q
    margin = strict_inequality("endpoint error floor", lhs, rhs)
    return [
        "worst endpoint k=2^40, n=2^44, q=2^128",
        "(1/(2k))*(1-n/q)>2^-128 checked by integer cross-multiplication",
        margin,
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    args = parser.parse_args()

    packet = load_packet(args.packet)
    n = int(packet["n_min"])
    q = 2**256 - 1

    print("=" * 74)
    print("AUDIT: towards-prize v2 ordinary-locator and envelope constants")
    print("=" * 74)

    failed = 0
    total = 0
    for row in packet["rates"]:
        for title, fn in (
            ("ordinary locator", check_ordinary_locator),
            ("quadratic envelope", check_quadratic_envelope),
        ):
            total += 1
            label = f"rho={row['rho']} {title}"
            try:
                details = fn(row, n, q)
            except AuditError as exc:
                failed += 1
                print(f"\n[FAIL] {label}")
                print(f"       {exc}")
                continue
            print(f"\n[PASS] {label}")
            for line in details:
                print(f"       {line}")

    total += 1
    try:
        details = check_endpoint_error_floor(n)
    except AuditError as exc:
        failed += 1
        print("\n[FAIL] endpoint error floor")
        print(f"       {exc}")
    else:
        print("\n[PASS] endpoint error floor")
        for line in details:
            print(f"       {line}")

    print("\n" + "-" * 74)
    print(f"implemented PASS: {total - failed}   FAIL: {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
