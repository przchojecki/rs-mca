#!/usr/bin/env python3
"""Audit the punctured-Johnson sparse-direction MCA profile."""

from __future__ import annotations

import copy
from fractions import Fraction


ROWS = {
    "KoalaBear": {
        "R": 1048576,
        "d": 67472,
        "K": 14,
        "budget": 274980728111395087,
        "last": 63908,
        "defect": 984668,
        "dlast": 1218,
        "dnext": -5924,
        "half": 31954,
        "jhalf": 27,
        "jlast": 2882094,
        "coarse": 4607583,
    },
    "Mersenne-31": {
        "R": 1048576,
        "d": 67448,
        "K": 6,
        "budget": 16777215,
        "last": 65236,
        "defect": 983340,
        "dlast": 2794,
        "dnext": -1636,
        "half": 32618,
        "jhalf": 28,
        "jlast": 778863,
        "coarse": 2605443,
    },
}


class Reject(ValueError):
    pass


def denominator(R: int, d: int, K: int, e: int, h: int | None = None) -> int:
    if h is None:
        h = e
    return (d + K - h) ** 2 - (R + K - e) * (K - 1)


def cap(R: int, d: int, K: int, e: int, h: int) -> int:
    if h == 0:
        return 0
    den = denominator(R, d, K, e, h)
    if den <= 0:
        raise Reject("nonpositive denominator")
    return (R + K - e) * (d - h + 1) // den


def coarse(R: int, d: int, K: int, e: int) -> int:
    return (e - 1) * cap(R, d, K, e, e // 2) + cap(R, d, K, e, e)


def derive(row: dict[str, int]) -> dict[str, int]:
    R, d, K, budget = (row[key] for key in ("R", "d", "K", "budget"))
    last = 0
    best = (-1, -1)
    previous = None
    checks = 0
    for e in range(1, d):
        den = denominator(R, d, K, e)
        if den <= 0:
            break
        if previous is not None and den >= previous:
            raise Reject("denominator not descending")
        previous = den
        value = coarse(R, d, K, e)
        if value > budget:
            raise Reject("budget failure inside Johnson prefix")
        if value > best[1]:
            best = (e, value)
        last = e
        checks += 1
    half = last // 2
    return {
        "last": last,
        "defect": R - last,
        "dlast": denominator(R, d, K, last),
        "dnext": denominator(R, d, K, last + 1),
        "half": half,
        "jhalf": cap(R, d, K, last, half),
        "jlast": cap(R, d, K, last, last),
        "coarse": best[1],
        "maximizer": best[0],
        "checks": checks,
    }


def independent_cap(R: int, d: int, K: int, e: int, h: int) -> int:
    if h == 0:
        return 0
    length = R + K - e
    agreement = d + K - h
    den = agreement * agreement - length * (K - 1)
    if den <= 0:
        raise Reject("independent denominator")
    value = Fraction(length * (agreement - K + 1), den)
    return value.numerator // value.denominator


def profile_controls() -> int:
    checks = 0
    for R, d, K in ((101, 20, 3), (211, 31, 5)):
        for e in range(1, min(d, 18)):
            if denominator(R, d, K, e) <= 0:
                continue
            previous = 0
            profile = 0
            for h in range(1, e + 1):
                current = independent_cap(R, d, K, e, h)
                if current < previous:
                    raise Reject("cumulative cap")
                profile += (current - previous) * (e // h)
                previous = current
            upper = (
                (e - 1) * independent_cap(R, d, K, e, e // 2)
                + independent_cap(R, d, K, e, e)
            )
            if profile > upper:
                raise Reject("coarse profile")
            checks += 1
    return checks


def validate(rows: dict[str, dict[str, int]]) -> int:
    checks = 0
    for name, expected in ROWS.items():
        row = rows[name]
        derived = derive(row)
        for key in (
            "last", "defect", "dlast", "dnext", "half", "jhalf",
            "jlast", "coarse",
        ):
            if derived[key] != expected[key] or row[key] != expected[key]:
                raise Reject(f"{name}: {key}")
            checks += 1
        if derived["maximizer"] != expected["last"]:
            raise Reject(f"{name}: maximizer")
        checks += derived["checks"]
    return checks


def main() -> None:
    checks = validate(copy.deepcopy(ROWS)) + profile_controls()
    mutations = []
    for name, key in (("KoalaBear", "last"), ("Mersenne-31", "coarse")):
        changed = copy.deepcopy(ROWS)
        changed[name][key] += 1
        try:
            validate(changed)
        except Reject:
            mutations.append(True)
        else:
            mutations.append(False)
    if not all(mutations):
        raise AssertionError("mutation controls")
    print(
        "MCA_SPARSE_DIRECTION_PUNCTURED_JOHNSON_PROFILE_V1_PASS "
        f"checks={checks} mutations={sum(mutations)}/{len(mutations)}"
    )


if __name__ == "__main__":
    main()
