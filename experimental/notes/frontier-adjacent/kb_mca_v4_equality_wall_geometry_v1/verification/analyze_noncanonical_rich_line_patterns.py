#!/usr/bin/env python3
"""Extract exact root-set patterns on the richest finite noncanonical lines."""

from __future__ import annotations
class VerificationError(RuntimeError):
    """Raised when an exact verifier condition fails."""


def require(condition, message):
    if not condition:
        raise VerificationError(str(message))


if not __debug__:
    raise RuntimeError(
        "Verifier refuses optimized execution; rerun without Python -O."
    )



import itertools
import json
from collections import Counter, defaultdict

import sympy

from verify_postcritical_block_line_relation_space import (
    line_key,
    rref,
    vertex_coordinates,
)


def correspondence_factorization(
    prime: int,
    sources: tuple[int, ...],
    point_rows: list[list[int]],
) -> dict[str, object]:
    """Test the exact bivariate correspondence for low-bidegree factors."""
    t_symbol, lambda_symbol = sympy.symbols("T lambda")
    u = point_rows[0]
    v = [
        (right - left) % prime
        for left, right in zip(point_rows[0], point_rows[1])
    ]
    source_product = sympy.prod(t_symbol - source for source in sources)
    expression = 0
    for index, source in enumerate(sources):
        denominator = 1
        for other in sources:
            if other != source:
                denominator = denominator * (source - other) % prime
        lagrange = (
            source_product
            / (t_symbol - source)
            * pow(denominator, prime - 2, prime)
        )
        line_cofactor = sympy.prod(
            (u[position] + lambda_symbol * v[position])
            for position in range(len(sources))
            if position != index
        )
        expression += lagrange * line_cofactor
    polynomial = sympy.Poly(
        sympy.cancel(expression),
        t_symbol,
        lambda_symbol,
        modulus=prime,
    )

    projective_coefficients = []
    for coefficients in itertools.product(range(prime), repeat=4):
        first = next(
            (value for value in coefficients if value != 0),
            None,
        )
        if first != 1:
            continue
        projective_coefficients.append(coefficients)

    bilinear_factors = []
    for c00, c10, c01, c11 in projective_coefficients:
        if c10 == c11 == 0 or c01 == c11 == 0:
            continue
        candidate = sympy.Poly(
            c00
            + c10 * t_symbol
            + c01 * lambda_symbol
            + c11 * t_symbol * lambda_symbol,
            t_symbol,
            lambda_symbol,
            modulus=prime,
        )
        quotient, remainder = polynomial.div(candidate)
        if remainder.is_zero:
            bilinear_factors.append(
                {
                    "factor": str(candidate.as_expr()),
                    "quotient_t_degree": int(quotient.degree(t_symbol)),
                    "quotient_lambda_degree": int(
                        quotient.degree(lambda_symbol)
                    ),
                }
            )

    return {
        "t_degree": int(polynomial.degree(t_symbol)),
        "lambda_degree": int(polynomial.degree(lambda_symbol)),
        "bilinear_factors": bilinear_factors,
    }


def line_patterns(
    prime: int,
    sources: tuple[int, ...],
    selected: tuple[int, ...],
) -> list[dict[str, object]]:
    labels = list(itertools.combinations(selected, len(sources) - 1))
    points = [
        vertex_coordinates(prime, sources, label) for label in labels
    ]
    canonical = {
        line_key(prime, sources, block)
        for block in itertools.combinations(selected, len(sources))
    }
    line_points: dict[tuple[tuple[int, ...], ...], set[int]] = defaultdict(set)
    for left, right in itertools.combinations(range(len(points)), 2):
        reduced, pivots = rref([points[left], points[right]], prime)
        require(
            len(pivots) == 2,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/analyze_noncanonical_rich_line_patterns.py:114',
        )
        key = tuple(tuple(row) for row in reduced[:2])
        line_points[key].update((left, right))

    rows = []
    for key, indices in line_points.items():
        if key in canonical or len(indices) < 3:
            continue
        blocks = [labels[index] for index in sorted(indices)]
        point_rows = [points[index] for index in sorted(indices)]
        common = set(blocks[0]).intersection(*map(set, blocks[1:]))
        pair_intersections = Counter(
            len(set(left) & set(right))
            for left, right in itertools.combinations(blocks, 2)
        )
        anchor_template_counts = []
        for left, right in itertools.combinations(blocks, 2):
            anchor_union = set(left) | set(right)
            anchor_template_counts.append(
                sum(set(block) <= anchor_union for block in blocks)
            )
        rows.append(
            {
                "size": len(blocks),
                "blocks": [list(block) for block in blocks],
                "common_roots": sorted(common),
                "union_size": len(set().union(*map(set, blocks))),
                "pair_intersection_histogram": {
                    str(value): count
                    for value, count in sorted(pair_intersections.items())
                },
                "maximum_two_anchor_template_count": max(
                    anchor_template_counts, default=0
                ),
                "_point_rows": point_rows,
            }
        )
    return rows


def main() -> None:
    prime = 13
    field = set(range(prime))
    maximum = 0
    raw_examples: list[
        tuple[tuple[int, ...], dict[str, object], list[list[int]]]
    ] = []
    size_histogram: Counter[int] = Counter()
    for sources in itertools.combinations(range(prime), 4):
        selected = tuple(sorted(field - set(sources)))
        for row in line_patterns(prime, sources, selected):
            size = int(row["size"])
            size_histogram[size] += 1
            point_rows = row.pop("_point_rows")
            if size > maximum:
                maximum = size
                raw_examples = [(sources, row, point_rows)]
            elif size == maximum and len(raw_examples) < 20:
                raw_examples.append((sources, row, point_rows))

    examples = []
    for sources, row, point_rows in raw_examples:
        examples.append(
            {
                "sources": list(sources),
                **row,
                "correspondence_factors": correspondence_factorization(
                    prime,
                    sources,
                    point_rows,
                ),
            }
        )

    print(
        json.dumps(
            {
                "prime": prime,
                "a": 4,
                "R": 9,
                "maximum_noncanonical_line_size": maximum,
                "noncanonical_line_size_histogram": {
                    str(size): count
                    for size, count in sorted(size_histogram.items())
                },
                "maximum_examples": examples,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
