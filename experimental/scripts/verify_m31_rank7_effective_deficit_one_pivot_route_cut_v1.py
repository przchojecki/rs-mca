#!/usr/bin/env python3
"""Verify the M31 rank-seven effective-deficit one-pivot route cut.

The positive theorem is a nowhere-zero refinement of the recursive
affine-span list compiler.  Applied to the master-denominator received table,
it bounds every cumulative effective-deficit head

    delta_i = q_i - s_i = g - deg(H_i)

by a nested-floor rank-six expression H_Q(g).

The negative result is deliberately narrower.  At the final residual cell,
the sharp H_Q histogram, with s=0 and q=delta, survives every scalar and
harmonic marginal resource printed by the predecessor packet.  This is an
exact integer relaxation, not a source family or a row closure.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import Counter
from math import comb
from typing import Any, Iterable


FIELD_PRIME = 2**31 - 1
N = 2**21
K = 2**20
A = 1_116_023
R = N - A
W = A - K
B_STAR = 2**24 - 1
DEEP_CAP = 1_001_282
L = B_STAR - DEEP_CAP
TARGET = L - 1
S_MAX = 366_886

RANK = 7
G_MIN = 72_428
G_MAX = 354_972
FIXED_G_LAST_PREPAID = 72_859
FIXED_G_NEW_TRANSITION = 217_543
Q_PROFILE = W + 1
D6_MIN = N - K + 6
MODULE_DEGREE = 2_048

SCHEMA_ID = "m31-rank7-effective-deficit-one-pivot-route-cut-summary-v1"
THEOREM_ID = "M31_RANK7_EFFECTIVE_DEFICIT_ONE_PIVOT_ROUTE_CUT_V1"
ARCHITECTURE_ID = (
    "M31_BASE_FIELD_BOUNDARY_RANK7_EFFECTIVE_DEFICIT_ONE_PIVOT_V1"
)
STATUS = "PROVED_ONE_PIVOT_HEAD_AND_FIXED_G_CLOSURE_ROUTE_CUT_ROW_OPEN"
PARENT_PAYLOAD = (
    "7d5df76a7188a66188cabfce710d4b4cb692be6a8e12428c99887ab882453625"
)

INTERVAL_SHA256 = (
    "4e2e2d6ddf919ace174a1cdd3f8df78520d0608a90c87fa231a5075cb8d13b52"
)
ENDPOINT_HISTOGRAM_SHA256 = (
    "7189e2ededaac854d54ee469451cf6e2f8afe5817c39d47ac65c355d1d04f4a0"
)
ENDPOINT_TRANSPORT_SHA256 = (
    "c3b09d3958cd5b6ebc4c78c937e3f86e5a5d95d632c3be7db3c136efbde6bb79"
)
ENDPOINT_SCALAR_RESOURCES_SHA256 = (
    "58789a52f5d9ba4dfc47a36b589232d34e7d447158c6d9c91bbe3e8cc3022dbe"
)


class VerificationError(RuntimeError):
    """Raised when an exact verification gate fails."""


CHECKS = 0


def require(condition: bool, label: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        raise VerificationError(label)


def product(values: Iterable[int]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def falling(value: int, length: int) -> int:
    require(length >= 0, "falling length nonnegative")
    require(value >= length, "falling argument large enough")
    return product(value - offset for offset in range(length))


def ceil_div(numerator: int, denominator: int) -> int:
    require(denominator > 0, "ceil-div denominator positive")
    return -((-numerator) // denominator)


def canonical_json(value: Any, *, pretty: bool = False) -> bytes:
    text = json.dumps(
        value,
        sort_keys=True,
        indent=2 if pretty else None,
        separators=None if pretty else (",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    )
    return (text + "\n").encode("ascii")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


def payload_sha256(payload: dict[str, Any]) -> str:
    unsigned = copy.deepcopy(payload)
    unsigned.pop("payload_sha256", None)
    return sha256_json(unsigned)


def legal_cutoff_bounds(union_size: int) -> tuple[int, int]:
    require(G_MIN <= union_size <= G_MAX, "union range")
    lower = max(union_size - R, -S_MAX)
    upper = min(W, union_size - W - 1)
    require(lower <= upper, "nonempty legal cutoff interval")
    return lower, upper


def one_pivot_cap(
    union_size: int,
    cutoff: int,
    *,
    rank: int = RANK,
    common_zeros: int = 0,
) -> int:
    """Nested-floor nowhere-zero one-pivot cap.

    Here the RS message dimension is d=g-w, the agreement threshold is
    m=g-Q, and its excess over d is v=w-Q.  The order of the two floors is
    load-bearing.
    """

    lower, upper = legal_cutoff_bounds(union_size)
    require(lower <= cutoff <= upper, "one-pivot cutoff range")
    require(1 <= rank <= RANK, "one-pivot rank range")
    require(0 <= common_zeros <= R, "common-zero range")

    dimension = union_size - W
    agreement = union_size - cutoff
    excess = W - cutoff
    require(1 <= dimension <= agreement <= R, "RS parameter order")
    if agreement > R - common_zeros:
        return 0

    inner_numerator = comb(
        R - dimension + rank - 1,
        rank - 1,
    )
    inner_denominator = comb(
        excess + common_zeros + rank - 1,
        rank - 1,
    )
    inner = inner_numerator // inner_denominator
    return (R - common_zeros) * inner // agreement


def affine_span_cap(union_size: int, cutoff: int) -> int:
    """Predecessor rank-seven cap, now valid for delta_i <= cutoff."""

    lower, upper = legal_cutoff_bounds(union_size)
    require(lower <= cutoff <= upper, "affine cutoff range")
    return comb(R - union_size + W + RANK, RANK) // comb(
        W - cutoff + RANK,
        RANK,
    )


def paid_cutoff(union_size: int) -> int:
    """Largest legal Q for which H_Q(g) is at most TARGET."""

    lower, upper = legal_cutoff_bounds(union_size)
    require(one_pivot_cap(union_size, lower) <= TARGET, "lower cutoff paid")
    if one_pivot_cap(union_size, upper) <= TARGET:
        return upper
    low, high = lower, upper
    while low < high:
        middle = (low + high + 1) // 2
        if one_pivot_cap(union_size, middle) <= TARGET:
            low = middle
        else:
            high = middle - 1
    return low


def endpoint_histogram() -> tuple[int, list[int]]:
    """Sharp H_Q marginal histogram at g=G_MAX, with s=0 and q=delta."""

    cutoff = paid_cutoff(G_MAX)
    require(cutoff >= 0, "endpoint cutoff nonnegative")
    histogram: list[int] = []
    previous = 0
    for deficit in range(cutoff + 1):
        current = one_pivot_cap(G_MAX, deficit)
        require(current >= previous, "endpoint caps nondecreasing")
        histogram.append(current - previous)
        previous = current
    histogram.append(L - previous)
    require(histogram[-1] > 0, "endpoint forced tail nonempty")
    return cutoff, histogram


def histogram_moments(histogram: list[int]) -> tuple[int, int, int]:
    total = sum(histogram)
    first = sum(index * count for index, count in enumerate(histogram))
    second = sum(
        index * index * count for index, count in enumerate(histogram)
    )
    return total, first, second


def affine_fiber_cap(dimension: int) -> int:
    require(1 <= dimension <= 5, "q6 affine-fiber dimension")
    return comb((N - K) + dimension, dimension) // comb(
        W + dimension,
        dimension,
    )


def raw_q6_cap(union_size: int, fiber_dimension: int) -> int:
    fixed = L * union_size * product(
        W + index for index in range(fiber_dimension + 1, RANK - 1)
    )
    numerator = affine_fiber_cap(fiber_dimension) * falling(
        R + union_size,
        RANK - fiber_dimension,
    )
    return numerator // fixed - (W + RANK - 1)


def q6_envelope(union_size: int) -> tuple[int, int, int]:
    raw_cap, winner = min(
        (raw_q6_cap(union_size, dimension), dimension)
        for dimension in range(1, RANK - 1)
    )
    strict_cap = union_size - W - RANK
    require(strict_cap >= 0, "strict generalized-weight cap")
    return min(raw_cap, strict_cap), winner, raw_cap


def pi_profile(d6: int, mismatch: int) -> int:
    require(d6 >= D6_MIN, "legal d6")
    require(mismatch >= 0, "nonnegative mismatch")
    return (d6 - R + mismatch) * product(
        W + index + mismatch for index in range(1, 6)
    )


def joint_q_b_transport(
    histogram: list[int],
    b_zero_total: int,
    union_size: int,
    layer: int,
) -> list[list[int]]:
    require(0 <= b_zero_total <= sum(histogram), "transport column range")
    remaining = b_zero_total
    table: list[list[int]] = []
    for deficit, count in enumerate(histogram):
        at_zero = min(count, remaining)
        at_layer = count - at_zero
        remaining -= at_zero
        require(at_zero >= 0 and at_layer >= 0, "transport nonnegative")
        require(at_zero + at_layer == count, "transport row marginal")
        if at_zero:
            require(layer <= union_size - deficit, "b=0 placement")
        if at_layer:
            require(union_size - deficit <= R - layer, "b=e placement")
        table.append([deficit, at_zero, at_layer])
    require(remaining == 0, "transport first column exhausted")
    require(sum(row[1] for row in table) == b_zero_total, "transport col 0")
    require(
        sum(row[2] for row in table) == sum(histogram) - b_zero_total,
        "transport col e",
    )
    return table


def scan_frontier() -> dict[str, Any]:
    intervals: list[dict[str, int]] = []
    interval_start = G_MIN
    interval_value = paid_cutoff(G_MIN)
    zero_tail_cells: list[dict[str, int]] = []
    maximum_tail_upper = (-1, -1, -1)

    record_cells = {
        72_428,
        72_540,
        72_859,
        72_860,
        100_000,
        150_000,
        200_000,
        217_542,
        217_543,
        250_000,
        300_000,
        328_677,
        328_678,
        354_397,
        354_972,
    }
    records: dict[str, Any] = {}

    for union_size in range(G_MIN, G_MAX + 1):
        cutoff = paid_cutoff(union_size)
        if cutoff != interval_value:
            intervals.append(
                {
                    "start": interval_start,
                    "end": union_size - 1,
                    "cutoff": interval_value,
                }
            )
            interval_start = union_size
            interval_value = cutoff

        cap = one_pivot_cap(union_size, cutoff)
        _, upper = legal_cutoff_bounds(union_size)
        next_cap = (
            one_pivot_cap(union_size, cutoff + 1)
            if cutoff < upper
            else None
        )
        require(cap <= TARGET, "frontier cap paid")
        require(next_cap is None or next_cap > TARGET, "frontier maximal")
        tail_upper = TARGET - cap
        if tail_upper == 0:
            zero_tail_cells.append({"g": union_size, "cutoff": cutoff})
        if tail_upper > maximum_tail_upper[0]:
            maximum_tail_upper = (tail_upper, union_size, cutoff)

        if union_size in record_cells:
            records[str(union_size)] = {
                "cutoff": cutoff,
                "head_cap": cap,
                "next_cap": next_cap,
                "forced_tail": L - cap,
                "tail_closure_upper": tail_upper,
            }

    intervals.append(
        {"start": interval_start, "end": G_MAX, "cutoff": interval_value}
    )
    interval_lengths = Counter(
        interval["end"] - interval["start"] + 1 for interval in intervals
    )
    digest = sha256_json(intervals)
    require(digest == INTERVAL_SHA256, "frontier interval digest")
    require(len(intervals) == 38_569, "frontier interval count")
    require(
        dict(sorted(interval_lengths.items()))
        == {2: 1, 4: 608, 5: 6_225, 6: 7_068, 7: 6_716,
            8: 6_640, 9: 6_750, 10: 4_475, 11: 86},
        "frontier interval length histogram",
    )
    require(
        maximum_tail_upper == (1_852, 354_397, 15_129),
        "maximum tail upper",
    )
    require(len(zero_tail_cells) == 204, "zero-tail cell count")

    return {
        "g_cells": G_MAX - G_MIN + 1,
        "legal_cutoff": (
            "max(g-R,-366886)<=Q<=min(w,g-w-1)"
        ),
        "interval_count": len(intervals),
        "interval_sha256": digest,
        "interval_length_histogram": {
            str(key): value for key, value in sorted(interval_lengths.items())
        },
        "cutoff_range": [
            intervals[0]["cutoff"],
            intervals[-1]["cutoff"],
        ],
        "sample_records": records,
        "maximum_tail_closure_upper": {
            "value": maximum_tail_upper[0],
            "g": maximum_tail_upper[1],
            "cutoff": maximum_tail_upper[2],
        },
        "zero_tail_closure_upper_cells": len(zero_tail_cells),
        "zero_tail_cells_sha256": sha256_json(zero_tail_cells),
    }


def endpoint_relaxation() -> dict[str, Any]:
    cutoff, histogram = endpoint_histogram()
    total, first, second = histogram_moments(histogram)
    require(total == L, "endpoint histogram total")
    require(cutoff == 15_186, "endpoint cutoff")
    require(len(histogram) == 15_188, "endpoint histogram rows")
    require(histogram[-1] == 1_184, "endpoint tail")
    require(first == 122_692_619_370, "endpoint first moment")
    require(second == 1_411_089_367_885_678, "endpoint second moment")
    require(
        G_MAX * first - second == 42_141_355_115_121_962,
        "endpoint cross moment",
    )
    require(
        sha256_json(histogram) == ENDPOINT_HISTOGRAM_SHA256,
        "endpoint histogram digest",
    )

    cumulative = 0
    for deficit, count in enumerate(histogram):
        require(count >= 0, "histogram nonnegative")
        cumulative += count
        if deficit <= cutoff:
            require(
                cumulative == one_pivot_cap(G_MAX, deficit),
                "H marginal saturated",
            )
            require(
                cumulative <= affine_span_cap(G_MAX, deficit),
                "predecessor affine head respected",
            )
    require(cumulative == L, "histogram cumulative total")

    full_six_factor = falling(W + 6, 6)
    cross_extension = comb(W + 5, 5)
    affine_line_extension = comb(W + 6, 5)
    inequalities = {
        "first_pivot": (
            L * G_MAX * full_six_factor,
            falling(R + G_MAX, 7),
        ),
        "colored_E": (
            (G_MAX * L - first) * full_six_factor,
            R * falling(R + G_MAX - 1, 6),
        ),
        "colored_S": (
            first * full_six_factor,
            G_MAX * falling(R + G_MAX - 1, 6),
        ),
        "cross_block": (
            (G_MAX * first - second) * cross_extension,
            G_MAX * R * comb(R + G_MAX - 2, 5),
        ),
        "affine_line": (
            L * G_MAX * affine_line_extension,
            15 * (R + G_MAX) * comb(R + G_MAX - 1, 5),
        ),
    }
    resource_records: dict[str, Any] = {}
    for name, (lhs, rhs) in inequalities.items():
        require(lhs <= rhs, f"endpoint {name} feasible")
        resource_records[name] = {
            "lhs": lhs,
            "rhs": rhs,
            "margin": rhs - lhs,
            "utilization_parts_per_billion": lhs * 10**9 // rhs,
        }

    q6_cap, q6_winner, q6_raw = q6_envelope(G_MAX)
    d6 = D6_MIN + q6_cap
    layer = R + G_MAX - d6
    pi_zero = pi_profile(d6, 0)
    pi_layer = pi_profile(d6, layer)
    t_capacity = layer * falling(d6, 6)
    u_capacity = falling(d6, 7)
    t_cost_zero = layer * pi_zero
    u_cost_zero = (Q_PROFILE - layer) * pi_zero
    u_cost_layer = Q_PROFILE * pi_layer
    high = min(L, t_capacity // t_cost_zero)
    low = max(
        0,
        ceil_div(
            L * u_cost_layer - u_capacity,
            u_cost_layer - u_cost_zero,
        ),
    )
    require((low, high) == (10_411_669, 10_411_790), "harmonic interval")
    transport = joint_q_b_transport(histogram, low, G_MAX, layer)
    transport_digest = sha256_json(transport)
    require(transport_digest == ENDPOINT_TRANSPORT_SHA256, "transport digest")
    split_rows = [
        row for row in transport if row[1] > 0 and row[2] > 0
    ]
    require(split_rows == [[11_539, 202, 946]], "unique split transport row")
    minimum_b_zero_margin = min(
        G_MAX - row[0] - layer for row in transport if row[1] > 0
    )
    minimum_b_layer_margin = min(
        R - layer - (G_MAX - row[0])
        for row in transport
        if row[2] > 0
    )
    require(minimum_b_zero_margin == 277_918, "active b=0 margin")
    require(minimum_b_layer_margin == 572_181, "active b=e margin")

    return {
        "g": G_MAX,
        "construction": (
            "s=0, q=delta; h_0=H_0; h_j=H_j-H_{j-1}; "
            "h_{Q_star+1}=L-H_{Q_star}"
        ),
        "cutoff": cutoff,
        "H_0": one_pivot_cap(G_MAX, 0),
        "H_2463": one_pivot_cap(G_MAX, 2_463),
        "H_cutoff_minus_one": one_pivot_cap(G_MAX, cutoff - 1),
        "H_cutoff": one_pivot_cap(G_MAX, cutoff),
        "H_cutoff_plus_one": one_pivot_cap(G_MAX, cutoff + 1),
        "forced_tail_at_2464": L - one_pivot_cap(G_MAX, 2_463),
        "forced_tail_at_cutoff_plus_one": histogram[-1],
        "tail_closure_upper": histogram[-1] - 1,
        "histogram_rows": len(histogram),
        "histogram_sha256": sha256_json(histogram),
        "first_moment": first,
        "second_moment": second,
        "cross_moment": G_MAX * first - second,
        "scalar_resources": resource_records,
        "scalar_resources_sha256": sha256_json(resource_records),
        "harmonic": {
            "q6_cap": q6_cap,
            "q6_winner": q6_winner,
            "q6_raw": q6_raw,
            "d6": d6,
            "layer": layer,
            "low": low,
            "high": high,
            "integer_width": high - low + 1,
            "b_zero_total": low,
            "b_layer_total": L - low,
            "transport_rows": len(transport),
            "transport_sha256": transport_digest,
            "unique_split_row": split_rows[0],
            "minimum_b_zero_placement_margin": minimum_b_zero_margin,
            "minimum_b_layer_placement_margin": minimum_b_layer_margin,
        },
        "scope": (
            "EXACT_INTEGER_H_Q_AND_SCALAR_HARMONIC_MARGINAL_RELAXATION; "
            "NO_COMMON_SUPPORT_OR_SOURCE_REALIZATION"
        ),
    }


def module_profile(degree_bound: int) -> dict[str, int]:
    require(degree_bound >= 0, "module degree nonnegative")
    quotient, remainder = divmod(degree_bound, MODULE_DEGREE)
    dimension = (
        remainder * (quotient + 1)
        + (MODULE_DEGREE - remainder) * quotient
    )
    require(dimension == degree_bound, "module dimension identity")
    return {
        "degree_bound": degree_bound,
        "quotient": quotient,
        "remainder": remainder,
        "high_channels": remainder,
        "low_channels": MODULE_DEGREE - remainder,
    }


def balanced_layout(total: int, blocks: int) -> dict[str, int]:
    base, raised = divmod(total, blocks)
    require(base * blocks + raised == total, "balanced layout identity")
    return {
        "total": total,
        "blocks": blocks,
        "base_occupancy": base,
        "raised_blocks": raised,
        "raised_occupancy": base + 1,
    }


def structural_route_cut() -> dict[str, Any]:
    message_dimension = G_MAX - W
    old_tail_delta = 2_464
    old_tail_h = G_MAX - old_tail_delta
    new_tail_delta = 15_187
    new_tail_h = G_MAX - new_tail_delta

    require(message_dimension == 287_525, "endpoint message dimension")
    require(old_tail_h == 352_508, "old effective tail H degree")
    require(new_tail_h == 339_785, "new effective tail H degree")
    require(old_tail_h - message_dimension == 64_983, "old moderate gap")
    require(new_tail_h - message_dimension == 52_260, "new moderate gap")

    a32 = balanced_layout(A, N // 32)
    r32 = balanced_layout(R, N // 32)
    h32 = balanced_layout(old_tail_h, N // 32)
    a2048 = balanced_layout(A, N // MODULE_DEGREE)
    r2048 = balanced_layout(R, N // MODULE_DEGREE)
    h2048 = balanced_layout(old_tail_h, N // MODULE_DEGREE)

    require(
        (a32["base_occupancy"], a32["raised_blocks"])
        == (17, 1_911),
        "A 32-block layout",
    )
    require(
        (r32["base_occupancy"], r32["raised_blocks"])
        == (14, 63_625),
        "R 32-block layout",
    )
    require(
        (h32["base_occupancy"], h32["raised_blocks"])
        == (5, 24_828),
        "H 32-block layout",
    )
    require(
        (a2048["base_occupancy"], a2048["raised_blocks"])
        == (1_089, 887),
        "A 2048-block layout",
    )
    require(
        (r2048["base_occupancy"], r2048["raised_blocks"])
        == (958, 137),
        "R 2048-block layout",
    )
    require(
        (h2048["base_occupancy"], h2048["raised_blocks"])
        == (344, 252),
        "H 2048-block layout",
    )
    require(h32["raised_occupancy"] < 14, "H fits every 32-block L0 slice")
    require(
        h2048["raised_occupancy"] < 958,
        "H fits every 2048-block L0 slice",
    )

    return {
        "effective_deficit_identity": "delta=q-s=g-deg(H)",
        "fixed_H_divisibility_fiber": {
            "moderate": (
                "delta<=w: empty or singleton, with f=rem_H(Y) "
                "when deg(rem_H(Y))<d"
            ),
            "deep": (
                "delta>w: divisibility fiber is "
                "f0 + (W intersect H*F[X]_{<delta-w})"
            ),
            "deep_affine_dimension_upper": "min(7,delta-w)",
            "exact_gcd_warning": (
                "The exact-gcd source fiber is a subset of the affine "
                "divisibility fiber; it need not itself be affine."
            ),
        },
        "endpoint_degrees": {
            "d": message_dimension,
            "old_C_frontier_delta": old_tail_delta,
            "old_C_frontier_H_max": old_tail_h,
            "old_C_frontier_H_minus_d": old_tail_h - message_dimension,
            "new_H_frontier_delta": new_tail_delta,
            "new_H_frontier_H_max": new_tail_h,
            "new_H_frontier_H_minus_d": new_tail_h - message_dimension,
        },
        "c2048_profiles": {
            "d": module_profile(message_dimension),
            "old_C_frontier_H_max": module_profile(old_tail_h),
            "new_H_frontier_H_max": module_profile(new_tail_h),
        },
        "balanced_boundary_layouts": {
            "block_size_32": {"A0": a32, "L0": r32, "H": h32},
            "block_size_2048": {
                "A0": a2048,
                "L0": r2048,
                "H": h2048,
            },
            "consequence": (
                "Boundary cardinalities and H-degree bounds alone do not "
                "force one complete 32- or 2048-point fiber."
            ),
            "nonclaim": (
                "This is a support-layout falsifier of an automatic domain "
                "adapter, not a source-compatible prefix/full-gcd family."
            ),
        },
        "nonintegrated_pr1073_quantifier_cut": {
            "head": "c2d901ebe405d11330d07777ec8926a733c81829",
            "local_cap": 3_432,
            "fixed_keys": [
                "pinned (u,v)=(0,1) quotient profile",
                "fixed canonical T32 remainder",
                "fixed depth-32 locator-prefix target",
            ],
            "missing_keys": [
                "source adapter from arbitrary H|L0",
                "cross-remainder aggregation",
                "cross-cofactor aggregation",
                "arbitrary boundary-profile and unit-V control",
            ],
            "dependency": False,
        },
    }


def fixed_g_consequence() -> dict[str, Any]:
    h_before = one_pivot_cap(217_542, 0)
    h_after = one_pivot_cap(217_543, 0)
    require(h_before == 15_775_952, "fixed-G pretransition cap")
    require(h_after == 15_775_767, "fixed-G transition cap")
    require(h_before > TARGET and h_after <= TARGET, "fixed-G crossing")
    for union_size in range(FIXED_G_NEW_TRANSITION, G_MAX + 1):
        require(one_pivot_cap(union_size, 0) <= TARGET, "fixed-G upper paid")

    residual_start = FIXED_G_LAST_PREPAID + 1
    residual_end = FIXED_G_NEW_TRANSITION - 1
    require(residual_end - residual_start + 1 == 144_683, "fixed-G open count")
    return {
        "scope": (
            "PURE_FULL_G_ZERO_ANCHORED_LINEAR_RANK_AT_MOST_SEVEN_ONLY"
        ),
        "reason": "pure full-G has q=0 and hence delta=-s<=0",
        "H_0_at_217542": h_before,
        "H_0_at_217543": h_after,
        "new_paid_interval": [FIXED_G_NEW_TRANSITION, G_MAX],
        "predecessor_paid_interval": [G_MIN, FIXED_G_LAST_PREPAID],
        "remaining_interval": [residual_start, residual_end],
        "remaining_g_cells": residual_end - residual_start + 1,
        "rank8_warning": (
            "No rank-eight-or-higher fixed-G payment is claimed."
        ),
    }


def one_pivot_theorem_record() -> dict[str, Any]:
    return {
        "ambient_statement": (
            "|L|<=floor((N-z)/m * "
            "floor(C(N-d+k-1,k-1)/C(v+z+k-1,k-1)))"
        ),
        "hypotheses": [
            "W is a k-dimensional linear subspace of RS(E,d)",
            "the received table is nowhere zero on E",
            "m=d+v and 1<=d<=m<=N-z",
            "z is the common-zero count of W",
            "k>=1; the k=0 list is empty for m>0",
        ],
        "floor_order": (
            "inner=numerator//denominator; "
            "bound=(N-z)*inner//m"
        ),
        "effective_deficit": "delta_i=q_i-s_i=g-deg(H_i)",
        "specialized_bound": (
            "N_delta(<=Q)<=H_Q(g)=floor(R/(g-Q)*"
            "floor(C(R-g+w+6,6)/C(w-Q+6,6)))"
        ),
        "rank_monotonicity": (
            "After weakening z to zero, the raw inner cap is "
            "nondecreasing for k<=7 because R-(g-w)>=w-Q."
        ),
        "negative_Q": (
            "Negative Q is legal for delta-heads, not q-heads; "
            "Q>=g-R keeps g-Q<=R."
        ),
    }


def build_summary() -> dict[str, Any]:
    frontier = scan_frontier()
    endpoint = endpoint_relaxation()
    fixed_g = fixed_g_consequence()
    structural = structural_route_cut()

    summary: dict[str, Any] = {
        "schema": SCHEMA_ID,
        "theorem_id": THEOREM_ID,
        "architecture": ARCHITECTURE_ID,
        "status": STATUS,
        "parent_payload_sha256": PARENT_PAYLOAD,
        "checks": CHECKS,
        "row": {
            "field_prime": FIELD_PRIME,
            "n": N,
            "K": K,
            "a": A,
            "R": R,
            "w": W,
            "B_star": B_STAR,
            "deep_cap": DEEP_CAP,
            "shallow_forbidden_size": L,
            "shallow_target": TARGET,
            "residual_g_range": [G_MIN, G_MAX],
            "rank": RANK,
        },
        "one_pivot_theorem": one_pivot_theorem_record(),
        "frontier_scan": frontier,
        "fixed_g_rank7_consequence": fixed_g,
        "endpoint_relaxation": endpoint,
        "structural_route_cut": structural,
        "missing_theorem": {
            "name": (
                "CROSS_COFACTOR_INTERLACED_H_AND_DEEP_FIBER_INCIDENCE"
            ),
            "input": (
                "One rank-at-most-seven W subset F_p[X]_{<g-w}, "
                "arbitrary split P|A0, unit V mod L0, exact H_i="
                "gcd(L0,Y-f_i), and all cumulative C_Q/H_Q bounds."
            ),
            "terminal": (
                "Either pay the combined effective-deficit tail uniformly, "
                "route it to an existing invariant quotient owner through "
                "a proved source adapter, or emit a source-compatible "
                "primitive family."
            ),
            "fixed_G_subterminal": (
                "Deterministic rank-at-most-seven ordinary-RS list theorem "
                "for 72860<=g<=217542."
            ),
            "deep_subterminal": (
                "Uniformly control the delta>w fixed-H divisibility fibers "
                "and their aggregation across H."
            ),
        },
        "impact": {
            "new_green_one_pivot_theorem": True,
            "new_fixed_g_rank7_payment": [217_543, 354_972],
            "current_scalar_route_cut": True,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "rank7_closed": False,
            "rank8_and_above_closed": False,
            "row_closed": False,
        },
        "nonclaims": [
            "The endpoint histogram is not a source family.",
            "The q-b transport does not construct one common support layer.",
            "Fixed-H uniqueness does not bound the number of possible H.",
            "The deep exact-gcd fiber is not asserted to be affine.",
            "PR #1073 is not an owner or dependency of this packet.",
            "No complete 32- or 2048-point fiber is forced by cardinality.",
            "No v4 atom or official row value moves.",
        ],
    }
    summary["checks"] = CHECKS
    summary["payload_sha256"] = payload_sha256(summary)
    return summary


def validate_summary(summary: dict[str, Any]) -> None:
    require(summary["schema"] == SCHEMA_ID, "schema id")
    require(summary["theorem_id"] == THEOREM_ID, "theorem id")
    require(summary["architecture"] == ARCHITECTURE_ID, "architecture id")
    require(summary["status"] == STATUS, "status")
    require(summary["parent_payload_sha256"] == PARENT_PAYLOAD, "parent pin")
    require(summary["payload_sha256"] == payload_sha256(summary), "payload seal")
    require(summary["row"]["residual_g_range"] == [G_MIN, G_MAX], "row range")
    require(summary["frontier_scan"]["g_cells"] == 282_545, "frontier cells")
    require(
        summary["frontier_scan"]["interval_sha256"] == INTERVAL_SHA256,
        "frontier digest",
    )
    require(
        summary["frontier_scan"]["cutoff_range"] == [-23_382, 15_186],
        "frontier cutoff range",
    )
    require(
        summary["fixed_g_rank7_consequence"]["remaining_interval"]
        == [72_860, 217_542],
        "fixed-G residual interval",
    )
    require(
        summary["endpoint_relaxation"]["histogram_sha256"]
        == ENDPOINT_HISTOGRAM_SHA256,
        "endpoint histogram seal",
    )
    require(
        summary["endpoint_relaxation"]["harmonic"]["transport_sha256"]
        == ENDPOINT_TRANSPORT_SHA256,
        "endpoint transport seal",
    )
    resources = summary["endpoint_relaxation"]["scalar_resources"]
    require(
        set(resources)
        == {
            "first_pivot",
            "colored_E",
            "colored_S",
            "cross_block",
            "affine_line",
        },
        "scalar resource keys",
    )
    require(
        summary["endpoint_relaxation"]["scalar_resources_sha256"]
        == sha256_json(resources)
        == ENDPOINT_SCALAR_RESOURCES_SHA256,
        "scalar resource seal",
    )
    require(
        summary["endpoint_relaxation"]["harmonic"]
        == {
            "q6_cap": 222_004,
            "q6_winner": 5,
            "q6_raw": 222_004,
            "d6": 1_270_586,
            "layer": 65_515,
            "low": 10_411_669,
            "high": 10_411_790,
            "integer_width": 122,
            "b_zero_total": 10_411_669,
            "b_layer_total": 5_364_264,
            "transport_rows": 15_188,
            "transport_sha256": ENDPOINT_TRANSPORT_SHA256,
            "unique_split_row": [11_539, 202, 946],
            "minimum_b_zero_placement_margin": 277_918,
            "minimum_b_layer_placement_margin": 572_181,
        },
        "harmonic record",
    )
    require(
        summary["endpoint_relaxation"]["scope"]
        == (
            "EXACT_INTEGER_H_Q_AND_SCALAR_HARMONIC_MARGINAL_RELAXATION; "
            "NO_COMMON_SUPPORT_OR_SOURCE_REALIZATION"
        ),
        "endpoint nonrealization scope",
    )
    require(
        summary["structural_route_cut"]["balanced_boundary_layouts"][
            "block_size_2048"
        ]["H"]["raised_occupancy"]
        == 345,
        "interlaced H occupancy",
    )
    require(
        summary["structural_route_cut"]["balanced_boundary_layouts"][
            "nonclaim"
        ]
        == (
            "This is a support-layout falsifier of an automatic domain "
            "adapter, not a source-compatible prefix/full-gcd family."
        ),
        "layout nonclaim",
    )
    require(
        summary["nonclaims"]
        == [
            "The endpoint histogram is not a source family.",
            "The q-b transport does not construct one common support layer.",
            "Fixed-H uniqueness does not bound the number of possible H.",
            "The deep exact-gcd fiber is not asserted to be affine.",
            "PR #1073 is not an owner or dependency of this packet.",
            "No complete 32- or 2048-point fiber is forced by cardinality.",
            "No v4 atom or official row value moves.",
        ],
        "critical nonclaims",
    )
    require(
        summary["one_pivot_theorem"]["floor_order"]
        == "inner=numerator//denominator; bound=(N-z)*inner//m",
        "nested floor order",
    )
    require(
        summary["one_pivot_theorem"]["specialized_bound"]
        == (
            "N_delta(<=Q)<=H_Q(g)=floor(R/(g-Q)*"
            "floor(C(R-g+w+6,6)/C(w-Q+6,6)))"
        ),
        "specialized one-pivot bound",
    )
    require(
        summary["one_pivot_theorem"] == one_pivot_theorem_record(),
        "complete one-pivot theorem record",
    )
    require(
        summary["impact"]
        == {
            "new_green_one_pivot_theorem": True,
            "new_fixed_g_rank7_payment": [217_543, 354_972],
            "current_scalar_route_cut": True,
            "ledger_movement": 0,
            "official_endpoint_movement": 0,
            "rank7_closed": False,
            "rank8_and_above_closed": False,
            "row_closed": False,
        },
        "honest impact",
    )
    require(
        summary["missing_theorem"]["name"]
        == "CROSS_COFACTOR_INTERLACED_H_AND_DEEP_FIBER_INCIDENCE",
        "complete missing theorem name",
    )


def set_path(payload: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
    target: Any = payload
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    payload["payload_sha256"] = payload_sha256(payload)


def tamper_selftest() -> dict[str, Any]:
    baseline = build_summary()
    mutations: list[tuple[tuple[str, ...], Any]] = [
        (("schema",), SCHEMA_ID + "-tampered"),
        (("theorem_id",), THEOREM_ID + "_TAMPERED"),
        (("architecture",), ARCHITECTURE_ID + "_TAMPERED"),
        (("status",), "ROW_CLOSED"),
        (("parent_payload_sha256",), "0" * 64),
        (("row", "residual_g_range"), [G_MIN, G_MAX + 1]),
        (("frontier_scan", "g_cells"), 282_544),
        (("frontier_scan", "interval_sha256"), "1" * 64),
        (("frontier_scan", "cutoff_range"), [-23_381, 15_186]),
        (
            ("fixed_g_rank7_consequence", "remaining_interval"),
            [72_860, 217_541],
        ),
        (
            ("endpoint_relaxation", "histogram_sha256"),
            "2" * 64,
        ),
        (
            ("endpoint_relaxation", "harmonic", "transport_sha256"),
            "3" * 64,
        ),
        (
            ("endpoint_relaxation", "scalar_resources"),
            {},
        ),
        (
            ("endpoint_relaxation", "harmonic", "q6_cap"),
            0,
        ),
        (
            ("endpoint_relaxation", "scope"),
            "SOURCE_REALIZATION_AND_ROW_CLOSURE",
        ),
        (
            (
                "structural_route_cut",
                "balanced_boundary_layouts",
                "block_size_2048",
                "H",
                "raised_occupancy",
            ),
            346,
        ),
        (
            (
                "structural_route_cut",
                "balanced_boundary_layouts",
                "nonclaim",
            ),
            "This is a source-compatible counterexample.",
        ),
        (
            ("nonclaims",),
            ["The endpoint histogram is a source family."],
        ),
        (
            ("one_pivot_theorem", "floor_order"),
            "MERGE_THE_FLOORS",
        ),
        (
            ("one_pivot_theorem", "specialized_bound"),
            "N_delta(<=Q)<=B_star",
        ),
        (
            ("one_pivot_theorem", "ambient_statement"),
            "THE BOUND HOLDS WITHOUT HYPOTHESES",
        ),
        (
            ("one_pivot_theorem", "hypotheses"),
            ["the received table may vanish"],
        ),
        (
            ("one_pivot_theorem", "effective_deficit"),
            "delta_i=q_i+s_i",
        ),
        (("impact", "ledger_movement"), 1),
        (("impact", "rank7_closed"), True),
        (("impact", "rank8_and_above_closed"), True),
        (("impact", "row_closed"), True),
        (
            ("missing_theorem", "name"),
            "CROSS_H_ONLY_INCIDENCE",
        ),
    ]
    detected = 0
    for path, value in mutations:
        candidate = copy.deepcopy(baseline)
        set_path(candidate, path, value)
        try:
            validate_summary(candidate)
        except (KeyError, TypeError, VerificationError):
            detected += 1
    require(detected == len(mutations), "all primary mutations detected")
    result = {
        "schema": "m31-rank7-effective-deficit-one-pivot-tamper-v1",
        "mutations": len(mutations),
        "detected": detected,
        "all_detected": detected == len(mutations),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.check:
        summary = build_summary()
        validate_summary(summary)
        sys.stdout.buffer.write(canonical_json(summary))
        return 0
    result = tamper_selftest()
    sys.stdout.buffer.write(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
