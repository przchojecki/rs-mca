#!/usr/bin/env python3
"""Verifier for W-C: large-characteristic lift and dyadic descent.

This checks the arithmetic used by the proof:

* the norm threshold max_r binom(b,r)^phi(n);
* the characteristic-zero dyadic descent on small 2-power domains;
* finite-field toy rows with p above the norm threshold.
"""

from __future__ import annotations

from itertools import combinations
import json
import math
import os
import sys
from typing import Any


HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
CERT = os.path.join(
    REPO,
    "experimental",
    "data",
    "certificates",
    "w-c-large-characteristic-lift",
    "w_c_large_characteristic_lift.json",
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


def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def phi_power_two(n: int) -> int:
    if not is_power_of_two(n):
        raise ValueError("this verifier only handles n=2^s")
    return n // 2


def first_power_two_gt(t: int) -> int:
    return 1 << t.bit_length()


def norm_threshold(n: int, b: int, t: int) -> int:
    upto = min(t, b)
    if upto <= 0:
        return 1
    phi = phi_power_two(n)
    return max(math.comb(b, r) ** phi for r in range(1, upto + 1))


def mask_from_tuple(items: tuple[int, ...]) -> int:
    out = 0
    for i in items:
        out |= 1 << i
    return out


def exponents(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def is_union_mu_m_cosets(mask: int, n: int, m: int) -> bool:
    if n % m:
        return False
    step = n // m
    for r in range(step):
        coset = 0
        for j in range(m):
            coset |= 1 << (r + j * step)
        hit = mask & coset
        if hit and hit != coset:
            return False
    return True


def cyclotomic_zero_from_counts(counts: list[int], n: int) -> bool:
    half = n // 2
    return all(counts[i] == counts[i + half] for i in range(half))


def char0_elementary_zero(mask: int, n: int, t: int) -> bool:
    selected = exponents(mask, n)
    reps = [[0] * n for _ in range(t + 1)]
    reps[0][0] = 1
    max_r = 0
    for exponent in selected:
        max_r = min(t, max_r + 1)
        for r in range(max_r, 0, -1):
            source = reps[r - 1]
            target = reps[r]
            for idx, value in enumerate(source):
                if value:
                    target[(idx + exponent) % n] += value
    return all(cyclotomic_zero_from_counts(reps[r], n) for r in range(1, min(t, len(selected)) + 1))


def char0_descent_row(n: int, t: int) -> dict[str, Any]:
    m = first_power_two_gt(t)
    zero_masks = 0
    bad: list[list[int]] = []
    nondivisible_zero = 0
    for mask in range(1 << n):
        if not char0_elementary_zero(mask, n, t):
            continue
        zero_masks += 1
        if mask.bit_count() % m:
            nondivisible_zero += 1
        if not is_union_mu_m_cosets(mask, n, m):
            bad.append(exponents(mask, n))
            if len(bad) >= 5:
                break

    expected = 2 ** (n // m) if n % m == 0 else 0
    check(
        f"char0 n={n}, t={t}: zero sets are exactly mu_{m}-coset unions",
        not bad and zero_masks == expected,
        f"zero_masks={zero_masks}, expected={expected}",
    )
    check(
        f"char0 n={n}, t={t}: no zero set violates M | b",
        nondivisible_zero == 0,
        f"nondivisible_zero={nondivisible_zero}",
    )
    return {
        "n": n,
        "t": t,
        "M": m,
        "zero_masks": zero_masks,
        "expected_coset_unions": expected,
        "nondivisible_zero": nondivisible_zero,
        "bad_examples": bad,
    }


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


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def next_prime_congruent(lower: int, modulus: int, residue: int = 1) -> int:
    candidate = lower + ((residue - lower) % modulus)
    if candidate <= lower:
        candidate += modulus
    while not is_prime(candidate):
        candidate += modulus
    return candidate


def primitive_root(p: int) -> int:
    factors = factor_distinct(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // r, p) != 1 for r in factors):
            return g
    raise RuntimeError(f"no primitive root mod {p}")


def mu_domain(p: int, n: int) -> list[int]:
    if (p - 1) % n:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    zeta = pow(primitive_root(p), (p - 1) // n, p)
    values = [pow(zeta, i, p) for i in range(n)]
    if len(set(values)) != n:
        raise RuntimeError(f"bad mu_{n} generator in F_{p}")
    return values


def finite_elementary_zero(mask: int, domain: list[int], t: int, p: int) -> bool:
    e = [0] * (t + 1)
    e[0] = 1
    for i, x in enumerate(domain):
        if not ((mask >> i) & 1):
            continue
        for r in range(t, 0, -1):
            e[r] = (e[r] + x * e[r - 1]) % p
    return all(e[r] == 0 for r in range(1, t + 1))


def finite_lift_row(n: int, b: int, t: int) -> dict[str, Any]:
    threshold = norm_threshold(n, b, t)
    p = next_prime_congruent(threshold, n, 1)
    domain = mu_domain(p, n)
    m = first_power_two_gt(t)
    zero_subsets = 0
    bad: list[list[int]] = []
    for comb in combinations(range(n), b):
        mask = mask_from_tuple(comb)
        if not finite_elementary_zero(mask, domain, t, p):
            continue
        zero_subsets += 1
        if not is_union_mu_m_cosets(mask, n, m):
            bad.append(list(comb))
            if len(bad) >= 5:
                break

    expected = math.comb(n // m, b // m) if b % m == 0 and n % m == 0 else 0
    check(
        f"finite n={n}, b={b}, t={t}: p exceeds norm threshold",
        p > threshold and (p - 1) % n == 0,
        f"p={p}, threshold={threshold}",
    )
    check(
        f"finite n={n}, b={b}, t={t}: t-null subsets are mu_{m}-coset unions",
        not bad and zero_subsets == expected,
        f"zero_subsets={zero_subsets}, expected={expected}",
    )
    return {
        "n": n,
        "b": b,
        "t": t,
        "M": m,
        "phi_n": phi_power_two(n),
        "threshold": threshold,
        "prime": p,
        "zero_subsets": zero_subsets,
        "expected_coset_unions_of_size_b": expected,
        "bad_examples": bad,
    }


def build_certificate() -> dict[str, Any]:
    threshold_rows = []
    for n, b, t in [(8, 4, 1), (8, 4, 3), (16, 4, 3), (16, 5, 3)]:
        m = first_power_two_gt(t)
        threshold = norm_threshold(n, b, t)
        check(
            f"threshold n={n}, b={b}, t={t}: M is first power of two above t",
            m > t and (m // 2) <= t,
            f"M={m}",
        )
        threshold_rows.append(
            {
                "n": n,
                "b": b,
                "t": t,
                "M": m,
                "phi_n": phi_power_two(n),
                "threshold": threshold,
                "M_divides_b": b % m == 0,
            }
        )

    char0_rows = [
        char0_descent_row(8, 1),
        char0_descent_row(16, 3),
        char0_descent_row(16, 4),
    ]
    finite_rows = [
        finite_lift_row(8, 4, 1),
        finite_lift_row(8, 4, 3),
        finite_lift_row(16, 4, 3),
        finite_lift_row(16, 5, 3),
    ]
    check("all characteristic-zero rows have no bad examples", all(not row["bad_examples"] for row in char0_rows))
    check("all finite rows have no bad examples", all(not row["bad_examples"] for row in finite_rows))

    return {
        "task": "W-C large-characteristic lift and dyadic descent",
        "node": "u2_large_characteristic_lift",
        "status": "PROVED",
        "claim": (
            "Above p > max_r binom(b,r)^phi(n), finite t-null b-subsets of "
            "mu_n lift to characteristic zero and are unions of mu_M-cosets, "
            "M=2^ceil(log2(t+1))."
        ),
        "threshold_rows": threshold_rows,
        "char0_descent_rows": char0_rows,
        "finite_lift_rows": finite_rows,
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

    print("\nfinite row summary:")
    for row in cert["finite_lift_rows"]:
        print(
            f"n={row['n']} b={row['b']} t={row['t']} M={row['M']} "
            f"p={row['prime']} zero={row['zero_subsets']}"
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
