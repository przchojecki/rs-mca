#!/usr/bin/env python3
"""Replay the exact bounded-scale census counts packet."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "census_exact_counts.md"
BOUNDED_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "census-bounded-scales"
    / "census_bounded_scales.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "census-exact-counts"
    / "census_exact_counts.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "census_exact_counts",
    "dependency": "census_bounded_scales",
    "exact_count": "K = binom(N', l')",
    "diophantine": "B* = floor(q / 2^128)",
    "non_claim": "certified lower-bound strength",
}

RATE_TABLE = {
    "1/2": {"k": 2**40, "t": 8_592_912_739, "Nprime": 128, "selected": 64, "want_log2": 124.171},
    "1/4": {"k": 2**39, "t": 7_014_660_390, "Nprime": 128, "selected": 94, "want_log2": 103.244},
    "1/8": {"k": 2**38, "t": 4_722_556_392, "Nprime": 256, "selected": 222, "want_log2": 140.896},
    "1/16": {"k": 2**37, "t": 2_943_177_800, "Nprime": 512, "selected": 478, "want_log2": 176.588},
}


def dependency_check() -> dict[str, object]:
    cert = json.loads(BOUNDED_CERT.read_text(encoding="utf-8"))
    return {
        "path": str(BOUNDED_CERT.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "accepted": cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == "census_bounded_scales",
    }


def exact_table() -> dict[str, object]:
    n = 2**41
    rows: dict[str, object] = {}
    ok = True
    for rate, params in RATE_TABLE.items():
        k = int(params["k"])
        t = int(params["t"])
        nprime = int(params["Nprime"])
        selected = int(params["selected"])
        want = float(params["want_log2"])
        j = n - k - t
        forced = j * nprime / n
        count = math.comb(nprime, selected)
        got = math.log2(count)
        log_ok = abs(got - want) <= 0.002
        ratio_ok = abs(selected - forced) <= 2.0
        ok = ok and log_ok and ratio_ok
        rows[rate] = {
            "n": n,
            "k": k,
            "t": t,
            "j": j,
            "Nprime": nprime,
            "selected": selected,
            "forced_selected_float": round(forced, 6),
            "exact_count": count,
            "log2_count": round(got, 6),
            "pinned_log2": want,
            "log_check": log_ok,
            "forced_ratio_check": ratio_ok,
            "bit_length": count.bit_length(),
        }
    return {"rows": rows, "all_checks_pass": ok}


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "census-exact-counts-v1",
        "status": "PROVED",
        "source_dag_node": "census_exact_counts",
        "dependencies": [dependency_check()],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "exact_table": exact_table(),
        "non_claims": [
            "does not supply the certified lower-bound strength L",
            "does not prove the residual window is empty",
            "does not close a deployed adjacent theorem",
        ],
        "note": "experimental/notes/thresholds/census_exact_counts.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "census-exact-counts-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")
    table = cert["exact_table"]
    if not isinstance(table, dict) or not table.get("all_checks_pass"):
        raise AssertionError("exact table check failed")


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
