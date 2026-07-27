#!/usr/bin/env python3
"""Exact regression for the source-partition Cremona descent."""

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

from verify_complement_locator_interpolation_descent import (
    add,
    divmod_poly,
    mul,
    scale,
)


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "source_partition_cremona_descent_certificate.json"
S = 202_416
E = 134_944


def product(polynomials: list[list[int]]) -> list[int]:
    out = [1]
    for polynomial in polynomials:
        out = mul(out, polynomial)
    return out


def omit_product(
    polynomials: list[list[int]], omitted: int
) -> list[int]:
    return product(
        [
            polynomial
            for index, polynomial in enumerate(polynomials)
            if index != omitted
        ]
    )


def finite_regression() -> dict[str, object]:
    source_factors = [
        [1, 1],
        [2, 1],
        [3, 1],
        [4, 1],
    ]
    residuals = [
        [5, 1],
        [6],
        [7, 1],
        [8],
    ]
    source_product = product(source_factors)
    residual_product = product(residuals)
    coefficients = [
        mul(
            divmod_poly(source_product, source_factors[index])[0],
            residuals[index],
        )
        for index in range(4)
    ]
    psi = [
        mul(source_factors[index], omit_product(residuals, index))
        for index in range(4)
    ]

    inverse_coordinates = [
        omit_product(psi, index)
        for index in range(4)
    ]
    common = product([residual_product, residual_product])
    quotients = []
    for index, coordinate in enumerate(inverse_coordinates):
        quotient, remainder = divmod_poly(
            coordinate, mul(common, coefficients[index])
        )
        require(
            remainder == [0],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_source_partition_cremona_descent.py:81',
        )
        require(
            quotient == [1],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_source_partition_cremona_descent.py:82',
        )
        quotients.append(quotient[0])

    selected_coefficients = [3, 5, 7, 11]
    selected_locator = [0]
    transformed = [0]
    for index, coefficient in enumerate(selected_coefficients):
        selected_locator = add(
            selected_locator, scale(coefficients[index], coefficient)
        )
        transformed = add(
            transformed, scale(inverse_coordinates[index], coefficient)
        )
    expected_transformed = mul(common, selected_locator)
    require(
        transformed == expected_transformed,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_source_partition_cremona_descent.py:96',
    )

    return {
        "source_factor_degrees": [
            len(polynomial) - 1 for polynomial in source_factors
        ],
        "residual_degrees": [
            len(polynomial) - 1 for polynomial in residuals
        ],
        "coefficient_degrees": [
            len(polynomial) - 1 for polynomial in coefficients
        ],
        "cremona_degrees": [
            len(polynomial) - 1 for polynomial in psi
        ],
        "inverse_common_degree": len(common) - 1,
        "inverse_coordinate_quotients": quotients,
        "selected_hypersurface_identity": (
            transformed == expected_transformed
        ),
    }


def endpoint_rows() -> list[dict[str, int]]:
    inputs = {
        12: 118_077,
        13: 119_375,
        14: 120_487,
        15: 121_451,
        16: 122_294,
    }
    rows = []
    for splitting_degree, h_min in inputs.items():
        n0 = E - h_min + 1
        source_budget = (
            S
            - splitting_degree * (E - h_min)
            - (splitting_degree - 1)
        )
        rows.append(
            {
                "a": splitting_degree,
                "h_min": h_min,
                "n0": n0,
                "source_budget": source_budget,
                "cremona_degree_cap": n0 + source_budget,
            }
        )
    return rows


def payload() -> dict[str, object]:
    result = {
        "status": "PROVED_CREMONA_DESCENT_OPEN_RIGIDITY",
        "finite_regression": finite_regression(),
        "endpoint_rows": endpoint_rows(),
        "theorem": {
            "coordinates": "Psi_j=Lambda_(Sigma_j)*product_(k!=j) Rtilde_k",
            "inverse": "Cr(Psi)_j=R_*^(a-2)*Qbar_j",
            "selected_equation": "H_i(Psi)=R_*^(a-2)*pbar_i",
            "covering_degree": "PRESERVED",
            "next_target": "CREMONA_DESCENDED_SELECTED_VERTEX_RIGIDITY",
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
    finite = data["finite_regression"]
    require(
        finite['selected_hypersurface_identity'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_source_partition_cremona_descent.py:171',
    )
    require(
        finite['inverse_coordinate_quotients'] == [1, 1, 1, 1],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_source_partition_cremona_descent.py:172',
    )
    require(
        [row['cremona_degree_cap'] for row in data['endpoint_rows']] == [16869, 15577, 14463, 13501, 12652],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_source_partition_cremona_descent.py:173',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_source_partition_cremona_descent.py:192',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["endpoint_rows"][0]["cremona_degree_cap"] += 1
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("source-partition Cremona identity: PASS")
    print("selected-hypersurface pullback: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
