#!/usr/bin/env python3
"""Verify the M31 rank-seven proper-G zero-excess incidence route cut."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import sys
from collections import defaultdict, deque
from itertools import combinations
from math import ceil, comb
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from typing import Any


SCHEMA_ID = (
    "rs-mca-m31-rank7-proper-g-zero-excess-incidence-route-cut-v1"
)
THEOREM_ID = "M31_RANK7_PROPER_G_ZERO_EXCESS_INCIDENCE_ROUTE_CUT_V1"
STATUS = (
    "PROVED_LOCAL_DANGEROUS_CLASS_REDUCTION_"
    "PROPER_G_ZERO_EXCESS_ROUTE_CUT_Q147595_OPEN"
)

P_FIELD = 2**31 - 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_023
RADIUS = N - AGREEMENT
W = AGREEMENT - K
G = 354_972
D = G - W
SIGMA = 282_544
RESIDUAL_K = D - SIGMA
Q_CUTOFF = 147_595

CURRENT_CLASS_CAP = 9_806_438
CLOSING_CLASS_CAP = 9_806_393
VIOLATING_CLASS_MINIMUM = CLOSING_CLASS_CAP + 1
POSITIVE_Z_CAP = 444_522
RANK_FIVE_CAP = 908_021
RANK_FIVE_EXCESS_ONE_CAP = 907_953
POSITIVE_EXCESS_CAP = 6_466_046
FULL_P_ZERO_CAP = 1_182_419
PROPER_ZERO_TARGET = 2_157_928
PROPER_ZERO_VIOLATING_MINIMUM = PROPER_ZERO_TARGET + 1
PROPER_FIXED_G_CAP = 119_177
PROPER_FIXED_G_CAP_Q = RESIDUAL_K - 1
OCCUPIED_PROPER_G_MINIMUM = 19

SOURCE_RANK = 7
PAIR_COUNT = comb(SOURCE_RANK, 2)
PAIR_COMPLEMENT_INTERSECTION_CAP = RESIDUAL_K - 1
TOTAL_COMPLEMENT_INTERSECTION_CAP = (
    PAIR_COUNT * PAIR_COMPLEMENT_INTERSECTION_CAP
)
PAIR_COMPLEMENT_UNION_SUM_CAP = (
    6 * G + 5 * TOTAL_COMPLEMENT_INTERSECTION_CAP
)
PAIR_COMPLEMENT_UNION_CAP = PAIR_COMPLEMENT_UNION_SUM_CAP // PAIR_COUNT
FORCED_PAIR_OVERLAP = G - PAIR_COMPLEMENT_UNION_CAP
FORCED_COMMON_H = SIGMA
FORCED_PAIR_COFACTOR_SUM = 2 * G - (
    FORCED_PAIR_OVERLAP + FORCED_COMMON_H + W + 1
)

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = (
    ROOT
    / "experimental/data/schemas/"
    "m31_rank7_proper_g_zero_excess_incidence_route_cut_v1.schema.json"
)
VERIFIER_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_proper_g_zero_excess_incidence_route_cut_v1.py"
)
INDEPENDENT_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_proper_g_zero_excess_incidence_route_cut_v1_independent.py"
)
SAGE_PATH = (
    ROOT
    / "experimental/scripts/"
    "verify_m31_rank7_proper_g_zero_excess_incidence_route_cut_v1.sage"
)
NOTE_PATH = (
    ROOT
    / "experimental/notes/thresholds/"
    "m31_rank7_proper_g_zero_excess_incidence_route_cut_v1.md"
)
README_PATH = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-proper-g-zero-excess-incidence-route-cut-v1/README.md"
)
DEFAULT_MANIFEST = README_PATH.with_name("manifest.json")

PARENT_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-source-basis-private-root-overlap-dichotomy-v1/manifest.json"
)
PARENT_SHA256 = (
    "869822cdb063c30c9ebadc4879afbbda2e76318dcd3270f7d933e5d882c10a0a"
)
PARENT_PAYLOAD = (
    "e84de9e76f23f5645fe3d2fd5649319306109705ba59abb1c5111d33a00b1cd8"
)
SHALLOW_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-rank7-shallow-master-denominator-cut-v1/manifest.json"
)
SHALLOW_SHA256 = (
    "d8b24840a7a6ea4119defd0cad831e1eca256f754ac5dd07c4e63e7eb53f1d57"
)
SHALLOW_PAYLOAD = (
    "8135b49370b491cc14defb6c9e62648148fa2420a3d0cc45084ba00410eca239"
)
SHALLOW_NOTE = (
    ROOT
    / "experimental/notes/thresholds/"
    "m31_rank7_shallow_master_denominator_cut_v1.md"
)
SHALLOW_NOTE_SHA256 = (
    "5ad5018345fc12038aed37f646dde97cade756a27bf6b6aeca7348a8a85f0db3"
)
MIGRATION_MANIFEST = (
    ROOT
    / "experimental/data/certificates/"
    "m31-list-v4-grande-finale-provenance-migration-v1/manifest.json"
)
MIGRATION_SHA256 = (
    "f4b4fce7513d547d72b1caec9546099767c7dc38d610bb030371ea13361492fa"
)
MIGRATION_PAYLOAD = (
    "6ecd0eda3035aef7544646f0e3f1ddbf8b9aad4c0a1a9e0f8518ac22e3671479"
)
GRANDE_FINALE = ROOT / "experimental/grande_finale.tex"
GRANDE_FINALE_SHA256 = (
    "336ba3c9a6d9483d0eab74677d6224aae23adf15d84891c6099f6d2f45cf226d"
)


class VerificationError(RuntimeError):
    pass


CHECKS = 0
MAX_JSON_BYTES = 64 * 1024 * 1024
MAX_JSON_DEPTH = 256
MAX_SOURCE_BYTES = 64 * 1024 * 1024


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def canonical_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
        + b"\n"
    )


def repo_relative(path: Path, root: Path = ROOT) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError as exc:
        raise VerificationError(
            f"source path outside repository: {path}"
        ) from exc


def readonly_flags() -> int:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    if hasattr(os, "O_NONBLOCK"):
        flags |= os.O_NONBLOCK
    return flags


def sha256_path(path: Path, root: Path = ROOT) -> str:
    relative = repo_relative(path, root)
    safe_path = safe_repo_path(relative, root)
    digest = hashlib.sha256()
    descriptor = os.open(safe_path, readonly_flags())
    try:
        metadata = os.fstat(descriptor)
        require(stat.S_ISREG(metadata.st_mode), f"source regular: {relative}")
        require(
            metadata.st_size <= MAX_SOURCE_BYTES,
            f"source size: {relative}",
        )
        total = 0
        while chunk := os.read(descriptor, 1024 * 1024):
            total += len(chunk)
            require(total <= MAX_SOURCE_BYTES, f"source size: {relative}")
            digest.update(chunk)
    finally:
        os.close(descriptor)
    return digest.hexdigest()


def payload_sha256(value: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(value)
    unsigned.pop("payload_sha256", None)
    return hashlib.sha256(canonical_bytes(unsigned)).hexdigest()


def seal(value: dict[str, Any]) -> dict[str, Any]:
    output = copy.deepcopy(value)
    output.pop("payload_sha256", None)
    output["payload_sha256"] = payload_sha256(output)
    return output


def parse_strict_json(raw: bytes, label: str) -> dict[str, Any]:
    require(len(raw) <= MAX_JSON_BYTES, f"file size: {label}")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"non-ASCII JSON: {label}") from exc

    depth = 0
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            require(
                depth <= MAX_JSON_DEPTH,
                f"JSON nesting forbidden: {label}",
            )
        elif character in "]}":
            depth -= 1

    def reject_float(_value: str) -> Any:
        raise VerificationError("JSON float forbidden")

    def reject_constant(_value: str) -> Any:
        raise VerificationError("JSON constant forbidden")

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, f"duplicate JSON key: {key}")
            output[key] = value
        return output

    try:
        value = json.loads(
            text,
            object_pairs_hook=unique,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except RecursionError as exc:
        raise VerificationError(f"JSON nesting forbidden: {label}") from exc
    require(isinstance(value, dict), f"JSON object: {label}")
    return value


def strict_json(path: Path) -> dict[str, Any]:
    require(not path.is_symlink(), f"JSON path symlink: {path}")
    descriptor = os.open(path, readonly_flags())
    raw = bytearray()
    try:
        metadata = os.fstat(descriptor)
        require(stat.S_ISREG(metadata.st_mode), f"JSON regular file: {path}")
        require(metadata.st_size <= MAX_JSON_BYTES, f"file size: {path}")
        while chunk := os.read(descriptor, 1024 * 1024):
            raw.extend(chunk)
            require(len(raw) <= MAX_JSON_BYTES, f"file size: {path}")
    finally:
        os.close(descriptor)
    return parse_strict_json(bytes(raw), str(path))


def safe_repo_path(relative: str, root: Path = ROOT) -> Path:
    pure = PurePosixPath(relative)
    require(not pure.is_absolute(), "source path relative")
    require(".." not in pure.parts, "source path traversal")
    require("\\" not in relative, "source path separator")
    resolved_root = root.resolve(strict=True)
    path = root
    for part in pure.parts:
        path = path / part
        require(not path.is_symlink(), f"source path symlink: {relative}")
    require(path.exists(), f"source exists: {relative}")
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise VerificationError(
            f"source path outside repository: {relative}"
        ) from exc
    require(resolved.is_file(), f"source is file: {relative}")
    return resolved


def source_binding(
    binding_id: str,
    path: Path,
    role: str,
    internal_payload_sha256: str | None = None,
    root: Path = ROOT,
) -> dict[str, Any]:
    return {
        "binding_id": binding_id,
        "path": repo_relative(path, root),
        "role": role,
        "sha256": sha256_path(path, root),
        "internal_payload_sha256": internal_payload_sha256,
    }


def affine_cap(rank: int, ambient_gap: int, excess: int) -> int:
    return comb(ambient_gap + rank, rank) // comb(excess + rank, rank)


def direct_cap(rank: int, dimension: int, excess: int) -> int:
    child = (
        comb(K + rank - 1, rank - 1)
        // comb(excess + rank - 1, rank - 1)
    )
    value = (K + dimension) * child // (excess + dimension)
    denominator = (
        (excess + dimension) ** 2
        - (K + dimension) * (dimension - 1)
    )
    if denominator > 0:
        value = min(
            value,
            (K + dimension) * (excess + 1) // denominator,
        )
    return value


def recurrence_arrays(
    maximum_dimension: int,
    excess: int,
) -> dict[int, list[int]]:
    arrays: dict[int, list[int]] = {}
    rank_one = [0] * (maximum_dimension + 1)
    for dimension in range(1, maximum_dimension + 1):
        rank_one[dimension] = (K + dimension) // (excess + dimension)
    arrays[1] = rank_one

    for rank in range(2, 7):
        child = arrays[rank - 1]
        current = child.copy()
        prefix_cap = -1
        window: deque[int] = deque()
        for dimension in range(rank, maximum_dimension + 1):
            added = dimension - 1
            prefix_cap = max(prefix_cap, child[added])
            while window and child[window[-1]] <= child[added]:
                window.pop()
            window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            require(bool(window), "nonempty recurrence window")
            candidate = (
                (dimension - 1) * prefix_cap
                + (K + 1) * child[window[0]]
            ) // (excess + dimension)
            current[dimension] = max(
                child[dimension],
                min(candidate, direct_cap(rank, dimension, excess)),
            )
        arrays[rank] = current
    return arrays


def proper_fixed_g_cap(q: int) -> int:
    require(1 <= q < RESIDUAL_K, "proper fixed-G q range")
    numerator = comb(RADIUS - G + q + W + 5, 5)
    denominator = comb(W + 5, 5)
    return numerator // denominator


def support_sharpness() -> dict[str, Any]:
    patterns: list[tuple[int, ...]] = []
    for pair in combinations(range(7), 2):
        patterns.extend([pair] * PAIR_COMPLEMENT_INTERSECTION_CAP)
    singleton_counts = [
        35_771,
        35_771,
        35_770,
        35_770,
        35_770,
        35_770,
        35_770,
    ]
    for index, count in enumerate(singleton_counts):
        patterns.extend([(index,)] * count)
    require(len(patterns) == G, "support fixture universe")

    complement_sizes = [
        sum(index in pattern for pattern in patterns)
        for index in range(7)
    ]
    complement_pair_intersections = []
    locator_pair_overlaps = []
    for left, right in combinations(range(7), 2):
        complement_pair_intersections.append(
            sum(left in pattern and right in pattern for pattern in patterns)
        )
        locator_pair_overlaps.append(
            sum(
                left not in pattern and right not in pattern
                for pattern in patterns
            )
        )
    require(
        set(complement_pair_intersections)
        == {PAIR_COMPLEMENT_INTERSECTION_CAP},
        "support fixture complement intersections",
    )
    require(max(locator_pair_overlaps) == FORCED_PAIR_OVERLAP, "sharp overlap")
    return {
        "q2_pattern_count": PAIR_COUNT,
        "roots_per_q2_pattern": PAIR_COMPLEMENT_INTERSECTION_CAP,
        "q2_root_total": PAIR_COUNT * PAIR_COMPLEMENT_INTERSECTION_CAP,
        "q1_counts": singleton_counts,
        "q1_root_total": sum(singleton_counts),
        "universe_size": len(patterns),
        "complement_sizes": sorted(complement_sizes),
        "all_complement_pair_intersections":
            sorted(set(complement_pair_intersections)),
        "maximum_locator_pair_overlap": max(locator_pair_overlaps),
        "minimum_locator_pair_overlap": min(locator_pair_overlaps),
        "bound_attained": True,
        "polynomial_source_realized": False,
    }


# Small-field polynomial helpers.  Coefficients are low to high.
TOY_P = 31


def poly_trim(poly: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    output = list(poly)
    while len(output) > 1 and output[-1] % TOY_P == 0:
        output.pop()
    return tuple(value % TOY_P for value in output)


def poly_add(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    size = max(len(left), len(right))
    return poly_trim(
        [
            (
                (left[index] if index < len(left) else 0)
                + (right[index] if index < len(right) else 0)
            )
            % TOY_P
            for index in range(size)
        ]
    )


def poly_neg(poly: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((-value) % TOY_P for value in poly)


def poly_mul(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    output = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            output[left_index + right_index] = (
                output[left_index + right_index]
                + left_value * right_value
            ) % TOY_P
    return poly_trim(output)


def locator(roots: tuple[int, ...]) -> tuple[int, ...]:
    output = (1,)
    for root in roots:
        output = poly_mul(output, ((-root) % TOY_P, 1))
    return output


def rank_mod(rows: list[tuple[int, ...]]) -> int:
    if not rows:
        return 0
    width = max(len(row) for row in rows)
    matrix = [
        list(row) + [0] * (width - len(row))
        for row in rows
        if any(value % TOY_P for value in row)
    ]
    rank = 0
    for column in range(width):
        pivot = next(
            (
                row
                for row in range(rank, len(matrix))
                if matrix[row][column] % TOY_P
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, TOY_P)
        matrix[rank] = [
            value * inverse % TOY_P for value in matrix[rank]
        ]
        for row in range(len(matrix)):
            if row == rank or matrix[row][column] == 0:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (value - factor * pivot_value) % TOY_P
                for value, pivot_value in zip(matrix[row], matrix[rank])
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def maximum_support_intersection(
    supports: list[tuple[int, ...]],
) -> int:
    maximum_size = max(map(len, supports))
    for size in range(maximum_size, -1, -1):
        owners: dict[tuple[int, ...], int] = {}
        for index, support in enumerate(supports):
            for subset in combinations(support, size):
                if subset in owners and owners[subset] != index:
                    return size
                owners[subset] = index
    return 0


def finite_field_counterfixture() -> dict[str, Any]:
    p_roots = tuple(range(8))
    l_roots = tuple(range(8, 31))
    s_roots = (8,)
    records: list[
        tuple[
            tuple[int, ...],
            tuple[int, ...],
            tuple[int, ...],
            tuple[int, ...],
        ]
    ] = []
    by_g: dict[tuple[int, ...], int] = defaultdict(int)

    for m in range(1, 9):
        for g_roots in combinations(p_roots, m):
            g_poly = locator(g_roots)
            q_roots = tuple(sorted(set(p_roots) - set(g_roots)))
            q_poly = locator(q_roots)
            extras = tuple(root for root in l_roots if root not in s_roots)
            for extra_h in combinations(extras, m - 1):
                h_roots = tuple(sorted(s_roots + extra_h))
                if sum(g_roots) % TOY_P != sum(h_roots) % TOY_P:
                    continue
                h_poly = locator(h_roots)
                b_poly = poly_add(g_poly, poly_neg(h_poly))
                f_poly = poly_mul(q_poly, b_poly)
                require(len(b_poly) - 1 < m - 1, "toy b degree")
                require(len(f_poly) - 1 < 7, "toy f degree")
                padded = f_poly + (0,) * (7 - len(f_poly))
                records.append((padded, g_roots, q_roots, h_roots))
                by_g[g_roots] += 1

    messages = [record[0] for record in records]
    require(len(messages) == len(set(messages)), "toy distinct messages")
    require(len(records) == 65_671, "toy total")
    proper = [
        record for record in records if len(record[1]) < len(p_roots)
    ]
    full = [
        record for record in records if len(record[1]) == len(p_roots)
    ]
    require(len(proper) == 60_166, "toy proper")
    require(len(full) == 5_505, "toy full")
    require(len(by_g) == 235, "toy occupied G")
    require(max(by_g.values()) == 5_505, "toy fixed-G maximum")

    linear_rank = rank_mod(messages)
    anchor = messages[0]
    directions = [
        tuple((value - base) % TOY_P for value, base in zip(row, anchor))
        for row in messages[1:]
    ]
    direction_rank = rank_mod(directions)
    require(linear_rank == 7, "toy linear rank")
    require(direction_rank == 6, "toy direction rank")

    basis_indices: list[int] = []
    basis_rows: list[tuple[int, ...]] = []
    old_rank = 0
    for index, record in enumerate(records):
        if len(record[1]) == len(p_roots):
            continue
        new_rank = rank_mod(basis_rows + [record[0]])
        if new_rank > old_rank:
            basis_indices.append(index)
            basis_rows.append(record[0])
            old_rank = new_rank
        if old_rank == 7:
            break
    require(len(basis_indices) == 7, "toy proper source basis")
    require(
        set().union(*(set(records[index][1]) for index in basis_indices))
        == set(p_roots),
        "toy proper source basis lcm",
    )

    subfamily_indices = list(basis_indices)
    for index, record in enumerate(records):
        if len(subfamily_indices) == 29:
            break
        if index not in subfamily_indices and len(record[1]) < len(p_roots):
            subfamily_indices.append(index)
    require(len(subfamily_indices) == 29 < TOY_P - 1, "toy CRT-sized family")
    sub_rows = [records[index][0] for index in subfamily_indices]
    sub_anchor = sub_rows[0]
    sub_directions = [
        tuple(
            (value - base) % TOY_P
            for value, base in zip(row, sub_anchor)
        )
        for row in sub_rows[1:]
    ]
    require(rank_mod(sub_rows) == 7, "toy subfamily linear rank")
    require(rank_mod(sub_directions) == 6, "toy subfamily direction rank")
    require(
        set().union(*(set(records[index][1]) for index in subfamily_indices))
        == set(p_roots),
        "toy subfamily lcm",
    )

    residual_supports = [
        tuple(
            sorted(
                set(q_roots)
                | (set(h_roots) - set(s_roots))
            )
        )
        for _, _, q_roots, h_roots in records
    ]
    require(
        all(len(support) == 7 for support in residual_supports),
        "toy residual support sizes",
    )
    maximum_intersection = maximum_support_intersection(residual_supports)
    require(maximum_intersection == 5, "toy pair residual intersection")

    return {
        "field": TOY_P,
        "P_roots": list(p_roots),
        "L_roots": list(l_roots),
        "S_roots": list(s_roots),
        "w": 1,
        "d": 7,
        "k": 6,
        "Y": "P",
        "V": 1,
        "construction": "b=G-H; Q=P/G; f=Q*b=P-Q*H",
        "root_sum_gate": "sum Z(G)=sum Z(H) mod 31",
        "total_members": len(records),
        "proper_g_members": len(proper),
        "full_p_members": len(full),
        "occupied_g_slices": len(by_g),
        "maximum_fixed_g_slice": max(by_g.values()),
        "linear_rank": linear_rank,
        "label_direction_rank": direction_rank,
        "direction_after_L_S_division_is_full_degree_below_6": True,
        "common_direction_zero_count": 0,
        "complete_projective_line_size": 1,
        "master_lcm_restored": True,
        "common_V_literal": True,
        "full_gcd_identity_checked_by_sage": True,
        "zero_excess": True,
        "maximum_pair_residual_intersection": maximum_intersection,
        "pair_residual_intersection_cap": 5,
        "pure_proper_crt_sized_subfamily": {
            "size": len(subfamily_indices),
            "strictly_below_p_minus_1": True,
            "proper_g_members": len(subfamily_indices),
            "full_p_members": 0,
            "linear_rank": 7,
            "label_direction_rank": 6,
            "master_lcm_restored": True,
        },
        "deployed_parameter_counterexample": False,
        "one_slice_aggregation_bound_falsified": True,
        "universal_aggregate_factor_strictly_below_ratio_falsified": True,
        "aggregate_factor_obstruction_numerator": len(proper),
        "aggregate_factor_obstruction_denominator": max(by_g.values()),
    }


def build_template() -> dict[str, Any]:
    require(P_FIELD == 2_147_483_647, "M31 field")
    require(RADIUS == 981_129, "radius")
    require(W == 67_447, "excess")
    require(D == 287_525, "dimension")
    require(RESIDUAL_K == 4_981, "residual link")
    require(PAIR_COUNT == 21, "pair count")
    require(
        sha256_path(PARENT_MANIFEST) == PARENT_SHA256,
        "immediate parent file pin",
    )
    require(
        sha256_path(SHALLOW_MANIFEST) == SHALLOW_SHA256,
        "shallow parent file pin",
    )
    require(
        sha256_path(SHALLOW_NOTE) == SHALLOW_NOTE_SHA256,
        "fixed-G note pin",
    )
    require(
        sha256_path(MIGRATION_MANIFEST) == MIGRATION_SHA256,
        "migration file pin",
    )
    require(
        sha256_path(GRANDE_FINALE) == GRANDE_FINALE_SHA256,
        "Grande Finale pin",
    )

    arrays = recurrence_arrays(RESIDUAL_K, W + 1)
    excess_child = arrays[5][RESIDUAL_K - 1]
    excess_numerator = (K + RESIDUAL_K) * excess_child
    excess_denominator = W + 1 + RESIDUAL_K
    excess_quotient, excess_remainder = divmod(
        excess_numerator,
        excess_denominator,
    )
    require(excess_child == 444_522, "excess-one child")
    require(excess_quotient == POSITIVE_EXCESS_CAP, "excess-one cap")
    require(excess_remainder == 19_020, "excess-one remainder")

    rank_five = affine_cap(5, K, W)
    rank_five_plus = affine_cap(5, K, W + 1)
    require(rank_five == RANK_FIVE_CAP, "rank-five exact")
    require(
        rank_five_plus == RANK_FIVE_EXCESS_ONE_CAP,
        "rank-five excess exact",
    )

    full_numerator = comb(RADIUS - G + W + 6, 6)
    full_denominator = comb(W + 6, 6)
    full_quotient, full_remainder = divmod(
        full_numerator,
        full_denominator,
    )
    require(full_quotient == FULL_P_ZERO_CAP, "full-P cap")

    proper_numerator = comb(
        RADIUS - G + PROPER_FIXED_G_CAP_Q + W + 5,
        5,
    )
    proper_denominator = comb(W + 5, 5)
    proper_quotient, proper_remainder = divmod(
        proper_numerator,
        proper_denominator,
    )
    require(proper_quotient == PROPER_FIXED_G_CAP, "proper fixed-G cap")
    require(
        proper_fixed_g_cap(PROPER_FIXED_G_CAP_Q) == PROPER_FIXED_G_CAP,
        "proper fixed-G function",
    )
    require(
        all(
            proper_fixed_g_cap(q)
            <= proper_fixed_g_cap(q + 1)
            for q in range(1, PROPER_FIXED_G_CAP_Q)
        ),
        "proper fixed-G monotonicity",
    )

    proper_minimum = (
        VIOLATING_CLASS_MINIMUM
        - POSITIVE_EXCESS_CAP
        - FULL_P_ZERO_CAP
    )
    require(
        proper_minimum == PROPER_ZERO_VIOLATING_MINIMUM,
        "proper zero minimum",
    )
    require(
        POSITIVE_EXCESS_CAP + FULL_P_ZERO_CAP + PROPER_ZERO_TARGET
        == CLOSING_CLASS_CAP,
        "closing add-back",
    )
    require(
        ceil(PROPER_ZERO_VIOLATING_MINIMUM / PROPER_FIXED_G_CAP)
        == OCCUPIED_PROPER_G_MINIMUM,
        "occupied proper G",
    )

    pointwise = []
    for missing in range(7):
        present = 7 - missing
        missing_pairs = comb(missing, 2)
        present_pairs = comb(present, 2)
        pointwise.append(
            {
                "missing_count": missing,
                "present_count": present,
                "missing_incidence": missing,
                "one_plus_missing_pairs": 1 + missing_pairs,
                "present_pairs": present_pairs,
                "present_plus_five_missing_pairs":
                    present_pairs + 5 * missing_pairs,
            }
        )
        require(missing <= 1 + missing_pairs, "pointwise missing inequality")
        require(
            present_pairs + 5 * missing_pairs >= 15,
            "pointwise overlap inequality",
        )

    require(
        TOTAL_COMPLEMENT_INTERSECTION_CAP == 104_580,
        "total complement intersection",
    )
    require(
        PAIR_COMPLEMENT_UNION_SUM_CAP == 2_652_732,
        "pair union sum",
    )
    pair_union_quotient, pair_union_remainder = divmod(
        PAIR_COMPLEMENT_UNION_SUM_CAP,
        PAIR_COUNT,
    )
    require(pair_union_quotient == 126_320, "pair union quotient")
    require(pair_union_remainder == 12, "pair union remainder")
    require(FORCED_PAIR_OVERLAP == 228_652, "forced overlap")
    require(FORCED_PAIR_COFACTOR_SUM == 131_300, "cofactor sum")

    sharpness = support_sharpness()
    toy = finite_field_counterfixture()

    result: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture_id": THEOREM_ID,
        "status": STATUS,
        "row_contract": {
            "row": "Mersenne-31 list at 2^-100",
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "p": P_FIELD,
            "n": N,
            "K": K,
            "agreement": AGREEMENT,
            "radius": RADIUS,
            "w": W,
            "master_union_degree": G,
            "master_dimension": D,
            "largest_line_size": SIGMA,
            "residual_dimension": RESIDUAL_K,
            "cutoff_Q": Q_CUTOFF,
            "current_class_cap": CURRENT_CLASS_CAP,
            "closing_class_cap": CLOSING_CLASS_CAP,
            "required_improvement": CURRENT_CLASS_CAP - CLOSING_CLASS_CAP,
            "violating_class_minimum": VIOLATING_CLASS_MINIMUM,
            "counted_normalized_label_nonzero": True,
        },
        "dangerous_class_reduction": {
            "positive_common_direction_zero_cap": POSITIVE_Z_CAP,
            "violating_class_forces_z_zero": True,
            "rank_at_most_five_cap": rank_five,
            "violating_class_forces_actual_affine_rank": 6,
            "label_multiplicity_bound": SIGMA,
            "label_multiplicity_forced": SIGMA,
            "c_below_sigma_adds_at_least_one_agreement": True,
            "excess_one_recurrence": {
                "excess": W + 1,
                "rank_five_child_dimension": RESIDUAL_K - 1,
                "rank_five_child_cap": excess_child,
                "numerator": excess_numerator,
                "denominator": excess_denominator,
                "quotient": excess_quotient,
                "remainder": excess_remainder,
                "rank_at_most_five_fallback": rank_five_plus,
            },
            "positive_excess_portion_cap": POSITIVE_EXCESS_CAP,
            "positive_excess_and_zero_excess_disjoint": True,
            "full_p_zero_excess_cap": {
                "affine_direction_rank_cap": 6,
                "numerator_argument": 693_610,
                "denominator_argument": 67_453,
                "numerator": full_numerator,
                "denominator": full_denominator,
                "quotient": full_quotient,
                "remainder": full_remainder,
            },
            "proper_g_zero_excess_violating_minimum":
                PROPER_ZERO_VIOLATING_MINIMUM,
            "proper_g_zero_excess_closing_target": PROPER_ZERO_TARGET,
            "closing_add_back": CLOSING_CLASS_CAP,
            "proper_zero_portion_affine_rank": 6,
        },
        "proper_slice_bound": {
            "proper_slice_linear_rank_cap_before_label": 6,
            "nonzero_label_intersection_affine_direction_rank_cap": 5,
            "q_definition": "deg(P/G)",
            "small_q_range": [1, PROPER_FIXED_G_CAP_Q],
            "small_q_cap_formula":
                "floor(binomial(693604+q+5,5)/binomial(67452,5))",
            "small_q_cap_monotone": True,
            "maximum_cap_q": PROPER_FIXED_G_CAP_Q,
            "maximum_cap_numerator": proper_numerator,
            "maximum_cap_denominator": proper_denominator,
            "maximum_cap": proper_quotient,
            "maximum_cap_remainder": proper_remainder,
            "q_at_least_k_slice_cap": 1,
            "q_at_least_k_reason":
                "L_S*(P/G) divides every same-label difference and has degree at least d",
            "uniform_proper_fixed_g_cap": PROPER_FIXED_G_CAP,
            "minimum_occupied_proper_locators": OCCUPIED_PROPER_G_MINIMUM,
            "nineteen_slice_scalar_allowance":
                OCCUPIED_PROPER_G_MINIMUM * PROPER_FIXED_G_CAP,
            "nineteen_slice_scalar_allowance_exceeds_target": True,
            "independent_slice_caps_summable": False,
        },
        "seven_basis_incidence": {
            "proper_zero_mass_exceeds_rank_five_cap": True,
            "seven_members_affinely_independent": True,
            "seven_members_are_actual_proper_g_zero_excess_members": True,
            "nonzero_label_turns_affine_independence_into_linear_basis": True,
            "basis_size": SOURCE_RANK,
            "basis_restores_master_lcm": True,
            "pair_count": PAIR_COUNT,
            "C_ij_definition": "P/lcm(G_i,G_j)",
            "C_ij_divides_a_i_minus_a_j": True,
            "C_ij_coprime_to_L_S": True,
            "C_ij_degree_cap": PAIR_COMPLEMENT_INTERSECTION_CAP,
            "total_C_ij_degree_cap": TOTAL_COMPLEMENT_INTERSECTION_CAP,
            "pointwise_checks": pointwise,
            "total_missing_incidence_bound": "Q_total<=g+C_total",
            "pair_complement_union_identity": "sum_union=6*Q_total-C_total",
            "pair_complement_union_sum_cap": PAIR_COMPLEMENT_UNION_SUM_CAP,
            "pair_complement_union_average_quotient": pair_union_quotient,
            "pair_complement_union_average_remainder": pair_union_remainder,
            "one_pair_complement_union_cap": PAIR_COMPLEMENT_UNION_CAP,
            "total_locator_pair_overlap_floor": 4_801_680,
            "forced_pairwise_gcd_degree": FORCED_PAIR_OVERLAP,
        },
        "pair_factorization": {
            "J_definition": "gcd(G_i,G_j)",
            "G_i_factorization": "G_i=J*A_i",
            "G_j_factorization": "G_j=J*A_j",
            "C_definition": "P/lcm(G_i,G_j)",
            "Q_i_factorization": "Q_i=C*A_j",
            "Q_j_factorization": "Q_j=C*A_i",
            "sign_convention": "a_i-a_j=-C*T_ij",
            "reduced_determinant_identity": "A_i*b_j-A_j*b_i=L_S*T_ij",
            "reduced_determinant_nonzero": True,
            "T_ij_degree_cap": "4980-deg(C)",
            "K_ij_definition": "gcd(H_i,H_j)",
            "S_subset_K_ij": True,
            "K_ij_degree_floor": FORCED_COMMON_H,
            "K_ij_divides_reduced_determinant": True,
            "G_degree_sum_floor": 578_644,
            "q_i_plus_q_j_cap": FORCED_PAIR_COFACTOR_SUM,
            "paid_owner": None,
        },
        "abstract_support_sharpness": sharpness,
        "finite_field_counterfixture": toy,
        "remaining_terminal": {
            "name":
                "PROPER_G_ZERO_EXCESS_CROSS_COFACTOR_INTERLACED_INCIDENCE",
            "exact_missing_cap": PROPER_ZERO_TARGET,
            "sufficient_weighted_occupancy_inequality":
                "119177*N_(1<=q<=4980)+N_(q>=4981)<=2157928",
            "current_hypotheses_bound_occupied_slices": False,
            "current_hypotheses_bound_high_q_members": False,
            "paid_owner": None,
            "Q147595_closed": False,
            "next_exact_theorem":
                "global occupied-locator incidence from the complete C_ij/T_ij/common-V/full-gcd system",
        },
        "ledger_state": {
            "local_branch_reduction": True,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "U_paid": 3_730,
            "U_Q": None,
            "U_list_int": None,
            "U_ext": None,
            "U_new": None,
            "signed_Xi46_paid": False,
            "row_closed": False,
        },
        "nonclaims": {
            "proper_g_zero_excess_cap_proved": False,
            "Q147595_paid": False,
            "remaining_terminal_paid": False,
            "global_rank7_closed": False,
            "rank_at_least_8_treated": False,
            "v4_atom_paid": False,
            "row_upper_bound_proved": False,
            "toy_extrapolated_to_deployed_row": False,
            "stable_paper_modified": False,
            "lean_used": False,
        },
        "source_bindings": [
            source_binding(
                "packet_schema",
                SCHEMA_PATH,
                "Top-level envelope schema; nested semantics are verifier-closed.",
            ),
            source_binding("packet_verifier", VERIFIER_PATH, "Primary verifier."),
            source_binding(
                "independent_replay",
                INDEPENDENT_PATH,
                "Independent exact-integer and support replay.",
            ),
            source_binding(
                "sage_replay",
                SAGE_PATH,
                "Sage deployed arithmetic and exhaustive GF(31) source census.",
            ),
            source_binding("theorem_note", NOTE_PATH, "Proof and audit."),
            source_binding("packet_readme", README_PATH, "Replay contract."),
            source_binding(
                "source_basis_parent",
                PARENT_MANIFEST,
                "Immediate high-overlap route-cut predecessor.",
                PARENT_PAYLOAD,
            ),
            source_binding(
                "shallow_master_parent",
                SHALLOW_MANIFEST,
                "Master normalization and proper fixed-G rank loss.",
                SHALLOW_PAYLOAD,
            ),
            source_binding(
                "fixed_g_theorem_note",
                SHALLOW_NOTE,
                "Direct fixed-G affine-span theorem source.",
            ),
            source_binding(
                "provenance_migration",
                MIGRATION_MANIFEST,
                "Exact compatibility bridge for stale canonical-source hashes.",
                MIGRATION_PAYLOAD,
            ),
            source_binding(
                "current_grande_finale",
                GRANDE_FINALE,
                "Current affine-span theorem source after audited migration.",
            ),
        ],
    }
    return seal(result)


def validate_schema_shape(data: dict[str, Any]) -> None:
    schema = strict_json(SCHEMA_PATH)
    require(schema["$id"] == SCHEMA_ID, "schema id")
    require(
        schema["additionalProperties"] is False,
        "top-level schema rejects additional keys",
    )
    require(set(data) == set(schema["required"]), "closed top-level keys")
    for key, spec in schema["properties"].items():
        if "const" in spec:
            require(data[key] == spec["const"], f"schema const {key}")


def deep_exact(actual: Any, expected: Any, path: str = "root") -> None:
    require(type(actual) is type(expected), f"{path} type")
    if isinstance(expected, dict):
        require(set(actual) == set(expected), f"{path} keys")
        for key in expected:
            deep_exact(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        require(len(actual) == len(expected), f"{path} length")
        for index, value in enumerate(expected):
            deep_exact(actual[index], value, f"{path}[{index}]")
    else:
        require(actual == expected, f"{path} value")


def validate_source_contract(
    data: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    actual_bindings = data["source_bindings"]
    trusted_bindings = expected["source_bindings"]
    require(isinstance(actual_bindings, list), "source binding list")
    require(
        len(actual_bindings) == len(trusted_bindings),
        "source binding count",
    )
    for index, trusted in enumerate(trusted_bindings):
        actual = actual_bindings[index]
        require(isinstance(actual, dict), f"source binding object {index}")
        require(
            actual.get("binding_id") == trusted["binding_id"],
            f"binding id {index}",
        )
        require(
            actual.get("path") == trusted["path"],
            f"binding path {trusted['binding_id']}",
        )


def validate_sources(data: dict[str, Any]) -> None:
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    for binding in data["source_bindings"]:
        binding_id = binding["binding_id"]
        relative = binding["path"]
        require(binding_id not in seen_ids, "unique binding id")
        require(relative not in seen_paths, "unique source path")
        seen_ids.add(binding_id)
        seen_paths.add(relative)
        path = safe_repo_path(relative)
        require(
            binding["sha256"] == sha256_path(path),
            f"fresh source {binding_id}",
        )
        internal = binding["internal_payload_sha256"]
        if internal is not None:
            source = strict_json(path)
            require(source["payload_sha256"] == internal, "internal payload")
            require(payload_sha256(source) == internal, "internal seal")


def validate_semantics(data: dict[str, Any]) -> None:
    reduction = data["dangerous_class_reduction"]
    proper = data["proper_slice_bound"]
    incidence = data["seven_basis_incidence"]
    factor = data["pair_factorization"]
    toy = data["finite_field_counterfixture"]
    terminal = data["remaining_terminal"]
    ledger = data["ledger_state"]

    require(reduction["violating_class_forces_z_zero"] is True, "z gate")
    require(
        reduction["violating_class_forces_actual_affine_rank"] == 6,
        "rank gate",
    )
    require(
        reduction["positive_excess_and_zero_excess_disjoint"] is True,
        "disjoint mass partition",
    )
    require(
        reduction["proper_g_zero_excess_closing_target"]
        == PROPER_ZERO_TARGET,
        "proper target",
    )
    require(
        proper["q_at_least_k_slice_cap"] == 1,
        "large-q singleton",
    )
    require(
        proper["independent_slice_caps_summable"] is False,
        "no invalid slice summation",
    )
    require(
        incidence["seven_members_are_actual_proper_g_zero_excess_members"]
        is True,
        "actual proper source basis",
    )
    require(
        incidence["forced_pairwise_gcd_degree"] == FORCED_PAIR_OVERLAP,
        "forced overlap",
    )
    require(
        factor["sign_convention"] == "a_i-a_j=-C*T_ij",
        "factor sign convention",
    )
    require(
        factor["reduced_determinant_identity"]
        == "A_i*b_j-A_j*b_i=L_S*T_ij",
        "determinant sign",
    )
    require(factor["paid_owner"] is None, "pair owner absent")
    require(
        toy["deployed_parameter_counterexample"] is False,
        "toy scope",
    )
    require(
        toy["one_slice_aggregation_bound_falsified"] is True,
        "toy one-slice route cut",
    )
    require(
        toy[
            "universal_aggregate_factor_strictly_below_ratio_falsified"
        ]
        is True,
        "toy exact-factor route cut",
    )
    require(
        toy["aggregate_factor_obstruction_numerator"] == 60_166,
        "toy exact-factor numerator",
    )
    require(
        toy["aggregate_factor_obstruction_denominator"] == 5_505,
        "toy exact-factor denominator",
    )
    require(terminal["paid_owner"] is None, "terminal owner absent")
    require(terminal["Q147595_closed"] is False, "Q open")
    require(ledger["ledger_movement"] == 0, "zero ledger movement")
    require(ledger["row_closed"] is False, "row open")
    require(
        all(value is False for value in data["nonclaims"].values()),
        "all nonclaims false",
    )


def validation_phase(label: str, operation: Any) -> None:
    try:
        operation()
    except VerificationError as exc:
        raise VerificationError(f"{label}: {exc}") from exc
    except (
        IndexError,
        KeyError,
        OSError,
        RecursionError,
        TypeError,
        ValueError,
    ) as exc:
        raise VerificationError(
            f"{label}: malformed input ({type(exc).__name__})"
        ) from exc


def validate(
    data: dict[str, Any],
    expected: dict[str, Any] | None = None,
) -> None:
    trusted = expected if expected is not None else build_template()
    validation_phase("schema", lambda: validate_schema_shape(data))
    validation_phase(
        "payload",
        lambda: require(
            data["payload_sha256"] == payload_sha256(data),
            "payload seal",
        ),
    )
    validation_phase(
        "source-contract",
        lambda: validate_source_contract(data, trusted),
    )
    validation_phase("sources", lambda: validate_sources(data))
    validation_phase("semantics", lambda: validate_semantics(data))
    validation_phase("exact", lambda: deep_exact(data, trusted))


def mutate(
    data: dict[str, Any],
    path: tuple[str | int, ...],
    value: Any,
) -> dict[str, Any]:
    output = copy.deepcopy(data)
    cursor: Any = output
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    return seal(output)


def expect_rejected(
    label: str,
    candidate: dict[str, Any],
    expected: dict[str, Any],
    expected_phase: str,
    expected_reason: str,
) -> None:
    try:
        validate(candidate, expected)
    except VerificationError as exc:
        message = str(exc)
        require(
            message.startswith(f"{expected_phase}: "),
            f"mutation rejection phase: {label}",
        )
        require(
            expected_reason in message,
            f"mutation rejection reason: {label}",
        )
        return
    raise VerificationError(f"mutation accepted: {label}")


def expect_operation_rejected(
    label: str,
    operation: Any,
    expected_reason: str,
) -> None:
    try:
        operation()
    except VerificationError as exc:
        require(
            expected_reason in str(exc),
            f"direct rejection reason: {label}",
        )
        return
    raise VerificationError(f"hostile operation accepted: {label}")


def tamper_selftest(template: dict[str, Any]) -> None:
    mutations = [
        (
            "schema constant",
            mutate(
                template,
                ("schema",),
                f"{SCHEMA_ID}-tampered",
            ),
        ),
        ("cutoff Q", mutate(template, ("row_contract", "cutoff_Q"), 147_594)),
        (
            "residual k",
            mutate(template, ("row_contract", "residual_dimension"), 4_980),
        ),
        (
            "line sigma",
            mutate(template, ("row_contract", "largest_line_size"), 282_543),
        ),
        (
            "rank-five gate",
            mutate(
                template,
                ("dangerous_class_reduction", "rank_at_most_five_cap"),
                908_022,
            ),
        ),
        (
            "z gate",
            mutate(
                template,
                ("dangerous_class_reduction", "violating_class_forces_z_zero"),
                False,
            ),
        ),
        (
            "label multiplicity",
            mutate(
                template,
                ("dangerous_class_reduction", "label_multiplicity_forced"),
                SIGMA - 1,
            ),
        ),
        (
            "excess recurrence child",
            mutate(
                template,
                (
                    "dangerous_class_reduction",
                    "excess_one_recurrence",
                    "rank_five_child_cap",
                ),
                444_521,
            ),
        ),
        (
            "positive cap",
            mutate(
                template,
                ("dangerous_class_reduction", "positive_excess_portion_cap"),
                POSITIVE_EXCESS_CAP + 1,
            ),
        ),
        (
            "partition overlap",
            mutate(
                template,
                (
                    "dangerous_class_reduction",
                    "positive_excess_and_zero_excess_disjoint",
                ),
                False,
            ),
        ),
        (
            "full-P cap",
            mutate(
                template,
                (
                    "dangerous_class_reduction",
                    "full_p_zero_excess_cap",
                    "quotient",
                ),
                FULL_P_ZERO_CAP + 1,
            ),
        ),
        (
            "proper target",
            mutate(
                template,
                (
                    "dangerous_class_reduction",
                    "proper_g_zero_excess_closing_target",
                ),
                PROPER_ZERO_TARGET + 1,
            ),
        ),
        (
            "proper label rank",
            mutate(
                template,
                (
                    "proper_slice_bound",
                    "nonzero_label_intersection_affine_direction_rank_cap",
                ),
                6,
            ),
        ),
        (
            "large-q singleton",
            mutate(
                template,
                ("proper_slice_bound", "q_at_least_k_slice_cap"),
                2,
            ),
        ),
        (
            "proper fixed-G cap",
            mutate(
                template,
                ("proper_slice_bound", "uniform_proper_fixed_g_cap"),
                188_944,
            ),
        ),
        (
            "slice summation",
            mutate(
                template,
                ("proper_slice_bound", "independent_slice_caps_summable"),
                True,
            ),
        ),
        (
            "arbitrary basis",
            mutate(
                template,
                (
                    "seven_basis_incidence",
                    "seven_members_are_actual_proper_g_zero_excess_members",
                ),
                False,
            ),
        ),
        (
            "affine-linear bridge",
            mutate(
                template,
                (
                    "seven_basis_incidence",
                    "nonzero_label_turns_affine_independence_into_linear_basis",
                ),
                False,
            ),
        ),
        (
            "C degree",
            mutate(
                template,
                ("seven_basis_incidence", "C_ij_degree_cap"),
                4_981,
            ),
        ),
        (
            "pair count",
            mutate(
                template,
                ("seven_basis_incidence", "pair_count"),
                20,
            ),
        ),
        (
            "union coefficient",
            mutate(
                template,
                ("seven_basis_incidence", "pair_complement_union_identity"),
                "sum_union=5*Q_total-C_total",
            ),
        ),
        (
            "union floor",
            mutate(
                template,
                (
                    "seven_basis_incidence",
                    "one_pair_complement_union_cap",
                ),
                126_321,
            ),
        ),
        (
            "forced overlap",
            mutate(
                template,
                ("seven_basis_incidence", "forced_pairwise_gcd_degree"),
                FORCED_PAIR_OVERLAP - 1,
            ),
        ),
        (
            "factor sign",
            mutate(
                template,
                ("pair_factorization", "sign_convention"),
                "a_i-a_j=C*T_ij",
            ),
        ),
        (
            "determinant sign",
            mutate(
                template,
                ("pair_factorization", "reduced_determinant_identity"),
                "A_i*b_j-A_j*b_i=-L_S*T_ij",
            ),
        ),
        (
            "C-LS coprimality",
            mutate(
                template,
                ("seven_basis_incidence", "C_ij_coprime_to_L_S"),
                False,
            ),
        ),
        (
            "T degree",
            mutate(
                template,
                ("pair_factorization", "T_ij_degree_cap"),
                "4981-deg(C)",
            ),
        ),
        (
            "common H",
            mutate(
                template,
                ("pair_factorization", "K_ij_degree_floor"),
                SIGMA - 1,
            ),
        ),
        (
            "toy total",
            mutate(
                template,
                ("finite_field_counterfixture", "total_members"),
                65_670,
            ),
        ),
        (
            "toy aggregation obstruction numerator",
            mutate(
                template,
                (
                    "finite_field_counterfixture",
                    "aggregate_factor_obstruction_numerator",
                ),
                60_165,
            ),
        ),
        (
            "toy extrapolation",
            mutate(
                template,
                (
                    "finite_field_counterfixture",
                    "deployed_parameter_counterexample",
                ),
                True,
            ),
        ),
        (
            "forced owner",
            mutate(
                template,
                ("remaining_terminal", "paid_owner"),
                "UNJUSTIFIED_OWNER",
            ),
        ),
        (
            "false Q closure",
            mutate(
                template,
                ("remaining_terminal", "Q147595_closed"),
                True,
            ),
        ),
        (
            "ledger movement",
            mutate(template, ("ledger_state", "ledger_movement"), 1),
        ),
        (
            "source hash",
            mutate(template, ("source_bindings", 0, "sha256"), "0" * 64),
        ),
        (
            "source traversal",
            mutate(template, ("source_bindings", 0, "path"), "../schema.json"),
        ),
        (
            "untrusted in-repo source",
            mutate(template, ("source_bindings", 0, "path"), "agents.md"),
        ),
        (
            "parent payload",
            mutate(
                template,
                ("source_bindings", 6, "internal_payload_sha256"),
                "0" * 64,
            ),
        ),
        (
            "payload hash",
            {**template, "payload_sha256": "0" * 64},
        ),
    ]
    expected_rejections = {
        "schema constant": ("schema", "schema const schema"),
        "cutoff Q": ("exact", "root.row_contract.cutoff_Q value"),
        "residual k": (
            "exact",
            "root.row_contract.residual_dimension value",
        ),
        "line sigma": (
            "exact",
            "root.row_contract.largest_line_size value",
        ),
        "rank-five gate": (
            "exact",
            "root.dangerous_class_reduction.rank_at_most_five_cap value",
        ),
        "z gate": ("semantics", "z gate"),
        "label multiplicity": (
            "exact",
            "root.dangerous_class_reduction.label_multiplicity_forced value",
        ),
        "excess recurrence child": (
            "exact",
            "root.dangerous_class_reduction.excess_one_recurrence."
            "rank_five_child_cap value",
        ),
        "positive cap": (
            "exact",
            "root.dangerous_class_reduction.positive_excess_portion_cap value",
        ),
        "partition overlap": ("semantics", "disjoint mass partition"),
        "full-P cap": (
            "exact",
            "root.dangerous_class_reduction.full_p_zero_excess_cap."
            "quotient value",
        ),
        "proper target": ("semantics", "proper target"),
        "proper label rank": (
            "exact",
            "root.proper_slice_bound."
            "nonzero_label_intersection_affine_direction_rank_cap value",
        ),
        "large-q singleton": ("semantics", "large-q singleton"),
        "proper fixed-G cap": (
            "exact",
            "root.proper_slice_bound.uniform_proper_fixed_g_cap value",
        ),
        "slice summation": ("semantics", "no invalid slice summation"),
        "arbitrary basis": ("semantics", "actual proper source basis"),
        "affine-linear bridge": (
            "exact",
            "root.seven_basis_incidence."
            "nonzero_label_turns_affine_independence_into_linear_basis value",
        ),
        "C degree": (
            "exact",
            "root.seven_basis_incidence.C_ij_degree_cap value",
        ),
        "pair count": (
            "exact",
            "root.seven_basis_incidence.pair_count value",
        ),
        "union coefficient": (
            "exact",
            "root.seven_basis_incidence."
            "pair_complement_union_identity value",
        ),
        "union floor": (
            "exact",
            "root.seven_basis_incidence."
            "one_pair_complement_union_cap value",
        ),
        "forced overlap": ("semantics", "forced overlap"),
        "factor sign": ("semantics", "factor sign convention"),
        "determinant sign": ("semantics", "determinant sign"),
        "C-LS coprimality": (
            "exact",
            "root.seven_basis_incidence.C_ij_coprime_to_L_S value",
        ),
        "T degree": (
            "exact",
            "root.pair_factorization.T_ij_degree_cap value",
        ),
        "common H": (
            "exact",
            "root.pair_factorization.K_ij_degree_floor value",
        ),
        "toy total": (
            "exact",
            "root.finite_field_counterfixture.total_members value",
        ),
        "toy aggregation obstruction numerator": (
            "semantics",
            "toy exact-factor numerator",
        ),
        "toy extrapolation": ("semantics", "toy scope"),
        "forced owner": ("semantics", "terminal owner absent"),
        "false Q closure": ("semantics", "Q open"),
        "ledger movement": ("semantics", "zero ledger movement"),
        "source hash": ("sources", "fresh source packet_schema"),
        "source traversal": (
            "source-contract",
            "binding path packet_schema",
        ),
        "untrusted in-repo source": (
            "source-contract",
            "binding path packet_schema",
        ),
        "parent payload": ("sources", "internal payload"),
        "payload hash": ("payload", "payload seal"),
    }
    require(
        set(expected_rejections) == {label for label, _candidate in mutations},
        "complete phase-specific mutation expectations",
    )
    for label, candidate in mutations:
        phase, reason = expected_rejections[label]
        expect_rejected(label, candidate, template, phase, reason)

    expect_operation_rejected(
        "duplicate JSON key",
        lambda: parse_strict_json(
            b'{"x":1,"x":2}\n',
            "duplicate-control",
        ),
        "duplicate JSON key: x",
    )

    with TemporaryDirectory(prefix="m31-route-cut-hostile-") as raw_root:
        hostile_root = Path(raw_root)
        target = hostile_root / "target.json"
        target.write_bytes(b"{}\n")
        symlink = hostile_root / "source.json"
        symlink.symlink_to(target)
        expect_operation_rejected(
            "template-binding symlink source",
            lambda: source_binding(
                "hostile",
                symlink,
                "hostile",
                root=hostile_root,
            ),
            "source path symlink: source.json",
        )

        fifo = hostile_root / "source.fifo"
        os.mkfifo(fifo)
        expect_operation_rejected(
            "template-binding special source",
            lambda: source_binding(
                "hostile",
                fifo,
                "hostile",
                root=hostile_root,
            ),
            "source is file: source.fifo",
        )

        oversized = hostile_root / "oversized.json"
        with oversized.open("wb") as handle:
            handle.seek(MAX_JSON_BYTES)
            handle.write(b"\n")
        expect_operation_rejected(
            "oversized JSON before read",
            lambda: strict_json(oversized),
            "file size:",
        )

    deeply_nested = (
        ("[" * 10_000) + "0" + ("]" * 10_000)
    ).encode("ascii")
    expect_operation_rejected(
        "deep JSON nesting",
        lambda: parse_strict_json(deeply_nested, "nesting-control"),
        "JSON nesting forbidden: nesting-control",
    )

    print(
        "M31 rank7 proper-G zero-excess hostile controls: "
        f"PASS ({len(mutations) + 5} mutations)"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--print-template", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        template = build_template()
        if args.write:
            args.manifest.parent.mkdir(parents=True, exist_ok=True)
            args.manifest.write_bytes(canonical_bytes(template))
            print(f"wrote {args.manifest}")
        if args.print_template:
            sys.stdout.buffer.write(canonical_bytes(template))
        if args.check:
            validate(strict_json(args.manifest), template)
            print(
                "M31 rank7 proper-G zero-excess route cut: "
                f"PASS ({CHECKS} checks)"
            )
        if args.tamper_selftest:
            tamper_selftest(template)
        if not (
            args.write
            or args.print_template
            or args.check
            or args.tamper_selftest
        ):
            validate(strict_json(args.manifest), template)
            print(
                "M31 rank7 proper-G zero-excess route cut: "
                f"PASS ({CHECKS} checks)"
            )
    except (OSError, KeyError, TypeError, ValueError, VerificationError) as exc:
        print(
            f"M31 rank7 proper-G zero-excess route cut: FAIL: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(1)


if __name__ == "__main__":
    main()
