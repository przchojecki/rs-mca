#!/usr/bin/env python3
"""Verify small Dickson--Chebyshev circle-domain fiber identities.

Proof status: EXPERIMENTAL / AUDIT.

For odd p and even N | p+1, define

    X_N = {zeta + zeta^{-1} : zeta in mu_N(F_{p^2})} subset F_p.

The monic Dickson polynomial D_m is defined by D_m(z+z^{-1})=z^m+z^{-m}.
The Chebyshev transfer in slackMCA_v4.tex uses the finite identities

    D_m(X_N) = X_{N/m},
    D_m^{-1}(w) cap X_N has size m for w not in {+2,-2},
    locator(D_m^{-1}(w) cap X_N) = D_m(X)-w.

This script verifies those identities exactly for small prime fields.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

Element = Tuple[int, int]
Poly = List[int]


@dataclass(frozen=True)
class QuadraticField:
    """Arithmetic in F_p[u]/(u^2-d), with d a nonsquare."""

    p: int
    d: int

    def element(self, a: int, b: int = 0) -> Element:
        return (a % self.p, b % self.p)

    def add(self, x: Element, y: Element) -> Element:
        return ((x[0] + y[0]) % self.p, (x[1] + y[1]) % self.p)

    def sub(self, x: Element, y: Element) -> Element:
        return ((x[0] - y[0]) % self.p, (x[1] - y[1]) % self.p)

    def mul(self, x: Element, y: Element) -> Element:
        a = x[0] * y[0] + self.d * x[1] * y[1]
        b = x[0] * y[1] + x[1] * y[0]
        return (a % self.p, b % self.p)

    def pow(self, x: Element, exponent: int) -> Element:
        result = self.element(1)
        base = x
        value = exponent
        while value:
            if value & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            value >>= 1
        return result

    def conjugate(self, x: Element) -> Element:
        return (x[0], (-x[1]) % self.p)

    def norm(self, x: Element) -> int:
        return (x[0] * x[0] - self.d * x[1] * x[1]) % self.p


def prime_factors(value: int) -> List[int]:
    factors = []
    trial = 2
    remaining = value
    while trial * trial <= remaining:
        if remaining % trial == 0:
            factors.append(trial)
            while remaining % trial == 0:
                remaining //= trial
        trial += 1 if trial == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def least_nonsquare(p: int) -> int:
    for candidate in range(2, p):
        if pow(candidate, (p - 1) // 2, p) == p - 1:
            return candidate
    raise ValueError(f"could not find nonsquare modulo {p}")


def norm_one_elements(field: QuadraticField) -> List[Element]:
    elements = []
    for a in range(field.p):
        for b in range(field.p):
            x = field.element(a, b)
            if field.norm(x) == 1:
                elements.append(x)
    return elements


def norm_one_generator(field: QuadraticField) -> Element:
    order = field.p + 1
    factors = prime_factors(order)
    identity = field.element(1)
    for candidate in norm_one_elements(field):
        if candidate == identity:
            continue
        if all(field.pow(candidate, order // factor) != identity for factor in factors):
            return candidate
    raise ValueError(f"could not find norm-one generator for p={field.p}")


def mu_n_generator(field: QuadraticField, n: int) -> Element:
    if (field.p + 1) % n != 0:
        raise ValueError(f"N={n} must divide p+1={field.p + 1}")
    generator = norm_one_generator(field)
    return field.pow(generator, (field.p + 1) // n)


def circle_x_domain(field: QuadraticField, n: int) -> List[int]:
    generator = mu_n_generator(field, n)
    values = set()
    zeta = field.element(1)
    for _ in range(n):
        inverse = field.conjugate(zeta)
        x_value = field.add(zeta, inverse)
        if x_value[1] != 0:
            raise AssertionError(f"zeta+zeta^-1 not in base field: {x_value}")
        values.add(x_value[0])
        zeta = field.mul(zeta, generator)
    return sorted(values)


def trim(poly: Poly) -> Poly:
    result = poly[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_add(a: Poly, b: Poly, p: int) -> Poly:
    size = max(len(a), len(b))
    result = [0] * size
    for i in range(size):
        result[i] = ((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p
    return trim(result)


def poly_sub(a: Poly, b: Poly, p: int) -> Poly:
    size = max(len(a), len(b))
    result = [0] * size
    for i in range(size):
        result[i] = ((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % p
    return trim(result)


def poly_mul_x(a: Poly, p: int) -> Poly:
    return [0] + [coefficient % p for coefficient in a]


def poly_mul(a: Poly, b: Poly, p: int) -> Poly:
    result = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            result[i + j] = (result[i + j] + ai * bj) % p
    return trim(result)


def poly_eval(poly: Poly, x: int, p: int) -> int:
    result = 0
    for coefficient in reversed(poly):
        result = (result * x + coefficient) % p
    return result


def dickson_poly(m: int, p: int) -> Poly:
    if m == 0:
        return [2 % p]
    if m == 1:
        return [0, 1]
    previous = [2 % p]
    current = [0, 1]
    for _ in range(2, m + 1):
        next_poly = poly_sub(poly_mul_x(current, p), previous, p)
        previous, current = current, next_poly
    return current


def locator_poly(roots: Sequence[int], p: int) -> Poly:
    result = [1]
    for root in roots:
        result = poly_mul(result, [(-root) % p, 1], p)
    return result


def verify_case(p: int, n: int, m: int) -> Dict[str, object]:
    if p % 2 == 0:
        raise ValueError("p must be odd")
    if (p + 1) % n != 0:
        raise ValueError(f"N={n} must divide p+1={p + 1}")
    if n % m != 0:
        raise ValueError(f"m={m} must divide N={n}")
    if n % 2 != 0 or (n // m) % 2 != 0:
        raise ValueError("N and N/m must be even for this X_N convention")

    field = QuadraticField(p=p, d=least_nonsquare(p))
    domain = circle_x_domain(field, n)
    target_domain = circle_x_domain(field, n // m)
    dickson = dickson_poly(m, p)
    if len(dickson) != m + 1 or dickson[-1] != 1:
        raise AssertionError(f"D_{m} is not monic degree {m}: {dickson}")

    image = sorted({poly_eval(dickson, x, p) for x in domain})
    image_matches = image == target_domain
    interior = [w for w in target_domain if w not in {2 % p, (-2) % p}]
    fiber_records = []
    all_fibers_ok = True
    all_locators_ok = True
    for w in interior:
        roots = sorted(x for x in domain if poly_eval(dickson, x, p) == w)
        expected = dickson[:]
        expected[0] = (expected[0] - w) % p
        locator = locator_poly(roots, p)
        fiber_ok = len(roots) == m
        locator_ok = locator == trim(expected)
        all_fibers_ok = all_fibers_ok and fiber_ok
        all_locators_ok = all_locators_ok and locator_ok
        fiber_records.append(
            {
                "w": w,
                "fiber_size": len(roots),
                "fiber_ok": fiber_ok,
                "locator_ok": locator_ok,
                "roots": roots,
            }
        )

    return {
        "p": p,
        "n": n,
        "m": m,
        "field": f"F_{p}[u]/(u^2-{field.d})",
        "domain_size": len(domain),
        "expected_domain_size": n // 2 + 1,
        "target_size": len(target_domain),
        "expected_target_size": n // (2 * m) + 1,
        "domain": domain,
        "target_domain": target_domain,
        "dickson_coefficients_low_to_high": dickson,
        "image": image,
        "image_matches_target": image_matches,
        "interior_target_count": len(interior),
        "all_fibers_size_m": all_fibers_ok,
        "all_locators_match": all_locators_ok,
        "passed": image_matches and all_fibers_ok and all_locators_ok,
        "fibers": fiber_records,
    }


def divisors(value: int) -> List[int]:
    return [candidate for candidate in range(1, value + 1) if value % candidate == 0]


def default_cases(p: int) -> List[Tuple[int, int]]:
    cases = []
    for n in divisors(p + 1):
        if n < 8 or n % 2:
            continue
        for m in divisors(n):
            if m <= 1 or (n // m) < 4 or (n // m) % 2:
                continue
            cases.append((n, m))
    return cases


def parse_case(raw: str) -> Tuple[int, int]:
    try:
        n_raw, m_raw = raw.split(":")
        return (int(n_raw), int(m_raw))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("cases must have form N:m") from exc


def print_text(result: Dict[str, object]) -> None:
    print("Chebyshev circle-domain fiber verifier")
    print("proof_status: EXPERIMENTAL / AUDIT")
    print("object: D_m(X_N)=X_{N/m} and locator(D_m^{-1}(w))=D_m(X)-w")
    print()
    for case in result["cases"]:
        print(
            "p={p} N={n:<3} m={m:<3} |X_N|={size:<3} |X_target|={target:<3} "
            "image={image} fibers={fibers} locators={locators} passed={passed}".format(
                p=case["p"],
                n=case["n"],
                m=case["m"],
                size=case["domain_size"],
                target=case["target_size"],
                image="OK" if case["image_matches_target"] else "FAIL",
                fibers="OK" if case["all_fibers_size_m"] else "FAIL",
                locators="OK" if case["all_locators_match"] else "FAIL",
                passed="OK" if case["passed"] else "FAIL",
            )
        )
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify small Dickson--Chebyshev circle-domain fiber identities."
    )
    parser.add_argument("--prime", type=int, default=31, help="odd prime p")
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        type=parse_case,
        metavar="N:m",
        help="verify a specific case with N | p+1 and m | N",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    args = parser.parse_args()

    cases = args.case or default_cases(args.prime)
    results = [verify_case(args.prime, n, m) for n, m in cases]
    output = {
        "proof_status": "EXPERIMENTAL / AUDIT",
        "theorem_problem_id": "X3-Chebyshev-circle-fiber-transfer",
        "determinism": "deterministic finite-field verification; no random seed",
        "object_checked": (
            "D_m(X_N)=X_{N/m}; interior fibers have size m and locator D_m(X)-w"
        ),
        "cases": results,
    }
    if args.format == "json":
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print_text(output)


if __name__ == "__main__":
    main()
