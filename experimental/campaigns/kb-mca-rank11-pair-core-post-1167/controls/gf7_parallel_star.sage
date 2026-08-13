#!/usr/bin/env sage
"""Small actual-record parallel-star control for the rank-11 route cut."""

F = GF(7)
D = list(F)[:6]
n, K, core_size = len(D), 1, 2
m = core_size + 1
w = m - K
core = D[:core_size]
outside = D[core_size:]
slopes = list(F)[:len(outside)]

r0 = []
r1 = []
for x in D:
    if x in core:
        r0.append(F(0))
        r1.append(F(0))
    else:
        index = outside.index(x)
        r0.append(-slopes[index])
        r1.append(F(1))

for index, gamma in enumerate(slopes):
    support = [
        coordinate
        for coordinate in range(n)
        if r0[coordinate] + gamma * r1[coordinate] == 0
    ]
    assert len(support) == m
    assert set(D[coordinate] for coordinate in support) == set(
        core + [outside[index]]
    )
    # A constant pair cannot explain both received rows on the support.
    assert len(set(r1[coordinate] for coordinate in support)) == 2

    word = [r0[coordinate] + gamma * r1[coordinate] for coordinate in range(n)]
    maximum_constant_agreement = max(word.count(value) for value in F)
    assert maximum_constant_agreement == m
    assert n - maximum_constant_agreement > w

common_pair_core = [
    coordinate
    for coordinate in range(n)
    if r0[coordinate] == 0 and r1[coordinate] == 0
]
assert common_pair_core == list(range(core_size))

# At cutoff tau=1, A=m-tau=2 and all four records select the same pair.
agreement = m - 1
assert len(slopes) == n - agreement == 4

print(
    "KB_MCA_RANK11_GF7_PARALLEL_STAR_PASS "
    "field=7 n=6 post_near=1 parallel=4 n_minus_A=4"
)
