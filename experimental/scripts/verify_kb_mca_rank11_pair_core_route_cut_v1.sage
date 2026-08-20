#!/usr/bin/env sage
"""Independent Sage sharpness replay for the rank-11 pair/core route cut."""

# This is the finite parallel-star control.  It proves that a fixed selected
# pair may own floor((n-m+delta)/delta) distinct slopes already at delta=1;
# consequently a pair-core argument may not assume distinct-neighbor
# expansion or reduce the fixed-pair multiplier from the current hypotheses.

F = GF(11)
n, K, m = 11, 1, 3
core = [0, 1]
slopes = list(map(F, range(9)))
r0 = [F(0), F(0)] + [-gamma for gamma in slopes]
r1 = [F(0), F(0)] + [F(1)] * len(slopes)

common_pair_core = [index for index in range(n) if r0[index] == 0 and r1[index] == 0]
assert common_pair_core == core
delta = m - len(common_pair_core)
assert delta == 1

supports = []
for offset, gamma in enumerate(slopes):
    support = [index for index in range(n) if r0[index] + gamma * r1[index] == 0]
    assert support == core + [offset + 2]
    supports.append(tuple(support))

    # Degree-<1 words are constants.  The scalar word has exact maximal
    # zero-agreement support and is post-near.
    scalar_word = [r0[index] + gamma * r1[index] for index in range(n)]
    maximum_constant_agreement = max(
        scalar_word.count(value) for value in F
    )
    assert maximum_constant_agreement == m
    assert n - maximum_constant_agreement > m - K

    # The received pair is not simultaneously constant on this support.
    pair_values = {(r0[index], r1[index]) for index in support}
    assert len(pair_values) == 2

    exception = tuple(index for index in support if index not in common_pair_core)
    assert exception == (offset + 2,)

assert len(set(supports)) == len(slopes)
sharp_capacity = (n - m + delta) // delta
assert len(slopes) == sharp_capacity == 9

print(
    "KB_MCA_RANK11_PAIR_CORE_ROUTE_CUT_SAGE_PASS "
    "parallel_records=9 deficiency=1 sharp_capacity=9"
)
