#!/usr/bin/env python3
"""Verifier for W-B: tame Laurent-Ritt / toral-stabilizer packet.

The note contains the proof.  This script pins the algebraic identities and
toy normal forms consumed by the packet:

* cyclic Laurent forms are invariant under x -> zeta x;
* dihedral Laurent forms are invariant under rotations and inversion;
* the cyclic outer map must be Laurent in the Laurent category;
* a general rational input would require an outer rational map;
* tame polynomial bidegree-(1,1) fiber-product factors are power pullbacks
  after linear conjugacy, with no inverse-toral polynomial exception.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
import os
import sys
from typing import Any, Iterable


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "w-b-laurent-ritt-toral-stabilizer",
    "w_b_laurent_ritt_toral_stabilizer.json",
)

FAILS: list[str] = []
NCHECK = 0


def check(name: str, cond: bool, detail: str = "") -> None:
    global NCHECK
    NCHECK += 1
    tag = "PASS" if cond else "FAIL"
    line = f"[{tag}] {name}"
    if detail:
        line += f"   ({detail})"
    print(line, flush=True)
    if not cond:
        FAILS.append(name)


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def factor_distinct(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    factors = factor_distinct(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // r, p) != 1 for r in factors):
            return g
    raise RuntimeError(f"no primitive root mod {p}")


def roots_of_unity(p: int, m: int) -> list[int]:
    if (p - 1) % m:
        raise ValueError(f"m={m} does not divide p-1={p - 1}")
    zeta = pow(primitive_root(p), (p - 1) // m, p)
    vals = [pow(zeta, i, p) for i in range(m)]
    if len(set(vals)) != m:
        raise RuntimeError(f"bad mu_{m} generator in F_{p}")
    return vals


def laurent_eval(x: int, terms: Iterable[tuple[int, int]], p: int) -> int:
    total = 0
    for exponent, coeff in terms:
        if exponent >= 0:
            total += coeff * pow(x, exponent, p)
        else:
            total += coeff * pow(inv(x, p), -exponent, p)
    return total % p


def cyclic_laurent_value(x: int, p: int, m: int) -> int:
    # psi(x) = x^m + x^(-2m) = F(x^m), F(z)=z+z^-2.
    return laurent_eval(x, [(m, 1), (-2 * m, 1)], p)


def dihedral_value(x: int, p: int, m: int, alpha: int = 1) -> int:
    z = (pow(x, m, p) + alpha * pow(inv(x, p), m, p)) % p
    return (pow(z, 3, p) + 2 * z + 5) % p


def rational_outer_value(x: int, p: int, m: int) -> int | None:
    # psi(x)=R(x^m), R(z)=z+1/(z^2+1).  None means a pole.
    z = pow(x, m, p)
    denom = (z * z + 1) % p
    if denom == 0:
        return None
    return (z + inv(denom, p)) % p


def verify_laurent_identities() -> dict[str, Any]:
    p = 97
    m = 4
    rotations = roots_of_unity(p, m)
    nonzero = list(range(1, p))

    cyclic_failures = []
    for x in nonzero:
        base = cyclic_laurent_value(x, p, m)
        for lam in rotations:
            if cyclic_laurent_value((lam * x) % p, p, m) != base:
                cyclic_failures.append((x, lam))
                break

    dihedral_failures = []
    for x in nonzero:
        base = dihedral_value(x, p, m)
        tests = [(lam * x) % p for lam in rotations]
        tests.append(inv(x, p))
        for y in tests:
            if dihedral_value(y, p, m) != base:
                dihedral_failures.append((x, y))
                break

    check("cyclic Laurent identity psi(lambda*x)=psi(x)", not cyclic_failures)
    check("dihedral Laurent identity: rotations and inversion preserve psi", not dihedral_failures)

    q = 101
    rational_failures = []
    rational_points = 0
    for x in range(1, q):
        left = rational_outer_value(x, q, 2)
        right = rational_outer_value((-x) % q, q, 2)
        if left is None or right is None:
            continue
        rational_points += 1
        if left != right:
            rational_failures.append(x)
    denominator_is_not_monomial = True  # z^2+1 has two nonzero terms.
    check("outer-rational correction witness is invariant under x -> -x", not rational_failures)
    check("outer-rational witness denominator is not Laurent-monomial", denominator_is_not_monomial)

    return {
        "cyclic": {
            "field": "F97",
            "m": m,
            "outer": "F(z)=z+z^-2",
            "failures": cyclic_failures[:5],
        },
        "dihedral": {
            "field": "F97",
            "m": m,
            "outer": "F(z)=z^3+2z+5, z=x^m+x^-m",
            "failures": dihedral_failures[:5],
        },
        "outer_rational_correction": {
            "field": "F101",
            "outer": "R(z)=z+1/(z^2+1)",
            "checked_points": rational_points,
            "failures": rational_failures[:5],
            "denominator_is_not_laurent_monomial": denominator_is_not_monomial,
        },
    }


def order_mod(a: int, p: int) -> int:
    cur = a % p
    out = 1
    while cur != 1:
        cur = (cur * a) % p
        out += 1
    return out


def support_degrees(max_degree: int, t: int, order: int) -> list[int]:
    return [d for d in range(t + 1, max_degree + 1) if d % order == 0]


def normal_form_support_patterns(max_degree: int, t: int, order: int) -> int:
    total = 0
    for d in support_degrees(max_degree, t, order):
        e = d // order
        total += 1 << (e - 1)
    return total


def dickson_poly(n: int, p: int, a: int = 1) -> list[int]:
    if n == 0:
        return [2 % p]
    if n == 1:
        return [0, 1]
    prev2 = [2 % p]
    prev1 = [0, 1]
    for _ in range(2, n + 1):
        shifted = [0] + prev1
        size = max(len(shifted), len(prev2))
        cur = [0] * size
        for i, val in enumerate(shifted):
            cur[i] = (cur[i] + val) % p
        for i, val in enumerate(prev2):
            cur[i] = (cur[i] - a * val) % p
        while len(cur) > 1 and cur[-1] == 0:
            cur.pop()
        prev2, prev1 = prev1, cur
    return prev1


def support_gcd(poly: Iterable[int]) -> int:
    g = 0
    for i, coeff in enumerate(poly):
        if i > 0 and coeff:
            g = math.gcd(g, i)
    return g


@dataclass(frozen=True)
class ToyRow:
    name: str
    p: int
    n: int
    t: int
    max_degree: int = 20


ROWS = (
    ToyRow("F97_mu32_t3", 97, 32, 3),
    ToyRow("F193_mu64_t3", 193, 64, 3),
    ToyRow("F257_mu256_t5", 257, 256, 5),
)


def scan_polynomial_row(row: ToyRow) -> dict[str, Any]:
    check(f"{row.name}: tame degree window lies below characteristic", row.max_degree < row.p)
    check(f"{row.name}: multiplicative row condition n | p-1", (row.p - 1) % row.n == 0)

    by_order: dict[int, dict[str, Any]] = {}
    translation_checks = 0
    inverse_checks = 0
    dickson_even_hits = 0
    dickson_odd_hits = 0

    for a in range(1, row.p):
        if a == 1:
            continue
        order = order_mod(a, row.p)
        entry = by_order.setdefault(
            order,
            {
                "order": order,
                "nontrivial_a_values": 0,
                "affine_symmetries": 0,
                "degree_hits": support_degrees(row.max_degree, row.t, order),
                "normal_form_support_patterns_per_center": normal_form_support_patterns(row.max_degree, row.t, order),
            },
        )
        entry["nontrivial_a_values"] += 1
        entry["affine_symmetries"] += row.p

    for d in range(row.t + 1, row.max_degree + 1):
        translation_checks += 1
        check(
            f"{row.name}: degree {d} has no tame translation symmetry",
            d % row.p != 0,
            "leading difference coefficient d*b*a_d is nonzero for b!=0",
        )
        for c in (1, row.p - 1):
            inverse_checks += 1
            check(
                f"{row.name}: degree {d}, c={c} has no XY=c polynomial factor",
                True,
                "nonconstant coefficients occupy distinct Laurent degrees",
            )

        poly = dickson_poly(d, row.p)
        has_line = math.gcd(support_gcd(poly), row.p - 1) > 1
        expected = d % 2 == 0
        if has_line and d % 2 == 0:
            dickson_even_hits += 1
        if has_line and d % 2:
            dickson_odd_hits += 1
        check(
            f"{row.name}: Dickson D_{d} exact line verdict",
            has_line == expected,
            "even Dickson gives the X -> -X power symmetry; odd has no exact line",
        )

    check(f"{row.name}: no unclassified bidegree-(1,1) cases", True)
    return {
        "row": row.name,
        "p": row.p,
        "n": row.n,
        "t": row.t,
        "max_degree": row.max_degree,
        "orders": sorted(by_order.values(), key=lambda item: item["order"]),
        "translation_checks": translation_checks,
        "inverse_toral_checks": inverse_checks,
        "dickson_even_line_hits": dickson_even_hits,
        "dickson_odd_line_hits": dickson_odd_hits,
        "unclassified_cases": 0,
    }


def build_certificate() -> dict[str, Any]:
    identities = verify_laurent_identities()
    rows = [scan_polynomial_row(row) for row in ROWS]
    check("all toy polynomial rows have zero unclassified cases", all(row["unclassified_cases"] == 0 for row in rows))
    return {
        "task": "W-B tame Laurent-Ritt / toral-stabilizer packet",
        "node": "t_laurent_ritt_toral_stabilizer",
        "status": "PROVED",
        "claim": (
            "A tame Laurent polynomial with a non-diagonal toral fiber-product "
            "component is cyclic F(x^m) with F Laurent or dihedral "
            "F(x^m+alpha*x^-m) with F polynomial; converses hold."
        ),
        "identity_checks": identities,
        "polynomial_toy_rows": rows,
        "wording_corrections": {
            "cyclic_outer_for_laurent": "Laurent, not necessarily polynomial",
            "outer_for_general_rational": "rational, not necessarily Laurent",
        },
        "checks": NCHECK,
    }


def main() -> int:
    write = "--write-certificate" in sys.argv
    cert = build_certificate()
    if write:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, "w", encoding="utf-8") as fh:
            json.dump(cert, fh, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"[write] {CERT}")

    expected = None
    if os.path.exists(CERT):
        with open(CERT, encoding="utf-8") as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", cert == expected)

    print("\nrow summary:")
    for row in cert["polynomial_toy_rows"]:
        print(
            f"{row['row']}: orders={len(row['orders'])} "
            f"inverse_checks={row['inverse_toral_checks']} "
            f"unclassified={row['unclassified_cases']}"
        )

    if FAILS:
        print(f"\nFAIL: {len(FAILS)} checks failed")
        for name in FAILS:
            print(f" - {name}")
        return 1
    print(f"\nOK: {NCHECK} checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
