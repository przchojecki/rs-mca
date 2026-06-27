#!/usr/bin/env python3
"""Verify the local length-16 imbalance lemma used by the L1 dyadic note."""

from itertools import product

P = 17
OMEGA = 3


def mod(x: int) -> int:
    return x % P


def eval_delta(delta: tuple[int, ...], odd_power: int) -> int:
    total = 0
    for q, coeff in enumerate(delta):
        total += coeff * pow(OMEGA, odd_power * q, P)
    return mod(total)


def shift_mod_u8_plus_1(delta: tuple[int, ...], shift: int) -> tuple[int, ...]:
    out = [0] * 8
    for q, coeff in enumerate(delta):
        target = q + shift
        if target < 8:
            out[target] += coeff
        else:
            out[target - 8] -= coeff
    return tuple(out)


def canonical(delta: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(mod(x) for x in delta)


def weight(delta: tuple[int, ...]) -> int:
    return sum(1 for x in delta if x != 0)


def main() -> None:
    delta0 = (0, 0, 1, -1, -1, 1, 1, 1)

    values_delta0 = (
        eval_delta(delta0, 1),
        eval_delta(delta0, 3),
        eval_delta(delta0, 5),
    )
    assert values_delta0 == (0, 0, 15)

    expected = {canonical((0,) * 8)}
    for shift in range(8):
        shifted = shift_mod_u8_plus_1(delta0, shift)
        expected.add(canonical(shifted))
        expected.add(canonical(tuple(-x for x in shifted)))

    solutions_13 = []
    solutions_135 = []
    for delta in product((-1, 0, 1), repeat=8):
        if eval_delta(delta, 1) == 0 and eval_delta(delta, 3) == 0:
            solutions_13.append(delta)
            if eval_delta(delta, 5) == 0:
                solutions_135.append(delta)

    assert len(solutions_13) == 17
    assert {weight(delta) for delta in solutions_13} == {0, 6}
    assert {canonical(delta) for delta in solutions_13} == expected
    assert solutions_135 == [(0,) * 8]

    print("local16 imbalance check passed")
    print("solutions for Delta(3)=Delta(3^3)=0:", len(solutions_13))
    print("weights:", sorted({weight(delta) for delta in solutions_13}))
    print("Delta0 values at 3, 3^3, 3^5:", values_delta0)
    print("solutions also vanishing at 3^5:", len(solutions_135))


if __name__ == "__main__":
    main()
