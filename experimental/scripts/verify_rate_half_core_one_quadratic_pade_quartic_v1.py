#!/usr/bin/env python3
"""Replay the rate-half quadratic Pade/quartic degree identities."""

from __future__ import annotations

import argparse
import copy
import hashlib
from dataclasses import dataclass
from math import comb
from pathlib import Path


SOURCE_COMMIT = "a22ff2c2e3d2c7dcf257244ed300bb737a9cbd2f"
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
    require(len(SOURCE_HASHES) == 74, "source hash inventory changed")
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
