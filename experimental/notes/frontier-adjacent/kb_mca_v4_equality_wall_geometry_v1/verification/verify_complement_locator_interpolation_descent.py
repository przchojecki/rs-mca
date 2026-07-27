#!/usr/bin/env python3
"""Finite-field regression for complement-locator interpolation descent."""

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


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "complement_locator_interpolation_certificate.json"
FIELD = 101
S = 202_416
E = 134_944
C = 67_472
J = 981_105


def inv(x: int) -> int:
    return pow(x % FIELD, FIELD - 2, FIELD)


def trim(poly: list[int]) -> list[int]:
    out = [x % FIELD for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def add(a: list[int], b: list[int]) -> list[int]:
    out = [0] * max(len(a), len(b))
    for i in range(len(out)):
        out[i] = (
            (a[i] if i < len(a) else 0)
            + (b[i] if i < len(b) else 0)
        ) % FIELD
    return trim(out)


def sub(a: list[int], b: list[int]) -> list[int]:
    return add(a, [(-x) % FIELD for x in b])


def scale(a: list[int], c: int) -> list[int]:
    return trim([(c * x) % FIELD for x in a])


def mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % FIELD
    return trim(out)


def evaluate(poly: list[int], x: int) -> int:
    out = 0
    for coeff in reversed(poly):
        out = (out * x + coeff) % FIELD
    return out


def divmod_poly(
    dividend: list[int], divisor: list[int]
) -> tuple[list[int], list[int]]:
    rem = trim(dividend)
    divisor = trim(divisor)
    if divisor == [0]:
        raise ZeroDivisionError
    if len(rem) < len(divisor):
        return [0], rem
    quotient = [0] * (len(rem) - len(divisor) + 1)
    lead_inv = inv(divisor[-1])
    while rem != [0] and len(rem) >= len(divisor):
        shift = len(rem) - len(divisor)
        coeff = rem[-1] * lead_inv % FIELD
        quotient[shift] = coeff
        rem = sub(rem, [0] * shift + scale(divisor, coeff))
    return trim(quotient), trim(rem)


def lagrange(points: list[int], values: list[int]) -> list[int]:
    result = [0]
    for i, ti in enumerate(points):
        basis = [1]
        denominator = 1
        for j, tj in enumerate(points):
            if i == j:
                continue
            basis = mul(basis, [(-tj) % FIELD, 1])
            denominator = denominator * (ti - tj) % FIELD
        result = add(
            result,
            scale(basis, values[i] * inv(denominator) % FIELD),
        )
    return trim(result)


def interpolate_polynomials(
    points: list[int], values: list[list[int]]
) -> list[list[int]]:
    max_x = max(len(poly) for poly in values)
    coefficient_t_polys = []
    for x_degree in range(max_x):
        coefficient_t_polys.append(
            lagrange(
                points,
                [
                    poly[x_degree] if x_degree < len(poly) else 0
                    for poly in values
                ],
            )
        )
    max_t = max(len(poly) for poly in coefficient_t_polys)
    result = [[0] for _ in range(max_t)]
    for x_degree, t_poly in enumerate(coefficient_t_polys):
        for t_degree, coeff in enumerate(t_poly):
            if len(result[t_degree]) <= x_degree:
                result[t_degree].extend(
                    [0] * (x_degree + 1 - len(result[t_degree]))
                )
            result[t_degree][x_degree] = coeff
    return [trim(poly) for poly in result]


def bivariate_mul(
    a: list[list[int]], b: list[list[int]]
) -> list[list[int]]:
    result = [[0] for _ in range(len(a) + len(b) - 1)]
    for i, a_x in enumerate(a):
        for j, b_x in enumerate(b):
            result[i + j] = add(result[i + j], mul(a_x, b_x))
    return [trim(poly) for poly in result]


def divide_t_factor(
    numerator: list[list[int]], divisor: list[int]
) -> tuple[list[list[int]], list[list[int]]]:
    max_x = max(len(poly) for poly in numerator)
    quotient_columns = []
    remainder_columns = []
    for x_degree in range(max_x):
        t_poly = [
            poly[x_degree] if x_degree < len(poly) else 0
            for poly in numerator
        ]
        quotient, remainder = divmod_poly(t_poly, divisor)
        quotient_columns.append(quotient)
        remainder_columns.append(remainder)

    def transpose(columns: list[list[int]]) -> list[list[int]]:
        max_t = max(len(poly) for poly in columns)
        rows = [[0] for _ in range(max_t)]
        for x_degree, poly in enumerate(columns):
            for t_degree, coeff in enumerate(poly):
                if len(rows[t_degree]) <= x_degree:
                    rows[t_degree].extend(
                        [0] * (x_degree + 1 - len(rows[t_degree]))
                    )
                rows[t_degree][x_degree] = coeff
        return [trim(poly) for poly in rows]

    return transpose(quotient_columns), transpose(remainder_columns)


def regression() -> dict[str, object]:
    # Synthetic a=2 family:
    # lambda=t, P(t,X)=1+t(X-sigma), p_t=P/lambda is monic, and
    # its root sigma-1/t is placed in the fixed carrier.
    sigma = 50
    points = [1, 2, 3, 4, 5]
    roots = [(sigma - inv(t)) % FIELD for t in points]

    carrier = [1]
    for root in roots:
        carrier = mul(carrier, [(-root) % FIELD, 1])

    locators = [[(-root) % FIELD, 1] for root in roots]
    complements = []
    for locator in locators:
        quotient, remainder = divmod_poly(carrier, locator)
        require(
            remainder == [0],
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:184',
        )
        complements.append(quotient)

    q_bivariate = interpolate_polynomials(points, complements)
    p_bivariate = [[1], [(-sigma) % FIELD, 1]]
    numerator = bivariate_mul(p_bivariate, q_bivariate)

    # Subtract lambda(t) R_U(X).
    numerator[1] = sub(numerator[1], carrier)

    h_t = [1]
    for t in points:
        h_t = mul(h_t, [(-t) % FIELD, 1])

    source_multiple, remainder = divide_t_factor(numerator, h_t)
    require(
        all((poly == [0] for poly in remainder)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:199',
    )
    require(
        len(source_multiple) == 1,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:200',
    )  # a-2=0

    source_locator = [(-sigma) % FIELD, 1]
    descended, source_remainder = divmod_poly(
        source_multiple[0], source_locator
    )
    require(
        source_remainder == [0],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:206',
    )

    rows = []
    for x in roots:
        incidence = [
            i for i, locator in enumerate(locators)
            if evaluate(locator, x) == 0
        ]
        q_at_x = [
            evaluate(x_poly, x) for x_poly in q_bivariate
        ]
        complement_zeros = [
            i for i, t in enumerate(points)
            if evaluate(q_at_x, t) == 0
        ]
        rows.append(
            {
                "x": x,
                "incidence": incidence,
                "complement_zero_indices": complement_zeros,
                "m": len(incidence),
            }
        )

    return {
        "field": FIELD,
        "source_point": sigma,
        "selected_parameters": points,
        "carrier_roots": roots,
        "interpolant_t_degree": len(q_bivariate) - 1,
        "descended_t_degree": len(source_multiple) - 1,
        "source_quotient_degree": len(descended) - 1,
        "carrier_rows": rows,
        "pass": all(
            row["m"] == 1
            and len(row["complement_zero_indices"]) == len(points) - 1
            for row in rows
        ),
    }


def resultant_budget_ledger() -> list[dict[str, int]]:
    a = 12
    regular = 69
    rows = []
    for h in (118_077, 118_599):
        locator_degree = C + h
        carrier_size = J + locator_degree
        mds_deficit = (
            (a - 1) * carrier_size
            - regular * locator_degree
        )
        source_budget = S - a * (E - h) - (a - 1)
        resultant_degree_bound = (
            a * locator_degree
            + (a - 1) * (carrier_size - S - 1)
        )
        selected_incidences = regular * locator_degree
        excess = resultant_degree_bound - selected_incidences
        require(
            excess == mds_deficit + source_budget,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:265',
        )
        rows.append(
            {
                "h": h,
                "locator_degree": locator_degree,
                "carrier_size": carrier_size,
                "selected_incidences": selected_incidences,
                "mds_deficit": mds_deficit,
                "source_budget": source_budget,
                "resultant_degree_bound": resultant_degree_bound,
                "resultant_excess": excess,
            }
        )
    return rows


def payload() -> dict[str, object]:
    result = {
        "status": "PROVED_REDUCTION_OPEN_CAP",
        "finite_regression": regression(),
        "resultant_budget_ledger": resultant_budget_ledger(),
        "theorem": {
            "identity": "Pbar*Q-lambda*R_U=H_T*Lambda_Sigma*S",
            "t_degree": "deg_t S <= a-2",
            "x_degree": "deg_X S <= n-s-1",
            "minimum_row": "eta=0 implies deg A=0 and deg B<=a-2",
            "resultant_excess": "deg_X Res_t(Pbar,C)-R*D <= Delta_R+B_a(h)",
            "active_owner": "NONE",
            "cap_68": "OPEN",
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
        finite['pass'],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:305',
    )
    require(
        finite['interpolant_t_degree'] == 4,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:306',
    )
    require(
        finite['descended_t_degree'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:307',
    )
    require(
        all((row['m'] == 1 for row in finite['carrier_rows'])),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:308',
    )
    ledger = data["resultant_budget_ledger"]
    require(
        [row['resultant_excess'] for row in ledger] == [30314, 6302],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:310',
    )
    require(
        [row['mds_deficit'] for row in ledger] == [30313, 37],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:311',
    )
    require(
        [row['source_budget'] for row in ledger] == [1, 6265],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:312',
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
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_complement_locator_interpolation_descent.py:329',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["resultant_budget_ledger"][0]["resultant_excess"] += 1
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("complement interpolation identity: PASS")
    print("source divisor and row factorization: PASS")
    print("resultant budget identity: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
