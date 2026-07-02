#!/usr/bin/env python3
"""Toy verifier for the Conjecture F reduction lemmas.

The proofs are elementary and live in the companion note.  This script checks
the identities over F_97 with H = mu_16:

* common-GCD division maps D_j(H) points injectively into D_{j-w}(H');
* quotient pullback g(Y) -> g(X^M) is exactly the M-periodic stratum;
* gcd-trivial projective pencils meet D_j(H) in at most floor(n/j) points.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from math import comb
from pathlib import Path


P = 97
N = 16
J_GCD = 5
COMMON_DEGREE = 2
J_SCALE = 6
SCALE_M = 2
J_VOTING = 4
PENCIL_TRIALS = 500
SEED = 2026070202
OUTPUT = Path(
    "experimental/data/certificates/conjecture-f-reductions/"
    "conjecture_f_reductions_toy.json"
)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def primitive_root(p: int) -> int:
    factors = []
    m = p - 1
    d = 2
    while d * d <= m:
        if m % d == 0:
            factors.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        factors.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise RuntimeError(f"no primitive root for F_{p}")


def subgroup(order: int) -> list[int]:
    g = primitive_root(P)
    omega = pow(g, (P - 1) // order, P)
    values = [pow(omega, i, P) for i in range(order)]
    assert len(set(values)) == order
    return values


def trim(poly: tuple[int, ...]) -> tuple[int, ...]:
    out = list(poly)
    while len(out) > 1 and out[-1] % P == 0:
        out.pop()
    return tuple(x % P for x in out)


def poly_add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    n = max(len(a), len(b))
    return trim(tuple(((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % P for i in range(n)))


def poly_scale(c: int, a: tuple[int, ...]) -> tuple[int, ...]:
    return trim(tuple((c * x) % P for x in a))


def poly_mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = (out[i + j] + ai * bj) % P
    return trim(tuple(out))


def poly_eval(poly: tuple[int, ...], x: int) -> int:
    acc = 0
    for coeff in reversed(poly):
        acc = (acc * x + coeff) % P
    return acc


def poly_div_exact(poly: tuple[int, ...], divisor: tuple[int, ...]) -> tuple[int, ...]:
    rem = list(poly)
    div = trim(divisor)
    assert div[-1] == 1
    q = [0] * (max(0, len(rem) - len(div)) + 1)
    while len(rem) >= len(div):
        coeff = rem[-1] % P
        shift = len(rem) - len(div)
        q[shift] = coeff
        for i, di in enumerate(div):
            rem[shift + i] = (rem[shift + i] - coeff * di) % P
        while rem and rem[-1] % P == 0:
            rem.pop()
    assert not rem
    return trim(tuple(q))


def locator(roots: tuple[int, ...]) -> tuple[int, ...]:
    poly = (1,)
    for root in roots:
        poly = poly_mul(poly, ((-root) % P, 1))
    return poly


def compose_x_power(poly: tuple[int, ...], power: int) -> tuple[int, ...]:
    out = [0] * ((len(poly) - 1) * power + 1)
    for i, coeff in enumerate(poly):
        out[i * power] = coeff % P
    return trim(tuple(out))


def monic_degree_j(poly: tuple[int, ...], j: int) -> tuple[int, ...] | None:
    poly = trim(poly)
    if len(poly) != j + 1 or poly[-1] == 0:
        return None
    inv = pow(poly[-1], -1, P)
    return poly_scale(inv, poly)


def divisor_set(H: list[int], j: int) -> set[tuple[int, ...]]:
    return {locator(tuple(combo)) for combo in itertools.combinations(H, j)}


def root_set(poly: tuple[int, ...], H: list[int]) -> set[int]:
    return {x for x in H if poly_eval(poly, x) == 0}


def check_gcd_reduction(H: list[int]) -> dict:
    common_roots = tuple(H[:COMMON_DEGREE])
    G = locator(common_roots)
    H_reduced = H[COMMON_DEGREE:]
    containing = [
        locator(tuple(combo))
        for combo in itertools.combinations(H, J_GCD)
        if set(common_roots).issubset(combo)
    ]
    images = {poly_div_exact(poly, G) for poly in containing}
    target = divisor_set(H_reduced, J_GCD - COMMON_DEGREE)
    linearity_ok = True
    rng = random.Random(SEED)
    for _ in range(25):
        a = rng.randrange(P)
        b = rng.randrange(P)
        q1 = rng.choice(tuple(images))
        q2 = rng.choice(tuple(images))
        left = poly_add(poly_scale(a, poly_mul(G, q1)), poly_scale(b, poly_mul(G, q2)))
        right = poly_mul(G, poly_add(poly_scale(a, q1), poly_scale(b, q2)))
        linearity_ok &= trim(left) == trim(right)
    ok = len(images) == len(containing) == comb(N - COMMON_DEGREE, J_GCD - COMMON_DEGREE)
    ok &= images == target
    ok &= linearity_ok
    return {
        "name": "common_gcd_reduction",
        "status": "PASS" if ok else "FAIL",
        "n": N,
        "j": J_GCD,
        "common_degree": COMMON_DEGREE,
        "source_count": len(containing),
        "image_count": len(images),
        "target_count": len(target),
        "linearity_spot_checks": 25,
    }


def check_scale_recursion(H: list[int]) -> dict:
    small_order = N // SCALE_M
    H_small = subgroup(small_order)
    small_divisors = divisor_set(H_small, J_SCALE // SCALE_M)
    image = {compose_x_power(g, SCALE_M) for g in small_divisors}
    periodic = set()
    for combo in itertools.combinations(range(N), J_SCALE):
        exponents = set(combo)
        is_union = all(((e + small_order) % N) in exponents for e in exponents)
        if is_union:
            periodic.add(locator(tuple(H[i] for i in combo)))
    roots_match = True
    for g in small_divisors:
        pulled = compose_x_power(g, SCALE_M)
        expected = {x for x in H if poly_eval(g, pow(x, SCALE_M, P)) == 0}
        roots_match &= root_set(pulled, H) == expected
    ok = image == periodic
    ok &= len(image) == comb(small_order, J_SCALE // SCALE_M)
    ok &= roots_match
    return {
        "name": "quotient_pullback_scale_recursion",
        "status": "PASS" if ok else "FAIL",
        "n": N,
        "M": SCALE_M,
        "j": J_SCALE,
        "small_order": small_order,
        "image_count": len(image),
        "periodic_count": len(periodic),
        "expected_count": comb(small_order, J_SCALE // SCALE_M),
    }


def independent(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    scalar = None
    for ai, bi in itertools.zip_longest(a, b, fillvalue=0):
        ai %= P
        bi %= P
        if bi == 0:
            if ai != 0:
                return True
            continue
        candidate = ai * pow(bi, -1, P) % P
        if scalar is None:
            scalar = candidate
        elif scalar != candidate:
            return True
    return False


def gcd_trivial_on_H(a: tuple[int, ...], b: tuple[int, ...], H: list[int]) -> bool:
    return all((poly_eval(a, x), poly_eval(b, x)) != (0, 0) for x in H)


def projective_line(a: tuple[int, ...], b: tuple[int, ...]) -> list[tuple[int, ...]]:
    return [poly_add(a, poly_scale(z, b)) for z in range(P)] + [b]


def random_poly(rng: random.Random, max_degree: int) -> tuple[int, ...]:
    return trim(tuple(rng.randrange(P) for _ in range(max_degree + 1)))


def count_divisor_points(a: tuple[int, ...], b: tuple[int, ...],
                         D: set[tuple[int, ...]]) -> int:
    count = 0
    seen = set()
    for poly in projective_line(a, b):
        monic = monic_degree_j(poly, J_VOTING)
        if monic is not None and monic in D and monic not in seen:
            seen.add(monic)
            count += 1
    return count


def check_voting_bound(H: list[int]) -> dict:
    D = divisor_set(H, J_VOTING)
    bound = N // J_VOTING
    rng = random.Random(SEED + 1)
    max_count = 0
    accepted = 0
    attempts = 0

    # First include deterministic pencils through disjoint divisor points.
    divisor_list = sorted(D)
    for a in divisor_list[:30]:
        for b in divisor_list[-30:]:
            attempts += 1
            if independent(a, b) and gcd_trivial_on_H(a, b, H):
                count = count_divisor_points(a, b, D)
                max_count = max(max_count, count)
                accepted += 1
                if count > bound:
                    return {
                        "name": "dimension_one_voting_bound",
                        "status": "FAIL",
                        "counterexample_count": count,
                        "bound": bound,
                    }

    while accepted < PENCIL_TRIALS:
        attempts += 1
        a = random_poly(rng, J_VOTING)
        b = random_poly(rng, J_VOTING)
        if not independent(a, b):
            continue
        if not gcd_trivial_on_H(a, b, H):
            continue
        count = count_divisor_points(a, b, D)
        max_count = max(max_count, count)
        accepted += 1
        if count > bound:
            return {
                "name": "dimension_one_voting_bound",
                "status": "FAIL",
                "counterexample_count": count,
                "bound": bound,
            }
    return {
        "name": "dimension_one_voting_bound",
        "status": "PASS",
        "n": N,
        "j": J_VOTING,
        "projective_bound": bound,
        "accepted_pencils": accepted,
        "attempts": attempts,
        "max_observed_divisor_points": max_count,
    }


def build_report() -> dict:
    H = subgroup(N)
    checks = [
        check_gcd_reduction(H),
        check_scale_recursion(H),
        check_voting_bound(H),
    ]
    return {
        "schema": "conjecture_f_reduction_toy_v1",
        "status": "EXPERIMENTAL_VERIFICATION_OF_PROVED_LEMMAS",
        "field": {"p": P},
        "domain": {"type": "mu_n", "n": N, "elements": H},
        "checks": checks,
        "script_sha256": sha256_text(Path(__file__).read_text()),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    report = build_report()
    print("=" * 72)
    print("Conjecture F reduction lemmas toy verifier")
    print("=" * 72)
    ok = True
    for check in report["checks"]:
        ok &= check["status"] == "PASS"
        print(f"[{check['status']}] {check['name']}")
        for key, value in check.items():
            if key not in {"name", "status"}:
                print(f"        {key}: {value}")
    if args.emit:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {OUTPUT}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
