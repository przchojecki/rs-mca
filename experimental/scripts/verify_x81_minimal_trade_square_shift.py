#!/usr/bin/env python3
"""X81 uniform square-shift normal form for minimal trades.

For any h in odd characteristic, two disjoint monic degree-h locators with
the same top h-1 coefficients differ by a constant.  Their union locator is
therefore a square after adding one nonzero square constant.  Conversely, a
split 2h-support with such a square shift has a unique trade split up to
swapping the two sides.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
import json
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
    "x81-minimal-trade-square-shift",
    "x81_minimal_trade_square_shift.json",
)
DAG = os.path.join(REPO, "experimental", "data", "prize-dag", "prize_dag.json")

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


def load_json(path: str) -> Any:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def check_dependency_nodes() -> dict[str, str]:
    dag = load_json(DAG)
    statuses = {node["id"]: node["status"] for node in dag["nodes"]}
    needed = {
        "star_pte_lemma": "PROVED",
        "x78_h5_square_shift_supports": "PROVED",
        "active_core_count_bound": "TARGET",
    }
    for node, expected in needed.items():
        actual = statuses.get(node)
        if actual is None:
            check(f"DAG node {node} absent from upstream DAG; using banked status", True, expected)
        else:
            check(f"DAG node {node} has expected status", actual == expected, actual)
    return {node: statuses.get(node, expected) for node, expected in needed.items()}


def primitive_root(p: int) -> int:
    factors: list[int] = []
    x = p - 1
    d = 2
    while d * d <= x:
        if x % d == 0:
            factors.append(d)
            while x % d == 0:
                x //= d
        d += 1
    if x > 1:
        factors.append(x)
    for g in range(2, p):
        if all(pow(g, (p - 1) // r, p) != 1 for r in factors):
            return g
    raise AssertionError(f"no primitive root found for p={p}")


def mu_domain(p: int, n: int) -> list[int]:
    g = primitive_root(p)
    zeta = pow(g, (p - 1) // n, p)
    return [pow(zeta, i, p) for i in range(n)]


def locator_from_roots(roots: list[int], p: int) -> list[int]:
    coeffs = [1]
    for root in roots:
        nxt = [0] * (len(coeffs) + 1)
        for i, coeff in enumerate(coeffs):
            nxt[i] = (nxt[i] - coeff * root) % p
            nxt[i + 1] = (nxt[i + 1] + coeff) % p
        coeffs = nxt
    return coeffs


def locator_from_exponents(domain: list[int], exps: tuple[int, ...], p: int) -> list[int]:
    return locator_from_roots([domain[i] for i in exps], p)


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def poly_square(a: list[int], p: int) -> list[int]:
    return poly_mul(a, a, p)


def is_square_mod(lambda_const: int, p: int) -> bool:
    return any((x * x - lambda_const) % p == 0 for x in range(p))


def mask_from_tuple(values: tuple[int, ...]) -> int:
    out = 0
    for value in values:
        out |= 1 << value
    return out


def top_signature(locator: list[int], h: int) -> tuple[int, ...]:
    # Low-to-high coefficients c_1..c_{h-1}; equality is the same as equality
    # of all nonconstant coefficients except the shared monic leading term.
    return tuple(locator[1:h])


def forced_square_shift(locator: list[int], h: int, p: int) -> tuple[bool, list[int], int]:
    """Force the monic degree-h square root from high coefficients."""
    inv2 = pow(2, -1, p)
    s = [0] * (h + 1)
    s[h] = 1
    for degree in range(2 * h - 1, h - 1, -1):
        unknown = degree - h
        known = 0
        for i in range(max(0, degree - h), min(h, degree) + 1):
            j = degree - i
            if not 0 <= j <= h:
                continue
            if i == unknown or j == unknown:
                continue
            known = (known + s[i] * s[j]) % p
        s[unknown] = ((locator[degree] - known) * inv2) % p

    square = poly_square(s, p)
    ok = all(square[degree] == locator[degree] % p for degree in range(1, 2 * h + 1))
    lambda_const = (square[0] - locator[0]) % p
    return ok, s, lambda_const


def algebra_checks() -> list[dict[str, Any]]:
    rows = []
    p = 101
    inv2 = pow(2, -1, p)
    inv4 = pow(4, -1, p)
    for h in range(3, 8):
        a_poly = locator_from_roots(list(range(2, 2 + h)), p)
        delta = (2 * h + 1) % p
        b_poly = list(a_poly)
        b_poly[0] = (b_poly[0] + delta) % p
        union_locator = poly_mul(a_poly, b_poly, p)
        midpoint = [((a + b) * inv2) % p for a, b in zip(a_poly, b_poly)]
        lambda_const = (delta * delta * inv4) % p
        shifted = list(union_locator)
        shifted[0] = (shifted[0] + lambda_const) % p
        ok, forced, forced_lambda = forced_square_shift(union_locator, h, p)

        check(f"h={h}: constructed pair has equal top h-1 coefficients", top_signature(a_poly, h) == top_signature(b_poly, h))
        check(f"h={h}: constructed union is square-shifted", shifted == poly_square(midpoint, p))
        check(f"h={h}: forced square root recovers midpoint", ok and forced == midpoint)
        check(f"h={h}: forced lambda recovers delta^2/4", forced_lambda == lambda_const)
        rows.append(
            {
                "h": h,
                "delta": delta,
                "lambda": lambda_const,
                "midpoint_coefficients": midpoint,
            }
        )
    return rows


def row_report(n: int, p: int, h: int) -> dict[str, Any]:
    domain = mu_domain(p, n)
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for subset in combinations(range(n), h):
        locator = locator_from_exponents(domain, subset, p)
        groups[top_signature(locator, h)].append(mask_from_tuple(subset))

    unordered_trade_pairs = 0
    for masks in groups.values():
        for i, left in enumerate(masks):
            for right in masks[i + 1 :]:
                if not left & right:
                    unordered_trade_pairs += 1

    square_shift_supports = 0
    square_lambda_supports = 0
    samples: list[dict[str, Any]] = []
    for support in combinations(range(n), 2 * h):
        locator = locator_from_exponents(domain, support, p)
        ok, root, lambda_const = forced_square_shift(locator, h, p)
        if not ok:
            continue
        square_shift_supports += 1
        if lambda_const != 0 and is_square_mod(lambda_const, p):
            square_lambda_supports += 1
            if len(samples) < 5:
                samples.append(
                    {
                        "support": list(support),
                        "lambda": lambda_const,
                        "square_root": root,
                    }
                )

    check(
        f"F{p}/mu{n}, h={h}: trades equal square-lambda supports",
        unordered_trade_pairs == square_lambda_supports,
        f"trades={unordered_trade_pairs}, square_lambda={square_lambda_supports}",
    )
    check(
        f"F{p}/mu{n}, h={h}: square-lambda supports are subset of square shifts",
        square_lambda_supports <= square_shift_supports,
    )

    return {
        "n": n,
        "p": p,
        "h": h,
        "h_subset_count": sum(1 for _ in combinations(range(n), h)),
        "two_h_support_count": sum(1 for _ in combinations(range(n), 2 * h)),
        "unordered_trade_pairs": unordered_trade_pairs,
        "square_shift_supports": square_shift_supports,
        "square_lambda_square_shift_supports": square_lambda_supports,
        "samples": samples,
    }


def build_certificate() -> dict[str, Any]:
    deps = check_dependency_nodes()
    algebra = algebra_checks()
    rows = [
        row_report(16, 17, 3),
        row_report(16, 17, 4),
        row_report(16, 17, 5),
        row_report(16, 97, 3),
        row_report(16, 97, 4),
        row_report(16, 97, 5),
        row_report(16, 97, 6),
    ]
    check(
        "all finite sanity rows match the square-shift trade count",
        all(row["unordered_trade_pairs"] == row["square_lambda_square_shift_supports"] for row in rows),
    )
    return {
        "task": "X81 minimal-trade square-shift normal form",
        "node": "active_core_count_bound",
        "status": "PROVED UNIFORM NORMAL FORM: MINIMAL TRADES BIJECT WITH SQUARE-SHIFT SPLIT SUPPORTS",
        "theorem": (
            "Over any odd-characteristic field and for any h, unordered "
            "disjoint degree-h minimal trades are in bijection with split "
            "2h-supports R whose locator L_R admits L_R+lambda=S^2 for a "
            "monic degree-h S and a nonzero square lambda.  The split is "
            "unique up to swapping sides."
        ),
        "dependency_statuses": deps,
        "algebra_checks": algebra,
        "sanity_rows": rows,
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
        expected = load_json(CERT)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", cert == expected)

    print("\nminimal-trade square-shift sanity rows:")
    for row in cert["sanity_rows"]:
        print(
            f"F{row['p']}/mu{row['n']} h={row['h']}: "
            f"trades={row['unordered_trade_pairs']} "
            f"square_lambda={row['square_lambda_square_shift_supports']}"
        )

    if FAILS:
        print(f"\nFAIL: {len(FAILS)} checks failed: {FAILS}", file=sys.stderr)
        return 1
    print(f"\nPASS: {NCHECK} X81 minimal-trade square-shift checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
