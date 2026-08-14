#!/usr/bin/env python3
"""Independent replay of the rank-11 component and split-pencil constants."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from math import comb, isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-dense-locator-split-pencil-v1/manifest.json"
PAIRCORE_SOURCE = {
    "id": "rate_half_mca_rank11_rank9_split_pencil_paircore_dichotomy",
    "path": "background/nodes/rate_half_mca_rank11_rank9_split_pencil_paircore_dichotomy",
    "commit": "0e547404a4426b9c2e5672d44b7f23e726756e01",
    "tree": "a74872d50f946260fc65c6a798e069d6e17ace59",
    "contract_sha256": "e899fbb6893e61495371f689f6a2ca5eb196d0bbc6d6ec8dc39b34eb9965c252",
}
FIXED_CHART_SOURCES = {
    "component_star_large_owner_uniqueness": {
        "id": "rate_half_mca_rank11_component_star_large_owner_uniqueness",
        "path": "background/nodes/rate_half_mca_rank11_component_star_large_owner_uniqueness",
        "commit": "b6f4705196e52e0940d592ca21363d9fd8a920b2",
        "tree": "4c8d49092349cc1c78c265be3845d5a526144b25",
        "contract_sha256": "731e65b2926b11ef0d192e11fb55e5eac280e0d93038270fe131d79b9ca7b076",
    },
    "component_ninesubset_concentrator": {
        "id": "rate_half_mca_rank11_component_ninesubset_lane_concentrator",
        "path": "background/nodes/rate_half_mca_rank11_component_ninesubset_lane_concentrator",
        "commit": "1ae1bb841771f40c4b6e74cf6a1954595237de1e",
        "tree": "4cae12dccd27f70f9373a746f763805d9b59f0dd",
        "contract_sha256": "f3e7cebc5b859df1d9950ca5cf49c085a994b91c949da3e49fbe701ffe169192",
    },
    "rank9_ninecell_paircore": {
        "id": "rate_half_mca_rank11_rank9_ninecell_paircore_extension",
        "path": "background/nodes/rate_half_mca_rank11_rank9_ninecell_paircore_extension",
        "commit": "1ae1bb841771f40c4b6e74cf6a1954595237de1e",
        "tree": "bf907dcbd67a65b2d6f51bbcbb6ad0df49da5789",
        "contract_sha256": "8d91c142853cbc92720abb7372d677287dd1e83d3755e12361d322a617d2fe78",
    },
    "component_ninesubset_targets": {
        "id": "rate_half_mca_rank11_component_ninesubset_target_router",
        "path": "background/nodes/rate_half_mca_rank11_component_ninesubset_target_router",
        "commit": "1ae1bb841771f40c4b6e74cf6a1954595237de1e",
        "tree": "4b2ba55d7280db1378e17e05a9d59217630c544e",
        "contract_sha256": "6bcbfc8f5ae87e892898137660af54014a48c57f5d55295327923af6ab5f6e4b",
    },
    "rank9_fixed_chart_local_cap_fence": {
        "id": "rate_half_mca_rank11_rank9_fixed_chart_local_cap_fence",
        "path": "background/nodes/rate_half_mca_rank11_rank9_fixed_chart_local_cap_fence",
        "commit": "3004fb4628bda19a33b9de4de3ffaa1c646c24e7",
        "tree": "dd42039516fc8ef146fa37a0fd3d7b00baf1f95c",
        "contract_sha256": "1cb156081477cb7438193899419d8c537054a9ee4570d5f6fdb5ec03868cdeca",
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def independent_binomial_ratio(k_value: int) -> Fraction:
    ratio = Fraction(198, 1)
    for index in range(11):
        ratio *= Fraction(1048576 + k_value - index, 67472 + k_value - index)
    return ratio


def affine_plane_design(field: int = 7) -> tuple[int, int, int]:
    points = [(a, b) for a in range(field) for b in range(field)]
    slopes = list(range(field))
    # Nonparallel lines alpha+gamma*beta=gamma^2.
    lines = {
        gamma: {
            (a, b)
            for a, b in points
            if (a + gamma * b - gamma * gamma) % field == 0
        }
        for gamma in slopes
    }
    for left, right in combinations(slopes, 2):
        require(len(lines[left] & lines[right]) == 1, "unique pairwise owner")
    multiplicities = {
        point: sum(point in lines[gamma] for gamma in slopes) for point in points
    }
    design_pairs = sum(comb(value, 2) for value in multiplicities.values())
    require(design_pairs == comb(len(slopes), 2), "pairwise-balanced design")

    # Off a root of u, evaluation identifies exactly one owner point.
    targets = {(a, b): (a + 2, b + 3) for a, b in points}
    require(len(set(targets.values())) == field * field, "unique off-root petals")
    return len(points), len(slopes), design_pairs


def main() -> None:
    data = json.loads(MANIFEST.read_text())
    component = data["component_incidence"]
    star = data["component_star"]
    owner_unique = data["component_star_large_owner_uniqueness"]
    cell = data["rank9_split_pencil_cell"]
    paircore = data["rank9_split_pencil_paircore"]
    concentrator = data["component_ninesubset_concentrator"]
    ninecell = data["rank9_ninecell_paircore"]
    targets = data["component_ninesubset_targets"]
    local_fence = data["rank9_fixed_chart_local_cap_fence"]
    require(
        data["source_prize_dag"]["nodes"]["rank9_split_pencil_paircore"]
        == PAIRCORE_SOURCE,
        "pair-core source pin",
    )
    require(
        {
            key: data["source_prize_dag"]["nodes"][key]
            for key in FIXED_CHART_SOURCES
        }
        == FIXED_CHART_SOURCES,
        "fixed-chart source pins",
    )

    endpoint = ceiling(independent_binomial_ratio(10))
    require(endpoint == 2526815879272440, "isolated endpoint")
    for k_value in (11, 100, 4923, 1048576):
        # Every factor decreases because 1048576>67472.
        require(independent_binomial_ratio(k_value) < independent_binomial_ratio(10), "strict endpoint")
    require(endpoint == component["isolated_equivalent_ceiling"], "manifest endpoint")

    non_dense = 274980728111395087 + 1 - 134944 - 18
    isolated_ppb = ceiling(Fraction(endpoint * 10**9, non_dense))
    require(isolated_ppb == 9189066, "isolated ppb")
    component_ppb = 10**9 - isolated_ppb
    require(component_ppb == component["component_incidence_ppb_floor"], "component ppb")

    record_fraction = Fraction(component_ppb, 10**9) - Fraction(98, 100)
    record_fraction /= Fraction(2, 100)
    require(record_fraction == Fraction(540546700, 10**9), "record fraction")
    records = ceiling(non_dense * record_fraction)
    require(records == star["threshold_record_floor"] == 148639925144138894, "record floor")

    m_max = 67472 + 1048576
    extensions = ceiling(Fraction(98 * (m_max - 10), 100))
    require(m_max - 10 - extensions == star["full_rank_owner_deficiency_ceiling"] == 22320, "owner deficiency")
    require(extensions - (1048576 - 11) == star["rank9_extension_floor"] == 45153, "pencil extensions")
    owner_deficiency = star["full_rank_owner_deficiency_ceiling"]
    root_gap = (67472 + 10 - 2 * owner_deficiency) - (10 - 1)
    require(root_gap == 22833, "owner uniqueness root gap")
    require(owner_unique == {
        "large_owner_deficiency_ceiling": owner_deficiency,
        "two_owner_deficiency_sum": 2 * owner_deficiency,
        "distance_margin_after_two_owners": 67472 - 2 * owner_deficiency,
        "intersection_over_root_cap": root_gap,
        "owner_count_per_record": 1,
    }, "owner uniqueness constants")

    owner_cap = 2097152 - m_max + 1
    weighted = owner_cap * (2097152 - 10)
    fixed_cell = weighted // 45153
    require(owner_cap == cell["fixed_owner_slope_cap"] == 981105, "owner slope cap")
    require(weighted == cell["weighted_petal_incidence_cap"] == 2057516501910, "petal cap")
    require(cell["source_weak_ceiling_cap"] == ceiling(Fraction(weighted, 45153)) == 45567659, "source ceiling")
    require(fixed_cell == cell["sharp_fixed_cell_record_cap"] == 45567658, "sharp fixed-cell cap")
    require(cell["rounding_rule"].startswith("floor"), "rounding rule")

    n = 2097152
    m = 1116048
    common_core = 2 * m - n - 1
    coefficient = n - m + 1
    ordered_resource = coefficient * (n - 10)
    plane_cap = (1 + isqrt(1 + 4 * ordered_resource)) // 2
    next_integer_fails_by = (plane_cap + 1) * plane_cap - ordered_resource
    require(paircore == {
        "two_support_intersection_floor": 2 * m - n,
        "low_common_core_max": common_core,
        "ordered_pair_petal_coefficient": coefficient,
        "ordered_pair_resource_ceiling": ordered_resource,
        "low_common_core_plane_cap": plane_cap,
        "next_integer_fails_by": next_integer_fails_by,
        "large_shared_pair_core_floor": 2 * m - n,
    }, "pair-core constants")
    require(plane_cap == 1434405, "low-core plane cap")
    require(next_integer_fails_by == 2636520, "next integer gap")

    selector_ratio = Fraction(495405467 * non_dense, 10**9)
    for index in range(9):
        selector_ratio *= Fraction(67482 - index, 1048586 - index)
    selector_records = ceiling(selector_ratio)
    require(selector_records == 2578110, "nine-subset endpoint")
    require(concentrator == {
        "selector_size": 9,
        "component_tuple_size": 11,
        "subsets_per_component_tuple": 55,
        "extension_multiplicity": "C(m_prime-9,2)",
        "dominant_lane_incidence_ppb_floor": 495405467,
        "uniform_endpoint_K_prime": 10,
        "fixed_selector_record_floor": selector_records,
    }, "concentrator constants")

    ninecell_resource = coefficient * (n - 9)
    ninecell_cap = (1 + isqrt(1 + 4 * ninecell_resource)) // 2
    require(ninecell == {
        "fixed_cell_size": 9,
        "common_core_floor": 9,
        "ordered_pair_resource_ceiling": ninecell_resource,
        "low_common_core_plane_cap": ninecell_cap,
        "next_integer_fails_by": (ninecell_cap + 1) * ninecell_cap - ninecell_resource,
        "large_shared_pair_core_floor": 2 * m - n,
    }, "nine-cell constants")
    require(ninecell_cap == 1434405, "nine-cell cap")

    rank8_error_differences = [[-1, 0, 1], [0, -1, 2], [0, 0, 3]]
    determinant = (
        rank8_error_differences[0][0]
        * rank8_error_differences[1][1]
        * rank8_error_differences[2][2]
    )
    require(determinant != 0, "sharp rank-three model")
    require(targets == {
        "fixed_selector_record_floor": selector_records,
        "population_excess_over_plane_cap": selector_records - ninecell_cap,
        "rank8_kernel_dimension": 2,
        "rank8_error_rank_ceiling": 3,
        "routes": [
            "FIXED_KERNEL_NINESUBSET_CHART",
            "RANK9_SHARED_PAIR_CORE_PLANE",
            "RANK8_OWNER_FLAT_ERROR_RANK_AT_MOST_3",
        ],
    }, "target routes")

    fixed_core = 1048576 - 1
    outside_weight = n - fixed_core
    outside_support = m - fixed_core
    heavy_count = 8
    heavy_weight = outside_support - 1
    light_count = outside_weight - heavy_count * heavy_weight
    fence_slopes = heavy_count * light_count
    require(local_fence == {
        "common_core_size": fixed_core,
        "outside_coordinate_weight": outside_weight,
        "outside_support_weight": outside_support,
        "heavy_owner_count": heavy_count,
        "heavy_owner_weight": heavy_weight,
        "unit_owner_count": light_count,
        "rich_slope_count": fence_slopes,
        "selector_floor_excess": fence_slopes - selector_records,
        "base_prime": 2130706433,
        "forbidden_slope_count": 18,
        "error_affine_rank_ceiling": 2,
    }, "local-cap fence constants")
    intervals = [
        (i * light_count - (light_count - 1), i * light_count)
        for i in range(heavy_count)
    ]
    require(
        all(left[1] + 1 == right[0] for left, right in zip(intervals, intervals[1:])),
        "disjoint direction intervals",
    )
    require(sum(high - low + 1 for low, high in intervals) == fence_slopes, "direction count")
    require(fixed_core + heavy_weight + 1 == m, "exact fence support")
    require(fixed_core + heavy_weight > 1048576 - 1, "pair root bound")
    require(fence_slopes == 4070408 > selector_records, "strict local fence")

    core_checks = 0
    for owner_core in range(2 * m - n, m):
        owner_multiplicity = (n - owner_core) // (m - owner_core)
        require(
            owner_multiplicity * (owner_multiplicity - 1)
            <= coefficient * (owner_core - common_core),
            "owner ordered pairs paid by petals",
        )
        core_checks += 1

    points, slopes, design_pairs = affine_plane_design()
    require(data["claims"] == {
        "local_theorem_packet": True,
        "incidence_is_record_count": False,
        "cross_cell_census": False,
        "fixed_chart_output_suffices_for_payment": False,
        "full_rank_star_owner_is_record_intrinsic": True,
        "chronology_owner": False,
        "rank11_paid": False,
        "active_v4_ledger_movement": 0,
        "KoalaBear_closed": False,
    }, "claim boundary")
    print(
        "KB_MCA_RANK11_DENSE_LOCATOR_SPLIT_PENCIL_V1_INDEPENDENT_PASS "
        f"endpoint={endpoint} records={records} cell_cap={fixed_cell} "
        f"plane_cap={plane_cap} core_checks={core_checks} "
        f"selector_records={selector_records} ninecell_cap={ninecell_cap} "
        f"local_fence_slopes={fence_slopes} "
        f"toy_points={points} toy_slopes={slopes} design_pairs={design_pairs}"
    )


if __name__ == "__main__":
    main()
