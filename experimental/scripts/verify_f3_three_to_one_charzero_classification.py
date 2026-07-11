#!/usr/bin/env python3
"""Replay the exact characteristic-zero h=3 three-to-one classification."""

from __future__ import annotations

from collections import Counter
from itertools import permutations


def reduce_exponent(exponent: int, n: int) -> tuple[int, int]:
    exponent %= n
    half = n // 2
    if exponent >= half:
        return exponent - half, -1
    return exponent, 1


def relation_vector(a: int, b: int, c: int, d: int, n: int) -> Counter[int]:
    terms = (
        (-1, a),
        (-1, b),
        (-1, c),
        (1, a + b),
        (1, a + c),
        (1, b + c),
        (-1, a + b + c),
        (1, d),
    )
    result: Counter[int] = Counter()
    for coefficient, exponent in terms:
        reduced, sign = reduce_exponent(exponent, n)
        result[reduced] += coefficient * sign
        if result[reduced] == 0:
            del result[reduced]
    return result


def signed_root_exponents(
    a: int, b: int, c: int, d: int, n: int
) -> tuple[int, ...]:
    half = n // 2
    return (
        (a + b) % n,
        (a + c) % n,
        (b + c) % n,
        d % n,
        (a + half) % n,
        (b + half) % n,
        (c + half) % n,
        (a + b + c + half) % n,
    )


def verify_collision_locus_count() -> int:
    # Excluding the output root, equality of two signed monomials is recorded
    # by (right-hand sign, exponent difference), modulo inversion.
    monomials = (
        (1, (1, 1, 0)),
        (1, (1, 0, 1)),
        (1, (0, 1, 1)),
        (-1, (1, 0, 0)),
        (-1, (0, 1, 0)),
        (-1, (0, 0, 1)),
        (-1, (1, 1, 1)),
    )
    loci: set[tuple[int, tuple[int, int, int]]] = set()
    for index, (left_sign, left_exponents) in enumerate(monomials):
        for right_sign, right_exponents in monomials[index + 1 :]:
            difference = tuple(
                left - right
                for left, right in zip(left_exponents, right_exponents)
            )
            first_nonzero = next(value for value in difference if value)
            if first_nonzero < 0:
                difference = tuple(-value for value in difference)
            loci.add((right_sign * left_sign, difference))
    if len(loci) != 12:
        raise AssertionError(("non-output collision loci", len(loci), loci))
    return len(loci) + 7


def canonical(a: int, b: int, c: int, d: int, n: int) -> bool:
    target = tuple(sorted((a, b, c)))
    for q in range(1, n):
        roots = (q, (q + n // 2) % n, (2 * q + n // 2) % n)
        if 0 not in roots and tuple(sorted(roots)) == target and 4 * q % n == d:
            return True
    return False


def verify_order(n: int) -> tuple[int, int, int]:
    count = 0
    canonical_count = 0
    maximum_folded_mass = 0
    maximum_collision_free_mass = 0
    for a in range(1, n):
        for b in range(1, n):
            for c in range(1, n):
                for d in range(1, n):
                    relation = relation_vector(a, b, c, d, n)
                    if len({a, b, c}) == 3:
                        maximum_folded_mass = max(
                            maximum_folded_mass,
                            sum(coefficient**2 for coefficient in relation.values()),
                        )
                    if len(set(signed_root_exponents(a, b, c, d, n))) == 8:
                        maximum_collision_free_mass = max(
                            maximum_collision_free_mass,
                            sum(coefficient**2 for coefficient in relation.values()),
                        )
                    if relation:
                        continue
                    count += 1
                    if canonical(a, b, c, d, n):
                        canonical_count += 1
    expected = 3 * (n - 4)
    if count != expected or canonical_count != expected:
        raise AssertionError((n, count, canonical_count, expected))

    generated = set()
    for q in range(1, n):
        roots = (q, (q + n // 2) % n, (2 * q + n // 2) % n)
        d = 4 * q % n
        if 0 in roots or d == 0:
            continue
        for ordered in permutations(roots):
            if relation_vector(*ordered, d, n):
                raise AssertionError(("forward", n, q, ordered, d))
            generated.add((*ordered, d))
    if len(generated) != expected:
        raise AssertionError(("generated", n, len(generated), expected))
    if maximum_folded_mass != 22:
        raise AssertionError(("folded mass", n, maximum_folded_mass))
    expected_collision_free = 0 if n == 8 else 8
    if maximum_collision_free_mass != expected_collision_free:
        raise AssertionError(
            ("collision-free mass", n, maximum_collision_free_mass)
        )
    return count, maximum_folded_mass, maximum_collision_free_mass


def main() -> None:
    rows = (8, 16, 32)
    results = tuple(verify_order(n) for n in rows)
    if any(result[1] != 22 for result in results):
        raise AssertionError(("folded rows", results))

    for exponent in range(13, 42):
        n = 1 << exponent
        transported_bound = (
            19 * (n - 1) ** 2 + 2 * (n - 1) + 3 * (n - 4)
        )
        residual = 36 * n * n - n // 2 - transported_bound
        if residual <= 0 or residual**3 <= 512 * n**4:
            raise AssertionError(("direct floor", exponent, residual))
    collision_loci = verify_collision_locus_count()
    print(
        "H3_THREE_TO_ONE_CHARZERO_CLASSIFICATION_PASS "
        f"rows={len(rows)} folded={max(result[1] for result in results)} "
        f"collision_free={max(result[2] for result in results)} "
        f"collision_loci={collision_loci}"
    )


if __name__ == "__main__":
    main()
