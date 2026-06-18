#!/usr/bin/env python3
"""Audit the slack-two depth-two Kummer-Weil saturation certificate."""

from __future__ import annotations

from typing import Sequence, Tuple

from m1_support_occupancy_scan import slack_two_second_kummer_saturation_data
from mca_slope_scan import make_domain


CASES = (
    # Index-two proper subgroups where the certificate is positive.
    (383, 191, True),
    (769, 384, True),
    # A high-index sample from the non-field-filling side of the existing PR.
    (193, 6, False),
)


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


def main() -> None:
    checked = []
    for p, n, expected_certificate in CASES:
        _, domain = make_domain(p, n, None)
        certificate = slack_two_second_kummer_saturation_data(p, n)
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
                nonzero_coset_count,
                total_coset_count,
            )
        )
    print(
        "verify_m1_slack_two_depth_two_kummer_saturation: "
        f"PASS checked={checked}"
    )


if __name__ == "__main__":
    main()
