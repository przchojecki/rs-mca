#!/usr/bin/env python3
"""Classify the P04cw parity pair-specialization spectra exactly.

The modular line-pair terminal reconstructs every exact-five coefficient
state created by an exceptional specialization.  This script deduplicates
those projective states and computes the complete quotient-label spectrum of
P(Z)=gamma_1 Z+...+gamma_5 Z^5 on every multiplicative H-coset, |H|=11.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy


ELL = 11


def order_eleven_root(prime: int) -> int:
    exponent = (prime - 1) // ELL
    base = 2
    while True:
        root = pow(base, exponent, prime)
        if root != 1:
            assert pow(root, ELL, prime) == 1
            return root
        base += 1


def coset_representatives(prime: int, zeta: int) -> numpy.ndarray:
    visited = bytearray(prime)
    representatives = []
    for candidate in range(1, prime):
        if visited[candidate]:
            continue
        representatives.append(candidate)
        value = candidate
        for _ in range(ELL):
            assert not visited[value]
            visited[value] = 1
            value = value * zeta % prime
        assert value == candidate
    assert len(representatives) == (prime - 1) // ELL
    assert all(visited[1:])
    return numpy.asarray(representatives, dtype=numpy.int64)


def polynomial_values(
    points: numpy.ndarray, gamma: tuple[int, ...], prime: int
) -> numpy.ndarray:
    accumulator = numpy.full(points.shape, gamma[-1], dtype=numpy.int64)
    for coefficient in reversed(gamma[:-1]):
        accumulator = (accumulator * points + coefficient) % prime
    return accumulator * points % prime


def summarize(maximum_run: numpy.ndarray) -> dict[str, object]:
    counts = numpy.bincount(maximum_run, minlength=ELL + 1)
    top = []
    for fibre_size in range(ELL, 0, -1):
        top.extend([fibre_size] * min(int(counts[fibre_size]), 3 - len(top)))
        if len(top) == 3:
            break
    while len(top) < 3:
        top.append(0)
    histogram = {
        str(fibre_size): int(counts[fibre_size])
        for fibre_size in range(1, ELL + 1)
        if counts[fibre_size]
    }
    return {
        "labels": int(len(maximum_run)),
        "top_three": top,
        "S3": sum(top),
        "maximum_fibre": max(
            int(value) for value in numpy.flatnonzero(counts)
        ),
        "histogram": histogram,
    }


def spectrum(
    prime: int,
    zeta: int,
    representatives: numpy.ndarray,
    gamma: tuple[int, ...],
) -> dict[str, object]:
    quotient_size = len(representatives)
    values = numpy.empty((ELL, quotient_size), dtype=numpy.int64)
    zeta_power = 1
    for root_index in range(ELL):
        points = representatives * zeta_power % prime
        values[root_index] = polynomial_values(points, gamma, prime)
        zeta_power = zeta_power * zeta % prime
    values.sort(axis=0)

    current_run = numpy.ones(quotient_size, dtype=numpy.int8)
    maximum_run = numpy.ones(quotient_size, dtype=numpy.int8)
    for row in range(1, ELL):
        equal = values[row] == values[row - 1]
        current_run = numpy.where(equal, current_run + 1, 1)
        maximum_run = numpy.maximum(maximum_run, current_run)

    square_mask = numpy.asarray(
        [pow(int(value), (prime - 1) // 2, prime) == 1 for value in representatives],
        dtype=numpy.bool_,
    )
    assert int(square_mask.sum()) == quotient_size // 2
    return {
        "full_quotient": summarize(maximum_run),
        "square_quotient": summarize(maximum_run[square_mask]),
        "nonsquare_quotient": summarize(maximum_run[~square_mask]),
    }


def scalar_spectrum(
    prime: int, zeta: int, representatives: list[int], gamma: tuple[int, ...]
) -> dict[str, object]:
    maxima = []
    square_flags = []
    for representative in representatives:
        fibre_values = []
        point = representative
        for _ in range(ELL):
            value = 0
            power = point
            for coefficient in gamma:
                value = (value + coefficient * power) % prime
                power = power * point % prime
            fibre_values.append(value)
            point = point * zeta % prime
        multiplicities = {}
        for value in fibre_values:
            multiplicities[value] = multiplicities.get(value, 0) + 1
        maxima.append(max(multiplicities.values()))
        square_flags.append(pow(representative, (prime - 1) // 2, prime) == 1)

    def scalar_summary(selected: list[int]) -> dict[str, object]:
        selected.sort(reverse=True)
        histogram = {
            str(size): selected.count(size) for size in sorted(set(selected))
        }
        top = (selected + [0, 0, 0])[:3]
        return {
            "labels": len(selected),
            "top_three": top,
            "S3": sum(top),
            "maximum_fibre": selected[0],
            "histogram": histogram,
        }

    return {
        "full_quotient": scalar_summary(maxima[:]),
        "square_quotient": scalar_summary(
            [value for value, square in zip(maxima, square_flags) if square]
        ),
        "nonsquare_quotient": scalar_summary(
            [value for value, square in zip(maxima, square_flags) if not square]
        ),
    }


def classify(terminal: dict[str, object]) -> dict[str, object]:
    assert terminal["schema"] == "P04CW_PARITY_LINE_PAIR_MODULAR_TERMINAL_V1"
    provenance: dict[tuple[int, tuple[int, ...]], int] = {}
    exclusion_counts = {
        "same_quotient_label": 0,
        "non_one_dimensional_kernel": 0,
        "proper_support": 0,
    }
    for row in terminal["exceptional_state_rows"]:
        if not row["ratio_is_distinct_label"]:
            exclusion_counts["same_quotient_label"] += 1
            continue
        if row["matrix_rank"] != 4 or row["gamma"] is None:
            exclusion_counts["non_one_dimensional_kernel"] += 1
            continue
        if not row["exact_five_support"]:
            exclusion_counts["proper_support"] += 1
            continue
        key = (int(row["prime"]), tuple(int(value) for value in row["gamma"]))
        provenance[key] = provenance.get(key, 0) + 1

    grouped: dict[int, list[tuple[tuple[int, ...], int]]] = {}
    for (prime, gamma), multiplicity in sorted(provenance.items()):
        grouped.setdefault(prime, []).append((gamma, multiplicity))

    state_rows = []
    scalar_cross_checks = 0
    maximum_full_s3 = 0
    maximum_transport_s3 = 0
    for prime, states in grouped.items():
        zeta = order_eleven_root(prime)
        representatives = coset_representatives(prime, zeta)
        for gamma, multiplicity in states:
            current = spectrum(prime, zeta, representatives, gamma)
            if prime < 100:
                independent = scalar_spectrum(
                    prime, zeta, representatives.tolist(), gamma
                )
                assert current == independent
                scalar_cross_checks += 1
            maximum_full_s3 = max(
                maximum_full_s3, int(current["full_quotient"]["S3"])
            )
            maximum_transport_s3 = max(
                maximum_transport_s3,
                int(current["square_quotient"]["S3"]),
            )
            state_rows.append(
                {
                    "prime": prime,
                    "gamma": list(gamma),
                    "source_rows": multiplicity,
                    **current,
                }
            )

    violations = [
        row for row in state_rows if row["square_quotient"]["S3"] > 10
    ]
    extremizers = [
        row
        for row in state_rows
        if row["square_quotient"]["S3"] == maximum_transport_s3
    ]
    return {
        "schema": "P04CW_PARITY_PAIR_EXCEPTIONAL_PROFILES_V1",
        "source_exceptional_state_rows": len(terminal["exceptional_state_rows"]),
        "exclusion_counts": exclusion_counts,
        "unique_exact_five_projective_states": len(state_rows),
        "primes_with_exact_five_states": len(grouped),
        "complete_quotient_spectra_computed": len(state_rows),
        "scalar_cross_checks_at_primes_below_100": scalar_cross_checks,
        "maximum_full_quotient_S3": maximum_full_s3,
        "maximum_transport_S3_on_Q_squared": maximum_transport_s3,
        "states_with_transport_S3_above_10": violations,
        "transport_extremizers": extremizers,
        "state_rows": state_rows,
        "deduction": (
            "Every exact-five state arising from an off-diagonal modular "
            "specialization satisfies S3(P|Q^2)<=10 if "
            "states_with_transport_S3_above_10 is empty."
        ),
        "remaining": (
            "Treat the characteristic-zero diagonal family and the tail "
            "after a five-point fibre."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terminal", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    terminal = json.loads(arguments.terminal.read_text(encoding="utf-8"))
    result = classify(terminal)
    arguments.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(result["schema"])
    print(
        "states="
        + str(result["unique_exact_five_projective_states"])
        + " primes="
        + str(result["primes_with_exact_five_states"])
        + " max_transport_S3="
        + str(result["maximum_transport_S3_on_Q_squared"])
        + " violations="
        + str(len(result["states_with_transport_S3_above_10"]))
    )
    if result["states_with_transport_S3_above_10"]:
        print("COUNTEREXAMPLE_P04CW_PARITY_PAIR_BOUND")
    else:
        print("PASS_P04CW_PARITY_PAIR_EXCEPTIONAL_PROFILES")


if __name__ == "__main__":
    main()
