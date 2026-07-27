#!/usr/bin/env python3
"""Validate the guarded Q=6,s=6,u=2 normalized-model search artifact."""

from __future__ import annotations
class VerificationError(RuntimeError):
    """Raised when an exact verifier condition fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(str(message))


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )



import argparse
import copy
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "experiments" / "q6_u2_normalized_model_search.cpp"
OUTPUT = (
    ROOT / "experiments" / "q6_u2_normalized_model_search_output.txt"
)
REPORT = ROOT / "experiments" / "q6_u2_normalized_model_search_report.md"

EXPECTED = {
    "status": "NO_FIXTURE",
    "field": "2130706433",
    "rows": "6",
    "common_poles": "10",
    "free_edge_poles": "12",
    "required_owned_edges": "4",
    "common_occurrence": "2",
    "grs_crosscheck_trials": "20000",
    "identical_zero_edge_branch": "NO_FIXTURE",
    "distinct_zero_edge_branch": "NO_FIXTURE",
    "distinct_common_pairs": "21945",
}


def parse_output(text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        key, value = line.split("=", 1)
        require(
            key not in parsed,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:37',
        )
        parsed[key] = value
    return parsed


def validate(parsed: dict[str, str]) -> None:
    require(
        parsed == EXPECTED,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:43',
    )
    source = SOURCE.read_text(encoding="utf-8")
    require(
        'common_occurrences[root] >= 2' in source,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:45',
    )
    require(
        'count == 2' in source,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:46',
    )
    require(
        'grs_degree_two_valid_direct' in source,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:47',
    )
    require(
        'find_identical_zero_edge_fixture' in source,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:48',
    )
    require(
        'rank-three fixture' in source,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:49',
    )

    report = REPORT.read_text(encoding="utf-8")
    require(
        'experimental' in report,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:52',
    )
    require(
        'evidence' in report,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:53',
    )
    require(
        'not a proof over' in report,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:54',
    )
    require(
        'actual divisor' in report,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:55',
    )
    require(
        'no same-record owner payment' in report,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:56',
    )


def tamper_selftest() -> int:
    mutations: list[dict[str, str]] = []
    for key, value in [
        ("status", "PROVED"),
        ("common_occurrence", "1"),
        ("grs_crosscheck_trials", "0"),
        ("identical_zero_edge_branch", "FIXTURE"),
        ("distinct_zero_edge_branch", "FIXTURE"),
    ]:
        forged = copy.deepcopy(EXPECTED)
        forged[key] = value
        mutations.append(forged)

    rejected = 0
    for forged in mutations:
        try:
            validate(forged)
        except VerificationError:
            rejected += 1
    require(
        rejected == len(mutations),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_q6_u2_normalized_model_search_artifact.py:78',
    )
    return rejected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    parsed = parse_output(OUTPUT.read_text(encoding="utf-8"))
    validate(parsed)
    rejected = tamper_selftest() if args.tamper_selftest else 0

    print("normalized-model artifact status: PASS")
    print("exact common-pole multiplicity: PASS")
    print("weighted-GRS direct cross-check marker: PASS")
    print("proof-status guardrail: PASS")
    if args.tamper_selftest:
        print(f"tamper mutations rejected: PASS {rejected}/5")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
