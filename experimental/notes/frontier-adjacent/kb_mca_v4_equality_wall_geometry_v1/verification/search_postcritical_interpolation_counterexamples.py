#!/usr/bin/env python3
"""Search small finite fields for exceptional PRCI configurations."""

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



import argparse
import hashlib
import itertools
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "postcritical_interpolation_exhaustive_certificate.json"


def compositions(total: int, parts: int) -> list[tuple[int, ...]]:
    if parts == 1:
        return [(total,)]
    return [
        (first,) + tail
        for first in range(total + 1)
        for tail in compositions(total - first, parts - 1)
    ]


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    data = [[entry % prime for entry in row] for row in matrix]
    rows = len(data)
    columns = len(data[0]) if data else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(rank, rows)
                if data[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        data[rank], data[pivot] = data[pivot], data[rank]
        inverse = pow(data[rank][column], prime - 2, prime)
        data[rank] = [
            inverse * entry % prime for entry in data[rank]
        ]
        for row in range(rank + 1, rows):
            factor = data[row][column]
            if factor:
                data[row] = [
                    (data[row][index] - factor * data[rank][index])
                    % prime
                    for index in range(columns)
                ]
        rank += 1
        if rank == rows:
            break
    return rank


def evaluation_rank(
    prime: int,
    sources: tuple[int, ...],
    selected: tuple[int, ...],
) -> int:
    a = len(sources)
    degree = len(selected) - a + 2
    monomials = compositions(degree, a)
    matrix: list[list[int]] = []
    for subset in itertools.combinations(selected, a - 1):
        coordinates = []
        for source in sources:
            product = 1
            for parameter in subset:
                product = product * (source - parameter) % prime
            coordinates.append(pow(product, prime - 2, prime))
        scale = pow(coordinates[0], prime - 2, prime)
        coordinates = [
            coordinate * scale % prime for coordinate in coordinates
        ]
        matrix.append(
            [
                product_mod(
                    (
                        pow(coordinate, exponent, prime)
                        for coordinate, exponent in zip(
                            coordinates, exponents
                        )
                    ),
                    prime,
                )
                for exponents in monomials
            ]
        )
    return rank_mod(matrix, prime)


def product_mod(values, prime: int) -> int:
    result = 1
    for value in values:
        result = result * value % prime
    return result


def search_case(
    prime: int,
    a: int,
    selected_count: int,
    limit: int | None,
) -> dict[str, object]:
    field = tuple(range(prime))
    point_count = comb(selected_count, a - 1)
    tested = 0
    for sources in itertools.combinations(field, a):
        available = tuple(value for value in field if value not in sources)
        for selected in itertools.combinations(available, selected_count):
            tested += 1
            rank = evaluation_rank(prime, sources, selected)
            if rank != point_count:
                return {
                    "prime": prime,
                    "a": a,
                    "R": selected_count,
                    "tested": tested,
                    "status": "COUNTEREXAMPLE",
                    "rank": rank,
                    "point_count": point_count,
                    "sources": sources,
                    "selected": selected,
                }
            if limit is not None and tested >= limit:
                return {
                    "prime": prime,
                    "a": a,
                    "R": selected_count,
                    "tested": tested,
                    "status": "NO_COUNTEREXAMPLE_WITHIN_LIMIT",
                    "point_count": point_count,
                }
    return {
        "prime": prime,
        "a": a,
        "R": selected_count,
        "tested": tested,
        "status": "EXHAUSTIVE_NO_COUNTEREXAMPLE",
        "point_count": point_count,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()
    cases = [
        (7, 3, 4),
        (11, 3, 5),
        (11, 4, 6),
        (11, 4, 7),
        (13, 5, 8),
    ]
    results = [
        search_case(prime, a, selected_count, args.limit)
        for prime, a, selected_count in cases
    ]
    data = {
        "status": (
            "FINITE_EXHAUSTIVE_EVIDENCE_ONLY_"
            "KPRCI_OPEN_UNIVERSAL_FALSE"
        ),
        "cases": results,
        "total_configurations": sum(row["tested"] for row in results),
        "claim": {
            "universal_postcritical_surjectivity": "FALSE",
            "koalabear_postcritical_surjectivity": "OPEN",
            "selected_record_semantic_or_interpolation": "OPEN",
            "known_block_line_planted_branch": "PROVED_SEPARATELY",
            "finite_counterexample": "NONE_IN_PRINTED_CASES",
        },
    }
    canonical = json.dumps(
        data, sort_keys=True, separators=(",", ":")
    ).encode()
    data["payload_sha256"] = hashlib.sha256(canonical).hexdigest()

    def validate(candidate: dict[str, object]) -> None:
        expected = {
            (7, 3, 4): 35,
            (11, 3, 5): 9_240,
            (11, 4, 6): 2_310,
            (11, 4, 7): 330,
            (13, 5, 8): 1_287,
        }
        require(
            candidate['total_configurations'] == 13202,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/search_postcritical_interpolation_counterexamples.py:198',
        )
        rows = candidate["cases"]
        require(
            len(rows) == len(expected),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/search_postcritical_interpolation_counterexamples.py:200',
        )
        for row in rows:
            key = (row["prime"], row["a"], row["R"])
            require(
                key in expected,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/search_postcritical_interpolation_counterexamples.py:203',
            )
            require(
                row['status'] == 'EXHAUSTIVE_NO_COUNTEREXAMPLE',
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/search_postcritical_interpolation_counterexamples.py:204',
            )
            require(
                row['tested'] == expected[key],
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/search_postcritical_interpolation_counterexamples.py:205',
            )

    if args.limit is None:
        validate(data)
        if args.emit:
            CERTIFICATE.write_text(
                json.dumps(data, indent=2, sort_keys=True) + "\n"
            )
        if args.check:
            require(
                json.loads(CERTIFICATE.read_text()) == data,
                'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/search_postcritical_interpolation_counterexamples.py:214',
            )
        if args.tamper_selftest:
            tampered = json.loads(json.dumps(data))
            tampered["cases"][0]["status"] = "COUNTEREXAMPLE"
            try:
                validate(tampered)
            except VerificationError:
                pass
            else:
                raise VerificationError("tamper was not rejected")

    print(json.dumps(data, indent=2))
    return int(any(row["status"] == "COUNTEREXAMPLE" for row in results))


if __name__ == "__main__":
    raise SystemExit(main())
