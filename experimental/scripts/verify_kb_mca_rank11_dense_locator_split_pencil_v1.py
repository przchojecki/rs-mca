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
        "claims": {
            "local_theorem_packet": True,
            "incidence_is_record_count": False,
            "cross_cell_census": False,
            "fixed_chart_output_suffices_for_payment": False,
            "full_rank_star_owner_is_record_intrinsic": True,
            "rank9_fixed_target_eliminated": True,
            "kernel_dominant_lane_closed_through_Kprime": 1048576,
            "kernel_fixed_lane_closed": True,
            "kernel_uniform_corank2_cap_proved": True,
            "kernel_uniform_corank3_cap_proved": True,
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
