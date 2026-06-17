#!/usr/bin/env python3
"""Compute Paper C list/MCA/query soundness budgets.

The script implements the accounting in Paper C's challenge-size target:

    log2(q_line) >= max(lambda_list + log2(L_mu),
                       lambda_mca + log2(N_mca)).

It also computes the toy-protocol query count
t >= lambda_query / log2(1 / (1 - delta)) when requested.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any


NEG_INF = float("-inf")


def positive_int(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def nonnegative_float(text: str) -> float:
    value = float(text)
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative number")
    return value


def parse_probability(text: str) -> float:
    if "/" in text:
        value = float(Fraction(text))
    else:
        value = float(text)
    if not 0.0 < value < 1.0:
        raise argparse.ArgumentTypeError("expected a number in (0, 1)")
    return value


def log2_sum_exp(values: list[float]) -> float:
    finite = [value for value in values if not math.isinf(value)]
    if not finite:
        return NEG_INF
    maximum = max(finite)
    return maximum + math.log2(sum(2.0 ** (value - maximum) for value in finite))


def bits_text(value: float | None) -> str:
    if value is None:
        return "not provided"
    if math.isinf(value):
        return "-inf"
    if abs(value) >= 1000:
        return f"{value:.3f}"
    return f"{value:.6f}".rstrip("0").rstrip(".")


def compute_list_bits(args: argparse.Namespace, log2_n: float) -> dict[str, Any]:
    sources = [
        args.list_bound_bits is not None,
        args.base_list_bits is not None,
        args.base_list_exponent is not None,
    ]
    if sum(sources) != 1:
        raise ValueError(
            "provide exactly one of --list-bound-bits, --base-list-bits, "
            "or --base-list-exponent"
        )

    if args.list_bound_bits is not None:
        return {
            "method": "direct_interleaved_bound",
            "log2_L_mu": args.list_bound_bits,
        }

    if args.base_list_bits is not None:
        return {
            "method": "trivial_product_from_base_bits",
            "log2_L_mu": args.mu * args.base_list_bits,
            "log2_L_1": args.base_list_bits,
        }

    return {
        "method": "trivial_product_from_base_exponent",
        "log2_L_mu": args.mu * args.base_list_exponent * log2_n,
        "B_L": args.base_list_exponent,
    }


def compute_mca_bits(args: argparse.Namespace, log2_n: float) -> dict[str, Any]:
    if args.qprofile_empty and args.qprofile_bits is not None:
        raise ValueError("use either --qprofile-empty or --qprofile-bits, not both")

    base_term_bits = args.mca_exponent * log2_n
    terms = [{"name": "n^A_M", "log2_bits": base_term_bits}]

    quotient_term_bits: float | None = None
    if args.qprofile_bits is not None:
        quotient_term_bits = args.beta_over_hbin * args.qprofile_bits
        quotient_term_bits += args.gamma_m_bits
        terms.append(
            {
                "name": "quotient_profile",
                "log2_bits": quotient_term_bits,
                "beta_over_hbin": args.beta_over_hbin,
                "qprofile_bits": args.qprofile_bits,
                "gamma_m_bits": args.gamma_m_bits,
            }
        )

    numerator_without_nu = log2_sum_exp([term["log2_bits"] for term in terms])
    numerator_bits = math.log2(args.nu) + numerator_without_nu
    return {
        "method": "paper_c_corrected_rs_numerator",
        "nu": args.nu,
        "A_M": args.mca_exponent,
        "qprofile_empty": args.qprofile_empty or args.qprofile_bits is None,
        "terms": terms,
        "log2_N_mca": numerator_bits,
    }


def compute_query(args: argparse.Namespace) -> dict[str, Any] | None:
    if args.lambda_query is None:
        return None
    if args.delta is None:
        raise ValueError("--lambda-query requires --delta")

    per_query_bits = math.log2(1.0 / (1.0 - args.delta))
    count = math.ceil(args.lambda_query / per_query_bits)
    return {
        "delta": args.delta,
        "lambda_query": args.lambda_query,
        "per_query_bits": per_query_bits,
        "minimum_queries": count,
    }


def compute_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.qline is not None and args.qline_bits is not None:
        raise ValueError("use either --qline or --qline-bits, not both")

    log2_n = math.log2(args.n)
    list_data = compute_list_bits(args, log2_n)
    mca_data = compute_mca_bits(args, log2_n)

    required_list_bits = args.lambda_list + list_data["log2_L_mu"]
    required_mca_bits = args.lambda_mca + mca_data["log2_N_mca"]
    required_qline_bits = max(required_list_bits, required_mca_bits)

    actual_qline_bits = None
    if args.qline is not None:
        actual_qline_bits = math.log2(args.qline)
    elif args.qline_bits is not None:
        actual_qline_bits = args.qline_bits

    list_margin = None
    mca_margin = None
    qline_margin = None
    if actual_qline_bits is not None:
        list_margin = actual_qline_bits - required_list_bits
        mca_margin = actual_qline_bits - required_mca_bits
        qline_margin = actual_qline_bits - required_qline_bits

    report: dict[str, Any] = {
        "n": args.n,
        "log2_n": log2_n,
        "mu": args.mu,
        "list_budget": {
            **list_data,
            "lambda_list": args.lambda_list,
            "required_qline_bits": required_list_bits,
            "actual_qline_margin_bits": list_margin,
            "clears_actual_qline": None if list_margin is None else list_margin >= 0,
        },
        "mca_budget": {
            **mca_data,
            "lambda_mca": args.lambda_mca,
            "required_qline_bits": required_mca_bits,
            "actual_qline_margin_bits": mca_margin,
            "clears_actual_qline": None if mca_margin is None else mca_margin >= 0,
        },
        "required_qline_bits": required_qline_bits,
        "actual_qline_bits": actual_qline_bits,
        "actual_qline_margin_bits": qline_margin,
        "clears_actual_qline": None if qline_margin is None else qline_margin >= 0,
    }

    query_data = compute_query(args)
    if query_data is not None:
        report["query_budget"] = query_data

    return report


def print_report(report: dict[str, Any]) -> None:
    print(f"n={report['n']} log2(n)={bits_text(report['log2_n'])}")
    print()
    print("list budget")
    print(f"  method: {report['list_budget']['method']}")
    print(f"  log2 L_mu: {bits_text(report['list_budget']['log2_L_mu'])}")
    print(
        "  required log2(q_line): "
        f"{bits_text(report['list_budget']['required_qline_bits'])}"
    )
    if report["list_budget"]["actual_qline_margin_bits"] is not None:
        print(
            "  actual q_line margin: "
            f"{bits_text(report['list_budget']['actual_qline_margin_bits'])} bits"
        )

    print()
    print("MCA / line-decoding budget")
    print(f"  method: {report['mca_budget']['method']}")
    print(f"  log2 N_mca: {bits_text(report['mca_budget']['log2_N_mca'])}")
    print(
        "  required log2(q_line): "
        f"{bits_text(report['mca_budget']['required_qline_bits'])}"
    )
    if report["mca_budget"]["actual_qline_margin_bits"] is not None:
        print(
            "  actual q_line margin: "
            f"{bits_text(report['mca_budget']['actual_qline_margin_bits'])} bits"
        )

    print()
    print(f"required log2(q_line): {bits_text(report['required_qline_bits'])}")
    if report["actual_qline_bits"] is not None:
        print(f"actual log2(q_line): {bits_text(report['actual_qline_bits'])}")
        print(
            "overall q_line margin: "
            f"{bits_text(report['actual_qline_margin_bits'])} bits"
        )
        print(f"clears actual q_line: {str(report['clears_actual_qline']).lower()}")

    if "query_budget" in report:
        query = report["query_budget"]
        print()
        print("query budget")
        print(f"  delta: {bits_text(query['delta'])}")
        print(f"  per-query bits: {bits_text(query['per_query_bits'])}")
        print(f"  minimum queries: {query['minimum_queries']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compute Paper C interleaved-list, MCA, and query budgets."
    )
    parser.add_argument("--n", type=positive_int, required=True, help="domain size")
    parser.add_argument("--mu", type=positive_int, default=1, help="list arity")
    parser.add_argument(
        "--list-bound-bits",
        type=nonnegative_float,
        help="direct value of log2 L_mu(delta)",
    )
    parser.add_argument(
        "--base-list-bits",
        type=nonnegative_float,
        help="direct value of log2 L_1(delta), promoted by L_mu <= L_1^mu",
    )
    parser.add_argument(
        "--base-list-exponent",
        type=nonnegative_float,
        help="B_L in L_1(delta) <= n^B_L, promoted by L_mu <= n^(mu B_L)",
    )
    parser.add_argument(
        "--lambda-list",
        type=nonnegative_float,
        required=True,
        help="target list soundness bits",
    )
    parser.add_argument(
        "--lambda-mca",
        type=nonnegative_float,
        required=True,
        help="target MCA or line-decoding soundness bits",
    )
    parser.add_argument(
        "--nu",
        type=positive_int,
        default=1,
        help="implementation interleaving multiplier for the MCA numerator",
    )
    parser.add_argument(
        "--mca-exponent",
        type=nonnegative_float,
        default=1.0,
        help="A_M in the n^A_M MCA numerator term",
    )
    parser.add_argument(
        "--qprofile-empty",
        action="store_true",
        help="record that no quotient-profile numerator term is present",
    )
    parser.add_argument(
        "--qprofile-bits",
        type=nonnegative_float,
        help="Qprof_H(a,k) in bits, if a quotient term is present",
    )
    parser.add_argument(
        "--beta-over-hbin",
        type=nonnegative_float,
        default=1.0,
        help="beta(rho)/Hbin(rho) multiplier for the quotient-profile term",
    )
    parser.add_argument(
        "--gamma-m-bits",
        type=float,
        default=0.0,
        help="additive Gamma_M slack in the quotient-profile MCA term",
    )
    parser.add_argument(
        "--qline",
        type=positive_int,
        help="actual line-field size, if known exactly",
    )
    parser.add_argument(
        "--qline-bits",
        type=nonnegative_float,
        help="actual log2(q_line), if only bit width is known",
    )
    parser.add_argument(
        "--delta",
        type=parse_probability,
        help="distance radius for the optional query budget, e.g. 7/16",
    )
    parser.add_argument(
        "--lambda-query",
        type=nonnegative_float,
        help="target query soundness bits for t >= lambda/log2(1/(1-delta))",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = compute_report(args)
    except ValueError as exc:
        parser.error(str(exc))

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
