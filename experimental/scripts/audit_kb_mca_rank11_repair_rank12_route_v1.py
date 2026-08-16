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
FIBER = 981_105


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


def transfer(s: int, k: int, load: int) -> int:
    return ceilq(Fraction(load * (D + k) - c_resource(s, k), R + k))


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


def q_core(k: int, threshold: int) -> int:
    n = R + k
    h = D + k - threshold
    lam = k - 1
    den = h * h - lam * n
    assert den > 0
    return max((n + 2 * h - 1) // (2 * h) - 1, n * (h - lam) // den)


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

    loads = {10: BUDGET - NEAR + 1}
    for s in range(10, 1, -1):
        loads[s - 1] = transfer(s, s, loads[s])
    assert loads[1] == 5_201_865
    assert result["rank11_payment"]["forced_rank_one_load"] == loads[1]

    loads12 = {11: BUDGET - NEAR + 1}
    for s in range(11, 2, -1):
        k = 4280 + s - 3
        threshold = 249 if s >= 4 else 380
        cap = c_resource(s, k) // (threshold + 1) + q_core(k, threshold) * FIBER
        assert cap < loads12[s]
        loads12[s - 1] = transfer(s, k + 1, loads12[s])
    assert loads12[2] == 8_681_730

    high = c_resource(2, 2) // 1923
    low = loads12[2] - high
    assert (high, low, q_core(2, 1922)) == (131_690, 8_550_040, 15)
    c1 = FIBER
    c2 = 490_553
    assert 2 * c1 + 13 * c2 < low <= 3 * c1 + 12 * c2
    assert 3 * c1 + 12 * c2 - low == 279_911
    assert transfer(2, 2, loads12[2]) == 558_412

    endpoint = result["rank12_route"]["rank_two_endpoint"]
    assert endpoint["capacity_excess"] == 279_911
    assert result["claims"]["complete_affine_error_rank_11_branch_paid"] is True
    assert result["claims"]["affine_error_rank_12_paid"] is False

    print("KB_MCA_RANK11_REPAIR_RANK12_ROUTE_AUDIT_PASS")
    print(f"uniform_rank_one={maximum}")
    print(f"rank11_final={loads[1]}")
    print(f"rank12_rank2={loads12[2]}")
    print(f"rank2_capacity_excess={endpoint['capacity_excess']}")


if __name__ == "__main__":
    main()
