#!/usr/bin/env python3
"""Verify the KoalaBear rank-11 dense-locator/split-pencil packet."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from fractions import Fraction
from functools import cache
from math import comb, isqrt, prod
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


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def ceil_ratio(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def falling(value: int, length: int) -> int:
    return prod(range(value - length + 1, value + 1))


def rising(value: int, length: int) -> int:
    return prod(range(value, value + length))


def kernel_record_cap(kprime: int, dimension: int) -> int:
    if dimension == 9:
        return 61871313426630599
    rank = 10 - dimension
    shortened_k = kprime - rank
    shortened_n = 1048576 + shortened_k
    shortened_m = 67472 + shortened_k
    zero_endpoint = Fraction(
        falling(shortened_n, dimension + 1),
        shortened_m * rising(67473, dimension - 1),
    )
    maximum_endpoint = Fraction(
        falling(1048576 + dimension, dimension + 1),
        rising(67473, dimension),
    )
    value = max(zero_endpoint, maximum_endpoint)
    return value.numerator // value.denominator


def kernel_capacity(kprime: int) -> int:
    nprime = 1048576 + kprime
    total = 0
    for dimension in range(1, 10):
        rank = 10 - dimension
        extra = kprime - 10
        extensions = comb(extra, dimension + 1) if extra >= dimension + 1 else 0
        total += comb(nprime, rank) * kernel_record_cap(kprime, dimension) * extensions
    return total


def kernel_multibasis_capacity(kprime: int) -> int:
    nprime = 1048576 + kprime
    total = 0
    for dimension in range(1, 10):
        rank = 10 - dimension
        extra = kprime - 10
        extensions = comb(extra, dimension + 1) if extra >= dimension + 1 else 0
        decorated = comb(nprime, rank) * kernel_record_cap(kprime, dimension) * extensions
        total += decorated // (dimension + 2)
    return total


def kernel_hybrid_terms(kprime: int) -> list[tuple[int, int, str]]:
    nprime = 1048576 + kprime
    mprime = 67472 + kprime
    extra = kprime - 10
    rows = []
    for dimension in range(1, 10):
        rank = 10 - dimension
        extensions = comb(extra, dimension + 1) if extra >= dimension + 1 else 0
        ambient = comb(nprime, rank) * kernel_record_cap(kprime, dimension) * extensions // (dimension + 2)
        per_record = comb(mprime, rank) * extensions // (dimension + 2)
        support = 274980728111260126 * per_record
        rows.append((ambient, support, "ambient" if ambient <= support else "record"))
    return rows


def kernel_hybrid_capacity(kprime: int) -> int:
    return sum(min(ambient, support) for ambient, support, _ in kernel_hybrid_terms(kprime))


def kernel_shadow_weights_caps(kprime: int) -> tuple[list[Fraction], list[Fraction], list[str]]:
    weights = []
    caps = []
    branches = []
    for dimension, (ambient, support, branch) in enumerate(kernel_hybrid_terms(kprime), 1):
        cap = Fraction(min(ambient, support), 274980728111260126)
        caps.append(cap)
        branches.append(branch)
        if not cap:
            weights.append(Fraction(0))
            continue
        weights.append(Fraction(comb(dimension + 2, 2), comb(kprime - dimension - 9, 2)))
    return weights, caps, branches


def kernel_nine_shadow_optimum(kprime: int) -> tuple[Fraction, int, list[Fraction]]:
    weights, caps, _ = kernel_shadow_weights_caps(kprime)
    remaining = Fraction(comb(67472 + kprime, 9))
    total = Fraction(0)
    frontier = 0
    allocation = []
    require([weight for weight in weights if weight] == sorted(weight for weight in weights if weight), "nine-shadow weight order")
    for dimension, (weight, cap) in enumerate(zip(weights, caps), 1):
        if not cap:
            allocation.append(Fraction(0))
            continue
        take = min(cap, remaining / weight)
        allocation.append(take)
        total += take
        remaining -= weight * take
        if take < cap and not frontier:
            frontier = dimension
    return total, frontier, allocation


def lower_shadow_maximum(budget: Fraction, weights: list[Fraction], caps: list[Fraction]) -> Fraction:
    total = Fraction(0)
    for weight, cap in zip(weights[1:], caps[1:]):
        if not cap:
            continue
        take = min(cap, max(Fraction(0), budget) / weight)
        total += take
        budget -= weight * take
    return total


def kernel_full_shadow_optimum(kprime: int) -> tuple[Fraction, list[Fraction]]:
    weights, caps, _ = kernel_shadow_weights_caps(kprime)
    shadow_budget = Fraction(comb(67472 + kprime, 9))
    support_extensions = Fraction(comb(67472 + kprime - 9, 2))
    if not caps[0]:
        return kernel_nine_shadow_optimum(kprime)[0], kernel_nine_shadow_optimum(kprime)[2]

    rank9_extensions = Fraction(comb(kprime - 10, 2))
    rank9_coefficient = 52 + 3 * support_extensions / rank9_extensions
    candidates = {Fraction(0), caps[0]}
    cumulative_weighted_cap = Fraction(0)
    cumulative_cap = Fraction(0)
    for weight, cap in zip(weights[1:], caps[1:]):
        if not cap:
            continue
        kink = (shadow_budget - cumulative_weighted_cap) / weights[0]
        if 0 <= kink <= caps[0]:
            candidates.add(kink)
        denominator = rank9_coefficient / 55 - weights[0] / weight
        numerator = (
            support_extensions * shadow_budget / 55
            - cumulative_cap
            - (shadow_budget - cumulative_weighted_cap) / weight
        )
        if denominator:
            crossing = numerator / denominator
            if 0 <= crossing <= caps[0]:
                candidates.add(crossing)
        cumulative_weighted_cap += weight * cap
        cumulative_cap += cap

    all_lower_crossing = (
        support_extensions * shadow_budget - 55 * cumulative_cap
    ) / rank9_coefficient
    if 0 <= all_lower_crossing <= caps[0]:
        candidates.add(all_lower_crossing)

    best = Fraction(-1)
    best_allocation = []
    for x1 in candidates:
        if weights[0] * x1 > shadow_budget:
            continue
        qmax = lower_shadow_maximum(shadow_budget - weights[0] * x1, weights, caps)
        cmax = (support_extensions * shadow_budget - rank9_coefficient * x1) / 55
        remaining_count = max(Fraction(0), min(qmax, cmax, sum(caps[1:], Fraction(0))))
        remaining_shadow = shadow_budget - weights[0] * x1
        allocation = [x1]
        for weight, cap in zip(weights[1:], caps[1:]):
            if not cap:
                allocation.append(Fraction(0))
                continue
            take = min(cap, remaining_count, remaining_shadow / weight)
            allocation.append(take)
            remaining_count -= take
            remaining_shadow -= weight * take
        require(remaining_count == 0, "full-shadow lower allocation")
        value = sum(allocation, Fraction(0))
        if value > best:
            best = value
            best_allocation = allocation
    require(best >= 0 and len(best_allocation) == 9, "full-shadow optimizer")
    return best, best_allocation


def kernel_rank8_shadow_data(
    kprime: int,
) -> tuple[list[Fraction], list[Fraction], list[Fraction], Fraction, Fraction]:
    weights, caps, _ = kernel_shadow_weights_caps(kprime)
    shadow_budget = Fraction(comb(67472 + kprime, 9))
    support_extensions = Fraction(comb(67472 + kprime - 9, 2))
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
    return weights, caps, coefficients, shadow_budget, support_extensions * shadow_budget


def kernel_rank8_shadow_optimum(
    kprime: int,
) -> tuple[Fraction, Fraction, Fraction, list[int], list[int], list[int]]:
    weights, caps, coefficients, shadow_budget, containment_budget = kernel_rank8_shadow_data(kprime)
    active = [index for index, cap in enumerate(caps) if cap]
    candidates = {(Fraction(0), Fraction(0))}
    for index in active:
        candidates.add((1 / weights[index], Fraction(0)))
        candidates.add((Fraction(0), 1 / coefficients[index]))
    for offset, left in enumerate(active):
        for right in active[offset + 1:]:
            determinant = weights[left] * coefficients[right] - weights[right] * coefficients[left]
            if not determinant:
                continue
            lam = (coefficients[right] - coefficients[left]) / determinant
            mu = (weights[left] - weights[right]) / determinant
            if lam >= 0 and mu >= 0:
                candidates.add((lam, mu))

    best = None
    best_data = None
    for lam, mu in sorted(candidates):
        value = lam * shadow_budget + mu * containment_budget
        tight, capped, zero = [], [], []
        for index in active:
            coverage = lam * weights[index] + mu * coefficients[index]
            if coverage == 1:
                tight.append(index + 1)
            elif coverage < 1:
                capped.append(index + 1)
                value += (1 - coverage) * caps[index]
            else:
                zero.append(index + 1)
        if best is None or value < best:
            best = value
            best_data = (lam, mu, tight, capped, zero)
    require(best is not None and best_data is not None, f"rank-eight shadow dual {kprime}")
    return best, *best_data


def kernel_rank8_shadow_patterns(end: int) -> list[list[object]]:
    output = []
    start = 10
    current = None
    for kprime in range(start, end + 1):
        _, _, _, tight, capped, zero = kernel_rank8_shadow_optimum(kprime)
        pattern = [tight, capped, zero]
        if current is None:
            current = pattern
        elif pattern != current:
            output.append([start, kprime - 1, *current])
            start, current = kprime, pattern
    require(current is not None, "rank-eight shadow pattern ledger")
    output.append([start, end, *current])
    return output


def kernel_demand_ceiling(kprime: int) -> int:
    return ceil_ratio(
        495405467 * 274980728111260126 * comb(67472 + kprime, 11),
        10**9,
    )


def kernel_demand_ratio(kprime: int) -> Fraction:
    return Fraction(495405467 * comb(67472 + kprime, 11), 10**9)


def scaled_fraction_floor(value: Fraction) -> int:
    scaled = 274980728111260126 * value
    return scaled.numerator // scaled.denominator


def rank8_weighted_demand(kprime: int) -> int:
    nprime = 1048576 + kprime
    mprime = 67472 + kprime
    return ceil_ratio(
        55 * 495405467 * 274980728111260126 * comb(mprime, 11),
        10**9 * comb(nprime, 9),
    )


def rank8_owner_pair_cap(kprime: int) -> int:
    nprime = 1048576 + kprime
    return 981105 * comb(nprime - 9, 2)


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


@cache
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
    kernel_endpoint = 4598
    kernel_wall = 4599
    kernel_endpoint_demand = kernel_demand_ceiling(kernel_endpoint)
    kernel_endpoint_capacity = kernel_capacity(kernel_endpoint)
    kernel_wall_demand = kernel_demand_ceiling(kernel_wall)
    kernel_wall_capacity = kernel_capacity(kernel_wall)
    multibasis_endpoint = 11641
    multibasis_wall = 11642
    multibasis_endpoint_demand = kernel_demand_ceiling(multibasis_endpoint)
    multibasis_endpoint_capacity = kernel_multibasis_capacity(multibasis_endpoint)
    multibasis_wall_demand = kernel_demand_ceiling(multibasis_wall)
    multibasis_wall_capacity = kernel_multibasis_capacity(multibasis_wall)
    hybrid_endpoint = 11772
    hybrid_wall = 11773
    hybrid_endpoint_demand = kernel_demand_ceiling(hybrid_endpoint)
    hybrid_endpoint_capacity = kernel_hybrid_capacity(hybrid_endpoint)
    hybrid_wall_demand = kernel_demand_ceiling(hybrid_wall)
    hybrid_wall_capacity = kernel_hybrid_capacity(hybrid_wall)
    shadow_endpoint = 15445
    shadow_wall = 15446
    shadow_endpoint_optimum, shadow_endpoint_frontier, shadow_endpoint_allocation = kernel_nine_shadow_optimum(shadow_endpoint)
    shadow_wall_optimum, shadow_wall_frontier, shadow_wall_allocation = kernel_nine_shadow_optimum(shadow_wall)
    shadow_endpoint_demand = kernel_demand_ceiling(shadow_endpoint)
    shadow_endpoint_capacity = scaled_fraction_floor(shadow_endpoint_optimum)
    shadow_wall_demand = kernel_demand_ceiling(shadow_wall)
    shadow_wall_capacity = scaled_fraction_floor(shadow_wall_optimum)
    containment_endpoint = 15670
    containment_wall = 15671
    containment_endpoint_optimum, containment_endpoint_allocation = kernel_full_shadow_optimum(containment_endpoint)
    containment_wall_optimum, containment_wall_allocation = kernel_full_shadow_optimum(containment_wall)
    containment_endpoint_demand = kernel_demand_ceiling(containment_endpoint)
    containment_endpoint_capacity = scaled_fraction_floor(containment_endpoint_optimum)
    containment_wall_demand = kernel_demand_ceiling(containment_wall)
    containment_wall_capacity = scaled_fraction_floor(containment_wall_optimum)
    rank8_shadow_endpoint = 17608
    rank8_shadow_wall = 17609
    (
        rank8_shadow_endpoint_optimum,
        rank8_shadow_endpoint_lambda,
        rank8_shadow_endpoint_mu,
        rank8_shadow_endpoint_tight,
        rank8_shadow_endpoint_capped,
        rank8_shadow_endpoint_zero,
    ) = kernel_rank8_shadow_optimum(rank8_shadow_endpoint)
    (
        rank8_shadow_wall_optimum,
        rank8_shadow_wall_lambda,
        rank8_shadow_wall_mu,
        rank8_shadow_wall_tight,
        rank8_shadow_wall_capped,
        rank8_shadow_wall_zero,
    ) = kernel_rank8_shadow_optimum(rank8_shadow_wall)
    rank8_shadow_endpoint_demand = kernel_demand_ceiling(rank8_shadow_endpoint)
    rank8_shadow_endpoint_capacity = scaled_fraction_floor(rank8_shadow_endpoint_optimum)
    rank8_shadow_wall_demand = kernel_demand_ceiling(rank8_shadow_wall)
    rank8_shadow_wall_capacity = scaled_fraction_floor(rank8_shadow_wall_optimum)
    rank8_last_open = 37995
    rank8_first_closed = 37996
    rank8_last_demand = rank8_weighted_demand(rank8_last_open)
    rank8_last_cap = rank8_owner_pair_cap(rank8_last_open)
    rank8_first_demand = rank8_weighted_demand(rank8_first_closed)
    rank8_first_cap = rank8_owner_pair_cap(rank8_first_closed)
    dense_owner_last = 22525
    dense_owner_first = 22526
    dense_owner_multiplier = 200631
    dense_owner_last_weight = rank8_weighted_demand(dense_owner_last)
    dense_owner_last_pairs = comb(1048576 + dense_owner_last - 9, 2)
    dense_owner_first_weight = rank8_weighted_demand(dense_owner_first)
    dense_owner_first_pairs = comb(1048576 + dense_owner_first - 9, 2)
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
        "kernel_canonical_basis_globalizer": {
            "correction_dimension": 10,
            "component_subset_size": 11,
            "rank_minimum": 1,
            "rank_maximum": 9,
            "extra_common_zero_offset": 10,
            "rank9_record_cap": 61871313426630599,
            "fixed_basis_capacity_formula": "M_d*C(K_prime-10,d+1)",
        },
        "kernel_rankstratified_capacity_cut": {
            "closed_K_prime_minimum": 10,
            "closed_K_prime_maximum": kernel_endpoint,
            "first_open_K_prime": kernel_wall,
            "endpoint_demand": kernel_endpoint_demand,
            "endpoint_capacity": kernel_endpoint_capacity,
            "endpoint_gap": kernel_endpoint_demand - kernel_endpoint_capacity,
            "wall_demand": kernel_wall_demand,
            "wall_capacity": kernel_wall_capacity,
            "capacity_formula": "sum_d C(n_prime,10-d)*M_d*C(K_prime-10,d+1)",
        },
        "kernel_multibasis_decoration_compression": {
            "correction_dimension": 10,
            "component_subset_size": 11,
            "global_common_zero_count": 0,
            "basis_multiplicities": list(range(3, 12)),
            "capacity_formula": "floor(C(n_prime,10-d)*M_d*C(K_prime-10,d+1)/(d+2))",
        },
        "kernel_multibasis_capacity_cut": {
            "closed_K_prime_minimum": 10,
            "closed_K_prime_maximum": multibasis_endpoint,
            "first_open_K_prime": multibasis_wall,
            "endpoint_demand": multibasis_endpoint_demand,
            "endpoint_capacity": multibasis_endpoint_capacity,
            "endpoint_gap": multibasis_endpoint_demand - multibasis_endpoint_capacity,
            "wall_demand": multibasis_wall_demand,
            "wall_capacity": multibasis_wall_capacity,
            "wall_excess": multibasis_wall_capacity - multibasis_wall_demand,
            "capacity_formula": "sum_d floor(C(n_prime,10-d)*M_d*C(K_prime-10,d+1)/(d+2))",
        },
        "kernel_record_support_capacity": {
            "correction_dimension": 10,
            "component_subset_size": 11,
            "basis_multiplicities": list(range(3, 12)),
            "capacity_formula": "floor(C(m_prime,10-d)*C(K_prime-10,d+1)/(d+2))",
        },
        "kernel_hybrid_capacity_cut": {
            "closed_K_prime_minimum": 10,
            "closed_K_prime_maximum": hybrid_endpoint,
            "first_open_K_prime": hybrid_wall,
            "endpoint_branch_pattern": ["ambient", "ambient"] + ["record"] * 7,
            "endpoint_demand": hybrid_endpoint_demand,
            "endpoint_capacity": hybrid_endpoint_capacity,
            "endpoint_gap": hybrid_endpoint_demand - hybrid_endpoint_capacity,
            "wall_demand": hybrid_wall_demand,
            "wall_capacity": hybrid_wall_capacity,
            "wall_excess": hybrid_wall_capacity - hybrid_wall_demand,
            "capacity_formula": "sum_d min(A_d,N_min*P_d)",
        },
        "kernel_nine_shadow_coupling": {
            "correction_dimension": 10,
            "component_subset_size": 11,
            "shadow_subset_size": 9,
            "spanning_shadow_coefficients": [comb(d + 2, 2) for d in range(1, 10)],
            "extension_formula": "C(K_prime-d-9,2)",
            "resource_formula": "sum_d C(d+2,2)*I_d/C(K_prime-d-9,2) <= C(m_prime,9)",
        },
        "kernel_nine_shadow_capacity_cut": {
            "closed_K_prime_minimum": 10,
            "closed_K_prime_maximum": shadow_endpoint,
            "first_open_K_prime": shadow_wall,
            "endpoint_branch_pattern": kernel_shadow_weights_caps(shadow_endpoint)[2],
            "endpoint_frontier_corank": shadow_endpoint_frontier,
            "endpoint_active_coranks": [index + 1 for index, value in enumerate(shadow_endpoint_allocation) if value],
            "wall_frontier_corank": shadow_wall_frontier,
            "wall_active_coranks": [index + 1 for index, value in enumerate(shadow_wall_allocation) if value],
            "endpoint_demand": shadow_endpoint_demand,
            "endpoint_capacity": shadow_endpoint_capacity,
            "endpoint_gap": shadow_endpoint_demand - shadow_endpoint_capacity,
            "wall_demand": shadow_wall_demand,
            "wall_capacity": shadow_wall_capacity,
            "wall_excess": shadow_wall_capacity - shadow_wall_demand,
            "capacity_formula": "fractional knapsack under the shared rank-preserving nine-shadow resource",
        },
        "kernel_nine_shadow_containment_coupling": {
            "shadows_per_eleven_subset": 55,
            "rank9_spanning_shadow_minimum": 3,
            "support_extension_formula": "C(m_prime-9,2)",
            "rank9_extension_formula": "C(K_prime-10,2)",
            "rank9_coefficient_formula": "52+3*C(m_prime-9,2)/C(K_prime-10,2)",
            "resource_formula": "rank9_coefficient*I_1+55*sum_d_ge_2 I_d <= C(m_prime-9,2)*C(m_prime,9)",
        },
        "kernel_nine_shadow_containment_capacity_cut": {
            "closed_K_prime_minimum": 10,
            "closed_K_prime_maximum": containment_endpoint,
            "first_open_K_prime": containment_wall,
            "endpoint_branch_pattern": kernel_shadow_weights_caps(containment_endpoint)[2],
            "endpoint_active_coranks": [index + 1 for index, value in enumerate(containment_endpoint_allocation) if value],
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
        },
        "kernel_rank8_nine_shadow_extension_deficit": {
            "rank8_closure_offset": 2,
            "outside_rank8_closure_minimum": 67474,
            "outside_parallel_class_partner_minimum": 67473,
            "independent_pair_floor": comb(67474, 2),
            "rank8_bad_extension_formula": "C(m_prime-9,2)-C(67474,2)",
            "rank8_resource_coefficient_formula": "55+6*C(67474,2)/C(K_prime-11,2)",
            "resource_formula": "[52+3*E0/E1]*I1+[55+6*C(67474,2)/E2]*I2+55*sum_d_ge_3 I_d <= E0*C(m_prime,9)",
        },
        "kernel_rank8_nine_shadow_capacity_cut": {
            "closed_K_prime_minimum": 10,
            "closed_K_prime_maximum": rank8_shadow_endpoint,
            "first_open_K_prime": rank8_shadow_wall,
            "endpoint_branch_pattern": kernel_shadow_weights_caps(rank8_shadow_endpoint)[2],
            "endpoint_tight_coranks": rank8_shadow_endpoint_tight,
            "endpoint_capped_coranks": rank8_shadow_endpoint_capped,
            "endpoint_zero_coranks": rank8_shadow_endpoint_zero,
            "endpoint_dual_lambda_numerator": rank8_shadow_endpoint_lambda.numerator,
            "endpoint_dual_lambda_denominator": rank8_shadow_endpoint_lambda.denominator,
            "endpoint_dual_mu_numerator": rank8_shadow_endpoint_mu.numerator,
            "endpoint_dual_mu_denominator": rank8_shadow_endpoint_mu.denominator,
            "endpoint_optimum_numerator": rank8_shadow_endpoint_optimum.numerator,
            "endpoint_optimum_denominator": rank8_shadow_endpoint_optimum.denominator,
            "endpoint_demand": rank8_shadow_endpoint_demand,
            "endpoint_capacity": rank8_shadow_endpoint_capacity,
            "endpoint_gap": rank8_shadow_endpoint_demand - rank8_shadow_endpoint_capacity,
            "wall_tight_coranks": rank8_shadow_wall_tight,
            "wall_capped_coranks": rank8_shadow_wall_capped,
            "wall_zero_coranks": rank8_shadow_wall_zero,
            "wall_dual_lambda_numerator": rank8_shadow_wall_lambda.numerator,
            "wall_dual_lambda_denominator": rank8_shadow_wall_lambda.denominator,
            "wall_dual_mu_numerator": rank8_shadow_wall_mu.numerator,
            "wall_dual_mu_denominator": rank8_shadow_wall_mu.denominator,
            "wall_optimum_numerator": rank8_shadow_wall_optimum.numerator,
            "wall_optimum_denominator": rank8_shadow_wall_optimum.denominator,
            "wall_demand": rank8_shadow_wall_demand,
            "wall_capacity": rank8_shadow_wall_capacity,
            "wall_excess": rank8_shadow_wall_capacity - rank8_shadow_wall_demand,
            "pattern_ledger": kernel_rank8_shadow_patterns(rank8_shadow_wall),
            "capacity_formula": "exact two-resource LP with rank-eight extension deficit and individual ambient/record caps",
        },
        "rank8_owner_pair_weight_cap": {
            "kernel_dimension": 2,
            "owner_flat_dimension": 4,
            "fixed_subset_size": 9,
            "fixed_owner_record_cap": 981105,
            "coordinate_pair_resource_formula": "C(n_prime-9,2)",
            "weighted_cap_formula": "981105*C(n_prime-9,2)",
        },
        "rank8_weighted_capacity_cut": {
            "last_open_K_prime": rank8_last_open,
            "last_open_demand": rank8_last_demand,
            "last_open_cap": rank8_last_cap,
            "last_open_gap": rank8_last_cap - rank8_last_demand,
            "first_closed_K_prime": rank8_first_closed,
            "first_closed_demand": rank8_first_demand,
            "first_closed_cap": rank8_first_cap,
            "first_closed_gap": rank8_first_demand - rank8_first_cap,
            "closed_K_prime_maximum": 1048576,
            "ratio_formula": "constant*C(m_prime,11)/C(n_prime,11)",
        },
        "rank8_dense_owner_terminal_bridge": {
            "last_unforced_K_prime": dense_owner_last,
            "last_unforced_deficit": dense_owner_multiplier * dense_owner_last_pairs - dense_owner_last_weight,
            "first_forced_K_prime": dense_owner_first,
            "first_forced_excess": dense_owner_first_weight - dense_owner_multiplier * dense_owner_first_pairs,
            "owner_record_floor": 200632,
            "owner_core_deficiency_ceiling": 4,
            "delta5_record_cap": 196221,
            "terminal_interval_maximum": 37995,
        },
        "claims": {
            "local_theorem_packet": True,
            "incidence_is_record_count": False,
            "cross_cell_census": False,
            "fixed_chart_output_suffices_for_payment": False,
            "full_rank_star_owner_is_record_intrinsic": True,
            "rank9_fixed_target_eliminated": True,
            "kernel_dominant_lane_closed_through_Kprime": 17608,
            "rank8_owner_flat_closed_from_Kprime": 37996,
            "rank8_dense_owner_terminal_from_Kprime": 22526,
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
    kernel_cut = value["kernel_rankstratified_capacity_cut"]
    for kprime in range(10, kernel_cut["closed_K_prime_maximum"] + 1):
        require(kernel_demand_ceiling(kprime) > kernel_capacity(kprime), f"kernel cut {kprime}")
    require(kernel_demand_ceiling(4599) <= kernel_capacity(4599), "kernel wall")
    multibasis = value["kernel_multibasis_decoration_compression"]
    require(multibasis == {
        "correction_dimension": 10,
        "component_subset_size": 11,
        "global_common_zero_count": 0,
        "basis_multiplicities": list(range(3, 12)),
        "capacity_formula": "floor(C(n_prime,10-d)*M_d*C(K_prime-10,d+1)/(d+2))",
    }, "kernel multi-basis constants")
    multibasis_cut = value["kernel_multibasis_capacity_cut"]
    for kprime in range(10, multibasis_cut["closed_K_prime_maximum"] + 1):
        require(
            kernel_demand_ceiling(kprime) > kernel_multibasis_capacity(kprime),
            f"kernel multi-basis cut {kprime}",
        )
    require(kernel_demand_ceiling(11642) < kernel_multibasis_capacity(11642), "kernel multi-basis wall")
    require(multibasis_cut["endpoint_gap"] == 17769453550459149385453824948016076737082337523706893862084, "kernel multi-basis endpoint")
    require(multibasis_cut["wall_excess"] == 187031323586740190878769118921060658362307444191332937452616, "kernel multi-basis wall excess")
    record_support = value["kernel_record_support_capacity"]
    require(record_support == {
        "correction_dimension": 10,
        "component_subset_size": 11,
        "basis_multiplicities": list(range(3, 12)),
        "capacity_formula": "floor(C(m_prime,10-d)*C(K_prime-10,d+1)/(d+2))",
    }, "kernel record-support constants")
    hybrid_cut = value["kernel_hybrid_capacity_cut"]
    for kprime in range(10, hybrid_cut["closed_K_prime_maximum"] + 1):
        require(kernel_demand_ceiling(kprime) > kernel_hybrid_capacity(kprime), f"kernel hybrid cut {kprime}")
    require([choice for _, _, choice in kernel_hybrid_terms(11772)] == ["ambient", "ambient"] + ["record"] * 7, "kernel hybrid branches")
    require(kernel_demand_ceiling(11773) < kernel_hybrid_capacity(11773), "kernel hybrid wall")
    require(hybrid_cut["endpoint_gap"] == 76504076505592948633027913576880724493595282142849410185084, "kernel hybrid endpoint")
    require(hybrid_cut["wall_excess"] == 139343682529231472322825521514042608524569163680782450618944, "kernel hybrid wall excess")
    shadow_coupling = value["kernel_nine_shadow_coupling"]
    require(shadow_coupling["spanning_shadow_coefficients"] == [3, 6, 10, 15, 21, 28, 36, 45, 55], "nine-shadow coefficients")
    shadow_cut = value["kernel_nine_shadow_capacity_cut"]
    for kprime in range(10, shadow_cut["closed_K_prime_maximum"] + 1):
        optimum, _, _ = kernel_nine_shadow_optimum(kprime)
        require(kernel_demand_ratio(kprime) > optimum, f"kernel nine-shadow cut {kprime}")
    require(kernel_demand_ratio(15446) < kernel_nine_shadow_optimum(15446)[0], "kernel nine-shadow wall")
    require(shadow_cut["endpoint_frontier_corank"] == shadow_cut["wall_frontier_corank"] == 2, "nine-shadow frontier")
    require(shadow_cut["endpoint_active_coranks"] == shadow_cut["wall_active_coranks"] == [1, 2], "nine-shadow support")
    require(shadow_cut["endpoint_gap"] == 178044655461817065880792270525721984196903835342334290540589, "nine-shadow endpoint")
    require(shadow_cut["wall_excess"] == 124087038578417364551353992932097013573495323735890481286577, "nine-shadow wall excess")
    containment = value["kernel_nine_shadow_containment_coupling"]
    require(containment["shadows_per_eleven_subset"] == comb(11, 9), "full-containment shadows")
    require(containment["rank9_spanning_shadow_minimum"] == 3, "full-containment rank-nine shadow floor")
    containment_cut = value["kernel_nine_shadow_containment_capacity_cut"]
    for kprime in range(10, containment_cut["closed_K_prime_maximum"] + 1):
        optimum, _ = kernel_full_shadow_optimum(kprime)
        require(kernel_demand_ratio(kprime) > optimum, f"kernel full-shadow cut {kprime}")
    endpoint_optimum, endpoint_allocation = kernel_full_shadow_optimum(15670)
    wall_optimum, wall_allocation = kernel_full_shadow_optimum(15671)
    require(kernel_demand_ratio(15671) < wall_optimum, "kernel full-shadow wall")
    require(endpoint_optimum == Fraction(containment_cut["endpoint_optimum_numerator"], containment_cut["endpoint_optimum_denominator"]), "full-shadow endpoint optimum")
    require(wall_optimum == Fraction(containment_cut["wall_optimum_numerator"], containment_cut["wall_optimum_denominator"]), "full-shadow wall optimum")
    require(containment_cut["endpoint_active_coranks"] == [1, 2], "full-shadow active coranks")
    require(all(value > 0 for value in endpoint_allocation[:2]) and all(value == 0 for value in endpoint_allocation[2:]), "full-shadow endpoint support")
    require(all(value > 0 for value in wall_allocation[:2]) and all(value == 0 for value in wall_allocation[2:]), "full-shadow wall support")
    require(containment_cut["endpoint_gap"] == 60244744187647715538325354175068999745872308513185869854532, "full-shadow endpoint")
    require(containment_cut["wall_excess"] == 291105561463347587484268984669020036510369238771859813045635, "full-shadow wall excess")
    rank8_deficit = value["kernel_rank8_nine_shadow_extension_deficit"]
    require(rank8_deficit["independent_pair_floor"] == comb(67474, 2) == 2276336601, "rank-eight pair floor")
    require(rank8_deficit["outside_rank8_closure_minimum"] == 67474, "rank-eight contraction outside floor")
    rank8_shadow_cut = value["kernel_rank8_nine_shadow_capacity_cut"]
    for kprime in range(10, rank8_shadow_cut["closed_K_prime_maximum"] + 1):
        optimum, _, _, _, _, _ = kernel_rank8_shadow_optimum(kprime)
        require(kernel_demand_ratio(kprime) > optimum, f"kernel rank-eight-shadow cut {kprime}")
    rank8_endpoint = kernel_rank8_shadow_optimum(17608)
    rank8_wall = kernel_rank8_shadow_optimum(17609)
    require(kernel_demand_ratio(17609) < rank8_wall[0], "kernel rank-eight-shadow wall")
    require(rank8_endpoint[3:] == ([2, 4], [1, 3], [5, 6, 7, 8, 9]), "rank-eight-shadow endpoint pattern")
    require(rank8_wall[3:] == rank8_endpoint[3:], "rank-eight-shadow wall pattern")
    require(rank8_shadow_cut["pattern_ledger"] == kernel_rank8_shadow_patterns(17609), "rank-eight-shadow pattern ledger")
    require(rank8_shadow_cut["endpoint_gap"] == 126547040539829546354916747965612889135249249684319416999204, "rank-eight-shadow endpoint")
    require(rank8_shadow_cut["wall_excess"] == 165662859003771823867021831078593815988062146919602894849014, "rank-eight-shadow wall excess")
    require(value["claims"]["kernel_dominant_lane_closed_through_Kprime"] == 17608, "kernel claim")
    rank8_cap = value["rank8_owner_pair_weight_cap"]
    require(rank8_cap == {
        "kernel_dimension": 2,
        "owner_flat_dimension": 4,
        "fixed_subset_size": 9,
        "fixed_owner_record_cap": 981105,
        "coordinate_pair_resource_formula": "C(n_prime-9,2)",
        "weighted_cap_formula": "981105*C(n_prime-9,2)",
    }, "rank-eight owner-pair cap")
    rank8_cut = value["rank8_weighted_capacity_cut"]
    require(rank8_weighted_demand(37995) <= rank8_owner_pair_cap(37995), "rank-eight last open")
    require(rank8_weighted_demand(37996) > rank8_owner_pair_cap(37996), "rank-eight first closed")
    require(rank8_cut["first_closed_gap"] == 36370688210984, "rank-eight first gap")
    require(rank8_cut["last_open_gap"] == 18174297527234, "rank-eight last gap")
    for index in range(11):
        require(
            Fraction(105469 - index, 1086573 - index)
            > Fraction(105468 - index, 1086572 - index),
            f"rank-eight monotone factor {index}",
        )
    require(value["claims"]["rank8_owner_flat_closed_from_Kprime"] == 37996, "rank-eight claim")
    dense_owner = value["rank8_dense_owner_terminal_bridge"]
    require(dense_owner == {
        "last_unforced_K_prime": 22525,
        "last_unforced_deficit": 1170919108090,
        "first_forced_K_prime": 22526,
        "first_forced_excess": 11714977255865,
        "owner_record_floor": 200632,
        "owner_core_deficiency_ceiling": 4,
        "delta5_record_cap": 196221,
        "terminal_interval_maximum": 37995,
    }, "dense-owner terminal bridge")
    require(1 + 981104 // 5 == dense_owner["delta5_record_cap"], "dense-owner deficiency cut")
    require(value["claims"]["rank8_dense_owner_terminal_from_Kprime"] == 22526, "dense-owner claim")
    return {
        **dense,
        "component_ppb": component["component_incidence_ppb_floor"],
        "cell_cap": value["rank9_split_pencil_cell"]["sharp_fixed_cell_record_cap"],
        "plane_cap": value["rank9_split_pencil_paircore"]["low_common_core_plane_cap"],
        "selector_records": value["component_ninesubset_concentrator"]["fixed_selector_record_floor"],
        "local_fence_slopes": fence["rich_slope_count"],
        "weighted_demand": weighted_elimination["boundary_demand"],
        "weighted_cap": weighted_elimination["boundary_cap"],
        "kernel_endpoint_gap": kernel_cut["endpoint_gap"],
        "kernel_wall_gap": kernel_cut["wall_capacity"] - kernel_cut["wall_demand"],
        "multibasis_endpoint_gap": multibasis_cut["endpoint_gap"],
        "multibasis_wall_excess": multibasis_cut["wall_excess"],
        "hybrid_endpoint_gap": hybrid_cut["endpoint_gap"],
        "hybrid_wall_excess": hybrid_cut["wall_excess"],
        "shadow_endpoint_gap": shadow_cut["endpoint_gap"],
        "shadow_wall_excess": shadow_cut["wall_excess"],
        "containment_endpoint_gap": containment_cut["endpoint_gap"],
        "containment_wall_excess": containment_cut["wall_excess"],
        "rank8_shadow_endpoint_gap": rank8_shadow_cut["endpoint_gap"],
        "rank8_shadow_wall_excess": rank8_shadow_cut["wall_excess"],
        "rank8_last_gap": rank8_cut["last_open_gap"],
        "rank8_first_gap": rank8_cut["first_closed_gap"],
        "dense_owner_first_excess": dense_owner["first_forced_excess"],
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
        lambda item: item["kernel_canonical_basis_globalizer"].__setitem__("extra_common_zero_offset", 9),
        lambda item: item["kernel_rankstratified_capacity_cut"].__setitem__("closed_K_prime_maximum", 4599),
        lambda item: item["kernel_multibasis_decoration_compression"]["basis_multiplicities"].__setitem__(0, 2),
        lambda item: item["kernel_multibasis_capacity_cut"].__setitem__("closed_K_prime_maximum", 11642),
        lambda item: item["kernel_multibasis_capacity_cut"].__setitem__("wall_excess", 187031323586740190878769118921060658362307444191332937452615),
        lambda item: item["kernel_record_support_capacity"]["basis_multiplicities"].__setitem__(2, 4),
        lambda item: item["kernel_hybrid_capacity_cut"]["endpoint_branch_pattern"].__setitem__(2, "ambient"),
        lambda item: item["kernel_hybrid_capacity_cut"].__setitem__("closed_K_prime_maximum", 11773),
        lambda item: item["kernel_nine_shadow_coupling"]["spanning_shadow_coefficients"].__setitem__(0, 2),
        lambda item: item["kernel_nine_shadow_capacity_cut"].__setitem__("closed_K_prime_maximum", 15446),
        lambda item: item["kernel_nine_shadow_capacity_cut"].__setitem__("wall_excess", 124087038578417364551353992932097013573495323735890481286576),
        lambda item: item["kernel_nine_shadow_containment_coupling"].__setitem__("shadows_per_eleven_subset", 54),
        lambda item: item["kernel_nine_shadow_containment_capacity_cut"].__setitem__("closed_K_prime_maximum", 15671),
        lambda item: item["kernel_nine_shadow_containment_capacity_cut"].__setitem__("endpoint_optimum_denominator", 3820255350),
        lambda item: item["kernel_rank8_nine_shadow_extension_deficit"].__setitem__("independent_pair_floor", 2276336600),
        lambda item: item["kernel_rank8_nine_shadow_capacity_cut"].__setitem__("closed_K_prime_maximum", 17609),
        lambda item: item["rank8_owner_pair_weight_cap"].__setitem__("fixed_owner_record_cap", 981104),
        lambda item: item["rank8_weighted_capacity_cut"].__setitem__("first_closed_K_prime", 37995),
        lambda item: item["rank8_dense_owner_terminal_bridge"].__setitem__("owner_record_floor", 200631),
        lambda item: item["claims"].__setitem__("rank8_dense_owner_terminal_from_Kprime", 22525),
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
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.write:
        MANIFEST.write_text(json.dumps(expected(), indent=2) + "\n")
        print(f"WROTE {MANIFEST}")
        return
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
        f"kernel_endpoint_gap={result['kernel_endpoint_gap']} "
        f"kernel_wall_gap={result['kernel_wall_gap']} "
        f"multibasis_endpoint_gap={result['multibasis_endpoint_gap']} "
        f"multibasis_wall_excess={result['multibasis_wall_excess']} "
        f"hybrid_endpoint_gap={result['hybrid_endpoint_gap']} "
        f"hybrid_wall_excess={result['hybrid_wall_excess']} "
        f"shadow_endpoint_gap={result['shadow_endpoint_gap']} "
        f"shadow_wall_excess={result['shadow_wall_excess']} "
        f"containment_endpoint_gap={result['containment_endpoint_gap']} "
        f"containment_wall_excess={result['containment_wall_excess']} "
        f"rank8_shadow_endpoint_gap={result['rank8_shadow_endpoint_gap']} "
        f"rank8_shadow_wall_excess={result['rank8_shadow_wall_excess']} "
        f"rank8_last_gap={result['rank8_last_gap']} "
        f"rank8_first_gap={result['rank8_first_gap']} "
        f"dense_owner_first_excess={result['dense_owner_first_excess']} "
        f"controls={controls} manifest_sha256={hashlib.sha256(MANIFEST.read_bytes()).hexdigest()}"
    )


if __name__ == "__main__":
    main()
