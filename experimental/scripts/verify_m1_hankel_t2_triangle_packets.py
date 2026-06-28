#!/usr/bin/env python3
"""Verify t=2 same-slope triangle packet lifts in the Hankel model.

Proof status: PROVED-LOCAL / EXACT FINITE VERIFICATION.

The previous t=2 verifier checks one-exchange edges.  This script checks the
next local shape: pairwise one-exchange triangles inside a fixed-slope fiber.
For the combined syndrome s=Syn(Y-lambda phi), a complement T is active when

    H_{2,j}(s) ell_T = 0.

Every pairwise one-exchange triangle of active complements is either a star or
a top packet:

* star triangles have a common (j-1)-core R and lift to H_{3,j-1}(s) ell_R=0;
* top triangles are contained in a common (j+1)-set U and lift to
  H_{1,j+1}(s) ell_U=0.

The script enumerates all syndrome vectors in small cases, including the first
genuine top-triangle case (F_7, k=2, t=2, j=2).

It also checks the full-top zero-syndrome lemma: if all j+1 complements
U\\{x} inside one (j+1)-top set U are active, then the combined syndrome is
zero.  Thus full top packets belong to the global-codeword/tangent ledger.
Consequently every nonzero top packet has at most j active complements; the
script records the exact active-size profile.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from typing import Sequence

from scan_m1_exact_target_v0 import cyclic_subgroup, support_records
from verify_m1_exact_target_hankel_equivalence import (
    hankel_annihilates,
    locator_coeffs,
    support_hankel_records,
)


def is_one_exchange(left: Sequence[int], right: Sequence[int], j: int) -> bool:
    return len(set(left) & set(right)) == j - 1


def classify_triangle(
    complements: Sequence[Sequence[int]],
    j: int,
) -> tuple[str, tuple[int, ...]]:
    sets = [set(complement) for complement in complements]
    common = set.intersection(*sets)
    union = set.union(*sets)
    if len(common) == j - 1:
        return ("star", tuple(sorted(common)))
    if len(union) == j + 1:
        return ("top", tuple(sorted(union)))
    raise AssertionError(
        {
            "kind": "unclassified-one-exchange-triangle",
            "j": j,
            "complements": [list(complement) for complement in complements],
            "common": sorted(common),
            "union": sorted(union),
        }
    )


def analyze_case(
    p: int,
    k: int,
    max_syndromes: int,
    max_examples: int,
) -> dict[str, object]:
    n = p - 1
    t = 2
    a = k + t
    j = n - a
    r = n - k
    if not (0 < k < a <= n):
        raise ValueError("case must satisfy 0 < k and k+2 <= p-1")
    if j < 1:
        raise ValueError("one-exchange packets require j >= 1")
    syndrome_count = p**r
    if syndrome_count > max_syndromes:
        raise ValueError(
            f"would enumerate {syndrome_count} syndromes; "
            f"raise --max-syndromes to run this exact case"
        )

    domain = cyclic_subgroup(p, n)
    support_hankels = support_hankel_records(domain, support_records(n, a), p)
    complements = [tuple(record["complement_indices"]) for record in support_hankels]
    locators = [tuple(record["locator"]) for record in support_hankels]

    active_histogram: Counter[int] = Counter()
    edge_histogram: Counter[int] = Counter()
    triangle_histogram: Counter[int] = Counter()
    max_active = 0
    max_edges = 0
    max_triangles = 0
    one_exchange_edges = 0
    star_triangles = 0
    top_triangles = 0
    nonzero_top_triangles = 0
    full_top_cliques = 0
    nonzero_full_top_cliques = 0
    max_nonzero_top_active_members = 0
    nonzero_top_active_size_histogram: Counter[int] = Counter()
    star_examples: list[dict[str, object]] = []
    top_examples: list[dict[str, object]] = []
    full_top_examples: list[dict[str, object]] = []

    for syn in itertools.product(range(p), repeat=r):
        active = [
            index
            for index, locator in enumerate(locators)
            if hankel_annihilates(syn, locator, t, p)
        ]
        active_histogram[len(active)] += 1
        max_active = max(max_active, len(active))

        case_edges = 0
        for left, right in itertools.combinations(active, 2):
            if not is_one_exchange(complements[left], complements[right], j):
                continue
            case_edges += 1
            core = tuple(sorted(set(complements[left]) & set(complements[right])))
            core_locator = locator_coeffs(domain, core, p)
            if not hankel_annihilates(syn, core_locator, t + 1, p):
                raise AssertionError(
                    {
                        "kind": "edge-core-lift-failed",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "left": list(complements[left]),
                        "right": list(complements[right]),
                        "core": list(core),
                        "core_locator": list(core_locator),
                    }
                )
        one_exchange_edges += case_edges
        edge_histogram[case_edges] += 1
        max_edges = max(max_edges, case_edges)

        case_triangles = 0
        for triangle in itertools.combinations(active, 3):
            triangle_complements = [complements[index] for index in triangle]
            if not all(
                is_one_exchange(left, right, j)
                for left, right in itertools.combinations(triangle_complements, 2)
            ):
                continue
            case_triangles += 1
            kind, packet = classify_triangle(triangle_complements, j)
            if kind == "star":
                star_triangles += 1
                packet_locator = locator_coeffs(domain, packet, p)
                row_count = t + 1
                if len(star_examples) < max_examples:
                    star_examples.append(
                        {
                            "syndrome": list(syn),
                            "complements": [
                                list(complement) for complement in triangle_complements
                            ],
                            "core": list(packet),
                        }
                    )
            else:
                top_triangles += 1
                if any(syn):
                    nonzero_top_triangles += 1
                packet_locator = locator_coeffs(domain, packet, p)
                row_count = 1
                if len(top_examples) < max_examples:
                    top_examples.append(
                        {
                            "syndrome": list(syn),
                            "complements": [
                                list(complement) for complement in triangle_complements
                            ],
                            "top": list(packet),
                            "nonzero_syndrome": bool(any(syn)),
                        }
                    )

            if not hankel_annihilates(syn, packet_locator, row_count, p):
                raise AssertionError(
                    {
                        "kind": f"{kind}-triangle-lift-failed",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "complements": [
                            list(complement) for complement in triangle_complements
                        ],
                        "packet": list(packet),
                        "packet_locator": list(packet_locator),
                    }
                )

        triangle_histogram[case_triangles] += 1
        max_triangles = max(max_triangles, case_triangles)

        active_set = set(active)
        for top in itertools.combinations(range(n), j + 1):
            top_set = set(top)
            top_members = [
                index
                for index, complement in enumerate(complements)
                if set(complement).issubset(top_set)
            ]
            if len(top_members) != j + 1:
                raise AssertionError(
                    {
                        "kind": "unexpected-top-member-count",
                        "p": p,
                        "k": k,
                        "top": list(top),
                        "member_count": len(top_members),
                    }
                )
            if not all(index in active_set for index in top_members):
                if any(syn):
                    active_size = sum(1 for index in top_members if index in active_set)
                    max_nonzero_top_active_members = max(
                        max_nonzero_top_active_members,
                        active_size,
                    )
                    nonzero_top_active_size_histogram[active_size] += 1
                    if active_size > j:
                        raise AssertionError(
                            {
                                "kind": "nonzero-top-active-size-exceeds-j",
                                "p": p,
                                "k": k,
                                "syndrome": list(syn),
                                "top": list(top),
                                "active_size": active_size,
                                "j": j,
                            }
                        )
                continue
            full_top_cliques += 1
            if any(syn):
                nonzero_full_top_cliques += 1
                raise AssertionError(
                    {
                        "kind": "nonzero-full-top-clique",
                        "p": p,
                        "k": k,
                        "syndrome": list(syn),
                        "top": list(top),
                        "complements": [list(complements[index]) for index in top_members],
                    }
                )
            if len(full_top_examples) < max_examples:
                full_top_examples.append(
                    {
                        "syndrome": list(syn),
                        "top": list(top),
                        "complements": [list(complements[index]) for index in top_members],
                    }
                )

    return {
        "status": "PASS",
        "params": {
            "p": p,
            "n": n,
            "k": k,
            "a": a,
            "t": t,
            "j": j,
            "r": r,
            "domain": domain,
            "support_count": len(support_hankels),
            "syndrome_count": syndrome_count,
        },
        "max_active_complements": max_active,
        "max_one_exchange_edges_per_syndrome": max_edges,
        "max_triangles_per_syndrome": max_triangles,
        "one_exchange_edges": one_exchange_edges,
        "star_triangles": star_triangles,
        "top_triangles": top_triangles,
        "nonzero_top_triangles": nonzero_top_triangles,
        "full_top_cliques": full_top_cliques,
        "nonzero_full_top_cliques": nonzero_full_top_cliques,
        "max_nonzero_top_active_members": max_nonzero_top_active_members,
        "active_complement_histogram": dict(sorted(active_histogram.items())),
        "one_exchange_edge_histogram": dict(sorted(edge_histogram.items())),
        "triangle_histogram": dict(sorted(triangle_histogram.items())),
        "nonzero_top_active_size_histogram": dict(
            sorted(nonzero_top_active_size_histogram.items())
        ),
        "star_examples": star_examples,
        "top_examples": top_examples,
        "full_top_examples": full_top_examples,
    }


def parse_case(value: str) -> tuple[int, int]:
    parts = value.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("case must have form p,k")
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("case entries must be integers") from exc


def print_summary(results: Sequence[dict[str, object]]) -> None:
    print("M1 t=2 Hankel triangle packet verifier")
    for result in results:
        params = result["params"]
        print(
            "case "
            f"p={params['p']} n={params['n']} k={params['k']} "
            f"a={params['a']} j={params['j']}: "
            f"syndromes={params['syndrome_count']} "
            f"edges={result['one_exchange_edges']} "
            f"star_triangles={result['star_triangles']} "
            f"top_triangles={result['top_triangles']} "
            f"nonzero_top={result['nonzero_top_triangles']} "
            f"full_top={result['full_top_cliques']} "
            f"max_nonzero_top_active={result['max_nonzero_top_active_members']}"
        )
    print("PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        type=parse_case,
        dest="cases",
        help="case p,k with t fixed to 2; may be supplied multiple times",
    )
    parser.add_argument(
        "--max-syndromes",
        type=int,
        default=100_000,
        help="guardrail for exact syndrome enumeration",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        default=3,
        help="number of star/top examples retained",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = args.cases or [(5, 1), (7, 2), (7, 3)]
    results = [
        analyze_case(
            p=p,
            k=k,
            max_syndromes=args.max_syndromes,
            max_examples=args.max_examples,
        )
        for p, k in cases
    ]
    if args.json:
        print(json.dumps({"status": "PASS", "cases": results}, indent=2, sort_keys=True))
    else:
        print_summary(results)


if __name__ == "__main__":
    main()
