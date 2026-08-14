#!/usr/bin/env python3
"""Verify the exact GF(1009) affine-span MCA counterexample."""

from __future__ import annotations

import copy
from collections import Counter


class Reject(ValueError):
    pass


def construct(p: int) -> tuple[list[int], list[int], list[tuple[int, int]]]:
    base = [0] * 100
    direction = [0] * 100
    slopes = list(range(1, 31))

    for i, x in enumerate(range(20, 50), 1):
        base[x] = (-i * i) % p
        direction[x] = i

    used = set(range(31))
    candidate = 31
    for x in range(50, 71):
        while candidate in used or any(
            (1 + slope * candidate) % p == 0 for slope in slopes
        ):
            candidate += 1
        base[x] = 1
        direction[x] = candidate
        used.add(candidate)
        candidate += 1

    for x in range(71, 100):
        while candidate in used:
            candidate += 1
        direction[x] = candidate
        used.add(candidate)
        forbidden = {0, 1} | {
            (-slope * candidate) % p for slope in slopes
        }
        base[x] = next(value for value in range(2, p) if value not in forbidden)
        candidate += 1

    selected = [(slope, 0) for slope in slopes] + [(0, 1)]
    return base, direction, selected


def validate(expected: dict[str, int]) -> dict[str, int]:
    p = 1009
    base, direction, selected = construct(p)
    if any(value == 0 for value in direction[20:]):
        raise Reject("nonzero direction tail")
    if len(set(direction[20:])) != 80:
        raise Reject("distinct direction tail")

    explanations = set()
    for slope, explanation in selected:
        support = [
            x for x in range(100)
            if (base[x] + slope * direction[x] - explanation) % p == 0
        ]
        if len(support) != expected["support_size"]:
            raise Reject("maximal support")
        if (
            len({base[x] for x in support}) == 1
            and len({direction[x] for x in support}) == 1
        ):
            raise Reject("pair containment")
        explanations.add(explanation)

    direction_max = max(Counter(direction).values())
    bound = max(100 * 99 // (21 * 20), 100 * 99 // (20 * 21))
    observed = {
        "slopes": len(selected),
        "support_size": 21,
        "affine_rank": len(explanations) - 1,
        "direction_max": direction_max,
        "bound": bound,
    }
    if observed != expected:
        raise Reject("expected values")
    if not direction_max < 21 or not len(selected) > bound:
        raise Reject("theorem violation")
    return observed


def main() -> None:
    expected = {
        "slopes": 31,
        "support_size": 21,
        "affine_rank": 1,
        "direction_max": 20,
        "bound": 23,
    }
    result = validate(expected)
    mutations = 0
    for key in ("slopes", "support_size", "direction_max", "bound"):
        changed = copy.deepcopy(expected)
        changed[key] += 1
        try:
            validate(changed)
        except Reject:
            mutations += 1
    if mutations != 4:
        raise AssertionError("mutation controls")
    print(
        "MCA_AFFINE_SPAN_INCIDENCE_COUNTEREXAMPLE_V1_PASS "
        f"slopes={result['slopes']} bound={result['bound']} "
        f"direction_max={result['direction_max']} mutations={mutations}/4"
    )


if __name__ == "__main__":
    main()
