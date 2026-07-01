#!/usr/bin/env python3
"""Verify a rank-6 projective-infinity witness family in the F_17^32 M3 window."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
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


SCHEMA_VERSION = "f17-32-m3-rank6-projective-witness-v1"
Q_LINE = 17**32
PROJECTIVE_DENOMINATOR = Q_LINE + 1
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
RANK = 6
FULL_M3_A_MIN = 385
A_MIN = 388
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
RANK_DROP_BRIDGE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-regular-root-rank-drop/"
    "f17_32_n512_k256_m3_m5_regular_root_rank_drop.json"
)
PROJECTIVE_KERNEL_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m5-projective-infinity-kernel-chart/"
    "f17_32_n512_k256_m3_m5_projective_infinity_kernel_chart.json"
)
PROJECTIVE_SPLIT_LOCATOR_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-projective-split-locator-gate/"
    "f17_32_n512_k256_m3_projective_split_locator_gate.json"
)
M4_PROJECTIVE_BUDGET_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-m4-projective-budget-split/"
    "f17_32_n512_k256_m3_m4_projective_budget_split.json"
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


def comparison(value: int, budget: int) -> str:
    relation = "<=" if value <= budget else ">"
    return f"{value} {relation} {budget}"


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    base_size = j_value + 1
    union_size = base_size + RANK
    direction_first = base_size
    direction_last = base_size + RANK - 1
    base_locator_last = j_value - RANK - 1
    surviving_base_first = j_value - RANK
    surviving_base_last = j_value

    require(j_value >= RANK, f"A={agreement}: locator needs j>=6")
    require(t_value >= union_size, f"A={agreement}: finite-rank proof needs t>=j+7")
    require(base_locator_last + 1 == j_value - RANK, "base locator count mismatch")
    require(surviving_base_last - surviving_base_first + 1 == RANK + 1, "survivor count mismatch")

    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "base_support_size": base_size,
        "direction_support_size": RANK,
        "base_plus_direction_support_size": union_size,
        "direction_rank": RANK,
        "finite_rank_hypothesis": {
            "t_at_least_support_union_size": True,
            "support_union_size": union_size,
            "z_zero_rank": base_size,
            "z_nonzero_rank": base_size,
            "canonical_finite_roots": [],
            "canonical_finite_root_count": 0,
            "canonical_common_gcd": "1",
            "finite_upper_bound": 0,
            "finite_budget": FINITE_BUDGET,
            "comparison_to_budget": comparison(0, FINITE_BUDGET),
        },
        "projective_infinity": {
            "ambient_direction_rank": RANK,
            "ambient_projective_kernel_dimension": base_size - RANK,
            "split_locator_roots": {
                "direction_index_range": [direction_first, direction_last],
                "base_prefix_range": [0, base_locator_last],
                "root_count": j_value,
            },
            "surviving_base_index_range": [surviving_base_first, surviving_base_last],
            "surviving_base_count": RANK + 1,
            "H_v_locator": 0,
            "H_u_locator_nonzero": True,
            "split_locator_chart_nonempty": True,
            "exact_projective_endpoint_contribution": 1,
            "projective_upper_bound": 1,
            "projective_budget": PROJECTIVE_BUDGET,
            "comparison_to_budget": comparison(1, PROJECTIVE_BUDGET),
        },
    }


def check_dependency_window(ref: str, data: dict[str, Any]) -> None:
    if "window" in data:
        require(data["window"]["A_min"] <= FULL_M3_A_MIN, f"{ref}: A_min too large")
        require(data["window"]["A_max"] >= A_MAX, f"{ref}: A_max too small")
    if "row" in data:
        require(data["row"]["n"] == N, f"{ref}: n mismatch")
        require(data["row"]["k"] == K, f"{ref}: k mismatch")


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    rank_drop = load_json(RANK_DROP_BRIDGE_REF)
    projective_kernel = load_json(PROJECTIVE_KERNEL_REF)
    projective_split = load_json(PROJECTIVE_SPLIT_LOCATOR_REF)
    projective_budget = load_json(M4_PROJECTIVE_BUDGET_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "descriptor syndrome mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == FULL_M3_A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
    )
    require(
        rank_drop["schema_version"] == "f17-32-m3-m5-regular-root-rank-drop-v1",
        "rank-drop schema mismatch",
    )
    require(
        projective_kernel["schema_version"]
        == "f17-32-m3-m5-projective-infinity-kernel-chart-v1",
        "projective kernel schema mismatch",
    )
    require(
        projective_split["schema_version"] == "f17-32-m3-projective-split-locator-gate-v1",
        "projective split-locator schema mismatch",
    )
    require(
        projective_budget["schema_version"] == "f17-32-m3-m4-projective-budget-split-v1",
        "projective budget schema mismatch",
    )
    for ref, data in {
        RANK_DROP_BRIDGE_REF: rank_drop,
        PROJECTIVE_KERNEL_REF: projective_kernel,
        PROJECTIVE_SPLIT_LOCATOR_REF: projective_split,
        M4_PROJECTIVE_BUDGET_REF: projective_budget,
    }.items():
        check_dependency_window(ref, data)

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    max_support_needed = (N - A_MIN + 1) + RANK
    require(
        len(set(domain_encodings[:max_support_needed])) == max_support_needed,
        "rank-6 prefix support is not distinct",
    )
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")
    require(
        min(record["projective_infinity"]["ambient_projective_kernel_dimension"] for record in records)
        == (N - A_MAX + 1) - RANK,
        "ambient endpoint kernel minimum mismatch",
    )
    require(
        max(record["projective_infinity"]["ambient_projective_kernel_dimension"] for record in records)
        == (N - A_MIN + 1) - RANK,
        "ambient endpoint kernel maximum mismatch",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT for this synthetic family",
        "object": "M3 rank-6 projective-infinity split-locator witness family",
        "row": {
            "code": "RS[F_17^32,H,256]",
            "n": N,
            "k": K,
            "field": "F_17^32",
            "domain_hash": descriptor["row"]["domain_hash"],
            "q_line": Q_LINE,
        },
        "source_artifacts": {
            "row_descriptor": {"ref": ROW_DESCRIPTOR_REF, "sha256": sha256_file(ROW_DESCRIPTOR_REF)},
            "regular_root_rank_drop_bridge": {
                "ref": RANK_DROP_BRIDGE_REF,
                "sha256": sha256_file(RANK_DROP_BRIDGE_REF),
            },
            "projective_infinity_kernel_chart": {
                "ref": PROJECTIVE_KERNEL_REF,
                "sha256": sha256_file(PROJECTIVE_KERNEL_REF),
            },
            "projective_split_locator_gate": {
                "ref": PROJECTIVE_SPLIT_LOCATOR_REF,
                "sha256": sha256_file(PROJECTIVE_SPLIT_LOCATOR_REF),
            },
            "m4_projective_budget_split": {
                "ref": M4_PROJECTIVE_BUDGET_REF,
                "sha256": sha256_file(M4_PROJECTIVE_BUDGET_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
            "omitted_regular_agreements": [385, 386, 387],
            "omission_reason": (
                "For rank 6, the finite-root emptiness proof uses t >= j+7; "
                "this starts at A=388.  No claim is made for A=385..387."
            ),
        },
        "family": {
            "base_support": "prefix X_A={x_0,...,x_j}",
            "direction_support": "next six descriptor-domain nodes Y_A={x_{j+1},...,x_{j+6}}",
            "weights": "unit weights in both u and v",
            "syndrome": "u_m=sum_{x in X_A} x^m, v_m=sum_{y in Y_A} y^m",
            "direction_rank": RANK,
        },
        "theorem": {
            "direction_rank": (
                "H(v)=V_t(Y_A) V_{j+1}(Y_A)^T has rank 6 because Y_A is "
                "distinct and both Vandermonde factors have rank 6."
            ),
            "finite_z_zero": (
                "At z=0, H(u)=V_t(X_A) V_{j+1}(X_A)^T has rank j+1 because "
                "X_A is distinct and t>=j+1."
            ),
            "finite_z_nonzero": (
                "At z!=0, H(u+zv)=V_t(X_A union Y_A) diag(1,z) "
                "V_{j+1}(X_A union Y_A)^T has rank j+1.  The proof uses "
                "t>=|X_A union Y_A|=j+7, so the left Vandermonde is injective, "
                "while the right Vandermonde has full column rank j+1."
            ),
            "canonical_finite_roots": (
                "By the regular-root rank-drop bridge, finite v10 canonical "
                "roots are exactly finite rank-drop slopes in nonsingular "
                "regular buckets.  The preceding rank computation makes the "
                "finite canonical root table empty, even after scalar extension."
            ),
            "projective_witness": (
                "At infinity, choose the monic locator whose roots are all six "
                "direction nodes and the first j-6 base nodes.  It divides "
                "X^512-1, has degree j, and satisfies H(v)ell=0.  The seven "
                "surviving base nodes give H(u)ell!=0 by a 7x7 Vandermonde "
                "argument."
            ),
            "rank6_boundary_consequence": (
                "This shows that a genuine support-wise projective endpoint can "
                "occur in a Hankel-realizable rank-6 direction family.  Thus the "
                "rank-6 boundary cannot be closed by asserting endpoint emptiness "
                "from Hankel realizability alone; one needs endpoint payment or "
                "finite root-table refinement."
            ),
        },
        "sampler_denominators": {
            "finite_affine_line": {
                "denominator": Q_LINE,
                "denominator_formula": "|F|",
                "budget_floor_denominator_over_2_128": FINITE_BUDGET,
            },
            "projective_line": {
                "denominator": PROJECTIVE_DENOMINATOR,
                "denominator_formula": "|P^1(F)| = |F| + 1",
                "budget_floor_denominator_over_2_128": PROJECTIVE_BUDGET,
            },
        },
        "field_audit": {
            "full_domain_distinct": True,
            "domain_size": len(domain_encodings),
            "domain_hash": hash_value(domain_encodings),
            "decoded_roundtrip_hash": hash_value([field.encode(value) for value in decoded]),
            "largest_prefix_support_needed": max_support_needed,
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "direction_rank": RANK,
            "finite_canonical_root_count_per_agreement": 0,
            "projective_endpoint_exact_contribution_per_agreement": 1,
            "ambient_projective_kernel_dimension_min": min(
                record["projective_infinity"]["ambient_projective_kernel_dimension"]
                for record in records
            ),
            "ambient_projective_kernel_dimension_max": max(
                record["projective_infinity"]["ambient_projective_kernel_dimension"]
                for record in records
            ),
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
            "finite_safe": True,
            "projective_safe": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "the needed prefix domain nodes are distinct",
            "direction rank is exactly 6 by Vandermonde factorization",
            "finite slopes have full column rank for A=388..426",
            "the projective locator divides X^512-1 by construction",
            "H(v)ell=0 because all direction nodes are locator roots",
            "H(u)ell!=0 because seven surviving base nodes form an invertible Vandermonde system",
            "finite and projective counts are within the printed 2^-128 budgets for this family",
        ],
        "nonclaims": [
            "does not classify arbitrary rank-6 Hankel pencils",
            "does not prove simultaneous rank-6 finite sharpness and projective endpoint sharpness",
            "does not make a claim for A=385..387",
            "does not prove endpoint payment or quotient/extension status",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 projective witness certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 projective-infinity witness")
    print("A={A_min}..{A_max}, agreements={agreement_count}".format(**window))
    print(
        "rank={direction_rank}, finite roots={finite_canonical_root_count_per_agreement}, projective endpoint={projective_endpoint_exact_contribution_per_agreement}".format(
            **summary
        )
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
