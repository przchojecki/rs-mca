#!/usr/bin/env python3
"""Verify the A=386 moving-slope split-incidence budget."""

from __future__ import annotations

import argparse
import itertools
from hashlib import sha256
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experimental.scripts.emit_f17_32_hankel_row_descriptor import K, N, P  # noqa: E402


SCHEMA_VERSION = "f17-32-m3-rank6-a386-moving-slope-split-incidence-v34"
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
SLOPE_DICHOTOMY_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a386-global-component-slope-dichotomy/"
    "f17_32_n512_k256_m3_rank6_a386_global_component_slope_dichotomy.json"
)
SLOPE_FREE_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a386-slope-free-containment/"
    "f17_32_n512_k256_m3_rank6_a386_slope_free_containment.json"
)
ENDPOINT_UNIFORM_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-projective-endpoint-uniform/"
    "f17_32_n512_k256_m3_rank6_projective_endpoint_uniform.json"
)
NULLPOLY_SPLIT_GATE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-nullpolynomial-split-locator-gate/"
    "f17_32_n512_k256_m3_nullpolynomial_split_locator_gate.json"
)
PROJECTIVE_TANGENT_REF = "experimental/notes/high_agreement/line_ca_projective.tex"


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


def finite_q_class_bound(component_degree: int, forced_core_size: int, locator_degree: int) -> int:
    require(component_degree > 0, "component degree must be positive")
    require(0 <= forced_core_size < locator_degree, "forced core outside budget formula range")
    incidences_available = component_degree * (N - forced_core_size)
    incidences_needed_per_split_locator = locator_degree - forced_core_size
    return incidences_available // incidences_needed_per_split_locator


def external_q_class_bound(
    component_degree: int,
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> int | None:
    require(component_degree > 0, "component degree must be positive")
    require(0 <= forced_external_core_size <= external_root_count, "external core out of range")
    required_external_roots = locator_degree - base_root_cap - forced_external_core_size
    if required_external_roots <= 0:
        return None
    incidences_available = component_degree * (external_root_count - forced_external_core_size)
    return incidences_available // required_external_roots


def max_core_for_bound(component_degree: int, locator_degree: int, target_bound: int) -> int | None:
    safe_values = [
        core
        for core in range(locator_degree)
        if finite_q_class_bound(component_degree, core, locator_degree) <= target_bound
    ]
    return max(safe_values) if safe_values else None


def max_external_core_for_bound(
    component_degree: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
    target_bound: int,
) -> int | None:
    safe_values = []
    for core in range(locator_degree - base_root_cap):
        bound = external_q_class_bound(
            component_degree,
            core,
            locator_degree,
            base_root_cap,
            external_root_count,
        )
        if bound is not None and bound <= target_bound:
            safe_values.append(core)
    return max(safe_values) if safe_values else None


def table_row(component_degree: int, forced_core_size: int, locator_degree: int) -> dict[str, Any]:
    finite_bound = finite_q_class_bound(component_degree, forced_core_size, locator_degree)
    return {
        "component_degree": component_degree,
        "forced_split_root_core_size": forced_core_size,
        "remaining_required_roots_per_valid_locator": locator_degree - forced_core_size,
        "remaining_root_hyperplanes": N - forced_core_size,
        "incidence_capacity": component_degree * (N - forced_core_size),
        "finite_Q_class_upper_bound": finite_bound,
        "finite_slope_upper_bound": finite_bound,
        "projective_total_with_endpoint_upper_bound": finite_bound + 1,
        "finite_safe": finite_bound <= FINITE_BUDGET,
        "projective_safe_with_endpoint": finite_bound + 1 <= PROJECTIVE_BUDGET,
    }


def external_table_row(
    component_degree: int,
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> dict[str, Any]:
    finite_bound = external_q_class_bound(
        component_degree,
        forced_external_core_size,
        locator_degree,
        base_root_cap,
        external_root_count,
    )
    required_external_roots = locator_degree - base_root_cap - forced_external_core_size
    row: dict[str, Any] = {
        "component_degree": component_degree,
        "forced_external_split_root_core_size": forced_external_core_size,
        "base_root_cap_per_Q": base_root_cap,
        "remaining_required_external_roots_per_valid_locator": max(required_external_roots, 0),
        "remaining_external_root_hyperplanes": external_root_count - forced_external_core_size,
        "external_incidence_capacity": component_degree
        * (external_root_count - forced_external_core_size),
    }
    if finite_bound is None:
        row.update(
            {
                "finite_Q_class_upper_bound": None,
                "finite_slope_upper_bound": None,
                "projective_total_with_endpoint_upper_bound": None,
                "finite_safe": False,
                "projective_safe_with_endpoint": False,
                "status": "RESIDUAL: external forced core already covers the post-base root requirement",
            }
        )
    else:
        row.update(
            {
                "finite_Q_class_upper_bound": finite_bound,
                "finite_slope_upper_bound": finite_bound,
                "projective_total_with_endpoint_upper_bound": finite_bound + 1,
                "finite_safe": finite_bound <= FINITE_BUDGET,
                "projective_safe_with_endpoint": finite_bound + 1 <= PROJECTIVE_BUDGET,
                "status": "bounded",
            }
        )
    return row


def conic_packing_excludes(
    candidate_count: int,
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> bool:
    require(candidate_count >= 2, "candidate count must be at least two")
    require(0 <= forced_external_core_size < locator_degree - base_root_cap, "core out of range")
    required_external_roots = locator_degree - base_root_cap - forced_external_core_size
    available_external_roots = external_root_count - forced_external_core_size
    lower_union_bound = (
        candidate_count * required_external_roots
        - candidate_count * (candidate_count - 1) // 2
    )
    return lower_union_bound > available_external_roots


def conic_packing_row(
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> dict[str, Any]:
    required_external_roots = locator_degree - base_root_cap - forced_external_core_size
    available_external_roots = external_root_count - forced_external_core_size

    def lower_union(candidate_count: int) -> int:
        return (
            candidate_count * required_external_roots
            - candidate_count * (candidate_count - 1) // 2
        )

    six_excluded = lower_union(6) > available_external_roots
    seven_excluded = lower_union(7) > available_external_roots
    return {
        "forced_external_split_root_core_size": forced_external_core_size,
        "required_nonforced_external_roots_per_valid_Q": required_external_roots,
        "available_nonforced_external_root_lines": available_external_roots,
        "lower_union_bound_for_6_Q_classes": lower_union(6),
        "six_Q_classes_excluded": six_excluded,
        "projective_safe_consequence": six_excluded,
        "lower_union_bound_for_7_Q_classes": lower_union(7),
        "seven_Q_classes_excluded": seven_excluded,
        "finite_safe_consequence": seven_excluded,
    }


def conic_pair_packing_finite_bound(
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> int | None:
    """Return the first pair-overlap exclusion upper bound, if one occurs."""
    required_external_roots = locator_degree - base_root_cap - forced_external_core_size
    available_external_roots = external_root_count - forced_external_core_size
    if required_external_roots <= 0:
        return None
    for candidate_count in range(1, locator_degree + 2):
        lower_union_bound = (
            candidate_count * required_external_roots
            - candidate_count * (candidate_count - 1) // 2
        )
        if lower_union_bound > available_external_roots:
            return candidate_count - 1
    return None


def projective_bound_profile_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: list[dict[str, Any]] = []
    for row in rows:
        value = row["current_projective_upper_bound"]
        if groups and groups[-1]["current_projective_upper_bound"] == value:
            groups[-1]["external_core_range"][1] = row["forced_external_core_size"]
        else:
            groups.append(
                {
                    "external_core_range": [
                        row["forced_external_core_size"],
                        row["forced_external_core_size"],
                    ],
                    "current_projective_upper_bound": value,
                    "projective_safe": value <= PROJECTIVE_BUDGET,
                    "one_over_budget": value == PROJECTIVE_BUDGET + 1,
                }
            )
    return groups


def cofactor_improved_intermediate_residual_profile_row(
    raw_row: dict[str, Any],
) -> dict[str, Any]:
    """Apply the cofactor-span top-saturation exclusion to the current envelope."""
    component_type = raw_row["component_type"]
    core = raw_row["forced_external_core_size"]
    cofactor_row = punctured_tangent_top_saturation_exclusion_row(component_type, core)
    if component_type == "line":
        incidence_projective_bound = raw_row["external_incidence_projective_bound"]
        incidence_method = "external incidence plus endpoint"
    else:
        require(component_type == "irreducible_conic", "unknown component type")
        pair_bound = raw_row["pair_overlap_finite_bound"]
        incidence_projective_bound = None if pair_bound is None else pair_bound + 1
        incidence_method = "pair-overlap packing plus endpoint"
    cofactor_bound = cofactor_row["cofactor_improved_projective_tangent_bound"]
    current_bound = min(
        bound for bound in [incidence_projective_bound, cofactor_bound] if bound is not None
    )
    active_methods = []
    if incidence_projective_bound == current_bound:
        active_methods.append(incidence_method)
    if cofactor_bound == current_bound:
        active_methods.append("cofactor-improved punctured projective tangent")
    return {
        "component_type": component_type,
        "forced_external_core_size": core,
        "incidence_or_pair_projective_bound": incidence_projective_bound,
        "raw_punctured_projective_tangent_bound": raw_row["punctured_projective_tangent_bound"],
        "cofactor_improved_projective_tangent_bound": cofactor_bound,
        "cofactor_top_saturation_excluded": cofactor_row[
            "top_saturation_excluded_by_cofactor_span"
        ],
        "current_projective_upper_bound": current_bound,
        "active_best_methods": active_methods,
        "projective_safe": current_bound <= PROJECTIVE_BUDGET,
        "one_over_budget": current_bound == PROJECTIVE_BUDGET + 1,
    }


def tangent_near_extremizer_common_support_complements(
    punctured_radius: int,
    finite_bad_slope_count: int,
) -> list[dict[str, Any]]:
    """Residual-budget alternatives from the tangent-staircase proof."""
    rows: list[dict[str, Any]] = []
    for complement_size in range(1, 2 * punctured_radius + 1):
        if complement_size <= punctured_radius:
            residual_budget_bound = complement_size
            private_zero_quota = 1
            branch = "common_support_at_least_agreement"
        else:
            private_zero_quota = complement_size - punctured_radius
            residual_budget_bound = complement_size // private_zero_quota
            branch = "common_support_below_agreement"
        if residual_budget_bound >= finite_bad_slope_count:
            rows.append(
                {
                    "common_support_complement_size": complement_size,
                    "private_zero_quota_per_slope": private_zero_quota,
                    "residual_budget_bound": residual_budget_bound,
                    "branch": branch,
                }
            )
    return rows


def max_simple_edges_for_signed_rank_at_most(rank_bound: int) -> dict[str, Any]:
    """Maximize simple graph edges with signed incidence rank at most rank_bound."""
    require(rank_bound >= 0, "rank bound should be nonnegative")
    component_capacities: list[dict[str, Any]] = []
    for component_rank in range(1, rank_bound + 1):
        component_capacities.append(
            {
                "component_type": "connected_graph",
                "component_rank": component_rank,
                "vertex_count": component_rank + 1,
                "max_edges": component_rank * (component_rank + 1) // 2,
                "model": "complete_graph",
            }
        )

    dp = [0] + [-1] * rank_bound
    parent: list[dict[str, Any] | None] = [None] * (rank_bound + 1)
    for total_rank in range(1, rank_bound + 1):
        for component in component_capacities:
            component_rank = component["component_rank"]
            if component_rank > total_rank or dp[total_rank - component_rank] < 0:
                continue
            candidate = dp[total_rank - component_rank] + component["max_edges"]
            if candidate > dp[total_rank]:
                dp[total_rank] = candidate
                parent[total_rank] = component

    best_rank = max(range(rank_bound + 1), key=lambda rank: dp[rank])
    decomposition: list[dict[str, Any]] = []
    cursor = best_rank
    while cursor > 0 and parent[cursor] is not None:
        component = parent[cursor]
        decomposition.append(component)
        cursor -= component["component_rank"]

    return {
        "field_characteristic": P,
        "uses_char_not_two": P != 2,
        "rank_bound": rank_bound,
        "max_edges": dp[best_rank],
        "rank_used_by_extremizer": best_rank,
        "component_capacity_by_rank": component_capacities,
        "extremal_decomposition": decomposition,
        "rank_formula": (
            "After scaling by barycentric weights, two-private cofactors are "
            "oriented edge vectors.  Over characteristic not two, a connected "
            "component of the signed incidence matrix contributes |V|-1 to rank."
        ),
    }


def exact_tail_private_rank_obstruction(
    quotient_dimension: int,
    finite_component_cofactor_count_at_least: int,
    max_private_coordinate_count: int,
) -> dict[str, Any]:
    if max_private_coordinate_count <= 1:
        return {
            "branch": "one_private_coordinate",
            "span_dimension_at_least": finite_component_cofactor_count_at_least,
            "strictly_exceeds_quotient_dimension": (
                finite_component_cofactor_count_at_least > quotient_dimension
            ),
            "rank_capacity_check": None,
        }
    require(
        max_private_coordinate_count == 2,
        "exact-tail closure only handles one- and two-private-coordinate branches",
    )
    rank_capacity = max_simple_edges_for_signed_rank_at_most(quotient_dimension)
    span_dimension_at_least = quotient_dimension + 1
    return {
        "branch": "two_private_coordinate_signed_edge",
        "span_dimension_at_least": span_dimension_at_least,
        "strictly_exceeds_quotient_dimension": (
            finite_component_cofactor_count_at_least > rank_capacity["max_edges"]
        ),
        "rank_capacity_check": rank_capacity,
    }


def tangent_tail_exact_agreement_closure_row(
    component_type: str,
    core: int,
) -> dict[str, Any]:
    """Close the cofactor-current tangent tail for r'=126-e_G <= 17."""
    row = punctured_tangent_top_saturation_exclusion_row(component_type, core)
    punctured_radius = row["punctured_cosupport_radius"]
    require(7 <= punctured_radius <= 17, "exact-tail closure covers r'=7..17")
    require(
        row["cofactor_improved_projective_tangent_bound"] >= PROJECTIVE_BUDGET + 1,
        "exact-tail closure should only target still-unsafe cofactor rows",
    )
    dangerous_projective_count = PROJECTIVE_BUDGET + 1
    near_extremizer_rows = tangent_near_extremizer_common_support_complements(
        punctured_radius,
        dangerous_projective_count,
    )
    private_coordinate_counts = [
        max(0, entry["common_support_complement_size"] - punctured_radius)
        for entry in near_extremizer_rows
    ]
    require(
        max(private_coordinate_counts) <= 2,
        "exact-tail closure only handles one- and two-private-coordinate branches",
    )
    quotient_dimension = quotient_family_vector_dimension(component_type)
    finite_component_cofactor_count_at_least = dangerous_projective_count - 1
    private_rank_obstruction = exact_tail_private_rank_obstruction(
        quotient_dimension,
        finite_component_cofactor_count_at_least,
        max(private_coordinate_counts),
    )
    require(
        private_rank_obstruction["strictly_exceeds_quotient_dimension"],
        "private cofactor span should strictly exceed quotient dimension",
    )
    minimum_finite_component_span_dimension = private_rank_obstruction[
        "span_dimension_at_least"
    ]
    require(
        minimum_finite_component_span_dimension > quotient_dimension,
        "exact-tail finite cofactor span should exceed quotient dimension",
    )
    return {
        "component_type": component_type,
        "forced_external_core_size": core,
        "punctured_length": row["punctured_length"],
        "punctured_exact_agreement": AGREEMENT,
        "punctured_cosupport_radius": punctured_radius,
        "raw_projective_tangent_bound": row["raw_projective_tangent_bound"],
        "cofactor_improved_projective_tangent_bound": (
            row["cofactor_improved_projective_tangent_bound"]
        ),
        "dangerous_projective_count": dangerous_projective_count,
        "after_projective_recoordinate": (
            "choose a nonbad projective point as infinity; seven projective "
            "bad points become seven finite bad slopes in the punctured row"
        ),
        "near_extremizer_common_support_complement_options": near_extremizer_rows,
        "private_coordinate_count_options": sorted(set(private_coordinate_counts)),
        "d_less_than_r_exclusion": (
            "If the common-support complement d is smaller than r'=n'-A, the "
            "common support has size greater than A.  This is a higher-agreement "
            "branch, not an exact-A contribution."
        ),
        "d_equals_r_exclusion": (
            "If d=r', the common support already has size A=386.  An exact-A "
            "split locator has no residual coordinate left to add, while the "
            "support-wise noncontainment argument requires a private residual "
            "coordinate outside the common support; this branch is higher-"
            "agreement or same-support contained."
        ),
        "d_equals_r_plus_1_cofactor_obstruction": (
            "If d=r'+1, every exact-A noncontained slope is obtained by adding "
            "one residual coordinate to a size-385 common support.  The residual "
            "quotient locators are degree-r' cofactors of an (r'+1)-point "
            "residual set."
        ),
        "d_equals_r_plus_2_edge_cofactor_obstruction": (
            "If d=r'+2, every exact-A noncontained slope is obtained by adding "
            "two residual coordinates to a size-384 common support.  The residual "
            "quotient locators evaluate on the residual set as six distinct "
            "two-supported oriented edge vectors after barycentric scaling.  Six "
            "distinct simple edges have signed incidence rank at least three over "
            "characteristic 17, so this branch closes line components but is not "
            "by itself enough for irreducible conic components."
        ),
        "original_projective_endpoint_count_at_most": 1,
        "finite_component_slope_count_at_least": finite_component_cofactor_count_at_least,
        "cofactor_independence_witness": (
            "For residual set Omega={omega_1,...,omega_{r'+1}}, the cofactors "
            "R_i(X)=prod_{m != i}(X-omega_m) satisfy R_i(omega_i)!=0 and "
            "R_m(omega_i)=0 for m != i, so every subset is linearly independent."
        ),
        "edge_cofactor_rank_witness": (
            "For the two-private-coordinate branch, restrict each cofactor to "
            "the residual set.  Its nonzero evaluations are supported exactly "
            "on the two private coordinates.  After invertible column scaling, "
            "these are signed edge vectors.  A rank-at-most-two signed incidence "
            "matrix over characteristic 17 supports at most three distinct simple "
            "edges, so six distinct finite slopes force rank at least three."
        ),
        "private_rank_obstruction": private_rank_obstruction,
        "finite_component_cofactor_span_dimension_at_least": (
            minimum_finite_component_span_dimension
        ),
        "quotient_family_vector_dimension_at_most": quotient_dimension,
        "contradiction": True,
        "projective_safe_after_exact_agreement_obstruction": True,
        "projective_upper_bound_after_obstruction": PROJECTIVE_BUDGET,
    }


def exact_agreement_current_profile_row(
    cofactor_current_row: dict[str, Any],
    exact_tail_safe_core_min: int,
) -> dict[str, Any]:
    """Apply the exact-agreement tangent-tail closure to the envelope."""
    row = dict(cofactor_current_row)
    if (
        row["forced_external_core_size"] >= exact_tail_safe_core_min
        and row["active_best_methods"] == ["cofactor-improved punctured projective tangent"]
        and row["current_projective_upper_bound"] > PROJECTIVE_BUDGET
    ):
        row["current_projective_upper_bound"] = PROJECTIVE_BUDGET
        row["projective_safe"] = True
        row["one_over_budget"] = False
        row["active_best_methods"] = ["exact-agreement tangent-tail cofactor closure"]
        row["exact_agreement_tail_closure_applied"] = True
    else:
        row["exact_agreement_tail_closure_applied"] = False
    return row


def intermediate_residual_profile_row(
    component_type: str,
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> dict[str, Any]:
    projective_tangent_bound = punctured_tangent_tail_row(forced_external_core_size)[
        "projective_bound_from_punctured_projective_tangent"
    ]
    if component_type == "line":
        finite_bound = external_q_class_bound(
            1,
            forced_external_core_size,
            locator_degree,
            base_root_cap,
            external_root_count,
        )
        incidence_projective_bound = None if finite_bound is None else finite_bound + 1
        current_bound = min(
            bound
            for bound in [incidence_projective_bound, projective_tangent_bound]
            if bound is not None
        )
        active_methods = []
        if incidence_projective_bound == current_bound:
            active_methods.append("external incidence plus endpoint")
        if projective_tangent_bound == current_bound:
            active_methods.append("punctured projective tangent")
        return {
            "component_type": component_type,
            "forced_external_core_size": forced_external_core_size,
            "external_incidence_finite_bound": finite_bound,
            "external_incidence_projective_bound": incidence_projective_bound,
            "pair_overlap_finite_bound": None,
            "punctured_projective_tangent_bound": projective_tangent_bound,
            "current_projective_upper_bound": current_bound,
            "active_best_methods": active_methods,
            "projective_safe": current_bound <= PROJECTIVE_BUDGET,
            "one_over_budget": current_bound == PROJECTIVE_BUDGET + 1,
        }

    require(component_type == "irreducible_conic", "unknown component type")
    pair_bound = conic_pair_packing_finite_bound(
        forced_external_core_size,
        locator_degree,
        base_root_cap,
        external_root_count,
    )
    pair_projective_bound = None if pair_bound is None else pair_bound + 1
    current_bound = min(
        bound for bound in [pair_projective_bound, projective_tangent_bound] if bound is not None
    )
    active_methods = []
    if pair_projective_bound == current_bound:
        active_methods.append("pair-overlap packing plus endpoint")
    if projective_tangent_bound == current_bound:
        active_methods.append("punctured projective tangent")
    return {
        "component_type": component_type,
        "forced_external_core_size": forced_external_core_size,
        "external_incidence_finite_bound": external_q_class_bound(
            2,
            forced_external_core_size,
            locator_degree,
            base_root_cap,
            external_root_count,
        ),
        "external_incidence_projective_bound": None,
        "pair_overlap_finite_bound": pair_bound,
        "punctured_projective_tangent_bound": projective_tangent_bound,
        "current_projective_upper_bound": current_bound,
        "active_best_methods": active_methods,
        "projective_safe": current_bound <= PROJECTIVE_BUDGET,
        "one_over_budget": current_bound == PROJECTIVE_BUDGET + 1,
    }


def line_six_finite_saturation_row(
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> dict[str, Any]:
    """Necessary conditions if a residual line reaches six finite classes."""
    required_external_roots = locator_degree - base_root_cap - forced_external_core_size
    available_external_roots = external_root_count - forced_external_core_size
    finite_target = FINITE_BUDGET
    minimal_external_incidence = finite_target * required_external_roots
    slack = available_external_roots - minimal_external_incidence
    require(slack >= 0, "six finite line classes should be incidence-feasible here")
    return {
        "component_type": "line",
        "forced_external_core_size": forced_external_core_size,
        "finite_classes_in_saturation_scenario": finite_target,
        "required_external_roots_per_class_min": required_external_roots,
        "available_nonforced_external_root_lines": available_external_roots,
        "minimal_external_root_lines_used_by_six_classes": minimal_external_incidence,
        "external_line_slack_after_minimal_six_classes": slack,
        "pairwise_external_root_sets_disjoint": True,
        "total_external_excess_over_minimal_six_classes_at_most": slack,
        "total_base_roots_across_six_classes_at_least": max(
            0,
            finite_target * base_root_cap - slack,
        ),
        "next_saving_needed": "exclude the six-class saturation pattern or pay the endpoint",
    }


def conic_six_finite_saturation_row(
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> dict[str, Any]:
    """Necessary conditions if a residual irreducible conic reaches six classes."""
    required_external_roots = locator_degree - base_root_cap - forced_external_core_size
    available_external_roots = external_root_count - forced_external_core_size
    finite_target = FINITE_BUDGET
    max_pair_overlap_events = finite_target * (finite_target - 1) // 2
    minimal_external_incidence = finite_target * required_external_roots
    forced_pair_overlaps_before_external_excess = max(
        0,
        minimal_external_incidence - available_external_roots,
    )
    require(
        forced_pair_overlaps_before_external_excess <= max_pair_overlap_events,
        "six finite conic classes should be pair-overlap feasible here",
    )
    return {
        "component_type": "irreducible_conic",
        "forced_external_core_size": forced_external_core_size,
        "finite_classes_in_saturation_scenario": finite_target,
        "required_external_roots_per_class_min": required_external_roots,
        "available_nonforced_external_root_lines": available_external_roots,
        "minimal_external_incidence_before_pair_overlap": minimal_external_incidence,
        "max_pair_overlap_events_for_six_classes": max_pair_overlap_events,
        "forced_pair_overlap_events_before_external_excess_at_least": (
            forced_pair_overlaps_before_external_excess
        ),
        "pair_overlap_slack_before_external_excess": (
            max_pair_overlap_events - forced_pair_overlaps_before_external_excess
        ),
        "extra_external_roots_raise_required_pair_overlaps_one_for_one": True,
        "next_saving_needed": "exclude the six-class saturation pattern or pay the endpoint",
    }


def tangent_one_over_tail_saturation_row(forced_external_core_size: int) -> dict[str, Any]:
    row = punctured_tangent_tail_row(forced_external_core_size)
    require(
        row["projective_bound_from_punctured_projective_tangent"] == PROJECTIVE_BUDGET + 1,
        "tail saturation row should be exactly one over budget",
    )
    return {
        "forced_external_core_size": forced_external_core_size,
        "punctured_length": row["punctured_length"],
        "punctured_cosupport_radius": row["punctured_radius"],
        "projective_tangent_bound": row["projective_bound_from_punctured_projective_tangent"],
        "saturation_meaning": (
            "any surviving branch at this core must saturate the punctured "
            "projective high-agreement tangent bound"
        ),
        "next_saving_needed": "one punctured tangent slope must be paid, duplicated, or absent",
    }


def line_over_budget_survival_row(saturation_row: dict[str, Any]) -> dict[str, Any]:
    """Necessary conditions for a line one-over row to genuinely exceed budget."""
    core = saturation_row["forced_external_core_size"]
    base_pressure = saturation_row["total_base_roots_across_six_classes_at_least"]
    if base_pressure >= 11:
        pressure_label = "near-complete base splitting"
    elif base_pressure >= 6:
        pressure_label = "positive base splitting"
    elif base_pressure >= 1:
        pressure_label = "weak base splitting"
    else:
        pressure_label = "external slack alone can absorb base deficit"
    return {
        "component_type": "line",
        "forced_external_core_size": core,
        "dangerous_projective_count": PROJECTIVE_BUDGET + 1,
        "finite_source_classes_must_equal": FINITE_BUDGET,
        "finite_slopes_must_be_distinct": True,
        "endpoint_must_survive_unpaid": True,
        "all_incidence_inequalities_must_saturate": True,
        "external_line_slack_after_minimal_six_classes": saturation_row[
            "external_line_slack_after_minimal_six_classes"
        ],
        "total_base_roots_across_six_classes_at_least": base_pressure,
        "base_pressure_label": pressure_label,
        "breakers": [
            "one missing split Q-class",
            "one duplicate finite slope",
            "endpoint paid or absent",
            "external/base incidence deficit exceeding the printed slack",
        ],
    }


def conic_over_budget_survival_row(saturation_row: dict[str, Any]) -> dict[str, Any]:
    """Necessary conditions for a conic one-over row to genuinely exceed budget."""
    required_edges = saturation_row["forced_pair_overlap_events_before_external_excess_at_least"]
    min_vertex_degree_lower_bound = max(0, required_edges - 10)
    if required_edges >= 14:
        pressure_label = "almost complete secant graph"
    elif required_edges >= 9:
        pressure_label = "dense secant graph"
    elif required_edges >= 4:
        pressure_label = "nontrivial secant graph"
    else:
        pressure_label = "pair-overlap pressure not forced before external excess"
    return {
        "component_type": "irreducible_conic",
        "forced_external_core_size": saturation_row["forced_external_core_size"],
        "dangerous_projective_count": PROJECTIVE_BUDGET + 1,
        "finite_source_classes_must_equal": FINITE_BUDGET,
        "finite_slopes_must_be_distinct": True,
        "endpoint_must_survive_unpaid": True,
        "all_pair_overlap_inequalities_must_saturate": True,
        "secant_graph_edges_required_before_external_excess_at_least": required_edges,
        "secant_graph_min_vertex_degree_lower_bound": min_vertex_degree_lower_bound,
        "pair_overlap_slack_before_external_excess": saturation_row[
            "pair_overlap_slack_before_external_excess"
        ],
        "secant_pressure_label": pressure_label,
        "breakers": [
            "one missing split Q-class",
            "one duplicate finite slope",
            "endpoint paid or absent",
            "too few external-root secants among the six Q-classes",
        ],
    }


def tangent_tail_over_budget_survival_row(
    component_type: str,
    saturation_row: dict[str, Any],
) -> dict[str, Any]:
    """Necessary conditions for the e=120 tangent one-over row to exceed budget."""
    return {
        "component_type": component_type,
        "forced_external_core_size": saturation_row["forced_external_core_size"],
        "dangerous_projective_count": PROJECTIVE_BUDGET + 1,
        "projective_tangent_bound_must_be_saturated": True,
        "punctured_cosupport_radius": saturation_row["punctured_cosupport_radius"],
        "punctured_length": saturation_row["punctured_length"],
        "breakers": [
            "one punctured tangent slope absent",
            "one duplicate slope after returning to the original branch",
            "one slope paid by tangent, quotient, extension, or containment",
        ],
    }


def single_saving_closure_row(survival_row: dict[str, Any]) -> dict[str, Any]:
    """A one-over row closes after any one of these single-saving events."""
    component_type = survival_row["component_type"]
    core = survival_row["forced_external_core_size"]
    if component_type == "line":
        return {
            "component_type": component_type,
            "forced_external_core_size": core,
            "one_over_source": "external incidence plus endpoint",
            "dangerous_projective_count": PROJECTIVE_BUDGET + 1,
            "safe_projective_count_after_one_saving": PROJECTIVE_BUDGET,
            "sufficient_single_savings": [
                "at most five finite split Q-classes",
                "at most five distinct finite slopes",
                "one duplicate among the six finite slopes",
                "projective endpoint absent or paid",
                "external/base incidence deficit exceeds the printed slack",
            ],
        }
    if component_type == "irreducible_conic":
        return {
            "component_type": component_type,
            "forced_external_core_size": core,
            "one_over_source": "pair-overlap packing plus endpoint",
            "dangerous_projective_count": PROJECTIVE_BUDGET + 1,
            "safe_projective_count_after_one_saving": PROJECTIVE_BUDGET,
            "sufficient_single_savings": [
                "at most five finite split Q-classes",
                "at most five distinct finite slopes",
                "one duplicate among the six finite slopes",
                "projective endpoint absent or paid",
                "too few external-root secants for the printed pair-overlap threshold",
            ],
        }
    raise AssertionError(f"unknown one-over component type: {component_type}")


def tangent_tail_single_saving_closure_row(survival_row: dict[str, Any]) -> dict[str, Any]:
    """Single-saving closure row for the e=120 punctured-tangent one-over case."""
    return {
        "component_type": survival_row["component_type"],
        "forced_external_core_size": survival_row["forced_external_core_size"],
        "one_over_source": "punctured projective tangent",
        "dangerous_projective_count": survival_row["dangerous_projective_count"],
        "safe_projective_count_after_one_saving": PROJECTIVE_BUDGET,
        "sufficient_single_savings": [
            "punctured projective tangent count at most six",
            "one punctured tangent slope absent",
            "one duplicate slope after returning to the original branch",
            "one slope paid by tangent, quotient, extension, or containment",
            "cofactor-span obstruction excludes the seven-slope tangent-star saturation profile",
        ],
    }


def tangent_tail_projective_extremizer_row(
    component_type: str,
    saturation_row: dict[str, Any],
) -> dict[str, Any]:
    """Necessary tangent-star structure if the e=120 projective tail saturates."""
    punctured_length = saturation_row["punctured_length"]
    punctured_agreement = AGREEMENT
    punctured_radius = saturation_row["punctured_cosupport_radius"]
    projective_count = saturation_row["projective_tangent_bound"]
    common_support_size = punctured_agreement - 1
    residual_coordinate_count = punctured_length - common_support_size
    tangent_gate_margin = 3 * punctured_agreement - 2 * punctured_length - K
    require(component_type in {"line", "irreducible_conic"}, "unknown component type")
    require(
        projective_count == PROJECTIVE_BUDGET + 1,
        "tail extremizer profile should only cover one-over rows",
    )
    require(projective_count == punctured_radius + 1, "projective count should be r'+1")
    require(
        residual_coordinate_count == projective_count,
        "tangent-star residual coordinates should biject to saturated projective slopes",
    )
    require(tangent_gate_margin >= 0, "punctured row must be in tangent-star range")
    require(
        PROJECTIVE_DENOMINATOR > projective_count,
        "a nonbad projective point must exist for the coordinate-change proof",
    )
    return {
        "component_type": component_type,
        "forced_external_core_size": saturation_row["forced_external_core_size"],
        "punctured_length": punctured_length,
        "punctured_agreement": punctured_agreement,
        "punctured_cosupport_radius": punctured_radius,
        "projective_saturation_count": projective_count,
        "projective_line_size": PROJECTIVE_DENOMINATOR,
        "nonbad_projective_point_available": True,
        "tangent_gate_margin_3a_minus_2n_minus_k": tangent_gate_margin,
        "after_projective_recoordinate": (
            "choose a nonbad projective point as infinity; the saturated bad "
            "projective set becomes a finite bad-slope set of size r'+1"
        ),
        "finite_tangent_star_common_support_size": common_support_size,
        "finite_tangent_star_residual_coordinate_count": residual_coordinate_count,
        "residual_coordinate_to_bad_slope_bijection_required": True,
        "cited_extremizer_result": (
            "Corollary cor:tangent-star-extremizers, applied after the "
            "coordinate-change step in Theorem thm:ca-projective-tangent-staircase"
        ),
        "next_saving_target": (
            "exclude compatibility between this tangent-star residual-coordinate "
            "bijection and the component's quotient split-locator family, or pay "
            "one of the seven projective tangent-star slopes"
        ),
        "nonclosure_reason": (
            "this is a necessary saturation profile only; it does not classify "
            "the endpoint or prove a paid slope"
        ),
    }


def tangent_tail_cofactor_span_closure_row(extremizer_row: dict[str, Any]) -> dict[str, Any]:
    """Close the e=120 tail by comparing cofactor span with the quotient family."""
    component_type = extremizer_row["component_type"]
    if component_type == "line":
        quotient_family_vector_dimension_at_most = 2
        quotient_family_reason = (
            "a line component is the projectivization of a 2-dimensional Q-subspace"
        )
    else:
        require(component_type == "irreducible_conic", "unknown component type")
        quotient_family_vector_dimension_at_most = 3
        quotient_family_reason = "a conic component lies in the ambient 3-dimensional Q-plane"

    projective_cofactor_count = extremizer_row["finite_tangent_star_residual_coordinate_count"]
    require(projective_cofactor_count == PROJECTIVE_BUDGET + 1, "tail should have seven cofactors")
    finite_component_cofactor_count_at_least = projective_cofactor_count - 1
    finite_component_cofactor_span_dimension_at_least = finite_component_cofactor_count_at_least
    require(
        finite_component_cofactor_span_dimension_at_least
        > quotient_family_vector_dimension_at_most,
        "finite cofactor span should exceed the quotient-family vector dimension",
    )
    return {
        "component_type": component_type,
        "forced_external_core_size": extremizer_row["forced_external_core_size"],
        "hypothetical_projective_saturation_count": projective_cofactor_count,
        "original_projective_endpoint_count_at_most": 1,
        "finite_component_slope_count_at_least": finite_component_cofactor_count_at_least,
        "punctured_residual_coordinate_count": projective_cofactor_count,
        "cofactor_polynomials": (
            "for residual set Omega={omega_1,...,omega_7}, the saturated "
            "split locators after forced-core puncturing are "
            "R_i(X)=prod_{m != i}(X-omega_m)"
        ),
        "cofactor_independence_witness": (
            "evaluation at omega_i kills all R_m with m != i and gives "
            "R_i(omega_i)!=0, so every subset of the seven cofactors is "
            "linearly independent"
        ),
        "finite_component_cofactor_span_dimension_at_least": (
            finite_component_cofactor_span_dimension_at_least
        ),
        "quotient_family_vector_dimension_at_most": quotient_family_vector_dimension_at_most,
        "quotient_family_reason": quotient_family_reason,
        "contradiction": True,
        "projective_safe_after_cofactor_span_obstruction": True,
        "projective_upper_bound_after_obstruction": PROJECTIVE_BUDGET,
        "closure_statement": (
            "the e_G=120 tail cannot realize seven projective slopes: at least "
            "six of them must be finite classes on the component, but their "
            "cofactors already span dimension six, exceeding the fixed-core "
            "quotient-family dimension"
        ),
    }


def one_over_mechanism_priority_ledger(
    line_catalog_rows: list[dict[str, Any]],
    conic_catalog_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Group one-over rows by the kind of saving that can still act first."""
    line_base_active = [
        row["forced_external_core_size"]
        for row in line_catalog_rows
        if not row["all_histograms_allowed"]
    ]
    line_external_only = [
        row["forced_external_core_size"]
        for row in line_catalog_rows
        if row["all_histograms_allowed"]
    ]
    conic_base_secant_active = [
        row["forced_external_core_size"]
        for row in conic_catalog_rows
        if not row["all_histograms_allowed"]
    ]
    conic_secant_only = [
        row["forced_external_core_size"]
        for row in conic_catalog_rows
        if row["all_histograms_allowed"] and not row["required_pair_overlap_range"] == [0, 0]
    ]
    conic_endpoint_only = [
        row["forced_external_core_size"]
        for row in conic_catalog_rows
        if row["all_histograms_allowed"] and row["required_pair_overlap_range"] == [0, 0]
    ]
    return [
        {
            "mechanism_class": "line_base_splitting_active",
            "component_type": "line",
            "external_core_range": [min(line_base_active), max(line_base_active)],
            "core_count": len(line_base_active),
            "primary_remaining_savings": [
                "base-root deficit",
                "duplicate finite slope",
                "endpoint paid or absent",
            ],
        },
        {
            "mechanism_class": "line_external_slack_only",
            "component_type": "line",
            "external_core_range": [min(line_external_only), max(line_external_only)],
            "core_count": len(line_external_only),
            "primary_remaining_savings": [
                "duplicate finite slope",
                "endpoint paid or absent",
                "paid/absent split class",
            ],
        },
        {
            "mechanism_class": "conic_base_and_secant_pressure_active",
            "component_type": "irreducible_conic",
            "external_core_range": [
                min(conic_base_secant_active),
                max(conic_base_secant_active),
            ],
            "core_count": len(conic_base_secant_active),
            "primary_remaining_savings": [
                "base-root deficit",
                "too few secants",
                "duplicate finite slope",
                "endpoint paid or absent",
            ],
        },
        {
            "mechanism_class": "conic_secant_pressure_only",
            "component_type": "irreducible_conic",
            "external_core_range": [min(conic_secant_only), max(conic_secant_only)],
            "core_count": len(conic_secant_only),
            "primary_remaining_savings": [
                "too few secants",
                "duplicate finite slope",
                "endpoint paid or absent",
            ],
        },
        {
            "mechanism_class": "conic_endpoint_or_duplicate_only",
            "component_type": "irreducible_conic",
            "external_core_range": [min(conic_endpoint_only), max(conic_endpoint_only)],
            "core_count": len(conic_endpoint_only),
            "primary_remaining_savings": [
                "duplicate finite slope",
                "endpoint paid or absent",
                "paid/absent split class",
            ],
        },
        {
            "mechanism_class": "punctured_tangent_tail_closed_by_cofactor_span",
            "component_type": "line_or_irreducible_conic",
            "external_core_range": [120, 120],
            "core_count": 2,
            "primary_remaining_savings": [
                "closed: six finite tangent-star cofactors cannot fit in the fixed-core quotient family",
            ],
        },
    ]


def exact_current_minimal_obstruction_profile(
    line_survival_rows: list[dict[str, Any]],
    conic_survival_rows: list[dict[str, Any]],
    line_catalog_rows: list[dict[str, Any]],
    conic_catalog_rows: list[dict[str, Any]],
    single_saving_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Normal form for any exact-current one-over witness that still survives."""
    line_catalog_by_core = {
        row["forced_external_core_size"]: row for row in line_catalog_rows
    }
    conic_catalog_by_core = {
        row["forced_external_core_size"]: row for row in conic_catalog_rows
    }
    saving_by_key = {
        (row["component_type"], row["forced_external_core_size"]): row
        for row in single_saving_rows
        if row["component_type"] in {"line", "irreducible_conic"}
        and row["forced_external_core_size"] != 120
    }
    rows: list[dict[str, Any]] = []
    for survival in line_survival_rows:
        core = survival["forced_external_core_size"]
        catalog = line_catalog_by_core[core]
        saving = saving_by_key[("line", core)]
        rows.append(
            {
                "component_type": "line",
                "forced_external_core_size": core,
                "status": "minimal exact-current finite-incidence obstruction",
                "one_over_source": saving["one_over_source"],
                "dangerous_projective_count": survival["dangerous_projective_count"],
                "finite_source_classes_must_equal": survival[
                    "finite_source_classes_must_equal"
                ],
                "finite_slopes_must_be_distinct": survival[
                    "finite_slopes_must_be_distinct"
                ],
                "endpoint_must_survive_unpaid": survival[
                    "endpoint_must_survive_unpaid"
                ],
                "all_incidence_inequalities_must_saturate": survival[
                    "all_incidence_inequalities_must_saturate"
                ],
                "base_pressure_label": survival["base_pressure_label"],
                "allowed_base_root_histogram_count": catalog[
                    "allowed_base_root_histogram_count"
                ],
                "total_base_root_incidence_range": catalog[
                    "total_base_root_incidence_range"
                ],
                "unused_nonforced_external_root_line_range": catalog[
                    "unused_nonforced_external_root_line_range"
                ],
                "pairwise_external_root_sets_disjoint": True,
                "single_savings_that_close": saving["sufficient_single_savings"],
                "next_algebraic_inputs": [
                    "force a duplicate finite slope in the line slope map",
                    "pay or remove the projective endpoint",
                    "prove a forced split-class absence from the quotient pencil",
                ],
            }
        )
    for survival in conic_survival_rows:
        core = survival["forced_external_core_size"]
        catalog = conic_catalog_by_core[core]
        saving = saving_by_key[("irreducible_conic", core)]
        rows.append(
            {
                "component_type": "irreducible_conic",
                "forced_external_core_size": core,
                "status": "minimal exact-current finite-incidence obstruction",
                "one_over_source": saving["one_over_source"],
                "dangerous_projective_count": survival["dangerous_projective_count"],
                "finite_source_classes_must_equal": survival[
                    "finite_source_classes_must_equal"
                ],
                "finite_slopes_must_be_distinct": survival[
                    "finite_slopes_must_be_distinct"
                ],
                "endpoint_must_survive_unpaid": survival[
                    "endpoint_must_survive_unpaid"
                ],
                "all_pair_overlap_inequalities_must_saturate": survival[
                    "all_pair_overlap_inequalities_must_saturate"
                ],
                "secant_pressure_label": survival["secant_pressure_label"],
                "allowed_base_root_histogram_count": catalog[
                    "allowed_base_root_histogram_count"
                ],
                "total_base_root_incidence_range": catalog[
                    "total_base_root_incidence_range"
                ],
                "required_pair_overlap_range": catalog["required_pair_overlap_range"],
                "maximum_missing_secant_range": catalog["maximum_missing_secant_range"],
                "nonforced_external_triple_use_forbidden": True,
                "single_savings_that_close": saving["sufficient_single_savings"],
                "next_algebraic_inputs": [
                    "force a duplicate finite slope in the conic slope map",
                    "pay or remove the projective endpoint",
                    "prove a forced secant deficit or split-class absence",
                ],
            }
        )
    return rows


def line_base_defect_threshold_row(survival_row: dict[str, Any]) -> dict[str, Any]:
    """Exact base-root distribution thresholds for six surviving line classes."""
    required_total = survival_row["total_base_roots_across_six_classes_at_least"]
    distributions = [
        tuple(counts)
        for counts in itertools.product(range(3), repeat=FINITE_BUDGET)
        if sum(counts) >= required_total
    ]
    require(distributions, "line base-root distributions should be feasible")
    min_two_root_classes = min(sum(1 for value in counts if value == 2) for counts in distributions)
    max_zero_root_classes = max(sum(1 for value in counts if value == 0) for counts in distributions)
    return {
        "component_type": "line",
        "forced_external_core_size": survival_row["forced_external_core_size"],
        "six_finite_classes": FINITE_BUDGET,
        "required_total_base_root_incidences": required_total,
        "minimum_two_base_root_classes": min_two_root_classes,
        "maximum_zero_base_root_classes": max_zero_root_classes,
        "closes_if_total_base_root_incidences_at_most": (
            required_total - 1 if required_total > 0 else None
        ),
        "closes_if_two_base_root_classes_at_most": (
            min_two_root_classes - 1 if min_two_root_classes > 0 else None
        ),
        "closes_if_zero_base_root_classes_at_least": (
            max_zero_root_classes + 1
            if max_zero_root_classes < FINITE_BUDGET
            else None
        ),
    }


def graph_extremal_stats(vertex_count: int, required_edges: int) -> dict[str, Any]:
    """Brute-force tiny graph extremal facts for required secant edges."""
    vertices = range(vertex_count)
    all_edges = list(itertools.combinations(vertices, 2))
    best_min_degree: int | None = None
    best_min_triangles: int | None = None
    for mask in range(1 << len(all_edges)):
        edge_count = mask.bit_count()
        if edge_count < required_edges:
            continue
        degrees = [0] * vertex_count
        edge_set = set()
        for index, edge in enumerate(all_edges):
            if mask & (1 << index):
                a, b = edge
                degrees[a] += 1
                degrees[b] += 1
                edge_set.add(edge)
        triangle_count = 0
        for a, b, c in itertools.combinations(vertices, 3):
            if (
                tuple(sorted((a, b))) in edge_set
                and tuple(sorted((a, c))) in edge_set
                and tuple(sorted((b, c))) in edge_set
            ):
                triangle_count += 1
        min_degree = min(degrees)
        best_min_degree = min_degree if best_min_degree is None else min(best_min_degree, min_degree)
        best_min_triangles = (
            triangle_count
            if best_min_triangles is None
            else min(best_min_triangles, triangle_count)
        )
    require(best_min_degree is not None, "graph extremal search should have feasible graphs")
    require(best_min_triangles is not None, "graph extremal search should have feasible graphs")
    return {
        "vertex_count": vertex_count,
        "possible_edges": len(all_edges),
        "required_edges": required_edges,
        "maximum_missing_edges": len(all_edges) - required_edges,
        "minimum_possible_min_degree": best_min_degree,
        "minimum_possible_triangles": best_min_triangles,
    }


def conic_secant_defect_threshold_row(survival_row: dict[str, Any]) -> dict[str, Any]:
    """Exact six-point graph thresholds for conic secant-overlap survival."""
    required_edges = survival_row["secant_graph_edges_required_before_external_excess_at_least"]
    stats = graph_extremal_stats(FINITE_BUDGET, required_edges)
    return {
        "component_type": "irreducible_conic",
        "forced_external_core_size": survival_row["forced_external_core_size"],
        "six_finite_classes": FINITE_BUDGET,
        "required_secant_edges_before_external_excess": required_edges,
        "maximum_missing_secants_before_external_excess": stats["maximum_missing_edges"],
        "minimum_possible_secant_graph_min_degree": stats["minimum_possible_min_degree"],
        "minimum_possible_secant_triangles": stats["minimum_possible_triangles"],
        "closes_if_secant_edges_at_most": required_edges - 1 if required_edges > 0 else None,
        "closes_if_secant_triangles_at_most": (
            stats["minimum_possible_triangles"] - 1
            if stats["minimum_possible_triangles"] > 0
            else None
        ),
    }


def line_base_extremal_shape_row(defect_row: dict[str, Any]) -> dict[str, Any]:
    """Classify base-root histograms compatible with a line defect threshold."""
    required_total = defect_row["required_total_base_root_incidences"]
    histograms = sorted(
        {
            (
                sum(1 for value in counts if value == 0),
                sum(1 for value in counts if value == 1),
                sum(1 for value in counts if value == 2),
            )
            for counts in itertools.product(range(3), repeat=FINITE_BUDGET)
            if sum(counts) >= required_total
        }
    )
    return {
        "component_type": "line",
        "forced_external_core_size": defect_row["forced_external_core_size"],
        "histogram_format": "[zero_base_root_classes, one_base_root_classes, two_base_root_classes]",
        "allowed_base_root_histograms": [list(histogram) for histogram in histograms],
        "closes_if_histogram_outside_list": True,
    }


def conic_secant_extremal_shape_row(defect_row: dict[str, Any]) -> dict[str, Any]:
    """Classify six-point secant graph shapes compatible with a conic threshold."""
    vertex_count = defect_row["six_finite_classes"]
    required_edges = defect_row["required_secant_edges_before_external_excess"]
    vertices = range(vertex_count)
    all_edges = list(itertools.combinations(vertices, 2))
    degree_sequences: set[tuple[int, ...]] = set()
    triangle_counts: set[int] = set()
    missing_edge_counts: set[int] = set()
    for mask in range(1 << len(all_edges)):
        edge_count = mask.bit_count()
        if edge_count < required_edges:
            continue
        degrees = [0] * vertex_count
        edge_set = set()
        for index, edge in enumerate(all_edges):
            if mask & (1 << index):
                a, b = edge
                degrees[a] += 1
                degrees[b] += 1
                edge_set.add(edge)
        triangle_count = 0
        for a, b, c in itertools.combinations(vertices, 3):
            if (
                tuple(sorted((a, b))) in edge_set
                and tuple(sorted((a, c))) in edge_set
                and tuple(sorted((b, c))) in edge_set
            ):
                triangle_count += 1
        degree_sequences.add(tuple(sorted(degrees)))
        triangle_counts.add(triangle_count)
        missing_edge_counts.add(len(all_edges) - edge_count)
    return {
        "component_type": "irreducible_conic",
        "forced_external_core_size": defect_row["forced_external_core_size"],
        "allowed_missing_secant_counts": sorted(missing_edge_counts),
        "allowed_sorted_degree_sequences": [list(seq) for seq in sorted(degree_sequences)],
        "allowed_secant_triangle_counts": sorted(triangle_counts),
        "closes_if_missing_secants_at_least": max(missing_edge_counts) + 1,
        "shape_description": "complete graph K6 or K6 with one missing edge",
    }


def base_root_histograms(min_total_base_roots: int) -> list[tuple[int, int, int]]:
    """Return histograms of six classes with 0/1/2 base roots and enough total roots."""
    return sorted(
        {
            (
                sum(1 for value in counts if value == 0),
                sum(1 for value in counts if value == 1),
                sum(1 for value in counts if value == 2),
            )
            for counts in itertools.product(range(3), repeat=FINITE_BUDGET)
            if sum(counts) >= min_total_base_roots
        }
    )


def exact_line_root_budget_alternatives(
    forced_external_core_size: int,
    locator_degree: int,
    external_root_count: int,
) -> list[dict[str, Any]]:
    """Exact six-class root-budget alternatives for a line component."""
    alternatives: list[dict[str, Any]] = []
    available_external = external_root_count - forced_external_core_size
    for histogram in base_root_histograms(0):
        zero_count, one_count, two_count = histogram
        total_base_roots = one_count + 2 * two_count
        exact_nonforced_external_roots = (
            FINITE_BUDGET * (locator_degree - forced_external_core_size)
            - total_base_roots
        )
        if exact_nonforced_external_roots <= available_external:
            alternatives.append(
                {
                    "base_root_histogram": list(histogram),
                    "total_base_root_incidences": total_base_roots,
                    "exact_nonforced_external_root_incidences": (
                        exact_nonforced_external_roots
                    ),
                    "unused_nonforced_external_root_lines": (
                        available_external - exact_nonforced_external_roots
                    ),
                }
            )
    return alternatives


def exact_conic_root_budget_alternatives(
    forced_external_core_size: int,
    locator_degree: int,
    external_root_count: int,
) -> list[dict[str, Any]]:
    """Exact six-class root-budget alternatives for an irreducible conic."""
    alternatives: list[dict[str, Any]] = []
    available_external = external_root_count - forced_external_core_size
    max_pair_overlaps = FINITE_BUDGET * (FINITE_BUDGET - 1) // 2
    for histogram in base_root_histograms(0):
        zero_count, one_count, two_count = histogram
        total_base_roots = one_count + 2 * two_count
        exact_nonforced_external_roots = (
            FINITE_BUDGET * (locator_degree - forced_external_core_size)
            - total_base_roots
        )
        required_pair_overlaps = max(0, exact_nonforced_external_roots - available_external)
        if required_pair_overlaps <= max_pair_overlaps:
            alternatives.append(
                {
                    "base_root_histogram": list(histogram),
                    "total_base_root_incidences": total_base_roots,
                    "exact_nonforced_external_root_incidences_before_overlap": (
                        exact_nonforced_external_roots
                    ),
                    "required_pair_overlaps_before_external_excess": required_pair_overlaps,
                    "maximum_missing_secants_before_external_excess": (
                        max_pair_overlaps - required_pair_overlaps
                    ),
                }
            )
    return alternatives


def line_one_over_design_catalog(
    forced_external_core_sizes: list[int],
    locator_degree: int,
    external_root_count: int,
) -> list[dict[str, Any]]:
    """Compact exact design catalog for the line one-over finite-incidence range."""
    rows: list[dict[str, Any]] = []
    for core in forced_external_core_sizes:
        alternatives = exact_line_root_budget_alternatives(
            core, locator_degree, external_root_count
        )
        base_totals = [row["total_base_root_incidences"] for row in alternatives]
        unused = [row["unused_nonforced_external_root_lines"] for row in alternatives]
        histograms = [row["base_root_histogram"] for row in alternatives]
        rows.append(
            {
                "forced_external_core_size": core,
                "allowed_base_root_histogram_count": len(alternatives),
                "total_base_root_incidence_range": [min(base_totals), max(base_totals)],
                "unused_nonforced_external_root_line_range": [min(unused), max(unused)],
                "all_zero_base_root_histogram_allowed": [FINITE_BUDGET, 0, 0] in histograms,
                "all_histograms_allowed": len(alternatives)
                == len(base_root_histograms(0)),
            }
        )
    return rows


def conic_one_over_design_catalog(
    forced_external_core_sizes: list[int],
    locator_degree: int,
    external_root_count: int,
) -> list[dict[str, Any]]:
    """Compact exact design catalog for the conic one-over finite-incidence range."""
    rows: list[dict[str, Any]] = []
    for core in forced_external_core_sizes:
        alternatives = exact_conic_root_budget_alternatives(
            core, locator_degree, external_root_count
        )
        base_totals = [row["total_base_root_incidences"] for row in alternatives]
        required_overlaps = [
            row["required_pair_overlaps_before_external_excess"]
            for row in alternatives
        ]
        missing_secants = [
            row["maximum_missing_secants_before_external_excess"]
            for row in alternatives
        ]
        histograms = [row["base_root_histogram"] for row in alternatives]
        rows.append(
            {
                "forced_external_core_size": core,
                "allowed_base_root_histogram_count": len(alternatives),
                "total_base_root_incidence_range": [min(base_totals), max(base_totals)],
                "required_pair_overlap_range": [
                    min(required_overlaps),
                    max(required_overlaps),
                ],
                "maximum_missing_secant_range": [min(missing_secants), max(missing_secants)],
                "all_zero_base_root_histogram_allowed": [FINITE_BUDGET, 0, 0] in histograms,
                "zero_pair_overlap_allowed": min(required_overlaps) == 0,
                "all_histograms_allowed": len(alternatives)
                == len(base_root_histograms(0)),
            }
        )
    return rows


def class_sizes_from_histogram(
    histogram: list[int],
    forced_external_core_size: int,
    locator_degree: int,
) -> list[int]:
    """Nonforced external roots demanded by classes with 0/1/2 base roots."""
    sizes: list[int] = []
    for base_root_count, class_count in enumerate(histogram):
        sizes.extend([locator_degree - forced_external_core_size - base_root_count] * class_count)
    return sorted(sizes, reverse=True)


def line_extremal_design_shapes(
    alternatives: list[dict[str, Any]],
    forced_external_core_size: int,
    locator_degree: int,
) -> list[dict[str, Any]]:
    """Combine the line histogram alternatives with disjoint external roots."""
    shapes: list[dict[str, Any]] = []
    for alternative in alternatives:
        unused = alternative["unused_nonforced_external_root_lines"]
        shapes.append(
            {
                "base_root_histogram": alternative["base_root_histogram"],
                "nonforced_external_class_sizes": class_sizes_from_histogram(
                    alternative["base_root_histogram"],
                    forced_external_core_size,
                    locator_degree,
                ),
                "covered_nonforced_external_root_lines": (
                    alternative["exact_nonforced_external_root_incidences"]
                ),
                "unused_nonforced_external_root_lines": unused,
                "partition_status": "covers_all" if unused == 0 else "covers_all_but_one",
            }
        )
    return shapes


def conic_extremal_design_shapes(
    alternatives: list[dict[str, Any]],
    forced_external_core_size: int,
    locator_degree: int,
    external_root_count: int,
) -> list[dict[str, Any]]:
    """Combine conic histograms with the K6/K6-minus-one secant alternatives."""
    shapes: list[dict[str, Any]] = []
    available_external = external_root_count - forced_external_core_size
    max_pair_overlaps = FINITE_BUDGET * (FINITE_BUDGET - 1) // 2
    for alternative in alternatives:
        max_missing = alternative["maximum_missing_secants_before_external_excess"]
        for missing_secants in range(max_missing + 1):
            pair_overlaps = max_pair_overlaps - missing_secants
            covered = (
                alternative["exact_nonforced_external_root_incidences_before_overlap"]
                - pair_overlaps
            )
            unused = available_external - covered
            if unused < 0:
                continue
            shapes.append(
                {
                    "base_root_histogram": alternative["base_root_histogram"],
                    "nonforced_external_class_sizes": class_sizes_from_histogram(
                        alternative["base_root_histogram"],
                        forced_external_core_size,
                        locator_degree,
                    ),
                    "secant_graph": (
                        "K6" if missing_secants == 0 else "K6_minus_one_edge"
                    ),
                    "pair_overlaps": pair_overlaps,
                    "missing_secants": missing_secants,
                    "secant_triangles": 20 if missing_secants == 0 else 16,
                    "covered_nonforced_external_root_lines": covered,
                    "unused_nonforced_external_root_lines": unused,
                    "cover_status": "covers_all" if unused == 0 else "covers_all_but_one",
                }
            )
    return shapes


def line_design_multiplicity_profiles(
    shapes: list[dict[str, Any]],
    external_root_count: int,
    forced_external_core_size: int,
) -> list[dict[str, Any]]:
    """Exact line-design membership counts on the nonforced external roots."""
    available_external = external_root_count - forced_external_core_size
    profiles: list[dict[str, Any]] = []
    for shape in shapes:
        covered = shape["covered_nonforced_external_root_lines"]
        unused = shape["unused_nonforced_external_root_lines"]
        require(covered + unused == available_external, "line design universe mismatch")
        profiles.append(
            {
                "base_root_histogram": shape["base_root_histogram"],
                "class_size_sequence": shape["nonforced_external_class_sizes"],
                "available_nonforced_external_root_lines": available_external,
                "multiplicity_zero_lines": unused,
                "multiplicity_one_lines": covered,
                "multiplicity_two_or_more_lines": 0,
                "pairwise_class_intersections": "all_zero",
            }
        )
    return profiles


def conic_design_multiplicity_profiles(
    shapes: list[dict[str, Any]],
    external_root_count: int,
    forced_external_core_size: int,
) -> list[dict[str, Any]]:
    """Exact conic-design membership counts; irreducibility excludes triple use."""
    available_external = external_root_count - forced_external_core_size
    profiles: list[dict[str, Any]] = []
    for shape in shapes:
        covered = shape["covered_nonforced_external_root_lines"]
        unused = shape["unused_nonforced_external_root_lines"]
        double_lines = shape["pair_overlaps"]
        single_lines = covered - double_lines
        require(covered + unused == available_external, "conic design universe mismatch")
        require(single_lines >= 0, "conic single-line count negative")
        profiles.append(
            {
                "base_root_histogram": shape["base_root_histogram"],
                "class_size_sequence": shape["nonforced_external_class_sizes"],
                "secant_graph": shape["secant_graph"],
                "class_overlap_degree_sequence": (
                    [5, 5, 5, 5, 5, 5]
                    if shape["secant_graph"] == "K6"
                    else [4, 4, 5, 5, 5, 5]
                ),
                "available_nonforced_external_root_lines": available_external,
                "multiplicity_zero_lines": unused,
                "multiplicity_one_lines": single_lines,
                "multiplicity_two_lines": double_lines,
                "multiplicity_three_or_more_lines": 0,
                "reason_no_triple_use": (
                    "a nonforced external root line meets an irreducible conic "
                    "in length at most two"
                ),
            }
        )
    return profiles


def line_design_local_profiles(shapes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per-Q-class local incidence data for the extremal line designs."""
    profiles: list[dict[str, Any]] = []
    for shape in shapes:
        class_sizes = shape["nonforced_external_class_sizes"]
        profiles.append(
            {
                "base_root_histogram": shape["base_root_histogram"],
                "class_count": len(class_sizes),
                "class_size_sequence": class_sizes,
                "pair_overlap_degree_sequence": [0] * len(class_sizes),
                "singleton_root_line_sequence": class_sizes,
                "local_description": (
                    "each valid Q-class owns exactly its class-size many "
                    "nonforced external root lines, with pairwise disjoint "
                    "ownership"
                ),
            }
        )
    return profiles


def line_e72_quotient_pencil_obstruction_profile(
    shapes: list[dict[str, Any]],
    quotient_degree: int,
) -> list[dict[str, Any]]:
    """Quotient-pencil normal form for the extremal line e_G=72 branch."""
    rows: list[dict[str, Any]] = []
    for shape in shapes:
        external_sizes = shape["nonforced_external_class_sizes"]
        base_root_counts = [quotient_degree - size for size in external_sizes]
        require(
            all(0 <= count <= 2 for count in base_root_counts),
            "line e=72 base-root counts should respect the degree<3 cap",
        )
        require(
            sum(base_root_counts)
            == sum(index * count for index, count in enumerate(shape["base_root_histogram"])),
            "line e=72 quotient fiber base-root count mismatch",
        )
        rows.append(
            {
                "base_root_histogram": shape["base_root_histogram"],
                "forced_external_core_size": 72,
                "quotient_degree": quotient_degree,
                "finite_split_fiber_count": FINITE_BUDGET,
                "nonforced_external_class_sizes": external_sizes,
                "base_root_count_sequence": sorted(base_root_counts),
                "covered_nonforced_external_root_lines": shape[
                    "covered_nonforced_external_root_lines"
                ],
                "unused_nonforced_external_root_lines": shape[
                    "unused_nonforced_external_root_lines"
                ],
                "external_partition_status": shape["partition_status"],
                "hidden_non_subgroup_roots_per_member": 0,
                "every_listed_member_is_full_degree_split": True,
                "pairwise_external_root_sets_disjoint": True,
                "necessary_condition": (
                    "After factoring the forced external core C_E, the residual "
                    "line component is a two-dimensional quotient pencil of "
                    "degree 54.  An extremal e_G=72 over-budget witness requires "
                    "six distinct projective pencil parameters whose quotient "
                    "polynomials are squarefree split degree-54 divisors of the "
                    "remaining subgroup polynomial."
                ),
                "closure_if_condition_fails": True,
                "next_algebraic_test": (
                    "Show that no degree-54 quotient pencil can have these six "
                    "full-split fibers with the printed external partition, or "
                    "force two fibers to produce the same finite slope."
                ),
            }
        )
    return rows


def line_quotient_pencil_obstruction_catalog(
    catalog_rows: list[dict[str, Any]],
    locator_degree: int,
    external_root_count: int,
) -> list[dict[str, Any]]:
    """Quotient-pencil normal form for every exact-current line one-over row."""
    rows: list[dict[str, Any]] = []
    for catalog in catalog_rows:
        core = catalog["forced_external_core_size"]
        quotient_degree = locator_degree - core
        alternatives = exact_line_root_budget_alternatives(
            core, locator_degree, external_root_count
        )
        class_size_sequences = [
            class_sizes_from_histogram(
                alternative["base_root_histogram"],
                core,
                locator_degree,
            )
            for alternative in alternatives
        ]
        total_base_roots = [
            alternative["total_base_root_incidences"] for alternative in alternatives
        ]
        unused_external = [
            alternative["unused_nonforced_external_root_lines"]
            for alternative in alternatives
        ]
        require(
            len(alternatives) == catalog["allowed_base_root_histogram_count"],
            "line quotient catalog histogram count mismatch",
        )
        require(
            [min(total_base_roots), max(total_base_roots)]
            == catalog["total_base_root_incidence_range"],
            "line quotient catalog base-root range mismatch",
        )
        require(
            [min(unused_external), max(unused_external)]
            == catalog["unused_nonforced_external_root_line_range"],
            "line quotient catalog unused external range mismatch",
        )
        require(
            all(
                sum(sequence) + alternative["total_base_root_incidences"]
                == FINITE_BUDGET * quotient_degree
                for sequence, alternative in zip(class_size_sequences, alternatives)
            ),
            "line quotient fibers should be full degree after forced core removal",
        )
        rows.append(
            {
                "component_type": "line",
                "forced_external_core_size": core,
                "quotient_degree": quotient_degree,
                "quotient_family": "two-dimensional quotient pencil",
                "finite_split_fiber_count": FINITE_BUDGET,
                "allowed_base_root_histogram_count": len(alternatives),
                "total_base_root_incidence_range": [
                    min(total_base_roots),
                    max(total_base_roots),
                ],
                "unused_nonforced_external_root_line_range": [
                    min(unused_external),
                    max(unused_external),
                ],
                "nonforced_external_roots_per_fiber_range": [
                    min(min(sequence) for sequence in class_size_sequences),
                    max(max(sequence) for sequence in class_size_sequences),
                ],
                "hidden_non_subgroup_roots_per_member": 0,
                "every_surviving_member_is_full_degree_split": True,
                "pairwise_external_root_sets_disjoint": True,
                "closure_if_condition_fails": True,
                "necessary_condition": (
                    "After the forced external core is factored, a surviving "
                    "line row must provide six distinct full-split members of "
                    "the printed quotient pencil with one of the listed base-root "
                    "histograms."
                ),
            }
        )
    return rows


def conic_quotient_family_obstruction_catalog(
    catalog_rows: list[dict[str, Any]],
    locator_degree: int,
    external_root_count: int,
) -> list[dict[str, Any]]:
    """Quotient-family normal form for every exact-current conic one-over row."""
    rows: list[dict[str, Any]] = []
    for catalog in catalog_rows:
        core = catalog["forced_external_core_size"]
        quotient_degree = locator_degree - core
        alternatives = exact_conic_root_budget_alternatives(
            core, locator_degree, external_root_count
        )
        class_size_sequences = [
            class_sizes_from_histogram(
                alternative["base_root_histogram"],
                core,
                locator_degree,
            )
            for alternative in alternatives
        ]
        total_base_roots = [
            alternative["total_base_root_incidences"] for alternative in alternatives
        ]
        pair_overlaps = [
            alternative["required_pair_overlaps_before_external_excess"]
            for alternative in alternatives
        ]
        missing_secants = [
            alternative["maximum_missing_secants_before_external_excess"]
            for alternative in alternatives
        ]
        require(
            len(alternatives) == catalog["allowed_base_root_histogram_count"],
            "conic quotient catalog histogram count mismatch",
        )
        require(
            [min(total_base_roots), max(total_base_roots)]
            == catalog["total_base_root_incidence_range"],
            "conic quotient catalog base-root range mismatch",
        )
        require(
            [min(pair_overlaps), max(pair_overlaps)]
            == catalog["required_pair_overlap_range"],
            "conic quotient catalog overlap range mismatch",
        )
        require(
            [min(missing_secants), max(missing_secants)]
            == catalog["maximum_missing_secant_range"],
            "conic quotient catalog missing-secant range mismatch",
        )
        require(
            all(
                sum(sequence) + alternative["total_base_root_incidences"]
                == FINITE_BUDGET * quotient_degree
                for sequence, alternative in zip(class_size_sequences, alternatives)
            ),
            "conic quotient members should be full degree after forced core removal",
        )
        rows.append(
            {
                "component_type": "irreducible_conic",
                "forced_external_core_size": core,
                "quotient_degree": quotient_degree,
                "quotient_family": "irreducible conic in the quotient Q-plane",
                "finite_split_member_count": FINITE_BUDGET,
                "allowed_base_root_histogram_count": len(alternatives),
                "total_base_root_incidence_range": [
                    min(total_base_roots),
                    max(total_base_roots),
                ],
                "required_pair_overlap_range": [
                    min(pair_overlaps),
                    max(pair_overlaps),
                ],
                "maximum_missing_secant_range": [
                    min(missing_secants),
                    max(missing_secants),
                ],
                "nonforced_external_roots_per_member_range": [
                    min(min(sequence) for sequence in class_size_sequences),
                    max(max(sequence) for sequence in class_size_sequences),
                ],
                "hidden_non_subgroup_roots_per_member": 0,
                "every_surviving_member_is_full_degree_split": True,
                "pairwise_external_overlap_at_most_one": True,
                "triple_external_root_line_use_forbidden": True,
                "closure_if_condition_fails": True,
                "necessary_condition": (
                    "After the forced external core is factored, a surviving "
                    "irreducible-conic row must provide six full-split quotient "
                    "members on the conic, with pair-overlap and missing-secant "
                    "ranges matching the printed catalog."
                ),
            }
        )
    return rows


def conic_design_local_profiles(shapes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Per-Q-class local secant/singleton counts for conic extremal designs."""
    profiles: list[dict[str, Any]] = []
    for shape in shapes:
        class_sizes = shape["nonforced_external_class_sizes"]
        overlap_degrees = (
            [5, 5, 5, 5, 5, 5]
            if shape["secant_graph"] == "K6"
            else [4, 4, 5, 5, 5, 5]
        )
        singleton_counts = [
            class_size - overlap_degree
            for class_size, overlap_degree in zip(class_sizes, overlap_degrees)
        ]
        require(min(singleton_counts) >= 0, "negative conic singleton count")
        profiles.append(
            {
                "base_root_histogram": shape["base_root_histogram"],
                "secant_graph": shape["secant_graph"],
                "class_count": len(class_sizes),
                "class_size_sequence": class_sizes,
                "secant_degree_sequence": overlap_degrees,
                "singleton_root_line_sequence": singleton_counts,
                "local_description": (
                    "each valid Q-class is incident to its secant-degree many "
                    "double-use external lines and the remaining listed singleton "
                    "external lines"
                ),
            }
        )
    return profiles


def canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    """Canonical representative of an undirected Hamiltonian cycle."""
    n = len(cycle)
    rotations = [cycle[i:] + cycle[:i] for i in range(n)]
    reversed_cycle = tuple(reversed(cycle))
    rotations.extend(reversed_cycle[i:] + reversed_cycle[:i] for i in range(n))
    return min(rotations)


def graph_edges_for_conic_secant_shape(secant_graph: str) -> set[tuple[int, int]]:
    """Representative six-vertex secant graph for the conic extremal shape."""
    edges = {
        (i, j)
        for i in range(FINITE_BUDGET)
        for j in range(i + 1, FINITE_BUDGET)
    }
    if secant_graph == "K6":
        return edges
    require(secant_graph == "K6_minus_one_edge", "unknown secant graph")
    edges.remove((0, 1))
    return edges


def hamiltonian_cycles(edge_set: set[tuple[int, int]]) -> list[tuple[int, ...]]:
    """Enumerate undirected Hamiltonian cycles supported by a six-vertex graph."""
    cycles: set[tuple[int, ...]] = set()
    vertices = tuple(range(FINITE_BUDGET))
    for perm in itertools.permutations(vertices):
        if perm[0] != 0:
            continue
        if all(
            tuple(sorted((perm[i], perm[(i + 1) % FINITE_BUDGET]))) in edge_set
            for i in range(FINITE_BUDGET)
        ):
            cycles.add(canonical_cycle(perm))
    return sorted(cycles)


def pascal_relation_for_cycle(cycle: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    """Return the three opposite-side intersection pairs for a Pascal relation."""
    a, b, c, d, e, f = cycle
    pairs = [
        (tuple(sorted((a, b))), tuple(sorted((d, e)))),
        (tuple(sorted((b, c))), tuple(sorted((e, f)))),
        (tuple(sorted((c, d))), tuple(sorted((f, a)))),
    ]
    return tuple(sorted(tuple(sorted(pair)) for pair in pairs))


def conic_e69_pascal_obstruction_profile(
    shapes: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Pascal-line necessary conditions for the extremal conic e_G=69 branch."""
    rows: list[dict[str, Any]] = []
    for shape in shapes:
        edge_set = graph_edges_for_conic_secant_shape(shape["secant_graph"])
        cycles = hamiltonian_cycles(edge_set)
        pascal_relations = sorted({pascal_relation_for_cycle(cycle) for cycle in cycles})
        require(cycles, "extremal conic graph should have Hamiltonian cycles")
        require(
            len(pascal_relations) == len(cycles),
            "generic Pascal relation count should match the cycle count",
        )
        rows.append(
            {
                "base_root_histogram": shape["base_root_histogram"],
                "secant_graph": shape["secant_graph"],
                "missing_secants": shape["missing_secants"],
                "secant_edge_count": len(edge_set),
                "hamiltonian_cycle_count": len(cycles),
                "pascal_collinearity_relation_count": len(pascal_relations),
                "representative_hamiltonian_cycle": list(cycles[0]),
                "representative_pascal_relation": [
                    [list(edge_pair[0]), list(edge_pair[1])]
                    for edge_pair in pascal_relations[0]
                ],
                "necessary_condition": (
                    "For every Hamiltonian cycle in the six-class secant graph, "
                    "Pascal's theorem forces the three intersections of opposite "
                    "external-root secants to be collinear in the Q-plane."
                ),
                "closure_if_condition_fails": True,
                "nonclosure_reason": (
                    "This records necessary Pascal constraints on any Hankel-realizable "
                    "extremal conic obstruction; it does not yet test the actual "
                    "external root-line arrangement."
                ),
            }
        )
    return rows


def interval_size(interval: list[int]) -> int:
    return interval[1] - interval[0]


def intervals_to_sets(intervals: list[list[int]]) -> list[set[int]]:
    return [set(range(start, stop)) for start, stop in intervals]


def first_line_incidence_only_sharpness_witness(
    forced_external_core_size: int,
    locator_degree: int,
    external_root_count: int,
) -> dict[str, Any]:
    """Construct an abstract line incidence design saturating the one-over bound."""
    alternatives = exact_line_root_budget_alternatives(
        forced_external_core_size,
        locator_degree,
        external_root_count,
    )
    require(alternatives, "line sharpness witness needs at least one alternative")
    alternative = alternatives[0]
    class_sizes = class_sizes_from_histogram(
        alternative["base_root_histogram"],
        forced_external_core_size,
        locator_degree,
    )
    available = external_root_count - forced_external_core_size
    intervals: list[list[int]] = []
    cursor = 0
    for size in class_sizes:
        intervals.append([cursor, cursor + size])
        cursor += size
    require(cursor <= available, "line sharpness design exceeds available lines")
    class_sets = intervals_to_sets(intervals)
    require(
        all(left.isdisjoint(right) for left, right in itertools.combinations(class_sets, 2)),
        "line sharpness classes should be pairwise disjoint",
    )
    return {
        "component_type": "line",
        "forced_external_core_size": forced_external_core_size,
        "status": "ABSTRACT_SHARPNESS_WITNESS_NOT_HANKEL_REALIZABILITY",
        "base_root_histogram": alternative["base_root_histogram"],
        "total_base_root_incidences": alternative["total_base_root_incidences"],
        "class_count": FINITE_BUDGET,
        "nonforced_external_class_size_sequence": class_sizes,
        "available_nonforced_external_root_lines": available,
        "class_intervals_on_abstract_external_lines": intervals,
        "covered_nonforced_external_root_lines": cursor,
        "unused_nonforced_external_root_lines": available - cursor,
        "pairwise_class_intersections": "all_zero",
        "saturates_current_finite_incidence_bound": True,
    }


def validate_line_incidence_only_sharpness_witness(
    row: dict[str, Any],
    locator_degree: int,
    external_root_count: int,
) -> None:
    core = row["forced_external_core_size"]
    histogram = row["base_root_histogram"]
    class_sizes = row["nonforced_external_class_size_sequence"]
    intervals = row["class_intervals_on_abstract_external_lines"]
    available = external_root_count - core
    require(row["component_type"] == "line", "line witness component mismatch")
    require(row["class_count"] == FINITE_BUDGET, "line witness should have six classes")
    require(sum(histogram) == FINITE_BUDGET, "line base histogram should have six classes")
    require(len(class_sizes) == FINITE_BUDGET, "line class-size count mismatch")
    require(len(intervals) == FINITE_BUDGET, "line interval count mismatch")
    require(all(0 <= start <= stop <= available for start, stop in intervals), "line interval range")
    require(
        [interval_size(interval) for interval in intervals] == class_sizes,
        "line interval sizes mismatch",
    )
    require(
        sorted(class_sizes, reverse=True)
        == class_sizes_from_histogram(histogram, core, locator_degree),
        "line class sizes do not match base histogram",
    )
    class_sets = intervals_to_sets(intervals)
    require(
        all(left.isdisjoint(right) for left, right in itertools.combinations(class_sets, 2)),
        "line class sets should be disjoint",
    )
    covered = len(set().union(*class_sets))
    require(
        covered == row["covered_nonforced_external_root_lines"],
        "line covered-line count mismatch",
    )
    require(
        row["unused_nonforced_external_root_lines"] == available - covered,
        "line unused-line count mismatch",
    )
    require(row["saturates_current_finite_incidence_bound"], "line witness should be sharp")


def first_conic_incidence_only_sharpness_witness(
    forced_external_core_size: int,
    locator_degree: int,
    external_root_count: int,
) -> dict[str, Any]:
    """Construct an abstract conic incidence design saturating the one-over bound."""
    alternatives = exact_conic_root_budget_alternatives(
        forced_external_core_size,
        locator_degree,
        external_root_count,
    )
    require(alternatives, "conic sharpness witness needs at least one alternative")
    alternative = alternatives[0]
    class_sizes = class_sizes_from_histogram(
        alternative["base_root_histogram"],
        forced_external_core_size,
        locator_degree,
    )
    required_pair_overlaps = alternative["required_pair_overlaps_before_external_excess"]
    all_edges = list(itertools.combinations(range(FINITE_BUDGET), 2))
    chosen_edges = all_edges[:required_pair_overlaps]
    degrees = [0] * FINITE_BUDGET
    for left, right in chosen_edges:
        degrees[left] += 1
        degrees[right] += 1
    singleton_counts = [
        class_size - degree for class_size, degree in zip(class_sizes, degrees)
    ]
    require(min(singleton_counts) >= 0, "conic singleton count negative")
    available = external_root_count - forced_external_core_size
    singleton_intervals: list[list[int]] = []
    cursor = required_pair_overlaps
    for count in singleton_counts:
        singleton_intervals.append([cursor, cursor + count])
        cursor += count
    require(cursor <= available, "conic sharpness design exceeds available lines")
    return {
        "component_type": "irreducible_conic",
        "forced_external_core_size": forced_external_core_size,
        "status": "ABSTRACT_SHARPNESS_WITNESS_NOT_HANKEL_REALIZABILITY",
        "base_root_histogram": alternative["base_root_histogram"],
        "total_base_root_incidences": alternative["total_base_root_incidences"],
        "class_count": FINITE_BUDGET,
        "nonforced_external_class_size_sequence": class_sizes,
        "available_nonforced_external_root_lines": available,
        "shared_secant_edges_on_classes": [list(edge) for edge in chosen_edges],
        "shared_secant_label_interval": [0, required_pair_overlaps],
        "singleton_intervals_on_abstract_external_lines": singleton_intervals,
        "covered_nonforced_external_root_lines": cursor,
        "unused_nonforced_external_root_lines": available - cursor,
        "pair_overlap_count": required_pair_overlaps,
        "class_overlap_degree_sequence": degrees,
        "singleton_root_line_sequence": singleton_counts,
        "multiplicity_three_or_more_lines": 0,
        "saturates_current_pair_overlap_bound": True,
    }


def validate_conic_incidence_only_sharpness_witness(
    row: dict[str, Any],
    locator_degree: int,
    external_root_count: int,
) -> None:
    core = row["forced_external_core_size"]
    histogram = row["base_root_histogram"]
    class_sizes = row["nonforced_external_class_size_sequence"]
    edges = [tuple(edge) for edge in row["shared_secant_edges_on_classes"]]
    singleton_intervals = row["singleton_intervals_on_abstract_external_lines"]
    available = external_root_count - core
    require(row["component_type"] == "irreducible_conic", "conic witness component mismatch")
    require(row["class_count"] == FINITE_BUDGET, "conic witness should have six classes")
    require(sum(histogram) == FINITE_BUDGET, "conic base histogram should have six classes")
    require(len(class_sizes) == FINITE_BUDGET, "conic class-size count mismatch")
    require(len(singleton_intervals) == FINITE_BUDGET, "conic singleton interval count")
    require(all(left < right for left, right in edges), "conic edge orientation mismatch")
    require(len(set(edges)) == len(edges), "conic edges should be distinct")
    require(
        row["shared_secant_label_interval"] == [0, len(edges)],
        "conic shared label interval mismatch",
    )
    require(
        sorted(class_sizes, reverse=True)
        == class_sizes_from_histogram(histogram, core, locator_degree),
        "conic class sizes do not match base histogram",
    )
    class_sets = [set() for _ in range(FINITE_BUDGET)]
    for label, (left, right) in enumerate(edges):
        class_sets[left].add(label)
        class_sets[right].add(label)
    for class_index, interval in enumerate(singleton_intervals):
        start, stop = interval
        require(0 <= start <= stop <= available, "conic singleton interval range")
        class_sets[class_index].update(range(start, stop))
    require(
        [len(class_set) for class_set in class_sets] == class_sizes,
        "conic class set sizes mismatch",
    )
    pairwise_intersections = [
        len(left & right) for left, right in itertools.combinations(class_sets, 2)
    ]
    require(max(pairwise_intersections, default=0) <= 1, "conic pairs should share at most one line")
    all_labels = [label for class_set in class_sets for label in class_set]
    multiplicity_counts = {label: all_labels.count(label) for label in set(all_labels)}
    require(
        max(multiplicity_counts.values(), default=0) <= 2,
        "conic design should have no triple-used line",
    )
    covered = len(set().union(*class_sets))
    require(
        covered == row["covered_nonforced_external_root_lines"],
        "conic covered-line count mismatch",
    )
    require(
        row["unused_nonforced_external_root_lines"] == available - covered,
        "conic unused-line count mismatch",
    )
    require(row["pair_overlap_count"] == len(edges), "conic pair-overlap count mismatch")
    require(row["saturates_current_pair_overlap_bound"], "conic witness should be sharp")


def quotient_residual_row(
    component_type: str,
    forced_external_core_threshold: int,
    locator_degree: int,
    base_root_cap: int,
    projective_source_dimension: int,
    forced_core_gcd_arity: int,
    forced_core_structure: str,
) -> dict[str, Any]:
    quotient_degree_bound = locator_degree - forced_external_core_threshold
    required_noncore_roots = locator_degree - base_root_cap - forced_external_core_threshold
    return {
        "component_type": component_type,
        "residual_forced_external_core_at_least": forced_external_core_threshold,
        "projective_source_dimension_after_core_factor": projective_source_dimension,
        "forced_core_gcd_arity": forced_core_gcd_arity,
        "forced_core_structure": forced_core_structure,
        "quotient_degree_at_most": quotient_degree_bound,
        "required_noncore_external_roots_after_base_cap_at_most": max(required_noncore_roots, 0),
        "normal_form": (
            "L_Q(X)=C_E(X) R_Q(X), where C_E is the forced external split-core "
            "divisor and deg R_Q <= j-|E|"
        ),
    }


def punctured_tangent_row(component_type: str, forced_external_core_threshold: int) -> dict[str, Any]:
    punctured_length = N - forced_external_core_threshold
    punctured_radius = (N - AGREEMENT) - forced_external_core_threshold
    tangent_radius = (punctured_length - K) // 3
    tangent_agreement_start = punctured_length - tangent_radius
    return {
        "component_type": component_type,
        "forced_external_core_at_least": forced_external_core_threshold,
        "punctured_length_at_threshold": punctured_length,
        "punctured_exact_agreement": AGREEMENT,
        "punctured_radius_at_threshold": punctured_radius,
        "punctured_tangent_radius_floor": tangent_radius,
        "punctured_tangent_exact_start": tangent_agreement_start,
        "in_high_agreement_tangent_range_at_threshold": punctured_radius <= tangent_radius,
        "tangent_numerator_at_threshold": punctured_radius + 1,
    }


def punctured_tangent_tail_row(forced_external_core_size: int) -> dict[str, Any]:
    punctured_length = N - forced_external_core_size
    punctured_radius = (N - AGREEMENT) - forced_external_core_size
    tangent_radius = (punctured_length - K) // 3
    finite_tangent_bound = punctured_radius + 1
    conservative_projective_bound_with_separate_endpoint = finite_tangent_bound + 1
    projective_tangent_bound = punctured_radius + 1
    return {
        "forced_external_core_size": forced_external_core_size,
        "punctured_length": punctured_length,
        "punctured_exact_agreement": AGREEMENT,
        "punctured_radius": punctured_radius,
        "punctured_tangent_radius_floor": tangent_radius,
        "in_high_agreement_tangent_range": punctured_radius <= tangent_radius,
        "finite_slope_bound_from_punctured_tangent": finite_tangent_bound,
        "conservative_endpoint_uniform_extra": 1,
        "conservative_projective_bound_with_separate_endpoint": (
            conservative_projective_bound_with_separate_endpoint
        ),
        "projective_bound_from_punctured_projective_tangent": projective_tangent_bound,
        "projective_safe_by_punctured_projective_tangent": (
            projective_tangent_bound <= PROJECTIVE_BUDGET
        ),
    }


def quotient_family_vector_dimension(component_type: str) -> int:
    if component_type == "line":
        return 2
    require(component_type == "irreducible_conic", "unknown component type")
    return 3


def punctured_tangent_top_saturation_exclusion_row(
    component_type: str,
    forced_external_core_size: int,
) -> dict[str, Any]:
    """Exclude top tangent saturation when the cofactor span is too large."""
    row = punctured_tangent_tail_row(forced_external_core_size)
    raw_projective_bound = row["projective_bound_from_punctured_projective_tangent"]
    quotient_dimension = quotient_family_vector_dimension(component_type)
    finite_component_count_at_top_at_least = raw_projective_bound - 1
    top_saturation_excluded = finite_component_count_at_top_at_least > quotient_dimension
    improved_bound = raw_projective_bound - 1 if top_saturation_excluded else raw_projective_bound
    return {
        "component_type": component_type,
        "forced_external_core_size": forced_external_core_size,
        "punctured_length": row["punctured_length"],
        "punctured_cosupport_radius": row["punctured_radius"],
        "raw_projective_tangent_bound": raw_projective_bound,
        "quotient_family_vector_dimension_at_most": quotient_dimension,
        "finite_component_cofactors_under_top_saturation_at_least": (
            finite_component_count_at_top_at_least
        ),
        "top_saturation_excluded_by_cofactor_span": top_saturation_excluded,
        "cofactor_improved_projective_tangent_bound": improved_bound,
        "cofactor_improved_projective_safe": improved_bound <= PROJECTIVE_BUDGET,
        "cofactor_improved_one_over_budget": improved_bound == PROJECTIVE_BUDGET + 1,
    }


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    low_degree = load_json(LOW_DEGREE_TRANSFER_REF)
    slope_dichotomy = load_json(SLOPE_DICHOTOMY_REF)
    slope_free = load_json(SLOPE_FREE_REF)
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
        slope_dichotomy["schema_version"]
        == "f17-32-m3-rank6-a386-global-component-slope-dichotomy-v1",
        "slope dichotomy schema mismatch",
    )
    require(
        "determined nonconstant slope map"
        in slope_dichotomy["summary"]["remaining_residuals"],
        "moving-slope residual is not exposed by dependency",
    )
    require(
        slope_free["schema_version"] == "f17-32-m3-rank6-a386-slope-free-containment-v1",
        "slope-free schema mismatch",
    )
    require(
        slope_free["summary"]["slope_free_vector_finite_noncontained_contribution"] == 0,
        "slope-free finite contribution mismatch",
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
    require(j_value == 126, "A=386 locator degree mismatch")
    require(h_value == 3, "A=386 boundary defect should be three")
    base_support_size = m_value
    external_root_count = N - base_support_size
    base_root_cap = h_value - 1
    require(base_support_size == 127, "base support size mismatch")
    require(external_root_count == 385, "external root count mismatch")
    require(base_root_cap == 2, "base root cap mismatch")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 2,
        "A=386 Q-space should be projective dimension two",
    )

    line_projective_safe_core_max = max_core_for_bound(1, j_value, PROJECTIVE_BUDGET - 1)
    line_finite_safe_core_max = max_core_for_bound(1, j_value, FINITE_BUDGET)
    conic_projective_safe_core_max = max_core_for_bound(2, j_value, PROJECTIVE_BUDGET - 1)
    conic_finite_safe_core_max = max_core_for_bound(2, j_value, FINITE_BUDGET)
    line_projective_safe_external_core_max = max_external_core_for_bound(
        1, j_value, base_root_cap, external_root_count, PROJECTIVE_BUDGET - 1
    )
    line_finite_safe_external_core_max = max_external_core_for_bound(
        1, j_value, base_root_cap, external_root_count, FINITE_BUDGET
    )
    conic_projective_safe_external_core_max = max_external_core_for_bound(
        2, j_value, base_root_cap, external_root_count, PROJECTIVE_BUDGET - 1
    )
    conic_finite_safe_external_core_max = max_external_core_for_bound(
        2, j_value, base_root_cap, external_root_count, FINITE_BUDGET
    )
    conic_projective_safe_packing_external_core_max = max(
        core
        for core in range(j_value - base_root_cap)
        if conic_packing_excludes(6, core, j_value, base_root_cap, external_root_count)
    )
    conic_finite_safe_packing_external_core_max = max(
        core
        for core in range(j_value - base_root_cap)
        if conic_packing_excludes(7, core, j_value, base_root_cap, external_root_count)
    )

    require(line_projective_safe_core_max == 48, "line projective threshold changed")
    require(line_finite_safe_core_max == 61, "line finite threshold changed")
    require(conic_projective_safe_core_max is None, "conic projective safety should not follow")
    require(conic_finite_safe_core_max is None, "conic finite safety should not follow")
    require(
        line_projective_safe_external_core_max == 71,
        "base-sharpened line projective threshold changed",
    )
    require(
        line_finite_safe_external_core_max == 80,
        "base-sharpened line finite threshold changed",
    )
    require(
        conic_projective_safe_external_core_max is None,
        "base-sharpened conic projective safety should not follow",
    )
    require(
        conic_finite_safe_external_core_max == 19,
        "base-sharpened conic finite threshold changed",
    )
    require(
        conic_projective_safe_packing_external_core_max == 68,
        "conic packing projective threshold changed",
    )
    require(
        conic_finite_safe_packing_external_core_max == 76,
        "conic packing finite threshold changed",
    )

    unrefined_sample_rows = [
        table_row(1, 0, j_value),
        table_row(1, line_projective_safe_core_max, j_value),
        table_row(1, line_projective_safe_core_max + 1, j_value),
        table_row(1, line_finite_safe_core_max, j_value),
        table_row(1, line_finite_safe_core_max + 1, j_value),
        table_row(2, 0, j_value),
        table_row(2, line_projective_safe_core_max, j_value),
        table_row(2, j_value - 1, j_value),
    ]
    base_sharpened_sample_rows = [
        external_table_row(1, 0, j_value, base_root_cap, external_root_count),
        external_table_row(
            1,
            line_projective_safe_external_core_max,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        external_table_row(
            1,
            line_projective_safe_external_core_max + 1,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        external_table_row(
            1,
            line_finite_safe_external_core_max,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        external_table_row(
            1,
            line_finite_safe_external_core_max + 1,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        external_table_row(2, 0, j_value, base_root_cap, external_root_count),
        external_table_row(
            2,
            conic_finite_safe_external_core_max,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        external_table_row(
            2,
            conic_finite_safe_external_core_max + 1,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        external_table_row(2, j_value - base_root_cap, j_value, base_root_cap, external_root_count),
    ]
    conic_packing_sample_rows = [
        conic_packing_row(0, j_value, base_root_cap, external_root_count),
        conic_packing_row(
            conic_projective_safe_packing_external_core_max,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        conic_packing_row(
            conic_projective_safe_packing_external_core_max + 1,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        conic_packing_row(
            conic_finite_safe_packing_external_core_max,
            j_value,
            base_root_cap,
            external_root_count,
        ),
        conic_packing_row(
            conic_finite_safe_packing_external_core_max + 1,
            j_value,
            base_root_cap,
            external_root_count,
        ),
    ]
    line_residual_core_threshold = line_projective_safe_external_core_max + 1
    conic_residual_core_threshold = conic_projective_safe_packing_external_core_max + 1
    quotient_residual_rows = [
        quotient_residual_row(
            "line",
            line_residual_core_threshold,
            j_value,
            base_root_cap,
            projective_source_dimension=1,
            forced_core_gcd_arity=2,
            forced_core_structure=(
                "dual-evaluation fiber: the external evaluation functional "
                "vanishes on the two-dimensional vector subspace underlying the line"
            ),
        ),
        quotient_residual_row(
            "irreducible_conic",
            conic_residual_core_threshold,
            j_value,
            base_root_cap,
            projective_source_dimension=2,
            forced_core_gcd_arity=3,
            forced_core_structure=(
                "global common core: an irreducible conic is not contained in a "
                "projective line, so the external evaluation functional is zero on the whole Q-plane"
            ),
        ),
    ]
    punctured_tangent_rows = [
        punctured_tangent_row("line", line_residual_core_threshold),
        punctured_tangent_row("irreducible_conic", conic_residual_core_threshold),
    ]
    tail_projective_safe_core_min = min(
        core
        for core in range(line_residual_core_threshold, j_value)
        if punctured_tangent_tail_row(core)["projective_safe_by_punctured_projective_tangent"]
    )
    punctured_tangent_tail_rows = [
        punctured_tangent_tail_row(tail_projective_safe_core_min - 1),
        punctured_tangent_tail_row(tail_projective_safe_core_min),
        punctured_tangent_tail_row(j_value - 1),
    ]
    line_cofactor_tangent_rows = [
        punctured_tangent_top_saturation_exclusion_row("line", core)
        for core in range(line_residual_core_threshold, j_value)
    ]
    conic_cofactor_tangent_rows = [
        punctured_tangent_top_saturation_exclusion_row("irreducible_conic", core)
        for core in range(conic_residual_core_threshold, j_value)
    ]
    line_cofactor_tangent_safe_core_min = min(
        row["forced_external_core_size"]
        for row in line_cofactor_tangent_rows
        if row["cofactor_improved_projective_safe"]
    )
    conic_cofactor_tangent_safe_core_min = min(
        row["forced_external_core_size"]
        for row in conic_cofactor_tangent_rows
        if row["cofactor_improved_projective_safe"]
    )
    line_cofactor_tangent_one_over_cores = [
        row["forced_external_core_size"]
        for row in line_cofactor_tangent_rows
        if row["cofactor_improved_one_over_budget"]
    ]
    conic_cofactor_tangent_one_over_cores = [
        row["forced_external_core_size"]
        for row in conic_cofactor_tangent_rows
        if row["cofactor_improved_one_over_budget"]
    ]
    line_intermediate_profile_rows = [
        intermediate_residual_profile_row(
            "line",
            core,
            j_value,
            base_root_cap,
            external_root_count,
        )
        for core in range(line_residual_core_threshold, tail_projective_safe_core_min)
    ]
    conic_intermediate_profile_rows = [
        intermediate_residual_profile_row(
            "irreducible_conic",
            core,
            j_value,
            base_root_cap,
            external_root_count,
        )
        for core in range(conic_residual_core_threshold, tail_projective_safe_core_min)
    ]
    line_profile_groups = projective_bound_profile_groups(line_intermediate_profile_rows)
    conic_profile_groups = projective_bound_profile_groups(conic_intermediate_profile_rows)
    line_cofactor_current_profile_rows = [
        cofactor_improved_intermediate_residual_profile_row(row)
        for row in line_intermediate_profile_rows
    ]
    conic_cofactor_current_profile_rows = [
        cofactor_improved_intermediate_residual_profile_row(row)
        for row in conic_intermediate_profile_rows
    ]
    line_cofactor_current_profile_groups = projective_bound_profile_groups(
        line_cofactor_current_profile_rows
    )
    conic_cofactor_current_profile_groups = projective_bound_profile_groups(
        conic_cofactor_current_profile_rows
    )
    line_incidence_one_over_cores = [
        row["forced_external_core_size"]
        for row in line_intermediate_profile_rows
        if row["one_over_budget"] and "external incidence plus endpoint" in row["active_best_methods"]
    ]
    conic_pair_one_over_cores = [
        row["forced_external_core_size"]
        for row in conic_intermediate_profile_rows
        if row["one_over_budget"] and "pair-overlap packing plus endpoint" in row["active_best_methods"]
    ]
    tangent_one_over_tail_cores = sorted(
        {
            row["forced_external_core_size"]
            for row in line_intermediate_profile_rows + conic_intermediate_profile_rows
            if row["one_over_budget"] and row["active_best_methods"] == ["punctured projective tangent"]
        }
    )
    line_six_saturation_rows = [
        line_six_finite_saturation_row(core, j_value, base_root_cap, external_root_count)
        for core in line_incidence_one_over_cores
    ]
    conic_six_saturation_rows = [
        conic_six_finite_saturation_row(core, j_value, base_root_cap, external_root_count)
        for core in conic_pair_one_over_cores
    ]
    tangent_tail_saturation_rows = [
        tangent_one_over_tail_saturation_row(core) for core in tangent_one_over_tail_cores
    ]
    line_survival_rows = [
        line_over_budget_survival_row(row) for row in line_six_saturation_rows
    ]
    conic_survival_rows = [
        conic_over_budget_survival_row(row) for row in conic_six_saturation_rows
    ]
    tangent_tail_survival_rows = [
        tangent_tail_over_budget_survival_row(component_type, tangent_tail_saturation_rows[0])
        for component_type in ["line", "irreducible_conic"]
    ]
    tangent_tail_extremizer_rows = [
        tangent_tail_projective_extremizer_row(component_type, tangent_tail_saturation_rows[0])
        for component_type in ["line", "irreducible_conic"]
    ]
    tangent_tail_cofactor_span_closure_rows = [
        tangent_tail_cofactor_span_closure_row(row) for row in tangent_tail_extremizer_rows
    ]
    def exact_tail_safe_radius_max_for_component(component_type: str) -> int:
        quotient_dimension = quotient_family_vector_dimension(component_type)
        safe_radii: list[int] = []
        for radius in range(PROJECTIVE_BUDGET + 1, j_value + 1):
            private_coordinate_count = max(
                max(0, entry["common_support_complement_size"] - radius)
                for entry in tangent_near_extremizer_common_support_complements(
                    radius,
                    PROJECTIVE_BUDGET + 1,
                )
            )
            if private_coordinate_count > 2:
                continue
            obstruction = exact_tail_private_rank_obstruction(
                quotient_dimension,
                PROJECTIVE_BUDGET,
                private_coordinate_count,
            )
            if obstruction["strictly_exceeds_quotient_dimension"]:
                safe_radii.append(radius)
        return max(safe_radii)

    line_exact_tail_safe_radius_max = exact_tail_safe_radius_max_for_component("line")
    conic_exact_tail_safe_radius_max = exact_tail_safe_radius_max_for_component(
        "irreducible_conic"
    )
    line_exact_tail_safe_core_min = j_value - line_exact_tail_safe_radius_max
    conic_exact_tail_safe_core_min = j_value - conic_exact_tail_safe_radius_max
    require(line_exact_tail_safe_radius_max == 17, "line exact-tail safe radius changed")
    require(line_exact_tail_safe_core_min == 109, "line exact-tail safe core changed")
    require(conic_exact_tail_safe_radius_max == 11, "conic exact-tail safe radius changed")
    require(conic_exact_tail_safe_core_min == 115, "conic exact-tail safe core changed")
    exact_tail_closure_cores_by_component = {
        "line": list(range(line_exact_tail_safe_core_min, line_cofactor_tangent_safe_core_min)),
        "irreducible_conic": list(
            range(conic_exact_tail_safe_core_min, conic_cofactor_tangent_safe_core_min)
        ),
    }
    require(
        exact_tail_closure_cores_by_component
        == {
            "line": list(range(109, 120)),
            "irreducible_conic": list(range(115, 120)),
        },
        "exact-tail cores",
    )
    tangent_tail_exact_closure_rows = [
        tangent_tail_exact_agreement_closure_row(component_type, core)
        for component_type in ["line", "irreducible_conic"]
        for core in exact_tail_closure_cores_by_component[component_type]
    ]
    line_base_defect_rows = [
        line_base_defect_threshold_row(row) for row in line_survival_rows
    ]
    conic_secant_defect_rows = [
        conic_secant_defect_threshold_row(row) for row in conic_survival_rows
    ]
    line_e72_extremal_shape = line_base_extremal_shape_row(line_base_defect_rows[0])
    conic_e69_extremal_shape = conic_secant_extremal_shape_row(conic_secant_defect_rows[0])
    line_e72_exact_root_budget_alternatives = exact_line_root_budget_alternatives(
        forced_external_core_size=72,
        locator_degree=j_value,
        external_root_count=external_root_count,
    )
    conic_e69_exact_root_budget_alternatives = exact_conic_root_budget_alternatives(
        forced_external_core_size=69,
        locator_degree=j_value,
        external_root_count=external_root_count,
    )
    line_e72_extremal_design_shapes = line_extremal_design_shapes(
        line_e72_exact_root_budget_alternatives,
        forced_external_core_size=72,
        locator_degree=j_value,
    )
    conic_e69_extremal_design_shapes = conic_extremal_design_shapes(
        conic_e69_exact_root_budget_alternatives,
        forced_external_core_size=69,
        locator_degree=j_value,
        external_root_count=external_root_count,
    )
    line_e72_design_multiplicity_profiles = line_design_multiplicity_profiles(
        line_e72_extremal_design_shapes,
        external_root_count=external_root_count,
        forced_external_core_size=72,
    )
    conic_e69_design_multiplicity_profiles = conic_design_multiplicity_profiles(
        conic_e69_extremal_design_shapes,
        external_root_count=external_root_count,
        forced_external_core_size=69,
    )
    line_e72_design_local_profiles = line_design_local_profiles(
        line_e72_extremal_design_shapes
    )
    line_e72_quotient_pencil_obstruction_rows = (
        line_e72_quotient_pencil_obstruction_profile(
            line_e72_extremal_design_shapes,
            quotient_degree=j_value - line_residual_core_threshold,
        )
    )
    conic_e69_design_local_profiles = conic_design_local_profiles(
        conic_e69_extremal_design_shapes
    )
    conic_e69_pascal_obstruction_rows = conic_e69_pascal_obstruction_profile(
        conic_e69_extremal_design_shapes
    )
    line_one_over_design_catalog_rows = line_one_over_design_catalog(
        line_incidence_one_over_cores,
        locator_degree=j_value,
        external_root_count=external_root_count,
    )
    conic_one_over_design_catalog_rows = conic_one_over_design_catalog(
        conic_pair_one_over_cores,
        locator_degree=j_value,
        external_root_count=external_root_count,
    )
    line_quotient_pencil_obstruction_catalog_rows = (
        line_quotient_pencil_obstruction_catalog(
            line_one_over_design_catalog_rows,
            locator_degree=j_value,
            external_root_count=external_root_count,
        )
    )
    conic_quotient_family_obstruction_catalog_rows = (
        conic_quotient_family_obstruction_catalog(
            conic_one_over_design_catalog_rows,
            locator_degree=j_value,
            external_root_count=external_root_count,
        )
    )
    line_exact_current_profile_rows = [
        exact_agreement_current_profile_row(row, line_exact_tail_safe_core_min)
        for row in line_cofactor_current_profile_rows
    ]
    conic_exact_current_profile_rows = [
        exact_agreement_current_profile_row(row, conic_exact_tail_safe_core_min)
        for row in conic_cofactor_current_profile_rows
    ]
    line_exact_current_profile_groups = projective_bound_profile_groups(
        line_exact_current_profile_rows
    )
    conic_exact_current_profile_groups = projective_bound_profile_groups(
        conic_exact_current_profile_rows
    )
    line_incidence_only_sharpness_witnesses = [
        first_line_incidence_only_sharpness_witness(
            core,
            locator_degree=j_value,
            external_root_count=external_root_count,
        )
        for core in line_incidence_one_over_cores
    ]
    conic_incidence_only_sharpness_witnesses = [
        first_conic_incidence_only_sharpness_witness(
            core,
            locator_degree=j_value,
            external_root_count=external_root_count,
        )
        for core in conic_pair_one_over_cores
    ]
    for row in line_incidence_only_sharpness_witnesses:
        validate_line_incidence_only_sharpness_witness(
            row,
            locator_degree=j_value,
            external_root_count=external_root_count,
        )
    for row in conic_incidence_only_sharpness_witnesses:
        validate_conic_incidence_only_sharpness_witness(
            row,
            locator_degree=j_value,
            external_root_count=external_root_count,
        )
    single_saving_closure_rows = (
        [single_saving_closure_row(row) for row in line_survival_rows]
        + [single_saving_closure_row(row) for row in conic_survival_rows]
        + [
            tangent_tail_single_saving_closure_row(row)
            for row in tangent_tail_survival_rows
        ]
    )
    exact_current_minimal_obstruction_rows = exact_current_minimal_obstruction_profile(
        line_survival_rows,
        conic_survival_rows,
        line_one_over_design_catalog_rows,
        conic_one_over_design_catalog_rows,
        single_saving_closure_rows,
    )
    mechanism_priority_rows = one_over_mechanism_priority_ledger(
        line_one_over_design_catalog_rows,
        conic_one_over_design_catalog_rows,
    )
    require(line_residual_core_threshold == 72, "line residual threshold mismatch")
    require(conic_residual_core_threshold == 69, "conic residual threshold mismatch")
    require(
        j_value - line_residual_core_threshold == 54,
        "line residual quotient degree mismatch",
    )
    require(
        j_value - conic_residual_core_threshold == 57,
        "conic residual quotient degree mismatch",
    )
    require(
        quotient_residual_rows[0]["projective_source_dimension_after_core_factor"] == 1,
        "line residual should remain a projective line after core factoring",
    )
    require(
        quotient_residual_rows[0]["forced_core_gcd_arity"] == 2,
        "line residual forced core should be a two-polynomial gcd",
    )
    require(
        quotient_residual_rows[1]["projective_source_dimension_after_core_factor"] == 2,
        "irreducible conic residual should remain a projective plane family after core factoring",
    )
    require(
        quotient_residual_rows[1]["forced_core_gcd_arity"] == 3,
        "irreducible conic residual forced core should be a three-polynomial gcd",
    )
    for row in punctured_tangent_rows:
        require(
            row["in_high_agreement_tangent_range_at_threshold"],
            f"{row['component_type']} threshold should be tangent-exact after puncturing",
        )
    require(
        punctured_tangent_rows[0]["tangent_numerator_at_threshold"] == 55,
        "line tangent numerator mismatch",
    )
    require(
        punctured_tangent_rows[1]["tangent_numerator_at_threshold"] == 58,
        "conic tangent numerator mismatch",
    )
    require(tail_projective_safe_core_min == 121, "punctured projective tangent tail threshold mismatch")
    require(
        line_cofactor_tangent_safe_core_min == 120,
        "line cofactor-improved tangent tail threshold mismatch",
    )
    require(
        conic_cofactor_tangent_safe_core_min == 120,
        "conic cofactor-improved tangent tail threshold mismatch",
    )
    require(
        line_cofactor_tangent_one_over_cores == [119],
        "line cofactor-improved tangent one-over core mismatch",
    )
    require(
        conic_cofactor_tangent_one_over_cores == [119],
        "conic cofactor-improved tangent one-over core mismatch",
    )
    require(
        line_cofactor_tangent_rows[-1]["top_saturation_excluded_by_cofactor_span"] is False,
        "line terminal tail should not need cofactor exclusion",
    )
    require(
        conic_cofactor_tangent_rows[-1]["top_saturation_excluded_by_cofactor_span"] is False,
        "conic terminal tail should not need cofactor exclusion",
    )
    require(
        not punctured_tangent_tail_rows[0]["projective_safe_by_punctured_projective_tangent"],
        "core 120 should not be projective-safe by punctured projective tangent",
    )
    require(
        punctured_tangent_tail_rows[1]["projective_bound_from_punctured_projective_tangent"]
        == PROJECTIVE_BUDGET,
        "core 121 should exactly meet the projective budget",
    )
    require(
        punctured_tangent_tail_rows[2]["projective_safe_by_punctured_projective_tangent"],
        "maximal high core should be projective-safe",
    )
    require(
        [group for group in line_profile_groups if group["one_over_budget"]]
        == [
            {
                "external_core_range": [72, 80],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
            {
                "external_core_range": [120, 120],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
        ],
        "line one-over-budget profile changed",
    )
    require(
        [group for group in conic_profile_groups if group["one_over_budget"]]
        == [
            {
                "external_core_range": [69, 76],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
            {
                "external_core_range": [120, 120],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
        ],
        "conic one-over-budget profile changed",
    )
    require(
        max(row["current_projective_upper_bound"] for row in line_intermediate_profile_rows) == 18,
        "line profile max bound changed",
    )
    require(
        max(row["current_projective_upper_bound"] for row in conic_intermediate_profile_rows)
        == 26,
        "conic profile max bound changed",
    )
    require(
        [group for group in line_cofactor_current_profile_groups if group["one_over_budget"]]
        == [
            {
                "external_core_range": [72, 80],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
            {
                "external_core_range": [119, 119],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
        ],
        "line cofactor-current one-over profile changed",
    )
    require(
        [group for group in conic_cofactor_current_profile_groups if group["one_over_budget"]]
        == [
            {
                "external_core_range": [69, 76],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
            {
                "external_core_range": [119, 119],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            },
        ],
        "conic cofactor-current one-over profile changed",
    )
    require(
        max(row["current_projective_upper_bound"] for row in line_cofactor_current_profile_rows)
        == 18,
        "line cofactor-current profile max bound changed",
    )
    require(
        max(row["current_projective_upper_bound"] for row in conic_cofactor_current_profile_rows)
        == 25,
        "conic cofactor-current profile max bound changed",
    )
    require(
        line_cofactor_current_profile_rows[-1]["forced_external_core_size"] == 120
        and line_cofactor_current_profile_rows[-1]["projective_safe"],
        "line e=120 should be safe in the cofactor-current profile",
    )
    require(
        conic_cofactor_current_profile_rows[-1]["forced_external_core_size"] == 120
        and conic_cofactor_current_profile_rows[-1]["projective_safe"],
        "conic e=120 should be safe in the cofactor-current profile",
    )
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["projective_upper_bound_after_obstruction"],
                row["finite_component_cofactor_span_dimension_at_least"],
                row["quotient_family_vector_dimension_at_most"],
            )
            for row in tangent_tail_exact_closure_rows
        ]
        == [
            *[("line", core, 6, 3 if core <= 114 else 6, 2) for core in range(109, 120)],
            *[
                ("irreducible_conic", core, 6, 6, 3)
                for core in range(115, 120)
            ],
        ],
        "exact-agreement tangent-tail closure range changed",
    )
    require(
        all(
            row["projective_safe_after_exact_agreement_obstruction"]
            and row["contradiction"]
            and max(row["private_coordinate_count_options"]) <= 2
            and (
                row["finite_component_cofactor_span_dimension_at_least"] == 3
                if row["component_type"] == "line" and row["forced_external_core_size"] <= 114
                else row["finite_component_cofactor_span_dimension_at_least"] == 6
            )
            for row in tangent_tail_exact_closure_rows
        ),
        "exact-agreement tangent-tail closure should be active",
    )
    require(
        [group for group in line_exact_current_profile_groups if group["one_over_budget"]]
        == [
            {
                "external_core_range": [72, 80],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            }
        ],
        "line exact-current one-over profile changed",
    )
    require(
        [group for group in conic_exact_current_profile_groups if group["one_over_budget"]]
        == [
            {
                "external_core_range": [69, 76],
                "current_projective_upper_bound": 7,
                "projective_safe": False,
                "one_over_budget": True,
            }
        ],
        "conic exact-current one-over profile changed",
    )
    require(
        line_exact_current_profile_groups[-1]["external_core_range"] == [109, 120]
        and line_exact_current_profile_groups[-1]["projective_safe"],
        "line exact-current tail should be safe from e=109",
    )
    require(
        conic_exact_current_profile_groups[-1]["external_core_range"] == [115, 120]
        and conic_exact_current_profile_groups[-1]["projective_safe"],
        "conic exact-current tail should be safe from e=115",
    )
    require(
        line_incidence_one_over_cores == list(range(72, 81)),
        "line incidence one-over cores changed",
    )
    require(
        conic_pair_one_over_cores == list(range(69, 77)),
        "conic pair-overlap one-over cores changed",
    )
    require(tangent_one_over_tail_cores == [120], "tangent one-over tail core changed")
    require(
        line_six_saturation_rows[0]["external_line_slack_after_minimal_six_classes"] == 1,
        "line e=72 saturation slack changed",
    )
    require(
        line_six_saturation_rows[-1]["external_line_slack_after_minimal_six_classes"] == 41,
        "line e=80 saturation slack changed",
    )
    require(
        conic_six_saturation_rows[0][
            "forced_pair_overlap_events_before_external_excess_at_least"
        ]
        == 14,
        "conic e=69 forced overlap changed",
    )
    require(
        conic_six_saturation_rows[-1][
            "forced_pair_overlap_events_before_external_excess_at_least"
        ]
        == 0,
        "conic e=76 forced overlap changed",
    )
    require(
        line_survival_rows[0]["base_pressure_label"] == "near-complete base splitting",
        "line e=72 base pressure changed",
    )
    require(
        line_survival_rows[1]["base_pressure_label"] == "positive base splitting",
        "line e=73 base pressure changed",
    )
    require(
        line_survival_rows[2]["base_pressure_label"] == "weak base splitting",
        "line e=74 base pressure changed",
    )
    require(
        line_survival_rows[-1]["base_pressure_label"]
        == "external slack alone can absorb base deficit",
        "line e=80 base pressure changed",
    )
    require(
        conic_survival_rows[0]["secant_pressure_label"] == "almost complete secant graph",
        "conic e=69 secant pressure changed",
    )
    require(
        conic_survival_rows[1]["secant_pressure_label"] == "dense secant graph",
        "conic e=70 secant pressure changed",
    )
    require(
        conic_survival_rows[2]["secant_pressure_label"] == "nontrivial secant graph",
        "conic e=71 secant pressure changed",
    )
    require(
        conic_survival_rows[-1]["secant_pressure_label"]
        == "pair-overlap pressure not forced before external excess",
        "conic e=76 secant pressure changed",
    )
    require(
        line_base_defect_rows[0]["required_total_base_root_incidences"] == 11,
        "line e=72 required base-root count changed",
    )
    require(
        line_base_defect_rows[0]["minimum_two_base_root_classes"] == 5,
        "line e=72 two-base-root threshold changed",
    )
    require(
        line_base_defect_rows[0]["maximum_zero_base_root_classes"] == 0,
        "line e=72 zero-base-root threshold changed",
    )
    require(
        line_base_defect_rows[1]["required_total_base_root_incidences"] == 6,
        "line e=73 required base-root count changed",
    )
    require(
        line_base_defect_rows[2]["required_total_base_root_incidences"] == 1,
        "line e=74 required base-root count changed",
    )
    require(
        conic_secant_defect_rows[0]["required_secant_edges_before_external_excess"] == 14,
        "conic e=69 required secants changed",
    )
    require(
        conic_secant_defect_rows[0]["maximum_missing_secants_before_external_excess"] == 1,
        "conic e=69 missing secants changed",
    )
    require(
        conic_secant_defect_rows[0]["minimum_possible_secant_triangles"] == 16,
        "conic e=69 triangle threshold changed",
    )
    require(
        conic_secant_defect_rows[1]["required_secant_edges_before_external_excess"] == 9,
        "conic e=70 required secants changed",
    )
    require(
        conic_secant_defect_rows[2]["required_secant_edges_before_external_excess"] == 4,
        "conic e=71 required secants changed",
    )
    require(
        line_e72_extremal_shape["allowed_base_root_histograms"]
        == [[0, 0, 6], [0, 1, 5]],
        "line e=72 extremal histograms changed",
    )
    require(
        conic_e69_extremal_shape["allowed_missing_secant_counts"] == [0, 1],
        "conic e=69 missing secant shape changed",
    )
    require(
        conic_e69_extremal_shape["allowed_sorted_degree_sequences"]
        == [[4, 4, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]],
        "conic e=69 degree sequences changed",
    )
    require(
        conic_e69_extremal_shape["allowed_secant_triangle_counts"] == [16, 20],
        "conic e=69 triangle counts changed",
    )
    require(
        line_e72_exact_root_budget_alternatives
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "total_base_root_incidences": 12,
                "exact_nonforced_external_root_incidences": 312,
                "unused_nonforced_external_root_lines": 1,
            },
            {
                "base_root_histogram": [0, 1, 5],
                "total_base_root_incidences": 11,
                "exact_nonforced_external_root_incidences": 313,
                "unused_nonforced_external_root_lines": 0,
            },
        ],
        "line e=72 exact root-budget alternatives changed",
    )
    require(
        conic_e69_exact_root_budget_alternatives
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "total_base_root_incidences": 12,
                "exact_nonforced_external_root_incidences_before_overlap": 330,
                "required_pair_overlaps_before_external_excess": 14,
                "maximum_missing_secants_before_external_excess": 1,
            },
            {
                "base_root_histogram": [0, 1, 5],
                "total_base_root_incidences": 11,
                "exact_nonforced_external_root_incidences_before_overlap": 331,
                "required_pair_overlaps_before_external_excess": 15,
                "maximum_missing_secants_before_external_excess": 0,
            },
        ],
        "conic e=69 exact root-budget alternatives changed",
    )
    require(
        line_e72_extremal_design_shapes
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "nonforced_external_class_sizes": [52, 52, 52, 52, 52, 52],
                "covered_nonforced_external_root_lines": 312,
                "unused_nonforced_external_root_lines": 1,
                "partition_status": "covers_all_but_one",
            },
            {
                "base_root_histogram": [0, 1, 5],
                "nonforced_external_class_sizes": [53, 52, 52, 52, 52, 52],
                "covered_nonforced_external_root_lines": 313,
                "unused_nonforced_external_root_lines": 0,
                "partition_status": "covers_all",
            },
        ],
        "line e=72 extremal design shapes changed",
    )
    require(
        conic_e69_extremal_design_shapes
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "nonforced_external_class_sizes": [55, 55, 55, 55, 55, 55],
                "secant_graph": "K6",
                "pair_overlaps": 15,
                "missing_secants": 0,
                "secant_triangles": 20,
                "covered_nonforced_external_root_lines": 315,
                "unused_nonforced_external_root_lines": 1,
                "cover_status": "covers_all_but_one",
            },
            {
                "base_root_histogram": [0, 0, 6],
                "nonforced_external_class_sizes": [55, 55, 55, 55, 55, 55],
                "secant_graph": "K6_minus_one_edge",
                "pair_overlaps": 14,
                "missing_secants": 1,
                "secant_triangles": 16,
                "covered_nonforced_external_root_lines": 316,
                "unused_nonforced_external_root_lines": 0,
                "cover_status": "covers_all",
            },
            {
                "base_root_histogram": [0, 1, 5],
                "nonforced_external_class_sizes": [56, 55, 55, 55, 55, 55],
                "secant_graph": "K6",
                "pair_overlaps": 15,
                "missing_secants": 0,
                "secant_triangles": 20,
                "covered_nonforced_external_root_lines": 316,
                "unused_nonforced_external_root_lines": 0,
                "cover_status": "covers_all",
            },
        ],
        "conic e=69 extremal design shapes changed",
    )
    require(
        line_e72_design_multiplicity_profiles
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "class_size_sequence": [52, 52, 52, 52, 52, 52],
                "available_nonforced_external_root_lines": 313,
                "multiplicity_zero_lines": 1,
                "multiplicity_one_lines": 312,
                "multiplicity_two_or_more_lines": 0,
                "pairwise_class_intersections": "all_zero",
            },
            {
                "base_root_histogram": [0, 1, 5],
                "class_size_sequence": [53, 52, 52, 52, 52, 52],
                "available_nonforced_external_root_lines": 313,
                "multiplicity_zero_lines": 0,
                "multiplicity_one_lines": 313,
                "multiplicity_two_or_more_lines": 0,
                "pairwise_class_intersections": "all_zero",
            },
        ],
        "line e=72 design multiplicity profiles changed",
    )
    require(
        conic_e69_design_multiplicity_profiles
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "secant_graph": "K6",
                "class_overlap_degree_sequence": [5, 5, 5, 5, 5, 5],
                "available_nonforced_external_root_lines": 316,
                "multiplicity_zero_lines": 1,
                "multiplicity_one_lines": 300,
                "multiplicity_two_lines": 15,
                "multiplicity_three_or_more_lines": 0,
                "reason_no_triple_use": (
                    "a nonforced external root line meets an irreducible conic "
                    "in length at most two"
                ),
            },
            {
                "base_root_histogram": [0, 0, 6],
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "secant_graph": "K6_minus_one_edge",
                "class_overlap_degree_sequence": [4, 4, 5, 5, 5, 5],
                "available_nonforced_external_root_lines": 316,
                "multiplicity_zero_lines": 0,
                "multiplicity_one_lines": 302,
                "multiplicity_two_lines": 14,
                "multiplicity_three_or_more_lines": 0,
                "reason_no_triple_use": (
                    "a nonforced external root line meets an irreducible conic "
                    "in length at most two"
                ),
            },
            {
                "base_root_histogram": [0, 1, 5],
                "class_size_sequence": [56, 55, 55, 55, 55, 55],
                "secant_graph": "K6",
                "class_overlap_degree_sequence": [5, 5, 5, 5, 5, 5],
                "available_nonforced_external_root_lines": 316,
                "multiplicity_zero_lines": 0,
                "multiplicity_one_lines": 301,
                "multiplicity_two_lines": 15,
                "multiplicity_three_or_more_lines": 0,
                "reason_no_triple_use": (
                    "a nonforced external root line meets an irreducible conic "
                    "in length at most two"
                ),
            },
        ],
        "conic e=69 design multiplicity profiles changed",
    )
    require(
        line_e72_design_local_profiles
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "class_count": 6,
                "class_size_sequence": [52, 52, 52, 52, 52, 52],
                "pair_overlap_degree_sequence": [0, 0, 0, 0, 0, 0],
                "singleton_root_line_sequence": [52, 52, 52, 52, 52, 52],
                "local_description": (
                    "each valid Q-class owns exactly its class-size many "
                    "nonforced external root lines, with pairwise disjoint "
                    "ownership"
                ),
            },
            {
                "base_root_histogram": [0, 1, 5],
                "class_count": 6,
                "class_size_sequence": [53, 52, 52, 52, 52, 52],
                "pair_overlap_degree_sequence": [0, 0, 0, 0, 0, 0],
                "singleton_root_line_sequence": [53, 52, 52, 52, 52, 52],
                "local_description": (
                    "each valid Q-class owns exactly its class-size many "
                    "nonforced external root lines, with pairwise disjoint "
                    "ownership"
                ),
            },
        ],
        "line e=72 design local profiles changed",
    )
    require(
        [
            (
                row["base_root_histogram"],
                row["quotient_degree"],
                row["nonforced_external_class_sizes"],
                row["base_root_count_sequence"],
                row["unused_nonforced_external_root_lines"],
            )
            for row in line_e72_quotient_pencil_obstruction_rows
        ]
        == [
            ([0, 0, 6], 54, [52, 52, 52, 52, 52, 52], [2, 2, 2, 2, 2, 2], 1),
            ([0, 1, 5], 54, [53, 52, 52, 52, 52, 52], [1, 2, 2, 2, 2, 2], 0),
        ],
        "line e=72 quotient-pencil obstruction profile changed",
    )
    require(
        all(
            row["every_listed_member_is_full_degree_split"]
            and row["pairwise_external_root_sets_disjoint"]
            and row["closure_if_condition_fails"]
            for row in line_e72_quotient_pencil_obstruction_rows
        ),
        "line e=72 quotient-pencil obstruction rows should be closure criteria",
    )
    require(
        conic_e69_design_local_profiles
        == [
            {
                "base_root_histogram": [0, 0, 6],
                "secant_graph": "K6",
                "class_count": 6,
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "secant_degree_sequence": [5, 5, 5, 5, 5, 5],
                "singleton_root_line_sequence": [50, 50, 50, 50, 50, 50],
                "local_description": (
                    "each valid Q-class is incident to its secant-degree many "
                    "double-use external lines and the remaining listed singleton "
                    "external lines"
                ),
            },
            {
                "base_root_histogram": [0, 0, 6],
                "secant_graph": "K6_minus_one_edge",
                "class_count": 6,
                "class_size_sequence": [55, 55, 55, 55, 55, 55],
                "secant_degree_sequence": [4, 4, 5, 5, 5, 5],
                "singleton_root_line_sequence": [51, 51, 50, 50, 50, 50],
                "local_description": (
                    "each valid Q-class is incident to its secant-degree many "
                    "double-use external lines and the remaining listed singleton "
                    "external lines"
                ),
            },
            {
                "base_root_histogram": [0, 1, 5],
                "secant_graph": "K6",
                "class_count": 6,
                "class_size_sequence": [56, 55, 55, 55, 55, 55],
                "secant_degree_sequence": [5, 5, 5, 5, 5, 5],
                "singleton_root_line_sequence": [51, 50, 50, 50, 50, 50],
                "local_description": (
                    "each valid Q-class is incident to its secant-degree many "
                    "double-use external lines and the remaining listed singleton "
                    "external lines"
                ),
            },
        ],
        "conic e=69 design local profiles changed",
    )
    require(
        [
            (
                row["base_root_histogram"],
                row["secant_graph"],
                row["missing_secants"],
                row["hamiltonian_cycle_count"],
                row["pascal_collinearity_relation_count"],
            )
            for row in conic_e69_pascal_obstruction_rows
        ]
        == [
            ([0, 0, 6], "K6", 0, 60, 60),
            ([0, 0, 6], "K6_minus_one_edge", 1, 36, 36),
            ([0, 1, 5], "K6", 0, 60, 60),
        ],
        "conic e=69 Pascal obstruction profile changed",
    )
    require(
        all(
            row["closure_if_condition_fails"]
            and row["secant_edge_count"] in {14, 15}
            for row in conic_e69_pascal_obstruction_rows
        ),
        "conic e=69 Pascal obstruction rows should be closure criteria",
    )
    require(
        line_one_over_design_catalog_rows
        == [
            {
                "forced_external_core_size": 72,
                "allowed_base_root_histogram_count": 2,
                "total_base_root_incidence_range": [11, 12],
                "unused_nonforced_external_root_line_range": [0, 1],
                "all_zero_base_root_histogram_allowed": False,
                "all_histograms_allowed": False,
            },
            {
                "forced_external_core_size": 73,
                "allowed_base_root_histogram_count": 16,
                "total_base_root_incidence_range": [6, 12],
                "unused_nonforced_external_root_line_range": [0, 6],
                "all_zero_base_root_histogram_allowed": False,
                "all_histograms_allowed": False,
            },
            {
                "forced_external_core_size": 74,
                "allowed_base_root_histogram_count": 27,
                "total_base_root_incidence_range": [1, 12],
                "unused_nonforced_external_root_line_range": [0, 11],
                "all_zero_base_root_histogram_allowed": False,
                "all_histograms_allowed": False,
            },
            {
                "forced_external_core_size": 75,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "unused_nonforced_external_root_line_range": [4, 16],
                "all_zero_base_root_histogram_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 76,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "unused_nonforced_external_root_line_range": [9, 21],
                "all_zero_base_root_histogram_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 77,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "unused_nonforced_external_root_line_range": [14, 26],
                "all_zero_base_root_histogram_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 78,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "unused_nonforced_external_root_line_range": [19, 31],
                "all_zero_base_root_histogram_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 79,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "unused_nonforced_external_root_line_range": [24, 36],
                "all_zero_base_root_histogram_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 80,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "unused_nonforced_external_root_line_range": [29, 41],
                "all_zero_base_root_histogram_allowed": True,
                "all_histograms_allowed": True,
            },
        ],
        "line one-over design catalog changed",
    )
    require(
        conic_one_over_design_catalog_rows
        == [
            {
                "forced_external_core_size": 69,
                "allowed_base_root_histogram_count": 2,
                "total_base_root_incidence_range": [11, 12],
                "required_pair_overlap_range": [14, 15],
                "maximum_missing_secant_range": [0, 1],
                "all_zero_base_root_histogram_allowed": False,
                "zero_pair_overlap_allowed": False,
                "all_histograms_allowed": False,
            },
            {
                "forced_external_core_size": 70,
                "allowed_base_root_histogram_count": 16,
                "total_base_root_incidence_range": [6, 12],
                "required_pair_overlap_range": [9, 15],
                "maximum_missing_secant_range": [0, 6],
                "all_zero_base_root_histogram_allowed": False,
                "zero_pair_overlap_allowed": False,
                "all_histograms_allowed": False,
            },
            {
                "forced_external_core_size": 71,
                "allowed_base_root_histogram_count": 27,
                "total_base_root_incidence_range": [1, 12],
                "required_pair_overlap_range": [4, 15],
                "maximum_missing_secant_range": [0, 11],
                "all_zero_base_root_histogram_allowed": False,
                "zero_pair_overlap_allowed": False,
                "all_histograms_allowed": False,
            },
            {
                "forced_external_core_size": 72,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "required_pair_overlap_range": [0, 11],
                "maximum_missing_secant_range": [4, 15],
                "all_zero_base_root_histogram_allowed": True,
                "zero_pair_overlap_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 73,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "required_pair_overlap_range": [0, 6],
                "maximum_missing_secant_range": [9, 15],
                "all_zero_base_root_histogram_allowed": True,
                "zero_pair_overlap_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 74,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "required_pair_overlap_range": [0, 1],
                "maximum_missing_secant_range": [14, 15],
                "all_zero_base_root_histogram_allowed": True,
                "zero_pair_overlap_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 75,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "required_pair_overlap_range": [0, 0],
                "maximum_missing_secant_range": [15, 15],
                "all_zero_base_root_histogram_allowed": True,
                "zero_pair_overlap_allowed": True,
                "all_histograms_allowed": True,
            },
            {
                "forced_external_core_size": 76,
                "allowed_base_root_histogram_count": 28,
                "total_base_root_incidence_range": [0, 12],
                "required_pair_overlap_range": [0, 0],
                "maximum_missing_secant_range": [15, 15],
                "all_zero_base_root_histogram_allowed": True,
                "zero_pair_overlap_allowed": True,
                "all_histograms_allowed": True,
            },
        ],
        "conic one-over design catalog changed",
    )
    require(
        [
            (
                row["forced_external_core_size"],
                row["quotient_degree"],
                row["allowed_base_root_histogram_count"],
                row["total_base_root_incidence_range"],
                row["unused_nonforced_external_root_line_range"],
                row["nonforced_external_roots_per_fiber_range"],
            )
            for row in line_quotient_pencil_obstruction_catalog_rows
        ]
        == [
            (72, 54, 2, [11, 12], [0, 1], [52, 53]),
            (73, 53, 16, [6, 12], [0, 6], [51, 53]),
            (74, 52, 27, [1, 12], [0, 11], [50, 52]),
            (75, 51, 28, [0, 12], [4, 16], [49, 51]),
            (76, 50, 28, [0, 12], [9, 21], [48, 50]),
            (77, 49, 28, [0, 12], [14, 26], [47, 49]),
            (78, 48, 28, [0, 12], [19, 31], [46, 48]),
            (79, 47, 28, [0, 12], [24, 36], [45, 47]),
            (80, 46, 28, [0, 12], [29, 41], [44, 46]),
        ],
        "line quotient-pencil obstruction catalog changed",
    )
    require(
        all(
            row["every_surviving_member_is_full_degree_split"]
            and row["pairwise_external_root_sets_disjoint"]
            and row["closure_if_condition_fails"]
            and row["hidden_non_subgroup_roots_per_member"] == 0
            for row in line_quotient_pencil_obstruction_catalog_rows
        ),
        "line quotient-pencil rows should be full-split closure criteria",
    )
    require(
        [
            (
                row["forced_external_core_size"],
                row["quotient_degree"],
                row["allowed_base_root_histogram_count"],
                row["total_base_root_incidence_range"],
                row["required_pair_overlap_range"],
                row["maximum_missing_secant_range"],
                row["nonforced_external_roots_per_member_range"],
            )
            for row in conic_quotient_family_obstruction_catalog_rows
        ]
        == [
            (69, 57, 2, [11, 12], [14, 15], [0, 1], [55, 56]),
            (70, 56, 16, [6, 12], [9, 15], [0, 6], [54, 56]),
            (71, 55, 27, [1, 12], [4, 15], [0, 11], [53, 55]),
            (72, 54, 28, [0, 12], [0, 11], [4, 15], [52, 54]),
            (73, 53, 28, [0, 12], [0, 6], [9, 15], [51, 53]),
            (74, 52, 28, [0, 12], [0, 1], [14, 15], [50, 52]),
            (75, 51, 28, [0, 12], [0, 0], [15, 15], [49, 51]),
            (76, 50, 28, [0, 12], [0, 0], [15, 15], [48, 50]),
        ],
        "conic quotient-family obstruction catalog changed",
    )
    require(
        all(
            row["every_surviving_member_is_full_degree_split"]
            and row["pairwise_external_overlap_at_most_one"]
            and row["triple_external_root_line_use_forbidden"]
            and row["closure_if_condition_fails"]
            and row["hidden_non_subgroup_roots_per_member"] == 0
            for row in conic_quotient_family_obstruction_catalog_rows
        ),
        "conic quotient-family rows should be full-split closure criteria",
    )
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["class_count"],
                row["covered_nonforced_external_root_lines"],
                row["unused_nonforced_external_root_lines"],
            )
            for row in line_incidence_only_sharpness_witnesses
        ]
        == [
            ("line", 72, 6, 312, 1),
            ("line", 73, 6, 306, 6),
            ("line", 74, 6, 300, 11),
            ("line", 75, 6, 294, 16),
            ("line", 76, 6, 288, 21),
            ("line", 77, 6, 282, 26),
            ("line", 78, 6, 276, 31),
            ("line", 79, 6, 270, 36),
            ("line", 80, 6, 264, 41),
        ],
        "line incidence-only sharpness witnesses changed",
    )
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["class_count"],
                row["pair_overlap_count"],
                row["covered_nonforced_external_root_lines"],
                row["unused_nonforced_external_root_lines"],
            )
            for row in conic_incidence_only_sharpness_witnesses
        ]
        == [
            ("irreducible_conic", 69, 6, 14, 316, 0),
            ("irreducible_conic", 70, 6, 9, 315, 0),
            ("irreducible_conic", 71, 6, 4, 314, 0),
            ("irreducible_conic", 72, 6, 0, 312, 1),
            ("irreducible_conic", 73, 6, 0, 306, 6),
            ("irreducible_conic", 74, 6, 0, 300, 11),
            ("irreducible_conic", 75, 6, 0, 294, 16),
            ("irreducible_conic", 76, 6, 0, 288, 21),
        ],
        "conic incidence-only sharpness witnesses changed",
    )
    require(
        [
            (row["component_type"], row["forced_external_core_size"], row["one_over_source"])
            for row in single_saving_closure_rows
        ]
        == [
            *[("line", core, "external incidence plus endpoint") for core in range(72, 81)],
            *[
                ("irreducible_conic", core, "pair-overlap packing plus endpoint")
                for core in range(69, 77)
            ],
            ("line", 120, "punctured projective tangent"),
            ("irreducible_conic", 120, "punctured projective tangent"),
        ],
        "single-saving closure ledger coverage changed",
    )
    require(
        all(
            row["dangerous_projective_count"] == PROJECTIVE_BUDGET + 1
            and row["safe_projective_count_after_one_saving"] == PROJECTIVE_BUDGET
            for row in single_saving_closure_rows
        ),
        "single-saving closure ledger should be exactly one over budget",
    )
    require(
        [
            (row["component_type"], row["forced_external_core_size"])
            for row in exact_current_minimal_obstruction_rows
        ]
        == [
            *[("line", core) for core in range(72, 81)],
            *[("irreducible_conic", core) for core in range(69, 77)],
        ],
        "exact-current minimal obstruction coverage changed",
    )
    require(
        all(
            row["dangerous_projective_count"] == PROJECTIVE_BUDGET + 1
            and row["finite_source_classes_must_equal"] == PROJECTIVE_BUDGET
            and row["finite_slopes_must_be_distinct"]
            and row["endpoint_must_survive_unpaid"]
            and row["status"] == "minimal exact-current finite-incidence obstruction"
            for row in exact_current_minimal_obstruction_rows
        ),
        "exact-current minimal obstructions should all require six distinct finite slopes plus endpoint",
    )
    require(
        [
            row["base_pressure_label"]
            for row in exact_current_minimal_obstruction_rows
            if row["component_type"] == "line"
        ]
        == [
            "near-complete base splitting",
            "positive base splitting",
            "weak base splitting",
            *["external slack alone can absorb base deficit"] * 6,
        ],
        "line minimal obstruction pressure labels changed",
    )
    require(
        [
            row["secant_pressure_label"]
            for row in exact_current_minimal_obstruction_rows
            if row["component_type"] == "irreducible_conic"
        ]
        == [
            "almost complete secant graph",
            "dense secant graph",
            "nontrivial secant graph",
            *["pair-overlap pressure not forced before external excess"] * 5,
        ],
        "conic minimal obstruction pressure labels changed",
    )
    require(
        [
            (
                row["mechanism_class"],
                row["component_type"],
                row["external_core_range"],
                row["core_count"],
            )
            for row in mechanism_priority_rows
        ]
        == [
            ("line_base_splitting_active", "line", [72, 74], 3),
            ("line_external_slack_only", "line", [75, 80], 6),
            (
                "conic_base_and_secant_pressure_active",
                "irreducible_conic",
                [69, 71],
                3,
            ),
            ("conic_secant_pressure_only", "irreducible_conic", [72, 74], 3),
            ("conic_endpoint_or_duplicate_only", "irreducible_conic", [75, 76], 2),
            (
                "punctured_tangent_tail_closed_by_cofactor_span",
                "line_or_irreducible_conic",
                [120, 120],
                2,
            ),
        ],
        "one-over mechanism-priority ledger changed",
    )
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["projective_saturation_count"],
                row["finite_tangent_star_common_support_size"],
                row["finite_tangent_star_residual_coordinate_count"],
            )
            for row in tangent_tail_extremizer_rows
        ]
        == [
            ("line", 120, 7, 385, 7),
            ("irreducible_conic", 120, 7, 385, 7),
        ],
        "punctured tangent tail extremizer profile changed",
    )
    require(
        all(
            row["nonbad_projective_point_available"]
            and row["residual_coordinate_to_bad_slope_bijection_required"]
            and row["tangent_gate_margin_3a_minus_2n_minus_k"] == 118
            for row in tangent_tail_extremizer_rows
        ),
        "punctured tangent tail should force the same tangent-star profile",
    )
    require(
        [
            (
                row["component_type"],
                row["forced_external_core_size"],
                row["finite_component_slope_count_at_least"],
                row["finite_component_cofactor_span_dimension_at_least"],
                row["quotient_family_vector_dimension_at_most"],
                row["projective_upper_bound_after_obstruction"],
            )
            for row in tangent_tail_cofactor_span_closure_rows
        ]
        == [
            ("line", 120, 6, 6, 2, 6),
            ("irreducible_conic", 120, 6, 6, 3, 6),
        ],
        "punctured tangent tail cofactor-span closure changed",
    )
    require(
        all(
            row["contradiction"]
            and row["projective_safe_after_cofactor_span_obstruction"]
            for row in tangent_tail_cofactor_span_closure_rows
        ),
        "punctured tangent tail should be closed by cofactor-span obstruction",
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=386 separated rank-6 moving-slope split-incidence budget",
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
            "a386_global_component_slope_dichotomy": {
                "ref": SLOPE_DICHOTOMY_REF,
                "sha256": sha256_file(SLOPE_DICHOTOMY_REF),
            },
            "a386_slope_free_containment": {
                "ref": SLOPE_FREE_REF,
                "sha256": sha256_file(SLOPE_FREE_REF),
            },
            "rank6_projective_endpoint_uniform": {
                "ref": ENDPOINT_UNIFORM_REF,
                "sha256": sha256_file(ENDPOINT_UNIFORM_REF),
            },
            "nullpolynomial_split_locator_gate": {
                "ref": NULLPOLY_SPLIT_GATE_REF,
                "sha256": sha256_file(NULLPOLY_SPLIT_GATE_REF),
            },
            "projective_tangent_staircase_note": {
                "ref": PROJECTIVE_TANGENT_REF,
                "sha256": sha256_file(PROJECTIVE_TANGENT_REF),
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
            "base_support_size": base_support_size,
            "external_root_count": external_root_count,
            "base_root_cap_per_Q": base_root_cap,
        },
        "incidence_setup": {
            "component": (
                "Let G be an irreducible positive-dimensional moving-slope "
                "component in the A=386 Q-plane, with degree c in {1,2}."
            ),
            "root_hyperplanes": (
                "For each subgroup point s in H, E_s={Q in P^2: L_Q(s)=0} "
                "is a root hyperplane for the split-locator gate."
            ),
            "forced_split_root_core": (
                "r_G is the number of subgroup points s for which G is contained "
                "in E_s; these are roots forced for every L_Q on G."
            ),
            "external_forced_split_root_core": (
                "e_G is the number of forced root hyperplanes among H\\X.  "
                "The base support X is handled separately because L_Q(x)=0 "
                "is equivalent to Q(x)=0 there."
            ),
        },
        "theorem": {
            "base_interpolation_injective": (
                "The linear map Q -> L_Q is injective: if L_Q=0 then Q vanishes "
                "on the base support X of size m=127, impossible for deg Q<3 "
                "unless Q=0."
            ),
            "base_root_cap": (
                "On the base support X, a_x L_Q(x)=Omega_x Q(x) with nonzero "
                "a_x and Omega_x.  Thus L_Q has at most two roots in X for "
                "nonzero Q, because deg Q<3."
            ),
            "no_identically_split_positive_dimensional_component": (
                "A positive-dimensional component cannot have r_G>=j=126.  "
                "Otherwise every L_Q on G would be divisible by the same degree-j "
                "split locator, hence scalar-multiple to it because deg L_Q<=j, "
                "contradicting projective injectivity of Q -> L_Q on G."
            ),
            "incidence_budget": (
                "For r_G<j, each valid degree-j split locator on G needs at least "
                "j-r_G additional intersections with non-forced root hyperplanes.  "
                "Each non-forced E_s cuts G in length at most c.  Hence the "
                "number of valid Q-classes, and therefore the number of finite "
                "slopes represented by this component, is at most "
                "floor(c*(512-r_G)/(126-r_G))."
            ),
            "base_sharpened_external_incidence_budget": (
                "Let e_G be the forced split-root core outside X.  Since each "
                "nonzero Q has at most two base-support roots, a valid degree-126 "
                "split locator needs at least 124-e_G additional roots outside X.  "
                "Each non-forced external root hyperplane cuts G in length at most "
                "c.  For e_G<124, the number of valid Q-classes, and hence finite "
                "slopes, is at most floor(c*(385-e_G)/(124-e_G))."
            ),
            "line_projective_safe_core_threshold": (
                "For a line component c=1, the unrefined all-root budget gives "
                "projective safety at r_G<=48.  The base-sharpened external "
                "budget improves this: e_G<=71 gives at most five finite "
                "Q-classes.  Adding the endpoint-uniform contribution gives "
                "projective total at most 6, exactly the projective budget."
            ),
            "conic_status": (
                "For an irreducible conic c=2, the base-sharpened budget gives "
                "six finite Q-classes at e_G=0 and finite safety through e_G<=19, "
                "but the projective endpoint still makes total seven at best.  "
                "The conic pair-overlap packing lemma below supplies the needed "
                "extra saving through e_G<=68."
            ),
            "conic_pair_overlap_packing": (
                "On an irreducible conic, two distinct Q-classes can share at most "
                "one non-forced external root hyperplane: two shared external "
                "roots would give two distinct lines through the same two points.  "
                "Thus M valid Q-classes, each requiring R=124-e_G non-forced "
                "external roots, force a union of at least M*R-binomial(M,2) "
                "external root lines.  Since only 385-e_G are available, six "
                "Q-classes are impossible for e_G<=68 and seven are impossible "
                "for e_G<=76."
            ),
            "conic_projective_safe_threshold": (
                "For irreducible conics, e_G<=68 gives at most five finite "
                "Q-classes by pair-overlap packing.  Adding the endpoint-uniform "
                "contribution gives projective total at most 6."
            ),
            "conic_remaining_residual": (
                "Irreducible conics with forced external split-root core e_G>=69 "
                "remain residual for a sharper split, paid, or exact-root-table "
                "argument."
            ),
            "high_core_quotient_normal_form": (
                "For any remaining high-core line or conic component, let E be "
                "the forced external split-root core and C_E(X)=prod_{s in E}(X-s).  "
                "Every Q-class on the component has L_Q divisible by C_E.  After "
                "factoring, L_Q=C_E R_Q with deg R_Q<=126-|E|, and the split-locator "
                "gate is exactly R_Q | (X^512-1)/C_E plus the remaining "
                "noncontainment filters.  Thus residual line components reduce "
                "to quotient degree <=54, while residual conic components reduce "
                "to quotient degree <=57."
            ),
            "high_core_forced_core_structure": (
                "The forced-core condition is a linear condition in the Q-plane.  "
                "For a line component P(U), a forced external root is exactly an "
                "external evaluation functional that vanishes on U, so C_E is a "
                "two-polynomial gcd on the line's underlying vector subspace.  "
                "For an irreducible conic, containment in a root hyperplane can "
                "only occur when the evaluation functional is zero on the whole "
                "Q-plane; hence C_E is a global common divisor of all three "
                "basis kernel polynomials."
            ),
            "punctured_high_agreement_tangent_reduction": (
                "Deleting the forced external core E leaves a punctured RS row of "
                "length n'=512-|E|, while the same witness has exact agreement "
                "386 and co-support radius r'=126-|E|.  Since r' <= floor((n'-256)/3) "
                "for |E|>=61, every remaining high-core branch lies in the "
                "very-high-agreement tangent-staircase range of the punctured row."
            ),
            "very_high_core_projective_tail_closure": (
                "The high-agreement projective tangent staircase applies to the "
                "punctured row and bounds finite plus infinity slopes together by "
                "r'+1=127-|E|.  Hence every high-core branch with |E|>=121 has "
                "projective contribution at most 6.  This closes the very-high-core "
                "tail but leaves the intermediate high-core quotient range unresolved."
            ),
            "punctured_tangent_tail_cofactor_span_closure": (
                "The remaining one-over tangent tail at e_G=120 is also closed.  "
                "If it had seven projective slopes, the tangent-star extremizer "
                "profile on the punctured row would give seven degree-6 cofactors "
                "of a seven-point residual set.  At most one of the seven projective "
                "bad points is the original endpoint, so at least six cofactors come "
                "from finite Q-classes on the component.  Any six cofactors are "
                "linearly independent by evaluation on the residual points, but the "
                "fixed-core quotient family has vector dimension at most 2 on a line "
                "component and at most 3 on an irreducible conic component.  This "
                "contradiction bounds the tail by six projective slopes."
            ),
            "cofactor_improved_tangent_tail_profile": (
                "The same cofactor-span obstruction excludes top saturation of "
                "the punctured projective tangent bound whenever the residual "
                "cofactor degree exceeds the fixed-core quotient-family dimension.  "
                "Thus the raw tangent bound r'+1 improves to r' in the high-core "
                "line/conic quotient tails until the cofactor degree drops to the "
                "ambient family dimension.  In particular e_G=120 is projective-safe "
                "for both lines and conics, while e_G=119 is the next "
                "cofactor-current one-over tangent-tail core."
            ),
            "intermediate_residual_profile": (
                "Combining the external-incidence, pair-overlap, and punctured "
                "projective tangent bounds gives a sharp current proof envelope "
                "for the unresolved intermediate cores.  The one-over-budget "
                "finite-incidence subranges are line e_G=72..80 and conic e_G=69..76.  "
                "The tangent-tail row e_G=120 is closed by the cofactor-span obstruction, "
                "and exact-agreement residual-budget splitting closes the "
                "cofactor-current tangent tail e_G=109..119 for lines and "
                "e_G=115..119 for irreducible conics; "
                "all other intermediate cores need more than a "
                "single endpoint/root saving under the present methods."
            ),
            "one_over_saturation_profile": (
                "If a one-over finite-incidence branch actually reaches six "
                "finite Q-classes, the root sets must nearly saturate the "
                "incidence inequality.  For line cores e_G=72..80 the six "
                "external root sets are pairwise disjoint and have total "
                "external excess at most 5e_G-359.  For conic cores e_G=69..76, "
                "six classes require at least max(0,359-5e_G) pair-overlap "
                "events before any external excess.  The e_G=120 cases are "
                "different: they would have to saturate the punctured projective "
                "tangent bound itself."
            ),
            "over_budget_survival_profile": (
                "A genuine over-budget witness in a one-over row must saturate "
                "the source-class bound, have six distinct finite slopes, and "
                "keep the projective endpoint unpaid.  Line cores e_G=72,73,74 "
                "also force near-complete, positive, and weak base-splitting "
                "pressure respectively.  Conic cores e_G=69,70,71 force almost "
                "complete, dense, and nontrivial external-secants respectively."
            ),
            "defect_threshold_profile": (
                "The survival pressures are converted into exact closure-by-defect "
                "thresholds.  At line e_G=72, six finite classes require at least "
                "eleven base-root incidences, so all six classes have a base root "
                "and at least five have two.  At conic e_G=69, six finite classes "
                "require at least fourteen of the fifteen pair secants before "
                "external excess, hence at least sixteen secant triangles."
            ),
            "extremal_survival_shape_profile": (
                "The extremal e_G=72 line case has only two possible base-root "
                "histograms among the six finite classes: six two-root classes, "
                "or five two-root classes plus one one-root class.  The extremal "
                "e_G=69 conic case has secant graph K6 or K6 with one missing edge."
            ),
            "exact_root_budget_alternatives": (
                "Using exact degree-126 split-locator accounting, line e_G=72 "
                "has only two alternatives: histogram (0,0,6) leaves exactly one "
                "unused nonforced external root line, while histogram (0,1,5) "
                "uses all nonforced external root lines.  For conic e_G=69, "
                "histogram (0,0,6) requires fourteen pair overlaps and histogram "
                "(0,1,5) requires all fifteen pair overlaps."
            ),
            "extremal_design_shapes": (
                "Combining the root budgets with the extremal line/conic shapes, "
                "line e_G=72 is a disjoint partition by six size-52 classes plus "
                "one unused nonforced external root line, or by one size-53 class "
                "and five size-52 classes covering all nonforced external roots.  "
                "Conic e_G=69 has only three designs: six size-55 classes with K6 "
                "and one unused root line, six size-55 classes with K6 minus one "
                "edge covering all roots, or one size-56 plus five size-55 classes "
                "with K6 covering all roots."
            ),
            "extremal_design_multiplicity_profiles": (
                "The line designs have no pairwise external overlap: their "
                "nonforced external roots have multiplicities (zero, one, >=two) "
                "equal to (1,312,0) or (0,313,0).  The conic designs have no "
                "triple external overlap, and their multiplicities (zero, one, two) "
                "are (1,300,15), (0,302,14), or (0,301,15)."
            ),
            "extremal_design_local_profiles": (
                "Locally, the line designs have singleton-root sequences "
                "(52,52,52,52,52,52) or (53,52,52,52,52,52).  The conic designs "
                "have secant-degree/singleton pairs (5^6;50^6), "
                "((4,4,5,5,5,5);(51,51,50,50,50,50)), or "
                "(5^6;(51,50,50,50,50,50))."
            ),
            "line_e72_quotient_pencil_obstruction_profile": (
                "In the extremal line e_G=72 branch, factoring the forced "
                "external core leaves a degree-54 quotient pencil.  Any remaining "
                "over-budget witness must give six distinct full-degree split "
                "members of this pencil: either six fibers with 52 external roots "
                "and two base roots each, leaving one nonforced external point "
                "unused, or one fiber with 53 external roots and one base root "
                "plus five fibers with 52 external roots and two base roots, "
                "covering all nonforced external points."
            ),
            "finite_incidence_quotient_obstruction_catalog": (
                "The same quotient-normal-form obstruction is recorded for the "
                "whole exact-current one-over finite-incidence range.  Line cores "
                "e_G=72..80 require six distinct full-split members of a quotient "
                "pencil of degrees 54 down to 46, with pairwise disjoint external "
                "fibers and one of the printed base-root histograms.  Conic cores "
                "e_G=69..76 require six full-split members on an irreducible "
                "quotient conic of degrees 57 down to 50, with the printed "
                "pair-overlap and missing-secant ranges.  If the relevant "
                "full-split quotient family does not exist, that row closes by "
                "the single-saving ledger."
            ),
            "conic_e69_pascal_obstruction_profile": (
                "In the extremal conic e_G=69 branch, the K6 and K6-minus-one "
                "secant graphs are not arbitrary incidence graphs if they come "
                "from six points on an irreducible conic.  Pascal's theorem gives "
                "one collinearity relation for every Hamiltonian cycle in the "
                "secant graph: 60 relations for K6 and 36 for K6-minus-one.  "
                "Failure of these relations in the external root-line arrangement "
                "would close the corresponding extremal conic branch."
            ),
            "one_over_design_catalog": (
                "The whole endpoint-only finite-incidence one-over range now has "
                "an exact compact catalog.  Line cores 72,73,74 allow 2,16,27 "
                "base-root histograms respectively, and line cores 75..80 allow "
                "all 28 histograms with increasing unused external slack.  Conic "
                "cores 69,70,71 allow 2,16,27 histograms respectively, while "
                "cores 72..76 allow all 28; pair-overlap pressure disappears "
                "from cores 75 and 76."
            ),
            "finite_incidence_one_over_sharpness": (
                "For every remaining one-over finite-incidence core, the current "
                "incidence axioms are sharp in an abstract set-system sense.  "
                "Line cores e_G=72..80 admit six pairwise-disjoint abstract "
                "external root classes satisfying the base-root cap and external "
                "root budget.  Conic cores e_G=69..76 admit six abstract classes "
                "whose pairwise intersections have multiplicity at most one and "
                "no triple-used external root line.  These are not Hankel "
                "realisability witnesses; they show that incidence counting "
                "alone cannot close the rows."
            ),
            "cofactor_current_residual_profile": (
                "Applying the cofactor-span top-saturation exclusion to the "
                "whole intermediate profile gives the current best projective "
                "envelope.  The previously raw one-over tail e_G=120 becomes "
                "safe, while e_G=119 becomes the next cofactor-improved "
                "tangent-tail one-over core before exact-agreement filtering.  "
                "The maximum line bound remains "
                "18, and the maximum conic bound drops from 26 to 25."
            ),
            "exact_agreement_tangent_tail_closure": (
                "The cofactor-current tangent tail is closed by exact agreement "
                "for line cores e_G=109..119 and conic cores e_G=115..119.  If "
                "seven projective slopes survived, they could be sent to seven "
                "finite slopes in the punctured row.  For residual radius r'<=17 "
                "the tangent-staircase residual-budget proof allows at most two "
                "private residual coordinates beyond the common support complement.  "
                "The cases d<r' are higher-agreement, d=r' is same-support "
                "contained at exact A, and d=r'+1 gives degree-r' cofactors of "
                "an (r'+1)-point residual set.  At least six finite component "
                "cofactors would be independent, exceeding the line/conic "
                "quotient-family dimensions 2 and 3.  In the d=r'+2 branch the "
                "six finite cofactors are six two-supported signed edge vectors.  "
                "The checked signed-incidence edge cap gives span dimension at "
                "least 3, closing line components but not conic components by "
                "dimension alone."
            ),
            "single_saving_closure_ledger": (
                "Every cofactor-current one-over row in the moving-slope packet is "
                "listed in a single-saving closure ledger.  The ledger covers "
                "line cores 72..80, conic cores 69..76, and the line/conic "
                "punctured-tangent tail at core 120.  In each row, any one listed "
                "saving lowers the projective count from 7 to the budget 6."
            ),
            "exact_current_minimal_obstruction_profile": (
                "After the component-wise exact-agreement tail closure, any remaining "
                "projective over-budget witness must be an exact-current "
                "finite-incidence obstruction: one of the line cores 72..80 or "
                "conic cores 69..76, with exactly six finite source classes, six "
                "distinct finite slopes, and an unpaid projective endpoint.  The "
                "profile records the saturated base-root, external-slack, and "
                "secant-overlap conditions that must also hold in each row."
            ),
            "one_over_mechanism_priority_ledger": (
                "The one-over rows split into six mechanism classes: line "
                "base-splitting active (72..74), line external-slack only "
                "(75..80), conic base+secant pressure active (69..71), conic "
                "secant-only pressure (72..74), conic endpoint-or-duplicate only "
                "(75..76), and the punctured tangent tail (120), now closed by "
                "the cofactor-span obstruction."
            ),
            "punctured_tangent_tail_extremizer_profile": (
                "If the e_G=120 tail actually exceeds budget, it must saturate "
                "the projective tangent staircase on the punctured row "
                "(n',a')=(392,386).  Since the projective bad set has size 7 "
                "and P^1(F) has q+1 points, a nonbad projective point can be "
                "sent to infinity.  The finite tangent-star extremizer "
                "corollary then forces a common support of size 385 and a "
                "bijection from the seven punctured residual coordinates to "
                "the seven bad projective slopes."
            ),
        },
        "budget_formula": {
            "locator_degree_j": j_value,
            "subgroup_root_count": N,
            "component_degree_c": "1 for a line, 2 for an irreducible conic",
            "forced_core_size_r": "0 <= r < j",
            "finite_Q_class_upper_bound": "floor(c*(512-r)/(126-r))",
            "finite_slope_upper_bound_reason": "the slope image cannot have more values than source Q-classes",
            "projective_total_upper_bound": "finite_Q_class_upper_bound + 1 endpoint",
        },
        "base_sharpened_budget_formula": {
            "base_support_size": base_support_size,
            "external_root_count": external_root_count,
            "base_root_cap_per_nonzero_Q": base_root_cap,
            "component_degree_c": "1 for a line, 2 for an irreducible conic",
            "forced_external_core_size_e": "0 <= e < 124",
            "finite_Q_class_upper_bound": "floor(c*(385-e)/(124-e))",
            "projective_total_upper_bound": "finite_Q_class_upper_bound + 1 endpoint",
            "residual_when_e_at_least": j_value - base_root_cap,
        },
        "safe_thresholds": {
            "line_component": {
                "unrefined_projective_safe_if_forced_core_at_most": line_projective_safe_core_max,
                "unrefined_finite_safe_if_forced_core_at_most": line_finite_safe_core_max,
                "base_sharpened_projective_safe_if_external_core_at_most": (
                    line_projective_safe_external_core_max
                ),
                "base_sharpened_finite_safe_if_external_core_at_most": (
                    line_finite_safe_external_core_max
                ),
                "projective_endpoint_added": 1,
            },
            "irreducible_conic_component": {
                "unrefined_projective_safe_for_any_core_by_this_budget": False,
                "unrefined_finite_safe_for_any_core_by_this_budget": False,
                "unrefined_smallest_finite_bound_by_this_budget": finite_q_class_bound(2, 0, j_value),
                "base_sharpened_projective_safe_for_any_external_core_by_this_budget": False,
                "base_sharpened_finite_safe_if_external_core_at_most": (
                    conic_finite_safe_external_core_max
                ),
                "base_sharpened_smallest_finite_bound_by_this_budget": (
                    external_q_class_bound(2, 0, j_value, base_root_cap, external_root_count)
                ),
                "pair_overlap_projective_safe_if_external_core_at_most": (
                    conic_projective_safe_packing_external_core_max
                ),
                "pair_overlap_finite_safe_if_external_core_at_most": (
                    conic_finite_safe_packing_external_core_max
                ),
            },
        },
        "unrefined_sample_budget_rows": unrefined_sample_rows,
        "base_sharpened_sample_budget_rows": base_sharpened_sample_rows,
        "conic_pair_overlap_sample_rows": conic_packing_sample_rows,
        "high_core_quotient_residual_rows": quotient_residual_rows,
        "punctured_tangent_reduction_rows": punctured_tangent_rows,
        "punctured_tangent_tail_rows": punctured_tangent_tail_rows,
        "cofactor_improved_tangent_tail_profile": {
            "line_rows": line_cofactor_tangent_rows,
            "irreducible_conic_rows": conic_cofactor_tangent_rows,
        },
        "intermediate_residual_profile": {
            "line_rows": line_intermediate_profile_rows,
            "line_projective_bound_groups": line_profile_groups,
            "irreducible_conic_rows": conic_intermediate_profile_rows,
            "irreducible_conic_projective_bound_groups": conic_profile_groups,
        },
        "cofactor_current_intermediate_residual_profile": {
            "line_rows": line_cofactor_current_profile_rows,
            "line_projective_bound_groups": line_cofactor_current_profile_groups,
            "irreducible_conic_rows": conic_cofactor_current_profile_rows,
            "irreducible_conic_projective_bound_groups": conic_cofactor_current_profile_groups,
        },
        "exact_current_intermediate_residual_profile": {
            "line_rows": line_exact_current_profile_rows,
            "line_projective_bound_groups": line_exact_current_profile_groups,
            "irreducible_conic_rows": conic_exact_current_profile_rows,
            "irreducible_conic_projective_bound_groups": conic_exact_current_profile_groups,
        },
        "one_over_saturation_profile": {
            "line_six_finite_saturation_rows": line_six_saturation_rows,
            "irreducible_conic_six_finite_saturation_rows": conic_six_saturation_rows,
            "punctured_tangent_tail_saturation_rows": tangent_tail_saturation_rows,
        },
        "over_budget_survival_profile": {
            "line_incidence_survival_rows": line_survival_rows,
            "irreducible_conic_pair_overlap_survival_rows": conic_survival_rows,
            "punctured_tangent_tail_survival_rows": tangent_tail_survival_rows,
        },
        "defect_threshold_profile": {
            "line_base_defect_threshold_rows": line_base_defect_rows,
            "irreducible_conic_secant_defect_threshold_rows": conic_secant_defect_rows,
        },
        "extremal_survival_shape_profile": {
            "line_e72_base_root_shape": line_e72_extremal_shape,
            "irreducible_conic_e69_secant_graph_shape": conic_e69_extremal_shape,
        },
        "exact_root_budget_alternatives": {
            "line_e72": line_e72_exact_root_budget_alternatives,
            "irreducible_conic_e69": conic_e69_exact_root_budget_alternatives,
        },
        "extremal_design_shapes": {
            "line_e72": line_e72_extremal_design_shapes,
            "irreducible_conic_e69": conic_e69_extremal_design_shapes,
        },
        "extremal_design_multiplicity_profiles": {
            "line_e72": line_e72_design_multiplicity_profiles,
            "irreducible_conic_e69": conic_e69_design_multiplicity_profiles,
        },
        "extremal_design_local_profiles": {
            "line_e72": line_e72_design_local_profiles,
            "irreducible_conic_e69": conic_e69_design_local_profiles,
        },
        "line_e72_quotient_pencil_obstruction_profile": (
            line_e72_quotient_pencil_obstruction_rows
        ),
        "conic_e69_pascal_obstruction_profile": conic_e69_pascal_obstruction_rows,
        "finite_incidence_quotient_obstruction_catalog": {
            "line_endpoint_only_incidence_range": (
                line_quotient_pencil_obstruction_catalog_rows
            ),
            "irreducible_conic_endpoint_only_incidence_range": (
                conic_quotient_family_obstruction_catalog_rows
            ),
        },
        "one_over_design_catalog": {
            "line_endpoint_only_incidence_range": line_one_over_design_catalog_rows,
            "irreducible_conic_endpoint_only_incidence_range": (
                conic_one_over_design_catalog_rows
            ),
        },
        "incidence_only_sharpness_witnesses": {
            "line_endpoint_only_incidence_range": line_incidence_only_sharpness_witnesses,
            "irreducible_conic_endpoint_only_incidence_range": (
                conic_incidence_only_sharpness_witnesses
            ),
        },
        "single_saving_closure_ledger": single_saving_closure_rows,
        "exact_current_minimal_obstruction_profile": exact_current_minimal_obstruction_rows,
        "one_over_mechanism_priority_ledger": mechanism_priority_rows,
        "punctured_tangent_tail_extremizer_profile": tangent_tail_extremizer_rows,
        "punctured_tangent_tail_cofactor_span_closure": tangent_tail_cofactor_span_closure_rows,
        "punctured_tangent_tail_exact_agreement_closure": tangent_tail_exact_closure_rows,
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
            "locator_degree_j": j_value,
            "base_root_cap_per_Q": base_root_cap,
            "external_root_count": external_root_count,
            "positive_dimensional_component_forced_core_upper_bound": j_value - 1,
            "line_projective_safe_for_external_core_at_most": line_projective_safe_external_core_max,
            "line_finite_safe_for_external_core_at_most": line_finite_safe_external_core_max,
            "line_residual_quotient_degree_at_most": j_value - line_residual_core_threshold,
            "line_residual_punctured_tangent_numerator_at_threshold": (
                punctured_tangent_rows[0]["tangent_numerator_at_threshold"]
            ),
            "line_residual_projective_safe_by_punctured_tangent_for_external_core_at_least": (
                tail_projective_safe_core_min
            ),
            "line_residual_projective_safe_after_cofactor_span_for_external_core_at_least": (
                line_cofactor_tangent_safe_core_min
            ),
            "line_residual_projective_safe_after_exact_tail_for_external_core_at_least": (
                line_exact_tail_safe_core_min
            ),
            "line_cofactor_improved_tangent_one_over_external_core": (
                line_cofactor_tangent_one_over_cores
            ),
            "line_remaining_unclosed_external_core_range": [
                line_residual_core_threshold,
                line_exact_tail_safe_core_min - 1,
            ],
            "line_one_over_budget_external_core_ranges": [
                group["external_core_range"] for group in line_profile_groups if group["one_over_budget"]
            ],
            "line_cofactor_current_one_over_external_core_ranges": [
                group["external_core_range"]
                for group in line_cofactor_current_profile_groups
                if group["one_over_budget"]
            ],
            "line_cofactor_current_safe_external_core_ranges": [
                group["external_core_range"]
                for group in line_cofactor_current_profile_groups
                if group["projective_safe"]
            ],
            "line_exact_current_one_over_external_core_ranges": [
                group["external_core_range"]
                for group in line_exact_current_profile_groups
                if group["one_over_budget"]
            ],
            "line_exact_current_safe_external_core_ranges": [
                group["external_core_range"]
                for group in line_exact_current_profile_groups
                if group["projective_safe"]
            ],
            "line_incidence_one_over_external_core_range": [
                min(line_incidence_one_over_cores),
                max(line_incidence_one_over_cores),
            ],
            "line_six_finite_saturation_external_slack_range": [
                min(
                    row["external_line_slack_after_minimal_six_classes"]
                    for row in line_six_saturation_rows
                ),
                max(
                    row["external_line_slack_after_minimal_six_classes"]
                    for row in line_six_saturation_rows
                ),
            ],
            "line_over_budget_base_pressure_core_labels": {
                str(row["forced_external_core_size"]): row["base_pressure_label"]
                for row in line_survival_rows
            },
            "line_e72_defect_thresholds": line_base_defect_rows[0],
            "line_e72_allowed_base_root_histograms": (
                line_e72_extremal_shape["allowed_base_root_histograms"]
            ),
            "line_e72_exact_root_budget_alternatives": line_e72_exact_root_budget_alternatives,
            "line_e72_extremal_design_shapes": line_e72_extremal_design_shapes,
            "line_e72_design_multiplicity_profiles": (
                line_e72_design_multiplicity_profiles
            ),
            "line_e72_design_local_profiles": line_e72_design_local_profiles,
            "line_e72_quotient_pencil_obstruction_class_sizes": [
                row["nonforced_external_class_sizes"]
                for row in line_e72_quotient_pencil_obstruction_rows
            ],
            "line_e72_quotient_pencil_obstruction_base_root_counts": [
                row["base_root_count_sequence"]
                for row in line_e72_quotient_pencil_obstruction_rows
            ],
            "line_e72_quotient_pencil_obstruction_unused_external_counts": [
                row["unused_nonforced_external_root_lines"]
                for row in line_e72_quotient_pencil_obstruction_rows
            ],
            "line_quotient_pencil_obstruction_degrees": [
                row["quotient_degree"]
                for row in line_quotient_pencil_obstruction_catalog_rows
            ],
            "line_quotient_pencil_obstruction_histogram_counts": [
                row["allowed_base_root_histogram_count"]
                for row in line_quotient_pencil_obstruction_catalog_rows
            ],
            "line_one_over_design_catalog": line_one_over_design_catalog_rows,
            "line_incidence_only_sharpness_witness_count": len(
                line_incidence_only_sharpness_witnesses
            ),
            "line_incidence_only_sharpness_external_core_range": [
                min(
                    row["forced_external_core_size"]
                    for row in line_incidence_only_sharpness_witnesses
                ),
                max(
                    row["forced_external_core_size"]
                    for row in line_incidence_only_sharpness_witnesses
                ),
            ],
            "line_intermediate_max_current_projective_upper_bound": max(
                row["current_projective_upper_bound"] for row in line_intermediate_profile_rows
            ),
            "line_cofactor_current_max_projective_upper_bound": max(
                row["current_projective_upper_bound"]
                for row in line_cofactor_current_profile_rows
            ),
            "conic_projective_safe_for_external_core_at_most": (
                conic_projective_safe_packing_external_core_max
            ),
            "conic_finite_safe_for_external_core_at_most": (
                conic_finite_safe_packing_external_core_max
            ),
            "conic_residual_quotient_degree_at_most": j_value - conic_residual_core_threshold,
            "conic_residual_punctured_tangent_numerator_at_threshold": (
                punctured_tangent_rows[1]["tangent_numerator_at_threshold"]
            ),
            "conic_residual_projective_safe_by_punctured_tangent_for_external_core_at_least": (
                tail_projective_safe_core_min
            ),
            "conic_residual_projective_safe_after_cofactor_span_for_external_core_at_least": (
                conic_cofactor_tangent_safe_core_min
            ),
            "conic_residual_projective_safe_after_exact_tail_for_external_core_at_least": (
                conic_exact_tail_safe_core_min
            ),
            "conic_cofactor_improved_tangent_one_over_external_core": (
                conic_cofactor_tangent_one_over_cores
            ),
            "conic_remaining_unclosed_external_core_range": [
                conic_residual_core_threshold,
                conic_exact_tail_safe_core_min - 1,
            ],
            "conic_one_over_budget_external_core_ranges": [
                group["external_core_range"]
                for group in conic_profile_groups
                if group["one_over_budget"]
            ],
            "conic_cofactor_current_one_over_external_core_ranges": [
                group["external_core_range"]
                for group in conic_cofactor_current_profile_groups
                if group["one_over_budget"]
            ],
            "conic_cofactor_current_safe_external_core_ranges": [
                group["external_core_range"]
                for group in conic_cofactor_current_profile_groups
                if group["projective_safe"]
            ],
            "conic_exact_current_one_over_external_core_ranges": [
                group["external_core_range"]
                for group in conic_exact_current_profile_groups
                if group["one_over_budget"]
            ],
            "conic_exact_current_safe_external_core_ranges": [
                group["external_core_range"]
                for group in conic_exact_current_profile_groups
                if group["projective_safe"]
            ],
            "conic_pair_one_over_external_core_range": [
                min(conic_pair_one_over_cores),
                max(conic_pair_one_over_cores),
            ],
            "conic_six_finite_forced_pair_overlap_range": [
                min(
                    row["forced_pair_overlap_events_before_external_excess_at_least"]
                    for row in conic_six_saturation_rows
                ),
                max(
                    row["forced_pair_overlap_events_before_external_excess_at_least"]
                    for row in conic_six_saturation_rows
                ),
            ],
            "conic_over_budget_secant_pressure_core_labels": {
                str(row["forced_external_core_size"]): row["secant_pressure_label"]
                for row in conic_survival_rows
            },
            "conic_e69_defect_thresholds": conic_secant_defect_rows[0],
            "conic_e69_allowed_missing_secant_counts": (
                conic_e69_extremal_shape["allowed_missing_secant_counts"]
            ),
            "conic_e69_allowed_secant_triangle_counts": (
                conic_e69_extremal_shape["allowed_secant_triangle_counts"]
            ),
            "conic_e69_exact_root_budget_alternatives": (
                conic_e69_exact_root_budget_alternatives
            ),
            "conic_e69_extremal_design_shapes": conic_e69_extremal_design_shapes,
            "conic_e69_design_multiplicity_profiles": (
                conic_e69_design_multiplicity_profiles
            ),
            "conic_e69_design_local_profiles": conic_e69_design_local_profiles,
            "conic_e69_pascal_obstruction_relation_counts": [
                row["pascal_collinearity_relation_count"]
                for row in conic_e69_pascal_obstruction_rows
            ],
            "conic_e69_pascal_obstruction_cycle_counts": [
                row["hamiltonian_cycle_count"]
                for row in conic_e69_pascal_obstruction_rows
            ],
            "conic_quotient_family_obstruction_degrees": [
                row["quotient_degree"]
                for row in conic_quotient_family_obstruction_catalog_rows
            ],
            "conic_quotient_family_obstruction_histogram_counts": [
                row["allowed_base_root_histogram_count"]
                for row in conic_quotient_family_obstruction_catalog_rows
            ],
            "conic_quotient_family_obstruction_pair_overlap_ranges": [
                row["required_pair_overlap_range"]
                for row in conic_quotient_family_obstruction_catalog_rows
            ],
            "conic_one_over_design_catalog": conic_one_over_design_catalog_rows,
            "conic_cofactor_current_max_projective_upper_bound": max(
                row["current_projective_upper_bound"]
                for row in conic_cofactor_current_profile_rows
            ),
            "conic_incidence_only_sharpness_witness_count": len(
                conic_incidence_only_sharpness_witnesses
            ),
            "conic_incidence_only_sharpness_external_core_range": [
                min(
                    row["forced_external_core_size"]
                    for row in conic_incidence_only_sharpness_witnesses
                ),
                max(
                    row["forced_external_core_size"]
                    for row in conic_incidence_only_sharpness_witnesses
                ),
            ],
            "single_saving_closure_ledger_count": len(single_saving_closure_rows),
            "single_saving_closure_ledger_core_ranges": {
                "line_external_incidence": [72, 80],
                "irreducible_conic_pair_overlap": [69, 76],
                "punctured_tangent_tail": [120, 120],
            },
            "exact_current_minimal_obstruction_count": len(
                exact_current_minimal_obstruction_rows
            ),
            "exact_current_minimal_obstruction_core_ranges": {
                "line_external_incidence": [72, 80],
                "irreducible_conic_pair_overlap": [69, 76],
            },
            "exact_current_minimal_obstruction_required_finite_slopes": PROJECTIVE_BUDGET,
            "exact_current_minimal_obstruction_requires_unpaid_endpoint": True,
            "one_over_mechanism_priority_classes": [
                {
                    "mechanism_class": row["mechanism_class"],
                    "component_type": row["component_type"],
                    "external_core_range": row["external_core_range"],
                    "core_count": row["core_count"],
                }
                for row in mechanism_priority_rows
            ],
            "punctured_tangent_tail_extremizer_profile": tangent_tail_extremizer_rows,
            "punctured_tangent_tail_cofactor_span_closure": (
                tangent_tail_cofactor_span_closure_rows
            ),
            "punctured_tangent_tail_exact_agreement_closure": tangent_tail_exact_closure_rows,
            "conic_intermediate_max_current_projective_upper_bound": max(
                row["current_projective_upper_bound"] for row in conic_intermediate_profile_rows
            ),
            "punctured_tangent_one_over_tail_external_core": tangent_one_over_tail_cores[0],
            "line_high_core_forced_core_is_dual_evaluation_fiber": True,
            "conic_high_core_forced_core_is_global_common_core": True,
            "remaining_unclosed_residuals": [
                "moving-slope line component with forced external split-root core in 72..108 for projective accounting",
                "irreducible moving-slope conic component with forced external split-root core in 69..114 for projective accounting",
                "possible independent noncontained vectors at slopes also admitting a slope-free vector",
            ],
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=386 has locator degree j=126 and Q-space P^2",
            "moving-slope residual is exposed by the slope-dichotomy dependency",
            "slope-free displayed vectors have already been filtered by noncontainment",
            "base interpolation Q->L_Q is injective because |X|=127>deg Q",
            "base roots satisfy L_Q(x)=0 iff Q(x)=0 and therefore at most two occur on X",
            "r_G>=126 is impossible for a positive-dimensional component",
            "incidence formula floor(c*(512-r)/(126-r)) is evaluated for c=1,2",
            "base-sharpened external incidence formula floor(c*(385-e)/(124-e)) is evaluated for c=1,2",
            "base-sharpened line projective-safe threshold is e<=71",
            "base-sharpened line finite-safe threshold is e<=80",
            "base-sharpened conic finite-safe threshold is e<=19",
            "conic pair-overlap packing excludes six Q-classes for e<=68",
            "conic pair-overlap packing excludes seven Q-classes for e<=76",
            "high-core line residuals factor through quotient locators of degree <=54",
            "high-core conic residuals factor through quotient locators of degree <=57",
            "line high-core forced roots are dual-evaluation fibers on a projective line",
            "irreducible conic high-core forced roots are global common roots of the whole Q-plane",
            "high-core residuals satisfy the punctured high-agreement tangent inequality",
            "very-high-core tail e>=121 is projective-safe by the punctured projective tangent staircase",
            "the e=120 punctured tangent tail is projective-safe by the cofactor-span obstruction",
            "cofactor-span top-saturation exclusion improves the high-core tangent bound from r'+1 to r' until the cofactor degree reaches the fixed quotient-family dimension",
            "cofactor-current residual profile makes e=120 safe and exposes e=119 before exact-tail closure",
            "exact-agreement tangent-tail closure makes line e=109..119 and conic e=115..119 projective-safe",
            "intermediate high-core residual profile is computed from the best available incidence/packing/tangent bounds",
            "one-over finite-incidence saturation conditions are computed for the endpoint-only subranges",
            "over-budget survival conditions require bound saturation, distinct finite slopes, and an unpaid endpoint",
            "line base-root and conic secant-graph defect thresholds are computed by six-class exact enumeration",
            "line e=72 and conic e=69 extremal survival shapes are classified by exact enumeration",
            "line e=72 and conic e=69 exact degree-126 root-budget alternatives are enumerated",
            "line e=72 and conic e=69 extremal finite design shapes are enumerated",
            "line e=72 and conic e=69 extremal multiplicity profiles are enumerated",
            "line e=72 and conic e=69 extremal local incidence profiles are enumerated",
            "line e=72 extremal quotient-pencil fibers are fully split degree-54 members",
            "all finite-incidence one-over line/conic rows have full-split quotient obstruction catalogs",
            "conic e=69 extremal secant graphs carry Pascal collinearity obstruction counts",
            "line and conic endpoint-only one-over finite-incidence design catalogs are enumerated",
            "abstract incidence-only sharpness witnesses are constructed for every finite-incidence one-over core",
            "every one-over moving-slope residual row has a single-saving closure ledger entry",
            "exact-current minimal obstruction profile requires six distinct finite slopes plus endpoint",
            "one-over finite-incidence moving-slope residual rows are grouped by the first available saving mechanism",
            "the e=120 one-over tail is closed by the punctured tangent-star cofactor-span obstruction",
        ],
        "nonclaims": [
            "does not prove every moving-slope component is a line",
            "does not close line components with forced external split-root core in 72..108 in projective accounting",
            "does not close irreducible conic moving-slope components with forced external split-root core in 69..114 in projective accounting",
            "does not close conic tangent-tail cores 109..114 from the signed-edge rank bound alone",
            "does not prove the high-core quotient split problem is empty or paid",
            "does not claim the punctured tangent numerator at the residual threshold is within the original row budget",
            "does not rule out another independent noncontained vector at the same finite slope",
            "does not cover A=385",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not produce a row-level M3 safe-side bound",
            "incidence-only sharpness witnesses are abstract set-system witnesses, not Hankel-realizable components",
            "incidence-only sharpness does not prove an over-budget MCA witness; it rules out closing the finite-incidence one-over rows by incidence counting alone",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=386 moving-slope split-incidence mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=386 moving-slope split-incidence budget")
    print(
        "line projective safe external core<= {line_projective_safe_for_external_core_at_most}; "
        "conic projective safe external core<= {conic_projective_safe_for_external_core_at_most}".format(
            **summary
        )
    )
    print(
        "cofactor tail safe for external core>= "
        "{line_residual_projective_safe_after_cofactor_span_for_external_core_at_least}; "
        "exact tail safe for line core>= "
        "{line_residual_projective_safe_after_exact_tail_for_external_core_at_least}, "
        "conic core>= "
        "{conic_residual_projective_safe_after_exact_tail_for_external_core_at_least}".format(
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
