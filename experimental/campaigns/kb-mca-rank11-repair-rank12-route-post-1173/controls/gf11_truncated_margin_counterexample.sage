# Exact post-near counterexample to treating a truncated margin as raw.

F = GF(11)
D = [F(i) for i in range(9)]
K = 4
m = 6
w = m - K
S = list(range(6))

r0 = [F(0)] * 6 + [F(1)] * 3
r1 = [F(0), F(0), F(1), F(4), F(5), F(5), F(0), F(0), F(0)]


def evaluation(coeffs):
    return [sum(coeffs[j] * x**j for j in range(len(coeffs))) for x in D]


code = [
    evaluation(coeffs)
    for coeffs in cartesian_product([F] * K)
]

# The slope gamma=0 is post-near: its received scalar word is r0.
max_scalar_agreement = max(
    sum(r0[i] == word[i] for i in range(len(D)))
    for word in code
)
assert max_scalar_agreement == 6
assert len(D) - max_scalar_agreement == 3 > w

# On S, no degree-<K word equals r1, so the exact support is pair-noncontained.
assert all(any(word[i] != r1[i] for i in S) for word in code)

# Use C'=span{1,X}.  Every affine direction matches r1 on at most two
# support coordinates, and this maximum is attained.
directions = [
    [a + b * D[i] for i in range(len(D))]
    for a in F for b in F
]
best = max(sum(direction[i] == r1[i] for i in S) for direction in directions)
assert best == 2

raw_margin = m - best
truncated_margin = min(w + 1, raw_margin)
pair_core_on_support = best

assert raw_margin == 4
assert truncated_margin == 3
assert pair_core_on_support == 2
assert pair_core_on_support < m - truncated_margin

print(
    "KB_MCA_GF11_TRUNCATED_MARGIN_COUNTEREXAMPLE_PASS "
    f"post_near_distance={len(D)-max_scalar_agreement} "
    f"raw={raw_margin} truncated={truncated_margin} core={pair_core_on_support}"
)
