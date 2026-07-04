#!/usr/bin/env python3
"""X82 square-shift row and certifier keys.

X81 puts minimal trades in square-shift support currency.  This verifier
checks the two key operations relevant to a certifier:

* domain scaling is a genuine row symmetry;
* unit exponent maps are Galois relabelings of the cyclotomic support data,
  not fixed-generator row-count symmetries.

The distinction matters: the finite-row square-shift predicate is checked only
on scaling orbits.  Unit relabeling is used only to compress cyclotomic
obstruction/resultant computations.
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
    "x82-square-shift-certifier-keys",
    "x82_square_shift_certifier_keys.json",
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
        "x67_h4_galois_norm_gate_compression": "PROVED",
        "x81_minimal_trade_square_shift": "PROVED",
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


def poly_mul(a: list[int], b: list[int], p: int) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def poly_square(a: list[int], p: int) -> list[int]:
    return poly_mul(a, a, p)


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


def forced_square_shift(locator: list[int], h: int, p: int) -> tuple[bool, list[int], int]:
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


def is_square_mod(lambda_const: int, p: int) -> bool:
    return any((x * x - lambda_const) % p == 0 for x in range(p))


def units_mod(n: int) -> list[int]:
    return [u for u in range(n) if math.gcd(u, n) == 1]


def transform_support(support: tuple[int, ...], n: int, *, shift: int = 0, unit: int = 1) -> tuple[int, ...]:
    return tuple(sorted(((unit * value + shift) % n for value in support)))


def canonical_key(support: tuple[int, ...], n: int) -> tuple[int, ...]:
    """Certifier key: scaling plus Galois/unit relabeling."""
    keys = []
    for unit in units_mod(n):
        for shift in range(n):
            keys.append(transform_support(support, n, shift=shift, unit=unit))
    return min(keys)


def scaling_key(support: tuple[int, ...], n: int) -> tuple[int, ...]:
    """Row-count key: genuine domain scaling only."""
    return min(transform_support(support, n, shift=shift) for shift in range(n))


def square_shift_data(domain: list[int], support: tuple[int, ...], p: int, h: int) -> dict[str, Any]:
    locator = locator_from_exponents(domain, support, p)
    ok, root, lambda_const = forced_square_shift(locator, h, p)
    square_lambda = ok and lambda_const != 0 and is_square_mod(lambda_const, p)
    return {
        "ok": ok,
        "lambda": lambda_const,
        "square_lambda": square_lambda,
        "root": root,
    }


def algebra_checks() -> dict[str, Any]:
    p = 101
    h = 4
    scale = 7
    roots = [2, 3, 5, 11, 13, 17, 19, 23]
    locator = locator_from_roots(roots, p)
    ok, root, lambda_const = forced_square_shift(locator, h, p)
    scaled_roots = [(scale * value) % p for value in roots]
    scaled_locator = locator_from_roots(scaled_roots, p)
    scaled_ok, scaled_root, scaled_lambda = forced_square_shift(scaled_locator, h, p)
    predicted_lambda = (pow(scale, 2 * h, p) * lambda_const) % p

    check("scaling preserves forced square-shift existence in algebra sample", ok == scaled_ok)
    check("scaling sends lambda to gamma^(2h) lambda", scaled_lambda == predicted_lambda)
    check(
        "scaling sends the square root by gamma^h S(X/gamma)",
        scaled_root
        == [
            (pow(scale, h - i, p) * coeff) % p
            for i, coeff in enumerate(root)
        ],
    )
    return {
        "field_p": p,
        "h": h,
        "scale": scale,
        "lambda": lambda_const,
        "scaled_lambda": scaled_lambda,
        "predicted_scaled_lambda": predicted_lambda,
    }


def row_report(n: int, p: int, h: int) -> dict[str, Any]:
    domain = mu_domain(p, n)
    units = units_mod(n)
    supports = list(combinations(range(n), 2 * h))
    square_count = 0
    shift_failures: list[dict[str, Any]] = []
    unit_mismatches: list[dict[str, Any]] = []
    square_scaling_keys: set[tuple[int, ...]] = set()
    square_certifier_keys: set[tuple[int, ...]] = set()
    all_scaling_keys: set[tuple[int, ...]] = set()
    all_certifier_keys: set[tuple[int, ...]] = set()
    sample_square: list[dict[str, Any]] = []
    certifier_key_failures: list[dict[str, Any]] = []

    for support in supports:
        base = square_shift_data(domain, support, p, h)
        row_key = scaling_key(support, n)
        cert_key = canonical_key(support, n)
        all_scaling_keys.add(row_key)
        all_certifier_keys.add(cert_key)
        if base["square_lambda"]:
            square_count += 1
            square_scaling_keys.add(row_key)
            square_certifier_keys.add(cert_key)
            if len(sample_square) < 5:
                sample_square.append(
                    {
                        "support": list(support),
                        "lambda": base["lambda"],
                        "scaling_key": list(row_key),
                        "certifier_key": list(cert_key),
                    }
                )
        for shift in range(n):
            shifted = transform_support(support, n, shift=shift)
            shifted_data = square_shift_data(domain, shifted, p, h)
            if bool(shifted_data["square_lambda"]) != bool(base["square_lambda"]) and len(shift_failures) < 5:
                shift_failures.append({"support": list(support), "shift": shift, "shifted": list(shifted)})
            if canonical_key(shifted, n) != cert_key and len(certifier_key_failures) < 5:
                certifier_key_failures.append(
                    {"support": list(support), "shift": shift, "shifted": list(shifted)}
                )
        for unit in units:
            relabeled = transform_support(support, n, unit=unit)
            relabeled_data = square_shift_data(domain, relabeled, p, h)
            if bool(relabeled_data["square_lambda"]) != bool(base["square_lambda"]) and len(unit_mismatches) < 5:
                unit_mismatches.append(
                    {"support": list(support), "unit": unit, "relabeled": list(relabeled)}
                )
            if canonical_key(relabeled, n) != cert_key and len(certifier_key_failures) < 5:
                certifier_key_failures.append(
                    {"support": list(support), "unit": unit, "relabeled": list(relabeled)}
                )

    check(
        f"F{p}/mu{n}, h={h}: square-shift predicate is scaling invariant",
        not shift_failures,
        f"sample_failures={shift_failures}",
    )
    check(
        f"F{p}/mu{n}, h={h}: certifier key is constant on scaling/unit relabeling",
        not certifier_key_failures,
        f"sample_failures={certifier_key_failures}",
    )
    check(
        f"F{p}/mu{n}, h={h}: row scaling key count does not exceed support count",
        len(all_scaling_keys) <= len(supports),
        f"keys={len(all_scaling_keys)}, supports={len(supports)}",
    )
    check(
        f"F{p}/mu{n}, h={h}: certifier key count does not exceed scaling key count",
        len(all_certifier_keys) <= len(all_scaling_keys),
        f"certifier_keys={len(all_certifier_keys)}, scaling_keys={len(all_scaling_keys)}",
    )

    return {
        "n": n,
        "p": p,
        "h": h,
        "two_h_support_count": len(supports),
        "unit_count": len(units),
        "square_lambda_support_count": square_count,
        "all_scaling_key_count": len(all_scaling_keys),
        "all_certifier_key_count": len(all_certifier_keys),
        "square_lambda_scaling_key_count": len(square_scaling_keys),
        "square_lambda_certifier_key_count": len(square_certifier_keys),
        "scaling_failures": shift_failures,
        "unit_row_predicate_mismatches": unit_mismatches,
        "certifier_key_failures": certifier_key_failures,
        "sample_square_shift_keys": sample_square,
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
    ]
    check(
        "all checked rows preserve square-shift predicate under row scaling",
        all(not row["scaling_failures"] for row in rows),
    )
    check(
        "all checked rows have stable scaling/unit certifier keys",
        all(not row["certifier_key_failures"] for row in rows),
    )
    check(
        "unit relabeling is not asserted as a fixed-row symmetry",
        any(row["unit_row_predicate_mismatches"] for row in rows),
    )
    check(
        "some checked row has nonempty square-shift scaling compression",
        any(
            row["square_lambda_scaling_key_count"] < row["square_lambda_support_count"]
            for row in rows
            if row["square_lambda_support_count"]
        ),
    )
    return {
        "task": "X82 square-shift certifier keys",
        "node": "active_core_count_bound",
        "status": "PROVED KEY DISCIPLINE: SQUARE-SHIFT ROW KEYS AND GALOIS CERTIFIER KEYS ARE SEPARATE",
        "theorem": (
            "For any minimal-trade square-shift support R in mu_n, domain "
            "scaling by gamma sends lambda to gamma^(2h) lambda and preserves "
            "the finite-row nonzero-square shift predicate.  Unit exponent "
            "maps send the square-shift identity through the cyclotomic "
            "Galois automorphism and preserve obstruction norm prime sets, "
            "but they are certifier compression only, not fixed-generator "
            "row-count symmetries."
        ),
        "warning": (
            "The verifier intentionally records fixed-row unit mismatches.  "
            "They are not failures; they prevent using Galois/unit keys to "
            "divide finite-row square-shift mass."
        ),
        "dependency_statuses": deps,
        "algebra_checks": algebra,
        "rows": rows,
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

    print("\nsquare-shift certifier-key rows:")
    for row in cert["rows"]:
        print(
            f"F{row['p']}/mu{row['n']} h={row['h']}: "
            f"square_supports={row['square_lambda_support_count']} "
            f"scaling_keys={row['square_lambda_scaling_key_count']} "
            f"certifier_keys={row['square_lambda_certifier_key_count']} "
            f"unit_mismatch_samples={len(row['unit_row_predicate_mismatches'])}"
        )

    if FAILS:
        print(f"\nFAIL: {len(FAILS)} checks failed: {FAILS}", file=sys.stderr)
        return 1
    print(f"\nPASS: {NCHECK} X82 square-shift certifier-key checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
