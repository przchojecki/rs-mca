#!/usr/bin/env python3
"""Verify the M31 fixed-cutoff residue-two anchor repair."""

from __future__ import annotations

import copy

ROW = {
    "R": 1048576, "d": 67448, "K": 6, "budget": 16777215,
    "e": 101156, "cutoff": 65258, "s": 33716, "q": 2,
    "H": 67439, "prefix": 1440609, "boundary": 15454671,
    "forcing": 16895280, "D1": 284224, "D2": 258385,
    "lower": 16352671, "line": 981129, "threshold": 424545,
    "core": 67452, "inside": 67447, "sync": 33715,
    "agreement": 33740, "low": 28, "absorption": 3813497,
    "outside": 94742, "disjoint": 3,
    "cases": (3813497, 16705799, 16611058, 16705798, 16611059),
    "bound": 16705799, "slack": 71416,
    "next_e": 101157, "next_q": 0,
}

class Reject(ValueError):
    pass


def cap(R: int, d: int, K: int, e: int, h: int) -> int:
    n, m, c = R + K - e, d + K, K - 1
    agreement = m - h
    johnson = agreement * agreement - n * c
    if johnson > 0:
        return n * (agreement - c) // johnson
    gap = -johnson
    balance = 2 * agreement * agreement - n * c
    tangent = (n - agreement) ** 2 - (n - 1) * gap
    if balance < 0 or tangent <= 0:
        raise Reject("undefined prefix cap")
    return ((n - 1) * n * n * (agreement - c)
            // (agreement * tangent))


def prefix(R: int, d: int, K: int, e: int, cutoff: int) -> int:
    values = [0] + [cap(R, d, K, e, h) for h in range(1, cutoff + 1)]
    for h in range(cutoff - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    return sum((values[h] - values[h - 1]) * (e // h)
               for h in range(1, cutoff + 1))


def layer_charge(R: int, d: int, K: int, e: int, h: int) -> int:
    N, m, c = R + K, d + K, K - 1
    A = 2 * h - e
    denominator = A * A - e * c
    outside = m - h
    n = N - e
    if 2 * h <= e or denominator <= 0 or not (n > outside > c):
        raise Reject("boundary guard")
    classes = e * (A - c) // denominator
    line = (n - c) // (outside - c)
    return 1 + classes * (line - 1)


def endpoint(row):
    R, d, K, e = row["R"], row["d"], row["K"], row["e"]
    N, m, c = R + K, d + K, K - 1
    s, q = divmod(e - K, 3)
    H = e - s - 1
    p = prefix(R, d, K, e, row["cutoff"])
    layers = [layer_charge(R, d, K, e, h)
              for h in range(row["cutoff"] + 1, H + 1)]
    boundary = sum(layers)
    forcing = p + boundary
    d1, d2 = layers[-1], layers[-2]
    lower = forcing - d1 - d2
    line = N - m + 1
    threshold = row["budget"] - lower + 1
    core = (threshold * m - N + threshold - 2) // (threshold - 1)
    inside = core - c
    sync = e - inside + K
    agreement = m - sync + 1
    n = N - e
    denominator = agreement * agreement - n * c
    if denominator <= 0:
        raise Reject("low Johnson")
    low = n * (agreement - c) // denominator
    absorption = e * low + line
    outside = (n - c) // (m - H - c)
    disjoint = e // (s + 1)
    cases = (
        absorption,
        forcing - d1 + outside + 1,
        forcing - d1 + 2,
        forcing - d1 + outside,
        forcing - d1 + disjoint,
    )
    return {
        "s": s, "q": q, "H": H, "prefix": p,
        "boundary": boundary, "forcing": forcing,
        "D1": d1, "D2": d2, "lower": lower, "line": line,
        "threshold": threshold, "core": core, "inside": inside,
        "sync": sync, "agreement": agreement, "low": low,
        "absorption": absorption, "outside": outside,
        "disjoint": disjoint, "cases": cases, "bound": max(cases),
    }, len(layers)


def validate(row):
    got, layers = endpoint(row)
    for key, value in got.items():
        if row[key] != value:
            raise Reject(key)
    if (row["q"] != 2 or
            row["e"] - 2 * row["s"] - (row["s"] + 2) != row["K"] or
            row["budget"] - row["bound"] != row["slack"] or
            row["slack"] <= 0 or
            (row["next_e"] - row["K"]) % 3 != row["next_q"] or
            row["next_q"] != 0):
        raise Reject("guards")
    return 37 + layers


def main() -> None:
    checks = validate(copy.deepcopy(ROW))
    mutations = []
    for key, delta in (("prefix", 1), ("D1", 1),
                       ("absorption", -1), ("bound", -1),
                       ("slack", 1)):
        changed = copy.deepcopy(ROW)
        changed[key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_FULL_LIFT_FIXED_CUTOFF_Q2_ANCHOR_REPAIR_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
