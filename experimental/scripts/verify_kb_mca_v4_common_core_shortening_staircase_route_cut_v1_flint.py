#!/usr/bin/env python3
"""Independent FLINT replay of the load-bearing KoalaBear integer walls."""

from math import comb

from flint import fmpq, fmpz


n = fmpz(2097152)
k = fmpz(1048576)
m = fmpz(1116048)
d = m - k
R = n - k
B = fmpz(274980728111395087)

assert d == 67472 and R == 1048576 and n - m == 981104
assert 32 * d - 2 * R == 61952


def ceil_div(x, y):
    return (x + y - 1) // y


def degree_floor(c):
    c = fmpz(c)
    return ceil_div(32 * (m - c), n - c)


assert degree_floor(4130) == 18
assert degree_floor(4131) == 17
assert degree_floor(k - 1) == 3


def J(s):
    value = fmpq(1)
    for i in range(s + 1):
        value *= fmpq(R + i, d + i)
    return value.numerator // value.denominator


assert J(13) == 47876303026096432
assert J(14) == 743896698428332665
assert B - J(13) == 227104425085298655
assert B - J(14) == -468915970316937578

for s, expected in [
    (1, 549756338176),
    (2, 192154133857304576),
    (3, 50372197381489643749376),
]:
    bound = min(fmpz(comb(int(R + s), int(d + s))), fmpz(comb(int(R + s), s + 1)))
    assert bound == expected

c = 4131
numerator = fmpz(comb(int(n), c))
denominator = fmpz(comb(int(m), c))
ceiling = ceil_div(numerator, denominator)
assert numerator > B * denominator
assert int(ceiling).bit_length() == 3765
assert len(str(ceiling)) == 1134

print("PASS FLINT common-core staircase arithmetic")
print("degree18_last=4130 degree17_first=4131")
print(f"J13={J(13)} J14={J(14)} JoBits={int(ceiling).bit_length()}")
