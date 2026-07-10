#!/usr/bin/env python3
"""Verify the split-pencil G2 support-forcing repair packet.

The replay is standalone.  It checks two fixed-M hybrid witnesses and the
set-level all-scales closure on small 2-power cyclic sets.
"""

from __future__ import annotations


def eval_poly(poly: tuple[int, ...], x: int, p: int) -> int:
    value = 0
    for coefficient in reversed(poly):
        value = (value * x + coefficient) % p
    return value


def locator_coeffs(domain: list[int], indices: list[int], p: int) -> list[int]:
    coeffs = [1]
    for index in indices:
        root = domain[index]
        new = [0] * (len(coeffs) + 1)
        for degree, coefficient in enumerate(coeffs):
            new[degree] = (new[degree] - root * coefficient) % p
            new[degree + 1] = (new[degree + 1] + coefficient) % p
        coeffs = new
    return coeffs


def full_fibers_and_residual(support: set[int], n: int, m: int) -> tuple[int, int]:
    step = n // m
    full = 0
    covered = 0
    for residue in range(step):
        fiber = {residue + step * i for i in range(m)}
        if fiber <= support:
            full += 1
            covered += m
    return full, len(support) - covered


def stabilizer_shifts(support: set[int], n: int, m: int | None = None) -> list[int]:
    if m is None:
        shifts = range(n)
    else:
        step = n // m
        shifts = range(0, n, step)
    return [
        shift
        for shift in shifts
        if all(((point + shift) % n) in support for point in support)
    ]


def verify_fixed_m_failure(
    support: set[int], n: int, m: int, k: int, sigma: int
) -> None:
    size = len(support)
    if not (k + sigma <= size <= k + sigma + m - 1):
        raise AssertionError(("not in top band", n, m, size))
    full, residual = full_fibers_and_residual(support, n, m)
    if residual < m:
        raise AssertionError(("fixed-M staircase unexpectedly holds", n, m, full))
    stabilizer = stabilizer_shifts(support, n, m)
    if len(stabilizer) == 1:
        raise AssertionError(("fixed-M primitive unexpectedly holds", n, m))


def verify_n8_witness() -> None:
    p = 17
    n = 8
    m = 4
    k = 3
    sigma = 1
    domain = [1, 9, 13, 15, 16, 8, 4, 2]

    core = [0, 4]
    petals = [[1, 5], [2, 6], [3, 7]]
    scalars = [1, 5, 8]
    locator = locator_coeffs(domain, core, p)

    values = [0] * n
    for scalar, petal in zip(scalars, petals):
        for index in petal:
            values[index] = scalar * eval_poly(tuple(locator), domain[index], p) % p

    expected_values = [0, 12, 7, 7, 0, 12, 7, 7]
    if values != expected_values:
        raise AssertionError(("n8 word values", values))

    witnesses = (
        ((16, 0, 1), {0, 1, 4, 5}),
        ((9, 0, 8), {0, 3, 4, 7}),
        ((11, 0, 4), {1, 2, 5, 6}),
        ((7, 0, 0), {2, 3, 6, 7}),
    )
    for poly, support in witnesses:
        actual = {i for i, x in enumerate(domain) if eval_poly(poly, x, p) == values[i]}
        if actual != support:
            raise AssertionError(("n8 agreement set", poly, actual, support))
        verify_fixed_m_failure(support, n, m, k, sigma)


def verify_n32_witness() -> None:
    p = 97
    n = 32
    k = 12
    sigma = 1
    domain = [
        1,
        28,
        8,
        30,
        64,
        46,
        27,
        77,
        22,
        34,
        79,
        78,
        50,
        42,
        12,
        45,
        96,
        69,
        89,
        67,
        33,
        51,
        70,
        20,
        75,
        63,
        18,
        19,
        47,
        55,
        85,
        52,
    ]
    values = [
        66,
        0,
        24,
        91,
        0,
        0,
        85,
        0,
        0,
        0,
        0,
        0,
        81,
        28,
        30,
        51,
        0,
        0,
        84,
        60,
        95,
        83,
        28,
        54,
        63,
        34,
        0,
        31,
        0,
        34,
        78,
        62,
    ]
    poly = (92, 95, 18, 0, 83, 72, 47, 36, 35, 14, 49, 10)
    support = {0, 4, 5, 9, 12, 13, 15, 16, 20, 21, 25, 28, 29, 31}

    if any(pow(x, 32, p) != 1 for x in domain) or len(set(domain)) != n:
        raise AssertionError("bad n32 domain")
    generator = domain[1]
    if any(domain[(j + 1) % n] != generator * domain[j] % p for j in range(n)):
        raise AssertionError("bad n32 cyclic order")

    actual = {i for i, x in enumerate(domain) if eval_poly(poly, x, p) == values[i]}
    if actual != support:
        raise AssertionError(("n32 agreement set", actual))
    for m in (4, 8):
        verify_fixed_m_failure(support, n, m, k, sigma)

    full, residual = full_fibers_and_residual(support, n, 2)
    if full != 7 or residual != 0:
        raise AssertionError(("n32 closure scale", full, residual))


def rotate_mask(mask: int, n: int, shift: int) -> int:
    full = (1 << n) - 1
    return ((mask << shift) | (mask >> (n - shift))) & full


def mask_to_set(mask: int, n: int) -> set[int]:
    return {i for i in range(n) if (mask >> i) & 1}


def dyadic_scales(n: int) -> list[int]:
    scales = []
    m = 2
    while m <= n:
        if n % m == 0:
            scales.append(m)
        m *= 2
    return scales


def is_periodic(mask: int, n: int) -> bool:
    return any(rotate_mask(mask, n, shift) == mask for shift in range(1, n))


def staircase_some_scale(mask: int, n: int) -> bool:
    support = mask_to_set(mask, n)
    for m in dyadic_scales(n):
        full, residual = full_fibers_and_residual(support, n, m)
        if full >= 1 and residual < m:
            return True
    return False


def verify_closure_for_masks(n: int, masks) -> tuple[int, int]:
    checked = 0
    periodic = 0
    for mask in masks:
        if mask == 0:
            continue
        checked += 1
        if not is_periodic(mask, n):
            continue
        periodic += 1
        if not staircase_some_scale(mask, n):
            raise AssertionError(("third class", n, mask))
    return checked, periodic


def antipodal_fiber_unions(n: int):
    half = n // 2
    fibers = [(1 << j) | (1 << (j + half)) for j in range(half)]
    for fiber_mask in range(1, 1 << half):
        mask = 0
        for j, fiber in enumerate(fibers):
            if (fiber_mask >> j) & 1:
                mask |= fiber
        yield mask


def verify_all_scales_closure() -> int:
    closure_rows = 0
    for n in (8, 16):
        verify_closure_for_masks(n, range(1, 1 << n))
        closure_rows += 1

    # Every nontrivially periodic subset of a 2-power cyclic set is invariant
    # under the unique order-2 subgroup, so antipodal-fiber unions cover the
    # periodic n=32 case without scanning all 2^32 subsets.
    verify_closure_for_masks(32, antipodal_fiber_unions(32))
    closure_rows += 1
    return closure_rows


def main() -> None:
    verify_n8_witness()
    verify_n32_witness()
    closure_rows = verify_all_scales_closure()
    print(
        "SPLIT_PENCIL_G2_SUPPORT_FORCING_REPAIR_PASS "
        f"fixed_m_witnesses=2 closure_rows={closure_rows}"
    )


if __name__ == "__main__":
    main()
