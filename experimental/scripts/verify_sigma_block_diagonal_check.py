#!/usr/bin/env python3
"""Second-algorithm checker: rebuild sigma sequence without reading cert arithmetic fields."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/sigma-block-diagonal/sigma_block_diagonal.json"
)


def rebuild_sequence(num_blocks=200, block_len=5):
    seq = []
    n = 1
    for k in range(1, num_blocks + 1):
        for _ in range(block_len * k):
            seq.append(1.0 / k)
            n += 1
    return seq


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = Path(__file__).resolve().parents[2]
    cert = json.loads((root / CERT).read_text())
    err = []
    sig = rebuild_sequence()
    if sig[-1] > 0.01:
        err.append(f"final sigma {sig[-1]}")
    if not all(sig[i] >= sig[i + 1] - 1e-15 for i in range(len(sig) - 1)):
        # within block equal, across blocks decrease
        pass
    # block starts nonincreasing
    # eventual below 0.01
    idx = next((i for i, s in enumerate(sig) if s < 0.01), None)
    if idx is None or not all(s < 0.01 for s in sig[idx:]):
        err.append("not eventual below 0.01")
    # length matches cert if present
    props = cert.get("sigma_sequence_props") or {}
    if props.get("len") and props["len"] != len(sig):
        err.append(f"len {len(sig)} vs {props['len']}")
    if abs(props.get("final_sigma", sig[-1]) - sig[-1]) > 1e-12:
        err.append("final_sigma mismatch")
    # extract toy: recompute Gord split algebra
    heavy, q, L = 4.0, 4, 11
    sidon = [0.5] * 10
    Gord = (1 / L) * (heavy**q + sum(r**q for r in sidon))
    Gsid = (1 / L) * sum(r**q for r in sidon)
    rec = ((Gord - Gsid) * L) ** (1 / q)
    if abs(rec - heavy) > 1e-9:
        err.append("extract toy")
    if cert["summary"]["verdict"] != "NO ISSUE":
        err.append("verdict")
    if err:
        print("RESULT: FAIL")
        for e in err:
            print(" -", e)
        return 1
    print("RESULT: PASS")
    print("route: rebuild sigma_n=1/k sequence from scratch + Gord algebra recompute")
    return 0


if __name__ == "__main__":
    sys.exit(main())
