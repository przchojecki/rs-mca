#!/usr/bin/env python3
"""Verify the KoalaBear rank-11 dense-locator/split-pencil packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from math import comb, isqrt
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "experimental/data/certificates/kb-mca-rank11-dense-locator-split-pencil-v1/manifest.json"
PARENT = "b4bad860750f91955dbaead8f2b5a0fdef1f1343"
SOURCE_NODES = {
    "dense_root_highspan": {
        "id": "rate_half_mca_rank11_dense_root_highspan_saturation",
        "path": "background/nodes/rate_half_mca_rank11_dense_root_highspan_saturation",
        "commit": "e30d06ff5793dde8ed0a2413a23d33d6dbd389fa",
        "tree": "5b461ef0609c5755de695d39b77fd11032fbfc99",
        "contract_sha256": "9847a084251f60c01dabceda6a29f64b11df92cdb06352e922a19fa4ba1e79a6",
    },
    "component_incidence": {
        "id": "rate_half_mca_rank11_dense_locator_component_incidence_dichotomy",
        "path": "background/nodes/rate_half_mca_rank11_dense_locator_component_incidence_dichotomy",
        "commit": "2aea009ba11c88e65f7654b7b4f786d6cf428d0a",
        "tree": "ef5092f58c21a4ea798aef75182c3d938b02365c",
        "contract_sha256": "6eec697bc3729eab2aba4d282b3c1536e862826cc7c1c17379c2df4ebf55d59b",
    },
    "component_star": {
        "id": "rate_half_mca_rank11_component_star_owner_pencil_router",
        "path": "background/nodes/rate_half_mca_rank11_component_star_owner_pencil_router",
        "commit": "20eb40d59f751f5e8872329c2ef22437c99037e4",
        "tree": "39e1b4222d88c7d50e343fb215d98ecca302c7f2",
        "contract_sha256": "23894520514168a69e1de5e638705c2036c6303e678bd295c124fe4278a917f7",
    },
    "component_star_large_owner_uniqueness": {
        "id": "rate_half_mca_rank11_component_star_large_owner_uniqueness",
        "path": "background/nodes/rate_half_mca_rank11_component_star_large_owner_uniqueness",
        "commit": "b6f4705196e52e0940d592ca21363d9fd8a920b2",
        "tree": "4c8d49092349cc1c78c265be3845d5a526144b25",
        "contract_sha256": "731e65b2926b11ef0d192e11fb55e5eac280e0d93038270fe131d79b9ca7b076",
    },
    "rank9_split_pencil_cell": {
        "id": "rate_half_mca_rank11_rank9_split_pencil_cell_ledger",
        "path": "background/nodes/rate_half_mca_rank11_rank9_split_pencil_cell_ledger",
        "commit": "51cb474f63b364de6d1193bac98476d63ebfea6e",
        "tree": "41906278691510040285434141ea6957069d0d25",
        "contract_sha256": "150863c70ede9590605eaa93eb97a16da4edb6883d6ede80c60c1c12d9795cf3",
    },
    "rank9_split_pencil_paircore": {
        "id": "rate_half_mca_rank11_rank9_split_pencil_paircore_dichotomy",
        "path": "background/nodes/rate_half_mca_rank11_rank9_split_pencil_paircore_dichotomy",
        "commit": "0e547404a4426b9c2e5672d44b7f23e726756e01",
        "tree": "a74872d50f946260fc65c6a798e069d6e17ace59",
        "contract_sha256": "e899fbb6893e61495371f689f6a2ca5eb196d0bbc6d6ec8dc39b34eb9965c252",
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
}


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def ceil_ratio(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def rank_mod(vectors: list[list[int]], field: int) -> int:
    rows = [[value % field for value in row] for row in vectors]
    rank = 0
    columns = len(rows[0]) if rows else 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, field)
        rows[rank] = [(inverse * value) % field for value in rows[rank]]
        for i, row in enumerate(rows):
            if i == rank or row[column] == 0:
                continue
            scale = row[column]
            rows[i] = [(a - scale * b) % field for a, b in zip(row, rows[rank])]
        rank += 1
    return rank


def locator(roots: list[int], field: int) -> list[int]:
    coefficients = [1]
    for root in roots:
        product = [0] * (len(coefficients) + 1)
        for index, value in enumerate(coefficients):
            product[index] = (product[index] - root * value) % field
            product[index + 1] = (product[index + 1] + value) % field
        coefficients = product
    return coefficients


def vector_polynomial_product(
    scalar: list[int], vectors: list[list[int]], field: int
) -> list[list[int]]:
    dimension = len(vectors[0])
    result = [[0] * dimension for _ in range(len(scalar) + len(vectors) - 1)]
    for i, coefficient in enumerate(scalar):
        for j, vector in enumerate(vectors):
            for coordinate, value in enumerate(vector):
                result[i + j][coordinate] = (
                    result[i + j][coordinate] + coefficient * value
                ) % field
    return result


def evaluate(coefficients: list[list[int]], point: int, field: int) -> list[int]:
    result = [0] * len(coefficients[0])
    for coefficient in reversed(coefficients):
        result = [
            (point * value + addend) % field
            for value, addend in zip(result, coefficient)
        ]
    return result


def dense_root_model() -> dict[str, int]:
    field = 101
    roots = list(range(18))
    quotient = []
    for index in range(14):
        if index < 10:
            vector = [0] * 10
            vector[index] = 1
        else:
            vector = [pow(index + 1, coordinate, field) for coordinate in range(10)]
        quotient.append(vector)
    q = locator(roots, field)
    deviation = vector_polynomial_product(q, quotient, field)
    require(len(q) == 19 and q[-1] == 1, "monic degree-18 locator")
    require(len(deviation) == 32, "degree-31 deviation")
    require(
        all(evaluate(deviation, root, field) == [0] * 10 for root in roots),
        "dense roots",
    )
    require(rank_mod(quotient, field) == 10, "quotient span")
    require(rank_mod(deviation[18:32], field) == 10, "triangular high span")
    values = [evaluate(deviation, point, field) for point in range(18, 28)]
    require(rank_mod(values, field) == 10, "normalized value span")
    return {"roots": 18, "high_rank": 10}


def expected() -> dict[str, Any]:
    budget = 274980728111395087
    near = 134944
    dense = 18
    non_dense = budget + 1 - near - dense
    isolated = ceil_ratio(198 * comb(1048576 + 10, 11), comb(67472 + 10, 11))
    isolated_ppb = ceil_ratio(isolated * 10**9, non_dense)
    component_ppb = 10**9 - isolated_ppb
    record_ppb = (component_ppb - 980000000) * 50
    threshold_records = ceil_ratio(non_dense * record_ppb, 10**9)
    m_max = 67472 + 1048576
    extensions = ceil_ratio(98 * (m_max - 10), 100)
    deficiency = m_max - 10 - extensions
    pencil = extensions - (1048576 - 11)
    owner_cap = 2097152 - m_max + 1
    weighted = owner_cap * (2097152 - 10)
    cell = weighted // pencil
    pair_intersection = 2 * 1116048 - 2097152
    paircore_coefficient = 981104 + 1
    paircore_resource = paircore_coefficient * (2097152 - 10)
    plane_cap = (1 + isqrt(1 + 4 * paircore_resource)) // 2
    next_integer_fails_by = (plane_cap + 1) * plane_cap - paircore_resource
    lane_ppb = component_ppb // 2
    selector_records = ceil_ratio(
        lane_ppb * non_dense * comb(67472 + 10, 9),
        10**9 * comb(1048576 + 10, 9),
    )
    ninecell_resource = paircore_coefficient * (2097152 - 9)
    ninecell_cap = (1 + isqrt(1 + 4 * ninecell_resource)) // 2
    ninecell_next_fails_by = (
        (ninecell_cap + 1) * ninecell_cap - ninecell_resource
    )
    common_core = 1048576 - 1
    outside_weight = 2097152 - common_core
    outside_support = 1116048 - common_core
    heavy_owners = 8
    heavy_weight = outside_support - 1
    unit_owners = outside_weight - heavy_owners * heavy_weight
    local_fence_slopes = heavy_owners * unit_owners
    weighted_selector_endpoint = ceil_ratio(
        lane_ppb
        * non_dense
        * comb(67472 + 10, 9)
        * comb(67472 + 10 - 9, 2),
        10**9 * comb(1048576 + 10, 9),
    )
    weighted_boundary_k = 67473
    weighted_boundary_n = 1048576 + weighted_boundary_k
    weighted_boundary_m = 67472 + weighted_boundary_k
    weighted_boundary_demand = ceil_ratio(
        lane_ppb
        * non_dense
        * comb(weighted_boundary_m, 9)
        * comb(weighted_boundary_m - 9, 2),
        10**9 * comb(weighted_boundary_n, 9),
    )
    weighted_boundary_cap = (
        owner_cap * (weighted_boundary_m - 10) * weighted_boundary_n
    )
    return {
        "schema": "kb-mca-rank11-dense-locator-split-pencil-v1",
        "exact_parent": PARENT,
        "source_prize_dag": {
            "repository": "AllenGrahamHart/rs-mca-prize-dag",
            "nodes": SOURCE_NODES,
        },
        "row": {
            "name": "KoalaBear MCA",
            "n": 2097152,
            "k": 1048576,
            "agreement": 1116048,
            "budget": budget,
            "near_charge": near,
            "unit": "distinct bad finite slopes per received line",
        },
        "dense_root_saturation": {
            "anchor_count": 32,
            "dense_root_count": 18,
            "quotient_degree_maximum": 13,
            "correction_dimension": 10,
            "triangular_coefficient_start": 18,
            "triangular_coefficient_end": 31,
        },
        "component_incidence": {
            "R": 1048576,
            "d": 67472,
            "K_min": 10,
            "K_max": 1048576,
            "tuple_size": 11,
            "coordinate_bidegree": [18, 1],
            "isolated_bezout": 198,
            "removed_dense_records": dense,
            "non_dense_record_floor": non_dense,
            "isolated_equivalent_ceiling": isolated,
            "isolated_incidence_ppb_ceiling": isolated_ppb,
            "component_incidence_ppb_floor": component_ppb,
            "one_lane_ppb_floor": component_ppb // 2,
        },
        "component_star": {
            "threshold_percent": 98,
            "record_fraction_ppb_floor": record_ppb,
            "threshold_record_floor": threshold_records,
            "full_rank_owner_deficiency_ceiling": deficiency,
            "rank9_extension_floor": pencil,
            "low_rank_kernel_dimension_floor": 2,
            "routes": ["LARGE_AFFINE_OWNER", "RANK9_OWNER_PENCIL", "KERNEL_PLANE"],
        },
        "component_star_large_owner_uniqueness": {
            "large_owner_deficiency_ceiling": deficiency,
            "two_owner_deficiency_sum": 2 * deficiency,
            "distance_margin_after_two_owners": 67472 - 2 * deficiency,
            "intersection_over_root_cap": 67472 - 2 * deficiency + 1,
            "owner_count_per_record": 1,
        },
        "rank9_split_pencil_cell": {
            "cell_size": 10,
            "cell_rank": 9,
            "kernel_dimension": 1,
            "fixed_owner_slope_cap": owner_cap,
            "common_root_core_floor": 10,
            "weighted_petal_incidence_cap": weighted,
            "source_weak_ceiling_cap": ceil_ratio(weighted, pencil),
            "sharp_fixed_cell_record_cap": cell,
            "rounding_rule": "floor(weighted_petal_incidence_cap/rank9_extension_floor)",
        },
        "rank9_split_pencil_paircore": {
            "two_support_intersection_floor": pair_intersection,
            "low_common_core_max": pair_intersection - 1,
            "ordered_pair_petal_coefficient": paircore_coefficient,
            "ordered_pair_resource_ceiling": paircore_resource,
            "low_common_core_plane_cap": plane_cap,
            "next_integer_fails_by": next_integer_fails_by,
            "large_shared_pair_core_floor": pair_intersection,
        },
        "component_ninesubset_concentrator": {
            "selector_size": 9,
            "component_tuple_size": 11,
            "subsets_per_component_tuple": comb(11, 9),
            "extension_multiplicity": "C(m_prime-9,2)",
            "dominant_lane_incidence_ppb_floor": lane_ppb,
            "uniform_endpoint_K_prime": 10,
            "fixed_selector_record_floor": selector_records,
        },
        "rank9_ninecell_paircore": {
            "fixed_cell_size": 9,
            "common_core_floor": 9,
            "ordered_pair_resource_ceiling": ninecell_resource,
            "low_common_core_plane_cap": ninecell_cap,
            "next_integer_fails_by": ninecell_next_fails_by,
            "large_shared_pair_core_floor": pair_intersection,
        },
        "component_ninesubset_targets": {
            "fixed_selector_record_floor": selector_records,
            "population_excess_over_plane_cap": selector_records - ninecell_cap,
            "rank8_kernel_dimension": 2,
            "rank8_error_rank_ceiling": 3,
            "routes": [
                "FIXED_KERNEL_NINESUBSET_CHART",
                "RANK9_SHARED_PAIR_CORE_PLANE",
                "RANK8_OWNER_FLAT_ERROR_RANK_AT_MOST_3",
            ],
        },
        "rank9_fixed_chart_local_cap_fence": {
            "common_core_size": common_core,
            "outside_coordinate_weight": outside_weight,
            "outside_support_weight": outside_support,
            "heavy_owner_count": heavy_owners,
            "heavy_owner_weight": heavy_weight,
            "unit_owner_count": unit_owners,
            "rich_slope_count": local_fence_slopes,
            "selector_floor_excess": local_fence_slopes - selector_records,
            "base_prime": 2130706433,
            "forbidden_slope_count": 18,
            "error_affine_rank_ceiling": 2,
        },
        "component_ninesubset_weighted_concentrator": {
            "weighted_endpoint_K_prime": 10,
            "marked_component_extension_floor": weighted_selector_endpoint,
            "deduplicated_record_floor": selector_records,
            "weight_unit": "record_component_eleven_subset_containing_fixed_ninesubset",
        },
        "rank9_weighted_component_cap": {
            "fixed_owner_record_cap": owner_cap,
            "cap_formula": "981105*(m_prime-10)*n_prime",
            "boundary_K_prime": weighted_boundary_k,
            "boundary_cap": weighted_boundary_cap,
        },
        "rank9_weighted_target_elimination": {
            "small_dimension_ceiling": 67472,
            "weighted_boundary_K_prime": weighted_boundary_k,
            "forced_common_core_floor": pair_intersection,
            "boundary_demand": weighted_boundary_demand,
            "boundary_cap": weighted_boundary_cap,
            "boundary_gap": weighted_boundary_demand - weighted_boundary_cap,
            "remaining_routes": [
                "FIXED_KERNEL_NINESUBSET_CHART",
                "RANK8_OWNER_FLAT_ERROR_RANK_AT_MOST_3",
            ],
        },
        "claims": {
            "local_theorem_packet": True,
            "incidence_is_record_count": False,
            "cross_cell_census": False,
            "fixed_chart_output_suffices_for_payment": False,
            "full_rank_star_owner_is_record_intrinsic": True,
            "rank9_fixed_target_eliminated": True,
            "chronology_owner": False,
            "rank11_paid": False,
            "active_v4_ledger_movement": 0,
            "KoalaBear_closed": False,
        },
    }


def validate(value: object) -> dict[str, int]:
    require(isinstance(value, dict), "manifest object")
    wanted = expected()
    require(value == wanted, "canonical manifest")
    dense = dense_root_model()
    component = value["component_incidence"]
    for k_value in (10, 11, 100, 4923, 1048576):
        current = ceil_ratio(
            198 * comb(1048576 + k_value, 11),
            comb(67472 + k_value, 11),
        )
        require(current <= component["isolated_equivalent_ceiling"], "endpoint monotonicity")
    require(18 * 11 == component["isolated_bezout"], "multihomogeneous Bezout")
    owner_unique = value["component_star_large_owner_uniqueness"]
    require(owner_unique["intersection_over_root_cap"] == 22833, "large-owner root gap")
    require(owner_unique["owner_count_per_record"] == 1, "record-intrinsic owner")
    require(value["claims"]["active_v4_ledger_movement"] == 0, "ledger movement")
    fence = value["rank9_fixed_chart_local_cap_fence"]
    require(fence["rich_slope_count"] > value["component_ninesubset_targets"]["fixed_selector_record_floor"], "local-cap fence")
    require(fence["base_prime"] > fence["forbidden_slope_count"] * fence["rich_slope_count"], "forbidden-slope translate")
    weighted_elimination = value["rank9_weighted_target_elimination"]
    require(weighted_elimination["boundary_demand"] > weighted_elimination["boundary_cap"], "weighted target gap")
    require(value["claims"]["rank9_fixed_target_eliminated"], "rank-nine elimination")
    return {
        **dense,
        "component_ppb": component["component_incidence_ppb_floor"],
        "cell_cap": value["rank9_split_pencil_cell"]["sharp_fixed_cell_record_cap"],
        "plane_cap": value["rank9_split_pencil_paircore"]["low_common_core_plane_cap"],
        "selector_records": value["component_ninesubset_concentrator"]["fixed_selector_record_floor"],
        "local_fence_slopes": fence["rich_slope_count"],
        "weighted_demand": weighted_elimination["boundary_demand"],
        "weighted_cap": weighted_elimination["boundary_cap"],
    }


def tamper_selftest(reference: dict[str, Any]) -> int:
    mutations = (
        lambda item: item["dense_root_saturation"].__setitem__("dense_root_count", 17),
        lambda item: item["component_incidence"].__setitem__("isolated_bezout", 197),
        lambda item: item["component_incidence"].__setitem__("component_incidence_ppb_floor", 990810935),
        lambda item: item["component_star"].__setitem__("rank9_extension_floor", 45152),
        lambda item: item["component_star_large_owner_uniqueness"].__setitem__("intersection_over_root_cap", 22832),
        lambda item: item["rank9_split_pencil_cell"].__setitem__("sharp_fixed_cell_record_cap", 45567659),
        lambda item: item["rank9_split_pencil_cell"].__setitem__("rounding_rule", "ceil"),
        lambda item: item["rank9_split_pencil_paircore"].__setitem__("low_common_core_plane_cap", 1434406),
        lambda item: item["component_ninesubset_concentrator"].__setitem__("fixed_selector_record_floor", 2578109),
        lambda item: item["rank9_ninecell_paircore"].__setitem__("ordered_pair_resource_ceiling", 2057517483014),
        lambda item: item["component_ninesubset_targets"].__setitem__("rank8_error_rank_ceiling", 4),
        lambda item: item["rank9_fixed_chart_local_cap_fence"].__setitem__("rich_slope_count", 2578110),
        lambda item: item["component_ninesubset_weighted_concentrator"].__setitem__("marked_component_extension_floor", 5868470021012019),
        lambda item: item["rank9_weighted_component_cap"].__setitem__("boundary_cap", 147748596828055574),
        lambda item: item["rank9_weighted_target_elimination"].__setitem__("boundary_gap", 6701539979372921063),
        lambda item: item["claims"].__setitem__("fixed_chart_output_suffices_for_payment", True),
        lambda item: item["claims"].__setitem__("full_rank_star_owner_is_record_intrinsic", False),
        lambda item: item["claims"].__setitem__("rank9_fixed_target_eliminated", False),
        lambda item: item["claims"].__setitem__("incidence_is_record_count", True),
        lambda item: item["claims"].__setitem__("rank11_paid", True),
        lambda item: item["source_prize_dag"]["nodes"]["component_star"].__setitem__("commit", "0" * 40),
    )
    caught = 0
    for mutation in mutations:
        changed = copy.deepcopy(reference)
        mutation(changed)
        try:
            validate(changed)
        except Reject:
            caught += 1
    require(caught == len(mutations), "all hostile mutations rejected")
    return caught


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    value = json.loads(MANIFEST.read_text())
    result = validate(value)
    controls = tamper_selftest(value) if args.tamper_selftest else 0
    print(
        "KB_MCA_RANK11_DENSE_LOCATOR_SPLIT_PENCIL_V1_PASS "
        f"roots={result['roots']} high_rank={result['high_rank']} "
        f"component_ppb={result['component_ppb']} cell_cap={result['cell_cap']} "
        f"plane_cap={result['plane_cap']} "
        f"selector_records={result['selector_records']} "
        f"local_fence_slopes={result['local_fence_slopes']} "
        f"weighted_demand={result['weighted_demand']} "
        f"weighted_cap={result['weighted_cap']} "
        f"controls={controls} manifest_sha256={hashlib.sha256(MANIFEST.read_bytes()).hexdigest()}"
    )


if __name__ == "__main__":
    main()
