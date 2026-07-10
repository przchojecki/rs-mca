#!/usr/bin/env python3
"""Checker: forward env parse; recompute status counts from stored statements."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

CERT = Path(
    "experimental/data/certificates/newdraft-mining-map/newdraft_mining_map.json"
)
TEX = Path("experimental/asymptotic_rs_mca_frontiers.tex")
ENVS = (
    "theorem",
    "proposition",
    "lemma",
    "corollary",
    "definition",
    "hypothesis",
    "remark",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def forward_labels(lines):
    begin_re = re.compile(r"\\begin\{(" + "|".join(ENVS) + r")\}")
    end_re = re.compile(r"\\end\{(" + "|".join(ENVS) + r")\}")
    label_re = re.compile(r"\\label(?:\[[^\]]*\])?\{([^}]+)\}")
    labs = set()
    i, n = 0, len(lines)
    while i < n:
        bm = begin_re.search(lines[i])
        if not bm:
            i += 1
            continue
        env = bm.group(1)
        # include labels on the begin line
        for m in label_re.finditer(lines[i]):
            labs.add(m.group(1))
        i += 1
        while i < n:
            em = end_re.search(lines[i])
            if em and em.group(1) == env:
                # labels on end line rare; still scan before break
                for m in label_re.finditer(lines[i]):
                    labs.add(m.group(1))
                break
            for m in label_re.finditer(lines[i]):
                labs.add(m.group(1))
            i += 1
        i += 1
    return labs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    if not args.check:
        p.print_help()
        return 2
    root = repo_root()
    cert = json.loads((root / CERT).read_text(encoding="utf-8"))
    lines = (root / TEX).read_text(encoding="utf-8").splitlines()
    fwd = forward_labels(lines)
    stored = {s["label"] for s in cert["statements"]}
    fails = []
    # compare stored formal-env labels to forward inventory
    env_stored = {s["label"] for s in cert["statements"] if s.get("env") != "equation"}
    inter = len(env_stored & fwd)
    if inter < 0.85 * max(len(env_stored), 1):
        fails.append(f"overlap:{inter}/{len(env_stored)}/{len(fwd)}")
    by = Counter(s["status"] for s in cert["statements"])
    if dict(by) != cert["counts"]["by_status"]:
        fails.append("status_counts")
    if not cert.get("oracle_pass"):
        fails.append("oracle")
    if not cert.get("all_pass"):
        fails.append("all_pass")
    if cert.get("n_statements", 0) < 50:
        fails.append("too_few")
    if fails:
        print("RESULT: FAIL", fails)
        return 1
    print("RESULT: PASS")
    print("route: forward begin→label set; recount status")
    print("payload_sha256:", cert.get("payload_sha256"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
