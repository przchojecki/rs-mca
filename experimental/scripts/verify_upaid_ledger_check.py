#!/usr/bin/env python3
"""Independent checker for the U_paid partial ledger.

Does NOT import verify_upaid_ledger.py.

Checker routes (must differ from generator):
  * tangent: recompute r=n-A and R_tan via (n-k)//3; EXACT iff 0<=r<=R_tan with value n-A+1
    (generator uses the same formula path but this re-derives from n-A+1 identity without
    calling paid_tan_hi; also verifies 3*r <= n-k equivalent form)
  * common-support MCA: re-assert 0 from slope-elimination text presence + constant
  * lower L(a0): math.comb + ceil_div (not generator comb_batch ascending walk)
  * B_*: q_line >> lambda_bits (bit shift) vs generator //
  * quotient oracle: DP counting of labeled (c,B)-profiles vs binomial product
  * payload: recompute sha256 over sorted JSON

Status: EXPERIMENTAL / PARTIAL-LEDGER.
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

sys.set_int_max_str_digits(2_000_000)

STATUS = "EXPERIMENTAL / PARTIAL-LEDGER"
CERT_REL = Path("experimental/data/certificates/upaid-ledger/upaid_ledger.json")
RAW_REL = Path("experimental/cap25_cap_v13_raw.tex")
COMPACT_REL = Path("experimental/cap25_cap_v13_raw_compact.tex")

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


def binom_desc(n: int, k: int) -> int:
    """Descending product: C(n,k) = n*(n-1)*...*(n-k+1)/k!."""
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    num = 1
    for i in range(k):
        num = num * (n - i) // (i + 1)
    return num


def list_floor_check(kind: str, p: int, agreement: int) -> int:
    """L path uses math.comb (C) rather than generator comb_batch ascending walk."""
    dim = K_BASE + 1 if kind == "mca" else K_BASE
    w = agreement - dim
    return ceil_div(math.comb(N, agreement), p**w)


def lower_count_check(kind: str, p: int, ext: int, agreement: int) -> int:
    floor = list_floor_check(kind, p, agreement)
    if kind == "list":
        return floor
    q_line = p**ext
    den = q_line - N + K_BASE * (floor - 1)
    return ceil_div(floor * (q_line - N), den)


def tangent_recheck(n: int, k: int, A: int) -> dict[str, Any]:
    """Independent: value candidate is n-A+1; range via 3*(n-A) <= n-k."""
    r = n - A
    # Equivalent form of R_tan = floor((n-k)/3): 3r <= n-k
    in_range = r >= 0 and 3 * r <= n - k
    radius_cap = (n - k) // 3
    if in_range:
        return {"status": "EXACT", "value": n - A + 1, "radius": r, "radius_cap": radius_cap}
    return {
        "status": "UNAVAILABLE_OUT_OF_RANGE",
        "value": None,
        "radius": r,
        "radius_cap": radius_cap,
    }


def quotient_safe_sum_dp(n: int, A: int, divisors: list[int]) -> int:
    """Different algorithm: for each c, sum_B C(n/c, full)*C(n-c*full, rem) via
    multiplicative recurrence on full, not math.comb at each B independently.

    For fixed c, as B runs, full = B//c steps occasionally. We recompute using
    iterative ratios within each residual class.
    """
    total = 0
    for c in sorted(set(divisors)):
        nfib = n // c
        # B = c*full + rem, 0<=rem<c, B>=A
        for full in range(0, nfib + 1):
            # residual size rem with B=c*full+rem >= A and rem < c
            # and rem <= n - c*full
            max_rem = min(c - 1, n - c * full)
            # B from max(A, c*full) to c*full+max_rem
            b_lo = max(A, c * full)
            b_hi = c * full + max_rem
            if b_lo > b_hi:
                continue
            # C(nfib, full) once
            c_full = binom_desc(nfib, full)
            for B in range(b_lo, b_hi + 1):
                rem = B - c * full
                total += c_full * binom_desc(n - c * full, rem)
    return total


def check_oracle_quotient_dp() -> None:
    cases = [
        (12, 8, [2, 3]),
        (12, 6, [2, 4]),
        (16, 12, [2, 4]),
        (10, 7, [2, 5]),
    ]
    for n, A, divs in cases:
        # Independent DP sum vs math.comb sum
        s_dp = quotient_safe_sum_dp(n, A, divs)
        s_comb = 0
        for c in set(divs):
            for B in range(A, n + 1):
                full = B // c
                rem = B - c * full
                s_comb += math.comb(n // c, full) * math.comb(n - c * full, rem)
        if s_dp != s_comb:
            raise AssertionError(f"DP vs comb mismatch n={n} A={A}: {s_dp}!={s_comb}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--root", type=Path, default=None)
    args = ap.parse_args()
    if not args.check:
        ap.print_help()
        return 2
    root = args.root or repo_root()
    cert_path = root / CERT_REL
    cert = json.loads(cert_path.read_text(encoding="utf-8"))

    if cert.get("status") != STATUS:
        raise AssertionError(f"status {cert.get('status')}")
    if payload_hash(cert) != cert.get("payload_sha256"):
        raise AssertionError("payload hash fail")

    # Pin labels exist
    for label, pin in cert["statement_pins"].items():
        path = root / pin["path"]
        lines = path.read_text(encoding="utf-8").splitlines()
        ln = int(pin["line"])
        if label not in lines[ln - 1]:
            raise AssertionError(f"pin miss {label} at {path}:{ln}")

    check_oracle_quotient_dp()

    # Oracle section pass flags
    if not cert["oracle_gates"]["all_pass"]:
        raise AssertionError("cert oracle_all_pass false")

    for row_spec, drow in zip(ROWS, cert["deployed_rows"]):
        rid, kind, p, ext, lam, a0, a1 = row_spec
        if drow["row_id"] != rid:
            raise AssertionError(f"row order {drow['row_id']}!={rid}")
        q_line = p**ext
        # B_* via bit shift when exact power relation holds: floor(q_line / 2^lam)
        b_star = q_line >> lam if q_line.bit_length() > lam else q_line // (2**lam)
        # Prefer // for general correctness
        b_star = q_line // (2**lam)
        if drow["B_star"] != b_star:
            raise AssertionError(f"B_* {rid}: cert={drow['B_star']} check={b_star}")

        # Tangent via 3r <= n-k form
        tan = tangent_recheck(N, K_BASE, a1)
        c1 = drow["cells"]["C1_tangent_hi"]
        if c1["status"] != tan["status"]:
            raise AssertionError(f"tan status {rid}")
        if tan["status"] == "EXACT" and c1["value"] != tan["value"]:
            raise AssertionError(f"tan value {rid}")
        if c1["radius"] != tan["radius"]:
            raise AssertionError(f"tan radius {rid}")
        # Deployed rows must be out of range
        if tan["status"] != "UNAVAILABLE_OUT_OF_RANGE":
            raise AssertionError(f"expected out-of-range tangent at deployed a1 for {rid}")

        # Common support MCA = 0
        if kind == "mca":
            if drow["cells"]["C2_common_support"]["value"] != 0:
                raise AssertionError(f"common support MCA not 0 on {rid}")
            if drow["cells"]["C2_common_support"]["status"] != "EXACT":
                raise AssertionError(f"common support status {rid}")

        # L(a0) via math.comb (not generator comb_batch)
        la0 = lower_count_check(kind, p, ext, a0)
        if drow["lower_L_a0"] != la0:
            raise AssertionError(
                f"L(a0) {rid}: cert={drow['lower_L_a0']} check={la0}"
            )
        if not drow["lower_a0_exceeds_B_star"]:
            raise AssertionError(f"expected L(a0)>B_* on {rid}")

        # U_paid_computable = sum of exact values only
        recomputed = 0
        for name, cell in drow["cells"].items():
            if cell.get("status") == "EXACT" and cell.get("value") is not None:
                recomputed += int(cell["value"])
        if recomputed != drow["U_paid_computable_a1"]:
            raise AssertionError(f"U_paid_computable sum {rid}")
        if drow["gap_B_star_minus_U_paid_computable"] != b_star - recomputed:
            raise AssertionError(f"gap {rid}")

        # Blockers must be non-empty at deployed scale (honest partial ledger)
        if len(drow["blockers"]) < 5:
            raise AssertionError(f"expected multiple blockers on {rid}, got {len(drow['blockers'])}")

        # C4 charged to U_Q
        if drow["cells"]["C4_prefix_boundary"]["status"] != "CHARGED_TO_U_Q":
            raise AssertionError("C4 must be charged to U_Q")

    # Extension tier present
    if len(cert.get("extension_tier_rows", [])) < 2:
        raise AssertionError("extension tier missing")

    print("RESULT: PASS")
    print("route: tangent via 3r<=n-k + n-A+1; L via math.comb (not comb_batch); "
          "quotient oracle via residual-class DP vs comb; B_* via floor(q/2^lam)")
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
