"""Exact c=0 post-near counterexample to the discarded n-m=w inference."""

F = GF(11)
D = list(F)[:10]
n = 10
K = 3
d = 1
m = K + d
w = d
U = D[:m]
outside = D[m:]

# The received pair is zero on U.  At outside coordinate x_j set
# (r0,r1)=(-gamma_j,1), with distinct gamma_j.
gammas = list(F)[:len(outside)]
r0 = {x: F(0) for x in U}
r1 = {x: F(0) for x in U}
for x, gamma in zip(outside, gammas):
    r0[x] = -gamma
    r1[x] = F(1)

Rpoly.<X> = PolynomialRing(F)
codewords = []
for c0 in F:
    for c1 in F:
        for c2 in F:
            f = c0 + c1 * X + c2 * X^2
            codewords.append(tuple(f(x) for x in D))

for x_star, gamma in zip(outside, gammas):
    word = tuple(r0[x] + gamma * r1[x] for x in D)
    distance = min(sum(a != b for a, b in zip(word, cw)) for cw in codewords)
    assert distance <= n - m - 1
    assert distance > w

    # Three common-core coordinates plus x_star give an exact size-m scalar
    # support for h=0.  Any explaining pair would vanish on K core points,
    # hence be identically zero, contradicting r1(x_star)=1.
    support = U[:K] + [x_star]
    assert len(support) == m
    assert all(r0[x] + gamma * r1[x] == 0 for x in support)
    pair_contained = False
    for a0 in F:
        for a1 in F:
            for a2 in F:
                a = a0 + a1 * X + a2 * X^2
                if any(a(x) != r0[x] for x in support):
                    continue
                for b0 in F:
                    for b1 in F:
                        for b2 in F:
                            b = b0 + b1 * X + b2 * X^2
                            if all(b(x) == r1[x] for x in support):
                                pair_contained = True
                                break
                        if pair_contained:
                            break
                    if pair_contained:
                        break
                if pair_contained:
                    break
            if pair_contained:
                break
        if pair_contained:
            break
    assert not pair_contained

# On U, both received restrictions are the global zero codeword, so c=0.
assert all(r0[x] == 0 and r1[x] == 0 for x in U)
print("KB_MCA_GLUING_RANK_ZERO_POST_NEAR_COUNTEREXAMPLE_SAGE_PASS")
print(f"slopes={len(gammas)} minimum_distance_gt={w}")
