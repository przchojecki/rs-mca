#!/usr/bin/env python3
"""Verify the full-domain slack-two depth-two frontier certificate.

Proof status: AUDIT / EXPERIMENTAL.

The theorem note proves saturation for p>=23 by a character-sum margin. This
script checks the remaining odd primes below 23 and samples the large-prime
certificate against direct enumeration.
"""

from m1_support_occupancy_scan import (
    full_domain_slack_two_depth_two_A_class_data,
)


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def main() -> None:
    expected_failures = {5: "empty_or_zero_only", 7: "one_class_only"}
    finite_successes = {11, 13, 17, 19}
    checked = []
    for p in [prime for prime in range(5, 100) if is_prime(prime)]:
        data = full_domain_slack_two_depth_two_A_class_data(p)
        assert data is not None
        saturates = bool(data["saturates_nonzero_square_cosets"])
        if p in expected_failures:
            if saturates:
                raise AssertionError(f"unexpected saturation at p={p}")
        elif p in finite_successes:
            if not saturates or not data["finite_low_prime_certificate"]:
                raise AssertionError(f"finite certificate failed at p={p}")
        else:
            if not saturates:
                raise AssertionError(f"large-prime saturation failed at p={p}")
            if p >= 23 and not data["large_prime_certificate"]:
                raise AssertionError(f"large-prime margin failed at p={p}")
        checked.append((p, data["nonzero_slope_image"]))
    print(
        "verify_m1_slack_two_depth_two_full_domain: PASS "
        f"checked={checked}"
    )


if __name__ == "__main__":
    main()
