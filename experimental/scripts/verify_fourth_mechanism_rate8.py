#!/usr/bin/env python3
"""Replay the rate-1/8 fourth-mechanism wedge packet."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "fourth_mechanism_rate8.md"
CAP_END_CERT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "cap-end-sharpening"
    / "cap_end_sharpening.json"
)
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "fourth-mechanism-rate8"
    / "fourth_mechanism_rate8.json"
)

REQUIRED_WEDGE = Decimal("0.00707")
CAP_END_GAIN = Decimal(1) / Decimal(16)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "fourth_mechanism_rate8",
    "dependency": "cap_end_sharpening",
    "gain": "1/16 = 0.0625",
    "inequality": "1/16 > 0.00707",
    "non_claim": "does not alter Papers A-D",
}


def dependency_check() -> dict[str, object]:
    cert = json.loads(CAP_END_CERT.read_text(encoding="utf-8"))
    point = cert.get("point", {})
    return {
        "path": str(CAP_END_CERT.relative_to(REPO)),
        "schema": cert.get("schema"),
        "status": cert.get("status"),
        "source_dag_node": cert.get("source_dag_node"),
        "gain_fraction": point.get("gain_fraction") if isinstance(point, dict) else None,
        "accepted": cert.get("schema") == "cap-end-sharpening-v1"
        and cert.get("status") == "PROVED"
        and cert.get("source_dag_node") == "cap_end_sharpening"
        and isinstance(point, dict)
        and point.get("all_checks_pass")
        and point.get("gain_fraction") == "1/16",
    }


def wedge_check() -> dict[str, object]:
    margin = CAP_END_GAIN - REQUIRED_WEDGE
    return {
        "rate": "1/8",
        "required_wedge": str(REQUIRED_WEDGE),
        "cap_end_gain_fraction": "1/16",
        "cap_end_gain": str(CAP_END_GAIN),
        "margin": str(margin),
        "gain_to_requirement_ratio": str((CAP_END_GAIN / REQUIRED_WEDGE).quantize(Decimal("0.000001"))),
        "route": "cap_end_sharpening",
        "verdict": "PASS" if CAP_END_GAIN > REQUIRED_WEDGE else "FAIL",
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "fourth-mechanism-rate8-v1",
        "status": "PROVED",
        "source_dag_node": "fourth_mechanism_rate8",
        "dependencies": [dependency_check()],
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "wedge_check": wedge_check(),
        "non_claims": [
            "does not assemble the full clean-rate corridor ledger",
            "does not treat the rate-1/2 band",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/fourth_mechanism_rate8.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "fourth-mechanism-rate8-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "fourth_mechanism_rate8":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not all(dep.get("accepted") for dep in cert["dependencies"]):
        raise AssertionError("dependency check failed")
    check = cert.get("wedge_check")
    if not isinstance(check, dict) or check.get("verdict") != "PASS":
        raise AssertionError("wedge check failed")
    if Decimal(str(check["cap_end_gain"])) <= Decimal(str(check["required_wedge"])):
        raise AssertionError("cap-end gain does not clear the wedge")


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
