#!/usr/bin/env python3
"""Exact replay for the rate-half cyclic quotient-rotation list floor."""

from __future__ import annotations

from itertools import combinations
from math import comb, gcd, isqrt


N_OFFICIAL = 1 << 41
K_OFFICIAL = 1 << 40
C_OFFICIAL = 1 << 33
AGREEMENT = K_OFFICIAL + (1 << 34) - 1
ERRORS = N_OFFICIAL - AGREEMENT
Q0 = 3 * N_OFFICIAL + 1


def trim(poly: list[int]) -> list[int]:
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def mul(left: list[int], right: list[int], prime: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i + j] = (out[i + j] + a * b) % prime
    return trim(out)


def evaluate(poly: list[int], value: int, prime: int) -> int:
    out = 0
    for coefficient in reversed(poly):
        out = (out * value + coefficient) % prime
    return out


def product_linear(roots: tuple[int, ...], prime: int) -> list[int]:
    out = [1]
    for root in roots:
        out = mul(out, [(-root) % prime, 1], prime)
    return out


def find_power_two_root(prime: int, order: int) -> int:
    assert order > 1 and order & (order - 1) == 0
    assert (prime - 1) % order == 0
    cofactor = (prime - 1) // order
    for seed in range(2, prime):
        root = pow(seed, cofactor, prime)
        if pow(root, order, prime) == 1 and pow(root, order // 2, prime) != 1:
            return root
    raise AssertionError("no root of requested order")


def rotate(locator: list[int], size: int, d: int, delta: int,
           prime: int) -> list[int]:
    out = [0] * size
    for j, coefficient in enumerate(locator):
        exponent = size - d + j
        if exponent >= size:
            exponent -= size
            coefficient *= delta
        out[exponent] = (out[exponent] + coefficient) % prime
    return trim(out)


def substitute_power(poly: list[int], c: int) -> list[int]:
    out = [0] * ((len(poly) - 1) * c + 1)
    for i, coefficient in enumerate(poly):
        out[i * c] = coefficient
    return trim(out)


def padded(poly: list[int], length: int) -> tuple[int, ...]:
    return tuple(poly) + (0,) * (length - len(poly))


def toy_replay(prime: int, n: int, c: int, d: int,
               s: int) -> tuple[int, int, int]:
    k = n // 2
    size = n // c
    m = size // 2 + d
    root = find_power_two_root(prime, n)
    domain = tuple(pow(root, i, prime) for i in range(n))
    quotient = tuple(dict.fromkeys(pow(x, c, prime) for x in domain))
    assert len(quotient) == size
    deltas = {pow(y, size, prime) for y in quotient}
    assert len(deltas) == 1
    delta = next(iter(deltas))

    distinguished = quotient[0]
    fiber = tuple(x for x in domain if pow(x, c, prime) == distinguished)
    tail = fiber[:s]
    tail_locator = product_linear(tail, prime)
    buckets: dict[tuple[int, ...], list[tuple[tuple[int, ...], list[int]]]] = {}
    constant_terms: set[int] = set()
    reduced_key_high: dict[tuple[int, ...], tuple[int, ...]] = {}
    constant_is_load_bearing = False

    for chosen in combinations(quotient[1:], m):
        quotient_locator = product_linear(chosen, prime)
        rotated = rotate(quotient_locator, size, d, delta, prime)
        locator = mul(tail_locator, substitute_power(rotated, c), prime)
        locator_pad = padded(locator, n)

        for x in domain:
            y = pow(x, c, prime)
            assert evaluate(rotated, y, prime) == (
                pow(y, size - d, prime)
                * evaluate(quotient_locator, y, prime)
            ) % prime

        key = tuple(quotient_locator[:d])
        buckets.setdefault(key, []).append((chosen, locator))
        constant_terms.add(quotient_locator[0])
        reduced = tuple(quotient_locator[1:d])
        old_high = reduced_key_high.get(reduced)
        if old_high is not None and old_high != locator_pad[k:]:
            constant_is_load_bearing = True
        reduced_key_high.setdefault(reduced, locator_pad[k:])

    total = comb(size - 1, m)
    denominator = size * prime ** (d - 1)
    lower = (total + denominator - 1) // denominator
    assert len(constant_terms) <= size
    assert len(buckets) <= denominator
    assert constant_is_load_bearing

    bucket = max(buckets.values(), key=len)
    assert len(bucket) >= lower
    common_high = padded(bucket[0][1], n)[k:]
    words: set[tuple[int, ...]] = set()
    for chosen, locator in bucket:
        locator_pad = padded(locator, n)
        assert locator_pad[k:] == common_high
        codeword = tuple((-locator_pad[i]) % prime for i in range(k))
        words.add(codeword)
        expected = set(tail)
        expected.update(x for x in domain if pow(x, c, prime) in chosen)
        actual = {x for x in domain if evaluate(locator, x, prime) == 0}
        assert actual == expected
        assert len(actual) == k + d * c + s
        received = (0,) * k + common_high
        agreement = sum(
            evaluate(list(received), x, prime)
            == evaluate(list(codeword), x, prime)
            for x in domain
        )
        assert agreement == len(actual)
    assert len(words) == len(bucket)
    return total, lower, len(bucket)


def support_map_audit() -> int:
    checks = 0
    for size in range(4, 66, 2):
        half = size // 2
        for d in range(1, half):
            m = half + d
            image = {}
            for j in range(m + 1):
                exponent = size - d + j
                image[j] = exponent - size if exponent >= size else exponent
            assert {j for j, exponent in image.items() if exponent >= half} == (
                set(range(d)) | {m}
            )
            assert image[m] == half
            checks += 1
    return checks


def pocklington_anchor() -> int:
    assert Q0 - 1 == 3 * N_OFFICIAL
    assert Q0 - 1 > isqrt(Q0)
    base = 5
    assert pow(base, Q0 - 1, Q0) == 1
    for prime_divisor in (2, 3):
        assert gcd(pow(base, (Q0 - 1) // prime_divisor, Q0) - 1, Q0) == 1
    subgroup_generator = pow(base, 3, Q0)
    assert pow(subgroup_generator, N_OFFICIAL, Q0) == 1
    assert pow(subgroup_generator, N_OFFICIAL // 2, Q0) != 1
    return subgroup_generator


def official_arithmetic() -> dict[str, int | bool]:
    size = N_OFFICIAL // C_OFFICIAL
    d = 1
    m = size // 2 + d
    count = comb(size - 1, m)
    list_lower = (count + size - 1) // size
    assert (size, m) == (256, 129)
    assert AGREEMENT == K_OFFICIAL + 2 * C_OFFICIAL - 1
    assert ERRORS == (1 << 40) - (1 << 34) + 1
    assert count % size == 221
    assert list_lower == (
        11092230961998080258863221315535829014398723445840079610908300691051869570
    )
    assert list_lower > 1 << 238
    assert list_lower > 1 << 128

    # Radius is beyond the RS Johnson radius exactly when agreement is below
    # sqrt(n(k-1)); no floating point participates in this gate.
    assert AGREEMENT * AGREEMENT < N_OFFICIAL * (K_OFFICIAL - 1)
    assert not (ERRORS * ERRORS > N_OFFICIAL * (K_OFFICIAL - 1))

    # For every q<2^256, floor(q/2^128)<2^128<list_lower.
    assert ((1 << 256) - 1) // (1 << 128) < 1 << 128

    mutation_checks = sum((
        list_lower != count // size,  # replacing ceil by floor
        AGREEMENT != K_OFFICIAL + 2 * C_OFFICIAL,  # dropping s=c-1
        not (ERRORS * ERRORS > N_OFFICIAL * (K_OFFICIAL - 1)),
        list_lower < count,  # dropping the quotient-prefix factor N
    ))
    assert mutation_checks == 4

    return {
        "n": N_OFFICIAL,
        "k": K_OFFICIAL,
        "agreement": AGREEMENT,
        "radius_numerator": ERRORS,
        "radius_denominator": N_OFFICIAL,
        "list_lower": list_lower,
        "list_lower_bits": list_lower.bit_length(),
        "johnson_exact": True,
        "mutation_checks": mutation_checks,
    }


def main() -> None:
    toy_d1 = toy_replay(193, 64, 4, 1, 2)
    toy_d2 = toy_replay(97, 32, 2, 2, 1)
    support_checks = support_map_audit()
    generator = pocklington_anchor()
    row = official_arithmetic()
    print(
        "RATE_HALF_CYCLIC_QUOTIENT_ROTATION_LIST_FLOOR_PASS "
        f"toy_d1={toy_d1} toy_d2={toy_d2} "
        f"support_checks={support_checks} q0={Q0} generator={generator} "
        f"agreement={row['agreement']} radius={row['radius_numerator']}/"
        f"{row['radius_denominator']} list_bits={row['list_lower_bits']} "
        f"post_johnson=true mutations={row['mutation_checks']}/4"
    )


if __name__ == "__main__":
    main()
