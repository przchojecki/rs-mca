#!/usr/bin/env python3
"""Replay checks for the F2 Newton empty-extremes lemma.

The proof is algebraic. This verifier checks the Newton identities and the
empty-edge conclusion on small prime-field root domains where exhaustive
enumeration of the edge band is cheap.
"""

from __future__ import annotations

from itertools import combinations


def prime_factors(n: int) -> set[int]:
    out: set[int] = set()
    d = 2
    while d * d <= n:
        while n % d == 0:
            out.add(d)
            n //= d
        d += 1
    if n > 1:
        out.add(n)
    return out


def primitive_root(q: int) -> int:
    factors = prime_factors(q - 1)
    for g in range(2, q):
        if all(pow(g, (q - 1) // r, q) != 1 for r in factors):
            return g
    raise ValueError(f"no primitive root found for {q}")


def root_domain(q: int, n: int) -> list[int]:
    assert (q - 1) % n == 0
    g = primitive_root(q)
    h = pow(g, (q - 1) // n, q)
    return sorted(pow(h, i, q) for i in range(n))


def elementary_coefficients(xs: tuple[int, ...], q: int) -> list[int]:
    # e[degree] for prod(1 + x T).
    e = [1] + [0] * len(xs)
    for x in xs:
        for k in range(len(xs), 0, -1):
            e[k] = (e[k] + x * e[k - 1]) % q
    return e


def power_sums(xs: tuple[int, ...], q: int, depth: int) -> list[int]:
    return [sum(pow(x, j, q) for x in xs) % q for j in range(1, depth + 1)]


def is_t_null(xs: tuple[int, ...], q: int, t: int) -> bool:
    for j in range(1, t + 1):
        if j % q == 0:
            continue
        if sum(pow(x, j, q) for x in xs) % q:
            return False
    return True


def check_newton(xs: tuple[int, ...], q: int) -> None:
    b = len(xs)
    e = elementary_coefficients(xs, q)
    pows = [0] + power_sums(xs, q, b)
    for k in range(1, b + 1):
        rhs = 0
        for i in range(1, k + 1):
            sign = 1 if i % 2 == 1 else -1
            rhs = (rhs + sign * e[k - i] * pows[i]) % q
        lhs = (k * e[k]) % q
        assert lhs == rhs, (q, xs, k, lhs, rhs)


def check_row(q: int, n: int, t: int) -> dict[str, int]:
    domain = root_domain(q, n)
    assert t < n
    for j in range(1, t + 1):
        assert sum(pow(x, j, q) for x in domain) % q == 0, (q, n, t, j)

    width = min(t, q - 1)
    checked = 0
    for b in range(1, width + 1):
        for subset in combinations(domain, b):
            checked += 1
            check_newton(subset, q)
            assert not is_t_null(subset, q, t), (q, n, t, subset)

            complement = tuple(x for x in domain if x not in subset)
            assert not is_t_null(complement, q, t), (q, n, t, "complement", subset)

    assert is_t_null(tuple(domain), q, t)
    return {"q": q, "n": n, "t": t, "width": width, "checked": checked}


def main() -> None:
    rows = [
        (17, 16, 2),
        (17, 16, 4),
        (97, 32, 2),
        (97, 32, 4),
        (193, 32, 3),
        (257, 16, 5),
    ]
    for q, n, t in rows:
        row = check_row(q, n, t)
        print(
            f"row q={q} n={n} t={t}: width={row['width']} "
            f"small_subsets_checked={row['checked']} proper_top_band_empty=True"
        )

    p_bits = 31
    n_bits = 41
    print(
        "official-shape sanity: if t >= p and t < N with "
        f"p~=2^{p_bits}, N~=2^{n_bits}, the Newton edge width is p-1, not t"
    )
    print("F2_NEWTON_EMPTY_EXTREMES_PASS")


if __name__ == "__main__":
    main()
