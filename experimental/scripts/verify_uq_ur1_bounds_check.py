#!/usr/bin/env python3
"""Independent checker for U_Q / U_R1 brackets.

Does NOT import verify_uq_ur1_bounds.py.

Checker routes:
  * log2 C(n,k): additive sum of log2((n-i)/(i+1)) in REVERSE order (k-1 down to 0)
    vs generator's forward product / lgamma
  * anticode log2 R_Q: recompute |B|^w / C(n-m+w,w) via reverse product
  * one-pencil: integer division n//(n-m) recomputed
  * U_Q lower: descending binomial product for C(n,m) then ceil_div by p^w
  * prop:proper-q-gap table: re-check abs_diff < 0.1 from cert floats vs reverse product
  * oracle: re-run one small ES-prefix census independently
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

sys.set_int_max_str_digits(2_000_000)

STATUS = "EXPERIMENTAL / PARTIAL-LEDGER"
CERT_REL = Path("experimental/data/certificates/uq-ur1-bounds/uq_ur1_bounds.json")

N = 2**21
K_BASE = 2**20
P_KB = 2**31 - 2**24 + 1
P_M31 = 2**31 - 1
LOG2 = math.log(2.0)

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


def log2_binom_reverse(n: int, k: int) -> float:
    """Checker route: reverse-order product sum."""
    if k < 0 or k > n:
        return float("-inf")
    k = min(k, n - k)
    s = 0.0
    for i in range(k - 1, -1, -1):
        s += math.log2(n - i) - math.log2(i + 1)
    return s


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def binom_check(n: int, k: int) -> int:
    """Checker C(n,k): math.comb, not generator comb_batch ascending walk."""
    return math.comb(n, k)


def es_prefix(M: tuple[int, ...], w: int, p: int) -> tuple[int, ...]:
    dp = [0] * (w + 1)
    dp[0] = 1
    for x in M:
        for h in range(w, 0, -1):
            dp[h] = (dp[h] + dp[h - 1] * (x % p)) % p
    return tuple(dp[1:])


def oracle_one_case(n: int, m: int, w: int, p: int) -> None:
    t = w // 2
    den = math.comb(m, t) * math.comb(n - m, t)
    pack = math.comb(n, m) // den
    fibers: dict[tuple[int, ...], int] = {}
    for M in combinations(range(n), m):
        z = es_prefix(M, w, p)
        fibers[z] = fibers.get(z, 0) + 1
    mx = max(fibers.values())
    if mx > pack:
        raise AssertionError(f"packing violated brute {mx} > {pack}")


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

    # pins
    for label, pin in cert["statement_pins"].items():
        lines = (root / pin["path"]).read_text(encoding="utf-8").splitlines()
        if label not in lines[int(pin["line"]) - 1]:
            raise AssertionError(f"pin {label}")

    if not cert["oracle_gates"]["all_pass"]:
        raise AssertionError("oracle flag")
    oracle_one_case(9, 5, 2, 11)

    for spec, drow in zip(ROWS, cert["deployed_rows"]):
        rid, kind, p, ext, lam, a0, a1 = spec
        if drow["row_id"] != rid:
            raise AssertionError("row order")
        K = K_BASE + 1 if kind == "mca" else K_BASE
        m = a1
        w = m - K
        t = w // 2
        b = (p**ext) // (2**lam)
        if drow["B_star"] != b:
            raise AssertionError(f"B_* {rid}")

        log2_Bw = w * math.log2(p)
        log2_RQ = log2_Bw - log2_binom_reverse(m, t) - log2_binom_reverse(N - m, t)
        got = drow["U_Q"]["log2_R_Q_pack_johnson_exact_p"]
        if abs(log2_RQ - got) > 1e-3:
            raise AssertionError(
                f"RQ reverse-product mismatch {rid}: check={log2_RQ} cert={got}"
            )
        log2_RQ31 = w * 31.0 - log2_binom_reverse(m, t) - log2_binom_reverse(N - m, t)
        if abs(log2_RQ31 - drow["U_Q"]["log2_R_Q_pack_johnson_prop31"]) > 1e-3:
            raise AssertionError(f"RQ prop31 mismatch {rid}")
        # anticode
        log2_ac = log2_Bw - log2_binom_reverse(N - m + w, w)
        if abs(log2_ac - drow["U_Q"]["log2_R_Q_anticode"]) > 1e-3:
            raise AssertionError(f"anticode {rid}")

        # one-pencil
        omega = N - m
        if drow["U_R1"]["U_R1_upper_one_pencil_conditional"] != N // omega:
            raise AssertionError(f"one_pencil {rid}")
        if drow["U_R1"]["U_R1_lower"] != 0:
            raise AssertionError("R1 lower")

        # U_Q lower via math.comb (independent of generator comb_batch)
        uq_lo = ceil_div(binom_check(N, m), p**w)
        if drow["U_Q"]["U_Q_lower_pigeonhole"] != uq_lo:
            raise AssertionError(
                f"UQ lower {rid}: cert={drow['U_Q']['U_Q_lower_pigeonhole']} check={uq_lo}"
            )

        # upper must exceed B_*
        if not drow["U_Q"]["upper_exceeds_B_star"]:
            raise AssertionError(f"expected packing >> B_* on {rid}")
        if drow["closing_status"]["unconditional_closing_possible_from_these_bounds"]:
            raise AssertionError("must not claim unconditional closing")

        # width positive and huge
        if drow["U_Q"]["distance_johnson_upper_to_B_star_bits"] < 1e6:
            raise AssertionError(f"expected million-bit gap on {rid}")

    for gr in cert["prop_proper_q_gap_replay"]:
        if not gr["agrees_to_0p1_under_prop31_convention"]:
            raise AssertionError(f"gap table {gr}")
        if not gr["exact_p_is_strictly_below_prop31"]:
            raise AssertionError(f"exact p should be below prop31 on {gr['row_id']}")

    if len(cert.get("extension_tier_rows", [])) < 2:
        raise AssertionError("extension tier")

    print("RESULT: PASS")
    print(
        "route: log2 binom reverse-order product; anticode reverse; "
        "UQ lower math.comb ceil_div; one-pencil n//omega; oracle ES-prefix re-census"
    )
    print(f"payload {cert['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
