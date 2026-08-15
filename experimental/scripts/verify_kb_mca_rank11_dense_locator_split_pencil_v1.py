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
        "commit": "77960db9fdcf69e5e053a020707b2be1505b1205",
        "tree": "7044fbca17167f49a1bd890f21d1ec1d5282f74d",
        "contract_sha256": "28cfa4f50ea4ffa9a61888148c3916b0638906117d6efdbd2a779d8f4a925d94",
    },
    "rank9_residual_petal_capacity_cut": {
        "id": "rate_half_mca_rank11_rank9_residual_petal_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_rank9_residual_petal_capacity_cut",
        "commit": "6a5ffb3d8b55f52e5bf0b1ba43bda2fb8e8f5fd1",
        "tree": "c5a753ba2494a92eb0349584ba83a74ffeb95691",
        "contract_sha256": "2980ce37664731e481b65d74ea39f4635ef8e9cba09bd8c22d48cc1493d1a1a8",
    },
    "rank9_exact_petal_partition_capacity_cut": {
        "id": "rate_half_mca_rank11_rank9_exact_petal_partition_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_rank9_exact_petal_partition_capacity_cut",
        "commit": "1dac113d38255e1e2f1247a7c7e9ca7d730be47f",
        "tree": "f0cf373ed6c780a401ad248bd9232322c6b22415",
        "contract_sha256": "df54f15d0ba1f4e335eb606f8f47c496e240ac7e2fe3beb209e100a3a4a7dd39",
    },
    "weighted_split_pencil_selected_support_cap": {
        "id": "rate_half_mca_weighted_split_pencil_selected_support_cap",
        "path": "background/nodes/rate_half_mca_weighted_split_pencil_selected_support_cap",
        "commit": "84d93e9f034008a8057702a4dfb85541ac5b5e06",
        "tree": "f588d0b5b13a30c6aa6df6c292695024aec7e96b",
        "contract_sha256": "414e1f902ec6a53abdb7ea789061c6147af9953c841440b963d71d6dfb7be434",
    },
    "rank9_minimal_shortening_split_pencil_payment": {
        "id": "rate_half_mca_rank11_rank9_minimal_shortening_split_pencil_payment",
        "path": "background/nodes/rate_half_mca_rank11_rank9_minimal_shortening_split_pencil_payment",
        "commit": "84d93e9f034008a8057702a4dfb85541ac5b5e06",
        "tree": "aea5f2935d3d8b26c583342f95ea3ce970f5f7de",
        "contract_sha256": "029b609ad2401fa9c9e689bdff2496fff2b202f2d00acb6010b64eac67acf881",
    },
    "weighted_split_pencil_core_offset_cap": {
        "id": "rate_half_mca_weighted_split_pencil_core_offset_cap",
        "path": "background/nodes/rate_half_mca_weighted_split_pencil_core_offset_cap",
        "commit": "635d38a2b8bccb113065c0007da31360b6c68769",
        "tree": "e6c43c22b639c42e216929b437ad61d46b4e43b1",
        "contract_sha256": "c16ddeb5b7e492a6ababe1f558ba7f7b049ac4f1116149191d7065dbed163159",
    },
    "rank11_k11_circuit_split_pencil_payment": {
        "id": "rate_half_mca_rank11_k11_circuit_split_pencil_payment",
        "path": "background/nodes/rate_half_mca_rank11_k11_circuit_split_pencil_payment",
        "commit": "635d38a2b8bccb113065c0007da31360b6c68769",
        "tree": "aca673faaa3ed10ab4ae758789de84688af83548",
        "contract_sha256": "72c6d95b858551bceea1467d6832b9a0e1daf73edac9c9ae54dc9af3e11b692a",
    },
    "codimension_two_quotient_line_sparse_circuit_cap": {
        "id": "rate_half_mca_codimension_two_quotient_line_sparse_circuit_cap",
        "path": "background/nodes/rate_half_mca_codimension_two_quotient_line_sparse_circuit_cap",
        "commit": "212a708b28a846e3aa3b1ba1aa7a676ecc84ab52",
        "tree": "c4ca702ca288d6e84efcae9569e182713908afe6",
        "contract_sha256": "2007208c46a197c7d526ea185b9fe9034c860279f02c6d7d815cc0816eb90c82",
    },
    "rank11_k12_quotient_line_circuit_payment": {
        "id": "rate_half_mca_rank11_k12_quotient_line_circuit_payment",
        "path": "background/nodes/rate_half_mca_rank11_k12_quotient_line_circuit_payment",
        "commit": "212a708b28a846e3aa3b1ba1aa7a676ecc84ab52",
        "tree": "f5e9556ee7c6bab9a79885a9feab541f50bb7f67",
        "contract_sha256": "8189f852eb61e3df83bec0d7158a71a8d0b5f6bbe8d38b2b60521ae875956d3c",
    },
    "codimension_three_sparse_circuit_completion_cap": {
        "id": "rate_half_mca_codimension_three_sparse_circuit_completion_cap",
        "path": "background/nodes/rate_half_mca_codimension_three_sparse_circuit_completion_cap",
        "commit": "8fa0f03b24795b6bf81da0973f7bbb42cb833e43",
        "tree": "39deb2b2d24bde9b553f43a985cf75d26f6c937f",
        "contract_sha256": "87d1bd00338c62a01640e593eec40d0cec20c8e8cbde2c138b482958a458c7e5",
    },
    "rank11_k13_sparse_circuit_completion_payment": {
        "id": "rate_half_mca_rank11_k13_sparse_circuit_completion_payment",
        "path": "background/nodes/rate_half_mca_rank11_k13_sparse_circuit_completion_payment",
        "commit": "8fa0f03b24795b6bf81da0973f7bbb42cb833e43",
        "tree": "5e0b2f59feeead4f69ae1365950555d8f30228c3",
        "contract_sha256": "12473a9dbffe68438eb813e042d666c9ab08b25ac48bc8cdc0c5dcc2d3b4b30b",
    },
    "sparse_circuit_completion_dimension_ladder": {
        "id": "rate_half_mca_sparse_circuit_completion_dimension_ladder",
        "path": "background/nodes/rate_half_mca_sparse_circuit_completion_dimension_ladder",
        "commit": "e9a8a76800cd05dbe8382a3ac253d83a52d71d2c",
        "tree": "32f790041de21037bdb2dad648a7e20a7be782e3",
        "contract_sha256": "25bbeb3c2124f34399659550c214400bc6afe4ce9d5ee615939241e2e94c298b",
    },
    "rank9_sparse_shadow_joint_ledger": {
        "id": "rate_half_mca_rank9_sparse_shadow_joint_ledger",
        "path": "background/nodes/rate_half_mca_rank9_sparse_shadow_joint_ledger",
        "commit": "e9a8a76800cd05dbe8382a3ac253d83a52d71d2c",
        "tree": "b0c09e54fcdaaf64bffd8f1dfadcea410b205a15",
        "contract_sha256": "2f9446f4efd0a3cbb393a74f78f77384dee26f2f3d5fdddb53ba1b4b71762013",
    },
    "rank11_k14_k21_sparse_shadow_payment": {
        "id": "rate_half_mca_rank11_k14_k21_sparse_shadow_payment",
        "path": "background/nodes/rate_half_mca_rank11_k14_k21_sparse_shadow_payment",
        "commit": "e9a8a76800cd05dbe8382a3ac253d83a52d71d2c",
        "tree": "8d83ef5e484e76301b88e39f8c28998fb5d37edf",
        "contract_sha256": "eb1c5343d7aee27704ff1c9a5a30639e3cb101c51e7b13eb0a3f04be071f56e1",
    },
    "weighted_split_pencil_integral_heavy_cap": {
        "id": "rate_half_mca_weighted_split_pencil_integral_heavy_cap",
        "path": "background/nodes/rate_half_mca_weighted_split_pencil_integral_heavy_cap",
        "commit": "16bb0595c464c32746961dabe808d0d0f73ad1c6",
        "tree": "4c3cd3970e804a29b1b0f965c63e4c9f8b65b86d",
        "contract_sha256": "e701eafd9f64560bbbe67023ff62009028e8ae11e0426f8becb88976cb26878f",
    },
    "sparse_circuit_near_saturation_carrier": {
        "id": "rate_half_mca_sparse_circuit_near_saturation_carrier",
        "path": "background/nodes/rate_half_mca_sparse_circuit_near_saturation_carrier",
        "commit": "16bb0595c464c32746961dabe808d0d0f73ad1c6",
        "tree": "145d35b36773a87cac7d0c63220de9fa2826bfd5",
        "contract_sha256": "03da7712fdd01435cb12f7d0c2afc96d3fadd39f9270152980cc44c79075f38b",
    },
    "rank11_k22_integral_near_saturation_payment": {
        "id": "rate_half_mca_rank11_k22_integral_near_saturation_payment",
        "path": "background/nodes/rate_half_mca_rank11_k22_integral_near_saturation_payment",
        "commit": "16bb0595c464c32746961dabe808d0d0f73ad1c6",
        "tree": "7b41e28bbd24f6a16e8deec623cb0efb4e287858",
        "contract_sha256": "4d2031a5d96149bc5cf2d1c20e9b997200f3baf4a98c14b87ab5e7836435f77d",
    },
    "sparse_circuit_completion_defect_hierarchy": {
        "id": "rate_half_mca_sparse_circuit_completion_defect_hierarchy",
        "path": "background/nodes/rate_half_mca_sparse_circuit_completion_defect_hierarchy",
        "commit": "523e124ca703d5a9797f175c862a8f5e72535662",
        "tree": "7dadedbe3e8104bbf93814d614a60eb3f48aff20",
        "contract_sha256": "c09209dd879b2845e237915ebc9282fb8218e452833b5d810cf52b6813a0b4fa",
    },
    "rank11_k23_completion_defect_payment": {
        "id": "rate_half_mca_rank11_k23_completion_defect_payment",
        "path": "background/nodes/rate_half_mca_rank11_k23_completion_defect_payment",
        "commit": "523e124ca703d5a9797f175c862a8f5e72535662",
        "tree": "5392ceb7c22d2fd22dcd9405a5ffba88da94bb72",
        "contract_sha256": "37a1bca5a03ec0b007a4ac9901e5e04ecaa40f3d4592a5ef1f080efaa6b1293b",
    },
    "sparse_circuit_universal_completion_incidence_cap": {
        "id": "rate_half_mca_sparse_circuit_universal_completion_incidence_cap",
        "path": "background/nodes/rate_half_mca_sparse_circuit_universal_completion_incidence_cap",
        "commit": "ffb120ecd3200489fd6e6464ce0e916dad04596a",
        "tree": "0f8c84cd5172ecbd88c2884b9cb5e43dbf4260d7",
        "contract_sha256": "0f60be130825abd28548760bada38246758588fbf19da9c627e168bda5894d2b",
    },
    "rank9_full_circuit_deficit_ledger": {
        "id": "rate_half_mca_rank9_full_circuit_deficit_ledger",
        "path": "background/nodes/rate_half_mca_rank9_full_circuit_deficit_ledger",
        "commit": "ffb120ecd3200489fd6e6464ce0e916dad04596a",
        "tree": "4db4915a49176787967486d1b6b02989414a019c",
        "contract_sha256": "2a03a7595972ebd3708a681012fbd78799ea7132326d149d41d6534adfc1c69c",
    },
    "rank11_k24_k40_full_deficit_shadow_payment": {
        "id": "rate_half_mca_rank11_k24_k40_full_deficit_shadow_payment",
        "path": "background/nodes/rate_half_mca_rank11_k24_k40_full_deficit_shadow_payment",
        "commit": "ffb120ecd3200489fd6e6464ce0e916dad04596a",
        "tree": "aaeafc666b5880de825572df4dc527aba32a7d97",
        "contract_sha256": "29303e23b2286b8c6dbd5d496d5ec9dc779f929bf880d20c5c1eb86268e9782a",
    },
    "rank_stratified_isolated_incidence_cap": {
        "id": "rate_half_mca_rank11_rank_stratified_isolated_incidence_cap",
        "path": "background/nodes/rate_half_mca_rank11_rank_stratified_isolated_incidence_cap",
        "commit": "ad44a0555d5f085cc90e7c96b28248d9e244f647",
        "tree": "e9d6ce6768c7e61fc98c85394e50a8a725ece9b9",
        "contract_sha256": "25def3f3f47dedd1d7aeb704c24dd28c00b507fda019bd72e9240ed6bcbd123c",
    },
    "rank11_k41_sharp_isolated_payment": {
        "id": "rate_half_mca_rank11_k41_sharp_isolated_payment",
        "path": "background/nodes/rate_half_mca_rank11_k41_sharp_isolated_payment",
        "commit": "ad44a0555d5f085cc90e7c96b28248d9e244f647",
        "tree": "9dbe7abfaa4dd656219239a9f4f2b2f661208598",
        "contract_sha256": "0b926a50e1d5ab12e56bdb1db2cdd143e7de60bf371862501d3853beb86ded69",
    },
    "sparse_circuit_cross_support_defect_carrier": {
        "id": "rate_half_mca_sparse_circuit_cross_support_defect_carrier",
        "path": "background/nodes/rate_half_mca_sparse_circuit_cross_support_defect_carrier",
        "commit": "291986739177a8511ba46d969e93056d8cc321a3",
        "tree": "d8c561802115fc65ad056a926c2d1295335915f3",
        "contract_sha256": "f51f62b2198f3477091f4966b76473aa21f49607535b189b75e87c28ecf2ab9c",
    },
    "rank11_k42_cross_support_defect_payment": {
        "id": "rate_half_mca_rank11_k42_cross_support_defect_payment",
        "path": "background/nodes/rate_half_mca_rank11_k42_cross_support_defect_payment",
        "commit": "291986739177a8511ba46d969e93056d8cc321a3",
        "tree": "301831b4776e41e2f0940c7c29c64bfca3803d5d",
        "contract_sha256": "db90a48687728e7e6490e5ee976b54b3eda5b35b7184be7fc4a98e82c3a635b8",
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
    "kernel_corank1_projective_pair_cap": {
        "id": "rate_half_mca_rank11_kernel_corank1_projective_pair_cap",
        "path": "background/nodes/rate_half_mca_rank11_kernel_corank1_projective_pair_cap",
        "commit": "ce200a0cd7e6db25623bac54121b8ab219fe8e79",
        "tree": "0df97220f4e335c305eae2c962d2add70f6d5f42",
        "contract_sha256": "274e46e67449c810193279941492511ddd67acff87649f5756b2b330718d9015",
    },
    "kernel_projective_pair_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_projective_pair_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_projective_pair_capacity_cut",
        "commit": "10ff16378eb487137819dbb2b48df8e2b50c3309",
        "tree": "458a335697935cd2b36aa07bc71411fc1cfa27e3",
        "contract_sha256": "05df2ec3f8cb69275a1aa0b4d0295ad82621e9ad6792dd2a70edf27cf6684156",
    },
    "kernel_corank2_projective_basis_cap": {
        "id": "rate_half_mca_rank11_kernel_corank2_projective_basis_cap",
        "path": "background/nodes/rate_half_mca_rank11_kernel_corank2_projective_basis_cap",
        "commit": "75a424e9656fc44f1de88f40eca97667802e9be1",
        "tree": "2cccdc7854b55e3f5b2627ca5ee2bf4cb58640cc",
        "contract_sha256": "e1a679080c4efd83af40aa7d969960946b3ca3d7654e46e65be8dcb68a910d6c",
    },
    "matroid_rank3_bounded_parallel_basis_floor": {
        "id": "matroid_rank3_bounded_parallel_basis_floor",
        "path": "background/nodes/matroid_rank3_bounded_parallel_basis_floor",
        "commit": "543be2bd2eac138a525893d6396fc25c4b839b79",
        "tree": "3e7f309a80191b0456d6035e6e3cb6e0964e05c3",
        "contract_sha256": "a765b84a8cff00ae03d2cc33a6ad9be904200612d1628f94f5700cd94e5500fb",
    },
    "kernel_corank2_uniform_projective_basis_cap": {
        "id": "rate_half_mca_rank11_kernel_corank2_uniform_projective_basis_cap",
        "path": "background/nodes/rate_half_mca_rank11_kernel_corank2_uniform_projective_basis_cap",
        "commit": "543be2bd2eac138a525893d6396fc25c4b839b79",
        "tree": "b262c8b126cd317930cfa6a385fc9c82b9344547",
        "contract_sha256": "0eefc50e8452fb30d8dba4cf94ecfc639ae618dba34a1662ef9decf7de4f2cfd",
    },
    "kernel_corank2_projective_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_corank2_projective_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_corank2_projective_capacity_cut",
        "commit": "543be2bd2eac138a525893d6396fc25c4b839b79",
        "tree": "a88331ca72593d46d4c539693e8b9bdddc588dae",
        "contract_sha256": "3136181b886366f3b19a6c2ffeb97dff2d924a34d47855b9897117df52951aa9",
    },
    "kernel_corank3_projective_basis_cap": {
        "id": "rate_half_mca_rank11_kernel_corank3_projective_basis_cap",
        "path": "background/nodes/rate_half_mca_rank11_kernel_corank3_projective_basis_cap",
        "commit": "005d58f92a743043644926e2daeed5b6f58873a6",
        "tree": "214797e76ee997373f9e6d769dc106dfa28c859f",
        "contract_sha256": "1df3954f0b52dc475f5212be64af83530645e3b1b035b2178185f422671e6b8a",
    },
    "matroid_rank4_bounded_point_line_basis_floor": {
        "id": "matroid_rank4_bounded_point_line_basis_floor",
        "path": "background/nodes/matroid_rank4_bounded_point_line_basis_floor",
        "commit": "a75333b21538bf9b2b90c3332f32e093659867b8",
        "tree": "8c347327c17423e1cc73ce756b299bf685d84234",
        "contract_sha256": "1e81b6891afdd1d54f65891b2f29128bb3fd47ff53526fa83e769446bc041f97",
    },
    "kernel_corank3_uniform_projective_basis_cap": {
        "id": "rate_half_mca_rank11_kernel_corank3_uniform_projective_basis_cap",
        "path": "background/nodes/rate_half_mca_rank11_kernel_corank3_uniform_projective_basis_cap",
        "commit": "a75333b21538bf9b2b90c3332f32e093659867b8",
        "tree": "5d52e54f0eb4d557304b2d1c3be6c9f5a39cf9fa",
        "contract_sha256": "598eb55c00ce2778fa57b185360f80208b5ae34b418a001bd5293b55d6669a7d",
    },
    "kernel_corank3_projective_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_corank3_projective_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_corank3_projective_capacity_cut",
        "commit": "a75333b21538bf9b2b90c3332f32e093659867b8",
        "tree": "d9dbd0b8eb8edec4138d2a84b5ece248e6faa424",
        "contract_sha256": "ed03c341d0cbcc9b70648c4563dd9d9ccfdc505a801bd4a795becce560560e59",
    },
    "matroid_paving_basis_floor": {
        "id": "matroid_paving_basis_floor",
        "path": "background/nodes/matroid_paving_basis_floor",
        "commit": "10ff16378eb487137819dbb2b48df8e2b50c3309",
        "tree": "a47a3474eb9bfa677ecc5efc56b9c472382edfaf",
        "contract_sha256": "e9090a0719eaabde0fe291fb61237841aae14b51765f5c482ba110632304e648",
    },
    "kernel_projective_paving_record_caps": {
        "id": "rate_half_mca_rank11_kernel_projective_paving_record_caps",
        "path": "background/nodes/rate_half_mca_rank11_kernel_projective_paving_record_caps",
        "commit": "10ff16378eb487137819dbb2b48df8e2b50c3309",
        "tree": "27e99b1f3417c5e872b7cf0b27778e09497a488c",
        "contract_sha256": "2aa863ef930e21cd06b8268dbe12a64571ffbf4ecca42888e77453a9b70d23ea",
    },
    "kernel_projective_paving_integer_gap_fence": {
        "id": "rate_half_mca_rank11_kernel_projective_paving_integer_gap_fence",
        "path": "background/nodes/rate_half_mca_rank11_kernel_projective_paving_integer_gap_fence",
        "commit": "543be2bd2eac138a525893d6396fc25c4b839b79",
        "tree": "a45a48306ea298efbcec8d4d71f8e468aa05104b",
        "contract_sha256": "f62c32a69299fa026812eebb2490dbf74ffe00676e3a0e32d314fcd0f89d310c",
    },
    "kernel_shortening_weighted_extension_cap": {
        "id": "rate_half_mca_rank11_kernel_shortening_weighted_extension_cap",
        "path": "background/nodes/rate_half_mca_rank11_kernel_shortening_weighted_extension_cap",
        "commit": "47a9ef9f064f30ad998db559eb1e198f2d9ea8c9",
        "tree": "750a3fafcb3ca2f9e7e754792a6bbb1b2668ee8b",
        "contract_sha256": "7e8c30e32fed0c67ff8d4526f89e8a6314d3548ee1e8af4b032b831832918ce0",
    },
    "kernel_shortening_weighted_capacity_cut": {
        "id": "rate_half_mca_rank11_kernel_shortening_weighted_capacity_cut",
        "path": "background/nodes/rate_half_mca_rank11_kernel_shortening_weighted_capacity_cut",
        "commit": "47a9ef9f064f30ad998db559eb1e198f2d9ea8c9",
        "tree": "7137541f08951af4c7af4173c507370a0f3be1bb",
        "contract_sha256": "346275c29a091b24c528cbdf0f880e9585261f636c92ae041ceda9aefb5a9281",
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
    "rank8_fixed_chart_local_cap_fence": {
        "id": "rate_half_mca_rank11_rank8_fixed_chart_local_cap_fence",
        "path": "background/nodes/rate_half_mca_rank11_rank8_fixed_chart_local_cap_fence",
        "commit": "90f7509bb2b706cc5daf90003efc45dd23a82c75",
        "tree": "cdaab7eb0a655760057433a9d22f76f6e0963bc3",
        "contract_sha256": "553bbf5c9ba10d97f220480d50aea1dd7017407ddd833459f513992b97667093",
    },
    "rank8_minimal_shortening_exclusion": {
        "id": "rate_half_mca_rank11_rank8_minimal_shortening_exclusion",
        "path": "background/nodes/rate_half_mca_rank11_rank8_minimal_shortening_exclusion",
        "commit": "d7d09fd437080a63d4571ce84abb6220698528a1",
        "tree": "cfeeaeda449d3527d14218bb2519ab25e3803518",
        "contract_sha256": "d03271ea09234ab73dad72b6509a136b07427a479bba822c7db55adf8c4c868e",
    },
    "rank8_codimension_one_circuit_shadow_census": {
        "id": "rate_half_mca_rank11_rank8_codimension_one_circuit_shadow_census",
        "path": "background/nodes/rate_half_mca_rank11_rank8_codimension_one_circuit_shadow_census",
        "commit": "ebdeb497f575cb7cf2a22565200c748e794cf02b",
        "tree": "24448f28d742304c6e437256c0c7311601de81f5",
        "contract_sha256": "c6e5d380725fb05eee4fe901c8884eaae9806545c70024ef1a58af18e56e3e7f",
    },
}


class Reject(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Reject(message)


def ceil_ratio(numerator: int, denominator: int) -> int:
    return (numerator + denominator - 1) // denominator


def quotient_line_label_cap(support_size: int, record_support_size: int) -> int:
    if support_size == 1:
        return 2
    candidates = [support_size + 1]
    for degree in range(1, support_size + 1):
        for fixed_roots in range(support_size):
            candidates.append(
                support_size
                + degree * (record_support_size - fixed_roots)
                // (support_size - fixed_roots)
            )
    return max(candidates)


def falling(value: int, length: int) -> int:
    return prod(range(value - length + 1, value + 1))


def rising(value: int, length: int) -> int:
    return prod(range(value, value + length))


SHORTENING_WEIGHTED_COMPLETE_CAPS = [
    8147918,
    84416263,
    983902549,
    12232092309,
    158406193634,
    2109949210211,
    28689347099870,
    396280526311830,
    5542092977392141,
]
SHORTENING_WEIGHTED_F1 = {
    4: Fraction(39454364588033681799449404, 645140654628855),
    5: Fraction(5171392066056191766078781868141, 5441519492853793965),
    6: Fraction(10845267613602799461300374655281788406, 734365704516293844907605),
    7: Fraction(236920293652959955631837334531958308623273, 1032380486753585722033044225),
    8: Fraction(397489705792142424121936242288309604876375549928, 111464056369332649181844021859713),
    9: Fraction(2075542489830289697734864933850536886198804539463, 37455710631658593932397487767705),
}


def shortening_weighted_f_value(dimension: int, t_value: int) -> Fraction:
    return Fraction(
        falling(1048576 + dimension + t_value, dimension + 1),
        (67472 + dimension + t_value) * rising(67473, dimension - 1),
    )


def shortening_weighted_ratio(kprime: int, dimension: int, t_value: int) -> Fraction:
    extension_degree = dimension + 1
    s_value = kprime - 10
    return Fraction(
        (1048576 + dimension + t_value + 1)
        * (67472 + dimension + t_value)
        * (s_value - t_value - extension_degree),
        (1048576 + t_value)
        * (67472 + dimension + t_value + 1)
        * (s_value - t_value),
    )


def shortening_weighted_gap(kprime: int) -> Fraction:
    s_value = kprime - 10
    capacity = Fraction(0)
    for dimension in range(1, 10):
        weighted = (
            Fraction(SHORTENING_WEIGHTED_COMPLETE_CAPS[dimension - 1] * comb(s_value, dimension + 1))
            if dimension <= 3
            else SHORTENING_WEIGHTED_F1[dimension] * comb(s_value - 1, dimension + 1)
        )
        capacity += Fraction(comb(1048576 + kprime, 10 - dimension), dimension + 2) * weighted
    demand = Fraction(
        274980728111260126 * 495405467 * comb(67472 + kprime, 11),
        10**9,
    )
    return demand - capacity


def shortening_weighted_newton_coefficients(start: int = 796599) -> list[Fraction]:
    values = [shortening_weighted_gap(start + offset) for offset in range(12)]
    coefficients = []
    while values:
        coefficients.append(values[0])
        values = [values[index + 1] - values[index] for index in range(len(values) - 1)]
    return coefficients


def fraction_vector_digest(values: list[Fraction]) -> str:
    payload = json.dumps(
        [[value.numerator, value.denominator] for value in values],
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def rank4_sum_integers(lo: int, hi: int) -> int:
    return 0 if lo > hi else (lo + hi) * (hi - lo + 1) // 2


def rank4_square_prefix(value: int) -> int:
    return value * (value + 1) * (2 * value + 1) // 6


def rank4_sum_squares(lo: int, hi: int) -> int:
    return 0 if lo > hi else rank4_square_prefix(hi) - rank4_square_prefix(lo - 1)


def rank4_progression_sums(lo: int, hi: int, residue: int) -> tuple[int, int, int]:
    first = lo + ((residue - lo) % 4)
    if first > hi:
        return 0, 0, 0
    count = (hi - first) // 4 + 1
    last = first + 4 * (count - 1)
    index_sum = count * (count - 1) // 2
    index_square_sum = count * (count - 1) * (2 * count - 1) // 6
    return (
        count,
        count * (first + last) // 2,
        count * first * first + 8 * first * index_sum + 16 * index_square_sum,
    )


def rank4_sum_h_weight(a: int, lo: int, hi: int) -> int:
    if lo > hi:
        return 0
    half = (a + 1) // 2
    constant_start = 4 * half - a
    floor_end = min(hi, constant_start - 1)
    total = 0
    if lo <= floor_end:
        numerator = 0
        for residue in range(4):
            count, value_sum, square_sum = rank4_progression_sums(lo, floor_end, residue)
            remainder = (a + residue) % 4
            shifted_a = a - remainder
            numerator += square_sum + (shifted_a - 2) * value_sum - 2 * shifted_a * count
        require(numerator % 4 == 0, "rank-four residue divisibility")
        total += numerator // 4
    constant_lo = max(lo, constant_start)
    if constant_lo <= hi:
        count = hi - constant_lo + 1
        total += half * (rank4_sum_integers(constant_lo, hi) - 2 * count)
    return total


def rank4_sum_increment6(a: int, lo: int, hi: int) -> int:
    if lo > hi:
        return 0
    count = hi - lo + 1
    value_sum = rank4_sum_integers(lo, hi)
    unfloored = (
        (a - 1) * (value_sum - 2 * count)
        + rank4_sum_squares(lo, hi)
        - 2 * value_sum
    )
    return 3 * (unfloored - rank4_sum_h_weight(a, lo, hi))


def rank4_h(a: int, rank_gap: int) -> int:
    return min((a + 1) // 2, (a + rank_gap) // 4)


def rank4_coloop6(a: int, rank_gap: int) -> int:
    return (a + rank_gap - 1) * (rank_gap - 1) * (rank_gap - 2)


def rank4_increment6(a: int, rank_gap: int) -> int:
    return 3 * (a + rank_gap - rank4_h(a, rank_gap) - 1) * (rank_gap - 2)


def rank4_basis_floor6(a: int, rank_gap: int = 67474) -> int:
    base = 6 + rank4_sum_increment6(a, 4, rank_gap)
    half = (a + 1) // 2
    threshold = (a + 4) // 3
    if threshold > half:
        reset = rank_gap
    else:
        first_nondecreasing = max(5, 4 * threshold - a)
        reset = rank_gap if first_nondecreasing > rank_gap else first_nondecreasing - 1
    reset_value = rank4_coloop6(a, reset) + rank4_sum_increment6(a, reset + 1, rank_gap)
    return min(base, reset_value)


def uniform_corank3_row(t_value: int) -> dict[str, int]:
    floor6 = rank4_basis_floor6(t_value + 1)
    resource = falling(1048579 + t_value, 4)
    ordered = 4 * floor6
    cap, remainder = divmod(resource, ordered)
    return {
        "t": t_value,
        "basis_floor_times_6": floor6,
        "ordered_basis_floor": ordered,
        "record_cap": cap,
        "division_remainder": remainder,
        "next_integer_gap": 983902550 * ordered - resource,
    }


def scan_uniform_corank3() -> tuple[int, int, int]:
    maximum = (-1, 0)
    first_excess = -1
    for t_value in range(1048567):
        current = uniform_corank3_row(t_value)
        require(current["next_integer_gap"] > 0, "uniform corank-three next-integer gap")
        maximum = max(maximum, (current["record_cap"], -t_value))
        if current["record_cap"] > 983902549 and first_excess < 0:
            first_excess = t_value
    return maximum[0], -maximum[1], first_excess


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


def joint_core_offset_capacity(petal_mass: int, total: int, offset: int) -> int:
    heavy = total // (petal_mass // 2 + 1)
    cross_floor = petal_mass * petal_mass // 4
    balanced = comb(total, 2) * (cross_floor + offset * petal_mass) // cross_floor
    collision = comb(heavy, 2) * (comb(petal_mass - 1, 2) + offset * petal_mass)
    vertex_num = (petal_mass - 2) * total + 2 * heavy * offset * petal_mass
    vertex_den = 2 * (petal_mass - 2)
    center = vertex_num // vertex_den
    clean = max(
        light
        * (
            (petal_mass - 2) * (total - light)
            + 2 * heavy * offset * petal_mass
        )
        // 2
        for light in range(max(0, center - 3), min(total, center + 3) + 1)
    )
    return clean + balanced + collision


def completion_ladder_value(mprime: int, support: int, completions: int) -> int:
    return completions * comb(
        mprime - support + 1 - completions,
        11 - support,
    )


@cache
def integral_clean_cap(petal_mass: int, total: int, offset: int) -> dict[str, int]:
    """Exact integer heavy-owner optimization, including residual weights."""
    minimum_weight = petal_mass // 2 + 1
    maximum_weight = petal_mass - 1
    width = maximum_weight - minimum_weight
    charge = comb(petal_mass, 2) + offset * petal_mass

    def phi(weight: int) -> Fraction:
        return Fraction(charge, petal_mass - weight) - weight

    def value(light: int, count: int, full: int) -> Fraction:
        if full == count:
            return light * count * phi(maximum_weight)
        minimum = count - full - 1
        residual = (
            total
            - light
            - full * maximum_weight
            - minimum * minimum_weight
        )
        require(minimum_weight <= residual <= maximum_weight, "residual weight")
        return light * (
            full * phi(maximum_weight)
            + minimum * phi(minimum_weight)
            + phi(residual)
        )

    def derivative(light: int, count: int, full: int) -> Fraction:
        minimum = count - full - 1
        delta = (
            petal_mass
            - total
            + full * maximum_weight
            + minimum * minimum_weight
        )
        constant = full * phi(maximum_weight) + minimum * phi(minimum_weight)
        linear = constant + delta - petal_mass
        denominator = light + delta
        return 2 * light + linear + Fraction(
            charge * delta,
            denominator * denominator,
        )

    candidates: list[tuple[Fraction, int, int, int]] = []
    segment_count = 0
    for count in range(1, total // minimum_weight + 1):
        if total - count * maximum_weight >= 0:
            high = total - count * maximum_weight
            candidates.append((value(0, count, count), 0, count, count))
            candidates.append((value(high, count, count), high, count, count))
            segment_count += 1

        for full in range(count):
            low = max(
                0,
                total - count * minimum_weight - (full + 1) * width + 1,
            )
            high = min(
                total - count * minimum_weight,
                total - count * minimum_weight - full * width,
            )
            if low > high:
                continue
            segment_count += 1
            points = {low, high}
            minimum = count - full - 1
            delta = (
                petal_mass
                - total
                + full * maximum_weight
                + minimum * minimum_weight
            )

            if delta > 0:
                if (low + delta) ** 3 >= charge * delta:
                    split = low
                elif (high + delta) ** 3 < charge * delta:
                    split = high + 1
                else:
                    left, right = low, high
                    while left < right:
                        middle = (left + right) // 2
                        if (middle + delta) ** 3 >= charge * delta:
                            right = middle
                        else:
                            left = middle + 1
                    split = left

                concave_high = min(high, split - 1)
                if low <= concave_high:
                    low_derivative = derivative(low, count, full)
                    high_derivative = derivative(concave_high, count, full)
                    if low_derivative > 0 and high_derivative < 0:
                        left, right = low, concave_high
                        while left < right:
                            middle = (left + right) // 2
                            if derivative(middle, count, full) <= 0:
                                right = middle
                            else:
                                left = middle + 1
                        points.update(
                            range(max(low, left - 2), min(high, left + 2) + 1)
                        )
                points.update(
                    range(max(low, split - 2), min(high, split + 2) + 1)
                )

            for light in points:
                candidates.append((value(light, count, full), light, count, full))

    best, light, count, full = max(candidates)
    return {
        "cap": best.numerator // best.denominator,
        "light": light,
        "count": count,
        "full": full,
        "segments": segment_count,
        "candidates": len(candidates),
    }


@cache
def integral_core_offset_row(kprime: int, core: int) -> dict[str, int]:
    nprime = 1048576 + kprime
    mprime = 67472 + kprime
    petal_mass = mprime - core
    total = nprime - core
    offset = core - 9
    clean = integral_clean_cap(petal_mass, total, offset)
    heavy_count = total // (petal_mass // 2 + 1)
    cross_floor = petal_mass * petal_mass // 4
    balanced = (
        comb(total, 2) * (cross_floor + offset * petal_mass) // cross_floor
    )
    collision = comb(heavy_count, 2) * (
        comb(petal_mass - 1, 2) + offset * petal_mass
    )
    return {
        **clean,
        "chart": clean["cap"] + balanced + collision,
        "balanced": balanced,
        "collision": collision,
    }


def refined_kernel_record_cap(kprime: int, corank: int) -> int:
    if corank == 1:
        return 8147918
    if corank == 9:
        return 61871313426630599
    rank = 10 - corank
    shortened = kprime - rank
    zero_endpoint = Fraction(
        falling(1048576 + shortened, corank + 1),
        (67472 + shortened) * rising(67473, corank - 1),
    )
    maximum_endpoint = Fraction(
        falling(1048576 + corank, corank + 1),
        rising(67473, corank),
    )
    return int(max(zero_endpoint, maximum_endpoint))


def refined_kernel_capacity(kprime: int) -> int:
    nprime = 1048576 + kprime
    quotient = kprime - 10
    return sum(
        comb(nprime, 10 - corank)
        * refined_kernel_record_cap(kprime, corank)
        * comb(quotient, corank + 1)
        for corank in range(1, min(9, quotient - 1) + 1)
    )


def completion_defect_row(
    quotient: int,
    mprime: int,
    support: int,
    depth: int,
) -> dict[str, Any]:
    carrier_caps = {
        str(defect): (
            comb(quotient + (defect + 1) * (support - 1), support)
            * comb(mprime - support, 11 - support)
        )
        for defect in range(1, depth + 1)
    }
    ceiling = quotient - depth - 1
    value, maximizing = max(
        (completion_ladder_value(mprime, support, count), count)
        for count in range(ceiling + 1)
    )
    deletion = comb(mprime, support - 1) * value // support
    return {
        "carrier_caps": carrier_caps,
        "deletion_cap": deletion,
        "completion_maximizer": maximizing,
        "active_cap": max([deletion, *carrier_caps.values()]),
    }


def universal_completion_row(
    quotient: int,
    mprime: int,
    support: int,
) -> dict[str, int]:
    value, maximizing = max(
        (completion_ladder_value(mprime, support, count), count)
        for count in range(quotient + 1)
    )
    return {
        "completion_maximizer": maximizing,
        "incidence_cap": comb(mprime, support - 1) * value // support,
    }


def refined_payment_row(
    kprime: int,
    records: int,
    baseline: int,
    sparse_caps: dict[int, int],
    sparse_weights: dict[int, int],
) -> dict[str, Any]:
    nprime = 1048576 + kprime
    mprime = 67472 + kprime
    core_rows = {
        str(core): integral_core_offset_row(kprime, core)
        for core in range(9, kprime)
    }
    maximizing_core = max(core_rows, key=lambda key: core_rows[key]["chart"])
    chart = core_rows[maximizing_core]["chart"]
    marks = comb(nprime, 9) * chart
    premium = sum(sparse_weights[support] * sparse_caps[support] for support in sparse_caps)
    kernel = refined_kernel_capacity(kprime)
    full_rank = (marks + records * premium) // baseline
    total = kernel + full_rank
    demand_numerator = 990810934 * records * comb(mprime, 11)
    demand = ceil_ratio(demand_numerator, 10**9)
    coefficient = baseline * 990810934 * comb(mprime, 11) - 10**9 * premium
    raw = records * coefficient - 10**9 * (baseline * kernel + marks)
    return {
        "K_prime": kprime,
        "n_prime": nprime,
        "m_prime": mprime,
        "maximizing_core": int(maximizing_core),
        "uniform_rank9_chart_cap": chart,
        "kernel_capacity": kernel,
        "global_rank9_mark_capacity": marks,
        "active_sparse_premium": premium,
        "full_rank_capacity": full_rank,
        "total_capacity": total,
        "required_incidence": demand,
        "demand_capacity_gap": demand - total,
        "record_coefficient_cross": coefficient,
        "floor_record_raw_cross": raw,
    }


def completion_deletion_cap(mprime: int, support: int, ceiling: int) -> int:
    value = max(
        completion_ladder_value(mprime, support, count)
        for count in range(ceiling + 1)
    )
    return comb(mprime, support - 1) * value // support


def cross_support_branch_premiums(kprime: int) -> tuple[int, dict[str, int]]:
    quotient = kprime - 10
    mprime = 67472 + kprime
    weights = {support: comb(11 - support, 2) for support in range(2, 10)}
    caps = {
        support: (
            completion_defect_row(
                quotient,
                mprime,
                support,
                {2: 7, 3: 2, 4: 1, 5: 0}[support],
            )["active_cap"]
            if support <= 5
            else universal_completion_row(quotient, mprime, support)["incidence_cap"]
        )
        for support in range(2, 10)
    }
    uncoupled = sum(weights[support] * caps[support] for support in caps)
    branches: dict[str, int] = {}
    for defect in range(5):
        branch = dict(caps)
        branch[5] = min(
            branch[5], completion_deletion_cap(mprime, 5, quotient - defect)
        )
        for target in range(2, 10):
            if 5 + (defect + 1) * target - defect - 1 <= 10:
                carrier = quotient + 4 + defect * (target - 1)
                cross_cap = comb(carrier, target) * comb(
                    mprime - target, 11 - target
                )
                branch[target] = min(branch[target], cross_cap)
        branches[f"defect_{defect}"] = sum(
            weights[support] * branch[support] for support in branch
        )
    fallback = dict(caps)
    fallback[5] = min(
        fallback[5], completion_deletion_cap(mprime, 5, quotient - 5)
    )
    branches["fallback"] = sum(
        weights[support] * fallback[support] for support in fallback
    )
    return uncoupled, branches


def cross_support_payment_row(kprime: int, records: int) -> dict[str, Any]:
    nprime = 1048576 + kprime
    mprime = 67472 + kprime
    quotient = kprime - 10
    core_rows = {
        core: integral_core_offset_row(kprime, core)["chart"]
        for core in range(9, kprime)
    }
    maximizing_core = max(core_rows, key=core_rows.get)
    chart = core_rows[maximizing_core]
    marks = comb(nprime, 9) * chart
    kernel = refined_kernel_capacity(kprime)
    uncoupled, branches = cross_support_branch_premiums(kprime)
    premium = max(branches.values())
    full_rank = (marks + records * premium) // 55
    total = kernel + full_rank
    demand = records * comb(mprime, 11) - comb(nprime, 11)
    coefficient = 55 * comb(mprime, 11) - premium
    raw = (
        records * coefficient
        - 55 * comb(nprime, 11)
        - 55 * kernel
        - marks
    )
    return {
        "n": nprime,
        "m": mprime,
        "q": quotient,
        "isolated_global_cap": comb(nprime, 11),
        "max_core": maximizing_core,
        "chart": chart,
        "kernel_capacity": kernel,
        "rank_nine_marks": marks,
        "uncoupled_completion_premium": uncoupled,
        "branch_premiums": branches,
        "completion_premium": premium,
        "premium_saving": uncoupled - premium,
        "full_rank_capacity": full_rank,
        "total_capacity": total,
        "required_component_incidence": demand,
        "gap": demand - total,
        "record_coefficient_cross": coefficient,
        "floor_record_raw_cross": raw,
    }


def joint_sparse_shadow_row(kprime: int, records: int) -> dict[str, Any]:
    nprime = 1048576 + kprime
    mprime = 67472 + kprime
    quotient = kprime - 10
    coranks = list(range(1, min(9, quotient - 1) + 1))
    record_caps = [kernel_record_cap(kprime, corank) for corank in coranks]
    extensions = [comb(quotient, corank + 1) for corank in coranks]
    kernel_terms = [
        comb(nprime, 10 - corank) * cap * extension
        for corank, cap, extension in zip(coranks, record_caps, extensions)
    ]
    kernel = sum(kernel_terms)

    core_sizes = list(range(9, kprime))
    core_caps = [
        joint_core_offset_capacity(mprime - core, nprime - core, core - 9)
        for core in core_sizes
    ]
    chart = max(core_caps)
    maximizing_core = core_sizes[core_caps.index(chart)]
    marks = comb(nprime, 9) * chart

    structured_terms = {
        str(support): (
            comb(quotient + 4, support) * comb(mprime - support, 11 - support)
        )
        for support in range(2, 6)
    }
    completion_maximizers: dict[str, int] = {}
    unstructured_terms: dict[str, int] = {}
    for support in range(2, 6):
        value, completions = max(
            (completion_ladder_value(mprime, support, count), count)
            for count in range(quotient)
        )
        completion_maximizers[str(support)] = completions
        unstructured_terms[str(support)] = (
            comb(mprime, support - 1) * value // support
        )
    shadow_counts = {
        str(support): 55 - comb(11 - support, 2)
        for support in range(2, 6)
    }
    premium_weights = {
        support: 45 - shadow_counts[support]
        for support in shadow_counts
    }
    structured_premium = sum(
        premium_weights[support] * structured_terms[support]
        for support in premium_weights
    )
    unstructured_premium = sum(
        premium_weights[support] * unstructured_terms[support]
        for support in premium_weights
    )
    premium = max(structured_premium, unstructured_premium)
    full_rank = (marks + records * premium) // 45
    total = kernel + full_rank
    demand_numerator = 990810934 * records * comb(mprime, 11)
    demand = ceil_ratio(demand_numerator, 10**9)
    coefficient = 45 * 990810934 * comb(mprime, 11) - 10**9 * premium
    raw = records * coefficient - 10**9 * (45 * kernel + marks)
    return {
        "K_prime": kprime,
        "n_prime": nprime,
        "m_prime": mprime,
        "quotient_dimension": quotient,
        "kernel_coranks": coranks,
        "kernel_record_caps": record_caps,
        "kernel_extension_factors": extensions,
        "kernel_incidence_terms": kernel_terms,
        "kernel_incidence_cap": kernel,
        "rank9_core_sizes": core_sizes,
        "rank9_core_caps": core_caps,
        "rank9_core_maximizer": maximizing_core,
        "uniform_rank9_chart_cap": chart,
        "global_rank9_mark_capacity": marks,
        "structured_support_terms": structured_terms,
        "unstructured_completion_maximizers": completion_maximizers,
        "unstructured_support_terms": unstructured_terms,
        "rank9_shadow_counts": shadow_counts,
        "premium_weights": premium_weights,
        "structured_sparse_premium": structured_premium,
        "unstructured_sparse_premium": unstructured_premium,
        "active_sparse_premium": premium,
        "full_rank_joint_capacity_at_record_floor": full_rank,
        "total_capacity_at_record_floor": total,
        "required_incidence_at_record_floor": demand,
        "demand_capacity_gap": demand - total,
        "record_coefficient_cross": coefficient,
        "raw_demand_capacity_cross": raw,
    }


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


def two_step_hierarchy_rows() -> list[list[int]]:
    return [
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


def solve_exact(matrix: list[list[Fraction]], right: list[Fraction]) -> list[Fraction]:
    size = len(right)
    augmented = [list(row) + [value] for row, value in zip(matrix, right)]
    for column in range(size):
        pivot = next((row for row in range(column, size) if augmented[row][column]), None)
        require(pivot is not None, f"two-step dual pivot {column}")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            scale = augmented[row][column]
            augmented[row] = [
                left - scale * pivot_value
                for left, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [augmented[index][-1] for index in range(size)]


def kernel_two_step_certificate(
    kprime: int,
) -> tuple[Fraction, list[Fraction], list[Fraction], list[str]]:
    _, caps, coefficients, shadow_budget, containment_budget = kernel_rank8_shadow_data(kprime)
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
    odd_price = sum(coefficients[index] * factors[index] for index in range(0, 9, 2))
    even_price = sum(coefficients[index] * factors[index] for index in range(1, 9, 2))
    even_base = (containment_budget - odd_price * odd_base) / even_price
    allocation = [
        factor * (odd_base if index % 2 == 0 else even_base)
        for index, factor in enumerate(factors)
    ]
    require(all(value > 0 for value in allocation), f"two-step positive allocation {kprime}")
    require(all(value <= cap for value, cap in zip(allocation, caps)), f"two-step caps {kprime}")
    require(allocation[0] == caps[0], f"two-step corank-one cap {kprime}")
    require(all(allocation[index] < caps[index] for index in range(1, 9)), f"two-step other caps {kprime}")
    require(sum(coefficients[i] * allocation[i] for i in range(9)) == containment_budget, f"two-step containment {kprime}")
    require(sum(kernel_shadow_weights_caps(kprime)[0][i] * allocation[i] for i in range(9)) < shadow_budget, f"two-step shadow slack {kprime}")
    for dimension in range(3, 10):
        require(
            raising[dimension] * allocation[dimension - 1]
            == multiplicity[dimension] * allocation[dimension - 3],
            f"two-step hierarchy d={dimension} K={kprime}",
        )

    # Variables are the containment multiplier, the corank-one cap multiplier,
    # and the seven hierarchy multipliers H_3,...,H_9.
    dual_matrix = []
    for dimension in range(1, 10):
        row = [coefficients[dimension - 1], Fraction(1 if dimension == 1 else 0)]
        row.extend(Fraction(0) for _ in range(7))
        if dimension >= 3:
            row[dimension - 1] += raising[dimension]
        if dimension + 2 <= 9:
            row[dimension + 1] -= multiplicity[dimension + 2]
        dual_matrix.append(row)
    dual = solve_exact(dual_matrix, [Fraction(1) for _ in range(9)])
    require(all(value >= 0 for value in dual), f"two-step dual signs {kprime}")
    optimum = sum(allocation, Fraction(0))
    require(dual[0] * containment_budget + dual[1] * caps[0] == optimum, f"two-step strong duality {kprime}")
    branches = kernel_shadow_weights_caps(kprime)[2]
    return optimum, allocation, dual, branches


def multistep_hierarchy_rows() -> list[list[int]]:
    return [
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


def multistep_raising(kprime: int, step: int, dimension: int) -> Fraction:
    return Fraction(
        comb(dimension + 2, step) * comb(67472 + dimension, step),
        comb(kprime - dimension - 11 + step, step),
    )


def multistep_multiplicity(step: int, dimension: int) -> int:
    return comb(9 - dimension + step, step)


MULTISTEP_DUAL_TREE = [[2, 3], [2, 4], [2, 6], [2, 8], [3, 5], [2, 7], [2, 9]]
MULTISTEP_TIGHT_ROWS = [
    [2, 3], [2, 4], [2, 6], [2, 7], [2, 8], [2, 9],
    [3, 5], [3, 7], [3, 8], [3, 9],
    [4, 6], [4, 8], [4, 9],
    [5, 7], [5, 9], [6, 8], [7, 9],
]


def multistep_tree_factors(
    kprime: int,
    tree: list[list[int]],
) -> tuple[list[Fraction], list[int]]:
    factors = [Fraction(0) for _ in range(9)]
    roots = [0 for _ in range(9)]
    factors[0] = factors[1] = Fraction(1)
    roots[0], roots[1] = 1, 2
    changed = True
    while changed:
        changed = False
        for step, source in tree:
            target = source - step
            source_index, target_index = source - 1, target - 1
            ratio = Fraction(
                multistep_multiplicity(step, source),
                multistep_raising(kprime, step, source),
            )
            if roots[target_index] and not roots[source_index]:
                factors[source_index] = ratio * factors[target_index]
                roots[source_index] = roots[target_index]
                changed = True
            elif roots[source_index] and not roots[target_index]:
                factors[target_index] = factors[source_index] / ratio
                roots[target_index] = roots[source_index]
                changed = True
    require(all(roots), f"multistep tree spans K={kprime}")
    return factors, roots


def kernel_multistep_certificate(
    kprime: int,
) -> tuple[Fraction, list[Fraction], list[Fraction], list[str], list[list[int]]]:
    _, caps, coefficients, shadow_budget, containment_budget = kernel_rank8_shadow_data(kprime)
    shadow = kernel_shadow_weights_caps(kprime)[0]
    factors, roots = multistep_tree_factors(kprime, MULTISTEP_DUAL_TREE)
    first_base = caps[0]
    first_price = sum(coefficients[i] * factors[i] for i in range(9) if roots[i] == 1)
    second_price = sum(coefficients[i] * factors[i] for i in range(9) if roots[i] == 2)
    second_base = (containment_budget - first_price * first_base) / second_price
    allocation = [
        factors[index] * (first_base if roots[index] == 1 else second_base)
        for index in range(9)
    ]
    require(all(0 < value <= cap for value, cap in zip(allocation, caps)), f"multistep caps K={kprime}")
    require(allocation[0] == caps[0], f"multistep corank-one cap K={kprime}")
    require(all(allocation[index] < caps[index] for index in range(1, 9)), f"multistep other caps K={kprime}")
    require(sum(coefficients[i] * allocation[i] for i in range(9)) == containment_budget, f"multistep containment K={kprime}")
    require(sum(shadow[i] * allocation[i] for i in range(9)) < shadow_budget, f"multistep shadow slack K={kprime}")

    tight = []
    for step in range(2, 9):
        for dimension in range(step + 1, 10):
            left = multistep_raising(kprime, step, dimension) * allocation[dimension - 1]
            right = multistep_multiplicity(step, dimension) * allocation[dimension - step - 1]
            require(left <= right, f"multistep t={step} d={dimension} K={kprime}")
            if left == right:
                tight.append([step, dimension])
    require(tight == MULTISTEP_TIGHT_ROWS, f"multistep tight rows K={kprime}")

    dual_matrix = []
    for dimension in range(1, 10):
        row = [coefficients[dimension - 1], Fraction(1 if dimension == 1 else 0)]
        for step, source in MULTISTEP_DUAL_TREE:
            coefficient = Fraction(0)
            if dimension == source:
                coefficient += multistep_raising(kprime, step, source)
            if dimension == source - step:
                coefficient -= multistep_multiplicity(step, source)
            row.append(coefficient)
        dual_matrix.append(row)
    dual = solve_exact(dual_matrix, [Fraction(1) for _ in range(9)])
    require(all(value >= 0 for value in dual), f"multistep dual signs K={kprime}")
    optimum = sum(allocation, Fraction(0))
    require(dual[0] * containment_budget + dual[1] * caps[0] == optimum, f"multistep strong duality K={kprime}")
    branches = kernel_shadow_weights_caps(kprime)[2]
    return optimum, allocation, dual, branches, tight


PROJECTIVE_PAIR_RECORD_CAP = 8147918
PROJECTIVE_PAIR_DUAL_TREE = [[2, 3], [3, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9]]
PROJECTIVE_PAIR_TIGHT_ROWS = [
    [2, 3], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9],
    [3, 4], [3, 6], [3, 7], [3, 8], [3, 9],
    [4, 5], [4, 7], [4, 8], [4, 9],
    [5, 6], [5, 8], [5, 9],
    [6, 7], [6, 9], [7, 8], [8, 9],
]


def kernel_projective_pair_data(
    kprime: int,
) -> tuple[list[Fraction], list[str], list[Fraction], list[Fraction], Fraction, Fraction]:
    terms = kernel_hybrid_terms(kprime)
    nprime = 1048576 + kprime
    extension = comb(kprime - 10, 2)
    ambient = comb(nprime, 9) * PROJECTIVE_PAIR_RECORD_CAP * extension // 3
    support = terms[0][1]
    terms[0] = (ambient, support, "ambient" if ambient <= support else "record")
    caps = [Fraction(min(left, right), 274980728111260126) for left, right, _ in terms]
    branches = [branch for _, _, branch in terms]
    _, _, containment, shadow_budget, containment_budget = kernel_rank8_shadow_data(kprime)
    shadow = kernel_shadow_weights_caps(kprime)[0]
    return caps, branches, shadow, containment, shadow_budget, containment_budget


def kernel_projective_pair_certificate(
    kprime: int,
) -> tuple[Fraction, list[Fraction], dict[int, Fraction], list[str], list[list[int]]]:
    caps, branches, shadow, containment, shadow_budget, containment_budget = kernel_projective_pair_data(kprime)
    tree = [tuple(edge) for edge in PROJECTIVE_PAIR_DUAL_TREE]
    parent = {source: (step, source) for step, source in tree}
    children: dict[int, list[tuple[int, int]]] = {dimension: [] for dimension in range(1, 10)}
    for step, source in tree:
        children[source - step].append((step, source))

    factors = [Fraction(0) for _ in range(9)]
    roots = [0 for _ in range(9)]
    factors[0] = factors[1] = Fraction(1)
    roots[0], roots[1] = 1, 2
    for source in range(3, 10):
        step, _ = parent[source]
        target = source - step
        factors[source - 1] = (
            multistep_multiplicity(step, source)
            * factors[target - 1]
            / multistep_raising(kprime, step, source)
        )
        roots[source - 1] = roots[target - 1]
    require(roots == [1, 2, 1, 1, 1, 1, 1, 1, 1], f"projective roots K={kprime}")
    allocation = [factors[index] * caps[roots[index] - 1] for index in range(9)]

    hierarchy_dual: dict[tuple[int, int], Fraction] = {}
    for source in range(9, 2, -1):
        edge = parent[source]
        child_charge = sum(
            multistep_multiplicity(*child) * hierarchy_dual[child]
            for child in children[source]
        )
        hierarchy_dual[edge] = (
            1 + child_charge
        ) / multistep_raising(kprime, *edge)
    cap_dual = {
        root: 1 + sum(
            multistep_multiplicity(*child) * hierarchy_dual[child]
            for child in children[root]
        )
        for root in (1, 2)
    }

    require(all(0 < number <= cap for number, cap in zip(allocation, caps)), f"projective caps K={kprime}")
    require(allocation[:2] == caps[:2], f"projective root caps K={kprime}")
    require(all(allocation[index] < caps[index] for index in range(2, 9)), f"projective nonroot caps K={kprime}")
    require(branches[:2] == ["ambient", "ambient"], f"projective root branches K={kprime}")
    require(sum(shadow[index] * allocation[index] for index in range(9)) < shadow_budget, f"projective shadow slack K={kprime}")
    require(sum(containment[index] * allocation[index] for index in range(9)) < containment_budget, f"projective containment slack K={kprime}")

    tight = []
    for step in range(2, 9):
        for dimension in range(step + 1, 10):
            left = multistep_raising(kprime, step, dimension) * allocation[dimension - 1]
            right = multistep_multiplicity(step, dimension) * allocation[dimension - step - 1]
            require(left <= right, f"projective hierarchy t={step} d={dimension} K={kprime}")
            if left == right:
                tight.append([step, dimension])
    require(tight == PROJECTIVE_PAIR_TIGHT_ROWS, f"projective tight rows K={kprime}")
    require(all(number > 0 for number in hierarchy_dual.values()), f"projective hierarchy dual K={kprime}")
    require(all(number > 0 for number in cap_dual.values()), f"projective cap dual K={kprime}")
    optimum = sum(allocation, Fraction(0))
    require(optimum == cap_dual[1] * caps[0] + cap_dual[2] * caps[1], f"projective strong duality K={kprime}")
    return optimum, allocation, cap_dual, branches, tight


PROJECTIVE_BASIS_RECORD_CAP = 84416263
PROJECTIVE_BASIS_DUAL_TREE = [[2, 3], [2, 4], [2, 6], [2, 8], [3, 5], [2, 7], [2, 9]]
PROJECTIVE_BASIS_TIGHT_ROWS = [
    [2, 3], [2, 4], [2, 6], [2, 7], [2, 8], [2, 9],
    [3, 5], [3, 7], [3, 8], [3, 9],
    [4, 6], [4, 8], [4, 9],
    [5, 7], [5, 9], [6, 8], [7, 9],
]


def kernel_projective_basis_data(
    kprime: int,
) -> tuple[list[Fraction], list[str], list[Fraction], list[Fraction], Fraction, Fraction]:
    terms = kernel_hybrid_terms(kprime)
    nprime = 1048576 + kprime
    extension1 = comb(kprime - 10, 2)
    extension2 = comb(kprime - 10, 3)
    ambient1 = comb(nprime, 9) * PROJECTIVE_PAIR_RECORD_CAP * extension1 // 3
    ambient2 = comb(nprime, 8) * PROJECTIVE_BASIS_RECORD_CAP * extension2 // 4
    terms[0] = (ambient1, terms[0][1], "ambient" if ambient1 <= terms[0][1] else "record")
    terms[1] = (ambient2, terms[1][1], "ambient" if ambient2 <= terms[1][1] else "record")
    caps = [Fraction(min(left, right), 274980728111260126) for left, right, _ in terms]
    branches = [branch for _, _, branch in terms]
    _, _, containment, shadow_budget, containment_budget = kernel_rank8_shadow_data(kprime)
    shadow = kernel_shadow_weights_caps(kprime)[0]
    return caps, branches, shadow, containment, shadow_budget, containment_budget


def kernel_projective_basis_certificate(
    kprime: int,
) -> tuple[Fraction, list[Fraction], dict[int, Fraction], list[str], list[list[int]]]:
    caps, branches, shadow, containment, shadow_budget, containment_budget = kernel_projective_basis_data(kprime)
    tree = [tuple(edge) for edge in PROJECTIVE_BASIS_DUAL_TREE]
    parent = {source: (step, source) for step, source in tree}
    children: dict[int, list[tuple[int, int]]] = {dimension: [] for dimension in range(1, 10)}
    for step, source in tree:
        children[source - step].append((step, source))

    factors = [Fraction(0) for _ in range(9)]
    roots = [0 for _ in range(9)]
    factors[0] = factors[1] = Fraction(1)
    roots[0], roots[1] = 1, 2
    for source in range(3, 10):
        step, _ = parent[source]
        target = source - step
        factors[source - 1] = (
            multistep_multiplicity(step, source)
            * factors[target - 1]
            / multistep_raising(kprime, step, source)
        )
        roots[source - 1] = roots[target - 1]
    require(roots == [1, 2, 1, 2, 2, 2, 2, 2, 2], f"projective-basis roots K={kprime}")
    allocation = [factors[index] * caps[roots[index] - 1] for index in range(9)]

    hierarchy_dual: dict[tuple[int, int], Fraction] = {}
    for source in range(9, 2, -1):
        edge = parent[source]
        child_charge = sum(
            multistep_multiplicity(*child) * hierarchy_dual[child]
            for child in children[source]
        )
        hierarchy_dual[edge] = (1 + child_charge) / multistep_raising(kprime, *edge)
    cap_dual = {
        root: 1 + sum(
            multistep_multiplicity(*child) * hierarchy_dual[child]
            for child in children[root]
        )
        for root in (1, 2)
    }

    require(all(0 < number <= cap for number, cap in zip(allocation, caps)), f"projective-basis caps K={kprime}")
    require(allocation[:2] == caps[:2], f"projective-basis root caps K={kprime}")
    require(all(allocation[index] < caps[index] for index in range(2, 9)), f"projective-basis nonroot caps K={kprime}")
    require(branches[:2] == ["ambient", "ambient"], f"projective-basis branches K={kprime}")
    require(sum(shadow[index] * allocation[index] for index in range(9)) < shadow_budget, f"projective-basis shadow slack K={kprime}")
    require(sum(containment[index] * allocation[index] for index in range(9)) < containment_budget, f"projective-basis containment slack K={kprime}")

    tight = []
    for step in range(2, 9):
        for dimension in range(step + 1, 10):
            left = multistep_raising(kprime, step, dimension) * allocation[dimension - 1]
            right = multistep_multiplicity(step, dimension) * allocation[dimension - step - 1]
            require(left <= right, f"projective-basis hierarchy t={step} d={dimension} K={kprime}")
            if left == right:
                tight.append([step, dimension])
    require(tight == PROJECTIVE_BASIS_TIGHT_ROWS, f"projective-basis tight rows K={kprime}")
    require(all(number > 0 for number in hierarchy_dual.values()), f"projective-basis hierarchy dual K={kprime}")
    require(all(number > 0 for number in cap_dual.values()), f"projective-basis cap dual K={kprime}")
    optimum = sum(allocation, Fraction(0))
    require(optimum == cap_dual[1] * caps[0] + cap_dual[2] * caps[1], f"projective-basis strong duality K={kprime}")
    return optimum, allocation, cap_dual, branches, tight


PROJECTIVE_FRAME_RECORD_CAP = 983902549
PROJECTIVE_FRAME_DUAL_FOREST = [[2, 4], [2, 5], [3, 6], [4, 7], [5, 8], [6, 9]]
PROJECTIVE_FRAME_TIGHT_ROWS = [
    [2, 4], [2, 5], [2, 7], [2, 8], [2, 9],
    [3, 6], [3, 8], [3, 9],
    [4, 7], [4, 9], [5, 8], [6, 9],
]


def kernel_projective_frame_data(
    kprime: int,
) -> tuple[list[Fraction], list[str], list[Fraction], list[Fraction], Fraction, Fraction]:
    terms = kernel_hybrid_terms(kprime)
    nprime = 1048576 + kprime
    extensions = [comb(kprime - 10, length) for length in (2, 3, 4)]
    record_caps = [PROJECTIVE_PAIR_RECORD_CAP, PROJECTIVE_BASIS_RECORD_CAP, PROJECTIVE_FRAME_RECORD_CAP]
    for index in range(3):
        rank = 9 - index
        ambient = comb(nprime, rank) * record_caps[index] * extensions[index] // (index + 3)
        terms[index] = (
            ambient,
            terms[index][1],
            "ambient" if ambient <= terms[index][1] else "record",
        )
    caps = [Fraction(min(left, right), 274980728111260126) for left, right, _ in terms]
    branches = [branch for _, _, branch in terms]
    _, _, containment, shadow_budget, containment_budget = kernel_rank8_shadow_data(kprime)
    shadow = kernel_shadow_weights_caps(kprime)[0]
    return caps, branches, shadow, containment, shadow_budget, containment_budget


def kernel_projective_frame_certificate(
    kprime: int,
) -> tuple[Fraction, list[Fraction], dict[int, Fraction], list[str], list[list[int]]]:
    caps, branches, shadow, containment, shadow_budget, containment_budget = kernel_projective_frame_data(kprime)
    forest = [tuple(edge) for edge in PROJECTIVE_FRAME_DUAL_FOREST]
    parent = {source: (step, source) for step, source in forest}
    children: dict[int, list[tuple[int, int]]] = {dimension: [] for dimension in range(1, 10)}
    for step, source in forest:
        children[source - step].append((step, source))

    factors = [Fraction(0) for _ in range(9)]
    roots = [0 for _ in range(9)]
    for root in (1, 2, 3):
        factors[root - 1] = Fraction(1)
        roots[root - 1] = root
    for source in range(4, 10):
        step, _ = parent[source]
        target = source - step
        factors[source - 1] = (
            multistep_multiplicity(step, source)
            * factors[target - 1]
            / multistep_raising(kprime, step, source)
        )
        roots[source - 1] = roots[target - 1]
    require(roots == [1, 2, 3, 2, 3, 3, 3, 3, 3], f"projective-frame roots K={kprime}")
    allocation = [factors[index] * caps[roots[index] - 1] for index in range(9)]

    hierarchy_dual: dict[tuple[int, int], Fraction] = {}
    for source in range(9, 3, -1):
        edge = parent[source]
        child_charge = sum(
            multistep_multiplicity(*child) * hierarchy_dual[child]
            for child in children[source]
        )
        hierarchy_dual[edge] = (1 + child_charge) / multistep_raising(kprime, *edge)
    cap_dual = {
        root: 1 + sum(
            multistep_multiplicity(*child) * hierarchy_dual[child]
            for child in children[root]
        )
        for root in (1, 2, 3)
    }

    require(all(0 < number <= cap for number, cap in zip(allocation, caps)), f"projective-frame caps K={kprime}")
    require(allocation[:3] == caps[:3], f"projective-frame root caps K={kprime}")
    require(all(allocation[index] < caps[index] for index in range(3, 9)), f"projective-frame nonroot caps K={kprime}")
    require(branches[:3] == ["ambient", "ambient", "ambient"], f"projective-frame branches K={kprime}")
    require(sum(shadow[index] * allocation[index] for index in range(9)) < shadow_budget, f"projective-frame shadow slack K={kprime}")
    require(sum(containment[index] * allocation[index] for index in range(9)) < containment_budget, f"projective-frame containment slack K={kprime}")

    tight = []
    for step in range(2, 9):
        for dimension in range(step + 1, 10):
            left = multistep_raising(kprime, step, dimension) * allocation[dimension - 1]
            right = multistep_multiplicity(step, dimension) * allocation[dimension - step - 1]
            require(left <= right, f"projective-frame hierarchy t={step} d={dimension} K={kprime}")
            if left == right:
                tight.append([step, dimension])
    require(tight == PROJECTIVE_FRAME_TIGHT_ROWS, f"projective-frame tight rows K={kprime}")
    require(all(number > 0 for number in hierarchy_dual.values()), f"projective-frame hierarchy dual K={kprime}")
    require(all(number > 0 for number in cap_dual.values()), f"projective-frame cap dual K={kprime}")
    optimum = sum(allocation, Fraction(0))
    require(
        optimum == sum(cap_dual[root] * caps[root - 1] for root in (1, 2, 3)),
        f"projective-frame strong duality K={kprime}",
    )
    return optimum, allocation, cap_dual, branches, tight


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
    weighted_last_open_k = 20617
    weighted_last_open_n = 1048576 + weighted_last_open_k
    weighted_last_open_m = 67472 + weighted_last_open_k
    weighted_last_open_demand = ceil_ratio(
        lane_ppb
        * non_dense
        * comb(weighted_last_open_m, 9)
        * comb(weighted_last_open_m - 9, 2),
        10**9 * comb(weighted_last_open_n, 9),
    )
    weighted_last_open_cap = owner_cap * (weighted_last_open_m - 10) * weighted_last_open_n
    weighted_boundary_k = 20618
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
    residual_petal_last_open_k = 15634
    residual_petal_last_open_n = 1048576 + residual_petal_last_open_k
    residual_petal_last_open_m = 67472 + residual_petal_last_open_k
    residual_petal_last_open_numerator = (
        lane_ppb
        * non_dense
        * comb(residual_petal_last_open_m, 9)
        * comb(residual_petal_last_open_m - 9, 2)
    )
    residual_petal_last_open_denominator = (
        10**9 * comb(residual_petal_last_open_n, 9)
    )
    residual_petal_last_open_demand = ceil_ratio(
        residual_petal_last_open_numerator,
        residual_petal_last_open_denominator,
    )
    residual_petal_last_open_j = residual_petal_last_open_k - 1
    residual_petal_last_open_cap_twice = (
        owner_cap
        * (residual_petal_last_open_n - residual_petal_last_open_j)
        * (residual_petal_last_open_m + residual_petal_last_open_j - 20)
    )
    residual_petal_last_open_cap = residual_petal_last_open_cap_twice // 2
    residual_petal_last_open_raw_cross = (
        2 * residual_petal_last_open_numerator
        - residual_petal_last_open_cap_twice
        * residual_petal_last_open_denominator
    )
    residual_petal_boundary_k = 15635
    residual_petal_boundary_n = 1048576 + residual_petal_boundary_k
    residual_petal_boundary_m = 67472 + residual_petal_boundary_k
    residual_petal_boundary_numerator = (
        lane_ppb
        * non_dense
        * comb(residual_petal_boundary_m, 9)
        * comb(residual_petal_boundary_m - 9, 2)
    )
    residual_petal_boundary_denominator = (
        10**9 * comb(residual_petal_boundary_n, 9)
    )
    residual_petal_boundary_demand = ceil_ratio(
        residual_petal_boundary_numerator,
        residual_petal_boundary_denominator,
    )
    residual_petal_boundary_j = residual_petal_boundary_k - 1
    residual_petal_boundary_cap_twice = (
        owner_cap
        * (residual_petal_boundary_n - residual_petal_boundary_j)
        * (residual_petal_boundary_m + residual_petal_boundary_j - 20)
    )
    residual_petal_boundary_cap = residual_petal_boundary_cap_twice // 2
    residual_petal_boundary_raw_cross = (
        2 * residual_petal_boundary_numerator
        - residual_petal_boundary_cap_twice
        * residual_petal_boundary_denominator
    )
    exact_petal_budget = 981105

    def exact_petal_line(a: int) -> tuple[int, int]:
        full = 1 + exact_petal_budget // a
        remainder = exact_petal_budget % a
        slope = exact_petal_budget + a
        intercept = (
            slope * (67462 - a)
            + (full * a * (a - 1) + remainder * (remainder - 1)) // 2
        )
        return slope, intercept

    exact_petal_a = 67472
    exact_petal_slope, exact_petal_intercept = exact_petal_line(exact_petal_a)

    def exact_petal_row(kprime: int) -> tuple[int, int, int]:
        nprime, mprime = 1048576 + kprime, 67472 + kprime
        numerator = (
            lane_ppb
            * non_dense
            * comb(mprime, 9)
            * comb(mprime - 9, 2)
        )
        denominator = 10**9 * comb(nprime, 9)
        upper = owner_cap * (exact_petal_slope * kprime + exact_petal_intercept)
        return ceil_ratio(numerator, denominator), upper, numerator - upper * denominator

    exact_petal_last_open_k = 15528
    exact_petal_boundary_k = 15529
    exact_petal_last_open = exact_petal_row(exact_petal_last_open_k)
    exact_petal_boundary = exact_petal_row(exact_petal_boundary_k)
    exact_petal_endpoints = [67472, 70078, 70079, 75469, 75470, 81758, 81759, 83096]
    exact_petal_endpoint_value = (
        exact_petal_slope * 15634 + exact_petal_intercept
    )
    exact_petal_endpoint_gaps = [
        exact_petal_endpoint_value
        - (lambda line: line[0] * 15634 + line[1])(exact_petal_line(a))
        for a in exact_petal_endpoints
    ]
    minimal_split_A = 67473
    minimal_split_S = 1048577
    minimal_split_heavy_threshold = minimal_split_A // 2 + 1
    minimal_split_heavy_count = minimal_split_S // minimal_split_heavy_threshold
    minimal_split_clean = (
        (minimal_split_A - 2) * minimal_split_S * minimal_split_S // 8
    )
    minimal_split_balanced = comb(minimal_split_S, 2)
    minimal_split_collision = (
        comb(minimal_split_heavy_count, 2) * comb(minimal_split_A - 1, 2)
    )
    minimal_split_capacity = (
        minimal_split_clean + minimal_split_balanced + minimal_split_collision
    )
    minimal_split_demand_numerator = (
        990810934
        * non_dense
        * comb(67482, 9)
        * comb(67473, 2)
    )
    minimal_split_demand_denominator = 10**9 * comb(1048586, 9)
    minimal_split_demand = ceil_ratio(
        minimal_split_demand_numerator,
        minimal_split_demand_denominator,
    )
    minimal_split_raw_cross = (
        minimal_split_demand_numerator
        - minimal_split_capacity * minimal_split_demand_denominator
    )

    def core_offset_capacity(petal_mass: int, total: int, offset: int) -> dict[str, int]:
        heavy = total // (petal_mass // 2 + 1)
        cross_floor = petal_mass * petal_mass // 4
        balanced = (
            (cross_floor + offset * petal_mass) * comb(total, 2) // cross_floor
        )
        collision = comb(heavy, 2) * (
            comb(petal_mass - 1, 2) + offset * petal_mass
        )
        vertex_num = (petal_mass - 2) * total + 2 * heavy * offset * petal_mass
        vertex_den = 2 * (petal_mass - 2)
        center = vertex_num // vertex_den
        candidates = range(max(0, center - 3), min(total, center + 3) + 1)
        clean, light = max(
            (
                ell
                * (
                    (petal_mass - 2) * (total - ell)
                    + 2 * heavy * offset * petal_mass
                )
                // 2,
                ell,
            )
            for ell in candidates
        )
        return {
            "heavy_count": heavy,
            "balanced_cross_floor": cross_floor,
            "maximizing_light_mass": light,
            "clean_cap": clean,
            "balanced_cap": balanced,
            "collision_cap": collision,
            "total_cap": clean + balanced + collision,
        }

    k11_core_rows = []
    for core_size in (9, 10):
        petal_mass = 67483 - core_size
        offset = core_size - 9
        total = 1048587 - core_size
        k11_core_rows.append({
            "j": core_size,
            "P": petal_mass,
            "r": offset,
            "S": total,
            **core_offset_capacity(petal_mass, total, offset),
        })
    k11_chart_cap = max(row["total_cap"] for row in k11_core_rows)
    k11_global_marks = comb(1048587, 9) * k11_chart_cap
    k11_high_cap = k11_global_marks // 45
    k11_low_per_record = comb(67482, 10)
    k11_low_cap = non_dense * k11_low_per_record
    k11_total_cap = k11_high_cap + k11_low_cap
    k11_demand_numerator = 990810934 * non_dense * comb(67483, 11)
    k11_demand = ceil_ratio(k11_demand_numerator, 10**9)
    k11_raw_cross = k11_demand_numerator - 10**9 * k11_total_cap
    k11_record_coefficient_cross = (
        990810934 * comb(67483, 11) - 10**9 * k11_low_per_record
    )
    k12_n, k12_m = 1048588, 67484
    k12_core_rows = []
    for core_size in (9, 10, 11):
        petal_mass = k12_m - core_size
        offset = core_size - 9
        total = k12_n - core_size
        k12_core_rows.append({
            "j": core_size,
            "P": petal_mass,
            "r": offset,
            "S": total,
            **core_offset_capacity(petal_mass, total, offset),
        })
    quotient_line_caps = {
        str(support): quotient_line_label_cap(support, k12_m)
        for support in range(1, 6)
    }
    quotient_line_terms = {
        str(support): quotient_line_caps[str(support)]
        * comb(k12_m - support, 11 - support)
        for support in range(1, 6)
    }
    quotient_line_per_record = sum(quotient_line_terms.values())
    k12_kernel_record_cap = 16295594
    k12_kernel_cap = comb(k12_n, 9) * k12_kernel_record_cap
    k12_chart_cap = max(row["total_cap"] for row in k12_core_rows)
    k12_global_marks = comb(k12_n, 9) * k12_chart_cap
    k12_high_cap = k12_global_marks // 45
    k12_low_cap = non_dense * quotient_line_per_record
    k12_total_cap = k12_kernel_cap + k12_high_cap + k12_low_cap
    k12_demand_numerator = 990810934 * non_dense * comb(k12_m, 11)
    k12_demand = ceil_ratio(k12_demand_numerator, 10**9)
    k12_raw_cross = k12_demand_numerator - 10**9 * k12_total_cap
    k12_record_coefficient_cross = (
        990810934 * comb(k12_m, 11) - 10**9 * quotient_line_per_record
    )
    k13_n, k13_m = 1048589, 67485
    k13_core_rows = []
    for core_size in (9, 10, 11, 12):
        petal_mass = k13_m - core_size
        offset = core_size - 9
        total = k13_n - core_size
        k13_core_rows.append({
            "j": core_size,
            "P": petal_mass,
            "r": offset,
            "S": total,
            **core_offset_capacity(petal_mass, total, offset),
        })
    k13_structured_cap = sum(
        comb(7, support) * comb(k13_m - support, 11 - support)
        for support in range(2, 6)
    )
    k13_unstructured_terms = {
        str(support): (
            2 * comb(k13_m, support - 1)
            * comb(k13_m - support - 1, 11 - support) // support
        )
        for support in range(2, 6)
    }
    k13_sparse_cap = sum(k13_unstructured_terms.values())
    k13_coranks = [1, 2]
    k13_kernel_record_caps = [kernel_record_cap(13, corank) for corank in k13_coranks]
    k13_kernel_extensions = [comb(3, corank + 1) for corank in k13_coranks]
    k13_kernel_terms = [
        comb(k13_n, 10 - corank) * record_cap * extension
        for corank, record_cap, extension in zip(
            k13_coranks, k13_kernel_record_caps, k13_kernel_extensions
        )
    ]
    k13_kernel_cap = sum(k13_kernel_terms)
    k13_chart_cap = max(row["total_cap"] for row in k13_core_rows)
    k13_global_marks = comb(k13_n, 9) * k13_chart_cap
    k13_high_cap = k13_global_marks // 45
    k13_low_cap = non_dense * k13_sparse_cap
    k13_total_cap = k13_kernel_cap + k13_high_cap + k13_low_cap
    k13_demand_numerator = 990810934 * non_dense * comb(k13_m, 11)
    k13_demand = ceil_ratio(k13_demand_numerator, 10**9)
    k13_raw_cross = k13_demand_numerator - 10**9 * k13_total_cap
    k13_record_coefficient_cross = (
        990810934 * comb(k13_m, 11) - 10**9 * k13_sparse_cap
    )
    joint_sparse_rows = [
        joint_sparse_shadow_row(kprime, non_dense)
        for kprime in range(14, 22)
    ]
    joint_sparse_wall = joint_sparse_shadow_row(22, non_dense)
    completion_endpoint_totals = {
        str(row["K_prime"]): {
            "structured": sum(row["structured_support_terms"].values()),
            "unstructured": sum(row["unstructured_support_terms"].values()),
        }
        for row in (joint_sparse_rows[0], joint_sparse_rows[-1])
    }
    refined_record_cap = non_dense
    sparse_weights_45 = {2: 26, 3: 18, 4: 11, 5: 5}
    completion_defect_depths = {2: 7, 3: 2, 4: 1, 5: 0}
    full_shadow_deficits = {
        support: comb(11 - support, 2)
        for support in range(2, 10)
    }

    k22_m = 67494
    k22_q = 12
    k22_integral_rows = {
        str(core): integral_core_offset_row(22, core)
        for core in range(9, 22)
    }
    k22_integral_core = max(
        k22_integral_rows,
        key=lambda key: k22_integral_rows[key]["chart"],
    )
    k22_defect_rows = {
        support: completion_defect_row(
            k22_q,
            k22_m,
            support,
            1 if support <= 4 else 0,
        )
        for support in sparse_weights_45
    }
    k22_structured_caps = {
        support: comb(k22_q + 4, support) * comb(k22_m - support, 11 - support)
        for support in sparse_weights_45
    }
    k22_refined_caps = {
        support: k22_defect_rows[support]["active_cap"]
        for support in sparse_weights_45
    }
    k22_payment = refined_payment_row(
        22,
        refined_record_cap,
        45,
        k22_refined_caps,
        sparse_weights_45,
    )

    k23_m = 67495
    k23_q = 13
    k23_defect_rows = {
        support: completion_defect_row(
            k23_q,
            k23_m,
            support,
            completion_defect_depths[support],
        )
        for support in sparse_weights_45
    }
    k23_structured_caps = {
        support: comb(k23_q + 4, support) * comb(k23_m - support, 11 - support)
        for support in sparse_weights_45
    }
    k23_refined_caps = {
        support: k23_defect_rows[support]["active_cap"]
        for support in sparse_weights_45
    }
    k23_payment = refined_payment_row(
        23,
        refined_record_cap,
        45,
        k23_refined_caps,
        sparse_weights_45,
    )
    k24_old_defect_rows = {
        support: completion_defect_row(
            14,
            67496,
            support,
            completion_defect_depths[support],
        )
        for support in sparse_weights_45
    }
    k24_old_payment = refined_payment_row(
        24,
        refined_record_cap,
        45,
        {
            support: k24_old_defect_rows[support]["active_cap"]
            for support in sparse_weights_45
        },
        sparse_weights_45,
    )

    k24_universal_rows = {
        support: universal_completion_row(14, 67496, support)
        for support in range(6, 10)
    }
    full_deficit_payment_rows: dict[str, dict[str, Any]] = {}
    for kprime in range(24, 43):
        quotient = kprime - 10
        mprime = 67472 + kprime
        structured_caps = {
            support: (
                comb(quotient + 4, support)
                * comb(mprime - support, 11 - support)
            )
            for support in range(2, 6)
        }
        defect_rows = {
            support: completion_defect_row(
                quotient,
                mprime,
                support,
                completion_defect_depths[support],
            )
            for support in range(2, 6)
        }
        universal_rows = {
            support: universal_completion_row(quotient, mprime, support)
            for support in range(6, 10)
        }
        common_premium = sum(
            full_shadow_deficits[support]
            * universal_rows[support]["incidence_cap"]
            for support in universal_rows
        )
        structured_premium = common_premium + sum(
            full_shadow_deficits[support] * structured_caps[support]
            for support in structured_caps
        )
        defect_premium = common_premium + sum(
            full_shadow_deficits[support]
            * defect_rows[support]["active_cap"]
            for support in defect_rows
        )
        if defect_premium >= structured_premium:
            active_caps = {
                **{
                    support: defect_rows[support]["active_cap"]
                    for support in defect_rows
                },
                **{
                    support: universal_rows[support]["incidence_cap"]
                    for support in universal_rows
                },
            }
        else:
            active_caps = {
                **structured_caps,
                **{
                    support: universal_rows[support]["incidence_cap"]
                    for support in universal_rows
                },
            }
        payment = refined_payment_row(
            kprime,
            refined_record_cap,
            55,
            active_caps,
            full_shadow_deficits,
        )
        payment["structured_sparse_premium"] = structured_premium
        payment["completion_defect_sparse_premium"] = defect_premium
        full_deficit_payment_rows[str(kprime)] = payment
    cross_support_payment_rows = {
        str(kprime): cross_support_payment_row(kprime, refined_record_cap)
        for kprime in (42, 43)
    }
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
    two_step_endpoint = 18101
    two_step_wall = 18102
    two_step_endpoint_optimum, _, _, two_step_endpoint_branches = kernel_two_step_certificate(two_step_endpoint)
    two_step_wall_optimum, _, _, _ = kernel_two_step_certificate(two_step_wall)
    two_step_endpoint_demand = kernel_demand_ceiling(two_step_endpoint)
    two_step_endpoint_capacity = scaled_fraction_floor(two_step_endpoint_optimum)
    two_step_wall_demand = kernel_demand_ceiling(two_step_wall)
    two_step_wall_capacity = scaled_fraction_floor(two_step_wall_optimum)
    multistep_endpoint = 18158
    multistep_wall = 18159
    (
        multistep_endpoint_optimum,
        _,
        _,
        multistep_endpoint_branches,
        multistep_endpoint_tight,
    ) = kernel_multistep_certificate(multistep_endpoint)
    multistep_wall_optimum, _, _, _, _ = kernel_multistep_certificate(multistep_wall)
    multistep_endpoint_demand = kernel_demand_ceiling(multistep_endpoint)
    multistep_endpoint_capacity = scaled_fraction_floor(multistep_endpoint_optimum)
    multistep_wall_demand = kernel_demand_ceiling(multistep_wall)
    multistep_wall_capacity = scaled_fraction_floor(multistep_wall_optimum)
    projective_pair_start = 18159
    projective_pair_endpoint = 377673
    projective_pair_wall = 377674
    projective_pair_start_optimum = kernel_projective_pair_certificate(projective_pair_start)[0]
    projective_pair_endpoint_optimum = kernel_projective_pair_certificate(projective_pair_endpoint)[0]
    projective_pair_wall_optimum = kernel_projective_pair_certificate(projective_pair_wall)[0]
    projective_pair_start_demand = kernel_demand_ceiling(projective_pair_start)
    projective_pair_start_capacity = scaled_fraction_floor(projective_pair_start_optimum)
    projective_pair_endpoint_demand = kernel_demand_ceiling(projective_pair_endpoint)
    projective_pair_endpoint_capacity = scaled_fraction_floor(projective_pair_endpoint_optimum)
    projective_pair_wall_demand = kernel_demand_ceiling(projective_pair_wall)
    projective_pair_wall_capacity = scaled_fraction_floor(projective_pair_wall_optimum)
    projective_basis_start = 377674
    projective_basis_endpoint = 568338
    projective_basis_wall = 568339
    projective_basis_start_optimum = kernel_projective_basis_certificate(projective_basis_start)[0]
    projective_basis_endpoint_optimum = kernel_projective_basis_certificate(projective_basis_endpoint)[0]
    projective_basis_wall_optimum = kernel_projective_basis_certificate(projective_basis_wall)[0]
    projective_basis_start_demand = kernel_demand_ceiling(projective_basis_start)
    projective_basis_start_capacity = scaled_fraction_floor(projective_basis_start_optimum)
    projective_basis_endpoint_demand = kernel_demand_ceiling(projective_basis_endpoint)
    projective_basis_endpoint_capacity = scaled_fraction_floor(projective_basis_endpoint_optimum)
    projective_basis_wall_demand = kernel_demand_ceiling(projective_basis_wall)
    projective_basis_wall_capacity = scaled_fraction_floor(projective_basis_wall_optimum)
    projective_frame_start = 568339
    projective_frame_endpoint = 796598
    projective_frame_wall = 796599
    projective_frame_start_optimum = kernel_projective_frame_certificate(projective_frame_start)[0]
    projective_frame_endpoint_optimum = kernel_projective_frame_certificate(projective_frame_endpoint)[0]
    projective_frame_wall_optimum = kernel_projective_frame_certificate(projective_frame_wall)[0]
    projective_frame_start_demand = kernel_demand_ceiling(projective_frame_start)
    projective_frame_start_capacity = scaled_fraction_floor(projective_frame_start_optimum)
    projective_frame_endpoint_demand = kernel_demand_ceiling(projective_frame_endpoint)
    projective_frame_endpoint_capacity = scaled_fraction_floor(projective_frame_endpoint_optimum)
    projective_frame_wall_demand = kernel_demand_ceiling(projective_frame_wall)
    projective_frame_wall_capacity = scaled_fraction_floor(projective_frame_wall_optimum)
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
    rank8_fence_kprime = 11
    rank8_fence_nprime = 1048576 + rank8_fence_kprime
    rank8_fence_mprime = 67472 + rank8_fence_kprime
    rank8_fence_petal = rank8_fence_mprime - 1 - 9
    rank8_fence_remainder = rank8_fence_nprime - 9 - 8 * rank8_fence_petal
    rank8_fence_slopes = 8 * rank8_fence_remainder
    rank8_fence_extensions = comb(rank8_fence_petal, 2)
    rank8_fence_marked = rank8_fence_slopes * rank8_fence_extensions
    rank8_fence_demand = rank8_weighted_demand(rank8_fence_kprime)
    uniform_corank3_complete = uniform_corank3_row(0)
    uniform_corank3_adjacent = uniform_corank3_row(1)
    uniform_corank3_endpoint = uniform_corank3_row(1048566)
    shortening_weighted_newton = shortening_weighted_newton_coefficients()
    shortening_weighted_start_gap = shortening_weighted_gap(796599)
    shortening_weighted_endpoint_gap = shortening_weighted_gap(1048576)
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
            "last_open_K_prime": weighted_last_open_k,
            "last_open_demand": weighted_last_open_demand,
            "last_open_cap": weighted_last_open_cap,
            "last_open_gap": weighted_last_open_cap - weighted_last_open_demand,
            "first_closed_K_prime": weighted_boundary_k,
            "first_closed_demand": weighted_boundary_demand,
            "first_closed_cap": weighted_boundary_cap,
            "first_closed_gap": weighted_boundary_demand - weighted_boundary_cap,
            "closed_K_prime_maximum": 1048576,
            "reopened_interval": [10, weighted_last_open_k],
            "deleted_core_size_formula": "1048576-K_prime",
            "original_row_common_core_is_residual_floor": False,
            "remaining_routes_above_boundary": [
                "FIXED_KERNEL_NINESUBSET_CHART",
                "RANK8_OWNER_FLAT_ERROR_RANK_AT_MOST_3",
            ],
            "remaining_routes_below_boundary": [
                "FIXED_KERNEL_NINESUBSET_CHART",
                "RANK9_SHARED_PAIR_CORE_PLANE",
                "RANK8_OWNER_FLAT_ERROR_RANK_AT_MOST_3",
            ],
        },
        "rank9_residual_petal_capacity_cut": {
            "common_core_minimum": 9,
            "common_core_maximum_formula": "K_prime-1",
            "petal_pair_formula": "s*(j-9)+C(s,2)",
            "capacity_formula": "floor(981105*(n_prime-j)*(m_prime+j-20)/2)",
            "worst_core_on_claimed_interval": "j=K_prime-1",
            "last_open_K_prime": residual_petal_last_open_k,
            "last_open_demand": residual_petal_last_open_demand,
            "last_open_cap": residual_petal_last_open_cap,
            "last_open_gap": residual_petal_last_open_cap - residual_petal_last_open_demand,
            "last_open_raw_cross": residual_petal_last_open_raw_cross,
            "first_closed_K_prime": residual_petal_boundary_k,
            "first_closed_demand": residual_petal_boundary_demand,
            "first_closed_cap": residual_petal_boundary_cap,
            "first_closed_gap": residual_petal_boundary_demand - residual_petal_boundary_cap,
            "first_closed_raw_cross": residual_petal_boundary_raw_cross,
            "closed_K_prime_maximum": weighted_last_open_k,
            "remaining_rank9_interval": [10, residual_petal_last_open_k],
            "combined_rank9_closed_from_Kprime": residual_petal_boundary_k,
            "original_row_common_core_used": False,
        },
        "rank9_exact_petal_partition_capacity_cut": {
            "petal_budget_offset": exact_petal_budget,
            "a_minimum": exact_petal_a,
            "a_maximum_formula": "67462+K_prime",
            "partition_formula": "r*q_j(a)+q_j(b)",
            "full_petals_formula": "1+floor(981105/a)",
            "remainder_formula": "981105 mod a",
            "quotient_blocks": [
                [14, 67472, 70078],
                [13, 70079, 75469],
                [12, 75470, 81758],
                [11, 81759, 83096],
            ],
            "convexity_endpoints": exact_petal_endpoints,
            "endpoint_gaps": exact_petal_endpoint_gaps,
            "maximizing_a": exact_petal_a,
            "maximizing_full_petals": 1 + exact_petal_budget // exact_petal_a,
            "maximizing_remainder": exact_petal_budget % exact_petal_a,
            "packed_charge_slope": exact_petal_slope,
            "packed_charge_intercept": exact_petal_intercept,
            "capacity_formula": "981105*(1048577*K_prime+34798536326)",
            "last_open_K_prime": exact_petal_last_open_k,
            "last_open_demand": exact_petal_last_open[0],
            "last_open_cap": exact_petal_last_open[1],
            "last_open_gap": exact_petal_last_open[1] - exact_petal_last_open[0],
            "last_open_raw_cross": exact_petal_last_open[2],
            "first_closed_K_prime": exact_petal_boundary_k,
            "first_closed_demand": exact_petal_boundary[0],
            "first_closed_cap": exact_petal_boundary[1],
            "first_closed_gap": exact_petal_boundary[0] - exact_petal_boundary[1],
            "first_closed_raw_cross": exact_petal_boundary[2],
            "persistence_polynomial": [1048577, 69598121229, -77044697164886],
            "persistence_shift": 15529,
            "persistence_shifted_polynomial": [1048577, 102164825695, 1256608704226512],
            "newly_closed_interval": [15529, 15634],
            "remaining_rank9_interval": [10, 15528],
            "combined_rank9_closed_from_Kprime": 15529,
        },
        "weighted_split_pencil_selected_support_cap": {
            "minimum_A": 3,
            "owner_weight_ceiling_formula": "A-1",
            "selected_line_mass_formula": "sum_p x_Lp=A",
            "line_charge_formula": "sum_p C(x_Lp,2)",
            "heavy_threshold_formula": "floor(A/2)+1",
            "clean_dominant_cap_formula": "floor((A-2)*S^2/8)",
            "balanced_cap_formula": "C(S,2)",
            "heavy_collision_cap_formula": "C(h,2)*C(A-1,2)",
            "total_cap_formula": "floor((A-2)*S^2/8)+C(S,2)+C(h,2)*C(A-1,2)",
            "clean_inequality_slack_factorization": "(d-1)*(d+s)*(s-1)",
        },
        "rank9_minimal_shortening_split_pencil_payment": {
            "residual_K_prime": 10,
            "residual_n_prime": 1048586,
            "residual_m_prime": 67482,
            "correction_space_dimension": 10,
            "selector_size": 9,
            "selector_rank": 9,
            "kernel_zero_count": 9,
            "common_core_size": 9,
            "selected_outside_mass_A": minimal_split_A,
            "petal_total_ceiling_S": minimal_split_S,
            "petal_size_ceiling": minimal_split_A - 1,
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "heavy_threshold": minimal_split_heavy_threshold,
            "heavy_count": minimal_split_heavy_count,
            "clean_dominant_cap": minimal_split_clean,
            "balanced_cap": minimal_split_balanced,
            "heavy_collision_cap": minimal_split_collision,
            "total_capacity": minimal_split_capacity,
            "weighted_demand": minimal_split_demand,
            "demand_capacity_gap": minimal_split_demand - minimal_split_capacity,
            "raw_demand_capacity_cross": minimal_split_raw_cross,
            "newly_closed_rows": [10, 10],
            "remaining_rank9_interval": [11, 15528],
        },
        "weighted_split_pencil_core_offset_cap": {
            "minimum_P": 3,
            "minimum_r": 0,
            "owner_weight_ceiling_formula": "P-1",
            "selected_line_mass_formula": "sum_p x_Lp=P",
            "line_charge_formula": "sum_p C(x_Lp,2)+rP",
            "heavy_threshold_formula": "floor(P/2)+1",
            "balanced_cross_floor_formula": "floor(P^2/4)",
            "clean_cap_formula": "max_0<=ell<=S floor(ell*((P-2)*(S-ell)/2+h*r*P))",
            "balanced_cap_formula": "floor((M+rP)*C(S,2)/M)",
            "collision_cap_formula": "C(h,2)*(C(P-1,2)+rP)",
            "clean_inequality_slack_factorization": "(d-1)*(d+s)*(s-1)",
            "K11_specializations": k11_core_rows,
        },
        "rank11_k11_circuit_split_pencil_payment": {
            "K_prime": 11,
            "n_prime": 1048587,
            "m_prime": 67483,
            "correction_dimension": 10,
            "ambient_RS_dimension": 11,
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "residual_record_floor": non_dense,
            "rank9_core_sizes": [9, 10],
            "rank9_core_caps": [row["total_cap"] for row in k11_core_rows],
            "uniform_rank9_chart_cap": k11_chart_cap,
            "global_rank9_mark_capacity": k11_global_marks,
            "high_circuit_threshold": 6,
            "minimum_high_circuit_rank9_shadows": 45,
            "high_circuit_incidence_cap": k11_high_cap,
            "low_circuit_support_ceiling": 5,
            "low_circuit_support_coalesces": True,
            "low_circuit_per_record_cap_formula": "C(m_prime-1,10)",
            "low_circuit_incidence_cap_at_record_floor": k11_low_cap,
            "total_capacity_at_record_floor": k11_total_cap,
            "required_incidence_at_record_floor": k11_demand,
            "demand_capacity_gap": k11_demand - k11_total_cap,
            "raw_demand_capacity_cross": k11_raw_cross,
            "record_coefficient_cross": k11_record_coefficient_cross,
            "newly_closed_rows": [11, 11],
            "remaining_rank9_interval": [12, 15528],
        },
        "codimension_two_quotient_line_sparse_circuit_cap": {
            "ambient_polynomial_dimension": 12,
            "correction_dimension": 10,
            "quotient_dimension": 2,
            "component_subset_size": 11,
            "support_ceiling": 5,
            "official_support_size": k12_m,
            "support_one_label_cap": 2,
            "support_label_caps": quotient_line_caps,
            "support_incidence_terms": quotient_line_terms,
            "per_record_sparse_incidence_cap": quotient_line_per_record,
            "label_cap_formula": "max(c+1, c+floor(e*(m-g)/(c-g)))",
        },
        "rank11_k12_quotient_line_circuit_payment": {
            "K_prime": 12,
            "n_prime": k12_n,
            "m_prime": k12_m,
            "correction_dimension": 10,
            "ambient_RS_dimension": 12,
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "residual_record_floor": non_dense,
            "kernel_corank_one_record_cap": k12_kernel_record_cap,
            "kernel_extension_factor": 1,
            "kernel_incidence_cap": k12_kernel_cap,
            "rank9_core_sizes": [9, 10, 11],
            "rank9_core_caps": [row["total_cap"] for row in k12_core_rows],
            "uniform_rank9_chart_cap": k12_chart_cap,
            "global_rank9_mark_capacity": k12_global_marks,
            "high_circuit_threshold": 6,
            "minimum_high_circuit_rank9_shadows": 45,
            "high_circuit_incidence_cap": k12_high_cap,
            "low_circuit_support_ceiling": 5,
            "low_circuit_per_record_cap": quotient_line_per_record,
            "low_circuit_incidence_cap_at_record_floor": k12_low_cap,
            "total_capacity_at_record_floor": k12_total_cap,
            "required_incidence_at_record_floor": k12_demand,
            "demand_capacity_gap": k12_demand - k12_total_cap,
            "raw_demand_capacity_cross": k12_raw_cross,
            "record_coefficient_cross": k12_record_coefficient_cross,
            "newly_closed_rows": [12, 12],
            "remaining_rank9_interval": [13, 15528],
        },
        "codimension_three_sparse_circuit_completion_cap": {
            "ambient_polynomial_dimension": 13,
            "correction_dimension": 10,
            "quotient_dimension": 3,
            "component_subset_size": 11,
            "support_minimum": 2,
            "support_ceiling": 5,
            "global_common_zero_count": 0,
            "completion_ceiling": 3,
            "unstructured_completion_ceiling": 2,
            "structured_carrier_ceiling": 7,
            "official_support_size": k13_m,
            "structured_carrier_cap": k13_structured_cap,
            "unstructured_support_terms": k13_unstructured_terms,
            "unstructured_completion_cap": k13_sparse_cap,
            "per_record_sparse_incidence_cap": k13_sparse_cap,
        },
        "rank11_k13_sparse_circuit_completion_payment": {
            "K_prime": 13,
            "n_prime": k13_n,
            "m_prime": k13_m,
            "correction_dimension": 10,
            "ambient_RS_dimension": 13,
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "residual_record_floor": non_dense,
            "kernel_coranks": k13_coranks,
            "kernel_record_caps": k13_kernel_record_caps,
            "kernel_extension_factors": k13_kernel_extensions,
            "kernel_incidence_terms": k13_kernel_terms,
            "kernel_incidence_cap": k13_kernel_cap,
            "rank9_core_sizes": [9, 10, 11, 12],
            "rank9_core_caps": [row["total_cap"] for row in k13_core_rows],
            "uniform_rank9_chart_cap": k13_chart_cap,
            "global_rank9_mark_capacity": k13_global_marks,
            "high_circuit_threshold": 6,
            "minimum_high_circuit_rank9_shadows": 45,
            "high_circuit_incidence_cap": k13_high_cap,
            "low_circuit_support_ceiling": 5,
            "low_circuit_per_record_cap": k13_sparse_cap,
            "low_circuit_incidence_cap_at_record_floor": k13_low_cap,
            "total_capacity_at_record_floor": k13_total_cap,
            "required_incidence_at_record_floor": k13_demand,
            "demand_capacity_gap": k13_demand - k13_total_cap,
            "raw_demand_capacity_cross": k13_raw_cross,
            "record_coefficient_cross": k13_record_coefficient_cross,
            "newly_closed_rows": [13, 13],
            "remaining_rank9_interval": [14, 15528],
        },
        "sparse_circuit_completion_dimension_ladder": {
            "correction_dimension": 10,
            "component_subset_size": 11,
            "support_range": [2, 5],
            "global_common_zero_count": 0,
            "quotient_dimension_formula": "q=K_prime-10",
            "completion_ceiling_formula": "q",
            "unstructured_completion_ceiling_formula": "q-1",
            "structured_carrier_ceiling_formula": "q+4",
            "structured_support_cap_formula": "C(q+4,c)*C(m-c,11-c)",
            "unstructured_support_cap_formula": "floor(C(m,c-1)*max_b(b*C(m-c+1-b,11-c))/c)",
            "official_K_prime_interval": [14, 21],
            "official_unstructured_maximizer_formula": "b=q-1",
            "endpoint_totals": completion_endpoint_totals,
        },
        "rank9_sparse_shadow_joint_ledger": {
            "component_subset_size": 11,
            "shadow_subset_size": 9,
            "total_shadow_count": 55,
            "high_support_minimum": 6,
            "baseline_shadow_cost": 45,
            "low_supports": [2, 3, 4, 5],
            "rank9_shadow_counts": [19, 27, 34, 40],
            "premium_weights": [26, 18, 11, 5],
            "shadow_formula": "55-C(11-c,2)",
            "joint_capacity_formula": "floor((G+R*max_a(sum_c((45-q_c)*L_a_c)))/45)",
        },
        "rank11_k14_k21_sparse_shadow_payment": {
            "closed_K_prime_interval": [14, 21],
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "residual_record_floor": non_dense,
            "rows": joint_sparse_rows,
            "minimum_record_coefficient_cross": min(
                row["record_coefficient_cross"] for row in joint_sparse_rows
            ),
            "minimum_gap_row": min(
                joint_sparse_rows,
                key=lambda row: row["demand_capacity_gap"],
            )["K_prime"],
            "newly_closed_rows": [14, 21],
            "remaining_rank9_interval": [22, 15528],
            "K22_method_wall": {
                "K_prime": 22,
                "total_capacity_at_record_floor": joint_sparse_wall["total_capacity_at_record_floor"],
                "required_incidence_at_record_floor": joint_sparse_wall["required_incidence_at_record_floor"],
                "capacity_excess": -joint_sparse_wall["demand_capacity_gap"],
            },
        },
        "weighted_split_pencil_integral_heavy_cap": {
            "K_prime": 22,
            "core_interval": [9, 21],
            "petal_mass_formula": "67494-core",
            "total_mass_formula": "1048598-core",
            "offset_formula": "core-9",
            "extreme_owner_count": 8,
            "clean_caps": {
                key: row["cap"] for key, row in k22_integral_rows.items()
            },
            "chart_caps": {
                key: row["chart"] for key, row in k22_integral_rows.items()
            },
            "light_mass_maximizers": {
                key: row["light"] for key, row in k22_integral_rows.items()
            },
            "uniform_chart_cap": k22_integral_rows[k22_integral_core]["chart"],
            "maximizing_core": int(k22_integral_core),
            "old_uniform_chart_cap": joint_sparse_wall["uniform_rank9_chart_cap"],
            "chart_saving": (
                joint_sparse_wall["uniform_rank9_chart_cap"]
                - k22_integral_rows[k22_integral_core]["chart"]
            ),
        },
        "sparse_circuit_near_saturation_carrier": {
            "correction_dimension": 10,
            "component_size": 11,
            "support_interval": [2, 4],
            "near_completion_count_formula": "q-1",
            "fallback_completion_count_formula": (
                "max_(0<=b<=q-2) b*C(m-c+1-b,11-c)"
            ),
            "carrier_size_formula": "q+2c-2",
            "vandermonde_union_formula": "q+3c-2",
            "K22": {
                "q": k22_q,
                "m": k22_m,
                "active_caps": {
                    str(support): k22_refined_caps[support]
                    for support in range(2, 5)
                },
                "old_q_minus_1_caps": {
                    str(support): completion_defect_row(
                        k22_q,
                        k22_m,
                        support,
                        0,
                    )["active_cap"]
                    for support in range(2, 5)
                },
                "premium_weights": {
                    str(support): sparse_weights_45[support]
                    for support in range(2, 5)
                },
                "weighted_premium_saving": sum(
                    sparse_weights_45[support]
                    * (
                        completion_defect_row(
                            k22_q,
                            k22_m,
                            support,
                            0,
                        )["active_cap"]
                        - k22_refined_caps[support]
                    )
                    for support in range(2, 5)
                ),
            },
        },
        "rank11_k22_integral_near_saturation_payment": {
            **k22_payment,
            "quotient_dimension": k22_q,
            "residual_record_floor": refined_record_cap,
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "uniform_corank_one_record_cap": refined_kernel_record_cap(22, 1),
            "structured_sparse_caps": {
                str(support): value
                for support, value in k22_structured_caps.items()
            },
            "refined_unstructured_sparse_caps": {
                str(support): value
                for support, value in k22_refined_caps.items()
            },
            "premium_weights": {
                str(support): value
                for support, value in sparse_weights_45.items()
            },
            "structured_sparse_premium": sum(
                sparse_weights_45[support] * k22_structured_caps[support]
                for support in sparse_weights_45
            ),
            "new_closed_prefix": [10, 22],
            "remaining_rank9_interval": [23, 15528],
        },
        "sparse_circuit_completion_defect_hierarchy": {
            "correction_dimension": 10,
            "component_size": 11,
            "depths": {
                str(support): depth
                for support, depth in completion_defect_depths.items()
            },
            "carrier_size_formula": "q+(s+1)(c-1)",
            "vandermonde_condition": "(s+2)c-s-1<=10",
            "K23": {
                "q": k23_q,
                "m": k23_m,
                "completion_maximizers": {
                    str(support): row["completion_maximizer"]
                    for support, row in k23_defect_rows.items()
                },
                "active_caps": {
                    str(support): row["active_cap"]
                    for support, row in k23_defect_rows.items()
                },
                "premium_weights": {
                    str(support): value
                    for support, value in sparse_weights_45.items()
                },
                "weighted_premium": sum(
                    sparse_weights_45[support]
                    * k23_defect_rows[support]["active_cap"]
                    for support in sparse_weights_45
                ),
            },
        },
        "rank11_k23_completion_defect_payment": {
            **k23_payment,
            "quotient_dimension": k23_q,
            "residual_record_floor": refined_record_cap,
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "core_chart_caps": {
                str(core): integral_core_offset_row(23, core)["chart"]
                for core in range(9, 23)
            },
            "structured_sparse_caps": {
                str(support): value
                for support, value in k23_structured_caps.items()
            },
            "refined_sparse_caps": {
                str(support): value
                for support, value in k23_refined_caps.items()
            },
            "completion_maximizers": {
                str(support): row["completion_maximizer"]
                for support, row in k23_defect_rows.items()
            },
            "premium_weights": {
                str(support): value
                for support, value in sparse_weights_45.items()
            },
            "structured_sparse_premium": sum(
                sparse_weights_45[support] * k23_structured_caps[support]
                for support in sparse_weights_45
            ),
            "new_closed_prefix": [10, 23],
            "remaining_rank9_interval": [24, 15528],
            "K24_method_wall": {
                "uniform_rank9_chart_cap": k24_old_payment["uniform_rank9_chart_cap"],
                "active_sparse_premium": k24_old_payment["active_sparse_premium"],
                "kernel_capacity": k24_old_payment["kernel_capacity"],
                "total_capacity": k24_old_payment["total_capacity"],
                "required_incidence": k24_old_payment["required_incidence"],
                "capacity_excess": -k24_old_payment["demand_capacity_gap"],
            },
        },
        "sparse_circuit_universal_completion_incidence_cap": {
            "correction_dimension": 10,
            "component_subset_size": 11,
            "supported_circuit_sizes": list(range(2, 10)),
            "quotient_dimension_formula": "q=K_prime-10",
            "completion_ceiling": "b<=q",
            "incidence_formula": (
                "floor(C(m,c-1)*max_(0<=b<=q)"
                "(b*C(m-c+1-b,11-c))/c)"
            ),
            "K24_example": {
                "q": 14,
                "m": 67496,
                "completion_maximizers": {
                    str(support): row["completion_maximizer"]
                    for support, row in k24_universal_rows.items()
                },
                "incidence_caps": {
                    str(support): row["incidence_cap"]
                    for support, row in k24_universal_rows.items()
                },
            },
        },
        "rank9_full_circuit_deficit_ledger": {
            "component_subset_size": 11,
            "shadow_subset_size": 9,
            "total_shadow_count": 55,
            "circuit_supports": list(range(2, 12)),
            "rank9_shadow_counts": [
                55 - comb(11 - support, 2)
                for support in range(2, 12)
            ],
            "deficit_weights": [
                comb(11 - support, 2)
                for support in range(2, 12)
            ],
            "joint_capacity_formula": (
                "floor((G+R*max_a(sum_(c=2)^9"
                "(C(11-c,2)*L_a_c)))/55)"
            ),
        },
        "rank11_k24_k40_full_deficit_shadow_payment": {
            "closed_K_prime_interval": [24, 40],
            "new_closed_prefix": [10, 40],
            "first_method_wall": 41,
            "residual_record_floor": refined_record_cap,
            "component_density_numerator": 990810934,
            "component_density_denominator": 10**9,
            "shadow_baseline": 55,
            "deficit_weights": {
                str(support): weight
                for support, weight in full_shadow_deficits.items()
            },
            "rows": {
                key: {
                    "maximizing_core": row["maximizing_core"],
                    "uniform_rank9_chart_cap": row["uniform_rank9_chart_cap"],
                    "active_sparse_premium": row["active_sparse_premium"],
                    "demand_capacity_gap": row["demand_capacity_gap"],
                }
                for key, row in full_deficit_payment_rows.items()
                if int(key) <= 41
            },
            "K24_endpoint": {
                key: full_deficit_payment_rows["24"][key]
                for key in (
                    "kernel_capacity",
                    "full_rank_capacity",
                    "total_capacity",
                    "required_incidence",
                )
            },
            "K40_endpoint": {
                key: full_deficit_payment_rows["40"][key]
                for key in (
                    "kernel_capacity",
                    "full_rank_capacity",
                    "total_capacity",
                    "required_incidence",
                    "record_coefficient_cross",
                    "floor_record_raw_cross",
                )
            },
            "K41_method_wall": {
                "kernel_capacity": full_deficit_payment_rows["41"]["kernel_capacity"],
                "full_rank_capacity": full_deficit_payment_rows["41"]["full_rank_capacity"],
                "total_capacity": full_deficit_payment_rows["41"]["total_capacity"],
                "required_incidence": full_deficit_payment_rows["41"]["required_incidence"],
                "capacity_excess": -full_deficit_payment_rows["41"]["demand_capacity_gap"],
                "floor_record_raw_cross": full_deficit_payment_rows["41"]["floor_record_raw_cross"],
            },
            "remaining_rank9_interval": [41, 15528],
        },
        "rank_stratified_isolated_incidence_cap": {
            "correction_dimension": 10,
            "tuple_size": 11,
            "dense_locator_degree": 18,
            "retained_slopes_are_distinct": True,
            "retained_slopes_avoid_locator_roots": True,
            "old_generic_isolated_cap_per_tuple": 198,
            "new_record_isolated_cap_per_tuple": 1,
            "component_lower_bound": "N*C(m_prime,11)-C(n_prime,11)",
        },
        "rank11_k41_sharp_isolated_payment": {
            "closed_row": 41,
            "new_closed_prefix": [10, 41],
            "first_method_wall": 42,
            "residual_record_floor": refined_record_cap,
            "n": full_deficit_payment_rows["41"]["n_prime"],
            "m": full_deficit_payment_rows["41"]["m_prime"],
            "q": 31,
            "isolated_cap_per_eleven_set": 1,
            "isolated_global_cap": comb(1048617, 11),
            "max_core": full_deficit_payment_rows["41"]["maximizing_core"],
            "chart": full_deficit_payment_rows["41"]["uniform_rank9_chart_cap"],
            "kernel_capacity": full_deficit_payment_rows["41"]["kernel_capacity"],
            "rank_nine_marks": full_deficit_payment_rows["41"]["global_rank9_mark_capacity"],
            "completion_premium": full_deficit_payment_rows["41"]["active_sparse_premium"],
            "full_rank_capacity": full_deficit_payment_rows["41"]["full_rank_capacity"],
            "total_capacity": full_deficit_payment_rows["41"]["total_capacity"],
            "required_component_incidence": (
                refined_record_cap * comb(67513, 11) - comb(1048617, 11)
            ),
            "gap": (
                refined_record_cap * comb(67513, 11)
                - comb(1048617, 11)
                - full_deficit_payment_rows["41"]["total_capacity"]
            ),
            "record_coefficient_cross": (
                55 * comb(67513, 11)
                - full_deficit_payment_rows["41"]["active_sparse_premium"]
            ),
            "floor_record_raw_cross": (
                refined_record_cap
                * (
                    55 * comb(67513, 11)
                    - full_deficit_payment_rows["41"]["active_sparse_premium"]
                )
                - 55 * comb(1048617, 11)
                - 55 * full_deficit_payment_rows["41"]["kernel_capacity"]
                - full_deficit_payment_rows["41"]["global_rank9_mark_capacity"]
            ),
            "K42_capacity_excess": (
                full_deficit_payment_rows["42"]["total_capacity"]
                - refined_record_cap * comb(67514, 11)
                + comb(1048618, 11)
            ),
            "remaining_rank9_interval": [42, 15528],
        },
        "sparse_circuit_cross_support_defect_carrier": {
            "correction_dimension": 10,
            "component_size": 11,
            "source_support_symbol": "c",
            "target_support_symbol": "d",
            "support_range": [2, 9],
            "defect_range": "0<=s<=q",
            "completion_count": "q-s",
            "carrier_size": "q+c-1+s(d-1)",
            "vandermonde_condition": "c+(s+1)d-s-1<=10",
            "incidence_cap": "C(q+c-1+s(d-1),d)C(m-d,11-d)",
            "support5_target_supports": {
                str(defect): [
                    target
                    for target in range(2, 10)
                    if 5 + (defect + 1) * target - defect - 1 <= 10
                ]
                for defect in range(5)
            },
            "fallback_completion_ceiling": "q-5",
        },
        "rank11_k42_cross_support_defect_payment": {
            "closed_row": 42,
            "new_closed_prefix": [10, 42],
            "first_method_wall": 43,
            "residual_record_floor": refined_record_cap,
            "deficit_weights": {
                str(support): comb(11 - support, 2)
                for support in range(2, 10)
            },
            "source_support": 5,
            "carrier_defects": list(range(5)),
            "branch_partition": (
                "s=q-max_A b_A for s=0..4, otherwise max_A b_A<=q-5"
            ),
            "fallback_completion_ceiling": "q-5",
            **cross_support_payment_rows["42"],
            "K43_method_wall": {
                key: value
                for key, value in cross_support_payment_rows["43"].items()
                if key
                not in {
                    "isolated_global_cap",
                    "uncoupled_completion_premium",
                    "premium_saving",
                    "gap",
                }
            }
            | {
                "capacity_excess": -cross_support_payment_rows["43"]["gap"]
            },
            "remaining_rank9_interval": [43, 15528],
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
        "kernel_two_step_nine_shadow_hierarchy": {
            "support_offset": 67472,
            "corank_minimum": 3,
            "corank_maximum": 9,
            "couplings": two_step_hierarchy_rows(),
            "same_rank_extension_formula": "C(K_prime-d-9,2)",
            "inequality_formula": "C(d+2,2)*C(67472+d,2)*I_d/C(K_prime-d-9,2) <= C(11-d,2)*I_(d-2)",
        },
        "kernel_two_step_nine_shadow_capacity_cut": {
            "previous_closed_K_prime": rank8_shadow_endpoint,
            "replay_K_prime_minimum": rank8_shadow_wall,
            "closed_K_prime_maximum": two_step_endpoint,
            "first_open_K_prime": two_step_wall,
            "replay_rows": 494,
            "endpoint_branch_pattern": two_step_endpoint_branches,
            "active_individual_caps": [1],
            "active_shared_resources": ["full_containment_nine_shadow"],
            "slack_shared_resources": ["rank_preserving_nine_shadow"],
            "active_hierarchy_coranks": list(range(3, 10)),
            "positive_coranks": list(range(1, 10)),
            "endpoint_optimum_numerator": two_step_endpoint_optimum.numerator,
            "endpoint_optimum_denominator": two_step_endpoint_optimum.denominator,
            "endpoint_demand": two_step_endpoint_demand,
            "endpoint_capacity": two_step_endpoint_capacity,
            "endpoint_gap": two_step_endpoint_demand - two_step_endpoint_capacity,
            "wall_optimum_numerator": two_step_wall_optimum.numerator,
            "wall_optimum_denominator": two_step_wall_optimum.denominator,
            "wall_demand": two_step_wall_demand,
            "wall_capacity": two_step_wall_capacity,
            "wall_excess": two_step_wall_capacity - two_step_wall_demand,
            "capacity_formula": "exact full-containment plus two-step hierarchy LP with individual ambient/record caps",
        },
        "kernel_multistep_shadow_hierarchy": {
            "support_offset": 67472,
            "corank_minimum": 3,
            "corank_maximum": 9,
            "step_minimum": 2,
            "coupling_count": 28,
            "couplings": multistep_hierarchy_rows(),
            "triple_couplings": [row[1:] for row in multistep_hierarchy_rows() if row[0] == 3],
            "spanning_shadow_formula": "C(d+2,t)",
            "same_rank_extension_formula": "C(K_prime-d-11+t,t)",
            "rank_raising_extension_formula": "C(67472+d,t)",
            "target_multiplicity_formula": "C(9-d+t,t)",
            "inequality_formula": "C(d+2,t)*C(67472+d,t)*I_d/C(K_prime-d-11+t,t) <= C(9-d+t,t)*I_(d-t)",
        },
        "kernel_three_step_shadow_capacity_cut": {
            "previous_closed_K_prime": two_step_endpoint,
            "replay_K_prime_minimum": two_step_wall,
            "closed_K_prime_maximum": multistep_endpoint,
            "first_open_K_prime": multistep_wall,
            "replay_rows": 58,
            "endpoint_branch_pattern": multistep_endpoint_branches,
            "active_individual_caps": [1],
            "active_shared_resources": ["full_containment_nine_shadow"],
            "slack_shared_resources": ["rank_preserving_nine_shadow"],
            "positive_coranks": list(range(1, 10)),
            "dual_tree": MULTISTEP_DUAL_TREE,
            "tight_hierarchy_rows": multistep_endpoint_tight,
            "endpoint_optimum_numerator": multistep_endpoint_optimum.numerator,
            "endpoint_optimum_denominator": multistep_endpoint_optimum.denominator,
            "endpoint_demand": multistep_endpoint_demand,
            "endpoint_capacity": multistep_endpoint_capacity,
            "endpoint_gap": multistep_endpoint_demand - multistep_endpoint_capacity,
            "wall_optimum_numerator": multistep_wall_optimum.numerator,
            "wall_optimum_denominator": multistep_wall_optimum.denominator,
            "wall_demand": multistep_wall_demand,
            "wall_capacity": multistep_wall_capacity,
            "wall_excess": multistep_wall_capacity - multistep_wall_demand,
            "capacity_formula": "exact full-containment plus all-step hierarchy LP with individual ambient/record caps",
        },
        "kernel_corank1_projective_pair_cap": {
            "domain_size": 1048577,
            "code_dimension": 1,
            "support_size": 67473,
            "explanation_dimension": 1,
            "zero_normal_upper_bound": 0,
            "minimum_projective_classes": 2,
            "minimum_independent_ordered_pairs_per_record": 134944,
            "coordinate_ordered_pair_resource": 1099512676352,
            "record_cap": PROJECTIVE_PAIR_RECORD_CAP,
            "division_remainder": 29760,
            "previous_transversality_record_cap": 16295594,
            "record_cap_improvement": 8147676,
            "capacity_formula": "floor(n*(n-1)/(2*(m-1)))",
        },
        "kernel_projective_pair_capacity_cut": {
            "previous_closed_K_prime": multistep_endpoint,
            "replay_K_prime_minimum": projective_pair_start,
            "closed_K_prime_maximum": projective_pair_endpoint,
            "first_open_K_prime": projective_pair_wall,
            "checked_rows_including_wall": 359516,
            "active_individual_caps": [1, 2],
            "active_individual_cap_branches": ["ambient", "ambient"],
            "active_shared_resources": [],
            "slack_shared_resources": ["rank_preserving_nine_shadow", "full_containment_nine_shadow"],
            "positive_coranks": list(range(1, 10)),
            "dual_tree": PROJECTIVE_PAIR_DUAL_TREE,
            "tight_hierarchy_rows": PROJECTIVE_PAIR_TIGHT_ROWS,
            "replay_start_optimum_numerator": projective_pair_start_optimum.numerator,
            "replay_start_optimum_denominator": projective_pair_start_optimum.denominator,
            "replay_start_demand": projective_pair_start_demand,
            "replay_start_capacity": projective_pair_start_capacity,
            "replay_start_gap": projective_pair_start_demand - projective_pair_start_capacity,
            "endpoint_optimum_numerator": projective_pair_endpoint_optimum.numerator,
            "endpoint_optimum_denominator": projective_pair_endpoint_optimum.denominator,
            "endpoint_demand": projective_pair_endpoint_demand,
            "endpoint_capacity": projective_pair_endpoint_capacity,
            "endpoint_gap": projective_pair_endpoint_demand - projective_pair_endpoint_capacity,
            "wall_optimum_numerator": projective_pair_wall_optimum.numerator,
            "wall_optimum_denominator": projective_pair_wall_optimum.denominator,
            "wall_demand": projective_pair_wall_demand,
            "wall_capacity": projective_pair_wall_capacity,
            "wall_excess": projective_pair_wall_capacity - projective_pair_wall_demand,
            "source_replay_script_sha256": "0ae83004c6a711d8b2d1917fb6ebe60c1c110bfac47cad88cc9f950478a515d0",
            "source_replay_result_sha256": "5de596473bb713fd8d66bccd977eee62a841b7251aa9363288b13293063fd4c4",
            "source_replay_chunks": 64,
            "source_replay_worker_timeout_seconds": 60,
            "source_replay_worker_memory_mb": 256,
            "source_replay_peak_mb": 57,
            "capacity_formula": "two active individual caps plus exact all-step hierarchy tree",
        },
        "kernel_corank2_projective_basis_cap": {
            "domain_size": 1048578,
            "code_dimension": 2,
            "support_size": 67474,
            "explanation_dimension": 2,
            "support_excess": 67472,
            "normal_space_dimension": 3,
            "zero_normal_upper_bound": 0,
            "minimum_normals_outside_projective_class": 67473,
            "maximum_projective_class_size": 1,
            "minimum_projective_points": 67474,
            "noncollinear": True,
            "maximum_collinear_unordered_triples": 51194051445096,
            "minimum_independent_ordered_triples_per_record": 13657614768,
            "coordinate_ordered_triple_resource": 1152924803143827456,
            "record_cap": PROJECTIVE_BASIS_RECORD_CAP,
            "division_remainder": 2935655472,
            "previous_transversality_record_cap": 253241283,
            "previous_division_remainder": 389629290,
            "record_cap_improvement": 168825020,
            "capacity_formula": "floor(n*(n-1)*(n-2)/(3*(m-1)*(m-2)))",
        },
        "matroid_rank3_bounded_parallel_basis_floor": {
            "status": "proved",
            "rank": 3,
            "loopless": True,
            "basis_floor": "2*b(M)>=(m-1)*(m-1-a)",
            "smallest_class_contraction_floor": "b(M/e)>=c*(m-2*c)>=m-2",
            "induction_slack": "a-1",
            "sharp_when": "a divides m-1 and m-1>=2a",
        },
        "kernel_corank2_uniform_projective_basis_cap": {
            "status": "proved",
            "t_minimum": 0,
            "t_maximum": 1048566,
            "parallel_class_ceiling": "t+1",
            "ordered_basis_floor": "3*67472*(67473+t)",
            "record_cap_formula": "floor((1048576+t)*(1048577+t)*(1048578+t)/(3*67472*(67473+t)))",
            "ratio_step_sign": "2*t+3*67472+3-1048576",
            "turn_left": 423078,
            "turn_right": 423079,
            "complete_cap": 84416263,
            "adjacent_cap": 84415253,
            "far_endpoint_cap": 40828171,
            "uniform_record_cap": PROJECTIVE_BASIS_RECORD_CAP,
        },
        "kernel_corank2_projective_capacity_cut": {
            "status": "proved",
            "previous_closed_K_prime": projective_pair_endpoint,
            "replay_K_prime_minimum": projective_basis_start,
            "closed_K_prime_maximum": projective_basis_endpoint,
            "first_open_K_prime": projective_basis_wall,
            "checked_rows_including_wall": 190666,
            "active_individual_caps": [1, 2],
            "active_individual_cap_branches": ["ambient", "ambient"],
            "active_shared_resources": [],
            "slack_shared_resources": ["rank_preserving_nine_shadow", "full_containment_nine_shadow"],
            "positive_coranks": list(range(1, 10)),
            "dual_tree": PROJECTIVE_BASIS_DUAL_TREE,
            "tight_hierarchy_rows": PROJECTIVE_BASIS_TIGHT_ROWS,
            "replay_start_optimum_numerator": projective_basis_start_optimum.numerator,
            "replay_start_optimum_denominator": projective_basis_start_optimum.denominator,
            "replay_start_demand": projective_basis_start_demand,
            "replay_start_capacity": projective_basis_start_capacity,
            "replay_start_gap": projective_basis_start_demand - projective_basis_start_capacity,
            "endpoint_optimum_numerator": projective_basis_endpoint_optimum.numerator,
            "endpoint_optimum_denominator": projective_basis_endpoint_optimum.denominator,
            "endpoint_demand": projective_basis_endpoint_demand,
            "endpoint_capacity": projective_basis_endpoint_capacity,
            "endpoint_gap": projective_basis_endpoint_demand - projective_basis_endpoint_capacity,
            "wall_optimum_numerator": projective_basis_wall_optimum.numerator,
            "wall_optimum_denominator": projective_basis_wall_optimum.denominator,
            "wall_demand": projective_basis_wall_demand,
            "wall_capacity": projective_basis_wall_capacity,
            "wall_excess": projective_basis_wall_capacity - projective_basis_wall_demand,
            "source_replay_script_sha256": "f69404cfc33d035cee8214cf6571749b29f2e5eb18a10daf8abb758acd672c62",
            "source_replay_result_sha256": "cce4f82fc9f21570ef15a97da212a171ca3db3af7ec24df23ef9c477cf6e176c",
            "source_replay_chunks": 64,
            "source_replay_worker_timeout_seconds": 60,
            "source_replay_worker_memory_mb": 256,
            "source_replay_peak_mb": 57,
            "capacity_formula": "two strengthened individual caps plus exact all-step hierarchy tree",
        },
        "kernel_corank3_projective_basis_cap": {
            "domain_size": 1048579,
            "code_dimension": 3,
            "support_size": 67475,
            "explanation_dimension": 3,
            "support_excess": 67472,
            "normal_space_dimension": 4,
            "zero_normal_upper_bound": 0,
            "minimum_normals_outside_projective_class": 67474,
            "maximum_projective_class_size": 1,
            "minimum_normals_outside_projective_line": 67473,
            "maximum_projective_line_size": 2,
            "minimum_projective_points": 67475,
            "spans_projective_space": True,
            "maximum_coplanar_unordered_quadruples": 863566856801601876,
            "minimum_independent_ordered_quadruples_per_record": 1228711865141376,
            "coordinate_ordered_quadruple_resource": 1208932737155751449985024,
            "record_cap": PROJECTIVE_FRAME_RECORD_CAP,
            "division_remainder": 1056607358217600,
            "previous_transversality_record_cap": 3935435218,
            "previous_division_remainder": 191426448255924,
            "record_cap_improvement": 2951532669,
            "capacity_formula": "floor((n)_fall_4/(4*(m-1)*(m-2)*(m-3)))",
        },
        "matroid_rank4_bounded_point_line_basis_floor": {
            "status": "proved",
            "rank": 4,
            "loopless": True,
            "parallel_class_ceiling": "a",
            "rank2_flat_ceiling": "a+1",
            "smallest_class_ceiling": "h_a(r)=min(floor((a+1)/2),floor((a+r)/4))",
            "coloop_floor_times_6": "C_a(r)=(a+r-1)*(r-1)*(r-2)",
            "contraction_increment_times_6": "L_a(r)=3*(a+r-h_a(r)-1)*(r-2)",
            "recurrence": "Q_a(3)=6; Q_a(r)=min(C_a(r),Q_a(r-1)+L_a(r))",
            "basis_floor": "6*b(M)>=Q_a(r)",
            "reset_difference_sign": "3*h_a(x)-a-2",
        },
        "kernel_corank3_uniform_projective_basis_cap": {
            "status": "proved",
            "rank_gap": 67474,
            "t_minimum": 0,
            "t_maximum": 1048566,
            "parallel_class_ceiling": "t+1",
            "rank2_flat_ceiling": "t+2",
            "basis_floor_times_6": "Q_(t+1)(67474)",
            "ordered_basis_floor": "4*Q_(t+1)(67474)",
            "record_cap_formula": "floor((1048576+t)*(1048577+t)*(1048578+t)*(1048579+t)/(4*Q_(t+1)(67474)))",
            "complete_row": uniform_corank3_complete,
            "adjacent_row": uniform_corank3_adjacent,
            "first_nontrivial_row": uniform_corank3_row(2),
            "middle_row": uniform_corank3_row(1048566 // 2),
            "official_endpoint": uniform_corank3_endpoint,
            "uniform_record_cap": 983902549,
            "checked_rows": 1048567,
            "first_maximizer": 0,
            "first_excess": None,
            "recurrence_checks": 9440,
            "residue_checks": 2240,
            "source_scan_script_sha256": "0b00e75ab46b74b152a8e8d3cd5302dca4f02ee709259d8ec4eed3e7878efcf5",
            "source_scan_result_sha256": "c9f43ce8d0ef2d81a8fd37b23fb71800f1f04aa90b252e9163c2850f0c869042",
            "source_scan_worker_timeout_seconds": 60,
            "source_scan_worker_memory_mb": 512,
            "source_scan_max_containers": 1,
        },
        "kernel_corank3_projective_capacity_cut": {
            "status": "proved",
            "premises": [],
            "previous_closed_K_prime": projective_basis_endpoint,
            "replay_K_prime_minimum": projective_frame_start,
            "closed_K_prime_maximum": projective_frame_endpoint,
            "first_open_K_prime": projective_frame_wall,
            "checked_rows_including_wall": 228261,
            "active_individual_caps": [1, 2, 3],
            "active_individual_cap_branches": ["ambient", "ambient", "ambient"],
            "active_shared_resources": [],
            "slack_shared_resources": ["rank_preserving_nine_shadow", "full_containment_nine_shadow"],
            "positive_coranks": list(range(1, 10)),
            "dual_forest": PROJECTIVE_FRAME_DUAL_FOREST,
            "tight_hierarchy_rows": PROJECTIVE_FRAME_TIGHT_ROWS,
            "replay_start_optimum_numerator": projective_frame_start_optimum.numerator,
            "replay_start_optimum_denominator": projective_frame_start_optimum.denominator,
            "replay_start_demand": projective_frame_start_demand,
            "replay_start_capacity": projective_frame_start_capacity,
            "replay_start_gap": projective_frame_start_demand - projective_frame_start_capacity,
            "endpoint_optimum_numerator": projective_frame_endpoint_optimum.numerator,
            "endpoint_optimum_denominator": projective_frame_endpoint_optimum.denominator,
            "endpoint_demand": projective_frame_endpoint_demand,
            "endpoint_capacity": projective_frame_endpoint_capacity,
            "endpoint_gap": projective_frame_endpoint_demand - projective_frame_endpoint_capacity,
            "wall_optimum_numerator": projective_frame_wall_optimum.numerator,
            "wall_optimum_denominator": projective_frame_wall_optimum.denominator,
            "wall_demand": projective_frame_wall_demand,
            "wall_capacity": projective_frame_wall_capacity,
            "wall_excess": projective_frame_wall_capacity - projective_frame_wall_demand,
            "source_replay_script_sha256": "24a6072a384b07ce56729d6e390694d78df90975034cf32e0ca20dab754f73ba",
            "source_replay_result_sha256": "ae609e8b948f0cd4df77448f91b102385ec4334e7bd2260aa12ec8ab38d27daa",
            "source_replay_chunks": 64,
            "source_replay_worker_timeout_seconds": 60,
            "source_replay_worker_memory_mb": 256,
            "source_replay_peak_mb": 59,
            "capacity_formula": "three strengthened individual caps plus exact all-step hierarchy forest",
        },
        "kernel_projective_paving_scope_repair": {
            "status": "proved",
            "complete_chart_caps": [
                8147918,
                84416263,
                983902549,
                12232092309,
                158406193634,
                2109949210211,
                28689347099870,
                396280526311830,
                5542092977392141,
            ],
            "uniform_corank1_cap": 8147918,
            "uniform_corank2_cap": 84416263,
            "uniform_corank2_cap_proved": True,
            "uniform_corank3_cap": 983902549,
            "uniform_corank3_cap_proved": True,
            "integer_gap_formula": "floor(max(P_d,F_d(1),F_d(K_prime-10)))",
            "audit_K_prime": 377674,
            "audit_corank2_cap": 253238254,
            "audit_corank3_cap": 3935391907,
            "unconditional_kernel_closed_through_K_prime": 796598,
        },
        "kernel_shortening_weighted_extension_cap": {
            "status": "proved",
            "K_prime_minimum": 796599,
            "K_prime_maximum": 1048576,
            "complete_record_caps": SHORTENING_WEIGHTED_COMPLETE_CAPS,
            "uniform_coranks": [1, 2, 3],
            "noncomplete_coranks": [4, 5, 6, 7, 8, 9],
            "weighted_extension_formula": "M_d(t)*C(K_prime-10-t,d+1)",
            "noncomplete_maximizer": "t=1",
            "successive_ratio_formula": "((1048576+d+t+1)*(67472+d+t)*(K_prime-10-t-d-1))/((1048576+t)*(67472+d+t+1)*(K_prime-10-t))",
            "all_basis_decoration_divisor": "d+2",
            "t1_F_fractions": {
                str(dimension): [value.numerator, value.denominator]
                for dimension, value in SHORTENING_WEIGHTED_F1.items()
            },
            "dominance_checks": 6,
            "ratio_checks": 54,
        },
        "kernel_shortening_weighted_capacity_cut": {
            "status": "proved",
            "premises": [],
            "previous_closed_K_prime": 796598,
            "replay_K_prime_minimum": 796599,
            "closed_K_prime_maximum": 1048576,
            "polynomial_degree": 11,
            "positive_newton_coefficients": len(shortening_weighted_newton),
            "positive_shifted_power_coefficients": 12,
            "newton_vector_sha256": fraction_vector_digest(shortening_weighted_newton),
            "shifted_power_vector_sha256": "85f67eade03100e7fc6f3ef0443a3a787f1133427a0f9d4030d638eca9080082",
            "start_gap": [shortening_weighted_start_gap.numerator, shortening_weighted_start_gap.denominator],
            "endpoint_gap": [shortening_weighted_endpoint_gap.numerator, shortening_weighted_endpoint_gap.denominator],
            "capacity_formula": "sum_d C(1048576+K_prime,10-d)*U_d(K_prime)/(d+2)",
            "positivity_formula": "G(796599+s)=sum_j C(s,j)*Delta^j G(796599)",
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
        "rank8_fixed_chart_local_cap_fence": {
            "residual_K_prime": rank8_fence_kprime,
            "residual_n_prime": rank8_fence_nprime,
            "residual_m_prime": rank8_fence_mprime,
            "selector_size": 9,
            "selector_rank": 8,
            "kernel_dimension": 2,
            "owner_count": 8,
            "petal_size": rank8_fence_petal,
            "remainder_size": rank8_fence_remainder,
            "rich_slope_count": rank8_fence_slopes,
            "selector_record_floor": 2578110,
            "component_extensions_per_record": rank8_fence_extensions,
            "marked_component_weight": rank8_fence_marked,
            "weighted_selector_demand": rank8_fence_demand,
            "forbidden_slope_count": 18,
            "maximum_greedy_forbidden_values": 64 * (rank8_fence_remainder - 1) + 8 * 18,
            "base_prime": 2130706433,
            "error_affine_rank_ceiling": 2,
            "lifted_owner_core_deficiency": 1,
        },
        "rank8_minimal_shortening_exclusion": {
            "residual_K_prime": 10,
            "ambient_RS_dimension": 10,
            "correction_space_dimension": 10,
            "selector_size": 9,
            "selector_rank": 9,
            "excluded_selector_rank": 8,
            "interpolation_degree_ceiling": 8,
            "first_uncovered_K_prime": 11,
        },
        "rank8_codimension_one_circuit_shadow_census": {
            "residual_K_prime": 11,
            "ambient_RS_dimension": 11,
            "correction_space_dimension": 10,
            "selector_size": 9,
            "selector_rank": 8,
            "selector_kernel_dimension": 2,
            "empty_global_common_support": True,
            "fixed_chart_record_floor": 2578110,
            "minimum_distinct_slopes_for_loop_exclusion": 2,
            "circuit_sizes": list(range(2, 10)),
            "rank8_shadow_counts": [comb(11 - c, 2) for c in range(2, 10)],
            "rank9_shadow_counts": [55 - comb(11 - c, 2) for c in range(2, 10)],
            "rank10_basis_counts": list(range(2, 10)),
            "locator_ideal_dimensions": [11 - c for c in range(2, 10)],
            "eight_petal_circuit_size": 9,
        },
        "claims": {
            "local_theorem_packet": True,
            "incidence_is_record_count": False,
            "cross_cell_census": False,
            "fixed_chart_output_suffices_for_payment": False,
            "full_rank_star_owner_is_record_intrinsic": True,
            "rank9_fixed_target_eliminated_from_Kprime": 15529,
            "rank9_minimal_shortening_closed_K_prime": 10,
            "rank9_k11_circuit_split_pencil_closed_K_prime": 11,
            "rank9_k12_quotient_line_circuit_closed_K_prime": 12,
            "rank9_k13_sparse_circuit_completion_closed_K_prime": 13,
            "rank9_k14_k21_sparse_shadow_closed_K_prime": 21,
            "rank9_k22_integral_near_saturation_closed_K_prime": 22,
            "rank9_k23_completion_defect_closed_K_prime": 23,
            "rank9_k24_k40_full_deficit_shadow_closed_K_prime": 40,
            "rank9_k41_sharp_isolated_closed_K_prime": 41,
            "rank9_k42_cross_support_defect_closed_K_prime": 42,
            "rank9_low_shortening_reopened": True,
            "rank9_remaining_interval": [43, 15528],
            "kernel_dominant_lane_closed_through_Kprime": 1048576,
            "kernel_fixed_lane_closed": True,
            "kernel_uniform_corank2_cap_proved": True,
            "kernel_uniform_corank3_cap_proved": True,
            "rank8_owner_flat_closed_from_Kprime": 37996,
            "rank8_dense_owner_terminal_from_Kprime": 22526,
            "rank8_fixed_chart_output_suffices_for_payment": False,
            "rank8_minimal_shortening_closed_K_prime": 10,
            "rank8_Kprime11_fixed_circuit_census_proved": True,
            "chronology_owner": False,
            "rank11_paid": False,
            "active_v4_ledger_movement": 0,
            "KoalaBear_closed": False,
        },
    }


def validate(value: object, wanted: dict[str, Any] | None = None) -> dict[str, int]:
    require(isinstance(value, dict), "manifest object")
    if wanted is None:
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
    residual_petal = value["rank9_residual_petal_capacity_cut"]
    exact_petal = value["rank9_exact_petal_partition_capacity_cut"]
    split_pencil_cap = value["weighted_split_pencil_selected_support_cap"]
    minimal_split_payment = value["rank9_minimal_shortening_split_pencil_payment"]
    offset_split_cap = value["weighted_split_pencil_core_offset_cap"]
    k11_payment = value["rank11_k11_circuit_split_pencil_payment"]
    quotient_line_cap = value["codimension_two_quotient_line_sparse_circuit_cap"]
    k12_payment = value["rank11_k12_quotient_line_circuit_payment"]
    completion_cap = value["codimension_three_sparse_circuit_completion_cap"]
    k13_payment = value["rank11_k13_sparse_circuit_completion_payment"]
    completion_ladder = value["sparse_circuit_completion_dimension_ladder"]
    joint_shadow_ledger = value["rank9_sparse_shadow_joint_ledger"]
    joint_sparse_payment = value["rank11_k14_k21_sparse_shadow_payment"]
    integral_heavy_cap = value["weighted_split_pencil_integral_heavy_cap"]
    near_saturation = value["sparse_circuit_near_saturation_carrier"]
    k22_refined_payment = value["rank11_k22_integral_near_saturation_payment"]
    defect_hierarchy = value["sparse_circuit_completion_defect_hierarchy"]
    k23_refined_payment = value["rank11_k23_completion_defect_payment"]
    universal_completion = value["sparse_circuit_universal_completion_incidence_cap"]
    full_deficit_ledger = value["rank9_full_circuit_deficit_ledger"]
    full_deficit_payment = value["rank11_k24_k40_full_deficit_shadow_payment"]
    sharp_isolated = value["rank_stratified_isolated_incidence_cap"]
    k41_sharp = value["rank11_k41_sharp_isolated_payment"]
    cross_support_carrier = value["sparse_circuit_cross_support_defect_carrier"]
    k42_cross_support = value["rank11_k42_cross_support_defect_payment"]
    require(
        weighted_elimination["first_closed_demand"]
        > weighted_elimination["first_closed_cap"],
        "weighted target gap",
    )
    require(
        value["claims"]["rank9_fixed_target_eliminated_from_Kprime"] == 15529,
        "rank-nine exact-petal boundary",
    )
    require(value["claims"]["rank9_low_shortening_reopened"] is True, "rank-nine reopened interval")
    require(value["claims"]["rank9_remaining_interval"] == [43, 15528], "rank-nine remaining interval")
    require(residual_petal["last_open_raw_cross"] < 0, "residual-petal last raw cross")
    require(residual_petal["first_closed_raw_cross"] > 0, "residual-petal first raw cross")
    for kprime in range(10, 20618):
        nprime, mprime = 1048576 + kprime, 67472 + kprime
        numerator = (
            495405467
            * 274980728111260126
            * comb(mprime, 9)
            * comb(mprime - 9, 2)
        )
        denominator = 10**9 * comb(nprime, 9)
        j = kprime - 1
        cap_twice = 981105 * (nprime - j) * (mprime + j - 20)
        raw_cross = 2 * numerator - cap_twice * denominator
        require((raw_cross > 0) == (kprime >= 15635), f"residual-petal crossing K'={kprime}")
    require(exact_petal["maximizing_a"] == 67472, "exact-petal maximizing ceiling")
    require(exact_petal["maximizing_full_petals"] == 15, "exact-petal full petals")
    require(exact_petal["maximizing_remainder"] == 36497, "exact-petal remainder")
    require(exact_petal["endpoint_gaps"] == [
        0,
        676268727,
        676325879,
        3265037774,
        3265407519,
        6322001175,
        6322245154,
        7515065748,
    ], "exact-petal endpoint gaps")
    exact_slope = exact_petal["packed_charge_slope"]
    exact_intercept = exact_petal["packed_charge_intercept"]
    require((exact_slope, exact_intercept) == (1048577, 34798536326), "exact-petal line")
    require(exact_petal["last_open_raw_cross"] < 0, "exact-petal last raw cross")
    require(exact_petal["first_closed_raw_cross"] > 0, "exact-petal first raw cross")
    baseline = exact_slope * 15634 + exact_intercept
    for a in range(67472, 83097):
        full, remainder = 1 + 981105 // a, 981105 % a
        slope = 981105 + a
        intercept = (
            slope * (67462 - a)
            + (full * a * (a - 1) + remainder * (remainder - 1)) // 2
        )
        require(slope * 15634 + intercept <= baseline, f"exact-petal ceiling a={a}")
    for kprime in range(10, 15635):
        nprime, mprime = 1048576 + kprime, 67472 + kprime
        numerator = (
            495405467
            * 274980728111260126
            * comb(mprime, 9)
            * comb(mprime - 9, 2)
        )
        denominator = 10**9 * comb(nprime, 9)
        upper = 981105 * (exact_slope * kprime + exact_intercept)
        require((numerator - upper * denominator > 0) == (kprime >= 15529), f"exact-petal row K'={kprime}")
    require(
        exact_petal["persistence_shifted_polynomial"]
        == [1048577, 102164825695, 1256608704226512],
        "exact-petal persistence",
    )
    require(split_pencil_cap == {
        "minimum_A": 3,
        "owner_weight_ceiling_formula": "A-1",
        "selected_line_mass_formula": "sum_p x_Lp=A",
        "line_charge_formula": "sum_p C(x_Lp,2)",
        "heavy_threshold_formula": "floor(A/2)+1",
        "clean_dominant_cap_formula": "floor((A-2)*S^2/8)",
        "balanced_cap_formula": "C(S,2)",
        "heavy_collision_cap_formula": "C(h,2)*C(A-1,2)",
        "total_cap_formula": "floor((A-2)*S^2/8)+C(S,2)+C(h,2)*C(A-1,2)",
        "clean_inequality_slack_factorization": "(d-1)*(d+s)*(s-1)",
    }, "weighted split-pencil theorem")
    split_a = minimal_split_payment["selected_outside_mass_A"]
    split_total = minimal_split_payment["petal_total_ceiling_S"]
    split_h = split_total // (split_a // 2 + 1)
    split_terms = (
        (split_a - 2) * split_total * split_total // 8,
        comb(split_total, 2),
        comb(split_h, 2) * comb(split_a - 1, 2),
    )
    require(minimal_split_payment == {
        "residual_K_prime": 10,
        "residual_n_prime": 1048586,
        "residual_m_prime": 67482,
        "correction_space_dimension": 10,
        "selector_size": 9,
        "selector_rank": 9,
        "kernel_zero_count": 9,
        "common_core_size": 9,
        "selected_outside_mass_A": 67473,
        "petal_total_ceiling_S": 1048577,
        "petal_size_ceiling": 67472,
        "component_density_numerator": 990810934,
        "component_density_denominator": 10**9,
        "heavy_threshold": 33737,
        "heavy_count": 31,
        "clean_dominant_cap": 9273161316835569,
        "balanced_cap": 549756338176,
        "heavy_collision_cap": 1058433770040,
        "total_capacity": 9274769506943785,
        "weighted_demand": 11736940042024039,
        "demand_capacity_gap": 2462170535080254,
        "raw_demand_capacity_cross": 10398643318411131997122333957687361195838785918523698945763964238907518400,
        "newly_closed_rows": [10, 10],
        "remaining_rank9_interval": [11, 15528],
    }, "minimal split-pencil payment")
    require(tuple(split_terms) == (
        minimal_split_payment["clean_dominant_cap"],
        minimal_split_payment["balanced_cap"],
        minimal_split_payment["heavy_collision_cap"],
    ), "minimal split-pencil terms")
    require(
        sum(split_terms) == minimal_split_payment["total_capacity"]
        < minimal_split_payment["weighted_demand"],
        "minimal split-pencil contradiction",
    )
    clean_inequality_checks = 0
    for size in range(split_a // 2 + 1, split_a):
        deficit = split_a - size
        line_charge = comb(size, 2) + comb(deficit, 2)
        require(
            deficit * size * (split_a - 2) - 2 * line_charge
            == (deficit - 1) * split_a * (size - 1),
            f"minimal split-pencil clean inequality s={size}",
        )
        clean_inequality_checks += 1
    require(
        value["claims"]["rank9_minimal_shortening_closed_K_prime"] == 10,
        "rank-nine minimal split-pencil closure",
    )
    require(offset_split_cap["K11_specializations"] == [
        {
            "j": 9,
            "P": 67474,
            "r": 0,
            "S": 1048578,
            "heavy_count": 31,
            "balanced_cross_floor": 1138185169,
            "maximizing_light_mass": 524289,
            "clean_cap": 9273316443456456,
            "balanced_cap": 549757386753,
            "collision_cap": 1058465144520,
            "total_cap": 9274924665987729,
        },
        {
            "j": 10,
            "P": 67473,
            "r": 1,
            "S": 1048577,
            "heavy_count": 31,
            "balanced_cross_floor": 1138151432,
            "maximizing_light_mass": 524320,
            "clean_cap": 9274257984105680,
            "balanced_cap": 549788929365,
            "collision_cap": 1058465144985,
            "total_cap": 9275866238180030,
        },
    ], "core-offset K'=11 specializations")
    offset_partition_checks = 0
    for petal_mass in range(3, 25):
        for size in range(petal_mass // 2 + 1, petal_mass):
            deficit = petal_mass - size
            charge_twice = size * (size - 1) + deficit * (deficit - 1)
            require(
                deficit * size * (petal_mass - 2) - charge_twice
                == (deficit - 1) * petal_mass * (size - 1),
                f"core-offset clean slack P={petal_mass} s={size}",
            )
            offset_partition_checks += 1

    k11_n, k11_m = k11_payment["n_prime"], k11_payment["m_prime"]
    k11_chart = max(k11_payment["rank9_core_caps"])
    k11_global = comb(k11_n, 9) * k11_chart
    k11_high = k11_global // k11_payment["minimum_high_circuit_rank9_shadows"]
    k11_low_per_record = comb(k11_m - 1, 10)
    k11_low = k11_payment["residual_record_floor"] * k11_low_per_record
    k11_total = k11_high + k11_low
    k11_num = (
        k11_payment["component_density_numerator"]
        * k11_payment["residual_record_floor"]
        * comb(k11_m, 11)
    )
    k11_demand = ceil_ratio(k11_num, k11_payment["component_density_denominator"])
    require(k11_payment["uniform_rank9_chart_cap"] == k11_chart, "K'=11 chart cap")
    require(k11_payment["global_rank9_mark_capacity"] == k11_global, "K'=11 global marks")
    require(k11_payment["high_circuit_incidence_cap"] == k11_high, "K'=11 high circuits")
    require(k11_payment["low_circuit_incidence_cap_at_record_floor"] == k11_low, "K'=11 low circuits")
    require(k11_payment["total_capacity_at_record_floor"] == k11_total, "K'=11 capacity")
    require(k11_payment["required_incidence_at_record_floor"] == k11_demand, "K'=11 demand")
    require(k11_payment["demand_capacity_gap"] == k11_demand - k11_total > 0, "K'=11 gap")
    require(
        k11_payment["record_coefficient_cross"]
        == 990810934 * comb(k11_m, 11) - 10**9 * k11_low_per_record
        > 0,
        "K'=11 record monotonicity",
    )
    for circuit_size in range(1, 6):
        require(
            comb(k11_m - circuit_size, 11 - circuit_size) <= k11_low_per_record,
            f"K'=11 sparse circuit cap c={circuit_size}",
        )
    require(
        value["claims"]["rank9_k11_circuit_split_pencil_closed_K_prime"] == 11,
        "rank-nine K'=11 circuit split-pencil closure",
    )
    k12_m = quotient_line_cap["official_support_size"]
    computed_label_caps = {
        str(support): quotient_line_label_cap(support, k12_m)
        for support in range(1, 6)
    }
    computed_incidence_terms = {
        str(support): computed_label_caps[str(support)]
        * comb(k12_m - support, 11 - support)
        for support in range(1, 6)
    }
    require(quotient_line_cap == {
        "ambient_polynomial_dimension": 12,
        "correction_dimension": 10,
        "quotient_dimension": 2,
        "component_subset_size": 11,
        "support_ceiling": 5,
        "official_support_size": 67484,
        "support_one_label_cap": 2,
        "support_label_caps": computed_label_caps,
        "support_incidence_terms": computed_incidence_terms,
        "per_record_sparse_incidence_cap": sum(computed_incidence_terms.values()),
        "label_cap_formula": "max(c+1, c+floor(e*(m-g)/(c-g)))",
    }, "codimension-two quotient-line sparse-circuit cap")
    require(max(computed_incidence_terms, key=computed_incidence_terms.get) == "2", "quotient-line largest stratum")

    k12_n, k12_m = k12_payment["n_prime"], k12_payment["m_prime"]
    require((k12_payment["K_prime"], k12_n, k12_m) == (12, 1048588, 67484), "K'=12 row")
    k12_core_rows = []
    for core_size in (9, 10, 11):
        petal_mass = k12_m - core_size
        total = k12_n - core_size
        heavy = total // (petal_mass // 2 + 1)
        cross_floor = petal_mass * petal_mass // 4
        balanced = (cross_floor + (core_size - 9) * petal_mass) * comb(total, 2) // cross_floor
        collision = comb(heavy, 2) * (comb(petal_mass - 1, 2) + (core_size - 9) * petal_mass)
        vertex_num = (petal_mass - 2) * total + 2 * heavy * (core_size - 9) * petal_mass
        center = vertex_num // (2 * (petal_mass - 2))
        clean = max(
            light * ((petal_mass - 2) * (total - light) + 2 * heavy * (core_size - 9) * petal_mass) // 2
            for light in range(max(0, center - 3), min(total, center + 3) + 1)
        )
        k12_core_rows.append(clean + balanced + collision)
    k12_kernel = comb(k12_n, 9) * 16295594
    k12_chart = max(k12_core_rows)
    k12_global = comb(k12_n, 9) * k12_chart
    k12_high = k12_global // 45
    k12_low_per_record = quotient_line_cap["per_record_sparse_incidence_cap"]
    k12_low = k12_payment["residual_record_floor"] * k12_low_per_record
    k12_total = k12_kernel + k12_high + k12_low
    k12_numerator = 990810934 * k12_payment["residual_record_floor"] * comb(k12_m, 11)
    k12_demand = ceil_ratio(k12_numerator, 10**9)
    require(k12_payment["kernel_corank_one_record_cap"] == 16295594, "K'=12 kernel record cap")
    require(k12_payment["kernel_extension_factor"] == comb(2, 2) == 1, "K'=12 kernel extension")
    require(k12_payment["kernel_incidence_cap"] == k12_kernel, "K'=12 kernel capacity")
    require(k12_payment["rank9_core_sizes"] == [9, 10, 11], "K'=12 core sizes")
    require(k12_payment["rank9_core_caps"] == k12_core_rows, "K'=12 core caps")
    require(k12_payment["uniform_rank9_chart_cap"] == k12_chart, "K'=12 chart cap")
    require(k12_payment["global_rank9_mark_capacity"] == k12_global, "K'=12 global marks")
    require(k12_payment["minimum_high_circuit_rank9_shadows"] == 45, "K'=12 high shadow floor")
    require(k12_payment["high_circuit_incidence_cap"] == k12_high, "K'=12 high capacity")
    require(k12_payment["low_circuit_per_record_cap"] == k12_low_per_record, "K'=12 low per record")
    require(k12_payment["low_circuit_incidence_cap_at_record_floor"] == k12_low, "K'=12 low capacity")
    require(k12_payment["total_capacity_at_record_floor"] == k12_total, "K'=12 total capacity")
    require(k12_payment["required_incidence_at_record_floor"] == k12_demand, "K'=12 demand")
    require(k12_payment["demand_capacity_gap"] == k12_demand - k12_total > 0, "K'=12 gap")
    require(k12_payment["raw_demand_capacity_cross"] == k12_numerator - 10**9 * k12_total > 0, "K'=12 raw cross")
    require(
        k12_payment["record_coefficient_cross"]
        == 990810934 * comb(k12_m, 11) - 10**9 * k12_low_per_record
        > 0,
        "K'=12 record persistence",
    )
    require(k12_payment["newly_closed_rows"] == [12, 12], "K'=12 closed row")
    require(k12_payment["remaining_rank9_interval"] == [13, 15528], "K'=12 remaining interval")
    require(
        value["claims"]["rank9_k12_quotient_line_circuit_closed_K_prime"] == 12,
        "rank-nine K'=12 quotient-line closure",
    )
    k13_m = completion_cap["official_support_size"]
    structured_cap = sum(
        comb(7, support) * comb(k13_m - support, 11 - support)
        for support in range(2, 6)
    )
    unstructured_terms = {
        str(support): (
            2 * comb(k13_m, support - 1)
            * comb(k13_m - support - 1, 11 - support) // support
        )
        for support in range(2, 6)
    }
    sparse_cap = sum(unstructured_terms.values())
    require(completion_cap == {
        "ambient_polynomial_dimension": 13,
        "correction_dimension": 10,
        "quotient_dimension": 3,
        "component_subset_size": 11,
        "support_minimum": 2,
        "support_ceiling": 5,
        "global_common_zero_count": 0,
        "completion_ceiling": 3,
        "unstructured_completion_ceiling": 2,
        "structured_carrier_ceiling": 7,
        "official_support_size": 67485,
        "structured_carrier_cap": structured_cap,
        "unstructured_support_terms": unstructured_terms,
        "unstructured_completion_cap": sparse_cap,
        "per_record_sparse_incidence_cap": sparse_cap,
    }, "codimension-three sparse-circuit completion cap")
    require(sparse_cap > structured_cap, "codimension-three active branch")
    require(all(
        2 * comb(k13_m - support - 1, 11 - support)
        >= comb(k13_m - support, 11 - support)
        for support in range(2, 6)
    ), "codimension-three two-completion maximizer")

    k13_n = k13_payment["n_prime"]
    require((k13_payment["K_prime"], k13_n, k13_payment["m_prime"]) == (13, 1048589, 67485), "K'=13 row")
    k13_core_rows = []
    for core_size in (9, 10, 11, 12):
        petal_mass = k13_m - core_size
        total = k13_n - core_size
        heavy = total // (petal_mass // 2 + 1)
        cross_floor = petal_mass * petal_mass // 4
        balanced = (cross_floor + (core_size - 9) * petal_mass) * comb(total, 2) // cross_floor
        collision = comb(heavy, 2) * (comb(petal_mass - 1, 2) + (core_size - 9) * petal_mass)
        vertex_num = (petal_mass - 2) * total + 2 * heavy * (core_size - 9) * petal_mass
        center = vertex_num // (2 * (petal_mass - 2))
        clean = max(
            light * ((petal_mass - 2) * (total - light) + 2 * heavy * (core_size - 9) * petal_mass) // 2
            for light in range(max(0, center - 3), min(total, center + 3) + 1)
        )
        k13_core_rows.append(clean + balanced + collision)
    k13_coranks = [1, 2]
    k13_record_caps = [kernel_record_cap(13, corank) for corank in k13_coranks]
    k13_extensions = [comb(3, corank + 1) for corank in k13_coranks]
    k13_kernel_terms = [
        comb(k13_n, 10 - corank) * cap * extension
        for corank, cap, extension in zip(k13_coranks, k13_record_caps, k13_extensions)
    ]
    k13_kernel = sum(k13_kernel_terms)
    k13_chart = max(k13_core_rows)
    k13_global = comb(k13_n, 9) * k13_chart
    k13_high = k13_global // 45
    k13_low = k13_payment["residual_record_floor"] * sparse_cap
    k13_total = k13_kernel + k13_high + k13_low
    k13_numerator = 990810934 * k13_payment["residual_record_floor"] * comb(k13_m, 11)
    k13_demand = ceil_ratio(k13_numerator, 10**9)
    require(k13_payment["kernel_coranks"] == k13_coranks, "K'=13 kernel coranks")
    require(k13_payment["kernel_record_caps"] == k13_record_caps == [16295594, 253241283], "K'=13 kernel record caps")
    require(k13_payment["kernel_extension_factors"] == k13_extensions == [3, 1], "K'=13 kernel extensions")
    require(k13_payment["kernel_incidence_terms"] == k13_kernel_terms, "K'=13 kernel terms")
    require(k13_payment["kernel_incidence_cap"] == k13_kernel, "K'=13 kernel capacity")
    require(k13_payment["rank9_core_sizes"] == [9, 10, 11, 12], "K'=13 core sizes")
    require(k13_payment["rank9_core_caps"] == k13_core_rows, "K'=13 core caps")
    require(k13_payment["uniform_rank9_chart_cap"] == k13_chart, "K'=13 chart cap")
    require(k13_payment["global_rank9_mark_capacity"] == k13_global, "K'=13 global marks")
    require(k13_payment["minimum_high_circuit_rank9_shadows"] == 45, "K'=13 high shadow floor")
    require(k13_payment["high_circuit_incidence_cap"] == k13_high, "K'=13 high capacity")
    require(k13_payment["low_circuit_per_record_cap"] == sparse_cap, "K'=13 low per record")
    require(k13_payment["low_circuit_incidence_cap_at_record_floor"] == k13_low, "K'=13 low capacity")
    require(k13_payment["total_capacity_at_record_floor"] == k13_total, "K'=13 total capacity")
    require(k13_payment["required_incidence_at_record_floor"] == k13_demand, "K'=13 demand")
    require(k13_payment["demand_capacity_gap"] == k13_demand - k13_total > 0, "K'=13 gap")
    require(k13_payment["raw_demand_capacity_cross"] == k13_numerator - 10**9 * k13_total > 0, "K'=13 raw cross")
    require(
        k13_payment["record_coefficient_cross"]
        == 990810934 * comb(k13_m, 11) - 10**9 * sparse_cap
        > 0,
        "K'=13 record persistence",
    )
    require(k13_payment["newly_closed_rows"] == [13, 13], "K'=13 closed row")
    require(k13_payment["remaining_rank9_interval"] == [14, 15528], "K'=13 remaining interval")
    require(
        value["claims"]["rank9_k13_sparse_circuit_completion_closed_K_prime"] == 13,
        "rank-nine K'=13 sparse-circuit closure",
    )
    records = joint_sparse_payment["residual_record_floor"]
    joint_rows = [
        joint_sparse_shadow_row(kprime, records)
        for kprime in range(14, 22)
    ]
    endpoint_totals = {
        str(row["K_prime"]): {
            "structured": sum(row["structured_support_terms"].values()),
            "unstructured": sum(row["unstructured_support_terms"].values()),
        }
        for row in (joint_rows[0], joint_rows[-1])
    }
    require(completion_ladder == {
        "correction_dimension": 10,
        "component_subset_size": 11,
        "support_range": [2, 5],
        "global_common_zero_count": 0,
        "quotient_dimension_formula": "q=K_prime-10",
        "completion_ceiling_formula": "q",
        "unstructured_completion_ceiling_formula": "q-1",
        "structured_carrier_ceiling_formula": "q+4",
        "structured_support_cap_formula": "C(q+4,c)*C(m-c,11-c)",
        "unstructured_support_cap_formula": "floor(C(m,c-1)*max_b(b*C(m-c+1-b,11-c))/c)",
        "official_K_prime_interval": [14, 21],
        "official_unstructured_maximizer_formula": "b=q-1",
        "endpoint_totals": endpoint_totals,
    }, "sparse-circuit completion ladder")
    require(joint_shadow_ledger == {
        "component_subset_size": 11,
        "shadow_subset_size": 9,
        "total_shadow_count": 55,
        "high_support_minimum": 6,
        "baseline_shadow_cost": 45,
        "low_supports": [2, 3, 4, 5],
        "rank9_shadow_counts": [19, 27, 34, 40],
        "premium_weights": [26, 18, 11, 5],
        "shadow_formula": "55-C(11-c,2)",
        "joint_capacity_formula": "floor((G+R*max_a(sum_c((45-q_c)*L_a_c)))/45)",
    }, "joint sparse-shadow ledger")
    require(joint_sparse_payment["rows"] == joint_rows, "joint sparse-shadow rows")
    require(joint_sparse_payment["closed_K_prime_interval"] == [14, 21], "joint closed interval")
    require(
        (joint_sparse_payment["component_density_numerator"],
         joint_sparse_payment["component_density_denominator"])
        == (990810934, 10**9),
        "joint density",
    )
    require(all(
        row["rank9_core_maximizer"] == row["K_prime"] - 1
        and set(row["unstructured_completion_maximizers"].values())
        == {row["quotient_dimension"] - 1}
        and row["unstructured_sparse_premium"] > row["structured_sparse_premium"]
        and row["demand_capacity_gap"] > 0
        and row["record_coefficient_cross"] > 0
        and row["raw_demand_capacity_cross"] > 0
        for row in joint_rows
    ), "joint sparse-shadow strict rows")
    require(
        joint_sparse_payment["minimum_record_coefficient_cross"]
        == min(row["record_coefficient_cross"] for row in joint_rows)
        == 142682033239797420617137269900169736054865857428491736720,
        "joint minimum record coefficient",
    )
    require(
        joint_sparse_payment["minimum_gap_row"] == 21
        and joint_rows[-1]["demand_capacity_gap"]
        == 205305519860193617784849691734671763401656917434567909452790,
        "joint minimum gap",
    )
    require(joint_sparse_payment["newly_closed_rows"] == [14, 21], "joint newly closed rows")
    require(joint_sparse_payment["remaining_rank9_interval"] == [22, 15528], "joint remaining interval")
    wall = joint_sparse_shadow_row(22, records)
    require(joint_sparse_payment["K22_method_wall"] == {
        "K_prime": 22,
        "total_capacity_at_record_floor": wall["total_capacity_at_record_floor"],
        "required_incidence_at_record_floor": wall["required_incidence_at_record_floor"],
        "capacity_excess": -wall["demand_capacity_gap"],
    }, "K'=22 method wall")
    require(wall["demand_capacity_gap"] < 0, "K'=22 payment failure")
    require(
        value["claims"]["rank9_k14_k21_sparse_shadow_closed_K_prime"] == 21,
        "rank-nine K'=14..21 joint closure",
    )
    integral_rows = {
        str(core): integral_core_offset_row(22, core)
        for core in range(9, 22)
    }
    require(
        integral_heavy_cap["clean_caps"]
        == {key: row["cap"] for key, row in integral_rows.items()},
        "integral heavy clean caps",
    )
    require(
        integral_heavy_cap["chart_caps"]
        == {key: row["chart"] for key, row in integral_rows.items()},
        "integral heavy chart caps",
    )
    require(
        all(
            row["count"] == row["full"] == 8 and row["segments"] == 271
            for row in integral_rows.values()
        ),
        "integral heavy optimizer shape",
    )
    require(
        integral_heavy_cap["maximizing_core"] == 21
        and integral_heavy_cap["uniform_chart_cap"] == 9269974099565290
        and integral_heavy_cap["chart_saving"] == 17960461975558,
        "integral heavy endpoint",
    )
    require(
        near_saturation["support_interval"] == [2, 4]
        and near_saturation["K22"]["weighted_premium_saving"]
        == 393439020925119039272226731095485935384019750,
        "near-saturation carrier saving",
    )
    require(
        k22_refined_payment["uniform_corank_one_record_cap"] == 8147918
        and k22_refined_payment["maximizing_core"] == 21
        and k22_refined_payment["demand_capacity_gap"]
        == 1232731756628187885277355254597101817411431837269258943471111
        and k22_refined_payment["record_coefficient_cross"] > 0
        and k22_refined_payment["floor_record_raw_cross"] > 0,
        "K'=22 strict refined payment",
    )
    require(
        k22_refined_payment["active_sparse_premium"]
        > k22_refined_payment["structured_sparse_premium"],
        "K'=22 active refined branch",
    )
    depths = {2: 7, 3: 2, 4: 1, 5: 0}
    require(
        defect_hierarchy["depths"]
        == {str(support): depth for support, depth in depths.items()},
        "completion-defect depths",
    )
    require(
        all(
            (depth + 2) * support - depth - 1 <= 10
            for support, depth in depths.items()
            if depth > 0
        )
        and all(
            (depth + 3) * support - depth - 2 > 10
            for support, depth in depths.items()
        ),
        "completion-defect maximality",
    )
    require(
        k23_refined_payment["maximizing_core"] == 22
        and k23_refined_payment["uniform_rank9_chart_cap"] == 9270248806170409
        and k23_refined_payment["demand_capacity_gap"]
        == 1704262040773185642290284810631267267026794188450394076492364
        and k23_refined_payment["record_coefficient_cross"] > 0
        and k23_refined_payment["floor_record_raw_cross"] > 0,
        "K'=23 strict completion-defect payment",
    )
    require(
        k23_refined_payment["K24_method_wall"]["capacity_excess"]
        == 1284050362432335685834886981937569506815315444344843084997754,
        "old K'=24 method wall",
    )
    require(
        universal_completion["supported_circuit_sizes"] == list(range(2, 10))
        and universal_completion["completion_ceiling"] == "b<=q"
        and set(universal_completion["K24_example"]["incidence_caps"])
        == {"6", "7", "8", "9"},
        "universal completion cap",
    )
    shadow_supports = list(range(2, 12))
    require(
        full_deficit_ledger["circuit_supports"] == shadow_supports
        and full_deficit_ledger["deficit_weights"]
        == [comb(11 - support, 2) for support in shadow_supports]
        and all(
            shadow + deficit == 55
            for shadow, deficit in zip(
                full_deficit_ledger["rank9_shadow_counts"],
                full_deficit_ledger["deficit_weights"],
            )
        ),
        "full 55-shadow deficit ledger",
    )
    full_rows = full_deficit_payment["rows"]
    require(set(full_rows) == {str(kprime) for kprime in range(24, 42)}, "full-deficit rows")
    require(
        all(
            full_rows[str(kprime)]["maximizing_core"] == kprime - 1
            and full_rows[str(kprime)]["demand_capacity_gap"] > 0
            for kprime in range(24, 41)
        ),
        "full-deficit strict closed rows",
    )
    require(
        min(
            full_rows[str(kprime)]["demand_capacity_gap"]
            for kprime in range(24, 41)
        )
        == full_rows["40"]["demand_capacity_gap"]
        == 2272401814108959137912675549447888006236817090602808413697595,
        "full-deficit minimum gap",
    )
    require(
        full_rows["41"]["demand_capacity_gap"] < 0
        and full_deficit_payment["K41_method_wall"]["capacity_excess"]
        == 4398836630793080990004182400858693750491819390616783425932508,
        "full-deficit K'=41 wall",
    )
    require(
        sharp_isolated == {
            "correction_dimension": 10,
            "tuple_size": 11,
            "dense_locator_degree": 18,
            "retained_slopes_are_distinct": True,
            "retained_slopes_avoid_locator_roots": True,
            "old_generic_isolated_cap_per_tuple": 198,
            "new_record_isolated_cap_per_tuple": 1,
            "component_lower_bound": "N*C(m_prime,11)-C(n_prime,11)",
        },
        "rank-stratified isolated-incidence theorem",
    )
    sharp_demand = (
        k41_sharp["residual_record_floor"] * comb(k41_sharp["m"], 11)
        - comb(k41_sharp["n"], 11)
    )
    sharp_coefficient = (
        55 * comb(k41_sharp["m"], 11) - k41_sharp["completion_premium"]
    )
    sharp_raw = (
        k41_sharp["residual_record_floor"] * sharp_coefficient
        - 55 * comb(k41_sharp["n"], 11)
        - 55 * k41_sharp["kernel_capacity"]
        - k41_sharp["rank_nine_marks"]
    )
    require(
        k41_sharp["closed_row"] == 41
        and k41_sharp["new_closed_prefix"] == [10, 41]
        and k41_sharp["first_method_wall"] == 42
        and k41_sharp["isolated_cap_per_eleven_set"] == 1
        and k41_sharp["isolated_global_cap"] == comb(k41_sharp["n"], 11)
        and k41_sharp["required_component_incidence"] == sharp_demand
        and k41_sharp["gap"] == sharp_demand - k41_sharp["total_capacity"]
        and k41_sharp["gap"]
        == 3959829848992990899082071934034620604165114037293042026746826
        and k41_sharp["record_coefficient_cross"] == sharp_coefficient > 0
        and k41_sharp["floor_record_raw_cross"] == sharp_raw > 0
        and k41_sharp["K42_capacity_excess"]
        == 2710771376158610722953158157862051010402433288229120154217278
        and k41_sharp["remaining_rank9_interval"] == [42, 15528],
        "sharp-isolated K'=41 payment and K'=42 wall",
    )
    expected_target_supports = {
        str(defect): [
            target
            for target in range(2, 10)
            if 5 + (defect + 1) * target - defect - 1 <= 10
        ]
        for defect in range(5)
    }
    require(
        cross_support_carrier
        == {
            "correction_dimension": 10,
            "component_size": 11,
            "source_support_symbol": "c",
            "target_support_symbol": "d",
            "support_range": [2, 9],
            "defect_range": "0<=s<=q",
            "completion_count": "q-s",
            "carrier_size": "q+c-1+s(d-1)",
            "vandermonde_condition": "c+(s+1)d-s-1<=10",
            "incidence_cap": "C(q+c-1+s(d-1),d)C(m-d,11-d)",
            "support5_target_supports": expected_target_supports,
            "fallback_completion_ceiling": "q-5",
        },
        "cross-support carrier theorem",
    )
    row42_cross = cross_support_payment_row(42, k41_sharp["residual_record_floor"])
    row43_cross = cross_support_payment_row(43, k41_sharp["residual_record_floor"])
    require(
        k42_cross_support["closed_row"] == 42
        and k42_cross_support["new_closed_prefix"] == [10, 42]
        and k42_cross_support["first_method_wall"] == 43
        and k42_cross_support["residual_record_floor"]
        == k41_sharp["residual_record_floor"]
        and k42_cross_support["source_support"] == 5
        and k42_cross_support["carrier_defects"] == list(range(5))
        and k42_cross_support["branch_partition"]
        == "s=q-max_A b_A for s=0..4, otherwise max_A b_A<=q-5"
        and k42_cross_support["fallback_completion_ceiling"] == "q-5"
        and all(
            k42_cross_support[key] == row42_cross[key]
            for key in row42_cross
        )
        and k42_cross_support["completion_premium"]
        == k42_cross_support["branch_premiums"]["fallback"]
        and k42_cross_support["gap"]
        == 4081031051590194485758587836050845115467905186032497191061176
        and k42_cross_support["record_coefficient_cross"] > 0
        and k42_cross_support["floor_record_raw_cross"] > 0
        and all(
            k42_cross_support["K43_method_wall"][key] == row43_cross[key]
            for key in row43_cross
            if key
            not in {
                "isolated_global_cap",
                "uncoupled_completion_premium",
                "premium_saving",
                "gap",
            }
        )
        and k42_cross_support["K43_method_wall"]["capacity_excess"]
        == -row43_cross["gap"]
        == 2590504432899371163130658487199612335023802688487478696166262
        and row43_cross["floor_record_raw_cross"] < 0
        and k42_cross_support["remaining_rank9_interval"] == [43, 15528],
        "cross-support K'=42 payment and K'=43 wall",
    )
    require(
        value["claims"]["rank9_k22_integral_near_saturation_closed_K_prime"] == 22
        and value["claims"]["rank9_k23_completion_defect_closed_K_prime"] == 23
        and value["claims"]["rank9_k24_k40_full_deficit_shadow_closed_K_prime"] == 40
        and value["claims"]["rank9_k41_sharp_isolated_closed_K_prime"] == 41
        and value["claims"]["rank9_k42_cross_support_defect_closed_K_prime"] == 42,
        "refined rank-nine closure claims",
    )
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
    hierarchy = value["kernel_two_step_nine_shadow_hierarchy"]
    require(hierarchy["couplings"] == two_step_hierarchy_rows(), "two-step hierarchy rows")
    hierarchy_checks = 0
    for dimension, shadows, outside, partners, pair_floor, coloops, multiplicity in hierarchy["couplings"]:
        require(outside == partners + 1, f"two-step outside d={dimension}")
        require(pair_floor == outside * partners // 2, f"two-step pair floor d={dimension}")
        require(shadows == comb(dimension + 2, 2), f"two-step shadows d={dimension}")
        require(coloops == 11 - dimension, f"two-step coloop cap d={dimension}")
        require(multiplicity == comb(coloops, 2), f"two-step target multiplicity d={dimension}")
        hierarchy_checks += 1
    two_step_cut = value["kernel_two_step_nine_shadow_capacity_cut"]
    two_step_checks = 0
    for kprime in range(two_step_cut["replay_K_prime_minimum"], two_step_cut["closed_K_prime_maximum"] + 1):
        optimum, allocation, dual, branches = kernel_two_step_certificate(kprime)
        require(kernel_demand_ratio(kprime) > optimum, f"kernel two-step cut {kprime}")
        require(all(number > 0 for number in allocation), f"two-step positive support {kprime}")
        require(all(number >= 0 for number in dual), f"two-step dual {kprime}")
        require(branches == two_step_cut["endpoint_branch_pattern"], f"two-step branches {kprime}")
        two_step_checks += 1
    two_step_endpoint = kernel_two_step_certificate(18101)[0]
    two_step_wall = kernel_two_step_certificate(18102)[0]
    require(two_step_checks == two_step_cut["replay_rows"] - 1, "two-step closed row count")
    require(two_step_endpoint == Fraction(two_step_cut["endpoint_optimum_numerator"], two_step_cut["endpoint_optimum_denominator"]), "two-step endpoint optimum")
    require(two_step_wall == Fraction(two_step_cut["wall_optimum_numerator"], two_step_cut["wall_optimum_denominator"]), "two-step wall optimum")
    require(kernel_demand_ratio(18102) < two_step_wall, "kernel two-step wall")
    require(two_step_cut["endpoint_gap"] == 33462159928103132226516704640419847248244116666500998762314, "two-step endpoint gap")
    require(two_step_cut["wall_excess"] == 275016496133605602641019628236447268989861205055439981187167, "two-step wall excess")
    multistep_hierarchy = value["kernel_multistep_shadow_hierarchy"]
    require(multistep_hierarchy["couplings"] == multistep_hierarchy_rows(), "multistep hierarchy rows")
    require(multistep_hierarchy["coupling_count"] == 28, "multistep hierarchy count")
    require(multistep_hierarchy["triple_couplings"] == [row[1:] for row in multistep_hierarchy_rows() if row[0] == 3], "triple hierarchy rows")
    multistep_hierarchy_checks = 0
    for step, dimension, shadows, outside, raising_floor, coloops, multiplicity in multistep_hierarchy["couplings"]:
        require(shadows == comb(dimension + 2, step), f"multistep shadows t={step} d={dimension}")
        require(outside == 67472 + dimension, f"multistep outside t={step} d={dimension}")
        require(raising_floor == comb(outside, step), f"multistep raising t={step} d={dimension}")
        require(coloops == 9 - dimension + step, f"multistep coloops t={step} d={dimension}")
        require(multiplicity == comb(coloops, step), f"multistep multiplicity t={step} d={dimension}")
        multistep_hierarchy_checks += 1
    multistep_cut = value["kernel_three_step_shadow_capacity_cut"]
    multistep_checks = 0
    for kprime in range(multistep_cut["replay_K_prime_minimum"], multistep_cut["closed_K_prime_maximum"] + 1):
        optimum, allocation, dual, branches, tight = kernel_multistep_certificate(kprime)
        require(kernel_demand_ratio(kprime) > optimum, f"kernel multistep cut {kprime}")
        require(all(number > 0 for number in allocation), f"multistep positive support {kprime}")
        require(all(number >= 0 for number in dual), f"multistep dual {kprime}")
        require(branches == multistep_cut["endpoint_branch_pattern"], f"multistep branches {kprime}")
        require(tight == multistep_cut["tight_hierarchy_rows"], f"multistep tight rows {kprime}")
        multistep_checks += 1
    multistep_endpoint = kernel_multistep_certificate(18158)[0]
    multistep_wall = kernel_multistep_certificate(18159)[0]
    require(multistep_checks == multistep_cut["replay_rows"] - 1, "multistep closed row count")
    require(multistep_endpoint == Fraction(multistep_cut["endpoint_optimum_numerator"], multistep_cut["endpoint_optimum_denominator"]), "multistep endpoint optimum")
    require(multistep_wall == Fraction(multistep_cut["wall_optimum_numerator"], multistep_cut["wall_optimum_denominator"]), "multistep wall optimum")
    require(kernel_demand_ratio(18159) < multistep_wall, "kernel multistep wall")
    require(multistep_cut["endpoint_gap"] == 289110608820324799941118306538399899258195112067661304310498, "multistep endpoint gap")
    require(multistep_cut["wall_excess"] == 20286290696334777989469267474876769475675508046109372076445, "multistep wall excess")
    projective_cap = value["kernel_corank1_projective_pair_cap"]
    projective_n = projective_cap["domain_size"]
    projective_m = projective_cap["support_size"]
    maximum_dependent = (projective_m - 1) ** 2 + 1
    independent_pairs = projective_m**2 - maximum_dependent
    projective_record_cap, projective_remainder = divmod(
        projective_n * (projective_n - 1), independent_pairs
    )
    require(projective_cap["zero_normal_upper_bound"] == 0, "projective zero normals")
    require(projective_cap["minimum_projective_classes"] == 2, "projective class count")
    require(independent_pairs == projective_cap["minimum_independent_ordered_pairs_per_record"] == 134944, "projective pair floor")
    require(projective_record_cap == projective_cap["record_cap"] == PROJECTIVE_PAIR_RECORD_CAP, "projective record cap")
    require(projective_remainder == projective_cap["division_remainder"] == 29760, "projective remainder")
    projective_cut = value["kernel_projective_pair_capacity_cut"]
    require(projective_cut["checked_rows_including_wall"] == projective_cut["first_open_K_prime"] - projective_cut["replay_K_prime_minimum"] + 1, "projective replay count")
    require(projective_cut["active_individual_caps"] == [1, 2], "projective active caps")
    require(projective_cut["active_shared_resources"] == [], "projective active resources")
    require(projective_cut["dual_tree"] == PROJECTIVE_PAIR_DUAL_TREE, "projective dual tree")
    require(projective_cut["tight_hierarchy_rows"] == PROJECTIVE_PAIR_TIGHT_ROWS, "projective tight rows")
    projective_rows = (
        ("replay_start", 18159, True),
        ("endpoint", 377673, True),
        ("wall", 377674, False),
    )
    for prefix, kprime, closed in projective_rows:
        optimum, allocation, cap_dual, branches, tight = kernel_projective_pair_certificate(kprime)
        require(optimum == Fraction(projective_cut[f"{prefix}_optimum_numerator"], projective_cut[f"{prefix}_optimum_denominator"]), f"projective {prefix} optimum")
        require((kernel_demand_ratio(kprime) > optimum) is closed, f"projective {prefix} sign")
        require(all(number > 0 for number in allocation), f"projective {prefix} support")
        require(all(number > 0 for number in cap_dual.values()), f"projective {prefix} dual")
        require(branches[:2] == projective_cut["active_individual_cap_branches"], f"projective {prefix} branches")
        require(tight == projective_cut["tight_hierarchy_rows"], f"projective {prefix} tight")
    require(projective_cut["endpoint_gap"] == 608290099077401798561583762592584078050381528604243813748500153228, "projective endpoint gap")
    require(projective_cut["wall_excess"] == 1089804128361045148874283346879615159892995682385275039289561845323, "projective wall excess")
    projective_basis_cap = value["kernel_corank2_projective_basis_cap"]
    basis_n = projective_basis_cap["domain_size"]
    basis_m = projective_basis_cap["support_size"]
    maximum_collinear = comb(basis_m - 1, 3)
    independent_triples = basis_m * (basis_m - 1) * (basis_m - 2) - 6 * maximum_collinear
    basis_record_cap, basis_remainder = divmod(
        basis_n * (basis_n - 1) * (basis_n - 2), independent_triples
    )
    q, r = 17, basis_m - 17
    split_difference = maximum_collinear - comb(q, 3) - comb(r + 1, 3)
    split_decomposition = (r - 1) * (comb(q, 2) - 1) + (q - 2) * comb(r - 1, 2)
    require(projective_basis_cap["zero_normal_upper_bound"] == 0, "projective-basis zero normals")
    require(projective_basis_cap["maximum_projective_class_size"] == 1, "projective-basis class size")
    require(projective_basis_cap["noncollinear"] is True, "projective-basis noncollinearity")
    require(split_difference == split_decomposition >= 0, "projective-basis split identity")
    require(maximum_collinear == projective_basis_cap["maximum_collinear_unordered_triples"], "projective-basis collinear triples")
    require(independent_triples == projective_basis_cap["minimum_independent_ordered_triples_per_record"] == 13657614768, "projective-basis triple floor")
    require(basis_record_cap == projective_basis_cap["record_cap"] == PROJECTIVE_BASIS_RECORD_CAP, "projective-basis record cap")
    require(basis_remainder == projective_basis_cap["division_remainder"] == 2935655472, "projective-basis remainder")
    matroid_floor = value["matroid_rank3_bounded_parallel_basis_floor"]
    require(matroid_floor == {
        "status": "proved",
        "rank": 3,
        "loopless": True,
        "basis_floor": "2*b(M)>=(m-1)*(m-1-a)",
        "smallest_class_contraction_floor": "b(M/e)>=c*(m-2*c)>=m-2",
        "induction_slack": "a-1",
        "sharp_when": "a divides m-1 and m-1>=2a",
    }, "rank-three matroid floor")
    uniform_basis_cap = value["kernel_corank2_uniform_projective_basis_cap"]
    require(uniform_basis_cap["status"] == "proved", "uniform projective-basis status")
    require(uniform_basis_cap["t_minimum"] == 0 and uniform_basis_cap["t_maximum"] == 1048566, "uniform projective-basis range")
    require(uniform_basis_cap["parallel_class_ceiling"] == "t+1", "uniform projective-basis parallel ceiling")
    require(uniform_basis_cap["ordered_basis_floor"] == "3*67472*(67473+t)", "uniform projective-basis floor")
    require(uniform_basis_cap["ratio_step_sign"] == "2*t+3*67472+3-1048576", "uniform projective-basis ratio")
    require(uniform_basis_cap["turn_left"] == 423078 and uniform_basis_cap["turn_right"] == 423079, "uniform projective-basis turn")
    require(uniform_basis_cap["complete_cap"] == 84416263, "uniform projective-basis complete endpoint")
    require(uniform_basis_cap["adjacent_cap"] == 84415253, "uniform projective-basis adjacent endpoint")
    require(uniform_basis_cap["far_endpoint_cap"] == 40828171, "uniform projective-basis far endpoint")
    require(uniform_basis_cap["uniform_record_cap"] == PROJECTIVE_BASIS_RECORD_CAP, "uniform projective-basis cap")
    projective_basis_cut = value["kernel_corank2_projective_capacity_cut"]
    require(projective_basis_cut["status"] == "proved", "projective-basis status")
    require(projective_basis_cut["checked_rows_including_wall"] == projective_basis_cut["first_open_K_prime"] - projective_basis_cut["replay_K_prime_minimum"] + 1, "projective-basis replay count")
    require(projective_basis_cut["active_individual_caps"] == [1, 2], "projective-basis active caps")
    require(projective_basis_cut["active_shared_resources"] == [], "projective-basis active resources")
    require(projective_basis_cut["dual_tree"] == PROJECTIVE_BASIS_DUAL_TREE, "projective-basis dual tree")
    require(projective_basis_cut["tight_hierarchy_rows"] == PROJECTIVE_BASIS_TIGHT_ROWS, "projective-basis tight rows")
    projective_basis_rows = (
        ("replay_start", 377674, True),
        ("endpoint", 568338, True),
        ("wall", 568339, False),
    )
    for prefix, kprime, closed in projective_basis_rows:
        optimum, allocation, cap_dual, branches, tight = kernel_projective_basis_certificate(kprime)
        require(optimum == Fraction(projective_basis_cut[f"{prefix}_optimum_numerator"], projective_basis_cut[f"{prefix}_optimum_denominator"]), f"projective-basis {prefix} optimum")
        require((kernel_demand_ratio(kprime) > optimum) is closed, f"projective-basis {prefix} sign")
        require(all(number > 0 for number in allocation), f"projective-basis {prefix} support")
        require(all(number > 0 for number in cap_dual.values()), f"projective-basis {prefix} dual")
        require(branches[:2] == projective_basis_cut["active_individual_cap_branches"], f"projective-basis {prefix} branches")
        require(tight == projective_basis_cut["tight_hierarchy_rows"], f"projective-basis {prefix} tight")
    require(projective_basis_cut["endpoint_gap"] == 38432453444617070485037263551626410396462586389410416394578520596038, "projective-basis endpoint gap")
    require(projective_basis_cut["wall_excess"] == 36180877960369511460476382880286784896208001102094988739728829832800, "projective-basis wall excess")
    projective_frame_cap = value["kernel_corank3_projective_basis_cap"]
    frame_n = projective_frame_cap["domain_size"]
    frame_m = projective_frame_cap["support_size"]
    maximum_coplanar = comb(frame_m - 1, 4)
    independent_quadruples = (
        frame_m * (frame_m - 1) * (frame_m - 2) * (frame_m - 3)
        - 24 * maximum_coplanar
    )
    frame_record_cap, frame_remainder = divmod(
        frame_n * (frame_n - 1) * (frame_n - 2) * (frame_n - 3),
        independent_quadruples,
    )
    q, r = 18, frame_m - 18
    split_bound = comb(q, 4) + (q // 2) * comb(r, 2) + 2 * comb(r, 3) + comb(r, 4)
    split_difference = maximum_coplanar - split_bound
    split_decomposition = (
        (q - 3) * comb(r, 3)
        + (comb(q - 1, 2) - q // 2) * comb(r, 2)
        + (r - 1) * comb(q - 1, 3)
    )
    require(projective_frame_cap["zero_normal_upper_bound"] == 0, "projective-frame zero normals")
    require(projective_frame_cap["maximum_projective_class_size"] == 1, "projective-frame class size")
    require(projective_frame_cap["maximum_projective_line_size"] == 2, "projective-frame line size")
    require(projective_frame_cap["spans_projective_space"] is True, "projective-frame span")
    require(split_difference == split_decomposition >= 0, "projective-frame split identity")
    require(maximum_coplanar == projective_frame_cap["maximum_coplanar_unordered_quadruples"], "projective-frame coplanar quadruples")
    require(independent_quadruples == projective_frame_cap["minimum_independent_ordered_quadruples_per_record"] == 1228711865141376, "projective-frame quadruple floor")
    require(frame_record_cap == projective_frame_cap["record_cap"] == PROJECTIVE_FRAME_RECORD_CAP, "projective-frame record cap")
    require(frame_remainder == projective_frame_cap["division_remainder"] == 1056607358217600, "projective-frame remainder")
    rank4_floor = value["matroid_rank4_bounded_point_line_basis_floor"]
    require(rank4_floor["status"] == "proved" and rank4_floor["rank"] == 4, "rank-four matroid status")
    require(rank4_floor["parallel_class_ceiling"] == "a", "rank-four point ceiling")
    require(rank4_floor["rank2_flat_ceiling"] == "a+1", "rank-four line ceiling")
    require(rank4_floor["basis_floor"] == "6*b(M)>=Q_a(r)", "rank-four basis floor")
    rank4_recurrence_checks = 0
    for a_test in range(1, 31):
        direct = 6
        for r_test in range(3, 81):
            if r_test >= 4:
                direct = min(
                    rank4_coloop6(a_test, r_test),
                    direct + rank4_increment6(a_test, r_test),
                )
            require(rank4_basis_floor6(a_test, r_test) == direct, "rank-four recurrence evaluator")
            rank4_recurrence_checks += 1
    require(rank4_recurrence_checks == 2340, "rank-four recurrence grid")
    uniform_frame_cap = value["kernel_corank3_uniform_projective_basis_cap"]
    require(uniform_frame_cap["status"] == "proved", "uniform projective-frame status")
    require(uniform_frame_cap["rank_gap"] == 67474, "uniform projective-frame rank gap")
    require(uniform_frame_cap["parallel_class_ceiling"] == "t+1", "uniform projective-frame point ceiling")
    require(uniform_frame_cap["rank2_flat_ceiling"] == "t+2", "uniform projective-frame line ceiling")
    require(uniform_frame_cap["complete_row"] == uniform_corank3_row(0), "uniform projective-frame complete row")
    require(uniform_frame_cap["adjacent_row"] == uniform_corank3_row(1), "uniform projective-frame adjacent row")
    require(uniform_frame_cap["first_nontrivial_row"] == uniform_corank3_row(2), "uniform projective-frame first nontrivial row")
    require(uniform_frame_cap["middle_row"] == uniform_corank3_row(1048566 // 2), "uniform projective-frame middle row")
    require(uniform_frame_cap["official_endpoint"] == uniform_corank3_row(1048566), "uniform projective-frame endpoint")
    require(uniform_frame_cap["uniform_record_cap"] == PROJECTIVE_FRAME_RECORD_CAP, "uniform projective-frame cap")
    require(uniform_frame_cap["checked_rows"] == 1048567, "uniform projective-frame row count")
    require(uniform_frame_cap["first_maximizer"] == 0 and uniform_frame_cap["first_excess"] is None, "uniform projective-frame maximum")
    projective_frame_cut = value["kernel_corank3_projective_capacity_cut"]
    require(projective_frame_cut["status"] == "proved", "projective-frame status")
    require(projective_frame_cut["premises"] == [], "projective-frame premises")
    require(projective_frame_cut["checked_rows_including_wall"] == projective_frame_cut["first_open_K_prime"] - projective_frame_cut["replay_K_prime_minimum"] + 1, "projective-frame replay count")
    require(projective_frame_cut["active_individual_caps"] == [1, 2, 3], "projective-frame active caps")
    require(projective_frame_cut["active_shared_resources"] == [], "projective-frame active resources")
    require(projective_frame_cut["dual_forest"] == PROJECTIVE_FRAME_DUAL_FOREST, "projective-frame dual forest")
    require(projective_frame_cut["tight_hierarchy_rows"] == PROJECTIVE_FRAME_TIGHT_ROWS, "projective-frame tight rows")
    projective_frame_rows = (
        ("replay_start", 568339, True),
        ("endpoint", 796598, True),
        ("wall", 796599, False),
    )
    for prefix, kprime, closed in projective_frame_rows:
        optimum, allocation, cap_dual, branches, tight = kernel_projective_frame_certificate(kprime)
        require(optimum == Fraction(projective_frame_cut[f"{prefix}_optimum_numerator"], projective_frame_cut[f"{prefix}_optimum_denominator"]), f"projective-frame {prefix} optimum")
        require((kernel_demand_ratio(kprime) > optimum) is closed, f"projective-frame {prefix} sign")
        require(all(number > 0 for number in allocation), f"projective-frame {prefix} support")
        require(all(number > 0 for number in cap_dual.values()), f"projective-frame {prefix} dual")
        require(branches[:3] == projective_frame_cut["active_individual_cap_branches"], f"projective-frame {prefix} branches")
        require(tight == projective_frame_cut["tight_hierarchy_rows"], f"projective-frame {prefix} tight")
    require(projective_frame_cut["endpoint_gap"] == 1063274038253455766288412818872693782800681544679740581002823089126086, "projective-frame endpoint gap")
    require(projective_frame_cut["wall_excess"] == 670721678337441589385303494237372283642375643589068751593971045368244, "projective-frame wall excess")
    scope = value["kernel_projective_paving_scope_repair"]
    require(scope["status"] == "proved", "projective scope status")
    require(scope["audit_corank2_cap"] == 253238254, "integer-gap M2")
    require(scope["audit_corank3_cap"] == 3935391907, "integer-gap M3")
    require(scope["uniform_corank2_cap"] == 84416263, "uniform M2 value")
    require(scope["uniform_corank2_cap_proved"] is True, "uniform M2 scope")
    require(scope["uniform_corank3_cap"] == 983902549, "uniform M3 value")
    require(scope["uniform_corank3_cap_proved"] is True, "uniform M3 scope")
    require(scope["unconditional_kernel_closed_through_K_prime"] == 796598, "unconditional kernel scope")
    require(value["claims"]["kernel_uniform_corank3_cap_proved"] is True, "uniform M3 claim")
    weighted_extension = value["kernel_shortening_weighted_extension_cap"]
    require(weighted_extension["status"] == "proved", "shortening-weighted extension status")
    require(weighted_extension["complete_record_caps"] == SHORTENING_WEIGHTED_COMPLETE_CAPS, "shortening-weighted complete caps")
    require(weighted_extension["uniform_coranks"] == [1, 2, 3], "shortening-weighted uniform coranks")
    require(weighted_extension["noncomplete_coranks"] == list(range(4, 10)), "shortening-weighted noncomplete coranks")
    dominance_checks = 0
    ratio_checks = 0
    s_min, s_max = 796599 - 10, 1048576 - 10
    for dimension in range(4, 10):
        t1 = shortening_weighted_f_value(dimension, 1)
        require(
            weighted_extension["t1_F_fractions"][str(dimension)]
            == [t1.numerator, t1.denominator],
            f"shortening-weighted F1 d={dimension}",
        )
        require(
            t1 * comb(s_min - 1, dimension + 1)
            > SHORTENING_WEIGHTED_COMPLETE_CAPS[dimension - 1] * comb(s_min, dimension + 1),
            f"shortening-weighted t1 dominance d={dimension}",
        )
        dominance_checks += 1
        for s_value in (s_min, (s_min + s_max) // 2, s_max):
            for t_value in (1, max(1, (s_value - dimension - 1) // 2), s_value - dimension - 2):
                if t_value < s_value - dimension - 1:
                    ratio = shortening_weighted_ratio(s_value + 10, dimension, t_value)
                    require(0 < ratio < 1, f"shortening-weighted ratio d={dimension}")
                    ratio_checks += 1
    require(dominance_checks == weighted_extension["dominance_checks"] == 6, "shortening-weighted dominance count")
    require(ratio_checks == weighted_extension["ratio_checks"] == 54, "shortening-weighted ratio count")
    weighted_cut = value["kernel_shortening_weighted_capacity_cut"]
    require(weighted_cut["status"] == "proved" and weighted_cut["premises"] == [], "shortening-weighted cut status")
    require(
        (weighted_cut["previous_closed_K_prime"], weighted_cut["replay_K_prime_minimum"], weighted_cut["closed_K_prime_maximum"])
        == (796598, 796599, 1048576),
        "shortening-weighted interval",
    )
    newton = shortening_weighted_newton_coefficients()
    require(len(newton) == weighted_cut["positive_newton_coefficients"] == 12, "shortening-weighted Newton count")
    require(all(value > 0 for value in newton), "shortening-weighted Newton signs")
    require(fraction_vector_digest(newton) == weighted_cut["newton_vector_sha256"], "shortening-weighted Newton digest")
    for prefix, kprime in (("start", 796599), ("endpoint", 1048576)):
        current_gap = shortening_weighted_gap(kprime)
        require(
            weighted_cut[f"{prefix}_gap"] == [current_gap.numerator, current_gap.denominator],
            f"shortening-weighted {prefix} gap",
        )
    require(value["claims"]["kernel_dominant_lane_closed_through_Kprime"] == 1048576, "kernel claim")
    require(value["claims"]["kernel_fixed_lane_closed"] is True, "fixed-kernel closure claim")
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
    rank8_fence = value["rank8_fixed_chart_local_cap_fence"]
    require(rank8_fence == {
        "residual_K_prime": 11,
        "residual_n_prime": 1048587,
        "residual_m_prime": 67483,
        "selector_size": 9,
        "selector_rank": 8,
        "kernel_dimension": 2,
        "owner_count": 8,
        "petal_size": 67473,
        "remainder_size": 508794,
        "rich_slope_count": 4070352,
        "selector_record_floor": 2578110,
        "component_extensions_per_record": 2276269128,
        "marked_component_weight": 9265216597693056,
        "weighted_selector_demand": 5869376383979174,
        "forbidden_slope_count": 18,
        "maximum_greedy_forbidden_values": 32562896,
        "base_prime": 2130706433,
        "error_affine_rank_ceiling": 2,
        "lifted_owner_core_deficiency": 1,
    }, "rank-eight fixed-chart fence")
    require(
        rank8_fence["selector_size"]
        + rank8_fence["owner_count"] * rank8_fence["petal_size"]
        + rank8_fence["remainder_size"]
        == rank8_fence["residual_n_prime"],
        "rank-eight fence partition",
    )
    require(
        rank8_fence["rich_slope_count"] > rank8_fence["selector_record_floor"],
        "rank-eight distinct fence",
    )
    require(
        rank8_fence["marked_component_weight"]
        == rank8_fence["rich_slope_count"] * comb(rank8_fence["petal_size"], 2)
        > rank8_fence["weighted_selector_demand"],
        "rank-eight weighted fence",
    )
    require(
        rank8_fence["base_prime"] > rank8_fence["maximum_greedy_forbidden_values"],
        "rank-eight greedy field budget",
    )
    require(
        value["claims"]["rank8_fixed_chart_output_suffices_for_payment"] is False,
        "rank-eight local-payment claim",
    )
    rank8_minimal = value["rank8_minimal_shortening_exclusion"]
    require(rank8_minimal == {
        "residual_K_prime": 10,
        "ambient_RS_dimension": 10,
        "correction_space_dimension": 10,
        "selector_size": 9,
        "selector_rank": 9,
        "excluded_selector_rank": 8,
        "interpolation_degree_ceiling": 8,
        "first_uncovered_K_prime": 11,
    }, "rank-eight minimal-shortening exclusion")
    require(
        rank8_minimal["residual_K_prime"]
        == rank8_minimal["ambient_RS_dimension"]
        == rank8_minimal["correction_space_dimension"],
        "rank-eight minimal dimension equality",
    )
    require(
        rank8_minimal["selector_rank"] == rank8_minimal["selector_size"]
        and rank8_minimal["excluded_selector_rank"] + 1 == rank8_minimal["selector_rank"],
        "rank-eight minimal selector exclusion",
    )
    require(
        value["claims"]["rank8_minimal_shortening_closed_K_prime"] == 10,
        "rank-eight minimal closure claim",
    )
    circuit = value["rank8_codimension_one_circuit_shadow_census"]
    circuit_sizes = list(range(2, 10))
    require(circuit == {
        "residual_K_prime": 11,
        "ambient_RS_dimension": 11,
        "correction_space_dimension": 10,
        "selector_size": 9,
        "selector_rank": 8,
        "selector_kernel_dimension": 2,
        "empty_global_common_support": True,
        "fixed_chart_record_floor": 2578110,
        "minimum_distinct_slopes_for_loop_exclusion": 2,
        "circuit_sizes": circuit_sizes,
        "rank8_shadow_counts": [comb(11 - c, 2) for c in circuit_sizes],
        "rank9_shadow_counts": [55 - comb(11 - c, 2) for c in circuit_sizes],
        "rank10_basis_counts": circuit_sizes,
        "locator_ideal_dimensions": [11 - c for c in circuit_sizes],
        "eight_petal_circuit_size": 9,
    }, "rank-eight codimension-one circuit-shadow census")
    require(
        all(left + right == 55 for left, right in zip(
            circuit["rank8_shadow_counts"], circuit["rank9_shadow_counts"]
        )),
        "rank-eight 55-shadow partition",
    )
    require(
        value["claims"]["rank8_Kprime11_fixed_circuit_census_proved"] is True,
        "rank-eight fixed-circuit claim",
    )
    return {
        **dense,
        "component_ppb": component["component_incidence_ppb_floor"],
        "cell_cap": value["rank9_split_pencil_cell"]["sharp_fixed_cell_record_cap"],
        "plane_cap": value["rank9_split_pencil_paircore"]["low_common_core_plane_cap"],
        "selector_records": value["component_ninesubset_concentrator"]["fixed_selector_record_floor"],
        "local_fence_slopes": fence["rich_slope_count"],
        "rank8_local_fence_slopes": rank8_fence["rich_slope_count"],
        "rank8_local_fence_weighted_excess": (
            rank8_fence["marked_component_weight"]
            - rank8_fence["weighted_selector_demand"]
        ),
        "rank8_minimal_closed_kprime": rank8_minimal["residual_K_prime"],
        "rank8_circuit_sizes": len(circuit_sizes),
        "weighted_demand": weighted_elimination["first_closed_demand"],
        "weighted_cap": weighted_elimination["first_closed_cap"],
        "minimal_split_capacity": minimal_split_payment["total_capacity"],
        "minimal_split_demand": minimal_split_payment["weighted_demand"],
        "minimal_split_gap": minimal_split_payment["demand_capacity_gap"],
        "minimal_split_clean_checks": clean_inequality_checks,
        "k11_chart_cap": k11_chart,
        "k11_gap": k11_payment["demand_capacity_gap"],
        "k11_offset_checks": offset_partition_checks,
        "k12_chart_cap": k12_chart,
        "k12_gap": k12_payment["demand_capacity_gap"],
        "k12_sparse_cap": k12_low_per_record,
        "k13_chart_cap": k13_chart,
        "k13_gap": k13_payment["demand_capacity_gap"],
        "k13_sparse_cap": sparse_cap,
        "joint_sparse_rows": len(joint_rows),
        "k21_joint_gap": joint_rows[-1]["demand_capacity_gap"],
        "k22_joint_excess": -wall["demand_capacity_gap"],
        "k22_refined_gap": k22_refined_payment["demand_capacity_gap"],
        "k23_refined_gap": k23_refined_payment["demand_capacity_gap"],
        "full_deficit_rows": 17,
        "k40_full_deficit_gap": full_rows["40"]["demand_capacity_gap"],
        "k41_full_deficit_excess": full_deficit_payment["K41_method_wall"]["capacity_excess"],
        "k41_sharp_gap": k41_sharp["gap"],
        "k42_sharp_excess": k41_sharp["K42_capacity_excess"],
        "k42_cross_support_gap": k42_cross_support["gap"],
        "k43_cross_support_excess": k42_cross_support["K43_method_wall"]["capacity_excess"],
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
        "two_step_hierarchy_checks": hierarchy_checks,
        "two_step_checks": two_step_checks + 1,
        "two_step_endpoint_gap": two_step_cut["endpoint_gap"],
        "two_step_wall_excess": two_step_cut["wall_excess"],
        "multistep_hierarchy_checks": multistep_hierarchy_checks,
        "multistep_checks": multistep_checks + 1,
        "multistep_endpoint_gap": multistep_cut["endpoint_gap"],
        "multistep_wall_excess": multistep_cut["wall_excess"],
        "projective_pair_record_cap": projective_cap["record_cap"],
        "projective_pair_checks": len(projective_rows),
        "projective_pair_endpoint_gap": projective_cut["endpoint_gap"],
        "projective_pair_wall_excess": projective_cut["wall_excess"],
        "projective_basis_record_cap": projective_basis_cap["record_cap"],
        "projective_basis_checks": len(projective_basis_rows),
        "projective_basis_endpoint_gap": projective_basis_cut["endpoint_gap"],
        "projective_basis_wall_excess": projective_basis_cut["wall_excess"],
        "projective_frame_record_cap": projective_frame_cap["record_cap"],
        "uniform_projective_frame_record_cap": uniform_frame_cap["uniform_record_cap"],
        "rank4_recurrence_checks": rank4_recurrence_checks,
        "projective_frame_checks": len(projective_frame_rows),
        "projective_frame_endpoint_gap": projective_frame_cut["endpoint_gap"],
        "projective_frame_wall_excess": projective_frame_cut["wall_excess"],
        "shortening_weighted_dominance_checks": dominance_checks,
        "shortening_weighted_ratio_checks": ratio_checks,
        "shortening_weighted_newton_checks": len(newton),
        "rank8_last_gap": rank8_cut["last_open_gap"],
        "rank8_first_gap": rank8_cut["first_closed_gap"],
        "dense_owner_first_excess": dense_owner["first_forced_excess"],
    }


def tamper_selftest(reference: dict[str, Any]) -> int:
    wanted = expected()
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
        lambda item: item["rank9_weighted_component_cap"].__setitem__("boundary_cap", 92395178310909599),
        lambda item: item["rank9_weighted_target_elimination"].__setitem__("first_closed_gap", 2403530864990),
        lambda item: item["rank9_residual_petal_capacity_cut"].__setitem__("first_closed_gap", 3381772318664),
        lambda item: item["rank9_exact_petal_partition_capacity_cut"]["endpoint_gaps"].__setitem__(1, 676268726),
        lambda item: item["weighted_split_pencil_selected_support_cap"].__setitem__("heavy_threshold_formula", "floor(A/2)"),
        lambda item: item["rank9_minimal_shortening_split_pencil_payment"].__setitem__("total_capacity", 9274769506943786),
        lambda item: item["rank9_minimal_shortening_split_pencil_payment"].__setitem__("component_density_numerator", 495405467),
        lambda item: item["weighted_split_pencil_core_offset_cap"]["K11_specializations"][1].__setitem__("total_cap", 9275866238180029),
        lambda item: item["rank11_k11_circuit_split_pencil_payment"].__setitem__("minimum_high_circuit_rank9_shadows", 44),
        lambda item: item["rank11_k11_circuit_split_pencil_payment"].__setitem__("low_circuit_support_coalesces", False),
        lambda item: item["rank11_k11_circuit_split_pencil_payment"].__setitem__("record_coefficient_cross", 0),
        lambda item: item["codimension_two_quotient_line_sparse_circuit_cap"]["support_label_caps"].__setitem__("2", 134967),
        lambda item: item["codimension_two_quotient_line_sparse_circuit_cap"].__setitem__("per_record_sparse_incidence_cap", 0),
        lambda item: item["rank11_k12_quotient_line_circuit_payment"].__setitem__("kernel_incidence_cap", 0),
        lambda item: item["rank11_k12_quotient_line_circuit_payment"].__setitem__("minimum_high_circuit_rank9_shadows", 44),
        lambda item: item["rank11_k12_quotient_line_circuit_payment"].__setitem__("record_coefficient_cross", 0),
        lambda item: item["codimension_three_sparse_circuit_completion_cap"].__setitem__("completion_ceiling", 4),
        lambda item: item["codimension_three_sparse_circuit_completion_cap"].__setitem__("structured_carrier_cap", 0),
        lambda item: item["codimension_three_sparse_circuit_completion_cap"]["unstructured_support_terms"].__setitem__("4", 0),
        lambda item: item["rank11_k13_sparse_circuit_completion_payment"]["kernel_record_caps"].__setitem__(1, 0),
        lambda item: item["rank11_k13_sparse_circuit_completion_payment"].__setitem__("kernel_incidence_cap", 0),
        lambda item: item["rank11_k13_sparse_circuit_completion_payment"].__setitem__("minimum_high_circuit_rank9_shadows", 44),
        lambda item: item["rank11_k13_sparse_circuit_completion_payment"].__setitem__("record_coefficient_cross", 0),
        lambda item: item["sparse_circuit_completion_dimension_ladder"].__setitem__("completion_ceiling_formula", "q+1"),
        lambda item: item["sparse_circuit_completion_dimension_ladder"]["endpoint_totals"]["21"].__setitem__("unstructured", 0),
        lambda item: item["rank9_sparse_shadow_joint_ledger"]["rank9_shadow_counts"].__setitem__(0, 18),
        lambda item: item["rank9_sparse_shadow_joint_ledger"]["premium_weights"].__setitem__(3, 6),
        lambda item: item["rank11_k14_k21_sparse_shadow_payment"]["rows"][7].__setitem__("demand_capacity_gap", 0),
        lambda item: item["rank11_k14_k21_sparse_shadow_payment"]["rows"][0].__setitem__("kernel_incidence_cap", 0),
        lambda item: item["rank11_k14_k21_sparse_shadow_payment"]["K22_method_wall"].__setitem__("capacity_excess", 0),
        lambda item: item["weighted_split_pencil_integral_heavy_cap"]["clean_caps"].__setitem__("21", 0),
        lambda item: item["sparse_circuit_near_saturation_carrier"]["K22"]["active_caps"].__setitem__("3", 0),
        lambda item: item["rank11_k22_integral_near_saturation_payment"].__setitem__("demand_capacity_gap", 0),
        lambda item: item["sparse_circuit_completion_defect_hierarchy"]["depths"].__setitem__("2", 8),
        lambda item: item["rank11_k23_completion_defect_payment"].__setitem__("floor_record_raw_cross", 0),
        lambda item: item["sparse_circuit_universal_completion_incidence_cap"]["K24_example"]["incidence_caps"].__setitem__("9", 0),
        lambda item: item["rank9_full_circuit_deficit_ledger"]["deficit_weights"].__setitem__(0, 35),
        lambda item: item["rank11_k24_k40_full_deficit_shadow_payment"]["rows"]["40"].__setitem__("demand_capacity_gap", 0),
        lambda item: item["rank11_k24_k40_full_deficit_shadow_payment"]["K41_method_wall"].__setitem__("capacity_excess", 0),
        lambda item: item["rank_stratified_isolated_incidence_cap"].__setitem__("new_record_isolated_cap_per_tuple", 2),
        lambda item: item["rank11_k41_sharp_isolated_payment"].__setitem__("gap", 0),
        lambda item: item["rank11_k41_sharp_isolated_payment"].__setitem__("K42_capacity_excess", 0),
        lambda item: item["sparse_circuit_cross_support_defect_carrier"]["support5_target_supports"].__setitem__("1", [2, 3, 4]),
        lambda item: item["rank11_k42_cross_support_defect_payment"]["branch_premiums"].__setitem__("fallback", 0),
        lambda item: item["rank11_k42_cross_support_defect_payment"]["K43_method_wall"].__setitem__("capacity_excess", 0),
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
        lambda item: item["kernel_two_step_nine_shadow_hierarchy"]["couplings"][0].__setitem__(4, 2276404074),
        lambda item: item["kernel_two_step_nine_shadow_capacity_cut"].__setitem__("closed_K_prime_maximum", 18102),
        lambda item: item["kernel_multistep_shadow_hierarchy"]["couplings"][7].__setitem__(4, 51200880454901),
        lambda item: item["kernel_three_step_shadow_capacity_cut"].__setitem__("closed_K_prime_maximum", 18159),
        lambda item: item["kernel_corank1_projective_pair_cap"].__setitem__("record_cap", 8147919),
        lambda item: item["kernel_projective_pair_capacity_cut"].__setitem__("closed_K_prime_maximum", 377674),
        lambda item: item["kernel_projective_pair_capacity_cut"].__setitem__("wall_excess", 1089804128361045148874283346879615159892995682385275039289561845322),
        lambda item: item["kernel_corank2_projective_basis_cap"].__setitem__("record_cap", 84416264),
        lambda item: item["matroid_rank3_bounded_parallel_basis_floor"].__setitem__("induction_slack", "a"),
        lambda item: item["kernel_corank2_uniform_projective_basis_cap"].__setitem__("far_endpoint_cap", 84416264),
        lambda item: item["kernel_corank2_projective_capacity_cut"].__setitem__("closed_K_prime_maximum", 568339),
        lambda item: item["kernel_corank2_projective_capacity_cut"].__setitem__("status", "conditional"),
        lambda item: item["kernel_corank2_projective_capacity_cut"].__setitem__("wall_excess", 36180877960369511460476382880286784896208001102094988739728829832799),
        lambda item: item["kernel_corank3_projective_basis_cap"].__setitem__("record_cap", 983902550),
        lambda item: item["matroid_rank4_bounded_point_line_basis_floor"].__setitem__("rank2_flat_ceiling", "a+2"),
        lambda item: item["kernel_corank3_uniform_projective_basis_cap"]["adjacent_row"].__setitem__("record_cap", 983902550),
        lambda item: item["kernel_corank3_projective_capacity_cut"].__setitem__("status", "conditional"),
        lambda item: item["kernel_corank3_projective_capacity_cut"].__setitem__("closed_K_prime_maximum", 796599),
        lambda item: item["kernel_projective_paving_scope_repair"].__setitem__("audit_corank2_cap", 84416263),
        lambda item: item["kernel_corank3_projective_capacity_cut"].__setitem__("wall_excess", 670721678337441589385303494237372283642375643589068751593971045368243),
        lambda item: item["kernel_shortening_weighted_extension_cap"]["complete_record_caps"].__setitem__(3, 12232092308),
        lambda item: item["kernel_shortening_weighted_extension_cap"]["t1_F_fractions"]["4"].__setitem__(0, 1),
        lambda item: item["kernel_shortening_weighted_capacity_cut"].__setitem__("replay_K_prime_minimum", 796600),
        lambda item: item["kernel_shortening_weighted_capacity_cut"].__setitem__("newton_vector_sha256", "0" * 64),
        lambda item: item["kernel_shortening_weighted_capacity_cut"]["endpoint_gap"].__setitem__(0, 1),
        lambda item: item["claims"].__setitem__("kernel_fixed_lane_closed", False),
        lambda item: item["rank8_owner_pair_weight_cap"].__setitem__("fixed_owner_record_cap", 981104),
        lambda item: item["rank8_weighted_capacity_cut"].__setitem__("first_closed_K_prime", 37995),
        lambda item: item["rank8_dense_owner_terminal_bridge"].__setitem__("owner_record_floor", 200631),
        lambda item: item["claims"].__setitem__("rank8_dense_owner_terminal_from_Kprime", 22525),
        lambda item: item["rank8_fixed_chart_local_cap_fence"].__setitem__("rich_slope_count", 2578110),
        lambda item: item["rank8_fixed_chart_local_cap_fence"].__setitem__("marked_component_weight", 5869376383979174),
        lambda item: item["rank8_fixed_chart_local_cap_fence"].__setitem__("maximum_greedy_forbidden_values", 2130706433),
        lambda item: item["claims"].__setitem__("rank8_fixed_chart_output_suffices_for_payment", True),
        lambda item: item["rank8_minimal_shortening_exclusion"].__setitem__("correction_space_dimension", 9),
        lambda item: item["rank8_minimal_shortening_exclusion"].__setitem__("selector_rank", 8),
        lambda item: item["claims"].__setitem__("rank8_minimal_shortening_closed_K_prime", 11),
        lambda item: item["rank8_codimension_one_circuit_shadow_census"].__setitem__("selector_kernel_dimension", 3),
        lambda item: item["rank8_codimension_one_circuit_shadow_census"]["rank8_shadow_counts"].__setitem__(0, 35),
        lambda item: item["rank8_codimension_one_circuit_shadow_census"]["locator_ideal_dimensions"].__setitem__(7, 1),
        lambda item: item["claims"].__setitem__("rank8_Kprime11_fixed_circuit_census_proved", False),
        lambda item: item["claims"].__setitem__("fixed_chart_output_suffices_for_payment", True),
        lambda item: item["claims"].__setitem__("full_rank_star_owner_is_record_intrinsic", False),
        lambda item: item["claims"].__setitem__("rank9_fixed_target_eliminated_from_Kprime", 15636),
        lambda item: item["claims"].__setitem__("rank9_minimal_shortening_closed_K_prime", 11),
        lambda item: item["claims"].__setitem__("rank9_k11_circuit_split_pencil_closed_K_prime", 10),
        lambda item: item["claims"].__setitem__("rank9_k12_quotient_line_circuit_closed_K_prime", 11),
        lambda item: item["claims"].__setitem__("rank9_k13_sparse_circuit_completion_closed_K_prime", 12),
        lambda item: item["claims"].__setitem__("rank9_k14_k21_sparse_shadow_closed_K_prime", 20),
        lambda item: item["claims"].__setitem__("rank9_k24_k40_full_deficit_shadow_closed_K_prime", 39),
        lambda item: item["claims"].__setitem__("rank9_k41_sharp_isolated_closed_K_prime", 40),
        lambda item: item["claims"].__setitem__("rank9_k42_cross_support_defect_closed_K_prime", 41),
        lambda item: item["claims"].__setitem__("rank9_remaining_interval", [10, 15528]),
        lambda item: item["claims"].__setitem__("rank9_low_shortening_reopened", False),
        lambda item: item["claims"].__setitem__("incidence_is_record_count", True),
        lambda item: item["claims"].__setitem__("rank11_paid", True),
        lambda item: item["source_prize_dag"]["nodes"]["component_star"].__setitem__("commit", "0" * 40),
    )
    caught = 0
    for mutation in mutations:
        changed = copy.deepcopy(reference)
        mutation(changed)
        try:
            validate(changed, wanted)
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
    uniform_maximum, uniform_first_maximizer, uniform_first_excess = scan_uniform_corank3()
    require(
        (uniform_maximum, uniform_first_maximizer, uniform_first_excess)
        == (983902549, 0, -1),
        "uniform corank-three all-row scan",
    )
    print(
        "KB_MCA_RANK11_DENSE_LOCATOR_SPLIT_PENCIL_V1_PASS "
        f"roots={result['roots']} high_rank={result['high_rank']} "
        f"component_ppb={result['component_ppb']} cell_cap={result['cell_cap']} "
        f"plane_cap={result['plane_cap']} "
        f"selector_records={result['selector_records']} "
        f"local_fence_slopes={result['local_fence_slopes']} "
        f"rank8_local_fence_slopes={result['rank8_local_fence_slopes']} "
        f"rank8_local_fence_weighted_excess={result['rank8_local_fence_weighted_excess']} "
        f"rank8_minimal_closed_kprime={result['rank8_minimal_closed_kprime']} "
        f"rank8_circuit_sizes={result['rank8_circuit_sizes']} "
        f"weighted_demand={result['weighted_demand']} "
        f"weighted_cap={result['weighted_cap']} "
        f"minimal_split_capacity={result['minimal_split_capacity']} "
        f"minimal_split_demand={result['minimal_split_demand']} "
        f"minimal_split_gap={result['minimal_split_gap']} "
        f"minimal_split_clean_checks={result['minimal_split_clean_checks']} "
        f"k11_chart_cap={result['k11_chart_cap']} "
        f"k11_gap={result['k11_gap']} "
        f"k11_offset_checks={result['k11_offset_checks']} "
        f"k12_chart_cap={result['k12_chart_cap']} "
        f"k12_sparse_cap={result['k12_sparse_cap']} "
        f"k12_gap={result['k12_gap']} "
        f"k13_chart_cap={result['k13_chart_cap']} "
        f"k13_sparse_cap={result['k13_sparse_cap']} "
        f"k13_gap={result['k13_gap']} "
        f"joint_sparse_rows={result['joint_sparse_rows']} "
        f"k21_joint_gap={result['k21_joint_gap']} "
        f"k22_joint_excess={result['k22_joint_excess']} "
        f"k22_refined_gap={result['k22_refined_gap']} "
        f"k23_refined_gap={result['k23_refined_gap']} "
        f"full_deficit_rows={result['full_deficit_rows']} "
        f"k40_full_deficit_gap={result['k40_full_deficit_gap']} "
        f"k41_full_deficit_excess={result['k41_full_deficit_excess']} "
        f"k41_sharp_gap={result['k41_sharp_gap']} "
        f"k42_sharp_excess={result['k42_sharp_excess']} "
        f"k42_cross_support_gap={result['k42_cross_support_gap']} "
        f"k43_cross_support_excess={result['k43_cross_support_excess']} "
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
        f"two_step_hierarchy_checks={result['two_step_hierarchy_checks']} "
        f"two_step_checks={result['two_step_checks']} "
        f"two_step_endpoint_gap={result['two_step_endpoint_gap']} "
        f"two_step_wall_excess={result['two_step_wall_excess']} "
        f"multistep_hierarchy_checks={result['multistep_hierarchy_checks']} "
        f"multistep_checks={result['multistep_checks']} "
        f"multistep_endpoint_gap={result['multistep_endpoint_gap']} "
        f"multistep_wall_excess={result['multistep_wall_excess']} "
        f"projective_pair_record_cap={result['projective_pair_record_cap']} "
        f"projective_pair_checks={result['projective_pair_checks']} "
        f"projective_pair_endpoint_gap={result['projective_pair_endpoint_gap']} "
        f"projective_pair_wall_excess={result['projective_pair_wall_excess']} "
        f"projective_basis_record_cap={result['projective_basis_record_cap']} "
        f"projective_basis_checks={result['projective_basis_checks']} "
        f"projective_basis_endpoint_gap={result['projective_basis_endpoint_gap']} "
        f"projective_basis_wall_excess={result['projective_basis_wall_excess']} "
        f"projective_frame_record_cap={result['projective_frame_record_cap']} "
        f"uniform_projective_frame_record_cap={result['uniform_projective_frame_record_cap']} "
        f"uniform_projective_frame_rows=1048567 "
        f"rank4_recurrence_checks={result['rank4_recurrence_checks']} "
        f"projective_frame_checks={result['projective_frame_checks']} "
        f"projective_frame_endpoint_gap={result['projective_frame_endpoint_gap']} "
        f"projective_frame_wall_excess={result['projective_frame_wall_excess']} "
        f"shortening_weighted_dominance_checks={result['shortening_weighted_dominance_checks']} "
        f"shortening_weighted_ratio_checks={result['shortening_weighted_ratio_checks']} "
        f"shortening_weighted_newton_checks={result['shortening_weighted_newton_checks']} "
        f"rank8_last_gap={result['rank8_last_gap']} "
        f"rank8_first_gap={result['rank8_first_gap']} "
        f"dense_owner_first_excess={result['dense_owner_first_excess']} "
        f"controls={controls} manifest_sha256={hashlib.sha256(MANIFEST.read_bytes()).hexdigest()}"
    )


if __name__ == "__main__":
    main()
