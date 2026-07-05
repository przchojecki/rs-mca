#!/usr/bin/env python3
"""Replay the list corridor widths packet."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "list_corridor_widths.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "list-corridor-widths"
    / "list_corridor_widths.json"
)

LOG2_Q = 256.0
TOL = 5e-12

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "list_corridor_widths",
    "unsafe_endpoint": "unsafe reserve = H(rho) / 128",
    "safe_endpoint": "safe reserve   = tau_star(rho, log2 q = 256)",
    "width_formula": "W_list          = (unsafe reserve - safe reserve) / eta",
    "non_claim": "does not treat the rate-`1/2` band",
}

EXPECTED = {
    "1/4": {
        "H_rho": 0.8112781244591328,
        "eta": 0.001953125,
        "unsafe_reserve_H_over_128": 0.006338110347337,
        "safe_reserve_tau_star": 0.003188644533466,
        "dyadic_hi_reserve_H_over_256": 0.003169055173668,
        "unsafe_delta": 0.743661889652663,
        "safe_delta": 0.746811355466534,
        "dyadic_hi_delta": 0.746830944826332,
        "W_list": 1.612526496982,
        "dyadic_window_width": 1.622556248918,
        "tau_star_minus_H_over_256_in_grid_steps": 0.010029751936,
    },
    "1/8": {
        "H_rho": 0.5435644431995964,
        "eta": 0.001953125,
        "unsafe_reserve_H_over_128": 0.004246597212497,
        "safe_reserve_tau_star": 0.002146721906218,
        "dyadic_hi_reserve_H_over_256": 0.002123298606248,
        "unsafe_delta": 0.870753402787503,
        "safe_delta": 0.872853278093782,
        "dyadic_hi_delta": 0.872876701393752,
        "W_list": 1.075136156735,
        "dyadic_window_width": 1.087128886399,
        "tau_star_minus_H_over_256_in_grid_steps": 0.011992729665,
    },
    "1/16": {
        "H_rho": 0.3372900666170139,
        "eta": 0.0009765625,
        "unsafe_reserve_H_over_128": 0.002635078645446,
        "safe_reserve_tau_star": 0.001337871459676,
        "dyadic_hi_reserve_H_over_256": 0.001317539322723,
        "unsafe_delta": 0.934864921354554,
        "safe_delta": 0.936162128540324,
        "dyadic_hi_delta": 0.936182460677277,
        "W_list": 1.328340157828,
        "dyadic_window_width": 1.349160266468,
        "tau_star_minus_H_over_256_in_grid_steps": 0.02082010864,
    },
}


def entropy_binary(x: float) -> float:
    if not 0 < x < 1:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def tau_star(rho: float, log2_q: float = LOG2_Q) -> float:
    lo, hi = 1e-12, 1.0 - rho - 1e-12
    for _ in range(300):
        mid = (lo + hi) / 2.0
        if mid * log2_q - entropy_binary(rho + mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2.0


def rate_value(label: str) -> float:
    num, den = label.split("/")
    return int(num) / int(den)


def cap_step(rate: str) -> float:
    return 2.0**-10 if rate == "1/16" else 2.0**-9


def compute_row(rate: str) -> dict[str, float | str]:
    rho = rate_value(rate)
    eta = cap_step(rate)
    h = entropy_binary(rho)
    unsafe = h / 128.0
    safe = tau_star(rho)
    dyadic_hi = h / 256.0
    return {
        "rate": rate,
        "H_rho": h,
        "eta": eta,
        "unsafe_reserve_H_over_128": unsafe,
        "safe_reserve_tau_star": safe,
        "dyadic_hi_reserve_H_over_256": dyadic_hi,
        "unsafe_delta": 1.0 - rho - unsafe,
        "safe_delta": 1.0 - rho - safe,
        "dyadic_hi_delta": 1.0 - rho - dyadic_hi,
        "W_list": (unsafe - safe) / eta,
        "dyadic_window_width": (unsafe - dyadic_hi) / eta,
        "tau_star_minus_H_over_256_in_grid_steps": (safe - dyadic_hi) / eta,
    }


def close(a: float, b: float) -> bool:
    return abs(a - b) <= TOL


def rounded_row(rate: str) -> dict[str, float | str]:
    row = compute_row(rate)
    rounded: dict[str, float | str] = {"rate": rate}
    for key, value in row.items():
        if key == "rate":
            continue
        if key == "H_rho":
            rounded[key] = float(value)
        else:
            rounded[key] = round(float(value), 15)
    return rounded


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    rows = [rounded_row(rate) for rate in ("1/4", "1/8", "1/16")]
    cert = {
        "schema": "list-corridor-widths-v1",
        "status": "PROVED",
        "source_dag_node": "list_corridor_widths",
        "units": "cap-grid steps eta",
        "log2_q": 256,
        "endpoint_convention": {
            "unsafe_reserve": "H(rho) / 128",
            "safe_reserve": "tau_star(rho, log2_q=256)",
            "grid_step": "eta = 2^-9 for rates 1/4 and 1/8; eta = 2^-10 for rate 1/16",
            "width_formula": "W_list = (unsafe_reserve - safe_reserve) / eta",
        },
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "rows": rows,
        "non_claims": [
            "does not treat the rate-1/2 band",
            "does not by itself prove a list adjacent threshold row",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/list_corridor_widths.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "list-corridor-widths-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "list_corridor_widths":
        raise AssertionError("source DAG node mismatch")
    if cert.get("units") != "cap-grid steps eta":
        raise AssertionError("unexpected units")
    if cert.get("log2_q") != 256:
        raise AssertionError("log2_q must be 256")

    rows = cert.get("rows")
    if not isinstance(rows, list) or [r.get("rate") for r in rows] != ["1/4", "1/8", "1/16"]:
        raise AssertionError("rows must be exactly clean rates 1/4, 1/8, 1/16")

    for row in rows:
        rate = str(row["rate"])
        expected = EXPECTED[rate]
        recomputed = compute_row(rate)
        for key, value in expected.items():
            if not close(float(row[key]), value):
                raise AssertionError(f"{rate} {key}: table={row[key]!r} expected={value!r}")
            if not close(float(row[key]), float(recomputed[key])):
                raise AssertionError(
                    f"{rate} {key}: table={row[key]!r} recomputed={recomputed[key]!r}"
                )
        if float(row["W_list"]) <= 1.0:
            raise AssertionError(f"{rate} W_list should exceed one grid step")
        if float(row["tau_star_minus_H_over_256_in_grid_steps"]) >= 0.025:
            raise AssertionError(f"{rate} tau_star drift exceeds audit bound")


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
