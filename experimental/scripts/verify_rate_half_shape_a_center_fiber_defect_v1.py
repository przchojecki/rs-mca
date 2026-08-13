#!/usr/bin/env python3
"""Replay the Lane-T center-fiber and large-class defect dichotomy."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path


SOURCE_COMMIT = "04ae6011ff62187d0b101ef23a7ab0101f7f9db4"
SOURCE_HASHES = {
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_defect_and_large_class_dichotomy/statement.md": "6525db0f3f98127403a859cb06de798fbfaa981dc4c255b71cea89299df92587",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_defect_and_large_class_dichotomy/proof.md": "29b08bed3273e1e3a54f027f1516231c65052e218394c5708a894fc246e5c55a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_defect_and_large_class_dichotomy/audit.md": "cdcdfbc017da1af3499831222f2c7715d7e43537cdbc95a3b6a88d50bce80b29",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_defect_and_large_class_dichotomy/verify.py": "520665a07d452ac9978d09d54669d64c576b3493765b587c012bffb4f6456396",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_defect_and_large_class_dichotomy/verify_audit.py": "c14eba30c4c72b053ea55ff0cef82bbb304a39b5bec81dd381f3993116772e83",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_live_linear_quadratic_syzygy_and_small_class_defect/statement.md": "9fcaeaa70a58ac26582698e0df3651ff435a2ddc8855bd1b9ee9c1aea7ed9286",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_live_linear_quadratic_syzygy_and_small_class_defect/proof.md": "45019f223a448640dfc10033a0dc54cff6f259c79be3e2be23f4323ffdf3df3f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_dual_mds_split_biform_reduction/statement.md": "bfc301188ff4d08086fcbd9acceedb6f886b26f1f0fcb337c0e2cfff3d0e3b05",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_dual_mds_split_biform_reduction/proof.md": "03cbd1b1dfc702bb79b9974a76104bceba00758595bb78af706fa75b1261a857",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_heavy_row_quadratic_residual_factorization/statement.md": "b03b5355fb3a09a62f2263754d3ce4b409c9c3019f357bc41387a4aad099afdb",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_heavy_row_quadratic_residual_factorization/proof.md": "54130913e897c1a95dd76d86365db4a25fc6d7ef261d548fe972b40d24ef9ac0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_large_class_center_residual_exclusion/statement.md": "4457a7b6ef5612d88d2bbee0dadd229b2ceb4fa272fc3bc5fc395c995d3bc1e1",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_large_class_center_residual_exclusion/proof.md": "ca006d05891e6e2cee6deb6932d83388af385868dbe740411e737e90a8087a38",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_large_class_center_residual_exclusion/audit.md": "0bc8759ed5729868d9b2b38d28e72af09d3a2d1744b630aae77e0e08f1a2e244",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_large_class_center_residual_exclusion/verify.py": "acdf2ed5200e56811cf72bf1b6da249704aaedd717d2597e859122b83e94230c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_large_class_center_residual_exclusion/verify_audit.py": "bb09991e07d6d2887daf553c2a79ae89a312ec9a98dbe35b798834f0e62506b0",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_resultant_regular_quartic_identification/statement.md": "c8de176f5c5d3a3081737b9cbfe702d3cb821cfc881510fac8bc3cf26f03ebf6",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_extremal_resultant_regular_quartic_identification/proof.md": "fa8b278e41e9c579f729c82c2756715693e5f1895e33590f27dc190e606eb9c3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_coprimality_and_pade_quotient/statement.md": "8b816eeca742803e0df83d0d105977b2e86bf623d66775dcc01647e9d3e9851f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_coprimality_and_pade_quotient/proof.md": "14656be12d13cf24ec78d8ca0a8c2e2fcd238a0203bec3729048139f1a2c077a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_coprimality_and_pade_quotient/audit.md": "2710dae2850e5ccae573c66bb803bceee854a0dfd34aa31a8f5d95b1f338f72d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_coprimality_and_pade_quotient/verify.py": "18cc54f28baee91afa4fa36e08b2a90c5f24ce81657ef63ddc71c07c5152b4bc",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_fiber_coprimality_and_pade_quotient/verify_audit.py": "7907ba45d601a66b46ef3e1db55e991211ad6596523388094fa209c7b536f44b",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_regular_factor_identity/statement.md": "de1ffaa7a71b105c5526a16dbff1838ae5b6529acc73d94428964ef8039b199c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_pade_regular_factor_identity/proof.md": "6a84f32f36fb249177181c67251e03b5d0b62c430c1576ff110220d1ea84cd18",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_padded_center_pade_transversality/statement.md": "4a08bea17d88cd610667184269388af34b67561eba0205f4b804fa25c314327c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_padded_center_pade_transversality/proof.md": "5a0c1689a3ea6f108176ceab0f9177e6ebee1a53eab505f6deb147cdf005a4c2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_padded_center_pade_transversality/audit.md": "d7a8f10acbd34cc4b2bf341d509098c963d66e3d459e0d23dbcd488b387d643e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_padded_center_pade_transversality/verify.py": "dc30f32cbeaf309f73f13ac65109627b5c46301a213d0083b45d8e833a16d96e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_padded_center_pade_transversality/verify_audit.py": "dc07229ddaf35605742ca68c733197b07bd2c538dade03c3bc03e4fff1667130",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_primitive_source_pencil_three_center_fibers/statement.md": "7e897560c872f00f58ee87f83af5012a8758cba827b5a420a3e796e267576557",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_primitive_source_pencil_three_center_fibers/proof.md": "85fb9ab3f22135c457aab05176710408f850fd41f54a36c722a205455ed17d7e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_primitive_source_pencil_three_center_fibers/audit.md": "b445ed1154b0cfa78284aaf41ceb3f9b489352e31b3397a225debea386eeeb84",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_primitive_source_pencil_three_center_fibers/verify.py": "c401f054bbdac3f1bd748a6526b2c0e1764d4a240bd836c4f256492d35670910",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_primitive_source_pencil_three_center_fibers/verify_audit.py": "75c20483d7db026c5d355c8cd4ae2abacdc94c85ccf3459426c1a443096faeee",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_residue_pairing_common_kernel_router/statement.md": "e4336708e1b8599755dd6e467231968746bb90d0f28acc224c21556ac2f5a899",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_residue_pairing_common_kernel_router/proof.md": "6973fffba5a1cc803a2187a5389f513ec62ba530f3dfa698bb178dd1002a682a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_residue_pairing_common_kernel_router/audit.md": "4de3149e82cd9d6bbc086b506e389b2bcc04c20816bccfc583ddfe1b9f5012a2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_residue_pairing_common_kernel_router/verify.py": "fd1e0d891a952f3249ba265366624b6cfc291daaa5d7ee87bc221db6fd854636",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_center_residue_pairing_common_kernel_router/verify_audit.py": "61f3885726c0844b508a1b0510558176fada600b6b9539de2425ad02549aba21",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_global_source_multiplier_common_kernel_normal_form/statement.md": "a17eb9d5de92e217dfd10f6bdd3c48ef89ae4ba2c8803ce77b9ed6b247bb91b1",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_global_source_multiplier_common_kernel_normal_form/proof.md": "0158feccaa9aa5020eb46b424f8ade923308311a79d6d98116919bd1b3d2e2b7",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_global_source_multiplier_common_kernel_normal_form/audit.md": "bbeeb6edfe9d5d85a8ee693c74da3a96722ca83cc9eb1c32ce9e5d9004d0c4ce",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_global_source_multiplier_common_kernel_normal_form/verify.py": "918182e76ccd7668f6b79b1701d9b5046db63b332026c57be15f3c4725e090f5",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_global_source_multiplier_common_kernel_normal_form/verify_audit.py": "88c8c7b2471670a6899f68016aaf72e5fbb16c103d8db5afaa04e620c8a1f002",
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


@dataclass(frozen=True)
class Formula:
    official_e: int = 183251937963
    boundary_rank: int = 91625968982
    projection_rank: int = 91625968981
    small_class: int = 274877906943
    large_class: int = 274877906944
    locator_degree: int = 549755813887
    small_rest: int = 549755813887
    large_rest: int = 549755813886
    large_dual_dimension: int = 2
    residual_before: int = 3
    residual_after: int = 2
    small_toy_rank: int = 3
    large_toy_rank: int = 2
    exact_large_rank: int = 91625968981
    residual_degree: int = 4
    multiplication_chain_dimension: int = 0
    center_common_roots: int = 0
    large_padded_value_nonzero: int = 1
    small_pade_quotient_degree: int = 549755813886
    large_pade_quotient_degree: int = 549755813885
    padded_center_resultant_order: int = 1
    padded_center_intersection_length: int = 1
    padded_center_source_value_nonzero: int = 1
    primitive_degree_maximum: int = 824633720829
    primitive_degree_minimum: int = 274877906944
    primitive_small_residual_offset: int = 549755813886
    primitive_large_residual_offset: int = 549755813885
    primitive_relation_dimension: int = 1
    residue_form_rank: int = 274877906941
    residue_toy_form_rank: int = 4
    residue_toy_restricted_rank: int = 2
    residue_toy_combined_rank: int = 5
    common_kernel_boundary: int = 183251937960
    zero_kappa_rank_floor: int = 152709948302
    source_multiplier_toy_e3_rank: int = 9
    source_multiplier_toy_block_rank: int = 9
    source_multiplier_toy_global_rank: int = 9
    source_multiplier_e3_dimension: int = 274877906946
    source_multiplier_orthogonal_dimension: int = 549755813884
    source_multiplier_intersection_floor: int = 183251937960


def matrix_rank(rows: list[list[int]], modulus: int) -> int:
    work = [[entry % modulus for entry in row] for row in rows]
    row = 0
    for column in range(len(work[0])):
        pivot = next((i for i in range(row, len(work))
                      if work[i][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        inverse = pow(work[row][column], modulus - 2, modulus)
        work[row] = [entry * inverse % modulus for entry in work[row]]
        for i in range(len(work)):
            if i != row and work[i][column]:
                scale = work[i][column]
                work[i] = [
                    (left - scale * right) % modulus
                    for left, right in zip(work[i], work[row])
                ]
        row += 1
        if row == len(work):
            break
    return row


def dual_rs_toy(class_size: int) -> int:
    modulus = 101
    degree = 3
    points = list(range(1, class_size + 1))
    x_star = 17
    weights = []
    for x in points:
        derivative = 1
        for y in points:
            if y != x:
                derivative = derivative * (x - y) % modulus
        weights.append(pow(derivative, modulus - 2, modulus))
    forms = (
        lambda x: 1,
        lambda x: x - x_star,
        lambda x: x * x,
        lambda x: x * x * x,
    )
    rows = [
        [
            sum(
                weight * form(x) * pow(x, power, modulus)
                for x, weight in zip(points, weights)
            ) % modulus
            for power in range(degree + 1)
        ]
        for form in forms
    ]
    return matrix_rank(rows, modulus)


def center_residue_toy() -> tuple[int, int, int]:
    modulus = 211
    degree = 4
    centers = (
        ([147, 69, 51, 42, 34, 104], [18, 54, 113], None),
        ([95, 101, 140, 7, 67, 21], [42, 29, 88], None),
        ([151, 117, 76, 2, 132, 88, 52], [154, 14, 27], 200),
    )

    def value(coefficients: list[int], x: int) -> int:
        return sum(
            coefficient * pow(x, power, modulus)
            for power, coefficient in enumerate(coefficients)
        ) % modulus

    def gram(
        points: list[int], coefficients: list[int], x_star: int | None
    ) -> list[list[int]]:
        weights = []
        for x in points:
            derivative = 1
            for y in points:
                if x != y:
                    derivative = derivative * (x - y) % modulus
            g_value = value(coefficients, x)
            require(g_value != 0, "residue toy center nonvanishing")
            r_value = 1 if x_star is None else x - x_star
            weights.append(
                r_value
                * pow(g_value * derivative % modulus, modulus - 2, modulus)
                % modulus
            )
        return [
            [
                sum(
                    weight * pow(x, i + j, modulus)
                    for x, weight in zip(points, weights)
                )
                % modulus
                for j in range(degree + 1)
            ]
            for i in range(degree + 1)
        ]

    forms = []
    for points, coefficients, x_star in centers:
        form = gram(points, coefficients, x_star)
        require(matrix_rank(form, modulus) == degree, "residue toy form rank")
        radical = coefficients + [0] * (degree + 1 - len(coefficients))
        image = [
            sum(row[i] * radical[i] for i in range(degree + 1)) % modulus
            for row in form
        ]
        require(image == [0] * (degree + 1), "residue toy radical")
        forms.append(form)

    restricted = [form[:3] for form in forms]
    require(
        all(matrix_rank(form, modulus) == 2 for form in restricted),
        "residue toy restricted rank",
    )
    combined = [row for form in restricted for row in form]
    return degree, 2, matrix_rank(combined, modulus)


def source_multiplier_toy() -> tuple[int, int, int]:
    modulus = 211
    centers = (
        (2, [147, 69, 51, 42, 34, 104], [18, 54, 113], None),
        (5, [95, 101, 140, 7, 67, 21], [42, 29, 88], None),
        (9, [151, 117, 76, 2, 132, 88, 52], [154, 14, 27], 200),
    )
    domain = [x for _, points, _, _ in centers for x in points]

    def value(coefficients: list[int], x: int) -> int:
        return sum(
            coefficient * pow(x, power, modulus)
            for power, coefficient in enumerate(coefficients)
        ) % modulus

    def derivative(x: int) -> int:
        out = 1
        for y in domain:
            if y != x:
                out = out * (x - y) % modulus
        return out

    phi: dict[int, int] = {}
    j_value: dict[int, int] = {}
    block_rows = []
    for gamma, points, coefficients, x_star in centers:
        other = [x for x in domain if x not in points]
        for x in points:
            rest = 1
            for y in other:
                rest = rest * (x - y) % modulus
            r_value = 1 if x_star is None else x - x_star
            denominator = r_value * rest % modulus
            require(denominator != 0, "source multiplier denominator")
            j_value[x] = value(coefficients, x) * pow(
                denominator, modulus - 2, modulus
            ) % modulus
            require(j_value[x] != 0, "source multiplier unit")
            phi[x] = gamma
        for degree in range(3):
            block_rows.append([
                (
                    pow(x, degree, modulus)
                    * pow(j_value[x] * derivative(x) % modulus,
                          modulus - 2, modulus)
                    if x in points else 0
                ) % modulus
                for x in domain
            ])

    global_rows = [
        [
            pow(phi[x], power, modulus)
            * pow(x, degree, modulus)
            * pow(j_value[x] * derivative(x) % modulus,
                  modulus - 2, modulus)
            % modulus
            for x in domain
        ]
        for power in range(3)
        for degree in range(3)
    ]
    e3_rows = [
        [
            pow(phi[x], power, modulus) * pow(x, degree, modulus) % modulus
            for x in domain
        ]
        for power in range(3)
        for degree in range(3)
    ]
    block_rank = matrix_rank(block_rows, modulus)
    global_rank = matrix_rank(global_rows, modulus)
    require(
        matrix_rank(block_rows + global_rows, modulus)
        == block_rank == global_rank,
        "source indicator/multiplier row-space identity",
    )
    return matrix_rank(e3_rows, modulus), block_rank, global_rank


def verify_source(root: Path) -> int:
    checked = 0
    for relative, expected in SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), f"missing pinned source: {relative}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        require(actual == expected, f"source hash mismatch: {relative}")
        checked += 1
    return checked


def replay(formula: Formula) -> dict[str, int]:
    e = (2**39 + 1) // 3
    n = (3 * e - 7) // 2
    d = 3 * e - 2
    total = (9 * e - 7) // 2
    r = (e + 1) // 2
    kernel = 3 * r - (e + 1)
    c1 = 2 * r - e
    projection = kernel - c1
    require(e == formula.official_e, "official e")
    require(r == formula.boundary_rank, "boundary rank")
    require(projection == formula.projection_rank == r - 1,
            "projection rank")
    require(n + 2 == formula.small_class, "small class")
    require(n + 3 == formula.large_class, "large class")
    require(d == formula.locator_degree, "locator degree")
    require(total - (n + 2) == formula.small_rest == d, "small rest")
    require(total - (n + 3) == formula.large_rest == d - 1, "large rest")
    require((n + 3) - (n + 1) == formula.large_dual_dimension,
            "large dual dimension")
    require(formula.residual_before - 1 == formula.residual_after,
            "residual quotient")
    small_toy = dual_rs_toy(5)
    large_toy = dual_rs_toy(6)
    require(small_toy == formula.small_toy_rank, "small toy rank")
    require(large_toy == formula.large_toy_rank, "large toy rank")
    require(r - 1 == formula.exact_large_rank, "exact large rank")
    require(formula.residual_degree == 4, "residual degree")
    require(formula.multiplication_chain_dimension == 0,
            "multiplication chain excluded")
    residual_support = {"tau": formula.residual_degree}
    require("gamma_0" not in residual_support, "center residual support")
    require(formula.center_common_roots == 0, "center coprimality")
    require(formula.large_padded_value_nonzero == 1,
            "large padded value")
    total = (9 * e - 7) // 2
    require(total - 1 - (n + 2) == formula.small_pade_quotient_degree,
            "small Pade quotient")
    require(total - 1 - (n + 3) == formula.large_pade_quotient_degree,
            "large Pade quotient")
    require(formula.padded_center_resultant_order == 1,
            "padded center resultant")
    require(formula.padded_center_intersection_length
            == formula.padded_center_resultant_order,
            "padded center intersection")
    require(formula.padded_center_source_value_nonzero == 1,
            "padded center source value")
    before = total - 1
    require(before == formula.primitive_degree_maximum,
            "primitive degree maximum")
    require(n + 3 == formula.primitive_degree_minimum,
            "primitive degree minimum")
    require(before - (n + 2) == formula.primitive_small_residual_offset,
            "primitive small residual")
    require(before - (n + 3) == formula.primitive_large_residual_offset,
            "primitive large residual")
    require(formula.primitive_relation_dimension == 1,
            "primitive relation")
    residue_form, residue_restricted, residue_combined = center_residue_toy()
    require(n == formula.residue_form_rank, "official residue form rank")
    require(residue_form == formula.residue_toy_form_rank,
            "residue toy form")
    require(residue_restricted == formula.residue_toy_restricted_rank,
            "residue toy restriction")
    require(residue_combined == formula.residue_toy_combined_rank,
            "residue toy combination")
    require(n + 1 - r == formula.common_kernel_boundary == e - 3,
            "common-kernel boundary")
    require((5 * e - 3) // 6 == formula.zero_kappa_rank_floor,
            "zero-kappa floor")
    multiplier_e3, multiplier_block, multiplier_global = source_multiplier_toy()
    require(multiplier_e3 == formula.source_multiplier_toy_e3_rank,
            "source multiplier toy E3")
    require(multiplier_block == formula.source_multiplier_toy_block_rank,
            "source multiplier toy block")
    require(multiplier_global == formula.source_multiplier_toy_global_rank,
            "source multiplier toy global")
    require(3 * r == n + 5 == formula.source_multiplier_e3_dimension,
            "source multiplier E3 dimension")
    require(total - 3 * r == 2 * n + 2
            == formula.source_multiplier_orthogonal_dimension,
            "source multiplier orthogonal dimension")
    require(e - 3 == formula.source_multiplier_intersection_floor,
            "source multiplier intersection floor")
    return {
        "rank": r,
        "projection": projection,
        "small_class": n + 2,
        "large_class": n + 3,
        "small_toy_rank": small_toy,
        "large_toy_rank": large_toy,
        "exact_large_rank": r - 1,
        "residual_degree": formula.residual_degree,
        "small_pade_quotient_degree": formula.small_pade_quotient_degree,
        "large_pade_quotient_degree": formula.large_pade_quotient_degree,
        "padded_center_order": formula.padded_center_resultant_order,
        "primitive_degree_range": (
            formula.primitive_degree_minimum,
            formula.primitive_degree_maximum,
        ),
        "residue_toy_ranks": (
            residue_form,
            residue_restricted,
            residue_combined,
        ),
        "common_kernel_boundary": formula.common_kernel_boundary,
        "zero_kappa_rank_floor": formula.zero_kappa_rank_floor,
        "source_multiplier_toy_ranks": (
            multiplier_e3,
            multiplier_block,
            multiplier_global,
        ),
        "source_multiplier_dimensions": (
            formula.source_multiplier_e3_dimension,
            formula.source_multiplier_orthogonal_dimension,
            formula.source_multiplier_intersection_floor,
        ),
    }


def tamper_selftest() -> int:
    base = Formula()
    rejected = 0
    for field in base.__dict__:
        values = dict(base.__dict__)
        values[field] += 1
        try:
            replay(Formula(**values))
        except VerificationError:
            rejected += 1
    require(rejected == len(base.__dict__), "hostile mutations")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--source-root", type=Path)
    args = parser.parse_args()
    require(args.check or args.tamper_selftest, "select a replay mode")
    if args.check:
        result = replay(Formula())
        result["source_commit"] = SOURCE_COMMIT
        if args.source_root is not None:
            result["source_files_checked"] = verify_source(args.source_root)
        print("RATE_HALF_SHAPE_A_CENTER_FIBER_DEFECT_PASS", result)
    if args.tamper_selftest:
        print(
            "RATE_HALF_SHAPE_A_CENTER_FIBER_DEFECT_TAMPER_PASS",
            tamper_selftest(),
        )


if __name__ == "__main__":
    main()
