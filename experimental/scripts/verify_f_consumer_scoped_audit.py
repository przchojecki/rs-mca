#!/usr/bin/env python3
"""Verify source markers for the Conjecture F consumer-scope audit."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


OUTPUT = Path(
    "experimental/data/certificates/f-consumer-scoped-audit/"
    "f_consumer_scoped_audit.json"
)


@dataclass(frozen=True)
class Marker:
    path: str
    phrases: tuple[str, ...]


MARKERS = [
    Marker(
        "experimental/notes/roadmaps/proof_sketch/s3b_iii_3_fibers_and_noanchor.md",
        (
            "prob:perfiber",
            "COORDINATE-plane sections",
            "fiber(Z)",
            "ker M(Z)",
        ),
    ),
    Marker(
        "experimental/notes/roadmaps/proof_sketch/s7_list_side.md",
        (
            "L1 battle is Conjecture F",
            "petal-structured",
        ),
    ),
    Marker(
        "experimental/notes/l1/l1_full_list_quotient_proof_program.md",
        (
            "Mixed-petal sunflower amplification",
            "CONJECTURAL",
            "Maximal sunflower residual frontier",
        ),
    ),
]


def marker_payload(marker: Marker) -> dict[str, Any]:
    path = Path(marker.path)
    text = path.read_text()
    hits = {}
    for phrase in marker.phrases:
        idx = text.find(phrase)
        if idx < 0:
            raise AssertionError(f"missing marker {phrase!r} in {marker.path}")
        line = text.count("\n", 0, idx) + 1
        hits[phrase] = {"line": line}
    return {"path": marker.path, "markers": hits}


def build_certificate() -> dict[str, Any]:
    source_markers = [marker_payload(marker) for marker in MARKERS]
    consumers = [
        {
            "id": "prefix_perfiber",
            "classification": "coordinate_slice_prefix_fiber",
            "audit_result": "SCOPED",
            "source": "s3b_iii_3_fibers_and_noanchor.md",
        },
        {
            "id": "mca_slope_fiber",
            "classification": "hankel_pencil_kernel_flat",
            "audit_result": "SCOPED",
            "source": "s3b_iii_3_fibers_and_noanchor.md",
        },
        {
            "id": "list_imgfib_sunflower_residual",
            "classification": "petal_structured_auxiliary_list_plane_family",
            "audit_result": "ESCAPING_CONSUMER",
            "source": "s7_list_side.md + l1_full_list_quotient_proof_program.md",
        },
    ]
    return {
        "schema": "f-consumer-scoped-audit-v1",
        "status": "AUDIT_PARTIAL_NO_GLOBAL_DEMOTION",
        "roadmap_task": "A0/QF.9 f_consumer_scoped audit",
        "question": (
            "Does every current Conjecture F consumer lie in coordinate-slice/"
            "prefix-fiber flats or Hankel-pencil kernel flats?"
        ),
        "answer": "NO_NOT_GLOBALLY",
        "consumers": consumers,
        "escaping_consumer": "list_imgfib_sunflower_residual",
        "conservative_next_step": (
            "Open scoped proof attempts for coordinate-prefix and Hankel-kernel "
            "families only; keep general Conjecture F live until the PMA-wide "
            "sunflower residual is reduced, proved, or refuted."
        ),
        "source_markers": source_markers,
    }


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("Conjecture F consumer-scope audit")
    print(f"  schema: {cert['schema']}")
    print(f"  answer: {cert['answer']}")
    for consumer in cert["consumers"]:
        print(
            f"  {consumer['id']}: {consumer['audit_result']} "
            f"({consumer['classification']})"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {OUTPUT}")
    if args.check:
        actual = json.loads(args.check.read_text())
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()

