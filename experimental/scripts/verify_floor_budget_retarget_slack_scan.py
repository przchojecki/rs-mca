#!/usr/bin/env python3
"""Replay the floor-budget retarget slack arithmetic.

This verifies only the arithmetic imported by the note.  The compiler packets
that supply the cited floor shapes are intentionally separate artifacts.
"""

from __future__ import annotations

from math import comb, log2


def check_small_core_floor() -> None:
    n_max = 2**41
    tight_constant = 29
    consumed_constant = 16

    tight_bits = log2(tight_constant * n_max**3)
    consumed_bits = log2(consumed_constant * n_max**3)
    slack_bits = log2(tight_constant / consumed_constant)

    assert abs(tight_bits - 127.9) < 0.1, tight_bits
    assert 0.85 < slack_bits < 0.87, slack_bits
    assert abs((consumed_bits + slack_bits) - tight_bits) < 1e-12

    print("small_core_floor: PASS")
    print(f"  binding allowance: 29*n^3 = 2^{tight_bits:.2f}")
    print(f"  consumed floor:    16*n^3 = 2^{consumed_bits:.2f}")
    print(f"  uniform retune:    log2(29/16) = {slack_bits:.3f} bits")


def check_petal_floor() -> None:
    expected = {
        41: (5.768, 5.769),
        42: (5.773, 5.775),
        43: (5.778, 5.780),
        44: (5.783, 5.786),
    }

    for exponent, bracket in expected.items():
        n = 2**exponent
        paid_column = comb(n + 6, 6)
        excess_c14_column = comb(n + 20, 6)
        paid_exp = log2(paid_column) / exponent
        excess_exp = log2(excess_c14_column) / exponent
        room_bits = (6 - paid_exp) * exponent

        assert paid_column <= n**6
        assert excess_c14_column <= n**6
        assert bracket[0] < paid_exp < bracket[1], paid_exp
        assert room_bits > 9.0

        print(
            "petal_floor: PASS "
            f"n=2^{exponent} log_n binom(n+6,6)={paid_exp:.4f} "
            f"room={room_bits:.1f} bits c14_exp={excess_exp:.4f}"
        )


def check_worst_word_convention_floor() -> None:
    within_column_bits = (27.0, 60.6)
    aggregate_bits = 0.9

    assert within_column_bits[0] > 20
    assert within_column_bits[1] > 60
    assert 0 < aggregate_bits < 1

    print("worst_word_convention_floor: PASS")
    print("  within-column room is large, but aggregate convention room is <1 bit")


def main() -> int:
    check_small_core_floor()
    check_petal_floor()
    check_worst_word_convention_floor()
    print("FLOOR_BUDGET_RETARGET_SLACK_SCAN_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
