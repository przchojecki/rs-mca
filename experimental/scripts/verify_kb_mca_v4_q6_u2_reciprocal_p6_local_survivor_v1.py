#!/usr/bin/env python3
"""Verify the deployed-field reciprocal P6 local source-facet survivor.

The certificate is a local Q=6,u=2 equality-wall route cut.  It proves
that the source-facet, deck, split-quartic, reciprocal-involution, exact
P6-incidence, and degree-two GRS interpolation equations are jointly
consistent over the deployed KoalaBear field.  It does not construct a
received line, a bad slope, an active owner, or a row payment.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )


class VerificationError(RuntimeError):
    """Raised when an exact certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = (
    ROOT
    / "data"
    / "certificates"
    / "kb-mca-v4-q6-u2-reciprocal-p6-local-survivor-v1"
    / "kb_mca_v4_q6_u2_reciprocal_p6_local_survivor_v1.json"
)

TOP_LEVEL_KEYS = {
    "format",
    "status",
    "row",
    "scope",
    "witness",
    "claims",
    "nonclaims",
    "source_base_commit",
    "upstream_prs_checked",
    "payload_sha256",
}

P = 2_130_706_433
OMEGA_SQUARE = 1_923_159_404


@dataclass(frozen=True)
class Fp2:
    """Element a+b*omega of F_p[omega]/(omega^2-OMEGA_SQUARE)."""

    a: int = 0
    b: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "a", self.a % P)
        object.__setattr__(self, "b", self.b % P)

    @staticmethod
    def coerce(value: object) -> "Fp2":
        if isinstance(value, Fp2):
            return value
        if isinstance(value, int):
            return Fp2(value, 0)
        return NotImplemented

    def __add__(self, other: object) -> "Fp2":
        other_value = self.coerce(other)
        if other_value is NotImplemented:
            return NotImplemented
        return Fp2(self.a + other_value.a, self.b + other_value.b)

    __radd__ = __add__

    def __neg__(self) -> "Fp2":
        return Fp2(-self.a, -self.b)

    def __sub__(self, other: object) -> "Fp2":
        other_value = self.coerce(other)
        if other_value is NotImplemented:
            return NotImplemented
        return self + (-other_value)

    def __rsub__(self, other: object) -> "Fp2":
        other_value = self.coerce(other)
        if other_value is NotImplemented:
            return NotImplemented
        return other_value - self

    def __mul__(self, other: object) -> "Fp2":
        other_value = self.coerce(other)
        if other_value is NotImplemented:
            return NotImplemented
        return Fp2(
            self.a * other_value.a
            + OMEGA_SQUARE * self.b * other_value.b,
            self.a * other_value.b + self.b * other_value.a,
        )

    __rmul__ = __mul__

    def __pow__(
        self, exponent: int, modulus: object | None = None
    ) -> "Fp2":
        require(exponent >= 0, "negative F_p2 exponent")
        require(modulus in (None, P), "unexpected F_p2 modulus")
        result = Fp2(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result

    def __mod__(self, modulus: int) -> "Fp2":
        require(modulus == P, "unexpected F_p2 reduction modulus")
        return self

    def __eq__(self, other: object) -> bool:
        other_value = self.coerce(other)
        if other_value is NotImplemented:
            return False
        return self.a == other_value.a and self.b == other_value.b

    def __bool__(self) -> bool:
        return self.a != 0 or self.b != 0

    def is_base_field(self) -> bool:
        return self.b == 0


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def payload_hash(data: dict[str, Any]) -> str:
    unsigned = {
        key: value for key, value in data.items() if key != "payload_sha256"
    }
    return hashlib.sha256(canonical_json(unsigned).encode()).hexdigest()


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def inv(value: int | Fp2, prime: int) -> int | Fp2:
    value %= prime
    require(value != 0, "attempted inversion of zero")
    if isinstance(value, Fp2):
        return value ** (prime * prime - 2)
    return pow(value, prime - 2, prime)


def poly_trim(poly: list[int], prime: int) -> list[int]:
    result = [value % prime for value in poly]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    result = [0] * size
    for index in range(size):
        result[index] = (
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
        ) % prime
    return poly_trim(result, prime)


def poly_sub(left: list[int], right: list[int], prime: int) -> list[int]:
    return poly_add(left, [-value for value in right], prime)


def poly_scale(poly: list[int], scalar: int, prime: int) -> list[int]:
    return poly_trim([scalar * value for value in poly], prime)


def poly_mul(left: list[int], right: list[int], prime: int) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index]
                + left_value * right_value
            ) % prime
    return poly_trim(result, prime)


def poly_eval(poly: list[int], value: int, prime: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * value + coefficient) % prime
    return result


def poly_derivative(poly: list[int], prime: int) -> list[int]:
    if len(poly) <= 1:
        return [0]
    return poly_trim(
        [index * poly[index] for index in range(1, len(poly))], prime
    )


def poly_divmod(
    numerator: list[int], denominator: list[int], prime: int
) -> tuple[list[int], list[int]]:
    num = poly_trim(numerator, prime)
    den = poly_trim(denominator, prime)
    require(den != [0], "polynomial division by zero")
    if len(num) < len(den):
        return [0], num
    quotient = [0] * (len(num) - len(den) + 1)
    den_lead_inv = inv(den[-1], prime)
    while num != [0] and len(num) >= len(den):
        shift = len(num) - len(den)
        scalar = num[-1] * den_lead_inv % prime
        quotient[shift] = scalar
        subtractor = [0] * shift + [
            scalar * coefficient % prime for coefficient in den
        ]
        num = poly_sub(num, subtractor, prime)
    return poly_trim(quotient, prime), poly_trim(num, prime)


def poly_monic(poly: list[int], prime: int) -> list[int]:
    poly = poly_trim(poly, prime)
    require(poly != [0], "zero polynomial has no monic normalization")
    return poly_scale(poly, inv(poly[-1], prime), prime)


def poly_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    left = poly_trim(left, prime)
    right = poly_trim(right, prime)
    while right != [0]:
        _, remainder = poly_divmod(left, right, prime)
        left, right = right, remainder
    return poly_monic(left, prime)


def quadratic(parameter: int, prime: int) -> list[int]:
    """Return X^2-parameter*X+1 in ascending coefficient order."""
    return [1, -parameter % prime, 1]


def determinant(matrix: list[list[int]], prime: int) -> int:
    size = len(matrix)
    require(
        size > 0 and all(len(row) == size for row in matrix),
        "determinant requires a nonempty square matrix",
    )
    work = [[value % prime for value in row] for row in matrix]
    result = 1
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != 0
            ),
            None,
        )
        if pivot is None:
            return 0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            result = -result
        pivot_value = work[column][column]
        result = result * pivot_value % prime
        pivot_inverse = inv(pivot_value, prime)
        for row in range(column + 1, size):
            scalar = work[row][column] * pivot_inverse % prime
            for index in range(column, size):
                work[row][index] = (
                    work[row][index] - scalar * work[column][index]
                ) % prime
    return result % prime


def solve_quadratic_interpolant(
    xs: list[int], ys: list[int], prime: int
) -> list[int]:
    require(len(xs) == len(ys) == 3, "three interpolation anchors required")
    matrix = [
        [1, xs[index], xs[index] * xs[index] % prime, ys[index]]
        for index in range(3)
    ]
    for column in range(3):
        pivot = next(
            (
                row
                for row in range(column, 3)
                if matrix[row][column] % prime
            ),
            None,
        )
        require(pivot is not None, "singular interpolation anchor")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scalar = inv(matrix[column][column], prime)
        matrix[column] = [
            value * scalar % prime for value in matrix[column]
        ]
        for row in range(3):
            if row == column:
                continue
            scalar = matrix[row][column] % prime
            matrix[row] = [
                (matrix[row][index] - scalar * matrix[column][index])
                % prime
                for index in range(4)
            ]
    return [matrix[index][3] % prime for index in range(3)]


def cross(left: list[int], right: list[int], prime: int) -> list[int]:
    require(len(left) == len(right) == 3, "cross product has length three")
    return [
        (left[1] * right[2] - left[2] * right[1]) % prime,
        (left[2] * right[0] - left[0] * right[2]) % prime,
        (left[0] * right[1] - left[1] * right[0]) % prime,
    ]


def validate(data: dict[str, Any]) -> dict[str, Any]:
    require(set(data) == TOP_LEVEL_KEYS, "top-level certificate keys changed")
    require(
        data["format"]
        == "kb-mca-v4-q6-u2-reciprocal-p6-local-survivor-v1",
        "certificate format changed",
    )
    require(
        data["status"] == "PROVED_LOCAL_SOURCE_FACET_SURVIVOR",
        "status changed",
    )
    require(data["payload_sha256"] == payload_hash(data), "payload hash")

    row = data["row"]
    require(
        set(row)
        == {
            "field_characteristic",
            "field_extension_degree",
            "agreement",
            "B_star",
            "object",
            "workboard_item",
        },
        "row schema",
    )
    require(row["field_characteristic"] == P, "KoalaBear prime")
    require(row["field_extension_degree"] == 6, "sextic field")
    require(row["agreement"] == 1_116_048, "agreement")
    require(row["B_star"] == 274_980_728_111_395_087, "B*")
    require(row["object"] == "MCA", "object kind")
    require(row["workboard_item"] == "K3", "workboard item")

    scope = data["scope"]
    require(
        set(scope)
        == {
            "pole_partition",
            "endpoint_rows",
            "right_label_permutation",
            "signature_graph",
            "signature_path",
            "quotient_profile",
            "terminal",
            "owner_id",
            "ledger_movement",
            "active_ledger",
        },
        "scope schema",
    )
    require(scope["pole_partition"] == [6], "pole partition")
    require(scope["endpoint_rows"] == [0, 2], "endpoint rows")
    require(scope["signature_graph"] == "P6", "signature graph")
    require(scope["signature_path"] == [0, 1, 3, 4, 5, 2], "path")
    require(scope["quotient_profile"] == "RECIPROCAL", "profile")
    require(scope["terminal"] == "UNROUTED_LOCAL_COMPONENT", "terminal")
    require(scope["owner_id"] is None, "owner must remain null")
    require(scope["ledger_movement"] == 0, "ledger movement")
    require(
        scope["active_ledger"]
        == {"U_paid": None, "U_Q": None, "U_BC": None, "U_new": None},
        "active ledger must remain null",
    )

    witness = data["witness"]
    require(
        set(witness)
        == {
            "quadratic_subfield",
            "alpha_noninvariant",
            "invariant_extra_label",
            "common_parameter_multipliers",
            "free_parameter_multipliers",
            "factor_sequence_multipliers",
            "S_coefficient_multipliers",
            "P_coefficients",
            "weighted_GRS_scale_coefficients",
            "common_source_locator_coefficients",
        },
        "witness schema",
    )
    quadratic_subfield = witness["quadratic_subfield"]
    require(
        quadratic_subfield
        == {"generator": "omega", "omega_square": OMEGA_SQUARE},
        "quadratic subfield model",
    )
    require(
        pow(OMEGA_SQUARE, (P - 1) // 2, P) == P - 1,
        "omega square must be a nonsquare",
    )
    omega = Fp2(0, 1)
    require(omega * omega == OMEGA_SQUARE, "omega relation")
    alpha = [Fp2(value) for value in witness["alpha_noninvariant"]]
    require(len(alpha) == 6 and len(set(alpha)) == 6, "six source labels")
    require(all(value != 0 for value in alpha), "nonzero source labels")
    require(
        all(value * value != 1 for value in alpha),
        "noninvariant source labels avoid reciprocal fixed points",
    )
    require(alpha[3] == inv(alpha[1], P), "alpha_3=alpha_1^-1")
    require(alpha[5] == inv(alpha[4], P), "alpha_5=alpha_4^-1")
    require(witness["invariant_extra_label"] == 0, "extra invariant label")

    common = [
        Fp2(0, value)
        for value in witness["common_parameter_multipliers"]
    ]
    require(len(common) == 5, "five common parameters")
    a_value = common[1]
    b_value = common[4]
    require(
        common
        == [0, a_value, -a_value % P, -b_value % P, b_value],
        "reciprocal common-parameter order",
    )
    free = {
        int(key): Fp2(0, value)
        for key, value in witness["free_parameter_multipliers"].items()
    }
    require(set(free) == {0, 2}, "free parameter rows")
    factor_sequence = [
        Fp2(0, value)
        for value in witness["factor_sequence_multipliers"]
    ]
    require(
        factor_sequence
        == [free[0], *common, free[2]],
        "factor sequence",
    )
    require(len(set(factor_sequence)) == 7, "seven distinct factors")
    require(
        all((value * value - 4) % P != 0 for value in factor_sequence),
        "all pole quadratics are reduced",
    )
    require(
        row["field_extension_degree"] % 2 == 0,
        "quadratic split field must embed",
    )
    for value in factor_sequence:
        discriminant = (value * value - 4) % P
        require(discriminant != 0, "nonzero quadratic discriminant")
        require(
            discriminant ** ((P * P - 1) // 2)
            == 1,
            "pole quadratic does not split over F_(p^2)",
        )

    path = scope["signature_path"]
    row_factors: dict[int, tuple[int, int]] = {}
    for position, label in enumerate(path):
        row_factors[label] = (
            factor_sequence[position],
            factor_sequence[position + 1],
        )
    require(set(row_factors) == set(range(6)), "path labels")

    s_values = [
        sum(row_factors[label]) % P for label in range(6)
    ]
    p_values = [
        row_factors[label][0] * row_factors[label][1] % P
        for label in range(6)
    ]
    s_coefficients = [
        Fp2(0, value)
        for value in witness["S_coefficient_multipliers"]
    ]
    p_coefficients = [
        Fp2(value) for value in witness["P_coefficients"]
    ]
    require(len(s_coefficients) == len(p_coefficients) == 3, "quadratics")
    require(
        solve_quadratic_interpolant(alpha[:3], s_values[:3], P)
        == s_coefficients,
        "S interpolation anchors",
    )
    require(
        solve_quadratic_interpolant(alpha[:3], p_values[:3], P)
        == p_coefficients,
        "P interpolation anchors",
    )
    require(
        [poly_eval(s_coefficients, value, P) for value in alpha]
        == s_values,
        "all S interpolation equations",
    )
    require(
        [poly_eval(p_coefficients, value, P) for value in alpha]
        == p_values,
        "all P interpolation equations",
    )
    coefficient_map_determinant = (
        s_coefficients[1] * p_coefficients[2]
        - s_coefficients[2] * p_coefficients[1]
    ) % P
    require(coefficient_map_determinant != 0, "conic map rank three")

    row_polynomials = {
        label: poly_mul(
            quadratic(row_factors[label][0], P),
            quadratic(row_factors[label][1], P),
            P,
        )
        for label in range(6)
    }
    for label in range(6):
        expected = [
            1,
            -s_values[label] % P,
            (2 + p_values[label]) % P,
            -s_values[label] % P,
            1,
        ]
        require(row_polynomials[label] == expected, f"H row {label}")
        require(
            poly_gcd(
                row_polynomials[label],
                poly_derivative(row_polynomials[label], P),
                P,
            )
            == [1],
            f"row {label} squarefree",
        )

    path_edges = {
        tuple(sorted((path[index], path[index + 1])))
        for index in range(5)
    }
    for left in range(6):
        for right in range(left + 1, 6):
            gcd_degree = (
                len(poly_gcd(row_polynomials[left], row_polynomials[right], P))
                - 1
            )
            expected_degree = 2 if (left, right) in path_edges else 0
            require(
                gcd_degree == expected_degree,
                f"signature gcd {left},{right}",
            )

    scale_coefficients = [
        Fp2(value)
        for value in witness["weighted_GRS_scale_coefficients"]
    ]
    require(scale_coefficients == [1, 0, 0], "weighted GRS scale")
    barycentric_denominators = []
    for index, value in enumerate(alpha):
        denominator = Fp2(1)
        for other_index, other_value in enumerate(alpha):
            if index != other_index:
                denominator *= value - other_value
        require(denominator != 0, "barycentric denominator")
        barycentric_denominators.append(denominator)
    for moment in range(3):
        for coefficient_index in range(4):
            parity_check = Fp2(0)
            for index, value in enumerate(alpha):
                scale_value = poly_eval(scale_coefficients, value, P)
                parity_check += (
                    (value ** moment)
                    * scale_value
                    * row_polynomials[index][coefficient_index]
                    * inv(barycentric_denominators[index], P)
                )
            require(
                parity_check == 0,
                f"weighted GRS parity m={moment},c={coefficient_index}",
            )

    common_decic = [1]
    for parameter in common:
        common_decic = poly_mul(common_decic, quadratic(parameter, P), P)
    require(len(common_decic) - 1 == 10, "common decic degree")
    require(
        common_decic == list(reversed(common_decic)),
        "iota invariance",
    )
    require(
        all(
            coefficient == 0
            for index, coefficient in enumerate(common_decic)
            if index % 2
        ),
        "deck invariance",
    )
    require(
        poly_gcd(common_decic, poly_derivative(common_decic, P), P)
        == [1],
        "common decic reduced",
    )
    require(
        poly_gcd(common_decic, [-1, 0, 1], P) == [1],
        "common decic has no iota fixed root",
    )
    require(common_decic[0] != 0 and common_decic[-1] != 0, "deck branch")

    first_row = [1, -free[0] % P, -1 % P]
    second_row = [1, -free[2] % P, -1 % P]
    candidate = cross(first_row, second_row, P)
    c_value, matrix_a, matrix_b = candidate
    require(c_value != 0, "candidate scale")
    scale = inv(c_value, P)
    require(
        [value * scale % P for value in candidate] == [1, 0, 1],
        "candidate involution is lambda -> 1/lambda",
    )
    require(
        (matrix_a * matrix_a + matrix_b * c_value) % P != 0,
        "candidate involution nondegenerate",
    )

    right_permutation = scope["right_label_permutation"]
    require(
        sorted(right_permutation) == list(range(6)),
        "right-label permutation",
    )
    pole_edges = {
        (left, left) for left in range(6)
    } | {
        (left, (left - 1) % 6) for left in range(6)
    }
    require(
        all(
            right_permutation[right] != left
            for left, right in pole_edges
        ),
        "diagonal pole incidence",
    )
    for endpoint in scope["endpoint_rows"]:
        right_vertices = [endpoint, (endpoint - 1) % 6]
        source_indices = [
            right_permutation[right] for right in right_vertices
        ]
        source_values = [alpha[index] for index in source_indices]
        u_value = free[endpoint]
        require(
            sum(source_values) % P == (u_value * u_value - 2) % P,
            f"endpoint {endpoint} deck-fibre sum",
        )
        require(
            source_values[0] * source_values[1] % P == 1,
            f"endpoint {endpoint} deck-fibre product",
        )
        require(
            endpoint not in source_indices,
            f"endpoint {endpoint} diagonal source",
        )
    require(
        not any(size == 2 for size in scope["pole_partition"]),
        "free edges must not be a paid four-cycle component",
    )

    common_source_locator = poly_mul(
        [1, 1],
        poly_mul(
            [1, (2 - a_value * a_value) % P, 1],
            [1, (2 - b_value * b_value) % P, 1],
            P,
        ),
        P,
    )
    require(
        common_source_locator
        == [
            Fp2(value)
            for value in witness["common_source_locator_coefficients"]
        ],
        "common source locator",
    )
    require(
        all(
            Fp2.coerce(value).is_base_field()
            for value in common_source_locator
        ),
        "common source locator descends to F_p",
    )
    for reciprocal_pair_parameter in (
        (2 - a_value * a_value) % P,
        (2 - b_value * b_value) % P,
    ):
        discriminant = (
            reciprocal_pair_parameter * reciprocal_pair_parameter - 4
        ) % P
        require(discriminant != 0, "source-pair discriminant")
        require(
            discriminant ** ((P * P - 1) // 2) == 1,
            "common source locator does not split over F_p2",
        )
    require(
        poly_gcd(
            common_source_locator,
            poly_derivative(common_source_locator, P),
            P,
        )
        == [1],
        "five common source labels distinct",
    )
    require(
        poly_eval(common_source_locator, -1 % P, P) == 0,
        "reciprocal fixed common label",
    )
    require(
        poly_eval(common_source_locator, 1, P) != 0,
        "only one reciprocal fixed common label",
    )
    require(
        poly_eval(common_source_locator, 0, P) != 0,
        "extra invariant label distinct",
    )
    require(
        all(
            poly_eval(common_source_locator, value, P) != 0
            for value in alpha
        ),
        "common and noninvariant source labels disjoint",
    )
    require(
        common_source_locator == list(reversed(common_source_locator)),
        "source quintic reciprocal",
    )

    claims = data["claims"]
    require(
        claims
        == {
            "deployed_characteristic": True,
            "source_labels_live_in_F_p6": True,
            "source_facet_and_deck_equations": True,
            "weighted_GRS_reconstruction": True,
            "degree_2_GRS_interpolation": True,
            "smooth_conic_image": True,
            "exact_P6_signature": True,
            "reduced_common_decic": True,
            "reciprocal_profile": True,
            "active_first_match_record": False,
            "same_record_owner_supplied": False,
            "row_payment": False,
        },
        "claims changed",
    )
    require(
        data["nonclaims"]
        == [
            "received-line witness",
            "bad-slope witness",
            "survival of every earlier first-match cell",
            "active owner payment",
            "cap-68 refutation",
            "KoalaBear MCA counterexample",
            "row closure",
        ],
        "nonclaims changed",
    )
    require(
        data["source_base_commit"]
        == "93fba1be3f3299b0ba4708d88715377bbb656e45",
        "source base commit",
    )
    require(
        data["upstream_prs_checked"] == [1121, 1122, 1123, 1124, 1125],
        "upstream PR audit",
    )

    return {
        "prime": P,
        "source_labels": 12,
        "common_decic_degree": 10,
        "signature_edges": len(path_edges),
        "coefficient_map_determinant": coefficient_map_determinant,
        "terminal": scope["terminal"],
        "ledger_movement": scope["ledger_movement"],
    }


def mutate(
    data: dict[str, Any], path: tuple[object, ...], value: object
) -> dict[str, Any]:
    result = copy.deepcopy(data)
    target: Any = result
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    result["payload_sha256"] = payload_hash(result)
    return result


def tamper_selftest(data: dict[str, Any]) -> tuple[int, int]:
    tests = [
        ("prime", ("row", "field_characteristic"), P + 2),
        ("extension", ("row", "field_extension_degree"), 5),
        ("agreement", ("row", "agreement"), 1_116_047),
        ("budget", ("row", "B_star"), 274_980_728_111_395_086),
        ("object", ("row", "object"), "LIST"),
        ("partition", ("scope", "pole_partition"), [4, 2]),
        ("endpoints", ("scope", "endpoint_rows"), [0, 1]),
        ("right-map", ("scope", "right_label_permutation", 0), 4),
        ("signature", ("scope", "signature_graph"), "P2_PLUS_C4"),
        ("path", ("scope", "signature_path", 1), 3),
        ("profile", ("scope", "quotient_profile"), "D4"),
        ("terminal", ("scope", "terminal"), "PAID_SAME_RECORD_OWNER"),
        ("owner", ("scope", "owner_id"), "FAKE_OWNER"),
        ("movement", ("scope", "ledger_movement"), 1),
        ("ledger", ("scope", "active_ledger", "U_paid"), 0),
        (
            "omega-square",
            ("witness", "quadratic_subfield", "omega_square"),
            OMEGA_SQUARE + 1,
        ),
        ("alpha", ("witness", "alpha_noninvariant", 0), 1_706_416_116),
        ("alpha-fixed", ("witness", "alpha_noninvariant", 0), 1),
        ("extra-label", ("witness", "invariant_extra_label"), 1),
        (
            "common-a",
            ("witness", "common_parameter_multipliers", 1),
            1_168_433_533,
        ),
        (
            "common-order",
            ("witness", "common_parameter_multipliers", 2),
            1,
        ),
        (
            "free-0",
            ("witness", "free_parameter_multipliers", "0"),
            2,
        ),
        (
            "free-2",
            ("witness", "free_parameter_multipliers", "2"),
            1_646_993_079,
        ),
        (
            "sequence",
            ("witness", "factor_sequence_multipliers", 3),
            0,
        ),
        (
            "S",
            ("witness", "S_coefficient_multipliers", 0),
            190_235_002,
        ),
        ("P", ("witness", "P_coefficients", 0), 1_619_401_243),
        (
            "GRS-scale",
            ("witness", "weighted_GRS_scale_coefficients", 0),
            2,
        ),
        (
            "source-locator",
            ("witness", "common_source_locator_coefficients", 1),
            735_731_089,
        ),
        ("claim-active", ("claims", "active_first_match_record"), True),
        ("claim-owner", ("claims", "same_record_owner_supplied"), True),
        ("claim-payment", ("claims", "row_payment"), True),
        ("nonclaim", ("nonclaims", 0), "received-line proof"),
        ("base", ("source_base_commit",), "0" * 40),
        ("prs", ("upstream_prs_checked", 4), 1126),
    ]
    passed = 0
    for name, path, value in tests:
        candidate = mutate(data, path, value)
        try:
            validate(candidate)
        except VerificationError:
            passed += 1
        else:
            raise VerificationError(f"tamper survived: {name}")
    hash_tamper = copy.deepcopy(data)
    hash_tamper["status"] = "OPEN"
    try:
        validate(hash_tamper)
    except VerificationError:
        passed += 1
    else:
        raise VerificationError("tamper survived: stale payload hash")
    return passed, len(tests) + 1


def load_certificate() -> dict[str, Any]:
    with CERTIFICATE.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-hash", action="store_true")
    arguments = parser.parse_args()
    require(
        arguments.check or arguments.tamper_selftest or arguments.print_hash,
        "choose --check, --tamper-selftest, or --print-hash",
    )
    data = load_certificate()
    if arguments.print_hash:
        print(payload_hash(data))
    if arguments.check:
        summary = validate(data)
        print("status=PROVED_LOCAL_SOURCE_FACET_SURVIVOR")
        print(f"field=F_{summary['prime']}^6")
        print(f"source_labels={summary['source_labels']}")
        print(f"common_decic_degree={summary['common_decic_degree']}")
        print(f"signature_edges={summary['signature_edges']}")
        print(
            "coefficient_map_determinant="
            f"{summary['coefficient_map_determinant']}"
        )
        print(f"terminal={summary['terminal']}")
        print(f"ledger_movement={summary['ledger_movement']}")
    if arguments.tamper_selftest:
        passed, total = tamper_selftest(data)
        print(f"tamper_selftest={passed}/{total}")


if __name__ == "__main__":
    main()
