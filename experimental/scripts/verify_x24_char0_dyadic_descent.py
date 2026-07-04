#!/usr/bin/env python3
"""X24 characteristic-zero dyadic descent classifier.

For n=2^s over characteristic zero, same-top-(h-1) trades in mu_n recursively
descend through the antipodal quotient.  Consequently:

  * if h is not a power of two, no disjoint h-trade exists;
  * if h is a power of two, every h-trade is a pair of full mu_h fibers.

The verifier performs exact small-row checks using cyclotomic-coordinate
signatures, and records the proof packet.  Finite-field p-specific reductions
are outside this characteristic-zero theorem.
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
    "x24-char0-dyadic-descent",
    "x24_char0_dyadic_descent.json",
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


def is_power_of_two(x: int) -> bool:
    return x > 0 and (x & (x - 1)) == 0


def mask_from_tuple(t: tuple[int, ...]) -> int:
    out = 0
    for i in t:
        out |= 1 << i
    return out


def exps(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def cyclotomic_rep_from_counts(n: int, counts: list[int]) -> tuple[int, ...]:
    """Represent a value in Q(zeta_n), n=2^s, in the Phi_n basis.

    Since Phi_n(X)=X^(n/2)+1, the reduced coefficient vector is
    counts[i] - counts[i+n/2].
    """
    half = n // 2
    return tuple(counts[i] - counts[i + half] for i in range(half))


def power_sum_rep(n: int, subset: tuple[int, ...], r: int) -> tuple[int, ...]:
    counts = [0] * n
    for i in subset:
        counts[(r * i) % n] += 1
    return cyclotomic_rep_from_counts(n, counts)


def trade_signature(n: int, subset: tuple[int, ...], h: int) -> tuple[tuple[int, ...], ...]:
    # In characteristic zero, equality of e_1..e_{h-1} is equivalent to
    # equality of power sums p_1..p_{h-1}.
    return tuple(power_sum_rep(n, subset, r) for r in range(1, h))


def is_full_mu_h_fiber(mask: int, n: int, h: int) -> bool:
    if mask.bit_count() != h or n % h:
        return False
    step = n // h
    s = set(exps(mask, n))
    return any({(r + j * step) % n for j in range(h)} == s for r in range(step))


def is_antipodal_union(mask: int, n: int) -> bool:
    half = n // 2
    s = set(exps(mask, n))
    return all(((i + half) % n) in s for i in s)


def quotient_mask(mask: int, n: int) -> int:
    half = n // 2
    out = 0
    for i in exps(mask, n):
        out |= 1 << (i % half)
    return out


def classified_by_dyadic_descent(p_mask: int, q_mask: int, n: int, h: int) -> bool:
    if h == 1:
        return p_mask.bit_count() == q_mask.bit_count() == 1 and not (p_mask & q_mask)
    if h % 2:
        return False
    if not (is_antipodal_union(p_mask, n) and is_antipodal_union(q_mask, n)):
        return False
    return classified_by_dyadic_descent(quotient_mask(p_mask, n), quotient_mask(q_mask, n), n // 2, h // 2)


def expected_trade_count(n: int, h: int) -> int:
    if not is_power_of_two(h) or n % h:
        return 0
    fibers = n // h
    return fibers * (fibers - 1) // 2


def analyze_row(n: int, h: int) -> dict[str, Any]:
    groups: dict[tuple[tuple[int, ...], ...], list[int]] = defaultdict(list)
    for subset in combinations(range(n), h):
        groups[trade_signature(n, subset, h)].append(mask_from_tuple(subset))

    trade_count = 0
    classified_count = 0
    bad: list[dict[str, Any]] = []
    for masks in groups.values():
        if len(masks) < 2:
            continue
        for a, p_mask in enumerate(masks):
            for q_mask in masks[a + 1 :]:
                if p_mask & q_mask:
                    continue
                trade_count += 1
                classified = (
                    is_full_mu_h_fiber(p_mask, n, h)
                    and is_full_mu_h_fiber(q_mask, n, h)
                    and classified_by_dyadic_descent(p_mask, q_mask, n, h)
                )
                if classified:
                    classified_count += 1
                elif len(bad) < 5:
                    bad.append({"P": exps(p_mask, n), "Q": exps(q_mask, n)})

    expected = expected_trade_count(n, h)
    check(
        f"n={n}, h={h}: char-zero trades match dyadic fiber classifier",
        not bad and trade_count == expected and classified_count == trade_count,
        f"trades={trade_count}, expected={expected}, classified={classified_count}",
    )
    return {
        "n": n,
        "h": h,
        "subset_count": sum(1 for _ in combinations(range(n), h)),
        "trade_count": trade_count,
        "expected_trade_count": expected,
        "classified_count": classified_count,
        "bad_examples": bad,
    }


def build_certificate() -> dict[str, Any]:
    rows = [
        analyze_row(8, 2),
        analyze_row(8, 3),
        analyze_row(8, 4),
        analyze_row(16, 2),
        analyze_row(16, 3),
        analyze_row(16, 4),
        analyze_row(16, 5),
        analyze_row(16, 8),
        analyze_row(32, 2),
        analyze_row(32, 3),
        analyze_row(32, 4),
    ]
    check("all checked rows have no bad examples", all(not row["bad_examples"] for row in rows))
    check(
        "non-power h rows are empty in checked rows",
        all(row["trade_count"] == 0 for row in rows if not is_power_of_two(row["h"])),
    )
    return {
        "task": "X24 characteristic-zero dyadic descent",
        "node": "active_core_count_bound",
        "status": "PROVED over characteristic zero: dyadic trades are exactly full power-of-two fibers",
        "theorem": (
            "For n=2^s over C, disjoint h-subsets of mu_n with equal first "
            "h-1 elementary symmetric sums exist only when h is a power of "
            "two; then both supports are full mu_h fibers."
        ),
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
            f"n={row['n']:<2d} h={row['h']:<2d} trades={row['trade_count']:<4d} "
            f"expected={row['expected_trade_count']:<4d}"
        )

    if FAILS:
        print("\nFAIL:")
        for name in FAILS:
            print(f"  - {name}")
        return 1

    print(f"\nPASS: {NCHECK} X24 char-zero dyadic-descent checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
