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
    "kernel_multibasis_decoration_compression": {
        "id": "rate_half_mca_rank11_kernel_multibasis_decoration_compression",
        "path": "background/nodes/rate_half_mca_rank11_kernel_multibasis_decoration_compression",
        "commit": "103807c376fb5ec90ec2158ea8c617dab2a95538",
        "tree": "1dca4b03b66d63b2120f11b35414e7edebda2417",
        "contract_sha256": "2db1ee7ecda1fb2498203ee3eec190f732d149e21e1aa8df87d8e52aafd16f52",
    },
    "kernel_multibasis_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_multibasis_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_multibasis_capacity_cut",
        "commit": "103807c376fb5ec90ec2158ea8c617dab2a95538",
        "tree": "f4b0f0a84e71a4e8b78c18c405776c7d5f78263d",
        "contract_sha256": "47cd5f4ee795bc82161711e65e1fdbfd70cc86d0947854a4ed9aa320508b8a64",
    },
    "kernel_record_support_capacity": {
        "id": "rate_half_mca_rank11_kernel_record_support_capacity",
        "path": "background/nodes/rate_half_mca_rank11_kernel_record_support_capacity",
        "commit": "11a8c12ffa1061e899b36a912277caef2b11a3de",
        "tree": "c7a7d8a8498ae167efbb4174b8a4bbcb054a1608",
        "contract_sha256": "ede7f01e37f1f856118ba73b3c94af8b99658361cac2e747f7f69fe24d3a7e7e",
    },
    "kernel_hybrid_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_hybrid_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_hybrid_capacity_cut",
        "commit": "11a8c12ffa1061e899b36a912277caef2b11a3de",
        "tree": "9921a1975991825967e67cf6f5d3350ee96488f1",
        "contract_sha256": "ce3e5d908adba2db8ce0a12cd0f464d1d9b45b0602203f9f5a8adef7e0d51837",
    },
    "kernel_nine_shadow_coupling": {
        "id": "rate_half_mca_rank11_kernel_nine_shadow_coupling",
        "path": "background/nodes/rate_half_mca_rank11_kernel_nine_shadow_coupling",
        "commit": "26c4396652ebeaa4036b5cf0d226fd412a7f38b6",
        "tree": "8a916d6371274ed5bb55ac8a734e47988385a63a",
        "contract_sha256": "191af0d208a5cce6a6339bfc265de3be1bf8ca86b1c6da298ade68142e80c63e",
    },
    "kernel_nine_shadow_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_nine_shadow_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_nine_shadow_capacity_cut",
        "commit": "26c4396652ebeaa4036b5cf0d226fd412a7f38b6",
        "tree": "f69573f892c12735b6f111aef40d05e71b4118a7",
        "contract_sha256": "1bbf5e021b422c8124ac339fc14cf79e50b0368d4b42cd1b22fd4a59307ca75e",
    },
    "kernel_nine_shadow_containment_coupling": {
        "id": "rate_half_mca_rank11_kernel_nine_shadow_containment_coupling",
        "path": "background/nodes/rate_half_mca_rank11_kernel_nine_shadow_containment_coupling",
        "commit": "0620558d5eb0a49e03000b2a2fc16ec826e2e2fb",
        "tree": "0d809e2286193d2ad9c63781d58278ee79dfd15d",
        "contract_sha256": "3ba2ac2f6053c753f3a60e2df8152f4bde8221deb772648699f99c9c5c314056",
    },
    "kernel_nine_shadow_containment_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_nine_shadow_containment_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_nine_shadow_containment_capacity_cut",
        "commit": "0620558d5eb0a49e03000b2a2fc16ec826e2e2fb",
        "tree": "f396ad96d235ca25e2f313ff38819be9aa668139",
        "contract_sha256": "7d56dc863b2bb327c392b33405098b5163a305e4a909a007482e32bfbd00f7e4",
    },
    "kernel_rank8_nine_shadow_extension_deficit": {
        "id": "rate_half_mca_rank11_kernel_rank8_nineshadow_extension_deficit",
        "path": "background/nodes/rate_half_mca_rank11_kernel_rank8_nineshadow_extension_deficit",
        "commit": "8c0dac47b86bec6b355fa174130aafee2c2e6b18",
        "tree": "0ddfc4509b2ccdcd818e89f0314a6d74f4e3aa67",
        "contract_sha256": "f78e2d0d08b3c4535a1ef2db02e2bde7956b4c0eebe67e3de2c8cebc0441ec2a",
    },
    "kernel_rank8_nine_shadow_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_rank8_nineshadow_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_rank8_nineshadow_capacity_cut",
        "commit": "8c0dac47b86bec6b355fa174130aafee2c2e6b18",
        "tree": "8780eadecc3902a9e90523186a93560393caec82",
        "contract_sha256": "bd95dca74b2f9018d78e9b89571d1175b7c5ad219bc48b6ec57167651d6835b3",
    },
    "kernel_two_step_nine_shadow_hierarchy": {
        "id": "rate_half_mca_rank11_kernel_two_step_nineshadow_hierarchy",
        "path": "background/nodes/rate_half_mca_rank11_kernel_two_step_nineshadow_hierarchy",
        "commit": "770a3823e2f9f80d98ba11fcc7b62711728657b8",
        "tree": "f737cb00316ac8c8471739adae997de23d46507b",
        "contract_sha256": "b62be3d37c39c2f482b2e50dcc638acf2c39fb49ebe14f56e11e7adb35eaf317",
    },
    "kernel_two_step_nine_shadow_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_two_step_nineshadow_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_two_step_nineshadow_capacity_cut",
        "commit": "770a3823e2f9f80d98ba11fcc7b62711728657b8",
        "tree": "828122e33c5e9799b22d3a21015c8c52ca27a4e7",
        "contract_sha256": "2e8396fb8eb41b2d3d4d9f8f6e13ab52bd51f814b348d2fcb00b98dbc04caaae",
    },
    "kernel_multistep_shadow_hierarchy": {
        "id": "rate_half_mca_rank11_kernel_multistep_shadow_hierarchy",
        "path": "background/nodes/rate_half_mca_rank11_kernel_multistep_shadow_hierarchy",
        "commit": "28b82fda1bb777ee6c609446d87a6322108b7c16",
        "tree": "058dda0c6c37a53a7f67693b33b0aaa294ab35e7",
        "contract_sha256": "c7561d9192a00cd97530d61adff244cccfec97ce248fbe23c6074d641c33053b",
    },
    "kernel_three_step_shadow_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_three_step_shadow_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_three_step_shadow_capacity_cut",
        "commit": "28b82fda1bb777ee6c609446d87a6322108b7c16",
        "tree": "948a43bb37ed08bc01ceea42dfa26a8b1e59c7a5",
        "contract_sha256": "1645081d2c338bd79210f3417f2520c14bfc72d0351af70fbb042b3ecd408636",
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
    "rank8_dense_owner_terminal_bridge": {
        "id": "rate_half_mca_rank11_rank8_dense_owner_terminal_bridge",
        "path": "background/nodes/rate_half_mca_rank11_rank8_dense_owner_terminal_bridge",
        "commit": "ab1551006e0da01a3357065cf218bc303e4a7098",
        "tree": "92bae9306cabf755ddf1b180ea6dcc8db3be3944",
        "contract_sha256": "c77779cfc39566264dbfa48bfe4081eb6c46a4913c579e21e1bcf204de13da67",
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


def independent_kernel_multibasis_capacity(kprime: int) -> int:
    total = 0
    for rank in range(9, 0, -1):
        dimension = 10 - rank
        extras = kprime - 10
        extensions = comb(extras, dimension + 1) if extras >= dimension + 1 else 0
        decorated = (
            comb(1048576 + kprime, rank)
            * independent_kernel_record_cap(kprime, rank)
            * extensions
        )
        total += decorated // (dimension + 2)
    return total


def independent_kernel_hybrid_terms(kprime: int) -> list[tuple[int, int, str]]:
    rows = []
    for rank in range(9, 0, -1):
        dimension = 10 - rank
        extension = comb(kprime - 10, dimension + 1)
        ambient = (
            comb(1048576 + kprime, rank)
            * independent_kernel_record_cap(kprime, rank)
            * extension
            // (dimension + 2)
        )
        support = (
            274980728111260126
            * (comb(67472 + kprime, rank) * extension // (dimension + 2))
        )
        rows.append((ambient, support, "ambient" if ambient <= support else "record"))
    return rows


def independent_kernel_hybrid_capacity(kprime: int) -> int:
    return sum(min(ambient, support) for ambient, support, _ in independent_kernel_hybrid_terms(kprime))


def independent_shadow_caps_weights(kprime: int) -> tuple[list[Fraction], list[Fraction]]:
    caps = []
    weights = []
    for dimension, (ambient, support, _) in enumerate(independent_kernel_hybrid_terms(kprime), 1):
        cap = Fraction(min(ambient, support), 274980728111260126)
        caps.append(cap)
        weights.append(
            Fraction(comb(dimension + 2, 2), comb(kprime - dimension - 9, 2))
            if cap else Fraction(0)
        )
    return caps, weights


def independent_nine_shadow_dual(kprime: int) -> tuple[Fraction, int]:
    caps, weights = independent_shadow_caps_weights(kprime)
    budget = Fraction(comb(67472 + kprime, 9))
    spent = Fraction(0)
    for index, (cap, weight) in enumerate(zip(caps, weights)):
        if cap and spent + weight * cap > budget:
            multiplier = 1 / weight
            bound = multiplier * budget
            for earlier in range(index):
                bound += (1 - multiplier * weights[earlier]) * caps[earlier]
            return bound, index + 1
        spent += weight * cap
    return sum(caps, Fraction(0)), 0


def independent_full_shadow_resource_dual(kprime: int) -> Fraction | None:
    if kprime < 13:
        return None
    budget = Fraction(comb(67472 + kprime, 9))
    support_extensions = Fraction(comb(67472 + kprime - 9, 2))
    rank9_extensions = Fraction(comb(kprime - 10, 2))
    rank8_extensions = Fraction(comb(kprime - 11, 2))
    w1 = Fraction(3, rank9_extensions)
    w2 = Fraction(6, rank8_extensions)
    v1 = 52 + 3 * support_extensions / rank9_extensions
    determinant = v1 * w2 - 55 * w1
    require(determinant > 0, f"full-shadow determinant {kprime}")
    lam = (v1 - 55) / determinant
    mu = (w2 - w1) / determinant
    require(lam >= 0 and mu >= 0, f"full-shadow dual signs {kprime}")
    require(lam * w1 + mu * v1 == 1, f"full-shadow dual d1 {kprime}")
    require(lam * w2 + 55 * mu == 1, f"full-shadow dual d2 {kprime}")
    for dimension in range(3, 10):
        if kprime - dimension - 9 < 2:
            continue
        weight = Fraction(comb(dimension + 2, 2), comb(kprime - dimension - 9, 2))
        require(lam * weight + 55 * mu >= 1, f"full-shadow dual d{dimension} {kprime}")
    return lam * budget + mu * support_extensions * budget


def independent_full_shadow_bound(kprime: int) -> Fraction:
    caps, _ = independent_shadow_caps_weights(kprime)
    individual = sum(caps, Fraction(0))
    dual = independent_full_shadow_resource_dual(kprime)
    return individual if dual is None else min(individual, dual)


def independent_rank8_shadow_primal(
    kprime: int, ledger: list[list[object]]
) -> tuple[Fraction, Fraction, Fraction, list[Fraction]]:
    caps, weights = independent_shadow_caps_weights(kprime)
    shadow_budget = Fraction(comb(67472 + kprime, 9))
    support_extensions = Fraction(comb(67472 + kprime - 9, 2))
    containment_budget = support_extensions * shadow_budget
    coefficients = []
    for dimension, cap in enumerate(caps, 1):
        if not cap:
            coefficients.append(Fraction(0))
        elif dimension == 1:
            coefficients.append(52 + 3 * support_extensions / comb(kprime - 10, 2))
        elif dimension == 2:
            coefficients.append(55 + Fraction(6 * comb(67474, 2), comb(kprime - 11, 2)))
        else:
            coefficients.append(Fraction(55))

    pattern = next(
        (row[2:] for row in ledger if row[0] <= kprime <= row[1]),
        None,
    )
    require(pattern is not None, f"rank-eight shadow ledger row {kprime}")
    tight, capped, zero = pattern
    active = {index + 1 for index, cap in enumerate(caps) if cap}
    require(active == set(tight) | set(capped) | set(zero), f"rank-eight shadow partition {kprime}")

    if not tight:
        lam, mu = Fraction(0), Fraction(0)
    elif len(tight) == 1:
        require(tight == [1], f"rank-eight shadow singleton {kprime}")
        lam, mu = Fraction(0), 1 / coefficients[0]
    else:
        require(len(tight) == 2, f"rank-eight shadow tight count {kprime}")
        left, right = tight[0] - 1, tight[1] - 1
        determinant = weights[left] * coefficients[right] - weights[right] * coefficients[left]
        lam = (coefficients[right] - coefficients[left]) / determinant
        mu = (weights[left] - weights[right]) / determinant
    require(lam >= 0 and mu >= 0, f"rank-eight shadow dual signs {kprime}")

    for dimension in active:
        coverage = lam * weights[dimension - 1] + mu * coefficients[dimension - 1]
        if dimension in tight:
            require(coverage == 1, f"rank-eight shadow tight d={dimension} K={kprime}")
        elif dimension in capped:
            require(coverage < 1, f"rank-eight shadow capped d={dimension} K={kprime}")
        else:
            require(coverage > 1, f"rank-eight shadow zero d={dimension} K={kprime}")

    allocation = [Fraction(0) for _ in range(9)]
    for dimension in capped:
        allocation[dimension - 1] = caps[dimension - 1]
    remaining_shadow = shadow_budget - sum(weights[i] * allocation[i] for i in range(9))
    remaining_containment = containment_budget - sum(
        coefficients[i] * allocation[i] for i in range(9)
    )
    if len(tight) == 1:
        allocation[tight[0] - 1] = remaining_containment / coefficients[tight[0] - 1]
    elif len(tight) == 2:
        left, right = tight[0] - 1, tight[1] - 1
        determinant = weights[left] * coefficients[right] - weights[right] * coefficients[left]
        allocation[left] = (
            remaining_shadow * coefficients[right] - weights[right] * remaining_containment
        ) / determinant
        allocation[right] = (
            weights[left] * remaining_containment - remaining_shadow * coefficients[left]
        ) / determinant
    require(all(0 <= value <= cap for value, cap in zip(allocation, caps)), f"rank-eight shadow bounds {kprime}")
    require(sum(weights[i] * allocation[i] for i in range(9)) <= shadow_budget, f"rank-eight shadow first resource {kprime}")
    require(sum(coefficients[i] * allocation[i] for i in range(9)) <= containment_budget, f"rank-eight shadow second resource {kprime}")

    dual = lam * shadow_budget + mu * containment_budget
    for dimension in capped:
        coverage = lam * weights[dimension - 1] + mu * coefficients[dimension - 1]
        dual += (1 - coverage) * caps[dimension - 1]
    primal = sum(allocation, Fraction(0))
    require(primal == dual, f"rank-eight shadow strong duality {kprime}")
    return primal, lam, mu, allocation


def independent_two_step_recurrence(
    kprime: int,
) -> tuple[Fraction, list[Fraction], Fraction, Fraction, dict[int, Fraction]]:
    caps, shadow = independent_shadow_caps_weights(kprime)
    shadow_budget = Fraction(comb(67472 + kprime, 9))
    support_extensions = Fraction(comb(67472 + kprime - 9, 2))
    containment_budget = support_extensions * shadow_budget
    containment = []
    for dimension in range(1, 10):
        if dimension == 1:
            containment.append(52 + Fraction(3 * support_extensions, comb(kprime - 10, 2)))
        elif dimension == 2:
            containment.append(55 + Fraction(6 * comb(67474, 2), comb(kprime - 11, 2)))
        else:
            containment.append(Fraction(55))
    raising = {
        dimension: Fraction(
            comb(dimension + 2, 2) * comb(67472 + dimension, 2),
            comb(kprime - dimension - 9, 2),
        )
        for dimension in range(3, 10)
    }
    multiplicity = {dimension: comb(11 - dimension, 2) for dimension in range(3, 10)}

    factors = [Fraction(1), Fraction(1)] + [Fraction(0) for _ in range(7)]
    for dimension in range(3, 10):
        factors[dimension - 1] = (
            multiplicity[dimension] * factors[dimension - 3] / raising[dimension]
        )
    odd_base = caps[0]
    odd_price = sum(containment[index] * factors[index] for index in range(0, 9, 2))
    even_price = sum(containment[index] * factors[index] for index in range(1, 9, 2))
    even_base = (containment_budget - odd_price * odd_base) / even_price
    allocation = [
        factor * (odd_base if index % 2 == 0 else even_base)
        for index, factor in enumerate(factors)
    ]

    def hierarchy_multipliers(mu: Fraction) -> dict[int, Fraction]:
        values: dict[int, Fraction] = {}
        for parity_top in (9, 8):
            for dimension in range(parity_top, 2, -2):
                child = (
                    multiplicity[dimension + 2] * values[dimension + 2]
                    if dimension + 2 <= 9
                    else Fraction(0)
                )
                values[dimension] = (
                    1 - mu * containment[dimension - 1] + child
                ) / raising[dimension]
        return values

    def even_equation(mu: Fraction) -> Fraction:
        values = hierarchy_multipliers(mu)
        return mu * containment[1] - multiplicity[4] * values[4] - 1

    at_zero, at_one = even_equation(Fraction(0)), even_equation(Fraction(1))
    mu = -at_zero / (at_one - at_zero)
    hierarchy_dual = hierarchy_multipliers(mu)
    eta = 1 - mu * containment[0] + multiplicity[3] * hierarchy_dual[3]
    require(mu >= 0 and eta >= 0, f"two-step base dual signs {kprime}")
    require(all(value >= 0 for value in hierarchy_dual.values()), f"two-step hierarchy dual signs {kprime}")
    for dimension in range(1, 10):
        coverage = mu * containment[dimension - 1]
        if dimension == 1:
            coverage += eta
        if dimension >= 3:
            coverage += raising[dimension] * hierarchy_dual[dimension]
        if dimension + 2 <= 9:
            coverage -= multiplicity[dimension + 2] * hierarchy_dual[dimension + 2]
        require(coverage == 1, f"two-step dual equality d={dimension} K={kprime}")

    require(all(0 < value <= cap for value, cap in zip(allocation, caps)), f"two-step primal caps {kprime}")
    require(allocation[0] == caps[0], f"two-step primal cap equality {kprime}")
    require(sum(shadow[i] * allocation[i] for i in range(9)) < shadow_budget, f"two-step shadow slack {kprime}")
    require(sum(containment[i] * allocation[i] for i in range(9)) == containment_budget, f"two-step containment {kprime}")
    for dimension in range(3, 10):
        require(
            raising[dimension] * allocation[dimension - 1]
            == multiplicity[dimension] * allocation[dimension - 3],
            f"two-step primal d={dimension} K={kprime}",
        )
    optimum = sum(allocation, Fraction(0))
    require(mu * containment_budget + eta * caps[0] == optimum, f"two-step strong duality {kprime}")
    return optimum, allocation, mu, eta, hierarchy_dual


def independent_multistep_recurrence(
    kprime: int,
    tree_rows: list[list[int]],
) -> tuple[Fraction, list[Fraction], Fraction, Fraction, dict[tuple[int, int], Fraction]]:
    caps, shadow = independent_shadow_caps_weights(kprime)
    shadow_budget = Fraction(comb(67472 + kprime, 9))
    support_extensions = Fraction(comb(67472 + kprime - 9, 2))
    containment_budget = support_extensions * shadow_budget
    containment = []
    for dimension in range(1, 10):
        if dimension == 1:
            containment.append(52 + Fraction(3 * support_extensions, comb(kprime - 10, 2)))
        elif dimension == 2:
            containment.append(55 + Fraction(6 * comb(67474, 2), comb(kprime - 11, 2)))
        else:
            containment.append(Fraction(55))

    def edge_data(step: int, source: int) -> tuple[Fraction, int]:
        return (
            Fraction(
                comb(source + 2, step) * comb(67472 + source, step),
                comb(kprime - source - 11 + step, step),
            ),
            comb(9 - source + step, step),
        )

    tree = [tuple(row) for row in tree_rows]
    parent = {source: (step, source) for step, source in tree}
    children: dict[int, list[tuple[int, int]]] = {dimension: [] for dimension in range(1, 10)}
    for step, source in tree:
        children[source - step].append((step, source))

    factors = [Fraction(0) for _ in range(9)]
    roots = [0 for _ in range(9)]
    factors[0] = factors[1] = Fraction(1)
    roots[0], roots[1] = 1, 2
    for source in range(3, 10):
        if source not in parent:
            continue
        step, _ = parent[source]
        target = source - step
        require(roots[target - 1] != 0, f"multistep tree order source={source}")
        raising, multiplicity = edge_data(step, source)
        factors[source - 1] = multiplicity * factors[target - 1] / raising
        roots[source - 1] = roots[target - 1]
    require(all(roots), f"multistep tree spans K={kprime}")

    first_base = caps[0]
    first_price = sum(containment[i] * factors[i] for i in range(9) if roots[i] == 1)
    second_price = sum(containment[i] * factors[i] for i in range(9) if roots[i] == 2)
    second_base = (containment_budget - first_price * first_base) / second_price
    allocation = [
        factors[i] * (first_base if roots[i] == 1 else second_base)
        for i in range(9)
    ]

    def tree_multipliers(mu: Fraction) -> dict[tuple[int, int], Fraction]:
        values: dict[tuple[int, int], Fraction] = {}
        for source in range(9, 2, -1):
            if source not in parent:
                continue
            edge = parent[source]
            raising, _ = edge_data(*edge)
            child_charge = sum(
                edge_data(*child)[1] * values[child]
                for child in children[source]
            )
            values[edge] = (1 - mu * containment[source - 1] + child_charge) / raising
        return values

    def root_two_equation(mu: Fraction) -> Fraction:
        values = tree_multipliers(mu)
        child_charge = sum(
            edge_data(*child)[1] * values[child]
            for child in children[2]
        )
        return mu * containment[1] - child_charge - 1

    at_zero, at_one = root_two_equation(Fraction(0)), root_two_equation(Fraction(1))
    mu = -at_zero / (at_one - at_zero)
    hierarchy_dual = tree_multipliers(mu)
    root_one_charge = sum(
        edge_data(*child)[1] * hierarchy_dual[child]
        for child in children[1]
    )
    eta = 1 - mu * containment[0] + root_one_charge
    require(mu >= 0 and eta >= 0, f"multistep root dual signs K={kprime}")
    require(all(value >= 0 for value in hierarchy_dual.values()), f"multistep tree dual signs K={kprime}")
    for dimension in range(1, 10):
        coverage = mu * containment[dimension - 1]
        if dimension == 1:
            coverage += eta
        if dimension in parent:
            raising, _ = edge_data(*parent[dimension])
            coverage += raising * hierarchy_dual[parent[dimension]]
        coverage -= sum(
            edge_data(*child)[1] * hierarchy_dual[child]
            for child in children[dimension]
        )
        require(coverage == 1, f"multistep dual equality d={dimension} K={kprime}")

    require(all(0 < value <= cap for value, cap in zip(allocation, caps)), f"multistep primal caps K={kprime}")
    require(allocation[0] == caps[0], f"multistep cap equality K={kprime}")
    require(sum(shadow[i] * allocation[i] for i in range(9)) < shadow_budget, f"multistep shadow slack K={kprime}")
    require(sum(containment[i] * allocation[i] for i in range(9)) == containment_budget, f"multistep containment K={kprime}")
    for step in range(2, 9):
        for source in range(step + 1, 10):
            raising, multiplicity = edge_data(step, source)
            require(
                raising * allocation[source - 1] <= multiplicity * allocation[source - step - 1],
                f"multistep hierarchy t={step} d={source} K={kprime}",
            )
    optimum = sum(allocation, Fraction(0))
    require(mu * containment_budget + eta * caps[0] == optimum, f"multistep strong duality K={kprime}")
    return optimum, allocation, mu, eta, hierarchy_dual


def independent_kernel_demand(kprime: int) -> int:
    return ceiling(
        Fraction(
            495405467 * 274980728111260126 * comb(67472 + kprime, 11),
            10**9,
        )
    )


def independent_kernel_demand_ratio(kprime: int) -> Fraction:
    return Fraction(495405467 * comb(67472 + kprime, 11), 10**9)


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
    kernel_multibasis = data["kernel_multibasis_decoration_compression"]
    kernel_multibasis_cut = data["kernel_multibasis_capacity_cut"]
    kernel_record_support = data["kernel_record_support_capacity"]
    kernel_hybrid_cut = data["kernel_hybrid_capacity_cut"]
    kernel_shadow_coupling = data["kernel_nine_shadow_coupling"]
    kernel_shadow_cut = data["kernel_nine_shadow_capacity_cut"]
    kernel_containment = data["kernel_nine_shadow_containment_coupling"]
    kernel_containment_cut = data["kernel_nine_shadow_containment_capacity_cut"]
    kernel_rank8_shadow_deficit = data["kernel_rank8_nine_shadow_extension_deficit"]
    kernel_rank8_shadow_cut = data["kernel_rank8_nine_shadow_capacity_cut"]
    kernel_two_step_hierarchy = data["kernel_two_step_nine_shadow_hierarchy"]
    kernel_two_step_cut = data["kernel_two_step_nine_shadow_capacity_cut"]
    kernel_multistep_hierarchy = data["kernel_multistep_shadow_hierarchy"]
    kernel_multistep_cut = data["kernel_three_step_shadow_capacity_cut"]
    rank8_owner_cap = data["rank8_owner_pair_weight_cap"]
    rank8_cut = data["rank8_weighted_capacity_cut"]
    dense_owner = data["rank8_dense_owner_terminal_bridge"]
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
    require(kernel_multibasis == {
        "correction_dimension": 10,
        "component_subset_size": 11,
        "global_common_zero_count": 0,
        "basis_multiplicities": [d + 2 for d in range(1, 10)],
        "capacity_formula": "floor(C(n_prime,10-d)*M_d*C(K_prime-10,d+1)/(d+2))",
    }, "kernel multi-basis constants")
    multibasis_checks = 0
    for kprime in range(10, 11642):
        require(
            independent_kernel_demand(kprime) > independent_kernel_multibasis_capacity(kprime),
            f"kernel multi-basis capacity {kprime}",
        )
        multibasis_checks += 1
    multibasis_endpoint_demand = independent_kernel_demand(11641)
    multibasis_endpoint_capacity = independent_kernel_multibasis_capacity(11641)
    multibasis_wall_demand = independent_kernel_demand(11642)
    multibasis_wall_capacity = independent_kernel_multibasis_capacity(11642)
    require(kernel_multibasis_cut == {
        "closed_K_prime_minimum": 10,
        "closed_K_prime_maximum": 11641,
        "first_open_K_prime": 11642,
        "endpoint_demand": multibasis_endpoint_demand,
        "endpoint_capacity": multibasis_endpoint_capacity,
        "endpoint_gap": multibasis_endpoint_demand - multibasis_endpoint_capacity,
        "wall_demand": multibasis_wall_demand,
        "wall_capacity": multibasis_wall_capacity,
        "wall_excess": multibasis_wall_capacity - multibasis_wall_demand,
        "capacity_formula": "sum_d floor(C(n_prime,10-d)*M_d*C(K_prime-10,d+1)/(d+2))",
    }, "kernel multi-basis capacity constants")
    require(multibasis_wall_capacity > multibasis_wall_demand, "kernel multi-basis wall")
    require(kernel_record_support == {
        "correction_dimension": 10,
        "component_subset_size": 11,
        "basis_multiplicities": [d + 2 for d in range(1, 10)],
        "capacity_formula": "floor(C(m_prime,10-d)*C(K_prime-10,d+1)/(d+2))",
    }, "kernel record-support constants")
    hybrid_checks = 0
    for kprime in range(10, 11773):
        require(
            independent_kernel_demand(kprime) > independent_kernel_hybrid_capacity(kprime),
            f"kernel hybrid capacity {kprime}",
        )
        hybrid_checks += 1
    hybrid_endpoint_demand = independent_kernel_demand(11772)
    hybrid_endpoint_capacity = independent_kernel_hybrid_capacity(11772)
    hybrid_wall_demand = independent_kernel_demand(11773)
    hybrid_wall_capacity = independent_kernel_hybrid_capacity(11773)
    hybrid_branches = [choice for _, _, choice in independent_kernel_hybrid_terms(11772)]
    require(kernel_hybrid_cut == {
        "closed_K_prime_minimum": 10,
        "closed_K_prime_maximum": 11772,
        "first_open_K_prime": 11773,
        "endpoint_branch_pattern": hybrid_branches,
        "endpoint_demand": hybrid_endpoint_demand,
        "endpoint_capacity": hybrid_endpoint_capacity,
        "endpoint_gap": hybrid_endpoint_demand - hybrid_endpoint_capacity,
        "wall_demand": hybrid_wall_demand,
        "wall_capacity": hybrid_wall_capacity,
        "wall_excess": hybrid_wall_capacity - hybrid_wall_demand,
        "capacity_formula": "sum_d min(A_d,N_min*P_d)",
    }, "kernel hybrid capacity constants")
    require(hybrid_branches == ["ambient", "ambient"] + ["record"] * 7, "kernel hybrid branches")
    require(hybrid_wall_capacity > hybrid_wall_demand, "kernel hybrid wall")

    require(kernel_shadow_coupling == {
        "correction_dimension": 10,
        "component_subset_size": 11,
        "shadow_subset_size": 9,
        "spanning_shadow_coefficients": [3, 6, 10, 15, 21, 28, 36, 45, 55],
        "extension_formula": "C(K_prime-d-9,2)",
        "resource_formula": "sum_d C(d+2,2)*I_d/C(K_prime-d-9,2) <= C(m_prime,9)",
    }, "kernel nine-shadow coupling")
    shadow_checks = 0
    for kprime in range(10, 15446):
        bound, _ = independent_nine_shadow_dual(kprime)
        require(independent_kernel_demand_ratio(kprime) > bound, f"kernel nine-shadow dual {kprime}")
        shadow_checks += 1
    shadow_endpoint_optimum, shadow_endpoint_frontier = independent_nine_shadow_dual(15445)
    shadow_wall_optimum, shadow_wall_frontier = independent_nine_shadow_dual(15446)
    shadow_endpoint_scaled = 274980728111260126 * shadow_endpoint_optimum
    shadow_wall_scaled = 274980728111260126 * shadow_wall_optimum
    shadow_endpoint_capacity = shadow_endpoint_scaled.numerator // shadow_endpoint_scaled.denominator
    shadow_wall_capacity = shadow_wall_scaled.numerator // shadow_wall_scaled.denominator
    shadow_endpoint_demand = independent_kernel_demand(15445)
    shadow_wall_demand = independent_kernel_demand(15446)
    require(kernel_shadow_cut == {
        "closed_K_prime_minimum": 10,
        "closed_K_prime_maximum": 15445,
        "first_open_K_prime": 15446,
        "endpoint_branch_pattern": [choice for _, _, choice in independent_kernel_hybrid_terms(15445)],
        "endpoint_frontier_corank": shadow_endpoint_frontier,
        "endpoint_active_coranks": [1, 2],
        "wall_frontier_corank": shadow_wall_frontier,
        "wall_active_coranks": [1, 2],
        "endpoint_demand": shadow_endpoint_demand,
        "endpoint_capacity": shadow_endpoint_capacity,
        "endpoint_gap": shadow_endpoint_demand - shadow_endpoint_capacity,
        "wall_demand": shadow_wall_demand,
        "wall_capacity": shadow_wall_capacity,
        "wall_excess": shadow_wall_capacity - shadow_wall_demand,
        "capacity_formula": "fractional knapsack under the shared rank-preserving nine-shadow resource",
    }, "kernel nine-shadow capacity constants")
    require(shadow_endpoint_frontier == shadow_wall_frontier == 2, "kernel nine-shadow frontier")
    require(independent_kernel_demand_ratio(15446) < shadow_wall_optimum, "kernel nine-shadow wall")

    require(kernel_containment == {
        "shadows_per_eleven_subset": 55,
        "rank9_spanning_shadow_minimum": 3,
        "support_extension_formula": "C(m_prime-9,2)",
        "rank9_extension_formula": "C(K_prime-10,2)",
        "rank9_coefficient_formula": "52+3*C(m_prime-9,2)/C(K_prime-10,2)",
        "resource_formula": "rank9_coefficient*I_1+55*sum_d_ge_2 I_d <= C(m_prime-9,2)*C(m_prime,9)",
    }, "kernel full-containment coupling")
    containment_checks = 0
    for kprime in range(10, 15671):
        require(
            independent_kernel_demand_ratio(kprime) > independent_full_shadow_bound(kprime),
            f"kernel full-shadow dual {kprime}",
        )
        containment_checks += 1
    containment_endpoint_optimum = independent_full_shadow_resource_dual(15670)
    containment_wall_optimum = independent_full_shadow_resource_dual(15671)
    require(containment_endpoint_optimum is not None and containment_wall_optimum is not None, "full-shadow boundary duals")
    containment_endpoint_scaled = 274980728111260126 * containment_endpoint_optimum
    containment_wall_scaled = 274980728111260126 * containment_wall_optimum
    containment_endpoint_capacity = containment_endpoint_scaled.numerator // containment_endpoint_scaled.denominator
    containment_wall_capacity = containment_wall_scaled.numerator // containment_wall_scaled.denominator
    containment_endpoint_demand = independent_kernel_demand(15670)
    containment_wall_demand = independent_kernel_demand(15671)
    require(kernel_containment_cut == {
        "closed_K_prime_minimum": 10,
        "closed_K_prime_maximum": 15670,
        "first_open_K_prime": 15671,
        "endpoint_branch_pattern": [choice for _, _, choice in independent_kernel_hybrid_terms(15670)],
        "endpoint_active_coranks": [1, 2],
        "endpoint_active_resources": ["rank_preserving_nine_shadow", "full_containment_nine_shadow"],
        "endpoint_optimum_numerator": containment_endpoint_optimum.numerator,
        "endpoint_optimum_denominator": containment_endpoint_optimum.denominator,
        "endpoint_demand": containment_endpoint_demand,
        "endpoint_capacity": containment_endpoint_capacity,
        "endpoint_gap": containment_endpoint_demand - containment_endpoint_capacity,
        "wall_optimum_numerator": containment_wall_optimum.numerator,
        "wall_optimum_denominator": containment_wall_optimum.denominator,
        "wall_demand": containment_wall_demand,
        "wall_capacity": containment_wall_capacity,
        "wall_excess": containment_wall_capacity - containment_wall_demand,
        "capacity_formula": "exact two-resource LP with individual ambient/record caps",
    }, "kernel full-shadow capacity constants")
    require(independent_kernel_demand_ratio(15671) < containment_wall_optimum, "kernel full-shadow wall")

    require(kernel_rank8_shadow_deficit == {
        "rank8_closure_offset": 2,
        "outside_rank8_closure_minimum": 67474,
        "outside_parallel_class_partner_minimum": 67473,
        "independent_pair_floor": comb(67474, 2),
        "rank8_bad_extension_formula": "C(m_prime-9,2)-C(67474,2)",
        "rank8_resource_coefficient_formula": "55+6*C(67474,2)/C(K_prime-11,2)",
        "resource_formula": "[52+3*E0/E1]*I1+[55+6*C(67474,2)/E2]*I2+55*sum_d_ge_3 I_d <= E0*C(m_prime,9)",
    }, "rank-eight nine-shadow extension deficit")
    require(comb(67474, 2) == 2276336601, "rank-eight independent-pair floor")
    rank8_shadow_checks = 0
    rank8_shadow_ledger = kernel_rank8_shadow_cut["pattern_ledger"]
    for kprime in range(10, 17609):
        optimum, _, _, _ = independent_rank8_shadow_primal(kprime, rank8_shadow_ledger)
        require(independent_kernel_demand_ratio(kprime) > optimum, f"rank-eight shadow primal {kprime}")
        rank8_shadow_checks += 1
    rank8_shadow_endpoint = independent_rank8_shadow_primal(17608, rank8_shadow_ledger)
    rank8_shadow_wall = independent_rank8_shadow_primal(17609, rank8_shadow_ledger)
    rank8_shadow_endpoint_scaled = 274980728111260126 * rank8_shadow_endpoint[0]
    rank8_shadow_wall_scaled = 274980728111260126 * rank8_shadow_wall[0]
    rank8_shadow_endpoint_capacity = rank8_shadow_endpoint_scaled.numerator // rank8_shadow_endpoint_scaled.denominator
    rank8_shadow_wall_capacity = rank8_shadow_wall_scaled.numerator // rank8_shadow_wall_scaled.denominator
    rank8_shadow_endpoint_demand = independent_kernel_demand(17608)
    rank8_shadow_wall_demand = independent_kernel_demand(17609)
    require(kernel_rank8_shadow_cut["closed_K_prime_maximum"] == 17608, "rank-eight shadow endpoint row")
    require(kernel_rank8_shadow_cut["first_open_K_prime"] == 17609, "rank-eight shadow wall row")
    require(kernel_rank8_shadow_cut["endpoint_tight_coranks"] == [2, 4], "rank-eight shadow endpoint tight")
    require(kernel_rank8_shadow_cut["endpoint_capped_coranks"] == [1, 3], "rank-eight shadow endpoint capped")
    require(kernel_rank8_shadow_cut["endpoint_zero_coranks"] == [5, 6, 7, 8, 9], "rank-eight shadow endpoint zero")
    require(rank8_shadow_endpoint[0] == Fraction(kernel_rank8_shadow_cut["endpoint_optimum_numerator"], kernel_rank8_shadow_cut["endpoint_optimum_denominator"]), "rank-eight shadow endpoint optimum")
    require(rank8_shadow_wall[0] == Fraction(kernel_rank8_shadow_cut["wall_optimum_numerator"], kernel_rank8_shadow_cut["wall_optimum_denominator"]), "rank-eight shadow wall optimum")
    require(rank8_shadow_endpoint[1] == Fraction(kernel_rank8_shadow_cut["endpoint_dual_lambda_numerator"], kernel_rank8_shadow_cut["endpoint_dual_lambda_denominator"]), "rank-eight shadow endpoint lambda")
    require(rank8_shadow_endpoint[2] == Fraction(kernel_rank8_shadow_cut["endpoint_dual_mu_numerator"], kernel_rank8_shadow_cut["endpoint_dual_mu_denominator"]), "rank-eight shadow endpoint mu")
    require(rank8_shadow_wall[1] == Fraction(kernel_rank8_shadow_cut["wall_dual_lambda_numerator"], kernel_rank8_shadow_cut["wall_dual_lambda_denominator"]), "rank-eight shadow wall lambda")
    require(rank8_shadow_wall[2] == Fraction(kernel_rank8_shadow_cut["wall_dual_mu_numerator"], kernel_rank8_shadow_cut["wall_dual_mu_denominator"]), "rank-eight shadow wall mu")
    require(rank8_shadow_endpoint_capacity == kernel_rank8_shadow_cut["endpoint_capacity"], "rank-eight shadow endpoint capacity")
    require(rank8_shadow_wall_capacity == kernel_rank8_shadow_cut["wall_capacity"], "rank-eight shadow wall capacity")
    require(rank8_shadow_endpoint_demand - rank8_shadow_endpoint_capacity == 126547040539829546354916747965612889135249249684319416999204, "rank-eight shadow endpoint gap")
    require(rank8_shadow_wall_capacity - rank8_shadow_wall_demand == 165662859003771823867021831078593815988062146919602894849014, "rank-eight shadow wall excess")
    require(independent_kernel_demand_ratio(17609) < rank8_shadow_wall[0], "rank-eight shadow wall")

    expected_hierarchy = [
        [
            dimension,
            comb(dimension + 2, 2),
            67472 + dimension,
            67471 + dimension,
            comb(67472 + dimension, 2),
            11 - dimension,
            comb(11 - dimension, 2),
        ]
        for dimension in range(3, 10)
    ]
    require(kernel_two_step_hierarchy == {
        "support_offset": 67472,
        "corank_minimum": 3,
        "corank_maximum": 9,
        "couplings": expected_hierarchy,
        "same_rank_extension_formula": "C(K_prime-d-9,2)",
        "inequality_formula": "C(d+2,2)*C(67472+d,2)*I_d/C(K_prime-d-9,2) <= C(11-d,2)*I_(d-2)",
    }, "two-step hierarchy")
    closure_checks = 0
    for dimension, _, _, _, pair_floor, coloop_cap, multiplicity in expected_hierarchy:
        for kprime in (dimension + 11, 101, 17609, 18102):
            mprime = 67472 + kprime
            for closure_size in range(kprime - dimension + 1):
                outside = mprime - closure_size
                parallel_cap = kprime - dimension + 1 - closure_size
                require(outside * (outside - parallel_cap) // 2 >= pair_floor, f"two-step pair d={dimension} K={kprime}")
                closure_checks += 1
        require(coloop_cap == 11 - dimension, f"two-step coloop cap d={dimension}")
        require(multiplicity == comb(coloop_cap, 2), f"two-step multiplicity d={dimension}")

    two_step_checks = 0
    for kprime in range(17609, 18102):
        optimum, allocation, _, _, hierarchy_dual = independent_two_step_recurrence(kprime)
        require(independent_kernel_demand_ratio(kprime) > optimum, f"two-step recurrence {kprime}")
        require(all(value > 0 for value in allocation), f"two-step allocation {kprime}")
        require(len(hierarchy_dual) == 7, f"two-step dual count {kprime}")
        two_step_checks += 1
    two_step_endpoint = independent_two_step_recurrence(18101)[0]
    two_step_wall = independent_two_step_recurrence(18102)[0]
    two_step_endpoint_scaled = 274980728111260126 * two_step_endpoint
    two_step_wall_scaled = 274980728111260126 * two_step_wall
    two_step_endpoint_capacity = two_step_endpoint_scaled.numerator // two_step_endpoint_scaled.denominator
    two_step_wall_capacity = two_step_wall_scaled.numerator // two_step_wall_scaled.denominator
    two_step_endpoint_demand = independent_kernel_demand(18101)
    two_step_wall_demand = independent_kernel_demand(18102)
    require(kernel_two_step_cut == {
        "previous_closed_K_prime": 17608,
        "replay_K_prime_minimum": 17609,
        "closed_K_prime_maximum": 18101,
        "first_open_K_prime": 18102,
        "replay_rows": 494,
        "endpoint_branch_pattern": [choice for _, _, choice in independent_kernel_hybrid_terms(18101)],
        "active_individual_caps": [1],
        "active_shared_resources": ["full_containment_nine_shadow"],
        "slack_shared_resources": ["rank_preserving_nine_shadow"],
        "active_hierarchy_coranks": list(range(3, 10)),
        "positive_coranks": list(range(1, 10)),
        "endpoint_optimum_numerator": two_step_endpoint.numerator,
        "endpoint_optimum_denominator": two_step_endpoint.denominator,
        "endpoint_demand": two_step_endpoint_demand,
        "endpoint_capacity": two_step_endpoint_capacity,
        "endpoint_gap": two_step_endpoint_demand - two_step_endpoint_capacity,
        "wall_optimum_numerator": two_step_wall.numerator,
        "wall_optimum_denominator": two_step_wall.denominator,
        "wall_demand": two_step_wall_demand,
        "wall_capacity": two_step_wall_capacity,
        "wall_excess": two_step_wall_capacity - two_step_wall_demand,
        "capacity_formula": "exact full-containment plus two-step hierarchy LP with individual ambient/record caps",
    }, "two-step capacity constants")
    require(two_step_checks == 493, "two-step replay count")
    require(two_step_endpoint_demand - two_step_endpoint_capacity == 33462159928103132226516704640419847248244116666500998762314, "two-step endpoint gap")
    require(two_step_wall_capacity - two_step_wall_demand == 275016496133605602641019628236447268989861205055439981187167, "two-step wall excess")
    require(independent_kernel_demand_ratio(18102) < two_step_wall, "two-step wall")

    expected_multistep_rows = [
        [
            step,
            dimension,
            comb(dimension + 2, step),
            67472 + dimension,
            comb(67472 + dimension, step),
            9 - dimension + step,
            comb(9 - dimension + step, step),
        ]
        for step in range(2, 9)
        for dimension in range(step + 1, 10)
    ]
    require(kernel_multistep_hierarchy == {
        "support_offset": 67472,
        "corank_minimum": 3,
        "corank_maximum": 9,
        "step_minimum": 2,
        "coupling_count": 28,
        "couplings": expected_multistep_rows,
        "triple_couplings": [row[1:] for row in expected_multistep_rows if row[0] == 3],
        "spanning_shadow_formula": "C(d+2,t)",
        "same_rank_extension_formula": "C(K_prime-d-11+t,t)",
        "rank_raising_extension_formula": "C(67472+d,t)",
        "target_multiplicity_formula": "C(9-d+t,t)",
        "inequality_formula": "C(d+2,t)*C(67472+d,t)*I_d/C(K_prime-d-11+t,t) <= C(9-d+t,t)*I_(d-t)",
    }, "multistep hierarchy")
    multistep_recurrence_checks = 0
    for step, dimension, shadows, outside, raising_floor, coloops, multiplicity in expected_multistep_rows:
        require(shadows == comb(dimension + 2, step), f"multistep shadow recurrence t={step} d={dimension}")
        require(raising_floor == comb(outside, step), f"multistep raising recurrence t={step} d={dimension}")
        require(multiplicity == comb(coloops, step), f"multistep reverse recurrence t={step} d={dimension}")
        multistep_recurrence_checks += 1
    multistep_tree = [[2, 3], [2, 4], [2, 6], [2, 8], [3, 5], [2, 7], [2, 9]]
    multistep_checks = 0
    for kprime in range(18102, 18159):
        optimum, allocation, mu, eta, hierarchy_dual = independent_multistep_recurrence(kprime, multistep_tree)
        require(independent_kernel_demand_ratio(kprime) > optimum, f"multistep recurrence {kprime}")
        require(all(value > 0 for value in allocation), f"multistep allocation {kprime}")
        require(mu >= 0 and eta >= 0 and len(hierarchy_dual) == 7, f"multistep dual {kprime}")
        multistep_checks += 1
    multistep_endpoint = independent_multistep_recurrence(18158, multistep_tree)[0]
    multistep_wall = independent_multistep_recurrence(18159, multistep_tree)[0]
    multistep_endpoint_scaled = 274980728111260126 * multistep_endpoint
    multistep_wall_scaled = 274980728111260126 * multistep_wall
    multistep_endpoint_capacity = multistep_endpoint_scaled.numerator // multistep_endpoint_scaled.denominator
    multistep_wall_capacity = multistep_wall_scaled.numerator // multistep_wall_scaled.denominator
    multistep_endpoint_demand = independent_kernel_demand(18158)
    multistep_wall_demand = independent_kernel_demand(18159)
    tight_rows = [
        [2, 3], [2, 4], [2, 6], [2, 7], [2, 8], [2, 9],
        [3, 5], [3, 7], [3, 8], [3, 9],
        [4, 6], [4, 8], [4, 9],
        [5, 7], [5, 9], [6, 8], [7, 9],
    ]
    require(kernel_multistep_cut == {
        "previous_closed_K_prime": 18101,
        "replay_K_prime_minimum": 18102,
        "closed_K_prime_maximum": 18158,
        "first_open_K_prime": 18159,
        "replay_rows": 58,
        "endpoint_branch_pattern": [choice for _, _, choice in independent_kernel_hybrid_terms(18158)],
        "active_individual_caps": [1],
        "active_shared_resources": ["full_containment_nine_shadow"],
        "slack_shared_resources": ["rank_preserving_nine_shadow"],
        "positive_coranks": list(range(1, 10)),
        "dual_tree": multistep_tree,
        "tight_hierarchy_rows": tight_rows,
        "endpoint_optimum_numerator": multistep_endpoint.numerator,
        "endpoint_optimum_denominator": multistep_endpoint.denominator,
        "endpoint_demand": multistep_endpoint_demand,
        "endpoint_capacity": multistep_endpoint_capacity,
        "endpoint_gap": multistep_endpoint_demand - multistep_endpoint_capacity,
        "wall_optimum_numerator": multistep_wall.numerator,
        "wall_optimum_denominator": multistep_wall.denominator,
        "wall_demand": multistep_wall_demand,
        "wall_capacity": multistep_wall_capacity,
        "wall_excess": multistep_wall_capacity - multistep_wall_demand,
        "capacity_formula": "exact full-containment plus all-step hierarchy LP with individual ambient/record caps",
    }, "multistep capacity constants")
    require(multistep_recurrence_checks == 28, "multistep hierarchy recurrence count")
    require(multistep_checks == 57, "multistep replay count")
    require(multistep_endpoint_demand - multistep_endpoint_capacity == 289110608820324799941118306538399899258195112067661304310498, "multistep endpoint gap")
    require(multistep_wall_capacity - multistep_wall_demand == 20286290696334777989469267474876769475675508046109372076445, "multistep wall excess")
    require(independent_kernel_demand_ratio(18159) < multistep_wall, "multistep wall")

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
    dense_last_weight = independent_rank8_demand(22525)
    dense_last_pairs = (1048576 + 22525 - 9) * (1048576 + 22525 - 10) // 2
    dense_first_weight = independent_rank8_demand(22526)
    dense_first_pairs = (1048576 + 22526 - 9) * (1048576 + 22526 - 10) // 2
    require(dense_owner == {
        "last_unforced_K_prime": 22525,
        "last_unforced_deficit": 200631 * dense_last_pairs - dense_last_weight,
        "first_forced_K_prime": 22526,
        "first_forced_excess": dense_first_weight - 200631 * dense_first_pairs,
        "owner_record_floor": 200632,
        "owner_core_deficiency_ceiling": 4,
        "delta5_record_cap": 196221,
        "terminal_interval_maximum": 37995,
    }, "dense-owner terminal bridge")
    require(1 + 981104 // 5 == dense_owner["delta5_record_cap"] < dense_owner["owner_record_floor"], "dense-owner deficiency")

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
        "kernel_dominant_lane_closed_through_Kprime": 18158,
        "rank8_owner_flat_closed_from_Kprime": 37996,
        "rank8_dense_owner_terminal_from_Kprime": 22526,
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
        f"multibasis_checks={multibasis_checks} "
        f"multibasis_endpoint_gap={multibasis_endpoint_demand-multibasis_endpoint_capacity} "
        f"multibasis_wall_excess={multibasis_wall_capacity-multibasis_wall_demand} "
        f"hybrid_checks={hybrid_checks} "
        f"hybrid_endpoint_gap={hybrid_endpoint_demand-hybrid_endpoint_capacity} "
        f"hybrid_wall_excess={hybrid_wall_capacity-hybrid_wall_demand} "
        f"shadow_checks={shadow_checks} "
        f"shadow_endpoint_gap={shadow_endpoint_demand-shadow_endpoint_capacity} "
        f"shadow_wall_excess={shadow_wall_capacity-shadow_wall_demand} "
        f"containment_checks={containment_checks} "
        f"containment_endpoint_gap={containment_endpoint_demand-containment_endpoint_capacity} "
        f"containment_wall_excess={containment_wall_capacity-containment_wall_demand} "
        f"rank8_shadow_checks={rank8_shadow_checks} "
        f"rank8_shadow_endpoint_gap={rank8_shadow_endpoint_demand-rank8_shadow_endpoint_capacity} "
        f"rank8_shadow_wall_excess={rank8_shadow_wall_capacity-rank8_shadow_wall_demand} "
        f"two_step_checks={two_step_checks+1} "
        f"two_step_closure_checks={closure_checks} "
        f"two_step_endpoint_gap={two_step_endpoint_demand-two_step_endpoint_capacity} "
        f"two_step_wall_excess={two_step_wall_capacity-two_step_wall_demand} "
        f"multistep_hierarchy_checks={multistep_recurrence_checks} "
        f"multistep_checks={multistep_checks+1} "
        f"multistep_endpoint_gap={multistep_endpoint_demand-multistep_endpoint_capacity} "
        f"multistep_wall_excess={multistep_wall_capacity-multistep_wall_demand} "
        f"rank8_last_gap={rank8_last_cap-rank8_last_demand} "
        f"rank8_first_gap={rank8_first_demand-rank8_first_cap} "
        f"rank8_monotone_factors={monotone_factors} "
        f"dense_owner_first_excess={dense_owner['first_forced_excess']} "
        f"toy_points={points} toy_slopes={slopes} design_pairs={design_pairs}"
    )


if __name__ == "__main__":
    main()
