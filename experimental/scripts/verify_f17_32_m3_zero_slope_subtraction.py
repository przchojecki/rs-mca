#!/usr/bin/env python3
"""Verify the F_17^32 M3 zero-slope subtraction sidecar.

This is a deliberately narrow M4-style ledger.  It does not turn the
synthetic top-window packet into an actual-row MCA bound.  It only checks that
the packet's sole regular-minor root is the finite slope 0, and that the
line-value lift has f=0, so this root is paid by the zero-codeword
tangent/common-code-line branch.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-m3-zero-slope-subtraction-v1"
TOP_WINDOW_MIN = 421
TOP_WINDOW_MAX = 426
ROOT_UNION = [0]

TOP_PACKET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-fixed-top-window/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_packet.json"
)
LINE_VALUE_LIFT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-line-value-lift/"
    "f17_32_n512_k256_a421_426_fixed_prefix92_line_values.json"
)
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-m3-zero-slope-subtraction/"
    "f17_32_n512_k256_a421_426_zero_slope_subtraction.json"
)
SCHEMA_CHECKER = ROOT / "scripts/check_aperiodic_eliminant_packet.py"
SCHEMA = ROOT / "scripts/aperiodic_eliminant_schema.json"


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


def load_schema_checker():
    spec = importlib.util.spec_from_file_location(
        "check_aperiodic_eliminant_packet", SCHEMA_CHECKER
    )
    require(spec is not None and spec.loader is not None, "could not load schema checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_source_packet(packet: dict[str, Any]) -> None:
    checker = load_schema_checker()
    checker.check_path(ROOT / TOP_PACKET_REF, SCHEMA)

    require(packet["row"]["n"] == 512, "top packet n mismatch")
    require(packet["row"]["k"] == 256, "top packet k mismatch")
    require(packet["row"]["field"] == "F_17^32", "top packet field mismatch")
    require(packet["agreement_threshold"] == TOP_WINDOW_MIN, "top packet threshold mismatch")
    require(packet["declared_aperiodic_numerator"] == 1, "top packet numerator mismatch")
    require(packet["root_union"] == ROOT_UNION, "top packet root union mismatch")
    agreements = [int(item["A"]) for item in packet["exact_agreements"]]
    require(agreements == list(range(TOP_WINDOW_MIN, TOP_WINDOW_MAX + 1)), "top packet A range mismatch")
    for item in packet["exact_agreements"]:
        require(item["status"] == "regular_minor", f"A={item['A']}: expected regular_minor")
        require(
            item["regular_minor_data"]["roots"] == ROOT_UNION,
            f"A={item['A']}: regular root mismatch",
        )
        require(
            item["extractor_audit"]["root_count"] == 1,
            f"A={item['A']}: root_count mismatch",
        )


def check_line_value_lift(line_value_lift: dict[str, Any]) -> None:
    require(
        line_value_lift["schema_version"] == "f17-32-m3-line-value-lift-v1",
        "line-value lift schema mismatch",
    )
    require(
        line_value_lift["source_packet"]["fixed_top_window_packet_ref"] == TOP_PACKET_REF,
        "line-value lift packet ref mismatch",
    )
    require(
        line_value_lift["syndrome_replay"]["matches_fixed_top_window_input"] is True,
        "line-value lift does not replay source input",
    )
    f_values = line_value_lift["line_values"]["f"]
    require(len(f_values) == 512, "line-value lift f length mismatch")
    require(all(value == 0 for value in f_values), "line-value lift f is not identically zero")


def per_agreement_records(packet: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    for item in packet["exact_agreements"]:
        regular_roots = item["regular_minor_data"]["roots"]
        tangent_roots = [0]
        residual_roots = sorted(set(regular_roots) - set(tangent_roots))
        overlap_roots = sorted(set(regular_roots) & set(tangent_roots))
        require(regular_roots == ROOT_UNION, f"A={item['A']}: unexpected regular roots")
        require(overlap_roots == ROOT_UNION, f"A={item['A']}: zero slope not removed")
        require(residual_roots == [], f"A={item['A']}: residual roots remain")
        records.append(
            {
                "A": item["A"],
                "j": item["j"],
                "t": item["t"],
                "regular_minor_root_union_before_removed_ledgers": regular_roots,
                "B_ap_regular_before_removed_ledgers": len(regular_roots),
                "B_tan_common_code_line": len(tangent_roots),
                "B_quot_support": 0,
                "B_quot_image": 0,
                "B_ext": 0,
                "overlap_regular_tangent_roots": overlap_roots,
                "aperiodic_root_union_after_removed_ledgers": residual_roots,
                "B_ap_after_removed_ledgers": len(residual_roots),
                "deduped_total_upper_for_synthetic_packet": len(tangent_roots)
                + len(residual_roots),
                "claim_status": "synthetic_packet_only",
            }
        )
    return records


def build_certificate() -> dict[str, Any]:
    packet = load_json(TOP_PACKET_REF)
    line_value_lift = load_json(LINE_VALUE_LIFT_REF)
    check_source_packet(packet)
    check_line_value_lift(line_value_lift)
    records = per_agreement_records(packet)
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "AUDIT",
        "row": packet["row"],
        "scope": {
            "agreement_range": {"A_min": TOP_WINDOW_MIN, "A_max": TOP_WINDOW_MAX},
            "packet_type": "synthetic fixed top-window v9 packet",
            "sampler": packet["sampler"],
        },
        "source_artifacts": {
            "fixed_top_window_packet": {
                "ref": TOP_PACKET_REF,
                "sha256": sha256_file(TOP_PACKET_REF),
                "schema_version": packet["schema_version"],
                "declared_aperiodic_numerator_before_subtraction": packet[
                    "declared_aperiodic_numerator"
                ],
            },
            "line_value_lift": {
                "ref": LINE_VALUE_LIFT_REF,
                "sha256": sha256_file(LINE_VALUE_LIFT_REF),
                "schema_version": line_value_lift["schema_version"],
            },
        },
        "subtraction_rule": {
            "name": "zero_codeword_tangent_slope",
            "finite_slope": 0,
            "reason": (
                "The line-value lift has f(x)=0 for every x in H.  At finite "
                "slope z=0, the line word f+z g is therefore the zero "
                "Reed-Solomon codeword, so the root z=0 is paid by the "
                "tangent/common-code-line ledger."
            ),
            "removed_tangent_roots": ROOT_UNION,
            "removed_quotient_support_roots": [],
            "removed_quotient_image_roots": [],
            "removed_extension_roots": [],
        },
        "summary": {
            "agreements": len(records),
            "regular_root_union_before_removed_ledgers": ROOT_UNION,
            "tangent_root_union_removed": ROOT_UNION,
            "aperiodic_root_union_after_removed_ledgers": [],
            "raw_regular_numerator": 1,
            "tangent_numerator_removed": 1,
            "deduped_aperiodic_numerator_after_removed_ledgers": 0,
            "actual_row_status": "not supplied",
            "next_required": (
                "Repeat this subtraction discipline for actual F_17^32 row "
                "pencils and for quotient-image roots before claiming an M4 "
                "row table."
            ),
        },
        "per_agreement": records,
        "nonclaims": [
            "not a worst-case MCA bound",
            "not actual M3 row data",
            "not a Prime192 subtraction table",
            "not a singular-pivot packet",
            "does not prove quotient/tangent subtraction for arbitrary row pencils",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"zero-slope subtraction certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    window = certificate["scope"]["agreement_range"]
    print("F_17^32 M3 zero-slope subtraction")
    print(f"window: A={window['A_min']}..{window['A_max']}")
    print(
        "roots: regular={regular_root_union_before_removed_ledgers} "
        "removed_tangent={tangent_root_union_removed} "
        "residual={aperiodic_root_union_after_removed_ledgers}".format(**summary)
    )
    print(
        "numerator: raw={raw_regular_numerator}, tangent_removed={tangent_numerator_removed}, "
        "aperiodic_after_removed={deduped_aperiodic_numerator_after_removed_ledgers}".format(
            **summary
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic certificate JSON")
    parser.add_argument("--check", type=Path, help="check deterministic certificate JSON")
    parser.add_argument("--json", action="store_true", help="print certificate JSON")
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
