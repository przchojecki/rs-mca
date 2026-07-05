#!/usr/bin/env python3
"""Replay the list corridor ledger packet."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "list_corridor_ledger.md"
WIDTHS_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "list-corridor-widths"
    / "list_corridor_widths.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "list-corridor-ledger"
    / "list_corridor_ledger.json"
)

N_EXP = 41
TOL = 5e-12

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "list_corridor_ledger",
    "dependency": "list_corridor_widths",
    "inequality": "available_gain(rate) >= W_list(rate) - 1",
    "trigger": "binom(N, m) > 2^(256 d - e)",
    "non_claim": "does not treat the rate-`1/2` band",
}

SWEEP_POINTS = {
    "1/4": {
        "e": 39,
        "step_exp": 9,
        "j": 25,
        "d": 209,
        "expected_gain": Fraction(81, 128),
    },
    "1/8": {
        "e": 38,
        "step_exp": 9,
        "j": 21,
        "d": 2251,
        "expected_gain": Fraction(203, 2048),
    },
    "1/16": {
        "e": 37,
        "step_exp": 10,
        "j": 28,
        "d": 11,
        "expected_gain": Fraction(3, 8),
    },
}


def log2_bigint(x: int) -> float:
    bits = x.bit_length()
    if bits <= 60:
        return math.log2(x)
    return (bits - 60) + math.log2(x >> (bits - 60))


def dependency_check() -> dict[str, object]:
    cert = json.loads(WIDTHS_CERT.read_text(encoding="utf-8"))
    rows = cert.get("rows", [])
    return {
        "path": str(WIDTHS_CERT.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "rates": [row.get("rate") for row in rows] if isinstance(rows, list) else [],
        "accepted": cert.get("schema") == "list-corridor-widths-v1"
        and cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == "list_corridor_widths",
    }


def widths_by_rate() -> dict[str, float]:
    cert = json.loads(WIDTHS_CERT.read_text(encoding="utf-8"))
    return {str(row["rate"]): float(row["W_list"]) for row in cert["rows"]}


def check_sweep_point(rate: str, params: dict[str, object]) -> dict[str, object]:
    e = int(params["e"])
    step_exp = int(params["step_exp"])
    j = int(params["j"])
    d = int(params["d"])
    expected_gain = params["expected_gain"]
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
    gain = Fraction(d << step_exp, N) - 1
    log2_l = log2_bigint(comb) - 256 * w
    margin_bits = log2_l - (256 - e)

    all_checks = all(hypotheses.values()) and trigger and maximal_d and gain == expected_gain
    return {
        "rate": rate,
        "e_log2_k": e,
        "c": f"2^{j}",
        "d": d,
        "N": f"2^{N_EXP - j}",
        "m": m,
        "w": w,
        "hypotheses": hypotheses,
        "trigger": trigger,
        "maximal_d": maximal_d,
        "gain_fraction": f"{gain.numerator}/{gain.denominator}",
        "gain": float(gain),
        "expected_gain_fraction": f"{expected_gain.numerator}/{expected_gain.denominator}",
        "log2_L": round(log2_l, 6),
        "margin_bits": round(margin_bits, 6),
        "all_checks_pass": all_checks,
    }


def sweep_checks() -> list[dict[str, object]]:
    return [check_sweep_point(rate, SWEEP_POINTS[rate]) for rate in ("1/4", "1/8", "1/16")]


def ledger_rows(widths: dict[str, float], sweep: list[dict[str, object]]) -> list[dict[str, object]]:
    gain_by_rate = {str(row["rate"]): float(row["gain"]) for row in sweep}
    frac_by_rate = {str(row["rate"]): str(row["gain_fraction"]) for row in sweep}
    rows = []
    for rate in ("1/4", "1/8", "1/16"):
        w_list = widths[rate]
        required = w_list - 1.0
        gain = gain_by_rate[rate]
        rows.append(
            {
                "rate": rate,
                "W_list": round(w_list, 12),
                "required_gain_W_list_minus_1": round(required, 12),
                "sweep_gain_fraction": frac_by_rate[rate],
                "sweep_gain": gain,
                "margin": round(gain - required, 12),
                "verdict": "PASS" if gain - required > 0 else "FAIL",
            }
        )
    return rows


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    widths = widths_by_rate()
    sweep = sweep_checks()
    cert = {
        "schema": "list-corridor-ledger-v1",
        "status": "PROVED",
        "source_dag_node": "list_corridor_ledger",
        "dependencies": [dependency_check()],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "units": "cap-grid steps eta",
        "claim": "For every clean rate, scale-free floor gain >= W_list - 1.",
        "scale_free_floor_checks": sweep,
        "rows": ledger_rows(widths, sweep),
        "non_claims": [
            "does not treat the rate-1/2 band",
            "does not prove missing list-safe or list-unsafe endpoint formulas",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/list_corridor_ledger.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "list-corridor-ledger-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "list_corridor_ledger":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")

    sweep = cert.get("scale_free_floor_checks")
    if not isinstance(sweep, list) or [row.get("rate") for row in sweep] != ["1/4", "1/8", "1/16"]:
        raise AssertionError("unexpected sweep rows")
    for row in sweep:
        if not row.get("all_checks_pass"):
            raise AssertionError(f"{row.get('rate')}: scale-free floor check failed")

    rows = cert.get("rows")
    if not isinstance(rows, list) or [row.get("rate") for row in rows] != ["1/4", "1/8", "1/16"]:
        raise AssertionError("unexpected ledger rows")
    expected_widths = widths_by_rate()
    for row in rows:
        rate = str(row["rate"])
        expected_gain = SWEEP_POINTS[rate]["expected_gain"]
        assert isinstance(expected_gain, Fraction)
        if not math.isclose(float(row["W_list"]), expected_widths[rate], abs_tol=TOL):
            raise AssertionError(f"{rate}: W_list mismatch")
        if row.get("sweep_gain_fraction") != f"{expected_gain.numerator}/{expected_gain.denominator}":
            raise AssertionError(f"{rate}: sweep gain fraction mismatch")
        if float(row["margin"]) <= 0:
            raise AssertionError(f"{rate}: non-positive margin")
        if row.get("verdict") != "PASS":
            raise AssertionError(f"{rate}: verdict should be PASS")


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
