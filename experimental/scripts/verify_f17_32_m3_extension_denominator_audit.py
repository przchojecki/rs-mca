#!/usr/bin/env python3
"""Verify the denominator audit for the F_17^32 M3 line-value packet."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-extension-denominator-audit-v1"
P = 17
EXTENSION_DEGREE = 32
N = 512
K = 256
Q_BASE = P
Q_LINE = P**EXTENSION_DEGREE
EPS_DENOMINATOR_BITS = 128

TOP_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_packet.json"
)
LINE_VALUE_LIFT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-line-value-lift/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json"
)
ZERO_SLOPE_SUBTRACTION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/"
    "f17_32_n512_k256_a421_426_zero_slope_subtraction.json"
)
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/"
    "f17_32_n512_k256_a421_426_extension_denominator_audit.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def is_base_field_value(encoded: int) -> bool:
    return 0 <= encoded < P


def value_stats(values: list[int]) -> dict[str, Any]:
    base_count = sum(1 for value in values if is_base_field_value(value))
    nonzero_count = sum(1 for value in values if value != 0)
    first_nonbase = next(
        (
            {"index": index, "value": value}
            for index, value in enumerate(values)
            if not is_base_field_value(value)
        ),
        None,
    )
    return {
        "length": len(values),
        "base_field_values": base_count,
        "nonbase_values": len(values) - base_count,
        "nonzero_values": nonzero_count,
        "first_nonbase_value": first_nonbase,
    }


def validate_inputs(
    packet: dict[str, Any],
    line_value_lift: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
) -> None:
    require(packet["row"]["n"] == N, "packet n mismatch")
    require(packet["row"]["k"] == K, "packet k mismatch")
    require(packet["row"]["field"] == "F_17^32", "packet field mismatch")
    require(packet["sampler"] == "finite_affine_line", "packet sampler mismatch")
    require(
        line_value_lift["schema_version"] == "f17-32-m3-line-value-lift-v1",
        "line-value lift schema mismatch",
    )
    require(
        line_value_lift["source_packet"]["fixed_top_window_packet_ref"] == TOP_PACKET_REF,
        "line-value lift packet ref mismatch",
    )
    require(
        zero_slope_subtraction["schema_version"]
        == "f17-32-m3-zero-slope-subtraction-v1",
        "zero-slope subtraction schema mismatch",
    )
    require(
        zero_slope_subtraction["source_artifacts"]["line_value_lift"]["ref"]
        == LINE_VALUE_LIFT_REF,
        "zero-slope subtraction line-value ref mismatch",
    )
    require(Q_LINE < 2**256, "line field violates prize field-size cap")
    require(Q_LINE // 2**EPS_DENOMINATOR_BITS == 6, "line denominator budget mismatch")


def build_certificate() -> dict[str, Any]:
    packet = load_json(TOP_PACKET_REF)
    line_value_lift = load_json(LINE_VALUE_LIFT_REF)
    zero_slope_subtraction = load_json(ZERO_SLOPE_SUBTRACTION_REF)
    validate_inputs(packet, line_value_lift, zero_slope_subtraction)

    f_values = line_value_lift["line_values"]["f"]
    g_values = line_value_lift["line_values"]["g"]
    require(len(f_values) == N, "f length mismatch")
    require(len(g_values) == N, "g length mismatch")
    f_stats = value_stats(f_values)
    g_stats = value_stats(g_values)
    require(f_stats["base_field_values"] == N, "f is not base-valued")
    require(f_stats["nonzero_values"] == 0, "f is not the zero vector")
    require(g_stats["nonbase_values"] == N, "g is not everywhere extension-valued")
    require(g_stats["nonzero_values"] == N, "g has zero values")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "AUDIT",
        "row": packet["row"],
        "source_artifacts": {
            "fixed_top_window_packet": {
                "ref": TOP_PACKET_REF,
                "sha256": sha256_file(TOP_PACKET_REF),
                "schema_version": packet["schema_version"],
            },
            "line_value_lift": {
                "ref": LINE_VALUE_LIFT_REF,
                "sha256": sha256_file(LINE_VALUE_LIFT_REF),
                "schema_version": line_value_lift["schema_version"],
            },
            "zero_slope_subtraction": {
                "ref": ZERO_SLOPE_SUBTRACTION_REF,
                "sha256": sha256_file(ZERO_SLOPE_SUBTRACTION_REF),
                "schema_version": zero_slope_subtraction["schema_version"],
            },
        },
        "field_ledgers": {
            "base_field": "F_17",
            "ambient_line_field": "F_17^32",
            "q_base": Q_BASE,
            "q_line": Q_LINE,
            "finite_affine_slope_denominator": Q_LINE,
            "projective_slope_denominator": Q_LINE + 1,
            "epsilon_star": "2^-128",
            "finite_affine_budget": Q_LINE // 2**EPS_DENOMINATOR_BITS,
            "base_field_budget_if_wrongly_used": Q_BASE // 2**EPS_DENOMINATOR_BITS,
            "denominator_rule": (
                "Because the packet samples finite affine slopes z in F_17^32, "
                "the support-wise MCA numerator must be divided by q_line=17^32."
            ),
        },
        "line_value_classification": {
            "field_encoding": "base-p low-to-high polynomial-basis integer",
            "base_field_embedding": "encoded values 0..16",
            "f": f_stats,
            "g": g_stats,
            "classification": (
                "The line is genuinely F_17^32-valued: f is the zero "
                "base-field vector, while every g(x) is outside the base field."
            ),
        },
        "subtraction_context": {
            "zero_slope": 0,
            "zero_slope_is_base_field_element": True,
            "zero_slope_subtraction_ref": ZERO_SLOPE_SUBTRACTION_REF,
            "deduped_aperiodic_numerator_after_zero_slope_subtraction": 0,
            "denominator_for_that_statement": Q_LINE,
        },
        "nonclaims": [
            "not an extension-line lift theorem",
            "not a base-field MCA packet",
            "not actual M3 row data",
            "not a Prime192 denominator audit",
            "not a safe-side MCA bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"extension denominator audit mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    ledgers = certificate["field_ledgers"]
    classification = certificate["line_value_classification"]
    print("F_17^32 M3 extension-denominator audit")
    print(
        "q_base={q_base}, q_line={q_line}, finite_affine_budget={finite_affine_budget}".format(
            **ledgers
        )
    )
    print(
        "f: base={base_field_values}/{length}, nonzero={nonzero_values}".format(
            **classification["f"]
        )
    )
    print(
        "g: nonbase={nonbase_values}/{length}, nonzero={nonzero_values}".format(
            **classification["g"]
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic audit JSON")
    parser.add_argument("--check", type=Path, help="check deterministic audit JSON")
    parser.add_argument("--json", action="store_true", help="print audit JSON")
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    if args.json:
        print(render(certificate), end="")
        return
    print_summary(certificate)


if __name__ == "__main__":
    main()
