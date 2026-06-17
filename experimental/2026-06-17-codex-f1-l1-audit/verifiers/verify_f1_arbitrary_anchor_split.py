#!/usr/bin/env python3
"""Verify the F1 arbitrary-anchor locator-split packet.

The packet works over F_17[t]/(t^2-3), with D=F_17^*, k=3, sigma=t=2,
E=X(X-alpha), and N=1.  It checks that two supports have the same monic-anchor
locator readout modulo hatE=lcm(E,E^tau), while an arbitrary anchor splits them
into two different support-wise bad slopes.  It also checks the sunflower-floor
packet realizing floor((16-3)/(5-3))=6 slopes.
"""


class Fp2:
    p = 17
    d = 3

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

    def inv(self):
        den = (self.a * self.a - self.d * self.b * self.b) % self.p
        if den == 0:
            raise ZeroDivisionError("nonzero element expected")
        inv_den = pow(den, -1, self.p)
        return type(self)(self.a * inv_den, -self.b * inv_den)

    def __truediv__(self, other):
        return self * self.coerce(other).inv()

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
        return hash((self.a, self.b))

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        return f"{self.a}+{self.b}t"


F = Fp2
ZERO = F(0)
ONE = F(1)
ALPHA = F(0, 1)


def trim(poly):
    out = poly[:]
    while len(out) > 1 and out[-1] == ZERO:
        out.pop()
    return out


def poly_add(a, b):
    out = []
    for i in range(max(len(a), len(b))):
        out.append((a[i] if i < len(a) else ZERO) + (b[i] if i < len(b) else ZERO))
    return trim(out)


def poly_sub(a, b):
    out = []
    for i in range(max(len(a), len(b))):
        out.append((a[i] if i < len(a) else ZERO) - (b[i] if i < len(b) else ZERO))
    return trim(out)


def poly_scale(c, poly):
    return trim([c * x for x in poly])


def poly_mul(a, b):
    out = [ZERO for _ in range(len(a) + len(b) - 1)]
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            out[i + j] = out[i + j] + ai * bj
    return trim(out)


def poly_eval(poly, x):
    value = ZERO
    for coeff in reversed(poly):
        value = value * x + coeff
    return value


def poly_degree(poly):
    return len(trim(poly)) - 1


def lagrange_interpolate(points, point_values):
    result = [ZERO]
    for i, xi_raw in enumerate(points):
        xi = F(xi_raw)
        basis = [ONE]
        denominator = ONE
        for j, xj_raw in enumerate(points):
            if i == j:
                continue
            xj = F(xj_raw)
            basis = poly_mul(basis, [-xj, ONE])
            denominator = denominator * (xi - xj)
        result = poly_add(result, poly_scale(point_values[i] / denominator, basis))
    return trim(result)


def locator(support):
    poly = [ONE]
    for x in support:
        poly = poly_mul(poly, [-F(x), ONE])
    return poly


def values(poly, support):
    return {x: poly_eval(poly, F(x)) for x in support}


def direction_not_low_degree(e_poly, support, k):
    direction_values = [-(ONE / poly_eval(e_poly, F(x))) for x in support[:k]]
    candidate = lagrange_interpolate(support[:k], direction_values)
    assert poly_degree(candidate) < k
    return any(
        poly_eval(candidate, F(x)) != -(ONE / poly_eval(e_poly, F(x)))
        for x in support[k:]
    )


def quotient_for_core(e_poly, support, slope, core):
    values_on_core = [-(slope / poly_eval(e_poly, F(x))) for x in core]
    r_poly = lagrange_interpolate(core, values_on_core) if core else [ZERO]
    q_poly = poly_add([slope], poly_mul(e_poly, r_poly))
    assert poly_degree(q_poly) < len(support)
    for x in core:
        assert poly_eval(q_poly, F(x)) == ZERO
    return q_poly


def verify_locator_split_packet(e_poly, k, sigma):
    a = k + sigma
    support_s = (1, 3, 4, 7, 9)
    support_t = (1, 2, 11, 12, 16)
    assert len(support_s) == a
    assert len(support_t) == a
    assert set(support_s).intersection(support_t) == {1}

    locator_s = locator(support_s)
    locator_t = locator(support_t)
    roots_hat_e = (ZERO, ALPHA, -ALPHA)
    readout_s = tuple(poly_eval(locator_s, root) for root in roots_hat_e)
    readout_t = tuple(poly_eval(locator_t, root) for root in roots_hat_e)
    assert readout_s == readout_t
    assert readout_s == (F(9), F(2, 5), F(2, 12))

    p_t = [-(ONE / poly_eval(e_poly, F(1)))]
    assert p_t == [F(9, 9)]

    q_s = [ZERO]
    q_t = poly_add([ONE], poly_mul(e_poly, p_t))
    assert poly_degree(q_s) < a
    assert poly_degree(q_t) < a
    assert poly_eval(q_s, F(1)) == poly_eval(q_t, F(1)) == ZERO

    anchor = {}
    anchor.update(values(q_s, support_s))
    for x, value in values(q_t, support_t).items():
        if x in anchor:
            assert anchor[x] == value
        anchor[x] = value

    assert all(poly_eval(q_s, F(x)) == anchor[x] for x in support_s)
    assert all(poly_eval(q_t, F(x)) == anchor[x] for x in support_t)

    assert all(poly_eval(q_s, root) == ZERO for root in (ZERO, ALPHA))
    q_t_minus_one = poly_sub(q_t, [ONE])
    assert all(poly_eval(q_t_minus_one, root) == ZERO for root in (ZERO, ALPHA))

    assert direction_not_low_degree(e_poly, support_s, k)
    assert direction_not_low_degree(e_poly, support_t, k)
    return readout_s, support_s, support_t


def verify_sunflower_floor_packet(e_poly, k, sigma):
    a = k + sigma
    core = (1, 2, 3)
    petals = ((4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15))
    supports = tuple(tuple(core + petal) for petal in petals)
    slopes = tuple(F(i) for i in range(len(supports)))
    assert len(supports) == (16 - k) // sigma == 6

    anchor = {x: ZERO for x in core}
    q_polys = []
    for support, slope, petal in zip(supports, slopes, petals):
        q_poly = quotient_for_core(e_poly, support, slope, core)
        q_polys.append(q_poly)
        for x in petal:
            assert x not in anchor
            anchor[x] = poly_eval(q_poly, F(x))

    for support, slope, q_poly in zip(supports, slopes, q_polys):
        assert all(poly_eval(q_poly, F(x)) == anchor[x] for x in support)
        q_minus_slope = poly_sub(q_poly, [slope])
        assert all(poly_eval(q_minus_slope, root) == ZERO for root in (ZERO, ALPHA))
        assert direction_not_low_degree(e_poly, support, k)

    return supports, slopes


def main():
    k = 3
    sigma = 2

    # E=X(X-alpha)=X^2-alpha X and hatE=X(X-alpha)(X+alpha).
    e_poly = [ZERO, -ALPHA, ONE]
    assert poly_eval(e_poly, F(1)) == F(1) - ALPHA
    assert all(poly_eval(e_poly, F(x)) != ZERO for x in range(1, 17))

    readout_s, support_s, support_t = verify_locator_split_packet(e_poly, k, sigma)
    sunflower_supports, sunflower_slopes = verify_sunflower_floor_packet(
        e_poly, k, sigma
    )

    print("F1 arbitrary-anchor locator-split verifier passed")
    print(f"p=17, k={k}, sigma={sigma}, supports={support_s} and {support_t}")
    print(f"shared locator readout modulo hatE: {readout_s}")
    print("arbitrary anchor splits slopes 0 and 1")
    print(
        "sunflower floor slopes: "
        f"{len(sunflower_slopes)} supports={sunflower_supports}"
    )


if __name__ == "__main__":
    main()
