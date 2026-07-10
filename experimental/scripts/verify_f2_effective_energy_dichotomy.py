#!/usr/bin/env python3
"""Replay checks for the F2 effective energy dichotomy note.

This script does not prove the external BSG or quasicube theorems. It checks
the integer arithmetic of the composition lemma's finite-row table and
exhaustively tests the Boolean difference-growth corollary on small cubes.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import log2


def diff_code(a: tuple[int, ...], b: tuple[int, ...]) -> int:
    """Encode a-b in {-1,0,1}^d as a base-3 integer."""

    code = 0
    place = 1
    for x, y in zip(a, b):
        code += (x - y + 1) * place
        place *= 3
    return code


def check_quasicube_difference(max_d: int = 4) -> None:
    for d in range(1, max_d + 1):
        points = list(product((0, 1), repeat=d))
        universe_size = len(points)
        diff_table = [
            [diff_code(points[i], points[j]) for j in range(universe_size)]
            for i in range(universe_size)
        ]

        min_margin: int | None = None
        checked = 0
        for mask in range(1, 1 << universe_size):
            indices = [i for i in range(universe_size) if mask & (1 << i)]
            diff_bits = 0
            for i in indices:
                row = diff_table[i]
                for j in indices:
                    diff_bits |= 1 << row[j]
            diff_size = diff_bits.bit_count()
            size = len(indices)
            margin = diff_size * diff_size - size * size * size
            assert margin >= 0, (d, mask, size, diff_size, margin)
            min_margin = margin if min_margin is None else min(min_margin, margin)
            checked += 1

        print(f"quasicube-corollary d={d}: subsets={checked} min_margin={min_margin}")


@dataclass(frozen=True)
class BSGRow:
    label: str
    c1_bits: float
    c2_bits: float
    e1: int
    e2: int
    expected_deficit_bits: float

    @property
    def exponent(self) -> int:
        return self.e1 + 2 * self.e2

    def deficit_bits(self, budget_bits: float) -> float:
        return (budget_bits - self.c1_bits - 2 * self.c2_bits) / self.exponent


def check_constant_table() -> None:
    rows = [
        BSGRow("idealized-Schoen", 0.0, 0.0, 1, 4, 123.0 / 9.0),
        BSGRow("conservative-Schoen", 10.0, 10.0, 1, 4, 93.0 / 9.0),
        BSGRow("classical-safe", 10.0, 10.0, 2, 5, 93.0 / 12.0),
    ]

    budget_bits = 123.0
    for row in rows:
        observed = row.deficit_bits(budget_bits)
        assert abs(observed - row.expected_deficit_bits) < 1e-12, (row, observed)
        pieces_bits = observed / 2.0
        print(
            f"{row.label}: exponent={row.exponent} "
            f"energy_deficit_bits={observed:.12g} few_piece_bits={pieces_bits:.12g}"
        )

    weakest = rows[-1].deficit_bits(budget_bits)
    assert weakest == 7.75
    assert weakest / 2.0 == 3.875
    assert 3.8 < weakest / 2.0

    subcube_deficit = budget_bits * log2(4.0 / 3.0)
    assert subcube_deficit > 50.0
    print(f"subcube-size-2^123 energy_deficit_bits={subcube_deficit:.12g}")


def main() -> None:
    check_quasicube_difference(max_d=4)
    check_constant_table()
    print("F2_EFFECTIVE_ENERGY_DICHOTOMY_PASS")


if __name__ == "__main__":
    main()
