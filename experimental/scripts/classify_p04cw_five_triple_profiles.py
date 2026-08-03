#!/usr/bin/env python3
"""Compute complete Q^2 spectra for every P04cw five-fibre terminal state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import classify_p04cw_parity_pair_exceptional_profiles as profiles


def classify(terminal: dict[str, object]) -> dict[str, object]:
    assert terminal["schema"] == "P04CW_FIVE_TRIPLE_MODULAR_TERMINAL_V1"
    assert not terminal["rank_drop_rows"]
    source_states = terminal["unique_exact_five_anchor_states_with_events"]
    rows = []
    maximum_transport_s3 = 0
    scalar_cross_checks = 0

    grouped: dict[int, list[dict[str, object]]] = {}
    for state in source_states:
        grouped.setdefault(int(state["prime"]), []).append(state)

    for prime, states in grouped.items():
        zeta = profiles.order_eleven_root(prime)
        representatives = profiles.coset_representatives(prime, zeta)
        for state in states:
            gamma = tuple(int(value) for value in state["gamma"])
            current = profiles.spectrum(prime, zeta, representatives, gamma)
            if prime < 100:
                independent = profiles.scalar_spectrum(
                    prime, zeta, representatives.tolist(), gamma
                )
                assert current == independent
                scalar_cross_checks += 1
            assert current["square_quotient"]["maximum_fibre"] >= 5
            maximum_transport_s3 = max(
                maximum_transport_s3,
                int(current["square_quotient"]["S3"]),
            )
            rows.append(
                {
                    "prime": prime,
                    "gamma": list(gamma),
                    "anchor_fibre_size": state["anchor_fibre_size"],
                    "square_triple_labels": state["square_triple_labels"],
                    "source_five_root_indices": state[
                        "source_five_root_indices"
                    ],
                    **current,
                }
            )

    violations = [
        row for row in rows if row["square_quotient"]["S3"] > 10
    ]
    extremizers = [
        row
        for row in rows
        if row["square_quotient"]["S3"] == maximum_transport_s3
    ]
    return {
        "schema": "P04CW_FIVE_TRIPLE_PROFILES_V1",
        "source_states": len(source_states),
        "primes": len(grouped),
        "complete_Q_squared_spectra": len(rows),
        "scalar_cross_checks_at_primes_below_100": scalar_cross_checks,
        "maximum_transport_S3_on_Q_squared": maximum_transport_s3,
        "states_with_transport_S3_above_10": violations,
        "transport_extremizers": extremizers,
        "state_rows": rows,
        "deduction": (
            "Every exact-five anchor state surviving the finite "
            "specialization terminal satisfies S3(P|Q^2)<=10 if the "
            "violation list is empty. States with no distinct triple event "
            "satisfy the stronger envelope 5+2+2=9."
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
        + str(result["source_states"])
        + " max_transport_S3="
        + str(result["maximum_transport_S3_on_Q_squared"])
        + " violations="
        + str(len(result["states_with_transport_S3_above_10"]))
    )
    if result["states_with_transport_S3_above_10"]:
        print("COUNTEREXAMPLE_P04CW_FIVE_TRIPLE_BOUND")
    else:
        print("PASS_P04CW_FIVE_TRIPLE_PROFILES")


if __name__ == "__main__":
    main()
