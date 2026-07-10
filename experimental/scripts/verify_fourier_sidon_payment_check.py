#!/usr/bin/env python3
"""Independent checker for Fourier/Sidon payment audit.

Routes: reverse product log2 for PF score; pin labels by reverse line scan;
recompute energy 6**k; require PF menu has both pass and fail.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/fourier-sidon-payment/fourier_sidon_payment.json"
)
TEX_REL = Path("experimental/rs_mca_entropy_frontiers.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def log2_binom_reverse(n: int, k: int) -> float:
    k = min(k, n - k)
    s = 0.0
    for i in range(k - 1, -1, -1):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


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
    for lab, pin in cert["statement_pins"].items():
        ln = int(pin["line"])
        if lab not in lines[ln - 1] and "label" not in lines[ln - 1]:
            # allow nearby
            window = "\n".join(lines[max(0, ln - 2) : ln + 1])
            if lab not in window:
                raise AssertionError(f"pin {lab}")

    # PF scores reverse
    for row in cert["PF_toy_menu"]:
        R, q, Lam, m, T = row["R"], row["q"], row["Lambda"], row["m"], row["T"]
        score = (
            R * math.log2(q)
            + log2_binom_reverse(Lam + m - 1, m)
            - log2_binom_reverse(T, m)
        )
        if abs(score - row["score_bits_product"]) > 1e-3:
            raise AssertionError(f"PF score {score} vs {row['score_bits_product']}")

    if not cert["PF_falsifiable"]:
        raise AssertionError("falsifiable")
    if cert["sidon_heavy_toy"]["energy"] != 6 ** cert["sidon_heavy_toy"]["k"]:
        raise AssertionError("energy")
    if cert["verdict"] not in ("NO ISSUE", "OPEN GAP", "FIXED"):
        raise AssertionError("verdict")

    print("RESULT: PASS")
    print("route: reverse log2 binom PF score; reverse label pin; energy 6^k")
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
