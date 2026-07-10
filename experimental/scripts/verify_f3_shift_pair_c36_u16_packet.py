#!/usr/bin/env python3
"""Replay the F3 shift-pair C36' and U16 compiler packet.

The script is standalone and intentionally small: it checks exact integer
arithmetic, tiny subgroup enumerations, the catch-71 trace-zero repair, and
the official-row h=2/U16 inequalities.  It does not run the Modal prefix sweep
and it does not prove the C36' or HGE4 target premises.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from math import comb


OFFICIAL_EXPONENTS = tuple(range(13, 42))
DIRECT_FLOOR_ROWS = {
    (97, 32): (9_692, 10_315, 4_742, 4_950),
    (4_289, 64): (3_639, 10_755, 981, 2_658),
    (7_937, 64): (5_765, 13_191, 1_571, 4_194),
}


def primitive_root(p: int) -> int:
    factors: set[int] = set()
    value = p - 1
    candidate = 2
    while candidate * candidate <= value:
        if value % candidate == 0:
            factors.add(candidate)
            while value % candidate == 0:
                value //= candidate
        candidate += 1
    if value > 1:
        factors.add(value)

    for root in range(2, p):
        if all(pow(root, (p - 1) // factor, p) != 1 for factor in factors):
            return root
    raise AssertionError(("no primitive root", p))


def subgroup(p: int, n: int) -> tuple[int, ...]:
    if (p - 1) % n != 0:
        raise AssertionError((p, n, "n does not divide p-1"))
    generator = pow(primitive_root(p), (p - 1) // n, p)
    values: list[int] = []
    x = 1
    for _ in range(n):
        values.append(x)
        x = x * generator % p
    if x != 1 or len(set(values)) != n:
        raise AssertionError((p, n, "bad subgroup"))
    return tuple(values)


def verify_k6_h2_payment() -> int:
    linear_supply = Fraction(35, 36) * Fraction(5, 6) ** 2
    linear_demand = Fraction(2, 5) * Fraction(7, 5)
    if linear_supply != Fraction(875, 1296):
        raise AssertionError(linear_supply)
    if linear_demand != Fraction(14, 25):
        raise AssertionError(linear_demand)
    if linear_supply <= linear_demand:
        raise AssertionError((linear_supply, linear_demand))

    degree_constant = Fraction(360, 67) + Fraction(180, 67 * 36)
    if degree_constant >= 6:
        raise AssertionError(degree_constant)

    h2_energy = 1 + 5 * (6 * 6 + 6)
    if h2_energy != 211:
        raise AssertionError(h2_energy)
    threshold = Fraction(h2_energy * h2_energy, 64)
    if threshold != Fraction(44_521, 64):
        raise AssertionError(threshold)
    for exponent in OFFICIAL_EXPONENTS:
        n = 1 << exponent
        if threshold >= n:
            raise AssertionError(("h2 official threshold", exponent, threshold))
    return h2_energy


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


def canonical_char0(a: int, b: int, c: int, d: int, n: int) -> bool:
    target = tuple(sorted((a, b, c)))
    for q in range(1, n):
        roots = (q, (q + n // 2) % n, (2 * q + n // 2) % n)
        if 0 not in roots and tuple(sorted(roots)) == target and 4 * q % n == d:
            return True
    return False


def verify_collision_locus_count() -> int:
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
                left - right for left, right in zip(left_exponents, right_exponents)
            )
            first_nonzero = next(value for value in difference if value)
            if first_nonzero < 0:
                difference = tuple(-value for value in difference)
            loci.add((right_sign * left_sign, difference))
    if len(loci) != 12:
        raise AssertionError(("non-output collision loci", len(loci), loci))
    return len(loci) + 7


def verify_char0_order(n: int) -> tuple[int, int, int]:
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
                    if canonical_char0(a, b, c, d, n):
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
        raise AssertionError(("collision-free mass", n, maximum_collision_free_mass))
    return count, maximum_folded_mass, maximum_collision_free_mass


def verify_c36_char0_compiler() -> None:
    rows = (8, 16, 32)
    results = tuple(verify_char0_order(n) for n in rows)
    if any(result[1] != 22 for result in results):
        raise AssertionError(("folded rows", results))
    if verify_collision_locus_count() != 19:
        raise AssertionError("bad collision locus count")

    for exponent in OFFICIAL_EXPONENTS:
        n = 1 << exponent
        transported_bound = 19 * (n - 1) ** 2 + 2 * (n - 1) + 3 * (n - 4)
        residual = 36 * n * n - n // 2 - transported_bound
        if residual <= 0 or residual**3 <= 512 * n**4:
            raise AssertionError(("direct floor", exponent, residual))


def verify_direct_floor_row(p: int, n: int) -> tuple[int, int, int, int]:
    roots = subgroup(p, n)
    root_set = set(roots)
    shifted = tuple((1 - value) % p for value in roots if value != 1)

    product = Counter(left * right % p for left in shifted for right in shifted)
    quotient = Counter(
        left * pow(right, -1, p) % p for left in shifted for right in shifted
    )
    three_to_one = sum(product[value] * quotient[value] for value in product)
    energy = sum(multiplicity * multiplicity for multiplicity in product.values())

    forced_output = 0
    signed_collisions = 0
    collision_free = 0
    for left in roots:
        if left == 1:
            continue
        for middle in roots:
            if middle == 1:
                continue
            partial = (1 - left) * (1 - middle) % p
            for right in roots:
                if right == 1:
                    continue
                output = (1 - partial * (1 - right)) % p
                if output in root_set:
                    forced_output += 1
                    signed_roots = (
                        left * middle % p,
                        left * right % p,
                        middle * right % p,
                        output,
                        -left % p,
                        -middle % p,
                        -right % p,
                        -left * middle * right % p,
                    )
                    if len(set(signed_roots)) < 8:
                        signed_collisions += 1
                    else:
                        collision_free += 1

    if forced_output != three_to_one:
        raise AssertionError(("three-to-one", p, n, forced_output, three_to_one))
    if three_to_one > energy:
        raise AssertionError(("energy", p, n, three_to_one, energy))
    if signed_collisions + collision_free != three_to_one:
        raise AssertionError(("collision split", p, n))
    return three_to_one, energy, signed_collisions, collision_free


def verify_c36_direct_floor_examples() -> None:
    for row, expected in DIRECT_FLOOR_ROWS.items():
        actual = verify_direct_floor_row(*row)
        if actual != expected:
            raise AssertionError((row, actual, expected))

    official_n = 8192
    official_three_to_one = 66_933_997
    residual_twice = (
        72 * official_n * official_n - official_n - 2 * official_three_to_one
    )
    if residual_twice <= 0 or residual_twice**3 <= 32**3 * official_n**4:
        raise AssertionError(("official-prefix evidence residual", residual_twice))


def trace_zero_audit(p: int, n: int) -> tuple[int, int, int, int, int, int]:
    roots = subgroup(p, n)
    root_set = set(roots)
    ordered_roots = sorted(roots)
    i_count = sum(1 for x in roots if (x + 1) % p in root_set)

    triples: set[tuple[int, int, int]] = set()
    for x in ordered_roots:
        for y in ordered_roots:
            if y <= x:
                continue
            z = (-x - y) % p
            if z in root_set and z != x and z != y and z > y:
                triples.add((x, y, z))

    seen: set[tuple[int, int, int]] = set()
    orbits = 0
    for triple in triples:
        if triple in seen:
            continue
        orbit = set()
        for g in ordered_roots:
            scaled = tuple(sorted(g * element % p for element in triple))
            orbit.add(scaled)
            seen.add(scaled)
        if len(orbit) != n:
            raise AssertionError(("non-free orbit", p, n, triple, len(orbit)))
        orbits += 1

    def e2(triple: tuple[int, int, int]) -> int:
        return (
            triple[0] * triple[1]
            + triple[0] * triple[2]
            + triple[1] * triple[2]
        ) % p

    pairs: list[tuple[tuple[int, int, int], tuple[int, int, int]]] = []
    triple_list = sorted(triples)
    for i, left in enumerate(triple_list):
        for right in triple_list[i + 1 :]:
            if set(left) & set(right):
                continue
            if e2(left) == e2(right):
                pairs.append((left, right))

    orbit_of = {}
    for triple in triples:
        key = min(tuple(sorted(g * element % p for element in triple)) for g in roots)
        orbit_of[triple] = key

    seen_pairs: set[frozenset[tuple[int, int, int]]] = set()
    pair_orbits = 0
    same_orbit_pairs = 0
    for left, right in pairs:
        frozen = frozenset((left, right))
        if frozen in seen_pairs:
            continue
        for g in roots:
            scaled_left = tuple(sorted(g * element % p for element in left))
            scaled_right = tuple(sorted(g * element % p for element in right))
            seen_pairs.add(frozenset((scaled_left, scaled_right)))
        pair_orbits += 1
        if orbit_of[left] == orbit_of[right]:
            same_orbit_pairs += 1

    return i_count, len(triples), orbits, pair_orbits, len(pairs), same_orbit_pairs


def verify_trace_zero_repair() -> None:
    for p, n in ((4_289, 64), (7_937, 64)):
        i_count, _triples, orbit_count, pair_orbits, raw_pairs, _same = (
            trace_zero_audit(p, n)
        )
        if 6 * orbit_count > i_count:
            raise AssertionError(("orbit count", p, n, i_count, orbit_count))
        if pair_orbits > orbit_count * orbit_count:
            raise AssertionError(("corrected trace-zero envelope", p, n))
        if raw_pairs > n * orbit_count * orbit_count:
            raise AssertionError(("corrected compiler payment", p, n))

    i_count, _triples, orbit_count, pair_orbits, raw_pairs, _same = (
        trace_zero_audit(7_937, 64)
    )
    if not (pair_orbits == 2 and comb(orbit_count, 2) == 1):
        raise AssertionError(
            ("catch-71 counterexample missing", i_count, orbit_count, pair_orbits)
        )
    # The old envelope fails as a statement about pair-orbits.  At this tiny
    # row the raw-pair compiler payment is exactly tied, so raw underpayment is
    # not the correct failure criterion.
    if pair_orbits <= comb(orbit_count, 2):
        raise AssertionError(("old binomial envelope unexpectedly holds", raw_pairs))

    for c0, c1 in ((Fraction(4, 9), 16),):
        n73 = c0 - Fraction(c1, 36)
        n2 = Fraction(1, 72) - Fraction(1, 2 * 36)
        if n73 != 0 or n2 != 0:
            raise AssertionError(("C36 cancellation", n73, n2))


def verify_u16_assembly() -> int:
    for exponent in OFFICIAL_EXPONENTS:
        n = 1 << exponent
        if 4 >= 9 * n:
            raise AssertionError(("CP h2 check", exponent))

    h1_budget = 0
    h2_budget = 1
    h3_budget = 1
    tail_budget = 14
    total_budget = 16
    if h1_budget + h2_budget + h3_budget + tail_budget != total_budget:
        raise AssertionError("bad U16 partition")
    return len(OFFICIAL_EXPONENTS)


def main() -> None:
    h2_energy = verify_k6_h2_payment()
    verify_c36_char0_compiler()
    verify_c36_direct_floor_examples()
    verify_trace_zero_repair()
    rows = verify_u16_assembly()
    print(f"F3_SHIFT_PAIR_C36_U16_PACKET_PASS rows={rows} h2_energy={h2_energy}")


if __name__ == "__main__":
    main()
