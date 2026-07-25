#!/usr/bin/env sage
"""Sage replay for the M31 rank-seven source-basis overlap dichotomy."""

from collections import deque


K = ZZ(1048576)
W = ZZ(67447)
G = ZZ(354972)
J = 4981


def direct_cap(rank, dimension, excess):
    inner = binomial(K + rank - 1, rank - 1) // binomial(
        excess + rank - 1, rank - 1
    )
    output = (K + dimension) * inner // (excess + dimension)
    denominator = (
        (excess + dimension)^2
        - (K + dimension) * (dimension - 1)
    )
    if denominator > 0:
        output = min(
            output,
            (K + dimension) * (excess + 1) // denominator,
        )
    return output


def recurrence(maximum, excess):
    arrays = {}
    arrays[1] = [ZZ(0)] + [
        (K + dimension) // (excess + dimension)
        for dimension in range(1, maximum + 1)
    ]
    for rank in range(2, 7):
        child = arrays[rank - 1]
        current = list(child)
        prefix = ZZ(-1)
        window = deque()
        for dimension in range(rank, maximum + 1):
            added = dimension - 1
            prefix = max(prefix, child[added])
            while window and child[window[-1]] <= child[added]:
                window.pop()
            window.append(added)
            lower = dimension - (dimension - 1) // (rank - 1)
            while window and window[0] < lower:
                window.popleft()
            value = (
                (dimension - 1) * prefix
                + (K + 1) * child[window[0]]
            ) // (excess + dimension)
            current[dimension] = max(
                child[dimension],
                min(value, direct_cap(rank, dimension, excess)),
            )
        arrays[rank] = current
    return arrays


zero = recurrence(J, W)
one = recurrence(J - 1, W + 1)
assert zero[5][J - 1] == 674155
assert zero[6][J] == 9806438
assert one[6][J - 1] == 444522
assert 5 * (zero[5][J - 1] - zero[5][J - 5]) == 3273960

# Finite-field source control.  Five roots are private to G_0; every other
# locator has one private root.  The normalized f_i=(P/G_i)b_i use b_i=1.
F = GF(101)
RX = PolynomialRing(F, "X")
X = RX.gen()
private = [
    [F(1), F(2), F(3), F(4), F(5)],
    [F(6)],
    [F(7)],
    [F(8)],
    [F(9)],
    [F(10)],
    [F(11)],
]
G_polys = [
    prod(X - root for root in roots)
    for roots in private
]
P_poly = prod(G_polys)
f_polys = [P_poly // locator for locator in G_polys]

evaluation = matrix(
    F,
    [
        [poly(root) for poly in f_polys]
        for roots in private
        for root in roots
    ],
)
assert evaluation.rank() == 7
assert gcd(f_polys) == 1

# Every private root evaluates on exactly its coordinate axis.
offset = 0
for index, roots in enumerate(private):
    for row in range(offset, offset + len(roots)):
        assert evaluation[row, index] != 0
        assert all(
            evaluation[row, other] == 0
            for other in range(7)
            if other != index
        )
    offset += len(roots)

# For lambda=sum coordinates, the kernel has rank six and all five type-zero
# private roots restrict to the same nonzero projective functional.
lambda_sum = matrix(F, 1, 7, [1] * 7)
kernel_sum = lambda_sum.right_kernel().basis_matrix()
assert kernel_sum.nrows() == 6
restricted = evaluation * kernel_sum.transpose()
assert all(not restricted[row].is_zero() for row in range(11))
for row in range(1, 5):
    assert matrix(F, [restricted[0], restricted[row]]).rank() == 1

# The nonvanishing qualifier is load-bearing: lambda=e_0 makes all type-zero
# private roots common direction zeros.
lambda_axis = matrix(F, 1, 7, [1, 0, 0, 0, 0, 0, 0])
kernel_axis = lambda_axis.right_kernel().basis_matrix()
restricted_axis = evaluation * kernel_axis.transpose()
assert all(restricted_axis[row].is_zero() for row in range(5))
assert all(not restricted_axis[row].is_zero() for row in range(5, 11))

assert 2 * G - 28 == 709916
assert 709916 - G == 354944
assert ceil(ZZ(354944) / binomial(7, 2)) == 16903

print(
    "M31 rank7 source-basis overlap Sage replay: PASS "
    "(exact recurrence and finite-field source control)"
)
