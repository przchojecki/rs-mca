#!/usr/bin/env python3
"""Verify the M1 all-line Hankel aperiodic split-locator ledger.

Status: PROVED finite normal form / AUDIT verifier.

This script checks the finite object requested by the M1 all-line aperiodic
residue-packing target.  It enumerates split complement locators T, applies the
Hankel-pencil gate

    (H(u)+zH(v)) ell_T = 0,

removes contained/tangent-core locators with H(v)ell_T=0, labels whole-fiber
quotient-periodic complements on cyclic multiplicative domains, and reports the
remaining aperiodic slope image.  Every reported bad slope is cross-checked by
direct Reed-Solomon interpolation on the support D \\ T.  A deterministic
arbitrary-line probe exercises the rank-one zero-determinant branch.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations


def inv_mod(x: int, p: int) -> int:
    if x % p == 0:
        raise ZeroDivisionError("zero")
    return pow(x % p, p - 2, p)


def primitive_root(p: int) -> int:
    factors = set()
    value = p - 1
    d = 2
    while d * d <= value:
        if value % d == 0:
            factors.add(d)
            while value % d == 0:
                value //= d
        d += 1
    if value > 1:
        factors.add(value)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in factors):
            return g
    raise AssertionError(f"no primitive root for {p}")


def cyclic_domain(p: int, n: int) -> tuple[tuple[int, ...], dict[int, int], int]:
    if (p - 1) % n:
        raise AssertionError("n must divide p-1")
    gen = pow(primitive_root(p), (p - 1) // n, p)
    domain = tuple(pow(gen, i, p) for i in range(n))
    exponents = {x: i for i, x in enumerate(domain)}
    if len(exponents) != n:
        raise AssertionError("domain generator has wrong order")
    return domain, exponents, gen


def poly_mul(left: list[int], right: list[int], p: int) -> list[int]:
    out = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            out[i + j] = (out[i + j] + x * y) % p
    return trim_mod(out, p)


def trim_mod(poly: list[int], p: int) -> list[int]:
    out = [x % p for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def poly_eval(poly: list[int], x: int, p: int) -> int:
    value = 0
    for coeff in reversed(poly):
        value = (value * x + coeff) % p
    return value


def poly_degree(poly: list[int]) -> int:
    return len(poly) - 1


def interpolate(points: tuple[int, ...], values: tuple[int, ...], p: int) -> list[int]:
    result = [0]
    for i, xi in enumerate(points):
        basis = [1]
        denom = 1
        for j, xj in enumerate(points):
            if i == j:
                continue
            basis = poly_mul(basis, [(-xj) % p, 1], p)
            denom = denom * ((xi - xj) % p) % p
        scale = values[i] * inv_mod(denom, p) % p
        if len(result) < len(basis):
            result.extend([0] * (len(basis) - len(result)))
        for idx, coeff in enumerate(basis):
            result[idx] = (result[idx] + scale * coeff) % p
    return trim_mod(result, p)


def locator(points: tuple[int, ...], p: int) -> list[int]:
    poly = [1]
    for x in points:
        poly = poly_mul(poly, [(-x) % p, 1], p)
    return poly


def lambda_weights(domain: tuple[int, ...], p: int) -> dict[int, int]:
    weights = {}
    for x in domain:
        denom = 1
        for y in domain:
            if x != y:
                denom = denom * ((x - y) % p) % p
        weights[x] = inv_mod(denom, p)
    return weights


def syndrome(values: dict[int, int], domain: tuple[int, ...], r: int, p: int) -> tuple[int, ...]:
    weights = lambda_weights(domain, p)
    out = []
    for m in range(r):
        total = 0
        for x in domain:
            total = (total + weights[x] * pow(x, m, p) * values[x]) % p
        out.append(total)
    return tuple(out)


def hankel_apply(syn: tuple[int, ...], t: int, j: int, ell: list[int], p: int) -> tuple[int, ...]:
    return tuple(
        sum(syn[row + col] * ell[col] for col in range(j + 1)) % p
        for row in range(t)
    )


def slope_from_gate(a_vec: tuple[int, ...], b_vec: tuple[int, ...], p: int) -> int | None:
    if all(x == 0 for x in b_vec):
        return None
    slope = None
    for a, b in zip(a_vec, b_vec):
        if b == 0:
            if a != 0:
                return None
            continue
        candidate = (-a * inv_mod(b, p)) % p
        if slope is None:
            slope = candidate
        elif slope != candidate:
            return None
    return slope


def determinant_gate_t2(a_vec: tuple[int, ...], b_vec: tuple[int, ...], p: int) -> bool:
    if len(a_vec) != 2 or len(b_vec) != 2:
        raise AssertionError("determinant gate is only for t=2")
    return det2(a_vec, b_vec, p) == 0


def det2(left: tuple[int, int], right: tuple[int, int], p: int) -> int:
    return (left[0] * right[1] - left[1] * right[0]) % p


def determinant_value_t2(
    u: tuple[int, ...],
    v: tuple[int, ...],
    complement: tuple[int, ...],
    j: int,
    p: int,
) -> int:
    ell = locator(complement, p)
    a_vec = hankel_apply(u, 2, j, ell, p)
    b_vec = hankel_apply(v, 2, j, ell, p)
    return det2(a_vec, b_vec, p)


def rank_two_vectors(first: tuple[int, int], second: tuple[int, int], p: int) -> int:
    if det2(first, second, p) != 0:
        return 2
    if any(value != 0 for value in first + second):
        return 1
    return 0


def slice_affine_data_t2(
    u: tuple[int, ...],
    v: tuple[int, ...],
    core: tuple[int, ...],
    j: int,
    p: int,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]]:
    core_locator = locator(core, p)
    if len(core_locator) != j:
        raise AssertionError("core locator has wrong degree")
    shift_vec = [0] + core_locator
    pad_vec = core_locator + [0]
    a_shift = hankel_apply(u, 2, j, shift_vec, p)
    a_pad = hankel_apply(u, 2, j, pad_vec, p)
    b_shift = hankel_apply(v, 2, j, shift_vec, p)
    b_pad = hankel_apply(v, 2, j, pad_vec, p)
    return a_shift, a_pad, b_shift, b_pad


def determinant_coefficients_t2(
    u: tuple[int, ...],
    v: tuple[int, ...],
    core: tuple[int, ...],
    j: int,
    p: int,
) -> tuple[int, int, int]:
    a_shift, a_pad, b_shift, b_pad = slice_affine_data_t2(u, v, core, j, p)
    return (
        det2(a_shift, b_shift, p),
        (-det2(a_pad, b_shift, p) - det2(a_shift, b_pad, p)) % p,
        det2(a_pad, b_pad, p),
    )


def quadratic_companion_root(coeffs: tuple[int, int, int], root: int, p: int) -> int | None:
    if poly_eval(list(coeffs), root, p) != 0:
        raise AssertionError("quadratic companion root was not a root")
    if all(coeff == 0 for coeff in coeffs):
        return None
    _, c1, c2 = coeffs
    if c2 == 0:
        return None
    return ((-c1 * inv_mod(c2, p)) - root) % p


def strict_exchange_profile(
    locator_rows: list[tuple[tuple[int, ...], int]], t: int
) -> dict[str, int]:
    strict_pairs = 0
    same_slope_strict_pairs = 0
    degrees = [0] * len(locator_rows)
    slope_fibers: dict[int, int] = {}
    for _, slope in locator_rows:
        slope_fibers[slope] = slope_fibers.get(slope, 0) + 1

    for left in range(len(locator_rows)):
        set_left = set(locator_rows[left][0])
        slope_left = locator_rows[left][1]
        for right in range(left + 1, len(locator_rows)):
            set_right = set(locator_rows[right][0])
            exchange = len(set_left - set_right)
            if exchange != len(set_right - set_left):
                raise AssertionError("equal-size complements should have symmetric exchange")
            if 0 < exchange < t:
                strict_pairs += 1
                degrees[left] += 1
                degrees[right] += 1
                if slope_left == locator_rows[right][1]:
                    same_slope_strict_pairs += 1

    return {
        "strict_pairs": strict_pairs,
        "max_strict_degree": max(degrees, default=0),
        "same_slope_strict_pairs": same_slope_strict_pairs,
        "max_slope_fiber": max(slope_fibers.values(), default=0),
    }


def fixed_slope_incidence(
    u: tuple[int, ...],
    v: tuple[int, ...],
    complement: tuple[int, ...],
    slope: int,
    t: int,
    j: int,
    p: int,
) -> tuple[bool, bool]:
    ell = locator(complement, p)
    a_vec = hankel_apply(u, t, j, ell, p)
    b_vec = hankel_apply(v, t, j, ell, p)
    incident = all((a + slope * b) % p == 0 for a, b in zip(a_vec, b_vec))
    noncontained = any(b != 0 for b in b_vec)
    return incident, noncontained


def root_slice_profile(
    locator_rows: list[tuple[tuple[int, ...], int]],
    domain: tuple[int, ...],
    u: tuple[int, ...],
    v: tuple[int, ...],
    t: int,
    j: int,
    p: int,
) -> dict[str, int]:
    if t != 2:
        slope_fibers: dict[int, int] = {}
        for _, slope in locator_rows:
            slope_fibers[slope] = slope_fibers.get(slope, 0) + 1
        return {
            "root_slices": 0,
            "same_slope_edges_covered": 0,
            "max_root_slice_noncontained": 0,
            "max_root_slice_aperiodic_members": 0,
            "root_slice_slope_count": 0,
            "root_slice_members": 0,
            "root_slice_residual_locators": len(locator_rows),
            "root_slice_residual_slopes": len({slope for _, slope in locator_rows}),
            "root_slice_residual_max_slope_fiber": max(slope_fibers.values(), default=0),
            "root_slice_residual_strict_pairs": 0,
            "root_slice_residual_max_strict_degree": 0,
            "root_slice_residual_same_slope_edges": 0,
            "root_slice_residual_triangles": 0,
            "root_slice_residual_top_triangles": 0,
            "root_slice_residual_star_triangles": 0,
            "root_slice_residual_top_packets": 0,
            "root_slice_residual_large_top_packets": 0,
            "root_slice_residual_pair_top_packets": 0,
            "root_slice_residual_max_top_packet": 0,
            "root_slice_residual_top_packet_edges": 0,
            "root_slice_residual_top_packet_triangles": 0,
            "root_slice_residual_top_packet_degree_sum": 0,
            "root_slice_residual_top_packet_degree_max": 0,
            "root_slice_residual_top_packet_incidence_max": 0,
        }

    row_map = {tuple(sorted(complement)): slope for complement, slope in locator_rows}
    slice_keys: set[tuple[tuple[int, ...], int]] = set()
    same_slope_edges = 0
    for left in range(len(locator_rows)):
        left_set = set(locator_rows[left][0])
        left_slope = locator_rows[left][1]
        for right in range(left + 1, len(locator_rows)):
            right_set = set(locator_rows[right][0])
            if left_slope != locator_rows[right][1]:
                continue
            if len(left_set - right_set) == 1 and len(right_set - left_set) == 1:
                same_slope_edges += 1
                core = tuple(sorted(left_set & right_set))
                if len(core) != j - 1:
                    raise AssertionError("one-exchange core has wrong size")
                slice_keys.add((core, left_slope))

    max_noncontained = 0
    max_aperiodic_members = 0
    root_slice_members: set[tuple[int, ...]] = set()
    for core, slope in slice_keys:
        noncontained_count = 0
        aperiodic_member_count = 0
        for x in domain:
            if x in core:
                continue
            complement = tuple(sorted(core + (x,)))
            incident, noncontained = fixed_slope_incidence(u, v, complement, slope, t, j, p)
            if not incident:
                raise AssertionError("same-slope edge did not extend to full root slice")
            if noncontained:
                noncontained_count += 1
            if row_map.get(complement) == slope:
                aperiodic_member_count += 1
                root_slice_members.add(complement)
        max_noncontained = max(max_noncontained, noncontained_count)
        max_aperiodic_members = max(max_aperiodic_members, aperiodic_member_count)

    residual_rows = [
        (complement, slope)
        for complement, slope in locator_rows
        if tuple(sorted(complement)) not in root_slice_members
    ]
    residual_same_slope_edges = 0
    residual_strict_pairs = 0
    residual_degrees = [0] * len(residual_rows)
    residual_adj = [set() for _ in residual_rows]
    residual_top_packets: dict[tuple[int, ...], set[int]] = {}
    residual_slope_fibers: dict[int, int] = {}
    for _, slope in residual_rows:
        residual_slope_fibers[slope] = residual_slope_fibers.get(slope, 0) + 1
    for left in range(len(residual_rows)):
        left_set = set(residual_rows[left][0])
        left_slope = residual_rows[left][1]
        for right in range(left + 1, len(residual_rows)):
            right_set = set(residual_rows[right][0])
            if len(left_set - right_set) == 1 and len(right_set - left_set) == 1:
                residual_strict_pairs += 1
                residual_degrees[left] += 1
                residual_degrees[right] += 1
                residual_adj[left].add(right)
                residual_adj[right].add(left)
                top_packet = tuple(sorted(left_set | right_set))
                if len(top_packet) != j + 1:
                    raise AssertionError("residual edge had wrong top-packet size")
                residual_top_packets.setdefault(top_packet, set()).update((left, right))
                if left_slope == residual_rows[right][1]:
                    residual_same_slope_edges += 1
    if residual_same_slope_edges:
        raise AssertionError("root-slice peeling left a same-slope strict edge")
    if max(residual_degrees, default=0) > j:
        raise AssertionError("residual one-exchange degree exceeded the t=2 core bound")

    residual_triangles = 0
    residual_top_triangles = 0
    residual_star_triangles = 0
    for left in range(len(residual_rows)):
        for middle in residual_adj[left]:
            if middle <= left:
                continue
            for right in residual_adj[left] & residual_adj[middle]:
                if right <= middle:
                    continue
                residual_triangles += 1
                sets = [set(residual_rows[idx][0]) for idx in (left, middle, right)]
                common = set.intersection(*sets)
                union = set.union(*sets)
                if len(common) == j - 1:
                    residual_star_triangles += 1
                elif len(common) == j - 2 and len(union) == j + 1:
                    residual_top_triangles += 1
                else:
                    raise AssertionError("residual triangle had unknown Johnson type")
    if residual_star_triangles:
        raise AssertionError("root-slice peeling left a star triangle")

    top_packet_edges = 0
    top_packet_triangles = 0
    large_top_packets = 0
    pair_top_packets = 0
    max_top_packet = 0
    top_packet_degrees = [0] * len(residual_rows)
    top_packet_incidences = [0] * len(residual_rows)
    for vertices in residual_top_packets.values():
        size = len(vertices)
        max_top_packet = max(max_top_packet, size)
        top_packet_edges += size * (size - 1) // 2
        top_packet_triangles += size * (size - 1) * (size - 2) // 6
        if size == 2:
            pair_top_packets += 1
        elif size >= 3:
            large_top_packets += 1
        slopes = {residual_rows[idx][1] for idx in vertices}
        if len(slopes) != size:
            raise AssertionError("residual top packet was not slope-injective")
        for idx in vertices:
            top_packet_degrees[idx] += size - 1
            top_packet_incidences[idx] += 1
    if top_packet_edges != residual_strict_pairs:
        raise AssertionError("residual top-packet edge ledger was not exact")
    if top_packet_triangles != residual_top_triangles:
        raise AssertionError("residual top-packet triangle ledger was not exact")
    if top_packet_degrees != residual_degrees:
        raise AssertionError("residual top-packet degree ledger was not exact")

    return {
        "root_slices": len(slice_keys),
        "same_slope_edges_covered": same_slope_edges,
        "max_root_slice_noncontained": max_noncontained,
        "max_root_slice_aperiodic_members": max_aperiodic_members,
        "root_slice_slope_count": len({slope for _, slope in slice_keys}),
        "root_slice_members": len(root_slice_members),
        "root_slice_residual_locators": len(residual_rows),
        "root_slice_residual_slopes": len(residual_slope_fibers),
        "root_slice_residual_max_slope_fiber": max(residual_slope_fibers.values(), default=0),
        "root_slice_residual_strict_pairs": residual_strict_pairs,
        "root_slice_residual_max_strict_degree": max(residual_degrees, default=0),
        "root_slice_residual_same_slope_edges": residual_same_slope_edges,
        "root_slice_residual_triangles": residual_triangles,
        "root_slice_residual_top_triangles": residual_top_triangles,
        "root_slice_residual_star_triangles": residual_star_triangles,
        "root_slice_residual_top_packets": len(residual_top_packets),
        "root_slice_residual_large_top_packets": large_top_packets,
        "root_slice_residual_pair_top_packets": pair_top_packets,
        "root_slice_residual_max_top_packet": max_top_packet,
        "root_slice_residual_top_packet_edges": top_packet_edges,
        "root_slice_residual_top_packet_triangles": top_packet_triangles,
        "root_slice_residual_top_packet_degree_sum": sum(top_packet_degrees),
        "root_slice_residual_top_packet_degree_max": max(top_packet_degrees, default=0),
        "root_slice_residual_top_packet_incidence_max": max(top_packet_incidences, default=0),
    }


def quadratic_slice_profile(
    locator_rows: list[tuple[tuple[int, ...], int]],
    domain: tuple[int, ...],
    u: tuple[int, ...],
    v: tuple[int, ...],
    t: int,
    j: int,
    p: int,
) -> dict[str, int]:
    if t != 2:
        return {
            "different_slope_strict_pairs": 0,
            "different_slope_cores": 0,
            "quadratic_slices_checked": 0,
            "zero_determinant_slices": 0,
            "edge_zero_determinant_slices": 0,
            "zero_det_different_slope_edges": 0,
            "zero_det_constant_slices": 0,
            "zero_det_injective_slices": 0,
            "zero_det_empty_slices": 0,
            "zero_det_direction_rank0_slices": 0,
            "zero_det_direction_rank1_slices": 0,
            "zero_det_direction_rank2_slices": 0,
            "zero_det_aperiodic_repeated_slope_pairs": 0,
            "max_zero_det_slope_image": 0,
            "max_zero_det_aperiodic_members": 0,
            "nonzero_quadratic_edge_slices": 0,
            "quadratic_companion_checks": 0,
            "max_determinant_roots_nonzero": 0,
        }

    row_map = {tuple(sorted(complement)): slope for complement, slope in locator_rows}
    different_slope_edges: dict[tuple[int, ...], list[frozenset[int]]] = {}
    for left in range(len(locator_rows)):
        left_set = set(locator_rows[left][0])
        left_slope = locator_rows[left][1]
        for right in range(left + 1, len(locator_rows)):
            right_set = set(locator_rows[right][0])
            if left_slope == locator_rows[right][1]:
                continue
            if len(left_set - right_set) == 1 and len(right_set - left_set) == 1:
                core = tuple(sorted(left_set & right_set))
                if len(core) != j - 1:
                    raise AssertionError("one-exchange core has wrong size")
                exchanged = frozenset(
                    (next(iter(left_set - right_set)), next(iter(right_set - left_set)))
                )
                different_slope_edges.setdefault(core, []).append(exchanged)

    zero_determinant_slices = 0
    edge_zero_determinant_slices = 0
    zero_det_different_slope_edges = 0
    zero_det_constant_slices = 0
    zero_det_injective_slices = 0
    zero_det_empty_slices = 0
    zero_det_direction_rank0_slices = 0
    zero_det_direction_rank1_slices = 0
    zero_det_direction_rank2_slices = 0
    zero_det_aperiodic_repeated_slope_pairs = 0
    max_zero_det_slope_image = 0
    max_zero_det_aperiodic_members = 0
    nonzero_quadratic_edge_slices = 0
    quadratic_companion_checks = 0
    max_determinant_roots_nonzero = 0
    checked = 0
    domain_set = set(domain)

    for core in combinations(domain, j - 1):
        checked += 1
        core_tuple = tuple(sorted(core))
        _, _, b_shift, b_pad = slice_affine_data_t2(u, v, core_tuple, j, p)
        direction_rank = rank_two_vectors(b_shift, b_pad, p)
        det_coeffs = determinant_coefficients_t2(u, v, core_tuple, j, p)
        det_poly = list(det_coeffs)
        field_roots = {
            x
            for x in range(p)
            if poly_eval(det_poly, x, p) == 0
        }
        for x in range(p):
            complement = tuple(sorted(core_tuple + (x,)))
            if poly_eval(det_poly, x, p) != determinant_value_t2(u, v, complement, j, p):
                raise AssertionError("determinant coefficient certificate failed")

        zero_slice = all(coeff == 0 for coeff in det_coeffs)
        if zero_slice:
            if len(field_roots) != p:
                raise AssertionError("zero determinant slice did not vanish everywhere")
            zero_determinant_slices += 1
            if direction_rank == 0:
                zero_det_direction_rank0_slices += 1
            elif direction_rank == 1:
                zero_det_direction_rank1_slices += 1
            elif direction_rank == 2:
                zero_det_direction_rank2_slices += 1
            else:
                raise AssertionError("unexpected direction rank")

            slope_counts: dict[int, int] = {}
            aperiodic_slope_counts: dict[int, int] = {}
            for x in domain:
                if x in core_tuple:
                    continue
                complement = tuple(sorted(core_tuple + (x,)))
                ell = locator(complement, p)
                a_vec = hankel_apply(u, t, j, ell, p)
                b_vec = hankel_apply(v, t, j, ell, p)
                if all(value == 0 for value in b_vec):
                    continue
                slope = slope_from_gate(a_vec, b_vec, p)
                if slope is None:
                    raise AssertionError("zero determinant noncontained point had no slope")
                slope_counts[slope] = slope_counts.get(slope, 0) + 1
                if complement in row_map:
                    if row_map[complement] != slope:
                        raise AssertionError("aperiodic row slope disagrees on zero slice")
                    aperiodic_slope_counts[slope] = aperiodic_slope_counts.get(slope, 0) + 1

            noncontained_count = sum(slope_counts.values())
            aperiodic_count = sum(aperiodic_slope_counts.values())
            max_zero_det_slope_image = max(max_zero_det_slope_image, len(slope_counts))
            max_zero_det_aperiodic_members = max(max_zero_det_aperiodic_members, aperiodic_count)
            zero_det_aperiodic_repeated_slope_pairs += sum(
                count * (count - 1) // 2 for count in aperiodic_slope_counts.values()
            )
            if noncontained_count == 0:
                if direction_rank != 0:
                    raise AssertionError("nonzero direction slice had no noncontained points")
                zero_det_empty_slices += 1
            elif max(slope_counts.values()) == noncontained_count:
                zero_det_constant_slices += 1
            else:
                raise AssertionError("zero determinant slice was not constant-slope")
        else:
            if len(field_roots) > 2:
                raise AssertionError("nonzero determinant slice has more than two roots")
            max_determinant_roots_nonzero = max(max_determinant_roots_nonzero, len(field_roots))

        edge_roots = different_slope_edges.get(core_tuple, [])
        if not edge_roots:
            continue
        if zero_slice:
            edge_zero_determinant_slices += 1
            zero_det_different_slope_edges += len(edge_roots)
            continue

        domain_roots = field_roots & domain_set
        if len(domain_roots) != 2:
            raise AssertionError("different-slope edge did not exhaust nonzero quadratic roots")
        for exchanged in edge_roots:
            if exchanged != domain_roots:
                raise AssertionError("different-slope edge is not the quadratic root set")
            left, right = tuple(exchanged)
            if quadratic_companion_root(det_coeffs, left, p) != right:
                raise AssertionError("left exchanged root did not map to its companion")
            if quadratic_companion_root(det_coeffs, right, p) != left:
                raise AssertionError("right exchanged root did not map to its companion")
            quadratic_companion_checks += 2
        nonzero_quadratic_edge_slices += 1

    return {
        "different_slope_strict_pairs": sum(len(edges) for edges in different_slope_edges.values()),
        "different_slope_cores": len(different_slope_edges),
        "quadratic_slices_checked": checked,
        "zero_determinant_slices": zero_determinant_slices,
        "edge_zero_determinant_slices": edge_zero_determinant_slices,
        "zero_det_different_slope_edges": zero_det_different_slope_edges,
        "zero_det_constant_slices": zero_det_constant_slices,
        "zero_det_injective_slices": zero_det_injective_slices,
        "zero_det_empty_slices": zero_det_empty_slices,
        "zero_det_direction_rank0_slices": zero_det_direction_rank0_slices,
        "zero_det_direction_rank1_slices": zero_det_direction_rank1_slices,
        "zero_det_direction_rank2_slices": zero_det_direction_rank2_slices,
        "zero_det_aperiodic_repeated_slope_pairs": zero_det_aperiodic_repeated_slope_pairs,
        "max_zero_det_slope_image": max_zero_det_slope_image,
        "max_zero_det_aperiodic_members": max_zero_det_aperiodic_members,
        "nonzero_quadratic_edge_slices": nonzero_quadratic_edge_slices,
        "quadratic_companion_checks": quadratic_companion_checks,
        "max_determinant_roots_nonzero": max_determinant_roots_nonzero,
    }


def word_value(kind: str, x: int, p: int, seed: int) -> int:
    if kind == "f":
        return (
            (seed + 1) * pow(x, 13, p)
            + (2 * seed + 3) * pow(x, 7, p)
            + (seed + 5) * x
            + 4
        ) % p
    if kind == "g":
        return (
            (seed + 2) * pow(x, 14, p)
            + (3 * seed + 1) * pow(x, 11, p)
            + (seed + 6) * pow(x, 3, p)
            + 1
        ) % p
    raise AssertionError(kind)


def is_explained_on_support(
    word: dict[int, int], support: tuple[int, ...], k: int, p: int
) -> bool:
    seed = support[:k]
    poly = interpolate(seed, tuple(word[x] for x in seed), p)
    if poly_degree(poly) >= k:
        raise AssertionError("interpolant degree should be < k")
    return all(poly_eval(poly, x, p) == word[x] for x in support)


def is_quotient_periodic(
    complement: tuple[int, ...],
    domain: tuple[int, ...],
    exponents: dict[int, int],
    charged_fiber_sizes: tuple[int, ...],
) -> bool:
    n = len(domain)
    comp = set(complement)
    for m in charged_fiber_sizes:
        if m <= 1 or m >= n or n % m or len(comp) % m:
            continue
        quotient_size = n // m
        ok = True
        for residue in range(quotient_size):
            fiber = {
                x for x in domain
                if exponents[x] % quotient_size == residue
            }
            if bool(fiber & comp) and not fiber <= comp:
                ok = False
                break
        if ok:
            return True
    return False


@dataclass(frozen=True)
class Case:
    name: str
    p: int
    n: int
    j: int
    t: int
    charged_fiber_sizes: tuple[int, ...]
    seeds: tuple[int, ...]


def verify_word_pair(
    case: Case,
    seed: object,
    f: dict[int, int],
    g: dict[int, int],
) -> dict[str, object]:
    p, n, j, t = case.p, case.n, case.j, case.t
    k = n - j - t
    if k <= 0:
        raise AssertionError("invalid k")
    domain, exponents, _ = cyclic_domain(p, n)
    if set(f) != set(domain) or set(g) != set(domain):
        raise AssertionError("word pair is not defined on the cyclic domain")
    u = syndrome(f, domain, j + t, p)
    v = syndrome(g, domain, j + t, p)

    bad_slopes: set[int] = set()
    quotient_slopes: set[int] = set()
    aperiodic_slopes: set[int] = set()
    bad_locators = 0
    quotient_locators = 0
    aperiodic_locators = 0
    contained_core = 0
    direct_checks = 0
    determinant_checks = 0
    aperiodic_locator_rows: list[tuple[tuple[int, ...], int]] = []

    for complement in combinations(domain, j):
        ell = locator(complement, p)
        a_vec = hankel_apply(u, t, j, ell, p)
        b_vec = hankel_apply(v, t, j, ell, p)
        if all(x == 0 for x in b_vec):
            contained_core += 1
            continue
        slope = slope_from_gate(a_vec, b_vec, p)
        if t == 2:
            determinant_ok = determinant_gate_t2(a_vec, b_vec, p)
            if determinant_ok != (slope is not None):
                raise AssertionError("t=2 determinant gate disagrees with projective slope gate")
            determinant_checks += 1
        if slope is None:
            continue

        support = tuple(x for x in domain if x not in set(complement))
        line_word = {x: (f[x] + slope * g[x]) % p for x in domain}
        if not is_explained_on_support(line_word, support, k, p):
            raise AssertionError("Hankel bad slope failed direct RS check")
        if is_explained_on_support(g, support, k, p):
            raise AssertionError("noncontained Hankel slope was contained")
        direct_checks += 1

        bad_locators += 1
        bad_slopes.add(slope)
        if is_quotient_periodic(complement, domain, exponents, case.charged_fiber_sizes):
            quotient_locators += 1
            quotient_slopes.add(slope)
        else:
            aperiodic_locators += 1
            aperiodic_slopes.add(slope)
            aperiodic_locator_rows.append((complement, slope))

    if not aperiodic_slopes <= bad_slopes:
        raise AssertionError("aperiodic slopes escaped bad slope set")
    if not quotient_slopes <= bad_slopes:
        raise AssertionError("quotient slopes escaped bad slope set")
    if bad_locators != quotient_locators + aperiodic_locators:
        raise AssertionError("charged/aperiodic locator partition failed")
    exchange_profile = strict_exchange_profile(aperiodic_locator_rows, t)
    root_profile = root_slice_profile(aperiodic_locator_rows, domain, u, v, t, j, p)
    if root_profile["same_slope_edges_covered"] != exchange_profile["same_slope_strict_pairs"]:
        raise AssertionError("root-slice coverage missed same-slope strict edges")
    quadratic_profile = quadratic_slice_profile(aperiodic_locator_rows, domain, u, v, t, j, p)
    expected_different_slope = (
        exchange_profile["strict_pairs"] - exchange_profile["same_slope_strict_pairs"]
    )
    if quadratic_profile["different_slope_strict_pairs"] != expected_different_slope:
        raise AssertionError("quadratic-slice profile missed different-slope strict edges")
    if (
        quadratic_profile["zero_det_aperiodic_repeated_slope_pairs"]
        != exchange_profile["same_slope_strict_pairs"]
    ):
        raise AssertionError("zero determinant slices did not explain same-slope strict edges")

    return {
        "name": case.name,
        "seed": seed,
        "p": p,
        "n": n,
        "k": k,
        "j": j,
        "t": t,
        "q_line": p,
        "charged_fiber_sizes": case.charged_fiber_sizes,
        "split_locators": sum(1 for _ in combinations(domain, j)),
        "contained_core_locators": contained_core,
        "bad_locators": bad_locators,
        "bad_slopes": len(bad_slopes),
        "quotient_locators": quotient_locators,
        "quotient_slopes": len(quotient_slopes),
        "aperiodic_locators": aperiodic_locators,
        "aperiodic_slopes": len(aperiodic_slopes),
        "aperiodic_max_slope_fiber": exchange_profile["max_slope_fiber"],
        "aperiodic_strict_pairs": exchange_profile["strict_pairs"],
        "aperiodic_max_strict_degree": exchange_profile["max_strict_degree"],
        "aperiodic_same_slope_strict_pairs": exchange_profile["same_slope_strict_pairs"],
        "root_slices": root_profile["root_slices"],
        "same_slope_edges_covered": root_profile["same_slope_edges_covered"],
        "max_root_slice_noncontained": root_profile["max_root_slice_noncontained"],
        "max_root_slice_aperiodic_members": root_profile["max_root_slice_aperiodic_members"],
        "root_slice_slope_count": root_profile["root_slice_slope_count"],
        "root_slice_members": root_profile["root_slice_members"],
        "root_slice_residual_locators": root_profile["root_slice_residual_locators"],
        "root_slice_residual_slopes": root_profile["root_slice_residual_slopes"],
        "root_slice_residual_max_slope_fiber": (
            root_profile["root_slice_residual_max_slope_fiber"]
        ),
        "root_slice_residual_strict_pairs": root_profile["root_slice_residual_strict_pairs"],
        "root_slice_residual_max_strict_degree": (
            root_profile["root_slice_residual_max_strict_degree"]
        ),
        "root_slice_residual_same_slope_edges": (
            root_profile["root_slice_residual_same_slope_edges"]
        ),
        "root_slice_residual_triangles": root_profile["root_slice_residual_triangles"],
        "root_slice_residual_top_triangles": root_profile["root_slice_residual_top_triangles"],
        "root_slice_residual_star_triangles": root_profile["root_slice_residual_star_triangles"],
        "root_slice_residual_top_packets": root_profile["root_slice_residual_top_packets"],
        "root_slice_residual_large_top_packets": root_profile["root_slice_residual_large_top_packets"],
        "root_slice_residual_pair_top_packets": root_profile["root_slice_residual_pair_top_packets"],
        "root_slice_residual_max_top_packet": root_profile["root_slice_residual_max_top_packet"],
        "root_slice_residual_top_packet_edges": root_profile["root_slice_residual_top_packet_edges"],
        "root_slice_residual_top_packet_triangles": (
            root_profile["root_slice_residual_top_packet_triangles"]
        ),
        "root_slice_residual_top_packet_degree_sum": (
            root_profile["root_slice_residual_top_packet_degree_sum"]
        ),
        "root_slice_residual_top_packet_degree_max": (
            root_profile["root_slice_residual_top_packet_degree_max"]
        ),
        "root_slice_residual_top_packet_incidence_max": (
            root_profile["root_slice_residual_top_packet_incidence_max"]
        ),
        "different_slope_strict_pairs": quadratic_profile["different_slope_strict_pairs"],
        "different_slope_cores": quadratic_profile["different_slope_cores"],
        "quadratic_slices_checked": quadratic_profile["quadratic_slices_checked"],
        "zero_determinant_slices": quadratic_profile["zero_determinant_slices"],
        "edge_zero_determinant_slices": quadratic_profile["edge_zero_determinant_slices"],
        "zero_det_different_slope_edges": quadratic_profile["zero_det_different_slope_edges"],
        "zero_det_constant_slices": quadratic_profile["zero_det_constant_slices"],
        "zero_det_injective_slices": quadratic_profile["zero_det_injective_slices"],
        "zero_det_empty_slices": quadratic_profile["zero_det_empty_slices"],
        "zero_det_direction_rank0_slices": quadratic_profile["zero_det_direction_rank0_slices"],
        "zero_det_direction_rank1_slices": quadratic_profile["zero_det_direction_rank1_slices"],
        "zero_det_direction_rank2_slices": quadratic_profile["zero_det_direction_rank2_slices"],
        "zero_det_aperiodic_repeated_slope_pairs": (
            quadratic_profile["zero_det_aperiodic_repeated_slope_pairs"]
        ),
        "max_zero_det_slope_image": quadratic_profile["max_zero_det_slope_image"],
        "max_zero_det_aperiodic_members": quadratic_profile["max_zero_det_aperiodic_members"],
        "nonzero_quadratic_edge_slices": quadratic_profile["nonzero_quadratic_edge_slices"],
        "quadratic_companion_checks": quadratic_profile["quadratic_companion_checks"],
        "max_determinant_roots_nonzero": quadratic_profile["max_determinant_roots_nonzero"],
        "determinant_checks": determinant_checks,
        "direct_checks": direct_checks,
    }


def verify_case_seed(case: Case, seed: int) -> dict[str, object]:
    domain, _, _ = cyclic_domain(case.p, case.n)
    f = {x: word_value("f", x, case.p, seed) for x in domain}
    g = {x: word_value("g", x, case.p, seed) for x in domain}
    return verify_word_pair(case, seed, f, g)


def verify_case(case: Case) -> dict[str, object]:
    rows = [verify_case_seed(case, seed) for seed in case.seeds]
    return {
        "case": case,
        "rows": rows,
        "max_bad_slopes": max(row["bad_slopes"] for row in rows),
        "max_quotient_slopes": max(row["quotient_slopes"] for row in rows),
        "max_aperiodic_slopes": max(row["aperiodic_slopes"] for row in rows),
        "max_aperiodic_slope_fiber": max(row["aperiodic_max_slope_fiber"] for row in rows),
        "max_aperiodic_strict_pairs": max(row["aperiodic_strict_pairs"] for row in rows),
        "max_aperiodic_strict_degree": max(row["aperiodic_max_strict_degree"] for row in rows),
        "max_root_slices": max(row["root_slices"] for row in rows),
        "max_root_slice_noncontained": max(row["max_root_slice_noncontained"] for row in rows),
        "max_root_slice_members": max(row["root_slice_members"] for row in rows),
        "max_root_slice_residual_locators": max(row["root_slice_residual_locators"] for row in rows),
        "max_root_slice_residual_slopes": max(row["root_slice_residual_slopes"] for row in rows),
        "max_root_slice_residual_slope_fiber": max(
            row["root_slice_residual_max_slope_fiber"] for row in rows
        ),
        "max_root_slice_residual_strict_pairs": max(
            row["root_slice_residual_strict_pairs"] for row in rows
        ),
        "max_root_slice_residual_strict_degree": max(
            row["root_slice_residual_max_strict_degree"] for row in rows
        ),
        "max_root_slice_residual_triangles": max(
            row["root_slice_residual_triangles"] for row in rows
        ),
        "max_root_slice_residual_top_triangles": max(
            row["root_slice_residual_top_triangles"] for row in rows
        ),
        "max_root_slice_residual_star_triangles": max(
            row["root_slice_residual_star_triangles"] for row in rows
        ),
        "max_root_slice_residual_top_packets": max(
            row["root_slice_residual_top_packets"] for row in rows
        ),
        "max_root_slice_residual_large_top_packets": max(
            row["root_slice_residual_large_top_packets"] for row in rows
        ),
        "max_root_slice_residual_pair_top_packets": max(
            row["root_slice_residual_pair_top_packets"] for row in rows
        ),
        "max_root_slice_residual_top_packet_size": max(
            row["root_slice_residual_max_top_packet"] for row in rows
        ),
        "max_root_slice_residual_top_packet_edges": max(
            row["root_slice_residual_top_packet_edges"] for row in rows
        ),
        "max_root_slice_residual_top_packet_triangles": max(
            row["root_slice_residual_top_packet_triangles"] for row in rows
        ),
        "max_root_slice_residual_top_packet_degree_sum": max(
            row["root_slice_residual_top_packet_degree_sum"] for row in rows
        ),
        "max_root_slice_residual_top_packet_degree": max(
            row["root_slice_residual_top_packet_degree_max"] for row in rows
        ),
        "max_root_slice_residual_top_packet_incidence": max(
            row["root_slice_residual_top_packet_incidence_max"] for row in rows
        ),
        "max_different_slope_strict_pairs": max(row["different_slope_strict_pairs"] for row in rows),
        "max_zero_determinant_slices": max(row["zero_determinant_slices"] for row in rows),
        "max_edge_zero_determinant_slices": max(row["edge_zero_determinant_slices"] for row in rows),
        "max_zero_det_different_slope_edges": max(row["zero_det_different_slope_edges"] for row in rows),
        "max_zero_det_constant_slices": max(row["zero_det_constant_slices"] for row in rows),
        "max_zero_det_injective_slices": max(row["zero_det_injective_slices"] for row in rows),
        "max_zero_det_direction_rank0_slices": max(
            row["zero_det_direction_rank0_slices"] for row in rows
        ),
        "max_zero_det_direction_rank1_slices": max(
            row["zero_det_direction_rank1_slices"] for row in rows
        ),
        "max_zero_det_direction_rank2_slices": max(
            row["zero_det_direction_rank2_slices"] for row in rows
        ),
        "max_zero_det_aperiodic_members": max(row["max_zero_det_aperiodic_members"] for row in rows),
        "max_nonzero_quadratic_edge_slices": max(row["nonzero_quadratic_edge_slices"] for row in rows),
        "max_quadratic_companion_checks": max(row["quadratic_companion_checks"] for row in rows),
        "max_determinant_roots_nonzero": max(row["max_determinant_roots_nonzero"] for row in rows),
        "total_direct_checks": sum(row["direct_checks"] for row in rows),
    }


def verify_rank_one_zero_slice_probe() -> dict[str, object]:
    case = Case(
        "F17_full_j4_t2_rank1_probe",
        p=17,
        n=16,
        j=4,
        t=2,
        charged_fiber_sizes=(2, 4, 8),
        seeds=(),
    )
    domain, _, _ = cyclic_domain(case.p, case.n)
    f_values = (5, 15, 0, 16, 8, 10, 8, 10, 3, 6, 15, 11, 7, 2, 10, 0)
    g_values = (7, 14, 9, 12, 5, 14, 7, 2, 10, 9, 10, 4, 9, 6, 8, 4)
    f = dict(zip(domain, f_values, strict=True))
    g = dict(zip(domain, g_values, strict=True))
    row = verify_word_pair(case, "rank1-probe", f, g)
    if row["zero_det_direction_rank1_slices"] < 1:
        raise AssertionError("rank-one zero-slice probe did not hit rank one")
    if row["zero_det_injective_slices"] != 0:
        raise AssertionError("rank-one probe unexpectedly produced an injective zero slice")
    return row


def main() -> None:
    cases = (
        Case("F17_full_j4_t2", p=17, n=16, j=4, t=2, charged_fiber_sizes=(2, 4, 8), seeds=(0, 1, 2, 3)),
        Case("F17_order8_j3_t2", p=17, n=8, j=3, t=2, charged_fiber_sizes=(2, 4), seeds=(0, 1, 2, 3)),
        Case("F13_order12_j4_t2", p=13, n=12, j=4, t=2, charged_fiber_sizes=(2, 3, 4, 6), seeds=(0, 1, 2, 3)),
    )
    summaries = [verify_case(case) for case in cases]
    rank_one_probe = verify_rank_one_zero_slice_probe()
    for summary in summaries:
        case = summary["case"]
        for row in summary["rows"]:
            print(
                "{name} seed={seed}: p={p} n={n} k={k} j={j} t={t} "
                "split={split_locators} bad_locators={bad_locators} "
                "bad_slopes={bad_slopes} quotient_locators={quotient_locators} "
                "quotient_slopes={quotient_slopes} aperiodic_locators={aperiodic_locators} "
                "aperiodic_slopes={aperiodic_slopes} contained_core={contained_core_locators} "
                "aperiodic_fiber_max={aperiodic_max_slope_fiber} "
                "strict_pairs={aperiodic_strict_pairs} "
                "strict_degree_max={aperiodic_max_strict_degree} "
                "same_slope_strict={aperiodic_same_slope_strict_pairs} "
                "root_slices={root_slices} "
                "root_slice_slopes={root_slice_slope_count} "
                "root_slice_members={root_slice_members} "
                "root_slice_noncontained_max={max_root_slice_noncontained} "
                "root_slice_aperiodic_max={max_root_slice_aperiodic_members} "
                "root_residual_locators={root_slice_residual_locators} "
                "root_residual_slopes={root_slice_residual_slopes} "
                "root_residual_fiber_max={root_slice_residual_max_slope_fiber} "
                "root_residual_strict={root_slice_residual_strict_pairs} "
                "root_residual_degree_max={root_slice_residual_max_strict_degree} "
                "root_residual_same_slope={root_slice_residual_same_slope_edges} "
                "root_residual_triangles={root_slice_residual_triangles} "
                "root_residual_top_triangles={root_slice_residual_top_triangles} "
                "root_residual_star_triangles={root_slice_residual_star_triangles} "
                "root_residual_top_packets={root_slice_residual_top_packets} "
                "root_residual_large_top_packets={root_slice_residual_large_top_packets} "
                "root_residual_pair_top_packets={root_slice_residual_pair_top_packets} "
                "root_residual_top_packet_max={root_slice_residual_max_top_packet} "
                "root_residual_top_packet_edges={root_slice_residual_top_packet_edges} "
                "root_residual_top_packet_triangles={root_slice_residual_top_packet_triangles} "
                "root_residual_top_packet_degree_sum={root_slice_residual_top_packet_degree_sum} "
                "root_residual_top_packet_degree_max={root_slice_residual_top_packet_degree_max} "
                "root_residual_top_packet_incidence_max={root_slice_residual_top_packet_incidence_max} "
                "different_slope_strict={different_slope_strict_pairs} "
                "different_slope_cores={different_slope_cores} "
                "quadratic_slices={quadratic_slices_checked} "
                "zero_det_slices={zero_determinant_slices} "
                "edge_zero_det_slices={edge_zero_determinant_slices} "
                "zero_det_diff_edges={zero_det_different_slope_edges} "
                "zero_det_constant={zero_det_constant_slices} "
                "zero_det_injective={zero_det_injective_slices} "
                "zero_det_rank0={zero_det_direction_rank0_slices} "
                "zero_det_rank1={zero_det_direction_rank1_slices} "
                "zero_det_rank2={zero_det_direction_rank2_slices} "
                "zero_det_aperiodic_max={max_zero_det_aperiodic_members} "
                "zero_det_slope_image_max={max_zero_det_slope_image} "
                "zero_det_repeated_pairs={zero_det_aperiodic_repeated_slope_pairs} "
                "nonzero_quad_edge_slices={nonzero_quadratic_edge_slices} "
                "quad_companion_checks={quadratic_companion_checks} "
                "max_nonzero_det_roots={max_determinant_roots_nonzero} "
                "det_checks={determinant_checks} direct_checks={direct_checks}".format(**row)
            )
        print(
            f"{case.name}: seeds={len(case.seeds)} "
            f"max_bad_slopes={summary['max_bad_slopes']} "
            f"max_quotient_slopes={summary['max_quotient_slopes']} "
            f"max_aperiodic_slopes={summary['max_aperiodic_slopes']} "
            f"max_aperiodic_fiber={summary['max_aperiodic_slope_fiber']} "
            f"max_strict_pairs={summary['max_aperiodic_strict_pairs']} "
            f"max_strict_degree={summary['max_aperiodic_strict_degree']} "
            f"max_root_slices={summary['max_root_slices']} "
            f"max_root_slice_noncontained={summary['max_root_slice_noncontained']} "
            f"max_root_slice_members={summary['max_root_slice_members']} "
            f"max_root_residual_locators={summary['max_root_slice_residual_locators']} "
            f"max_root_residual_slopes={summary['max_root_slice_residual_slopes']} "
            f"max_root_residual_fiber={summary['max_root_slice_residual_slope_fiber']} "
            f"max_root_residual_strict={summary['max_root_slice_residual_strict_pairs']} "
            f"max_root_residual_degree={summary['max_root_slice_residual_strict_degree']} "
            f"max_root_residual_triangles={summary['max_root_slice_residual_triangles']} "
            f"max_root_residual_top_triangles={summary['max_root_slice_residual_top_triangles']} "
            f"max_root_residual_star_triangles={summary['max_root_slice_residual_star_triangles']} "
            f"max_root_residual_top_packets={summary['max_root_slice_residual_top_packets']} "
            f"max_root_residual_large_top_packets={summary['max_root_slice_residual_large_top_packets']} "
            f"max_root_residual_pair_top_packets={summary['max_root_slice_residual_pair_top_packets']} "
            f"max_root_residual_top_packet_size={summary['max_root_slice_residual_top_packet_size']} "
            f"max_root_residual_top_packet_edges={summary['max_root_slice_residual_top_packet_edges']} "
            f"max_root_residual_top_packet_triangles={summary['max_root_slice_residual_top_packet_triangles']} "
            f"max_root_residual_top_packet_degree_sum={summary['max_root_slice_residual_top_packet_degree_sum']} "
            f"max_root_residual_top_packet_degree={summary['max_root_slice_residual_top_packet_degree']} "
            f"max_root_residual_top_packet_incidence={summary['max_root_slice_residual_top_packet_incidence']} "
            f"max_different_slope_strict={summary['max_different_slope_strict_pairs']} "
            f"max_zero_det_slices={summary['max_zero_determinant_slices']} "
            f"max_edge_zero_det_slices={summary['max_edge_zero_determinant_slices']} "
            f"max_zero_det_diff_edges={summary['max_zero_det_different_slope_edges']} "
            f"max_zero_det_constant={summary['max_zero_det_constant_slices']} "
            f"max_zero_det_injective={summary['max_zero_det_injective_slices']} "
            f"max_zero_det_rank0={summary['max_zero_det_direction_rank0_slices']} "
            f"max_zero_det_rank1={summary['max_zero_det_direction_rank1_slices']} "
            f"max_zero_det_rank2={summary['max_zero_det_direction_rank2_slices']} "
            f"max_zero_det_aperiodic={summary['max_zero_det_aperiodic_members']} "
            f"max_nonzero_quad_edge_slices={summary['max_nonzero_quadratic_edge_slices']} "
            f"max_quad_companion_checks={summary['max_quadratic_companion_checks']} "
            f"max_nonzero_det_roots={summary['max_determinant_roots_nonzero']} "
            f"direct_checks={summary['total_direct_checks']}"
        )
    print(
        "{name} seed={seed}: p={p} n={n} k={k} j={j} t={t} "
        "aperiodic_locators={aperiodic_locators} aperiodic_slopes={aperiodic_slopes} "
        "zero_det_slices={zero_determinant_slices} "
        "zero_det_rank1={zero_det_direction_rank1_slices} "
        "zero_det_constant={zero_det_constant_slices} "
        "zero_det_injective={zero_det_injective_slices} "
        "root_residual_degree_max={root_slice_residual_max_strict_degree} "
        "root_residual_same_slope={root_slice_residual_same_slope_edges} "
        "root_residual_triangles={root_slice_residual_triangles} "
        "root_residual_top_triangles={root_slice_residual_top_triangles} "
        "root_residual_star_triangles={root_slice_residual_star_triangles} "
        "root_residual_top_packets={root_slice_residual_top_packets} "
        "root_residual_large_top_packets={root_slice_residual_large_top_packets} "
        "root_residual_pair_top_packets={root_slice_residual_pair_top_packets} "
        "root_residual_top_packet_max={root_slice_residual_max_top_packet} "
        "root_residual_top_packet_edges={root_slice_residual_top_packet_edges} "
        "root_residual_top_packet_triangles={root_slice_residual_top_packet_triangles} "
        "root_residual_top_packet_degree_sum={root_slice_residual_top_packet_degree_sum} "
        "root_residual_top_packet_degree_max={root_slice_residual_top_packet_degree_max} "
        "root_residual_top_packet_incidence_max={root_slice_residual_top_packet_incidence_max} "
        "quad_companion_checks={quadratic_companion_checks} "
        "direct_checks={direct_checks}".format(**rank_one_probe)
    )
    all_rows = [row for summary in summaries for row in summary["rows"]] + [rank_one_probe]
    max_aperiodic = max(row["aperiodic_slopes"] for row in all_rows)
    max_strict_degree = max(row["aperiodic_max_strict_degree"] for row in all_rows)
    max_residual_degree = max(row["root_slice_residual_max_strict_degree"] for row in all_rows)
    max_residual_triangles = max(row["root_slice_residual_triangles"] for row in all_rows)
    max_residual_top_triangles = max(row["root_slice_residual_top_triangles"] for row in all_rows)
    max_residual_star_triangles = max(row["root_slice_residual_star_triangles"] for row in all_rows)
    max_residual_top_packets = max(row["root_slice_residual_top_packets"] for row in all_rows)
    max_residual_large_top_packets = max(
        row["root_slice_residual_large_top_packets"] for row in all_rows
    )
    max_residual_pair_top_packets = max(
        row["root_slice_residual_pair_top_packets"] for row in all_rows
    )
    max_residual_top_packet = max(row["root_slice_residual_max_top_packet"] for row in all_rows)
    max_residual_top_packet_edges = max(
        row["root_slice_residual_top_packet_edges"] for row in all_rows
    )
    max_residual_top_packet_triangles = max(
        row["root_slice_residual_top_packet_triangles"] for row in all_rows
    )
    max_residual_top_packet_degree_sum = max(
        row["root_slice_residual_top_packet_degree_sum"] for row in all_rows
    )
    max_residual_top_packet_degree = max(
        row["root_slice_residual_top_packet_degree_max"] for row in all_rows
    )
    max_residual_top_packet_incidence = max(
        row["root_slice_residual_top_packet_incidence_max"] for row in all_rows
    )
    max_companion_checks = max(row["quadratic_companion_checks"] for row in all_rows)
    max_rank_one_zero = max(row["zero_det_direction_rank1_slices"] for row in all_rows)
    total_lines = sum(len(summary["case"].seeds) for summary in summaries) + 1
    print(
        "m1_all_line_hankel_aperiodic: PASS "
        f"cases={len(summaries)} line_samples={total_lines} "
        f"rank_one_probes=1 "
        f"max_aperiodic_slopes={max_aperiodic} "
        f"max_strict_degree={max_strict_degree} "
        f"max_root_residual_degree={max_residual_degree} "
        f"max_root_residual_triangles={max_residual_triangles} "
        f"max_root_residual_top_triangles={max_residual_top_triangles} "
        f"max_root_residual_star_triangles={max_residual_star_triangles} "
        f"max_root_residual_top_packets={max_residual_top_packets} "
        f"max_root_residual_large_top_packets={max_residual_large_top_packets} "
        f"max_root_residual_pair_top_packets={max_residual_pair_top_packets} "
        f"max_root_residual_top_packet_size={max_residual_top_packet} "
        f"max_root_residual_top_packet_edges={max_residual_top_packet_edges} "
        f"max_root_residual_top_packet_triangles={max_residual_top_packet_triangles} "
        f"max_root_residual_top_packet_degree_sum={max_residual_top_packet_degree_sum} "
        f"max_root_residual_top_packet_degree={max_residual_top_packet_degree} "
        f"max_root_residual_top_packet_incidence={max_residual_top_packet_incidence} "
        f"max_quad_companion_checks={max_companion_checks} "
        f"max_rank_one_zero_slices={max_rank_one_zero}"
    )


if __name__ == "__main__":
    main()
