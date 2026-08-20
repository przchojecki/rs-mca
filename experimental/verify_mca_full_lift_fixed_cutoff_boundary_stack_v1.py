#!/usr/bin/env python3
"""Verify endpoints of the M31 fixed-cutoff boundary-stack payment."""

from __future__ import annotations

import copy


R, D, K, BUDGET, CUTOFF = 1048576, 67448, 6, 16777215, 65200
N, M, C = R + K, D + K, K - 1
EXPECTED = {
    98232: (1381829, 391210, 1773039, 15004177, "direct"),
    101149: (1422377, 14327810, 15750187, 1027029, "direct"),
    101150: (1422391, 14530797, 15953188, 824028,
             "absorption", 67453, 28, 3813329),
    101155: (1422461, 15244572, 16667033, 110183,
             "absorption", 67446, 28, 3813469),
    101156: (1422475, 15528748, 16951223, -174007,
             "fixed_cutoff_wall"),
}


class Reject(ValueError):
    pass


def cap(e: int, h: int) -> int:
    n, agreement = N - e, M - h
    johnson = agreement * agreement - n * C
    if johnson > 0:
        return n * (agreement - C) // johnson
    gap = -johnson
    balance = 2 * agreement * agreement - n * C
    tangent = (n - agreement) ** 2 - (n - 1) * gap
    if balance < 0 or tangent <= 0:
        raise Reject("undefined prefix cap")
    return ((n - 1) * n * n * (agreement - C)
            // (agreement * tangent))


def prefix(e: int) -> int:
    values = [0] + [cap(e, h) for h in range(1, CUTOFF + 1)]
    for h in range(CUTOFF - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    return sum((values[h] - values[h - 1]) * (e // h)
               for h in range(1, CUTOFF + 1))


def record(e: int):
    s, _ = divmod(e - K, 3)
    H = e - s - 1
    p = prefix(e)
    stack = 0
    for h in range(CUTOFF + 1, H + 1):
        A, n, outside = 2 * h - e, N - e, M - h
        denominator = A * A - e * C
        if (2 * h <= e or denominator <= 0 or not (n > outside > C)):
            raise Reject("boundary guard")
        classes = e * (A - C) // denominator
        line = (n - C) // (outside - C)
        stack += 1 + classes * (line - 1)
    forcing = p + stack
    threshold = BUDGET - forcing + 1
    if forcing + (N - M + 1) <= BUDGET:
        return (p, stack, forcing, threshold, "direct")
    if threshold < 2:
        return (p, stack, forcing, threshold, "fixed_cutoff_wall")
    core = (threshold * M - N + threshold - 2) // (threshold - 1)
    inside = core - C
    sync = e - inside + K
    agreement = M - sync + 1
    n = N - e
    denominator = agreement * agreement - n * C
    if denominator <= 0:
        raise Reject("low Johnson")
    low = n * (agreement - C) // denominator
    bound = e * low + (N - M + 1)
    return (p, stack, forcing, threshold, "absorption", core, low, bound)


def validate(expected):
    for e, row in expected.items():
        if record(e) != row:
            raise Reject(f"endpoint {e}")
    if 101155 - 98232 + 1 != 2924:
        raise Reject("census")
    if EXPECTED[101156][2] - BUDGET != 174008:
        raise Reject("adjacent excess")
    if EXPECTED[101155][-1] >= BUDGET:
        raise Reject("endpoint budget")
    return 41


def main() -> None:
    checks = validate(copy.deepcopy(EXPECTED))
    mutations = []
    for e, index, delta in ((98232, 0, 1), (101150, 6, -1),
                            (101155, 7, -1), (101156, 2, -1)):
        changed = copy.deepcopy(EXPECTED)
        row = list(changed[e])
        row[index] += delta
        changed[e] = tuple(row)
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_FULL_LIFT_FIXED_CUTOFF_BOUNDARY_STACK_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
