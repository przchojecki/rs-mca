#!/usr/bin/env python3
"""Verify the first residue-zero common-core absorption payment."""

from __future__ import annotations

import copy


ROW = {
    "R": 1048576, "d": 67448, "K": 6, "e": 98232,
    "budget": 16777215, "core": 67452, "inside_core": 67447,
    "sync_start": 30791, "low_end": 30790,
    "agreement": 36664, "punctured_length": 950350,
    "johnson_denominator": 1339497146,
    "johnson_numerator": 34838880650, "list_cap": 26,
    "low_slopes": 2554032, "line_cap": 981129,
    "bound": 3535161, "slack": 13242054, "next_e": 98233,
}


class Reject(ValueError):
    pass


def endpoint(row):
    R, d, K, e = row["R"], row["d"], row["K"], row["e"]
    N, m, c = R + K, d + K, K - 1
    inside = row["core"] - c
    sync = e - inside + K
    low_end = sync - 1
    agreement = m - low_end
    n = N - e
    denominator = agreement * agreement - n * c
    numerator = n * (agreement - c)
    list_cap = numerator // denominator
    low = e * list_cap
    line = N - m + 1
    bound = low + line
    if row["core"] < m - 2 or denominator <= 0 or bound >= row["budget"]:
        raise Reject("guards")
    return {
        "inside_core": inside, "sync_start": sync, "low_end": low_end,
        "agreement": agreement, "punctured_length": n,
        "johnson_denominator": denominator,
        "johnson_numerator": numerator, "list_cap": list_cap,
        "low_slopes": low, "line_cap": line, "bound": bound,
        "slack": row["budget"] - bound, "next_e": e + 1,
    }


def validate(row):
    for key, value in endpoint(row).items():
        if row[key] != value:
            raise Reject(key)
    return 23


def main() -> None:
    checks = validate(copy.deepcopy(ROW))
    mutations = []
    for key, delta in (("inside_core", 1), ("list_cap", -1),
                       ("bound", -1), ("slack", 1)):
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
        "MCA_FULL_LIFT_RESIDUE_ZERO_CORE_ABSORPTION_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
