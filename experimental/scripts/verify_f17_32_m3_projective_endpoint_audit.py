#!/usr/bin/env python3
"""Verify the projective endpoint audit for the F_17^32 M3 top window.

The source packet is finite-affine.  This sidecar checks the extra projective
point [0:1] for the fixed synthetic top-window packet A=421..426.  In each
bucket the regular-minor determinant is a nonzero scalar times Z^(j+1), so the
homogenized determinant is nonzero at infinity and [0:1] contributes no extra
projective slope.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_aperiodic_eliminant_packet import PolynomialBasisField


SCHEMA_VERSION = "f17-32-m3-projective-endpoint-audit-v1"
TOP_WINDOW_MIN = 421
TOP_WINDOW_MAX = 426
ROOT_UNION = [0]
TWO128 = 2**128

TOP_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_packet.json"
)
ZERO_SLOPE_SUBTRACTION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/"
    "f17_32_n512_k256_a421_426_zero_slope_subtraction.json"
)
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-projective-endpoint-audit/"
    "f17_32_n512_k256_a421_426_projective_endpoint_audit.json"
)


def load_json(ref: str) -> dict[str, Any]:
    return json.loads((ROOT / ref).read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def top_window_items(packet: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(item["A"]): item for item in packet["exact_agreements"]}


def zero_subtraction_items(certificate: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(item["A"]): item for item in certificate["per_agreement"]}


def coefficients(item: dict[str, Any]) -> list[int]:
    data = item.get("regular_minor_polynomial_data")
    require(isinstance(data, dict), f"A={item.get('A')}: missing polynomial data")
    values = data.get("coefficients_ascending")
    require(isinstance(values, list), f"A={item.get('A')}: missing coefficients")
    require(
        all(isinstance(value, int) for value in values),
        f"A={item.get('A')}: coefficients must be integers",
    )
    return values


def build_records(
    top_packet: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
    field: PolynomialBasisField,
) -> list[dict[str, Any]]:
    top_by_a = top_window_items(top_packet)
    zero_by_a = zero_subtraction_items(zero_slope_subtraction)
    records = []
    for agreement in range(TOP_WINDOW_MIN, TOP_WINDOW_MAX + 1):
        item = top_by_a[agreement]
        zero_item = zero_by_a[agreement]
        require(item["status"] == "regular_minor", f"A={agreement}: not regular")
        top_degree = item["j"] + 1
        require(
            item["regular_minor"]["degree"] == top_degree,
            f"A={agreement}: degree is not j+1",
        )
        poly = coefficients(item)
        require(len(poly) == top_degree + 1, f"A={agreement}: bad coefficient length")
        require(
            all(coefficient == 0 for coefficient in poly[:top_degree]),
            f"A={agreement}: determinant is not monomial in Z",
        )
        top_coefficient = poly[top_degree]
        require(
            not field.is_zero(field.decode(top_coefficient)),
            f"A={agreement}: top coefficient vanishes",
        )
        roots = item["regular_minor_data"]["roots"]
        require(roots == ROOT_UNION, f"A={agreement}: finite root union mismatch")
        require(
            zero_item["B_ap_after_removed_ledgers"] == 0,
            f"A={agreement}: zero-slope subtraction mismatch",
        )
        require(
            zero_item["overlap_regular_tangent_roots"] == ROOT_UNION,
            f"A={agreement}: tangent overlap mismatch",
        )
        records.append(
            {
                "A": agreement,
                "j": item["j"],
                "t": item["t"],
                "top_degree": top_degree,
                "top_coefficient_encoding": top_coefficient,
                "finite_root_union_before_removed_ledgers": ROOT_UNION,
                "projective_infinity": {
                    "projective_point": "[0:1]",
                    "status": "empty",
                    "contribution": 0,
                    "reason": (
                        "the homogenized determinant evaluates to the nonzero "
                        "top coefficient at [0:1]"
                    ),
                },
                "aperiodic_root_union_after_removed_ledgers": [],
                "B_ap_after_removed_ledgers": 0,
            }
        )
    return records


def validate_inputs(
    top_packet: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
) -> PolynomialBasisField:
    require(
        top_packet["schema_version"] == "aperiodic-hankel-eliminant-v1",
        "top-window packet schema mismatch",
    )
    require(top_packet["sampler"] == "finite_affine_line", "source packet sampler mismatch")
    require(top_packet["root_union"] == ROOT_UNION, "source root union mismatch")
    require(top_packet["declared_aperiodic_numerator"] == 1, "source numerator mismatch")
    require(
        [item["A"] for item in top_packet["exact_agreements"]]
        == list(range(TOP_WINDOW_MIN, TOP_WINDOW_MAX + 1)),
        "top-window agreement range mismatch",
    )
    require(
        zero_slope_subtraction["schema_version"]
        == "f17-32-m3-zero-slope-subtraction-v1",
        "zero-slope subtraction schema mismatch",
    )
    require(
        zero_slope_subtraction["source_artifacts"]["fixed_top_window_packet"]["ref"]
        == TOP_PACKET_REF,
        "zero-slope subtraction source packet mismatch",
    )
    field = PolynomialBasisField.from_packet(top_packet)
    require(field is not None, "top-window packet lacks field model")
    require(field.size == 17**32, "unexpected field size")
    return field


def build_audit() -> dict[str, Any]:
    top_packet = load_json(TOP_PACKET_REF)
    zero_slope_subtraction = load_json(ZERO_SLOPE_SUBTRACTION_REF)
    field = validate_inputs(top_packet, zero_slope_subtraction)
    records = build_records(top_packet, zero_slope_subtraction, field)
    finite_denominator = field.size
    projective_denominator = field.size + 1
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "row": top_packet["row"],
        "source_artifacts": {
            "fixed_top_window_packet": {
                "ref": TOP_PACKET_REF,
                "sha256": sha256_file(TOP_PACKET_REF),
                "sampler": top_packet["sampler"],
            },
            "zero_slope_subtraction": {
                "ref": ZERO_SLOPE_SUBTRACTION_REF,
                "sha256": sha256_file(ZERO_SLOPE_SUBTRACTION_REF),
            },
        },
        "endpoint_conventions": {
            "finite_affine_slope_denominator": finite_denominator,
            "projective_slope_denominator": projective_denominator,
            "finite_budget_numerator": finite_denominator // TWO128,
            "projective_budget_numerator": projective_denominator // TWO128,
            "extra_projective_point": "[0:1]",
        },
        "summary": {
            "agreements": len(records),
            "agreement_range": {"A_min": TOP_WINDOW_MIN, "A_max": TOP_WINDOW_MAX},
            "finite_root_union_before_removed_ledgers": ROOT_UNION,
            "projective_infinity_contribution_before_removed_ledgers": 0,
            "projective_regular_numerator_before_removed_ledgers": 1,
            "aperiodic_root_union_after_removed_ledgers": [],
            "deduped_aperiodic_numerator_after_removed_ledgers": 0,
            "interpretation": (
                "For this fixed synthetic top-window packet, passing from "
                "finite-affine to projective slopes adds no regular-minor root "
                "at infinity."
            ),
        },
        "per_agreement": records,
        "nonclaims": [
            "not actual M3 row data",
            "not a worst-case MCA bound",
            "not a new quotient/tangent subtraction table",
            "does not convert the source packet itself to sampler=projective_line",
        ],
    }


def check_audit(path: Path) -> None:
    expected = render(build_audit())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"projective endpoint audit mismatch: {path}")


def print_summary(audit: dict[str, Any]) -> None:
    summary = audit["summary"]
    print("F_17^32 M3 projective endpoint audit")
    print(
        "window: A={A_min}..{A_max}, agreements={agreements}".format(
            agreements=summary["agreements"],
            **summary["agreement_range"],
        )
    )
    print(
        "infinity contribution={projective_infinity_contribution_before_removed_ledgers}; "
        "aperiodic after removed ledgers={deduped_aperiodic_numerator_after_removed_ledgers}".format(
            **summary
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic audit JSON")
    parser.add_argument("--check", type=Path, help="check deterministic audit JSON")
    parser.add_argument("--json", action="store_true", help="print audit JSON")
    args = parser.parse_args()
    audit = build_audit()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(audit), encoding="utf-8")
    if args.check:
        check_audit(args.check)
    if args.json:
        print(render(audit), end="")
        return
    print_summary(audit)


if __name__ == "__main__":
    main()
