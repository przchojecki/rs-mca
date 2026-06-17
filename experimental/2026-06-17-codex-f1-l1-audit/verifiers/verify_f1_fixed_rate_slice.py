#!/usr/bin/env python3
"""Verify the fixed-rate Vieta-slice lower bound for the F1 counterexample.

The proof is elementary, but this script checks the finite packet mechanics:
for B=F_p, F=F_p[t]/(t^2-d), H=F_p^*, k, a=k+1, and fixed
T of size a-2, the slopes z_{T union {x,y}} are distinct as {x,y} varies.
"""

from itertools import combinations


class Fp2:
    p = None
    d = None

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = int(a) % self.p
        self.b = int(b) % self.p

    @classmethod
    def coerce(cls, other):
        return other if isinstance(other, cls) else cls(other, 0)

    def __add__(self, other):
        other = self.coerce(other)
        return type(self)(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        other = self.coerce(other)
        return type(self)(self.a - other.a, self.b - other.b)

    def __neg__(self):
        return type(self)(-self.a, -self.b)

    def __mul__(self, other):
        other = self.coerce(other)
        return type(self)(
            self.a * other.a + self.d * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def __pow__(self, exponent):
        result = type(self)(1)
        base = self
        while exponent:
            if exponent & 1:
                result = result * base
            base = base * base
            exponent >>= 1
        return result

    def __eq__(self, other):
        other = self.coerce(other)
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b, self.p, self.d))

    def __repr__(self):
        return str(self.a) if self.b == 0 else f"{self.a}+{self.b}t"


def make_field(p, d):
    class F(Fp2):
        pass

    F.p = p
    F.d = d
    return F


def legendre(a, p):
    return pow(a % p, (p - 1) // 2, p)


def first_nonsquare(p):
    for d in range(2, p):
        if legendre(d, p) == p - 1:
            return d
    raise ValueError("no nonsquare found")


def slice_slopes(p, k, d=None):
    if d is None:
        d = first_nonsquare(p)
    F = make_field(p, d)
    alpha = F(0, 1)
    a = k + 1
    if a < 2 or a > p - 1:
        raise ValueError("need 2 <= a <= p-1")

    domain = list(range(1, p))
    fixed_tail = domain[: a - 2]
    pool = domain[a - 2 :]

    tail_product = F(1)
    for t in fixed_tail:
        tail_product = tail_product * (alpha - F(t))

    alpha_a = alpha**a
    slopes = {}
    for x, y in combinations(pool, 2):
        pair_product = (alpha - F(x)) * (alpha - F(y))
        z = alpha_a - tail_product * pair_product
        slopes[z] = (x, y)

    return len(slopes), len(pool) * (len(pool) - 1) // 2, d


def extension_degree_numerator_rows(p, k, degrees):
    distinct, expected, d = slice_slopes(p, k)
    assert distinct == expected
    rows = []
    for degree in degrees:
        assert degree >= 2
        denominator = p**degree
        rows.append(
            {
                "extension_degree": degree,
                "bad_slopes": distinct,
                "density_num": distinct,
                "density_den": denominator,
                "forced_numerator": distinct,
                "base_numerator": p,
                "numerator_ratio_lower": distinct / p,
                "nonsquare": d,
            }
        )
    return rows


def main():
    cases = [
        (7, 3),
        (17, 8),
        (31, 15),
        (97, 48),
    ]
    for p, k in cases:
        distinct, expected, d = slice_slopes(p, k)
        assert distinct == expected
        density = distinct / (p * p)
        print(
            f"p={p}, k={k}, d={d}: slice slopes {distinct}/{p*p} "
            f"(density {density:.6f})"
        )
    rows = extension_degree_numerator_rows(17, 8, (2, 3, 6))
    for row in rows:
        print(
            "extension degree {extension_degree}: "
            "bad slopes={bad_slopes}, density={density_num}/{density_den}, "
            "forced numerator/base numerator >= {numerator_ratio_lower:.6f}".format(
                **row
            )
        )
    print("F1 fixed-rate slice verifier passed")


if __name__ == "__main__":
    main()
