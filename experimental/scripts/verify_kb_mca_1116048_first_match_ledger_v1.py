#!/usr/bin/env python3
"""Verifier for the KoalaBear MCA A=1116048 first-match ledger v1.

This packet is an accounting verifier, not a proof of primitive Q-fin
flatness.  It records the exact deployed-row constants and discharges one
proved first-match bucket:

    finite-only base/generated-field affine-row survivors
    -> row-indexed generated-slope image cells, cost <= R*p <= t*p.

All other nonprimitive branches are listed with explicit OPEN/CONDITIONAL
status and are not deducted from the proved remaining budget.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any


P = 2**31 - 2**24 + 1
N = 2**21
K = 2**20
A_ADJACENT = 1_116_048
J = N - A_ADJACENT
T = A_ADJACENT - K
W_PREFIX = T - 1
Q_LINE = P**6
B_STAR = (Q_LINE - 1) // 2**128

ROOT = Path(__file__).resolve().parents[2]
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "kb_mca_1116048_first_match_ledger_v1.md"
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "kb-mca-1116048-first-match-ledger-v1"
CERT_PATH = CERT_DIR / "kb_mca_1116048_first_match_ledger_v1.json"
CERT_README_PATH = CERT_DIR / "README.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "kb_mca_1116048_first_match_ledger_v1.report.md"
)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def log2_binom(n: int, k: int) -> float:
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / math.log(2)


@lru_cache(maxsize=1)
def deployed_binom() -> int:
    return math.comb(N, J)


@lru_cache(maxsize=1)
def deployed_p_power() -> int:
    return P**W_PREFIX


def exact_k_multiplier(budget: int) -> int:
    """Return floor(budget * p^w / binom(n,j)) for the deployed row."""

    ensure(budget >= 0, "budget must be nonnegative")
    return (budget * deployed_p_power()) // deployed_binom()


class TwoPowerCyclotomic:
    """Exact arithmetic in Q(zeta_n), n=2^m, using zeta^(n/2)=-1."""

    def __init__(self, n: int) -> None:
        ensure(n >= 4 and n & (n - 1) == 0, "n must be a 2-power >= 4")
        self.n = n
        self.half = n // 2

    def zero(self) -> tuple[int, ...]:
        return (0,) * self.half

    def one(self) -> tuple[int, ...]:
        return (1,) + (0,) * (self.half - 1)

    def root(self, exp: int) -> tuple[int, ...]:
        exp %= self.n
        sign = 1
        if exp >= self.half:
            exp -= self.half
            sign = -1
        out = [0] * self.half
        out[exp] = sign
        return tuple(out)

    def add(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(a + b for a, b in zip(left, right))

    def sub(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(a - b for a, b in zip(left, right))

    def neg(self, value: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(-a for a in value)

    def mul(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        out = [0] * self.half
        for i, a in enumerate(left):
            if not a:
                continue
            for j, b in enumerate(right):
                if not b:
                    continue
                exp = i + j
                if exp >= self.half:
                    out[exp - self.half] -= a * b
                else:
                    out[exp] += a * b
        return tuple(out)

    def is_zero(self, value: tuple[int, ...]) -> bool:
        return all(a == 0 for a in value)

    def key(self, value: tuple[int, ...]) -> str:
        return ",".join(str(a) for a in value)


def reduce_cyclotomic_mod(value: tuple[int, ...], omega: int, p: int) -> int:
    total = 0
    power = 1
    for coeff in value:
        total = (total + coeff * power) % p
        power = (power * omega) % p
    return total


def locator_coeffs_exact(field: TwoPowerCyclotomic, support: tuple[int, ...]) -> list[tuple[int, ...]]:
    coeffs = [field.one()]
    for exp in support:
        x = field.root(exp)
        new = [field.zero()] * (len(coeffs) + 1)
        for idx, coeff in enumerate(coeffs):
            new[idx] = field.sub(new[idx], field.mul(coeff, x))
            new[idx + 1] = field.add(new[idx + 1], coeff)
        coeffs = new
    return coeffs


def locator_coeffs_mod(values: list[int], p: int) -> list[int]:
    coeffs = [1]
    for x in values:
        new = [0] * (len(coeffs) + 1)
        for idx, coeff in enumerate(coeffs):
            new[idx] = (new[idx] - coeff * x) % p
            new[idx + 1] = (new[idx + 1] + coeff) % p
        coeffs = new
    return coeffs


def half_turn_residual_size(n: int, support: tuple[int, ...]) -> int:
    half = n // 2
    support_set = set(support)
    seen: set[int] = set()
    residual = 0
    for exp in support:
        if exp in seen:
            continue
        opposite = (exp + half) % n
        if opposite in support_set:
            seen.add(exp)
            seen.add(opposite)
        else:
            residual += 1
            seen.add(exp)
    return residual


def generated_collision_guardrail() -> dict[str, Any]:
    """Finite-field guardrail for the {1,3} generated-collision bucket."""

    p = 17
    n = 16
    omega = 3
    support = (0, 1, 3, 14)
    values = [pow(omega, exp, p) for exp in support]
    coeffs_mod = locator_coeffs_mod(values, p)
    j = len(support)
    slope = (-coeffs_mod[j - 1]) % p
    row1 = (coeffs_mod[j - 1] + slope * coeffs_mod[j]) % p
    row3 = (coeffs_mod[j - 3] + slope * coeffs_mod[j - 2]) % p
    g3_mod = (coeffs_mod[j - 3] - coeffs_mod[j - 1] * coeffs_mod[j - 2]) % p

    field = TwoPowerCyclotomic(n)
    coeffs_exact = locator_coeffs_exact(field, support)
    g3_exact = field.sub(
        coeffs_exact[j - 3],
        field.mul(coeffs_exact[j - 1], coeffs_exact[j - 2]),
    )
    g3_reduced = reduce_cyclotomic_mod(g3_exact, omega, p)

    ensure(row1 == 0 and row3 == 0, "finite {1,3} rows should vanish")
    ensure(g3_mod == 0 and g3_reduced == 0, "cross defect should reduce to zero")
    ensure(not field.is_zero(g3_exact), "guardrail should be finite-only, not honest")
    ensure(half_turn_residual_size(n, support) == 4, "guardrail residual size changed")

    return {
        "status": "FINITE_ONLY_GENERATED_COLLISION_GUARDRAIL",
        "field": "F_17",
        "n": n,
        "omega": omega,
        "support_exponents": list(support),
        "support_values": values,
        "locator_coefficients_c0_to_cj_mod_p": coeffs_mod,
        "forced_slope": slope,
        "row1_zero": row1 == 0,
        "row3_zero": row3 == 0,
        "half_turn_residual_size": half_turn_residual_size(n, support),
        "g3_exact_key": field.key(g3_exact),
        "g3_exact_nonzero": not field.is_zero(g3_exact),
        "g3_mod_p": g3_mod,
        "generated_cell": {"row_index": 3, "lambda": slope},
        "meaning": (
            "The support is a finite-field {1,3} survivor, but its honest "
            "cyclotomic cross-defect is nonzero and only vanishes after "
            "reduction modulo 17."
        ),
    }


def generated_prefix_support_payment_counterexample() -> dict[str, Any]:
    """Small replay showing image-cell generated-prefix labels are not support payments."""

    p = 17
    n = 16
    omega = 3
    j = 8
    w = 1
    finite_target = 1
    field = TwoPowerCyclotomic(n)
    domain = [pow(omega, exp, p) for exp in range(n)]

    exact_lift_class_counts: dict[tuple[tuple[int, ...], ...], int] = {}
    finite_fiber_size = 0
    for support in itertools.combinations(range(n), j):
        values = [domain[exp] for exp in support]
        coeffs_mod = locator_coeffs_mod(values, p)
        prefix_mod = tuple(coeffs_mod[j - d] for d in range(1, w + 1))
        if prefix_mod != (finite_target,):
            continue
        finite_fiber_size += 1
        coeffs_exact = locator_coeffs_exact(field, support)
        exact_prefix = tuple(coeffs_exact[j - d] for d in range(1, w + 1))
        ensure(
            tuple(reduce_cyclotomic_mod(value, omega, p) for value in exact_prefix) == prefix_mod,
            "exact prefix reduction mismatch",
        )
        exact_lift_class_counts[exact_prefix] = exact_lift_class_counts.get(exact_prefix, 0) + 1

    exact_lift_classes = len(exact_lift_class_counts)
    largest_exact_lift_class = max(exact_lift_class_counts.values())
    nonretained_supports = finite_fiber_size - largest_exact_lift_class
    image_cell_bound = w * p

    ensure(finite_fiber_size == 757, "generated-prefix counterexample fiber size changed")
    ensure(exact_lift_classes == 193, "generated-prefix counterexample lift-class count changed")
    ensure(largest_exact_lift_class == 20, "generated-prefix counterexample largest class changed")
    ensure(nonretained_supports == 737, "generated-prefix counterexample nonretained count changed")
    ensure(image_cell_bound == 17, "generated-prefix counterexample image-cell bound changed")
    ensure(nonretained_supports > image_cell_bound, "counterexample should exceed image-cell support bound")

    return {
        "status": "COUNTEREXAMPLE_TO_NAIVE_SUPPORT_PAYMENT_FROM_IMAGE_CELLS",
        "field": "F_17",
        "n": n,
        "omega": omega,
        "j": j,
        "w": w,
        "primitive_target": finite_target,
        "target_stabilizer_size": 1,
        "finite_fiber_size": finite_fiber_size,
        "exact_lift_classes": exact_lift_classes,
        "largest_exact_lift_class": largest_exact_lift_class,
        "nonretained_supports_after_keeping_largest_class": nonretained_supports,
        "w_times_p_image_cell_bound": image_cell_bound,
        "meaning": (
            "Every non-retained lift class is a genuine generated-prefix "
            "collision label, but the support multiplicity is much larger than "
            "the row-indexed image-cell count.  A separate support/fiber "
            "multiplicity theorem is required for finite Q2 use."
        ),
    }


def deployed_arithmetic() -> dict[str, Any]:
    log_avg = log2_binom(N, J) - W_PREFIX * math.log2(P)
    log_budget = math.log2(B_STAR)
    k_raw = exact_k_multiplier(B_STAR)
    b_gen = T * P
    b_rem_after_gen = B_STAR - b_gen
    k_after_gen = exact_k_multiplier(b_rem_after_gen)
    pair_small = N + 1
    k_after_gen_pair_small = exact_k_multiplier(b_rem_after_gen - pair_small)
    terminal_quotient_raw = math.comb(32, 14) + math.comb(16, 7)
    b_rem_after_gen_terminal_quotient = b_rem_after_gen - terminal_quotient_raw
    k_after_gen_terminal_quotient = exact_k_multiplier(b_rem_after_gen_terminal_quotient)

    ensure(P == 2_130_706_433, "KoalaBear prime mismatch")
    ensure(N == 2_097_152 and K == 1_048_576, "deployed row size mismatch")
    ensure(A_ADJACENT == 1_116_048 and J == 981_104, "deployed agreement mismatch")
    ensure(T == 67_472 and W_PREFIX == 67_471, "deployed prefix-depth mismatch")
    ensure(B_STAR == 274_980_728_111_395_087, "budget mismatch")
    ensure(k_raw == 4_807_520, "K_raw mismatch")
    ensure(b_gen == 143_763_024_447_376, "B_gen mismatch")
    ensure(b_rem_after_gen == 274_836_965_086_947_711, "B_rem after gen mismatch")
    ensure(k_after_gen == 4_805_007, "K_after_gen mismatch")
    ensure(k_after_gen_pair_small == 4_805_007, "K_after_gen_pair_small mismatch")
    ensure(terminal_quotient_raw == 471_447_040, "terminal quotient raw count mismatch")
    ensure(
        b_rem_after_gen_terminal_quotient == 274_836_964_615_500_671,
        "B_rem after terminal quotient mismatch",
    )
    ensure(k_after_gen_terminal_quotient == 4_805_007, "K_after_gen_terminal_quotient mismatch")

    return {
        "p": P,
        "q_line": Q_LINE,
        "base_generated_field_size_for_generated_cells": P,
        "line_field_size": Q_LINE,
        "B_star_floor_q_minus_1_over_2^128": B_STAR,
        "n": N,
        "k": K,
        "A_adjacent_candidate": A_ADJACENT,
        "not_certified_safe": True,
        "safe_certificate_status": "NOT_PROVED_BY_THIS_PACKET",
        "j": J,
        "t": T,
        "prefix_depth_w": W_PREFIX,
        "log2_average": log_avg,
        "log2_budget": log_budget,
        "raw_margin_bits": log_budget - log_avg,
        "K_raw": k_raw,
        "B_gen_t_times_p": b_gen,
        "B_rem_after_generated_collision": b_rem_after_gen,
        "K_after_generated_collision": k_after_gen,
        "pair_small_n_plus_1_cost": pair_small,
        "K_after_generated_collision_plus_pair_small": k_after_gen_pair_small,
        "terminal_quotient_raw_paid_cost": terminal_quotient_raw,
        "B_rem_after_generated_collision_and_terminal_quotient": b_rem_after_gen_terminal_quotient,
        "K_after_generated_collision_and_terminal_quotient": k_after_gen_terminal_quotient,
    }


def quotient_planted_rung_table(budget: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for exp in range(0, 22):
        c = 2**exp
        n_c = N // c
        j_c = J // c
        a_c = n_c - j_c
        r_c = J - c * j_c
        w_c = W_PREFIX // c
        descent_applies = r_c <= W_PREFIX
        raw_count = math.comb(n_c, j_c)
        k_c = (budget * (P**w_c)) // raw_count if raw_count else 0
        terminal_raw_paid = c in (65_536, 131_072)
        if c == 1:
            status = "TOP_PRIMITIVE_TARGET"
        elif descent_applies and c in (2, 4, 8, 16):
            status = "PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND"
        elif descent_applies and c < 65_536:
            status = "PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND"
        elif descent_applies and terminal_raw_paid:
            status = "PROVED_DESCENT_AND_RAW_PAID"
        else:
            status = "OPEN_PLANTED_TAIL_R_GREATER_THAN_W"
        rows.append(
            {
                "c": c,
                "n_c": n_c,
                "A_c": a_c,
                "j_c": j_c,
                "r_c": r_c,
                "w_c": w_c,
                "K_c_at_current_B_rem": k_c,
                "raw_quotient_count": raw_count if terminal_raw_paid else None,
                "raw_quotient_count_bit_length": raw_count.bit_length(),
                "raw_quotient_count_log2": log2_binom(n_c, j_c),
                "descent_condition_r_c_le_w": descent_applies,
                "terminal_raw_paid": terminal_raw_paid,
                "status": status,
            }
        )
    return rows


def quotient_planted_descent_block(budget: int) -> dict[str, Any]:
    rows = quotient_planted_rung_table(budget)
    terminal_rows = [row for row in rows if row["terminal_raw_paid"]]
    terminal_cost = sum(row["raw_quotient_count"] for row in terminal_rows)
    ensure(terminal_cost == 471_447_040, "terminal quotient raw cost mismatch")
    ensure([row["c"] for row in terminal_rows] == [65_536, 131_072], "terminal rung mismatch")
    open_rows = [row for row in rows if row["status"] == "OPEN_PLANTED_TAIL_R_GREATER_THAN_W"]
    ensure([row["c"] for row in open_rows] == [262_144, 524_288, 1_048_576, 2_097_152], "open rung mismatch")
    exact_quotient_rows = [
        row
        for row in rows
        if row["status"] == "PROVED_EXACT_QUOTIENT_DESCENT_NEEDS_LOWER_RUNG_BOUND"
    ]
    planted_descent_rows = [
        row
        for row in rows
        if row["status"] == "PROVED_PLANTED_DESCENT_NEEDS_LOWER_RUNG_BOUND"
    ]
    lower_obligation_rows = exact_quotient_rows + planted_descent_rows
    ensure([row["c"] for row in exact_quotient_rows] == [2, 4, 8, 16], "exact quotient rung mismatch")
    ensure(
        [row["c"] for row in planted_descent_rows]
        == [32, 64, 128, 256, 512, 1_024, 2_048, 4_096, 8_192, 16_384, 32_768],
        "planted descent rung mismatch",
    )
    ensure(len(lower_obligation_rows) == 15, "lower-rung obligation count mismatch")
    return {
        "step": "Q0",
        "name": "Q0 quotient/planted rung-margin audit",
        "status": "PROVED_DESCENT_WITH_TERMINAL_RAW_PAID_ROWS_AND_EXPLICIT_LOWER_RUNG_OBLIGATIONS",
        "theorem": "dyadic quotient/planted prefix descent",
        "condition_for_descent": "r_c <= w",
        "fiber_bound": "top c-quotient/planted fiber injects into lower Phi_{w_c} fiber",
        "audit_results": [
            (
                "Support-level quotient counting is not a valid payment route: "
                "periodic support mass is far above the MCA numerator budget."
            ),
            (
                "Image-level descent is valid for every dyadic rung with r_c<=w, "
                "which covers c=2 through c=131072 for this row."
            ),
            (
                "The terminal covered rungs c=65536 and c=131072 are already "
                "raw-paid; nonterminal covered rungs become explicit lower-rung "
                "max-fiber obligations."
            ),
            (
                "The only dyadic quotient/planted rungs not covered by this theorem "
                "are c>=262144, where the planted tail has r_c>w and is not "
                "recoverable from the top prefix."
            ),
        ],
        "exact_quotient_descent_rungs": exact_quotient_rows,
        "planted_descent_needs_lower_rung_bound": planted_descent_rows,
        "lower_rung_obligations": [
            {
                "c": row["c"],
                "n_c": row["n_c"],
                "j_c": row["j_c"],
                "w_c": row["w_c"],
                "required_multiplier_K_c": row["K_c_at_current_B_rem"],
                "target": "max_u |Phi_{w_c}^{-1}(u)| <= K_c * binom(n_c,j_c) / p^w_c",
            }
            for row in lower_obligation_rows
        ],
        "terminal_raw_paid_cost": terminal_cost,
        "terminal_raw_paid_rungs": terminal_rows,
        "open_planted_tail_rungs": open_rows,
        "open_rungs": open_rows,
        "rungs": rows,
        "nonclaims": [
            "Lower-rung max-fiber certificates are not proved for c=2..32768.",
            "Arbitrary planted tails with r_c>w remain open for c>=262144.",
            "This descent theorem is not primitive Q-fin flatness.",
        ],
    }


def honest_exact_lift_fiber_bound(k_rem: int) -> dict[str, Any]:
    terminal_order = 16
    terminal_coset_size = N // terminal_order
    max_variable_cosets = J // terminal_coset_size
    honest_bound = max(math.comb(terminal_order, q) for q in range(max_variable_cosets + 1))
    ensure(max_variable_cosets == 7, "unexpected terminal variable-coset cap")
    ensure(honest_bound == 11_440, "honest exact-lift bound mismatch")
    ensure((2**16) <= W_PREFIX < (2**17), "prefix depth power-of-two window mismatch")
    ensure(honest_bound * deployed_p_power() <= k_rem * deployed_binom(), "honest bound target comparison failed")
    return {
        "status": "PROVED_EXACT_LIFT_ONLY_NOT_DEDUCTED",
        "n": N,
        "j": J,
        "w": W_PREFIX,
        "largest_power_of_two_exponent_at_most_w": 16,
        "terminal_quotient_order": terminal_order,
        "terminal_coset_size": terminal_coset_size,
        "max_variable_terminal_cosets": max_variable_cosets,
        "honest_cyclotomic_exact_fiber_bound": honest_bound,
        "comparison_K_rem": k_rem,
        "bound_is_below_K_rem_times_average": True,
        "why_not_deducted": (
            "The exact-lift proof works after a single honest cyclotomic prefix lift is fixed. "
            "The proposed lift-class generated removal would need a valid finite-field image "
            "cost for prefix-vector lift classes; w*p row-coordinate cells do not bound the "
            "number of finite prefix values or raw supports."
        ),
    }


def split_prefix_collision_distance_block() -> dict[str, Any]:
    """Support-level rigidity for two split locators in the same prefix fiber."""

    one_sided = W_PREFIX + 1
    symmetric = 2 * one_sided
    ensure(one_sided == 67_472, "unexpected one-sided prefix collision distance")
    ensure(symmetric == 134_944, "unexpected symmetric prefix collision distance")
    ensure(one_sided < J, "distance lemma should be nonvacuous for this row")
    return {
        "status": "PROVED_SUPPORT_LEVEL_PREFIX_COLLISION_RIGIDITY",
        "statement": (
            "If two distinct j-subsets have the same first w locator-prefix "
            "coefficients, then their one-sided difference size is at least w+1."
        ),
        "parameters": {
            "j": J,
            "w": W_PREFIX,
            "minimum_one_sided_difference": one_sided,
            "minimum_symmetric_difference": symmetric,
        },
        "proof_summary": [
            "Let Lambda_S=G A and Lambda_T=G B, where G is the common split locator and deg A=deg B=e.",
            "Equality of the first w prefix coefficients gives deg(Lambda_S-Lambda_T) <= j-w-1.",
            "Since Lambda_S-Lambda_T=G(A-B), nonzero difference implies j-e+deg(A-B) <= j-w-1, hence e>=w+1.",
        ],
        "limitations": [
            "This is a pairwise support-separation lemma, not a worst-case fiber bound.",
            "Packing bounds from this distance are not strong enough to close the finite Q-fin target.",
        ],
    }


def multiplicative_order(value: int, p: int) -> int:
    ensure(value % p != 0, "zero has no multiplicative order")
    power = 1
    for order in range(1, p):
        power = (power * value) % p
        if power == 1:
            return order
    raise AssertionError("multiplicative order not found")


def q1_prefix_key_for_mask(domain: list[int], mask: int, j: int, w: int, p: int) -> tuple[int, ...]:
    values = [domain[idx] for idx in range(len(domain)) if (mask >> idx) & 1]
    ensure(len(values) == j, "mask has wrong support size")
    coeffs = locator_coeffs_mod(values, p)
    return tuple(coeffs[j - d] for d in range(1, w + 1))


@lru_cache(maxsize=None)
def prefix_buckets_for_case(p: int, n: int, omega: int, j: int, w: int) -> dict[tuple[int, ...], tuple[int, ...]]:
    ensure(multiplicative_order(omega, p) == n, "omega does not have requested order")
    domain = [pow(omega, idx, p) for idx in range(n)]
    buckets_mut: dict[tuple[int, ...], list[int]] = {}
    for combo in itertools.combinations(range(n), j):
        mask = sum(1 << idx for idx in combo)
        key = q1_prefix_key_for_mask(domain, mask, j, w, p)
        buckets_mut.setdefault(key, []).append(mask)
    return {key: tuple(values) for key, values in buckets_mut.items()}


def q1_replay_case(p: int, n: int, omega: int, j: int, w: int) -> dict[str, Any]:
    buckets = prefix_buckets_for_case(p, n, omega, j, w)

    total_supports = math.comb(n, j)
    ensure(sum(len(values) for values in buckets.values()) == total_supports, "support enumeration mismatch")
    second_moment = sum(len(values) ** 2 for values in buckets.values())
    strata: dict[int, int] = {}
    max_fiber = 0
    max_keys = 0
    for masks in buckets.values():
        if len(masks) > max_fiber:
            max_fiber = len(masks)
            max_keys = 1
        elif len(masks) == max_fiber:
            max_keys += 1
        for left in masks:
            for right in masks:
                e = j - (left & right).bit_count()
                strata[e] = strata.get(e, 0) + 1

    ensure(strata.get(0, 0) == total_supports, "diagonal stratum mismatch")
    ensure(sum(strata.values()) == second_moment, "second moment stratum mismatch")
    forbidden = {e: count for e, count in strata.items() if 0 < e <= w and count}
    ensure(not forbidden, "Q1 distance gap failed in replay")
    nontrivial = {e: count for e, count in strata.items() if e > 0 and count}
    min_nontrivial = min(nontrivial) if nontrivial else None
    if min_nontrivial is not None:
        ensure(min_nontrivial >= w + 1, "replay has nontrivial collision below w+1")

    return {
        "field": f"F_{p}",
        "p": p,
        "n": n,
        "omega": omega,
        "j": j,
        "w": w,
        "total_supports": total_supports,
        "fiber_count": len(buckets),
        "max_fiber": max_fiber,
        "number_of_max_fibers": max_keys,
        "second_moment": second_moment,
        "average_fiber": total_supports / len(buckets),
        "second_moment_over_average_squared": second_moment * len(buckets) / (total_supports * total_supports),
        "collision_distance_strata": {str(e): count for e, count in sorted(strata.items())},
        "minimum_nontrivial_one_sided_difference": min_nontrivial,
        "forbidden_strata_1_through_w_empty": not forbidden,
    }


def twist_target_key(key: tuple[int, ...], p: int, omega: int, shift: int) -> tuple[int, ...]:
    return tuple((value * pow(omega, shift * (idx + 1), p)) % p for idx, value in enumerate(key))


def target_stabilizer_size(key: tuple[int, ...], n: int) -> int:
    support_gcd = 0
    for idx, value in enumerate(key, start=1):
        if value:
            support_gcd = math.gcd(support_gcd, idx)
    if support_gcd == 0:
        return n
    return math.gcd(n, support_gcd)


def q2_replay_case(p: int, n: int, omega: int, j: int, w: int) -> dict[str, Any]:
    buckets = prefix_buckets_for_case(p, n, omega, j, w)
    sizes = {key: len(values) for key, values in buckets.items()}
    max_fiber = max(sizes.values())
    heavy_keys = [key for key, size in sizes.items() if size == max_fiber]
    heavy_set = set(heavy_keys)
    orbit_size_distribution: dict[int, int] = {}
    stabilizer_distribution: dict[int, int] = {}
    seen_orbit_reps: set[tuple[int, ...]] = set()
    forced_nontrivial = len(heavy_keys) < n

    for key in heavy_keys:
        stabilizer = target_stabilizer_size(key, n)
        orbit = {twist_target_key(key, p, omega, shift) for shift in range(n)}
        ensure(len(orbit) * stabilizer == n, "orbit-stabilizer check failed")
        ensure(orbit <= heavy_set, "heavy target set is not twist-invariant")
        if forced_nontrivial:
            ensure(stabilizer > 1, "few heavy targets should force nontrivial stabilizer")
        for idx, value in enumerate(key, start=1):
            if value:
                ensure(idx % stabilizer == 0, "stabilized target has non-quotient coordinate")
        orbit_size_distribution[len(orbit)] = orbit_size_distribution.get(len(orbit), 0) + 1
        stabilizer_distribution[stabilizer] = stabilizer_distribution.get(stabilizer, 0) + 1
        seen_orbit_reps.add(min(orbit))

    return {
        "field": f"F_{p}",
        "p": p,
        "n": n,
        "omega": omega,
        "j": j,
        "w": w,
        "fiber_count": len(buckets),
        "max_fiber": max_fiber,
        "heavy_threshold_used": max_fiber,
        "heavy_target_count": len(heavy_keys),
        "heavy_target_count_less_than_n": forced_nontrivial,
        "number_of_heavy_twist_orbits": len(seen_orbit_reps),
        "orbit_size_distribution_on_heavy_targets": {str(k): v for k, v in sorted(orbit_size_distribution.items())},
        "stabilizer_distribution_on_heavy_targets": {str(k): v for k, v in sorted(stabilizer_distribution.items())},
        "interpretation": (
            "If heavy_target_count<n, every max-heavy target in this replay has "
            "nontrivial twist stabilizer and nonzero coordinates only at multiples "
            "of that stabilizer."
        ),
    }


def q2_symmetry_descent_block() -> dict[str, Any]:
    divisor_thresholds = []
    for exp in range(1, 22):
        h = 2**exp
        divisor_thresholds.append(
            {
                "forced_stabilizer_at_least": h,
                "sufficient_heavy_target_count_bound": N // h,
                "quotient_prefix_depth_floor_w_over_h": W_PREFIX // h,
            }
        )
    replay_cases = [
        q2_replay_case(p=17, n=8, omega=2, j=3, w=1),
        q2_replay_case(p=17, n=16, omega=3, j=8, w=3),
        q2_replay_case(p=97, n=16, omega=8, j=8, w=2),
    ]
    ensure(replay_cases[1]["heavy_target_count_less_than_n"], "expected F_17 n=16 w=3 heavy stabilizer replay")
    ensure(replay_cases[1]["stabilizer_distribution_on_heavy_targets"] == {"2": 8}, "unexpected Q2 stabilizer replay")
    return {
        "step": "Q2",
        "name": "heavy-fiber twist-stabilizer descent",
        "status": "PROVED_STABILIZER_FORCING_CONDITIONAL_ON_HEAVY_COUNT_BOUND",
        "theorem": "twist orbit-stabilizer reduction for heavy prefix fibers",
        "statement": (
            "The mu_n twist action sends a prefix target (z_1,...,z_w) to "
            "(eta z_1, eta^2 z_2, ..., eta^w z_w) and preserves fiber size. "
            "If a heavy-target set has size at most M, every heavy target has "
            "twist orbit size at most M.  Hence if M<=n/h, its stabilizer has "
            "size at least h and its nonzero prefix coordinates occur only at "
            "indices divisible by h."
        ),
        "deployed_thresholds": divisor_thresholds,
        "proof_summary": [
            "Twisting supports by eta in mu_n bijects each prefix fiber with the twisted target fiber.",
            "Therefore any threshold-heavy target set is a union of twist orbits.",
            "If a heavy target set has at most M elements, each heavy orbit has size at most M.",
            "Orbit-stabilizer gives |Stab(z)|=n/|Orb(z)|; M<=n/h forces |Stab(z)|>=h.",
            "If eta is in Stab(z), eta^d z_d=z_d for each prefix coordinate d; a stabilizer of order h forces z_d=0 unless h divides d.",
            "The surviving coordinates are exactly a quotient-prefix target at depth floor(w/h), ready for Q0 descent after folding-defect accounting.",
        ],
        "toy_replay_cases": replay_cases,
        "what_q2_proves": [
            "Heavy-fiber targets are twist-orbit structured.",
            "A sufficiently small heavy-target count forces quotient-supported prefix targets.",
            "The stabilizer order gives the quotient rung and lower prefix depth floor(w/h).",
        ],
        "what_q2_does_not_prove": [
            "It does not supply the heavy-target count bound; that needs evaluated Q1/higher moments.",
            "It does not prove the folding-defect descent from stabilized target to Q0 quotient/planted support cells.",
            "It does not prove the final primitive max-orbit bound with K<=4805007.",
            "It does not pay extension-valued, sparse, or pair-deficient M1 residual branches.",
        ],
    }


def q2_folding_rigidity_block() -> dict[str, Any]:
    """Q2 folding bridge from stabilized targets to quotient cosets."""

    rows = []
    quotient_descended: list[int] = []
    empty_exact_lift: list[int] = []
    not_applicable: list[int] = []
    for exp in range(1, 22):
        h = 2**exp
        applies = h // 2 <= W_PREFIX
        divisible = J % h == 0
        if applies and divisible:
            outcome = "QUOTIENT_DESCENT"
            quotient_descended.append(h)
        elif applies:
            outcome = "EMPTY_AFTER_GENERATED_PREFIX_REMOVAL"
            empty_exact_lift.append(h)
        else:
            outcome = "NOT_APPLICABLE_H_OVER_2_GREATER_THAN_W"
            not_applicable.append(h)
        rows.append(
            {
                "h": h,
                "h_over_2": h // 2,
                "n_over_h": N // h,
                "j_div_h": J // h if divisible else None,
                "j_mod_h": J % h,
                "floor_w_over_h": W_PREFIX // h,
                "h_over_2_le_w": applies,
                "h_divides_j": divisible,
                "exact_lift_outcome": outcome,
            }
        )

    generated_prefix_cells_used = W_PREFIX * P
    generated_cells_budgeted = T * P
    ensure(generated_prefix_cells_used == 143_760_893_740_943, "Q2 generated-prefix cell count mismatch")
    ensure(generated_cells_budgeted == 143_763_024_447_376, "Q2 generated budget mismatch")
    ensure(generated_cells_budgeted - generated_prefix_cells_used == P, "Q2 generated slack mismatch")
    ensure(quotient_descended == [2, 4, 8, 16], "Q2 quotient-descended h list mismatch")
    ensure(
        empty_exact_lift
        == [32, 64, 128, 256, 512, 1_024, 2_048, 4_096, 8_192, 16_384, 32_768, 65_536, 131_072],
        "Q2 empty exact-lift h list mismatch",
    )
    ensure(not_applicable == [262_144, 524_288, 1_048_576, 2_097_152], "Q2 not-applicable h list mismatch")
    ensure(J == 981_104 and J == (2**4) * 17 * 3_607, "deployed j factorization mismatch")

    return {
        "step": "Q2",
        "name": "stabilized prefix fibers fold to quotient cosets",
        "status": "PROVED_EXACT_LIFT_FINITE_CONDITIONAL_ON_GENERATED_PREFIX_BUCKET",
        "theorem": (
            "If an exact lifted prefix target is h-stabilized and h/2<=w, then "
            "every support in that exact lifted fiber is a union of h-cosets."
        ),
        "finite_wrapper": {
            "status": "FINITE_USE_CONDITIONAL_ON_GENERATED_PREFIX_COLLISION_BUCKET",
            "predicate": (
                "First d<=h/2 with lifted lambda_d nonzero in Z[zeta_n] but "
                "finite lambda_d=0 in F_p."
            ),
            "global_generated_rows_used": W_PREFIX,
            "generated_cells_used_bound": generated_prefix_cells_used,
            "generated_cells_budgeted_t_times_p": generated_cells_budgeted,
            "slack": generated_cells_budgeted - generated_prefix_cells_used,
            "cost_model_warning": (
                "This is an image-cell generated-prefix cover, not a raw support "
                "bound.  It is deducted only if the first-match generated bucket "
                "is explicitly scoped to include prefix-coordinate lift collisions."
            ),
        },
        "deployed_h_rows": rows,
        "quotient_descended_h": quotient_descended,
        "empty_exact_lift_h": empty_exact_lift,
        "not_applicable_h": not_applicable,
        "proof_summary": [
            "An h-stabilized exact target has lambda_d=0 for all d<=w with h not dividing d.",
            "Since h is a 2-power and h/2<=w, this gives lambda_1=...=lambda_{h/2}=0.",
            "Newton identities in characteristic zero give P_k(S)=0 for every 1<=k<=h/2, in particular for k=1,2,4,...,h/2.",
            "The 2-power positive zero-sum lemma forces P_1(S)=0 to make S antipodally paired.",
            "Iterating on the quotient by x->x^2, P_{2^a}(S)=0 forces union of 2^{a+1}-cosets.",
            "Thus S is a union of h-cosets.  If h does not divide j the exact lifted fiber is empty; otherwise it descends bijectively to the quotient prefix fiber at (n/h,j/h,floor(w/h)).",
        ],
        "what_this_buys": [
            "A stabilized heavy target is not unstructured top-rung primitive mass after generated-prefix lift collisions are removed.",
            "For h=2,4,8,16 the exact lifted branch descends to the corresponding Q0 quotient rung.",
            "For h=32,...,131072 the exact lifted branch is empty because h does not divide j=981104.",
        ],
        "does_not_prove": [
            "It does not prove heavy-target fewness; Q1/higher moments still need evaluated constants.",
            "It does not prove lower-rung max-fiber constants for h=2,4,8,16.",
            "It does not apply to h>=262144 because h/2>w.",
            "Finite KoalaBear use is conditional unless generated-prefix lift collisions are included in the generated first-match bucket.",
        ],
    }


def q2_heavy_fiber_closure_block(proved_rem: int, quotient_block: dict[str, Any]) -> dict[str, Any]:
    """Conditional Q2 closure once primitive-heavy orbits are excluded."""

    k_rem = exact_k_multiplier(proved_rem)
    ensure(k_rem == 4_805_007, "Q2 closure K_rem mismatch")
    pointwise_lift_bound_pass = 11_440 * deployed_p_power() < k_rem * deployed_binom()
    ensure(pointwise_lift_bound_pass, "pointwise exact-lift threshold comparison failed")
    first_useful_h = 2
    sufficient_global_heavy_count_bound = N // first_useful_h
    prefix_heavy_cells = sufficient_global_heavy_count_bound * W_PREFIX
    existing_generated_allowance = T * P
    ensure(prefix_heavy_cells == 70_748_471_296, "heavy-prefix cell count mismatch")
    ensure(prefix_heavy_cells < existing_generated_allowance, "heavy-prefix cells should fit in generated allowance")
    separate_deduction_k = exact_k_multiplier(proved_rem - prefix_heavy_cells)
    ensure(separate_deduction_k == 4_805_006, "separate heavy-prefix deduction should drop K by one")

    q0_rows_by_c = {row["c"]: row for row in quotient_block["rungs"]}
    lower_rows = []
    for h in (2, 4, 8, 16):
        n_h = N // h
        j_h = J // h
        w_h = W_PREFIX // h
        k_h = q0_rows_by_c[h]["K_c_at_current_B_rem"]
        ensure(q0_rows_by_c[h]["j_c"] == j_h and q0_rows_by_c[h]["w_c"] == w_h, "Q2 lower row mismatch")
        ensure(w_h >= n_h // 32, "terminal-16 exact-lift hypothesis failed")
        terminal_coset_size = n_h // 16
        max_variable_terminal_cosets = j_h // terminal_coset_size
        exact_lift_bound = max(math.comb(16, q) for q in range(max_variable_terminal_cosets + 1))
        ensure(max_variable_terminal_cosets == 7, "unexpected terminal variable-coset count")
        ensure(exact_lift_bound == 11_440, "lower-rung exact-lift bound mismatch")
        ensure(
            exact_lift_bound * (P**w_h) <= k_h * math.comb(n_h, j_h),
            f"lower-rung exact-lift bound does not fit K_h target for h={h}",
        )
        lower_rows.append(
            {
                "h": h,
                "N": n_h,
                "J": j_h,
                "W": w_h,
                "K_h": k_h,
                "terminal_coset_size": terminal_coset_size,
                "max_variable_terminal_cosets": max_variable_terminal_cosets,
                "exact_lift_max_fiber_bound": exact_lift_bound,
                "status": "PROVED_EXACT_LIFT_FINITE_USE_REQUIRES_GENERATED_PREFIX_BUCKET",
                "proof_key": "W>=N/32 forces terminal-16 exact-lift rigidity.",
            }
        )

    return {
        "step": "Q2",
        "name": "Q2 exact-lift closure conditional on generated-prefix support multiplicity",
        "status": "CONDITIONAL_ON_PRIMITIVE_HEAVY_ORBIT_EXCLUSION",
        "threshold": {
            "K_rem_proved": k_rem,
            "rational_form": "4805007 * binom(2097152,981104) / p^67471",
            "integer_heavy_test": "N_pre(z) * p^67471 > 4805007 * binom(2097152,981104)",
        },
        "primitive_heavy_orbit_input": {
            "status": "OPEN_REQUIRED_CERTIFICATE",
            "target": (
                "For every trivial-stabilizer prefix-target orbit O, "
                "N_pre(O) * p^w <= 4805007 * binom(n,j)."
            ),
            "why_this_is_the_right_Q2_trigger": (
                "Q2 only needs every threatening target to have nontrivial twist "
                "stabilizer.  The global count bound #heavy<=n/2 is sufficient "
                "but stronger than necessary."
            ),
            "stronger_but_not_needed": f"|{{z : |R_pre(z)| > threshold}}| <= {sufficient_global_heavy_count_bound}",
            "suggested_certificate_shape": (
                "An orbit-stratified integer excess certificate.  For each "
                "primitive orbit O, define X_O=max(0,N_pre(O)*p^w-K_rem*binom(n,j)); "
                "the clean successful certificate is sum_{O primitive} X_O^q=0."
            ),
        },
        "generated_prefix_bucket": {
            "status": "PAID_IF_INCLUDED_IN_GENERATED_FIRST_MATCH_BUCKET",
            "cell_model": "heavy-target-local prefix lift collision cells (z,d)",
            "worst_case_h": first_useful_h,
            "max_cells_if_separate": prefix_heavy_cells,
            "existing_generated_allowance_t_times_p": existing_generated_allowance,
            "fits_existing_generated_allowance": True,
            "K_if_deducted_separately": separate_deduction_k,
            "note": (
                "Do not claim no new cost unless generated row-universe coalescing "
                "is explicit.  If treated as a separate paid branch, deduct at most "
                "(n/h)*w cells; at h=2 this drops the top multiplier by one."
            ),
        },
        "closure_statement": (
            "If primitive-heavy-orbit exclusion holds, every threatening target "
            "has nontrivial dyadic stabilizer.  After generated-prefix "
            "lift-collision removal, Q2 folding sends each such target to quotient "
            "descent when h divides j, or to an empty exact-lift branch when h "
            "does not divide j."
        ),
        "q2_folding_outcomes": {
            "quotient_descended_h": [2, 4, 8, 16],
            "empty_exact_lift_h": [
                32,
                64,
                128,
                256,
                512,
                1_024,
                2_048,
                4_096,
                8_192,
                16_384,
                32_768,
                65_536,
                131_072,
            ],
            "not_applicable_h": [262_144, 524_288, 1_048_576, 2_097_152],
        },
        "lower_rung_exact_lift_certificates": lower_rows,
        "generated_lift_class_pointwise_route": {
            "status": "CONDITIONAL_ON_GENERATED_PREFIX_SUPPORT_MULTIPLICITY_CERTIFICATE",
            "claim_if_bucket_is_paid": (
                "If for every finite prefix target z the first-match ledger may "
                "retain one exact lifted prefix class and charge all other exact "
                "lift classes over z as generated-prefix collisions, then every "
                "residual finite fiber is contained in one exact lifted fiber and "
                "has size <=11440.  This would imply no target is heavy."
            ),
            "exact_lift_bound_used": 11_440,
            "threshold_comparison": "11440 * p^w < 4805007 * binom(n,j)",
            "threshold_comparison_pass": pointwise_lift_bound_pass,
            "why_not_marked_proved_here": (
                "The assignment depends on the finite target z and its retained "
                "exact lift class.  A row-indexed w*p image-cell count does not "
                "by itself bound the number of removed exact lift classes or raw "
                "supports.  The packet records this as a conditional route and "
                "adds a small finite replay showing that the naive image-cell to "
                "support-payment inference is false."
            ),
        },
        "generated_prefix_support_multiplicity_target": {
            "status": "OPEN_REQUIRED_SUPPORT_MULTIPLICITY_CERTIFICATE",
            "proved_part": (
                "A non-retained exact lift class over a finite target gives a "
                "nonzero cyclotomic prefix-coordinate difference whose reduction "
                "mod p is zero."
            ),
            "not_proved": (
                "The number of supports lying in those generated-prefix collision "
                "cells is bounded by t*p or by the remaining primitive threshold."
            ),
            "sufficient_deployed_bound": (
                "(|G_gen_prefix(z)| + 11440) * p^67471 <= "
                "4805007 * binom(2097152,981104) for every primitive target z."
            ),
            "convenient_stronger_bound": "|G_gen_prefix(z)| <= t*p = 143763024447376",
            "convenient_bound_fits_threshold": (T * P + 11_440) * deployed_p_power()
            < k_rem * deployed_binom(),
            "why_this_is_still_the_Q2_bottleneck": (
                "Since each retained exact-lift class is already <=11440, bounding "
                "the non-retained generated-prefix support mass is equivalent, up "
                "to 11440, to the finite primitive prefix-fiber bound for that target."
            ),
        },
        "does_not_prove": [
            "primitive-heavy-orbit exclusion / orbitwise excess certificate",
            "global heavy-target fewness; it is stronger than necessary and remains unproved",
            "generated-prefix support multiplicity; image-cell labels are not support payments",
            "BC split-pencil census",
            "SP primitive shift-pair control",
            "extension-valued slope branch",
            "sparse/Pade-Hankel residual branch",
            "arbitrary planted tails outside the stabilized Q2 branch",
            "finite use unless generated-prefix lift collisions are included in first-match generated cells",
        ],
    }


def q1_distance_insufficiency_block() -> dict[str, Any]:
    """Show the Q1 distance gap is not enough for finite heavy-target exclusion."""

    e = W_PREFIX + 1
    logs = [log2_binom(J, i) + log2_binom(N - J, i) for i in range(e)]
    max_log = max(logs)
    log2_ball = max_log + math.log2(sum(2 ** (value - max_log) for value in logs))
    log2_total = log2_binom(N, J)
    log2_greedy = log2_total - log2_ball
    log2_threshold = math.log2(4_805_007) + log2_total - W_PREFIX * math.log2(P)
    log2_n_times_threshold = math.log2(N) + log2_threshold

    ensure(abs(log2_ball - 721_930.7849983689) < 1e-6, "Johnson ball log changed")
    ensure(abs(log2_total - 2_090_873.2797933037) < 1e-6, "total support log changed")
    ensure(abs(log2_greedy - 1_368_942.4947949348) < 1e-6, "greedy distance log changed")
    ensure(abs(log2_n_times_threshold - 78.93135351664387) < 1e-9, "n*T log changed")

    return {
        "status": "PROVED_DISTANCE_ONLY_INSUFFICIENT",
        "statement": (
            "The Q1 one-sided distance lower bound e>=w+1 is far too weak by "
            "itself to imply primitive-heavy-orbit exclusion or #heavy<=n/2."
        ),
        "parameters": {
            "n": N,
            "j": J,
            "w": W_PREFIX,
            "one_sided_distance_e": e,
        },
        "johnson_ball_log2_radius_e_minus_1": log2_ball,
        "total_support_log2": log2_total,
        "greedy_distance_code_lower_bound_log2": log2_greedy,
        "log2_threshold_T": log2_threshold,
        "log2_n_times_threshold_T": log2_n_times_threshold,
        "interpretation": (
            "A generic constant-weight packing with the Q1 distance constraint can "
            "be astronomically larger than the heavy-target scale.  The missing "
            "theorem must use moment-curve algebra and first-match branch "
            "structure, not distance alone."
        ),
    }


def q2_failed_route_evidence_block() -> dict[str, Any]:
    """Record failed Q2 proof routes as evidence, without promoting them to proofs."""

    k_rem = 4_805_007
    retained_exact_lift_bound = 11_440
    t_times_p = T * P
    conditional_support_bound = t_times_p + retained_exact_lift_bound
    threshold_num = k_rem * deployed_binom()
    threshold_den = deployed_p_power()
    threshold_floor = threshold_num // threshold_den
    threshold_ceil = (threshold_num + threshold_den - 1) // threshold_den
    slack_bits = math.log2(threshold_floor / conditional_support_bound)

    ensure(t_times_p == 143_763_024_447_376, "Q2 evidence t*p mismatch")
    ensure(conditional_support_bound == 143_763_024_458_816, "Q2 evidence t*p+11440 mismatch")
    ensure(threshold_floor == 274_836_936_291_722_953, "Q2 threshold floor mismatch")
    ensure(threshold_ceil == 274_836_936_291_722_954, "Q2 threshold ceil mismatch")
    ensure(conditional_support_bound < threshold_floor, "conditional support bound should fit threshold")

    log2_t_times_p = math.log2(t_times_p)
    e_min = W_PREFIX + 1
    route_a_ball_log = 721_930.7849983689
    route_a_total_log = log2_binom(N, J)
    route_a_gilbert_log = route_a_total_log - route_a_ball_log
    route_a_gap = route_a_gilbert_log - log2_t_times_p

    route_b_log_choose = log2_binom(J, e_min)
    route_b_naive_log = route_b_log_choose + math.log2(P)
    route_b_gap_choose = route_b_log_choose - log2_t_times_p
    route_b_gap_naive = route_b_naive_log - log2_t_times_p

    tuple_q3_log = 3 * math.log2(threshold_ceil)
    tuple_q4_log = 4 * math.log2(threshold_ceil)

    folded_n = N // 2
    odd_constraints = (W_PREFIX + 1) // 2
    even_constraints = W_PREFIX // 2
    first_allowed_defect = odd_constraints + 1
    route_d_defect_log = log2_binom(folded_n, first_allowed_defect)
    route_d_gap = route_d_defect_log - log2_t_times_p

    ensure(e_min == 67_472, "Q2 evidence e_min mismatch")
    ensure(even_constraints == 33_735 and odd_constraints == 33_736, "Q2 route D constraint mismatch")
    ensure(first_allowed_defect == 33_737, "Q2 route D first defect mismatch")

    return {
        "status": "EVIDENCE_RECORDED_NO_Q2_CLOSURE",
        "remaining_q2_target": {
            "status": "OPEN_REQUIRED_SUPPORT_MULTIPLICITY_OR_PRIMITIVE_EXCESS_CERTIFICATE",
            "statement": (
                "For every primitive finite prefix target z, prove |G_gen(z)| <= t*p, "
                "or at least (|G_gen(z)|+11440)*p^67471 <= "
                "4805007*binom(2097152,981104)."
            ),
            "t_times_p": t_times_p,
            "retained_exact_lift_bound": retained_exact_lift_bound,
            "conditional_support_bound_t_p_plus_retained": conditional_support_bound,
            "threshold_floor": threshold_floor,
            "threshold_ceil": threshold_ceil,
            "slack_bits_vs_t_p_plus_retained": slack_bits,
            "conditional_closure_status": "PROVED_IF_SUPPORT_BOUND_SUPPLIED",
        },
        "route_A_delsarte_distance_attempt": {
            "status": "OPEN_MISSING_ROUTE_A_DUAL_EXCESS_CERTIFICATE",
            "diagnostics": {
                "log2_binom_n_j": route_a_total_log,
                "log2_johnson_ball_radius_w": route_a_ball_log,
                "log2_gilbert_lower_bound_at_q1_distance": route_a_gilbert_log,
                "log2_t_times_p": log2_t_times_p,
                "gap_bits_vs_t_p": route_a_gap,
            },
            "conclusion": (
                "Q1/distance-only information is astronomically too weak; a real "
                "BCH/Fourier/prefix dual or excess-moment certificate is needed."
            ),
        },
        "route_B_split_pair_rank_attempt": {
            "status": "PROVED_LOCAL_FULL_ROW_RANK_ONLY_INSUFFICIENT",
            "proved": (
                "The split-pair power-sum Jacobian has a nonzero Vandermonde pivot "
                "minor on ordinary distinct exchange variables."
            ),
            "diagnostics": {
                "e_min": e_min,
                "rank": W_PREFIX,
                "minimum_nullity": 1,
                "log2_choose_j_e_min": route_b_log_choose,
                "log2_naive_A_side_full_rank_bound": route_b_naive_log,
                "log2_t_times_p": log2_t_times_p,
                "gap_choose_j_e_min_vs_t_p": route_b_gap_choose,
                "gap_naive_full_rank_vs_t_p": route_b_gap_naive,
            },
            "conclusion": (
                "Local nondegeneracy does not control global support multiplicity; "
                "almost all B choices must be proved impossible or first-matched "
                "to paid branches."
            ),
        },
        "route_C_primitive_orbit_excess_attempt": {
            "status": "OPEN_REQUIRED_PRIMITIVE_EXCESS_CERTIFICATE",
            "proved": [
                "exact threshold arithmetic",
                "formal excess-to-tuple amplification",
                "tuple-strata certificate interface",
            ],
            "diagnostics": {
                "threshold_floor": threshold_floor,
                "threshold_ceil": threshold_ceil,
                "log2_threshold": math.log2(threshold_floor),
                "q3_minimum_ordered_tuple_log2": tuple_q3_log,
                "q4_minimum_ordered_tuple_log2": tuple_q4_log,
            },
            "missing_certificate": (
                "Prove sum_{primitive O} X_O^3=0 or sum_{primitive O} X_O^4=0, "
                "or provide a complete tuple first-match classification with zero "
                "primitive full-rank tuple residual."
            ),
        },
        "route_D_folding_defect_transfer_attempt": {
            "status": "OPEN_MISSING_ROUTE_D_FOLDING_DEFECT_SUPPORT_CERTIFICATE",
            "proved": [
                "dyadic folding identities",
                "small signed-defect emptiness via odd-equation BCH/RS distance",
                "recursive first-match schema that refuses to count open strata",
            ],
            "diagnostics": {
                "folded_n": folded_n,
                "even_constraints": even_constraints,
                "odd_constraints": odd_constraints,
                "first_allowed_nonzero_signed_defect_size": first_allowed_defect,
                "log2_choose_folded_n_first_allowed_defect": route_d_defect_log,
                "log2_t_times_p": log2_t_times_p,
                "gap_bits_vs_t_p": route_d_gap,
            },
            "next_theorem": (
                "Large signed folding-defect transfer: every large signed defect "
                "satisfying the odd prefix equations must be quotient-descended, "
                "sparse/Pade-Hankel, M1/half-turn/window-shadow, rank-drop with "
                "printed pivot cost, generated-field support-paid, or bounded in "
                "a primitive full-rank defect stratum by <=t*p."
            ),
        },
        "small_model_regression_summary": {
            "status": "EVIDENCE_ONLY",
            "warnings_confirmed": [
                "generated-prefix image labels do not imply support payment",
                "global max fibers can be stabilized rather than primitive",
                "retained exact-lift class need not be singleton in small models",
            ],
            "observed_failures": [
                {
                    "case": "F17 n16 j8 w1",
                    "max_primitive": 757,
                    "max_nonretained": 737,
                    "w_times_p": 17,
                    "nonretained_le_w_times_p": False,
                },
                {
                    "case": "F17 n16 j8 w2",
                    "max_primitive": 49,
                    "max_nonretained": 47,
                    "w_times_p": 34,
                    "nonretained_le_w_times_p": False,
                },
            ],
        },
    }


def q1_collision_ledger_block() -> dict[str, Any]:
    max_e = min(J, N - J)
    ensure(max_e == J, "unexpected deployed max collision distance")
    ensure(W_PREFIX + 1 == 67_472, "deployed Q1 minimum collision mismatch")
    ensure(math.gcd(N, W_PREFIX + 1) == 16, "unexpected gcd(n,w+1)")
    replay_cases = [
        q1_replay_case(p=17, n=8, omega=2, j=3, w=1),
        q1_replay_case(p=17, n=16, omega=3, j=5, w=2),
        q1_replay_case(p=17, n=16, omega=3, j=8, w=3),
        q1_replay_case(p=97, n=16, omega=8, j=8, w=2),
    ]
    ensure([case["minimum_nontrivial_one_sided_difference"] for case in replay_cases] == [2, 3, 4, 3], "Q1 replay minima changed")
    return {
        "step": "Q1",
        "name": "exact split-prefix collision ledger",
        "status": "PROVED_EXACT_PAIR_DECOMPOSITION_AND_TOY_REPLAY",
        "theorem": "split-prefix second-moment decomposition by one-sided collision distance",
        "deployed_parameters": {
            "n": N,
            "j": J,
            "w": W_PREFIX,
            "minimum_nontrivial_one_sided_difference": W_PREFIX + 1,
            "forbidden_one_sided_differences": [1, W_PREFIX],
            "maximum_possible_one_sided_difference": max_e,
            "gcd_n_w_plus_1": math.gcd(N, W_PREFIX + 1),
            "w_plus_1_divides_n": N % (W_PREFIX + 1) == 0,
        },
        "exact_second_moment_identity": {
            "statement": (
                "sum_z N_w(z)^2 = binom(n,j) + sum_{e=w+1}^{min(j,n-j)} C_e, "
                "where C_e counts ordered distinct support pairs with one-sided "
                "difference e and equal first w locator-prefix coefficients."
            ),
            "factorized_form": (
                "C_e = sum_{I subset D, |I|=j-e} P_w(D\\I,e), where "
                "P_w(E,e) counts ordered disjoint e-subsets A,B of E with "
                "deg(Lambda_A - Lambda_B) <= e-w-1."
            ),
            "minimal_collision_clause": (
                "For e=w+1, the condition becomes Lambda_A - Lambda_B is constant; "
                "these are the constant-shift split-pair packets."
            ),
        },
        "proof_summary": [
            "For a colliding ordered pair S,T, write I=S cap T, S=I disjoint-union A, T=I disjoint-union B.",
            "Then Lambda_S - Lambda_T = Lambda_I (Lambda_A - Lambda_B).",
            "Equal first w prefix coefficients are equivalent to deg(Lambda_S-Lambda_T) <= j-w-1.",
            "If S!=T and e=deg Lambda_A=deg Lambda_B, this is equivalent to deg(Lambda_A-Lambda_B) <= e-w-1, hence e>=w+1.",
            "Summing ordered pairs by e gives the displayed exact second-moment decomposition.",
        ],
        "toy_replay_cases": replay_cases,
        "what_q1_proves": [
            "No nontrivial prefix collision can occur below one-sided distance w+1.",
            "The second moment is exactly reduced to the residual split-pair counts C_e for e>=w+1.",
            "Minimal collisions are exactly constant-shift split-pair packets.",
            "Small finite cyclic-domain replays satisfy the formula and the distance gap.",
        ],
        "what_q1_does_not_prove": [
            "It does not evaluate all deployed C_e summands.",
            "It does not prove a worst-case max-fiber bound.",
            "It does not prove the Q0 lower-rung max-fiber certificates.",
            "It does not replace the Q2 heavy-fiber symmetry descent.",
        ],
    }


def conditional_first_match_closure_block(proved_paid: int, proved_rem: int) -> dict[str, Any]:
    k_rem = exact_k_multiplier(proved_rem)
    ensure(k_rem == 4_805_007, "conditional closure K_rem mismatch")
    ensure(proved_paid + proved_rem == B_STAR, "ledger split should add to B*")
    return {
        "status": "CONDITIONAL_ON_ALL_NAMED_OPEN_BRANCH_PAYMENTS",
        "theorem": "conditional ledger implication for KB-MCA A=1116048",
        "residual_fiber_definition": (
            "R(z) is the first-match residual set of j-subsets with Phi_w(S)=z "
            "after generated-field, terminal quotient/planted, tangent/common-line, "
            "extension-confined, sparse/Pade-Hankel, known M1/half-turn, and "
            "contained/rank-drop branches are removed."
        ),
        "assumptions_required": [
            "Every named open first-match branch is paid by an explicit theorem/certificate with printed cost.",
            "The remaining primitive Q-fin residual satisfies max_z |R(z)| <= 4805007 * binom(2097152,981104) / p^67471.",
            "The complete first-match paid-cell sum is <= B* under the repo endpoint and denominator conventions.",
        ],
        "proved_paid_budget": proved_paid,
        "remaining_budget": proved_rem,
        "K_rem": k_rem,
        "conclusion_if_all_assumptions_hold": "the row would close under a future complete U(1116048) upper-ledger certificate",
        "not_proved_here": (
            "This packet does not prove U(1116048)<=B*.  It does not pay all named "
            "open branches and does not prove the primitive max-orbit certificate."
        ),
    }


def q1_q2_plan_block() -> dict[str, Any]:
    return {
        "Q1": {
            "name": "exact split-prefix collision ledger",
            "status": "PROVED_IN_THIS_PACKET_AS_EXACT_PAIR_DECOMPOSITION",
            "target": (
                "Reduce the exact second moment sum_z N_w(z)^2 to ordered "
                "split-pair collision counts stratified by one-sided distance "
                "e=|S\\T|, with no nontrivial terms below e=w+1."
            ),
            "proved_input_already_in_this_packet": (
                "If two distinct supports collide in the first w prefix "
                "coordinates, then e>=w+1."
            ),
            "deliverables": [
                "exact second-moment decomposition by e",
                "constant-shift split-pair normal form for minimal e=w+1 collisions",
                "small cyclic-domain replay of the distance gap and stratum identity",
            ],
            "proof_ideas": [
                "Use Lambda_S=G A and Lambda_T=G B; prefix equality is a high-order vanishing condition on G(A-B).",
                "Minimal collisions have A-B constant, matching quotient constant-shift split pairs.",
            ],
            "why_it_does_not_close_Q_fin": (
                "Q1 leaves the deployed C_e summands unevaluated and gives "
                "typical/heavy-fiber calibration, not the finite worst-case "
                "max-fiber bound with K<=4805007."
            ),
        },
        "Q2": {
            "name": "heavy-fiber symmetry descent and primitive max-orbit reduction",
            "status": "PROVED_STABILIZER_AND_EXACT_LIFT_FOLDING_WITH_OPEN_SUPPORT_MULTIPLICITY",
            "target": (
                "Use orbitwise moment/excess certificates, or a support-level "
                "generated-prefix multiplicity theorem, to rule out primitive "
                "heavy target orbits.  Then apply the proved twist-stabilizer "
                "theorem and exact-lift folding rigidity to route every "
                "threatening stabilized target toward quotient descent or emptiness."
            ),
            "deliverables": [
                "twist orbit-stabilizer theorem for prefix targets",
                "stabilizer-to-quotient target normal form",
                "exact-lift folding theorem for stabilized target fibers",
                "finite wrapper conditional on generated-prefix support multiplicity",
                "small replay showing generated-prefix image cells are not support payments",
                "toy replay showing few max-heavy fibers force nontrivial stabilizer",
            ],
            "proof_ideas": [
                "The mu_n twist action sends z_i to eta^i z_i and preserves fiber sizes; few heavy fibers force stabilizer.",
                "An h-stabilized exact lifted target has lambda_1=...=lambda_{h/2}=0, so Newton identities force P_1,P_2,P_4,...,P_{h/2}=0.",
                "Iterated 2-power antipodal balancing then forces the support to be a union of h-cosets.",
                "Finite KoalaBear use first classifies nonzero lifted low-prefix coefficients reducing to zero as generated-prefix collisions; support payment still needs a multiplicity theorem.",
            ],
            "experimental_evidence_used": [
                "Small prefix-fiber scans showed mode-at-null is false, so Q2 should target max-orbit/stabilizer descent rather than a null-fiber shortcut.",
                "Finite {1,3}/{1,4} scans produced generated-only survivors, confirming that generated-field stripping must precede finite Q comparisons.",
                "Small cyclic-domain scans showed heavy fibers often have visible stabilizer/quotient structure after primitive filtering.",
            ],
            "finite_row_acceptance_threshold": (
                "For the current local packet, Q2 must eventually imply "
                "max_z |R(z)| <= 4805007 * binom(2097152,981104) / p^67471, "
                "or replace that inequality with an equivalent replayable certified recursion. "
                "The structural stabilizer and exact-lift folding parts are now proved; "
                "the missing input is primitive-heavy-orbit exclusion, or equivalently "
                "a support-level generated-prefix multiplicity certificate for non-retained "
                "exact lift classes.  The stronger #heavy<=n/2 target is sufficient "
                "but not necessary."
            ),
        },
    }


def row_packet_block(arith: dict[str, Any]) -> dict[str, Any]:
    return {
        "field": "KoalaBear sextic line field",
        "D": "mu_2^21",
        "n": N,
        "k": K,
        "agreement": A_ADJACENT,
        "rho": "1/2",
        "epsilon_star": "2^-128",
        "q_gen": P,
        "q_line": Q_LINE,
        "q_chal": None,
        "q_list": None,
        "B_star": B_STAR,
        "endpoint_convention": "B* = floor((q_line - 1) / 2^128)",
        "unsafe_certificate": None,
        "safe_certificate": None,
        "safe_certificate_status": "NOT_PROVED_BY_THIS_PACKET",
        "not_certified_safe": True,
        "deduplication_rule": (
            "First-match order is recorded in first_match_branches.  Only rows "
            "with deducted_in_proved_ledger=true are included in the partial "
            "paid-cell total."
        ),
        "replay": {
            "script": "experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py",
            "quick_check_command": (
                "python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --check"
            ),
            "full_recompute_command": (
                "python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --full --check"
            ),
            "json_sha256": None,
            "seed": None,
        },
        "denominator_separation_note": (
            "q_gen, q_line, q_chal, and q_list are intentionally separate. "
            "This packet does not instantiate q_chal or q_list ledgers."
        ),
        "partial_paid_cells_total": arith["B_gen_t_times_p"] + arith["terminal_quotient_raw_paid_cost"],
    }


def branch_rows(arith: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "order": 1,
            "branch": "contained_or_noncontained_failure",
            "status": "INTERFACE_BUCKET_NOT_A_DEDUCTED_SAFE_CELL",
            "cost": 0,
            "deducted_in_proved_ledger": False,
            "reason": "These witnesses are removed before the noncontained finite-slope numerator is counted.",
        },
        {
            "order": 2,
            "branch": "rank_drop_or_pivot_failure",
            "status": "OPEN_EXACT_MINOR_OR_PIVOT_BUCKET_REQUIRED",
            "cost": None,
            "deducted_in_proved_ledger": False,
            "reason": "The generated-collision lemma assumes a surviving pivot row with red_p(B_0(S)) nonzero.",
        },
        {
            "order": 3,
            "branch": "tangent_common_line_residue",
            "status": "OPEN_FOR_THIS_ROW",
            "cost": None,
            "deducted_in_proved_ledger": False,
            "radius_j": J,
            "high_agreement_tangent_cap_floor_n_minus_k_over_3": (N - K) // 3,
            "reason": "The standard high-agreement tangent function is unavailable because j is outside the high-agreement range.",
        },
        {
            "order": 4,
            "branch": "quotient_periodic_or_divisor_stabilized",
            "status": "PARTIAL_PROVED_DESCENT_WITH_TERMINAL_RAW_PAID",
            "cost": arith["terminal_quotient_raw_paid_cost"],
            "deducted_in_proved_ledger": True,
            "reason": "Dyadic quotient/planted descent is proved for r_c<=w; terminal rungs c=65536,131072 are raw-paid. Lower-rung obligations and large planted tails remain open.",
        },
        {
            "order": 5,
            "branch": "planted_prefix_structured",
            "status": "OPEN_EXACT_IMAGE_COST_REQUIRED",
            "cost": None,
            "deducted_in_proved_ledger": False,
            "reason": "Planted/prefix structured cells need a row-specific image cost before deduction.",
        },
        {
            "order": 6,
            "branch": "extension_valued_slope",
            "status": "OPEN_PROPER_EXTENSION_BRANCH",
            "cost": None,
            "deducted_in_proved_ledger": False,
            "reason": "Line slopes live in F_{p^6}; this packet only pays base-generated finite-only cells over F_p.",
        },
        {
            "order": 7,
            "branch": "base_generated_field_collision",
            "status": "PROVED_IMAGE_CELL_COVER",
            "cost": arith["B_gen_t_times_p"],
            "deducted_in_proved_ledger": True,
            "cost_model": "row-indexed generated-slope image cells",
            "row_count_bound_R": T,
            "base_field_slope_values": P,
            "formula": "B_gen <= R*p <= t*p",
            "not_a_raw_support_bound": True,
        },
        {
            "order": 8,
            "branch": "sparse_sigma_or_sparse_support",
            "status": "OPEN_ROW_SPECIFIC_BOUND_REQUIRED",
            "cost": None,
            "deducted_in_proved_ledger": False,
            "reason": "No A=1116048 sparse-sigma image cost is supplied by this packet.",
        },
        {
            "order": 9,
            "branch": "m1_half_turn_or_coefficient_shadow",
            "status": "PARTIAL_NORMAL_FORM_WITH_NAMED_RESIDUAL",
            "cost": N + 1,
            "deducted_in_proved_ledger": False,
            "deducted_in_conditional_ledger": True,
            "reason": "The half-turn and nonconsecutive-window packets localize printed coefficient windows; pair-deficient residual windows and arbitrary sparse Hankel row-slices remain open.",
        },
        {
            "order": 10,
            "branch": "primitive_qfin_residual",
            "status": "TARGET_NOT_DEDUCTED",
            "cost": None,
            "deducted_in_proved_ledger": False,
            "target": "max primitive Q-fin fiber <= K_rem * binom(n,j)/p^w",
        },
    ]


def build_certificate() -> dict[str, Any]:
    arith = deployed_arithmetic()
    branches = branch_rows(arith)

    proved_paid = sum(row["cost"] for row in branches if row.get("deducted_in_proved_ledger"))
    conditional_paid = proved_paid + sum(
        row["cost"] for row in branches if row.get("deducted_in_conditional_ledger")
    )
    ensure(
        proved_paid == arith["B_gen_t_times_p"] + arith["terminal_quotient_raw_paid_cost"],
        "proved paid total mismatch",
    )

    proved_rem = B_STAR - proved_paid
    conditional_rem = B_STAR - conditional_paid
    ensure(
        proved_rem == arith["B_rem_after_generated_collision_and_terminal_quotient"],
        "proved rem mismatch",
    )
    quotient_block = quotient_planted_descent_block(proved_rem)
    honest_lift = honest_exact_lift_fiber_bound(exact_k_multiplier(proved_rem))
    split_collision = split_prefix_collision_distance_block()
    q1_collision = q1_collision_ledger_block()
    q2_symmetry = q2_symmetry_descent_block()
    q2_folding = q2_folding_rigidity_block()
    q2_heavy_closure = q2_heavy_fiber_closure_block(proved_rem, quotient_block)
    q1_distance_insufficient = q1_distance_insufficiency_block()
    q2_failed_routes = q2_failed_route_evidence_block()
    conditional_closure = conditional_first_match_closure_block(proved_paid, proved_rem)
    generated_prefix_counterexample = generated_prefix_support_payment_counterexample()

    cert = {
        "status": "CONDITIONAL",
        "claim_class": "PARTIAL_UPPER_LEDGER_AUDIT",
        "not_a_safe_side_certificate": True,
        "not_certified_safe": True,
        "note": "experimental/notes/thresholds/kb_mca_1116048_first_match_ledger_v1.md",
        "script": "experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py",
        "scope": {
            "object": "KoalaBear sextic finite-slope support-wise MCA partial first-match ledger audit",
            "row": "KB-MCA A=1116048",
            "top_level_nonclaim": "This packet does not prove U(1116048) <= B*.",
            "proved_here": [
                "deployed integer constants",
                "generated-field collision image-cell cost B_gen <= t*p",
                "dyadic quotient/planted prefix descent for r_c<=w",
                "raw-paid terminal quotient/planted rungs c=65536 and c=131072",
                "Q1 exact split-prefix collision decomposition by one-sided difference e",
                "Q2 twist-stabilizer forcing theorem for heavy prefix targets",
                "Q2 exact-lift folding rigidity for stabilized prefix targets",
                "split-prefix collision distance e>=w+1 for supports in a common prefix fiber",
                "honest cyclotomic exact-lift prefix fiber bound <= 11440, not deducted for finite-field use",
                "small finite replay showing generated-prefix image cells are not support payments",
                "Route A/B/C/D evidence explaining why Q2 support multiplicity remains open",
                "proved remaining primitive allowance after generated-cell deduction",
            ],
            "does_not_prove": [
                "primitive Q-fin max-orbit flatness",
                "extension-valued slope safety over F_{p^6} \\ F_p",
                "lower-rung quotient/planted max-fiber bounds for c=2..32768",
                "arbitrary planted-tail bounds for c>=262144",
                "sparse-sigma bounds",
                "arbitrary M1 row-slice compression",
                "raw support multiplicity inside a generated-field image cell",
                "finite-field lift-class removal at cost w*p for prefix-vector fibers",
                "generated-prefix support multiplicity bound for non-retained exact lift classes",
                "primitive-heavy-orbit exclusion from evaluated higher moments",
            ],
        },
        "row_packet": row_packet_block(arith),
        "deployed_arithmetic": arith,
        "generated_field_collision_charge": {
            "status": "PROVED_IMAGE_CELL_COVER",
            "theorem": "finite-only affine row survivors are generated-field reduction collisions",
            "requires_prior_buckets": [
                "contained/noncontained failure removed",
                "rank-drop/pivot-failure removed",
                "denominators cleared and not killed by reduction",
                "base/generated-field normalized printed affine row packet",
            ],
            "cost_model": "row-indexed generated-slope image cells, not raw supports",
            "row_count_bound_R": T,
            "base_slope_field_size": P,
            "B_gen_bound": arith["B_gen_t_times_p"],
        },
        "quotient_planted_descent": quotient_block,
        "q1_collision_ledger": q1_collision,
        "q2_symmetry_descent": q2_symmetry,
        "q2_folding_stabilized_fiber_rigidity": q2_folding,
        "q2_heavy_fiber_closure": q2_heavy_closure,
        "q1_distance_insufficiency": q1_distance_insufficient,
        "q2_failed_route_evidence": q2_failed_routes,
        "generated_prefix_support_payment_counterexample": generated_prefix_counterexample,
        "split_prefix_collision_distance": split_collision,
        "honest_cyclotomic_exact_lift_fiber_bound": honest_lift,
        "conditional_first_match_closure": conditional_closure,
        "finite_field_guardrail": generated_collision_guardrail(),
        "first_match_branches": branches,
        "partial_paid_ledger": {
            "not_complete_U": True,
            "B_paid_proved": proved_paid,
            "B_rem_proved": proved_rem,
            "K_rem_proved": exact_k_multiplier(proved_rem),
            "paid_cells": [
                {
                    "name": row["branch"],
                    "status": row["status"],
                    "paid": True,
                    "cost": row["cost"],
                    "dedup_rule": "first-match branch order",
                }
                for row in branches
                if row.get("deducted_in_proved_ledger")
            ],
            "unpaid_residual_cells": [
                {
                    "name": row["branch"],
                    "status": row["status"],
                    "paid": False,
                    "cost": row["cost"],
                    "blocking_input": row.get("target") or row.get("reason") or "named first-match branch payment required",
                    "dedup_rule": None,
                }
                for row in branches
                if not row.get("deducted_in_proved_ledger")
            ],
        },
        "conditional_ledger": {
            "meaning": "Adds only the named n+1 half-turn/pair-small image cost as a scenario; still not a deployed proof.",
            "B_paid_conditional": conditional_paid,
            "B_rem_conditional": conditional_rem,
            "K_rem_conditional": exact_k_multiplier(conditional_rem),
            "deducted_conditional_branches": [
                row["branch"]
                for row in branches
                if row.get("deducted_in_proved_ledger") or row.get("deducted_in_conditional_ledger")
            ],
        },
        "next_target": {
            "name": "KB-MCA 1116048 primitive Q-fin max-orbit flatness after first-match removal",
            "proved_K_rem_current": exact_k_multiplier(proved_rem),
            "statement": "max primitive Q-fin fiber <= K_rem * binom(n,j) / p^w",
            "remaining_ledger_work": [
                "prove or certify extension-valued slope image cells",
                "prove lower-rung quotient/planted max-fiber certificates for c=2..32768",
                "prove arbitrary planted-tail bounds for c>=262144",
                "prove primitive-heavy-orbit exclusion from Q1/higher collision ledgers so Q2 stabilizer forcing activates",
                "prove sparse-sigma image costs or keep sparse branch in primitive residual",
                "pay pair-deficient residual windows and classify arbitrary sparse Hankel row-slices beyond printed {1,r} coefficient windows",
                "prove generated-prefix support multiplicity for non-retained exact lift classes, or an equivalent primitive orbitwise flatness certificate",
                "prove primitive max-orbit flatness with K<=4805007, or replace it by a replayable certified recursion",
            ],
        },
        "q1_q2_plan": q1_q2_plan_block(),
    }
    assert_certificate(cert)
    return cert


def assert_certificate(cert: dict[str, Any]) -> None:
    arith = cert["deployed_arithmetic"]
    ensure(arith["K_raw"] == 4_807_520, "bad K_raw")
    ensure(arith["K_after_generated_collision"] == 4_805_007, "bad K_after_generated")
    ensure(cert["status"] == "CONDITIONAL", "top-level status should be conditional")
    ensure(cert["claim_class"] == "PARTIAL_UPPER_LEDGER_AUDIT", "bad claim class")
    ensure(cert["not_a_safe_side_certificate"] is True, "packet must not be marked safe")
    ensure(cert["row_packet"]["safe_certificate_status"] == "NOT_PROVED_BY_THIS_PACKET", "bad safe status")
    ensure(cert["partial_paid_ledger"]["B_paid_proved"] == T * P + 471_447_040, "bad proved paid")
    ensure(cert["partial_paid_ledger"]["K_rem_proved"] == 4_805_007, "bad K_rem proved")
    ensure(cert["conditional_ledger"]["K_rem_conditional"] == 4_805_007, "bad K_rem conditional")
    branches = cert["first_match_branches"]
    ensure([row["order"] for row in branches] == list(range(1, len(branches) + 1)), "branch order mismatch")
    ensure(
        sum(1 for row in branches if row.get("deducted_in_proved_ledger")) == 2,
        "generated collision and terminal quotient should be deducted as proved",
    )
    ensure(
        cert["quotient_planted_descent"]["terminal_raw_paid_cost"] == 471_447_040,
        "terminal quotient block mismatch",
    )
    ensure(cert["quotient_planted_descent"]["step"] == "Q0", "quotient block should be Q0")
    ensure(
        [row["c"] for row in cert["quotient_planted_descent"]["exact_quotient_descent_rungs"]]
        == [2, 4, 8, 16],
        "Q0 exact quotient rung list mismatch",
    )
    ensure(
        len(cert["quotient_planted_descent"]["lower_rung_obligations"]) == 15,
        "Q0 lower-rung obligation count mismatch",
    )
    ensure(
        [row["c"] for row in cert["quotient_planted_descent"]["open_planted_tail_rungs"]]
        == [262_144, 524_288, 1_048_576, 2_097_152],
        "Q0 open planted-tail rung list mismatch",
    )
    ensure(
        cert["honest_cyclotomic_exact_lift_fiber_bound"]["honest_cyclotomic_exact_fiber_bound"] == 11_440,
        "honest exact-lift bound mismatch",
    )
    ensure(
        cert["q1_collision_ledger"]["status"] == "PROVED_EXACT_PAIR_DECOMPOSITION_AND_TOY_REPLAY",
        "Q1 collision ledger status mismatch",
    )
    ensure(
        cert["q1_collision_ledger"]["deployed_parameters"]["minimum_nontrivial_one_sided_difference"]
        == W_PREFIX + 1,
        "Q1 deployed distance mismatch",
    )
    ensure(
        [case["minimum_nontrivial_one_sided_difference"] for case in cert["q1_collision_ledger"]["toy_replay_cases"]]
        == [2, 3, 4, 3],
        "Q1 toy replay minima mismatch",
    )
    ensure(
        cert["q2_symmetry_descent"]["status"]
        == "PROVED_STABILIZER_FORCING_CONDITIONAL_ON_HEAVY_COUNT_BOUND",
        "Q2 symmetry status mismatch",
    )
    ensure(
        cert["q2_symmetry_descent"]["deployed_thresholds"][0]["forced_stabilizer_at_least"] == 2
        and cert["q2_symmetry_descent"]["deployed_thresholds"][0]["sufficient_heavy_target_count_bound"] == N // 2,
        "Q2 first deployed threshold mismatch",
    )
    ensure(
        cert["q2_symmetry_descent"]["toy_replay_cases"][1]["stabilizer_distribution_on_heavy_targets"] == {"2": 8},
        "Q2 stabilizer replay mismatch",
    )
    ensure(
        cert["q2_folding_stabilized_fiber_rigidity"]["status"]
        == "PROVED_EXACT_LIFT_FINITE_CONDITIONAL_ON_GENERATED_PREFIX_BUCKET",
        "Q2 folding status mismatch",
    )
    ensure(
        cert["q2_folding_stabilized_fiber_rigidity"]["quotient_descended_h"] == [2, 4, 8, 16],
        "Q2 folding quotient h mismatch",
    )
    ensure(
        cert["q2_folding_stabilized_fiber_rigidity"]["empty_exact_lift_h"]
        == [32, 64, 128, 256, 512, 1_024, 2_048, 4_096, 8_192, 16_384, 32_768, 65_536, 131_072],
        "Q2 folding empty h mismatch",
    )
    ensure(
        cert["q2_folding_stabilized_fiber_rigidity"]["finite_wrapper"]["generated_cells_used_bound"]
        < cert["q2_folding_stabilized_fiber_rigidity"]["finite_wrapper"]["generated_cells_budgeted_t_times_p"],
        "Q2 folding generated-prefix cell bound should fit under t*p",
    )
    q2_closure = cert["q2_heavy_fiber_closure"]
    ensure(
        q2_closure["status"] == "CONDITIONAL_ON_PRIMITIVE_HEAVY_ORBIT_EXCLUSION",
        "Q2 closure status mismatch",
    )
    ensure(
        q2_closure["primitive_heavy_orbit_input"]["stronger_but_not_needed"]
        == "|{z : |R_pre(z)| > threshold}| <= 1048576",
        "Q2 closure stronger count target mismatch",
    )
    ensure(q2_closure["generated_prefix_bucket"]["max_cells_if_separate"] == 70_748_471_296, "Q2 closure prefix cell count mismatch")
    ensure(q2_closure["generated_prefix_bucket"]["K_if_deducted_separately"] == 4_805_006, "Q2 closure separate K mismatch")
    ensure(
        [row["h"] for row in q2_closure["lower_rung_exact_lift_certificates"]] == [2, 4, 8, 16],
        "Q2 closure lower-rung h list mismatch",
    )
    ensure(
        q2_closure["generated_lift_class_pointwise_route"]["status"]
        == "CONDITIONAL_ON_GENERATED_PREFIX_SUPPORT_MULTIPLICITY_CERTIFICATE",
        "Q2 lift-class route status mismatch",
    )
    ensure(
        q2_closure["generated_prefix_support_multiplicity_target"]["status"]
        == "OPEN_REQUIRED_SUPPORT_MULTIPLICITY_CERTIFICATE",
        "Q2 support multiplicity status mismatch",
    )
    ensure(
        q2_closure["generated_prefix_support_multiplicity_target"]["convenient_bound_fits_threshold"],
        "Q2 convenient support bound should fit threshold",
    )
    ensure(
        all(row["exact_lift_max_fiber_bound"] == 11_440 for row in q2_closure["lower_rung_exact_lift_certificates"]),
        "Q2 closure lower-rung exact-lift bound mismatch",
    )
    prefix_counterexample = cert["generated_prefix_support_payment_counterexample"]
    ensure(
        prefix_counterexample["nonretained_supports_after_keeping_largest_class"]
        > prefix_counterexample["w_times_p_image_cell_bound"],
        "generated-prefix support counterexample should exceed image-cell bound",
    )
    ensure(
        prefix_counterexample["target_stabilizer_size"] == 1,
        "generated-prefix counterexample target should be primitive",
    )
    q2_routes = cert["q2_failed_route_evidence"]
    ensure(q2_routes["status"] == "EVIDENCE_RECORDED_NO_Q2_CLOSURE", "Q2 route evidence status mismatch")
    ensure(
        q2_routes["remaining_q2_target"]["threshold_floor"] == 274_836_936_291_722_953,
        "Q2 route evidence threshold floor mismatch",
    )
    ensure(
        q2_routes["remaining_q2_target"]["conditional_support_bound_t_p_plus_retained"]
        == 143_763_024_458_816,
        "Q2 route evidence support bound mismatch",
    )
    ensure(
        q2_routes["route_A_delsarte_distance_attempt"]["status"]
        == "OPEN_MISSING_ROUTE_A_DUAL_EXCESS_CERTIFICATE",
        "Route A status mismatch",
    )
    ensure(
        q2_routes["route_B_split_pair_rank_attempt"]["status"]
        == "PROVED_LOCAL_FULL_ROW_RANK_ONLY_INSUFFICIENT",
        "Route B status mismatch",
    )
    ensure(
        q2_routes["route_C_primitive_orbit_excess_attempt"]["status"]
        == "OPEN_REQUIRED_PRIMITIVE_EXCESS_CERTIFICATE",
        "Route C status mismatch",
    )
    ensure(
        q2_routes["route_D_folding_defect_transfer_attempt"]["status"]
        == "OPEN_MISSING_ROUTE_D_FOLDING_DEFECT_SUPPORT_CERTIFICATE",
        "Route D status mismatch",
    )
    ensure(
        q2_routes["route_D_folding_defect_transfer_attempt"]["diagnostics"][
            "first_allowed_nonzero_signed_defect_size"
        ]
        == 33_737,
        "Route D first signed-defect size mismatch",
    )
    ensure(
        cert["q1_distance_insufficiency"]["status"] == "PROVED_DISTANCE_ONLY_INSUFFICIENT",
        "Q1 distance insufficiency status mismatch",
    )
    ensure(
        cert["split_prefix_collision_distance"]["parameters"]["minimum_one_sided_difference"] == W_PREFIX + 1,
        "split-prefix collision distance mismatch",
    )
    ensure(
        cert["conditional_first_match_closure"]["status"]
        == "CONDITIONAL_ON_ALL_NAMED_OPEN_BRANCH_PAYMENTS",
        "conditional closure status mismatch",
    )
    ensure(
        cert["finite_field_guardrail"]["g3_exact_nonzero"]
        and cert["finite_field_guardrail"]["g3_mod_p"] == 0,
        "finite-field guardrail mismatch",
    )


def render_report(cert: dict[str, Any]) -> str:
    arith = cert["deployed_arithmetic"]
    lines = [
        "# KB-MCA 1116048 first-match ledger v1 report",
        "",
        f"Status: `{cert['status']}`.",
        "",
        "This report records exact arithmetic for the KoalaBear MCA adjacent candidate `A=1116048`",
        "partial first-match ledger and discharges the generated-field collision image-cell bucket",
        "plus terminal raw-paid quotient/planted rungs.",
        "It does not prove `U(1116048) <= B*`, the first-safe agreement, or primitive Q-fin flatness.",
        "",
        "## Deployed constants",
        "",
        f"- `p = {arith['p']}`.",
        f"- `q_gen = {cert['row_packet']['q_gen']}`.",
        f"- `q_line = p^6 = {arith['q_line']}`.",
        f"- `q_chal = {cert['row_packet']['q_chal']}`.",
        f"- `q_list = {cert['row_packet']['q_list']}`.",
        f"- `B* = floor((q_line - 1)/2^128) = {arith['B_star_floor_q_minus_1_over_2^128']}`.",
        f"- `(n,k,A,j,t,w) = ({arith['n']}, {arith['k']}, {arith['A_adjacent_candidate']}, {arith['j']}, {arith['t']}, {arith['prefix_depth_w']})`.",
        f"- `log2(avg) = {arith['log2_average']:.12f}`.",
        f"- `raw margin = {arith['raw_margin_bits']:.12f}` bits.",
        f"- `K_raw = {arith['K_raw']}`.",
        "",
        "## Generated-field collision bucket",
        "",
        f"- `B_gen <= t*p = {arith['B_gen_t_times_p']}`.",
        f"- `B_rem_after_gen = B* - B_gen = {arith['B_rem_after_generated_collision']}`.",
        f"- `K_after_gen = {arith['K_after_generated_collision']}`.",
        "",
        "This is an image-cell cost over base generated slopes.  It is not a raw support bound.",
        "",
        "## Q0 quotient/planted rung audit",
        "",
        f"Status: `{cert['quotient_planted_descent']['status']}`.",
        "",
        "The dyadic quotient/planted descent theorem injects each covered top fiber",
        "into a lower prefix fiber when `r_c <= w`.  The terminal covered rungs",
        "`c=65536` and `c=131072` are paid by raw lower quotient count.",
        "",
        f"- `B_quot_terminal = {cert['quotient_planted_descent']['terminal_raw_paid_cost']}`.",
        f"- `B_rem_after_gen_and_terminal_quotient = {arith['B_rem_after_generated_collision_and_terminal_quotient']}`.",
        f"- `K_after_gen_and_terminal_quotient = {arith['K_after_generated_collision_and_terminal_quotient']}`.",
        f"- exact quotient-descent rungs needing lower bounds: `{[row['c'] for row in cert['quotient_planted_descent']['exact_quotient_descent_rungs']]}`.",
        f"- planted-descent rungs needing lower bounds: `{[row['c'] for row in cert['quotient_planted_descent']['planted_descent_needs_lower_rung_bound']]}`.",
        f"- open planted-tail rungs: `{[row['c'] for row in cert['quotient_planted_descent']['open_planted_tail_rungs']]}`.",
        "",
        "| c | n_c | A_c | j_c | r_c | w_c | status | K_c |",
        "| -: | -: | -: | -: | -: | -: | --- | -: |",
    ]
    for row in cert["quotient_planted_descent"]["rungs"]:
        lines.append(
            "| {c} | {n_c} | {A_c} | {j_c} | {r_c} | {w_c} | `{status}` | {K_c} |".format(
                c=row["c"],
                n_c=row["n_c"],
                A_c=row["A_c"],
                j_c=row["j_c"],
                r_c=row["r_c"],
                w_c=row["w_c"],
                status=row["status"],
                K_c=row["K_c_at_current_B_rem"],
            )
        )
    lines.extend(
        [
            "",
            "Q0 lower-rung obligations:",
            "",
            "| c | n_c | j_c | w_c | required K_c |",
            "| -: | -: | -: | -: | -: |",
        ]
    )
    for row in cert["quotient_planted_descent"]["lower_rung_obligations"]:
        lines.append(
            "| {c} | {n_c} | {j_c} | {w_c} | {required_multiplier_K_c} |".format(**row)
        )
    q1 = cert["q1_collision_ledger"]
    lines.extend(
        [
            "",
            "## Q1 exact split-prefix collision ledger",
            "",
            f"Status: `{q1['status']}`.",
            "",
            q1["exact_second_moment_identity"]["statement"],
            "",
            q1["exact_second_moment_identity"]["factorized_form"],
            "",
            q1["exact_second_moment_identity"]["minimal_collision_clause"],
            "",
            f"- deployed minimum nontrivial one-sided difference: `{q1['deployed_parameters']['minimum_nontrivial_one_sided_difference']}`.",
            f"- deployed forbidden one-sided differences: `1..{q1['deployed_parameters']['forbidden_one_sided_differences'][1]}`.",
            f"- `gcd(n,w+1) = {q1['deployed_parameters']['gcd_n_w_plus_1']}`.",
            f"- `w+1` divides `n`: `{q1['deployed_parameters']['w_plus_1_divides_n']}`.",
            "",
            "Toy replay cases:",
            "",
            "| field | n | j | w | supports | fibers | max fiber | second moment | min e>0 |",
            "| --- | -: | -: | -: | -: | -: | -: | -: | -: |",
        ]
    )
    for case in q1["toy_replay_cases"]:
        lines.append(
            "| {field} | {n} | {j} | {w} | {total_supports} | {fiber_count} | {max_fiber} | {second_moment} | {minimum_nontrivial_one_sided_difference} |".format(
                **case
            )
        )
    lines.extend(
        [
            "",
            "Q1 proves the exact collision decomposition and the low-distance gap.",
            "It does not evaluate all deployed `C_e` summands and does not prove",
            "the finite worst-case max-fiber bound.",
        ]
    )
    q2 = cert["q2_symmetry_descent"]
    lines.extend(
        [
            "",
            "## Q2 heavy-fiber twist-stabilizer descent",
            "",
            f"Status: `{q2['status']}`.",
            "",
            q2["statement"],
            "",
            "Deployed stabilizer thresholds:",
            "",
            "| forced stabilizer >= h | sufficient heavy-target count <= | quotient depth floor(w/h) |",
            "| -: | -: | -: |",
        ]
    )
    for row in q2["deployed_thresholds"][:8]:
        lines.append(
            "| {forced_stabilizer_at_least} | {sufficient_heavy_target_count_bound} | {quotient_prefix_depth_floor_w_over_h} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "Toy replay cases:",
            "",
            "| field | n | j | w | max fiber | heavy targets | heavy < n? | stabilizers |",
            "| --- | -: | -: | -: | -: | -: | --- | --- |",
        ]
    )
    for case in q2["toy_replay_cases"]:
        lines.append(
            "| {field} | {n} | {j} | {w} | {max_fiber} | {heavy_target_count} | {heavy_target_count_less_than_n} | `{stabilizer_distribution_on_heavy_targets}` |".format(
                **case
            )
        )
    lines.extend(
        [
            "",
            "Q2 proves the symmetry/stabilizer forcing step.  It still needs an",
            "evaluated heavy-target bound from Q1/higher moments before it can",
            "activate the folding theorem below.",
        ]
    )
    q2_fold = cert["q2_folding_stabilized_fiber_rigidity"]
    lines.extend(
        [
            "",
            "## Q2 stabilized-fiber folding rigidity",
            "",
            f"Status: `{q2_fold['status']}`.",
            "",
            q2_fold["theorem"],
            "",
            "Finite KoalaBear use is conditional on the generated first-match",
            "bucket including prefix-coordinate lift collisions.  Under that",
            "wrapper, generated-prefix cells use at most:",
            "",
            f"- `w*p = {q2_fold['finite_wrapper']['generated_cells_used_bound']}`.",
            f"- budgeted `t*p = {q2_fold['finite_wrapper']['generated_cells_budgeted_t_times_p']}`.",
            f"- slack `{q2_fold['finite_wrapper']['slack']}`.",
            "",
            f"Quotient-descended stabilizers: `{q2_fold['quotient_descended_h']}`.",
            f"Empty exact-lift stabilizers: `{q2_fold['empty_exact_lift_h']}`.",
            f"Not applicable because `h/2>w`: `{q2_fold['not_applicable_h']}`.",
            "",
            "| h | h/2 | n/h | j/h or rem | floor(w/h) | exact-lift outcome |",
            "| -: | -: | -: | ---: | -: | --- |",
        ]
    )
    for row in q2_fold["deployed_h_rows"]:
        j_status = row["j_div_h"] if row["h_divides_j"] else f"rem {row['j_mod_h']}"
        lines.append(
            "| {h} | {h_over_2} | {n_over_h} | {j_status} | {floor_w_over_h} | `{outcome}` |".format(
                h=row["h"],
                h_over_2=row["h_over_2"],
                n_over_h=row["n_over_h"],
                j_status=j_status,
                floor_w_over_h=row["floor_w_over_h"],
                outcome=row["exact_lift_outcome"],
            )
        )
    lines.extend(
        [
            "",
            "Thus a stabilized target is not remaining top-rung primitive mass after",
            "generated-prefix lift collisions are removed: it either descends to",
            "one of the Q0 quotient rungs `h=2,4,8,16`, or is empty in the exact",
            "lift for `h=32,...,131072`.",
        ]
    )
    q2_close = cert["q2_heavy_fiber_closure"]
    lines.extend(
        [
            "",
            "## Q2 heavy-fiber closure theorem",
            "",
            f"Status: `{q2_close['status']}`.",
            "",
            q2_close["closure_statement"],
            "",
            "The remaining open input is the primitive-heavy-orbit exclusion certificate:",
            "",
            f"```text\n{q2_close['primitive_heavy_orbit_input']['target']}\n```",
            "",
            "The stronger global count bound",
            "",
            f"```text\n{q2_close['primitive_heavy_orbit_input']['stronger_but_not_needed']}\n```",
            "",
            "would imply this, but is not necessary.",
            "",
            "Generated-prefix lift collisions on certified heavy targets are covered by:",
            "",
            f"- cell model: `{q2_close['generated_prefix_bucket']['cell_model']}`.",
            f"- separate worst-case cells at `h=2`: `{q2_close['generated_prefix_bucket']['max_cells_if_separate']}`.",
            f"- existing generated allowance `t*p`: `{q2_close['generated_prefix_bucket']['existing_generated_allowance_t_times_p']}`.",
            f"- `K` if deducted separately: `{q2_close['generated_prefix_bucket']['K_if_deducted_separately']}`.",
            "",
            "Do not claim no new cost unless these generated-prefix cells are explicitly",
            "coalesced into the generated first-match bucket.",
            "",
            "Lower-rung exact-lift certificates for quotient-descended heavy targets:",
            "",
            "| h | N | J | W | K_h | exact-lift max fiber | status |",
            "| -: | -: | -: | -: | -: | -: | --- |",
        ]
    )
    for row in q2_close["lower_rung_exact_lift_certificates"]:
        lines.append(
            "| {h} | {N} | {J} | {W} | {K_h} | {exact_lift_max_fiber_bound} | `{status}` |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "These four exact-lift bounds do not prove finite lower-rung flatness by",
            "themselves; finite use still requires generated-prefix lift collision",
            "handling.  They do show that once lifted, the descended rows are far below",
            "their printed `K_h * average` targets.",
            "",
            "Conditional pointwise route:",
            "",
            q2_close["generated_lift_class_pointwise_route"]["claim_if_bucket_is_paid"],
            "",
            q2_close["generated_lift_class_pointwise_route"]["why_not_marked_proved_here"],
            "",
            "The exact remaining support-level certificate is:",
            "",
            f"```text\n{q2_close['generated_prefix_support_multiplicity_target']['sufficient_deployed_bound']}\n```",
            "",
            "A convenient stronger bound would be:",
            "",
            f"```text\n{q2_close['generated_prefix_support_multiplicity_target']['convenient_stronger_bound']}\n```",
            "",
            q2_close["generated_prefix_support_multiplicity_target"]["why_this_is_still_the_Q2_bottleneck"],
        ]
    )
    prefix_counter = cert["generated_prefix_support_payment_counterexample"]
    lines.extend(
        [
            "",
            "## Generated-prefix support-payment counterexample",
            "",
            f"Status: `{prefix_counter['status']}`.",
            "",
            "This small replay shows why a generated-prefix image-cell label is not",
            "a support/fiber payment.",
            "",
            "| field | n | j | w | primitive target | finite fiber | exact lift classes | largest lift class | non-retained supports | w*p |",
            "| --- | -: | -: | -: | -: | -: | -: | -: | -: | -: |",
            "| {field} | {n} | {j} | {w} | {primitive_target} | {finite_fiber_size} | {exact_lift_classes} | {largest_exact_lift_class} | {nonretained_supports_after_keeping_largest_class} | {w_times_p_image_cell_bound} |".format(
                **prefix_counter
            ),
            "",
            prefix_counter["meaning"],
        ]
    )
    route_evidence = cert["q2_failed_route_evidence"]
    lines.extend(
        [
            "",
            "## Q2 failed-route evidence",
            "",
            f"Status: `{route_evidence['status']}`.",
            "",
            "The attempted Route A/B/C/D packets are recorded as evidence and",
            "interfaces for future certificates.  They do not close Q2.",
            "",
            "The common remaining target is:",
            "",
            f"```text\n{route_evidence['remaining_q2_target']['statement']}\n```",
            "",
            "Conditional arithmetic:",
            "",
            f"- retained exact-lift bound: `{route_evidence['remaining_q2_target']['retained_exact_lift_bound']}`.",
            f"- `t*p`: `{route_evidence['remaining_q2_target']['t_times_p']}`.",
            f"- `t*p + retained`: `{route_evidence['remaining_q2_target']['conditional_support_bound_t_p_plus_retained']}`.",
            f"- threshold floor: `{route_evidence['remaining_q2_target']['threshold_floor']}`.",
            f"- slack bits: `{route_evidence['remaining_q2_target']['slack_bits_vs_t_p_plus_retained']:.6f}`.",
            "",
            "| route | status | key diagnostic |",
            "| --- | --- | --- |",
            "| A / Delsarte-distance | `{}` | Gilbert lower-bound gap vs `t*p`: `{:.6f}` bits |".format(
                route_evidence["route_A_delsarte_distance_attempt"]["status"],
                route_evidence["route_A_delsarte_distance_attempt"]["diagnostics"]["gap_bits_vs_t_p"],
            ),
            "| B / split-pair rank | `{}` | local rank `{}`, nullity `{}`, naive gap `{:.6f}` bits |".format(
                route_evidence["route_B_split_pair_rank_attempt"]["status"],
                route_evidence["route_B_split_pair_rank_attempt"]["diagnostics"]["rank"],
                route_evidence["route_B_split_pair_rank_attempt"]["diagnostics"]["minimum_nullity"],
                route_evidence["route_B_split_pair_rank_attempt"]["diagnostics"]["gap_naive_full_rank_vs_t_p"],
            ),
            "| C / primitive excess | `{}` | q=3 tuple threshold log2 `{:.6f}` |".format(
                route_evidence["route_C_primitive_orbit_excess_attempt"]["status"],
                route_evidence["route_C_primitive_orbit_excess_attempt"]["diagnostics"][
                    "q3_minimum_ordered_tuple_log2"
                ],
            ),
            "| D / folding defect | `{}` | first nonzero signed defect `{}`, gap `{:.6f}` bits |".format(
                route_evidence["route_D_folding_defect_transfer_attempt"]["status"],
                route_evidence["route_D_folding_defect_transfer_attempt"]["diagnostics"][
                    "first_allowed_nonzero_signed_defect_size"
                ],
                route_evidence["route_D_folding_defect_transfer_attempt"]["diagnostics"]["gap_bits_vs_t_p"],
            ),
            "",
            "Route D is the most useful next structure, but it still needs:",
            "",
            f"```text\n{route_evidence['route_D_folding_defect_transfer_attempt']['next_theorem']}\n```",
        ]
    )
    q1_gap = cert["q1_distance_insufficiency"]
    lines.extend(
        [
            "",
            "## Q1 distance-only insufficiency",
            "",
            f"Status: `{q1_gap['status']}`.",
            "",
            q1_gap["statement"],
            "",
            f"- `log2 Johnson ball radius e-1 = {q1_gap['johnson_ball_log2_radius_e_minus_1']:.6f}`.",
            f"- `log2 binom(n,j) = {q1_gap['total_support_log2']:.6f}`.",
            f"- `log2 greedy distance-code lower bound = {q1_gap['greedy_distance_code_lower_bound_log2']:.6f}`.",
            f"- `log2(n*T) = {q1_gap['log2_n_times_threshold_T']:.6f}`.",
            "",
            q1_gap["interpretation"],
        ]
    )
    split = cert["split_prefix_collision_distance"]
    lines.extend(
        [
            "",
            "## Split-prefix collision distance",
            "",
            f"Status: `{split['status']}`.",
            "",
            "If two distinct split supports have the same first `w` locator-prefix",
            "coefficients, then their common-prefix collision has large support distance.",
            "",
            f"- one-sided difference lower bound: `{split['parameters']['minimum_one_sided_difference']}`.",
            f"- symmetric-difference lower bound: `{split['parameters']['minimum_symmetric_difference']}`.",
            "",
            "This is useful Q1 collision rigidity, but it is not a worst-case fiber",
            "bound; the remaining primitive max-orbit certificate is still open.",
        ]
    )
    lift = cert["honest_cyclotomic_exact_lift_fiber_bound"]
    lines.extend(
        [
            "",
            "## Honest exact-lift fiber bound",
            "",
            f"Status: `{lift['status']}`.",
            "",
            "Over the honest cyclotomic model, equality of the first `w` prefix",
            "coordinates forces terminal `16`-coset periodicity because `w >= 2^16`.",
            "",
            f"- terminal coset size: `{lift['terminal_coset_size']}`.",
            f"- exact honest prefix-fiber bound: `{lift['honest_cyclotomic_exact_fiber_bound']}`.",
            "",
            "This bound is deliberately not deducted as a finite-field first-match",
            "payment.  The missing input is a valid finite-field lift-class cost",
            "model for prefix-vector fibers.",
        "",
        "## First-match table",
        "",
        "| order | branch | status | cost | deducted proved? |",
        "| -: | --- | --- | ---: | --- |",
        ]
    )
    for row in cert["first_match_branches"]:
        cost = "" if row["cost"] is None else str(row["cost"])
        lines.append(
            "| {order} | `{branch}` | `{status}` | {cost} | {deducted} |".format(
                order=row["order"],
                branch=row["branch"],
                status=row["status"],
                cost=cost,
                deducted="yes" if row.get("deducted_in_proved_ledger") else "no",
            )
        )
    lines.extend(
        [
            "",
            "## Partial paid-cell ledger",
            "",
            "This is not a complete `U(1116048)` upper ledger.",
            "",
            f"- `B_paid_proved = {cert['partial_paid_ledger']['B_paid_proved']}`.",
            f"- `B_rem_proved = {cert['partial_paid_ledger']['B_rem_proved']}`.",
            f"- `K_rem_proved = {cert['partial_paid_ledger']['K_rem_proved']}`.",
            "",
            "Open branches:",
            "",
        ]
    )
    for cell in cert["partial_paid_ledger"]["unpaid_residual_cells"]:
        lines.append(f"- `{cell['name']}`: `{cell['status']}`.")
    closure = cert["conditional_first_match_closure"]
    lines.extend(
        [
            "",
            "## Conditional closure theorem",
            "",
            f"Status: `{closure['status']}`.",
            "",
            "This packet records only the implication shape for a future complete",
            "safe-side certificate.  It does not prove `U(1116048) <= B*`.",
            "",
            "Required future inputs:",
            "",
        ]
    )
    for assumption in closure["assumptions_required"]:
        lines.append(f"- {assumption}")
    lines.extend(
        [
            "",
            f"Remaining budget: `{closure['remaining_budget']}`.",
            f"Required multiplier: `{closure['K_rem']}`.",
            f"Conclusion if all inputs exist: {closure['conclusion_if_all_assumptions_hold']}.",
            "",
            closure["not_proved_here"],
        ]
    )
    lines.extend(
        [
            "",
            "## Finite-field guardrail",
            "",
        ]
    )
    guard = cert["finite_field_guardrail"]
    lines.append(
        "The `{{1,3}}` support `{}` over `{}` is a finite survivor with slope `{}`, "
        "but its honest cyclotomic defect is nonzero and reduces to zero modulo `17`.".format(
            guard["support_exponents"], guard["field"], guard["forced_slope"]
        )
    )
    lines.extend(
        [
            "",
            "## Next target",
            "",
            f"`{cert['next_target']['name']}`.",
            "",
            f"Target multiplier under the proved ledger: `K_rem = {cert['next_target']['proved_K_rem_current']}`.",
            "",
            "The theorem to prove is:",
            "",
            f"```text\n{cert['next_target']['statement']}\n```",
            "",
            "## Q1 and Q2 plan",
            "",
            f"### Q1: {cert['q1_q2_plan']['Q1']['name']}",
            "",
            f"Status: `{cert['q1_q2_plan']['Q1']['status']}`.",
            "",
            cert["q1_q2_plan"]["Q1"]["target"],
            "",
            "Deliverables:",
            "",
        ]
    )
    for item in cert["q1_q2_plan"]["Q1"]["deliverables"]:
        lines.append(f"- {item}.")
    lines.extend(
        [
            "",
            "Proof ideas:",
            "",
        ]
    )
    for item in cert["q1_q2_plan"]["Q1"]["proof_ideas"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            f"### Q2: {cert['q1_q2_plan']['Q2']['name']}",
            "",
            f"Status: `{cert['q1_q2_plan']['Q2']['status']}`.",
            "",
            cert["q1_q2_plan"]["Q2"]["target"],
            "",
            "Deliverables:",
            "",
        ]
    )
    for item in cert["q1_q2_plan"]["Q2"]["deliverables"]:
        lines.append(f"- {item}.")
    lines.extend(
        [
            "",
            "Proof ideas:",
            "",
        ]
    )
    for item in cert["q1_q2_plan"]["Q2"]["proof_ideas"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "Remaining ledger work:",
            "",
        ]
    )
    for item in cert["next_target"]["remaining_ledger_work"]:
        lines.append(f"- {item}.")
    lines.append("")
    return "\n".join(lines)


def render_cert_readme(cert: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# KB-MCA 1116048 first-match ledger v1 certificate",
            "",
            f"Status: `{cert['status']}`.",
            f"Claim class: `{cert['claim_class']}`.",
            "",
            "Generated artifacts for the KoalaBear MCA `A=1116048` partial first-match ledger audit.",
            "",
            "**This packet does not prove `U(1116048) <= B*`, does not certify the",
            "KoalaBear MCA first-safe agreement, and does not promote v13 raw material",
            "into Paper D.**",
            "",
            "## Files",
            "",
            "- `kb_mca_1116048_first_match_ledger_v1.json`: machine-readable certificate.",
            "- `README.md`: this generated certificate-directory summary.",
            "- `experimental/notes/certificate_scanner/outputs/kb_mca_1116048_first_match_ledger_v1.report.md`: generated Markdown report.",
            "",
            "## Regeneration",
            "",
            "```bash",
            "python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --write",
            "python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --check",
            "python3 experimental/scripts/verify_kb_mca_1116048_first_match_ledger_v1.py --full --check",
            "python3 -m json.tool experimental/data/certificates/kb-mca-1116048-first-match-ledger-v1/kb_mca_1116048_first_match_ledger_v1.json",
            "```",
            "",
            "## Partial claim",
            "",
            "The generated-field collision bucket is paid by row-indexed generated-slope image cells",
            "with cost `B_gen <= t*p`.  Q0 records the dyadic quotient/planted rung audit:",
            "descent holds for every rung with `r_c<=w`, terminal rungs `c=65536,131072`",
            "are raw-paid, and the remaining covered rungs are emitted as explicit lower-rung",
            "max-fiber obligations.  The proved remaining multiplier is still `K_rem=4805007`.",
            "",
            "Q1 records the exact split-prefix collision decomposition:",
            "`sum_z N_w(z)^2 = binom(n,j) + sum_{e=w+1}^{min(j,n-j)} C_e`,",
            "where `C_e` counts ordered support-pair collisions at one-sided",
            "difference `e`.  The verifier replays this decomposition on small",
            "cyclic-domain examples.",
            "",
            "Q2 records the heavy-fiber twist-stabilizer theorem: the `mu_n` twist",
            "action preserves prefix-fiber size, so a sufficiently small heavy-target",
            "set forces nontrivial stabilizer and hence quotient-supported prefix",
            "coordinates.  The verifier replays this stabilizer forcing on small",
            "cyclic-domain examples.",
            "",
            "Q2 also records the stabilized-fiber folding theorem.  Over exact",
            "lifted cyclotomic fibers, an `h`-stabilized target with `h/2<=w`",
            "forces every support in the fiber to be a union of `h`-cosets.",
            "For finite KoalaBear use this is conditional on the generated bucket",
            "including prefix-coordinate lift collisions.  Under that wrapper,",
            "`h=2,4,8,16` descend to Q0 quotient rungs and `h=32,...,131072`",
            "are empty in the exact lift because `h` does not divide `j=981104`.",
            "",
            "The Q2 closure block records the precise remaining input:",
            "primitive-heavy-orbit exclusion, or equivalently a support-level",
            "generated-prefix multiplicity certificate for non-retained exact",
            "lift classes.  The stronger global count `#heavy<=n/2` would imply",
            "primitive-heavy exclusion, but is not necessary.  At the first useful",
            "scale `h=2`, the heavy-target generated-prefix bucket has at most",
            "`70748471296` image cells if paid separately, and the four",
            "quotient-descended exact-lift lower rows all have max fiber bound `<=11440`.",
            "",
            "The packet includes a small `F_17, n=16, j=8, w=1` replay showing",
            "that generated-prefix image cells are not support payments: for the",
            "primitive finite target `z=1`, there are `737` non-retained supports",
            "after keeping the largest exact lift class, while `w*p=17`.",
            "",
            "The packet also records failed-route evidence for Q2: Route A",
            "(Delsarte/distance), Route B (local split-pair rank), Route C",
            "(primitive excess moments), and Route D (dyadic folding defects).",
            "Each is kept at its honest status.  Route D supplies the most useful",
            "next target, but still lacks the large signed folding-defect support",
            "certificate needed to pay generated-prefix multiplicity.",
            "",
            "The packet also records why Q1 distance alone cannot prove that",
            "orbitwise certificate: the Johnson-packing gap remains enormous.",
            "",
            "The certificate proves the split-prefix collision-distance lemma: two distinct",
            "supports in the same prefix fiber differ in at least `w+1=67472` points on",
            "each side.  This is supporting rigidity, not the missing max-fiber theorem.",
            "",
            "The certificate also records an honest cyclotomic exact-lift fiber bound `<=11440`.",
            "That bound is not deducted for finite-field use because a valid finite-field lift-class",
            "image cost model remains open.",
            "",
            "## Remaining Q2 follow-up",
            "",
            "Q1 is now proved as an exact pair-decomposition, and Q2 is proved as",
            "twist-stabilizer forcing plus exact-lift folding rigidity.  The remaining",
            "Q2 work is to supply a primitive-heavy-orbit exclusion certificate",
            "from Q1/higher moments, or a support-level generated-prefix",
            "multiplicity certificate for deployed use.  Once that orbitwise",
            "certificate exists, Q2 routes threatening stabilized targets to generated-prefix",
            "cells, empty exact-lift branches, or the four exact-lift-certified",
            "quotient rungs `h=2,4,8,16`.",
            "",
            "## Nonclaims",
            "",
            "- Does not prove primitive Q-fin max-orbit flatness.",
            "- Does not pay extension-valued, quotient/planted, sparse, or arbitrary M1 branches.",
            "- Does not prove the Q0 lower-rung quotient/planted max-fiber bounds for `c=2..32768`.",
            "- Does not pay arbitrary planted tails with `r_c>w`.",
            "- Does not prove finite-field lift-class removal at cost `w*p` for prefix-vector fibers.",
            "- Does not prove support multiplicity bounds for non-retained generated-prefix exact lift classes.",
            "- Does not prove primitive-heavy-orbit exclusion needed to activate Q2 stabilizer forcing.",
            "- Does not bound raw support multiplicity inside generated-field image cells.",
            "",
        ]
    )


def json_bytes(cert: dict[str, Any]) -> bytes:
    return (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")


def report_bytes(cert: dict[str, Any]) -> bytes:
    return render_report(cert).encode("utf-8")


def cert_readme_bytes(cert: dict[str, Any]) -> bytes:
    return render_cert_readme(cert).encode("utf-8")


def write_artifacts(cert: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_bytes(json_bytes(cert))
    CERT_README_PATH.write_bytes(cert_readme_bytes(cert))
    REPORT_PATH.write_bytes(report_bytes(cert))


def check_artifacts(cert: dict[str, Any]) -> None:
    assert_certificate(cert)
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


def load_artifact_certificate() -> dict[str, Any]:
    if not CERT_PATH.exists():
        raise AssertionError(f"missing certificate JSON: {CERT_PATH}")
    cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    assert_certificate(cert)
    return cert


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--full", action="store_true", help="recompute the full certificate before checking")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    cert = build_certificate() if (args.write or args.full) else load_artifact_certificate()
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
        print(f"B_gen: {cert['deployed_arithmetic']['B_gen_t_times_p']}")
        print(f"K_rem_proved: {cert['partial_paid_ledger']['K_rem_proved']}")
        print("RESULT: PASS")


if __name__ == "__main__":
    main()
