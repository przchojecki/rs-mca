#!/usr/bin/env python3
"""Check Paper D v9 aperiodic Hankel eliminant packets.

The JSON schema catches the structural contract.  This script adds the
arithmetical checks that are easiest to get wrong in generated packets:
``j=n-A``, ``t=A-k``, residual labels, regular-minor degree/root hashes, and
declared root-union numerators when the packet includes inline root tables.  If
the packet gives an explicit polynomial-basis field model, the checker verifies
the model is compatible with the row field, verifies the modulus is irreducible,
and evaluates encoded extension roots directly in that field.  In small fields,
it also enumerates the full finite field to check that inline root tables have
not omitted any roots.  For packets emitted by the regular-minor extractor, it
also checks the rank-pivot audit metadata needed to justify singular
regular-bucket declarations, rank-witness degree-bound packets, common-gcd
minor families, and pivot-atlas records.  Pivot eliminant targets with
machine-readable coefficient/root tables are checked arithmetically.  Local
packet references such as removed-ledger certificates are resolved, including
JSON pointer fragments.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import re
from typing import Any


DEFAULT_SCHEMA = Path("scripts/aperiodic_eliminant_schema.json")
ROOT_COMPLETENESS_ENUMERATION_LIMIT = 1_000_000
INLINE_MINOR_REPLAY_SIZE_LIMIT = 16


class PacketError(Exception):
    """Raised when a packet fails a schema or arithmetic check."""


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PacketError(f"{path}: invalid JSON: {exc}") from exc


def hash_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def hash_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def require_int_list(values: Any, field: str) -> list[int]:
    if not isinstance(values, list):
        raise PacketError(f"{field}: expected a list")
    out: list[int] = []
    for value in values:
        if not isinstance(value, int):
            raise PacketError(f"{field}: expected integer entries")
        out.append(value)
    return out


def normalize_int_list(values: Any, field: str) -> list[int]:
    out = require_int_list(values, field)
    return sorted(set(out))


def poly_degree(coefficients: list[int]) -> int:
    degree = len(coefficients) - 1
    while degree > 0 and coefficients[degree] == 0:
        degree -= 1
    return degree


def poly_eval_mod(coefficients: list[int], value: int, modulus: int) -> int:
    total = 0
    power = 1
    for coefficient in coefficients:
        total = (total + coefficient * power) % modulus
        power = (power * value) % modulus
    return total


def poly_mul_mod_coefficients(
    left: list[int], right: list[int], modulus: int
) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_coeff in enumerate(left):
        for j, right_coeff in enumerate(right):
            out[i + j] = (out[i + j] + left_coeff * right_coeff) % modulus
    return out


def poly_power_mod_coefficients(
    factor: list[int], exponent: int, modulus: int
) -> list[int]:
    out = [1]
    for _ in range(exponent):
        out = poly_mul_mod_coefficients(out, factor, modulus)
    return out


def trim_mod_coefficients(coefficients: list[int], modulus: int) -> list[int]:
    out = [coefficient % modulus for coefficient in coefficients]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def require_exact_roots(
    listed_roots: list[int],
    actual_roots: list[int],
    location: str,
) -> None:
    if listed_roots == actual_roots:
        return
    listed = set(listed_roots)
    actual = set(actual_roots)
    missing = sorted(actual - listed)
    extra = sorted(listed - actual)
    details = []
    if missing:
        details.append(f"missing roots {missing}")
    if extra:
        details.append(f"extra non-roots {extra}")
    raise PacketError(f"{location}: incomplete root table ({'; '.join(details)})")


def monomial_exact_roots(
    coefficients: list[int],
    modulus: int | None = None,
) -> list[int] | None:
    nonzero_indices = []
    for index, coefficient in enumerate(coefficients):
        value = coefficient % modulus if modulus is not None else coefficient
        if value != 0:
            nonzero_indices.append(index)
    if len(nonzero_indices) != 1:
        return None
    return [0] if nonzero_indices[0] > 0 else []


def repeated_root_power_exact_roots_mod(
    coefficients: list[int],
    roots: list[int],
    modulus: int,
) -> list[int] | None:
    if len(roots) != 1:
        return None
    coefficients = [coefficient % modulus for coefficient in coefficients]
    degree = poly_degree(coefficients)
    if degree <= 0:
        return [] if coefficients[0] % modulus else None
    root = roots[0] % modulus
    leading = coefficients[degree] % modulus
    expected = poly_power_mod_coefficients([(-root) % modulus, 1], degree, modulus)
    expected = [(leading * coefficient) % modulus for coefficient in expected]
    while len(expected) < len(coefficients):
        expected.append(0)
    if expected[: len(coefficients)] == coefficients:
        return [root]
    return None


def parse_prime_field(field_name: str) -> int | None:
    match = re.fullmatch(r"F_(\d+)", field_name)
    if not match:
        return None
    return int(match.group(1))


def parse_prime_power_field(field_name: str) -> tuple[int, int] | None:
    match = re.fullmatch(r"F_(\d+)(?:\^(\d+))?", field_name)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2) or "1")


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def ppoly_trim(poly: list[int], prime: int) -> list[int]:
    out = [coeff % prime for coeff in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def ppoly_degree(poly: list[int], prime: int) -> int:
    return len(ppoly_trim(poly, prime)) - 1


def ppoly_sub(left: list[int], right: list[int], prime: int) -> list[int]:
    size = max(len(left), len(right))
    out = [0] * size
    for index in range(size):
        out[index] = (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        ) % prime
    return ppoly_trim(out, prime)


def ppoly_mod(poly: list[int], modulus: list[int], prime: int) -> list[int]:
    work = ppoly_trim(poly, prime)
    modulus = ppoly_trim(modulus, prime)
    mod_degree = len(modulus) - 1
    inv_mod_lead = pow(modulus[-1], -1, prime)
    while len(work) - 1 >= mod_degree and not (len(work) == 1 and work[0] == 0):
        lead = (work[-1] * inv_mod_lead) % prime
        if lead:
            offset = len(work) - len(modulus)
            for index, coeff in enumerate(modulus):
                work[offset + index] = (work[offset + index] - lead * coeff) % prime
        work = ppoly_trim(work, prime)
    return work


def ppoly_mul_mod(
    left: list[int], right: list[int], modulus: list[int], prime: int
) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, left_coeff in enumerate(left):
        for j, right_coeff in enumerate(right):
            out[i + j] = (out[i + j] + left_coeff * right_coeff) % prime
    return ppoly_mod(out, modulus, prime)


def ppoly_pow_mod(
    base: list[int], exponent: int, modulus: list[int], prime: int
) -> list[int]:
    out = [1]
    factor = ppoly_mod(base, modulus, prime)
    while exponent:
        if exponent & 1:
            out = ppoly_mul_mod(out, factor, modulus, prime)
        factor = ppoly_mul_mod(factor, factor, modulus, prime)
        exponent >>= 1
    return out


def ppoly_gcd(left: list[int], right: list[int], prime: int) -> list[int]:
    a = ppoly_trim(left, prime)
    b = ppoly_trim(right, prime)
    while not (len(b) == 1 and b[0] == 0):
        a, b = b, ppoly_mod(a, b, prime)
    inv_lead = pow(a[-1], -1, prime)
    return [(coeff * inv_lead) % prime for coeff in a]


def ppoly_monic(poly: list[int], prime: int) -> list[int]:
    out = ppoly_trim(poly, prime)
    if len(out) == 1 and out[0] == 0:
        return out
    inv_lead = pow(out[-1], -1, prime)
    return [(coeff * inv_lead) % prime for coeff in out]


def ppoly_gcd_many(polynomials: list[list[int]], prime: int) -> list[int]:
    if not polynomials:
        raise PacketError("need a nonzero minor polynomial for common gcd")
    out = ppoly_trim(polynomials[0], prime)
    for polynomial in polynomials[1:]:
        out = ppoly_gcd(out, polynomial, prime)
    return ppoly_monic(out, prime)


def prime_divisors(value: int) -> list[int]:
    out = []
    remaining = value
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            out.append(divisor)
            while remaining % divisor == 0:
                remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        out.append(remaining)
    return out


def frobenius_power_x(modulus: list[int], prime: int, iterations: int) -> list[int]:
    out = [0, 1]
    for _ in range(iterations):
        out = ppoly_pow_mod(out, prime, modulus, prime)
    return out


def is_irreducible_mod_prime(modulus: list[int], prime: int) -> bool:
    modulus = ppoly_trim(modulus, prime)
    degree = len(modulus) - 1
    if degree < 1 or modulus[-1] != 1:
        return False
    if degree == 1:
        return True
    x_poly = [0, 1]
    for divisor in prime_divisors(degree):
        test = frobenius_power_x(modulus, prime, degree // divisor)
        if ppoly_degree(ppoly_gcd(ppoly_sub(test, x_poly, prime), modulus, prime), prime):
            return False
    final = frobenius_power_x(modulus, prime, degree)
    return ppoly_mod(ppoly_sub(final, x_poly, prime), modulus, prime) == [0]


class PolynomialBasisField:
    """Finite field F_p[X]/(modulus), with low-degree-first coefficients."""

    def __init__(self, prime: int, modulus: list[int]):
        if not is_prime(prime):
            raise PacketError("field_model.p must be prime")
        if len(modulus) < 2:
            raise PacketError("field_model.modulus must have positive degree")
        if modulus[-1] % prime != 1:
            raise PacketError("field_model.modulus must be monic")
        self.p = prime
        self.modulus = [value % prime for value in modulus]
        self.degree = len(modulus) - 1
        self.size = prime**self.degree
        self.zero = (0,) * self.degree
        self.one = (1,) + (0,) * (self.degree - 1)
        if not is_irreducible_mod_prime(self.modulus, self.p):
            raise PacketError("field_model.modulus must be irreducible over F_p")

    @classmethod
    def from_packet(cls, packet: dict[str, Any]) -> "PolynomialBasisField | None":
        extractor = packet.get("extractor")
        if not isinstance(extractor, dict):
            return None
        model = extractor.get("field_model")
        if not isinstance(model, dict):
            return None
        if model.get("kind") != "polynomial_basis":
            raise PacketError("unsupported extractor.field_model.kind")
        if "p" not in model or "modulus" not in model:
            raise PacketError("field_model needs p and modulus")
        if not isinstance(model["p"], int):
            raise PacketError("field_model.p must be integer")
        modulus = require_int_list(model["modulus"], "field_model.modulus")
        field = cls(model["p"], modulus)
        if "degree" in model and model["degree"] != field.degree:
            raise PacketError("field_model.degree does not match modulus degree")
        row = packet.get("row")
        row_field = row.get("field") if isinstance(row, dict) else None
        parsed_row_field = (
            parse_prime_power_field(row_field) if isinstance(row_field, str) else None
        )
        if parsed_row_field is not None and parsed_row_field != (field.p, field.degree):
            raise PacketError("row.field does not match extractor.field_model")
        return field

    def normalize(self, value: Any) -> tuple[int, ...]:
        if isinstance(value, int):
            coeffs = [value % self.p]
        elif isinstance(value, list):
            coeffs = [
                entry % self.p
                for entry in require_int_list(value, "field element")
            ]
        elif isinstance(value, tuple):
            if any(not isinstance(entry, int) for entry in value):
                raise PacketError("field element tuple entries must be integers")
            coeffs = [entry % self.p for entry in value]
        else:
            raise PacketError(f"unsupported field element {value!r}")
        if len(coeffs) > self.degree:
            raise PacketError("field element has too many coefficients")
        coeffs += [0] * (self.degree - len(coeffs))
        return tuple(coeffs)

    def encode(self, value: Any) -> int:
        elem = self.normalize(value)
        total = 0
        place = 1
        for coeff in elem:
            total += coeff * place
            place *= self.p
        return total

    def decode(self, value: int) -> tuple[int, ...]:
        if not isinstance(value, int) or value < 0 or value >= self.size:
            raise PacketError(
                f"encoded field element {value!r} outside 0..{self.size - 1}"
            )
        coeffs = []
        remaining = value
        for _ in range(self.degree):
            coeffs.append(remaining % self.p)
            remaining //= self.p
        return tuple(coeffs)

    def add(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple((left[i] + right[i]) % self.p for i in range(self.degree))

    def sub(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple((left[i] - right[i]) % self.p for i in range(self.degree))

    def neg(self, value: tuple[int, ...]) -> tuple[int, ...]:
        return self.sub(self.zero, value)

    def mul(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        coeffs = [0] * (2 * self.degree - 1)
        for i, left_coeff in enumerate(left):
            for j, right_coeff in enumerate(right):
                coeffs[i + j] = (
                    coeffs[i + j] + left_coeff * right_coeff
                ) % self.p
        for deg in range(len(coeffs) - 1, self.degree - 1, -1):
            lead = coeffs[deg] % self.p
            if lead == 0:
                continue
            offset = deg - self.degree
            for j in range(self.degree):
                coeffs[offset + j] = (
                    coeffs[offset + j] - lead * self.modulus[j]
                ) % self.p
        return tuple(coeffs[: self.degree])

    def pow(self, value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
        if exponent < 0:
            return self.pow(self.inv(value), -exponent)
        out = self.one
        base = value
        while exponent:
            if exponent & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            exponent >>= 1
        return out

    def inv(self, value: tuple[int, ...]) -> tuple[int, ...]:
        if value == self.zero:
            raise ZeroDivisionError("division by zero")
        return self.pow(value, self.size - 2)

    def div(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return self.mul(left, self.inv(right))

    def is_zero(self, value: tuple[int, ...]) -> bool:
        return value == self.zero

    def poly_eval_encoded(self, coefficients: list[int], value: int) -> tuple[int, ...]:
        root = self.decode(value)
        total = self.zero
        power = self.one
        for coefficient in coefficients:
            total = self.add(total, self.mul(self.decode(coefficient), power))
            power = self.mul(power, root)
        return total


def repeated_root_power_exact_roots_extension(
    coefficients: list[int],
    roots: list[int],
    field: PolynomialBasisField,
) -> list[int] | None:
    if len(roots) != 1:
        return None
    degree = poly_degree(coefficients)
    if degree <= 0:
        return [] if coefficients and field.decode(coefficients[0]) != field.zero else None
    root = field.decode(roots[0])
    leading = field.decode(coefficients[degree])
    factor = [field.sub(field.zero, root), field.one]
    expected = [field.one]
    for _ in range(degree):
        next_expected = [field.zero] * (len(expected) + 1)
        for i, left_coeff in enumerate(expected):
            for j, right_coeff in enumerate(factor):
                next_expected[i + j] = field.add(
                    next_expected[i + j], field.mul(left_coeff, right_coeff)
                )
        expected = next_expected
    expected = [field.mul(leading, coefficient) for coefficient in expected]
    decoded = [field.decode(coefficient) for coefficient in coefficients]
    while len(expected) < len(decoded):
        expected.append(field.zero)
    if expected[: len(decoded)] == decoded:
        return [roots[0]]
    return None


def extension_poly_mul(
    left: list[tuple[int, ...]],
    right: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    out = [field.zero] * (len(left) + len(right) - 1)
    for i, left_coeff in enumerate(left):
        for j, right_coeff in enumerate(right):
            out[i + j] = field.add(out[i + j], field.mul(left_coeff, right_coeff))
    while len(out) > 1 and out[-1] == field.zero:
        out.pop()
    return out


def extension_poly_trim(
    poly: list[tuple[int, ...]], field: PolynomialBasisField
) -> list[tuple[int, ...]]:
    out = poly[:]
    while len(out) > 1 and out[-1] == field.zero:
        out.pop()
    if not out:
        return [field.zero]
    return out


def extension_poly_is_zero(
    poly: list[tuple[int, ...]], field: PolynomialBasisField
) -> bool:
    trimmed = extension_poly_trim(poly, field)
    return len(trimmed) == 1 and trimmed[0] == field.zero


def extension_poly_degree(
    poly: list[tuple[int, ...]], field: PolynomialBasisField
) -> int:
    return len(extension_poly_trim(poly, field)) - 1


def extension_poly_divmod(
    numerator: list[tuple[int, ...]],
    denominator: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]]]:
    work = extension_poly_trim(numerator, field)
    divisor = extension_poly_trim(denominator, field)
    if extension_poly_is_zero(divisor, field):
        raise ZeroDivisionError("polynomial division by zero")
    quotient = [field.zero] * max(1, len(work) - len(divisor) + 1)
    while len(work) >= len(divisor) and not extension_poly_is_zero(work, field):
        coeff = field.div(work[-1], divisor[-1])
        shift = len(work) - len(divisor)
        quotient[shift] = coeff
        subtractor = [field.zero] * shift + [
            field.mul(coeff, term) for term in divisor
        ]
        size = max(len(work), len(subtractor))
        work = extension_poly_trim(
            [
                field.sub(
                    work[index] if index < len(work) else field.zero,
                    subtractor[index] if index < len(subtractor) else field.zero,
                )
                for index in range(size)
            ],
            field,
        )
    return extension_poly_trim(quotient, field), work


def extension_poly_mod(
    numerator: list[tuple[int, ...]],
    denominator: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    _quotient, remainder = extension_poly_divmod(numerator, denominator, field)
    return remainder


def extension_poly_monic(
    poly: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    out = extension_poly_trim(poly, field)
    if extension_poly_is_zero(out, field):
        return out
    inv_lead = field.inv(out[-1])
    return extension_poly_trim([field.mul(coeff, inv_lead) for coeff in out], field)


def extension_poly_gcd(
    left: list[tuple[int, ...]],
    right: list[tuple[int, ...]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    a = extension_poly_trim(left, field)
    b = extension_poly_trim(right, field)
    if extension_poly_is_zero(a, field):
        return extension_poly_monic(b, field)
    if extension_poly_is_zero(b, field):
        return extension_poly_monic(a, field)
    while not extension_poly_is_zero(b, field):
        a, b = b, extension_poly_mod(a, b, field)
    return extension_poly_monic(a, field)


def extension_poly_gcd_many(
    polynomials: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> list[tuple[int, ...]]:
    if not polynomials:
        raise PacketError("need a nonzero extension minor polynomial for common gcd")
    out = extension_poly_trim(polynomials[0], field)
    for polynomial in polynomials[1:]:
        out = extension_poly_gcd(out, polynomial, field)
    return extension_poly_monic(out, field)


def extension_poly_eval(
    coefficients: list[tuple[int, ...]],
    value: tuple[int, ...],
    field: PolynomialBasisField,
) -> tuple[int, ...]:
    total = field.zero
    power = field.one
    for coefficient in coefficients:
        total = field.add(total, field.mul(coefficient, power))
        power = field.mul(power, value)
    return total


def validate_split_linear_root_certificate_mod(
    certificate: Any,
    coefficients: list[int],
    roots: list[int],
    modulus: int,
    location: str,
) -> list[int] | None:
    if certificate is None:
        return None
    if not isinstance(certificate, dict):
        raise PacketError(f"{location}.root_certificate must be an object")
    if certificate.get("kind") != "split_linear_factorization":
        raise PacketError(f"{location}.root_certificate.kind is unsupported")
    leading = certificate.get("leading_coefficient")
    if not isinstance(leading, int):
        raise PacketError(f"{location}.root_certificate.leading_coefficient must be int")
    factors = certificate.get("factors")
    if not isinstance(factors, list):
        raise PacketError(f"{location}.root_certificate.factors must be a list")
    reconstructed = [leading % modulus]
    factor_roots = []
    total_multiplicity = 0
    for index, factor in enumerate(factors):
        if not isinstance(factor, dict):
            raise PacketError(f"{location}.root_certificate.factors[{index}] must be an object")
        root = factor.get("root")
        multiplicity = factor.get("multiplicity")
        if not isinstance(root, int):
            raise PacketError(f"{location}.root_certificate.factors[{index}].root must be int")
        if not isinstance(multiplicity, int) or multiplicity <= 0:
            raise PacketError(
                f"{location}.root_certificate.factors[{index}].multiplicity must be positive"
            )
        root %= modulus
        factor_roots.append(root)
        total_multiplicity += multiplicity
        for _ in range(multiplicity):
            reconstructed = poly_mul_mod_coefficients(
                reconstructed, [(-root) % modulus, 1], modulus
            )
    if total_multiplicity != poly_degree(coefficients):
        raise PacketError(
            f"{location}.root_certificate multiplicities do not match polynomial degree"
        )
    if trim_mod_coefficients(reconstructed, modulus) != trim_mod_coefficients(
        coefficients, modulus
    ):
        raise PacketError(f"{location}.root_certificate does not reconstruct polynomial")
    exact_roots = sorted(set(factor_roots))
    require_exact_roots(roots, exact_roots, location)
    return exact_roots


def validate_split_linear_root_certificate_extension(
    certificate: Any,
    coefficients: list[int],
    roots: list[int],
    field: PolynomialBasisField,
    location: str,
) -> list[int] | None:
    if certificate is None:
        return None
    if not isinstance(certificate, dict):
        raise PacketError(f"{location}.root_certificate must be an object")
    if certificate.get("kind") != "split_linear_factorization":
        raise PacketError(f"{location}.root_certificate.kind is unsupported")
    leading = certificate.get("leading_coefficient")
    if not isinstance(leading, int):
        raise PacketError(f"{location}.root_certificate.leading_coefficient must be int")
    factors = certificate.get("factors")
    if not isinstance(factors, list):
        raise PacketError(f"{location}.root_certificate.factors must be a list")
    reconstructed = [field.decode(leading)]
    factor_roots = []
    total_multiplicity = 0
    for index, factor in enumerate(factors):
        if not isinstance(factor, dict):
            raise PacketError(f"{location}.root_certificate.factors[{index}] must be an object")
        root_value = factor.get("root")
        multiplicity = factor.get("multiplicity")
        if not isinstance(root_value, int):
            raise PacketError(f"{location}.root_certificate.factors[{index}].root must be int")
        if not isinstance(multiplicity, int) or multiplicity <= 0:
            raise PacketError(
                f"{location}.root_certificate.factors[{index}].multiplicity must be positive"
            )
        root = field.decode(root_value)
        factor_roots.append(root_value)
        total_multiplicity += multiplicity
        linear = [field.sub(field.zero, root), field.one]
        for _ in range(multiplicity):
            reconstructed = extension_poly_mul(reconstructed, linear, field)
    if total_multiplicity != poly_degree(coefficients):
        raise PacketError(
            f"{location}.root_certificate multiplicities do not match polynomial degree"
        )
    decoded = [field.decode(coefficient) for coefficient in coefficients]
    while len(decoded) > 1 and decoded[-1] == field.zero:
        decoded.pop()
    if reconstructed != decoded:
        raise PacketError(f"{location}.root_certificate does not reconstruct polynomial")
    exact_roots = sorted(set(factor_roots))
    require_exact_roots(roots, exact_roots, location)
    return exact_roots


def first_matching_key(data: dict[str, Any], *patterns: str) -> str | None:
    for pattern in patterns:
        regex = re.compile(pattern)
        for key in data:
            if regex.fullmatch(key):
                return key
    return None


def modulus_named_in_key(key: str) -> int | None:
    match = re.search(r"_mod_(\d+)(?:_|$)", key)
    return int(match.group(1)) if match else None


def require_key_modulus(key: str, expected: int, location: str) -> None:
    named = modulus_named_in_key(key)
    if named is not None and named != expected:
        raise PacketError(f"{location}.{key} uses modulus {named}, expected {expected}")


REFERENCE_SENTINELS = {"not_enumerated", "not_applicable", "none", "unknown"}


def decode_json_pointer_token(token: str) -> str:
    return token.replace("~1", "/").replace("~0", "~")


def resolve_json_pointer(document: Any, pointer: str, location: str) -> Any:
    if pointer == "":
        return document
    if not pointer.startswith("/"):
        raise PacketError(f"{location}: JSON pointer fragment must start with /")
    current = document
    for raw_token in pointer[1:].split("/"):
        token = decode_json_pointer_token(raw_token)
        if isinstance(current, dict):
            if token not in current:
                raise PacketError(f"{location}: missing JSON pointer token {token!r}")
            current = current[token]
        elif isinstance(current, list):
            if not token.isdigit():
                raise PacketError(f"{location}: array token {token!r} is not numeric")
            index = int(token)
            if index >= len(current):
                raise PacketError(f"{location}: array index {index} out of range")
            current = current[index]
        else:
            raise PacketError(f"{location}: JSON pointer enters scalar value")
    return current


def validate_packet_reference(reference: str, location: str) -> Any | None:
    if not reference:
        raise PacketError(f"{location}: empty reference")
    if reference.startswith("inline:") or reference in REFERENCE_SENTINELS:
        return None

    path_text, separator, fragment = reference.partition("#")
    if not path_text:
        raise PacketError(f"{location}: reference must include a path")
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        raise PacketError(f"{location}: reference must be a repo-relative path")
    if not path.exists():
        raise PacketError(f"{location}: referenced file does not exist: {path}")

    if not separator:
        return load_json(path) if path.suffix == ".json" else None
    if path.suffix != ".json":
        raise PacketError(f"{location}: only JSON references may use fragments")
    document = load_json(path)
    return resolve_json_pointer(document, fragment, location)


def repo_relative_file(path_text: str, location: str) -> Path:
    path = Path(path_text)
    if path.is_absolute() or ".." in path.parts:
        raise PacketError(f"{location}: reference must be a repo-relative path")
    if not path.exists():
        raise PacketError(f"{location}: referenced file does not exist: {path}")
    return path


def table_numerator(target: Any, location: str) -> int | None:
    roots = table_roots(target, location)
    if roots is not None:
        return len(roots)
    if not isinstance(target, dict):
        return None

    declared = target.get("declared_aperiodic_numerator")
    if declared is not None:
        if not isinstance(declared, int) or declared < 0:
            raise PacketError(f"{location}.declared_aperiodic_numerator is invalid")
        return declared

    return None


def table_roots(target: Any, location: str) -> list[int] | None:
    if isinstance(target, list):
        return normalize_int_list(target, location)
    if not isinstance(target, dict):
        return None

    root_key = first_matching_key(target, r"root_union_mod_\d+", r"root_union", r"roots")
    if root_key is None:
        return None
    return normalize_int_list(target[root_key], f"{location}.{root_key}")


def validate_external_root_union_table(packet: dict[str, Any], target: Any) -> None:
    if "declared_aperiodic_numerator" not in packet:
        return
    declared = packet["declared_aperiodic_numerator"]
    if not isinstance(declared, int):
        return
    numerator = table_numerator(target, "root_union_table_ref")
    if numerator is None:
        return
    if declared != numerator:
        raise PacketError(
            "declared_aperiodic_numerator="
            f"{declared} but external root-union table has numerator {numerator}"
        )


def validate_references(packet: dict[str, Any]) -> None:
    for index, ledger in enumerate(packet.get("removed_ledgers", [])):
        reference = ledger.get("certificate_ref")
        if isinstance(reference, str):
            validate_packet_reference(
                reference, f"removed_ledgers[{index}].certificate_ref"
            )

    root_union_table_ref = packet.get("root_union_table_ref")
    if isinstance(root_union_table_ref, str):
        target = validate_packet_reference(root_union_table_ref, "root_union_table_ref")
        if target is not None:
            validate_external_root_union_table(packet, target)


def validate_schema(packet: Any, schema_path: Path) -> None:
    schema = load_json(schema_path)
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - depends on environment
        validate_schema_fallback(packet, schema)
        return

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(packet), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "<root>"
        raise PacketError(f"schema error at {location}: {first.message}")


def validate_schema_fallback(packet: Any, schema: dict[str, Any]) -> None:
    """Small stdlib fallback for the certificate contract.

    Full Draft 2020-12 validation is used when ``jsonschema`` is installed.
    This fallback checks the structural fields this script consumes, so packet
    arithmetic can still be replayed in a minimal Python environment.
    """

    if not isinstance(packet, dict):
        raise PacketError("packet must be a JSON object")

    for field in schema.get("required", []):
        if field not in packet:
            raise PacketError(f"missing required field {field}")

    if packet.get("schema_version") != "aperiodic-hankel-eliminant-v1":
        raise PacketError("bad schema_version")

    row = packet.get("row")
    if not isinstance(row, dict):
        raise PacketError("row must be an object")
    for field in ("n", "k", "field", "domain_hash"):
        if field not in row:
            raise PacketError(f"row: missing required field {field}")
    if not isinstance(row["n"], int) or row["n"] < 1:
        raise PacketError("row.n must be a positive integer")
    if not isinstance(row["k"], int) or row["k"] < 1:
        raise PacketError("row.k must be a positive integer")
    if not isinstance(row["field"], str) or not isinstance(row["domain_hash"], str):
        raise PacketError("row.field and row.domain_hash must be strings")

    if not isinstance(packet.get("agreement_threshold"), int):
        raise PacketError("agreement_threshold must be an integer")
    if packet.get("agreement_threshold") < 0:
        raise PacketError("agreement_threshold must be nonnegative")

    sampler = packet.get("sampler")
    if sampler is not None and sampler not in {
        "finite_affine_line",
        "projective_line",
        "finite_power_curve",
    }:
        raise PacketError("bad sampler")

    removed = packet.get("removed_ledgers")
    if not isinstance(removed, list):
        raise PacketError("removed_ledgers must be an array")
    for index, ledger in enumerate(removed):
        if not isinstance(ledger, dict):
            raise PacketError(f"removed_ledgers[{index}] must be an object")
        for field in ("name", "numerator", "certificate_ref"):
            if field not in ledger:
                raise PacketError(f"removed_ledgers[{index}]: missing {field}")
        if not isinstance(ledger["name"], str):
            raise PacketError(f"removed_ledgers[{index}].name must be a string")
        if not isinstance(ledger["certificate_ref"], str):
            raise PacketError(
                f"removed_ledgers[{index}].certificate_ref must be a string"
            )
        if not isinstance(ledger["numerator"], int) or ledger["numerator"] < 0:
            raise PacketError(
                f"removed_ledgers[{index}].numerator must be nonnegative integer"
            )

    agreements = packet.get("exact_agreements")
    if not isinstance(agreements, list):
        raise PacketError("exact_agreements must be an array")
    valid_status = {"regular_minor", "pivot_atlas", "empty", "residual_obstruction"}
    valid_residual = {
        "quotient",
        "tangent",
        "extension",
        "candidate_new_obstruction",
        "unknown",
    }
    valid_pivot_status = {
        "eliminant",
        "empty",
        "dimension_degree",
        "residual_obstruction",
    }
    for index, item in enumerate(agreements):
        if not isinstance(item, dict):
            raise PacketError(f"exact_agreements[{index}] must be an object")
        for field in ("A", "j", "t", "status"):
            if field not in item:
                raise PacketError(f"exact_agreements[{index}]: missing {field}")
        for field in ("A", "j", "t"):
            if not isinstance(item[field], int):
                raise PacketError(f"exact_agreements[{index}].{field} must be int")
        if item["status"] not in valid_status:
            raise PacketError(f"exact_agreements[{index}]: bad status")
        if item["status"] == "residual_obstruction":
            if item.get("residual_label") not in valid_residual:
                raise PacketError(
                    f"exact_agreements[{index}]: bad or missing residual_label"
                )
        if "regular_minor" in item and not isinstance(item["regular_minor"], dict):
            raise PacketError(f"exact_agreements[{index}].regular_minor must be object")
        for chart_index, chart in enumerate(item.get("charts", [])):
            if not isinstance(chart, dict):
                raise PacketError(
                    f"exact_agreements[{index}].charts[{chart_index}] must be object"
                )
            for field in ("chart_id", "equations_ref", "inequations_ref", "pivot_records"):
                if field not in chart:
                    raise PacketError(
                        f"exact_agreements[{index}].charts[{chart_index}]: missing {field}"
                    )
            if not isinstance(chart["pivot_records"], list):
                raise PacketError(
                    f"exact_agreements[{index}].charts[{chart_index}].pivot_records must be array"
                )
            for pivot_index, pivot in enumerate(chart["pivot_records"]):
                if not isinstance(pivot, dict):
                    raise PacketError(
                        "exact_agreements[{index}].charts[{chart_index}]"
                        f".pivot_records[{pivot_index}] must be object"
                    )
                if "pivot" not in pivot or "status" not in pivot:
                    raise PacketError(
                        "exact_agreements[{index}].charts[{chart_index}]"
                        f".pivot_records[{pivot_index}]: missing pivot/status"
                    )
                if pivot["status"] not in valid_pivot_status:
                    raise PacketError(
                        "exact_agreements[{index}].charts[{chart_index}]"
                        f".pivot_records[{pivot_index}]: bad status"
                    )
                if pivot["status"] == "residual_obstruction":
                    if pivot.get("residual_label") not in valid_residual:
                        raise PacketError(
                            "exact_agreements[{index}].charts[{chart_index}]"
                            f".pivot_records[{pivot_index}]: bad residual_label"
                        )


def validate_residual_labels(packet: dict[str, Any]) -> None:
    for item in packet.get("exact_agreements", []):
        if item.get("status") == "residual_obstruction" and "residual_label" not in item:
            raise PacketError(f"A={item.get('A')}: missing residual_label")
        for chart in item.get("charts", []):
            for pivot in chart.get("pivot_records", []):
                if (
                    pivot.get("status") == "residual_obstruction"
                    and "residual_label" not in pivot
                ):
                    raise PacketError(
                        "A={A} chart={chart} pivot={pivot}: missing residual_label".format(
                            A=item.get("A"),
                            chart=chart.get("chart_id"),
                            pivot=pivot.get("pivot"),
                        )
                    )


def require_nonnegative_int(value: Any, location: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise PacketError(f"{location} must be a nonnegative integer")
    return value


def require_nonempty_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise PacketError(f"{location} must be a nonempty string")
    return value


def require_enum(value: Any, allowed: set[str], location: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise PacketError(f"{location} must be one of {sorted(allowed)}")
    return value


CLAIM_SCOPE_ROW_DATA = {
    "toy_row",
    "synthetic_syndrome_pencil",
    "generic_symbolic",
    "settled_row_bookkeeping",
    "actual_row_certificate",
}
CLAIM_SCOPE_THRESHOLD_ROLES = {
    "none",
    "format_smoke",
    "toy_mechanism",
    "synthetic_stress",
    "generic_identity",
    "actual_row_audit",
    "actual_safe_side_bound",
    "actual_unsafe_lower_bound",
    "threshold_pin",
}
CLAIM_SCOPE_ROOT_STATUS = {
    "enumerated",
    "closed_form",
    "degree_bound_only",
    "removed_by_ledgers",
    "not_enumerated",
    "not_applicable",
}
PINNING_ROLES = {
    "actual_safe_side_bound",
    "actual_unsafe_lower_bound",
    "threshold_pin",
}
PINNING_NONCLAIM_PHRASES = {
    "synthetic",
    "toy row",
    "toy packet",
    "not a prize-row threshold theorem",
    "not a worst-case",
    "not actual",
}


def validate_claim_scope(packet: dict[str, Any]) -> None:
    scope = packet.get("claim_scope")
    if scope is None:
        return
    if not isinstance(scope, dict):
        raise PacketError("claim_scope must be an object")

    row_data = require_enum(
        scope.get("row_data"), CLAIM_SCOPE_ROW_DATA, "claim_scope.row_data"
    )
    threshold_role = require_enum(
        scope.get("threshold_role"),
        CLAIM_SCOPE_THRESHOLD_ROLES,
        "claim_scope.threshold_role",
    )
    root_status = require_enum(
        scope.get("root_status"),
        CLAIM_SCOPE_ROOT_STATUS,
        "claim_scope.root_status",
    )
    may_pin = scope.get("may_be_used_for_threshold_pinning")
    if not isinstance(may_pin, bool):
        raise PacketError("claim_scope.may_be_used_for_threshold_pinning must be bool")

    if not may_pin and threshold_role in PINNING_ROLES:
        raise PacketError(
            "claim_scope threshold-pinning role requires "
            "may_be_used_for_threshold_pinning=true"
        )
    if not may_pin:
        return

    if row_data != "actual_row_certificate":
        raise PacketError(
            "claim_scope: threshold-pinning packets must be actual_row_certificate"
        )
    if threshold_role not in PINNING_ROLES:
        raise PacketError(
            "claim_scope: threshold-pinning packets need an actual threshold role"
        )
    if root_status in {"degree_bound_only", "not_enumerated", "not_applicable"}:
        raise PacketError(
            "claim_scope: threshold-pinning packets need enumerated, closed-form, "
            "or removed-by-ledgers roots"
        )
    if packet.get("root_union_table_ref") == "not_enumerated":
        raise PacketError(
            "claim_scope: threshold-pinning packets cannot leave root_union_table_ref "
            "not_enumerated"
        )

    nonclaims = packet.get("nonclaims", [])
    if isinstance(nonclaims, list):
        nonclaim_text = " ".join(str(item).lower() for item in nonclaims)
        for phrase in PINNING_NONCLAIM_PHRASES:
            if phrase in nonclaim_text:
                raise PacketError(
                    "claim_scope: threshold-pinning packet conflicts with nonclaims"
                )


def validate_pivot_atlas(packet: dict[str, Any]) -> list[int]:
    row = packet.get("row", {})
    row_field = row.get("field") if isinstance(row, dict) else None
    modulus = parse_prime_field(row_field) if isinstance(row_field, str) else None
    extension_field = PolynomialBasisField.from_packet(packet)
    pivot_roots: set[int] = set()

    for item in packet.get("exact_agreements", []):
        if item.get("status") == "pivot_atlas":
            charts = item.get("charts")
            if not isinstance(charts, list) or not charts:
                raise PacketError(f"A={item.get('A')}: pivot_atlas needs charts")
        else:
            charts = item.get("charts", [])
        for chart_index, chart in enumerate(charts):
            location = f"A={item.get('A')} charts[{chart_index}]"
            if not isinstance(chart, dict):
                raise PacketError(f"{location} must be an object")
            for ref_field in ("equations_ref", "inequations_ref", "coverage_ref"):
                reference = chart.get(ref_field)
                if isinstance(reference, str):
                    validate_packet_reference(reference, f"{location}.{ref_field}")
            pivots = chart.get("pivot_records")
            if not isinstance(pivots, list) or not pivots:
                raise PacketError(f"{location}.pivot_records must be a nonempty array")
            for pivot_index, pivot in enumerate(pivots):
                pivot_location = f"{location}.pivot_records[{pivot_index}]"
                if not isinstance(pivot, dict):
                    raise PacketError(f"{pivot_location} must be an object")
                status = pivot.get("status")
                if status == "eliminant":
                    degree = require_nonnegative_int(
                        pivot.get("degree"), f"{pivot_location}.degree"
                    )
                    reference = require_nonempty_string(
                        pivot.get("eliminant_ref"),
                        f"{pivot_location}.eliminant_ref",
                    )
                    target = validate_packet_reference(
                        reference, f"{pivot_location}.eliminant_ref"
                    )
                    if isinstance(target, dict):
                        target_status = target.get("status")
                        if target_status is not None and target_status != "eliminant":
                            raise PacketError(
                                f"{pivot_location}.eliminant_ref points to "
                                f"status {target_status!r}"
                            )
                        target_degree = target.get("degree")
                        if target_degree is not None and target_degree != degree:
                            raise PacketError(
                                f"{pivot_location}.degree={degree} but "
                                f"eliminant target degree is {target_degree}"
                            )
                        roots = validate_pivot_eliminant_target(
                            target,
                            degree,
                            f"{pivot_location}.eliminant_ref",
                            modulus,
                            extension_field,
                        )
                        if roots is not None:
                            pivot_roots.update(roots)
                elif status == "dimension_degree":
                    require_nonnegative_int(
                        pivot.get("dimension"), f"{pivot_location}.dimension"
                    )
                    require_nonnegative_int(
                        pivot.get("variety_degree"),
                        f"{pivot_location}.variety_degree",
                    )
    return sorted(pivot_roots)


def validate_regular_minor_projective_infinity(
    item: dict[str, Any],
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
) -> int:
    audit = item.get("projective_infinity")
    if not isinstance(audit, dict):
        raise PacketError(
            f"A={item.get('A')}: projective_line regular_minor needs "
            "projective_infinity"
        )
    if audit.get("projective_point") != "[0:1]":
        raise PacketError(
            f"A={item.get('A')}: projective_infinity.projective_point must be [0:1]"
        )
    status = audit.get("status")
    if status not in {"empty", "nonempty"}:
        raise PacketError(
            f"A={item.get('A')}: projective_infinity status needs empty/nonempty"
        )
    top_degree = require_nonnegative_int(
        audit.get("top_degree"),
        f"A={item.get('A')}: projective_infinity.top_degree",
    )
    expected_top_degree = item["j"] + 1
    if top_degree != expected_top_degree:
        raise PacketError(
            f"A={item.get('A')}: projective_infinity top_degree {top_degree} "
            f"but expected j+1={expected_top_degree}"
        )
    top_coefficient = audit.get("top_coefficient")
    if not isinstance(top_coefficient, int) or top_coefficient < 0:
        raise PacketError(
            f"A={item.get('A')}: projective_infinity.top_coefficient must be "
            "a nonnegative integer"
        )
    if modulus is not None and top_coefficient >= modulus:
        raise PacketError(
            f"A={item.get('A')}: projective_infinity.top_coefficient outside F_{modulus}"
        )
    if extension_field is not None:
        extension_field.decode(top_coefficient)

    if "regular_minor_gcd" in item:
        gcd_info = item["regular_minor_gcd"]
        row_sets_raw = gcd_info.get("row_sets") if isinstance(gcd_info, dict) else None
        if not isinstance(row_sets_raw, list) or not row_sets_raw:
            raise PacketError(
                f"A={item.get('A')}: projective gcd infinity needs row_sets"
            )
        row_sets = [
            normalize_int_list(
                row_set,
                f"A={item.get('A')}: projective gcd row_sets[{index}]",
            )
            for index, row_set in enumerate(row_sets_raw)
        ]
        top_records = audit.get("top_coefficients")
        if not isinstance(top_records, list) or len(top_records) != len(row_sets):
            raise PacketError(
                f"A={item.get('A')}: projective gcd infinity needs one "
                "top_coefficients record per row set"
            )
        data = item.get("regular_minor_gcd_data")
        if not isinstance(data, dict):
            raise PacketError(
                f"A={item.get('A')}: projective gcd infinity needs gcd data"
            )
        minor_polynomial_key = first_matching_key(
            data,
            r"minor_polynomials_mod_\d+_ascending",
            r"minor_polynomials_ascending",
        )
        if minor_polynomial_key is None:
            raise PacketError(
                f"A={item.get('A')}: projective gcd infinity needs minor polynomials"
            )
        minor_records = data[minor_polynomial_key]
        if not isinstance(minor_records, list) or len(minor_records) != len(row_sets):
            raise PacketError(
                f"A={item.get('A')}: projective gcd minor records mismatch row sets"
            )
        actual_top_by_row_set = {}
        for index, (expected_row_set, record) in enumerate(zip(row_sets, minor_records)):
            if not isinstance(record, dict):
                raise PacketError(
                    f"A={item.get('A')}: projective gcd minor record {index} must be object"
                )
            row_set = normalize_int_list(
                record.get("row_set", []),
                f"A={item.get('A')}: projective gcd minor record {index} row_set",
            )
            if row_set != expected_row_set:
                raise PacketError(
                    f"A={item.get('A')}: projective gcd minor row_set {index} mismatch"
                )
            coefficients = require_int_list(
                record.get("coefficients", []),
                f"A={item.get('A')}: projective gcd minor {index} coefficients",
            )
            actual_top = coefficients[top_degree] if top_degree < len(coefficients) else 0
            if modulus is not None:
                actual_top %= modulus
            elif extension_field is not None:
                actual_top = extension_field.encode(extension_field.decode(actual_top))
            actual_top_by_row_set[tuple(row_set)] = actual_top
        listed_top_values = []
        for index, (expected_row_set, record) in enumerate(zip(row_sets, top_records)):
            if not isinstance(record, dict):
                raise PacketError(
                    f"A={item.get('A')}: projective gcd top record {index} must be object"
                )
            row_set = normalize_int_list(
                record.get("row_set", []),
                f"A={item.get('A')}: projective gcd top record {index} row_set",
            )
            if row_set != expected_row_set:
                raise PacketError(
                    f"A={item.get('A')}: projective gcd top row_set {index} mismatch"
                )
            listed_top = record.get("top_coefficient")
            if not isinstance(listed_top, int) or listed_top < 0:
                raise PacketError(
                    f"A={item.get('A')}: projective gcd top record {index} "
                    "needs nonnegative top_coefficient"
                )
            if modulus is not None:
                listed_top %= modulus
            elif extension_field is not None:
                listed_top = extension_field.encode(extension_field.decode(listed_top))
            actual_top = actual_top_by_row_set[tuple(row_set)]
            if listed_top != actual_top:
                raise PacketError(
                    f"A={item.get('A')}: projective gcd top record {index} "
                    f"has value {listed_top} but polynomial coefficient is {actual_top}"
                )
            listed_top_values.append(listed_top)
        nonzero_tops = [value for value in listed_top_values if value != 0]
        expected_status = "empty" if nonzero_tops else "nonempty"
        expected_top = nonzero_tops[0] if nonzero_tops else 0
        if status != expected_status:
            raise PacketError(
                f"A={item.get('A')}: projective gcd infinity status {status} "
                f"but top coefficients imply {expected_status}"
            )
        if top_coefficient != expected_top:
            raise PacketError(
                f"A={item.get('A')}: projective gcd top_coefficient "
                f"{top_coefficient} != witness {expected_top}"
            )
    else:
        data = item.get("regular_minor_polynomial_data")
        if not isinstance(data, dict):
            raise PacketError(
                f"A={item.get('A')}: projective regular minor needs polynomial data"
            )
        coefficient_key = first_matching_key(
            data, r"coefficients_mod_\d+_ascending", r"coefficients_ascending"
        )
        if coefficient_key is None:
            raise PacketError(
                f"A={item.get('A')}: projective regular minor needs coefficients"
            )
        coefficients = require_int_list(
            data[coefficient_key],
            f"A={item.get('A')}: projective_infinity polynomial coefficients",
        )
        actual_top = coefficients[top_degree] if top_degree < len(coefficients) else 0
        if modulus is not None:
            actual_top %= modulus
        elif extension_field is not None:
            actual_top = extension_field.encode(extension_field.decode(actual_top))
        if actual_top != top_coefficient:
            raise PacketError(
                f"A={item.get('A')}: projective_infinity top_coefficient "
                f"{top_coefficient} != polynomial coefficient {actual_top}"
            )

    is_zero_top = top_coefficient == 0
    if status == "empty" and is_zero_top:
        raise PacketError(
            f"A={item.get('A')}: empty projective_infinity needs nonzero top coefficient"
        )
    if status == "nonempty" and not is_zero_top:
        raise PacketError(
            f"A={item.get('A')}: nonempty projective_infinity needs zero top coefficient"
        )
    contribution = require_nonnegative_int(
        audit.get("contribution"),
        f"A={item.get('A')}: projective_infinity.contribution",
    )
    expected_contribution = 0 if status == "empty" else 1
    if contribution != expected_contribution:
        raise PacketError(
            f"A={item.get('A')}: projective_infinity contribution {contribution} "
            f"but expected {expected_contribution}"
        )
    return contribution


def validate_projective_infinity(
    packet: dict[str, Any],
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
) -> int:
    if packet.get("sampler") != "projective_line":
        return 0
    projective_infinity_present = False
    for item in packet.get("exact_agreements", []):
        if item.get("status") == "regular_minor":
            if validate_regular_minor_projective_infinity(
                item, modulus, extension_field
            ):
                projective_infinity_present = True
            continue
        if item.get("status") != "pivot_atlas":
            continue
        charts = item.get("charts")
        infinity_charts = [
            chart
            for chart in charts
            if (
                isinstance(chart, dict)
                and chart.get("chart_id") == "projective_infinity"
            )
        ]
        if len(infinity_charts) != 1:
            raise PacketError(
                f"A={item.get('A')}: projective_line pivot_atlas needs exactly "
                "one projective_infinity chart"
            )
        chart = infinity_charts[0]
        coverage_ref = chart.get("coverage_ref")
        if not isinstance(coverage_ref, str):
            raise PacketError(
                f"A={item.get('A')}: projective_infinity chart needs coverage_ref"
            )
        target = validate_packet_reference(
            coverage_ref, f"A={item.get('A')}: projective_infinity.coverage_ref"
        )
        if not isinstance(target, dict):
            raise PacketError(
                f"A={item.get('A')}: projective_infinity coverage_ref must "
                "point to object"
            )
        status = target.get("status")
        if status not in {"empty", "nonempty"}:
            raise PacketError(
                f"A={item.get('A')}: projective_infinity target needs status empty/nonempty"
            )
        pivots = chart.get("pivot_records")
        if not isinstance(pivots, list) or not pivots:
            raise PacketError(
                f"A={item.get('A')}: projective_infinity needs pivot_records"
            )
        if status == "empty" and any(
            pivot.get("status") != "empty" for pivot in pivots
        ):
            raise PacketError(
                f"A={item.get('A')}: empty projective_infinity target needs empty pivots"
            )
        contribution = target.get("support_count", target.get("contribution"))
        if contribution is None:
            raise PacketError(
                f"A={item.get('A')}: projective_infinity target needs "
                "support_count or contribution"
            )
        value = require_nonnegative_int(
            contribution,
            f"A={item.get('A')}: projective_infinity contribution",
        )
        if status == "empty" and value != 0:
            raise PacketError(
                f"A={item.get('A')}: empty projective_infinity target "
                f"has contribution {value}"
            )
        if status == "nonempty" and value == 0:
            raise PacketError(
                f"A={item.get('A')}: nonempty projective_infinity target "
                "needs positive contribution"
            )
        if value > 0:
            projective_infinity_present = True
    return int(projective_infinity_present)


RANK_WITNESS_POLYNOMIAL_REF = "rank_witness:determinant_nonzero_at_pivot_node"
PROPORTIONAL_RESIDUAL_CLASSIFICATIONS = {
    "proportional_window_tangent",
    "proportional_window_single_slope",
}
ENCODED_FIELD_INPUT_ENCODINGS = {
    "base-p low-to-high integer",
    "base-p low-to-high encoded integer",
    "encoded_integer",
}


def needs_inline_regular_minor_replay(item: dict[str, Any]) -> bool:
    minor = item.get("regular_minor")
    if not isinstance(minor, dict):
        return False
    polynomial_ref = minor.get("polynomial_ref")
    row_set = minor.get("row_set")
    return (
        isinstance(polynomial_ref, str)
        and polynomial_ref.startswith("inline:")
        and isinstance(row_set, list)
        and len(row_set) <= INLINE_MINOR_REPLAY_SIZE_LIMIT
        and isinstance(item.get("regular_minor_data"), dict)
    )


def packet_has_rank_replay_items(packet: dict[str, Any]) -> bool:
    for item in packet.get("exact_agreements", []):
        if not isinstance(item, dict):
            continue
        minor = item.get("regular_minor")
        if (
            isinstance(minor, dict)
            and minor.get("polynomial_ref") == RANK_WITNESS_POLYNOMIAL_REF
        ):
            return True
        if needs_inline_regular_minor_replay(item):
            return True
        if item.get("regular_minor_gcd") is not None:
            return True
        audit = item.get("extractor_audit")
        source = audit.get("row_set_source") if isinstance(audit, dict) else None
        if (
            item.get("status") == "residual_obstruction"
            and isinstance(source, str)
            and source.startswith("rank_at_nodes")
        ):
            return True
        if (
            isinstance(audit, dict)
            and audit.get("residual_classification")
            in PROPORTIONAL_RESIDUAL_CLASSIFICATIONS
        ):
            return True
    return False


def load_rank_replay_input(packet: dict[str, Any]) -> dict[str, Any] | None:
    if not packet_has_rank_replay_items(packet):
        return None
    extractor = packet.get("extractor")
    if not isinstance(extractor, dict):
        raise PacketError("rank replay packet needs extractor metadata")
    input_ref = extractor.get("input_ref")
    if not isinstance(input_ref, str) or not input_ref:
        raise PacketError("rank replay packet needs extractor.input_ref")
    if input_ref.startswith("inline:") or input_ref in REFERENCE_SENTINELS:
        raise PacketError("rank replay extractor.input_ref must be a JSON file")
    path_text, separator, _fragment = input_ref.partition("#")
    if separator:
        raise PacketError("rank replay extractor.input_ref must point to a full file")
    path = repo_relative_file(path_text, "extractor.input_ref")
    if path.suffix != ".json":
        raise PacketError("rank replay extractor.input_ref must be JSON")

    input_sha = extractor.get("input_sha256")
    if not isinstance(input_sha, str) or not input_sha:
        raise PacketError("rank replay packet needs extractor.input_sha256")
    actual_sha = hash_file(path)
    if input_sha != actual_sha:
        raise PacketError(
            f"extractor.input_sha256 mismatch: packet has {input_sha}, "
            f"file has {actual_sha}"
        )

    data = load_json(path)
    if not isinstance(data, dict):
        raise PacketError("rank replay extractor input must be a JSON object")
    if data.get("schema_version") != "regular-hankel-minor-extractor-input-v1":
        raise PacketError("rank replay input has wrong schema_version")

    input_row = data.get("row")
    packet_row = packet.get("row")
    if not isinstance(input_row, dict) or not isinstance(packet_row, dict):
        raise PacketError("rank replay input and packet need row objects")
    for field_name in ("n", "k", "field"):
        if input_row.get(field_name) != packet_row.get(field_name):
            raise PacketError(
                f"rank replay input row.{field_name} does not match packet row"
            )
    if data.get("sampler") != packet.get("sampler"):
        raise PacketError("rank replay input sampler does not match packet sampler")
    return data


def matrix_at_rank_replay_node_mod(
    u: list[int],
    v: list[int],
    row_set: list[int],
    cols: int,
    node: int,
    prime: int,
) -> list[list[int]]:
    return [
        [(u[row + col] + node * v[row + col]) % prime for col in range(cols)]
        for row in row_set
    ]


def matrix_is_full_rank_mod(matrix: list[list[int]], prime: int) -> bool:
    if not matrix:
        return False
    columns = len(matrix[0])
    if columns == 0 or any(len(row) != columns for row in matrix):
        return False
    work = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    for col in range(columns):
        pivot = None
        for row in range(pivot_row, len(work)):
            if work[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            return False
        if pivot != pivot_row:
            work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inv_pivot = pow(work[pivot_row][col] % prime, -1, prime)
        for row in range(pivot_row + 1, len(work)):
            factor = (work[row][col] * inv_pivot) % prime
            if factor == 0:
                continue
            for entry_col in range(col, columns):
                work[row][entry_col] = (
                    work[row][entry_col] - factor * work[pivot_row][entry_col]
                ) % prime
        pivot_row += 1
    return True


def normalize_field_input_value(
    value: Any,
    field: PolynomialBasisField,
    encoding: str | None,
    location: str,
) -> tuple[int, ...]:
    if encoding in ENCODED_FIELD_INPUT_ENCODINGS:
        if not isinstance(value, int):
            raise PacketError(f"{location}: encoded field input must be an integer")
        return field.decode(value)
    return field.normalize(value)


def normalize_field_input_list(
    values: Any,
    field: PolynomialBasisField,
    encoding: str | None,
    location: str,
) -> list[tuple[int, ...]]:
    if not isinstance(values, list):
        raise PacketError(f"{location}: expected a list")
    return [
        normalize_field_input_value(value, field, encoding, f"{location}[{index}]")
        for index, value in enumerate(values)
    ]


def matrix_at_rank_replay_node_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    row_set: list[int],
    cols: int,
    node: tuple[int, ...],
    field: PolynomialBasisField,
) -> list[list[tuple[int, ...]]]:
    return [
        [
            field.add(u[row + col], field.mul(node, v[row + col]))
            for col in range(cols)
        ]
        for row in row_set
    ]


def determinant_square_mod(matrix: list[list[int]], prime: int) -> int:
    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise PacketError("determinant replay needs a square matrix")
    work = [[entry % prime for entry in row] for row in matrix]
    determinant = 1
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if work[row][col] % prime:
                pivot = row
                break
        if pivot is None:
            return 0
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            determinant = (-determinant) % prime
        pivot_value = work[col][col] % prime
        determinant = (determinant * pivot_value) % prime
        inv_pivot = pow(pivot_value, -1, prime)
        for row in range(col + 1, size):
            factor = (work[row][col] * inv_pivot) % prime
            if factor == 0:
                continue
            for entry_col in range(col, size):
                work[row][entry_col] = (
                    work[row][entry_col] - factor * work[col][entry_col]
                ) % prime
    return determinant % prime


def matrix_is_full_rank_field(
    matrix: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> bool:
    if not matrix:
        return False
    columns = len(matrix[0])
    if columns == 0 or any(len(row) != columns for row in matrix):
        return False
    work = [[field.normalize(entry) for entry in row] for row in matrix]
    pivot_row = 0
    for col in range(columns):
        pivot = None
        for row in range(pivot_row, len(work)):
            if not field.is_zero(work[row][col]):
                pivot = row
                break
        if pivot is None:
            return False
        if pivot != pivot_row:
            work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inv_pivot = field.inv(work[pivot_row][col])
        for row in range(pivot_row + 1, len(work)):
            factor = field.mul(work[row][col], inv_pivot)
            if field.is_zero(factor):
                continue
            for entry_col in range(col, columns):
                work[row][entry_col] = field.sub(
                    work[row][entry_col],
                    field.mul(factor, work[pivot_row][entry_col]),
                )
        pivot_row += 1
    return True


def determinant_square_field(
    matrix: list[list[tuple[int, ...]]],
    field: PolynomialBasisField,
) -> tuple[int, ...]:
    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise PacketError("determinant replay needs a square matrix")
    work = [[field.normalize(entry) for entry in row] for row in matrix]
    determinant = field.one
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if not field.is_zero(work[row][col]):
                pivot = row
                break
        if pivot is None:
            return field.zero
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            determinant = field.neg(determinant)
        pivot_value = work[col][col]
        determinant = field.mul(determinant, pivot_value)
        inv_pivot = field.inv(pivot_value)
        for row in range(col + 1, size):
            factor = field.mul(work[row][col], inv_pivot)
            if field.is_zero(factor):
                continue
            for entry_col in range(col, size):
                work[row][entry_col] = field.sub(
                    work[row][entry_col],
                    field.mul(factor, work[col][entry_col]),
                )
    return determinant


def validate_rank_specializations(
    item: dict[str, Any],
    row_set: list[int],
    nodes: list[int],
    rank_replay_input: dict[str, Any] | None,
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
    location: str,
    *,
    expected_full_rank: bool,
) -> None:
    if rank_replay_input is None:
        raise PacketError(f"{location}: missing replay input")

    exact_agreements = rank_replay_input.get("exact_agreements")
    if not isinstance(exact_agreements, list) or item.get("A") not in exact_agreements:
        raise PacketError(f"{location}: replay input does not list this agreement")
    if min(row_set) < 0 or max(row_set) >= item["t"]:
        raise PacketError(f"{location}: row_set outside Hankel row range")

    syndrome = rank_replay_input.get("line_syndrome")
    if not isinstance(syndrome, dict):
        raise PacketError(f"{location}: replay input needs line_syndrome")
    if "u" not in syndrome or "v" not in syndrome:
        raise PacketError(f"{location}: line_syndrome needs u and v")
    needed_length = item["t"] + item["j"]
    cols = item["j"] + 1

    if modulus is not None:
        u = require_int_list(syndrome["u"], f"{location}: line_syndrome.u")
        v = require_int_list(syndrome["v"], f"{location}: line_syndrome.v")
        if len(u) < needed_length or len(v) < needed_length:
            raise PacketError(
                f"{location}: syndrome length must be at least {needed_length}"
            )
        for node in nodes:
            if node >= modulus:
                raise PacketError(f"{location}: rank node outside F_{modulus}")
            matrix = matrix_at_rank_replay_node_mod(
                u, v, row_set, cols, node, modulus
            )
            is_full_rank = matrix_is_full_rank_mod(matrix, modulus)
            if is_full_rank != expected_full_rank:
                expectation = "full rank" if expected_full_rank else "rank deficient"
                raise PacketError(
                    f"{location}: selected row_set is not {expectation} at node {node}"
                )
        return

    if extension_field is None:
        raise PacketError(f"{location}: unsupported row field")
    encoding = syndrome.get(
        "field_encoding", rank_replay_input.get("field_element_encoding")
    )
    if encoding is not None and not isinstance(encoding, str):
        raise PacketError(f"{location}: field encoding must be a string")
    u_field = normalize_field_input_list(
        syndrome["u"], extension_field, encoding, f"{location}: line_syndrome.u"
    )
    v_field = normalize_field_input_list(
        syndrome["v"], extension_field, encoding, f"{location}: line_syndrome.v"
    )
    if len(u_field) < needed_length or len(v_field) < needed_length:
        raise PacketError(
            f"{location}: syndrome length must be at least {needed_length}"
        )
    for node in nodes:
        if node >= extension_field.size:
            raise PacketError(f"{location}: rank node outside extension field")
        matrix = matrix_at_rank_replay_node_field(
            u_field,
            v_field,
            row_set,
            cols,
            extension_field.decode(node),
            extension_field,
        )
        is_full_rank = matrix_is_full_rank_field(matrix, extension_field)
        if is_full_rank != expected_full_rank:
            expectation = "full rank" if expected_full_rank else "rank deficient"
            raise PacketError(
                f"{location}: selected row_set is not {expectation} at node {node}"
            )


def validate_minor_polynomial_replay(
    item: dict[str, Any],
    row_set: list[int],
    polynomial: list[int],
    rank_replay_input: dict[str, Any] | None,
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
    location: str,
) -> None:
    if rank_replay_input is None:
        raise PacketError(f"{location}: missing replay input")

    exact_agreements = rank_replay_input.get("exact_agreements")
    if not isinstance(exact_agreements, list) or item.get("A") not in exact_agreements:
        raise PacketError(f"{location}: replay input does not list this agreement")

    syndrome = rank_replay_input.get("line_syndrome")
    if not isinstance(syndrome, dict):
        raise PacketError(f"{location}: replay input needs line_syndrome")
    if "u" not in syndrome or "v" not in syndrome:
        raise PacketError(f"{location}: line_syndrome needs u and v")

    needed_length = item["t"] + item["j"]
    cols = item["j"] + 1
    node_count = cols + 1

    if modulus is not None:
        if modulus < node_count:
            raise PacketError(
                f"{location}: not enough prime-field nodes to replay degree {cols}"
            )
        u = require_int_list(syndrome["u"], f"{location}: line_syndrome.u")
        v = require_int_list(syndrome["v"], f"{location}: line_syndrome.v")
        if len(u) < needed_length or len(v) < needed_length:
            raise PacketError(
                f"{location}: syndrome length must be at least {needed_length}"
            )
        for node in range(node_count):
            determinant = determinant_square_mod(
                matrix_at_rank_replay_node_mod(
                    u, v, row_set, cols, node, modulus
                ),
                modulus,
            )
            value = poly_eval_mod(polynomial, node, modulus)
            if value != determinant:
                raise PacketError(
                    f"{location}: minor polynomial does not replay at node {node}"
                )
        return

    if extension_field is None:
        raise PacketError(f"{location}: unsupported row field")
    if extension_field.size < node_count:
        raise PacketError(
            f"{location}: not enough extension-field nodes to replay degree {cols}"
        )
    encoding = syndrome.get(
        "field_encoding", rank_replay_input.get("field_element_encoding")
    )
    if encoding is not None and not isinstance(encoding, str):
        raise PacketError(f"{location}: field encoding must be a string")
    u_field = normalize_field_input_list(
        syndrome["u"], extension_field, encoding, f"{location}: line_syndrome.u"
    )
    v_field = normalize_field_input_list(
        syndrome["v"], extension_field, encoding, f"{location}: line_syndrome.v"
    )
    if len(u_field) < needed_length or len(v_field) < needed_length:
        raise PacketError(
            f"{location}: syndrome length must be at least {needed_length}"
        )
    decoded_polynomial = [
        extension_field.decode(coefficient) for coefficient in polynomial
    ]
    for node in range(node_count):
        node_value = extension_field.decode(node)
        determinant = determinant_square_field(
            matrix_at_rank_replay_node_field(
                u_field, v_field, row_set, cols, node_value, extension_field
            ),
            extension_field,
        )
        value = extension_poly_eval(
            decoded_polynomial, node_value, extension_field
        )
        if value != determinant:
            raise PacketError(
                f"{location}: extension minor polynomial does not replay at node {node}"
            )


def visible_proportional_scalar_mod(
    u: list[int],
    v: list[int],
    visible_length: int,
    prime: int,
) -> int | None:
    scalar: int | None = None
    for index in range(visible_length):
        u_i = u[index] % prime
        v_i = v[index] % prime
        if v_i == 0:
            if u_i != 0:
                return None
            continue
        candidate = (u_i * pow(v_i, -1, prime)) % prime
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return None
    return scalar


def visible_proportional_scalar_field(
    u: list[tuple[int, ...]],
    v: list[tuple[int, ...]],
    visible_length: int,
    field: PolynomialBasisField,
) -> tuple[int, ...] | None:
    scalar: tuple[int, ...] | None = None
    for index in range(visible_length):
        u_i = u[index]
        v_i = v[index]
        if v_i == field.zero:
            if u_i != field.zero:
                return None
            continue
        candidate = field.mul(u_i, field.inv(v_i))
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return None
    return scalar


def validate_proportional_residual_audit(
    item: dict[str, Any],
    audit: dict[str, Any],
    rank_replay_input: dict[str, Any] | None,
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
    location: str,
) -> None:
    if rank_replay_input is None:
        raise PacketError(f"{location}: proportional residual needs replay input")
    exact_agreements = rank_replay_input.get("exact_agreements")
    if not isinstance(exact_agreements, list) or item.get("A") not in exact_agreements:
        raise PacketError(f"{location}: replay input does not list this agreement")
    syndrome = rank_replay_input.get("line_syndrome")
    if not isinstance(syndrome, dict):
        raise PacketError(f"{location}: replay input needs line_syndrome")
    if "u" not in syndrome or "v" not in syndrome:
        raise PacketError(f"{location}: line_syndrome needs u and v")
    visible_length = item["t"] + item["j"]

    if modulus is not None:
        scalar = audit["scalar_multiple_u_over_v"]
        tangent = audit["residual_single_slope"]
        if scalar < 0 or scalar >= modulus:
            raise PacketError(f"{location}.scalar_multiple_u_over_v outside F_{modulus}")
        if tangent < 0 or tangent >= modulus:
            raise PacketError(f"{location}.residual_single_slope outside F_{modulus}")
        u = require_int_list(syndrome["u"], f"{location}: line_syndrome.u")
        v = require_int_list(syndrome["v"], f"{location}: line_syndrome.v")
        if len(u) < visible_length or len(v) < visible_length:
            raise PacketError(
                f"{location}: syndrome length must be at least {visible_length}"
            )
        actual_scalar = visible_proportional_scalar_mod(
            u, v, visible_length, modulus
        )
        if actual_scalar is None:
            raise PacketError(f"{location}: visible window is not proportional")
        if actual_scalar != scalar:
            raise PacketError(
                f"{location}.scalar_multiple_u_over_v={scalar} "
                f"but replay gives {actual_scalar}"
            )
        actual_tangent = (-actual_scalar) % modulus
        full_proportional = len(u) == len(v) and all(
            (u_i - actual_scalar * v_i) % modulus == 0 for u_i, v_i in zip(u, v)
        )
    else:
        if extension_field is None:
            raise PacketError(f"{location}: unsupported row field")
        scalar = audit["scalar_multiple_u_over_v"]
        tangent = audit["residual_single_slope"]
        scalar_elem = extension_field.decode(scalar)
        extension_field.decode(tangent)
        encoding = syndrome.get(
            "field_encoding", rank_replay_input.get("field_element_encoding")
        )
        if encoding is not None and not isinstance(encoding, str):
            raise PacketError(f"{location}: field encoding must be a string")
        u_field = normalize_field_input_list(
            syndrome["u"], extension_field, encoding, f"{location}: line_syndrome.u"
        )
        v_field = normalize_field_input_list(
            syndrome["v"], extension_field, encoding, f"{location}: line_syndrome.v"
        )
        if len(u_field) < visible_length or len(v_field) < visible_length:
            raise PacketError(
                f"{location}: syndrome length must be at least {visible_length}"
            )
        actual_scalar_elem = visible_proportional_scalar_field(
            u_field, v_field, visible_length, extension_field
        )
        if actual_scalar_elem is None:
            raise PacketError(f"{location}: visible window is not proportional")
        actual_scalar = extension_field.encode(actual_scalar_elem)
        if actual_scalar_elem != scalar_elem:
            raise PacketError(
                f"{location}.scalar_multiple_u_over_v={scalar} "
                f"but replay gives {actual_scalar}"
            )
        actual_tangent = extension_field.encode(extension_field.neg(actual_scalar_elem))
        full_proportional = len(u_field) == len(v_field) and all(
            extension_field.sub(u_i, extension_field.mul(actual_scalar_elem, v_i))
            == extension_field.zero
            for u_i, v_i in zip(u_field, v_field)
        )

    if tangent != actual_tangent:
        raise PacketError(
            f"{location}.residual_single_slope={tangent} "
            f"but replay gives {actual_tangent}"
        )
    declared_tangent = syndrome.get("tangent_root")
    if declared_tangent is not None and int(declared_tangent) != actual_tangent:
        raise PacketError(f"{location}: input tangent_root does not match replay")
    if audit["full_syndrome_proportional"] != full_proportional:
        raise PacketError(
            f"{location}.full_syndrome_proportional="
            f"{audit['full_syndrome_proportional']} but replay gives "
            f"{full_proportional}"
        )
    expected_classification = (
        "proportional_window_tangent"
        if full_proportional
        else "proportional_window_single_slope"
    )
    expected_charge = (
        "tangent_common_code_line" if full_proportional else "tail_check_required"
    )
    if audit["residual_classification"] != expected_classification:
        raise PacketError(
            f"{location}.residual_classification={audit['residual_classification']} "
            f"but replay gives {expected_classification}"
        )
    if audit["residual_charge"] != expected_charge:
        raise PacketError(
            f"{location}.residual_charge={audit['residual_charge']} "
            f"but replay gives {expected_charge}"
        )


def validate_pivot_eliminant_target(
    target: dict[str, Any],
    declared_degree: int,
    location: str,
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
) -> list[int] | None:
    coefficient_key = first_matching_key(
        target,
        r"eliminant_coefficients_mod_\d+_ascending",
        r"coefficients_mod_\d+_ascending",
        r"coefficients_ascending",
    )
    root_key = first_matching_key(target, r"roots_mod_\d+", r"roots")
    if coefficient_key is None and root_key is None:
        return None
    if coefficient_key is None or root_key is None:
        raise PacketError(
            f"{location}: eliminant target needs both coefficients and roots"
        )

    coefficients = require_int_list(
        target[coefficient_key], f"{location}.{coefficient_key}"
    )
    roots = normalize_int_list(target[root_key], f"{location}.{root_key}")
    if not coefficients:
        raise PacketError(f"{location}.{coefficient_key}: empty coefficient list")

    if modulus is not None:
        require_key_modulus(coefficient_key, modulus, location)
        require_key_modulus(root_key, modulus, location)
        coefficients = [coefficient % modulus for coefficient in coefficients]
    if all(coefficient == 0 for coefficient in coefficients):
        raise PacketError(f"{location}: zero pivot eliminant polynomial")

    actual_degree = poly_degree(coefficients)
    if actual_degree != declared_degree:
        raise PacketError(
            f"{location}: pivot degree {declared_degree} != actual {actual_degree}"
        )
    target_degree = target.get("degree")
    if target_degree is not None and actual_degree != target_degree:
        raise PacketError(
            f"{location}: target degree {target_degree} != actual {actual_degree}"
        )

    if modulus is not None:
        if modulus <= ROOT_COMPLETENESS_ENUMERATION_LIMIT:
            actual_roots = [
                root
                for root in range(modulus)
                if poly_eval_mod(coefficients, root, modulus) == 0
            ]
            require_exact_roots(roots, actual_roots, location)
        else:
            non_roots = [
                root for root in roots if poly_eval_mod(coefficients, root, modulus)
            ]
            if non_roots:
                raise PacketError(f"{location}: listed non-roots {non_roots}")
            exact_monomial_roots = monomial_exact_roots(coefficients, modulus)
            if exact_monomial_roots is not None:
                require_exact_roots(roots, exact_monomial_roots, location)
            exact_repeated_roots = repeated_root_power_exact_roots_mod(
                coefficients, roots, modulus
            )
            if exact_repeated_roots is not None:
                require_exact_roots(roots, exact_repeated_roots, location)

    if extension_field is not None:
        for coefficient in coefficients:
            extension_field.decode(coefficient)
        if extension_field.size <= ROOT_COMPLETENESS_ENUMERATION_LIMIT:
            actual_roots = [
                root
                for root in range(extension_field.size)
                if extension_field.is_zero(
                    extension_field.poly_eval_encoded(coefficients, root)
                )
            ]
            require_exact_roots(roots, actual_roots, location)
        else:
            non_roots = [
                root
                for root in roots
                if not extension_field.is_zero(
                    extension_field.poly_eval_encoded(coefficients, root)
                )
            ]
            if non_roots:
                raise PacketError(
                    f"{location}: listed extension non-roots {non_roots}"
                )
            exact_monomial_roots = monomial_exact_roots(coefficients)
            if exact_monomial_roots is not None:
                require_exact_roots(roots, exact_monomial_roots, location)
            exact_repeated_roots = repeated_root_power_exact_roots_extension(
                coefficients, roots, extension_field
            )
            if exact_repeated_roots is not None:
                require_exact_roots(roots, exact_repeated_roots, location)

    return roots


def validate_regular_minor(
    item: dict[str, Any],
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
    rank_replay_input: dict[str, Any] | None,
) -> tuple[list[int] | None, list[int]]:
    minor = item.get("regular_minor")
    if not isinstance(minor, dict):
        raise PacketError(f"A={item.get('A')}: regular_minor status needs data")

    for field in ("row_set", "polynomial_ref", "degree", "root_hash"):
        if field not in minor:
            raise PacketError(f"A={item.get('A')}: missing regular_minor.{field}")

    row_set = normalize_int_list(minor["row_set"], f"A={item.get('A')} row_set")
    expected_size = item["j"] + 1
    if len(row_set) != expected_size:
        raise PacketError(
            f"A={item.get('A')}: row_set has {len(row_set)} rows, expected {expected_size}"
        )
    if min(row_set) < 0 or max(row_set) >= item["t"]:
        raise PacketError(f"A={item.get('A')}: row_set outside Hankel row range")

    if not isinstance(minor["degree"], int) or minor["degree"] < 0:
        raise PacketError(f"A={item.get('A')}: bad regular_minor.degree")
    if minor["degree"] > item["j"] + 1:
        raise PacketError(
            f"A={item.get('A')}: degree {minor['degree']} exceeds j+1={item['j'] + 1}"
        )

    data = item.get("regular_minor_data")
    if str(minor["polynomial_ref"]).startswith("rank_witness:"):
        validate_rank_witness_minor(
            item,
            row_set,
            rank_replay_input,
            modulus,
            extension_field,
        )
        if "regular_minor_data" in item or "regular_minor_polynomial_data" in item:
            raise PacketError(
                f"A={item.get('A')}: rank_witness minor must not carry inline data"
            )
        return None, []
    if data is None:
        return None, []
    if not isinstance(data, dict):
        raise PacketError(f"A={item.get('A')}: regular_minor_data must be an object")

    coefficient_key = first_matching_key(
        data, r"coefficients_mod_\d+_ascending", r"coefficients_ascending"
    )
    root_key = first_matching_key(data, r"roots_mod_\d+", r"roots")
    bad_slope_key = first_matching_key(
        data, r"enumerated_bad_slopes_mod_\d+", r"enumerated_bad_slopes"
    )
    if coefficient_key is None or root_key is None:
        raise PacketError(
            f"A={item.get('A')}: inline regular_minor_data needs coefficients and roots"
        )
    coefficients = require_int_list(
        data[coefficient_key], f"A={item.get('A')} coefficients"
    )
    roots = normalize_int_list(data[root_key], f"A={item.get('A')} roots")
    bad_slopes = normalize_int_list(
        data.get(bad_slope_key, []), f"A={item.get('A')} bad_slopes"
    )
    root_certificate = data.get("root_certificate")

    if not coefficients:
        raise PacketError(f"A={item.get('A')}: empty coefficient list")
    if all(coefficient == 0 for coefficient in coefficients):
        raise PacketError(f"A={item.get('A')}: zero regular-minor polynomial")
    actual_degree = poly_degree(coefficients)
    if actual_degree != minor["degree"]:
        raise PacketError(
            f"A={item.get('A')}: degree field {minor['degree']} != actual {actual_degree}"
        )
    if hash_json(roots) != minor["root_hash"]:
        raise PacketError(f"A={item.get('A')}: root_hash mismatch")
    if not set(bad_slopes).issubset(roots):
        raise PacketError(f"A={item.get('A')}: enumerated bad slopes are not roots")
    if expected_size <= INLINE_MINOR_REPLAY_SIZE_LIMIT:
        validate_minor_polynomial_replay(
            item,
            row_set,
            coefficients,
            rank_replay_input,
            modulus,
            extension_field,
            f"A={item.get('A')}: regular_minor",
        )
    if modulus is not None:
        validate_split_linear_root_certificate_mod(
            root_certificate,
            coefficients,
            roots,
            modulus,
            f"A={item.get('A')}",
        )
        exact_monomial_roots = monomial_exact_roots(coefficients, modulus)
        if modulus <= ROOT_COMPLETENESS_ENUMERATION_LIMIT:
            actual_roots = [
                root
                for root in range(modulus)
                if poly_eval_mod(coefficients, root, modulus) == 0
            ]
            require_exact_roots(roots, actual_roots, f"A={item.get('A')}")
        else:
            non_roots = [
                root for root in roots if poly_eval_mod(coefficients, root, modulus)
            ]
            if non_roots:
                raise PacketError(f"A={item.get('A')}: listed non-roots {non_roots}")
            if exact_monomial_roots is not None:
                require_exact_roots(
                    roots, exact_monomial_roots, f"A={item.get('A')}"
                )
            exact_repeated_roots = repeated_root_power_exact_roots_mod(
                coefficients, roots, modulus
            )
            if exact_repeated_roots is not None:
                require_exact_roots(
                    roots, exact_repeated_roots, f"A={item.get('A')}"
                )
    if extension_field is not None:
        for coefficient in coefficients:
            extension_field.decode(coefficient)
        validate_split_linear_root_certificate_extension(
            root_certificate,
            coefficients,
            roots,
            extension_field,
            f"A={item.get('A')}",
        )
        exact_monomial_roots = monomial_exact_roots(coefficients)
        if extension_field.size <= ROOT_COMPLETENESS_ENUMERATION_LIMIT:
            actual_roots = [
                root
                for root in range(extension_field.size)
                if extension_field.is_zero(
                    extension_field.poly_eval_encoded(coefficients, root)
                )
            ]
            require_exact_roots(roots, actual_roots, f"A={item.get('A')}")
        else:
            non_roots = [
                root
                for root in roots
                if not extension_field.is_zero(
                    extension_field.poly_eval_encoded(coefficients, root)
                )
            ]
            if non_roots:
                raise PacketError(
                    f"A={item.get('A')}: listed extension non-roots {non_roots}"
                )
            if exact_monomial_roots is not None:
                require_exact_roots(
                    roots, exact_monomial_roots, f"A={item.get('A')}"
                )
            exact_repeated_roots = repeated_root_power_exact_roots_extension(
                coefficients, roots, extension_field
            )
            if exact_repeated_roots is not None:
                require_exact_roots(
                    roots, exact_repeated_roots, f"A={item.get('A')}"
                )

    return roots, bad_slopes


def validate_regular_minor_gcd(
    item: dict[str, Any],
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
    rank_replay_input: dict[str, Any] | None,
) -> tuple[list[int] | None, list[int]]:
    if modulus is None and extension_field is None:
        raise PacketError(
            f"A={item.get('A')}: regular_minor_gcd needs a finite-field row"
        )
    gcd_info = item.get("regular_minor_gcd")
    if not isinstance(gcd_info, dict):
        raise PacketError(f"A={item.get('A')}: missing regular_minor_gcd")
    if "regular_minor" in item:
        raise PacketError(
            f"A={item.get('A')}: use either regular_minor or regular_minor_gcd, not both"
        )
    audit = item.get("extractor_audit")
    if not isinstance(audit, dict) or audit.get("certificate_mode") != "minor_gcd_roots":
        raise PacketError(
            f"A={item.get('A')}: regular_minor_gcd needs certificate_mode=minor_gcd_roots"
        )
    for field in ("row_sets", "polynomial_ref", "degree", "root_hash", "minor_count"):
        if field not in gcd_info:
            raise PacketError(f"A={item.get('A')}: missing regular_minor_gcd.{field}")
    row_sets_raw = gcd_info["row_sets"]
    if not isinstance(row_sets_raw, list) or not row_sets_raw:
        raise PacketError(f"A={item.get('A')}: regular_minor_gcd.row_sets must be nonempty")
    expected_size = item["j"] + 1
    row_sets = []
    for index, row_set_raw in enumerate(row_sets_raw):
        row_set = normalize_int_list(
            row_set_raw, f"A={item.get('A')} regular_minor_gcd.row_sets[{index}]"
        )
        if len(row_set) != expected_size:
            raise PacketError(
                f"A={item.get('A')}: gcd row set {index} has {len(row_set)} rows, "
                f"expected {expected_size}"
            )
        if len(set(row_set)) != len(row_set):
            raise PacketError(f"A={item.get('A')}: gcd row set {index} has duplicates")
        if min(row_set) < 0 or max(row_set) >= item["t"]:
            raise PacketError(
                f"A={item.get('A')}: gcd row set {index} outside Hankel row range"
            )
        row_sets.append(row_set)
    if gcd_info["minor_count"] != len(row_sets):
        raise PacketError(
            f"A={item.get('A')}: minor_count does not match row_sets length"
        )
    if not isinstance(gcd_info["degree"], int) or gcd_info["degree"] < 0:
        raise PacketError(f"A={item.get('A')}: bad regular_minor_gcd.degree")
    if gcd_info["degree"] > item["j"] + 1:
        raise PacketError(
            f"A={item.get('A')}: gcd degree {gcd_info['degree']} exceeds j+1={item['j'] + 1}"
        )

    data = item.get("regular_minor_gcd_data")
    if not isinstance(data, dict):
        raise PacketError(
            f"A={item.get('A')}: regular_minor_gcd_data must be an object"
        )
    coefficient_key = first_matching_key(
        data, r"gcd_coefficients_mod_\d+_ascending", r"gcd_coefficients_ascending"
    )
    root_key = first_matching_key(data, r"roots_mod_\d+", r"roots")
    minor_polynomial_key = first_matching_key(
        data, r"minor_polynomials_mod_\d+_ascending", r"minor_polynomials_ascending"
    )
    bad_slope_key = first_matching_key(
        data, r"enumerated_bad_slopes_mod_\d+", r"enumerated_bad_slopes"
    )
    if coefficient_key is None or minor_polynomial_key is None:
        raise PacketError(
            f"A={item.get('A')}: gcd data needs gcd coefficients and minor polynomials"
        )
    coefficients = require_int_list(
        data[coefficient_key], f"A={item.get('A')} gcd coefficients"
    )
    if not coefficients:
        raise PacketError(f"A={item.get('A')}: empty gcd coefficient list")
    roots = (
        normalize_int_list(data[root_key], f"A={item.get('A')} gcd roots")
        if root_key is not None
        else None
    )
    bad_slopes = normalize_int_list(
        data.get(bad_slope_key, []), f"A={item.get('A')} gcd bad_slopes"
    )
    root_certificate = data.get("root_certificate")
    if roots is None and bad_slopes:
        raise PacketError(
            f"A={item.get('A')}: enumerated bad slopes need an exact gcd root table"
        )

    if modulus is not None:
        require_key_modulus(coefficient_key, modulus, f"A={item.get('A')}: gcd")
        if root_key is not None:
            require_key_modulus(root_key, modulus, f"A={item.get('A')}: gcd")
        if bad_slope_key is not None:
            require_key_modulus(
                bad_slope_key, modulus, f"A={item.get('A')}: gcd"
            )
        if all(coefficient % modulus == 0 for coefficient in coefficients):
            raise PacketError(f"A={item.get('A')}: zero gcd polynomial")
        actual_degree = poly_degree([coefficient % modulus for coefficient in coefficients])
        decoded_coefficients = None
        exact_monomial_roots = monomial_exact_roots(coefficients, modulus)
        field_size = modulus
    else:
        assert extension_field is not None
        if data.get("p") not in (None, extension_field.p):
            raise PacketError(f"A={item.get('A')}: gcd data p does not match field")
        if data.get("field_extension_degree") not in (None, extension_field.degree):
            raise PacketError(
                f"A={item.get('A')}: gcd data extension degree does not match field"
            )
        decoded_coefficients = [
            extension_field.decode(coefficient) for coefficient in coefficients
        ]
        if extension_poly_is_zero(decoded_coefficients, extension_field):
            raise PacketError(f"A={item.get('A')}: zero gcd polynomial")
        actual_degree = extension_poly_degree(decoded_coefficients, extension_field)
        exact_monomial_roots = monomial_exact_roots(coefficients)
        if roots is not None:
            for root in roots:
                extension_field.decode(root)
        for slope in bad_slopes:
            extension_field.decode(slope)
        field_size = extension_field.size

    if actual_degree != gcd_info["degree"]:
        raise PacketError(
            f"A={item.get('A')}: gcd degree field {gcd_info['degree']} != actual {actual_degree}"
        )
    root_hash_payload: Any = (
        roots
        if roots is not None
        else {
            "roots": "not_enumerated",
            "degree_bound": actual_degree,
            "row_sets": row_sets,
        }
    )
    if hash_json(root_hash_payload) != gcd_info["root_hash"]:
        raise PacketError(f"A={item.get('A')}: gcd root_hash mismatch")
    if roots is not None and not set(bad_slopes).issubset(roots):
        raise PacketError(
            f"A={item.get('A')}: enumerated bad slopes are not gcd roots"
        )
    if root_certificate is not None and roots is None:
        raise PacketError(
            f"A={item.get('A')}: gcd root_certificate needs an exact root table"
        )
    if root_certificate is not None:
        if modulus is not None:
            validate_split_linear_root_certificate_mod(
                root_certificate,
                coefficients,
                roots or [],
                modulus,
                f"A={item.get('A')}: gcd",
            )
        else:
            assert extension_field is not None
            validate_split_linear_root_certificate_extension(
                root_certificate,
                coefficients,
                roots or [],
                extension_field,
                f"A={item.get('A')}: gcd",
            )

    minor_records = data[minor_polynomial_key]
    if not isinstance(minor_records, list) or len(minor_records) != len(row_sets):
        raise PacketError(
            f"A={item.get('A')}: minor polynomial records must match row_sets"
        )
    polynomial_by_row_set: dict[tuple[int, ...], list[int]] = {}
    nonzero_minor_polynomials_mod: list[list[int]] = []
    nonzero_minor_polynomials_extension: list[list[tuple[int, ...]]] = []
    for index, (expected_row_set, record) in enumerate(zip(row_sets, minor_records)):
        if not isinstance(record, dict):
            raise PacketError(
                f"A={item.get('A')}: minor polynomial record {index} must be an object"
            )
        row_set = normalize_int_list(
            record.get("row_set", []),
            f"A={item.get('A')} minor polynomial row_set {index}",
        )
        if row_set != expected_row_set:
            raise PacketError(
                f"A={item.get('A')}: minor polynomial row_set {index} mismatch"
            )
        polynomial = require_int_list(
            record.get("coefficients", []),
            f"A={item.get('A')} minor polynomial coefficients {index}",
        )
        if not polynomial:
            raise PacketError(
                f"A={item.get('A')}: minor polynomial {index} has empty coefficients"
            )
        validate_minor_polynomial_replay(
            item,
            expected_row_set,
            polynomial,
            rank_replay_input,
            modulus,
            extension_field,
            f"A={item.get('A')}: minor polynomial {index}",
        )
        polynomial_by_row_set[tuple(row_set)] = polynomial
        if modulus is not None:
            if any(coefficient % modulus != 0 for coefficient in polynomial):
                trimmed_polynomial = trim_mod_coefficients(polynomial, modulus)
                degree = poly_degree(trimmed_polynomial)
                if degree > item["j"] + 1:
                    raise PacketError(
                        f"A={item.get('A')}: minor polynomial {index} degree exceeds j+1"
                    )
                if record.get("degree") != degree:
                    raise PacketError(
                        f"A={item.get('A')}: minor polynomial {index} degree mismatch"
                    )
                if ppoly_mod(polynomial, coefficients, modulus) != [0]:
                    raise PacketError(
                        f"A={item.get('A')}: gcd does not divide minor polynomial {index}"
                    )
                nonzero_minor_polynomials_mod.append(trimmed_polynomial)
            elif record.get("degree") != -1:
                raise PacketError(
                    f"A={item.get('A')}: zero minor polynomial {index} must have degree -1"
                )
        else:
            assert extension_field is not None and decoded_coefficients is not None
            decoded_polynomial = [
                extension_field.decode(coefficient) for coefficient in polynomial
            ]
            if not extension_poly_is_zero(decoded_polynomial, extension_field):
                degree = extension_poly_degree(decoded_polynomial, extension_field)
                if degree > item["j"] + 1:
                    raise PacketError(
                        f"A={item.get('A')}: minor polynomial {index} degree exceeds j+1"
                    )
                if record.get("degree") != degree:
                    raise PacketError(
                        f"A={item.get('A')}: minor polynomial {index} degree mismatch"
                    )
                remainder = extension_poly_mod(
                    decoded_polynomial, decoded_coefficients, extension_field
                )
                if not extension_poly_is_zero(remainder, extension_field):
                    raise PacketError(
                        f"A={item.get('A')}: gcd does not divide minor polynomial {index}"
                    )
                nonzero_minor_polynomials_extension.append(
                    extension_poly_trim(decoded_polynomial, extension_field)
                )
            elif record.get("degree") != -1:
                raise PacketError(
                    f"A={item.get('A')}: zero minor polynomial {index} must have degree -1"
                )

    if modulus is not None:
        recomputed_gcd = ppoly_gcd_many(nonzero_minor_polynomials_mod, modulus)
        if ppoly_monic(coefficients, modulus) != recomputed_gcd:
            raise PacketError(
                f"A={item.get('A')}: gcd coefficients are not the common gcd"
            )
    else:
        assert extension_field is not None and decoded_coefficients is not None
        recomputed_gcd = extension_poly_gcd_many(
            nonzero_minor_polynomials_extension, extension_field
        )
        if extension_poly_monic(decoded_coefficients, extension_field) != recomputed_gcd:
            raise PacketError(
                f"A={item.get('A')}: extension gcd coefficients are not the common gcd"
            )

    audit = item.get("extractor_audit")
    source = audit.get("row_set_source") if isinstance(audit, dict) else None
    if isinstance(source, str) and source.startswith("rank_at_nodes_family"):
        witness_records = audit.get("rank_pivot_witness_records")
        if not isinstance(witness_records, list) or not witness_records:
            raise PacketError(
                f"A={item.get('A')}: rank-node gcd needs witness records"
            )
        for index, record in enumerate(witness_records):
            if not isinstance(record, dict):
                raise PacketError(
                    f"A={item.get('A')}: rank-node witness {index} must be an object"
                )
            witness_node = record.get("node")
            if not isinstance(witness_node, int):
                raise PacketError(
                    f"A={item.get('A')}: rank-node witness {index} needs integer node"
                )
            witness_row_set = tuple(
                normalize_int_list(
                    record.get("row_set", []),
                    f"A={item.get('A')} rank-node witness {index} row_set",
                )
            )
            polynomial = polynomial_by_row_set.get(witness_row_set)
            if polynomial is None:
                raise PacketError(
                    f"A={item.get('A')}: rank-node witness {index} row_set "
                    "has no matching minor polynomial"
                )
            if modulus is not None:
                if poly_eval_mod(polynomial, witness_node, modulus) == 0:
                    raise PacketError(
                        f"A={item.get('A')}: rank-node witness {index} "
                        "does not evaluate to a nonzero minor"
                    )
            else:
                assert extension_field is not None
                if extension_field.is_zero(
                    extension_field.poly_eval_encoded(polynomial, witness_node)
                ):
                    raise PacketError(
                        f"A={item.get('A')}: rank-node witness {index} "
                        "does not evaluate to a nonzero extension minor"
                    )

    if field_size <= ROOT_COMPLETENESS_ENUMERATION_LIMIT and roots is None:
        raise PacketError(
            f"A={item.get('A')}: small-field gcd packets need exact roots"
        )
    if modulus is not None and roots is not None:
        if modulus <= ROOT_COMPLETENESS_ENUMERATION_LIMIT:
            actual_roots = [
                root
                for root in range(modulus)
                if poly_eval_mod(coefficients, root, modulus) == 0
            ]
            require_exact_roots(roots, actual_roots, f"A={item.get('A')}: gcd")
        else:
            non_roots = [
                root for root in roots if poly_eval_mod(coefficients, root, modulus)
            ]
            if non_roots:
                raise PacketError(
                    f"A={item.get('A')}: listed gcd non-roots {non_roots}"
                )
            if exact_monomial_roots is not None:
                require_exact_roots(
                    roots, exact_monomial_roots, f"A={item.get('A')}: gcd"
                )
    else:
        assert extension_field is not None
        if roots is not None:
            if extension_field.size <= ROOT_COMPLETENESS_ENUMERATION_LIMIT:
                actual_roots = [
                    root
                    for root in range(extension_field.size)
                    if extension_field.is_zero(
                        extension_field.poly_eval_encoded(coefficients, root)
                    )
                ]
                require_exact_roots(roots, actual_roots, f"A={item.get('A')}: gcd")
            else:
                non_roots = [
                    root
                    for root in roots
                    if not extension_field.is_zero(
                        extension_field.poly_eval_encoded(coefficients, root)
                    )
                ]
                if non_roots:
                    raise PacketError(
                        f"A={item.get('A')}: listed extension gcd non-roots {non_roots}"
                    )
                if exact_monomial_roots is not None:
                    require_exact_roots(
                        roots, exact_monomial_roots, f"A={item.get('A')}: gcd"
                    )
    return roots, bad_slopes


def validate_rank_witness_minor(
    item: dict[str, Any],
    row_set: list[int],
    rank_replay_input: dict[str, Any] | None,
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
) -> None:
    minor = item["regular_minor"]
    location = f"A={item.get('A')}: rank_witness"
    if minor["polynomial_ref"] != "rank_witness:determinant_nonzero_at_pivot_node":
        raise PacketError(f"{location}: unsupported polynomial_ref")

    audit = item.get("extractor_audit")
    if not isinstance(audit, dict):
        raise PacketError(f"{location}: missing extractor_audit")
    if audit.get("certificate_mode") != "rank_witness_bound":
        raise PacketError(f"{location}: certificate_mode must be rank_witness_bound")

    expected_degree = item["j"] + 1
    if minor["degree"] != expected_degree:
        raise PacketError(
            f"{location}: degree {minor['degree']} but rank witness needs {expected_degree}"
        )
    if audit.get("degree_bound") != expected_degree:
        raise PacketError(
            f"{location}: degree_bound must equal j+1={expected_degree}"
        )
    if audit.get("root_count") != "not_enumerated":
        raise PacketError(f"{location}: root_count must be not_enumerated")

    node = audit.get("rank_pivot_node")
    if not isinstance(node, int) or node < 0:
        raise PacketError(f"{location}: rank_pivot_node must name the witness node")

    expected_hash = hash_json(
        {
            "roots": "not_enumerated",
            "degree_bound": expected_degree,
            "row_set": row_set,
            "rank_pivot_node": node,
        }
    )
    if minor["root_hash"] != expected_hash:
        raise PacketError(f"{location}: root_hash mismatch")
    if (
        not isinstance(rank_replay_input, dict)
        or rank_replay_input.get("certificate_mode") != "rank_witness_bound"
    ):
        raise PacketError(
            f"{location}: replay input must use certificate_mode=rank_witness_bound"
        )
    validate_rank_specializations(
        item,
        row_set,
        [node],
        rank_replay_input,
        modulus,
        extension_field,
        location,
        expected_full_rank=True,
    )


def validate_extractor_audit(
    item: dict[str, Any],
    roots: list[int] | None,
    rank_replay_input: dict[str, Any] | None,
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
) -> None:
    audit = item.get("extractor_audit")
    if audit is None:
        return
    if not isinstance(audit, dict):
        raise PacketError(f"A={item.get('A')}: extractor_audit must be an object")

    location = f"A={item.get('A')}: extractor_audit"
    source = audit.get("row_set_source")
    if source is not None and not isinstance(source, str):
        raise PacketError(f"{location}.row_set_source must be a string or null")

    tested_row_sets = audit.get("tested_row_sets")
    if tested_row_sets is not None:
        if not isinstance(tested_row_sets, int) or tested_row_sets < 0:
            raise PacketError(
                f"{location}.tested_row_sets must be a nonnegative integer"
            )

    if roots is not None and "root_count" in audit:
        root_count = audit["root_count"]
        if root_count != "not_enumerated":
            if not isinstance(root_count, int) or root_count != len(roots):
                raise PacketError(
                    f"{location}.root_count={root_count!r} "
                    f"but inline roots have size {len(roots)}"
                )

    if item.get("status") == "regular_minor" and "degree_bound" in audit:
        degree_bound = audit["degree_bound"]
        if "regular_minor" in item:
            degree = item["regular_minor"]["degree"]
        elif "regular_minor_gcd" in item:
            degree = item["regular_minor_gcd"]["degree"]
        else:
            raise PacketError(
                f"{location}.degree_bound needs regular_minor or regular_minor_gcd"
            )
        if (
            not isinstance(degree_bound, int)
            or degree_bound < degree
            or degree_bound > item["j"] + 1
        ):
            raise PacketError(
                f"{location}.degree_bound must lie between degree={degree} "
                f"and j+1={item['j'] + 1}"
            )

    residual_classification = audit.get("residual_classification")
    if residual_classification in PROPORTIONAL_RESIDUAL_CLASSIFICATIONS:
        if item.get("status") != "residual_obstruction":
            raise PacketError(
                f"{location}.residual_classification only applies to residuals"
            )
        if not isinstance(audit.get("scalar_multiple_u_over_v"), int):
            raise PacketError(f"{location}.scalar_multiple_u_over_v must be int")
        if not isinstance(audit.get("residual_single_slope"), int):
            raise PacketError(f"{location}.residual_single_slope must be int")
        if not isinstance(audit.get("full_syndrome_proportional"), bool):
            raise PacketError(f"{location}.full_syndrome_proportional must be bool")
        residual_charge = audit.get("residual_charge")
        validate_proportional_residual_audit(
            item,
            audit,
            rank_replay_input,
            modulus,
            extension_field,
            location,
        )
        if residual_classification == "proportional_window_tangent":
            if item.get("residual_label") != "tangent":
                raise PacketError(
                    f"{location}: proportional_window_tangent needs residual_label=tangent"
                )
            if residual_charge != "tangent_common_code_line":
                raise PacketError(
                    f"{location}: tangent classification needs tangent_common_code_line charge"
                )
            if audit.get("full_syndrome_proportional") is not True:
                raise PacketError(
                    f"{location}: tangent charge needs full_syndrome_proportional=true"
                )
        elif residual_charge != "tail_check_required":
            raise PacketError(
                f"{location}: local single-slope residual needs tail_check_required"
            )

    rank_source = None
    if isinstance(source, str):
        if source.startswith("rank_at_nodes_family"):
            rank_source = "rank_at_nodes_family"
        elif source.startswith("rank_at_nodes"):
            rank_source = "rank_at_nodes"
    if rank_source is None:
        return

    expected_required = item["j"] + 2
    required = audit.get("rank_pivot_nodes_required")
    if required != expected_required:
        raise PacketError(
            f"{location}.rank_pivot_nodes_required={required!r} "
            f"but rank_at_nodes needs j+2={expected_required}"
        )
    tested = audit.get("rank_pivot_nodes_tested")
    if not isinstance(tested, int):
        raise PacketError(f"{location}.rank_pivot_nodes_tested must be an integer")
    if rank_source == "rank_at_nodes_family":
        if tested < expected_required:
            raise PacketError(
                f"{location}.rank_pivot_nodes_tested={tested} "
                f"but a rank-node family needs at least j+2={expected_required} nodes"
            )
    elif tested < 1 or tested > expected_required:
        raise PacketError(
            f"{location}.rank_pivot_nodes_tested must be in "
            f"1..{expected_required}"
        )
    test_nodes = audit.get("rank_pivot_test_nodes")
    if not isinstance(test_nodes, list):
        raise PacketError(f"{location}.rank_pivot_test_nodes must list tested nodes")
    if len(test_nodes) != tested:
        raise PacketError(
            f"{location}.rank_pivot_test_nodes has length {len(test_nodes)} "
            f"but rank_pivot_nodes_tested={tested}"
        )
    if any(
        not isinstance(node_value, int) or node_value < 0
        for node_value in test_nodes
    ):
        raise PacketError(
            f"{location}.rank_pivot_test_nodes must contain nonnegative integers"
        )
    if len(set(test_nodes)) != len(test_nodes):
        raise PacketError(f"{location}.rank_pivot_test_nodes must be distinct")
    if test_nodes != list(range(tested)):
        raise PacketError(
            f"{location}.rank_pivot_test_nodes must be the deterministic "
            f"prefix nodes 0..{tested - 1}"
        )

    node = audit.get("rank_pivot_node")
    if item.get("status") == "regular_minor":
        if not isinstance(node, int) or node < 0:
            raise PacketError(
                f"{location}.rank_pivot_node must name the successful node"
            )
        if rank_source == "rank_at_nodes" and test_nodes[-1] != node:
            raise PacketError(
                f"{location}.rank_pivot_node must be the last tested node"
            )
        if tested_row_sets is not None and tested_row_sets < 1:
            raise PacketError(
                f"{location}.tested_row_sets must be positive for a regular minor"
            )
        if rank_source == "rank_at_nodes_family":
            witness_records = audit.get("rank_pivot_witness_records")
            if not isinstance(witness_records, list) or not witness_records:
                raise PacketError(
                    f"{location}.rank_pivot_witness_records must be a nonempty list"
                )
            if "regular_minor_gcd" not in item:
                raise PacketError(
                    f"{location}: rank-node family packets must use regular_minor_gcd"
                )
            row_sets_raw = item["regular_minor_gcd"].get("row_sets")
            if not isinstance(row_sets_raw, list):
                raise PacketError(f"{location}: missing regular_minor_gcd.row_sets")
            row_set_keys = {
                tuple(
                    normalize_int_list(
                        row_set,
                        f"A={item.get('A')} rank-node family gcd row_set",
                    )
                )
                for row_set in row_sets_raw
            }
            witness_keys = set()
            for index, record in enumerate(witness_records):
                if not isinstance(record, dict):
                    raise PacketError(
                        f"{location}.rank_pivot_witness_records[{index}] must be an object"
                    )
                witness_node = record.get("node")
                if not isinstance(witness_node, int) or witness_node not in test_nodes:
                    raise PacketError(
                        f"{location}.rank_pivot_witness_records[{index}].node "
                        "must be one of the tested nodes"
                    )
                witness_row_set = normalize_int_list(
                    record.get("row_set", []),
                    f"{location}.rank_pivot_witness_records[{index}].row_set",
                )
                key = tuple(witness_row_set)
                if key not in row_set_keys:
                    raise PacketError(
                        f"{location}.rank_pivot_witness_records[{index}].row_set "
                        "is not one of the gcd row sets"
                    )
                witness_keys.add(key)
            if witness_keys != row_set_keys:
                raise PacketError(
                    f"{location}.rank_pivot_witness_records must witness every "
                    "gcd row set exactly"
                )
        return

    if item.get("status") != "residual_obstruction":
        return
    if node is not None:
        raise PacketError(
            f"{location}.rank_pivot_node must be null for a singular declaration"
        )
    if rank_source == "rank_at_nodes" and tested != expected_required:
        raise PacketError(
            f"{location}.rank_pivot_nodes_tested={tested} "
            f"but a singular declaration needs all j+2={expected_required} nodes"
        )
    if (
        rank_source == "rank_at_nodes_family"
        and audit.get("rank_pivot_witness_records") not in ([], None)
    ):
        raise PacketError(
            f"{location}.rank_pivot_witness_records must be empty for a singular declaration"
        )
    reason = item.get("residual_reason")
    if not isinstance(reason, str) or "size+1 distinct slopes" not in reason:
        raise PacketError(
            f"{location}: singular rank_at_nodes packets must record the "
            "degree/root-vanishing residual_reason"
        )
    validate_rank_specializations(
        item,
        list(range(item["t"])),
        test_nodes,
        rank_replay_input,
        modulus,
        extension_field,
        location,
        expected_full_rank=False,
    )


def validate_packet(packet: dict[str, Any], schema_path: Path) -> None:
    validate_schema(packet, schema_path)
    validate_claim_scope(packet)
    validate_residual_labels(packet)
    validate_references(packet)
    pivot_roots = validate_pivot_atlas(packet)

    row = packet["row"]
    n = row["n"]
    k = row["k"]
    modulus = parse_prime_field(row["field"])
    extension_field = PolynomialBasisField.from_packet(packet)
    rank_replay_input = load_rank_replay_input(packet)
    projective_infinity_count = validate_projective_infinity(
        packet, modulus, extension_field
    )
    all_roots: set[int] = set()
    all_bad: set[int] = set()
    all_roots.update(pivot_roots)

    for item in packet["exact_agreements"]:
        agreement = item["A"]
        roots: list[int] | None = None
        if item["j"] != n - agreement:
            raise PacketError(f"A={agreement}: j={item['j']} but n-A={n - agreement}")
        if item["t"] != agreement - k:
            raise PacketError(f"A={agreement}: t={item['t']} but A-k={agreement - k}")
        if agreement < packet["agreement_threshold"]:
            raise PacketError(
                f"A={agreement}: below threshold {packet['agreement_threshold']}"
            )
        if item["status"] == "regular_minor":
            if "regular_minor_gcd" in item:
                roots, bad_slopes = validate_regular_minor_gcd(
                    item, modulus, extension_field, rank_replay_input
                )
            else:
                roots, bad_slopes = validate_regular_minor(
                    item, modulus, extension_field, rank_replay_input
                )
            if roots is not None:
                all_roots.update(roots)
            all_bad.update(bad_slopes)
        validate_extractor_audit(
            item,
            roots,
            rank_replay_input,
            modulus,
            extension_field,
        )

    root_union_key = first_matching_key(packet, r"root_union_mod_\d+", r"root_union")
    root_union: list[int] | None = None
    if root_union_key is not None:
        root_union = normalize_int_list(packet[root_union_key], root_union_key)
        if all_roots and root_union != sorted(all_roots):
            raise PacketError(
                f"{root_union_key} does not match the union of inline root tables"
            )
        if "declared_aperiodic_numerator" in packet:
            declared = packet["declared_aperiodic_numerator"]
            expected = len(root_union) + projective_infinity_count
            if declared != expected:
                raise PacketError(
                    "declared_aperiodic_numerator="
                    f"{declared} but finite root union plus projective infinity "
                    f"has size {expected}"
                )
    elif packet.get("root_union_table_ref", "").startswith("inline"):
        raise PacketError("inline root_union_table_ref requires an inline root_union")
    else:
        root_union_table_ref = packet.get("root_union_table_ref")
        if isinstance(root_union_table_ref, str):
            target = validate_packet_reference(root_union_table_ref, "root_union_table_ref")
            if target is not None:
                root_union = table_roots(target, "root_union_table_ref")
                if all_roots and root_union is not None and root_union != sorted(all_roots):
                    raise PacketError(
                        "root_union_table_ref does not match the union of inline "
                        "or pivot root tables"
                    )

    bad_union_key = first_matching_key(
        packet, r"enumerated_bad_slope_union_mod_\d+", r"enumerated_bad_slope_union"
    )
    if bad_union_key is not None:
        bad_union = normalize_int_list(
            packet[bad_union_key],
            bad_union_key,
        )
        if sorted(all_bad) and bad_union != sorted(all_bad):
            raise PacketError(
                f"{bad_union_key} does not match inline bad slopes"
            )
        if root_union_key is not None and not set(bad_union).issubset(
            packet[root_union_key]
        ):
            raise PacketError("bad-slope union is not contained in root union")


def check_path(path: Path, schema_path: Path) -> None:
    packet = load_json(path)
    if not isinstance(packet, dict):
        raise PacketError(f"{path}: packet must be a JSON object")
    validate_packet(packet, schema_path)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packets", nargs="+", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument(
        "--expect-fail",
        action="store_true",
        help="succeed only if each listed packet fails validation",
    )
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    failed = False
    for path in args.packets:
        try:
            check_path(path, args.schema)
        except PacketError as exc:
            if args.expect_fail:
                if not args.quiet:
                    print(f"EXPECTED-FAIL {path}: {exc}")
                continue
            failed = True
            print(f"FAIL {path}: {exc}")
            continue

        if args.expect_fail:
            failed = True
            print(f"UNEXPECTED-PASS {path}")
        elif not args.quiet:
            print(f"OK {path}: schema and arithmetic checks passed")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
