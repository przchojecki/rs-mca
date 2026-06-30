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
regular-bucket declarations, rank-witness degree-bound packets, and pivot-atlas
records.  Local packet references such as removed-ledger certificates are
resolved, including JSON pointer fragments.
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


def first_matching_key(data: dict[str, Any], *patterns: str) -> str | None:
    for pattern in patterns:
        regex = re.compile(pattern)
        for key in data:
            if regex.fullmatch(key):
                return key
    return None


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


def table_numerator(target: Any, location: str) -> int | None:
    if isinstance(target, list):
        return len(normalize_int_list(target, location))
    if not isinstance(target, dict):
        return None

    declared = target.get("declared_aperiodic_numerator")
    if declared is not None:
        if not isinstance(declared, int) or declared < 0:
            raise PacketError(f"{location}.declared_aperiodic_numerator is invalid")
        return declared

    root_key = first_matching_key(target, r"root_union_mod_\d+", r"root_union", r"roots")
    if root_key is None:
        return None
    return len(normalize_int_list(target[root_key], f"{location}.{root_key}"))


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


def validate_pivot_atlas(packet: dict[str, Any]) -> None:
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
                elif status == "dimension_degree":
                    require_nonnegative_int(
                        pivot.get("dimension"), f"{pivot_location}.dimension"
                    )
                    require_nonnegative_int(
                        pivot.get("variety_degree"),
                        f"{pivot_location}.variety_degree",
                    )


def validate_regular_minor(
    item: dict[str, Any],
    modulus: int | None,
    extension_field: PolynomialBasisField | None,
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

    if not isinstance(minor["degree"], int) or minor["degree"] < 0:
        raise PacketError(f"A={item.get('A')}: bad regular_minor.degree")
    if minor["degree"] > item["j"] + 1:
        raise PacketError(
            f"A={item.get('A')}: degree {minor['degree']} exceeds j+1={item['j'] + 1}"
        )

    data = item.get("regular_minor_data")
    if str(minor["polynomial_ref"]).startswith("rank_witness:"):
        validate_rank_witness_minor(item, row_set)
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
    if modulus is not None:
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
    if extension_field is not None:
        for coefficient in coefficients:
            extension_field.decode(coefficient)
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

    return roots, bad_slopes


def validate_rank_witness_minor(item: dict[str, Any], row_set: list[int]) -> None:
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


def validate_extractor_audit(
    item: dict[str, Any],
    roots: list[int] | None,
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
        degree = item["regular_minor"]["degree"]
        if (
            not isinstance(degree_bound, int)
            or degree_bound < degree
            or degree_bound > item["j"] + 1
        ):
            raise PacketError(
                f"{location}.degree_bound must lie between degree={degree} "
                f"and j+1={item['j'] + 1}"
            )

    if source != "rank_at_nodes":
        return

    expected_required = item["j"] + 2
    required = audit.get("rank_pivot_nodes_required")
    if required != expected_required:
        raise PacketError(
            f"{location}.rank_pivot_nodes_required={required!r} "
            f"but rank_at_nodes needs j+2={expected_required}"
        )
    tested = audit.get("rank_pivot_nodes_tested")
    if not isinstance(tested, int) or tested < 1 or tested > expected_required:
        raise PacketError(
            f"{location}.rank_pivot_nodes_tested must be in "
            f"1..{expected_required}"
        )

    node = audit.get("rank_pivot_node")
    if item.get("status") == "regular_minor":
        if not isinstance(node, int) or node < 0:
            raise PacketError(
                f"{location}.rank_pivot_node must name the successful node"
            )
        if tested_row_sets is not None and tested_row_sets < 1:
            raise PacketError(
                f"{location}.tested_row_sets must be positive for a regular minor"
            )
        return

    if item.get("status") != "residual_obstruction":
        return
    if node is not None:
        raise PacketError(
            f"{location}.rank_pivot_node must be null for a singular declaration"
        )
    if tested != expected_required:
        raise PacketError(
            f"{location}.rank_pivot_nodes_tested={tested} "
            f"but a singular declaration needs all j+2={expected_required} nodes"
        )
    reason = item.get("residual_reason")
    if not isinstance(reason, str) or "size+1 distinct slopes" not in reason:
        raise PacketError(
            f"{location}: singular rank_at_nodes packets must record the "
            "degree/root-vanishing residual_reason"
        )


def validate_packet(packet: dict[str, Any], schema_path: Path) -> None:
    validate_schema(packet, schema_path)
    validate_residual_labels(packet)
    validate_references(packet)
    validate_pivot_atlas(packet)

    row = packet["row"]
    n = row["n"]
    k = row["k"]
    modulus = parse_prime_field(row["field"])
    extension_field = PolynomialBasisField.from_packet(packet)
    all_roots: set[int] = set()
    all_bad: set[int] = set()

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
            roots, bad_slopes = validate_regular_minor(
                item, modulus, extension_field
            )
            if roots is not None:
                all_roots.update(roots)
            all_bad.update(bad_slopes)
        validate_extractor_audit(item, roots)

    root_union_key = first_matching_key(packet, r"root_union_mod_\d+", r"root_union")
    if root_union_key is not None:
        root_union = normalize_int_list(packet[root_union_key], root_union_key)
        if all_roots and root_union != sorted(all_roots):
            raise PacketError(
                f"{root_union_key} does not match the union of inline root tables"
            )
        if "declared_aperiodic_numerator" in packet:
            declared = packet["declared_aperiodic_numerator"]
            if declared != len(root_union):
                raise PacketError(
                    "declared_aperiodic_numerator="
                    f"{declared} but root union has size {len(root_union)}"
                )
    elif packet.get("root_union_table_ref", "").startswith("inline"):
        raise PacketError("inline root_union_table_ref requires an inline root_union")

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
