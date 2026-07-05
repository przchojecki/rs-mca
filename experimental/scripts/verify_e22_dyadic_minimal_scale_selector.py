#!/usr/bin/env python3
"""Replay the E22 dyadic minimal-scale selector packet."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
NOTE = REPO / "experimental" / "notes" / "thresholds" / "e22_dyadic_minimal_scale_selector.md"
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "e22-dyadic-minimal-scale-selector"
    / "e22_dyadic_minimal_scale_selector.json"
)

ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "e22_dyadic_minimal_scale_selector",
    "admissible_set": "A(R) = {M : M > t and |B_M(R)| < M}",
    "unique_minimum": "unique minimal admissible modulus",
    "non_claim": "does not assemble a pricing column",
}


def fibers(n: int, modulus: int) -> list[frozenset[int]]:
    assert n % modulus == 0
    step = n // modulus
    return [frozenset(range(r, n, step)) for r in range(step)]


def recover_tail(n: int, modulus: int, support: set[int]) -> set[int]:
    full = [fiber for fiber in fibers(n, modulus) if fiber <= support]
    full_union = set().union(*full) if full else set()
    return set(support) - full_union


def admissible_moduli(n: int, t: int, support: set[int]) -> list[int]:
    out = []
    modulus = 1
    while modulus <= n:
        if modulus > t and len(recover_tail(n, modulus, support)) < modulus:
            out.append(modulus)
        modulus *= 2
    return out


def selector_check() -> dict[str, object]:
    n = 16
    t = 2
    checked = 0
    selected: dict[str, int] = {}
    for size in range(n + 1):
        for combo in combinations(range(n), size):
            support = set(combo)
            mods = admissible_moduli(n, t, support)
            if not mods:
                continue
            checked += 1
            if mods != sorted(mods):
                raise AssertionError("admissible moduli are not sorted")
            if mods[0] != min(mods):
                raise AssertionError("first admissible modulus is not the minimum")
            selected[",".join(map(str, combo))] = mods[0]

    sample = {0, 1, 4, 5, 8}
    sample_moduli = admissible_moduli(n, t, sample)
    return {
        "toy_n": n,
        "toy_t": t,
        "supports_with_selector": checked,
        "selected_count": len(selected),
        "sample_support": sorted(sample),
        "sample_moduli": sample_moduli,
        "sample_selected": sample_moduli[0],
        "all_checks_pass": checked > 0
        and len(selected) == checked
        and sample_moduli[0] == min(sample_moduli),
    }


def build_certificate() -> dict[str, object]:
    note_text = NOTE.read_text(encoding="utf-8")
    cert = {
        "schema": "e22-dyadic-minimal-scale-selector-v1",
        "status": "PROVED",
        "source_dag_node": "e22_dyadic_minimal_scale_selector",
        "anchor_checks": {
            "note_exists": NOTE.exists(),
            **{name: needle in note_text for name, needle in ANCHORS.items()},
        },
        "selector_check": selector_check(),
        "non_claims": [
            "does not compute cross-scale overlaps",
            "does not assemble a pricing column",
            "does not alter Papers A-D",
        ],
        "note": "experimental/notes/thresholds/e22_dyadic_minimal_scale_selector.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, object]) -> None:
    if cert["schema"] != "e22-dyadic-minimal-scale-selector-v1":
        raise AssertionError("unexpected schema")
    if cert.get("status") != "PROVED":
        raise AssertionError("status must be PROVED")
    if cert.get("source_dag_node") != "e22_dyadic_minimal_scale_selector":
        raise AssertionError("source DAG node mismatch")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    check = cert.get("selector_check")
    if not isinstance(check, dict) or not check.get("all_checks_pass"):
        raise AssertionError("selector check failed")


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
