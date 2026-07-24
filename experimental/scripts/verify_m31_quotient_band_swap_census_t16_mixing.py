#!/usr/bin/env python3
"""Exact replay for the M31 quotient-band swap census and T16 mixing packet.

Python is auxiliary replay only. The proof-validation gate is the stdlib-only
Lean package `experimental/lean/m31_quotient_band_mixing/` built by fork CI.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence

P = 2**31 - 1
SCALE_2048 = pow(2, -2047, P)
BASE_SHA = "5b8bbc2083583460dd3d9b23b8d8fca6701f7ae6"
BRANCH = "gptpro/m31-quotient-band-mixing-r3"

CORE31_REPS = [
    63, 65, 127, 129, 191, 193, 255, 257,
    319, 321, 383, 385, 447, 449, 511, 513,
    575, 577, 639, 641, 703, 705, 767, 769,
    831, 833, 895, 897, 959, 961, 1023,
]
INTACT_CLASSES = list(range(5, 32, 2))
ANCHOR_CLASSES = [5, 7, 9, 11, 13, 15, 17]
X16_MIN_REPS = [29, 15, 93, 21, 119, 95]
Y16_MIN_REPS = [33, 71, 9, 107, 7, 113]

# Upstream steering files are recorded for provenance, not gated.  `agents.md` is
# rewritten by governance commits -- fb6d955 replaced the blob this packet froze --
# so drift there must report, never fail.  The recorded blob stays in the payload.
STEERING_SOURCES = frozenset({"agents.md"})
SOURCE_PINS = {
    "agents.md": "30d8b9f1b4caa3c7504fe3d24fc7ce8da84de434",
    "experimental/grande_finale.tex":
        "8a5d9791900ca9eed773feba146b92ad296704ce",
    "experimental/notes/thresholds/m31_c2048_partial_occupancy_30carrier_reduction.md":
        "7460c0830ac5d47db9f96e6f74f2a42d89ff8cbb",
    "experimental/notes/thresholds/m31_c2048_fixed_template_interleaved_quotient_route_cut.md":
        "3f69250b63b861963da03759b46d726f3e8754d1",
    "experimental/notes/thresholds/m31_q_rooted_shell_envelope.md":
        "45fd288abd2173d06af3fab244ed20568c991607",
    "experimental/notes/thresholds/m31_quotient_prefix_flatness_t64_witness.md":
        "f422a80d89568bed5be9688b7cc1975786d5d983",
    "experimental/lean/m31_quotient_prefix_flatness/M31QuotientPrefixFlatness/T64Witness.lean":
        "f65cbe956189c7978d16879b5e6fc74f7839af02",
}

LEGACY_PACKET_FILE_SHA256 = {
    "PR_BODY.md": "f68c51c682a0720244e84bd84787158fa586b8557c8e5b321bf256991b41712e",
    "experimental/agents-log-entry-gptpro-m31-quotient-band-mixing-r3.md": "227a94c58a62502802af3ec4d7375d99be89a9c3d5b270f3097f80cbc410adb8",
}

PACKET_FILES = [
    "experimental/notes/thresholds/m31_quotient_band_swap_census_t16_mixing.md",
    "experimental/scripts/verify_m31_quotient_band_swap_census_t16_mixing.py",
    "experimental/lean/m31_quotient_band_mixing/.gitignore",
    "experimental/lean/m31_quotient_band_mixing/CORRESPONDENCE.md",
    "experimental/lean/m31_quotient_band_mixing/M31QuotientBandMixing.lean",
    "experimental/lean/m31_quotient_band_mixing/M31QuotientBandMixing/Witnesses.lean",
    "experimental/lean/m31_quotient_band_mixing/lake-manifest.json",
    "experimental/lean/m31_quotient_band_mixing/lakefile.lean",
    "experimental/lean/m31_quotient_band_mixing/lean-toolchain",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def add2(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
    return ((u[0] + v[0]) % P, (u[1] + v[1]) % P)


def mul2(u: tuple[int, int], v: tuple[int, int]) -> tuple[int, int]:
    return (
        (u[0] * v[0] - u[1] * v[1]) % P,
        (u[0] * v[1] + u[1] * v[0]) % P,
    )


def pow2(u: tuple[int, int], exponent: int) -> tuple[int, int]:
    acc = (1, 0)
    base = u
    e = exponent
    while e:
        if e & 1:
            acc = mul2(acc, base)
        base = mul2(base, base)
        e >>= 1
    return acc


def quotient_labels_pow() -> dict[int, int]:
    g = (1717986917, 1288490189)
    return {
        r: (SCALE_2048 * pow2(g, r * 2**19)[0]) % P
        for r in range(1, 2048, 2)
    }


def quotient_labels_recurrence() -> dict[int, int]:
    g = (1717986917, 1288490189)
    base = pow2(g, 2**19)
    step = mul2(base, base)
    current = base
    out: dict[int, int] = {}
    for j in range(1024):
        r = 2 * j + 1
        out[r] = (SCALE_2048 * current[0]) % P
        current = mul2(current, step)
    return out


def chebyshev_pow_two(x: int, exponent_log2: int) -> int:
    value = x % P
    for _ in range(exponent_log2):
        value = (2 * value * value - 1) % P
    return value


def block_reps64(a: int) -> list[int]:
    return [
        r for r in range(1, 2048, 2)
        if r % 64 in {a, 64 - a}
    ]


def poly_mul_linear(poly: Sequence[int], root: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for i, coefficient in enumerate(poly):
        out[i] = (out[i] - root * coefficient) % P
        out[i + 1] = (out[i + 1] + coefficient) % P
    return out


def poly_from_values(values: Iterable[int]) -> list[int]:
    poly = [1]
    for value in values:
        poly = poly_mul_linear(poly, value)
    return poly


def locator_for_reps(reps: Iterable[int], labels: dict[int, int]) -> list[int]:
    return poly_from_values(labels[r] for r in sorted(reps))


def locator_prefix(
    reps: Iterable[int], labels: dict[int, int], depth: int
) -> list[int]:
    poly = locator_for_reps(reps, labels)
    require(poly[-1] == 1, "locator is not monic")
    return list(reversed(poly[:-1]))[:depth]


def common_prefix_length(left: Sequence[int], right: Sequence[int]) -> int:
    count = 0
    for x, y in zip(reversed(left[:-1]), reversed(right[:-1])):
        if x != y:
            break
        count += 1
    return count


def comb_product(n: int, k: int) -> int:
    value = 1
    for i in range(1, k + 1):
        numerator = n - k + i
        require((value * numerator) % i == 0, "nonintegral binomial step")
        value = value * numerator // i
    return value


def int_list_sha256(values: Iterable[int]) -> str:
    payload = ",".join(str(value) for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


def family_sha256(
    family: Sequence[tuple[tuple[int, ...], tuple[int, ...]]]
) -> str:
    digest = hashlib.sha256()
    for classes, support in family:
        digest.update(("classes:" + ",".join(map(str, classes)) + "\n").encode())
        digest.update(("support:" + ",".join(map(str, support)) + "\n").encode())
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def truncated_leading_product(
    factors: Sequence[Sequence[int]], depth: int
) -> list[int]:
    """Multiply leading-first coefficient lists, retaining `depth` terms."""
    acc = [1]
    for factor in factors:
        out = [0] * min(depth, len(acc) + len(factor) - 1)
        for i, x in enumerate(acc):
            if i >= depth:
                break
            for j, y in enumerate(factor):
                if i + j >= depth:
                    break
                out[i + j] = (out[i + j] + x * y) % P
        acc = out
    return acc


def t16_sigma(r: int, labels: dict[int, int]) -> int:
    return chebyshev_pow_two((2 * labels[r]) % P, 4)


def fiber16_reps(r0: int, labels: dict[int, int]) -> list[int]:
    target = t16_sigma(r0, labels)
    return [
        r for r in range(1, 2048, 2)
        if t16_sigma(r, labels) == target
    ]


def shell_counts_formula() -> dict[int, int]:
    return {
        64 * t: math.comb(7, t) ** 2
        for t in range(1, 8)
    }


def build_expected(repo_root: Path) -> dict[str, Any]:
    labels_pow = quotient_labels_pow()
    labels_rec = quotient_labels_recurrence()
    require(labels_pow == labels_rec, "quotient label routes disagree")
    labels = labels_pow
    require(len(labels) == 1024, "wrong quotient label count")
    require(len(set(labels.values())) == 1024, "duplicate quotient labels")

    g = (1717986917, 1288490189)
    require(mul2(g, (g[0], -g[1])) == (1, 0), "generator norm failure")
    require(pow2(g, 2**30) == (P - 1, 0), "generator half-order failure")
    require(pow2(g, 2**31) == (1, 0), "generator order failure")

    qprime_reps = [r for r in range(1, 2048, 2) if r not in {1, 3}]
    require(len(qprime_reps) == 1022, "wrong punctured domain size")

    blocks: dict[int, list[int]] = {}
    block_locators: dict[int, list[int]] = {}
    for a in INTACT_CLASSES:
        reps = block_reps64(a)
        require(len(reps) == 64, f"class {a} has wrong size")
        require(len(set(reps)) == 64, f"class {a} has duplicates")
        require(set(reps) <= set(qprime_reps), f"class {a} is punctured")
        blocks[a] = reps
        block_locators[a] = locator_for_reps(reps, labels)
    all_intact = [r for a in INTACT_CLASSES for r in blocks[a]]
    require(len(all_intact) == 896, "wrong intact union size")
    require(len(set(all_intact)) == 896, "intact classes overlap")

    require(len(CORE31_REPS) == 31, "wrong core size")
    require(len(set(CORE31_REPS)) == 31, "core duplicates")
    require(set(CORE31_REPS) <= set(qprime_reps), "core outside Q'")
    require(set(CORE31_REPS).isdisjoint(all_intact), "core meets intact class")

    nonconstant_templates = {tuple(poly[1:]) for poly in block_locators.values()}
    require(
        len(nonconstant_templates) == 1,
        "T64 block locators do not differ only in the constant",
    )

    family: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for classes in itertools.combinations(INTACT_CLASSES, 7):
        support = sorted(
            set(CORE31_REPS).union(*(set(blocks[a]) for a in classes))
        )
        require(len(support) == 479, "family support has wrong size")
        require(set(support) <= set(qprime_reps), "family support outside Q'")
        family.append((classes, tuple(support)))
    require(len(family) == math.comb(14, 7) == 3432, "wrong family size")
    require(len({support for _, support in family}) == 3432, "duplicate supports")

    anchor_support = next(
        support for classes, support in family
        if list(classes) == ANCHOR_CLASSES
    )
    direct_shell_counts: Counter[int] = Counter()
    anchor_set = set(anchor_support)
    for _, support in family:
        if support != anchor_support:
            direct_shell_counts[len(anchor_set - set(support))] += 1
    formula_shell_counts = shell_counts_formula()
    require(dict(sorted(direct_shell_counts.items())) == formula_shell_counts,
            "closed-form and direct shell counts disagree")

    round2_included = [5, 15, 17, 19, 21, 23, 25]
    round2_excluded = [7, 9, 11, 13, 29, 31]
    round2_counts_closed = {
        64 * t: math.comb(7, t) * math.comb(6, t)
        for t in range(1, 4)
    }
    round2_counts_direct = {
        64 * t: sum(
            1
            for _ in itertools.combinations(round2_included, t)
            for _ in itertools.combinations(round2_excluded, t)
        )
        for t in range(1, 4)
    }
    require(
        round2_counts_closed == round2_counts_direct
        == {64: 42, 128: 315, 192: 700},
        "round-2 full-class swap census drift",
    )

    # Independent all-family leading-prefix route: constants occur only at
    # leading-first index 64, beyond the retained 64 terms.
    core_locator = locator_for_reps(CORE31_REPS, labels)
    family_prefixes: set[tuple[int, ...]] = set()
    for classes, _ in family:
        factors = [list(reversed(core_locator))]
        factors.extend(list(reversed(block_locators[a])) for a in classes)
        leading = truncated_leading_product(factors, 64)
        require(len(leading) == 64 and leading[0] == 1,
                "truncated family locator malformed")
        family_prefixes.add(tuple(leading[1:64]))
    require(len(family_prefixes) == 1, "family depth-63 prefixes differ")

    triple_classes = (11, 13, 15, 17, 19, 21, 23)
    triple_support = next(
        support for classes, support in family if classes == triple_classes
    )
    require(len(set(anchor_support) - set(triple_support)) == 192,
            "triple-swap deficiency mismatch")
    require(
        locator_prefix(anchor_support, labels, 63)
        == locator_prefix(triple_support, labels, 63),
        "direct triple-swap prefix mismatch",
    )

    x_fibers = [fiber16_reps(r, labels) for r in X16_MIN_REPS]
    y_fibers = [fiber16_reps(r, labels) for r in Y16_MIN_REPS]
    for fiber in x_fibers + y_fibers:
        require(len(fiber) == 16, "T16 fiber has wrong size")
        require(len(set(fiber)) == 16, "T16 fiber duplicates")
        require(set(fiber) <= set(qprime_reps), "T16 fiber is punctured")
    x_reps = sorted(r for fiber in x_fibers for r in fiber)
    y_reps = sorted(r for fiber in y_fibers for r in fiber)
    require(len(x_reps) == len(set(x_reps)) == 96, "X side malformed")
    require(len(y_reps) == len(set(y_reps)) == 96, "Y side malformed")
    require(set(x_reps).isdisjoint(y_reps), "T16 sides overlap")

    x_sigmas = [t16_sigma(r, labels) for r in X16_MIN_REPS]
    y_sigmas = [t16_sigma(r, labels) for r in Y16_MIN_REPS]
    require(
        x_sigmas
        == [583555490, 812986380, 849605071,
            1093071961, 1362440376, 2022380190],
        "X sigma list drift",
    )
    require(
        y_sigmas
        == [125103457, 197700101, 785043271,
            1054411686, 1079800039, 1334497267],
        "Y sigma list drift",
    )
    x_sum = sum(x_sigmas) % P
    y_sum = sum(y_sigmas) % P
    x_square_sum = sum(value * value for value in x_sigmas) % P
    y_square_sum = sum(value * value for value in y_sigmas) % P
    require(x_sum == y_sum == 281588527, "T16 first moment mismatch")
    require(
        x_square_sum == y_square_sum == 1888686693,
        "T16 second moment mismatch",
    )
    x_e2 = sum(
        x_sigmas[i] * x_sigmas[j]
        for i in range(6) for j in range(i + 1, 6)
    ) % P
    y_e2 = sum(
        y_sigmas[i] * y_sigmas[j]
        for i in range(6) for j in range(i + 1, 6)
    ) % P
    require(x_e2 == y_e2 == 1950190555, "T16 e2 mismatch")
    x_sigma_poly = poly_from_values(x_sigmas)
    y_sigma_poly = poly_from_values(y_sigmas)
    sigma_difference = [
        (left - right) % P
        for left, right in zip(x_sigma_poly, y_sigma_poly)
    ]
    require(
        sigma_difference
        == [1030524974, 16043166, 1710076578, 1294116245, 0, 0, 0],
        "T16 block polynomial difference drift",
    )

    available_core = [
        r for r in qprime_reps
        if r not in set(x_reps) and r not in set(y_reps)
    ]
    core383 = available_core[:383]
    mixing_anchor = sorted(core383 + x_reps)
    mixing_neighbor = sorted(core383 + y_reps)
    require(len(core383) == 383, "mixing core size mismatch")
    require(len(mixing_anchor) == len(set(mixing_anchor)) == 479,
            "mixing anchor malformed")
    require(len(mixing_neighbor) == len(set(mixing_neighbor)) == 479,
            "mixing neighbor malformed")
    require(len(set(mixing_anchor) - set(mixing_neighbor)) == 96,
            "mixing deficiency mismatch")
    mixing_anchor_locator = locator_for_reps(mixing_anchor, labels)
    mixing_neighbor_locator = locator_for_reps(mixing_neighbor, labels)
    prefix_length = common_prefix_length(
        mixing_anchor_locator, mixing_neighbor_locator
    )
    require(prefix_length == 47, "mixing common prefix is not exactly 47")
    mixing_prefix47 = locator_prefix(mixing_anchor, labels, 47)
    require(
        mixing_prefix47 == locator_prefix(mixing_neighbor, labels, 47),
        "mixing direct prefix mismatch",
    )
    require(
        locator_prefix(mixing_anchor, labels, 48)
        != locator_prefix(mixing_neighbor, labels, 48),
        "mixing prefix unexpectedly extends to 48",
    )

    # Every asserted integer is recomputed by two independent routes.
    h192_math = math.comb(479, 192) * math.comb(543, 192)
    h192_product = comb_product(479, 192) * comb_product(543, 192)
    require(h192_math == h192_product, "H192 binomial routes disagree")
    q32 = P**32
    require(4 * h192_math < q32, "4H192 is not below Q")
    require((4 * h192_math) // q32 == 0, "H192 floor is not zero")

    m_math = math.comb(1022, 479)
    m_product = comb_product(1022, 479)
    require(m_math == m_product, "M binomial routes disagree")
    require(m_math // q32 == 3614119, "floor(M/Q) drift")
    require((m_math + q32 - 1) // q32 == 3614120, "ceil(M/Q) drift")
    require((4 * m_math) // q32 == 14456476, "floor(4M/Q) drift")
    compiler_total = 1 + 1225 * 447 + (4 * m_math) // q32
    require(compiler_total == 15004052, "compiler total drift")
    require(16777215 - compiler_total == 1773163, "reserve drift")

    packet_hashes: dict[str, str] = dict(LEGACY_PACKET_FILE_SHA256)
    for relative in PACKET_FILES:
        path = repo_root / relative
        require(path.is_file(), f"missing packet file: {relative}")
        packet_hashes[relative] = file_sha256(path)

    checked_source_pins: dict[str, str] = {}
    present_source_count = sum(
        1 for relative in SOURCE_PINS if (repo_root / relative).is_file()
    )
    if present_source_count not in {0, len(SOURCE_PINS)}:
        raise AssertionError("partial source-pin tree: use the complete repository")
    if present_source_count == len(SOURCE_PINS):
        for relative, expected_sha in SOURCE_PINS.items():
            actual_sha = git_blob_sha(repo_root / relative)
            if relative in STEERING_SOURCES:
                if actual_sha != expected_sha:
                    print(
                        f"NOTE steering source drifted: {relative} "
                        f"recorded {expected_sha}, observed {actual_sha}"
                    )
                checked_source_pins[relative] = expected_sha
                continue
            require(
                actual_sha == expected_sha,
                f"stale source pin for {relative}: "
                f"expected {expected_sha}, got {actual_sha}",
            )
            checked_source_pins[relative] = actual_sha
    else:
        checked_source_pins = dict(SOURCE_PINS)

    return {
        "schema": "m31-quotient-band-swap-census-t16-mixing-v1",
        "status": "COUNTEREXAMPLE_NEW_FLOOR",
        "activity": "FALSIFY",
        "base_sha": BASE_SHA,
        "branch": BRANCH,
        "workboard_item": "M1",
        "row": "Mersenne-31 list at 2^-100",
        "object": "LIST",
        "target_epsilon": "2^-100",
        "agreement": 1116023,
        "B_star": 16777215,
        "architecture": "DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE",
        "partition_digest": "N/A; fixed local support profile, no row atom banked",
        "atom_or_cell": "Q / fixed-template quotient-prefix family",
        "projection_and_unit": (
            "479-subsets per first-32 quotient-locator coefficient target; "
            "no received-word, codeword, ray, or slope projection."
        ),
        "direct_statement": (
            "One exact 3432-support T64 family has rooted shell lower bounds "
            "49, 441, and 1225 at e=64,128,192. A separate exact T16 exchange "
            "has e=96 and 47 matching nonleading locator coefficients."
        ),
        "field": {
            "p": P,
            "p_power_32": str(q32),
            "monic_T2048_scale": SCALE_2048,
            "norm_one_generator": [1717986917, 1288490189],
        },
        "domain": {
            "Q_prime_size": 1022,
            "punctured_reps": [1, 3],
            "punctured_labels": [labels[1], labels[3]],
            "quotient_label_sha256":
                int_list_sha256(labels[r] for r in range(1, 2048, 2)),
            "intact_T64_classes": INTACT_CLASSES,
            "intact_union_size": 896,
        },
        "swap_family": {
            "core31_reps": CORE31_REPS,
            "core31_rep_sha256": int_list_sha256(CORE31_REPS),
            "anchor_classes": ANCHOR_CLASSES,
            "anchor_support_reps": list(anchor_support),
            "anchor_support_rep_sha256": int_list_sha256(anchor_support),
            "family_size": 3432,
            "family_sha256": family_sha256(family),
            "selection_sha256":
                int_list_sha256(c for classes, _ in family for c in classes),
            "common_locator_prefix_depth": 63,
            "common_prefix63":
                locator_prefix(anchor_support, labels, 63),
            "shell_counts": {
                str(distance): count
                for distance, count in sorted(formula_shell_counts.items())
            },
            "band_lower_bounds": {
                "64": 49,
                "128": 441,
                "192": 1225,
            },
            "round2_anchor_full_class_swap_counts": {
                str(distance): count
                for distance, count in sorted(round2_counts_closed.items())
            },
            "round2_printed_six_complete": False,
            "degree_transfer": {
                "core_degree": 31,
                "block_degree": 64,
                "class_product_difference_degree": 6,
                "locator_difference_degree_bound": 415,
            },
        },
        "off_lattice_T16_witness": {
            "deficiency": 96,
            "x_min_reps": X16_MIN_REPS,
            "y_min_reps": Y16_MIN_REPS,
            "x_sigmas": x_sigmas,
            "y_sigmas": y_sigmas,
            "sigma_sum": x_sum,
            "sigma_square_sum": x_square_sum,
            "sigma_e2": x_e2,
            "sigma_polynomial_difference_ascending": sigma_difference,
            "x_fibers": [
                {
                    "min_rep": min(fiber),
                    "sigma": t16_sigma(min(fiber), labels),
                    "reps": fiber,
                }
                for fiber in x_fibers
            ],
            "y_fibers": [
                {
                    "min_rep": min(fiber),
                    "sigma": t16_sigma(min(fiber), labels),
                    "reps": fiber,
                }
                for fiber in y_fibers
            ],
            "core383_reps": core383,
            "anchor_reps": mixing_anchor,
            "neighbor_reps": mixing_neighbor,
            "anchor_rep_sha256": int_list_sha256(mixing_anchor),
            "neighbor_rep_sha256": int_list_sha256(mixing_neighbor),
            "common_prefix_length": prefix_length,
            "common_prefix47": mixing_prefix47,
            "common_prefix47_sha256": int_list_sha256(mixing_prefix47),
            "next_coefficient_anchor":
                locator_prefix(mixing_anchor, labels, 48)[47],
            "next_coefficient_neighbor":
                locator_prefix(mixing_neighbor, labels, 48)[47],
        },
        "arithmetic": {
            "M": str(m_math),
            "floor_M_over_Q": 3614119,
            "ceil_M_over_Q": 3614120,
            "floor_4M_over_Q": 14456476,
            "H192": str(h192_math),
            "floor_4H192_over_Q": 0,
            "necessary_uniform_intercept_floor": 1225,
            "maximum_budget_fitting_uniform_intercept": 5191,
            "compiler_total_at_b1225": compiler_total,
            "compiler_reserve_at_b1225": 1773163,
        },
        "rung_status": {
            "A1": "FALSE_BY_T16_E96_WITNESS",
            "A2": "OPEN",
            "A3": "OPEN",
            "A4_zero_rigidity": "FALSE_BY_T16_E96_WITNESS",
            "A4_capped_form": "OPEN",
            "B1": "NOT_REACHED",
            "B2": "NOT_REACHED",
        },
        "packet_file_sha256": packet_hashes,
        "source_git_blob_pins": checked_source_pins,
        "nonclaims": [
            "No uniform band cap is proved.",
            "No non-full deficiency-64 neighbor is constructed.",
            "No shell degree of 5192 is constructed.",
            "No received word, first-match survivor, codeword, ray, or slope is constructed.",
            "No row-global atom or adjacent-row closure is claimed.",
        ],
    }


def canonical_text(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def first_difference(left: Any, right: Any, path: str = "$") -> str | None:
    if type(left) is not type(right):
        return f"{path}: type {type(left).__name__} != {type(right).__name__}"
    if isinstance(left, dict):
        if left.keys() != right.keys():
            return f"{path}: key sets differ"
        for key in left:
            difference = first_difference(left[key], right[key], f"{path}.{key}")
            if difference is not None:
                return difference
        return None
    if isinstance(left, list):
        if len(left) != len(right):
            return f"{path}: lengths {len(left)} != {len(right)}"
        for index, (x, y) in enumerate(zip(left, right)):
            difference = first_difference(x, y, f"{path}[{index}]")
            if difference is not None:
                return difference
        return None
    if left != right:
        return f"{path}: {left!r} != {right!r}"
    return None


def validate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    difference = first_difference(candidate, expected)
    if difference is not None:
        raise AssertionError(f"certificate mismatch: {difference}")


def run_tamper_selftest(expected: dict[str, Any]) -> None:
    mutators = [
        lambda data: data["swap_family"]["band_lower_bounds"].__setitem__(
            "192", 1224
        ),
        lambda data: data["off_lattice_T16_witness"]["x_sigmas"].__setitem__(
            0, data["off_lattice_T16_witness"]["x_sigmas"][0] + 1
        ),
        lambda data: data["off_lattice_T16_witness"].__setitem__(
            "common_prefix_length", 48
        ),
        lambda data: data["arithmetic"].__setitem__(
            "compiler_total_at_b1225", 15004053
        ),
        lambda data: data["packet_file_sha256"].__setitem__(
            "PR_BODY.md", "0" * 64
        ),
    ]
    for index, mutate in enumerate(mutators, start=1):
        tampered = copy.deepcopy(expected)
        mutate(tampered)
        try:
            validate(tampered, expected)
        except AssertionError:
            continue
        raise AssertionError(f"tamper self-test {index} was not rejected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()

    require(
        args.check or args.write or args.tamper_selftest,
        "choose --check, --write, and/or --tamper-selftest",
    )
    repo_root = args.repo_root.resolve()
    expected = build_expected(repo_root)
    certificate_path = (
        repo_root
        / "experimental/data/certificates/"
          "m31-quotient-band-swap-census-t16-mixing/"
          "m31_quotient_band_swap_census_t16_mixing.json"
    )

    if args.write:
        certificate_path.parent.mkdir(parents=True, exist_ok=True)
        certificate_path.write_text(canonical_text(expected))

    if args.check:
        require(certificate_path.is_file(), f"missing {certificate_path}")
        candidate = json.loads(certificate_path.read_text())
        validate(candidate, expected)
        require(
            certificate_path.read_text() == canonical_text(candidate),
            "certificate is not in canonical JSON form",
        )
        print("m31 quotient-band certificate: OK")

    if args.tamper_selftest:
        run_tamper_selftest(expected)
        print("m31 quotient-band tamper self-test: OK")


if __name__ == "__main__":
    main()
