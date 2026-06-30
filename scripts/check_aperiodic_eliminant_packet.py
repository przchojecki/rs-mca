#!/usr/bin/env python3
"""Check Paper D v9 aperiodic Hankel eliminant packets.

The JSON schema catches the structural contract.  This script adds the
arithmetical checks that are easiest to get wrong in generated packets:
``j=n-A``, ``t=A-k``, residual labels, regular-minor degree/root hashes, and
declared root-union numerators when the packet includes inline root tables.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import re
from typing import Any


DEFAULT_SCHEMA = Path("scripts/aperiodic_eliminant_schema.json")


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


def validate_schema(packet: Any, schema_path: Path) -> None:
    schema = load_json(schema_path)
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise PacketError(
            "jsonschema is required for schema validation; install jsonschema"
        ) from exc

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(packet), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "<root>"
        raise PacketError(f"schema error at {location}: {first.message}")


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


def validate_removed_ledgers(packet: dict[str, Any]) -> None:
    for index, ledger in enumerate(packet.get("removed_ledgers", [])):
        for field in ("name", "certificate_ref"):
            value = ledger.get(field)
            if not isinstance(value, str) or not value.strip():
                raise PacketError(f"removed_ledgers[{index}]: empty {field}")


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


def validate_packet(packet: dict[str, Any], schema_path: Path) -> None:
    validate_schema(packet, schema_path)
    validate_residual_labels(packet)
    validate_removed_ledgers(packet)

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
