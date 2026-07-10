#!/usr/bin/env python3
"""Correction audit: cor:bc-one-pencil worked table omega values.

grande_finale.tex prints omega = 980104 (KB MCA a+=1116048) and 980128 (M31).
Correct omega = n - m with n=2^21:
  2097152 - 1116048 = 981104
  2097152 - 1116024 = 981128
Off by exactly 1000. floor(n/omega)=2 unchanged.

Verdict: FIXED-class discrepancy (table typo); floor claim unaffected.
PARKS for Ken — correction against maintainer text.

Status: EXPERIMENTAL / AUDIT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

STATUS = "EXPERIMENTAL / AUDIT"
CERT_REL = Path(
    "experimental/data/certificates/bc-one-pencil-omega/bc_one_pencil_omega.json"
)
TEX_REL = Path("experimental/grande_finale.tex")
N = 2**21


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def payload_hash(obj: dict[str, Any]) -> str:
    c = dict(obj)
    c.pop("payload_sha256", None)
    return hashlib.sha256(
        json.dumps(c, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build_certificate(root: Path) -> dict[str, Any]:
    lines = (root / TEX_REL).read_text(encoding="utf-8").splitlines()
    # pin cor:bc-one-pencil
    idx = next(
        i
        for i, ln in enumerate(lines, 1)
        if "cor:bc-one-pencil" in ln and "label" in ln
    )
    # find printed table values
    printed = {"kb": None, "m31": None}
    for i, ln in enumerate(lines[idx - 1 : idx + 30], start=idx):
        if "1116048" in ln and "980104" in ln:
            printed["kb"] = {"line": i, "text": ln.strip(), "omega_printed": 980104, "m": 1116048}
        if "1116024" in ln and "980128" in ln:
            printed["m31"] = {"line": i, "text": ln.strip(), "omega_printed": 980128, "m": 1116024}

    rows = []
    for key, m, printed_omega in (
        ("kb_mca", 1116048, 980104),
        ("m31_mca", 1116024, 980128),
    ):
        omega_true = N - m
        # route A: n-m
        # route B: n + (-m) integer
        omega_b = N + (-m)
        assert omega_true == omega_b
        floor_printed = N // printed_omega
        floor_true = N // omega_true
        rows.append(
            {
                "row_id": key,
                "n": N,
                "m_a_plus": m,
                "omega_printed_in_tex": printed_omega,
                "omega_correct_n_minus_m": omega_true,
                "discrepancy": omega_true - printed_omega,
                "floor_n_over_omega_printed": floor_printed,
                "floor_n_over_omega_correct": floor_true,
                "floor_unaffected": floor_printed == floor_true,
            }
        )

    if not all(r["discrepancy"] == 1000 for r in rows):
        raise AssertionError("expected off-by-1000")
    if not all(r["floor_unaffected"] for r in rows):
        raise AssertionError("floor changed — unexpected")

    cert: dict[str, Any] = {
        "status": STATUS,
        "object": "cor:bc-one-pencil worked table omega correction",
        "base_sha": "2b1a7e20654d44d0beefcd5c7d508be618b0cea1",
        "is_degenerate_by_construction": False,
        "beats_trivial_baseline": True,
        "is_tautology_under_preconditions": False,
        "evidence_type": "CANONICAL_STATEMENT_HIT",
        "verdict": "FIXED",
        "parks_for_ken": True,
        "park_reason": "correction against maintainer text (grande_finale.tex table)",
        "statement_pin": {
            "path": TEX_REL.as_posix(),
            "label": "cor:bc-one-pencil",
            "line": idx,
        },
        "printed_table_hits": printed,
        "rows": rows,
        "repair_suggestion": (
            "In cor:bc-one-pencil table, replace omega 980104→981104 (KB) and "
            "980128→981128 (M31); floor(n/omega)=2 unchanged."
        ),
        "generator_routes": {
            "omega_A": "n - m exact integer",
            "omega_B": "n + (-m)",
            "floor": "integer division n//omega both printed and corrected",
        },
        "claim_boundaries": {
            "is_counterexample": False,
            "asserts": [
                "printed omega values are n-m-1000",
                "floor(n/omega)=2 for both printed and corrected",
            ],
            "does_not_assert": [
                "that the mathematical one-pencil bound is false",
                "automatic edit of grande_finale.tex",
            ],
        },
        "honest_headline": (
            "FIXED-class table typo: omega understated by 1000; one-pencil floor 2 unaffected. "
            "PARKS for Ken (maintainer-text correction)."
        ),
    }
    cert["payload_sha256"] = payload_hash(cert)
    return cert


def run_check(root: Path, path: Path) -> None:
    cert = json.loads(path.read_text(encoding="utf-8"))
    if cert.get("payload_sha256") != payload_hash(cert):
        raise AssertionError("payload")
    rebuilt = build_certificate(root)
    if rebuilt["rows"] != cert["rows"] and [
        r["omega_correct_n_minus_m"] for r in rebuilt["rows"]
    ] != [r["omega_correct_n_minus_m"] for r in cert["rows"]]:
        raise AssertionError("drift")
    for r in cert["rows"]:
        if r["omega_correct_n_minus_m"] != N - r["m_a_plus"]:
            raise AssertionError("omega")
        if r["discrepancy"] != 1000:
            raise AssertionError("disc")
    print("RESULT: PASS")
    print("route: n-m and n+(-m); floor both sides")
    print(f"payload {cert['payload_sha256']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    root = repo_root()
    path = root / CERT_REL
    if args.emit:
        cert = build_certificate(root)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"wrote {path}")
        for r in cert["rows"]:
            print(
                f"{r['row_id']}: printed={r['omega_printed_in_tex']} "
                f"correct={r['omega_correct_n_minus_m']} delta={r['discrepancy']}"
            )
        print(f"payload={cert['payload_sha256']}")
    if args.check:
        run_check(root, path)
    if not args.emit and not args.check:
        ap.print_help()
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
