#!/usr/bin/env python3
"""Exact arithmetic checks for the rank-one source-fiber reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


S = 202_416
E = 134_944
C = 67_472
J = 981_105
DELTA_FLOOR = 3_912
MAX_A = 16
ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "kb-mca-v4-rank-one-split-scroll-source-fiber-reduction-v1/"
    "certificate.json"
)


def canonical_json(payload: dict) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def build_payload() -> dict:
    source_rows = []
    for a in range(2, MAX_A + 1):
        h_min = E - (S - (a - 1)) // a
        h_max = min(E - 1, ((a - 1) * J) // 54 - C)
        source_rows.append(
            {
                "a": a,
                "exceptional_parameter_cap": 16 - a,
                "regular_parameter_floor": 53 + a,
                "h_min": h_min,
                "incidence_h_max": h_max,
                "minimum_residual_budget":
                    S - a * (E - h_min) - (a - 1),
                "first_moment_feasible": h_min <= h_max,
            }
        )

    a3 = source_rows[1]
    a2_low_margin = 62 * (C + 33_737) - J
    a3_contradiction_margin = 56 * (2 * C) - 2 * (J + 2 * C)
    eliminated = [
        row["a"] for row in source_rows
        if not row["first_moment_feasible"]
    ]
    surviving = [
        row for row in source_rows
        if row["first_moment_feasible"]
    ]

    gates = {
        "constant_relations": S == E + C and E == 2 * C and S == 3 * C,
        "source_fiber_minimum": (S + E - 1) // E == 2,
        "exact_q_two": (
            (S + C) // E == 2
            and (S + E - 1) // E == 2
        ),
        "exact_q_one_lower_range": (
            (S + DELTA_FLOOR) // E == 1
            and (S + C - 1) // E == 1
        ),
        "a2_lower_range_contradiction":
            a2_low_margin == 5_293_853,
        "kernel_degree_cap": MAX_A == 2 * (9 - 1),
        "a3_regular_floor": a3["regular_parameter_floor"] == 56,
        "a3_contradiction": (
            not a3["first_moment_feasible"]
            and a3_contradiction_margin == 5_324_766
        ),
        "eliminated_splitting_degrees":
            eliminated == list(range(2, 12)),
        "surviving_splitting_degrees":
            [row["a"] for row in surviving] == list(range(12, 17)),
        "closed_delta_interval": (
            surviving[0]["h_min"] == 118_077
            and DELTA_FLOOR < surviving[0]["h_min"]
        ),
        "surviving_windows": [
            (
                row["a"],
                row["regular_parameter_floor"],
                row["h_min"],
                row["incidence_h_max"],
            )
            for row in surviving
        ] == [
            (12, 65, 118_077, 132_382),
            (13, 66, 119_375, 134_943),
            (14, 67, 120_487, 134_943),
            (15, 68, 121_451, 134_943),
            (16, 69, 122_294, 134_943),
        ],
        "monicity_refinement": (
            E - (S - 2) // 3 == C + 1
        ),
        "all_minimum_residual_budgets": all(
            0 <= row["minimum_residual_budget"]
            for row in source_rows
        ),
    }

    payload = {
        "theorem": "rank-one split-scroll source-fiber reduction",
        "status": "proved partial exclusion; full cap 68 open",
        "constants": {
            "source_size": S,
            "pencil_degree": E,
            "half_degree": C,
            "carrier_offset": J,
            "delta_floor": DELTA_FLOOR,
            "max_kernel_splitting_degree": MAX_A,
            "lower_excess_q": 1,
            "exact_surviving_low_excess_q": 2,
        },
        "proved": {
            "source_scalar_roots":
                "simple roots exactly equal the projective source-map values",
            "source_fiber_count": "a = |f(Sigma)|",
            "persistent_core_bound":
                "ag <= a(delta-e)+s-(a-1)",
            "incidence_bound":
                "54(c+h) <= (a-1)J, h=delta-g",
            "exceptional_parameter_bound": "D_exc <= 16-a",
            "regular_parameter_bound": "R_reg >= 53+a",
            "lower_range_a2_contradiction_margin": a2_low_margin,
            "a3_excluded": True,
            "a3_contradiction_margin": a3_contradiction_margin,
            "eliminated_splitting_degrees": eliminated,
            "excluded_delta_interval":
                [DELTA_FLOOR, surviving[0]["h_min"] - 1],
            "excluded_delta_count":
                surviving[0]["h_min"] - DELTA_FLOOR,
        },
        "surviving_cases": surviving,
        "remaining":
            "a=12..16 low-excess windows and general-excess descent",
        "source_rows": source_rows,
        "gates": gates,
        "all_gates_pass": all(gates.values()),
    }
    return payload


def payload_sha256(payload: dict) -> str:
    data = canonical_json(payload).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def load_certificate(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_certificate(path: Path) -> int:
    expected = build_payload()
    actual = load_certificate(path)
    if actual != expected:
        print("certificate_mismatch")
        return 1
    if not expected["all_gates_pass"]:
        print("gate_failure")
        return 1
    print("RESULT = PASS")
    print(f"payload_sha256 = {payload_sha256(expected)}")
    print(
        "excluded_delta_interval = "
        f"{expected['proved']['excluded_delta_interval']}"
    )
    print(
        "surviving_cases = "
        f"{[(row['a'], row['h_min'], row['incidence_h_max']) for row in expected['surviving_cases']]}"
    )
    return 0


def tamper_selftest(path: Path) -> int:
    actual = load_certificate(path)
    mutations = []

    bad = json.loads(json.dumps(actual))
    bad["proved"]["a3_excluded"] = False
    mutations.append(bad)

    bad = json.loads(json.dumps(actual))
    bad["proved"]["excluded_delta_interval"][1] += 1
    mutations.append(bad)

    bad = json.loads(json.dumps(actual))
    bad["surviving_cases"][0]["h_min"] += 1
    mutations.append(bad)

    expected = build_payload()
    rejected = sum(mutation != expected for mutation in mutations)
    if rejected != len(mutations):
        print("tamper_selftest_failure")
        return 1
    print(f"TAMPER SELF-TEST = PASS {rejected}/{len(mutations)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=CERTIFICATE_PATH,
    )
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    if args.emit:
        payload = build_payload()
        args.certificate.write_text(
            canonical_json(payload),
            encoding="utf-8",
            newline="\n",
        )
        print(f"wrote {args.certificate}")
        print(f"payload_sha256 = {payload_sha256(payload)}")
        return 0
    if args.check:
        return check_certificate(args.certificate)
    if args.tamper_selftest:
        return tamper_selftest(args.certificate)

    parser.error("choose --emit, --check, or --tamper-selftest")
    return 2


if __name__ == "__main__":
    sys.exit(main())
