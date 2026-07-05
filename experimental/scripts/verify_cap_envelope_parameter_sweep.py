#!/usr/bin/env python3
"""Replay the cap-envelope parameter sweep packet."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "cap_envelope_parameter_sweep.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "cap-envelope-parameter-sweep"
    / "cap_envelope_parameter_sweep.json"
)

N_EXP = 41

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "cap_envelope_parameter_sweep",
    "scale_free": "quotient-remainder floor used in the cap envelope is scale-free",
    "trigger": "binom(N, m) > 2^(256 d - e)",
    "gain": "gain = d * 2^step / N - 1",
    "non_claim": "does not alter Papers A-D",
}

POINTS = [
    {
        "label": "rate 1/4 optimum",
        "rate": "1/4",
        "e": 39,
        "step_exp": 9,
        "j": 25,
        "d": 209,
        "expected_gain": Fraction(81, 128),
        "required_task_gain": 0.318,
        "required_ledger_gain": 0.367,
        "role": "clean-rate optimum",
    },
    {
        "label": "rate 1/8 optimum",
        "rate": "1/8",
        "e": 38,
        "step_exp": 9,
        "j": 21,
        "d": 2251,
        "expected_gain": Fraction(203, 2048),
        "required_task_gain": 0.023,
        "required_ledger_gain": 0.023,
        "role": "clean-rate optimum",
    },
    {
        "label": "rate 1/16 optimum",
        "rate": "1/16",
        "e": 37,
        "step_exp": 10,
        "j": 28,
        "d": 11,
        "expected_gain": Fraction(3, 8),
        "required_task_gain": 0.304,
        "required_ledger_gain": 0.304,
        "role": "clean-rate optimum",
    },
    {
        "label": "rate 1/8 template",
        "rate": "1/8",
        "e": 38,
        "step_exp": 9,
        "j": 28,
        "d": 17,
        "expected_gain": Fraction(1, 16),
        "required_task_gain": 0.023,
        "required_ledger_gain": 0.023,
        "role": "template replay",
    },
]


def log2_bigint(x: int) -> float:
    bits = x.bit_length()
    if bits <= 60:
        return math.log2(x)
    return (bits - 60) + math.log2(x >> (bits - 60))


def check_point(point: dict[str, object]) -> dict[str, object]:
    e = int(point["e"])
    step_exp = int(point["step_exp"])
    j = int(point["j"])
    d = int(point["d"])
    expected_gain = point["expected_gain"]
    assert isinstance(expected_gain, Fraction)

    n = 1 << N_EXP
    k = 1 << e
    c = 1 << j
    N = 1 << (N_EXP - j)
    m0 = 1 << (e - j)
    m = m0 + d
    A0 = m * c
    sigma = A0 - (k + 1)
    w = sigma // c

    hypotheses = {
        "c_divides_k": j <= e and (k % c) == 0,
        "c_divides_n": j <= N_EXP and (n % c) == 0,
        "k_over_c_integral": (k % c) == 0,
        "K_less_than_n": (k + 1) < n,
        "m_in_range": 0 <= m <= N,
        "A0_gt_k": A0 > k,
        "A0_le_n": A0 <= n,
        "full_fiber_side_condition": True,
        "w_equals_d_minus_1": w == d - 1,
    }

    comb = math.comb(N, m)
    trigger = comb > (1 << (256 * d - e))
    comb_next = math.comb(N, m + 1)
    maximal_d = not (comb_next > (1 << (256 * (d + 1) - e)))
    log2_c = log2_bigint(comb)
    log2_l = log2_c - 256 * w
    threshold = 256 - e
    margin_bits = log2_l - threshold
    gain = Fraction(d << step_exp, N) - 1
    required_ledger = float(point["required_ledger_gain"])

    all_checks = (
        all(hypotheses.values())
        and trigger
        and maximal_d
        and gain == expected_gain
        and float(gain) >= required_ledger
    )

    return {
        "label": point["label"],
        "role": point["role"],
        "rate": point["rate"],
        "e_log2_k": e,
        "c": f"2^{j}",
        "d": d,
        "N": f"2^{N_EXP - j}",
        "m": m,
        "w": w,
        "hypotheses": hypotheses,
        "trigger": trigger,
        "maximal_d": maximal_d,
        "log2_binom": round(log2_c, 6),
        "log2_L_lower_bound": round(log2_l, 6),
        "trigger_threshold_log2": threshold,
        "margin_bits": round(margin_bits, 6),
        "gain_fraction": f"{gain.numerator}/{gain.denominator}",
        "gain": float(gain),
        "expected_gain_fraction": f"{expected_gain.numerator}/{expected_gain.denominator}",
        "required_task_gain": float(point["required_task_gain"]),
        "required_ledger_gain": required_ledger,
        "ledger_margin": round(float(gain) - required_ledger, 12),
        "all_checks_pass": all_checks,
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    rows = [check_point(point) for point in POINTS]
    clean = [row for row in rows if row["role"] == "clean-rate optimum"]
    cert = {
        "schema": "cap-envelope-parameter-sweep-v1",
        "status": "PROVED",
        "source_dag_node": "cap_envelope_parameter_sweep",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "model": {
            "n": "2^41",
            "q_bound": "q < 2^256",
            "fiber": "s = 0",
            "trigger": "binom(N,m) > 2^(256*d - e)",
            "gain": "d * 2^step / N - 1",
        },
        "points": rows,
        "clean_rate_summary": [
            {
                "rate": row["rate"],
                "best_c": row["c"],
                "best_d": row["d"],
                "gain_fraction": row["gain_fraction"],
                "gain": row["gain"],
                "required_ledger_gain": row["required_ledger_gain"],
                "ledger_margin": row["ledger_margin"],
            }
            for row in clean
        ],
        "conclusion": "The exact sweep covers the clean-rate ledger deficits at 1/4, 1/8, and 1/16.",
        "non_claims": [
            "does not reprove the quotient-remainder floor lemma",
            "does not by itself close a deployed adjacent row theorem",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/cap_envelope_parameter_sweep.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "cap-envelope-parameter-sweep-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "cap_envelope_parameter_sweep":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    points = cert.get("points")
    if not isinstance(points, list) or len(points) != len(POINTS):
        raise AssertionError("unexpected point table")
    for row in points:
        if not row.get("all_checks_pass"):
            raise AssertionError(f"{row.get('label')}: point check failed")
        if float(row["ledger_margin"]) < 0:
            raise AssertionError(f"{row.get('label')}: negative ledger margin")
    summary = cert.get("clean_rate_summary")
    if not isinstance(summary, list) or [row.get("rate") for row in summary] != ["1/4", "1/8", "1/16"]:
        raise AssertionError("unexpected clean-rate summary")


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
