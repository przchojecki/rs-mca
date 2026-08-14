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
    cell = data["rank9_split_pencil_cell"]
    paircore = data["rank9_split_pencil_paircore"]
    require(
        data["source_prize_dag"]["nodes"]["rank9_split_pencil_paircore"]
        == PAIRCORE_SOURCE,
        "pair-core source pin",
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
        "chronology_owner": False,
        "rank11_paid": False,
        "active_v4_ledger_movement": 0,
        "KoalaBear_closed": False,
    }, "claim boundary")
    print(
        "KB_MCA_RANK11_DENSE_LOCATOR_SPLIT_PENCIL_V1_INDEPENDENT_PASS "
        f"endpoint={endpoint} records={records} cell_cap={fixed_cell} "
        f"plane_cap={plane_cap} core_checks={core_checks} "
        f"toy_points={points} toy_slopes={slopes} design_pairs={design_pairs}"
    )


if __name__ == "__main__":
    main()
