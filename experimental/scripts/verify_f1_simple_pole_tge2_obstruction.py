#!/usr/bin/env python3
"""Simple-pole F1 obstruction at slack t>=2.

Proof status: PROVED for the named simple-pole pencil / AUDIT.

This verifier freezes the elementary algebraic reason the upstream
`f1_extension_full_orbit_scan.py` has a t=1 growth branch but a t>=2 zero
branch for the simple-pole pencil

    f_beta(x) = 1/(x - beta),    g(x) = x^k.

It is not an extension-cell theorem for arbitrary genuinely-F-valued received
pairs.  It only proves that this specific pencil cannot produce any bad slope
on supports of size k+t once t>=2.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
FRONTIER_DIR = REPO / "experimental" / "data" / "certificates" / "frontier-adjacent"
ARTIFACT = FRONTIER_DIR / "f1_simple_pole_tge2_obstruction_v1.json"
F1_SCAN = FRONTIER_DIR / "f1_full_orbit_scan_v1.json"
SLACK_TRANSLATION = FRONTIER_DIR / "f1_effective_slack_translation_v1.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def t_ge_2_rows_are_zero(scan: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for table_name, table in scan["growth_tables"].items():
        if int(table["t"]) < 2:
            continue
        feasible_rows = [
            row for row in table["rows"] if row.get("full_count") is not None
        ]
        rows.append(
            {
                "table": table_name,
                "shape": table["shape"],
                "t": table["t"],
                "feasible_points": [
                    [row["p0"], row["full_count"]] for row in feasible_rows
                ],
                "all_feasible_full_counts_zero": all(
                    row["full_count"] == 0 for row in feasible_rows
                ),
            }
        )
    return rows


def t_eq_1_rows_grow(scan: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for table_name, table in scan["growth_tables"].items():
        if int(table["t"]) != 1:
            continue
        rows.append(
            {
                "table": table_name,
                "shape": table["shape"],
                "t": table["t"],
                "points": table["fit"]["points"],
                "verdict": table["fit"]["verdict"],
                "has_nonzero_full_count": any(
                    count > 0 for _p0, count in table["fit"]["points"]
                ),
            }
        )
    return rows


def build_certificate() -> dict[str, Any]:
    scan = read_json(F1_SCAN)
    slack = read_json(SLACK_TRANSLATION) if SLACK_TRANSLATION.exists() else None
    cert = {
        "schema": "f1-simple-pole-tge2-obstruction-v1",
        "status": "PROVED_FOR_SIMPLE_POLE_PENCIL__AUDIT",
        "statement": {
            "pencil": "f_beta(x)=1/(x-beta), g(x)=x^k",
            "assumptions": [
                "F is any field containing the domain values",
                "S is a support with beta not in S",
                "k >= 1",
                "t >= 2",
                "|S| = k + t",
                "P is required to have degree < k",
            ],
            "conclusion": (
                "There is no slope gamma and no degree-<k polynomial P with "
                "P(x)=1/(x-beta)+gamma*x^k for every x in S."
            ),
        },
        "proof_steps": [
            {
                "id": "multiply_out_denominator",
                "claim": (
                    "If such P and gamma exist, then R(X)=(X-beta)P(X) "
                    "- gamma*(X-beta)*X^k - 1 vanishes on S."
                ),
                "status": "PROVED",
            },
            {
                "id": "degree_bound",
                "claim": (
                    "Since deg(P)<k, deg R <= k+1 unless R is zero; the "
                    "highest possible term is -gamma*X^(k+1)."
                ),
                "status": "PROVED",
            },
            {
                "id": "root_count",
                "claim": (
                    "|S|=k+t>=k+2, so R has more roots than its degree bound; "
                    "therefore R is the zero polynomial."
                ),
                "status": "PROVED",
            },
            {
                "id": "top_coefficient_forces_gamma_zero",
                "claim": "The X^(k+1) coefficient of R is -gamma, so R=0 forces gamma=0.",
                "status": "PROVED",
            },
            {
                "id": "evaluate_at_pole_contradiction",
                "claim": (
                    "With gamma=0, R=(X-beta)P(X)-1. Evaluating the polynomial "
                    "identity R=0 at X=beta gives -1=0, impossible in a field."
                ),
                "status": "PROVED",
            },
        ],
        "scanner_cross_checks": {
            "source": "frontier-adjacent/f1_full_orbit_scan_v1.json",
            "t_eq_1_growth_rows": t_eq_1_rows_grow(scan),
            "t_ge_2_zero_rows": t_ge_2_rows_are_zero(scan),
        },
        "deployed_translation": None
        if slack is None
        else {
            "source": "frontier-adjacent/f1_effective_slack_translation_v1.json",
            "adjacent_open_t_values": slack["summary"]["adjacent_open_t_values"],
            "all_adjacent_open_rows_have_t_at_least_2": slack["summary"][
                "all_adjacent_open_rows_have_t_at_least_2"
            ],
        },
        "interpretation": (
            "The simple-pole pencil's t>=2 branch is explained by a degree/root "
            "obstruction, not by a finite-field accident.  The t=1 branch is "
            "sharp because the same root-count argument is exactly one root "
            "short of contradiction."
        ),
        "non_claims": [
            "does not prove paid_extension(a) is safe",
            "does not classify all genuinely F-valued received pairs",
            "does not rule out t>=2 growth for a different F-valued pencil",
            "does not close the frontier-adjacent extension cell",
            "does not resolve Q/BC/SP residuals in CAP25 v13",
        ],
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert.get("schema") != "f1-simple-pole-tge2-obstruction-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED_FOR_SIMPLE_POLE_PENCIL__AUDIT":
        raise AssertionError("unexpected status")
    if any(step.get("status") != "PROVED" for step in cert["proof_steps"]):
        raise AssertionError("proof step not marked PROVED")
    if len(cert["proof_steps"]) != 5:
        raise AssertionError("unexpected proof-step count")
    growth_rows = cert["scanner_cross_checks"]["t_eq_1_growth_rows"]
    if not growth_rows or not all(row["has_nonzero_full_count"] for row in growth_rows):
        raise AssertionError("t=1 sharpness/growth cross-check missing")
    zero_rows = cert["scanner_cross_checks"]["t_ge_2_zero_rows"]
    if not zero_rows or not all(row["all_feasible_full_counts_zero"] for row in zero_rows):
        raise AssertionError("t>=2 scanner zero cross-check failed")
    deployed = cert.get("deployed_translation")
    if deployed is not None:
        if not deployed["all_adjacent_open_rows_have_t_at_least_2"]:
            raise AssertionError("deployed t translation no longer lands in t>=2")
        if min(deployed["adjacent_open_t_values"].values()) < 2:
            raise AssertionError("unexpected deployed t value below 2")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def tamper_selftest(cert: dict[str, Any]) -> None:
    bad = json.loads(json.dumps(cert))
    bad["proof_steps"][2]["status"] = "OPEN"
    try:
        validate(bad)
    except AssertionError:
        return
    raise AssertionError("tamper selftest failed")


def print_summary(cert: dict[str, Any]) -> None:
    print("f1_simple_pole_tge2_obstruction")
    print(f"  status: {cert['status']}")
    print(f"  interpretation: {cert['interpretation']}")
    for row in cert["scanner_cross_checks"]["t_ge_2_zero_rows"]:
        print(
            f"  {row['table']}: t={row['t']} feasible_points={row['feasible_points']} "
            f"zero={row['all_feasible_full_counts_zero']}"
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-defaults", action="store_true")
    parser.add_argument("--check", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    if args.tamper_selftest:
        tamper_selftest(cert)
    if args.emit_defaults:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = read_json(args.check)
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    if not args.emit_defaults and not args.check and not args.json:
        print_summary(cert)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
