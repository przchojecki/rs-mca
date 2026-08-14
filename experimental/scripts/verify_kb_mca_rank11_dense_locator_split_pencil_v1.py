#!/usr/bin/env python3
"""Verify the KoalaBear rank-11 dense-locator/split-pencil packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from math import comb
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
    "rank9_split_pencil_cell": {
        "id": "rate_half_mca_rank11_rank9_split_pencil_cell_ledger",
        "path": "background/nodes/rate_half_mca_rank11_rank9_split_pencil_cell_ledger",
        "commit": "51cb474f63b364de6d1193bac98476d63ebfea6e",
        "tree": "41906278691510040285434141ea6957069d0d25",
        "contract_sha256": "150863c70ede9590605eaa93eb97a16da4edb6883d6ede80c60c1c12d9795cf3",
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
        "claims": {
            "local_theorem_packet": True,
            "incidence_is_record_count": False,
            "cross_cell_census": False,
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
    require(value["claims"]["active_v4_ledger_movement"] == 0, "ledger movement")
    return {
        **dense,
        "component_ppb": component["component_incidence_ppb_floor"],
        "cell_cap": value["rank9_split_pencil_cell"]["sharp_fixed_cell_record_cap"],
    }


def tamper_selftest(reference: dict[str, Any]) -> int:
    mutations = (
        lambda item: item["dense_root_saturation"].__setitem__("dense_root_count", 17),
        lambda item: item["component_incidence"].__setitem__("isolated_bezout", 197),
        lambda item: item["component_incidence"].__setitem__("component_incidence_ppb_floor", 990810935),
        lambda item: item["component_star"].__setitem__("rank9_extension_floor", 45152),
        lambda item: item["rank9_split_pencil_cell"].__setitem__("sharp_fixed_cell_record_cap", 45567659),
        lambda item: item["rank9_split_pencil_cell"].__setitem__("rounding_rule", "ceil"),
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
        f"controls={controls} manifest_sha256={hashlib.sha256(MANIFEST.read_bytes()).hexdigest()}"
    )


if __name__ == "__main__":
    main()
