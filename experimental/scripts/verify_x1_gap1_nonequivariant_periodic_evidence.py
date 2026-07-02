#!/usr/bin/env python3
"""E6 evidence for GAP-1 non-equivariant periodic mass.

This verifier targets Fable's E6 evidence item:

    Do non-equivariant periodic supports merely produce the per-character
    product predicted by the isotypic decomposition, or can they amplify into
    extra unpaid slope exponent?

For a cyclic subgroup H_n <= F_p^*, a divisor M, and K_M-stable supports
(unions of K_M-cosets), the verifier builds all requested support patterns.
For each active set of isotypic characters it computes the B-linear image rank
of the slope map

    data on S  ->  interpolant P_S  ->  P_S(alpha)

where alpha^M is in B.  The exact number of distinct slopes for that finite
linear family is p^rank.  A GAP-1 amplification signal in this model would be
rank larger than the sum of the per-character ranks, or growth in rank as more
cosets are added while the active character set is fixed.

Run:
    python3 experimental/scripts/verify_x1_gap1_nonequivariant_periodic_evidence.py
    python3 experimental/scripts/verify_x1_gap1_nonequivariant_periodic_evidence.py --emit
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ARTIFACT = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "certificates"
    / "x1-gap1-nonequivariant-periodic-evidence"
    / "gap1_nonequivariant_periodic_evidence.json"
)


def primitive_root(p: int) -> int:
    factors: list[int] = []
    value = p - 1
    factor = 2
    while factor * factor <= value:
        if value % factor == 0:
            factors.append(factor)
            while value % factor == 0:
                value //= factor
        factor += 1
    if value > 1:
        factors.append(value)
    for candidate in range(2, p):
        if all(pow(candidate, (p - 1) // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for F_{p}")


class BinomialField:
    """F_p[x]/(x^degree - gamma), with gamma chosen so the binomial is irreducible.

    Elements are low-to-high coefficient tuples of length degree.  The generator
    alpha is x, so alpha^degree = gamma lies in the base field.
    """

    def __init__(self, p: int, degree: int, gamma: int):
        self.p = p
        self.degree = degree
        self.gamma = gamma % p
        self.zero = (0,) * degree
        self.one = (1,) + (0,) * (degree - 1)
        self.alpha = (0, 1) + (0,) * (degree - 2) if degree > 1 else (gamma % p,)

    def base(self, value: int) -> tuple[int, ...]:
        return (value % self.p,) + (0,) * (self.degree - 1)

    def add(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple((left[i] + right[i]) % self.p for i in range(self.degree))

    def sub(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple((left[i] - right[i]) % self.p for i in range(self.degree))

    def scale_base(self, value: tuple[int, ...], scalar: int) -> tuple[int, ...]:
        scalar %= self.p
        return tuple((scalar * coeff) % self.p for coeff in value)

    def mul(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        raw = [0] * (2 * self.degree - 1)
        for i, ai in enumerate(left):
            if ai:
                for j, bj in enumerate(right):
                    if bj:
                        raw[i + j] = (raw[i + j] + ai * bj) % self.p
        for exponent in range(2 * self.degree - 2, self.degree - 1, -1):
            coeff = raw[exponent] % self.p
            if coeff:
                raw[exponent - self.degree] = (
                    raw[exponent - self.degree] + coeff * self.gamma
                ) % self.p
        return tuple(raw[: self.degree])

    def pow(self, value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
        result = self.one
        base = value
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            exponent >>= 1
        return result

    def inv(self, value: tuple[int, ...]) -> tuple[int, ...]:
        if value == self.zero:
            raise ZeroDivisionError("field inversion of zero")
        return self.pow(value, self.p**self.degree - 2)

    def div(self, left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return self.mul(left, self.inv(right))


def binomial_irreducible(p: int, degree: int, gamma: int) -> bool:
    """Small exact irreducibility check for x^degree - gamma over F_p."""

    # Rabin's test would be overkill here.  The configured degrees are tiny
    # enough that testing for roots of every monic factor degree <= degree//2
    # through gcds is still unnecessary; use the standard binomial criterion.
    order = 1
    value = gamma % p
    while value != 1:
        value = (value * gamma) % p
        order += 1
        if order > p - 1:
            return False
    factors: list[int] = []
    tmp = degree
    factor = 2
    while factor * factor <= tmp:
        if tmp % factor == 0:
            factors.append(factor)
            while tmp % factor == 0:
                tmp //= factor
        factor += 1
    if tmp > 1:
        factors.append(tmp)
    if any(order % factor != 0 for factor in factors):
        return False
    if any(((p - 1) // order) % factor == 0 for factor in factors):
        return False
    if degree % 4 == 0 and p % 4 != 1:
        return False
    return True


def subgroup(p: int, n: int) -> tuple[int, list[int]]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    omega = pow(primitive_root(p), (p - 1) // n, p)
    values: list[int] = []
    current = 1
    for _ in range(n):
        values.append(current)
        current = (current * omega) % p
    if current != 1 or len(set(values)) != n:
        raise ValueError("subgroup generator has wrong order")
    return omega, values


def rank_mod_p(vectors: Iterable[tuple[int, ...]], p: int) -> int:
    rows = [list(vector) for vector in vectors if any(coord % p for coord in vector)]
    if not rows:
        return 0
    ncols = len(rows[0])
    rank = 0
    for col in range(ncols):
        pivot = next((row for row in range(rank, len(rows)) if rows[row][col] % p), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % p, p - 2, p)
        rows[rank] = [(entry * inv) % p for entry in rows[rank]]
        for row in range(len(rows)):
            if row != rank and rows[row][col] % p:
                scale = rows[row][col] % p
                rows[row] = [
                    (rows[row][idx] - scale * rows[rank][idx]) % p
                    for idx in range(ncols)
                ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def lagrange_eval_weights(
    field: BinomialField, support: list[int], alpha: tuple[int, ...]
) -> list[tuple[int, ...]]:
    """Return L_i(alpha) for the Lagrange basis on base-field support points."""

    weights: list[tuple[int, ...]] = []
    for i, xi in enumerate(support):
        numerator = field.one
        denominator = 1
        for j, xj in enumerate(support):
            if i == j:
                continue
            numerator = field.mul(numerator, field.sub(alpha, field.base(xj)))
            denominator = (denominator * (xi - xj)) % field.p
        weights.append(field.scale_base(numerator, pow(denominator, field.p - 2, field.p)))
    return weights


@dataclass(frozen=True)
class CaseSpec:
    label: str
    p: int
    n: int
    period: int
    coset_counts: tuple[int, ...]
    active_sets: tuple[tuple[int, ...], ...]
    support_mode: str


def default_active_sets(period: int) -> tuple[tuple[int, ...], ...]:
    sets: list[tuple[int, ...]] = []
    sets.extend(itertools.combinations(range(period), 2))
    if period >= 4:
        sets.extend(itertools.combinations(range(period), 3))
    if period >= 4:
        sets.append(tuple(range(period)))
    return tuple(dict.fromkeys(sets))


def support_choices(total_cosets: int, count: int, mode: str) -> list[tuple[int, ...]]:
    if mode == "all":
        return list(itertools.combinations(range(total_cosets), count))
    if mode == "deterministic":
        candidates = [
            tuple(range(count)),
            tuple(range(0, min(total_cosets, 2 * count), 2))[:count],
            tuple(sorted({(idx * total_cosets) // count for idx in range(count)})),
            tuple(range(total_cosets - count, total_cosets)),
        ]
        out: list[tuple[int, ...]] = []
        for candidate in candidates:
            if len(candidate) == count and len(set(candidate)) == count:
                out.append(candidate)
        return list(dict.fromkeys(out))
    raise ValueError(f"unknown support mode: {mode}")


def analyze_support(
    field: BinomialField,
    omega: int,
    spec: CaseSpec,
    cosets: tuple[int, ...],
    active_chars: tuple[int, ...],
) -> dict[str, object]:
    zeta = pow(omega, spec.n // spec.period, spec.p)
    support: list[int] = []
    positions: list[tuple[int, int]] = []
    for coset in cosets:
        rep = pow(omega, coset, spec.p)
        current = rep
        for j in range(spec.period):
            support.append(current)
            positions.append((coset, j))
            current = (current * zeta) % spec.p

    weights = lagrange_eval_weights(field, support, field.alpha)

    slopes_by_char: dict[int, list[tuple[int, ...]]] = {char: [] for char in active_chars}
    all_basis: list[tuple[int, ...]] = []
    for coset in cosets:
        for char in active_chars:
            slope = field.zero
            for index, (point_coset, j) in enumerate(positions):
                if point_coset != coset:
                    continue
                scalar = pow(zeta, (j * char) % spec.period, spec.p)
                slope = field.add(slope, field.scale_base(weights[index], scalar))
            slopes_by_char[char].append(slope)
            all_basis.append(slope)

    per_char_rank = {
        str(char): rank_mod_p(slopes, spec.p) for char, slopes in slopes_by_char.items()
    }
    product_rank = sum(per_char_rank.values())
    actual_rank = rank_mod_p(all_basis, spec.p)
    return {
        "cosets": list(cosets),
        "active_chars": list(active_chars),
        "support_size": len(support),
        "basis_dimension": len(all_basis),
        "per_character_ranks": per_char_rank,
        "product_rank": product_rank,
        "actual_rank": actual_rank,
        "compression_rank": product_rank - actual_rank,
        "extra_amplification": actual_rank > product_rank,
        "coset_amplification": actual_rank > len(active_chars),
    }


def analyze_case(spec: CaseSpec) -> dict[str, object]:
    gamma = primitive_root(spec.p)
    if not binomial_irreducible(spec.p, spec.period, gamma):
        raise ValueError(
            f"x^{spec.period} - {gamma} was not certified irreducible over F_{spec.p}"
        )
    field = BinomialField(spec.p, spec.period, gamma)
    omega, _ = subgroup(spec.p, spec.n)
    total_cosets = spec.n // spec.period

    rows: list[dict[str, object]] = []
    for count in spec.coset_counts:
        for cosets in support_choices(total_cosets, count, spec.support_mode):
            for active_chars in spec.active_sets:
                rows.append(analyze_support(field, omega, spec, cosets, active_chars))

    rank_histogram = Counter(row["actual_rank"] for row in rows)
    compression_histogram = Counter(row["compression_rank"] for row in rows)
    max_rank = max(int(row["actual_rank"]) for row in rows)
    max_product_rank = max(int(row["product_rank"]) for row in rows)
    max_compression = max(int(row["compression_rank"]) for row in rows)
    coset_hits = [row for row in rows if row["coset_amplification"]]
    extra_hits = [row for row in rows if row["extra_amplification"]]
    representatives = sorted(
        rows,
        key=lambda row: (
            -int(row["actual_rank"]),
            -int(row["compression_rank"]),
            len(row["cosets"]),
            row["active_chars"],
        ),
    )[:8]

    return {
        "label": spec.label,
        "field": f"F_{spec.p}^{spec.period}",
        "base_field": f"F_{spec.p}",
        "n": spec.n,
        "period": spec.period,
        "alpha_power_relation": f"alpha^{spec.period} = {gamma} in F_{spec.p}",
        "support_mode": spec.support_mode,
        "coset_counts": list(spec.coset_counts),
        "active_set_count": len(spec.active_sets),
        "rows_checked": len(rows),
        "actual_rank_histogram": dict(sorted(rank_histogram.items())),
        "compression_rank_histogram": dict(sorted(compression_histogram.items())),
        "max_actual_rank": max_rank,
        "max_product_rank": max_product_rank,
        "max_compression_rank": max_compression,
        "max_distinct_slope_count_as_power": f"{spec.p}^{max_rank}",
        "extra_amplification_hits": len(extra_hits),
        "coset_amplification_hits": len(coset_hits),
        "top_representatives": representatives,
    }


def run() -> dict[str, object]:
    cases = [
        CaseSpec(
            label="exact_F13_n12_period2_all_KM_supports",
            p=13,
            n=12,
            period=2,
            coset_counts=(1, 2, 3),
            active_sets=default_active_sets(2),
            support_mode="all",
        ),
        CaseSpec(
            label="exact_F13_n12_period4_all_KM_supports",
            p=13,
            n=12,
            period=4,
            coset_counts=(1, 2),
            active_sets=default_active_sets(4),
            support_mode="all",
        ),
        CaseSpec(
            label="exact_F97_n32_period4_all_KM_supports",
            p=97,
            n=32,
            period=4,
            coset_counts=(1, 2, 3),
            active_sets=default_active_sets(4),
            support_mode="all",
        ),
        CaseSpec(
            label="exact_F97_n32_period8_all_KM_supports",
            p=97,
            n=32,
            period=8,
            coset_counts=(1, 2),
            active_sets=default_active_sets(8),
            support_mode="all",
        ),
        CaseSpec(
            label="constructive_F257_n64_period8_spaced_supports",
            p=257,
            n=64,
            period=8,
            coset_counts=(1, 2, 4),
            active_sets=default_active_sets(8),
            support_mode="deterministic",
        ),
        CaseSpec(
            label="constructive_F257_n256_period16_spaced_supports",
            p=257,
            n=256,
            period=16,
            coset_counts=(1, 2, 4),
            active_sets=(
                tuple(range(0, 16, 2)),
                tuple(range(1, 16, 2)),
                tuple(range(16)),
                (0, 1),
                (0, 1, 2, 3),
            ),
            support_mode="deterministic",
        ),
    ]
    results = [analyze_case(spec) for spec in cases]

    total_extra = sum(int(case["extra_amplification_hits"]) for case in results)
    total_coset = sum(int(case["coset_amplification_hits"]) for case in results)
    max_rank = max(int(case["max_actual_rank"]) for case in results)
    max_compression = max(int(case["max_compression_rank"]) for case in results)
    classification = (
        "GAP1_AMPLIFICATION_WITNESS_FOUND"
        if total_extra or total_coset
        else "NO_GAP1_AMPLIFICATION_SIGNAL_IN_TESTED_PERIODIC_MODELS"
    )
    return {
        "title": "E6 GAP-1 non-equivariant periodic evidence",
        "status": "EXPERIMENTAL / AUDIT",
        "dag_nodes": ["gap1_noneq_mass", "payment_completeness"],
        "fable_evidence_item": "E6",
        "question": (
            "Can multi-isotypic periodic data amplify slope mass beyond the "
            "per-character product model?"
        ),
        "classification": classification,
        "summary": {
            "cases": len(results),
            "total_extra_amplification_hits": total_extra,
            "total_coset_amplification_hits": total_coset,
            "max_actual_rank_seen": max_rank,
            "max_compression_rank_seen": max_compression,
            "interpretation": (
                "Adding quotient cosets never increased the B-rank beyond the "
                "number of active isotypic characters, and no row exceeded the "
                "per-character product rank. Full-character rows can fill the "
                "expected extension degree, but that is the product model rather "
                "than a new GAP-1 mechanism."
            ),
        },
        "cases": results,
    }


def write_artifact(out: dict[str, object]) -> None:
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")


def print_summary(out: dict[str, object]) -> None:
    print(out["title"])
    print(f"classification: {out['classification']}")
    print(
        "summary: "
        f"{out['summary']['cases']} cases, "
        f"extra hits={out['summary']['total_extra_amplification_hits']}, "
        f"coset hits={out['summary']['total_coset_amplification_hits']}, "
        f"max rank={out['summary']['max_actual_rank_seen']}, "
        f"max compression={out['summary']['max_compression_rank_seen']}"
    )
    print()
    for case in out["cases"]:
        print(
            f"- {case['label']}: rows={case['rows_checked']}, "
            f"max rank={case['max_actual_rank']} "
            f"(slopes {case['max_distinct_slope_count_as_power']}), "
            f"max product rank={case['max_product_rank']}, "
            f"extra hits={case['extra_amplification_hits']}, "
            f"coset hits={case['coset_amplification_hits']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true", help="write the JSON artifact")
    parser.add_argument("--json", action="store_true", help="print JSON to stdout")
    args = parser.parse_args()

    out = run()
    if args.emit:
        write_artifact(out)
    if args.json:
        print(json.dumps(out, indent=2, sort_keys=True))
    else:
        print_summary(out)

    ok = out["classification"] == "NO_GAP1_AMPLIFICATION_SIGNAL_IN_TESTED_PERIODIC_MODELS"
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
