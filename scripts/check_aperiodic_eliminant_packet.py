#!/usr/bin/env python3
"""Check Paper D v12 aperiodic Hankel eliminant packets.

The JSON schema catches the structural contract.  This script adds the
arithmetical checks that are easiest to get wrong in generated packets:
``j=n-A``, ``t=A-k``, residual labels, regular-minor or regular-minor-gcd
degree/root hashes, and declared root-union numerators when the packet includes
inline root tables.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import re
from typing import Any


DEFAULT_SCHEMA = Path("scripts/aperiodic_eliminant_schema.json")

STRATIFICATION_ORDER = ("T0", "T1", "T2", "T3", "T4", "T5", "T6")
STRATIFICATION_LABELS = {
    "T0": "excluded",
    "T1": "paid:degenerate",
    "T2": "paid:tangent",
    "T3": "paid:quotient",
    "T4": "paid:extension",
    "T5": "dedup:higher_agreement",
}
STRATIFICATION_CLOSED_LABELS = {"eliminant", "empty", "dimension_degree"}
STRATIFICATION_RESIDUAL_LABELS = {
    "quotient",
    "tangent",
    "extension",
    "candidate_new_obstruction",
    "unknown",
}
STRATIFICATION_COUNTABLE_LABELS = {
    "eliminant",
    "dimension_degree",
    "residual:candidate_new_obstruction",
    "residual:unknown",
}


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


def parse_prime_field(field_name: str) -> int | None:
    match = re.fullmatch(r"F_(\d+)", field_name)
    if not match:
        return None
    return int(match.group(1))


def first_matching_key(data: dict[str, Any], *patterns: str) -> str | None:
    for pattern in patterns:
        regex = re.compile(pattern)
        for key in data:
            if regex.fullmatch(key):
                return key
    return None


def ref_path_part(ref: str) -> str:
    return ref.split("#", 1)[0]


def is_external_or_virtual_ref(ref: str) -> bool:
    return ref.startswith(
        ("inline:", "none:", "not_emitted:", "http://", "https://", "doi:")
    )


def validate_local_ref(ref: str, field: str) -> None:
    if not ref:
        raise PacketError(f"{field}: empty reference")
    if ref.startswith("not_emitted:"):
        raise PacketError(f"{field}: not_emitted references need a field-specific guard")
    if is_external_or_virtual_ref(ref):
        return
    path_part = ref_path_part(ref)
    if not path_part:
        raise PacketError(f"{field}: empty path before fragment")
    path = Path(path_part)
    if path.is_absolute():
        raise PacketError(f"{field}: absolute paths are not portable: {ref}")
    if not path.exists():
        raise PacketError(f"{field}: referenced file does not exist: {path_part}")


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
        validate_local_ref(
            ledger["certificate_ref"],
            f"removed_ledgers[{index}].certificate_ref",
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


def validate_references(packet: dict[str, Any]) -> None:
    for index, ledger in enumerate(packet.get("removed_ledgers", [])):
        validate_local_ref(
            ledger.get("certificate_ref", ""),
            f"removed_ledgers[{index}].certificate_ref",
        )


def validate_regular_minor(
    item: dict[str, Any], modulus: int | None
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
        non_roots = [root for root in roots if poly_eval_mod(coefficients, root, modulus)]
        if non_roots:
            raise PacketError(f"A={item.get('A')}: listed non-roots {non_roots}")

    return roots, bad_slopes


def is_zero_u_monomial(coefficients: list[int], degree: int) -> bool:
    return (
        len(coefficients) == degree + 1
        and degree >= 0
        and all(coefficient == 0 for coefficient in coefficients[:degree])
        and coefficients[degree] != 0
    )


def validate_zero_root_certificate(
    certificate: Any,
    coefficients: list[int],
    degree: int,
    roots: list[int],
    field: str,
) -> None:
    if not isinstance(certificate, dict):
        raise PacketError(f"{field}: root_certificate must be an object")
    if certificate.get("kind") != "split_linear_factorization":
        raise PacketError(f"{field}: unsupported root_certificate kind")
    if certificate.get("leading_coefficient") != coefficients[degree]:
        raise PacketError(f"{field}: root_certificate leading coefficient mismatch")
    if roots != [0]:
        raise PacketError(f"{field}: zero-u monomial certificate needs roots [0]")
    factors = certificate.get("factors")
    if factors != [{"root": 0, "multiplicity": degree}]:
        raise PacketError(f"{field}: zero-u monomial factors mismatch")


def validate_regular_minor_gcd(
    item: dict[str, Any], modulus: int | None
) -> tuple[list[int] | None, list[int]]:
    gcd = item.get("regular_minor_gcd")
    if not isinstance(gcd, dict):
        raise PacketError(f"A={item.get('A')}: regular_minor_gcd status needs data")

    for field in ("row_sets", "polynomial_ref", "degree", "root_hash", "minor_count"):
        if field not in gcd:
            raise PacketError(f"A={item.get('A')}: missing regular_minor_gcd.{field}")

    expected_size = item["j"] + 1
    row_sets_raw = gcd["row_sets"]
    if not isinstance(row_sets_raw, list) or not row_sets_raw:
        raise PacketError(f"A={item.get('A')}: regular_minor_gcd.row_sets must be nonempty")
    row_sets = [
        normalize_int_list(row_set, f"A={item.get('A')} gcd row_set[{index}]")
        for index, row_set in enumerate(row_sets_raw)
    ]
    for row_set in row_sets:
        if len(row_set) != expected_size:
            raise PacketError(
                f"A={item.get('A')}: gcd row_set has {len(row_set)} rows, expected {expected_size}"
            )
    if gcd["minor_count"] != len(row_sets):
        raise PacketError(
            f"A={item.get('A')}: minor_count={gcd['minor_count']} but row_sets has {len(row_sets)}"
        )

    if not isinstance(gcd["degree"], int) or gcd["degree"] < 0:
        raise PacketError(f"A={item.get('A')}: bad regular_minor_gcd.degree")
    if gcd["degree"] > expected_size:
        raise PacketError(
            f"A={item.get('A')}: gcd degree {gcd['degree']} exceeds j+1={expected_size}"
        )

    data = item.get("regular_minor_gcd_data")
    if data is None:
        return None, []
    if not isinstance(data, dict):
        raise PacketError(f"A={item.get('A')}: regular_minor_gcd_data must be an object")

    coefficient_key = first_matching_key(
        data, r"gcd_coefficients_mod_\d+_ascending", r"gcd_coefficients_ascending"
    )
    root_key = first_matching_key(data, r"roots_mod_\d+", r"roots")
    bad_slope_key = first_matching_key(
        data, r"enumerated_bad_slopes_mod_\d+", r"enumerated_bad_slopes"
    )
    if coefficient_key is None or root_key is None:
        raise PacketError(
            f"A={item.get('A')}: inline regular_minor_gcd_data needs coefficients and roots"
        )
    coefficients = require_int_list(
        data[coefficient_key], f"A={item.get('A')} gcd coefficients"
    )
    roots = normalize_int_list(data[root_key], f"A={item.get('A')} gcd roots")
    bad_slopes = normalize_int_list(
        data.get(bad_slope_key, []), f"A={item.get('A')} gcd bad_slopes"
    )
    if not coefficients:
        raise PacketError(f"A={item.get('A')}: empty gcd coefficient list")
    if all(coefficient == 0 for coefficient in coefficients):
        raise PacketError(f"A={item.get('A')}: zero regular-minor gcd polynomial")
    actual_degree = poly_degree(coefficients)
    if actual_degree != gcd["degree"]:
        raise PacketError(
            f"A={item.get('A')}: gcd degree field {gcd['degree']} != actual {actual_degree}"
        )
    if hash_json(roots) != gcd["root_hash"]:
        raise PacketError(f"A={item.get('A')}: gcd root_hash mismatch")
    if not set(bad_slopes).issubset(roots):
        raise PacketError(f"A={item.get('A')}: gcd bad slopes are not roots")
    if modulus is not None:
        non_roots = [root for root in roots if poly_eval_mod(coefficients, root, modulus)]
        if non_roots:
            raise PacketError(f"A={item.get('A')}: listed gcd non-roots {non_roots}")
    elif is_zero_u_monomial(coefficients, actual_degree):
        validate_zero_root_certificate(
            data.get("root_certificate"),
            coefficients,
            actual_degree,
            roots,
            f"A={item.get('A')} gcd",
        )

    minor_records = data.get("minor_polynomials_ascending", [])
    if not isinstance(minor_records, list):
        raise PacketError(f"A={item.get('A')}: minor_polynomials_ascending must be a list")
    if minor_records and len(minor_records) != len(row_sets):
        raise PacketError(
            f"A={item.get('A')}: minor polynomial count does not match row_sets"
        )
    for index, record in enumerate(minor_records):
        if not isinstance(record, dict):
            raise PacketError(f"A={item.get('A')}: minor record {index} must be object")
        record_row_set = normalize_int_list(
            record.get("row_set"), f"A={item.get('A')} minor record row_set[{index}]"
        )
        if record_row_set != row_sets[index]:
            raise PacketError(f"A={item.get('A')}: minor record row_set mismatch at {index}")
        record_coefficients = require_int_list(
            record.get("coefficients"), f"A={item.get('A')} minor record coefficients[{index}]"
        )
        record_degree = poly_degree(record_coefficients)
        if record.get("degree") != record_degree:
            raise PacketError(f"A={item.get('A')}: minor record degree mismatch at {index}")
        if is_zero_u_monomial(coefficients, actual_degree):
            if not is_zero_u_monomial(record_coefficients, actual_degree):
                raise PacketError(
                    f"A={item.get('A')}: zero-u gcd minor {index} is not a matching monomial"
                )

    return roots, bad_slopes


def expected_stratification_leaf(entry: dict[str, Any]) -> tuple[str, str]:
    raw_claims = entry.get("claim_ids")
    if not isinstance(raw_claims, list):
        raise PacketError("stratification_leaf_table entry: claim_ids must be a list")
    claims = []
    for claim in raw_claims:
        if claim not in STRATIFICATION_ORDER:
            raise PacketError(f"stratification_leaf_table: bad claim_id {claim!r}")
        claims.append(claim)

    for leaf_id in STRATIFICATION_ORDER:
        if leaf_id in claims:
            if leaf_id == "T6":
                terminal_label = entry.get("terminal_label")
                if terminal_label not in STRATIFICATION_CLOSED_LABELS:
                    raise PacketError(
                        "stratification_leaf_table: T6 needs closed terminal label"
                    )
                return leaf_id, terminal_label
            return leaf_id, STRATIFICATION_LABELS[leaf_id]

    residual_label = entry.get("residual_label", "unknown")
    if residual_label not in STRATIFICATION_RESIDUAL_LABELS:
        raise PacketError(
            f"stratification_leaf_table: bad residual_label {residual_label!r}"
        )
    return "T7", f"residual:{residual_label}"


def validate_stratification_leaf_table(packet: dict[str, Any]) -> None:
    table = packet.get("stratification_leaf_table")
    if table is None:
        return
    if not isinstance(table, list):
        raise PacketError("stratification_leaf_table must be a list")

    seen_candidates: set[int] = set()
    counted: set[int] = set()
    counted_labels = packet.get(
        "stratification_counted_terminal_labels",
        sorted(STRATIFICATION_COUNTABLE_LABELS),
    )
    if not isinstance(counted_labels, list):
        raise PacketError("stratification_counted_terminal_labels must be a list")
    counted_label_set = set()
    for label in counted_labels:
        if label not in STRATIFICATION_COUNTABLE_LABELS:
            raise PacketError(f"bad counted terminal label {label!r}")
        counted_label_set.add(label)

    for index, entry in enumerate(table):
        if not isinstance(entry, dict):
            raise PacketError(f"stratification_leaf_table[{index}] must be an object")
        candidate = entry.get("candidate")
        if not isinstance(candidate, int):
            raise PacketError(f"stratification_leaf_table[{index}].candidate must be int")
        if candidate in seen_candidates:
            raise PacketError(f"stratification candidate {candidate} appears twice")
        seen_candidates.add(candidate)

        expected_leaf, expected_label = expected_stratification_leaf(entry)
        if entry.get("leaf_id") != expected_leaf:
            raise PacketError(
                "stratification candidate {candidate}: leaf_id {actual!r} "
                "should be {expected!r}".format(
                    candidate=candidate,
                    actual=entry.get("leaf_id"),
                    expected=expected_leaf,
                )
            )
        if entry.get("terminal_label") != expected_label:
            raise PacketError(
                "stratification candidate {candidate}: terminal_label {actual!r} "
                "should be {expected!r}".format(
                    candidate=candidate,
                    actual=entry.get("terminal_label"),
                    expected=expected_label,
                )
            )
        if expected_label in counted_label_set:
            counted.add(candidate)

    if "stratification_counted_union" in packet:
        declared = normalize_int_list(
            packet["stratification_counted_union"],
            "stratification_counted_union",
        )
        if declared != sorted(counted):
            raise PacketError(
                "stratification_counted_union does not match first-match counted leaves"
            )
        if "declared_aperiodic_numerator" in packet:
            numerator = packet["declared_aperiodic_numerator"]
            if numerator != len(declared):
                raise PacketError(
                    "declared_aperiodic_numerator="
                    f"{numerator} but stratification_counted_union has size "
                    f"{len(declared)}"
                )


def packet_has_residual_obstruction(packet: dict[str, Any]) -> bool:
    for item in packet.get("exact_agreements", []):
        if item.get("status") == "residual_obstruction":
            return True
        for chart in item.get("charts", []):
            for pivot in chart.get("pivot_records", []):
                if pivot.get("status") == "residual_obstruction":
                    return True
    return False


def validate_not_emitted_root_union_ref(packet: dict[str, Any], ref: str) -> None:
    if ref == "not_emitted:":
        raise PacketError("root_union_table_ref: empty not_emitted reason")
    if not packet_has_residual_obstruction(packet):
        raise PacketError(
            "root_union_table_ref: not_emitted requires a residual_obstruction branch"
        )


def validate_packet(packet: dict[str, Any], schema_path: Path) -> None:
    validate_schema(packet, schema_path)
    validate_residual_labels(packet)
    validate_references(packet)
    validate_stratification_leaf_table(packet)

    row = packet["row"]
    n = row["n"]
    k = row["k"]
    modulus = parse_prime_field(row["field"])
    all_roots: set[int] = set()
    all_bad: set[int] = set()

    for item in packet["exact_agreements"]:
        agreement = item["A"]
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
                roots, bad_slopes = validate_regular_minor_gcd(item, modulus)
            else:
                roots, bad_slopes = validate_regular_minor(item, modulus)
            if roots is not None:
                all_roots.update(roots)
            all_bad.update(bad_slopes)

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
    elif "root_union_table_ref" in packet:
        root_union_ref = packet["root_union_table_ref"]
        if root_union_ref.startswith("not_emitted:"):
            validate_not_emitted_root_union_ref(packet, root_union_ref)
        else:
            validate_local_ref(root_union_ref, "root_union_table_ref")

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
