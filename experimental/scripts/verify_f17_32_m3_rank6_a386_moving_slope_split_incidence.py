#!/usr/bin/env python3
"""Verify the A=386 moving-slope split-incidence budget."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a386-moving-slope-split-incidence-v2"
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
                "Conics therefore remain residual for a sharper split, paid, or "
                "exact-root-table argument."
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
            },
        },
        "unrefined_sample_budget_rows": unrefined_sample_rows,
        "base_sharpened_sample_budget_rows": base_sharpened_sample_rows,
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
            "conic_finite_safe_for_external_core_at_most": conic_finite_safe_external_core_max,
            "conic_projective_closed_by_this_incidence_budget": False,
            "remaining_unclosed_residuals": [
                "moving-slope line component with forced external split-root core >=72 for projective accounting",
                "irreducible moving-slope conic component; base-sharpened incidence is one endpoint over budget at best",
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
            "conic components are still not projective-closed by this incidence budget",
        ],
        "nonclaims": [
            "does not prove every moving-slope component is a line",
            "does not close line components with forced external split-root core >=72 in projective accounting",
            "does not close irreducible conic moving-slope components",
            "does not rule out another independent noncontained vector at the same finite slope",
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
        raise AssertionError(f"A=386 moving-slope split-incidence mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=386 moving-slope split-incidence budget")
    print(
        "line projective safe external core<= {line_projective_safe_for_external_core_at_most}; "
        "conic projective closed={conic_projective_closed_by_this_incidence_budget}".format(
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
