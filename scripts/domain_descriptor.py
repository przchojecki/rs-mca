#!/usr/bin/env python3
"""Emit a field/domain descriptor for Paper C reserve certificates."""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from typing import Any


def positive_int(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def nonnegative_int(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def factor_integer(value: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    remaining = value

    count = 0
    while remaining % 2 == 0:
        count += 1
        remaining //= 2
    if count:
        factors[2] = count

    divisor = 3
    limit = math.isqrt(remaining)
    while divisor <= limit and remaining > 1:
        count = 0
        while remaining % divisor == 0:
            count += 1
            remaining //= divisor
        if count:
            factors[divisor] = count
            limit = math.isqrt(remaining)
        divisor += 2

    if remaining > 1:
        factors[remaining] = factors.get(remaining, 0) + 1
    return factors


def factor_list(value: int) -> list[dict[str, int]]:
    return [
        {"prime": prime, "exponent": exponent}
        for prime, exponent in sorted(factor_integer(value).items())
    ]


def integer_nth_root(value: int, degree: int) -> int:
    if degree <= 0:
        raise ValueError("degree must be positive")
    if value in {0, 1}:
        return value

    low = 1
    high = 1 << ((value.bit_length() + degree - 1) // degree)
    while low <= high:
        mid = (low + high) // 2
        powered = mid**degree
        if powered == value:
            return mid
        if powered < value:
            low = mid + 1
        else:
            high = mid - 1
    return high


def is_prime_by_trial(value: int) -> bool:
    if value < 2:
        return False
    factors = factor_integer(value)
    return len(factors) == 1 and factors.get(value) == 1


def prime_power(size: int) -> dict[str, Any]:
    data: dict[str, Any] = {
        "size": size,
        "factorization": [],
        "is_prime_power": False,
        "prime": None,
        "degree": None,
        "log2_size": math.log2(size),
    }

    for degree in range(size.bit_length(), 1, -1):
        root = integer_nth_root(size, degree)
        if (
            root > 1
            and root <= 10**12
            and root**degree == size
            and is_prime_by_trial(root)
        ):
            data["factorization"] = [{"prime": root, "exponent": degree}]
            data["is_prime_power"] = True
            data["prime"] = root
            data["degree"] = degree
            return data

    if size <= 10**12 and is_prime_by_trial(size):
        data["factorization"] = [{"prime": size, "exponent": 1}]
        data["is_prime_power"] = True
        data["prime"] = size
        data["degree"] = 1
        return data

    if size <= 10**12:
        data["factorization"] = factor_list(size)
    else:
        data["factorization"] = [{"prime": size, "exponent": 1, "unverified": 1}]
    data["is_prime_power"] = False
    return data


def extension_degree(base: dict[str, Any], top: dict[str, Any]) -> int | None:
    if not base["is_prime_power"] or not top["is_prime_power"]:
        return None
    if base["prime"] != top["prime"]:
        return None
    if top["degree"] % base["degree"] != 0:
        return None
    return top["degree"] // base["degree"]


def check(status: str, name: str, detail: str) -> dict[str, str]:
    return {"status": status, "name": name, "detail": detail}


def format_factorization(value: int) -> str:
    parts = []
    for item in factor_list(value):
        prime = item["prime"]
        exponent = item["exponent"]
        parts.append(str(prime) if exponent == 1 else f"{prime}^{exponent}")
    return " * ".join(parts) if parts else "1"


def reserve_data(n: int, k: int, a: int | None, sigma: int | None) -> dict[str, Any] | None:
    if a is None and sigma is None:
        return None
    if a is not None and sigma is not None:
        raise ValueError("use either --a or --sigma, not both")
    agreement = a if a is not None else k + sigma
    if agreement < k or agreement > n:
        raise ValueError("expected k <= a <= n")
    slack = agreement - k
    return {
        "a": agreement,
        "sigma": slack,
        "eta": str(Fraction(slack, n)),
        "eta_float": slack / n,
        "delta": str(Fraction(n - agreement, n)),
        "delta_float": 1.0 - agreement / n,
    }


def compute_report(args: argparse.Namespace) -> dict[str, Any]:
    if args.k > args.n:
        raise ValueError("expected k <= n")
    if args.expected_extension_degree is not None and args.expected_extension_degree <= 0:
        raise ValueError("--expected-extension-degree must be positive")

    fields = {
        "q_arith": prime_power(args.q_arith),
        "q_gen": prime_power(args.q_gen),
        "q_line": prime_power(args.q_line),
    }
    if args.q_chal is not None:
        fields["q_chal"] = prime_power(args.q_chal)

    ext_gen_over_arith = extension_degree(fields["q_arith"], fields["q_gen"])
    ext_line_over_gen = extension_degree(fields["q_gen"], fields["q_line"])
    ext_chal_over_line = None
    if "q_chal" in fields:
        ext_chal_over_line = extension_degree(fields["q_line"], fields["q_chal"])

    gcd_n_k = math.gcd(args.n, args.k)
    reserve = reserve_data(args.n, args.k, args.a, args.sigma)

    checks = []
    for label, field in fields.items():
        if field["is_prime_power"]:
            checks.append(
                check(
                    "PASS",
                    f"{label}_prime_power",
                    f"{field['size']} = {field['prime']}^{field['degree']}",
                )
            )
        else:
            checks.append(
                check("FAIL", f"{label}_prime_power", "field size is not a prime power")
            )

    if args.domain_type in {"multiplicative_subgroup", "multiplicative_coset"}:
        if (args.q_gen - 1) % args.n == 0:
            checks.append(
                check("PASS", "domain_in_q_gen", "n divides q_gen - 1")
            )
        else:
            checks.append(
                check("FAIL", "domain_in_q_gen", "n does not divide q_gen - 1")
            )
    else:
        checks.append(
            check(
                "SKIP",
                "domain_in_q_gen",
                "multiplicative divisibility check not applicable to domain type",
            )
        )

    if ext_line_over_gen is None:
        checks.append(
            check(
                "WARN",
                "q_line_over_q_gen",
                "q_gen is not verified as a subfield of q_line",
            )
        )
    else:
        checks.append(
            check(
                "PASS",
                "q_line_over_q_gen",
                f"extension degree [q_line:q_gen] = {ext_line_over_gen}",
            )
        )

    if args.expected_extension_degree is not None:
        if ext_line_over_gen == args.expected_extension_degree:
            checks.append(
                check("PASS", "expected_extension_degree", "matches q_line over q_gen")
            )
        else:
            checks.append(
                check(
                    "FAIL",
                    "expected_extension_degree",
                    f"expected {args.expected_extension_degree}, got {ext_line_over_gen}",
                )
            )

    if args.k <= args.n:
        checks.append(check("PASS", "dimension", "k <= n"))
    else:
        checks.append(check("FAIL", "dimension", "k > n"))

    return {
        "name": args.name,
        "description": args.description,
        "fields": fields,
        "extensions": {
            "q_gen_over_q_arith": ext_gen_over_arith,
            "q_line_over_q_gen": ext_line_over_gen,
            "q_chal_over_q_line": ext_chal_over_line,
        },
        "domain": {
            "type": args.domain_type,
            "n": args.n,
            "n_factorization": factor_list(args.n),
            "n_factorization_text": format_factorization(args.n),
            "is_power_of_two": args.n > 0 and args.n & (args.n - 1) == 0,
        },
        "code": {
            "k": args.k,
            "rho": str(Fraction(args.k, args.n)),
            "rho_float": args.k / args.n,
            "gcd_n_k": gcd_n_k,
            "gcd_n_k_factorization": factor_list(gcd_n_k),
            "gcd_n_k_factorization_text": format_factorization(gcd_n_k),
        },
        "reserve": reserve,
        "interleaving": {
            "mu": args.mu,
            "nu": args.nu,
        },
        "checks": checks,
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"name: {report['name'] or 'unnamed'}")
    print(f"domain: {report['domain']['type']} of size {report['domain']['n']}")
    print(f"n factorization: {report['domain']['n_factorization_text']}")
    print(
        "k={k} rho={rho} gcd(n,k)={gcd} ({factors})".format(
            k=report["code"]["k"],
            rho=report["code"]["rho"],
            gcd=report["code"]["gcd_n_k"],
            factors=report["code"]["gcd_n_k_factorization_text"],
        )
    )
    if report["reserve"] is not None:
        reserve = report["reserve"]
        print(
            "reserve: a={a} sigma={sigma} eta={eta} delta={delta}".format(
                a=reserve["a"],
                sigma=reserve["sigma"],
                eta=reserve["eta"],
                delta=reserve["delta"],
            )
        )
    print(f"interleaving: mu={report['interleaving']['mu']} nu={report['interleaving']['nu']}")

    print()
    print("fields")
    for label, field in report["fields"].items():
        if field["is_prime_power"]:
            field_text = f"{field['size']} = {field['prime']}^{field['degree']}"
        else:
            field_text = f"{field['size']} is not a prime power"
        print(f"  {label}: {field_text}, log2={field['log2_size']:.6f}")

    print()
    print("extensions")
    for label, value in report["extensions"].items():
        print(f"  {label}: {value if value is not None else 'not verified'}")

    print()
    print("checks")
    for item in report["checks"]:
        print(f"  [{item['status']}] {item['name']}: {item['detail']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Emit a field/domain descriptor for reserve certificates."
    )
    parser.add_argument("--q-arith", type=positive_int, required=True)
    parser.add_argument("--q-gen", type=positive_int, required=True)
    parser.add_argument("--q-line", type=positive_int, required=True)
    parser.add_argument("--q-chal", type=positive_int)
    parser.add_argument("--n", type=positive_int, required=True)
    parser.add_argument("--k", type=positive_int, required=True)
    parser.add_argument(
        "--domain-type",
        choices=(
            "multiplicative_subgroup",
            "multiplicative_coset",
            "extension_code",
            "circle_x_coordinate",
            "mixed_radix",
            "other",
        ),
        required=True,
    )
    parser.add_argument("--a", type=positive_int, help="agreement size")
    parser.add_argument("--sigma", type=nonnegative_int, help="agreement slack a-k")
    parser.add_argument("--mu", type=positive_int, default=1, help="protocol list arity")
    parser.add_argument("--nu", type=positive_int, default=1, help="MCA interleaving")
    parser.add_argument("--expected-extension-degree", type=positive_int)
    parser.add_argument("--name", help="optional descriptor name")
    parser.add_argument("--description", help="optional free-form description")
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
