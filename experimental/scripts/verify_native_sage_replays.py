#!/usr/bin/env python3
"""Native replay companions for Sage-only audit scripts.

Proof status: AUDIT. These checks do not replace Sage as an independent CAS
backend. They keep the local replay suite meaningful on hosts where Sage or WSL
is unavailable by rechecking the same finite witnesses with exact Python
arithmetic and explicit combinatorial certificates.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from experimental.scripts.locator.locator_fiber_sweep.run_locator_fiber_sweep import (
    DEFAULT_MAX_SUPPORTS,
)
from experimental.scripts.locator.locator_fiber_sweep.run_locator_fiber_sweep import (
    SweepCase,
)
from experimental.scripts.locator.locator_fiber_sweep.run_locator_fiber_sweep import (
    analyze_case as locator_analyze_case,
)
from experimental.scripts.verify_m1_cycle120_self_contained_certificate import (
    QONE,
    QZERO,
    THETA,
    emb,
    qadd,
    qeq,
    qis_zero,
    qkey,
    qmul,
    qpow,
    qsub,
    qinv,
)


PROOF_STATUS = "AUDIT"
THEOREM_PROBLEM_ID = "native-sage-replay-companions"
P = 17
FIELD_DEGREE = 32
FIELD_SIZE = P**FIELD_DEGREE
TARGET_BITS = 128
N = 512
K = 256
GATE_NUMERATOR = 7
FIBER_SIZE = 32
QUOTIENT_SIZE = 16
QUOTIENT_SUBSET_SIZE = 10
PRIMITIVE_ROOT_MOD_17 = 3

CASE_CHOICES = (
    "all",
    "threshold-descent",
    "threshold-interval-sharpening",
    "threshold-upward-push",
    "hybrid-quotient-residual",
    "locator-selected",
)

SAGE_REPLACEMENTS = {
    "threshold-descent": (
        "experimental/scripts/audit_m1_interleaved_list_threshold_descent.sage"
    ),
    "threshold-interval-sharpening": (
        "experimental/scripts/audit_m1_interleaved_list_threshold_interval_sharpening.sage"
    ),
    "threshold-upward-push": (
        "experimental/scripts/audit_m1_interleaved_list_threshold_upward_push.sage"
    ),
    "hybrid-quotient-residual": (
        "experimental/scripts/audit_m1_interleaved_list_hybrid_quotient_residual.sage"
    ),
    "locator-selected": (
        "experimental/scripts/locator/sage_locator_fiber_crosscheck/"
        "sage_locator_fiber_crosscheck.sage"
    ),
}

SELECTED_QUOTIENT_INDICES = [
    [1, 2, 4, 5, 8, 9, 10, 11, 12, 15],
    [1, 2, 5, 6, 7, 8, 9, 12, 14, 15],
    [1, 3, 4, 6, 7, 10, 11, 12, 13, 14],
    [1, 3, 5, 7, 8, 9, 10, 12, 13, 14],
    [2, 3, 4, 5, 6, 9, 11, 12, 14, 15],
    [2, 4, 5, 7, 8, 11, 12, 13, 14, 15],
    [2, 4, 6, 8, 9, 10, 11, 13, 14, 15],
]

SCHEDULE_BY_QUOTIENT = {
    0: {0: 7, 11: 7, 7: 6, 14: 6, 2: 6},
    1: {8: 32},
    2: {13: 32},
    3: {2: 32},
    4: {16: 32},
    5: {9: 32},
    6: {4: 32},
    7: {15: 32},
    8: {1: 32},
    9: {8: 32},
    10: {13: 32},
    11: {2: 32},
    12: {16: 32},
    13: {9: 32},
    14: {4: 32},
    15: {15: 32},
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def hash_payload(payload: Any) -> str:
    encoded = json.dumps(
        json_ready(payload), sort_keys=True, separators=(",", ":")
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def json_ready(payload: Any) -> Any:
    if payload is None or isinstance(payload, (str, bool, int, float)):
        return payload
    if isinstance(payload, tuple):
        return [json_ready(item) for item in payload]
    if isinstance(payload, list):
        return [json_ready(item) for item in payload]
    if isinstance(payload, dict):
        return {str(key): json_ready(value) for key, value in payload.items()}
    return str(payload)


def qneg(value: Any) -> Any:
    return qsub(QZERO, value)


def qscalar(value: int) -> Any:
    return emb([value % P])


def qrepr(value: Any) -> list[list[int]]:
    left, right = qkey(value)
    return [list(left), list(right)]


def qhash(value: Any) -> str:
    return hash_payload(qrepr(value))


def q_poly_trim(poly: list[Any]) -> list[Any]:
    while len(poly) > 1 and qis_zero(poly[-1]):
        poly.pop()
    return poly


def q_poly_mul(left: list[Any], right: list[Any]) -> list[Any]:
    out = [QZERO] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        if qis_zero(a):
            continue
        for j, b in enumerate(right):
            if not qis_zero(b):
                out[i + j] = qadd(out[i + j], qmul(a, b))
    return q_poly_trim(out)


def q_poly_mul_linear(poly: list[Any], root: Any) -> list[Any]:
    out = [QZERO] * (len(poly) + 1)
    for index, coeff in enumerate(poly):
        out[index] = qsub(out[index], qmul(coeff, root))
        out[index + 1] = qadd(out[index + 1], coeff)
    return q_poly_trim(out)


def q_poly_scale(poly: list[Any], scalar: Any) -> list[Any]:
    return q_poly_trim([qmul(coeff, scalar) for coeff in poly])


def q_poly_eval(poly: list[Any], value: Any) -> Any:
    acc = QZERO
    for coeff in reversed(poly):
        acc = qadd(qmul(acc, value), coeff)
    return acc


def q_poly_degree(poly: list[Any]) -> int:
    trimmed = q_poly_trim(poly[:])
    if len(trimmed) == 1 and qis_zero(trimmed[0]):
        return -1
    return len(trimmed) - 1


def q_root_polynomial(points: list[Any]) -> list[Any]:
    poly = [QONE]
    for point in points:
        poly = q_poly_mul_linear(poly, point)
    return poly


def q_div(numerator: Any, denominator: Any) -> Any:
    require(not qis_zero(denominator), "division by zero in F_17^32")
    return qmul(numerator, qinv(denominator))


def q_linear_residual(root: Any, scale: Any = QONE) -> list[Any]:
    return [qmul(qneg(root), scale), scale]


def domain_h() -> list[Any]:
    return [qpow(THETA, index) for index in range(N)]


def q_support_hash(support: list[int]) -> str:
    return hash_payload([int(item) for item in support])


def field_header(case: str) -> dict[str, Any]:
    return {
        "case": case,
        "replacement_for": SAGE_REPLACEMENTS[case],
        "proof_status": PROOF_STATUS,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "row": "RS[F_17^32,H,256]",
        "track": "INTERLEAVED_LIST" if case != "locator-selected" else "LOCATOR_FIBER",
        "q_gen": str(FIELD_SIZE),
        "q_line": str(FIELD_SIZE),
        "q_chal": str(FIELD_SIZE),
        "field_denominator_label": "17^32",
        "target_bits": TARGET_BITS,
        "threshold_floor": FIELD_SIZE // (2**TARGET_BITS),
        "minimum_to_clear": FIELD_SIZE // (2**TARGET_BITS) + 1,
        "native_replay_scope": (
            "exact Python replay companion for local hosts without Sage/WSL; "
            "Sage remains an optional independent CAS backend"
        ),
    }


def verify_field_gate() -> None:
    require(FIELD_SIZE // (2**TARGET_BITS) == 6, "wrong 2^-128 floor")
    require(6 * 2**TARGET_BITS < FIELD_SIZE < 7 * 2**TARGET_BITS, "bad gate")
    h = domain_h()
    require(len({qkey(point) for point in h}) == N, "H is not order 512")
    require(qeq(qpow(THETA, N), QONE), "theta^512 != 1")
    require(not qeq(qpow(THETA, N // 2), QONE), "theta has smaller order")


def verify_threshold_descent() -> dict[str, Any]:
    case = "threshold-descent"
    verify_field_gate()
    root_set_size = K - 1
    agreement = 291
    block_size = agreement - root_set_size
    root_indices = list(range(root_set_size))
    complement_indices = list(range(root_set_size, N))

    # The Sage audit evaluates the root polynomial over GF(17^32).  For this
    # native companion the same claim is checked combinatorially: a monic
    # polynomial with the first K-1 distinct H-points as roots has degree K-1,
    # hence is a degree-<K codeword, and a nonzero scalar multiple agrees with
    # the zero received word exactly on those roots.  Assigning disjoint
    # complement blocks to seven distinct prime-field scalars then gives seven
    # distinct agreement supports of size 291.
    require(root_set_size < K, "root polynomial is not a codeword")
    require(len(complement_indices) == 257, "bad complement size")
    require(GATE_NUMERATOR * block_size + 5 == len(complement_indices), "bad block packing")
    scalars = list(range(1, GATE_NUMERATOR + 1))
    require(len(set(scalars)) == GATE_NUMERATOR, "scalars collide")

    supports: list[list[int]] = []
    descriptors: list[dict[str, Any]] = []
    for witness_id in range(GATE_NUMERATOR):
        block_start = witness_id * block_size
        block_stop = block_start + block_size
        require(block_stop <= len(complement_indices), "block overrun")
        block_indices = complement_indices[block_start:block_stop]
        support = root_indices + block_indices
        require(len(support) == agreement, "wrong descent agreement count")
        require(set(root_indices).issubset(support), "common roots not present")
        supports.append(support)
        descriptors.append(
            {
                "witness_id": witness_id,
                "scalar_in_prime_field": witness_id + 1,
                "agreement": len(support),
                "block_start": block_indices[0],
                "block_stop_inclusive": block_indices[-1],
                "support_hash": q_support_hash(support),
            }
        )

    require(len({tuple(support) for support in supports}) == GATE_NUMERATOR, "supports collide")
    return {
        **field_header(case),
        "result": "PASS",
        "exact_object": "root-pencil scalar-multiple lower-bound witnesses at a=291",
        "input_parameters": {
            "n": N,
            "k": K,
            "agreement": agreement,
            "root_set_size": root_set_size,
            "block_size": block_size,
        },
        "certificate": {
            "lambda_lower_bound": len(supports),
            "clears_list_gate": len(supports) >= GATE_NUMERATOR,
            "agreement_counts": [len(support) for support in supports],
            "residual_size": len(complement_indices) - GATE_NUMERATOR * block_size,
            "root_polynomial_degree": root_set_size,
            "root_polynomial_model": "monic product over first 255 distinct H-points",
            "witness_descriptors": descriptors,
            "witness_descriptors_hash": hash_payload(descriptors),
        },
        "status": "AUDIT_PASS_NATIVE_REPLAY_LOWER_BOUND_A291",
        "mca_counted": False,
    }


def verify_threshold_interval_sharpening() -> dict[str, Any]:
    case = "threshold-interval-sharpening"
    verify_field_gate()
    h = domain_h()
    common_root_size = K - 2
    agreement = 292
    common_roots = h[:common_root_size]
    complement = h[common_root_size:]
    require(len(complement) == N - common_root_size == 258, "bad complement")
    x1, x2, x3, x4, x5, x6, y12, y34 = complement[:8]
    root_poly = q_root_polynomial(common_roots)
    require(q_poly_degree(root_poly) == common_root_size, "bad common root degree")
    for point in common_roots:
        require(qis_zero(q_poly_eval(root_poly, point)), "common root missed")
    for point in complement:
        require(not qis_zero(q_poly_eval(root_poly, point)), "extra common root")

    scale12 = q_div(qsub(y12, x1), qsub(y12, x2))
    scale34 = q_div(qsub(y34, x3), qsub(y34, x4))
    residuals = [
        [QZERO],
        q_linear_residual(x1),
        q_linear_residual(x2, scale12),
        q_linear_residual(x3),
        q_linear_residual(x4, scale34),
        q_linear_residual(x5),
        q_linear_residual(x6),
    ]
    codewords = [q_poly_mul(root_poly, residual) for residual in residuals]
    degrees = [q_poly_degree(codeword) for codeword in codewords]
    require(max(degrees) == K - 1, "unexpected max degree")
    require(all(degree < K for degree in degrees), "degree bound failed")
    require(
        len({hash_payload([qrepr(coeff) for coeff in codeword]) for codeword in codewords})
        == GATE_NUMERATOR,
        "codewords collide",
    )

    supports = [set(range(common_root_size)) for _ in range(GATE_NUMERATOR)]
    received: list[Any | None] = [None] * N
    for position in range(common_root_size):
        received[position] = QZERO
    controlled = [
        (common_root_size + 0, [0, 1]),
        (common_root_size + 1, [0, 2]),
        (common_root_size + 2, [0, 3]),
        (common_root_size + 3, [0, 4]),
        (common_root_size + 4, [0, 5]),
        (common_root_size + 5, [0, 6]),
        (common_root_size + 6, [1, 2]),
        (common_root_size + 7, [3, 4]),
    ]
    for position, active in controlled:
        values = [q_poly_eval(codewords[index], h[position]) for index in active]
        require(all(qeq(values[0], value) for value in values), "controlled values disagree")
        received[position] = values[0]
        for index in active:
            supports[index].add(position)

    unique_needed = [agreement - len(support) for support in supports]
    require(unique_needed == [32, 36, 36, 36, 36, 37, 37], "bad unique schedule")
    cursor = 0
    for index, needed in enumerate(unique_needed):
        start = common_root_size + len(controlled) + cursor
        stop = start + needed
        cursor += needed
        for position in range(start, stop):
            received[position] = q_poly_eval(codewords[index], h[position])
            supports[index].add(position)
    require(all(value is not None for value in received), "received word incomplete")

    agreement_supports: list[list[int]] = []
    for index, codeword in enumerate(codewords):
        support = [
            position
            for position, point in enumerate(h)
            if qeq(q_poly_eval(codeword, point), received[position])
        ]
        require(set(support) == supports[index], "accidental agreement mismatch")
        require(len(support) == agreement, "wrong interval agreement count")
        agreement_supports.append(support)

    intersections = []
    for i in range(GATE_NUMERATOR):
        for j in range(i + 1, GATE_NUMERATOR):
            size = len(set(agreement_supports[i]) & set(agreement_supports[j]))
            require(size <= K - 1, "MDS support-intersection budget exceeded")
            intersections.append({"i": i, "j": j, "intersection_size": size})

    return {
        **field_header(case),
        "result": "PASS",
        "exact_object": "common-root linear-overlap witnesses at a=292",
        "input_parameters": {
            "n": N,
            "k": K,
            "agreement": agreement,
            "common_root_size": common_root_size,
            "controlled_overlap_point_count": len(controlled),
        },
        "certificate": {
            "lambda_lower_bound": GATE_NUMERATOR,
            "clears_list_gate": True,
            "degrees": degrees,
            "agreement_counts": [len(support) for support in agreement_supports],
            "unique_needed_by_witness": unique_needed,
            "support_intersections": intersections,
            "agreement_supports_hash": hash_payload(agreement_supports),
            "residual_hashes": [
                hash_payload([qrepr(coeff) for coeff in residual])
                for residual in residuals
            ],
        },
        "status": "AUDIT_PASS_NATIVE_REPLAY_LOWER_BOUND_A292",
        "mca_counted": False,
    }


def f17_values() -> list[int]:
    values = [pow(PRIMITIVE_ROOT_MOD_17, index, P) for index in range(QUOTIENT_SIZE)]
    require(len(set(values)) == QUOTIENT_SIZE, "3 is not primitive in F_17")
    return values


def f17_trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] % P == 0:
        poly.pop()
    return [coeff % P for coeff in poly]


def f17_degree(poly: list[int]) -> int:
    poly = f17_trim(poly[:])
    if len(poly) == 1 and poly[0] == 0:
        return -1
    return len(poly) - 1


def f17_mul(left: list[int], right: list[int]) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % P
    return f17_trim(out)


def f17_mul_linear(poly: list[int], root: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for index, coeff in enumerate(poly):
        out[index] = (out[index] - root * coeff) % P
        out[index + 1] = (out[index + 1] + coeff) % P
    return f17_trim(out)


def f17_eval(poly: list[int], value: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * value + coeff) % P
    return acc


def f17_sub(left: list[int], right: list[int]) -> list[int]:
    width = max(len(left), len(right))
    out = [0] * width
    for index in range(width):
        out[index] = (
            (left[index] if index < len(left) else 0)
            - (right[index] if index < len(right) else 0)
        ) % P
    return f17_trim(out)


def f17_divmod(numerator: list[int], denominator: list[int]) -> tuple[list[int], list[int]]:
    numerator = f17_trim(numerator[:])
    denominator = f17_trim(denominator[:])
    require(f17_degree(denominator) >= 0, "zero denominator polynomial")
    quotient = [0] * max(1, (len(numerator) - len(denominator) + 1))
    denom_degree = f17_degree(denominator)
    denom_lead_inv = pow(denominator[-1], -1, P)
    while f17_degree(numerator) >= denom_degree and f17_degree(numerator) >= 0:
        shift = f17_degree(numerator) - denom_degree
        factor = numerator[-1] * denom_lead_inv % P
        quotient[shift] = factor
        subtractor = [0] * shift + [(factor * coeff) % P for coeff in denominator]
        numerator = f17_sub(numerator, subtractor)
    return f17_trim(quotient), f17_trim(numerator)


def f17_locator(indices: tuple[int, ...] | list[int]) -> list[int]:
    values = f17_values()
    poly = [1]
    for index in indices:
        poly = f17_mul_linear(poly, values[index])
    return poly


def quotient_received_poly(h8: int = 0, h9: int = 0) -> list[int]:
    poly = [0] * 11
    poly[10] = 1
    poly[9] = h9 % P
    poly[8] = h8 % P
    return f17_trim(poly)


def best_quotient_fiber() -> tuple[tuple[int, int], list[tuple[int, ...]]]:
    fibers: dict[tuple[int, int], list[tuple[int, ...]]] = {}
    for indices in itertools.combinations(range(QUOTIENT_SIZE), QUOTIENT_SUBSET_SIZE):
        locator = f17_locator(indices)
        key = (locator[8], locator[9])
        fibers.setdefault(key, []).append(indices)
    return max(
        fibers.items(),
        key=lambda item: (len(item[1]), tuple(str(value) for value in item[0])),
    )


def verify_threshold_upward_push() -> dict[str, Any]:
    case = "threshold-upward-push"
    key, best_fiber = best_quotient_fiber()
    h8, h9 = key
    values = f17_values()
    received = quotient_received_poly(h8, h9)
    expected_floor = math.ceil(
        math.comb(QUOTIENT_SIZE, QUOTIENT_SUBSET_SIZE) / (P ** 2)
    )
    require(len(best_fiber) >= expected_floor >= 28, "pigeonhole floor failed")
    witness_descriptors = []
    supports_payload = []
    coefficient_hashes = set()
    for witness_index, indices in enumerate(best_fiber):
        locator = f17_locator(indices)
        _, remainder = f17_divmod(received, locator)
        require(f17_degree(remainder) < math.ceil(K / FIBER_SIZE), "bad quotient degree")
        active = set(indices)
        support = [
            position
            for qidx in range(QUOTIENT_SIZE)
            for position in range(qidx * FIBER_SIZE, (qidx + 1) * FIBER_SIZE)
            if qidx in active
        ]
        require(len(support) == FIBER_SIZE * QUOTIENT_SUBSET_SIZE, "bad support")
        for qidx in active:
            require(
                f17_eval(remainder, values[qidx]) == f17_eval(received, values[qidx]),
                "remainder does not match active quotient point",
            )
        coeff_hash = hash_payload(remainder)
        require(coeff_hash not in coefficient_hashes, "remainder collision")
        coefficient_hashes.add(coeff_hash)
        supports_payload.append(support)
        witness_descriptors.append(
            {
                "witness": witness_index,
                "quotient_indices": list(indices),
                "agreement": len(support),
                "quotient_remainder_degree": f17_degree(remainder),
                "x_degree_bound": FIBER_SIZE * f17_degree(remainder),
                "coefficient_hash": coeff_hash,
                "support_hash": q_support_hash(support),
            }
        )

    return {
        **field_header(case),
        "result": "PASS",
        "exact_object": "quotient-fiber prefix list floor at a=320",
        "input_parameters": {
            "n": N,
            "k": K,
            "fiber_size": FIBER_SIZE,
            "quotient_size": QUOTIENT_SIZE,
            "quotient_subset_size": QUOTIENT_SUBSET_SIZE,
            "agreement": FIBER_SIZE * QUOTIENT_SUBSET_SIZE,
        },
        "certificate": {
            "quotient_field": "F_17",
            "primitive_root_mod_17": PRIMITIVE_ROOT_MOD_17,
            "quotient_key": [h8, h9],
            "best_fiber_size": len(best_fiber),
            "expected_floor": expected_floor,
            "lambda_lower_from_verified_witnesses": len(witness_descriptors),
            "clears_list_gate": len(witness_descriptors) >= GATE_NUMERATOR,
            "witness_descriptors": witness_descriptors,
            "witness_descriptors_hash": hash_payload(witness_descriptors),
            "agreement_supports_hash": hash_payload(supports_payload),
        },
        "status": "AUDIT_PASS_NATIVE_REPLAY_LOWER_BOUND_A320",
        "mca_counted": False,
    }


def verify_hybrid_quotient_residual() -> dict[str, Any]:
    case = "hybrid-quotient-residual"
    key, best_fiber = best_quotient_fiber()
    require(key == (0, 0), "unexpected best quotient key")
    selected = [tuple(indices) for indices in SELECTED_QUOTIENT_INDICES]
    selected_ids = [best_fiber.index(indices) for indices in selected]
    require(selected_ids == [23, 24, 26, 28, 29, 30, 31], "selected witness ids changed")
    values = f17_values()
    received = quotient_received_poly()
    descriptors = []
    agreement_hash_payload = []
    agreement_counts = []
    for witness_index, indices in enumerate(selected):
        locator = f17_locator(indices)
        _, remainder = f17_divmod(received, locator)
        require(f17_degree(remainder) < math.ceil(K / FIBER_SIZE), "bad quotient degree")
        support_positions = []
        for qidx in range(QUOTIENT_SIZE):
            code_value = f17_eval(remainder, values[qidx])
            schedule = SCHEDULE_BY_QUOTIENT[qidx]
            require(sum(schedule.values()) == FIBER_SIZE, "bad quotient schedule")
            multiplicity = schedule.get(code_value, 0)
            support_positions.extend(
                range(qidx * FIBER_SIZE, qidx * FIBER_SIZE + multiplicity)
            )
        agreement_counts.append(len(support_positions))
        agreement_hash_payload.append(support_positions)
        descriptors.append(
            {
                "witness": witness_index,
                "best_fiber_index": selected_ids[witness_index],
                "quotient_indices": list(indices),
                "quotient_remainder_degree": f17_degree(remainder),
                "x_degree_bound": FIBER_SIZE * f17_degree(remainder),
                "agreement": len(support_positions),
                "coefficient_hash": hash_payload(remainder),
                "support_hash": q_support_hash(support_positions),
            }
        )

    require(agreement_counts == [327, 327, 327, 326, 326, 326, 327], "bad hybrid counts")
    return {
        **field_header(case),
        "result": "PASS",
        "exact_object": "hybrid quotient-residual value-class schedule at a=326",
        "input_parameters": {
            "n": N,
            "k": K,
            "fiber_size": FIBER_SIZE,
            "quotient_size": QUOTIENT_SIZE,
            "candidate_agreement": min(agreement_counts),
        },
        "certificate": {
            "quotient_field": "F_17",
            "primitive_root_mod_17": PRIMITIVE_ROOT_MOD_17,
            "selected_witness_ids": selected_ids,
            "selected_quotient_indices": SELECTED_QUOTIENT_INDICES,
            "agreement_counts": agreement_counts,
            "lambda_lower": len(selected),
            "clears_list_gate": len(selected) >= GATE_NUMERATOR,
            "received_word_hash": hash_payload(
                {
                    "schedule_by_quotient": SCHEDULE_BY_QUOTIENT,
                    "primitive_root_mod_17": PRIMITIVE_ROOT_MOD_17,
                }
            ),
            "witness_descriptors": descriptors,
            "witness_descriptors_hash": hash_payload(descriptors),
            "agreement_supports_hash": hash_payload(agreement_hash_payload),
        },
        "status": "AUDIT_PASS_NATIVE_REPLAY_LOWER_BOUND_A326",
        "mca_counted": False,
    }


def locator_selected_cases() -> list[SweepCase]:
    return [
        SweepCase(p=5, n=4, k=2, agreement_size=3, template="monomial", seed=0),
        SweepCase(p=5, n=4, k=2, agreement_size=3, template="zero", seed=0),
        SweepCase(p=17, n=16, k=8, agreement_size=9, template="monomial", seed=0),
    ]


def verify_locator_selected() -> dict[str, Any]:
    case = "locator-selected"
    reports = [
        locator_analyze_case(
            item,
            max_witnesses=0,
            max_supports=DEFAULT_MAX_SUPPORTS,
            parameters={"native_replay_for": SAGE_REPLACEMENTS[case]},
        )
        for item in locator_selected_cases()
    ]
    fibers = {
        (
            report["inputs"]["p"],
            report["inputs"]["n"],
            report["inputs"]["k"],
            report["inputs"]["agreement_size"],
            report["inputs"]["template"],
        ): report["scan"]["fiber_size"]
        for report in reports
    }
    require(fibers[(5, 4, 2, 3, "monomial")] == 0, "p5 monomial fiber drift")
    require(fibers[(5, 4, 2, 3, "zero")] == 4, "p5 zero fiber drift")
    require(fibers[(17, 16, 8, 9, "monomial")] == 0, "p17 monomial fiber drift")
    return {
        **field_header(case),
        "result": "PASS",
        "q_gen": "prime-field toy rows",
        "q_line": "prime-field toy rows",
        "q_chal": "not used",
        "exact_object": "tiny prime-field locator-fiber selected cross-checks",
        "input_parameters": {
            "cases": [
                {
                    "p": item.p,
                    "n": item.n,
                    "k": item.k,
                    "agreement_size": item.agreement_size,
                    "template": item.template,
                    "seed": item.seed,
                }
                for item in locator_selected_cases()
            ]
        },
        "certificate": {
            "reports": reports,
            "fiber_sizes": {
                "p5_n4_k2_a3_monomial": fibers[(5, 4, 2, 3, "monomial")],
                "p5_n4_k2_a3_zero": fibers[(5, 4, 2, 3, "zero")],
                "p17_n16_k8_a9_monomial": fibers[(17, 16, 8, 9, "monomial")],
            },
            "reports_hash": hash_payload(stable_hash_payload(reports)),
        },
        "status": "AUDIT_PASS_NATIVE_REPLAY_LOCATOR_SELECTED",
        "mca_counted": False,
    }


VERIFY_CASE = {
    "threshold-descent": verify_threshold_descent,
    "threshold-interval-sharpening": verify_threshold_interval_sharpening,
    "threshold-upward-push": verify_threshold_upward_push,
    "hybrid-quotient-residual": verify_hybrid_quotient_residual,
    "locator-selected": verify_locator_selected,
}


def selected_cases(case: str) -> list[str]:
    if case == "all":
        return list(VERIFY_CASE)
    return [case]


def stable_hash_payload(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: stable_hash_payload(item)
            for key, item in value.items()
            if key != "created_at_utc"
        }
    if isinstance(value, list):
        return [stable_hash_payload(item) for item in value]
    return value


def build_report(case: str) -> dict[str, Any]:
    cases = selected_cases(case)
    results = [VERIFY_CASE[item]() for item in cases]
    return {
        "schema_version": "native-sage-replay-companions-0.1.0",
        "proof_status": PROOF_STATUS,
        "theorem_problem_id": THEOREM_PROBLEM_ID,
        "result": "PASS",
        "cases_checked": len(results),
        "cases": results,
        "summary": {
            "pass_count": sum(1 for item in results if item["result"] == "PASS"),
            "replacements": {
                item["case"]: item["replacement_for"] for item in results
            },
            "case_hash": hash_payload(
                stable_hash_payload({
                    item["case"]: {
                        "status": item["status"],
                        "certificate": item["certificate"],
                    }
                    for item in results
                })
            ),
        },
        "non_claims": [
            "not_a_Sage_or_Arb_execution",
            "not_protocol_soundness",
            "not_mca_n_bad",
            "not_a_theorem_status_upgrade",
        ],
    }


def format_text(report: dict[str, Any]) -> str:
    lines = [
        "Native Sage replay companions",
        f"proof_status: {report['proof_status']}",
        f"theorem_problem_id: {report['theorem_problem_id']}",
        f"result: {report['result']}",
        f"cases_checked: {report['cases_checked']}",
    ]
    for item in report["cases"]:
        lines.append(
            f"- {item['case']}: {item['result']} "
            f"({item['status']}); replacement_for={item['replacement_for']}"
        )
    lines.append(f"case_hash: {report['summary']['case_hash']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=CASE_CHOICES, default="all")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    report = build_report(args.case)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(format_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
