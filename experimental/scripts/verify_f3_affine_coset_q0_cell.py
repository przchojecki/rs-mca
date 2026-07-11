#!/usr/bin/env python3
"""Replay the F3 affine-coset q0-cell packet.

This script checks exact finite-row samples and all integer arithmetic used by
the note.  It does not prove the Stepanov h=2 input; that is the classical
input being imported by the packet.
"""

from __future__ import annotations


OFFICIAL_EXPONENTS = tuple(range(13, 42))
SAMPLE_ROWS = (
    (97, 16, 3, 5),
    (193, 32, 7, 11),
    (257, 64, 19, 23),
    (769, 128, 29, 31),
)


def ceil_cuberoot(value: int) -> int:
    lo = 0
    hi = 1
    while hi**3 < value:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**3 >= value:
            hi = mid
        else:
            lo = mid
    return hi


def factor_distinct(value: int) -> set[int]:
    factors: set[int] = set()
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.add(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        factors.add(value)
    return factors


def primitive_root(p: int) -> int:
    factors = factor_distinct(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // factor, p) != 1 for factor in factors):
            return g
    raise AssertionError(("no primitive root", p))


def subgroup(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n != 0:
        raise AssertionError((p, n, "n must divide p-1"))
    zeta = pow(primitive_root(p), (p - 1) // n, p)
    values: list[int] = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = x * zeta % p
    if x != 1 or len(set(values)) != n:
        raise AssertionError((p, n, "bad subgroup"))
    return tuple(values)


def h2_affine_bound(n: int) -> int:
    return ceil_cuberoot((66**3) * (n**2))


def q0_bound(n: int) -> int:
    return ceil_cuberoot((132**3) * (n**2))


def affine_pair_count(p: int, n: int, alpha: int, beta: int) -> int:
    if alpha % p == 0 or beta % p == 0:
        raise AssertionError((p, alpha, beta, "nonzero slope and offset required"))
    hset = set(subgroup(p, n))
    return sum(1 for y in hset if (alpha * y + beta) % p in hset)


def q0_roots(p: int) -> list[int]:
    return [r for r in range(p) if (r * r + r + 1) % p == 0]


def q0_cell_count(p: int, n: int) -> dict[str, int]:
    hset = set(subgroup(p, n))
    total = 0
    active_roots = 0
    for r in q0_roots(p):
        if r == p - 1:
            raise AssertionError((p, r, "r+1 should be nonzero"))
        c3 = (-r * pow(r + 1, -1, p)) % p
        if c3 != (r * r) % p:
            raise AssertionError((p, r, c3, "q0 identity failed"))

        local = 0
        for t in range(1, p):
            vals = (
                (1 + t) % p,
                (1 + r * t) % p,
                (1 + c3 * t) % p,
            )
            if all(v in hset for v in vals) and len(set(vals)) == 3:
                local += 1
        if local:
            active_roots += 1
        total += local

    return {
        "roots": len(q0_roots(p)),
        "active_roots": active_roots,
        "count": total,
        "bound": q0_bound(n),
    }


def verify_sample_rows() -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for p, n, alpha, beta in SAMPLE_ROWS:
        if not n**4 < p**3:
            raise AssertionError((p, n, "h2 hypothesis failed in sample"))

        affine_count = affine_pair_count(p, n, alpha, beta)
        affine_cap = h2_affine_bound(n)
        if affine_count > affine_cap:
            raise AssertionError((p, n, alpha, beta, affine_count, affine_cap))

        q0 = q0_cell_count(p, n)
        if q0["count"] > q0["bound"]:
            raise AssertionError((p, n, q0))

        rows.append(
            {
                "p": p,
                "n": n,
                "affine_count": affine_count,
                "affine_cap": affine_cap,
                "q0_roots": q0["roots"],
                "q0_count": q0["count"],
                "q0_cap": q0["bound"],
            }
        )
    return rows


def verify_official_rows() -> tuple[int, int, int]:
    first_lambda_improvement = 0
    last_lambda_cap = 0

    for exponent in OFFICIAL_EXPONENTS:
        n = 2**exponent

        # Official rows have p >= n^2, hence n^4 < p^3 for n > 1.
        if not n**4 < (n**2) ** 3:
            raise AssertionError((n, "official h2 hypothesis gate failed"))

        # q0 payment: 1584*n^(5/3) < n^3, cubed to avoid floats.
        if not 1584**3 < n**4:
            raise AssertionError((n, "q0 cubic floor failed"))

        lambda_cap = h2_affine_bound(n) // 3
        trivial_cap = (n - 1) // 3
        if first_lambda_improvement == 0 and lambda_cap < trivial_cap:
            first_lambda_improvement = exponent
        if exponent == OFFICIAL_EXPONENTS[-1]:
            last_lambda_cap = lambda_cap

    if first_lambda_improvement != 19:
        raise AssertionError(("unexpected lambda improvement row", first_lambda_improvement))
    if last_lambda_cap != 3_720_282_297:
        raise AssertionError(("unexpected final lambda cap", last_lambda_cap))

    return len(OFFICIAL_EXPONENTS), first_lambda_improvement, last_lambda_cap


def main() -> None:
    samples = verify_sample_rows()
    official_count, first_lambda, last_lambda = verify_official_rows()

    print("F3 affine-coset q0-cell replay")
    for row in samples:
        print(
            "sample "
            f"p={row['p']} n={row['n']} "
            f"affine={row['affine_count']}/{row['affine_cap']} "
            f"q0_roots={row['q0_roots']} q0={row['q0_count']}/{row['q0_cap']}"
        )
    print(f"last official lambda-one h2 cap={last_lambda}")
    print(
        "F3_AFFINE_COSET_Q0_CELL_PASS "
        f"official_rows={official_count} "
        f"sample_rows={len(samples)} "
        f"first_lambda_improvement=2^{first_lambda}"
    )


if __name__ == "__main__":
    main()
