#!/usr/bin/env sage
"""Independent Sage replay for the M31 rank-seven one-pivot packet."""

import hashlib
import json
from collections import Counter
from math import comb


R_VALUE = 981129
W_VALUE = 67447
L_VALUE = 15775933
TARGET_VALUE = L_VALUE - 1
S_MAX_VALUE = 366886
G_MIN_VALUE = 72428
G_MAX_VALUE = 354972


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
        default=int,
    ).encode("ascii")


def digest(value):
    return hashlib.sha256(canonical(value) + b"\n").hexdigest()


def bounds(g):
    return max(g - R_VALUE, -S_MAX_VALUE), min(W_VALUE, g - W_VALUE - 1)


def h_cap(g, q):
    lo, hi = bounds(g)
    assert lo <= q <= hi
    d = g - W_VALUE
    m = g - q
    v = W_VALUE - q
    inner = comb(R_VALUE - d + 6, 6) // comb(v + 6, 6)
    return R_VALUE * inner // m


def q_star(g):
    lo, hi = bounds(g)
    assert h_cap(g, lo) <= TARGET_VALUE
    while lo < hi:
        middle = (lo + hi + 1) // 2
        if h_cap(g, middle) <= TARGET_VALUE:
            lo = middle
        else:
            hi = middle - 1
    return lo


# Independent all-g scan.
intervals = []
start = G_MIN_VALUE
value = q_star(start)
zero_tail = 0
maximum_tail = (-1, -1, -1)
for g in range(G_MIN_VALUE, G_MAX_VALUE + 1):
    q = q_star(g)
    if q != value:
        intervals.append({"start": start, "end": g - 1, "cutoff": value})
        start = g
        value = q
    cap = h_cap(g, q)
    tail = TARGET_VALUE - cap
    if tail == 0:
        zero_tail += 1
    if tail > maximum_tail[0]:
        maximum_tail = (tail, g, q)
intervals.append({"start": start, "end": G_MAX_VALUE, "cutoff": value})

length_histogram = Counter(
    interval["end"] - interval["start"] + 1 for interval in intervals
)
assert len(intervals) == 38569
assert digest(intervals) == (
    "4e2e2d6ddf919ace174a1cdd3f8df78520d0608a90c87fa231a5075cb8d13b52"
)
assert dict(sorted(length_histogram.items())) == {
    2: 1,
    4: 608,
    5: 6225,
    6: 7068,
    7: 6716,
    8: 6640,
    9: 6750,
    10: 4475,
    11: 86,
}
assert zero_tail == 204
assert maximum_tail == (1852, 354397, 15129)


# Independent endpoint histogram.
endpoint_q = q_star(G_MAX_VALUE)
endpoint_caps = [h_cap(G_MAX_VALUE, q) for q in range(endpoint_q + 1)]
histogram = [endpoint_caps[0]]
histogram.extend(
    endpoint_caps[index] - endpoint_caps[index - 1]
    for index in range(1, len(endpoint_caps))
)
histogram.append(L_VALUE - endpoint_caps[-1])
first_moment = sum(index * count for index, count in enumerate(histogram))
second_moment = sum(
    index * index * count for index, count in enumerate(histogram)
)
assert endpoint_q == 15186
assert h_cap(G_MAX_VALUE, 0) == 3268160
assert h_cap(G_MAX_VALUE, 15185) == 15772893
assert h_cap(G_MAX_VALUE, 15186) == 15774749
assert h_cap(G_MAX_VALUE, 15187) == 15776606
assert histogram[-1] == 1184
assert digest(histogram) == (
    "7189e2ededaac854d54ee469451cf6e2f8afe5817c39d47ac65c355d1d04f4a0"
)
assert first_moment == 122692619370
assert second_moment == 1411089367885678


# Fixed-G transition.
assert h_cap(217542, 0) == 15775952
assert h_cap(217543, 0) == 15775767
assert h_cap(217542, 0) > TARGET_VALUE
assert h_cap(217543, 0) <= TARGET_VALUE


# Exact module profiles and balanced support layouts.
def module_profile(e, c=2048):
    kappa, remainder = divmod(e, c)
    assert remainder * (kappa + 1) + (c - remainder) * kappa == e
    return [kappa, remainder]


assert module_profile(287525) == [140, 805]
assert module_profile(352508) == [172, 252]
assert module_profile(339785) == [165, 1865]
assert divmod(1116023, 65536) == (17, 1911)
assert divmod(981129, 65536) == (14, 63625)
assert divmod(352508, 65536) == (5, 24828)
assert divmod(1116023, 1024) == (1089, 887)
assert divmod(981129, 1024) == (958, 137)
assert divmod(352508, 1024) == (344, 252)


# Tiny exact control for the fixed-H divisibility-fiber dichotomy.
F = GF(31)
SAGE_R.<X> = PolynomialRing(F)
d_toy = 5
Y_toy = X^8 + 7*X^6 + 3*X^2 + 1

H_moderate = (X - 1)*(X - 2)*(X - 3)*(X - 4)*(X - 5)
moderate_remainder = Y_toy.mod(H_moderate)
assert moderate_remainder.degree() < d_toy
moderate = [
    f for f in [moderate_remainder]
    if (Y_toy - f).mod(H_moderate) == 0 and f.degree() < d_toy
]
assert len(moderate) == 1

H_deep = (X - 1)*(X - 2)*(X - 3)
deep_remainder = Y_toy.mod(H_deep)
deep = [
    deep_remainder + H_deep*(a + b*X)
    for a in F
    for b in F
]
assert len(set(deep)) == 31^2
assert all(f.degree() < d_toy for f in deep)
assert all((Y_toy - f).mod(H_deep) == 0 for f in deep)
deep_vectors = [
    vector(F, [f[index] for index in range(d_toy)])
    for f in deep
]
base = deep_vectors[0]
deep_rank = matrix(F, [row - base for row in deep_vectors]).rank()
assert deep_rank == d_toy - H_deep.degree() == 2


record = {
    "schema": "m31-rank7-effective-deficit-one-pivot-sage-replay-v1",
    "scope": "INDEPENDENT_EXACT_ARITHMETIC_AND_FIXED_H_TOY_CONTROL",
    "frontier_interval_count": len(intervals),
    "frontier_interval_sha256": digest(intervals),
    "frontier_cutoff_range": [intervals[0]["cutoff"], intervals[-1]["cutoff"]],
    "zero_tail_cells": zero_tail,
    "maximum_tail_upper": list(maximum_tail),
    "endpoint_cutoff": endpoint_q,
    "endpoint_H_0": h_cap(G_MAX_VALUE, 0),
    "endpoint_H_cutoff": h_cap(G_MAX_VALUE, endpoint_q),
    "endpoint_H_next": h_cap(G_MAX_VALUE, endpoint_q + 1),
    "endpoint_tail": histogram[-1],
    "endpoint_histogram_sha256": digest(histogram),
    "endpoint_first_moment": first_moment,
    "endpoint_second_moment": second_moment,
    "fixed_g_transition": [217543, h_cap(217543, 0)],
    "module_profiles": {
        "d": module_profile(287525),
        "old_tail_H": module_profile(352508),
        "new_tail_H": module_profile(339785),
    },
    "fixed_H_toy": {
        "field": 31,
        "message_dimension": d_toy,
        "moderate_fiber_size": len(moderate),
        "deep_fiber_size": len(deep),
        "deep_affine_rank": deep_rank,
    },
}
record["payload_sha256"] = hashlib.sha256(canonical(record)).hexdigest()
print(canonical(record).decode("ascii"))
