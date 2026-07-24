#!/usr/bin/env python3
"""Verify the M31 weighted-head and interlaced-source rank-seven route cut.

The positive theorem retains the exact agreement weights in the one-pivot
double count.  Full projective-line deletion and a planted-root source lift
then reject both the predecessor's H-saturated histogram and the strongest
declared single-level endpoint marginal.  A per-label dual-domain compiler
then pays the complete Q=26193 head and gives a sharp method route cut at
Q=26194.  Finally, seven exact boundary companions (plus the zero anchor)
give a genuine deployed source-compatible interlaced mixed-G obstruction.

The construction is deliberately combinatorial.  The common unit V is
supplied by the already-proved pairwise CRT equivalence after the exact
Wronskian gates are checked.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import deque
from functools import lru_cache
from pathlib import Path
from math import comb, gcd, isqrt
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / (
    "experimental/data/certificates/"
    "m31-rank7-weighted-head-interlaced-source-route-cut-v1/manifest.json"
)

P = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
L = B_STAR + 1
DEEP_CAP = 1_001_282
SHALLOW_L = B_STAR - DEEP_CAP
SHALLOW_TARGET = SHALLOW_L - 1

RANK = 7
G = 354_972
D = G - W
M = W + 1
Q = G - M
S = 0
DELTA = Q - S

WEIGHTED_CUTOFF = 26_144
WEIGHTED_H = G - WEIGHTED_CUTOFF
OLD_H_CUTOFF = 15_186
S_MAX = 366_886
Q6 = 222_004
D6 = 1_270_586
HARMONIC_LAYER = 65_515
HARMONIC_X_MIN = 10_411_669
HARMONIC_X_MAX = 10_411_790

SINGLE_LEVEL_HISTOGRAM_SHA256 = (
    "c393b083f7b71a8b03c8823153cae6e4c81044cd3924bfae002f8dd257a853d5"
)
SINGLE_LEVEL_TRANSPORT_SHA256 = (
    "e4fd2bbef5e5f983a9c6edeb75baf592c4f3c8aa1157816b998e978f5e29c2ae"
)
SINGLE_LEVEL_TRANSPORT_SPARSE_SHA256 = (
    "8bd18793245255c785979c0f447ac0cfeb7f3057c5504e6ffa38cbb49261ea20"
)

SCHEMA_ID = "m31-rank7-weighted-head-interlaced-source-route-cut-v1"
THEOREM_ID = "M31_RANK7_WEIGHTED_HEAD_INTERLACED_SOURCE_ROUTE_CUT_V1"
ARCHITECTURE_ID = "M31_RANK7_WEIGHTED_HEAD_INTERLACED_SOURCE_V1"
STATUS = "PROVED_WEIGHTED_HEAD_AND_SOURCE_OBSTRUCTION_ROW_OPEN"


class VerificationError(RuntimeError):
    """Raised when a fail-closed gate fails."""


def require(condition: bool, label: str, checks: list[str]) -> None:
    if not condition:
        raise VerificationError(label)
    checks.append(label)


def canonical_json(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise VerificationError("canonical JSON encoding") from exc
    return (text + "\n").encode("ascii")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_path(path: Path) -> str:
    if not path.is_file():
        raise VerificationError(f"missing source binding: {path}")
    return sha256_bytes(path.read_bytes())


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    result.pop("payload_sha256", None)
    result["payload_sha256"] = sha256_bytes(canonical_json(result))
    return result


def product(values: Any) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def falling(value: int, length: int) -> int:
    if length < 0 or value < length:
        raise VerificationError("falling factorial range")
    return product(value - index for index in range(length))


def ceil_div(numerator: int, denominator: int) -> int:
    if denominator <= 0:
        raise VerificationError("ceil-div denominator")
    return -((-numerator) // denominator)


def legal_q_bounds(union_size: int) -> tuple[int, int]:
    return (
        max(union_size - R, -S_MAX),
        min(W, union_size - W - 1),
    )


def rank_six_affine_head_cap(union_size: int, cutoff: int) -> int:
    """B_6(Q): the affine rank-at-most-six head cap after one pivot."""

    lower, upper = legal_q_bounds(union_size)
    if not lower <= cutoff <= upper:
        raise VerificationError("rank-six head cutoff")
    return comb(R - union_size + W + 6, 6) // comb(W - cutoff + 6, 6)


def weighted_e_rhs(union_size: int, cutoff: int) -> int:
    """Right side of sum_{delta<=Q}(g-delta) <= R B_6(Q)."""

    return R * rank_six_affine_head_cap(union_size, cutoff)


def old_one_pivot_cap(union_size: int, cutoff: int) -> int:
    agreement = union_size - cutoff
    return weighted_e_rhs(union_size, cutoff) // agreement


def rank_five_one_pivot_cap(union_size: int, cutoff: int) -> int:
    """Phi_Q(g): two-pivot cap used on each cofactor root."""

    agreement = union_size - cutoff
    inner = comb(R - union_size + W + 5, 5) // comb(W - cutoff + 5, 5)
    return R * inner // agreement


def rank_five_affine_cap(union_size: int, cutoff: int) -> int:
    """The inner B_5(Q) cap shared by every projective-column slice."""

    lower, upper = legal_q_bounds(union_size)
    if not lower <= cutoff <= upper:
        raise VerificationError("rank-five affine cutoff")
    return comb(R - union_size + W + 5, 5) // comb(W - cutoff + 5, 5)


def proper_fixed_g_cap(union_size: int, cofactor_degree: int) -> int:
    """Rank-at-most-six fixed-G cap at base agreement deg(G)=g-q."""

    if not 1 <= cofactor_degree <= union_size - W - 1:
        raise VerificationError("proper fixed-G moderate cofactor range")
    cutoff = min(cofactor_degree, W)
    denominator = max(cofactor_degree, W)
    inner = comb(R - union_size + cofactor_degree + W + 5, 5) // comb(
        denominator + 5,
        5,
    )
    return R * inner // (union_size - cutoff)


def two_stage_slice_envelope(
    union_size: int,
    cutoff: int,
) -> tuple[int, int, int, list[int], list[int]]:
    """Return (M_Q, winning rank, winning nu, caps by rank, nu by rank)."""

    dimension = union_size - W
    v = W - cutoff
    ambient_gap = R - dimension
    if v < 0:
        raise VerificationError("two-stage nonnegative excess")

    rank_caps = [1]
    rank_nu = [-1]
    global_best = 1
    global_rank = 0
    global_nu = -1
    for rank in range(1, 7):
        inner = comb(ambient_gap + rank - 1, rank - 1) // comb(
            v + rank - 1,
            rank - 1,
        )
        best = -1
        best_nu = -1
        for nu in range(rank, dimension):
            support_cap = (ambient_gap + nu) * inner // (v + nu)
            denominator = (v + nu) ** 2 - (ambient_gap + nu) * (nu - 1)
            if denominator > 0:
                johnson = (ambient_gap + nu) * (v + 1) // denominator
                candidate = min(support_cap, johnson)
            else:
                candidate = support_cap
            if candidate > best:
                best = candidate
                best_nu = nu
        rank_caps.append(best)
        rank_nu.append(best_nu)
        if best > global_best:
            global_best = best
            global_rank = rank
            global_nu = best_nu
    return global_best, global_rank, global_nu, rank_caps, rank_nu


def two_stage_head_cap(union_size: int, cutoff: int) -> tuple[int, Any]:
    envelope = two_stage_slice_envelope(union_size, cutoff)
    return R * envelope[0] // (union_size - cutoff), envelope


def generic_affine_johnson_cap(rank: int, dimension: int, excess: int) -> int:
    """Affine-span cap intersected with active common-zero Johnson."""

    if not 1 <= rank <= dimension:
        raise VerificationError("generic local rank/dimension")
    ambient_gap = R - D
    recursive = (
        (ambient_gap + dimension)
        * (
            comb(ambient_gap + rank - 1, rank - 1)
            // comb(excess + rank - 1, rank - 1)
        )
        // (excess + dimension)
    )
    denominator = (
        (excess + dimension) ** 2
        - (ambient_gap + dimension) * (dimension - 1)
    )
    if denominator > 0:
        johnson = (
            (ambient_gap + dimension) * (excess + 1) // denominator
        )
        return min(recursive, johnson)
    return recursive


def recursive_full_line_arrays(
    cutoff: int,
    *,
    max_rank: int = 7,
) -> tuple[dict[int, list[int]], list[dict[str, int]]]:
    """O(max_rank*d) full-projective-line deletion envelope."""

    excess = W - cutoff
    if excess < 0:
        raise VerificationError("recursive full-line excess")
    ambient_gap = R - D
    arrays: dict[int, list[int]] = {}
    base = [0] * (D + 1)
    for dimension in range(1, D + 1):
        base[dimension] = (
            ambient_gap + dimension
        ) // (excess + dimension)
    arrays[1] = base
    traces: list[dict[str, int]] = []

    for rank in range(2, max_rank + 1):
        child = arrays[rank - 1]
        legal_child_dimensions = range(rank - 1, D + 1)
        uniform_child = max(child[index] for index in legal_child_dimensions)
        uniform_arg = next(
            index
            for index in legal_child_dimensions
            if child[index] == uniform_child
        )
        current = child.copy()
        exact_rank = [0] * (D + 1)
        window: deque[int] = deque()
        for dimension in range(rank - 1, D + 1):
            added = dimension - 1
            if added >= rank - 1:
                while window and child[window[-1]] <= child[added]:
                    window.pop()
                window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            if dimension < rank:
                continue
            if not window:
                raise VerificationError("recursive full-line window")
            top_mass = dimension - 1
            two_tier = (
                top_mass * uniform_child
                + (ambient_gap + 1) * child[window[0]]
            ) // (excess + dimension)
            exact_rank[dimension] = min(
                two_tier,
                generic_affine_johnson_cap(rank, dimension, excess),
            )
            current[dimension] = max(
                child[dimension],
                exact_rank[dimension],
            )
        dominance_margin = min(
            exact_rank[dimension] - child[dimension]
            for dimension in range(rank, D + 1)
        )
        if dominance_margin < 0:
            raise VerificationError("exact-rank dominance gate")
        arrays[rank] = current
        maximum = max(current)
        traces.append(
            {
                "rank": rank,
                "uniform_child_cap": uniform_child,
                "uniform_child_arg_dimension": uniform_arg,
                "rank_cap_max": maximum,
                "rank_cap_arg_dimension": current.index(maximum),
                "exact_rank_cap_at_deployed_dimension": exact_rank[D],
                "at_most_rank_cap_at_deployed_dimension": current[D],
                "exact_rank_dominance_min_margin": dominance_margin,
            }
        )
    return arrays, traces


def full_rank_seven_projective_head_cap(
    cutoff: int,
) -> tuple[int, dict[str, Any]]:
    """Full top-six size-coupled rank-seven source envelope."""

    arrays, traces = recursive_full_line_arrays(cutoff, max_rank=6)
    child = arrays[6]
    top_six_sum = D - 1
    largest_class = D - 6
    class_caps = [0] + [
        child[D - size] for size in range(1, largest_class + 1)
    ]
    prefix_caps = [0] * (largest_class + 1)
    prefix_args = [0] * (largest_class + 1)
    for size in range(1, largest_class + 1):
        if class_caps[size] > prefix_caps[size - 1]:
            prefix_caps[size] = class_caps[size]
            prefix_args[size] = size
        else:
            prefix_caps[size] = prefix_caps[size - 1]
            prefix_args[size] = prefix_args[size - 1]

    best_numerator = -1
    best: dict[str, Any] | None = None
    for size in range(1, largest_class + 1):
        other_top_mass = top_six_sum - size
        other_top_size_cap = min(size, other_top_mass - 4)
        tail_size_cap = min(size, other_top_mass // 5)
        if other_top_size_cap < 1 or tail_size_cap < 1:
            continue
        numerator = (
            size * class_caps[size]
            + other_top_mass * prefix_caps[other_top_size_cap]
            + (R - top_six_sum) * prefix_caps[tail_size_cap]
        )
        if numerator > best_numerator:
            best_numerator = numerator
            best = {
                "largest_class_size": size,
                "largest_class_cap": class_caps[size],
                "other_top_mass": other_top_mass,
                "other_top_size_cap": other_top_size_cap,
                "other_top_cap": prefix_caps[other_top_size_cap],
                "other_top_cap_arg_size": prefix_args[other_top_size_cap],
                "tail_mass": R - top_six_sum,
                "tail_size_cap": tail_size_cap,
                "tail_cap": prefix_caps[tail_size_cap],
                "tail_cap_arg_size": prefix_args[tail_size_cap],
            }
    if best is None:
        raise VerificationError("full top-six optimizer")
    agreement = G - cutoff
    return best_numerator // agreement, {
        "objective_numerator": best_numerator,
        "head_cap": best_numerator // agreement,
        "top_six_sum_cap": top_six_sum,
        "lower_rank_cap": child[D],
        "recursive_trace": traces,
        **best,
    }


def planted_root_affine_cap(
    cutoff: int,
    residual_dimension: int,
) -> int | None:
    """Rank-six source cap after one full E0-line deletion.

    In the one-level q=delta=cutoff source specialization, a member in the
    deleted-line slice has a residual degree below ``residual_dimension`` and
    agrees with one fixed table on at least ``cutoff`` of the ``G`` planted
    roots.  The ordinary affine-span cap applies once the agreement threshold
    reaches the residual dimension.
    """

    if not 0 <= residual_dimension <= D:
        raise VerificationError("planted-root residual dimension")
    if residual_dimension > cutoff:
        return None
    return (
        comb(G - residual_dimension + 6, 6)
        // comb(cutoff - residual_dimension + 6, 6)
    )


def source_lifted_full_rank_seven_head_cap(
    cutoff: int,
) -> tuple[int, dict[str, Any]]:
    """Top-six optimizer with the planted-root cap on every eligible line."""

    arrays, traces = recursive_full_line_arrays(cutoff, max_rank=6)
    previous_planted = planted_root_affine_cap(cutoff, 0)
    if previous_planted is None:
        raise VerificationError("planted-root monotonicity base")
    planted_min_increment: int | None = None
    for residual_dimension in range(1, cutoff + 1):
        current_planted = planted_root_affine_cap(
            cutoff, residual_dimension
        )
        if current_planted is None or current_planted < previous_planted:
            raise VerificationError("planted-root cap monotonicity")
        increment = current_planted - previous_planted
        planted_min_increment = (
            increment
            if planted_min_increment is None
            else min(planted_min_increment, increment)
        )
        previous_planted = current_planted
    child = arrays[6]
    top_six_sum = D - 1
    largest_class = D - 6
    class_caps = [0] * (largest_class + 1)
    old_class_caps = [0] * (largest_class + 1)
    planted_class_caps: list[int | None] = [None] * (largest_class + 1)
    prefix_caps = [0] * (largest_class + 1)
    prefix_args = [0] * (largest_class + 1)

    for size in range(1, largest_class + 1):
        residual_dimension = D - size
        old_cap = child[residual_dimension]
        planted_cap = planted_root_affine_cap(cutoff, residual_dimension)
        cap = old_cap if planted_cap is None else min(old_cap, planted_cap)
        old_class_caps[size] = old_cap
        planted_class_caps[size] = planted_cap
        class_caps[size] = cap
        if cap > prefix_caps[size - 1]:
            prefix_caps[size] = cap
            prefix_args[size] = size
        else:
            prefix_caps[size] = prefix_caps[size - 1]
            prefix_args[size] = prefix_args[size - 1]

    best_numerator = -1
    best: dict[str, Any] | None = None
    for size in range(1, largest_class + 1):
        other_top_mass = top_six_sum - size
        other_top_size_cap = min(size, other_top_mass - 4)
        tail_size_cap = min(size, other_top_mass // 5)
        if other_top_size_cap < 1 or tail_size_cap < 1:
            continue
        numerator = (
            size * class_caps[size]
            + other_top_mass * prefix_caps[other_top_size_cap]
            + (R - top_six_sum) * prefix_caps[tail_size_cap]
        )
        if numerator > best_numerator:
            best_numerator = numerator
            planted_cap = planted_class_caps[size]
            best = {
                "largest_class_size": size,
                "largest_residual_dimension": D - size,
                "largest_class_old_cap": old_class_caps[size],
                "largest_class_planted_cap": planted_cap,
                "largest_class_cap": class_caps[size],
                "other_top_mass": other_top_mass,
                "other_top_size_cap": other_top_size_cap,
                "other_top_cap": prefix_caps[other_top_size_cap],
                "other_top_cap_arg_size": prefix_args[other_top_size_cap],
                "tail_mass": R - top_six_sum,
                "tail_size_cap": tail_size_cap,
                "tail_cap": prefix_caps[tail_size_cap],
                "tail_cap_arg_size": prefix_args[tail_size_cap],
            }
    if best is None:
        raise VerificationError("source-lifted top-six optimizer")
    agreement = G - cutoff
    return best_numerator // agreement, {
        "cutoff": cutoff,
        "planted_root_agreement": cutoff,
        "planted_root_domain_size": G,
        "planted_root_affine_rank": 6,
        "planted_cap_activation": "residual_dimension<=cutoff",
        "planted_cap_formula": (
            "floor(binomial(g-Kprime+6,6)/"
            "binomial(q-Kprime+6,6))"
        ),
        "initial_common_zero_reduction": {
            "state_map": (
                "(R,D,v)->(R-t,D-t,v+t), then add t to the "
                "largest projective-line class in the t=0 partition"
            ),
            "largest_residual_dimension": "UNCHANGED",
            "other_residual_dimensions": "Kprime->Kprime+t",
            "old_cap_monotonicity": (
                "C6(Kprime;v+t)<=C6(Kprime+t;v), with the "
                "largest-class special case C6(Kprime;v+t)<=C6(Kprime;v)"
            ),
            "planted_cap_monotonicity": (
                "A_q(Kprime+t)>=A_q(Kprime), or the planted cap "
                "becomes inactive"
            ),
            "planted_dimensions_checked": [0, cutoff],
            "planted_min_increment": planted_min_increment,
            "prefix_gate_map": (
                "sum_top_j+t<=D-t-7+j+t=D-7+j"
            ),
            "denominator": "g-q_UNCHANGED",
            "conclusion": "T_ZERO_IS_WORST_CASE",
        },
        "objective_numerator": best_numerator,
        "objective_remainder": best_numerator % agreement,
        "head_cap": best_numerator // agreement,
        "target_margin": SHALLOW_TARGET - best_numerator // agreement,
        "shallow_margin": SHALLOW_L - best_numerator // agreement,
        "top_six_sum_cap": top_six_sum,
        "lower_rank_cap": child[D],
        "recursive_trace": traces,
        **best,
    }


def parameterized_affine_johnson_cap(
    rank: int,
    dimension: int,
    ambient_gap: int,
    excess: int,
) -> int:
    """Affine one-pivot cap intersected with active Johnson."""

    if not 1 <= rank <= dimension:
        raise VerificationError("parameterized local rank/dimension")
    if ambient_gap < 0 or excess < 0:
        raise VerificationError("parameterized local gaps")
    inner = (
        comb(ambient_gap + rank - 1, rank - 1)
        // comb(excess + rank - 1, rank - 1)
    )
    result = (ambient_gap + dimension) * inner // (excess + dimension)
    denominator = (
        (excess + dimension) ** 2
        - (ambient_gap + dimension) * (dimension - 1)
    )
    if denominator > 0:
        result = min(
            result,
            (ambient_gap + dimension) * (excess + 1) // denominator,
        )
    return result


def local_prefix_projective_arrays(
    ambient_gap: int,
    excess: int,
    max_dimension: int,
    *,
    max_rank: int = 6,
) -> tuple[dict[int, list[int]], list[dict[str, int]]]:
    """Exact-rank/at-most-rank local-prefix projective compiler."""

    if ambient_gap < 0 or excess < 0 or max_dimension < max_rank:
        raise VerificationError("local-prefix parameters")
    arrays: dict[int, list[int]] = {}
    base = [0] * (max_dimension + 1)
    for dimension in range(1, max_dimension + 1):
        base[dimension] = (
            ambient_gap + dimension
        ) // (excess + dimension)
    arrays[1] = base
    traces: list[dict[str, int]] = []

    for rank in range(2, max_rank + 1):
        child = arrays[rank - 1]
        current = child.copy()
        exact = [0] * (max_dimension + 1)
        prefix_cap = -1
        prefix_arg = -1
        window: deque[int] = deque()
        dominance_violations = 0
        for dimension in range(rank, max_dimension + 1):
            added = dimension - 1
            if child[added] > prefix_cap:
                prefix_cap = child[added]
                prefix_arg = added
            while window and child[window[-1]] <= child[added]:
                window.pop()
            window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            if not window or prefix_arg < rank - 1:
                raise VerificationError("local-prefix window")
            two_tier = (
                (dimension - 1) * prefix_cap
                + (ambient_gap + 1) * child[window[0]]
            ) // (excess + dimension)
            exact[dimension] = min(
                two_tier,
                parameterized_affine_johnson_cap(
                    rank, dimension, ambient_gap, excess
                ),
            )
            if exact[dimension] < child[dimension]:
                dominance_violations += 1
            current[dimension] = max(
                child[dimension],
                exact[dimension],
            )
        arrays[rank] = current
        traces.append(
            {
                "rank": rank,
                "at_most_cap": current[max_dimension],
                "exact_cap": exact[max_dimension],
                "dominance_violations": dominance_violations,
            }
        )
    return arrays, traces


@lru_cache(maxsize=None)
def local_prefix_cap_six(
    ambient_gap: int,
    excess: int,
    dimension: int,
) -> int:
    arrays, _traces = local_prefix_projective_arrays(
        ambient_gap,
        excess,
        dimension,
        max_rank=6,
    )
    return arrays[6][dimension]


def top_six_outer_scan(
    cutoff: int,
    class_caps: list[int],
) -> tuple[int, dict[str, int], list[int]]:
    """Size-coupled outer scan from one cap for every line size."""

    largest_class = D - 6
    if len(class_caps) != largest_class + 1:
        raise VerificationError("top-six class cap length")
    prefix_caps = [0] * (largest_class + 1)
    prefix_args = [0] * (largest_class + 1)
    for size in range(1, largest_class + 1):
        if class_caps[size] > prefix_caps[size - 1]:
            prefix_caps[size] = class_caps[size]
            prefix_args[size] = size
        else:
            prefix_caps[size] = prefix_caps[size - 1]
            prefix_args[size] = prefix_args[size - 1]

    agreement = G - cutoff
    target_numerator = SHALLOW_TARGET * agreement
    best_numerator = -1
    best: dict[str, int] | None = None
    target_survivors: list[int] = []
    for size in range(1, largest_class + 1):
        other_top_mass = D - 1 - size
        other_top_size_cap = min(size, other_top_mass - 4)
        tail_size_cap = min(size, other_top_mass // 5)
        if other_top_size_cap < 1 or tail_size_cap < 1:
            continue
        numerator = (
            size * class_caps[size]
            + other_top_mass * prefix_caps[other_top_size_cap]
            + (R - (D - 1)) * prefix_caps[tail_size_cap]
        )
        if numerator > target_numerator:
            target_survivors.append(size)
        if numerator > best_numerator:
            best_numerator = numerator
            best = {
                "largest_class_size": size,
                "largest_residual_dimension": D - size,
                "largest_class_cap": class_caps[size],
                "other_top_mass": other_top_mass,
                "other_top_size_cap": other_top_size_cap,
                "other_top_cap": prefix_caps[other_top_size_cap],
                "other_top_cap_arg_size": prefix_args[other_top_size_cap],
                "tail_mass": R - (D - 1),
                "tail_size_cap": tail_size_cap,
                "tail_cap": prefix_caps[tail_size_cap],
                "tail_cap_arg_size": prefix_args[tail_size_cap],
                "objective_numerator": numerator,
                "objective_remainder": numerator % agreement,
                "head_cap": numerator // agreement,
            }
    if best is None:
        raise VerificationError("top-six outer optimizer")
    return best_numerator // agreement, best, target_survivors


def dual_domain_schedule(residual_dimension: int) -> int:
    return 44_835 - (67 * residual_dimension) // 10


def dual_domain_tangent_schedule(residual_dimension: int) -> int:
    return max(
        residual_dimension - 1,
        W
        + residual_dimension
        - isqrt((R - D + residual_dimension) * (residual_dimension - 1))
        - 11,
    )


def dual_domain_class_cap(
    cutoff: int,
    residual_dimension: int,
    split: int,
    old_cap: int,
) -> dict[str, int]:
    """Per-label-subclass E0/planted-domain split cap."""

    if not residual_dimension - 1 <= split < cutoff:
        raise VerificationError("dual-domain split legality")
    e_low = local_prefix_cap_six(
        R - D,
        W - split,
        residual_dimension,
    )
    planted = local_prefix_cap_six(
        G - residual_dimension,
        split + 1 - residual_dimension,
        residual_dimension,
    )
    phi = rank_five_one_pivot_cap(G, cutoff)
    high = max(phi, planted)
    dual_sum = e_low + high
    return {
        "cutoff": cutoff,
        "residual_dimension": residual_dimension,
        "split": split,
        "old_E0_cap": old_cap,
        "low_E0_cap": e_low,
        "Phi_Q": phi,
        "planted_cap": planted,
        "high_cap": high,
        "dual_sum": dual_sum,
        "refined_cap": min(old_cap, dual_sum),
    }


def dual_domain_rank_seven_positive_cap(
    cutoff: int,
    *,
    schedule_kind: str = "linear",
) -> tuple[int, dict[str, Any]]:
    """Refine every coarse-unpaid largest-line candidate."""

    if schedule_kind == "linear":
        schedule = dual_domain_schedule
        schedule_statement = "x(k)=44835-floor(67*k/10)"
    elif schedule_kind == "tangent_shift_11":
        schedule = dual_domain_tangent_schedule
        schedule_statement = (
            "x(k)=max(k-1,w+k-isqrt((A_E+k)(k-1))-11)"
        )
    else:
        raise VerificationError("dual-domain schedule kind")
    arrays, trace = local_prefix_projective_arrays(
        R - D,
        W - cutoff,
        D,
        max_rank=6,
    )
    child = arrays[6]
    largest_class = D - 6
    coarse_caps = [0] + [
        child[D - size] for size in range(1, largest_class + 1)
    ]
    coarse_head, coarse, survivors = top_six_outer_scan(
        cutoff, coarse_caps
    )
    refined_caps = coarse_caps.copy()
    records = []
    for size in survivors:
        residual_dimension = D - size
        split = schedule(residual_dimension)
        record = dual_domain_class_cap(
            cutoff,
            residual_dimension,
            split,
            coarse_caps[size],
        )
        record["class_size"] = size
        refined_caps[size] = record["refined_cap"]
        records.append(record)

    raw_dual_caps = [
        record["dual_sum"]
        for record in sorted(
            records, key=lambda item: item["residual_dimension"]
        )
    ]
    monotonicity_violations = sum(
        left > right
        for left, right in zip(
            raw_dual_caps,
            raw_dual_caps[1:],
        )
    )
    refined_head, refined, remaining = top_six_outer_scan(
        cutoff, refined_caps
    )
    return refined_head, {
        "cutoff": cutoff,
        "schedule": schedule_statement,
        "coarse_head": coarse_head,
        "coarse_certificate": coarse,
        "coarse_survivor_count": len(survivors),
        "coarse_survivor_size_interval": [
            min(survivors),
            max(survivors),
        ],
        "coarse_survivor_residual_interval": [
            D - max(survivors),
            D - min(survivors),
        ],
        "refined_count": len(records),
        "raw_dual_cap_first": raw_dual_caps[0],
        "raw_dual_cap_last": raw_dual_caps[-1],
        "raw_dual_cap_monotonicity_violations": monotonicity_violations,
        "remaining_survivor_count": len(remaining),
        "objective_numerator": refined["objective_numerator"],
        "head_cap": refined_head,
        "target_margin": SHALLOW_TARGET - refined_head,
        "certificate": refined,
        "first_refinement": min(
            records, key=lambda item: item["residual_dimension"]
        ),
        "last_refinement": max(
            records, key=lambda item: item["residual_dimension"]
        ),
        "local_trace": trace,
    }


def dual_domain_no_split_route_cut(
    cutoff: int,
    residual_dimension: int,
    old_cap: int,
) -> dict[str, Any]:
    """Exact monotone-interval cover proving no legal split improves a class."""

    declared_intervals = [
        (3_144, 23_768, 18, 15_764_297, 15_764_315),
        (23_769, 23_775, 16_772, 15_746_404, 15_763_176),
        (23_776, 23_778, 26_254, 15_736_663, 15_762_917),
        (23_779, 23_780, 34_649, 15_732_593, 15_767_242),
        (23_781, 23_785, 44_038, 15_718_801, 15_762_839),
        (23_786, 23_816, 136_553, 15_627_111, 15_763_664),
        (23_817, 26_193, 11_031_141, 8_136_412, 19_167_553),
    ]
    if declared_intervals[0][0] != residual_dimension - 1:
        raise VerificationError("no-split interval start")
    if declared_intervals[-1][1] != cutoff - 1:
        raise VerificationError("no-split interval end")
    phi = rank_five_one_pivot_cap(G, cutoff)
    rows = []
    previous_end = residual_dimension - 2
    for start, end, expected_low, expected_high, expected_sum in declared_intervals:
        if start != previous_end + 1 or start > end:
            raise VerificationError("no-split interval cover")
        low = local_prefix_cap_six(
            R - D,
            W - start,
            residual_dimension,
        )
        planted = local_prefix_cap_six(
            G - residual_dimension,
            end + 1 - residual_dimension,
            residual_dimension,
        )
        high = max(phi, planted)
        lower_sum = low + high
        if (low, high, lower_sum) != (
            expected_low,
            expected_high,
            expected_sum,
        ):
            raise VerificationError("no-split interval arithmetic")
        rows.append(
            {
                "start": start,
                "end": end,
                "E_low_at_start": low,
                "high_at_end": high,
                "sum_lower_bound": lower_sum,
                "excess_over_old": lower_sum - old_cap,
            }
        )
        previous_end = end
    minimum = min(row["sum_lower_bound"] for row in rows)
    return {
        "cutoff": cutoff,
        "residual_dimension": residual_dimension,
        "old_cap": old_cap,
        "Phi_Q": phi,
        "legal_split_interval": [residual_dimension - 1, cutoff - 1],
        "monotonicity": (
            "E(x) nondecreasing; max(Phi_Q,P(x+1)) nonincreasing"
        ),
        "intervals": rows,
        "minimum_dual_sum_lower_bound": minimum,
        "minimum_excess_over_old": minimum - old_cap,
        "conclusion": "NO_LEGAL_SPLIT_IMPROVES_THIS_CLASS",
    }


def dual_domain_global_e0_zero_reduction(cutoff: int) -> dict[str, Any]:
    """Pay large t directly and map the unique planted-active line for small t."""

    ambient_gap = R - D
    excess = W - cutoff

    def affine_rank_seven(t: int) -> int:
        return (
            comb(ambient_gap + 7, 7)
            // comb(excess + t + 7, 7)
        )

    low = 0
    high = D
    while low < high:
        middle = (low + high) // 2
        if affine_rank_seven(middle) <= SHALLOW_TARGET:
            high = middle
        else:
            low = middle + 1
    first_paid_t = low
    last_unpaid_t = first_paid_t - 1
    minimum_remaining_dimension = D - last_unpaid_t
    two_active_lower_sum = 2 * (
        minimum_remaining_dimension - cutoff
    )
    top_two_prefix_cap = minimum_remaining_dimension - 5
    return {
        "cutoff": cutoff,
        "generic_rank_seven_formula": (
            "floor(binomial(A_E+7,7)/binomial(v_Q+t+7,7))"
        ),
        "last_unpaid_t": last_unpaid_t,
        "last_unpaid_cap": affine_rank_seven(last_unpaid_t),
        "first_paid_t": first_paid_t,
        "first_paid_cap": affine_rank_seven(first_paid_t),
        "first_paid_margin": (
            SHALLOW_TARGET - affine_rank_seven(first_paid_t)
        ),
        "small_t_remaining_dimension_min": minimum_remaining_dimension,
        "twice_cutoff": 2 * cutoff,
        "two_planted_active_lines_size_lower_bound": two_active_lower_sum,
        "top_two_prefix_cap": top_two_prefix_cap,
        "uniqueness_margin": two_active_lower_sum - top_two_prefix_cap,
        "small_t_conclusion": (
            "AT_MOST_ONE_LINE_HAS_RESIDUAL_DIMENSION_LE_Q_"
            "AND_IT_IS_THE_LARGEST"
        ),
        "dummy_map": (
            "add all t to that largest line; its residual k, split x(k), "
            "and planted cap stay fixed; all other k>Q lines use the "
            "ordinary E-domain recurrence"
        ),
        "conclusion": "T_ZERO_SCAN_DOMINATES_ALL_INITIAL_E0_COMMON_ZEROS",
    }


def declared_top_six_relaxation(
    cutoff: int,
    top_six: list[int],
) -> tuple[int, dict[str, Any]]:
    """Evaluate one exact inequality-feasible top-six/tail packing."""

    if (
        len(top_six) != 6
        or any(size <= 0 for size in top_six)
        or top_six != sorted(top_six, reverse=True)
    ):
        raise VerificationError("declared top-six shape")
    if any(
        sum(top_six[:rank]) > D - 7 + rank
        for rank in range(1, 7)
    ):
        raise VerificationError("declared top-six prefix gate")
    if sum(top_six) != D - 1:
        raise VerificationError("declared top-six sum")
    arrays, _traces = recursive_full_line_arrays(cutoff, max_rank=6)
    child = arrays[6]
    class_caps = [child[D - size] for size in top_six]
    tail_size = top_six[-1]
    tail_mass = R - (D - 1)
    tail_full_classes, tail_remainder = divmod(tail_mass, tail_size)
    tail_cap = child[D - tail_size]
    tail_remainder_cap = child[D - tail_remainder]
    numerator = sum(
        size * cap for size, cap in zip(top_six, class_caps, strict=True)
    )
    numerator += (
        (tail_mass - tail_remainder) * tail_cap
        + tail_remainder * tail_remainder_cap
    )
    agreement = G - cutoff
    return numerator // agreement, {
        "top_six": top_six,
        "top_six_caps": class_caps,
        "tail_mass": tail_mass,
        "tail_size": tail_size,
        "tail_full_classes": tail_full_classes,
        "tail_remainder": tail_remainder,
        "tail_cap": tail_cap,
        "tail_remainder_cap": tail_remainder_cap,
        "objective_numerator": numerator,
        "head_cap": numerator // agreement,
    }


def predecessor_affine_cap(union_size: int, cutoff: int) -> int:
    return comb(R - union_size + W + 7, 7) // comb(W - cutoff + 7, 7)


def old_saturated_histogram() -> list[int]:
    histogram: list[int] = []
    previous = 0
    for deficit in range(OLD_H_CUTOFF + 1):
        current = old_one_pivot_cap(G, deficit)
        if current < previous:
            raise VerificationError("old cap monotonicity")
        histogram.append(current - previous)
        previous = current
    histogram.append(SHALLOW_L - previous)
    return histogram


def single_level_histogram() -> list[int]:
    result = [0] * (WEIGHTED_CUTOFF + 1)
    result[WEIGHTED_CUTOFF] = SHALLOW_L
    return result


def canonical_digest(value: Any) -> str:
    return sha256_bytes(canonical_json(value))


def scalar_resources(first: int, second: int, total: int) -> dict[str, Any]:
    six_factor = falling(W + 6, 6)
    inequalities = {
        "first_pivot": (
            total * G * six_factor,
            falling(R + G, 7),
        ),
        "colored_E": (
            (G * total - first) * six_factor,
            R * falling(R + G - 1, 6),
        ),
        "colored_S": (
            first * six_factor,
            G * falling(R + G - 1, 6),
        ),
        "cross_block": (
            (G * first - second) * comb(W + 5, 5),
            G * R * comb(R + G - 2, 5),
        ),
        "affine_line": (
            total * G * comb(W + 6, 5),
            15 * (R + G) * comb(R + G - 1, 5),
        ),
    }
    result: dict[str, Any] = {}
    for name, (lhs, rhs) in inequalities.items():
        if lhs > rhs:
            raise VerificationError(f"scalar resource failed: {name}")
        result[name] = {
            "lhs": lhs,
            "rhs": rhs,
            "margin": rhs - lhs,
            "utilization_parts_per_billion": lhs * 10**9 // rhs,
        }
    return result


def pi_profile(d6: int, mismatch: int) -> int:
    return (d6 - R + mismatch) * product(
        W + index + mismatch for index in range(1, 6)
    )


def harmonic_interval(total: int) -> tuple[int, int]:
    layer = HARMONIC_LAYER
    profile = W + 1
    pi_zero = pi_profile(D6, 0)
    pi_layer = pi_profile(D6, layer)
    t_capacity = layer * falling(D6, 6)
    u_capacity = falling(D6, 7)
    t_cost_zero = layer * pi_zero
    u_cost_zero = (profile - layer) * pi_zero
    u_cost_layer = profile * pi_layer
    high = min(total, t_capacity // t_cost_zero)
    low = max(
        0,
        ceil_div(
            total * u_cost_layer - u_capacity,
            u_cost_layer - u_cost_zero,
        ),
    )
    return low, high


def single_level_transport(total: int) -> tuple[list[list[int]], dict[str, int]]:
    dense = [[q, 0, 0] for q in range(WEIGHTED_CUTOFF + 1)]
    dense[WEIGHTED_CUTOFF] = [
        WEIGHTED_CUTOFF,
        HARMONIC_X_MIN,
        total - HARMONIC_X_MIN,
    ]
    sparse = {
        "delta": WEIGHTED_CUTOFF,
        "count": total,
        "b_zero": HARMONIC_X_MIN,
        "b_layer": total - HARMONIC_X_MIN,
    }
    return dense, sparse


def e0_rank_flag_resources(total: int, deficit: int) -> list[dict[str, int]]:
    """Universal truncated generalized-weight relaxation on E0."""

    dimension = G - W
    result = []
    for rank in range(0, 7):
        fiber_cap = comb(R - dimension + rank, rank) // comb(W + rank, rank)
        omega = product(
            W - deficit + index for index in range(rank + 1, 8)
        )
        lhs = total * omega
        rhs = fiber_cap * falling(R, 7 - rank)
        if lhs > rhs:
            raise VerificationError(f"E0 rank-flag resource failed: {rank}")
        result.append(
            {
                "rank": rank,
                "fiber_cap": fiber_cap,
                "lhs": lhs,
                "rhs": rhs,
                "margin": rhs - lhs,
                "utilization_parts_per_billion": lhs * 10**9 // rhs,
            }
        )
    return result


def source_bindings() -> list[dict[str, str]]:
    specifications = [
        (
            "schema",
            "experimental/data/schemas/"
            "m31_rank7_weighted_head_interlaced_source_route_cut_v1.schema.json",
            "Closed certificate schema.",
        ),
        (
            "primary",
            "experimental/scripts/"
            "verify_m31_rank7_weighted_head_interlaced_source_route_cut_v1.py",
            "Exact deployed arithmetic, existence proof, and mutations.",
        ),
        (
            "independent_sage",
            "experimental/scripts/"
            "verify_m31_rank7_weighted_head_interlaced_source_route_cut_v1.sage",
            "Independent arithmetic and direct finite-field realization.",
        ),
        (
            "packet",
            "experimental/scripts/"
            "verify_m31_rank7_weighted_head_interlaced_source_route_cut_packet_v1.py",
            "Fail-closed packet replay.",
        ),
        (
            "note",
            "experimental/notes/thresholds/"
            "m31_rank7_weighted_head_interlaced_source_route_cut_v1.md",
            "Proof, v4 chronology, and nonclaims.",
        ),
        (
            "readme",
            "experimental/data/certificates/"
            "m31-rank7-weighted-head-interlaced-source-route-cut-v1/README.md",
            "Replay instructions and scope.",
        ),
        (
            "common_v_predecessor",
            "experimental/notes/thresholds/"
            "m31_common_v_split_flat_pairwise_crt_equivalence_v1.md",
            "Pairwise Wronskian criterion for one common unit.",
        ),
        (
            "master_denominator_predecessor",
            "experimental/notes/thresholds/"
            "m31_rank7_shallow_master_denominator_cut_v1.md",
            "Master-denominator and exact full-gcd adapter.",
        ),
        (
            "effective_deficit_predecessor",
            "experimental/notes/thresholds/"
            "m31_rank7_effective_deficit_one_pivot_route_cut_v1.md",
            "Endpoint effective-deficit terminal.",
        ),
        (
            "v4_chronology",
            "experimental/notes/thresholds/"
            "m31_list_v4_global_completion_compiler.md",
            "Five-atom LIST chronology and signed credit gate.",
        ),
    ]
    result = []
    for binding_id, relative, role in specifications:
        result.append(
            {
                "binding_id": binding_id,
                "path": relative,
                "role": role,
                "sha256": sha256_path(ROOT / relative),
            }
        )
    return result


def derive_payload() -> dict[str, Any]:
    checks: list[str] = []

    # Exact weighted-head correction at the endpoint.
    old_histogram = old_saturated_histogram()
    require(sum(old_histogram) == SHALLOW_L, "old histogram total", checks)
    weighted_rejection_margins: dict[str, int] = {}
    for cutoff, expected_margin in [
        (0, 279_531),
        (1, -3_193_224),
        (2_463, -9_044_103_237),
        (15_186, -116_880_365_780),
    ]:
        lhs = sum(
            (G - deficit) * old_histogram[deficit]
            for deficit in range(cutoff + 1)
        )
        margin = weighted_e_rhs(G, cutoff) - lhs
        require(
            margin == expected_margin,
            f"old histogram weighted margin Q={cutoff}",
            checks,
        )
        weighted_rejection_margins[str(cutoff)] = margin
    require(
        weighted_rejection_margins["1"] < 0,
        "old histogram rejected at Q=1",
        checks,
    )

    old_single_head, old_single_envelope = two_stage_head_cap(G, 15_187)
    frontier_head, frontier_envelope = two_stage_head_cap(G, 15_838)
    next_head, next_envelope = two_stage_head_cap(G, 15_839)
    require(
        old_single_envelope[:3] == (5_052_479, 6, 4_638),
        "two-stage Q15187 optimizer",
        checks,
    )
    require(old_single_head == 14_589_030, "two-stage Q15187 head", checks)
    require(old_single_head < SHALLOW_L, "Q15187 all-L marginal rejected", checks)
    require(frontier_head == 15_774_764, "two-stage frontier head", checks)
    require(
        SHALLOW_L - frontier_head == 1_169,
        "two-stage forced frontier tail",
        checks,
    )
    require(frontier_head <= SHALLOW_TARGET, "two-stage frontier paid", checks)
    require(
        next_envelope[:3] == (5_453_288, 6, 4_513),
        "two-stage Q15839 optimizer",
        checks,
    )
    require(
        next_envelope[3] == [1, 13, 162, 2_240, 30_191, 405_788, 5_453_288],
        "two-stage Q15839 rank caps",
        checks,
    )
    require(
        next_envelope[4] == [-1, 1, 4_136, 4_486, 4_511, 4_513, 4_513],
        "two-stage Q15839 optimizer nu",
        checks,
    )
    require(next_head == 15_776_639, "two-stage next head", checks)
    require(next_head > SHALLOW_TARGET, "two-stage next unpaid", checks)

    intermediate_arrays, intermediate_trace = recursive_full_line_arrays(
        26_052, max_rank=7
    )
    intermediate_next_arrays, _ = recursive_full_line_arrays(
        26_053, max_rank=7
    )
    require(
        intermediate_arrays[7][D] == 15_775_392,
        "recursive two-tier Q26052",
        checks,
    )
    require(
        intermediate_next_arrays[7][D] == 15_776_368,
        "recursive two-tier Q26053",
        checks,
    )
    require(
        [
            record["uniform_child_cap"]
            for record in intermediate_trace
        ]
        == [16, 253, 3_987, 62_817, 989_693, 15_592_472],
        "recursive two-tier child maxima",
        checks,
    )
    require(
        [
            record["uniform_child_arg_dimension"]
            for record in intermediate_trace
        ]
        == [1, 2_620, 2_795, 2_806, 2_807, 2_808],
        "recursive two-tier child maximizers",
        checks,
    )

    recursive_frontier_head, recursive_frontier = (
        full_rank_seven_projective_head_cap(26_143)
    )
    recursive_next_head, recursive_next = (
        full_rank_seven_projective_head_cap(26_144)
    )
    require(
        recursive_frontier_head == 15_775_194,
        "full top-six Q26143 head",
        checks,
    )
    require(
        SHALLOW_TARGET - recursive_frontier_head == 738,
        "full top-six Q26143 target margin",
        checks,
    )
    require(
        recursive_frontier["objective_numerator"]
        == 5_187_341_399_069,
        "full top-six Q26143 numerator",
        checks,
    )
    require(
        (
            recursive_frontier["largest_class_size"],
            recursive_frontier["largest_class_cap"],
            recursive_frontier["other_top_mass"],
            recursive_frontier["other_top_size_cap"],
            recursive_frontier["other_top_cap"],
            recursive_frontier["other_top_cap_arg_size"],
            recursive_frontier["tail_size_cap"],
            recursive_frontier["tail_cap"],
            recursive_frontier["tail_cap_arg_size"],
        )
        == (
            284_730,
            15_737_600,
            2_794,
            2_790,
            1_014_691,
            2_783,
            558,
            1_014_323,
            553,
        ),
        "full top-six Q26143 optimizer",
        checks,
    )
    require(recursive_next_head == 15_776_151, "full top-six Q26144 head", checks)
    refined_next_head, refined_next = declared_top_six_relaxation(
        26_144,
        [284_730, 614, 545, 545, 545, 545],
    )
    require(
        refined_next_head == 15_776_148,
        "refined Q26144 relaxation head",
        checks,
    )
    require(
        refined_next["objective_numerator"] == 5_187_639_320_584,
        "refined Q26144 relaxation numerator",
        checks,
    )
    require(
        refined_next["top_six_caps"]
        == [15_738_557, 1_014_371, 1_014_361, 1_014_361, 1_014_361, 1_014_361],
        "refined Q26144 top-six caps",
        checks,
    )
    require(
        (
            refined_next["tail_full_classes"],
            refined_next["tail_remainder"],
            refined_next["tail_cap"],
            refined_next["tail_remainder_cap"],
        )
        == (1_272, 365, 1_014_361, 1_014_344),
        "refined Q26144 exact tail packing",
        checks,
    )
    require(
        refined_next_head > SHALLOW_TARGET,
        "refined Q26144 inequality-only relaxation exceeds target",
        checks,
    )
    source_lifted_head, source_lifted = (
        source_lifted_full_rank_seven_head_cap(WEIGHTED_CUTOFF)
    )
    require(
        source_lifted_head == 15_345_533,
        "source-lifted Q26144 head",
        checks,
    )
    require(
        source_lifted["objective_numerator"] == 5_046_040_936_511,
        "source-lifted Q26144 numerator",
        checks,
    )
    require(
        source_lifted["objective_remainder"] == 11_187,
        "source-lifted Q26144 remainder",
        checks,
    )
    require(
        source_lifted["target_margin"] == 430_399,
        "source-lifted Q26144 target margin",
        checks,
    )
    require(
        source_lifted["initial_common_zero_reduction"][
            "planted_min_increment"
        ]
        == 1_331,
        "source-lifted planted-cap monotonicity",
        checks,
    )
    require(
        (
            source_lifted["largest_class_size"],
            source_lifted["largest_residual_dimension"],
            source_lifted["largest_class_old_cap"],
            source_lifted["largest_class_planted_cap"],
            source_lifted["largest_class_cap"],
            source_lifted["other_top_mass"],
            source_lifted["other_top_size_cap"],
            source_lifted["other_top_cap"],
            source_lifted["other_top_cap_arg_size"],
            source_lifted["tail_size_cap"],
            source_lifted["tail_cap"],
            source_lifted["tail_cap_arg_size"],
        )
        == (
            283_663,
            3_862,
            15_294_703,
            15_295_049,
            15_294_703,
            3_861,
            3_857,
            1_014_887,
            3_846,
            772,
            1_014_383,
            757,
        ),
        "source-lifted Q26144 optimizer",
        checks,
    )
    require(
        source_lifted_head <= SHALLOW_TARGET,
        "source-lifted Q26144 one-level marginal rejected",
        checks,
    )
    dual_positive_head, dual_positive = (
        dual_domain_rank_seven_positive_cap(
            26_193,
            schedule_kind="linear",
        )
    )
    require(
        dual_positive_head == 15_775_776,
        "dual-domain Q26193 head",
        checks,
    )
    require(
        dual_positive["objective_numerator"] == 5_186_744_182_280,
        "dual-domain Q26193 numerator",
        checks,
    )
    require(
        dual_positive["target_margin"] == 156,
        "dual-domain Q26193 target margin",
        checks,
    )
    require(
        (
            dual_positive["coarse_survivor_count"],
            dual_positive["coarse_survivor_size_interval"],
            dual_positive["coarse_survivor_residual_interval"],
            dual_positive["refined_count"],
            dual_positive["remaining_survivor_count"],
        )
        == (
            239,
            [284_499, 284_737],
            [2_788, 3_026],
            239,
            0,
        ),
        "dual-domain Q26193 exhaustive survivors",
        checks,
    )
    require(
        (
            dual_positive["raw_dual_cap_first"],
            dual_positive["raw_dual_cap_last"],
            dual_positive["raw_dual_cap_monotonicity_violations"],
        )
        == (7_899_882, 12_277_361, 0),
        "dual-domain Q26193 linear-schedule caps",
        checks,
    )
    require(
        (
            dual_positive["certificate"]["largest_class_size"],
            dual_positive["certificate"]["largest_residual_dimension"],
            dual_positive["certificate"]["largest_class_cap"],
            dual_positive["certificate"]["objective_remainder"],
        )
        == (284_498, 3_027, 15_738_077, 324_776),
        "dual-domain Q26193 optimizer",
        checks,
    )
    require(
        all(
            record["dominance_violations"] == 0
            for record in dual_positive["local_trace"]
        ),
        "dual-domain exact-rank current-copy gate",
        checks,
    )
    e0_zero_reduction = dual_domain_global_e0_zero_reduction(26_193)
    require(
        (
            e0_zero_reduction["last_unpaid_t"],
            e0_zero_reduction["last_unpaid_cap"],
            e0_zero_reduction["first_paid_t"],
            e0_zero_reduction["first_paid_cap"],
            e0_zero_reduction["first_paid_margin"],
        )
        == (23_729, 15_776_593, 23_730, 15_774_894, 1_038),
        "dual-domain global E0-zero threshold",
        checks,
    )
    require(
        (
            e0_zero_reduction["small_t_remaining_dimension_min"],
            e0_zero_reduction["uniqueness_margin"],
        )
        == (263_796, 211_415),
        "dual-domain unique planted-active line",
        checks,
    )
    dual_negative_head, dual_negative = (
        dual_domain_rank_seven_positive_cap(
            26_194,
            schedule_kind="tangent_shift_11",
        )
    )
    require(
        dual_negative_head == 15_800_402,
        "dual-domain Q26194 tangent head",
        checks,
    )
    require(
        dual_negative["objective_numerator"] == 5_194_824_788_248,
        "dual-domain Q26194 tangent numerator",
        checks,
    )
    require(
        (
            dual_negative["certificate"]["largest_class_size"],
            dual_negative["certificate"]["largest_residual_dimension"],
            dual_negative["certificate"]["largest_class_cap"],
        )
        == (284_380, 3_145, 15_762_647),
        "dual-domain Q26194 tangent optimizer",
        checks,
    )
    no_split = dual_domain_no_split_route_cut(
        26_194,
        3_145,
        15_762_647,
    )
    require(no_split["Phi_Q"] == 4_008_251, "Q26194 route-cut Phi", checks)
    require(
        (
            no_split["minimum_dual_sum_lower_bound"],
            no_split["minimum_excess_over_old"],
            len(no_split["intervals"]),
        )
        == (15_762_839, 192, 7),
        "Q26194 seven-interval no-split route cut",
        checks,
    )

    new_histogram = single_level_histogram()
    require(sum(new_histogram) == SHALLOW_L, "single-level histogram total", checks)
    first_moment = SHALLOW_L * WEIGHTED_CUTOFF
    second_moment = SHALLOW_L * WEIGHTED_CUTOFF**2
    mixed_moment = G * first_moment - second_moment
    require(first_moment == 412_445_992_352, "single-level first moment", checks)
    require(
        second_moment == 10_782_988_024_050_688,
        "single-level second moment",
        checks,
    )
    require(
        mixed_moment == 135_623_790_773_123_456,
        "single-level mixed moment",
        checks,
    )
    b6_cutoff = rank_six_affine_head_cap(G, WEIGHTED_CUTOFF)
    h_cutoff = old_one_pivot_cap(G, WEIGHTED_CUTOFF)
    weighted_lhs = SHALLOW_L * WEIGHTED_H
    weighted_rhs = weighted_e_rhs(G, WEIGHTED_CUTOFF)
    weighted_margin = weighted_rhs - weighted_lhs
    require(b6_cutoff == 22_416_731, "single-level B6", checks)
    require(h_cutoff == 66_885_134, "single-level old H cap", checks)
    require(weighted_lhs == 5_187_568_496_524, "weighted E lhs", checks)
    require(weighted_rhs == 21_993_704_869_299, "weighted E rhs", checks)
    require(weighted_margin == 16_806_136_372_775, "weighted E margin", checks)
    require(
        predecessor_affine_cap(G, WEIGHTED_CUTOFF) == 376_385_666,
        "predecessor C head",
        checks,
    )

    # Cofactor-pivot resource.  The theorem and proper-slice cap are filled
    # below after their exact formulas are source-pinned.
    phi_cutoff = rank_five_one_pivot_cap(G, WEIGHTED_CUTOFF)
    cofactor_lhs = first_moment
    cofactor_rhs = G * phi_cutoff
    cofactor_margin = cofactor_rhs - cofactor_lhs
    require(phi_cutoff == 3_983_444, "cofactor Phi cutoff", checks)
    require(cofactor_rhs == 1_414_011_083_568, "cofactor weighted rhs", checks)
    require(cofactor_margin == 1_001_565_091_216, "cofactor weighted margin", checks)
    require(
        G * phi_cutoff // WEIGHTED_CUTOFF == 54_085_491,
        "cofactor band cap",
        checks,
    )

    f_cutoff = proper_fixed_g_cap(G, WEIGHTED_CUTOFF)
    f_values = [
        proper_fixed_g_cap(G, cofactor)
        for cofactor in range(1, G - W)
    ]
    f_max = max(f_values)
    f_max_q = f_values.index(f_max) + 1
    require(f_cutoff == 412_817, "proper fixed-G F_26144", checks)
    require(f_max == 624_046, "proper fixed-G F maximum", checks)
    require(f_max_q == W, "proper fixed-G F maximizer", checks)
    require(proper_fixed_g_cap(G, 1) == 317_828, "F_1 control", checks)
    require(
        proper_fixed_g_cap(G, 100_000) == 107_399,
        "F_100000 control",
        checks,
    )
    require(
        proper_fixed_g_cap(G, G - W - 1) == 1_576,
        "F_terminal control",
        checks,
    )

    slice_count = ceil_div(SHALLOW_L, f_cutoff)
    slice_counts = [f_cutoff] * (slice_count - 1)
    slice_counts.append(SHALLOW_L - sum(slice_counts))
    require(slice_count == 39, "proper-slice relaxation count", checks)
    require(slice_counts[-1] == 88_887, "proper-slice final count", checks)
    require(sum(slice_counts) == SHALLOW_L, "proper-slice count total", checks)

    # Exact cyclic cofactor-support/lcm marginal.
    require(gcd(WEIGHTED_CUTOFF, G) == 4, "cyclic gcd", checks)
    require(
        slice_count < G // gcd(WEIGHTED_CUTOFF, G),
        "cyclic starts distinct",
        checks,
    )
    root_loads = [0] * G
    root_word_loads = [0] * G
    support_starts = []
    for index, count in enumerate(slice_counts):
        start = (index * WEIGHTED_CUTOFF) % G
        support_starts.append(start)
        for offset in range(WEIGHTED_CUTOFF):
            root = (start + offset) % G
            root_loads[root] += 1
            root_word_loads[root] += count
    root_load_histogram = {
        str(load): root_loads.count(load) for load in sorted(set(root_loads))
    }
    require(
        root_load_histogram == {"2": 45_300, "3": 309_672},
        "cyclic cofactor root-load histogram",
        checks,
    )
    require(min(root_loads) == 2, "cyclic lcm coverage", checks)
    require(max(root_loads) == 3, "cyclic intersection empty", checks)
    require(
        max(root_word_loads) <= 3 * f_cutoff == 1_238_451,
        "cyclic per-root word load",
        checks,
    )
    require(
        max(root_word_loads) < phi_cutoff,
        "cyclic per-root load below Phi",
        checks,
    )

    scalar = scalar_resources(first_moment, second_moment, SHALLOW_L)
    require(
        [
            scalar[name]["utilization_parts_per_billion"]
            for name in [
                "first_pivot",
                "colored_E",
                "colored_S",
                "cross_block",
                "affine_line",
            ]
        ]
        == [69_379_632, 87_522_529, 19_233_358, 127_683_710, 91_623_946],
        "single-level scalar ppb",
        checks,
    )
    rank_flags = e0_rank_flag_resources(SHALLOW_L, WEIGHTED_CUTOFF)
    require(
        [record["utilization_parts_per_billion"] for record in rank_flags]
        == [
            3_699_023,
            8_786_552,
            19_876_982,
            45_605_940,
            105_301_025,
            243_213_036,
            561_762_488,
        ],
        "single-level E0 rank-flag ppb",
        checks,
    )
    harmonic_low, harmonic_high = harmonic_interval(SHALLOW_L)
    require(
        (harmonic_low, harmonic_high)
        == (HARMONIC_X_MIN, HARMONIC_X_MAX),
        "single-level harmonic interval",
        checks,
    )
    dense_transport, sparse_transport = single_level_transport(SHALLOW_L)
    require(
        dense_transport[WEIGHTED_CUTOFF]
        == [WEIGHTED_CUTOFF, 10_411_669, 5_364_264],
        "single-level transport row",
        checks,
    )
    require(
        canonical_digest(new_histogram) == SINGLE_LEVEL_HISTOGRAM_SHA256,
        "single-level histogram digest",
        checks,
    )
    require(
        canonical_digest(dense_transport) == SINGLE_LEVEL_TRANSPORT_SHA256,
        "single-level dense transport digest",
        checks,
    )
    require(
        canonical_digest(sparse_transport) == SINGLE_LEVEL_TRANSPORT_SPARSE_SHA256,
        "single-level sparse transport digest",
        checks,
    )
    b0_margin = WEIGHTED_H - HARMONIC_LAYER
    be_margin = (R - HARMONIC_LAYER) - WEIGHTED_H
    require(b0_margin == 263_313, "b=0 placement margin", checks)
    require(be_margin == 586_786, "b=e placement margin", checks)

    # Nested T_2048/T_32 boundary layout.
    big_blocks = 1_024
    small_per_big = 64
    small_blocks = big_blocks * small_per_big
    small_size = 32
    pairs_per_small = 16
    t2_pairs = small_blocks * pairs_per_small
    big_size = small_per_big * small_size
    two_extra_big = 887
    one_extra_big = 137
    extra_small = 2 * two_extra_big + one_extra_big
    baseline_s = 17
    s_in_two_extra = baseline_s * small_per_big + 2
    s_in_one_extra = baseline_s * small_per_big + 1
    e_in_two_extra = big_size - s_in_two_extra
    e_in_one_extra = big_size - s_in_one_extra

    require(big_size == 2_048, "T2048 block size", checks)
    require(small_blocks == 65_536, "T32 block count", checks)
    require(t2_pairs == 1_048_576, "T2 pair count", checks)
    require(two_extra_big + one_extra_big == big_blocks, "big block split", checks)
    require(extra_small == 1_911, "18-point T32 block count", checks)
    require(
        two_extra_big * s_in_two_extra + one_extra_big * s_in_one_extra == A,
        "S0 total",
        checks,
    )
    require(
        two_extra_big * e_in_two_extra + one_extra_big * e_in_one_extra == R,
        "E0 total",
        checks,
    )
    require(s_in_two_extra == 1_090, "S0 high T2048 occupancy", checks)
    require(s_in_one_extra == 1_089, "S0 low T2048 occupancy", checks)
    require(e_in_two_extra == 958, "E0 low T2048 occupancy", checks)
    require(e_in_one_extra == 959, "E0 high T2048 occupancy", checks)
    require(G <= t2_pairs, "one P root per T2 placement capacity", checks)

    # Seven degree-m split numerators.  Abstract root categories are later
    # injected into S0 with at most six P-roots per T32 block.
    unique_sizes = [33_973] * 4 + [33_972] * 3
    pair_base = 5_579
    extra_pairs = {(1, 2), (3, 4), (5, 6), (6, 7), (5, 7)}
    pair_sizes: dict[str, int] = {}
    pair_degrees = [0] * RANK
    for left in range(1, RANK + 1):
        for right in range(left + 1, RANK + 1):
            size = pair_base + int((left, right) in extra_pairs)
            pair_sizes[f"{left}-{right}"] = size
            pair_degrees[left - 1] += size
            pair_degrees[right - 1] += size

    numerator_sizes = [
        unique_sizes[index] + pair_degrees[index] for index in range(RANK)
    ]
    union_size = sum(unique_sizes) + sum(pair_sizes.values())
    require(sum(unique_sizes) == 237_808, "unique-root total", checks)
    require(sum(pair_sizes.values()) == 117_164, "pair-root total", checks)
    require(pair_degrees == [33_475] * 4 + [33_476] * 3, "pair degrees", checks)
    require(numerator_sizes == [M] * RANK, "all numerator degrees", checks)
    require(union_size == G, "exact lcm union degree", checks)
    require(6 * small_blocks >= G, "six-per-T32 P placement capacity", checks)
    require(6 < 17, "each G misses an S0 point in every T32 block", checks)

    # Give each H_i one distinct E0 point in every T32 block and then
    # 1,912 further distinct points, never more than two in one block.
    h_baseline = small_blocks
    h_extras_each = M - h_baseline
    h_total_extras = RANK * h_extras_each
    residual_e_after_baseline = R - RANK * small_blocks
    residual_per_t32_min = 14 - RANK
    require(h_extras_each == 1_912, "H extras per locator", checks)
    require(h_total_extras == 13_384, "H total extras", checks)
    require(
        residual_e_after_baseline == 522_377,
        "E0 residual after H baselines",
        checks,
    )
    require(residual_per_t32_min == 7, "minimum residual E0 per T32", checks)
    require(
        residual_per_t32_min * small_blocks >= h_total_extras,
        "disjoint H extra-slot capacity",
        checks,
    )

    # Choose global nonzero scalar labels sequentially.  At stage j the
    # values b_i G_j(x)/G_i(x), i<j and x in E0, are the only forbidden
    # values.  This makes every W_ij=G_i b_j-G_j b_i nonzero on all E0.
    label_forbidden_max = (RANK - 1) * R
    require(label_forbidden_max == 5_886_774, "label forbidden maximum", checks)
    require(label_forbidden_max < P - 1, "global scalar label field gate", checks)

    # Source and master arithmetic.
    require(P > N, "base field contains evaluation domain", checks)
    require(RANK < P - 1, "pairwise CRT field-size gate", checks)
    require(M == W + 1, "first legal numerator degree", checks)
    require(A - M == K - 1, "codeword degree", checks)
    require(Q == 287_524, "cofactor degree", checks)
    require(D == 287_525, "master message dimension", checks)
    require(Q == D - 1, "cofactor is maximal legal message degree", checks)
    require(DELTA == Q, "effective deficit", checks)
    require(G - DELTA == M, "H degree from effective deficit", checks)
    require(M + (A - M) == A, "exact agreement count", checks)
    require(M + (R - M) == R, "exact error weight", checks)
    require(RANK == 7, "unique-root evaluation rank", checks)
    require(RANK + 1 == 8, "anchor plus companion lower floor", checks)

    payload = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture": ARCHITECTURE_ID,
        "status": STATUS,
        "row": {
            "field_prime": P,
            "target_field_degree": 4,
            "n": N,
            "K": K,
            "agreement": A,
            "radius": R,
            "slack": W,
            "B_star": B_STAR,
            "forbidden_list_size": L,
            "object": "LIST",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
        },
        "weighted_head_theorem": {
            "general_statement": (
                "sum_{f in I_m} agr_E(f,u) <= (N-z)*B_{k-1}(z)"
            ),
            "B_formula": (
                "floor(binomial(N-d+k-1,k-1)/"
                "binomial(v+z+k-1,k-1))"
            ),
            "hypotheses": (
                "W linear rank k; u nowhere zero; z common zeros; "
                "m=d+v<=N-z"
            ),
            "m31_statement": (
                "sum_{delta_i<=Q}(g-delta_i) <= "
                "R*floor(binomial(R-g+w+6,6)/binomial(w-Q+6,6))"
            ),
            "proof": "EXACT_AGREEMENT_PIVOT_DOUBLE_COUNT",
            "status": "PROVED_SOURCE_BOUND",
        },
        "two_stage_pivot_johnson_theorem": {
            "pivot_slice_parameters": (
                "r<=6; z>=1 common zeros; c>=1 common agreements; "
                "nu=d-z>=r; b=z-c>=0"
            ),
            "B_formula": (
                "B_{r-1}=floor(binomial(A+r-1,r-1)/"
                "binomial(v+r-1,r-1))"
            ),
            "support_cap": (
                "C_r(nu,b)=floor((A+nu)*B_{r-1}/(v+nu+b))"
            ),
            "johnson_cap": (
                "J(nu,b)=floor((A+nu)*(v+b+1)/"
                "((v+nu+b)^2-(A+nu)*(nu-1))) when denominator>0"
            ),
            "b_monotonicity": (
                "C and active J are nonincreasing in b, so b=0 is safe"
            ),
            "r_zero_cap": 1,
            "M_definition": (
                "max_{1<=r<=6,r<=nu<=d-1} min(C_r(nu,0),"
                "J(nu,0) if active), together with r=0 cap 1"
            ),
            "head_statement": "N_{delta<=Q}<=floor(R*M_Q/(g-Q))",
            "status": "PROVED_SOURCE_BOUND",
        },
        "recursive_full_line_compiler": {
            "exact_rank_semantics": (
                "E_r bounds exact direction rank r; "
                "C_r=max_{0<=j<=r} E_j, with E_0<=1"
            ),
            "base": "C_1(N,K,m)=floor(N/m) when the direction has no domain zero",
            "line_deletion": (
                "(N,K,m,r)->(N-s,K-s,m-s,r-1) after deleting "
                "one full projective evaluation-line class"
            ),
            "exact_recurrence": (
                "E_r<=floor(max_partition sum_i s_i*C_{r-1}"
                "(N-s_i,K-s_i,m-s_i)/m), "
                "sum of top r-1 class sizes <=K-1"
            ),
            "two_tier_envelope": (
                "floor(((K-1)U_{r-1}+(A+1)M_{r-1}(K))/(K+v))"
            ),
            "algorithm": "EXACT_MONOTONE_DEQUE_O_7D",
            "rank_dominance_gate": (
                "Ehat_r>=C_{r-1} checked for every legal K at both "
                "deployed frontier endpoints"
            ),
            "intermediate_frontier": {
                "Q": 26_052,
                "head": intermediate_arrays[7][D],
                "next_Q": 26_053,
                "next_head": intermediate_next_arrays[7][D],
                "trace": intermediate_trace,
                "classification": "SAFE_TWO_TIER_NOT_SIZE_COUPLED",
            },
            "full_top_six_frontier": {
                "Q": 26_143,
                "head": recursive_frontier_head,
                "target_margin": SHALLOW_TARGET - recursive_frontier_head,
                "certificate": recursive_frontier,
                "next_Q": 26_144,
                "next_coarse_head": recursive_next_head,
                "next_coarse_certificate": recursive_next,
                "next_exact_relaxation": refined_next,
                "next_source_lifted_bound": source_lifted,
            },
            "lower_rank_cap_at_frontier": recursive_frontier["lower_rank_cap"],
            "status": "PROVED_SOURCE_BOUND",
        },
        "dual_domain_per_label_compiler": {
            "local_state": (
                "C_r(A,v,K) uses exact-rank projective recurrence; "
                "C_r=max(C_{r-1},Ehat_r), so lower ranks are retained"
            ),
            "E_domain_cap": "C6E_z(k)=C_6(A_E=R-d,v=w-z,K=k)",
            "planted_domain_cap": (
                "C6P(k,x+1)=C_6(A_P=g-k,v=x+1-k,K=k)"
            ),
            "per_subclass_dichotomy": (
                "delta<=x is paid by C6E_x; delta>=x+1 has at least "
                "x+1 planted agreements; a common planted agreement is "
                "paid by Phi_Q, otherwise C6P applies after fixed "
                "mismatches are factored"
            ),
            "refined_cap": (
                "D_Q(k,x)=min(C6E_Q(k),"
                "C6E_x(k)+max(Phi_Q,C6P(k,x+1)))"
            ),
            "split_legality": "k-1<=x<=Q-1",
            "monotonicity": {
                "E_domain": "C6E_x(k) is nondecreasing in x",
                "planted_domain": (
                    "max(Phi_Q,C6P(k,x+1)) is nonincreasing in x"
                ),
                "Johnson_derivative_numerator": (
                    "A-(A+1)K-v^2-2v<0"
                ),
                "preservation": (
                    "base, affine, two-tier, floor, min, and max "
                    "preserve the required directions"
                ),
            },
            "Q26193_positive": dual_positive,
            "global_E0_common_zero_reduction": e0_zero_reduction,
            "Q26194_tangent_scan": dual_negative,
            "Q26194_schedule_independent_route_cut": no_split,
            "frontier": {
                "last_paid_Q": 26_193,
                "last_paid_head": dual_positive_head,
                "last_paid_target_margin": (
                    SHALLOW_TARGET - dual_positive_head
                ),
                "first_unpaid_Q": 26_194,
                "tangent_head": dual_negative_head,
                "route_cut": (
                    "NO_PER_LABEL_TWO_DOMAIN_SPLIT_CAN_IMPROVE_"
                    "THE_Q26194_OUTER_MAXIMIZER"
                ),
            },
            "status": "PROVED_SOURCE_BOUND_AND_SHARP_METHOD_ROUTE_CUT",
        },
        "cofactor_pivot_theorem": {
            "statement": "sum_{delta_i<=Q} q_i <= g*Phi_Q(g)",
            "Phi_formula": (
                "floor(R/(g-Q)*floor("
                "binomial(R-g+w+5,5)/binomial(w-Q+5,5)))"
            ),
            "proof": "COFACTOR_ROOT_PIVOT_THEN_NOWHERE_ZERO_E0_PIVOT",
            "endpoint_cutoff": WEIGHTED_CUTOFF,
            "Phi_endpoint": phi_cutoff,
            "lhs_endpoint": cofactor_lhs,
            "rhs_endpoint": cofactor_rhs,
            "margin_endpoint": cofactor_margin,
            "band_corollary": (
                "#{D<=delta_i<=Q} <= floor(g*Phi_Q(g)/D), 1<=D<=Q"
            ),
            "endpoint_band_cap": G * phi_cutoff // WEIGHTED_CUTOFF,
            "proper_fixed_G_moderate_cap": (
                "F_q(g)=floor(R/(g-min(q,w))*floor("
                "binomial(R-g+q+w+5,5)/binomial(max(q,w)+5,5)))"
            ),
            "F_at_endpoint_cutoff": f_cutoff,
            "F_max": f_max,
            "F_max_q": f_max_q,
            "status": "PROVED_SOURCE_BOUND",
        },
        "endpoint_relaxation": {
            "g": G,
            "old_H_saturated_histogram_rejected": True,
            "old_histogram_weighted_margins": weighted_rejection_margins,
            "two_stage_common_zero_johnson": {
                "Q_15187_head": old_single_head,
                "Q_15187_optimizer": list(old_single_envelope[:3]),
                "frontier_Q": 15_838,
                "frontier_head": frontier_head,
                "frontier_forced_tail": SHALLOW_L - frontier_head,
                "next_Q": 15_839,
                "next_head": next_head,
                "next_optimizer": list(next_envelope[:3]),
                "next_rank_caps": next_envelope[3],
                "next_optimizer_nu": next_envelope[4],
            },
            "recursive_full_line_projective": {
                "paid_through_Q": 26_143,
                "paid_head": recursive_frontier_head,
                "paid_target_margin": SHALLOW_TARGET - recursive_frontier_head,
                "first_unpaid_Q": 26_144,
                "coarse_head": recursive_next_head,
                "exact_inequality_relaxation_head": refined_next_head,
                "exact_inequality_relaxation": refined_next,
                "source_lifted_head": source_lifted_head,
                "source_lifted_target_margin": source_lifted[
                    "target_margin"
                ],
                "source_lifted_certificate": source_lifted,
                "classification": (
                    "SOURCE_BOUND_UPPER_THROUGH_Q26143_AND_"
                    "SOURCE_IMPOSSIBLE_ONE_LEVEL_Q26144"
                ),
            },
            "tested_histogram": "ALL_SHALLOW_L_AT_DELTA_Q_26144",
            "delta": WEIGHTED_CUTOFF,
            "q": WEIGHTED_CUTOFF,
            "s": 0,
            "H_degree": WEIGHTED_H,
            "count": SHALLOW_L,
            "histogram_sha256": canonical_digest(new_histogram),
            "B6": b6_cutoff,
            "old_H_cap": h_cutoff,
            "weighted_E_lhs": weighted_lhs,
            "weighted_E_rhs": weighted_rhs,
            "weighted_E_margin": weighted_margin,
            "predecessor_C_cap": predecessor_affine_cap(G, WEIGHTED_CUTOFF),
            "first_moment": first_moment,
            "second_moment": second_moment,
            "mixed_moment": mixed_moment,
            "scalar_resources": scalar,
            "E0_rank_flag_resources": rank_flags,
            "harmonic": {
                "q6": Q6,
                "d6": D6,
                "layer": HARMONIC_LAYER,
                "x_interval": [harmonic_low, harmonic_high],
                "chosen_x": HARMONIC_X_MIN,
                "transport_row": dense_transport[WEIGHTED_CUTOFF],
                "dense_transport_sha256": canonical_digest(dense_transport),
                "sparse_transport": sparse_transport,
                "sparse_transport_sha256": canonical_digest(sparse_transport),
                "b_zero_placement_margin": b0_margin,
                "b_layer_placement_margin": be_margin,
            },
            "classification": (
                "EXACT_INTEGER_MARGINAL_REJECTED_BY_"
                "PLANTED_ROOT_SOURCE_LIFT"
            ),
        },
        "cofactor_slice_marginal": {
            "classification": "EXACT_COMBINATORIAL_RELAXATION_NOT_SOURCE",
            "proper_slice_count": slice_count,
            "slice_capacity": f_cutoff,
            "slice_counts": slice_counts,
            "cofactor_degree": WEIGHTED_CUTOFF,
            "cyclic_support_starts": support_starts,
            "cyclic_support_rule": (
                "Q_j={j*q,...,j*q+q-1} modulo g"
            ),
            "gcd_q_g": gcd(WEIGHTED_CUTOFF, G),
            "root_load_histogram": root_load_histogram,
            "root_load_min": min(root_loads),
            "root_load_max": max(root_loads),
            "root_word_load_max": max(root_word_loads),
            "Phi_per_root_cap": phi_cutoff,
            "Q_supports_distinct": True,
            "intersection_all_Q_empty": True,
            "lcm_G_equals_P": True,
            "nonclaim": "NO_COMMON_W_B_H_V_OR_FULL_GCD_SOURCE_REALIZATION",
        },
        "no_second_cofactor_pivot_witness": {
            "space": "W=<1> direct_sum Q*<1,X,...,X^5>",
            "dimension": 7,
            "degree_gate": "deg(Q)+5<d",
            "common_zero_on_ZP": False,
            "evaluation_on_each_alpha_dividing_Q": "[1,0,0,0,0,0,0]",
            "Q_root_column_rank": 1,
            "conclusion": "MANY_Q_ROOTS_REFUND_ONLY_ONE_RANK_IN_GENERAL",
            "classification": "STRUCTURAL_POLYNOMIAL_SPACE_NOT_SOURCE_LIST",
        },
        "boundary_layout": {
            "T2048_blocks": big_blocks,
            "T32_per_T2048": small_per_big,
            "T32_blocks": small_blocks,
            "T32_size": small_size,
            "T2_pairs_per_T32": pairs_per_small,
            "T2_pairs": t2_pairs,
            "E0_roots_per_T2_cap": 1,
            "T2048_size": big_size,
            "T2048_S0_1090_count": two_extra_big,
            "T2048_S0_1089_count": one_extra_big,
            "T32_S0_18_count": extra_small,
            "T32_S0_17_count": small_blocks - extra_small,
            "T32_E0_14_or_15": True,
            "T2048_E0_958_or_959": True,
        },
        "split_numerators": {
            "count": RANK,
            "degree_each": M,
            "unique_root_sizes": unique_sizes,
            "pair_root_base": pair_base,
            "extra_pairs": [list(pair) for pair in sorted(extra_pairs)],
            "pair_root_sizes": pair_sizes,
            "pair_incidence_degrees": pair_degrees,
            "union_degree": union_size,
            "P_roots_per_T32_cap": 6,
            "P_roots_per_T2_cap": 1,
            "each_G_has_unique_roots": True,
            "P_G_Q_have_no_complete_T2_fiber": True,
        },
        "interlaced_H_selection": {
            "degree_each": M,
            "pairwise_disjoint": True,
            "T32_blocks_hit_by_each_H": small_blocks,
            "baseline_roots_each": h_baseline,
            "extra_roots_each": h_extras_each,
            "total_extra_roots": h_total_extras,
            "H_roots_per_T32_min": 1,
            "H_roots_per_T32_max": 2,
            "residual_E0_after_baseline": residual_e_after_baseline,
            "minimum_residual_E0_per_T32": residual_per_t32_min,
            "H_has_no_complete_T2_fiber": True,
            "no_complete_T32_agreement_or_error_support": True,
            "no_complete_T2048_agreement_or_error_support": True,
        },
        "common_unit": {
            "b_i": "NONZERO_SCALARS_CHOSEN_SEQUENTIALLY",
            "forbidden_label_equation": "b_j=b_i*G_j(x)/G_i(x)",
            "forbidden_label_count_max": label_forbidden_max,
            "J_ij": 1,
            "W_ij": "G_i*b_j-G_j*b_i",
            "W_ij_nonzero_on_all_E0": True,
            "gcd_HiHj_Wij": 1,
            "family_size": RANK,
            "field_gate": "6*R < p-1",
            "consequence": "EXISTS_UNIT_V_WITH_H_i=gcd(L0,G_i-b_i*V)",
            "dependency": "IMPORTED_PROVED_PAIRWISE_CRT_EQUIVALENCE",
        },
        "master_normalization": {
            "g": G,
            "d": D,
            "m_i": M,
            "s_i": S,
            "q_i": Q,
            "delta_i": DELTA,
            "deg_H_i": M,
            "f_i": "Q_i*b_i=(P/G_i)*b_i",
            "deg_f_i": Q,
            "lcm_G_i": "P",
            "common_zero_on_ZP": False,
            "full_gcd": "gcd(P*L0,Y-f_i)=Q_i*H_i",
            "branch": "DEEP_DELTA_GREATER_THAN_W",
        },
        "source_consequence": {
            "zero_anchor": True,
            "companions": RANK,
            "total_certified_codewords": RANK + 1,
            "codeword": "c_i=(A0/G_i)*b_i",
            "codeword_degree": A - M,
            "exact_agreement": A,
            "exact_error_weight": R,
            "zero_anchored_rank": RANK,
            "mixed_G": True,
            "target_field_valid_by_base_field_embedding": True,
            "rigor": "PROVED_EXISTENCE",
        },
        "v4_chronology": {
            "architecture": "GRANDE_FINALE_V4_M31_LIST_SOURCE_ADAPTER_V1",
            "unit": "DISTINCT_CODEWORDS_PER_RECEIVED_WORD",
            "selected_codewords_are": "HIGH_BOUNDARY_EXACT_CODEWORD",
            "U_paid_movement": 0,
            "U_Q_movement": 0,
            "U_list_int_movement": 0,
            "U_ext_movement": 0,
            "U_new_movement": 0,
            "signed_Xi46_payment": False,
            "first_match_payment": False,
        },
        "impact": {
            "classification": "SOURCE_BOUND_ROUTE_CUT",
            "proved_lower_floor": 8,
            "complete_fiber_forcing_from_current_source_gates": False,
            "missing_theorem": (
                "BEYOND_PER_LABEL_TWO_DOMAIN_SPLITTING_AT_"
                "THE_Q26194_K3145_PRIMITIVE_CLASS"
            ),
            "missing_local_state": {
                "last_paid_head_cutoff": 26_193,
                "last_paid_head": dual_positive_head,
                "last_paid_target_margin": (
                    SHALLOW_TARGET - dual_positive_head
                ),
                "first_unpaid_head_cutoff": 26_194,
                "primitive_residual_dimension": 3_145,
                "primitive_old_cap": 15_762_647,
                "best_dual_sum_lower_bound": 15_762_839,
                "dual_method_gap": 192,
                "unresolved_object": (
                    "CROSS_SUBCLASS_OR_THIRD_DOMAIN_INCIDENCE"
                ),
            },
            "row_closed": False,
            "ledger_movement": 0,
        },
        "nonclaims": [
            "The construction has eight certified codewords, not 16,777,216.",
            "It is not a counterexample to the deployed M31 LIST bound.",
            "It does not determine the complete list of its received word.",
            "It does not produce a v4 atom upper payment or signed Xi_46 refund.",
            "It does not close the rank-seven census or any rank at least eight.",
            "No fixed-template or block-metric count is promoted to codeword add-back.",
            "Absence of complete ambient fibers does not exclude every quotient owner.",
        ],
        "source_bindings": source_bindings(),
        "checks": len(checks),
    }
    return seal(payload)


def exact_types_and_values(actual: Any, expected: Any, path: str = "payload") -> None:
    if type(actual) is not type(expected):
        raise VerificationError(f"{path}: exact type")
    if isinstance(expected, dict):
        if set(actual) != set(expected):
            raise VerificationError(f"{path}: exact keys")
        for key in expected:
            exact_types_and_values(actual[key], expected[key], f"{path}.{key}")
    elif isinstance(expected, list):
        if len(actual) != len(expected):
            raise VerificationError(f"{path}: exact list length")
        for index, (left, right) in enumerate(zip(actual, expected, strict=True)):
            exact_types_and_values(left, right, f"{path}[{index}]")
    elif actual != expected:
        raise VerificationError(f"{path}: exact value")


def validate_payload(
    payload: dict[str, Any],
    *,
    expected: dict[str, Any] | None = None,
) -> None:
    if type(payload) is not dict:
        raise VerificationError("top-level object")
    supplied_hash = payload.get("payload_sha256")
    if type(supplied_hash) is not str or len(supplied_hash) != 64:
        raise VerificationError("payload hash form")
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    if sha256_bytes(canonical_json(unsigned)) != supplied_hash:
        raise VerificationError("payload hash")
    if expected is None:
        expected = derive_payload()
    exact_types_and_values(payload, expected)


def mutate(payload: dict[str, Any], path: tuple[Any, ...], value: Any) -> dict[str, Any]:
    result = copy.deepcopy(payload)
    target: Any = result
    for component in path[:-1]:
        target = target[component]
    target[path[-1]] = value
    # Reseal so every semantic mutation passes the superficial hash gate.
    return seal(result)


def run_tamper_selftest() -> int:
    payload = derive_payload()
    mutations: list[tuple[str, Callable[[dict[str, Any]], dict[str, Any]]]] = [
        ("prime", lambda x: mutate(x, ("row", "field_prime"), P - 2)),
        ("agreement", lambda x: mutate(x, ("row", "agreement"), A - 1)),
        ("radius", lambda x: mutate(x, ("row", "radius"), R + 1)),
        ("slack", lambda x: mutate(x, ("row", "slack"), W + 1)),
        (
            "weighted-margin",
            lambda x: mutate(
                x,
                ("endpoint_relaxation", "weighted_E_margin"),
                429_887_678_710,
            ),
        ),
        (
            "two-stage-head",
            lambda x: mutate(
                x,
                (
                    "endpoint_relaxation",
                    "two_stage_common_zero_johnson",
                    "next_head",
                ),
                15_776_638,
            ),
        ),
        (
            "two-stage-rank-cap",
            lambda x: mutate(
                x,
                (
                    "endpoint_relaxation",
                    "two_stage_common_zero_johnson",
                    "next_rank_caps",
                    6,
                ),
                5_453_287,
            ),
        ),
        (
            "recursive-frontier",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "head",
                ),
                15_775_195,
            ),
        ),
        (
            "recursive-rank-semantics",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "exact_rank_semantics",
                ),
                "AT_MOST_RANK_ONLY",
            ),
        ),
        (
            "recursive-dominance",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "intermediate_frontier",
                    "trace",
                    0,
                    "exact_rank_dominance_min_margin",
                ),
                -1,
            ),
        ),
        (
            "recursive-tail-packing",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "next_exact_relaxation",
                    "tail_remainder",
                ),
                364,
            ),
        ),
        (
            "recursive-prefix-gate",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "next_exact_relaxation",
                    "top_six",
                    0,
                ),
                284_731,
            ),
        ),
        (
            "recursive-zero-class",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "next_exact_relaxation",
                    "top_six",
                    5,
                ),
                0,
            ),
        ),
        (
            "recursive-tail-count",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "next_exact_relaxation",
                    "tail_full_classes",
                ),
                1_271,
            ),
        ),
        (
            "source-lift-head",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "next_source_lifted_bound",
                    "head_cap",
                ),
                15_345_534,
            ),
        ),
        (
            "source-lift-activation",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "next_source_lifted_bound",
                    "planted_cap_activation",
                ),
                "residual_dimension<cutoff",
            ),
        ),
        (
            "source-lift-optimizer",
            lambda x: mutate(
                x,
                (
                    "recursive_full_line_compiler",
                    "full_top_six_frontier",
                    "next_source_lifted_bound",
                    "largest_class_size",
                ),
                283_664,
            ),
        ),
        (
            "dual-Q26193-head",
            lambda x: mutate(
                x,
                (
                    "dual_domain_per_label_compiler",
                    "Q26193_positive",
                    "head_cap",
                ),
                15_775_777,
            ),
        ),
        (
            "dual-Q26193-schedule",
            lambda x: mutate(
                x,
                (
                    "dual_domain_per_label_compiler",
                    "Q26193_positive",
                    "schedule",
                ),
                "TANGENT_SCHEDULE",
            ),
        ),
        (
            "dual-E0-zero-threshold",
            lambda x: mutate(
                x,
                (
                    "dual_domain_per_label_compiler",
                    "global_E0_common_zero_reduction",
                    "first_paid_t",
                ),
                23_729,
            ),
        ),
        (
            "dual-Q26194-interval",
            lambda x: mutate(
                x,
                (
                    "dual_domain_per_label_compiler",
                    "Q26194_schedule_independent_route_cut",
                    "intervals",
                    4,
                    "sum_lower_bound",
                ),
                15_762_838,
            ),
        ),
        (
            "cofactor-Phi",
            lambda x: mutate(
                x, ("cofactor_pivot_theorem", "Phi_endpoint"), 1_268_269
            ),
        ),
        (
            "proper-fixed-G-cap",
            lambda x: mutate(
                x,
                ("cofactor_pivot_theorem", "F_at_endpoint_cutoff"),
                372_427,
            ),
        ),
        (
            "slice-count",
            lambda x: mutate(
                x, ("cofactor_slice_marginal", "proper_slice_count"), 42
            ),
        ),
        (
            "slice-lcm",
            lambda x: mutate(
                x, ("cofactor_slice_marginal", "lcm_G_equals_P"), False
            ),
        ),
        (
            "histogram-digest",
            lambda x: mutate(
                x,
                ("endpoint_relaxation", "histogram_sha256"),
                "0" * 64,
            ),
        ),
        (
            "big-layout-count",
            lambda x: mutate(x, ("boundary_layout", "T2048_S0_1090_count"), 886),
        ),
        (
            "small-layout-count",
            lambda x: mutate(x, ("boundary_layout", "T32_S0_18_count"), 1_910),
        ),
        (
            "numerator-degree",
            lambda x: mutate(x, ("split_numerators", "degree_each"), M - 1),
        ),
        (
            "unique-size",
            lambda x: mutate(x, ("split_numerators", "unique_root_sizes", 0), 33_972),
        ),
        (
            "pair-base",
            lambda x: mutate(x, ("split_numerators", "pair_root_base"), 5_578),
        ),
        (
            "union-degree",
            lambda x: mutate(x, ("split_numerators", "union_degree"), G - 1),
        ),
        (
            "P-block-cap",
            lambda x: mutate(x, ("split_numerators", "P_roots_per_T32_cap"), 17),
        ),
        (
            "H-block-cap",
            lambda x: mutate(
                x, ("interlaced_H_selection", "H_roots_per_T32_max"), 15
            ),
        ),
        (
            "label-budget",
            lambda x: mutate(
                x, ("common_unit", "forbidden_label_count_max"), P - 1
            ),
        ),
        (
            "common-unit-family",
            lambda x: mutate(x, ("common_unit", "family_size"), P - 1),
        ),
        (
            "cofactor-degree",
            lambda x: mutate(x, ("master_normalization", "q_i"), Q - 1),
        ),
        (
            "effective-deficit",
            lambda x: mutate(x, ("master_normalization", "delta_i"), DELTA - 1),
        ),
        (
            "full-gcd",
            lambda x: mutate(
                x,
                ("master_normalization", "full_gcd"),
                "H_i",
            ),
        ),
        (
            "rank",
            lambda x: mutate(x, ("source_consequence", "zero_anchored_rank"), 6),
        ),
        (
            "codeword-floor",
            lambda x: mutate(x, ("impact", "proved_lower_floor"), 9),
        ),
        (
            "ledger-movement",
            lambda x: mutate(x, ("impact", "ledger_movement"), 1),
        ),
        (
            "signed-payment",
            lambda x: mutate(x, ("v4_chronology", "signed_Xi46_payment"), True),
        ),
        (
            "source-binding",
            lambda x: mutate(
                x, ("source_bindings", 0, "sha256"), "0" * 64
            ),
        ),
        (
            "remove-nonclaim",
            lambda x: seal(
                {**x, "nonclaims": x["nonclaims"][:-1], "payload_sha256": ""}
            ),
        ),
    ]
    passed = 0
    for label, operation in mutations:
        candidate = operation(payload)
        try:
            validate_payload(candidate, expected=payload)
        except VerificationError:
            passed += 1
            continue
        raise VerificationError(f"mutation unexpectedly accepted: {label}")
    print(f"[PASS] semantic mutations {passed}/{len(mutations)}")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-manifest", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    arguments = parser.parse_args()

    if arguments.tamper_selftest:
        run_tamper_selftest()
        return 0

    payload = derive_payload()
    validate_payload(payload, expected=payload)
    if arguments.write_manifest:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_bytes(canonical_json(payload))
    if arguments.json:
        print(canonical_json(payload).decode("ascii"), end="")
    else:
        print(
            "[PASS] M31 rank-seven interlaced mixed-G source obstruction "
            f"checks={payload['checks']} "
            f"payload={payload['payload_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
