#!/usr/bin/env python3
"""Independent checker for L1 petal residual (no generator import)."""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

CERT_REL = Path(
    "experimental/data/certificates/l1-petal-residual/l1_petal_residual.json"
)
PAPER_REL = Path("experimental/cap25_cap_v13_raw.tex")


def repo_root():
    return Path(__file__).resolve().parents[2]


def check():
    root = repo_root()
    cert = json.loads((root / CERT_REL).read_text())
    text = (root / PAPER_REL).read_text()
    errors = []
    for lab in ("prob:capf-l1-residuals", "rem:capf-l1-evidence"):
        if lab not in text:
            errors.append(lab)
    # Independent recount of total configs: C(C(n,s), M) * q^M
    n, s, M, q = 6, 2, 3, 7
    from math import comb

    total = comb(comb(n, s), M) * (q**M)
    if total != cert["census"]["total_labeled_configs"]:
        errors.append(f"total {total} vs {cert['census']['total_labeled_configs']}")
    paid = cert["census"]["paid_total"]
    res = cert["census"]["residual_total"]
    if paid + res != total:
        errors.append("paid+residual != total")
    if cert["summary"]["verdict"] != "NO ISSUE":
        errors.append("verdict")
    if errors:
        print("RESULT: FAIL")
        for e in errors:
            print(" -", e)
        raise SystemExit(1)
    print("RESULT: PASS")
    print("route: binomial total recount + paid/residual partition")


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
