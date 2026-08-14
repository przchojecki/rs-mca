#!/usr/bin/env python3
"""Independent replay of the rank-11 component and split-pencil constants."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from math import comb, isqrt, prod
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
    "component_ninesubset_weighted_concentrator": {
        "id": "rate_half_mca_rank11_component_ninesubset_weighted_concentrator",
        "path": "background/nodes/rate_half_mca_rank11_component_ninesubset_weighted_concentrator",
        "commit": "01d5e936e4d9a6df7daf59310b9c00c10cb6d081",
        "tree": "c553262475b8e70070f3ffd61a2d70ecf5086161",
        "contract_sha256": "050954321fc65a504b801b19dc0787e21d31f979f8062319ea67055e37709895",
    },
    "rank9_weighted_component_cap": {
        "id": "rate_half_mca_rank11_rank9_weighted_component_cap",
        "path": "background/nodes/rate_half_mca_rank11_rank9_weighted_component_cap",
        "commit": "01d5e936e4d9a6df7daf59310b9c00c10cb6d081",
        "tree": "1148246aa2b5df2295cfedb1dc26764ad050758a",
        "contract_sha256": "d8000c85400cd931d846b9da91d7203720fb31cedce7abcd08318bf4879a22b5",
    },
    "rank9_weighted_target_elimination": {
        "id": "rate_half_mca_rank11_rank9_weighted_target_elimination",
        "path": "background/nodes/rate_half_mca_rank11_rank9_weighted_target_elimination",
        "commit": "01d5e936e4d9a6df7daf59310b9c00c10cb6d081",
        "tree": "671ed959f3e958354f111b0a3211c7af9106d537",
        "contract_sha256": "78436c5e0cc6cd9d313e8d4de24e849d87676a4236be6e2c09b203576a002ab9",
    },
    "kernel_canonical_basis_globalizer": {
        "id": "rate_half_mca_rank11_kernel_canonical_basis_globalizer",
        "path": "background/nodes/rate_half_mca_rank11_kernel_canonical_basis_globalizer",
        "commit": "b16e254492023dadba37f0caff043ed189d80a0f",
        "tree": "ab27bebc2af47d7e7f3baa6254d241064e27efd2",
        "contract_sha256": "98de8b079e0de815c691dcebfd49ad2520dc7ca3c232ea62b34eb4e94ecbfdfa",
    },
    "kernel_rankstratified_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_rankstratified_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_rankstratified_capacity_cut",
        "commit": "b16e254492023dadba37f0caff043ed189d80a0f",
        "tree": "a55878b5c4b9c7b3b3e67e4fcc7e71e23c75abff",
        "contract_sha256": "9fffc92c3682c65db6ac6c1f4b4fc7509c14516f41f2d9c7ebfe8750a7760312",
    },
    "rank8_owner_pair_weight_cap": {
        "id": "rate_half_mca_rank11_rank8_owner_pair_weight_cap",
        "path": "background/nodes/rate_half_mca_rank11_rank8_owner_pair_weight_cap",
        "commit": "9e44f19b0217069bfdfb74763d36d6a9c873e8d7",
        "tree": "ee5e4aa7f501997f94c85c61ab71adecfe4139c7",
        "contract_sha256": "478aa8e2affd878acaf36cd1fd313fcdb857b552e5edf28dda1e4ad1c59cb32c",
    },
    "rank8_weighted_capacity_cut": {
        "id": "rate_half_mca_rank11_rank8_weighted_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_rank8_weighted_capacity_cut",
        "commit": "9e44f19b0217069bfdfb74763d36d6a9c873e8d7",
        "tree": "215c4c6801da15652103458deb833a099c3da1cd",
        "contract_sha256": "dad2aa8f83ec9cd1bbcebad2f7b127efd2037743df539e2f2662629a4a1c1396",
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def short_fall(value: int, length: int) -> int:
    return prod(value - offset for offset in range(length))


def short_rise(value: int, length: int) -> int:
    return prod(value + offset for offset in range(length))


def independent_kernel_record_cap(kprime: int, rank: int) -> int:
    dimension = 10 - rank
    if dimension == 9:
        return 61871313426630599
    shortened_k = kprime - rank
    first = Fraction(
        short_fall(1048576 + shortened_k, dimension + 1),
        (67472 + shortened_k) * short_rise(67473, dimension - 1),
    )
    second = Fraction(
        short_fall(1048576 + dimension, dimension + 1),
        short_rise(67473, dimension),
    )
    return int(max(first, second))


def independent_kernel_capacity(kprime: int) -> int:
    total = 0
    for rank in range(9, 0, -1):
        dimension = 10 - rank
        extras = kprime - 10
        extensions = comb(extras, dimension + 1) if extras >= dimension + 1 else 0
        total += (
            comb(1048576 + kprime, rank)
            * independent_kernel_record_cap(kprime, rank)
            * extensions
        )
    return total


def independent_kernel_demand(kprime: int) -> int:
    return ceiling(
        Fraction(
            495405467 * 274980728111260126 * comb(67472 + kprime, 11),
            10**9,
        )
    )


def independent_rank8_demand(kprime: int) -> int:
    nprime = 1048576 + kprime
    mprime = 67472 + kprime
    return ceiling(Fraction(
        55 * 495405467 * 274980728111260126 * comb(mprime, 11),
        10**9 * comb(nprime, 9),
    ))


def independent_rank8_cap(kprime: int) -> int:
    outside = 1048576 + kprime - 9
    return 981105 * outside * (outside - 1) // 2


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
    weighted_concentrator = data["component_ninesubset_weighted_concentrator"]
    weighted_cap = data["rank9_weighted_component_cap"]
    weighted_elimination = data["rank9_weighted_target_elimination"]
    kernel_globalizer = data["kernel_canonical_basis_globalizer"]
    kernel_cut = data["kernel_rankstratified_capacity_cut"]
    rank8_owner_cap = data["rank8_owner_pair_weight_cap"]
    rank8_cut = data["rank8_weighted_capacity_cut"]
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

    marked_endpoint = ceiling(
        selector_ratio * comb(67482 - 9, 2)
    )
    require(marked_endpoint == 5868470021012020, "weighted selector endpoint")
    require(weighted_concentrator == {
        "weighted_endpoint_K_prime": 10,
        "marked_component_extension_floor": marked_endpoint,
        "deduplicated_record_floor": selector_records,
        "weight_unit": "record_component_eleven_subset_containing_fixed_ninesubset",
    }, "weighted concentrator constants")

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

    boundary_k = 67473
    boundary_n = 1048576 + boundary_k
    boundary_m = 67472 + boundary_k
    boundary_ratio = Fraction(495405467 * non_dense, 10**9)
    for index in range(9):
        boundary_ratio *= Fraction(boundary_m - index, boundary_n - index)
    boundary_ratio *= comb(boundary_m - 9, 2)
    boundary_demand = ceiling(boundary_ratio)
    boundary_cap = coefficient * (boundary_m - 10) * boundary_n
    require(weighted_cap == {
        "fixed_owner_record_cap": coefficient,
        "cap_formula": "981105*(m_prime-10)*n_prime",
        "boundary_K_prime": boundary_k,
        "boundary_cap": boundary_cap,
    }, "weighted rank-nine cap")
    require(weighted_elimination == {
        "small_dimension_ceiling": 67472,
        "weighted_boundary_K_prime": boundary_k,
        "forced_common_core_floor": 2 * m - n,
        "boundary_demand": boundary_demand,
        "boundary_cap": boundary_cap,
        "boundary_gap": boundary_demand - boundary_cap,
        "remaining_routes": [
            "FIXED_KERNEL_NINESUBSET_CHART",
            "RANK8_OWNER_FLAT_ERROR_RANK_AT_MOST_3",
        ],
    }, "weighted rank-nine elimination")
    require(boundary_demand == 6849288576200976639, "weighted boundary demand")
    require(boundary_cap == 147748596828055575, "weighted boundary cap")
    ratios = []
    for k_value in (67473, 67474, 100000, 1048576):
        n_value, m_value = 1048576 + k_value, 67472 + k_value
        ratio = Fraction(comb(m_value, 9), comb(n_value, 9))
        ratio *= Fraction(m_value - 9, n_value)
        ratios.append(ratio)
    require(all(a < b for a, b in zip(ratios, ratios[1:])), "weighted ratio monotonicity")

    require(kernel_globalizer == {
        "correction_dimension": 10,
        "component_subset_size": 11,
        "rank_minimum": 1,
        "rank_maximum": 9,
        "extra_common_zero_offset": 10,
        "rank9_record_cap": 61871313426630599,
        "fixed_basis_capacity_formula": "M_d*C(K_prime-10,d+1)",
    }, "kernel basis constants")
    kernel_checks = 0
    for kprime in range(10, 4599):
        require(
            independent_kernel_demand(kprime) > independent_kernel_capacity(kprime),
            f"kernel capacity {kprime}",
        )
        kernel_checks += 1
    kernel_endpoint_demand = independent_kernel_demand(4598)
    kernel_endpoint_capacity = independent_kernel_capacity(4598)
    kernel_wall_demand = independent_kernel_demand(4599)
    kernel_wall_capacity = independent_kernel_capacity(4599)
    require(kernel_cut == {
        "closed_K_prime_minimum": 10,
        "closed_K_prime_maximum": 4598,
        "first_open_K_prime": 4599,
        "endpoint_demand": kernel_endpoint_demand,
        "endpoint_capacity": kernel_endpoint_capacity,
        "endpoint_gap": kernel_endpoint_demand - kernel_endpoint_capacity,
        "wall_demand": kernel_wall_demand,
        "wall_capacity": kernel_wall_capacity,
        "capacity_formula": "sum_d C(n_prime,10-d)*M_d*C(K_prime-10,d+1)",
    }, "kernel capacity constants")
    require(kernel_wall_demand < kernel_wall_capacity, "kernel method wall")

    require(rank8_owner_cap == {
        "kernel_dimension": 2,
        "owner_flat_dimension": 4,
        "fixed_subset_size": 9,
        "fixed_owner_record_cap": 981105,
        "coordinate_pair_resource_formula": "C(n_prime-9,2)",
        "weighted_cap_formula": "981105*C(n_prime-9,2)",
    }, "rank-eight owner-pair cap")
    rank8_last_demand = independent_rank8_demand(37995)
    rank8_last_cap = independent_rank8_cap(37995)
    rank8_first_demand = independent_rank8_demand(37996)
    rank8_first_cap = independent_rank8_cap(37996)
    require(rank8_cut == {
        "last_open_K_prime": 37995,
        "last_open_demand": rank8_last_demand,
        "last_open_cap": rank8_last_cap,
        "last_open_gap": rank8_last_cap - rank8_last_demand,
        "first_closed_K_prime": 37996,
        "first_closed_demand": rank8_first_demand,
        "first_closed_cap": rank8_first_cap,
        "first_closed_gap": rank8_first_demand - rank8_first_cap,
        "closed_K_prime_maximum": 1048576,
        "ratio_formula": "constant*C(m_prime,11)/C(n_prime,11)",
    }, "rank-eight capacity cut")
    require(rank8_last_demand <= rank8_last_cap, "rank-eight last open")
    require(rank8_first_demand > rank8_first_cap, "rank-eight first closed")
    monotone_factors = 0
    for index in range(10, -1, -1):
        require(
            Fraction(105469 - index, 1086573 - index)
            > Fraction(105468 - index, 1086572 - index),
            f"rank-eight factor {index}",
        )
        monotone_factors += 1

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
        "rank9_fixed_target_eliminated": True,
        "kernel_dominant_lane_closed_through_Kprime": 4598,
        "rank8_owner_flat_closed_from_Kprime": 37996,
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
        f"weighted_demand={boundary_demand} weighted_cap={boundary_cap} "
        f"kernel_checks={kernel_checks} "
        f"kernel_endpoint_gap={kernel_endpoint_demand-kernel_endpoint_capacity} "
        f"kernel_wall_gap={kernel_wall_capacity-kernel_wall_demand} "
        f"rank8_last_gap={rank8_last_cap-rank8_last_demand} "
        f"rank8_first_gap={rank8_first_demand-rank8_first_cap} "
        f"rank8_monotone_factors={monotone_factors} "
        f"toy_points={points} toy_slopes={slopes} design_pairs={design_pairs}"
    )


if __name__ == "__main__":
    main()
