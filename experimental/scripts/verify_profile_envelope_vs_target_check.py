#!/usr/bin/env python3
"""Checker: alternate envelope expansion + integer U?B* from cert."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/profile-envelope-vs-target/profile_envelope_vs_target.json"
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def E_alt(n: int, a: int, barNs: list[int]) -> int:
    return (n - a + 2) + sum(barNs) + len(barNs)


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
    if E_alt(32, 20, [50, 10, 5]) != (1 + (32 - 20 + 1) + (51 + 11 + 6)):
        fails.append("E_formula")
    for r in cert.get("rows", []):
        if r.get("kind", "").startswith("deployed_"):
            if not (r["a0"]["U"] > r["B_star"] and r["a1"]["U"] <= r["B_star"]):
                fails.append(r["kind"])
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: alternate E expansion; integer U?B*")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
