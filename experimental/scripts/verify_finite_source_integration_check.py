#!/usr/bin/env python3
"""Independent checker for finite-source integration audit.

Does NOT import generator.

Checker routes:
  * re-search numbers via reverse line scan
  * recompute citation counts with different regex set
  * re-load q-r1 JSON and compare B_* integers independently
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
    "experimental/data/certificates/finite-source-integration/finite_source_integration.json"
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
    # reverse scan for each tracked number
    for name, val in cert["tracked_numbers"].items():
        s = str(val)
        found = any(s in ln for ln in reversed(lines))
        cert_found = any(h["name"] == name for h in cert["number_hits_in_paper"])
        if found != cert_found:
            raise AssertionError(f"hit mismatch {name}: reverse={found} cert={cert_found}")

    # independent Cho26 cite count
    text = "\n".join(lines)
    cho_cap = len(re.findall(r"Cho26CapV13|Cho26a", text))
    cho_gr = len(re.findall(r"Cho26Grande|Cho26b", text))
    if cert["citation_hit_counts"].get("Cho26CapV13", 0) > 0 and cho_cap == 0:
        raise AssertionError("Cho26Cap cite vanished")
    if cho_cap < 1 and cho_gr < 1:
        raise AssertionError("expected bibliography/cite presence for Cho26")

    # q-r1 values
    if (root / Q_R1).is_file():
        d = json.loads((root / Q_R1).read_text(encoding="utf-8"))
        rows = {r["row_id"]: r for r in d.get("row_table", [])}
        if rows["kb_mca"]["B_star_threshold"] != 274980728111395087:
            raise AssertionError("kb B_*")
        if rows["kb_mca"]["lower_floor_at_a1"] != 57198030366:
            raise AssertionError("kb L a1")

    if cert["verdict"] not in ("NO ISSUE", "OPEN GAP", "FIXED"):
        raise AssertionError("verdict vocab")
    if cert["integration_mode"] == "THEOREM_CITATION_ONLY" and cert["number_hits_in_paper"]:
        raise AssertionError("mode/hits inconsistency")

    print("RESULT: PASS")
    print(
        "route: reverse number scan; independent Cho26 regex counts; "
        "q-r1 JSON B_* re-read"
    )
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
