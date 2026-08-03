#!/usr/bin/env python3
"""Audit the modular terminal of the P04cw five-plus-triple filter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy

import derive_p04cw_five_triple_filter as five_triple
import verify_p04cw_parity_line_pair_modular_terminal as modular


ELL = 11


def anchor_matrix(
    roots: tuple[int, ...], zeta: int, prime: int
) -> list[list[int]]:
    powers = [pow(zeta, index, prime) for index in range(ELL)]
    return [
        [
            (
                powers[(roots[row] * exponent) % ELL]
                - powers[(roots[0] * exponent) % ELL]
            )
            % prime
            for exponent in five_triple.SUPPORT
        ]
        for row in range(1, 5)
    ]


def event_polynomials(
    gamma: list[int], roots: tuple[int, ...], zeta: int, prime: int
) -> list[list[int]]:
    powers = [pow(zeta, index, prime) for index in range(ELL)]
    output = []
    for row in range(1, 3):
        polynomial = [0] * 6
        for exponent, coefficient in zip(five_triple.SUPPORT, gamma):
            difference = (
                powers[(roots[row] * exponent) % ELL]
                - powers[(roots[0] * exponent) % ELL]
            ) % prime
            polynomial[exponent] = coefficient * difference % prime
        while polynomial and polynomial[0] == 0:
            polynomial.pop(0)
        output.append(modular.trim(polynomial))
    return output


def roots_in_prime_field(polynomial: list[int], prime: int) -> list[int]:
    polynomial = modular.trim(polynomial[:])
    if len(polynomial) <= 1:
        return []
    if len(polynomial) == 2:
        return [
            -polynomial[0] * pow(polynomial[1], prime - 2, prime) % prime
        ]
    variable = sympy.Symbol("t")
    expression = sum(
        coefficient * variable**degree
        for degree, coefficient in enumerate(polynomial)
    )
    factors = sympy.factor_list(expression, modulus=prime)[1]
    roots = []
    for factor, _ in factors:
        current = sympy.Poly(factor, variable, modulus=prime)
        if current.degree() != 1:
            continue
        leading, constant = [int(value) % prime for value in current.all_coeffs()]
        roots.append(-constant * pow(leading, prime - 2, prime) % prime)
    return sorted(set(roots))


def anchor_fibre_size(
    gamma: list[int], zeta: int, prime: int
) -> int:
    values = []
    point = 1
    for _ in range(ELL):
        value = 0
        power = point
        for coefficient in gamma:
            value = (value + coefficient * power) % prime
            power = power * point % prime
        values.append(value)
        point = point * zeta % prime
    multiplicities = {}
    for value in values:
        multiplicities[value] = multiplicities.get(value, 0) + 1
    return max(multiplicities.values())


def audit(source: dict[str, object]) -> dict[str, object]:
    assert source["schema"] == "P04CW_FIVE_TRIPLE_FILTER_V1"
    assert not source["characteristic_zero_nontrivial_rows"]
    global_candidates = set(
        source["candidate_primes_congruent_to_one_mod_11"]
    )
    assert len(global_candidates) == 80
    assert all(sympy.isprime(prime) for prime in global_candidates)

    same_label = [-1] + [0] * 10 + [1]
    state_events: dict[tuple[int, tuple[int, ...]], dict[str, object]] = {}
    residual_rows = []
    event_rows = []
    rank_drop_keys = set()
    proper_support_keys = set()
    specialization_count = 0

    for row in source["candidate_prime_cell_rows"]:
        five_index = int(row["five_root_index"])
        triple_index = int(row["triple_root_index"])
        five_roots = five_triple.FIVE_ROOT_CLASSES[five_index]
        triple_roots = five_triple.TRIPLE_ROOT_CLASSES[triple_index]
        for prime_value in row["candidate_primes"]:
            prime = int(prime_value)
            assert prime in global_candidates
            base_zeta = modular.order_eleven_root(prime)
            for embedding in range(1, ELL):
                specialization_count += 1
                zeta = pow(base_zeta, embedding, prime)
                rank, gamma = modular.one_dimensional_kernel(
                    anchor_matrix(five_roots, zeta, prime), prime
                )
                anchor_key = (prime, embedding, five_index)
                if rank != 4 or gamma is None:
                    rank_drop_keys.add((*anchor_key, rank))
                    continue
                if not all(gamma):
                    proper_support_keys.add(anchor_key)
                    continue
                polynomials = event_polynomials(
                    gamma, triple_roots, zeta, prime
                )
                current = modular.gcd_polynomial(
                    polynomials[0], polynomials[1], prime
                )
                residual, removed_degree = modular.saturate_same_label(
                    current, same_label, prime
                )
                residual_degree = len(residual) - 1
                if residual_degree <= 0:
                    continue
                roots = roots_in_prime_field(residual, prime)
                residual_rows.append(
                    {
                        "prime": prime,
                        "embedding": embedding,
                        "five_root_index": five_index,
                        "triple_root_index": triple_index,
                        "residual_degree": residual_degree,
                        "same_label_degree_removed": removed_degree,
                        "residual_polynomial": residual,
                        "roots_in_Fp": roots,
                    }
                )
                state_key = (prime, tuple(gamma))
                state = state_events.setdefault(
                    state_key,
                    {
                        "prime": prime,
                        "gamma": gamma,
                        "anchor_fibre_size": anchor_fibre_size(
                            gamma, zeta, prime
                        ),
                        "square_triple_labels": set(),
                        "nonsquare_triple_labels": set(),
                        "source_five_root_indices": set(),
                    },
                )
                state["source_five_root_indices"].add(five_index)
                for ratio in roots:
                    assert pow(ratio, ELL, prime) != 1
                    quotient_label = pow(ratio, ELL, prime)
                    square = pow(ratio, (prime - 1) // 2, prime) == 1
                    target = (
                        state["square_triple_labels"]
                        if square
                        else state["nonsquare_triple_labels"]
                    )
                    target.add(quotient_label)
                    event_rows.append(
                        {
                            "prime": prime,
                            "embedding": embedding,
                            "five_root_index": five_index,
                            "triple_root_index": triple_index,
                            "ratio": ratio,
                            "quotient_label": quotient_label,
                            "ratio_is_square": square,
                            "gamma": gamma,
                        }
                    )

    states = []
    for state in state_events.values():
        states.append(
            {
                **{
                    key: value
                    for key, value in state.items()
                    if not isinstance(value, set)
                },
                "square_triple_labels": sorted(state["square_triple_labels"]),
                "nonsquare_triple_labels": sorted(
                    state["nonsquare_triple_labels"]
                ),
                "source_five_root_indices": sorted(
                    state["source_five_root_indices"]
                ),
            }
        )
    dangerous = [
        state for state in states if len(state["square_triple_labels"]) >= 2
    ]
    return {
        "schema": "P04CW_FIVE_TRIPLE_MODULAR_TERMINAL_V1",
        "candidate_primes": len(global_candidates),
        "candidate_cell_rows": len(source["candidate_prime_cell_rows"]),
        "specializations_audited": specialization_count,
        "rank_drop_rows": [list(row) for row in sorted(rank_drop_keys)],
        "proper_support_rows": [
            list(row) for row in sorted(proper_support_keys)
        ],
        "residual_rows": residual_rows,
        "event_rows": event_rows,
        "unique_exact_five_anchor_states_with_events": states,
        "dangerous_states_with_two_square_triple_labels": dangerous,
        "deduction": (
            "If rank-drop rows are discharged and dangerous_states is empty, "
            "no exact-five anchor has two further triple fibres on Q^2."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    source = json.loads(arguments.filter.read_text(encoding="utf-8"))
    result = audit(source)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(result["schema"])
    print(
        "specializations="
        + str(result["specializations_audited"])
        + " residual_rows="
        + str(len(result["residual_rows"]))
        + " states="
        + str(len(result["unique_exact_five_anchor_states_with_events"]))
        + " dangerous="
        + str(len(result["dangerous_states_with_two_square_triple_labels"]))
        + " rank_drop="
        + str(len(result["rank_drop_rows"]))
    )
    print("PASS_P04CW_FIVE_TRIPLE_MODULAR_TERMINAL")


if __name__ == "__main__":
    main()
