#!/usr/bin/env python3
"""
Exact quotient support-union ledger for the divisor-block formula in the v10
milestone-2 insert.

This is a small reference scanner, not a high-performance implementation.  It
enumerates subsets of one lcm block of size h=lcm(C), builds the block-profile
polynomial, exponentiates it by dynamic programming over the n/h identical
blocks, and evaluates

    U_C^supp(a) = sum_{A>=a, nu} coeff(A,nu)
                  * 1[exists c in C: nu_c=floor(A/c)].

The script is intended for small/moderate lcm blocks h.  For large h, use the
same formula with orbit compression or a specialized polynomial engine.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from math import gcd
from typing import Dict, Iterable, List, Tuple
import argparse

Profile = Tuple[int, ...]
Key = Tuple[int, Profile]


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def lcm_many(values: Iterable[int]) -> int:
    return reduce(lcm, values, 1)


def cosets_in_block(h: int, c: int) -> List[int]:
    """Return bitmasks for the c-subfibers inside a block of size h."""
    if h % c != 0:
        raise ValueError(f"c={c} must divide h={h}")
    step = h // c
    cosets: List[int] = []
    for r in range(step):
        mask = 0
        for t in range(c):
            mask |= 1 << ((r + t * step) % h)
        cosets.append(mask)
    return cosets


def block_polynomial(divisors: List[int]) -> Dict[Key, int]:
    """Build G_{C,h} as a sparse dict (block_size, profile)->coefficient."""
    h = lcm_many(divisors)
    cosets = [cosets_in_block(h, c) for c in divisors]
    poly: Dict[Key, int] = defaultdict(int)
    for mask in range(1 << h):
        size = mask.bit_count()
        profile = tuple(sum(1 for cm in c_cosets if mask & cm == cm) for c_cosets in cosets)
        poly[(size, profile)] += 1
    return dict(poly)


def multiply_truncated(
    left: Dict[Key, int],
    right: Dict[Key, int],
    max_a: int,
    profile_caps: Profile,
) -> Dict[Key, int]:
    out: Dict[Key, int] = defaultdict(int)
    for (a1, p1), v1 in left.items():
        for (a2, p2), v2 in right.items():
            a = a1 + a2
            if a > max_a:
                continue
            p = tuple(x + y for x, y in zip(p1, p2))
            if any(x > cap for x, cap in zip(p, profile_caps)):
                continue
            out[(a, p)] += v1 * v2
    return dict(out)


def power_polynomial(poly: Dict[Key, int], exponent: int, max_a: int, profile_caps: Profile) -> Dict[Key, int]:
    """Exponentiate a sparse polynomial by repeated squaring with truncation."""
    zero_profile = tuple(0 for _ in profile_caps)
    result: Dict[Key, int] = {(0, zero_profile): 1}
    base = dict(poly)
    e = exponent
    while e:
        if e & 1:
            result = multiply_truncated(result, base, max_a, profile_caps)
        e >>= 1
        if e:
            base = multiply_truncated(base, base, max_a, profile_caps)
    return result


@dataclass(frozen=True)
class SupportLedgerResult:
    n: int
    divisors: Tuple[int, ...]
    threshold: int
    h: int
    blocks: int
    exact_union: int
    safe_sum: int
    coefficient_states: int


def exact_support_union(n: int, divisors: Iterable[int], threshold: int) -> SupportLedgerResult:
    divisors = tuple(sorted(set(divisors)))
    if not divisors:
        raise ValueError("divisors must be nonempty")
    if any(n % c for c in divisors):
        raise ValueError("every divisor must divide n")
    if not (0 <= threshold <= n):
        raise ValueError("threshold must be in [0,n]")
    h = lcm_many(divisors)
    blocks = n // h
    if h > 24:
        raise ValueError(
            f"h={h} is large for brute-force block enumeration; use orbit compression/specialization"
        )
    profile_caps = tuple(n // c for c in divisors)
    block = block_polynomial(list(divisors))
    coeffs = power_polynomial(block, blocks, n, profile_caps)

    exact = 0
    for (A, profile), count in coeffs.items():
        if A < threshold:
            continue
        if any(profile[i] == A // c for i, c in enumerate(divisors)):
            exact += count

    # Safe sum from the manuscript, computed directly.
    from math import comb
    safe = 0
    for c in divisors:
        for A in range(threshold, n + 1):
            m, s = divmod(A, c)
            safe += comb(n // c, m) * comb(n - c * m, s)

    return SupportLedgerResult(
        n=n,
        divisors=divisors,
        threshold=threshold,
        h=h,
        blocks=blocks,
        exact_union=exact,
        safe_sum=safe,
        coefficient_states=len(coeffs),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True, help="domain size")
    parser.add_argument("--a", type=int, required=True, help="closed agreement threshold")
    parser.add_argument("--divisors", type=int, nargs="+", required=True, help="divisor set C")
    args = parser.parse_args()
    res = exact_support_union(args.n, args.divisors, args.a)
    print(f"n={res.n}")
    print(f"divisors={list(res.divisors)}")
    print(f"threshold={res.threshold}")
    print(f"h=lcm(C)={res.h}")
    print(f"blocks=n/h={res.blocks}")
    print(f"coefficient_states={res.coefficient_states}")
    print(f"exact_U_supp={res.exact_union}")
    print(f"safe_sum={res.safe_sum}")
    if res.safe_sum:
        print(f"exact/safe={res.exact_union/res.safe_sum:.12g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
