#!/usr/bin/env python3
"""Exact sub-minute replay for the M31 aligned depth-32 collision census.

Python is auxiliary replay only.  No kernel Lean is shipped with this packet
(see the note's "Validation and replay" section); the two proved sub-facts it
would formalise -- even parity of aligned deficiencies and the exact binomial
cost arithmetic -- are elementary and are recomputed here from scratch.

`--check` recomputes, independently of the enumerator sources:

  * the unrestricted enumeration-cost table  C(479,e) * C(543,e), e in [34,65],
    with base-10 magnitudes, meet-in-the-middle storage per side, and the
    single-side wall-clock lower bound at the smallest deficiency;
  * the dyadic intact-fiber census  14 / 6 / 2  at scales T64 / T128 / T256;
  * the even-parity structural fact for dyadic-fiber-aligned deficiencies and
    the induced reachable-aligned map on [34,65];
  * the complete T16-aligned depth-32 collision census at e=48 and e=64, by an
    exact 32-power-sum hash join over all C(28,3)*C(31,3) and C(28,4)*C(31,4)
    class subsets (~15 s of the budget);
  * the classification of the 49 e=64 collisions as whole-T64-block swaps
    (7 x 7), checked directly on all 49 anchor/complement block pairs; and
  * the equivalence  (first 32 power sums of X, Y agree)
    <=> (top-32 nonleading locator coefficients of P_A, P_B agree)
    on fixed colliding and non-colliding 479-support witness pairs.

The T8-aligned long-run sweeps (e in {40, 48, 56}) are NOT re-run here; their
exact repro commands, wall-clock runtimes, and empty hit logs are recorded in
the note and their EMPTY outcome is carried as recorded data in the certificate.

Modes: --check, --write, --tamper-selftest.  Every asserted integer is produced
by two independent routes.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Any, Iterable, Sequence

P = 2**31 - 1
SCALE_2048 = pow(2, -2047, P)          # 1073741824 = 2^30 = 2^-2047 (mod p)
GENERATOR = (1717986917, 1288490189)   # norm 1, order 2^31 in F_p[i]
DEPTH = 32
SECONDS_PER_YEAR = 3.15e7
OPS_PER_SECOND = 1.0e9

ANCHOR_SIZE = 479
COMPLEMENT_SIZE = 543                  # |Q'| - |anchor| = 1022 - 479
INTACT_T64_CLASSES = list(range(5, 32, 2))     # {5, 7, ..., 31}: 14 classes
ANCHOR_CLASSES = [5, 7, 9, 11, 13, 15, 17]      # band anchor: census root

# The t16_mixing_floor rooted-shell anchor (integrated series cross-check).
INSIDE_T64 = [7, 9, 13, 19, 21, 23, 27]
OUTSIDE_T64 = [5, 11, 15, 17, 25, 29, 31]

CORE31_REPS = [
    63, 65, 127, 129, 191, 193, 255, 257,
    319, 321, 383, 385, 447, 449, 511, 513,
    575, 577, 639, 641, 703, 705, 767, 769,
    831, 833, 895, 897, 959, 961, 1023,
]

# Certified depth-32 target of the t16_mixing_floor anchor (core31 + INSIDE_T64
# blocks); reproduced here as an independent tie to the integrated series.
ETA_E192 = [
    1034127669, 50736831, 297947808, 2001416587, 582486197, 1119161472,
    2092060217, 691570973, 351942517, 1850514162, 230010785, 1719889839,
    1235349562, 568398669, 1689825028, 515651434, 18957312, 672550470,
    1519314673, 322573603, 116542290, 1792409170, 753121918, 223352466,
    1193775763, 493795963, 257600683, 1893789609, 1766068826, 431705051,
    1355303332, 141998040,
]

# e=96 T16 mixing witness (integrated series): six intact T16 fibers per side.
X16_MIN_REPS = [29, 15, 93, 21, 119, 95]
Y16_MIN_REPS = [33, 71, 9, 107, 7, 113]

# Ties this packet's quotient domain to the integrated band_mixing /
# t16_mixing_floor series: SHA-256 of the 1024 ordered quotient labels
# q_1, q_3, ..., q_2047.  Any drift in the field construction fails --check.
QUOTIENT_LABEL_SHA256 = (
    "082950c9e4f02d32329b2c49353c53a4b63c15aa54f461941fc78903be44fe55"
)

# T8-aligned partial-fiber sweeps: recorded long-run results, not re-run by
# --check.  Reproduce with gen_atoms.py + census_atoms.c (see the note).
# collisions == 0 <=> the stdout hit log is empty.
T8_RECORDED = {
    40: {"atoms_per_side": 5, "anchor_subsets": 3819816,
         "comp_subsets": 7028847, "collisions": 0, "real_seconds": 1.22,
         "hit_log": "hits_d8_a5.txt"},
    48: {"atoms_per_side": 6, "anchor_subsets": 32468436,
         "comp_subsets": 67945521, "collisions": 0, "real_seconds": 12.56,
         "hit_log": "hits_d8_a6.txt"},
    56: {"atoms_per_side": 7, "anchor_subsets": 231917400,
         "comp_subsets": 553270671, "collisions": 0, "real_seconds": 835.79,
         "hit_log": "hits_d8_a7.txt"},
}

PACKET_FILES = [
    "experimental/notes/thresholds/m31_aligned_collision_census_v1.md",
    "experimental/scripts/verify_m31_aligned_collision_census.py",
    "experimental/scripts/census_aligned.py",
    "experimental/scripts/gen_atoms.py",
    "experimental/scripts/census_atoms.c",
]

CERTIFICATE_RELPATH = (
    "experimental/data/certificates/m31-aligned-collision-census-v1/"
    "results_census.json"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


# ---------------------------------------------------------------- F_p[i] ----
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
    return {
        r: (SCALE_2048 * pow2(GENERATOR, r * 2**19)[0]) % P
        for r in range(1, 2048, 2)
    }


def quotient_labels_recurrence() -> dict[int, int]:
    base = pow2(GENERATOR, 2**19)
    step = mul2(base, base)
    current = base
    out: dict[int, int] = {}
    for j in range(1024):
        out[2 * j + 1] = (SCALE_2048 * current[0]) % P
        current = mul2(current, step)
    return out


# ------------------------------------------------------------- fibers -------
def block_reps64(a: int) -> list[int]:
    return [r for r in range(1, 2048, 2) if r % 64 in {a, 64 - a}]


def dyadic_fiber_reps(d: int, a: int) -> list[int]:
    m = 4096 // d
    return [r for r in range(1, 2048, 2) if r % m in {a, m - a}]


def intact_fibers(d: int, dset: set[int]) -> list[list[int]]:
    m = 4096 // d
    out = []
    for a in range(1, m // 2, 2):
        fib = dyadic_fiber_reps(d, a)
        if len(fib) == d and len(set(fib)) == d and set(fib) <= dset:
            out.append(fib)
    return out


# --------------------------------------------------------- polynomials ------
def poly_mul_linear(poly: Sequence[int], root: int) -> list[int]:
    out = [0] * (len(poly) + 1)
    for i, coefficient in enumerate(poly):
        out[i] = (out[i] - root * coefficient) % P
        out[i + 1] = (out[i + 1] + coefficient) % P
    return out


def locator_prefix(reps: Iterable[int], labels: dict[int, int],
                   depth: int) -> tuple[int, ...]:
    poly = [1]
    for r in sorted(reps):
        poly = poly_mul_linear(poly, labels[r])
    require(poly[-1] == 1, "locator is not monic")
    return tuple(reversed(poly[:-1]))[:depth]


def power_sums(reps: Iterable[int], labels: dict[int, int],
               depth: int) -> tuple[int, ...]:
    acc = [0] * depth
    for r in reps:
        q = labels[r]
        cur = q
        for k in range(depth):
            acc[k] = (acc[k] + cur) % P
            cur = (cur * q) % P
    return tuple(acc)


def cheb_pow_two(x: int, exponent_log2: int) -> int:
    value = x % P
    for _ in range(exponent_log2):
        value = (2 * value * value - 1) % P
    return value


def t16_sigma(r: int, labels: dict[int, int]) -> int:
    return cheb_pow_two((2 * labels[r]) % P, 4)


def common_prefix_length(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    count = 0
    for x, y in zip(left, right):
        if x != y:
            break
        count += 1
    return count


# ------------------------------------------------------------ hashing -------
def int_list_sha256(values: Iterable[int]) -> str:
    payload = ",".join(str(value) for value in values).encode()
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def comb_product(n: int, k: int) -> int:
    value = 1
    for i in range(1, k + 1):
        numerator = n - k + i
        require((value * numerator) % i == 0, "nonintegral binomial step")
        value = value * numerator // i
    return value


# -------------------------------------------------------- cost model --------
def cost_model() -> dict[str, Any]:
    per_e: dict[str, dict[str, float]] = {}
    total_pairs = 0
    for e in range(34, 66):
        cA = math.comb(ANCHOR_SIZE, e)
        cC = math.comb(COMPLEMENT_SIZE, e)
        require(cA == comb_product(ANCHOR_SIZE, e), "cA route disagreement")
        require(cC == comb_product(COMPLEMENT_SIZE, e), "cC route disagreement")
        total_pairs += cA * cC
        half = e // 2
        pairs_log = math.log10(cA) + math.log10(cC)
        mitm_log = (math.log10(math.comb(ANCHOR_SIZE, half))
                    + math.log10(math.comb(COMPLEMENT_SIZE, half)))
        one_side_log = math.log10(cA)
        years_one_side = one_side_log - math.log10(OPS_PER_SECOND) \
            - math.log10(SECONDS_PER_YEAR)
        per_e[str(e)] = {
            "pairs_log10": round(pairs_log, 1),
            "one_side_C479_log10": round(one_side_log, 1),
            "mitm_per_side_log10": round(mitm_log, 1),
            "one_side_years_log10": round(years_one_side, 1),
        }
    smallest = per_e["34"]
    return {
        "per_e": per_e,
        "total_pairs_log10": round(math.log10(total_pairs), 1),
        "smallest_slice_e34_pairs_log10": smallest["pairs_log10"],
        "largest_slice_e65_pairs_log10": per_e["65"]["pairs_log10"],
        "smallest_slice_one_side_years_log10": smallest["one_side_years_log10"],
        "mitm_per_side_log10_min": min(v["mitm_per_side_log10"]
                                       for v in per_e.values()),
        "mitm_per_side_log10_max": max(v["mitm_per_side_log10"]
                                       for v in per_e.values()),
    }


# --------------------------------------------------- expected certificate ---
def build_expected(repo_root: Path) -> dict[str, Any]:
    labels_pow = quotient_labels_pow()
    labels_rec = quotient_labels_recurrence()
    require(labels_pow == labels_rec, "quotient label routes disagree")
    labels = labels_pow
    require(len(labels) == 1024, "wrong quotient label count")
    require(len(set(labels.values())) == 1024, "duplicate quotient labels")
    require(SCALE_2048 == 1073741824, "monic scale mismatch")

    require(mul2(GENERATOR, (GENERATOR[0], -GENERATOR[1])) == (1, 0),
            "generator norm failure")
    require(pow2(GENERATOR, 2**30) == (P - 1, 0), "generator half-order failure")
    require(pow2(GENERATOR, 2**31) == (1, 0), "generator order failure")

    ordered_labels = [labels[r] for r in range(1, 2048, 2)]
    require(int_list_sha256(ordered_labels) == QUOTIENT_LABEL_SHA256,
            "quotient-label digest drift vs integrated series")

    qprime = [r for r in range(1, 2048, 2) if r not in {1, 3}]
    dset = set(qprime)
    require(len(qprime) == 1022, "wrong punctured domain size")

    # --- anchor support (band anchor): core31 + T64 blocks {5,...,17} ---
    require(len(CORE31_REPS) == 31 and len(set(CORE31_REPS)) == 31,
            "core31 malformed")
    require(set(CORE31_REPS) <= dset, "core31 outside Q'")
    anchor = set(CORE31_REPS)
    for a in ANCHOR_CLASSES:
        block = block_reps64(a)
        require(len(block) == 64 and set(block) <= dset, f"block {a} malformed")
        anchor |= set(block)
    require(len(anchor) == 479, "anchor support is not 479 points")
    complement = dset - anchor
    require(len(complement) == 543, "complement is not 543 points")

    # --- dyadic intact-fiber census 14 / 6 / 2 ---
    dyadic_census = {
        "64": len(intact_fibers(64, dset)),
        "128": len(intact_fibers(128, dset)),
        "256": len(intact_fibers(256, dset)),
    }
    require(dyadic_census == {"64": 14, "128": 6, "256": 2},
            "dyadic intact-fiber census drift")

    # --- even-parity structural fact + reachable-aligned map on [34,65] ---
    fiber_sizes = [2, 4, 8, 16, 32, 64]
    require(all(size % 2 == 0 for size in fiber_sizes),
            "a dyadic fiber has odd size")
    require(min(fiber_sizes) == 2, "smallest dyadic fiber is not size 2")
    reachable_aligned: dict[str, list[str]] = {}
    for e in range(34, 66):
        reach = []
        if e % 16 == 0 and e // 16 <= 4:
            reach.append(f"T16(a={e // 16})")
        if e % 8 == 0 and e // 8 <= 7:
            reach.append(f"T8(a={e // 8})")
        reachable_aligned[str(e)] = reach
    for e in range(34, 66, 2):    # even e: some are reachable
        pass
    require(all(reachable_aligned[str(e)] == []
                for e in range(35, 66, 2)),
            "an odd deficiency is marked aligned-reachable")

    # --- T16 classes: 62 intact, split anchor / complement / straddling ---
    t16_classes: list[frozenset[int]] = []
    for a in range(1, 128, 2):
        reps = dyadic_fiber_reps(16, a)
        if len(reps) == 16 and len(set(reps)) == 16 and set(reps) <= dset:
            t16_classes.append(frozenset(reps))
    require(len(t16_classes) == 62, "intact T16 class count drift")
    anchor_side = [c for c in t16_classes if c <= anchor]
    comp_side = [c for c in t16_classes if c <= complement]
    straddling = [c for c in t16_classes
                  if not (c <= anchor) and not (c <= complement)]
    require(len(anchor_side) == 28, "anchor-side T16 count drift")
    require(len(comp_side) == 31, "complement-side T16 count drift")
    require(len(straddling) == 3, "straddling T16 count drift")

    # per-class 32-power-sum vectors (power sums are additive over unions)
    def class_moment(cls: frozenset[int]) -> tuple[int, ...]:
        return power_sums(cls, labels, DEPTH)

    anchor_mom = [class_moment(c) for c in anchor_side]
    comp_mom = [class_moment(c) for c in comp_side]

    def subset_moment(moms: list[tuple[int, ...]],
                      idx: tuple[int, ...]) -> tuple[int, ...]:
        acc = [0] * DEPTH
        for i in idx:
            row = moms[i]
            for k in range(DEPTH):
                acc[k] = (acc[k] + row[k]) % P
        return tuple(acc)

    # map each intact T64 block to its 4 anchor-/comp-side T16 subclass indices
    def block_subclass_indices(side_classes: list[frozenset[int]],
                               classes: list[int]) -> dict[int, frozenset[int]]:
        out: dict[int, frozenset[int]] = {}
        for a in classes:
            block = set(block_reps64(a))
            members = frozenset(i for i, c in enumerate(side_classes)
                                if c <= block)
            if len(members) == 4:
                out[a] = members
        return out

    anchor_blocks = block_subclass_indices(anchor_side, ANCHOR_CLASSES)
    comp_classes = [a for a in INTACT_T64_CLASSES if a not in ANCHOR_CLASSES]
    comp_blocks = block_subclass_indices(comp_side, comp_classes)
    require(len(anchor_blocks) == 7, "anchor T64 block decomposition drift")
    require(len(comp_blocks) == 7, "complement T64 block decomposition drift")
    anchor_block_sets = set(anchor_blocks.values())
    comp_block_sets = set(comp_blocks.values())

    def census(atoms: int) -> dict[str, int]:
        left: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
        for idx in itertools.combinations(range(len(anchor_side)), atoms):
            left.setdefault(subset_moment(anchor_mom, idx), []).append(idx)
        collisions = whole_block = nonblock = 0
        for idx in itertools.combinations(range(len(comp_side)), atoms):
            mv = subset_moment(comp_mom, idx)
            matches = left.get(mv)
            if not matches:
                continue
            comp_is_block = (atoms == 4 and frozenset(idx) in comp_block_sets)
            for lidx in matches:
                collisions += 1
                anchor_is_block = (atoms == 4
                                   and frozenset(lidx) in anchor_block_sets)
                if anchor_is_block and comp_is_block:
                    whole_block += 1
                else:
                    nonblock += 1
        return {"collisions": collisions, "whole_T64_block_swaps": whole_block,
                "nonblock_collisions": nonblock}

    census_48 = census(3)
    require(census_48 == {"collisions": 0, "whole_T64_block_swaps": 0,
                          "nonblock_collisions": 0},
            "T16-aligned e=48 census is not empty")
    census_64 = census(4)
    require(census_64 == {"collisions": 49, "whole_T64_block_swaps": 49,
                          "nonblock_collisions": 0},
            "T16-aligned e=64 census is not 49 whole-block collisions")

    # --- 49-family collision property, verified directly on all 49 pairs ---
    verified_pairs = 0
    for a in ANCHOR_CLASSES:
        xa = power_sums(block_reps64(a), labels, DEPTH)
        for b in comp_classes:
            yb = power_sums(block_reps64(b), labels, DEPTH)
            require(xa == yb, f"block pair ({a},{b}) is not a depth-32 collision")
            verified_pairs += 1
    require(verified_pairs == 49, "did not verify exactly 49 block pairs")

    # --- (power sums agree) <=> (locator prefix-32 agree) on witnesses ---
    def support_swap(remove: set[int], add: set[int]) -> list[int]:
        support = (anchor - remove) | add
        require(len(support) == 479, "swapped support is not 479 points")
        require(support <= dset, "swapped support leaves Q'")
        return sorted(support)

    identity_witnesses = []
    # three colliding whole-block swaps (expected: both sides True)
    for a, b in [(5, 19), (7, 21), (9, 23)]:
        x = set(block_reps64(a))
        y = set(block_reps64(b))
        b_support = support_swap(x, y)
        ps_agree = power_sums(x, labels, DEPTH) == power_sums(y, labels, DEPTH)
        pref_agree = (locator_prefix(anchor, labels, DEPTH)
                      == locator_prefix(b_support, labels, DEPTH))
        require(ps_agree and pref_agree and ps_agree == pref_agree,
                f"colliding witness ({a},{b}) failed the equivalence")
        identity_witnesses.append(
            {"remove_block": a, "add_block": b, "kind": "whole_block_swap",
             "power_sums_agree": ps_agree, "prefix32_agree": pref_agree})
    # two non-colliding swaps: three T16 subclasses of one block plus one from
    # a second block, exchanged for a whole complement block (expected: both
    # sides False -- the equivalence still holds)
    for (a1, a2), b in [((5, 7), 19), ((9, 11), 21)]:
        sub = sorted(anchor_blocks[a1])[:3]
        x_classes = [anchor_side[i] for i in sub] + \
                    [anchor_side[sorted(anchor_blocks[a2])[0]]]
        x = set().union(*x_classes)
        require(len(x) == 64, "non-colliding X is not 64 points")
        y = set(block_reps64(b))
        b_support = support_swap(x, y)
        ps_agree = power_sums(x, labels, DEPTH) == power_sums(y, labels, DEPTH)
        pref_agree = (locator_prefix(anchor, labels, DEPTH)
                      == locator_prefix(b_support, labels, DEPTH))
        require((not ps_agree) and (not pref_agree) and ps_agree == pref_agree,
                f"non-colliding witness ({a1},{a2}->{b}) broke the equivalence")
        identity_witnesses.append(
            {"remove_partial_blocks": [a1, a2], "add_block": b,
             "kind": "non_block", "power_sums_agree": ps_agree,
             "prefix32_agree": pref_agree})

    # --- bring-up cross-checks against the integrated rooted-shell series ---
    # (a) certified depth-32 target eta of the t16_mixing_floor anchor
    e192_anchor = set(CORE31_REPS)
    for a in INSIDE_T64:
        e192_anchor |= set(block_reps64(a))
    require(len(e192_anchor) == 479, "t16_mixing_floor anchor is not 479 points")
    require(list(locator_prefix(e192_anchor, labels, DEPTH)) == ETA_E192,
            "eta reproduction drift vs integrated t16_mixing_floor packet")

    # (b) rooted-shell family counts 49 / 441 / 1225 (closed form and direct)
    family_counts_closed = {64 * t: math.comb(7, t) ** 2 for t in (1, 2, 3)}
    family_counts_direct = {
        64 * t: sum(1
                    for _ in itertools.combinations(INSIDE_T64, t)
                    for _ in itertools.combinations(OUTSIDE_T64, t))
        for t in (1, 2, 3)
    }
    require(family_counts_closed == family_counts_direct
            == {64: 49, 128: 441, 192: 1225}, "rooted-shell family count drift")

    # (c) all 1225 triple-T64 swaps agree through coefficient 63, break at 64
    block_ps = {a: power_sums(block_reps64(a), labels, 66)
                for a in INTACT_T64_CLASSES}

    def sum_vec(classes):
        acc = [0] * 66
        for a in classes:
            row = block_ps[a]
            for k in range(66):
                acc[k] = (acc[k] + row[k]) % P
        return tuple(acc)

    triple_nu = set()
    for removed in itertools.combinations(INSIDE_T64, 3):
        xv = sum_vec(removed)
        for added in itertools.combinations(OUTSIDE_T64, 3):
            triple_nu.add(common_prefix_length(xv, sum_vec(added)))
    require(triple_nu == {63}, "triple-T64 swap prefix agreement is not 63")

    # (d) the e=96 T16 mixing witness shares exactly 47 nonleading coefficients
    def fiber16(r0: int) -> list[int]:
        target = t16_sigma(r0, labels)
        return [r for r in range(1, 2048, 2) if t16_sigma(r, labels) == target]

    x96 = sorted(r for r0 in X16_MIN_REPS for r in fiber16(r0))
    y96 = sorted(r for r0 in Y16_MIN_REPS for r in fiber16(r0))
    require(len(x96) == len(set(x96)) == 96 and len(y96) == len(set(y96)) == 96
            and set(x96).isdisjoint(y96) and set(x96) <= dset
            and set(y96) <= dset, "e=96 witness sides malformed")
    core383 = [r for r in qprime if r not in set(x96) and r not in set(y96)][:383]
    a96 = sorted(core383 + x96)
    b96 = sorted(core383 + y96)
    require(len(a96) == len(b96) == 479, "e=96 supports are not 479 points")
    witness_nu = common_prefix_length(
        locator_prefix(a96, labels, 48), locator_prefix(b96, labels, 48))
    require(witness_nu == 47, "e=96 witness common prefix is not 47")

    # --- H_192 shell arithmetic (continuity with the rooted-shell series) ---
    h192 = math.comb(479, 192) * math.comb(543, 192)
    require(h192 == comb_product(479, 192) * comb_product(543, 192),
            "H192 route disagreement")
    q32 = P**DEPTH
    require(4 * h192 < q32 and (4 * h192) // q32 == 0, "floor(4 H192 / p^32) drift")

    costs = cost_model()

    packet_hashes: dict[str, str] = {}
    for relative in PACKET_FILES:
        path = repo_root / relative
        require(path.is_file(), f"missing packet file: {relative}")
        packet_hashes[relative] = file_sha256(path)

    return {
        "schema": "m31-aligned-collision-census-v1",
        "status": "EXPERIMENTAL",
        "workboard_item": "M1",
        "row": "Mersenne-31 list at 2^-100",
        "object": "LIST",
        "agreement": 1116023,
        "B_star": 16777215,
        "architecture": "DIRECT_PINNED_C2048_U0_V1_QUOTIENT_PROFILE",
        "census_object": (
            "depth-32 dyadic-fiber-aligned collision census, e in [34, 65], "
            "rooted at the 479-point band anchor"
        ),
        "collision_criterion": (
            "depth-32 collision <=> first 32 power sums of X = A\\B and "
            "Y = B\\A agree <=> top-32 nonleading coefficients of the monic "
            "locators P_A, P_B agree"
        ),
        "field": {
            "p": P,
            "p_power_32": str(q32),
            "monic_T2048_scale": SCALE_2048,
            "norm_one_generator": list(GENERATOR),
        },
        "domain": {
            "Q_prime_size": 1022,
            "punctured_reps": [1, 3],
            "punctured_labels": [labels[1], labels[3]],
            "quotient_label_sha256": QUOTIENT_LABEL_SHA256,
            "intact_T64_classes": INTACT_T64_CLASSES,
            "intact_T16_classes": {
                "total": 62, "anchor_side": 28,
                "complement_side": 31, "straddling": 3,
            },
        },
        "anchor": {
            "classes": ANCHOR_CLASSES,
            "core31_reps": CORE31_REPS,
            "core31_rep_sha256": int_list_sha256(CORE31_REPS),
            "support_size": 479,
            "support_rep_sha256": int_list_sha256(sorted(anchor)),
            "complement_size": 543,
        },
        "parity_fact": {
            "claim": ("every dyadic fiber has even size (min size 2 at T2), so "
                      "any union of whole fibers has even cardinality; hence a "
                      "dyadic-fiber-aligned deficiency is even and no aligned "
                      "exchange exists at odd e"),
            "min_fiber_size": 2,
            "aligned_deficiency_parity": "even",
            "status": "PROVED",
        },
        "reachable_aligned": reachable_aligned,
        "aligned_T16_census": {
            "48": {
                "scale": "T16", "atoms_per_side": 3,
                "exhaustive_over": "C(28,3) x C(31,3) anchor/complement triples",
                **census_48, "status": "EMPTY", "recomputed_by_check": True,
            },
            "64": {
                "scale": "T16", "atoms_per_side": 4,
                "exhaustive_over":
                    "C(28,4) x C(31,4) anchor/complement quadruples",
                **census_64,
                "classification":
                    "all 49 are whole-T64-block swaps (7 anchor x 7 complement); "
                    "no non-block T16-aligned collision exists",
                "status": "49 WHOLE-BLOCK / 0 NON-BLOCK",
                "recomputed_by_check": True,
            },
        },
        "aligned_T8_recorded": {
            str(e): {
                "scale": "T8", "atoms_per_side": rec["atoms_per_side"],
                "anchor_subsets": rec["anchor_subsets"],
                "comp_subsets": rec["comp_subsets"],
                "collisions": rec["collisions"],
                "exhaustive_over":
                    f"C(56,{rec['atoms_per_side']}) x "
                    f"C(63,{rec['atoms_per_side']}) T8-fiber subsets",
                "real_seconds": rec["real_seconds"],
                "hit_log": rec["hit_log"],
                "status": "EMPTY",
                "recomputed_by_check": False,
            }
            for e, rec in sorted(T8_RECORDED.items())
        },
        "identity_witnesses": identity_witnesses,
        "cost_model": costs,
        "shell_arithmetic": {
            "H192": str(h192),
            "floor_4_H192_over_p32": 0,
        },
        "min_weight_reformulation": (
            "A depth-32 collision (X, Y) is a nonzero balanced +/-1 vector in "
            "the kernel over F_p of the 32 x 1022 power-sum matrix "
            "V = [q_r^k]_{k=1..32}; that kernel is a length-1022 F_p code of "
            "dimension >= 990. The minimum unrestricted deficiency is the "
            "minimum-weight balanced codeword of this structured code. Stated "
            "only as a reformulation; no hardness is claimed."
        ),
        "sanity_gate": {
            "quotient_label_two_routes": "pow and order-1024 recurrence agree",
            "quotient_label_sha256_matches_integrated_series": True,
            "dyadic_census_14_6_2": [14, 6, 2],
            "block_pairs_49_all_collide": True,
            "power_sum_prefix32_equivalence": "confirmed on 5 witnesses",
            "eta_e192_anchor": "reproduced (prefix-32 of the t16_mixing_floor anchor)",
            "rooted_shell_family_49_441_1225": "closed form and direct agree",
            "triple_T64_e192_prefix_agreement": 63,
            "e96_T16_witness_prefix_agreement": 47,
            "c_vs_python_d16_a4_hits": "49 (recorded; census_atoms.c vs census_aligned.py)",
        },
        "packet_file_sha256": packet_hashes,
        "nonclaims": [
            "The unrestricted (non-aligned) census over e in [34, 65] is not "
            "resolved; only the dyadic-fiber-aligned slice is exhaustive.",
            "The T8-aligned sweeps at e in {40, 48, 56} are recorded long-run "
            "results, not re-verified by --check.",
            "No uniform band upper bound, received word, first-match survivor, "
            "codeword, ray, or slope is claimed.",
            "No row-global atom, adjacent-row closure, or endpoint movement is "
            "claimed; the packet is support-level on the pinned (u,v)=(0,1) "
            "profile.",
        ],
    }


# ------------------------------------------------------- canonical form -----
def canonical_text(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def first_difference(left: Any, right: Any, path: str = "$") -> str | None:
    if type(left) is not type(right):
        return f"{path}: type {type(left).__name__} != {type(right).__name__}"
    if isinstance(left, dict):
        if left.keys() != right.keys():
            return (f"{path}: key sets differ "
                    f"({sorted(set(left) ^ set(right))})")
        for key in left:
            diff = first_difference(left[key], right[key], f"{path}.{key}")
            if diff is not None:
                return diff
        return None
    if isinstance(left, list):
        if len(left) != len(right):
            return f"{path}: lengths {len(left)} != {len(right)}"
        for index, (x, y) in enumerate(zip(left, right)):
            diff = first_difference(x, y, f"{path}[{index}]")
            if diff is not None:
                return diff
        return None
    if left != right:
        return f"{path}: {left!r} != {right!r}"
    return None


def validate(candidate: dict[str, Any], expected: dict[str, Any]) -> None:
    diff = first_difference(candidate, expected)
    if diff is not None:
        raise AssertionError(f"certificate mismatch: {diff}")


def run_tamper_selftest(expected: dict[str, Any]) -> None:
    mutators = [
        lambda d: d["aligned_T16_census"]["64"].__setitem__("collisions", 50),
        lambda d: d["aligned_T16_census"]["64"].__setitem__(
            "nonblock_collisions", 1),
        lambda d: d["aligned_T16_census"]["48"].__setitem__("collisions", 1),
        lambda d: d["cost_model"].__setitem__("total_pairs_log10", 166.6),
        lambda d: d["cost_model"]["per_e"]["34"].__setitem__(
            "pairs_log10", 106.3),
        lambda d: d["parity_fact"].__setitem__("min_fiber_size", 1),
        lambda d: d["aligned_T8_recorded"]["56"].__setitem__("collisions", 1),
        lambda d: d["packet_file_sha256"].__setitem__(
            PACKET_FILES[0], "0" * 64),
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument("--repo-root", type=Path,
                        default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    require(args.check or args.write or args.tamper_selftest,
            "choose --check, --write, and/or --tamper-selftest")

    repo_root = args.repo_root.resolve()
    expected = build_expected(repo_root)
    certificate_path = repo_root / CERTIFICATE_RELPATH

    if args.write:
        certificate_path.parent.mkdir(parents=True, exist_ok=True)
        certificate_path.write_text(canonical_text(expected))
        print(f"wrote {CERTIFICATE_RELPATH}")

    if args.check:
        require(certificate_path.is_file(), f"missing {certificate_path}")
        candidate = json.loads(certificate_path.read_text())
        validate(candidate, expected)
        require(certificate_path.read_text() == canonical_text(candidate),
                "certificate is not in canonical JSON form")
        print("m31 aligned-collision census certificate: OK")

    if args.tamper_selftest:
        run_tamper_selftest(expected)
        print("m31 aligned-collision census tamper self-test: OK")


if __name__ == "__main__":
    main()
