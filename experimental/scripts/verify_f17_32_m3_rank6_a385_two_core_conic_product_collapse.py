#!/usr/bin/env python3
"""Verify the A=385 fixed two-core irreducible-conic product collapse."""

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

from experimental.scripts.emit_f17_32_hankel_row_descriptor import K, N, P  # noqa: E402


SCHEMA_VERSION = "f17-32-m3-rank6-a385-two-core-conic-product-collapse-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 385
RANK = 6
BASE_CORE_SIZE = 2
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_DEGREE_TRANSFER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/"
    "f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json"
)
HIGH_CORE_QUOTIENT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-high-core-quotient/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_high_core_quotient.json"
)
NULLPOLY_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
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


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    low_degree = load_json(LOW_DEGREE_TRANSFER_REF)
    high_core = load_json(HIGH_CORE_QUOTIENT_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(AGREEMENT in low_degree["window"]["agreements"], "A=385 not in transfer packet")
    require(
        high_core["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-high-core-quotient-v1",
        "high-core quotient schema mismatch",
    )
    require(
        high_core["summary"]["conic_residual_quotient_degree_at_most"] == 59,
        "high-core quotient dependency does not expose the conic quotient branch",
    )
    require(
        split_gate["schema_version"] == "f17-32-m3-nullpolynomial-split-locator-gate-v1",
        "split-gate schema mismatch",
    )
    require(split_gate["summary"]["split_locator_gate_available"], "split gate unavailable")
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    residual_vector_dimension = h_value - BASE_CORE_SIZE
    residual_projective_dimension = residual_vector_dimension - 1
    conic_threshold = high_core["summary"]["conic_high_core_external_core_min"]
    fixed_base_roots = BASE_CORE_SIZE
    residual_degree_bound = residual_vector_dimension
    residual_extra_root_cap = residual_degree_bound - 1
    product_common_factor_degree_bound = m_value - 3
    product_closed_max_external_core = (
        j_value - fixed_base_roots - residual_extra_root_cap - 1
    )
    conic_tail_core = product_closed_max_external_core + 1
    require(j_value == 127, "A=385 locator degree changed")
    require(h_value == 5, "A=385 boundary defect should be five")
    require(m_value == 128, "A=385 base support size changed")
    require(residual_vector_dimension == 3, "fixed two-core residual dimension changed")
    require(residual_projective_dimension == 2, "fixed two-core residual should be P^2")
    require(conic_threshold == 68, "conic high-core threshold changed")
    require(product_common_factor_degree_bound == 125, "common factor degree changed")
    require(product_closed_max_external_core == 122, "product-collapse closure limit changed")
    require(conic_tail_core == 123, "conic quotient tail core changed")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 4,
        "A=385 Q-space should be projective dimension four before core reduction",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed two-core irreducible-conic product collapse",
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
            "rank6_boundary_low_degree_transfer": {
                "ref": LOW_DEGREE_TRANSFER_REF,
                "sha256": sha256_file(LOW_DEGREE_TRANSFER_REF),
            },
            "a385_two_core_high_core_quotient": {
                "ref": HIGH_CORE_QUOTIENT_REF,
                "sha256": sha256_file(HIGH_CORE_QUOTIENT_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_GATE_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_GATE_REF),
            },
        },
        "agreement": {
            "A": AGREEMENT,
            "j": j_value,
            "t": t_value,
            "m": m_value,
            "direction_rank": RANK,
            "combined_support_size": support_size,
            "boundary_defect_h": h_value,
            "projective_Q_search_dimension_before_core": 4,
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "split_locator_degree": j_value,
        },
        "setup": {
            "base_multiplier": (
                "Let S be the degree-<m interpolant S(x)=Omega_x/a_x on X, "
                "let E be the fixed two-core locator, and put G=S*E."
            ),
            "kernel_polynomial": (
                "For residual R with deg R<3, L_{E R} is the remainder of "
                "G*R modulo P_X=prod_{x in X}(T-x)."
            ),
            "irreducible_conic_global_core": (
                "In the high-core irreducible-conic branch, every forced "
                "external root is global: ev_s(R)=L_{E R}(s) vanishes on the "
                "whole residual Q-plane."
            ),
        },
        "theorem": {
            "remainder_comparison": (
                "Write G=q_0 P_X+H with deg H<m.  If ev_s(1)=ev_s(T)=ev_s(T^2)=0 "
                "for some external s, then comparing ev_s(T)-s ev_s(1) and "
                "ev_s(T^2)-s ev_s(T) forces the T^(m-1) and T^(m-2) "
                "coefficients of H to vanish because P_X(s)!=0.  Thus deg H<=m-3."
            ),
            "product_collapse": (
                "With deg H<=m-3 and deg R<3, no modular reduction occurs: "
                "L_{E R}=H*R for every residual R."
            ),
            "base_roots_of_H": (
                "On the base support, H(x)R(x)=a_x^{-1}Omega_x E(x)R(x).  "
                "Thus H has exactly the two fixed base-core roots on X and no "
                "other base roots."
            ),
            "external_roots_of_H": (
                "For an external subgroup point s, H(s)=0 is equivalent to "
                "ev_s vanishing on the whole residual Q-plane.  Hence the "
                "external subgroup roots of H are exactly the global forced "
                "external core."
            ),
            "root_count_obstruction": (
                "Every product H*R has at most e_G forced external roots, the "
                "two fixed base roots, and at most two further subgroup roots "
                "from the nonzero residual polynomial R.  If e_G<=122, this is "
                "at most 126 roots, fewer than the 127 roots required by the "
                "degree-127 split-locator gate."
            ),
            "core_bound": (
                "Because H is nonzero of degree at most 125 and already has "
                "the two fixed base roots, an irreducible-conic global external "
                "core has size at most 123 after product collapse."
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
        "summary": {
            "agreement": AGREEMENT,
            "split_locator_degree": j_value,
            "conic_high_core_external_core_min": conic_threshold,
            "product_common_factor_degree_bound": product_common_factor_degree_bound,
            "fixed_base_roots_in_product_common_factor": fixed_base_roots,
            "residual_extra_root_cap": residual_extra_root_cap,
            "conic_product_collapse_closed_external_core_range": [
                conic_threshold,
                product_closed_max_external_core,
            ],
            "conic_product_collapse_impossible_external_core_range": [124, 126],
            "conic_quotient_tail_residual_external_core": conic_tail_core,
            "remaining_conic_residual_after_product_collapse": (
                "fixed two-core irreducible-conic quotient tail at e_G=123"
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 fixed two-core residual has Q-plane P^2 and locator degree 127",
            "high-core quotient dependency exposes the irreducible-conic quotient family",
            "global external core forces the top two remainder coefficients to vanish",
            "product collapse gives L_{E R}=H*R with deg H<=125",
            "H has exactly two fixed base roots and e_G global external roots on the subgroup",
            "e_G<=122 gives at most 126 subgroup roots for every H*R",
            "e_G>=124 is impossible for a nonzero H of degree <=125 with two fixed base roots",
        ],
        "nonclaims": [
            "does not close the e_G=123 irreducible-conic quotient tail",
            "does not prove product collapse for A=385 high-core line components",
            "does not close the full fixed two-core nonconstant moving-slope branch",
            "does not prove that every A=385 over-budget branch has a fixed two-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 two-core conic product-collapse mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed two-core conic product collapse")
    print(
        "closed conic cores={0}; residual e={1}".format(
            summary["conic_product_collapse_closed_external_core_range"],
            summary["conic_quotient_tail_residual_external_core"],
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
        check_certificate(args.check, certificate)
    print_summary(certificate)


if __name__ == "__main__":
    main()
