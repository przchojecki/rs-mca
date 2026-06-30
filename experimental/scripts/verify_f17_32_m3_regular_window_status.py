#!/usr/bin/env python3
"""Verify the F_17^32 M3 regular-window status ledger.

This is an audit ledger for the Paper D v9 M3 work.  It combines the existing
regular-window plan, generic all-row-set nonsingularity certificate, synthetic
rank-witness family, and fixed top-window v9 packet into one compact status
object.  It deliberately does not claim an actual-row MCA bound.
"""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-regular-window-status-v1"
AGREEMENT_MIN = 385
AGREEMENT_MAX = 426
TOP_WINDOW_MIN = 421
TOP_WINDOW_MAX = 426
ROOT_UNION = [0]

PLAN_REF = (
    "experimental/data/certificates/hankel-regular-window-f17-385-426/"
    "f17_32_n512_k256_regular_window_plan.json"
)
GENERIC_REF = (
    "experimental/data/certificates/hankel-f17-32-generic-regular-minor/"
    "f17_32_n512_k256_m3_generic_all_row_set_regular_minor_certificate.json"
)
FAMILY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank-witness-family/"
    "f17_32_n512_k256_m3_rank_witness_family_certificate.json"
)
TOP_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_packet.json"
)
LINE_VALUE_LIFT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-line-value-lift/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json"
)
SUBGROUP_SECTION_REF = (
    "experimental/data/certificates/subgroup-syndrome-section/"
    "subgroup_syndrome_section_certificate.json"
)
SYNDROME_REALIZABILITY_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-syndrome-realizability/"
    "f17_32_n512_k256_m3_syndrome_realizability_certificate.json"
)
ZERO_SLOPE_SUBTRACTION_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/"
    "f17_32_n512_k256_a421_426_zero_slope_subtraction.json"
)
EXTENSION_DENOMINATOR_AUDIT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-extension-denominator-audit/"
    "f17_32_n512_k256_a421_426_extension_denominator_audit.json"
)
PROJECTIVE_ENDPOINT_AUDIT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-endpoint-audit/"
    "f17_32_n512_k256_a421_426_projective_endpoint_audit.json"
)
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-regular-window-status/"
    "f17_32_n512_k256_m3_regular_window_status.json"
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


def artifact_record(name: str, ref: str, schema_version: str) -> dict[str, Any]:
    data = load_json(ref)
    require(data.get("schema_version") == schema_version, f"{name}: schema mismatch")
    return {
        "name": name,
        "ref": ref,
        "schema_version": schema_version,
        "sha256": sha256_file(ref),
        "status": data.get("status"),
    }


def top_window_by_agreement(packet: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(item["A"]): item for item in packet["exact_agreements"]}


def validate_inputs(
    plan: dict[str, Any],
    generic: dict[str, Any],
    family: dict[str, Any],
    top_packet: dict[str, Any],
    line_value_lift: dict[str, Any],
    subgroup_section: dict[str, Any],
    syndrome_realizability: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
    extension_denominator_audit: dict[str, Any],
    projective_endpoint_audit: dict[str, Any],
) -> None:
    require(plan["window"]["A_min"] == AGREEMENT_MIN, "plan A_min mismatch")
    require(plan["window"]["A_max"] == AGREEMENT_MAX, "plan A_max mismatch")
    require(plan["budget_context"]["degree_bound_sum"] == 4515, "bad degree sum")
    require(generic["claim"]["degree_sum"] == 4515, "generic degree sum mismatch")
    require(
        generic["claim"]["regular_window"] == {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
        "generic window mismatch",
    )
    require(len(generic["agreements"]) == 42, "generic agreement count mismatch")
    require(len(family["agreements"]) == 42, "family agreement count mismatch")
    require(
        family["claim"]["closed_form_root_union"] == ROOT_UNION,
        "family root union mismatch",
    )
    require(
        top_packet["exact_agreements"][0]["A"] == TOP_WINDOW_MIN
        and top_packet["exact_agreements"][-1]["A"] == TOP_WINDOW_MAX,
        "top-window packet range mismatch",
    )
    require(top_packet["root_union"] == ROOT_UNION, "top-window root union mismatch")
    require(
        top_packet["declared_aperiodic_numerator"] == 1,
        "top-window numerator mismatch",
    )
    require(
        line_value_lift["source_packet"]["fixed_top_window_input_ref"]
        == top_packet["extractor"]["input_ref"],
        "line-value lift input ref mismatch",
    )
    require(
        line_value_lift["source_packet"]["fixed_top_window_packet_ref"] == TOP_PACKET_REF,
        "line-value lift packet ref mismatch",
    )
    require(
        line_value_lift["syndrome_replay"]["matches_fixed_top_window_input"] is True,
        "line-value lift does not replay the fixed input",
    )
    section_cases = {case["name"]: case for case in subgroup_section["cases"]}
    require(
        "F17_32_H512_fixed_top_window" in section_cases,
        "subgroup section lacks the F17^32 fixed top-window case",
    )
    require(
        section_cases["F17_32_H512_fixed_top_window"]["line_value_lift_ref"]
        == LINE_VALUE_LIFT_REF,
        "subgroup section does not reference the line-value lift",
    )
    require(
        syndrome_realizability["schema_version"]
        == "f17-32-m3-syndrome-realizability-v1",
        "syndrome realizability schema mismatch",
    )
    require(
        syndrome_realizability["source_artifacts"]["subgroup_syndrome_section"]["ref"]
        == SUBGROUP_SECTION_REF,
        "syndrome realizability subgroup-section ref mismatch",
    )
    require(
        syndrome_realizability["row"]["domain_hash"] == plan["row"]["domain_hash"],
        "syndrome realizability domain mismatch",
    )
    require(
        syndrome_realizability["summary"]["regular_window"]
        == {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
        "syndrome realizability window mismatch",
    )
    require(
        syndrome_realizability["summary"]["visible_syndrome_length"] == 256,
        "syndrome realizability length mismatch",
    )
    require(
        syndrome_realizability["summary"]["pencil_realizability"]
        == "surjective onto all length-256 u,v syndrome pencils",
        "syndrome realizability summary mismatch",
    )
    require(
        len(syndrome_realizability["per_agreement"]) == 42,
        "syndrome realizability agreement count mismatch",
    )
    require(
        zero_slope_subtraction["schema_version"]
        == "f17-32-m3-zero-slope-subtraction-v1",
        "zero-slope subtraction schema mismatch",
    )
    require(
        zero_slope_subtraction["source_artifacts"]["fixed_top_window_packet"]["ref"]
        == TOP_PACKET_REF,
        "zero-slope subtraction top-packet ref mismatch",
    )
    require(
        zero_slope_subtraction["source_artifacts"]["line_value_lift"]["ref"]
        == LINE_VALUE_LIFT_REF,
        "zero-slope subtraction line-value ref mismatch",
    )
    require(
        zero_slope_subtraction["summary"][
            "deduped_aperiodic_numerator_after_removed_ledgers"
        ]
        == 0,
        "zero-slope subtraction residual numerator mismatch",
    )
    require(
        extension_denominator_audit["schema_version"]
        == "f17-32-m3-extension-denominator-audit-v1",
        "extension denominator audit schema mismatch",
    )
    require(
        extension_denominator_audit["source_artifacts"]["line_value_lift"]["ref"]
        == LINE_VALUE_LIFT_REF,
        "extension denominator audit line-value ref mismatch",
    )
    require(
        extension_denominator_audit["field_ledgers"][
            "finite_affine_slope_denominator"
        ]
        == 17**32,
        "extension denominator audit q_line mismatch",
    )
    require(
        extension_denominator_audit["line_value_classification"]["g"][
            "nonbase_values"
        ]
        == 512,
        "extension denominator audit did not classify g as extension-valued",
    )
    require(
        projective_endpoint_audit["schema_version"]
        == "f17-32-m3-projective-endpoint-audit-v1",
        "projective endpoint audit schema mismatch",
    )
    require(
        projective_endpoint_audit["source_artifacts"]["fixed_top_window_packet"][
            "ref"
        ]
        == TOP_PACKET_REF,
        "projective endpoint audit top-packet ref mismatch",
    )
    require(
        projective_endpoint_audit["summary"][
            "projective_infinity_contribution_before_removed_ledgers"
        ]
        == 0,
        "projective endpoint audit infinity contribution mismatch",
    )
    require(
        projective_endpoint_audit["summary"][
            "deduped_aperiodic_numerator_after_removed_ledgers"
        ]
        == 0,
        "projective endpoint audit residual numerator mismatch",
    )


def per_agreement_records(
    plan: dict[str, Any],
    generic: dict[str, Any],
    family: dict[str, Any],
    top_packet: dict[str, Any],
    syndrome_realizability: dict[str, Any],
    zero_slope_subtraction: dict[str, Any],
    projective_endpoint_audit: dict[str, Any],
) -> list[dict[str, Any]]:
    plan_by_a = {int(item["A"]): item for item in plan["per_agreement"]}
    generic_by_a = {int(item["A"]): item for item in generic["agreements"]}
    family_by_a = {int(item["A"]): item for item in family["agreements"]}
    realizability_by_a = {
        int(item["A"]): item for item in syndrome_realizability["per_agreement"]
    }
    top_by_a = top_window_by_agreement(top_packet)
    zero_subtraction_by_a = {
        int(item["A"]): item for item in zero_slope_subtraction["per_agreement"]
    }
    projective_by_a = {
        int(item["A"]): item for item in projective_endpoint_audit["per_agreement"]
    }
    records = []
    for agreement in range(AGREEMENT_MIN, AGREEMENT_MAX + 1):
        plan_item = plan_by_a[agreement]
        generic_item = generic_by_a[agreement]
        family_item = family_by_a[agreement]
        realizability_item = realizability_by_a[agreement]
        top_item = top_by_a.get(agreement)
        require(plan_item["degree_bound"] == generic_item["generic_degree"], f"A={agreement}: degree mismatch")
        require(
            family_item["synthetic_roots"] == ROOT_UNION,
            f"A={agreement}: synthetic roots mismatch",
        )
        require(
            realizability_item["visible_syndrome_length"] == 256
            and realizability_item["section_applies"] is True,
            f"A={agreement}: syndrome realizability mismatch",
        )
        if top_item is not None:
            require(
                top_item["extractor_audit"]["root_count"] == 1,
                f"A={agreement}: top-window root count mismatch",
            )
            zero_subtraction_item = zero_subtraction_by_a[agreement]
            require(
                zero_subtraction_item["B_ap_after_removed_ledgers"] == 0,
                f"A={agreement}: zero-slope residual mismatch",
            )
            require(
                zero_subtraction_item["overlap_regular_tangent_roots"] == ROOT_UNION,
                f"A={agreement}: zero-slope overlap mismatch",
            )
            projective_item = projective_by_a[agreement]
            require(
                projective_item["projective_infinity"]["contribution"] == 0,
                f"A={agreement}: projective endpoint contribution mismatch",
            )
            require(
                projective_item["top_degree"] == top_item["j"] + 1,
                f"A={agreement}: projective top degree mismatch",
            )
        else:
            zero_subtraction_item = None
            projective_item = None
        records.append(
            {
                "A": agreement,
                "j": plan_item["j"],
                "t": plan_item["t"],
                "minor_size": plan_item["minor_size"],
                "degree_bound": plan_item["degree_bound"],
                "generic_status": "all maximal row-set minors are generically nonzero",
                "generic_all_row_set_count": generic_item["all_row_set_atlas"]["count"],
                "synthetic_family_status": "closed-form u=0 prefix witness has exact root union {0}",
                "synthetic_root_union": ROOT_UNION,
                "syndrome_pencil_realizability": (
                    "all length-256 u,v syndrome pencils are realized by explicit "
                    "line values on H"
                ),
                "syndrome_realizability_certificate": SYNDROME_REALIZABILITY_REF,
                "fixed_top_window_v9_packet": TOP_PACKET_REF if top_item is not None else None,
                "fixed_top_window_line_value_lift": LINE_VALUE_LIFT_REF
                if top_item is not None
                else None,
                "fixed_top_window_zero_slope_subtraction": ZERO_SLOPE_SUBTRACTION_REF
                if top_item is not None
                else None,
                "fixed_top_window_extension_denominator_audit": EXTENSION_DENOMINATOR_AUDIT_REF
                if top_item is not None
                else None,
                "fixed_top_window_projective_endpoint_audit": PROJECTIVE_ENDPOINT_AUDIT_REF
                if top_item is not None
                else None,
                "fixed_top_window_degree": (
                    top_item["extractor_audit"]["degree_bound"] if top_item is not None else None
                ),
                "fixed_top_window_projective_infinity_contribution": (
                    projective_item["projective_infinity"]["contribution"]
                    if projective_item is not None
                    else None
                ),
                "fixed_top_window_aperiodic_after_tangent": (
                    zero_subtraction_item["B_ap_after_removed_ledgers"]
                    if zero_subtraction_item is not None
                    else None
                ),
                "actual_row_outcome": (
                    "line-value lift and zero-slope tangent subtraction supplied "
                    "for the fixed synthetic packet; "
                    "universal tangent/quotient-deduped row outcome not supplied"
                    if top_item is not None
                    else "row-realizability discharged; universal row outcome not supplied"
                ),
                "next_required": (
                    "classify arbitrary length-256 F_17^32 syndrome pencils after "
                    "tangent/quotient/extension ledgers: compute a nonzero regular "
                    "minor root table or declare the first singular bucket"
                ),
            }
        )
    return records


def build_status() -> dict[str, Any]:
    plan = load_json(PLAN_REF)
    generic = load_json(GENERIC_REF)
    family = load_json(FAMILY_REF)
    top_packet = load_json(TOP_PACKET_REF)
    line_value_lift = load_json(LINE_VALUE_LIFT_REF)
    subgroup_section = load_json(SUBGROUP_SECTION_REF)
    syndrome_realizability = load_json(SYNDROME_REALIZABILITY_REF)
    zero_slope_subtraction = load_json(ZERO_SLOPE_SUBTRACTION_REF)
    extension_denominator_audit = load_json(EXTENSION_DENOMINATOR_AUDIT_REF)
    projective_endpoint_audit = load_json(PROJECTIVE_ENDPOINT_AUDIT_REF)
    validate_inputs(
        plan,
        generic,
        family,
        top_packet,
        line_value_lift,
        subgroup_section,
        syndrome_realizability,
        zero_slope_subtraction,
        extension_denominator_audit,
        projective_endpoint_audit,
    )
    records = per_agreement_records(
        plan,
        generic,
        family,
        top_packet,
        syndrome_realizability,
        zero_slope_subtraction,
        projective_endpoint_audit,
    )
    artifacts = [
        artifact_record("regular_window_plan", PLAN_REF, "regular-hankel-window-plan-v1"),
        artifact_record(
            "generic_all_row_set_regular_minor",
            GENERIC_REF,
            "f17-32-m3-generic-all-row-set-regular-minor-v1",
        ),
        artifact_record(
            "synthetic_rank_witness_family",
            FAMILY_REF,
            "f17-32-m3-rank-witness-family-v1",
        ),
        artifact_record("fixed_top_window_v9_packet", TOP_PACKET_REF, "aperiodic-hankel-eliminant-v1"),
        artifact_record(
            "fixed_top_window_line_value_lift",
            LINE_VALUE_LIFT_REF,
            "f17-32-m3-line-value-lift-v1",
        ),
        artifact_record(
            "subgroup_syndrome_section",
            SUBGROUP_SECTION_REF,
            "subgroup-syndrome-section-v1",
        ),
        artifact_record(
            "m3_syndrome_realizability",
            SYNDROME_REALIZABILITY_REF,
            "f17-32-m3-syndrome-realizability-v1",
        ),
        artifact_record(
            "fixed_top_window_zero_slope_subtraction",
            ZERO_SLOPE_SUBTRACTION_REF,
            "f17-32-m3-zero-slope-subtraction-v1",
        ),
        artifact_record(
            "fixed_top_window_extension_denominator_audit",
            EXTENSION_DENOMINATOR_AUDIT_REF,
            "f17-32-m3-extension-denominator-audit-v1",
        ),
        artifact_record(
            "fixed_top_window_projective_endpoint_audit",
            PROJECTIVE_ENDPOINT_AUDIT_REF,
            "f17-32-m3-projective-endpoint-audit-v1",
        ),
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "AUDIT",
        "row": plan["row"],
        "summary": {
            "regular_window": {"A_min": AGREEMENT_MIN, "A_max": AGREEMENT_MAX},
            "agreements": len(records),
            "degree_bound_sum": sum(record["degree_bound"] for record in records),
            "finite_slope_budget_numerator": plan["budget_context"]["budget_numerator"],
            "generic_regular_minors_status": "proved generically nonzero for every row-set chart",
            "synthetic_family_status": "proved closed-form root union {0} for all 42 synthetic pencils",
            "fixed_top_window_status": "one v9 packet covers A=421..426 with root union {0}",
            "fixed_top_window_line_value_status": "explicit f,g line values replay the fixed top-window syndrome input",
            "subgroup_syndrome_section_status": "proved explicit inverse-Fourier section for subgroup syndrome vectors",
            "syndrome_pencil_realizability_status": "all length-256 u,v pencils in the M3 window are realized by explicit line values on H",
            "fixed_top_window_subtraction_status": "the synthetic root {0} is removed by the zero-codeword tangent slope, leaving aperiodic numerator 0",
            "fixed_top_window_denominator_status": "the line-value lift is genuinely F_17^32-valued, so the finite-affine slope denominator is 17^32",
            "fixed_top_window_projective_endpoint_status": "the projective endpoint [0:1] is empty for A=421..426, so projectivizing the fixed synthetic packet adds no regular-minor root",
            "actual_row_status": "row-realizability is discharged; universal tangent/quotient-deduped row outcomes are not supplied",
            "first_actual_row_task": "classify arbitrary length-256 syndrome pencils by root table or singular-bucket outcome for A=385..426",
        },
        "artifacts": artifacts,
        "per_agreement": records,
        "claim_boundaries": {
            "proved": [
                "the v9 regular window is exactly 385 <= A <= 426",
                "every maximal row-set regular minor is generically nonzero",
                "the synthetic u=0 family has exact root union {0}",
                "the fixed synthetic top-window packet is v9-checkable for A=421..426",
                "the fixed top-window syndrome input has an explicit line-value lift",
                "subgroup syndrome vectors have an explicit inverse-Fourier line-value section",
                "every length-256 syndrome pencil in the M3 regular window is realized by explicit line values on the pinned subgroup row",
                "the fixed synthetic top-window root {0} is the zero-codeword tangent slope and leaves no synthetic residual aperiodic roots after subtraction",
                "the fixed top-window line-value lift is extension-valued and must use q_line=17^32 for finite-affine slope accounting",
                "the fixed top-window projective endpoint [0:1] is empty and contributes no extra synthetic regular-minor root",
            ],
            "not_proved": [
                "a universal root table for arbitrary length-256 syndrome pencils at any A in 385..426",
                "a tangent/quotient-deduped safe-side upper bound for the whole row in this window",
                "a Prime192 quotient/tangent subtraction or denominator table",
                "the first universal singular bucket classification",
            ],
        },
        "nonclaims": [
            "not a worst-case MCA bound",
            "not a universal M3 row outcome",
            "not a full quotient/tangent subtraction table",
            "not a singular-pivot packet",
        ],
    }


def check_status(path: Path) -> None:
    expected = render(build_status())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"regular-window status mismatch: {path}")


def print_summary(status: dict[str, Any]) -> None:
    summary = status["summary"]
    print("F_17^32 M3 regular-window status")
    print(
        "window: A={A_min}..{A_max}, agreements={agreements}, degree_sum={degree_bound_sum}".format(
            agreements=summary["agreements"],
            degree_bound_sum=summary["degree_bound_sum"],
            **summary["regular_window"],
        )
    )
    print(f"generic: {summary['generic_regular_minors_status']}")
    print(f"synthetic: {summary['synthetic_family_status']}")
    print(f"actual row: {summary['actual_row_status']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic status JSON")
    parser.add_argument("--check", type=Path, help="check deterministic status JSON")
    parser.add_argument("--json", action="store_true", help="print status JSON")
    args = parser.parse_args()

    status = build_status()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(status), encoding="utf-8")
    if args.check:
        check_status(args.check)
    if args.json:
        print(render(status), end="")
        return
    print_summary(status)


if __name__ == "__main__":
    main()
