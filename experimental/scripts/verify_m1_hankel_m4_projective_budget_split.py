#!/usr/bin/env python3
"""Verify the M4 finite/projective direction-rank budget split."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import (  # noqa: E402
    Field,
    K,
    MODULUS,
    N,
    P,
)


SCHEMA_VERSION = "f17-32-m3-m4-projective-budget-split-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_BUDGET = (Q_LINE + 1) // 2**TARGET_BITS
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
DIRECTION_RANK_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-direction-rank-degree-cap/"
    "f17_32_n512_k256_m3_direction_rank_degree_cap.json"
)
PROJECTIVE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/"
    "f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json"
)


def load_json(ref: str | Path) -> dict[str, Any]:
    path = ref if isinstance(ref, Path) else ROOT / ref
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(ref: str) -> str:
    return sha256((ROOT / ref).read_bytes()).hexdigest()


def hash_value(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    size = j_value + 1
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "minor_size": size,
        "maximal_row_set_count": comb(t_value, size),
        "finite_budget": FINITE_BUDGET,
        "projective_budget": PROJECTIVE_BUDGET,
        "finite_safe_direction_rank_max": FINITE_BUDGET,
        "projective_safe_without_endpoint_payment_rank_max": PROJECTIVE_BUDGET - 1,
        "endpoint_sensitive_direction_rank": PROJECTIVE_BUDGET,
    }


def budget_decision_table() -> dict[str, Any]:
    return {
        "input_theorems": {
            "finite_direction_rank_degree_cap": {
                "certificate_ref": DIRECTION_RANK_REF,
                "statement": (
                    "In a nonsingular regular bucket, if r=rank H_{t,j}(v), "
                    "then the canonical finite regular root count is at most r."
                ),
            },
            "projective_infinity_kernel_chart": {
                "certificate_ref": PROJECTIVE_KERNEL_REF,
                "statement": (
                    "The projective endpoint [0:1] is empty under kernel "
                    "containment and otherwise contributes at most one "
                    "projective parameter."
                ),
            },
        },
        "combined_bound": {
            "hypothesis": "nonsingular regular bucket after tangent/common-code-line finite overlap removal",
            "direction_rank": "r = rank H_{t,j}(v)",
            "endpoint_indicator": (
                "e_infty=0 if the infinity chart is empty or paid; "
                "e_infty<=1 always by the M5 projective kernel chart"
            ),
            "finite_affine_numerator_bound": "B_ap_regular_finite <= r",
            "projective_numerator_bound": "B_ap_regular_projective <= r + e_infty",
        },
        "rank_cutoffs_for_f17_32_row": {
            "finite_safe": {
                "condition": f"r <= {FINITE_BUDGET}",
                "upper_bound": FINITE_BUDGET,
                "safe_against_finite_sampler": True,
            },
            "projective_safe_without_endpoint_payment": {
                "condition": f"r <= {PROJECTIVE_BUDGET - 1}",
                "upper_bound": f"r + 1 <= {PROJECTIVE_BUDGET}",
                "safe_against_projective_sampler": True,
            },
            "endpoint_sensitive": {
                "condition": f"r = {PROJECTIVE_BUDGET}",
                "finite_upper_bound": PROJECTIVE_BUDGET,
                "projective_upper_bound_before_endpoint_payment": PROJECTIVE_BUDGET + 1,
                "safe_if": (
                    "the endpoint is empty/paid or the exact finite root table "
                    f"has at most {PROJECTIVE_BUDGET - 1} surviving roots"
                ),
            },
            "root_table_needed": {
                "condition": f"r > {PROJECTIVE_BUDGET}",
                "reason": "the rank cap alone exceeds the 2^-128 numerator budget",
            },
        },
    }


def check_dependency_windows(direction: dict[str, Any], projective: dict[str, Any]) -> None:
    require(
        direction["schema_version"] == "f17-32-m3-direction-rank-degree-cap-v1",
        "unexpected direction-rank schema",
    )
    require(
        projective["schema_version"] == "f17-32-m3-m5-projective-infinity-kernel-chart-v1",
        "unexpected projective-kernel schema",
    )
    for name, data in [("direction", direction), ("projective", projective)]:
        require(data["window"]["A_min"] == A_MIN, f"{name} A_min mismatch")
        require(data["window"]["A_max"] == A_MAX, f"{name} A_max mismatch")


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    direction = load_json(DIRECTION_RANK_REF)
    projective = load_json(PROJECTIVE_KERNEL_REF)
    check_dependency_windows(direction, projective)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "syndrome length mismatch")
    require(FINITE_BUDGET == 6, "unexpected finite budget")
    require(PROJECTIVE_BUDGET == 6, "unexpected projective budget")

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    total_row_sets = sum(record["maximal_row_set_count"] for record in records)
    require(total_row_sets == direction["window"]["all_row_set_total"], "direction total mismatch")
    require(total_row_sets == projective["window"]["all_row_set_total"], "projective total mismatch")
    require(
        all(record["minor_size"] > PROJECTIVE_BUDGET for record in records),
        "M3 regular window should have minor size above budget",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "M4 finite/projective direction-rank budget split for the F_17^32 M3 window",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
            "finite_affine_denominator": Q_LINE,
            "projective_denominator": Q_LINE + 1,
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "direction_rank_degree_cap": {
                "ref": DIRECTION_RANK_REF,
                "sha256": sha256_file(DIRECTION_RANK_REF),
            },
            "projective_infinity_kernel_chart": {
                "ref": PROJECTIVE_KERNEL_REF,
                "sha256": sha256_file(PROJECTIVE_KERNEL_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "all_row_set_total": total_row_sets,
        },
        "theorem": {
            "statement": (
                "For any nonsingular M3 regular bucket, let "
                "r=rank H_{t,j}(v).  After finite tangent/common-code-line "
                "overlap is removed, the finite affine regular contribution is "
                "at most r.  For the projective sampler, the same bucket "
                "contributes at most r+e_infty, where e_infty is 0 if the "
                "projective-infinity chart is empty or paid and is always at "
                "most 1 by the M5 projective kernel chart."
            ),
            "proof_skeleton": [
                "The direction-rank degree cap bounds the canonical finite regular root table by r.",
                "The M5 projective-infinity kernel chart separates the single endpoint [0:1] from finite affine roots.",
                "That endpoint is empty under kernel containment and otherwise has projective parameter degree 1.",
                "Therefore projective counting adds at most one parameter to the finite rank cap.",
                "For q_line=17^32, both finite and projective 2^-128 budgets equal 6, so r<=5 is projective-safe without endpoint payment, while r=6 is endpoint-sensitive.",
            ],
        },
        "budget_decision_table": budget_decision_table(),
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
            "finite_safe_direction_rank_max": FINITE_BUDGET,
            "projective_safe_without_endpoint_payment_rank_max": PROJECTIVE_BUDGET - 1,
            "endpoint_sensitive_direction_rank": PROJECTIVE_BUDGET,
            "all_minor_sizes_exceed_budget": True,
            "dependencies_checked": 2,
        },
        "checks": [
            "finite and projective 2^-128 budgets both equal 6",
            "dependency windows are both 385..426",
            "dependency row-set totals agree with this certificate",
            "the projective endpoint is counted separately from finite affine roots",
            "rank<=5 is projective-safe without quotient or endpoint subtraction",
            "rank=6 is finite-safe but projective endpoint-sensitive",
        ],
        "nonclaims": [
            "does not compute exact finite root tables for rank>6",
            "does not prove the endpoint is paid in the rank=6 case",
            "does not classify singular all-minor-zero buckets",
            "does not claim a worst-case support-wise MCA row bound",
            "does not duplicate synthetic low-rank quotient-image packets",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"M4 projective budget split certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3/M4 projective budget split")
    print(
        "A={A_min}..{A_max}, agreements={agreement_count}, row sets={all_row_set_total}".format(
            **window
        )
    )
    print("finite budget={finite_budget}, projective budget={projective_budget}".format(**summary))
    print(
        "finite-safe r<={finite_safe_direction_rank_max}; "
        "projective-safe without endpoint payment r<={projective_safe_without_endpoint_payment_rank_max}; "
        "endpoint-sensitive r={endpoint_sensitive_direction_rank}".format(**summary)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()

    certificate = build_certificate()
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        check_certificate(args.check)
    print_summary(certificate)


if __name__ == "__main__":
    main()
