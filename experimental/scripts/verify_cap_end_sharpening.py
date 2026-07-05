#!/usr/bin/env python3
"""Replay the rate-1/8 cap-end sharpening packet."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "cap_end_sharpening.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "cap-end-sharpening"
    / "cap_end_sharpening.json"
)

N_EXP = 41
E_LOG2_K = 38
STEP_EXP = 9
J_LOG2_C = 28
D_EXTRA = 17

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "cap_end_sharpening",
    "point": "c = 2^28, N = 8192, d = 17, m = 1041, s = 0",
    "lower_bound": "L >= binom(8192, 1041) / 2^(256 * 16) > 2^398",
    "trigger": "binom(8192, 1041) > 2^(256 * 17 - 38)",
    "gain": "17 * 2^9 / 8192 - 1 = 1/16",
    "non_claim": "does not treat list decoding",
}


def log2_bigint(x: int) -> float:
    bits = x.bit_length()
    if bits <= 60:
        return math.log2(x)
    return (bits - 60) + math.log2(x >> (bits - 60))


def point_check() -> dict[str, object]:
    n = 1 << N_EXP
    k = 1 << E_LOG2_K
    c = 1 << J_LOG2_C
    N = 1 << (N_EXP - J_LOG2_C)
    m0 = 1 << (E_LOG2_K - J_LOG2_C)
    m = m0 + D_EXTRA
    A0 = m * c
    sigma = A0 - (k + 1)
    w = sigma // c

    hypotheses = {
        "c_divides_k": (k % c) == 0,
        "c_divides_n": (n % c) == 0,
        "K_less_than_n": (k + 1) < n,
        "m_in_range": 0 <= m <= N,
        "A0_gt_k": A0 > k,
        "A0_le_n": A0 <= n,
        "full_fiber_s_zero": True,
        "w_equals_d_minus_1": w == D_EXTRA - 1,
    }

    comb = math.comb(N, m)
    trigger = comb > (1 << (256 * D_EXTRA - E_LOG2_K))
    log2_c = log2_bigint(comb)
    log2_l = log2_c - 256 * w
    threshold = 256 - E_LOG2_K
    gain = Fraction(D_EXTRA << STEP_EXP, N) - 1
    unsafe_old = Fraction(7, 8) - Fraction(16, 8192)
    unsafe_new = Fraction(7, 8) - Fraction(17, 8192)

    return {
        "rate": "1/8",
        "n": "2^41",
        "k": "2^38",
        "q_bound": "q < 2^256",
        "c": "2^28",
        "N": N,
        "d": D_EXTRA,
        "m": m,
        "w": w,
        "hypotheses": hypotheses,
        "trigger": trigger,
        "log2_binom": round(log2_c, 6),
        "log2_L_lower_bound": round(log2_l, 6),
        "trigger_threshold_log2": threshold,
        "margin_bits": round(log2_l - threshold, 6),
        "gain_fraction": f"{gain.numerator}/{gain.denominator}",
        "gain": float(gain),
        "old_unsafe_boundary": "7152/8192",
        "new_unsafe_boundary": "7151/8192",
        "boundary_shift": "1/8192",
        "all_checks_pass": all(hypotheses.values())
        and trigger
        and log2_l > 398.0
        and gain == Fraction(1, 16)
        and unsafe_old - unsafe_new == Fraction(1, 8192),
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "cap-end-sharpening-v1",
        "status": "PROVED",
        "source_dag_node": "cap_end_sharpening",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "point": point_check(),
        "non_claims": [
            "does not claim a full clean-rate corridor ledger",
            "does not treat list decoding",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/cap_end_sharpening.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "cap-end-sharpening-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "cap_end_sharpening":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    point = cert.get("point")
    if not isinstance(point, dict) or not point.get("all_checks_pass"):
        raise AssertionError("point check failed")
    if point.get("gain_fraction") != "1/16":
        raise AssertionError("unexpected gain fraction")
    if float(point["margin_bits"]) <= 180.0:
        raise AssertionError("expected more than 180 trigger-margin bits")


def assert_same(expected: dict[str, object], actual: dict[str, object]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text(encoding="utf-8"))
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['source_dag_node']}")


if __name__ == "__main__":
    main()
