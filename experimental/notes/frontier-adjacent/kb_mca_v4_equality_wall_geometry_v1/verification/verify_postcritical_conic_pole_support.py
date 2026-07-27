#!/usr/bin/env python3
"""Verify conic pole-support arithmetic and endpoint design identities."""

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
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "postcritical_conic_pole_support_certificate.json"


def pole_fixture(coordinate_roots: list[list[int]]) -> dict[str, object]:
    a = len(coordinate_roots)
    require(
        all((len(roots) == 2 for roots in coordinate_roots)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:19',
    )
    total = Counter(
        root for roots in coordinate_roots for root in roots
    )
    maximum = {
        root: max(roots.count(root) for roots in coordinate_roots)
        for root in total
    }
    beta = sum(maximum.values())
    v = beta - 2
    u = a - 1
    off_block = 0
    for root, multiplicity in maximum.items():
        carriers = sum(
            roots.count(root) == multiplicity
            for roots in coordinate_roots
        )
        # All fixtures below use simple projective roots.
        require(
            multiplicity == 1,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:37',
        )
        off_block += a - carriers
    source_divisor_degree = a * v
    pole_divisor_degree = beta * u
    effective_degree = pole_divisor_degree - source_divisor_degree
    require(
        off_block == source_divisor_degree,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:42',
    )
    require(
        effective_degree == 2 * a - beta,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:43',
    )
    return {
        "a": a,
        "coordinate_roots": coordinate_roots,
        "distinct_poles": sorted(maximum),
        "beta": beta,
        "u": u,
        "v": v,
        "source_divisor_degree": source_divisor_degree,
        "pole_divisor_degree": pole_divisor_degree,
        "off_block_degree": off_block,
        "effective_divisor_degree": effective_degree,
    }


def principal_row_cases() -> list[dict[str, object]]:
    a = 12
    regular_count = 69
    selected_count = 120
    cases = []
    for d in range(a):
        for beta in range(3, 2 * a + 1):
            if beta * (d + 1) > 2 * a:
                continue
            u = a - 1 - d
            r = regular_count - d - 5 * a
            s = selected_count - 5 * beta
            if beta < 2 * a:
                require(
                    0 <= r <= u - 1,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:71',
                )
                require(
                    s >= 5,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:72',
                )
                branch = "KUNNETH_VANISHING"
            else:
                require(
                    beta == 2 * a,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:75',
                )
                require(
                    d == 0,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:76',
                )
                require(
                    r == 9,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:77',
                )
                require(
                    s == 0,
                    'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:78',
                )
                branch = "POLE_DISJOINT_ENDPOINT"
            cases.append(
                {
                    "d": d,
                    "beta": beta,
                    "u": u,
                    "effective_divisor_degree": (
                        2 * a - beta * (d + 1)
                    ),
                    "reduced_first_degree": r,
                    "reduced_negative_second_degree": s,
                    "branch": branch,
                }
            )
    return cases


def a14_r68_cases() -> list[dict[str, int]]:
    a = 14
    regular_count = 68
    selected_count = 114
    cases = []
    for d in range(a):
        for beta in range(3, 2 * a + 1):
            if beta * (d + 1) > 2 * a:
                continue
            u = a - 1 - d
            r = regular_count - d - 4 * a
            s = selected_count - 4 * beta
            require(
                r == u - 1,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:108',
            )
            require(
                s >= 2,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:109',
            )
            cases.append(
                {
                    "d": d,
                    "beta": beta,
                    "u": u,
                    "reduced_first_degree": r,
                    "reduced_negative_second_degree": s,
                }
            )
    return cases


def endpoint_design() -> dict[str, int]:
    selected_roots = 69
    blocks = 120
    block_size = 11
    vertical_degree = 22
    total_incidence = blocks * block_size
    active_roots = total_incidence // vertical_degree
    inactive_roots = selected_roots - active_roots
    remainder_degree = inactive_roots
    divisor_degree = remainder_degree * vertical_degree
    require(
        total_incidence == 1320,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:132',
    )
    require(
        active_roots == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:133',
    )
    require(
        inactive_roots == 9,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:134',
    )
    require(
        divisor_degree == 198,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:135',
    )
    return {
        "selected_roots": selected_roots,
        "blocks": blocks,
        "block_size": block_size,
        "replication": vertical_degree,
        "total_incidence": total_incidence,
        "active_roots": active_roots,
        "inactive_roots": inactive_roots,
        "remainder_polynomial_degree": remainder_degree,
        "remainder_divisor_degree": divisor_degree,
    }


def payload() -> dict[str, object]:
    endpoint_fixture = pole_fixture(
        [[10, 11], [20, 21], [30, 31], [40, 41]]
    )
    shared_fixture = pole_fixture(
        [[10, 11], [10, 21], [30, 31], [40, 41]]
    )
    result = {
        "status": (
            "PROVED_CONIC_DEGENERACY_EXCLUSION_AND_ENDPOINT_DESIGN_"
            "POLE_DISJOINT_ENDPOINT_OPEN"
        ),
        "finite_pole_fixtures": {
            "pole_disjoint": endpoint_fixture,
            "shared_pole": shared_fixture,
        },
        "principal_a12_R69_cases": principal_row_cases(),
        "a14_R68_cases": a14_r68_cases(),
        "endpoint_design": endpoint_design(),
        "claims": {
            "effective_conic_source_pole_period": "PROVED",
            "principal_common_root_branch": "IMPOSSIBLE",
            "principal_shared_coordinate_pole_branch": "IMPOSSIBLE",
            "principal_pole_disjoint_endpoint": "OPEN",
            "principal_endpoint_design": "PROVED_1_(60,11,22)",
            "principal_remainder": "EXACT_NINE_INACTIVE_ROOT_LOCATOR",
            "a14_R68_irreducible_conic": "IMPOSSIBLE",
            "reducible_conic": "OPEN",
            "cubic_and_large_circuit": "OPEN",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    fixtures = data["finite_pole_fixtures"]
    require(
        fixtures['pole_disjoint']['beta'] == 8,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:189',
    )
    require(
        fixtures['pole_disjoint']['effective_divisor_degree'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:190',
    )
    require(
        fixtures['shared_pole']['beta'] == 7,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:191',
    )
    require(
        fixtures['shared_pole']['effective_divisor_degree'] == 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:192',
    )
    principal = data["principal_a12_R69_cases"]
    endpoints = [
        case for case in principal
        if case["branch"] == "POLE_DISJOINT_ENDPOINT"
    ]
    require(
        endpoints == [{'d': 0, 'beta': 24, 'u': 11, 'effective_divisor_degree': 0, 'reduced_first_degree': 9, 'reduced_negative_second_degree': 0, 'branch': 'POLE_DISJOINT_ENDPOINT'}],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:198',
    )
    require(
        all((case['reduced_negative_second_degree'] >= 5 for case in principal if case['branch'] == 'KUNNETH_VANISHING')),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:209',
    )
    require(
        all((case['reduced_first_degree'] == case['u'] - 1 and case['reduced_negative_second_degree'] >= 2 for case in data['a14_R68_cases'])),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:214',
    )
    design = data["endpoint_design"]
    require(
        design['active_roots'] == 60,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:220',
    )
    require(
        design['inactive_roots'] == 9,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:221',
    )
    require(
        design['remainder_divisor_degree'] == 198,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:222',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_conic_pole_support.py:239',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["endpoint_design"]["active_roots"] = 59
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("conic pole-support fixtures: PASS")
    print("principal degeneracy exclusion: PASS")
    print("endpoint 1-(60,11,22) design: PASS")
    print("a14 R68 irreducible-conic exclusion: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
