#!/usr/bin/env python3
"""Toy verifier for the EF interleaved floor import."""

from __future__ import annotations

from itertools import combinations

P = 17
NS = 3  # t^2 = 3 is nonsquare over F_17.


class F2:
    __slots__ = ("a", "b")

    def __init__(self, a: int = 0, b: int = 0):
        self.a = a % P
        self.b = b % P

    def __add__(self, other):
        other = coerce(other)
        return F2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __sub__(self, other):
        other = coerce(other)
        return F2(self.a - other.a, self.b - other.b)

    def __rsub__(self, other):
        return coerce(other) - self

    def __neg__(self):
        return F2(-self.a, -self.b)

    def __mul__(self, other):
        other = coerce(other)
        return F2(
            self.a * other.a + NS * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def inv(self):
        den = (self.a * self.a - NS * self.b * self.b) % P
        inv_den = pow(den, -1, P)
        return F2(self.a * inv_den, -self.b * inv_den)

    def __truediv__(self, other):
        return self * coerce(other).inv()

    def __eq__(self, other):
        try:
            other = coerce(other)
        except TypeError:
            return False
        return self.a == other.a and self.b == other.b

    def __hash__(self):
        return hash((self.a, self.b))

    def __repr__(self):
        return f"{self.a}+{self.b}t" if self.b else str(self.a)


def coerce(value) -> F2:
    if isinstance(value, F2):
        return value
    if isinstance(value, int):
        return F2(value, 0)
    raise TypeError(type(value))


ZERO = F2(0, 0)
ONE = F2(1, 0)
T = F2(0, 1)


def trim(poly: list[F2]) -> list[F2]:
    poly = poly[:]
    while poly and poly[-1] == ZERO:
        poly.pop()
    return poly


def degree(poly: list[F2]) -> int:
    return len(trim(poly)) - 1


def peval(poly: list[F2], x: F2) -> F2:
    out = ZERO
    for coeff in reversed(poly):
        out = out * x + coeff
    return out


def poly_div_linear(poly: list[F2], alpha: F2) -> tuple[list[F2], F2]:
    """Return quotient and remainder for poly(X)/(X-alpha)."""
    coeffs = trim(poly)
    if not coeffs:
        return [], ZERO
    quotient = [ZERO] * (len(coeffs) - 1)
    carry = coeffs[-1]
    for idx in range(len(coeffs) - 2, -1, -1):
        quotient[idx] = carry
        carry = coeffs[idx] + alpha * carry
    return trim(quotient), carry


def interpolate(points: list[tuple[F2, F2]]) -> list[F2]:
    result: list[F2] = []
    for i, (xi, yi) in enumerate(points):
        basis = [ONE]
        denom = ONE
        for j, (xj, _yj) in enumerate(points):
            if i == j:
                continue
            new_basis = [ZERO] * (len(basis) + 1)
            for d, coeff in enumerate(basis):
                new_basis[d] = new_basis[d] - xj * coeff
                new_basis[d + 1] = new_basis[d + 1] + coeff
            basis = new_basis
            denom = denom * (xi - xj)
        scale = yi / denom
        if len(result) < len(basis):
            result.extend([ZERO] * (len(basis) - len(result)))
        for d, coeff in enumerate(basis):
            result[d] = result[d] + scale * coeff
    return trim(result)


def phi(x: F2) -> tuple[int, int]:
    return x.a, x.b


def matmul_mz(z: F2, coords: tuple[int, int]) -> tuple[int, int]:
    a, b = coords
    return ((z.a * a + NS * z.b * b) % P, (z.b * a + z.a * b) % P)


def add_coords(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] + right[0]) % P, (left[1] + right[1]) % P)


def subgroup(order: int) -> list[F2]:
    assert (P - 1) % order == 0
    generator = 3
    step = pow(generator, (P - 1) // order, P)
    out = []
    cur = 1
    for _ in range(order):
        out.append(F2(cur, 0))
        cur = (cur * step) % P
    return out


def check_syndrome_commutes(domain: list[F2]) -> None:
    values = {x: F2(2 * x.a + 1, 3 * x.a + 4) for x in domain}
    for power in range(4):
        ext_sum = ZERO
        coord_sum = (0, 0)
        for x in domain:
            scale = pow(x.a, power, P)
            ext_sum = ext_sum + values[x] * scale
            coord_sum = (
                (coord_sum[0] + values[x].a * scale) % P,
                (coord_sum[1] + values[x].b * scale) % P,
            )
        assert phi(ext_sum) == coord_sum


def check_singleton_floor_import() -> None:
    domain = subgroup(8)
    kappa = 3
    alpha = T
    poly = [F2(5, 1), F2(2, 0), F2(0, 1), F2(3, 0)]
    z = peval(poly, alpha)
    shifted = poly[:]
    shifted[0] = shifted[0] - z
    quotient, remainder = poly_div_linear(shifted, alpha)
    assert remainder == ZERO
    assert degree(quotient) < kappa

    support = domain[: kappa + 1]
    received = {}
    for x in domain:
        received[x] = peval(poly, x) if x in support else F2(x.a + 7, 2 * x.a + 3)

    f_alpha = {x: received[x] / (x - alpha) for x in domain}
    g_alpha = {x: -ONE / (x - alpha) for x in domain}

    for x in support:
        explained = peval(quotient, x)
        assert f_alpha[x] + z * g_alpha[x] == explained
        lhs_coords = add_coords(phi(f_alpha[x]), matmul_mz(z, phi(g_alpha[x])))
        assert lhs_coords == phi(explained)

    for test_support in combinations(domain, kappa + 1):
        interpolant = interpolate([(x, g_alpha[x]) for x in test_support])
        assert degree(interpolant) >= kappa


def main() -> int:
    domain = subgroup(8)
    check_syndrome_commutes(domain)
    print("syndrome_commutes_with_basis_expansion: PASS")
    check_singleton_floor_import()
    print("singleton_multiplication_slice_floor_import: PASS")
    print("EF_INTERLEAVED_FLOOR_IMPORT_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
