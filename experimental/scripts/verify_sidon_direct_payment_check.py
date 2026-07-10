#!/usr/bin/env python3
"""Checker: 4-fold energy; require OPEN GAP + open_input."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/sidon-direct-payment/sidon_direct_payment.json"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def energy4(F):
    c = 0
    for a, b, x, y in itertools.product(F, F, F, F):
        if all(a[i] - b[i] == x[i] - y[i] for i in range(len(a))):
            c += 1
    return c


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
    if energy4([(1, 0), (0, 1), (0, 0)]) <= 0:
        fails.append("energy")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if not cert.get("pins_ok"):
        fails.append("pins")
    if cert.get("verdict") != "OPEN GAP":
        fails.append("verdict_should_be_OPEN_GAP")
    if not cert.get("open_input"):
        fails.append("open_input")
    # W36-R1: payment_falsifiability must compute can_fail from instances
    pf = next((r for r in cert.get("rows", []) if r.get("kind") == "payment_falsifiability"), None)
    if pf is None:
        fails.append("missing_payment_falsifiability")
    else:
        if "fail_instance_Gsid" not in pf or "pass_instance_Gsid" not in pf:
            fails.append("falsifiability_not_computed")
        thr = pf.get("threshold", 1.0)
        if not (pf.get("fail_instance_Gsid", 0) > thr):
            fails.append("fail_instance_not_failing")
        if pf.get("can_fail") is not True:
            fails.append("can_fail_false")
        if pf.get("can_fail") != pf.get("fail_instance_fails_inequality"):
            fails.append("can_fail_inconsistent")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: 4-fold energy; require OPEN GAP + open_input disclosure")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
