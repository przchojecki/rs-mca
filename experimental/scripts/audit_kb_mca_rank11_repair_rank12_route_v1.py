#!/usr/bin/env python3
"""Independent exact audit for the rank-11 repair / rank-12 route packet."""

from __future__ import annotations

import json
from fractions import Fraction
from math import prod
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULT = ROOT / "experimental/data/certificates/kb-mca-rank11-repair-rank12-route-v1/result.json"

R = 1_048_576
D = 67_472
BUDGET = 274_980_728_111_395_087
NEAR = 134_944


def down(x: int, r: int) -> int:
    value = 1
    for i in range(r):
        value *= x - i
    return value


def up(x: int, r: int) -> int:
    value = 1
    for i in range(r):
        value *= x + i
    return value


def ceilq(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def c_resource(s: int, k: int) -> int:
    values = [
        Fraction(down(R + k, s + 1), (D + k) * up(D + 1, s - 1)),
        Fraction(down(R + s, s + 1), up(D + 1, s)),
    ]
    value = max(values)
    return value.numerator // value.denominator


def raw_low_requirement(s: int, k: int, child: int, threshold: int) -> int:
    high = c_resource(s, k) // (threshold + 1)
    return high + ((child - 1) * (R + k)) // (D + k - threshold) + 1


def line_cap(j: int) -> int:
    """Independent exact maximization using the concave deficiency quadratic.

    For fixed dominant-line count t, write r for the number of effective
    deficiencies equal to q and A=n-t(m-1).  Before the final floor, the
    variable term

        (A+r(q-1)) * (t-r+r/q)

    is a concave quadratic in r.  Its integer maximum occurs at the
    feasibility boundary, an endpoint, or next to the real vertex.
    """

    n = R + j
    m = D + j
    q = m // 2
    low = n * (n - 1) // (2 * q * (m - q))
    high = 0
    for t in range(1, n // (q + 1) + 1):
        A = n - t * (m - 1)
        if A >= 0:
            r_min = 0
        else:
            r_min = (-A + (q - 2)) // (q - 1)
        if r_min > t:
            continue
        vertex_num = q * t - A
        vertex_den = 2 * (q - 1)
        r0 = vertex_num // vertex_den
        candidates = {r_min, t}
        for r in range(r0 - 2, r0 + 4):
            if r_min <= r <= t:
                candidates.add(r)
        for r in candidates:
            outside = A + r * (q - 1)
            numerator = outside * ((t - r) * q + r)
            value = t * (t - 1) + numerator // q
            high = max(high, value)
    return low + high


def main() -> None:
    result = json.loads(RESULT.read_text())

    maximum = -1
    argmax = 0
    for j in range(1, R + 1):
        value = line_cap(j)
        if value > maximum:
            maximum, argmax = value, j
    assert (maximum, argmax) == (4_070_947, 1)
    assert result["uniform_rank_one"]["maximum"] == maximum

    thresholds = {2: 515, 3: 511, 4: 507, 5: 503, 6: 499,
                  7: 496, 8: 492, 9: 489, 10: 485}
    expected = {1: 4_070_948}
    for s in range(2, 11):
        threshold = thresholds[s]
        expected[s] = max(
            raw_low_requirement(s, k, expected[s - 1], threshold)
            for k in range(s, R + 1)
        )
    assert expected == {
        1: 4_070_948,
        2: 64_241_811,
        3: 1_013_639_041,
        4: 15_991_635_730,
        5: 252_259_306_484,
        6: 3_978_753_104_997,
        7: 62_747_001_947_996,
        8: 989_431_810_807_346,
        9: 15_600_062_750_954_861,
        10: 248_706_399_341_288_370,
    }
    unsafe = BUDGET - NEAR + 1
    assert unsafe - expected[10] == 26_274_328_769_971_774
    assert result["rank11_payment"]["loads"] == {
        str(k): value for k, value in expected.items()
    }

    wall = min(
        (raw_low_requirement(11, R, expected[10], threshold), threshold)
        for threshold in range(1, D + 1)
    )
    assert wall == (546_519_697_764_383_119, D)
    assert wall[0] - unsafe == 271_538_969_653_122_975
    assert result["rank12_method_wall"]["required_parent_load"] == wall[0]
    assert result["claims"]["complete_affine_error_rank_11_branch_paid"] is True
    assert result["claims"]["affine_error_rank_12_paid"] is False

    print("KB_MCA_RANK11_REPAIR_RANK12_ROUTE_AUDIT_PASS")
    print(f"uniform_rank_one={maximum}")
    print(f"rank11_required={expected[10]}")
    print(f"rank11_slack={unsafe - expected[10]}")
    print(f"rank12_method_shortfall={wall[0] - unsafe}")


if __name__ == "__main__":
    main()
