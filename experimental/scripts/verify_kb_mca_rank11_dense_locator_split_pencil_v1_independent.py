#!/usr/bin/env python3
"""Independent replay of the rank-11 component and split-pencil constants."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import combinations
from math import comb, factorial, isqrt, prod
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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def ceiling(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def short_fall(value: int, length: int) -> int:
    return prod(value - offset for offset in range(length))


def short_rise(value: int, length: int) -> int:
    return prod(value + offset for offset in range(length))


def independent_weighted_f1(dimension: int) -> Fraction:
    return Fraction(
        short_fall(1048577 + dimension, dimension + 1),
        (67473 + dimension) * short_rise(67473, dimension - 1),
    )


def independent_weighted_gap(kprime: int, extension: dict[str, object]) -> Fraction:
    s_value = kprime - 10
    complete_caps = extension["complete_record_caps"]
    capacity = Fraction(0)
    for dimension in range(1, 10):
        record_extension = (
            Fraction(complete_caps[dimension - 1] * comb(s_value, dimension + 1))
            if dimension <= 3
            else independent_weighted_f1(dimension) * comb(s_value - 1, dimension + 1)
        )
        capacity += Fraction(comb(1048576 + kprime, 10 - dimension), dimension + 2) * record_extension
    demand = Fraction(
        274980728111260126 * 495405467 * comb(67472 + kprime, 11),
        10**9,
    )
    return demand - capacity


def polynomial_multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0) for _ in range(len(left) + len(right) - 1)]
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] += left_value * right_value
    return result


def polynomial_add(
    left: list[Fraction],
    right: list[Fraction],
    scale: Fraction = Fraction(1),
) -> list[Fraction]:
    return [
        (left[index] if index < len(left) else 0)
        + scale * (right[index] if index < len(right) else 0)
        for index in range(max(len(left), len(right)))
    ]


def shifted_binomial_polynomial(anchor: int, degree: int) -> list[Fraction]:
    result = [Fraction(1)]
    for offset in range(degree):
        result = polynomial_multiply(result, [Fraction(anchor - offset), Fraction(1)])
    return [value / factorial(degree) for value in result]


def fraction_vector_digest(values: list[Fraction]) -> str:
    payload = json.dumps(
        [[value.numerator, value.denominator] for value in values],
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def independent_weighted_shifted_polynomial(
    extension: dict[str, object],
    start: int = 796599,
) -> list[Fraction]:
    density = Fraction(274980728111260126 * 495405467, 10**9)
    polynomial = [value * density for value in shifted_binomial_polynomial(67472 + start, 11)]
    complete_caps = extension["complete_record_caps"]
    s_start = start - 10
    for dimension in range(1, 10):
        bases = shifted_binomial_polynomial(1048576 + start, 10 - dimension)
        extensions = shifted_binomial_polynomial(
            s_start if dimension <= 3 else s_start - 1,
            dimension + 1,
        )
        multiplier = (
            Fraction(complete_caps[dimension - 1])
            if dimension <= 3
            else independent_weighted_f1(dimension)
        )
        extensions = [value * multiplier for value in extensions]
        capacity = [
            value / (dimension + 2)
            for value in polynomial_multiply(bases, extensions)
        ]
        polynomial = polynomial_add(polynomial, capacity, Fraction(-1))
    return polynomial


def independent_rank4_h(a: int, rank_gap: int) -> int:
    return min((a + 1) // 2, (a + rank_gap) // 4)


def independent_rank4_floor6(a: int, rank_gap: int = 67474) -> int:
    value = 6
    for current in range(4, rank_gap + 1):
        coloop = (a + current - 1) * (current - 1) * (current - 2)
        increment = 3 * (a + current - independent_rank4_h(a, current) - 1) * (current - 2)
        value = min(coloop, value + increment)
    return value


def independent_uniform_corank3_row(t_value: int) -> dict[str, int]:
    floor6 = independent_rank4_floor6(t_value + 1)
    resource = short_fall(1048579 + t_value, 4)
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


def independent_projective_pair_optimum(
    kprime: int,
) -> tuple[Fraction, list[Fraction]]:
    rows = independent_kernel_hybrid_terms(kprime)
    extension = comb(kprime - 10, 2)
    ambient = comb(1048576 + kprime, 9) * 8147918 * extension // 3
    rows[0] = (ambient, rows[0][1], "ambient" if ambient <= rows[0][1] else "record")
    caps = [Fraction(min(left, right), 274980728111260126) for left, right, _ in rows]

    def ratio(step: int, source: int) -> Fraction:
        raising = Fraction(
            comb(source + 2, step) * comb(67472 + source, step),
            comb(kprime - source - 11 + step, step),
        )
        return Fraction(comb(9 - source + step, step), 1) / raising

    factor = {1: Fraction(1), 2: Fraction(1)}
    factor[3] = ratio(2, 3)
    factor[4] = ratio(3, 4)
    factor[5] = factor[3] * ratio(2, 5)
    factor[6] = factor[4] * ratio(2, 6)
    factor[7] = factor[5] * ratio(2, 7)
    factor[8] = factor[6] * ratio(2, 8)
    factor[9] = factor[7] * ratio(2, 9)
    allocation = [
        caps[0] * factor[dimension] if dimension != 2 else caps[1]
        for dimension in range(1, 10)
    ]
    require(all(0 < number <= cap for number, cap in zip(allocation, caps)), f"projective direct caps K={kprime}")
    require(allocation[:2] == caps[:2], f"projective direct roots K={kprime}")
    return sum(allocation, Fraction(0)), allocation


def independent_projective_basis_optimum(
    kprime: int,
) -> tuple[Fraction, list[Fraction]]:
    rows = independent_kernel_hybrid_terms(kprime)
    nprime = 1048576 + kprime
    ambient1 = comb(nprime, 9) * 8147918 * comb(kprime - 10, 2) // 3
    ambient2 = comb(nprime, 8) * 84416263 * comb(kprime - 10, 3) // 4
    rows[0] = (ambient1, rows[0][1], "ambient" if ambient1 <= rows[0][1] else "record")
    rows[1] = (ambient2, rows[1][1], "ambient" if ambient2 <= rows[1][1] else "record")
    caps = [Fraction(min(left, right), 274980728111260126) for left, right, _ in rows]

    def ratio(step: int, source: int) -> Fraction:
        raising = Fraction(
            comb(source + 2, step) * comb(67472 + source, step),
            comb(kprime - source - 11 + step, step),
        )
        return Fraction(comb(9 - source + step, step), 1) / raising

    factor = {1: Fraction(1), 2: Fraction(1)}
    factor[3] = ratio(2, 3)
    factor[4] = ratio(2, 4)
    factor[5] = ratio(3, 5)
    factor[6] = factor[4] * ratio(2, 6)
    factor[7] = factor[5] * ratio(2, 7)
    factor[8] = factor[6] * ratio(2, 8)
    factor[9] = factor[7] * ratio(2, 9)
    allocation = [
        caps[0] * factor[dimension]
        if dimension in (1, 3)
        else caps[1] * factor[dimension]
        for dimension in range(1, 10)
    ]
    require(all(0 < number <= cap for number, cap in zip(allocation, caps)), f"projective-basis direct caps K={kprime}")
    require(allocation[:2] == caps[:2], f"projective-basis direct roots K={kprime}")
    return sum(allocation, Fraction(0)), allocation


def independent_projective_frame_optimum(
    kprime: int,
) -> tuple[Fraction, list[Fraction]]:
    rows = independent_kernel_hybrid_terms(kprime)
    nprime = 1048576 + kprime
    record_caps = (8147918, 84416263, 983902549)
    for index, record_cap in enumerate(record_caps):
        ambient = (
            comb(nprime, 9 - index)
            * record_cap
            * comb(kprime - 10, index + 2)
            // (index + 3)
        )
        rows[index] = (
            ambient,
            rows[index][1],
            "ambient" if ambient <= rows[index][1] else "record",
        )
    caps = [Fraction(min(left, right), 274980728111260126) for left, right, _ in rows]

    def ratio(step: int, source: int) -> Fraction:
        raising = Fraction(
            comb(source + 2, step) * comb(67472 + source, step),
            comb(kprime - source - 11 + step, step),
        )
        return Fraction(comb(9 - source + step, step), 1) / raising

    factor = {dimension: Fraction(1) for dimension in (1, 2, 3)}
    factor[4] = ratio(2, 4)
    for source in range(5, 10):
        factor[source] = ratio(source - 3, source)
    allocation = [
        caps[0]
        if dimension == 1
        else caps[1] * factor[dimension]
        if dimension in (2, 4)
        else caps[2] * factor[dimension]
        for dimension in range(1, 10)
    ]
    require(all(0 < number <= cap for number, cap in zip(allocation, caps)), f"projective-frame direct caps K={kprime}")
    require(allocation[:3] == caps[:3], f"projective-frame direct roots K={kprime}")
    return sum(allocation, Fraction(0)), allocation


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


def rank8_local_fence_toy() -> tuple[int, int, int]:
    field = 1009
    domain = list(range(1, 20))
    selector = domain[:9]
    petals = [domain[9:12], domain[12:15]]
    remainder = domain[15:]
    owner_parameters = [0, 1]

    def u0(x: int) -> int:
        return prod((x - root) % field for root in selector) % field

    vandermonde = prod(
        (selector[j] - selector[i]) % field
        for i in range(8) for j in range(i + 1, 8)
    ) % field
    require(vandermonde != 0, "rank-eight toy selector rank")
    require(all(u0(x) != 0 for x in domain[9:]), "rank-eight toy locator roots")

    r0 = {x: 0 for x in selector}
    r1 = {x: 1 for x in selector}
    for owner, petal in enumerate(petals):
        for x in petal:
            r0[x] = owner * u0(x) % field
            r1[x] = 1

    slopes: set[int] = set()
    records: list[tuple[int, int, int]] = []
    for x in remainder:
        received_value = next(
            value for value in range(field)
            if len({(value - owner * u0(x)) % field for owner in owner_parameters}) == 2
            and all(
                (value - owner * u0(x)) % field not in slopes
                for owner in owner_parameters
            )
        )
        r0[x], r1[x] = received_value, 0
        for owner in owner_parameters:
            slope = (received_value - owner * u0(x)) % field
            slopes.add(slope)
            records.append((owner, x, slope))

    require(len(slopes) == len(records) == 8, "rank-eight toy slopes")
    errors: list[tuple[int, int, list[int]]] = []
    component_checks = 0
    for owner, singled, slope in records:
        support = []
        error = []
        for x in domain:
            explanation = (owner * u0(x) + slope) % field
            line_value = (r0[x] + slope * r1[x]) % field
            error.append((line_value - explanation) % field)
            if line_value == explanation:
                support.append(x)
        require(support == selector + petals[owner] + [singled], "rank-eight toy support")
        require(len(selector) + len(petals[owner]) > 10 and r1[singled] == 0, "rank-eight toy noncontainment")
        for x, y in combinations(petals[owner], 2):
            determinant = u0(x) * u0(y) * (y - x) % field
            require(determinant != 0, "rank-eight toy extension rank")
            require(
                all(r0[z] == owner * u0(z) % field and r1[z] == 1 for z in selector + [x, y]),
                "rank-eight toy component owner",
            )
            component_checks += 1
        errors.append((owner, slope, error))

    anchor_owner, anchor_slope, anchor_error = errors[0]
    for owner, slope, error in errors[1:]:
        predicted = [
            (-(owner - anchor_owner) * u0(x)
             + (slope - anchor_slope) * (r1[x] - 1)) % field
            for x in domain
        ]
        actual = [(left - right) % field for left, right in zip(error, anchor_error)]
        require(actual == predicted, "rank-eight toy error two-space")
    return len(records), len(slopes), component_checks


def rank8_minimal_shortening_toy() -> int:
    field = 103
    points = list(range(2, 11))
    determinant = prod(
        (points[j] - points[i]) % field
        for i in range(len(points)) for j in range(i + 1, len(points))
    ) % field
    require(determinant != 0, "rank-eight minimal Vandermonde")
    return determinant


def rank8_circuit_shadow_toy() -> tuple[int, int, int]:
    field = 107
    points = list(range(2, 13))
    checks = 0
    for circuit_size in range(2, 10):
        weights = list(range(1, circuit_size + 1))
        moments = [
            sum(
                weight * pow(point, degree, field)
                for weight, point in zip(weights, points[:circuit_size])
            ) % field
            for degree in range(11)
        ]
        require(any(moments), f"rank-eight circuit functional c={circuit_size}")
        pivot = next(degree for degree, value in enumerate(moments) if value)
        pivot_inverse = pow(moments[pivot], -1, field)
        for degree in range(11):
            if degree == pivot:
                continue
            pivot_coefficient = -moments[degree] * pivot_inverse % field
            relation = sum(
                weight * (
                    pow(point, degree, field)
                    + pivot_coefficient * pow(point, pivot, field)
                )
                for weight, point in zip(weights, points[:circuit_size])
            ) % field
            require(relation == 0, f"rank-eight hyperplane basis c={circuit_size}")
            checks += 1
        for point in points:
            require(
                any(
                    moments[degree] != moments[0] * pow(point, degree, field) % field
                    for degree in range(11)
                ),
                f"rank-eight loopless toy c={circuit_size}",
            )
            checks += 1
        rank8 = sum(
            set(omitted).isdisjoint(range(circuit_size))
            for omitted in combinations(range(11), 2)
        )
        rank9 = comb(11, 2) - rank8
        bases = sum(omitted < circuit_size for omitted in range(11))
        require(rank8 == comb(11 - circuit_size, 2), f"rank-eight shadows c={circuit_size}")
        require(rank9 == 55 - rank8, f"rank-nine shadows c={circuit_size}")
        require(bases == circuit_size, f"rank-ten bases c={circuit_size}")
        checks += 3
    return field, checks, len(range(2, 10))


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
    kernel_projective_cap = data["kernel_corank1_projective_pair_cap"]
    kernel_projective_cut = data["kernel_projective_pair_capacity_cut"]
    kernel_projective_basis_cap = data["kernel_corank2_projective_basis_cap"]
    matroid_rank3_floor = data["matroid_rank3_bounded_parallel_basis_floor"]
    kernel_projective_basis_uniform = data["kernel_corank2_uniform_projective_basis_cap"]
    kernel_projective_basis_cut = data["kernel_corank2_projective_capacity_cut"]
    kernel_projective_frame_cap = data["kernel_corank3_projective_basis_cap"]
    matroid_rank4_floor = data["matroid_rank4_bounded_point_line_basis_floor"]
    kernel_projective_frame_uniform = data["kernel_corank3_uniform_projective_basis_cap"]
    kernel_projective_frame_cut = data["kernel_corank3_projective_capacity_cut"]
    kernel_projective_scope = data["kernel_projective_paving_scope_repair"]
    kernel_weighted_extension = data["kernel_shortening_weighted_extension_cap"]
    kernel_weighted_cut = data["kernel_shortening_weighted_capacity_cut"]
    rank8_owner_cap = data["rank8_owner_pair_weight_cap"]
    rank8_cut = data["rank8_weighted_capacity_cut"]
    dense_owner = data["rank8_dense_owner_terminal_bridge"]
    rank8_fence = data["rank8_fixed_chart_local_cap_fence"]
    rank8_minimal = data["rank8_minimal_shortening_exclusion"]
    rank8_circuit = data["rank8_codimension_one_circuit_shadow_census"]
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

    projective_n, projective_m = 1048577, 67473
    concentrated_maximum = max(
        (projective_m - classes + 1) ** 2 + classes - 1
        for classes in range(2, projective_m + 1)
    )
    projective_pairs = projective_m**2 - concentrated_maximum
    projective_cap, projective_remainder = divmod(
        projective_n * (projective_n - 1), projective_pairs
    )
    require(kernel_projective_cap == {
        "domain_size": projective_n,
        "code_dimension": 1,
        "support_size": projective_m,
        "explanation_dimension": 1,
        "zero_normal_upper_bound": 0,
        "minimum_projective_classes": 2,
        "minimum_independent_ordered_pairs_per_record": projective_pairs,
        "coordinate_ordered_pair_resource": projective_n * (projective_n - 1),
        "record_cap": projective_cap,
        "division_remainder": projective_remainder,
        "previous_transversality_record_cap": projective_n * (projective_n - 1) // projective_m,
        "record_cap_improvement": projective_n * (projective_n - 1) // projective_m - projective_cap,
        "capacity_formula": "floor(n*(n-1)/(2*(m-1)))",
    }, "projective pair cap")
    require(projective_pairs == 134944 and projective_cap == 8147918, "projective pair arithmetic")
    projective_tree = [[2, 3], [3, 4], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9]]
    projective_tight = [
        [2, 3], [2, 5], [2, 6], [2, 7], [2, 8], [2, 9],
        [3, 4], [3, 6], [3, 7], [3, 8], [3, 9],
        [4, 5], [4, 7], [4, 8], [4, 9],
        [5, 6], [5, 8], [5, 9],
        [6, 7], [6, 9], [7, 8], [8, 9],
    ]
    require(kernel_projective_cut["dual_tree"] == projective_tree, "projective tree")
    require(kernel_projective_cut["tight_hierarchy_rows"] == projective_tight, "projective tight rows")
    require(kernel_projective_cut["checked_rows_including_wall"] == 359516, "projective replay rows")
    require(kernel_projective_cut["source_replay_chunks"] == 64, "projective replay chunks")
    projective_checks = 0
    for prefix, kprime, closed in (
        ("replay_start", 18159, True),
        ("endpoint", 377673, True),
        ("wall", 377674, False),
    ):
        optimum, allocation = independent_projective_pair_optimum(kprime)
        require(optimum == Fraction(kernel_projective_cut[f"{prefix}_optimum_numerator"], kernel_projective_cut[f"{prefix}_optimum_denominator"]), f"projective {prefix} optimum")
        require((independent_kernel_demand_ratio(kprime) > optimum) is closed, f"projective {prefix} sign")
        scaled = 274980728111260126 * optimum
        capacity = scaled.numerator // scaled.denominator
        demand = independent_kernel_demand(kprime)
        require(capacity == kernel_projective_cut[f"{prefix}_capacity"], f"projective {prefix} capacity")
        require(demand == kernel_projective_cut[f"{prefix}_demand"], f"projective {prefix} demand")
        require(all(number > 0 for number in allocation), f"projective {prefix} allocation")
        projective_checks += 1
    require(kernel_projective_cut["endpoint_gap"] == 608290099077401798561583762592584078050381528604243813748500153228, "projective endpoint gap")
    require(kernel_projective_cut["wall_excess"] == 1089804128361045148874283346879615159892995682385275039289561845323, "projective wall excess")

    basis_n, basis_m = 1048578, 67474
    collinear_maximum = max(
        comb(q, 3) + comb(basis_m - q + 1, 3)
        for q in range(2, basis_m)
    )
    projective_bases = basis_m * (basis_m - 1) * (basis_m - 2) - 6 * collinear_maximum
    basis_cap, basis_remainder = divmod(
        basis_n * (basis_n - 1) * (basis_n - 2), projective_bases
    )
    previous_basis_cap, previous_basis_remainder = divmod(
        basis_n * (basis_n - 1) * (basis_n - 2), basis_m * (basis_m - 1)
    )
    require(kernel_projective_basis_cap == {
        "domain_size": basis_n,
        "code_dimension": 2,
        "support_size": basis_m,
        "explanation_dimension": 2,
        "support_excess": 67472,
        "normal_space_dimension": 3,
        "zero_normal_upper_bound": 0,
        "minimum_normals_outside_projective_class": 67473,
        "maximum_projective_class_size": 1,
        "minimum_projective_points": basis_m,
        "noncollinear": True,
        "maximum_collinear_unordered_triples": collinear_maximum,
        "minimum_independent_ordered_triples_per_record": projective_bases,
        "coordinate_ordered_triple_resource": basis_n * (basis_n - 1) * (basis_n - 2),
        "record_cap": basis_cap,
        "division_remainder": basis_remainder,
        "previous_transversality_record_cap": previous_basis_cap,
        "previous_division_remainder": previous_basis_remainder,
        "record_cap_improvement": previous_basis_cap - basis_cap,
        "capacity_formula": "floor(n*(n-1)*(n-2)/(3*(m-1)*(m-2)))",
    }, "projective basis cap")
    require(projective_bases == 13657614768 and basis_cap == 84416263, "projective basis arithmetic")
    require(matroid_rank3_floor == {
        "status": "proved",
        "rank": 3,
        "loopless": True,
        "basis_floor": "2*b(M)>=(m-1)*(m-1-a)",
        "smallest_class_contraction_floor": "b(M/e)>=c*(m-2*c)>=m-2",
        "induction_slack": "a-1",
        "sharp_when": "a divides m-1 and m-1>=2a",
    }, "rank-three matroid floor")
    for m_test in range(3, 65):
        for a_test in range(1, m_test):
            induction_lhs = (m_test - 2) * (m_test - 2 - a_test) + 2 * (m_test - 2)
            induction_target = (m_test - 1) * (m_test - 1 - a_test)
            require(induction_lhs - induction_target == a_test - 1, "matroid induction identity")
        for c_test in range(1, m_test // 3 + 1):
            require(c_test * (m_test - 2 * c_test) >= m_test - 2, "matroid contraction floor")
    def shortened_corank2_cap(t_value: int) -> int:
        numerator = (1048576 + t_value) * (1048577 + t_value) * (1048578 + t_value)
        denominator = 3 * 67472 * (67473 + t_value)
        return numerator // denominator
    require(kernel_projective_basis_uniform == {
        "status": "proved",
        "t_minimum": 0,
        "t_maximum": 1048566,
        "parallel_class_ceiling": "t+1",
        "ordered_basis_floor": "3*67472*(67473+t)",
        "record_cap_formula": "floor((1048576+t)*(1048577+t)*(1048578+t)/(3*67472*(67473+t)))",
        "ratio_step_sign": "2*t+3*67472+3-1048576",
        "turn_left": 423078,
        "turn_right": 423079,
        "complete_cap": shortened_corank2_cap(0),
        "adjacent_cap": shortened_corank2_cap(1),
        "far_endpoint_cap": shortened_corank2_cap(1048566),
        "uniform_record_cap": 84416263,
    }, "uniform projective-basis cap")
    require(shortened_corank2_cap(0) == 84416263, "uniform projective-basis complete arithmetic")
    require(shortened_corank2_cap(1) == 84415253, "uniform projective-basis adjacent arithmetic")
    require(shortened_corank2_cap(1048566) == 40828171, "uniform projective-basis far arithmetic")
    for t_test in (0, 1, 423078, 423079, 1048565):
        left = (1048579 + t_test) * (67473 + t_test)
        right = (1048576 + t_test) * (67474 + t_test)
        require((left > right) == (2 * t_test + 3 * 67472 + 3 - 1048576 > 0), "uniform projective-basis ratio sign")
    require(kernel_projective_basis_cut["status"] == "proved", "projective-basis status")
    projective_basis_tree = [[2, 3], [2, 4], [2, 6], [2, 8], [3, 5], [2, 7], [2, 9]]
    projective_basis_tight = [
        [2, 3], [2, 4], [2, 6], [2, 7], [2, 8], [2, 9],
        [3, 5], [3, 7], [3, 8], [3, 9],
        [4, 6], [4, 8], [4, 9],
        [5, 7], [5, 9], [6, 8], [7, 9],
    ]
    require(kernel_projective_basis_cut["dual_tree"] == projective_basis_tree, "projective-basis tree")
    require(kernel_projective_basis_cut["tight_hierarchy_rows"] == projective_basis_tight, "projective-basis tight rows")
    require(kernel_projective_basis_cut["checked_rows_including_wall"] == 190666, "projective-basis replay rows")
    require(kernel_projective_basis_cut["source_replay_chunks"] == 64, "projective-basis replay chunks")
    projective_basis_checks = 0
    for prefix, kprime, closed in (
        ("replay_start", 377674, True),
        ("endpoint", 568338, True),
        ("wall", 568339, False),
    ):
        optimum, allocation = independent_projective_basis_optimum(kprime)
        require(optimum == Fraction(kernel_projective_basis_cut[f"{prefix}_optimum_numerator"], kernel_projective_basis_cut[f"{prefix}_optimum_denominator"]), f"projective-basis {prefix} optimum")
        require((independent_kernel_demand_ratio(kprime) > optimum) is closed, f"projective-basis {prefix} sign")
        scaled = 274980728111260126 * optimum
        capacity = scaled.numerator // scaled.denominator
        demand = independent_kernel_demand(kprime)
        require(capacity == kernel_projective_basis_cut[f"{prefix}_capacity"], f"projective-basis {prefix} capacity")
        require(demand == kernel_projective_basis_cut[f"{prefix}_demand"], f"projective-basis {prefix} demand")
        require(all(number > 0 for number in allocation), f"projective-basis {prefix} allocation")
        projective_basis_checks += 1
    require(kernel_projective_basis_cut["endpoint_gap"] == 38432453444617070485037263551626410396462586389410416394578520596038, "projective-basis endpoint gap")
    require(kernel_projective_basis_cut["wall_excess"] == 36180877960369511460476382880286784896208001102094988739728829832800, "projective-basis wall excess")

    frame_n, frame_m = 1048579, 67475
    plane_bounds = []
    for q in range(3, frame_m):
        r = frame_m - q
        plane_bounds.append(
            comb(q, 4)
            + (q // 2) * comb(r, 2)
            + 2 * comb(r, 3)
            + comb(r, 4)
        )
    coplanar_maximum = max(plane_bounds)
    plane_maximizers = [q for q, bound in zip(range(3, frame_m), plane_bounds) if bound == coplanar_maximum]
    projective_frames = (
        frame_m * (frame_m - 1) * (frame_m - 2) * (frame_m - 3)
        - 24 * coplanar_maximum
    )
    frame_resource = frame_n * (frame_n - 1) * (frame_n - 2) * (frame_n - 3)
    frame_cap, frame_remainder = divmod(frame_resource, projective_frames)
    previous_frame_cap, previous_frame_remainder = divmod(
        frame_resource,
        frame_m * 67473 * 67474,
    )
    require(plane_maximizers == [3, frame_m - 1], "projective-frame split maximizers")
    require(kernel_projective_frame_cap == {
        "domain_size": frame_n,
        "code_dimension": 3,
        "support_size": frame_m,
        "explanation_dimension": 3,
        "support_excess": 67472,
        "normal_space_dimension": 4,
        "zero_normal_upper_bound": 0,
        "minimum_normals_outside_projective_class": 67474,
        "maximum_projective_class_size": 1,
        "minimum_normals_outside_projective_line": 67473,
        "maximum_projective_line_size": 2,
        "minimum_projective_points": frame_m,
        "spans_projective_space": True,
        "maximum_coplanar_unordered_quadruples": coplanar_maximum,
        "minimum_independent_ordered_quadruples_per_record": projective_frames,
        "coordinate_ordered_quadruple_resource": frame_resource,
        "record_cap": frame_cap,
        "division_remainder": frame_remainder,
        "previous_transversality_record_cap": previous_frame_cap,
        "previous_division_remainder": previous_frame_remainder,
        "record_cap_improvement": previous_frame_cap - frame_cap,
        "capacity_formula": "floor((n)_fall_4/(4*(m-1)*(m-2)*(m-3)))",
    }, "projective frame cap")
    require(projective_frames == 1228711865141376 and frame_cap == 983902549, "projective frame arithmetic")
    require(matroid_rank4_floor == {
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
    }, "rank-four matroid floor")
    uniform_samples = {
        "complete_row": 0,
        "adjacent_row": 1,
        "first_nontrivial_row": 2,
        "middle_row": 1048566 // 2,
        "official_endpoint": 1048566,
    }
    uniform_sample_checks = 0
    for key, t_value in uniform_samples.items():
        direct = independent_uniform_corank3_row(t_value)
        require(kernel_projective_frame_uniform[key] == direct, f"uniform projective-frame {key}")
        require(direct["next_integer_gap"] > 0, f"uniform projective-frame {key} gap")
        uniform_sample_checks += len(direct)
    require(kernel_projective_frame_uniform["status"] == "proved", "uniform projective-frame status")
    require(kernel_projective_frame_uniform["rank_gap"] == 67474, "uniform projective-frame rank gap")
    require(kernel_projective_frame_uniform["parallel_class_ceiling"] == "t+1", "uniform projective-frame point ceiling")
    require(kernel_projective_frame_uniform["rank2_flat_ceiling"] == "t+2", "uniform projective-frame line ceiling")
    require(kernel_projective_frame_uniform["uniform_record_cap"] == 983902549, "uniform projective-frame cap")
    require(kernel_projective_frame_uniform["checked_rows"] == 1048567, "uniform projective-frame rows")
    require(kernel_projective_frame_uniform["first_maximizer"] == 0, "uniform projective-frame maximizer")
    require(kernel_projective_frame_uniform["first_excess"] is None, "uniform projective-frame excess")
    require(kernel_projective_frame_cut["status"] == "proved", "projective-frame status")
    require(kernel_projective_frame_cut["premises"] == [], "projective-frame premises")
    projective_frame_forest = [[2, 4], [2, 5], [3, 6], [4, 7], [5, 8], [6, 9]]
    projective_frame_tight = [
        [2, 4], [2, 5], [2, 7], [2, 8], [2, 9],
        [3, 6], [3, 8], [3, 9],
        [4, 7], [4, 9], [5, 8], [6, 9],
    ]
    require(kernel_projective_frame_cut["dual_forest"] == projective_frame_forest, "projective-frame forest")
    require(kernel_projective_frame_cut["tight_hierarchy_rows"] == projective_frame_tight, "projective-frame tight rows")
    require(kernel_projective_frame_cut["checked_rows_including_wall"] == 228261, "projective-frame replay rows")
    require(kernel_projective_frame_cut["source_replay_chunks"] == 64, "projective-frame replay chunks")
    projective_frame_checks = 0
    for prefix, kprime, closed in (
        ("replay_start", 568339, True),
        ("endpoint", 796598, True),
        ("wall", 796599, False),
    ):
        optimum, allocation = independent_projective_frame_optimum(kprime)
        require(optimum == Fraction(kernel_projective_frame_cut[f"{prefix}_optimum_numerator"], kernel_projective_frame_cut[f"{prefix}_optimum_denominator"]), f"projective-frame {prefix} optimum")
        require((independent_kernel_demand_ratio(kprime) > optimum) is closed, f"projective-frame {prefix} sign")
        scaled = 274980728111260126 * optimum
        capacity = scaled.numerator // scaled.denominator
        demand = independent_kernel_demand(kprime)
        require(capacity == kernel_projective_frame_cut[f"{prefix}_capacity"], f"projective-frame {prefix} capacity")
        require(demand == kernel_projective_frame_cut[f"{prefix}_demand"], f"projective-frame {prefix} demand")
        require(all(number > 0 for number in allocation), f"projective-frame {prefix} allocation")
        projective_frame_checks += 1
    require(kernel_projective_frame_cut["endpoint_gap"] == 1063274038253455766288412818872693782800681544679740581002823089126086, "projective-frame endpoint gap")
    require(kernel_projective_frame_cut["wall_excess"] == 670721678337441589385303494237372283642375643589068751593971045368244, "projective-frame wall excess")
    require(kernel_projective_scope == {
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
    }, "projective paving scope")

    require(kernel_weighted_extension["status"] == "proved", "shortening-weighted extension status")
    require(kernel_weighted_extension["uniform_coranks"] == [1, 2, 3], "shortening-weighted uniform coranks")
    require(kernel_weighted_extension["noncomplete_coranks"] == list(range(4, 10)), "shortening-weighted noncomplete coranks")
    s_min = 796599 - 10
    weighted_dominance_checks = 0
    for dimension in range(4, 10):
        f1 = independent_weighted_f1(dimension)
        require(
            kernel_weighted_extension["t1_F_fractions"][str(dimension)]
            == [f1.numerator, f1.denominator],
            f"shortening-weighted F1 d={dimension}",
        )
        require(
            f1 * comb(s_min - 1, dimension + 1)
            > kernel_weighted_extension["complete_record_caps"][dimension - 1] * comb(s_min, dimension + 1),
            f"shortening-weighted dominance d={dimension}",
        )
        weighted_dominance_checks += 1
    weighted_polynomial = independent_weighted_shifted_polynomial(kernel_weighted_extension)
    require(len(weighted_polynomial) == kernel_weighted_cut["positive_shifted_power_coefficients"] == 12, "shortening-weighted power count")
    require(all(value > 0 for value in weighted_polynomial), "shortening-weighted power signs")
    require(
        fraction_vector_digest(weighted_polynomial) == kernel_weighted_cut["shifted_power_vector_sha256"],
        "shortening-weighted power digest",
    )
    for prefix, kprime in (("start", 796599), ("endpoint", 1048576)):
        current_gap = independent_weighted_gap(kprime, kernel_weighted_extension)
        require(
            kernel_weighted_cut[f"{prefix}_gap"] == [current_gap.numerator, current_gap.denominator],
            f"shortening-weighted {prefix} gap",
        )
    require(kernel_weighted_cut["status"] == "proved" and kernel_weighted_cut["premises"] == [], "shortening-weighted cut status")
    require(kernel_weighted_cut["closed_K_prime_maximum"] == 1048576, "shortening-weighted endpoint")

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

    rank8_fence_kprime = 11
    rank8_fence_nprime = 1048576 + rank8_fence_kprime
    rank8_fence_mprime = 67472 + rank8_fence_kprime
    rank8_fence_petal = rank8_fence_mprime - 1 - 9
    rank8_fence_remainder = rank8_fence_nprime - 9 - 8 * rank8_fence_petal
    rank8_fence_slopes = 8 * rank8_fence_remainder
    rank8_fence_extensions = comb(rank8_fence_petal, 2)
    rank8_fence_marked = rank8_fence_slopes * rank8_fence_extensions
    rank8_fence_demand = independent_rank8_demand(rank8_fence_kprime)
    require(rank8_fence == {
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
    }, "rank-eight fixed-chart fence")
    require(rank8_fence_slopes > rank8_fence["selector_record_floor"], "rank-eight distinct fence")
    require(rank8_fence_marked > rank8_fence_demand, "rank-eight weighted fence")
    require(rank8_fence["base_prime"] > rank8_fence["maximum_greedy_forbidden_values"], "rank-eight field budget")
    toy_rank8_records, toy_rank8_slopes, toy_rank8_components = rank8_local_fence_toy()
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
        rank8_minimal["ambient_RS_dimension"] == rank8_minimal["correction_space_dimension"]
        and rank8_minimal["selector_rank"] == rank8_minimal["selector_size"],
        "rank-eight minimal rank exclusion",
    )
    rank8_minimal_determinant = rank8_minimal_shortening_toy()
    circuit_sizes = list(range(2, 10))
    require(rank8_circuit == {
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
    }, "rank-eight circuit-shadow census")
    circuit_field, circuit_checks, circuit_rows = rank8_circuit_shadow_toy()

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
    }, "claim boundary")
    print(
        "KB_MCA_RANK11_DENSE_LOCATOR_SPLIT_PENCIL_V1_INDEPENDENT_PASS "
        f"endpoint={endpoint} records={records} cell_cap={fixed_cell} "
        f"plane_cap={plane_cap} core_checks={core_checks} "
        f"selector_records={selector_records} ninecell_cap={ninecell_cap} "
        f"local_fence_slopes={fence_slopes} "
        f"uniform_projective_frame_sample_checks={uniform_sample_checks} "
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
        f"projective_pair_cap={projective_cap} "
        f"projective_pair_checks={projective_checks} "
        f"projective_pair_endpoint_gap={kernel_projective_cut['endpoint_gap']} "
        f"projective_pair_wall_excess={kernel_projective_cut['wall_excess']} "
        f"projective_basis_cap={basis_cap} "
        f"projective_basis_checks={projective_basis_checks} "
        f"projective_basis_endpoint_gap={kernel_projective_basis_cut['endpoint_gap']} "
        f"projective_basis_wall_excess={kernel_projective_basis_cut['wall_excess']} "
        f"projective_frame_cap={frame_cap} "
        f"projective_frame_checks={projective_frame_checks} "
        f"projective_frame_splits={len(plane_bounds)} "
        f"projective_frame_endpoint_gap={kernel_projective_frame_cut['endpoint_gap']} "
        f"projective_frame_wall_excess={kernel_projective_frame_cut['wall_excess']} "
        f"shortening_weighted_dominance_checks={weighted_dominance_checks} "
        f"shortening_weighted_power_checks={len(weighted_polynomial)} "
        f"rank8_last_gap={rank8_last_cap-rank8_last_demand} "
        f"rank8_first_gap={rank8_first_demand-rank8_first_cap} "
        f"rank8_monotone_factors={monotone_factors} "
        f"dense_owner_first_excess={dense_owner['first_forced_excess']} "
        f"rank8_local_fence_slopes={rank8_fence_slopes} "
        f"rank8_local_fence_weighted_excess={rank8_fence_marked-rank8_fence_demand} "
        f"rank8_toy={toy_rank8_records}/{toy_rank8_slopes}/{toy_rank8_components} "
        f"rank8_minimal_kprime={rank8_minimal['residual_K_prime']} "
        f"rank8_minimal_det={rank8_minimal_determinant} "
        f"rank8_circuit_toy=GF({circuit_field})/{circuit_rows}/{circuit_checks} "
        f"toy_points={points} toy_slopes={slopes} design_pairs={design_pairs}"
    )


if __name__ == "__main__":
    main()
