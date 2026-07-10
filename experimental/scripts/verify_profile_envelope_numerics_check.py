#!/usr/bin/env python3
"""Independent checker for profile-envelope numerics.

Does NOT import generator.

Routes:
  * L via math.comb (not comb_batch walk)
  * U via integer loop: smallest u with u*den >= L*(q-n)
  * g* via reverse grid (scan from hi to lo)
  * B_* via bit operations when possible
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
    "experimental/data/certificates/profile-envelope-numerics/profile_envelope_numerics.json"
)

N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1

ROWS = [
    ("kb_mca", "mca", P_KB, 6, 128, 1116047, 1116048),
    ("kb_list", "list", P_KB, 6, 128, 1116046, 1116047),
    ("m31_mca", "mca", P_M31, 4, 100, 1116023, 1116024),
    ("m31_list", "list", P_M31, 4, 100, 1116022, 1116023),
]


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


def U_loop(L: int, q: int, n: int, k: int) -> int:
    if L <= 0:
        return 0
    target = L * (q - n)
    den = q - n + k * (L - 1)
    u = 0
    # linear search from ceil estimate
    u = target // den
    while u * den < target:
        u += 1
    while u > 0 and (u - 1) * den >= target:
        u -= 1
    return u


def H2(x: float) -> float:
    if x <= 0 or x >= 1:
        return 0.0
    return -x * math.log2(x) - (1 - x) * math.log2(1 - x)


def g_star_reverse(rho: float, beta: float, grid: int = 40000) -> float:
    best = 0.0
    for i in range(grid, -1, -1):
        g = (1.0 - rho) * i / grid
        if H2(rho + g) >= beta * g - 1e-15:
            return g
    return best


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

    for spec, drow in zip(ROWS, cert["deployed_rows"]):
        rid, kind, p, ext, lam, a0, a1 = spec
        if drow["row_id"] != rid:
            raise AssertionError("order")
        q = p**ext
        b = q // (2**lam)
        if drow["B_star"] != b:
            raise AssertionError("B_*")
        K = K_BASE + 1 if kind == "mca" else K_BASE
        for lab, a in (("a0", a0), ("a1", a1)):
            w = a - K
            L = ceil_div(math.comb(N, a), p**w)
            if drow[lab]["L_list_floor"] != L:
                raise AssertionError(f"L {rid} {lab}")
            if kind == "mca":
                U = U_loop(L, q, N, K_BASE)
            else:
                U = L
            if drow[lab]["U_collision_aware"] != U:
                raise AssertionError(f"U {rid} {lab}: {drow[lab]['U_collision_aware']}!={U}")
        if not drow["a0"]["U_exceeds_B_star"]:
            raise AssertionError("a0 unsafe")
        if drow["a1"]["U_exceeds_B_star"]:
            raise AssertionError("a1 should be quiet")
        # g*
        rho = K_BASE / N
        beta = math.log2(p)
        gs = g_star_reverse(rho, beta)
        if abs(gs - drow["g_star"]) > 2e-3:
            raise AssertionError(f"g* reverse {gs} vs {drow['g_star']}")

    if not all(t["pass"] for t in cert["toy_grid"]):
        raise AssertionError("toys")

    print("RESULT: PASS")
    print(
        "route: L via math.comb; U via incremental integer loop; "
        "g* via reverse grid; B_* floor(q/2^lam)"
    )
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
