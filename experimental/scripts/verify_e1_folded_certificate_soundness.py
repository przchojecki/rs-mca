#!/usr/bin/env python3
"""Replay the E1 folded-certificate soundness packet."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "e1-folded-certificate-soundness"
    / "e1_folded_certificate_soundness.json"
)
NOTE = REPO / "experimental" / "notes" / "e1" / "e1_folded_certificate_soundness.md"

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e1_folded_certificate_soundness",
    "folded_box": "w in {-2,-1,0,1,2}^{N'/2}",
    "opposite_pairing": "w_x = v_x - v_{x+N'/2}",
    "antipodal": "antipodal/cyclotomic relation",
    "non_claim": "folded no-vector search",
}


def factor_int(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    factors = factor_int(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise AssertionError("no primitive root")


def order_n_generator(p: int, n: int) -> int:
    z = pow(primitive_root(p), (p - 1) // n, p)
    if pow(z, n, p) != 1 or pow(z, n // 2, p) == 1:
        raise AssertionError("not an exact 2-power root")
    return z


def folded_zero_count(n: int, p: int) -> int:
    z = order_n_generator(p, n)
    powers = [pow(z, i, p) for i in range(n // 2)]
    count = 0
    for w in itertools.product(range(-2, 3), repeat=n // 2):
        if all(x == 0 for x in w):
            continue
        if sum(x * powers[i] for i, x in enumerate(w)) % p == 0:
            count += 1
    return count


def toy_checks() -> list[dict[str, Any]]:
    certified = folded_zero_count(16, 60161)
    bad = folded_zero_count(16, 10177)
    return [
        {
            "n": 16,
            "p": 60161,
            "nonzero_folded_zero_count": certified,
            "expected": 0,
            "passes": certified == 0,
        },
        {
            "n": 16,
            "p": 10177,
            "nonzero_folded_zero_count": bad,
            "expected": 48,
            "passes": bad == 48,
        },
    ]


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "e1-folded-certificate-soundness-v1",
        "status": "PROVED_FOLDED_KERNEL_SOUNDNESS",
        "source_dag_node": "e1_folded_certificate_soundness",
        "statement": (
            "a complete zero folded-kernel search over {-2,-1,0,1,2}^{N'/2} "
            "excludes non-quotient E1 collisions at 2-power N'"
        ),
        "anchor_checks": checks,
        "toy_checks": toy_checks(),
        "dependencies": ["kernel_lattice_reframing", "2-power antipodal folding"],
        "non_claims": [
            "does not run the N'=128 or N'=256 no-vector searches",
            "does not certify an E1 open-cell payload by itself",
        ],
        "note": "experimental/notes/e1/e1_folded_certificate_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "e1-folded-certificate-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    failed_toys = [check for check in cert["toy_checks"] if not check["passes"]]
    if failed_toys:
        raise AssertionError(f"failed toy checks: {failed_toys}")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("e1-folded-certificate-soundness certificate")
    print(f"  status: {cert['status']}")
    for check in cert["toy_checks"]:
        print(
            "  toy n={n} p={p}: {count} ({status})".format(
                n=check["n"],
                p=check["p"],
                count=check["nonzero_folded_zero_count"],
                status="PASS" if check["passes"] else "FAIL",
            )
        )


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
