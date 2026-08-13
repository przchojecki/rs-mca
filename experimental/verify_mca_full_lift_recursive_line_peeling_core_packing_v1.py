#!/usr/bin/env python3
"""Verify selected exact records for recursive M31 line peeling."""

from __future__ import annotations

import copy


R, D, K = 1048576, 67448, 6
N, M, C = R + K, D + K, K - 1
BUDGET, LINE = 16777215, N - M + 1

EXPECTED = {
    "first": {
        "e": 124806, "cutoff": 65304, "certificate": "profile",
        "lines": 1, "upper": 59633, "piece": 1622861,
        "bound": 2603990, "slack": 14173225, "inside_sum": 65178,
        "packing": 65178, "thresholds": [433],
    },
    "first_packing": {
        "e": 128340, "cutoff": 65304, "certificate": "packing",
        "lines": 2, "upper": 65523, "piece": 0, "bound": 0,
        "slack": 0, "inside_sum": 129396, "packing": 129391,
        "thresholds": [213, 1122],
    },
    "last": {
        "e": 130198, "cutoff": 65504, "certificate": "packing",
        "lines": 5, "upper": 67454, "piece": 0, "bound": 0,
        "slack": 0, "inside_sum": 133210, "packing": 133160,
        "thresholds": [34, 30, 26, 22, 19],
    },
    "adjacent": {
        "e": 130199, "cutoff": 65504, "certificate": "wall",
        "lines": 9, "upper": 67454, "piece": 8154082,
        "bound": 7947054, "slack": 0, "inside_sum": 126232,
        "packing": 126052, "thresholds": [33, 29, 25, 22, 18, 14, 11, 7, 3],
    },
    "paid_count": 5393,
}


class Reject(ValueError):
    pass


def raw_cap(e: int, h: int) -> int:
    shortened, agreement = N - e, M - h
    if agreement <= C:
        raise Reject("prefix agreement")
    johnson = agreement * agreement - shortened * C
    if johnson > 0:
        return shortened * (agreement - C) // johnson
    gap = -johnson
    balance = 2 * agreement * agreement - shortened * C
    tangent = (shortened - agreement) ** 2 - (shortened - 1) * gap
    if balance < 0 or tangent <= 0:
        raise Reject("undefined prefix")
    return ((shortened - 1) * shortened * shortened * (agreement - C)
            // (agreement * tangent))


def prefix(e: int, cutoff: int) -> int:
    if not 1 <= cutoff <= M:
        raise Reject("prefix cutoff")
    values = [0] + [raw_cap(e, h) for h in range(1, cutoff + 1)]
    for h in range(cutoff - 1, 0, -1):
        values[h] = min(values[h], values[h + 1])
    return sum((values[h] - values[h - 1]) * (e // h)
               for h in range(1, cutoff + 1))


def choose_cutoff(e: int) -> int:
    initial = 65304
    cutoff = initial
    while cutoff < M:
        h = cutoff + 1
        agreement = 2 * h - e
        if (2 * h > e and agreement > C and
                agreement * agreement > e * C):
            break
        cutoff += 1
    if cutoff > initial and cutoff < M:
        cutoff += 2
    if cutoff >= M:
        raise Reject("no bank")
    return cutoff


def record(e: int) -> dict[str, object]:
    H = e - (e - K) // 3 - 1
    if H < M:
        raise Reject("scope")
    cutoff = choose_cutoff(e)
    bank_prefix = prefix(e, cutoff)
    upper = M
    steps: list[dict[str, int]] = []
    inside_sum = 0

    while len(steps) < 32:
        target = BUDGET - len(steps) * LINE
        if target < 0:
            raise Reject("budget")
        try:
            whole_prefix = prefix(e, upper)
        except Reject:
            whole_prefix = None
        if whole_prefix is not None and whole_prefix <= target:
            bound = len(steps) * LINE + whole_prefix
            return {
                "e": e, "cutoff": cutoff, "certificate": "profile",
                "lines": len(steps), "upper": upper, "piece": whole_prefix,
                "bound": bound, "slack": BUDGET - bound,
                "inside_sum": inside_sum,
                "packing": inside_sum - len(steps) * (len(steps) - 1) * C // 2,
                "thresholds": [step["threshold"] for step in steps],
            }
        groups = 0
        for h in range(cutoff + 1, upper + 1):
            agreement = 2 * h - e
            denominator = agreement * agreement - e * C
            if 2 * h <= e or agreement <= C or denominator <= 0:
                raise Reject("bank guard")
            groups += e * (agreement - C) // denominator
        base = bank_prefix + upper - cutoff - groups
        required = target - base + 1
        if required <= 0:
            return {
                "e": e, "cutoff": cutoff, "certificate": "wall",
                "lines": len(steps), "upper": upper, "piece": base,
                "bound": target, "slack": 0, "inside_sum": inside_sum,
                "packing": inside_sum - len(steps) * (len(steps) - 1) * C // 2,
                "thresholds": [step["threshold"] for step in steps],
            }
        threshold = (required + groups - 1) // groups
        if not 2 <= threshold <= LINE:
            raise Reject("threshold")
        numerator = threshold * M - N
        core = 0 if numerator <= 0 else (
            numerator + threshold - 2) // (threshold - 1)
        inside = max(core - C, 0)
        sync = e - inside + K
        inside_sum += inside
        line_number = len(steps) + 1
        packing = inside_sum - line_number * (line_number - 1) * C // 2
        steps.append({"threshold": threshold, "inside": inside,
                      "sync": sync, "packing": packing})
        if packing > e:
            return {
                "e": e, "cutoff": cutoff, "certificate": "packing",
                "lines": len(steps), "upper": upper, "piece": 0,
                "bound": 0, "slack": 0, "inside_sum": inside_sum,
                "packing": packing,
                "thresholds": [step["threshold"] for step in steps],
            }
        upper = min(upper, sync - 1)
    raise Reject("recursion")


def validate(expected: dict[str, object]) -> int:
    checks = 43
    for name in ("first", "first_packing", "last", "adjacent"):
        got = record(expected[name]["e"])
        if got != expected[name]:
            raise Reject(name)
        checks += 10 + len(got["thresholds"])
    if (expected["paid_count"] !=
            expected["last"]["e"] - expected["first"]["e"] + 1 or
            expected["adjacent"]["e"] != expected["last"]["e"] + 1):
        raise Reject("summary")
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(EXPECTED))
    mutations = []
    for name, key, delta in (
            ("first", "bound", 1),
            ("first_packing", "packing", -1),
            ("last", "inside_sum", 1),
            ("adjacent", "piece", -1)):
        changed = copy.deepcopy(EXPECTED)
        changed[name][key] += delta
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    changed = copy.deepcopy(EXPECTED)
    changed["paid_count"] += 1
    try:
        validate(changed)
    except Reject:
        mutations.append(True)
    else:
        mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_FULL_LIFT_RECURSIVE_LINE_PEELING_CORE_PACKING_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
