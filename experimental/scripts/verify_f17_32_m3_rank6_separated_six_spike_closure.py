#!/usr/bin/env python3
"""Verify the tall-range separated six-spike rank-6 closure."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-separated-six-spike-closure-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
RANK = 6
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
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
)
PROJECTIVE_BUDGET_REF = (
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
    column_count = j_value + 1
    finite_nonzero_support_size = column_count + RANK

    require(t_value >= column_count, f"A={agreement}: z=0 block is not tall")
    require(
        t_value >= finite_nonzero_support_size,
        f"A={agreement}: nonzero finite block is not tall enough",
    )
    require(column_count >= RANK + 1, f"A={agreement}: endpoint survivor count fails")

    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "base_support_size": column_count,
        "direction_support_size": RANK,
        "finite_nonzero_support_size": finite_nonzero_support_size,
        "t_minus_nonzero_support_size": t_value - finite_nonzero_support_size,
        "support_choice_count": comb(N, column_count) * comb(N - column_count, RANK),
        "weight_choice_count_formula": f"(q_line-1)^{column_count + RANK}",
        "finite_affine": {
            "z_zero_rank": column_count,
            "z_nonzero_rank": column_count,
            "canonical_finite_roots": [],
            "canonical_finite_root_count": 0,
            "canonical_common_gcd": "1",
            "finite_upper_bound": 0,
            "finite_budget": FINITE_BUDGET,
            "comparison_to_budget": comparison(0, FINITE_BUDGET),
        },
        "projective_infinity": {
            "endpoint_source": ENDPOINT_UNIFORM_REF,
            "exact_projective_endpoint_contribution": 1,
            "projective_total": 1,
            "projective_budget": PROJECTIVE_BUDGET,
            "comparison_to_budget": comparison(1, PROJECTIVE_BUDGET),
        },
    }


def check_dependency_window(ref: str, data: dict[str, Any]) -> None:
    if "window" in data:
        require(data["window"]["A_min"] <= A_MIN, f"{ref}: A_min too large")
        require(data["window"]["A_max"] >= A_MAX, f"{ref}: A_max too small")
    if "row" in data:
        require(data["row"]["n"] == N, f"{ref}: n mismatch")
        require(data["row"]["k"] == K, f"{ref}: k mismatch")


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    rank_drop = load_json(RANK_DROP_BRIDGE_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)
    projective_budget = load_json(PROJECTIVE_BUDGET_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(descriptor["row"]["syndrome_length"] == N - K, "descriptor syndrome mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] <= A_MIN
        and descriptor["m3_regular_window"]["A_max"] >= A_MAX,
        "descriptor M3 window mismatch",
    )
    require(
        rank_drop["schema_version"] == "f17-32-m3-m5-regular-root-rank-drop-v1",
        "rank-drop schema mismatch",
    )
    require(
        endpoint_uniform["schema_version"]
        == "f17-32-m3-rank6-projective-endpoint-uniform-v1",
        "endpoint-uniform schema mismatch",
    )
    require(
        endpoint_uniform["summary"]["projective_endpoint_exact_contribution_per_agreement"] == 1,
        "endpoint-uniform contribution mismatch",
    )
    require(
        projective_budget["schema_version"] == "f17-32-m3-m4-projective-budget-split-v1",
        "projective budget schema mismatch",
    )
    for ref, data in {
        RANK_DROP_BRIDGE_REF: rank_drop,
        ENDPOINT_UNIFORM_REF: endpoint_uniform,
        PROJECTIVE_BUDGET_REF: projective_budget,
    }.items():
        check_dependency_window(ref, data)

    domain_encodings = descriptor["domain"]["domain_encodings"]
    require(len(domain_encodings) == N, "domain length mismatch")
    require(len(set(domain_encodings)) == N, "descriptor domain is not distinct")
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    decoded = [field.decode(value) for value in domain_encodings]
    require(
        [field.encode(value) for value in decoded] == domain_encodings,
        "domain decode/encode roundtrip failed",
    )

    records = [agreement_record(agreement) for agreement in range(A_MIN, A_MAX + 1)]
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")
    require(records[0]["t_minus_nonzero_support_size"] == 1, "A_min tall margin mismatch")
    require(records[-1]["t_minus_nonzero_support_size"] == 77, "A_max tall margin mismatch")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "M3 rank-6 separated six-spike closure in the tall range",
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
            "regular_root_rank_drop": {
                "ref": RANK_DROP_BRIDGE_REF,
                "sha256": sha256_file(RANK_DROP_BRIDGE_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
            },
            "m4_projective_budget_split": {
                "ref": PROJECTIVE_BUDGET_REF,
                "sha256": sha256_file(PROJECTIVE_BUDGET_REF),
            },
        },
        "window": {
            "A_min": A_MIN,
            "A_max": A_MAX,
            "agreement_count": len(records),
        },
        "family": {
            "base_support": "any subset X of H with |X|=j+1",
            "direction_support": "any subset Y of H\\X with |Y|=6",
            "weights": "any nonzero base weights a_x and direction weights b_y",
            "syndrome": "u_m=sum_{x in X} a_x x^m, v_m=sum_{y in Y} b_y y^m",
            "finite_pencil": "H(u+zv)=V_t(S_z) diag(w_z) V_{j+1}(S_z)^T",
        },
        "theorem": {
            "finite_z_zero": (
                "At z=0, S_z=X has size j+1 and t>=j+1, so the Hankel block "
                "has full column rank j+1 by the weighted Vandermonde factorization."
            ),
            "finite_z_nonzero": (
                "For z!=0, S_z=X union Y has size j+7 and all weights remain "
                "nonzero.  In the tall range A>=388, t>=j+7.  Thus V_t(S_z) "
                "has full column rank j+7, diag(w_z) is invertible, and "
                "V_{j+1}(S_z)^T has full column rank j+1; the product has rank j+1."
            ),
            "finite_root_table": (
                "No finite affine slope can be a canonical regular rank-drop root "
                "for this separated support family."
            ),
            "projective_endpoint": (
                "The endpoint-uniform packet supplies a genuine split-locator "
                "witness at [0:1] for the same supports and weights."
            ),
            "projective_count": (
                "The projective contribution for this family is exactly one "
                "slope parameter, [0:1], hence it is within the projective budget 6."
            ),
        },
        "sampler_denominators": {
            "finite_line": {
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
            "x_512_minus_1_squarefree": True,
        },
        "agreement_records": records,
        "summary": {
            "agreement_count": len(records),
            "direction_rank": RANK,
            "finite_canonical_root_count_per_agreement": 0,
            "projective_endpoint_exact_contribution_per_agreement": 1,
            "projective_total_per_agreement": 1,
            "finite_budget": FINITE_BUDGET,
            "projective_budget": PROJECTIVE_BUDGET,
            "support_weight_uniform_separated_six_spike_closure": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "domain has 512 distinct nonzero elements and X^512-1 is separable",
            "for every A in 388..426, t>=j+7",
            "weighted Vandermonde factorization gives full column rank at z=0",
            "weighted Vandermonde factorization gives full column rank at every z!=0",
            "endpoint-uniform dependency supplies the projective split-locator witness",
            "projective total 1 is within the projective budget 6",
        ],
        "nonclaims": [
            "does not cover the boundary agreements A=385,386,387",
            "does not classify arbitrary rank-6 Hankel pencils",
            "does not handle overlapping base and direction supports",
            "does not prove endpoint payment by quotient, tangent, or extension ledgers",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 separated six-spike closure certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 separated six-spike closure")
    print("A={A_min}..{A_max}, agreements={agreement_count}".format(**window))
    print(
        "finite roots={finite_canonical_root_count_per_agreement}, projective total={projective_total_per_agreement}".format(
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
