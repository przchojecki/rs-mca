#!/usr/bin/env python3
"""Finite Hilbert diagnostics and exact arithmetic for PRCI."""

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
import hashlib
import json
from pathlib import Path

from verify_reciprocal_cauchy_separator_target import (
    interpolation_profile,
)


ROOT = Path(__file__).resolve().parent
CERTIFICATE = (
    ROOT / "postcritical_reciprocal_cauchy_interpolation_certificate.json"
)


def koalabear_arithmetic() -> dict[str, int]:
    h_min = 118_077
    h_max = 118_599

    def minimum_rows(h: int) -> int:
        return 59 * (67_472 + h) - 10 * 981_105

    def cremona_degree(h: int) -> int:
        return 11 * h - 1_281_978

    closed_values = [
        h
        for h in range(h_min, h_max + 1)
        if minimum_rows(h) > 60 * cremona_degree(h)
    ]
    return {
        "h_min": h_min,
        "h_max": h_max,
        "conditional_closed_min": min(closed_values),
        "conditional_closed_max": max(closed_values),
        "conditional_closed_count": len(closed_values),
        "remaining_min": max(closed_values) + 1,
        "remaining_max": h_max,
        "remaining_count": h_max - max(closed_values),
        "endpoint_minimum_rows": minimum_rows(h_min),
        "endpoint_cremona_degree": cremona_degree(h_min),
        "endpoint_bezout_cap": 60 * cremona_degree(h_min),
        "endpoint_margin": (
            minimum_rows(h_min) - 60 * cremona_degree(h_min)
        ),
    }


def payload() -> dict[str, object]:
    profiles = [
        interpolation_profile(3, 6, 301),
        interpolation_profile(3, 7, 302),
        interpolation_profile(4, 8, 303),
        interpolation_profile(4, 9, 304),
        interpolation_profile(5, 10, 305),
        interpolation_profile(5, 11, 306),
    ]
    below_threshold = interpolation_profile(5, 6, 401)
    result = {
        "status": (
            "EXPERIMENTAL_KPRCI_OPEN_UNIVERSAL_FALSE_"
            "CONDITIONAL_REDUCTION_PROVED"
        ),
        "finite_profiles_at_or_above_threshold": profiles,
        "below_threshold_guardrail": below_threshold,
        "koalabear_conditional_arithmetic": koalabear_arithmetic(),
        "claims": {
            "universal_postcritical_surjectivity": "FALSE",
            "koalabear_postcritical_surjectivity": "OPEN",
            "selected_record_semantic_or_interpolation": "OPEN",
            "known_block_line_planted_branch": "PROVED_SEPARATELY",
            "characteristic_13_guardrail": (
                "SEE postcritical_characteristic13_guardrail.json"
            ),
            "surjectivity_to_separator": "PROVED",
            "a12_R69_conditional_reduction": "PROVED",
            "cap_68": "OPEN",
            "active_owner": "NONE",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    profiles = data["finite_profiles_at_or_above_threshold"]
    require(
        all((case['separator_defect'] == 0 for case in profiles)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:96',
    )
    guardrail = data["below_threshold_guardrail"]
    require(
        guardrail['a'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:98',
    )
    require(
        guardrail['R'] == 6,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:99',
    )
    require(
        guardrail['separator_defect'] == 5,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:100',
    )
    arithmetic = data["koalabear_conditional_arithmetic"]
    require(
        arithmetic['conditional_closed_min'] == 118077,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:102',
    )
    require(
        arithmetic['conditional_closed_max'] == 118283,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:103',
    )
    require(
        arithmetic['conditional_closed_count'] == 207,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:104',
    )
    require(
        arithmetic['remaining_count'] == 316,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:105',
    )
    require(
        arithmetic['endpoint_minimum_rows'] == 1136341,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:106',
    )
    require(
        arithmetic['endpoint_cremona_degree'] == 16869,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:107',
    )
    require(
        arithmetic['endpoint_bezout_cap'] == 1012140,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:108',
    )
    require(
        arithmetic['endpoint_margin'] == 124201,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:109',
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    data = payload()
    validate(data)
    if args.emit:
        CERTIFICATE.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n"
        )
    if args.check:
        require(
            json.loads(CERTIFICATE.read_text()) == data,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_reciprocal_cauchy_interpolation.py:126',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["below_threshold_guardrail"]["separator_defect"] = 0
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("postcritical reciprocal-Cauchy diagnostics: PASS")
    print("KoalaBear degree-60 conditional arithmetic: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
