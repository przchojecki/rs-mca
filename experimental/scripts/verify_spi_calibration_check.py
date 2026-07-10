#!/usr/bin/env python3
"""Independent checker for SPI calibration (no generator import)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT_REL = Path("experimental/data/certificates/spi-calibration/spi_calibration.json")
PAPER_REL = Path("experimental/cap25_cap_v13_raw.tex")


def repo_root():
    return Path(__file__).resolve().parents[2]


def check():
    root = repo_root()
    cert = json.loads((root / CERT_REL).read_text())
    errors = []
    text = (root / PAPER_REL).read_text()
    if "rem:capf-spi-calibration" not in text or "49408" not in text:
        errors.append("paper pin")
    # Independent: cap = t * (n - j + 2)
    n, j, t = 512, 128, 128
    cap = t * (n - j + 2)
    if cap != 49408 or cert["remark_calibration"]["cap"] != 49408:
        errors.append(f"cap {cap}")
    if not cert["oracle"]["pass"]:
        errors.append("oracle")
    if cert["summary"]["verdict"] != "NO ISSUE":
        errors.append("verdict")
    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    print("RESULT: PASS")
    print("route: cap = t*(n-j+2) rewrite")


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
