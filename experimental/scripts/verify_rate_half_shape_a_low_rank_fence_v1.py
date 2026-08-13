#!/usr/bin/env python3
"""Replay the Shape-A rank fence and rank-three geometry routers."""

from __future__ import annotations

import argparse
import hashlib
import math
import random
from dataclasses import dataclass
from pathlib import Path


SOURCE_COMMIT = "d4bb2f4728b7653c52531091a228b19daf65b7da"
SOURCE_HASHES = {
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_parameter_mds_gate/probe_results.md": "603668188e6fa399919f0ce0955b4a7ccef06a549286a43e3e43b6f8ba922203",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_parameter_mds_gate/verify_probe.py": "f783f91f9b22084d457c2f96205cb838e9b5b9f6562547f6b746825150229da9",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_degree_ledger_rank_route_fence/statement.md": "d673f4b6354a6d65c045cf62110db14481811c40a191c9d1793b09071299a2aa",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_degree_ledger_rank_route_fence/proof.md": "1a13cb380c18d75634e4e5864dc498769d75a4115c339ff009eae64f15198062",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_degree_ledger_rank_route_fence/audit.md": "d229975b997921e01cde26d4b804e83122b0a56dcdc8e3b3377efc120d1196ae",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_degree_ledger_rank_route_fence/verify.py": "62ddae09bb5f2c47f6b52bfda426c200916ab3ac30db5cf34de627c1ce1e6be3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_degree_ledger_rank_route_fence/verify_audit.py": "0a250327cacf77ea5a66e966b5301de932f2e521bfff04f642869fd18549affc",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_two_biform_exclusion/statement.md": "db8ce7462dfa0163452564675dca4d94989cbd0ce6defae39c02c7c02d229b93",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_two_biform_exclusion/proof.md": "e1daacdad3eca9dc749ec0ef814d4d30e9a0d71925e996f1822221af1662391a",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_two_biform_exclusion/audit.md": "a05990b75ff20c33599b0a3c41404ba4c8fe65388dae7cb1f45023cec893570f",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_two_biform_exclusion/verify.py": "15a9638bfc8d5dfb48169b954e2be2ccaee695e8c9f077c655f1fbaa70d9a1fc",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_two_biform_exclusion/verify_audit.py": "25d91265ec5cb0aac486883cbbe8cd1c683b7c0e7bc85d7888564dce90b800b7",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_projective_frame_router/statement.md": "ff65f8ae7097f8fa2caadb2764880ad3e2a098fc0b145c275dbc8ace0a9fcbbe",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_projective_frame_router/proof.md": "131c76e92f4ecdec4eb52a8b2fdb2aabeb183f9cc5fc3358198e9ce094e7c5da",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_projective_frame_router/audit.md": "859cf7359a527782d72de8eae05efb96d28513b309701d929d53d917c7501e4c",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_projective_frame_router/verify.py": "2ca82d2787f27cd069a8814c5cf39b2f177b6b0b168d1c3b5730f504676f1250",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_projective_frame_router/verify_audit.py": "ac6b57be2bcfa49f271098e0687d82bba4edc3c3bc131880fc1268c7ac939e5e",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_parameter_curve_birational_singularity_router/statement.md": "2950712884f820402f759bc051abfa4a3f6ec2fd2757d0126e4d1f361c3ef87d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_parameter_curve_birational_singularity_router/proof.md": "229a02b14cc6883536af9b73190b9d253314668127d942e2a64ce7707b99a199",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_parameter_curve_birational_singularity_router/audit.md": "8645a83f4f8693dac5c9ed1f7db9c6f33161da87cb85979b38d1c497cc00553d",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_parameter_curve_birational_singularity_router/verify.py": "83b250276c327f62708c77bb3668c92177c01ecf58dc9e3a7d3baf97fc026ce3",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_tensor_rank_three_parameter_curve_birational_singularity_router/verify_audit.py": "df268b77a83763422ffb20aea5d134c05c7e811fa9466ba390ca572ebb18d0f2",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_parameter_map_birationality/statement.md": "1f73cee669c095a25f8c69e27b6f561bf55e4c094772d17df02f3b7a335c6329",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_parameter_map_birationality/proof.md": "d663ed93d01542168015fd72cf7c96335ea8ecb38b6e1e9c38fc3e3e288ca443",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_parameter_map_birationality/audit.md": "565e1b1273dd68c9677ccf3d1d96a0ca420a04fb75aaac1d5cb28e59f4975448",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_parameter_map_birationality/verify.py": "5baf7c7cba71326a0cad05236ee2b22a2ca0f54f44732351eabdacfa698e0413",
    "background/nodes/rate_half_ca_hankel_a1_first_degree_core_one_quadratic_gap_four_double_root_nonreduced_unshared_collision_shape_a_all_excess_parameter_map_birationality/verify_audit.py": "2af906340debdc5e37007256718197ef882eb783a3c5abbbd0ae37e55f2f6216",
}


class VerificationError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def prime_factors(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(modulus: int) -> int:
    factors = prime_factors(modulus - 1)
    for candidate in range(2, modulus):
        if all(
            pow(candidate, (modulus - 1) // factor, modulus) != 1
            for factor in factors
        ):
            return candidate
    raise VerificationError("primitive root")


def multiply(left: list[int], right: list[int], modulus: int) -> list[int]:
    product = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            product[i + j] = (product[i + j] + a * b) % modulus
    return product


def root_polynomial(roots: list[int], modulus: int) -> list[int]:
    polynomial = [1]
    for root in roots:
        polynomial = multiply(polynomial, [-root % modulus, 1], modulus)
    return polynomial


def matrix_rank(rows: list[list[int]], columns: int, modulus: int) -> int:
    pivots: dict[int, list[int]] = {}
    for source in rows:
        row = source[:]
        for column, pivot in pivots.items():
            if row[column]:
                scale = row[column]
                row = [
                    (left - scale * right) % modulus
                    for left, right in zip(row, pivot)
                ]
        for column, value in enumerate(row):
            if value:
                inverse = pow(value, modulus - 2, modulus)
                pivots[column] = [entry * inverse % modulus for entry in row]
                break
        if len(pivots) == columns:
            return columns
    return len(pivots)


def all_excess_matrix(
    incidence: list[set[int]],
    domain: list[int],
    slopes: list[int],
    modulus: int,
) -> tuple[list[list[int]], list[tuple[int, int]]]:
    excesses = [
        7 - sum(column in row for row in incidence)
        for column in range(len(slopes))
    ]
    require(sum(excesses) == 7, "total excess")
    weights = []
    for index, slope in enumerate(slopes):
        derivative = 1
        for other_index, other in enumerate(slopes):
            if index != other_index:
                derivative = derivative * (slope - other) % modulus
        weights.append(pow(derivative, modulus - 2, modulus))

    known = []
    columns = []
    for delta_index, excess in enumerate(excesses):
        roots = [
            domain[row]
            for row in range(len(domain))
            if delta_index in incidence[row]
        ]
        known.append(root_polynomial(roots, modulus))
        for residual_degree in range(excess + 1):
            columns.append((delta_index, residual_degree))
    require(len(columns) == 28, "4e columns")

    rows = []
    for coefficient in range(8):
        for power in range(15):
            row = []
            for delta_index, residual_degree in columns:
                known_degree = coefficient - residual_degree
                coefficient_value = (
                    known[delta_index][known_degree]
                    if 0 <= known_degree < len(known[delta_index])
                    else 0
                )
                row.append(
                    coefficient_value
                    * pow(slopes[delta_index], power, modulus)
                    * weights[delta_index]
                    % modulus
                )
            rows.append(row)
    return rows, columns


def partitions(total: int, ceiling: int | None = None):
    if total == 0:
        yield ()
        return
    if ceiling is None or ceiling > total:
        ceiling = total
    for first in range(ceiling, 0, -1):
        for tail in partitions(total - first, first):
            yield (first, *tail)


def incidence_with_column_degrees(
    column_degrees: list[int], offset: int
) -> list[set[int]]:
    incidence = [set() for _ in range(28)]
    remaining = [5] * 28
    order = sorted(
        range(21), key=lambda column: (-column_degrees[column], column)
    )
    for column in order:
        choices = sorted(
            range(28),
            key=lambda row: (-remaining[row], (row - offset * column) % 28),
        )
        chosen = [row for row in choices if remaining[row] > 0][
            : column_degrees[column]
        ]
        require(len(chosen) == column_degrees[column], "degree realization")
        for row in chosen:
            incidence[row].add(column)
            remaining[row] -= 1
    require(not any(remaining), "row degrees")
    return incidence


def switched_copy(base: list[set[int]], rng: random.Random) -> list[set[int]]:
    incidence = [row.copy() for row in base]
    for _ in range(120):
        first, second = rng.sample(range(28), 2)
        left = rng.choice(tuple(incidence[first]))
        right = rng.choice(tuple(incidence[second]))
        if left != right and right not in incidence[first] and left not in incidence[second]:
            incidence[first].remove(left)
            incidence[first].add(right)
            incidence[second].remove(right)
            incidence[second].add(left)
    return incidence


@dataclass(frozen=True)
class Formula:
    partition_count: int = 15
    partition_cases: int = 630
    fence_rank: int = 27
    rank_two_onset: int = 9
    official_row_surplus: int = 7
    rank_three_repeated_floor: int = 183251937955
    rank_three_pair_floor: int = 30541989660
    maximum_empty_columns: int = 1
    normalization_degree: int = 1
    local_delta_floor: int = 466406566180502462970
    six_vertex_delta_floor: int = 2798439396930304829525


def partition_probe() -> tuple[int, int, int]:
    profiles = list(partitions(7))
    cases = 0
    minimum_rank = 28
    for modulus in (337, 421):
        generator = primitive_root(modulus)
        domain = [
            pow(generator, (modulus - 1) // 28 * exponent, modulus)
            for exponent in range(28)
        ]
        slopes = [
            pow(generator, (modulus - 1) // 21 * exponent, modulus)
            for exponent in range(21)
        ]
        for profile_index, profile in enumerate(profiles):
            deficits = list(profile) + [0] * (21 - len(profile))
            base = incidence_with_column_degrees(
                [7 - deficit for deficit in deficits], profile_index + 1
            )
            rng = random.Random(20260813 + 1000 * profile_index + modulus)
            candidates = [base] + [switched_copy(base, rng) for _ in range(20)]
            for candidate in candidates:
                rows, columns = all_excess_matrix(
                    candidate, domain, slopes, modulus
                )
                rank = matrix_rank(rows, len(columns), modulus)
                minimum_rank = min(minimum_rank, rank)
                cases += 1
    return len(profiles), cases, minimum_rank


def degree_ledger_fence() -> tuple[int, int]:
    modulus = 211
    values = {pow(2, 35 * index, modulus) for index in range(4)}
    domain = [x for x in range(1, modulus) if pow(x, 7, modulus) in values]
    slopes = [0] + [
        delta
        for delta in range(1, modulus)
        if pow(delta, 5, modulus) in values
    ]
    incidence = [
        {
            index
            for index, delta in enumerate(slopes)
            if pow(delta, 5, modulus) == pow(x, 7, modulus)
        }
        for x in domain
    ]
    require(len(domain) == 28 and len(slopes) == 21, "fence grid")
    require({len(row) for row in incidence} == {5}, "fence row degree")
    require(
        [sum(column in row for row in incidence) for column in range(21)]
        == [0] + [7] * 20,
        "fence column degrees",
    )
    rows, columns = all_excess_matrix(incidence, domain, slopes, modulus)
    kernel = [-1 % modulus if index == 7 or index >= 8 else 0 for index in range(28)]
    require(
        all(
            sum(left * right for left, right in zip(row, kernel)) % modulus == 0
            for row in rows
        ),
        "block-supported kernel",
    )
    return matrix_rank(rows, len(columns), modulus), 21


def verify_source(root: Path) -> int:
    checked = 0
    for relative, expected in SOURCE_HASHES.items():
        path = root / relative
        require(path.is_file(), f"missing pinned source: {relative}")
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == expected,
            f"source hash mismatch: {relative}",
        )
        checked += 1
    return checked


def replay(formula: Formula) -> dict[str, int]:
    profile_count, cases, minimum_rank = partition_probe()
    require(profile_count == formula.partition_count, "partition count")
    require(cases == formula.partition_cases, "partition cases")
    require(minimum_rank == 28, "partition minimum rank")

    fence_rank, blocks = degree_ledger_fence()
    require(fence_rank == formula.fence_rank, "fence rank")
    require(blocks == 21, "fence block support")

    onset = next(e for e in range(7, 20, 2) if 4 * (e - 2) > 3 * e)
    require(onset == formula.rank_two_onset, "rank-two onset")
    e = 183251937963
    m = e - 2
    n = (3 * e - 7) // 2
    row_count = (9 * e - 7) // 2
    require(row_count - 3 * n == formula.official_row_surplus, "row surplus")
    require((3 * e) // (e - 2) == 3, "official row-type cap")
    repeated_floor = 4 * (e - 2) - 3 * e
    pair_floor = (repeated_floor + 5) // 6
    require(
        repeated_floor == formula.rank_three_repeated_floor,
        "rank-three repeated-slope floor",
    )
    require(pair_floor == formula.rank_three_pair_floor, "rank-three pair floor")
    n = (3 * e - 7) // 2
    total_deficit = 2 * e - 7
    maximum_empty = total_deficit // n
    require(maximum_empty == formula.maximum_empty_columns, "empty columns")
    require(2 * n > total_deficit, "two empty columns")
    normalization_degree = max(
        math.gcd(m, 3 * e),
        math.gcd(m, 3 * e - 1),
    )
    require(
        normalization_degree == formula.normalization_degree,
        "normalization degree",
    )
    local_delta = pair_floor * (pair_floor - 1) // 2
    require(local_delta == formula.local_delta_floor, "local delta floor")
    low, extra = divmod(repeated_floor, 6)
    six_delta = (
        extra * (low + 1) * low // 2
        + (6 - extra) * low * (low - 1) // 2
    )
    require(six_delta == formula.six_vertex_delta_floor, "six delta floor")
    return {
        "profiles": profile_count,
        "cases": cases,
        "minimum_rank": minimum_rank,
        "fence_rank": fence_rank,
        "blocks": blocks,
        "onset": onset,
        "official_surplus": row_count - 3 * n,
        "rank_three_repeated_floor": repeated_floor,
        "rank_three_pair_floor": pair_floor,
        "maximum_empty_columns": maximum_empty,
        "normalization_degree": normalization_degree,
        "local_delta_floor": local_delta,
        "six_vertex_delta_floor": six_delta,
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
        if args.source_root is not None:
            result["source_files_checked"] = verify_source(args.source_root)
        print("RATE_HALF_SHAPE_A_LOW_RANK_FENCE_PASS", result)
    if args.tamper_selftest:
        print("RATE_HALF_SHAPE_A_LOW_RANK_FENCE_TAMPER_PASS", tamper_selftest())


if __name__ == "__main__":
    main()
