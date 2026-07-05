#!/usr/bin/env python3
"""Replay the SOV forced-root recursion algebra packet."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "sov" / "sov_forced_root_recursion_algebra.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "sov-forced-root-recursion-algebra"
    / "sov_forced_root_recursion_algebra.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "sov_forced_root_recursion_algebra",
    "triangular_step": "2 s_{d-h} + known higher terms",
    "obstruction_coordinates": "O_i = [X^i](S^2 - L)",
    "non_claim": "does not prove the SOV value-set bound",
}


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def locator_from_roots(roots: list[int], p: int) -> list[int]:
    coeffs = [1]
    for root in roots:
        nxt = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            nxt[i] = (nxt[i] - coeff * root) % p
            nxt[i + 1] = (nxt[i + 1] + coeff) % p
        coeffs = nxt
    return coeffs


def square_shift_root(locator: list[int], p: int, h: int) -> list[int]:
    inv2 = pow(2, -1, p)
    s = [0] * (h + 1)
    s[h] = 1
    for degree in range(2 * h - 1, h - 1, -1):
        unknown = degree - h
        known = 0
        lo = max(0, degree - h)
        hi = min(h, degree)
        for i in range(lo, hi + 1):
            j = degree - i
            if not (0 <= j <= h):
                continue
            if i == unknown or j == unknown:
                continue
            known = (known + s[i] * s[j]) % p
        s[unknown] = ((locator[degree] - known) * inv2) % p
    return s


def forced_obstructions(locator: list[int], p: int, h: int) -> tuple[list[int], list[int], int]:
    root = square_shift_root(locator, p, h)
    root_square = poly_mul(root, root, p)
    obstructions = [(root_square[i] - locator[i]) % p for i in range(1, h)]
    constant_obstruction = (root_square[0] - locator[0]) % p
    return root, obstructions, constant_obstruction


def is_square_mod(a: int, p: int) -> bool:
    return a % p == 0 or pow(a, (p - 1) // 2, p) == 1


def recursion_check() -> dict[str, Any]:
    checks = []
    primes = {5: 101, 6: 65537, 10: 65537, 21: 65537, 40: 65537}
    for h, p in primes.items():
        rng = random.Random(17 * h)
        roots = rng.sample(range(2, p - 1), h)
        a_poly = locator_from_roots(roots, p)
        delta = 13 + h
        b_poly = list(a_poly)
        b_poly[0] = (b_poly[0] + delta) % p
        locator = poly_mul(a_poly, b_poly, p)
        root, obstructions, constant_obstruction = forced_obstructions(locator, p, h)
        midpoint = [((a + b) * pow(2, -1, p)) % p for a, b in zip(a_poly, b_poly)]
        expected_constant = (delta * delta * pow(4, -1, p)) % p
        ok = (
            root == midpoint
            and all(v == 0 for v in obstructions)
            and constant_obstruction == expected_constant
            and constant_obstruction != 0
            and is_square_mod(constant_obstruction, p)
        )
        checks.append({"h": h, "p": p, "delta": delta, "ok": ok})

    h = 10
    p = 65537
    roots = random.Random(99).sample(range(2, p - 1), h)
    a_poly = locator_from_roots(roots, p)
    b_poly = list(a_poly)
    b_poly[0] = (b_poly[0] + 17) % p
    locator = poly_mul(a_poly, b_poly, p)
    _, obs0, _ = forced_obstructions(locator, p, h)
    perturbed = list(locator)
    perturbed[h - 1] = (perturbed[h - 1] + 1) % p
    _, obs1, _ = forced_obstructions(perturbed, p, h)
    sensitivity_ok = (obs1[-1] - obs0[-1]) % p == (-1) % p and obs0[:-1] == obs1[:-1]

    return {
        "midpoint_checks": checks,
        "midpoint_checks_passed": all(row["ok"] for row in checks),
        "sensitivity_gate_passed": sensitivity_ok,
        "total_checks": len(checks) + 1,
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    cert = {
        "schema": "sov-forced-root-recursion-algebra-v1",
        "status": "PROVED_FORCED_ROOT_REPLAY",
        "source_dag_node": "sov_forced_root_recursion_algebra",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "recursion_check": recursion_check(),
        "non_claims": ["does not prove the SOV value-set bound for actual anchored-core families"],
        "note": "experimental/notes/sov/sov_forced_root_recursion_algebra.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "sov-forced-root-recursion-algebra-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert["recursion_check"]
    if not (check["midpoint_checks_passed"] and check["sensitivity_gate_passed"]):
        raise AssertionError(f"failed recursion check: {check}")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
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
        actual = json.loads(args.check.read_text())
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print(f"{cert['status']}: {cert['recursion_check']}")


if __name__ == "__main__":
    main()
