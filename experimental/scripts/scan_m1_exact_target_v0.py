#!/usr/bin/env python3
"""Exact tiny-field scanner for the M1-v0 primitive slope target.

Proof status: EXPERIMENTAL / FALSIFICATION-FIRST.

The scanner enumerates quotient-normal endpoint pairs (phi,Y) in F^H/C for a
small cyclic domain H, computes the finite noncontained slope ledger

    A + lambda phi = Y on an a-support S,

and splits each bad slope into the exact support-stabilizer budget and the
primitive remainder from experimental/notes/m1/m1_exact_target_v0.md.

This is not evidence by curve fitting.  It is a counterexample search for the
normalized object in the conjecture: many primitive slopes after quotient
gauges, contained branches, and periodic support packets have been removed.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from typing import Iterable, Sequence


def factorint(value: int) -> dict[int, int]:
    factors: dict[int, int] = {}
    divisor = 2
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    return factors


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value in (2, 3):
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def primitive_root(p: int) -> int:
    if p == 2:
        return 1
    phi = p - 1
    factors = factorint(phi).keys()
    for candidate in range(2, p):
        if all(pow(candidate, phi // factor, p) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for p={p}")


def cyclic_subgroup(p: int, n: int) -> list[int]:
    if (p - 1) % n != 0:
        raise ValueError(f"n={n} does not divide p-1={p - 1}")
    generator = pow(primitive_root(p), (p - 1) // n, p)
    out: list[int] = []
    current = 1
    for _ in range(n):
        out.append(current)
        current = (current * generator) % p
    return out


def eval_poly(coeffs: Sequence[int], x_value: int, p: int) -> int:
    out = 0
    for coeff in reversed(coeffs):
        out = (out * x_value + coeff) % p
    return out


def poly_values(coeffs: Sequence[int], domain: Sequence[int], p: int) -> tuple[int, ...]:
    return tuple(eval_poly(coeffs, x_value, p) for x_value in domain)


def rs_codewords(domain: Sequence[int], dimension: int, p: int) -> list[tuple[int, ...]]:
    if dimension < 0 or dimension > len(domain):
        raise ValueError("RS dimension must lie between 0 and n")
    return [
        poly_values(coeffs, domain, p)
        for coeffs in itertools.product(range(p), repeat=dimension)
    ]


def generator_matrix(domain: Sequence[int], k: int, p: int) -> list[list[int]]:
    return [[pow(x_value, degree, p) for x_value in domain] for degree in range(k)]


def matrix_rref(matrix: list[list[int]], p: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix]
    pivot_columns: list[int] = []
    pivot_row = 0
    column_count = len(rows[0]) if rows else 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column] % p),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column] % p, -1, p)
        rows[pivot_row] = [(value * inverse) % p for value in rows[pivot_row]]
        for row_index, row in enumerate(rows):
            if row_index == pivot_row:
                continue
            factor = row[column] % p
            if factor:
                rows[row_index] = [
                    (entry - factor * pivot_entry) % p
                    for entry, pivot_entry in zip(row, rows[pivot_row], strict=True)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivot_columns


def quotient_representatives(domain: Sequence[int], k: int, p: int) -> list[tuple[int, ...]]:
    """Return one linear-complement representative for every class in F^H/C."""
    rref, pivots = matrix_rref(generator_matrix(domain, k, p), p)
    if len(pivots) != k:
        raise ValueError("generator matrix did not have full row rank")
    pivot_set = set(pivots)
    free_columns = [index for index in range(len(domain)) if index not in pivot_set]
    reps: list[tuple[int, ...]] = []
    for values in itertools.product(range(p), repeat=len(free_columns)):
        vector = [0] * len(domain)
        for index, value in zip(free_columns, values, strict=True):
            vector[index] = value
        reps.append(tuple(vector))

    # Sanity check: zeroing the pivot coordinates defines a complement.
    for row in rref:
        if all(row[pivot] == 0 for pivot in pivots):
            raise AssertionError("unexpected row in quotient complement")
    return reps


def mask_from_indices(indices: Iterable[int]) -> int:
    mask = 0
    for index in indices:
        mask |= 1 << index
    return mask


def mask_indices(mask: int, n: int) -> list[int]:
    return [index for index in range(n) if mask & (1 << index)]


def rotate_mask(mask: int, shift: int, n: int) -> int:
    shift %= n
    if shift == 0:
        return mask
    full = (1 << n) - 1
    return ((mask << shift) | (mask >> (n - shift))) & full


def stabilizer_order(mask: int, n: int) -> int:
    return sum(1 for shift in range(n) if rotate_mask(mask, shift, n) == mask)


def support_records(n: int, a: int) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for indices in itertools.combinations(range(n), a):
        mask = mask_from_indices(indices)
        records.append(
            {
                "mask": mask,
                "indices": tuple(indices),
                "stabilizer_order": stabilizer_order(mask, n),
            }
        )
    return records


def restriction_sets(
    codewords: Sequence[tuple[int, ...]],
    supports: Sequence[dict[str, object]],
) -> dict[int, set[tuple[int, ...]]]:
    out: dict[int, set[tuple[int, ...]]] = {}
    for support in supports:
        mask = int(support["mask"])
        indices = tuple(support["indices"])
        out[mask] = {
            tuple(codeword[index] for index in indices)
            for codeword in codewords
        }
    return out


def support_values(word: Sequence[int], indices: Sequence[int]) -> tuple[int, ...]:
    return tuple(word[index] for index in indices)


def word_difference(
    target: Sequence[int],
    scalar: int,
    direction: Sequence[int],
    p: int,
) -> tuple[int, ...]:
    return tuple(
        (target[index] - scalar * direction[index]) % p
        for index in range(len(target))
    )


def classify_pair(
    phi: tuple[int, ...],
    y_word: tuple[int, ...],
    p: int,
    supports: Sequence[dict[str, object]],
    support_code: dict[int, set[tuple[int, ...]]],
) -> dict[str, object]:
    contained: dict[int, bool] = {}
    for support in supports:
        mask = int(support["mask"])
        indices = tuple(support["indices"])
        contained[mask] = (
            support_values(phi, indices) in support_code[mask]
            and support_values(y_word, indices) in support_code[mask]
        )

    bad_slopes: list[int] = []
    periodic_slopes: list[int] = []
    primitive_slopes: list[int] = []
    periodic_witnesses: dict[int, int] = {}
    primitive_witnesses: dict[int, int] = {}

    for slope in range(p):
        target = word_difference(y_word, slope, phi, p)
        first_primitive_mask: int | None = None
        has_bad_witness = False
        has_periodic_witness = False

        for support in supports:
            mask = int(support["mask"])
            if contained[mask]:
                continue
            indices = tuple(support["indices"])
            target_restriction = support_values(target, indices)
            if target_restriction not in support_code[mask]:
                continue

            has_bad_witness = True
            if int(support["stabilizer_order"]) > 1:
                has_periodic_witness = True
                periodic_witnesses[slope] = mask
                break
            if first_primitive_mask is None:
                first_primitive_mask = mask

        if not has_bad_witness:
            continue
        bad_slopes.append(slope)
        if has_periodic_witness:
            periodic_slopes.append(slope)
        else:
            primitive_slopes.append(slope)
            if first_primitive_mask is None:
                raise AssertionError("primitive slope without primitive witness")
            primitive_witnesses[slope] = first_primitive_mask

    if len(bad_slopes) != len(periodic_slopes) + len(primitive_slopes):
        raise AssertionError("bad slopes do not split into periodic and primitive")

    return {
        "bad_slopes": bad_slopes,
        "periodic_slopes": periodic_slopes,
        "primitive_slopes": primitive_slopes,
        "periodic_witnesses": periodic_witnesses,
        "primitive_witnesses": primitive_witnesses,
    }


def monic_polynomials(degree: int, p: int) -> Iterable[tuple[int, ...]]:
    if degree == 0:
        yield (1,)
        return
    for lower in itertools.product(range(p), repeat=degree):
        yield tuple(lower) + (1,)


def root_free_denominators(
    domain: Sequence[int],
    max_degree: int,
    p: int,
) -> dict[int, list[tuple[int, ...]]]:
    out: dict[int, list[tuple[int, ...]]] = {}
    for degree in range(max_degree + 1):
        denoms = []
        for coeffs in monic_polynomials(degree, p):
            if all(eval_poly(coeffs, x_value, p) != 0 for x_value in domain):
                denoms.append(coeffs)
        out[degree] = denoms
    return out


def endpoint_denominator_profile(
    word: Sequence[int],
    domain: Sequence[int],
    k: int,
    p: int,
    code_sets_by_dimension: dict[int, set[tuple[int, ...]]],
    denominators_by_degree: dict[int, list[tuple[int, ...]]],
) -> list[dict[str, int]]:
    records: list[dict[str, int]] = []
    for degree, denominators in denominators_by_degree.items():
        code_set = code_sets_by_dimension[k + degree]
        count = 0
        for denominator in denominators:
            product_word = tuple(
                (eval_poly(denominator, x_value, p) * value) % p
                for x_value, value in zip(domain, word, strict=True)
            )
            if product_word in code_set:
                count += 1
        records.append(
            {
                "degree": degree,
                "root_free_projective_denominators": count,
                "root_free_projective_candidates": len(denominators),
            }
        )
    return records


def witness_record(
    slope: int,
    mask: int,
    n: int,
    domain: Sequence[int],
) -> dict[str, object]:
    indices = mask_indices(mask, n)
    return {
        "lambda": slope,
        "support_indices": indices,
        "support_values": [domain[index] for index in indices],
        "stabilizer_order": stabilizer_order(mask, n),
    }


def example_record(
    pair_index: int,
    phi_index: int,
    y_index: int,
    phi: tuple[int, ...],
    y_word: tuple[int, ...],
    pair_result: dict[str, object],
    domain: Sequence[int],
    k: int,
    p: int,
    code_sets_by_dimension: dict[int, set[tuple[int, ...]]],
    denominators_by_degree: dict[int, list[tuple[int, ...]]],
) -> dict[str, object]:
    n = len(domain)
    primitive_witnesses = pair_result["primitive_witnesses"]
    periodic_witnesses = pair_result["periodic_witnesses"]
    return {
        "pair_index": pair_index,
        "phi_index": phi_index,
        "Y_index": y_index,
        "phi": list(phi),
        "Y": list(y_word),
        "bad_slopes": list(pair_result["bad_slopes"]),
        "periodic_slopes": list(pair_result["periodic_slopes"]),
        "primitive_slopes": list(pair_result["primitive_slopes"]),
        "primitive_witnesses": [
            witness_record(slope, primitive_witnesses[slope], n, domain)
            for slope in pair_result["primitive_slopes"]
        ],
        "periodic_witnesses": [
            witness_record(slope, periodic_witnesses[slope], n, domain)
            for slope in pair_result["periodic_slopes"]
        ],
        "phi_endpoint_denominators": endpoint_denominator_profile(
            phi,
            domain,
            k,
            p,
            code_sets_by_dimension,
            denominators_by_degree,
        ),
        "Y_endpoint_denominators": endpoint_denominator_profile(
            y_word,
            domain,
            k,
            p,
            code_sets_by_dimension,
            denominators_by_degree,
        ),
    }


def scan_case(
    p: int,
    n: int,
    k: int,
    a: int,
    alert_power: float,
    max_quotient_pairs: int,
    max_codewords: int,
    max_examples: int,
) -> dict[str, object]:
    if not is_prime(p):
        raise ValueError("--p must be prime")
    if not (0 < k < a <= n):
        raise ValueError("parameters must satisfy 0 < k < a <= n")

    quotient_class_count = p ** (n - k)
    quotient_pair_count = quotient_class_count ** 2
    if quotient_pair_count > max_quotient_pairs:
        raise ValueError(
            f"would scan {quotient_pair_count} quotient pairs; "
            f"raise --max-quotient-pairs to run this exact case"
        )
    if p ** k > max_codewords:
        raise ValueError(
            f"would build {p ** k} RS codewords; "
            f"raise --max-codewords to run this exact case"
        )
    if p ** n > max_codewords:
        raise ValueError(
            f"endpoint denominator profiles would build {p ** n} length-n "
            f"codewords; raise --max-codewords to run this exact case"
        )

    domain = cyclic_subgroup(p, n)
    codewords = rs_codewords(domain, k, p)
    reps = quotient_representatives(domain, k, p)
    if len(reps) != quotient_class_count:
        raise AssertionError("unexpected quotient representative count")

    code_sets_by_dimension = {
        dimension: set(rs_codewords(domain, dimension, p))
        for dimension in range(k, n + 1)
    }
    supports = support_records(n, a)
    support_code = restriction_sets(codewords, supports)

    denominators_by_degree = root_free_denominators(domain, n - k, p)
    bad_histogram: Counter[int] = Counter()
    periodic_histogram: Counter[int] = Counter()
    primitive_histogram: Counter[int] = Counter()
    max_bad = 0
    max_periodic = 0
    max_primitive = 0
    examples: list[dict[str, object]] = []

    pair_index = 0
    for phi_index, phi in enumerate(reps):
        for y_index, y_word in enumerate(reps):
            pair_result = classify_pair(phi, y_word, p, supports, support_code)
            bad_count = len(pair_result["bad_slopes"])
            periodic_count = len(pair_result["periodic_slopes"])
            primitive_count = len(pair_result["primitive_slopes"])
            bad_histogram[bad_count] += 1
            periodic_histogram[periodic_count] += 1
            primitive_histogram[primitive_count] += 1
            max_bad = max(max_bad, bad_count)
            max_periodic = max(max_periodic, periodic_count)
            if primitive_count > max_primitive:
                max_primitive = primitive_count
                examples = []
            if primitive_count == max_primitive and len(examples) < max_examples:
                examples.append(
                    example_record(
                        pair_index,
                        phi_index,
                        y_index,
                        phi,
                        y_word,
                        pair_result,
                        domain,
                        k,
                        p,
                        code_sets_by_dimension,
                        denominators_by_degree,
                    )
                )
            pair_index += 1

    threshold = n ** alert_power
    primitive_alert = max_primitive > threshold
    status = (
        "EXPERIMENTAL/M1_V0_PRIMITIVE_ALERT"
        if primitive_alert
        else "EXPERIMENTAL/M1_V0_NO_PRIMITIVE_ALERT"
    )
    return {
        "status": status,
        "params": {
            "p": p,
            "n": n,
            "k": k,
            "a": a,
            "t": a - k,
            "domain": domain,
            "quotient_dimension": n - k,
            "quotient_class_count": len(reps),
            "quotient_pair_count": quotient_pair_count,
            "support_count": len(supports),
            "periodic_support_count": sum(
                1 for support in supports if int(support["stabilizer_order"]) > 1
            ),
        },
        "max_bad_slopes": max_bad,
        "max_periodic_budget": max_periodic,
        "max_primitive_remainder": max_primitive,
        "primitive_alert_power": alert_power,
        "primitive_alert_threshold": threshold,
        "primitive_alert": primitive_alert,
        "bad_count_histogram": dict(sorted(bad_histogram.items())),
        "periodic_count_histogram": dict(sorted(periodic_histogram.items())),
        "primitive_count_histogram": dict(sorted(primitive_histogram.items())),
        "root_free_denominator_candidates_by_degree": {
            str(degree): len(values)
            for degree, values in sorted(denominators_by_degree.items())
        },
        "max_primitive_examples": examples,
    }


def print_summary(result: dict[str, object]) -> None:
    params = result["params"]
    print("M1 exact target v0 quotient-normal scan")
    print(f"status: {result['status']}")
    print(
        "parameters: "
        f"p={params['p']} n={params['n']} k={params['k']} "
        f"a={params['a']} t={params['t']}"
    )
    print(
        "enumeration: "
        f"{params['quotient_pair_count']} quotient pairs, "
        f"{params['support_count']} supports "
        f"({params['periodic_support_count']} periodic)"
    )
    print(
        "maxima: "
        f"bad={result['max_bad_slopes']} "
        f"periodic={result['max_periodic_budget']} "
        f"primitive={result['max_primitive_remainder']}"
    )
    print(
        "primitive alert: "
        f"{result['primitive_alert']} "
        f"(threshold n^{result['primitive_alert_power']}="
        f"{result['primitive_alert_threshold']:.6g})"
    )
    print(f"primitive histogram: {result['primitive_count_histogram']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--p", type=int, default=5, help="prime field size")
    parser.add_argument(
        "--n",
        type=int,
        default=None,
        help="cyclic subgroup order, default p-1",
    )
    parser.add_argument("--k", type=int, default=2, help="RS dimension")
    parser.add_argument("--a", type=int, default=3, help="agreement support size")
    parser.add_argument(
        "--alert-power",
        type=float,
        default=2.0,
        help="flag primitive packets larger than n^alert_power",
    )
    parser.add_argument(
        "--max-quotient-pairs",
        type=int,
        default=1_000_000,
        help="guardrail for exact quotient-pair enumeration",
    )
    parser.add_argument(
        "--max-codewords",
        type=int,
        default=1_000_000,
        help="guardrail for exact RS codeword tables",
    )
    parser.add_argument(
        "--max-examples",
        type=int,
        default=3,
        help="number of max-primitive examples retained",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    parser.add_argument("--output", help="write JSON output to this path")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n = args.p - 1 if args.n is None else args.n
    result = scan_case(
        p=args.p,
        n=n,
        k=args.k,
        a=args.a,
        alert_power=args.alert_power,
        max_quotient_pairs=args.max_quotient_pairs,
        max_codewords=args.max_codewords,
        max_examples=args.max_examples,
    )
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2, sort_keys=True)
            handle.write("\n")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_summary(result)


if __name__ == "__main__":
    main()
