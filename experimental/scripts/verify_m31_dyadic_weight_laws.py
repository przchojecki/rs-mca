#!/usr/bin/env python3
"""Exact replay for the M31 dyadic collision weight laws (T_16 and T_32).

Self-contained, standard-library big-integer arithmetic only.  Every claimed
integer is recomputed from the frozen domain definitions of the integrated
packages

    experimental/lean/m31_quotient_band_mixing/        (field, generator, labels)
    experimental/lean/m31_quotient_t16_mixing_floor/    (T_16/T_32/T_64 machinery)

and from the note

    experimental/notes/thresholds/m31_dyadic_weight_laws_v1.md

No external certificate, data file, or precomputed table is read.  The two
dyadic levels are recomputed independently and cross-checked against each other.

T_32 half (same-remainder sector):
  * domain decomposition, the odd/even power-sum flatness and the k=32 closed
    form, weight antisymmetry and the T_64 split;
  * the eta byte-match on the integrated anchor;
  * the collision <-> single class-weight-sum equation (necessity by Newton),
    with the full C(25,9) same-remainder census, the exact deficiency spectrum,
    s_224 = 40, the forty explicit e=224 witnesses, and the counterfactual 60.

T_16 half (cross-remainder sector):
  * the finer domain decomposition, the level law and the k=16 closed form
    p16 = 8*C(16,8) + 8*xi, weight antisymmetry xi_{128-c} = -xi_c;
  * the exact dyadic nesting T_32(a) = T_16(a) U T_16(128-a) with xi-cancellation
    / eta-doubling recovering the T_32 weight;
  * the depth-32 cross-remainder two-equation law {E16: sum xi, E32: sum eta},
    the eight integrated T_16-mixed witnesses (prefix agreement exactly 47),
    the exhaustive o_e meet-in-the-middle census (o_64=49, o_128=441, o_96=0),
    the constructive o_192 = 1225 whole-T_64 + 8 mixed = 1233 (= the integrated
    rooted degree), and the alternate-anchor e=96 consistency pair.

Modes:
    --check           recompute everything and compare against the claimed
                      constants; exit 0 iff every comparison holds.
    --tamper-selftest corrupt each load-bearing claimed constant in turn and
                      confirm the comparison layer rejects it; exit 0 iff every
                      injected mutation is caught.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import math
import sys
import time
from typing import Any, Dict, List, Tuple

# --------------------------------------------------------------------------- #
# Frozen domain definitions (band_mixing / t16_mixing_floor Witness sources)
# --------------------------------------------------------------------------- #
P = 2 ** 31 - 1                       # fieldPrime
SCALE = 1 << 30                       # monicT2048Scale = 1073741824 = 2^-2047 mod p
G = (1717986917, 1288490189)          # normOneGenerator


def fp2_mul(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    ar, ai = a
    br, bi = b
    return ((ar * br % P + P - ai * bi % P) % P, (ar * bi % P + ai * br % P) % P)


def fp2_conj(a: Tuple[int, int]) -> Tuple[int, int]:
    return (a[0] % P, (P - a[1] % P) % P)


def fp2_pow_two(e: int, u: Tuple[int, int]) -> Tuple[int, int]:
    for _ in range(e):
        u = fp2_mul(u, u)
    return u


def fp2_pow(u: Tuple[int, int], n: int) -> Tuple[int, int]:
    r = (1, 0)
    while n:
        if n & 1:
            r = fp2_mul(r, u)
        u = fp2_mul(u, u)
        n >>= 1
    return r


# quotient labels q_r = (2^30 * Re(g^(r 2^19))) mod p, r odd, via iterateMul
_QBASE = fp2_pow_two(19, G)
_QSTEP = fp2_mul(_QBASE, _QBASE)
_UNITS: List[Tuple[int, int]] = []
_u = _QBASE
for _ in range(1024):
    _UNITS.append(_u)
    _u = fp2_mul(_u, _QSTEP)
_LABELS = [(SCALE * x[0]) % P for x in _UNITS]

ODD = [2 * j + 1 for j in range(1024)]            # 1 .. 2047
PUNCT = [r for r in ODD if r not in (1, 3)]        # |D| = 1022
PUNCT_SET = set(PUNCT)


def label(r: int) -> int:
    return _LABELS[(r - 1) // 2]


def fold(res: int, m: int) -> int:
    return res if res <= m // 2 else m - res


def t16_class(r: int) -> int:
    return fold(r % 256, 256)


def t32_class(r: int) -> int:
    return fold(r % 128, 128)


def t64_class(r: int) -> int:
    return fold(r % 64, 64)


ODD_T32 = [2 * j + 1 for j in range(32)]           # T_32 labels {1,3,...,63}
INTACT = [a for a in ODD_T32 if a not in (1, 3)]   # 30 complete T_32 classes
ODD_T16 = [2 * j + 1 for j in range(64)]           # T_16 labels {1,3,...,127}
INTACT16 = [c for c in ODD_T16 if c not in (1, 3)]  # 62 complete T_16 classes

# level characters:  psi_16 = g^(2^23) order 256 ;  psi_32 = g^(2^24) order 128
PSI16 = fp2_pow_two(23, G)
PSI32 = fp2_pow_two(24, G)


def xi(c: int) -> int:                             # xi_c = psi16^c + psi16^-c
    return (2 * fp2_pow(PSI16, c)[0]) % P


def eta(c: int) -> int:                            # eta_c = psi32^c + psi32^-c
    return (2 * fp2_pow(PSI32, c)[0]) % P


def t16_block(c: int) -> List[int]:
    return [r for r in ODD if r % 256 in (c, 256 - c)]


def t32_block(a: int) -> List[int]:
    return [r for r in ODD if r % 128 in (a, 128 - a)]


def t64_block(a: int) -> List[int]:
    return [r for r in ODD if r % 64 in (a, 64 - a)]


def t16_of_t64(a: int) -> List[int]:
    return sorted({t16_class(r) for r in t64_block(a)})


def power_sum_block(block: List[int], k: int) -> int:
    return sum(pow(label(r), k, P) for r in block) % P


def locator_prefix(depth: int, reps: List[int]) -> List[int]:
    """First `depth` non-leading coefficients of prod_{r in reps}(Y - q_r)."""
    c = [1] + [0] * depth
    for r in reps:
        root = label(r) % P
        nw = c[:]
        prev = c[0]
        for i in range(1, len(c)):
            nw[i] = (c[i] + P - (root * prev) % P) % P
            prev = c[i]
        c = nw
    return c[1:]


def canonical_support(seed: List[int]) -> List[int]:
    s = set(seed)
    return [r for r in PUNCT if r in s]


def canonical_t32_remainder(support: List[int]) -> List[int]:
    occ: Dict[int, int] = {}
    for r in support:
        occ[t32_class(r)] = occ.get(t32_class(r), 0) + 1
    complete = {a for a in INTACT if occ.get(a, 0) == 32}
    return [r for r in support if t32_class(r) not in complete]


def deficiency(anchor: List[int], support: List[int]) -> int:
    ss = set(support)
    return len(anchor) - sum(1 for r in anchor if r in ss)


# integrated T16-mixing-floor anchor depth-32 target vector (eta)
ETA = [1034127669, 50736831, 297947808, 2001416587, 582486197, 1119161472,
       2092060217, 691570973, 351942517, 1850514162, 230010785, 1719889839,
       1235349562, 568398669, 1689825028, 515651434, 18957312, 672550470,
       1519314673, 322573603, 116542290, 1792409170, 753121918, 223352466,
       1193775763, 493795963, 257600683, 1893789609, 1766068826, 431705051,
       1355303332, 141998040]

# integrated T64 anchor partition and the eight T16-mixed witnesses
INSIDE_T64 = [7, 9, 13, 19, 21, 23, 27]
OUTSIDE_T64 = [5, 11, 15, 17, 25, 29, 31]
MIXED_SPECS = [
    ([7, 9, 27, 37, 55, 71, 73, 77, 83, 109, 115, 119], [5, 11, 17, 25, 39, 47, 53, 69, 79, 93, 99, 113]),
    ([7, 21, 27, 37, 43, 71, 77, 83, 85, 107, 109, 115], [5, 11, 17, 25, 39, 47, 53, 69, 79, 93, 99, 113]),
    ([7, 23, 27, 37, 41, 71, 77, 83, 87, 105, 109, 115], [5, 11, 17, 25, 39, 47, 53, 69, 79, 93, 99, 113]),
    ([9, 37, 41, 51, 55, 83, 85, 101, 105, 107, 109, 115], [5, 25, 31, 33, 47, 69, 75, 89, 93, 99, 111, 117]),
    ([13, 19, 21, 23, 27, 43, 45, 73, 77, 87, 91, 119], [11, 17, 29, 35, 39, 53, 59, 81, 95, 97, 103, 123]),
    ([9, 13, 19, 45, 51, 55, 57, 73, 91, 101, 119, 121], [15, 29, 35, 49, 59, 75, 81, 89, 103, 111, 117, 123]),
    ([13, 19, 21, 43, 45, 51, 57, 85, 91, 101, 107, 121], [15, 29, 35, 49, 59, 75, 81, 89, 103, 111, 117, 123]),
    ([13, 19, 23, 41, 45, 51, 57, 87, 91, 101, 105, 121], [15, 29, 35, 49, 59, 75, 81, 89, 103, 111, 117, 123]),
]
# alternate (band-mixing) e=96 pair at its own mixingAnchor (!= standard anchor)
ALT_X16MIN = [29, 15, 93, 21, 119, 95]
ALT_Y16MIN = [33, 71, 9, 107, 7, 113]


# --------------------------------------------------------------------------- #
# Claimed constants (the object of the packet).
# --------------------------------------------------------------------------- #
def claimed() -> Dict[str, Any]:
    return {
        # ---------- T_32 level ----------
        "t32_domain_size": 1022,
        "t32_num_complete": 30,
        "t32_incomplete_classes": [1, 3],
        "t32_incomplete_occupancy": 31,
        "t32_even_constants": {2: 4, 4: 1610612736, 6: 335544320, 8: 73400320,
                               10: 16515072, 12: 3784704, 14: 878592, 16: 205920,
                               18: 48620, 20: 536882459, 22: 1275071171,
                               24: 417333908, 26: 1504444574, 28: 554418214,
                               30: 527689737},
        "t32_first_class_dependent_k": 32,
        "t32_num_distinct_p32": 30,
        "base_const_B32": 513675826,
        "pair_sum_2B32": 1027351652,
        "p32_by_class": {
            5: 2104424953, 7: 613586304, 9: 1039897240, 11: 746156306,
            13: 481150863, 15: 1765281411, 17: 1511697280, 19: 627984930,
            21: 2022338803, 23: 42900917, 25: 420466079, 27: 514672161,
            29: 1565821297, 31: 1344250191, 33: 1830585108, 35: 1609014002,
            37: 512679491, 39: 606885573, 41: 984450735, 43: 1152496496,
            45: 399366722, 47: 1663138019, 49: 1409553888, 51: 546200789,
            53: 281195346, 55: 2134938059, 57: 413765348, 59: 1070410346,
            61: 670534994, 63: 1406012443},
        "eta": ETA,
        "anchor_len": 479,
        "e192_removed": [5, 21, 27, 29, 31, 39],
        "e192_added": [13, 19, 33, 37, 43, 63],
        "num_available": 25,
        "census_target": 520865170,
        "remainder_len": 191,
        "spectrum": {192: 10, 224: 40, 256: 30, 288: 4},
        "total_neighbors": 84,
        "s224": 40,
        "num_witnesses": 40,
        "weight_matches": 85,          # 84 neighbours + the identity selection
        "nonmatch_sample": 3000,
        "counterfactual_s224": 60,
        "deployed_C52_C41": 40,
        "abstract_C52_C61": 60,
        # ---------- T_16 level ----------
        "t16_domain_size": 1022,
        "t16_num_complete": 62,
        "t16_incomplete_classes": [1, 3],
        "t16_incomplete_occupancy": 15,
        "t16_even_constants": {2: 2, 4: 805306368, 6: 167772160, 8: 36700160,
                               10: 8257536, 12: 1892352, 14: 439296},
        "t16_first_class_dependent_k": 16,
        "t16_num_distinct_p16": 62,
        "base_const_B16": 102960,       # 8*C(16,8)
        # dyadic nesting / cross-remainder law
        "mixed_witnesses": 8,
        "mixed_prefix_agreement": 47,   # nu = 47 = 3*16 - 1
        "mixed_first_diff_k": 48,
        # o_e cross-remainder census at the standard anchor
        "pool_size": 28,
        "o_spectrum_exhaustive": {16: 0, 32: 0, 48: 0, 64: 49, 80: 0, 96: 0,
                                  112: 0, 128: 441},
        "o_192": 1233,
        "o_192_whole_t64": 1225,        # C(7,3)^2
        "o_192_mixed": 8,
        "o_96_e16_only": 132552,
        "o_96_e32_only": 5798464,
        "suff_pairs": 1723,             # 49 + 441 + 1225 + 8
        "nec_sample": 1000,
        # alternate-anchor e=96 consistency
        "alt_deficiency": 96,
        "alt_sigma_sum": 281588527,
        "alt_sigma_sqsum": 1888686693,
    }


# --------------------------------------------------------------------------- #
# Recompute -- runs the enumerations once, returns everything as a dict.
# --------------------------------------------------------------------------- #
def recompute() -> Dict[str, Any]:
    R: Dict[str, Any] = {}
    t0 = time.time()

    # generator sanity
    R["gen_norm_one"] = fp2_mul(G, fp2_conj(G)) == (1, 0)
    R["gen_half_order"] = fp2_pow_two(30, G) == (P - 1, 0)
    R["gen_full_order"] = fp2_pow_two(31, G) == (1, 0)

    # ===================== T_32 level =====================
    occ32 = {a: sum(1 for r in PUNCT if t32_class(r) == a) for a in ODD_T32}
    R["t32_domain_size"] = len(PUNCT)
    R["t32_num_complete"] = sum(1 for a in ODD_T32 if occ32[a] == 32)
    R["t32_incomplete_classes"] = sorted(a for a in ODD_T32 if occ32[a] != 32)
    R["t32_incomplete_occupancy"] = sorted({occ32[a] for a in ODD_T32 if occ32[a] != 32})
    R["t32_complete_equals_intact"] = sorted(a for a in ODD_T32 if occ32[a] == 32) == INTACT

    t32blk = {a: t32_block(a) for a in INTACT}
    R["t32_odd_k_all_zero"] = all(power_sum_block(t32blk[a], k) == 0
                                  for a in INTACT for k in range(1, 48, 2))
    even32: Dict[int, int] = {}
    even32_indep = True
    even32_formula = True
    for k in range(2, 31, 2):
        vals = {power_sum_block(t32blk[a], k) for a in INTACT}
        if len(vals) != 1:
            even32_indep = False
        v = next(iter(vals))
        even32[k] = v
        if v != (32 * pow(2, 29 * k, P) * math.comb(k, k // 2)) % P:
            even32_formula = False
    R["t32_even_constants"] = even32
    R["t32_even_class_independent"] = even32_indep
    R["t32_even_matches_formula"] = even32_formula
    p32 = {a: power_sum_block(t32blk[a], 32) for a in INTACT}
    R["p32_by_class"] = p32
    R["t32_num_distinct_p32"] = len(set(p32.values()))
    R["t32_first_class_dependent_k"] = 32 if (len({power_sum_block(t32blk[a], 30) for a in INTACT}) == 1
                                              and len(set(p32.values())) > 1) else None

    R["psi32_order_128"] = fp2_pow_two(6, PSI32) == (P - 1, 0) and fp2_pow_two(7, PSI32) == (1, 0)
    B32 = (8 * math.comb(32, 16)) % P
    R["base_const_B32"] = B32

    def w32(a: int) -> int:
        return (8 * (fp2_pow(PSI32, a)[0] + fp2_pow(PSI32, (128 - a % 128) % 128)[0])) % P

    R["t32_closed_form_matches"] = all((B32 + w32(a)) % P == p32[a] for a in INTACT)
    R["t32_antisymmetry"] = all((w32(a) + w32(64 - a)) % P == 0 for a in range(5, 32, 2))
    pair_sums = {(p32[a] + p32[64 - a]) % P for a in range(5, 32, 2)}
    R["pair_sum_2B32"] = next(iter(pair_sums)) if len(pair_sums) == 1 else None
    R["t64_split"] = all(set(t64_block(a)) == set(t32_block(a)) | set(t32_block(64 - a))
                         and len(t64_block(a)) == 64 for a in range(1, 32, 2))

    # eta byte-match on the integrated T16-mixing-floor anchor
    res31 = [r for r in t64_block(1) if r != 1][:31]
    anchor = canonical_support(res31 + [r for a in INSIDE_T64 for r in t64_block(a)])
    R["anchor_len"] = len(anchor)
    R["eta"] = locator_prefix(32, anchor)
    anchor_prefix32 = locator_prefix(32, anchor)
    anchor_prefix47 = locator_prefix(47, anchor)
    anchor_prefix48 = locator_prefix(48, anchor)

    # collision <=> equal Sigma p32 : integrated non-T64 e=192 pair
    rmv = [5, 21, 27, 29, 31, 39]
    add = [13, 19, 33, 37, 43, 63]
    rR = [r for a in rmv for r in t32_block(a)]
    aR = [r for a in add for r in t32_block(a)]
    core = [r for r in PUNCT if r not in set(rR) and r not in set(aR)][:287]
    A192 = canonical_support(core + rR)
    N192 = canonical_support(core + aR)
    R["e192_deficiency"] = deficiency(A192, N192)
    R["e192_weights_equal"] = (sum(p32[a] for a in rmv) % P == sum(p32[a] for a in add) % P)
    R["e192_prefix32_equal"] = locator_prefix(32, A192) == locator_prefix(32, N192)
    R["e192_prefix63_equal"] = locator_prefix(63, A192) == locator_prefix(63, N192)
    R["e192_prefix64_differs"] = locator_prefix(64, A192) != locator_prefix(64, N192)

    # deployed e=224 same-remainder anchor and census over C(25,9)
    def take(xs: List[int], n: int) -> List[int]:
        return xs[:n]

    remainder191 = canonical_support(
        [r for r in t32_block(1) if r != 1] + [r for r in t32_block(3) if r != 3]
        + take(t32_block(17), 31) + take(t32_block(47), 31)
        + take(t32_block(23), 31) + take(t32_block(41), 31)
        + take(t32_block(61), 5))
    anchor_classes = [59, 13, 19, 43, 25, 37, 35, 33, 63]
    anchor_set = set(anchor_classes)

    def support_from(classes: List[int]) -> List[int]:
        return canonical_support(remainder191 + [r for a in classes for r in t32_block(a)])

    anchor224 = support_from(anchor_classes)
    anchor224_prefix32 = locator_prefix(32, anchor224)
    target = sum(p32[a] for a in anchor_classes) % P
    available = [a for a in INTACT if a not in (17, 47, 23, 41, 61)]
    R["remainder_len"] = len(remainder191)
    R["num_available"] = len(available)
    R["census_target"] = target

    NONMATCH_SAMPLE = 3000
    spectrum: Dict[int, int] = {}
    e224_sel: List[Tuple[int, ...]] = []
    weight_matches = 0
    weight_matches_collide = True
    nonmatch_checked = 0
    nonmatch_collides = False
    for sel in itertools.combinations(sorted(available), 9):
        if sum(p32[a] for a in sel) % P != target:
            if nonmatch_checked < NONMATCH_SAMPLE:
                nonmatch_checked += 1
                if locator_prefix(32, support_from(list(sel))) == anchor224_prefix32:
                    nonmatch_collides = True
            continue
        weight_matches += 1
        if locator_prefix(32, support_from(list(sel))) != anchor224_prefix32:
            weight_matches_collide = False
        e = 32 * (9 - len(anchor_set.intersection(sel)))
        spectrum[e] = spectrum.get(e, 0) + 1
        if e == 224:
            e224_sel.append(tuple(sorted(sel)))
    R["identity_count"] = spectrum.get(0, 0)
    R["spectrum"] = {e: spectrum[e] for e in sorted(spectrum) if e}
    R["total_neighbors"] = sum(v for e, v in spectrum.items() if e)
    R["s224"] = spectrum.get(224, 0)
    R["weight_matches"] = weight_matches
    R["weight_matches_collide"] = weight_matches_collide
    R["nonmatch_checked"] = nonmatch_checked
    R["no_nonmatch_collides"] = not nonmatch_collides

    anchor_one_pairs = [[5, 59], [13, 51], [19, 45], [25, 39], [29, 35]]
    avail_zz = [[7, 57], [9, 55], [11, 53], [15, 49]]
    fixed = [21, 27, 31]
    built = set()
    for two in itertools.combinations(anchor_one_pairs, 2):
        for one in itertools.combinations(avail_zz, 1):
            built.add(tuple(sorted(fixed + [x for pr in two for x in pr]
                                   + [x for pr in one for x in pr])))
    R["num_witnesses"] = len(built)
    R["witnesses_equal_enum"] = built == set(e224_sel)
    arem = canonical_t32_remainder(anchor224)
    R["witnesses_all_deployed"] = all(
        len(s := support_from(list(c))) == 479
        and locator_prefix(32, s) == anchor224_prefix32
        and deficiency(anchor224, s) == 224
        and canonical_t32_remainder(s) == arem
        for c in built)

    cf = 0
    for sel in itertools.combinations(sorted(available + [17, 47, 23, 41]), 9):
        if sum(p32[a] for a in sel) % P == target and \
                32 * (9 - len(anchor_set.intersection(sel))) == 224:
            cf += 1
    R["counterfactual_s224"] = cf
    R["deployed_C52_C41"] = math.comb(5, 2) * math.comb(4, 1)
    R["abstract_C52_C61"] = math.comb(5, 2) * math.comb(6, 1)

    # ===================== T_16 level =====================
    occ16 = {c: sum(1 for r in PUNCT if t16_class(r) == c) for c in ODD_T16}
    R["t16_domain_size"] = len(PUNCT)
    R["t16_num_complete"] = sum(1 for c in ODD_T16 if occ16[c] == 16)
    R["t16_incomplete_classes"] = sorted(c for c in ODD_T16 if occ16[c] != 16)
    R["t16_incomplete_occupancy"] = sorted({occ16[c] for c in ODD_T16 if occ16[c] != 16})
    R["t16_complete_equals_intact"] = sorted(c for c in ODD_T16 if occ16[c] == 16) == INTACT16

    t16blk = {c: t16_block(c) for c in INTACT16}
    R["t16_odd_k_all_zero"] = all(power_sum_block(t16blk[c], k) == 0
                                  for c in INTACT16 for k in range(1, 48, 2))
    even16: Dict[int, int] = {}
    even16_indep = True
    even16_formula = True
    for k in range(2, 15, 2):
        vals = {power_sum_block(t16blk[c], k) for c in INTACT16}
        if len(vals) != 1:
            even16_indep = False
        v = next(iter(vals))
        even16[k] = v
        if v != (16 * pow(2, 29 * k, P) * math.comb(k, k // 2)) % P:
            even16_formula = False
    R["t16_even_constants"] = even16
    R["t16_even_class_independent"] = even16_indep
    R["t16_even_matches_formula"] = even16_formula
    p16 = {c: power_sum_block(t16blk[c], 16) for c in INTACT16}
    R["t16_num_distinct_p16"] = len(set(p16.values()))
    R["t16_first_class_dependent_k"] = 16 if (len({power_sum_block(t16blk[c], 14) for c in INTACT16}) == 1
                                              and len(set(p16.values())) > 1) else None
    B16 = (8 * math.comb(16, 8)) % P
    R["base_const_B16"] = B16
    R["t16_closed_form_matches"] = all((B16 + 16 * fp2_pow(PSI16, c)[0]) % P == p16[c] for c in INTACT16)
    R["psi16_order_256"] = (fp2_pow_two(7, PSI16) == (P - 1, 0) and fp2_pow_two(8, PSI16) == (1, 0)
                            and fp2_pow(PSI16, 128) == (P - 1, 0))
    R["t16_antisymmetry"] = all((xi(c) + xi(128 - c)) % P == 0 for c in range(1, 64, 2))

    # dyadic nesting T_32(a) = T_16(a) U T_16(128-a), xi cancels / eta doubles
    nest = add_ok = eta_partner = wt_ok = True
    for a in INTACT:
        reps = set(t32_block(a))
        halves = sorted({t16_class(r) for r in reps})
        if len(halves) != 2 or set(r for c in halves for r in t16_block(c)) != reps:
            nest = False
        if (power_sum_block(t16_block(halves[0]), 32)
                + power_sum_block(t16_block(halves[1]), 32)) % P != power_sum_block(list(reps), 32) % P:
            add_ok = False
        if len({eta(c) for c in halves}) != 1:
            eta_partner = False
        if power_sum_block(list(reps), 32) % P != (B32 + 8 * eta(halves[0])) % P:
            wt_ok = False
    R["t16_nesting"] = nest
    R["t16_additivity"] = add_ok
    R["t16_eta_partner_equal"] = eta_partner
    R["t16_weight_is_8eta"] = wt_ok

    # eight T16-mixed witnesses: E16 & E32, first diff k=48, prefix47 == anchor
    PK16 = {c: [power_sum_block(t16_block(c), k) for k in range(49)] for c in ODD_T16}

    def support_swap16(rem_c: List[int], add_c: List[int]) -> List[int]:
        rem = set(r for c in rem_c for r in t16_block(c))
        addr = set(r for c in add_c for r in t16_block(c))
        anchorset = set(anchor)
        return [r for r in PUNCT if (r in anchorset and r not in rem) or (r in addr)]

    mixed_ok = 0
    mixed_first_diffs = set()
    for Rm, Am in MIXED_SPECS:
        e16 = sum(xi(c) for c in Rm) % P == sum(xi(c) for c in Am) % P
        e32 = sum(eta(c) for c in Rm) % P == sum(eta(c) for c in Am) % P
        firstdiff = next(k for k in range(1, 49)
                         if sum(PK16[c][k] for c in Rm) % P != sum(PK16[c][k] for c in Am) % P)
        mixed_first_diffs.add(firstdiff)
        nb = support_swap16(Rm, Am)
        supp = (len(nb) == 479 and deficiency(anchor, nb) == 192
                and locator_prefix(47, nb) == anchor_prefix47
                and locator_prefix(48, nb) != anchor_prefix48)
        if e16 and e32 and firstdiff == 48 and supp:
            mixed_ok += 1
    R["mixed_witnesses"] = mixed_ok
    R["mixed_first_diff_k"] = sorted(mixed_first_diffs)
    R["mixed_prefix_agreement"] = 47 if (mixed_ok == 8 and mixed_first_diffs == {48}) else None

    # o_e cross-remainder census, meet-in-the-middle over the T16-fold pools
    inside_pool = sorted({c for a in INSIDE_T64 for c in t16_of_t64(a)})
    outside_pool = sorted({c for a in OUTSIDE_T64 for c in t16_of_t64(a)})
    R["pool_size"] = min(len(inside_pool), len(outside_pool)) if len(inside_pool) == len(outside_pool) else -1
    block_xi = {sum(xi(c) for c in t16_of_t64(a)) % P for a in INSIDE_T64 + OUTSIDE_T64}
    R["t64_block_xi_zero"] = block_xi == {0}
    xin = [xi(c) for c in inside_pool]
    ein = [eta(c) for c in inside_pool]
    xou = [xi(c) for c in outside_pool]
    eou = [eta(c) for c in outside_pool]

    def dist(pxi: List[int], pet: List[int], t: int, mode: int = 0) -> Dict[Any, int]:
        n = len(pxi)
        d: Dict[Any, int] = {}

        def rec(i: int, left: int, sx: int, se: int) -> None:
            if left == 0:
                key = (sx, se) if mode == 0 else (sx if mode == 1 else se)
                d[key] = d.get(key, 0) + 1
                return
            if n - i < left:
                return
            rec(i + 1, left - 1, (sx + pxi[i]) % P, (se + pet[i]) % P)
            rec(i + 1, left, sx, se)
        rec(0, t, 0, 0)
        return d

    o_spec: Dict[int, int] = {}
    for t in range(1, 9):
        din = dist(xin, ein, t)
        dou = dist(xou, eou, t)
        o_spec[16 * t] = sum(din[k] * dou.get(k, 0) for k in din)
    R["o_spectrum_exhaustive"] = o_spec
    xin6 = dist(xin, ein, 6, 1)
    xou6 = dist(xou, eou, 6, 1)
    ein6 = dist(xin, ein, 6, 2)
    eou6 = dist(xou, eou, 6, 2)
    R["o_96_e16_only"] = sum(v * xou6.get(k, 0) for k, v in xin6.items())
    R["o_96_e32_only"] = sum(v * eou6.get(k, 0) for k, v in ein6.items())

    def collide_ps16(rem_c: List[int], add_c: List[int]) -> bool:
        return all(sum(PK16[c][k] for c in rem_c) % P == sum(PK16[c][k] for c in add_c) % P
                   for k in range(1, 33))

    # o_192 constructive: 1225 whole-T64 3-swaps (E16&E32 & collide) + 8 mixed
    wt64 = wt64_coll = 0
    for rin in itertools.combinations(INSIDE_T64, 3):
        rc = [c for a in rin for c in t16_of_t64(a)]
        for aou in itertools.combinations(OUTSIDE_T64, 3):
            ac = [c for a in aou for c in t16_of_t64(a)]
            e = (sum(xi(c) for c in rc) % P == sum(xi(c) for c in ac) % P
                 and sum(eta(c) for c in rc) % P == sum(eta(c) for c in ac) % P)
            wt64 += 1
            wt64_coll += 1 if (e and collide_ps16(rc, ac)) else 0
    mixed_coll = sum(1 for Rm, Am in MIXED_SPECS if collide_ps16(Rm, Am))
    R["o_192_whole_t64"] = wt64_coll if wt64 == 1225 else -1
    R["o_192_mixed"] = mixed_coll
    R["o_192"] = wt64_coll + mixed_coll

    # sufficiency: all whole-T64 j-swaps (j=1,2,3) + 8 mixed collide
    suff_total = suff_coll = 0
    for j in (1, 2, 3):
        for rin in itertools.combinations(INSIDE_T64, j):
            rc = [c for a in rin for c in t16_of_t64(a)]
            for aou in itertools.combinations(OUTSIDE_T64, j):
                ac = [c for a in aou for c in t16_of_t64(a)]
                suff_total += 1
                suff_coll += 1 if collide_ps16(rc, ac) else 0
    suff_total += 8
    suff_coll += mixed_coll
    R["suff_pairs"] = suff_total
    R["suff_all_collide"] = suff_total == suff_coll

    # necessity: deterministic non-satisfying selection pairs must not collide
    nec_checked = 0
    nec_collides = False
    combos_in = list(itertools.combinations(range(len(inside_pool)), 3))
    combos_ou = list(itertools.combinations(range(len(outside_pool)), 3))
    step = 97
    idx = 0
    while nec_checked < 1000 and idx < len(combos_in) * len(combos_ou):
        ci = combos_in[(idx // len(combos_ou)) % len(combos_in)]
        co = combos_ou[(idx * step) % len(combos_ou)]
        idx += 1
        Si = [inside_pool[i] for i in ci]
        So = [outside_pool[i] for i in co]
        if (sum(xi(c) for c in Si) % P == sum(xi(c) for c in So) % P
                and sum(eta(c) for c in Si) % P == sum(eta(c) for c in So) % P):
            continue
        nec_checked += 1
        if collide_ps16(Si, So):
            nec_collides = True
    R["nec_checked"] = nec_checked
    R["no_nec_collides"] = not nec_collides

    # alternate-anchor e=96 consistency pair (band-mixing mixingAnchor)
    def cheb_double(x: int) -> int:
        return (2 * (x % P) * (x % P) + (P - 1)) % P

    def cheb_pow_two(e: int, x: int) -> int:
        for _ in range(e):
            x = cheb_double(x)
        return x % P

    def sigma16(r: int) -> int:                    # Re(g^(r 2^23)) via Chebyshev
        return cheb_pow_two(4, (2 * label(r)) % P)

    def fiber(r0: int) -> List[int]:
        s = sigma16(r0)
        return [r for r in ODD if sigma16(r) == s]

    x_classes = sorted({t16_class(r) for r in ALT_X16MIN})
    y_classes = sorted({t16_class(r) for r in ALT_Y16MIN})
    x_exch = [r for r0 in ALT_X16MIN for r in fiber(r0)]
    y_exch = [r for r0 in ALT_Y16MIN for r in fiber(r0)]
    core383 = [r for r in PUNCT if r not in set(x_exch) and r not in set(y_exch)][:383]
    mix_anchor = core383 + x_exch
    mix_neighbor = core383 + y_exch
    R["alt_e16"] = sum(xi(c) for c in x_classes) % P == sum(xi(c) for c in y_classes) % P
    R["alt_e32"] = sum(eta(c) for c in x_classes) % P == sum(eta(c) for c in y_classes) % P
    R["alt_deficiency"] = deficiency(mix_anchor, mix_neighbor)
    R["alt_prefix47_equal"] = locator_prefix(47, mix_anchor) == locator_prefix(47, mix_neighbor)
    R["alt_prefix48_differs"] = locator_prefix(48, mix_anchor) != locator_prefix(48, mix_neighbor)
    R["alt_distinct_anchor"] = set(mix_anchor) != set(anchor)
    xsig = [sigma16(r) for r in ALT_X16MIN]
    ysig = [sigma16(r) for r in ALT_Y16MIN]
    R["alt_sigma_sum"] = sum(xsig) % P
    R["alt_sigma_sum_equal"] = sum(xsig) % P == sum(ysig) % P
    R["alt_sigma_sqsum"] = sum((s * s) % P for s in xsig) % P
    R["alt_sigma_sqsum_equal"] = sum((s * s) % P for s in xsig) % P == sum((s * s) % P for s in ysig) % P

    R["_elapsed"] = time.time() - t0
    return R


# --------------------------------------------------------------------------- #
def compare(R: Dict[str, Any], C: Dict[str, Any]) -> List[str]:
    fails: List[str] = []

    def eq(name: str, got: Any, want: Any) -> None:
        if got != want:
            fails.append(name)

    def tru(name: str) -> None:
        if not R[name]:
            fails.append(name)

    for k in ("gen_norm_one", "gen_half_order", "gen_full_order"):
        tru(k)

    # ---------- T_32 ----------
    eq("t32_domain_size", R["t32_domain_size"], C["t32_domain_size"])
    eq("t32_num_complete", R["t32_num_complete"], C["t32_num_complete"])
    eq("t32_incomplete_classes", R["t32_incomplete_classes"], C["t32_incomplete_classes"])
    eq("t32_incomplete_occupancy", R["t32_incomplete_occupancy"], [C["t32_incomplete_occupancy"]])
    tru("t32_complete_equals_intact")
    tru("t32_odd_k_all_zero")
    tru("t32_even_class_independent")
    tru("t32_even_matches_formula")
    eq("t32_even_constants", R["t32_even_constants"], C["t32_even_constants"])
    eq("t32_num_distinct_p32", R["t32_num_distinct_p32"], C["t32_num_distinct_p32"])
    eq("t32_first_class_dependent_k", R["t32_first_class_dependent_k"], C["t32_first_class_dependent_k"])
    eq("p32_by_class", R["p32_by_class"], C["p32_by_class"])
    tru("psi32_order_128")
    eq("base_const_B32", R["base_const_B32"], C["base_const_B32"])
    tru("t32_closed_form_matches")
    tru("t32_antisymmetry")
    eq("pair_sum_2B32", R["pair_sum_2B32"], C["pair_sum_2B32"])
    tru("t64_split")
    eq("anchor_len", R["anchor_len"], C["anchor_len"])
    eq("eta", R["eta"], C["eta"])
    eq("e192_deficiency", R["e192_deficiency"], 192)
    tru("e192_weights_equal")
    tru("e192_prefix32_equal")
    tru("e192_prefix63_equal")
    tru("e192_prefix64_differs")
    eq("remainder_len", R["remainder_len"], C["remainder_len"])
    eq("num_available", R["num_available"], C["num_available"])
    eq("census_target", R["census_target"], C["census_target"])
    eq("identity_count", R["identity_count"], 1)
    eq("spectrum", R["spectrum"], C["spectrum"])
    eq("total_neighbors", R["total_neighbors"], C["total_neighbors"])
    eq("s224", R["s224"], C["s224"])
    eq("num_witnesses", R["num_witnesses"], C["num_witnesses"])
    tru("witnesses_equal_enum")
    tru("witnesses_all_deployed")
    eq("weight_matches", R["weight_matches"], C["weight_matches"])
    tru("weight_matches_collide")
    eq("nonmatch_checked", R["nonmatch_checked"], C["nonmatch_sample"])
    tru("no_nonmatch_collides")
    eq("counterfactual_s224", R["counterfactual_s224"], C["counterfactual_s224"])
    eq("deployed_C52_C41", R["deployed_C52_C41"], C["deployed_C52_C41"])
    eq("abstract_C52_C61", R["abstract_C52_C61"], C["abstract_C52_C61"])

    # ---------- T_16 ----------
    eq("t16_domain_size", R["t16_domain_size"], C["t16_domain_size"])
    eq("t16_num_complete", R["t16_num_complete"], C["t16_num_complete"])
    eq("t16_incomplete_classes", R["t16_incomplete_classes"], C["t16_incomplete_classes"])
    eq("t16_incomplete_occupancy", R["t16_incomplete_occupancy"], [C["t16_incomplete_occupancy"]])
    tru("t16_complete_equals_intact")
    tru("t16_odd_k_all_zero")
    tru("t16_even_class_independent")
    tru("t16_even_matches_formula")
    eq("t16_even_constants", R["t16_even_constants"], C["t16_even_constants"])
    eq("t16_num_distinct_p16", R["t16_num_distinct_p16"], C["t16_num_distinct_p16"])
    eq("t16_first_class_dependent_k", R["t16_first_class_dependent_k"], C["t16_first_class_dependent_k"])
    eq("base_const_B16", R["base_const_B16"], C["base_const_B16"])
    tru("t16_closed_form_matches")
    tru("psi16_order_256")
    tru("t16_antisymmetry")
    tru("t16_nesting")
    tru("t16_additivity")
    tru("t16_eta_partner_equal")
    tru("t16_weight_is_8eta")
    eq("mixed_witnesses", R["mixed_witnesses"], C["mixed_witnesses"])
    eq("mixed_first_diff_k", R["mixed_first_diff_k"], [C["mixed_first_diff_k"]])
    eq("mixed_prefix_agreement", R["mixed_prefix_agreement"], C["mixed_prefix_agreement"])
    eq("pool_size", R["pool_size"], C["pool_size"])
    tru("t64_block_xi_zero")
    eq("o_spectrum_exhaustive", R["o_spectrum_exhaustive"], C["o_spectrum_exhaustive"])
    eq("o_96_e16_only", R["o_96_e16_only"], C["o_96_e16_only"])
    eq("o_96_e32_only", R["o_96_e32_only"], C["o_96_e32_only"])
    eq("o_192_whole_t64", R["o_192_whole_t64"], C["o_192_whole_t64"])
    eq("o_192_mixed", R["o_192_mixed"], C["o_192_mixed"])
    eq("o_192", R["o_192"], C["o_192"])
    eq("suff_pairs", R["suff_pairs"], C["suff_pairs"])
    tru("suff_all_collide")
    eq("nec_checked", R["nec_checked"], C["nec_sample"])
    tru("no_nec_collides")
    tru("alt_e16")
    tru("alt_e32")
    eq("alt_deficiency", R["alt_deficiency"], C["alt_deficiency"])
    tru("alt_prefix47_equal")
    tru("alt_prefix48_differs")
    tru("alt_distinct_anchor")
    eq("alt_sigma_sum", R["alt_sigma_sum"], C["alt_sigma_sum"])
    tru("alt_sigma_sum_equal")
    eq("alt_sigma_sqsum", R["alt_sigma_sqsum"], C["alt_sigma_sqsum"])
    tru("alt_sigma_sqsum_equal")
    return fails


# --------------------------------------------------------------------------- #
def run_check() -> int:
    R = recompute()
    fails = compare(R, claimed())
    order = [
        ("t32_domain_size", "T32 Lemma A: |D| = 1022 = 30x32 + 2x31"),
        ("t32_even_matches_formula", "T32 Lemma B: even p_k = 32*2^(29k)*C(k,k/2), first dep k=32"),
        ("base_const_B32", "T32 Lemma B: p32 = 8*C(32,16) + 8(psi^a+psi^-a), B32 = 513675826"),
        ("t32_antisymmetry", "T32 Lemma C: w(64-a) = -w(a), T64 split"),
        ("eta", "cross-check: depth-32 prefix of integrated anchor = eta"),
        ("weight_matches_collide", "T32 collision-iff: 85 weight-matches collide, 0/3000 non-matches"),
        ("spectrum", "T32 census: spectrum {192:10,224:40,256:30,288:4}, 84 neighbours"),
        ("s224", "T32 census: s_224 = 40 exactly (masking 60 -> 40)"),
        ("t16_domain_size", "T16 Lemma A': |D| = 1022 = 62x16 + 2x15"),
        ("t16_even_matches_formula", "T16 level law: even p_k = 16*2^(29k)*C(k,k/2), first dep k=16"),
        ("base_const_B16", "T16 closed form: p16 = 8*C(16,8) + 16*Re(psi'^c), B16 = 102960"),
        ("t16_antisymmetry", "T16 Lemma C': xi_{128-c} = -xi_c (psi' order 256)"),
        ("t16_weight_is_8eta", "dyadic nesting: T32(a)=T16(a)UT16(128-a), xi cancels / eta doubles"),
        ("mixed_prefix_agreement", "cross-remainder: 8 T16-mixed witnesses, prefix agreement nu=47"),
        ("o_spectrum_exhaustive", "o-census (MITM t<=8): o_64=49, o_128=441, o_96=0, rest 0"),
        ("o_192", "o_192 = 1225 whole-T64 + 8 mixed = 1233 (= integrated rooted degree)"),
        ("suff_all_collide", "cross-remainder law: 1723 {E16,E32} pairs collide, 1000 failing do not"),
        ("alt_deficiency", "alternate anchor: band-mixing e=96 pair satisfies {E16,E32}"),
    ]
    for key, desc in order:
        print(f"  [{'FAIL' if key in fails else 'PASS'}] {desc}")
    print(f"\n  (recompute {R['_elapsed']:.1f}s)")
    if fails:
        print("RESULT: FAIL ->", sorted(set(fails)))
        return 1
    print("RESULT: ALL PASS")
    return 0


def run_tamper_selftest() -> int:
    R = recompute()
    mutations = []

    def add(name: str, mutate) -> None:
        c = copy.deepcopy(claimed())
        mutate(c)
        mutations.append((name, c))

    # T_32 mutations
    add("t32_domain_size", lambda c: c.__setitem__("t32_domain_size", 1023))
    add("t32_num_complete", lambda c: c.__setitem__("t32_num_complete", 31))
    add("t32_even_constant k=2", lambda c: c["t32_even_constants"].__setitem__(2, 5))
    add("base_const_B32", lambda c: c.__setitem__("base_const_B32", 513675827))
    add("pair_sum_2B32", lambda c: c.__setitem__("pair_sum_2B32", 1027351653))
    add("p32_by_class[5]", lambda c: c["p32_by_class"].__setitem__(5, 0))
    add("eta[0]", lambda c: c["eta"].__setitem__(0, 0))
    add("census_target", lambda c: c.__setitem__("census_target", 520865171))
    add("spectrum[224]", lambda c: c["spectrum"].__setitem__(224, 41))
    add("total_neighbors", lambda c: c.__setitem__("total_neighbors", 85))
    add("s224", lambda c: c.__setitem__("s224", 60))
    add("weight_matches", lambda c: c.__setitem__("weight_matches", 84))
    add("counterfactual_s224", lambda c: c.__setitem__("counterfactual_s224", 40))
    # T_16 mutations
    add("t16_domain_size", lambda c: c.__setitem__("t16_domain_size", 1021))
    add("t16_num_complete", lambda c: c.__setitem__("t16_num_complete", 61))
    add("t16_incomplete_occupancy", lambda c: c.__setitem__("t16_incomplete_occupancy", 16))
    add("t16_even_constant k=2", lambda c: c["t16_even_constants"].__setitem__(2, 3))
    add("t16_first_class_dependent_k", lambda c: c.__setitem__("t16_first_class_dependent_k", 14))
    add("base_const_B16", lambda c: c.__setitem__("base_const_B16", 102961))
    add("mixed_prefix_agreement", lambda c: c.__setitem__("mixed_prefix_agreement", 48))
    add("mixed_witnesses", lambda c: c.__setitem__("mixed_witnesses", 7))
    add("o_spectrum o_64", lambda c: c["o_spectrum_exhaustive"].__setitem__(64, 50))
    add("o_spectrum o_96", lambda c: c["o_spectrum_exhaustive"].__setitem__(96, 1))
    add("o_192", lambda c: c.__setitem__("o_192", 1234))
    add("o_192_mixed", lambda c: c.__setitem__("o_192_mixed", 7))
    add("suff_pairs", lambda c: c.__setitem__("suff_pairs", 1722))
    add("pool_size", lambda c: c.__setitem__("pool_size", 27))
    add("alt_deficiency", lambda c: c.__setitem__("alt_deficiency", 64))
    add("alt_sigma_sum", lambda c: c.__setitem__("alt_sigma_sum", 281588528))

    escaped = []
    for name, c in mutations:
        if not compare(R, c):
            escaped.append(name)
    if escaped:
        print("FAIL: mutations escaped ->", escaped)
        return 1
    print(f"PASS tamper selftest ({len(mutations)} mutations rejected)")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args(argv)
    return run_check() if args.check else run_tamper_selftest()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
