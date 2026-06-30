#!/usr/bin/env python3
"""Verify the M1 post-sift residual alternative."""

from __future__ import annotations

from verify_m1_near_star_template_localization import (
    footprint,
    near_star_footprint_cap,
    template_bound,
)
from verify_m1_packet_overlap_endpoint_sift import (
    actual_stats,
    endpoint_support_degree,
    make_random_labels,
    max_labels_per_support,
    support_floor_from_disjoint_pair_cap,
)

import random


def endpoint_support_count(labels) -> int:
    return len({label.endpoints for label in labels})


def residual_supports(labels):
    return {label.endpoints for label in labels}


def check_exact_alternative_grid() -> None:
    checked = 0
    for k in range(2, 22):
        for s in range(1, 13):
            for h in range(1, 6):
                for degree_cap in range(1, 8):
                    for lambda_cap in range(0, s + 1):
                        floor = support_floor_from_disjoint_pair_cap(
                            k, s, h, degree_cap, lambda_cap
                        )
                        for support_budget in range(1, k * s + 1):
                            condition = floor > support_budget
                            # The theorem is a contrapositive of the support
                            # floor. If the condition fails, no closure is
                            # claimed; if it holds, B<=R and the cap cannot
                            # coexist.
                            if condition and floor <= support_budget:
                                raise AssertionError(
                                    (
                                        k,
                                        s,
                                        h,
                                        degree_cap,
                                        lambda_cap,
                                        floor,
                                        support_budget,
                                    )
                                )
                            checked += 1
    print(f"exact_alternative_parameter_grid_checked={checked}")


def check_sampled_packet_systems() -> None:
    rng = random.Random(20260630)
    checked = 0
    triggered = 0
    for trial in range(600):
        labels = make_random_labels(rng, trial)
        k = len(labels)
        if k < 2:
            continue
        s = len(labels[0].packet)
        h = max_labels_per_support(labels)
        degree_cap = endpoint_support_degree(labels)
        stats = actual_stats(labels)
        support_size = stats["support_size"]
        max_disjoint_overlap = stats["max_disjoint_overlap"]
        m = endpoint_support_count(labels)

        for far_factor in range(2, 6):
            supports = residual_supports(labels)
            cap = near_star_footprint_cap(
                max(3, len(footprint(supports))), degree_cap, far_factor
            )
            if m < far_factor * degree_cap:
                if len(footprint(supports)) > cap:
                    raise AssertionError((trial, far_factor, m, degree_cap, cap))

            for lambda_cap in range(0, s + 1):
                floor = support_floor_from_disjoint_pair_cap(
                    k, s, h, degree_cap, lambda_cap
                )
                for support_budget in (support_size, max(1, support_size - 1)):
                    if floor <= support_budget:
                        continue
                    large_support = support_size > support_budget
                    near_star = m < far_factor * degree_cap
                    high_disjoint = max_disjoint_overlap > lambda_cap
                    if not (large_support or near_star or high_disjoint):
                        raise AssertionError(
                            (
                                trial,
                                k,
                                s,
                                h,
                                degree_cap,
                                far_factor,
                                lambda_cap,
                                floor,
                                support_budget,
                                support_size,
                                m,
                                max_disjoint_overlap,
                                stats,
                            )
                        )
                    triggered += 1
        checked += 1
    print(f"sampled_packet_systems_checked={checked}")
    print(f"sampled_alternatives_triggered={triggered}")


def check_near_star_template_interface() -> None:
    rng = random.Random(20260701)
    checked = 0
    for trial in range(300):
        labels = make_random_labels(rng, trial + 1000)
        if not labels:
            continue
        degree_cap = endpoint_support_degree(labels)
        h = max_labels_per_support(labels)
        m = endpoint_support_count(labels)
        supports = residual_supports(labels)
        q = max(3, len(footprint(supports)))
        for far_factor in range(2, 7):
            if m >= far_factor * degree_cap:
                continue
            cap = near_star_footprint_cap(q, degree_cap, far_factor)
            actual_footprint = len(footprint(supports))
            if actual_footprint > cap:
                raise AssertionError(
                    (trial, q, degree_cap, far_factor, m, actual_footprint, cap)
                )
            templates = template_bound(q, degree_cap, far_factor, h)
            if templates <= 0:
                raise AssertionError((trial, q, degree_cap, far_factor, h))
            checked += 1
    print(f"near_star_template_interfaces_checked={checked}")


def main() -> None:
    check_exact_alternative_grid()
    check_sampled_packet_systems()
    check_near_star_template_interface()
    print("m1 post-sift residual alternative checks passed")


if __name__ == "__main__":
    main()
