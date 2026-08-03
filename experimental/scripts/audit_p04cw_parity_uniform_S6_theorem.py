#!/usr/bin/env python3
"""Independent scalar audit of the P04cw parity uniform S6 theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from pathlib import Path

import sympy


ELL = 11
HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "certificates" / "l1-exact-five-parity-s6"


def load(name: str) -> dict[str, object]:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def audit_factorizations(artifact: dict[str, object]) -> None:
    rows = artifact["norm_factorizations"]
    rendered = json.dumps(
        rows, sort_keys=True, separators=(",", ":")
    ).encode("ascii")
    assert hashlib.sha256(rendered).hexdigest() == artifact[
        "norm_factorization_sha256"
    ]
    candidate_primes = set()
    for row in rows:
        integer = int(row["integer"])
        factors = [(int(p), int(e)) for p, e in row["factors"]]
        assert math.prod(p**e for p, e in factors) == integer
        assert all(sympy.isprime(p) for p, _ in factors)
        candidate_primes.update(p for p, _ in factors if p % ELL == 1)
    assert candidate_primes == set(
        artifact["candidate_primes_congruent_to_one_mod_11"]
    )


def canonical_translation(roots: tuple[int, ...]) -> tuple[int, ...]:
    return min(
        tuple(sorted((root + shift) % ELL for root in roots))
        for shift in range(ELL)
    )


def root_classes(size: int) -> list[tuple[int, ...]]:
    return sorted(
        {
            canonical_translation(roots)
            for roots in itertools.combinations(range(ELL), size)
        }
    )


FOUR_ROOTS = root_classes(4)
FIVE_ROOTS = root_classes(5)
TRIPLE_ROOTS = root_classes(3)
assert (len(FOUR_ROOTS), len(FIVE_ROOTS), len(TRIPLE_ROOTS)) == (30, 42, 15)


def order_eleven_root(prime: int) -> int:
    exponent = (prime - 1) // ELL
    base = 2
    while True:
        root = pow(base, exponent, prime)
        if root != 1:
            assert pow(root, ELL, prime) == 1
            return root
        base += 1


def evaluate(
    gamma: tuple[int, ...], support: tuple[int, ...], point: int, prime: int
) -> int:
    return sum(
        coefficient * pow(point, exponent, prime)
        for coefficient, exponent in zip(gamma, support)
    ) % prime


def equal_on_roots(
    gamma: tuple[int, ...],
    support: tuple[int, ...],
    roots: tuple[int, ...],
    ratio: int,
    zeta: int,
    prime: int,
) -> bool:
    values = {
        evaluate(
            gamma,
            support,
            ratio * pow(zeta, root, prime) % prime,
            prime,
        )
        for root in roots
    }
    return len(values) == 1


def quotient_representatives(prime: int, zeta: int) -> list[int]:
    visited = bytearray(prime)
    output = []
    for candidate in range(1, prime):
        if visited[candidate]:
            continue
        output.append(candidate)
        value = candidate
        for _ in range(ELL):
            assert not visited[value]
            visited[value] = 1
            value = value * zeta % prime
    assert len(output) == (prime - 1) // ELL
    return output


def fibre_maximum(
    gamma: tuple[int, ...],
    support: tuple[int, ...],
    representative: int,
    zeta: int,
    prime: int,
) -> int:
    multiplicities = {}
    point = representative
    for _ in range(ELL):
        value = evaluate(gamma, support, point, prime)
        multiplicities[value] = multiplicities.get(value, 0) + 1
        point = point * zeta % prime
    return max(multiplicities.values())


def summarize(maxima: list[int]) -> dict[str, object]:
    ordered = sorted(maxima, reverse=True)
    top = (ordered + [0, 0, 0])[:3]
    return {
        "labels": len(maxima),
        "top_three": top,
        "S3": sum(top),
        "maximum_fibre": ordered[0],
        "histogram": {
            str(size): maxima.count(size) for size in sorted(set(maxima))
        },
    }


PROFILE_CACHE: dict[
    tuple[int, tuple[int, ...]], tuple[dict[str, object], int]
] = {}
REPRESENTATIVE_CACHE: dict[int, tuple[int, list[int]]] = {}


def direct_profiles(
    prime: int, gamma: tuple[int, ...]
) -> tuple[dict[str, object], int]:
    key = (prime, gamma)
    if key in PROFILE_CACHE:
        return PROFILE_CACHE[key]
    if prime not in REPRESENTATIVE_CACHE:
        zeta = order_eleven_root(prime)
        REPRESENTATIVE_CACHE[prime] = (
            zeta,
            quotient_representatives(prime, zeta),
        )
    zeta, representatives = REPRESENTATIVE_CACHE[prime]
    full = []
    square = []
    nonsquare = []
    even = []
    for representative in representatives:
        current = fibre_maximum(
            gamma, (1, 2, 3, 4, 5), representative, zeta, prime
        )
        full.append(current)
        if pow(representative, (prime - 1) // 2, prime) == 1:
            square.append(current)
        else:
            nonsquare.append(current)
        even.append(
            fibre_maximum(
                gamma,
                (2, 4, 6, 8, 10),
                representative,
                zeta,
                prime,
            )
        )
    even.sort(reverse=True)
    even_s6 = sum((even + [0] * 6)[:6])
    result = (
        {
            "full_quotient": summarize(full),
            "square_quotient": summarize(square),
            "nonsquare_quotient": summarize(nonsquare),
        },
        even_s6,
    )
    assert even_s6 == 2 * result[0]["square_quotient"]["S3"]
    PROFILE_CACHE[key] = result
    return result


def audit_line_events(terminal: dict[str, object]) -> None:
    assert not terminal["rank_drop_rows"] if "rank_drop_rows" in terminal else True
    for row in terminal["exceptional_state_rows"]:
        prime = int(row["prime"])
        zeta = pow(order_eleven_root(prime), int(row["embedding"]), prime)
        gamma = tuple(int(value) for value in row["gamma"])
        assert row["matrix_rank"] == 4
        assert bool(row["exact_five_support"]) == all(gamma)
        assert row["ratio_is_distinct_label"]
        assert equal_on_roots(
            gamma,
            (1, 2, 3, 4, 5),
            FOUR_ROOTS[int(row["first_root_index"])],
            1,
            zeta,
            prime,
        )
        assert equal_on_roots(
            gamma,
            (1, 2, 3, 4, 5),
            FOUR_ROOTS[int(row["second_root_index"])],
            int(row["ratio"]),
            zeta,
            prime,
        )


def audit_five_events(terminal: dict[str, object]) -> None:
    assert not terminal["rank_drop_rows"]
    rebuilt: dict[tuple[int, tuple[int, ...]], set[int]] = {}
    for row in terminal["event_rows"]:
        prime = int(row["prime"])
        zeta = pow(order_eleven_root(prime), int(row["embedding"]), prime)
        gamma = tuple(int(value) for value in row["gamma"])
        ratio = int(row["ratio"])
        assert all(gamma)
        assert equal_on_roots(
            gamma,
            (1, 2, 3, 4, 5),
            FIVE_ROOTS[int(row["five_root_index"])],
            1,
            zeta,
            prime,
        )
        assert equal_on_roots(
            gamma,
            (1, 2, 3, 4, 5),
            TRIPLE_ROOTS[int(row["triple_root_index"])],
            ratio,
            zeta,
            prime,
        )
        assert pow(ratio, ELL, prime) == int(row["quotient_label"])
        assert (
            pow(ratio, (prime - 1) // 2, prime) == 1
        ) == bool(row["ratio_is_square"])
        if row["ratio_is_square"]:
            rebuilt.setdefault((prime, gamma), set()).add(
                int(row["quotient_label"])
            )
    assert max((len(labels) for labels in rebuilt.values()), default=0) <= 1


def audit_profile_artifact(artifact: dict[str, object]) -> None:
    assert not artifact["states_with_transport_S3_above_10"]
    maximum = 0
    for row in artifact["state_rows"]:
        prime = int(row["prime"])
        gamma = tuple(int(value) for value in row["gamma"])
        direct, even_s6 = direct_profiles(prime, gamma)
        assert direct["full_quotient"] == row["full_quotient"]
        assert direct["square_quotient"] == row["square_quotient"]
        assert direct["nonsquare_quotient"] == row["nonsquare_quotient"]
        assert even_s6 <= 20
        maximum = max(maximum, direct["square_quotient"]["S3"])
    assert maximum == artifact["maximum_transport_S3_on_Q_squared"] == 10


def main() -> None:
    line_filter = load("p04cw_parity_line_pair_filter.json")
    line_terminal = load("p04cw_parity_line_pair_modular_terminal.json")
    line_profiles = load("p04cw_parity_pair_exceptional_profiles.json")
    five_filter = load("p04cw_five_triple_filter.json")
    five_terminal = load("p04cw_five_triple_modular_terminal.json")
    five_profiles = load("p04cw_five_triple_profiles.json")

    assert not line_filter["characteristic_zero_nontrivial_rows"]
    assert not five_filter["characteristic_zero_nontrivial_rows"]
    audit_factorizations(line_filter)
    audit_factorizations(five_filter)
    audit_line_events(line_terminal)
    audit_five_events(five_terminal)
    audit_profile_artifact(line_profiles)
    audit_profile_artifact(five_profiles)

    assert line_profiles["unique_exact_five_projective_states"] == 252
    assert five_profiles["source_states"] == 241
    print("P04CW_INDEPENDENT_PARITY_UNIFORM_S6_AUDIT_V1")
    print(
        "line_states=252 five_states=241 unique_scalar_profiles="
        + str(len(PROFILE_CACHE))
    )
    print("PASS_P04CW_INDEPENDENT_PARITY_UNIFORM_S6_AUDIT")


if __name__ == "__main__":
    main()
