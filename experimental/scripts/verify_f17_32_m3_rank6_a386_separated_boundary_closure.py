#!/usr/bin/env python3
"""Verify the A=386 separated rank-6 boundary closure."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a386-separated-boundary-closure-v1"
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
CONIC_PAIR_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-conic-pair-safety/"
    "f17_32_n512_k256_m3_rank6_a386_conic_pair_safety.json"
)
COMPONENT_CUT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-component-cut-safety/"
    "f17_32_n512_k256_m3_rank6_a386_component_cut_safety.json"
)
GLOBAL_COMPONENT_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/"
    "f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json"
)
SLOPE_FREE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-slope-free-containment/"
    "f17_32_n512_k256_m3_rank6_a386_slope_free_containment.json"
)
MOVING_SLOPE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a386-moving-slope-split-incidence/"
    "f17_32_n512_k256_m3_rank6_a386_moving_slope_split_incidence.json"
)
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
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
    conic_pair = load_json(CONIC_PAIR_REF)
    component_cut = load_json(COMPONENT_CUT_REF)
    global_component = load_json(GLOBAL_COMPONENT_REF)
    slope_free = load_json(SLOPE_FREE_REF)
    moving_slope = load_json(MOVING_SLOPE_REF)
    endpoint_uniform = load_json(ENDPOINT_UNIFORM_REF)

    require(descriptor["row"]["n"] == N, "descriptor n mismatch")
    require(descriptor["row"]["k"] == K, "descriptor k mismatch")
    require(descriptor["row"]["field_order"] == Q_LINE, "descriptor q mismatch")
    require(
        low_degree["schema_version"] == "f17-32-m3-rank6-boundary-low-degree-transfer-v1",
        "low-degree transfer schema mismatch",
    )
    require(AGREEMENT in low_degree["window"]["agreements"], "A=386 not in transfer packet")
    require(
        conic_pair["schema_version"] == "f17-32-m3-rank6-a386-conic-pair-safety-v1",
        "conic-pair schema mismatch",
    )
    require(
        component_cut["schema_version"]
        == "f17-32-m3-rank6-a386-component-cut-safety-v1",
        "component-cut schema mismatch",
    )
    require(
        global_component["schema_version"]
        == "f17-32-m3-rank6-a386-global-component-slope-dichotomy-v1",
        "global-component schema mismatch",
    )
    require(
        slope_free["schema_version"] == "f17-32-m3-rank6-a386-slope-free-containment-v2",
        "slope-free schema mismatch",
    )
    require(
        moving_slope["schema_version"]
        == "f17-32-m3-rank6-a386-moving-slope-split-incidence-v51",
        "moving-slope schema mismatch",
    )
    require(
        endpoint_uniform["schema_version"]
        == "f17-32-m3-rank6-projective-endpoint-uniform-v1",
        "endpoint-uniform schema mismatch",
    )
    require(N % P != 0, "X^512-1 is not separable in this characteristic")
    require(FINITE_BUDGET == 6 and PROJECTIVE_BUDGET == 6, "unexpected budget")

    j_value = N - AGREEMENT
    t_value = AGREEMENT - K
    m_value = j_value + 1
    support_size = m_value + RANK
    h_value = support_size - t_value
    require(h_value == 3, "A=386 boundary defect should be three")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 2,
        "A=386 Q-space should be projective dimension two",
    )

    conic_summary = conic_pair["summary"]
    require(
        conic_summary["projective_safe_under_no_common_component_criterion"],
        "no-common-component branch should be safe",
    )
    require(
        conic_summary["support_wise_projective_total_upper_bound_under_criterion"] == 5,
        "no-common-component bound mismatch",
    )
    require(
        conic_summary["projective_endpoint_count"] == 1,
        "no-common-component endpoint mismatch",
    )

    cut_summary = component_cut["summary"]
    require(
        cut_summary["projective_safe_under_component_cut_criterion"],
        "component-cut branch should be safe",
    )
    require(
        cut_summary["support_wise_projective_total_upper_bound_under_component_cut"] == 5,
        "component-cut bound mismatch",
    )
    require(cut_summary["component_degrees"] == [1, 2], "component degree list mismatch")
    require(
        "irreducible component contained in all direction-consistency conics"
        in cut_summary["remaining_residual"],
        "component-cut residual mismatch",
    )

    global_summary = global_component["summary"]
    require(
        global_summary["constant_slope_non_base_branch_projective_safe"],
        "constant-slope branch should be safe",
    )
    require(
        global_summary["constant_slope_projective_total_upper_bound_off_base_locus"] == 2,
        "constant-slope bound mismatch",
    )
    require(
        global_summary["remaining_residuals"]
        == ["determined nonconstant slope map", "slope-free base locus or global component"],
        "global-component residual split mismatch",
    )

    slope_free_summary = slope_free["summary"]
    require(
        slope_free_summary["slope_free_vector_finite_noncontained_contribution"] == 0,
        "slope-free finite contribution mismatch",
    )
    require(
        slope_free_summary["slope_free_vector_projective_endpoint_contribution"] == 0,
        "slope-free endpoint contribution mismatch",
    )
    require(
        slope_free_summary["same_slope_shadow_additional_finite_parameter_contribution"] == 0,
        "same-slope finite shadow mismatch",
    )
    require(
        slope_free_summary["same_slope_shadow_additional_projective_parameter_contribution"]
        == 0,
        "same-slope endpoint shadow mismatch",
    )
    require(
        slope_free_summary["same_slope_noncontained_witness_charged_to_non_slope_free_branch"],
        "same-slope noncontained branch should be charged elsewhere",
    )

    moving_summary = moving_slope["summary"]
    require(
        moving_summary["line_moving_slope_components_projective_safe_all_external_cores"],
        "line moving-slope branch should be safe",
    )
    require(
        moving_summary["conic_moving_slope_components_projective_safe_all_external_cores"],
        "conic moving-slope branch should be safe",
    )
    require(
        moving_summary["line_remaining_unclosed_external_core_range"] == [],
        "line moving-slope residual should be empty",
    )
    require(
        moving_summary["conic_remaining_unclosed_external_core_range"] == [],
        "conic moving-slope residual should be empty",
    )
    require(
        moving_summary["remaining_unclosed_residuals"] == [],
        "moving-slope residual list should be empty",
    )
    require(
        endpoint_uniform["summary"]["projective_endpoint_exact_contribution_per_agreement"] == 1,
        "endpoint contribution mismatch",
    )

    branch_partition = [
        {
            "branch": "no_common_component_pair",
            "source": CONIC_PAIR_REF,
            "status": "projective_safe",
            "projective_total_upper_bound": 5,
            "reason": "two direction-consistency conics meet in at most four finite Q-classes",
        },
        {
            "branch": "common_component_cut_by_some_direction_conic",
            "source": COMPONENT_CUT_REF,
            "status": "projective_safe",
            "projective_total_upper_bound": 5,
            "reason": "component cuts plus off-component Bezout leave at most four finite Q-classes",
        },
        {
            "branch": "global_component_constant_slope_off_base_locus",
            "source": GLOBAL_COMPONENT_REF,
            "status": "projective_safe",
            "projective_total_upper_bound": 2,
            "reason": "constant slope contributes at most one finite parameter plus the endpoint",
        },
        {
            "branch": "global_component_slope_free_locus",
            "source": SLOPE_FREE_REF,
            "status": "zero_additional_support_wise_parameters",
            "projective_total_upper_bound": 0,
            "reason": "slope-free vectors fail both finite and projective noncontainment gates",
        },
        {
            "branch": "global_component_nonconstant_moving_slope_line_or_conic",
            "source": MOVING_SLOPE_REF,
            "status": "projective_safe",
            "projective_total_upper_bound": PROJECTIVE_BUDGET,
            "reason": "line and irreducible-conic moving-slope components are safe for every external core size",
        },
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=386 separated rank-6 boundary projective closure",
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
            "a386_conic_pair_safety": {
                "ref": CONIC_PAIR_REF,
                "sha256": sha256_file(CONIC_PAIR_REF),
            },
            "a386_component_cut_safety": {
                "ref": COMPONENT_CUT_REF,
                "sha256": sha256_file(COMPONENT_CUT_REF),
            },
            "a386_global_component_slope_dichotomy": {
                "ref": GLOBAL_COMPONENT_REF,
                "sha256": sha256_file(GLOBAL_COMPONENT_REF),
            },
            "a386_slope_free_containment": {
                "ref": SLOPE_FREE_REF,
                "sha256": sha256_file(SLOPE_FREE_REF),
            },
            "a386_moving_slope_split_incidence": {
                "ref": MOVING_SLOPE_REF,
                "sha256": sha256_file(MOVING_SLOPE_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
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
        "family": {
            "base_support": "any subset X of H with |X|=j+1",
            "direction_support": "any subset Y of H\\X with |Y|=6",
            "weights": "any nonzero base weights a_x and direction weights b_y",
            "support_condition": "X and Y are disjoint",
        },
        "theorem": {
            "low_degree_transfer": (
                "Every finite root in a separated rank-6 A=386 boundary bucket "
                "is represented by a projective Q-class with deg Q<3 in P^2, "
                "satisfying six direction-consistency equations before the "
                "split-locator divisor gate is applied."
            ),
            "bezout_or_component_split": (
                "Either two direction-consistency conics have no common component, "
                "or a common component appears.  The no-common-component branch "
                "is projective-safe by Bezout.  In the common-component branch, "
                "component cuts are projective-safe unless an irreducible component "
                "is contained in every direction-consistency conic."
            ),
            "global_component_split": (
                "A global component has a well-defined induced slope map away "
                "from the slope-free locus.  Constant maps are projective-safe; "
                "the remaining nonconstant map is a moving-slope line or "
                "irreducible-conic component because the component is an "
                "irreducible component of a plane conic."
            ),
            "slope_free_accounting": (
                "Slope-free transfer vectors satisfy both H(v)L_Q=0 and H(u)L_Q=0, "
                "so they fail the finite and projective noncontainment gates.  "
                "If an independent noncontained vector occurs at the same finite "
                "parameter, the parameter is charged once through the non-slope-free "
                "branch; the slope-free shadow adds no support-wise count."
            ),
            "moving_slope_closure": (
                "The moving-slope split-incidence packet closes all separated "
                "positive-dimensional line and irreducible-conic components for "
                "every external forced-core size, after the product-collapse and "
                "punctured/exact-tail refinements."
            ),
            "projective_safety": (
                "The branch partition has no live separated A=386 rank-6 residual. "
                "Every branch contributes at most the projective budget 6."
            ),
        },
        "branch_partition": branch_partition,
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
            "projective_budget": PROJECTIVE_BUDGET,
            "separated_support_rank6_boundary_projective_safe": True,
            "live_separated_a386_rank6_residuals": [],
            "branch_count": len(branch_partition),
            "explicit_bezout_projective_total_upper_bound": 5,
            "constant_slope_projective_total_upper_bound": 2,
            "slope_free_additional_support_wise_parameters": 0,
            "moving_slope_line_or_conic_projective_safe": True,
            "moving_slope_component_degrees_covered": [1, 2],
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=386 has boundary defect h=3 and Q-space P^2",
            "no-common-component conic pairs are projective-safe",
            "component-cut branches are projective-safe",
            "the only post-cut common-component residual is a global irreducible conic component",
            "global components split into constant-slope, moving-slope, and slope-free branches",
            "constant-slope non-base branch is projective-safe",
            "slope-free vectors add zero support-wise parameters",
            "same-slope slope-free shadows are charged through the non-slope-free branch if needed",
            "every irreducible component left by the conic tree is a line or irreducible conic",
            "moving-slope line and irreducible-conic branches have no live residual external-core range",
            "endpoint-uniform dependency supplies exactly one endpoint where endpoint accounting is used",
        ],
        "nonclaims": [
            "does not cover A=385",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment; it uses endpoint-budget accounting",
            "does not compute arbitrary non-separated rank-6 root tables",
            "does not close arbitrary rank-6 Hankel pencils",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=386 separated boundary closure mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=386 separated boundary closure")
    print(
        "branches={branch_count}, projective safe={separated_support_rank6_boundary_projective_safe}, live residuals={live_separated_a386_rank6_residuals}".format(
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
