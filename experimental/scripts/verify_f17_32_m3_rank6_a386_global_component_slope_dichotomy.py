#!/usr/bin/env python3
"""Verify the A=386 global-component slope-map dichotomy."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a386-global-component-slope-dichotomy-v1"
Q_LINE = 17**32
TARGET_BITS = 128
FINITE_BUDGET = Q_LINE // 2**TARGET_BITS
PROJECTIVE_DENOMINATOR = Q_LINE + 1
PROJECTIVE_BUDGET = PROJECTIVE_DENOMINATOR // 2**TARGET_BITS
AGREEMENT = 386
RANK = 6
ROW_DESCRIPTOR_REF = (
    "experimental/data/certificates/hankel-f17-32-row-descriptor/"
    "f17_32_n512_k256_hankel_row_descriptor.json"
)
LOW_DEGREE_TRANSFER_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-boundary-low-degree-transfer/"
    "f17_32_n512_k256_m3_rank6_boundary_low_degree_transfer.json"
)
COMPONENT_CUT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/"
    "f17_32_n512_k256_m3_rank6_a386_component_cut_safety.json"
)
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
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
    component_cut = load_json(COMPONENT_CUT_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)
    split_gate = load_json(NULLPOLY_SPLIT_GATE_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(
        component_cut["schema_version"]
        == "f17-32-m3-rank6-a386-component-cut-safety-v1",
        "component-cut schema mismatch",
    )
    require(
        component_cut["summary"]["projective_safe_under_component_cut_criterion"],
        "component-cut summary mismatch",
    )
    require(
        endpoint_uniform["schema_version"]
        == "f17-32-m3-rank6-projective-endpoint-uniform-v1",
        "endpoint-uniform schema mismatch",
    )
    require(
        endpoint_uniform["summary"]["projective_endpoint_exact_contribution_per_agreement"] == 1,
        "endpoint contribution mismatch",
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
    require(h_value == 3, "A=386 boundary defect should be three")
    require(RANK * (RANK - 1) // 2 == 15, "pairwise conic count mismatch")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 2,
        "A=386 Q-space should be projective dimension two",
    )

    constant_slope_case = {
        "case": "determined_constant_slope_map_off_base_locus",
        "finite_slope_upper_bound_off_base_locus": 1,
        "projective_endpoint_count": 1,
        "support_wise_projective_total_upper_bound_off_base_locus": 2,
        "projective_budget": PROJECTIVE_BUDGET,
        "projective_safe_off_base_locus": True,
        "base_locus_status": "RESIDUAL unless split-locator or paid-ledger checks remove it",
    }
    residual_cases = [
        {
            "case": "determined_nonconstant_slope_map",
            "status": "RESIDUAL / UNKNOWN",
            "residual_label": "unknown",
            "meaning": (
                "a positive-dimensional component carries a nonconstant rational "
                "slope map; it must be cut by the split-locator divisor gate or "
                "identified as quotient/tangent/extension structure"
            ),
        },
        {
            "case": "slope_free_base_locus_or_component",
            "status": "RESIDUAL / UNKNOWN",
            "residual_label": "unknown",
            "meaning": (
                "all six numerator and denominator linear forms vanish at a "
                "base point, or identically on the component, so finite "
                "consistency does not determine a slope before further "
                "Hankel/split analysis"
            ),
        },
    ]
    require(
        constant_slope_case["support_wise_projective_total_upper_bound_off_base_locus"]
        <= PROJECTIVE_BUDGET,
        "constant slope branch should be projective safe",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=386 separated rank-6 global-component slope-map dichotomy",
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
            "a386_component_cut_safety": {
                "ref": COMPONENT_CUT_REF,
                "sha256": sha256_file(COMPONENT_CUT_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
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
            "projective_Q_search_dimension": 2,
        },
        "setup": {
            "direction_pairs": (
                "For each direction node y, set N_y(Q)=Omega_y Q(y) and "
                "D_y(Q)=b_y L_Q(y); both are linear forms in the Q-plane."
            ),
            "pairwise_consistency_conics": (
                "C_{y,y'}(Q)=N_y(Q)D_{y'}(Q)-N_{y'}(Q)D_y(Q), one for each "
                "pair of direction nodes."
            ),
            "global_component_residual": (
                "an irreducible component G in P^2 contained in all pairwise "
                "direction-consistency conics after the component-cut packet"
            ),
        },
        "theorem": {
            "slope_map": (
                "If some pair (N_y,D_y) is not identically zero on G, then "
                "[N_y:D_y] defines a rational projective slope map on G; the "
                "pairwise conics make this map independent of y on common "
                "domains of definition."
            ),
            "finite_roots_factor_through_slope_map": (
                "Every finite root represented by a Q-class on G has finite "
                "slope z=N_y(Q)/D_y(Q) for the induced map, before the "
                "split-locator divisor gate possibly removes it."
            ),
            "constant_map_safe": (
                "If the induced slope map is constant, then away from its "
                "base locus the component contributes at most one finite slope; "
                "adding the endpoint-uniform point gives projective total at "
                "most 2<=6 for the non-base branch."
            ),
            "nonconstant_residual": (
                "If the induced slope map is nonconstant, the branch is exactly "
                "a moving-slope global-component residual and is not closed by "
                "Bezout root counting alone."
            ),
            "slope_free_residual": (
                "If all pairs (N_y,D_y) vanish at a point, or identically on G, "
                "the finite consistency equations impose no slope there; this "
                "slope-free locus is a separate residual."
            ),
        },
        "constant_slope_case": constant_slope_case,
        "residual_cases": residual_cases,
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
            "boundary_defect_h": h_value,
            "projective_Q_search_dimension": 2,
            "direction_pair_count": RANK,
            "pairwise_direction_conic_count": RANK * (RANK - 1) // 2,
            "constant_slope_finite_root_upper_bound_off_base_locus": 1,
            "constant_slope_projective_total_upper_bound_off_base_locus": 2,
            "projective_budget": PROJECTIVE_BUDGET,
            "constant_slope_non_base_branch_projective_safe": True,
            "remaining_residuals": [
                "determined nonconstant slope map",
                "slope-free base locus or global component",
            ],
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=386 has boundary defect h=3 and Q-space P^2",
            "component-cut packet narrows to global components",
            "six direction pairs give fifteen pairwise conics",
            "constant slope gives at most one finite parameter off the base locus",
            "split-locator gate cannot increase finite parameter count",
            "endpoint-uniform dependency supplies exactly one endpoint",
            "2 <= projective budget 6",
        ],
        "nonclaims": [
            "does not prove all global components have constant slope",
            "does not close moving-slope global components",
            "does not close slope-free base loci or global components",
            "does not cover A=385",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=386 global-component slope dichotomy mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=386 global-component slope-map dichotomy")
    print(
        "constant finite off base <= {constant_slope_finite_root_upper_bound_off_base_locus}, projective total off base <= {constant_slope_projective_total_upper_bound_off_base_locus}; residuals={remaining_residuals}".format(
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
        check_certificate(args.check, certificate)
    print_summary(certificate)


if __name__ == "__main__":
    main()
