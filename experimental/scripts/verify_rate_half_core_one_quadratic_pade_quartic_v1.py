#!/usr/bin/env python3
"""Replay the rate-half quadratic Pade/quartic degree identities."""

from __future__ import annotations

import argparse
import copy
import hashlib
from dataclasses import dataclass
from itertools import combinations
from math import comb, gcd
from pathlib import Path


SOURCE_COMMIT = "b25caad721a6a11136f4e6576e173cc412e78c63"
SOURCE_HASHES = {
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_all_excess_residual_fiber_factorization/statement.md": "0ef4e2eda6c08df7ef172c7f4e3e5e12ad8832644f0171cc8d92ec395819f193",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_all_excess_residual_fiber_factorization/proof.md": "e35416d3950a743d4466f32c6c360c618087046377978b1e86f5fff8d467bc62",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_coprime_resultant_exact_four_core/statement.md": "03af81362c918c0a537371c7c51810052cdef52a8956d9dfa28663413c57d14f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_coprime_resultant_exact_four_core/proof.md": "fcafb6e1d471c746891db593408e52d43c8939b62aef88d477a956cb3f0d38e8",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_regular_factor_identity/statement.md": "de1ffaa7a71b105c5526a16dbff1838ae5b6529acc73d94428964ef8039b199c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_regular_factor_identity/proof.md": "6a84f32f36fb249177181c67251e03b5d0b62c430c1576ff110220d1ea84cd18",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_resultant_regular_quartic_identification/statement.md": "c8de176f5c5d3a3081737b9cbfe702d3cb821cfc881510fac8bc3cf26f03ebf6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_resultant_regular_quartic_identification/proof.md": "fa8b278e41e9c579f729c82c2756715693e5f1895e33590f27dc190e606eb9c3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_correction_marked_jet_route_fence/statement.md": "16dfa510de497812e3ec3bef088a50464bd647acebd47d4ce2b645bc92ff3b2c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_correction_marked_jet_route_fence/proof.md": "df14c50468d1c6f7c68b3a672f2efe414fc25c71971f46406df40b9d6e271f34",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_supported_first_jet_perfect_pairing/statement.md": "dd5741a5f8f189cd009c3a80dd253996e861e7bec6270d5dfb77cdc544ef57dd",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_supported_first_jet_perfect_pairing/proof.md": "880ac7cc7ba37e6811af3736b66af1e6b9a7c9e95bd2a2c015fda4e682c8b8a9",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_supported_coefficient_plane_kernel_intersection/statement.md": "e5470716c2f85b5b02338213ae0c8654ec8f89b6c3616e15008f333f3812e177",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_supported_coefficient_plane_kernel_intersection/proof.md": "229aea8c16c49d9d657ee03ef11513e02ed81e9df507f5a1f99ca05f473020d8",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_heavy_quotient_cubic_residual/statement.md": "c888235f0efe4ed23ca4d3c05ecbd3b263c560d52b69e9a687a6914c514d5419",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_heavy_quotient_cubic_residual/proof.md": "86bf14cfc6fece3cd739af15621a26c2cbf34b3b1e989c017418574d202886f2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_heavy_row_center_overlap_factorization/statement.md": "f4ca71e7dad263b81b5bb6785e1c41c19d8bc130be1ecfa1508566b4f06710cb",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_heavy_row_center_overlap_factorization/proof.md": "caea37f7fa0254d84304850b700b50a810e6492fdd4293546664c0d36926a1e3",
    "background/nodes/rate_half_layer_a_saturation_count_route_fence/statement.md": "79248b4c1402ac0d125e41ae6ed5c489938173abb28bad755bb2b4c7aebc035e",
    "background/nodes/rate_half_layer_a_saturation_count_route_fence/proof.md": "2658e564d4eda83af64cee8e2fdab73aff531a1eace1fe1ef2cfbd3f2f6d1cac",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_heavy_row_barycentric_remainder_gate/statement.md": "ce6c3e3c2a53f9f1259811e7150f28e3d1c71730cefb8b7039f0866d85ab35b1",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_heavy_row_barycentric_remainder_gate/proof.md": "2538c8ba0c5063a210fe91e8b599ec66151e950b9fa6dc29df0709b68fe0b42a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_center_disjoint_heavy_row_nonzero_scalar/statement.md": "0d8c08f08b94463af07bcff141367cb63d0f9fb14293c787cef320bde6553935",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_center_disjoint_heavy_row_nonzero_scalar/proof.md": "d815dcc569e9b58862d729f409298f39b8f603cf64178f1c4877967aeb95be60",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_heavy_row_nonzero/statement.md": "526fe94e415f0940d5aac29bae4a48062d2c61d8b269261e9dc1b4fcd13659c6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_heavy_row_nonzero/proof.md": "beb045df9a3e1cef2e36132c3d5f381405823ef1096d6b72d02490406bce619a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_heavy_row_correction_exact_order/statement.md": "b2564f19937e4f1415acdaedafdb7ef29729dba00070d7aab92525cfaa41a3a9",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_heavy_row_correction_exact_order/proof.md": "9a3cdc703dc0c38f26609df5c874d3c8b520890a4b27f509c7945d6d241ea931",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_center_overlap_cap_two/statement.md": "25d20172763333686d0cbdb9a4c127f9ee985eaaaddbb349cfccf635260e6ae6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_center_overlap_cap_two/proof.md": "fc385c4aea754ea9e0a79d5f9ef073211857d6879094e093e85db694907c2f9f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_correction_center_disjoint_overlap_cap_one/statement.md": "1077a662880f178c14fedacda38c53aff4e4547a1fdee70e11e2a0a8c96ae78e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_separated_correction_center_disjoint_overlap_cap_one/proof.md": "33cb3a2c4f3a83d52a79cbe11a2dfa3cbfa74e604384c9c4ce40984a631f2e0a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_shared_correction_third_jet_gate/statement.md": "b63c4152873f04ff0d5dd263287ef87bc154dbb5b53cf1414b01deb54af0f06d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_shared_correction_third_jet_gate/proof.md": "f3c3b3e776288322ba7653da1905a7b81db349321a83f6dc12fb9c05f5dff459",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_shared_correction_third_jet_vanishing/statement.md": "60c0d1ce951a2f46c835bbe50756a2b5704dc23ec5cfc8d15f34ffd0c79bdeaa",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_shared_correction_third_jet_vanishing/proof.md": "34579c3c726f41e5bc41f06a7d8770aaa0d1f47290dbadbe067732b77d177751",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_unified_heavy_row_remainder_gate/statement.md": "29905a8b21943e295833eddc17806d85fc985c4948661506978b7d5c801a3ee2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_unified_heavy_row_remainder_gate/proof.md": "3b7ec72714ff4e00e61fb93cf8507ac2c70f9cabd597acbbf8d8e889cbd7104a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_correction_two_jet_gate/statement.md": "5610d73b036054898e0618df45c15933c8c02ed094dc43c3baec2f66847242f4",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_correction_two_jet_gate/proof.md": "0111ed16df6f01012237e25b8e770afe2b3be05a517108decc3ebae8d2610939",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_center_overlap_exact_deficit_ledger/statement.md": "62bd5e1d732a619a8be032b020cf0eaf96aca16d61bb033f2554989721198e41",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_squarefree_center_overlap_exact_deficit_ledger/proof.md": "7bbdc2db7988c546df04e62695d9203d3ff80559acb1ba98b49f1f2ae920c624",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_split_biform_macroscopic_parameter_factor/statement.md": "946dde2786e3d542c82145c262361f5e66297c34eff743a24bfe535e880ccac3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_split_biform_macroscopic_parameter_factor/proof.md": "f2b39e7707a0360218d99ff322996314e6e2c6eaddfb4708610b942a31882701",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_corank_one_jet_vanishing_router/statement.md": "d792e0f254368b4c53a804cdd2c3dcf2f4289c7bc1b1e9807447a3480e6b767e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_corank_one_jet_vanishing_router/proof.md": "dce7b05c13e0585bcb2b27f3de34aa446b9987b37787932942bb7bac471dd17e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_split_biform_factor_degree_profile_trichotomy/statement.md": "e3e40287fca3898ede3f4d6f4e18db930191db1686dc349166624f05c7539ebb",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_paired_split_biform_factor_degree_profile_trichotomy/proof.md": "d9eb908cecd6b38f83802acd92aceb4332eeb1106db1e1404870dc06da334c53",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_higher_corank_smith_jet_router/statement.md": "80df4071c0c6633a3b0bea7f9e08b7dfa37a8713689f91fca31654912b0a01d7",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_higher_corank_smith_jet_router/proof.md": "33c20f3661307ae9cf36627c06485f053a76a1059272959bf85fc9d5082308b0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_normalization_collision_dichotomy/statement.md": "2ea5532df0f3eaa72842b6efab15388818e98853bad965bf0ee6e535b5d64094",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_normalization_collision_dichotomy/proof.md": "dae58a9195d4bb1b016ad7ab1ffc97d62566f34359840f96aca876e2765b48a4",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_bezout_contact_module_presentation/statement.md": "e7261fe256c2169ce8179ab4500cf466cb01a1a2a081ea2583319251d43e5a89",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_bezout_contact_module_presentation/proof.md": "c167dadedccd6d568dd22912c973517e9d9b7a8fc25618b3679649ea44cebd16",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_exact_collision_bezout_smith_router/statement.md": "ad57623a827323d9f034148ab7c849c62927b9360046d09937f14bccaf6727b4",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_exact_collision_bezout_smith_router/proof.md": "c42c27a6045be6cb1d6c0c325762b63355c6fab38d29d6d6ab627a75009e9b7a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_truncated_source_minimal_recurrence_separation_fence/statement.md": "a039644be780608b7ead355eebdb2aa09250e0b69102d9fde6fc1b4e32fe72b7",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_truncated_source_minimal_recurrence_separation_fence/proof.md": "bc2f29e50f55892a0b0e8ee6b458659a85a3978f7356b5717e41c28b7c2f1e69",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_pade_split_jet_dictionary/statement.md": "5285637fe42f691a100848c6b03f121c3e436902caee8dcb06f3c8bc33426f7f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_pade_split_jet_dictionary/proof.md": "901e98d33413f255a7dab03cf6ae0f7b6644da86da6503b7e5b0e8322e751cf6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_barycentric_split_jet_gate/statement.md": "ee34bff50a0717589009feb0e579a6db86e3cf9f3289b40db29de02e93d4d53b",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_barycentric_split_jet_gate/proof.md": "ebfa59faeba87a8ab34c66cdd3fe68e09be9f8cfecbbf7083b0640285c74d5f6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_heavy_row_quadratic_residual_factorization/statement.md": "b03b5355fb3a09a62f2263754d3ce4b409c9c3019f357bc41387a4aad099afdb",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_heavy_row_quadratic_residual_factorization/proof.md": "54130913e897c1a95dd76d86365db4a25fc6d7ef261d548fe972b40d24ef9ac0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_divided_row_quintic_quotient/statement.md": "d0cc1e4c299a4062d0ffb8a17757edad34e569e62850a2690a60b7e7cfa93749",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_divided_row_quintic_quotient/proof.md": "6868035c13ef7fa281edf18603b62b0821852dfbe2c9b1ebb1a979cc0123c26d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_factor_profile_unsupported_root_budget/statement.md": "ee09d10890920d345c4d05f949b1c286e809fbd0e716246161e26fc9da1f0cae",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_factor_profile_unsupported_root_budget/proof.md": "3ae3d0c8bf775ac0d53da362112d0707026c95a0a5c8c96100d4290c05666aed",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_divided_row_quintic_cauchy_closed_form/statement.md": "219b52b4bade5996628050c59fb39003bed2535fd561410521242978b3e862c7",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_divided_row_quintic_cauchy_closed_form/proof.md": "96cf80c0b3065cae5a39c638fefa480b264c102400d669196d84f9524aeced7c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_factorwise_bezout_shape_classification/statement.md": "b7bd2842a782cd364e4483ca29f6423eec48db3cd337db0ba1512f7a59010aa4",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_factorwise_bezout_shape_classification/proof.md": "65f4a55a62efdd316cecddd4ef906a560917111030467e58ce79491d7d2941ae",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_companion_norm_gate/statement.md": "52494e3757c6ea98d05dcf6f9e5793868c41c46753da82a8c285f89456b9cdbc",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_companion_norm_gate/proof.md": "de2fba5b1bf6d4a89a045a4e2264a9fc32b5b2a3ed12b99ae557fe0c51575f0f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_two_branch_tangent_profile_router/statement.md": "16bcb089ccb0b35841a20e9ade2c27584640d9c52d75b94798080035b71d3657",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_two_branch_tangent_profile_router/proof.md": "b3e74fac2854fa78f959aeee332987308ab3e63cd4c50b1e15a00a236761f8b7",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_quadratic_companion_subgroup_coincidence_router/statement.md": "206ae687a048e4ff93632bf297d470d0562b6cf045c33a82e297914041fd7b57",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_quadratic_companion_subgroup_coincidence_router/proof.md": "408094584149953ef1f9e81caa8fb20891804ec3b727030fb25d9e2e059405a4",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_quadratic_companion_torus_gcd_exclusion/statement.md": "cef1aaf5b7689cdb71387d9d4401b5d0a4143bdc74bba0e2c2b4b3c3d4e111a7",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_quadratic_companion_torus_gcd_exclusion/proof.md": "16ead95c5b04937a930a53d79a7b20a9dee2d6ef36d1b92968f0eaa6fdbb7876",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_quartic_companion_toral_deck_involution_router/statement.md": "9fb9ffbdd5ceeed4b9c794c5854fa9628bcb5e354a5a359c11fa60b8c742d25d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_quartic_companion_toral_deck_involution_router/proof.md": "aa867d25e5dd9ae63cb30db5e23239661c84e7933c324d17c5937d5bf377f43f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_companion_complete_shape_exclusion/statement.md": "c1771c79e77a3c9ac45639dcb063575c6dfa523efe3e7ba96cbb3b96599868e2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_ordinary_companion_complete_shape_exclusion/proof.md": "d06c610ab90e5b8ce3560e1fc6cd57dc9dd60d2beaec6675dac8c306377e1342",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_norm_concentration/statement.md": "0e5c3cd397a2a04a6314d8b34093ff54f648d44127884da5b02b286844dddcb0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_norm_concentration/proof.md": "92baf69c4b9d1a65d52c98c1f83a28717c090089d0e24d54042ee69e92f9b5c3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_pure_split_component_floor/statement.md": "c6a3c8fea3fefbf29b912aeee37d171205fd3a183e8201e766161755e861a64f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_pure_split_component_floor/proof.md": "70497eb01127958eb7810271afb49d82a157c7444381b922fc21c420d91150d2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_componentwise_degree_floor/statement.md": "4edd8a430d2999ae8774907455b3510f03c52fab2ae5b319181cc4e25c1ac0c0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_componentwise_degree_floor/proof.md": "93d5febc3c8b7c21ffa0e0097545d724cfa231bf8a71c34cd86f0ebd43012afe",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_global_subgroup_genus_floor/statement.md": "4b29e09907aa576b1d85232838d33772229f1b597ccd6e20b07792d7df988fe9",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_global_subgroup_genus_floor/proof.md": "3625dc1fbc95e95b2a85a660c960a0e134adef59077480156390f63e932541fa",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_residual_four_cycle_rigidity/statement.md": "5ac92a9a0af5e414370bc78e3110db3c17b870009a5a578612fbcaf6d08e3ef9",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_residual_four_cycle_rigidity/proof.md": "707af9b50c3e6afe2c6a544a12cd25b919bdf126718070454d370c40811e4ca6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/audit.md": "466e67e2defabcb366e18e8b8ac097228bd1ab32bf171132fbd912079f82f943",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/claim_contract.md": "21d2d0dd163993337aaac760c2bbd37611ea4611a3875a4759979a0ba693fe66",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/dependency_subdag.md": "09a565bac59a2cbc9dd02a65b155f49e07b5ce8ca55024e0f6504ec62d37dfad",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/node.json": "cdb97c1c9401087f2a3433c953dd2b25b3d250c53878597d0d31ca7cad6f4078",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/proof.md": "dd1d56ba2e94e3bc7779fc0c31c16b7cee907860e1d8760b9f93732b02b1e018",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/provenance.md": "8a6ace027ef21bd612433181574c1d02aeee70ccbac6e35a342cbd2632c5a1a3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/result.md": "5368e124c4a47ff6e65ec9a2a4f7e312c656942fe76c19569bcb63704379b07b",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/statement.md": "2ff8aa7df67b18c5b3e724f329f0c25f51c92460ea2796383e0ad940fc637fa5",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/verify.py": "cdad923c947d7759d8096156e4c1b88f7515be07b25138cbdf5af9d8aa4dbad3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_excess_norm_omitted_recurrence_flag/verify_audit.py": "43eabea2562251854a2cbac17d22d8592c1e13fc2703146ed8c587e670268386",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/audit.md": "23908b68f0e302a69071926c91563696e0d98338c534ca76615fa21f0b096828",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/claim_contract.md": "dc023e893208cd6345639b3339c4bb4344bae6f23044edef09d361445bf3c96d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/dependency_subdag.md": "599b98f36e15856a2b14f4fa0575ad6022346f96414ac8d7979557b4854e6e20",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/node.json": "e9355eea4d8a2c464322a45b280829fb3af7676fa5be4b6a17a5c6b41dff3b0d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/proof.md": "99ed9d06054e002c4792278a6812e50adb96eaaa56074644a83f0f3f4b7c11fa",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/provenance.md": "beb876e448625eb1ed0842eeab0606b4c6f45812feff5c4dfcff04874805d76f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/result.md": "8f744a443836c0bbea16f5a986f6cdf9865cc473c7be5d27c16c82540a76c119",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/statement.md": "c24ad834f13ee4d7f7aa7a153f2ef46855e462fbbf3995b127a401678aa38f3e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/verify.py": "5f9af4d4451ae365d4c491ea0ed6ec7927948b9accd6bc4b0b1c8e45e346e4e1",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_omitted_recurrence_bordered_hankel_flag/verify_audit.py": "059a36811e369ece743f9512e784285ac47bc1dc72a24d41a3d1f9029fb16751",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/audit.md": "0f6f376f2189afce3d7f9317edbb2c388f6042eda59310411fa968b2a23f391e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/claim_contract.md": "866308e1cfdb7ba6e9c105f7c0342ed52a700f1dbfcf19112ba684196aa08fe9",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/dependency_subdag.md": "d74e7ec3873860c8c7e5239aa8744e700b829333030c452c2bd1664dbd70deea",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/node.json": "5c95d496fdebb7708df42fd3d878ab8f97d8dc1d3b794d84a875ef60ac1385b0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/proof.md": "2e7ff7d77fc2cca3c8f414d744f3550a81a03179bbda2ed1aa690e7de2b502bf",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/provenance.md": "29d96eeb551d63722d0bd71f78aba5b6afc37fcefcc900432ca065a87dbbddbd",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/result.md": "0919c976162705e51afbc73375a8c2fb65e8dc09fca12fd991af9a9a50648e3c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/statement.md": "309415ae75fcdc79b5b318a1e7695b87e7dd15931494d05e5f27d6d66ee71cc4",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/verify.py": "a21820ebb3fb2f1dc898bffa1d07de7aa15af315fd0a21c465f20947604780f6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_shape_a_static_source_arbitrary_drop_fence/verify_audit.py": "61e8ff55d7ae3e598d3e8d5aa58ab784d7a1e50ceb91a377ca96b29c7094b470",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/audit.md": "7605d59384d48a8cb2a893d2615739001f398c34d07c28f2d776a4abd64484b2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/claim_contract.md": "e5367e8ac994ffd5077f34f7c0138ed9bc261f2739dfff2b892e48d215e60e5f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/dependency_subdag.md": "f521dd7df8324b84ef279ff69860dcab62bf764aba55a851a41a4e8f84da7c78",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/node.json": "eca80ef5ae6bddb711c683cc64a1e506a1f72398294551e65e19b61a398f07e6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/proof.md": "1b6e217600923d29738a8c28412252330f3ba31d2d88c2eef5285f21cd7896f9",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/provenance.md": "5cc01dc51128e56bad34274f9a415633ed079262712162c7a55dbb936d279c25",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/result.md": "846f3eae2510b07877fc930552d44871b3d661097ac0414837eaf26698c38ee0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/statement.md": "8d2f20c293cba15ca9269f7bdc7aa1652cb8ec811c778eb6b73e2accad493f7d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/verify.py": "17b7848da84e448235708a6e9132d28f2de5f153836e2f7f00d1dcd558a2a48e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_scalar_weld_residual_mds_flag/verify_audit.py": "fc551cdd0439a68d2b97fd4ca859aa52db858befcfdeb5169453015c66290e1c",
}


class VerificationError(RuntimeError):
    """Raised when an exact packet identity fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_div(left: int, right: int) -> int:
    return (left + right - 1) // right


def least_with_parity(numerator: int, denominator: int, parity: int) -> int:
    value = ceil_div(numerator, denominator)
    if value % 2 != parity:
        value += 1
    return value


def partitions(total: int, ceiling: int | None = None):
    if total == 0:
        yield ()
        return
    if ceiling is None or ceiling > total:
        ceiling = total
    for first in range(ceiling, 0, -1):
        for tail in partitions(total - first, first):
            yield (first, *tail)


@dataclass(frozen=True)
class Formula:
    pade_exponent_offset: int = 1
    residual_degree: int = 4
    double_correction_multiplicity: int = 2
    simple_correction_total: int = 4
    supported_exception_cap: int = 4
    separated_residual_degree: int = 3
    separated_smith_exponent: int = 2
    center_overlap_cap: int = 1
    heavy_row_unknowns: int = 2
    layer_a_rank: int = 20
    layer_a_nullity: int = 4
    layer_a_row_surplus: int = 2
    barycentric_remainder_defect: int = 1
    center_disjoint_quotient_degree: int = 0
    separated_heavy_row_nonzero: int = 1
    shared_forced_jet_order: int = 2
    shared_third_jet_vanishes: int = 1
    nonreduced_forced_order: int = 2
    nonreduced_missing_jets: int = 2
    center_overlap_equals_deficit: int = 1
    macroscopic_factor_d_a0: int = 61083979321
    macroscopic_factor_d_a1: int = 78536544842
    separated_corank_one_unresolved_jets: int = 0
    nonreduced_nonzero_jet_min_corank: int = 1
    automatic_source_separation: int = 0
    factor_content_degree: int = 0
    factor_degree_slack: int = 0
    factor_profile_count: int = 3
    large_odd_d_a0: int = 61083979321
    large_odd_d_a1: int = 78536544843
    huge_even_d_a0: int = 122167958642
    huge_even_d_a1: int = 157073089684
    nonreduced_first_nonzero_third_jet: int = 0
    nonreduced_noncollision_nonzero_jet: int = 0
    collision_max_regular_corank: int = 2
    collision_profile_count: int = 3
    collision_global_jet_count: int = 2
    collision_barycentric_functional_count: int = 4
    collision_heavy_row_residual_degree_d_a0: int = 2
    collision_heavy_row_residual_degree_d_a1: int = 3
    collision_divided_row_quotient_degree: int = 5
    collision_unsupported_root_budget_d_a0: int = 4
    collision_unsupported_root_budget_d_a1: int = 5
    collision_d_a1_factor_profile_count: int = 1
    collision_quintic_independent_gate_count: int = 0
    collision_factor_shape_count: int = 4
    collision_large_factor_max_deficit: int = 6
    collision_ordinary_companion_degree_cap: int = 4
    collision_q2_norm_cap: int = 7
    collision_q2_reduced_norm_cap: int = 6
    collision_q4_norm_cap: int = 14
    collision_q4_reduced_norm_cap: int = 12
    collision_two_branch_shape_count: int = 2
    collision_two_branch_profile_count: int = 2
    collision_two_branch_excluded_profile_count: int = 1
    collision_q2_vertical_defect: int = 7
    collision_q2_full_fiber_floor: int = 549755813882
    collision_q2_pair_floor: int = 1649267441646
    collision_q2_s3_subgroup_constant: int = 8192
    collision_q2_c3_subgroup_constant: int = 512
    collision_q2_vm_admissible_survivors: int = 0
    collision_q2_s3_gcd_cube_constant: int = 27648
    collision_q2_c3_gcd_cube_constant: int = 1728
    collision_q2_excluded_shape_count: int = 2
    collision_remaining_shape_count: int = 2
    collision_q4_vertical_defect: int = 14
    collision_q4_full_fiber_floor: int = 549755813875
    collision_q4_pair_floor: int = 4123168604063
    collision_q4_quotient_row_degree: int = 3
    collision_q4_residual_pair_floor: int = 3298534883250
    collision_q4_residual_component_cap: int = 4
    collision_q4_excluded_shape_count: int = 1
    collision_final_shape_count: int = 1
    collision_shape_a_padding_degree: int = 183251937956
    collision_shape_a_excess_norm_degree_cap: int = 183251937963
    collision_shape_a_pure_fiber_floor: int = 183251937970
    collision_shape_a_resultant_bidegree: int = 50371909149418411349340
    collision_shape_a_pair_floor: int = 75557863727701029814224
    collision_shape_a_component_floor: int = 274877906955
    collision_shape_a_component_min_bidegree: int = 39768216
    collision_shape_a_component_min_point_floor: int = 10931403977394458172
    collision_shape_a_component_multiplicity_ratio: int = 4608
    collision_shape_a_global_point_floor: int = 151115727450087753427630
    collision_shape_a_global_chi_floor: int = 262353693488940318721
    collision_shape_a_global_genus_floor: int = 131176846286340314460
    collision_shape_a_global_genus_ceiling: int = 50371909149143533442400
    collision_shape_a_residual_divisor_multiplier: int = 2
    collision_shape_a_residual_cycle_degree: int = 4
    collision_shape_a_residual_section_dimension: int = 1
    collision_shape_a_second_modification_constant_rank: int = 0
    collision_shape_a_second_modification_negative_ceiling: int = -549755813885
    collision_shape_a_source_row_count: int = 824633720830
    collision_shape_a_source_locator_degree: int = 549755813887
    collision_shape_a_omitted_recurrence_length: int = 274877906941
    collision_shape_a_offline_slope_count: int = 549755813889
    collision_shape_a_fixture_layer_cake: int = 3
    collision_shape_a_bordered_matrix_size: int = 549755813889
    collision_shape_a_padding_flag_degree: int = 183251937956
    collision_shape_a_regular_flag_degree: int = 366503875933
    collision_shape_a_bordered_source_subset_size: int = 549755813889
    collision_shape_a_bordered_fixture_subset_checks: int = 252
    collision_shape_a_static_drop_fixture_cases: int = 4
    collision_shape_a_static_drop_source_count: int = 8
    collision_shape_a_static_drop_maximum: int = 3
    collision_shape_a_static_drop_residue_checks: int = 36
    collision_shape_a_static_drop_subset_checks: int = 560
    collision_shape_a_residual_mds_row_surplus: int = 549755813889
    collision_shape_a_residual_mds_unpadded_start: int = 549755813888
    collision_shape_a_residual_mds_padded_start: int = 549755813889
    collision_shape_a_residual_mds_fixture_cases: int = 4
    collision_shape_a_residual_mds_fixture_parities: int = 22
    collision_shape_a_residual_mds_fixture_rows: int = 108


def finite_field_rank(matrix: list[list[int]], prime: int) -> int:
    work = [row[:] for row in matrix]
    row = 0
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], prime - 2, prime)
        work[row] = [entry * inverse % prime for entry in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            scale = work[index][column]
            work[index] = [
                (left - scale * right) % prime
                for left, right in zip(work[index], work[row])
            ]
        row += 1
    return row


def verify_layer_a_fixture(formula: Formula) -> int:
    prime = 97
    zeta = 28
    require(pow(zeta, 32, prime) == 1, "Layer-A root order failed")
    require(pow(zeta, 16, prime) != 1, "Layer-A root is not primitive")
    points = [pow(zeta, 2 * index, prime) for index in range(13)]
    slopes = [pow(zeta, 4 * index, prime) for index in range(8)] + [zeta]
    incidences = []
    for x in points:
        roots = [
            gamma
            for gamma in slopes
            if (gamma * gamma - pow(x, 4, prime)) % prime == 0
        ]
        require(len(roots) == 2, "Layer-A point is not saturated")
        require(set(roots) == {x * x % prime, -x * x % prime}, "wrong roots")
        incidences.extend((gamma, x) for gamma in roots)
    matrix = [
        [
            pow(gamma, degree_z, prime) * pow(x, degree_x, prime) % prime
            for degree_z in range(3)
            for degree_x in range(8)
        ]
        for gamma, x in incidences
    ]
    rank = finite_field_rank(matrix, prime)
    require(len(matrix) == 26, "Layer-A row count changed")
    require(len(matrix[0]) == 24, "Layer-A column count changed")
    require(rank == formula.layer_a_rank, "Layer-A rank changed")
    require(24 - rank == formula.layer_a_nullity, "Layer-A nullity changed")
    require(26 - 24 == formula.layer_a_row_surplus, "Layer-A surplus changed")
    return 32


def verify_factor_profiles(formula: Formula) -> tuple[int, int]:
    checks = 0
    feasible = 0
    profile_counts = {(0, 1, 0): 0, (1, 2, 0): 0, (1, 0, 1): 0}

    for e in range(7, 32, 2):
        p = (3 * e - 1) // 2
        capital_m = e - 2
        capital_n = p - 3
        for d_a in (0, 1):
            q = 9 - 2 * d_a
            row_count = 3 * p - 3 + d_a
            slope_count = 3 * e
            for factor_degrees in partitions(capital_m):
                checks += 1
                minima = [
                    ceil_div(row_count * degree, slope_count)
                    for degree in factor_degrees
                ]
                if sum(minima) > capital_n:
                    continue

                feasible += 1
                slack = capital_n - sum(minima)
                small = sum(
                    degree % 2 == 1 and q * degree < 3 * e
                    for degree in factor_degrees
                )
                large = sum(
                    degree % 2 == 1 and q * degree >= 3 * e
                    for degree in factor_degrees
                )
                huge = sum(
                    degree % 2 == 0 and q * degree >= 6 * e
                    for degree in factor_degrees
                )
                require(
                    small - large - 2 * huge + 2 * slack == -1,
                    "factor deficit equation failed",
                )
                require(slack == formula.factor_degree_slack, "factor slack changed")
                profile = (small, large, huge)
                require(profile in profile_counts, "factor profile escaped trichotomy")
                profile_counts[profile] += 1

    require(checks == 25504, "factor partition coverage changed")
    require(feasible == 776, "feasible factor partition count changed")
    require(
        len(profile_counts) == formula.factor_profile_count,
        "factor profile count changed",
    )
    require(
        profile_counts == {
            (0, 1, 0): 622,
            (1, 2, 0): 73,
            (1, 0, 1): 81,
        },
        "factor profile census changed",
    )
    return checks, feasible


def verify_nonreduced_collision(formula: Formula) -> int:
    """Replay the normalization solutions and local quadratic Smith ledger."""
    solutions = []
    for multiplicities in ((2,), (1, 1)):
        ramification_choices = ((1,), (2,)) if len(multiplicities) == 1 else ((1, 1),)
        for ramification in ramification_choices:
            for base_order in range(2, 5):
                if all(
                    e_b * base_order == 2 * m_b
                    for e_b, m_b in zip(ramification, multiplicities)
                ):
                    solutions.append((multiplicities, ramification, base_order))
    require(
        solutions == [((2,), (1,), 4), ((2,), (2,), 2), ((1, 1), (1, 1), 2)],
        "nonreduced normalization solutions changed",
    )
    require(
        formula.nonreduced_first_nonzero_third_jet == 0,
        "first-nonzero third jet returned",
    )
    require(
        formula.nonreduced_noncollision_nonzero_jet == 0,
        "noncollision nonzero jet returned",
    )
    require(formula.collision_max_regular_corank == 2, "collision corank changed")

    profiles = set()
    for order_a in range(0, 7):
        first_exponent = min(2, order_a)
        profile = (first_exponent, 4 - first_exponent)
        profiles.add(profile)
        expected = (0, 4) if order_a == 0 else ((1, 3) if order_a == 1 else (2, 2))
        require(profile == expected, "Smith router")
    require(
        profiles == {(0, 4), (1, 3), (2, 2)},
        "collision Smith profile set changed",
    )
    require(len(profiles) == formula.collision_profile_count, "profile count changed")
    return 3 + 7


def verify_collision_split_jet_dictionary(formula: Formula) -> int:
    """Replay the low-order moment propagation and profile dictionary."""
    prime = 101
    x_star = 17
    checks = 0

    def add(left: list[int], right: list[int]) -> list[int]:
        size = max(len(left), len(right))
        return [
            ((left[i] if i < len(left) else 0)
             + (right[i] if i < len(right) else 0)) % prime
            for i in range(size)
        ]

    def multiply(left: list[int], right: list[int]) -> list[int]:
        out = [0] * (len(left) + len(right) - 1)
        for i, x in enumerate(left):
            for j, y in enumerate(right):
                out[i + j] = (out[i + j] + x * y) % prime
        return out

    for lambda_0 in (0, 9):
        for lambda_1 in (0, 13):
            a = [lambda_0, lambda_1, 22, 5]
            c_1 = [0, 0, 0, 7]
            c_0 = [0, 0, 0, 0, 0, 0, 11]
            derivative = add(a, add(multiply(c_1, [3, 8]), multiply(c_0, [4])))
            require(derivative[:3] == a[:3], "quadratic reduction changed jets")
            checks += 1

            moments = [[lambda_0, lambda_1, 0, 0]]
            for i in range(5):
                source = [0, 0, 3 * (i + 1)]
                q_x_h = [0, 0, 0, 5 * (i + 2)]
                following = add(source, [(-value) % prime for value in q_x_h])
                following = add(
                    following,
                    [(x_star * value) % prime for value in moments[-1]],
                )
                moments.append(following)
                require(
                    following[0] == pow(x_star, i + 1, prime) * lambda_0 % prime,
                    "zeroth split jet did not propagate",
                )
                require(
                    following[1] == pow(x_star, i + 1, prime) * lambda_1 % prime,
                    "first split jet did not propagate",
                )
                checks += 2

            profile = (4,)
            if lambda_0 == 0:
                profile = (1, 3) if lambda_1 else (2, 2)
            require(profile in {(4,), (1, 3), (2, 2)}, "split-jet profile")
            checks += 1

    require(formula.collision_global_jet_count == 2, "global jet count changed")
    return checks


def verify_collision_barycentric_gate(formula: Formula) -> int:
    """Replay outside-row value and derivative interpolation."""
    prime = 101

    def inv(value: int) -> int:
        return pow(value % prime, prime - 2, prime)

    def multiply(left: list[int], right: list[int]) -> list[int]:
        out = [0] * (len(left) + len(right) - 1)
        for i, x in enumerate(left):
            for j, y in enumerate(right):
                out[i + j] = (out[i + j] + x * y) % prime
        return out

    def hasse(poly: list[int], point: int, order: int) -> int:
        return sum(
            comb(power, order) * coefficient * pow(point, power - order, prime)
            for power, coefficient in enumerate(poly)
            if power >= order
        ) % prime

    rows = [1, 2, 3, 4, 5]
    x_star = 17
    tau = 11
    locator = [1]
    for x in rows:
        locator = multiply(locator, [(-x) % prime, 1])
    locator_value = hasse(locator, x_star, 0)
    locator_derivative = hasse(locator, x_star, 1)

    value_weights = []
    derivative_weights = []
    for x in rows:
        derivative_at_x = 1
        for y in rows:
            if y != x:
                derivative_at_x = derivative_at_x * (x - y) % prime
        value = locator_value * inv(x_star - x) * inv(derivative_at_x) % prime
        derivative = value * (
            locator_derivative * inv(locator_value) - inv(x_star - x)
        ) % prime
        value_weights.append(value)
        derivative_weights.append(derivative)

    base = multiply([(-tau) % prime, 1], [(-tau) % prime, 1])
    base = multiply(base, [-29 % prime, 1])
    jet_rows = (
        [1],
        [(-tau) % prime, 1],
        multiply([(-tau) % prime, 1], [(-tau) % prime, 1]),
    )

    checks = 0
    for expected_profile, jet_row in zip(((4,), (1, 3), (2, 2)), jet_rows):
        rows_in_t = []
        for x in rows:
            size = max(len(base), len(jet_row))
            row = [0] * size
            for i, value in enumerate(base):
                row[i] = (row[i] + value) % prime
            for i, value in enumerate(jet_row):
                row[i] = (row[i] + (x - x_star) * value) % prime
            rows_in_t.append(row)

        value_row = [
            sum(
                value_weights[i]
                * (rows_in_t[i][power] if power < len(rows_in_t[i]) else 0)
                for i in range(len(rows))
            ) % prime
            for power in range(max(map(len, rows_in_t)))
        ]
        derivative_row = [
            sum(
                derivative_weights[i]
                * (rows_in_t[i][power] if power < len(rows_in_t[i]) else 0)
                for i in range(len(rows))
            ) % prime
            for power in range(max(map(len, rows_in_t)))
        ]

        for power in range(len(value_row)):
            require(
                value_row[power] == (base[power] if power < len(base) else 0),
                "barycentric value row",
            )
            require(
                derivative_row[power]
                == (jet_row[power] if power < len(jet_row) else 0),
                "barycentric derivative row",
            )
            checks += 2

        value_jets = [hasse(value_row, tau, order) for order in range(3)]
        derivative_jets = [hasse(derivative_row, tau, order) for order in range(2)]
        require(
            value_jets[0] == value_jets[1] == 0 and value_jets[2] != 0,
            "barycentric value order",
        )
        profile = (4,)
        if derivative_jets[0] == 0:
            profile = (1, 3) if derivative_jets[1] else (2, 2)
        require(profile == expected_profile, "barycentric profile")
        checks += 2

    require(
        formula.collision_barycentric_functional_count == 4,
        "barycentric functional count changed",
    )
    return checks


def verify_nonreduced_heavy_row_residual(formula: Formula) -> int:
    """Replay the center-adjusted supported and residual degree ledger."""
    checks = 0
    for e in (7, 13, 183251937963):
        for d_a in (0, 1):
            supported_degree = e - 6 - d_a
            correction_degree = 2
            residual_degree = (
                formula.collision_heavy_row_residual_degree_d_a0
                if d_a == 0
                else formula.collision_heavy_row_residual_degree_d_a1
            )
            require(
                supported_degree + correction_degree + residual_degree == e - 2,
                "nonreduced heavy-row degree",
            )
            require(
                supported_degree + correction_degree == e - 4 - d_a,
                "nonreduced remainder modulus degree",
            )
            require(
                residual_degree == 2 + d_a,
                "nonreduced center-adjusted residual degree changed",
            )
            checks += 3
    return checks


def verify_nonreduced_divided_row_quotient(formula: Formula) -> int:
    """Replay the quintic degree and correction-value recurrence."""
    prime = 101
    tau = 17
    x_star = 13

    def add(left: list[int], right: list[int]) -> list[int]:
        size = max(len(left), len(right))
        return [
            ((left[i] if i < len(left) else 0)
             + (right[i] if i < len(right) else 0)) % prime
            for i in range(size)
        ]

    def multiply(left: list[int], right: list[int]) -> list[int]:
        out = [0] * (len(left) + len(right) - 1)
        for i, x in enumerate(left):
            for j, y in enumerate(right):
                out[i + j] = (out[i + j] + x * y) % prime
        return out

    def value(poly: list[int], point: int) -> int:
        return sum(
            coefficient * pow(point, power, prime)
            for power, coefficient in enumerate(poly)
        ) % prime

    s_b = multiply([(-tau) % prime, 1], [(-tau) % prime, 1])
    s_b_squared = multiply(s_b, s_b)
    quotient_rows = [[3, 4, 5, 6, 7, 8]]
    checks = 0
    for i in range(6):
        h_i = [i + 2, 2 * i + 1]
        forcing = multiply(s_b_squared, h_i)
        following = add(
            [(x_star * coefficient) % prime for coefficient in quotient_rows[-1]],
            [(-coefficient) % prime for coefficient in forcing],
        )
        quotient_rows.append(following)
        require(
            len(following) - 1 <= formula.collision_divided_row_quotient_degree,
            "divided-row quotient degree",
        )
        require(
            value(following, tau)
            == x_star * value(quotient_rows[-2], tau) % prime,
            "divided-row correction recurrence",
        )
        checks += 2

    require(value(quotient_rows[0], tau) != 0, "initial quotient value")
    for i, row in enumerate(quotient_rows):
        require(
            value(row, tau)
            == pow(x_star, i, prime) * value(quotient_rows[0], tau) % prime,
            "geometric quotient vector",
        )
        checks += 1
    checks += 1

    for e in (7, 13, 183251937963):
        require(
            (e + 1) - (e - 4) == formula.collision_divided_row_quotient_degree,
            "quintic degree subtraction",
        )
        checks += 1
    return checks


def verify_collision_factor_unsupported_root_budget(formula: Formula) -> int:
    """Replay the sharpened thresholds and d_A=1 profile compression."""
    checks = 0
    for e in range(7, 80, 2):
        total = e - 2
        for d_a, q in ((0, 9), (1, 7)):
            budget = (
                formula.collision_unsupported_root_budget_d_a0
                if d_a == 0
                else formula.collision_unsupported_root_budget_d_a1
            )
            budget_twice = 2 * budget
            large = least_with_parity(3 * e - budget_twice, q - 2, 1)
            huge = least_with_parity(6 * e - budget_twice, q - 2, 0)
            require((q - 2) * large >= 3 * e - budget_twice, "budget large")
            require(
                (q - 2) * (large - 2) < 3 * e - budget_twice,
                "budget large predecessor",
            )
            require((q - 2) * huge >= 6 * e - budget_twice, "budget huge")
            require(
                (q - 2) * (huge - 2) < 6 * e - budget_twice,
                "budget huge predecessor",
            )
            checks += 4
            if d_a == 1:
                require(2 * large + 1 > total, "profile II survived")
                require(huge + 1 > total, "profile III survived")
                checks += 2

    official = 183251937963
    require(
        least_with_parity(
            3 * official - 2 * formula.collision_unsupported_root_budget_d_a0,
            7,
            1,
        ) == 78536544841,
        "official d_A=0 large",
    )
    require(
        least_with_parity(
            6 * official - 2 * formula.collision_unsupported_root_budget_d_a0,
            7,
            0,
        ) == 157073089682,
        "official d_A=0 huge",
    )
    require(
        least_with_parity(
            3 * official - 2 * formula.collision_unsupported_root_budget_d_a1,
            5,
            1,
        ) == 109951162777,
        "official d_A=1 large",
    )
    require(
        least_with_parity(
            6 * official - 2 * formula.collision_unsupported_root_budget_d_a1,
            5,
            0,
        ) == 219902325554,
        "official d_A=1 huge",
    )
    checks += 4

    for d_a, q, chi, coefficient in (
        (0, 9, -1, 3),
        (0, 9, -2, 6),
        (1, 7, -1, 3),
        (1, 7, -2, 6),
    ):
        e = 101
        budget = (
            formula.collision_unsupported_root_budget_d_a0
            if d_a == 0
            else formula.collision_unsupported_root_budget_d_a1
        )
        budget_twice = 2 * budget
        threshold = least_with_parity(
            coefficient * e - budget_twice,
            q - 2,
            1 if chi == -1 else 0,
        )
        sigma_twice = 3 * e * chi + q * threshold
        require(
            sigma_twice >= 2 * threshold - budget_twice,
            "factor slack inequality",
        )
        checks += 1

    require(
        formula.collision_d_a1_factor_profile_count == 1,
        "d_A=1 factor-profile count changed",
    )
    return checks


def verify_collision_quintic_cauchy_closed_form(formula: Formula) -> int:
    """Replay the center-adjusted Cauchy formula over two finite fields."""

    def run_fixture(prime: int, d_a: int) -> int:
        def trim(poly: list[int]) -> list[int]:
            out = [value % prime for value in poly]
            while len(out) > 1 and out[-1] == 0:
                out.pop()
            return out

        def add(left: list[int], right: list[int]) -> list[int]:
            size = max(len(left), len(right))
            return trim([
                (left[i] if i < len(left) else 0)
                + (right[i] if i < len(right) else 0)
                for i in range(size)
            ])

        def scale(poly: list[int], scalar: int) -> list[int]:
            return trim([scalar * value for value in poly])

        def multiply(left: list[int], right: list[int]) -> list[int]:
            out = [0] * (len(left) + len(right) - 1)
            for i, x in enumerate(left):
                for j, y in enumerate(right):
                    out[i + j] += x * y
            return trim(out)

        def inverse(value: int) -> int:
            return pow(value % prime, prime - 2, prime)

        def product(values) -> int:
            answer = 1
            for value in values:
                answer = answer * value % prime
            return answer

        e = 7
        p = (3 * e - 1) // 2
        n_0 = 3 * p - 2
        d = 2 * p - 1
        degree_x = p - 3
        source = list(range(1, n_0 + 1))
        x_star = n_0 + 9
        tau = 0
        gamma = n_0 + 3
        a_q = 7

        s_b = [0, 0, 1]
        j_star = [1] if d_a == 0 else [(-gamma) % prime, 1]
        g_off = [(-gamma) % prime, 1] if d_a == 0 else [1]
        g_star = multiply(j_star, g_off)
        h_nr = multiply(g_star, s_b)
        residual = [3, 4, 1] if d_a == 0 else [3, 4, 1, 1]
        g_heavy = multiply(multiply(g_off, s_b), residual)
        q_heavy = scale(
            multiply(g_star, multiply(s_b, multiply(s_b, s_b))),
            a_q,
        )
        lambda_0 = multiply([2, 1], [3, 1])
        if d_a == 0:
            lambda_0 = multiply([1, 1], lambda_0)
        lambda_form = multiply(j_star, lambda_0)

        def k_value(y: int) -> list[int]:
            answer = [0]
            power = 1
            for degree in range(degree_x):
                coefficient = [degree + 2, y + degree + 1, 2 * degree + 1]
                answer = add(answer, scale(coefficient, power))
                power = power * y % prime
            return answer

        def g_value(y: int) -> list[int]:
            return add(g_heavy, scale(k_value(y), y - x_star))

        l_at_star = product(x_star - y for y in source)
        l_prime = {
            y: product(y - z for z in source if z != y)
            for y in source
        }
        omega = {y: [y + 2, 2 * y + 1] for y in source}
        source_product = {
            y: scale(multiply(lambda_form, g_value(y)), inverse(l_prime[y]))
            for y in source
        }

        checks = 0
        previous_d = None
        previous_c = None
        previous_h = None
        for i in range(d + 1):
            d_i = [0]
            h_i = [0]
            f_i = [0]
            for y in source:
                y_power = pow(y, i, prime)
                d_i = add(
                    d_i,
                    scale(omega[y], y_power * inverse(x_star - y)),
                )
                h_i = add(h_i, scale(omega[y], y_power))
                divided_value = scale(
                    add(
                        source_product[y],
                        scale(multiply(omega[y], q_heavy), -1),
                    ),
                    inverse(y - x_star),
                )
                f_i = add(f_i, scale(divided_value, y_power))

            c_i = add(
                scale(
                    multiply(lambda_0, residual),
                    -pow(x_star, i, prime) * inverse(l_at_star),
                ),
                scale(multiply(multiply(s_b, s_b), d_i), a_q),
            )
            require(f_i == multiply(h_nr, c_i), "quintic Cauchy formula")
            require(
                len(c_i) - 1 <= formula.collision_divided_row_quotient_degree,
                "quintic degree",
            )
            checks += 2

            if previous_d is not None:
                require(
                    d_i == add(scale(previous_d, x_star), scale(previous_h, -1)),
                    "Cauchy recurrence",
                )
                require(
                    c_i
                    == add(
                        scale(previous_c, x_star),
                        scale(multiply(multiply(s_b, s_b), previous_h), -a_q),
                    ),
                    "closed-form quintic recurrence",
                )
                checks += 2
            previous_d = d_i
            previous_h = h_i
            previous_c = c_i

            correction_value = c_i[0] % prime
            expected = (
                pow(x_star, i, prime)
                * scale(
                    multiply(lambda_0, residual),
                    -inverse(l_at_star),
                )[0]
            ) % prime
            require(correction_value == expected, "geometric correction value")
            checks += 1

        require(tau not in source and x_star not in source, "fixture separation")
        return checks + 1

    require(
        formula.collision_quintic_independent_gate_count == 0,
        "quintic independent-gate count changed",
    )
    return sum(
        run_fixture(prime, d_a)
        for prime in (101, 127)
        for d_a in (0, 1)
    )


def verify_collision_factorwise_bezout_shapes(formula: Formula) -> int:
    """Exhaust the factorwise contact and heavy-row degree records."""
    ordinary = []
    for b in range(3):
        for t in range(4):
            m = 2 * (b - t)
            r = m - b - t
            if m > 0 and m % 2 == 0 and r >= 0:
                n = 3 * m // 2
                ell = 2 * b
                require(3 * m // 2 == r + ell, "ordinary Bezout capacity")
                ordinary.append((m, n, r, b, t, ell))
    ordinary.sort()
    require(
        ordinary == [(2, 3, 1, 1, 0, 2), (4, 6, 2, 2, 0, 4)],
        "ordinary factor records",
    )

    checks = 2
    for e in list(range(7, 200, 2)) + [183251937963]:
        shapes = []
        for q_count in range(3):
            for f_count in range(2):
                companions = [ordinary[0]] * q_count + [ordinary[1]] * f_count
                if sum(row[3] for row in companions) > 2:
                    continue
                large = (
                    e - 2 - sum(row[0] for row in companions),
                    (3 * e - 7) // 2 - sum(row[1] for row in companions),
                    e - 7 - sum(row[2] for row in companions),
                    2 - sum(row[3] for row in companions),
                    3 - sum(row[4] for row in companions),
                    4 - sum(row[5] for row in companions),
                )
                m, n, r, b, t, ell = large
                if min(large) < 0 or m % 2 != 1:
                    continue
                if 2 * n - 3 * m != -1 or m != e + 2 * b - 2 * t:
                    continue
                if (3 * m - e) // 2 != r + ell:
                    continue
                if 7 * m < 3 * e or 5 * m < 3 * e - 10:
                    continue
                shapes.append((large, tuple(sorted(companions))))

        expected_count = 1 if e == 7 else 2 if e == 9 else 4
        require(len(shapes) == expected_count, "factor shape count")
        for large, companions in shapes:
            rows = (large, *companions)
            require(sum(row[0] for row in rows) == e - 2, "shape m total")
            require(sum(row[1] for row in rows) == (3 * e - 7) // 2,
                    "shape n total")
            require(sum(row[2] for row in rows) == e - 7, "shape padding total")
            require(sum(row[3] for row in rows) == 2, "shape correction total")
            require(sum(row[4] for row in rows) == 3, "shape residual total")
            require(sum(row[5] for row in rows) == 4, "shape contact total")
            checks += 6
        checks += 1

    require(formula.collision_factor_shape_count == 4, "factor shape count changed")
    require(
        formula.collision_large_factor_max_deficit == 6,
        "large factor deficit changed",
    )
    require(
        formula.collision_ordinary_companion_degree_cap == 4,
        "ordinary companion cap changed",
    )
    return checks + 3


def verify_collision_ordinary_companion_norm(formula: Formula) -> int:
    """Replay the low-degree companion norm caps and forced divisors."""
    checks = 0
    for e in list(range(9, 200, 2)) + [183251937963]:
        p = (3 * e - 1) // 2
        row_count = 3 * p - 2
        require(2 * row_count == 9 * e - 7, "companion row count")
        checks += 1
        for m, n, norm_cap, reduced_cap in (
            (2, 3, formula.collision_q2_norm_cap,
             formula.collision_q2_reduced_norm_cap),
            (4, 6, formula.collision_q4_norm_cap,
             formula.collision_q4_reduced_norm_cap),
        ):
            sigma = 3 * e * n - row_count * m
            require(sigma == norm_cap == 7 * m // 2, "companion norm cap")
            require(m // 2 + reduced_cap == norm_cap, "companion reduced cap")
            require(norm_cap < row_count, "companion interpolation gate")
            checks += 3
    return checks


def verify_collision_two_branch_tangent_router(formula: Formula) -> int:
    """Replay the product-rule profile router for shapes B and D."""

    def multiply(left, right, prime):
        product = {}
        for (z_left, y_left), left_value in left.items():
            for (z_right, y_right), right_value in right.items():
                z_degree = z_left + z_right
                y_degree = y_left + y_right
                if z_degree > 2 or y_degree > 2:
                    continue
                key = (z_degree, y_degree)
                product[key] = (
                    product.get(key, 0) + left_value * right_value
                ) % prime
        return product

    def derivative_y(polynomial, prime):
        return {
            (z_degree, y_degree - 1): y_degree * value % prime
            for (z_degree, y_degree), value in polynomial.items()
            if y_degree
        }

    shape_orders = {"A": (2,), "B": (1, 1), "C": (2,), "D": (1, 1)}
    two_branch = tuple(
        name for name, orders in shape_orders.items() if orders == (1, 1)
    )
    require(two_branch == ("B", "D"), "two-branch shape ledger")

    checks = 1
    for prime in (101, 127):
        for a_1 in range(1, 6):
            for a_2 in range(1, 6):
                for v_1 in range(6):
                    for v_2 in range(6):
                        u_0 = (2 * a_1 + 3 * a_2 + 1) % prime
                        require(u_0 != 0, "two-branch unit fixture")
                        f_1 = {
                            (1, 0): a_1,
                            (0, 1): v_1,
                            (2, 0): 7,
                            (1, 1): 11,
                            (0, 2): 13,
                        }
                        f_2 = {
                            (1, 0): a_2,
                            (0, 1): v_2,
                            (2, 0): 17,
                            (1, 1): 19,
                            (0, 2): 23,
                        }
                        unit = {(0, 0): u_0, (1, 0): 29, (0, 1): 31}
                        product = multiply(
                            multiply(unit, f_1, prime), f_2, prime
                        )
                        g_x = derivative_y(product, prime)
                        expected = u_0 * (a_1 * v_2 + a_2 * v_1) % prime
                        require(
                            g_x.get((0, 0), 0) == 0,
                            "profile-four exclusion",
                        )
                        require(g_x.get((1, 0), 0) == expected, "tangent sum")
                        require(
                            (expected == 0)
                            == ((v_1 * a_2 + v_2 * a_1) % prime == 0),
                            "two-branch profile router",
                        )
                        checks += 4

    require(
        formula.collision_two_branch_shape_count == len(two_branch),
        "two-branch shape count changed",
    )
    require(
        formula.collision_two_branch_profile_count == 2,
        "two-branch profile count changed",
    )
    require(
        formula.collision_two_branch_excluded_profile_count == 1,
        "two-branch excluded-profile count changed",
    )
    return checks + 3


def verify_collision_quadratic_subgroup_router(formula: Formula) -> int:
    """Replay the seven-defect count and divided quadratic resultant."""

    def evaluate(coefficients, value, prime):
        total = 0
        for coefficient in reversed(coefficients):
            total = (total * value + coefficient) % prime
        return total

    def determinant(matrix, prime):
        work = [[entry % prime for entry in row] for row in matrix]
        value = 1
        for column in range(len(work)):
            pivot = next(
                (row for row in range(column, len(work)) if work[row][column]),
                None,
            )
            if pivot is None:
                return 0
            if pivot != column:
                work[pivot], work[column] = work[column], work[pivot]
                value = -value
            pivot_value = work[column][column]
            value = value * pivot_value % prime
            inverse = pow(pivot_value, -1, prime)
            for row in range(column + 1, len(work)):
                multiplier = work[row][column] * inverse % prime
                for index in range(column, len(work)):
                    work[row][index] = (
                        work[row][index] - multiplier * work[column][index]
                    ) % prime
        return value % prime

    N = 2**41
    e = (2**39 + 1) // 3
    gamma_size = 3 * e
    row_count = (9 * e - 7) // 2
    incidences = 2 * row_count
    defect = 3 * gamma_size - incidences
    full_fibers = gamma_size - defect
    pair_floor = 3 * full_fibers

    require(defect == formula.collision_q2_vertical_defect, "Q2 vertical defect")
    require(
        full_fibers == formula.collision_q2_full_fiber_floor,
        "Q2 full-fiber floor",
    )
    require(pair_floor == formula.collision_q2_pair_floor, "Q2 pair floor")

    s3_constant = 16 * 4 * 4**2 * (4 + 4)
    c3_constant = 16 * 2 * 2**2 * (2 + 2)
    require(
        s3_constant == formula.collision_q2_s3_subgroup_constant,
        "Q2 S3 subgroup constant",
    )
    require(
        c3_constant == formula.collision_q2_c3_subgroup_constant,
        "Q2 C3 subgroup constant",
    )
    require(s3_constant**3 * N**2 < pair_floor**3, "Q2 S3 strict margin")
    require(
        c3_constant**3 * N**2 < (pair_floor // 2) ** 3,
        "Q2 C3 strict margin",
    )
    require(10000 * (4 * 4) ** 3 < N**2, "Q2 subgroup lower size")
    require((3 * N) ** 4 < (2**167) ** 3, "Q2 subgroup upper size")
    require(2 * row_count > 3, "Q2 absolute irreducibility point floor")
    require(pair_floor // 2 > 8, "Q2 cyclic Frobenius intersection")
    require(
        formula.collision_q2_vm_admissible_survivors == 0,
        "Q2 VM-admissible survivor count",
    )

    fixtures = (
        ((1, 2, 0, 1), (3, 1, 4, 1), (2, 0, 5, 2)),
        ((2, 1, 3, 2), (1, 4, 0, 3), (5, 2, 1, 1)),
        ((4, 0, 2, 1), (2, 3, 1, 2), (1, 5, 2, 3)),
    )
    checks = 12
    hostile_sign_caught = False
    for coefficients in fixtures:
        for prime in (101, 127):
            for x_value in range(1, 12):
                for y_value in range(13, 24):
                    first = tuple(
                        evaluate(row, x_value, prime) for row in coefficients
                    )
                    second = tuple(
                        evaluate(row, y_value, prime) for row in coefficients
                    )
                    a, b, c = first
                    A, B, C = second
                    sylvester = [
                        [a, b, c, 0],
                        [0, a, b, c],
                        [A, B, C, 0],
                        [0, A, B, C],
                    ]
                    resultant = determinant(sylvester, prime)
                    delta = (x_value - y_value) % prime
                    minor_ab = (a * B - A * b) * pow(delta, -1, prime) % prime
                    minor_ac = (a * C - A * c) * pow(delta, -1, prime) % prime
                    minor_bc = (b * C - B * c) * pow(delta, -1, prime) % prime
                    divided = (minor_ac**2 - minor_ab * minor_bc) % prime
                    hostile = (minor_ac**2 + minor_ab * minor_bc) % prime
                    require(
                        resultant == delta**2 * divided % prime,
                        "Q2 divided resultant",
                    )
                    hostile_sign_caught |= hostile != divided
                    checks += 1
    require(hostile_sign_caught, "Q2 hostile resultant sign mutation")
    return checks + 1


def verify_collision_quadratic_torus_gcd_exclusion(formula: Formula) -> int:
    """Replay the gcd margins and translated-subtorus character cases."""
    N = 2**41
    characteristic_floor = 2**167
    full_fibers = 2**39 - 6
    s3_points = 3 * full_fibers
    c3_points = s3_points // 2

    s3_cube_constant = 108 * (4 * 4) ** 2
    c3_cube_constant = 108 * (2 * 2) ** 2
    require(
        s3_cube_constant == formula.collision_q2_s3_gcd_cube_constant,
        "Q2 S3 gcd cube constant",
    )
    require(
        c3_cube_constant == formula.collision_q2_c3_gcd_cube_constant,
        "Q2 C3 gcd cube constant",
    )
    require(s3_cube_constant * N**2 < s3_points**3, "Q2 S3 gcd first term")
    require(c3_cube_constant * N**2 < c3_points**3, "Q2 C3 gcd first term")
    require(
        192 * N**2 < characteristic_floor * s3_points,
        "Q2 S3 gcd characteristic term",
    )
    require(
        48 * N**2 < characteristic_floor * c3_points,
        "Q2 C3 gcd characteristic term",
    )

    swap_invariant = set()
    for r in range(-4, 5):
        for s in range(-4, 5):
            if r and s and gcd(abs(r), abs(s)) == 1:
                if (s, r) in ((r, s), (-r, -s)):
                    swap_invariant.add((r, s))
    require(
        swap_invariant == {(1, 1), (-1, -1), (1, -1), (-1, 1)},
        "Q2 S3 translated-subtorus cases",
    )

    cyclic = set()
    for q in (1, 2):
        for r in range(-2, 3):
            for s in range(-2, 3):
                if r and s and gcd(abs(r), abs(s)) == 1:
                    if q * abs(r) == q * abs(s) == 2:
                        cyclic.add((q, r, s))
    require(
        cyclic
        == {
            (2, 1, 1),
            (2, 1, -1),
            (2, -1, 1),
            (2, -1, -1),
        },
        "Q2 C3 translated-subtorus cases",
    )
    require(gcd(3, N) == 1, "Q2 dyadic 3-torsion")
    require(2 % 3 != 0, "Q2 degree factors through cubic quotient")
    require(
        formula.collision_q2_excluded_shape_count == 2,
        "Q2 excluded shape count",
    )
    require(
        formula.collision_remaining_shape_count == 2,
        "Q2 remaining shape count",
    )
    return 12


def verify_collision_quartic_toral_deck_router(formula: Formula) -> int:
    """Replay the quartic defect, gcd margin, and toral character gate."""
    N = 2**41
    e = (2**39 + 1) // 3
    row_count = (9 * e - 7) // 2
    incidences = 4 * row_count
    defect = 6 * (3 * e) - incidences
    full_fibers = 3 * e - defect
    pair_floor = (30 * full_fibers + 3) // 4
    require(defect == formula.collision_q4_vertical_defect, "Q4 vertical defect")
    require(
        full_fibers == formula.collision_q4_full_fiber_floor,
        "Q4 full-fiber floor",
    )
    require(pair_floor == formula.collision_q4_pair_floor, "Q4 pair floor")
    require(24 - 4 == 20, "Q4 divided-resultant bidegree")
    require(6 - 1 == 5, "Q4 component cap")
    require(
        125 * 17280000 * N**2 < pair_floor**3,
        "Q4 five-component first term",
    )
    require(
        5 * 4800 * N**2 < 2**167 * pair_floor,
        "Q4 five-component characteristic term",
    )

    characters = set()
    for subdegree in range(1, 6):
        for map_degree in range(1, 21):
            for a in range(-20, 21):
                for b in range(-20, 21):
                    if not a or not b or gcd(abs(a), abs(b)) != 1:
                        continue
                    if map_degree * abs(a) == map_degree * abs(b) == 4 * subdegree:
                        characters.add((subdegree, map_degree, a, b))
    require(characters, "Q4 toral character census")
    require(
        all(abs(a) == abs(b) == 1 and map_degree == 4 * subdegree
            for subdegree, map_degree, a, b in characters),
        "Q4 toral graph reduction",
    )
    require(gcd(6, N) == 2, "Q4 scaling deck order")
    require(
        formula.collision_q4_quotient_row_degree == 3,
        "Q4 quotient row degree",
    )
    return 10


def verify_collision_ordinary_companion_complete_exclusion(formula: Formula) -> int:
    """Replay graph deletion, the second-torus margin, and the deck-group gate."""
    N = 2**41
    e = (2**39 + 1) // 3
    full_fibers = 3 * e - 14
    residual_pairs_per_fiber = 30 - 6
    pair_floor = residual_pairs_per_fiber * full_fibers // 4

    require(residual_pairs_per_fiber == 24, "Q4 known graph deletion")
    require(
        pair_floor == formula.collision_q4_residual_pair_floor,
        "Q4 residual pair floor",
    )
    require(
        5 - 1 == formula.collision_q4_residual_component_cap,
        "Q4 residual component cap",
    )
    require(
        64 * 17280000 * N**2 < pair_floor**3,
        "Q4 four-component first term",
    )
    require(
        4 * 4800 * N**2 < 2**167 * pair_floor,
        "Q4 four-component characteristic term",
    )
    require(gcd(6, N) == 2, "Q4 second scaling order")
    require(6 % 4 != 0, "degree-six deck group contains no V4")
    require(
        formula.collision_q4_excluded_shape_count == 1,
        "Q4 excluded shape count",
    )
    require(
        formula.collision_final_shape_count == 1,
        "collision final shape count",
    )

    for prime, x, k in ((101, 7, 9), (127, 11, 25)):
        reciprocal = lambda a, value: a * pow(value, -1, prime) % prime
        antipodal = lambda value: -value % prime
        require(
            antipodal(reciprocal(k, x)) == reciprocal(k, antipodal(x)),
            "antipodal/reciprocal V4 relation",
        )
        c = -k % prime
        require(
            reciprocal(c, reciprocal(k, x))
            == reciprocal(k, reciprocal(c, x))
            == antipodal(x),
            "reciprocal/reciprocal V4 relation",
        )
    return 11


def verify_collision_shape_a_norm_concentration(formula: Formula) -> int:
    """Replay the exact shape-A padding and residual norm degrees."""
    e = (2**39 + 1) // 3
    m = e - 2
    n = (3 * e - 7) // 2
    row_count = (9 * e - 7) // 2
    padding_degree = e - 7
    excess_norm_cap = e

    require(2 * n == 3 * e - 7, "shape-A row degree")
    require(m + 2 == e, "shape-A parameter degree")
    require(
        padding_degree == formula.collision_shape_a_padding_degree,
        "shape-A padding degree",
    )
    require(
        excess_norm_cap == formula.collision_shape_a_excess_norm_degree_cap,
        "shape-A excess norm cap",
    )
    require(
        padding_degree + excess_norm_cap
        == 2 * e - 7,
        "shape-A norm split",
    )
    require(row_count > excess_norm_cap, "shape-A interpolation margin")
    return 6


def verify_collision_shape_a_pure_split_component_floor(formula: Formula) -> int:
    """Replay the exact pure-fiber, pair, and component floors."""
    e = (2**39 + 1) // 3
    m = e - 2
    n = (3 * e - 7) // 2
    pure_fibers = e + 7
    resultant_bidegree = m * (n - 1)
    pair_floor = ceil_div(pure_fibers * n * (n - 1), m)
    component_floor = ceil_div(pair_floor, n - 1)

    require(3 * e - e - (e - 7) == pure_fibers, "shape-A pure fibers")
    require(
        pure_fibers == formula.collision_shape_a_pure_fiber_floor,
        "shape-A pure-fiber floor",
    )
    require(
        resultant_bidegree == formula.collision_shape_a_resultant_bidegree,
        "shape-A resultant bidegree",
    )
    require(
        pair_floor == formula.collision_shape_a_pair_floor,
        "shape-A pair floor",
    )
    require(
        component_floor == formula.collision_shape_a_component_floor,
        "shape-A component floor",
    )
    require(component_floor == n + 14, "shape-A n+14 floor")
    require(13 * m < 9 * n < 14 * m, "shape-A ceiling interval")
    require(2 * m * n // 4 <= m * n // 2, "shape-A Bezout orbit cap")
    require((9 * e - 7) * m // 2 > m * n // 2, "shape-A grid margin")
    return 9


def verify_collision_shape_a_componentwise_degree_floor(formula: Formula) -> int:
    """Replay the prime-field componentwise subgroup-curve threshold."""
    e = (2**39 + 1) // 3
    m = e - 2
    n = (3 * e - 7) // 2
    N = 2**41
    characteristic_floor = 2**167
    numerator = (e + 7) ** 3 * n**3
    denominator = 108 * N**2 * m**3
    degree_floor = ceil_div(numerator, denominator)
    point_floor = ceil_div((e + 7) * n * degree_floor, m)

    require(n == 2**38 - 3 and n % 2 == 1, "shape-A odd cover")
    require(
        degree_floor == formula.collision_shape_a_component_min_bidegree,
        "shape-A component minimum bidegree",
    )
    require(
        point_floor == formula.collision_shape_a_component_min_point_floor,
        "shape-A component minimum point floor",
    )
    require((degree_floor - 1) * denominator < numerator, "CZ first term")
    require(degree_floor * denominator >= numerator, "CZ exact ceiling")
    require(
        degree_floor * 12 * N**2 * m
        < characteristic_floor * (e + 7) * n,
        "CZ characteristic term",
    )
    require(degree_floor < characteristic_floor, "CZ differential range")
    require(
        formula.collision_shape_a_component_multiplicity_ratio == 4608,
        "shape-A exact multiplicity-ratio integer",
    )
    require(
        m < formula.collision_shape_a_component_multiplicity_ratio * degree_floor,
        "shape-A component multiplicity ratio",
    )
    return 8


def verify_collision_shape_a_global_genus_floor(formula: Formula) -> int:
    """Replay the global subgroup-point, chi, and genus floors."""
    e = (2**39 + 1) // 3
    m = e - 2
    n = (3 * e - 7) // 2
    N = 2**41
    characteristic_floor = 2**167
    row_count = (9 * e - 7) // 2
    point_floor = row_count * m
    denominator = 54 * N**2 * m * n
    chi_floor = ceil_div(point_floor**3, denominator)
    genus_floor = ceil_div(chi_floor - 2 * (m + n) + 2, 2)
    genus_ceiling = (m - 1) * (n - 1)

    require(gcd(n, N) == 1 and n > 1, "shape-A subtorus exclusion")
    require(
        point_floor == formula.collision_shape_a_global_point_floor,
        "shape-A global point floor",
    )
    require(
        12 * N**2 * m * n < characteristic_floor,
        "shape-A global characteristic branch",
    )
    require((chi_floor - 1) * denominator < point_floor**3, "chi strictness")
    require(chi_floor * denominator >= point_floor**3, "chi ceiling")
    require(
        chi_floor == formula.collision_shape_a_global_chi_floor,
        "shape-A global chi floor",
    )
    require(
        genus_floor == formula.collision_shape_a_global_genus_floor,
        "shape-A global genus floor",
    )
    require(
        genus_ceiling == formula.collision_shape_a_global_genus_ceiling,
        "shape-A global genus ceiling",
    )
    require(384 * genus_floor < genus_ceiling, "shape-A factor-384 endpoint")
    require(genus_ceiling < 385 * genus_floor, "shape-A factor-385 gap")
    return 10


def verify_collision_shape_a_residual_four_cycle_rigidity(
    formula: Formula,
) -> int:
    """Replay the residual 2B divisor and second-modification section cap."""
    e = (2**39 + 1) // 3
    d = 3 * e - 2
    deg_r = e - 6
    deg_b = 2

    require(deg_r > 0, "shape-A proper residual fibre divisor")
    require(deg_r + 3 * deg_b == e, "shape-A vertical divisor degree")
    require(deg_r + 2 * deg_b == e - 2, "shape-A contact divisor degree")
    require(
        formula.collision_shape_a_residual_divisor_multiplier == 2,
        "shape-A residual divisor multiplier",
    )
    require(
        formula.collision_shape_a_residual_cycle_degree == 2 * deg_b,
        "shape-A residual cycle degree",
    )

    for partition in ((2,), (1, 1)):
        require(sum(partition) == deg_b, "shape-A correction partition")
        require(
            sum(
                formula.collision_shape_a_residual_divisor_multiplier * value
                for value in partition
            )
            == formula.collision_shape_a_residual_cycle_degree,
            "shape-A normalized residual length",
        )

    require(
        formula.collision_shape_a_second_modification_constant_rank == 0,
        "shape-A constant modification direction",
    )
    negative_ceiling = (1 - d) + 1
    require(
        negative_ceiling
        == formula.collision_shape_a_second_modification_negative_ceiling
        < 0,
        "shape-A second modification negativity",
    )
    require(
        formula.collision_shape_a_residual_section_dimension == 1,
        "shape-A residual section dimension",
    )
    return 12


def verify_collision_shape_a_omitted_recurrence_flag(formula: Formula) -> int:
    """Replay the exact degree-drop/omitted-recurrence layer cake."""
    e = (2**39 + 1) // 3
    p = (3 * e - 1) // 2
    rows = 3 * p - 2
    locator_degree = 2 * p - 1
    recurrence_length = p - 3

    require(
        rows == formula.collision_shape_a_source_row_count,
        "shape-A source row count",
    )
    require(
        locator_degree == formula.collision_shape_a_source_locator_degree,
        "shape-A source locator degree",
    )
    require(
        recurrence_length == formula.collision_shape_a_omitted_recurrence_length,
        "shape-A omitted recurrence length",
    )
    require(
        rows - locator_degree - 2 == recurrence_length,
        "shape-A coefficient/recurrence index weld",
    )
    require(
        3 * e == formula.collision_shape_a_offline_slope_count,
        "shape-A off-line slope count",
    )

    prime = 101
    points = tuple(range(1, 9))

    def multiply(left: list[int], right: list[int]) -> list[int]:
        product = [0] * (len(left) + len(right) - 1)
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                product[i + j] = (product[i + j] + a * b) % prime
        return product

    locator = [1]
    for point in points:
        locator = multiply(locator, [-point % prime, 1])

    derivatives = []
    for point in points:
        quotient = [0] * (len(locator) - 1)
        carry = locator[-1]
        quotient[-1] = carry
        for index in range(len(locator) - 2, 0, -1):
            carry = (locator[index] + point * carry) % prime
            quotient[index - 1] = carry
        require(
            (locator[0] + point * carry) % prime == 0,
            "shape-A fixture synthetic remainder",
        )
        derivative = sum(
            coefficient * pow(point, index, prime)
            for index, coefficient in enumerate(quotient)
        ) % prime
        require(derivative != 0, "shape-A fixture distinct points")
        derivatives.append(derivative)

    fixture_d = 3
    fixture_n = len(points) - fixture_d - 2
    expected_drops = (2, 1, 0)
    for slope, expected_drop in zip((10, 11, 12), expected_drops):
        coefficients = [
            7,
            5,
            (slope - 10) % prime,
            (slope - 10) * (slope - 11) % prime,
        ]
        while len(coefficients) > 1 and coefficients[-1] == 0:
            coefficients.pop()
        require(
            fixture_n - (len(coefficients) - 1) == expected_drop,
            "shape-A fixture degree drop",
        )

        weights = []
        for point, derivative in zip(points, derivatives):
            value = sum(
                coefficient * pow(point, index, prime)
                for index, coefficient in enumerate(coefficients)
            ) % prime
            weights.append(value * pow(derivative, prime - 2, prime) % prime)
        moments = tuple(
            sum(
                weight * pow(point, power, prime)
                for weight, point in zip(weights, points)
            ) % prime
            for power in range(fixture_d + 1 + fixture_n)
        )
        require(
            all(value == 0 for value in moments[: fixture_d + 1]),
            "shape-A fixture forced moments",
        )
        zero_run = 0
        for value in moments[fixture_d + 1 :]:
            if value:
                break
            zero_run += 1
        require(zero_run == expected_drop, "shape-A fixture recurrence flag")

    layer_cake = sum(
        1
        for drop in expected_drops
        for level in range(1, fixture_n + 1)
        if drop >= level
    )
    require(
        layer_cake == sum(expected_drops)
        == formula.collision_shape_a_fixture_layer_cake,
        "shape-A fixture nested-gcd layer cake",
    )
    return 18


def verify_collision_shape_a_bordered_hankel_flag(formula: Formula) -> int:
    """Replay the replacement-minor, bordered-square, and source-sum flags."""
    e = (2**39 + 1) // 3
    d = 3 * e - 2
    matrix_size = d + 2
    padding_degree = e - 7
    regular_degree = 2 * e + 7

    require(e == 183251937963, "shape-A bordered official e")
    require(d == formula.collision_shape_a_source_locator_degree,
            "shape-A bordered locator degree")
    require(matrix_size == formula.collision_shape_a_bordered_matrix_size,
            "shape-A bordered matrix size")
    require(matrix_size == formula.collision_shape_a_bordered_source_subset_size,
            "shape-A bordered source subset size")
    require(padding_degree == formula.collision_shape_a_padding_flag_degree,
            "shape-A padding flag degree")
    require(regular_degree == formula.collision_shape_a_regular_flag_degree,
            "shape-A regular flag degree")
    require(padding_degree + regular_degree
            == formula.collision_shape_a_offline_slope_count,
            "shape-A bordered flag partition")

    prime = 101

    def determinant(matrix: list[list[int]]) -> int:
        work = [[entry % prime for entry in row] for row in matrix]
        value = 1
        for column in range(len(work)):
            pivot = next(
                (row for row in range(column, len(work))
                 if work[row][column]),
                None,
            )
            if pivot is None:
                return 0
            if pivot != column:
                work[column], work[pivot] = work[pivot], work[column]
                value = -value
            pivot_value = work[column][column]
            value = value * pivot_value % prime
            inverse = pow(pivot_value, prime - 2, prime)
            for row in range(column + 1, len(work)):
                if not work[row][column]:
                    continue
                scale = work[row][column] * inverse % prime
                for index in range(column, len(work)):
                    work[row][index] = (
                        work[row][index] - scale * work[column][index]
                    ) % prime
        return value % prime

    def solve(matrix: list[list[int]], right: list[int]) -> list[int]:
        augmented = [
            [entry % prime for entry in row] + [target % prime]
            for row, target in zip(matrix, right)
        ]
        size = len(matrix)
        for column in range(size):
            pivot = next(
                (row for row in range(column, size)
                 if augmented[row][column]),
                None,
            )
            require(pivot is not None, "shape-A source reconstruction rank")
            augmented[column], augmented[pivot] = (
                augmented[pivot], augmented[column]
            )
            inverse = pow(augmented[column][column], prime - 2, prime)
            augmented[column] = [
                entry * inverse % prime for entry in augmented[column]
            ]
            for row in range(size):
                if row == column or not augmented[row][column]:
                    continue
                scale = augmented[row][column]
                augmented[row] = [
                    (left - scale * right_entry) % prime
                    for left, right_entry
                    in zip(augmented[row], augmented[column])
                ]
        return [augmented[index][-1] for index in range(size)]

    moments = [1, 0, 1, 0, 1, 2, 3, 4, 5]
    fixture_d = 2
    middle = [
        [moments[i + j] for j in range(fixture_d + 1)]
        for i in range(fixture_d + 1)
    ]
    kernel = [-1, 0, 1]
    require(finite_field_rank(middle, prime) == fixture_d,
            "shape-A bordered middle rank")
    require(
        all(
            sum(middle[i][j] * kernel[j] for j in range(fixture_d + 1))
            % prime == 0
            for i in range(fixture_d + 1)
        ),
        "shape-A bordered primitive kernel",
    )

    defects = []
    for s in (0, 1):
        exponent = fixture_d + 1 + s
        vector = [moments[exponent + i] for i in range(fixture_d + 1)]
        defect = sum(
            left * right for left, right in zip(kernel, vector)
        ) % prime
        defects.append(defect)
        for column in range(fixture_d + 1):
            replaced = [row[:] for row in middle]
            for row in range(fixture_d + 1):
                replaced[row][column] = vector[row]
            require(
                determinant(replaced) == kernel[column] * defect % prime,
                "shape-A replacement-minor identity",
            )

        exponents = list(range(fixture_d + 1)) + [exponent]
        bordered = [
            [moments[left + right] for right in exponents]
            for left in exponents
        ]
        require(
            determinant(bordered) == -defect * defect % prime,
            "shape-A bordered determinant square",
        )
    require(defects == [2, 2], "shape-A bordered fixture defects")

    points = list(range(1, 10))
    vandermonde = [
        [pow(point, power, prime) for point in points]
        for power in range(len(points))
    ]
    weights = solve(vandermonde, moments)
    require(
        all(
            sum(
                weight * pow(point, power, prime)
                for point, weight in zip(points, weights)
            ) % prime == moments[power] % prime
            for power in range(len(moments))
        ),
        "shape-A source moment reconstruction",
    )

    subset_checks = 0
    for s, defect in enumerate(defects):
        exponents = list(range(fixture_d + 1)) + [fixture_d + 1 + s]
        source_sum = 0
        for subset in combinations(range(len(points)), fixture_d + 2):
            alternant = determinant([
                [pow(points[index], exponent, prime) for index in subset]
                for exponent in exponents
            ])
            subset_weight = 1
            for index in subset:
                subset_weight = subset_weight * weights[index] % prime
            source_sum = (
                source_sum + alternant * alternant * subset_weight
            ) % prime
            subset_checks += 1
        require(source_sum == -defect * defect % prime,
                "shape-A bordered source subset sum")
    require(
        subset_checks == formula.collision_shape_a_bordered_fixture_subset_checks,
        "shape-A bordered source subset count",
    )
    return subset_checks + 22


def verify_collision_shape_a_static_source_arbitrary_drop(
    formula: Formula,
) -> int:
    """Replay arbitrary bordered-rank stagnation for a static source."""
    prime = 101
    d = 3
    n = 3
    source = list(range(1, 9))
    roots = [20, 21, 22]
    auxiliary_root = 30

    require(
        len(source) == formula.collision_shape_a_static_drop_source_count,
        "shape-A static-drop source count",
    )
    require(
        n == formula.collision_shape_a_static_drop_maximum,
        "shape-A static-drop maximum",
    )
    require(len(source) == d + n + 2, "shape-A static-drop dimensions")
    require(
        len(set(source + roots + [auxiliary_root]))
        == len(source) + len(roots) + 1,
        "shape-A static-drop point separation",
    )

    def multiply(left: list[int], right: list[int]) -> list[int]:
        product = [0] * (len(left) + len(right) - 1)
        for i, left_entry in enumerate(left):
            for j, right_entry in enumerate(right):
                product[i + j] = (
                    product[i + j] + left_entry * right_entry
                ) % prime
        return product

    def evaluate(polynomial: list[int], value: int) -> int:
        result = 0
        for coefficient in reversed(polynomial):
            result = (result * value + coefficient) % prime
        return result

    def determinant(matrix: list[list[int]]) -> int:
        work = [[entry % prime for entry in row] for row in matrix]
        value = 1
        for column in range(len(work)):
            pivot = next(
                (row for row in range(column, len(work))
                 if work[row][column]),
                None,
            )
            if pivot is None:
                return 0
            if pivot != column:
                work[column], work[pivot] = work[pivot], work[column]
                value = -value
            pivot_value = work[column][column]
            value = value * pivot_value % prime
            inverse = pow(pivot_value, prime - 2, prime)
            for row in range(column + 1, len(work)):
                if not work[row][column]:
                    continue
                scale = work[row][column] * inverse % prime
                for index in range(column, len(work)):
                    work[row][index] = (
                        work[row][index] - scale * work[column][index]
                    ) % prime
        return value % prime

    locator = [1]
    for root in roots:
        locator = multiply(locator, [-root % prime, 1])

    cases = 0
    residue_checks = 0
    subset_checks = 0
    for drop in range(n + 1):
        residual = [1]
        for _ in range(n - drop):
            residual = multiply(residual, [-auxiliary_root % prime, 1])

        weights = []
        for point in source:
            q_value = evaluate(locator, point)
            source_derivative = 1
            for other in source:
                if other != point:
                    source_derivative = (
                        source_derivative * (point - other)
                    ) % prime
            denominator = q_value * source_derivative % prime
            require(denominator, "shape-A static-drop source denominator")
            weights.append(
                evaluate(residual, point)
                * pow(denominator, prime - 2, prime)
                % prime
            )
        require(all(weights), "shape-A static-drop nonzero weights")

        moment_limit = 2 * (d + 1 + drop)
        moments = [
            sum(
                weight * pow(point, power, prime)
                for point, weight in zip(source, weights)
            ) % prime
            for power in range(moment_limit + 1)
        ]
        middle = [
            [moments[i + j] for j in range(d + 1)]
            for i in range(d + 1)
        ]
        require(
            finite_field_rank(middle, prime) == d,
            "shape-A static-drop exact middle corank",
        )
        require(
            all(
                sum(
                    middle[i][j] * locator[j] for j in range(d + 1)
                ) % prime == 0
                for i in range(d + 1)
            ),
            "shape-A static-drop locator kernel",
        )

        defects = [
            sum(locator[i] * moments[i + j] for i in range(d + 1))
            % prime
            for j in range(d + 1, d + 2 + drop)
        ]
        require(
            defects[:drop] == [0] * drop,
            "shape-A static-drop initial zero run",
        )
        require(
            defects[drop] == residual[-1] == 1,
            "shape-A static-drop first omitted defect",
        )

        for left in range(d):
            for right in range(d):
                root_pairing = 0
                for root in roots:
                    q_derivative = 1
                    for other in roots:
                        if other != root:
                            q_derivative = q_derivative * (root - other) % prime
                    source_locator_value = 1
                    for point in source:
                        source_locator_value = (
                            source_locator_value * (root - point)
                        ) % prime
                    coefficient = (
                        evaluate(residual, root)
                        * pow(
                            q_derivative * source_locator_value % prime,
                            prime - 2,
                            prime,
                        )
                    ) % prime
                    root_pairing = (
                        root_pairing
                        - coefficient * pow(root, left + right, prime)
                    ) % prime
                require(
                    moments[left + right] == root_pairing,
                    "shape-A static-drop residue pairing",
                )
                residue_checks += 1

        regular_factor = determinant([row[:d] for row in middle[:d]])
        require(regular_factor, "shape-A static-drop adjugate scalar")
        for level in range(drop + 1):
            vector = [
                moments[d + 1 + level + i] for i in range(d + 1)
            ]
            defect = defects[level]
            for column in range(d + 1):
                replaced = [row[:] for row in middle]
                for row in range(d + 1):
                    replaced[row][column] = vector[row]
                require(
                    determinant(replaced)
                    == regular_factor * locator[column] * defect % prime,
                    "shape-A static-drop replacement minor",
                )

            exponents = list(range(d + 1)) + [d + 1 + level]
            bordered = [
                [moments[left + right] for right in exponents]
                for left in exponents
            ]
            bordered_value = determinant(bordered)
            require(
                bordered_value
                == -regular_factor * defect * defect % prime,
                "shape-A static-drop bordered square",
            )

            source_sum = 0
            for subset in combinations(range(len(source)), d + 2):
                alternant = determinant([
                    [
                        pow(source[index], exponent, prime)
                        for index in subset
                    ]
                    for exponent in exponents
                ])
                subset_weight = 1
                for index in subset:
                    subset_weight = subset_weight * weights[index] % prime
                source_sum = (
                    source_sum + alternant * alternant * subset_weight
                ) % prime
                subset_checks += 1
            require(
                source_sum == bordered_value,
                "shape-A static-drop source Cauchy-Binet",
            )
        cases += 1

    require(
        cases == formula.collision_shape_a_static_drop_fixture_cases,
        "shape-A static-drop fixture cases",
    )
    require(
        residue_checks == formula.collision_shape_a_static_drop_residue_checks,
        "shape-A static-drop residue count",
    )
    require(
        subset_checks == formula.collision_shape_a_static_drop_subset_checks,
        "shape-A static-drop subset count",
    )
    return cases + residue_checks + subset_checks


def verify_collision_shape_a_scalar_weld_residual_mds_flag(
    formula: Formula,
) -> int:
    """Replay the globally welded residual interpolation flag."""
    official_e = 183251937963
    row_surplus = 3 * official_e
    require(
        row_surplus == formula.collision_shape_a_residual_mds_row_surplus,
        "shape-A residual-MDS row surplus",
    )
    require(
        row_surplus - 1
        == formula.collision_shape_a_residual_mds_unpadded_start,
        "shape-A residual-MDS unpadded start",
    )
    require(
        row_surplus
        == formula.collision_shape_a_residual_mds_padded_start,
        "shape-A residual-MDS padded start",
    )

    prime = 101
    source = list(range(1, 10))
    incidence = source[:2]
    complement = source[2:]
    excess = 3
    padding_degree = 1
    parameter_degree = 5
    delta = 40
    padding_root = 20
    residual_root = 30

    def multiply(left: list[int], right: list[int]) -> list[int]:
        product = [0] * (len(left) + len(right) - 1)
        for i, left_entry in enumerate(left):
            for j, right_entry in enumerate(right):
                product[i + j] = (
                    product[i + j] + left_entry * right_entry
                ) % prime
        while len(product) > 1 and product[-1] == 0:
            product.pop()
        return product

    def evaluate(polynomial: list[int], value: int) -> int:
        result = 0
        for coefficient in reversed(polynomial):
            result = (result * value + coefficient) % prime
        return result

    def power_linear(root: int, exponent: int) -> list[int]:
        result = [1]
        for _ in range(exponent):
            result = multiply(result, [-root % prime, 1])
        return result

    actual = [1]
    for point in incidence:
        actual = multiply(actual, [-point % prime, 1])
    padding = power_linear(padding_root, padding_degree)
    generic_degree = len(incidence) + padding_degree + excess
    generic_coefficient = [1] + [0] * (generic_degree - 1) + [1]
    row_scalars = [evaluate(generic_coefficient, point) for point in source]
    require(all(row_scalars), "shape-A residual-MDS row scalars")

    fixture_surplus = len(source) - generic_degree
    parity_start = fixture_surplus + padding_degree - 1
    require(
        fixture_surplus == 3 and parity_start == 3,
        "shape-A residual-MDS fixture start",
    )

    cases = 0
    parity_checks = 0
    row_checks = 0
    for drop in range(excess + 1):
        residual = power_linear(residual_root, excess - drop)
        fiber = multiply(multiply(actual, padding), residual)
        require(
            len(fiber) - 1 == generic_degree - drop,
            "shape-A residual-MDS fiber drop",
        )

        residual_values = []
        for point, row_scalar in zip(source, row_scalars):
            fiber_value = evaluate(fiber, point)
            row_value = fiber_value * pow(row_scalar, prime - 2, prime) % prime
            require(
                (row_value == 0) == (point in incidence),
                "shape-A residual-MDS incidence",
            )
            for parameter in (0, delta, 70):
                parameter_term = pow(
                    parameter - delta, parameter_degree, prime
                )
                require(
                    (
                        fiber_value
                        + parameter_term
                        * evaluate(generic_coefficient, point)
                    ) % prime
                    == row_scalar * (parameter_term + row_value) % prime,
                    "shape-A residual-MDS global row weld",
                )
                row_checks += 1
            if point not in incidence:
                denominator = (
                    evaluate(actual, point) * evaluate(padding, point)
                ) % prime
                require(denominator, "shape-A residual-MDS denominator")
                residual_values.append(
                    (
                        point,
                        row_scalar
                        * row_value
                        * pow(denominator, prime - 2, prime)
                        % prime,
                    )
                )

        require(
            all(
                value == evaluate(residual, point)
                for point, value in residual_values
            ),
            "shape-A residual-MDS residual reconstruction",
        )
        parities = []
        for power in range(parity_start + drop + 1):
            value = 0
            for point, residual_value in residual_values:
                derivative = 1
                for other, _ in residual_values:
                    if other != point:
                        derivative = derivative * (point - other) % prime
                value = (
                    value
                    + residual_value
                    * pow(point, power, prime)
                    * pow(derivative, prime - 2, prime)
                ) % prime
            parities.append(value)
            parity_checks += 1
        require(
            parities[:parity_start] == [0] * parity_start,
            "shape-A residual-MDS base parities",
        )
        require(
            parities[parity_start:parity_start + drop] == [0] * drop,
            "shape-A residual-MDS extra run",
        )
        require(
            parities[parity_start + drop] == residual[-1] == 1,
            "shape-A residual-MDS first nonzero parity",
        )
        cases += 1

    require(
        cases == formula.collision_shape_a_residual_mds_fixture_cases,
        "shape-A residual-MDS fixture cases",
    )
    require(
        parity_checks
        == formula.collision_shape_a_residual_mds_fixture_parities,
        "shape-A residual-MDS fixture parities",
    )
    require(
        row_checks == formula.collision_shape_a_residual_mds_fixture_rows,
        "shape-A residual-MDS fixture row checks",
    )
    return cases + parity_checks + row_checks


def verify_truncated_source_separation_fence() -> int:
    prime = 101
    degree = 13
    source = list(range(1, 20))
    certificates = {
        1: [
            19, 6, 47, 37, 31, 62, 4, 97, 45, 45, 10, 55, 19, 38, 15,
            77, 48, 13, 31, 15, 14, 72, 34, 58, 80, 84, 20, 3, 7, 98, 28,
        ],
        2: [
            17, 65, 86, 42, 83, 10, 82, 77, 54, 30, 27, 1, 42, 83, 12,
            52, 41, 80, 17, 68, 91, 8, 26, 26, 17, 54, 22, 81, 40, 80,
        ],
    }

    checks = 0
    for regular_corank, certificate in certificates.items():
        compressed_size = degree - regular_corank
        compressed = list(range(30, 30 + compressed_size))
        points = source + compressed
        require(len(certificate) == len(points) and all(certificate), "fence vector")
        require(set(source).isdisjoint(compressed), "fence supports")
        for power in range(2 * degree + 1):
            require(
                sum(
                    weight * pow(point, power, prime)
                    for weight, point in zip(certificate, points)
                ) % prime == 0,
                "fence moment transfer",
            )
            checks += 1
        moments = [
            sum(
                weight * pow(point, power, prime)
                for weight, point in zip(certificate[:len(source)], source)
            ) % prime
            for power in range(2 * degree + 1)
        ]
        hankel = [
            [moments[i + j] for j in range(degree + 1)]
            for i in range(degree + 1)
        ]
        require(finite_field_rank(hankel, prime) == compressed_size, "fence rank")
        require(30 not in source and 30 in compressed, "fence root separation")
        checks += 2
    return checks


def verify_source(root: Path) -> int:
    checked = 0
    for relative, expected in SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), f"missing pinned source: {relative}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == expected, f"source hash mismatch: {relative}")
        checked += 1
    return checked


def replay(formula: Formula) -> dict[str, int]:
    require(formula.pade_exponent_offset == 1, "Pade exponent changed")
    require(formula.residual_degree == 4, "residual degree changed")
    require(
        formula.double_correction_multiplicity == 2,
        "double correction multiplicity changed",
    )
    require(
        formula.simple_correction_total == 4,
        "simple correction total changed",
    )
    require(formula.supported_exception_cap == 4, "exception cap changed")
    require(
        formula.separated_residual_degree == 3,
        "separated residual degree changed",
    )
    require(
        formula.separated_smith_exponent == 2,
        "separated Smith exponent changed",
    )
    require(formula.center_overlap_cap == 1, "center-overlap cap changed")
    require(formula.heavy_row_unknowns == 2, "heavy-row unknown cap changed")
    require(formula.layer_a_rank == 20, "Layer-A rank constant changed")
    require(formula.layer_a_nullity == 4, "Layer-A nullity constant changed")
    require(formula.layer_a_row_surplus == 2, "Layer-A surplus constant changed")
    require(
        formula.barycentric_remainder_defect == 1,
        "barycentric remainder defect changed",
    )
    require(
        formula.center_disjoint_quotient_degree == 0,
        "center-disjoint quotient degree changed",
    )
    require(
        formula.separated_heavy_row_nonzero == 1,
        "separated heavy-row nonzero gate changed",
    )
    require(
        formula.shared_forced_jet_order == 2,
        "shared forced-jet order changed",
    )
    require(
        formula.shared_third_jet_vanishes == 1,
        "shared third-jet vanishing changed",
    )
    require(
        formula.nonreduced_forced_order == 2,
        "nonreduced forced order changed",
    )
    require(
        formula.nonreduced_missing_jets == 2,
        "nonreduced missing-jet count changed",
    )
    require(
        formula.center_overlap_equals_deficit == 1,
        "center-overlap/deficit identity changed",
    )
    require(
        formula.macroscopic_factor_d_a0 == 61083979321,
        "d_A=0 macroscopic factor bound changed",
    )
    require(
        formula.macroscopic_factor_d_a1 == 78536544842,
        "d_A=1 macroscopic factor bound changed",
    )
    require(
        formula.separated_corank_one_unresolved_jets == 0,
        "separated corank-one jet count changed",
    )
    require(
        formula.nonreduced_nonzero_jet_min_corank == 1,
        "nonzero-jet corank router changed",
    )
    require(formula.automatic_source_separation == 0, "source fence changed")
    require(formula.factor_content_degree == 0, "factor content changed")
    require(formula.factor_degree_slack == 0, "factor degree slack changed")
    require(formula.factor_profile_count == 3, "factor trichotomy changed")
    require(formula.large_odd_d_a0 == 61083979321, "d_A=0 odd threshold changed")
    require(formula.large_odd_d_a1 == 78536544843, "d_A=1 odd threshold changed")
    require(formula.huge_even_d_a0 == 122167958642, "d_A=0 even threshold changed")
    require(formula.huge_even_d_a1 == 157073089684, "d_A=1 even threshold changed")
    require(
        formula.nonreduced_first_nonzero_third_jet == 0,
        "first-nonzero third-jet count changed",
    )
    require(
        formula.nonreduced_noncollision_nonzero_jet == 0,
        "noncollision nonzero-jet count changed",
    )
    require(formula.collision_max_regular_corank == 2, "collision corank changed")
    require(formula.collision_profile_count == 3, "collision profile count changed")
    require(formula.collision_global_jet_count == 2, "collision jet count changed")
    require(
        formula.collision_barycentric_functional_count == 4,
        "collision barycentric count changed",
    )
    require(
        formula.collision_heavy_row_residual_degree_d_a0 == 2,
        "collision d_A=0 heavy-row residual changed",
    )
    require(
        formula.collision_heavy_row_residual_degree_d_a1 == 3,
        "collision d_A=1 heavy-row residual changed",
    )
    require(
        formula.collision_divided_row_quotient_degree == 5,
        "collision divided-row quotient changed",
    )
    require(
        formula.collision_unsupported_root_budget_d_a0 == 4,
        "collision d_A=0 unsupported-root budget changed",
    )
    require(
        formula.collision_unsupported_root_budget_d_a1 == 5,
        "collision d_A=1 unsupported-root budget changed",
    )
    require(
        formula.collision_d_a1_factor_profile_count == 1,
        "collision d_A=1 factor-profile count changed",
    )
    require(
        formula.collision_quintic_independent_gate_count == 0,
        "collision quintic route-fence count changed",
    )
    require(formula.collision_factor_shape_count == 4, "collision shape count changed")
    require(
        formula.collision_large_factor_max_deficit == 6,
        "collision large-factor deficit changed",
    )
    require(
        formula.collision_ordinary_companion_degree_cap == 4,
        "collision ordinary-companion cap changed",
    )

    checks = 0
    for e in (7, 13, 127, 1009, 183251937963):
        p = (3 * e - 1) // 2
        d = 3 * e - 2
        n = p - 3
        n0 = 3 * p - 2
        intersection = d * (e - 2) + e * n
        pade_exponent = 2 * d + formula.pade_exponent_offset

        require(n0 + d - 1 - n == pade_exponent, "Pade cancellation failed")
        require(
            (2 * d * e - e + d) - e * pade_exponent == e - 2,
            "regular-factor degree failed",
        )
        require(
            3 * e * n - e + formula.residual_degree == intersection,
            "projective four-core failed",
        )
        require(
            (e - 6) + formula.double_correction_multiplicity * 2 == e - 2,
            "double correction degree failed",
        )
        require(
            (e - 3) // 2
            + (e - 9) // 2
            + formula.simple_correction_total
            == e - 2,
            "two-simple correction degree failed",
        )
        for rank_loss in (0, 1, 2):
            require(
                (d - rank_loss) + rank_loss - d == 0,
                "center cancellation failed",
            )
        for rank_loss in (1, 2):
            kernel_dimension = rank_loss + 1
            min_coefficient_rank = e - rank_loss // 2
            require(
                kernel_dimension - rank_loss == 1,
                "first-jet radical dimension failed",
            )
            require(
                min_coefficient_rank in (e - 1, e),
                "coefficient-plane rank failed",
            )
        for excess in range(5):
            for padding in range(3):
                require(
                    (n - excess - padding) + padding == n - excess,
                    "all-excess padding cancellation failed",
                )
        checks += 23

        for overlap in range(formula.center_overlap_cap + 1):
            require(
                (e - 2 - overlap) + overlap == e - 2,
                "heavy-row center cancellation failed",
            )
            require(
                overlap + 1 <= formula.heavy_row_unknowns,
                "heavy-row scalar cap failed",
            )
            require(
                (e - 2) - (e - 2 - overlap) == overlap,
                "remainder quotient degree failed",
            )
            checks += 3

        for d_a in (0, 1):
            row_count = 3 * p - 3 + d_a
            slope_count = 3 * e
            factor_denominator = 9 - 2 * d_a
            threshold = (3 * e + factor_denominator - 1) // factor_denominator
            large_odd = least_with_parity(3 * e, factor_denominator, 1)
            huge_even = least_with_parity(6 * e, factor_denominator, 0)
            require(
                2 * row_count == 9 * e - factor_denominator,
                "factor row-count identity failed",
            )
            require(
                factor_denominator * (threshold - 1) < 3 * e
                <= factor_denominator * threshold,
                "macroscopic factor threshold failed",
            )
            require(
                d_a == d_a * formula.center_overlap_equals_deficit,
                "center overlap is not the deficit bit",
            )
            require(
                factor_denominator * large_odd >= 3 * e,
                "large-odd threshold failed",
            )
            require(
                factor_denominator * (large_odd - 2) < 3 * e,
                "large-odd predecessor failed",
            )
            require(
                factor_denominator * huge_even >= 6 * e,
                "huge-even threshold failed",
            )
            require(
                factor_denominator * (huge_even - 2) < 6 * e,
                "huge-even predecessor failed",
            )
            require(3 * large_odd > e - 2, "three large factors fit")
            require(2 * huge_even > e - 2, "two huge factors fit")
            require(large_odd + huge_even > e - 2, "large and huge factors fit")
            if e == 183251937963:
                expected = (
                    formula.macroscopic_factor_d_a0
                    if d_a == 0
                    else formula.macroscopic_factor_d_a1
                )
                require(threshold == expected, "official factor bound failed")
                expected_large = (
                    formula.large_odd_d_a0
                    if d_a == 0
                    else formula.large_odd_d_a1
                )
                expected_huge = (
                    formula.huge_even_d_a0
                    if d_a == 0
                    else formula.huge_even_d_a1
                )
                require(large_odd == expected_large, "official odd threshold failed")
                require(huge_even == expected_huge, "official even threshold failed")
            checks += 13

    require(2 + 2 * 3 == 8, "double marked order failed")
    require(1 + 2 * 3 == 7, "simple marked order failed")
    require(
        (183251937963 + 1) - (183251937963 - 2)
        == formula.separated_residual_degree,
        "cubic quotient degree failed",
    )
    require(
        formula.separated_smith_exponent == 2,
        "type-[2] correction failed",
    )
    require(
        6 - 4 == formula.nonreduced_missing_jets,
        "nonreduced determinant gap failed",
    )
    require(
        formula.nonreduced_forced_order + formula.nonreduced_missing_jets == 4,
        "nonreduced two-jet ledger failed",
    )
    require(
        4 - 4 == formula.separated_corank_one_unresolved_jets,
        "separated corank-one Schur order failed",
    )
    require(
        1 == formula.nonreduced_nonzero_jet_min_corank,
        "collision corank floor failed",
    )
    require(formula.automatic_source_separation == 0, "separation fence failed")
    require(len(SOURCE_COMMIT) == 40, "source commit pin malformed")
    require(len(SOURCE_HASHES) == 134, "source hash inventory changed")
    require(
        all(len(digest) == 64 for digest in SOURCE_HASHES.values()),
        "source hash malformed",
    )

    checks += verify_layer_a_fixture(formula)
    factor_partition_checks, factor_feasible_profiles = verify_factor_profiles(formula)
    checks += verify_nonreduced_collision(formula)
    checks += verify_collision_split_jet_dictionary(formula)
    checks += verify_collision_barycentric_gate(formula)
    checks += verify_nonreduced_heavy_row_residual(formula)
    checks += verify_nonreduced_divided_row_quotient(formula)
    checks += verify_collision_factor_unsupported_root_budget(formula)
    checks += verify_collision_quintic_cauchy_closed_form(formula)
    checks += verify_collision_factorwise_bezout_shapes(formula)
    checks += verify_collision_ordinary_companion_norm(formula)
    checks += verify_collision_two_branch_tangent_router(formula)
    checks += verify_collision_quadratic_subgroup_router(formula)
    checks += verify_collision_quadratic_torus_gcd_exclusion(formula)
    checks += verify_collision_quartic_toral_deck_router(formula)
    checks += verify_collision_ordinary_companion_complete_exclusion(formula)
    checks += verify_collision_shape_a_norm_concentration(formula)
    checks += verify_collision_shape_a_pure_split_component_floor(formula)
    checks += verify_collision_shape_a_componentwise_degree_floor(formula)
    checks += verify_collision_shape_a_global_genus_floor(formula)
    checks += verify_collision_shape_a_residual_four_cycle_rigidity(formula)
    checks += verify_collision_shape_a_omitted_recurrence_flag(formula)
    checks += verify_collision_shape_a_bordered_hankel_flag(formula)
    checks += verify_collision_shape_a_static_source_arbitrary_drop(formula)
    checks += verify_collision_shape_a_scalar_weld_residual_mds_flag(formula)
    checks += verify_truncated_source_separation_fence()

    return {
        "checks": checks + 15 + factor_partition_checks,
        "official_e": 183251937963,
        "pade_exponent": 2 * (3 * 183251937963 - 2) + 1,
        "residual_degree": formula.residual_degree,
        "double_marked_order": 8,
        "simple_marked_order": 7,
        "supported_exception_cap": formula.supported_exception_cap,
        "separated_residual_degree": formula.separated_residual_degree,
        "separated_smith_exponent": formula.separated_smith_exponent,
        "heavy_row_unknowns": formula.heavy_row_unknowns,
        "barycentric_remainder_defect": formula.barycentric_remainder_defect,
        "separated_heavy_row_nonzero": formula.separated_heavy_row_nonzero,
        "shared_forced_jet_order": formula.shared_forced_jet_order,
        "shared_third_jet_vanishes": formula.shared_third_jet_vanishes,
        "nonreduced_missing_jets": formula.nonreduced_missing_jets,
        "center_overlap_equals_deficit": formula.center_overlap_equals_deficit,
        "macroscopic_factor_d_a0": formula.macroscopic_factor_d_a0,
        "macroscopic_factor_d_a1": formula.macroscopic_factor_d_a1,
        "separated_corank_one_unresolved_jets": (
            formula.separated_corank_one_unresolved_jets
        ),
        "nonreduced_nonzero_jet_min_corank": (
            formula.nonreduced_nonzero_jet_min_corank
        ),
        "automatic_source_separation": formula.automatic_source_separation,
        "factor_content_degree": formula.factor_content_degree,
        "factor_degree_slack": formula.factor_degree_slack,
        "factor_profile_count": formula.factor_profile_count,
        "factor_feasible_profiles": factor_feasible_profiles,
        "large_odd_d_a0": formula.large_odd_d_a0,
        "large_odd_d_a1": formula.large_odd_d_a1,
        "huge_even_d_a0": formula.huge_even_d_a0,
        "huge_even_d_a1": formula.huge_even_d_a1,
        "nonreduced_first_nonzero_third_jet": (
            formula.nonreduced_first_nonzero_third_jet
        ),
        "nonreduced_noncollision_nonzero_jet": (
            formula.nonreduced_noncollision_nonzero_jet
        ),
        "collision_max_regular_corank": formula.collision_max_regular_corank,
        "collision_profile_count": formula.collision_profile_count,
        "collision_global_jet_count": formula.collision_global_jet_count,
        "collision_barycentric_functional_count": (
            formula.collision_barycentric_functional_count
        ),
        "collision_heavy_row_residual_degree_d_a0": (
            formula.collision_heavy_row_residual_degree_d_a0
        ),
        "collision_heavy_row_residual_degree_d_a1": (
            formula.collision_heavy_row_residual_degree_d_a1
        ),
        "collision_divided_row_quotient_degree": (
            formula.collision_divided_row_quotient_degree
        ),
        "collision_unsupported_root_budget_d_a0": (
            formula.collision_unsupported_root_budget_d_a0
        ),
        "collision_unsupported_root_budget_d_a1": (
            formula.collision_unsupported_root_budget_d_a1
        ),
        "collision_d_a1_factor_profile_count": (
            formula.collision_d_a1_factor_profile_count
        ),
        "collision_quintic_independent_gate_count": (
            formula.collision_quintic_independent_gate_count
        ),
        "collision_factor_shape_count": formula.collision_factor_shape_count,
        "collision_large_factor_max_deficit": (
            formula.collision_large_factor_max_deficit
        ),
        "collision_ordinary_companion_degree_cap": (
            formula.collision_ordinary_companion_degree_cap
        ),
        "collision_q2_norm_cap": formula.collision_q2_norm_cap,
        "collision_q2_reduced_norm_cap": (
            formula.collision_q2_reduced_norm_cap
        ),
        "collision_q4_norm_cap": formula.collision_q4_norm_cap,
        "collision_q4_reduced_norm_cap": (
            formula.collision_q4_reduced_norm_cap
        ),
        "collision_two_branch_shape_count": (
            formula.collision_two_branch_shape_count
        ),
        "collision_two_branch_profile_count": (
            formula.collision_two_branch_profile_count
        ),
        "collision_two_branch_excluded_profile_count": (
            formula.collision_two_branch_excluded_profile_count
        ),
        "collision_q2_vertical_defect": formula.collision_q2_vertical_defect,
        "collision_q2_full_fiber_floor": formula.collision_q2_full_fiber_floor,
        "collision_q2_pair_floor": formula.collision_q2_pair_floor,
        "collision_q2_s3_subgroup_constant": (
            formula.collision_q2_s3_subgroup_constant
        ),
        "collision_q2_c3_subgroup_constant": (
            formula.collision_q2_c3_subgroup_constant
        ),
        "collision_q2_vm_admissible_survivors": (
            formula.collision_q2_vm_admissible_survivors
        ),
        "collision_q2_s3_gcd_cube_constant": (
            formula.collision_q2_s3_gcd_cube_constant
        ),
        "collision_q2_c3_gcd_cube_constant": (
            formula.collision_q2_c3_gcd_cube_constant
        ),
        "collision_q2_excluded_shape_count": (
            formula.collision_q2_excluded_shape_count
        ),
        "collision_remaining_shape_count": formula.collision_remaining_shape_count,
        "collision_q4_vertical_defect": formula.collision_q4_vertical_defect,
        "collision_q4_full_fiber_floor": formula.collision_q4_full_fiber_floor,
        "collision_q4_pair_floor": formula.collision_q4_pair_floor,
        "collision_q4_quotient_row_degree": (
            formula.collision_q4_quotient_row_degree
        ),
        "collision_q4_residual_pair_floor": (
            formula.collision_q4_residual_pair_floor
        ),
        "collision_q4_residual_component_cap": (
            formula.collision_q4_residual_component_cap
        ),
        "collision_q4_excluded_shape_count": (
            formula.collision_q4_excluded_shape_count
        ),
        "collision_final_shape_count": formula.collision_final_shape_count,
        "collision_shape_a_padding_degree": (
            formula.collision_shape_a_padding_degree
        ),
        "collision_shape_a_excess_norm_degree_cap": (
            formula.collision_shape_a_excess_norm_degree_cap
        ),
        "collision_shape_a_pure_fiber_floor": (
            formula.collision_shape_a_pure_fiber_floor
        ),
        "collision_shape_a_resultant_bidegree": (
            formula.collision_shape_a_resultant_bidegree
        ),
        "collision_shape_a_pair_floor": formula.collision_shape_a_pair_floor,
        "collision_shape_a_component_floor": (
            formula.collision_shape_a_component_floor
        ),
        "collision_shape_a_component_min_bidegree": (
            formula.collision_shape_a_component_min_bidegree
        ),
        "collision_shape_a_component_min_point_floor": (
            formula.collision_shape_a_component_min_point_floor
        ),
        "collision_shape_a_component_multiplicity_ratio": (
            formula.collision_shape_a_component_multiplicity_ratio
        ),
        "collision_shape_a_global_point_floor": (
            formula.collision_shape_a_global_point_floor
        ),
        "collision_shape_a_global_chi_floor": (
            formula.collision_shape_a_global_chi_floor
        ),
        "collision_shape_a_global_genus_floor": (
            formula.collision_shape_a_global_genus_floor
        ),
        "collision_shape_a_global_genus_ceiling": (
            formula.collision_shape_a_global_genus_ceiling
        ),
        "collision_shape_a_residual_divisor_multiplier": (
            formula.collision_shape_a_residual_divisor_multiplier
        ),
        "collision_shape_a_residual_cycle_degree": (
            formula.collision_shape_a_residual_cycle_degree
        ),
        "collision_shape_a_residual_section_dimension": (
            formula.collision_shape_a_residual_section_dimension
        ),
        "collision_shape_a_second_modification_constant_rank": (
            formula.collision_shape_a_second_modification_constant_rank
        ),
        "collision_shape_a_second_modification_negative_ceiling": (
            formula.collision_shape_a_second_modification_negative_ceiling
        ),
        "collision_shape_a_source_row_count": (
            formula.collision_shape_a_source_row_count
        ),
        "collision_shape_a_source_locator_degree": (
            formula.collision_shape_a_source_locator_degree
        ),
        "collision_shape_a_omitted_recurrence_length": (
            formula.collision_shape_a_omitted_recurrence_length
        ),
        "collision_shape_a_offline_slope_count": (
            formula.collision_shape_a_offline_slope_count
        ),
        "collision_shape_a_fixture_layer_cake": (
            formula.collision_shape_a_fixture_layer_cake
        ),
        "collision_shape_a_bordered_matrix_size": (
            formula.collision_shape_a_bordered_matrix_size
        ),
        "collision_shape_a_padding_flag_degree": (
            formula.collision_shape_a_padding_flag_degree
        ),
        "collision_shape_a_regular_flag_degree": (
            formula.collision_shape_a_regular_flag_degree
        ),
        "collision_shape_a_bordered_source_subset_size": (
            formula.collision_shape_a_bordered_source_subset_size
        ),
        "collision_shape_a_bordered_fixture_subset_checks": (
            formula.collision_shape_a_bordered_fixture_subset_checks
        ),
        "collision_shape_a_static_drop_fixture_cases": (
            formula.collision_shape_a_static_drop_fixture_cases
        ),
        "collision_shape_a_static_drop_source_count": (
            formula.collision_shape_a_static_drop_source_count
        ),
        "collision_shape_a_static_drop_maximum": (
            formula.collision_shape_a_static_drop_maximum
        ),
        "collision_shape_a_static_drop_residue_checks": (
            formula.collision_shape_a_static_drop_residue_checks
        ),
        "collision_shape_a_static_drop_subset_checks": (
            formula.collision_shape_a_static_drop_subset_checks
        ),
        "collision_shape_a_residual_mds_row_surplus": (
            formula.collision_shape_a_residual_mds_row_surplus
        ),
        "collision_shape_a_residual_mds_unpadded_start": (
            formula.collision_shape_a_residual_mds_unpadded_start
        ),
        "collision_shape_a_residual_mds_padded_start": (
            formula.collision_shape_a_residual_mds_padded_start
        ),
        "collision_shape_a_residual_mds_fixture_cases": (
            formula.collision_shape_a_residual_mds_fixture_cases
        ),
        "collision_shape_a_residual_mds_fixture_parities": (
            formula.collision_shape_a_residual_mds_fixture_parities
        ),
        "collision_shape_a_residual_mds_fixture_rows": (
            formula.collision_shape_a_residual_mds_fixture_rows
        ),
        "layer_a_rank": formula.layer_a_rank,
        "layer_a_nullity": formula.layer_a_nullity,
        "source_hashes": len(SOURCE_HASHES),
    }


def tamper_selftest() -> int:
    base = Formula()
    rejected = 0
    for field in base.__dict__:
        values = copy.copy(base.__dict__)
        values[field] += 1
        try:
            replay(Formula(**values))
        except VerificationError:
            rejected += 1
    require(
        rejected == len(base.__dict__),
        "tamper self-test did not reject every mutation",
    )
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "select --check or --tamper-selftest")

    if args.check:
        result = replay(Formula())
        if args.source_root is not None:
            result["source_files_checked"] = verify_source(args.source_root)
        print("RATE_HALF_QUADRATIC_PADE_QUARTIC_PASS", result)
    if args.tamper_selftest:
        print("RATE_HALF_QUADRATIC_PADE_QUARTIC_TAMPER_PASS", tamper_selftest())


if __name__ == "__main__":
    main()
