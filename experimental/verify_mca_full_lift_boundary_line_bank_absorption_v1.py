#!/usr/bin/env python3
"""Verify endpoints of the M31 boundary-line-bank payment."""

from __future__ import annotations

import copy


ROW = {
    "R": 1048576, "d": 67448, "K": 6, "budget": 16777215,
    "cutoff": 65272, "paid_count": 23649,
    "first": {
        "e": 101157, "q": 0, "H": 67439, "prefix": 1502226,
        "layers": 2167, "groups": 6502, "base": 1497892,
        "direct": 6380798650, "threshold": 2350, "core": 67037,
        "inside": 67032, "sync": 34131, "agreement": 33324,
        "low": 28, "bound": 3813525, "slack": 12963690,
    },
    "last": {
        "e": 124805, "q": 2, "H": 83205, "prefix": 1636955,
        "layers": 2182, "groups": 34560, "base": 1604577,
        "direct": 33909422817, "threshold": 440, "core": 65220,
        "inside": 65215, "sync": 59596, "agreement": 7859,
        "low": 126, "bound": 16706559, "slack": 70656,
    },
    "adjacent": {
        "e": 124806, "q": 0, "H": 83205, "prefix": 1636968,
        "layers": 2182, "groups": 34564, "base": 1604586,
        "direct": 33913347342, "threshold": 439, "core": 65214,
        "inside": 65209, "sync": 59603, "agreement": 7852,
        "low": 127, "bound": 16831491, "slack": -54276,
    },
}


class Reject(ValueError):
    pass


def raw_cap(R: int, d: int, K: int, e: int, h: int) -> int:
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
    values = [0] + [
        raw_cap(R, d, K, e, h) for h in range(1, cutoff + 1)]
    for h in range(cutoff - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    return sum((values[h] - values[h - 1]) * (e // h)
               for h in range(1, cutoff + 1))


def endpoint(row, expected):
    R, d, K, e = row["R"], row["d"], row["K"], expected["e"]
    N, m, c = R + K, d + K, K - 1
    s, q = divmod(e - K, 3)
    H = e - s - 1
    upper = min(H, m)
    p = prefix(R, d, K, e, row["cutoff"])
    class_sum = 0
    layers = 0
    for h in range(row["cutoff"] + 1, upper + 1):
        A = 2 * h - e
        denominator = A * A - e * c
        if 2 * h <= e or A <= c or denominator <= 0:
            raise Reject("line-bank guard")
        classes = e * (A - c) // denominator
        if classes < 1:
            raise Reject("class count")
        class_sum += classes
        layers += 1
    groups = int(H < m) + class_sum
    base = p + layers - class_sum
    direct = base + groups * (N - m + 1)
    required = row["budget"] - base + 1
    threshold = (required + groups - 1) // groups
    if required <= 0 or threshold < 2:
        raise Reject("pigeonhole")
    core = (threshold * m - N + threshold - 2) // (threshold - 1)
    inside = core - c
    sync = e - inside + K
    agreement = m - sync + 1
    n = N - e
    denominator = agreement * agreement - n * c
    if denominator <= 0:
        raise Reject("low Johnson")
    low = n * (agreement - c) // denominator
    bound = e * low + (N - m + 1)
    return {
        "e": e, "q": q, "H": H, "prefix": p, "layers": layers,
        "groups": groups, "base": base, "direct": direct,
        "threshold": threshold, "core": core, "inside": inside,
        "sync": sync, "agreement": agreement, "low": low,
        "bound": bound, "slack": row["budget"] - bound,
    }, layers


def validate(row):
    checks = 47
    for name in ("first", "last", "adjacent"):
        got, layers = endpoint(row, row[name])
        if got != row[name]:
            raise Reject(name)
        checks += layers
    if (row["paid_count"] != row["last"]["e"] - row["first"]["e"] + 1 or
            row["adjacent"]["e"] != row["last"]["e"] + 1 or
            row["last"]["bound"] > row["budget"] or
            row["adjacent"]["bound"] <= row["budget"]):
        raise Reject("summary")
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROW))
    mutations = []
    for section, key, delta in (
            ("last", "prefix", 1), ("last", "groups", 1),
            ("last", "bound", -1), ("adjacent", "bound", -1),
            (None, "paid_count", 1)):
        changed = copy.deepcopy(ROW)
        target = changed if section is None else changed[section]
        target[key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_FULL_LIFT_BOUNDARY_LINE_BANK_ABSORPTION_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
