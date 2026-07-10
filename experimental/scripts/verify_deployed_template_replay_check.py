#!/usr/bin/env python3
"""Independent checker for deployed template replay.

Does NOT import generator.

Routes: L via math.comb; U via binary search ceil; B_* recompute.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(2_000_000)

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/deployed-template-replay/deployed_template_replay.json"
)

N = 2**21
K = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def U_binsearch(L: int, q: int, n: int, k: int) -> int:
    target = L * (q - n)
    den = q - n + k * (L - 1)
    lo, hi = 0, target
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * den >= target:
            hi = mid
        else:
            lo = mid + 1
    return lo


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

    specs = [
        ("kb_mca", P_KB, 6, 128, 1116047, 1116048),
        ("m31_mca", P_M31, 4, 100, 1116023, 1116024),
    ]
    for (rid, p, ext, lam, a0, a1), row in zip(specs, cert["rows"]):
        if row["row_id"] != rid:
            raise AssertionError("order")
        q = p**ext
        b = q // (2**lam)
        if row["B_star"] != b:
            raise AssertionError("B_*")
        dim = K + 1
        for lab, a, Lkey, Ukey in (
            ("a0", a0, "L_a0", "U_a0"),
            ("a1", a1, "L_a1", "U_a1"),
        ):
            w = a - dim
            L = ceil_div(math.comb(N, a), p**w)
            if row[Lkey] != L:
                raise AssertionError(f"L {rid} {lab}")
            U = U_binsearch(L, q, N, K)
            if row[Ukey] != U:
                raise AssertionError(f"U {rid} {lab}")
        if not row["unsafe_quiet_pattern"]:
            raise AssertionError("pattern")
    if cert.get("template_has_printed_deployed_numbers") is not False:
        raise AssertionError("template numbers flag")

    print("RESULT: PASS")
    print("route: L math.comb; U binary-search ceil; B_* floor(q/2^lam)")
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
