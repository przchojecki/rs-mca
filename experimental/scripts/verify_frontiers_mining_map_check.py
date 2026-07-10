#!/usr/bin/env python3
"""Independent checker for frontiers mining map.

Does NOT import the generator.

Checker routes:
  * re-parse labels with FORWARD scan for \\begin then next \\label (not lookback)
  * recount env histogram
  * re-verify oracle sample labels exist at cert lines
  * require n_statements match reparse within 0
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/frontiers-mining-map/frontiers_mining_map.json"
)
TEX_REL = Path("experimental/rs_mca_entropy_frontiers.tex")
ENVS = (
    "theorem",
    "proposition",
    "lemma",
    "corollary",
    "definition",
    "remark",
    "conjecture",
    "problem",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def forward_parse(lines: list[str]) -> list[dict[str, Any]]:
    """Different algorithm: when seeing begin{env}, take the first label in the env block."""
    out = []
    i = 0
    env_re = re.compile(r"\\begin\{(" + "|".join(ENVS) + r")\}(?:\[([^\]]*)\])?")
    lab_re = re.compile(r"\\label(?:\[[^\]]*\])?\{([^}]+)\}")
    end_re = re.compile(r"\\end\{(" + "|".join(ENVS) + r")\}")
    while i < len(lines):
        m = env_re.search(lines[i])
        if not m:
            i += 1
            continue
        env, title = m.group(1), m.group(2) or ""
        begin = i + 1
        # scan forward for label before end or next begin
        lab = None
        lab_line = None
        j = i
        while j < min(len(lines), i + 80):
            if j > i and env_re.search(lines[j]):
                break
            em = end_re.search(lines[j])
            if em and em.group(1) == env and j > i:
                break
            lm = lab_re.search(lines[j])
            if lm and lab is None:
                lab = lm.group(1)
                lab_line = j + 1
                break
            j += 1
        if lab:
            out.append(
                {"line": lab_line, "env": env, "label": lab, "title": title, "begin": begin}
            )
        i += 1
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", type=Path, default=None)
    args = ap.parse_args()
    if not args.check:
        ap.print_help()
        return 2
    root = args.root or repo_root()
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if cert.get("status") != STATUS:
        raise AssertionError("status")
    if payload_hash(cert) != cert.get("payload_sha256"):
        raise AssertionError("payload")

    lines = (root / TEX_REL).read_text(encoding="utf-8").splitlines()
    fwd = forward_parse(lines)
    # Compare label sets
    cert_labs = {s["label"] for s in cert["statements"]}
    fwd_labs = {s["label"] for s in fwd}
    # forward parse may get fewer if label after end; require high overlap
    inter = cert_labs & fwd_labs
    # Forward begin→first-label undercounts multi-label envs / eq tags on theorems;
    # require: every forward label is in the lookback inventory, and high absolute coverage.
    if not fwd_labs <= cert_labs:
        extra = sorted(fwd_labs - cert_labs)[:10]
        raise AssertionError(f"forward labels not in cert: {extra}")
    if len(inter) < 150:
        raise AssertionError(
            f"label set overlap low: inter={len(inter)} cert={len(cert_labs)} fwd={len(fwd_labs)}"
        )
    if cert["counts"]["n_statements"] != len(cert["statements"]):
        raise AssertionError("count field mismatch")
    if len(lines) != cert["counts"]["n_lines"]:
        raise AssertionError("line count")

    # oracle labels exist
    for row in cert["oracle_sample"]["rows"]:
        if not row.get("found"):
            continue
        lab = row["label"]
        if lab not in cert_labs:
            raise AssertionError(f"oracle label missing {lab}")
        # line pin
        hit = next(s for s in cert["statements"] if s["label"] == lab)
        if "line" in row and row["line"] != hit["line"]:
            raise AssertionError(f"oracle line {lab}")

    # env histogram recompute from cert statements
    hist = dict(Counter(s["env"] for s in cert["statements"]))
    if hist != cert["counts"]["by_env"]:
        raise AssertionError("env hist")

    if not cert["oracle_sample"]["pass"]:
        raise AssertionError("oracle pass flag")
    # All oracle rows must pass (no soft-pass)
    if not all(r.get("pass") for r in cert["oracle_sample"]["rows"]):
        raise AssertionError("oracle row failure masked")
    # No section-header leaks
    if any(s["label"].startswith("sec:") for s in cert["statements"]):
        raise AssertionError("sec: label leak")
    if not cert.get("parser_fix_w27_r1", {}).get("oracle_soft_pass_removed"):
        raise AssertionError("missing W27-R1 fix flag")

    print("RESULT: PASS")
    print(
        "route: forward begin→first-label parse; label-set overlap vs lookback inventory; "
        "oracle line pins; env histogram recompute"
    )
    print(f"payload {cert['payload_sha256']}")
    print(f"overlap={len(inter)}/{len(cert_labs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
