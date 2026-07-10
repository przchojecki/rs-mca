#!/usr/bin/env python3
"""Independent checker for #444 absorption audit.

Does NOT import the generator.

Checker routes:
  * A_k via iterative product of falling factorials (not comb chain, not factorial)
  * heavy = 1<<k bit shift
  * Delta = pow(3,k)/pow(4,k)
  * energy = pow(6,k)
  * re-pin thm:polynomial-obstruction and require n=2(p-1) pattern in block
  * require cert verdict in {NO ISSUE, OPEN GAP, FIXED}
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
    "experimental/data/certificates/counterexample-absorption/counterexample_absorption.json"
)
TEX_REL = Path("experimental/asymptotic_rs_mca.tex")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def A_k_falling(k: int) -> int:
    """k!/(r!)^5 via successive falling products."""
    r = k // 5
    out = 1
    # multinomial as product_{j=0}^{4} falling(k-jr, r)/r!
    n = k
    for _ in range(5):
        num = 1
        for i in range(r):
            num *= n - i
        den = 1
        for i in range(1, r + 1):
            den *= i
        out *= num // den
        n -= r
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

    k = 5
    Ak = A_k_falling(k)
    if Ak != cert["recomputed_444_k5"]["A_k"]:
        raise AssertionError(f"A_k falling {Ak} != cert {cert['recomputed_444_k5']['A_k']}")
    if cert["recomputed_444_k5"]["heavy_fiber_size"] != (1 << k):
        raise AssertionError("heavy bitshift")
    if cert["recomputed_444_k5"]["energy_E"] != 6**k:
        raise AssertionError("energy")
    if cert["recomputed_444_k5"]["Delta_heavy_num"] != 3**k:
        raise AssertionError("delta num")
    if cert["recomputed_444_k5"]["Delta_heavy_den"] != 4**k:
        raise AssertionError("delta den")

    # paper construction
    text = (root / TEX_REL).read_text(encoding="utf-8")
    if "thm:polynomial-obstruction" not in text:
        raise AssertionError("missing thm:polynomial-obstruction")
    if not re.search(r"n=2\(p-1\)", text) and "2(p-1)" not in text:
        # allow latex form
        if r"n=2(p-1)" not in text and "2(p-1)" not in text:
            raise AssertionError("paper obstruction missing n=2(p-1) scale")
    if not cert["paper_counterexample_block"]["distinct_from_444"]:
        raise AssertionError("paper must be distinct from #444 blocks")
    if cert["verdict"] not in ("NO ISSUE", "OPEN GAP", "FIXED"):
        raise AssertionError("verdict vocab")
    if not cert["residual_predicate_test"]["excluded_from_primitive_Q_by_paid_sidon"]:
        raise AssertionError("must exclude via Sidon")

    print("RESULT: PASS")
    print(
        "route: A_k falling-factorial multinomial; heavy 1<<k; "
        "Delta 3^k/4^k; energy 6^k; re-pin square-quotient obstruction"
    )
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
