#!/usr/bin/env python3
"""Verify the F1 minimal field descent packet.

The proof is field-theoretic.  This verifier checks the divisor-lattice
calculation and runs small concrete finite-field Frobenius descents using only
the Python standard library.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from math import gcd
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
ARTIFACT = (
    REPO
    / "experimental"
    / "data"
    / "certificates"
    / "f1-minimal-field-descent"
    / "f1_minimal_field_descent.json"
)


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def divisors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


def prime_factors(n: int) -> list[int]:
    out = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def check_lattice(max_n: int = 60) -> dict[str, Any]:
    cases = 0
    for n in range(1, max_n + 1):
        divs = divisors(n)
        for d1 in divs:
            for d2 in divs:
                if n % gcd(d1, d2) != 0:
                    raise AssertionError((n, d1, d2, "gcd"))
                if n % lcm(d1, d2) != 0:
                    raise AssertionError((n, d1, d2, "lcm"))
                cases += 1
        for b in divs:
            for dx in divs:
                fields = [d for d in divs if d % b == 0 and d % dx == 0]
                k = lcm(b, dx)
                if not fields:
                    raise AssertionError((n, b, dx, "empty fields"))
                if min(fields) != k:
                    raise AssertionError((n, b, dx, fields, k))
                if any(field % k for field in fields):
                    raise AssertionError((n, b, dx, fields, k, "not multiples"))
                cases += 1
    return {
        "max_N": max_n,
        "cases_checked": cases,
        "status": "PASS",
        "checks": [
            "subfield intersection degree is gcd",
            "subfield compositum degree is lcm",
            "minimal field containing base b and datum degree d_x is lcm(b,d_x)",
        ],
    }


def poly_mulmod(a: list[int], b: list[int], mod: list[int], p: int) -> list[int]:
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            res[i + j] = (res[i + j] + ai * bj) % p

    n = len(mod) - 1
    for i in range(len(res) - 1, n - 1, -1):
        coeff = res[i] % p
        if coeff == 0:
            continue
        for j in range(n + 1):
            res[i - n + j] = (res[i - n + j] - coeff * mod[j]) % p
    res = res[:n]
    while len(res) < n:
        res.append(0)
    return res


def field_pow(a: list[int], exponent: int, mod: list[int], p: int) -> list[int]:
    result = [1] + [0] * (len(mod) - 2)
    base = a[:]
    e = exponent
    while e:
        if e & 1:
            result = poly_mulmod(result, base, mod, p)
        base = poly_mulmod(base, base, mod, p)
        e >>= 1
    return result


def frobenius_power(x: list[int], p: int, steps: int, mod: list[int]) -> list[int]:
    y = x[:]
    for _ in range(steps):
        y = field_pow(y, p, mod, p)
    return y


def is_irreducible(mod: list[int], p: int, degree: int) -> bool:
    x = ([0, 1] + [0] * (degree - 1))[:degree]
    if frobenius_power(x, p, degree, mod) != x:
        return False
    for q in set(prime_factors(degree)):
        if frobenius_power(x, p, degree // q, mod) == x:
            return False
    return True


def find_irreducible(p: int, degree: int) -> list[int]:
    for coeffs in product(range(p), repeat=degree):
        if coeffs[0] == 0:
            continue
        mod = list(coeffs) + [1]
        if is_irreducible(mod, p, degree):
            return mod
    raise RuntimeError(f"no irreducible polynomial found for F_{p}^{degree}")


def check_concrete(p: int, degree: int, base_degree: int) -> dict[str, Any]:
    if degree % base_degree != 0:
        raise ValueError("base degree must divide extension degree")
    mod = find_irreducible(p, degree)
    counts = {"K=B": 0, "B<K<F": 0, "K=F": 0}
    for coeffs in product(range(p), repeat=degree):
        x = list(coeffs)
        y = field_pow(x, p, mod, p)
        dx = 1
        while y != x:
            y = field_pow(y, p, mod, p)
            dx += 1
            if dx > degree:
                raise AssertionError((p, degree, coeffs, "orbit did not close"))
        if degree % dx != 0:
            raise AssertionError((p, degree, coeffs, dx, "dx does not divide degree"))

        k = lcm(base_degree, dx)
        if degree % k != 0:
            raise AssertionError((p, degree, base_degree, dx, k, "K not subfield"))
        if k == base_degree:
            counts["K=B"] += 1
        elif k == degree:
            counts["K=F"] += 1
        else:
            counts["B<K<F"] += 1

    total = sum(counts.values())
    if total != p**degree:
        raise AssertionError((p, degree, total, p**degree))
    return {
        "p": p,
        "degree_N": degree,
        "base_degree_b": base_degree,
        "irreducible_modulus_coefficients_low_to_high": mod,
        "case_counts": counts,
        "total_elements": total,
        "status": "PASS",
    }


def build_certificate() -> dict[str, Any]:
    concrete_cases = [
        check_concrete(2, 6, 2),
        check_concrete(2, 12, 3),
        check_concrete(3, 4, 2),
        check_concrete(5, 4, 1),
    ]
    cert = {
        "schema": "f1-minimal-field-descent-v1",
        "status": "PROVED_BY_FIELD_THEORY_WITH_STDLIB_REPLAY",
        "source_dag_node": "f1_minimal_field_descent",
        "agents_md_priority": (
            "Highest-value item 5: extension-line MCA theorem or explicit "
            "corrected-reserve counterexample."
        ),
        "lattice_check": check_lattice(),
        "concrete_frobenius_checks": concrete_cases,
        "conclusion": (
            "Every finite-field pencil datum has a unique minimal field of "
            "definition K containing B, giving the exhaustive split K=B, "
            "B<K<F, or K=F."
        ),
        "non_claims": [
            "does not prove the full F1 pole-forcing/classification theorem",
            "does not provide a row-level adjacent upper certificate",
            "does not replace extension-pole/list threshold accounting",
        ],
        "note": "experimental/notes/f1/f1_minimal_field_descent.md",
    }
    validate(cert)
    return cert


def validate(cert: dict[str, Any]) -> None:
    if cert["schema"] != "f1-minimal-field-descent-v1":
        raise AssertionError("unexpected schema")
    if cert["lattice_check"]["status"] != "PASS":
        raise AssertionError("lattice check did not pass")
    for case in cert["concrete_frobenius_checks"]:
        if case["status"] != "PASS":
            raise AssertionError("concrete check did not pass")
        if sum(case["case_counts"].values()) != case["total_elements"]:
            raise AssertionError("case counts do not partition the field")
    if "K=B" not in cert["conclusion"] or "K=F" not in cert["conclusion"]:
        raise AssertionError("conclusion does not state the trichotomy")


def assert_same(expected: dict[str, Any], actual: dict[str, Any]) -> None:
    if expected != actual:
        raise AssertionError(
            "certificate mismatch\nexpected:\n"
            + json.dumps(expected, indent=2, sort_keys=True)
            + "\nactual:\n"
            + json.dumps(actual, indent=2, sort_keys=True)
        )


def print_summary(cert: dict[str, Any]) -> None:
    print("f1-minimal-field-descent certificate")
    print(f"  schema: {cert['schema']}")
    print(f"  status: {cert['status']}")
    print(f"  lattice cases: {cert['lattice_check']['cases_checked']}")
    for case in cert["concrete_frobenius_checks"]:
        print(
            f"  F_{case['p']}^{case['degree_N']} base={case['base_degree_b']} "
            f"counts={case['case_counts']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the default certificate")
    parser.add_argument("--check", type=Path, help="check an existing certificate")
    args = parser.parse_args()

    cert = build_certificate()
    if args.emit:
        ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
        ARTIFACT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n")
        print(f"wrote {ARTIFACT.relative_to(REPO)}")
    if args.check:
        actual = json.loads(args.check.read_text())
        validate(actual)
        assert_same(cert, actual)
        print(f"checked {args.check}")
    if not args.emit and not args.check:
        print_summary(cert)


if __name__ == "__main__":
    main()
