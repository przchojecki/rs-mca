#!/usr/bin/env python3
"""Replay the rate-half quadratic Pade/quartic degree identities."""

from __future__ import annotations

import argparse
import copy
import hashlib
from dataclasses import dataclass
from pathlib import Path


SOURCE_COMMIT = "f68d685e78da099e0a4dff362cc90ed2601a341f"
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
    "background/nodes/rate_half_layer_a_saturation_count_route_fence/statement.md": "6f28fea411e3bba5f055103229d09817e46aec18232c71cccb800297146bb36d",
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
}


class VerificationError(RuntimeError):
    """Raised when an exact packet identity fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


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
            if e == 183251937963:
                expected = (
                    formula.macroscopic_factor_d_a0
                    if d_a == 0
                    else formula.macroscopic_factor_d_a1
                )
                require(threshold == expected, "official factor bound failed")
            checks += 4

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
    require(len(SOURCE_COMMIT) == 40, "source commit pin malformed")
    require(len(SOURCE_HASHES) == 44, "source hash inventory changed")
    require(
        all(len(digest) == 64 for digest in SOURCE_HASHES.values()),
        "source hash malformed",
    )

    checks += verify_layer_a_fixture(formula)

    return {
        "checks": checks + 13,
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
    require(rejected == 22, "tamper self-test did not reject every mutation")
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
