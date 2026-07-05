#!/usr/bin/env python3
"""Replay the E1 250-bit Pocklington exhibit-field certificate."""

from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "e1-pocklington-250bit-exhibit-field"
    / "e1_pocklington_250bit_exhibit_field.json"
)
NOTE = REPO / "experimental" / "notes" / "e1" / "e1_pocklington_250bit_exhibit_field.md"

C = 562949953421383
F = 1 << 200
P = 904625697166646869347790708689937759412227977745095982970820953353127723009
A = 3
RHO_128 = 440266185830122294862552098878717819794821358702875176198798016633729926114
RHO_256 = 368095729527972287347366462180303065908636718991804826343652948937354262881

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e1_pocklington_250bit_exhibit_field",
    "pocklington": "Use Pocklington's theorem",
    "known_factor": "F = 2^200",
    "rho_128": "rho_128",
    "rho_256": "rho_256",
    "non_claim": "folded no-vector certificate",
}


def order_check(rho: int, order: int) -> dict[str, Any]:
    return {
        "order": order,
        "power_order_is_one": pow(rho, order, P) == 1,
        "half_power_not_one": pow(rho, order // 2, P) != 1,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
        "p_equals_c_times_f_plus_one": P == C * F + 1,
        "p_bit_length_250": P.bit_length() == 250,
        "p_less_than_2_256": P < (1 << 256),
        "p_congruent_1_mod_256": P % 256 == 1,
        "known_factor_exceeds_sqrt_p": F * F > P,
        "pocklington_power": pow(A, P - 1, P) == 1,
        "pocklington_gcd": gcd(pow(A, (P - 1) // 2, P) - 1, P) == 1,
        "rho_128_value": RHO_128 == pow(A, (P - 1) // 128, P),
        "rho_256_value": RHO_256 == pow(A, (P - 1) // 256, P),
    }
    cert = {
        "schema": "e1-pocklington-250bit-exhibit-field-v1",
        "status": "PROVED_BY_POCKLINGTON_REPLAY",
        "source_dag_node": "e1_pocklington_250bit_exhibit_field",
        "field": {"p": P, "bit_length": P.bit_length(), "c": C, "known_factor": F},
        "pocklington": {"base": A, "known_factor_prime_divisors": [2]},
        "roots": {
            "128": {"rho": RHO_128, **order_check(RHO_128, 128)},
            "256": {"rho": RHO_256, **order_check(RHO_256, 256)},
        },
        "anchor_checks": checks,
        "non_claims": [
            "does not certify either folded no-vector payload",
            "does not prove the E1 open-cell payload",
        ],
        "note": "experimental/notes/e1/e1_pocklington_250bit_exhibit_field.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "e1-pocklington-250bit-exhibit-field-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed checks: {failed}")
    for root in cert["roots"].values():
        if not root["power_order_is_one"] or not root["half_power_not_one"]:
            raise AssertionError(f"failed root order check: {root}")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("e1-pocklington-250bit-exhibit-field certificate")
    print(f"  status: {cert['status']}")
    print(f"  p bit length: {cert['field']['bit_length']}")
    for name, ok in cert["anchor_checks"].items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text())
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
