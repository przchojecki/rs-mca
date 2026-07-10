#!/usr/bin/env python3
"""Replay the row-sharp Q full-ladder dictionary.

The proved lemma is the log-derivative identity:

    p_1(S)=...=p_t(S)=0
      iff
    c_i(S)=0 for every 1 <= i <= min(t, |S|) with char(F) not dividing i,

where prod_{x in S}(1 - xX) = 1 + c_1 X + ... + c_b X^b.

The script checks small subgroup-subset rows over prime fields and separate
formal-derivative rows that exercise the Frobenius-free indices q | i.  It is
an audit replay, not a replacement for the proof in the note.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CERT_DIR = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "rowsharp-q-full-ladder-dictionary"
)
CERT_PATH = CERT_DIR / "rowsharp_q_full_ladder_dictionary.json"


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


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
    raise AssertionError(f"no primitive root found for p={p}")


def multiplicative_subgroup(p: int, n: int) -> list[int]:
    ensure((p - 1) % n == 0, "n must divide p-1")
    g = primitive_root(p)
    h = pow(g, (p - 1) // n, p)
    return sorted({pow(h, i, p) for i in range(n)})


def locator_coefficients(subset: tuple[int, ...], p: int) -> list[int]:
    coeff = [1]
    for x in subset:
        nxt = [0] * (len(coeff) + 1)
        for i, c in enumerate(coeff):
            nxt[i] = (nxt[i] + c) % p
            nxt[i + 1] = (nxt[i + 1] - c * x) % p
        coeff = nxt
    return coeff


def power_sums(subset: tuple[int, ...], t: int, p: int) -> list[int]:
    return [sum(pow(x, j, p) for x in subset) % p for j in range(1, t + 1)]


def q_free_indices(q: int, b: int, t: int) -> list[int]:
    return [i for i in range(1, min(b, t) + 1) if i % q != 0]


def subset_row(p: int, n: int, b: int, t: int) -> dict[str, Any]:
    domain = multiplicative_subgroup(p, n)
    qfree = q_free_indices(p, b, t)
    counts: Counter[str] = Counter()
    mismatches: list[dict[str, Any]] = []
    for subset in itertools.combinations(domain, b):
        sums = power_sums(subset, t, p)
        coeff = locator_coefficients(subset, p)
        power_zero = all(x == 0 for x in sums)
        coeff_zero = all(coeff[i] == 0 for i in qfree)
        counts["power_zero" if power_zero else "power_nonzero"] += 1
        counts["coeff_zero" if coeff_zero else "coeff_nonzero"] += 1
        if power_zero:
            counts["both_zero"] += int(coeff_zero)
        if power_zero != coeff_zero:
            mismatches.append(
                {
                    "subset": list(subset),
                    "power_sums": sums,
                    "locator_coefficients": coeff,
                    "q_free_indices": qfree,
                }
            )
    total = sum(1 for _ in itertools.combinations(domain, b))
    return {
        "p": p,
        "n": n,
        "b": b,
        "t": t,
        "domain": domain,
        "total_subsets": total,
        "q_free_indices": qfree,
        "counts": dict(counts),
        "mismatch_count": len(mismatches),
        "mismatch_examples": mismatches[:3],
        "pass": len(mismatches) == 0,
    }


def derivative_zero(coeff: tuple[int, ...], q: int, t: int) -> bool:
    b = len(coeff) - 1
    return all((i * coeff[i]) % q == 0 for i in range(1, min(b, t) + 1))


def qfree_coeff_zero(coeff: tuple[int, ...], q: int, t: int) -> bool:
    b = len(coeff) - 1
    return all(coeff[i] % q == 0 for i in q_free_indices(q, b, t))


def formal_derivative_row(q: int, b: int, t: int) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    mismatches: list[dict[str, Any]] = []
    for tail in itertools.product(range(q), repeat=b):
        coeff = (1,) + tail
        dzero = derivative_zero(coeff, q, t)
        czero = qfree_coeff_zero(coeff, q, t)
        counts["derivative_zero" if dzero else "derivative_nonzero"] += 1
        counts["qfree_coeff_zero" if czero else "qfree_coeff_nonzero"] += 1
        if dzero != czero:
            mismatches.append({"coefficients": list(coeff)})
    return {
        "q": q,
        "b": b,
        "t": t,
        "total_polynomials": q**b,
        "q_free_indices": q_free_indices(q, b, t),
        "q_divisible_free_indices": [
            i for i in range(1, min(b, t) + 1) if i % q == 0
        ],
        "counts": dict(counts),
        "mismatch_count": len(mismatches),
        "mismatch_examples": mismatches[:3],
        "pass": len(mismatches) == 0,
    }


def build_certificate() -> dict[str, Any]:
    subset_rows = [
        subset_row(5, 4, 2, 1),
        subset_row(7, 6, 3, 2),
        subset_row(11, 10, 5, 3),
        subset_row(17, 8, 4, 20),
        subset_row(17, 16, 8, 20),
        subset_row(31, 15, 7, 40),
    ]
    formal_rows = [
        formal_derivative_row(2, 8, 8),
        formal_derivative_row(3, 7, 9),
        formal_derivative_row(5, 6, 11),
    ]
    ensure(all(row["pass"] for row in subset_rows), "subset row mismatch")
    ensure(all(row["pass"] for row in formal_rows), "formal row mismatch")
    ensure(any(row["counts"].get("both_zero", 0) > 0 for row in subset_rows), "no true branch exercised")
    ensure(any(row["t"] > row["p"] for row in subset_rows), "no t>p subset row exercised")
    ensure(
        all(row["q_divisible_free_indices"] for row in formal_rows),
        "formal rows did not exercise q-divisible free indices",
    )
    return {
        "schema_version": "rowsharp-q-full-ladder-dictionary-v1",
        "status": "PROVED_DICTIONARY_LEMMA_WITH_AUDIT_REPLAY",
        "claim": (
            "For reversed locators ell*_S=prod(1-xX), vanishing power sums "
            "p_1..p_t are equivalent to vanishing coefficients c_i at exactly "
            "the indices 1<=i<=min(t,|S|) with char(F) not dividing i."
        ),
        "does_not_prove": [
            "row-sharp Q",
            "a max-fiber bound",
            "image-scale MI/MA",
            "a direct Sidon payment",
            "a finite adjacent upper ledger",
        ],
        "subset_rows": subset_rows,
        "formal_derivative_rows": formal_rows,
    }


def main() -> None:
    cert = build_certificate()
    CERT_DIR.mkdir(parents=True, exist_ok=True)
    CERT_PATH.write_text(json.dumps(cert, indent=2) + "\n")
    print(json.dumps({
        "status": cert["status"],
        "subset_rows": len(cert["subset_rows"]),
        "formal_derivative_rows": len(cert["formal_derivative_rows"]),
        "certificate": str(CERT_PATH.relative_to(ROOT)),
    }, indent=2))


if __name__ == "__main__":
    main()
