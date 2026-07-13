#!/usr/bin/env python3
"""Verify the selector-free direction-distance all-pair compiler.

The checker is deterministic, uses only the Python standard library, and
keeps every check active under optimized Python.  It verifies complete pair families,
including same-slope multiplicity, against the high-direction extension-ball
bound and the minimum-lift realized-puncture bound.

Usage:
  python3 experimental/scripts/verify_selector_free_direction_distance_all_pair.py --summary-only
  python3 experimental/scripts/verify_selector_free_direction_distance_all_pair.py --check
  python3 experimental/scripts/verify_selector_free_direction_distance_all_pair.py --tamper-selftest
"""

import argparse
import copy
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = (
    ROOT
    / "experimental/data/certificates/selector-free-direction-distance-all-pair"
    / "selector_free_direction_distance_all_pair.json"
)

FORMULAS = {
    "realized_weighted": (
        "|P| <= sum_{w in W_P} floor(d/max(1,d+wt(w)-t))"
    ),
    "high": "D_high>0 => |P| <= floor(N(d-t)/D_high)",
    "low": "D_low>0 => |P| <= d floor(M(Delta-rho)/D_low)",
    "rank": "affdim(E_P) <= affdim(W_P)+1 <= |W_P|",
    "residual": "D_high <= 0 and D_low <= 0",
}

EXPECTED_SOURCES = {
    "base": "fe93bb59dff3d022f66a097208e17c27e1e0deb4",
    "high_direction_predecessor": {
        "pr": 555,
        "head": "994f62dd8425e456897d013243204e49a8e93f98",
        "author": "DannyExperiments",
    },
    "minimum_lift_predecessor": {
        "pr": 619,
        "head": "861f678d387d7ba8ef1eb894859e6496645b779c",
        "author": "DannyExperiments",
    },
    "all_pair_target": {
        "pr": 715,
        "head": "203701154afa0f6cb53e01c5f9d40cf46e4ff996",
        "author": "latifkasuli",
    },
    "rational_host_boundary": {
        "pr": 721,
        "head": "aa66634ea1e6026026dab76ed38ac5883780efcf",
        "author": "DannyExperiments",
    },
    "all_pair_affine_core": {
        "pr": 737,
        "head": "8fcd4152709889da768ec1453d05ec09bccfb41a",
        "author": "holmbuar",
    },
}

EXPECTED_NONCLAIMS = [
    "no theorem extracting a hosted chart for y0 and y1",
    "no payment when both high and low denominators are nonpositive",
    "no witness-exhaustive atlas or profile-scale comparison",
    "no raw LineRay transversality before common-support removal",
    "no general sublinear realized-list rank outside the paid branches",
    "no deployed finite-row or Grand MCA/List theorem",
]

EXPECTED_CERTIFICATE_KEYS = {
    "schema",
    "status",
    "lean_status",
    "hard_input",
    "theorem",
    "formulas",
    "sources",
    "computed_summary",
    "nonclaims",
}

SWEEP_PARAMETERS = (
    (3, 3, 2, 1),
    (5, 4, 2, 1),
    (5, 5, 3, 1),
    (5, 5, 3, 2),
)

EXPECTED_SWEEP_ROWS = (
    {
        "q": 3,
        "N": 3,
        "R": 2,
        "kappa": 1,
        "t": 1,
        "directions": 4,
        "parameter_rows": 36,
        "nonempty_complete_families": 36,
        "complete_pairs": 66,
        "distinct_slopes": 66,
        "families_with_same_slope_multiplicity": 0,
        "same_slope_fibers": 0,
        "same_slope_excess_pairs": 0,
        "realized_words": 60,
        "exact_weighted_budget": 69,
        "exact_weighted_equalities": 33,
        "rank_cap_equalities": 6,
        "high_only": 9,
        "both_paid": 0,
        "low_only": 27,
        "unpaid": 0,
        "maximum_pairs": 3,
        "maximum_slopes": 3,
        "maximum_same_slope_fiber": 1,
        "maximum_same_slope_excess": 0,
        "maximum_puncture_cluster": 2,
    },
    {
        "q": 5,
        "N": 4,
        "R": 2,
        "kappa": 2,
        "t": 1,
        "directions": 6,
        "parameter_rows": 150,
        "nonempty_complete_families": 150,
        "complete_pairs": 430,
        "distinct_slopes": 430,
        "families_with_same_slope_multiplicity": 0,
        "same_slope_fibers": 0,
        "same_slope_excess_pairs": 0,
        "realized_words": 390,
        "exact_weighted_budget": 440,
        "exact_weighted_equalities": 140,
        "rank_cap_equalities": 40,
        "high_only": 50,
        "both_paid": 0,
        "low_only": 100,
        "unpaid": 0,
        "maximum_pairs": 4,
        "maximum_slopes": 4,
        "maximum_same_slope_fiber": 1,
        "maximum_same_slope_excess": 0,
        "maximum_puncture_cluster": 2,
    },
    {
        "q": 5,
        "N": 5,
        "R": 3,
        "kappa": 2,
        "t": 1,
        "directions": 31,
        "parameter_rows": 3_875,
        "nonempty_complete_families": 2_355,
        "complete_pairs": 3_155,
        "distinct_slopes": 3_155,
        "families_with_same_slope_multiplicity": 0,
        "same_slope_fibers": 0,
        "same_slope_excess_pairs": 0,
        "realized_words": 2_655,
        "exact_weighted_budget": 3_280,
        "exact_weighted_equalities": 2_230,
        "rank_cap_equalities": 500,
        "high_only": 105,
        "both_paid": 1_825,
        "low_only": 425,
        "unpaid": 0,
        "maximum_pairs": 2,
        "maximum_slopes": 2,
        "maximum_same_slope_fiber": 1,
        "maximum_same_slope_excess": 0,
        "maximum_puncture_cluster": 2,
    },
    {
        "q": 5,
        "N": 5,
        "R": 3,
        "kappa": 2,
        "t": 2,
        "directions": 31,
        "parameter_rows": 3_875,
        "nonempty_complete_families": 3_875,
        "complete_pairs": 23_155,
        "distinct_slopes": 17_155,
        "families_with_same_slope_multiplicity": 2_420,
        "same_slope_fibers": 6_000,
        "same_slope_excess_pairs": 6_000,
        "realized_words": 16_475,
        "exact_weighted_budget": 24_850,
        "exact_weighted_equalities": 2_485,
        "rank_cap_equalities": 900,
        "high_only": 0,
        "both_paid": 0,
        "low_only": 0,
        "unpaid": 3_875,
        "maximum_pairs": 10,
        "maximum_slopes": 5,
        "maximum_same_slope_fiber": 2,
        "maximum_same_slope_excess": 5,
        "maximum_puncture_cluster": 3,
    },
)

EXPECTED_SWEEP_TOTALS = {
    "direction_rows": 72,
    "parameter_rows": 7_936,
    "nonempty_complete_families": 6_416,
    "complete_pairs": 26_806,
    "distinct_slopes": 20_806,
    "families_with_same_slope_multiplicity": 2_420,
    "same_slope_fibers": 6_000,
    "same_slope_excess_pairs": 6_000,
    "realized_words": 19_580,
    "exact_weighted_budget": 28_639,
    "exact_weighted_equalities": 4_888,
    "rank_cap_equalities": 1_446,
    "high_only": 164,
    "both_paid": 1_825,
    "low_only": 552,
    "unpaid": 3_875,
    "maximum_pairs": 10,
    "maximum_slopes": 5,
    "maximum_same_slope_fiber": 2,
    "maximum_same_slope_excess": 5,
    "maximum_puncture_cluster": 3,
}


class VerificationError(RuntimeError):
    """A fail-closed verifier condition failed."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def is_prime(value):
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


def add(first, second, modulus):
    require(len(first) == len(second), "vector length mismatch")
    return tuple((left + right) % modulus for left, right in zip(first, second))


def subtract(first, second, modulus):
    require(len(first) == len(second), "vector length mismatch")
    return tuple((left - right) % modulus for left, right in zip(first, second))


def scale(scalar, vector, modulus):
    return tuple((scalar * value) % modulus for value in vector)


def weight(vector):
    return sum(value != 0 for value in vector)


def support(vector):
    return tuple(index for index, value in enumerate(vector) if value != 0)


def restrict(vector, indices):
    return tuple(vector[index] for index in indices)


def rref(matrix, modulus, width=None):
    if not matrix:
        require(width is not None, "empty matrix needs an explicit width")
        return [], []
    work = [list(row) for row in matrix]
    column_count = len(work[0])
    require(all(len(row) == column_count for row in work), "ragged matrix")
    pivots = []
    active = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(active, len(work))
                if work[row][column] % modulus
            ),
            None,
        )
        if pivot is None:
            continue
        work[active], work[pivot] = work[pivot], work[active]
        inverse = pow(work[active][column] % modulus, -1, modulus)
        work[active] = [value * inverse % modulus for value in work[active]]
        for row in range(len(work)):
            if row == active:
                continue
            factor = work[row][column] % modulus
            if factor:
                work[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(work[row], work[active])
                ]
        pivots.append(column)
        active += 1
        if active == len(work):
            break
    return work, pivots


def matrix_rank(matrix, modulus, width=None):
    return len(rref(matrix, modulus, width=width)[1])


def nullspace_basis(matrix, modulus, width):
    reduced, pivots = rref(matrix, modulus, width=width)
    if matrix:
        require(len(matrix[0]) == width, "nullspace width mismatch")
    free_columns = [column for column in range(width) if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-reduced[row][free]) % modulus
        basis.append(tuple(vector))
    return tuple(basis)


def linear_combination(coefficients, vectors, modulus, width):
    require(len(coefficients) == len(vectors), "coefficient count mismatch")
    result = [0] * width
    for coefficient, vector in zip(coefficients, vectors):
        require(len(vector) == width, "combination width mismatch")
        for index, value in enumerate(vector):
            result[index] = (result[index] + coefficient * value) % modulus
    return tuple(result)


def enumerate_code(basis, modulus, width):
    if not basis:
        return ((0,) * width,)
    return tuple(
        linear_combination(coefficients, basis, modulus, width)
        for coefficients in product(range(modulus), repeat=len(basis))
    )


def mat_vec(matrix, vector, modulus):
    require(all(len(row) == len(vector) for row in matrix), "matrix/vector mismatch")
    return tuple(
        sum(entry * value for entry, value in zip(row, vector)) % modulus
        for row in matrix
    )


def in_span(vector, generators, modulus):
    if not generators:
        return all(value % modulus == 0 for value in vector)
    require(all(len(row) == len(vector) for row in generators), "span width mismatch")
    return matrix_rank(tuple(generators) + (vector,), modulus) == matrix_rank(
        generators, modulus
    )


def affine_rank(vectors, modulus):
    require(vectors, "affine rank needs a nonempty family")
    if len(vectors) == 1:
        return 0
    base = vectors[0]
    return matrix_rank(
        tuple(subtract(vector, base, modulus) for vector in vectors[1:]),
        modulus,
        width=len(base),
    )


def parity_matrix(modulus, length, redundancy):
    require(length <= modulus, "canonical evaluation points collide")
    return tuple(
        tuple(pow(point, degree, modulus) for point in range(length))
        for degree in range(redundancy)
    )


def matrix_columns(matrix, indices):
    return tuple(
        tuple(row[index] for row in matrix)
        for index in indices
    )


def normalize_projective(vector, modulus):
    first = next(value for value in vector if value)
    inverse = pow(first, -1, modulus)
    return tuple(inverse * value % modulus for value in vector)


def low_weight_vectors(modulus, length, radius):
    yield (0,) * length
    for size in range(1, radius + 1):
        for selected in combinations(range(length), size):
            for values in product(range(1, modulus), repeat=size):
                vector = [0] * length
                for index, value in zip(selected, values):
                    vector[index] = value
                yield tuple(vector)


def code_distance(code):
    nonzero = [weight(vector) for vector in code if any(vector)]
    require(nonzero, "distance requested for the zero code")
    return min(nonzero)


class SmallContext:
    """Cached exact data for one small canonical prime-field chart."""

    def __init__(self, modulus, length, redundancy):
        require(is_prime(modulus), "modulus is not prime")
        require(1 <= redundancy < length <= modulus, "invalid chart dimensions")
        self.q = modulus
        self.N = length
        self.R = redundancy
        self.kappa = length - redundancy
        self.matrix = parity_matrix(modulus, length, redundancy)
        require(
            matrix_rank(self.matrix, modulus) == redundancy,
            "parity matrix lost row rank",
        )
        self.target_vectors = tuple(product(range(modulus), repeat=redundancy))
        self.fibers = defaultdict(list)
        for vector in product(range(modulus), repeat=length):
            self.fibers[mat_vec(self.matrix, vector, modulus)].append(vector)
        zero = (0,) * redundancy
        self.kernel = tuple(self.fibers[zero])
        self.kernel_basis = nullspace_basis(self.matrix, modulus, length)
        require(len(self.kernel_basis) == self.kappa, "kernel dimension mismatch")
        require(
            set(enumerate_code(self.kernel_basis, modulus, length))
            == set(self.kernel),
            "kernel basis enumeration mismatch",
        )
        require(len(self.kernel) == modulus ** self.kappa, "kernel size mismatch")
        require(code_distance(self.kernel) == redundancy + 1, "kernel is not MDS")
        self.directions = tuple(
            sorted(
                {
                    normalize_projective(vector, modulus)
                    for vector in self.target_vectors
                    if any(vector)
                }
            )
        )
        self.direction_records = {}
        for direction in self.directions:
            lift = min(
                self.fibers[direction],
                key=lambda vector: (weight(vector), vector),
            )
            self.direction_records[direction] = build_direction_record(
                modulus,
                self.matrix,
                self.kernel,
                self.kernel_basis,
                direction,
                lift,
            )
        self.error_cache = {}

    def errors_and_spans(self, radius):
        if radius not in self.error_cache:
            by_syndrome = defaultdict(list)
            span_sets = {}
            for error in low_weight_vectors(self.q, self.N, radius):
                exact_support = support(error)
                by_syndrome[mat_vec(self.matrix, error, self.q)].append(error)
                if exact_support not in span_sets:
                    columns = matrix_columns(self.matrix, exact_support)
                    span_sets[exact_support] = set(
                        enumerate_code(columns, self.q, self.R)
                    )
            self.error_cache[radius] = (by_syndrome, span_sets)
        return self.error_cache[radius]


def build_direction_record(modulus, matrix, kernel, kernel_basis, y1, lift):
    length = len(matrix[0])
    redundancy = len(matrix)
    require(mat_vec(matrix, lift, modulus) == y1, "direction lift has wrong syndrome")
    direction_distance = min(
        weight(add(lift, kernel_word, modulus)) for kernel_word in kernel
    )
    require(weight(lift) == direction_distance, "direction lift is not minimum")
    require(1 <= direction_distance <= redundancy, "direction distance out of range")
    direction_support = support(lift)
    puncture = tuple(
        index for index in range(length) if index not in set(direction_support)
    )
    punctured_length = length - direction_distance
    punctured_distance = redundancy + 1 - direction_distance
    require(len(puncture) == punctured_length, "puncture length mismatch")
    punctured_basis = tuple(restrict(vector, puncture) for vector in kernel_basis)
    require(
        matrix_rank(punctured_basis, modulus, width=punctured_length)
        == len(kernel_basis),
        "minimum-lift puncture is not injective",
    )
    punctured_code = tuple(restrict(vector, puncture) for vector in kernel)
    require(len(set(punctured_code)) == len(kernel), "punctured kernel collision")
    require(
        code_distance(punctured_code) == punctured_distance,
        "punctured kernel distance mismatch",
    )
    extension_code = frozenset(
        add(kernel_word, scale(gamma, lift, modulus), modulus)
        for gamma in range(modulus)
        for kernel_word in kernel
    )
    require(
        code_distance(extension_code) == direction_distance,
        "extension-code distance mismatch",
    )
    return {
        "v": lift,
        "d": direction_distance,
        "J": direction_support,
        "I": puncture,
        "M": punctured_length,
        "Delta": punctured_distance,
        "extension_code": extension_code,
    }


def complete_pair_family(context, y0, y1, radius):
    by_syndrome, span_sets = context.errors_and_spans(radius)
    pairs = []
    for gamma in range(context.q):
        target = add(y0, scale(gamma, y1, context.q), context.q)
        for error in by_syndrome.get(target, ()):
            span = span_sets[support(error)]
            if not (y0 in span and y1 in span):
                pairs.append((gamma, error))
    require(len(set(pairs)) == len(pairs), "complete family contains duplicates")
    return tuple(pairs)


def transverse(matrix, y0, y1, error, modulus):
    columns = matrix_columns(matrix, support(error))
    return not (
        in_span(y0, columns, modulus) and in_span(y1, columns, modulus)
    )


def verify_pair_family(
    modulus,
    matrix,
    kernel,
    kernel_basis,
    b0,
    y0,
    y1,
    pairs,
    radius,
    direction,
    label,
):
    require(pairs, label + ": empty pair family")
    length = len(matrix[0])
    redundancy = len(matrix)
    require(mat_vec(matrix, b0, modulus) == y0, label + ": bad y0 lift")
    require(any(y1), label + ": zero direction syndrome")
    require(len(set(pairs)) == len(pairs), label + ": duplicate pair")
    errors = tuple(error for _, error in pairs)
    require(len(set(errors)) == len(errors), label + ": pair/error map is not injective")
    for gamma, error in pairs:
        require(0 <= gamma < modulus, label + ": slope outside field")
        require(len(error) == length, label + ": error width mismatch")
        expected = add(y0, scale(gamma, y1, modulus), modulus)
        require(mat_vec(matrix, error, modulus) == expected, label + ": bad syndrome")
        require(weight(error) <= radius, label + ": error exceeds radius")
        require(transverse(matrix, y0, y1, error, modulus), label + ": nontransverse pair")

    lift = direction["v"]
    distance = direction["d"]
    require(mat_vec(matrix, lift, modulus) == y1, label + ": bad direction record")
    extension_words = set()
    for gamma, error in pairs:
        kernel_word = subtract(
            subtract(error, b0, modulus),
            scale(gamma, lift, modulus),
            modulus,
        )
        require(mat_vec(matrix, kernel_word, modulus) == (0,) * redundancy,
                label + ": bad kernel decomposition")
        codeword = subtract(b0, error, modulus)
        require(
            codeword == scale(-1, add(scale(gamma, lift, modulus), kernel_word, modulus), modulus),
            label + ": extension identity failed",
        )
        require(codeword in direction["extension_code"], label + ": extension membership failed")
        require(weight(subtract(codeword, b0, modulus)) <= radius,
                label + ": extension word outside ball")
        extension_words.add(codeword)
    require(len(extension_words) == len(pairs), label + ": extension words collide")

    high_denominator = (length - radius) ** 2 - length * (length - distance)
    high_bound = None
    high_ball_size = None
    if high_denominator > 0:
        high_bound = length * (distance - radius) // high_denominator
        high_ball_size = sum(
            weight(subtract(codeword, b0, modulus)) <= radius
            for codeword in direction["extension_code"]
        )
        require(len(pairs) <= high_ball_size <= high_bound,
                label + ": high-direction bound failed")

    clusters = defaultdict(list)
    realized_u = {}
    puncture = direction["I"]
    for gamma, error in pairs:
        u = subtract(error, scale(gamma, lift, modulus), modulus)
        require(mat_vec(matrix, u, modulus) == y0, label + ": bad affine lift")
        w = restrict(u, puncture)
        require(w == restrict(error, puncture), label + ": puncture identity failed")
        if w in realized_u:
            require(realized_u[w] == u, label + ": affine puncture collision")
        else:
            realized_u[w] = u
        clusters[w].append((gamma, error, u))

    realized_words = tuple(sorted(clusters))
    rho = min(radius, direction["M"])
    require(all(weight(word) <= rho for word in realized_words),
            label + ": realized word exceeds rho")
    exact_budget = 0
    cluster_sizes = []
    for word in realized_words:
        rows = clusters[word]
        require(len({gamma for gamma, _, _ in rows}) == len(rows),
                label + ": puncture cluster repeats a slope")
        demand = max(1, distance + weight(word) - radius)
        zero_sets = []
        for _, error, _ in rows:
            zeros = frozenset(index for index in direction["J"] if error[index] == 0)
            require(len(zeros) >= demand, label + ": zero demand failed")
            zero_sets.append(zeros)
        zero_union = set().union(*zero_sets)
        require(sum(len(zeros) for zeros in zero_sets) == len(zero_union),
                label + ": a direction coordinate serves two slopes")
        cap = distance // demand
        require(len(rows) <= cap, label + ": cluster cap failed")
        exact_budget += cap
        cluster_sizes.append(len(rows))
    require(len(pairs) <= exact_budget, label + ": exact realized bound failed")

    for first, second in combinations(realized_words, 2):
        require(weight(subtract(first, second, modulus)) >= direction["Delta"],
                label + ": realized words violate punctured distance")

    u_rank = affine_rank(tuple(realized_u[word] for word in realized_words), modulus)
    w_rank = affine_rank(realized_words, modulus)
    pair_rank = affine_rank(errors, modulus)
    require(u_rank == w_rank, label + ": puncture changed affine rank")
    require(pair_rank <= w_rank + 1 <= len(realized_words),
            label + ": realized affine-rank cap failed")

    low_denominator = (
        direction["Delta"] * direction["M"]
        - 2 * rho * direction["M"]
        + rho * rho
    )
    low_list_bound = None
    low_pair_bound = None
    if low_denominator > 0:
        low_list_bound = (
            direction["M"] * (direction["Delta"] - rho) // low_denominator
        )
        low_pair_bound = distance * low_list_bound
        require(len(realized_words) <= low_list_bound,
                label + ": realized Johnson bound failed")
        require(len(pairs) <= low_pair_bound, label + ": low pair bound failed")

    slope_counts = Counter(gamma for gamma, _ in pairs)
    return {
        "pairs": len(pairs),
        "slopes": len(slope_counts),
        "same_slope_fibers": sum(count > 1 for count in slope_counts.values()),
        "same_slope_excess": sum(count - 1 for count in slope_counts.values()),
        "maximum_same_slope_fiber": max(slope_counts.values()),
        "direction_distance": distance,
        "M": direction["M"],
        "Delta": direction["Delta"],
        "rho": rho,
        "realized_words": len(realized_words),
        "cluster_sizes": sorted(cluster_sizes, reverse=True),
        "exact_weighted_budget": exact_budget,
        "pair_affine_rank": pair_rank,
        "realized_affine_rank": w_rank,
        "high_denominator": high_denominator,
        "high_bound": high_bound,
        "high_ball_size": high_ball_size,
        "low_denominator": low_denominator,
        "low_list_bound": low_list_bound,
        "low_pair_bound": low_pair_bound,
    }


def verify_high_fixture(context):
    y0 = (0, 1, 0, 0)
    y1 = (0, 0, 0, 1)
    pairs = complete_pair_family(context, y0, y1, 2)
    expected_pairs = (
        (1, (0, 3, 0, 0, 2)),
        (4, (0, 0, 4, 1, 0)),
    )
    require(pairs == expected_pairs, "F5 high fixture complete family changed")
    metrics = verify_pair_family(
        context.q,
        context.matrix,
        context.kernel,
        context.kernel_basis,
        context.fibers[y0][0],
        y0,
        y1,
        pairs,
        2,
        context.direction_records[y1],
        "F5-high",
    )
    expected = {
        "q": 5,
        "N": 5,
        "R": 4,
        "kappa": 1,
        "t": 2,
        **metrics,
        "complete_family": True,
    }
    require(expected["direction_distance"] == 4, "F5 high direction changed")
    require(expected["realized_words"] == 1, "F5 high realized set changed")
    require(expected["cluster_sizes"] == [2], "F5 high cluster changed")
    require(expected["exact_weighted_budget"] == 2, "F5 high exact cap changed")
    require(expected["high_denominator"] == 4, "F5 high denominator changed")
    require(expected["high_bound"] == expected["high_ball_size"] == 2,
            "F5 high bound is no longer sharp")
    require(expected["low_denominator"] == 0, "F5 high low-boundary changed")
    require(expected["pair_affine_rank"] == 1, "F5 high pair rank changed")
    require(expected["realized_affine_rank"] == 0, "F5 high W rank changed")
    return expected


def verify_same_slope_fixture(context):
    y0 = (0, 1, 0)
    y1 = (0, 0, 1)
    pairs = complete_pair_family(context, y0, y1, 2)
    expected_pairs = (
        (0, (0, 3, 0, 0, 2)),
        (0, (0, 0, 4, 1, 0)),
        (1, (4, 1, 0, 0, 0)),
        (1, (0, 0, 2, 0, 3)),
        (2, (2, 0, 3, 0, 0)),
        (2, (0, 0, 0, 4, 1)),
        (3, (3, 0, 0, 2, 0)),
        (3, (0, 4, 1, 0, 0)),
        (4, (1, 0, 0, 0, 4)),
        (4, (0, 2, 0, 3, 0)),
    )
    require(pairs == expected_pairs, "F5 same-slope complete family changed")
    metrics = verify_pair_family(
        context.q,
        context.matrix,
        context.kernel,
        context.kernel_basis,
        context.fibers[y0][0],
        y0,
        y1,
        pairs,
        2,
        context.direction_records[y1],
        "F5-same-slope",
    )
    expected = {
        "q": 5,
        "N": 5,
        "R": 3,
        "kappa": 2,
        "t": 2,
        **metrics,
        "complete_family": True,
    }
    require(expected["pairs"] == 10 and expected["slopes"] == 5,
            "F5 same-slope pair/slopes changed")
    require(expected["same_slope_fibers"] == 5, "F5 slope fibers changed")
    require(expected["same_slope_excess"] == 5, "F5 slope excess changed")
    require(expected["maximum_same_slope_fiber"] == 2,
            "F5 maximum slope fiber changed")
    require(expected["realized_words"] == 8, "F5 realized set changed")
    require(expected["cluster_sizes"] == [3, 1, 1, 1, 1, 1, 1, 1],
            "F5 puncture clusters changed")
    require(expected["exact_weighted_budget"] == 10, "F5 exact cap changed")
    require(expected["pair_affine_rank"] == 3, "F5 pair rank changed")
    require(expected["realized_affine_rank"] == 2, "F5 W rank changed")
    require(expected["high_denominator"] == -1, "F5 high residual changed")
    require(expected["low_denominator"] == -2, "F5 low residual changed")
    return expected


def verify_f11_fixture():
    modulus, length, redundancy, radius = 11, 9, 8, 4
    matrix = parity_matrix(modulus, length, redundancy)
    require(
        matrix_rank(matrix, modulus) == redundancy,
        "F11 parity matrix lost full row rank",
    )
    omega = []
    for point in range(length):
        derivative = 1
        for other in range(length):
            if point != other:
                derivative = derivative * (point - other) % modulus
        omega.append(pow(derivative, -1, modulus))
    omega = tuple(omega)
    require(omega == (9, 5, 10, 2, 3, 2, 10, 5, 9), "F11 omega changed")
    require(any(omega), "F11 kernel generator vanished")
    require(
        mat_vec(matrix, omega, modulus) == (0,) * redundancy,
        "F11 omega is not in the parity kernel",
    )
    computed_kernel_basis = nullspace_basis(matrix, modulus, length)
    require(len(computed_kernel_basis) == 1, "F11 parity kernel is not one-dimensional")
    kernel_basis = (omega,)
    kernel = enumerate_code(kernel_basis, modulus, length)
    require(len(set(kernel)) == modulus, "F11 omega span has the wrong size")
    require(
        set(kernel)
        == set(enumerate_code(computed_kernel_basis, modulus, length)),
        "F11 omega does not span the full parity kernel",
    )
    require(code_distance(kernel) == 9, "F11 kernel distance changed")
    lift = (0, 0, 0, 0, 0, 0, 0, 10, 1)
    b0 = (0, 0, 0, 0, 0, 0, 0, 0, 10)
    y0 = mat_vec(matrix, b0, modulus)
    y1 = mat_vec(matrix, lift, modulus)
    require(y0 == (10, 3, 2, 5, 7, 1, 8, 9), "F11 y0 changed")
    require(y1 == (0, 1, 4, 4, 1, 0, 10, 7), "F11 y1 changed")
    pairs = []
    for gamma in range(modulus):
        for coefficient in range(modulus):
            error = add(
                add(b0, scale(gamma, lift, modulus), modulus),
                scale(coefficient, omega, modulus),
                modulus,
            )
            if weight(error) <= radius and transverse(
                matrix, y0, y1, error, modulus
            ):
                pairs.append((gamma, error))
    pairs = tuple(pairs)
    expected_pairs = (
        (0, (0, 0, 0, 0, 0, 0, 0, 0, 10)),
        (1, (0, 0, 0, 0, 0, 0, 0, 10, 0)),
    )
    require(pairs == expected_pairs, "F11 complete family changed")
    direction = build_direction_record(
        modulus, matrix, kernel, kernel_basis, y1, lift
    )
    metrics = verify_pair_family(
        modulus,
        matrix,
        kernel,
        kernel_basis,
        b0,
        y0,
        y1,
        pairs,
        radius,
        direction,
        "F11-low",
    )
    expected = {
        "q": modulus,
        "N": length,
        "R": redundancy,
        "kappa": 1,
        "t": radius,
        **metrics,
        "complete_family": True,
        "affine_solutions_exhausted": modulus * modulus,
    }
    require(expected["direction_distance"] == 2, "F11 direction changed")
    require(expected["realized_words"] == 1, "F11 realized set changed")
    require(expected["cluster_sizes"] == [2], "F11 cluster changed")
    require(expected["exact_weighted_budget"] == 2, "F11 exact cap changed")
    require(expected["high_denominator"] == -38, "F11 high denominator changed")
    require(expected["low_denominator"] == 9, "F11 low denominator changed")
    require(expected["low_list_bound"] == 2, "F11 list cap changed")
    require(expected["low_pair_bound"] == 4, "F11 pair cap changed")
    require(expected["pair_affine_rank"] == 1, "F11 pair rank changed")
    require(expected["realized_affine_rank"] == 0, "F11 W rank changed")
    return expected


def sweep_row(context, radius):
    counters = Counter()
    counters["directions"] = len(context.directions)
    counters["parameter_rows"] = len(context.directions) * len(context.target_vectors)
    maxima = {
        "maximum_pairs": 0,
        "maximum_slopes": 0,
        "maximum_same_slope_fiber": 0,
        "maximum_same_slope_excess": 0,
        "maximum_puncture_cluster": 0,
    }
    for y1 in context.directions:
        direction = context.direction_records[y1]
        for y0 in context.target_vectors:
            pairs = complete_pair_family(context, y0, y1, radius)
            if not pairs:
                continue
            metrics = verify_pair_family(
                context.q,
                context.matrix,
                context.kernel,
                context.kernel_basis,
                context.fibers[y0][0],
                y0,
                y1,
                pairs,
                radius,
                direction,
                "sweep-F{}-N{}-R{}-t{}".format(
                    context.q, context.N, context.R, radius
                ),
            )
            counters["nonempty_complete_families"] += 1
            counters["complete_pairs"] += metrics["pairs"]
            counters["distinct_slopes"] += metrics["slopes"]
            counters["families_with_same_slope_multiplicity"] += int(
                metrics["same_slope_excess"] > 0
            )
            counters["same_slope_fibers"] += metrics["same_slope_fibers"]
            counters["same_slope_excess_pairs"] += metrics["same_slope_excess"]
            counters["realized_words"] += metrics["realized_words"]
            counters["exact_weighted_budget"] += metrics["exact_weighted_budget"]
            counters["exact_weighted_equalities"] += int(
                metrics["pairs"] == metrics["exact_weighted_budget"]
            )
            counters["rank_cap_equalities"] += int(
                metrics["pair_affine_rank"] == metrics["realized_words"]
            )
            high = metrics["high_denominator"] > 0
            low = metrics["low_denominator"] > 0
            if high and low:
                counters["both_paid"] += 1
            elif high:
                counters["high_only"] += 1
            elif low:
                counters["low_only"] += 1
            else:
                counters["unpaid"] += 1
            maxima["maximum_pairs"] = max(maxima["maximum_pairs"], metrics["pairs"])
            maxima["maximum_slopes"] = max(maxima["maximum_slopes"], metrics["slopes"])
            maxima["maximum_same_slope_fiber"] = max(
                maxima["maximum_same_slope_fiber"],
                metrics["maximum_same_slope_fiber"],
            )
            maxima["maximum_same_slope_excess"] = max(
                maxima["maximum_same_slope_excess"],
                metrics["pairs"] - metrics["slopes"],
            )
            maxima["maximum_puncture_cluster"] = max(
                maxima["maximum_puncture_cluster"], max(metrics["cluster_sizes"])
            )
    return {
        "q": context.q,
        "N": context.N,
        "R": context.R,
        "kappa": context.kappa,
        "t": radius,
        **{key: counters[key] for key in (
            "directions",
            "parameter_rows",
            "nonempty_complete_families",
            "complete_pairs",
            "distinct_slopes",
            "families_with_same_slope_multiplicity",
            "same_slope_fibers",
            "same_slope_excess_pairs",
            "realized_words",
            "exact_weighted_budget",
            "exact_weighted_equalities",
            "rank_cap_equalities",
            "high_only",
            "both_paid",
            "low_only",
            "unpaid",
        )},
        **maxima,
    }


def verify_sweeps(contexts):
    rows = []
    for modulus, length, redundancy, radius in SWEEP_PARAMETERS:
        key = (modulus, length, redundancy)
        if key not in contexts:
            contexts[key] = SmallContext(*key)
        rows.append(sweep_row(contexts[key], radius))
    require(tuple(rows) == EXPECTED_SWEEP_ROWS, "complete sweep counters changed")
    totals = {}
    additive = (
        "directions",
        "parameter_rows",
        "nonempty_complete_families",
        "complete_pairs",
        "distinct_slopes",
        "families_with_same_slope_multiplicity",
        "same_slope_fibers",
        "same_slope_excess_pairs",
        "realized_words",
        "exact_weighted_budget",
        "exact_weighted_equalities",
        "rank_cap_equalities",
        "high_only",
        "both_paid",
        "low_only",
        "unpaid",
    )
    for key in additive:
        totals["direction_rows" if key == "directions" else key] = sum(
            row[key] for row in rows
        )
    for key in (
        "maximum_pairs",
        "maximum_slopes",
        "maximum_same_slope_fiber",
        "maximum_same_slope_excess",
        "maximum_puncture_cluster",
    ):
        totals[key] = max(row[key] for row in rows)
    require(totals == EXPECTED_SWEEP_TOTALS, "aggregate sweep counters changed")
    return {"rows": rows, "totals": totals}


def verify_positive_rate_arithmetic():
    rows = []
    for m in range(5, 101):
        length = 9 * m
        redundancy = 8 * m
        radius = 4 * m
        distance = 2 * m
        punctured_length = 7 * m
        punctured_distance = 6 * m + 1
        high_denominator = (length - radius) ** 2 - length * (length - distance)
        low_denominator = (
            punctured_distance * punctured_length
            - 2 * radius * punctured_length
            + radius * radius
        )
        list_bound = (
            punctured_length * (punctured_distance - radius) // low_denominator
        )
        coarse_pair_bound = distance * list_bound
        exact_cluster_bound = distance // max(1, distance - radius)
        require(high_denominator == -38 * m * m, "positive-rate high formula changed")
        require(low_denominator == m * (2 * m + 7), "positive-rate low formula changed")
        require(list_bound <= 6, "positive-rate list cap exceeds six")
        require(coarse_pair_bound <= 12 * m, "positive-rate coarse cap changed")
        require(exact_cluster_bound == distance, "positive-rate exact cluster changed")
        rows.append(
            {
                "m": m,
                "N": length,
                "R": redundancy,
                "kappa": m,
                "t": radius,
                "d": distance,
                "M": punctured_length,
                "Delta": punctured_distance,
                "high_denominator": high_denominator,
                "low_denominator": low_denominator,
                "realized_words": 1,
                "realized_pair_count": distance,
                "exact_cluster_bound": exact_cluster_bound,
                "johnson_list_bound": list_bound,
                "coarse_pair_bound": coarse_pair_bound,
            }
        )
    summary = {
        "m_min": 5,
        "m_max": 100,
        "rows": len(rows),
        "first": rows[0],
        "last": rows[-1],
        "maximum_johnson_list_bound": max(row["johnson_list_bound"] for row in rows),
        "all_low_paid": all(row["low_denominator"] > 0 for row in rows),
        "all_high_unpaid": all(row["high_denominator"] <= 0 for row in rows),
        "all_exact_clusters_sharp": all(
            row["realized_pair_count"] == row["exact_cluster_bound"] for row in rows
        ),
        "all_coarse_bounds_at_most_12m": all(
            row["coarse_pair_bound"] <= 12 * row["m"] for row in rows
        ),
    }
    require(summary["rows"] == 96, "positive-rate row count changed")
    require(summary["maximum_johnson_list_bound"] == 6,
            "positive-rate maximum list bound changed")
    return summary


def compute_summary():
    contexts = {}
    contexts[(5, 5, 4)] = SmallContext(5, 5, 4)
    contexts[(5, 5, 3)] = SmallContext(5, 5, 3)
    fixtures = {
        "high_paid_F5": verify_high_fixture(contexts[(5, 5, 4)]),
        "low_paid_F11": verify_f11_fixture(),
        "same_slope_residual_F5": verify_same_slope_fixture(contexts[(5, 5, 3)]),
    }
    return {
        "schema": 1,
        "theorem": "selector-free direction-distance all-pair compiler",
        "formulas": FORMULAS,
        "fixtures": fixtures,
        "sweeps": verify_sweeps(contexts),
        "positive_rate_arithmetic": verify_positive_rate_arithmetic(),
    }


def reject_json_constant(value):
    raise VerificationError("nonstandard JSON constant: " + value)


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_certificate_text(text):
    try:
        return json.loads(
            text,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_json_constant,
        )
    except json.JSONDecodeError as error:
        raise VerificationError("invalid certificate JSON: " + str(error)) from error


def strict_equal(first, second):
    if type(first) is not type(second):
        return False
    if isinstance(first, dict):
        return first.keys() == second.keys() and all(
            strict_equal(first[key], second[key]) for key in first
        )
    if isinstance(first, list):
        return len(first) == len(second) and all(
            strict_equal(left, right) for left, right in zip(first, second)
        )
    return first == second


def expected_certificate(summary):
    return {
        "schema": 1,
        "status": "PROVED",
        "lean_status": "UNPROVED STATEMENT TARGET",
        "hard_input": 3,
        "theorem": summary["theorem"],
        "formulas": FORMULAS,
        "sources": EXPECTED_SOURCES,
        "computed_summary": summary,
        "nonclaims": EXPECTED_NONCLAIMS,
    }


def load_certificate():
    require(CERTIFICATE.is_file(), "certificate file is missing")
    try:
        text = CERTIFICATE.read_text(encoding="utf-8")
    except OSError as error:
        raise VerificationError("cannot read certificate: " + str(error)) from error
    return parse_certificate_text(text)


def validate_certificate(certificate, summary):
    require(type(certificate) is dict, "certificate root is not an object")
    require(certificate.keys() == EXPECTED_CERTIFICATE_KEYS,
            "certificate top-level keys mismatch")
    require(type(certificate["schema"]) is int and certificate["schema"] == 1,
            "certificate schema mismatch")
    require(type(certificate["status"]) is str and certificate["status"] == "PROVED",
            "certificate status mismatch")
    require(
        type(certificate["lean_status"]) is str
        and certificate["lean_status"] == "UNPROVED STATEMENT TARGET",
        "certificate Lean status mismatch",
    )
    require(type(certificate["hard_input"]) is int and certificate["hard_input"] == 3,
            "certificate hard-input mismatch")
    require(certificate["theorem"] == summary["theorem"], "certificate theorem mismatch")
    require(strict_equal(certificate["formulas"], FORMULAS), "certificate formulas mismatch")
    require(strict_equal(certificate["sources"], EXPECTED_SOURCES), "certificate sources mismatch")
    require(strict_equal(certificate["computed_summary"], summary),
            "certificate computed summary mismatch")
    require(strict_equal(certificate["nonclaims"], EXPECTED_NONCLAIMS),
            "certificate nonclaims mismatch")


def tamper_selftest(summary):
    certificate = load_certificate()
    validate_certificate(certificate, summary)
    mutations = []

    changed = copy.deepcopy(certificate)
    changed["status"] = "CONDITIONAL"
    mutations.append(("status", changed))

    for formula_name in ("realized_weighted", "high", "low"):
        changed = copy.deepcopy(certificate)
        changed["formulas"][formula_name] = "tampered"
        mutations.append(("formula-" + formula_name, changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["fixtures"]["high_paid_F5"]["pairs"] += 1
    mutations.append(("high-fixture", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["fixtures"]["low_paid_F11"]["realized_words"] += 1
    mutations.append(("low-fixture", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["fixtures"]["same_slope_residual_F5"][
        "same_slope_excess"
    ] -= 1
    mutations.append(("same-slope-fixture", changed))

    for counter_name in (
        "complete_pairs",
        "same_slope_fibers",
        "realized_words",
        "rank_cap_equalities",
    ):
        changed = copy.deepcopy(certificate)
        changed["computed_summary"]["sweeps"]["totals"][counter_name] += 1
        mutations.append(("sweep-" + counter_name, changed))

    changed = copy.deepcopy(certificate)
    changed["sources"]["all_pair_affine_core"]["head"] = "tampered"
    mutations.append(("source-pin", changed))

    changed = copy.deepcopy(certificate)
    changed["nonclaims"] = changed["nonclaims"][:-1]
    mutations.append(("nonclaim", changed))

    changed = copy.deepcopy(certificate)
    changed["unexpected"] = "payload"
    mutations.append(("unknown-key", changed))

    changed = copy.deepcopy(certificate)
    changed["schema"] = True
    mutations.append(("schema-type-alias", changed))

    changed = copy.deepcopy(certificate)
    changed["computed_summary"]["positive_rate_arithmetic"]["all_low_paid"] = 1
    mutations.append(("boolean-type-alias", changed))

    parser_tampers = (
        ("duplicate-key", '{"schema": 1, "schema": 1}'),
        ("nonstandard-constant", '{"value": NaN}'),
    )
    rejected = 0
    for name, mutation in mutations:
        try:
            validate_certificate(mutation, summary)
        except VerificationError:
            rejected += 1
            continue
        raise VerificationError("tamper was accepted: " + name)
    for name, text in parser_tampers:
        try:
            parse_certificate_text(text)
        except VerificationError:
            rejected += 1
            continue
        raise VerificationError("parser tamper was accepted: " + name)
    tamper_cases = len(mutations) + len(parser_tampers)
    require(tamper_cases == 18, "tamper class count changed")
    require(rejected == tamper_cases, "not every tamper was rejected")
    return {"tamper_cases": tamper_cases, "rejected": rejected}


def parse_args(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--summary-only", action="store_true")
    group.add_argument("--check", action="store_true")
    group.add_argument("--tamper-selftest", action="store_true")
    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    try:
        summary = compute_summary()
        if args.summary_only:
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        if args.check:
            validate_certificate(load_certificate(), summary)
            print(json.dumps({"status": "ok", "summary": summary}, sort_keys=True))
            return 0
        result = tamper_selftest(summary)
        print(json.dumps({"status": "ok", **result}, sort_keys=True))
        return 0
    except VerificationError as error:
        print("verification failed: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
