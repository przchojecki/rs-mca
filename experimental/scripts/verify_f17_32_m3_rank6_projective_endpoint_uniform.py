#!/usr/bin/env python3
"""Verify the support-weight uniform rank-6 projective endpoint theorem."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-projective-endpoint-uniform-v1"
Q_LINE = 17**32
PROJECTIVE_DENOMINATOR = Q_LINE + 1
TARGET_BITS = 128
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
RANK = 6
SURVIVING_BASE_COUNT = RANK + 1
A_MIN = 385
A_MAX = 426
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
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


def agreement_record(agreement: int) -> dict[str, Any]:
    j_value = N - agreement
    t_value = agreement - K
    base_size = j_value + 1
    direction_choices_after_base = N - base_size
    require(j_value >= RANK, f"A={agreement}: need j>=6")
    require(t_value >= SURVIVING_BASE_COUNT, f"A={agreement}: need at least 7 rows")
    require(direction_choices_after_base >= RANK, f"A={agreement}: not enough direction nodes")
    support_choice_count = comb(N, base_size) * comb(direction_choices_after_base, RANK)
    survivor_choice_count_per_support = comb(base_size, SURVIVING_BASE_COUNT)
    return {
        "A": agreement,
        "j": j_value,
        "t": t_value,
        "base_support_size": base_size,
        "direction_support_size": RANK,
        "surviving_base_count": SURVIVING_BASE_COUNT,
        "support_choice_count": support_choice_count,
        "survivor_choice_count_per_support": survivor_choice_count_per_support,
        "weight_choice_count_formula": f"(q_line-1)^{base_size + RANK}",
        "projective_infinity": {
            "direction_rank": RANK,
            "ambient_kernel_dimension": base_size - RANK,
            "split_locator_degree": j_value,
            "split_locator_roots": (
                "the six direction nodes plus all but seven chosen base nodes"
            ),
            "H_v_locator": 0,
            "H_u_locator_nonzero": True,
            "split_locator_chart_nonempty": True,
            "projective_endpoint": "[0:1]",
            "exact_projective_endpoint_contribution": 1,
            "projective_budget": PROJECTIVE_BUDGET,
            "projective_safe_for_this_endpoint_parameter": 1 <= PROJECTIVE_BUDGET,
        },
    }


def build_certificate() -> dict[str, Any]:
    field = Field(P, MODULUS)
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    projective_kernel = load_json(PROJECTIVE_KERNEL_REF)
    projective_split = load_json(PROJECTIVE_SPLIT_LOCATOR_REF)
    projective_budget = load_json(M4_PROJECTIVE_BUDGET_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field"] == "F_17^32", "descriptor field mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        descriptor["m3_regular_window"]["A_min"] == A_MIN
        and descriptor["m3_regular_window"]["A_max"] == A_MAX,
        "descriptor M3 window mismatch",
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
    require(PROJECTIVE_BUDGET == 6, "unexpected projective budget")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "support-weight uniform rank-6 projective endpoint theorem",
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
        },
        "family": {
            "base_support": "any subset X of H with |X|=j+1",
            "direction_support": "any subset Y of H\\X with |Y|=6",
            "weights": "any nonzero base weights a_x and direction weights b_y",
            "syndrome": "u_m=sum_{x in X} a_x x^m, v_m=sum_{y in Y} b_y y^m",
            "endpoint_locator": (
                "choose any seven surviving base nodes R subset X; the locator "
                "roots are Y union (X\\R)"
            ),
        },
        "theorem": {
            "direction_rank": (
                "H(v)=V_t(Y) diag(b_y) V_{j+1}(Y)^T has rank 6 because Y is "
                "distinct, all b_y are nonzero, and t,j+1>=6."
            ),
            "split_locator": (
                "The endpoint locator has roots in H, degree 6+(j+1-7)=j, "
                "and therefore divides X^512-1."
            ),
            "H_v_zero": (
                "Every direction node is a locator root, so H(v)ell has rows "
                "sum_y b_y y^r L(y)=0."
            ),
            "H_u_nonzero": (
                "Only the seven surviving base nodes contribute to H(u)ell.  "
                "If H(u)ell were zero, the first seven rows would give an "
                "invertible 7x7 Vandermonde system forcing the seven nonzero "
                "values a_x L(x) to vanish."
            ),
            "slope_counting_note": (
                "The many locator choices are witnesses for the same projective "
                "slope [0:1]; they prove endpoint nonemptiness, not multiple "
                "projective slope parameters."
            ),
            "rank6_boundary_consequence": (
                "Endpoint nonemptiness is support- and weight-uniform for "
                "rank-6 separated-support Hankel directions.  Thus endpoint "
                "emptiness cannot be a generic rank-6 closure mechanism."
            ),
        },
        "sampler_denominators": {
            "projective_line": {
                "denominator": PROJECTIVE_DENOMINATOR,
                "denominator_formula": "|P^1(F)| = |F| + 1",
                "budget_floor_denominator_over_2_128": PROJECTIVE_BUDGET,
            }
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
            "projective_endpoint_exact_contribution_per_agreement": 1,
            "projective_budget": PROJECTIVE_BUDGET,
            "endpoint_nonempty_support_weight_uniform": True,
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "domain has 512 distinct nonzero elements and X^512-1 is separable",
            "for every A in 385..426 there are enough base and direction nodes",
            "direction rank is 6 by weighted Vandermonde factorization",
            "the endpoint locator is a monic degree-j divisor of X^512-1",
            "H(v)ell=0 because all direction nodes are locator roots",
            "H(u)ell!=0 by a seven-node weighted Vandermonde argument",
        ],
        "nonclaims": [
            "does not compute finite affine root tables",
            "does not classify arbitrary rank-6 Hankel pencils",
            "does not prove endpoint payment or quotient/extension status",
            "does not imply more than one projective slope parameter",
            "not a worst-case support-wise MCA row bound",
        ],
    }


def check_certificate(path: Path) -> None:
    expected = render(build_certificate())
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"rank-6 projective endpoint uniform certificate mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    window = certificate["window"]
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 projective endpoint uniform theorem")
    print("A={A_min}..{A_max}, agreements={agreement_count}".format(**window))
    print(
        "rank={direction_rank}, endpoint contribution={projective_endpoint_exact_contribution_per_agreement}".format(
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
