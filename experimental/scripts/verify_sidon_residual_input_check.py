#!/usr/bin/env python3
"""Checker: recompute SFM1 ratios; require OPEN GAP + MISSING_B."""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/sidon-residual-input/sidon_residual_input.json"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = repo_root()
    cert = json.loads((root / CERT).read_text(encoding="utf-8"))
    fails = []
    # shallow ok: R=1, p=101, N=1000
    if 1 * math.sqrt(101) / 1000 >= 0.1:
        fails.append("shallow")
    # deep fail
    if 1000 * math.sqrt(2**31 - 1) / (2**21) < 0.1:
        fails.append("deep_should_fail_sfm1")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if cert.get("verdict") != "OPEN GAP":
        fails.append("verdict")
    if not cert.get("missing_input", {}).get("id"):
        fails.append("missing_input")
    # sfm1 row
    row = next((r for r in cert.get("rows", []) if r.get("kind") == "sfm1_parameter_separation"), None)
    if not row or not row.get("all_shallow_ok") or not row.get("all_deep_fail_sfm1"):
        fails.append("sfm1_row")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: independent SFM1 ratio; MISSING_B + OPEN GAP")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
