#!/usr/bin/env python3
"""Verify the F1 arbitrary-anchor locator-split and sunflower packet.

This checks the finite packet in
experimental/notes/f1/f1_arbitrary_anchor_locator_split.md over
F_17[t]/(t^2-3).  It verifies:

* two supports with the same monic-anchor readout modulo hatE split into
  different support-wise bad slopes under an arbitrary anchor;
* the core-k sunflower construction realizes floor((n-k)/sigma) bad slopes;
* the core-k choice maximizes the sunflower floor among all core sizes c<=k.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

Element = tuple[int, int]
Poly = list[Element]

P = 17
D = 3
ZERO = (0, 0)
ONE = (1, 0)
ALPHA = (0, 1)


def elt(a: int, b: int = 0) -> Element:
    return (a % P, b % P)


def add(x: Element, y: Element) -> Element:
    return ((x[0] + y[0]) % P, (x[1] + y[1]) % P)


def neg(x: Element) -> Element:
    return ((-x[0]) % P, (-x[1]) % P)


def sub(x: Element, y: Element) -> Element:
    return add(x, neg(y))


def mul(x: Element, y: Element) -> Element:
    return (
        (x[0] * y[0] + D * x[1] * y[1]) % P,
        (x[0] * y[1] + x[1] * y[0]) % P,
    )


def inv(x: Element) -> Element:
    norm = (x[0] * x[0] - D * x[1] * x[1]) % P
    if norm == 0:
        raise ZeroDivisionError(x)
    norm_inv = pow(norm, -1, P)
    return ((x[0] * norm_inv) % P, (-x[1] * norm_inv) % P)


def div(x: Element, y: Element) -> Element:
    return mul(x, inv(y))


def trim(poly: Poly) -> Poly:
    out = poly[:]
    while len(out) > 1 and out[-1] == ZERO:
        out.pop()
    return out


def poly_add(left: Poly, right: Poly) -> Poly:
    out = []
    for idx in range(max(len(left), len(right))):
        x = left[idx] if idx < len(left) else ZERO
        y = right[idx] if idx < len(right) else ZERO
        out.append(add(x, y))
    return trim(out)


def poly_sub(left: Poly, right: Poly) -> Poly:
    return poly_add(left, [neg(coeff) for coeff in right])


def poly_scale(scalar: Element, poly: Poly) -> Poly:
    return trim([mul(scalar, coeff) for coeff in poly])


def poly_mul(left: Poly, right: Poly) -> Poly:
    out = [ZERO for _ in range(len(left) + len(right) - 1)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = add(out[i + j], mul(x, y))
    return trim(out)


def poly_eval(poly: Poly, x: Element) -> Element:
    value = ZERO
    for coeff in reversed(poly):
        value = add(mul(value, x), coeff)
    return value


def poly_degree(poly: Poly) -> int:
    return len(trim(poly)) - 1


def interpolate(points: tuple[int, ...], values: list[Element]) -> Poly:
    result: Poly = [ZERO]
    for i, xi_raw in enumerate(points):
        xi = elt(xi_raw)
        basis: Poly = [ONE]
        denominator = ONE
        for j, xj_raw in enumerate(points):
            if i == j:
                continue
            xj = elt(xj_raw)
            basis = poly_mul(basis, [neg(xj), ONE])
            denominator = mul(denominator, sub(xi, xj))
        result = poly_add(result, poly_scale(div(values[i], denominator), basis))
    return trim(result)


def locator(support: tuple[int, ...]) -> Poly:
    out: Poly = [ONE]
    for x in support:
        out = poly_mul(out, [neg(elt(x)), ONE])
    return out


def values(poly: Poly, support: tuple[int, ...]) -> dict[int, Element]:
    return {x: poly_eval(poly, elt(x)) for x in support}


def direction_not_low_degree(e_poly: Poly, support: tuple[int, ...], k: int) -> bool:
    direction_values = [neg(inv(poly_eval(e_poly, elt(x)))) for x in support[:k]]
    candidate = interpolate(support[:k], direction_values)
    if poly_degree(candidate) >= k:
        raise AssertionError("direction interpolant should have degree < k")
    return any(
        poly_eval(candidate, elt(x)) != neg(inv(poly_eval(e_poly, elt(x))))
        for x in support[k:]
    )


def quotient_for_zero_core(
    e_poly: Poly, slope: Element, core: tuple[int, ...]
) -> Poly:
    core_values = [neg(div(slope, poly_eval(e_poly, elt(x)))) for x in core]
    r_poly = interpolate(core, core_values) if core else [ZERO]
    return poly_add([slope], poly_mul(e_poly, r_poly))


def verify_core_optimization(n: int, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    floors = {c: (n - c) // (a - c) for c in range(k + 1)}
    optimized = (n - k) // sigma
    if max(floors.values()) != optimized:
        raise AssertionError((floors, optimized))

    real_values = [Fraction(n - c, a - c) for c in range(k + 1)]
    if real_values != sorted(real_values):
        raise AssertionError(real_values)

    return {"floors": floors, "optimized": optimized}


def verify_core_optimization_grid(max_n: int = 80) -> int:
    checked = 0
    for n in range(2, max_n + 1):
        for k in range(1, n):
            for sigma in range(1, n - k + 1):
                verify_core_optimization(n, k, sigma)
                checked += 1
    return checked


def verify_locator_split_packet(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    support_s = (1, 3, 4, 7, 9)
    support_t = (1, 2, 11, 12, 16)
    if len(support_s) != a or len(support_t) != a:
        raise AssertionError("wrong support sizes")
    if set(support_s).intersection(support_t) != {1}:
        raise AssertionError("expected one-point overlap")

    locator_s = locator(support_s)
    locator_t = locator(support_t)
    roots_hat_e = (ZERO, ALPHA, neg(ALPHA))
    readout_s = tuple(poly_eval(locator_s, root) for root in roots_hat_e)
    readout_t = tuple(poly_eval(locator_t, root) for root in roots_hat_e)
    if readout_s != readout_t:
        raise AssertionError("locator readouts should agree modulo hatE")
    if readout_s != (elt(9), elt(2, 5), elt(2, 12)):
        raise AssertionError(readout_s)

    q_s: Poly = [ZERO]
    q_t = poly_add([ONE], poly_mul(e_poly, [neg(inv(poly_eval(e_poly, elt(1))))]))
    if poly_degree(q_s) >= a or poly_degree(q_t) >= a:
        raise AssertionError("witness degree too large")
    if poly_eval(q_s, elt(1)) != ZERO or poly_eval(q_t, elt(1)) != ZERO:
        raise AssertionError("anchor values disagree on overlap")

    anchor: dict[int, Element] = {}
    anchor.update(values(q_s, support_s))
    for x, value in values(q_t, support_t).items():
        if x in anchor and anchor[x] != value:
            raise AssertionError("anchor conflict")
        anchor[x] = value

    if not all(poly_eval(q_s, elt(x)) == anchor[x] for x in support_s):
        raise AssertionError("slope 0 witness fails")
    if not all(poly_eval(q_t, elt(x)) == anchor[x] for x in support_t):
        raise AssertionError("slope 1 witness fails")

    if not direction_not_low_degree(e_poly, support_s, k):
        raise AssertionError("slope 0 should be noncontained")
    if not direction_not_low_degree(e_poly, support_t, k):
        raise AssertionError("slope 1 should be noncontained")

    return {
        "support_s": support_s,
        "support_t": support_t,
        "shared_hatE_readout": readout_s,
    }


def verify_sunflower_floor_packet(e_poly: Poly, k: int, sigma: int) -> dict[str, object]:
    a = k + sigma
    domain = tuple(range(1, 17))
    core = (1, 2, 3)
    petals = ((4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15))
    supports = tuple(tuple(core + petal) for petal in petals)
    slopes = tuple(elt(i) for i in range(len(supports)))
    expected_floor = (len(domain) - k) // sigma
    if len(supports) != expected_floor:
        raise AssertionError((len(supports), expected_floor))

    anchor = {x: ZERO for x in core}
    q_polys = []
    for support, slope, petal in zip(supports, slopes, petals):
        q_poly = quotient_for_zero_core(e_poly, slope, core)
        if poly_degree(q_poly) >= a:
            raise AssertionError("sunflower witness degree too large")
        q_polys.append(q_poly)
        for x in petal:
            if x in anchor:
                raise AssertionError("petals should be disjoint")
            anchor[x] = poly_eval(q_poly, elt(x))

    for support, slope, q_poly in zip(supports, slopes, q_polys):
        if not all(poly_eval(q_poly, elt(x)) == anchor[x] for x in support):
            raise AssertionError("sunflower witness does not match anchor")
        q_minus_slope = poly_sub(q_poly, [slope])
        if not all(poly_eval(q_minus_slope, root) == ZERO for root in (ZERO, ALPHA)):
            raise AssertionError("sunflower witness has wrong residue modulo E")
        if not direction_not_low_degree(e_poly, support, k):
            raise AssertionError("sunflower support should be noncontained")

    return {"core": core, "supports": supports, "slope_count": len(slopes)}


@dataclass(frozen=True)
class Verification:
    core_optimization: dict[str, object]
    core_grid_checks: int
    locator_split: dict[str, object]
    sunflower: dict[str, object]


def verify() -> Verification:
    k = 3
    sigma = 2
    n = 16
    e_poly = [ZERO, neg(ALPHA), ONE]  # E=X(X-alpha)
    if not all(poly_eval(e_poly, elt(x)) != ZERO for x in range(1, 17)):
        raise AssertionError("E should be nonzero on D=F_17^*")
    return Verification(
        core_optimization=verify_core_optimization(n, k, sigma),
        core_grid_checks=verify_core_optimization_grid(),
        locator_split=verify_locator_split_packet(e_poly, k, sigma),
        sunflower=verify_sunflower_floor_packet(e_poly, k, sigma),
    )


def main() -> None:
    result = verify()
    print("f1_arbitrary_anchor_split: PASS")
    print(
        "core floor optimization: "
        f"max={result.core_optimization['optimized']} "
        f"floors={result.core_optimization['floors']}"
    )
    print(f"core optimization grid checks: {result.core_grid_checks}")
    print(
        "locator split: supports="
        f"{result.locator_split['support_s']} and {result.locator_split['support_t']}"
    )
    print(
        "sunflower floor: "
        f"{result.sunflower['slope_count']} slopes on core {result.sunflower['core']}"
    )


if __name__ == "__main__":
    main()
