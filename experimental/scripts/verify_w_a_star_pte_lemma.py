#!/usr/bin/env python3
"""Verifier for W-A: the star-PTE canonical-trade normal form.

The proof is the elementary-symmetric convolution identity.  This verifier
replays that normal form on small multiplicative rows: it enumerates locator
supports with equal top coefficients, removes the pairwise common core, and
checks that the residual supports form a PTE trade through the same level.

Run:
  python3 experimental/scripts/verify_w_a_star_pte_lemma.py
Refresh certificate:
  python3 experimental/scripts/verify_w_a_star_pte_lemma.py --write-certificate
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
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
    "w-a-star-pte-lemma",
    "w_a_star_pte_lemma.json",
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


@dataclass(frozen=True)
class RowSpec:
    name: str
    p: int
    n: int
    A: int
    t: int


ROWS = (
    RowSpec("F17_mu8_A4_t3", 17, 8, 4, 3),
    RowSpec("F13_mu12_A5_t3", 13, 12, 5, 3),
    RowSpec("F17_mu16_A6_t3", 17, 16, 6, 3),
    RowSpec("F97_mu16_A8_t3", 97, 16, 8, 3),
)


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


def mask_from_tuple(items: tuple[int, ...]) -> int:
    out = 0
    for i in items:
        out |= 1 << i
    return out


def values_from_mask(mask: int, domain: list[int]) -> list[int]:
    return [domain[i] for i in range(len(domain)) if (mask >> i) & 1]


def elementary(values: list[int], t: int, p: int) -> list[int]:
    e = [0] * (t + 1)
    e[0] = 1
    for x in values:
        for r in range(t, 0, -1):
            e[r] = (e[r] + x * e[r - 1]) % p
    return e


def signature(mask: int, domain: list[int], t: int, p: int) -> tuple[int, ...]:
    return tuple(elementary(values_from_mask(mask, domain), t, p)[1:])


def convolution_difference(
    common: int,
    p_part: int,
    q_part: int,
    domain: list[int],
    t: int,
    p: int,
) -> list[int]:
    e_common = elementary(values_from_mask(common, domain), t, p)
    e_p = elementary(values_from_mask(p_part, domain), t, p)
    e_q = elementary(values_from_mask(q_part, domain), t, p)
    out = []
    for r in range(1, t + 1):
        total = 0
        for i in range(r + 1):
            total += e_common[i] * (e_p[r - i] - e_q[r - i])
        out.append(total % p)
    return out


def analyze_row(row: RowSpec) -> dict[str, Any]:
    domain = mu_domain(row.p, row.n)
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for comb in combinations(range(row.n), row.A):
        mask = mask_from_tuple(comb)
        groups[signature(mask, domain, row.t, row.p)].append(mask)

    same_top_pairs = 0
    residual_failures: list[dict[str, Any]] = []
    max_family = max((len(masks) for masks in groups.values()), default=0)
    max_trade_size = 0

    for masks in groups.values():
        if len(masks) < 2:
            continue
        for i, base in enumerate(masks):
            for target in masks[i + 1 :]:
                same_top_pairs += 1
                common = base & target
                q_part = base & ~common
                p_part = target & ~common
                max_trade_size = max(max_trade_size, p_part.bit_count())

                star_equal = (
                    signature(p_part, domain, row.t, row.p)
                    == signature(q_part, domain, row.t, row.p)
                )
                convolution_zero = all(
                    x == 0
                    for x in convolution_difference(common, p_part, q_part, domain, row.t, row.p)
                )
                if (
                    p_part & q_part
                    or p_part.bit_count() != q_part.bit_count()
                    or not star_equal
                    or not convolution_zero
                ):
                    residual_failures.append(
                        {
                            "base": [j for j in range(row.n) if (base >> j) & 1],
                            "target": [j for j in range(row.n) if (target >> j) & 1],
                            "p_size": p_part.bit_count(),
                            "q_size": q_part.bit_count(),
                            "star_equal": star_equal,
                            "convolution_zero": convolution_zero,
                        }
                    )
                    if len(residual_failures) >= 5:
                        break
            if len(residual_failures) >= 5:
                break
        if len(residual_failures) >= 5:
            break

    check(
        f"{row.name}: every same-top pair gives a canonical star-PTE trade",
        not residual_failures,
        f"same_top_pairs={same_top_pairs}, max_family={max_family}",
    )
    check(
        f"{row.name}: at least one nontrivial same-top pair was replayed",
        same_top_pairs > 0,
        f"same_top_pairs={same_top_pairs}",
    )
    return {
        "row": row.name,
        "p": row.p,
        "n": row.n,
        "A": row.A,
        "t": row.t,
        "support_count": sum(1 for _ in combinations(range(row.n), row.A)),
        "same_top_classes": sum(1 for masks in groups.values() if len(masks) > 1),
        "same_top_pairs": same_top_pairs,
        "max_same_top_family": max_family,
        "max_residual_trade_size": max_trade_size,
        "residual_failures": residual_failures,
    }


def build_certificate() -> dict[str, Any]:
    rows = [analyze_row(row) for row in ROWS]
    check("all toy rows have zero residual failures", all(not row["residual_failures"] for row in rows))
    check("toy replay exercised same-top pairs", sum(row["same_top_pairs"] for row in rows) > 0)
    return {
        "task": "W-A star-PTE canonical-trade normal form",
        "node": "u1_pte_trade_compression",
        "status": "PROVED",
        "claim": (
            "Same-top locator pairs decompose uniquely into a common core plus "
            "a residual PTE trade; conversely residual PTE trades preserve the "
            "top coefficients after adding a common core."
        ),
        "proof_identities": [
            "e_r(C union P)-e_r(C union Q)=sum_i e_i(C)(e_{r-i}(P)-e_{r-i}(Q))",
            "induction uses e_0(C)=1 to force e_r(P)=e_r(Q)",
        ],
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
        with open(CERT, encoding="utf-8") as fh:
            expected = json.load(fh)
    check("certificate exists", expected is not None, CERT)
    if expected is not None:
        check("certificate matches recomputed summary", cert == expected)

    print("\nrow summary:")
    for row in cert["rows"]:
        print(
            f"{row['row']}: pairs={row['same_top_pairs']} "
            f"classes={row['same_top_classes']} max_family={row['max_same_top_family']} "
            f"max_trade_size={row['max_residual_trade_size']}"
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
