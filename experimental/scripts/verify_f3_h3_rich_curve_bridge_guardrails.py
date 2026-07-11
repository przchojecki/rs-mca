#!/usr/bin/env python3
"""Replay local h=3 rich-curve bridge guardrails."""

from __future__ import annotations

import random
from collections import defaultdict
from itertools import combinations, permutations


def prime_factors(n: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def primitive_root(p: int) -> int:
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // r, p) != 1 for r in factors):
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


def primitive_cube_root(p: int) -> int:
    if (p - 1) % 3:
        raise ValueError(p)
    for cand in range(2, p):
        root = pow(cand, (p - 1) // 3, p)
        if root != 1 and (root * root + root + 1) % p == 0:
            return root
    raise AssertionError(("no primitive cube root", p))


def verify_hyperbola_identity() -> int:
    rng = random.Random(20260711)
    checked = 0
    for p in (7, 13, 19, 31, 37, 43, 61, 73, 97, 109):
        omega = primitive_cube_root(p)
        omega2 = omega * omega % p
        det = (omega2 - omega) % p
        alpha = (1 + omega2) * pow(det, -1, p) % p
        beta = (1 - alpha) % p
        for _ in range(200):
            u = rng.randrange(p)
            v = rng.randrange(p)
            a = rng.randrange(p)
            b = rng.randrange(p)
            A = (u - omega * v) % p
            B = (u - omega2 * v) % p
            if (alpha * A + beta * B - (u + v)) % p:
                raise AssertionError(("linear inverse", p, u, v))
            if (A * B - (u * u + u * v + v * v)) % p:
                raise AssertionError(("quadratic factor", p, u, v))
            X = (A + a * beta) % p
            Y = (B + a * alpha) % p
            delta = (a * a % p * alpha % p * beta - b) % p
            G = (u * u + u * v + v * v + a * (u + v) + b) % p
            if (X * Y - delta - G) % p:
                raise AssertionError(("XY-Delta", p, u, v, a, b))
            checked += 1
    return checked


def inv(x: int, p: int) -> int:
    return pow(x % p, -1, p)


def g_value(u: int, v: int, a: int, b: int, p: int) -> int:
    return (u * u + u * v + v * v + a * (u + v) + b) % p


def f0_value(x: int, a: int, b: int, p: int) -> int:
    return (x * x * x + a * x * x + b * x) % p


def e2_value(u: int, v: int, w: int, p: int) -> int:
    return (u * v + u * w + v * w) % p


def case_b(p: int, a: int, u0: int, v0: int) -> int:
    return (-(u0 * u0 + u0 * v0 + v0 * v0 + a * (u0 + v0))) % p


def q_value(t: int, p: int) -> int:
    return (t * t + t + 1) % p


def chart_point(
    p: int, a: int, b: int, u0: int, v0: int, t: int
) -> tuple[int, int, int] | None:
    del b
    q = q_value(t, p)
    if q == 0:
        return None
    a0 = (2 * u0 + v0 + a) % p
    b0 = (u0 + 2 * v0 + a) % p
    s = (-(a0 + b0 * t) * inv(q, p)) % p
    u = (u0 + s) % p
    v = (v0 + t * s) % p
    w = (-a - u - v) % p
    return u, v, w


def infinity_point(p: int, a: int, u0: int, v0: int) -> tuple[int, int]:
    return u0 % p, (-a - u0 - v0) % p


def numerator_coefficients(
    p: int, a: int, u0: int, v0: int
) -> dict[str, tuple[int, int, int]]:
    a0 = (2 * u0 + v0 + a) % p
    b0 = (u0 + 2 * v0 + a) % p
    u_num = ((u0 - a0) % p, (u0 - b0) % p, u0 % p)
    v_num = (v0 % p, (v0 - a0) % p, (v0 - b0) % p)
    w_num = tuple(((-a) - u_num[i] - v_num[i]) % p for i in range(3))
    return {"U": u_num, "V": v_num, "W": w_num}


def eval_quad(coeffs: tuple[int, int, int], t: int, p: int) -> int:
    return (coeffs[0] + coeffs[1] * t + coeffs[2] * t * t) % p


def verify_chart_identities(p: int, a: int, u0: int, v0: int) -> dict[str, int]:
    b = case_b(p, a, u0, v0)
    if (a * a - 3 * b) % p == 0:
        raise AssertionError(("degenerate case selected", p, a, b, u0, v0))
    if g_value(u0, v0, a, b, p) != 0:
        raise AssertionError(("base point not on conic", p, a, b, u0, v0))

    coeffs = numerator_coefficients(p, a, u0, v0)
    checked = 0
    skipped_poles = 0
    for t in range(p):
        point = chart_point(p, a, b, u0, v0, t)
        if point is None:
            skipped_poles += 1
            continue
        u, v, w = point
        q = q_value(t, p)
        for name, value in (("U", u), ("V", v), ("W", w)):
            if (eval_quad(coeffs[name], t, p) * inv(q, p)) % p != value:
                raise AssertionError((name, "numerator mismatch", p, t))
        if g_value(u, v, a, b, p) != 0:
            raise AssertionError(("chart left conic", p, t, u, v))
        if (u + v + w + a) % p != 0:
            raise AssertionError(("bad e1", p, t, u, v, w))
        if e2_value(u, v, w, p) != b:
            raise AssertionError(("bad e2", p, t, u, v, w, b))
        f = f0_value(u, a, b, p)
        if f0_value(v, a, b, p) != f or f0_value(w, a, b, p) != f:
            raise AssertionError(("not same fiber", p, t, u, v, w))
        checked += 1

    u_inf, v_inf = infinity_point(p, a, u0, v0)
    if g_value(u_inf, v_inf, a, b, p) != 0:
        raise AssertionError(("infinity mate not on conic", p, u_inf, v_inf))
    return {"b": b, "checked_t": checked, "skipped_poles": skipped_poles}


def verify_coverage(p: int, a: int, u0: int, v0: int) -> dict[str, int]:
    b = case_b(p, a, u0, v0)
    conic_points = {
        (u, v)
        for u in range(p)
        for v in range(p)
        if g_value(u, v, a, b, p) == 0
    }
    image_points: set[tuple[int, int]] = set()
    for t in range(p):
        point = chart_point(p, a, b, u0, v0, t)
        if point is not None:
            image_points.add(point[:2])
    image_points.add(infinity_point(p, a, u0, v0))
    if image_points != conic_points:
        raise AssertionError(("coverage mismatch", p))
    return {"conic_points": len(conic_points), "image_points": len(image_points)}


def elementary_key(values: tuple[int, int, int], p: int) -> tuple[int, int]:
    x, y, z = values
    return (x + y + z) % p, (x * y + x * z + y * z) % p


def ordered_fibers(p: int, n: int) -> dict[tuple[int, int], set[tuple[int, int, int]]]:
    vals = subgroup(p, n)
    fibers: dict[tuple[int, int], set[tuple[int, int, int]]] = defaultdict(set)
    for exps in combinations(range(n), 3):
        values = tuple(vals[e] for e in exps)
        key = elementary_key(values, p)
        for ordered in permutations(values, 3):
            fibers[key].add(ordered)
    return fibers


def chart_count_for_fiber(
    p: int, hset: set[int], key: tuple[int, int], ordered: set[tuple[int, int, int]]
) -> tuple[int, int, int]:
    s1, s2 = key
    a = (-s1) % p
    b = s2
    if (a * a - 3 * b) % p == 0:
        return 0, 0, 1

    u0, v0, _ = min(ordered)
    chart = set()
    for t in range(p):
        point = chart_point(p, a, b, u0, v0, t)
        if point is not None and len(set(point)) == 3 and all(x in hset for x in point):
            chart.add(point)

    vertical = (*infinity_point(p, a, u0, v0), v0 % p)
    epsilon = int(
        len(set(vertical)) == 3
        and all(x in hset for x in vertical)
        and vertical not in chart
    )
    if len(ordered) != len(chart) + epsilon:
        raise AssertionError((p, key, len(ordered), len(chart), epsilon))
    return len(chart), epsilon, 0


def verify_pair_compiler(p: int, n: int, max_fibers: int = 32) -> dict[str, int]:
    hset = set(subgroup(p, n))
    fibers = ordered_fibers(p, n)
    selected = sorted(
        ((len(ordered), key, ordered) for key, ordered in fibers.items()),
        reverse=True,
    )[:max_fibers]

    t_values: list[int] = []
    r_values: list[int] = []
    pair_total = 0
    skipped_degenerate = 0

    for _, key, ordered in selected:
        t_count, epsilon, skipped = chart_count_for_fiber(p, hset, key, ordered)
        skipped_degenerate += skipped
        if skipped:
            continue
        r_count = t_count + epsilon
        if r_count != len(ordered) or r_count % 6:
            raise AssertionError((p, n, key, t_count, epsilon, len(ordered)))
        n_triples = r_count // 6
        local_pairs = n_triples * (n_triples - 1) // 2
        formula_pairs = r_count * (r_count - 6) // 72
        if local_pairs != formula_pairs:
            raise AssertionError((p, n, key, local_pairs, formula_pairs))
        t_values.append(t_count)
        r_values.append(r_count)
        pair_total += local_pairs

    if not t_values:
        raise AssertionError((p, n, "no nondegenerate selected fibers"))

    z = len(t_values)
    total_t = sum(t_values)
    total_r = sum(r_values)
    max_t = max(t_values)
    max_r = max(r_values)
    exact_numer = max_r * total_r
    chart_numer = (max_t + 1) * (total_t + z)
    if 72 * pair_total > exact_numer or 72 * pair_total > chart_numer:
        raise AssertionError((p, n, pair_total, exact_numer, chart_numer))

    return {
        "fibers": z,
        "total_t": total_t,
        "max_t": max_t,
        "pairs": pair_total,
        "chart_bound": (chart_numer + 71) // 72,
        "skipped_degenerate": skipped_degenerate,
    }


def main() -> None:
    hyperbola_checks = verify_hyperbola_identity()
    print(f"hyperbola identity finite checks={hyperbola_checks}")

    print("conic degree-2 chart checks")
    for p, a, u0, v0 in (
        (17, 4, 2, 5),
        (97, 11, 7, 19),
        (193, 23, 41, 72),
        (769, 37, 101, 333),
    ):
        row = verify_chart_identities(p, a, u0, v0)
        coverage = verify_coverage(p, a, u0, v0) if p <= 193 else None
        coverage_text = ""
        if coverage is not None:
            coverage_text = f" conic_points={coverage['conic_points']}"
        print(
            f"p={p} a={a} b={row['b']} checked_t={row['checked_t']} "
            f"skipped_poles={row['skipped_poles']}{coverage_text}"
        )

    print("pair-count compiler checks")
    for p, n in ((97, 16), (97, 32), (193, 64)):
        row = verify_pair_compiler(p, n)
        print(
            f"p={p} n={n} fibers={row['fibers']} total_T={row['total_t']} "
            f"max_T={row['max_t']} pairs={row['pairs']} "
            f"chart_bound={row['chart_bound']} skipped={row['skipped_degenerate']}"
        )

    print("F3_H3_RICH_CURVE_BRIDGE_GUARDRAILS_PASS")


if __name__ == "__main__":
    main()
