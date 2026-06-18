#!/usr/bin/env python3
"""Audit the projective geometry of the M1 depth-two Kummer divisor."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


PRIMES = (5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
LINE_NAMES = ("u", "v", "w", "inf")


def inv(value: int, p: int) -> int:
    return pow(value % p, p - 2, p)


def qform(point: tuple[int, int, int], p: int) -> int:
    u, v, z = point
    return (
        u * u
        + v * v
        + u * v
        + u * z
        + v * z
        + z * z
    ) % p


def qgradient(point: tuple[int, int, int], p: int) -> tuple[int, int, int]:
    u, v, z = point
    return (
        (2 * u + v + z) % p,
        (u + 2 * v + z) % p,
        (u + v + 2 * z) % p,
    )


def affine_a(u: int, v: int, p: int) -> int:
    return (-(u * u + v * v + u * v + u + v + 1)) % p


def line(point: tuple[int, int, int], name: str, p: int) -> int:
    u, v, z = point
    if name == "u":
        return u % p
    if name == "v":
        return v % p
    if name == "w":
        return (u + v + z) % p
    if name == "inf":
        return z % p
    raise ValueError(name)


def normalize(point: tuple[int, int, int], p: int) -> tuple[int, int, int]:
    for coordinate in point:
        if coordinate % p:
            scale = inv(coordinate, p)
            return tuple((value * scale) % p for value in point)
    raise ValueError("zero projective point")


def projective_points(p: int) -> list[tuple[int, int, int]]:
    points = []
    seen = set()
    for u in range(p):
        for v in range(p):
            for z in range(p):
                if (u, v, z) == (0, 0, 0):
                    continue
                point = normalize((u, v, z), p)
                if point not in seen:
                    seen.add(point)
                    points.append(point)
    return points


def line_intersections(p: int) -> set[tuple[int, int, int]]:
    points = set()
    for left_index, left in enumerate(LINE_NAMES):
        for right in LINE_NAMES[left_index + 1 :]:
            pair_points = [
                point
                for point in projective_points(p)
                if line(point, left, p) == 0 and line(point, right, p) == 0
            ]
            if len(pair_points) != 1:
                raise AssertionError((p, left, right, pair_points))
            points.add(pair_points[0])
    return points


def conic_line_intersections(p: int) -> set[tuple[int, int, int]]:
    points = set()
    for name in LINE_NAMES:
        intersection = [
            point
            for point in projective_points(p)
            if line(point, name, p) == 0 and qform(point, p) == 0
        ]
        expected_count = 1 + legendre(-3, p)
        if len(intersection) != expected_count:
            raise AssertionError((p, name, expected_count, intersection))
        for point in intersection:
            grad = qgradient(point, p)
            if all(coordinate == 0 for coordinate in grad):
                raise AssertionError((p, "singular conic", point))
            if line_tangent_parallel_to_gradient(name, grad, p):
                raise AssertionError((p, "tangent", name, point, grad))
            points.add(point)
    return points


def affine_conic_value_counts(p: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for u in range(p):
        for v in range(p):
            counts[affine_a(u, v, p)] += 1
    return counts


def check_affine_conic_distribution(p: int) -> tuple[int, int, int]:
    counts = affine_conic_value_counts(p)
    epsilon = legendre(-3, p)
    special_value = (-2 * inv(3, p)) % p
    special_count = p + epsilon * (p - 1)
    generic_count = p - epsilon
    for value in range(p):
        expected = special_count if value == special_value else generic_count
        if counts[value] != expected:
            raise AssertionError((p, value, counts[value], expected))
    return special_value, special_count, generic_count


def line_tangent_parallel_to_gradient(
    name: str,
    gradient: tuple[int, int, int],
    p: int,
) -> bool:
    line_gradients = {
        "u": (1, 0, 0),
        "v": (0, 1, 0),
        "w": (1, 1, 1),
        "inf": (0, 0, 1),
    }
    target = line_gradients[name]
    nonzero = [index for index, value in enumerate(target) if value % p]
    if not nonzero:
        raise AssertionError(name)
    scale = gradient[nonzero[0]] * inv(target[nonzero[0]], p)
    return all(gradient[index] % p == scale * target[index] % p for index in range(3))


def selected_line_intersections(
    names: tuple[str, ...],
    p: int,
) -> set[tuple[int, int, int]]:
    points = set()
    for left, right in combinations(names, 2):
        pair_points = [
            point
            for point in projective_points(p)
            if line(point, left, p) == 0 and line(point, right, p) == 0
        ]
        if len(pair_points) != 1:
            raise AssertionError((p, left, right, pair_points))
        point = pair_points[0]
        if qform(point, p) == 0:
            raise AssertionError((p, "line-line point on conic", left, right, point))
        points.add(point)
    expected = len(names) * (len(names) - 1) // 2
    if len(points) != expected:
        raise AssertionError((p, names, points, expected))
    return points


def check_line_conic_transversality(names: tuple[str, ...], p: int) -> None:
    for name in names:
        intersection = [
            point
            for point in projective_points(p)
            if line(point, name, p) == 0 and qform(point, p) == 0
        ]
        expected_rational = 1 + legendre(-3, p)
        if len(intersection) != expected_rational:
            raise AssertionError((p, name, expected_rational, intersection))
        for point in intersection:
            grad = qgradient(point, p)
            if line_tangent_parallel_to_gradient(name, grad, p):
                raise AssertionError((p, "tangent", name, point, grad))


def two_coordinate_euler_targets(p: int) -> list[tuple[tuple[str, str], int, int]]:
    rows = []
    for active_lines in combinations(("u", "v", "w"), 2):
        selected_line_intersections(active_lines, p)
        check_line_conic_transversality(active_lines, p)
        finite_pair_intersections = 1 + 2 * len(active_lines)
        finite_component_chi = 2 * (len(active_lines) + 1)
        finite_divisor_chi = finite_component_chi - finite_pair_intersections
        finite_complement_chi = 3 - finite_divisor_chi
        if finite_complement_chi != 2:
            raise AssertionError((p, active_lines, finite_complement_chi))

        infinity_lines = active_lines + ("inf",)
        selected_line_intersections(infinity_lines, p)
        check_line_conic_transversality(infinity_lines, p)
        infinity_pair_intersections = 3 + 2 * len(infinity_lines)
        infinity_component_chi = 2 * (len(infinity_lines) + 1)
        infinity_divisor_chi = infinity_component_chi - infinity_pair_intersections
        infinity_complement_chi = 3 - infinity_divisor_chi
        if infinity_complement_chi != 4:
            raise AssertionError((p, active_lines, infinity_complement_chi))

        rows.append((active_lines, finite_complement_chi, infinity_complement_chi))
    return rows


def legendre(value: int, p: int) -> int:
    residue = pow(value % p, (p - 1) // 2, p)
    if residue == p - 1:
        return -1
    return residue


def main() -> None:
    checked = []
    for p in PRIMES:
        if p <= 3:
            raise AssertionError(p)
        conic_singular_points = [
            point
            for point in projective_points(p)
            if qform(point, p) == 0
            and all(coordinate == 0 for coordinate in qgradient(point, p))
        ]
        if conic_singular_points:
            raise AssertionError((p, conic_singular_points))
        pair_line_points = line_intersections(p)
        conic_points = conic_line_intersections(p)
        if pair_line_points & conic_points:
            raise AssertionError((p, pair_line_points & conic_points))
        if len(pair_line_points) != 6:
            raise AssertionError((p, pair_line_points))
        if len(conic_points) != 4 * (1 + legendre(-3, p)):
            raise AssertionError((p, conic_points))
        special_value, special_count, generic_count = (
            check_affine_conic_distribution(p)
        )
        checked.append(
            (
                p,
                len(pair_line_points),
                len(conic_points),
                legendre(-3, p),
                special_value,
                special_count,
                generic_count,
                two_coordinate_euler_targets(p),
            )
        )
    print(f"verify_m1_kummer_divisor_geometry: PASS checked={checked}")


if __name__ == "__main__":
    main()
