#!/usr/bin/env python3
"""Independent checker for finite-source full coverage.

Routes: reverse-line scan for each tracked value; recompute paper int set via
finditer positions; re-load q-r1 JSON.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/finite-source-full-coverage/"
    "finite_source_full_coverage.json"
)
TEX_REL = Path("experimental/rs_mca_entropy_frontiers.tex")
Q_R1 = Path("experimental/data/certificates/q-r1-closing-audit/q_r1_closing_audit.json")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.print_help()
        return 2
    root = repo_root()
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if cert.get("status") != STATUS:
        raise AssertionError("status")
    if payload_hash(cert) != cert.get("payload_sha256"):
        raise AssertionError("payload")

    lines = (root / TEX_REL).read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)
    paper_set = sorted({int(m.group(0)) for m in re.finditer(r"\b\d{7,}\b", text)})
    if paper_set != cert["paper_large_int_set_route_B"]:
        raise AssertionError(f"paper set {paper_set} vs {cert['paper_large_int_set_route_B']}")

    for row in cert["coverage_table"]:
        val = row["quoted_value"]
        found = any(str(val) in ln for ln in reversed(lines))
        if found != row["match_in_paper"]:
            raise AssertionError(f"hit {row['tracked_name']}")

    if (root / Q_R1).is_file():
        d = json.loads((root / Q_R1).read_text(encoding="utf-8"))
        rows = {r["row_id"]: r for r in d.get("row_table", [])}
        if rows["kb_mca"]["B_star_threshold"] != 274980728111395087:
            raise AssertionError("B_*")
        if rows["kb_mca"]["lower_floor_at_a1"] != 57198030366:
            raise AssertionError("U a1")

    if cert["verdict"] not in ("NO ISSUE", "OPEN GAP", "FIXED"):
        raise AssertionError("verdict")
    print("RESULT: PASS")
    print("route: reverse tracked search; finditer paper set; q-r1 JSON reload")
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
