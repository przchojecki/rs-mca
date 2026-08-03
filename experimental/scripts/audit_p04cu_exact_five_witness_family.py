#!/usr/bin/env python3
"""Independent pointwise audit of the P04cu exact-five witness family."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


P = 331
ELL = 11
SUPPORT = [1, 3, 5, 7, 9]


def trim(polynomial: list[int]) -> list[int]:
    while polynomial and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def add(first: list[int], second: list[int]) -> list[int]:
    output = [0] * max(len(first), len(second))
    for index, value in enumerate(first):
        output[index] = (output[index] + value) % P
    for index, value in enumerate(second):
        output[index] = (output[index] + value) % P
    return trim(output)


def multiply(first: list[int], second: list[int]) -> list[int]:
    output = [0] * (len(first) + len(second) - 1)
    for first_index, first_value in enumerate(first):
        for second_index, second_value in enumerate(second):
            output[first_index + second_index] = (
                output[first_index + second_index]
                + first_value * second_value
            ) % P
    return trim(output)


def substitute_ell(polynomial: list[int]) -> list[int]:
    output = [0] * ((len(polynomial) - 1) * ELL + 1)
    for index, value in enumerate(polynomial):
        output[index * ELL] = value
    return trim(output)


def evaluate(polynomial: list[int], point: int) -> int:
    value = 0
    for coefficient in reversed(polynomial):
        value = (value * point + coefficient) % P
    return value


def from_roots(roots: list[int]) -> list[int]:
    output = [1]
    for root in roots:
        output = multiply(output, [(-root) % P, 1])
    return output


def divide(dividend: list[int], divisor: list[int]) -> tuple[list[int], list[int]]:
    work = dividend[:]
    quotient = [0] * max(1, len(work) - len(divisor) + 1)
    inverse = pow(divisor[-1], -1, P)
    while work and len(work) >= len(divisor):
        coefficient = work[-1] * inverse % P
        shift = len(work) - len(divisor)
        quotient[shift] = coefficient
        for index, value in enumerate(divisor):
            work[shift + index] = (
                work[shift + index] - coefficient * value
            ) % P
        trim(work)
    return trim(quotient), trim(work)


def residue_support(codeword: list[int]) -> list[int]:
    return sorted(
        {
            index % ELL
            for index, coefficient in enumerate(codeword)
            if coefficient and index % ELL
        }
    )


def deletion_audit(
    codeword: list[int], retained: list[int], missed: list[int]
) -> tuple[int, list[int], list[int]]:
    retained_locator = from_roots(retained)
    kernel, remainder = divide(codeword, retained_locator)
    assert remainder == []
    deletable = []
    for point in missed:
        enlarged = multiply(retained_locator, [(-point) % P, 1])
        quotient, rem = divide(codeword, enlarged)
        if not rem and len(quotient) - 1 <= len(missed) - 1:
            deletable.append(point)
    negative_missed = missed + [retained[0]]
    negative_locator = from_roots(retained[1:])
    negative_deletable = []
    for point in negative_missed:
        enlarged = multiply(negative_locator, [(-point) % P, 1])
        quotient, rem = divide(codeword, enlarged)
        if not rem and len(quotient) - 1 <= len(negative_missed) - 1:
            negative_deletable.append(point)
    return len(kernel) - 1, deletable, negative_deletable


def pointwise_core(
    codeword: list[int], representatives: list[int], subgroup: list[int]
) -> tuple[list[int], list[int], list[int]]:
    retained: list[int] = []
    missed: list[int] = []
    profile = []
    for representative in representatives:
        count = 0
        for point in subgroup:
            x = representative * point % P
            if evaluate(codeword, x) == 0:
                retained.append(x)
                count += 1
            else:
                missed.append(x)
        profile.append(count)
    return retained, missed, profile


def stabilizer(missed: list[int], subgroup: list[int]) -> list[int]:
    missed_set = set(missed)
    return [
        multiplier
        for multiplier in subgroup
        if {multiplier * point % P for point in missed_set} == missed_set
    ]


def audit_anchor(anchor: dict[str, object]) -> dict[str, object]:
    generator = int(anchor["generator"])
    zeta = int(anchor["zeta"])
    subgroup = [pow(zeta, index, P) for index in range(ELL)]
    codeword = [int(value) for value in anchor["codeword_coefficients_ascending"]]
    core_locator = [
        int(value) for value in anchor["core_locator_coefficients_ascending"]
    ]
    assert residue_support(codeword) == SUPPORT
    assert len(codeword) - 1 == int(anchor["degree"])
    assert len(codeword) - 1 <= int(anchor["degree_bound"])

    gamma = [int(value) for value in anchor["gamma_active_coefficients"]]
    spectrum = []
    for label_index in range((P - 1) // ELL):
        representative = pow(generator, label_index, P)
        values = [
            sum(
                coefficient * pow(representative * point % P, exponent, P)
                for coefficient, exponent in zip(gamma, SUPPORT)
            )
            % P
            for point in subgroup
        ]
        spectrum.append(max(Counter(values).values()))
    assert Counter(spectrum) == Counter({1: 22, 2: 4, 3: 2, 5: 2})

    for representative, value, scalar, label in zip(
        anchor["petal_representatives"],
        anchor["petal_values"],
        anchor["petal_scalars"],
        anchor["alpha_labels"],
    ):
        for point in subgroup:
            x = int(representative) * point % P
            actual = evaluate(codeword, x)
            assert actual == int(value)
            assert actual == int(scalar) * evaluate(core_locator, int(label)) % P

    representatives = [int(value) for value in anchor["core_representatives"]]
    retained, missed, profile = pointwise_core(codeword, representatives, subgroup)
    assert profile == anchor["core_retained_profile"]
    assert sorted(missed) == anchor["exact_missed_core"]
    tau = int(anchor["tau"])
    agreement = tau * ELL + len(retained)
    assert agreement == int(anchor["total_agreement"])
    assert agreement >= int(anchor["listing_threshold"])
    kernel_degree, deletable, negative = deletion_audit(codeword, retained, missed)
    assert kernel_degree == int(anchor["kernel_quotient_degree"])
    assert deletable == anchor["single_point_deletions"] == []
    assert negative == anchor["minimality_negative_control"]
    assert stabilizer(missed, subgroup) == anchor["H_stabilizer"] == [1]
    return {
        "tau": tau,
        "profile": profile,
        "agreement": agreement,
        "missed": len(missed),
    }


def audit_padded(
    row: dict[str, object], anchor: dict[str, object]
) -> dict[str, object]:
    generator = int(anchor["generator"])
    zeta = int(anchor["zeta"])
    subgroup = [pow(zeta, index, P) for index in range(ELL)]
    base_codeword = [
        int(value) for value in anchor["codeword_coefficients_ascending"]
    ]
    base_locator = [
        int(value) for value in anchor["core_locator_coefficients_ascending"]
    ]
    q_polynomial = [int(value) for value in row["Q_coefficients_ascending"]]
    codeword = multiply(base_codeword, substitute_ell(q_polynomial))
    core_locator = multiply(base_locator, q_polynomial)
    assert residue_support(codeword) == SUPPORT
    assert len(codeword) - 1 == int(row["degree"])
    assert len(codeword) - 1 <= int(row["degree_bound"])

    for representative, scalar, label in zip(
        anchor["petal_representatives"],
        anchor["petal_scalars"],
        anchor["alpha_labels"],
    ):
        for point in subgroup:
            x = int(representative) * point % P
            assert evaluate(codeword, x) == (
                int(scalar) * evaluate(core_locator, int(label))
            ) % P

    new_indices = [int(value) for value in row["new_dead_core_quotient_indices"]]
    representatives = [int(value) for value in anchor["core_representatives"]] + [
        pow(generator, index, P) for index in new_indices
    ]
    retained, missed, profile = pointwise_core(codeword, representatives, subgroup)
    assert profile == row["core_retained_profile"]
    assert profile[-len(new_indices) :] == [ELL] * len(new_indices)
    assert sorted(missed) == anchor["exact_missed_core"]
    tau = int(row["tau"])
    agreement = tau * ELL + len(retained)
    assert agreement == int(row["total_agreement"])
    assert agreement >= int(row["listing_threshold"])
    kernel_degree, deletable, negative = deletion_audit(codeword, retained, missed)
    assert kernel_degree == int(row["kernel_quotient_degree"])
    assert deletable == row["single_point_deletions"] == []
    assert negative == row["minimality_negative_control"]
    assert stabilizer(missed, subgroup) == row["H_stabilizer"] == [1]
    return {
        "tau": tau,
        "m": int(row["m"]),
        "D": int(row["D"]),
        "agreement": agreement,
        "threshold": int(row["listing_threshold"]),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    arguments = parser.parse_args()
    certificate = json.loads(arguments.certificate.read_text(encoding="utf-8"))
    assert certificate["schema"] == "P04CU_ELL11_EXACT_FIVE_NONVACANCY_V1"
    assert certificate["finite_field_census"]["top_envelopes_S6_through_S9"] == [
        20,
        22,
        24,
        27,
    ]
    family = certificate["witness_family"]
    anchors = family["D_zero_anchors"]
    anchor_rows = [audit_anchor(anchor) for anchor in anchors]
    by_tau = {int(anchor["tau"]): anchor for anchor in anchors}
    padded_rows = [
        audit_padded(row, by_tau[int(row["tau"])])
        for row in family["D_positive_padded_words"]
    ]
    assert {(row["tau"], row["m"]) for row in padded_rows} == {
        (6, 8),
        (6, 9),
        (6, 10),
        (7, 9),
        (7, 10),
        (8, 10),
    }
    print("P04CU_INDEPENDENT_WITNESS_AUDIT_V1")
    print("anchors=" + json.dumps(anchor_rows, sort_keys=True))
    print("padded=" + json.dumps(padded_rows, sort_keys=True))
    print("PASS_P04CU_INDEPENDENT_EXACT_FIVE_WITNESS_AUDIT")


if __name__ == "__main__":
    main()
