#!/usr/bin/env python3
"""Audit the slack-two depth-two Kummer-Weil saturation certificate."""

from __future__ import annotations

import math
from itertools import product
from typing import Sequence, Tuple

from m1_support_occupancy_scan import (
    all_residual_packets_lift_active,
    kummer_quadratic_uniform_prime_threshold,
    quotient_limited_pair_parameter_bound,
    quotient_window_label_nonprincipal_bound,
    quotient_window_label_l1_data,
    quotient_window_label_triple_count,
    scan_supports,
    slack_two_second_fixed_window_data,
    slack_two_second_fixed_window_kummer_saturation_data,
    slack_two_second_quotient_window_union_kummer_saturation_data,
    slack_two_second_quotient_window_reduction_data,
    slack_two_second_kummer_saturation_data,
    slack_two_second_superboundary_shape_ledger,
    slack_two_second_two_fiber_kummer_saturation_data,
    slack_two_second_two_fiber_union_reduction_data,
    slack_two_second_two_fiber_window_data,
)
from mca_slope_scan import make_domain


CASES = (
    # Index-two proper subgroups where the certificate is positive.
    (383, 191, True),
    (769, 384, True),
    # A high-index sample from the non-field-filling side of the existing PR.
    (193, 6, False),
)

LIFT_CASES = (
    # The only quotient fiber is left unused, so every packet is active.
    (17, 16, 1, 16, 4, True),
    # Six quotient fibers, two whole fibers selected, four left for any packet.
    (97, 48, 6, 8, 20, True),
    # Only three quotient fibers remain, so four-fiber packets are not certified.
    (97, 48, 6, 8, 28, False),
)

LIFT_BOUND_CASES = (
    # Only one quotient fiber remains, giving a nontrivial exact-slope bound.
    (97, 48, 6, 8, 44, True),
    # Three quotient fibers remain; the bound is true but field-trivial here.
    (97, 48, 6, 8, 28, False),
)

KERNEL_REDUCTION_CASES = (
    # R=1: active normalized shapes are exactly the quotient-kernel catalog.
    (97, 48, 6, 8, 44),
)

TWO_FIBER_KUMMER_CASES = (
    # Small lift-limited sample: a fixed two-fiber window is not saturated.
    (97, 48, 6, False),
    # Full-domain N=3 sample where the two-fiber certificate is positive.
    (919, 918, 3, True),
    # Proper index-two N=3 sample above the uniform two-fiber threshold.
    (7351, 3675, 3, True),
)

TWO_FIBER_UNION_CASES = (
    # R=2: no fixed two-fiber certificate, but the union saturates.
    (97, 48, 6, 8, 36),
)

R_WINDOW_CASES = (
    # R=1: the general window reduction specializes to the kernel reduction.
    (97, 48, 6, 8, 44, False),
    # R=2: the general reduction agrees with the two-fiber union.
    (97, 48, 6, 8, 36, True),
    # R=3: exact-support saturation below the all-shapes R=4 gate.
    (97, 48, 6, 8, 28, True),
)

FIXED_WINDOW_KUMMER_CASES = (
    # Small R=3 sample below the conservative fixed-window threshold.
    (97, 48, 6, 3, False),
    # Positive fixed R=3 certificate for a full-domain N=4 window.
    (2213, 2212, 4, 3, True),
)

R_WINDOW_UNION_KUMMER_CASES = (
    # Exact R=2 union saturation, but below the union Kummer threshold.
    (97, 48, 6, 2, False, False),
    # The exact R=2 L1 certificate succeeds while the L1 bound fails.
    (181, 180, 3, 2, True, False),
    # The exact R=3 coefficient histogram improves the bounded L1 threshold.
    (113, 112, 4, 3, True, False),
)

SCAN_LABEL_CASES = (
    # Public scanner regression for the R=2 union-saturated label.
    (19, 18, 8, 2, 3, "r2_union_saturated"),
)


def divisor_power_failure_count(character_order: int, square_kernel_index: int) -> int:
    square_coset_index = character_order * square_kernel_index
    failures = 0
    for a in range(character_order):
        for b in range(character_order):
            for c in range(character_order):
                for d in range(square_coset_index):
                    if (a, b, c, d) == (0, 0, 0, 0):
                        continue
                    divisor_exponents = (
                        square_kernel_index * a,
                        square_kernel_index * b,
                        square_kernel_index * c,
                        d,
                    )
                    if all(
                        exponent % square_coset_index == 0
                        for exponent in divisor_exponents
                    ):
                        failures += 1
    return failures


def two_fiber_divisor_power_failure_count(
    kernel_character_order: int,
    square_coset_index: int,
) -> int:
    failures = 0
    for a in range(kernel_character_order):
        for b in range(kernel_character_order):
            for c in range(kernel_character_order):
                for d in range(square_coset_index):
                    if (a, b, c, d) == (0, 0, 0, 0):
                        continue
                    divisor_exponents = (a, b, c, d)
                    if all(exponent == 0 for exponent in divisor_exponents):
                        failures += 1
    return failures


def principal_open_count(p: int) -> int:
    count = 0
    for u in range(p):
        for v in range(p):
            w = (-1 - u - v) % p
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if u and v and w and shape_slope:
                count += 1
    return count


def degeneracy_line_union_count(p: int) -> int:
    count = 0
    for u in range(p):
        for v in range(p):
            w = (-1 - u - v) % p
            if u == 1 or v == 1 or w == 1 or u == v or u == w or v == w:
                count += 1
    return count


def square_coset_counts(p: int, domain: Sequence[int]) -> Tuple[int, int]:
    domain_set = set(domain)
    square_image = {x * x % p for x in domain}
    nonzero_cosets = set()
    for u in domain:
        for v in domain:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in domain_set or len(set(values)) != 4:
                continue
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                continue
            nonzero_cosets.add(
                min((shape_slope * square) % p for square in square_image)
            )
    return len(nonzero_cosets), (p - 1) // len(square_image)


def lift_limited_bound_formula(
    quotient_order: int,
    fiber_size: int,
    remaining_fibers: int,
) -> int:
    max_touched = min(remaining_fibers, 4, quotient_order)
    return sum(
        math.comb(quotient_order - 1, touched - 1)
        * (touched * fiber_size) ** 2
        for touched in range(1, max_touched + 1)
    )


def direct_quotient_window_label_triple_count(
    quotient_order: int,
    window_size: int,
) -> int:
    return sum(
        1
        for labels in product(range(quotient_order), repeat=3)
        if len({0, *labels}) <= window_size
    )


def quotient_label_sum(value: int, quotient_order: int) -> int:
    return quotient_order - 1 if value % quotient_order == 0 else -1


def quotient_window_label_coefficient(
    quotient_order: int,
    window_size: int,
    triple: Tuple[int, int, int],
) -> int:
    r, s, t = triple
    if window_size == 1:
        return 1
    if window_size == 2:
        zero_subset_count = 0
        frequencies = (r, s, t)
        for mask in range(1, 8):
            subset_sum = sum(
                frequencies[index]
                for index in range(3)
                if mask & (1 << index)
            )
            if subset_sum % quotient_order == 0:
                zero_subset_count += 1
        return zero_subset_count * quotient_order - 6
    if window_size == 3:
        full_cube = quotient_order ** 3 if (r, s, t) == (0, 0, 0) else 0
        distinct_nonzero = (
            quotient_label_sum(r, quotient_order)
            * quotient_label_sum(s, quotient_order)
            * quotient_label_sum(t, quotient_order)
            - quotient_label_sum(r + s, quotient_order)
            * quotient_label_sum(t, quotient_order)
            - quotient_label_sum(r + t, quotient_order)
            * quotient_label_sum(s, quotient_order)
            - quotient_label_sum(s + t, quotient_order)
            * quotient_label_sum(r, quotient_order)
            + 2 * quotient_label_sum(r + s + t, quotient_order)
        )
        return full_cube - distinct_nonzero
    return 0


def direct_quotient_window_label_nonprincipal_bound(
    quotient_order: int,
    window_size: int,
) -> int:
    return max(
        abs(
            quotient_window_label_coefficient(
                quotient_order,
                window_size,
                (r, s, t),
            )
        )
        for r in range(quotient_order)
        for s in range(quotient_order)
        for t in range(quotient_order)
        if (r, s, t) != (0, 0, 0)
    )


def direct_quotient_window_label_l1_data(
    quotient_order: int,
    window_size: int,
) -> Tuple[
    int,
    Tuple[Tuple[int, int], ...],
    Tuple[Tuple[int, int], ...],
]:
    total = 0
    zero_subset_histogram = {}
    coefficient_histogram = {}
    for r in range(quotient_order):
        for s in range(quotient_order):
            for t in range(quotient_order):
                coefficient = quotient_window_label_coefficient(
                    quotient_order,
                    window_size,
                    (r, s, t),
                )
                total += abs(coefficient)
                coefficient_histogram[coefficient] = (
                    coefficient_histogram.get(coefficient, 0) + 1
                )
                if window_size == 2:
                    zero_subset_count = sum(
                        (
                            (sum(
                                (r, s, t)[index]
                                for index in range(3)
                                if mask & (1 << index)
                            )
                            % quotient_order)
                            == 0
                        )
                        for mask in range(1, 8)
                    )
                    zero_subset_histogram[zero_subset_count] = (
                        zero_subset_histogram.get(zero_subset_count, 0) + 1
                    )
    return (
        total,
        tuple(sorted(zero_subset_histogram.items())),
        tuple(sorted(coefficient_histogram.items())),
    )


def direct_ambient_window_label_l1_bound(
    ambient_character_order: int,
    quotient_order: int,
    window_size: int,
    square_coset_index: int,
) -> int:
    label_triples = direct_quotient_window_label_triple_count(
        quotient_order,
        window_size,
    )
    quotient_l1_bound = sum(
        abs(
            quotient_window_label_coefficient(
                quotient_order,
                window_size,
                (
                    r % quotient_order,
                    s % quotient_order,
                    t % quotient_order,
                ),
            )
        )
        for r in range(ambient_character_order)
        for s in range(ambient_character_order)
        for t in range(ambient_character_order)
    )
    return square_coset_index * quotient_l1_bound - label_triples


def kernel_fiber_reduction_counts(
    p: int,
    domain: Sequence[int],
    quotient_order: int,
) -> Tuple[int, int, int, int, int]:
    kernel = tuple(domain[index] for index in range(0, len(domain), quotient_order))
    kernel_set = set(kernel)
    square_image = {x * x % p for x in domain}
    nonzero_cosets = set()
    parameter_count = 0
    zero_parameter_count = 0
    for u in kernel:
        for v in kernel:
            w = (-1 - u - v) % p
            values = (1, u, v, w)
            if w not in kernel_set or len(set(values)) != 4:
                continue
            parameter_count += 1
            shape_slope = (-(u * u + v * v + u * v + u + v + 1)) % p
            if shape_slope == 0:
                zero_parameter_count += 1
                continue
            nonzero_cosets.add(
                min((shape_slope * square) % p for square in square_image)
            )
    slope_count = (1 if zero_parameter_count else 0) + (
        len(nonzero_cosets) * len(square_image)
    )
    return (
        len(kernel),
        parameter_count,
        zero_parameter_count,
        len(nonzero_cosets),
        min(p, slope_count),
    )


def main() -> None:
    checked = []
    for p, n, expected_certificate in CASES:
        _, domain = make_domain(p, n, None)
        certificate = slack_two_second_kummer_saturation_data(p, n)
        failures = divisor_power_failure_count(
            int(certificate["character_order"]),
            int(certificate["square_kernel_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        deligne_constant = (radical_total - 1) ** 2
        if deligne_constant != int(certificate["deligne_constant"]):
            raise AssertionError((p, n, deligne_constant, certificate))
        if not bool(certificate["deligne_constant_check"]):
            raise AssertionError((p, n, certificate))
        principal_count = principal_open_count(p)
        if principal_count != int(certificate["principal_exact_count"]):
            raise AssertionError((p, n, principal_count, certificate))
        degeneracy_count = degeneracy_line_union_count(p)
        if degeneracy_count != int(certificate["degeneracy_line_union_count"]):
            raise AssertionError((p, n, degeneracy_count, certificate))
        coefficient_l1_bound = int(certificate["denominator"]) - 1
        if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        character_triple_count = int(certificate["character_order"]) ** 3
        square_coset_index = int(certificate["square_coset_index"])
        jacobi_l1_bound = character_triple_count - 1
        conic_l1_bound = square_coset_index - 1
        kummer_l1_bound = jacobi_l1_bound * (square_coset_index - 1)
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["nonprincipal_constant"]) * kummer_l1_bound
        )
        if (
            jacobi_l1_bound + conic_l1_bound + kummer_l1_bound
            != coefficient_l1_bound
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        lower_numerator = principal_count - (
            p * weighted_error_l1_bound
            + degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            1,
            (
                weighted_error_l1_bound
                + int(certificate["degeneracy_line_count"])
                * int(certificate["denominator"])
            ),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        nonzero_coset_count, total_coset_count = square_coset_counts(p, domain)
        saturates = nonzero_coset_count == total_coset_count
        certificate_positive = bool(certificate["saturation_certificate"])
        if certificate_positive != expected_certificate:
            raise AssertionError((p, n, certificate))
        if bool(certificate["uniform_threshold_applies"]) != certificate_positive:
            raise AssertionError((p, n, certificate))
        if certificate_positive and not saturates:
            raise AssertionError((p, n, nonzero_coset_count, total_coset_count))
        checked.append(
            (
                p,
                n,
                certificate_positive,
                certificate["uniform_prime_threshold"],
                failures,
                radical_total,
                deligne_constant,
                principal_count,
                degeneracy_count,
                nonzero_coset_count,
                total_coset_count,
            )
        )
    lift_checked = []
    for p, n, quotient_order, fiber_size, support_size, expected_gate in LIFT_CASES:
        _, domain = make_domain(p, n, None)
        gate, remaining_fibers, required_fibers = all_residual_packets_lift_active(
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            residual_size=4,
        )
        if gate != expected_gate:
            raise AssertionError(
                (p, n, quotient_order, fiber_size, support_size, gate)
            )
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if gate:
            if int(ledger["active_parameter_count"]) != int(
                ledger["parameter_count"]
            ):
                raise AssertionError((p, n, support_size, ledger))
            if int(ledger["active_nonzero_square_coset_count"]) != int(
                ledger["nonzero_square_coset_count"]
            ):
                raise AssertionError((p, n, support_size, ledger))
        lift_checked.append(
            (
                p,
                n,
                quotient_order,
                fiber_size,
                support_size,
                gate,
                remaining_fibers,
                required_fibers,
            )
        )
    lift_bound_checked = []
    for (
        p,
        n,
        quotient_order,
        fiber_size,
        support_size,
        expected_nontrivial,
    ) in LIFT_BOUND_CASES:
        _, domain = make_domain(p, n, None)
        whole_fibers = (support_size - 4) // fiber_size
        remaining_fibers = quotient_order - whole_fibers
        direct_bound = lift_limited_bound_formula(
            quotient_order,
            fiber_size,
            remaining_fibers,
        )
        helper_bound = quotient_limited_pair_parameter_bound(
            quotient_order=quotient_order,
            fiber_size=fiber_size,
            remaining_fibers=remaining_fibers,
            residual_size=4,
        )
        if direct_bound != helper_bound:
            raise AssertionError((p, n, support_size, direct_bound, helper_bound))
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        if int(ledger["lift_limited_parameter_bound"]) != direct_bound:
            raise AssertionError((p, n, support_size, ledger))
        slope_count = len(ledger["support_slope_histogram"])
        slope_bound = int(ledger["lift_limited_slope_bound"])
        if slope_count > slope_bound:
            raise AssertionError((p, n, support_size, slope_count, ledger))
        if bool(ledger["lift_limited_slope_bound_nontrivial"]) != (
            expected_nontrivial
        ):
            raise AssertionError((p, n, support_size, ledger))
        lift_bound_checked.append(
            (
                p,
                n,
                quotient_order,
                fiber_size,
                support_size,
                remaining_fibers,
                direct_bound,
                slope_count,
                slope_bound,
            )
        )
    kernel_checked = []
    for p, n, quotient_order, fiber_size, support_size in KERNEL_REDUCTION_CASES:
        _, domain = make_domain(p, n, None)
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        reduction = ledger["kernel_fiber_reduction"]
        if reduction is None:
            raise AssertionError((p, n, support_size, ledger))
        expected = kernel_fiber_reduction_counts(p, domain, quotient_order)
        observed = (
            int(reduction["kernel_order"]),
            int(reduction["parameter_count"]),
            int(reduction["zero_parameter_count"]),
            int(reduction["nonzero_square_coset_count"]),
            int(reduction["slope_count"]),
        )
        if observed != expected:
            raise AssertionError((p, n, support_size, observed, expected))
        if int(reduction["parameter_count"]) != int(
            ledger["active_parameter_count"]
        ):
            raise AssertionError((p, n, support_size, ledger))
        if int(reduction["zero_parameter_count"]) != int(
            ledger["active_zero_parameter_count"]
        ):
            raise AssertionError((p, n, support_size, ledger))
        if int(reduction["nonzero_square_coset_count"]) != int(
            ledger["active_nonzero_square_coset_count"]
        ):
            raise AssertionError((p, n, support_size, ledger))
        if int(reduction["slope_count"]) != len(ledger["support_slope_histogram"]):
            raise AssertionError((p, n, support_size, ledger))
        kernel_checked.append(
            (p, n, quotient_order, fiber_size, support_size, *observed)
        )
    two_fiber_checked = []
    for p, n, quotient_order, expected_certificate in TWO_FIBER_KUMMER_CASES:
        _, domain = make_domain(p, n, None)
        certificate = slack_two_second_two_fiber_kummer_saturation_data(
            p,
            n,
            quotient_order,
        )
        if certificate is None:
            raise AssertionError((p, n, quotient_order))
        failures = two_fiber_divisor_power_failure_count(
            int(certificate["kernel_character_order"]),
            int(certificate["square_coset_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        deligne_constant = (radical_total - 1) ** 2
        if deligne_constant != int(certificate["deligne_constant"]):
            raise AssertionError((p, n, deligne_constant, certificate))
        principal_count = principal_open_count(p)
        degeneracy_count = degeneracy_line_union_count(p)
        coefficient_l1_bound = int(certificate["coefficient_abs_bound"]) * (
            int(certificate["denominator"]) - 1
        )
        if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        character_triple_count = (
            int(certificate["kernel_character_order"]) ** 3
        )
        square_coset_index = int(certificate["square_coset_index"])
        jacobi_l1_bound = int(certificate["coefficient_abs_bound"]) * (
            character_triple_count - 1
        )
        conic_l1_bound = int(certificate["principal_weight"]) * (
            square_coset_index - 1
        )
        kummer_l1_bound = jacobi_l1_bound * (square_coset_index - 1)
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["nonprincipal_constant"]) * kummer_l1_bound
        )
        if (
            jacobi_l1_bound + conic_l1_bound + kummer_l1_bound
            != coefficient_l1_bound
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * weighted_error_l1_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            int(certificate["principal_weight"]),
            (
                weighted_error_l1_bound
                + int(certificate["degeneracy_line_count"])
                * int(certificate["denominator"])
            ),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        certificate_positive = bool(certificate["saturation_certificate"])
        if certificate_positive != expected_certificate:
            raise AssertionError((p, n, certificate))
        if (
            bool(certificate["uniform_threshold_applies"])
            and not certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        window = slack_two_second_two_fiber_window_data(
            p,
            domain,
            quotient_order,
        )
        if window is None:
            raise AssertionError((p, n, quotient_order))
        window_saturates = int(window["nonzero_square_coset_count"]) == int(
            window["total_nonzero_square_coset_count"]
        )
        if certificate_positive and not window_saturates:
            raise AssertionError((p, n, certificate, window))
        two_fiber_checked.append(
            (
                p,
                n,
                quotient_order,
                certificate_positive,
                certificate["kernel_character_order"],
                certificate["square_coset_index"],
                certificate["denominator"],
                certificate["uniform_prime_threshold"],
                window["parameter_count"],
                window["zero_parameter_count"],
                window["nonzero_square_coset_count"],
                window["total_nonzero_square_coset_count"],
            )
        )
    two_fiber_union_checked = []
    for p, n, quotient_order, fiber_size, support_size in TWO_FIBER_UNION_CASES:
        _, domain = make_domain(p, n, None)
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        reduction = slack_two_second_two_fiber_union_reduction_data(
            p,
            domain,
            quotient_order,
        )
        if reduction is None:
            raise AssertionError((p, n, quotient_order))
        remaining_fibers = int(ledger["lift_limited_remaining_fibers"])
        if remaining_fibers != 2:
            raise AssertionError((p, n, support_size, ledger))
        observed = (
            int(reduction["parameter_count"]),
            int(reduction["zero_parameter_count"]),
            int(reduction["nonzero_square_coset_count"]),
            int(reduction["slope_count"]),
        )
        expected = (
            int(ledger["active_parameter_count"]),
            int(ledger["active_zero_parameter_count"]),
            int(ledger["active_nonzero_square_coset_count"]),
            len(ledger["support_slope_histogram"]),
        )
        if observed != expected:
            raise AssertionError((p, n, support_size, observed, expected))
        if not bool(reduction["saturates_nonzero_square_cosets"]):
            raise AssertionError((p, n, support_size, reduction))
        per_window_cosets = tuple(
            int(profile["nonzero_square_coset_count"])
            for profile in reduction["per_window_profiles"]
        )
        if max(per_window_cosets) >= int(
            reduction["total_nonzero_square_coset_count"]
        ):
            raise AssertionError((p, n, support_size, reduction))
        two_fiber_union_checked.append(
            (
                p,
                n,
                quotient_order,
                support_size,
                remaining_fibers,
                *observed,
                per_window_cosets,
            )
        )
    r_window_checked = []
    for (
        p,
        n,
        quotient_order,
        fiber_size,
        support_size,
        expected_saturation,
    ) in R_WINDOW_CASES:
        _, domain = make_domain(p, n, None)
        ledger = slack_two_second_superboundary_shape_ledger(
            p=p,
            domain=domain,
            support_size=support_size,
            quotient_order=quotient_order,
            fiber_size=fiber_size,
        )
        reduction = slack_two_second_quotient_window_reduction_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
            remaining_fibers=int(ledger["lift_limited_remaining_fibers"]),
        )
        if reduction is None:
            raise AssertionError((p, n, support_size))
        observed = (
            int(reduction["parameter_count"]),
            int(reduction["zero_parameter_count"]),
            int(reduction["nonzero_square_coset_count"]),
            int(reduction["slope_count"]),
        )
        expected = (
            int(ledger["active_parameter_count"]),
            int(ledger["active_zero_parameter_count"]),
            int(ledger["active_nonzero_square_coset_count"]),
            len(ledger["support_slope_histogram"]),
        )
        if observed != expected:
            raise AssertionError((p, n, support_size, observed, expected))
        saturates = bool(reduction["saturates_nonzero_square_cosets"])
        if saturates != expected_saturation:
            raise AssertionError((p, n, support_size, reduction))
        r_window_checked.append(
            (
                p,
                n,
                quotient_order,
                support_size,
                reduction["remaining_fibers"],
                reduction["effective_window_size"],
                *observed,
                tuple(reduction["touched_fiber_histogram"]),
            )
        )
    fixed_window_kummer_checked = []
    for (
        p,
        n,
        quotient_order,
        window_size,
        expected_certificate,
    ) in FIXED_WINDOW_KUMMER_CASES:
        _, domain = make_domain(p, n, None)
        certificate = slack_two_second_fixed_window_kummer_saturation_data(
            p=p,
            domain_order=n,
            quotient_order=quotient_order,
            window_size=window_size,
        )
        if certificate is None:
            raise AssertionError((p, n, quotient_order, window_size))
        failures = two_fiber_divisor_power_failure_count(
            int(certificate["kernel_character_order"]),
            int(certificate["square_coset_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        principal_count = principal_open_count(p)
        degeneracy_count = degeneracy_line_union_count(p)
        coefficient_l1_bound = int(certificate["coefficient_abs_bound"]) * (
            int(certificate["denominator"]) - 1
        )
        if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        character_triple_count = (
            int(certificate["kernel_character_order"]) ** 3
        )
        square_coset_index = int(certificate["square_coset_index"])
        jacobi_l1_bound = int(certificate["coefficient_abs_bound"]) * (
            character_triple_count - 1
        )
        conic_l1_bound = int(certificate["principal_weight"]) * (
            square_coset_index - 1
        )
        kummer_l1_bound = jacobi_l1_bound * (square_coset_index - 1)
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["nonprincipal_constant"]) * kummer_l1_bound
        )
        if (
            jacobi_l1_bound + conic_l1_bound + kummer_l1_bound
            != coefficient_l1_bound
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * weighted_error_l1_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            int(certificate["principal_weight"]),
            (
                weighted_error_l1_bound
                + 6 * int(certificate["denominator"])
            ),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        certificate_positive = bool(certificate["saturation_certificate"])
        if certificate_positive != expected_certificate:
            raise AssertionError((p, n, certificate))
        if (
            bool(certificate["uniform_threshold_applies"])
            and not certificate_positive
        ):
            raise AssertionError((p, n, certificate))
        window = slack_two_second_fixed_window_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
            window_fibers=tuple(range(window_size)),
        )
        if window is None:
            raise AssertionError((p, n, quotient_order, window_size))
        window_saturates = int(window["nonzero_square_coset_count"]) == int(
            window["total_nonzero_square_coset_count"]
        )
        if certificate_positive and not window_saturates:
            raise AssertionError((p, n, certificate, window))
        fixed_window_kummer_checked.append(
            (
                p,
                n,
                quotient_order,
                window_size,
                certificate_positive,
                certificate["kernel_character_order"],
                certificate["square_coset_index"],
                certificate["denominator"],
                certificate["uniform_prime_threshold"],
                window["parameter_count"],
                window["zero_parameter_count"],
                window["nonzero_square_coset_count"],
                window["total_nonzero_square_coset_count"],
            )
        )
    r_window_union_kummer_checked = []
    for (
        p,
        n,
        quotient_order,
        remaining_fibers,
        expected_union_certificate,
        expected_fixed_certificate,
    ) in R_WINDOW_UNION_KUMMER_CASES:
        _, domain = make_domain(p, n, None)
        label_triples = quotient_window_label_triple_count(
            quotient_order,
            remaining_fibers,
        )
        direct_label_triples = direct_quotient_window_label_triple_count(
            quotient_order,
            remaining_fibers,
        )
        if label_triples != direct_label_triples:
            raise AssertionError(
                (p, n, quotient_order, label_triples, direct_label_triples)
            )
        coefficient_bound = quotient_window_label_nonprincipal_bound(
            quotient_order,
            remaining_fibers,
        )
        direct_coefficient_bound = (
            direct_quotient_window_label_nonprincipal_bound(
                quotient_order,
                remaining_fibers,
            )
        )
        if coefficient_bound != direct_coefficient_bound:
            raise AssertionError(
                (
                    p,
                    n,
                    quotient_order,
                    coefficient_bound,
                    direct_coefficient_bound,
                )
            )
        quotient_l1 = quotient_window_label_l1_data(
            quotient_order,
            remaining_fibers,
        )
        (
            direct_quotient_l1,
            direct_zero_subset_histogram,
            direct_coefficient_histogram,
        ) = (
            direct_quotient_window_label_l1_data(
                quotient_order,
                remaining_fibers,
            )
        )
        if bool(quotient_l1["exact"]):
            if int(quotient_l1["l1_bound"]) != direct_quotient_l1:
                raise AssertionError((p, n, quotient_l1, direct_quotient_l1))
            if quotient_l1.get("zero_subset_count_histogram") is not None:
                expected_histogram = tuple(
                    (count, multiplicity)
                    for count, multiplicity in quotient_l1[
                        "zero_subset_count_histogram"
                    ]
                    if multiplicity
                )
                if (
                    expected_histogram
                    != direct_zero_subset_histogram
                ):
                    raise AssertionError(
                        (p, n, quotient_l1, direct_zero_subset_histogram)
                    )
            if quotient_l1.get("coefficient_value_histogram") is not None:
                if (
                    tuple(quotient_l1["coefficient_value_histogram"])
                    != direct_coefficient_histogram
                ):
                    raise AssertionError(
                        (p, n, quotient_l1, direct_coefficient_histogram)
                    )
        elif int(quotient_l1["l1_bound"]) < direct_quotient_l1:
            raise AssertionError((p, n, quotient_l1, direct_quotient_l1))
        certificate = (
            slack_two_second_quotient_window_union_kummer_saturation_data(
                p=p,
                domain_order=n,
                quotient_order=quotient_order,
                remaining_fibers=remaining_fibers,
            )
        )
        if certificate is None:
            raise AssertionError((p, n, quotient_order, remaining_fibers))
        if label_triples != int(certificate["label_triple_count"]):
            raise AssertionError((p, n, label_triples, certificate))
        if coefficient_bound != int(certificate["coefficient_abs_bound"]):
            raise AssertionError((p, n, coefficient_bound, certificate))
        ambient_kernel_count = (p - 1) // n
        if bool(quotient_l1["exact"]):
            quotient_l1_bound = (
                ambient_kernel_count ** 3 * int(quotient_l1["l1_bound"])
            )
        else:
            quotient_l1_bound = (
                ambient_kernel_count ** 3 * label_triples
                + (
                    int(certificate["kernel_character_order"]) ** 3
                    - ambient_kernel_count ** 3
                )
                * coefficient_bound
            )
        if quotient_l1_bound != int(
            certificate["quotient_coefficient_l1_bound"]
        ):
            raise AssertionError((p, n, quotient_l1_bound, certificate))
        if bool(certificate["quotient_l1_exact"]) != bool(quotient_l1["exact"]):
            raise AssertionError((p, n, quotient_l1, certificate))
        coefficient_l1_bound = direct_ambient_window_label_l1_bound(
            int(certificate["kernel_character_order"]),
            quotient_order,
            remaining_fibers,
            int(certificate["square_coset_index"]),
        )
        if bool(certificate["quotient_l1_exact"]):
            if coefficient_l1_bound != int(certificate["coefficient_l1_bound"]):
                raise AssertionError((p, n, coefficient_l1_bound, certificate))
        elif coefficient_l1_bound > int(certificate["coefficient_l1_bound"]):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        crude_coefficient_l1_bound = (
            int(certificate["crude_coefficient_abs_bound"])
            * int(certificate["denominator"])
            - int(certificate["principal_weight"])
        )
        if crude_coefficient_l1_bound != int(
            certificate["crude_coefficient_l1_bound"]
        ):
            raise AssertionError((p, n, crude_coefficient_l1_bound, certificate))
        jacobi_l1_bound = (
            int(certificate["quotient_coefficient_l1_bound"])
            - int(certificate["principal_weight"])
        )
        conic_l1_bound = int(certificate["principal_weight"]) * (
            int(certificate["square_coset_index"]) - 1
        )
        kummer_l1_bound = jacobi_l1_bound * (
            int(certificate["square_coset_index"]) - 1
        )
        weighted_error_l1_bound = (
            jacobi_l1_bound
            + conic_l1_bound
            + int(certificate["nonprincipal_constant"]) * kummer_l1_bound
        )
        if (
            jacobi_l1_bound + conic_l1_bound + kummer_l1_bound
            != int(certificate["coefficient_l1_bound"])
        ):
            raise AssertionError((p, n, coefficient_l1_bound, certificate))
        if jacobi_l1_bound != int(certificate["jacobi_l1_bound"]):
            raise AssertionError((p, n, jacobi_l1_bound, certificate))
        if conic_l1_bound != int(certificate["conic_l1_bound"]):
            raise AssertionError((p, n, conic_l1_bound, certificate))
        if kummer_l1_bound != int(certificate["kummer_l1_bound"]):
            raise AssertionError((p, n, kummer_l1_bound, certificate))
        if int(certificate["conic_error_constant"]) != 1:
            raise AssertionError((p, n, certificate))
        if weighted_error_l1_bound != int(
            certificate["weighted_error_l1_bound"]
        ):
            raise AssertionError((p, n, weighted_error_l1_bound, certificate))
        crude_jacobi_l1_bound = int(
            certificate["crude_coefficient_abs_bound"]
        ) * (int(certificate["kernel_character_order"]) ** 3 - 1)
        crude_conic_l1_bound = int(certificate["principal_weight"]) * (
            int(certificate["square_coset_index"]) - 1
        )
        crude_kummer_l1_bound = crude_jacobi_l1_bound * (
            int(certificate["square_coset_index"]) - 1
        )
        crude_weighted_error_l1_bound = (
            crude_jacobi_l1_bound
            + crude_conic_l1_bound
            + int(certificate["nonprincipal_constant"])
            * crude_kummer_l1_bound
        )
        if crude_jacobi_l1_bound != int(certificate["crude_jacobi_l1_bound"]):
            raise AssertionError((p, n, crude_jacobi_l1_bound, certificate))
        if crude_conic_l1_bound != int(certificate["crude_conic_l1_bound"]):
            raise AssertionError((p, n, crude_conic_l1_bound, certificate))
        if crude_kummer_l1_bound != int(certificate["crude_kummer_l1_bound"]):
            raise AssertionError((p, n, crude_kummer_l1_bound, certificate))
        if crude_weighted_error_l1_bound != int(
            certificate["crude_weighted_error_l1_bound"]
        ):
            raise AssertionError(
                (p, n, crude_weighted_error_l1_bound, certificate)
            )
        failures = two_fiber_divisor_power_failure_count(
            int(certificate["kernel_character_order"]),
            int(certificate["square_coset_index"]),
        )
        if failures != int(certificate["divisor_power_failure_count"]):
            raise AssertionError((p, n, failures, certificate))
        radical_degrees = tuple(certificate["radical_component_degrees"])
        if radical_degrees != (1, 1, 1, 2):
            raise AssertionError((p, n, radical_degrees, certificate))
        radical_total = sum(radical_degrees)
        if radical_total != int(certificate["radical_total_degree"]):
            raise AssertionError((p, n, radical_total, certificate))
        principal_count = principal_open_count(p)
        degeneracy_count = degeneracy_line_union_count(p)
        lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * weighted_error_l1_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if lower_numerator != int(certificate["lower_numerator"]):
            raise AssertionError((p, n, lower_numerator, certificate))
        expected_threshold = kummer_quadratic_uniform_prime_threshold(
            int(certificate["principal_weight"]),
            weighted_error_l1_bound + 6 * int(certificate["denominator"]),
        )
        if expected_threshold != int(certificate["uniform_prime_threshold"]):
            raise AssertionError((p, n, expected_threshold, certificate))
        direct_quotient_l1_bound_numerator = (
            coefficient_l1_bound + int(certificate["principal_weight"])
        )
        if (
            direct_quotient_l1_bound_numerator
            % int(certificate["square_coset_index"])
        ):
            raise AssertionError(
                (p, n, direct_quotient_l1_bound_numerator, certificate)
            )
        direct_quotient_l1_bound = (
            direct_quotient_l1_bound_numerator
            // int(certificate["square_coset_index"])
        )
        direct_weighted_error_l1_bound = (
            direct_quotient_l1_bound
            - int(certificate["principal_weight"])
            + int(certificate["principal_weight"])
            * (int(certificate["square_coset_index"]) - 1)
            + int(certificate["nonprincipal_constant"])
            * (int(certificate["square_coset_index"]) - 1)
            * (
                direct_quotient_l1_bound
                - int(certificate["principal_weight"])
            )
        )
        direct_lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * direct_weighted_error_l1_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if direct_lower_numerator < lower_numerator:
            raise AssertionError((p, n, direct_lower_numerator, certificate))
        crude_lower_numerator = (
            int(certificate["principal_weight"]) * principal_count
            - p * crude_weighted_error_l1_bound
            - degeneracy_count * int(certificate["denominator"])
        )
        if crude_lower_numerator != int(certificate["crude_lower_numerator"]):
            raise AssertionError((p, n, crude_lower_numerator, certificate))
        if crude_lower_numerator > 0:
            raise AssertionError((p, n, crude_lower_numerator, certificate))
        union_certificate_positive = bool(certificate["saturation_certificate"])
        if union_certificate_positive != expected_union_certificate:
            raise AssertionError((p, n, certificate))
        fixed_certificate = slack_two_second_fixed_window_kummer_saturation_data(
            p=p,
            domain_order=n,
            quotient_order=quotient_order,
            window_size=remaining_fibers,
        )
        if fixed_certificate is None:
            raise AssertionError((p, n, quotient_order, remaining_fibers))
        if (
            bool(fixed_certificate["saturation_certificate"])
            != expected_fixed_certificate
        ):
            raise AssertionError((p, n, fixed_certificate))
        reduction = slack_two_second_quotient_window_reduction_data(
            p=p,
            domain=domain,
            quotient_order=quotient_order,
            remaining_fibers=remaining_fibers,
        )
        if reduction is None:
            raise AssertionError((p, n, quotient_order, remaining_fibers))
        if union_certificate_positive and not bool(
            reduction["saturates_nonzero_square_cosets"]
        ):
            raise AssertionError((p, n, certificate, reduction))
        r_window_union_kummer_checked.append(
            (
                p,
                n,
                quotient_order,
                remaining_fibers,
                label_triples,
                coefficient_bound,
                certificate["denominator"],
                certificate["coefficient_l1_bound"],
                certificate["crude_lower_numerator"],
                certificate["lower_numerator"],
                union_certificate_positive,
                bool(fixed_certificate["saturation_certificate"]),
                reduction["nonzero_square_coset_count"],
                reduction["total_nonzero_square_coset_count"],
            )
        )
    scan_label_checked = []
    for p, n, k, slack, quotient_order, expected_label in SCAN_LABEL_CASES:
        result = scan_supports(
            p=p,
            n=n,
            k=k,
            slack=slack,
            quotient_order=quotient_order,
            primitive=None,
            anchor_exp=None,
            direction_exp=None,
            max_supports=50_000,
            top_histograms=3,
        )
        label = result["canonical_slack_two_second_index_window_label"]
        if label != expected_label:
            raise AssertionError((p, n, k, quotient_order, label, result))
        if not bool(
            result["canonical_slack_two_second_r2_union_exact_support_certificate"]
        ):
            raise AssertionError((p, n, k, quotient_order, result))
        if not bool(result["canonical_slack_two_second_r2_union_reduction_check"]):
            raise AssertionError((p, n, k, quotient_order, result))
        scan_label_checked.append((p, n, k, quotient_order, label))
    print(
        "verify_m1_slack_two_depth_two_kummer_saturation: "
        f"PASS checked={checked} lift_checked={lift_checked} "
        f"lift_bound_checked={lift_bound_checked} "
        f"kernel_checked={kernel_checked} "
        f"two_fiber_checked={two_fiber_checked} "
        f"two_fiber_union_checked={two_fiber_union_checked} "
        f"r_window_checked={r_window_checked} "
        f"fixed_window_kummer_checked={fixed_window_kummer_checked} "
        f"r_window_union_kummer_checked={r_window_union_kummer_checked} "
        f"scan_label_checked={scan_label_checked}"
    )


if __name__ == "__main__":
    main()
