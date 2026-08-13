#!/usr/bin/env sage
"""Independent Sage replay of the affine-span counterexample and repair."""

F = GF(257)
n, K, m, w = 256, 1, 86, 85
points = [(F(gamma), F(0)) for gamma in range(m)] + [(F(m), F(1))]

hyperplanes = [(F(0), F(0), "common") for _ in range(w)]
connector_b = set()
for gamma in range(m):
    b = F(1) / F(m - gamma)
    a = -F(gamma) * b
    connector_b.add(b)
    hyperplanes.append((a, b, "connector"))

available_b = [F(value) for value in range(1, 257)
               if F(value) not in connector_b]
for index, b in enumerate(available_b[:w]):
    forbidden = {lam - gamma * b for gamma, lam in points}
    a = next(F(value) for value in range(257) if F(value) not in forbidden)
    hyperplanes.append((a, b, "unused-%s" % index))

assert len(hyperplanes) == n
r0 = vector(F, [a for a, _, _ in hyperplanes])
r1 = vector(F, [b for _, b, _ in hyperplanes])
one = vector(F, [1] * n)

supports = []
errors = []
normal_ranks = []
near_distances = []
for gamma, lam in points:
    support = [index for index, (a, b, _) in enumerate(hyperplanes)
               if a + gamma * b == lam]
    assert len(support) == m
    # K=1: simultaneous containment would make r0 and r1 constant on S.
    assert (len({r0[index] for index in support}) > 1 or
            len({r1[index] for index in support}) > 1)
    normal_ranks.append(matrix(F, [[r1[index], -1]
                                   for index in support]).rank())
    supports.append(set(support))
    errors.append(r0 + gamma * r1 - lam * one)
    word = r0 + gamma * r1
    best_constant = max(list(word).count(value) for value in F)
    near_distances.append(n - best_constant)

assert len(points) == 87
assert set(normal_ranks) == {2}
assert len(set.intersection(*supports)) == 0
assert max(list(r1).count(value) for value in F) == w < m
assert min(near_distances) == 170 > w
assert matrix(F, [errors[index] - errors[0]
                  for index in range(1, len(errors))]).rank() == 2

# The explicit gauge is reversible and drops the explanation rank 2 -> 1.
gauge = -one
gauged_r1 = r1 - gauge
gauged_h = [(lam + gamma) * one for gamma, lam in points]
assert [r0 + gamma * gauged_r1 - h
        for (gamma, _), h in zip(points, gauged_h)] == errors
assert matrix(F, [gauged_h[index] - gauged_h[0]
                  for index in range(1, len(gauged_h))]).rank() == 1
assert [h + gamma * gauge for (gamma, _), h in zip(points, gauged_h)] == [
    lam * one for _, lam in points
]

def falling(value, length):
    return prod(value - index for index in range(length))

def rising(value, length):
    return prod(value + index for index in range(length))

def repaired_cap(n_value, k_value, m_value, rank, theta=1):
    w_value = m_value - k_value
    first = falling(n_value, rank + 1) / (
        m_value * theta * rising(w_value + 1, rank - 1)
    )
    second = falling(n_value - k_value + rank, rank + 1) / (
        theta * rising(w_value + 1, rank)
    )
    return floor(max(first, second))

old_first = falling(n, 2) // (m * w)
old_second = falling(n, 2) // (w * (w + 1))
assert old_first == old_second == 8 < len(points)
assert repaired_cap(n, K, m, 1) == 759 >= len(points)

kb_n, kb_k, kb_m = 2097152, 1048576, 1116048
kb_w = kb_m - kb_k
kb_budget = 274980728111395087
kb_caps = [repaired_cap(kb_n, kb_k, kb_m, rank)
           for rank in range(1, 10)]
assert kb_caps == [
    16295594, 253241283, 3935435218, 118319201475,
    3677348367069, 114289853114503, 3552007973114420,
    110390969172173096, 3430729820133944932,
]
assert kb_caps[7] + 2 * kb_w == 110390969172308040
assert kb_budget - (kb_caps[7] + 2 * kb_w) == 164589758939087047
assert [repaired_cap(kb_n, kb_k, kb_m, rank, theta)
        for rank, theta in [(9, 13), (10, 388), (11, 12050)]] == [
    263902293856457302, 274790124064526354, 274970108028773601,
]

# Complete shortened row (R+s,s,d+s): automatic theta=1 pays through s=9.
R, d = 1048576, 67472
short_caps = [repaired_cap(R + rank, rank, d + rank, rank)
              for rank in range(1, 11)]
assert short_caps[8] == 55413538236037195 < kb_budget
assert short_caps[9] == 861057176799343503 > kb_budget

print(
    "KB_MCA_SUPPORT_LOCAL_THETA_SAGE_PASS "
    "slopes=%s false_cap=%s repaired_cap=759 normal_rank=2 "
    "direction_max=85 min_near_distance=170 kb_wall=8/9 "
    "shortened_wall=9/10" % (len(points), old_first)
)
