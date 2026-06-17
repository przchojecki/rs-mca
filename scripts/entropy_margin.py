#!/usr/bin/env python3
"""Generated-field entropy margin checker.

This is an AUDIT helper for the Reed--Solomon reserve ledger.  It checks the
finite quantity

    sigma * log2(q_gen) - log2(binomial(n, k + sigma))

using q_gen, not the verifier challenge field.  The certified decision uses
standard binomial entropy bounds; the displayed estimate is for readability.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class EntropyReport:
    object: str
    status: str
    theorem_problem_id: str
    n: int
    k: int
    sigma: int
    a: int
    rho: float
    eta: float
    delta: float
    q_gen: int | None
    log2_q_gen: float
    list_exponent_B: float | None
    gamma_bits: float
    lhs_bits: float
    log2_binom_lower_bound: float
    log2_binom_upper_bound: float
    log2_binom_estimate: float
    entropy_margin_lower_bound_bits: float
    entropy_margin_upper_bound_bits: float
    entropy_margin_estimate_bits: float
    polynomial_margin_lower_bound_bits: float | None
    polynomial_margin_upper_bound_bits: float | None
    polynomial_margin_estimate_bits: float | None
    decision: str
    proof_certificate: str
    notes: list[str]


def positive_int(text: str) -> int:
    try:
        value = int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not an integer: {text}") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("must be positive")
    return value


def nonnegative_int(text: str) -> int:
    try:
        value = int(text, 0)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"not an integer: {text}") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return value


def h2(x: float) -> float:
    if x <= 0.0 or x >= 1.0:
        return 0.0
    return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)


def log2_binom_entropy_bounds(n: int, a: int) -> tuple[float, float]:
    if a < 0 or a > n:
        raise ValueError("a must satisfy 0 <= a <= n")
    if a == 0 or a == n:
        return 0.0, 0.0
    p = a / n
    upper = n * h2(p)
    lower = upper - math.log2(n + 1)
    return lower, upper


def log2_binom_estimate(n: int, a: int, exact_threshold: int) -> float:
    if a < 0 or a > n:
        raise ValueError("a must satisfy 0 <= a <= n")
    if a == 0 or a == n:
        return 0.0
    if n <= exact_threshold:
        return math.log2(math.comb(n, a))
    return (
        math.lgamma(n + 1)
        - math.lgamma(a + 1)
        - math.lgamma(n - a + 1)
    ) / math.log(2.0)


def build_report(args: argparse.Namespace) -> EntropyReport:
    n = args.n
    k = args.k
    sigma = args.sigma
    a = k + sigma
    if not (1 <= k <= n):
        raise ValueError("require 1 <= k <= n")
    if not (0 <= sigma <= n - k):
        raise ValueError("require 0 <= sigma <= n-k")

    if args.q_gen is None and args.q_gen_log2 is None:
        raise ValueError("provide either --q-gen or --q-gen-log2")
    if args.q_gen is not None and args.q_gen_log2 is not None:
        raise ValueError("provide only one of --q-gen or --q-gen-log2")
    if args.q_gen is not None:
        q_gen = args.q_gen
        log2_q_gen = math.log2(q_gen)
    else:
        q_gen = None
        log2_q_gen = args.q_gen_log2
        if log2_q_gen <= 0:
            raise ValueError("--q-gen-log2 must be positive")

    lower, upper = log2_binom_entropy_bounds(n, a)
    estimate = log2_binom_estimate(n, a, args.exact_threshold)
    lhs = sigma * log2_q_gen

    margin_lower = lhs - upper
    margin_upper = lhs - lower
    margin_estimate = lhs - estimate

    poly_lower = poly_upper = poly_estimate = None
    effective_lower = margin_lower
    effective_upper = margin_upper
    if args.list_exponent is not None:
        b_term = args.list_exponent * math.log2(n)
        poly_lower = margin_lower - b_term
        poly_upper = margin_upper - b_term
        poly_estimate = margin_estimate - b_term
        effective_lower = poly_lower
        effective_upper = poly_upper

    gamma = args.gamma_bits
    if effective_lower >= gamma:
        decision = "clears_margin"
    elif effective_upper < gamma:
        decision = "fails_margin"
    else:
        decision = "inconclusive_with_entropy_bounds"

    cert = (
        "Uses binomial entropy bounds: "
        "2^(n H2(a/n))/(n+1) <= binom(n,a) <= 2^(n H2(a/n)); "
        "therefore lhs-upper <= margin <= lhs-lower."
    )
    notes = [
        "AUDIT helper only; does not prove a locator local limit or protocol soundness.",
        "q_gen is the generated field. Do not substitute q_line or q_chal without a theorem.",
    ]
    if args.list_exponent is not None:
        notes.append("Polynomial margin subtracts B * log2(n) from the entropy margin.")
    if n > args.exact_threshold:
        notes.append("Displayed estimate uses lgamma; certified decision uses entropy bounds.")
    else:
        notes.append("Displayed estimate uses an exact integer binomial followed by log2.")

    return EntropyReport(
        object="generated_field_entropy_margin",
        status="AUDIT",
        theorem_problem_id="Paper C eq:entropy-margin / P2 certificate scanner",
        n=n,
        k=k,
        sigma=sigma,
        a=a,
        rho=k / n,
        eta=sigma / n,
        delta=1.0 - a / n,
        q_gen=q_gen,
        log2_q_gen=log2_q_gen,
        list_exponent_B=args.list_exponent,
        gamma_bits=gamma,
        lhs_bits=lhs,
        log2_binom_lower_bound=lower,
        log2_binom_upper_bound=upper,
        log2_binom_estimate=estimate,
        entropy_margin_lower_bound_bits=margin_lower,
        entropy_margin_upper_bound_bits=margin_upper,
        entropy_margin_estimate_bits=margin_estimate,
        polynomial_margin_lower_bound_bits=poly_lower,
        polynomial_margin_upper_bound_bits=poly_upper,
        polynomial_margin_estimate_bits=poly_estimate,
        decision=decision,
        proof_certificate=cert,
        notes=notes,
    )


def print_text(report: EntropyReport) -> None:
    rows: list[tuple[str, Any]] = [
        ("object", report.object),
        ("status", report.status),
        ("theorem/problem", report.theorem_problem_id),
        ("n", report.n),
        ("k", report.k),
        ("sigma", report.sigma),
        ("a = k + sigma", report.a),
        ("rho", f"{report.rho:.12g}"),
        ("eta", f"{report.eta:.12g}"),
        ("delta", f"{report.delta:.12g}"),
        ("q_gen", report.q_gen if report.q_gen is not None else "(given by log2)"),
        ("log2(q_gen)", f"{report.log2_q_gen:.12f}"),
        ("lhs bits", f"{report.lhs_bits:.12f}"),
        ("log2 binom lower", f"{report.log2_binom_lower_bound:.12f}"),
        ("log2 binom upper", f"{report.log2_binom_upper_bound:.12f}"),
        ("log2 binom estimate", f"{report.log2_binom_estimate:.12f}"),
        ("entropy margin lower", f"{report.entropy_margin_lower_bound_bits:.12f}"),
        ("entropy margin upper", f"{report.entropy_margin_upper_bound_bits:.12f}"),
        ("entropy margin estimate", f"{report.entropy_margin_estimate_bits:.12f}"),
    ]
    if report.list_exponent_B is not None:
        rows.extend(
            [
                ("list exponent B", f"{report.list_exponent_B:.12g}"),
                ("polynomial margin lower", f"{report.polynomial_margin_lower_bound_bits:.12f}"),
                ("polynomial margin upper", f"{report.polynomial_margin_upper_bound_bits:.12f}"),
                ("polynomial margin estimate", f"{report.polynomial_margin_estimate_bits:.12f}"),
            ]
        )
    rows.extend(
        [
            ("gamma bits", f"{report.gamma_bits:.12f}"),
            ("decision", report.decision),
            ("certificate", report.proof_certificate),
        ]
    )
    width = max(len(k) for k, _ in rows)
    print("Generated-field entropy margin (AUDIT)")
    for key, value in rows:
        print(f"{key:<{width}} : {value}")
    print("notes:")
    for note in report.notes:
        print(f"  - {note}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check the generated-field entropy reserve margin."
    )
    parser.add_argument("--n", required=True, type=positive_int, help="domain size")
    parser.add_argument("--k", required=True, type=positive_int, help="RS dimension")
    parser.add_argument(
        "--sigma",
        required=True,
        type=nonnegative_int,
        help="reserve in agreement symbols, so a=k+sigma",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--q-gen", type=positive_int, help="generated field size")
    group.add_argument(
        "--q-gen-log2",
        type=float,
        help="log2 generated field size, useful for bit-width audits",
    )
    parser.add_argument(
        "--gamma-bits",
        type=float,
        default=0.0,
        help="additive margin target Gamma_ent in bits",
    )
    parser.add_argument(
        "--list-exponent",
        type=float,
        default=None,
        help="optional polynomial target B; checks margin after subtracting B log2(n)",
    )
    parser.add_argument(
        "--exact-threshold",
        type=positive_int,
        default=5000,
        help="use math.comb for the displayed estimate when n is at most this value",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(sys.argv[1:] if argv is None else argv)
        report = build_report(args)
    except (ValueError, OverflowError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(asdict(report), indent=2, sort_keys=True))
    else:
        print_text(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
