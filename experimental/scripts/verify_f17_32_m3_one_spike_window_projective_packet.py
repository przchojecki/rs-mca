#!/usr/bin/env python3
"""Emit and verify the v9 projective-line packet for the M3 one-spike window."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.verify_f17_32_m3_low_rank6_11_shifted_minor_exclusion import (  # noqa: E402
    field_from_descriptor,
)
from experimental.scripts.verify_f17_32_m3_one_spike_window_full_hankel import (  # noqa: E402
    AGREEMENT_MAX,
    AGREEMENT_MIN,
    BUDGET_NUMERATOR,
    K,
    N,
    ONE_SPIKE_TEMPLATE_NOTE_REF,
    ONE_SPIKE_TEMPLATE_REF,
    OUTPUT_PATH as FULL_HANKEL_OUTPUT_PATH,
    ROW_DESCRIPTOR_REF,
    build_records,
    hash_json,
)


SCHEMA_VERSION = "aperiodic-hankel-eliminant-v1"
OUTPUT_PATH = REPO_ROOT / (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-one-spike-window-projective-line/"
    "f17_32_n512_k256_m3_one_spike_window_projective_line_packet.json"
)


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else REPO_ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(ref: str | Path) -> str:
    path = ref if isinstance(ref, Path) else REPO_ROOT / ref
    return sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sampler_audit(field_order: int) -> dict[str, Any]:
    return {
        "sampler": "projective_line",
        "slope_field": "F_17^32",
        "slope_field_order": field_order,
        "denominator": field_order + 1,
        "denominator_formula": "|P^1(F)| = |F| + 1",
        "field_role": "q_line",
        "extension_denominator_warning": (
            "extension-valued slope packets are divided by the slope-field "
            "projective-line denominator, not by the base field"
        ),
    }


def source_record(
    name: str,
    ref: str | Path,
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    ref_text = str(ref)
    if isinstance(ref, Path):
        ref_text = str(ref.relative_to(REPO_ROOT))
    record = {
        "name": name,
        "ref": ref_text,
        "sha256": file_sha256(ref),
    }
    if data is not None:
        record["schema_version"] = data.get("schema_version")
        record["status"] = data.get("status")
    return record


def projective_item(record: dict[str, Any], field_size: int) -> dict[str, Any]:
    coefficients = record["regular_minor_coefficients_ascending"]
    root = record["finite_root"]
    root_table = [root]
    row_set = list(range(record["minor_size"]))
    top_degree = record["minor_size"]
    top_coefficient = coefficients[top_degree] if top_degree < len(coefficients) else 0
    require(top_coefficient == 0, f"A={record['A']}: expected endpoint top coefficient 0")
    return {
        "A": record["A"],
        "j": record["j"],
        "t": record["t"],
        "status": "regular_minor",
        "regular_minor": {
            "row_set": row_set,
            "polynomial_ref": "inline:regular_minor.coefficients_ascending",
            "degree": record["regular_minor_degree"],
            "root_hash": hash_json(root_table),
        },
        "regular_minor_data": {
            "coefficients_ascending": coefficients,
            "field_encoding": "base-p low-to-high integer",
            "field_extension_degree": 32,
            "p": 17,
            "roots": root_table,
            "root_certificate": {
                "kind": "split_linear_factorization",
                "field_encoding": "base-p low-to-high integer",
                "leading_coefficient": coefficients[1],
                "factors": [
                    {
                        "root": root,
                        "multiplicity": 1,
                    }
                ],
            },
        },
        "regular_minor_polynomial_data": {
            "coefficients_ascending": coefficients,
            "field_encoding": "base-p low-to-high integer",
            "field_extension_degree": 32,
            "p": 17,
        },
        "projective_infinity": {
            "projective_point": "[0:1]",
            "status": "nonempty",
            "top_degree": top_degree,
            "top_coefficient": 0,
            "field_encoding": "base-p low-to-high integer",
            "contribution": 1,
            "reason": (
                "The one-spike affine determinant has degree 1, strictly below "
                "the homogenizing degree j+1, so the projective endpoint is "
                "not excluded by this regular minor."
            ),
            "full_hankel_endpoint_charge_ref": (
                str(FULL_HANKEL_OUTPUT_PATH.relative_to(REPO_ROOT))
                + "#/method/endpoint_quotient_image"
            ),
        },
        "extractor_audit": {
            "certificate_mode": "one_spike_window_projective_line",
            "field_size": field_size,
            "row_set_source": "one_spike_linear_prefix",
            "tested_row_sets": 1,
            "degree_bound": 1,
            "root_count": 1,
            "spike_exponent": record["spike_exponent"],
            "shifted_minor_excludes_finite_root": (
                record["finite_regular_roots_excluded_by_shifted_minor"] == 1
            ),
            "endpoint_quotient_image_witness": (
                record["endpoint_quotient_image_witness"] == 1
            ),
        },
    }


def build_packet() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    template = load_json(ONE_SPIKE_TEMPLATE_REF)
    full_hankel = load_json(FULL_HANKEL_OUTPUT_PATH)
    field = field_from_descriptor(descriptor)
    domain = [field.decode(value) for value in descriptor["domain"]["domain_encodings"]]
    records = build_records(domain, field)
    finite_root_union = sorted({record["finite_root"] for record in records})

    require(full_hankel["status"] == "PROVED / AUDIT", "full-Hankel source status")
    require(full_hankel["aggregate"]["record_count"] == 42, "full-Hankel record count")
    require(len(records) == 42, "record count")
    require(len(finite_root_union) == 42, "finite root union should have 42 roots")

    field_order = descriptor["row"]["field_order"]
    packet = {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": {
            "n": N,
            "k": K,
            "field": descriptor["row"]["field"],
            "domain_hash": descriptor["row"]["domain_hash"],
            "domain_description": (
                "order-512 subgroup from the pinned F_17^32 row descriptor; "
                "synthetic one-spike M3 projective-line packet"
            ),
        },
        "agreement_threshold": AGREEMENT_MIN,
        "sampler": "projective_line",
        "sampler_audit": sampler_audit(field_order),
        "claim_scope": {
            "row_data": "synthetic_syndrome_pencil",
            "threshold_role": "synthetic_stress",
            "root_status": "closed_form",
            "may_be_used_for_threshold_pinning": False,
            "note": (
                "All-window non-proportional one-spike projective-line packet; "
                "this is a synthetic v9 stress packet, not an actual-row MCA bound."
            ),
        },
        "removed_ledgers": [],
        "exact_agreements": [
            projective_item(record, field_order) for record in records
        ],
        "root_union": finite_root_union,
        "root_union_table_ref": "inline:root_union",
        "enumerated_bad_slope_union": [],
        "declared_aperiodic_numerator": len(finite_root_union) + 1,
        "projective_endpoint_union": {
            "projective_point": "[0:1]",
            "contribution": 1,
            "charged_to_quotient_image_in_full_hankel_ledger": True,
            "full_hankel_ledger_ref": str(FULL_HANKEL_OUTPUT_PATH.relative_to(REPO_ROOT)),
        },
        "extractor": {
            "name": "one-spike-window-projective-packet-generator",
            "method": (
                "Cauchy-Binet one-spike affine determinant plus projective-line "
                "homogenized endpoint audit"
            ),
            "input_ref": str(FULL_HANKEL_OUTPUT_PATH.relative_to(REPO_ROOT)),
            "input_sha256": file_sha256(FULL_HANKEL_OUTPUT_PATH),
            "row_set_strategy": {"type": "prefix"},
            "scope": (
                "synthetic one-spike syndrome pencils over the pinned "
                "polynomial-basis F_17^32 row"
            ),
            "field_model": {
                "kind": "polynomial_basis",
                "p": descriptor["field_model"]["p"],
                "degree": descriptor["field_model"]["degree"],
                "modulus": descriptor["field_model"]["modulus"],
                "encoding": "base-p low-to-high integer",
            },
        },
        "source_artifacts": [
            source_record("row_descriptor", ROW_DESCRIPTOR_REF, descriptor),
            source_record("one_spike_template", ONE_SPIKE_TEMPLATE_REF, template),
            source_record("one_spike_template_note", ONE_SPIKE_TEMPLATE_NOTE_REF),
            source_record("one_spike_window_full_hankel", FULL_HANKEL_OUTPUT_PATH, full_hankel),
        ],
        "aggregate": {
            "agreement_range": [AGREEMENT_MIN, AGREEMENT_MAX],
            "exact_agreement_count": len(records),
            "finite_root_union_size": len(finite_root_union),
            "projective_endpoint_union_contribution": 1,
            "declared_projective_numerator": len(finite_root_union) + 1,
            "projective_budget_numerator": BUDGET_NUMERATOR,
            "finite_roots_cleared_from_full_hankel_by_shifted_minor": (
                full_hankel["aggregate"][
                    "finite_regular_roots_excluded_by_shifted_minor_sum"
                ]
            ),
            "aperiodic_full_hankel_residual_after_endpoint_image": (
                full_hankel["aggregate"][
                    "max_aperiodic_full_hankel_projective_upper_per_record"
                ]
            ),
        },
        "nonclaims": [
            "synthetic one-spike syndrome-pencil packet only",
            "not an arbitrary M3 row theorem",
            "not an actual-row safe-side threshold certificate",
            "the v9 projective numerator counts the regular-minor endpoint; the companion full-Hankel ledger charges that endpoint to quotient-image",
        ],
    }
    return packet


def check_packet(packet: dict[str, Any], path: Path) -> None:
    actual = path.read_text(encoding="utf-8")
    expected = render(packet)
    if actual != expected:
        raise AssertionError(f"one-spike v9 projective packet mismatch: {path}")


def print_summary(packet: dict[str, Any]) -> None:
    aggregate = packet["aggregate"]
    print("F_17^32 M3 one-spike window v9 projective-line packet")
    print(f"status: {packet['status']}")
    print(
        "records={records}, finite_union={finite}, projective_numerator={num}, "
        "full_hankel_residual={residual}".format(
            records=aggregate["exact_agreement_count"],
            finite=aggregate["finite_root_union_size"],
            num=aggregate["declared_projective_numerator"],
            residual=aggregate["aperiodic_full_hankel_residual_after_endpoint_image"],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic v9 packet")
    parser.add_argument("--check", type=Path, help="check deterministic v9 packet")
    parser.add_argument("--json", action="store_true", help="print packet JSON")
    args = parser.parse_args()

    packet = build_packet()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(packet), encoding="utf-8")
    if args.check:
        check_packet(packet, args.check)
    if args.json:
        print(render(packet), end="")
        return
    print_summary(packet)


if __name__ == "__main__":
    main()
