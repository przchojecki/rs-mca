#!/usr/bin/env python3
"""
Exact dual co-support quotient ledger for the v10 milestone-3 formula.

For a divisor set C and agreement threshold a, this computes the co-support union

    T_C^{>=a} = { T subset D : |T| <= n-a and
                  exists c in C with Psi_c(T)=ceil(|T|/c) },

where Psi_c(T) is the number of c-fibers hit by T.  It is the dual form of the
milestone-2 support ledger and is typically more efficient near capacity because
it truncates in co-support size J=n-a.

This is a small reference implementation; it enumerates one lcm block of size h
and should be used only when h is modest.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from math import gcd, comb
from typing import Dict, Iterable, List, Tuple
import argparse

Profile = Tuple[int, ...]
Key = Tuple[int, Profile]


def lcm(a: int, b: int) -> int:
    return a // gcd(a, b) * b


def lcm_many(values: Iterable[int]) -> int:
    return reduce(lcm, values, 1)


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


def cosets_in_block(h: int, c: int) -> List[int]:
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


def dual_block_polynomial(divisors: List[int]) -> Dict[Key, int]:
    h = lcm_many(divisors)
    cosets = [cosets_in_block(h, c) for c in divisors]
    poly: Dict[Key, int] = defaultdict(int)
    for mask in range(1 << h):
        size = mask.bit_count()
        profile = tuple(sum(1 for cm in c_cosets if mask & cm) for c_cosets in cosets)
        poly[(size, profile)] += 1
    return dict(poly)


def multiply_truncated(left: Dict[Key, int], right: Dict[Key, int], max_j: int, caps: Profile) -> Dict[Key, int]:
    out: Dict[Key, int] = defaultdict(int)
    for (j1, p1), v1 in left.items():
        for (j2, p2), v2 in right.items():
            j = j1 + j2
            if j > max_j:
                continue
            p = tuple(x + y for x, y in zip(p1, p2))
            if any(x > cap for x, cap in zip(p, caps)):
                continue
            out[(j, p)] += v1 * v2
    return dict(out)


def power_polynomial(poly: Dict[Key, int], exponent: int, max_j: int, caps: Profile) -> Dict[Key, int]:
    zero = tuple(0 for _ in caps)
    result: Dict[Key, int] = {(0, zero): 1}
    base = dict(poly)
    e = exponent
    while e:
        if e & 1:
            result = multiply_truncated(result, base, max_j, caps)
        e >>= 1
        if e:
            base = multiply_truncated(base, base, max_j, caps)
    return result


@dataclass(frozen=True)
class DualLedgerResult:
    n: int
    divisors: Tuple[int, ...]
    threshold: int
    J: int
    h: int
    blocks: int
    exact_union: int
    single_divisor_safe_sum: int
    coefficient_states: int


def exact_dual_union(n: int, divisors: Iterable[int], threshold: int) -> DualLedgerResult:
    divisors = tuple(sorted(set(divisors)))
    if not divisors:
        raise ValueError("divisors must be nonempty")
    if any(n % c for c in divisors):
        raise ValueError("every divisor must divide n")
    if not (0 <= threshold <= n):
        raise ValueError("threshold must be in [0,n]")
    J = n - threshold
    h = lcm_many(divisors)
    blocks = n // h
    if h > 24:
        raise ValueError(f"h={h} is large for brute-force enumeration; use orbit compression")
    caps = tuple(n // c for c in divisors)
    block = dual_block_polynomial(list(divisors))
    coeffs = power_polynomial(block, blocks, J, caps)

    exact = 0
    for (j, profile), count in coeffs.items():
        if j > J:
            continue
        if any(profile[i] == ceil_div(j, c) for i, c in enumerate(divisors)):
            exact += count

    # The raw one-divisor safe sum, for comparison only.  This is equal to the
    # milestone-2 safe sum under A=n-j.
    safe = 0
    for c in divisors:
        for j in range(0, J + 1):
            r = ceil_div(j, c)
            safe += comb(n // c, r) * comb(c * r, j)

    return DualLedgerResult(
        n=n,
        divisors=divisors,
        threshold=threshold,
        J=J,
        h=h,
        blocks=blocks,
        exact_union=exact,
        single_divisor_safe_sum=safe,
        coefficient_states=len(coeffs),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True, help="domain size")
    parser.add_argument("--a", type=int, required=True, help="closed agreement threshold")
    parser.add_argument("--divisors", type=int, nargs="+", required=True, help="divisor set C")
    args = parser.parse_args()
    res = exact_dual_union(args.n, args.divisors, args.a)
    print(f"n={res.n}")
    print(f"divisors={list(res.divisors)}")
    print(f"threshold={res.threshold}")
    print(f"J=n-a={res.J}")
    print(f"h=lcm(C)={res.h}")
    print(f"blocks=n/h={res.blocks}")
    print(f"coefficient_states={res.coefficient_states}")
    print(f"exact_dual_union={res.exact_union}")
    print(f"single_divisor_safe_sum={res.single_divisor_safe_sum}")
    if res.single_divisor_safe_sum:
        print(f"exact/safe={res.exact_union/res.single_divisor_safe_sum:.12g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
