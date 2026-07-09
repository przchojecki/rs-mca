#!/usr/bin/env python3
"""Verify the row-sharp Q singleton-heavy top-seam packet.

Status: CONDITIONAL_ON_WEIGHTED_PRIMITIVE_SP_PADE_BOUND_AND_PLANTED_CORE_COST_BOUND_AND_STRICT_DISTANCE_AND_ROW_BUDGET_SCOPE.

This packet records the useful local theorem extracted from the Route-D
experiments: singleton-heavy top-seam branch excess can be paid by top-seam
witness packets if repeated side-pair reuse is routed as a planted-switch
core-fiber branch with printed support cost, if the multiplicity-aware
SP/Padé certificates produced by same-cell cross pairs have a printed finite
primitive bound, if the strict-distance child predicate is a formal paid
first-match branch, and if the charged rows are budgeted by at most t rows.

It deliberately does not claim the row-sharp Q-prefix atom theorem or
U(1116048) <= B*.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = ROOT / "experimental" / "data" / "certificates" / "rowsharp-q-singleton-topseam-v1"
CERT_PATH = CERT_DIR / "rowsharp_q_singleton_topseam_v1.json"
CERT_README_PATH = CERT_DIR / "README.md"
NOTE_PATH = ROOT / "experimental" / "notes" / "thresholds" / "rowsharp_q_singleton_topseam_v1.md"
REPORT_PATH = (
    ROOT
    / "experimental"
    / "notes"
    / "certificate_scanner"
    / "outputs"
    / "rowsharp_q_singleton_topseam_v1.report.md"
)


P = 2**31 - 2**24 + 1
N = 2**21
K = 2**20
AGREEMENT = 1_116_048
J = N - AGREEMENT
T = AGREEMENT - K
W = T - 1
Q_LINE = P**6
B_STAR = (Q_LINE - 1) // 2**128
K_REM = 4_805_007
TARGET_FLOOR = 274_836_936_291_722_953
RETAINED_EXACT_LIFT_BOUND = math.comb(16, 7)
TP = T * P
PAID_PLUS_RETAINED = TP + RETAINED_EXACT_LIFT_BOUND
INTEGER_SLACK = TARGET_FLOOR - PAID_PLUS_RETAINED
INTEGER_SLACK_BITS = math.log2(INTEGER_SLACK)
MULTIPLICATIVE_GAP_BITS = math.log2(TARGET_FLOOR / PAID_PLUS_RETAINED)
STATUS = (
    "CONDITIONAL_ON_WEIGHTED_PRIMITIVE_SP_PADE_BOUND_AND_PLANTED_CORE_COST_BOUND_"
    "AND_STRICT_DISTANCE_AND_ROW_BUDGET_SCOPE"
)


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def poly_trim(poly: list[int]) -> list[int]:
    out = poly[:]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_add(a: list[int], b: list[int], p: int) -> list[int]:
    width = max(len(a), len(b))
    out = [0] * width
    for idx in range(width):
        out[idx] = ((a[idx] if idx < len(a) else 0) + (b[idx] if idx < len(b) else 0)) % p
    return poly_trim(out)


def poly_sub(a: list[int], b: list[int], p: int) -> list[int]:
    width = max(len(a), len(b))
    out = [0] * width
    for idx in range(width):
        out[idx] = ((a[idx] if idx < len(a) else 0) - (b[idx] if idx < len(b) else 0)) % p
    return poly_trim(out)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % p
    return poly_trim(out)


def poly_scale(a: list[int], c: int, p: int) -> list[int]:
    return poly_trim([(c * x) % p for x in a])


def poly_degree(a: list[int]) -> int:
    a = poly_trim(a)
    if len(a) == 1 and a[0] == 0:
        return -1
    return len(a) - 1


def poly_monic(a: list[int], p: int) -> list[int]:
    a = poly_trim(a)
    if poly_degree(a) < 0:
        return [0]
    inv = pow(a[-1], -1, p)
    return poly_scale(a, inv, p)


def poly_divmod(a: list[int], b: list[int], p: int) -> tuple[list[int], list[int]]:
    a = poly_trim(a)
    b = poly_trim(b)
    ensure(poly_degree(b) >= 0, "division by zero polynomial")
    if poly_degree(a) < poly_degree(b):
        return [0], a
    rem = a[:]
    quotient = [0] * (poly_degree(a) - poly_degree(b) + 1)
    inv_lc = pow(b[-1], -1, p)
    while poly_degree(rem) >= poly_degree(b):
        shift = poly_degree(rem) - poly_degree(b)
        coeff = (rem[-1] * inv_lc) % p
        quotient[shift] = coeff
        subtractor = [0] * shift + poly_scale(b, coeff, p)
        rem = poly_sub(rem, subtractor, p)
    return poly_trim(quotient), poly_trim(rem)


def poly_div_exact(a: list[int], b: list[int], p: int) -> list[int]:
    quotient, rem = poly_divmod(a, b, p)
    ensure(poly_degree(rem) < 0, "polynomial division was not exact")
    return quotient


def poly_gcd(a: list[int], b: list[int], p: int) -> list[int]:
    a = poly_trim(a)
    b = poly_trim(b)
    while poly_degree(b) >= 0:
        _, rem = poly_divmod(a, b, p)
        a, b = b, rem
    return poly_monic(a, p)


def monic_from_lower(lower: list[int], p: int) -> list[int]:
    """Ascending coefficients for X^r + lower[r-1]X^(r-1)+...+lower[0]."""
    return [x % p for x in lower] + [1]


def polynomial_cross_identity_checks() -> list[dict[str, Any]]:
    checks = []
    p = 101
    examples = [
        (1, [7], [13], 5),
        (2, [3, 9], [8, 4], 11),
        (4, [2, 5, 7, 19], [23, 29, 31, 37], 17),
        (7, [1, 4, 9, 16, 25, 36, 49], [2, 3, 5, 7, 11, 13, 17], 41),
    ]
    for r, lower1, lower2, c in examples:
        u1 = monic_from_lower(lower1, p)
        u2 = monic_from_lower(lower2, p)
        v1 = poly_sub(u1, [c], p)
        v2 = poly_sub(u2, [c], p)
        l_plus = poly_mul(u1, v2, p)
        l_minus = poly_mul(v1, u2, p)
        lhs = poly_sub(l_plus, l_minus, p)
        rhs = poly_scale(poly_sub(u2, u1, p), c, p)
        expected_degree_bound = r - 1
        checks.append(
            {
                "r": r,
                "prime": p,
                "c": c,
                "identity_pass": lhs == rhs,
                "degree_lhs": poly_degree(lhs),
                "degree_rhs": poly_degree(rhs),
                "expected_degree_bound": expected_degree_bound,
                "degree_bound_pass": poly_degree(lhs) <= expected_degree_bound,
            }
        )
    return checks


def cross_pair_branch_shape_checks() -> list[dict[str, Any]]:
    checks = []
    p = 101
    examples = [
        (1, [7], [13], 5),
        (2, [3, 9], [8, 4], 11),
        (4, [2, 5, 7, 19], [23, 29, 31, 37], 17),
        (7, [1, 4, 9, 16, 25, 36, 49], [2, 3, 5, 7, 11, 13, 17], 41),
    ]
    for r, lower1, lower2, c in examples:
        u1 = monic_from_lower(lower1, p)
        u2 = monic_from_lower(lower2, p)
        v1 = poly_sub(u1, [c], p)
        v2 = poly_sub(u2, [c], p)
        l_plus = poly_mul(u1, v2, p)
        l_minus = poly_mul(v1, u2, p)
        h_poly = poly_gcd(l_plus, l_minus, p)
        m_plus = poly_div_exact(l_plus, h_poly, p)
        m_minus = poly_div_exact(l_minus, h_poly, p)
        diff = poly_sub(m_plus, m_minus, p)
        h = poly_degree(h_poly)
        e = poly_degree(m_plus)
        recovered_u2 = poly_div_exact(poly_mul(h_poly, m_minus, p), v1, p)
        checks.append(
            {
                "r": r,
                "prime": p,
                "c": c,
                "u1_distinct_u2": u1 != u2,
                "h_degree": h,
                "h_degree_bound": r - 1,
                "h_degree_bound_pass": h <= r - 1,
                "E": e,
                "equal_reduced_degrees": e == poly_degree(m_minus),
                "E_lower_bound": r + 1,
                "E_lower_bound_pass": e >= r + 1,
                "degree_mplus_minus_mminus": poly_degree(diff),
                "shift_pair_degree_bound": e - r - 1,
                "shift_pair_degree_bound_pass": poly_degree(diff) <= e - r - 1,
                "coprime_reduced_pair": poly_degree(poly_gcd(m_plus, m_minus, p)) == 0,
                "support_recovery_from_certificate_pass": recovered_u2 == u2,
                "squarefree_required": False,
            }
        )
    return checks


def cross_pair_rule_two_block() -> dict[str, Any]:
    return {
        "status": "RULE_2_MULTIPLICITY_AWARE_SP_PADE_REALIZED_WITH_EXACT_SUPPORT_COST",
        "payment_status": "FINITE_WEIGHTED_PRIMITIVE_SP_BOUND_STILL_REQUIRED",
        "input": "same-cell canonical top-seam packets Pi0, Pi with U != U0",
        "construction": {
            "L_plus": "U0*(U-c)",
            "L_minus": "(U0-c)*U",
            "identity": "L_plus-L_minus=c*(U-U0)",
            "degree_before_cancellation": "deg(L_plus-L_minus) <= r-1",
        },
        "cancellation": {
            "H": "gcd(L_plus,L_minus)",
            "M_plus": "L_plus/H",
            "M_minus": "L_minus/H",
            "E": "deg(M_plus)=deg(M_minus)=2r-deg(H)",
            "proved_bound": "deg(M_plus-M_minus) <= E-r-1",
            "consequence": "depth-r shift-pair / prefix-collision degree inequality",
        },
        "multiplicity_aware_sp_match": {
            "condition": "M_plus and M_minus are monic split polynomials after cancellation; squarefreeness is not required",
            "matched_object": "multiplicity-aware depth-r weighted sp_shift_pair normal form",
            "locator_condition": "deg(M_plus-M_minus) <= E-r-1",
            "weighted_power_sum_condition": (
                "sum_a m_plus(a)*a^k = sum_a m_minus(a)*a^k for 0<=k<=r"
            ),
        },
        "pade_hankel_match": {
            "moment_certificate": "mu_k=sum_a (m_plus(a)-m_minus(a))*a^k=0 for 0<=k<=r",
            "object": "weighted sparse_pade_hankel / finite Hankel-Pade certificate shape",
            "non_squarefree_interpretation": (
                "non-squarefree reduced sides give weighted Padé/Hankel packets, not branch-shape failures"
            ),
        },
        "support_exact_cost": {
            "certificate_key": "(r,c,U0,G,H,M_plus,M_minus)",
            "recovery": "U = H*M_minus/(U0-c); V=U-c; marked core G recovers the deleted packet",
            "cost": "1 support unit per marked multiplicity-aware SP/Padé certificate",
            "not_an_image_cell": True,
        },
        "weighted_sp_pade_dichotomy": {
            "status": "WEIGHTED_SP_PADE_DICHOTOMY_PROVED_FULL_RANK_PRIMITIVE_COUNT_REQUIRED",
            "input_object": "marked weighted certificate C=(r,c,U0,G,H,M_plus,M_minus)",
            "signed_weight": "mu(a)=ord_{X=a}M_plus - ord_{X=a}M_minus on D=supp(mu)",
            "rule2_weight_bound": "Because L_plus and L_minus are products of two squarefree degree-r locators, residual multiplicities in M_plus and M_minus are at most 2; hence mu(a) in {-2,-1,0,1,2}.",
            "pade_normal_form": "F_mu(Y)=Y^(r+1)*R_D(Y)/Q_D(Y), Q_D(Y)=prod_{a in D}(1-aY)",
            "defect_complexity": "s=|D|-r-1 and deg R_D <= s-1",
            "first_match_classes": [
                {
                    "name": "support_collapse_or_common_divisor",
                    "predicate": "|D| <= r+1",
                    "consequence": "impossible for nonzero reduced mu; route to cancellation/common-divisor if produced upstream",
                },
                {
                    "name": "extension_slope",
                    "predicate": "R_D(0)=0, equivalently mu_{r+1}=0",
                    "consequence": "certificate extends from depth r to depth r+1",
                },
                {
                    "name": "rim_rank_drop_pivot",
                    "predicate": "canonical RIM/Hankel pivot vanishes",
                    "consequence": "route to rank_drop_pivot branch",
                },
                {
                    "name": "bc_corank_one_chart",
                    "predicate": "|D|=r+2 and the pivot is nonzero",
                    "consequence": "one-dimensional barycentric nullvector / BC chart",
                },
                {
                    "name": "structural_quotient_complete_common_planted",
                    "predicate": "quotient-pullback, complete-fiber, common-divisor, or planted-core structure is present",
                    "consequence": "route to the corresponding named structural branch",
                },
                {
                    "name": "full_rank_primitive_weighted_stratum",
                    "predicate": "|D|>=r+3, R_D(0)!=0, pivot nonzero, and no structural first-match predicate applies",
                    "consequence": "finite support-level chart count N_WSP_full(z) remains to be printed",
                },
            ],
            "full_rank_chart": {
                "pivot_set": "P subset D with |P|=r+1 and nonzero canonical pivot",
                "free_set": "F=D\\P with |F|=s",
                "linear_solution": "mu_P=-V_P^{-1}V_F*mu_F",
                "injective_chart_key": "(r,c,U0,G,H,D,P,mu_F)",
                "remaining_count": "N_WSP_full(z)",
            },
        },
        "fixed_key_split_shift_reduction": {
            "status": "FULL_RANK_WSP_REDUCED_TO_SPLIT_SHIFT_FLATNESS_PRINTED_FINITE_COUNT_REQUIRED",
            "fixed_key": "(r,c,U0,H), with V0=U0-c",
            "gcd_decomposition": [
                "H_A=gcd(H,U0)",
                "H_B=gcd(H,U0-c)",
                "H=H_A*H_B for exact same-key Rule-2 gcd data",
                "U0=H_A*U0_prime",
                "U0-c=H_B*V0_prime",
            ],
            "normal_form": [
                "U=U0+H*K",
                "U-c=U0-c+H*K",
                "deg K <= r-deg(H)-1",
            ],
            "sp_pade_automatic": (
                "With M_plus=U0_prime*(V0_prime+H_A*K) and "
                "M_minus=V0_prime*(U0_prime+H_B*K), one has "
                "M_plus-M_minus=c*K.  Thus the weighted SP/Pade degree "
                "condition is exactly the degree bound on K."
            ),
            "fixed_key_set": "X_{r,c,U0,H,beta}(z)",
            "fixed_key_conditions": [
                "deg K <= r-deg(H)-1",
                "U0+H*K is monic squarefree split degree r over Omega",
                "U0-c+H*K is monic squarefree split degree r over Omega",
                "the cross-pair gcd is exactly H",
                "G satisfies parent-prefix compatibility for beta",
                "all primitive first-match filters fail",
            ],
            "support_core_constraints": [
                "G subset Omega \\ (Roots(U) union Roots(U-c))",
                "|G|=j-r",
                "P_k(G)=beta_k-P_k(Roots(U)) for 1<=k<=r-1",
            ],
            "abstract_counterexample_family": {
                "parameters": "r=1, H=1, U0=X-a0, U=X-a",
                "certificate": "L_plus=(X-a0)(X-a-c), L_minus=(X-a0-c)(X-a), L_plus-L_minus=c*(a0-a)",
                "lesson": (
                    "SP/Pade shape alone allows many same-key full-rank "
                    "split-shift members; a KB proof needs a finite "
                    "split-locator flatness ledger or a new deletion branch."
                ),
            },
            "bound_reduction": (
                "N_WSP_full(z) = sum_{r,c,U0,H,beta} "
                "|X_{r,c,U0,H,beta}(z)| after canonical first-match "
                "partitioning"
            ),
            "remaining_bound": (
                "prove sum_{r,c,U0,H,beta} |X_{r,c,U0,H,beta}(z)| "
                "<= B_WSP_full with printed constants"
            ),
        },
        "first_match_realization": [
            "construct L_plus and L_minus",
            "cancel H=gcd(L_plus,L_minus)",
            "form weighted Padé normal form F_mu=Y^(r+1)R_D/Q_D",
            "if |D|<=r+1, route to cancellation/common-divisor",
            "if R_D(0)=0, route to extension_slope",
            "else if quotient-pullback, route to quotient_planted",
            "else if complete-fiber, route to complete_fiber/quotient",
            "else if planted-core data remains, route to planted_switch_core_fiber",
            "else if canonical RIM pivot minor vanishes, route to rank_drop_pivot",
            "else if |D|=r+2, route to BC corank-one chart",
            "else reduce to fixed-key split-shift set X_{r,c,U0,H,beta}(z) for printed counting",
        ],
        "algebra_checks": cross_pair_branch_shape_checks(),
    }


def planted_switch_algebra_checks() -> list[dict[str, Any]]:
    checks = []
    examples = [(1, 5), (2, 11), (17, 19), (T, 1), (T, P - 1)]
    for r, c in examples:
        row_delta = (-r * c) % P
        checks.append(
            {
                "r": r,
                "c": c,
                "r_less_than_p": r < P,
                "c_nonzero": c % P != 0,
                "side_switch_preserves_rows_before_r": True,
                "row_r_delta_formula": "-r*c",
                "row_r_delta_mod_p": row_delta,
                "row_r_crosses": row_delta != 0,
            }
        )
    return checks


def planted_switch_rule_one_block() -> dict[str, Any]:
    return {
        "status": "RULE_1_PROVED_AS_EXACT_PLANTED_SWITCH_DESCENT",
        "cost_status": "RULE_1_COST_REQUIRES_PLANTED_CORE_LEDGER",
        "not_zero_cost_row_cell_deletion": True,
        "side_data": {
            "A": "Roots(U)",
            "B": "Roots(U-c)",
            "disjointness": "A cap B is empty because U(x)=U(x)-c=0 would force c=0.",
            "free_core_domain": "Omega_AB = Omega \\ (A union B)",
        },
        "planted_switch": {
            "map_A_to_B": "tau_{A,B}(G union A)=G union B",
            "map_B_to_A": "tau_{B,A}(G union B)=G union A",
            "involution": True,
            "prefix_behavior": [
                "P_k(A)=P_k(B) for 1 <= k <= r-1",
                "P_r(A)-P_r(B)=-r*c != 0 because r<p and c != 0",
            ],
        },
        "core_fiber": {
            "parent_prefix": "beta=(beta_1,...,beta_{r-1})",
            "definition": (
                "G_{beta,A}={G subset Omega_AB: |G|=j-r and "
                "P_k(G)=beta_k-P_k(A) for 1<=k<=r-1}"
            ),
            "bijection": "Pi=(r,c,G,U,U-c;G union A,G union B) <-> G in G_{beta,A}",
            "first_exposed_specialization": {
                "r": "w+1=t",
                "beta": "original primitive target z",
                "core_size": J - T,
                "punctured_domain": "Omega \\ (A union B)",
            },
        },
        "dedup": {
            "correct_key": "(r,c,U,beta)",
            "why_beta_is_required": (
                "For all-depth nodes, the same side key can occur over different parent "
                "prefixes beta; those are different planted core fibers."
            ),
            "first_exposed_short_key_safe": "(r,c,U) only when beta=z is fixed globally.",
            "retain": "least core G_min(r,c,U,beta)",
            "delete": "every other core G under the same planted-switch key",
        },
        "cost_model": {
            "route_d_row_cell_cost": 0,
            "planted_switch_deleted_packet_cost": 1,
            "aggregate_cost": "|G_{beta,A}|-1",
            "requires_printed_ledger": True,
        },
        "algebra_checks": planted_switch_algebra_checks(),
    }


def theorem_scope_block() -> dict[str, Any]:
    return {
        "charged_row_set": {
            "definition": (
                "R_D = {rho(B): B contributes an unpaid top-seam Route-D branch-excess unit}, "
                "where rho(B)=m(B)+1."
            ),
            "row_budget_hypothesis": "|R_D| <= t",
            "deployed_first_exposed_seam": {
                "m": "w=t-1",
                "rho": "w+1=t",
                "R_D": "{t}",
                "local_bound": "sum_B(outdeg_unpaid(B)-1) <= p-1",
                "warning": (
                    "This local specialization only pays first-exposed nodes; all-depth use "
                    "requires the row-budget hypothesis."
                ),
            },
        },
        "budgeted_all_depth_theorem": {
            "status": "CONDITIONAL_COMPILER",
            "top_seam_scope": "e(B)=rho(B) for every singleton-heavy top-seam bucket B",
            "row_budget_scope": "|R_D| <= t",
            "branch_realization_scope": (
                "strict_distance_child is a genuine named paid first-match branch; "
                "repeated_side_pair_reuse is accounted for by the planted-switch "
                "core-fiber ledger; cross_pair_multiplicity_aware_sp_pade realizes "
                "same-cell distinct-U packets as marked weighted SP/Padé certificates "
                "with exact support cost, but still requires a printed finite weighted "
                "primitive SP/Padé bound."
            ),
            "conclusion": "sum_B(outdeg_unpaid(B)-1) <= |R_D|*(p-1) <= t*(p-1)",
        },
    }


def canonical_packet_schema() -> dict[str, Any]:
    return {
        "branch_excess_unit": {
            "symbol": "u=(B,C)",
            "definition": (
                "B is an unpaid primitive singleton-heavy top-seam bucket; C is an unpaid child "
                "of B under the row r=rho(B) split, excluding the canonical base child C0(B)."
            ),
            "base_child_rule": "C0(B) is the globally least unpaid child under a fixed total order.",
            "identity": "outdeg_unpaid(B)-1 = #{C unpaid child of B: C != C0(B)}",
        },
        "canonical_top_seam_boundary_packet": {
            "symbol": "Pi(B,C)=(r,c,G,U,V;S,S')",
            "source_orientation": "S is in the charged child C; S' is in B\\C.",
            "requirements": [
                "r=rho(B)=m(B)+1",
                "|S\\S'|=|S'\\S|=r",
                "G=S cap S'",
                "U(X)=prod_{a in S\\S'}(X-a)",
                "V(X)=prod_{a' in S'\\S}(X-a')",
                "U-V=c in F_p^*",
            ],
            "canonical_pair_rule": (
                "Choose the globally lexicographically least distance-r boundary pair (S,S') "
                "with S in C and S' in B\\C."
            ),
            "payment_cell": "(r,c)",
            "sidekey": "(r,c,U)",
            "markkey": "(r,c,G,U,V)",
            "note": "V=U-c is redundant but retained for verifier clarity.",
        },
    }


def formal_branch_predicates() -> dict[str, Any]:
    return {
        "strict_distance_child": {
            "input": "branch-excess unit (B,C), r=rho(B)",
            "predicate": "d(S,S')=|S\\S'| >= r+1 for every S in C and S' in B\\C",
            "meaning": "C has no top-seam boundary pair and is strict-distance separated from B\\C.",
            "first_match_priority": "P1",
            "paid_status": (
                "Paid only if the strict-distance Route-D/RIM/window-shadow payment theorem is imported; "
                "otherwise remains conditional residual."
            ),
            "route_d_cell_cost": 0,
            "dedup_key": "(B,C)",
        },
        "repeated_side_pair_reuse": {
            "input": "two canonical packets Pi_min, Pi with the same planted-switch key (r,c,U,beta)",
            "predicate": "r_min=r, c_min=c, U_min=U, beta_min=beta, and G_min != G",
            "meaning": (
                "The same local top-seam switch U <-> U-c is reused over the same parent "
                "prefix beta with two distinct marked cores."
            ),
            "first_match_priority": "P2",
            "paid_status": (
                "Rule 1 is proved as exact planted-switch core-fiber descent.  It is paid "
                "exactly to the extent that the planted-core fiber ledger includes the "
                "printed cost |G_{beta,A}|-1."
            ),
            "route_d_cell_cost": 0,
            "planted_switch_cost": "1 per deleted repeated packet, aggregated as |G_{beta,A}|-1",
            "dedup_key": "(r,c,U,beta)",
            "dedup_rule": (
                "Retain the globally least core for each planted-switch key (r,c,U,beta); "
                "noncanonical cores enter planted_switch_core_fiber."
            ),
            "first_exposed_short_key": "(r,c,U) is safe only at the first exposed seam because beta=z is fixed.",
        },
        "cross_pair_multiplicity_aware_sp_pade": {
            "input": "two canonical packets Pi0, Pi with the same cell (r,c) and U != U0",
            "predicate": (
                "L_+=U0*(U-c), L_-=(U0-c)*U; after H=gcd(L_+,L_-), "
                "M_+=L_+/H and M_-=L_-/H are split, coprime, nonidentical, and "
                "deg(M_+-M_-) <= E-r-1 where E=deg(M_+)=deg(M_-)."
            ),
            "verified_identity": "U0*(U-c) - (U0-c)*U = c*(U-U0)",
            "meaning": (
                "A same-cell collision with different side polynomials produces a nontrivial "
                "weighted low-degree split-pair relation through row r. After cancellation this "
                "realizes a multiplicity-aware SP/shift-pair and Padé/Hankel certificate."
            ),
            "first_match_priority": "P3",
            "paid_status": (
                "Rule 2 is realized as a marked multiplicity-aware SP/Padé certificate "
                "with exact support cost. The finite numerical payment remains conditional "
                "on a printed weighted primitive SP/Padé bound."
            ),
            "route_d_cell_cost": 0,
            "support_cost": "1 support unit per marked certificate (r,c,U0,G,H,M_+,M_-)",
            "recovery": "U = H*M_-/(U0-c), V=U-c, and marked core G recovers the deleted packet.",
            "dedup_key": "(r,c)",
            "dedup_rule": (
                "Retain the globally least packet per cell after P1/P2; compare every other same-cell "
                "packet against that representative."
            ),
        },
        "residual_route_d_cell_charge": {
            "input": "canonical packet surviving P1-P3",
            "predicate": "packet survives all earlier predicates and is charged to cell (r,c)",
            "first_match_priority": "P4",
            "route_d_cell_cost": 1,
            "validity_condition": "r in R_D and |R_D| <= t",
        },
    }


def first_match_order() -> list[dict[str, Any]]:
    return [
        {
            "priority": 0,
            "name": "earlier_global_first_match_branches",
            "examples": [
                "generated_field",
                "quotient_planted",
                "sparse_pade_hankel",
                "m1_window_shadow",
                "rank_drop_pivot",
                "bc_chart",
                "sp_shift_pair",
                "extension_slope",
            ],
        },
        {"priority": 1, "name": "strict_distance_child(B,C)"},
        {"priority": 2, "name": "construct canonical packet Pi(B,C)"},
        {"priority": 3, "name": "repeated_side_pair_reuse / planted_switch_core_fiber(Pi_min_key, Pi)"},
        {"priority": 4, "name": "cross_pair_multiplicity_aware_sp_pade(Pi_min_cell, Pi)"},
        {"priority": 5, "name": "residual_route_d_cell_charge(Pi)"},
    ]


def build_certificate() -> dict[str, Any]:
    cross_checks = polynomial_cross_identity_checks()
    planted_checks = planted_switch_algebra_checks()
    rule2_checks = cross_pair_branch_shape_checks()
    ensure(all(row["identity_pass"] for row in cross_checks), "cross identity check failed")
    ensure(all(row["degree_bound_pass"] for row in cross_checks), "cross degree bound failed")
    ensure(all(row["row_r_crosses"] for row in planted_checks), "planted switch row-r crossing failed")
    ensure(all(row["shift_pair_degree_bound_pass"] for row in rule2_checks), "Rule 2 degree check failed")
    ensure(W + 1 == T, "w/t convention mismatch")
    ensure(T < P, "charged row must be nonzero in F_p")
    ensure(RETAINED_EXACT_LIFT_BOUND == 11_440, "retained exact-lift bound changed")
    ensure(PAID_PLUS_RETAINED < TARGET_FLOOR, "deployed closure margin failed")

    return {
        "status": STATUS,
        "claim_class": "LOCAL_ROUTE_D_PAYMENT_COMPILER",
        "not_a_safe_side_certificate": True,
        "does_not_prove": [
            "U(1116048) <= B*",
            "KoalaBear MCA first-safe agreement",
            "row-sharp Q-prefix atom theorem without branch-payment realization",
            "zero-cost repeated side-pair deletion",
            "planted core-fiber cost bound |G_{beta,A}|-1",
            "finite numerical bound for weighted primitive SP/Pade certificates emitted by Rule 2",
            "strict-distance child payment unless it is already a named paid branch",
            "all-depth Route-D row-cell payment without the row-budget hypothesis |R_D|<=t",
            "a promoted Paper-D theorem",
        ],
        "open_pr_interactions": [
            {
                "pr": "#414",
                "topic": "signed-e_m inverse / participation-ratio bound",
                "position": (
                    "keeps raw versus masked residual accounting separate; does not "
                    "convert masked participation-ratio material into Row-sharp Q proof"
                ),
            },
            {
                "pr": "#416/#417",
                "topic": "masked participation ratio and lift-class cost model",
                "position": "does not rely on the lift-class cost model refuted by #417",
            },
            {
                "pr": "#418",
                "topic": "Lean correspondence audit",
                "position": (
                    "does not introduce Lean theorem-label dependencies or claim lake "
                    "build/correspondence closure"
                ),
            },
            {
                "pr": "#419",
                "topic": "BC near-pencil split-in-subspace residual",
                "position": (
                    "treats the fixed-key split-shift residual as a shared unresolved "
                    "object, not as a solved BC/SP payment"
                ),
            },
            {
                "pr": "#420/#421/#422",
                "topic": "entropy-inverse missing-cell and F_p-span cell",
                "position": (
                    "does not claim entropy-inverse removal-list completeness; "
                    "#422-style F_p-span normalization remains adjacent open context"
                ),
            },
            {
                "pr": "#423",
                "topic": "KB-MCA Route-D residual support certificate",
                "position": (
                    "records a local singleton-heavy top-seam compiler and does not "
                    "supersede a full Route-D residual support certificate"
                ),
            },
            {
                "pr": "#424",
                "topic": "row-sharp Q moment floor audit",
                "position": (
                    "does not use a moment-floor route as a closure; the weighted "
                    "primitive SP/Pade and row-budget obligations remain explicit"
                ),
            },
        ],
        "parameters": {
            "p": P,
            "n": N,
            "k": K,
            "agreement": AGREEMENT,
            "j": J,
            "t": T,
            "w": W,
            "B_star": B_STAR,
            "K_rem": K_REM,
        },
        "theorem_scope": theorem_scope_block(),
        "canonical_data": canonical_packet_schema(),
        "formal_branch_predicates": formal_branch_predicates(),
        "step_3_repeated_side_pair_planted_switch": planted_switch_rule_one_block(),
        "step_4_cross_pair_branch_matching": cross_pair_rule_two_block(),
        "first_match_order": first_match_order(),
        "proved_local_lemmas": {
            "lemma_A_singleton_witness_coverage": {
                "status": "PROVED_LOCAL",
                "statement": (
                    "At a top-seam bucket of depth m with r=m+1, every singleton child "
                    "either has a distance-r boundary witness and hence a canonical "
                    "top-seam packet, or has strict distance at least r+1 to the rest "
                    "of the bucket."
                ),
                "uses": [
                    "Q1 distance at common depth m",
                    "side-locator degree bound",
                    "top-seam constant-difference U-V=c",
                    "Newton identity P_r(A)-P_r(B)=-r*c",
                ],
            },
            "lemma_B_no_surviving_same_cell_collision": {
                "status": "ALGEBRA_PROVED_RULE1_DESCENT_RULE2_MULTIPLICITY_AWARE_EXACT_COST_CONDITIONAL_ON_NUMERIC_BOUNDS",
                "statement": (
                    "Two surviving canonical top-seam packets with the same cell (r,c) "
                    "must be identical, after same-side-pair repeats are routed to the "
                    "planted-switch core-fiber branch and distinct side-pair cross "
                    "identities are realized as marked multiplicity-aware SP/Pade-Hankel "
                    "certificates with exact support cost."
                ),
                "verified_cross_identity": "U0*(U-c) - (U0-c)*U = c*(U-U0)",
                "cross_identity_checks": cross_checks,
            },
            "lemma_C_live_child_excess_compiler": {
                "status": "COMPILER_PROVED_MODULO_ROW_BUDGET_AND_BRANCH_ROUTING",
                "statement": (
                    "After choosing one canonical base child at each unpaid top-seam "
                    "bucket, every other surviving child has a canonical top-seam "
                    "boundary packet; same-cell collisions are ruled out by Lemma B."
                ),
                "requires": [
                    "charged row set has size at most t",
                    "strict-distance child is a named paid branch",
                    "Lemma B branch routings are paid and first-matched",
                ],
            },
        },
        "missing_branch_realization": [
            {
                "name": "planted_switch_core_fiber_cost",
                "status": "RULE_1_PROVED_AS_PLANTED_DESCENT_OPEN_REQUIRED_PLANTED_CORE_LEDGER",
                "needed_statement": (
                    "Repeated side-pair reuse with key (r,c,U,beta) is exactly the "
                    "planted core fiber G_{beta,A}.  The noncanonical repeats are "
                    "removed from Route-D row-cell mass, but their printed support "
                    "cost |G_{beta,A}|-1 must be included in a planted/core ledger."
                ),
                "risk": "The descent is proved, but it is not zero-cost and cannot be hidden inside image-cell accounting.",
            },
            {
                "name": "weighted_primitive_sp_pade_bound",
                "status": "RULE_2_MULTIPLICITY_AWARE_REALIZED_OPEN_REQUIRED_WEIGHTED_PRIMITIVE_SP_BOUND",
                "needed_statement": (
                    "If U != U0 in a common cell (r,c), cancellation produces a marked "
                    "multiplicity-aware SP/Pade certificate (r,c,U0,G,H,M_+,M_-) with "
                    "deg(M_+-M_-) <= E-r-1 and exact support cost one.  The weighted "
                    "SP/Pade dichotomy first-matches cancellation/common-divisor, "
                    "extension-slope, RIM rank-drop, BC corank-one, and structural "
                    "quotient/planted classes.  The full-rank primitive residual reduces "
                    "to fixed-key split-shift sets X_{r,c,U0,H,beta}(z).  The finite "
                    "ledger still needs a printed bound for their total count, "
                    "equivalently for N_WSP_full(z)."
                ),
                "risk": "Exact support-cost realization is not the same as a small printed finite adjacent bound.",
            },
            {
                "name": "strict_distance_child",
                "status": "OPEN_REQUIRED_BRANCH_PAYMENT_CHECK",
                "needed_statement": (
                    "A child separated from the rest of a top-seam bucket by distance at least r+1 "
                    "is already paid or routed by strict-distance Route-D/RIM/window-shadow rules."
                ),
                "risk": "If not already a named branch, this is a new payment obligation.",
            },
            {
                "name": "charged_row_budget",
                "status": "OPEN_REQUIRED_SCOPE_CHECK",
                "needed_statement": (
                    "All charged top-seam rows r used by the compiler lie in a row set of size at most t, "
                    "or the theorem is explicitly restricted to the first exposed seam."
                ),
                "risk": "Without this, the cell count t*(p-1) does not follow.",
            },
        ],
        "conditional_counting_compiler": {
            "charged_cells": "|R_D|*(p-1) <= t*(p-1)",
            "charged_cell_count_under_row_budget": T * (P - 1),
            "tree_identity": "unpaid leaves = 1 + sum_B(outdeg_unpaid(B)-1)",
            "if_branch_realization_and_row_budget_hold": "sum_B(outdeg_unpaid(B)-1) <= |R_D|*(p-1) <= t*(p-1)",
            "then_unpaid_supports_bound": "1 + t*(p-1) <= t*p",
            "t_times_p": TP,
        },
        "deployed_arithmetic_closure_if_compiler_is_paid": {
            "retained_exact_lift_bound": RETAINED_EXACT_LIFT_BOUND,
            "paid_plus_retained": PAID_PLUS_RETAINED,
            "target_floor": TARGET_FLOOR,
            "integer_slack": INTEGER_SLACK,
            "integer_slack_bits": INTEGER_SLACK_BITS,
            "multiplicative_gap_bits": MULTIPLICATIVE_GAP_BITS,
            "status": "PASS_CONDITIONAL",
        },
    }


def json_bytes(cert: dict[str, Any]) -> bytes:
    return (json.dumps(cert, indent=2, sort_keys=True) + "\n").encode("utf-8")


def render_note(cert: dict[str, Any]) -> str:
    p = cert["parameters"]
    closure = cert["deployed_arithmetic_closure_if_compiler_is_paid"]
    scope = cert["theorem_scope"]
    step3 = cert["step_3_repeated_side_pair_planted_switch"]
    step4 = cert["step_4_cross_pair_branch_matching"]
    lines = [
        "# Row-sharp Q Singleton-Heavy Top-Seam Route-D Packet v1",
        "",
        f"Status: `{cert['status']}`.",
        "",
        "This packet records the local Route-D singleton-heavy top-seam compiler",
        "extracted from the proof attempts. It does **not** prove `U(1116048) <= B*`,",
        "does **not** certify the KoalaBear MCA first-safe agreement, and does **not**",
        "prove the row-sharp Q-prefix atom theorem until the named branch payments,",
        "finite weighted primitive SP/Padé bound, and row-budget scope below are",
        "formalized with printed costs.",
        "",
        "## Nonclaims",
        "",
        *[f"- {item}" for item in cert["does_not_prove"]],
        "",
        "## Deployed Row",
        "",
        "```text",
        f"p = {p['p']}",
        f"n = {p['n']}",
        f"k = {p['k']}",
        f"agreement = {p['agreement']}",
        f"j = {p['j']}",
        f"t = {p['t']}",
        f"w = {p['w']}",
        f"K_rem = {p['K_rem']}",
        "```",
        "",
        "## Interaction with Open Q/Entropy/BC PRs",
        "",
        *[
            f"- `{item['pr']}` ({item['topic']}): {item['position']}."
            for item in cert["open_pr_interactions"]
        ],
        "",
        "## Step 1: Exact Scope",
        "",
        "The Route-D charged row set is:",
        "",
        "```text",
        scope["charged_row_set"]["definition"],
        scope["charged_row_set"]["row_budget_hypothesis"],
        "```",
        "",
        "The budgeted all-depth compiler theorem is conditional on:",
        "",
        f"- top-seam scope: `{scope['budgeted_all_depth_theorem']['top_seam_scope']}`",
        f"- row-budget scope: `{scope['budgeted_all_depth_theorem']['row_budget_scope']}`",
        f"- branch realization: `{scope['budgeted_all_depth_theorem']['branch_realization_scope']}`",
        "",
        "It concludes:",
        "",
        "```text",
        scope["budgeted_all_depth_theorem"]["conclusion"],
        "```",
        "",
        "The first-exposed local specialization has `rho=w+1=t` and avoids the",
        "row-budget issue, but it pays only first-exposed top-seam nodes.",
        "",
        "## Step 2: Formal Branch Predicates",
        "",
        "Common data are a branch-excess unit `(B,C)` and a canonical top-seam",
        "boundary packet `Pi(B,C)=(r,c,G,U,V;S,S')`, with source side inside",
        "the charged child and target side outside it.",
        "",
    ]
    for name, pred in cert["formal_branch_predicates"].items():
        lines.extend(
            [
                f"### {name}",
                "",
                f"Input: `{pred['input']}`",
                "",
                f"Predicate: `{pred['predicate']}`",
                "",
                f"First-match priority: `{pred['first_match_priority']}`.",
                "",
                f"Paid/residual status: {pred.get('paid_status', pred.get('validity_condition', 'n/a'))}",
                "",
                f"Route-D cell cost: `{pred['route_d_cell_cost']}`.",
                "",
                f"Dedup key: `{pred.get('dedup_key', 'n/a')}`.",
                "",
            ]
        )
        if "planted_switch_cost" in pred:
            lines.extend(
                [
                    f"Planted-switch cost: `{pred['planted_switch_cost']}`.",
                    "",
                ]
            )
    lines.extend(
        [
            "First-match order for this layer:",
            "",
        ]
    )
    for item in cert["first_match_order"]:
        lines.append(f"{item['priority']}. `{item['name']}`")
    lines.extend(
        [
            "",
        "## Step 3: Rule 1 Planted-Switch Descent",
        "",
        f"Status: `{step3['status']}`.",
        "",
        f"Cost status: `{step3['cost_status']}`.",
        "",
        "Rule 1 is not a zero-cost row-cell deletion. If two packets reuse the",
        "same side switch, then the repeated mass is exactly free variation of",
        "the marked core inside a planted core prefix fiber.",
        "",
        "For side data:",
        "",
        "```text",
        "A = Roots(U)",
        "B = Roots(U-c)",
        "Omega_AB = Omega \\ (A union B)",
        "```",
        "",
        "The planted switch preserves rows before the seam and crosses row `r`:",
        "",
        "```text",
        "P_k(A)=P_k(B) for 1 <= k <= r-1",
        "P_r(A)-P_r(B)=-r*c != 0",
        "```",
        "",
        "For parent prefix `beta`, repeated packets with fixed key are in",
        "bijection with:",
        "",
        "```text",
        step3["core_fiber"]["definition"],
        "```",
        "",
        "The corrected all-depth dedup key is:",
        "",
        "```text",
        step3["dedup"]["correct_key"],
        "```",
        "",
        "For the first exposed seam only, `(r,c,U)` is safe because `beta=z`",
        "is fixed globally. For all-depth nodes, omitting `beta` silently",
        "merges different core fibers.",
        "",
        "Cost model:",
        "",
        "```text",
        f"Route-D row-cell cost = {step3['cost_model']['route_d_row_cell_cost']}",
        f"deleted repeated packet cost = {step3['cost_model']['planted_switch_deleted_packet_cost']}",
        f"aggregate planted-switch cost = {step3['cost_model']['aggregate_cost']}",
        "```",
        "",
        "Thus Rule 1 is proved as planted descent, while the PR remains",
        "conditional until the planted/core ledger prints and accepts that",
        "support cost.",
        "",
        "## Step 4: Rule 2 Multiplicity-Aware SP/Padé Realization",
        "",
        f"Status: `{step4['status']}`.",
        "",
        f"Payment status: `{step4['payment_status']}`.",
        "",
        "For two same-cell packets with `U != U0`, construct:",
        "",
        "```text",
        "L_+ = U0*(U-c)",
        "L_- = (U0-c)*U",
        "L_+ - L_- = c*(U-U0)",
        "```",
        "",
        "After cancellation by `H=gcd(L_+,L_-)`, write `L_+=H*M_+` and",
        "`L_-=H*M_-`.  The reduced pair satisfies:",
        "",
        "```text",
        step4["cancellation"]["proved_bound"],
        "```",
        "",
        "Thus `(M_+,M_-)` is a multiplicity-aware depth-`r` weighted",
        "SP/shift-pair normal form.  Squarefreeness is not required.  The same",
        "degree inequality gives the finite Padé/Hankel moment certificate",
        "`sum_a m_+(a)a^k = sum_a m_-(a)a^k` for `0<=k<=r`.",
        "",
        "```text",
        f"certificate key = {step4['support_exact_cost']['certificate_key']}",
        step4["support_exact_cost"]["recovery"],
        f"cost = {step4['support_exact_cost']['cost']}",
        "```",
        "",
        "So Rule 2 is now an unconditional multiplicity-aware branch realization",
        "with exact support cost.  It is not yet a finite numerical payment",
        "bound: the weighted primitive SP/Padé certificates still need a printed",
        "ledger bound after the earlier first-match deletions.",
        "",
        "### Step 4b: Weighted SP/Padé Dichotomy",
        "",
        f"Status: `{step4['weighted_sp_pade_dichotomy']['status']}`.",
        "",
        "For the signed weight `mu(a)=ord_a(M_+) - ord_a(M_-)` on",
        "`D=supp(mu)`, the Padé normal form is:",
        "",
        "```text",
        step4["weighted_sp_pade_dichotomy"]["pade_normal_form"],
        step4["weighted_sp_pade_dichotomy"]["defect_complexity"],
        "```",
        "",
        "The first-match alternatives are:",
        "",
    ]
    )
    for klass in step4["weighted_sp_pade_dichotomy"]["first_match_classes"]:
        lines.append(
            f"- `{klass['name']}`: `{klass['predicate']}`; {klass['consequence']}."
        )
    lines.extend(
        [
        "",
        "The final full-rank primitive weighted stratum is finite and support-level.",
        "A canonical full-rank chart uses:",
        "",
        "```text",
        step4["weighted_sp_pade_dichotomy"]["full_rank_chart"]["injective_chart_key"],
        step4["weighted_sp_pade_dichotomy"]["full_rank_chart"]["linear_solution"],
        "remaining count = " + step4["weighted_sp_pade_dichotomy"]["full_rank_chart"]["remaining_count"],
        "```",
        "",
        "This dichotomy isolates the remaining numeric theorem. It does not bound",
        "`N_WSP_full(z)` by itself.",
        "",
        "### Step 4c: Fixed-Key Split-Shift Normal Form",
        "",
        f"Status: `{step4['fixed_key_split_shift_reduction']['status']}`.",
        "",
        "Rule-2 origin still gives a small-weight constraint:",
        "",
        "```text",
        step4["weighted_sp_pade_dichotomy"]["rule2_weight_bound"],
        "```",
        "",
        "The sharper fixed-key normal form is:",
        "",
        "```text",
        step4["fixed_key_split_shift_reduction"]["fixed_key"],
        *step4["fixed_key_split_shift_reduction"]["gcd_decomposition"],
        *step4["fixed_key_split_shift_reduction"]["normal_form"],
        "```",
        "",
        "In this form the SP/Padé equation adds no further hidden rigidity:",
        "",
        "```text",
        step4["fixed_key_split_shift_reduction"]["sp_pade_automatic"],
        "```",
        "",
        "The remaining fixed-key set is:",
        "",
        "```text",
        step4["fixed_key_split_shift_reduction"]["fixed_key_set"],
        *step4["fixed_key_split_shift_reduction"]["fixed_key_conditions"],
        "```",
        "",
        "Support-core constraints:",
        "",
        "```text",
        *step4["fixed_key_split_shift_reduction"]["support_core_constraints"],
        "```",
        "",
        "The reduction also records why a shape-only proof cannot close the count:",
        "",
        "```text",
        "parameters: " + step4["fixed_key_split_shift_reduction"]["abstract_counterexample_family"]["parameters"],
        "certificate: " + step4["fixed_key_split_shift_reduction"]["abstract_counterexample_family"]["certificate"],
        "lesson: " + step4["fixed_key_split_shift_reduction"]["abstract_counterexample_family"]["lesson"],
        "```",
        "",
        "The remaining finite split-shift ledger is:",
        "",
        "```text",
        step4["fixed_key_split_shift_reduction"]["bound_reduction"],
        step4["fixed_key_split_shift_reduction"]["remaining_bound"],
        "```",
        "",
        "This proves the support-level fixed-key split-shift reduction. It does not",
        "provide the small printed bound for the total fixed-key `K`-pencil count.",
        "",
        "## Proved Local Content",
        "",
        "Lemma A is a local proof that every singleton child of a top-seam bucket",
        "either has a canonical distance-`r` top-seam witness or is strict-distance",
        "separated from the rest of the bucket.",
        "",
        "Lemma B verifies the algebraic same-cell collision guard.  The load-bearing",
        "identity is:",
        "",
        "```text",
        "U0*(U-c) - (U0-c)*U = c*(U-U0)",
        "```",
        "",
        "Since `U0` and `U` are monic degree `r`, `deg(U-U0) <= r-1`. Step 4",
        "upgrades this from a raw degree identity to a marked multiplicity-aware",
        "SP/Padé-Hankel certificate after cancellation. The certificate carries",
        "exact support cost one, but the finite adjacent row still needs the",
        "weighted primitive SP/Padé ledger bound.",
        "",
        "The same-side-polynomial case is now handled by Step 3 as a planted",
        "switch core-fiber descent, with support cost charged to the planted/core",
        "ledger rather than to a Route-D row cell.",
        "",
        "Lemma C is the counting compiler: choose one canonical base child in each",
        "unpaid top-seam bucket, assign every other surviving child a canonical",
        "top-seam packet, and inject surviving packets into cells `(r,c)`.",
        "",
        "## Required Branch Realization",
        "",
        ]
    )
    for item in cert["missing_branch_realization"]:
        lines.extend(
            [
                f"### {item['name']}",
                "",
                f"Status: `{item['status']}`.",
                "",
                item["needed_statement"],
                "",
                f"Risk: {item['risk']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Conditional Counting Closure",
            "",
            "If the branch-realization checks hold and `|R_D| <= t`, then:",
            "",
            "```text",
            "sum_B(outdeg_unpaid(B)-1) <= |R_D|*(p-1) <= t*(p-1)",
            "unpaid supports <= 1 + t*(p-1) <= t*p",
            "```",
            "",
            "For the deployed row:",
            "",
            "```text",
            f"t*p = {cert['conditional_counting_compiler']['t_times_p']}",
            f"retained exact-lift bound = {closure['retained_exact_lift_bound']}",
            f"t*p + retained = {closure['paid_plus_retained']}",
            f"target floor = {closure['target_floor']}",
            f"integer slack = {closure['integer_slack']}",
            f"integer slack bits = {closure['integer_slack_bits']:.9f}",
            f"multiplicative gap bits = {closure['multiplicative_gap_bits']:.9f}",
            "```",
            "",
            "## PR Use",
            "",
            "This is a useful PR packet because it turns the latest proof attempts into",
            "a narrow formalization target.  It should be reviewed as a conditional",
            "Route-D compiler and branch-predicate checklist, not as a complete safe-side",
            "upper ledger.",
            "",
        ]
    )
    return "\n".join(lines)


def render_readme(cert: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# rowsharp-q-singleton-topseam-v1",
            "",
            f"Status: `{cert['status']}`.",
            "",
            "This certificate records the singleton-heavy top-seam Route-D compiler",
            "and deployed arithmetic closure conditional on the weighted primitive",
            "SP/Pade bound, planted core-fiber support cost, strict-distance payment,",
            "and the charged-row budget scope.",
            "",
            "Replay:",
            "",
            "```bash",
            "python3 experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py --check",
            "python3 experimental/scripts/verify_rowsharp_q_singleton_topseam_v1.py --tamper-selftest",
            "```",
            "",
            "Nonclaim: this packet does not prove `U(1116048) <= B*` and does not",
            "prove the row-sharp Q-prefix atom theorem without the listed branch",
            "payment realizations.",
            "",
        ]
    )


def render_report(cert: dict[str, Any]) -> str:
    closure = cert["deployed_arithmetic_closure_if_compiler_is_paid"]
    return "\n".join(
        [
            "# rowsharp_q_singleton_topseam_v1 report",
            "",
            f"status: `{cert['status']}`",
            "",
            "Local algebra checks:",
            f"- cross-identity checks: `{len(cert['proved_local_lemmas']['lemma_B_no_surviving_same_cell_collision']['cross_identity_checks'])}`",
            f"- cross-pair multiplicity-aware checks: `{len(cert['step_4_cross_pair_branch_matching']['algebra_checks'])}`",
            f"- planted-switch checks: `{len(cert['step_3_repeated_side_pair_planted_switch']['algebra_checks'])}`",
            f"- conditional paid supports: `{cert['conditional_counting_compiler']['t_times_p']}`",
            f"- charged row scope: `{cert['theorem_scope']['charged_row_set']['row_budget_hypothesis']}`",
            f"- retained exact-lift: `{closure['retained_exact_lift_bound']}`",
            f"- target floor: `{closure['target_floor']}`",
            f"- integer slack: `{closure['integer_slack']}`",
            "",
            "Open branch realization items:",
            *[f"- `{item['name']}`: `{item['status']}`" for item in cert["missing_branch_realization"]],
            "",
            "Formal branch predicates:",
            *[f"- `{name}`" for name in cert["formal_branch_predicates"]],
            "",
        ]
    )


def write_artifacts(cert: dict[str, Any]) -> None:
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    NOTE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = json_bytes(cert)
    stable = json.loads(payload.decode("utf-8"))
    CERT_PATH.write_bytes(payload)
    CERT_README_PATH.write_text(render_readme(stable), encoding="utf-8", newline="\n")
    NOTE_PATH.write_text(render_note(stable), encoding="utf-8", newline="\n")
    REPORT_PATH.write_text(render_report(stable), encoding="utf-8", newline="\n")
    print(f"wrote {CERT_PATH}")
    print(f"wrote {CERT_README_PATH}")
    print(f"wrote {NOTE_PATH}")
    print(f"wrote {REPORT_PATH}")


def check_certificate(cert: dict[str, Any]) -> None:
    ensure(cert["status"] == STATUS, "bad status")
    ensure(cert["not_a_safe_side_certificate"] is True, "unsafe nonclaim missing")
    ensure(cert["parameters"]["p"] == P, "p changed")
    ensure(cert["parameters"]["t"] == T, "t changed")
    ensure(cert["parameters"]["w"] == W, "w changed")
    ensure(cert["conditional_counting_compiler"]["t_times_p"] == TP, "t*p changed")
    closure = cert["deployed_arithmetic_closure_if_compiler_is_paid"]
    ensure(closure["integer_slack"] == INTEGER_SLACK, "integer slack changed")
    ensure(abs(closure["integer_slack_bits"] - INTEGER_SLACK_BITS) < 1e-12, "integer slack bits changed")
    ensure(
        abs(closure["multiplicative_gap_bits"] - MULTIPLICATIVE_GAP_BITS) < 1e-12,
        "multiplicative gap bits changed",
    )
    ensure(
        cert["conditional_counting_compiler"]["charged_cell_count_under_row_budget"] == T * (P - 1),
        "charged row-cell count changed",
    )
    ensure(cert["theorem_scope"]["charged_row_set"]["row_budget_hypothesis"] == "|R_D| <= t", "row budget missing")
    ensure(
        cert["theorem_scope"]["budgeted_all_depth_theorem"]["conclusion"]
        == "sum_B(outdeg_unpaid(B)-1) <= |R_D|*(p-1) <= t*(p-1)",
        "budgeted theorem conclusion changed",
    )
    ensure(
        set(cert["formal_branch_predicates"])
        == {
            "strict_distance_child",
            "repeated_side_pair_reuse",
            "cross_pair_multiplicity_aware_sp_pade",
            "residual_route_d_cell_charge",
        },
        "formal branch predicates changed",
    )
    step3 = cert["step_3_repeated_side_pair_planted_switch"]
    ensure(step3["status"] == "RULE_1_PROVED_AS_EXACT_PLANTED_SWITCH_DESCENT", "Rule 1 status changed")
    ensure(step3["cost_status"] == "RULE_1_COST_REQUIRES_PLANTED_CORE_LEDGER", "Rule 1 cost status changed")
    ensure(step3["dedup"]["correct_key"] == "(r,c,U,beta)", "Rule 1 dedup key changed")
    ensure(step3["cost_model"]["aggregate_cost"] == "|G_{beta,A}|-1", "Rule 1 cost model changed")
    ensure(all(row["row_r_crosses"] for row in step3["algebra_checks"]), "planted switch checks failed")
    step4 = cert["step_4_cross_pair_branch_matching"]
    ensure(
        step4["status"] == "RULE_2_MULTIPLICITY_AWARE_SP_PADE_REALIZED_WITH_EXACT_SUPPORT_COST",
        "Rule 2 status changed",
    )
    ensure(
        step4["payment_status"] == "FINITE_WEIGHTED_PRIMITIVE_SP_BOUND_STILL_REQUIRED",
        "Rule 2 payment status changed",
    )
    ensure(
        step4["support_exact_cost"]["certificate_key"] == "(r,c,U0,G,H,M_plus,M_minus)",
        "Rule 2 support certificate key changed",
    )
    ensure(
        step4["weighted_sp_pade_dichotomy"]["status"]
        == "WEIGHTED_SP_PADE_DICHOTOMY_PROVED_FULL_RANK_PRIMITIVE_COUNT_REQUIRED",
        "Rule 2 weighted dichotomy status changed",
    )
    ensure(
        step4["weighted_sp_pade_dichotomy"]["full_rank_chart"]["remaining_count"] == "N_WSP_full(z)",
        "Rule 2 full-rank remaining count changed",
    )
    ensure(
        len(step4["weighted_sp_pade_dichotomy"]["first_match_classes"]) == 6,
        "Rule 2 dichotomy class list changed",
    )
    split_shift = step4["fixed_key_split_shift_reduction"]
    ensure(
        split_shift["status"]
        == "FULL_RANK_WSP_REDUCED_TO_SPLIT_SHIFT_FLATNESS_PRINTED_FINITE_COUNT_REQUIRED",
        "Rule 2 fixed-key split-shift status changed",
    )
    ensure(
        "U=U0+H*K" in split_shift["normal_form"],
        "Rule 2 fixed-key normal form changed",
    )
    ensure(
        split_shift["sp_pade_automatic"].startswith("With M_plus=U0_prime"),
        "Rule 2 automatic SP/Pade reduction changed",
    )
    ensure(
        split_shift["bound_reduction"]
        == "N_WSP_full(z) = sum_{r,c,U0,H,beta} |X_{r,c,U0,H,beta}(z)| after canonical first-match partitioning",
        "Rule 2 fixed-key bound reduction changed",
    )
    ensure(
        split_shift["remaining_bound"]
        == "prove sum_{r,c,U0,H,beta} |X_{r,c,U0,H,beta}(z)| <= B_WSP_full with printed constants",
        "Rule 2 fixed-key remaining bound changed",
    )
    ensure(
        all(
            row["h_degree_bound_pass"]
            and row["E_lower_bound_pass"]
            and row["shift_pair_degree_bound_pass"]
            and row["coprime_reduced_pair"]
            and row["support_recovery_from_certificate_pass"]
            and row["squarefree_required"] is False
            for row in step4["algebra_checks"]
        ),
        "Rule 2 multiplicity-aware checks failed",
    )
    ensure(len(cert["first_match_order"]) == 6, "first-match order changed")
    ensure(
        cert["deployed_arithmetic_closure_if_compiler_is_paid"]["paid_plus_retained"] == PAID_PLUS_RETAINED,
        "paid+retained changed",
    )
    ensure(
        cert["deployed_arithmetic_closure_if_compiler_is_paid"]["target_floor"] == TARGET_FLOOR,
        "target floor changed",
    )
    ensure(
        cert["deployed_arithmetic_closure_if_compiler_is_paid"]["integer_slack"]
        == TARGET_FLOOR - PAID_PLUS_RETAINED,
        "integer slack changed",
    )
    missing = {item["name"]: item for item in cert["missing_branch_realization"]}
    ensure(
        set(missing)
        == {
            "planted_switch_core_fiber_cost",
            "weighted_primitive_sp_pade_bound",
            "strict_distance_child",
            "charged_row_budget",
        },
        "branch realization checklist changed",
    )
    ensure(
        missing["planted_switch_core_fiber_cost"]["status"]
        == "RULE_1_PROVED_AS_PLANTED_DESCENT_OPEN_REQUIRED_PLANTED_CORE_LEDGER",
        "Rule 1 missing status changed",
    )
    ensure(
        missing["weighted_primitive_sp_pade_bound"]["status"]
        == "RULE_2_MULTIPLICITY_AWARE_REALIZED_OPEN_REQUIRED_WEIGHTED_PRIMITIVE_SP_BOUND",
        "Rule 2 missing status changed",
    )
    cross_checks = cert["proved_local_lemmas"]["lemma_B_no_surviving_same_cell_collision"]["cross_identity_checks"]
    ensure(all(row["identity_pass"] and row["degree_bound_pass"] for row in cross_checks), "cross checks failed")


def check_artifacts() -> None:
    cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    check_certificate(cert)
    ensure(CERT_PATH.read_bytes() == json_bytes(cert), "JSON is not canonical")
    ensure(CERT_README_PATH.read_text(encoding="utf-8") == render_readme(cert), "README mismatch")
    ensure(NOTE_PATH.read_text(encoding="utf-8") == render_note(cert), "note mismatch")
    ensure(REPORT_PATH.read_text(encoding="utf-8") == render_report(cert), "report mismatch")
    print("artifact check passed: 4 files")


def tamper_selftest() -> None:
    base = build_certificate()
    mutations: list[tuple[str, Any]] = [
        ("status", lambda c: c.__setitem__("status", "PROVED")),
        ("t", lambda c: c["parameters"].__setitem__("t", c["parameters"]["t"] + 1)),
        ("w", lambda c: c["parameters"].__setitem__("w", c["parameters"]["w"] + 1)),
        ("t_times_p", lambda c: c["conditional_counting_compiler"].__setitem__("t_times_p", TP - 1)),
        (
            "paid_plus_retained",
            lambda c: c["deployed_arithmetic_closure_if_compiler_is_paid"].__setitem__(
                "paid_plus_retained", PAID_PLUS_RETAINED - 1
            ),
        ),
        (
            "target_floor",
            lambda c: c["deployed_arithmetic_closure_if_compiler_is_paid"].__setitem__(
                "target_floor", TARGET_FLOOR + 1
            ),
        ),
        (
            "multiplicative_gap_bits",
            lambda c: c["deployed_arithmetic_closure_if_compiler_is_paid"].__setitem__(
                "multiplicative_gap_bits", 0
            ),
        ),
        (
            "cross_identity",
            lambda c: c["proved_local_lemmas"]["lemma_B_no_surviving_same_cell_collision"][
                "cross_identity_checks"
            ][0].__setitem__("identity_pass", False),
        ),
        ("branch_count", lambda c: c["missing_branch_realization"].pop()),
        (
            "row_budget_hypothesis",
            lambda c: c["theorem_scope"]["charged_row_set"].__setitem__("row_budget_hypothesis", "|R_D| <= t+1"),
        ),
        ("formal_predicate", lambda c: c["formal_branch_predicates"].pop("strict_distance_child")),
        ("first_match_order", lambda c: c["first_match_order"].pop()),
        (
            "missing_rule1_status",
            lambda c: c["missing_branch_realization"][0].__setitem__("status", "OPEN_REQUIRED_BRANCH_PAYMENT_CHECK"),
        ),
        (
            "rule1_key",
            lambda c: c["step_3_repeated_side_pair_planted_switch"]["dedup"].__setitem__(
                "correct_key", "(r,c,U)"
            ),
        ),
        (
            "rule1_cost",
            lambda c: c["step_3_repeated_side_pair_planted_switch"]["cost_model"].__setitem__(
                "aggregate_cost", "0"
            ),
        ),
        (
            "rule2_status",
            lambda c: c["step_4_cross_pair_branch_matching"].__setitem__("status", "PROVED"),
        ),
        (
            "rule2_shape_bound",
            lambda c: c["step_4_cross_pair_branch_matching"]["algebra_checks"][0].__setitem__(
                "shift_pair_degree_bound_pass", False
            ),
        ),
        (
            "rule2_support_certificate_key",
            lambda c: c["step_4_cross_pair_branch_matching"]["support_exact_cost"].__setitem__(
                "certificate_key", "(r,c)"
            ),
        ),
        (
            "rule2_dichotomy_status",
            lambda c: c["step_4_cross_pair_branch_matching"]["weighted_sp_pade_dichotomy"].__setitem__(
                "status", "PROVED"
            ),
        ),
        (
            "rule2_full_rank_count",
            lambda c: c["step_4_cross_pair_branch_matching"]["weighted_sp_pade_dichotomy"][
                "full_rank_chart"
            ].__setitem__("remaining_count", "0"),
        ),
        (
            "rule2_split_shift_status",
            lambda c: c["step_4_cross_pair_branch_matching"]["fixed_key_split_shift_reduction"].__setitem__(
                "status", "PROVED_WITH_BOUND"
            ),
        ),
        (
            "rule2_split_shift_bound",
            lambda c: c["step_4_cross_pair_branch_matching"]["fixed_key_split_shift_reduction"].__setitem__(
                "remaining_bound", "all fixed-key K-pencils are empty"
            ),
        ),
        (
            "rule2_recovery",
            lambda c: c["step_4_cross_pair_branch_matching"]["algebra_checks"][0].__setitem__(
                "support_recovery_from_certificate_pass", False
            ),
        ),
    ]
    passed = 0
    for name, mutate in mutations:
        trial = copy.deepcopy(base)
        mutate(trial)
        try:
            check_certificate(trial)
        except AssertionError:
            passed += 1
        else:
            raise AssertionError(f"tamper self-test failed to catch {name}")
    print(f"tamper self-test passed: {passed} mutations rejected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    if args.write:
        write_artifacts(build_certificate())
    if args.check:
        check_artifacts()
    if args.tamper_selftest:
        tamper_selftest()
    if not args.write and not args.check and not args.tamper_selftest:
        print(json.dumps(build_certificate(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
