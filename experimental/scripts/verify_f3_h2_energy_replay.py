#!/usr/bin/env python3
"""Exact h=2 replay for the F3 shallow stratum.

The script keeps Terminal B honest:
  * it verifies the corrected energy decomposition
    E(H)=8T_2+4M_2+2n^2-n;
  * it replays h=2 rows through n=512 at q~n^2 and q~n^3;
  * it checks that a hypothetical explicit C=100 energy theorem would close the
    h=2 floor once proved;
  * it audits a simple Stepanov-ansatz parameter family, without claiming the
    missing nonvanishing/rank lemma.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from fractions import Fraction


def is_prime(m: int) -> bool:
    if m < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for a in small:
        if m % a == 0:
            return m == a
    d, r = m - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in small:
        if a >= m:
            continue
        x = pow(a, d, m)
        if x in (1, m - 1):
            continue
        for _ in range(r - 1):
            x = x * x % m
            if x == m - 1:
                break
        else:
            return False
    return True


def next_prime_1mod(n: int, lo: int) -> int:
    q = (lo // n) * n + 1
    while q <= lo or not is_prime(q):
        q += n
    return q


def primitive_root_of_order(q: int, n: int) -> int:
    assert (q - 1) % n == 0
    for cand in range(2, q):
        x = pow(cand, (q - 1) // n, q)
        if x == 1:
            continue
        y, order = x, 1
        while y != 1:
            y = y * x % q
            order += 1
            if order > n:
                break
        if order == n:
            return x
    raise RuntimeError(f"no primitive {n}-th root modulo {q}")


@dataclass(frozen=True)
class H2Row:
    n: int
    q: int
    regime: int
    t2: int
    midpoint: int
    energy: int
    measured_c: float
    max_fiber: int
    toral: int


def h2_row(n: int, regime: int) -> H2Row:
    q = next_prime_1mod(n, n ** regime)
    zeta = primitive_root_of_order(q, n)
    domain = [pow(zeta, i, q) for i in range(n)]
    buckets: dict[int, list[tuple[int, int]]] = {}
    for a, b in itertools.combinations(range(n), 2):
        buckets.setdefault((domain[a] + domain[b]) % q, []).append((a, b))

    t2 = 0
    toral = 0
    step = n // 2 if n % 2 == 0 else None
    for pairs in buckets.values():
        if len(pairs) < 2:
            continue
        for i, left in enumerate(pairs):
            lset = set(left)
            for right in pairs[i + 1 :]:
                if lset & set(right):
                    continue
                t2 += 1
                if step is not None:
                    if (left[0] % step == left[1] % step) and (
                        right[0] % step == right[1] % step
                    ):
                        toral += 1

    domain_index = {x: i for i, x in enumerate(domain)}
    midpoint = 0
    inv2 = pow(2, -1, q)
    for pairs in buckets.values():
        s = (domain[pairs[0][0]] + domain[pairs[0][1]]) % q
        mid = (s * inv2) % q
        if mid in domain_index:
            # Every distinct pair in this bucket is disjoint from the midpoint
            # singleton in odd characteristic.
            midpoint += len(pairs)

    energy = 8 * t2 + 4 * midpoint + 2 * n * n - n

    # Direct ordered-energy check from sum buckets: ordered pair counts include
    # n diagonal pairs (a,a) plus two orders for each unordered distinct pair.
    ordered_sum_counts: dict[int, int] = {}
    for a in range(n):
        for b in range(n):
            s = (domain[a] + domain[b]) % q
            ordered_sum_counts[s] = ordered_sum_counts.get(s, 0) + 1
    direct_energy = sum(v * v for v in ordered_sum_counts.values())
    if direct_energy != energy:
        raise AssertionError((n, q, direct_energy, energy))

    max_fiber = max(len(v) for v in buckets.values())
    return H2Row(
        n=n,
        q=q,
        regime=regime,
        t2=t2,
        midpoint=midpoint,
        energy=energy,
        measured_c=energy / (n ** 2.5),
        max_fiber=max_fiber,
        toral=toral,
    )


@dataclass(frozen=True)
class StepanovAudit:
    n: int
    a: int
    b: int
    c: int
    d: int
    threshold_m: int
    unknowns: int
    constraints: int
    degree_bound: int
    contradiction_margin: int


def stepanov_parameter_audit(n: int) -> StepanovAudit:
    """A conservative parameter family for the single-shift ansatz.

    Under the falsifying assumption M > 4 n^(2/3), choose A,B,C on the
    standard n^(2/3), n^(1/3), n^(1/3) scale, then choose the least
    multiplicity D for which D*M beats the degree proxy
    (A-1)+(B+C-2)n.  This audits arithmetic only; it does not prove the
    nonvanishing/rank lemma.
    """

    root3 = math.ceil(n ** (1 / 3))
    root23 = math.ceil(n ** (2 / 3))
    a = 8 * root23
    b = root3
    c = root3
    threshold_m = math.floor(4 * (n ** (2 / 3))) + 1
    unknowns = a * b * c
    degree_bound = (a - 1) + (b + c - 2) * n
    d = degree_bound // threshold_m + 1
    constraints = threshold_m * d
    contradiction_margin = threshold_m * d - degree_bound
    if unknowns <= constraints:
        raise AssertionError((n, unknowns, constraints, degree_bound))
    return StepanovAudit(
        n=n,
        a=a,
        b=b,
        c=c,
        d=d,
        threshold_m=threshold_m,
        unknowns=unknowns,
        constraints=constraints,
        degree_bound=degree_bound,
        contradiction_margin=contradiction_margin,
    )


def main() -> None:
    ns = (16, 32, 64, 128, 256, 512)
    rows = [h2_row(n, reg) for n in ns for reg in (2, 3)]
    max_c = max(r.measured_c for r in rows)
    print("Exact h=2 energy rows:")
    print(
        "   n regime        q       T2     mid     toral    maxfib"
        "       E(H)   E/n^2.5"
    )
    for r in rows:
        print(
            f"{r.n:4d}   n^{r.regime:<1d} {r.q:8d} {r.t2:8d}"
            f" {r.midpoint:7d} {r.toral:8d} {r.max_fiber:8d}"
            f" {r.energy:10d} {r.measured_c:9.4f}"
        )
        if r.t2 >= r.n ** 3:
            raise AssertionError(f"h=2 floor fails at measured row {r}")

    c_hyp = 100
    n0 = math.floor((c_hyp / 8) ** 2) + 1
    for r in rows:
        if r.n < n0 and r.t2 >= r.n ** 3:
            raise AssertionError(f"small measured row not closed by exact T2: {r}")
    print(f"max measured E(H)/n^2.5 = {max_c:.4f}")
    print(
        f"If an explicit C={c_hyp} energy theorem is proved, "
        f"(C/8)n^2.5 < n^3 for all n >= {n0}; smaller measured rows pass exactly."
    )
    c_cp = Fraction(16, 3)
    cp_ratio = c_cp / 8
    if cp_ratio >= 1:
        raise AssertionError(cp_ratio)
    print(
        "If the explicit Cochrane-Pinner external constant C=16/3 is accepted, "
        "(C/8)n^2.5 = (2/3)n^2.5 < n^3 for every n >= 1."
    )

    print("\nStepanov single-shift ansatz parameter audit:")
    print("   n      A    B    C    D    M0  unknowns constraints degree margin")
    for n in ns:
        audit = stepanov_parameter_audit(n)
        print(
            f"{audit.n:4d} {audit.a:6d} {audit.b:4d} {audit.c:4d} {audit.d:4d}"
            f" {audit.threshold_m:5d} {audit.unknowns:9d}"
            f" {audit.constraints:11d} {audit.degree_bound:6d}"
            f" {audit.contradiction_margin:6d}"
        )
    print("H2_ENERGY_REPLAY_PASS")


if __name__ == "__main__":
    main()
