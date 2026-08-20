#!/usr/bin/env python3
"""Independent FLINT replay of repaired affine-span integer walls."""

from flint import fmpq, fmpz


def falling(value, length):
    result = fmpz(1)
    for index in range(length):
        result *= value - index
    return result


def rising(value, length):
    result = fmpz(1)
    for index in range(length):
        result *= value + index
    return result


def bound(n, K, m, rank, theta=1):
    w = m - K
    first = fmpq(
        falling(n, rank + 1),
        fmpz(m) * theta * rising(w + 1, rank - 1),
    )
    second = fmpq(
        falling(n - K + rank, rank + 1),
        fmpz(theta) * rising(w + 1, rank),
    )
    value = max(first, second)
    return value.numerator // value.denominator


# Exact GF(257) arithmetic: the old theorem says 8, the repaired theorem 759.
n, K, m = fmpz(256), fmpz(1), fmpz(86)
w = m - K
old = max(
    falling(n, 2) // (m * w),
    falling(n, 2) // (w * (w + 1)),
)
assert old == 8
assert bound(n, K, m, 1) == 759

kb_n, kb_K, kb_m = fmpz(2097152), fmpz(1048576), fmpz(1116048)
kb_w = kb_m - kb_K
budget = fmpz(274980728111395087)
caps = [bound(kb_n, kb_K, kb_m, rank) for rank in range(1, 10)]
assert caps[7] == 110390969172173096
assert caps[8] == 3430729820133944932
assert caps[7] + 2 * kb_w == 110390969172308040
assert budget - caps[7] - 2 * kb_w == 164589758939087047

thresholds = [(9, 13), (10, 388), (11, 12050)]
expected = [263902293856457302, 274790124064526354, 274970108028773601]
assert [bound(kb_n, kb_K, kb_m, rank, theta)
        for rank, theta in thresholds] == expected
assert [bound(kb_n, kb_K, kb_m, rank, theta - 1) + 2 * kb_w
        for rank, theta in thresholds] == [
    285894151677963688,
    275500176064828033,
    274992929018868606,
]

R, d = fmpz(1048576), fmpz(67472)
assert bound(R + 9, 9, d + 9, 9) == 55413538236037195
assert bound(R + 10, 10, d + 10, 10) == 861057176799343503

print(
    "KB_MCA_SUPPORT_LOCAL_THETA_FLINT_PASS "
    "gf257_old=8 gf257_repaired=759 kb_wall=8/9 "
    "error_wall=9/10 shortened_wall=9/10"
)
