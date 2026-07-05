#!/usr/bin/env python3
"""Replay the L1 petal squarefree ledger-soundness certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "l1-petal-squarefree-classification-ledger-soundness"
    / "l1_petal_squarefree_classification_ledger_soundness.json"
)
NOTE = (
    REPO
    / "experimental"
    / "notes"
    / "l1"
    / "l1_petal_squarefree_classification_ledger_soundness.md"
)


ANCHORS = {
    "status": "Status: PROVED.",
    "source_node": "petal_squarefree_classification_ledger_soundness",
    "disjoint_cover": "disjoint cover of `X`",
    "charged_records": "charged records, each citing an already paid family",
    "uncharged_records": "uncharged records, each carrying a bound",
    "counting_dependency": "finite-union counting lemma",
    "non_claim": "does not construct the squarefree classification ledger",
}


def ledger_sample() -> dict[str, Any]:
    universe = ["k0", "k1", "k2", "k3"]
    charged = {
        "k0": "paid_tail_family",
        "k1": "paid_norm_family",
    }
    uncharged = {
        "k2": {"coefficient": 5, "exponent": 3},
        "k3": {"coefficient": 7, "exponent": 4},
    }
    max_uncharged_records = 2

    charged_keys = set(charged)
    uncharged_keys = set(uncharged)
    covered = charged_keys | uncharged_keys
    universe_set = set(universe)
    checks = {
        "covers_universe": covered == universe_set,
        "records_disjoint": charged_keys.isdisjoint(uncharged_keys),
        "charged_citations_nonempty": all(bool(citation) for citation in charged.values()),
        "uncharged_exponents_nonnegative": all(
            record["exponent"] >= 0 for record in uncharged.values()
        ),
        "uncharged_coefficients_positive": all(
            record["coefficient"] > 0 for record in uncharged.values()
        ),
        "uncharged_record_count_bounded": len(uncharged) <= max_uncharged_records,
    }
    return {
        "universe": universe,
        "charged": charged,
        "uncharged": uncharged,
        "max_uncharged_records": max_uncharged_records,
        "checks": checks,
        "passes": all(checks.values()),
    }


def build_certificate() -> dict[str, Any]:
    note_text = NOTE.read_text()
    checks = {
        "note_exists": NOTE.exists(),
        **{name: needle in note_text for name, needle in ANCHORS.items()},
    }
    cert = {
        "schema": "l1-petal-squarefree-classification-ledger-soundness-v1",
        "status": "PROVED_LEDGER_SEMANTICS",
        "source_dag_node": "petal_squarefree_classification_ledger_soundness",
        "statement": (
            "a complete disjoint charged/uncharged squarefree ledger with "
            "paid citations and c-independent uncharged bounds satisfies the "
            "squarefree-kernel classification payload"
        ),
        "anchor_checks": checks,
        "sample_ledger": ledger_sample(),
        "dependencies": [
            "definition of petal_squarefree_kernel_classification_payload",
            "petal_squarefree_classification_counting_soundness for aggregate counts",
        ],
        "non_claims": [
            "does not construct the squarefree classification ledger",
            "does not certify a proposed ledger payload",
            "does not close the L1 mixed/growing residual by itself",
        ],
        "note": "experimental/notes/l1/l1_petal_squarefree_classification_ledger_soundness.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "l1-petal-squarefree-classification-ledger-soundness-v1":
        raise AssertionError("unexpected schema")
    failed = [name for name, ok in cert["anchor_checks"].items() if not ok]
    if failed:
        raise AssertionError(f"failed anchor checks: {failed}")
    if not cert["sample_ledger"]["passes"]:
        raise AssertionError(f"sample ledger failed: {cert['sample_ledger']}")
    if "complete disjoint" not in cert["statement"]:
        raise AssertionError("statement must record complete disjoint ledger semantics")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("l1-petal-squarefree-classification-ledger-soundness certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    for name, ok in cert["anchor_checks"].items():
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    for name, ok in cert["sample_ledger"]["checks"].items():
        print(f"  sample {name}: {'PASS' if ok else 'FAIL'}")


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
