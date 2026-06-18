#!/usr/bin/env python3
"""Audit the slack-two depth-two Kummer-Weil saturation certificate."""

from __future__ import annotations

import math
from typing import Sequence, Tuple

from m1_support_occupancy_scan import (
    all_residual_packets_lift_active,
    quotient_limited_pair_parameter_bound,
    slack_two_second_kummer_saturation_data,
    slack_two_second_superboundary_shape_ledger,
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
    print(
        "verify_m1_slack_two_depth_two_kummer_saturation: "
        f"PASS checked={checked} lift_checked={lift_checked} "
        f"lift_bound_checked={lift_bound_checked} "
        f"kernel_checked={kernel_checked}"
    )


if __name__ == "__main__":
    main()
