#!/usr/bin/env python3
"""Exact characteristic-13 counterexample census for universal PRCI."""

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
from collections import Counter
from pathlib import Path

from search_postcritical_interpolation_counterexamples import (
    evaluation_rank,
)


ROOT = Path(__file__).resolve().parent
CERTIFICATE = ROOT / "postcritical_characteristic13_guardrail.json"


def locator_coefficients(
    roots: tuple[int, ...], prime: int
) -> list[int]:
    coefficients = [1]
    for root in roots:
        product = [0] * (len(coefficients) + 1)
        for index, coefficient in enumerate(coefficients):
            product[index] = (
                product[index] - root * coefficient
            ) % prime
            product[index + 1] = (
                product[index + 1] + coefficient
            ) % prime
        coefficients = product
    return coefficients


def evaluate_polynomial(
    coefficients: list[int], value: int, prime: int
) -> int:
    return sum(
        coefficient * pow(value, index, prime)
        for index, coefficient in enumerate(coefficients)
    ) % prime


def block_line_identity(
    prime: int,
    sources: tuple[int, ...],
    first: tuple[int, ...],
    second: tuple[int, ...],
) -> int | None:
    source_locator = locator_coefficients(sources, prime)
    first_locator = locator_coefficients(first, prime)
    second_locator = locator_coefficients(second, prime)
    scalar = (
        evaluate_polynomial(first_locator, sources[0], prime)
        * pow(
            evaluate_polynomial(
                second_locator, sources[0], prime
            ),
            prime - 2,
            prime,
        )
    ) % prime
    expected = [
        (1 - scalar) * coefficient % prime
        for coefficient in source_locator
    ]
    actual = [
        (left - scalar * right) % prime
        for left, right in zip(first_locator, second_locator)
    ]
    return scalar if actual == expected else None


def complementary_block_identities(
    prime: int,
    sources: tuple[int, ...],
    selected: tuple[int, ...],
) -> list[dict[str, object]]:
    first_parameter = selected[0]
    identities = []
    for tail in itertools.combinations(selected[1:], len(sources) - 1):
        first = (first_parameter,) + tail
        second = tuple(sorted(set(selected) - set(first)))
        scalar = block_line_identity(
            prime, sources, first, second
        )
        if scalar is not None:
            identities.append(
                {
                    "first_block": list(first),
                    "second_block": list(second),
                    "scalar": scalar,
                }
            )
    return identities


def normalized_census() -> dict[str, object]:
    prime = 13
    field = set(range(prime))
    point_count = 56
    rank_counts: dict[int, int] = {}
    first_examples: dict[int, dict[str, object]] = {}
    defect_block_pair_table: Counter[tuple[int, int]] = Counter()
    tested = 0

    # A configuration uses 4 source values and 8 selected values, leaving
    # one field element unused. Translation moves that element to zero.
    for sources in itertools.combinations(range(1, prime), 4):
        selected = tuple(sorted(field - set(sources) - {0}))
        rank = evaluation_rank(prime, sources, selected)
        defect = point_count - rank
        identities = complementary_block_identities(
            prime, sources, selected
        )
        defect_block_pair_table[(defect, len(identities))] += 1
        require(
            defect == len(identities),
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:121',
        )
        tested += 1
        if rank != point_count:
            rank_counts[rank] = rank_counts.get(rank, 0) + 1
            first_examples.setdefault(
                rank,
                {
                    "sources": list(sources),
                    "selected": list(selected),
                    "rank": rank,
                    "defect": point_count - rank,
                    "coincident_complementary_block_pairs": identities,
                },
            )

    bad_normalized = sum(rank_counts.values())
    return {
        "prime": prime,
        "a": 4,
        "R": 8,
        "postcritical_degree": 6,
        "point_count": point_count,
        "normalization": "unique unused field value translated to zero",
        "normalized_configurations": tested,
        "normalized_bad_count": bad_normalized,
        "normalized_rank_counts": {
            str(rank): count for rank, count in sorted(rank_counts.items())
        },
        "all_configurations": prime * tested,
        "all_bad_count": prime * bad_normalized,
        "all_rank_counts": {
            str(rank): prime * count
            for rank, count in sorted(rank_counts.items())
        },
        "first_examples": {
            str(rank): row
            for rank, row in sorted(first_examples.items())
        },
        "defect_block_pair_table": {
            f"defect_{defect}_pairs_{pairs}": count
            for (defect, pairs), count in sorted(
                defect_block_pair_table.items()
            )
        },
        "unaccounted_postcritical_defects": 0,
    }


def characteristic_comparison() -> list[dict[str, object]]:
    sources = (0, 1, 2, 5)
    selected = (3, 4, 6, 7, 8, 9, 11, 12)
    return [
        {
            "prime": prime,
            "rank": evaluation_rank(
                prime, sources, selected
            ),
            "point_count": 56,
        }
        for prime in (13, 17, 1_000_003)
    ]


def explicit_larger_characteristic_exceptions() -> list[dict[str, object]]:
    cases = [
        (
            17,
            (1, 3, 10, 15),
            (0, 2, 4, 8, 9, 11, 12, 14),
        ),
        (
            19,
            (5, 13, 15, 18),
            (0, 1, 4, 6, 7, 10, 11, 12),
        ),
        (
            23,
            (6, 8, 9, 10),
            (2, 11, 14, 16, 17, 19, 20, 21),
        ),
    ]
    result = []
    for prime, sources, selected in cases:
        rank = evaluation_rank(prime, sources, selected)
        identities = complementary_block_identities(
            prime, sources, selected
        )
        result.append(
            {
                "prime": prime,
                "sources": list(sources),
                "selected": list(selected),
                "rank": rank,
                "point_count": 56,
                "postcritical_defect": 56 - rank,
                "coincident_complementary_block_pairs": identities,
            }
        )
    return result


def payload() -> dict[str, object]:
    result = {
        "status": (
            "UNIVERSAL_PRCI_FALSE_KOALABEAR_SPECIALIZATION_OPEN"
        ),
        "affine_normalized_exhaustive_census": normalized_census(),
        "same_integer_configuration_by_characteristic": (
            characteristic_comparison()
        ),
        "larger_characteristic_exceptions": (
            explicit_larger_characteristic_exceptions()
        ),
        "claims": {
            "universal_all_field_PRCI": "FALSE",
            "characteristic_13_counterexample": "PROVED",
            "known_counterexamples_are_block_line_planted": "PROVED",
            "koalabear_semantic_or_interpolation": "OPEN",
            "cap_68": "OPEN",
            "active_owner": "NONE",
        },
    }
    canonical = json.dumps(
        result, sort_keys=True, separators=(",", ":")
    ).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


def validate(data: dict[str, object]) -> None:
    census = data["affine_normalized_exhaustive_census"]
    require(
        census['normalized_configurations'] == 495,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:252',
    )
    require(
        census['normalized_bad_count'] == 21,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:253',
    )
    require(
        census['normalized_rank_counts'] == {'54': 3, '55': 18},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:254',
    )
    require(
        census['all_configurations'] == 6435,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:255',
    )
    require(
        census['all_bad_count'] == 273,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:256',
    )
    require(
        census['all_rank_counts'] == {'54': 39, '55': 234},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:257',
    )
    require(
        census['defect_block_pair_table'] == {'defect_0_pairs_0': 474, 'defect_1_pairs_1': 18, 'defect_2_pairs_2': 3},
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:258',
    )
    require(
        census['unaccounted_postcritical_defects'] == 0,
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:263',
    )

    comparison = data["same_integer_configuration_by_characteristic"]
    require(
        [row['prime'] for row in comparison] == [13, 17, 1000003],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:266',
    )
    require(
        [row['rank'] for row in comparison] == [55, 56, 56],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:271',
    )
    require(
        all((row['point_count'] == 56 for row in comparison)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:272',
    )

    larger = data["larger_characteristic_exceptions"]
    require(
        [row['prime'] for row in larger] == [17, 19, 23],
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:275',
    )
    require(
        all((row['rank'] == 55 and row['postcritical_defect'] == 1 and (len(row['coincident_complementary_block_pairs']) == 1) for row in larger)),
        'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:276',
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    data = payload()
    validate(data)
    if args.emit:
        CERTIFICATE.write_text(
            json.dumps(data, indent=2, sort_keys=True) + "\n"
        )
    if args.check:
        require(
            json.loads(CERTIFICATE.read_text()) == data,
            'verification condition failed at experimental/notes/frontier-adjacent/kb_mca_v4_equality_wall_geometry_v1/verification/verify_postcritical_characteristic13_guardrail.py:298',
        )
    if args.tamper_selftest:
        tampered = json.loads(json.dumps(data))
        tampered["affine_normalized_exhaustive_census"][
            "normalized_bad_count"
        ] = 20
        try:
            validate(tampered)
        except VerificationError:
            pass
        else:
            raise VerificationError("tamper was not rejected")

    print("characteristic-13 normalized exhaustive census: PASS")
    print("block-line planted-defect accounting: PASS")
    print("cross-characteristic guardrail: PASS")
    print(f"payload_sha256={data['payload_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
