#!/usr/bin/env python3
"""Verify finite identities for the selected-owner cube-mean boundary.

The script checks exact finite guardrails, sharp ambient localization,
same-owner packing, and the maximal-band theorem.  It does not prove the
signed selected-owner ambient-kernel inverse, non-equitable localization,
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


def cross_block_localization_regression() -> dict[str, Any]:
    sharp_projection = walsh_project(
        [Fraction(1), Fraction(0)], {1}
    )
    sharp_ambient_square = sharp_projection[1] ** 2
    sharp_input_square = Fraction(1)

    trials = 0
    maximum_cross_block_square = Fraction(0)
    maximum_load_ratio_fourth = Fraction(0)
    bands_by_order = {
        2: [{1}],
        4: [
            set(indices)
            for size in range(1, 4)
            for indices in itertools.combinations(range(1, 4), size)
        ],
        8: [{1}, {1, 2, 3, 5}, {1, 3, 5, 7}, set(range(1, 8))],
    }
    for order, bands in bands_by_order.items():
        for states in itertools.product(range(3), repeat=order):
            image = {index for index, state in enumerate(states) if state > 0}
            selected = {index for index, state in enumerate(states) if state == 2}
            outside = set(range(order)).difference(image)
            if not selected or not outside:
                continue
            layer = [Fraction(int(index in selected)) for index in range(order)]
            mass = len(selected)
            for band in bands:
                projected = walsh_project(layer, band)
                ambient = [projected[index] for index in sorted(outside)]
                second = sum((value**2 for value in ambient), Fraction(0))
                fourth = sum((value**4 for value in ambient), Fraction(0))
                maximum = max((abs(value) for value in ambient), default=Fraction(0))
                if 4 * second > mass:
                    raise AssertionError("cross-block 1/2 bound failed")
                if 4 * fourth > mass * maximum**2:
                    raise AssertionError("load-weighted localization failed")
                maximum_cross_block_square = max(
                    maximum_cross_block_square, second / mass
                )
                if maximum:
                    # This is R_amb^4 / Lambda_amb^2; the theorem bounds it by 1/4.
                    load_ratio = Fraction(fourth, mass) / maximum**2
                    maximum_load_ratio_fourth = max(
                        maximum_load_ratio_fourth, load_ratio
                    )
                trials += 1

    order = 8
    band = {1, 2, 3, 5}
    image = {0, 1, 2, 3, 4}
    selected = {0, 2, 4}
    layer = [Fraction(int(index in selected)) for index in range(order)]
    ambient_dual = [
        Fraction(value, 13) if index not in image else Fraction(0)
        for index, value in enumerate((3, -2, 5, 1, -4, 2, 7, -3))
    ]
    projected_layer = walsh_project(layer, band)
    projected_dual = walsh_project(ambient_dual, band)
    ambient_pairing = sum(
        (
            projected_layer[index] * ambient_dual[index]
            for index in range(order)
            if index not in image
        ),
        Fraction(0),
    )
    selected_pullback = sum(
        (projected_dual[index] for index in selected), Fraction(0)
    )

    # Positive truncation is strictly stronger than signed localization.
    order = 4
    band = {1}
    kernel = walsh_project(
        [Fraction(int(index == 0)) for index in range(order)], band
    )
    image = {0, 1}
    off_image_point = 2
    terms = [kernel[off_image_point ^ syndrome] for syndrome in sorted(image)]
    signed_sum = sum(terms, Fraction(0))
    positive_sum = sum((max(term, Fraction(0)) for term in terms), Fraction(0))

    return {
        "small_walsh_trials": trials,
        "sharp_example": {
            "group": "F_2",
            "ambient_square": str(sharp_ambient_square),
            "input_square": str(sharp_input_square),
        },
        "maximum_cross_block_square": str(maximum_cross_block_square),
        "maximum_load_ratio_fourth": str(maximum_load_ratio_fourth),
        "ambient_pullback": {
            "ambient_pairing": str(ambient_pairing),
            "selected_pullback": str(selected_pullback),
        },
        "positive_part_guardrail": {
            "group": "F_2^2",
            "band": sorted(band),
            "off_image_point": off_image_point,
            "kernel_terms": [str(term) for term in terms],
            "signed_sum": str(signed_sum),
            "positive_part_sum": str(positive_sum),
        },
        "checks": {
            "sharp_constant_one_half": (
                sharp_ambient_square == Fraction(1, 4) * sharp_input_square
            ),
            "cross_block_bound_exact": maximum_cross_block_square <= Fraction(1, 4),
            "load_weighted_bound_exact": maximum_load_ratio_fourth <= Fraction(1, 4),
            "ambient_pullback_exact": ambient_pairing == selected_pullback,
            "positive_part_strictly_stronger": (
                signed_sum == 0 and positive_sum > 0
            ),
        },
    }


def greedy_owner_family(
    supports: Sequence[tuple[int, ...]], k: int
) -> list[tuple[int, ...]]:
    family: list[tuple[int, ...]] = []
    family_sets: list[set[int]] = []
    for support in supports:
        support_set = set(support)
        if all(len(support_set.intersection(other)) < k for other in family_sets):
            family.append(support)
            family_sets.append(support_set)
    return family


def binary_entropy(value: float) -> float:
    if value <= 0.0 or value >= 1.0:
        return 0.0
    return -value * math.log2(value) - (1.0 - value) * math.log2(1.0 - value)


def owner_packing_regression() -> dict[str, Any]:
    packing_rows = 0
    johnson_rows = 0
    owner_dichotomy_rows = 0
    largest_family = 0
    for order in range(5, 13):
        for agreement in range(2, order):
            supports = list(itertools.combinations(range(order), agreement))
            orderings = (
                supports,
                list(reversed(supports)),
                sorted(
                    supports,
                    key=lambda support: (
                        sum(index**2 for index in support),
                        support,
                    ),
                ),
            )
            for dimension in range(1, agreement):
                for ordering in orderings:
                    family = greedy_owner_family(ordering, dimension)
                    family_sets = [set(support) for support in family]
                    if any(
                        len(left.intersection(right)) >= dimension
                        for index, left in enumerate(family_sets)
                        for right in family_sets[index + 1 :]
                    ):
                        raise AssertionError("same-owner intersection guard failed")
                    if len(family) * math.comb(agreement, dimension) > math.comb(
                        order, dimension
                    ):
                        raise AssertionError("same-owner k-packing bound failed")
                    denominator = agreement**2 - order * (dimension - 1)
                    if denominator > 0:
                        if len(family) * denominator > order * (
                            agreement - dimension + 1
                        ):
                            raise AssertionError("Johnson incidence bound failed")
                        johnson_rows += 1
                    largest_family = max(largest_family, len(family))
                    packing_rows += 1

    for total_load in range(1, 65):
        for owner_count in range(1, total_load + 1):
            quotient, remainder = divmod(total_load, owner_count)
            extremal_loads = [quotient + 1] * remainder + [quotient] * (
                owner_count - remainder
            )
            if max(extremal_loads) != math.ceil(total_load / owner_count):
                raise AssertionError("represented-owner dichotomy failed")
            owner_dichotomy_rows += 1

    phase_inputs = (
        ("paid_below_johnson_full_slice_image", 0.40, 0.17),
        ("paid_below_johnson_second", 0.70, 0.50),
        ("unpaid_below_johnson", 0.55, 0.45),
    )
    phase_rows = []
    for name, alpha, kappa in phase_inputs:
        slice_entropy = binary_entropy(alpha)
        # This is the largest feasible image rate because L <= binom(N,a).
        image_rate = slice_entropy
        owner_rate = binary_entropy(kappa) - alpha * binary_entropy(kappa / alpha)
        margin = owner_rate - image_rate / 2.0
        phase_rows.append(
            {
                "name": name,
                "alpha": alpha,
                "kappa": kappa,
                "slice_entropy_bits": slice_entropy,
                "image_rate_bits": image_rate,
                "owner_packing_rate_bits": owner_rate,
                "criterion_margin_bits": margin,
                "above_johnson": alpha**2 > kappa,
                "packing_pays": margin <= 0.0,
            }
        )

    deployed = {
        "name": "KoalaBear MCA",
        "N": 2_097_152,
        "k": 1_048_576,
        "a": 1_116_048,
        "p": 2_130_706_433,
        "w": 67_471,
    }
    deployed["johnson_integer_margin"] = (
        deployed["a"] ** 2 - deployed["N"] * (deployed["k"] - 1)
    )
    deployed["above_johnson"] = deployed["johnson_integer_margin"] > 0
    log_owner_ratio = (
        math.lgamma(deployed["N"] + 1)
        - math.lgamma(deployed["k"] + 1)
        - math.lgamma(deployed["N"] - deployed["k"] + 1)
        - math.lgamma(deployed["a"] + 1)
        + math.lgamma(deployed["k"] + 1)
        + math.lgamma(deployed["a"] - deployed["k"] + 1)
    ) / math.log(2.0)
    image_upper = deployed["w"] * math.log2(deployed["p"])
    slice_log2 = (
        math.lgamma(deployed["N"] + 1)
        - math.lgamma(deployed["a"] + 1)
        - math.lgamma(deployed["N"] - deployed["a"] + 1)
    ) / math.log(2.0)
    deployed["owner_packing_log2"] = round(log_owner_ratio, 3)
    deployed["image_upper_log2"] = round(image_upper, 3)
    deployed["slice_log2"] = round(slice_log2, 3)
    deployed["slice_minus_image_log2"] = round(slice_log2 - image_upper, 3)
    deployed["optimistic_image_is_slice_feasible"] = image_upper <= slice_log2
    deployed["optimistic_margin_log2"] = round(
        log_owner_ratio - image_upper / 2.0, 3
    )
    deployed["packing_pays_optimistically"] = (
        deployed["optimistic_margin_log2"] <= 0.0
    )

    return {
        "packing_rows": packing_rows,
        "johnson_rows": johnson_rows,
        "owner_dichotomy_rows": owner_dichotomy_rows,
        "largest_greedy_family": largest_family,
        "phase_rows": phase_rows,
        "deployed_audit": deployed,
        "checks": {
            "same_owner_k_packing": True,
            "represented_owner_dichotomy_sharp": owner_dichotomy_rows == 2080,
            "johnson_incidence_when_enabled": True,
            "phase_grid_contains_below_johnson_payment": (
                not phase_rows[0]["above_johnson"] and phase_rows[0]["packing_pays"]
            ),
            "phase_grid_respects_slice_entropy": all(
                row["image_rate_bits"] <= row["slice_entropy_bits"]
                for row in phase_rows
            ),
            "phase_grid_contains_unpaid_row": not phase_rows[2]["packing_pays"],
            "deployed_is_below_johnson": not deployed["above_johnson"],
            "deployed_optimistic_image_is_slice_feasible": deployed[
                "optimistic_image_is_slice_feasible"
            ],
            "deployed_not_paid_even_optimistically": not deployed[
                "packing_pays_optimistically"
            ],
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
                "PROVED_FINITE_BOUNDARIES_LOCALIZATION_OWNER_PACKING_AND_"
                "MAXIMAL_BAND__SIGNED_SOURCE_INVERSION_AND_ADMISSION_OPEN"
            ),
            "hamming_guardrail": hamming_guardrail(),
            "ambient_localization": cross_block_localization_regression(),
            "owner_packing": owner_packing_regression(),
            "commutator_guardrail": commutator_guardrail(),
            "equitable_reduction": equitable_reduction_regression(),
            "maximal_band": maximal_band_regression(),
            "open_obligations": [
                "signed selected-owner ambient-kernel inversion outside paid owner regimes",
                "non-equitable within-image cube localization",
                "commutator control or signed nonempty-mode compression",
                "paid selected-owner cube-spectrum admission",
            ],
            "nonclaims": [
                "the Hamming guardrail is not a post-atlas RS falsifier",
                "positive-part ambient emission is stronger than signed localization",
                "the ambient diagnostic dual is not the original natural charge",
                "the Johnson corollary and owner packing do not pay the deployed row",
                "EQ3 is assumed rather than proved by the equitable reduction",
                "EQ4 paid admission is not proved",
                "no stable paper theorem or finite deployed row is closed",
            ],
        }
    )


def validate(payload: dict[str, Any]) -> bool:
    blocks = (
        "hamming_guardrail",
        "ambient_localization",
        "owner_packing",
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
    ambient = payload["ambient_localization"]
    if ambient["sharp_example"]["ambient_square"] != "1/4":
        return False
    if ambient["ambient_pullback"]["ambient_pairing"] != ambient[
        "ambient_pullback"
    ]["selected_pullback"]:
        return False
    if ambient["positive_part_guardrail"]["signed_sum"] != "0":
        return False
    if Fraction(
        ambient["positive_part_guardrail"]["positive_part_sum"]
    ) <= 0:
        return False
    owner = payload["owner_packing"]
    if any(
        row["image_rate_bits"] > row["slice_entropy_bits"]
        for row in owner["phase_rows"]
    ):
        return False
    if owner["deployed_audit"]["johnson_integer_margin"] >= 0:
        return False
    if not owner["deployed_audit"]["optimistic_image_is_slice_feasible"]:
        return False
    if owner["deployed_audit"]["slice_minus_image_log2"] <= 0:
        return False
    if owner["deployed_audit"]["optimistic_margin_log2"] <= 0:
        return False
    if owner["deployed_audit"]["packing_pays_optimistically"]:
        return False
    maximal = payload["maximal_band"]
    return maximal["full_trials"] == 4750 and maximal["ambient_trials"] == 156750


def print_summary(payload: dict[str, Any]) -> None:
    hamming = payload["hamming_guardrail"]
    ambient = payload["ambient_localization"]
    owner = payload["owner_packing"]
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
    print(f"ambient localization trials         = {ambient['small_walsh_trials']}")
    print(
        "sharp cross-block square           = "
        f"{ambient['maximum_cross_block_square']}"
    )
    print(f"same-owner packing rows             = {owner['packing_rows']}")
    print(f"owner-dichotomy rows                = {owner['owner_dichotomy_rows']}")
    print(f"above-Johnson incidence rows        = {owner['johnson_rows']}")
    print(
        "deployed optimistic margin (bits)  = "
        f"{owner['deployed_audit']['optimistic_margin_log2']}"
    )
    print(
        "deployed slice/image slack (bits)  = "
        f"{owner['deployed_audit']['slice_minus_image_log2']}"
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
        sign_tamper = json.loads(json.dumps(expected))
        sign_tamper["ambient_localization"]["positive_part_guardrail"][
            "signed_sum"
        ] = "1/4"
        coverage_tamper = json.loads(json.dumps(expected))
        coverage_tamper["owner_packing"]["deployed_audit"][
            "packing_pays_optimistically"
        ] = True
        phase_tamper = json.loads(json.dumps(expected))
        phase_tamper["owner_packing"]["phase_rows"][0][
            "image_rate_bits"
        ] = phase_tamper["owner_packing"]["phase_rows"][0][
            "slice_entropy_bits"
        ] + 0.25
        image_feasibility_tamper = json.loads(json.dumps(expected))
        image_feasibility_tamper["owner_packing"]["deployed_audit"][
            "optimistic_image_is_slice_feasible"
        ] = False
        caught = sum(
            int(not validate(payload))
            for payload in (
                semantic_tamper,
                data_tamper,
                sign_tamper,
                coverage_tamper,
                phase_tamper,
                image_feasibility_tamper,
            )
        )
        if caught != 6:
            raise SystemExit(f"tamper self-test failed: caught {caught}/6")
        print("TAMPER SELF-TEST: PASS (6/6)")
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
