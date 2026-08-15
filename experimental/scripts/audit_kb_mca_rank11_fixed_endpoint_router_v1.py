#!/usr/bin/env python3
"""Independent arithmetic and finite-field audit of the fixed-endpoint router."""

from __future__ import annotations

from math import gcd


N = 2_097_152
K = 1_048_576
M = 1_116_048
W = 67_472
S = 10
NEAR = 134_944
BUDGET = 274_980_728_111_395_087
RESOURCE = 106_618_568_137_036_225_644


def choose(n: int, r: int) -> int:
    """Independent multiplicative binomial implementation with gcd cancellation."""
    if r < 0 or r > n:
        return 0
    r = min(r, n - r)
    numerator = list(range(n - r + 1, n + 1))
    denominator = list(range(1, r + 1))
    for j, den in enumerate(denominator):
        value = den
        for i, num in enumerate(numerator):
            factor = gcd(num, value)
            if factor > 1:
                numerator[i] //= factor
                value //= factor
            if value == 1:
                break
        if value != 1:
            raise AssertionError(f"uncancelled denominator {j}: {value}")
    result = 1
    for value in numerator:
        result *= value
    return result


def exact_floor_max(tau: int) -> tuple[int, int, int]:
    d = W - tau
    denominator = choose(d + S, S)
    # Recurrence for C(x+s,s); no calls to math.comb.
    current = choose(d + S, S)
    best_value = -1
    best_x = -1
    best_cap = -1
    for x in range(d, K + 1):
        if x > d:
            current = current * (x + S) // x
        cap = current // denominator
        value = (K - x) * cap
        if value > best_value:
            best_value, best_x, best_cap = value, x, cap
    return best_value, best_x, best_cap


def envelope(tau: int) -> tuple[int, int, int]:
    x = 953_250
    low = (K - x) * choose(x + S, S) // choose(W - tau + S, S) + 1
    high = RESOURCE // (tau + 1)
    return low, high, NEAR + low + high


def projective_check(p: int = 7) -> tuple[int, int, int]:
    gl2 = 0
    outside = 0
    maximum = 0
    for a in range(p):
        for b in range(p):
            for c in range(p):
                for d in range(p):
                    det = (a * d - b * c) % p
                    if det == 0:
                        continue
                    gl2 += 1
                    z = pow(det, -1, p)
                    q00, q01 = d * z % p, -b * z % p
                    q10, q11 = -c * z % p, a * z % p
                    assert sum((q01 + gamma * q11) % p == 0 for gamma in range(p)) <= 1
                    for v0 in range(1, p):
                        for v1 in range(p):
                            outside += 1
                            roots = sum(
                                (
                                    ((q00 + gamma * q10) * v0)
                                    + ((q01 + gamma * q11) * v1)
                                )
                                % p
                                == 0
                                for gamma in range(p)
                            )
                            maximum = max(maximum, roots)
                            assert roots <= 1
    return gl2, outside, maximum


def main() -> None:
    # Derive the continuous maximizer from the exact successive-ratio sign.
    threshold_num = S * K - S - 1
    xstar = threshold_num // (S + 1) + 1
    assert xstar == 953_250

    # Independently scan all cutoffs using the theorem envelope.
    first = None
    minimum = None
    for tau in range(1, W):
        low, high, total = envelope(tau)
        row = (total, tau, low, high, BUDGET - total)
        if first is None and total <= BUDGET:
            first = row
        if minimum is None or row < minimum:
            minimum = row

    assert first == (
        274_530_191_074_227_933,
        439,
        32_215_263_489_919_749,
        242_314_927_584_173_240,
        450_537_037_167_154,
    )
    assert minimum == (
        81_826_485_385_525_648,
        3608,
        52_284_072_490_672_992,
        29_542_412_894_717_712,
        193_154_242_725_869_439,
    )

    exact439 = exact_floor_max(439)
    exact3608 = exact_floor_max(3608)
    assert exact439 == (32_215_263_489_916_276, 953_250, 337_948_340_326)
    assert exact3608 == (52_284_072_490_618_276, 953_250, 548_476_517_326)

    shared = 2 * (M - 439) - N
    assert shared == 134_066
    assert projective_check() == (2016, 84672, 1)

    print(
        "KB_MCA_RANK11_FIXED_ENDPOINT_INDEPENDENT_PASS "
        f"first_tau={first[1]} best_tau={minimum[1]} "
        f"exact439={exact439[0]} common_factor={shared}"
    )


if __name__ == "__main__":
    main()
