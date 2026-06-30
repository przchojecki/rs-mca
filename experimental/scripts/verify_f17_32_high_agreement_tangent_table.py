#!/usr/bin/env python3
"""Verify the F_17^32 high-agreement tangent subtraction table."""

from __future__ import annotations

import argparse
import json
from hashlib import sha256
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "f17-32-high-agreement-tangent-table-v1"
N = 512
K = 256
Q_LINE = 17**32
TARGET_BITS = 128

HIGH_AGREEMENT_REF = (
    "experimental/data/certificates/high-agreement-threshold-package/"
    "f17_512_high_agreement_threshold_certificate.json"
)
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
SMOKE_NUMERATOR_TABLE_REF = (
    "experimental/data/certificates/hankel-smoke-f17-506-507/"
    "f17_32_n512_k256_a506_507_numerator_table.json"
)
OUTPUT_PATH = ROOT / (
    "experimental/data/certificates/hankel-f17-32-high-agreement-tangent-table/"
    "f17_32_n512_k256_a427_512_high_agreement_tangent_table.json"
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


def verdict(total: int, budget: int) -> str:
    if total <= budget:
        return "SAFE_BY_PROVED_UPPER_BOUND"
    return "UNSAFE_BY_PROVED_LOWER_BOUND"


def comparison(total: int, budget: int) -> str:
    relation = "<=" if total <= budget else ">"
    return f"{total} {relation} {budget}"


def row_record(agreement: int, budget: int) -> dict[str, Any]:
    r = N - agreement
    tangent = r + 1
    return {
        "A": agreement,
        "j": r,
        "t": agreement - K,
        "r": r,
        "B_tan": tangent,
        "B_quot_support": 0,
        "B_quot_image": 0,
        "B_ap_regular": 0,
        "B_ap_pivot": 0,
        "B_ext": 0,
        "deduped_total_upper_bound": tangent,
        "known_lower_bound": tangent,
        "aperiodic_after_removed_ledgers": 0,
        "denominator": Q_LINE,
        "budget": budget,
        "comparison_to_budget": comparison(tangent, budget),
        "verdict": verdict(tangent, budget),
    }


def validate_inputs(
    high_agreement: dict[str, Any],
    row_descriptor: dict[str, Any],
    smoke_table: dict[str, Any],
) -> tuple[int, int, int]:
    row = row_descriptor["row"]
    require(row["n"] == N, "row descriptor n mismatch")
    require(row["k"] == K, "row descriptor k mismatch")
    require(row["field"] == "F_17^32", "row descriptor field mismatch")
    require(row["field_order"] == Q_LINE, "row descriptor field order mismatch")
    require(
        row_descriptor["m3_regular_window"]["tangent_exact_start"] == 427,
        "row descriptor tangent start mismatch",
    )

    affine = high_agreement["f17_512_affine"]
    require(affine["applies"] is True, "high-agreement certificate does not apply")
    require(affine["threshold_pinned"] is True, "threshold is not pinned")
    require(affine["budget"] == Q_LINE // 2**TARGET_BITS, "budget mismatch")
    require(affine["line_exact_radius"] == (N - K) // 3, "exact radius mismatch")
    require(affine["exact_range_min_agreement"] == N - affine["line_exact_radius"], "exact range start mismatch")
    require(affine["first_safe_agreement"] == 507, "first safe agreement mismatch")
    require(affine["last_unsafe_agreement"] == 506, "last unsafe agreement mismatch")
    require(affine["safe_line_numerator"] == 6, "safe numerator mismatch")
    require(affine["unsafe_line_numerator"] == 7, "unsafe numerator mismatch")

    smoke_rows = {int(row["A"]): row for row in smoke_table["rows"]}
    for agreement in (506, 507):
        require(agreement in smoke_rows, f"smoke table missing A={agreement}")
        expected = row_record(agreement, affine["budget"])
        require(
            smoke_rows[agreement]["tangent_numerator"] == expected["B_tan"],
            f"smoke tangent mismatch at A={agreement}",
        )
        require(
            smoke_rows[agreement]["aperiodic_after_removed_ledgers"] == 0,
            f"smoke residual mismatch at A={agreement}",
        )
        require(
            smoke_rows[agreement]["denominator"] == Q_LINE,
            f"smoke denominator mismatch at A={agreement}",
        )

    return (
        affine["exact_range_min_agreement"],
        N,
        affine["budget"],
    )


def build_certificate() -> dict[str, Any]:
    high_agreement = load_json(HIGH_AGREEMENT_REF)
    row_descriptor = load_json(ROW_DESCRIPTOR_REF)
    smoke_table = load_json(SMOKE_NUMERATOR_TABLE_REF)
    start, end, budget = validate_inputs(high_agreement, row_descriptor, smoke_table)
    rows = [row_record(agreement, budget) for agreement in range(start, end + 1)]
    safe_rows = [row for row in rows if row["verdict"] == "SAFE_BY_PROVED_UPPER_BOUND"]
    unsafe_rows = [
        row for row in rows if row["verdict"] == "UNSAFE_BY_PROVED_LOWER_BOUND"
    ]
    require(len(rows) == 86, "high-agreement row count mismatch")
    require(safe_rows[0]["A"] == 507 and safe_rows[-1]["A"] == 512, "safe interval mismatch")
    require(unsafe_rows[0]["A"] == 427 and unsafe_rows[-1]["A"] == 506, "unsafe interval mismatch")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "finite-slope support-wise MCA / LD_sw",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": row_descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
        },
        "source_artifacts": {
            "high_agreement_threshold_package": {
                "ref": HIGH_AGREEMENT_REF,
                "sha256": sha256_file(HIGH_AGREEMENT_REF),
            },
            "row_descriptor": {
                "ref": ROW_DESCRIPTOR_REF,
                "sha256": sha256_file(ROW_DESCRIPTOR_REF),
            },
            "hankel_smoke_numerator_table": {
                "ref": SMOKE_NUMERATOR_TABLE_REF,
                "sha256": sha256_file(SMOKE_NUMERATOR_TABLE_REF),
            },
        },
        "theorem_input": {
            "name": "high-agreement tangent line staircase",
            "formula": "LD_sw(C,A)=n-A+1 when n-A <= floor((n-k)/3)",
            "exact_range": {"A_min": start, "A_max": end},
            "removed_ledger": "tangent/common-code-line",
            "residual_after_tangent_removal": 0,
        },
        "target": {
            "epsilon": "2^-128",
            "budget_formula": "floor(q_line / 2^128)",
            "budget": budget,
            "budget_bracket": "6*2^128 < 17^32 < 7*2^128",
        },
        "summary": {
            "rows": len(rows),
            "unsafe_agreement_range": {"A_min": 427, "A_max": 506},
            "safe_agreement_range": {"A_min": 507, "A_max": 512},
            "largest_safe_integer_radius": 5,
            "first_unsafe_integer_radius": 6,
            "real_safe_interval": "[0, 6/512)",
            "aperiodic_after_removed_ledgers": 0,
            "quotient_after_removed_ledgers": 0,
            "extension_after_removed_ledgers": 0,
        },
        "rows": rows,
        "nonclaims": [
            "does not cover the lower-agreement range A < 427",
            "does not prove the M3 regular-window safe side",
            "does not provide singular-pivot packets",
            "does not replace the aperiodic local-limit problem",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"high-agreement tangent table mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    target = certificate["target"]
    print("F_17^32 high-agreement tangent table")
    print(
        "range: A={A_min}..{A_max}, rows={rows}".format(
            rows=summary["rows"], **certificate["theorem_input"]["exact_range"]
        )
    )
    print(f"budget: {target['budget']} ({target['budget_formula']})")
    print(
        "safe: A={A_min}..{A_max}; unsafe: A={U_min}..{U_max}".format(
            A_min=summary["safe_agreement_range"]["A_min"],
            A_max=summary["safe_agreement_range"]["A_max"],
            U_min=summary["unsafe_agreement_range"]["A_min"],
            U_max=summary["unsafe_agreement_range"]["A_max"],
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path, help="write deterministic table JSON")
    parser.add_argument("--check", type=Path, help="check deterministic table JSON")
    parser.add_argument("--json", action="store_true", help="print table JSON")
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
