#!/usr/bin/env python3
"""Independent checker for bc-one-pencil omega correction.

Route: recompute omega as sum of (n-m) via bit ops: n = 1<<21; subtract m.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/bc-one-pencil-omega/bc_one_pencil_omega.json"
)
TEX_REL = Path("experimental/grande_finale.tex")


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
    n = 1 << 21
    text = (root / TEX_REL).read_text(encoding="utf-8")
    if "980104" not in text or "cor:bc-one-pencil" not in text:
        raise AssertionError("tex pin")
    for r in cert["rows"]:
        omega = n - r["m_a_plus"]
        if omega != r["omega_correct_n_minus_m"]:
            raise AssertionError("omega")
        if r["omega_printed_in_tex"] + 1000 != omega:
            raise AssertionError("delta")
        if n // omega != 2 or n // r["omega_printed_in_tex"] != 2:
            raise AssertionError("floor")
    if cert["verdict"] != "FIXED":
        raise AssertionError("verdict")
    if not cert.get("parks_for_ken"):
        raise AssertionError("must park")
    print("RESULT: PASS")
    print("route: n=1<<21; omega=n-m; printed+1000; floor both")
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
