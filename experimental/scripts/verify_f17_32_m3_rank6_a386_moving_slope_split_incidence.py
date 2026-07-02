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


SCHEMA_VERSION = "f17-32-m3-rank6-a386-moving-slope-split-incidence-v21"
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
            "mechanism_class": "punctured_tangent_tail",
            "component_type": "line_or_irreducible_conic",
            "external_core_range": [120, 120],
            "core_count": 2,
            "primary_remaining_savings": [
                "punctured tangent slope absent",
                "duplicate slope after returning to original branch",
                "slope paid by tangent, quotient, extension, or containment",
            ],
        },
    ]


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
    conic_e69_design_local_profiles = conic_design_local_profiles(
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
    single_saving_closure_rows = (
        [single_saving_closure_row(row) for row in line_survival_rows]
        + [single_saving_closure_row(row) for row in conic_survival_rows]
        + [
            tangent_tail_single_saving_closure_row(row)
            for row in tangent_tail_survival_rows
        ]
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
            ("punctured_tangent_tail", "line_or_irreducible_conic", [120, 120], 2),
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
            "intermediate_residual_profile": (
                "Combining the external-incidence, pair-overlap, and punctured "
                "projective tangent bounds gives a sharp current proof envelope "
                "for the unresolved intermediate cores.  The one-over-budget "
                "subranges are line e_G=72..80 and e_G=120, and conic e_G=69..76 "
                "and e_G=120; all other intermediate cores need more than a "
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
            "one_over_design_catalog": (
                "The whole endpoint-only finite-incidence one-over range now has "
                "an exact compact catalog.  Line cores 72,73,74 allow 2,16,27 "
                "base-root histograms respectively, and line cores 75..80 allow "
                "all 28 histograms with increasing unused external slack.  Conic "
                "cores 69,70,71 allow 2,16,27 histograms respectively, while "
                "cores 72..76 allow all 28; pair-overlap pressure disappears "
                "from cores 75 and 76."
            ),
            "single_saving_closure_ledger": (
                "Every currently one-over row in the moving-slope packet is "
                "listed in a single-saving closure ledger.  The ledger covers "
                "line cores 72..80, conic cores 69..76, and the line/conic "
                "punctured-tangent tail at core 120.  In each row, any one listed "
                "saving lowers the projective count from 7 to the budget 6."
            ),
            "one_over_mechanism_priority_ledger": (
                "The one-over rows split into six mechanism classes: line "
                "base-splitting active (72..74), line external-slack only "
                "(75..80), conic base+secant pressure active (69..71), conic "
                "secant-only pressure (72..74), conic endpoint-or-duplicate only "
                "(75..76), and the punctured tangent tail (120)."
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
        "intermediate_residual_profile": {
            "line_rows": line_intermediate_profile_rows,
            "line_projective_bound_groups": line_profile_groups,
            "irreducible_conic_rows": conic_intermediate_profile_rows,
            "irreducible_conic_projective_bound_groups": conic_profile_groups,
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
        "one_over_design_catalog": {
            "line_endpoint_only_incidence_range": line_one_over_design_catalog_rows,
            "irreducible_conic_endpoint_only_incidence_range": (
                conic_one_over_design_catalog_rows
            ),
        },
        "single_saving_closure_ledger": single_saving_closure_rows,
        "one_over_mechanism_priority_ledger": mechanism_priority_rows,
        "punctured_tangent_tail_extremizer_profile": tangent_tail_extremizer_rows,
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
            "line_remaining_unclosed_external_core_range": [
                line_residual_core_threshold,
                tail_projective_safe_core_min - 1,
            ],
            "line_one_over_budget_external_core_ranges": [
                group["external_core_range"] for group in line_profile_groups if group["one_over_budget"]
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
            "line_one_over_design_catalog": line_one_over_design_catalog_rows,
            "line_intermediate_max_current_projective_upper_bound": max(
                row["current_projective_upper_bound"] for row in line_intermediate_profile_rows
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
            "conic_remaining_unclosed_external_core_range": [
                conic_residual_core_threshold,
                tail_projective_safe_core_min - 1,
            ],
            "conic_one_over_budget_external_core_ranges": [
                group["external_core_range"]
                for group in conic_profile_groups
                if group["one_over_budget"]
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
            "conic_one_over_design_catalog": conic_one_over_design_catalog_rows,
            "single_saving_closure_ledger_count": len(single_saving_closure_rows),
            "single_saving_closure_ledger_core_ranges": {
                "line_external_incidence": [72, 80],
                "irreducible_conic_pair_overlap": [69, 76],
                "punctured_tangent_tail": [120, 120],
            },
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
            "conic_intermediate_max_current_projective_upper_bound": max(
                row["current_projective_upper_bound"] for row in conic_intermediate_profile_rows
            ),
            "punctured_tangent_one_over_tail_external_core": tangent_one_over_tail_cores[0],
            "line_high_core_forced_core_is_dual_evaluation_fiber": True,
            "conic_high_core_forced_core_is_global_common_core": True,
            "remaining_unclosed_residuals": [
                "moving-slope line component with forced external split-root core in 72..120 for projective accounting",
                "irreducible moving-slope conic component with forced external split-root core in 69..120 for projective accounting",
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
            "intermediate high-core residual profile is computed from the best available incidence/packing/tangent bounds",
            "one-over finite-incidence saturation conditions are computed for the endpoint-only subranges",
            "over-budget survival conditions require bound saturation, distinct finite slopes, and an unpaid endpoint",
            "line base-root and conic secant-graph defect thresholds are computed by six-class exact enumeration",
            "line e=72 and conic e=69 extremal survival shapes are classified by exact enumeration",
            "line e=72 and conic e=69 exact degree-126 root-budget alternatives are enumerated",
            "line e=72 and conic e=69 extremal finite design shapes are enumerated",
            "line e=72 and conic e=69 extremal multiplicity profiles are enumerated",
            "line e=72 and conic e=69 extremal local incidence profiles are enumerated",
            "line and conic endpoint-only one-over finite-incidence design catalogs are enumerated",
            "every one-over moving-slope residual row has a single-saving closure ledger entry",
            "one-over moving-slope residual rows are grouped by the first available saving mechanism",
            "the e=120 one-over tail is sharpened to a punctured projective tangent-star extremizer profile",
        ],
        "nonclaims": [
            "does not prove every moving-slope component is a line",
            "does not close line components with forced external split-root core in 72..120 in projective accounting",
            "does not close irreducible conic moving-slope components with forced external split-root core in 69..120 in projective accounting",
            "does not prove the high-core quotient split problem is empty or paid",
            "does not claim the punctured tangent numerator at the residual threshold is within the original row budget",
            "does not rule out another independent noncontained vector at the same finite slope",
            "does not cover A=385",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment",
            "does not exclude the punctured tangent-star extremizer profile at e_G=120",
            "does not produce a row-level M3 safe-side bound",
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
        "punctured projective tangent tail safe for external core>= "
        "{line_residual_projective_safe_by_punctured_tangent_for_external_core_at_least}".format(
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
