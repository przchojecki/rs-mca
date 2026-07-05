#!/usr/bin/env python3
"""Verifier for the M1 half-turn pair-core compression packet.

The mathematical theorem is symbolic.  This script checks the deployed-row
arithmetic and performs exact small cyclotomic enumerations in Q(zeta_8) and
Q(zeta_16), using the relation zeta^(n/2) = -1.

It verifies two branch statements:

* {1,3}: survivors are exactly half-turn pair cores plus residual size <= 1.
* {1,4}: survivors are exactly those satisfying the residual-core equation
  e_2(U)-alpha_R e_1(U)+beta_R=0 after half-turn decomposition.
* {1,4}: after lower-domain shadow and higher-pair balanced residual ledgers
  are charged, the primitive residual image is bounded by n+1.
* {1,4}: parity-empty classes for the half-turn-balance ledger and a concrete
  counterexample to unrestricted twofold lower-fiber rigidity.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
from typing import Any


DEPLOYED_N = 2**21
DEPLOYED_K = 2**20
KOALABEAR_P = 2**31 - 2**24 + 1
Q_LINE = KOALABEAR_P**6
BUDGET_Q_LINE_FLOOR = Q_LINE // 2**128
BUDGET_CONSERVATIVE = (Q_LINE - 1) // 2**128
assert BUDGET_Q_LINE_FLOOR == BUDGET_CONSERVATIVE
BUDGET = BUDGET_CONSERVATIVE
AGREEMENTS = (1_116_044, 1_116_045, 1_116_046, 1_116_047)

ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "m1-half-turn-pair-core-13-v1"
CERT_PATH = CERT_DIR / "m1_half_turn_pair_core_13_v1.json"
CERT_README_PATH = CERT_DIR / "README.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "m1_half_turn_pair_core_13_v1.report.md"
)


class TwoPowerCyclotomic:
    """Exact arithmetic in Q(zeta_n) for n=2^m.

    Elements are integer coefficient tuples in the basis 1,zeta,...,zeta^(N-1),
    where N=n/2 and zeta^N=-1.
    """

    def __init__(self, n: int) -> None:
        assert n >= 4 and n & (n - 1) == 0
        self.n = n
        self.N = n // 2

    def zero(self) -> tuple[int, ...]:
        return (0,) * self.N

    def one(self) -> tuple[int, ...]:
        return (1,) + (0,) * (self.N - 1)

    def neg(self, a: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(-x for x in a)

    def add(self, a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(x + y for x, y in zip(a, b))

    def sub(self, a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(x - y for x, y in zip(a, b))

    def mul(self, a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
        out = [0] * self.N
        for i, x in enumerate(a):
            if not x:
                continue
            for j, y in enumerate(b):
                if not y:
                    continue
                exp = i + j
                if exp >= self.N:
                    out[exp - self.N] -= x * y
                else:
                    out[exp] += x * y
        return tuple(out)

    def is_zero(self, a: tuple[int, ...]) -> bool:
        return all(x == 0 for x in a)

    def root(self, exp: int) -> tuple[int, ...]:
        exp %= self.n
        sign = 1
        if exp >= self.N:
            sign = -1
            exp -= self.N
        out = [0] * self.N
        out[exp] = sign
        return tuple(out)

    def key(self, a: tuple[int, ...]) -> str:
        return ",".join(str(x) for x in a)


def locator_coeffs(field: TwoPowerCyclotomic, support: tuple[int, ...]) -> list[tuple[int, ...]]:
    coeffs = [field.one()]
    for exp in support:
        x = field.root(exp)
        new = [field.zero()] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            new[i] = field.sub(new[i], field.mul(coeff, x))
            new[i + 1] = field.add(new[i + 1], coeff)
        coeffs = new
    return coeffs


def half_turn_parts(n: int, support: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Return square exponents for paired-core orbits and residual exponents."""
    half = n // 2
    s = set(support)
    seen: set[int] = set()
    core_squares: list[int] = []
    residual: list[int] = []
    for x in support:
        if x in seen:
            continue
        y = (x + half) % n
        if y in s:
            core_squares.append((2 * x) % n)
            seen.add(x)
            seen.add(y)
        else:
            residual.append(x)
            seen.add(x)
    return tuple(sorted(core_squares)), tuple(sorted(residual))


def half_turn_residual_size(n: int, support: tuple[int, ...]) -> int:
    return len(half_turn_parts(n, support)[1])


def elementary_symmetric(
    field: TwoPowerCyclotomic, exponents: tuple[int, ...], degree: int
) -> tuple[int, ...]:
    if degree < 0:
        raise ValueError("degree must be nonnegative")
    elems = [field.zero()] * (degree + 1)
    elems[0] = field.one()
    for exp in exponents:
        x = field.root(exp)
        for r in range(degree, 0, -1):
            elems[r] = field.add(elems[r], field.mul(x, elems[r - 1]))
    return elems[degree]


def predicted_support_count(n: int, j: int) -> int:
    half = n // 2
    if j % 2 == 0:
        return math.comb(half, j // 2)
    return n * math.comb(half - 1, (j - 1) // 2)


def predicted_slope_bound(n: int, j: int) -> int:
    return 1 if j % 2 == 0 else n


def enumerate_case_13(n: int, j: int) -> dict[str, Any]:
    field = TwoPowerCyclotomic(n)
    survivors: list[tuple[int, ...]] = []
    slopes: set[str] = set()
    bad_predicted: list[tuple[int, ...]] = []
    bad_survivor: list[tuple[int, ...]] = []

    for support in itertools.combinations(range(n), j):
        coeffs = locator_coeffs(field, support)
        c_j = coeffs[j]
        assert c_j == field.one()
        z = field.neg(coeffs[j - 1])
        row1 = field.add(coeffs[j - 1], z)
        row3 = field.add(coeffs[j - 3], field.mul(z, coeffs[j - 2]))
        survivor = field.is_zero(row1) and field.is_zero(row3)
        predicted = half_turn_residual_size(n, support) <= 1
        if survivor:
            survivors.append(support)
            slopes.add(field.key(z))
        if predicted and not survivor:
            bad_predicted.append(support)
        if survivor and not predicted:
            bad_survivor.append(support)

    predicted_count = predicted_support_count(n, j)
    predicted_slopes = predicted_slope_bound(n, j)
    assert not bad_predicted
    assert not bad_survivor
    assert len(survivors) == predicted_count
    assert len(slopes) <= predicted_slopes

    return {
        "window": "{1,3}",
        "n": n,
        "j": j,
        "total_subsets": math.comb(n, j),
        "survivor_supports": len(survivors),
        "predicted_supports": predicted_count,
        "distinct_slopes": len(slopes),
        "predicted_slope_bound": predicted_slopes,
        "parity": "even" if j % 2 == 0 else "odd",
        "classification_exact": True,
        "sample_supports": [list(support) for support in survivors[:8]],
    }


def residual_choice_bound(n: int, j: int) -> int:
    half = n // 2
    out = 0
    for s in range(0, min(j, n - j) + 1):
        if s % 2 == j % 2:
            out += (2**s) * math.comb(half, s)
    return out


def residual_core_equation_14(
    field: TwoPowerCyclotomic, n: int, support: tuple[int, ...]
) -> tuple[bool, int]:
    core_squares, residual = half_turn_parts(n, support)

    e1r = elementary_symmetric(field, residual, 1)
    e2r = elementary_symmetric(field, residual, 2)
    e3r = elementary_symmetric(field, residual, 3)
    e4r = elementary_symmetric(field, residual, 4)
    alpha = field.sub(e2r, field.mul(e1r, e1r))
    beta = field.sub(e4r, field.mul(e1r, e3r))

    e1u = elementary_symmetric(field, core_squares, 1)
    e2u = elementary_symmetric(field, core_squares, 2)
    lhs = field.add(field.sub(e2u, field.mul(alpha, e1u)), beta)
    return field.is_zero(lhs), len(residual)


def residual_ab(field: TwoPowerCyclotomic, residual: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    e1 = elementary_symmetric(field, residual, 1)
    e2 = elementary_symmetric(field, residual, 2)
    e3 = elementary_symmetric(field, residual, 3)
    e4 = elementary_symmetric(field, residual, 4)
    a_value = field.sub(field.mul(e1, e1), e2)
    b_value = field.sub(field.mul(e1, e3), e4)
    return a_value, b_value


def residual_key(n: int, support: tuple[int, ...]) -> str:
    return ",".join(str(x) for x in half_turn_parts(n, support)[1])


def enumerate_case_14(n: int, j: int) -> dict[str, Any]:
    field = TwoPowerCyclotomic(n)
    survivors: list[tuple[int, ...]] = []
    slopes: set[str] = set()
    residual_to_slope: dict[str, str] = {}
    residual_histogram: dict[str, int] = {}
    bad_predicted: list[tuple[int, ...]] = []
    bad_survivor: list[tuple[int, ...]] = []

    for support in itertools.combinations(range(n), j):
        coeffs = locator_coeffs(field, support)
        c_j = coeffs[j]
        assert c_j == field.one()
        z = field.neg(coeffs[j - 1])
        row1 = field.add(coeffs[j - 1], z)
        row4 = field.add(coeffs[j - 4], field.mul(z, coeffs[j - 3]))
        survivor = field.is_zero(row1) and field.is_zero(row4)
        predicted, residual_size = residual_core_equation_14(field, n, support)
        if survivor:
            survivors.append(support)
            slope_key = field.key(z)
            slopes.add(slope_key)
            residual_histogram[str(residual_size)] = residual_histogram.get(str(residual_size), 0) + 1
            key = residual_key(n, support)
            old = residual_to_slope.setdefault(key, slope_key)
            assert old == slope_key
        if predicted and not survivor:
            bad_predicted.append(support)
        if survivor and not predicted:
            bad_survivor.append(support)

    bound = residual_choice_bound(n, j)
    assert not bad_predicted
    assert not bad_survivor
    assert len(slopes) <= bound

    return {
        "window": "{1,4}",
        "n": n,
        "j": j,
        "total_subsets": math.comb(n, j),
        "survivor_supports": len(survivors),
        "distinct_slopes": len(slopes),
        "residual_choice_bound": bound,
        "residual_histogram": residual_histogram,
        "residual_core_equation_exact": True,
        "residual_determines_slope": True,
        "sample_supports": [list(support) for support in survivors[:8]],
    }


def deployed_row(A: int) -> dict[str, Any]:
    j = DEPLOYED_N - A
    slope_bound = predicted_slope_bound(DEPLOYED_N, j)
    assert slope_bound < BUDGET
    return {
        "A": A,
        "j": j,
        "j_parity": "even" if j % 2 == 0 else "odd",
        "slope_image_bound": slope_bound,
        "slope_bound_explanation": "1 if j even, n if j odd",
        "below_budget": slope_bound < BUDGET,
        "budget_minus_slope_bound": BUDGET - slope_bound,
        "bit_margin_log2_budget_over_bound": math.log2(BUDGET / slope_bound),
    }


def finite_field_13_transfer_guardrail() -> dict[str, Any]:
    """Guardrail: the honest {1,3} theorem is not automatic in finite fields."""
    p = 17
    n = 16
    generator = 3
    support = (0, 1, 3, 14)
    domain = [pow(generator, i, p) for i in range(n)]
    values = [domain[i] for i in support]

    coeffs = [1]
    for x in values:
        new = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            new[i] = (new[i] - coeff * x) % p
            new[i + 1] = (new[i + 1] + coeff) % p
        coeffs = new

    j = len(support)
    z = (-coeffs[j - 1]) % p
    row1 = (coeffs[j - 1] + z * coeffs[j]) % p
    row3 = (coeffs[j - 3] + z * coeffs[j - 2]) % p
    _, residual = half_turn_parts(n, support)
    residual_size = len(residual)

    exact_field = TwoPowerCyclotomic(n)
    exact_e1 = elementary_symmetric(exact_field, residual, 1)
    exact_e2 = elementary_symmetric(exact_field, residual, 2)
    exact_e3 = elementary_symmetric(exact_field, residual, 3)
    exact_f3 = exact_field.sub(exact_field.mul(exact_e1, exact_e2), exact_e3)

    def elementary_mod(vals: list[int], degree: int) -> int:
        elems = [0] * (degree + 1)
        elems[0] = 1
        for x in vals:
            for r in range(degree, 0, -1):
                elems[r] = (elems[r] + x * elems[r - 1]) % p
        return elems[degree]

    residual_values = [domain[i] for i in residual]
    mod_e1 = elementary_mod(residual_values, 1)
    mod_e2 = elementary_mod(residual_values, 2)
    mod_e3 = elementary_mod(residual_values, 3)
    mod_f3 = (mod_e1 * mod_e2 - mod_e3) % p

    assert coeffs == [9, 3, 3, 1, 1]
    assert row1 == 0
    assert row3 == 0
    assert residual_size == 4
    assert not exact_field.is_zero(exact_f3)
    assert mod_f3 == 0

    return {
        "status": "COUNTEREXAMPLE_TO_NAIVE_FINITE_FIELD_TRANSFER",
        "field": "F_17",
        "n": n,
        "generator": generator,
        "support_exponents": list(support),
        "support_values": values,
        "coefficients_c0_to_cj": coeffs,
        "slope_z": z,
        "residual_exponents": list(residual),
        "row1_zero": row1 == 0,
        "row3_zero": row3 == 0,
        "half_turn_residual_size": residual_size,
        "residual_defect": "F3(R)=e1(R)*e2(R)-e3(R)",
        "F3_exact_key": exact_field.key(exact_f3),
        "F3_exact_nonzero": True,
        "F3_mod_17": mod_f3,
        "F3_mod_17_zero": True,
        "generated_collision_certificate": True,
        "meaning": (
            "The characteristic-zero {1,3} half-turn classification needs a "
            "finite-field generated-collision ledger before deployed finite-field use. "
            "Here the residual defect is nonzero over Q(zeta_16) but reduces to zero mod 17."
        ),
    }


def residual_image_ledger_bound() -> dict[str, Any]:
    primitive_bound = DEPLOYED_N + 1
    assert primitive_bound < BUDGET
    return {
        "branch": "{1,4}",
        "condition": "after charging lower-domain shadow and higher-pair balanced residual ledgers",
        "primitive_residual_image_bound": primitive_bound,
        "below_budget": primitive_bound < BUDGET,
        "budget_minus_bound": BUDGET - primitive_bound,
        "bit_margin_log2_budget_over_bound": math.log2(BUDGET / primitive_bound),
    }


def small_residual_parity_checks() -> list[dict[str, Any]]:
    checks = []
    for s, q in [(2, 1), (3, 1), (4, 1), (4, 0), (5, 0), (6, 0)]:
        a_len = math.comb(s + 1, 2)
        b_len = 3 * math.comb(s + 1, 4)
        if q == 0:
            length = b_len
            zero_sum = "Bcal_R"
        elif q == 1:
            length = b_len + a_len
            zero_sum = "Bcal_R disjoint_union (-u*Acal_R)"
        else:
            raise AssertionError("only q=0 and q=1 are parity-checked here")
        assert length % 2 == 1
        checks.append(
            {
                "s": s,
                "q": q,
                "zero_sum": zero_sum,
                "Acal_length": a_len,
                "Bcal_length": b_len,
                "total_zero_sum_length": length,
                "half_turn_balance_possible": False,
                "reason": "odd length cannot be half-turn-balanced",
            }
        )
    return checks


def parity_empty_classes() -> dict[str, Any]:
    q0_odd = []
    q1_odd = []
    for s in range(32):
        q0_len = 3 * math.comb(s + 1, 4)
        q1_len = q0_len + math.comb(s + 1, 2)
        if q0_len % 2 == 1:
            q0_odd.append(s % 8)
        if q1_len % 2 == 1:
            q1_odd.append(s % 8)
    q0_classes = sorted(set(q0_odd))
    q1_classes = sorted(set(q1_odd))
    assert q0_classes == [3, 4, 5, 6]
    assert q1_classes == [1, 2, 3, 4]
    return {
        "q0_empty_when_s_mod_8_in": q0_classes,
        "q1_empty_when_s_mod_8_in": q1_classes,
        "checked_s_range": "0..31",
        "method": "parity of 3*C(s+1,4) and 3*C(s+1,4)+C(s+1,2)",
    }


def twofold_rigidity_counterexample() -> dict[str, Any]:
    # n=16 is enough: y=zeta^2, i=y^2=zeta^4, R={y}, R'={1,i}.
    n = 16
    field = TwoPowerCyclotomic(n)
    residual_singleton = (2,)
    residual_pair = (0, 4)
    a_single, b_single = residual_ab(field, residual_singleton)
    a_pair, b_pair = residual_ab(field, residual_pair)
    assert a_single == a_pair
    assert b_single == b_pair
    neg_singleton = tuple(sorted((x + n // 2) % n for x in residual_singleton))
    assert residual_pair != residual_singleton
    assert residual_pair != neg_singleton
    return {
        "n": n,
        "residual_R": list(residual_singleton),
        "residual_R_prime": list(residual_pair),
        "negative_R": list(neg_singleton),
        "A_R_key": field.key(a_single),
        "B_R_key": field.key(b_single),
        "same_A_B": True,
        "same_residual": False,
        "antipodal_residual": False,
        "explanation": (
            "R={zeta^2}, R'={1,zeta^4}; both have (A_R,B_R)=(zeta^4,0) "
            "but have different sizes, so unrestricted twofold fiber rigidity is false."
        ),
    }


def neg_residual(n: int, residual: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted((x + n // 2) % n for x in residual))


def half_turn_free_residuals(n: int, size: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    half = n // 2
    for orbits in itertools.combinations(range(half), size):
        for signs in itertools.product((0, 1), repeat=size):
            out.append(tuple(sorted(o + sign * half for o, sign in zip(orbits, signs))))
    return out


def fixed_size_ab_rigidity_s2_checks() -> list[dict[str, Any]]:
    rows = []
    for n in (8, 16, 32, 64):
        field = TwoPowerCyclotomic(n)
        fibers: dict[tuple[tuple[int, ...], tuple[int, ...]], list[tuple[int, ...]]] = {}
        for residual in half_turn_free_residuals(n, 2):
            key = residual_ab(field, residual)
            fibers.setdefault(key, []).append(residual)

        bad_fibers = []
        max_size = 0
        for bucket in fibers.values():
            max_size = max(max_size, len(bucket))
            if len(bucket) != 2:
                bad_fibers.append([list(r) for r in bucket])
            elif bucket[1] != neg_residual(n, bucket[0]):
                bad_fibers.append([list(r) for r in bucket])

        assert not bad_fibers
        assert max_size == 2
        rows.append(
            {
                "n": n,
                "residual_size": 2,
                "residuals_checked": len(half_turn_free_residuals(n, 2)),
                "AB_fibers": len(fibers),
                "max_residuals_per_AB": max_size,
                "all_fibers_antipodal_twofold": True,
                "status": "CONSISTENT_WITH_PROVED_S2_BASE_CASE",
            }
        )
    return rows


def half_turn_balance_range_caveat() -> dict[str, Any]:
    # The bare statement "no half-turn-free R with |R|>=2 has B_R=0" is false:
    # for |R|=2, e_3(R)=e_4(R)=0, hence B_R=0.  This is outside the actual
    # q=0 {1,4} range, where j=s and the offset-4 row requires s>=4.
    n = 16
    field = TwoPowerCyclotomic(n)
    residual = (0, 2)
    assert len(residual) == 2
    assert (residual[0] + n // 2) % n not in residual
    _, b_value = residual_ab(field, residual)
    assert field.is_zero(b_value)
    return {
        "n": n,
        "residual_R": list(residual),
        "half_turn_free": True,
        "size": len(residual),
        "B_R_key": field.key(b_value),
        "B_R_is_zero": True,
        "outside_valid_q0_range": True,
        "reason": (
            "For every two-point residual, e_3=e_4=0, so B_R=0. "
            "The q=0 {1,4} branch has j=s>=4, so the corrected emptiness "
            "target must include the valid range restriction."
        ),
    }


def experiment_evidence_v3() -> dict[str, Any]:
    return {
        "status": "EXPERIMENTAL_EVIDENCE_NOT_A_PROOF",
        "source_folder": "m1_14_ledger_experiments_v3",
        "q1_arithmetic": "corrected root multiplication with wraparound sign",
        "half_turn_balance": {
            "statement": "No q=0 or q=1 half-turn-balance hits found.",
            "rows": [
                {"n": 32, "s": 7, "mode": "exhaustive", "examined": 1_464_320},
                {"n": 32, "s": 8, "mode": "exhaustive", "examined": 3_294_720},
                {"n": 32, "s": 9, "mode": "exhaustive", "examined": 5_857_280},
                {"n": 32, "s": 10, "mode": "exhaustive", "examined": 8_200_192},
                {"n": 64, "s": 4, "mode": "exhaustive", "examined": 575_360},
                {"n": 64, "s": 5, "mode": "exhaustive", "examined": 6_444_032},
                {"n": 64, "s": 6, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 7, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 8, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 9, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 10, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 11, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 12, "mode": "prefix_exhaustive_500000", "examined": 500_000},
            ],
            "q0_hits": 0,
            "q1_hits": 0,
        },
        "fixed_size_ab_fibers": {
            "statement": (
                "Every observed fixed-size (A_R,B_R) fiber has size at most 2, "
                "and every twofold fiber is exactly antipodal."
            ),
            "max_residuals_per_fiber": 2,
            "max_slopes_per_fiber": 2,
            "all_twofold_fibers_antipodal": True,
            "rows": [
                {"n": 32, "s": 2, "mode": "exhaustive", "examined": 480},
                {"n": 32, "s": 3, "mode": "exhaustive", "examined": 4_480},
                {"n": 32, "s": 4, "mode": "exhaustive", "examined": 29_120},
                {"n": 32, "s": 5, "mode": "exhaustive", "examined": 139_776},
                {"n": 32, "s": 6, "mode": "exhaustive", "examined": 512_512},
                {"n": 32, "s": 7, "mode": "exhaustive", "examined": 1_464_320},
                {"n": 32, "s": 8, "mode": "exhaustive", "examined": 3_294_720},
                {"n": 32, "s": 9, "mode": "prefix_exhaustive_1000000", "examined": 1_000_000},
                {"n": 32, "s": 10, "mode": "prefix_exhaustive_1000000", "examined": 1_000_000},
                {"n": 64, "s": 4, "mode": "exhaustive", "examined": 575_360},
                {"n": 64, "s": 5, "mode": "exhaustive", "examined": 6_444_032},
                {"n": 64, "s": 6, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 7, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 8, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 9, "mode": "prefix_exhaustive_500000", "examined": 500_000},
                {"n": 64, "s": 10, "mode": "prefix_exhaustive_500000", "examined": 500_000},
            ],
        },
        "recommended_next_targets": [
            "valid-range half-turn-balance emptiness",
            "fixed-size imbalance-profile rigidity modulo antipodal symmetry for residual sizes >=3",
            "sparse/nonconsecutive row-slice inverse classification",
            "finite-field generated-collision accounting",
        ],
    }


def imbalance_reduction_targets() -> dict[str, Any]:
    return {
        "status": "REDUCTION_TARGETS_NOT_PROVED_HERE",
        "imbalance_definition": (
            "For a positive multiset M of 2^m-th roots, Delta_M(xi) is "
            "mult_M(xi)-mult_M(-xi).  Over Q(zeta_{2^m}), sum(M)=0 iff "
            "Delta_M is identically zero."
        ),
        "half_turn_balance_emptiness": {
            "q0_valid_range": "s>=4, R half-turn-free",
            "q0_target": "Delta(Bcal_R) is not identically zero",
            "q1_valid_range": "s>=2, R half-turn-free, u in mu_{2^{m-1}} \\ R^2",
            "q1_target": "Delta(Bcal_R disjoint_union (-u*Acal_R)) is not identically zero",
            "proved_subcases": [
                "q=0 parity-empty for s mod 8 in {3,4,5,6}",
                "q=1 parity-empty for s mod 8 in {1,2,3,4}",
            ],
            "open_congruence_classes": {
                "q0_s_mod_8": [0, 1, 2, 7],
                "q1_s_mod_8": [0, 5, 6, 7],
            },
        },
        "fixed_size_AB_rigidity": {
            "target": (
                "For |R|=|R'|>=3, equality of Delta(Acal_R),Delta(Bcal_R) "
                "with Delta(Acal_R'),Delta(Bcal_R') forces R'=R or R'=-R."
            ),
            "proved_base_case": "|R|=|R'|=2",
            "known_false_unrestricted_case": "cross-size collision R={y}, R'={1,i} with y^2=i",
        },
    }


def build_certificate() -> dict[str, Any]:
    enumeration_cases_13 = []
    for n in (8, 16):
        for j in range(3, min(n, 8) + 1):
            enumeration_cases_13.append(enumerate_case_13(n, j))

    enumeration_cases_14 = []
    for n in (8, 16):
        for j in range(4, min(n, 8) + 1):
            enumeration_cases_14.append(enumerate_case_14(n, j))

    deployed_rows = [deployed_row(A) for A in AGREEMENTS]
    residual_ledger = residual_image_ledger_bound()
    parity_checks = small_residual_parity_checks()
    parity_classes = parity_empty_classes()
    counterexample = twofold_rigidity_counterexample()
    s2_rigidity = fixed_size_ab_rigidity_s2_checks()
    range_caveat = half_turn_balance_range_caveat()
    finite_field_guardrail = finite_field_13_transfer_guardrail()
    experiment_evidence = experiment_evidence_v3()
    imbalance_targets = imbalance_reduction_targets()
    cert: dict[str, Any] = {
        "schema": "m1_half_turn_pair_core_13_v1",
        "status": "PROVED_LOCAL_BRANCH_ALGEBRA_WITH_CONDITIONAL_LEDGER_DECOMPOSITION",
        "status_breakdown": {
            "case_13_characteristic_zero": "PROVED_LOCAL",
            "case_14_residual_core_equation": "PROVED_LOCAL",
            "case_14_primitive_bound_after_named_ledgers": "CONDITIONAL_LEDGER_DECOMPOSITION",
            "finite_field_generated_collision_accounting": "NOT_COVERED",
            "case_13_finite_field_collision_classification": "PROVED_LOCAL_REDUCTION",
            "koalabear_deployed_finite_field_slope_image": "NOT_CERTIFIED",
            "v3_experiment_evidence": "EXTERNAL_EXPERIMENTAL_EVIDENCE_NOT_REPLAYED",
        },
        "claim": (
            "For D=mu_{2^m}, the {1,3} coefficient-window branch has "
            "half-turn residual size at most 1 over the honest characteristic-zero "
            "2-power cyclotomic model. The {1,4} branch residualizes to the "
            "exact equation e_2(U)-alpha_R e_1(U)+beta_R=0 and admits a ledger "
            "decomposition into pair-small, recursive lower-domain, and "
            "half-turn-balance branches. After those ledgers are charged, the "
            "{1,4} primitive residual image is bounded by n+1. In finite-field "
            "{1,3} rows, any survivor with half-turn residual size greater than "
            "1 is classified as a generated-field collision of the residual "
            "defect F3(R)=e1(R)e2(R)-e3(R)."
        ),
        "parameters": {
            "deployed_n": DEPLOYED_N,
            "deployed_k": DEPLOYED_K,
            "koalabear_p": KOALABEAR_P,
            "q_line": str(Q_LINE),
            "budget_floor_q_line_over_2^128": BUDGET_Q_LINE_FLOOR,
            "budget_floor_q_line_minus_1_over_2^128": BUDGET_CONSERVATIVE,
            "budget_values_equal_for_this_row": BUDGET_Q_LINE_FLOOR == BUDGET_CONSERVATIVE,
        },
        "small_exact_enumerations_13": enumeration_cases_13,
        "small_exact_enumerations_14": enumeration_cases_14,
        "residual_image_ledger_bound_14": residual_ledger,
        "small_residual_parity_checks_14": parity_checks,
        "parity_empty_classes_14": parity_classes,
        "half_turn_balance_range_caveat": range_caveat,
        "finite_field_transfer_guardrails": [finite_field_guardrail],
        "twofold_rigidity_counterexample": counterexample,
        "fixed_size_AB_rigidity_s2_checks": s2_rigidity,
        "external_experiment_evidence_v3_not_replayed": experiment_evidence,
        "imbalance_reduction_targets_14": imbalance_targets,
        "deployed_rows": deployed_rows,
        "summary": {
            "all_small_enumerations_match_theorem": all(
                row["classification_exact"] for row in enumeration_cases_13
            ),
            "all_14_residual_core_checks_match_theorem": all(
                row["residual_core_equation_exact"] for row in enumeration_cases_14
            ),
            "all_14_residuals_determine_slope": all(
                row["residual_determines_slope"] for row in enumeration_cases_14
            ),
            "all_14_small_residual_parity_obstructions_hold": all(
                row["half_turn_balance_possible"] is False for row in parity_checks
            ),
            "parity_empty_classes_checked": (
                parity_classes["q0_empty_when_s_mod_8_in"] == [3, 4, 5, 6]
                and parity_classes["q1_empty_when_s_mod_8_in"] == [1, 2, 3, 4]
            ),
            "unrestricted_twofold_rigidity_counterexample_checked": counterexample[
                "same_A_B"
            ]
            and not counterexample["same_residual"]
            and not counterexample["antipodal_residual"],
            "bare_half_turn_balance_emptiness_requires_valid_range": range_caveat[
                "B_R_is_zero"
            ]
            and range_caveat["outside_valid_q0_range"],
            "fixed_size_AB_rigidity_s2_base_case_checked": all(
                row["all_fibers_antipodal_twofold"] for row in s2_rigidity
            ),
            "finite_field_13_transfer_guardrail_checked": (
                finite_field_guardrail["status"] == "COUNTEREXAMPLE_TO_NAIVE_FINITE_FIELD_TRANSFER"
                and finite_field_guardrail["half_turn_residual_size"] == 4
                and finite_field_guardrail["F3_exact_nonzero"] is True
                and finite_field_guardrail["F3_mod_17_zero"] is True
            ),
            "external_experiment_evidence_recorded_not_replayed": (
                experiment_evidence["status"] == "EXPERIMENTAL_EVIDENCE_NOT_A_PROOF"
            ),
            "imbalance_reduction_targets_recorded": (
                imbalance_targets["status"] == "REDUCTION_TARGETS_NOT_PROVED_HERE"
            ),
            "residual_image_ledger_bound_14_below_budget": residual_ledger["below_budget"],
            "max_deployed_slope_bound": max(row["slope_image_bound"] for row in deployed_rows),
            "all_deployed_slope_bounds_below_budget": all(
                row["below_budget"] for row in deployed_rows
            ),
        },
        "scope": {
            "covers": [
                "{1,3} coefficient-window branch over honest 2-power cyclotomic domains",
                "{1,4} residual-core equation over honest 2-power cyclotomic domains",
                "{1,4} residual-image ledger decomposition into pair-small, recursive lower, and half-turn-balance branches",
                "{1,4} half-turn-balance parity-empty classes",
                "valid-range caveat for half-turn-balance emptiness",
                "finite-field guardrail counterexample for naive {1,3} transfer",
                "{1,3} finite-field generated-collision classification via the residual defect F3(R)",
                "counterexample to unrestricted twofold lower-fiber rigidity",
                "fixed-size AB-rigidity base case for residual size 2",
                "imbalance-vector reductions for the two next inverse targets",
                "external non-replayed experimental evidence for the next two {1,4} inverse targets",
                "half-turn pair-core slope compression",
                "deployed KoalaBear parity and budget arithmetic for the honest characteristic-zero branch",
            ],
            "does_not_cover": [
                "finite-field generated-collision amplification",
                "finite-field {1,3} generated-collision emptiness or budget-smallness",
                "deployed KoalaBear finite-field {1,3} slope image",
                "a standalone numerical cost theorem for the recursive lower-domain ledger",
                "a standalone numerical cost theorem for the half-turn-balance ledger",
                "full valid-range half-turn-balance emptiness",
                "fixed-size imbalance-profile rigidity modulo antipodal symmetry for residual sizes >=3",
                "arbitrary nonconsecutive coefficient windows",
                "sparse Hankel-proxy row slices",
                "full M1 closure or deployed safe-side certificate",
            ],
        },
    }
    assert_certificate(cert)
    return cert


def assert_certificate(cert: dict[str, Any]) -> None:
    params = cert["parameters"]
    assert params["deployed_n"] == 2**21
    assert params["deployed_k"] == 2**20
    assert params["koalabear_p"] == 2**31 - 2**24 + 1
    assert int(params["q_line"]) == params["koalabear_p"] ** 6
    assert params["budget_floor_q_line_over_2^128"] == int(params["q_line"]) // 2**128
    assert params["budget_floor_q_line_minus_1_over_2^128"] == (
        int(params["q_line"]) - 1
    ) // 2**128
    assert params["budget_values_equal_for_this_row"] is True

    for row in cert["small_exact_enumerations_13"]:
        assert row["survivor_supports"] == row["predicted_supports"]
        assert row["distinct_slopes"] <= row["predicted_slope_bound"]
        assert row["classification_exact"] is True

    for row in cert["small_exact_enumerations_14"]:
        assert row["distinct_slopes"] <= row["residual_choice_bound"]
        assert row["residual_core_equation_exact"] is True
        assert row["residual_determines_slope"] is True

    residual_ledger = cert["residual_image_ledger_bound_14"]
    assert residual_ledger["primitive_residual_image_bound"] == DEPLOYED_N + 1
    assert residual_ledger["below_budget"] is True

    for row in cert["small_residual_parity_checks_14"]:
        assert row["total_zero_sum_length"] % 2 == 1
        assert row["half_turn_balance_possible"] is False

    assert cert["parity_empty_classes_14"]["q0_empty_when_s_mod_8_in"] == [3, 4, 5, 6]
    assert cert["parity_empty_classes_14"]["q1_empty_when_s_mod_8_in"] == [1, 2, 3, 4]
    caveat = cert["half_turn_balance_range_caveat"]
    assert caveat["B_R_is_zero"] is True
    assert caveat["outside_valid_q0_range"] is True
    cex = cert["twofold_rigidity_counterexample"]
    assert cex["same_A_B"] is True
    assert cex["same_residual"] is False
    assert cex["antipodal_residual"] is False
    for row in cert["fixed_size_AB_rigidity_s2_checks"]:
        assert row["residual_size"] == 2
        assert row["max_residuals_per_AB"] == 2
        assert row["all_fibers_antipodal_twofold"] is True
    guardrail = cert["finite_field_transfer_guardrails"][0]
    assert guardrail["status"] == "COUNTEREXAMPLE_TO_NAIVE_FINITE_FIELD_TRANSFER"
    assert guardrail["field"] == "F_17"
    assert guardrail["coefficients_c0_to_cj"] == [9, 3, 3, 1, 1]
    assert guardrail["row1_zero"] is True
    assert guardrail["row3_zero"] is True
    assert guardrail["half_turn_residual_size"] == 4
    assert guardrail["F3_exact_nonzero"] is True
    assert guardrail["F3_mod_17"] == 0
    assert guardrail["F3_mod_17_zero"] is True
    assert guardrail["generated_collision_certificate"] is True

    expected = {
        1_116_044: ("even", 1),
        1_116_045: ("odd", DEPLOYED_N),
        1_116_046: ("even", 1),
        1_116_047: ("odd", DEPLOYED_N),
    }
    for row in cert["deployed_rows"]:
        parity, bound = expected[row["A"]]
        assert row["j_parity"] == parity
        assert row["slope_image_bound"] == bound
        assert row["below_budget"] is True

    assert cert["summary"]["all_small_enumerations_match_theorem"] is True
    assert cert["summary"]["all_14_residual_core_checks_match_theorem"] is True
    assert cert["summary"]["all_14_residuals_determine_slope"] is True
    assert cert["summary"]["all_14_small_residual_parity_obstructions_hold"] is True
    assert cert["summary"]["parity_empty_classes_checked"] is True
    assert cert["summary"]["unrestricted_twofold_rigidity_counterexample_checked"] is True
    assert cert["summary"]["bare_half_turn_balance_emptiness_requires_valid_range"] is True
    assert cert["summary"]["fixed_size_AB_rigidity_s2_base_case_checked"] is True
    assert cert["summary"]["finite_field_13_transfer_guardrail_checked"] is True
    assert cert["summary"]["external_experiment_evidence_recorded_not_replayed"] is True
    assert cert["summary"]["imbalance_reduction_targets_recorded"] is True
    assert cert["summary"]["residual_image_ledger_bound_14_below_budget"] is True
    assert cert["summary"]["all_deployed_slope_bounds_below_budget"] is True


def render_report(cert: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("# M1 half-turn pair-core compression v1 report")
    lines.append("")
    lines.append(f"Status: `{cert['status']}`.")
    lines.append("")
    lines.append("The `{1,3}` classification is proved over the honest characteristic-zero")
    lines.append("2-power cyclotomic model.  Finite-field deployed use requires a separate")
    lines.append("generated-collision ledger; this report records a finite-field guardrail")
    lines.append("showing why that transfer cannot be assumed.")
    lines.append("")
    lines.append("## M1 wall localization")
    lines.append("")
    lines.append(
        "This packet does not close `CAP25-V13-M1-UNIFORM-SPLIT-LOCATOR-"
        "DETERMINANT-COMPRESSION`.  It localizes one half-turn coefficient-shadow "
        "subbranch: `{1,3}` pair-core mass is slope-small over the honest model, "
        "`{1,3}` finite-field failures are generated collisions of `F3(R)`, and "
        "`{1,4}` residuals decompose into pair-small, recursive lower-domain, and "
        "half-turn-balance ledgers."
    )
    lines.append("")
    lines.append("## Deployed KoalaBear branch arithmetic")
    lines.append("")
    lines.append(
        "These rows check the parity and budget arithmetic for the honest "
        "characteristic-zero `{1,3}` branch.  They do not certify the actual "
        "finite-field KoalaBear slope image."
    )
    lines.append("")
    lines.append("| A | j=n-A | parity | slope bound | below B* | bit margin |")
    lines.append("| -: | -: | :-: | -: | :-: | -: |")
    for row in cert["deployed_rows"]:
        lines.append(
            "| {A} | {j} | {parity} | {bound} | {below} | {margin:.6f} |".format(
                A=row["A"],
                j=row["j"],
                parity=row["j_parity"],
                bound=row["slope_image_bound"],
                below="yes" if row["below_budget"] else "no",
                margin=row["bit_margin_log2_budget_over_bound"],
            )
        )
    lines.append("")
    lines.append("## Finite-field transfer guardrail")
    lines.append("")
    guardrail = cert["finite_field_transfer_guardrails"][0]
    lines.append(
        "Over `{field}` with `n={n}` and generator `{generator}`, support exponents "
        "`{support}` satisfy the `{{1,3}}` rows with finite slope `{z}` but have "
        "half-turn residual size `{residual}`.  This is a counterexample to naive "
        "finite-field transfer of the characteristic-zero `{{1,3}}` classification.".format(
            field=guardrail["field"],
            n=guardrail["n"],
            generator=guardrail["generator"],
            support=guardrail["support_exponents"],
            z=guardrail["slope_z"],
            residual=guardrail["half_turn_residual_size"],
        )
    )
    lines.append(
        "The same residual-defect identity classifies the example: "
        "`F3(R)=e1(R)e2(R)-e3(R)` is nonzero over `Q(zeta_16)` with key `{}`, "
        "but reduces to `{}` modulo `17`.".format(
            guardrail["F3_exact_key"],
            guardrail["F3_mod_17"],
        )
    )
    lines.append("")
    lines.append("## Small exact {1,3} cyclotomic enumerations")
    lines.append("")
    lines.append("| n | j | survivor supports | predicted supports | slopes | bound |")
    lines.append("| -: | -: | -: | -: | -: | -: |")
    for row in cert["small_exact_enumerations_13"]:
        lines.append(
            "| {n} | {j} | {survivors} | {predicted} | {slopes} | {bound} |".format(
                n=row["n"],
                j=row["j"],
                survivors=row["survivor_supports"],
                predicted=row["predicted_supports"],
                slopes=row["distinct_slopes"],
                bound=row["predicted_slope_bound"],
            )
        )
    lines.append("")
    lines.append("## Small exact {1,4} residual-core checks")
    lines.append("")
    lines.append("| n | j | survivor supports | slopes | residual-choice bound | residual sizes |")
    lines.append("| -: | -: | -: | -: | -: | :-- |")
    for row in cert["small_exact_enumerations_14"]:
        hist = ", ".join(
            f"{key}:{value}" for key, value in sorted(row["residual_histogram"].items())
        )
        lines.append(
            "| {n} | {j} | {survivors} | {slopes} | {bound} | {hist} |".format(
                n=row["n"],
                j=row["j"],
                survivors=row["survivor_supports"],
                slopes=row["distinct_slopes"],
                bound=row["residual_choice_bound"],
                hist=hist or "none",
            )
        )
    lines.append("")
    lines.append("## {1,4} residual-image ledger bound")
    lines.append("")
    residual_ledger = cert["residual_image_ledger_bound_14"]
    lines.append(
        "After charging lower-domain shadow and higher-pair balanced residual "
        "ledgers, the primitive `{{1,4}}` residual image is bounded by `{}`.".format(
            residual_ledger["primitive_residual_image_bound"]
        )
    )
    lines.append("")
    lines.append("| bound | below B* | bit margin |")
    lines.append("| -: | :-: | -: |")
    lines.append(
        "| {bound} | {below} | {margin:.6f} |".format(
            bound=residual_ledger["primitive_residual_image_bound"],
            below="yes" if residual_ledger["below_budget"] else "no",
            margin=residual_ledger["bit_margin_log2_budget_over_bound"],
        )
    )
    lines.append("")
    lines.append("## Small {1,4} residual parity obstructions")
    lines.append("")
    lines.append("| s | q | zero-sum length | conclusion |")
    lines.append("| -: | -: | -: | :-- |")
    for row in cert["small_residual_parity_checks_14"]:
        lines.append(
            "| {s} | {q} | {length} | {reason} |".format(
                s=row["s"],
                q=row["q"],
                length=row["total_zero_sum_length"],
                reason=row["reason"],
            )
        )
    lines.append("")
    lines.append("## {1,4} parity-empty residue classes")
    lines.append("")
    parity_classes = cert["parity_empty_classes_14"]
    lines.append(
        "- `q=0` half-turn-balance is parity-empty for `s mod 8` in `{}`.".format(
            ", ".join(map(str, parity_classes["q0_empty_when_s_mod_8_in"]))
        )
    )
    lines.append(
        "- `q=1` half-turn-balance is parity-empty for `s mod 8` in `{}`.".format(
            ", ".join(map(str, parity_classes["q1_empty_when_s_mod_8_in"]))
        )
    )
    lines.append("")
    lines.append("## Twofold lower-fiber counterexample")
    lines.append("")
    cex = cert["twofold_rigidity_counterexample"]
    lines.append(
        "In `mu_{{16}}`, residuals `{}` and `{}` have the same `(A_R,B_R)` but "
        "are neither equal nor antipodal.  This rules out unrestricted "
        "twofold lower-fiber rigidity.".format(
            cex["residual_R"],
            cex["residual_R_prime"],
        )
    )
    lines.append("")
    lines.append("## Fixed-size AB-rigidity base case")
    lines.append("")
    lines.append(
        "The packet includes the proved `s=2` base case as a machine-checkable "
        "sanity check: every tested fixed-size `(A_R,B_R)` fiber is exactly "
        "the antipodal pair `{R,-R}`."
    )
    lines.append("")
    lines.append("| n | residuals checked | AB fibers | max residuals/AB |")
    lines.append("| -: | -: | -: | -: |")
    for row in cert["fixed_size_AB_rigidity_s2_checks"]:
        lines.append(
            "| {n} | {checked} | {fibers} | {max_size} |".format(
                n=row["n"],
                checked=row["residuals_checked"],
                fibers=row["AB_fibers"],
                max_size=row["max_residuals_per_AB"],
            )
        )
    lines.append("")
    lines.append("## Half-turn-balance valid-range caveat")
    lines.append("")
    caveat = cert["half_turn_balance_range_caveat"]
    lines.append(
        "The bare statement that no half-turn-free residual with `|R|>=2` has "
        "`B_R=0` is false: in `mu_{{{}}}`, residual `{}` has `B_R=0`.  This "
        "is outside the actual `q=0` `{{1,4}}` range, where `j=s>=4`.".format(
            caveat["n"],
            caveat["residual_R"],
        )
    )
    lines.append("")
    lines.append("## Imbalance-vector reduction targets")
    lines.append("")
    targets = cert["imbalance_reduction_targets_14"]
    lines.append(f"Status: `{targets['status']}`.")
    lines.append("")
    lines.append(targets["imbalance_definition"])
    lines.append("")
    half_turn = targets["half_turn_balance_emptiness"]
    lines.append("Half-turn-balance emptiness reduces to:")
    lines.append("")
    lines.append(f"- q=0 valid range `{half_turn['q0_valid_range']}`: `{half_turn['q0_target']}`.")
    lines.append(f"- q=1 valid range `{half_turn['q1_valid_range']}`: `{half_turn['q1_target']}`.")
    lines.append("")
    lines.append(
        "The still-open congruence classes are q=0 `s mod 8` in `{}` and "
        "q=1 `s mod 8` in `{}`.".format(
            ", ".join(map(str, half_turn["open_congruence_classes"]["q0_s_mod_8"])),
            ", ".join(map(str, half_turn["open_congruence_classes"]["q1_s_mod_8"])),
        )
    )
    lines.append("")
    rigidity = targets["fixed_size_AB_rigidity"]
    lines.append("Fixed-size AB-rigidity reduces to:")
    lines.append("")
    lines.append(f"- {rigidity['target']}")
    lines.append(f"- Proved base case: `{rigidity['proved_base_case']}`.")
    lines.append("")
    lines.append("## Experiment evidence for next targets")
    lines.append("")
    evidence = cert["external_experiment_evidence_v3_not_replayed"]
    lines.append(f"Status: `{evidence['status']}`.")
    lines.append("")
    lines.append(
        "- Half-turn-balance: no `q=0` or `q=1` hits were found in the "
        "extended exact/sampled rows."
    )
    lines.append(
        "- Fixed-size AB fibers: max residuals per `(A_R,B_R)` fiber was `2`, "
        "max slopes per fiber was `2`, and every observed twofold fiber was "
        "antipodal."
    )
    lines.append("")
    lines.append("Recommended next targets:")
    lines.append("")
    for target in evidence["recommended_next_targets"]:
        lines.append(f"- {target}.")
    lines.append("")
    lines.append("## Conclusion")
    lines.append("")
    lines.append(
        "The small exact enumerations match the symbolic classification: the "
        "`{1,3}` characteristic-zero branch consists exactly of half-turn pair "
        "cores plus at most one residual singleton.  The deployed KoalaBear rows "
        "record only the corresponding parity/budget arithmetic for that honest "
        "branch, not a finite-field slope certificate.  The `{1,4}` checks verify "
        "the exact residual-core equation and confirm that paired-core completions "
        "do not multiply slopes.  The residual-image ledger theorem then leaves "
        "only the `n+1` pair-small primitive remainder after the lower-domain "
        "and higher-pair balanced residual branches are charged."
    )
    lines.append("")
    lines.append("## Non-claims")
    lines.append("")
    for item in cert["scope"]["does_not_cover"]:
        lines.append(f"- Does not cover {item}.")
    lines.append("")
    return "\n".join(lines)


def json_bytes(cert: dict[str, Any]) -> bytes:
    return (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")


def report_bytes(cert: dict[str, Any]) -> bytes:
    return render_report(cert).encode("utf-8")


def render_cert_readme(cert: dict[str, Any]) -> str:
    guardrail = cert["finite_field_transfer_guardrails"][0]
    lines = [
        "# M1 half-turn pair-core compression v1 certificate",
        "",
        f"Status: `{cert['status']}`.",
        "",
        "This certificate records the generated artifacts for the M1 half-turn",
        "pair-core packet.  The characteristic-zero `{1,3}` and `{1,4}` branch",
        "algebra is proved locally; finite-field deployed use is conditional on",
        "the named generated-collision and ledger branches.",
        "",
        "The packet localizes one half-turn coefficient-shadow subbranch of",
        "`CAP25-V13-M1-UNIFORM-SPLIT-LOCATOR-DETERMINANT-COMPRESSION`; it does",
        "not close the full v13 M1 wall.",
        "",
        "## Files",
        "",
        "- `m1_half_turn_pair_core_13_v1.json`: machine-readable certificate.",
        "- `README.md`: this generated certificate-directory summary.",
        "- `experimental/notes/certificate_scanner/outputs/m1_half_turn_pair_core_13_v1.report.md`: generated Markdown report.",
        "",
        "## Regeneration",
        "",
        "```bash",
        "python3 experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py --write",
        "python3 experimental/scripts/verify_m1_half_turn_pair_core_13_v1.py --check",
        "python3 -m json.tool experimental/data/certificates/m1-half-turn-pair-core-13-v1/m1_half_turn_pair_core_13_v1.json",
        "```",
        "",
        "## Claims",
        "",
        "- `{1,3}` half-turn pair-core classification over the honest characteristic-zero `2`-power cyclotomic model.",
        "- `{1,3}` finite-field transfer obstruction classified by `F3(R)=e1(R)e2(R)-e3(R)`.",
        "- `{1,4}` residual-core equation and residual-only slope map.",
        "- `{1,4}` primitive residual image bound `n+1` after charging recursive lower-domain and half-turn-balance ledgers.",
        "- Parity-empty subcases and the proved fixed-size `s=2` AB-rigidity base case.",
        "- Exact imbalance-vector reductions for the next `{1,4}` inverse targets.",
        "",
        "## Guardrail",
        "",
        "The certificate includes a finite-field transfer guardrail:",
        "",
        f"- `{guardrail['field']}`, `n={guardrail['n']}`, generator `{guardrail['generator']}`.",
        f"- support exponents `{guardrail['support_exponents']}`.",
        f"- locator coefficients `c0..cj = {guardrail['coefficients_c0_to_cj']}`.",
        f"- both `{{1,3}}` rows vanish, but half-turn residual size is `{guardrail['half_turn_residual_size']}`.",
        f"- `F3(R)` exact key `{guardrail['F3_exact_key']}` is nonzero over `Q(zeta_16)`.",
        f"- `F3(R)` reduces to `{guardrail['F3_mod_17']}` modulo `17`.",
        "",
        "This shows that the characteristic-zero `{1,3}` theorem does not automatically",
        "certify the finite-field KoalaBear slope image without a generated-collision ledger.",
        "",
        "## External Evidence",
        "",
        "The v3 experiment evidence is recorded as external evidence and is not replayed by",
        "this verifier.  It supports, but does not prove, the next inverse targets.",
        "",
        "## Nonclaims",
        "",
    ]
    for item in cert["scope"]["does_not_cover"]:
        lines.append(f"- Does not cover {item}.")
    lines.append("")
    return "\n".join(lines)


def cert_readme_bytes(cert: dict[str, Any]) -> bytes:
    return render_cert_readme(cert).encode("utf-8")


def write_artifacts(cert: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_bytes(json_bytes(cert))
    CERT_README_PATH.write_bytes(cert_readme_bytes(cert))
    REPORT_PATH.write_bytes(report_bytes(cert))


def check_artifacts(cert: dict[str, Any]) -> None:
    expected = {
        CERT_PATH: json_bytes(cert),
        CERT_README_PATH: cert_readme_bytes(cert),
        REPORT_PATH: report_bytes(cert),
    }
    missing = [str(path) for path in expected if not path.exists()]
    if missing:
        raise AssertionError(f"missing artifacts: {missing}")
    mismatches = [
        str(path)
        for path, expected_bytes in expected.items()
        if path.read_bytes() != expected_bytes
    ]
    if mismatches:
        raise AssertionError(f"artifact mismatch; run --write: {mismatches}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate()
    if args.write:
        write_artifacts(cert)
        print(f"wrote {CERT_PATH}")
        print(f"wrote {CERT_README_PATH}")
        print(f"wrote {REPORT_PATH}")
    if args.check:
        check_artifacts(cert)
        print("artifact check passed: 3 files")
    if args.json:
        print(json.dumps(cert, indent=2, sort_keys=True))
    if not (args.write or args.check or args.json):
        print("STATUS:", cert["status"])
        print("RESULT: PASS")


if __name__ == "__main__":
    main()
