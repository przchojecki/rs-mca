#!/usr/bin/env python3
"""Verify the A=385 fixed two-core moving-slope incidence budget."""

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


SCHEMA_VERSION = "f17-32-m3-rank6-a385-two-core-moving-slope-incidence-v1"
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
GLOBAL_COMPONENT_REF = (
    "experimental/data/certificates/"
    "hankel-f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_global_component_slope_dichotomy.json"
)
SLOPE_FREE_REF = (
    "experimental/data/certificates/hankel-f17-32-m3-rank6-a385-two-core-slope-free-empty/"
    "f17_32_n512_k256_m3_rank6_a385_two_core_slope_free_empty.json"
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
    return component_degree * (N - forced_core_size) // (locator_degree - forced_core_size)


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
    return (
        component_degree * (external_root_count - forced_external_core_size)
        // required_external_roots
    )


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


def external_sample_row(
    component_degree: int,
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
) -> dict[str, Any]:
    required = locator_degree - base_root_cap - forced_external_core_size
    bound = external_q_class_bound(
        component_degree,
        forced_external_core_size,
        locator_degree,
        base_root_cap,
        external_root_count,
    )
    return {
        "component_degree": component_degree,
        "forced_external_core_size": forced_external_core_size,
        "base_root_cap": base_root_cap,
        "remaining_required_external_roots_per_valid_locator": required,
        "remaining_external_root_hyperplanes": external_root_count - forced_external_core_size,
        "external_incidence_capacity": (
            component_degree * (external_root_count - forced_external_core_size)
        ),
        "finite_q_class_bound": bound,
        "projective_total_with_endpoint_bound": (
            None if bound is None else bound + 1
        ),
    }


def conic_pair_overlap_row(
    forced_external_core_size: int,
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
    finite_target: int,
) -> dict[str, Any]:
    required = locator_degree - base_root_cap - forced_external_core_size
    require(required > 0, "pair-overlap row requires non-forced external roots")
    min_union = finite_target * required - finite_target * (finite_target - 1) // 2
    available = external_root_count - forced_external_core_size
    return {
        "component": "irreducible_conic",
        "forced_external_core_size": forced_external_core_size,
        "finite_target_q_classes": finite_target,
        "required_nonforced_external_roots_per_class": required,
        "minimum_union_size_after_pair_overlap": min_union,
        "available_nonforced_external_root_lines": available,
        "target_q_classes_impossible": min_union > available,
    }


def max_conic_pair_overlap_core(
    locator_degree: int,
    base_root_cap: int,
    external_root_count: int,
    finite_target: int,
) -> int:
    safe_values = []
    for core in range(locator_degree - base_root_cap):
        row = conic_pair_overlap_row(
            core,
            locator_degree,
            base_root_cap,
            external_root_count,
            finite_target,
        )
        if row["target_q_classes_impossible"]:
            safe_values.append(core)
    require(safe_values, "no pair-overlap safe values")
    return max(safe_values)


def build_certificate() -> dict[str, Any]:
    descriptor = load_json(ROW_DESCRIPTOR_REF)
    low_degree = load_json(LOW_DEGREE_TRANSFER_REF)
    global_component = load_json(GLOBAL_COMPONENT_REF)
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
    require(AGREEMENT in low_degree["window"]["agreements"], "A=385 not in transfer packet")
    require(
        global_component["schema_version"]
        == "f17-32-m3-rank6-a385-two-core-global-component-slope-dichotomy-v1",
        "A385 two-core global-component schema mismatch",
    )
    require(
        "fixed two-core determined nonconstant slope map"
        in global_component["summary"]["remaining_residuals"],
        "moving-slope residual is not exposed by global-component dependency",
    )
    require(
        slope_free["schema_version"] == "f17-32-m3-rank6-a385-two-core-slope-free-empty-v1",
        "A385 two-core slope-free schema mismatch",
    )
    require(
        slope_free["summary"]["remaining_residual"]
        == "fixed two-core determined nonconstant slope map",
        "slope-free dependency did not isolate the moving-slope residual",
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
    residual_vector_dimension = h_value - BASE_CORE_SIZE
    residual_projective_dimension = residual_vector_dimension - 1
    base_support_size = m_value
    external_root_count = N - base_support_size
    base_root_cap = BASE_CORE_SIZE + (residual_vector_dimension - 1)
    required_external_roots_no_forced_core = j_value - base_root_cap
    require(j_value == 127, "A=385 locator degree changed")
    require(h_value == 5, "A=385 boundary defect should be five")
    require(residual_vector_dimension == 3, "fixed two-core residual dimension changed")
    require(residual_projective_dimension == 2, "fixed two-core residual should be P^2")
    require(base_support_size == 128, "base support size changed")
    require(external_root_count == 384, "external root count changed")
    require(base_root_cap == 4, "fixed two-core base root cap changed")
    require(required_external_roots_no_forced_core == 123, "external root demand changed")

    transfer_record = next(
        record for record in low_degree["agreement_records"] if record["A"] == AGREEMENT
    )
    require(transfer_record["boundary_defect_h"] == h_value, "transfer h mismatch")
    require(
        transfer_record["finite_root_transfer"]["projective_Q_search_dimension"] == 4,
        "A=385 Q-space should be projective dimension four before core reduction",
    )

    line_projective_safe_core_max = max_core_for_bound(1, j_value, PROJECTIVE_BUDGET - 1)
    line_finite_safe_core_max = max_core_for_bound(1, j_value, FINITE_BUDGET)
    line_projective_safe_external_core_max = max_external_core_for_bound(
        1,
        j_value,
        base_root_cap,
        external_root_count,
        PROJECTIVE_BUDGET - 1,
    )
    line_finite_safe_external_core_max = max_external_core_for_bound(
        1,
        j_value,
        base_root_cap,
        external_root_count,
        FINITE_BUDGET,
    )
    conic_finite_safe_external_core_max = max_external_core_for_bound(
        2,
        j_value,
        base_root_cap,
        external_root_count,
        FINITE_BUDGET,
    )
    conic_pair_overlap_projective_safe_max = max_conic_pair_overlap_core(
        j_value,
        base_root_cap,
        external_root_count,
        PROJECTIVE_BUDGET,
    )
    conic_pair_overlap_finite_safe_max = max_conic_pair_overlap_core(
        j_value,
        base_root_cap,
        external_root_count,
        FINITE_BUDGET + 1,
    )
    require(line_projective_safe_core_max == 49, "unrefined line threshold changed")
    require(line_finite_safe_core_max == 62, "unrefined line finite threshold changed")
    require(line_projective_safe_external_core_max == 70, "line projective external threshold changed")
    require(line_finite_safe_external_core_max == 79, "line finite external threshold changed")
    require(conic_finite_safe_external_core_max == 18, "conic finite external threshold changed")
    require(
        conic_pair_overlap_projective_safe_max == 67,
        "conic pair-overlap projective threshold changed",
    )
    require(
        conic_pair_overlap_finite_safe_max == 75,
        "conic pair-overlap finite threshold changed",
    )

    line_sample_rows = [
        external_sample_row(1, core, j_value, base_root_cap, external_root_count)
        for core in [70, 71, 79, 80]
    ]
    conic_sample_rows = [
        external_sample_row(2, core, j_value, base_root_cap, external_root_count)
        for core in [0, 18, 19]
    ]
    conic_pair_rows = [
        conic_pair_overlap_row(core, j_value, base_root_cap, external_root_count, 6)
        for core in [67, 68]
    ] + [
        conic_pair_overlap_row(core, j_value, base_root_cap, external_root_count, 7)
        for core in [75, 76]
    ]
    require(line_sample_rows[0]["finite_q_class_bound"] == 5, "line e=70 sample mismatch")
    require(line_sample_rows[1]["finite_q_class_bound"] == 6, "line e=71 sample mismatch")
    require(conic_pair_rows[0]["target_q_classes_impossible"], "conic e=67 should be safe")
    require(not conic_pair_rows[1]["target_q_classes_impossible"], "conic e=68 should survive this test")

    return {
        "schema_version": SCHEMA_VERSION,
        "status": "PROVED / AUDIT",
        "object": "A=385 separated rank-6 fixed two-core moving-slope incidence budget",
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
            "a385_two_core_global_component_slope_dichotomy": {
                "ref": GLOBAL_COMPONENT_REF,
                "sha256": sha256_file(GLOBAL_COMPONENT_REF),
            },
            "a385_two_core_slope_free_empty": {
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
            "projective_Q_search_dimension_before_core": 4,
            "forced_base_core_size": BASE_CORE_SIZE,
            "residual_vector_dimension_after_core": residual_vector_dimension,
            "projective_Q_search_dimension_after_core": residual_projective_dimension,
            "base_support_size": base_support_size,
            "external_root_count": external_root_count,
            "split_locator_degree": j_value,
            "base_root_cap_per_Q": base_root_cap,
            "required_external_roots_without_forced_external_core": (
                required_external_roots_no_forced_core
            ),
        },
        "incidence_setup": {
            "component": (
                "Let G be an irreducible positive-dimensional fixed two-core "
                "moving-slope component in the residual Q-plane, with degree "
                "c in {1,2}."
            ),
            "root_hyperplanes": (
                "For each subgroup point s in H, E_s={R in P^2: L_{E R}(s)=0} "
                "is a root hyperplane for the split-locator gate."
            ),
            "external_forced_split_root_core": (
                "e_G is the number of forced root hyperplanes among H\\X.  "
                "The fixed two-point base core and the residual R-roots on X "
                "are counted separately."
            ),
        },
        "theorem": {
            "base_interpolation_injective": (
                "The linear map R -> L_{E R} is injective: if L_{E R}=0, then "
                "E(x)R(x)=0 for every x in the base support X.  Outside the "
                "two fixed core nodes, E(x) is nonzero, so R has 126 roots; "
                "deg R<3 forces R=0."
            ),
            "base_root_cap": (
                "On X, a_x L_{E R}(x)=Omega_x E(x)R(x).  Every candidate has "
                "the two fixed base-core roots, and nonzero R has at most two "
                "further roots on X.  Thus a valid degree-127 split locator "
                "has at most four base-support roots and must get at least "
                "123-e_G non-forced external roots."
            ),
            "incidence_budget": (
                "For e_G<123, each valid split locator on G needs at least "
                "123-e_G additional non-forced external root hyperplanes.  "
                "Each such hyperplane cuts G in length at most c.  Hence the "
                "number of valid Q-classes, and therefore finite slopes, is at "
                "most floor(c*(384-e_G)/(123-e_G))."
            ),
            "line_projective_safe_threshold": (
                "For a line component c=1, e_G<=70 gives at most five finite "
                "Q-classes.  Adding the endpoint-uniform contribution gives "
                "projective total at most 6, the projective budget."
            ),
            "line_finite_only_threshold": (
                "The same line incidence budget gives finite safety through "
                "e_G<=79.  The projective one-over diagnostic range left by "
                "incidence alone is 71<=e_G<=79."
            ),
            "conic_pair_overlap_packing": (
                "On an irreducible conic, two distinct Q-classes can share at "
                "most one non-forced external root hyperplane.  Thus M valid "
                "classes, each requiring R=123-e_G non-forced external roots, "
                "use at least M*R-binomial(M,2) external root lines.  Since "
                "only 384-e_G are available, six classes are impossible for "
                "e_G<=67 and seven are impossible for e_G<=75."
            ),
            "conic_projective_safe_threshold": (
                "For an irreducible conic, the pair-overlap saving gives at "
                "most five finite classes for e_G<=67.  Adding the endpoint "
                "gives projective total at most 6."
            ),
            "remaining_high_core_residual": (
                "This packet is an incidence budget only.  It leaves the line "
                "range e_G>=71 and conic range e_G>=68 for product-collapse, "
                "quotient, tangent-tail, or split-locator analysis."
            ),
        },
        "thresholds": {
            "unrefined_all_root_line_projective_safe_if_forced_core_at_most": (
                line_projective_safe_core_max
            ),
            "unrefined_all_root_line_finite_safe_if_forced_core_at_most": (
                line_finite_safe_core_max
            ),
            "line_projective_safe_if_external_core_at_most": (
                line_projective_safe_external_core_max
            ),
            "line_finite_safe_if_external_core_at_most": (
                line_finite_safe_external_core_max
            ),
            "line_projective_one_over_diagnostic_external_core_range": [71, 79],
            "conic_base_incidence_finite_safe_if_external_core_at_most": (
                conic_finite_safe_external_core_max
            ),
            "conic_pair_overlap_projective_safe_if_external_core_at_most": (
                conic_pair_overlap_projective_safe_max
            ),
            "conic_pair_overlap_finite_safe_if_external_core_at_most": (
                conic_pair_overlap_finite_safe_max
            ),
            "conic_projective_one_over_diagnostic_external_core_range": [68, 75],
            "external_incidence_formula_valid_for_e_G_at_most": (
                required_external_roots_no_forced_core - 1
            ),
        },
        "line_external_incidence_sample_rows": line_sample_rows,
        "conic_external_incidence_sample_rows": conic_sample_rows,
        "conic_pair_overlap_sample_rows": conic_pair_rows,
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
            "forced_base_core_size": BASE_CORE_SIZE,
            "base_root_cap_per_Q": base_root_cap,
            "external_root_count": external_root_count,
            "required_external_roots_without_forced_external_core": (
                required_external_roots_no_forced_core
            ),
            "line_projective_safe_external_core_max": line_projective_safe_external_core_max,
            "line_finite_safe_external_core_max": line_finite_safe_external_core_max,
            "conic_pair_overlap_projective_safe_external_core_max": (
                conic_pair_overlap_projective_safe_max
            ),
            "conic_pair_overlap_finite_safe_external_core_max": (
                conic_pair_overlap_finite_safe_max
            ),
            "line_projective_one_over_diagnostic_external_core_range": [71, 79],
            "conic_projective_one_over_diagnostic_external_core_range": [68, 75],
            "remaining_residual_after_incidence": (
                "fixed two-core moving-slope high-core line/conic branches"
            ),
        },
        "checks": [
            "row descriptor and dependency schemas match",
            "A=385 fixed two-core residual has Q-plane P^2 and locator degree 127",
            "slope-free dependency leaves only the determined nonconstant moving-slope residual",
            "base interpolation R->L_{E R} is injective",
            "base roots are capped by two fixed core roots plus at most two residual R-roots",
            "external incidence formula floor(c*(384-e)/(123-e)) is evaluated for c=1,2",
            "line projective-safe threshold is e<=70",
            "line finite-safe threshold is e<=79",
            "conic pair-overlap packing excludes six Q-classes for e<=67",
            "conic pair-overlap packing excludes seven Q-classes for e<=75",
        ],
        "nonclaims": [
            "does not close the full fixed two-core nonconstant moving-slope branch",
            "does not prove product collapse for A=385 high-core line or conic components",
            "does not claim the high-core quotient diagnostic problems are empty or paid",
            "does not prove that every A=385 over-budget branch has a fixed two-point base core",
            "does not close moving-core or no-common-core A=385 branches",
            "does not classify overlapping-support rank-6 pencils",
            "does not prove endpoint payment; it uses endpoint-budget accounting",
            "does not produce a row-level M3 safe-side bound",
        ],
    }


def check_certificate(path: Path, certificate: dict[str, Any]) -> None:
    expected = render(certificate)
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(f"A=385 two-core moving-slope incidence mismatch: {path}")


def print_summary(certificate: dict[str, Any]) -> None:
    summary = certificate["summary"]
    print("F_17^32 M3 rank-6 A=385 fixed two-core moving-slope incidence")
    print(
        "line projective safe e<={line_projective_safe_external_core_max}; conic projective safe e<={conic_pair_overlap_projective_safe_external_core_max}".format(
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
