#!/usr/bin/env python3
"""Verify the E1 250-bit exhibit field by Pocklington's theorem."""

from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path
from typing import Any


CERT_PATH = Path(
    "experimental/data/certificates/e1-pocklington-250bit-exhibit-field/"
    "e1_pocklington_250bit_exhibit_field.json"
)

C = 562949953421383
F = 1 << 200
P = 904625697166646869347790708689937759412227977745095982970820953353127723009
A = 3

RHO_128 = 440266185830122294862552098878717819794821358702875176198798016633729926114
RHO_256 = 368095729527972287347366462180303065908636718991804826343652948937354262881


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def root_record(order: int, rho: int) -> dict[str, Any]:
    require(order in (128, 256), "unexpected E1 folded order")
    require(rho == pow(A, (P - 1) // order, P), f"rho_{order} formula mismatch")
    require(pow(rho, order, P) == 1, f"rho_{order}^{order} is not 1")
    half_power = pow(rho, order // 2, P)
    require(half_power != 1, f"rho_{order} has smaller order")
    return {
        "order": order,
        "rho": str(rho),
        "formula": f"{A}^((p-1)/{order}) mod p",
        "pow_order_mod_p": "1",
        "pow_half_order_mod_p": str(half_power),
        "exact_order": order,
    }


def build_certificate() -> dict[str, Any]:
    require(P == C * F + 1, "p != c*2^200 + 1")
    require(P.bit_length() == 250, "p bit length mismatch")
    require(P < (1 << 256), "p violates field-size bound")
    require(P % 256 == 1, "p is not 1 mod 256")
    require((P - 1) % F == 0, "2^200 does not divide p-1")
    require(F * F > P, "Pocklington factor does not exceed sqrt(p)")

    fermat_mod = pow(A, P - 1, P)
    half_power = pow(A, (P - 1) // 2, P)
    half_gcd = gcd(half_power - 1, P)
    require(fermat_mod == 1, "base-3 Fermat congruence failed")
    require(half_gcd == 1, "Pocklington gcd condition failed")

    roots = [root_record(128, RHO_128), root_record(256, RHO_256)]

    return {
        "schema": "rs-mca.experimental.e1_pocklington_250bit_exhibit_field.v1",
        "status": "PROVED",
        "source_dag_node": "e1_pocklington_250bit_exhibit_field",
        "object": "E1 named exhibit field",
        "field": {
            "label": "F_p",
            "p": str(P),
            "bit_length": P.bit_length(),
            "less_than_2_256": P < (1 << 256),
            "p_mod_256": P % 256,
        },
        "pocklington": {
            "c": str(C),
            "known_factor": "2^200",
            "known_factor_value": str(F),
            "known_factor_prime_divisors": [2],
            "cofactor": str((P - 1) // F),
            "factor_square_exceeds_p": F * F > P,
            "base": A,
            "base_power_p_minus_1_mod_p": str(fermat_mod),
            "base_power_half_minus_one_gcd_p": str(half_gcd),
            "criterion": "Pocklington with known factor 2^200 > sqrt(p)",
        },
        "roots": roots,
        "consumers": [
            "e1_folded_certificate_cell_128_payload",
            "e1_folded_certificate_cell_256_payload",
        ],
        "non_claims": [
            "not a uniform-in-field theorem",
            "does not by itself close either E1 folded no-vector payload",
            "does not assert a fixed list of official row primes",
        ],
    }


def emit_certificate(path: Path, certificate: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")


def check_certificate(path: Path, expected: dict[str, Any]) -> None:
    loaded = json.loads(path.read_text())
    require(loaded == expected, f"certificate mismatch at {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", nargs="?", const=CERT_PATH, type=Path)
    parser.add_argument("--check", nargs="?", const=CERT_PATH, type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.emit is not None:
        emit_certificate(args.emit, certificate)
        print(f"WROTE: {args.emit}")
    if args.check is not None:
        check_certificate(args.check, certificate)
        print(f"PASS: certificate matches {args.check}")
    if args.emit is None and args.check is None:
        print("PASS: E1 250-bit Pocklington exhibit field")


if __name__ == "__main__":
    main()
