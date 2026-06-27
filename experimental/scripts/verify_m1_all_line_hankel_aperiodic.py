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
from itertools import combinations, product as cartesian_product
from math import comb, factorial


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


def coeff_at(poly: list[int], degree: int) -> int:
    return poly[degree] if degree < len(poly) else 0


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


def coord_det(
    left: tuple[int, ...], right: tuple[int, ...], row: int, col: int, p: int
) -> int:
    return (left[row] * right[col] - left[col] * right[row]) % p


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


def normalize_projective_vector(vector: list[int], p: int) -> tuple[int, ...]:
    for value in vector:
        if value % p != 0:
            scale = inv_mod(value, p)
            return tuple((entry * scale) % p for entry in vector)
    raise AssertionError("projective vector vanished")


def rref_rows(rows: list[tuple[int, ...]], p: int) -> tuple[list[list[int]], list[int]]:
    matrix = [[entry % p for entry in row] for row in rows]
    if not matrix:
        return [], []
    row_count = len(matrix)
    col_count = len(matrix[0])
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        pivot = None
        for row in range(pivot_row, row_count):
            if matrix[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = inv_mod(matrix[pivot_row][col], p)
        matrix[pivot_row] = [(entry * scale) % p for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or matrix[row][col] == 0:
                continue
            factor = matrix[row][col]
            matrix[row] = [
                (matrix[row][idx] - factor * matrix[pivot_row][idx]) % p
                for idx in range(col_count)
            ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return matrix[:pivot_row], pivot_cols


def vector_span_rank(vectors: list[tuple[int, ...]], p: int) -> int:
    if not vectors:
        return 0
    _, pivot_cols = rref_rows(vectors, p)
    return len(pivot_cols)


def nullspace_basis(rows: list[tuple[int, ...]], p: int) -> list[tuple[int, ...]]:
    if not rows:
        raise AssertionError("nullspace rows must have a known width")
    width = len(rows[0])
    rref, pivot_cols = rref_rows(rows, p)
    pivot_set = set(pivot_cols)
    basis: list[tuple[int, ...]] = []
    for free_col in range(width):
        if free_col in pivot_set:
            continue
        vector = [0] * width
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = (-rref[row][free_col]) % p
        basis.append(tuple(vector))
    return basis


def rowspace_key(rows: list[tuple[int, ...]], p: int) -> tuple[tuple[int, ...], ...]:
    rref, _ = rref_rows(rows, p)
    return tuple(tuple(row) for row in rref)


def projective_space_size(vector_dimension: int, p: int) -> int:
    if vector_dimension <= 0:
        return 0
    return (p**vector_dimension - 1) // (p - 1)


def projective_linear_ratio_image_bound(vector_dimension: int, p: int) -> int:
    if vector_dimension <= 0:
        return 0
    if vector_dimension == 1:
        return 1
    return p + 1


def fixed_anchor_root_hyperplane_weights(
    kernel_basis: list[tuple[int, ...]], domain: tuple[int, ...], p: int
) -> tuple[int, dict[tuple[int, ...], int]]:
    fixed_roots = 0
    root_hyperplane_weights: dict[tuple[int, ...], int] = {}
    for x in domain:
        root_hyperplane = tuple(poly_eval(list(vector), x, p) for vector in kernel_basis)
        if all(value == 0 for value in root_hyperplane):
            fixed_roots += 1
            continue
        root_hyperplane_key = normalize_projective_vector(list(root_hyperplane), p)
        root_hyperplane_weights[root_hyperplane_key] = (
            root_hyperplane_weights.get(root_hyperplane_key, 0) + 1
        )
    return fixed_roots, root_hyperplane_weights


def fixed_anchor_rank_stratified_bound(
    root_hyperplane_weights: dict[tuple[int, ...], int],
    dimension: int,
    richness_deficit: int,
    p: int,
    *,
    slope_image: bool = False,
) -> int:
    root_hyperplane_keys = tuple(root_hyperplane_weights)
    bound = 0
    for rank in range(1, dimension):
        heavy_flat_keys: set[tuple[tuple[int, ...], ...]] = set()
        for root_hyperplanes in combinations(root_hyperplane_keys, rank):
            flat_key = rowspace_key(list(root_hyperplanes), p)
            if len(flat_key) != rank:
                continue
            flat_weight = sum(
                weight
                for root_hyperplane_key, weight in root_hyperplane_weights.items()
                if rowspace_key([*flat_key, root_hyperplane_key], p) == flat_key
            )
            if flat_weight >= richness_deficit:
                heavy_flat_keys.add(flat_key)
        flat_dimension = dimension - rank
        if slope_image:
            bound += len(heavy_flat_keys) * projective_linear_ratio_image_bound(
                flat_dimension, p
            )
        else:
            bound += len(heavy_flat_keys) * projective_space_size(flat_dimension, p)
    return bound


def boundary_arrangement_profile(
    kernel_basis: list[tuple[int, ...]],
    root_domain: tuple[int, ...],
    required_roots: int,
    slope_u: tuple[int, ...],
    slope_v: tuple[int, ...],
    p: int,
    label: str,
) -> tuple[set[tuple[int, ...]], set[int], int, int, int]:
    """Return rich points, finite slopes, point count, point bound, and slope bound."""

    if not kernel_basis:
        return set(), set(), 0, 0, 0
    width = len(kernel_basis[0])
    projective_points = projective_span_points(kernel_basis, p)
    rich_points: set[tuple[int, ...]] = set()
    finite_rich_slopes: set[int] = set()
    for point in projective_points:
        root_count = sum(poly_eval(list(point), x, p) == 0 for x in root_domain)
        if root_count > required_roots:
            raise AssertionError(f"{label} arrangement point had too many roots")
        if root_count != required_roots:
            continue
        rich_points.add(point)
        slope_b = hankel_apply(slope_v, 1, width - 1, list(point), p)
        if slope_b[0] == 0:
            continue
        slope_a = hankel_apply(slope_u, 1, width - 1, list(point), p)
        slope = slope_from_gate(slope_a, slope_b, p)
        if slope is None:
            raise AssertionError(f"{label} rich point had inconsistent slope")
        finite_rich_slopes.add(slope)

    if required_roots <= 0:
        rank_stratified_bound = len(projective_points)
        rank_stratified_slope_bound = len(projective_points)
    elif len(kernel_basis) == 1:
        rank_stratified_bound = 1
        rank_stratified_slope_bound = 1
    else:
        fixed_roots, root_hyperplane_weights = fixed_anchor_root_hyperplane_weights(
            kernel_basis, root_domain, p
        )
        if fixed_roots >= required_roots:
            raise AssertionError(f"{label} kernel had too many fixed roots")
        richness_deficit = required_roots - fixed_roots
        if any(weight > richness_deficit for weight in root_hyperplane_weights.values()):
            raise AssertionError(f"{label} root hyperplane was overfull")
        rank_stratified_bound = fixed_anchor_rank_stratified_bound(
            root_hyperplane_weights, len(kernel_basis), richness_deficit, p
        )
        rank_stratified_slope_bound = fixed_anchor_rank_stratified_bound(
            root_hyperplane_weights,
            len(kernel_basis),
            richness_deficit,
            p,
            slope_image=True,
        )
    if len(rich_points) > rank_stratified_bound:
        raise AssertionError(f"{label} rich points exceeded rank-stratified bound")
    if len(finite_rich_slopes) > rank_stratified_bound:
        raise AssertionError(f"{label} slopes exceeded rank-stratified bound")
    if len(finite_rich_slopes) > rank_stratified_slope_bound:
        raise AssertionError(f"{label} slopes exceeded heavy-flat slope-image bound")
    return (
        rich_points,
        finite_rich_slopes,
        len(projective_points),
        rank_stratified_bound,
        rank_stratified_slope_bound,
    )


def projective_span_points(basis: list[tuple[int, ...]], p: int) -> set[tuple[int, ...]]:
    if not basis:
        return set()
    points: set[tuple[int, ...]] = set()
    dimension = len(basis)
    width = len(basis[0])
    for first_nonzero in range(dimension):
        tail_width = dimension - first_nonzero - 1
        for tail in cartesian_product(range(p), repeat=tail_width):
            coeffs = [0] * dimension
            coeffs[first_nonzero] = 1
            coeffs[first_nonzero + 1 :] = tail
            vector = [0] * width
            for coeff, basis_vector in zip(coeffs, basis, strict=True):
                if coeff == 0:
                    continue
                for idx, entry in enumerate(basis_vector):
                    vector[idx] = (vector[idx] + coeff * entry) % p
            points.add(normalize_projective_vector(vector, p))
    return points


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


def affine_rank_2d(points: list[tuple[int, int]], p: int) -> int:
    unique_points = list(dict.fromkeys(points))
    if len(unique_points) <= 1:
        return 0
    base = unique_points[0]
    differences = [
        ((point[0] - base[0]) % p, (point[1] - base[1]) % p)
        for point in unique_points[1:]
    ]
    if all(diff == (0, 0) for diff in differences):
        return 0
    for left, right in combinations(differences, 2):
        if det2(left, right, p) != 0:
            return 2
    return 1


def affine_line_key(points: list[tuple[int, int]], p: int) -> tuple[int, int, int]:
    unique_points = list(dict.fromkeys(points))
    if len(unique_points) < 2:
        raise AssertionError("line key needs two points")
    base = unique_points[0]
    for point in unique_points[1:]:
        dx = (point[0] - base[0]) % p
        dy = (point[1] - base[1]) % p
        if dx == 0 and dy == 0:
            continue
        normal_s = dy
        normal_p = (-dx) % p
        constant = (normal_s * base[0] + normal_p * base[1]) % p
        for value in (normal_s, normal_p):
            if value:
                scale = inv_mod(value, p)
                return (
                    normal_s * scale % p,
                    normal_p * scale % p,
                    constant * scale % p,
                )
    raise AssertionError("distinct points did not define a line")


def two_root_line_model(
    line_key: tuple[int, int, int], p: int
) -> tuple[str, int, int | None]:
    normal_sum, normal_product, constant = line_key
    if normal_sum == 0 and normal_product == 0:
        raise AssertionError("line key vanished")
    if normal_product == 0:
        total = constant * inv_mod(normal_sum, p) % p
        return "sum_mobius", total, None

    inv_product = inv_mod(normal_product, p)
    center = (-normal_sum * inv_product) % p
    offset = constant * inv_product % p
    multiplier = (center * center + offset) % p
    if multiplier == 0:
        return "fixed_root", center, None
    return "product_mobius", center, multiplier


def affine_line_points(line_key: tuple[int, int, int], p: int) -> list[tuple[int, int]]:
    normal_sum, normal_product, constant = line_key
    if normal_sum == 0 and normal_product == 0:
        raise AssertionError("line key vanished")
    if normal_product:
        inv_product = inv_mod(normal_product, p)
        return [
            (root_sum, (constant - normal_sum * root_sum) * inv_product % p)
            for root_sum in range(p)
        ]
    inv_sum = inv_mod(normal_sum, p)
    root_sum = constant * inv_sum % p
    return [(root_sum, root_product) for root_product in range(p)]


def affine_line_keys(p: int) -> list[tuple[int, int, int]]:
    keys = []
    for normal_sum in range(p):
        for normal_product in range(p):
            if normal_sum == 0 and normal_product == 0:
                continue
            if normal_sum:
                scale = inv_mod(normal_sum, p)
            else:
                scale = inv_mod(normal_product, p)
            normalized = (normal_sum * scale % p, normal_product * scale % p)
            if normalized != (normal_sum, normal_product):
                continue
            for constant in range(p):
                keys.append((normal_sum, normal_product, constant))
    return keys


def two_exchange_minor_coefficients(
    a_pad: tuple[int, ...],
    a_shift: tuple[int, ...],
    a_square_shift: tuple[int, ...],
    b_pad: tuple[int, ...],
    b_shift: tuple[int, ...],
    b_square_shift: tuple[int, ...],
    row: int,
    col: int,
    p: int,
) -> tuple[int, int, int, int, int, int]:
    return (
        coord_det(a_square_shift, b_square_shift, row, col, p),
        (
            -coord_det(a_shift, b_square_shift, row, col, p)
            - coord_det(a_square_shift, b_shift, row, col, p)
        )
        % p,
        (
            coord_det(a_pad, b_square_shift, row, col, p)
            + coord_det(a_square_shift, b_pad, row, col, p)
        )
        % p,
        coord_det(a_shift, b_shift, row, col, p),
        (
            -coord_det(a_shift, b_pad, row, col, p)
            - coord_det(a_pad, b_shift, row, col, p)
        )
        % p,
        coord_det(a_pad, b_pad, row, col, p),
    )


def two_exchange_minor_value(
    coeffs: tuple[int, int, int, int, int, int], s: int, q: int, p: int
) -> int:
    (
        const,
        coeff_sum,
        coeff_product,
        coeff_sum_sq,
        coeff_sum_product,
        coeff_product_sq,
    ) = coeffs
    return (
        const
        + coeff_sum * s
        + coeff_product * q
        + coeff_sum_sq * s * s
        + coeff_sum_product * s * q
        + coeff_product_sq * q * q
    ) % p


def strict_exchange_profile(
    locator_rows: list[tuple[tuple[int, ...], int]], t: int
) -> dict[str, int]:
    strict_pairs = 0
    one_exchange_pairs = 0
    same_slope_strict_pairs = 0
    same_slope_one_exchange_pairs = 0
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
            if exchange == 1:
                one_exchange_pairs += 1
                if slope_left == locator_rows[right][1]:
                    same_slope_one_exchange_pairs += 1

    return {
        "strict_pairs": strict_pairs,
        "one_exchange_pairs": one_exchange_pairs,
        "max_strict_degree": max(degrees, default=0),
        "same_slope_strict_pairs": same_slope_strict_pairs,
        "same_slope_one_exchange_pairs": same_slope_one_exchange_pairs,
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


def same_slope_one_exchange_root_slice_keys(
    locator_rows: list[tuple[tuple[int, ...], int]], j: int
) -> tuple[set[tuple[tuple[int, ...], int]], int]:
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
    return slice_keys, same_slope_edges


def same_slope_one_exchange_lift_profile(
    locator_rows: list[tuple[tuple[int, ...], int]],
    domain: tuple[int, ...],
    u: tuple[int, ...],
    v: tuple[int, ...],
    t: int,
    j: int,
    p: int,
) -> dict[str, int]:
    if j <= 0:
        raise AssertionError("invalid root-slice boundary size")
    row_map = {tuple(sorted(complement)): slope for complement, slope in locator_rows}
    slice_keys, same_slope_edges = same_slope_one_exchange_root_slice_keys(
        locator_rows, j
    )

    next_slope_set: set[int] = set()
    next_core_locators = 0
    for core in combinations(domain, j - 1):
        core_locator = locator(tuple(sorted(core)), p)
        next_a = hankel_apply(u, t + 1, j - 1, core_locator, p)
        next_b = hankel_apply(v, t + 1, j - 1, core_locator, p)
        next_slope = slope_from_gate(next_a, next_b, p)
        if next_slope is None:
            continue
        next_core_locators += 1
        next_slope_set.add(next_slope)

    max_noncontained = 0
    max_aperiodic_members = 0
    lifted_member_checks = 0
    for core, slope in slice_keys:
        core_locator = locator(core, p)
        next_a = hankel_apply(u, t + 1, j - 1, core_locator, p)
        next_b = hankel_apply(v, t + 1, j - 1, core_locator, p)
        if slope_from_gate(next_a, next_b, p) != slope:
            raise AssertionError("same-slope one-exchange edge missed the t+1 root lift")
        noncontained_count = 0
        aperiodic_member_count = 0
        for x in domain:
            if x in core:
                continue
            complement = tuple(sorted(core + (x,)))
            incident, noncontained = fixed_slope_incidence(u, v, complement, slope, t, j, p)
            if not incident:
                raise AssertionError("same-slope one-exchange edge did not extend to its root slice")
            if noncontained:
                noncontained_count += 1
            if row_map.get(complement) == slope:
                aperiodic_member_count += 1
            lifted_member_checks += 1
        max_noncontained = max(max_noncontained, noncontained_count)
        max_aperiodic_members = max(max_aperiodic_members, aperiodic_member_count)

    slice_slope_set = {slope for _, slope in slice_keys}
    if not slice_slope_set <= next_slope_set:
        raise AssertionError("same-slope root-slice slopes escaped the t+1 core image")
    return {
        "same_slope_one_exchange_edges": same_slope_edges,
        "same_slope_one_exchange_root_slices": len(slice_keys),
        "same_slope_one_exchange_root_slopes": len(slice_slope_set),
        "same_slope_one_exchange_next_core_locators": next_core_locators,
        "same_slope_one_exchange_next_slopes": len(next_slope_set),
        "same_slope_one_exchange_member_checks": lifted_member_checks,
        "same_slope_one_exchange_noncontained_max": max_noncontained,
        "same_slope_one_exchange_aperiodic_members_max": max_aperiodic_members,
    }


def two_exchange_quadratic_slice_profile(
    locator_rows: list[tuple[tuple[int, ...], int]],
    domain: tuple[int, ...],
    u: tuple[int, ...],
    v: tuple[int, ...],
    t: int,
    j: int,
    p: int,
    charged_root_slope_set: set[int] | None = None,
) -> dict[str, int]:
    if t != 3:
        return {
            "two_exchange_pairs": 0,
            "two_exchange_same_slope_pairs": 0,
            "two_exchange_different_slope_pairs": 0,
            "two_exchange_cores": 0,
            "two_exchange_slices_checked": 0,
            "two_exchange_minor_polynomial_checks": 0,
            "two_exchange_bad_locator_checks": 0,
            "two_exchange_max_slice_aperiodic_locators": 0,
            "two_exchange_max_slice_slope_image": 0,
            "two_exchange_same_slope_clusters": 0,
            "two_exchange_same_slope_line_clusters": 0,
            "two_exchange_same_slope_fixed_root_lines": 0,
            "two_exchange_same_slope_mobius_lines": 0,
            "two_exchange_same_slope_product_mobius_lines": 0,
            "two_exchange_same_slope_sum_mobius_lines": 0,
            "two_exchange_same_slope_line_two_exchange_pairs": 0,
            "two_exchange_same_slope_mobius_two_exchange_pairs": 0,
            "two_exchange_same_slope_mobius_pair_checks": 0,
            "two_exchange_same_slope_mobius_member_max": 0,
            "two_exchange_same_slope_plane_clusters": 0,
            "two_exchange_same_slope_plane_lifts": 0,
            "two_exchange_same_slope_plane_two_exchange_pairs": 0,
            "two_exchange_same_slope_affine_member_max": 0,
            "two_exchange_same_slope_lift_checks": 0,
            "two_exchange_det_line_components": 0,
            "two_exchange_det_line_fixed_root": 0,
            "two_exchange_det_line_product_mobius": 0,
            "two_exchange_det_line_sum_mobius": 0,
            "two_exchange_det_line_constant_slope": 0,
            "two_exchange_det_line_variable_slope": 0,
            "two_exchange_det_line_slope_max": 0,
            "two_exchange_det_line_aperiodic_max": 0,
            "two_exchange_det_line_point_checks": 0,
            "two_exchange_det_full_planes": 0,
            "two_exchange_det_full_plane_constant_slope": 0,
            "two_exchange_det_full_plane_variable_slope": 0,
            "two_exchange_det_full_plane_contained": 0,
            "two_exchange_det_full_plane_den_rank_max": 0,
            "two_exchange_det_full_plane_slope_max": 0,
            "two_exchange_det_full_plane_aperiodic_max": 0,
            "two_exchange_det_full_plane_lifts": 0,
            "two_exchange_det_proper_lines": 0,
            "two_exchange_det_proper_line_fixed_root": 0,
            "two_exchange_det_proper_line_product_mobius": 0,
            "two_exchange_det_proper_line_sum_mobius": 0,
            "two_exchange_det_proper_line_constant_slope": 0,
            "two_exchange_det_proper_line_variable_slope": 0,
            "two_exchange_det_proper_line_slope_max": 0,
            "two_exchange_det_proper_line_aperiodic_max": 0,
            "two_exchange_det_proper_line_core_max": 0,
            "two_exchange_det_proper_line_variable_injective": 0,
            "two_exchange_det_proper_line_variable_pole_max": 0,
            "two_exchange_det_proper_line_variable_aperiodic_slope_max": 0,
            "two_exchange_det_proper_line_variable_injective_checks": 0,
            "two_exchange_det_proper_line_variable_aperiodic_slopes": 0,
            "two_exchange_det_proper_line_variable_new_slopes": 0,
            "two_exchange_det_proper_line_variable_new_slope_max": 0,
            "two_exchange_det_proper_line_variable_nonfixed": 0,
            "two_exchange_det_proper_line_variable_anchored": 0,
            "two_exchange_det_proper_line_variable_unanchored": 0,
            "two_exchange_det_proper_line_variable_domain_pair_max": 0,
            "two_exchange_det_proper_line_variable_domain_pair_checks": 0,
            "two_exchange_det_proper_line_variable_charged_slope_checks": 0,
        }
    if j < 2:
        raise AssertionError("two-exchange slices need j>=2")

    charged_root_slope_set = charged_root_slope_set or set()
    row_map = {tuple(sorted(complement)): slope for complement, slope in locator_rows}
    two_exchange_pairs = 0
    same_slope_pairs = 0
    different_slope_pairs = 0
    edge_cores: set[tuple[int, ...]] = set()
    for left in range(len(locator_rows)):
        left_set = set(locator_rows[left][0])
        left_slope = locator_rows[left][1]
        for right in range(left + 1, len(locator_rows)):
            right_set = set(locator_rows[right][0])
            if len(left_set - right_set) != 2 or len(right_set - left_set) != 2:
                continue
            two_exchange_pairs += 1
            core = tuple(sorted(left_set & right_set))
            if len(core) != j - 2:
                raise AssertionError("two-exchange core has wrong size")
            edge_cores.add(core)
            if left_slope == locator_rows[right][1]:
                same_slope_pairs += 1
            else:
                different_slope_pairs += 1

    slices_checked = 0
    minor_polynomial_checks = 0
    bad_locator_checks = 0
    max_slice_aperiodic = 0
    max_slice_slope_image = 0
    same_slope_clusters = 0
    same_slope_line_clusters = 0
    same_slope_fixed_root_lines = 0
    same_slope_mobius_lines = 0
    same_slope_product_mobius_lines = 0
    same_slope_sum_mobius_lines = 0
    same_slope_line_two_exchange_pairs = 0
    same_slope_mobius_two_exchange_pairs = 0
    same_slope_mobius_pair_checks = 0
    same_slope_mobius_member_max = 0
    same_slope_plane_clusters = 0
    same_slope_plane_lifts = 0
    same_slope_plane_two_exchange_pairs = 0
    same_slope_affine_member_max = 0
    same_slope_lift_checks = 0
    same_slope_cluster_two_exchange_pairs = 0
    same_slope_line_keys: set[tuple[tuple[int, ...], tuple[int, int, int]]] = set()
    det_line_keys: set[tuple[tuple[int, ...], tuple[int, int, int]]] = set()
    det_line_components = 0
    det_line_fixed_root = 0
    det_line_product_mobius = 0
    det_line_sum_mobius = 0
    det_line_constant_slope = 0
    det_line_variable_slope = 0
    det_line_slope_max = 0
    det_line_aperiodic_max = 0
    det_line_point_checks = 0
    det_full_planes = 0
    det_full_plane_constant_slope = 0
    det_full_plane_variable_slope = 0
    det_full_plane_contained = 0
    det_full_plane_den_rank_max = 0
    det_full_plane_slope_max = 0
    det_full_plane_aperiodic_max = 0
    det_full_plane_lifts = 0
    det_proper_lines = 0
    det_proper_line_fixed_root = 0
    det_proper_line_product_mobius = 0
    det_proper_line_sum_mobius = 0
    det_proper_line_constant_slope = 0
    det_proper_line_variable_slope = 0
    det_proper_line_slope_max = 0
    det_proper_line_aperiodic_max = 0
    det_proper_line_core_max = 0
    det_proper_line_variable_injective = 0
    det_proper_line_variable_pole_max = 0
    det_proper_line_variable_aperiodic_slope_max = 0
    det_proper_line_variable_injective_checks = 0
    det_proper_line_variable_aperiodic_slopes: set[int] = set()
    det_proper_line_variable_new_slopes: set[int] = set()
    det_proper_line_variable_new_slope_max = 0
    det_proper_line_variable_nonfixed = 0
    det_proper_line_variable_anchored = 0
    det_proper_line_variable_unanchored = 0
    det_proper_line_variable_domain_pair_max = 0
    det_proper_line_variable_domain_pair_checks = 0
    det_proper_line_variable_slope_sets: list[set[int]] = []
    det_proper_line_variable_charged_slope_checks = 0
    det_charged_line_slope_set = set(charged_root_slope_set)
    all_affine_line_keys = affine_line_keys(p)
    for core in combinations(domain, j - 2):
        core_tuple = tuple(sorted(core))
        core_locator = locator(core_tuple, p)
        if len(core_locator) != j - 1:
            raise AssertionError("two-exchange core locator has wrong length")
        pad_vec = core_locator + [0, 0]
        shift_vec = [0] + core_locator + [0]
        square_shift_vec = [0, 0] + core_locator
        a_pad = hankel_apply(u, t, j, pad_vec, p)
        a_shift = hankel_apply(u, t, j, shift_vec, p)
        a_square_shift = hankel_apply(u, t, j, square_shift_vec, p)
        b_pad = hankel_apply(v, t, j, pad_vec, p)
        b_shift = hankel_apply(v, t, j, shift_vec, p)
        b_square_shift = hankel_apply(v, t, j, square_shift_vec, p)
        slices_checked += 1

        slice_aperiodic = 0
        slice_slopes: set[int] = set()
        same_slope_entries: dict[int, list[tuple[int, int, int, int]]] = {}
        minor_coefficients = [
            two_exchange_minor_coefficients(
                a_pad,
                a_shift,
                a_square_shift,
                b_pad,
                b_shift,
                b_square_shift,
                row,
                col,
                p,
            )
            for row, col in combinations(range(t), 2)
        ]
        core_full_det_plane = all(
            all(coefficient == 0 for coefficient in coeffs)
            for coeffs in minor_coefficients
        )
        if core_full_det_plane:
            det_full_planes += 1
            det_full_plane_den_rank_max = max(
                det_full_plane_den_rank_max,
                vector_span_rank([b_square_shift, b_shift, b_pad], p),
            )
        pair_coordinate_to_complement: dict[tuple[int, int], tuple[int, ...]] = {}
        available = tuple(x for x in domain if x not in core_tuple)
        for x, y in combinations(available, 2):
            root_sum = (x + y) % p
            root_product = x * y % p
            complement = tuple(sorted(core_tuple + (x, y)))
            if (root_sum, root_product) in pair_coordinate_to_complement:
                raise AssertionError("two domain pairs had the same elementary coordinates")
            pair_coordinate_to_complement[(root_sum, root_product)] = complement
            expected_locator = locator(complement, p)
            slice_locator = [
                (
                    square_shift_vec[idx]
                    - root_sum * shift_vec[idx]
                    + root_product * pad_vec[idx]
                )
                % p
                for idx in range(j + 1)
            ]
            if slice_locator != expected_locator:
                raise AssertionError("two-exchange elementary locator formula failed")
            a_vec = tuple(
                (
                    a_square_shift[idx]
                    - root_sum * a_shift[idx]
                    + root_product * a_pad[idx]
                )
                % p
                for idx in range(t)
            )
            b_vec = tuple(
                (
                    b_square_shift[idx]
                    - root_sum * b_shift[idx]
                    + root_product * b_pad[idx]
                )
                % p
                for idx in range(t)
            )
            if a_vec != hankel_apply(u, t, j, slice_locator, p):
                raise AssertionError("two-exchange numerator slice formula failed")
            if b_vec != hankel_apply(v, t, j, slice_locator, p):
                raise AssertionError("two-exchange denominator slice formula failed")

            all_minors_zero = True
            for coeffs, (row, col) in zip(minor_coefficients, combinations(range(t), 2), strict=True):
                polynomial_value = two_exchange_minor_value(
                    coeffs, root_sum, root_product, p
                )
                minor_value = coord_det(a_vec, b_vec, row, col, p)
                if polynomial_value != minor_value:
                    raise AssertionError("two-exchange minor polynomial certificate failed")
                if minor_value:
                    all_minors_zero = False
                minor_polynomial_checks += 1

            slope = slope_from_gate(a_vec, b_vec, p)
            if any(value != 0 for value in b_vec) and (slope is not None) != all_minors_zero:
                raise AssertionError("two-exchange minors disagreed with projective gate")
            row_slope = row_map.get(complement)
            if row_slope is not None:
                if row_slope != slope:
                    raise AssertionError("two-exchange row slope disagreed with slice gate")
                if not all_minors_zero:
                    raise AssertionError("aperiodic two-exchange locator missed slice minors")
                slice_aperiodic += 1
                slice_slopes.add(row_slope)
                same_slope_entries.setdefault(row_slope, []).append(
                    (x, y, root_sum, root_product)
                )
                bad_locator_checks += 1
        max_slice_aperiodic = max(max_slice_aperiodic, slice_aperiodic)
        max_slice_slope_image = max(max_slice_slope_image, len(slice_slopes))

        if core_full_det_plane:
            plane_slopes: set[int] = set()
            plane_aperiodic = 0
            for root_sum, root_product in cartesian_product(range(p), repeat=2):
                a_vec = tuple(
                    (
                        a_square_shift[idx]
                        - root_sum * a_shift[idx]
                        + root_product * a_pad[idx]
                    )
                    % p
                    for idx in range(t)
                )
                b_vec = tuple(
                    (
                        b_square_shift[idx]
                        - root_sum * b_shift[idx]
                        + root_product * b_pad[idx]
                    )
                    % p
                    for idx in range(t)
                )
                if all(value == 0 for value in b_vec):
                    continue
                slope = slope_from_gate(a_vec, b_vec, p)
                if slope is None:
                    raise AssertionError("full determinant plane point had no slope")
                plane_slopes.add(slope)
                complement = pair_coordinate_to_complement.get((root_sum, root_product))
                if complement is None:
                    continue
                row_slope = row_map.get(complement)
                if row_slope is None:
                    continue
                if row_slope != slope:
                    raise AssertionError("full-plane slope disagreed with row slope")
                plane_aperiodic += 1
            if not plane_slopes:
                det_full_plane_contained += 1
            elif len(plane_slopes) == 1:
                det_full_plane_constant_slope += 1
                slope = next(iter(plane_slopes))
                det_charged_line_slope_set.add(slope)
                next_a = hankel_apply(u, t + 2, j - 2, core_locator, p)
                next_b = hankel_apply(v, t + 2, j - 2, core_locator, p)
                if slope_from_gate(next_a, next_b, p) != slope:
                    raise AssertionError("constant full determinant plane missed H5 lift")
                if all(value == 0 for value in next_b) and plane_aperiodic:
                    raise AssertionError("noncontained full determinant plane lift was contained")
                det_full_plane_lifts += 1
            else:
                det_full_plane_variable_slope += 1
            det_full_plane_slope_max = max(det_full_plane_slope_max, len(plane_slopes))
            det_full_plane_aperiodic_max = max(
                det_full_plane_aperiodic_max, plane_aperiodic
            )

        core_det_line_count = 0
        core_proper_line_count = 0
        for line_key in all_affine_line_keys:
            line_points = affine_line_points(line_key, p)
            if not all(
                two_exchange_minor_value(coeffs, root_sum, root_product, p) == 0
                for root_sum, root_product in line_points
                for coeffs in minor_coefficients
            ):
                continue
            core_det_line_count += 1
            det_line_components += 1
            det_line_keys.add((core_tuple, line_key))
            line_model, _line_parameter, _line_multiplier = two_root_line_model(line_key, p)
            if line_model == "fixed_root":
                det_line_fixed_root += 1
            elif line_model == "product_mobius":
                det_line_product_mobius += 1
            elif line_model == "sum_mobius":
                det_line_sum_mobius += 1
            else:
                raise AssertionError("unknown two-root line model")

            line_slopes: set[int] = set()
            line_aperiodic_slopes: set[int] = set()
            line_noncontained = 0
            line_aperiodic = 0
            line_domain_pairs = 0
            for root_sum, root_product in line_points:
                a_vec = tuple(
                    (
                        a_square_shift[idx]
                        - root_sum * a_shift[idx]
                        + root_product * a_pad[idx]
                    )
                    % p
                    for idx in range(t)
                )
                b_vec = tuple(
                    (
                        b_square_shift[idx]
                        - root_sum * b_shift[idx]
                        + root_product * b_pad[idx]
                    )
                    % p
                    for idx in range(t)
                )
                if all(value == 0 for value in b_vec):
                    continue
                line_noncontained += 1
                slope = slope_from_gate(a_vec, b_vec, p)
                if slope is None:
                    raise AssertionError("determinantal line point had no slope")
                line_slopes.add(slope)
                complement = pair_coordinate_to_complement.get((root_sum, root_product))
                if complement is None:
                    continue
                line_domain_pairs += 1
                row_slope = row_map.get(complement)
                if row_slope is None:
                    continue
                if row_slope != slope:
                    raise AssertionError("line-component slope disagreed with row slope")
                line_aperiodic += 1
                line_aperiodic_slopes.add(slope)
            if len(line_slopes) <= 1:
                det_line_constant_slope += 1
            else:
                det_line_variable_slope += 1
            det_line_slope_max = max(det_line_slope_max, len(line_slopes))
            det_line_aperiodic_max = max(det_line_aperiodic_max, line_aperiodic)
            det_line_point_checks += len(line_points)
            if core_full_det_plane:
                continue
            core_proper_line_count += 1
            det_proper_lines += 1
            if line_model == "fixed_root":
                det_proper_line_fixed_root += 1
            elif line_model == "product_mobius":
                det_proper_line_product_mobius += 1
            elif line_model == "sum_mobius":
                det_proper_line_sum_mobius += 1
            else:
                raise AssertionError("unknown proper two-root line model")
            if len(line_slopes) <= 1:
                det_proper_line_constant_slope += 1
                if line_model == "fixed_root":
                    det_charged_line_slope_set.update(line_aperiodic_slopes)
            else:
                det_proper_line_variable_slope += 1
                if line_noncontained != len(line_slopes):
                    raise AssertionError("variable proper line was not slope-injective")
                if line_aperiodic != len(line_aperiodic_slopes):
                    raise AssertionError(
                        "variable proper line had repeated aperiodic slopes"
                    )
                if line_aperiodic > line_domain_pairs:
                    raise AssertionError("variable proper line exceeded its domain-pair packet")
                line_poles = len(line_points) - line_noncontained
                if line_poles > 1:
                    raise AssertionError("variable proper line had multiple poles")
                if line_model != "fixed_root":
                    det_proper_line_variable_nonfixed += 1
                    if _line_parameter in core_tuple:
                        det_proper_line_variable_anchored += 1
                    else:
                        det_proper_line_variable_unanchored += 1
                det_proper_line_variable_domain_pair_max = max(
                    det_proper_line_variable_domain_pair_max, line_domain_pairs
                )
                det_proper_line_variable_domain_pair_checks += line_domain_pairs
                det_proper_line_variable_slope_sets.append(set(line_aperiodic_slopes))
                det_proper_line_variable_injective += 1
                det_proper_line_variable_pole_max = max(
                    det_proper_line_variable_pole_max, line_poles
                )
                det_proper_line_variable_aperiodic_slope_max = max(
                    det_proper_line_variable_aperiodic_slope_max,
                    len(line_aperiodic_slopes),
                )
                det_proper_line_variable_injective_checks += line_noncontained
                det_proper_line_variable_aperiodic_slopes.update(
                    line_aperiodic_slopes
                )
                det_proper_line_variable_charged_slope_checks += len(
                    line_aperiodic_slopes
                )
            det_proper_line_slope_max = max(
                det_proper_line_slope_max, len(line_slopes)
            )
            det_proper_line_aperiodic_max = max(
                det_proper_line_aperiodic_max, line_aperiodic
            )
        if core_full_det_plane:
            if core_det_line_count != p * (p + 1):
                raise AssertionError(
                    "full determinant plane did not contain every affine line"
                )
        elif core_proper_line_count > 2:
            raise AssertionError(
                "proper two-exchange determinant locus had more than two line components"
            )
        det_proper_line_core_max = max(
            det_proper_line_core_max, core_proper_line_count
        )

        for slope, entries in same_slope_entries.items():
            if len(entries) < 2:
                continue
            same_slope_clusters += 1
            same_slope_affine_member_max = max(same_slope_affine_member_max, len(entries))
            point_rank = affine_rank_2d([(entry[2], entry[3]) for entry in entries], p)
            cluster_two_exchange_pairs = 0
            for left, right in combinations(entries, 2):
                if {left[0], left[1]}.isdisjoint({right[0], right[1]}):
                    cluster_two_exchange_pairs += 1
            same_slope_cluster_two_exchange_pairs += cluster_two_exchange_pairs

            if point_rank == 1:
                same_slope_line_clusters += 1
                same_slope_line_two_exchange_pairs += cluster_two_exchange_pairs
                line_key = affine_line_key([(entry[2], entry[3]) for entry in entries], p)
                same_slope_line_keys.add((core_tuple, line_key))
                line_model, line_parameter, line_multiplier = two_root_line_model(line_key, p)
                common_roots = set(entries[0][:2])
                for entry in entries[1:]:
                    common_roots &= set(entry[:2])
                if common_roots:
                    same_slope_fixed_root_lines += 1
                    fixed_root = next(iter(common_roots))
                    if line_model != "fixed_root" or line_parameter != fixed_root:
                        raise AssertionError("fixed-root line model disagreed with common root")
                    for _x, _y, root_sum, root_product in entries:
                        if (root_product - fixed_root * root_sum + fixed_root * fixed_root) % p:
                            raise AssertionError("fixed-root two-exchange line had wrong equation")
                    if cluster_two_exchange_pairs:
                        raise AssertionError("fixed-root line contributed a two-exchange pair")
                else:
                    same_slope_mobius_lines += 1
                    same_slope_mobius_two_exchange_pairs += cluster_two_exchange_pairs
                    same_slope_mobius_member_max = max(
                        same_slope_mobius_member_max, len(entries)
                    )
                    if line_model == "product_mobius":
                        same_slope_product_mobius_lines += 1
                        if line_multiplier is None or line_multiplier == 0:
                            raise AssertionError("product Mobius line had zero multiplier")
                        for x, y, _root_sum, _root_product in entries:
                            if (
                                (x - line_parameter)
                                * (y - line_parameter)
                                - line_multiplier
                            ) % p:
                                raise AssertionError("product Mobius line missed a pair")
                            if x == line_parameter or y == line_parameter:
                                raise AssertionError("product Mobius pair hit its pole")
                            if (
                                line_parameter
                                + line_multiplier * inv_mod((x - line_parameter) % p, p)
                                - y
                            ) % p:
                                raise AssertionError("product Mobius involution missed y")
                            if (
                                line_parameter
                                + line_multiplier * inv_mod((y - line_parameter) % p, p)
                                - x
                            ) % p:
                                raise AssertionError("product Mobius involution missed x")
                            same_slope_mobius_pair_checks += 2
                    elif line_model == "sum_mobius":
                        same_slope_sum_mobius_lines += 1
                        for x, y, root_sum, _root_product in entries:
                            if root_sum != line_parameter:
                                raise AssertionError("sum Mobius line missed a pair")
                            if (line_parameter - x - y) % p:
                                raise AssertionError("sum Mobius involution missed y")
                            if (line_parameter - y - x) % p:
                                raise AssertionError("sum Mobius involution missed x")
                            same_slope_mobius_pair_checks += 2
                    else:
                        raise AssertionError("non-common line was not Mobius")
                for _x, _y, root_sum, root_product in entries:
                    if (line_key[0] * root_sum + line_key[1] * root_product - line_key[2]) % p:
                        raise AssertionError("same-slope two-exchange line key missed a point")
                continue

            if point_rank == 2:
                same_slope_plane_clusters += 1
                same_slope_plane_two_exchange_pairs += cluster_two_exchange_pairs
                next_a = hankel_apply(u, t + 2, j - 2, core_locator, p)
                next_b = hankel_apply(v, t + 2, j - 2, core_locator, p)
                if slope_from_gate(next_a, next_b, p) != slope:
                    raise AssertionError("same-slope two-exchange plane missed the t+2 lift")
                if all(value == 0 for value in next_b):
                    raise AssertionError("same-slope two-exchange plane lift was contained")
                same_slope_plane_lifts += 1
                same_slope_lift_checks += len(entries)
                for x, y, _root_sum, _root_product in entries:
                    complement = tuple(sorted(core_tuple + (x, y)))
                    incident, noncontained = fixed_slope_incidence(
                        u, v, complement, slope, t, j, p
                    )
                    if not incident or not noncontained:
                        raise AssertionError("same-slope plane member failed its original gate")
                continue

            raise AssertionError("same-slope two-exchange cluster had duplicate affine points")

    if same_slope_cluster_two_exchange_pairs != same_slope_pairs:
        raise AssertionError("same-slope affine ledger missed a two-exchange pair")
    if not same_slope_line_keys <= det_line_keys:
        raise AssertionError("same-slope line cluster was not a determinantal line")
    det_proper_line_variable_new_slopes = (
        det_proper_line_variable_aperiodic_slopes - det_charged_line_slope_set
    )
    if det_proper_line_variable_slope_sets:
        det_proper_line_variable_new_slope_max = max(
            len(slope_set - det_charged_line_slope_set)
            for slope_set in det_proper_line_variable_slope_sets
        )

    return {
        "two_exchange_pairs": two_exchange_pairs,
        "two_exchange_same_slope_pairs": same_slope_pairs,
        "two_exchange_different_slope_pairs": different_slope_pairs,
        "two_exchange_cores": len(edge_cores),
        "two_exchange_slices_checked": slices_checked,
        "two_exchange_minor_polynomial_checks": minor_polynomial_checks,
        "two_exchange_bad_locator_checks": bad_locator_checks,
        "two_exchange_max_slice_aperiodic_locators": max_slice_aperiodic,
        "two_exchange_max_slice_slope_image": max_slice_slope_image,
        "two_exchange_same_slope_clusters": same_slope_clusters,
        "two_exchange_same_slope_line_clusters": same_slope_line_clusters,
        "two_exchange_same_slope_fixed_root_lines": same_slope_fixed_root_lines,
        "two_exchange_same_slope_mobius_lines": same_slope_mobius_lines,
        "two_exchange_same_slope_product_mobius_lines": (
            same_slope_product_mobius_lines
        ),
        "two_exchange_same_slope_sum_mobius_lines": same_slope_sum_mobius_lines,
        "two_exchange_same_slope_line_two_exchange_pairs": (
            same_slope_line_two_exchange_pairs
        ),
        "two_exchange_same_slope_mobius_two_exchange_pairs": (
            same_slope_mobius_two_exchange_pairs
        ),
        "two_exchange_same_slope_mobius_pair_checks": same_slope_mobius_pair_checks,
        "two_exchange_same_slope_mobius_member_max": same_slope_mobius_member_max,
        "two_exchange_same_slope_plane_clusters": same_slope_plane_clusters,
        "two_exchange_same_slope_plane_lifts": same_slope_plane_lifts,
        "two_exchange_same_slope_plane_two_exchange_pairs": (
            same_slope_plane_two_exchange_pairs
        ),
        "two_exchange_same_slope_affine_member_max": same_slope_affine_member_max,
        "two_exchange_same_slope_lift_checks": same_slope_lift_checks,
        "two_exchange_det_line_components": det_line_components,
        "two_exchange_det_line_fixed_root": det_line_fixed_root,
        "two_exchange_det_line_product_mobius": det_line_product_mobius,
        "two_exchange_det_line_sum_mobius": det_line_sum_mobius,
        "two_exchange_det_line_constant_slope": det_line_constant_slope,
        "two_exchange_det_line_variable_slope": det_line_variable_slope,
        "two_exchange_det_line_slope_max": det_line_slope_max,
        "two_exchange_det_line_aperiodic_max": det_line_aperiodic_max,
        "two_exchange_det_line_point_checks": det_line_point_checks,
        "two_exchange_det_full_planes": det_full_planes,
        "two_exchange_det_full_plane_constant_slope": det_full_plane_constant_slope,
        "two_exchange_det_full_plane_variable_slope": det_full_plane_variable_slope,
        "two_exchange_det_full_plane_contained": det_full_plane_contained,
        "two_exchange_det_full_plane_den_rank_max": det_full_plane_den_rank_max,
        "two_exchange_det_full_plane_slope_max": det_full_plane_slope_max,
        "two_exchange_det_full_plane_aperiodic_max": det_full_plane_aperiodic_max,
        "two_exchange_det_full_plane_lifts": det_full_plane_lifts,
        "two_exchange_det_proper_lines": det_proper_lines,
        "two_exchange_det_proper_line_fixed_root": det_proper_line_fixed_root,
        "two_exchange_det_proper_line_product_mobius": (
            det_proper_line_product_mobius
        ),
        "two_exchange_det_proper_line_sum_mobius": det_proper_line_sum_mobius,
        "two_exchange_det_proper_line_constant_slope": (
            det_proper_line_constant_slope
        ),
        "two_exchange_det_proper_line_variable_slope": (
            det_proper_line_variable_slope
        ),
        "two_exchange_det_proper_line_slope_max": det_proper_line_slope_max,
        "two_exchange_det_proper_line_aperiodic_max": (
            det_proper_line_aperiodic_max
        ),
        "two_exchange_det_proper_line_core_max": det_proper_line_core_max,
        "two_exchange_det_proper_line_variable_injective": (
            det_proper_line_variable_injective
        ),
        "two_exchange_det_proper_line_variable_pole_max": (
            det_proper_line_variable_pole_max
        ),
        "two_exchange_det_proper_line_variable_aperiodic_slope_max": (
            det_proper_line_variable_aperiodic_slope_max
        ),
        "two_exchange_det_proper_line_variable_injective_checks": (
            det_proper_line_variable_injective_checks
        ),
        "two_exchange_det_proper_line_variable_aperiodic_slopes": len(
            det_proper_line_variable_aperiodic_slopes
        ),
        "two_exchange_det_proper_line_variable_new_slopes": len(
            det_proper_line_variable_new_slopes
        ),
        "two_exchange_det_proper_line_variable_new_slope_max": (
            det_proper_line_variable_new_slope_max
        ),
        "two_exchange_det_proper_line_variable_nonfixed": (
            det_proper_line_variable_nonfixed
        ),
        "two_exchange_det_proper_line_variable_anchored": (
            det_proper_line_variable_anchored
        ),
        "two_exchange_det_proper_line_variable_unanchored": (
            det_proper_line_variable_unanchored
        ),
        "two_exchange_det_proper_line_variable_domain_pair_max": (
            det_proper_line_variable_domain_pair_max
        ),
        "two_exchange_det_proper_line_variable_domain_pair_checks": (
            det_proper_line_variable_domain_pair_checks
        ),
        "two_exchange_det_proper_line_variable_charged_slope_checks": (
            det_proper_line_variable_charged_slope_checks
        ),
    }


def root_slice_profile(
    locator_rows: list[tuple[tuple[int, ...], int]],
    domain: tuple[int, ...],
    u: tuple[int, ...],
    v: tuple[int, ...],
    f: dict[int, int],
    g: dict[int, int],
    k: int,
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
            "root_slice_new_slope_count": 0,
            "root_slice_total_slope_bound": 0,
            "root_slice_t3_core_locators": 0,
            "root_slice_t3_slope_count": 0,
            "root_slice_t3_new_slope_count": 0,
            "root_slice_recursive_slope_bound": 0,
            "root_slice_members": 0,
            "root_slice_residual_locators": len(locator_rows),
            "root_slice_residual_slopes": len({slope for _, slope in locator_rows}),
            "root_slice_residual_max_slope_fiber": max(slope_fibers.values(), default=0),
            "root_slice_residual_slope_core_checks": 0,
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
            "root_slice_residual_top_packet_overlap_pairs": 0,
            "root_slice_residual_top_packet_overlap_max": 0,
            "root_slice_residual_components": 0,
            "root_slice_residual_nontrivial_components": 0,
            "root_slice_residual_isolated_components": 0,
            "root_slice_residual_boundary_isolated_components": 0,
            "root_slice_residual_component_max": 0,
            "root_slice_residual_component_clique_edges": 0,
            "root_slice_residual_common_companion_checks": 0,
            "root_slice_residual_top_lift_gate_checks": 0,
            "root_slice_residual_top_anchor_checks": 0,
            "root_slice_residual_top_common_lift_gate_checks": 0,
            "root_slice_residual_top_numerator_anchor_checks": 0,
            "root_slice_residual_top_face_gate_checks": 0,
            "root_slice_residual_top_face_noncontained": 0,
            "root_slice_residual_top_face_aperiodic": 0,
            "root_slice_residual_top_face_residual": 0,
            "root_slice_residual_top_face_peeled": 0,
            "root_slice_residual_anchor_lifted_faces": 0,
            "root_slice_residual_anchor_escape_locators": 0,
            "root_slice_residual_anchor_beta0_zero": 0,
            "root_slice_residual_anchor_in_support": 0,
            "root_slice_residual_anchor_outside_domain": 0,
            "root_slice_residual_external_anchors": 0,
            "root_slice_residual_external_anchor_values": (),
            "root_slice_residual_external_anchor_locator_max": 0,
            "root_slice_residual_external_anchor_slope_max": 0,
            "root_slice_residual_external_anchor_slope_fibers": 0,
            "root_slice_residual_external_anchor_slope_fiber_max": 0,
            "root_slice_residual_external_anchor_slope_core_checks": 0,
            "root_slice_residual_external_anchor_kernel_dim_max": 0,
            "root_slice_residual_external_anchor_projective_points": 0,
            "root_slice_residual_external_anchor_rich_points": 0,
            "root_slice_residual_external_anchor_finite_rich_slopes": 0,
            "root_slice_residual_external_anchor_rich_residual_classes": 0,
            "root_slice_residual_external_anchor_twist_checks": 0,
            "root_slice_residual_external_anchor_interpolation_checks": 0,
            "root_slice_residual_external_anchor_pinned_t1_checks": 0,
            "root_slice_residual_anchor_lift_gate_checks": 0,
            "root_slice_residual_anchor_isolated_checks": 0,
            "root_slice_residual_anchor_projective_lift_checks": 0,
            "root_slice_residual_anchor_projective_unique_checks": 0,
            "root_slice_residual_projective_lift_fibers": 0,
            "root_slice_residual_projective_squarefree_fibers": 0,
            "root_slice_residual_projective_boundary_fibers": 0,
            "root_slice_residual_projective_boundary_singletons": 0,
            "root_slice_residual_projective_lift_fiber_max": 0,
            "root_slice_residual_projective_lift_pair_checks": 0,
            "root_slice_residual_anchor_finite_lift_checks": 0,
            "root_slice_residual_anchor_repeated_lift_checks": 0,
            "root_slice_residual_anchor_offdomain_lift_checks": 0,
            "root_slice_residual_anchor_infinity_checks": 0,
            "root_slice_residual_lifted_slopes": 0,
            "root_slice_residual_escape_slopes": 0,
            "root_slice_residual_lifted_escape_slope_overlap": 0,
            "root_slice_residual_escape_new_slopes": 0,
            "root_slice_residual_lifted_core_slope_bound": 0,
            "root_slice_residual_recursion_bound": 0,
            "root_slice_residual_new_escape_bound": 0,
            "root_slice_residual_active_new_escape_bound": 0,
            "root_slice_residual_active_face_new_escape_bound": 0,
            "root_slice_residual_boundary_arrangement_bound": 0,
            "root_slice_residual_boundary_slope_bound": 0,
            "root_slice_residual_boundary_active_anchors": 0,
            "root_slice_residual_boundary_anchor_slope_bound": 0,
            "root_slice_residual_boundary_field_slope_bound": 0,
            "root_slice_residual_active_lifted_core_slope_bound": 0,
            "root_slice_recursive_arrangement_bound": 0,
            "root_slice_recursive_boundary_slope_bound": 0,
            "root_slice_recursive_boundary_anchor_slope_bound": 0,
            "root_slice_recursive_boundary_field_slope_bound": 0,
            "root_slice_recursive_active_field_slope_bound": 0,
            "root_slice_recursive_new_escape_bound": 0,
            "root_slice_recursive_active_new_escape_bound": 0,
            "root_slice_recursive_active_face_new_escape_bound": 0,
            "root_slice_exact_active_face_bound": 0,
            "root_slice_recursive_active_face_new_root_bound": 0,
            "root_slice_two_input_field_bound": 0,
            "root_slice_lifted_u_t1_cores": 0,
            "root_slice_lifted_v_t1_cores": 0,
            "root_slice_lifted_common_cores": 0,
            "root_slice_lifted_common_active_cores": 0,
            "root_slice_lifted_common_inactive_cores": 0,
            "root_slice_lifted_common_core_noncontained_faces": 0,
            "root_slice_lifted_common_core_aperiodic_faces": 0,
            "root_slice_lifted_common_core_residual_faces": 0,
            "root_slice_lifted_common_core_peeled_faces": 0,
            "root_slice_lifted_common_core_residual_singletons": 0,
            "root_slice_lifted_common_core_residual_packets": 0,
            "root_slice_lifted_common_core_max_residual_faces": 0,
            "root_slice_lifted_common_core_common_base_checks": 0,
            "root_slice_lifted_common_core_residual_slope_checks": 0,
            "root_slice_lifted_common_core_active_ratio_checks": 0,
            "root_slice_lifted_common_core_residual_slope_pair_checks": 0,
            "root_slice_lifted_common_core_residual_slope_fiber_max": 0,
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

    root_slice_t3_slope_set: set[int] = set()
    root_slice_t3_core_locators = 0
    for core in combinations(domain, j - 1):
        core_locator = locator(tuple(sorted(core)), p)
        t3_a = hankel_apply(u, 3, j - 1, core_locator, p)
        t3_b = hankel_apply(v, 3, j - 1, core_locator, p)
        t3_slope = slope_from_gate(t3_a, t3_b, p)
        if t3_slope is None:
            continue
        root_slice_t3_core_locators += 1
        root_slice_t3_slope_set.add(t3_slope)

    max_noncontained = 0
    max_aperiodic_members = 0
    root_slice_members: set[tuple[int, ...]] = set()
    for core, slope in slice_keys:
        core_locator = locator(core, p)
        t3_a = hankel_apply(u, 3, j - 1, core_locator, p)
        t3_b = hankel_apply(v, 3, j - 1, core_locator, p)
        if slope_from_gate(t3_a, t3_b, p) != slope:
            raise AssertionError("root-slice slope missed the t=3 core-locator gate")
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
    residual_index = {
        tuple(sorted(complement)): idx for idx, (complement, _) in enumerate(residual_rows)
    }
    residual_same_slope_edges = 0
    residual_strict_pairs = 0
    residual_degrees = [0] * len(residual_rows)
    residual_adj = [set() for _ in residual_rows]
    residual_top_packets: dict[tuple[int, ...], set[int]] = {}
    residual_slope_fibers: dict[int, int] = {}
    residual_slope_indices: dict[int, list[int]] = {}
    for idx, (_, slope) in enumerate(residual_rows):
        residual_slope_fibers[slope] = residual_slope_fibers.get(slope, 0) + 1
        residual_slope_indices.setdefault(slope, []).append(idx)
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
    residual_slope_core_checks = 0
    for fiber_indices in residual_slope_indices.values():
        if len(fiber_indices) * j > comb(len(domain), j - 1):
            raise AssertionError("residual slope fiber exceeded packing bound")
        seen_cores: set[tuple[int, ...]] = set()
        for idx in fiber_indices:
            for core in combinations(residual_rows[idx][0], j - 1):
                core_key = tuple(sorted(core))
                if core_key in seen_cores:
                    raise AssertionError("residual slope fiber had a one-exchange pair")
                seen_cores.add(core_key)
                residual_slope_core_checks += 1
    if max(residual_degrees, default=0) > j:
        raise AssertionError("residual one-exchange degree exceeded the t=2 core bound")

    common_companion_checks = 0
    for left, (complement, _) in enumerate(residual_rows):
        left_set = set(complement)
        ell = locator(complement, p)
        b_vec = hankel_apply(v, t, j, ell, p)
        added_roots = set()
        for right in residual_adj[left]:
            right_set = set(residual_rows[right][0])
            added = tuple(right_set - left_set)
            if len(added) != 1:
                raise AssertionError("residual edge did not have one added root")
            added_roots.add(added[0])
            if b_vec[0] == 0:
                raise AssertionError("residual edge had no finite common companion anchor")
            anchor = b_vec[1] * inv_mod(b_vec[0], p) % p
            if added[0] != anchor:
                raise AssertionError("residual edge did not use the common companion anchor")
            common_companion_checks += 1
        if len(added_roots) > 1:
            raise AssertionError("residual locator used more than one companion anchor")

    domain_set = set(domain)
    residual_anchor_lifted_faces = 0
    residual_anchor_escape_beta0_zero = 0
    residual_anchor_escape_in_support = 0
    residual_anchor_escape_outside_domain = 0
    residual_anchor_lift_gate_checks = 0
    residual_anchor_isolated_checks = 0
    residual_anchor_projective_lift_checks = 0
    residual_anchor_projective_unique_checks = 0
    residual_anchor_finite_lift_checks = 0
    residual_anchor_repeated_lift_checks = 0
    residual_anchor_offdomain_lift_checks = 0
    residual_anchor_infinity_checks = 0
    residual_projective_lift_keys: list[tuple[int, ...] | None] = [None] * len(residual_rows)
    residual_projective_lift_squarefree_indices: set[int] = set()
    residual_projective_lift_boundary_indices: set[int] = set()
    residual_external_anchor_locators: dict[int, int] = {}
    residual_external_anchor_slopes: dict[int, set[int]] = {}
    residual_external_anchor_slope_locators: dict[tuple[int, int], int] = {}
    residual_external_anchor_slope_indices: dict[tuple[int, int], list[int]] = {}
    residual_external_anchor_projective_classes: dict[int, set[tuple[int, ...]]] = {}
    residual_repeated_anchor_locators: dict[int, int] = {}
    residual_repeated_anchor_slopes: dict[int, set[int]] = {}
    residual_repeated_anchor_projective_classes: dict[int, set[tuple[int, ...]]] = {}
    residual_infinity_slopes: set[int] = set()
    residual_infinity_projective_classes: set[tuple[int, ...]] = set()
    residual_external_anchor_slope_core_checks = 0
    residual_external_anchor_kernel_dim_max = 0
    residual_external_anchor_projective_points = 0
    residual_external_anchor_rich_points = 0
    residual_external_anchor_finite_rich_slopes = 0
    residual_external_anchor_rich_residual_classes = 0
    residual_external_anchor_twist_checks = 0
    residual_external_anchor_interpolation_checks = 0
    residual_external_anchor_pinned_t1_checks = 0
    residual_boundary_arrangement_bound = 0
    residual_boundary_slope_arrangement_bound = 0
    external_twist_syndromes: dict[int, tuple[tuple[int, ...], tuple[int, ...]]] = {}
    residual_anchor_lifted_face_indices: set[int] = set()
    residual_anchor_escape_indices: set[int] = set()
    for idx, (complement, line_slope) in enumerate(residual_rows):
        complement_set = set(complement)
        complement_locator = locator(complement, p)
        a_vec = hankel_apply(u, t, j, complement_locator, p)
        b_vec = hankel_apply(v, t, j, complement_locator, p)
        if all(value == 0 for value in b_vec):
            raise AssertionError("residual locator was contained in projective lift ledger")
        shift_vec = [0] + complement_locator
        pad_vec = complement_locator + [0]
        projective_lift = [
            (b_vec[0] * shift_vec[col] - b_vec[1] * pad_vec[col]) % p
            for col in range(j + 2)
        ]
        if all(value == 0 for value in projective_lift):
            raise AssertionError("projective residual lift vanished")
        residual_projective_lift_keys[idx] = normalize_projective_vector(projective_lift, p)
        if hankel_apply(v, 1, j + 1, projective_lift, p)[0] != 0:
            raise AssertionError("projective residual lift missed denominator gate")
        if hankel_apply(u, 1, j + 1, projective_lift, p)[0] != 0:
            raise AssertionError("projective residual lift missed numerator gate")
        residual_anchor_projective_lift_checks += 1
        projective_kernel_anchors: list[tuple[str, int | None]] = []
        for finite_anchor in range(p):
            finite_lift = [
                (shift_vec[col] - finite_anchor * pad_vec[col]) % p
                for col in range(j + 2)
            ]
            if (
                hankel_apply(v, 1, j + 1, finite_lift, p)[0] == 0
                and hankel_apply(u, 1, j + 1, finite_lift, p)[0] == 0
            ):
                projective_kernel_anchors.append(("finite", finite_anchor))
        if (
            hankel_apply(v, 1, j + 1, pad_vec, p)[0] == 0
            and hankel_apply(u, 1, j + 1, pad_vec, p)[0] == 0
        ):
            projective_kernel_anchors.append(("infinity", None))
        if len(projective_kernel_anchors) != 1:
            raise AssertionError("residual projective lift pencil was not unique")
        expected_anchor = (
            ("infinity", None)
            if b_vec[0] == 0
            else ("finite", b_vec[1] * inv_mod(b_vec[0], p) % p)
        )
        if projective_kernel_anchors[0] != expected_anchor:
            raise AssertionError("unique projective anchor disagreed with beta ratio")
        residual_anchor_projective_unique_checks += 1
        if b_vec[0] == 0:
            residual_anchor_escape_beta0_zero += 1
            residual_anchor_escape_indices.add(idx)
            residual_projective_lift_boundary_indices.add(idx)
            if a_vec[0] != 0 or b_vec[1] == 0:
                raise AssertionError("infinity anchor did not have the expected first-row gate")
            infinity_slope = (-a_vec[1] * inv_mod(b_vec[1], p)) % p
            if infinity_slope != line_slope:
                raise AssertionError("infinity-anchor shifted one-row slope disagreed")
            shifted_line = tuple(
                (u[row + 1] + line_slope * v[row + 1]) % p for row in range(j + 1)
            )
            if hankel_apply(shifted_line, 1, j, complement_locator, p)[0] != 0:
                raise AssertionError("infinity-anchor shifted one-row gate failed")
            residual_infinity_slopes.add(line_slope)
            residual_infinity_projective_classes.add(
                normalize_projective_vector(complement_locator, p)
            )
            if residual_adj[idx]:
                raise AssertionError("beta0-zero anchor escape had a residual neighbor")
            residual_anchor_infinity_checks += 1
            residual_anchor_isolated_checks += 1
            continue
        anchor = b_vec[1] * inv_mod(b_vec[0], p) % p
        top_packet = tuple(sorted(complement + (anchor,)))
        top_locator = locator(top_packet, p)
        if hankel_apply(v, 1, j + 1, top_locator, p)[0] != 0:
            raise AssertionError("finite residual anchor missed denominator lift gate")
        if (b_vec[1] - anchor * b_vec[0]) % p != 0:
            raise AssertionError("finite residual anchor missed denominator anchor")
        if hankel_apply(u, 1, j + 1, top_locator, p)[0] != 0:
            raise AssertionError("finite residual anchor missed numerator lift gate")
        if (a_vec[1] - anchor * a_vec[0]) % p != 0:
            raise AssertionError("finite residual anchor missed numerator anchor")
        residual_anchor_finite_lift_checks += 1
        if anchor in complement_set:
            residual_anchor_escape_in_support += 1
            residual_anchor_escape_indices.add(idx)
            residual_projective_lift_boundary_indices.add(idx)
            repeated_twisted_f = {
                x: 0 if x == anchor else f[x] * inv_mod((x - anchor) % p, p) % p
                for x in domain
            }
            repeated_twisted_g = {
                x: 0 if x == anchor else g[x] * inv_mod((x - anchor) % p, p) % p
                for x in domain
            }
            repeated_twisted_u = syndrome(repeated_twisted_f, domain, j + 2, p)
            repeated_twisted_v = syndrome(repeated_twisted_g, domain, j + 2, p)
            repeated_twisted_a = hankel_apply(repeated_twisted_u, 1, j + 1, top_locator, p)
            repeated_twisted_b = hankel_apply(repeated_twisted_v, 1, j + 1, top_locator, p)
            if repeated_twisted_a[0] != a_vec[0] or repeated_twisted_b[0] != b_vec[0]:
                raise AssertionError("repeated-anchor twist did not recover first row")
            repeated_twisted_slope = slope_from_gate(repeated_twisted_a, repeated_twisted_b, p)
            if repeated_twisted_b[0] == 0:
                raise AssertionError("repeated-anchor twisted denominator vanished")
            if repeated_twisted_slope != line_slope:
                raise AssertionError("repeated-anchor twist changed the residual slope")
            repeated_twisted_line = tuple(
                (repeated_twisted_u[row] + line_slope * repeated_twisted_v[row]) % p
                for row in range(j + 2)
            )
            if hankel_apply(repeated_twisted_line, 1, j + 1, top_locator, p)[0] != 0:
                raise AssertionError("repeated-anchor slope missed pinned t=1 gate")
            residual_repeated_anchor_locators[anchor] = (
                residual_repeated_anchor_locators.get(anchor, 0) + 1
            )
            residual_repeated_anchor_slopes.setdefault(anchor, set()).add(line_slope)
            residual_repeated_anchor_projective_classes.setdefault(anchor, set()).add(
                normalize_projective_vector(top_locator, p)
            )
            residual_anchor_repeated_lift_checks += 1
            if residual_adj[idx]:
                raise AssertionError("in-support anchor escape had a residual neighbor")
            residual_anchor_isolated_checks += 1
            continue
        if anchor not in domain_set:
            residual_anchor_escape_outside_domain += 1
            residual_anchor_escape_indices.add(idx)
            residual_projective_lift_boundary_indices.add(idx)
            residual_external_anchor_locators[anchor] = (
                residual_external_anchor_locators.get(anchor, 0) + 1
            )
            residual_external_anchor_slopes.setdefault(anchor, set()).add(line_slope)
            anchor_slope_key = (anchor, line_slope)
            residual_external_anchor_slope_locators[anchor_slope_key] = (
                residual_external_anchor_slope_locators.get(anchor_slope_key, 0) + 1
            )
            residual_external_anchor_slope_indices.setdefault(anchor_slope_key, []).append(idx)
            residual_external_anchor_projective_classes.setdefault(anchor, set()).add(
                normalize_projective_vector(top_locator, p)
            )
            if anchor not in external_twist_syndromes:
                twisted_f = {
                    x: f[x] * inv_mod((x - anchor) % p, p) % p
                    for x in domain
                }
                twisted_g = {
                    x: g[x] * inv_mod((x - anchor) % p, p) % p
                    for x in domain
                }
                external_twist_syndromes[anchor] = (
                    syndrome(twisted_f, domain, j + 2, p),
                    syndrome(twisted_g, domain, j + 2, p),
                )
            twisted_u, twisted_v = external_twist_syndromes[anchor]
            twisted_a = hankel_apply(twisted_u, 1, j + 1, top_locator, p)
            twisted_b = hankel_apply(twisted_v, 1, j + 1, top_locator, p)
            if twisted_a[0] != a_vec[0] or twisted_b[0] != b_vec[0]:
                raise AssertionError("external-anchor twist did not recover first row")
            twisted_slope = slope_from_gate(twisted_a, twisted_b, p)
            if twisted_b[0] == 0:
                raise AssertionError("external-anchor twisted denominator vanished")
            if twisted_slope != line_slope:
                raise AssertionError("external-anchor twist changed the residual slope")
            twisted_line = tuple(
                (twisted_u[row] + line_slope * twisted_v[row]) % p
                for row in range(j + 2)
            )
            if hankel_apply(twisted_line, 1, j + 1, top_locator, p)[0] != 0:
                raise AssertionError("external-anchor slope missed pinned t=1 gate")
            residual_external_anchor_pinned_t1_checks += 1
            residual_external_anchor_twist_checks += 1
            support = tuple(x for x in domain if x not in complement_set)
            if len(support) != k + 2:
                raise AssertionError("external-anchor support had wrong size")
            support_sum = sum(support) % p
            f_interp = interpolate(support, tuple(f[x] for x in support), p)
            g_interp = interpolate(support, tuple(g[x] for x in support), p)
            f_top = coeff_at(f_interp, k + 1)
            g_top = coeff_at(g_interp, k + 1)
            if f_top != a_vec[0] or g_top != b_vec[0]:
                raise AssertionError("external-anchor top coefficient missed first row")
            if coeff_at(f_interp, k) != ((anchor - support_sum) * f_top) % p:
                raise AssertionError("external-anchor f top coefficients were not locked")
            if coeff_at(g_interp, k) != ((anchor - support_sum) * g_top) % p:
                raise AssertionError("external-anchor g top coefficients were not locked")
            line_interp = interpolate(
                support,
                tuple((f[x] + line_slope * g[x]) % p for x in support),
                p,
            )
            if coeff_at(line_interp, k + 1) != 0 or coeff_at(line_interp, k) != 0:
                raise AssertionError("external-anchor slope did not cancel top coefficients")
            if poly_degree(line_interp) >= k:
                raise AssertionError("external-anchor line did not drop below degree k")
            residual_external_anchor_interpolation_checks += 1
            residual_anchor_offdomain_lift_checks += 1
            if residual_adj[idx]:
                raise AssertionError("outside-domain anchor escape had a residual neighbor")
            residual_anchor_isolated_checks += 1
            continue
        residual_anchor_lift_gate_checks += 1
        residual_anchor_lifted_faces += 1
        residual_anchor_lifted_face_indices.add(idx)
        residual_projective_lift_squarefree_indices.add(idx)

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
    top_packet_vertex_sets = list(residual_top_packets.values())
    top_lift_gate_checks = 0
    top_anchor_checks = 0
    top_common_lift_gate_checks = 0
    top_numerator_anchor_checks = 0
    top_face_gate_checks = 0
    top_face_noncontained = 0
    top_face_aperiodic = 0
    top_face_residual = 0
    top_face_peeled = 0
    for top_packet, vertices in residual_top_packets.items():
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
        top_locator = locator(top_packet, p)
        top_denominator_gate = hankel_apply(v, 1, j + 1, top_locator, p)[0]
        if top_denominator_gate != 0:
            raise AssertionError("residual top packet failed the denominator lift gate")
        top_lift_gate_checks += 1
        top_numerator_gate = hankel_apply(u, 1, j + 1, top_locator, p)[0]
        if top_numerator_gate != 0:
            raise AssertionError("residual top packet failed the numerator lift gate")
        top_common_lift_gate_checks += 1
        residual_faces_in_packet = 0
        for omitted_root in top_packet:
            face = tuple(sorted(set(top_packet) - {omitted_root}))
            face_locator = locator(face, p)
            a_vec = hankel_apply(u, t, j, face_locator, p)
            b_vec = hankel_apply(v, t, j, face_locator, p)
            if (b_vec[1] - omitted_root * b_vec[0]) % p != 0:
                raise AssertionError("lifted top face failed the denominator anchor")
            if (a_vec[1] - omitted_root * a_vec[0]) % p != 0:
                raise AssertionError("lifted top face failed the numerator anchor")
            if not determinant_gate_t2(a_vec, b_vec, p):
                raise AssertionError("lifted top face failed the determinant gate")
            top_face_gate_checks += 1
            if all(value == 0 for value in b_vec):
                continue
            top_face_noncontained += 1
            slope = slope_from_gate(a_vec, b_vec, p)
            if slope is None:
                raise AssertionError("noncontained lifted top face had no slope")
            if face in row_map:
                if row_map[face] != slope:
                    raise AssertionError("lifted top face slope disagreed with aperiodic row")
                top_face_aperiodic += 1
            if face in root_slice_members:
                top_face_peeled += 1
            residual_idx = residual_index.get(face)
            if residual_idx is not None:
                if residual_idx not in vertices:
                    raise AssertionError("residual face was assigned to the wrong top packet")
                residual_faces_in_packet += 1
                top_face_residual += 1
        if residual_faces_in_packet != size:
            raise AssertionError("top packet vertices did not match residual lifted faces")
        for idx in vertices:
            complement = residual_rows[idx][0]
            omitted = tuple(set(top_packet) - set(complement))
            if len(omitted) != 1:
                raise AssertionError("residual top-packet vertex had wrong omitted root")
            omitted_root = omitted[0]
            complement_locator = locator(complement, p)
            b_vec = hankel_apply(v, t, j, complement_locator, p)
            if b_vec[0] == 0:
                raise AssertionError("residual top-packet anchor was not finite")
            anchor = b_vec[1] * inv_mod(b_vec[0], p) % p
            if anchor != omitted_root:
                raise AssertionError("residual top-packet anchor missed omitted root")
            top_anchor_checks += 1
            a_vec = hankel_apply(u, t, j, complement_locator, p)
            if (a_vec[1] - omitted_root * a_vec[0]) % p != 0:
                raise AssertionError("residual top-packet numerator anchor missed omitted root")
            top_numerator_anchor_checks += 1
            top_packet_degrees[idx] += size - 1
            top_packet_incidences[idx] += 1
    if top_packet_edges != residual_strict_pairs:
        raise AssertionError("residual top-packet edge ledger was not exact")
    if top_packet_triangles != residual_top_triangles:
        raise AssertionError("residual top-packet triangle ledger was not exact")
    if top_packet_degrees != residual_degrees:
        raise AssertionError("residual top-packet degree ledger was not exact")

    lifted_common_cores = 0
    lifted_common_core_noncontained_faces = 0
    lifted_common_core_aperiodic_faces = 0
    lifted_common_core_residual_faces = 0
    lifted_common_core_peeled_faces = 0
    lifted_common_core_residual_singletons = 0
    lifted_common_core_residual_packets = 0
    lifted_common_core_max_residual_faces = 0
    lifted_common_core_common_base_checks = 0
    lifted_common_core_residual_slope_checks = 0
    lifted_common_core_active_ratio_checks = 0
    lifted_common_core_residual_slope_pair_checks = 0
    lifted_common_core_residual_slope_fiber_max = 0
    lifted_common_core_residual_face_indices: set[int] = set()
    lifted_common_core_active_ratio_slope_set: set[int] = set()
    lifted_u_t1_cores = 0
    lifted_v_t1_cores = 0
    for core in combinations(domain, j + 1):
        core_key = tuple(sorted(core))
        core_locator = locator(core_key, p)
        u_t1_core = hankel_apply(u, 1, j + 1, core_locator, p)[0] == 0
        v_t1_core = hankel_apply(v, 1, j + 1, core_locator, p)[0] == 0
        if u_t1_core:
            lifted_u_t1_cores += 1
        if v_t1_core:
            lifted_v_t1_cores += 1
        if not u_t1_core:
            continue
        if not v_t1_core:
            continue
        lifted_common_cores += 1
        base_support = tuple(x for x in domain if x not in set(core_key))
        if len(base_support) != k + 1:
            raise AssertionError("lifted common core had wrong base support size")
        if not is_explained_on_support(f, base_support, k, p):
            raise AssertionError("lifted common core was not an f common base")
        if not is_explained_on_support(g, base_support, k, p):
            raise AssertionError("lifted common core was not a g common base")
        f_base = interpolate(base_support[:k], tuple(f[x] for x in base_support[:k]), p)
        g_base = interpolate(base_support[:k], tuple(g[x] for x in base_support[:k]), p)
        lifted_common_core_common_base_checks += 1
        residual_face_indices = set()
        residual_face_slopes = []
        noncontained_faces = 0
        aperiodic_faces = 0
        peeled_faces = 0
        for omitted_root in core_key:
            face = tuple(sorted(set(core_key) - {omitted_root}))
            face_locator = locator(face, p)
            a_vec = hankel_apply(u, t, j, face_locator, p)
            b_vec = hankel_apply(v, t, j, face_locator, p)
            if (b_vec[1] - omitted_root * b_vec[0]) % p != 0:
                raise AssertionError("lifted common core face failed denominator anchor")
            if (a_vec[1] - omitted_root * a_vec[0]) % p != 0:
                raise AssertionError("lifted common core face failed numerator anchor")
            if not determinant_gate_t2(a_vec, b_vec, p):
                raise AssertionError("lifted common core face failed determinant gate")
            if all(value == 0 for value in b_vec):
                residual_g = (g[omitted_root] - poly_eval(g_base, omitted_root, p)) % p
                if residual_g != 0:
                    raise AssertionError("contained lifted common face had nonzero g residual")
                continue
            noncontained_faces += 1
            slope = slope_from_gate(a_vec, b_vec, p)
            if slope is None:
                raise AssertionError("noncontained lifted common face had no slope")
            residual_f = (f[omitted_root] - poly_eval(f_base, omitted_root, p)) % p
            residual_g = (g[omitted_root] - poly_eval(g_base, omitted_root, p)) % p
            if residual_g == 0:
                raise AssertionError("noncontained lifted common face had zero g residual")
            residual_slope = (-residual_f * inv_mod(residual_g, p)) % p
            if slope != residual_slope:
                raise AssertionError("lifted common face slope was not the residual slope")
            lifted_common_core_residual_slope_checks += 1
            if face in row_map:
                if row_map[face] != slope:
                    raise AssertionError("lifted common face slope disagreed with row map")
                aperiodic_faces += 1
            if face in root_slice_members:
                peeled_faces += 1
            residual_idx = residual_index.get(face)
            if residual_idx is not None:
                residual_face_indices.add(residual_idx)
                residual_face_slopes.append(slope)
                lifted_common_core_residual_face_indices.add(residual_idx)
                lifted_common_core_active_ratio_checks += 1
                lifted_common_core_active_ratio_slope_set.add(slope)
        residual_face_count = len(residual_face_indices)
        if residual_face_count != len(residual_face_slopes):
            raise AssertionError("lifted common core residual slope ledger lost a face")
        if len(set(residual_face_slopes)) != residual_face_count:
            raise AssertionError("lifted common core had a repeated residual slope")
        lifted_common_core_residual_slope_pair_checks += (
            residual_face_count * (residual_face_count - 1) // 2
        )
        for residual_slope in set(residual_face_slopes):
            lifted_common_core_residual_slope_fiber_max = max(
                lifted_common_core_residual_slope_fiber_max,
                residual_face_slopes.count(residual_slope),
            )
        lifted_common_core_noncontained_faces += noncontained_faces
        lifted_common_core_aperiodic_faces += aperiodic_faces
        lifted_common_core_residual_faces += residual_face_count
        lifted_common_core_peeled_faces += peeled_faces
        lifted_common_core_max_residual_faces = max(
            lifted_common_core_max_residual_faces, residual_face_count
        )
        if residual_face_count == 1:
            lifted_common_core_residual_singletons += 1
        elif residual_face_count >= 2:
            lifted_common_core_residual_packets += 1
            if core_key not in residual_top_packets:
                raise AssertionError("lifted common core with two residual faces was not a packet")
            if residual_face_indices != residual_top_packets[core_key]:
                raise AssertionError("lifted common core residual faces disagreed with packet")
    if lifted_common_core_residual_packets != len(residual_top_packets):
        raise AssertionError("residual top packets were not exactly lifted common packets")
    residual_anchor_escape_locators = (
        residual_anchor_escape_beta0_zero
        + residual_anchor_escape_in_support
        + residual_anchor_escape_outside_domain
    )
    if residual_anchor_lifted_faces != lifted_common_core_residual_faces:
        raise AssertionError("anchor-lifted face count missed lifted common residual faces")
    if residual_anchor_lifted_face_indices != lifted_common_core_residual_face_indices:
        raise AssertionError("anchor-lifted faces disagreed with lifted common residual faces")
    if len(lifted_common_core_residual_face_indices) != lifted_common_core_residual_faces:
        raise AssertionError("a lifted residual face was counted by two active common cores")
    if lifted_common_core_active_ratio_checks != lifted_common_core_residual_faces:
        raise AssertionError("active residual-ratio ledger lost a lifted common face")
    if residual_anchor_lifted_faces + residual_anchor_escape_locators != len(residual_rows):
        raise AssertionError("residual anchor ledger did not partition residual locators")
    if residual_anchor_projective_lift_checks != len(residual_rows):
        raise AssertionError("projective lift ledger did not cover every residual locator")
    if residual_anchor_projective_unique_checks != len(residual_rows):
        raise AssertionError("projective uniqueness ledger did not cover every residual locator")
    if residual_anchor_finite_lift_checks != (
        residual_anchor_lifted_faces
        + residual_anchor_escape_in_support
        + residual_anchor_escape_outside_domain
    ):
        raise AssertionError("finite residual-anchor lifts did not match finite anchors")
    if residual_anchor_repeated_lift_checks != residual_anchor_escape_in_support:
        raise AssertionError("repeated-root lift ledger missed in-support escapes")
    if residual_anchor_offdomain_lift_checks != residual_anchor_escape_outside_domain:
        raise AssertionError("off-domain lift ledger missed outside-domain escapes")
    if residual_anchor_infinity_checks != residual_anchor_escape_beta0_zero:
        raise AssertionError("infinity-anchor ledger missed beta0-zero escapes")
    if sum(residual_external_anchor_slope_locators.values()) != residual_anchor_escape_outside_domain:
        raise AssertionError("external-anchor slope fibers missed off-domain escapes")
    if len(residual_external_anchor_slope_locators) != sum(
        len(slopes) for slopes in residual_external_anchor_slopes.values()
    ):
        raise AssertionError("external-anchor slope fiber keys disagreed with slope image")
    if set(residual_external_anchor_slope_locators) != set(residual_external_anchor_slope_indices):
        raise AssertionError("external-anchor slope fiber indices missed a fiber")
    for fiber_indices in residual_external_anchor_slope_indices.values():
        if len(fiber_indices) * j > comb(len(domain), j - 1):
            raise AssertionError("external-anchor slope fiber exceeded packing bound")
        seen_cores: set[tuple[int, ...]] = set()
        for idx in fiber_indices:
            for core in combinations(residual_rows[idx][0], j - 1):
                core_key = tuple(sorted(core))
                if core_key in seen_cores:
                    raise AssertionError("external-anchor slope fiber had a one-exchange pair")
                seen_cores.add(core_key)
                residual_external_anchor_slope_core_checks += 1
    if set(residual_external_anchor_projective_classes) != set(residual_external_anchor_locators):
        raise AssertionError("external-anchor projective classes missed an anchor")
    for anchor, residual_classes in residual_external_anchor_projective_classes.items():
        kernel_rows = [
            tuple(pow(anchor, col, p) for col in range(j + 2)),
            tuple(u[col] for col in range(j + 2)),
            tuple(v[col] for col in range(j + 2)),
        ]
        kernel_basis = nullspace_basis(kernel_rows, p)
        residual_external_anchor_kernel_dim_max = max(
            residual_external_anchor_kernel_dim_max, len(kernel_basis)
        )
        projective_points = projective_span_points(kernel_basis, p)
        residual_external_anchor_projective_points += len(projective_points)
        twisted_u, twisted_v = external_twist_syndromes[anchor]
        rich_points: set[tuple[int, ...]] = set()
        finite_rich_slopes: set[int] = set()
        for point in projective_points:
            if poly_eval(list(point), anchor, p) != 0:
                raise AssertionError("fixed-anchor kernel point missed pinned root")
            if hankel_apply(u, 1, j + 1, list(point), p)[0] != 0:
                raise AssertionError("fixed-anchor kernel point missed numerator gate")
            if hankel_apply(v, 1, j + 1, list(point), p)[0] != 0:
                raise AssertionError("fixed-anchor kernel point missed denominator gate")
            root_set = tuple(x for x in domain if poly_eval(list(point), x, p) == 0)
            if len(root_set) != j:
                continue
            rich_points.add(point)
            twisted_b = hankel_apply(twisted_v, 1, j + 1, list(point), p)
            if twisted_b[0] == 0:
                continue
            twisted_a = hankel_apply(twisted_u, 1, j + 1, list(point), p)
            rich_slope = slope_from_gate(twisted_a, twisted_b, p)
            if rich_slope is None:
                raise AssertionError("finite rich point had no twisted slope")
            finite_rich_slopes.add(rich_slope)
        if not residual_classes <= rich_points:
            raise AssertionError("residual external classes were not rich arrangement points")
        if len(residual_classes) != residual_external_anchor_locators[anchor]:
            raise AssertionError("external-anchor projective classes were not injective")
        if not residual_external_anchor_slopes[anchor] <= finite_rich_slopes:
            raise AssertionError("residual external slopes escaped rich slope image")
        fixed_roots, root_hyperplane_weights = fixed_anchor_root_hyperplane_weights(
            kernel_basis, domain, p
        )
        if len(kernel_basis) == 1:
            rank_stratified_bound = 1
            rank_stratified_slope_bound = 1
        else:
            if fixed_roots >= j:
                raise AssertionError("fixed-anchor kernel had too many fixed roots")
            richness_deficit = j - fixed_roots
            if any(weight > richness_deficit for weight in root_hyperplane_weights.values()):
                raise AssertionError("fixed-anchor root hyperplane was overfull")
            rank_stratified_bound = fixed_anchor_rank_stratified_bound(
                root_hyperplane_weights, len(kernel_basis), richness_deficit, p
            )
            rank_stratified_slope_bound = fixed_anchor_rank_stratified_bound(
                root_hyperplane_weights,
                len(kernel_basis),
                richness_deficit,
                p,
                slope_image=True,
            )
        if len(rich_points) > rank_stratified_bound:
            raise AssertionError("fixed-anchor rich points exceeded rank-stratified bound")
        if len(finite_rich_slopes) > rank_stratified_bound:
            raise AssertionError("fixed-anchor slopes exceeded rank-stratified bound")
        if len(finite_rich_slopes) > rank_stratified_slope_bound:
            raise AssertionError("fixed-anchor slopes exceeded heavy-flat slope-image bound")
        if len(kernel_basis) == 1:
            if len(rich_points) > 1 or len(finite_rich_slopes) > 1:
                raise AssertionError("fixed-anchor projective point had too many rich slopes")
        if len(kernel_basis) == 2:
            fixed_roots = sum(
                all(poly_eval(list(vector), x, p) == 0 for vector in kernel_basis)
                for x in domain
            )
            if fixed_roots >= j:
                raise AssertionError("fixed-anchor pencil had too many fixed roots")
            pencil_bound = (len(domain) - fixed_roots) // (j - fixed_roots)
            if len(rich_points) > pencil_bound:
                raise AssertionError("fixed-anchor pencil exceeded rich-point bound")
            if len(finite_rich_slopes) > pencil_bound:
                raise AssertionError("fixed-anchor pencil exceeded rich-slope bound")
        if len(kernel_basis) == 3:
            fixed_roots = 0
            root_line_weights: dict[tuple[int, ...], int] = {}
            for x in domain:
                root_line = tuple(poly_eval(list(vector), x, p) for vector in kernel_basis)
                if all(value == 0 for value in root_line):
                    fixed_roots += 1
                    continue
                root_line_key = normalize_projective_vector(list(root_line), p)
                root_line_weights[root_line_key] = root_line_weights.get(root_line_key, 0) + 1
            if fixed_roots >= j:
                raise AssertionError("fixed-anchor plane had too many fixed roots")
            richness_deficit = j - fixed_roots
            heavy_root_lines = sum(
                1 for weight in root_line_weights.values() if weight >= richness_deficit
            )
            if any(weight > richness_deficit for weight in root_line_weights.values()):
                raise AssertionError("fixed-anchor plane root line was overfull")
            plane_bound = heavy_root_lines * (p + 1) + comb(len(root_line_weights), 2)
            if len(rich_points) > plane_bound:
                raise AssertionError("fixed-anchor plane exceeded rich-point bound")
            if len(finite_rich_slopes) > plane_bound:
                raise AssertionError("fixed-anchor plane exceeded rich-slope bound")
        if len(kernel_basis) == 4:
            fixed_roots = 0
            root_plane_weights: dict[tuple[int, ...], int] = {}
            for x in domain:
                root_plane = tuple(poly_eval(list(vector), x, p) for vector in kernel_basis)
                if all(value == 0 for value in root_plane):
                    fixed_roots += 1
                    continue
                root_plane_key = normalize_projective_vector(list(root_plane), p)
                root_plane_weights[root_plane_key] = root_plane_weights.get(root_plane_key, 0) + 1
            if fixed_roots >= j:
                raise AssertionError("fixed-anchor three-space had too many fixed roots")
            richness_deficit = j - fixed_roots
            if any(weight > richness_deficit for weight in root_plane_weights.values()):
                raise AssertionError("fixed-anchor three-space root plane was overfull")
            heavy_planes = sum(
                1 for weight in root_plane_weights.values() if weight == richness_deficit
            )
            root_plane_keys = tuple(root_plane_weights)
            heavy_line_keys: set[tuple[tuple[int, ...], ...]] = set()
            for left in range(len(root_plane_keys)):
                for right in range(left + 1, len(root_plane_keys)):
                    line_key = rowspace_key([root_plane_keys[left], root_plane_keys[right]], p)
                    line_weight = sum(
                        weight
                        for plane_key, weight in root_plane_weights.items()
                        if rowspace_key([*line_key, plane_key], p) == line_key
                    )
                    if line_weight >= richness_deficit:
                        heavy_line_keys.add(line_key)
            three_space_bound = (
                heavy_planes * (p * p + p + 1)
                + len(heavy_line_keys) * (p + 1)
                + comb(len(root_plane_keys), 3)
            )
            if len(rich_points) > three_space_bound:
                raise AssertionError("fixed-anchor three-space exceeded rich-point bound")
            if len(finite_rich_slopes) > three_space_bound:
                raise AssertionError("fixed-anchor three-space exceeded rich-slope bound")
        residual_external_anchor_rich_points += len(rich_points)
        residual_external_anchor_finite_rich_slopes += len(finite_rich_slopes)
        residual_external_anchor_rich_residual_classes += len(residual_classes)
        residual_boundary_arrangement_bound += rank_stratified_bound
        residual_boundary_slope_arrangement_bound += rank_stratified_slope_bound
    if set(residual_repeated_anchor_projective_classes) != set(residual_repeated_anchor_locators):
        raise AssertionError("repeated-anchor projective classes missed an anchor")
    for anchor, residual_classes in residual_repeated_anchor_projective_classes.items():
        repeated_twisted_f = {
            x: 0 if x == anchor else f[x] * inv_mod((x - anchor) % p, p) % p
            for x in domain
        }
        repeated_twisted_g = {
            x: 0 if x == anchor else g[x] * inv_mod((x - anchor) % p, p) % p
            for x in domain
        }
        repeated_twisted_u = syndrome(repeated_twisted_f, domain, j + 2, p)
        repeated_twisted_v = syndrome(repeated_twisted_g, domain, j + 2, p)
        repeated_kernel_rows = [
            tuple(pow(anchor, col, p) for col in range(j + 2)),
            tuple(
                0 if col == 0 else (col * pow(anchor, col - 1, p)) % p
                for col in range(j + 2)
            ),
            tuple(u[col] for col in range(j + 2)),
            tuple(v[col] for col in range(j + 2)),
        ]
        repeated_kernel_basis = nullspace_basis(repeated_kernel_rows, p)
        repeated_root_domain = tuple(x for x in domain if x != anchor)
        (
            rich_points,
            finite_rich_slopes,
            _,
            rank_stratified_bound,
            rank_stratified_slope_bound,
        ) = boundary_arrangement_profile(
            repeated_kernel_basis,
            repeated_root_domain,
            j - 1,
            repeated_twisted_u,
            repeated_twisted_v,
            p,
            "repeated-anchor",
        )
        if not residual_classes <= rich_points:
            raise AssertionError("residual repeated classes escaped rich arrangement")
        if len(residual_classes) != residual_repeated_anchor_locators[anchor]:
            raise AssertionError("repeated-anchor projective classes were not injective")
        if not residual_repeated_anchor_slopes[anchor] <= finite_rich_slopes:
            raise AssertionError("residual repeated slopes escaped rich slope image")
        residual_boundary_arrangement_bound += rank_stratified_bound
        residual_boundary_slope_arrangement_bound += rank_stratified_slope_bound
    if residual_infinity_projective_classes:
        infinity_kernel_rows = [
            tuple(u[col] for col in range(j + 1)),
            tuple(v[col] for col in range(j + 1)),
        ]
        infinity_kernel_basis = nullspace_basis(infinity_kernel_rows, p)
        shifted_u = tuple(u[row + 1] for row in range(j + 1))
        shifted_v = tuple(v[row + 1] for row in range(j + 1))
        (
            rich_points,
            finite_rich_slopes,
            _,
            rank_stratified_bound,
            rank_stratified_slope_bound,
        ) = boundary_arrangement_profile(
            infinity_kernel_basis,
            domain,
            j,
            shifted_u,
            shifted_v,
            p,
            "infinity-anchor",
        )
        if not residual_infinity_projective_classes <= rich_points:
            raise AssertionError("residual infinity classes escaped rich arrangement")
        if len(residual_infinity_projective_classes) != residual_anchor_escape_beta0_zero:
            raise AssertionError("infinity projective classes were not injective")
        if not residual_infinity_slopes <= finite_rich_slopes:
            raise AssertionError("residual infinity slopes escaped rich slope image")
        residual_boundary_arrangement_bound += rank_stratified_bound
        residual_boundary_slope_arrangement_bound += rank_stratified_slope_bound
    if residual_external_anchor_pinned_t1_checks != residual_anchor_escape_outside_domain:
        raise AssertionError("external-anchor pinned t=1 checks missed off-domain escapes")
    residual_projective_lift_fibers: dict[tuple[int, ...], set[int]] = {}
    for idx, key in enumerate(residual_projective_lift_keys):
        if key is None:
            raise AssertionError("residual projective lift key was not recorded")
        residual_projective_lift_fibers.setdefault(key, set()).add(idx)
    projective_lift_squarefree_fibers = 0
    projective_lift_boundary_fibers = 0
    projective_lift_boundary_singletons = 0
    projective_lift_pair_checks = 0
    projective_lift_fiber_max = 0
    for fiber in residual_projective_lift_fibers.values():
        projective_lift_fiber_max = max(projective_lift_fiber_max, len(fiber))
        boundary_vertices = fiber & residual_projective_lift_boundary_indices
        squarefree_vertices = fiber & residual_projective_lift_squarefree_indices
        if boundary_vertices:
            projective_lift_boundary_fibers += 1
            if len(fiber) != 1:
                raise AssertionError("boundary projective lift fiber was not singleton")
            if squarefree_vertices:
                raise AssertionError("boundary and squarefree projective fibers overlapped")
            projective_lift_boundary_singletons += 1
            continue
        if squarefree_vertices != fiber:
            raise AssertionError("projective lift fiber had an unclassified residual locator")
        projective_lift_squarefree_fibers += 1
        projective_lift_pair_checks += len(fiber) * (len(fiber) - 1) // 2
        if len(fiber) >= 2:
            union = set()
            for idx in fiber:
                union.update(residual_rows[idx][0])
            top_packet = tuple(sorted(union))
            if len(top_packet) != j + 1:
                raise AssertionError("nontrivial projective fiber was not a top packet")
            if residual_top_packets.get(top_packet) != fiber:
                raise AssertionError("projective lift fiber disagreed with top packet ledger")
    if projective_lift_pair_checks != residual_strict_pairs:
        raise AssertionError("projective lift fibers did not account for residual edges")
    if (
        projective_lift_boundary_singletons
        != len(residual_projective_lift_boundary_indices)
    ):
        raise AssertionError("boundary projective lift singleton count missed escapes")

    residual_component_count = 0
    residual_nontrivial_components = 0
    residual_isolated_components = 0
    residual_boundary_isolated_components = 0
    residual_component_clique_edges = 0
    residual_component_max = 0
    visited_components: set[int] = set()
    for start in range(len(residual_rows)):
        if start in visited_components:
            continue
        stack = [start]
        component: set[int] = set()
        visited_components.add(start)
        while stack:
            idx = stack.pop()
            component.add(idx)
            for neighbor in residual_adj[idx]:
                if neighbor not in visited_components:
                    visited_components.add(neighbor)
                    stack.append(neighbor)
        residual_component_count += 1
        residual_component_max = max(residual_component_max, len(component))
        if len(component) == 1:
            residual_isolated_components += 1
            idx = next(iter(component))
            if idx in residual_projective_lift_boundary_indices:
                residual_boundary_isolated_components += 1
            continue

        residual_nontrivial_components += 1
        edge_count = sum(len(residual_adj[idx] & component) for idx in component) // 2
        expected_edges = len(component) * (len(component) - 1) // 2
        if edge_count != expected_edges:
            raise AssertionError("residual component was not a clique")
        residual_component_clique_edges += edge_count
        if component & residual_projective_lift_boundary_indices:
            raise AssertionError("boundary projective lift appeared in a nontrivial component")
        if component - residual_projective_lift_squarefree_indices:
            raise AssertionError("nontrivial component was not squarefree lifted")
        keys = {residual_projective_lift_keys[idx] for idx in component}
        if len(keys) != 1:
            raise AssertionError("nontrivial component did not have one projective lift")
        lift_key = next(iter(keys))
        if lift_key is None or residual_projective_lift_fibers[lift_key] != component:
            raise AssertionError("nontrivial component was not one projective lift fiber")
        union = set()
        for idx in component:
            union.update(residual_rows[idx][0])
        top_packet = tuple(sorted(union))
        if len(top_packet) != j + 1:
            raise AssertionError("nontrivial component did not have one top packet")
        if residual_top_packets.get(top_packet) != component:
            raise AssertionError("nontrivial component disagreed with top-packet ledger")
        top_locator = locator(top_packet, p)
        if hankel_apply(u, 1, j + 1, top_locator, p)[0] != 0:
            raise AssertionError("nontrivial component missed numerator lifted gate")
        if hankel_apply(v, 1, j + 1, top_locator, p)[0] != 0:
            raise AssertionError("nontrivial component missed denominator lifted gate")
        slopes = {residual_rows[idx][1] for idx in component}
        if len(slopes) != len(component):
            raise AssertionError("nontrivial component was not slope-injective")
    if residual_nontrivial_components != len(residual_top_packets):
        raise AssertionError("residual components missed a top packet")
    if residual_component_clique_edges != residual_strict_pairs:
        raise AssertionError("residual component cliques did not account for every edge")
    if residual_boundary_isolated_components != len(residual_projective_lift_boundary_indices):
        raise AssertionError("boundary projective lift components were not all isolated")

    residual_slope_set = {slope for _, slope in residual_rows}
    root_slice_slope_set = {slope for _, slope in slice_keys}
    if not root_slice_slope_set <= root_slice_t3_slope_set:
        raise AssertionError("root-slice slopes escaped the t=3 core-locator image")
    root_slice_member_slope_set = {
        row_map[complement] for complement in root_slice_members
    }
    if not root_slice_member_slope_set <= root_slice_slope_set:
        raise AssertionError("root-slice members used a slope outside the slice ledger")
    if root_slice_member_slope_set != root_slice_slope_set:
        raise AssertionError("root-slice slope ledger was not exact")
    aperiodic_slope_set = {slope for _, slope in locator_rows}
    if aperiodic_slope_set != root_slice_member_slope_set | residual_slope_set:
        raise AssertionError("aperiodic slope image did not split into root and residual ledgers")
    root_slice_new_slope_set = root_slice_member_slope_set - residual_slope_set
    root_slice_t3_new_slope_set = root_slice_t3_slope_set - residual_slope_set
    if not root_slice_new_slope_set <= root_slice_t3_new_slope_set:
        raise AssertionError("new root-slice slopes escaped new t=3 slopes")
    if len(aperiodic_slope_set) != len(residual_slope_set) + len(root_slice_new_slope_set):
        raise AssertionError("aperiodic slope image did not have exact root/residual overlap")
    residual_lifted_slope_set = {
        residual_rows[idx][1] for idx in residual_anchor_lifted_face_indices
    }
    if lifted_common_core_active_ratio_slope_set != residual_lifted_slope_set:
        raise AssertionError("active residual-ratio slope image was not exact")
    residual_escape_slope_set = {
        residual_rows[idx][1] for idx in residual_anchor_escape_indices
    }
    if residual_slope_set != residual_lifted_slope_set | residual_escape_slope_set:
        raise AssertionError("residual slope image did not split by anchor ledger")
    if lifted_common_cores > min(lifted_u_t1_cores, lifted_v_t1_cores):
        raise AssertionError("lifted common cores exceeded an endpoint t=1 fiber")
    residual_lifted_escape_slope_overlap = len(
        residual_lifted_slope_set & residual_escape_slope_set
    )
    residual_escape_new_slopes = len(residual_escape_slope_set - residual_lifted_slope_set)
    residual_boundary_active_anchors = (
        len(residual_external_anchor_locators)
        + len(residual_repeated_anchor_locators)
        + (1 if residual_infinity_projective_classes else 0)
    )
    if residual_boundary_active_anchors > p + 1:
        raise AssertionError("boundary active anchors exceeded the projective line")
    residual_boundary_anchor_slope_bound = residual_boundary_active_anchors * (p + 1)
    residual_boundary_field_slope_bound = (p + 1) * (p + 1)
    lifted_core_slope_bound = (j + 1) * lifted_common_cores
    lifted_common_active_cores = (
        lifted_common_core_residual_singletons + lifted_common_core_residual_packets
    )
    lifted_common_inactive_cores = lifted_common_cores - lifted_common_active_cores
    active_lifted_core_slope_bound = (j + 1) * lifted_common_active_cores
    residual_recursion_bound = lifted_core_slope_bound + len(residual_escape_slope_set)
    residual_active_recursion_bound = (
        active_lifted_core_slope_bound + len(residual_escape_slope_set)
    )
    residual_new_escape_bound = lifted_core_slope_bound + residual_escape_new_slopes
    residual_active_new_escape_bound = (
        active_lifted_core_slope_bound + residual_escape_new_slopes
    )
    residual_active_face_new_escape_bound = (
        lifted_common_core_residual_faces + residual_escape_new_slopes
    )
    residual_arrangement_bound = lifted_core_slope_bound + residual_boundary_arrangement_bound
    residual_boundary_slope_bound = (
        lifted_core_slope_bound + residual_boundary_slope_arrangement_bound
    )
    residual_anchor_slope_bound = (
        lifted_core_slope_bound + residual_boundary_anchor_slope_bound
    )
    residual_field_slope_bound = (
        lifted_core_slope_bound + residual_boundary_field_slope_bound
    )
    if len(residual_lifted_slope_set) > lifted_common_core_residual_faces:
        raise AssertionError("lifted residual slopes exceeded lifted residual faces")
    if lifted_common_core_residual_faces > lifted_core_slope_bound:
        raise AssertionError("lifted residual faces exceeded the common-core face bound")
    if lifted_common_core_residual_faces > active_lifted_core_slope_bound:
        raise AssertionError("lifted residual faces exceeded the active-core face bound")
    if len(residual_slope_set) > residual_recursion_bound:
        raise AssertionError("residual slope image exceeded lifted-recursion bound")
    if len(residual_slope_set) > residual_active_recursion_bound:
        raise AssertionError("residual slope image exceeded active lifted-recursion bound")
    if len(residual_slope_set) > residual_new_escape_bound:
        raise AssertionError("residual slopes exceeded new-escape recursion bound")
    if len(residual_slope_set) > residual_active_new_escape_bound:
        raise AssertionError("residual slopes exceeded active new-escape recursion bound")
    if len(residual_slope_set) > residual_active_face_new_escape_bound:
        raise AssertionError("residual slopes exceeded active-face new-escape bound")
    if len(residual_escape_slope_set) > residual_boundary_anchor_slope_bound:
        raise AssertionError("escape slopes exceeded boundary active-anchor bound")
    if len(residual_escape_slope_set) > residual_boundary_field_slope_bound:
        raise AssertionError("escape slopes exceeded boundary field-size bound")
    if len(residual_escape_slope_set) > residual_boundary_arrangement_bound:
        raise AssertionError("escape slopes exceeded boundary arrangement bound")
    if len(residual_escape_slope_set) > residual_boundary_slope_arrangement_bound:
        raise AssertionError("escape slopes exceeded boundary slope-image bound")
    if len(residual_slope_set) > residual_arrangement_bound:
        raise AssertionError("residual slopes exceeded boundary arrangement reduction")
    if len(residual_slope_set) > residual_boundary_slope_bound:
        raise AssertionError("residual slopes exceeded boundary slope-image reduction")
    if len(residual_slope_set) > residual_anchor_slope_bound:
        raise AssertionError("residual slopes exceeded boundary active-anchor reduction")
    if len(residual_slope_set) > residual_field_slope_bound:
        raise AssertionError("residual slopes exceeded boundary field-size reduction")
    total_reduction_bound = len(root_slice_slope_set) + residual_recursion_bound
    if len(aperiodic_slope_set) > total_reduction_bound:
        raise AssertionError("aperiodic slope image exceeded t=2 reduction bound")
    exact_active_face_bound = (
        len(root_slice_new_slope_set)
        + lifted_common_core_residual_faces
        + residual_escape_new_slopes
    )
    if len(aperiodic_slope_set) > exact_active_face_bound:
        raise AssertionError("aperiodic slope image exceeded exact active-face bound")
    recursive_reduction_bound = len(root_slice_t3_slope_set) + residual_recursion_bound
    if len(aperiodic_slope_set) > recursive_reduction_bound:
        raise AssertionError("aperiodic slope image exceeded recursive t=3 reduction bound")
    recursive_new_escape_bound = len(root_slice_t3_slope_set) + residual_new_escape_bound
    if len(aperiodic_slope_set) > recursive_new_escape_bound:
        raise AssertionError("aperiodic slope image exceeded new-escape recursive bound")
    recursive_arrangement_bound = len(root_slice_t3_slope_set) + residual_arrangement_bound
    if len(aperiodic_slope_set) > recursive_arrangement_bound:
        raise AssertionError("aperiodic slope image exceeded arrangement-recursive bound")
    recursive_boundary_slope_bound = (
        len(root_slice_t3_slope_set) + residual_boundary_slope_bound
    )
    if len(aperiodic_slope_set) > recursive_boundary_slope_bound:
        raise AssertionError("aperiodic slope image exceeded boundary-slope recursive bound")
    recursive_anchor_slope_bound = (
        len(root_slice_t3_slope_set) + residual_anchor_slope_bound
    )
    if len(aperiodic_slope_set) > recursive_anchor_slope_bound:
        raise AssertionError("aperiodic slope image exceeded active-anchor recursive bound")
    recursive_field_slope_bound = (
        len(root_slice_t3_slope_set) + residual_field_slope_bound
    )
    if len(aperiodic_slope_set) > recursive_field_slope_bound:
        raise AssertionError("aperiodic slope image exceeded field-size recursive bound")
    recursive_active_field_slope_bound = (
        len(root_slice_t3_slope_set)
        + active_lifted_core_slope_bound
        + residual_boundary_field_slope_bound
    )
    if len(aperiodic_slope_set) > recursive_active_field_slope_bound:
        raise AssertionError("aperiodic slope image exceeded active-core field bound")
    recursive_active_new_escape_bound = (
        len(root_slice_t3_slope_set)
        + active_lifted_core_slope_bound
        + residual_escape_new_slopes
    )
    if len(aperiodic_slope_set) > recursive_active_new_escape_bound:
        raise AssertionError("aperiodic slope image exceeded active new-escape bound")
    recursive_active_face_new_escape_bound = (
        len(root_slice_t3_slope_set)
        + lifted_common_core_residual_faces
        + residual_escape_new_slopes
    )
    if len(aperiodic_slope_set) > recursive_active_face_new_escape_bound:
        raise AssertionError("aperiodic slope image exceeded active-face new-escape bound")
    recursive_active_face_new_root_bound = (
        len(root_slice_t3_new_slope_set)
        + lifted_common_core_residual_faces
        + residual_escape_new_slopes
    )
    if len(aperiodic_slope_set) > recursive_active_face_new_root_bound:
        raise AssertionError("aperiodic slope image exceeded active-face new-root bound")
    two_input_field_bound = (
        len(root_slice_t3_slope_set)
        + (j + 1) * min(lifted_u_t1_cores, lifted_v_t1_cores)
        + residual_boundary_field_slope_bound
    )
    if len(aperiodic_slope_set) > two_input_field_bound:
        raise AssertionError("aperiodic slope image exceeded two-input field-size bound")

    top_packet_overlap_pairs = 0
    top_packet_overlap_max = 0
    for left in range(len(top_packet_vertex_sets)):
        for right in range(left + 1, len(top_packet_vertex_sets)):
            overlap = len(top_packet_vertex_sets[left] & top_packet_vertex_sets[right])
            top_packet_overlap_max = max(top_packet_overlap_max, overlap)
            if overlap:
                top_packet_overlap_pairs += 1
            if overlap > 1:
                raise AssertionError("residual top-packet hypergraph was not linear")
    if max(top_packet_incidences, default=0) > 1:
        raise AssertionError("residual top packets were not vertex-disjoint")

    return {
        "root_slices": len(slice_keys),
        "same_slope_edges_covered": same_slope_edges,
        "max_root_slice_noncontained": max_noncontained,
        "max_root_slice_aperiodic_members": max_aperiodic_members,
        "root_slice_slope_count": len({slope for _, slope in slice_keys}),
        "root_slice_new_slope_count": len(root_slice_new_slope_set),
        "root_slice_total_slope_bound": total_reduction_bound,
        "root_slice_t3_core_locators": root_slice_t3_core_locators,
        "root_slice_t3_slope_count": len(root_slice_t3_slope_set),
        "root_slice_t3_new_slope_count": len(root_slice_t3_new_slope_set),
        "root_slice_recursive_slope_bound": recursive_reduction_bound,
        "root_slice_members": len(root_slice_members),
        "root_slice_residual_locators": len(residual_rows),
        "root_slice_residual_slopes": len(residual_slope_fibers),
        "root_slice_residual_max_slope_fiber": max(residual_slope_fibers.values(), default=0),
        "root_slice_residual_slope_core_checks": residual_slope_core_checks,
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
        "root_slice_residual_top_packet_overlap_pairs": top_packet_overlap_pairs,
        "root_slice_residual_top_packet_overlap_max": top_packet_overlap_max,
        "root_slice_residual_components": residual_component_count,
        "root_slice_residual_nontrivial_components": residual_nontrivial_components,
        "root_slice_residual_isolated_components": residual_isolated_components,
        "root_slice_residual_boundary_isolated_components": (
            residual_boundary_isolated_components
        ),
        "root_slice_residual_component_max": residual_component_max,
        "root_slice_residual_component_clique_edges": residual_component_clique_edges,
        "root_slice_residual_common_companion_checks": common_companion_checks,
        "root_slice_residual_top_lift_gate_checks": top_lift_gate_checks,
        "root_slice_residual_top_anchor_checks": top_anchor_checks,
        "root_slice_residual_top_common_lift_gate_checks": top_common_lift_gate_checks,
        "root_slice_residual_top_numerator_anchor_checks": top_numerator_anchor_checks,
        "root_slice_residual_top_face_gate_checks": top_face_gate_checks,
        "root_slice_residual_top_face_noncontained": top_face_noncontained,
        "root_slice_residual_top_face_aperiodic": top_face_aperiodic,
        "root_slice_residual_top_face_residual": top_face_residual,
        "root_slice_residual_top_face_peeled": top_face_peeled,
        "root_slice_residual_anchor_lifted_faces": residual_anchor_lifted_faces,
        "root_slice_residual_anchor_escape_locators": residual_anchor_escape_locators,
        "root_slice_residual_anchor_beta0_zero": residual_anchor_escape_beta0_zero,
        "root_slice_residual_anchor_in_support": residual_anchor_escape_in_support,
        "root_slice_residual_anchor_outside_domain": residual_anchor_escape_outside_domain,
        "root_slice_residual_external_anchors": len(residual_external_anchor_locators),
        "root_slice_residual_external_anchor_values": tuple(
            sorted(residual_external_anchor_locators)
        ),
        "root_slice_residual_external_anchor_locator_max": max(
            residual_external_anchor_locators.values(), default=0
        ),
        "root_slice_residual_external_anchor_slope_max": max(
            (len(slopes) for slopes in residual_external_anchor_slopes.values()),
            default=0,
        ),
        "root_slice_residual_external_anchor_slope_fibers": len(
            residual_external_anchor_slope_locators
        ),
        "root_slice_residual_external_anchor_slope_fiber_max": max(
            residual_external_anchor_slope_locators.values(), default=0
        ),
        "root_slice_residual_external_anchor_slope_core_checks": (
            residual_external_anchor_slope_core_checks
        ),
        "root_slice_residual_external_anchor_kernel_dim_max": (
            residual_external_anchor_kernel_dim_max
        ),
        "root_slice_residual_external_anchor_projective_points": (
            residual_external_anchor_projective_points
        ),
        "root_slice_residual_external_anchor_rich_points": (
            residual_external_anchor_rich_points
        ),
        "root_slice_residual_external_anchor_finite_rich_slopes": (
            residual_external_anchor_finite_rich_slopes
        ),
        "root_slice_residual_external_anchor_rich_residual_classes": (
            residual_external_anchor_rich_residual_classes
        ),
        "root_slice_residual_external_anchor_twist_checks": (
            residual_external_anchor_twist_checks
        ),
        "root_slice_residual_external_anchor_interpolation_checks": (
            residual_external_anchor_interpolation_checks
        ),
        "root_slice_residual_external_anchor_pinned_t1_checks": (
            residual_external_anchor_pinned_t1_checks
        ),
        "root_slice_residual_anchor_lift_gate_checks": residual_anchor_lift_gate_checks,
        "root_slice_residual_anchor_isolated_checks": residual_anchor_isolated_checks,
        "root_slice_residual_anchor_projective_lift_checks": (
            residual_anchor_projective_lift_checks
        ),
        "root_slice_residual_anchor_projective_unique_checks": (
            residual_anchor_projective_unique_checks
        ),
        "root_slice_residual_projective_lift_fibers": len(
            residual_projective_lift_fibers
        ),
        "root_slice_residual_projective_squarefree_fibers": (
            projective_lift_squarefree_fibers
        ),
        "root_slice_residual_projective_boundary_fibers": (
            projective_lift_boundary_fibers
        ),
        "root_slice_residual_projective_boundary_singletons": (
            projective_lift_boundary_singletons
        ),
        "root_slice_residual_projective_lift_fiber_max": projective_lift_fiber_max,
        "root_slice_residual_projective_lift_pair_checks": projective_lift_pair_checks,
        "root_slice_residual_anchor_finite_lift_checks": (
            residual_anchor_finite_lift_checks
        ),
        "root_slice_residual_anchor_repeated_lift_checks": (
            residual_anchor_repeated_lift_checks
        ),
        "root_slice_residual_anchor_offdomain_lift_checks": (
            residual_anchor_offdomain_lift_checks
        ),
        "root_slice_residual_anchor_infinity_checks": residual_anchor_infinity_checks,
        "root_slice_residual_lifted_slopes": len(residual_lifted_slope_set),
        "root_slice_residual_escape_slopes": len(residual_escape_slope_set),
        "root_slice_residual_lifted_escape_slope_overlap": (
            residual_lifted_escape_slope_overlap
        ),
        "root_slice_residual_escape_new_slopes": residual_escape_new_slopes,
        "root_slice_residual_lifted_core_slope_bound": lifted_core_slope_bound,
        "root_slice_residual_recursion_bound": residual_recursion_bound,
        "root_slice_residual_new_escape_bound": residual_new_escape_bound,
        "root_slice_residual_active_new_escape_bound": residual_active_new_escape_bound,
        "root_slice_residual_active_face_new_escape_bound": (
            residual_active_face_new_escape_bound
        ),
        "root_slice_residual_boundary_arrangement_bound": (
            residual_boundary_arrangement_bound
        ),
        "root_slice_residual_boundary_slope_bound": (
            residual_boundary_slope_arrangement_bound
        ),
        "root_slice_residual_boundary_active_anchors": residual_boundary_active_anchors,
        "root_slice_residual_boundary_anchor_slope_bound": (
            residual_boundary_anchor_slope_bound
        ),
        "root_slice_residual_boundary_field_slope_bound": (
            residual_boundary_field_slope_bound
        ),
        "root_slice_residual_active_lifted_core_slope_bound": (
            active_lifted_core_slope_bound
        ),
        "root_slice_recursive_arrangement_bound": recursive_arrangement_bound,
        "root_slice_recursive_boundary_slope_bound": recursive_boundary_slope_bound,
        "root_slice_recursive_boundary_anchor_slope_bound": recursive_anchor_slope_bound,
        "root_slice_recursive_boundary_field_slope_bound": recursive_field_slope_bound,
        "root_slice_recursive_active_field_slope_bound": (
            recursive_active_field_slope_bound
        ),
        "root_slice_recursive_new_escape_bound": recursive_new_escape_bound,
        "root_slice_recursive_active_new_escape_bound": (
            recursive_active_new_escape_bound
        ),
        "root_slice_recursive_active_face_new_escape_bound": (
            recursive_active_face_new_escape_bound
        ),
        "root_slice_exact_active_face_bound": exact_active_face_bound,
        "root_slice_recursive_active_face_new_root_bound": (
            recursive_active_face_new_root_bound
        ),
        "root_slice_two_input_field_bound": two_input_field_bound,
        "root_slice_lifted_u_t1_cores": lifted_u_t1_cores,
        "root_slice_lifted_v_t1_cores": lifted_v_t1_cores,
        "root_slice_lifted_common_cores": lifted_common_cores,
        "root_slice_lifted_common_active_cores": lifted_common_active_cores,
        "root_slice_lifted_common_inactive_cores": lifted_common_inactive_cores,
        "root_slice_lifted_common_core_noncontained_faces": (
            lifted_common_core_noncontained_faces
        ),
        "root_slice_lifted_common_core_aperiodic_faces": lifted_common_core_aperiodic_faces,
        "root_slice_lifted_common_core_residual_faces": lifted_common_core_residual_faces,
        "root_slice_lifted_common_core_peeled_faces": lifted_common_core_peeled_faces,
        "root_slice_lifted_common_core_residual_singletons": (
            lifted_common_core_residual_singletons
        ),
        "root_slice_lifted_common_core_residual_packets": lifted_common_core_residual_packets,
        "root_slice_lifted_common_core_max_residual_faces": (
            lifted_common_core_max_residual_faces
        ),
        "root_slice_lifted_common_core_common_base_checks": (
            lifted_common_core_common_base_checks
        ),
        "root_slice_lifted_common_core_residual_slope_checks": (
            lifted_common_core_residual_slope_checks
        ),
        "root_slice_lifted_common_core_active_ratio_checks": (
            lifted_common_core_active_ratio_checks
        ),
        "root_slice_lifted_common_core_residual_slope_pair_checks": (
            lifted_common_core_residual_slope_pair_checks
        ),
        "root_slice_lifted_common_core_residual_slope_fiber_max": (
            lifted_common_core_residual_slope_fiber_max
        ),
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
    return bool(
        quotient_periodic_scales(complement, domain, exponents, charged_fiber_sizes)
    )


def quotient_periodic_scale_residues(
    complement: tuple[int, ...],
    domain: tuple[int, ...],
    exponents: dict[int, int],
    fiber_size: int,
) -> tuple[int, ...] | None:
    n = len(domain)
    comp = set(complement)
    if fiber_size <= 1 or fiber_size >= n or n % fiber_size or len(comp) % fiber_size:
        return None
    quotient_size = n // fiber_size
    residues = []
    for residue in range(quotient_size):
        fiber = {x for x in domain if exponents[x] % quotient_size == residue}
        if fiber & comp:
            if not fiber <= comp:
                return None
            residues.append(residue)
    return tuple(residues)


def quotient_periodic_scales(
    complement: tuple[int, ...],
    domain: tuple[int, ...],
    exponents: dict[int, int],
    charged_fiber_sizes: tuple[int, ...],
) -> tuple[int, ...]:
    return tuple(
        fiber_size
        for fiber_size in charged_fiber_sizes
        if quotient_periodic_scale_residues(complement, domain, exponents, fiber_size)
        is not None
    )


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
    one_exchange_lift_profile = same_slope_one_exchange_lift_profile(
        aperiodic_locator_rows, domain, u, v, t, j, p
    )
    if (
        one_exchange_lift_profile["same_slope_one_exchange_edges"]
        != exchange_profile["same_slope_one_exchange_pairs"]
    ):
        raise AssertionError("same-slope one-exchange lift missed an edge")
    root_slice_keys, _ = same_slope_one_exchange_root_slice_keys(
        aperiodic_locator_rows, j
    )
    root_slice_slope_set = {slope for _core, slope in root_slice_keys}
    two_exchange_profile = two_exchange_quadratic_slice_profile(
        aperiodic_locator_rows,
        domain,
        u,
        v,
        t,
        j,
        p,
        root_slice_slope_set,
    )
    if t == 3:
        expected_two_exchange = (
            exchange_profile["strict_pairs"] - exchange_profile["one_exchange_pairs"]
        )
        if two_exchange_profile["two_exchange_pairs"] != expected_two_exchange:
            raise AssertionError("two-exchange profile missed a strict t=3 pair")
    root_profile = root_slice_profile(aperiodic_locator_rows, domain, u, v, f, g, k, t, j, p)
    if t == 2 and root_profile["same_slope_edges_covered"] != exchange_profile["same_slope_strict_pairs"]:
        raise AssertionError("root-slice coverage missed same-slope strict edges")
    quadratic_profile = quadratic_slice_profile(aperiodic_locator_rows, domain, u, v, t, j, p)
    expected_different_slope = (
        exchange_profile["strict_pairs"] - exchange_profile["same_slope_strict_pairs"]
    )
    if t == 2 and quadratic_profile["different_slope_strict_pairs"] != expected_different_slope:
        raise AssertionError("quadratic-slice profile missed different-slope strict edges")
    if (
        t == 2
        and
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
        "aperiodic_one_exchange_pairs": exchange_profile["one_exchange_pairs"],
        "aperiodic_max_strict_degree": exchange_profile["max_strict_degree"],
        "aperiodic_same_slope_strict_pairs": exchange_profile["same_slope_strict_pairs"],
        "aperiodic_same_slope_one_exchange_pairs": exchange_profile[
            "same_slope_one_exchange_pairs"
        ],
        "same_slope_one_exchange_root_slices": one_exchange_lift_profile[
            "same_slope_one_exchange_root_slices"
        ],
        "same_slope_one_exchange_root_slopes": one_exchange_lift_profile[
            "same_slope_one_exchange_root_slopes"
        ],
        "same_slope_one_exchange_next_core_locators": one_exchange_lift_profile[
            "same_slope_one_exchange_next_core_locators"
        ],
        "same_slope_one_exchange_next_slopes": one_exchange_lift_profile[
            "same_slope_one_exchange_next_slopes"
        ],
        "same_slope_one_exchange_member_checks": one_exchange_lift_profile[
            "same_slope_one_exchange_member_checks"
        ],
        "same_slope_one_exchange_noncontained_max": one_exchange_lift_profile[
            "same_slope_one_exchange_noncontained_max"
        ],
        "same_slope_one_exchange_aperiodic_members_max": one_exchange_lift_profile[
            "same_slope_one_exchange_aperiodic_members_max"
        ],
        "two_exchange_pairs": two_exchange_profile["two_exchange_pairs"],
        "two_exchange_same_slope_pairs": two_exchange_profile[
            "two_exchange_same_slope_pairs"
        ],
        "two_exchange_different_slope_pairs": two_exchange_profile[
            "two_exchange_different_slope_pairs"
        ],
        "two_exchange_cores": two_exchange_profile["two_exchange_cores"],
        "two_exchange_slices_checked": two_exchange_profile[
            "two_exchange_slices_checked"
        ],
        "two_exchange_minor_polynomial_checks": two_exchange_profile[
            "two_exchange_minor_polynomial_checks"
        ],
        "two_exchange_bad_locator_checks": two_exchange_profile[
            "two_exchange_bad_locator_checks"
        ],
        "two_exchange_max_slice_aperiodic_locators": two_exchange_profile[
            "two_exchange_max_slice_aperiodic_locators"
        ],
        "two_exchange_max_slice_slope_image": two_exchange_profile[
            "two_exchange_max_slice_slope_image"
        ],
        "two_exchange_same_slope_clusters": two_exchange_profile[
            "two_exchange_same_slope_clusters"
        ],
        "two_exchange_same_slope_line_clusters": two_exchange_profile[
            "two_exchange_same_slope_line_clusters"
        ],
        "two_exchange_same_slope_fixed_root_lines": two_exchange_profile[
            "two_exchange_same_slope_fixed_root_lines"
        ],
        "two_exchange_same_slope_mobius_lines": two_exchange_profile[
            "two_exchange_same_slope_mobius_lines"
        ],
        "two_exchange_same_slope_product_mobius_lines": two_exchange_profile[
            "two_exchange_same_slope_product_mobius_lines"
        ],
        "two_exchange_same_slope_sum_mobius_lines": two_exchange_profile[
            "two_exchange_same_slope_sum_mobius_lines"
        ],
        "two_exchange_same_slope_line_two_exchange_pairs": two_exchange_profile[
            "two_exchange_same_slope_line_two_exchange_pairs"
        ],
        "two_exchange_same_slope_mobius_two_exchange_pairs": two_exchange_profile[
            "two_exchange_same_slope_mobius_two_exchange_pairs"
        ],
        "two_exchange_same_slope_mobius_pair_checks": two_exchange_profile[
            "two_exchange_same_slope_mobius_pair_checks"
        ],
        "two_exchange_same_slope_mobius_member_max": two_exchange_profile[
            "two_exchange_same_slope_mobius_member_max"
        ],
        "two_exchange_same_slope_plane_clusters": two_exchange_profile[
            "two_exchange_same_slope_plane_clusters"
        ],
        "two_exchange_same_slope_plane_lifts": two_exchange_profile[
            "two_exchange_same_slope_plane_lifts"
        ],
        "two_exchange_same_slope_plane_two_exchange_pairs": two_exchange_profile[
            "two_exchange_same_slope_plane_two_exchange_pairs"
        ],
        "two_exchange_same_slope_affine_member_max": two_exchange_profile[
            "two_exchange_same_slope_affine_member_max"
        ],
        "two_exchange_same_slope_lift_checks": two_exchange_profile[
            "two_exchange_same_slope_lift_checks"
        ],
        "two_exchange_det_line_components": two_exchange_profile[
            "two_exchange_det_line_components"
        ],
        "two_exchange_det_line_fixed_root": two_exchange_profile[
            "two_exchange_det_line_fixed_root"
        ],
        "two_exchange_det_line_product_mobius": two_exchange_profile[
            "two_exchange_det_line_product_mobius"
        ],
        "two_exchange_det_line_sum_mobius": two_exchange_profile[
            "two_exchange_det_line_sum_mobius"
        ],
        "two_exchange_det_line_constant_slope": two_exchange_profile[
            "two_exchange_det_line_constant_slope"
        ],
        "two_exchange_det_line_variable_slope": two_exchange_profile[
            "two_exchange_det_line_variable_slope"
        ],
        "two_exchange_det_line_slope_max": two_exchange_profile[
            "two_exchange_det_line_slope_max"
        ],
        "two_exchange_det_line_aperiodic_max": two_exchange_profile[
            "two_exchange_det_line_aperiodic_max"
        ],
        "two_exchange_det_line_point_checks": two_exchange_profile[
            "two_exchange_det_line_point_checks"
        ],
        "two_exchange_det_full_planes": two_exchange_profile[
            "two_exchange_det_full_planes"
        ],
        "two_exchange_det_full_plane_constant_slope": two_exchange_profile[
            "two_exchange_det_full_plane_constant_slope"
        ],
        "two_exchange_det_full_plane_variable_slope": two_exchange_profile[
            "two_exchange_det_full_plane_variable_slope"
        ],
        "two_exchange_det_full_plane_contained": two_exchange_profile[
            "two_exchange_det_full_plane_contained"
        ],
        "two_exchange_det_full_plane_den_rank_max": two_exchange_profile[
            "two_exchange_det_full_plane_den_rank_max"
        ],
        "two_exchange_det_full_plane_slope_max": two_exchange_profile[
            "two_exchange_det_full_plane_slope_max"
        ],
        "two_exchange_det_full_plane_aperiodic_max": two_exchange_profile[
            "two_exchange_det_full_plane_aperiodic_max"
        ],
        "two_exchange_det_full_plane_lifts": two_exchange_profile[
            "two_exchange_det_full_plane_lifts"
        ],
        "two_exchange_det_proper_lines": two_exchange_profile[
            "two_exchange_det_proper_lines"
        ],
        "two_exchange_det_proper_line_fixed_root": two_exchange_profile[
            "two_exchange_det_proper_line_fixed_root"
        ],
        "two_exchange_det_proper_line_product_mobius": two_exchange_profile[
            "two_exchange_det_proper_line_product_mobius"
        ],
        "two_exchange_det_proper_line_sum_mobius": two_exchange_profile[
            "two_exchange_det_proper_line_sum_mobius"
        ],
        "two_exchange_det_proper_line_constant_slope": two_exchange_profile[
            "two_exchange_det_proper_line_constant_slope"
        ],
        "two_exchange_det_proper_line_variable_slope": two_exchange_profile[
            "two_exchange_det_proper_line_variable_slope"
        ],
        "two_exchange_det_proper_line_slope_max": two_exchange_profile[
            "two_exchange_det_proper_line_slope_max"
        ],
        "two_exchange_det_proper_line_aperiodic_max": two_exchange_profile[
            "two_exchange_det_proper_line_aperiodic_max"
        ],
        "two_exchange_det_proper_line_core_max": two_exchange_profile[
            "two_exchange_det_proper_line_core_max"
        ],
        "two_exchange_det_proper_line_variable_injective": two_exchange_profile[
            "two_exchange_det_proper_line_variable_injective"
        ],
        "two_exchange_det_proper_line_variable_pole_max": two_exchange_profile[
            "two_exchange_det_proper_line_variable_pole_max"
        ],
        "two_exchange_det_proper_line_variable_aperiodic_slope_max": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_aperiodic_slope_max"
            ]
        ),
        "two_exchange_det_proper_line_variable_injective_checks": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_injective_checks"
            ]
        ),
        "two_exchange_det_proper_line_variable_aperiodic_slopes": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_aperiodic_slopes"
            ]
        ),
        "two_exchange_det_proper_line_variable_new_slopes": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_new_slopes"
            ]
        ),
        "two_exchange_det_proper_line_variable_new_slope_max": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_new_slope_max"
            ]
        ),
        "two_exchange_det_proper_line_variable_nonfixed": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_nonfixed"
            ]
        ),
        "two_exchange_det_proper_line_variable_anchored": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_anchored"
            ]
        ),
        "two_exchange_det_proper_line_variable_unanchored": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_unanchored"
            ]
        ),
        "two_exchange_det_proper_line_variable_domain_pair_max": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_domain_pair_max"
            ]
        ),
        "two_exchange_det_proper_line_variable_domain_pair_checks": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_domain_pair_checks"
            ]
        ),
        "two_exchange_det_proper_line_variable_charged_slope_checks": (
            two_exchange_profile[
                "two_exchange_det_proper_line_variable_charged_slope_checks"
            ]
        ),
        "root_slices": root_profile["root_slices"],
        "same_slope_edges_covered": root_profile["same_slope_edges_covered"],
        "max_root_slice_noncontained": root_profile["max_root_slice_noncontained"],
        "max_root_slice_aperiodic_members": root_profile["max_root_slice_aperiodic_members"],
        "root_slice_slope_count": root_profile["root_slice_slope_count"],
        "root_slice_new_slope_count": root_profile["root_slice_new_slope_count"],
        "root_slice_total_slope_bound": root_profile["root_slice_total_slope_bound"],
        "root_slice_t3_core_locators": root_profile["root_slice_t3_core_locators"],
        "root_slice_t3_slope_count": root_profile["root_slice_t3_slope_count"],
        "root_slice_t3_new_slope_count": root_profile["root_slice_t3_new_slope_count"],
        "root_slice_recursive_slope_bound": root_profile[
            "root_slice_recursive_slope_bound"
        ],
        "root_slice_members": root_profile["root_slice_members"],
        "root_slice_residual_locators": root_profile["root_slice_residual_locators"],
        "root_slice_residual_slopes": root_profile["root_slice_residual_slopes"],
        "root_slice_residual_max_slope_fiber": (
            root_profile["root_slice_residual_max_slope_fiber"]
        ),
        "root_slice_residual_slope_core_checks": (
            root_profile["root_slice_residual_slope_core_checks"]
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
        "root_slice_residual_top_packet_overlap_pairs": (
            root_profile["root_slice_residual_top_packet_overlap_pairs"]
        ),
        "root_slice_residual_top_packet_overlap_max": (
            root_profile["root_slice_residual_top_packet_overlap_max"]
        ),
        "root_slice_residual_components": root_profile["root_slice_residual_components"],
        "root_slice_residual_nontrivial_components": (
            root_profile["root_slice_residual_nontrivial_components"]
        ),
        "root_slice_residual_isolated_components": (
            root_profile["root_slice_residual_isolated_components"]
        ),
        "root_slice_residual_boundary_isolated_components": (
            root_profile["root_slice_residual_boundary_isolated_components"]
        ),
        "root_slice_residual_component_max": (
            root_profile["root_slice_residual_component_max"]
        ),
        "root_slice_residual_component_clique_edges": (
            root_profile["root_slice_residual_component_clique_edges"]
        ),
        "root_slice_residual_common_companion_checks": (
            root_profile["root_slice_residual_common_companion_checks"]
        ),
        "root_slice_residual_top_lift_gate_checks": (
            root_profile["root_slice_residual_top_lift_gate_checks"]
        ),
        "root_slice_residual_top_anchor_checks": (
            root_profile["root_slice_residual_top_anchor_checks"]
        ),
        "root_slice_residual_top_common_lift_gate_checks": (
            root_profile["root_slice_residual_top_common_lift_gate_checks"]
        ),
        "root_slice_residual_top_numerator_anchor_checks": (
            root_profile["root_slice_residual_top_numerator_anchor_checks"]
        ),
        "root_slice_residual_top_face_gate_checks": (
            root_profile["root_slice_residual_top_face_gate_checks"]
        ),
        "root_slice_residual_top_face_noncontained": (
            root_profile["root_slice_residual_top_face_noncontained"]
        ),
        "root_slice_residual_top_face_aperiodic": (
            root_profile["root_slice_residual_top_face_aperiodic"]
        ),
        "root_slice_residual_top_face_residual": (
            root_profile["root_slice_residual_top_face_residual"]
        ),
        "root_slice_residual_top_face_peeled": (
            root_profile["root_slice_residual_top_face_peeled"]
        ),
        "root_slice_residual_anchor_lifted_faces": (
            root_profile["root_slice_residual_anchor_lifted_faces"]
        ),
        "root_slice_residual_anchor_escape_locators": (
            root_profile["root_slice_residual_anchor_escape_locators"]
        ),
        "root_slice_residual_anchor_beta0_zero": (
            root_profile["root_slice_residual_anchor_beta0_zero"]
        ),
        "root_slice_residual_anchor_in_support": (
            root_profile["root_slice_residual_anchor_in_support"]
        ),
        "root_slice_residual_anchor_outside_domain": (
            root_profile["root_slice_residual_anchor_outside_domain"]
        ),
        "root_slice_residual_external_anchors": (
            root_profile["root_slice_residual_external_anchors"]
        ),
        "root_slice_residual_external_anchor_values": (
            root_profile["root_slice_residual_external_anchor_values"]
        ),
        "root_slice_residual_external_anchor_locator_max": (
            root_profile["root_slice_residual_external_anchor_locator_max"]
        ),
        "root_slice_residual_external_anchor_slope_max": (
            root_profile["root_slice_residual_external_anchor_slope_max"]
        ),
        "root_slice_residual_external_anchor_slope_fibers": (
            root_profile["root_slice_residual_external_anchor_slope_fibers"]
        ),
        "root_slice_residual_external_anchor_slope_fiber_max": (
            root_profile["root_slice_residual_external_anchor_slope_fiber_max"]
        ),
        "root_slice_residual_external_anchor_slope_core_checks": (
            root_profile["root_slice_residual_external_anchor_slope_core_checks"]
        ),
        "root_slice_residual_external_anchor_kernel_dim_max": (
            root_profile["root_slice_residual_external_anchor_kernel_dim_max"]
        ),
        "root_slice_residual_external_anchor_projective_points": (
            root_profile["root_slice_residual_external_anchor_projective_points"]
        ),
        "root_slice_residual_external_anchor_rich_points": (
            root_profile["root_slice_residual_external_anchor_rich_points"]
        ),
        "root_slice_residual_external_anchor_finite_rich_slopes": (
            root_profile["root_slice_residual_external_anchor_finite_rich_slopes"]
        ),
        "root_slice_residual_external_anchor_rich_residual_classes": (
            root_profile["root_slice_residual_external_anchor_rich_residual_classes"]
        ),
        "root_slice_residual_external_anchor_twist_checks": (
            root_profile["root_slice_residual_external_anchor_twist_checks"]
        ),
        "root_slice_residual_external_anchor_interpolation_checks": (
            root_profile["root_slice_residual_external_anchor_interpolation_checks"]
        ),
        "root_slice_residual_external_anchor_pinned_t1_checks": (
            root_profile["root_slice_residual_external_anchor_pinned_t1_checks"]
        ),
        "root_slice_residual_anchor_lift_gate_checks": (
            root_profile["root_slice_residual_anchor_lift_gate_checks"]
        ),
        "root_slice_residual_anchor_isolated_checks": (
            root_profile["root_slice_residual_anchor_isolated_checks"]
        ),
        "root_slice_residual_anchor_projective_lift_checks": (
            root_profile["root_slice_residual_anchor_projective_lift_checks"]
        ),
        "root_slice_residual_anchor_projective_unique_checks": (
            root_profile["root_slice_residual_anchor_projective_unique_checks"]
        ),
        "root_slice_residual_projective_lift_fibers": (
            root_profile["root_slice_residual_projective_lift_fibers"]
        ),
        "root_slice_residual_projective_squarefree_fibers": (
            root_profile["root_slice_residual_projective_squarefree_fibers"]
        ),
        "root_slice_residual_projective_boundary_fibers": (
            root_profile["root_slice_residual_projective_boundary_fibers"]
        ),
        "root_slice_residual_projective_boundary_singletons": (
            root_profile["root_slice_residual_projective_boundary_singletons"]
        ),
        "root_slice_residual_projective_lift_fiber_max": (
            root_profile["root_slice_residual_projective_lift_fiber_max"]
        ),
        "root_slice_residual_projective_lift_pair_checks": (
            root_profile["root_slice_residual_projective_lift_pair_checks"]
        ),
        "root_slice_residual_anchor_finite_lift_checks": (
            root_profile["root_slice_residual_anchor_finite_lift_checks"]
        ),
        "root_slice_residual_anchor_repeated_lift_checks": (
            root_profile["root_slice_residual_anchor_repeated_lift_checks"]
        ),
        "root_slice_residual_anchor_offdomain_lift_checks": (
            root_profile["root_slice_residual_anchor_offdomain_lift_checks"]
        ),
        "root_slice_residual_anchor_infinity_checks": (
            root_profile["root_slice_residual_anchor_infinity_checks"]
        ),
        "root_slice_residual_lifted_slopes": root_profile["root_slice_residual_lifted_slopes"],
        "root_slice_residual_escape_slopes": root_profile["root_slice_residual_escape_slopes"],
        "root_slice_residual_lifted_escape_slope_overlap": (
            root_profile["root_slice_residual_lifted_escape_slope_overlap"]
        ),
        "root_slice_residual_escape_new_slopes": (
            root_profile["root_slice_residual_escape_new_slopes"]
        ),
        "root_slice_residual_lifted_core_slope_bound": (
            root_profile["root_slice_residual_lifted_core_slope_bound"]
        ),
        "root_slice_residual_recursion_bound": (
            root_profile["root_slice_residual_recursion_bound"]
        ),
        "root_slice_residual_new_escape_bound": (
            root_profile["root_slice_residual_new_escape_bound"]
        ),
        "root_slice_residual_active_new_escape_bound": (
            root_profile["root_slice_residual_active_new_escape_bound"]
        ),
        "root_slice_residual_active_face_new_escape_bound": (
            root_profile["root_slice_residual_active_face_new_escape_bound"]
        ),
        "root_slice_residual_boundary_arrangement_bound": (
            root_profile["root_slice_residual_boundary_arrangement_bound"]
        ),
        "root_slice_residual_boundary_slope_bound": (
            root_profile["root_slice_residual_boundary_slope_bound"]
        ),
        "root_slice_residual_boundary_active_anchors": (
            root_profile["root_slice_residual_boundary_active_anchors"]
        ),
        "root_slice_residual_boundary_anchor_slope_bound": (
            root_profile["root_slice_residual_boundary_anchor_slope_bound"]
        ),
        "root_slice_residual_boundary_field_slope_bound": (
            root_profile["root_slice_residual_boundary_field_slope_bound"]
        ),
        "root_slice_residual_active_lifted_core_slope_bound": (
            root_profile["root_slice_residual_active_lifted_core_slope_bound"]
        ),
        "root_slice_recursive_arrangement_bound": (
            root_profile["root_slice_recursive_arrangement_bound"]
        ),
        "root_slice_recursive_boundary_slope_bound": (
            root_profile["root_slice_recursive_boundary_slope_bound"]
        ),
        "root_slice_recursive_boundary_anchor_slope_bound": (
            root_profile["root_slice_recursive_boundary_anchor_slope_bound"]
        ),
        "root_slice_recursive_boundary_field_slope_bound": (
            root_profile["root_slice_recursive_boundary_field_slope_bound"]
        ),
        "root_slice_recursive_active_field_slope_bound": (
            root_profile["root_slice_recursive_active_field_slope_bound"]
        ),
        "root_slice_recursive_new_escape_bound": (
            root_profile["root_slice_recursive_new_escape_bound"]
        ),
        "root_slice_recursive_active_new_escape_bound": (
            root_profile["root_slice_recursive_active_new_escape_bound"]
        ),
        "root_slice_recursive_active_face_new_escape_bound": (
            root_profile["root_slice_recursive_active_face_new_escape_bound"]
        ),
        "root_slice_exact_active_face_bound": (
            root_profile["root_slice_exact_active_face_bound"]
        ),
        "root_slice_recursive_active_face_new_root_bound": (
            root_profile["root_slice_recursive_active_face_new_root_bound"]
        ),
        "root_slice_two_input_field_bound": root_profile[
            "root_slice_two_input_field_bound"
        ],
        "root_slice_lifted_u_t1_cores": root_profile["root_slice_lifted_u_t1_cores"],
        "root_slice_lifted_v_t1_cores": root_profile["root_slice_lifted_v_t1_cores"],
        "root_slice_lifted_common_cores": root_profile["root_slice_lifted_common_cores"],
        "root_slice_lifted_common_active_cores": (
            root_profile["root_slice_lifted_common_active_cores"]
        ),
        "root_slice_lifted_common_inactive_cores": (
            root_profile["root_slice_lifted_common_inactive_cores"]
        ),
        "root_slice_lifted_common_core_noncontained_faces": (
            root_profile["root_slice_lifted_common_core_noncontained_faces"]
        ),
        "root_slice_lifted_common_core_aperiodic_faces": (
            root_profile["root_slice_lifted_common_core_aperiodic_faces"]
        ),
        "root_slice_lifted_common_core_residual_faces": (
            root_profile["root_slice_lifted_common_core_residual_faces"]
        ),
        "root_slice_lifted_common_core_peeled_faces": (
            root_profile["root_slice_lifted_common_core_peeled_faces"]
        ),
        "root_slice_lifted_common_core_residual_singletons": (
            root_profile["root_slice_lifted_common_core_residual_singletons"]
        ),
        "root_slice_lifted_common_core_residual_packets": (
            root_profile["root_slice_lifted_common_core_residual_packets"]
        ),
        "root_slice_lifted_common_core_max_residual_faces": (
            root_profile["root_slice_lifted_common_core_max_residual_faces"]
        ),
        "root_slice_lifted_common_core_common_base_checks": (
            root_profile["root_slice_lifted_common_core_common_base_checks"]
        ),
        "root_slice_lifted_common_core_residual_slope_checks": (
            root_profile["root_slice_lifted_common_core_residual_slope_checks"]
        ),
        "root_slice_lifted_common_core_active_ratio_checks": (
            root_profile["root_slice_lifted_common_core_active_ratio_checks"]
        ),
        "root_slice_lifted_common_core_residual_slope_pair_checks": (
            root_profile["root_slice_lifted_common_core_residual_slope_pair_checks"]
        ),
        "root_slice_lifted_common_core_residual_slope_fiber_max": (
            root_profile["root_slice_lifted_common_core_residual_slope_fiber_max"]
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
        "max_aperiodic_one_exchange_pairs": max(
            row["aperiodic_one_exchange_pairs"] for row in rows
        ),
        "max_aperiodic_strict_degree": max(row["aperiodic_max_strict_degree"] for row in rows),
        "max_aperiodic_same_slope_one_exchange_pairs": max(
            row["aperiodic_same_slope_one_exchange_pairs"] for row in rows
        ),
        "max_same_slope_one_exchange_root_slices": max(
            row["same_slope_one_exchange_root_slices"] for row in rows
        ),
        "max_same_slope_one_exchange_root_slopes": max(
            row["same_slope_one_exchange_root_slopes"] for row in rows
        ),
        "max_same_slope_one_exchange_next_core_locators": max(
            row["same_slope_one_exchange_next_core_locators"] for row in rows
        ),
        "max_same_slope_one_exchange_next_slopes": max(
            row["same_slope_one_exchange_next_slopes"] for row in rows
        ),
        "max_same_slope_one_exchange_member_checks": max(
            row["same_slope_one_exchange_member_checks"] for row in rows
        ),
        "max_same_slope_one_exchange_noncontained": max(
            row["same_slope_one_exchange_noncontained_max"] for row in rows
        ),
        "max_same_slope_one_exchange_aperiodic_members": max(
            row["same_slope_one_exchange_aperiodic_members_max"] for row in rows
        ),
        "max_two_exchange_pairs": max(row["two_exchange_pairs"] for row in rows),
        "max_two_exchange_same_slope_pairs": max(
            row["two_exchange_same_slope_pairs"] for row in rows
        ),
        "max_two_exchange_different_slope_pairs": max(
            row["two_exchange_different_slope_pairs"] for row in rows
        ),
        "max_two_exchange_cores": max(row["two_exchange_cores"] for row in rows),
        "max_two_exchange_slices_checked": max(
            row["two_exchange_slices_checked"] for row in rows
        ),
        "max_two_exchange_minor_polynomial_checks": max(
            row["two_exchange_minor_polynomial_checks"] for row in rows
        ),
        "max_two_exchange_bad_locator_checks": max(
            row["two_exchange_bad_locator_checks"] for row in rows
        ),
        "max_two_exchange_slice_aperiodic_locators": max(
            row["two_exchange_max_slice_aperiodic_locators"] for row in rows
        ),
        "max_two_exchange_slice_slope_image": max(
            row["two_exchange_max_slice_slope_image"] for row in rows
        ),
        "max_two_exchange_same_slope_clusters": max(
            row["two_exchange_same_slope_clusters"] for row in rows
        ),
        "max_two_exchange_same_slope_line_clusters": max(
            row["two_exchange_same_slope_line_clusters"] for row in rows
        ),
        "max_two_exchange_same_slope_fixed_root_lines": max(
            row["two_exchange_same_slope_fixed_root_lines"] for row in rows
        ),
        "max_two_exchange_same_slope_mobius_lines": max(
            row["two_exchange_same_slope_mobius_lines"] for row in rows
        ),
        "max_two_exchange_same_slope_product_mobius_lines": max(
            row["two_exchange_same_slope_product_mobius_lines"] for row in rows
        ),
        "max_two_exchange_same_slope_sum_mobius_lines": max(
            row["two_exchange_same_slope_sum_mobius_lines"] for row in rows
        ),
        "max_two_exchange_same_slope_line_two_exchange_pairs": max(
            row["two_exchange_same_slope_line_two_exchange_pairs"] for row in rows
        ),
        "max_two_exchange_same_slope_mobius_two_exchange_pairs": max(
            row["two_exchange_same_slope_mobius_two_exchange_pairs"] for row in rows
        ),
        "max_two_exchange_same_slope_mobius_pair_checks": max(
            row["two_exchange_same_slope_mobius_pair_checks"] for row in rows
        ),
        "max_two_exchange_same_slope_mobius_member": max(
            row["two_exchange_same_slope_mobius_member_max"] for row in rows
        ),
        "max_two_exchange_same_slope_plane_clusters": max(
            row["two_exchange_same_slope_plane_clusters"] for row in rows
        ),
        "max_two_exchange_same_slope_plane_lifts": max(
            row["two_exchange_same_slope_plane_lifts"] for row in rows
        ),
        "max_two_exchange_same_slope_plane_two_exchange_pairs": max(
            row["two_exchange_same_slope_plane_two_exchange_pairs"] for row in rows
        ),
        "max_two_exchange_same_slope_affine_member": max(
            row["two_exchange_same_slope_affine_member_max"] for row in rows
        ),
        "max_two_exchange_same_slope_lift_checks": max(
            row["two_exchange_same_slope_lift_checks"] for row in rows
        ),
        "max_two_exchange_det_line_components": max(
            row["two_exchange_det_line_components"] for row in rows
        ),
        "max_two_exchange_det_line_fixed_root": max(
            row["two_exchange_det_line_fixed_root"] for row in rows
        ),
        "max_two_exchange_det_line_product_mobius": max(
            row["two_exchange_det_line_product_mobius"] for row in rows
        ),
        "max_two_exchange_det_line_sum_mobius": max(
            row["two_exchange_det_line_sum_mobius"] for row in rows
        ),
        "max_two_exchange_det_line_constant_slope": max(
            row["two_exchange_det_line_constant_slope"] for row in rows
        ),
        "max_two_exchange_det_line_variable_slope": max(
            row["two_exchange_det_line_variable_slope"] for row in rows
        ),
        "max_two_exchange_det_line_slope": max(
            row["two_exchange_det_line_slope_max"] for row in rows
        ),
        "max_two_exchange_det_line_aperiodic": max(
            row["two_exchange_det_line_aperiodic_max"] for row in rows
        ),
        "max_two_exchange_det_line_point_checks": max(
            row["two_exchange_det_line_point_checks"] for row in rows
        ),
        "max_two_exchange_det_full_planes": max(
            row["two_exchange_det_full_planes"] for row in rows
        ),
        "max_two_exchange_det_full_plane_constant_slope": max(
            row["two_exchange_det_full_plane_constant_slope"] for row in rows
        ),
        "max_two_exchange_det_full_plane_variable_slope": max(
            row["two_exchange_det_full_plane_variable_slope"] for row in rows
        ),
        "max_two_exchange_det_full_plane_contained": max(
            row["two_exchange_det_full_plane_contained"] for row in rows
        ),
        "max_two_exchange_det_full_plane_den_rank": max(
            row["two_exchange_det_full_plane_den_rank_max"] for row in rows
        ),
        "max_two_exchange_det_full_plane_slope": max(
            row["two_exchange_det_full_plane_slope_max"] for row in rows
        ),
        "max_two_exchange_det_full_plane_aperiodic": max(
            row["two_exchange_det_full_plane_aperiodic_max"] for row in rows
        ),
        "max_two_exchange_det_full_plane_lifts": max(
            row["two_exchange_det_full_plane_lifts"] for row in rows
        ),
        "max_two_exchange_det_proper_lines": max(
            row["two_exchange_det_proper_lines"] for row in rows
        ),
        "max_two_exchange_det_proper_line_fixed_root": max(
            row["two_exchange_det_proper_line_fixed_root"] for row in rows
        ),
        "max_two_exchange_det_proper_line_product_mobius": max(
            row["two_exchange_det_proper_line_product_mobius"] for row in rows
        ),
        "max_two_exchange_det_proper_line_sum_mobius": max(
            row["two_exchange_det_proper_line_sum_mobius"] for row in rows
        ),
        "max_two_exchange_det_proper_line_constant_slope": max(
            row["two_exchange_det_proper_line_constant_slope"] for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_slope": max(
            row["two_exchange_det_proper_line_variable_slope"] for row in rows
        ),
        "max_two_exchange_det_proper_line_slope": max(
            row["two_exchange_det_proper_line_slope_max"] for row in rows
        ),
        "max_two_exchange_det_proper_line_aperiodic": max(
            row["two_exchange_det_proper_line_aperiodic_max"] for row in rows
        ),
        "max_two_exchange_det_proper_line_core": max(
            row["two_exchange_det_proper_line_core_max"] for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_injective": max(
            row["two_exchange_det_proper_line_variable_injective"] for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_pole": max(
            row["two_exchange_det_proper_line_variable_pole_max"] for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_aperiodic_slope": max(
            row["two_exchange_det_proper_line_variable_aperiodic_slope_max"]
            for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_injective_checks": max(
            row["two_exchange_det_proper_line_variable_injective_checks"]
            for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_aperiodic_slopes": max(
            row["two_exchange_det_proper_line_variable_aperiodic_slopes"]
            for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_new_slopes": max(
            row["two_exchange_det_proper_line_variable_new_slopes"] for row in rows
        ),
        "max_two_exchange_det_proper_line_variable_charged_slope_checks": max(
            row["two_exchange_det_proper_line_variable_charged_slope_checks"]
            for row in rows
        ),
        "max_root_slices": max(row["root_slices"] for row in rows),
        "max_root_slice_noncontained": max(row["max_root_slice_noncontained"] for row in rows),
        "max_root_slice_total_slope_bound": max(
            row["root_slice_total_slope_bound"] for row in rows
        ),
        "max_root_slice_new_slope_count": max(
            row["root_slice_new_slope_count"] for row in rows
        ),
        "max_root_slice_t3_core_locators": max(
            row["root_slice_t3_core_locators"] for row in rows
        ),
        "max_root_slice_t3_slope_count": max(
            row["root_slice_t3_slope_count"] for row in rows
        ),
        "max_root_slice_t3_new_slope_count": max(
            row["root_slice_t3_new_slope_count"] for row in rows
        ),
        "max_root_slice_recursive_slope_bound": max(
            row["root_slice_recursive_slope_bound"] for row in rows
        ),
        "max_root_slice_members": max(row["root_slice_members"] for row in rows),
        "max_root_slice_residual_locators": max(row["root_slice_residual_locators"] for row in rows),
        "max_root_slice_residual_slopes": max(row["root_slice_residual_slopes"] for row in rows),
        "max_root_slice_residual_slope_fiber": max(
            row["root_slice_residual_max_slope_fiber"] for row in rows
        ),
        "max_root_slice_residual_slope_core_checks": max(
            row["root_slice_residual_slope_core_checks"] for row in rows
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
        "max_root_slice_residual_top_packet_overlap_pairs": max(
            row["root_slice_residual_top_packet_overlap_pairs"] for row in rows
        ),
        "max_root_slice_residual_top_packet_overlap": max(
            row["root_slice_residual_top_packet_overlap_max"] for row in rows
        ),
        "max_root_slice_residual_components": max(
            row["root_slice_residual_components"] for row in rows
        ),
        "max_root_slice_residual_nontrivial_components": max(
            row["root_slice_residual_nontrivial_components"] for row in rows
        ),
        "max_root_slice_residual_isolated_components": max(
            row["root_slice_residual_isolated_components"] for row in rows
        ),
        "max_root_slice_residual_boundary_isolated_components": max(
            row["root_slice_residual_boundary_isolated_components"] for row in rows
        ),
        "max_root_slice_residual_component_size": max(
            row["root_slice_residual_component_max"] for row in rows
        ),
        "max_root_slice_residual_component_clique_edges": max(
            row["root_slice_residual_component_clique_edges"] for row in rows
        ),
        "max_root_slice_residual_common_companion_checks": max(
            row["root_slice_residual_common_companion_checks"] for row in rows
        ),
        "max_root_slice_residual_top_lift_gate_checks": max(
            row["root_slice_residual_top_lift_gate_checks"] for row in rows
        ),
        "max_root_slice_residual_top_anchor_checks": max(
            row["root_slice_residual_top_anchor_checks"] for row in rows
        ),
        "max_root_slice_residual_top_common_lift_gate_checks": max(
            row["root_slice_residual_top_common_lift_gate_checks"] for row in rows
        ),
        "max_root_slice_residual_top_numerator_anchor_checks": max(
            row["root_slice_residual_top_numerator_anchor_checks"] for row in rows
        ),
        "max_root_slice_residual_top_face_gate_checks": max(
            row["root_slice_residual_top_face_gate_checks"] for row in rows
        ),
        "max_root_slice_residual_top_face_noncontained": max(
            row["root_slice_residual_top_face_noncontained"] for row in rows
        ),
        "max_root_slice_residual_top_face_aperiodic": max(
            row["root_slice_residual_top_face_aperiodic"] for row in rows
        ),
        "max_root_slice_residual_top_face_residual": max(
            row["root_slice_residual_top_face_residual"] for row in rows
        ),
        "max_root_slice_residual_top_face_peeled": max(
            row["root_slice_residual_top_face_peeled"] for row in rows
        ),
        "max_root_slice_residual_anchor_lifted_faces": max(
            row["root_slice_residual_anchor_lifted_faces"] for row in rows
        ),
        "max_root_slice_residual_anchor_escape_locators": max(
            row["root_slice_residual_anchor_escape_locators"] for row in rows
        ),
        "max_root_slice_residual_anchor_beta0_zero": max(
            row["root_slice_residual_anchor_beta0_zero"] for row in rows
        ),
        "max_root_slice_residual_anchor_in_support": max(
            row["root_slice_residual_anchor_in_support"] for row in rows
        ),
        "max_root_slice_residual_anchor_outside_domain": max(
            row["root_slice_residual_anchor_outside_domain"] for row in rows
        ),
        "max_root_slice_residual_external_anchors": max(
            row["root_slice_residual_external_anchors"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_locator": max(
            row["root_slice_residual_external_anchor_locator_max"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_slope": max(
            row["root_slice_residual_external_anchor_slope_max"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_slope_fibers": max(
            row["root_slice_residual_external_anchor_slope_fibers"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_slope_fiber": max(
            row["root_slice_residual_external_anchor_slope_fiber_max"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_slope_core_checks": max(
            row["root_slice_residual_external_anchor_slope_core_checks"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_kernel_dim": max(
            row["root_slice_residual_external_anchor_kernel_dim_max"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_projective_points": max(
            row["root_slice_residual_external_anchor_projective_points"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_rich_points": max(
            row["root_slice_residual_external_anchor_rich_points"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_finite_rich_slopes": max(
            row["root_slice_residual_external_anchor_finite_rich_slopes"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_rich_residual_classes": max(
            row["root_slice_residual_external_anchor_rich_residual_classes"]
            for row in rows
        ),
        "max_root_slice_residual_external_anchor_twist_checks": max(
            row["root_slice_residual_external_anchor_twist_checks"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_interpolation_checks": max(
            row["root_slice_residual_external_anchor_interpolation_checks"] for row in rows
        ),
        "max_root_slice_residual_external_anchor_pinned_t1_checks": max(
            row["root_slice_residual_external_anchor_pinned_t1_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_lift_gate_checks": max(
            row["root_slice_residual_anchor_lift_gate_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_isolated_checks": max(
            row["root_slice_residual_anchor_isolated_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_projective_lift_checks": max(
            row["root_slice_residual_anchor_projective_lift_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_projective_unique_checks": max(
            row["root_slice_residual_anchor_projective_unique_checks"] for row in rows
        ),
        "max_root_slice_residual_projective_lift_fibers": max(
            row["root_slice_residual_projective_lift_fibers"] for row in rows
        ),
        "max_root_slice_residual_projective_squarefree_fibers": max(
            row["root_slice_residual_projective_squarefree_fibers"] for row in rows
        ),
        "max_root_slice_residual_projective_boundary_fibers": max(
            row["root_slice_residual_projective_boundary_fibers"] for row in rows
        ),
        "max_root_slice_residual_projective_boundary_singletons": max(
            row["root_slice_residual_projective_boundary_singletons"] for row in rows
        ),
        "max_root_slice_residual_projective_lift_fiber": max(
            row["root_slice_residual_projective_lift_fiber_max"] for row in rows
        ),
        "max_root_slice_residual_projective_lift_pair_checks": max(
            row["root_slice_residual_projective_lift_pair_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_finite_lift_checks": max(
            row["root_slice_residual_anchor_finite_lift_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_repeated_lift_checks": max(
            row["root_slice_residual_anchor_repeated_lift_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_offdomain_lift_checks": max(
            row["root_slice_residual_anchor_offdomain_lift_checks"] for row in rows
        ),
        "max_root_slice_residual_anchor_infinity_checks": max(
            row["root_slice_residual_anchor_infinity_checks"] for row in rows
        ),
        "max_root_slice_residual_lifted_slopes": max(
            row["root_slice_residual_lifted_slopes"] for row in rows
        ),
        "max_root_slice_residual_escape_slopes": max(
            row["root_slice_residual_escape_slopes"] for row in rows
        ),
        "max_root_slice_residual_lifted_escape_slope_overlap": max(
            row["root_slice_residual_lifted_escape_slope_overlap"] for row in rows
        ),
        "max_root_slice_residual_escape_new_slopes": max(
            row["root_slice_residual_escape_new_slopes"] for row in rows
        ),
        "max_root_slice_residual_lifted_core_slope_bound": max(
            row["root_slice_residual_lifted_core_slope_bound"] for row in rows
        ),
        "max_root_slice_residual_recursion_bound": max(
            row["root_slice_residual_recursion_bound"] for row in rows
        ),
        "max_root_slice_residual_new_escape_bound": max(
            row["root_slice_residual_new_escape_bound"] for row in rows
        ),
        "max_root_slice_residual_active_new_escape_bound": max(
            row["root_slice_residual_active_new_escape_bound"] for row in rows
        ),
        "max_root_slice_residual_active_face_new_escape_bound": max(
            row["root_slice_residual_active_face_new_escape_bound"] for row in rows
        ),
        "max_root_slice_residual_boundary_arrangement_bound": max(
            row["root_slice_residual_boundary_arrangement_bound"] for row in rows
        ),
        "max_root_slice_residual_boundary_slope_bound": max(
            row["root_slice_residual_boundary_slope_bound"] for row in rows
        ),
        "max_root_slice_residual_boundary_active_anchors": max(
            row["root_slice_residual_boundary_active_anchors"] for row in rows
        ),
        "max_root_slice_residual_boundary_anchor_slope_bound": max(
            row["root_slice_residual_boundary_anchor_slope_bound"] for row in rows
        ),
        "max_root_slice_residual_boundary_field_slope_bound": max(
            row["root_slice_residual_boundary_field_slope_bound"] for row in rows
        ),
        "max_root_slice_residual_active_lifted_core_slope_bound": max(
            row["root_slice_residual_active_lifted_core_slope_bound"] for row in rows
        ),
        "max_root_slice_recursive_arrangement_bound": max(
            row["root_slice_recursive_arrangement_bound"] for row in rows
        ),
        "max_root_slice_recursive_boundary_slope_bound": max(
            row["root_slice_recursive_boundary_slope_bound"] for row in rows
        ),
        "max_root_slice_recursive_boundary_anchor_slope_bound": max(
            row["root_slice_recursive_boundary_anchor_slope_bound"] for row in rows
        ),
        "max_root_slice_recursive_boundary_field_slope_bound": max(
            row["root_slice_recursive_boundary_field_slope_bound"] for row in rows
        ),
        "max_root_slice_recursive_active_field_slope_bound": max(
            row["root_slice_recursive_active_field_slope_bound"] for row in rows
        ),
        "max_root_slice_recursive_new_escape_bound": max(
            row["root_slice_recursive_new_escape_bound"] for row in rows
        ),
        "max_root_slice_recursive_active_new_escape_bound": max(
            row["root_slice_recursive_active_new_escape_bound"] for row in rows
        ),
        "max_root_slice_recursive_active_face_new_escape_bound": max(
            row["root_slice_recursive_active_face_new_escape_bound"] for row in rows
        ),
        "max_root_slice_exact_active_face_bound": max(
            row["root_slice_exact_active_face_bound"] for row in rows
        ),
        "max_root_slice_recursive_active_face_new_root_bound": max(
            row["root_slice_recursive_active_face_new_root_bound"] for row in rows
        ),
        "max_root_slice_two_input_field_bound": max(
            row["root_slice_two_input_field_bound"] for row in rows
        ),
        "max_root_slice_lifted_u_t1_cores": max(
            row["root_slice_lifted_u_t1_cores"] for row in rows
        ),
        "max_root_slice_lifted_v_t1_cores": max(
            row["root_slice_lifted_v_t1_cores"] for row in rows
        ),
        "max_root_slice_lifted_common_cores": max(
            row["root_slice_lifted_common_cores"] for row in rows
        ),
        "max_root_slice_lifted_common_active_cores": max(
            row["root_slice_lifted_common_active_cores"] for row in rows
        ),
        "max_root_slice_lifted_common_inactive_cores": max(
            row["root_slice_lifted_common_inactive_cores"] for row in rows
        ),
        "max_root_slice_lifted_common_core_noncontained_faces": max(
            row["root_slice_lifted_common_core_noncontained_faces"] for row in rows
        ),
        "max_root_slice_lifted_common_core_aperiodic_faces": max(
            row["root_slice_lifted_common_core_aperiodic_faces"] for row in rows
        ),
        "max_root_slice_lifted_common_core_residual_faces": max(
            row["root_slice_lifted_common_core_residual_faces"] for row in rows
        ),
        "max_root_slice_lifted_common_core_peeled_faces": max(
            row["root_slice_lifted_common_core_peeled_faces"] for row in rows
        ),
        "max_root_slice_lifted_common_core_residual_singletons": max(
            row["root_slice_lifted_common_core_residual_singletons"] for row in rows
        ),
        "max_root_slice_lifted_common_core_residual_packets": max(
            row["root_slice_lifted_common_core_residual_packets"] for row in rows
        ),
        "max_root_slice_lifted_common_core_residual_faces_per_core": max(
            row["root_slice_lifted_common_core_max_residual_faces"] for row in rows
        ),
        "max_root_slice_lifted_common_core_common_base_checks": max(
            row["root_slice_lifted_common_core_common_base_checks"] for row in rows
        ),
        "max_root_slice_lifted_common_core_residual_slope_checks": max(
            row["root_slice_lifted_common_core_residual_slope_checks"] for row in rows
        ),
        "max_root_slice_lifted_common_core_active_ratio_checks": max(
            row["root_slice_lifted_common_core_active_ratio_checks"] for row in rows
        ),
        "max_root_slice_lifted_common_core_residual_slope_pair_checks": max(
            row["root_slice_lifted_common_core_residual_slope_pair_checks"] for row in rows
        ),
        "max_root_slice_lifted_common_core_residual_slope_fiber": max(
            row["root_slice_lifted_common_core_residual_slope_fiber_max"] for row in rows
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


def verify_boundary_only_projective_lift_probe(summary: dict[str, object]) -> None:
    case = summary["case"]
    if case.name != "F13_order12_j4_t2":
        raise AssertionError("boundary-only probe was called on the wrong case")
    for row in summary["rows"]:
        if row["root_slice_residual_slopes"] == 0:
            raise AssertionError("boundary-only probe had no residual slopes")
        if row["root_slice_lifted_common_cores"] != 0:
            raise AssertionError("boundary-only probe unexpectedly had lifted common cores")
        if row["root_slice_residual_lifted_slopes"] != 0:
            raise AssertionError("boundary-only probe unexpectedly had lifted slopes")
        if row["root_slice_residual_projective_squarefree_fibers"] != 0:
            raise AssertionError("boundary-only probe had squarefree projective fibers")
        if (
            row["root_slice_residual_projective_boundary_singletons"]
            != row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe did not have singleton boundary fibers")
        if (
            row["root_slice_residual_anchor_outside_domain"]
            != row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe was not purely off-domain")
        if row["root_slice_residual_external_anchors"] != 1:
            raise AssertionError("boundary-only probe did not have a single external anchor")
        if row["root_slice_residual_external_anchor_values"] != (0,):
            raise AssertionError("boundary-only probe did not use external anchor 0")
        if (
            row["root_slice_residual_external_anchor_locator_max"]
            != row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe did not concentrate on one anchor")
        if (
            row["root_slice_residual_external_anchor_slope_max"]
            != row["root_slice_residual_slopes"]
        ):
            raise AssertionError("boundary-only probe slopes did not share one anchor")
        if (
            row["root_slice_residual_external_anchor_slope_fibers"]
            != row["root_slice_residual_slopes"]
        ):
            raise AssertionError("boundary-only probe had wrong anchor-slope fibers")
        if row["root_slice_residual_external_anchor_slope_fiber_max"] != 4:
            raise AssertionError("boundary-only probe had wrong anchor-slope fiber size")
        if (
            row["root_slice_residual_external_anchor_slope_core_checks"]
            != 4 * row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe missed anchor-slope packing checks")
        if row["root_slice_residual_external_anchor_kernel_dim_max"] != 4:
            raise AssertionError("boundary-only probe had wrong fixed-anchor kernel dimension")
        if row["root_slice_residual_external_anchor_projective_points"] != 2380:
            raise AssertionError("boundary-only probe had wrong projective kernel size")
        if row["root_slice_residual_external_anchor_rich_points"] != 39:
            raise AssertionError("boundary-only probe had wrong rich-point count")
        if row["root_slice_residual_external_anchor_finite_rich_slopes"] != 9:
            raise AssertionError("boundary-only probe had wrong rich-slope image")
        if (
            row["root_slice_residual_external_anchor_rich_residual_classes"]
            != row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe missed residual rich classes")
        if (
            row["root_slice_residual_external_anchor_twist_checks"]
            != row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe missed external twist checks")
        if (
            row["root_slice_residual_external_anchor_pinned_t1_checks"]
            != row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe missed pinned t=1 checks")
        if (
            row["root_slice_residual_external_anchor_interpolation_checks"]
            != row["root_slice_residual_locators"]
        ):
            raise AssertionError("boundary-only probe missed interpolation checks")
        if (
            row["root_slice_residual_escape_new_slopes"]
            != row["root_slice_residual_slopes"]
        ):
            raise AssertionError("boundary-only probe slopes were absorbed by lifted side")


def verify_f13_boundary_zero_sum_product_model(case: Case) -> dict[str, int]:
    if (
        case.name != "F13_order12_j4_t2"
        or case.p != 13
        or case.n != 12
        or case.j != 4
        or case.t != 2
    ):
        raise AssertionError("zero-sum product model was called on the wrong case")
    domain, exponents, _ = cyclic_domain(case.p, case.n)
    expected_residual_products = {1: 4, 3: 4, 7: 4, 8: 4, 9: 4, 11: 4}
    checked_seeds = 0
    for seed in case.seeds:
        f = {x: word_value("f", x, case.p, seed) for x in domain}
        g = {x: word_value("g", x, case.p, seed) for x in domain}
        u = syndrome(f, domain, case.j + case.t, case.p)
        v = syndrome(g, domain, case.j + case.t, case.p)
        expected_numerator_top = (2 * seed + 3) % case.p
        expected_denominator_factor = (3 * seed + 1) % case.p
        zero_sum_locators = 0
        quotient_zero_sum_locators = 0
        residual_product_counts: dict[int, int] = {}
        residual_product_slopes: dict[int, set[int]] = {}
        for complement in combinations(domain, case.j):
            complement_sum = sum(complement) % case.p
            complement_product = 1
            for root in complement:
                complement_product = complement_product * root % case.p
            ell = locator(complement, case.p)
            a_vec = hankel_apply(u, case.t, case.j, ell, case.p)
            b_vec = hankel_apply(v, case.t, case.j, ell, case.p)
            slope = slope_from_gate(a_vec, b_vec, case.p)
            bad = slope is not None and any(value != 0 for value in b_vec)
            zero_sum = complement_sum == 0
            if bad != zero_sum:
                raise AssertionError("F13 boundary model bad locus was not zero-sum")
            if not zero_sum:
                continue
            zero_sum_locators += 1
            if a_vec != (expected_numerator_top, 0):
                raise AssertionError("F13 zero-sum numerator top row had wrong form")
            expected_denominator_top = (
                expected_denominator_factor * complement_product
            ) % case.p
            if b_vec != (expected_denominator_top, 0):
                raise AssertionError("F13 zero-sum denominator top row had wrong form")
            expected_slope = (
                -expected_numerator_top * inv_mod(expected_denominator_top, case.p)
            ) % case.p
            if slope != expected_slope:
                raise AssertionError("F13 zero-sum product slope formula failed")
            if is_quotient_periodic(
                complement, domain, exponents, case.charged_fiber_sizes
            ):
                quotient_zero_sum_locators += 1
                continue
            residual_product_counts[complement_product] = (
                residual_product_counts.get(complement_product, 0) + 1
            )
            residual_product_slopes.setdefault(complement_product, set()).add(slope)
        if zero_sum_locators != 39:
            raise AssertionError("F13 boundary model had wrong zero-sum count")
        if quotient_zero_sum_locators != 15:
            raise AssertionError("F13 boundary model had wrong quotient zero-sum count")
        if residual_product_counts != expected_residual_products:
            raise AssertionError("F13 residual product fibers had wrong sizes")
        if any(len(slopes) != 1 for slopes in residual_product_slopes.values()):
            raise AssertionError("F13 residual product fiber had multiple slopes")
        if len({next(iter(slopes)) for slopes in residual_product_slopes.values()}) != 6:
            raise AssertionError("F13 residual product fibers did not give six slopes")
        checked_seeds += 1
    if checked_seeds != 4:
        raise AssertionError("F13 boundary model did not check four seeds")
    return {
        "seeds": checked_seeds,
        "zero_sum_locators": 39,
        "quotient_zero_sum_locators": 15,
        "residual_zero_sum_locators": 24,
        "residual_product_fibers": len(expected_residual_products),
        "residual_product_fiber_size": max(expected_residual_products.values()),
    }


def verify_full_domain_monomial_boundary_model(
    p: int, j: int, charged_fiber_sizes: tuple[int, ...]
) -> dict[str, int]:
    n = p - 1
    t = 2
    if j <= 0 or p - 2 - j < 0:
        raise AssertionError("invalid monomial boundary parameters")
    domain, exponents, _ = cyclic_domain(p, n)
    f_degree = p - 2 - j
    g_degree = p - 2
    f = {x: pow(x, f_degree, p) for x in domain}
    g = {x: pow(x, g_degree, p) for x in domain}
    u = syndrome(f, domain, j + t, p)
    v = syndrome(g, domain, j + t, p)
    j_power_subgroup = {pow(root, j, p) for root in domain}
    zero_sum_locators = 0
    zero_sum_product_counts: dict[int, int] = {}
    quotient_zero_sum_locators = 0
    quotient_product_counts: dict[int, int] = {}
    quotient_scale_counts: dict[int, int] = {}
    quotient_scale_product_sets: dict[int, set[int]] = {}
    residual_product_counts: dict[int, int] = {}
    residual_product_slopes: dict[int, set[int]] = {}
    sign = -1 if j % 2 else 1
    for complement in combinations(domain, j):
        complement_sum = sum(complement) % p
        complement_product = 1
        for root in complement:
            complement_product = complement_product * root % p
        ell = locator(complement, p)
        a_vec = hankel_apply(u, t, j, ell, p)
        b_vec = hankel_apply(v, t, j, ell, p)
        expected_b0 = sign * complement_product % p
        if a_vec != (1, (-complement_sum) % p):
            raise AssertionError("monomial boundary numerator row had wrong form")
        if b_vec != (expected_b0, 0):
            raise AssertionError("monomial boundary denominator row had wrong form")
        slope = slope_from_gate(a_vec, b_vec, p)
        bad = slope is not None and any(value != 0 for value in b_vec)
        zero_sum = complement_sum == 0
        quotient_scales = quotient_periodic_scales(
            complement, domain, exponents, charged_fiber_sizes
        )
        if quotient_scales and not zero_sum:
            raise AssertionError("full-domain quotient-periodic locator was not zero-sum")
        if bad != zero_sum:
            raise AssertionError("monomial boundary bad locus was not zero-sum")
        if not zero_sum:
            continue
        zero_sum_locators += 1
        zero_sum_product_counts[complement_product] = (
            zero_sum_product_counts.get(complement_product, 0) + 1
        )
        if j == 3:
            base = complement[0]
            r = complement[1] * inv_mod(base, p) % p
            normalized_third = complement[2] * inv_mod(base, p) % p
            repeated_parameters = {1 % p, (-2) % p, (-inv_mod(2, p)) % p}
            if r == (-1) % p or r in repeated_parameters:
                raise AssertionError("j=3 normalized parameter was not distinct")
            if normalized_third != (-1 - r) % p:
                raise AssertionError("j=3 normalized zero-sum form failed")
            quadratic_value = (-r * (1 + r)) % p
            if complement_product != pow(base, 3, p) * quadratic_value % p:
                raise AssertionError("j=3 product was not a cube times -r(1+r)")
        if j == 4:
            base = complement[0]
            base_inv = inv_mod(base, p)
            r = complement[1] * base_inv % p
            s = complement[2] * base_inv % p
            normalized_fourth = complement[3] * base_inv % p
            if normalized_fourth != (-1 - r - s) % p:
                raise AssertionError("j=4 normalized zero-sum form failed")
            if 0 in {r, s, normalized_fourth}:
                raise AssertionError("j=4 normalized parameter was zero")
            if len({1 % p, r, s, normalized_fourth}) != 4:
                raise AssertionError("j=4 normalized parameter was not distinct")
            cubic_value = (-r * s * (1 + r + s)) % p
            if complement_product != pow(base, 4, p) * cubic_value % p:
                raise AssertionError(
                    "j=4 product was not a fourth power times -rs(1+r+s)"
                )
        expected_slope = -inv_mod(expected_b0, p) % p
        if slope != expected_slope:
            raise AssertionError("monomial boundary product slope formula failed")
        if quotient_scales:
            for fiber_size in quotient_scales:
                residues = quotient_periodic_scale_residues(
                    complement, domain, exponents, fiber_size
                )
                if residues is None:
                    raise AssertionError("missing quotient scale residue list")
                quotient_product = 1
                for residue in residues:
                    quotient_product = (
                        quotient_product * pow(domain[residue], fiber_size, p)
                    ) % p
                if len(residues) * (fiber_size + 1) % 2:
                    quotient_product = (-quotient_product) % p
                if quotient_product != complement_product:
                    raise AssertionError("quotient fiber product formula failed")
                quotient_scale_counts[fiber_size] = (
                    quotient_scale_counts.get(fiber_size, 0) + 1
                )
                quotient_scale_product_sets.setdefault(fiber_size, set()).add(
                    complement_product
                )
            quotient_product_counts[complement_product] = (
                quotient_product_counts.get(complement_product, 0) + 1
            )
            if j == 4 and 2 in charged_fiber_sizes:
                complement_set = set(complement)
                antipodal_union = all((-root) % p in complement_set for root in complement)
                if not antipodal_union:
                    raise AssertionError("j=4 quotient zero-sum locator was not antipodal")
            quotient_zero_sum_locators += 1
            continue
        residual_product_counts[complement_product] = (
            residual_product_counts.get(complement_product, 0) + 1
        )
        residual_product_slopes.setdefault(complement_product, set()).add(slope)
    if any(len(slopes) != 1 for slopes in residual_product_slopes.values()):
        raise AssertionError("monomial residual product fiber had multiple slopes")
    residual_slope_count = len(
        {next(iter(slopes)) for slopes in residual_product_slopes.values()}
    )
    if residual_slope_count != len(residual_product_counts):
        raise AssertionError("monomial product fibers did not inject to slopes")
    quotient_product_fibers = len(quotient_product_counts)
    quotient_product_set = set(quotient_product_counts)
    residual_product_set = set(residual_product_counts)
    zero_sum_product_set = set(zero_sum_product_counts)
    for image_name, image in (
        ("zero-sum", zero_sum_product_set),
        ("quotient", quotient_product_set),
        ("residual", residual_product_set),
    ):
        for product in image:
            for power in j_power_subgroup:
                if product * power % p not in image:
                    raise AssertionError(
                        f"monomial {image_name} product image was not j-power closed"
                    )
    quotient_product_cosets = (
        quotient_product_fibers // len(j_power_subgroup) if quotient_product_fibers else 0
    )
    residual_product_cosets = (
        len(residual_product_set) // len(j_power_subgroup) if residual_product_set else 0
    )
    zero_sum_product_cosets = (
        len(zero_sum_product_set) // len(j_power_subgroup) if zero_sum_product_set else 0
    )
    signed_count_correction = p - 1 if j % 2 == 0 else -(p - 1)
    expected_general_zero_sum = (comb(p - 1, j) + signed_count_correction) // p
    if zero_sum_locators != expected_general_zero_sum:
        raise AssertionError("general zero-sum boundary count formula failed")
    normalized_parameter_count = 0
    normalized_product_values: set[int] = set()
    for parameters in cartesian_product(domain, repeat=j - 2):
        final_parameter = (-1 - sum(parameters)) % p
        normalized_roots = (1, *parameters, final_parameter)
        if final_parameter and len(set(normalized_roots)) == j:
            normalized_parameter_count += 1
            normalized_product = final_parameter
            for parameter in parameters:
                normalized_product = normalized_product * parameter % p
            normalized_product_values.add(normalized_product)
    expected_normalized_parameters = factorial(j) * zero_sum_locators // (p - 1)
    if normalized_parameter_count != expected_normalized_parameters:
        raise AssertionError("general normalized zero-sum parameter count failed")
    normalized_product_image = {
        value * power % p
        for value in normalized_product_values
        for power in j_power_subgroup
    }
    if zero_sum_product_set != normalized_product_image:
        raise AssertionError("general normalized product image failed")
    quotient_scale_checks = 0
    quotient_scale_product_fibers = 0
    for fiber_size, image in quotient_scale_product_sets.items():
        if j % fiber_size:
            raise AssertionError("quotient scale did not divide boundary size")
        quotient_size = n // fiber_size
        selected_fibers = j // fiber_size
        expected_scale_count = comb(quotient_size, selected_fibers)
        if quotient_scale_counts[fiber_size] != expected_scale_count:
            raise AssertionError("quotient scale count formula failed")
        expected_scale_image = set()
        for residues in combinations(range(quotient_size), selected_fibers):
            scale_product = 1
            for residue in residues:
                scale_product = scale_product * pow(domain[residue], fiber_size, p) % p
            if selected_fibers * (fiber_size + 1) % 2:
                scale_product = (-scale_product) % p
            expected_scale_image.add(scale_product)
        if image != expected_scale_image:
            raise AssertionError("quotient scale product image formula failed")
        quotient_scale_checks += quotient_scale_counts[fiber_size]
        quotient_scale_product_fibers += len(image)
    if j == 4 and 2 in charged_fiber_sizes:
        j4_cubic_parameters = {
            (r, s)
            for r in domain
            for s in domain
            if (-1 - r - s) % p
            and len({1 % p, r, s, (-1 - r - s) % p}) == 4
        }
        if len(j4_cubic_parameters) != p * p - 9 * p + 26:
            raise AssertionError("j=4 normalized cubic parameter count failed")
        j4_cubic_values = {
            (-r * s * (1 + r + s)) % p for r, s in j4_cubic_parameters
        }
        if 0 in j4_cubic_values:
            raise AssertionError("j=4 cubic product image contained zero")
        j4_cubic_product_image = {
            value * power % p
            for value in j4_cubic_values
            for power in j_power_subgroup
        }
        if zero_sum_product_set != j4_cubic_product_image:
            raise AssertionError("j=4 product image was not the fourth-power cubic image")
        antipodal_pair_count = (p - 1) // 2
        expected_zero_sum = (p - 1) * (p * p - 9 * p + 26) // 24
        expected_quotient = antipodal_pair_count * (antipodal_pair_count - 1) // 2
        expected_residual = (p - 1) * (p - 5) * (p - 7) // 24
        if zero_sum_locators != expected_zero_sum:
            raise AssertionError("j=4 zero-sum boundary count formula failed")
        if quotient_zero_sum_locators != antipodal_pair_count * (antipodal_pair_count - 1) // 2:
            raise AssertionError("j=4 quotient zero-sum count was not antipodal-pair count")
        if quotient_zero_sum_locators != expected_quotient:
            raise AssertionError("j=4 quotient boundary count formula failed")
        if sum(residual_product_counts.values()) != expected_residual:
            raise AssertionError("j=4 residual boundary count formula failed")
        if quotient_product_fibers != antipodal_pair_count:
            raise AssertionError("j=4 quotient products were not the square subgroup")
        if p >= 17 and residual_product_set != set(domain):
            raise AssertionError("j=4 residual product image was not field-sized")
    if j == 3:
        expected_zero_sum = (p - 1) * (p - 5) // 6
        if zero_sum_locators != expected_zero_sum:
            raise AssertionError("j=3 zero-sum boundary count formula failed")
        if (p - 1) % 3 and p >= 11:
            if zero_sum_product_set != set(domain):
                raise AssertionError("j=3 cube-bijective product floor failed")
            if quotient_zero_sum_locators == 0 and residual_product_set != set(domain):
                raise AssertionError("j=3 cube-bijective residual floor failed")
        repeated_parameters = {1 % p, (-2) % p, (-inv_mod(2, p)) % p}
        j3_quadratic_parameters = {
            r
            for r in domain
            if r != (-1) % p and r not in repeated_parameters
        }
        j3_quadratic_values = {(-r * (1 + r)) % p for r in j3_quadratic_parameters}
        if 0 in j3_quadratic_values:
            raise AssertionError("j=3 quadratic product image contained zero")
        j3_quadratic_product_image = {
            value * power % p
            for value in j3_quadratic_values
            for power in j_power_subgroup
        }
        if zero_sum_product_set != j3_quadratic_product_image:
            raise AssertionError("j=3 product image was not the cube-closed quadratic image")
        expected_quotient_products = set()
        if 3 in charged_fiber_sizes and (p - 1) % 3 == 0:
            expected_quotient_products = set(j_power_subgroup)
            if quotient_zero_sum_locators != (p - 1) // 3:
                raise AssertionError("j=3 quotient zero-sum count was not the 3-coset count")
            if quotient_product_set != expected_quotient_products:
                raise AssertionError("j=3 quotient product image was not the cube subgroup")
            if p >= 31 and residual_product_set != set(domain):
                raise AssertionError("j=3 cubic-character residual floor failed")
        if all(3 % size for size in charged_fiber_sizes):
            if quotient_zero_sum_locators != 0:
                raise AssertionError("j=3 boundary count had an impossible quotient charge")
            if sum(residual_product_counts.values()) != expected_zero_sum:
                raise AssertionError("j=3 residual boundary count formula failed")
    return {
        "p": p,
        "j": j,
        "zero_sum_locators": zero_sum_locators,
        "zero_sum_product_fibers": len(zero_sum_product_counts),
        "zero_sum_product_cosets": zero_sum_product_cosets,
        "normalized_parameters": normalized_parameter_count,
        "normalized_product_values": len(normalized_product_values),
        "quotient_zero_sum_locators": quotient_zero_sum_locators,
        "quotient_scale_checks": quotient_scale_checks,
        "quotient_scale_product_fibers": quotient_scale_product_fibers,
        "quotient_product_fibers": quotient_product_fibers,
        "quotient_product_cosets": quotient_product_cosets,
        "quotient_residual_product_overlap": len(quotient_product_set & residual_product_set),
        "residual_zero_sum_locators": sum(residual_product_counts.values()),
        "residual_product_fibers": len(residual_product_counts),
        "residual_product_cosets": residual_product_cosets,
        "residual_product_fiber_size": max(residual_product_counts.values(), default=0),
        "j_power_subgroup_size": len(j_power_subgroup),
    }


def verify_j4_pair_product_floor_argument(primes: tuple[int, ...] = (53, 59, 61)) -> dict[str, int]:
    min_ordered_pair_representations = None
    min_good_representations = None
    max_excluded_representations = 0
    for p in primes:
        inv2 = inv_mod(2, p)
        pair_products: list[tuple[int, int, int]] = []
        for x in range(p):
            if x in (0, 1, inv2):
                continue
            pair_products.append((x * (1 - x) % p, x, (1 - x) % p))
        for target in range(1, p):
            ordered_pair_representations = 0
            excluded_representations = 0
            good_representations = 0
            for left_product, x, one_minus_x in pair_products:
                for right_product, u, _one_minus_u in pair_products:
                    if left_product * right_product % p != target:
                        continue
                    ordered_pair_representations += 1
                    candidate = (x, one_minus_x, (-u) % p, (u - 1) % p)
                    candidate_set = set(candidate)
                    antipodal = all((-root) % p in candidate_set for root in candidate)
                    if 0 in candidate_set or len(candidate_set) != 4 or antipodal:
                        excluded_representations += 1
                    else:
                        good_representations += 1
            if ordered_pair_representations <= 24:
                raise AssertionError("j=4 pair-product representation lower bound failed")
            if excluded_representations > 24:
                raise AssertionError("j=4 pair-product exclusion bound failed")
            if good_representations == 0:
                raise AssertionError("j=4 pair-product floor had no residual witness")
            min_ordered_pair_representations = (
                ordered_pair_representations
                if min_ordered_pair_representations is None
                else min(min_ordered_pair_representations, ordered_pair_representations)
            )
            min_good_representations = (
                good_representations
                if min_good_representations is None
                else min(min_good_representations, good_representations)
            )
            max_excluded_representations = max(
                max_excluded_representations, excluded_representations
            )
    return {
        "prime_count": len(primes),
        "min_ordered_pair_representations": min_ordered_pair_representations or 0,
        "min_good_representations": min_good_representations or 0,
        "max_excluded_representations": max_excluded_representations,
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


def verify_t3_same_slope_two_exchange_probe() -> dict[str, object]:
    case = Case(
        "F13_order12_j5_t3_same_slope_probe",
        p=13,
        n=12,
        j=5,
        t=3,
        charged_fiber_sizes=(2, 3, 4, 6),
        seeds=(),
    )
    domain, _, _ = cyclic_domain(case.p, case.n)
    f_values = (11, 2, 10, 12, 6, 0, 6, 0, 8, 5, 4, 3)
    g_values = (4, 3, 5, 8, 0, 3, 3, 3, 4, 3, 8, 9)
    f = dict(zip(domain, f_values, strict=True))
    g = dict(zip(domain, g_values, strict=True))
    row = verify_word_pair(case, "same-slope-two-exchange-probe", f, g)
    if row["two_exchange_same_slope_pairs"] != 378:
        raise AssertionError("same-slope two-exchange probe changed")
    if row["two_exchange_same_slope_line_clusters"] != 35:
        raise AssertionError("same-slope probe line cluster count changed")
    if row["two_exchange_same_slope_fixed_root_lines"] != 35:
        raise AssertionError("same-slope probe fixed-root line count changed")
    if row["two_exchange_same_slope_line_two_exchange_pairs"] != 0:
        raise AssertionError("fixed-root line clusters produced two-exchange pairs")
    if row["two_exchange_same_slope_plane_clusters"] != 1:
        raise AssertionError("same-slope probe plane cluster count changed")
    if row["two_exchange_same_slope_plane_lifts"] != 1:
        raise AssertionError("same-slope probe plane lift count changed")
    if row["two_exchange_same_slope_plane_two_exchange_pairs"] != 378:
        raise AssertionError("same-slope probe plane did not account for the two-exchange pairs")
    if row["two_exchange_det_proper_line_variable_nonfixed"] != 2:
        raise AssertionError("same-slope probe non-fixed variable-line count changed")
    if row["two_exchange_det_proper_line_variable_anchored"] != 2:
        raise AssertionError("same-slope probe variable lines were not anchored")
    if row["two_exchange_det_proper_line_variable_unanchored"] != 0:
        raise AssertionError("same-slope probe gained an unanchored variable line")
    if row["two_exchange_det_proper_line_variable_domain_pair_max"] != 3:
        raise AssertionError("same-slope probe variable-line domain packet changed")
    if row["two_exchange_det_proper_line_variable_new_slope_max"] != 0:
        raise AssertionError("same-slope probe gained a per-line new residual slope")
    return row


def verify_t3_variable_new_slope_probe() -> dict[str, object]:
    case = Case(
        "F13_order12_j5_t3_variable_new_slope_probe",
        p=13,
        n=12,
        j=5,
        t=3,
        charged_fiber_sizes=(2, 3, 4, 6),
        seeds=(),
    )
    domain, _, _ = cyclic_domain(case.p, case.n)
    f_values = (12, 4, 1, 0, 9, 4, 6, 6, 8, 5, 2, 11)
    g_values = (3, 4, 7, 0, 3, 9, 7, 0, 1, 1, 11, 7)
    f = dict(zip(domain, f_values, strict=True))
    g = dict(zip(domain, g_values, strict=True))
    row = verify_word_pair(case, "variable-new-slope-probe", f, g)
    if row["aperiodic_locators"] != 48:
        raise AssertionError("variable new-slope probe aperiodic count changed")
    if row["two_exchange_det_full_planes"] != 1:
        raise AssertionError("variable new-slope probe full-plane count changed")
    if row["two_exchange_det_full_plane_lifts"] != 1:
        raise AssertionError("variable new-slope probe full-plane lift changed")
    if row["two_exchange_det_proper_lines"] != 32:
        raise AssertionError("variable new-slope probe proper-line count changed")
    if row["two_exchange_det_proper_line_product_mobius"] != 1:
        raise AssertionError("variable new-slope probe lost its product-Mobius line")
    if row["two_exchange_det_proper_line_variable_slope"] != 1:
        raise AssertionError("variable new-slope probe lost its variable line")
    if row["two_exchange_det_proper_line_variable_aperiodic_slopes"] != 3:
        raise AssertionError("variable new-slope probe aperiodic variable slopes changed")
    if row["two_exchange_det_proper_line_variable_new_slopes"] != 1:
        raise AssertionError("variable new-slope probe lost the new residual slope")
    if row["two_exchange_det_proper_line_variable_new_slope_max"] != 1:
        raise AssertionError("variable new-slope probe per-line residual count changed")
    if row["two_exchange_det_proper_line_variable_nonfixed"] != 1:
        raise AssertionError("variable new-slope probe non-fixed line count changed")
    if row["two_exchange_det_proper_line_variable_anchored"] != 1:
        raise AssertionError("variable new-slope probe line was not anchored")
    if row["two_exchange_det_proper_line_variable_unanchored"] != 0:
        raise AssertionError("variable new-slope probe gained an unanchored line")
    if row["two_exchange_det_proper_line_variable_domain_pair_max"] != 3:
        raise AssertionError("variable new-slope probe domain packet changed")
    return row


def verify_two_exchange_line_geometry_models() -> dict[str, int]:
    p = 13

    fixed_root_points = [((3 + x) % p, (3 * x) % p) for x in (1, 2, 4)]
    fixed_key = affine_line_key(fixed_root_points, p)
    if two_root_line_model(fixed_key, p) != ("fixed_root", 3, None):
        raise AssertionError("fixed-root line model failed")

    product_points = []
    center, multiplier = 4, 5
    for x in (0, 1, 2, 6):
        y = (center + multiplier * inv_mod((x - center) % p, p)) % p
        product_points.append(((x + y) % p, x * y % p))
    product_key = affine_line_key(product_points, p)
    if two_root_line_model(product_key, p) != ("product_mobius", center, multiplier):
        raise AssertionError("product Mobius line model failed")

    sum_points = []
    total = 7
    for x in (0, 1, 3, 5):
        y = (total - x) % p
        sum_points.append((total, x * y % p))
    sum_key = affine_line_key(sum_points, p)
    if two_root_line_model(sum_key, p) != ("sum_mobius", total, None):
        raise AssertionError("sum Mobius line model failed")

    return {
        "field": p,
        "fixed_root_checks": len(fixed_root_points),
        "product_mobius_checks": len(product_points),
        "sum_mobius_checks": len(sum_points),
    }


def main() -> None:
    cases = (
        Case("F17_full_j4_t2", p=17, n=16, j=4, t=2, charged_fiber_sizes=(2, 4, 8), seeds=(0, 1, 2, 3)),
        Case("F17_order8_j3_t2", p=17, n=8, j=3, t=2, charged_fiber_sizes=(2, 4), seeds=(0, 1, 2, 3)),
        Case("F13_order12_j4_t2", p=13, n=12, j=4, t=2, charged_fiber_sizes=(2, 3, 4, 6), seeds=(0, 1, 2, 3)),
        Case("F13_order12_j7_t3", p=13, n=12, j=7, t=3, charged_fiber_sizes=(2, 3, 4, 6), seeds=(0, 1, 2, 3)),
    )
    summaries = [verify_case(case) for case in cases]
    boundary_only_summary = next(
        summary for summary in summaries if summary["case"].name == "F13_order12_j4_t2"
    )
    verify_boundary_only_projective_lift_probe(boundary_only_summary)
    boundary_product_model = verify_f13_boundary_zero_sum_product_model(
        boundary_only_summary["case"]
    )
    monomial_boundary_models = (
        verify_full_domain_monomial_boundary_model(13, 4, (2, 3, 4, 6)),
        verify_full_domain_monomial_boundary_model(13, 3, (2, 3, 4, 6)),
        verify_full_domain_monomial_boundary_model(17, 4, (2, 4, 8)),
        verify_full_domain_monomial_boundary_model(17, 3, (2, 4, 8)),
    )
    j3_bijective_cube_floor_models = (
        verify_full_domain_monomial_boundary_model(11, 3, (2, 5)),
        verify_full_domain_monomial_boundary_model(23, 3, (2, 11)),
        verify_full_domain_monomial_boundary_model(29, 3, (2, 4, 7, 14)),
    )
    j3_cubic_quotient_floor_models = (
        verify_full_domain_monomial_boundary_model(19, 3, (2, 3, 6, 9)),
        verify_full_domain_monomial_boundary_model(31, 3, (2, 3, 5, 6, 10, 15)),
        verify_full_domain_monomial_boundary_model(37, 3, (2, 3, 4, 6, 9, 12, 18)),
        verify_full_domain_monomial_boundary_model(43, 3, (2, 3, 6, 7, 14, 21)),
    )
    j4_residual_product_floor_models = (
        verify_full_domain_monomial_boundary_model(19, 4, (2, 3, 6, 9)),
        verify_full_domain_monomial_boundary_model(23, 4, (2, 11)),
        verify_full_domain_monomial_boundary_model(29, 4, (2, 4, 7, 14)),
        verify_full_domain_monomial_boundary_model(31, 4, (2, 3, 5, 6, 10, 15)),
        verify_full_domain_monomial_boundary_model(37, 4, (2, 3, 4, 6, 9, 12, 18)),
        verify_full_domain_monomial_boundary_model(41, 4, (2, 4, 5, 8, 10, 20)),
        verify_full_domain_monomial_boundary_model(43, 4, (2, 3, 6, 7, 14, 21)),
        verify_full_domain_monomial_boundary_model(47, 4, (2, 23)),
    )
    monomial_boundary_floor_cases = 0
    for model in monomial_boundary_models:
        if model["p"] == 17 and model["j"] in (3, 4):
            if model["residual_product_fibers"] != model["p"] - 1:
                raise AssertionError("F17 monomial boundary model was not field-sized")
            monomial_boundary_floor_cases += 1
    if monomial_boundary_floor_cases != 2:
        raise AssertionError("monomial boundary floor missed an F17 toy case")
    j3_bijective_cube_floor_models = (
        next(model for model in monomial_boundary_models if model["p"] == 17 and model["j"] == 3),
        *j3_bijective_cube_floor_models,
    )
    for model in j3_bijective_cube_floor_models:
        if (model["p"] - 1) % 3 == 0 or model["p"] < 11:
            raise AssertionError("j=3 cube-bijective floor model had wrong prime")
        if model["quotient_zero_sum_locators"] != 0:
            raise AssertionError("j=3 cube-bijective floor had quotient charge")
        if model["residual_product_fibers"] != model["p"] - 1:
            raise AssertionError("j=3 cube-bijective floor was not field-sized")
    j3_cubic_exception = next(
        model for model in j3_cubic_quotient_floor_models if model["p"] == 19
    )
    if j3_cubic_exception["residual_product_fibers"] != 12:
        raise AssertionError("j=3 cubic-character exception changed")
    for model in j3_cubic_quotient_floor_models:
        if (model["p"] - 1) % 3 or model["j"] != 3:
            raise AssertionError("j=3 cubic-character floor model had wrong parameters")
        if model["p"] >= 31 and model["residual_product_fibers"] != model["p"] - 1:
            raise AssertionError("j=3 cubic-character floor was not field-sized")
    j4_residual_product_floor_models = (
        next(model for model in monomial_boundary_models if model["p"] == 17 and model["j"] == 4),
        *j4_residual_product_floor_models,
    )
    for model in j4_residual_product_floor_models:
        if model["p"] < 17 or model["p"] >= 53 or model["j"] != 4:
            raise AssertionError("j=4 residual product floor audit had wrong parameters")
        if model["residual_product_fibers"] != model["p"] - 1:
            raise AssertionError("j=4 residual product floor audit was not field-sized")
    j4_pair_product_floor_argument = verify_j4_pair_product_floor_argument()
    rank_one_probe = verify_rank_one_zero_slice_probe()
    t3_same_slope_probe = verify_t3_same_slope_two_exchange_probe()
    t3_variable_new_slope_probe = verify_t3_variable_new_slope_probe()
    line_geometry_models = verify_two_exchange_line_geometry_models()
    print(
        "F13_order12_j4_t2_boundary_model: "
        f"seeds={boundary_product_model['seeds']} "
        f"zero_sum_locators={boundary_product_model['zero_sum_locators']} "
        f"quotient_zero_sum_locators={boundary_product_model['quotient_zero_sum_locators']} "
        f"residual_zero_sum_locators={boundary_product_model['residual_zero_sum_locators']} "
        f"residual_product_fibers={boundary_product_model['residual_product_fibers']} "
        f"residual_product_fiber_size={boundary_product_model['residual_product_fiber_size']}"
    )
    for model in monomial_boundary_models:
        print(
            "full_domain_monomial_boundary_model: "
            f"p={model['p']} j={model['j']} "
            f"j_power_subgroup={model['j_power_subgroup_size']} "
            f"zero_sum_locators={model['zero_sum_locators']} "
            f"zero_sum_product_fibers={model['zero_sum_product_fibers']} "
            f"zero_sum_product_cosets={model['zero_sum_product_cosets']} "
            f"normalized_parameters={model['normalized_parameters']} "
            f"normalized_product_values={model['normalized_product_values']} "
            f"quotient_zero_sum_locators={model['quotient_zero_sum_locators']} "
            f"quotient_scale_checks={model['quotient_scale_checks']} "
            f"quotient_scale_product_fibers={model['quotient_scale_product_fibers']} "
            f"quotient_product_fibers={model['quotient_product_fibers']} "
            f"quotient_product_cosets={model['quotient_product_cosets']} "
            f"quotient_residual_product_overlap={model['quotient_residual_product_overlap']} "
            f"residual_zero_sum_locators={model['residual_zero_sum_locators']} "
            f"residual_product_fibers={model['residual_product_fibers']} "
            f"residual_product_cosets={model['residual_product_cosets']} "
            f"residual_product_fiber_size={model['residual_product_fiber_size']}"
        )
    print(
        "full_domain_monomial_boundary_floor: "
        f"field_sized_cases={monomial_boundary_floor_cases} "
        "p=17 residual_product_fibers=16"
    )
    print(
        "j3_bijective_cube_floor: "
        f"primes={','.join(str(model['p']) for model in j3_bijective_cube_floor_models)} "
        f"field_sized_cases={len(j3_bijective_cube_floor_models)}"
    )
    print(
        "j3_cubic_quotient_floor: "
        f"small_exception_p={j3_cubic_exception['p']} "
        f"exception_residual_products={j3_cubic_exception['residual_product_fibers']} "
        f"field_sized_primes={','.join(str(model['p']) for model in j3_cubic_quotient_floor_models if model['p'] >= 31)}"
    )
    print(
        "j4_residual_product_floor: "
        f"small_primes={','.join(str(model['p']) for model in j4_residual_product_floor_models)} "
        f"field_sized_cases={len(j4_residual_product_floor_models)}"
    )
    print(
        "j4_pair_product_floor_argument: "
        f"prime_count={j4_pair_product_floor_argument['prime_count']} "
        f"min_ordered_pair_reps={j4_pair_product_floor_argument['min_ordered_pair_representations']} "
        f"min_good_reps={j4_pair_product_floor_argument['min_good_representations']} "
        f"max_excluded_reps={j4_pair_product_floor_argument['max_excluded_representations']}"
    )
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
                "one_exchange_pairs={aperiodic_one_exchange_pairs} "
                "strict_degree_max={aperiodic_max_strict_degree} "
                "same_slope_strict={aperiodic_same_slope_strict_pairs} "
                "same_slope_one_exchange={aperiodic_same_slope_one_exchange_pairs} "
                "same_slope_lift_slices={same_slope_one_exchange_root_slices} "
                "same_slope_lift_slopes={same_slope_one_exchange_root_slopes} "
                "same_slope_lift_next_cores={same_slope_one_exchange_next_core_locators} "
                "same_slope_lift_next_slopes={same_slope_one_exchange_next_slopes} "
                "same_slope_lift_member_checks={same_slope_one_exchange_member_checks} "
                "same_slope_lift_noncontained_max={same_slope_one_exchange_noncontained_max} "
                "same_slope_lift_aperiodic_max={same_slope_one_exchange_aperiodic_members_max} "
                "two_exchange_pairs={two_exchange_pairs} "
                "two_exchange_same_slope={two_exchange_same_slope_pairs} "
                "two_exchange_different_slope={two_exchange_different_slope_pairs} "
                "two_exchange_cores={two_exchange_cores} "
                "two_exchange_slices_checked={two_exchange_slices_checked} "
                "two_exchange_minor_checks={two_exchange_minor_polynomial_checks} "
                "two_exchange_bad_locator_checks={two_exchange_bad_locator_checks} "
                "two_exchange_slice_aperiodic_max={two_exchange_max_slice_aperiodic_locators} "
                "two_exchange_slice_slope_max={two_exchange_max_slice_slope_image} "
                "two_exchange_same_slope_clusters={two_exchange_same_slope_clusters} "
                "two_exchange_same_slope_lines={two_exchange_same_slope_line_clusters} "
                "two_exchange_same_slope_fixed_lines={two_exchange_same_slope_fixed_root_lines} "
                "two_exchange_same_slope_mobius_lines={two_exchange_same_slope_mobius_lines} "
                "two_exchange_same_slope_product_mobius_lines={two_exchange_same_slope_product_mobius_lines} "
                "two_exchange_same_slope_sum_mobius_lines={two_exchange_same_slope_sum_mobius_lines} "
                "two_exchange_same_slope_line_two_pairs={two_exchange_same_slope_line_two_exchange_pairs} "
                "two_exchange_same_slope_mobius_two_pairs={two_exchange_same_slope_mobius_two_exchange_pairs} "
                "two_exchange_same_slope_mobius_pair_checks={two_exchange_same_slope_mobius_pair_checks} "
                "two_exchange_same_slope_mobius_member_max={two_exchange_same_slope_mobius_member_max} "
                "two_exchange_same_slope_planes={two_exchange_same_slope_plane_clusters} "
                "two_exchange_same_slope_plane_lifts={two_exchange_same_slope_plane_lifts} "
                "two_exchange_same_slope_plane_two_pairs={two_exchange_same_slope_plane_two_exchange_pairs} "
                "two_exchange_same_slope_affine_member_max={two_exchange_same_slope_affine_member_max} "
                "two_exchange_same_slope_lift_checks={two_exchange_same_slope_lift_checks} "
                "two_exchange_det_lines={two_exchange_det_line_components} "
                "two_exchange_det_line_fixed={two_exchange_det_line_fixed_root} "
                "two_exchange_det_line_product_mobius={two_exchange_det_line_product_mobius} "
                "two_exchange_det_line_sum_mobius={two_exchange_det_line_sum_mobius} "
                "two_exchange_det_line_constant={two_exchange_det_line_constant_slope} "
                "two_exchange_det_line_variable={two_exchange_det_line_variable_slope} "
                "two_exchange_det_line_slope_max={two_exchange_det_line_slope_max} "
                "two_exchange_det_line_aperiodic_max={two_exchange_det_line_aperiodic_max} "
                "two_exchange_det_line_point_checks={two_exchange_det_line_point_checks} "
                "two_exchange_det_full_planes={two_exchange_det_full_planes} "
                "two_exchange_det_full_plane_constant={two_exchange_det_full_plane_constant_slope} "
                "two_exchange_det_full_plane_variable={two_exchange_det_full_plane_variable_slope} "
                "two_exchange_det_full_plane_contained={two_exchange_det_full_plane_contained} "
                "two_exchange_det_full_plane_den_rank_max={two_exchange_det_full_plane_den_rank_max} "
                "two_exchange_det_full_plane_slope_max={two_exchange_det_full_plane_slope_max} "
                "two_exchange_det_full_plane_aperiodic_max={two_exchange_det_full_plane_aperiodic_max} "
                "two_exchange_det_full_plane_lifts={two_exchange_det_full_plane_lifts} "
                "two_exchange_det_proper_lines={two_exchange_det_proper_lines} "
                "two_exchange_det_proper_line_fixed={two_exchange_det_proper_line_fixed_root} "
                "two_exchange_det_proper_line_product_mobius={two_exchange_det_proper_line_product_mobius} "
                "two_exchange_det_proper_line_sum_mobius={two_exchange_det_proper_line_sum_mobius} "
                "two_exchange_det_proper_line_constant={two_exchange_det_proper_line_constant_slope} "
                "two_exchange_det_proper_line_variable={two_exchange_det_proper_line_variable_slope} "
                "two_exchange_det_proper_line_slope_max={two_exchange_det_proper_line_slope_max} "
                "two_exchange_det_proper_line_aperiodic_max={two_exchange_det_proper_line_aperiodic_max} "
                "two_exchange_det_proper_line_core_max={two_exchange_det_proper_line_core_max} "
                "two_exchange_det_proper_line_variable_injective={two_exchange_det_proper_line_variable_injective} "
                "two_exchange_det_proper_line_variable_pole_max={two_exchange_det_proper_line_variable_pole_max} "
                "two_exchange_det_proper_line_variable_aperiodic_slope_max={two_exchange_det_proper_line_variable_aperiodic_slope_max} "
                "two_exchange_det_proper_line_variable_injective_checks={two_exchange_det_proper_line_variable_injective_checks} "
                "two_exchange_det_proper_line_variable_aperiodic_slopes={two_exchange_det_proper_line_variable_aperiodic_slopes} "
                "two_exchange_det_proper_line_variable_new_slopes={two_exchange_det_proper_line_variable_new_slopes} "
                "two_exchange_det_proper_line_variable_new_slope_max={two_exchange_det_proper_line_variable_new_slope_max} "
                "two_exchange_det_proper_line_variable_nonfixed={two_exchange_det_proper_line_variable_nonfixed} "
                "two_exchange_det_proper_line_variable_anchored={two_exchange_det_proper_line_variable_anchored} "
                "two_exchange_det_proper_line_variable_unanchored={two_exchange_det_proper_line_variable_unanchored} "
                "two_exchange_det_proper_line_variable_domain_pair_max={two_exchange_det_proper_line_variable_domain_pair_max} "
                "two_exchange_det_proper_line_variable_domain_pair_checks={two_exchange_det_proper_line_variable_domain_pair_checks} "
                "two_exchange_det_proper_line_variable_charged_slope_checks={two_exchange_det_proper_line_variable_charged_slope_checks} "
                "root_slices={root_slices} "
                "root_slice_slopes={root_slice_slope_count} "
                "root_slice_new_slopes={root_slice_new_slope_count} "
                "root_total_slope_bound={root_slice_total_slope_bound} "
                "root_t3_core_locators={root_slice_t3_core_locators} "
                "root_t3_slopes={root_slice_t3_slope_count} "
                "root_t3_new_slopes={root_slice_t3_new_slope_count} "
                "root_recursive_slope_bound={root_slice_recursive_slope_bound} "
                "root_slice_members={root_slice_members} "
                "root_slice_noncontained_max={max_root_slice_noncontained} "
                "root_slice_aperiodic_max={max_root_slice_aperiodic_members} "
                "root_residual_locators={root_slice_residual_locators} "
                "root_residual_slopes={root_slice_residual_slopes} "
                "root_residual_fiber_max={root_slice_residual_max_slope_fiber} "
                "root_residual_slope_core_checks={root_slice_residual_slope_core_checks} "
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
                "root_residual_top_packet_overlap_pairs={root_slice_residual_top_packet_overlap_pairs} "
                "root_residual_top_packet_overlap_max={root_slice_residual_top_packet_overlap_max} "
                "root_residual_components={root_slice_residual_components} "
                "root_residual_nontrivial_components={root_slice_residual_nontrivial_components} "
                "root_residual_isolated_components={root_slice_residual_isolated_components} "
                "root_residual_boundary_isolated_components={root_slice_residual_boundary_isolated_components} "
                "root_residual_component_max={root_slice_residual_component_max} "
                "root_residual_component_clique_edges={root_slice_residual_component_clique_edges} "
                "root_residual_common_companion_checks={root_slice_residual_common_companion_checks} "
                "root_residual_top_lift_gate_checks={root_slice_residual_top_lift_gate_checks} "
                "root_residual_top_anchor_checks={root_slice_residual_top_anchor_checks} "
                "root_residual_top_common_lift_gate_checks={root_slice_residual_top_common_lift_gate_checks} "
                "root_residual_top_numerator_anchor_checks={root_slice_residual_top_numerator_anchor_checks} "
                "root_residual_top_face_gate_checks={root_slice_residual_top_face_gate_checks} "
                "root_residual_top_face_noncontained={root_slice_residual_top_face_noncontained} "
                "root_residual_top_face_aperiodic={root_slice_residual_top_face_aperiodic} "
                "root_residual_top_face_residual={root_slice_residual_top_face_residual} "
                "root_residual_top_face_peeled={root_slice_residual_top_face_peeled} "
                "root_residual_anchor_lifted_faces={root_slice_residual_anchor_lifted_faces} "
                "root_residual_anchor_escape={root_slice_residual_anchor_escape_locators} "
                "root_residual_anchor_beta0_zero={root_slice_residual_anchor_beta0_zero} "
                "root_residual_anchor_in_support={root_slice_residual_anchor_in_support} "
                "root_residual_anchor_outside_domain={root_slice_residual_anchor_outside_domain} "
                "root_residual_external_anchors={root_slice_residual_external_anchors} "
                "root_residual_external_anchor_locator_max={root_slice_residual_external_anchor_locator_max} "
                "root_residual_external_anchor_slope_max={root_slice_residual_external_anchor_slope_max} "
                "root_residual_external_anchor_slope_fibers={root_slice_residual_external_anchor_slope_fibers} "
                "root_residual_external_anchor_slope_fiber_max={root_slice_residual_external_anchor_slope_fiber_max} "
                "root_residual_external_anchor_slope_core_checks={root_slice_residual_external_anchor_slope_core_checks} "
                "root_residual_external_anchor_kernel_dim_max={root_slice_residual_external_anchor_kernel_dim_max} "
                "root_residual_external_anchor_projective_points={root_slice_residual_external_anchor_projective_points} "
                "root_residual_external_anchor_rich_points={root_slice_residual_external_anchor_rich_points} "
                "root_residual_external_anchor_finite_rich_slopes={root_slice_residual_external_anchor_finite_rich_slopes} "
                "root_residual_external_anchor_rich_residual_classes={root_slice_residual_external_anchor_rich_residual_classes} "
                "root_residual_external_anchor_twist_checks={root_slice_residual_external_anchor_twist_checks} "
                "root_residual_external_anchor_interpolation_checks={root_slice_residual_external_anchor_interpolation_checks} "
                "root_residual_external_anchor_pinned_t1_checks={root_slice_residual_external_anchor_pinned_t1_checks} "
                "root_residual_anchor_lift_checks={root_slice_residual_anchor_lift_gate_checks} "
                "root_residual_anchor_isolated_checks={root_slice_residual_anchor_isolated_checks} "
                "root_residual_anchor_projective_lift_checks={root_slice_residual_anchor_projective_lift_checks} "
                "root_residual_anchor_projective_unique_checks={root_slice_residual_anchor_projective_unique_checks} "
                "root_residual_projective_lift_fibers={root_slice_residual_projective_lift_fibers} "
                "root_residual_projective_squarefree_fibers={root_slice_residual_projective_squarefree_fibers} "
                "root_residual_projective_boundary_fibers={root_slice_residual_projective_boundary_fibers} "
                "root_residual_projective_boundary_singletons={root_slice_residual_projective_boundary_singletons} "
                "root_residual_projective_lift_fiber_max={root_slice_residual_projective_lift_fiber_max} "
                "root_residual_projective_lift_pair_checks={root_slice_residual_projective_lift_pair_checks} "
                "root_residual_anchor_finite_lift_checks={root_slice_residual_anchor_finite_lift_checks} "
                "root_residual_anchor_repeated_lift_checks={root_slice_residual_anchor_repeated_lift_checks} "
                "root_residual_anchor_offdomain_lift_checks={root_slice_residual_anchor_offdomain_lift_checks} "
                "root_residual_anchor_infinity_checks={root_slice_residual_anchor_infinity_checks} "
                "root_residual_lifted_slopes={root_slice_residual_lifted_slopes} "
                "root_residual_escape_slopes={root_slice_residual_escape_slopes} "
                "root_residual_lifted_escape_slope_overlap={root_slice_residual_lifted_escape_slope_overlap} "
                "root_residual_escape_new_slopes={root_slice_residual_escape_new_slopes} "
                "root_residual_lifted_core_slope_bound={root_slice_residual_lifted_core_slope_bound} "
                "root_residual_recursion_bound={root_slice_residual_recursion_bound} "
                "root_residual_new_escape_bound={root_slice_residual_new_escape_bound} "
                "root_residual_active_new_escape_bound={root_slice_residual_active_new_escape_bound} "
                "root_residual_active_face_new_escape_bound={root_slice_residual_active_face_new_escape_bound} "
                "root_residual_boundary_arrangement_bound={root_slice_residual_boundary_arrangement_bound} "
                "root_residual_boundary_slope_bound={root_slice_residual_boundary_slope_bound} "
                "root_residual_boundary_active_anchors={root_slice_residual_boundary_active_anchors} "
                "root_residual_boundary_anchor_slope_bound={root_slice_residual_boundary_anchor_slope_bound} "
                "root_residual_boundary_field_slope_bound={root_slice_residual_boundary_field_slope_bound} "
                "root_residual_active_lifted_core_slope_bound={root_slice_residual_active_lifted_core_slope_bound} "
                "root_recursive_arrangement_bound={root_slice_recursive_arrangement_bound} "
                "root_recursive_boundary_slope_bound={root_slice_recursive_boundary_slope_bound} "
                "root_recursive_boundary_anchor_slope_bound={root_slice_recursive_boundary_anchor_slope_bound} "
                "root_recursive_boundary_field_slope_bound={root_slice_recursive_boundary_field_slope_bound} "
                "root_recursive_active_field_slope_bound={root_slice_recursive_active_field_slope_bound} "
                "root_recursive_new_escape_bound={root_slice_recursive_new_escape_bound} "
                "root_recursive_active_new_escape_bound={root_slice_recursive_active_new_escape_bound} "
                "root_recursive_active_face_new_escape_bound={root_slice_recursive_active_face_new_escape_bound} "
                "root_exact_active_face_bound={root_slice_exact_active_face_bound} "
                "root_recursive_active_face_new_root_bound={root_slice_recursive_active_face_new_root_bound} "
                "root_two_input_field_bound={root_slice_two_input_field_bound} "
                "lifted_u_t1_cores={root_slice_lifted_u_t1_cores} "
                "lifted_v_t1_cores={root_slice_lifted_v_t1_cores} "
                "lifted_common_cores={root_slice_lifted_common_cores} "
                "lifted_common_active_cores={root_slice_lifted_common_active_cores} "
                "lifted_common_inactive_cores={root_slice_lifted_common_inactive_cores} "
                "lifted_common_noncontained_faces={root_slice_lifted_common_core_noncontained_faces} "
                "lifted_common_aperiodic_faces={root_slice_lifted_common_core_aperiodic_faces} "
                "lifted_common_residual_faces={root_slice_lifted_common_core_residual_faces} "
                "lifted_common_peeled_faces={root_slice_lifted_common_core_peeled_faces} "
                "lifted_common_residual_singletons={root_slice_lifted_common_core_residual_singletons} "
                "lifted_common_residual_packets={root_slice_lifted_common_core_residual_packets} "
                "lifted_common_residual_faces_per_core={root_slice_lifted_common_core_max_residual_faces} "
                "lifted_common_base_checks={root_slice_lifted_common_core_common_base_checks} "
                "lifted_common_residual_slope_checks={root_slice_lifted_common_core_residual_slope_checks} "
                "lifted_common_active_ratio_checks={root_slice_lifted_common_core_active_ratio_checks} "
                "lifted_common_residual_slope_pair_checks={root_slice_lifted_common_core_residual_slope_pair_checks} "
                "lifted_common_residual_slope_fiber_max={root_slice_lifted_common_core_residual_slope_fiber_max} "
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
            f"max_one_exchange_pairs={summary['max_aperiodic_one_exchange_pairs']} "
            f"max_strict_degree={summary['max_aperiodic_strict_degree']} "
            f"max_same_slope_one_exchange={summary['max_aperiodic_same_slope_one_exchange_pairs']} "
            f"max_same_slope_lift_slices={summary['max_same_slope_one_exchange_root_slices']} "
            f"max_same_slope_lift_slopes={summary['max_same_slope_one_exchange_root_slopes']} "
            f"max_same_slope_lift_next_cores={summary['max_same_slope_one_exchange_next_core_locators']} "
            f"max_same_slope_lift_next_slopes={summary['max_same_slope_one_exchange_next_slopes']} "
            f"max_same_slope_lift_member_checks={summary['max_same_slope_one_exchange_member_checks']} "
            f"max_same_slope_lift_noncontained={summary['max_same_slope_one_exchange_noncontained']} "
            f"max_same_slope_lift_aperiodic={summary['max_same_slope_one_exchange_aperiodic_members']} "
            f"max_two_exchange_pairs={summary['max_two_exchange_pairs']} "
            f"max_two_exchange_same_slope={summary['max_two_exchange_same_slope_pairs']} "
            f"max_two_exchange_different_slope={summary['max_two_exchange_different_slope_pairs']} "
            f"max_two_exchange_cores={summary['max_two_exchange_cores']} "
            f"max_two_exchange_slices_checked={summary['max_two_exchange_slices_checked']} "
            f"max_two_exchange_minor_checks={summary['max_two_exchange_minor_polynomial_checks']} "
            f"max_two_exchange_bad_locator_checks={summary['max_two_exchange_bad_locator_checks']} "
            f"max_two_exchange_slice_aperiodic={summary['max_two_exchange_slice_aperiodic_locators']} "
            f"max_two_exchange_slice_slope={summary['max_two_exchange_slice_slope_image']} "
            f"max_two_exchange_same_slope_clusters={summary['max_two_exchange_same_slope_clusters']} "
            f"max_two_exchange_same_slope_lines={summary['max_two_exchange_same_slope_line_clusters']} "
            f"max_two_exchange_same_slope_fixed_lines={summary['max_two_exchange_same_slope_fixed_root_lines']} "
            f"max_two_exchange_same_slope_mobius_lines={summary['max_two_exchange_same_slope_mobius_lines']} "
            f"max_two_exchange_same_slope_product_mobius_lines={summary['max_two_exchange_same_slope_product_mobius_lines']} "
            f"max_two_exchange_same_slope_sum_mobius_lines={summary['max_two_exchange_same_slope_sum_mobius_lines']} "
            f"max_two_exchange_same_slope_line_two_pairs={summary['max_two_exchange_same_slope_line_two_exchange_pairs']} "
            f"max_two_exchange_same_slope_mobius_two_pairs={summary['max_two_exchange_same_slope_mobius_two_exchange_pairs']} "
            f"max_two_exchange_same_slope_mobius_pair_checks={summary['max_two_exchange_same_slope_mobius_pair_checks']} "
            f"max_two_exchange_same_slope_mobius_member={summary['max_two_exchange_same_slope_mobius_member']} "
            f"max_two_exchange_same_slope_planes={summary['max_two_exchange_same_slope_plane_clusters']} "
            f"max_two_exchange_same_slope_plane_lifts={summary['max_two_exchange_same_slope_plane_lifts']} "
            f"max_two_exchange_same_slope_plane_two_pairs={summary['max_two_exchange_same_slope_plane_two_exchange_pairs']} "
            f"max_two_exchange_same_slope_affine_member={summary['max_two_exchange_same_slope_affine_member']} "
            f"max_two_exchange_same_slope_lift_checks={summary['max_two_exchange_same_slope_lift_checks']} "
            f"max_two_exchange_det_lines={summary['max_two_exchange_det_line_components']} "
            f"max_two_exchange_det_line_fixed={summary['max_two_exchange_det_line_fixed_root']} "
            f"max_two_exchange_det_line_product_mobius={summary['max_two_exchange_det_line_product_mobius']} "
            f"max_two_exchange_det_line_sum_mobius={summary['max_two_exchange_det_line_sum_mobius']} "
            f"max_two_exchange_det_line_constant={summary['max_two_exchange_det_line_constant_slope']} "
            f"max_two_exchange_det_line_variable={summary['max_two_exchange_det_line_variable_slope']} "
            f"max_two_exchange_det_line_slope={summary['max_two_exchange_det_line_slope']} "
            f"max_two_exchange_det_line_aperiodic={summary['max_two_exchange_det_line_aperiodic']} "
            f"max_two_exchange_det_line_point_checks={summary['max_two_exchange_det_line_point_checks']} "
            f"max_two_exchange_det_full_planes={summary['max_two_exchange_det_full_planes']} "
            f"max_two_exchange_det_full_plane_constant={summary['max_two_exchange_det_full_plane_constant_slope']} "
            f"max_two_exchange_det_full_plane_variable={summary['max_two_exchange_det_full_plane_variable_slope']} "
            f"max_two_exchange_det_full_plane_contained={summary['max_two_exchange_det_full_plane_contained']} "
            f"max_two_exchange_det_full_plane_den_rank={summary['max_two_exchange_det_full_plane_den_rank']} "
            f"max_two_exchange_det_full_plane_slope={summary['max_two_exchange_det_full_plane_slope']} "
            f"max_two_exchange_det_full_plane_aperiodic={summary['max_two_exchange_det_full_plane_aperiodic']} "
            f"max_two_exchange_det_full_plane_lifts={summary['max_two_exchange_det_full_plane_lifts']} "
            f"max_two_exchange_det_proper_lines={summary['max_two_exchange_det_proper_lines']} "
            f"max_two_exchange_det_proper_line_fixed={summary['max_two_exchange_det_proper_line_fixed_root']} "
            f"max_two_exchange_det_proper_line_product_mobius={summary['max_two_exchange_det_proper_line_product_mobius']} "
            f"max_two_exchange_det_proper_line_sum_mobius={summary['max_two_exchange_det_proper_line_sum_mobius']} "
            f"max_two_exchange_det_proper_line_constant={summary['max_two_exchange_det_proper_line_constant_slope']} "
            f"max_two_exchange_det_proper_line_variable={summary['max_two_exchange_det_proper_line_variable_slope']} "
            f"max_two_exchange_det_proper_line_slope={summary['max_two_exchange_det_proper_line_slope']} "
            f"max_two_exchange_det_proper_line_aperiodic={summary['max_two_exchange_det_proper_line_aperiodic']} "
            f"max_two_exchange_det_proper_line_core={summary['max_two_exchange_det_proper_line_core']} "
            f"max_two_exchange_det_proper_line_variable_injective={summary['max_two_exchange_det_proper_line_variable_injective']} "
            f"max_two_exchange_det_proper_line_variable_pole={summary['max_two_exchange_det_proper_line_variable_pole']} "
            f"max_two_exchange_det_proper_line_variable_aperiodic_slope={summary['max_two_exchange_det_proper_line_variable_aperiodic_slope']} "
            f"max_two_exchange_det_proper_line_variable_injective_checks={summary['max_two_exchange_det_proper_line_variable_injective_checks']} "
            f"max_two_exchange_det_proper_line_variable_aperiodic_slopes={summary['max_two_exchange_det_proper_line_variable_aperiodic_slopes']} "
            f"max_two_exchange_det_proper_line_variable_new_slopes={summary['max_two_exchange_det_proper_line_variable_new_slopes']} "
            f"max_two_exchange_det_proper_line_variable_charged_slope_checks={summary['max_two_exchange_det_proper_line_variable_charged_slope_checks']} "
            f"max_root_slices={summary['max_root_slices']} "
            f"max_root_slice_noncontained={summary['max_root_slice_noncontained']} "
            f"max_root_total_slope_bound={summary['max_root_slice_total_slope_bound']} "
            f"max_root_new_slopes={summary['max_root_slice_new_slope_count']} "
            f"max_root_t3_core_locators={summary['max_root_slice_t3_core_locators']} "
            f"max_root_t3_slopes={summary['max_root_slice_t3_slope_count']} "
            f"max_root_t3_new_slopes={summary['max_root_slice_t3_new_slope_count']} "
            f"max_root_recursive_slope_bound={summary['max_root_slice_recursive_slope_bound']} "
            f"max_root_slice_members={summary['max_root_slice_members']} "
            f"max_root_residual_locators={summary['max_root_slice_residual_locators']} "
            f"max_root_residual_slopes={summary['max_root_slice_residual_slopes']} "
            f"max_root_residual_fiber={summary['max_root_slice_residual_slope_fiber']} "
            f"max_root_residual_slope_core_checks={summary['max_root_slice_residual_slope_core_checks']} "
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
            f"max_root_residual_top_packet_overlap_pairs={summary['max_root_slice_residual_top_packet_overlap_pairs']} "
            f"max_root_residual_top_packet_overlap={summary['max_root_slice_residual_top_packet_overlap']} "
            f"max_root_residual_components={summary['max_root_slice_residual_components']} "
            f"max_root_residual_nontrivial_components={summary['max_root_slice_residual_nontrivial_components']} "
            f"max_root_residual_isolated_components={summary['max_root_slice_residual_isolated_components']} "
            f"max_root_residual_boundary_isolated_components={summary['max_root_slice_residual_boundary_isolated_components']} "
            f"max_root_residual_component_size={summary['max_root_slice_residual_component_size']} "
            f"max_root_residual_component_clique_edges={summary['max_root_slice_residual_component_clique_edges']} "
            f"max_root_residual_common_companion_checks={summary['max_root_slice_residual_common_companion_checks']} "
            f"max_root_residual_top_lift_gate_checks={summary['max_root_slice_residual_top_lift_gate_checks']} "
            f"max_root_residual_top_anchor_checks={summary['max_root_slice_residual_top_anchor_checks']} "
            f"max_root_residual_top_common_lift_gate_checks={summary['max_root_slice_residual_top_common_lift_gate_checks']} "
            f"max_root_residual_top_numerator_anchor_checks={summary['max_root_slice_residual_top_numerator_anchor_checks']} "
            f"max_root_residual_top_face_gate_checks={summary['max_root_slice_residual_top_face_gate_checks']} "
            f"max_root_residual_top_face_noncontained={summary['max_root_slice_residual_top_face_noncontained']} "
            f"max_root_residual_top_face_aperiodic={summary['max_root_slice_residual_top_face_aperiodic']} "
            f"max_root_residual_top_face_residual={summary['max_root_slice_residual_top_face_residual']} "
            f"max_root_residual_top_face_peeled={summary['max_root_slice_residual_top_face_peeled']} "
            f"max_root_residual_anchor_lifted_faces={summary['max_root_slice_residual_anchor_lifted_faces']} "
            f"max_root_residual_anchor_escape={summary['max_root_slice_residual_anchor_escape_locators']} "
            f"max_root_residual_anchor_beta0_zero={summary['max_root_slice_residual_anchor_beta0_zero']} "
            f"max_root_residual_anchor_in_support={summary['max_root_slice_residual_anchor_in_support']} "
            f"max_root_residual_anchor_outside_domain={summary['max_root_slice_residual_anchor_outside_domain']} "
            f"max_root_residual_external_anchors={summary['max_root_slice_residual_external_anchors']} "
            f"max_root_residual_external_anchor_locator={summary['max_root_slice_residual_external_anchor_locator']} "
            f"max_root_residual_external_anchor_slope={summary['max_root_slice_residual_external_anchor_slope']} "
            f"max_root_residual_external_anchor_slope_fibers={summary['max_root_slice_residual_external_anchor_slope_fibers']} "
            f"max_root_residual_external_anchor_slope_fiber={summary['max_root_slice_residual_external_anchor_slope_fiber']} "
            f"max_root_residual_external_anchor_slope_core_checks={summary['max_root_slice_residual_external_anchor_slope_core_checks']} "
            f"max_root_residual_external_anchor_kernel_dim={summary['max_root_slice_residual_external_anchor_kernel_dim']} "
            f"max_root_residual_external_anchor_projective_points={summary['max_root_slice_residual_external_anchor_projective_points']} "
            f"max_root_residual_external_anchor_rich_points={summary['max_root_slice_residual_external_anchor_rich_points']} "
            f"max_root_residual_external_anchor_finite_rich_slopes={summary['max_root_slice_residual_external_anchor_finite_rich_slopes']} "
            f"max_root_residual_external_anchor_rich_residual_classes={summary['max_root_slice_residual_external_anchor_rich_residual_classes']} "
            f"max_root_residual_external_anchor_twist_checks={summary['max_root_slice_residual_external_anchor_twist_checks']} "
            f"max_root_residual_external_anchor_interpolation_checks={summary['max_root_slice_residual_external_anchor_interpolation_checks']} "
            f"max_root_residual_external_anchor_pinned_t1_checks={summary['max_root_slice_residual_external_anchor_pinned_t1_checks']} "
            f"max_root_residual_anchor_lift_checks={summary['max_root_slice_residual_anchor_lift_gate_checks']} "
            f"max_root_residual_anchor_isolated_checks={summary['max_root_slice_residual_anchor_isolated_checks']} "
            f"max_root_residual_anchor_projective_lift_checks={summary['max_root_slice_residual_anchor_projective_lift_checks']} "
            f"max_root_residual_anchor_projective_unique_checks={summary['max_root_slice_residual_anchor_projective_unique_checks']} "
            f"max_root_residual_projective_lift_fibers={summary['max_root_slice_residual_projective_lift_fibers']} "
            f"max_root_residual_projective_squarefree_fibers={summary['max_root_slice_residual_projective_squarefree_fibers']} "
            f"max_root_residual_projective_boundary_fibers={summary['max_root_slice_residual_projective_boundary_fibers']} "
            f"max_root_residual_projective_boundary_singletons={summary['max_root_slice_residual_projective_boundary_singletons']} "
            f"max_root_residual_projective_lift_fiber={summary['max_root_slice_residual_projective_lift_fiber']} "
            f"max_root_residual_projective_lift_pair_checks={summary['max_root_slice_residual_projective_lift_pair_checks']} "
            f"max_root_residual_anchor_finite_lift_checks={summary['max_root_slice_residual_anchor_finite_lift_checks']} "
            f"max_root_residual_anchor_repeated_lift_checks={summary['max_root_slice_residual_anchor_repeated_lift_checks']} "
            f"max_root_residual_anchor_offdomain_lift_checks={summary['max_root_slice_residual_anchor_offdomain_lift_checks']} "
            f"max_root_residual_anchor_infinity_checks={summary['max_root_slice_residual_anchor_infinity_checks']} "
            f"max_root_residual_lifted_slopes={summary['max_root_slice_residual_lifted_slopes']} "
            f"max_root_residual_escape_slopes={summary['max_root_slice_residual_escape_slopes']} "
            f"max_root_residual_lifted_escape_slope_overlap={summary['max_root_slice_residual_lifted_escape_slope_overlap']} "
            f"max_root_residual_escape_new_slopes={summary['max_root_slice_residual_escape_new_slopes']} "
            f"max_root_residual_lifted_core_slope_bound={summary['max_root_slice_residual_lifted_core_slope_bound']} "
            f"max_root_residual_recursion_bound={summary['max_root_slice_residual_recursion_bound']} "
            f"max_root_residual_new_escape_bound={summary['max_root_slice_residual_new_escape_bound']} "
            f"max_root_residual_active_new_escape_bound={summary['max_root_slice_residual_active_new_escape_bound']} "
            f"max_root_residual_active_face_new_escape_bound={summary['max_root_slice_residual_active_face_new_escape_bound']} "
            f"max_root_residual_boundary_arrangement_bound={summary['max_root_slice_residual_boundary_arrangement_bound']} "
            f"max_root_residual_boundary_slope_bound={summary['max_root_slice_residual_boundary_slope_bound']} "
            f"max_root_residual_boundary_active_anchors={summary['max_root_slice_residual_boundary_active_anchors']} "
            f"max_root_residual_boundary_anchor_slope_bound={summary['max_root_slice_residual_boundary_anchor_slope_bound']} "
            f"max_root_residual_boundary_field_slope_bound={summary['max_root_slice_residual_boundary_field_slope_bound']} "
            f"max_root_residual_active_lifted_core_slope_bound={summary['max_root_slice_residual_active_lifted_core_slope_bound']} "
            f"max_root_recursive_arrangement_bound={summary['max_root_slice_recursive_arrangement_bound']} "
            f"max_root_recursive_boundary_slope_bound={summary['max_root_slice_recursive_boundary_slope_bound']} "
            f"max_root_recursive_boundary_anchor_slope_bound={summary['max_root_slice_recursive_boundary_anchor_slope_bound']} "
            f"max_root_recursive_boundary_field_slope_bound={summary['max_root_slice_recursive_boundary_field_slope_bound']} "
            f"max_root_recursive_active_field_slope_bound={summary['max_root_slice_recursive_active_field_slope_bound']} "
            f"max_root_recursive_new_escape_bound={summary['max_root_slice_recursive_new_escape_bound']} "
            f"max_root_recursive_active_new_escape_bound={summary['max_root_slice_recursive_active_new_escape_bound']} "
            f"max_root_recursive_active_face_new_escape_bound={summary['max_root_slice_recursive_active_face_new_escape_bound']} "
            f"max_root_exact_active_face_bound={summary['max_root_slice_exact_active_face_bound']} "
            f"max_root_recursive_active_face_new_root_bound={summary['max_root_slice_recursive_active_face_new_root_bound']} "
            f"max_root_two_input_field_bound={summary['max_root_slice_two_input_field_bound']} "
            f"max_lifted_u_t1_cores={summary['max_root_slice_lifted_u_t1_cores']} "
            f"max_lifted_v_t1_cores={summary['max_root_slice_lifted_v_t1_cores']} "
            f"max_lifted_common_cores={summary['max_root_slice_lifted_common_cores']} "
            f"max_lifted_common_active_cores={summary['max_root_slice_lifted_common_active_cores']} "
            f"max_lifted_common_inactive_cores={summary['max_root_slice_lifted_common_inactive_cores']} "
            f"max_lifted_common_noncontained_faces={summary['max_root_slice_lifted_common_core_noncontained_faces']} "
            f"max_lifted_common_aperiodic_faces={summary['max_root_slice_lifted_common_core_aperiodic_faces']} "
            f"max_lifted_common_residual_faces={summary['max_root_slice_lifted_common_core_residual_faces']} "
            f"max_lifted_common_peeled_faces={summary['max_root_slice_lifted_common_core_peeled_faces']} "
            f"max_lifted_common_residual_singletons={summary['max_root_slice_lifted_common_core_residual_singletons']} "
            f"max_lifted_common_residual_packets={summary['max_root_slice_lifted_common_core_residual_packets']} "
            f"max_lifted_common_residual_faces_per_core={summary['max_root_slice_lifted_common_core_residual_faces_per_core']} "
            f"max_lifted_common_base_checks={summary['max_root_slice_lifted_common_core_common_base_checks']} "
            f"max_lifted_common_residual_slope_checks={summary['max_root_slice_lifted_common_core_residual_slope_checks']} "
            f"max_lifted_common_active_ratio_checks={summary['max_root_slice_lifted_common_core_active_ratio_checks']} "
            f"max_lifted_common_residual_slope_pair_checks={summary['max_root_slice_lifted_common_core_residual_slope_pair_checks']} "
            f"max_lifted_common_residual_slope_fiber={summary['max_root_slice_lifted_common_core_residual_slope_fiber']} "
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
        "one_exchange_pairs={aperiodic_one_exchange_pairs} "
        "same_slope_one_exchange={aperiodic_same_slope_one_exchange_pairs} "
        "same_slope_lift_slices={same_slope_one_exchange_root_slices} "
        "same_slope_lift_slopes={same_slope_one_exchange_root_slopes} "
        "same_slope_lift_next_cores={same_slope_one_exchange_next_core_locators} "
        "same_slope_lift_next_slopes={same_slope_one_exchange_next_slopes} "
        "same_slope_lift_member_checks={same_slope_one_exchange_member_checks} "
        "two_exchange_pairs={two_exchange_pairs} "
        "two_exchange_same_slope={two_exchange_same_slope_pairs} "
        "two_exchange_different_slope={two_exchange_different_slope_pairs} "
        "two_exchange_minor_checks={two_exchange_minor_polynomial_checks} "
        "root_slice_slopes={root_slice_slope_count} "
        "root_slice_new_slopes={root_slice_new_slope_count} "
        "root_t3_slopes={root_slice_t3_slope_count} "
        "root_t3_new_slopes={root_slice_t3_new_slope_count} "
        "zero_det_slices={zero_determinant_slices} "
        "zero_det_rank1={zero_det_direction_rank1_slices} "
        "zero_det_constant={zero_det_constant_slices} "
        "zero_det_injective={zero_det_injective_slices} "
        "root_residual_locators={root_slice_residual_locators} "
        "root_residual_slope_core_checks={root_slice_residual_slope_core_checks} "
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
        "root_residual_top_packet_overlap_pairs={root_slice_residual_top_packet_overlap_pairs} "
        "root_residual_top_packet_overlap_max={root_slice_residual_top_packet_overlap_max} "
        "root_residual_components={root_slice_residual_components} "
        "root_residual_nontrivial_components={root_slice_residual_nontrivial_components} "
        "root_residual_isolated_components={root_slice_residual_isolated_components} "
        "root_residual_boundary_isolated_components={root_slice_residual_boundary_isolated_components} "
        "root_residual_component_max={root_slice_residual_component_max} "
        "root_residual_component_clique_edges={root_slice_residual_component_clique_edges} "
        "root_residual_common_companion_checks={root_slice_residual_common_companion_checks} "
        "root_residual_top_lift_gate_checks={root_slice_residual_top_lift_gate_checks} "
        "root_residual_top_anchor_checks={root_slice_residual_top_anchor_checks} "
        "root_residual_top_common_lift_gate_checks={root_slice_residual_top_common_lift_gate_checks} "
        "root_residual_top_numerator_anchor_checks={root_slice_residual_top_numerator_anchor_checks} "
        "root_residual_top_face_gate_checks={root_slice_residual_top_face_gate_checks} "
        "root_residual_top_face_noncontained={root_slice_residual_top_face_noncontained} "
        "root_residual_top_face_aperiodic={root_slice_residual_top_face_aperiodic} "
        "root_residual_top_face_residual={root_slice_residual_top_face_residual} "
        "root_residual_top_face_peeled={root_slice_residual_top_face_peeled} "
        "root_residual_anchor_lifted_faces={root_slice_residual_anchor_lifted_faces} "
        "root_residual_anchor_escape={root_slice_residual_anchor_escape_locators} "
        "root_residual_anchor_beta0_zero={root_slice_residual_anchor_beta0_zero} "
        "root_residual_anchor_in_support={root_slice_residual_anchor_in_support} "
        "root_residual_anchor_outside_domain={root_slice_residual_anchor_outside_domain} "
        "root_residual_external_anchors={root_slice_residual_external_anchors} "
        "root_residual_external_anchor_locator_max={root_slice_residual_external_anchor_locator_max} "
        "root_residual_external_anchor_slope_max={root_slice_residual_external_anchor_slope_max} "
        "root_residual_external_anchor_slope_fibers={root_slice_residual_external_anchor_slope_fibers} "
        "root_residual_external_anchor_slope_fiber_max={root_slice_residual_external_anchor_slope_fiber_max} "
        "root_residual_external_anchor_slope_core_checks={root_slice_residual_external_anchor_slope_core_checks} "
        "root_residual_external_anchor_kernel_dim_max={root_slice_residual_external_anchor_kernel_dim_max} "
        "root_residual_external_anchor_projective_points={root_slice_residual_external_anchor_projective_points} "
        "root_residual_external_anchor_rich_points={root_slice_residual_external_anchor_rich_points} "
        "root_residual_external_anchor_finite_rich_slopes={root_slice_residual_external_anchor_finite_rich_slopes} "
        "root_residual_external_anchor_rich_residual_classes={root_slice_residual_external_anchor_rich_residual_classes} "
        "root_residual_external_anchor_twist_checks={root_slice_residual_external_anchor_twist_checks} "
        "root_residual_external_anchor_interpolation_checks={root_slice_residual_external_anchor_interpolation_checks} "
        "root_residual_external_anchor_pinned_t1_checks={root_slice_residual_external_anchor_pinned_t1_checks} "
        "root_residual_anchor_lift_checks={root_slice_residual_anchor_lift_gate_checks} "
        "root_residual_anchor_isolated_checks={root_slice_residual_anchor_isolated_checks} "
        "root_residual_anchor_projective_lift_checks={root_slice_residual_anchor_projective_lift_checks} "
        "root_residual_anchor_projective_unique_checks={root_slice_residual_anchor_projective_unique_checks} "
        "root_residual_projective_lift_fibers={root_slice_residual_projective_lift_fibers} "
        "root_residual_projective_squarefree_fibers={root_slice_residual_projective_squarefree_fibers} "
        "root_residual_projective_boundary_fibers={root_slice_residual_projective_boundary_fibers} "
        "root_residual_projective_boundary_singletons={root_slice_residual_projective_boundary_singletons} "
        "root_residual_projective_lift_fiber_max={root_slice_residual_projective_lift_fiber_max} "
        "root_residual_projective_lift_pair_checks={root_slice_residual_projective_lift_pair_checks} "
        "root_residual_anchor_finite_lift_checks={root_slice_residual_anchor_finite_lift_checks} "
        "root_residual_anchor_repeated_lift_checks={root_slice_residual_anchor_repeated_lift_checks} "
        "root_residual_anchor_offdomain_lift_checks={root_slice_residual_anchor_offdomain_lift_checks} "
        "root_residual_anchor_infinity_checks={root_slice_residual_anchor_infinity_checks} "
        "root_residual_lifted_slopes={root_slice_residual_lifted_slopes} "
        "root_residual_escape_slopes={root_slice_residual_escape_slopes} "
        "root_residual_lifted_escape_slope_overlap={root_slice_residual_lifted_escape_slope_overlap} "
        "root_residual_escape_new_slopes={root_slice_residual_escape_new_slopes} "
        "root_residual_lifted_core_slope_bound={root_slice_residual_lifted_core_slope_bound} "
        "root_residual_recursion_bound={root_slice_residual_recursion_bound} "
        "root_residual_new_escape_bound={root_slice_residual_new_escape_bound} "
        "root_residual_active_new_escape_bound={root_slice_residual_active_new_escape_bound} "
        "root_residual_active_face_new_escape_bound={root_slice_residual_active_face_new_escape_bound} "
        "root_residual_boundary_arrangement_bound={root_slice_residual_boundary_arrangement_bound} "
        "root_residual_boundary_slope_bound={root_slice_residual_boundary_slope_bound} "
        "root_residual_boundary_active_anchors={root_slice_residual_boundary_active_anchors} "
        "root_residual_boundary_anchor_slope_bound={root_slice_residual_boundary_anchor_slope_bound} "
        "root_residual_boundary_field_slope_bound={root_slice_residual_boundary_field_slope_bound} "
        "root_residual_active_lifted_core_slope_bound={root_slice_residual_active_lifted_core_slope_bound} "
        "root_recursive_arrangement_bound={root_slice_recursive_arrangement_bound} "
        "root_recursive_boundary_slope_bound={root_slice_recursive_boundary_slope_bound} "
        "root_recursive_boundary_anchor_slope_bound={root_slice_recursive_boundary_anchor_slope_bound} "
        "root_recursive_boundary_field_slope_bound={root_slice_recursive_boundary_field_slope_bound} "
        "root_recursive_active_field_slope_bound={root_slice_recursive_active_field_slope_bound} "
        "root_recursive_new_escape_bound={root_slice_recursive_new_escape_bound} "
        "root_recursive_active_new_escape_bound={root_slice_recursive_active_new_escape_bound} "
        "root_recursive_active_face_new_escape_bound={root_slice_recursive_active_face_new_escape_bound} "
        "root_exact_active_face_bound={root_slice_exact_active_face_bound} "
        "root_recursive_active_face_new_root_bound={root_slice_recursive_active_face_new_root_bound} "
        "root_two_input_field_bound={root_slice_two_input_field_bound} "
        "lifted_u_t1_cores={root_slice_lifted_u_t1_cores} "
        "lifted_v_t1_cores={root_slice_lifted_v_t1_cores} "
        "lifted_common_cores={root_slice_lifted_common_cores} "
        "lifted_common_active_cores={root_slice_lifted_common_active_cores} "
        "lifted_common_inactive_cores={root_slice_lifted_common_inactive_cores} "
        "lifted_common_noncontained_faces={root_slice_lifted_common_core_noncontained_faces} "
        "lifted_common_aperiodic_faces={root_slice_lifted_common_core_aperiodic_faces} "
        "lifted_common_residual_faces={root_slice_lifted_common_core_residual_faces} "
        "lifted_common_peeled_faces={root_slice_lifted_common_core_peeled_faces} "
        "lifted_common_residual_singletons={root_slice_lifted_common_core_residual_singletons} "
        "lifted_common_residual_packets={root_slice_lifted_common_core_residual_packets} "
        "lifted_common_residual_faces_per_core={root_slice_lifted_common_core_max_residual_faces} "
        "lifted_common_base_checks={root_slice_lifted_common_core_common_base_checks} "
        "lifted_common_residual_slope_checks={root_slice_lifted_common_core_residual_slope_checks} "
        "lifted_common_active_ratio_checks={root_slice_lifted_common_core_active_ratio_checks} "
        "lifted_common_residual_slope_pair_checks={root_slice_lifted_common_core_residual_slope_pair_checks} "
        "lifted_common_residual_slope_fiber_max={root_slice_lifted_common_core_residual_slope_fiber_max} "
        "quad_companion_checks={quadratic_companion_checks} "
        "direct_checks={direct_checks}".format(**rank_one_probe)
    )
    print(
        "{name} seed={seed}: p={p} n={n} k={k} j={j} t={t} "
        "aperiodic_locators={aperiodic_locators} aperiodic_slopes={aperiodic_slopes} "
        "strict_pairs={aperiodic_strict_pairs} one_exchange_pairs={aperiodic_one_exchange_pairs} "
        "same_slope_strict={aperiodic_same_slope_strict_pairs} "
        "same_slope_one_exchange={aperiodic_same_slope_one_exchange_pairs} "
        "two_exchange_pairs={two_exchange_pairs} "
        "two_exchange_same_slope={two_exchange_same_slope_pairs} "
        "two_exchange_different_slope={two_exchange_different_slope_pairs} "
        "two_exchange_same_slope_lines={two_exchange_same_slope_line_clusters} "
        "two_exchange_same_slope_fixed_lines={two_exchange_same_slope_fixed_root_lines} "
        "two_exchange_same_slope_mobius_lines={two_exchange_same_slope_mobius_lines} "
        "two_exchange_same_slope_product_mobius_lines={two_exchange_same_slope_product_mobius_lines} "
        "two_exchange_same_slope_sum_mobius_lines={two_exchange_same_slope_sum_mobius_lines} "
        "two_exchange_same_slope_line_two_pairs={two_exchange_same_slope_line_two_exchange_pairs} "
        "two_exchange_same_slope_mobius_two_pairs={two_exchange_same_slope_mobius_two_exchange_pairs} "
        "two_exchange_same_slope_mobius_pair_checks={two_exchange_same_slope_mobius_pair_checks} "
        "two_exchange_same_slope_planes={two_exchange_same_slope_plane_clusters} "
        "two_exchange_same_slope_plane_lifts={two_exchange_same_slope_plane_lifts} "
        "two_exchange_same_slope_plane_two_pairs={two_exchange_same_slope_plane_two_exchange_pairs} "
        "two_exchange_same_slope_affine_member_max={two_exchange_same_slope_affine_member_max} "
        "two_exchange_same_slope_lift_checks={two_exchange_same_slope_lift_checks} "
        "two_exchange_det_lines={two_exchange_det_line_components} "
        "two_exchange_det_line_fixed={two_exchange_det_line_fixed_root} "
        "two_exchange_det_line_variable={two_exchange_det_line_variable_slope} "
        "two_exchange_det_line_slope_max={two_exchange_det_line_slope_max} "
        "two_exchange_det_full_planes={two_exchange_det_full_planes} "
        "two_exchange_det_full_plane_lifts={two_exchange_det_full_plane_lifts} "
        "two_exchange_det_proper_lines={two_exchange_det_proper_lines} "
        "two_exchange_det_proper_line_variable={two_exchange_det_proper_line_variable_slope} "
        "two_exchange_det_proper_line_slope_max={two_exchange_det_proper_line_slope_max} "
        "two_exchange_det_proper_line_core_max={two_exchange_det_proper_line_core_max} "
        "two_exchange_det_proper_line_variable_injective={two_exchange_det_proper_line_variable_injective} "
        "two_exchange_det_proper_line_variable_pole_max={two_exchange_det_proper_line_variable_pole_max} "
        "two_exchange_det_proper_line_variable_aperiodic_slope_max={two_exchange_det_proper_line_variable_aperiodic_slope_max} "
        "two_exchange_det_proper_line_variable_injective_checks={two_exchange_det_proper_line_variable_injective_checks} "
        "two_exchange_det_proper_line_variable_aperiodic_slopes={two_exchange_det_proper_line_variable_aperiodic_slopes} "
        "two_exchange_det_proper_line_variable_new_slopes={two_exchange_det_proper_line_variable_new_slopes} "
        "two_exchange_det_proper_line_variable_new_slope_max={two_exchange_det_proper_line_variable_new_slope_max} "
        "two_exchange_det_proper_line_variable_nonfixed={two_exchange_det_proper_line_variable_nonfixed} "
        "two_exchange_det_proper_line_variable_anchored={two_exchange_det_proper_line_variable_anchored} "
        "two_exchange_det_proper_line_variable_unanchored={two_exchange_det_proper_line_variable_unanchored} "
        "two_exchange_det_proper_line_variable_domain_pair_max={two_exchange_det_proper_line_variable_domain_pair_max} "
        "two_exchange_det_proper_line_variable_domain_pair_checks={two_exchange_det_proper_line_variable_domain_pair_checks} "
        "two_exchange_det_proper_line_variable_charged_slope_checks={two_exchange_det_proper_line_variable_charged_slope_checks} "
        "two_exchange_minor_checks={two_exchange_minor_polynomial_checks} "
        "direct_checks={direct_checks}".format(**t3_same_slope_probe)
    )
    print(
        "{name} seed={seed}: p={p} n={n} k={k} j={j} t={t} "
        "aperiodic_locators={aperiodic_locators} "
        "aperiodic_slopes={aperiodic_slopes} "
        "two_exchange_det_full_planes={two_exchange_det_full_planes} "
        "two_exchange_det_full_plane_lifts={two_exchange_det_full_plane_lifts} "
        "two_exchange_det_proper_lines={two_exchange_det_proper_lines} "
        "two_exchange_det_proper_line_product_mobius={two_exchange_det_proper_line_product_mobius} "
        "two_exchange_det_proper_line_variable={two_exchange_det_proper_line_variable_slope} "
        "two_exchange_det_proper_line_variable_aperiodic_slopes={two_exchange_det_proper_line_variable_aperiodic_slopes} "
        "two_exchange_det_proper_line_variable_new_slopes={two_exchange_det_proper_line_variable_new_slopes} "
        "two_exchange_det_proper_line_variable_new_slope_max={two_exchange_det_proper_line_variable_new_slope_max} "
        "two_exchange_det_proper_line_variable_nonfixed={two_exchange_det_proper_line_variable_nonfixed} "
        "two_exchange_det_proper_line_variable_anchored={two_exchange_det_proper_line_variable_anchored} "
        "two_exchange_det_proper_line_variable_unanchored={two_exchange_det_proper_line_variable_unanchored} "
        "two_exchange_det_proper_line_variable_domain_pair_max={two_exchange_det_proper_line_variable_domain_pair_max} "
        "two_exchange_det_proper_line_variable_domain_pair_checks={two_exchange_det_proper_line_variable_domain_pair_checks} "
        "direct_checks={direct_checks}".format(**t3_variable_new_slope_probe)
    )
    print(
        "two_exchange_line_geometry_models: "
        f"field={line_geometry_models['field']} "
        f"fixed_root_checks={line_geometry_models['fixed_root_checks']} "
        f"product_mobius_checks={line_geometry_models['product_mobius_checks']} "
        f"sum_mobius_checks={line_geometry_models['sum_mobius_checks']}"
    )
    all_rows = [row for summary in summaries for row in summary["rows"]] + [
        rank_one_probe,
        t3_same_slope_probe,
        t3_variable_new_slope_probe,
    ]
    max_aperiodic = max(row["aperiodic_slopes"] for row in all_rows)
    max_strict_degree = max(row["aperiodic_max_strict_degree"] for row in all_rows)
    max_one_exchange_pairs = max(row["aperiodic_one_exchange_pairs"] for row in all_rows)
    max_same_slope_one_exchange_pairs = max(
        row["aperiodic_same_slope_one_exchange_pairs"] for row in all_rows
    )
    max_same_slope_lift_slices = max(
        row["same_slope_one_exchange_root_slices"] for row in all_rows
    )
    max_same_slope_lift_slopes = max(
        row["same_slope_one_exchange_root_slopes"] for row in all_rows
    )
    max_same_slope_lift_next_cores = max(
        row["same_slope_one_exchange_next_core_locators"] for row in all_rows
    )
    max_same_slope_lift_next_slopes = max(
        row["same_slope_one_exchange_next_slopes"] for row in all_rows
    )
    max_same_slope_lift_member_checks = max(
        row["same_slope_one_exchange_member_checks"] for row in all_rows
    )
    max_two_exchange_pairs = max(row["two_exchange_pairs"] for row in all_rows)
    max_two_exchange_same_slope_pairs = max(
        row["two_exchange_same_slope_pairs"] for row in all_rows
    )
    max_two_exchange_different_slope_pairs = max(
        row["two_exchange_different_slope_pairs"] for row in all_rows
    )
    max_two_exchange_cores = max(row["two_exchange_cores"] for row in all_rows)
    max_two_exchange_minor_checks = max(
        row["two_exchange_minor_polynomial_checks"] for row in all_rows
    )
    max_two_exchange_bad_locator_checks = max(
        row["two_exchange_bad_locator_checks"] for row in all_rows
    )
    max_two_exchange_same_slope_clusters = max(
        row["two_exchange_same_slope_clusters"] for row in all_rows
    )
    max_two_exchange_same_slope_line_clusters = max(
        row["two_exchange_same_slope_line_clusters"] for row in all_rows
    )
    max_two_exchange_same_slope_fixed_root_lines = max(
        row["two_exchange_same_slope_fixed_root_lines"] for row in all_rows
    )
    max_two_exchange_same_slope_mobius_lines = max(
        row["two_exchange_same_slope_mobius_lines"] for row in all_rows
    )
    max_two_exchange_same_slope_product_mobius_lines = max(
        row["two_exchange_same_slope_product_mobius_lines"] for row in all_rows
    )
    max_two_exchange_same_slope_sum_mobius_lines = max(
        row["two_exchange_same_slope_sum_mobius_lines"] for row in all_rows
    )
    max_two_exchange_same_slope_line_two_exchange_pairs = max(
        row["two_exchange_same_slope_line_two_exchange_pairs"] for row in all_rows
    )
    max_two_exchange_same_slope_mobius_two_exchange_pairs = max(
        row["two_exchange_same_slope_mobius_two_exchange_pairs"] for row in all_rows
    )
    max_two_exchange_same_slope_mobius_pair_checks = max(
        row["two_exchange_same_slope_mobius_pair_checks"] for row in all_rows
    )
    max_two_exchange_same_slope_mobius_member = max(
        row["two_exchange_same_slope_mobius_member_max"] for row in all_rows
    )
    max_two_exchange_same_slope_plane_clusters = max(
        row["two_exchange_same_slope_plane_clusters"] for row in all_rows
    )
    max_two_exchange_same_slope_plane_lifts = max(
        row["two_exchange_same_slope_plane_lifts"] for row in all_rows
    )
    max_two_exchange_same_slope_plane_two_exchange_pairs = max(
        row["two_exchange_same_slope_plane_two_exchange_pairs"] for row in all_rows
    )
    max_two_exchange_same_slope_affine_member = max(
        row["two_exchange_same_slope_affine_member_max"] for row in all_rows
    )
    max_two_exchange_same_slope_lift_checks = max(
        row["two_exchange_same_slope_lift_checks"] for row in all_rows
    )
    max_two_exchange_det_line_components = max(
        row["two_exchange_det_line_components"] for row in all_rows
    )
    max_two_exchange_det_line_fixed_root = max(
        row["two_exchange_det_line_fixed_root"] for row in all_rows
    )
    max_two_exchange_det_line_product_mobius = max(
        row["two_exchange_det_line_product_mobius"] for row in all_rows
    )
    max_two_exchange_det_line_sum_mobius = max(
        row["two_exchange_det_line_sum_mobius"] for row in all_rows
    )
    max_two_exchange_det_line_constant_slope = max(
        row["two_exchange_det_line_constant_slope"] for row in all_rows
    )
    max_two_exchange_det_line_variable_slope = max(
        row["two_exchange_det_line_variable_slope"] for row in all_rows
    )
    max_two_exchange_det_line_slope = max(
        row["two_exchange_det_line_slope_max"] for row in all_rows
    )
    max_two_exchange_det_line_aperiodic = max(
        row["two_exchange_det_line_aperiodic_max"] for row in all_rows
    )
    max_two_exchange_det_line_point_checks = max(
        row["two_exchange_det_line_point_checks"] for row in all_rows
    )
    max_two_exchange_det_full_planes = max(
        row["two_exchange_det_full_planes"] for row in all_rows
    )
    max_two_exchange_det_full_plane_constant_slope = max(
        row["two_exchange_det_full_plane_constant_slope"] for row in all_rows
    )
    max_two_exchange_det_full_plane_variable_slope = max(
        row["two_exchange_det_full_plane_variable_slope"] for row in all_rows
    )
    max_two_exchange_det_full_plane_contained = max(
        row["two_exchange_det_full_plane_contained"] for row in all_rows
    )
    max_two_exchange_det_full_plane_den_rank = max(
        row["two_exchange_det_full_plane_den_rank_max"] for row in all_rows
    )
    max_two_exchange_det_full_plane_slope = max(
        row["two_exchange_det_full_plane_slope_max"] for row in all_rows
    )
    max_two_exchange_det_full_plane_aperiodic = max(
        row["two_exchange_det_full_plane_aperiodic_max"] for row in all_rows
    )
    max_two_exchange_det_full_plane_lifts = max(
        row["two_exchange_det_full_plane_lifts"] for row in all_rows
    )
    max_two_exchange_det_proper_lines = max(
        row["two_exchange_det_proper_lines"] for row in all_rows
    )
    max_two_exchange_det_proper_line_fixed_root = max(
        row["two_exchange_det_proper_line_fixed_root"] for row in all_rows
    )
    max_two_exchange_det_proper_line_product_mobius = max(
        row["two_exchange_det_proper_line_product_mobius"] for row in all_rows
    )
    max_two_exchange_det_proper_line_sum_mobius = max(
        row["two_exchange_det_proper_line_sum_mobius"] for row in all_rows
    )
    max_two_exchange_det_proper_line_constant_slope = max(
        row["two_exchange_det_proper_line_constant_slope"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_slope = max(
        row["two_exchange_det_proper_line_variable_slope"] for row in all_rows
    )
    max_two_exchange_det_proper_line_slope = max(
        row["two_exchange_det_proper_line_slope_max"] for row in all_rows
    )
    max_two_exchange_det_proper_line_aperiodic = max(
        row["two_exchange_det_proper_line_aperiodic_max"] for row in all_rows
    )
    max_two_exchange_det_proper_line_core = max(
        row["two_exchange_det_proper_line_core_max"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_injective = max(
        row["two_exchange_det_proper_line_variable_injective"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_pole = max(
        row["two_exchange_det_proper_line_variable_pole_max"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_aperiodic_slope = max(
        row["two_exchange_det_proper_line_variable_aperiodic_slope_max"]
        for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_injective_checks = max(
        row["two_exchange_det_proper_line_variable_injective_checks"]
        for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_aperiodic_slopes = max(
        row["two_exchange_det_proper_line_variable_aperiodic_slopes"]
        for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_new_slopes = max(
        row["two_exchange_det_proper_line_variable_new_slopes"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_new_slope = max(
        row["two_exchange_det_proper_line_variable_new_slope_max"]
        for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_nonfixed = max(
        row["two_exchange_det_proper_line_variable_nonfixed"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_anchored = max(
        row["two_exchange_det_proper_line_variable_anchored"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_unanchored = max(
        row["two_exchange_det_proper_line_variable_unanchored"] for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_domain_pair = max(
        row["two_exchange_det_proper_line_variable_domain_pair_max"]
        for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_domain_pair_checks = max(
        row["two_exchange_det_proper_line_variable_domain_pair_checks"]
        for row in all_rows
    )
    max_two_exchange_det_proper_line_variable_charged_slope_checks = max(
        row["two_exchange_det_proper_line_variable_charged_slope_checks"]
        for row in all_rows
    )
    max_total_slope_bound = max(row["root_slice_total_slope_bound"] for row in all_rows)
    max_root_new_slopes = max(row["root_slice_new_slope_count"] for row in all_rows)
    max_root_t3_core_locators = max(row["root_slice_t3_core_locators"] for row in all_rows)
    max_root_t3_slopes = max(row["root_slice_t3_slope_count"] for row in all_rows)
    max_root_t3_new_slopes = max(row["root_slice_t3_new_slope_count"] for row in all_rows)
    max_recursive_slope_bound = max(
        row["root_slice_recursive_slope_bound"] for row in all_rows
    )
    max_residual_slope_core_checks = max(
        row["root_slice_residual_slope_core_checks"] for row in all_rows
    )
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
    max_residual_top_packet_overlap_pairs = max(
        row["root_slice_residual_top_packet_overlap_pairs"] for row in all_rows
    )
    max_residual_top_packet_overlap = max(
        row["root_slice_residual_top_packet_overlap_max"] for row in all_rows
    )
    max_residual_components = max(
        row["root_slice_residual_components"] for row in all_rows
    )
    max_residual_nontrivial_components = max(
        row["root_slice_residual_nontrivial_components"] for row in all_rows
    )
    max_residual_isolated_components = max(
        row["root_slice_residual_isolated_components"] for row in all_rows
    )
    max_residual_boundary_isolated_components = max(
        row["root_slice_residual_boundary_isolated_components"] for row in all_rows
    )
    max_residual_component_size = max(
        row["root_slice_residual_component_max"] for row in all_rows
    )
    max_residual_component_clique_edges = max(
        row["root_slice_residual_component_clique_edges"] for row in all_rows
    )
    max_residual_common_companion_checks = max(
        row["root_slice_residual_common_companion_checks"] for row in all_rows
    )
    max_residual_top_lift_gate_checks = max(
        row["root_slice_residual_top_lift_gate_checks"] for row in all_rows
    )
    max_residual_top_anchor_checks = max(
        row["root_slice_residual_top_anchor_checks"] for row in all_rows
    )
    max_residual_top_common_lift_gate_checks = max(
        row["root_slice_residual_top_common_lift_gate_checks"] for row in all_rows
    )
    max_residual_top_numerator_anchor_checks = max(
        row["root_slice_residual_top_numerator_anchor_checks"] for row in all_rows
    )
    max_residual_top_face_gate_checks = max(
        row["root_slice_residual_top_face_gate_checks"] for row in all_rows
    )
    max_residual_top_face_noncontained = max(
        row["root_slice_residual_top_face_noncontained"] for row in all_rows
    )
    max_residual_top_face_aperiodic = max(
        row["root_slice_residual_top_face_aperiodic"] for row in all_rows
    )
    max_residual_top_face_residual = max(
        row["root_slice_residual_top_face_residual"] for row in all_rows
    )
    max_residual_top_face_peeled = max(
        row["root_slice_residual_top_face_peeled"] for row in all_rows
    )
    max_residual_anchor_lifted_faces = max(
        row["root_slice_residual_anchor_lifted_faces"] for row in all_rows
    )
    max_residual_anchor_escape = max(
        row["root_slice_residual_anchor_escape_locators"] for row in all_rows
    )
    max_residual_anchor_beta0_zero = max(
        row["root_slice_residual_anchor_beta0_zero"] for row in all_rows
    )
    max_residual_anchor_in_support = max(
        row["root_slice_residual_anchor_in_support"] for row in all_rows
    )
    max_residual_anchor_outside_domain = max(
        row["root_slice_residual_anchor_outside_domain"] for row in all_rows
    )
    max_residual_external_anchors = max(
        row["root_slice_residual_external_anchors"] for row in all_rows
    )
    max_residual_external_anchor_locator = max(
        row["root_slice_residual_external_anchor_locator_max"] for row in all_rows
    )
    max_residual_external_anchor_slope = max(
        row["root_slice_residual_external_anchor_slope_max"] for row in all_rows
    )
    max_residual_external_anchor_slope_fibers = max(
        row["root_slice_residual_external_anchor_slope_fibers"] for row in all_rows
    )
    max_residual_external_anchor_slope_fiber = max(
        row["root_slice_residual_external_anchor_slope_fiber_max"] for row in all_rows
    )
    max_residual_external_anchor_slope_core_checks = max(
        row["root_slice_residual_external_anchor_slope_core_checks"] for row in all_rows
    )
    max_residual_external_anchor_kernel_dim = max(
        row["root_slice_residual_external_anchor_kernel_dim_max"] for row in all_rows
    )
    max_residual_external_anchor_projective_points = max(
        row["root_slice_residual_external_anchor_projective_points"] for row in all_rows
    )
    max_residual_external_anchor_rich_points = max(
        row["root_slice_residual_external_anchor_rich_points"] for row in all_rows
    )
    max_residual_external_anchor_finite_rich_slopes = max(
        row["root_slice_residual_external_anchor_finite_rich_slopes"] for row in all_rows
    )
    max_residual_external_anchor_rich_residual_classes = max(
        row["root_slice_residual_external_anchor_rich_residual_classes"] for row in all_rows
    )
    max_residual_external_anchor_twist_checks = max(
        row["root_slice_residual_external_anchor_twist_checks"] for row in all_rows
    )
    max_residual_external_anchor_interpolation_checks = max(
        row["root_slice_residual_external_anchor_interpolation_checks"] for row in all_rows
    )
    max_residual_external_anchor_pinned_t1_checks = max(
        row["root_slice_residual_external_anchor_pinned_t1_checks"] for row in all_rows
    )
    max_residual_anchor_lift_checks = max(
        row["root_slice_residual_anchor_lift_gate_checks"] for row in all_rows
    )
    max_residual_anchor_isolated_checks = max(
        row["root_slice_residual_anchor_isolated_checks"] for row in all_rows
    )
    max_residual_anchor_projective_lift_checks = max(
        row["root_slice_residual_anchor_projective_lift_checks"] for row in all_rows
    )
    max_residual_anchor_projective_unique_checks = max(
        row["root_slice_residual_anchor_projective_unique_checks"] for row in all_rows
    )
    max_residual_projective_lift_fibers = max(
        row["root_slice_residual_projective_lift_fibers"] for row in all_rows
    )
    max_residual_projective_squarefree_fibers = max(
        row["root_slice_residual_projective_squarefree_fibers"] for row in all_rows
    )
    max_residual_projective_boundary_fibers = max(
        row["root_slice_residual_projective_boundary_fibers"] for row in all_rows
    )
    max_residual_projective_boundary_singletons = max(
        row["root_slice_residual_projective_boundary_singletons"] for row in all_rows
    )
    max_residual_projective_lift_fiber = max(
        row["root_slice_residual_projective_lift_fiber_max"] for row in all_rows
    )
    max_residual_projective_lift_pair_checks = max(
        row["root_slice_residual_projective_lift_pair_checks"] for row in all_rows
    )
    max_residual_anchor_finite_lift_checks = max(
        row["root_slice_residual_anchor_finite_lift_checks"] for row in all_rows
    )
    max_residual_anchor_repeated_lift_checks = max(
        row["root_slice_residual_anchor_repeated_lift_checks"] for row in all_rows
    )
    max_residual_anchor_offdomain_lift_checks = max(
        row["root_slice_residual_anchor_offdomain_lift_checks"] for row in all_rows
    )
    max_residual_anchor_infinity_checks = max(
        row["root_slice_residual_anchor_infinity_checks"] for row in all_rows
    )
    max_residual_lifted_slopes = max(
        row["root_slice_residual_lifted_slopes"] for row in all_rows
    )
    max_residual_escape_slopes = max(
        row["root_slice_residual_escape_slopes"] for row in all_rows
    )
    max_residual_lifted_escape_slope_overlap = max(
        row["root_slice_residual_lifted_escape_slope_overlap"] for row in all_rows
    )
    max_residual_escape_new_slopes = max(
        row["root_slice_residual_escape_new_slopes"] for row in all_rows
    )
    max_residual_lifted_core_slope_bound = max(
        row["root_slice_residual_lifted_core_slope_bound"] for row in all_rows
    )
    max_residual_recursion_bound = max(
        row["root_slice_residual_recursion_bound"] for row in all_rows
    )
    max_residual_new_escape_bound = max(
        row["root_slice_residual_new_escape_bound"] for row in all_rows
    )
    max_residual_active_new_escape_bound = max(
        row["root_slice_residual_active_new_escape_bound"] for row in all_rows
    )
    max_residual_active_face_new_escape_bound = max(
        row["root_slice_residual_active_face_new_escape_bound"] for row in all_rows
    )
    max_residual_boundary_arrangement_bound = max(
        row["root_slice_residual_boundary_arrangement_bound"] for row in all_rows
    )
    max_residual_boundary_slope_bound = max(
        row["root_slice_residual_boundary_slope_bound"] for row in all_rows
    )
    max_residual_boundary_active_anchors = max(
        row["root_slice_residual_boundary_active_anchors"] for row in all_rows
    )
    max_residual_boundary_anchor_slope_bound = max(
        row["root_slice_residual_boundary_anchor_slope_bound"] for row in all_rows
    )
    max_residual_boundary_field_slope_bound = max(
        row["root_slice_residual_boundary_field_slope_bound"] for row in all_rows
    )
    max_residual_active_lifted_core_slope_bound = max(
        row["root_slice_residual_active_lifted_core_slope_bound"] for row in all_rows
    )
    max_recursive_arrangement_bound = max(
        row["root_slice_recursive_arrangement_bound"] for row in all_rows
    )
    max_recursive_boundary_slope_bound = max(
        row["root_slice_recursive_boundary_slope_bound"] for row in all_rows
    )
    max_recursive_boundary_anchor_slope_bound = max(
        row["root_slice_recursive_boundary_anchor_slope_bound"] for row in all_rows
    )
    max_recursive_boundary_field_slope_bound = max(
        row["root_slice_recursive_boundary_field_slope_bound"] for row in all_rows
    )
    max_recursive_active_field_slope_bound = max(
        row["root_slice_recursive_active_field_slope_bound"] for row in all_rows
    )
    max_recursive_new_escape_bound = max(
        row["root_slice_recursive_new_escape_bound"] for row in all_rows
    )
    max_recursive_active_new_escape_bound = max(
        row["root_slice_recursive_active_new_escape_bound"] for row in all_rows
    )
    max_recursive_active_face_new_escape_bound = max(
        row["root_slice_recursive_active_face_new_escape_bound"] for row in all_rows
    )
    max_exact_active_face_bound = max(
        row["root_slice_exact_active_face_bound"] for row in all_rows
    )
    max_recursive_active_face_new_root_bound = max(
        row["root_slice_recursive_active_face_new_root_bound"] for row in all_rows
    )
    max_two_input_field_bound = max(
        row["root_slice_two_input_field_bound"] for row in all_rows
    )
    max_lifted_u_t1_cores = max(row["root_slice_lifted_u_t1_cores"] for row in all_rows)
    max_lifted_v_t1_cores = max(row["root_slice_lifted_v_t1_cores"] for row in all_rows)
    max_lifted_common_cores = max(row["root_slice_lifted_common_cores"] for row in all_rows)
    max_lifted_common_active_cores = max(
        row["root_slice_lifted_common_active_cores"] for row in all_rows
    )
    max_lifted_common_inactive_cores = max(
        row["root_slice_lifted_common_inactive_cores"] for row in all_rows
    )
    max_lifted_common_noncontained_faces = max(
        row["root_slice_lifted_common_core_noncontained_faces"] for row in all_rows
    )
    max_lifted_common_aperiodic_faces = max(
        row["root_slice_lifted_common_core_aperiodic_faces"] for row in all_rows
    )
    max_lifted_common_residual_faces = max(
        row["root_slice_lifted_common_core_residual_faces"] for row in all_rows
    )
    max_lifted_common_peeled_faces = max(
        row["root_slice_lifted_common_core_peeled_faces"] for row in all_rows
    )
    max_lifted_common_residual_singletons = max(
        row["root_slice_lifted_common_core_residual_singletons"] for row in all_rows
    )
    max_lifted_common_residual_packets = max(
        row["root_slice_lifted_common_core_residual_packets"] for row in all_rows
    )
    max_lifted_common_residual_faces_per_core = max(
        row["root_slice_lifted_common_core_max_residual_faces"] for row in all_rows
    )
    max_lifted_common_base_checks = max(
        row["root_slice_lifted_common_core_common_base_checks"] for row in all_rows
    )
    max_lifted_common_residual_slope_checks = max(
        row["root_slice_lifted_common_core_residual_slope_checks"] for row in all_rows
    )
    max_lifted_common_active_ratio_checks = max(
        row["root_slice_lifted_common_core_active_ratio_checks"] for row in all_rows
    )
    max_lifted_common_residual_slope_pair_checks = max(
        row["root_slice_lifted_common_core_residual_slope_pair_checks"] for row in all_rows
    )
    max_lifted_common_residual_slope_fiber = max(
        row["root_slice_lifted_common_core_residual_slope_fiber_max"] for row in all_rows
    )
    max_companion_checks = max(row["quadratic_companion_checks"] for row in all_rows)
    max_rank_one_zero = max(row["zero_det_direction_rank1_slices"] for row in all_rows)
    total_lines = sum(len(summary["case"].seeds) for summary in summaries) + 3
    print(
        "m1_all_line_hankel_aperiodic: PASS "
        f"cases={len(summaries)} line_samples={total_lines} "
        f"rank_one_probes=1 "
        f"t3_same_slope_probes=1 "
        f"t3_variable_new_slope_probes=1 "
        f"line_geometry_probes=1 "
        f"max_aperiodic_slopes={max_aperiodic} "
        f"max_one_exchange_pairs={max_one_exchange_pairs} "
        f"max_same_slope_one_exchange={max_same_slope_one_exchange_pairs} "
        f"max_same_slope_lift_slices={max_same_slope_lift_slices} "
        f"max_same_slope_lift_slopes={max_same_slope_lift_slopes} "
        f"max_same_slope_lift_next_cores={max_same_slope_lift_next_cores} "
        f"max_same_slope_lift_next_slopes={max_same_slope_lift_next_slopes} "
        f"max_same_slope_lift_member_checks={max_same_slope_lift_member_checks} "
        f"max_two_exchange_pairs={max_two_exchange_pairs} "
        f"max_two_exchange_same_slope={max_two_exchange_same_slope_pairs} "
        f"max_two_exchange_different_slope={max_two_exchange_different_slope_pairs} "
        f"max_two_exchange_cores={max_two_exchange_cores} "
        f"max_two_exchange_minor_checks={max_two_exchange_minor_checks} "
        f"max_two_exchange_bad_locator_checks={max_two_exchange_bad_locator_checks} "
        f"max_two_exchange_same_slope_clusters={max_two_exchange_same_slope_clusters} "
        f"max_two_exchange_same_slope_lines={max_two_exchange_same_slope_line_clusters} "
        f"max_two_exchange_same_slope_fixed_lines={max_two_exchange_same_slope_fixed_root_lines} "
        f"max_two_exchange_same_slope_mobius_lines={max_two_exchange_same_slope_mobius_lines} "
        f"max_two_exchange_same_slope_product_mobius_lines={max_two_exchange_same_slope_product_mobius_lines} "
        f"max_two_exchange_same_slope_sum_mobius_lines={max_two_exchange_same_slope_sum_mobius_lines} "
        f"max_two_exchange_same_slope_line_two_pairs={max_two_exchange_same_slope_line_two_exchange_pairs} "
        f"max_two_exchange_same_slope_mobius_two_pairs={max_two_exchange_same_slope_mobius_two_exchange_pairs} "
        f"max_two_exchange_same_slope_mobius_pair_checks={max_two_exchange_same_slope_mobius_pair_checks} "
        f"max_two_exchange_same_slope_mobius_member={max_two_exchange_same_slope_mobius_member} "
        f"max_two_exchange_same_slope_planes={max_two_exchange_same_slope_plane_clusters} "
        f"max_two_exchange_same_slope_plane_lifts={max_two_exchange_same_slope_plane_lifts} "
        f"max_two_exchange_same_slope_plane_two_pairs={max_two_exchange_same_slope_plane_two_exchange_pairs} "
        f"max_two_exchange_same_slope_affine_member={max_two_exchange_same_slope_affine_member} "
        f"max_two_exchange_same_slope_lift_checks={max_two_exchange_same_slope_lift_checks} "
        f"max_two_exchange_det_lines={max_two_exchange_det_line_components} "
        f"max_two_exchange_det_line_fixed={max_two_exchange_det_line_fixed_root} "
        f"max_two_exchange_det_line_product_mobius={max_two_exchange_det_line_product_mobius} "
        f"max_two_exchange_det_line_sum_mobius={max_two_exchange_det_line_sum_mobius} "
        f"max_two_exchange_det_line_constant={max_two_exchange_det_line_constant_slope} "
        f"max_two_exchange_det_line_variable={max_two_exchange_det_line_variable_slope} "
        f"max_two_exchange_det_line_slope={max_two_exchange_det_line_slope} "
        f"max_two_exchange_det_line_aperiodic={max_two_exchange_det_line_aperiodic} "
        f"max_two_exchange_det_line_point_checks={max_two_exchange_det_line_point_checks} "
        f"max_two_exchange_det_full_planes={max_two_exchange_det_full_planes} "
        f"max_two_exchange_det_full_plane_constant={max_two_exchange_det_full_plane_constant_slope} "
        f"max_two_exchange_det_full_plane_variable={max_two_exchange_det_full_plane_variable_slope} "
        f"max_two_exchange_det_full_plane_contained={max_two_exchange_det_full_plane_contained} "
        f"max_two_exchange_det_full_plane_den_rank={max_two_exchange_det_full_plane_den_rank} "
        f"max_two_exchange_det_full_plane_slope={max_two_exchange_det_full_plane_slope} "
        f"max_two_exchange_det_full_plane_aperiodic={max_two_exchange_det_full_plane_aperiodic} "
        f"max_two_exchange_det_full_plane_lifts={max_two_exchange_det_full_plane_lifts} "
        f"max_two_exchange_det_proper_lines={max_two_exchange_det_proper_lines} "
        f"max_two_exchange_det_proper_line_fixed={max_two_exchange_det_proper_line_fixed_root} "
        f"max_two_exchange_det_proper_line_product_mobius={max_two_exchange_det_proper_line_product_mobius} "
        f"max_two_exchange_det_proper_line_sum_mobius={max_two_exchange_det_proper_line_sum_mobius} "
        f"max_two_exchange_det_proper_line_constant={max_two_exchange_det_proper_line_constant_slope} "
        f"max_two_exchange_det_proper_line_variable={max_two_exchange_det_proper_line_variable_slope} "
        f"max_two_exchange_det_proper_line_slope={max_two_exchange_det_proper_line_slope} "
        f"max_two_exchange_det_proper_line_aperiodic={max_two_exchange_det_proper_line_aperiodic} "
        f"max_two_exchange_det_proper_line_core={max_two_exchange_det_proper_line_core} "
        f"max_two_exchange_det_proper_line_variable_injective={max_two_exchange_det_proper_line_variable_injective} "
        f"max_two_exchange_det_proper_line_variable_pole={max_two_exchange_det_proper_line_variable_pole} "
        f"max_two_exchange_det_proper_line_variable_aperiodic_slope={max_two_exchange_det_proper_line_variable_aperiodic_slope} "
        f"max_two_exchange_det_proper_line_variable_injective_checks={max_two_exchange_det_proper_line_variable_injective_checks} "
        f"max_two_exchange_det_proper_line_variable_aperiodic_slopes={max_two_exchange_det_proper_line_variable_aperiodic_slopes} "
        f"max_two_exchange_det_proper_line_variable_new_slopes={max_two_exchange_det_proper_line_variable_new_slopes} "
        f"max_two_exchange_det_proper_line_variable_new_slope={max_two_exchange_det_proper_line_variable_new_slope} "
        f"max_two_exchange_det_proper_line_variable_nonfixed={max_two_exchange_det_proper_line_variable_nonfixed} "
        f"max_two_exchange_det_proper_line_variable_anchored={max_two_exchange_det_proper_line_variable_anchored} "
        f"max_two_exchange_det_proper_line_variable_unanchored={max_two_exchange_det_proper_line_variable_unanchored} "
        f"max_two_exchange_det_proper_line_variable_domain_pair={max_two_exchange_det_proper_line_variable_domain_pair} "
        f"max_two_exchange_det_proper_line_variable_domain_pair_checks={max_two_exchange_det_proper_line_variable_domain_pair_checks} "
        f"max_two_exchange_det_proper_line_variable_charged_slope_checks={max_two_exchange_det_proper_line_variable_charged_slope_checks} "
        f"max_total_slope_bound={max_total_slope_bound} "
        f"max_root_new_slopes={max_root_new_slopes} "
        f"max_root_t3_core_locators={max_root_t3_core_locators} "
        f"max_root_t3_slopes={max_root_t3_slopes} "
        f"max_root_t3_new_slopes={max_root_t3_new_slopes} "
        f"max_recursive_slope_bound={max_recursive_slope_bound} "
        f"max_strict_degree={max_strict_degree} "
        f"max_root_residual_slope_core_checks={max_residual_slope_core_checks} "
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
        f"max_root_residual_top_packet_overlap_pairs={max_residual_top_packet_overlap_pairs} "
        f"max_root_residual_top_packet_overlap={max_residual_top_packet_overlap} "
        f"max_root_residual_components={max_residual_components} "
        f"max_root_residual_nontrivial_components={max_residual_nontrivial_components} "
        f"max_root_residual_isolated_components={max_residual_isolated_components} "
        f"max_root_residual_boundary_isolated_components={max_residual_boundary_isolated_components} "
        f"max_root_residual_component_size={max_residual_component_size} "
        f"max_root_residual_component_clique_edges={max_residual_component_clique_edges} "
        f"max_root_residual_common_companion_checks={max_residual_common_companion_checks} "
        f"max_root_residual_top_lift_gate_checks={max_residual_top_lift_gate_checks} "
        f"max_root_residual_top_anchor_checks={max_residual_top_anchor_checks} "
        f"max_root_residual_top_common_lift_gate_checks={max_residual_top_common_lift_gate_checks} "
        f"max_root_residual_top_numerator_anchor_checks={max_residual_top_numerator_anchor_checks} "
        f"max_root_residual_top_face_gate_checks={max_residual_top_face_gate_checks} "
        f"max_root_residual_top_face_noncontained={max_residual_top_face_noncontained} "
        f"max_root_residual_top_face_aperiodic={max_residual_top_face_aperiodic} "
        f"max_root_residual_top_face_residual={max_residual_top_face_residual} "
        f"max_root_residual_top_face_peeled={max_residual_top_face_peeled} "
        f"max_root_residual_anchor_lifted_faces={max_residual_anchor_lifted_faces} "
        f"max_root_residual_anchor_escape={max_residual_anchor_escape} "
        f"max_root_residual_anchor_beta0_zero={max_residual_anchor_beta0_zero} "
        f"max_root_residual_anchor_in_support={max_residual_anchor_in_support} "
        f"max_root_residual_anchor_outside_domain={max_residual_anchor_outside_domain} "
        f"max_root_residual_external_anchors={max_residual_external_anchors} "
        f"max_root_residual_external_anchor_locator={max_residual_external_anchor_locator} "
        f"max_root_residual_external_anchor_slope={max_residual_external_anchor_slope} "
        f"max_root_residual_external_anchor_slope_fibers={max_residual_external_anchor_slope_fibers} "
        f"max_root_residual_external_anchor_slope_fiber={max_residual_external_anchor_slope_fiber} "
        f"max_root_residual_external_anchor_slope_core_checks={max_residual_external_anchor_slope_core_checks} "
        f"max_root_residual_external_anchor_kernel_dim={max_residual_external_anchor_kernel_dim} "
        f"max_root_residual_external_anchor_projective_points={max_residual_external_anchor_projective_points} "
        f"max_root_residual_external_anchor_rich_points={max_residual_external_anchor_rich_points} "
        f"max_root_residual_external_anchor_finite_rich_slopes={max_residual_external_anchor_finite_rich_slopes} "
        f"max_root_residual_external_anchor_rich_residual_classes={max_residual_external_anchor_rich_residual_classes} "
        f"max_root_residual_external_anchor_twist_checks={max_residual_external_anchor_twist_checks} "
        f"max_root_residual_external_anchor_interpolation_checks={max_residual_external_anchor_interpolation_checks} "
        f"max_root_residual_external_anchor_pinned_t1_checks={max_residual_external_anchor_pinned_t1_checks} "
        f"max_root_residual_anchor_lift_checks={max_residual_anchor_lift_checks} "
        f"max_root_residual_anchor_isolated_checks={max_residual_anchor_isolated_checks} "
        f"max_root_residual_anchor_projective_lift_checks={max_residual_anchor_projective_lift_checks} "
        f"max_root_residual_anchor_projective_unique_checks={max_residual_anchor_projective_unique_checks} "
        f"max_root_residual_projective_lift_fibers={max_residual_projective_lift_fibers} "
        f"max_root_residual_projective_squarefree_fibers={max_residual_projective_squarefree_fibers} "
        f"max_root_residual_projective_boundary_fibers={max_residual_projective_boundary_fibers} "
        f"max_root_residual_projective_boundary_singletons={max_residual_projective_boundary_singletons} "
        f"max_root_residual_projective_lift_fiber={max_residual_projective_lift_fiber} "
        f"max_root_residual_projective_lift_pair_checks={max_residual_projective_lift_pair_checks} "
        f"max_root_residual_anchor_finite_lift_checks={max_residual_anchor_finite_lift_checks} "
        f"max_root_residual_anchor_repeated_lift_checks={max_residual_anchor_repeated_lift_checks} "
        f"max_root_residual_anchor_offdomain_lift_checks={max_residual_anchor_offdomain_lift_checks} "
        f"max_root_residual_anchor_infinity_checks={max_residual_anchor_infinity_checks} "
        f"max_root_residual_lifted_slopes={max_residual_lifted_slopes} "
        f"max_root_residual_escape_slopes={max_residual_escape_slopes} "
        f"max_root_residual_lifted_escape_slope_overlap={max_residual_lifted_escape_slope_overlap} "
        f"max_root_residual_escape_new_slopes={max_residual_escape_new_slopes} "
        f"max_root_residual_lifted_core_slope_bound={max_residual_lifted_core_slope_bound} "
        f"max_root_residual_recursion_bound={max_residual_recursion_bound} "
        f"max_root_residual_new_escape_bound={max_residual_new_escape_bound} "
        f"max_root_residual_active_new_escape_bound={max_residual_active_new_escape_bound} "
        f"max_root_residual_active_face_new_escape_bound={max_residual_active_face_new_escape_bound} "
        f"max_root_residual_boundary_arrangement_bound={max_residual_boundary_arrangement_bound} "
        f"max_root_residual_boundary_slope_bound={max_residual_boundary_slope_bound} "
        f"max_root_residual_boundary_active_anchors={max_residual_boundary_active_anchors} "
        f"max_root_residual_boundary_anchor_slope_bound={max_residual_boundary_anchor_slope_bound} "
        f"max_root_residual_boundary_field_slope_bound={max_residual_boundary_field_slope_bound} "
        f"max_root_residual_active_lifted_core_slope_bound={max_residual_active_lifted_core_slope_bound} "
        f"max_root_recursive_arrangement_bound={max_recursive_arrangement_bound} "
        f"max_root_recursive_boundary_slope_bound={max_recursive_boundary_slope_bound} "
        f"max_root_recursive_boundary_anchor_slope_bound={max_recursive_boundary_anchor_slope_bound} "
        f"max_root_recursive_boundary_field_slope_bound={max_recursive_boundary_field_slope_bound} "
        f"max_root_recursive_active_field_slope_bound={max_recursive_active_field_slope_bound} "
        f"max_root_recursive_new_escape_bound={max_recursive_new_escape_bound} "
        f"max_root_recursive_active_new_escape_bound={max_recursive_active_new_escape_bound} "
        f"max_root_recursive_active_face_new_escape_bound={max_recursive_active_face_new_escape_bound} "
        f"max_root_exact_active_face_bound={max_exact_active_face_bound} "
        f"max_root_recursive_active_face_new_root_bound={max_recursive_active_face_new_root_bound} "
        f"max_root_two_input_field_bound={max_two_input_field_bound} "
        f"max_lifted_u_t1_cores={max_lifted_u_t1_cores} "
        f"max_lifted_v_t1_cores={max_lifted_v_t1_cores} "
        f"max_lifted_common_cores={max_lifted_common_cores} "
        f"max_lifted_common_active_cores={max_lifted_common_active_cores} "
        f"max_lifted_common_inactive_cores={max_lifted_common_inactive_cores} "
        f"max_lifted_common_noncontained_faces={max_lifted_common_noncontained_faces} "
        f"max_lifted_common_aperiodic_faces={max_lifted_common_aperiodic_faces} "
        f"max_lifted_common_residual_faces={max_lifted_common_residual_faces} "
        f"max_lifted_common_peeled_faces={max_lifted_common_peeled_faces} "
        f"max_lifted_common_residual_singletons={max_lifted_common_residual_singletons} "
        f"max_lifted_common_residual_packets={max_lifted_common_residual_packets} "
        f"max_lifted_common_residual_faces_per_core={max_lifted_common_residual_faces_per_core} "
        f"max_lifted_common_base_checks={max_lifted_common_base_checks} "
        f"max_lifted_common_residual_slope_checks={max_lifted_common_residual_slope_checks} "
        f"max_lifted_common_active_ratio_checks={max_lifted_common_active_ratio_checks} "
        f"max_lifted_common_residual_slope_pair_checks={max_lifted_common_residual_slope_pair_checks} "
        f"max_lifted_common_residual_slope_fiber={max_lifted_common_residual_slope_fiber} "
        f"max_quad_companion_checks={max_companion_checks} "
        f"max_rank_one_zero_slices={max_rank_one_zero}"
    )


if __name__ == "__main__":
    main()
