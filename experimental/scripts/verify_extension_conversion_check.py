#!/usr/bin/env python3
"""Independent checker for extension-conversion (no generator import).

Sharp ExtPole is recomputed by a GENUINELY DIFFERENT route from the generator's
ceil_div(L*m, m+kappa*(L-1)): an incremental integer loop that finds the least
N with N * den >= num (balanced-partition counting form).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/extension-conversion/extension_conversion.json"
)
PAPER_REL = Path("experimental/cap25_cap_v13_raw.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ext_pole_incremental(L: int, m: int, kappa: int) -> int:
    """Least integer N s.t. N >= L*m / (m + kappa*(L-1)).

    Implemented as: den = m + kappa*(L-1); find least N with N*den >= L*m
    by counting up (not via ceil division / not via -(-a//b)).
    """
    if L < 1 or m < 1 or kappa < 0:
        raise ValueError("bad params")
    den = m + kappa * (L - 1)
    num = L * m
    if den <= 0:
        raise ValueError("nonpositive denominator")
    n = 0
    acc = 0  # tracks n * den
    while acc < num:
        n += 1
        acc += den
    return n


def check():
    root = repo_root()
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    errors = []
    text = (root / PAPER_REL).read_text(encoding="utf-8")
    for lab in (
        "rem:capf-extension-main",
        "prop:capf-extension",
        "cor:extension-pole-deep-list-floor",
    ):
        if lab not in text:
            errors.append(f"missing {lab}")

    for row in cert["integer_menu"]:
        L, m, k = row["L"], row["m"], row["kappa"]
        sharp = ext_pole_incremental(L, m, k)
        if sharp != row["sharp"]:
            errors.append(f"sharp mismatch {row} vs incremental {sharp}")
        if row["sharp"] < row["weak"]:
            errors.append(f"sharp < weak {row}")

    ora = cert["oracle"]
    if ext_pole_incremental(2, 3, 1) != 2 or not ora["pass"]:
        errors.append("oracle")

    for row in cert["kappa_agreement_rows"]:
        if not row["respects_kappa"]:
            errors.append(f"kappa fail {row}")

    if cert["summary"]["verdict"] != "NO ISSUE":
        errors.append("verdict")

    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    print("RESULT: PASS")
    print("route: incremental N*den >= L*m loop (not ceil_div)")


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args(argv)
    if args.check:
        try:
            check()
            return 0
        except SystemExit as e:
            return int(e.code or 1)
    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
