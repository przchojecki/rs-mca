#!/usr/bin/env python3
"""Independently reconstruct and audit the affine-span MCA counterexample."""

from __future__ import annotations


class Reject(ValueError):
    pass


def main() -> None:
    p = 1009
    base: list[int | None] = [None] * 100
    direction: list[int | None] = [None] * 100

    for x in range(20):
        base[x], direction[x] = 0, 0
    for slope in range(1, 31):
        x = 19 + slope
        base[x], direction[x] = (-slope * slope) % p, slope

    forbidden_direction = {
        (-pow(slope, -1, p)) % p for slope in range(1, 31)
    }
    available = iter(
        value for value in range(31, p) if value not in forbidden_direction
    )
    used = set(range(31))
    for x in range(50, 71):
        value = next(value for value in available if value not in used)
        base[x], direction[x] = 1, value
        used.add(value)

    candidate = max(used) + 1
    for x in range(71, 100):
        while candidate in used:
            candidate += 1
        direction[x] = candidate
        used.add(candidate)
        forbidden_base = {0, 1} | {
            (-slope * candidate) % p for slope in range(1, 31)
        }
        base[x] = next(
            value for value in range(2, p) if value not in forbidden_base
        )
        candidate += 1

    if any(value is None for value in base + direction):
        raise Reject("incomplete construction")
    r0 = [int(value) for value in base]
    r1 = [int(value) for value in direction]
    selected = [(slope, 0) for slope in range(1, 31)] + [(0, 1)]

    for slope, explanation in selected:
        support = tuple(
            x
            for x in range(100)
            if (r0[x] + slope * r1[x]) % p == explanation
        )
        if len(support) != 21:
            raise Reject("selected support size")
        if len({r0[x] for x in support}) == 1 and len(
            {r1[x] for x in support}
        ) == 1:
            raise Reject("same-support pair containment")

    direction_max = max(
        sum(value == constant for value in r1) for constant in range(p)
    )
    affine_bound = (100 * 99) // (21 * 20)
    if (len(selected), direction_max, affine_bound) != (31, 20, 23):
        raise Reject("claimed invariants")

    print(
        "MCA_AFFINE_SPAN_INCIDENCE_COUNTEREXAMPLE_V1_INDEPENDENT_PASS "
        "slopes=31 support_checks=31 field_values=1009 "
        "bound=23"
    )


if __name__ == "__main__":
    main()
