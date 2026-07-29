#!/usr/bin/env python3
"""Independent exact replays of the M31 quotient-rotation spectrum."""

from collections import Counter
from math import comb


EXPECTED = Counter(
    {
        8_287_155: 16,
        8_286_755: 8,
        8_286_751: 5,
        8_286_750: 3,
    }
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def subset_product_dp() -> list[int]:
    """Count 17-subsets of the nonidentity elements of C_32 by product."""
    dp = [[0] * 32 for _ in range(18)]
    dp[0][0] = 1
    for exponent in range(1, 32):
        for size in range(min(17, exponent), 0, -1):
            for residue in range(32):
                dp[size][(residue + exponent) % 32] += dp[size - 1][residue]
    return dp[17]


def ramanujan_power_two(order: int, residue: int) -> int:
    if residue % order == 0:
        return order // 2
    if residue % (order // 2) == 0:
        return -(order // 2)
    return 0


def ramanujan_spectrum() -> list[int]:
    total = comb(31, 17)
    spectrum = []
    for residue in range(32):
        correction = (
            -6435 * ramanujan_power_two(2, residue)
            - 35 * ramanujan_power_two(4, residue)
            - 3 * ramanujan_power_two(8, residue)
            + ramanujan_power_two(16, residue)
            - ramanujan_power_two(32, residue)
        )
        require((total + correction) % 32 == 0, "nonintegral Fourier class")
        spectrum.append((total + correction) // 32)
    return spectrum


def main() -> None:
    direct = subset_product_dp()
    fourier = ramanujan_spectrum()
    require(direct == fourier, "DP and Fourier spectra disagree")
    require(Counter(direct) == EXPECTED, "unexpected spectrum")
    require(sum(direct) == comb(31, 17) == 265_182_525, "wrong total")
    require(max(direct) == 8_287_155, "wrong maximum")
    require((comb(31, 17) + 31) // 32 == 8_286_954, "wrong average floor")
    require(16_777_215 - max(direct) == 8_490_060, "wrong row headroom")
    require(16_777_215 - 2 * max(direct) == 202_905, "wrong two-copy gap")
    require(2**20 + 2**16 + 1911 == 1_116_023, "wrong agreement")
    print("M31_QUOTIENT_ROTATION_PRODUCT_SPECTRUM_PASS max=8287155")


if __name__ == "__main__":
    main()
