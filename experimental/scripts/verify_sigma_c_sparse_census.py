#!/usr/bin/env python3
"""Exact toy-row verifier for the sparse sigma_C MCA layer.

This is intentionally a small CPU certificate path. It brute-forces tiny
prime-field rows and checks the sparse mutual layer from `towards-prize.tex`
using the maximal witness set

    S_z = {i in D : eps1_i + gamma eps2_i = z_i}

for each close codeword z. Finite slopes only are counted. The verifier does
not quotient by projective/Mobius symmetries; future optimized searches should
only use slope-preserving upper-triangular reductions before returning to this
exact checker.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "sigma-c-sparse-census-v1"
DEFAULT_ROWS = (
    {"q": 5, "n": 4, "k": 2, "r": 1, "expected_sigma_c": 1},
    {"q": 7, "n": 6, "k": 3, "r": 1, "expected_sigma_c": 1},
    {"q": 5, "n": 4, "k": 2, "r": 2, "expected_sigma_c": None},
)


@dataclass(frozen=True)
class Row:
    q: int
    n: int
    k: int
    r: int
    expected_sigma_c: int | None = None


def render(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def inv(value: int, p: int) -> int:
    value %= p
    require(value != 0, "division by zero")
    return pow(value, p - 2, p)


def prime_factors(value: int) -> list[int]:
    out: list[int] = []
    d = 2
    while d * d <= value:
        if value % d == 0:
            out.append(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        out.append(value)
    return out


def primitive_root(p: int) -> int:
    require(p >= 3, "q must be an odd prime in this toy verifier")
    factors = prime_factors(p - 1)
    for g in range(2, p):
        if all(pow(g, (p - 1) // factor, p) != 1 for factor in factors):
            return g
    raise ValueError(f"no primitive root found for F_{p}")


def subgroup_domain(q: int, n: int) -> tuple[int, ...]:
    require((q - 1) % n == 0, "n must divide q-1")
    gen = primitive_root(q)
    step = pow(gen, (q - 1) // n, q)
    values: list[int] = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = (x * step) % q
    require(x == 1 and len(set(values)) == n, "domain generator has wrong order")
    return tuple(values)


def poly_eval(coeffs: tuple[int, ...], x: int, q: int) -> int:
    acc = 0
    power = 1
    for coeff in coeffs:
        acc = (acc + coeff * power) % q
        power = (power * x) % q
    return acc


def all_codewords(q: int, domain: tuple[int, ...], k: int) -> tuple[tuple[int, ...], ...]:
    words: list[tuple[int, ...]] = []
    for coeffs in itertools.product(range(q), repeat=k):
        words.append(tuple(poly_eval(coeffs, x, q) for x in domain))
    return tuple(words)


def support_restricts_to_code(
    eps2: tuple[int, ...],
    support: tuple[int, ...],
    codewords: tuple[tuple[int, ...], ...],
    k: int,
) -> bool:
    # Any assignment on at most k distinct RS domain points interpolates.
    if len(support) <= k:
        return True
    for codeword in codewords:
        if all(codeword[i] == eps2[i] for i in support):
            return True
    return False


def hamming_distance(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    return sum(x != y for x, y in zip(a, b, strict=True))


def enumerate_error_pairs(q: int, n: int, r: int) -> Iterable[tuple[tuple[int, ...], tuple[int, ...]]]:
    value_pairs = [(a, b) for a in range(q) for b in range(q) if a != 0 or b != 0]
    zero = (0,) * n
    yield zero, zero
    for size in range(1, r + 1):
        for support in itertools.combinations(range(n), size):
            for values in itertools.product(value_pairs, repeat=size):
                eps1 = [0] * n
                eps2 = [0] * n
                for index, (a, b) in zip(support, values, strict=True):
                    eps1[index] = a
                    eps2[index] = b
                yield tuple(eps1), tuple(eps2)


def bad_slope_witnesses(
    eps1: tuple[int, ...],
    eps2: tuple[int, ...],
    q: int,
    r: int,
    codewords: tuple[tuple[int, ...], ...],
    k: int,
) -> list[dict[str, Any]]:
    witnesses: list[dict[str, Any]] = []
    n = len(eps1)
    for gamma in range(q):
        word = tuple((eps1[i] + gamma * eps2[i]) % q for i in range(n))
        found: dict[str, Any] | None = None
        for codeword_index, codeword in enumerate(codewords):
            distance = hamming_distance(word, codeword)
            if distance > r:
                continue
            maximal_support = tuple(i for i, (wi, zi) in enumerate(zip(word, codeword, strict=True)) if wi == zi)
            if not support_restricts_to_code(eps2, maximal_support, codewords, k):
                found = {
                    "gamma": gamma,
                    "codeword_index": codeword_index,
                    "distance": distance,
                    "maximal_witness_set": list(maximal_support),
                    "agreement": len(maximal_support),
                }
                break
        if found is not None:
            witnesses.append(found)
    return witnesses


def sparse_union_size(eps1: tuple[int, ...], eps2: tuple[int, ...]) -> int:
    return sum(a != 0 or b != 0 for a, b in zip(eps1, eps2, strict=True))


def verify_row(row: Row) -> dict[str, Any]:
    q, n, k, r = row.q, row.n, row.k, row.r
    require(0 < k < n, "expected 0 < k < n")
    require(0 <= r <= n - k, "this census records the sparse layer r <= n-k")
    domain = subgroup_domain(q, n)
    codewords = all_codewords(q, domain, k)
    sigma_c = -1
    max_pairs: list[dict[str, Any]] = []
    pair_count = 0
    bad_pair_count = 0

    for eps1, eps2 in enumerate_error_pairs(q, n, r):
        pair_count += 1
        require(sparse_union_size(eps1, eps2) <= r, "enumerator emitted an oversized sparse pair")
        witnesses = bad_slope_witnesses(eps1, eps2, q, r, codewords, k)
        count = len(witnesses)
        if count:
            bad_pair_count += 1
        if count > sigma_c:
            sigma_c = count
            max_pairs = [
                {
                    "eps1": list(eps1),
                    "eps2": list(eps2),
                    "bad_slope_count": count,
                    "bad_slopes": witnesses,
                }
            ]
        elif count == sigma_c and count > 0 and len(max_pairs) < 3:
            max_pairs.append(
                {
                    "eps1": list(eps1),
                    "eps2": list(eps2),
                    "bad_slope_count": count,
                    "bad_slopes": witnesses,
                }
            )

    require(sigma_c >= 0, "sigma_c was not computed")
    if row.expected_sigma_c is not None:
        require(
            sigma_c == row.expected_sigma_c,
            f"expected sigma_C={row.expected_sigma_c} for {(q, n, k, r)}, got {sigma_c}",
        )
    if 2 * r <= n - k:
        require(sigma_c == r, f"trivial-regime check sigma_C=r failed for {(q, n, k, r)}")

    return {
        "q_line": q,
        "q_gen": q,
        "q_chal": None,
        "n": n,
        "k": k,
        "rho": f"{k}/{n}",
        "r": r,
        "delta_floor_convention": "r=floor(delta*n)",
        "domain": list(domain),
        "codeword_count": len(codewords),
        "sparse_pair_count": pair_count,
        "bad_pair_count": bad_pair_count,
        "sigma_c": sigma_c,
        "expected_sigma_c": row.expected_sigma_c,
        "trivial_regime_2r_le_n_minus_k": 2 * r <= n - k,
        "max_pairs_sample": max_pairs,
    }


def build_certificate(rows: Iterable[Row]) -> dict[str, Any]:
    checked_rows = [verify_row(row) for row in rows]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": "EXPERIMENTAL / PROVED-by-enumeration for the finite rows listed",
        "theorem_or_problem_id": "towards-prize prob:mutual; thm:sparsify sparse mutual layer",
        "object": "sigma_C(r)=max sparse-pair count of finite MCA-bad slopes",
        "conventions": {
            "finite_slopes_only": True,
            "slope_denominator": "q_line",
            "witness_set": "maximal S_z={i: eps1_i + gamma eps2_i equals close codeword z_i}",
            "symmetry_policy": "no symmetry quotient is used here; optimized searches must not use full Mobius reductions because they can send finite slopes to infinity",
            "field_ledger": "toy prime-field rows use q_gen=q_line; no q_chal soundness division is claimed",
        },
        "rows": checked_rows,
        "non_claims": [
            "No asymptotic bound is claimed.",
            "No prize-band deployed-row claim is made.",
            "No GPU search result is included in this certificate.",
        ],
    }


def rows_from_args(args: argparse.Namespace) -> list[Row]:
    if not args.row:
        return [Row(**row) for row in DEFAULT_ROWS]
    rows: list[Row] = []
    for spec in args.row:
        # PowerShell passes an unquoted comma-separated native argument as a
        # single whitespace-separated string, so accept both shell spellings.
        parts = [int(part) for part in spec.replace(",", " ").split()]
        require(len(parts) in {4, 5}, "--row expects q,n,k,r[,expected_sigma_c]")
        expected = parts[4] if len(parts) == 5 else None
        rows.append(Row(parts[0], parts[1], parts[2], parts[3], expected))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--row", action="append", help="row q,n,k,r[,expected_sigma_c]; may be repeated")
    parser.add_argument("--write", type=Path, help="write certificate JSON")
    parser.add_argument("--check", type=Path, help="check certificate JSON exactly")
    args = parser.parse_args()

    certificate = build_certificate(rows_from_args(args))
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(render(certificate), encoding="utf-8")
    if args.check:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        require(certificate == expected, f"sigma_C sparse census mismatch: {args.check}")

    print("sigma_C sparse census verifier")
    print("  object: sparse support-wise MCA bad-slope count")
    print("  theorem/problem: towards-prize prob:mutual / thm:sparsify")
    print("  status: EXPERIMENTAL; finite rows PROVED-by-enumeration")
    print("  conventions: finite slopes only; maximal S_z failure check; no Mobius quotient")
    for row in certificate["rows"]:
        print(
            "  row q={q_line} n={n} k={k} r={r}: sigma_C={sigma_c} "
            "pairs={sparse_pair_count} bad_pairs={bad_pair_count}".format(**row)
        )
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
