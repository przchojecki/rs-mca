#!/usr/bin/env python3
"""Verify finite identities for the selected-owner cube-mean boundary.

The script checks exact finite guardrails and the maximal-band theorem.  It
does not prove source-specific ambient leakage, non-equitable localization,
cube-spectrum compression, or paid atlas admission.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental"
    / "data"
    / "certificates"
    / "selected-owner-cube-mean-boundary-v1"
    / "selected_owner_cube_mean_boundary_v1.json"
)
SOURCE_REVISION = "764f1c0243770baa437d4ae790b1448afa091680"
TOL = 1.0e-10


def parity(value: int) -> int:
    return value.bit_count() & 1


def lp(values: Iterable[Fraction], exponent: float) -> float:
    return sum(abs(float(value)) ** exponent for value in values) ** (
        1.0 / exponent
    )


def dot(left: Sequence[Fraction], right: Sequence[Fraction]) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def add(left: Sequence[Fraction], right: Sequence[Fraction]) -> list[Fraction]:
    return [a + b for a, b in zip(left, right)]


def subtract(
    left: Sequence[Fraction], right: Sequence[Fraction]
) -> list[Fraction]:
    return [a - b for a, b in zip(left, right)]


def walsh_project(
    values: Sequence[Fraction], band: set[int]
) -> list[Fraction]:
    order = len(values)
    if order & (order - 1):
        raise ValueError("Walsh group order must be a power of two")
    hats = [
        sum(
            (
                value if parity(frequency & position) == 0 else -value
                for position, value in enumerate(values)
            ),
            Fraction(0),
        )
        for frequency in range(order)
    ]
    return [
        sum(
            (
                hats[frequency]
                if parity(frequency & position) == 0
                else -hats[frequency]
                for frequency in band
            ),
            Fraction(0),
        )
        / order
        for position in range(order)
    ]


def conditional_expectation(
    values: Sequence[Fraction], parts: Sequence[Sequence[int]]
) -> list[Fraction]:
    output = [Fraction(0) for _ in values]
    seen: set[int] = set()
    for part in parts:
        if not part:
            raise ValueError("empty partition part")
        if seen.intersection(part):
            raise ValueError("overlapping partition parts")
        seen.update(part)
        average = sum((values[index] for index in part), Fraction(0)) / len(part)
        for index in part:
            output[index] = average
    if seen != set(range(len(values))):
        raise ValueError("partition does not cover the group")
    return output


def constant_on_parts(
    values: Sequence[Fraction], parts: Sequence[Sequence[int]]
) -> bool:
    return all(all(values[index] == values[part[0]] for index in part) for part in parts)


def krawtchouk(order: int, shell: int, point_weight: int) -> int:
    lower = max(0, shell - (order - point_weight))
    upper = min(point_weight, shell)
    return sum(
        (-1) ** intersection
        * math.comb(point_weight, intersection)
        * math.comb(order - point_weight, shell - intersection)
        for intersection in range(lower, upper + 1)
    )


def hamming_guardrail() -> dict[str, Any]:
    rows = []
    all_shell_identities = True
    for order in range(8, 129, 4):
        half = order // 2
        quarter = order // 4
        shells = (half - 3, half - 2, half + 2, half + 3)
        shell_sum = sum(krawtchouk(order, shell, half) for shell in shells)
        formula = 2 * (-1) ** (quarter + 1) * math.comb(half, quarter - 1)
        all_shell_identities &= shell_sum == formula
        kappa = abs(shell_sum) / (2**order)
        image = math.comb(order, half)
        normalized_lower = kappa**3 * image**1.75 / (2 * order) ** 2
        rows.append(
            {
                "n": order,
                "signed_kernel_numerator": shell_sum,
                "formula_numerator": formula,
                "kernel_absolute_value": kappa,
                "image_size": image,
                "normalized_lower_bound": normalized_lower,
                "normalized_log_rate": math.log(normalized_lower) / order,
            }
        )

    order = 12
    half = order // 2
    color_bits = math.ceil(math.log2(order))
    classes: dict[int, list[tuple[int, ...]]] = {}
    for support in itertools.combinations(range(order), half):
        color = 0
        for index in support:
            color ^= index
        classes.setdefault(color, []).append(support)
    rim_free = True
    for supports in classes.values():
        support_sets = [set(support) for support in supports]
        for left_index, left in enumerate(support_sets):
            for right in support_sets[left_index + 1 :]:
                if len(left.intersection(right)) >= half - 1:
                    rim_free = False
    largest_class = max(map(len, classes.values()))
    image = math.comb(order, half)
    color_floor = image / (2**color_bits)
    return {
        "shell_rows": rows,
        "color_census": {
            "n": order,
            "image_size": image,
            "color_bits": color_bits,
            "nonempty_colors": len(classes),
            "largest_class": largest_class,
            "pigeonhole_floor": color_floor,
        },
        "scope": "source-free ambient guardrail; not a post-atlas RS falsifier",
        "checks": {
            "exact_krawtchouk_shell_identity": all_shell_identities,
            "color_classes_are_rim_free": rim_free,
            "color_pigeonhole_bound": largest_class + TOL >= color_floor,
            "positive_asymptotic_exponent_printed": True,
            "not_source_semantic_falsifier": True,
        },
    }


def commutator_guardrail() -> dict[str, Any]:
    order = 8
    band = {1, 2, 3, 5}
    parts = ((0, 1, 2), (3, 4), (5, 6, 7))
    u = [Fraction(value) for value in (1, 0, 1, 1, 0, 0, 1, 0)]
    g = [Fraction(value, 11) for value in (3, -2, 5, 1, -4, 2, 0, 6)]
    projected_g = walsh_project(g, band)
    r = projected_g
    expected_empty = dot(
        conditional_expectation(u, parts), conditional_expectation(r, parts)
    )
    projected_u = walsh_project(u, band)
    e_projected_u = conditional_expectation(projected_u, parts)
    projected_e_u = walsh_project(conditional_expectation(u, parts), band)
    commutator = subtract(projected_e_u, e_projected_u)
    reconstructed = dot(e_projected_u, g) + dot(commutator, g)
    pairing = dot(commutator, g)
    holder_rhs = lp(commutator, 4.0) * lp(g, 4.0 / 3.0)
    return {
        "group": "F_2^3",
        "band": sorted(band),
        "partition": [list(part) for part in parts],
        "empty_charge": str(expected_empty),
        "reconstructed_charge": str(reconstructed),
        "commutator": [str(value) for value in commutator],
        "commutator_pairing": str(pairing),
        "holder_rhs": holder_rhs,
        "checks": {
            "commutator_identity_exact": expected_empty == reconstructed,
            "commutator_is_nonzero": any(value != 0 for value in commutator),
            "holder_guard": abs(float(pairing)) <= holder_rhs + TOL,
        },
    }


def equitable_reduction_regression() -> dict[str, Any]:
    order = 8
    band = {1, 2, 3, 5}
    parts = ((0, 1), (2, 3), (4, 5), (6, 7))
    f = [Fraction(value) for value in (0, 0, 2, 2, 1, 1, 3, 3)]
    range_invariant = True
    for part in parts:
        basis = [Fraction(int(index in part)) for index in range(order)]
        range_invariant &= constant_on_parts(walsh_project(basis, band), parts)
    projected_f = walsh_project(f, band)
    dual_numerator = [value**3 for value in projected_f]
    projected_dual = walsh_project(dual_numerator, band)
    positive_counts = [
        count if weight > 0 else Fraction(0)
        for count, weight in zip(f, projected_dual)
    ]
    maximum_layer = int(max(positive_counts))
    layers = [
        [Fraction(int(count >= layer)) for count in positive_counts]
        for layer in range(1, maximum_layer + 1)
    ]
    commutator_zero = True
    layer_measurable = True
    projected_layer_measurable = True
    within_active_parts_zero = True
    for layer in layers:
        e_layer = conditional_expectation(layer, parts)
        projected_layer = walsh_project(layer, band)
        e_projected = conditional_expectation(projected_layer, parts)
        projected_e = walsh_project(e_layer, band)
        commutator_zero &= e_projected == projected_e
        layer_measurable &= constant_on_parts(layer, parts)
        projected_layer_measurable &= constant_on_parts(projected_layer, parts)
        active_parts = [part for part in parts if any(layer[index] for index in part)]
        within_active_parts_zero &= all(
            projected_layer[index] == projected_layer[part[0]]
            for part in active_parts
            for index in part
        )
    return {
        "group": "F_2^3",
        "band": sorted(band),
        "partition": [list(part) for part in parts],
        "layers": [[int(value) for value in layer] for layer in layers],
        "checks": {
            "EQ1_f_is_partition_measurable": constant_on_parts(f, parts),
            "EQ2_partition_range_invariant": range_invariant,
            "EQ2_commutator_zero_on_layers": commutator_zero,
            "norming_dual_numerator_measurable": constant_on_parts(
                dual_numerator, parts
            ),
            "root_weight_measurable": constant_on_parts(projected_dual, parts),
            "selected_layers_measurable": layer_measurable,
            "projected_layers_measurable": projected_layer_measurable,
            "within_active_parts_residual_zero": within_active_parts_zero,
        },
    }


def maximal_band_regression() -> dict[str, Any]:
    full_trials = 0
    ambient_trials = 0
    maximum_full_ratio = 0.0
    maximum_ambient_fourth = Fraction(0)
    for order in range(2, 97):
        for support in range(order + 1):
            fourth = Fraction(support * (order - support) ** 4, order**4)
            fourth += Fraction((order - support) * support**4, order**4)
            bound = 2 * support
            if fourth > bound:
                raise AssertionError("maximal-band fourth moment bound failed")
            if support:
                maximum_full_ratio = max(maximum_full_ratio, float(fourth / support))
            full_trials += 1
            for image in range(max(1, support), order + 1):
                normalized_fourth = Fraction(
                    (order - image) * support**4, order**4 * image
                )
                comparison = Fraction(image**3 * (order - image), order**4)
                if normalized_fourth > comparison or comparison > 1:
                    raise AssertionError("maximal-band ambient bound failed")
                maximum_ambient_fourth = max(
                    maximum_ambient_fourth, normalized_fourth
                )
                ambient_trials += 1
    return {
        "group_orders": [2, 96],
        "full_trials": full_trials,
        "ambient_trials": ambient_trials,
        "maximum_fourth_moment_per_support": maximum_full_ratio,
        "maximum_normalized_ambient_fourth_power": float(maximum_ambient_fourth),
        "checks": {
            "quartic_bound_at_most_2L": True,
            "normalized_ambient_bound_at_most_one": True,
        },
    }


def quantize(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 9)
    if isinstance(value, dict):
        return {key: quantize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [quantize(item) for item in value]
    if isinstance(value, tuple):
        return [quantize(item) for item in value]
    return value


def build_payload() -> dict[str, Any]:
    return quantize(
        {
            "certificate_id": "selected-owner-cube-mean-boundary-v1",
            "source_revision": SOURCE_REVISION,
            "status": (
                "PROVED_FINITE_BOUNDARIES_AND_MAXIMAL_BAND__"
                "SOURCE_AL4_AND_PAID_ADMISSION_OPEN"
            ),
            "hamming_guardrail": hamming_guardrail(),
            "commutator_guardrail": commutator_guardrail(),
            "equitable_reduction": equitable_reduction_regression(),
            "maximal_band": maximal_band_regression(),
            "open_obligations": [
                "source-specific ambient leakage AL4",
                "non-equitable within-image cube localization",
                "commutator control or signed nonempty-mode compression",
                "paid selected-owner cube-spectrum admission",
            ],
            "nonclaims": [
                "the Hamming guardrail is not a post-atlas RS falsifier",
                "EQ3 is assumed rather than proved by the equitable reduction",
                "EQ4 paid admission is not proved",
                "no stable paper theorem or finite deployed row is closed",
            ],
        }
    )


def validate(payload: dict[str, Any]) -> bool:
    blocks = (
        "hamming_guardrail",
        "commutator_guardrail",
        "equitable_reduction",
        "maximal_band",
    )
    if not all(all(payload[block]["checks"].values()) for block in blocks):
        return False
    hamming = payload["hamming_guardrail"]
    if any(
        row["signed_kernel_numerator"] != row["formula_numerator"]
        for row in hamming["shell_rows"]
    ):
        return False
    commutator = payload["commutator_guardrail"]
    if commutator["empty_charge"] != commutator["reconstructed_charge"]:
        return False
    if not any(Fraction(value) != 0 for value in commutator["commutator"]):
        return False
    maximal = payload["maximal_band"]
    return maximal["full_trials"] == 4750 and maximal["ambient_trials"] == 156750


def print_summary(payload: dict[str, Any]) -> None:
    hamming = payload["hamming_guardrail"]
    commutator = payload["commutator_guardrail"]
    equitable = payload["equitable_reduction"]
    maximal = payload["maximal_band"]
    print("SELECTED-OWNER CUBE-MEAN BOUNDARY")
    print(f"status                              = {payload['status']}")
    print(
        "Krawtchouk shell rows              = "
        f"{len(hamming['shell_rows'])} exact"
    )
    print(
        "Hamming n=12 largest color class   = "
        f"{hamming['color_census']['largest_class']}"
    )
    print(
        "commutator nonzero                 = "
        f"{commutator['checks']['commutator_is_nonzero']}"
    )
    print(
        "equitable checks                   = "
        f"{sum(equitable['checks'].values())}/{len(equitable['checks'])}"
    )
    print(f"maximal-band full trials            = {maximal['full_trials']}")
    print(f"maximal-band ambient trials         = {maximal['ambient_trials']}")
    print(f"RESULT                              = {'PASS' if validate(payload) else 'FAIL'}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--tamper-selftest", action="store_true")
    args = parser.parse_args()

    expected = build_payload()
    if args.tamper_selftest:
        semantic_tamper = json.loads(json.dumps(expected))
        semantic_tamper["hamming_guardrail"]["checks"][
            "not_source_semantic_falsifier"
        ] = False
        data_tamper = json.loads(json.dumps(expected))
        data_tamper["hamming_guardrail"]["shell_rows"][0][
            "formula_numerator"
        ] += 1
        caught = int(not validate(semantic_tamper)) + int(not validate(data_tamper))
        if caught != 2:
            raise SystemExit(f"tamper self-test failed: caught {caught}/2")
        print("TAMPER SELF-TEST: PASS (2/2)")
        return 0
    if args.write:
        CERTIFICATE.parent.mkdir(parents=True, exist_ok=True)
        CERTIFICATE.write_text(
            json.dumps(expected, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.check:
        actual = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
        if actual != expected:
            raise SystemExit("certificate mismatch")
    print_summary(expected)
    return 0 if validate(expected) else 1


if __name__ == "__main__":
    raise SystemExit(main())
