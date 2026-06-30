#!/usr/bin/env python3
"""Verify the M1 two-root line-packet closure identities.

This is a focused checker for
experimental/notes/m1/m1_two_root_line_packet_closure.md.  It checks local
finite-field algebra for fixed-sum and product-Mobius line packets.  It does
not scan MCA bad slopes and does not prove the global M1 local limit.
"""

from __future__ import annotations

from itertools import product
from random import Random


PRIMES = (3, 5, 7, 11, 17)


def value_on_line(
    rows: tuple[int, int, int, int], s_value: int, p_value: int, prime: int
) -> tuple[int, int]:
    d0, d1, d2, d3 = rows
    return (
        (d2 - s_value * d1 + p_value * d0) % prime,
        (d3 - s_value * d2 + p_value * d1) % prime,
    )


def check_two_root_line_classification() -> int:
    checked = 0
    for p in PRIMES:
        pairs = [(x, y) for x in range(p) for y in range(x + 1, p)]
        domain = tuple(range(1, (p + 1) // 2))
        domain_set = set(domain)
        for a in range(p):
            for b in range(p):
                if a == 0 and b == 0:
                    continue
                for c0 in range(p):
                    if b == 0:
                        s0 = (-c0 * pow(a, -1, p)) % p
                        for x, y in pairs:
                            in_line = (
                                a * ((x + y) % p) + b * ((x * y) % p) + c0
                            ) % p == 0
                            in_model = (x + y) % p == s0
                            assert in_line == in_model, (p, a, b, c0, x, y)

                        mixed_direct = [
                            (beta_ext, y)
                            for y in domain
                            for beta_ext in range(p)
                            if beta_ext not in domain_set
                            and (
                                a * ((beta_ext + y) % p)
                                + b * ((beta_ext * y) % p)
                                + c0
                            )
                            % p
                            == 0
                        ]
                        mixed_formula = [
                            ((s0 - y) % p, y)
                            for y in domain
                            if (s0 - y) % p not in domain_set
                        ]
                        assert sorted(mixed_direct) == sorted(mixed_formula), (
                            p,
                            a,
                            b,
                            c0,
                            mixed_direct,
                            mixed_formula,
                        )
                        assert len(mixed_direct) <= len(domain)
                        checked += 1
                        continue

                    center = (-a * pow(b, -1, p)) % p
                    beta = (-c0 * pow(b, -1, p)) % p
                    mu = (center * center + beta) % p

                    for x, y in pairs:
                        in_line = (
                            a * ((x + y) % p) + b * ((x * y) % p) + c0
                        ) % p == 0
                        if mu == 0:
                            in_model = x == center or y == center
                        else:
                            in_model = ((x - center) * (y - center)) % p == mu
                        assert in_line == in_model, (
                            p,
                            a,
                            b,
                            c0,
                            center,
                            mu,
                            x,
                            y,
                            in_line,
                            in_model,
                        )
                        if in_line and mu != 0:
                            assert x != center and y != center
                            assert (
                                center + mu * pow((x - center) % p, -1, p)
                            ) % p == y
                            assert (
                                center + mu * pow((y - center) % p, -1, p)
                            ) % p == x

                    mixed_direct = [
                        (beta_ext, y)
                        for y in domain
                        for beta_ext in range(p)
                        if beta_ext not in domain_set
                        and (
                            a * ((beta_ext + y) % p)
                            + b * ((beta_ext * y) % p)
                            + c0
                        )
                        % p
                        == 0
                    ]
                    if mu == 0:
                        assert all(
                            beta_ext == center or y == center
                            for beta_ext, y in mixed_direct
                        ), (p, a, b, c0, center, mu, mixed_direct)
                    else:
                        mixed_formula = [
                            (
                                (
                                    center
                                    + mu * pow((y - center) % p, -1, p)
                                )
                                % p,
                                y,
                            )
                            for y in domain
                            if y != center
                            and (
                                center + mu * pow((y - center) % p, -1, p)
                            )
                            % p
                            not in domain_set
                        ]
                        assert sorted(mixed_direct) == sorted(mixed_formula), (
                            p,
                            a,
                            b,
                            c0,
                            center,
                            mu,
                            mixed_direct,
                            mixed_formula,
                        )
                        assert len(mixed_direct) <= len(domain)
                    checked += 1
    return checked


def check_constant_slope_collapse() -> int:
    checked = 0
    for p in (5, 7, 11):
        for rows in product(range(p), repeat=4):
            for fixed_sum in range(p):
                zeros = [
                    p_value
                    for p_value in range(p)
                    if value_on_line(rows, fixed_sum, p_value, p) == (0, 0)
                ]
                if len(zeros) >= 2:
                    assert rows == (0, 0, 0, 0), (p, rows, fixed_sum, zeros)
                checked += 1

            for center in range(p):
                for mu in range(1, p):
                    zeros = [
                        s_value
                        for s_value in range(p)
                        if value_on_line(
                            rows,
                            s_value,
                            (center * s_value - center * center + mu) % p,
                            p,
                        )
                        == (0, 0)
                    ]
                    if len(zeros) >= 2:
                        assert rows == (0, 0, 0, 0), (
                            p,
                            rows,
                            center,
                            mu,
                            zeros,
                        )
                    checked += 1
    return checked


def check_sampled_injectivity() -> int:
    checked = 0
    rng = Random(20260630)
    for p in (17, 31, 43):
        for _ in range(2000):
            rows = tuple(rng.randrange(p) for _ in range(4))
            if rows == (0, 0, 0, 0):
                continue

            fixed_sum = rng.randrange(p)
            roots = [
                p_value
                for p_value in range(p)
                if value_on_line(rows, fixed_sum, p_value, p) == (0, 0)
            ]
            assert len(roots) <= 1, (p, rows, fixed_sum, roots)

            center = rng.randrange(p)
            mu = 1 + rng.randrange(p - 1)
            roots = [
                s_value
                for s_value in range(p)
                if value_on_line(
                    rows,
                    s_value,
                    (center * s_value - center * center + mu) % p,
                    p,
                )
                == (0, 0)
            ]
            assert len(roots) <= 1, (p, rows, center, mu, roots)
            checked += 1
    return checked


def main() -> None:
    classification_checks = check_two_root_line_classification()
    collapse_checks = check_constant_slope_collapse()
    injectivity_checks = check_sampled_injectivity()

    print("M1 two-root line-packet closure verifier passed")
    print(f"  line classification/mixed-trace checks: {classification_checks}")
    print(f"  constant-slope collapse checks: {collapse_checks}")
    print(f"  sampled injectivity checks: {injectivity_checks}")


if __name__ == "__main__":
    main()
