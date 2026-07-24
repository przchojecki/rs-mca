#!/usr/bin/env sage
"""Sage replay for the M31 fixed-mismatch recurrence packet."""

from collections import deque
import heapq
import hashlib
import json


p = Integer(2)^31 - 1
K = Integer(2)^20
w = Integer(67447)
RADIUS = Integer(981129)
g = Integer(354972)
d = Integer(287525)
target = Integer(15775932)


def digest(values):
    raw = (
        json.dumps([int(value) for value in values],
                   sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def direct_cap(rank, dimension):
    inner = (
        binomial(K + rank - 1, rank - 1)
        // binomial(w + rank - 1, rank - 1)
    )
    result = (K + dimension) * inner // (w + dimension)
    denominator = (
        (w + dimension)^2
        - (K + dimension) * (dimension - 1)
    )
    if denominator > 0:
        result = min(
            result,
            (K + dimension) * (w + 1) // denominator,
        )
    return Integer(result)


def recurrence_arrays():
    arrays = {}
    base = [Integer(0)] * (d + 1)
    for dimension in range(1, d + 1):
        base[dimension] = (K + dimension) // (w + dimension)
    arrays[1] = base

    for rank in range(2, 7):
        child = arrays[rank - 1]
        current = list(child)
        prefix_max = Integer(-1)
        window = deque()
        for dimension in range(rank, d + 1):
            added = dimension - 1
            prefix_max = max(prefix_max, child[added])
            while window and child[window[-1]] <= child[added]:
                window.pop()
            window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            recurrence = (
                (dimension - 1) * prefix_max
                + (K + 1) * child[window[0]]
            ) // (w + dimension)
            current[dimension] = max(
                child[dimension],
                min(recurrence, direct_cap(rank, dimension)),
            )
        arrays[rank] = current
    return arrays


def class_array(rank_six, reduction=0):
    output = [Integer(0)] * (d - 6 + 1)
    for size in range(1, len(output)):
        dimension = d - size
        output[size] = rank_six[dimension]
        if dimension == 4981:
            output[size] -= reduction
    return output


def prefix(values):
    maxima = [Integer(0)] * len(values)
    args = [0] * len(values)
    best = Integer(0)
    arg = 0
    for index in range(1, len(values)):
        if values[index] > best:
            best = values[index]
            arg = index
        maxima[index] = best
        args[index] = arg
    return maxima, args


def coarse(cutoff, classes):
    maxima, unused_args = prefix(classes)
    denominator = g - cutoff
    best = Integer(-1)
    survivors = 0
    for size in range(1, len(classes)):
        rest = d - 1 - size
        upper = min(size, rest - 4)
        tail = min(size, rest // 5)
        if upper < 1 or tail < 1:
            continue
        value = (
            size * classes[size]
            + rest * maxima[upper]
            + (RADIUS - (d - 1)) * maxima[tail]
        )
        if value // denominator > target:
            survivors += 1
        best = max(best, value)
    return (
        best,
        best // denominator,
        best % denominator,
        survivors,
    )


def exact_tail(tail_mass, maximum_part, classes):
    baseline = classes[maximum_part]
    losses = [Integer(0)] * maximum_part
    for part in range(1, maximum_part):
        losses[part] = part * (baseline - classes[part])
    infinity = Integer(10)^100
    distance = [infinity] * maximum_part
    mass = [infinity] * maximum_part
    previous = [None] * maximum_part
    distance[0] = 0
    mass[0] = 0
    queue = [(Integer(0), Integer(0), 0)]
    while queue:
        cost, used, residue = heapq.heappop(queue)
        if (cost, used) != (distance[residue], mass[residue]):
            continue
        for part in range(1, maximum_part):
            new_residue = (residue + part) % maximum_part
            candidate = (cost + losses[part], used + part)
            if candidate < (
                distance[new_residue],
                mass[new_residue],
            ):
                distance[new_residue], mass[new_residue] = candidate
                previous[new_residue] = (residue, part)
                heapq.heappush(
                    queue,
                    (candidate[0], candidate[1], new_residue),
                )
    residue = tail_mass % maximum_part
    parts = []
    cursor = residue
    while cursor:
        cursor, part = previous[cursor]
        parts.append(part)
    fillers = (tail_mass - mass[residue]) // maximum_part
    objective = tail_mass * baseline - distance[residue]
    return objective, distance[residue], fillers, sorted(parts)


def refined(cutoff, rank_six, reduction=0):
    classes = class_array(rank_six, reduction)
    maxima, unused_args = prefix(classes)
    largest = 282544
    budget = d - 1 - largest
    envelopes = []
    for sixth in range(1, budget // 5 + 1):
        high = budget - 4 * sixth
        value = (
            (RADIUS - largest) * maxima[sixth]
            + budget * (maxima[high] - maxima[sixth])
        )
        envelopes.append((value, sixth))
    envelopes.sort(reverse=True)
    assert envelopes[0] == (500828161030, 996)
    assert envelopes[1][0] == 500826095155

    tail_mass = RADIUS - largest - budget
    tail = exact_tail(tail_mass, 996, classes)
    assert tail == (497257822254, 87136, 696, [389])
    nonlargest = budget * classes[996] + tail[0]
    assert nonlargest == 500828073894
    assert nonlargest > envelopes[1][0]
    numerator = largest * classes[largest] + nonlargest
    denominator = g - cutoff
    return (
        numerator,
        numerator // denominator,
        numerator % denominator,
        target - numerator // denominator,
        coarse(cutoff, classes)[3],
    )


# Exact finite-field controls for the load-bearing full-hyperplane algebra.
F = GF(31)
V = VectorSpace(F, 7)
lam = V([1, 0, 0, 0, 0, 0, 0])
kernel_basis = [V.gen(i) for i in range(1, 7)]
assert all(lam.dot_product(vector) == 0 for vector in kernel_basis)
annihilator = Matrix(F, kernel_basis).right_kernel()
assert annihilator.dimension() == 1
assert annihilator.gen(0) in V.subspace([lam])
beta = F(7)
t_alpha = F(11)
assert beta != 0 and t_alpha != 0 and t_alpha * beta != 0
u_x = F(13)
L_x = F(9)
assert u_x / L_x != 0

assert p - K - 2 * d + 1 == 2145860022
arrays = recurrence_arrays()
rank_six = arrays[6]
assert [rank_six[index] for index in range(4981, 4987)] == [
    9806438,
    9806312,
    9806186,
    9806060,
    9805934,
    9805807,
]
assert arrays[5][4980] == 674155
assert rank_six[d - 996] == 716918
assert rank_six[d - 389] == 716694
assert digest(rank_six) == (
    "3cafd8d5d4a9d00b6bd90c13050476bab4bfac9ccb43125ba90a2844dbab70b6"
)

classes = class_array(rank_six)
assert coarse(147593, classes) == (
    3271586860242,
    15775883,
    19585,
    0,
)
assert refined(147594, rank_six) == (
    3271578292166,
    15775917,
    176540,
    15,
    1,
)
assert refined(147595, rank_six) == (
    3271578292166,
    15775993,
    191805,
    -61,
    1,
)
assert refined(147595, rank_six, 44)[:4] == (
    3271565860230,
    15775933,
    202489,
    -1,
)
assert refined(147595, rank_six, 45)[:4] == (
    3271565577686,
    15775932,
    127322,
    0,
)

print("M31 rank7 fixed-mismatch Sage replay: PASS")
