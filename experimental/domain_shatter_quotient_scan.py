#!/usr/bin/env python3
"""Residual quotient-core scan for punctured smooth cyclic domains.

Proof status: EXPERIMENTAL / AUDIT, with a proved finite lower-bound predicate.

The original smooth domain is represented by exponents Z/nZ.  For each dyadic
quotient scale M, the order-M subgroup cosets are residue classes modulo
N=n/M:

    C_r = {r + tN : 0 <= t < M}.

After puncturing, the usual quotient-core construction survives at scale M if
there are enough intact M-cosets for the quotient union and at least one anchor
M-coset containing sigma retained points.  If k is divisible by M and
qdim=k/M, the residual lower bound is

    binom(full_cosets - 1_anchor_is_full, qdim)

maximized over anchor cosets with retained size at least sigma.

This is a scanner for the X3 domain-shattering direction.  It does not prove a
positive local-limit theorem; it identifies which explicit quotient-core lower
bounds survive a proposed puncturing pattern.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Dict, Iterable, List, Optional, Sequence, Set

LOG2 = math.log(2)
DEFAULT_PATTERNS = ("none", "hit-cosets:8", "hit-cosets:16", "hit-cosets:32")
DEFAULT_RATES = (Fraction(1, 2), Fraction(1, 4))
DEFAULT_ETAS = (Fraction(1, 64), Fraction(1, 32), Fraction(1, 16))


@dataclass(frozen=True)
class ResidualScale:
    """One surviving punctured quotient-core contribution."""

    M: int
    N: int
    quotient_dimension: int
    full_cosets: int
    anchor_cosets: int
    best_available_full_cosets: int
    log2_list_size: float

    def to_json(self) -> Dict[str, object]:
        return {
            "M_coset_size": self.M,
            "N_quotient_order": self.N,
            "quotient_dimension": self.quotient_dimension,
            "full_cosets": self.full_cosets,
            "anchor_cosets": self.anchor_cosets,
            "best_available_full_cosets": self.best_available_full_cosets,
            "log2_list_size": round(self.log2_list_size, 6),
        }


def parse_fraction(raw: str) -> Fraction:
    try:
        return Fraction(raw)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid fraction: {raw}") from exc


def parse_fraction_list(raw: str) -> List[Fraction]:
    if not raw:
        return []
    return [parse_fraction(part.strip()) for part in raw.split(",") if part.strip()]


def fraction_label(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def ceil_fraction_times(value: Fraction, n: int) -> int:
    numerator = value.numerator * n
    return (numerator + value.denominator - 1) // value.denominator


def log2_binom(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    if k == 0 or k == n:
        return 0.0
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)) / LOG2


def divisors_of_power_of_two(n: int) -> List[int]:
    if n <= 0 or n & (n - 1):
        raise ValueError(f"expected a positive power of two, got n={n}")
    result = []
    value = 1
    while value <= n:
        result.append(value)
        value <<= 1
    return result


def parse_patterns(raw_patterns: Sequence[str], n: int) -> List[Dict[str, object]]:
    return [build_pattern(pattern, n) for pattern in raw_patterns]


def build_pattern(pattern: str, n: int) -> Dict[str, object]:
    if pattern == "none":
        return {"name": pattern, "deleted": set()}

    if pattern.startswith("hit-cosets:"):
        M = int(pattern.split(":", 1)[1])
        if M <= 0 or n % M != 0:
            raise ValueError(f"hit-cosets M must divide n: {pattern}")
        N = n // M
        return {
            "name": pattern,
            "deleted": set(range(N)),
            "description": f"delete one representative from every order-{M} coset",
        }

    if pattern.startswith("periodic:"):
        _, modulus_raw, residue_raw = pattern.split(":")
        modulus = int(modulus_raw)
        residue = int(residue_raw)
        if modulus <= 0:
            raise ValueError(f"periodic modulus must be positive: {pattern}")
        return {
            "name": pattern,
            "deleted": {i for i in range(n) if i % modulus == residue % modulus},
            "description": f"delete exponents i == {residue % modulus} mod {modulus}",
        }

    if pattern.startswith("prefix:"):
        count = int(pattern.split(":", 1)[1])
        if count < 0 or count > n:
            raise ValueError(f"prefix count must lie in [0,n]: {pattern}")
        return {
            "name": pattern,
            "deleted": set(range(count)),
            "description": f"delete the first {count} exponent positions",
        }

    if pattern.startswith("random:"):
        _, count_raw, seed_raw = pattern.split(":")
        count = int(count_raw)
        seed = int(seed_raw)
        if count < 0 or count > n:
            raise ValueError(f"random count must lie in [0,n]: {pattern}")
        rng = random.Random(seed)
        return {
            "name": pattern,
            "deleted": set(rng.sample(range(n), count)),
            "description": f"delete {count} positions with deterministic seed {seed}",
        }

    raise ValueError(f"unknown puncturing pattern: {pattern}")


def coset_counts(n: int, retained: Set[int], M: int) -> List[int]:
    N = n // M
    counts = [0] * N
    for position in retained:
        counts[position % N] += 1
    return counts


def residual_scales(n: int, retained: Set[int], k: int, sigma: int) -> List[ResidualScale]:
    records = []
    for M in divisors_of_power_of_two(n):
        if M <= 1 or sigma >= M or k % M != 0:
            continue
        N = n // M
        qdim = k // M
        if qdim < 1:
            continue

        counts = coset_counts(n, retained, M)
        full_cosets = sum(1 for count in counts if count == M)
        anchor_indices = [index for index, count in enumerate(counts) if count >= sigma]
        best_available = -1
        for index in anchor_indices:
            available = full_cosets - (1 if counts[index] == M else 0)
            best_available = max(best_available, available)
        if best_available < qdim:
            continue

        records.append(
            ResidualScale(
                M=M,
                N=N,
                quotient_dimension=qdim,
                full_cosets=full_cosets,
                anchor_cosets=len(anchor_indices),
                best_available_full_cosets=best_available,
                log2_list_size=log2_binom(best_available, qdim),
            )
        )
    records.sort(key=lambda item: (-item.log2_list_size, item.M))
    return records


def retained_positions(n: int, deleted: Set[int]) -> Set[int]:
    return set(range(n)) - deleted


def scan_case(
    m: int,
    rate: Fraction,
    eta: Fraction,
    pattern: Dict[str, object],
    dimension_source: str,
    top_scales: int,
) -> Dict[str, object]:
    n = 1 << m
    deleted = set(pattern["deleted"])
    retained = retained_positions(n, deleted)
    retained_count = len(retained)
    if dimension_source == "original":
        k_base = n
    else:
        k_base = retained_count
    if (rate * k_base).denominator != 1:
        k = (rate.numerator * k_base) // rate.denominator
    else:
        k = int(rate * k_base)
    sigma = ceil_fraction_times(eta, retained_count)
    scales = residual_scales(n, retained, k, sigma)
    retained_scales = scales if top_scales < 0 else scales[:top_scales]
    profile = None if not scales else round(scales[0].log2_list_size, 6)

    return {
        "m": m,
        "n_original": n,
        "retained_count": retained_count,
        "deleted_count": len(deleted),
        "retained_fraction": retained_count / n,
        "pattern": pattern["name"],
        "pattern_description": pattern.get("description", "no puncturing"),
        "rate_nominal": fraction_label(rate),
        "eta": fraction_label(eta),
        "dimension_source": dimension_source,
        "k": k,
        "sigma": sigma,
        "profile_log2": profile,
        "active_scales": [scale.to_json() for scale in retained_scales],
    }


def scan(
    m_min: int,
    m_max: int,
    rates: Iterable[Fraction],
    etas: Iterable[Fraction],
    patterns: Sequence[str],
    dimension_source: str,
    top_scales: int,
) -> Dict[str, object]:
    cases = []
    for m in range(m_min, m_max + 1):
        n = 1 << m
        built_patterns = parse_patterns(patterns, n)
        for pattern in built_patterns:
            for rate in rates:
                for eta in etas:
                    cases.append(
                        scan_case(
                            m=m,
                            rate=rate,
                            eta=eta,
                            pattern=pattern,
                            dimension_source=dimension_source,
                            top_scales=top_scales,
                        )
                    )
    return {
        "proof_status": "EXPERIMENTAL / AUDIT",
        "theorem_problem_id": "X3-domain-shattering-quotient-core-residual",
        "determinism": "deterministic scan; random patterns require explicit seed",
        "object_checked": (
            "surviving quotient-core lower bounds on punctured cyclic domains, "
            "counting intact quotient cosets and anchor cosets with sigma points"
        ),
        "cases": cases,
    }


def format_value(value: object) -> str:
    if value is None:
        return "empty"
    return f"{float(value):.2f}"


def format_scales(scales: Sequence[Dict[str, object]]) -> str:
    if not scales:
        return "-"
    pieces = []
    for scale in scales:
        pieces.append(
            "M={M},N={N},full={full},anchors={anchors},log={log:.1f}".format(
                M=scale["M_coset_size"],
                N=scale["N_quotient_order"],
                full=scale["full_cosets"],
                anchors=scale["anchor_cosets"],
                log=float(scale["log2_list_size"]),
            )
        )
    return "; ".join(pieces)


def print_text(result: Dict[str, object]) -> None:
    print("Domain-shattering quotient-core residual scan")
    print("proof_status: EXPERIMENTAL / AUDIT")
    print("object: residual quotient-core lower bounds after puncturing")
    print()
    for case in result["cases"]:
        print(
            "m={m:>2} n=2^{m:<2} pattern={pattern:<14} retained={retained}/{n} "
            "rho={rho:<4} eta={eta:<5} k={k:<7} sigma={sigma:<6} profile={profile}".format(
                m=case["m"],
                pattern=case["pattern"],
                retained=case["retained_count"],
                n=case["n_original"],
                rho=case["rate_nominal"],
                eta=case["eta"],
                k=case["k"],
                sigma=case["sigma"],
                profile=format_value(case["profile_log2"]),
            )
        )
        print("  active scales: " + format_scales(case["active_scales"]))
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan quotient-core lower bounds that survive domain puncturing."
    )
    parser.add_argument("--m-min", type=int, default=8, help="minimum m for n=2^m")
    parser.add_argument("--m-max", type=int, default=12, help="maximum m for n=2^m")
    parser.add_argument(
        "--rates",
        type=parse_fraction_list,
        default=list(DEFAULT_RATES),
        help="comma-separated nominal rates, e.g. 1/2,1/4",
    )
    parser.add_argument(
        "--etas",
        type=parse_fraction_list,
        default=list(DEFAULT_ETAS),
        help="comma-separated reserves eta, e.g. 1/64,1/32",
    )
    parser.add_argument(
        "--pattern",
        action="append",
        default=[],
        help=(
            "puncturing pattern: none, hit-cosets:M, periodic:mod:residue, "
            "prefix:count, or random:count:seed"
        ),
    )
    parser.add_argument(
        "--dimension-source",
        choices=("original", "retained"),
        default="original",
        help="compute k from the original length or retained length",
    )
    parser.add_argument(
        "--top-scales",
        type=int,
        default=-1,
        help="number of active scales retained per case; negative retains all",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="output format",
    )
    args = parser.parse_args()

    if args.m_min < 1 or args.m_max < args.m_min:
        raise SystemExit("require 1 <= --m-min <= --m-max")
    patterns = args.pattern or list(DEFAULT_PATTERNS)

    result = scan(
        m_min=args.m_min,
        m_max=args.m_max,
        rates=args.rates,
        etas=args.etas,
        patterns=patterns,
        dimension_source=args.dimension_source,
        top_scales=args.top_scales,
    )
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
