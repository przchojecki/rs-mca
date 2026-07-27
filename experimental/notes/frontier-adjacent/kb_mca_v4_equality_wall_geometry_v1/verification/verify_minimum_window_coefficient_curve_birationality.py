#!/usr/bin/env python3
"""Exact arithmetic verifier for minimum-window birationality."""

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
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = (
    ROOT / "minimum_window_coefficient_curve_birationality_certificate.json"
)
S = 202_416
E = 134_944
C = 67_472


def payload() -> dict[str, object]:
    inputs = {
        12: 118_077,
        13: 119_375,
        14: 120_487,
        15: 121_451,
        16: 122_294,
    }
    rows = []
    for splitting_degree, h_min in inputs.items():
        locator_degree = C + h_min
        finite_fiber_base = E - h_min + 1
        source_budget = (
            S
            - splitting_degree * (E - h_min)
            - (splitting_degree - 1)
        )
        zero_slack_finite_floor = (
            splitting_degree - 1 - source_budget
        )
        covering_gcd = math.gcd(locator_degree, finite_fiber_base)
        rows.append(
            {
                "a": splitting_degree,
                "h_min": h_min,
                "D": locator_degree,
                "n0": finite_fiber_base,
                "source_budget": source_budget,
                "zero_slack_finite_floor": zero_slack_finite_floor,
                "covering_gcd": covering_gcd,
                "forced_covering_degree": 1,
            }
        )

    result = {
        "status": "PROVED_ENDPOINT_BIRATIONALITY_OPEN_CAP",
        "rows": rows,
        "theorem": {
            "covering_divisors": "d_cov divides D and n0",
            "endpoint_conclusion": "d_cov=1 for a=12,...,16",
            "low_degree_cover": "EXCLUDED_AT_MINIMUM_WINDOWS",
            "next_target": "BIRATIONAL_MINIMUM_ROW_COMPLEMENTARY_DEFECT_RIGIDITY",
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
    rows = data["rows"]
    require(
        [row['a'] for row in rows] == [12, 13, 14, 15, 16],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_minimum_window_coefficient_curve_birationality.py:77',
    )
    require(
        [row['source_budget'] for row in rows] == [1, 7, 5, 7, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_minimum_window_coefficient_curve_birationality.py:78',
    )
    require(
        [row['zero_slack_finite_floor'] for row in rows] == [10, 5, 8, 7, 14],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_minimum_window_coefficient_curve_birationality.py:79',
    )
    require(
        all((row['zero_slack_finite_floor'] >= 2 for row in rows)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_minimum_window_coefficient_curve_birationality.py:82',
    )
    require(
        all((row['covering_gcd'] == 1 for row in rows)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_minimum_window_coefficient_curve_birationality.py:83',
    )
    require(
        all((row['D'] + row['n0'] == S + 1 for row in rows)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_minimum_window_coefficient_curve_birationality.py:84',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_minimum_window_coefficient_curve_birationality.py:101',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["rows"][2]["covering_gcd"] = 2
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("minimum-window source budget: PASS")
    print("coefficient-curve covering gcd: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
