#!/usr/bin/env python3
"""Verify the M1 all-line Hankel aperiodic split-locator ledger.

Status: PROVED finite normal form / AUDIT verifier.

This script checks the finite object requested by the M1 all-line aperiodic
residue-packing target.  It enumerates split complement locators T, applies the
Hankel-pencil gate

    (H(u)+zH(v)) ell_T = 0,

removes contained/tangent-core locators with H(v)ell_T=0, labels whole-fiber
quotient-periodic complements on cyclic multiplicative domains, and reports the
remaining aperiodic slope image.  Every reported bad slope is cross-checked by
direct Reed-Solomon interpolation on the support D \\ T.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


def inv_mod(x: int, p: int) -> int:
    if x % p == 0:
        raise ZeroDivisionError("zero")
    return pow(x % p, p - 2, p)


def primitive_root(p: int) -> int:
    factors = set()
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.add(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        factors.add(value)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise AssertionError(f"no primitive root for {p}")


def cyclic_domain(p: int, n: int) -> tuple[tuple[int, ...], dict[int, int], int]:
    if (p - 1) % n:
        raise AssertionError("n must divide p-1")
    gen = pow(primitive_root(p), (p - 1) // n, p)
    domain = tuple(pow(gen, i, p) for i in range(n))
    exponents = {x: i for i, x in enumerate(domain)}
    if len(exponents) != n:
        raise AssertionError("domain generator has wrong order")
    return domain, exponents, gen


def poly_mul(left: list[int], right: list[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % p
    return trim_mod(out, p)


def trim_mod(poly: list[int], p: int) -> list[int]:
    out = [x % p for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_eval(poly: list[int], x: int, p: int) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x + coeff) % p
    return value


def poly_degree(poly: list[int]) -> int:
    return len(poly) - 1


def interpolate(points: tuple[int, ...], values: tuple[int, ...], p: int) -> list[int]:
    result = [0]
    for i, xi in enumerate(points):
        basis = [1]
        denom = 1
        for j, xj in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, [(-xj) % p, 1], p)
            denom = denom * ((xi - xj) % p) % p
        scale = values[i] * inv_mod(denom, p) % p
        if len(result) < len(basis):
            result.extend([0] * (len(basis) - len(result)))
        for idx, coeff in enumerate(basis):
            result[idx] = (result[idx] + scale * coeff) % p
    return trim_mod(result, p)


def locator(points: tuple[int, ...], p: int) -> list[int]:
    poly = [1]
    for x in points:
        poly = poly_mul(poly, [(-x) % p, 1], p)
    return poly


def lambda_weights(domain: tuple[int, ...], p: int) -> dict[int, int]:
    weights = {}
    for x in domain:
        denom = 1
        for y in domain:
            if x != y:
                denom = denom * ((x - y) % p) % p
        weights[x] = inv_mod(denom, p)
    return weights


def syndrome(values: dict[int, int], domain: tuple[int, ...], r: int, p: int) -> tuple[int, ...]:
    weights = lambda_weights(domain, p)
    out = []
    for m in range(r):
        total = 0
        for x in domain:
            total = (total + weights[x] * pow(x, m, p) * values[x]) % p
        out.append(total)
    return tuple(out)


def hankel_apply(syn: tuple[int, ...], t: int, j: int, ell: list[int], p: int) -> tuple[int, ...]:
    return tuple(
        sum(syn[row + col] * ell[col] for col in range(j + 1)) % p
        for row in range(t)
    )


def slope_from_gate(a_vec: tuple[int, ...], b_vec: tuple[int, ...], p: int) -> int | None:
    if all(x == 0 for x in b_vec):
        return None
    slope = None
    for a, b in zip(a_vec, b_vec):
        if b == 0:
            if a != 0:
                return None
            continue
        candidate = (-a * inv_mod(b, p)) % p
        if slope is None:
            slope = candidate
        elif slope != candidate:
            return None
    return slope


def word_value(kind: str, x: int, p: int) -> int:
    if kind == "f":
        return (pow(x, 13, p) + 3 * pow(x, 7, p) + 5 * x + 4) % p
    if kind == "g":
        return (2 * pow(x, 14, p) + pow(x, 11, p) + 6 * pow(x, 3, p) + 1) % p
    raise AssertionError(kind)


def is_explained_on_support(
    word: dict[int, int], support: tuple[int, ...], k: int, p: int
) -> bool:
    seed = support[:k]
    poly = interpolate(seed, tuple(word[x] for x in seed), p)
    if poly_degree(poly) >= k:
        raise AssertionError("interpolant degree should be < k")
    return all(poly_eval(poly, x, p) == word[x] for x in support)


def is_quotient_periodic(
    complement: tuple[int, ...],
    domain: tuple[int, ...],
    exponents: dict[int, int],
    charged_fiber_sizes: tuple[int, ...],
) -> bool:
    n = len(domain)
    comp = set(complement)
    for m in charged_fiber_sizes:
        if m <= 1 or m >= n or n % m or len(comp) % m:
            continue
        quotient_size = n // m
        ok = True
        for residue in range(quotient_size):
            fiber = {
                x for x in domain
                if exponents[x] % quotient_size == residue
            }
            if bool(fiber & comp) and not fiber <= comp:
                ok = False
                break
        if ok:
            return True
    return False


@dataclass(frozen=True)
class Case:
    name: str
    p: int
    n: int
    j: int
    t: int
    charged_fiber_sizes: tuple[int, ...]


def verify_case(case: Case) -> dict[str, object]:
    p, n, j, t = case.p, case.n, case.j, case.t
    k = n - j - t
    if k <= 0:
        raise AssertionError("invalid k")
    domain, exponents, _ = cyclic_domain(p, n)
    f = {x: word_value("f", x, p) for x in domain}
    g = {x: word_value("g", x, p) for x in domain}
    u = syndrome(f, domain, j + t, p)
    v = syndrome(g, domain, j + t, p)

    bad_slopes: set[int] = set()
    quotient_slopes: set[int] = set()
    aperiodic_slopes: set[int] = set()
    bad_locators = 0
    quotient_locators = 0
    aperiodic_locators = 0
    contained_core = 0
    direct_checks = 0

    for complement in combinations(domain, j):
        ell = locator(complement, p)
        a_vec = hankel_apply(u, t, j, ell, p)
        b_vec = hankel_apply(v, t, j, ell, p)
        if all(x == 0 for x in b_vec):
            contained_core += 1
            continue
        slope = slope_from_gate(a_vec, b_vec, p)
        if slope is None:
            continue

        support = tuple(x for x in domain if x not in set(complement))
        line_word = {x: (f[x] + slope * g[x]) % p for x in domain}
        if not is_explained_on_support(line_word, support, k, p):
            raise AssertionError("Hankel bad slope failed direct RS check")
        if is_explained_on_support(g, support, k, p):
            raise AssertionError("noncontained Hankel slope was contained")
        direct_checks += 1

        bad_locators += 1
        bad_slopes.add(slope)
        if is_quotient_periodic(complement, domain, exponents, case.charged_fiber_sizes):
            quotient_locators += 1
            quotient_slopes.add(slope)
        else:
            aperiodic_locators += 1
            aperiodic_slopes.add(slope)

    if not aperiodic_slopes <= bad_slopes:
        raise AssertionError("aperiodic slopes escaped bad slope set")
    if not quotient_slopes <= bad_slopes:
        raise AssertionError("quotient slopes escaped bad slope set")
    if bad_locators != quotient_locators + aperiodic_locators:
        raise AssertionError("charged/aperiodic locator partition failed")

    return {
        "name": case.name,
        "p": p,
        "n": n,
        "k": k,
        "j": j,
        "t": t,
        "q_line": p,
        "charged_fiber_sizes": case.charged_fiber_sizes,
        "split_locators": sum(1 for _ in combinations(domain, j)),
        "contained_core_locators": contained_core,
        "bad_locators": bad_locators,
        "bad_slopes": len(bad_slopes),
        "quotient_locators": quotient_locators,
        "quotient_slopes": len(quotient_slopes),
        "aperiodic_locators": aperiodic_locators,
        "aperiodic_slopes": len(aperiodic_slopes),
        "direct_checks": direct_checks,
    }


def main() -> None:
    cases = (
        Case("F17_full_j4_t2", p=17, n=16, j=4, t=2, charged_fiber_sizes=(2, 4, 8)),
        Case("F17_order8_j3_t2", p=17, n=8, j=3, t=2, charged_fiber_sizes=(2, 4)),
        Case("F13_order12_j4_t2", p=13, n=12, j=4, t=2, charged_fiber_sizes=(2, 3, 4, 6)),
    )
    rows = [verify_case(case) for case in cases]
    for row in rows:
        print(
            "{name}: p={p} n={n} k={k} j={j} t={t} split={split_locators} "
            "bad_locators={bad_locators} bad_slopes={bad_slopes} "
            "quotient_locators={quotient_locators} quotient_slopes={quotient_slopes} "
            "aperiodic_locators={aperiodic_locators} aperiodic_slopes={aperiodic_slopes} "
            "contained_core={contained_core_locators} direct_checks={direct_checks}".format(**row)
        )
    max_aperiodic = max(row["aperiodic_slopes"] for row in rows)
    print(f"m1_all_line_hankel_aperiodic: PASS cases={len(rows)} max_aperiodic_slopes={max_aperiodic}")


if __name__ == "__main__":
    main()
