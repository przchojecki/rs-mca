#!/usr/bin/env python3
"""Exact verifier for the M31 post-Johnson conversion contract.

All verdict-bearing gates use integer or Fraction arithmetic.  The full-slice
binomial is recomputed independently by math.comb and by a prime-exponent
factorization.  Source pins are Git blob SHA-1 values.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

SCHEMA = "m31-postjohnson-conversion-contract-v1"
BASE_SHA = "c49e45eed71af9c24e3599c2fca3b76e02692be9"
CERT_REL = Path(
    "experimental/data/certificates/"
    "m31-postjohnson-conversion-contract/"
    "m31_postjohnson_conversion_contract.json"
)

# Upstream steering files are recorded for provenance, not gated.  `agents.md` is
# rewritten by governance commits -- fb6d955 replaced the blob the sibling packets
# froze -- so drift there must report, never fail.
STEERING_SOURCES = frozenset({"agents.md"})
SOURCE_PINS = {
    "RS_MCA_Paving_v9.2.tex": "3381e130c691561974f645d4d832173784db2108",
    "agents.md": "b85f2d23fdca64ac3b36b815c85b9bc366970c35",
    "experimental/Conjectures_and_Barriers_RS_MCA_v4_1_source/experimental/data/certificates/frontier-adjacent/m31_list_v1.packet.json":
        "ae8927f38e27c5de40a176c364135d3604cd2a86",
    "experimental/data/certificates/four-row-exact-completion-compiler-v1/four_row_exact_completion_compiler_v1.json":
        "357cf4865a04f3db78eda39c983a2d1ef79451e1",
    "experimental/notes/l1/l1_aperiodic_prefix_collision.md":
        "be91876079ba2b9a0332dedfa78f0fe36eccd0af",
    "experimental/notes/l1/l1_coset_petal_rank_collapse.md":
        "7c7586d1caf3cf561b2f602612128ce5e5f596ba",
    "experimental/notes/thresholds/m31_fixed_remainder_dyadic_route_cut.md":
        "e08705282f7f5a0f15d52d51b3bb97ce834041ff",
    "open-proximity.tex": "f8ccfcc11bbfcd5f1a00595ef4d81325128ff58a",
    "tex/cs25_cap_v13_2.tex": "5ceff5dbc4b1ac4cef53eae7eada32046e4bafeb",
}

MANDATORY_BLOCK = [
    "row:                 (F_{p^4}, D=chi(twin coset), k=1048576, n=2097152, rho=1/2)",
    "object:              ordinary LIST, not MCA",
    "radius/agreement:    delta=981129/2097152 and integer agreement 1116023",
    "Johnson comparison:  delta_Johnson=614241/2097152 and post-Johnson gap 366888",
    "bound:               CONDITIONAL |Lambda(C,delta)|<=16777215 from q*epsilon_CA(C,delta)<=16777214; BCHKS route-cut upper q-1",
    "route:               CS_CA_TO_LIST / BCHKS_CA_TO_LIST",
    "CA_or_MCA_input:     q*epsilon_CA(C,delta)<=16777214 for CS; epsilon_CA(C,981131/n,1048575/n)<1/4194304 for BCHKS",
    "code_shift:          C=RS(k); C^+=RS(k+1), with C subset C^+",
    "status:              PROVED / CONDITIONAL / AUDIT",
]


class VerificationError(RuntimeError):
    """Raised when an exact certificate gate fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def ceil_div(num: int, den: int) -> int:
    require(den > 0, "ceil_div denominator must be positive")
    return (num + den - 1) // den


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = (
                b"\x00" * (((limit - start) // prime) + 1)
            )
    return [prime for prime in range(2, limit + 1) if sieve[prime]]


def vp_factorial(value: int, prime: int) -> int:
    exponent = 0
    while value:
        value //= prime
        exponent += value
    return exponent


def binom_prime_factorization(n: int, k: int) -> int:
    k = min(k, n - k)
    factors: list[int] = []
    for prime in primes_upto(n):
        exponent = (
            vp_factorial(n, prime)
            - vp_factorial(k, prime)
            - vp_factorial(n - k, prime)
        )
        if exponent:
            factors.append(pow(prime, exponent))
    return math.prod(factors)


def finite_johnson_margin(
    *, agreement: int, pairwise_agreement: int, n: int, q: int, ell: int
) -> int:
    """Squared exact J_{q,ell} agreement inequality, positive means covered."""
    return (
        (ell - 1) * (q * agreement - n) ** 2
        - (
            n**2 * (q - 1) ** 2 * (ell - 1)
            - n * (q - 1) * q * ell * (n - pairwise_agreement)
        )
    )


def shortened_denominator(
    *, removed: int, agreement: int, n: int, k: int
) -> int:
    return (
        (agreement - removed) ** 2
        - (n - removed) * (k - removed - 1)
    )


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def derive_exact() -> dict[str, Any]:
    p = 2**31 - 1
    q_route_1 = p**4
    q_route_2 = (
        2**124 - 4 * 2**93 + 6 * 2**62 - 4 * 2**31 + 1
    )
    require(q_route_1 == q_route_2, "field-size routes disagree")
    q = q_route_1

    n = 2**21
    k = 2**20
    agreement = 1_116_023
    errors = n - agreement
    w = agreement - k
    mca_agreement = agreement + 1
    mca_errors = n - mca_agreement
    security_denominator = 2**100
    budget, floor_remainder = divmod(q, security_denominator)
    budget_ceil = ceil_div(q, security_denominator)
    require(budget == 2**24 - 1, "budget floor mismatch")
    require(budget_ceil == budget + 1, "budget ceiling mismatch")

    # Independent full-slice binomial routes.
    binomial_route_1 = math.comb(n, agreement)
    binomial_route_2 = binom_prime_factorization(n, agreement)
    require(binomial_route_1 == binomial_route_2, "binomial routes disagree")
    binomial = binomial_route_1
    prefix_denominator = p**w
    average_floor, average_remainder = divmod(binomial, prefix_denominator)
    average_ceiling = average_floor + (1 if average_remainder else 0)
    multiplier_floor, multiplier_remainder = divmod(
        budget * prefix_denominator, binomial
    )

    # R0: exact finite-q, finite-list Johnson comparison for C+ = RS(k+1).
    ell = budget
    johnson_prev = 1_482_910
    johnson_agreement = 1_482_911
    finite_prev_margin = finite_johnson_margin(
        agreement=johnson_prev,
        pairwise_agreement=k,
        n=n,
        q=q,
        ell=ell,
    )
    finite_margin = finite_johnson_margin(
        agreement=johnson_agreement,
        pairwise_agreement=k,
        n=n,
        q=q,
        ell=ell,
    )
    require(finite_prev_margin < 0 < finite_margin, "finite Johnson boundary")
    quadratic_prev = johnson_prev**2 - n * k
    quadratic_margin = johnson_agreement**2 - n * k
    require(quadratic_prev < 0 < quadratic_margin, "quadratic boundary")
    johnson_errors = n - johnson_agreement
    johnson_cap_num = n * (johnson_agreement - k)
    johnson_cap, johnson_cap_remainder = divmod(
        johnson_cap_num, quadratic_margin
    )

    # Convention audit: the packet row C itself has pairwise agreement k-1.
    row_johnson_prev = 1_482_909
    row_johnson_agreement = 1_482_910
    row_quad_prev = row_johnson_prev**2 - n * (k - 1)
    row_quad_margin = row_johnson_agreement**2 - n * (k - 1)
    require(row_quad_prev < 0 < row_quad_margin, "row-code Johnson boundary")
    row_cap_num = n * (row_johnson_agreement - (k - 1))
    row_cap, row_cap_remainder = divmod(row_cap_num, row_quad_margin)

    # R1 route 1: both row and partner are below their quadratic regions.
    row_stress_den = agreement**2 - n * (k - 1)
    partner_stress_den = agreement**2 - n * k

    # R1 route 2: shortening, then Johnson.
    shortening_s = 1_043_596
    shortening_prev_den = shortened_denominator(
        removed=shortening_s - 1, agreement=agreement, n=n, k=k
    )
    shortening_den = shortened_denominator(
        removed=shortening_s, agreement=agreement, n=n, k=k
    )
    require(
        shortening_prev_den <= 0 < shortening_den,
        "shortening activation boundary",
    )
    shortened_n = n - shortening_s
    shortened_k = k - shortening_s
    shortened_agreement = agreement - shortening_s
    shortened_cap_num = shortened_n * (
        shortened_agreement - (shortened_k - 1)
    )
    shortened_cap, shortened_cap_remainder = divmod(
        shortened_cap_num, shortening_den
    )
    averaging_removed = 27
    averaging_num_route_1 = math.comb(n, averaging_removed)
    averaging_den_route_1 = math.comb(agreement, averaging_removed)
    averaging_num_route_2 = math.prod(
        n - i for i in range(averaging_removed)
    )
    averaging_den_route_2 = math.prod(
        agreement - i for i in range(averaging_removed)
    )
    require(
        averaging_num_route_1 * averaging_den_route_2
        == averaging_num_route_2 * averaging_den_route_1,
        "shortening averaging routes disagree",
    )
    averaging_floor, averaging_remainder = divmod(
        averaging_num_route_1, averaging_den_route_1
    )

    # R3(i): CS25.  E denotes the integer CA bad-slope numerator q*epsilon.
    q_minus_n = q - n
    budget_times_k = budget * k
    cs_denominator = q_minus_n + budget_times_k
    cs_numerator = budget * q_minus_n
    cs_max_input, cs_remainder = divmod(cs_numerator, cs_denominator)
    cs_explicit_eta_num = 1
    cs_explicit_eta_den = budget
    cs_premise_margin = (
        q_minus_n - budget * (budget - 1) * k
    )
    require(cs_max_input == budget - 1, "CS maximal integer input")
    require(cs_premise_margin > 0, "CS explicit eta premise")
    require(
        Fraction(k * (budget - 1), q_minus_n)
        <= Fraction(cs_explicit_eta_num, cs_explicit_eta_den)
        <= Fraction(1, budget),
        "CS eta interval",
    )
    cs_output = ceil_div(
        (budget - 1) * cs_explicit_eta_den,
        cs_explicit_eta_den - cs_explicit_eta_num,
    )
    require(cs_output == budget, "CS explicit eta output")

    # R3(ii): BCHKS25.
    two_n = 2 * n
    bchks_input_max, bchks_q_remainder = divmod(q, two_n)
    require(bchks_q_remainder == 1, "BCHKS q congruence")
    bchks_lower_margin = q - two_n * bchks_input_max
    bchks_upper_margin = two_n * (bchks_input_max + 1) - q
    bchks_conclusion = q - 1
    bchks_budget_factor, bchks_budget_remainder = divmod(
        bchks_conclusion, budget
    )
    bchks_factor_over_2_100 = bchks_budget_factor - 2**100
    bchks_excess_over_2_100_budget = (
        bchks_conclusion - 2**100 * budget
    )

    # R3(iii): literal repository transcription of GCXK25, source-sign guarded.
    gcxk_base_numerator = budget**2 * errors
    # eta_0 = sqrt(agreement/n) - mca_agreement/n.
    # The following two squared comparisons prove 1/6 < eta_0 < 1/5.
    gcxk_eta_lower_margin = (
        36 * agreement * n - (6 * mca_agreement + n) ** 2
    )
    gcxk_eta_upper_margin = (
        (5 * mca_agreement + n) ** 2 - 25 * agreement * n
    )
    require(
        gcxk_eta_lower_margin > 0 and gcxk_eta_upper_margin > 0,
        "GCXK eta interval",
    )
    gcxk_adjacent_integer_numerator = gcxk_base_numerator + 5
    gcxk_budget_factor, gcxk_budget_remainder = divmod(
        gcxk_adjacent_integer_numerator, budget
    )

    return {
        "row": {
            "p": p,
            "extension_degree": 4,
            "q": q,
            "full_domain_n": n,
            "punctured_working_domain_n": n - 8,
            "k": k,
            "rho_num": 1,
            "rho_den": 2,
            "agreement": agreement,
            "errors": errors,
            "w": w,
            "mca_adjacent_agreement": mca_agreement,
            "mca_adjacent_errors": mca_errors,
            "security_denominator": security_denominator,
            "B_star": budget,
            "budget_floor_remainder": floor_remainder,
            "budget_ceiling": budget_ceil,
            "binomial_bit_length": binomial.bit_length(),
            "prefix_denominator_bit_length": prefix_denominator.bit_length(),
            "average_floor": average_floor,
            "average_remainder_nonzero": average_remainder != 0,
            "average_ceiling": average_ceiling,
            "full_budget_multiplier_floor": multiplier_floor,
            "full_budget_multiplier_remainder_nonzero":
                multiplier_remainder != 0,
        },
        "johnson": {
            "comparison_code": "C^+=RS_F(D,k+1)",
            "ell": ell,
            "pairwise_agreement": k,
            "a_johnson": johnson_agreement,
            "a_johnson_minus_one": johnson_prev,
            "delta_johnson_num": johnson_errors,
            "delta_johnson_den": n,
            "post_johnson_agreement_gap": johnson_agreement - agreement,
            "post_johnson_relative_gap_num": 45_861,
            "post_johnson_relative_gap_den": 262_144,
            "capacity_headroom_num": 67_447,
            "capacity_headroom_den": n,
            "finite_q_margin_at_previous": finite_prev_margin,
            "finite_q_margin_at_boundary": finite_margin,
            "quadratic_margin_at_previous": quadratic_prev,
            "quadratic_margin_at_boundary": quadratic_margin,
            "quadratic_cap_numerator": johnson_cap_num,
            "quadratic_cap": johnson_cap,
            "quadratic_cap_remainder": johnson_cap_remainder,
            "row_code_a_johnson": row_johnson_agreement,
            "row_code_delta_johnson_num": n - row_johnson_agreement,
            "row_code_quadratic_margin_at_previous": row_quad_prev,
            "row_code_quadratic_margin_at_boundary": row_quad_margin,
            "row_code_quadratic_cap": row_cap,
            "row_code_quadratic_cap_remainder": row_cap_remainder,
        },
        "direct_attacks": {
            "classical_johnson": {
                "row_code_denominator": row_stress_den,
                "partner_code_denominator": partner_stress_den,
                "status": "VACUOUS_AT_STRESS_ROW",
            },
            "shortening_then_johnson": {
                "minimal_removed_for_positive_denominator": shortening_s,
                "denominator_one_before": shortening_prev_den,
                "denominator_at_activation": shortening_den,
                "shortened_n": shortened_n,
                "shortened_k": shortened_k,
                "shortened_agreement": shortened_agreement,
                "shortened_johnson_cap_numerator": shortened_cap_num,
                "shortened_johnson_cap": shortened_cap,
                "shortened_johnson_cap_remainder": shortened_cap_remainder,
                "averaging_loss_test_removed": averaging_removed,
                "averaging_loss_floor": averaging_floor,
                "averaging_loss_remainder": averaging_remainder,
                "averaging_loss_minus_budget": averaging_floor - budget,
                "status": "EXACT_ROUTE_CUT",
            },
        },
        "witness_attacks": {
            "identity_prefix_lower": {
                "certified_codeword_lower": average_ceiling,
                "gap_below_budget": budget - average_ceiling,
                "status": "BELOW_BUDGET",
            },
            "round_robin_coset_169": {
                "proved_t3_distinct_codewords_upper": 1,
                "gap_below_budget": budget - 1,
                "status": "T3_RECONSTRUCTION_COLLAPSE",
            },
            "fixed_remainder_dyadic": {
                "largest_raw_support_fiber_cap": 35,
                "gap_below_budget": budget - 35,
                "projection_warning": "support cap only; no list-safety claim",
                "status": "NO_BUDGET_CROSSING_WITNESS",
            },
        },
        "cs25": {
            "input_code": "C=RS_F(D,k)",
            "output_code": "C^+=RS_F(D,k+1)",
            "radius_num": errors,
            "radius_den": n,
            "integer_input_name": "E=q*epsilon_CA(C,delta)",
            "feasible_eta_lower": "kE/(q-n)",
            "feasible_eta_upper": "(B_star-E)/B_star",
            "balanced_window_numerator": cs_numerator,
            "balanced_window_denominator": cs_denominator,
            "max_integer_input": cs_max_input,
            "floor_remainder": cs_remainder,
            "balanced_eta_numerator": budget_times_k,
            "balanced_eta_denominator": cs_denominator,
            "explicit_eta_numerator_for_max_input": cs_explicit_eta_num,
            "explicit_eta_denominator_for_max_input": cs_explicit_eta_den,
            "explicit_eta_premise_margin": cs_premise_margin,
            "explicit_eta_output_ceiling": cs_output,
            "candidate_mca_row_input_budget": budget,
            "candidate_mca_row_agreement": mca_agreement,
            "agreement_shift_needed": -1,
            "numerator_shift_needed": -1,
            "corrected_bridge": (
                "q*epsilon_CA(C,981129/2097152)<=16777214 "
                "implies List(C^+,981129/2097152)<=16777215 "
                "and hence List(C,981129/2097152)<=16777215"
            ),
            "status": "PROVED_EXACT_CONDITIONAL_BRIDGE",
        },
        "bchks25": {
            "code": "C=RS_F(D,k)",
            "delta_fld_num": errors + 2,
            "delta_fld_den": n,
            "delta_intr_num": n - k - 1,
            "delta_intr_den": n,
            "two_radius_gap_num": (n - k - 1) - (errors + 2),
            "two_radius_gap_den": n,
            "epsilon_threshold_denominator": two_n,
            "max_integer_CA_numerator_under_strict_threshold":
                bchks_input_max,
            "strict_lower_margin": bchks_lower_margin,
            "strict_upper_margin": bchks_upper_margin,
            "integer_list_conclusion": bchks_conclusion,
            "conclusion_minus_budget": bchks_conclusion - budget,
            "budget_factor_floor": bchks_budget_factor,
            "budget_factor_remainder": bchks_budget_remainder,
            "factor_floor_minus_2^100": bchks_factor_over_2_100,
            "conclusion_minus_2^100_times_budget":
                bchks_excess_over_2_100_budget,
            "status": "PROVED_EXACT_ROUTE_CUT",
        },
        "gcxk25": {
            "code": "C=RS_F(D,k)",
            "list_radius_num": errors,
            "list_radius_den": n,
            "list_bound": budget,
            "literal_repository_radius":
                "1-sqrt(1116023/2097152)+eta",
            "literal_repository_numerator":
                "B_star^2*981129+1/eta",
            "base_numerator": gcxk_base_numerator,
            "eta_for_adjacent_mca_radius":
                "sqrt(1116023/2097152)-1116024/2097152",
            "eta_lower_bound_num": 1,
            "eta_lower_bound_den": 6,
            "eta_upper_bound_num": 1,
            "eta_upper_bound_den": 5,
            "eta_lower_squared_margin": gcxk_eta_lower_margin,
            "eta_upper_squared_margin": gcxk_eta_upper_margin,
            "adjacent_radius_integer_numerator":
                gcxk_adjacent_integer_numerator,
            "adjacent_radius_budget_factor_floor": gcxk_budget_factor,
            "adjacent_radius_budget_factor_remainder": gcxk_budget_remainder,
            "rational_eta_tradeoff":
                "eta=1/t gives integer numerator at most B_star^2*981129+t",
            "source_sign_guard": (
                "The repository transcription prints a plus-eta radius; "
                "the cited GCXK25 abstract uses a different smaller-radius "
                "expression. No equivalence is claimed."
            ),
            "status": "AUDIT_SOURCE_SIGN_GUARDED",
        },
    }


def compare_section(
    actual: dict[str, Any], expected: dict[str, Any], path: str
) -> None:
    require(isinstance(actual, dict), f"{path} must be an object")
    require(set(actual) == set(expected), f"{path} keys differ")
    for key, expected_value in expected.items():
        actual_value = actual[key]
        child = f"{path}.{key}"
        if isinstance(expected_value, dict):
            compare_section(actual_value, expected_value, child)
        else:
            require(actual_value == expected_value, f"{child} mismatch")


def validate_certificate(
    data: dict[str, Any], *, repo_root: Path, check_sources: bool = True
) -> None:
    require(data.get("schema") == SCHEMA, "schema mismatch")
    require(data.get("base_sha") == BASE_SHA, "base SHA mismatch")
    require(
        data.get("workboard_item") == "M1",
        "workboard item must remain M1",
    )
    require(data.get("object") == "LIST", "object must remain LIST")
    require(
        data.get("architecture") == "DIRECT",
        "architecture must remain DIRECT",
    )
    require(
        data.get("mandatory_packet_block") == MANDATORY_BLOCK,
        "mandatory packet block mismatch",
    )
    require(
        data.get("source_pins") == SOURCE_PINS,
        "source pin table mismatch",
    )

    expected = derive_exact()
    for section, expected_value in expected.items():
        compare_section(data[section], expected_value, section)

    required_nonclaims = {
        "NO_DIRECT_LIST_UPPER_THEOREM",
        "NO_BUDGET_CROSSING_LIST_WITNESS",
        "NO_MCA_BAD_SLOPE_NUMERATOR_RELABELED_AS_LIST_BOUND",
        "NO_ADJACENT_MCA_ROW_TO_LIST_ROW_IMPLICATION",
        "NO_GCXK_EXTERNAL_THEOREM_CLAIM_UNTIL_SOURCE_SIGN_IS_RECONCILED",
        "NO_KOALABEAR_CLOSURE",
    }
    require(
        set(data.get("nonclaims", [])) == required_nonclaims,
        "nonclaims mismatch",
    )
    require(
        data.get("terminal_verdict")
        == "OPEN GAP: M1 needs a direct list theorem/counterexample or "
           "CA/MCA numerator <=16777214 at agreement 1116023",
        "terminal verdict mismatch",
    )

    if check_sources:
        for relative_path, expected_sha in SOURCE_PINS.items():
            path = repo_root / relative_path
            require(path.is_file(), f"missing source: {relative_path}")
            actual_sha = git_blob_sha(path.read_bytes())
            if relative_path in STEERING_SOURCES:
                if actual_sha != expected_sha:
                    print(
                        f"NOTE steering source drifted: {relative_path} "
                        f"recorded {expected_sha}, observed {actual_sha}"
                    )
                continue
            require(
                actual_sha == expected_sha,
                f"source pin mismatch for {relative_path}: {actual_sha}",
            )


def load_canonical(path: Path) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    canonical = json.dumps(data, indent=2, sort_keys=True) + "\n"
    require(raw == canonical, "certificate JSON is not canonical")
    return data


def run_check(repo_root: Path, cert_path: Path) -> None:
    data = load_canonical(cert_path)
    validate_certificate(data, repo_root=repo_root, check_sources=True)
    print("PASS schema/base/object/mandatory-block")
    print("PASS source Git-blob pins")
    print("PASS row arithmetic and two-route full-slice average")
    print("PASS finite-q Johnson and direct quadratic boundary")
    print("PASS direct Johnson and shortening route cuts")
    print("PASS witness-route non-crossings with unit guards")
    print("PASS CS25 exact eta window and one-count ceiling loss")
    print("PASS BCHKS25 two-radius route cut and exact margins")
    print("PASS GCXK25 literal-source arithmetic with sign guard")
    print("PASS adversarial terminal and explicit nonclaims")


def run_tamper_selftest(repo_root: Path, cert_path: Path) -> None:
    pristine = load_canonical(cert_path)
    validate_certificate(pristine, repo_root=repo_root, check_sources=True)

    mutations = [
        ("B_star", ("row", "B_star"), pristine["row"]["B_star"] + 1),
        (
            "Johnson boundary",
            ("johnson", "a_johnson"),
            pristine["johnson"]["a_johnson"] - 1,
        ),
        (
            "CS maximal input",
            ("cs25", "max_integer_input"),
            pristine["cs25"]["max_integer_input"] + 1,
        ),
    ]
    for label, path, replacement in mutations:
        mutated = copy.deepcopy(pristine)
        cursor: dict[str, Any] = mutated
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        try:
            validate_certificate(
                mutated, repo_root=repo_root, check_sources=False
            )
        except VerificationError:
            print(f"PASS tamper rejected: {label}")
        else:
            raise VerificationError(f"tamper was accepted: {label}")


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--tamper-selftest", action="store_true")
    parser.add_argument(
        "--certificate",
        type=Path,
        default=None,
        help="certificate path (defaults to the repository packet)",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    cert_path = (
        args.certificate.resolve()
        if args.certificate is not None
        else repo_root / CERT_REL
    )
    try:
        if args.check:
            run_check(repo_root, cert_path)
        else:
            run_tamper_selftest(repo_root, cert_path)
    except (OSError, ValueError, VerificationError) as exc:
        print(f"FAIL: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
