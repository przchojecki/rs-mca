#!/usr/bin/env python3
"""Verify the Hankel-pencil form of the M1-v0 exact target.

Proof status: EXPERIMENTAL / EXACT FINITE VERIFICATION.

For H <= F_p^* with |H|=n, this script checks two equivalent descriptions of
the support-wise rank-one predicate used in
experimental/notes/m1/m1_exact_target_v0.md:

1. the direct restricted-code test on an a-support S;
2. the complement-locator Hankel recurrence

       (H(Syn(Y)) - lambda H(Syn(phi))) ell_T = 0,
       H(Syn(phi)) ell_T != 0,

   where T=H\\S and ell_T is the monic locator of T.

For the original line notation of the M1 note, phi=-g and Y=f, so the first
display is the same as Przemek's (H(u)+zH(v)) ell_T=0 convention after
renaming v=Syn(g).
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from typing import Sequence

from scan_m1_exact_target_v0 import (
    classify_pair,
    cyclic_subgroup,
    quotient_representatives,
    restriction_sets,
    rs_codewords,
    support_records,
    support_values,
)


def syndrome(word: Sequence[int], domain: Sequence[int], k: int, p: int) -> tuple[int, ...]:
    """Weighted RS dual syndrome for H roots of X^n-1."""
    n = len(domain)
    inv_n = pow(n, -1, p)
    return tuple(
        sum(
            word[index]
            * domain[index]
            * inv_n
            * pow(domain[index], degree, p)
            for index in range(n)
        )
        % p
        for degree in range(n - k)
    )


def locator_coeffs(domain: Sequence[int], complement: Sequence[int], p: int) -> tuple[int, ...]:
    """Return the low-to-high coefficients of prod_{x in T}(X-x)."""
    coeffs: tuple[int, ...] = (1,)
    for index in complement:
        root = domain[index]
        out = [0] * (len(coeffs) + 1)
        for degree, coeff in enumerate(coeffs):
            out[degree] = (out[degree] - root * coeff) % p
            out[degree + 1] = (out[degree + 1] + coeff) % p
        coeffs = tuple(out)
    return coeffs


def hankel_annihilates(
    syn: Sequence[int],
    locator: Sequence[int],
    row_count: int,
    p: int,
) -> bool:
    return all(
        sum(locator[offset] * syn[row + offset] for offset in range(len(locator))) % p
        == 0
        for row in range(row_count)
    )


def support_hankel_records(
    domain: Sequence[int],
    supports: Sequence[dict[str, object]],
    p: int,
) -> list[dict[str, object]]:
    n = len(domain)
    records: list[dict[str, object]] = []
    for support in supports:
        indices = tuple(support["indices"])
        index_set = set(indices)
        complement = tuple(index for index in range(n) if index not in index_set)
        records.append(
            {
                "mask": int(support["mask"]),
                "indices": indices,
                "stabilizer_order": int(support["stabilizer_order"]),
                "complement_indices": complement,
                "locator": locator_coeffs(domain, complement, p),
            }
        )
    return records


def syndrome_difference(
    target_syn: Sequence[int],
    slope: int,
    direction_syn: Sequence[int],
    p: int,
) -> tuple[int, ...]:
    return tuple(
        (target_syn[index] - slope * direction_syn[index]) % p
        for index in range(len(target_syn))
    )


def classify_pair_hankel(
    phi_syn: tuple[int, ...],
    y_syn: tuple[int, ...],
    p: int,
    t: int,
    support_hankels: Sequence[dict[str, object]],
) -> dict[str, list[int]]:
    bad_slopes: list[int] = []
    periodic_slopes: list[int] = []
    primitive_slopes: list[int] = []

    for slope in range(p):
        target_syn = syndrome_difference(y_syn, slope, phi_syn, p)
        has_bad_witness = False
        has_periodic_witness = False

        for support in support_hankels:
            locator = tuple(support["locator"])
            if not hankel_annihilates(target_syn, locator, t, p):
                continue
            if hankel_annihilates(phi_syn, locator, t, p):
                continue

            has_bad_witness = True
            if int(support["stabilizer_order"]) > 1:
                has_periodic_witness = True
                break

        if not has_bad_witness:
            continue
        bad_slopes.append(slope)
        if has_periodic_witness:
            periodic_slopes.append(slope)
        else:
            primitive_slopes.append(slope)

    return {
        "bad_slopes": bad_slopes,
        "periodic_slopes": periodic_slopes,
        "primitive_slopes": primitive_slopes,
    }


def check_erasure_locator_identity(
    p: int,
    domain: Sequence[int],
    k: int,
    supports: Sequence[dict[str, object]],
    support_hankels: Sequence[dict[str, object]],
    support_code: dict[int, set[tuple[int, ...]]],
    max_words: int,
) -> int:
    n = len(domain)
    word_count = p**n
    if word_count > max_words:
        raise ValueError(
            f"would enumerate {word_count} words; raise --max-words to run this case"
        )
    support_by_mask = {int(support["mask"]): support for support in supports}
    check_count = 0
    support_size = len(tuple(supports[0]["indices"]))
    t = support_size - k

    for word in itertools.product(range(p), repeat=n):
        syn = syndrome(word, domain, k, p)
        for support in support_hankels:
            mask = int(support["mask"])
            direct = (
                support_values(word, tuple(support_by_mask[mask]["indices"]))
                in support_code[mask]
            )
            hankel = hankel_annihilates(syn, tuple(support["locator"]), t, p)
            if direct != hankel:
                raise AssertionError(
                    {
                        "kind": "erasure-locator-mismatch",
                        "word": list(word),
                        "support": list(support["indices"]),
                        "complement": list(support["complement_indices"]),
                        "syndrome": list(syn),
                        "locator": list(support["locator"]),
                        "direct": direct,
                        "hankel": hankel,
                    }
                )
            check_count += 1
    return check_count


def compare_pair_classifications(
    p: int,
    domain: Sequence[int],
    k: int,
    a: int,
    supports: Sequence[dict[str, object]],
    support_hankels: Sequence[dict[str, object]],
    support_code: dict[int, set[tuple[int, ...]]],
    max_quotient_pairs: int,
) -> dict[str, object]:
    reps = quotient_representatives(domain, k, p)
    pair_count = len(reps) ** 2
    if pair_count > max_quotient_pairs:
        raise ValueError(
            f"would compare {pair_count} quotient pairs; "
            f"raise --max-quotient-pairs to run this case"
        )

    t = a - k
    syndromes = {word: syndrome(word, domain, k, p) for word in reps}
    primitive_histogram: Counter[int] = Counter()
    periodic_histogram: Counter[int] = Counter()
    bad_histogram: Counter[int] = Counter()
    max_bad = 0
    max_periodic = 0
    max_primitive = 0

    for phi in reps:
        phi_syn = syndromes[phi]
        for y_word in reps:
            direct = classify_pair(phi, y_word, p, supports, support_code)
            hankel = classify_pair_hankel(
                phi_syn,
                syndromes[y_word],
                p,
                t,
                support_hankels,
            )
            for key in ("bad_slopes", "periodic_slopes", "primitive_slopes"):
                if direct[key] != hankel[key]:
                    raise AssertionError(
                        {
                            "kind": "pair-classification-mismatch",
                            "key": key,
                            "phi": list(phi),
                            "Y": list(y_word),
                            "direct": direct[key],
                            "hankel": hankel[key],
                        }
                    )
            bad_count = len(direct["bad_slopes"])
            periodic_count = len(direct["periodic_slopes"])
            primitive_count = len(direct["primitive_slopes"])
            bad_histogram[bad_count] += 1
            periodic_histogram[periodic_count] += 1
            primitive_histogram[primitive_count] += 1
            max_bad = max(max_bad, bad_count)
            max_periodic = max(max_periodic, periodic_count)
            max_primitive = max(max_primitive, primitive_count)

    return {
        "quotient_class_count": len(reps),
        "quotient_pair_count": pair_count,
        "max_bad_slopes": max_bad,
        "max_periodic_budget": max_periodic,
        "max_primitive_remainder": max_primitive,
        "bad_count_histogram": dict(sorted(bad_histogram.items())),
        "periodic_count_histogram": dict(sorted(periodic_histogram.items())),
        "primitive_count_histogram": dict(sorted(primitive_histogram.items())),
    }


def verify_case(
    p: int,
    k: int,
    a: int,
    max_words: int,
    max_quotient_pairs: int,
) -> dict[str, object]:
    n = p - 1
    if not (0 < k < a <= n):
        raise ValueError("case must satisfy 0 < k < a <= p-1")

    domain = cyclic_subgroup(p, n)
    supports = support_records(n, a)
    support_hankels = support_hankel_records(domain, supports, p)
    codewords = rs_codewords(domain, k, p)
    support_code = restriction_sets(codewords, supports)

    erasure_checks = check_erasure_locator_identity(
        p,
        domain,
        k,
        supports,
        support_hankels,
        support_code,
        max_words,
    )
    pair_report = compare_pair_classifications(
        p,
        domain,
        k,
        a,
        supports,
        support_hankels,
        support_code,
        max_quotient_pairs,
    )
    return {
        "status": "PASS",
        "params": {
            "p": p,
            "n": n,
            "k": k,
            "a": a,
            "t": a - k,
            "j": n - a,
            "domain": domain,
            "support_count": len(supports),
            "periodic_support_count": sum(
                1 for support in supports if int(support["stabilizer_order"]) > 1
            ),
        },
        "erasure_locator_checks": erasure_checks,
        **pair_report,
    }


def parse_case(value: str) -> tuple[int, int, int]:
    parts = value.split(",")
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("case must have form p,k,a")
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("case entries must be integers") from exc


def print_summary(results: Sequence[dict[str, object]]) -> None:
    print("M1 exact target Hankel equivalence verifier")
    for result in results:
        params = result["params"]
        print(
            "case "
            f"p={params['p']} n={params['n']} k={params['k']} "
            f"a={params['a']} t={params['t']} j={params['j']}: "
            f"erasure_checks={result['erasure_locator_checks']} "
            f"quotient_pairs={result['quotient_pair_count']} "
            f"max_bad={result['max_bad_slopes']} "
            f"max_periodic={result['max_periodic_budget']} "
            f"max_primitive={result['max_primitive_remainder']}"
        )
    print("PASS")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        action="append",
        type=parse_case,
        dest="cases",
        help="case p,k,a; may be supplied multiple times",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=200_000,
        help="guardrail for exact word enumeration",
    )
    parser.add_argument(
        "--max-quotient-pairs",
        type=int,
        default=1_000_000,
        help="guardrail for exact quotient-pair comparison",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cases = args.cases or [(5, 2, 3), (7, 3, 4)]
    results = [
        verify_case(
            p=p,
            k=k,
            a=a,
            max_words=args.max_words,
            max_quotient_pairs=args.max_quotient_pairs,
        )
        for p, k, a in cases
    ]
    if args.json:
        print(json.dumps({"status": "PASS", "cases": results}, indent=2, sort_keys=True))
    else:
        print_summary(results)


if __name__ == "__main__":
    main()
