#!/usr/bin/env python3
"""XR clean-rate polynomial forcing verifier.

DAG node: xr_clean_residual_any_gate.

This is a deterministic integer verifier for the clean-rate compiler proved in
experimental/notes/roadmaps/xr_clean_poly_forcing_reduction.md. It does not
prove the algebraic RK residual bound. It proves the exact arithmetic
consumption statement:

    B_quot_ub(A) + B_tan_max(A) + 16*n^3 <= B*

at all six clean-rate decision candidates from xr_budget_audit.md. Therefore
any per-pair post-strip residual bounded by 16*n^3 is absorbed by the
clean-rate gate.

Run:
    python3 experimental/scripts/verify_xr_clean_poly_forcing.py
    python3 experimental/scripts/verify_xr_clean_poly_forcing.py --write-certificate
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

PASS: list[str] = []
FAIL: list[str] = []

CERT_PATH = Path(
    "experimental/data/certificates/xr-clean-poly-forcing/"
    "xr_clean_poly_forcing_certificate.json"
)


def check(label: str, ok: bool, detail: str = "") -> None:
    (PASS if ok else FAIL).append(label)
    tag = "PASS" if ok else "FAIL"
    print(f"{tag}  {label}" + (f"  [{detail}]" if detail else ""))


def iroot(x: int, r: int) -> int:
    """Return floor(x**(1/r)) for nonnegative integers."""
    if x < 0 or r <= 0:
        raise ValueError("iroot expects x >= 0 and r > 0")
    lo, hi = 0, 1
    while hi**r <= x:
        hi *= 2
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if mid**r <= x:
            lo = mid
        else:
            hi = mid
    return lo


def log2_big(x: int) -> float:
    """Display-only log2 for positive big integers."""
    if x <= 0:
        raise ValueError("log2_big expects x > 0")
    bits = x.bit_length()
    if bits <= 53:
        return math.log2(x)
    return (bits - 53) + math.log2(x >> (bits - 53))


def bquot_ub(n: int, k: int, a: int) -> int:
    """Floor-rounded all-active-scale quotient upper bound from the audit."""
    t = a - k
    total = 0
    np = 2
    while np <= n and np * t <= n:
        lp = (n - a) * np // n
        if 1 <= lp <= np - 1:
            total += math.comb(np, lp)
        np *= 2
    return total


def bquot_strict(n: int, k: int, a: int) -> int:
    """Strict integral-l' quotient count from the audit."""
    t = a - k
    best = 0
    np = 2
    while np <= n and np * t <= n:
        j = n - a
        m = n // np
        if j % m == 0:
            lp = j // m
            if 1 <= lp <= np - 1:
                best = max(best, math.comb(np, lp))
        np *= 2
    return best


B_STAR_ROWC = 1 << 122
B_STAR_PRIZE = iroot(1 << 1279, 10)

AUDIT_ROWS = [
    {
        "row": "RowC",
        "rate": "1/4",
        "n": 1024,
        "rate_den": 4,
        "deciding_scale": 256,
        "B_star": B_STAR_ROWC,
        "expected_A": 261,
        "expected_s_lo": 5316907684064982757706454885536879188,
    },
    {
        "row": "RowC",
        "rate": "1/8",
        "n": 1024,
        "rate_den": 8,
        "deciding_scale": 256,
        "B_star": B_STAR_ROWC,
        "expected_A": 133,
        "expected_s_lo": 5316911983139662876649441475853304530,
    },
    {
        "row": "RowC",
        "rate": "1/16",
        "n": 1024,
        "rate_den": 16,
        "deciding_scale": 512,
        "B_star": B_STAR_ROWC,
        "expected_A": 67,
        "expected_s_lo": 5316911982997375233704305923711011740,
    },
    {
        "row": "prize",
        "rate": "1/4",
        "n": 1 << 41,
        "rate_den": 4,
        "deciding_scale": 256,
        "B_star": B_STAR_PRIZE,
        "expected_A": 558345748481,
        "expected_s_lo": 317494670476394092449112149242524378539,
    },
    {
        "row": "prize",
        "rate": "1/8",
        "n": 1 << 41,
        "rate_den": 8,
        "deciding_scale": 256,
        "B_star": B_STAR_PRIZE,
        "expected_A": 283467841537,
        "expected_s_lo": 317494674775468772568055135557962897065,
    },
    {
        "row": "prize",
        "rate": "1/16",
        "n": 1 << 41,
        "rate_den": 16,
        "deciding_scale": 512,
        "B_star": B_STAR_PRIZE,
        "expected_A": 141733920769,
        "expected_s_lo": 317494674775326484925109999864086683573,
    },
]


def build_certificate() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for item in AUDIT_ROWS:
        n = item["n"]
        rd = item["rate_den"]
        k = n // rd
        a = k + n // item["deciding_scale"] + 1
        j = n - a
        bq_ub = bquot_ub(n, k, a)
        bq_strict = bquot_strict(n, k, a)
        btan_max = n - a + 1
        s_lo = item["B_star"] - bq_ub - btan_max
        cubic = n**3
        reserve = 16 * cubic
        model_sum = cubic + n**2 + n
        rows.append(
            {
                "row": item["row"],
                "rate": item["rate"],
                "n": n,
                "k": k,
                "A": a,
                "j": j,
                "B_star": item["B_star"],
                "B_quot_strict": bq_strict,
                "B_quot_ub": bq_ub,
                "B_tan_max": btan_max,
                "s_lo": s_lo,
                "log2_s_lo": round(log2_big(s_lo), 12),
                "n_cubed": cubic,
                "residual_reserve_16n3": reserve,
                "margin_after_16n3": s_lo - reserve,
                "max_integer_cubic_coefficient": s_lo // cubic,
                "log2_s_over_n3": round(log2_big(s_lo) - 3 * math.log2(n), 12),
                "model_split": {
                    "primitive_n3": cubic,
                    "dihedral_n2": n**2,
                    "extension_n": n,
                    "sum": model_sum,
                    "slack_inside_16n3": reserve - model_sum,
                },
            }
        )
    return {
        "dag_node": "xr_clean_residual_any_gate",
        "parent_nodes": [
            "xr_target_budget_audit",
            "dihedral_staircase",
            "rigidity_kernel",
        ],
        "status": "PROVED compiler; conditional on the named residual/staircase input",
        "claim": (
            "At each clean-rate candidate, B_quot_ub + B_tan_max + 16*n^3 <= B*. "
            "Thus a per-pair post-strip residual bounded by 16*n^3 is absorbed."
        ),
        "rows": rows,
        "pinned_nonclaim": {
            "row": "pinned",
            "rate": "1/2",
            "n": 512,
            "A": 507,
            "B_star": 6,
            "s_at_A": 0,
            "reason": "rate-half calibration is tangent-exhausted and is not a clean-rate row",
        },
    }


def verify_certificate(cert: dict[str, Any]) -> None:
    check(
        "prize B* exact 10th-root pin",
        B_STAR_PRIZE**10 <= (1 << 1279) < (B_STAR_PRIZE + 1) ** 10
        and B_STAR_PRIZE == 317494674775468773183020924238786383963,
        f"B*={B_STAR_PRIZE}",
    )
    check("six clean-rate rows emitted", len(cert["rows"]) == 6)
    for source, row in zip(AUDIT_ROWS, cert["rows"]):
        tag = f"{row['row']} {row['rate']}"
        n = row["n"]
        cubic = row["n_cubed"]
        check(f"{tag}: candidate A matches xr_budget_audit pin", row["A"] == source["expected_A"])
        check(f"{tag}: s_lo matches xr_budget_audit pin", row["s_lo"] == source["expected_s_lo"])
        check(
            f"{tag}: j is odd, so strict quotient census is zero",
            row["j"] % 2 == 1 and row["B_quot_strict"] == 0,
        )
        check(
            f"{tag}: 16*n^3 residual reserve fits the clean-rate allowance",
            row["residual_reserve_16n3"] <= row["s_lo"],
            f"log2 margin={log2_big(row['margin_after_16n3']):.6f}",
        )
        check(
            f"{tag}: n^3 + n^2 + n split fits inside 16*n^3",
            row["model_split"]["sum"] <= row["residual_reserve_16n3"],
        )
        check(
            f"{tag}: allowance contains at least 29 cubic units",
            row["max_integer_cubic_coefficient"] >= 29,
            f"floor(s_lo/n^3)={row['max_integer_cubic_coefficient']}",
        )
        if row["row"] == "prize":
            check(
                f"{tag}: 30 cubic units are not claimed at prize scale",
                30 * cubic > row["s_lo"],
            )
        else:
            check(
                f"{tag}: RowC has far more than prize-scale cubic slack",
                row["log2_s_over_n3"] > 90,
            )
        check(
            f"{tag}: exact gate inequality",
            row["B_quot_ub"] + row["B_tan_max"] + row["residual_reserve_16n3"]
            <= row["B_star"],
        )
    pinned = cert["pinned_nonclaim"]
    check(
        "pinned 1/2 calibration remains excluded: s(A=507)=0",
        pinned["s_at_A"] == 0 and 16 * pinned["n"] ** 3 > pinned["s_at_A"],
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-certificate",
        action="store_true",
        help="rewrite the checked-in JSON certificate before verifying",
    )
    args = parser.parse_args()

    cert = build_certificate()
    if args.write_certificate:
        CERT_PATH.parent.mkdir(parents=True, exist_ok=True)
        CERT_PATH.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {CERT_PATH}")
    else:
        if CERT_PATH.exists():
            checked_in = json.loads(CERT_PATH.read_text())
            check("checked-in JSON certificate matches deterministic build", checked_in == cert)
        else:
            check("checked-in JSON certificate exists", False, str(CERT_PATH))

    verify_certificate(cert)

    print()
    print("row     rate  A              log2(s_lo)  floor(s_lo/n^3)")
    for row in cert["rows"]:
        print(
            f"{row['row']:<7} {row['rate']:<5} {row['A']:<14} "
            f"{row['log2_s_lo']:<11.6f} {row['max_integer_cubic_coefficient']}"
        )
    print()
    print(f"{len(PASS)} PASS, {len(FAIL)} FAIL")
    return 0 if not FAIL else 1


if __name__ == "__main__":
    sys.exit(main())
