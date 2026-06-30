#!/usr/bin/env python3
"""Verify the M1 popularity divisor-gate lemma.

The checks are finite algebra/combinatorics only. They verify that nonzero
univariate gates give the claimed popularity cap, and that the resulting
constant composes with the high-overlap popularity support floor.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from verify_m1_high_overlap_graph_budget import (
    support_floor_from_popularity_cap,
)


PRIMES = (5, 7, 11, 13, 17, 19, 23, 29)


def trim(poly: tuple[int, ...], p: int) -> tuple[int, ...]:
    coeffs = [value % p for value in poly]
    while coeffs and coeffs[-1] == 0:
        coeffs.pop()
    return tuple(coeffs)


def degree(poly: tuple[int, ...], p: int) -> int:
    reduced = trim(poly, p)
    if not reduced:
        raise ValueError("zero polynomial has no divisor-gate degree")
    return len(reduced) - 1


def eval_poly(poly: tuple[int, ...], x: int, p: int) -> int:
    total = 0
    power = 1
    for coeff in poly:
        total = (total + coeff * power) % p
        power = (power * x) % p
    return total


def roots(poly: tuple[int, ...], p: int) -> set[int]:
    degree(poly, p)
    return {x for x in range(p) if eval_poly(poly, x, p) == 0}


def normalize_projective(point: tuple[int, int], p: int) -> tuple[int, int]:
    x, z = point
    if x % p:
        inv_x = pow(x % p, p - 2, p)
        return (1, (z * inv_x) % p)
    if z % p:
        inv_z = pow(z % p, p - 2, p)
        return ((x * inv_z) % p, 1)
    raise ValueError("zero projective point")


def projective_line(p: int) -> list[tuple[int, int]]:
    return [(value, 1) for value in range(p)] + [(1, 0)]


def eval_binary_form(form: tuple[int, ...], point: tuple[int, int], p: int) -> int:
    x, z = point
    degree_bound = len(form) - 1
    total = 0
    for x_degree, coeff in enumerate(form):
        z_degree = degree_bound - x_degree
        total += coeff * pow(x, x_degree, p) * pow(z, z_degree, p)
    return total % p


def binary_degree(form: tuple[int, ...], p: int) -> int:
    if not form or all(coeff % p == 0 for coeff in form):
        raise ValueError("zero binary form has no divisor-gate degree")
    return len(form) - 1


def projective_roots(form: tuple[int, ...], p: int) -> set[tuple[int, int]]:
    binary_degree(form, p)
    return {
        point
        for point in projective_line(p)
        if eval_binary_form(form, point, p) == 0
    }


def multiply_binary_forms(
    left: tuple[int, ...], right: tuple[int, ...], p: int
) -> tuple[int, ...]:
    product = [0] * (len(left) + len(right) - 1)
    for i, a_i in enumerate(left):
        for j, b_j in enumerate(right):
            product[i + j] = (product[i + j] + a_i * b_j) % p
    return tuple(product)


def binary_form_from_projective_roots(
    selected_roots: list[tuple[int, int]], p: int
) -> tuple[int, ...]:
    form = (1,)
    for root in selected_roots:
        a, b = normalize_projective(root, p)
        # bX-aZ vanishes at [a:b].  Coefficients are ordered by X-degree.
        linear = ((-a) % p, b % p)
        form = multiply_binary_forms(form, linear, p)
    return form


def divisor_gate_cap(
    multiplicity: int,
    exceptional_size: int,
    degree_bounds: list[int],
) -> int:
    if multiplicity < 0 or exceptional_size < 0:
        raise ValueError("negative gate parameter")
    if any(bound < 0 for bound in degree_bounds):
        raise ValueError("negative degree bound")
    return multiplicity * (exceptional_size + sum(degree_bounds))


@dataclass(frozen=True)
class GateInstance:
    p: int
    multiplicity: int
    exceptional: frozenset[int]
    polynomials: tuple[tuple[int, ...], ...]

    @property
    def degree_bounds(self) -> list[int]:
        return [degree(poly, self.p) for poly in self.polynomials]

    @property
    def allowed_parameters(self) -> set[int]:
        allowed = set(self.exceptional)
        for poly in self.polynomials:
            allowed.update(roots(poly, self.p))
        return allowed

    @property
    def cap(self) -> int:
        return divisor_gate_cap(
            self.multiplicity,
            len(self.exceptional),
            self.degree_bounds,
        )


def nonzero_poly_from_roots(selected_roots: list[int], p: int) -> tuple[int, ...]:
    coeffs = [1]
    for root in selected_roots:
        nxt = [0] * (len(coeffs) + 1)
        for index, coeff in enumerate(coeffs):
            nxt[index] = (nxt[index] - coeff * root) % p
            nxt[index + 1] = (nxt[index + 1] + coeff) % p
        coeffs = nxt
    return trim(tuple(coeffs), p)


def make_random_instance(rng: random.Random, p: int, trial: int) -> GateInstance:
    multiplicity = 1 + trial % 4
    exceptional_size = trial % 5
    exceptional = frozenset(rng.sample(range(p), min(exceptional_size, p)))
    polynomials: list[tuple[int, ...]] = []
    for gate_index in range(1 + trial % 4):
        root_count = rng.randint(0, min(5, p - 1))
        root_pool = [x for x in range(p) if x not in exceptional]
        selected = rng.sample(root_pool, min(root_count, len(root_pool)))
        poly = nonzero_poly_from_roots(selected, p)
        # Add a nonzero scalar and occasionally a higher constant perturbation
        # that keeps the polynomial nonzero but changes its root set.
        scalar = 1 + (trial + gate_index) % (p - 1)
        poly = tuple((scalar * coeff) % p for coeff in poly)
        if trial % 7 == 0:
            poly = trim((poly[0] + 1,) + poly[1:], p)
        if not trim(poly, p):
            poly = (1,)
        polynomials.append(poly)
    return GateInstance(p, multiplicity, exceptional, tuple(polynomials))


def check_root_bound() -> None:
    checked = 0
    for p in PRIMES:
        for degree_bound in range(0, 7):
            for mask in range(1, min(p ** (degree_bound + 1), 600)):
                coeffs = []
                value = mask
                for _ in range(degree_bound + 1):
                    coeffs.append(value % p)
                    value //= p
                poly = trim(tuple(coeffs), p)
                if not poly:
                    continue
                root_count = len(roots(poly, p))
                actual_degree = degree(poly, p)
                if root_count > actual_degree:
                    raise AssertionError((p, poly, actual_degree, root_count))
                checked += 1
    print(f"root_bound_polynomials_checked={checked}")


def check_projective_root_bound() -> None:
    checked = 0
    for p in PRIMES:
        for degree_bound in range(0, 7):
            limit = min(p ** (degree_bound + 1), 700)
            for mask in range(1, limit):
                coeffs = []
                value = mask
                for _ in range(degree_bound + 1):
                    coeffs.append(value % p)
                    value //= p
                form = tuple(coeffs)
                if all(coeff % p == 0 for coeff in form):
                    continue
                root_count = len(projective_roots(form, p))
                actual_degree = binary_degree(form, p)
                if root_count > actual_degree:
                    raise AssertionError((p, form, actual_degree, root_count))
                checked += 1

        points = projective_line(p)
        rng = random.Random(20260701 + p)
        for trial in range(200):
            selected = rng.sample(points, rng.randint(0, min(6, len(points))))
            form = binary_form_from_projective_roots(selected, p)
            root_count = len(projective_roots(form, p))
            if root_count > binary_degree(form, p):
                raise AssertionError((p, selected, form, root_count))
            if not set(selected).issubset(projective_roots(form, p)):
                raise AssertionError((p, selected, form, projective_roots(form, p)))
            checked += 1
    print(f"projective_root_forms_checked={checked}")


def check_random_gate_instances() -> None:
    rng = random.Random(20260630)
    checked = 0
    sharp = 0
    for trial in range(900):
        p = PRIMES[trial % len(PRIMES)]
        instance = make_random_instance(rng, p, trial)
        allowed = instance.allowed_parameters
        if len(allowed) > len(instance.exceptional) + sum(instance.degree_bounds):
            raise AssertionError((trial, instance, allowed))

        leaves = []
        for parameter in sorted(allowed):
            for copy in range(instance.multiplicity):
                leaves.append((parameter, copy))
        if len(leaves) > instance.cap:
            raise AssertionError((trial, len(leaves), instance.cap, instance))
        if len(leaves) == instance.cap:
            sharp += 1

        # Any subset of covered leaves also satisfies the same cap.
        rng.shuffle(leaves)
        subset = leaves[: rng.randint(0, len(leaves))]
        if len(subset) > instance.cap:
            raise AssertionError((trial, len(subset), instance.cap))
        checked += 1
    print(f"random_gate_instances_checked={checked}")
    print(f"sharp_gate_instances_seen={sharp}")


def check_random_projective_gate_instances() -> None:
    rng = random.Random(20260702)
    checked = 0
    sharp = 0
    for trial in range(900):
        p = PRIMES[trial % len(PRIMES)]
        points = projective_line(p)
        multiplicity = 1 + trial % 5
        exceptional = set(rng.sample(points, rng.randint(0, min(5, len(points)))))
        forms = []
        for _ in range(1 + trial % 4):
            root_pool = [point for point in points if point not in exceptional]
            selected = rng.sample(root_pool, rng.randint(0, min(5, len(root_pool))))
            form = binary_form_from_projective_roots(selected, p)
            if trial % 6 == 0:
                form = tuple(
                    (coeff + (1 if index == 0 else 0)) % p
                    for index, coeff in enumerate(form)
                )
                if all(coeff % p == 0 for coeff in form):
                    form = (1,)
            forms.append(form)

        allowed = set(exceptional)
        degree_bounds = []
        for form in forms:
            allowed.update(projective_roots(form, p))
            degree_bounds.append(binary_degree(form, p))
        cap = divisor_gate_cap(multiplicity, len(exceptional), degree_bounds)
        leaves = []
        for point in sorted(allowed):
            for copy in range(multiplicity):
                leaves.append((point, copy))
        if len(leaves) > cap:
            raise AssertionError((trial, p, len(leaves), cap, forms, exceptional))
        if len(leaves) == cap:
            sharp += 1
        checked += 1
    print(f"random_projective_gate_instances_checked={checked}")
    print(f"sharp_projective_gate_instances_seen={sharp}")


def check_support_floor_composition() -> None:
    checked = 0
    for k in range(2, 24):
        for s in range(1, 12):
            for h in range(1, 5):
                for degree_cap in range(1, 7):
                    for lambda_cap in range(0, s):
                        for multiplicity in range(1, 5):
                            for exceptional_size in range(0, 5):
                                degree_bounds = [0, 1 + (k % 4), 2 + (s % 3)]
                                gate_cap = divisor_gate_cap(
                                    multiplicity,
                                    exceptional_size,
                                    degree_bounds,
                                )
                                floor = support_floor_from_popularity_cap(
                                    k,
                                    s,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                    gate_cap,
                                )
                                weaker_floor = support_floor_from_popularity_cap(
                                    k,
                                    s,
                                    h,
                                    degree_cap,
                                    lambda_cap,
                                    gate_cap + 1,
                                )
                                if floor < weaker_floor:
                                    raise AssertionError(
                                        (
                                            k,
                                            s,
                                            h,
                                            degree_cap,
                                            lambda_cap,
                                            gate_cap,
                                            floor,
                                            weaker_floor,
                                        )
                                    )
                                checked += 1
    print(f"support_floor_compositions_checked={checked}")


def main() -> None:
    check_root_bound()
    check_projective_root_bound()
    check_random_gate_instances()
    check_random_projective_gate_instances()
    check_support_floor_composition()
    print("m1 popularity divisor-gate checks passed")


if __name__ == "__main__":
    main()
