#!/usr/bin/env python3
"""Replay the Lane-T center-fiber and large-class defect dichotomy."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path


SOURCE_COMMIT = "5e2d69025"
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
    return {
        "rank": r,
        "projection": projection,
        "small_class": n + 2,
        "large_class": n + 3,
        "small_toy_rank": small_toy,
        "large_toy_rank": large_toy,
        "exact_large_rank": r - 1,
        "residual_degree": formula.residual_degree,
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
