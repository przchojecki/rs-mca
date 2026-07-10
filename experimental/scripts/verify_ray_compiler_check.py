#!/usr/bin/env python3
"""Checker for ray-compiler audit. Route: recompute Z*H <= J*P for each toy; re-pin hyp."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path("experimental/data/certificates/ray-compiler/ray_compiler.json")
TEX_REL = Path("experimental/rs_mca_entropy_frontiers.tex")


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(json.dumps(c, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if not args.check:
        ap.print_help()
        return 2
    root = Path(__file__).resolve().parents[2]
    cert = json.loads((root / CERT_REL).read_text(encoding="utf-8"))
    if cert.get("status") != STATUS or payload_hash(cert) != cert.get("payload_sha256"):
        raise AssertionError("status/payload")
    text = (root / TEX_REL).read_text(encoding="utf-8")
    if "hyp:ray-compiler" not in text or "eq:ray-compiler" not in text:
        raise AssertionError("pins")
    for t in cert["toy_double_count"]:
        holds = t["Z"] * t["H"] <= t["J"] * t["P"]
        if holds != t["holds_product"]:
            raise AssertionError(f"toy {t}")
    if not any(not t["holds_product"] for t in cert["toy_double_count"]):
        raise AssertionError("no fail toy")
    print("RESULT: PASS")
    print("route: recompute Z*H<=J*P per toy; re-search hyp:ray-compiler in tex")
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
